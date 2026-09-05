# Rótulos manuais (verdade de referência do PoC)

- `<video>_faces.csv`: `t_s,altura_px` — um rosto por linha, em 20 quadros amostrados nas cenas com plateia.
  Denominador do recall. Esforço: 3.000–6.000 cliques, 3–4 h no total com ferramenta de clique.
- `<video>_eventos.csv`: `t_ini_s,t_fim_s,tipo` — `riso`, `aplauso`, `pe`, `cabeca_baixa`, `neutro`.
  8–12 eventos e 8–12 trechos neutros por vídeo. Sem áudio de plateia em produção; no PoC o som do próprio vídeo pode confirmar a marcação.
- `<video>_momentos.csv`: `t_ini_s,t_fim_s,nome` — louvor, oracao, avisos, palavra, apelo, ceia, encerramento.
