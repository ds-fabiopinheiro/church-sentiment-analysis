"""Tempo e custo do job. Preço por hora do hardware do Hugging Face Jobs (set/2026): t4-small US$ 0,40."""
from __future__ import annotations
import time

PRICE_PER_HOUR = {"t4-small": 0.40, "t4-medium": 0.60, "l4x1": 0.80, "a10g-small": 1.00, "cpu-basic": 0.01, "local": 0.0}


class Timer:
    def __init__(self, flavor: str = "t4-small"):
        self.flavor = flavor
        self.t0 = time.time()
        self.marks: dict[str, float] = {}
        self._last = self.t0

    def mark(self, etapa: str):
        now = time.time()
        self.marks[etapa] = round(now - self._last, 1)
        self._last = now

    def summary(self, video_seconds: float) -> dict:
        total = time.time() - self.t0
        cost = total / 3600 * PRICE_PER_HOUR.get(self.flavor, 0.0)
        return {"flavor": self.flavor, "segundos_total": round(total, 1), "etapas": self.marks,
                "custo_usd": round(cost, 3), "custo_por_hora_de_video_usd": round(cost / max(video_seconds / 3600, 1e-6), 3),
                "tempo_por_hora_de_video_s": round(total / max(video_seconds / 3600, 1e-6), 0)}
