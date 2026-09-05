"""Transcrição do púlpito a partir da trilha de áudio do próprio arquivo (faster-whisper). Nenhum som de plateia é classificado."""
from __future__ import annotations
from .types import Segment


def transcribe(video_path: str, model_size: str = "medium", device: str = "auto") -> list[Segment]:
    from faster_whisper import WhisperModel
    compute = "float16" if device in ("auto", "cuda") else "int8"
    try:
        model = WhisperModel(model_size, device="cuda" if device == "auto" else device, compute_type=compute)
    except Exception:
        model = WhisperModel("small", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(video_path, language="pt", vad_filter=True, beam_size=5)
    return [Segment(t_ini=float(s.start), t_fim=float(s.end), texto=s.text.strip()) for s in segs]


def text_between(segments: list[Segment], t0: float, t1: float) -> str:
    return " ".join(s.texto for s in segments if s.t_fim >= t0 and s.t_ini <= t1).strip()
