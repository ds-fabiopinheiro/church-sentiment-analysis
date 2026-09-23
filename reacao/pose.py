"""Pose da cabeça (6DRepNet) → atenção aparente. Não usa landmarks identificadores; só ângulos."""
from __future__ import annotations
import numpy as np


def _escalar(v) -> float:
    """float() em array de forma (1,) é erro no NumPy recente; .item() exige exatamente um elemento."""
    return float(np.asarray(v).item())


class HeadPose:
    def __init__(self):
        import torch
        from sixdrepnet import SixDRepNet
        gpu_id = 0 if torch.cuda.is_available() else -1   # -1 = CPU (sem isso o pacote chama .cuda())
        self.model = SixDRepNet(gpu_id=gpu_id)   # baixa pesos na primeira execução (cache do torch hub)

    def predict_batch(self, crops_bgr: list[np.ndarray]) -> list[tuple[float, float]]:
        """Recortes em BGR (como saem do OpenCV): SixDRepNet.predict converte para RGB internamente."""
        out = []
        for c in crops_bgr:
            pitch, yaw, _ = self.model.predict(c)   # arrays de forma (1,): lote de um recorte
            out.append((_escalar(pitch), _escalar(yaw)))
        return out
