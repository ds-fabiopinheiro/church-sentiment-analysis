# Rótulos manuais (verdade de referência do PoC)

- `<video>_faces.csv`: `t_s,altura_px` — um rosto por linha, em 20 quadros amostrados nas cenas com plateia.
  Denominador do recall. Esforço: 3.000–6.000 cliques, 3–4 h no total com ferramenta de clique.
  `t_s` precisa cair em segundos inteiros: o pipeline amostra 1 quadro por segundo e rostos marcados em
  tempos quebrados não casam com quadro nenhum.
- `<video>_eventos.csv`: `t_ini_s,t_fim_s,tipo` — `riso`, `aplauso`, `pe`, `cabeca_baixa`, `neutro`.
  8–12 eventos e 8–12 trechos neutros por vídeo. Sem áudio de plateia em produção; no PoC o som do próprio vídeo pode confirmar a marcação.
  O critério 2 do gate precisa de pelo menos um `riso` e dois `neutro` por vídeo.
- `<video>_momentos.csv`: `t_ini_s,t_fim_s,nome` — louvor, oracao, avisos, palavra, apelo, ceia, encerramento.

O nome do arquivo casa com o do vídeo: `igreja_simples_03.mp4` → `igreja_simples_03_faces.csv`. O bench ignora
sem aviso o vídeo cujo `_faces.csv` não existir com o nome exato.

## Conferir antes de medir

```
uv run python tools/validar_labels.py --labels labels/ --corpus samples/
```

Sai com código 1 no que faria o bench medir errado (coluna ausente, tempo fora da grade, tipo desconhecido,
nome sem vídeo correspondente) e imprime avisos no que merece um olhar. Rodar isso antes de subir o corpus
evita perder horas de marcação por erro de formato.
