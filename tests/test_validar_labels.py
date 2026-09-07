"""O validador existe para que horas de marcação manual não se percam por erro de formato."""
from __future__ import annotations
import importlib.util
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("validar_labels", os.path.join(RAIZ, "tools", "validar_labels.py"))
validar_labels = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validar_labels)

FACES_OK = "t_s,altura_px\n" + "".join(f"{t},{80 + t}\n" for t in range(12))
EVENTOS_OK = "t_ini_s,t_fim_s,tipo\n10,14,riso\n30,40,neutro\n50,60,neutro\n"


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


def test_faces_ausente_e_erro_e_falta_de_riso_e_aviso(tmp_path, capsys):
    codigo, saida = _rodar(_escrever(tmp_path / "labels", faces=None), capsys)
    assert codigo == 1 and "sem ele o bench ignora este vídeo" in saida
    eventos = "t_ini_s,t_fim_s,tipo\n30,40,neutro\n50,60,neutro\n"
    codigo, saida = _rodar(_escrever(tmp_path / "l2", eventos=eventos), capsys)
    assert codigo == 0 and "critério 2 do gate não pode ser calculado" in saida


def test_nome_de_arquivo_sem_video_correspondente(tmp_path, capsys):
    labels = _escrever(tmp_path / "labels", base="clipe_com_typo")
    corpus = tmp_path / "corpus"
    corpus.mkdir()
    (corpus / "clipe01.mp4").write_bytes(b"")
    codigo = validar_labels.main(["--labels", labels, "--corpus", str(corpus)])
    saida = capsys.readouterr().out
    assert codigo == 1 and "não há vídeo com esse nome" in saida and "sem nenhum rótulo" in saida
