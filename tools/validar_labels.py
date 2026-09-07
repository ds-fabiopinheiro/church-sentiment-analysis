"""Confere os rótulos manuais antes do bench, para que horas de marcação não sejam perdidas por erro de formato.

Uso:
    uv run python tools/validar_labels.py --labels labels/
    uv run python tools/validar_labels.py --labels labels/ --corpus samples/pib

Sem dependências além da biblioteca padrão; a duração do vídeo só é conferida se o OpenCV estiver disponível.
Erro (sai com código 1) é o que faz o bench medir errado ou ignorar o arquivo. Aviso é o que merece um olhar.
Formatos em `labels/README.md`.
"""
from __future__ import annotations
import argparse
import csv
import glob
import os

TIPOS_EVENTO = {"riso", "aplauso", "pe", "cabeca_baixa", "neutro"}
MOMENTOS = {"louvor", "oracao", "avisos", "palavra", "apelo", "ceia", "encerramento"}
ALTURA_MENSURAVEL_PX = 64
TOLERANCIA_GRADE_S = 0.05      # o pipeline amostra em segundos inteiros; t_s fora disso não casa com quadro nenhum


class Relatorio:
    def __init__(self) -> None:
        self.erros: list[str] = []
        self.avisos: list[str] = []

    def erro(self, arquivo: str, msg: str) -> None:
        self.erros.append(f"{arquivo}: {msg}")

    def aviso(self, arquivo: str, msg: str) -> None:
        self.avisos.append(f"{arquivo}: {msg}")


def _ler(caminho: str, colunas: list[str], rel: Relatorio) -> list[dict[str, str]] | None:
    nome = os.path.basename(caminho)
    with open(caminho, newline="", encoding="utf-8-sig") as fh:
        linhas = list(csv.DictReader(fh))
    if not linhas:
        rel.erro(nome, "arquivo sem linhas de dados")
        return None
    faltando = [c for c in colunas if c not in (linhas[0].keys())]
    if faltando:
        rel.erro(nome, f"colunas ausentes: {', '.join(faltando)} (esperado: {', '.join(colunas)})")
        return None
    return linhas


def _numero(valor: str | None, arquivo: str, linha: int, coluna: str, rel: Relatorio) -> float | None:
    try:
        return float(str(valor).strip())
    except (TypeError, ValueError):
        rel.erro(arquivo, f"linha {linha}: '{coluna}' não é número: {valor!r}")
        return None


def validar_faces(caminho: str, duracao_s: float | None, rel: Relatorio) -> None:
    nome = os.path.basename(caminho)
    linhas = _ler(caminho, ["t_s", "altura_px"], rel)
    if linhas is None:
        return
    tempos: set[float] = set()
    fora_da_grade: set[float] = set()
    mensuraveis = 0
    for i, linha in enumerate(linhas, start=2):
        t = _numero(linha.get("t_s"), nome, i, "t_s", rel)
        h = _numero(linha.get("altura_px"), nome, i, "altura_px", rel)
        if t is None or h is None:
            continue
        if t < 0:
            rel.erro(nome, f"linha {i}: t_s negativo ({t})")
            continue
        if h <= 0:
            rel.erro(nome, f"linha {i}: altura_px deve ser positiva ({h})")
            continue
        if duracao_s is not None and t > duracao_s + 1:
            rel.erro(nome, f"linha {i}: t_s {t:.1f}s além da duração do vídeo ({duracao_s:.1f}s)")
            continue
        tempos.add(t)
        if abs(t - round(t)) > TOLERANCIA_GRADE_S:
            fora_da_grade.add(t)
        if h >= ALTURA_MENSURAVEL_PX:
            mensuraveis += 1
    if fora_da_grade:
        exemplos = ", ".join(f"{t:.2f}" for t in sorted(fora_da_grade)[:5])
        rel.erro(nome, f"{len(fora_da_grade)} tempo(s) fora dos segundos inteiros ({exemplos}); "
                       "o pipeline amostra 1 quadro por segundo e esses rostos não entram no recall")
    if mensuraveis == 0:
        rel.erro(nome, f"nenhum rosto com altura ≥ {ALTURA_MENSURAVEL_PX} px: o recall do critério 1 fica indefinido")
    if len(tempos) < 5:
        rel.aviso(nome, f"só {len(tempos)} quadro(s) distinto(s); o README pede cerca de 20")
    print(f"  {nome}: {len(linhas)} rosto(s) em {len(tempos)} quadro(s), {mensuraveis} com altura ≥ {ALTURA_MENSURAVEL_PX} px")


def validar_eventos(caminho: str, duracao_s: float | None, rel: Relatorio) -> None:
    nome = os.path.basename(caminho)
    linhas = _ler(caminho, ["t_ini_s", "t_fim_s", "tipo"], rel)
    if linhas is None:
        return
    intervalos: list[tuple[float, float, str]] = []
    for i, linha in enumerate(linhas, start=2):
        t0 = _numero(linha.get("t_ini_s"), nome, i, "t_ini_s", rel)
        t1 = _numero(linha.get("t_fim_s"), nome, i, "t_fim_s", rel)
        tipo = (linha.get("tipo") or "").strip().lower()
        if t0 is None or t1 is None:
            continue
        if tipo not in TIPOS_EVENTO:
            rel.erro(nome, f"linha {i}: tipo '{tipo}' fora de {sorted(TIPOS_EVENTO)}")
            continue
        if t1 <= t0:
            rel.erro(nome, f"linha {i}: t_fim_s ({t1}) deve ser maior que t_ini_s ({t0})")
            continue
        if t0 < 0:
            rel.erro(nome, f"linha {i}: t_ini_s negativo ({t0})")
            continue
        if duracao_s is not None and t0 > duracao_s + 1:
            rel.erro(nome, f"linha {i}: intervalo começa em {t0:.1f}s, além da duração do vídeo ({duracao_s:.1f}s)")
            continue
        intervalos.append((t0, t1, tipo))
    for a in range(len(intervalos)):
        for b in range(a + 1, len(intervalos)):
            (i0, i1, ta), (j0, j1, tb) = intervalos[a], intervalos[b]
            if i1 > j0 and j1 > i0:
                rel.aviso(nome, f"intervalos sobrepostos: {ta} [{i0:.0f}–{i1:.0f}] e {tb} [{j0:.0f}–{j1:.0f}]")
    contagem = {t: sum(1 for _, _, x in intervalos if x == t) for t in sorted(TIPOS_EVENTO)}
    if not contagem["riso"]:
        rel.aviso(nome, "nenhum evento de riso: o critério 2 do gate não pode ser calculado neste vídeo")
    if not contagem["neutro"]:
        rel.aviso(nome, "nenhum trecho neutro: sem base de comparação, sensibilidade e jitter ficam indefinidos")
    elif contagem["neutro"] < 2:
        rel.aviso(nome, "só um trecho neutro; o jitter precisa de pelo menos dois")
    print(f"  {nome}: {len(intervalos)} intervalo(s) " + ", ".join(f"{t}={n}" for t, n in contagem.items() if n))


def validar_momentos(caminho: str, duracao_s: float | None, rel: Relatorio) -> None:
    nome = os.path.basename(caminho)
    linhas = _ler(caminho, ["t_ini_s", "t_fim_s", "nome"], rel)
    if linhas is None:
        return
    n = 0
    for i, linha in enumerate(linhas, start=2):
        t0 = _numero(linha.get("t_ini_s"), nome, i, "t_ini_s", rel)
        t1 = _numero(linha.get("t_fim_s"), nome, i, "t_fim_s", rel)
        momento = (linha.get("nome") or "").strip().lower()
        if t0 is None or t1 is None:
            continue
        if momento not in MOMENTOS:
            rel.erro(nome, f"linha {i}: momento '{momento}' fora de {sorted(MOMENTOS)}")
            continue
        if t1 <= t0:
            rel.erro(nome, f"linha {i}: t_fim_s ({t1}) deve ser maior que t_ini_s ({t0})")
            continue
        n += 1
    print(f"  {nome}: {n} momento(s)")


def duracao_do_video(corpus: str | None, base: str) -> float | None:
    if not corpus:
        return None
    caminho = os.path.join(corpus, f"{base}.mp4")
    if not os.path.exists(caminho):
        return None
    try:
        from reacao.ingest import duration_s
    except ImportError:
        return None
    d = duration_s(caminho)
    return d if d > 0 else None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Confere os rótulos manuais do corpus antes do bench.")
    ap.add_argument("--labels", required=True, help="pasta com <video>_faces.csv, <video>_eventos.csv, <video>_momentos.csv")
    ap.add_argument("--corpus", help="pasta dos vídeos, para conferir nomes e durações (opcional)")
    args = ap.parse_args(argv)
    rel = Relatorio()
    if not os.path.isdir(args.labels):
        print(f"pasta de rótulos não encontrada: {args.labels}")
        return 1

    bases = sorted({os.path.basename(p).rsplit("_", 1)[0]
                    for sufixo in ("faces", "eventos", "momentos")
                    for p in glob.glob(os.path.join(args.labels, f"*_{sufixo}.csv"))})
    if not bases:
        print(f"nenhum arquivo <video>_faces.csv, _eventos.csv ou _momentos.csv em {args.labels}")
        return 1

    videos = {os.path.splitext(os.path.basename(p))[0] for p in glob.glob(os.path.join(args.corpus, "*.mp4"))} if args.corpus else set()
    for base in bases:
        print(f"{base}:")
        duracao = duracao_do_video(args.corpus, base)
        if videos and base not in videos:
            rel.erro(f"{base}_*.csv", "não há vídeo com esse nome no corpus; confira o nome do arquivo, "
                                      "porque o bench casa rótulo e vídeo pelo nome")
        faces = os.path.join(args.labels, f"{base}_faces.csv")
        if os.path.exists(faces):
            validar_faces(faces, duracao, rel)
        else:
            rel.erro(f"{base}_faces.csv", "ausente: sem ele o bench ignora este vídeo por completo")
        for sufixo, funcao in (("eventos", validar_eventos), ("momentos", validar_momentos)):
            caminho = os.path.join(args.labels, f"{base}_{sufixo}.csv")
            if os.path.exists(caminho):
                funcao(caminho, duracao, rel)
            elif sufixo == "eventos":
                rel.aviso(f"{base}_eventos.csv", "ausente: critérios 2 (sensibilidade) e jitter ficam sem medida")

    for video in sorted(videos - set(bases)):
        rel.aviso(f"{video}.mp4", "sem nenhum rótulo; o bench vai pular este vídeo")

    print()
    for msg in rel.avisos:
        print(f"[aviso] {msg}")
    for msg in rel.erros:
        print(f"[erro]  {msg}")
    print(f"\n{len(bases)} vídeo(s) rotulado(s), {len(rel.erros)} erro(s), {len(rel.avisos)} aviso(s).")
    return 1 if rel.erros else 0


if __name__ == "__main__":
    raise SystemExit(main())
