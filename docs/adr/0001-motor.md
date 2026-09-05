# ADR 0001 — Motor de expressão facial (preencher após o bake-off)

Contexto: Hume Expression Measurement encerrada em 14/06/2026; Affectiva/iMotions fora do orçamento (≥ € 9.000/ano);
produção 100% local em servidor com GPU NVIDIA; nenhum áudio de plateia; rostos de 34–96 px de altura nas câmeras atuais da PIB.

Candidatos: HSEmotion (ONNX, recorte), LibreFace (AUs), Py-Feat (AUs + emoções). Detector comum: insightface SCRFD, só detecção.

| Motor | recall ≥64 px | sensibilidade (p.p.) | jitter (p.p.) | fps T4 | custo/h vídeo | licença | decisão |
|---|---|---|---|---|---|---|---|
| hsemotion | | | | | | Apache-2.0 (verificar modelo) | |
| libreface | | | | | | verificar | |
| pyfeat | | | | | | MIT (modelos internos: verificar) | |

Decisão: produção = ____ ; reserva = ____ . Motivos: ____
