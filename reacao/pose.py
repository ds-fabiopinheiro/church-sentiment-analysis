"""Pose da cabeça (6DRepNet) → atenção aparente. Não usa landmarks identificadores; só ângulos."""
from __future__ import annotations
import numpy as np


class HeadPose:
    def __init__(self):
        from sixdrepnet import SixDRepNet
        self.model = SixDRepNet()   # baixa pesos na primeira execução (cache do HF)

    def predict_batch(self, crops_rgb: list[np.ndarray]) -> list[tuple[float, float]]:
        out = []
        for c in crops_rgb:
            pitch, yaw, roll = self.model.predict(c)
            out.append((float(pitch), float(yaw)))
        return out
