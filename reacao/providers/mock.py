"""Motor falso para testes e CI (sem modelos)."""
from __future__ import annotations
import numpy as np
from .base import Provider
from ..types import FaceObservation


class MockProvider(Provider):
    name = "mock"

    def analyze(self, frame_bgr: np.ndarray, faces: list[FaceObservation]) -> list[FaceObservation]:
        rng = np.random.default_rng(int(faces[0].t) if faces else 0)
        for f in faces:
            if f.measurable:
                f.p_smile = float(rng.uniform(0, 1))
                f.expressiveness = float(rng.uniform(0, 1))
                f.yaw = float(rng.normal(0, 20))
                f.pitch = float(rng.normal(0, 10))
        return faces
