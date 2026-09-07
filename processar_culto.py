# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "reacao[gpu,llm] @ git+https://github.com/ds-fabiopinheiro/church-sentiment-analysis",
#   "huggingface_hub>=0.30",
# ]
# ///
"""Processa UM culto: vídeo → rostos (só detecção) → expressão/pose em rostos ≥ 64 px → agregados por 30 s (k ≥ 10)
→ transcrição do púlpito → momentos → eventos → insights (lint) → Supabase ou JSON local. Nenhum quadro em disco.

Local:   uv run python processar_culto.py --video x.mp4 --culto teste --provider mock --out out/
HF Jobs: hf jobs uv run --flavor t4-small --timeout 3h --secret SUPABASE_URL=... --secret SUPABASE_SERVICE_KEY=... \
         --secret ANTHROPIC_API_KEY=... --secret HF_TOKEN=... processar_culto.py --video hf://datasets/u/corpus/c1.mp4 --culto poc-01
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from dataclasses import asdict


def resolve_video(path: str) -> str:
    if path.startswith("hf://datasets/"):
        from huggingface_hub import hf_hub_download
        repo, _, fname = path[len("hf://datasets/"):].partition("/")
        # repo pode ter dois níveis: usuario/nome; o resto é o arquivo
        parts = (repo + "/" + fname).split("/")
        repo_id, filename = "/".join(parts[:2]), "/".join(parts[2:])
        return hf_hub_download(repo_id=repo_id, filename=filename, repo_type="dataset", local_dir="/dev/shm/reacao-in")
    return path


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--culto", required=True)
    ap.add_argument("--fonte", default="camera-principal")
    ap.add_argument("--provider", default="hsemotion", choices=["hsemotion", "libreface", "pyfeat", "mock"])
    ap.add_argument("--fps", type=float, default=1.0)
    ap.add_argument("--min-faces-plateia", type=int, default=5, help="rostos no pré-filtro (640 px) para considerar a cena como plateia")
    ap.add_argument("--flavor", default=os.environ.get("HF_JOB_FLAVOR", "t4-small"))
    ap.add_argument("--no-transcribe", action="store_true")
    ap.add_argument("--out", default="out")
    ap.add_argument("--stdout", action="store_true", help="imprime janelas, eventos e insights em JSON no stdout (logs do HF Jobs sem Supabase)")
    args = ap.parse_args(argv)

    from reacao.guard import no_persistence
    from reacao.cost import Timer
    from reacao import ingest, detect
    from reacao.providers import get_provider
    from reacao.aggregate import aggregate
    from reacao.moments import segment, moment_at
    from reacao.events import detect_events
    from reacao.insights import write
    from reacao.store import Store
    from reacao.types import Segment

    timer = Timer(args.flavor)
    store = Store(args.out)
    with no_persistence([os.getcwd(), "/tmp"]):
        video = resolve_video(args.video)
        dur = ingest.duration_s(video)
        provider = get_provider(args.provider)
        timer.mark("carga")

        observations, frame_times, audience_times = [], [], set()
        for t, frame in ingest.frames(video, args.fps):
            frame_times.append(t)
            if args.provider == "mock":
                faces = [detect.FaceObservation(t, 10 * i, 10, 40, 70 if i % 3 else 30, 0.9) for i in range(24)]
            else:
                small = detect.detect(ingest.downscale(frame, 640), t, det_size=(640, 640))
                if len(small) < args.min_faces_plateia:
                    continue
                faces = detect.detect(frame, t)
            audience_times.add(t)
            observations.extend(provider.analyze(frame, faces))
        timer.mark("video")

        aggs = aggregate(args.culto, args.fonte, observations, frame_times, audience_times)
        del observations   # observações por rosto não sobrevivem à agregação
        store.save_windows(aggs)

        segments: list[Segment] = []
        if not args.no_transcribe and args.provider != "mock":
            from reacao.transcribe import transcribe
            segments = transcribe(video)
            store.save_segments(args.culto, segments)
        timer.mark("transcricao")

        moments = segment(segments, aggs, dur)
        store.save_moments(args.culto, moments)
        events = detect_events(aggs, moments)
        for e in events:
            e.momento = moment_at(moments, e.t_ini)
        store.save_events(args.culto, events)
        rejeitados: list[str] = []
        insights = write(events, segments, rejeitados=rejeitados)
        store.save_insights(args.culto, insights)
        timer.mark("analise")

        cobertura = round(100 * sum(1 for a in aggs if not a.insuficiente) / max(1, len(aggs)), 1)
        run = {"culto": args.culto, "provider": args.provider, "duracao_video_s": round(dur), "janelas": len(aggs),
               "cobertura_pct": cobertura, "eventos": len(events), "insights": len(insights),
               "insights_rejeitados_pelo_lint": len(rejeitados), **timer.summary(dur)}
        store.save_run(run)
        print(run)
        if args.stdout:
            for a in aggs:
                print("[janela] " + json.dumps(a.to_row(), ensure_ascii=False))
            for e in events:
                print("[evento] " + json.dumps({"culto": args.culto, **asdict(e)}, ensure_ascii=False))
            for i in insights:
                print("[insight] " + json.dumps({"culto": args.culto, **asdict(i)}, ensure_ascii=False))
        if os.path.exists("/dev/shm/reacao-in"):
            import shutil
            shutil.rmtree("/dev/shm/reacao-in", ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
