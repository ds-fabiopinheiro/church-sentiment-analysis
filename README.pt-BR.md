# Church Sentiment Analysis — Painel de Reação do Culto

> Retorno agregado e anônimo ao pregador: o que aconteceu na sala em cada parte da mensagem.

**Leia em:** [English](README.md) · Português · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [العربية](README.ar.md) · [中文](README.zh-CN.md) · [日本語](README.ja.md)

## Por quê
Numa pesquisa do Pew Research (2016), 83% das pessoas que procuraram uma nova igreja disseram que a qualidade dos sermões pesou na escolha — o fator mais citado. Mesmo assim, a maioria dos pregadores recebe só "bom sermão" na saída. Este projeto dá ao pregador uma visão objetiva, anônima e agregada de como a congregação reagiu, minuto a minuto, ligada à transcrição da mensagem, para preparar melhor a próxima.

## O que faz
- Lê a gravação de um culto (arquivo de vídeo).
- Detecta rostos nas cenas com plateia e mede, por janela de 30 segundos, só valores agregados: número de rostos mensuráveis, % voltados ao palco, % sorrindo, expressividade.
- Transcreve o áudio do púlpito e divide o culto em momentos (louvor, oração, avisos, palavra, apelo).
- Encontra subidas e quedas sustentadas e redige de 3 a 8 insights, cada um com minuto, momento, trecho citado e sinais usados.

## O que nunca faz (garantido por código e CI)
1. Nunca guarda um quadro, um recorte de rosto ou uma cópia do vídeo.
2. Nunca identifica ninguém: sem reconhecimento facial, sem embeddings, sem rastreamento entre quadros, sem cruzamento com cadastro de membros.
3. Nunca reporta uma janela com menos de 10 rostos mensuráveis; nada por assento, setor pequeno ou pessoa.
4. Nunca diz o que as pessoas "sentiram"; a linguagem é restrita à reação observada.
5. Nunca classifica pregadores nem avalia membros.

## Como roda
A mesma imagem Docker roda em qualquer lugar:
- Prova de conceito: Hugging Face Jobs na GPU mais barata (T4 small, cerca de US$ 0,40 por hora; US$ 0,30–1,10 por culto). Veja `docs/hf-jobs.md`.
- Produção: servidor NVIDIA local dentro da igreja, 100% on-premises. Veja `docs/onprem.md`.

Início rápido (local, motor simulado, sem GPU):
```
uv run processar_culto.py --video culto.mp4 --culto 2026-09-06-19h --provider mock --out out/
```

## Situação e roteiro
- Fase 0 (agora): prova de conceito com vídeos públicos de pregação que permitem download; gate com seis critérios mensuráveis (`docs/poc-gate.md`).
- Fase 1: piloto com uma igreja (4 cultos), após relatório de impacto à privacidade e aviso à congregação.
- Depois: painel ao vivo para a cabine e sinal discreto ao pregador.

## Para igrejas de outros países
As exigências legais variam (GDPR, LGPD e outras). As regras de "O que nunca faz" são o mínimo; verifique a lei local antes de processar suas próprias gravações. Traduções, conjuntos de dados de validação e notas sobre a lei local são bem-vindos.

## Contribuir
Veja `CONTRIBUTING.md`. Para adicionar um idioma, copie `README.md` para `README.<idioma>.md` e inclua o link acima.

## Licença
Apache-2.0 para este código. Modelos de terceiros mantêm suas próprias licenças (veja `docs/adr/0001-motor.md`).

## Origem
Iniciado na Primeira Igreja Batista de Campo Grande, Brasil, por Fabio Pinheiro, como projeto voluntário, para servir pregadores em qualquer lugar. "Ide, portanto, fazei discípulos de todas as nações" (Mateus 28:19).
