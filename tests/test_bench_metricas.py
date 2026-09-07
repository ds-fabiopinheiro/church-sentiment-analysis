"""Matemática das métricas do gate no bench: janelas por intervalo, fração de eventos sensíveis, resolução do corpus."""
from __future__ import annotations
import importlib.util
import math
import os

import pandas as pd
import pytest

from reacao.types import WindowAggregate

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("bench", os.path.join(RAIZ, "bench.py"))
bench = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bench)


def _janela(t_ini: float, pct_sorrindo: float | None, insuficiente: bool = False) -> WindowAggregate:
    return WindowAggregate("v", "bench", t_ini, t_ini + 10, 10, 10, 40, 20, insuficiente, pct_sorrindo=pct_sorrindo)


def test_janela_conta_por_sobreposicao_nao_por_inicio():
    aggs = [_janela(0, 10.0), _janela(10, 60.0), _janela(20, 12.0)]
    # evento de 12 s a 18 s cai inteiro dentro da segunda janela, que começa antes dele
    assert bench.janelas_no_intervalo(aggs, 12, 18, "pct_sorrindo") == [60.0]
    assert bench.janelas_no_intervalo(aggs, 5, 25, "pct_sorrindo") == [10.0, 60.0, 12.0]


def test_janela_insuficiente_e_valor_nulo_sao_ignorados():
    aggs = [_janela(0, 90.0, insuficiente=True), _janela(10, None), _janela(20, 30.0)]
    assert bench.janelas_no_intervalo(aggs, 0, 30, "pct_sorrindo") == [30.0]


def test_fracao_de_eventos_conta_pico_por_evento():
    aggs = [_janela(0, 12.0), _janela(10, 60.0), _janela(20, 14.0), _janela(30, 18.0)]
    eventos = pd.DataFrame([{"t_ini_s": 10, "t_fim_s": 19, "tipo": "riso"},     # pico 60, sobe 48 p.p.
                            {"t_ini_s": 30, "t_fim_s": 39, "tipo": "riso"},     # pico 18, sobe 6 p.p.
                            {"t_ini_s": 0, "t_fim_s": 9, "tipo": "neutro"},
                            {"t_ini_s": 20, "t_fim_s": 29, "tipo": "neutro"}])
    frac, n = bench.fracao_eventos_sensiveis(aggs, eventos, base=13.0, limiar_pp=15.0)
    assert (frac, n) == (0.5, 2)


def test_fracao_sem_eventos_medidos_e_nan():
    frac, n = bench.fracao_eventos_sensiveis([_janela(0, 12.0)], pd.DataFrame(columns=["t_ini_s", "t_fim_s", "tipo"]), 12.0, 15.0)
    assert math.isnan(frac) and n == 0


def test_mediana_e_media_de_lista_vazia_sao_nan():
    assert math.isnan(bench.mediana([])) and math.isnan(bench.media([]))
    assert bench.mediana([1.0, 5.0, 2.0]) == 2.0 and bench.mediana([1.0, 3.0]) == 2.0


def test_resolve_pasta_deixa_caminho_local_intacto_e_recusa_uri_incompleta():
    assert bench.resolve_pasta("samples/pib", {}) == "samples/pib"
    with pytest.raises(ValueError, match="incompleta"):
        bench.resolve_pasta("hf://datasets/so-um-nivel", {})
