from reacao.events import detect_events
from reacao.types import WindowAggregate, Moment


def _w(i, voltados, sorrindo=20.0):
    return WindowAggregate("c", "f", i * 30, (i + 1) * 30, 30, 30, 120, 60, False, pct_voltados=voltados, pct_sorrindo=sorrindo, expressividade=40.0)


def test_sustained_drop_is_detected_once():
    series = [80, 80, 80, 80, 60, 58, 57, 56, 79, 80]
    aggs = [_w(i, v) for i, v in enumerate(series)]
    ev = detect_events(aggs, [Moment("palavra", 0, 9999)])
    tipos = [e.tipo for e in ev]
    assert tipos.count("queda_atencao") == 1
    assert "recuperacao_atencao" in tipos


def test_smile_spike():
    aggs = [_w(i, 80, sorrindo=(60 if i == 8 else 20)) for i in range(10)]
    ev = detect_events(aggs, [Moment("palavra", 0, 9999)])
    assert any(e.tipo == "pico_sorriso" and e.t_ini == 240 for e in ev)


def test_insufficient_windows_are_ignored():
    aggs = [_w(i, 80) for i in range(10)]
    aggs[4].insuficiente = True
    aggs[4].pct_voltados = 10
    assert not [e for e in detect_events(aggs, [Moment("palavra", 0, 9999)]) if e.tipo == "queda_atencao"]
