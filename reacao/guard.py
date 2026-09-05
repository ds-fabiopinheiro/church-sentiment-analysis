"""Guarda de não-persistência: bloqueia gravação de imagens fora de /dev/shm e verifica o disco ao fim."""
from __future__ import annotations
import os
import time
from contextlib import contextmanager

SHM = "/dev/shm"
IMAGE_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff", ".mp4", ".mkv", ".avi", ".mov", ".npy", ".npz"}


class PersistenceViolation(RuntimeError):
    pass


def _allowed(path: str) -> bool:
    return os.path.abspath(path).startswith(SHM)


def _patch_writers():
    try:
        import cv2
        _orig = cv2.imwrite

        def guarded_imwrite(path, *a, **k):
            if not _allowed(str(path)):
                raise PersistenceViolation(f"cv2.imwrite fora de {SHM}: {path}")
            return _orig(path, *a, **k)
        cv2.imwrite = guarded_imwrite
    except ImportError:
        pass
    try:
        from PIL import Image
        _orig_save = Image.Image.save

        def guarded_save(self, fp, *a, **k):
            if isinstance(fp, (str, os.PathLike)) and not _allowed(str(fp)):
                raise PersistenceViolation(f"PIL save fora de {SHM}: {fp}")
            return _orig_save(self, fp, *a, **k)
        Image.Image.save = guarded_save
    except ImportError:
        pass


def _snapshot(roots: list[str]) -> set[str]:
    seen = set()
    for root in roots:
        for dp, _, fns in os.walk(root):
            if dp.startswith(SHM):
                continue
            for fn in fns:
                if os.path.splitext(fn)[1].lower() in IMAGE_EXT:
                    seen.add(os.path.join(dp, fn))
    return seen


@contextmanager
def no_persistence(watch_roots: list[str] | None = None):
    """`with no_persistence([os.getcwd(), "/tmp"]): ...` — levanta PersistenceViolation se um arquivo de
    imagem/vídeo novo aparecer fora de /dev/shm ou se /dev/shm ficar com resíduos ao fim."""
    roots = watch_roots or [os.getcwd(), "/tmp"]
    before = _snapshot(roots)
    shm_dir = os.path.join(SHM, "reacao")
    os.makedirs(shm_dir, exist_ok=True)
    _patch_writers()
    t0 = time.time()
    try:
        yield shm_dir
    finally:
        after = _snapshot(roots)
        novos = sorted(after - before)
        residuos = [os.path.join(dp, f) for dp, _, fs in os.walk(shm_dir) for f in fs]
        for p in residuos:
            try:
                os.remove(p)
            except OSError:
                pass
        if novos:
            raise PersistenceViolation(f"arquivos de imagem/vídeo criados fora de {SHM}: {novos[:5]}")
        if residuos:
            raise PersistenceViolation(f"resíduos em {shm_dir} ao fim (apagados agora): {residuos[:5]}")
        print(f"[guard] ok: nenhum quadro persistido; duração {time.time() - t0:.0f}s")
