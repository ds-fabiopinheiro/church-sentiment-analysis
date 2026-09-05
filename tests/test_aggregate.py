from reacao.aggregate import aggregate
from reacao.types import FaceObservation


def _obs(t, h, n, smile=0.9, yaw=0.0):
    return [FaceObservation(t=t, x=i, y=0, w=h, h=h, conf=0.9, yaw=yaw, pitch=0.0, p_smile=smile, expressiveness=0.5) for i in range(n)]


def test_k_min_marks_insufficient_and_hides_percentages():
    obs = _obs(0.0, 70, 7) + _obs(0.0, 30, 50)          # 7 mensuráveis (< 10) + 50 pequenos
    aggs = aggregate("c", "f", obs, [0.0], {0.0})
    assert aggs[0].insuficiente is True
    assert aggs[0].pct_sorrindo is None and aggs[0].pct_voltados is None
    assert aggs[0].n_total == 57 and aggs[0].n_mensuravel == 7


def test_sufficient_window_reports_percentages():
    obs = _obs(1.0, 80, 12, smile=0.9, yaw=5.0)
    aggs = aggregate("c", "f", obs, [1.0], {1.0})
    assert aggs[0].insuficiente is False
    assert aggs[0].pct_sorrindo == 100.0 and aggs[0].pct_voltados == 100.0


def test_no_per_person_fields_in_row():
    aggs = aggregate("c", "f", _obs(1.0, 80, 12), [1.0], {1.0})
    row = aggs[0].to_row()
    for banned in ("embedding", "track_id", "assento", "pessoa", "x", "y"):
        assert banned not in row
