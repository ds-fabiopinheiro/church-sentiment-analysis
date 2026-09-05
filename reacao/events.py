"""Picos e quedas sustentadas nas séries agregadas (mudança de nível contra janelas anteriores do mesmo momento)."""
from __future__ import annotations
from .types import WindowAggregate, Event, Moment
from .moments import moment_at


def _series(aggs: list[WindowAggregate], field: str):
    return [(a.t_ini, a.t_fim, getattr(a, field), a.n_mensuravel) for a in aggs if not a.insuficiente and getattr(a, field) is not None]


def detect_events(aggs: list[WindowAggregate], moments: list[Moment], drop_pp: float = 15.0,
                  rise_pp: float = 10.0, sustain: int = 3, spike_pp: float = 20.0) -> list[Event]:
    events: list[Event] = []
    # quedas e recuperações de atenção aparente, sustentadas por `sustain` janelas
    s = _series(aggs, "pct_voltados")
    base, run, run_start = None, 0, None
    for i, (t0, t1, v, n) in enumerate(s):
        if base is None:
            base = v
            continue
        if base - v >= drop_pp:
            run += 1
            run_start = run_start or t0
            if run == sustain:
                events.append(Event("queda_atencao", run_start, t1, "pct_voltados", round(base - v, 1), n, moment_at(moments, run_start)))
        else:
            if run >= sustain and v - (base - drop_pp) >= rise_pp:
                events.append(Event("recuperacao_atencao", t0, t1, "pct_voltados", round(v - (base - drop_pp), 1), n, moment_at(moments, t0)))
            run, run_start = 0, None
            base = 0.8 * base + 0.2 * v      # base móvel lenta
    # picos de sorriso: janela ≥ spike_pp acima da mediana móvel das 6 anteriores
    s = _series(aggs, "pct_sorrindo")
    for i in range(6, len(s)):
        prev = sorted(x[2] for x in s[i - 6:i])[3]
        t0, t1, v, n = s[i]
        if v - prev >= spike_pp:
            events.append(Event("pico_sorriso", t0, t1, "pct_sorrindo", round(v - prev, 1), n, moment_at(moments, t0)))
    return events
