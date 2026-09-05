"""Janelas de 30 s por fonte, com k-mínimo sobre rostos mensuráveis (altura ≥ 64 px)."""
from __future__ import annotations
from collections import defaultdict
from statistics import median
from .types import FaceObservation, WindowAggregate, K_MIN, WINDOW_S


def aggregate(culto: str, fonte: str, observations: list[FaceObservation], frame_times: list[float],
              audience_times: set[float], window_s: int = WINDOW_S) -> list[WindowAggregate]:
    by_win: dict[int, list[FaceObservation]] = defaultdict(list)
    for o in observations:
        by_win[int(o.t // window_s)].append(o)
    frames_by_win: dict[int, int] = defaultdict(int)
    aud_by_win: dict[int, int] = defaultdict(int)
    for t in frame_times:
        w = int(t // window_s)
        frames_by_win[w] += 1
        if t in audience_times:
            aud_by_win[w] += 1
    out = []
    for w in sorted(frames_by_win):
        obs = by_win.get(w, [])
        nq = max(1, frames_by_win[w])
        meas = [o for o in obs if o.measurable]
        n_total = round(len(obs) / nq)
        n_meas = round(len(meas) / nq)
        agg = WindowAggregate(culto=culto, fonte=fonte, t_ini=w * window_s, t_fim=(w + 1) * window_s,
                              quadros=frames_by_win[w], quadros_com_plateia=aud_by_win[w],
                              n_total=n_total, n_mensuravel=n_meas, insuficiente=n_meas < K_MIN)
        if obs:
            agg.altura_mediana_px = float(median(o.h for o in obs))
        if not agg.insuficiente:
            facing = [o.facing for o in meas if o.facing is not None]
            smiles = [o.p_smile for o in meas if o.p_smile is not None]
            expr = [o.expressiveness for o in meas if o.expressiveness is not None]
            eyes = [o.eyes_closed for o in meas if o.eyes_closed is not None]
            agg.pct_voltados = round(100 * sum(facing) / len(facing), 1) if facing else None
            agg.pct_sorrindo = round(100 * sum(1 for s in smiles if s >= 0.5) / len(smiles), 1) if smiles else None
            agg.expressividade = round(100 * sum(expr) / len(expr), 1) if expr else None
            agg.pct_olhos_fechados = round(100 * sum(eyes) / len(eyes), 1) if eyes else None
        out.append(agg)
    return out
