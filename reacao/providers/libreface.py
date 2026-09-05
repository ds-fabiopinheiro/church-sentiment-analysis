"""LibreFace: AUs (intensidade) e expressão. Aceita caminho de arquivo: recorte vai para /dev/shm e é apagado.
Verificar a assinatura da API na versão instalada (PBI-000D)."""
from __future__ import annotations
import os
import uuid
import cv2
from .base import Provider
from ..types import FaceObservation
from ..detect import crop
from ..guard import SHM


class LibreFaceProvider(Provider):
    name = "libreface"

    def __init__(self):
        import libreface  # noqa: F401
        self.libreface = libreface
        self.dir = os.path.join(SHM, "reacao")
        os.makedirs(self.dir, exist_ok=True)

    def analyze(self, frame_bgr, faces: list[FaceObservation]):
        for f in faces:
            if not f.measurable:
                continue
            p = os.path.join(self.dir, f"{uuid.uuid4().hex}.png")
            try:
                cv2.imwrite(p, crop(frame_bgr, f))            # permitido: /dev/shm é memória
                r = self.libreface.get_facial_attributes_image(p)   # TODO: confirmar nome/retorno na versão instalada
                aus = r.get("detected_aus", {}) if isinstance(r, dict) else {}
                f.p_smile = float(aus.get("au_12", 0.0))         # AU12 = puxador do canto da boca (sorriso)
                f.expressiveness = float(min(1.0, sum(aus.values()) / max(1, len(aus)))) if aus else None
                pose = r.get("head_pose", {}) if isinstance(r, dict) else {}
                f.yaw, f.pitch = pose.get("yaw"), pose.get("pitch")
            finally:
                if os.path.exists(p):
                    os.remove(p)
        return faces
