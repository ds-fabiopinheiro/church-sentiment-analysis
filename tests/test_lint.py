import pytest

from reacao.lint import check
from reacao.types import TRECHO_AUSENTE, Insight


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


@pytest.mark.parametrize("frase", [
    "Aos 42:10 a congregação sentiu tédio durante a palavra.",
    "Aos 42:10 as pessoas se sentem alegres com a mensagem.",
    "Aos 42:10 a plateia ficou comovida e animada.",
    "Aos 42:10 os presentes seguiram atentos à mensagem.",
])
def test_rejects_more_internal_state_wording(frase):
    assert check(_ins(frase))


def test_rejects_placeholder_excerpt():
    i = Insight(minuto="42:10", momento="palavra", trecho=TRECHO_AUSENTE,
                texto='Aos 42:10 a reação observada foi queda de atenção aparente: rostos voltados ao palco caíram 18 p.p.',
                sinais=["pct_voltados"])
    assert "sem transcrição para citar neste trecho" in check(i)


def test_rejects_text_without_minute_or_excerpt():
    sem_minuto = _ins('No momento palavra, enquanto o pregador dizia "a paciência no deserto", os rostos voltados ao palco caíram 18 p.p.')
    assert "o minuto não aparece no texto" in check(sem_minuto)
    sem_trecho = _ins("Aos 42:10 os rostos voltados ao palco caíram 18 p.p. (n ≥ 30).")
    assert "o trecho citado não aparece no texto" in check(sem_trecho)
