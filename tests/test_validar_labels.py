"""O validador existe para que horas de marcação manual não se percam por erro de formato."""
from __future__ import annotations
import importlib.util
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("validar_labels", os.path.join(RAIZ, "tools", "validar_labels.py"))
validar_labels = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validar_labels)

FACES_OK = "t_s,altura_px\n" + "".join(f"{t},{80 + t}\n" for t in range(12))
# o critério 2 é medido sobre o corpus: pelo menos um riso e quatro trechos neutros no total
EVENTOS_OK = ("t_ini_s,t_fim_s,tipo\n10,14,riso\n20,24,neutro\n30,34,neutro\n"
              "40,44,neutro\n50,54,neutro\n")


def _escrever(pasta, base="clipe01", faces=FACES_OK, eventos=EVENTOS_OK):
    pasta.mkdir(exist_ok=True)
    if faces is not None:
        (pasta / f"{base}_faces.csv").write_text(faces, encoding="utf-8")
    if eventos is not None:
        (pasta / f"{base}_eventos.csv").write_text(eventos, encoding="utf-8")
    return str(pasta)


def _rodar(pasta, capsys):
    codigo = validar_labels.main(["--labels", str(pasta)])
    return codigo, capsys.readouterr().out


def test_rotulos_validos_passam(tmp_path, capsys):
    codigo, saida = _rodar(_escrever(tmp_path / "labels"), capsys)
    assert codigo == 0 and "0 erro(s)" in saida


def test_tempo_fora_da_grade_de_amostragem_e_erro(tmp_path, capsys):
    faces = "t_s,altura_px\n0,80\n1,90\n2.5,70\n3,88\n4,95\n5,70\n"
    codigo, saida = _rodar(_escrever(tmp_path / "labels", faces=faces), capsys)
    assert codigo == 1 and "fora dos segundos inteiros" in saida


def test_nenhum_rosto_mensuravel_e_erro(tmp_path, capsys):
    faces = "t_s,altura_px\n" + "".join(f"{t},40\n" for t in range(6))
    codigo, saida = _rodar(_escrever(tmp_path / "labels", faces=faces), capsys)
    assert codigo == 1 and "recall do critério 1 fica indefinido" in saida


def test_coluna_ausente_e_altura_invalida(tmp_path, capsys):
    codigo, saida = _rodar(_escrever(tmp_path / "labels", faces="tempo,altura\n0,80\n"), capsys)
    assert codigo == 1 and "colunas ausentes" in saida
    codigo, saida = _rodar(_escrever(tmp_path / "l2", faces="t_s,altura_px\n0,80\n1,-3\n"), capsys)
    assert codigo == 1 and "altura_px deve ser positiva" in saida


def test_tipo_de_evento_desconhecido_e_intervalo_invertido(tmp_path, capsys):
    eventos = "t_ini_s,t_fim_s,tipo\n10,14,gargalhada\n40,30,neutro\n"
    codigo, saida = _rodar(_escrever(tmp_path / "labels", eventos=eventos), capsys)
    assert codigo == 1 and "fora de" in saida and "deve ser maior que" in saida


def test_faces_ausente_e_erro(tmp_path, capsys):
    codigo, saida = _rodar(_escrever(tmp_path / "labels", faces=None), capsys)
    assert codigo == 1 and "sem ele o bench ignora este vídeo" in saida


def test_corpus_sem_riso_ou_com_poucos_neutros_e_erro(tmp_path, capsys):
    """Os mínimos do critério 2 valem sobre o corpus inteiro, não por vídeo: com clipes de 8 a 23 s
    nenhum vídeo sozinho comporta quatro trechos neutros."""
    so_neutros = "t_ini_s,t_fim_s,tipo\n20,24,neutro\n30,34,neutro\n40,44,neutro\n50,54,neutro\n"
    codigo, saida = _rodar(_escrever(tmp_path / "labels", eventos=so_neutros), capsys)
    assert codigo == 1 and "nenhum evento de riso em todo o corpus" in saida
    poucos = "t_ini_s,t_fim_s,tipo\n10,14,riso\n20,24,neutro\n30,34,neutro\n"
    codigo, saida = _rodar(_escrever(tmp_path / "l2", eventos=poucos), capsys)
    assert codigo == 1 and "o jitter precisa de pelo menos 4" in saida


def test_video_sem_trecho_neutro_usa_a_base_do_corpus(tmp_path, capsys):
    labels = tmp_path / "labels"
    _escrever(labels, base="clipe01", eventos="t_ini_s,t_fim_s,tipo\n2,6,riso\n")
    _escrever(labels, base="clipe02", eventos="t_ini_s,t_fim_s,tipo\n1,3,neutro\n4,6,neutro\n7,9,neutro\n10,12,neutro\n")
    codigo, saida = _rodar(labels, capsys)
    assert codigo == 0 and "vai usar a base neutra do corpus" in saida


def test_nome_de_arquivo_sem_video_correspondente(tmp_path, capsys):
    labels = _escrever(tmp_path / "labels", base="clipe_com_typo")
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "clipe01.mp4").write_bytes(b"")
    codigo = validar_labels.main(["--labels", labels, "--corpus", str(corpus)])
    saida = capsys.readouterr().out
    assert codigo == 1 and "não há vídeo com esse nome" in saida and "sem nenhum rótulo" in saida
