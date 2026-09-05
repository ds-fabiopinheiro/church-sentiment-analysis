import os
import numpy as np
import pytest
from reacao.guard import no_persistence, PersistenceViolation


def test_blocks_imwrite_outside_shm(tmp_path):
    cv2 = pytest.importorskip("cv2")
    with no_persistence([str(tmp_path)]):
        with pytest.raises(PersistenceViolation):
            cv2.imwrite(str(tmp_path / "quadro.png"), np.zeros((8, 8, 3), dtype=np.uint8))


def test_detects_new_image_file(tmp_path):
    with pytest.raises(PersistenceViolation):
        with no_persistence([str(tmp_path)]):
            (tmp_path / "recorte.jpg").write_bytes(b"x")


def test_shm_is_allowed_and_cleaned():
    cv2 = pytest.importorskip("cv2")
    if not os.path.isdir("/dev/shm"):
        pytest.skip("sem /dev/shm")
    with no_persistence(["/nonexistent"]) as shm_dir:
        p = os.path.join(shm_dir, "tmp.png")
        cv2.imwrite(p, np.zeros((8, 8, 3), dtype=np.uint8))
        os.remove(p)
