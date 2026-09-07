# /// script
# requires-python = ">=3.10"
# dependencies = ["reacao[gpu,pyfeat,libreface] @ git+https://github.com/ds-fabiopinheiro/church-sentiment-analysis", "huggingface_hub>=0.30", "pandas>=2.0"]
# ///
"""Teste comparativo de motores no corpus rotulado (PBI-000H).

Métricas por motor e por vídeo:
- `recall_ge64`: rostos mensuráveis detectados / rostos de altura ≥ 64 px marcados à mão, nos quadros rotulados.
  Razão de contagens, não pareamento por posição: os rótulos não têm caixa, só tempo e altura (critério 1 do gate).
- `sensibilidade_pp`: média de `pct_sorrindo` nas janelas de riso menos a média nas janelas neutras.
- `frac_eventos_riso_ok`: fração dos eventos de riso cujo pico de `pct_sorrindo` sobe ≥ `--limiar-riso` p.p.
  sobre a mediana das janelas neutras. É a métrica do critério 2 do gate ("≥ 15 p.p. em ≥ 70% dos eventos").
- `jitter_pp`: amplitude (máximo menos mínimo) de `pct_sorrindo` nas janelas neutras.
- `fps`: quadros analisados por segundo, cronometrando só detecção e motor de expressão (não a decodificação).
- `custo_por_hora_video_usd`: preço do hardware dividido pelo fps, para amostragem a 1 quadro por segundo.

labels/<video>_faces.csv:   t_s, altura_px            (um rosto por linha, nos quadros amostrados)
labels/<video>_eventos.csv: t_ini_s, t_fim_s, tipo    (riso | aplauso | pe | cabeca_baixa | neutro)

Validar os rótulos antes: `uv run python tools/validar_labels.py --corpus <pasta> --labels <pasta>/labels`.
"""
from __future__ import annotations
import argparse
import glob
import os
import shutil
import time
import pandas as pd

HF_PREFIX = "hf://datasets/"
SHM_BENCH = "/dev/shm/reacao-bench"     # vídeos baixados vivem em memória, nunca em disco (regra 1 do CLAUDE.md)


def resolve_pasta(uri: str, cache: dict[str, str]) -> str:
    """Resolve `hf://datasets/<usuario>/<repo>[/<sub>]` para uma pasta local em /dev/shm. Caminho local passa direto."""
    if not uri.startswith(HF_PREFIX):
        return uri
    partes = uri[len(HF_PREFIX):].split("/")
    if len(partes) < 2:
        raise ValueError(f"URI de dataset incompleta: {uri} (esperado {HF_PREFIX}<usuario>/<repo>[/<sub>])")
    repo_id, sub = "/".join(partes[:2]), "/".join(partes[2:])
    if repo_id not in cache:
        from huggingface_hub import snapshot_download
        cache[repo_id] = snapshot_download(repo_id=repo_id, repo_type="dataset",
                                           local_dir=os.path.join(SHM_BENCH, repo_id.replace("/", "__")))
    return os.path.join(cache[repo_id], sub) if sub else cache[repo_id]


def janelas_no_intervalo(aggs, t_ini: float, t_fim: float, field: str) -> list[float]:
    """Valores de `field` nas janelas suficientes que se sobrepõem ao intervalo [t_ini, t_fim]."""
    return [getattr(a, field) for a in aggs
            if not a.insuficiente and getattr(a, field) is not None and a.t_fim > t_ini and a.t_ini < t_fim]


def valores_por_tipo(aggs, eventos: pd.DataFrame, tipo: str, field: str) -> list[float]:
    vals: list[float] = []
    for _, ev in eventos[eventos.tipo == tipo].iterrows():
        vals += janelas_no_intervalo(aggs, float(ev.t_ini_s), float(ev.t_fim_s), field)
    return vals


def media(vals: list[float]) -> float:
    return sum(vals) / len(vals) if vals else float("nan")


def mediana(vals: list[float]) -> float:
    if not vals:
        return float("nan")
    s = sorted(vals)
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


def fracao_eventos_sensiveis(aggs, eventos: pd.DataFrame, base: float, limiar_pp: float) -> tuple[float, int]:
    """Fração dos eventos de riso cujo pico de sorriso sobe ≥ limiar_pp sobre a base neutra, e quantos foram medidos."""
    picos = []
    for _, ev in eventos[eventos.tipo == "riso"].iterrows():
        vals = janelas_no_intervalo(aggs, float(ev.t_ini_s), float(ev.t_fim_s), "pct_sorrindo")
        if vals:
            picos.append(max(vals))
    if not picos or base != base:      # sem eventos medíveis ou base NaN
        return float("nan"), len(picos)
    return sum(1 for p in picos if p - base >= limiar_pp) / len(picos), len(picos)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "bench")
    ap.add_argument("--corpus", required=True, help="pasta local com os vídeos, ou hf://datasets/<usuario>/<repo>[/<sub>]")
    ap.add_argument("--labels", required=True, help="pasta local dos rótulos, ou hf://datasets/...")
    ap.add_argument("--provider", required=True)
    ap.add_argument("--flavor", default="t4-small")
    ap.add_argument("--fps-amostragem", type=float, default=1.0)
    ap.add_argument("--janela-s", type=int, default=10, help="janela de agregação do bench, menor que os 30 s de produção")
    ap.add_argument("--limiar-riso", type=float, default=15.0, help="subida mínima em p.p. para o evento contar (critério 2)")
    ap.add_argument("--out", default="out/bench")
    args = ap.parse_args(argv)
    from reacao.guard import no_persistence
    from reacao import ingest, detect
    from reacao.providers import get_provider
    from reacao.aggregate import aggregate
    from reacao.cost import PRICE_PER_HOUR
    os.makedirs(args.out, exist_ok=True)
    rows: list[dict] = []
    sem_rotulo: list[str] = []
    try:
        cache: dict[str, str] = {}
        corpus = resolve_pasta(args.corpus, cache)
        labels = resolve_pasta(args.labels, cache)
        videos = sorted(glob.glob(os.path.join(corpus, "*.mp4")))
        if not videos:
            print(f"[bench] nenhum .mp4 em {corpus} — nada medido")
            return 1
        with no_persistence([os.getcwd(), "/tmp"]):
            prov = get_provider(args.provider)
            for video in videos:
                name = os.path.splitext(os.path.basename(video))[0]
                faces_csv = os.path.join(labels, f"{name}_faces.csv")
                ev_csv = os.path.join(labels, f"{name}_eventos.csv")
                if not os.path.exists(faces_csv):
                    sem_rotulo.append(name)
                    continue
                manual = pd.read_csv(faces_csv)
                eventos = pd.read_csv(ev_csv) if os.path.exists(ev_csv) else pd.DataFrame(columns=["t_ini_s", "t_fim_s", "tipo"])
                sampled_t = sorted(set(manual.t_s.round().astype(int)))
                det_meas = 0
                n_frames = 0
                inferencia_s = 0.0
                obs_all, ftimes = [], []
                for t, frame in ingest.frames(video, args.fps_amostragem):
                    em_evento = not eventos.empty and ((eventos.t_ini_s <= t) & (eventos.t_fim_s >= t)).any()
                    if int(round(t)) not in sampled_t and not em_evento:
                        continue
                    t_inf = time.perf_counter()
                    faces = detect.detect(frame, t)
                    obs = prov.analyze(frame, faces)
                    inferencia_s += time.perf_counter() - t_inf     # só o motor, sem a decodificação do vídeo
                    obs_all.extend(obs)
                    ftimes.append(t)
                    n_frames += 1
                    if int(round(t)) in sampled_t:
                        det_meas += sum(1 for o in obs if o.measurable)
                man_meas = int((manual.altura_px >= 64).sum())
                recall = det_meas / man_meas if man_meas else float("nan")
                aggs = aggregate(name, "bench", obs_all, ftimes, set(ftimes), window_s=args.janela_s)
                riso = valores_por_tipo(aggs, eventos, "riso", "pct_sorrindo")
                neutro = valores_por_tipo(aggs, eventos, "neutro", "pct_sorrindo")
                base_neutra = mediana(neutro)
                frac_ok, n_eventos = fracao_eventos_sensiveis(aggs, eventos, base_neutra, args.limiar_riso)
                jitter = (max(neutro) - min(neutro)) if len(neutro) > 1 else float("nan")
                fps = n_frames / inferencia_s if inferencia_s > 0 else float("nan")
                rows.append({"video": name, "provider": args.provider,
                             "recall_ge64": round(recall, 3), "rostos_marcados_ge64": man_meas, "rostos_detectados_ge64": det_meas,
                             "sensibilidade_pp": round(media(riso) - media(neutro), 1),
                             "frac_eventos_riso_ok": round(frac_ok, 2), "eventos_riso_medidos": n_eventos,
                             "jitter_pp": round(jitter, 1), "janelas_neutras": len(neutro),
                             "fps": round(fps, 2),
                             "custo_por_hora_video_usd": round(PRICE_PER_HOUR.get(args.flavor, 0.0) / fps, 3) if fps == fps and fps > 0 else float("nan"),
                             "janela_s": args.janela_s, "quadros_analisados": n_frames})
    finally:
        shutil.rmtree(SHM_BENCH, ignore_errors=True)
    if sem_rotulo:
        print(f"[bench] {len(sem_rotulo)} vídeo(s) sem <nome>_faces.csv, fora da medição: {', '.join(sem_rotulo[:10])}")
    df = pd.DataFrame(rows)
    if df.empty:
        print("[bench] nenhum vídeo rotulado — nada medido")
        return 1
    df.to_csv(os.path.join(args.out, f"bench_{args.provider}.csv"), index=False)
    print(df.to_string(index=False))
    print(f"\nCritérios do gate: recall_ge64 ≥ 0,80 | frac_eventos_riso_ok ≥ 0,70 (subida ≥ {args.limiar_riso:.0f} p.p.) "
          f"| jitter_pp ≤ 5 | fps ≥ 1\nNaN significa sem rótulo suficiente para a métrica, não falha do motor.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
