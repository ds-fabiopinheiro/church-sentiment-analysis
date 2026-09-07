# Rótulos manuais (verdade de referência do PoC)

Dimensionado para o corpus real: clipes curtos de plateia (1 a 23 s cada). O pipeline amostra **1 quadro por
segundo**, então um clipe de 14 s tem 14 ou 15 quadros para rotular, não mais que isso.

- `<video>_faces.csv`: `t_s,altura_px` — um rosto por linha. Rotule **todos os quadros amostrados do clipe**
  (`t_s` = 0, 1, 2, … até o último segundo que existe no vídeo), não uma amostra deles: o recall só é medido nos
  quadros que têm rótulo, e quadro sem rótulo simplesmente não entra na conta.
  `t_s` precisa ser segundo inteiro e existir no vídeo. Rótulo em `t_s` fracionário ou depois do último quadro
  entra no denominador do recall e nunca pode ser detectado, ou seja, só derruba o número.
- `<video>_eventos.csv`: `t_ini_s,t_fim_s,tipo` — `riso`, `aplauso`, `pe`, `cabeca_baixa`, `neutro`.
  Marque os intervalos que de fato existem no clipe, tipicamente 1 a 3. **Os mínimos valem para o corpus inteiro,
  não por vídeo**: pelo menos 1 evento de `riso` e 4 trechos `neutro` somando todos os clipes. Um clipe sem trecho
  neutro usa a base neutra do corpus, o que é aceitável porque todos os clipes vêm do mesmo culto e da mesma câmera.
  Sem áudio de plateia em produção; no PoC o som do próprio vídeo pode confirmar a marcação.
- `<video>_momentos.csv`: `t_ini_s,t_fim_s,nome` — louvor, oracao, avisos, palavra, apelo, ceia, encerramento.
  Não se aplica a clipes curtos: o critério 3 do gate precisa de um culto inteiro.

Esforço: cerca de 250 quadros no corpus todo, a 20 a 40 rostos por quadro, o que dá as 3 a 4 h estimadas com
ferramenta de clique.

O nome do arquivo casa com o do vídeo: `igreja_simples_03.mp4` → `igreja_simples_03_faces.csv`. O bench ignora
sem aviso o vídeo cujo `_faces.csv` não existir com o nome exato.

## Conferir antes de medir

```
uv run python tools/validar_labels.py --labels labels/ --corpus samples/
```

Sai com código 1 no que faria o bench medir errado (coluna ausente, tempo fora da grade de quadros, tipo
desconhecido, nome sem vídeo correspondente, corpus sem riso ou com menos de 4 trechos neutros) e imprime avisos
no que merece um olhar. Rodar isso antes de subir o corpus evita perder horas de marcação por erro de formato.
