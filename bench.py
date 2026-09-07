# /// script
# requires-python = ">=3.10"
# dependencies = ["reacao[gpu,pyfeat,libreface] @ git+https://github.com/ds-fabiopinheiro/church-sentiment-analysis", "huggingface_hub>=0.30", "pandas>=2.0"]
# ///
"""Teste comparativo de motores no corpus rotulado (PBI-000H). O que cada coluna mede:

Critério 1 (recall em rostos ≥ 64 px), por quadro rotulado:
- `recall_ge64_max`: soma de min(detectados, marcados) por quadro, sobre o total marcado. É o limite SUPERIOR
  do recall pareado, sempre ≤ 1: se ele fica abaixo da meta, o critério reprova com certeza. É este o número do gate.
- `razao_contagem_ge64`: detectados sobre marcados, sem pareamento. Pode passar de 1 com falso positivo, e pode
  dar exatamente 1 escondendo perdas compensadas por falsos positivos. Diagnóstico, não critério.
- `discrepancia_rel` e `quadros_rotulados_sem_deteccao`: assinatura dessa compensação.

Critério 2 (sensibilidade a riso), um valor por intervalo ROTULADO:
Cada intervalo de `_eventos.csv` é agregado sobre os seus próprios quadros, numa janela alinhada ao intervalo, e não
sobre uma grade fixa. Assim a medida não depende da duração do evento nem da fase da grade, e a mesma janela não
entra como riso e como neutro. O k-mínimo (regra 3 do CLAUDE.md) continua valendo por intervalo.
- `frac_eventos_riso_ok`: eventos de riso que sobem ≥ `--limiar-riso` p.p. sobre a base neutra, sobre o total de
  eventos ROTULADOS. Evento sem k suficiente conta como não atingido; `frac_sobre_medidos` mostra a outra leitura.
- `frac_equiv30`: o mesmo, com a subida convertida para a janela de 30 s da produção (`reacao/types.py WINDOW_S`),
  onde um riso mais curto que a janela é diluído por min(duração, 30)/30.
- `jitter_dp_pp`: desvio-padrão de `pct_sorrindo` entre os trechos neutros. Invariante ao número de trechos.
  `jitter_amplitude_pp` (máximo menos mínimo) fica como diagnóstico: cresce com o número de trechos rotulados.

A linha `TOTAL` é a do gate: as metas valem sobre o corpus inteiro, não por vídeo. Cada evento é comparado à base
neutra do seu próprio vídeo; o que se soma são os eventos, não os percentuais.

labels/<video>_faces.csv:   t_s, altura_px            (um rosto por linha, nos quadros amostrados)
labels/<video>_eventos.csv: t_ini_s, t_fim_s, tipo    (riso | aplauso | pe | cabeca_baixa | neutro)

Validar os rótulos antes: `uv run python tools/validar_labels.py --labels <pasta> --corpus <pasta>`.
"""
from __future__ import annotations
import argparse
import glob
import os
import shutil
import statistics
import time
from collections import Counter

import pandas as pd

from reacao import detect, ingest
from reacao.aggregate import aggregate
from reacao.cost import PRICE_PER_HOUR
from reacao.guard import no_persistence
from reacao.providers import get_provider
from reacao.types import MIN_MEASURABLE_HEIGHT_PX, WINDOW_S

HF_PREFIX = "hf://datasets/"
SHM_BENCH = "/dev/shm/reacao-bench"    # vídeos baixados vivem em memória, nunca em disco (regra 1 do CLAUDE.md)
JANELA_UNICA_S = 10 ** 6               # agrega um intervalo inteiro como uma janela só
MIN_TRECHOS_JITTER = 4                 # abaixo disso o desvio-padrão não diz nada
NAN = float("nan")


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


def valor_do_intervalo(nome: str, obs, ftimes: list[float], aud: set[float], t0: float, t1: float,
                       field: str = "pct_sorrindo") -> float | None:
    """Agrega os quadros de [t0, t1] numa janela só. None quando não há quadro ou o k-mínimo não é alcançado."""
    ft = [t for t in ftimes if t0 <= t <= t1]
    if not ft:
        return None
    dentro = [o for o in obs if t0 <= o.t <= t1]
    a = aggregate(nome, "bench", dentro, ft, {t for t in aud if t0 <= t <= t1}, window_s=JANELA_UNICA_S)[0]
    return None if a.insuficiente else getattr(a, field)


def valores_por_tipo(nome: str, obs, ftimes: list[float], aud: set[float], eventos: pd.DataFrame,
                     tipo: str) -> list[tuple[float, float | None]]:
    """Um par (duração, valor) por intervalo rotulado do tipo. valor None = sem k suficiente para medir."""
    saida = []
    for _, ev in eventos[eventos.tipo == tipo].iterrows():
        t0, t1 = float(ev.t_ini_s), float(ev.t_fim_s)
        saida.append((t1 - t0, valor_do_intervalo(nome, obs, ftimes, aud, t0, t1)))
    return saida


def mediana(vals: list[float]) -> float:
    return statistics.median(vals) if vals else NAN


def _div(a: float, b: float) -> float:
    return a / b if b else NAN


def analisar_video(video: str, prov, min_faces_plateia: int, fps_amostragem: float) -> dict:
    """Repete o laço de produção: pré-filtro em 640, detecção plena só no quadro com plateia."""
    obs_all, ftimes, aud = [], [], set()
    det_por_t: Counter[int] = Counter()
    inferencia_s = 0.0
    for t, frame in ingest.frames(video, fps_amostragem):
        t_inf = time.perf_counter()
        small = detect.detect(ingest.downscale(frame, 640), t, det_size=(640, 640))
        if len(small) < min_faces_plateia:
            inferencia_s += time.perf_counter() - t_inf
            ftimes.append(t)                       # conta em `quadros`, não em `quadros_com_plateia`
            continue
        obs = prov.analyze(frame, detect.detect(frame, t))
        inferencia_s += time.perf_counter() - t_inf
        obs_all.extend(obs)
        ftimes.append(t)
        aud.add(t)
        det_por_t[int(round(t))] += sum(1 for o in obs if o.measurable)
    return {"obs": obs_all, "ftimes": ftimes, "aud": aud, "det_por_t": det_por_t, "inferencia_s": inferencia_s}


def medir_recall(det_por_t: Counter[int], manual: pd.DataFrame) -> dict:
    """Pareia por quadro: o rótulo tem `t_s`, então min(detectados, marcados) por quadro é um limite superior real."""
    man_por_t = Counter(manual[manual.altura_px >= MIN_MEASURABLE_HEIGHT_PX].t_s.round().astype(int).tolist())
    marcados = sum(man_por_t.values())
    detectados = sum(det_por_t[t] for t in man_por_t)
    pares = sum(min(det_por_t[t], n) for t, n in man_por_t.items())
    discrepancia = sum(abs(det_por_t[t] - n) for t, n in man_por_t.items())
    return {"rostos_marcados_ge64": marcados, "rostos_detectados_ge64": detectados, "pares_ge64": pares,
            "razao_contagem_ge64": round(_div(detectados, marcados), 3),
            "recall_ge64_max": round(_div(pares, marcados), 3),
            "discrepancia_rel": round(_div(discrepancia, marcados), 3),
            "quadros_rotulados_sem_deteccao": sum(1 for t, n in man_por_t.items() if n and not det_por_t[t])}


def medir_criterio2(risos: list[tuple[float, float | None]], base: float, limiar_pp: float) -> dict:
    """Cada riso rotulado contra a base neutra do próprio vídeo. Denominador do gate: risos ROTULADOS."""
    medidos = [(d, v) for d, v in risos if v is not None]
    ok = ok30 = 0
    if base == base:
        for d, v in medidos:
            subida = v - base
            ok += subida >= limiar_pp
            ok30 += subida * min(d, WINDOW_S) / WINDOW_S >= limiar_pp     # o que a janela de produção veria
    duracoes = [d for d, _ in risos]
    return {"eventos_riso_rotulados": len(risos), "eventos_riso_medidos": len(medidos) if base == base else 0,
            "eventos_riso_ok": ok, "eventos_riso_ok_equiv30": ok30,
            "frac_eventos_riso_ok": round(_div(ok, len(risos)), 2) if risos and base == base else NAN,
            "frac_sobre_medidos": round(_div(ok, len(medidos)), 2) if medidos and base == base else NAN,
            "frac_equiv30": round(_div(ok30, len(risos)), 2) if risos and base == base else NAN,
            "dur_riso_mediana_s": round(mediana(duracoes), 1) if duracoes else NAN}


def medir_jitter(neutros: list[float]) -> dict:
    suficiente = len(neutros) >= MIN_TRECHOS_JITTER
    return {"trechos_neutros_medidos": len(neutros),
            "jitter_dp_pp": round(statistics.stdev(neutros), 1) if suficiente else NAN,
            "jitter_amplitude_pp": round(max(neutros) - min(neutros), 1) if suficiente else NAN}


def linha_total(rows: list[dict], provider: str) -> dict:
    """Metas do gate valem aqui: eventos somados entre vídeos, cada um contra a base neutra do seu vídeo."""
    def soma(coluna: str) -> float:
        return sum(r[coluna] for r in rows)

    jitters = [r["jitter_dp_pp"] for r in rows if r["jitter_dp_pp"] == r["jitter_dp_pp"]]
    neutros_total = soma("trechos_neutros_medidos")
    return {"video": "TOTAL", "provider": provider,
            "recall_ge64_max": round(_div(soma("pares_ge64"), soma("rostos_marcados_ge64")), 3),
            "razao_contagem_ge64": round(_div(soma("rostos_detectados_ge64"), soma("rostos_marcados_ge64")), 3),
            "rostos_marcados_ge64": soma("rostos_marcados_ge64"), "rostos_detectados_ge64": soma("rostos_detectados_ge64"),
            "quadros_rotulados_sem_deteccao": soma("quadros_rotulados_sem_deteccao"),
            "eventos_riso_rotulados": soma("eventos_riso_rotulados"), "eventos_riso_medidos": soma("eventos_riso_medidos"),
            "eventos_riso_ok": soma("eventos_riso_ok"), "eventos_riso_ok_equiv30": soma("eventos_riso_ok_equiv30"),
            "frac_eventos_riso_ok": round(_div(soma("eventos_riso_ok"), soma("eventos_riso_rotulados")), 2),
            "frac_equiv30": round(_div(soma("eventos_riso_ok_equiv30"), soma("eventos_riso_rotulados")), 2),
            "trechos_neutros_medidos": neutros_total,
            "jitter_dp_pp": round(max(jitters), 1) if jitters else NAN,     # pior vídeo, não a média
            "quadros": soma("quadros"), "quadros_com_plateia": soma("quadros_com_plateia"),
            "fps": round(_div(soma("quadros"), soma("inferencia_s")), 2),
            "custo_por_hora_video_usd": round(PRICE_PER_HOUR.get(rows[0]["flavor"], 0.0)
                                              * _div(soma("inferencia_s"), soma("quadros")), 3)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Teste comparativo de motores no corpus rotulado.")
    ap.add_argument("--corpus", required=True, help="pasta local com os vídeos, ou hf://datasets/<usuario>/<repo>[/<sub>]")
    ap.add_argument("--labels", required=True, help="pasta local dos rótulos, ou hf://datasets/...")
    ap.add_argument("--provider", required=True)
    ap.add_argument("--flavor", default="t4-small")
    ap.add_argument("--fps-amostragem", type=float, default=1.0)
    ap.add_argument("--min-faces-plateia", type=int, default=5, help="igual ao padrão de processar_culto.py")
    ap.add_argument("--limiar-riso", type=float, default=15.0, help="subida mínima em p.p. para o evento contar (critério 2)")
    ap.add_argument("--out", default="out/bench")
    args = ap.parse_args(argv)
    os.makedirs(args.out, exist_ok=True)
    brutos: list[dict] = []
    sem_rotulo: list[str] = []
    try:
        cache: dict[str, str] = {}
        corpus, labels = resolve_pasta(args.corpus, cache), resolve_pasta(args.labels, cache)
        videos = sorted(glob.glob(os.path.join(corpus, "*.mp4")))
        if not videos:
            print(f"[bench] nenhum .mp4 em {corpus} — nada medido")
            return 1
        with no_persistence([os.getcwd(), "/tmp"]):
            prov = get_provider(args.provider)
            for video in videos:
                nome = os.path.splitext(os.path.basename(video))[0]
                faces_csv = os.path.join(labels, f"{nome}_faces.csv")
                ev_csv = os.path.join(labels, f"{nome}_eventos.csv")
                if not os.path.exists(faces_csv):
                    sem_rotulo.append(nome)
                    continue
                manual = pd.read_csv(faces_csv)
                eventos = pd.read_csv(ev_csv) if os.path.exists(ev_csv) else pd.DataFrame(columns=["t_ini_s", "t_fim_s", "tipo"])
                eventos["tipo"] = eventos["tipo"].astype(str).str.strip().str.lower()   # o validador normaliza; o bench também
                a = analisar_video(video, prov, args.min_faces_plateia, args.fps_amostragem)
                neutros = [v for _, v in valores_por_tipo(nome, a["obs"], a["ftimes"], a["aud"], eventos, "neutro") if v is not None]
                brutos.append({"video": nome, "provider": args.provider, "flavor": args.flavor,
                               "risos": valores_por_tipo(nome, a["obs"], a["ftimes"], a["aud"], eventos, "riso"),
                               "neutros": neutros, "inferencia_s": a["inferencia_s"],
                               "quadros": len(a["ftimes"]), "quadros_com_plateia": len(a["aud"]),
                               **medir_recall(a["det_por_t"], manual)})
    finally:
        shutil.rmtree(SHM_BENCH, ignore_errors=True)
    if sem_rotulo:
        print(f"[bench] {len(sem_rotulo)} vídeo(s) sem <nome>_faces.csv, fora da medição: {', '.join(sem_rotulo[:10])}")
    if not brutos:
        print("[bench] nenhum vídeo rotulado — nada medido")
        return 1

    todos_neutros = [v for b in brutos for v in b["neutros"]]
    base_corpus = mediana(todos_neutros)
    rows = []
    for b in brutos:
        base, origem = (mediana(b["neutros"]), "video") if b["neutros"] else (base_corpus, "corpus")
        row = {k: v for k, v in b.items() if k not in ("risos", "neutros")}
        row.update(base_neutra_pp=round(base, 1) if base == base else NAN, base_origem=origem if base == base else "sem",
                   **medir_criterio2(b["risos"], base, args.limiar_riso), **medir_jitter(b["neutros"]))
        row.update(fps=round(_div(row["quadros"], row["inferencia_s"]), 2))
        # a 1 quadro/s, uma hora de vídeo são 3600 quadros: custo = preço por hora × segundos de inferência por quadro
        row["custo_por_hora_video_usd"] = round(PRICE_PER_HOUR.get(args.flavor, 0.0)
                                                * _div(row["inferencia_s"], row["quadros"]), 3)
        rows.append(row)
    df = pd.DataFrame(rows + [linha_total(rows, args.provider)])
    df.to_csv(os.path.join(args.out, f"bench_{args.provider}.csv"), index=False)
    print(df.drop(columns=["flavor", "inferencia_s", "pares_ge64"], errors="ignore").to_string(index=False))
    sem_base = [r["video"] for r in rows if r["base_origem"] != "video"]
    if sem_base:
        print(f"\n[bench] {len(sem_base)} vídeo(s) sem trecho neutro próprio usaram a base do corpus "
              f"(mediana de {len(todos_neutros)} trechos): {', '.join(sem_base[:8])}")
    print(f"\nGate (linha TOTAL): recall_ge64_max ≥ 0,80 | frac_eventos_riso_ok ≥ 0,70 com subida ≥ {args.limiar_riso:.0f} p.p. "
          f"| jitter_dp_pp ≤ meta de docs/poc-gate.md | fps ≥ 1"
          f"\nAs linhas por vídeo são diagnóstico. NaN significa que faltou rótulo ou k-mínimo para a métrica existir, "
          f"não que o motor falhou; eventos rotulados sem k suficiente já contam como não atingidos em frac_eventos_riso_ok.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
