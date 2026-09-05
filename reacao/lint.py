"""Lint de linguagem controlada: reação observada, nunca estado interno; sempre com minuto, momento, trecho e sinais."""
from __future__ import annotations
import re
from .types import Insight

PROIBIDO = [r"\bsentir(am|a|em)\b", r"\bsentimento", r"entediad", r"emocionad", r"\bfelizes?\b", r"\btristes?\b",
            r"\bgostaram\b", r"\bnão gostaram\b", r"\bdistraíd", r"\bdesinteress", r"\bcansad", r"\bemoç(ão|ões)\b"]
PROIBIDO_INDIVIDUAL = [r"\buma pessoa\b", r"\bo (homem|rapaz|senhor)\b", r"\ba (mulher|moça|senhora)\b", r"\bfileira\b", r"\bassento\b"]


def check(ins: Insight) -> list[str]:
    erros = []
    txt = ins.texto.lower()
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
    return erros
