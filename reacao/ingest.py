"""Leitura do vídeo a N quadros por segundo, em memória, com redução para o pré-filtro de plateia."""
from __future__ import annotations
from typing import Iterator, Tuple
import cv2
import numpy as np


def frames(path: str, fps: float = 1.0) -> Iterator[Tuple[float, np.ndarray]]:
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise RuntimeError(f"não abriu o vídeo: {path}")
    src_fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    step = max(1, int(round(src_fps / fps)))
    idx = 0
    while True:
        if not cap.grab():
            break
        if idx % step == 0:
            ok, frame = cap.retrieve()
            if ok:
                yield idx / src_fps, frame
        idx += 1
    cap.release()


def duration_s(path: str) -> float:
    cap = cv2.VideoCapture(path)
    n = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    f = cap.get(cv2.CAP_PROP_FPS) or 25.0
    cap.release()
    return float(n / f) if f else 0.0


def ultimo_tempo_amostrado(path: str, fps: float = 1.0) -> float | None:
    """Último `t` que `frames()` produz. Rótulo marcado depois disso não casa com quadro nenhum."""
    cap = cv2.VideoCapture(path)
    n, src_fps = cap.get(cv2.CAP_PROP_FRAME_COUNT), cap.get(cv2.CAP_PROP_FPS) or 25.0
    cap.release()
    if n < 1 or src_fps <= 0:
        return None
    step = max(1, int(round(src_fps / fps)))
    return (((int(n) - 1) // step) * step) / src_fps


def downscale(frame: np.ndarray, width: int = 640) -> np.ndarray:
    h, w = frame.shape[:2]
    if w <= width:
        return frame
    return cv2.resize(frame, (width, int(h * width / w)), interpolation=cv2.INTER_AREA)
