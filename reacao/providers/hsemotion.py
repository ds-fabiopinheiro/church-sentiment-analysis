"""HSEmotion (ONNX): 8 expressões por recorte. Leve, roda em lote na T4. Pose via 6DRepNet (reacao.pose)."""
from __future__ import annotations
from .base import Provider
from ..detect import crop


class HSEmotionProvider(Provider):
    name = "hsemotion"

    def __init__(self, model_name: str = "enet_b0_8_best_afew", with_pose: bool = True):
        from hsemotion_onnx.facial_emotions import HSEmotionRecognizer
        self.rec = HSEmotionRecognizer(model_name=model_name)   # API: predict_multi_emotions(list[np.ndarray])
        self.pose = None
        if with_pose:
            from ..pose import HeadPose
            self.pose = HeadPose()

    def analyze(self, frame_bgr, faces):
        idx = [i for i, f in enumerate(faces) if f.measurable]
        if not idx:
            return faces
        crops = [crop(frame_bgr, faces[i])[:, :, ::-1] for i in idx]      # BGR -> RGB
        _, scores = self.rec.predict_multi_emotions(crops, logits=False)   # scores: (n, 8)
        labels = list(self.rec.idx_to_class.values()) if hasattr(self.rec, "idx_to_class") else \
            ["Anger", "Contempt", "Disgust", "Fear", "Happiness", "Neutral", "Sadness", "Surprise"]
        i_happy, i_neutral = labels.index("Happiness"), labels.index("Neutral")
        poses = self.pose.predict_batch(crops) if self.pose else [(None, None)] * len(crops)
        for k, i in enumerate(idx):
            f = faces[i]
            f.p_smile = float(scores[k][i_happy])
            f.expressiveness = float(1.0 - scores[k][i_neutral])
            f.pitch, f.yaw = poses[k]
        return faces
