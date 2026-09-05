"""Interface única de motor de expressão. Trocar de motor não altera agregação, eventos ou relatório."""
from __future__ import annotations
from abc import ABC, abstractmethod
import numpy as np
from ..types import FaceObservation


class Provider(ABC):
    name: str = "base"
    video_leaves_edge: bool = False     # True só para APIs em nuvem (nenhuma no escopo)

    @abstractmethod
    def analyze(self, frame_bgr: np.ndarray, faces: list[FaceObservation]) -> list[FaceObservation]:
        """Preenche p_smile, expressiveness, (yaw, pitch, eyes_closed quando o motor der) nos rostos mensuráveis.
        Nunca retorna vetor de identidade facial, id ou recorte. Rostos com h < 64 px voltam sem medição."""


def get_provider(name: str) -> Provider:
    if name == "hsemotion":
        from .hsemotion import HSEmotionProvider
        return HSEmotionProvider()
    if name == "libreface":
        from .libreface import LibreFaceProvider
        return LibreFaceProvider()
    if name == "pyfeat":
        from .pyfeat import PyFeatProvider
        return PyFeatProvider()
    if name == "mock":
        from .mock import MockProvider
        return MockProvider()
    raise ValueError(f"motor desconhecido: {name}")
