# /// script
# requires-python = ">=3.10"
# dependencies = ["reacao[gpu] @ git+https://github.com/ds-fabiopinheiro/church-sentiment-analysis", "huggingface_hub>=0.30", "pandas>=2.0"]
# ///
"""Teste comparativo de motores no corpus rotulado (PBI-000H).
Métricas por motor: recall (rostos ≥ 64 px vs contagem manual), jitter (p.p. entre janelas em trechos neutros),
sensibilidade (subida de sorriso/expressividade nos eventos de riso marcados), fps sustentado, custo por hora de vídeo.

labels/<video>_faces.csv:   t_s, altura_px            (um rosto por linha, nos 20 quadros amostrados)
labels/<video>_eventos.csv: t_ini_s, t_fim_s, tipo    (riso | aplauso | pe | cabeca_baixa | neutro)
"""
from __future__ import annotations
import argparse
import glob
import os
import time
import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True, help="pasta local com os vídeos (ou hf://datasets/...)")
    ap.add_argument("--labels", required=True)
    ap.add_argument("--provider", required=True)
    ap.add_argument("--flavor", default="t4-small")
    ap.add_argument("--out", default="out/bench")
    args = ap.parse_args()
    from reacao.guard import no_persistence
    from reacao import ingest, detect
    from reacao.providers import get_provider
    from reacao.aggregate import aggregate
    from reacao.cost import PRICE_PER_HOUR
    os.makedirs(args.out, exist_ok=True)
    rows = []
    with no_persistence([os.getcwd(), "/tmp"]):
        prov = get_provider(args.provider)
        for video in sorted(glob.glob(os.path.join(args.corpus, "*.mp4"))):
            name = os.path.splitext(os.path.basename(video))[0]
            faces_csv = os.path.join(args.labels, f"{name}_faces.csv")
            ev_csv = os.path.join(args.labels, f"{name}_eventos.csv")
            if not os.path.exists(faces_csv):
                continue
            manual = pd.read_csv(faces_csv)
            eventos = pd.read_csv(ev_csv) if os.path.exists(ev_csv) else pd.DataFrame(columns=["t_ini_s", "t_fim_s", "tipo"])
            sampled_t = sorted(set(manual.t_s.round().astype(int)))
            # recall nos quadros rotulados
            t0 = time.time()
            det_meas = 0
            n_frames = 0
            obs_all, ftimes = [], []
            for t, frame in ingest.frames(video, 1.0):
                if int(round(t)) in sampled_t or not eventos.empty and ((eventos.t_ini_s <= t) & (eventos.t_fim_s >= t)).any():
                    faces = detect.detect(frame, t)
                    obs = prov.analyze(frame, faces)
                    obs_all.extend(obs)
                    ftimes.append(t)
                    n_frames += 1
                    if int(round(t)) in sampled_t:
                        det_meas += sum(1 for o in obs if o.measurable)
            elapsed = max(1e-6, time.time() - t0)
            man_meas = int((manual.altura_px >= 64).sum())
            recall = det_meas / man_meas if man_meas else float("nan")
            aggs = aggregate(name, "bench", obs_all, ftimes, set(ftimes), window_s=10)
            def mean_in(tipo, field):
                vals = [getattr(a, field) for a in aggs if not a.insuficiente and getattr(a, field) is not None and
                        ((eventos.tipo == tipo) & (eventos.t_ini_s <= a.t_ini) & (eventos.t_fim_s >= a.t_ini)).any()]
                return sum(vals) / len(vals) if vals else float("nan")
            smile_riso, smile_neutro = mean_in("riso", "pct_sorrindo"), mean_in("neutro", "pct_sorrindo")
            neutro_vals = [a.pct_sorrindo for a in aggs if not a.insuficiente and a.pct_sorrindo is not None and
                           ((eventos.tipo == "neutro") & (eventos.t_ini_s <= a.t_ini) & (eventos.t_fim_s >= a.t_ini)).any()]
            jitter = (max(neutro_vals) - min(neutro_vals)) if len(neutro_vals) > 1 else float("nan")
            rows.append({"video": name, "provider": args.provider, "recall_ge64": round(recall, 3),
                         "sensibilidade_pp": round(smile_riso - smile_neutro, 1), "jitter_pp": round(jitter, 1),
                         "fps": round(n_frames / elapsed, 2), "custo_por_hora_video_usd": round(3600 / max(1e-6, n_frames / elapsed) / 3600 * PRICE_PER_HOUR.get(args.flavor, 0), 3)})
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(args.out, f"bench_{args.provider}.csv"), index=False)
    print(df.to_string(index=False))
    print("\nCritérios: recall_ge64 ≥ 0.80 | sensibilidade_pp ≥ 15 | jitter_pp ≤ 5 | fps ≥ 1")


if __name__ == "__main__":
    main()
