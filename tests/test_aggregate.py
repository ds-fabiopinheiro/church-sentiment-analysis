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


def test_media_de_95_rostos_e_insuficiente():
    """round(9.5) é 10 no Python; a regra 3 exige 10 rostos mensuráveis, não 9,5."""
    obs = _obs(0.0, 70, 9) + _obs(1.0, 70, 10)
    aggs = aggregate("c", "f", obs, [0.0, 1.0], {0.0, 1.0})
    assert aggs[0].insuficiente is True
    assert aggs[0].pct_sorrindo is None and aggs[0].pct_voltados is None


def test_quadros_sem_plateia_nao_diluem_a_media():
    """frame_times traz também os quadros de púlpito; só os de plateia entram no denominador."""
    obs = _obs(0.0, 80, 20) + _obs(1.0, 80, 20)
    frame_times = [float(t) for t in range(10)]      # 10 quadros na janela, 2 deles com plateia
    aggs = aggregate("c", "f", obs, frame_times, {0.0, 1.0})
    assert aggs[0].quadros == 10 and aggs[0].quadros_com_plateia == 2
    assert aggs[0].n_mensuravel == 20 and aggs[0].insuficiente is False


def test_janela_sem_quadro_de_plateia_e_insuficiente():
    aggs = aggregate("c", "f", [], [0.0, 1.0], set())
    assert aggs[0].insuficiente is True and aggs[0].n_mensuravel == 0
