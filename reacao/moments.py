"""Segmentação do culto em momentos. LLM (Anthropic) quando houver chave; senão heurística por palavras-chave."""
from __future__ import annotations
import json
import os
from .types import Segment, Moment, WindowAggregate

MOMENTOS = ["louvor", "oracao", "avisos", "palavra", "apelo", "ceia", "encerramento"]
KEYS = {
    "louvor": ["cantar", "adorar", "louvar", "aleluia", "vamos cantar"],
    "oracao": ["vamos orar", "oremos", "senhor, nós", "em nome de jesus, amém"],
    "avisos": ["aviso", "programação", "próximo domingo", "inscrição", "célula", "pgm"],
    "apelo": ["quem quer", "levante a mão", "venha à frente", "aceitar jesus", "entregar sua vida"],
    "ceia": ["ceia", "pão e o cálice", "corpo de cristo"],
    "encerramento": ["bênção", "vão em paz", "até o próximo", "boa noite a todos"],
}


def _heuristic(segments: list[Segment], duration: float) -> list[Moment]:
    labels = []
    for s in segments:
        low = s.texto.lower()
        lab = "palavra"
        for m, ks in KEYS.items():
            if any(k in low for k in ks):
                lab = m
                break
        labels.append((s.t_ini, lab))
    # histerese simples: só troca de momento com 2 segmentos consecutivos concordantes
    out: list[Moment] = []
    cur, start, pend = None, 0.0, 0
    for t, lab in labels:
        if cur is None:
            cur, start = lab, t
            continue
        if lab != cur:
            pend += 1
            if pend >= 2:
                out.append(Moment(cur, start, t))
                cur, start, pend = lab, t, 0
        else:
            pend = 0
    if cur is not None:
        out.append(Moment(cur, start, duration))
    return out


def segment(segments: list[Segment], aggregates: list[WindowAggregate], duration: float) -> list[Moment]:
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key or not segments:
        return _heuristic(segments, duration)
    import anthropic
    client = anthropic.Anthropic(api_key=key)
    transcript = "\n".join(f"[{int(s.t_ini)//60:02d}:{int(s.t_ini)%60:02d}] {s.texto}" for s in segments)
    visual = "\n".join(f"[{int(a.t_ini)//60:02d}:{int(a.t_ini)%60:02d}] rostos={a.n_total} voltados={a.pct_voltados} sorrindo={a.pct_sorrindo}"
                       for a in aggregates)
    prompt = (
        "Você segmenta um culto evangélico brasileiro em momentos, a partir da transcrição do púlpito com horários "
        f"e de sinais visuais agregados da plateia. Momentos possíveis: {', '.join(MOMENTOS)}. "
        "Regras: não trocar de momento por uma frase isolada; um momento dura pelo menos 60 s. "
        "Responda SOMENTE com JSON: uma lista de objetos {\"nome\", \"t_ini\", \"t_fim\"} em segundos, cobrindo todo o culto.\n\n"
        f"Duração: {int(duration)} s\n\nTRANSCRIÇÃO:\n{transcript[:60000]}\n\nSINAIS VISUAIS (por 30 s):\n{visual[:20000]}"
    )
    msg = client.messages.create(model="claude-sonnet-4-6", max_tokens=2000, messages=[{"role": "user", "content": prompt}])
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text").replace("```json", "").replace("```", "").strip()
    try:
        data = json.loads(text)
        return [Moment(d["nome"], float(d["t_ini"]), float(d["t_fim"])) for d in data if d.get("nome") in MOMENTOS]
    except Exception:
        return _heuristic(segments, duration)


def moment_at(moments: list[Moment], t: float) -> str:
    for m in moments:
        if m.t_ini <= t < m.t_fim:
            return m.nome
    return "desconhecido"
