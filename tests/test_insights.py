"""O texto entregue ao pastor precisa do sinal certo: events.py grava a magnitude sem sinal (regra 4)."""
from __future__ import annotations
import pytest

from reacao.insights import write
from reacao.types import Event, Segment

SEGMENTOS = [Segment(t_ini=2500.0, t_fim=2555.0, texto="a paciência no deserto e a espera do tempo de Deus")]


@pytest.fixture(autouse=True)
def _sem_llm(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)   # usa o modelo de frase, sem chamada externa


def _evento(tipo: str, magnitude_pp: float) -> Event:
    return Event(tipo=tipo, t_ini=2520.0, t_fim=2550.0, sinal="pct_voltados",
                 magnitude_pp=magnitude_pp, cobertura_min=30, momento="palavra")


def test_queda_sai_com_sinal_negativo():
    (ins,) = write([_evento("queda_atencao", 23.0)], SEGMENTOS)
    assert "-23 p.p." in ins.texto and "+23 p.p." not in ins.texto
    assert "queda de atenção aparente" in ins.texto and ins.minuto == "42:00"


def test_recuperacao_sai_com_sinal_positivo():
    (ins,) = write([_evento("recuperacao_atencao", 12.0)], SEGMENTOS)
    assert "+12 p.p." in ins.texto


def test_insight_sem_transcricao_e_descartado_pelo_lint():
    assert write([_evento("queda_atencao", 23.0)], []) == []
