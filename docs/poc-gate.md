# Gate do PoC (PBI-105)

Os números vêm da linha `TOTAL` de `out/bench/bench_<motor>.csv`, que agrega o corpus inteiro. As linhas por vídeo
são diagnóstico: com clipes de poucos segundos, cada um tem 0 ou 1 evento e a fração por vídeo só pode dar 0 ou 1.

| # | Critério | Métrica exata | Meta | Resultado | Fonte |
|---|---|---|---|---|---|
| 1 | Recall em rostos ≥ 64 px (vídeos com rostos de 34–96 px, condição da PIB) | `recall_ge64_max`: soma de min(detectados, marcados) por quadro rotulado, sobre o total marcado | ≥ 80% | | `bench_<motor>.csv`, linha TOTAL |
| 2a | Sensibilidade nos eventos de riso | `frac_eventos_riso_ok`: eventos de riso que sobem ≥ 15 p.p. sobre a base neutra, sobre os eventos **rotulados** | ≥ 70% | | idem |
| 2b | Estabilidade nos trechos neutros | `jitter_dp_pp`: desvio-padrão de `pct_sorrindo` entre trechos neutros, mínimo de 4 trechos | **a definir, ver nota** | | idem |
| 3 | Fronteiras de momento a ≤ 60 s da marcação manual (3 vídeos pt-BR) | comparação com `labels/*_momentos.csv` | ≥ 80% | | não medido pelo bench; precisa de culto inteiro |
| 4 | Relatório de sermão público: ≥ 3 insights; concordância Fabio + Filipe | contagem de insights aprovados pelo lint, e `insights_rejeitados_pelo_lint` no `run_log` | ≥ 3/5 | | `insight_feedback` |
| 5 | Custo e tempo por hora de vídeo (T4 small) | `custo_por_hora_video_usd` e `fps` da linha TOTAL | ≤ US$ 1,50 e ≤ 2 h | | `run_log` e bench |
| 6 | Guarda de não-persistência | passo do CI executa o pipeline e falha em violação | passa no CI | | Actions |

## Notas de medição, fixadas antes de o conjunto de teste existir

**Critério 1.** `recall_ge64_max` é um limite superior do recall pareado, sempre ≤ 1. O CSV também traz
`razao_contagem_ge64` (detectados sobre marcados), que pode passar de 1 com falso positivo e pode dar exatamente 1
escondendo perdas compensadas: é diagnóstico, não critério. Certificar o recall de verdade exigiria caixas nos
rótulos e pareamento por IoU, o que fica para depois do PoC.

**Critério 2a.** Cada intervalo rotulado é agregado sobre os seus próprios quadros, não sobre uma grade fixa, então
a medida não depende da duração do evento nem da fase da grade. O denominador são os eventos **rotulados**: evento
sem rostos mensuráveis suficientes conta como não atingido, para que um motor que perde os risos difíceis não seja
premiado. A coluna `frac_sobre_medidos` mostra a outra leitura.

**Janela.** O bench mede a subida dentro do intervalo do riso; a produção agrega em janelas de 30 s
(`reacao/types.py WINDOW_S`), onde um riso mais curto que a janela é diluído por min(duração, 30)/30. Um riso de
5 s com subida real de 48 p.p. aparece como 8 p.p. na janela de produção. Por isso o CSV traz também
`frac_equiv30`, com a subida convertida. **O gate julga o critério 2a por `frac_eventos_riso_ok`**; `frac_equiv30`
diz se a mesma sensibilidade sobreviveria ao agregador de produção, e é o número a olhar antes de prometer
detecção de riso ao pregador.

**Critério 2b, meta a definir.** A meta anterior de 5 p.p. era sobre a amplitude (máximo menos mínimo), que cresce
com o número de trechos rotulados: a mesma série passa com 2 trechos e reprova com 10. A métrica passou a ser o
desvio-padrão, que não depende disso. Para ruído gaussiano a amplitude esperada com 10 amostras é cerca de 3
desvios-padrão, então 5 p.p. de amplitude equivalem a algo perto de 1,7 p.p. de desvio-padrão. **Sugestão: 2,0
p.p.** A escolha precisa ser assinada antes de rodar o conjunto de teste; o valor de 5 p.p. entrou no repositório
sem calibração registrada. `jitter_amplitude_pp` continua no CSV como diagnóstico.

**Critério 5.** A detecção em resolução plena (1280) custa cerca de 8 vezes a do pré-filtro (640). Até o commit que
corrigiu `reacao/detect.py`, a passada plena rodava em 640 por causa de um cache, então medições anteriores a esse
commit subestimam tempo e custo.

Decisão: ( ) seguir para dados da PIB e RIPD  ( ) ajustar e repetir  ( ) parar. Data: ____ Assinam: Fabio Pinheiro, pastor Filipe.
