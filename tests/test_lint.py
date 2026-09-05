from reacao.lint import check
from reacao.types import Insight


def _ins(texto):
    return Insight(minuto="42:10", momento="palavra", trecho="a paciência no deserto e a espera", texto=texto, sinais=["pct_voltados"])


def test_rejects_internal_state_language():
    assert check(_ins("Aos 42:10 as pessoas sentiram tédio e ficaram tristes."))


def test_rejects_individual_reference():
    assert check(_ins("Aos 42:10 uma pessoa na terceira fileira olhou para o celular."))


def test_accepts_observed_reaction():
    ok = _ins('Aos 42:10, no momento palavra, enquanto o pregador dizia "a paciência no deserto", a reação observada foi queda de atenção aparente: rostos voltados ao palco caíram 18 p.p. (n ≥ 30).')
    assert check(ok) == []


def test_requires_fields():
    i = Insight(minuto="", momento="desconhecido", trecho="", texto="reação observada estável", sinais=[])
    assert len(check(i)) == 4
