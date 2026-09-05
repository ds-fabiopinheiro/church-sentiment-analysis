"""Py-Feat: AUs + emoções + pose por rosto. API da versão 0.6.x; confirmar na versão instalada (PBI-000D)."""
from __future__ import annotations
import numpy as np
from .base import Provider
from ..types import FaceObservation


class PyFeatProvider(Provider):
    name = "pyfeat"

    def __init__(self):
        from feat import Detector
        self.det = Detector(face_model="retinaface", landmark_model="mobilefacenet",
                            au_model="xgb", emotion_model="resmasknet", device="cuda")

    def analyze(self, frame_bgr, faces: list[FaceObservation]):
        meas = [f for f in faces if f.measurable]
        if not meas:
            return faces
        rgb = frame_bgr[:, :, ::-1]
        boxes = [[[f.x, f.y, f.x + f.w, f.y + f.h, f.conf] for f in meas]]
        lm = self.det.detect_landmarks(rgb, boxes)
        emo = self.det.detect_emotions(rgb, boxes, lm)          # colunas: anger..neutral
        pose = self.det.detect_facepose(rgb, lm)               # pitch, roll, yaw
        for i, f in enumerate(meas):
            row = np.asarray(emo[0][i]) if isinstance(emo, (list, tuple)) else np.asarray(emo)[i]
            # ordem Py-Feat: anger, disgust, fear, happiness, sadness, surprise, neutral
            f.p_smile = float(row[3])
            f.expressiveness = float(1.0 - row[6])
            pr = np.asarray(pose[0][i]) if isinstance(pose, (list, tuple)) else np.asarray(pose)[i]
            f.pitch, f.yaw = float(pr[0]), float(pr[2])
        return faces
