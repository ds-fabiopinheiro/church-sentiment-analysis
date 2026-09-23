"""Prepara a rotulagem manual: cria os CSVs vazios com o nome certo e lista os tempos que existem em cada vídeo.

O bench casa rótulo e vídeo pelo nome do arquivo e só mede nos quadros que o pipeline amostra. Os dois erros que
mais custam horas de marcação são o nome errado, que faz o vídeo ser ignorado sem aviso, e o tempo fora da grade
de amostragem, que entra no denominador do recall e nunca pode ser detectado. Este script elimina os dois.

Uso:
    uv run python tools/preparar_rotulagem.py --corpus samples/pib --labels labels/
    uv run python tools/preparar_rotulagem.py --corpus samples/pib --labels labels/ --excluir igreja_simples_07
"""
from __future__ import annotations
import argparse
import os
from glob import glob

CABECALHO_FACES = "t_s,altura_px\n"
CABECALHO_EVENTOS = "t_ini_s,t_fim_s,tipo\n"


def grade(caminho: str, fps: float = 1.0) -> list[int]:
    """Tempos inteiros que `reacao.ingest.frames` produz para este vídeo."""
    from reacao.ingest import ultimo_tempo_amostrado
    ultimo = ultimo_tempo_amostrado(caminho, fps)
    return [] if ultimo is None else list(range(int(round(ultimo)) + 1))


def criar(caminho: str, conteudo: str) -> str:
    if os.path.exists(caminho):
        return "já existia"
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(conteudo)
    return "criado"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else "preparar rotulagem")
    ap.add_argument("--corpus", required=True, help="pasta com os .mp4")
    ap.add_argument("--labels", required=True, help="pasta onde os CSVs serão criados")
    ap.add_argument("--excluir", default="", help="nomes de vídeo a pular, separados por vírgula")
    args = ap.parse_args(argv)
    excluidos = {n.strip() for n in args.excluir.split(",") if n.strip()}
    os.makedirs(args.labels, exist_ok=True)
    videos = sorted(glob(os.path.join(args.corpus, "*.mp4")))
    if not videos:
        print(f"nenhum .mp4 em {args.corpus}")
        return 1
    total_quadros = 0
    for video in videos:
        nome = os.path.splitext(os.path.basename(video))[0]
        if nome in excluidos:
            print(f"{nome}: pulado por --excluir")
            continue
        tempos = grade(video)
        if not tempos:
            print(f"{nome}: não foi possível ler a grade de quadros; o vídeo abre?")
            continue
        total_quadros += len(tempos)
        f = criar(os.path.join(args.labels, f"{nome}_faces.csv"), CABECALHO_FACES)
        e = criar(os.path.join(args.labels, f"{nome}_eventos.csv"), CABECALHO_EVENTOS)
        print(f"{nome}: {len(tempos)} quadro(s), t_s de {tempos[0]} a {tempos[-1]} | faces.csv {f} | eventos.csv {e}")
    print(f"\n{total_quadros} quadro(s) a rotular no total.")
    print("Em _faces.csv, uma linha por ROSTO: t_s da lista acima e a altura em pixels.")
    print("Em _eventos.csv, um intervalo por linha: riso, aplauso, pe, cabeca_baixa ou neutro.")
    print("O corpus inteiro precisa de pelo menos 1 riso e 4 trechos neutros.")
    print(f"\nDepois: uv run python tools/validar_labels.py --labels {args.labels} --corpus {args.corpus}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
