"""Detector de rostos compartilhado. Só detecção: nenhum módulo de reconhecimento é carregado."""
from __future__ import annotations
import numpy as np
from .types import FaceObservation, DETECTION_FLOOR_PX

_APP = None


def load(det_size=(1280, 1280)):
    global _APP
    if _APP is None:
        from insightface.app import FaceAnalysis
        # allowed_modules=["detection"] impede carregar o modelo de reconhecimento (regra 2 do CLAUDE.md)
        app = FaceAnalysis(name="buffalo_sc", allowed_modules=["detection"],
                           providers=["CUDAExecutionProvider", "CPUExecutionProvider"])
        app.prepare(ctx_id=0, det_size=det_size, det_thresh=0.5)
        loaded = set(app.models.keys())
        assert "recognition" not in loaded, f"módulo de reconhecimento carregado: {loaded}"
        _APP = app
    return _APP


def detect(frame_bgr: np.ndarray, t: float, det_size=(1280, 1280)) -> list[FaceObservation]:
    """Detecta rostos em resolução plena. Para 4K com rostos pequenos, detecção por ladrilhos: TODO (PBI-000D)."""
    app = load(det_size)
    out: list[FaceObservation] = []
    for f in app.get(frame_bgr):
        x1, y1, x2, y2 = [int(v) for v in f.bbox]
        h, w = max(0, y2 - y1), max(0, x2 - x1)
        if h < DETECTION_FLOOR_PX:
            continue
        out.append(FaceObservation(t=t, x=x1, y=y1, w=w, h=h, conf=float(f.det_score)))
    return out


def crop(frame_bgr: np.ndarray, obs: FaceObservation, margin: float = 0.15) -> np.ndarray:
    H, W = frame_bgr.shape[:2]
    mx, my = int(obs.w * margin), int(obs.h * margin)
    x1, y1 = max(0, obs.x - mx), max(0, obs.y - my)
    x2, y2 = min(W, obs.x + obs.w + mx), min(H, obs.y + obs.h + my)
    return frame_bgr[y1:y2, x1:x2]
