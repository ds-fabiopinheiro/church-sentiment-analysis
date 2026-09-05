# Gate do PoC (PBI-105)

| # | Critério | Meta | Resultado | Fonte |
|---|---|---|---|---|
| 1 | Recall em rostos ≥ 64 px (vídeos com rostos de 34–96 px, condição da PIB) | ≥ 80% | | `out/bench/bench_<motor>.csv` |
| 2 | Sensibilidade nos eventos de riso / jitter nos trechos neutros | ≥ 15 p.p. em ≥ 70% dos eventos / ≤ 5 p.p. | | idem |
| 3 | Fronteiras de momento a ≤ 60 s da marcação manual (3 vídeos pt-BR) | ≥ 80% | | `labels/*_momentos.csv` |
| 4 | Relatório de sermão público: ≥ 3 insights; concordância Fabio + Filipe | ≥ 3/5 | | `insight_feedback` |
| 5 | Custo e tempo por hora de vídeo (T4 small) | ≤ US$ 1,50 e ≤ 2 h | | `run_log` |
| 6 | Guarda de não-persistência | passa no CI | | Actions |

Decisão: ( ) seguir para dados da PIB e RIPD  ( ) ajustar e repetir  ( ) parar. Data: ____ Assinam: Fabio Pinheiro, pastor Filipe.
