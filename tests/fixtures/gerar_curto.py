"""Gera um mp4 sintético curto, sem rosto, para exercitar ingestão, guarda de não-persistência, agregação e
gravação com o motor `mock` (que fabrica as observações). Não serve para medir detecção.

Uso: uv run python tests/fixtures/gerar_curto.py [destino] [--segundos 10] [--fps 15]
O arquivo gerado é ignorado pelo git (*.mp4); o CI o cria a cada execução.
"""
from __future__ import annotations
import argparse
import os
import cv2
import numpy as np

CODECS = ("mp4v", "MJPG")   # mp4v vem nas wheels do opencv-python-headless; MJPG é a reserva


def _legivel(caminho: str, quadros_esperados: int) -> bool:
    """Confere relendo: um VideoWriter aberto não garante arquivo legível."""
    cap = cv2.VideoCapture(caminho)
    ok = cap.isOpened() and cap.get(cv2.CAP_PROP_FRAME_COUNT) >= quadros_esperados
    cap.release()
    return bool(ok)


def gerar(destino: str, segundos: float = 10.0, fps: float = 15.0, largura: int = 320, altura: int = 240) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)
    n = int(round(segundos * fps))
    for codec in CODECS:
        w = cv2.VideoWriter(destino, cv2.VideoWriter_fourcc(*codec), fps, (largura, altura))
        if not w.isOpened():
            w.release()
            continue
        for i in range(n):
            quadro = np.full((altura, largura, 3), (i % 256, 96, 48), dtype=np.uint8)
            cv2.putText(quadro, str(i), (16, altura // 2), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
            w.write(quadro)
        w.release()
        if os.path.exists(destino) and _legivel(destino, n):
            return destino
    raise RuntimeError(f"nenhum codec disponível para gravar {destino}: {CODECS}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Gera um mp4 sintético curto, sem rosto, para o CI e os testes.")
    ap.add_argument("destino", nargs="?", default=os.path.join(os.path.dirname(__file__), "curto.mp4"))
    ap.add_argument("--segundos", type=float, default=10.0)
    ap.add_argument("--fps", type=float, default=15.0)
    args = ap.parse_args(argv)
    p = gerar(args.destino, args.segundos, args.fps)
    print(f"fixture gerada: {p} ({os.path.getsize(p)} bytes, {args.segundos:g} s a {args.fps:g} fps)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
