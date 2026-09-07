"""Lint de linguagem controlada: reação observada, nunca estado interno; sempre com minuto, momento, trecho e sinais."""
from __future__ import annotations
import re
from .types import TRECHO_AUSENTE, Insight

PREFIXO_TRECHO = 20     # quantos caracteres do trecho precisam aparecer no texto

PROIBIDO = [r"\bsent(ir|iu|e|em|ia|iam|iram|indo)\b", r"\bsentir(am|a|em)\b", r"\bsentimento", r"\bt[eé]dio\b",
            r"entediad", r"emocionad", r"comovid", r"\bfelizes?\b", r"\btristes?\b", r"\balegr(e|es|ia|ias)\b",
            r"\bgostaram\b", r"\bnão gostaram\b", r"\bdistraíd", r"\bdesinteress", r"\bcansad", r"\bemoç(ão|ões)\b",
            r"animad", r"empolgad", r"entusiasm", r"chatead", r"aborrec", r"impactad", r"\btocad[oa]s?\b",
            r"\bansios", r"apreensiv", r"indiferen", r"\batent[oa]s?\b"]
PROIBIDO_INDIVIDUAL = [r"\buma pessoa\b", r"\bo (homem|rapaz|senhor)\b", r"\ba (mulher|moça|senhora)\b", r"\bfileira\b", r"\bassento\b"]


def _sem_citacao(ins: Insight) -> str:
    """Tira do texto a citação literal do púlpito. O vocabulário proibido descreve a congregação, não a
    pregação: um sermão diz "a alegria do Senhor" e "os cansados", e isso não é leitura de estado interno.
    Aspas cujo conteúdo não vem do trecho continuam sendo lintadas, para o LLM não contrabandear texto."""
    return re.sub(r'"([^"]*)"', lambda m: '"…"' if m.group(1) and m.group(1) in ins.trecho else m.group(0), ins.texto)


def check(ins: Insight) -> list[str]:
    erros = []
    txt = _sem_citacao(ins).lower()
    for p in PROIBIDO:
        if re.search(p, txt):
            erros.append(f"verbo/termo de estado interno: /{p}/")
    for p in PROIBIDO_INDIVIDUAL:
        if re.search(p, txt):
            erros.append(f"referência individual ou por assento: /{p}/")
    if not ins.minuto:
        erros.append("sem minuto")
    if not ins.momento or ins.momento == "desconhecido":
        erros.append("sem momento do culto")
    if not ins.trecho or len(ins.trecho) < 8:
        erros.append("sem trecho citado")
    if not ins.sinais:
        erros.append("sem sinais")
    if ins.trecho == TRECHO_AUSENTE:
        erros.append("sem transcrição para citar neste trecho")
    elif ins.trecho and len(ins.trecho) >= 8:
        if ins.trecho[:PREFIXO_TRECHO] not in ins.texto:
            erros.append("o trecho citado não aparece no texto")
        elif '"' not in ins.texto:
            erros.append("o trecho no texto não está entre aspas")
    if ins.minuto and ins.minuto not in ins.texto:
        erros.append("o minuto não aparece no texto")
    return erros
