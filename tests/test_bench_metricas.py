"""Aritmética das métricas do gate. Fixada antes de o conjunto de teste rotulado existir, de propósito."""
from __future__ import annotations
import importlib.util
import math
import os
from collections import Counter

import pandas as pd

from reacao.types import FaceObservation

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("bench", os.path.join(RAIZ, "bench.py"))
bench = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bench)


def _obs(t: float, n: int, p_smile: float) -> list[FaceObservation]:
    return [FaceObservation(t=t, x=i, y=0, w=80, h=80, conf=0.9, yaw=0.0, pitch=0.0, p_smile=p_smile,
                            expressiveness=0.5) for i in range(n)]


# --- critério 1: recall -------------------------------------------------------------------------

def test_recall_max_nao_deixa_falso_positivo_compensar_perda():
    det = Counter({0: 5, 1: 15})                       # 20 detecções, mas distribuídas errado
    manual = pd.DataFrame({"t_s": [0] * 10 + [1] * 10, "altura_px": [80] * 20})
    r = bench.medir_recall(det, manual)
    assert r["razao_contagem_ge64"] == 1.0             # a razão de contagens não vê o problema
    assert r["recall_ge64_max"] == 0.75                # o limite pareado por quadro vê
    assert r["discrepancia_rel"] == 0.5


def test_recall_ignora_rostos_abaixo_de_64_px_e_conta_quadro_sem_deteccao():
    manual = pd.DataFrame({"t_s": [0, 0, 1], "altura_px": [80, 40, 90]})
    r = bench.medir_recall(Counter({0: 1}), manual)
    assert r["rostos_marcados_ge64"] == 2 and r["recall_ge64_max"] == 0.5
    assert r["quadros_rotulados_sem_deteccao"] == 1


# --- critério 2: sensibilidade ------------------------------------------------------------------

def test_evento_rotulado_sem_k_conta_como_nao_atingido():
    r = bench.medir_criterio2([(5.0, 60.0), (5.0, None), (5.0, None)], base=12.0, limiar_pp=15.0)
    assert r["frac_eventos_riso_ok"] == 0.33           # denominador do gate: risos ROTULADOS
    assert r["frac_sobre_medidos"] == 1.0              # diagnóstico: dos medidos, todos passaram
    assert r["eventos_riso_rotulados"] == 3 and r["eventos_riso_medidos"] == 1


def test_equivalencia_com_a_janela_de_30_s_da_producao():
    r = bench.medir_criterio2([(5.0, 60.0)], base=12.0, limiar_pp=15.0)
    assert r["eventos_riso_ok"] == 1                   # subida de 48 p.p. no intervalo do riso
    assert r["eventos_riso_ok_equiv30"] == 0           # 48 * 5/30 = 8 p.p. na janela de produção


def test_sem_base_neutra_nao_inventa_aprovacao():
    r = bench.medir_criterio2([(5.0, 60.0)], base=float("nan"), limiar_pp=15.0)
    assert math.isnan(r["frac_eventos_riso_ok"]) and r["eventos_riso_ok"] == 0


def test_jitter_exige_quatro_trechos_distintos():
    assert math.isnan(bench.medir_jitter([18.0, 18.0])["jitter_dp_pp"])       # dois trechos: sem estatística
    r = bench.medir_jitter([10.0, 12.0, 11.0, 13.0])
    assert r["jitter_dp_pp"] == 1.3 and r["trechos_neutros_medidos"] == 4


# --- agregação por intervalo, não por grade -----------------------------------------------------

def test_valor_do_intervalo_usa_os_quadros_do_proprio_intervalo():
    obs = _obs(0.0, 12, 0.1) + _obs(1.0, 12, 0.9) + _obs(2.0, 12, 0.1)
    ft = [0.0, 1.0, 2.0]
    assert bench.valor_do_intervalo("v", obs, ft, set(ft), 1.0, 1.0) == 100.0   # só o quadro do riso
    assert bench.valor_do_intervalo("v", obs, ft, set(ft), 0.0, 2.0) == 33.3    # os três quadros


def test_intervalo_sem_k_minimo_sai_none():
    obs = _obs(0.0, 9, 0.9)
    assert bench.valor_do_intervalo("v", obs, [0.0], {0.0}, 0.0, 0.0) is None


def test_um_valor_por_intervalo_rotulado_mesmo_que_se_toquem():
    obs = _obs(0.0, 12, 0.9) + _obs(1.0, 12, 0.9)
    ft = [0.0, 1.0]
    eventos = pd.DataFrame([{"t_ini_s": 0, "t_fim_s": 1, "tipo": "neutro"},
                            {"t_ini_s": 0, "t_fim_s": 1, "tipo": "neutro"}])
    vals = bench.valores_por_tipo("v", obs, ft, set(ft), eventos, "neutro")
    assert len(vals) == 2 and all(v == 100.0 for _, v in vals)   # um por intervalo, sem contagem cruzada


# --- linha TOTAL --------------------------------------------------------------------------------

def _row(**kw) -> dict:
    base = {"video": "v", "provider": "p", "flavor": "local", "pares_ge64": 0, "rostos_marcados_ge64": 0,
            "rostos_detectados_ge64": 0, "quadros_rotulados_sem_deteccao": 0, "eventos_riso_rotulados": 0,
            "eventos_riso_medidos": 0, "eventos_riso_ok": 0, "eventos_riso_ok_equiv30": 0,
            "trechos_neutros_medidos": 0, "jitter_dp_pp": float("nan"), "quadros": 0, "quadros_com_plateia": 0,
            "inferencia_s": 0.0}
    base.update(kw)
    return base


def test_total_soma_eventos_e_nao_faz_media_de_fracoes():
    rows = [_row(eventos_riso_rotulados=10, eventos_riso_ok=8, jitter_dp_pp=1.0),
            _row(eventos_riso_rotulados=2, eventos_riso_ok=0, jitter_dp_pp=4.0)]
    total = bench.linha_total(rows, "p")
    assert total["frac_eventos_riso_ok"] == 0.67       # 8/12, não a média de 0,8 e 0,0
    assert total["jitter_dp_pp"] == 4.0                # pior vídeo, não a média


def test_total_do_recall_soma_pares_e_marcados():
    rows = [_row(pares_ge64=80, rostos_marcados_ge64=100, rostos_detectados_ge64=100),
            _row(pares_ge64=1, rostos_marcados_ge64=10, rostos_detectados_ge64=1)]
    total = bench.linha_total(rows, "p")
    assert total["recall_ge64_max"] == 0.736 and total["razao_contagem_ge64"] == 0.918


def test_custo_por_hora_de_video_a_um_quadro_por_segundo():
    # 1 h de vídeo = 3600 quadros; 0,5 s de inferência por quadro = 0,5 h de máquina
    total = bench.linha_total([_row(flavor="t4-small", quadros=100, inferencia_s=50.0)], "p")
    assert total["fps"] == 2.0 and total["custo_por_hora_video_usd"] == 0.2      # 0,40 US$/h × 0,5


# --- resolução do corpus ------------------------------------------------------------------------

def test_resolve_pasta_deixa_caminho_local_intacto_e_recusa_uri_incompleta():
    import pytest
    assert bench.resolve_pasta("samples/pib", {}) == "samples/pib"
    with pytest.raises(ValueError, match="incompleta"):
        bench.resolve_pasta("hf://datasets/so-um-nivel", {})
