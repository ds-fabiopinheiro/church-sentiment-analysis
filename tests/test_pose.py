import numpy as np

from reacao.pose import HeadPose


class _ModeloFalso:
    """Imita SixDRepNet.predict: devolve pitch, yaw, roll como arrays de forma (1,)."""
    def predict(self, img):
        return np.array([10.5]), np.array([-20.0]), np.array([3.0])


def test_predict_batch_aceita_arrays_de_um_elemento():
    pose = HeadPose.__new__(HeadPose)   # sem __init__: não carrega torch nem baixa pesos
    pose.model = _ModeloFalso()
    crops = [np.zeros((64, 64, 3), np.uint8)] * 2
    assert pose.predict_batch(crops) == [(10.5, -20.0), (10.5, -20.0)]
