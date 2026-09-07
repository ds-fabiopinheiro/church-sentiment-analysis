"""Redação dos insights: LLM com formato fixo quando houver chave; senão modelo de frase. Sempre passa pelo lint."""
from __future__ import annotations
import os
from .types import TRECHO_AUSENTE, Event, Insight, Segment
from .transcribe import text_between
from .lint import check

NOMES = {"queda_atencao": "queda de atenção aparente", "recuperacao_atencao": "recuperação de atenção aparente", "pico_sorriso": "pico de sorriso"}
TIPOS_DE_QUEDA = {"queda_atencao"}   # events.py grava a magnitude sem sinal; o texto precisa do sinal certo


def _mmss(t: float) -> str:
    return f"{int(t)//60:02d}:{int(t)%60:02d}"


def _com_sinal(ev: Event) -> float:
    """Queda sai negativa no texto; subida, positiva."""
    return -abs(ev.magnitude_pp) if ev.tipo in TIPOS_DE_QUEDA else abs(ev.magnitude_pp)


def _template(ev: Event, trecho: str) -> Insight:
    texto = (f"Aos {_mmss(ev.t_ini)}, no momento '{ev.momento}', enquanto o pregador dizia \"{trecho[:160]}\", "
             f"a reação observada foi {NOMES.get(ev.tipo, ev.tipo)}: {ev.sinal} variou {_com_sinal(ev):+.0f} p.p. "
             f"em rostos mensuráveis (n ≥ {ev.cobertura_min}).")
    return Insight(minuto=_mmss(ev.t_ini), momento=ev.momento, trecho=trecho[:200], texto=texto, sinais=[ev.sinal], evento=ev.tipo)


def write(events: list[Event], segments: list[Segment], max_insights: int = 8) -> list[Insight]:
    events = sorted(events, key=lambda e: -abs(e.magnitude_pp))[:max_insights]
    out: list[Insight] = []
    key = os.environ.get("ANTHROPIC_API_KEY")
    client = None
    if key:
        import anthropic
        client = anthropic.Anthropic(api_key=key)
    for ev in events:
        trecho = text_between(segments, ev.t_ini - 30, ev.t_fim) or TRECHO_AUSENTE
        ins = _template(ev, trecho)
        if client:
            prompt = (
                "Reescreva o insight abaixo para um pastor, em português, em UMA frase de até 45 palavras. "
                "Regras obrigatórias: descreva a reação OBSERVADA (rostos voltados ao palco, sorrisos), nunca sentimentos "
                "ou emoções da congregação; nunca cite pessoa, fileira ou assento; mantenha o minuto, o momento do culto, "
                "o trecho citado entre aspas e o sinal usado. Responda só com a frase.\n\n" + ins.texto
            )
            try:
                msg = client.messages.create(model="claude-sonnet-4-6", max_tokens=300, messages=[{"role": "user", "content": prompt}])
                cand = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text").strip()
                if cand and not check(Insight(ins.minuto, ins.momento, ins.trecho, cand, ins.sinais, ins.evento)):
                    ins.texto = cand
            except Exception:
                pass
        erros = check(ins)
        if erros:
            print(f"[lint] insight rejeitado {ins.minuto}: {erros}")
            continue
        out.append(ins)
    return out
