[Voltar ao épico](README.md)

# Preview — Feature F4 (novo) · Comparar os motores de expressão no corpus rotulado e registrar a decisão no ADR 0001

### Campos
| Campo | Conteúdo |
|---|---|
| Título | Comparar os motores de expressão no corpus rotulado e registrar a decisão no ADR 0001 |
| Tipo | Feature |
| Pai | Epic |
| Tags | F4; fase-0; gate; motor-expressao; adr-0001; hf-jobs; regra-1; regra-2; regra-3; k-minimo; PBI-000D; PBI-000H; PBI-104 |
| Estimativa | 51 pts / 266 h (soma dos PBIs, sugestão) |

### Descrição

**Problema:** O ADR 0001 está vazio. As colunas recall, sensibilidade, jitter, fps T4, custo/h, licença e decisão não têm valor (docs/adr/0001-motor.md:8-14), e nenhum job rodou no HF ('hf jobs ps -a' sem resultados em 2026-09-23). Sem esse ADR, os critérios 1, 2a e 2b do gate não têm resultado (docs/poc-gate.md:8-10). Os dois motores alternativos não rodam como estão escritos. O provider LibreFace chama get_facial_attributes_image com os padrões da biblioteca: temp_dir './tmp', onde a 0.2.0 grava a imagem alinhada com PIL, o que a guarda bloqueia. Ele lê 'au_12' como probabilidade e a chave 'head_pose', que a 0.2.0 não devolve. A 0.2.0 entrega pitch, yaw e roll da cabeça multiplicados por 360 sobre ângulos que já estão em graus. A execução para quando o MediaPipe não acha landmarks no recorte ou quando acha dois rostos nele (reacao/providers/libreface.py:29-34; reacao/guard.py:35-39; libreface 0.2.0 __init__.py:14-18,54-61 e detect_mediapipe_image.py:198,207-208,212-230,252-261,340-344). Os pesos do LibreFace vêm do Google Drive por gdown e vão para ./weights_libreface (libreface/utils.py:11-16). O provider Py-Feat importa Detector, que a 2.1.3 não exporta, e fixa device='cuda' (reacao/providers/pyfeat.py:12-14). O pyproject aceita py-feat>=0.6.1 (pyproject.toml:21), o que admite a 0.6.2. A 0.6.2 baixa e instancia o modelo de identidade facenet ao construir o Detector e rejeita identity_model=None, o que contraria a regra 2 por construção (py-feat 0.6.2 feat/pretrained.py:230-241; feat/detector.py:122,322-329). A 0.6.1 não tem modelo de identidade (py-feat 0.6.1 feat/detector.py:48-60). A 2.1.3 usa arcface como padrão e aceita None (feat/__init__.py:50-51; feat/detector.py:120,130), baixa pesos dos repositórios py-feat do HF sem revisão e carrega arquivos skops marcando como confiáveis todos os tipos desconhecidos (feat/pretrained.py:292-299). O libreface 0.2.0 exige torch==2.0.0 e o py-feat 2.1.3 exige torch>=2.5, então os dois não instalam no mesmo ambiente (METADATA das wheels; resolução seca com uv em 2026-09-23). O significado de p_smile muda de um motor para outro, mas a agregação aplica o limiar 0,5 a todos (reacao/aggregate.py:40). A agregação decide o k-mínimo pela altura dos rostos e calcula os percentuais só sobre os rostos com valor, então um rosto sem medição conta para o k-mínimo sem entrar no percentual (reacao/aggregate.py:25-40). Os limiares de voltado ao palco e de evento não têm calibração registrada (reacao/types.py:31-35; reacao/events.py:11-12). O pré-filtro conta só rostos de 24 px ou mais no quadro de 640 px, cerca de 72 px no quadro de 1920 px, e os rostos da PIB medem de 34 a 96 px. Além disso, a passada plena com det_size 1280 reduz o quadro de 1920 px para 1280 px antes do detector (processar_culto.py:73-76; reacao/types.py:6; docs/adr/0001-motor.md:4; insightface 2.0 model_zoo/scrfd.py:809-819). Os modelos pré-treinados do insightface, inclusive o detector comum aos três motores, servem só para pesquisa não comercial (insightface-2.0.dist-info/METADATA:52-54). Se a licença vetar o detector no piloto, hoje não há como trocá-lo.

**Solução proposta:** Tornar LibreFace e Py-Feat executáveis sob as regras 1 e 2, com as versões exatas que F2.1 fixa no lock das imagens de motor e pesos fixados, no ambiente e na versão do py-feat que o ADR de F2.4 decidir. Fazer cada percentual da janela e do intervalo do bench depender de pelo menos 10 rostos com valor, para que rostos sem medição não reduzam a base do percentual abaixo do k-mínimo, depois da decisão sobre a issue #1 registrada em F1.2. Registrar no ADR 0001 a licença do código e dos pesos de todo modelo carregado na execução (detector, motores, modelos embutidos em pacote e Whisper), com a decisão de uso no PoC, no espelhamento privado e no piloto. Medir nos clipes de desenvolvimento 07 a 10 o descarte do pré-filtro e a perda do detector e corrigir o piso do pré-filtro. Se a licença ou a medição exigirem, trocar o detector, ampliar a resolução de detecção ou adotar ladrilhos. Só nos clipes 07 a 10, calibrar o limiar de sorriso de cada motor e registrar a origem dos limites de voltado ao palco e dos limiares de evento. Antes de cada rodada de jobs, publicar por tag a imagem com digest que contém o código daquela etapa. Rodar, pela imagem de release que junta F4.1 a F4.5 e F4.7, um bench por motor na t4-small sobre o conjunto de teste e registrar no ADR o motor de produção e o de reserva. Todo processamento de vídeo desta Feature roda no HF Jobs, exceto os testes de CI sobre o vídeo licenciado de F1.6 (P18, P26), exceção que depende de confirmação diante da P3 revisada. Nada desta Feature vai ao painel web na Vercel.

**Usuários impactados:** Fabio Pinheiro (dono do repositório; assina o ADR 0001 e o gate; decide o enquadramento do piloto e a regra de k-mínimo por percentual), Time de Machine Learning e visão computacional, Pastor Filipe (lê o resultado dos critérios 1, 2a e 2b no gate, em F6.1), Governança e privacidade, com o encarregado de dados ainda sem nome (licenças, em F4.3)

**Valor de negócio:** Os critérios 1, 2a e 2b do gate só têm resultado quando o ADR 0001 trouxer os números do motor escolhido (docs/poc-gate.md:3-4,8-10), e a decisão de F6.1 depende deles. A Feature entrega esses números com linhagem, a escolha do motor de produção e do de reserva e a confirmação de que o detector e o motor escolhidos podem ser usados no piloto. Essa confirmação importa porque o critério 1 vale só para o detector medido (P31) e porque os pesos do detector atual servem só para pesquisa não comercial (insightface-2.0.dist-info/METADATA:52-54). A regra de k-mínimo por percentual faz com que nenhum percentual publicado venha de menos de 10 rostos medidos, como pede a regra 3 do CLAUDE.md.

**Regras de negócio:**
- RN01 – Durante a execução, cada observação de rosto guarda só t, caixa (x, y, w, h), confiança, p_smile, expressiveness, yaw, pitch e eyes_closed, sem vetor de identidade, id nem recorte, e nada disso sobrevive à agregação. Nenhum motor ou detector carrega modelo de reconhecimento ou de identidade nem calcula embedding (CLAUDE.md, regra 2; reacao/types.py:14-25; reacao/detect.py:36; reacao/providers/base.py:14-15; processar_culto.py:82).
- RN02 – Recortes e imagens intermediárias dos motores ficam só em /dev/shm e são apagados ao fim de cada rosto. A guarda faz a execução falhar se sobrar arquivo (CLAUDE.md, regra 1; reacao/guard.py:69-80).
- RN03 – Todo processamento de vídeo, bench e avaliação de modelo desta Feature roda no HF Jobs, exceto os testes de CI sobre o vídeo licenciado de F1.6, sem pessoas da congregação (P18, P26). O lançamento não usa caminho local, e cada execução paga tem aprovação prévia do dono da conta (P3 revisada; P7; P27). A exceção do CI depende de confirmação do usuário diante da P3 revisada (pendência).
- RN04 – A calibração e a medição do pré-filtro usam só os clipes de desenvolvimento 07 a 10, ou, se F3.1 vetar a PIB, os clipes públicos de desenvolvimento de F3.6 com os rótulos de F3.7 (F3.7.T4). O conjunto de teste só entra em F4.6 (docs/poc-gate.md:46-48; P8; P13).
- RN05 – Os pesos são carregados por revisão fixa, com o SHA-256 conferido antes do uso. Hash diferente faz o job falhar (mecanismo de F2.3).
- RN06 – Todo número registrado no ADR 0001 cita o arquivo de resultado e a linhagem de origem, no repositório de resultados de F2.8 (métrica de linhagem do épico).
- RN07 – Limiar sem dados suficientes para calibrar fica como está e é registrado como não calibrado, com o motivo (P8).
- RN08 – Motor cuja licença vete o uso no piloto sai da comparação. Se a licença vetar o SCRFD no piloto, ou se F4.3 vetar o espelhamento de det_500m.onnx, F4.7 é acionado.
- RN09 – As metas do gate (80% no critério 1, 70% e 15 p.p. no critério 2a e a meta do 2b assinada em F1.3) não são calibradas nesta Feature (docs/poc-gate.md:8-10).
- RN10 – O k-mínimo de 10 rostos mensuráveis por janela e a altura mínima de 64 px continuam valendo (CLAUDE.md, regra 3; reacao/types.py:5,7).
- RN11 – Cada percentual de uma janela ou de um intervalo do bench só é emitido quando a média por quadro de plateia de rostos mensuráveis com aquele valor for de pelo menos 10. Abaixo disso, o percentual sai nulo (reacao/aggregate.py:25-40; CLAUDE.md, regra 3). A regra depende da confirmação de Fabio antes de F4.6 (pendência) e é implementada depois da decisão sobre a issue #1 registrada em F1.2 (F1.2.T3).
- RN12 – O py-feat 0.6.2 não é usado: ele baixa e instancia o facenet ao construir o Detector e rejeita identity_model=None (py-feat 0.6.2 feat/pretrained.py:230-241; feat/detector.py:122,322-329).
- RN13 – Todo HF Job desta Feature roda numa imagem com digest publicada por tag a partir de um commit de main que já contém o código da etapa: tag de pré-release para os jobs de validação e de medição (F4.1, F4.2, F4.4, F4.5 e F4.7) e tag de release para o bench de F4.6. A imagem copia o código no build (Dockerfile:8-11), então código mesclado depois da publicação não entra no job.
- RN14 – As versões exatas de libreface e py-feat são fixadas por F2.1 no lock das imagens de motor. Esta Feature não altera o lock; uma mudança de versão volta a F2.1 e exige nova publicação pelo processo de F2.2.

**Fora de escopo:**
- Treino ou ajuste fino de modelos de expressão
- Motores comerciais: Hume, encerrada em 14/06/2026, e Affectiva/iMotions, a partir de 9.000 euros por ano (docs/adr/0001-motor.md:3)
- Medida de olhos fechados. Entra como PBI novo, com rótulo e bench, só se F6.2 decidir implementá-la
- Expressão e pose na GPU (F5.3, condicionada ao critério 5)
- Painel web na Vercel. Nenhum PBI desta Feature tem tela; o resultado vai ao ADR 0001 e, por F6.1, ao gate em docs/poc-gate.md
- Mudança da janela de 30 s da produção (WINDOW_S). Se a análise de F4.5 recomendar, vira item novo
- Critério 5 medido em cultos inteiros (F5.4)
- Execução local com vídeo da PIB (P3 revisada; P26)
- Escolha do ambiente e da versão do py-feat, que é do ADR de F2.4, e fixação das versões de libreface e py-feat no lock, que é de F2.1 (T2 e T3). Esta Feature entrega os insumos e confere a API na versão fixada
- Decisão sobre a issue #1 e o commit f2d5e4a, e reimplementação do k-mínimo se a decisão for reverter (F1.2)

**Dependências técnicas:**
- F1.1, F1.2, F1.3, F1.4 e F1.6: guarda e lançamento sem caminho local; tempo dos quadros e decisão registrada da issue #1 sobre o k-mínimo (F1.2.T3 e, se a decisão for reverter f2d5e4a, F1.2.T5); pré-registro das regras do gate e dos vídeos permitidos por tipo de job; bench com veredito na linha TOTAL; teste da regra 2 com vídeo de rostos licenciado
- F2.1 a F2.4, F2.6 e F2.8: lock das imagens de motor com as versões exatas de libreface e py-feat (F2.1.T2 e F2.1.T3); imagem com digest e processo de publicação por tag (F2.2); mecanismo de pesos por revisão fixa e hash (F2.3.T3); com o veto de F4.3 ao espelhamento de det_500m.onnx, os critérios 6 e 13 de F2.3 passam a F4.7; ADR do modo de execução dos jobs e da composição da imagem, que decide também a versão do py-feat (F2.4); token somente leitura dos repositórios de modelo para o CI (F2.6); repositório privado de resultados com linhagem (F2.8, que depende de F2.5, onde fica o run_id das linhas no Supabase)
- F3.1, F3.4 e F3.5 (e F3.6 e F3.7, se acionados): base legal do corpus da PIB, rótulos dos clipes de teste e de desenvolvimento com tag, leitura por revisão fixa e, no caminho alternativo, clipes públicos transferidos ao dataset privado (F3.6) com rótulos publicados com tag (F3.7), inclusive os de desenvolvimento (F3.7.T4) quando o acionamento for o veto da PIB
- HF Jobs com saldo positivo e flavor t4-small a US$ 0,40/h (https://huggingface.co/docs/hub/jobs-pricing; docs/hf-jobs.md:4; reacao/cost.py:5)
- Dataset privado ds-fabiopinheiro/reacao-poc-corpus e repositórios de modelo privados no HF (P3)
- Publicação da imagem no GHCR a cada tag v* (.github/workflows/docker.yml:3-4,19-25), a ser ajustada por F2.2 para registrar o digest
- Pacotes do PyPI: libreface 0.2.0, que exige Python de 3.9 a 3.11 e compilação do dlib 19.24.6 (libreface-0.2.0 METADATA:33,37,38,43,51; https://pypi.org/pypi/dlib/19.24.6/json; https://pypi.org/pypi/torch/2.0.0/json; https://pypi.org/pypi/mediapipe/0.10.5/json), e py-feat 0.6.1 ou 2.1.3 em versão exata, escolhida no ADR de F2.4. A 0.6.2 fica fora das opções (RN12)
- Origens dos pesos: Google Drive (LibreFace, libreface/utils.py:16); releases do GitHub cosanlab/py-feat e cosanlab/feat (py-feat 0.6.x, feat/resources/model_list.json; na 0.6.1 são 44 URLs em cosanlab/py-feat e 13 em cosanlab/feat); repositórios py-feat/* do HF (py-feat 2.1.3, feat/detector.py:180-432); GitHub (HSEmotion, hsemotion_onnx/facial_emotions.py:21); cloud.ovgu.de (6DRepNet, sixdrepnet/regressor.py:35); pacote buffalo_sc do insightface (SCRFD, reacao/detect.py:14); modelos faster-whisper medium e small (origem levantada em F4.3.T1)
- Modelos embutidos em pacote, sem download separado: FaceMesh do mediapipe 0.10.5, usado pelo LibreFace (detect_mediapipe_image.py:136,195-199), e Silero VAD do faster-whisper (faster_whisper/assets/silero_vad_v6.onnx no .venv; reacao/transcribe.py:13)

**Riscos:**
- LibreFace 0.2.0 (torch==2.0.0) e py-feat 2.x (torch>=2.5) não instalam no mesmo ambiente. Com uma imagem por motor, cada motor roda com um digest diferente, e F4.6 precisa registrar qual digest produziu cada linha do ADR.
- O MediaPipe do LibreFace pode não achar landmarks em recortes de 64 a 96 px, e com dois rostos no recorte a 0.2.0 levanta AttributeError (detect_mediapipe_image.py:198,207-208,212-230). Rostos sem medição continuam contando no k-mínimo pela altura, e os percentuais saem só dos rostos com valor (reacao/aggregate.py:25-40). Sem a regra RN11, uma janela com n_mensuravel de 10 ou mais publicaria pct_sorrindo e pct_voltados calculados sobre menos de 10 rostos medidos. Com a RN11, essas janelas ficam sem percentual, e o motor com muitos rostos sem medição perde cobertura na comparação.
- A RN11 vale para todos os motores e pode deixar sem percentual janelas que hoje publicam. Se Fabio não a confirmar antes de F4.6, o ADR 0001 registra a decisão de manter o k-mínimo só pela altura.
- O k-mínimo atual de reacao/aggregate.py vem do commit f2d5e4a, e a issue #1 continua aberta para a decisão do dono; um 'git revert' desfaz o commit (git show f2d5e4a; https://github.com/ds-fabiopinheiro/church-sentiment-analysis/issues/1). Se F1.2 reverter ou reimplementar o k-mínimo depois de F4.1.T7, a regra por percentual se perde. A dependência de F4.1.T7 em F1.2.T3 e F1.2.T5 trata esse caso.
- Na 0.6.1 do py-feat, a pose vem do img2pose, que detecta rostos por conta própria, ignora as caixas do SCRFD e devolve um dicionário com faces e poses (py-feat 0.6.1 feat/detector.py:467-500). Se a associação dessas poses às caixas do SCRFD não for confiável, o Py-Feat fica sem pct_voltados.
- Na 2.1.3, só o Detectorv2 recebe caixas externas pela API pública (feat/detector_v2.py:211), e ele usa outro modelo, multitarefa (feat/detector_v2.py:1-5). Se a 2.1.3 for escolhida, o motor comparado passa a ser esse modelo.
- Se F4.3 vetar o SCRFD no piloto e não aparecer detector só de detecção com licença compatível, o critério 1 não pode ser medido com um detector que o piloto possa usar (P31).
- Os clipes 07 a 10 somam 53 quadros (P8), e cada um é mais curto que uma janela de 30 s (samples/corpus/pib/ffprobe.csv; reacao/types.py:8). Os limiares de evento e, se houver poucos risos, o de sorriso podem chegar ao bench sem calibração.
- Não existe regra pré-registrada de escolha do motor. Se a escolha acontecer depois de ver os três resultados no conjunto de teste, o número do motor escolhido fica otimista.
- O py-feat 2.x carrega arquivos skops marcando como confiáveis todos os tipos desconhecidos (feat/pretrained.py:298-299). Se o hash não for conferido antes, um arquivo trocado na origem executaria código no job.
- A passada plena com det_size 1280 reduz os rostos pequenos antes do detector (scrfd.py:809-819), e a perda pode continuar mesmo com o piso proporcional.
- Os clipes 07 a 10 só têm planos de plateia (samples/corpus/pib/README.md:7). Eles não medem se o piso proporcional passa a aceitar quadros de púlpito como plateia.
- A imagem copia o código no build (Dockerfile:8-11). Se um job rodar numa imagem publicada antes da mesclagem do código da etapa, o número registrado no ADR 0001 não corresponde ao código revisado. As tasks de publicação registram o digest, e as tasks de QA conferem o digest de cada job na linhagem de F2.8.
- Se a exceção P26 não valer diante da P3 revisada, os testes de contrato com vídeo de F4.1 e F4.2 passam a HF Jobs, com custo por execução.
- Nenhum job rodou no HF, e o saldo de créditos e o custo total dos jobs de F4 não são conhecidos (P7).
- Com det_500m.onnx marcado como não espelhável, o mecanismo de F2.3 encerra a execução antes do primeiro quadro (critério 5 de F2.3). Se esse comportamento valer também para o uso no PoC, a medição de F4.4 com o SCRFD não roda, e o acionamento de F4.7 por medição fica sem números.

**Estratégia de fatiamento:** Por tipo de dado (motor) e por regra de negócio. Há um PBI por motor que precisa de adaptação (F4.1 LibreFace, que também leva a regra de k-mínimo por percentual, feita depois da decisão da issue #1 em F1.2, e F4.2 Py-Feat) e um PBI documental de licenças (F4.3). Depois vêm a medição e a correção do pré-filtro (F4.4), um PBI condicional de troca do detector ou da resolução de detecção (F4.7) e a calibração nos clipes de desenvolvimento (F4.5). Por fim, o bench no conjunto de teste com a decisão (F4.6). A divisão por disciplina fica nas Tasks. Cada PBI que roda jobs no HF tem uma task de DevOps que publica, antes dos jobs, a imagem com o código daquela etapa; F4.6 publica a release que junta o código de todos os PBIs anteriores.

### Critérios de aceite
- A tabela do ADR 0001 tem uma linha preenchida para cada motor comparado, cada coluna declara a unidade, e cada número cita o arquivo de resultado e a linhagem de origem.
- O ADR 0001 registra o motor de produção e o de reserva, com os motivos, ou registra quais metas dos critérios 1, 2a e 2b cada motor não atingiu.
- O ADR 0001 registra, com a fonte, a licença do código e dos pesos de todo modelo carregado na execução, baixado ou embutido em pacote (detector, motores, FaceMesh, faster-whisper e Silero VAD), e a decisão de uso no PoC, no espelhamento privado e no piloto, ou 'pendente de decisão de Fabio Pinheiro' na coluna do piloto.
- (erro) Motor que não roda sob as regras 1 e 2, ou cuja licença vete o piloto, aparece no ADR 0001 como fora da comparação, com o motivo.
- Cada limiar usado no bench do conjunto de teste tem a origem registrada num commit anterior ao primeiro job desse bench.
- O ADR 0001 traz os números do pré-filtro e do detector nos clipes 07 a 10, antes e depois da correção, e a decisão sobre F4.7.
- (erro) Nenhuma execução desta Feature carrega modelo de identidade (os testes negativos validam a configuração ou usam dublê, sem carregar o modelo), deixa imagem fora de /dev/shm ou usa clipe de teste antes de F4.6.
- Toda execução desta Feature sobre vídeo (clipes da PIB, clipes públicos ou conjunto de teste) é um HF Job com JOB_ID e digest da imagem anotados no PBI ou no registro de resultados de F2.8, e o lançador de F1.1 recusa caminho local. Os testes de CI sobre o vídeo licenciado de F1.6 ficam fora desta regra (P18, P26).
- (erro) Nenhuma janela do pipeline nem intervalo do bench publica percentual calculado sobre média menor que 10 rostos mensuráveis com aquele valor, salvo decisão contrária de Fabio registrada no ADR 0001 antes do primeiro job de F4.6.
- O digest de cada HF Job desta Feature é o de uma imagem publicada por tag depois da mesclagem do código da etapa, e o bench de F4.6 roda na imagem de release que junta F4.1 a F4.5 e F4.7, se acionado.

### Alterações em relação à árvore
- P3 revisada, parte do front end: F4 não tem tela, e o texto de F4 na árvore não cita Space para relatório, notas, revisão, perfis ou sinalização de qualidade. Por isso nenhum título mudou por esse motivo. O fora de escopo passou a registrar que nada de F4 vai ao painel web na Vercel.
- P3 revisada, parte do processamento ('todo processamento, inclusive bench e avaliação de modelos, roda no HF'): a validação de F4.1 e F4.2 e as medições de F4.4, F4.5 e F4.7 passam a ser HF Jobs explícitos, com aprovação do dono (P7) e lançamento sem caminho local (P27). Por isso F4.1 e F4.2 passam a depender de F1.1 e F2.4, e F4.4 de F1.1.
- O problema da Feature foi ampliado com evidências conferidas nas wheels e no insightface instalado: a exceção do LibreFace quando não há landmarks (detect_mediapipe_image.py:207-208), a confiança total do py-feat 2.1.3 nos tipos dos arquivos skops (feat/pretrained.py:298-299), o conflito de torch entre libreface 0.2.0 e py-feat 2.1.3 (METADATA das wheels; resolução seca com uv) e a redução do quadro de 1920 px para 1280 px na passada plena (scrfd.py:809-819).
- Regras de negócio, riscos, critérios de aceite, dependências técnicas e valor de negócio da Feature foram escritos. A árvore trazia só problema, solução, usuários, fatiamento e fora de escopo.
- F4.1: novas dependências F1.6 (o teste de contrato precisa de rosto real no CI, e os clipes da PIB não vão ao CI; P18, P26), F2.4 e F1.1. O valor 'grava yaw e pitch não nulos' virou contagem agregada no log, porque as observações por rosto são descartadas logo após a agregação (processar_culto.py:82). Entraram a regra e o critério do rosto sem landmarks e a regra que proíbe usar gaze_yaw e gaze_pitch como pose (libreface gaze_estimation/inference.py:47).
- F4.1 e F4.2: entrou o registro do conflito de torch e do ambiente de cada motor, a sincronizar com F2.1, F2.2 e F2.4.
- F4.2: novas dependências F2.4 e F1.1. Entraram a regra de conferir o hash antes de carregar arquivos skops (feat/pretrained.py:298-299,378-379,432-433) e o teste de contrato da ordem das colunas de emoção e de pose (reacao/providers/pyfeat.py:26-31).
- F4.3: título e escopo passaram a incluir o faster-whisper, medium e small (reacao/transcribe.py:6,10-12), porque F2.3 espelha o faster-whisper medium 'conforme as licenças registradas em F4.3'. Entraram também os dados de treino declarados nos caminhos e nas configurações dos pesos. Por ser um PBI documental, a verificação era a revisão de Fabio Pinheiro, sem task de QA (substituído na revisão 3).
- F4.4: novas dependências F2.3 e F2.5 (números no ADR 0001 com hash dos pesos e linhagem, conforme a métrica do épico; F2.5 trocado por F2.8 na revisão 3) e F1.1. Entraram a medição sem o pré-filtro, que separa a perda do detector, e a regra de acionamento de F4.7 registrada antes da medição. Ficou registrado que os clipes 07 a 10 só têm planos de plateia e não medem aceitação indevida.
- F4.5: os limiares de evento não podem ser exercitados nos clipes 07 a 10, que duram de 8,3 s a 15,7 s contra janelas de 30 s, e o pico_sorriso exige 6 janelas anteriores válidas (reacao/events.py:33-34). Por isso eles saem como 'mantido sem calibração', com esse motivo. O voltado ao palco só pode ser revisado pelos trechos cabeca_baixa, porque o rótulo não tem orientação por rosto (labels/README.md:6-11). Entraram a regra de que as metas do gate não são calibradas, a de que o job guarda só agregados por limiar candidato e a disciplina QA.
- F4.6: entrou a disciplina QA. Entrou o registro, em docs/hf-jobs.md, do comando do bench do gate, porque o comando atual aponta a raiz do dataset e uma pasta de rótulos inexistente e não exclui os clipes 07 a 10 (docs/hf-jobs.md:25-29). Entraram também o caminho de erro 'nenhum motor atende' e a declaração da fórmula de custo da coluna custo/h (bench.py:182-183).
- F4.7: título e opções passaram a incluir det_size na largura nativa do quadro, pela evidência de que det_size 1280 reduz o quadro de 1920 px (scrfd.py:809-819). Entraram a regra de contagem única de rostos entre ladrilhos, a medição do tempo por quadro e a dependência F1.6 (teste da regra 2 a estender ao detector novo).
- Estimativas acrescentadas como sugestão: story points por PBI e horas por Task. A árvore não trazia estimativas (P6).
- Revisão 2, py-feat: a 0.6.2 saiu das opções porque baixa e instancia o facenet e rejeita identity_model=None (feat/pretrained.py:230-241; feat/detector.py:122,322-329). A 0.6.1 foi inspecionada: não tem modelo de identidade (feat/detector.py:48-60). As opções passaram a ser py-feat==0.6.1 (imagem única) ou 2.1.3 com identity_model=None (imagem por motor). F4.2.T4 lista os modelos de identidade por versão, a premissa 'a API da 0.6.1 não foi inspecionada' foi retirada, e a premissa da Feature sobre a 0.6.x foi reescrita.
- Revisão 2, F4.2: o contexto registra os métodos públicos do Detectorv1 e do Detectorv2 da 2.1.3 (feat/detector.py:486,636,906,1067; feat/detector_v2.py:211) e, por verificação própria na wheel 0.6.1, que detect_facepose com img2pose ignora as caixas e devolve um dicionário com faces e poses (feat/detector.py:467-500), o que o provider atual não trata. F4.2.T3 foi reescrita para conferir a API, a pose e os modelos carregados na versão fixada.
- Revisão 2, F4.2: modelos carregados sem uso (l2cs e xgb na 2.1.3; os cinco obrigatórios na 0.6.1) entram no hash e no inventário. F4.2.T5 ganhou o passo que faz a biblioteca ler os arquivos conferidos (cache pré-preenchido, com HF_HUB_OFFLINE na 2.1.3) e o teste que mostra que nenhum download ocorre durante a carga. Entrou o critério correspondente.
- Revisão 2, citação do facenet: a referência a facenet_model.py:332, que está dentro de código comentado e aponta para outro repositório, foi trocada por feat/resources/model_list.json:139-142 e feat/pretrained.py:240-241 (0.6.2). As releases do GitHub cosanlab/py-feat e cosanlab/feat entraram nas origens dos pesos da Feature, de F4.3 e de F2.3.
- Revisão 2, F4.1, pose: a 0.2.0 multiplica por 360 ângulos que cv2.RQDecomp3x3 já devolve em graus (detect_mediapipe_image.py:252-261; conferido no .venv com cv2 4.11.0: 20° vira 7200), e a matriz de câmera troca cx e cy (:238-240). Entraram RN04 com conversão no provider, passo em F4.1.T1, casos em F4.1.T8 e os critérios 5 e 9.
- Revisão 2, F4.1, falhas por rosto: entrou a segunda falha (dois rostos no recorte levantam AttributeError; detect_mediapipe_image.py:198,212-230; margem de 15% em reacao/detect.py:40-45). A RN02 passou a cobrir qualquer exceção da biblioteca, com contagem por tipo, e, por verificação própria, a exigir que PersistenceViolation (subclasse de RuntimeError, reacao/guard.py:11) seja relançada. Entraram o caso de dois rostos no critério 3 e o critério 4.
- Revisão 2, F4.1, carga dos modelos: cada chamada de get_facial_attributes_image cria os solvers de AU, expressão e olhar e lê os checkpoints (AU_Recognition/solver_inference_combine.py:84,147). Entraram a RN09, a task F4.1.T3 (Machine Learning), que carrega o modelo de AU uma vez por execução e não carrega expressão nem olhar, e a exigência de uma carga por checkpoint no critério 8.
- Revisão 2, k-mínimo: o risco 2 da Feature estava errado (rostos sem medição entram no k-mínimo pela altura, e os percentuais saem de menos rostos; reacao/aggregate.py:25-40). Ele foi corrigido. Entraram a RN11 na Feature e em F4.1, o critério de erro correspondente, a task F4.1.T7 (Backend, reacao/aggregate.py), o teste com metade dos rostos sem p_smile em F4.1.T8 e a pendência de confirmação de Fabio. A disciplina Backend foi acrescentada a F4.1, com o motivo nas premissas.
- Revisão 2, ambiente do LibreFace: o contexto de F4.1 e a pendência para F2.1, F2.2 e F2.4 passaram a citar dlib==19.24.6 (só código-fonte no PyPI), cmake==3.30.3 e Python de 3.9 a 3.11 (METADATA:33,37,38). 'Instalaram' os três pacotes opencv virou 'incluíram na resolução', porque a evidência é uma resolução seca.
- Revisão 2, CI por motor: F4.1 e F4.2 ganharam uma task de DevOps (F4.1.T6 e F4.2.T6) que cria o job de CI do motor com a versão de Python e de torch e a leitura dos pesos com o token de F2.6. A disciplina DevOps foi acrescentada, com o motivo nas premissas. A definição de pronto usa um teste de fumaça com hash errado, para não criar ciclo com a task de QA que escreve o teste de contrato.
- Revisão 2, dono único da escolha do ambiente: o ADR de F2.4 decide a composição da imagem e a versão do py-feat. F4.1.T5 (antes T4) e F4.2.T1 passaram a fixar no lock o que o ADR decidiu, com definição de pronto dentro da task (lock versionado e PR com as versões resolvidas). A dependência técnica 'a decidir em F4.2' foi trocada. (Substituído na revisão 3: a fixação no lock passou a F2.1.)
- Revisão 2, testes duplicados: o teste com a guarda sobre o vídeo de F1.6 ficou só nas tasks de QA (F4.1.T8 e F4.2.T7). F4.1.T2 ficou com a lista dos arquivos que get_aligned_image grava, e F4.2.T3 com a conferência da API, da pose e dos modelos carregados.
- Revisão 2, regras da Feature: a RN01 foi reescrita com os campos que cada observação de rosto guarda (reacao/types.py:14-25). A RN03 e o critério 8 passaram a trazer a exceção dos testes de CI sobre o vídeo de F1.6 (P18, P26), com pendência de confirmação diante da P3 revisada. O critério 8 deixou de afirmar uma ausência não observável. Entraram a RN11, a RN12 e o critério 9.
- Revisão 2, validação de F4.1 e F4.2: a fixture sintética, que não tem rosto (.github/workflows/ci.yml:12), saiu dos vídeos de validação. O job roda com --min-faces-plateia 0 sobre vídeo permitido por F1.3 com rostos de 64 px ou mais (processar_culto.py:41,73-75).
- Revisão 2, dependências: F1.3 entrou em F4.1, F4.2, F4.1.T9 e F4.2.T8; F1.1 entrou em F4.6; F2.1 e F2.6 entraram em F4.1 e F4.2 pelas tasks de lock e de CI.
- Revisão 2, F4.3: o inventário passou a cobrir todo modelo carregado na execução, baixado ou embutido em pacote, com o FaceMesh do mediapipe 0.10.5 e o Silero VAD do faster-whisper. A decisão sobre o enquadramento do piloto saiu de F4.3.T3 e virou condição de Ready com dono. O critério 3 aceita 'pendente de decisão de Fabio Pinheiro', e o critério 4 aceita F4.7 em espera. O título mudou para refletir o novo escopo.
- Revisão 2, F4.4: o critério 7 passou a ser observável (tempos aceitos iguais num teste com detector simulado; quadros e quadros_com_plateia iguais no mesmo clipe), com o teste em F4.4.T2 e a conferência em F4.4.T7.
- Revisão 2, F4.5: o título passou a dizer o que o PBI entrega. Entrou a task F4.5.T3 (Machine Learning), que implementa no bench o cálculo por intervalo para a grade de limiares de p_smile e de |yaw| e |pitch|; a antiga T3 virou T4 e só executa os jobs, e a revisão do voltado ao palco depende da nova task. O critério 4 passou a referir a configuração versionada citada no ADR 0001, e F4.5.T8 confere que o ADR e a configuração trazem os mesmos valores. Story points passaram de 5 para 8.
- Revisão 2, F4.6: a coluna 'sensibilidade (p.p.)' do ADR 0001 recebe frac_eventos_riso_ok, que é fração de eventos (docs/adr/0001-motor.md:8; bench.py:176); F4.6.T4 a renomeia e declara a unidade de cada coluna, e o critério 3 foi ajustado. Entrou o critério da configuração do detector na linhagem (movido de F4.7), e o caso de erro passou a incluir o 2b.
- Revisão 2, F4.7: as tasks foram reordenadas. T1 lista as opções pelo gatilho, sem jobs novos; T2 verifica a licença dos candidatos antes da escolha; T3 escolhe; T4 implementa; T7 mede. Isso remove a dependência circular entre a antiga T1 e a antiga T4. Comparar e implementar opções de detecção passou a Visão Computacional, e Machine Learning saiu do PBI, com o motivo nas premissas. O critério 4 passou a validar a configuração sem carregar módulo de reconhecimento. A parte 'e F4.6 usa a mesma' do critério 8 foi para F4.6.
- Revisão 2, caminho de erro: o critério 2 da Feature e o critério 9 de F4.6 passaram a incluir a meta do critério 2b.
- Revisão 2, estimativas (sugestão): F4.1 de 5 para 8 pontos e F4.2 de 5 para 8 pontos, pelas tasks acrescentadas.
- Revisão 3, linhagem: as dependências 'resultados com linhagem' e 'repositório de resultados' passaram de F2.5 para F2.8 em F4.4 (dependências, RN07, premissas, INVEST e F4.4.T2) e em F4.6 (contexto, RN05, RN06, dependências e F4.6.T3), e também na RN06, no critério 8, na premissa P3 e nas dependências técnicas da Feature. Por verificação própria, F2.8 entrou também em F4.5 (F4.5.T4) e em F4.7 (F4.7.T4 e F4.7.T7), que registram números no ADR 0001 com arquivo de resultado e linhagem (RN06 da Feature). F2.5 continua só como dependência de F2.8.
- Revisão 3, clipes públicos: F4.6 passou a depender de F3.7 (rótulos públicos com tag), se acionado, no lugar de F3.6, e F4.6.T1 fixa a tag de F3.7 nesse caso. F4.4, F4.5, F4.4.T3 e F4.5.T4 ganharam F3.7 (F3.7.T4, rótulos públicos de desenvolvimento, publicados com tag em F3.7.T8), se o acionamento for o veto. F4.1, F4.2, F4.1.T9 e F4.2.T8 ganharam F3.6, se o acionamento for o veto. A RN04, a premissa P8/P13 e as dependências técnicas da Feature citam F3.6 e F3.7. A troca na métrica do épico ficou em pendências.
- Revisão 3, lock: a fixação de libreface e py-feat no lock ficou com F2.1 (T2 e T3), para que o lock não mude depois que F2.2 publicar os digests. F4.1.T5 saiu; o passo de registrar a versão do libreface no log foi para F4.1.T1, e F4.1.T6 passou a depender de F2.1.T3. F4.2.T1 passou a só conferir, na versão fixada por F2.1, a API usada pelo provider, com dependência de F2.1.T3 e estimativa de 4 h para 3 h. A RN06 de F4.1, a RN03 de F4.2, as dependências, as premissas, as pendências e o fora de escopo foram ajustados, e entrou a RN14 da Feature. Os números das demais tasks de F4.1 foram mantidos para não quebrar referências de outras Features a F4.1.T6.
- Revisão 3, publicação da imagem: entraram tasks de DevOps que publicam por tag a imagem com o código da etapa e registram o digest: F4.1.T10 (antes de F4.1.T9), F4.2.T9 (antes de F4.2.T8), F4.4.T8 (antes de F4.4.T3), F4.4.T9 (antes de F4.4.T5), F4.5.T9 (antes de F4.5.T4), F4.7.T9 (antes de F4.7.T7) e F4.6.T7 (release que junta F4.1 a F4.5 e F4.7, antes de F4.6.T1 e F4.6.T2). Fontes: a imagem copia o código no build (Dockerfile:8-11) e é publicada a cada tag v* (.github/workflows/docker.yml:3-4). Entraram a RN13 e o critério 10 da Feature, o critério 11 de F4.6, o digest nos critérios 1 de F4.1, F4.2 e F4.7 e no critério 4 de F4.4, e as conferências de digest nas tasks de QA. A disciplina DevOps entrou em F4.4, F4.5 e F4.7, com o motivo nas premissas, e F2.2 entrou nas dependências de F4.1, F4.2, F4.4, F4.5 e F4.7. As novas tasks receberam números seguintes aos existentes.
- Revisão 3, k-mínimo: F4.1.T7 passou a depender de F1.2.T3 (decisão registrada da issue #1) e, se a decisão for reverter f2d5e4a, de F1.2.T5, e a partir do k-mínimo que F1.2 deixar em reacao/aggregate.py. F1.2 entrou nas dependências de F4.1, a RN11 da Feature e de F4.1 cita a ordem, e entrou o risco da reversão (issue #1 aberta em 2026-09-23). A citação da regra no pré-registro de F1.3.T1 ficou em pendências.
- Revisão 3, F4.3: entrou F4.3.T5 [QA], que verifica os critérios de aceite contra as fontes depois da aprovação de Fabio em F4.3.T4. A disciplina QA foi acrescentada, com o motivo nas premissas; a premissa 'sem task de QA' e a falha de INVEST 'Testável' foram reescritas, e a definição de pronto de F4.3.T4 passou a exigir só a aprovação. Story points continuam em 3 (sugestão). F6.3.T8 ficou em pendências.
- Revisão 4, ciclo F2.3→F4.7: F4.4, F4.4.T3, F4.7 e F4.7.T5 passaram a depender de F2.3.T3 (mecanismo de pesos), e não do PBI F2.3 inteiro. F2.3 já não depende de F4.7 (detalhamento atual de F2). Com o veto de F4.3 ao espelhamento de det_500m.onnx, os critérios 6 e 13 de F2.3 passaram a F4.7: entraram a RN10 e os critérios 10 e 11 de F4.7, o passo do manifesto em F4.7.T5 e o job t4-small com a fixture sintética e o teste da regra 2 em F4.7.T8 (de 6 h para 8 h, com dependências de F4.7.T5, F4.7.T9, F1.1.T6 e aprovação). A RN01 de F4.7 e a RN08 da Feature passaram a citar o veto ao espelhamento como gatilho por licença. F1.1 entrou nas dependências de F4.7.
- Revisão 4, aprovação de job pago: F4.1.T9, F4.2.T8, F4.4.T3, F4.4.T5, F4.5.T4 e F4.7.T7 ganharam a dependência "Aprovação de Fabio (P7), com flavor, duração e custo previstos", como em F2.2.T4 e F2.7.T4, e o passo de pedir aprovação passou a citar flavor, duração e custo. F4.7.T8 ganhou a mesma dependência para o job condicional. F4.6.T3 continua dependendo de F4.6.T1, que colhe a aprovação do plano.
- Revisão 4, IDs antigos no repositório: F4.1.T1 troca PBI-000D por F4.1 em reacao/providers/libreface.py:1-2, F4.2.T2 troca por F4.2 em reacao/providers/pyfeat.py:1, e F4.4.T6, que já troca o TODO de reacao/detect.py:28 por uma referência ao ADR, retira dele PBI-000D e cita F4.7. A revisão punha a troca de detect.py em F4.7; ela ficou em F4.4.T6 porque F4.7 é condicional (P29) e F4.4.T6 já edita essa linha.
- Revisão 4, riscos e pendências: entrou o risco de o critério 5 de F2.3 impedir a medição de F4.4 com o SCRFD quando só o espelhamento for vetado, com pendência para F2.3.

### Premissas
- A P3 revisada prevalece sobre P3, P9, P10 e P11. O front end do produto é o painel web na Vercel, que lê só agregados, eventos e insights do Supabase. F4 não produz nada para ele: o ADR 0001 fica no repositório e os CSVs do bench no repositório de resultados do HF (F2.8).
- P26 lista como exceção à P3 o CI no GitHub Actions com vídeo licenciado sem pessoas da congregação (F1.6, P18). A P3 revisada não lista exceções. Esta Feature mantém a exceção só para os testes de CI de F4.1 e F4.2 e registra a confirmação como pendência; sem ela, esses testes passam a HF Job cpu-basic.
- P7: toda execução no HF Jobs gera custo e exige aprovação prévia do dono da conta.
- P8 e P13: a calibração e a medição do pré-filtro usam os clipes 07 a 10, ou, com o veto da PIB, os clipes públicos de F3.6 com os rótulos de F3.7 (F3.7.T4 para os de desenvolvimento).
- P29: as dependências de F3.6, F3.7 e F4.7 só valem se esses PBIs forem acionados.
- P31: o critério 1 vale só para o detector medido.
- Deduções aritméticas feitas sobre o código. 24 px no quadro de 640 px equivalem a 72 px no de 1920 px. Com det_size 1280, o quadro de 1920 px vai a 1280 px, então um rosto de 64 px chega ao detector com cerca de 43 px e um de 34 px com cerca de 23 px.
- A imagem base do Dockerfile é Ubuntu 22.04 cudnn-runtime, com python3 do apt e sem compilador instalado pelo apt (Dockerfile:3,5). É dedução que isso dá Python 3.10, abaixo do mínimo do py-feat 2.1.3 (METADATA:16), e que a imagem não compila o dlib do libreface. O job de fumaça de F2.2 confirma.
- Os fatos sobre o py-feat 0.6.1 vêm da wheel baixada do PyPI para o scratchpad (pf061); os da 0.6.2 e da 2.1.3, das wheels no scratchpad. A 0.6.1 não tem modelo de identidade, e a 0.6.2 o carrega sempre.
- O repositório não registra a natureza do piloto (pesquisa não comercial ou não). A decisão é de Fabio Pinheiro, fica como condição de Ready de F4.3 e, enquanto não vier, a coluna do piloto no ADR diz 'pendente de decisão de Fabio Pinheiro'.
- P6: a capacidade da sprint não está registrada. Story points e horas desta Feature são sugestão, a validar no refinamento.
- F2.5 e F2.8 na árvore revisada: F2.5 separa por run_id as linhas de cada execução no Supabase, e F2.8 envia ao repositório privado de resultados o conjunto de cada execução com linhagem. F2.8 depende de F2.5. Fontes: texto de F2.5 e F2.8 citado na revisão 3 e mapa de dependências deps_check_v3.py no scratchpad. O detalhamento revisado de F2 não está no scratchpad; a arvore_v1.json ainda junta as duas coisas em F2.5.
- É dedução que o registro dos jobs que falharam no repositório de resultados, usado pela RN06 de F4.6, é de F2.8, porque é ele que envia o conjunto de cada execução ao repositório. A confirmação fica como pendência com F2.8.
- Os IDs F2.1.T2 e F2.1.T3 (resolução dos conflitos de pacotes por imagem e lock das imagens de motor do ADR 0002), F1.2.T3 (decisão registrada da issue #1) e F1.2.T5 (k-mínimo reimplementado se a decisão for reverter f2d5e4a) vêm da revisão 3. O detalhamento revisado de F1 e F2 não está no scratchpad.
- É dedução que os jobs de validação e de medição de F4 usam imagem com digest, e não 'hf jobs uv run': os números vão ao ADR 0001 com a linhagem, que inclui o digest (F2.8), e o LibreFace precisa do dlib compilado na imagem. Se o ADR de F2.4 permitir 'hf jobs uv run' para esses jobs, as tasks de publicação criam só a tag de pré-release, que fixa script e pacote na mesma tag (F2.1).
- Revisão não aplicada em parte: F4.1, faixa de Python do LibreFace — a revisão dizia 3.8 a 3.11; ficou 3.9 a 3.11, porque o libreface 0.2.0 declara Requires-Python >=3.9 (libreface-0.2.0 METADATA:33), e torch 2.0.0 e mediapipe 0.10.5 têm wheels de cp38 a cp311.
- Revisão não aplicada em parte: F4.1 RN02, 'qualquer exceção da biblioteca deixa o rosto sem medição' — PersistenceViolation fica fora dessa captura, porque é subclasse de RuntimeError (reacao/guard.py:11) e precisa interromper a execução.
- Revisão não aplicada em parte: F4.2.T2, desligar au_model e gaze_model — vale só para a 2.1.3 (feat/detector.py:117-121). Na 0.6.1, os modelos de rosto, landmarks, AU, emoção e pose são obrigatórios (py-feat 0.6.1 feat/pretrained.py:111,125,139,183,208) e por isso entram no hash e no inventário de licenças.
- Revisão não aplicada nesta Feature (revisão 3, linhagem): troca de F2.5 por F2.8 em F5.4 e F5.4.T4, F5.5.T2, F5.7.T4, F6.1 (T1 e T2), F7.1 e F7.7 (T4) — fora de F4; registrada em pendências.
- Revisão não aplicada nesta Feature (revisão 3, clipes públicos): troca de F3.6 por F3.7 na métrica do critério 1 do épico — fora de F4; registrada em pendências.
- Revisão não aplicada nesta Feature (revisão 3, k-mínimo): citar a regra por percentual no pré-registro de F1.3.T1 — fora de F4; registrada em pendências. Das duas opções da revisão, ficou a dependência de F4.1.T7 em F1.2.T3, e não a mudança da task para F1.2, porque a RN11 é regra desta Feature e ainda depende da confirmação de Fabio.
- Revisão não aplicada nesta Feature (revisão 3, QA de PBI documental): F6.3.T8 — fora de F4; registrada em pendências.
- Revisão 4: o detalhamento atual de F2 está em feature_det_F2.json no scratchpad. Dele vêm F2.3.T3 (carga por revisão com SHA-256), os critérios 5, 6 e 13 de F2.3 e a ausência de F4.7 nas dependências de F2.3. F1.1.T6 (fixture sintética no dataset privado) vem de feature_det_F1.json.

### Pendências para sincronizar
- Azure DevOps: preencher Area Path (Time), Iteration Path, Responsável e Business Value da Feature e criar o vínculo Parent com o épico.
- F1.3: incluir no pré-registro a regra de escolha do motor de produção e do de reserva, para que a escolha em F4.6 não dependa de ver os resultados do conjunto de teste, e listar os vídeos com rostos de 64 px ou mais permitidos para os jobs de validação de F4.1 e F4.2. Se Fabio confirmar a RN11, citar a regra de k-mínimo por percentual no pré-registro (F1.3.T1).
- F1.2: F4.1.T7 altera reacao/aggregate.py depois de F1.2.T3 (decisão registrada da issue #1) e, se a decisão for reverter f2d5e4a, depois de F1.2.T5.
- F2.4 (dono único da escolha do ambiente e da versão do py-feat): entregar como insumo as duas opções. (a) Imagem única com py-feat==0.6.1 e libreface 0.2.0: Python de 3.9 a 3.11, torch==2.0.0, dlib 19.24.6 compilado, os três pacotes opencv na resolução seca (lock310.txt); a 0.6.1 não tem modelo de identidade, aceita caixas em detect_landmarks e detect_emotions, e a pose vem do img2pose, que ignora as caixas. (b) Imagem por motor com py-feat 2.1.3 e identity_model=None: Python >= 3.11 e torch >= 2.5; o Detectorv1 não recebe caixas externas pela API pública, e o Detectorv2 tem crop_faces_from_boxes com outro modelo. A 0.6.2 fica fora pela regra 2.
- F2.1 (T2 e T3), dona da fixação das versões: libreface==0.2.0 e a versão exata do py-feat decidida no ADR de F2.4 (diferente de 0.6.2) no lock das imagens de motor, com as versões resolvidas e o conflito de torch registrados. F4.1 e F4.2 só conferem o lock.
- F2.2: na imagem do LibreFace, build-essential, cmake e python3-dev para compilar o dlib; processo de publicação por tag de pré-release e de release com registro do digest, usado pelas tasks F4.1.T10, F4.2.T9, F4.4.T8, F4.4.T9, F4.5.T9, F4.7.T9 e F4.6.T7.
- F2.3: receber de F4.3 a decisão sobre o faster-whisper (medium e small) e sobre o Silero VAD, e incluir no mecanismo de pesos fixados os pesos do LibreFace e do Py-Feat, inclusive as releases do GitHub cosanlab/py-feat e cosanlab/feat (0.6.1) e os modelos obrigatórios sem uso.
- F2.6: token somente leitura dos repositórios de modelo também para os jobs de CI de F4.1.T6 e F4.2.T6.
- F2.8: confirmar que o repositório de resultados registra os jobs que falharam, com etapa e mensagem, e que a linhagem traz digest, configuração do detector, parâmetros do pré-filtro, limiar de p_smile por motor e hash dos pesos, usados por F4.4, F4.5, F4.6 e F4.7.
- F1.6: os jobs de CI por motor (F4.1.T6 e F4.2.T6) ficam ao lado do CI de F1.6, e o teste da regra 2 é estendido ao Py-Feat e ao detector de F4.7.
- F3.6 e F3.7: F4.1.T9 e F4.2.T8 dependem de F3.6, e F4.4 e F4.5 de F3.7 (F3.7.T4 e F3.7.T8), quando o acionamento for o veto da PIB; F4.6 depende de F3.7 se ele for acionado.
- Épico: na métrica do critério 1, trocar F3.6 por F3.7 (revisão 3).
- F5.4 (T4), F5.5.T2, F5.7.T4, F6.1 (T1 e T2), F7.1 e F7.7 (T4): trocar F2.5 por F2.8 ou acrescentar F2.8 onde o assunto é repositório de resultados ou linhagem; manter F2.5 em F7.4.T4, F7.5 e F7.6, onde o assunto é run_id ou falha no Supabase (revisão 3).
- F6.3: acrescentar F6.3.T8 [QA] 'Verificar os critérios de aceite do RIPD', com dependência de F6.3.T7 (revisão 3).
- Usuário: confirmar se a exceção P26 (CI no GitHub Actions com o vídeo licenciado de F1.6) continua valendo diante da P3 revisada. Se não valer, os testes de contrato com vídeo de F4.1 e F4.2 passam a HF Job cpu-basic.
- Fabio Pinheiro: confirmar, antes da sprint de F4.1, a regra de k-mínimo por percentual (RN11), ou registrar no ADR 0001, antes de F4.6, a decisão de manter o k-mínimo só pela altura.
- Fabio Pinheiro: decidir, antes da sprint de F4.3, se o piloto da Fase 1 se enquadra como pesquisa não comercial.
- F5.4: registrar quadros_com_plateia por momento nos cultos inteiros, porque os clipes 07 a 10 não medem se o piso proporcional aceita quadros de púlpito como plateia.
- F6.1: acrescentar a dependência de F4.7, apontada na crítica da árvore e fora desta Feature.
- Calibração dos limiares de evento: nenhum PBI tem rótulos de evento sobre janelas de 30 s. Decidir no refinamento se ela entra em F5.5, no plano da Fase 1 (F6.6) ou se os limiares ficam como estão.
- Custo estimado dos jobs de F4 para aprovação do dono (P7).
- F2.3: F4.4.T3 e F4.7.T5 dependem de F2.3.T3 (mecanismo), e não do PBI F2.3; com o veto ao espelhamento de det_500m.onnx, F4.7.T5 publica o detector escolhido no manifesto e F4.7.T8 verifica os critérios 6 e 13 de F2.3. Confirmar se, com o veto só ao espelhamento, a medição de F4.4.T3 pode carregar o SCRFD da origem com revisão e hash fixados (critério 5 de F2.3) (revisão 4).
- Referências aos IDs antigos: F4.1.T1 troca PBI-000D em reacao/providers/libreface.py, F4.2.T2 em reacao/providers/pyfeat.py e F4.4.T6 em reacao/detect.py:28. As demais (bench.py:5, 0001_init.sql:21, onprem.md, poc-gate.md:1, CLAUDE.md:31 e CONTRIBUTING.md:20) ficam com F1.3, F1.4, F2.1, F2.7, F5.4 e F7.2 (revisão 4).

## Preview — PBI F4.1 (novo) · Adaptar o provider LibreFace 0.2.0 para rodar sob a guarda, com pose em graus, pesos fixados e k-mínimo aplicado a cada percentual

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Adaptar o provider LibreFace 0.2.0 para rodar sob a guarda, com pose em graus, pesos fixados e k-mínimo aplicado a cada percentual |
| Tipo | Product Backlog Item |
| Pai | F4 |
| Tags | F4; libreface; motor-expressao; regra-1; regra-3; k-minimo; pesos-fixados; hf-jobs; PBI-000D |
| Estimativa | 8 pts (sugestão); tasks: 51 h |
| Dependências | F1.1 – script de lançamento que recusa caminho local (validação em HF Job, P27), F1.2 – decisão registrada da issue #1 (F1.2.T3) e, se a decisão for reverter f2d5e4a, k-mínimo reimplementado (F1.2.T5), antes de T7 (acrescentada na revisão 3), F1.3 – vídeos permitidos por tipo de job, usados na validação, F1.6 – vídeo de teste com rostos e licença, usado pelo teste de contrato no CI, F2.1 – lock das imagens de motor com libreface==0.2.0 fixado (F2.1.T2 e F2.1.T3), usado por T6, F2.2 – processo de publicação da imagem por tag com digest, usado por T10 (acrescentada na revisão 3), F2.3 – mecanismo de pesos por revisão fixa e hash, F2.4 – modo de execução dos jobs e composição da imagem, F2.6 – token somente leitura dos repositórios de modelo para o job de CI de T6, F3.1 – base legal do uso dos clipes da PIB, F3.6 – clipes públicos, se o acionamento for o veto da PIB (acrescentada na revisão 3), F4.3 – licença dos pesos do LibreFace e permissão de espelhar |
| Substitui | PBI-000D |

#### Descrição

Como integrante do time de Machine Learning e visão computacional que prepara o bench de F4.6  
Quero que o LibreFace meça os rostos mensuráveis no pipeline e no bench sem gravar imagem fora de /dev/shm, lendo as saídas que a versão fixada devolve, com a pose em graus, os modelos carregados uma vez por execução e pesos por revisão fixa, e que nenhum percentual saia de menos de 10 rostos medidos  
Para que o LibreFace seja comparado aos outros motores no conjunto de teste com números válidos, ou saia da comparação com o motivo registrado

**Contexto:** Hoje o provider grava o recorte em /dev/shm e chama libreface.get_facial_attributes_image(p) com os padrões da biblioteca, uma vez por rosto. Ele lê r['detected_aus']['au_12'] como p_smile e r['head_pose'] como pose, e o arquivo traz 'TODO: confirmar nome/retorno' (reacao/providers/libreface.py:1-2,22-37). Na 0.2.0, a função usa por padrão temp_dir='./tmp', device='cpu' e weights_download_dir='./weights_libreface' (libreface/__init__.py:14-18). Ela grava a imagem alinhada com PIL em temp_dir (detect_mediapipe_image.py:131,340), e a guarda bloqueia essa gravação fora de /dev/shm (reacao/guard.py:35-39). O .npy de landmarks e a imagem anotada têm caminho definido, mas não são gravados (detect_mediapipe_image.py:130,132,336). O retorno traz detected_aus binário (0 ou 1), au_intensities de 0 a 5, facial_expression, gaze_yaw e gaze_pitch (do olhar), os landmarks e pitch, yaw e roll (da cabeça) soltos no dicionário, sem a chave head_pose (__init__.py:30-39,54-61; detect_mediapipe_image.py:342-346; gaze_estimation/inference.py:47). A pose da cabeça sai de cv2.RQDecomp3x3, que já devolve graus, multiplicada por 360 (detect_mediapipe_image.py:252-261; https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html). No .venv do repositório (cv2 4.11.0), uma rotação de 20° em y dá 20 em RQDecomp3x3 e 7200 depois da multiplicação. A matriz de câmera põe img_h/2 na posição de cx e img_w/2 na de cy (detect_mediapipe_image.py:238-240). Com o limite de voltado ao palco em |yaw| < 30 e |pitch| < 25 (reacao/types.py:31-35), quase nenhum rosto medido pelo LibreFace sem conversão contaria como voltado. O MediaPipe roda com max_num_faces=2 (detect_mediapipe_image.py:198). Sem landmarks, a biblioteca levanta RuntimeError('No face landmarks') (:207-208). Com dois rostos no recorte, o laço chama .append em face_2d, que já virou numpy.ndarray na primeira volta, e levanta AttributeError (:212-230). O recorte tem margem de 15% (reacao/detect.py:40-45). PersistenceViolation, a exceção da guarda, é subclasse de RuntimeError (reacao/guard.py:11). Cada chamada de get_facial_attributes_image cria os solvers de AU, de expressão e de olhar, cujo construtor lê o checkpoint com torch.load, e abre um FaceMesh do MediaPipe (__init__.py:44,51-52; AU_Recognition/inference.py:97-100; AU_Recognition/solver_inference_combine.py:84,147; Facial_Expression_Recognition/inference.py:89-91; gaze_estimation/inference.py:70-71; detect_mediapipe_image.py:195-199). Os pesos vêm do Google Drive por gdown quando não estão no diretório de pesos (libreface/utils.py:11-16). O pacote exige Python >= 3.9 e fixa cmake==3.30.3, dlib==19.24.6, mediapipe==0.10.5, opencv-python==4.10.0.84 e torch==2.0.0 (METADATA:33,37,38,43,45,51). O dlib 19.24.6 só existe no PyPI como código-fonte (https://pypi.org/pypi/dlib/19.24.6/json), e torch 2.0.0 e mediapipe 0.10.5 só têm wheels de cp38 a cp311 (https://pypi.org/pypi/torch/2.0.0/json; https://pypi.org/pypi/mediapipe/0.10.5/json). O Dockerfile usa a imagem cudnn-runtime e o apt não instala compilador (Dockerfile:3,5), e o CI não fixa a versão do Python e instala só o extra dev (.github/workflows/ci.yml:8-9). Numa resolução seca com uv em 2026-09-23, libreface 0.2.0 e py-feat 2.1.3 deram incompatíveis. Os extras gpu, pyfeat e libreface juntos, em Python 3.10, resolveram py-feat 0.6.1 e torch 2.0.0 e incluíram na resolução opencv-python, opencv-python-headless e opencv-contrib-python ao mesmo tempo (lock310.txt no scratchpad). A fixação de libreface==0.2.0 no lock das imagens de motor é de F2.1 (T2 e T3). A agregação conta como mensurável todo rosto com 64 px ou mais, medido ou não, decide o k-mínimo por essa contagem e calcula os percentuais só sobre os rostos com valor (reacao/aggregate.py:25-42; reacao/types.py:27-29). Esse k-mínimo vem do commit f2d5e4a, que responde à issue #1, ainda aberta para a decisão do dono (git show f2d5e4a; https://github.com/ds-fabiopinheiro/church-sentiment-analysis/issues/1); F1.2 registra a decisão. O bench usa a mesma agregação por intervalo rotulado (bench.py:73-81), e os eventos ignoram percentuais nulos (reacao/events.py:8). As observações por rosto são apagadas logo após a agregação (processar_culto.py:82), então uma execução só mostra agregados. A imagem copia reacao/, processar_culto.py e bench.py no build (Dockerfile:8-11) e é publicada no GHCR a cada tag v* (.github/workflows/docker.yml:3-4,19-25), então o job de validação só roda o provider adaptado numa imagem publicada depois da mesclagem.

**Regras de negócio:**
- RN01 – O recorte e a imagem alinhada de cada rosto ficam em /dev/shm e são apagados ao fim do rosto, também quando a biblioteca levanta exceção (CLAUDE.md, regra 1).
- RN02 – Qualquer exceção da biblioteca num rosto, como RuntimeError('No face landmarks') ou AttributeError com dois rostos no recorte, deixa esse rosto sem medição (p_smile, expressiveness, yaw e pitch nulos), e a execução continua. O job registra só a contagem desses rostos por tipo de exceção, sem posição nem identificador. PersistenceViolation nunca é capturada pelo provider e interrompe a execução (reacao/guard.py:11).
- RN03 – p_smile vem da intensidade de AU12 (0 a 5) ou do AU12 binário. A saída e a escala usadas ficam declaradas no código e na linha libreface do ADR 0001.
- RN04 – yaw e pitch vêm da pose da cabeça, nunca do olhar (gaze_yaw, gaze_pitch), e saem do provider em graus, com a conversão da 0.2.0 (divisão por 360) feita no provider. A unidade, a conversão e a troca de cx e cy na matriz de câmera ficam registradas na linha libreface do ADR 0001.
- RN05 – Landmarks, imagem alinhada e expressão categórica devolvidos pela biblioteca não saem do provider (CLAUDE.md, regras 2 e 6).
- RN06 – A versão do libreface (0.2.0) é fixada por F2.1 no lock das imagens de motor, no ambiente decidido no ADR de F2.4 (imagem única ou por motor). Este PBI não altera o lock.
- RN07 – Os pesos são carregados por revisão fixa, com SHA-256, fora do diretório de trabalho. O espelhamento em repositório de modelo privado depende de F4.3; sem essa permissão, eles são baixados da origem com hash fixado (F2.3).
- RN08 – O dispositivo de inferência (cpu ou cuda) é parâmetro.
- RN09 – Cada modelo do LibreFace é carregado uma vez por execução. Por rosto, só o alinhamento e o modelo de AU são chamados. Os modelos de expressão e de olhar, que o provider não usa, não são carregados.
- RN10 – A validação roda em HF Job, pela imagem publicada em F4.1.T10, com --min-faces-plateia 0, sobre um vídeo permitido por F1.3 com rostos de 64 px ou mais: vídeo público (os clipes de F3.6, se o acionamento for o veto da PIB) ou, depois de F3.1, os clipes 07 a 10. Nunca roda sobre clipe de teste nem localmente com vídeo da PIB (P3 revisada; P26).
- RN11 – Cada percentual de uma janela do pipeline ou de um intervalo do bench só é emitido quando a média por quadro de plateia de rostos mensuráveis com aquele valor for de pelo menos 10 (K_MIN). Abaixo disso, o percentual sai nulo. n_mensuravel e insuficiente continuam calculados pela altura (CLAUDE.md, regra 3), sem coluna nova no schema. A implementação parte do k-mínimo que F1.2 deixar em reacao/aggregate.py depois da decisão sobre a issue #1.

**Fora de escopo:**
- Calibrar o limiar de sorriso do LibreFace (F4.5)
- Rodar o bench do conjunto de teste (F4.6)
- Decidir a licença de uso no piloto (F4.3)
- Decidir a composição da imagem e o ambiente (ADR de F2.4)
- Fixar a versão do libreface no lock (F2.1)
- Decidir sobre a issue #1 e o commit f2d5e4a (F1.2)
- get_facial_attributes_video, que extrai quadros com ffmpeg para temp_dir (libreface/__init__.py:65-76; libreface/utils.py:29-30)
- Reimplementar o alinhamento para reaproveitar o FaceMesh entre rostos
- Processamento em lote na GPU
- Medida de olhos fechados

#### Critérios de aceite

- Um HF Job com o motor LibreFace e --min-faces-plateia 0, pela imagem publicada em F4.1.T10 com o código deste PBI, sobre vídeo permitido por F1.3 com rostos de 64 px ou mais, termina com código de saída 0 e sem PersistenceViolation no log, e o digest fica anotado no PBI.
- O log desse job mostra, por vídeo, quantos rostos mensuráveis receberam p_smile, yaw e pitch e quantos ficaram sem medição, por tipo de exceção. O primeiro número é maior que zero.
- (erro) Com um recorte em que o LibreFace não acha landmarks e com um recorte com dois rostos, o provider devolve o rosto sem medição, não levanta exceção e a execução segue para o próximo rosto.
- (erro) Uma PersistenceViolation levantada dentro da chamada da biblioteca não é capturada pelo provider e interrompe a execução.
- (erro) O teste de contrato do CI falha quando falta, no retorno da versão instalada, a saída usada para p_smile, pitch ou yaw, quando o AU12 sai da escala declarada ou quando yaw ou pitch, depois da conversão, saem da faixa em graus declarada no provider.
- Ao fim do job e dos testes não há arquivo em /dev/shm/reacao nem imagem nova fora de /dev/shm, e o diretório de trabalho não tem ./tmp nem ./weights_libreface.
- (erro) Com um peso do LibreFace cujo SHA-256 difere do fixado, o job falha antes do primeiro quadro, com mensagem que nomeia o arquivo.
- O log do job registra a versão do libreface, o dispositivo usado, para cada peso a origem, a revisão ou URL e o SHA-256, e uma única carga de cada checkpoint por execução.
- A linha libreface do ADR 0001 registra de qual saída vem p_smile e em que escala, a unidade da pose e a conversão aplicada, a troca de cx e cy na matriz de câmera e se o FaceMesh é aberto a cada rosto.
- (erro) Numa janela do pipeline ou num intervalo do bench em que a média por quadro de plateia de rostos mensuráveis com p_smile for menor que 10, pct_sorrindo sai nulo, mesmo com n_mensuravel de 10 ou mais. O mesmo vale para pct_voltados com yaw e pitch. Um teste com metade dos rostos sem p_smile mostra isso.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F4.1.T1 | Machine Learning | Mapear as saídas do LibreFace 0.2.0 para p_smile, expressiveness, yaw e pitch em graus e tratar as exceções por rosto | 8 | — |
| F4.1.T2 | Visão Computacional | Manter em /dev/shm os arquivos que o alinhamento do LibreFace grava e apagá-los a cada rosto | 4 | — |
| F4.1.T3 | Machine Learning | Carregar o modelo de AU do LibreFace uma vez por execução e deixar de carregar os modelos de expressão e de olhar | 6 | F4.1.T1 |
| F4.1.T4 | MLOps | Carregar os pesos do LibreFace por revisão fixa com SHA-256, fora do diretório de trabalho | 8 | F2.3, F4.3, F4.1.T3 |
| F4.1.T6 | DevOps | Criar o job de CI do LibreFace com Python fixado, compilação do dlib e leitura dos pesos com hash | 6 | F1.6, F2.6, F2.1.T3, F4.1.T4 |
| F4.1.T7 | Backend | Aplicar em reacao/aggregate.py o k-mínimo a cada percentual, contando só os rostos com valor | 5 | F1.2.T3, F1.2.T5 (só se a decisão da issue #1 for reverter f2d5e4a) |
| F4.1.T8 | QA | Escrever os testes de contrato do LibreFace, da guarda com o vídeo de F1.6 e do k-mínimo por percentual | 8 | F1.6, F4.1.T1, F4.1.T2, F4.1.T3, F4.1.T6, F4.1.T7 |
| F4.1.T9 | QA | Executar no HF o job de validação do LibreFace e conferir os critérios de aceite | 4 | F4.1.T1, F4.1.T2, F4.1.T3, F4.1.T4, F4.1.T6, F4.1.T7, F4.1.T8, F4.1.T10, F1.1, F1.3, F2.4, F3.1, F3.6 (só se o acionamento for o veto da PIB), Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F4.1.T10 | DevOps | Publicar por tag de pré-release a imagem com o provider LibreFace adaptado e registrar o digest | 2 | F2.2, F4.1.T4, F4.1.T8 |

<details><summary>F4.1.T1 · [Machine Learning] Mapear as saídas do LibreFace 0.2.0 para p_smile, expressiveness, yaw e pitch em graus e tratar as exceções por rosto</summary>

**Objetivo:** O provider lê AU12 na escala declarada e pitch e yaw da cabeça em graus, trata as exceções da biblioteca por rosto sem engolir PersistenceViolation e conta rostos medidos e sem medição.

**Passos previstos:**
1. Ler o retorno de get_facial_attributes_image na 0.2.0 e escolher a saída de AU12 (au_intensities, 0 a 5, ou detected_aus, 0 ou 1), com a escala.
2. Se usar intensidade, normalizar p_smile para 0 a 1 e declarar a escala na docstring do provider.
3. Calcular expressiveness a partir das AUs, na mesma escala.
4. Ler pitch e yaw das chaves da pose da cabeça, e não de gaze_yaw nem de gaze_pitch, dividi-los por 360 para obter graus e declarar na docstring a faixa em graus esperada.
5. Anotar no PR a troca de cx e cy na matriz de câmera (detect_mediapipe_image.py:238-240), para a linha libreface do ADR 0001.
6. Relançar PersistenceViolation antes de qualquer captura de RuntimeError. Capturar por rosto as demais exceções da biblioteca, deixar o rosto sem medição e contar as ocorrências por tipo.
7. Expor as contagens agregadas (rostos medidos e rostos sem medição por tipo de exceção) e imprimi-las no log por vídeo, sem posição de rosto.
8. Receber o dispositivo por parâmetro e registrar no log a versão instalada do libreface e o dispositivo usado.
9. Descartar landmarks, imagem alinhada e expressão categórica dentro do provider.
10. Trocar na docstring de reacao/providers/libreface.py:1-2 a referência PBI-000D por F4.1.

**Definição de pronto:** Testes unitários com retorno simulado da 0.2.0 passam e cobrem rosto medido, landmarks ausentes, AttributeError de dois rostos, conversão de 7200 para 20 graus e PersistenceViolation relançada. ruff check e pytest passam. O PR cita F4.1 e PBI-000D. Uma busca por PBI-000D em reacao/providers/libreface.py não encontra resultado.

**Dependências:** nenhuma

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F4.1.T2 · [Visão Computacional] Manter em /dev/shm os arquivos que o alinhamento do LibreFace grava e apagá-los a cada rosto</summary>

**Objetivo:** Todo arquivo que o alinhamento da 0.2.0 grava fica num temp_dir em /dev/shm e é apagado a cada rosto, também quando há exceção.

**Passos previstos:**
1. Passar em temp_dir um subdiretório de /dev/shm/reacao criado por execução.
2. Apagar em finally, a cada rosto, o recorte, a imagem alinhada e qualquer arquivo criado no temp_dir, também quando a biblioteca levanta exceção.
3. Listar no PR os arquivos que get_aligned_image grava na 0.2.0: a imagem alinhada (detect_mediapipe_image.py:131,340). Registrar que o .npy de landmarks e a imagem anotada têm caminho definido, mas não são gravados (:130,132,336).
4. Escrever teste unitário com biblioteca simulada que grava um arquivo no temp_dir e levanta exceção, e confirmar que o provider apaga o arquivo.

**Definição de pronto:** A lista dos arquivos gravados por get_aligned_image está anotada no PR, e o teste unitário passa sem criar ./tmp no diretório de trabalho. ruff check e pytest passam.

**Dependências:** nenhuma

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.1.T3 · [Machine Learning] Carregar o modelo de AU do LibreFace uma vez por execução e deixar de carregar os modelos de expressão e de olhar</summary>

**Objetivo:** O provider cria o solver de AU uma vez e, por rosto, chama só o alinhamento e esse solver.

**Passos previstos:**
1. Criar no construtor do provider o solver de AU que a 0.2.0 usa com o model_choice padrão, com dispositivo e diretório de pesos, e reutilizá-lo em todos os rostos.
2. Chamar por rosto só o alinhamento (get_aligned_image) e o solver de AU.
3. Não criar os solvers de expressão e de olhar.
4. Registrar no log uma linha por checkpoint carregado.
5. Anotar no PR se o FaceMesh continua sendo aberto a cada rosto dentro de get_aligned_image (detect_mediapipe_image.py:195-199), para a linha libreface do ADR 0001.

**Definição de pronto:** Um teste unitário com solver simulado mostra uma única construção do solver de AU para vários rostos e nenhuma construção dos solvers de expressão e de olhar. ruff check e pytest passam. O PR cita F4.1.

**Dependências:** F4.1.T1

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F4.1.T4 · [MLOps] Carregar os pesos do LibreFace por revisão fixa com SHA-256, fora do diretório de trabalho</summary>

**Objetivo:** O job usa pesos com origem, revisão e hash conhecidos, sem chamar o gdown.

**Passos previstos:**
1. Listar os arquivos de peso que o provider carrega depois de F4.1.T3 e o weights_download_id de cada um.
2. Conforme F4.3, publicar os pesos no repositório de modelo privado usado por F2.3, ou fixar a URL de origem e o SHA-256.
3. Baixar por revisão fixa para um diretório fora do diretório de trabalho e passá-lo em weights_download_dir, para que o gdown não seja chamado (libreface/utils.py:11-16).
4. Conferir o SHA-256 antes do primeiro quadro e fazer o job falhar com mensagem que nomeia o arquivo.
5. Registrar a origem, a revisão e o hash no log e na linhagem.

**Definição de pronto:** Com um peso adulterado, a execução falha antes do primeiro quadro. Com os pesos corretos, o log mostra origem, revisão e hash. Com os pesos espelhados, não há chamada ao Google Drive.

**Dependências:** F2.3, F4.3, F4.1.T3

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F4.1.T6 · [DevOps] Criar o job de CI do LibreFace com Python fixado, compilação do dlib e leitura dos pesos com hash</summary>

**Objetivo:** Existe um job de CI que instala o extra libreface e obtém os pesos com hash, onde os testes de F4.1.T8 rodam.

**Passos previstos:**
1. Criar um job de CI separado que instala o extra libreface com o lock de F2.1 e a versão de Python fixada na faixa de 3.9 a 3.11.
2. Instalar no job o compilador e o cmake que a compilação do dlib 19.24.6 exige.
3. Dar ao job leitura dos pesos do LibreFace por revisão fixa com hash, com o token somente leitura de F2.6 passado só pelo nome.
4. Criar no job um teste de fumaça que importa o libreface e confere o hash dos pesos.
5. Configurar o job onde a pendência da Feature decidir: GitHub Actions, pela exceção P26, ou HF Job cpu-basic.

**Definição de pronto:** O job instala o extra libreface, o teste de fumaça passa com os pesos corretos e o job falha quando um peso com hash errado é oferecido.

**Dependências:** F1.6, F2.6, F2.1.T3, F4.1.T4

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F4.1.T7 · [Backend] Aplicar em reacao/aggregate.py o k-mínimo a cada percentual, contando só os rostos com valor</summary>

**Objetivo:** Nenhum percentual de janela ou de intervalo do bench sai de média menor que 10 rostos mensuráveis com aquele valor.

**Passos previstos:**
1. Ler a decisão da issue #1 registrada em F1.2.T3 e partir do k-mínimo que F1.2 deixou em reacao/aggregate.py (f2d5e4a mantido ou k-mínimo reimplementado por F1.2.T5).
2. Em aggregate, calcular para pct_voltados, pct_sorrindo, expressividade e pct_olhos_fechados a média por quadro de plateia dos rostos mensuráveis com aquele valor, na mesma base de média usada pelo k-mínimo.
3. Emitir cada percentual só quando essa média for de pelo menos K_MIN; abaixo disso, deixar o valor nulo.
4. Manter n_mensuravel e insuficiente calculados pela altura, sem coluna nova no schema.
5. Conferir que o bench herda a regra por valor_do_intervalo (bench.py:73-81) e que os eventos ignoram valores nulos (reacao/events.py:8).
6. Escrever testes unitários: janela com 12 rostos mensuráveis por quadro e 6 com p_smile sai com pct_sorrindo nulo; com 10 ou mais com valor, o percentual sai.

**Definição de pronto:** Os testes unitários passam. ruff check e pytest passam, inclusive tests/test_schema.py. O PR cita F4.1 e a issue #1.

**Dependências:** F1.2.T3, F1.2.T5 (só se a decisão da issue #1 for reverter f2d5e4a)

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F4.1.T8 · [QA] Escrever os testes de contrato do LibreFace, da guarda com o vídeo de F1.6 e do k-mínimo por percentual</summary>

**Objetivo:** Uma mudança nas chaves, na escala de AU12 ou na unidade da pose da versão instalada, uma gravação fora de /dev/shm ou um percentual sobre menos de 10 rostos com valor faz o CI falhar.

**Passos previstos:**
1. Extrair em memória um recorte de rosto com 64 px ou mais do vídeo de F1.6.
2. Chamar a versão instalada pelo provider, dentro de no_persistence, com temp_dir em /dev/shm, e verificar a presença e o tipo das chaves usadas, a escala de AU12 e yaw e pitch convertidos dentro da faixa em graus declarada.
3. Comparar, nesse recorte, a saída de AU da chamada direta do provider com a de get_facial_attributes_image.
4. Escrever o caso de retorno simulado com yaw 7200 (20° vezes 360): o provider devolve 20.
5. Escrever os casos negativos: recorte sem rosto e recorte montado em memória com dois rostos do vídeo de F1.6 voltam sem medição e sem exceção; PersistenceViolation simulada dentro da chamada interrompe a execução.
6. Escrever o teste do k-mínimo por percentual com metade dos rostos sem p_smile, pelo pipeline e pelo bench.
7. Incluir os testes no job de CI de F4.1.T6.

**Definição de pronto:** Os testes passam no job de CI com a versão fixada e falham quando uma chave usada é retirada de um retorno simulado. ruff check e pytest passam.

**Dependências:** F1.6, F4.1.T1, F4.1.T2, F4.1.T3, F4.1.T6, F4.1.T7

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F4.1.T9 · [QA] Executar no HF o job de validação do LibreFace e conferir os critérios de aceite</summary>

**Objetivo:** Os critérios de F4.1 ficam verificados com JOB_ID e digest anotados no PBI.

**Passos previstos:**
1. Pedir ao dono aprovação do job, com flavor, duração e custo previstos (P7).
2. Lançar pelo script de F1.1, pela imagem com o digest registrado em F4.1.T10, no modo do ADR de F2.4, com o motor libreface, --no-transcribe, --stdout e --min-faces-plateia 0, sobre vídeo permitido por F1.3 com rostos de 64 px ou mais (clipes de F3.6, se o acionamento for o veto da PIB).
3. Conferir o código de saída, a ausência de PersistenceViolation, as contagens por vídeo e por tipo de exceção e o log de versão, dispositivo, pesos e carga única de cada checkpoint.
4. Repetir com um peso de hash errado e conferir a falha antes do primeiro quadro.
5. Conferir a linha libreface do ADR 0001 (saída e escala de p_smile, unidade e conversão da pose, cx e cy, FaceMesh).
6. Conferir no resultado do CI os testes de contrato, da guarda e do k-mínimo por percentual.
7. Anotar no PBI os JOB_ID, o digest e o resultado de cada critério.

**Definição de pronto:** Os dez critérios de aceite estão marcados como passou ou não passou, com JOB_ID, digest e trecho de log anotados no PBI.

**Dependências:** F4.1.T1, F4.1.T2, F4.1.T3, F4.1.T4, F4.1.T6, F4.1.T7, F4.1.T8, F4.1.T10, F1.1, F1.3, F2.4, F3.1, F3.6 (só se o acionamento for o veto da PIB), Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.1.T10 · [DevOps] Publicar por tag de pré-release a imagem com o provider LibreFace adaptado e registrar o digest</summary>

**Objetivo:** O job de validação de F4.1.T9 tem uma imagem com digest que contém o código de F4.1.T1 a T4 e T7.

**Passos previstos:**
1. Conferir que os PRs de F4.1.T1, T2, T3, T4 e T7 estão mesclados em main e que os testes de F4.1.T8 passam no job de CI de F4.1.T6.
2. Criar a tag de pré-release no commit de main que contém esses PRs, pelo processo de publicação de F2.2 e na composição de imagem do ADR de F2.4 (imagem única ou imagem do LibreFace).
3. Conferir no log do build que a imagem foi construída com o lock de F2.1.
4. Registrar no PBI a tag, o commit e o digest publicado.

**Definição de pronto:** O PBI tem a tag, o commit e o digest, e o workflow de publicação desse commit terminou com sucesso.

**Dependências:** F2.2, F4.1.T4, F4.1.T8

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- reacao/providers/libreface.py:1-2,22-38
- reacao/guard.py:11,35-39,62,69-80
- reacao/aggregate.py:25-42
- reacao/types.py:5,7,14-35
- reacao/detect.py:40-45
- reacao/events.py:8
- bench.py:73-81
- processar_culto.py:41,43-45,73-75,82
- pyproject.toml:22
- Dockerfile:3,5,8-11
- .github/workflows/docker.yml:3-4,19-25
- .github/workflows/ci.yml:8-9,12
- commit f2d5e4a ('Corrige o denominador e o k-mínimo da agregação (refs #1)'); issue #1, aberta em 2026-09-23 (https://github.com/ds-fabiopinheiro/church-sentiment-analysis/issues/1)
- libreface-0.2.0 (wheel no scratchpad): libreface/__init__.py:14-63; detect_mediapipe_image.py:130-132,195-199,207-208,212-230,238-240,252-261,336,340-346; AU_Recognition/inference.py:97-100; AU_Recognition/solver_inference_combine.py:84,145-148; AU_Recognition/solver_inference_image.py:93; Facial_Expression_Recognition/inference.py:89-91; gaze_estimation/inference.py:47,70-71; utils.py:11-16; METADATA:33,37,38,43,45,51
- https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html (RQDecomp3x3 devolve ângulos em graus); conferência no .venv com cv2 4.11.0 em 2026-09-23
- https://pypi.org/pypi/dlib/19.24.6/json; https://pypi.org/pypi/torch/2.0.0/json; https://pypi.org/pypi/mediapipe/0.10.5/json
- Resolução seca com 'uv pip compile' em 2026-09-23 (libreface==0.2.0 com py-feat==2.1.3; extras gpu, pyfeat e libreface em Python 3.10; lock310.txt)
- CLAUDE.md, regras 1, 2, 3 e 6
- premissas P3 revisada, P7, P13, P18, P26 e P27

#### Verificação INVEST: pontos que falharam
- Independente: depende de F1.1, F1.2, F1.3, F1.6, F2.1, F2.2, F2.3, F2.4, F2.6, F3.1, F4.3 e, se acionado, F3.6.
- Small: 8 pontos e nove tasks. Se não couber na sprint, separar a regra de k-mínimo por percentual (T7 e o caso correspondente de T8) num PBI próprio.
- Valiosa: o benefício é para o time e para o gate; o usuário do produto não vê este PBI isolado.

#### Premissas
- Disciplinas: Machine Learning, Visão Computacional, MLOps e QA vêm da árvore. Backend entrou pela task F4.1.T7, que muda reacao/aggregate.py para aplicar o k-mínimo a cada percentual. DevOps entrou pelas tasks F4.1.T6, que cria o job de CI do LibreFace com Python fixado, compilação do dlib e leitura dos pesos com hash, e F4.1.T10, que publica a imagem com o código deste PBI antes do job de validação.
- F1.6 entrou porque o teste de contrato precisa de um rosto real e os clipes da PIB não podem ir ao CI (P18, P26).
- F1.1, F1.3 e F2.4 entraram porque, pela P3 revisada, a validação é um HF Job lançado sem caminho local (P27), no modo do ADR de F2.4, sobre um vídeo permitido por F1.3. F2.1 entra pelo lock das imagens de motor (F2.1.T3), do qual T6 depende; F2.6 pela task T6; F2.2 pela task T10; F1.2 pela task T7.
- F4.1.T5 (fixar o libreface no lock) saiu na revisão 3, porque a fixação é de F2.1. Os números das demais tasks foram mantidos para não quebrar referências de outras Features, como F1.6 e F2.6, a F4.1.T6.
- A validação usa --no-transcribe, --stdout e --min-faces-plateia 0, sem segredos do Supabase (processar_culto.py:41,43-45,108-115). É dedução que isso basta para verificar o segundo critério sem depender do pré-filtro.
- O flavor do job de validação fica a definir na task. É dedução que cpu-basic basta com dispositivo cpu.
- A escolha entre au_intensities e AU12 binário é deste PBI. F4.5 calibra o limiar na escala escolhida.
- O nome exato da chave de AU12 em au_intensities não foi conferido no levantamento; o teste de contrato o fixa. A lista de AUs da 0.2.0 inclui a 12 (AU_Recognition/solver_inference_image.py:93).
- É dedução, a partir de detect_mediapipe_image.py:238-240, que a troca de cx e cy desloca o centro óptico em recortes não quadrados. O efeito sobre yaw e pitch não foi medido e fica registrado na linha libreface do ADR 0001.
- É dedução que chamar o alinhamento e o solver de AU diretamente, em vez de get_facial_attributes_image, dá as mesmas saídas de AU. O teste de F4.1.T8 compara as duas chamadas num recorte.
- É dedução que a imagem cudnn-runtime não traz compilador para o dlib (Dockerfile:3,5); o job de fumaça de F2.2 confirma.
- A RN11 vale para todos os motores. Ela depende da confirmação de Fabio antes da sprint (pendência da Feature). Se ele preferir manter o k-mínimo só pela altura, T7 não é feita, o caso correspondente de T8 sai, e a decisão vai ao ADR 0001 antes de F4.6.
- A RN11 usa a média por quadro de plateia que f2d5e4a introduziu (reacao/aggregate.py:24-26). Se F1.2 reverter o commit, T7 aplica a regra sobre a base de média que F1.2.T5 deixar.
- Onde o job de CI de T6 roda (GitHub Actions pela exceção P26 ou HF Job cpu-basic) segue a pendência da Feature, respondida antes da sprint.
- Revisão não aplicada em parte: F4.1, faixa de Python — ficou 3.9 a 3.11, e não 3.8 a 3.11, porque o libreface 0.2.0 declara Requires-Python >=3.9 (METADATA:33).
- Revisão não aplicada em parte: F4.1 RN02 — PersistenceViolation fica fora da captura de exceções, porque é subclasse de RuntimeError (reacao/guard.py:11) e precisa interromper a execução.
- Story points e horas são sugestão, a validar no refinamento.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável, Story Points (sugestão: 8) e vínculo Parent com a Feature F4.
- F2.1 (T2 e T3): fixar libreface==0.2.0 no lock das imagens de motor e registrar as versões resolvidas (Python de 3.9 a 3.11, torch==2.0.0, mediapipe==0.10.5, opencv-python==4.10.0.84, dlib==19.24.6 compilado, cmake==3.30.3), a presença dos três pacotes opencv na resolução e o conflito com o py-feat 2.x (torch==2.0.0 contra torch>=2.5).
- F2.2: build-essential, cmake e python3-dev na imagem do LibreFace e publicação por tag de pré-release com registro do digest, usada por F4.1.T10. F2.4: composição da imagem.
- F2.3: lista de pesos do LibreFace a fixar ou espelhar, conforme F4.3 (depois de T3, só o modelo de AU é carregado).
- F2.6: token somente leitura dos repositórios de modelo para o job de CI de F4.1.T6.
- F1.2: F4.1.T7 espera F1.2.T3 e, se a decisão for reverter f2d5e4a, F1.2.T5.
- Usuário: confirmação da exceção P26 diante da P3 revisada, que define onde roda o job de F4.1.T6.
- Fabio Pinheiro: confirmação da RN11 antes da sprint.

## Preview — PBI F4.2 (novo) · Adaptar o provider Py-Feat a uma versão exata sem modelo de identidade (0.6.1 ou 2.1.3), com as caixas do SCRFD e pesos por revisão fixa

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Adaptar o provider Py-Feat a uma versão exata sem modelo de identidade (0.6.1 ou 2.1.3), com as caixas do SCRFD e pesos por revisão fixa |
| Tipo | Product Backlog Item |
| Pai | F4 |
| Tags | F4; py-feat; motor-expressao; regra-2; pesos-fixados; hf-jobs; PBI-000D |
| Estimativa | 8 pts (sugestão); tasks: 47 h |
| Dependências | F1.1 – script de lançamento que recusa caminho local, F1.3 – vídeos permitidos por tipo de job, usados na validação, F1.6 – teste da regra 2 e vídeo de teste com rostos, F2.1 – lock das imagens de motor com a versão exata do py-feat decidida no ADR de F2.4 (F2.1.T2 e F2.1.T3), conferido por T1, F2.2 – processo de publicação da imagem por tag com digest, usado por T9 (acrescentada na revisão 3), F2.3 – mecanismo de pesos por revisão fixa e hash, F2.4 – modo de execução dos jobs, composição da imagem e versão do py-feat, F2.6 – token somente leitura dos repositórios de modelo para o job de CI de T6, F3.1 – base legal do uso dos clipes da PIB, F3.6 – clipes públicos, se o acionamento for o veto da PIB (acrescentada na revisão 3), F4.3 – licença dos pesos do Py-Feat e permissão de espelhar |
| Substitui | PBI-000D |

#### Descrição

Como integrante do time de Machine Learning e visão computacional que prepara o bench de F4.6  
Quero que o Py-Feat meça os rostos mensuráveis, a partir das caixas do SCRFD, na versão exata decidida no ADR de F2.4, sem carregar nem baixar modelo de identidade e lendo só pesos com revisão fixa e hash conferido  
Para que o Py-Feat entre na comparação de F4.6 sem violar a regra 2, ou saia dela com o motivo registrado

**Contexto:** O provider importa Detector e o cria com retinaface, mobilefacenet, xgb, resmasknet e device='cuda' fixo, e o comentário diz que ele segue a API da 0.6.x (reacao/providers/pyfeat.py:1,12-14). Ele passa as caixas do SCRFD a detect_landmarks e detect_emotions, chama detect_facepose(rgb, lm) e lê happiness (coluna 3) como p_smile, 1 - neutral (coluna 6) como expressiveness e pitch e yaw pelas posições 0 e 2 de pose[0][i] (pyfeat.py:21-31). O pyproject aceita py-feat>=0.6.1 (pyproject.toml:21), o que admite a 0.6.2. Versão 0.6.1 (wheel baixada do PyPI): Detector não tem parâmetro de identidade, e o termo 'identity' não aparece em feat/detector.py nem em feat/pretrained.py (feat/detector.py:48-60). Os métodos detect_landmarks (:395), detect_facepose (:467) e detect_emotions (:590) existem. Os modelos de rosto, landmarks, AU, emoção e pose são obrigatórios, e None levanta ValueError (feat/pretrained.py:111,125,139,183,208). A pose só tem img2pose e img2pose-c (feat/pretrained.py:41-43). Com img2pose, detect_facepose devolve todas as poses que o próprio img2pose detecta no quadro, ignora caixas e landmarks e retorna um dicionário com faces e poses (feat/detector.py:467-500), o que o provider atual, que lê pose[0][i], não trata. Os pesos vêm de releases do GitHub, 44 URLs em cosanlab/py-feat e 13 em cosanlab/feat (feat/resources/model_list.json), e são baixados com download_url do torchvision para feat/resources, dentro do pacote (feat/utils/io.py:33-35,71-80). O código é MIT (METADATA:8). Versão 0.6.2: Detector usa por padrão identity_model='facenet' (feat/detector.py:57-58). identity_model=None levanta ValueError (feat/pretrained.py:230-233), e o construtor baixa o facenet de github.com/cosanlab/py-feat/releases/download/v0.1 (feat/pretrained.py:240-241; feat/resources/model_list.json:139-142) e o instancia (feat/detector.py:122,322-329). A 0.6.2 viola a regra 2 por construção. Versão 2.1.3: o pacote exporta só Detectorv1 e Detectorv2 (feat/__init__.py:50-51). No Detectorv1, identity_model tem padrão 'arcface' e aceita None, e au_model e gaze_model também aceitam None (feat/detector.py:117-121,130); o gaze_model 'l2cs' é carregado por padrão (:131,464-466). Os métodos públicos do Detectorv1 são detect_faces (:486), forward (:636) e detect (:906). Nenhum recebe caixas externas: detect roda o detector de rostos do próprio Py-Feat e chama compute_identities (:1067). O Detectorv2 é outro modelo, multitarefa, com identidade arcface por padrão e opção None (feat/detector_v2.py:1-5,85), e tem crop_faces_from_boxes, que recorta nas caixas dadas sem rodar o RetinaFace (:211). Os pesos vêm de repositórios py-feat/* do HF, por hf_hub_download sem revision e com cache_dir dentro do pacote (feat/detector.py:180-432; feat/utils/io.py:44-46). Os arquivos skops são carregados com todos os tipos desconhecidos marcados como confiáveis (feat/pretrained.py:292-299,378-379,432-433). A 2.1.3 exige Python >= 3.11 e torch >= 2.5 (METADATA:16,26). Numa resolução seca com uv em 2026-09-23, os extras gpu e pyfeat em Python 3.11 resolveram py-feat 2.1.3; junto com o extra libreface, em Python 3.10, resolveram py-feat 0.6.1 e torch 2.0.0 (lock310.txt). A escolha da versão e do ambiente é do ADR de F2.4, e a fixação no lock das imagens de motor é de F2.1 (T2 e T3). O passo do CI procura só recognition, embedding, arcface e w600k no código de reacao/ (.github/workflows/ci.yml:17) e não detecta o identity_model padrão da biblioteca. F1.6 cria o teste da regra 2 em runtime. A imagem copia o código no build (Dockerfile:8-11) e é publicada a cada tag v* (.github/workflows/docker.yml:3-4), então o job de validação só roda o provider adaptado numa imagem publicada depois da mesclagem.

**Regras de negócio:**
- RN01 – Nenhum modelo de identidade do Py-Feat (facenet, arcface ou arcface_r50) é carregado nem baixado (CLAUDE.md, regra 2). A 0.6.2 não é usada, porque carrega o facenet ao construir o Detector.
- RN02 – As caixas de rosto vêm do SCRFD comum, e o Py-Feat mede só os rostos com altura de 64 px ou mais (reacao/providers/base.py:14-15; reacao/types.py:5). O caminho usado para passar as caixas na versão fixada, e o modelo que ele usa, ficam registrados na linha pyfeat do ADR 0001.
- RN03 – A versão do py-feat é fixada por F2.1 no lock das imagens de motor em versão exata, 0.6.1 ou 2.1.3, conforme o ADR de F2.4. Este PBI não altera o lock. O motivo da escolha é registrado na linha pyfeat do ADR 0001.
- RN04 – Os pesos são carregados por revisão fixa, com o SHA-256 conferido antes de qualquer carga, inclusive dos arquivos skops. A biblioteca lê só os arquivos conferidos, sem baixar nada durante a construção do detector.
- RN05 – O dispositivo de inferência é parâmetro.
- RN06 – As colunas de emoção e de pose são lidas pelo nome, ou pela ordem fixada num teste de contrato da versão instalada.
- RN07 – A validação roda em HF Job, pela imagem publicada em F4.2.T9, com --min-faces-plateia 0, sobre vídeo permitido por F1.3 com rostos de 64 px ou mais (clipes de F3.6, se o acionamento for o veto da PIB). Nunca roda sobre clipe de teste nem localmente com vídeo da PIB.
- RN08 – Só p_smile, expressiveness, yaw e pitch saem do provider.
- RN09 – Modelos que o provider não usa são desligados quando a API aceita (na 2.1.3, au_model=None e gaze_model=None). Os que a versão exige (na 0.6.1, rosto, landmarks, AU, emoção e pose) entram no hash e no inventário de licenças.
- RN10 – Na 0.6.1, as poses do img2pose são associadas às caixas do SCRFD pela regra registrada no ADR 0001, ou yaw e pitch ficam nulos no Py-Feat, com o motivo registrado.

**Fora de escopo:**
- Calibrar o limiar de sorriso do Py-Feat (F4.5)
- Rodar o bench do conjunto de teste (F4.6)
- Decidir a licença de uso no piloto (F4.3)
- Escolher entre 0.6.1 e 2.1.3 (ADR de F2.4) e fixar a versão no lock (F2.1)
- Usar o detector de rostos do próprio Py-Feat no lugar do SCRFD para medir a expressão
- Medida de olhos fechados

#### Critérios de aceite

- Um HF Job com o motor Py-Feat e --min-faces-plateia 0, pela imagem publicada em F4.2.T9 com o código deste PBI, sobre vídeo permitido por F1.3 com rostos de 64 px ou mais, termina com código de saída 0 e sem PersistenceViolation no log, e o digest fica anotado no PBI.
- O log desse job mostra, por vídeo, quantos rostos mensuráveis receberam p_smile e quantos receberam yaw e pitch. O número com p_smile é maior que zero.
- O teste da regra 2 de F1.6, estendido ao Py-Feat, passa com a configuração do provider e confirma que o detector construído não tem modelo de identidade carregado.
- (erro) O teste da regra 2 falha quando a configuração do provider pede modelo de identidade, e a falha acontece antes de construir o detector, sem baixar nem carregar o modelo.
- (erro) Ao fim do job, nenhum arquivo de peso de identidade (facenet, arcface ou arcface_r50) existe no ambiente do job.
- (erro) Com um peso cujo SHA-256 difere do fixado, o job falha antes do primeiro quadro e antes de carregar qualquer arquivo de peso ou skops, com mensagem que nomeia o arquivo.
- (erro) Um teste mostra que nenhum download ocorre durante a construção do detector: a biblioteca lê só os arquivos conferidos.
- O log do job registra a versão do py-feat, o dispositivo usado e, para cada peso, a origem, a revisão e o SHA-256.
- (erro) O teste de contrato falha se o nome ou a ordem das colunas happiness, neutral, pitch e yaw mudar na versão instalada.
- O lock de F2.1 fixa o py-feat em versão exata diferente de 0.6.2, e a linha pyfeat do ADR 0001 registra a versão, o motivo, o caminho usado para passar as caixas do SCRFD, o modelo que esse caminho usa e a origem da pose, ou a ausência dela.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F4.2.T1 | Machine Learning | Conferir na versão do py-feat fixada por F2.1 a API usada pelo provider e registrá-la na linha pyfeat do ADR 0001 | 3 | F2.1.T3, F2.4 |
| F4.2.T2 | Machine Learning | Reescrever o provider Py-Feat para a versão fixada, sem modelo de identidade, com as caixas do SCRFD e dispositivo configurável | 8 | F4.2.T1, F4.2.T3 |
| F4.2.T3 | Visão Computacional | Conferir na versão fixada do Py-Feat o formato de caixa, a pose e os modelos que o construtor carrega | 5 | F4.2.T1 |
| F4.2.T4 | Governança e Privacidade | Definir por versão a lista de modelos de identidade proibidos do Py-Feat e revisar a verificação da regra 2 | 3 | F4.2.T1 |
| F4.2.T5 | MLOps | Carregar os pesos do Py-Feat por revisão fixa, com SHA-256 conferido antes de qualquer carga e sem download durante a construção | 10 | F2.3, F4.3, F4.2.T1, F4.2.T3 |
| F4.2.T6 | DevOps | Criar o job de CI do Py-Feat com o Python e o torch da versão fixada e a leitura dos pesos com hash | 6 | F1.6, F2.6, F4.2.T1, F4.2.T5 |
| F4.2.T7 | QA | Estender o teste da regra 2 e escrever os testes de contrato e da guarda do Py-Feat | 6 | F1.6, F4.2.T2, F4.2.T4, F4.2.T6 |
| F4.2.T8 | QA | Executar no HF o job de validação do Py-Feat e conferir os critérios de aceite | 4 | F4.2.T2, F4.2.T3, F4.2.T5, F4.2.T7, F4.2.T9, F1.1, F1.3, F2.4, F3.1, F3.6 (só se o acionamento for o veto da PIB), Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F4.2.T9 | DevOps | Publicar por tag de pré-release a imagem com o provider Py-Feat adaptado e registrar o digest | 2 | F2.2, F4.2.T5, F4.2.T7 |

<details><summary>F4.2.T1 · [Machine Learning] Conferir na versão do py-feat fixada por F2.1 a API usada pelo provider e registrá-la na linha pyfeat do ADR 0001</summary>

**Objetivo:** A linha pyfeat do ADR 0001 registra a versão fixada no lock de F2.1, o motivo trazido do ADR de F2.4 e os métodos que a versão oferece para receber caixas externas.

**Passos previstos:**
1. Conferir no lock de F2.1 que o py-feat está em versão exata, diferente de 0.6.2, e igual à decidida no ADR de F2.4. Se não estiver, devolver a F2.1 com o ponto a corrigir, sem alterar o lock.
2. Conferir na versão fixada os métodos públicos que recebem caixas externas (detect_landmarks e detect_emotions na 0.6.1; crop_faces_from_boxes no Detectorv2 da 2.1.3; nenhum no Detectorv1).
3. Registrar na linha pyfeat do ADR 0001 a versão, o motivo trazido do ADR de F2.4 e o resultado da conferência da API.

**Definição de pronto:** O PR que altera a linha pyfeat do ADR 0001 registra a versão fixada no lock de F2.1, o motivo e os métodos conferidos, e cita F4.2.

**Dependências:** F2.1.T3, F2.4

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F4.2.T2 · [Machine Learning] Reescrever o provider Py-Feat para a versão fixada, sem modelo de identidade, com as caixas do SCRFD e dispositivo configurável</summary>

**Objetivo:** O provider roda na versão fixada, recusa configuração com identidade antes de construir o detector, passa as caixas do SCRFD pelo caminho registrado e lê as colunas pelo nome ou pela ordem testada.

**Passos previstos:**
1. Validar a configuração do provider antes de construir o detector e recusar qualquer modelo de identidade.
2. Criar o detector da versão fixada sem modelo de identidade (sem o parâmetro na 0.6.1; identity_model=None na 2.1.3) e, na 2.1.3, com au_model=None e gaze_model=None.
3. Passar as caixas do SCRFD pelo caminho conferido em F4.2.T1 e F4.2.T3 e aplicar a regra de pose de F4.2.T3.
4. Receber o dispositivo por parâmetro.
5. Ler happiness, neutral, pitch e yaw pelo nome da coluna quando a API permitir.
6. Expor as contagens agregadas de rostos com p_smile e com pose e imprimi-las no log por vídeo.
7. Não escrever o termo arcface em reacao/, para não disparar o passo do CI (.github/workflows/ci.yml:17).
8. Trocar na docstring de reacao/providers/pyfeat.py:1 a referência PBI-000D por F4.2.

**Definição de pronto:** Testes unitários com saída simulada da versão fixada passam, inclusive o que recusa configuração com identidade antes de construir o detector. ruff check e pytest passam. O PR cita F4.2 e PBI-000D. Uma busca por PBI-000D em reacao/providers/pyfeat.py não encontra resultado.

**Dependências:** F4.2.T1, F4.2.T3

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F4.2.T3 · [Visão Computacional] Conferir na versão fixada do Py-Feat o formato de caixa, a pose e os modelos que o construtor carrega</summary>

**Objetivo:** O formato de caixa, a origem, a unidade e a associação da pose e a lista de modelos carregados na versão fixada ficam registrados antes da reescrita do provider.

**Passos previstos:**
1. Conferir o formato de caixa esperado pelo caminho de F4.2.T1 (hoje x1, y1, x2, y2 e confiança, em pyfeat.py:21).
2. Conferir o modelo de pose da versão fixada e em que unidade e ordem ele devolve pitch, roll e yaw.
3. Na 0.6.1, onde detect_facepose com img2pose ignora as caixas e devolve faces e poses (feat/detector.py:467-500), definir a regra de associação das poses às caixas do SCRFD ou registrar que yaw e pitch ficam nulos no Py-Feat.
4. Listar todo modelo que o construtor carrega com a configuração do provider, inclusive os obrigatórios sem uso (na 0.6.1, rosto, landmarks, AU, emoção e pose), e entregar a lista a F4.2.T5 e a F4.3.

**Definição de pronto:** Uma nota no PR registra o formato de caixa, a unidade, a ordem e a associação da pose e a lista dos modelos carregados, e a lista foi entregue a F4.2.T5 e a F4.3.

**Dependências:** F4.2.T1

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F4.2.T4 · [Governança e Privacidade] Definir por versão a lista de modelos de identidade proibidos do Py-Feat e revisar a verificação da regra 2</summary>

**Objetivo:** O teste da regra 2 cobre todos os modelos de identidade que a versão fixada oferece.

**Passos previstos:**
1. Registrar por versão os modelos de identidade: nenhum na 0.6.1 (feat/detector.py:48-60); facenet obrigatório na 0.6.2, fora das opções; arcface, facenet e arcface_r50 no Detectorv1 da 2.1.3 (feat/detector.py:120,393-432) e arcface e facenet no Detectorv2 (feat/detector_v2.py:43-47,85).
2. Registrar a lista em tests/ e a forma de verificar em runtime que nenhum desses modelos foi carregado nem baixado.
3. Revisar o PR de F4.2.T2 contra as regras 2 e 6 do CLAUDE.md.

**Definição de pronto:** A lista está no teste, e o PR de F4.2.T2 tem a aprovação da revisão de governança.

**Dependências:** F4.2.T1

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F4.2.T5 · [MLOps] Carregar os pesos do Py-Feat por revisão fixa, com SHA-256 conferido antes de qualquer carga e sem download durante a construção</summary>

**Objetivo:** Nenhum peso do Py-Feat, inclusive arquivos skops e modelos obrigatórios sem uso, é carregado sem revisão fixa e hash conferido, e a biblioteca não baixa nada ao construir o detector.

**Passos previstos:**
1. Receber de F4.2.T3 a lista dos modelos que o construtor carrega.
2. Conforme F4.3, espelhar os pesos no repositório de modelo privado de F2.3, ou fixar o commit de cada repositório py-feat/* (2.1.3) ou a URL de cada release do GitHub (0.6.1) e o SHA-256 dos arquivos.
3. Baixar para um diretório fora do diretório de trabalho e conferir o hash antes de chamar a biblioteca.
4. Fazer a biblioteca ler os arquivos conferidos: na 0.6.1, pré-preencher feat/resources, onde download_url grava (feat/utils/io.py:33-35,71-80); na 2.1.3, pré-preencher o cache usado por hf_hub_download e rodar com HF_HUB_OFFLINE. Registrar o mecanismo no PR.
5. Escrever o teste que mostra que nenhum download ocorre durante a construção do detector.
6. Fazer o job falhar com mensagem que nomeia o arquivo quando o hash diferir, e registrar a origem, a revisão e o hash no log e na linhagem.

**Definição de pronto:** Com um arquivo de peso ou skops adulterado, o job falha antes da carga. O teste sem download passa. Com os pesos corretos, o log mostra origem, revisão e hash.

**Dependências:** F2.3, F4.3, F4.2.T1, F4.2.T3

**Estimativa sugerida:** 10 h (sugestão; validar com o time)

</details>

<details><summary>F4.2.T6 · [DevOps] Criar o job de CI do Py-Feat com o Python e o torch da versão fixada e a leitura dos pesos com hash</summary>

**Objetivo:** Existe um job de CI que instala o extra pyfeat na versão fixada e obtém os pesos com hash, onde os testes de F4.2.T7 rodam.

**Passos previstos:**
1. Criar um job de CI separado que instala o extra pyfeat com o lock de F2.1 e o Python e o torch exigidos pela versão fixada.
2. Dar ao job leitura dos pesos do Py-Feat por revisão fixa com hash, com o token somente leitura de F2.6 passado só pelo nome.
3. Criar no job um teste de fumaça que importa o py-feat e confere o hash dos pesos.
4. Configurar o job onde a pendência da Feature decidir: GitHub Actions, pela exceção P26, ou HF Job cpu-basic.

**Definição de pronto:** O job instala o extra pyfeat, o teste de fumaça passa com os pesos corretos e o job falha quando um peso com hash errado é oferecido.

**Dependências:** F1.6, F2.6, F4.2.T1, F4.2.T5

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F4.2.T7 · [QA] Estender o teste da regra 2 e escrever os testes de contrato e da guarda do Py-Feat</summary>

**Objetivo:** O CI falha se o Py-Feat carregar ou baixar modelo de identidade, se as colunas mudarem na versão instalada ou se a biblioteca gravar imagem fora de /dev/shm.

**Passos previstos:**
1. Estender o teste da regra 2 de F1.6 com a lista de F4.2.T4 e confirmar que o detector construído não tem modelo de identidade carregado.
2. Escrever o teste negativo que passa ao provider uma configuração com modelo de identidade e espera a falha antes da construção do detector, sem baixar nem carregar o modelo.
3. Escrever o teste de contrato do nome e da ordem de happiness, neutral, pitch e yaw na versão instalada.
4. Rodar o provider dentro de no_persistence com o vídeo de F1.6 e confirmar que a biblioteca não grava arquivo.
5. Verificar ao fim dos testes que nenhum arquivo de peso de identidade existe no ambiente.
6. Incluir os testes no job de CI de F4.2.T6.

**Definição de pronto:** Os testes passam no job de CI com a configuração do provider e falham nos casos negativos. ruff check e pytest passam.

**Dependências:** F1.6, F4.2.T2, F4.2.T4, F4.2.T6

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F4.2.T8 · [QA] Executar no HF o job de validação do Py-Feat e conferir os critérios de aceite</summary>

**Objetivo:** Os critérios de F4.2 ficam verificados com JOB_ID e digest anotados no PBI.

**Passos previstos:**
1. Pedir ao dono aprovação do job, com flavor, duração e custo previstos (P7).
2. Lançar pelo script de F1.1, pela imagem com o digest registrado em F4.2.T9, no modo do ADR de F2.4, com o motor pyfeat, --no-transcribe, --stdout e --min-faces-plateia 0, sobre vídeo permitido por F1.3 com rostos de 64 px ou mais (clipes de F3.6, se o acionamento for o veto da PIB).
3. Conferir o código de saída, a ausência de PersistenceViolation, as contagens por vídeo e o log de versão, dispositivo e pesos.
4. Listar os arquivos de peso no ambiente do job e confirmar que não há modelo de identidade.
5. Repetir com um peso de hash errado e conferir a falha antes da carga.
6. Conferir o lock de F2.1 e a linha pyfeat do ADR 0001 e, no resultado do CI, os testes de F4.2.T5 e F4.2.T7.
7. Anotar no PBI os JOB_ID, o digest e o resultado de cada critério.

**Definição de pronto:** Os dez critérios de aceite estão marcados como passou ou não passou, com JOB_ID, digest e trecho de log anotados no PBI.

**Dependências:** F4.2.T2, F4.2.T3, F4.2.T5, F4.2.T7, F4.2.T9, F1.1, F1.3, F2.4, F3.1, F3.6 (só se o acionamento for o veto da PIB), Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.2.T9 · [DevOps] Publicar por tag de pré-release a imagem com o provider Py-Feat adaptado e registrar o digest</summary>

**Objetivo:** O job de validação de F4.2.T8 tem uma imagem com digest que contém o código de F4.2.T2 e T5.

**Passos previstos:**
1. Conferir que os PRs de F4.2.T2 e T5 estão mesclados em main e que os testes de F4.2.T7 passam no job de CI de F4.2.T6.
2. Criar a tag de pré-release no commit de main que contém esses PRs, pelo processo de publicação de F2.2 e na composição de imagem do ADR de F2.4 (imagem única ou imagem do Py-Feat).
3. Conferir no log do build que a imagem foi construída com o lock de F2.1.
4. Registrar no PBI a tag, o commit e o digest publicado.

**Definição de pronto:** O PBI tem a tag, o commit e o digest, e o workflow de publicação desse commit terminou com sucesso.

**Dependências:** F2.2, F4.2.T5, F4.2.T7

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- reacao/providers/pyfeat.py:1,12-31
- reacao/providers/base.py:14-15
- pyproject.toml:21
- .github/workflows/ci.yml:17
- Dockerfile:8-11
- .github/workflows/docker.yml:3-4,19-25
- py_feat-0.6.1 (wheel baixada do PyPI para scratchpad/pf061): feat/detector.py:48-60,395,467-500,590; feat/pretrained.py:41-43,111,125,139,183,208; feat/resources/model_list.json; feat/utils/io.py:33-35,71-80; METADATA:8
- py_feat-0.6.2 (wheel no scratchpad): feat/detector.py:51-63,122,322-329; feat/pretrained.py:230-241,253-256; feat/resources/model_list.json:139-142
- py_feat-2.1.3 (wheel no scratchpad): feat/__init__.py:50-51; feat/detector.py:111-131,180-432,464-466,486,636,906,1067; feat/detector_v2.py:1-5,43-47,85,211; feat/pretrained.py:292-299,378-379,432-433; feat/utils/io.py:44-46; METADATA:8,16,26
- https://pypi.org/pypi/py-feat/json
- Resolução seca com 'uv pip compile' em 2026-09-23 (extras gpu e pyfeat em Python 3.11; gpu, pyfeat e libreface em Python 3.10; lock310.txt)
- CLAUDE.md, regra 2

#### Verificação INVEST: pontos que falharam
- Independente: depende de F1.1, F1.3, F1.6, F2.1, F2.2, F2.3, F2.4, F2.6, F3.1, F4.3 e, se acionado, F3.6.
- Small: 8 pontos e nove tasks, no limite de uma sprint.
- Valiosa: o benefício é para o time e para o gate; o usuário do produto não vê este PBI isolado.

#### Premissas
- Disciplinas da árvore mantidas: Machine Learning, Visão Computacional, Governança e Privacidade, MLOps e QA. DevOps entrou pelas tasks F4.2.T6, que cria o job de CI do Py-Feat com o Python e o torch da versão escolhida e a leitura dos pesos com hash, e F4.2.T9, que publica a imagem com o código deste PBI antes do job de validação.
- F1.1, F1.3 e F2.4 entraram porque, pela P3 revisada, a validação é um HF Job lançado sem caminho local (P27), no modo do ADR de F2.4, sobre um vídeo permitido por F1.3. F2.1 entra pelo lock que T1 confere, F2.6 pela task T6 e F2.2 pela task T9.
- A lista de modelos de identidade proibidos fica em tests/, e não em reacao/, porque o passo do CI rejeita o termo arcface em reacao/ (.github/workflows/ci.yml:17).
- O ADR de F2.4 é o dono único da escolha entre 0.6.1 e 2.1.3, e F2.1 (T2 e T3) fixa a versão no lock das imagens de motor. F4.2.T1 só confere a API na versão fixada; se o lock não trouxer a versão decidida, a correção volta a F2.1.
- É dedução que, com a 2.1.3, receber as caixas do SCRFD pelo Detectorv2 muda o modelo medido (multitarefa) em relação ao Detectorv1. A linha pyfeat do ADR 0001 registra qual modelo foi medido.
- É dedução que, na 0.6.1, as poses do img2pose só podem ser ligadas às caixas do SCRFD pela posição das caixas que o img2pose devolve (feat/detector.py:467-500). F4.2.T3 registra a regra ou a ausência de pose.
- Onde o job de CI de T6 roda (GitHub Actions pela exceção P26 ou HF Job cpu-basic) segue a pendência da Feature, respondida antes da sprint.
- Revisão não aplicada em parte: F4.2.T2, desligar au_model e gaze_model — vale só para a 2.1.3; na 0.6.1 os cinco modelos são obrigatórios (feat/pretrained.py:111,125,139,183,208) e entram no hash e no inventário.
- Story points e horas são sugestão, a validar no refinamento.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável, Story Points (sugestão: 8) e vínculo Parent com a Feature F4.
- F2.4: insumos para a escolha entre py-feat==0.6.1 (imagem única com libreface) e 2.1.3 com identity_model=None (imagem por motor), com a 0.6.2 excluída pela regra 2 (ver pendência da Feature).
- F2.1 (T2 e T3): fixar no lock das imagens de motor a versão exata escolhida do py-feat, diferente de 0.6.2, e o ambiente que ela exige (Python >= 3.11 e torch >= 2.5 na 2.1.3). F2.2: publicação por tag de pré-release com registro do digest, usada por F4.2.T9.
- F1.6: extensão do teste da regra 2 ao Py-Feat e job de CI por motor.
- F2.3: lista das origens a fixar ou espelhar, conforme F4.3 (releases do GitHub cosanlab/py-feat e cosanlab/feat na 0.6.1; repositórios py-feat/* do HF na 2.1.3), com os modelos obrigatórios sem uso.
- F2.6: token somente leitura dos repositórios de modelo para o job de CI de F4.2.T6.
- Usuário: confirmação da exceção P26 diante da P3 revisada, que define onde roda o job de F4.2.T6.

## Preview — PBI F4.3 (novo) · Verificar as licenças de todo modelo carregado na execução (detector, motores, modelos embutidos e Whisper) e registrá-las no ADR 0001

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Verificar as licenças de todo modelo carregado na execução (detector, motores, modelos embutidos e Whisper) e registrá-las no ADR 0001 |
| Tipo | Product Backlog Item |
| Pai | F4 |
| Tags | F4; licencas; governanca; adr-0001; documental |
| Estimativa | 3 pts (sugestão); tasks: 22 h |
| Dependências | nenhuma |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro, dono do repositório e responsável pela decisão do gate  
Quero saber, com a fonte, sob que licença estão o código e os pesos de todo modelo carregado na execução, baixado ou embutido em pacote, e se o uso no PoC, o espelhamento privado e o uso no piloto cabem nelas  
Para que F2.3 saiba o que pode espelhar, que a comparação de F4.6 inclua só motores utilizáveis e que F4.7 seja acionado se o detector não puder ir ao piloto

**Contexto:** Na tabela do ADR 0001, a coluna licença diz 'Apache-2.0 (verificar modelo)' para hsemotion, 'verificar' para libreface e 'MIT (modelos internos: verificar)' para pyfeat (docs/adr/0001-motor.md:10-12). O detector comum é o SCRFD do pacote buffalo_sc do insightface (reacao/detect.py:14; docs/adr/0001-motor.md:6). O código do insightface é MIT, e os modelos pré-treinados servem só para pesquisa não comercial (insightface-2.0.dist-info/METADATA:52-54). O libreface 0.2.0 declara 'USC Research Licence' e remete ao texto no GitHub (METADATA:8,315). Os pesos dele vêm do Google Drive (libreface/utils.py:16), e os modelos de AU são configurados com DISFA e BP4D (AU_Recognition/inference.py:58-60). Para alinhar o rosto e calcular a pose, o LibreFace usa o FaceMesh do MediaPipe, que vem dentro do pacote mediapipe==0.10.5, sem download separado (detect_mediapipe_image.py:136,195-199; METADATA:43). O código do hsemotion-onnx é Apache-2.0 (METADATA:9), e o peso vem do repositório HSE-asavchenko/face-emotion-recognition, na pasta affectnet_emotions (hsemotion_onnx/facial_emotions.py:21). O código do sixdrepnet é MIT, e o peso 6DRepNet_300W_LP_AFLW2000.pth vem de cloud.ovgu.de (sixdrepnet/regressor.py:35). O código do py-feat é MIT (METADATA:8 da 0.6.1, da 0.6.2 e da 2.1.3). Na 0.6.1 os pesos vêm de releases do GitHub cosanlab/py-feat e cosanlab/feat (feat/resources/model_list.json), e os cinco modelos (rosto, landmarks, AU, emoção e pose) são carregados mesmo sem uso (feat/pretrained.py:111,125,139,183,208). Na 2.1.3 os pesos vêm de repositórios py-feat/* do HF (feat/detector.py:180-432). A transcrição usa o faster-whisper medium e cai para o small em CPU (reacao/transcribe.py:6,10-12), com vad_filter=True (reacao/transcribe.py:13); o pacote faster-whisper traz o modelo Silero VAD embutido (faster_whisper/assets/silero_vad_v6.onnx no .venv). F2.3 espelha o faster-whisper medium 'conforme as licenças registradas em F4.3'. O repositório não registra se o piloto se enquadra como pesquisa não comercial.

**Regras de negócio:**
- RN01 – Cada licença registrada tem fonte (URL ou arquivo do pacote) e data da consulta.
- RN02 – A licença do código e a licença dos pesos são registradas separadamente.
- RN03 – A decisão é registrada para três usos: PoC da Fase 0 no HF Jobs, espelhamento em repositório de modelo privado e uso no piloto da Fase 1.
- RN04 – Se a licença vetar o SCRFD no piloto, F4.7 é acionado. Se vetar um motor, ele sai da comparação de F4.6.
- RN05 – Peso cuja licença não foi localizada fica registrado como 'licença não localizada', e o uso dele segue a decisão da governança registrada no ADR.
- RN06 – Fabio Pinheiro revisa o registro, e o encarregado de dados também revisa quando for nomeado.
- RN07 – O inventário cobre todo modelo carregado durante a execução, baixado ou embutido em pacote.
- RN08 – Enquanto Fabio Pinheiro não decidir se o piloto é pesquisa não comercial, a coluna do piloto diz 'pendente de decisão de Fabio Pinheiro', e F4.7 fica em espera quanto ao gatilho de licença.

**Fora de escopo:**
- Negociar licença comercial com a USC ou com o insightface
- Parecer jurídico formal (a análise de base legal do corpus é de F3.1 e o RIPD é de F6.3)
- Decidir se o piloto é pesquisa não comercial (decisão de Fabio Pinheiro, condição de Ready)
- Espelhar os pesos (F2.3)
- Implementar a troca do detector (F4.7)

#### Critérios de aceite

- A tabela de licenças do ADR 0001 tem uma linha para cada modelo carregado durante a execução, baixado ou embutido em pacote: SCRFD (det_500m.onnx), HSEmotion (enet_b0_8_best_afew), 6DRepNet, os modelos de AU, expressão e olhar do LibreFace 0.2.0, o FaceMesh do mediapipe 0.10.5, os modelos que o construtor do Py-Feat carrega com a configuração do provider nas versões 0.6.1 e 2.1.3 (inclusive os obrigatórios sem uso), o faster-whisper (medium e small) e o Silero VAD do faster-whisper.
- Cada linha tem a licença do código, a licença dos pesos, a fonte e a data da consulta.
- Cada linha tem a decisão para os três usos: PoC, espelhamento privado e piloto. Enquanto a decisão sobre o enquadramento do piloto não vier, a coluna do piloto diz 'pendente de decisão de Fabio Pinheiro'.
- O ADR 0001 diz se F4.7 é acionado pela licença do SCRFD, não acionado ou em espera pela decisão sobre o piloto.
- (erro) Motor cujo uso no piloto é vetado aparece como retirado da comparação, com a cláusula citada.
- (erro) Peso sem licença localizada aparece como 'licença não localizada', com a decisão de uso registrada.
- O PR que altera o ADR 0001 tem a aprovação de Fabio Pinheiro.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F4.3.T1 | Machine Learning | Listar todo modelo que o detector, os motores e a transcrição carregam, baixado ou embutido em pacote, com a origem | 5 | — |
| F4.3.T2 | Governança e Privacidade | Levantar a licença do código, dos pesos e dos dados de treino declarados de cada item, com fonte e data | 8 | F4.3.T1 |
| F4.3.T3 | Governança e Privacidade | Registrar no ADR 0001 a decisão de uso no PoC, no espelhamento e no piloto para cada item | 4 | F4.3.T2 |
| F4.3.T4 | Governança e Privacidade | Revisar o registro de licenças do ADR 0001 (revisor: Fabio Pinheiro) | 2 | F4.3.T3 |
| F4.3.T5 | QA | Verificar os critérios de aceite do registro de licenças contra as fontes | 3 | F4.3.T4 |

<details><summary>F4.3.T1 · [Machine Learning] Listar todo modelo que o detector, os motores e a transcrição carregam, baixado ou embutido em pacote, com a origem</summary>

**Objetivo:** Existe o inventário de modelos por componente, com a origem e a forma de obtenção.

**Passos previstos:**
1. Listar os pesos do buffalo_sc que o pipeline usa (det_500m.onnx) e os que o instalador baixa (w600k_mbf.onnx).
2. Listar o peso do HSEmotion (enet_b0_8_best_afew.onnx) e o do 6DRepNet, com as URLs de origem do código.
3. Listar os modelos que a 0.2.0 do LibreFace pode carregar na função usada pelo provider (AU, expressão e olhar, com o weights_download_id de cada solver) e o FaceMesh embutido no mediapipe 0.10.5.
4. Listar, nas versões 0.6.1 e 2.1.3 do py-feat, os modelos que o construtor carrega com a configuração do provider, inclusive os obrigatórios sem uso, com a origem (releases do GitHub cosanlab/py-feat e cosanlab/feat na 0.6.1; repositórios py-feat/* do HF na 2.1.3).
5. Listar os modelos faster-whisper medium e small, com a origem, e o Silero VAD embutido no pacote faster-whisper.
6. Entregar o inventário a F4.3.T2 e a F2.3.

**Definição de pronto:** O inventário, com arquivo, componente, origem e forma de obtenção (baixado ou embutido) em cada linha, está no PR do ADR 0001.

**Dependências:** nenhuma

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F4.3.T2 · [Governança e Privacidade] Levantar a licença do código, dos pesos e dos dados de treino declarados de cada item, com fonte e data</summary>

**Objetivo:** Cada item do inventário tem a licença do código e a dos pesos, com URL e data da consulta.

**Passos previstos:**
1. Para cada item de F4.3.T1, localizar a licença do código (PyPI e repositório) e a dos pesos (model card, README ou arquivo de licença).
2. Quando o peso declarar dados de treino, anotar a licença desses dados e se ela restringe o uso dos pesos.
3. Ler o texto da USC Research Licence no endereço indicado no METADATA do libreface.
4. Localizar a licença do modelo FaceMesh do mediapipe e a do Silero VAD.
5. Marcar como 'licença não localizada' o que não tiver texto encontrado.
6. Registrar URL e data em cada linha.

**Definição de pronto:** A tabela de licenças no PR do ADR 0001 tem código, pesos, fonte e data em todas as linhas.

**Dependências:** F4.3.T1

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F4.3.T3 · [Governança e Privacidade] Registrar no ADR 0001 a decisão de uso no PoC, no espelhamento e no piloto para cada item</summary>

**Objetivo:** Cada item tem a decisão para os três usos, ou 'pendente de decisão de Fabio Pinheiro' na coluna do piloto, e as consequências para F2.3, F4.6 e F4.7.

**Passos previstos:**
1. Registrar a resposta de Fabio Pinheiro sobre o enquadramento do piloto como pesquisa não comercial, obtida antes da sprint, ou 'pendente de decisão de Fabio Pinheiro' na coluna do piloto.
2. Registrar a decisão de cada item para o PoC, o espelhamento privado e o piloto, citando a cláusula.
3. Marcar os motores retirados da comparação e o estado de F4.7: acionado, não acionado ou em espera pela decisão sobre o piloto.
4. Registrar a decisão sobre os itens com 'licença não localizada'.

**Definição de pronto:** O ADR 0001 tem a decisão dos três usos em todas as linhas, com 'pendente de decisão de Fabio Pinheiro' onde couber, e diz o estado de F4.7.

**Dependências:** F4.3.T2

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.3.T4 · [Governança e Privacidade] Revisar o registro de licenças do ADR 0001 (revisor: Fabio Pinheiro)</summary>

**Objetivo:** O registro de licenças tem a aprovação de Fabio Pinheiro antes da verificação da QA.

**Passos previstos:**
1. Conferir cada critério de aceite de F4.3 contra o ADR.
2. Abrir as fontes citadas por amostragem e conferir a cláusula.
3. Aprovar o PR ou devolvê-lo com os pontos a corrigir.
4. Se o encarregado de dados já estiver nomeado, pedir também a revisão dele.

**Definição de pronto:** O PR do ADR 0001 tem a aprovação de Fabio Pinheiro.

**Dependências:** F4.3.T3

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F4.3.T5 · [QA] Verificar os critérios de aceite do registro de licenças contra as fontes</summary>

**Objetivo:** Os sete critérios de F4.3 ficam verificados contra as fontes citadas e anotados no PBI.

**Passos previstos:**
1. Conferir que a tabela tem uma linha para cada item do inventário de F4.3.T1, inclusive FaceMesh, faster-whisper medium e small e Silero VAD.
2. Abrir a fonte de cada linha e conferir a licença do código, a dos pesos e a data da consulta.
3. Conferir em cada linha a decisão dos três usos, com 'pendente de decisão de Fabio Pinheiro' onde a decisão sobre o piloto não veio.
4. Conferir o estado de F4.7, os motores retirados com a cláusula citada e os itens com 'licença não localizada' com a decisão de uso.
5. Conferir a aprovação de Fabio Pinheiro no PR.
6. Anotar no PBI o resultado de cada critério.

**Definição de pronto:** Os sete critérios estão marcados como passou ou não passou, com a fonte conferida anotada no PBI.

**Dependências:** F4.3.T4

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- docs/adr/0001-motor.md:3-6,10-12
- reacao/detect.py:14
- reacao/transcribe.py:6,10-13
- .venv/.../insightface-2.0.dist-info/METADATA:52-54
- libreface-0.2.0 (wheel no scratchpad): METADATA:8,43,315; utils.py:11-16; AU_Recognition/inference.py:58-60; detect_mediapipe_image.py:136,195-199
- .venv/.../hsemotion_onnx-0.3.1.dist-info/METADATA:9; hsemotion_onnx/facial_emotions.py:21
- .venv/.../sixdrepnet-0.1.6.dist-info/METADATA (License: MIT); sixdrepnet/regressor.py:35
- .venv/lib/python3.11/site-packages/faster_whisper/assets/silero_vad_v6.onnx
- py_feat 0.6.1 (scratchpad/pf061): METADATA:8; feat/resources/model_list.json; feat/pretrained.py:111,125,139,183,208
- py_feat 0.6.2 e 2.1.3 (wheels no scratchpad): METADATA:8; feat/detector.py:180-432 (2.1.3)
- https://pypi.org/pypi/insightface/json; https://pypi.org/pypi/libreface/json; https://pypi.org/pypi/hsemotion-onnx/json; https://pypi.org/pypi/sixdrepnet/json
- Texto de F2.3 na árvore (espelha o faster-whisper medium 'conforme as licenças registradas em F4.3')
- Revisão 3: padrão de task de QA nos PBIs de documento da árvore (F1.3.T6, F2.4.T6, F6.6.T4)

#### Verificação INVEST: pontos que falharam
- Valiosa: o benefício é indireto (destrava F2.3, F4.6 e F4.7).
- Testável: verificado pela revisão de Fabio Pinheiro (T4) e pela conferência da QA contra as fontes (T5), sem teste automatizado.
- Independente: a coluna do piloto depende de decisão de Fabio Pinheiro, tratada como condição de Ready.

#### Premissas
- Este PBI é documental. A aprovação é de Fabio Pinheiro (e do encarregado de dados quando for nomeado), em F4.3.T4, e a verificação dos critérios contra as fontes é da task de QA F4.3.T5, acrescentada na revisão 3.
- Disciplinas: Governança e Privacidade e Machine Learning vêm da árvore. QA entrou pela task F4.3.T5, que verifica os critérios de aceite contra as fontes, seguindo o padrão dos PBIs de documento da árvore citado na revisão 3 (F1.3.T6, F2.4.T6, F6.6.T4) e porque F4.3 condiciona F1.6, F2.3 e F4.7.
- O Whisper entrou por coerência com F2.3, que depende desta decisão para espelhar o faster-whisper. O FaceMesh e o Silero VAD entraram porque rodam na execução sem download separado.
- As licenças do modelo FaceMesh e do Silero VAD não foram levantadas; F4.3.T2 as levanta.
- Os dados de treino citados (AffectNet, 300W_LP, AFLW2000, DISFA, BP4D) vêm dos nomes de caminhos e arquivos e da configuração dos pacotes. Se as licenças desses dados restringem os pesos, T2 verifica.
- A decisão sobre o enquadramento do piloto como pesquisa não comercial fica fora das tasks: é condição de Ready, com dono Fabio Pinheiro. T3 só registra a resposta ou o valor 'pendente'.
- O encarregado de dados ainda não tem nome (dependência do épico).
- Story points e horas são sugestão, a validar no refinamento. Com a task de QA, o PBI soma 22 h e continua com 3 pontos.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável, Story Points (sugestão: 3) e vínculo Parent com a Feature F4.
- F2.3: lista de pesos que podem ser espelhados e dos que serão baixados da origem com hash, inclusive faster-whisper e Silero VAD.
- F4.7: decisão de acionamento pela licença do SCRFD, ou estado de espera.
- Fabio Pinheiro: decidir, antes da sprint, se o piloto da Fase 1 se enquadra como pesquisa não comercial (condição de Ready).
- Encarregado de dados: nomear para revisar a decisão de uso no piloto.

## Preview — PBI F4.4 (novo) · Medir e corrigir nos clipes de desenvolvimento o descarte do pré-filtro de plateia e da detecção em rostos pequenos

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Medir e corrigir nos clipes de desenvolvimento o descarte do pré-filtro de plateia e da detecção em rostos pequenos |
| Tipo | Product Backlog Item |
| Pai | F4 |
| Tags | F4; pre-filtro; detector; visao-computacional; clipes-dev; PBI-104; PBI-000D |
| Estimativa | 8 pts (sugestão); tasks: 33 h |
| Dependências | F1.1 – script de lançamento que recusa caminho local, F2.2 – processo de publicação da imagem por tag com digest, usado por T8 e T9 (acrescentada na revisão 3), F2.3.T3 – mecanismo de pesos por revisão fixa e hash, que entram na linhagem (no lugar do PBI F2.3 inteiro, revisão 4), F2.8 – repositório de resultados com linhagem, exigido para números no ADR 0001 (no lugar de F2.5, revisão 3), F3.4 – rótulos dos clipes 07 a 10 com tag, F3.7 – rótulos públicos de desenvolvimento (F3.7.T4, publicados com tag em F3.7.T8), se o acionamento for o veto da PIB (acrescentada na revisão 3) |
| Substitui | PBI-104, PBI-000D |

#### Descrição

Como integrante do time de visão computacional  
Quero saber quantos quadros de plateia o pré-filtro descarta e quantos rostos de 64 px ou mais o detector perde nos clipes 07 a 10, e corrigir o piso do pré-filtro  
Para que o critério 1 seja medido com um pré-filtro que não descarte a condição da PIB (rostos de 34 a 96 px) e que a decisão sobre ladrilhos ou outro detector saia de um número registrado

**Contexto:** O pré-filtro reduz o quadro a 640 px de largura (reacao/ingest.py:45-49) e roda o detector com det_size 640 (processar_culto.py:73). O piso de 24 px (reacao/types.py:6; reacao/detect.py:34) vale no quadro reduzido, e a cena só conta como plateia com pelo menos 5 rostos (processar_culto.py:41,74). O bench repete o mesmo laço (bench.py:102-120). Os clipes da PIB têm 1920x1080 (samples/corpus/pib/ffprobe.csv; README.md:7-8), então o piso equivale a cerca de 72 px no quadro original, e os rostos de 34 a 96 px (docs/adr/0001-motor.md:4) ficam entre 11 e 32 px no quadro reduzido. A passada plena usa det_size 1280 (reacao/detect.py:9,27). O SCRFD redimensiona o quadro para caber no det_size (insightface 2.0 model_zoo/scrfd.py:809-819), então o quadro de 1920 px chega ao detector com 1280 px. No bench, quadro descartado pelo pré-filtro conta como zero detecção no recall (bench.py:110-113,119,125-128). Por isso recall_ge64_max mistura a perda do pré-filtro com a do detector; com --min-faces-plateia 0, o pré-filtro deixa passar todos os quadros (bench.py:110,193). O bench grava por vídeo só a contagem quadros_com_plateia (bench.py:231), e o pipeline grava quadros_com_plateia por janela (reacao/aggregate.py:28-31); nenhum dos dois registra os tempos aceitos (processar_culto.py:77). Os 23 clipes são todos planos de plateia (samples/corpus/pib/README.md:7), então todo quadro descartado nos clipes 07 a 10 é descarte indevido, e esses clipes não medem aceitação indevida de quadros de púlpito. Os clipes 07 a 10 somam 53 quadros amostrados (P8) e cada um dura menos de 30 s, ou seja, cabe numa única janela de agregação. O motor mock não passa pelo pré-filtro (processar_culto.py:70-71), então o CI não exercita esse caminho. O TODO de ladrilhos está em reacao/detect.py:28 (PBI-000D), e PBI-104 é o 'filtro de cena' citado em CONTRIBUTING.md:20. A imagem copia o código no build (Dockerfile:8-11) e é publicada a cada tag v* (.github/workflows/docker.yml:3-4), então a função compartilhada de T2 e o piso proporcional de T4 só entram nos jobs depois de publicados numa imagem nova. O bench exige --provider (bench.py:190), e o motor padrão do pipeline é hsemotion (processar_culto.py:39).

**Regras de negócio:**
- RN01 – As medições usam só os clipes 07 a 10, ou os clipes públicos de desenvolvimento de F3.6 com os rótulos de F3.7 se valer a P13, e rodam em HF Jobs pela imagem publicada com o código da etapa (F4.4.T8 para o piso atual e F4.4.T9 para o piso proporcional).
- RN02 – A medição separa o descarte do pré-filtro da perda do detector.
- RN03 – A correção deste PBI é tornar o piso do pré-filtro proporcional à escala da redução. Ladrilhos, det_size maior e outro detector ficam para F4.7.
- RN04 – O pipeline e o bench aplicam o mesmo pré-filtro, pela mesma função e com os mesmos parâmetros.
- RN05 – A regra que decide se a medição aciona F4.7 é registrada no ADR 0001 antes da primeira medição.
- RN06 – A altura mínima mensurável (64 px) e o k-mínimo (10) não mudam.
- RN07 – Os números vão ao ADR com arquivo de resultado e linhagem, no repositório de resultados de F2.8.

**Fora de escopo:**
- Implementar ladrilhos, det_size maior ou outro detector (F4.7)
- Calibrar limiares (F4.5)
- Medir no conjunto de teste (F4.6)
- Mudar a altura mínima mensurável ou o k-mínimo
- Medir aceitação indevida de quadros de púlpito (os clipes 07 a 10 não têm esses quadros)

#### Critérios de aceite

- Antes da primeira medição, o ADR 0001 registra a regra que decide se a medição aciona F4.7.
- Com o piso atual, o ADR 0001 registra para os clipes 07 a 10: quadros amostrados, quadros descartados pelo pré-filtro, recall_ge64_max com o pré-filtro e recall_ge64_max sem ele.
- O ADR 0001 registra os mesmos números com o piso proporcional.
- Cada número cita o arquivo de resultado, o JOB_ID e o digest da imagem de origem, e o registro traz os parâmetros usados (piso, det_size e mínimo de rostos).
- Um teste automatizado mostra que, num quadro de 1920 px, rostos detectados com 34 a 96 px de altura contam no pré-filtro.
- (erro) O mesmo teste mostra que um quadro com menos rostos que o mínimo continua descartado.
- Um teste com detector simulado mostra que a função compartilhada de pré-filtro devolve os mesmos tempos aceitos quando chamada pelo pipeline e pelo bench, e, no mesmo clipe, quadros e quadros_com_plateia são iguais no bench e no pipeline.
- (erro) Nenhuma execução deste PBI inclui clipe de teste: a lista de vídeos de cada registro contém só clipes de desenvolvimento.
- O ADR 0001 registra se o detector atual atende rostos de 34 a 96 px ou se F4.7 é acionado, e o TODO de reacao/detect.py:28 passa a citar o ADR.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F4.4.T1 | Data Science | Registrar no ADR 0001 o plano de medição e a regra de acionamento de F4.7 | 3 | — |
| F4.4.T2 | Visão Computacional | Extrair o pré-filtro para uma função compartilhada pelo pipeline e pelo bench, com piso e det_size configuráveis | 6 | F2.8 |
| F4.4.T3 | Visão Computacional | Medir no HF Jobs, nos clipes 07 a 10, o descarte do pré-filtro e a perda do detector com o piso atual | 4 | F4.4.T1, F4.4.T8, F1.1, F2.3.T3, F3.4, F3.7 (só se o acionamento for o veto da PIB), Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F4.4.T4 | Visão Computacional | Tornar o piso do pré-filtro proporcional à escala da redução | 4 | F4.4.T2 |
| F4.4.T5 | Visão Computacional | Medir de novo no HF Jobs com o piso proporcional | 3 | F4.4.T9, Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F4.4.T6 | Data Science | Analisar os números e registrar no ADR 0001 a decisão sobre F4.7 | 4 | F4.4.T3, F4.4.T5 |
| F4.4.T7 | QA | Verificar os critérios de aceite de F4.4 | 5 | F4.4.T6 |
| F4.4.T8 | DevOps | Publicar por tag de pré-release a imagem com o pré-filtro compartilhado de F4.4.T2 e registrar o digest | 2 | F2.2, F4.4.T2 |
| F4.4.T9 | DevOps | Publicar por tag de pré-release a imagem com o piso proporcional de F4.4.T4 e registrar o digest | 2 | F2.2, F4.4.T4 |

<details><summary>F4.4.T1 · [Data Science] Registrar no ADR 0001 o plano de medição e a regra de acionamento de F4.7</summary>

**Objetivo:** O plano e a regra ficam registrados e assinados antes da primeira medição.

**Passos previstos:**
1. Descrever as execuções: piso atual com e sem pré-filtro; piso proporcional com e sem pré-filtro; det_size na largura nativa só como diagnóstico para F4.7.
2. Definir as métricas: quadros descartados por clipe, recall_ge64_max e rostos marcados com 64 px ou mais.
3. Propor a regra que aciona F4.7 e colher a assinatura de Fabio.
4. Registrar o plano no ADR 0001 em commit anterior ao primeiro job.

**Definição de pronto:** O ADR 0001 tem o plano e a regra num commit anterior ao primeiro JOB_ID de F4.4.

**Dependências:** nenhuma

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F4.4.T2 · [Visão Computacional] Extrair o pré-filtro para uma função compartilhada pelo pipeline e pelo bench, com piso e det_size configuráveis</summary>

**Objetivo:** O pipeline e o bench usam uma única função de pré-filtro com piso, det_size e mínimo de rostos configuráveis, e um teste mostra que os dois aceitam os mesmos tempos.

**Passos previstos:**
1. Extrair para uma função compartilhada o pré-filtro de processar_culto.py:73-74 e bench.py:109-110, que devolve os tempos aceitos.
2. Acrescentar parâmetros de piso do pré-filtro e de det_size da passada plena, com os valores atuais como padrão.
3. Registrar os parâmetros usados no log e na linhagem de F2.8.
4. Escrever teste que confirma o mesmo resultado com os valores padrão.
5. Escrever teste com detector simulado que compara os tempos aceitos pela função quando chamada pelo caminho do pipeline e pelo do bench.

**Definição de pronto:** Com os valores padrão, pipeline e bench produzem o mesmo resultado de antes, e o teste de tempos aceitos passa. ruff check e pytest passam. O PR cita F4.4 e PBI-104.

**Dependências:** F2.8

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F4.4.T3 · [Visão Computacional] Medir no HF Jobs, nos clipes 07 a 10, o descarte do pré-filtro e a perda do detector com o piso atual</summary>

**Objetivo:** Os números com o piso atual ficam no repositório de resultados com linhagem.

**Passos previstos:**
1. Pedir ao dono aprovação dos jobs, com flavor, duração e custo previstos (P7).
2. Rodar o bench pela imagem com o digest de F4.4.T8, apontando para a pasta de rótulos de desenvolvimento, com o mínimo de rostos em 5 e em 0.
3. Rodar a variante com det_size na largura nativa, só como diagnóstico.
4. Conferir que os resultados chegaram ao repositório de resultados de F2.8 com JOB_ID, digest e parâmetros.

**Definição de pronto:** Três conjuntos de resultados com linhagem estão no repositório de resultados, e a lista de vídeos de cada um contém só clipes 07 a 10.

**Dependências:** F4.4.T1, F4.4.T8, F1.1, F2.3.T3, F3.4, F3.7 (só se o acionamento for o veto da PIB), Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.4.T4 · [Visão Computacional] Tornar o piso do pré-filtro proporcional à escala da redução</summary>

**Objetivo:** No quadro reduzido, o pré-filtro conta rostos pelo piso equivalente ao do quadro original.

**Passos previstos:**
1. Calcular o piso do pré-filtro a partir da razão entre a largura reduzida e a original.
2. Aplicar o novo piso só à contagem do pré-filtro, sem mudar o piso da passada plena nem a altura mensurável.
3. Escrever testes com detector simulado: rostos de 34 a 96 px num quadro de 1920 px contam, e um quadro com menos rostos que o mínimo é descartado.

**Definição de pronto:** Os testes passam. ruff check e pytest passam. O PR cita F4.4 e PBI-104.

**Dependências:** F4.4.T2

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.4.T5 · [Visão Computacional] Medir de novo no HF Jobs com o piso proporcional</summary>

**Objetivo:** Os números com o piso proporcional ficam no repositório de resultados com linhagem.

**Passos previstos:**
1. Pedir ao dono aprovação dos jobs, com flavor, duração e custo previstos (P7).
2. Rodar o bench pela imagem com o digest de F4.4.T9 nos clipes 07 a 10 com o piso proporcional, com o mínimo de rostos em 5 e em 0.
3. Rodar o pipeline de produção pela mesma imagem num dos clipes, com --no-transcribe e --stdout, e guardar quadros e quadros_com_plateia da janela para o critério 7.
4. Conferir a chegada dos resultados com JOB_ID, digest e parâmetros.

**Definição de pronto:** Os resultados com o piso proporcional e a execução do pipeline estão no repositório de resultados, só com clipes 07 a 10.

**Dependências:** F4.4.T9, Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F4.4.T6 · [Data Science] Analisar os números e registrar no ADR 0001 a decisão sobre F4.7</summary>

**Objetivo:** O ADR 0001 tem os números antes e depois e a decisão tomada pela regra registrada.

**Passos previstos:**
1. Montar a tabela por clipe e o total: quadros, descartados, recall_ge64_max com e sem pré-filtro, com o piso atual e o proporcional.
2. Separar a perda atribuída ao pré-filtro da perda atribuída ao detector.
3. Aplicar a regra de F4.4.T1 e registrar se F4.7 é acionado, com o diagnóstico da variante de det_size.
4. Trocar o TODO de reacao/detect.py:28 por uma referência ao ADR e retirar dele a referência PBI-000D, citando F4.7 no lugar.

**Definição de pronto:** O ADR 0001 tem a tabela, com arquivo, JOB_ID e digest em cada número, e a decisão. O PR tem a aprovação de Fabio. Uma busca por PBI-000D em reacao/detect.py não encontra resultado.

**Dependências:** F4.4.T3, F4.4.T5

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.4.T7 · [QA] Verificar os critérios de aceite de F4.4</summary>

**Objetivo:** Os nove critérios ficam verificados e anotados no PBI.

**Passos previstos:**
1. Conferir no histórico do git que o plano e a regra (T1) são anteriores ao primeiro JOB_ID.
2. Rodar os testes de T4 e conferir o caso de rostos de 34 a 96 px e o caso de quadro descartado.
3. Rodar o teste de tempos aceitos de T2 e comparar quadros e quadros_com_plateia do bench e do pipeline no mesmo clipe.
4. Conferir que cada número do ADR aponta arquivo, JOB_ID, digest e parâmetros, que o digest dos jobs é o de F4.4.T8 (piso atual) ou de F4.4.T9 (piso proporcional) e que as listas de vídeos só têm clipes 07 a 10.
5. Anotar no PBI o resultado de cada critério.

**Definição de pronto:** Os nove critérios estão marcados como passou ou não passou, com as evidências anotadas no PBI.

**Dependências:** F4.4.T6

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F4.4.T8 · [DevOps] Publicar por tag de pré-release a imagem com o pré-filtro compartilhado de F4.4.T2 e registrar o digest</summary>

**Objetivo:** As medições de F4.4.T3 têm uma imagem com digest que contém a função compartilhada de pré-filtro com piso e det_size configuráveis.

**Passos previstos:**
1. Conferir que o PR de F4.4.T2 está mesclado em main e que o CI desse commit passou.
2. Criar a tag de pré-release nesse commit, pelo processo de publicação de F2.2 e na composição de imagem do ADR de F2.4 (imagem única ou imagem do motor padrão, hsemotion).
3. Registrar no PBI a tag, o commit e o digest publicado.

**Definição de pronto:** O PBI tem a tag, o commit e o digest, e o workflow de publicação desse commit terminou com sucesso.

**Dependências:** F2.2, F4.4.T2

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F4.4.T9 · [DevOps] Publicar por tag de pré-release a imagem com o piso proporcional de F4.4.T4 e registrar o digest</summary>

**Objetivo:** As medições de F4.4.T5 têm uma imagem com digest que contém o piso proporcional.

**Passos previstos:**
1. Conferir que o PR de F4.4.T4 está mesclado em main e que o CI desse commit passou.
2. Criar a tag de pré-release nesse commit, pelo processo de publicação de F2.2 e na mesma composição de imagem usada em F4.4.T8.
3. Registrar no PBI a tag, o commit e o digest publicado.

**Definição de pronto:** O PBI tem a tag, o commit e o digest, e o workflow de publicação desse commit terminou com sucesso.

**Dependências:** F2.2, F4.4.T4

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- processar_culto.py:39,41,70-77
- reacao/detect.py:9,14-16,27-34
- reacao/ingest.py:45-49
- reacao/types.py:5-8
- reacao/aggregate.py:28-31
- bench.py:102-134,190,193,231
- Dockerfile:8-11
- .github/workflows/docker.yml:3-4
- insightface 2.0 instalado: insightface/model_zoo/scrfd.py:809-819
- samples/corpus/pib/README.md:7-8 e ffprobe.csv (não versionados)
- docs/adr/0001-motor.md:4
- docs/poc-gate.md:46-48
- CONTRIBUTING.md:20
- premissas P8 e P13

#### Verificação INVEST: pontos que falharam
- Small: 8 pontos e nove tasks, no limite de uma sprint.
- Independente: depende dos rótulos de F3.4 (ou de F3.7, com o veto da PIB), da linhagem de F2.8 e do processo de publicação de F2.2.

#### Premissas
- Disciplinas: Visão Computacional, Data Science e QA vêm da árvore. DevOps entrou pelas tasks F4.4.T8 e F4.4.T9, que publicam a imagem com o código de T2 e de T4 antes de cada rodada de medição (revisão 3).
- F2.3.T3 e F2.8 entraram porque a métrica do épico exige linhagem, com hash dos pesos, para todo número do ADR 0001; F4.4 depende só do mecanismo de F2.3 (T3), e não do PBI inteiro, para não voltar ao ciclo F2.3→F4.7→F4.4 (revisão 4). F1.1 entrou porque os jobs sobre clipes da PIB passam pelo lançador que recusa caminho local. F2.2 entrou pelas tasks de publicação.
- A regra de acionamento de F4.7 é proposta em T1 e assinada por Fabio. Um candidato é a meta de 80% do critério 1 (docs/poc-gate.md:8) aplicada aos clipes 07 a 10, mas a regra não está decidida.
- É dedução que a medição com o mínimo de rostos em 0 isola a perda do detector, porque esse valor deixa passar todos os quadros (bench.py:110).
- É dedução que cada clipe de 07 a 10 cabe numa janela de 30 s e que isso permite comparar quadros e quadros_com_plateia entre bench e pipeline no mesmo clipe.
- Os jobs de medição usam a imagem do motor padrão (hsemotion, processar_culto.py:39) quando o ADR de F2.4 decidir por uma imagem por motor. É dedução que o motor não altera recall_ge64_max nem o descarte do pré-filtro, que dependem só do detector.
- O flavor dos jobs de medição fica a definir; a aprovação do dono é obrigatória (P7).
- Story points e horas são sugestão. Com 8 pontos, o PBI está no limite de uma sprint; se não couber, dividir entre medição e correção.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável, Story Points (sugestão: 8) e vínculo Parent com a Feature F4.
- F4.7: regra de acionamento e números registrados.
- F2.8: parâmetros do pré-filtro (piso, det_size e mínimo de rostos) e digest na linhagem.
- F5.4: medir, nos cultos inteiros, os quadros de púlpito aceitos como plateia com o piso proporcional.
- F2.3: com o manifesto marcando det_500m.onnx como não espelhável, a execução termina antes do primeiro quadro (critério 5 de F2.3). Confirmar se a medição de F4.4.T3 com o SCRFD pode carregar o peso da origem com revisão e hash fixados quando F4.3 permitir o uso no PoC e vetar só o espelhamento (revisão 4).

## Preview — PBI F4.5 (novo) · Calibrar nos clipes de desenvolvimento o limiar de sorriso por motor e registrar a origem dos limites de voltado ao palco e dos limiares de evento

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Calibrar nos clipes de desenvolvimento o limiar de sorriso por motor e registrar a origem dos limites de voltado ao palco e dos limiares de evento |
| Tipo | Product Backlog Item |
| Pai | F4 |
| Tags | F4; limiares; calibracao; clipes-dev; data-science |
| Estimativa | 8 pts (sugestão); tasks: 41 h |
| Dependências | F1.2 – tempo dos quadros e janelas adjacentes nos eventos, F2.2 – processo de publicação da imagem por tag com digest, usado por T9 (acrescentada na revisão 3), F2.8 – repositório de resultados com linhagem, exigido para números no ADR 0001 (acrescentada na revisão 3), F3.4 – rótulos dos clipes 07 a 10, F3.7 – rótulos públicos de desenvolvimento (F3.7.T4, publicados com tag em F3.7.T8), se o acionamento for o veto da PIB (acrescentada na revisão 3), F4.1 – LibreFace executável, escala de p_smile e pose em graus, F4.2 – Py-Feat executável, F4.4 – pré-filtro corrigido e medido, F4.7 – detector novo, se acionado |
| Substitui | nenhum |

#### Descrição

Como integrante do time de Data Science que prepara o bench do conjunto de teste  
Quero definir por motor o limiar de sorriso e registrar a origem dos limites de voltado ao palco e dos limiares de evento, só com os clipes 07 a 10  
Para que o bench de F4.6 rode com limiares fixados antes do conjunto de teste, sem calibrar com clipes de teste

**Contexto:** A agregação conta como sorrindo todo rosto com p_smile >= 0,5, em qualquer motor (reacao/aggregate.py:40). O p_smile, porém, é a probabilidade de Happiness no HSEmotion (reacao/providers/hsemotion.py:31), a coluna happiness no Py-Feat (reacao/providers/pyfeat.py:28) e AU12 no LibreFace, na escala declarada em F4.1. 'Voltado ao palco' é |yaw| < 30 e |pitch| < 25, fixo em FaceObservation.facing (reacao/types.py:31-35), sem calibração registrada; a pose do LibreFace chega em graus depois da conversão de F4.1. Os eventos usam queda de 15 p.p., recuperação de 10 p.p., 3 janelas sustentadas e pico de 20 p.p., com os mesmos valores para todos os motores (reacao/events.py:11-12). O pico_sorriso compara cada janela com as 6 anteriores válidas (reacao/events.py:33-34). As janelas têm 30 s (reacao/types.py:8), e os clipes 07 a 10 duram 8,3 s, 15,7 s, 13,7 s e 13,9 s (samples/corpus/pib/ffprobe.csv), então cada um cabe numa única janela. Os rótulos marcam altura por rosto e intervalos de riso, aplauso, pe, cabeca_baixa e neutro, sem orientação por rosto (labels/README.md:6-11). O bench calcula um único valor por intervalo rotulado, com o limiar fixo da agregação (bench.py:73-81), mede a subida de cada riso rotulado sobre a base neutra e calcula frac_equiv30, a subida convertida para a janela de 30 s (bench.py:137-152; docs/poc-gate.md:28-33). Não existe no bench cálculo para limiares alternativos. A subida mínima de 15 p.p. e a meta de 70% são regras do critério 2a (docs/poc-gate.md:9). Calibrar com os clipes de teste está fora do épico (docs/poc-gate.md:46-48). As observações por rosto são apagadas após a agregação (processar_culto.py:82). A imagem copia o código no build (Dockerfile:8-11) e é publicada a cada tag v* (.github/workflows/docker.yml:3-4), então o limiar por motor de T2 e a grade de T3 só entram nos jobs depois de publicados numa imagem nova.

**Regras de negócio:**
- RN01 – Só entram os clipes 07 a 10, ou os públicos de desenvolvimento de F3.6 com os rótulos de F3.7 (P13). Nenhuma execução usa clipe de teste.
- RN02 – O limiar de p_smile é definido por motor, na escala do motor.
- RN03 – As metas do gate (80%, 70%, 15 p.p. e a meta do jitter assinada em F1.3) não são calibradas aqui.
- RN04 – O método de calibração (métrica, grade de valores e mínimo de eventos) é registrado antes das execuções.
- RN05 – Cada limiar usado no bench de F4.6 tem registro de origem: calibrado, com o arquivo de resultado, ou mantido sem calibração, com o motivo (P8).
- RN06 – Os valores ficam numa configuração versionada, citada no ADR 0001, num commit anterior ao primeiro job de F4.6.
- RN07 – Os jobs guardam só agregados por intervalo rotulado para cada limiar candidato. Nenhum valor por rosto sai do job (CLAUDE.md, regras 2 e 6; processar_culto.py:82).
- RN08 – Se F4.7 for acionado, a calibração usa o detector novo.
- RN09 – Os jobs rodam pela imagem publicada em F4.5.T9, com o código de T2 e T3 e dos PBIs F4.1, F4.2 e F4.4 (e F4.7, se acionado), e os resultados vão ao repositório de resultados com linhagem de F2.8.

**Fora de escopo:**
- Mudar a janela de 30 s da produção (se a análise recomendar, vira item novo)
- Calibrar com clipes de teste
- Mudar as metas do gate
- Calibrar limiares de evento com cultos inteiros (pendência)
- Treino ou ajuste fino de motor

#### Critérios de aceite

- Antes da primeira execução, o ADR 0001 registra o método de calibração: métrica, grade de valores e mínimo de eventos.
- Para cada motor que ficou na comparação, o ADR 0001 registra o limiar de p_smile, a escala, a origem e o commit da configuração versionada, e os valores são iguais aos dessa configuração.
- Os limites de |yaw| e |pitch| e os limiares de evento (15 p.p., 10 p.p., 3 janelas e 20 p.p.) têm origem registrada: calibrado, com o arquivo de resultado, ou mantido, com o motivo.
- (erro) Um teste falha se o pipeline ou o bench usar, para algum motor, um limiar de p_smile diferente do da configuração versionada citada no ADR 0001.
- O commit que registra os limiares é anterior ao primeiro job de F4.6.
- (erro) Nenhuma execução deste PBI inclui clipe de teste: a lista de vídeos de cada registro contém só clipes de desenvolvimento.
- (erro) Quando os clipes 07 a 10 não têm risos ou trechos neutros suficientes para o método, o limiar do motor fica como está, e o registro diz 'não calibrado' com a contagem de eventos.
- O frac_equiv30 de cada motor nos clipes 07 a 10 está registrado, com a decisão de manter a janela de 30 s ou abrir item novo.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F4.5.T1 | Data Science | Registrar o método de calibração antes das execuções | 4 | — |
| F4.5.T2 | Machine Learning | Tornar o limiar de p_smile configurável por motor no pipeline e no bench | 6 | — |
| F4.5.T3 | Machine Learning | Implementar no bench o cálculo por intervalo rotulado para a grade de limiares de p_smile e de \|yaw\| e \|pitch\| | 8 | F4.5.T1, F4.5.T2 |
| F4.5.T4 | Machine Learning | Executar no HF Jobs o bench de cada motor nos clipes 07 a 10 com a grade de limiares | 5 | F4.5.T9, F2.8, F3.4, F3.7 (só se o acionamento for o veto da PIB), Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F4.5.T5 | Data Science | Escolher o limiar de p_smile por motor e registrar a origem no ADR 0001 | 5 | F4.5.T4 |
| F4.5.T6 | Visão Computacional | Revisar os limites de voltado ao palco com os trechos cabeca_baixa dos clipes 07 a 10 | 4 | F4.5.T4 |
| F4.5.T7 | Data Science | Registrar a origem dos limiares de evento e a análise de frac_equiv30 | 3 | F4.5.T4 |
| F4.5.T8 | QA | Verificar os critérios de aceite de F4.5 | 4 | F4.5.T5, F4.5.T6, F4.5.T7 |
| F4.5.T9 | DevOps | Publicar por tag de pré-release as imagens com o limiar por motor e a grade do bench e registrar os digests | 2 | F2.2, F4.5.T3, F4.1, F4.2, F4.4, F4.7 (só se acionado) |

<details><summary>F4.5.T1 · [Data Science] Registrar o método de calibração antes das execuções</summary>

**Objetivo:** O método fica no ADR 0001 num commit anterior à primeira execução.

**Passos previstos:**
1. Definir a métrica de separação entre riso e neutro por motor, junto com o jitter nos trechos neutros.
2. Definir a grade de limiares candidatos de p_smile na escala de cada motor e a grade de limites de |yaw| e |pitch|.
3. Definir o mínimo de risos e de trechos neutros para calibrar, e o que acontece abaixo dele (P8).
4. Registrar no ADR 0001 e colher a aprovação de Fabio.

**Definição de pronto:** O método está no ADR 0001 num commit anterior ao primeiro JOB_ID de F4.5.

**Dependências:** nenhuma

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.5.T2 · [Machine Learning] Tornar o limiar de p_smile configurável por motor no pipeline e no bench</summary>

**Objetivo:** O pipeline e o bench leem o limiar de cada motor de uma configuração versionada.

**Passos previstos:**
1. Criar a configuração versionada de limiares por motor, com 0,5 como valor inicial.
2. Fazer a agregação e o bench usarem o limiar do motor em execução.
3. Registrar o limiar usado no log e na linhagem.
4. Escrever teste que falha quando o limiar usado difere do configurado.

**Definição de pronto:** Com a configuração inicial, os resultados não mudam. O teste passa. ruff check e pytest passam. O PR cita F4.5.

**Dependências:** nenhuma

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F4.5.T3 · [Machine Learning] Implementar no bench o cálculo por intervalo rotulado para a grade de limiares de p_smile e de |yaw| e |pitch|</summary>

**Objetivo:** O bench calcula, dentro do job, pct_sorrindo e pct_voltados por intervalo rotulado para cada valor candidato da grade, sem gravar valor por rosto.

**Passos previstos:**
1. Receber a grade de F4.5.T1 como parâmetro versionado do bench.
2. Para cada intervalo rotulado, calcular pct_sorrindo para cada limiar candidato de p_smile e pct_voltados para cada par candidato de limites de |yaw| e |pitch|, com a mesma regra de k-mínimo da agregação.
3. Gravar no CSV uma coluna por valor candidato, sem valor por rosto.
4. Escrever testes com observações simuladas que conferem os valores por candidato com um cálculo manual e verificam que nenhuma coluna traz valor por rosto.

**Definição de pronto:** ruff check e pytest passam. Um CSV de teste tem uma coluna por valor candidato e nenhum valor por rosto. O PR cita F4.5.

**Dependências:** F4.5.T1, F4.5.T2

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F4.5.T4 · [Machine Learning] Executar no HF Jobs o bench de cada motor nos clipes 07 a 10 com a grade de limiares</summary>

**Objetivo:** Para cada motor, os agregados por intervalo rotulado e por valor candidato ficam no repositório de resultados com linhagem.

**Passos previstos:**
1. Pedir ao dono aprovação dos jobs, com flavor, duração e custo previstos (P7).
2. Rodar um job por motor, pela imagem com o digest de F4.5.T9 (a do motor, se houver uma imagem por motor), com o bench de F4.5.T3, sobre a pasta de rótulos de desenvolvimento.
3. Conferir a chegada dos resultados ao repositório de resultados de F2.8 com JOB_ID, digest, motor, grade e lista de vídeos.

**Definição de pronto:** Há um conjunto de resultados por motor com linhagem, só com clipes 07 a 10, com as colunas da grade e sem valor por rosto.

**Dependências:** F4.5.T9, F2.8, F3.4, F3.7 (só se o acionamento for o veto da PIB), Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F4.5.T5 · [Data Science] Escolher o limiar de p_smile por motor e registrar a origem no ADR 0001</summary>

**Objetivo:** Cada motor tem o limiar escolhido pelo método de T1, ou o registro 'não calibrado'.

**Passos previstos:**
1. Aplicar o método de T1 aos resultados de T4.
2. Registrar por motor o limiar, a escala, a métrica obtida, a contagem de eventos e o arquivo de origem.
3. Quando faltarem eventos, registrar 'não calibrado' com a contagem.
4. Atualizar a configuração versionada de T2 e citar no ADR 0001 o commit dela.

**Definição de pronto:** O ADR 0001 e a configuração versionada têm o mesmo limiar para cada motor, num commit anterior ao primeiro job de F4.6.

**Dependências:** F4.5.T4

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F4.5.T6 · [Visão Computacional] Revisar os limites de voltado ao palco com os trechos cabeca_baixa dos clipes 07 a 10</summary>

**Objetivo:** Os limites de |yaw| e |pitch| ficam com origem registrada.

**Passos previstos:**
1. Contar os trechos cabeca_baixa rotulados nos clipes 07 a 10.
2. Se houver trechos, comparar por motor o pct_voltados das colunas da grade de T3 dentro e fora deles.
3. Registrar os limites mantidos ou alterados, com o arquivo de origem, ou 'mantido sem calibração' com a contagem de trechos.

**Definição de pronto:** O ADR 0001 registra a origem dos limites de |yaw| e |pitch|.

**Dependências:** F4.5.T4

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.5.T7 · [Data Science] Registrar a origem dos limiares de evento e a análise de frac_equiv30</summary>

**Objetivo:** Os limiares de evento e a janela de 30 s ficam com origem e decisão registradas.

**Passos previstos:**
1. Registrar que os clipes 07 a 10, cada um menor que uma janela de 30 s, não exercitam queda, recuperação nem pico, e marcar 15 p.p., 10 p.p., 3 janelas e 20 p.p. como 'mantido sem calibração'.
2. Registrar o frac_equiv30 de cada motor nos clipes 07 a 10.
3. Registrar a decisão de manter a janela de 30 s ou de propor item novo.

**Definição de pronto:** O ADR 0001 tem a origem dos limiares de evento e a decisão sobre a janela.

**Dependências:** F4.5.T4

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F4.5.T8 · [QA] Verificar os critérios de aceite de F4.5</summary>

**Objetivo:** Os oito critérios ficam verificados e anotados no PBI.

**Passos previstos:**
1. Conferir no histórico do git que o método é anterior ao primeiro JOB_ID de F4.5 e que os limiares são anteriores ao primeiro job de F4.6.
2. Rodar o teste de limiar por motor e conferir que ele falha com um valor divergente da configuração versionada.
3. Conferir que os valores de limiar do ADR 0001 são iguais aos da configuração versionada citada nele.
4. Conferir que as listas de vídeos só têm clipes 07 a 10, que nenhum resultado traz valor por rosto e que o digest de cada job de T4 é o de F4.5.T9.
5. Conferir a origem registrada de cada limiar.
6. Anotar no PBI o resultado de cada critério.

**Definição de pronto:** Os oito critérios estão marcados como passou ou não passou, com as evidências anotadas no PBI.

**Dependências:** F4.5.T5, F4.5.T6, F4.5.T7

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.5.T9 · [DevOps] Publicar por tag de pré-release as imagens com o limiar por motor e a grade do bench e registrar os digests</summary>

**Objetivo:** Os jobs de F4.5.T4 têm imagens com digest que contêm o código de F4.5.T2 e T3 e os providers e o pré-filtro de F4.1, F4.2 e F4.4 (e o detector de F4.7, se acionado).

**Passos previstos:**
1. Conferir que os PRs de F4.5.T2 e T3 e dos PBIs F4.1, F4.2 e F4.4 (e F4.7, se acionado) estão mesclados em main e que o CI desse commit passou.
2. Criar a tag de pré-release nesse commit, pelo processo de publicação de F2.2 e na composição de imagem do ADR de F2.4 (imagem única ou uma por motor).
3. Registrar no PBI a tag, o commit e o digest de cada imagem.

**Definição de pronto:** O PBI tem a tag, o commit e o digest de cada imagem, e o workflow de publicação desse commit terminou com sucesso.

**Dependências:** F2.2, F4.5.T3, F4.1, F4.2, F4.4, F4.7 (só se acionado)

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- reacao/aggregate.py:40
- reacao/types.py:8,31-35
- reacao/events.py:11-12,32-37
- reacao/providers/hsemotion.py:31; reacao/providers/pyfeat.py:28; reacao/providers/libreface.py:31
- bench.py:18-21,73-81,137-152,194
- docs/poc-gate.md:9,28-33,46-48
- labels/README.md:6-15
- samples/corpus/pib/ffprobe.csv (não versionado)
- processar_culto.py:82
- Dockerfile:8-11
- .github/workflows/docker.yml:3-4
- premissas P8 e P13

#### Verificação INVEST: pontos que falharam
- Independente: depende de nove PBIs, dois deles condicionais (F3.7 e F4.7).
- Small: 8 pontos e nove tasks, no limite de uma sprint.
- Testável: o resultado 'não calibrado' é aceitável, então o critério mede o registro, e não a melhoria do limiar.

#### Premissas
- QA entrou em relação à árvore (que previa Data Science, Machine Learning e Visão Computacional) porque o PBI muda código (limiar por motor e grade no bench) e a regra do épico exige task de QA para PBI com código.
- DevOps entrou pela task F4.5.T9, que publica a imagem com o código de T2 e T3 antes dos jobs de T4 (revisão 3).
- F2.8 entrou porque o PBI registra no ADR 0001 números com arquivo de resultado e linhagem (RN06 da Feature). F2.2 entrou pela task de publicação.
- É dedução do tamanho dos clipes e de reacao/events.py:33-34 que os limiares de evento não podem ser exercitados nos clipes 07 a 10. Se isso se confirmar, eles saem como 'mantido sem calibração' com esse motivo.
- É dedução que 'voltado ao palco' só pode ser revisado por meio dos trechos cabeca_baixa, porque o rótulo não tem orientação por rosto. Sem esses trechos nos clipes 07 a 10, os limites ficam como estão.
- É dedução que calcular dentro do job os agregados para cada limiar candidato atende às regras 2 e 6, porque nenhum valor por rosto sai do job.
- Story points e horas são sugestão, a validar no refinamento. Os pontos passaram de 5 para 8 com a task F4.5.T3.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável, Story Points (sugestão: 8) e vínculo Parent com a Feature F4.
- Calibração dos limiares de evento com dados que tenham janelas de 30 s rotuladas: decidir no refinamento entre F5.5, F6.6 ou manter como está.
- F4.6: valores e commit da configuração versionada de limiares.
- F2.8: limiar de p_smile por motor e grade de candidatos na linhagem.

## Preview — PBI F4.6 (novo) · Rodar o bench de cada motor na t4-small sobre o conjunto de teste e registrar a decisão no ADR 0001

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Rodar o bench de cada motor na t4-small sobre o conjunto de teste e registrar a decisão no ADR 0001 |
| Tipo | Product Backlog Item |
| Pai | F4 |
| Tags | F4; bench; t4-small; adr-0001; gate; hf-jobs; PBI-000H |
| Estimativa | 8 pts (sugestão); tasks: 29 h |
| Dependências | F1.1 – script de lançamento que recusa caminho local, usado por F4.6.T2, F1.4 – bench e validador corrigidos (e, por ele, F1.3), F2.2 – imagem com os motores, digest e processo de publicação por tag, usado por T7, F2.3 – pesos com hash, F2.4 – modo de execução dos jobs do gate, F2.8 – repositório de resultados com linhagem (no lugar de F2.5, revisão 3), F3.4 – rótulos do conjunto de teste com tag, F3.7 – rótulos públicos com tag, se acionado (no lugar de F3.6, revisão 3; F3.7 depende de F3.6), F4.1 – LibreFace executável, F4.2 – Py-Feat executável, F4.3 – licenças e motores retirados, F4.5 – limiares registrados, F4.7 – detector novo, se acionado |
| Substitui | PBI-000H |

#### Descrição

Como Fabio Pinheiro, que assina o ADR 0001 e o gate com o pastor Filipe  
Quero o resultado do bench de cada motor no conjunto de teste, na t4-small e com linhagem, e a escolha do motor de produção e do de reserva registrada no ADR 0001  
Para levar a F6.1 os valores dos critérios 1, 2a e 2b do motor escolhido e decidir o gate com números rastreáveis

**Contexto:** O bench repete o laço de produção e calcula recall_ge64_max, frac_eventos_riso_ok, frac_equiv30, jitter_dp_pp, fps e custo por hora de vídeo. A linha TOTAL é a que vale para o gate (bench.py:5-31,102-265; docs/poc-gate.md:3-4). O bench aceita --excluir para deixar os clipes 07 a 10 fora da medição (bench.py:195; docs/poc-gate.md:46-48). O conjunto de teste tem 19 clipes e 195 quadros, ou menos se F1.3 retirar o clipe 11, ou os clipes públicos de F3.6 com os rótulos de F3.7 se esses PBIs forem acionados. O CSV é gravado em out/bench (bench.py:255), que se perde ao fim do job no HF (https://huggingface.co/docs/hub/jobs-manage#persist-your-results); F2.8 envia o CSV ao repositório de resultados com a linhagem. O comando documentado roda 'hf jobs uv run' a partir do main, com --corpus na raiz do dataset, rótulos numa pasta que não existe e sem --excluir (docs/hf-jobs.md:23-29). F2.4 decide que os jobs do gate rodam com 'hf jobs run' pela imagem com digest. A imagem copia o código no build (Dockerfile:8-11) e é publicada a cada tag v* (.github/workflows/docker.yml:3-4), e a imagem publicada por F2.2 é anterior ao código de F4.1 a F4.5 e F4.7; por isso F4.6.T7 publica a release com esse código. O custo por hora do bench conta só o tempo de inferência (bench.py:182-183,250-252), e a fórmula do critério 5 é a pré-registrada em F1.3. A t4-small custa US$ 0,40/h (docs/hf-jobs.md:4; reacao/cost.py:5; https://huggingface.co/docs/hub/jobs-pricing). Nenhum job foi executado até 2026-09-23. A tabela do ADR 0001 tem as colunas recall ≥64 px, sensibilidade (p.p.), jitter (p.p.), fps T4, custo/h vídeo, licença e decisão (docs/adr/0001-motor.md:8-14). O valor que vai à coluna 'sensibilidade (p.p.)', frac_eventos_riso_ok, é uma fração de eventos de 0 a 1 (bench.py:176), e a meta do critério 2a é ≥ 70% (docs/poc-gate.md:9). O critério 1 vale só para o detector medido (P31); se F4.7 trocar o detector, o bench roda com o detector novo.

**Regras de negócio:**
- RN01 – Roda um job por motor que ficou na comparação depois de F4.1, F4.2 e F4.3, com 'hf jobs run' pela imagem com digest publicada em F4.6.T7 (modo do ADR de F2.4) e flavor t4-small (docs/poc-gate.md:13).
- RN02 – Commit, revisão dos rótulos, hash dos pesos comuns, configuração do detector e limiares de F4.5 são os mesmos em todos os jobs, exceto nos itens próprios de cada motor.
- RN03 – Nenhum job roda sobre o conjunto de teste antes da assinatura de F1.3 e do registro dos limiares de F4.5.
- RN04 – Entram só os clipes de teste. Os clipes 07 a 10 e o concatenado ficam de fora.
- RN05 – Todo número do ADR cita o arquivo de resultado e a linhagem, no repositório de resultados de F2.8.
- RN06 – Execução que falha fica no registro de resultados de F2.8 com a etapa e a mensagem, e uma nova execução recebe outro run_id.
- RN07 – Cada job pago tem aprovação prévia do dono, e o saldo precisa estar positivo (P7).
- RN08 – Motor com uso no piloto vetado por F4.3 não é escolhido para produção.
- RN09 – Os critérios 1, 2a e 2b do gate vêm da linha TOTAL do motor escolhido (docs/poc-gate.md:3-4).
- RN10 – A coluna custo/h do ADR declara a fórmula usada.
- RN11 – Cada coluna da tabela do ADR declara a unidade. frac_eventos_riso_ok é registrado como fração de eventos, sob esse nome.
- RN12 – A configuração do detector de todos os jobs é a registrada em F4.7, ou a atual se F4.7 não for acionado (P31).

**Fora de escopo:**
- Critério 5 em cultos inteiros (F5.4)
- Critérios 3 e 4 (F5.5 e F5.7)
- Preencher docs/poc-gate.md e decidir o gate (F6.1)
- Expressão e pose na GPU (F5.3)
- Tela de resultados no painel web na Vercel

#### Critérios de aceite

- O repositório de resultados tem um bench_<motor>.csv por motor comparado, cada um com JOB_ID, digest da imagem, commit, revisão dos rótulos e hash dos pesos.
- Todos os CSVs listam os mesmos vídeos de teste, e nenhum deles inclui os clipes 07 a 10 ou o concatenado.
- Para cada motor, a tabela do ADR 0001 tem recall ≥64 px (fração), frac_eventos_riso_ok (fração de eventos, 0 a 1, na coluna antes chamada 'sensibilidade (p.p.)'), jitter (p.p.), fps T4, custo/h (US$ por hora de vídeo) e licença. Cada coluna declara a unidade, e cada valor é igual ao da linha TOTAL do CSV citado.
- O ADR 0001 registra o motor de produção e o de reserva, com os motivos, citando os números e a licença.
- O ADR 0001 indica o arquivo e a linha de onde F6.1 lê os critérios 1, 2a e 2b.
- O primeiro job do bench tem data posterior ao commit da assinatura de F1.3 e ao commit dos limiares de F4.5.
- docs/hf-jobs.md traz o comando do bench do gate usado, pela imagem com digest, sem caminho local e com os segredos passados só pelo nome.
- (erro) Se um job falhar, o registro de resultados mostra esse job com a etapa e a mensagem, e o ADR não usa números dele.
- (erro) Se nenhum motor atingir as metas dos critérios 1, 2a e 2b, o ADR registra quais metas cada motor não atingiu e deixa explícita a escolha feita ou a falta dela.
- A configuração do detector na linhagem de cada job do bench é a registrada em F4.7, ou a atual se F4.7 não foi acionado.
- O digest de cada job do bench é o publicado em F4.6.T7, e o commit dessa release contém os PRs de F4.1, F4.2, F4.4, F4.5 (inclusive o commit dos limiares) e F4.7, se acionado.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F4.6.T1 | Data Science | Conferir os pré-requisitos do bench do conjunto de teste e preparar o plano de execução para aprovação | 4 | F1.3, F4.5, F4.6.T7, F3.4, F3.7 (só se acionado) |
| F4.6.T2 | DevOps | Montar o comando do bench do gate pela imagem com digest e registrá-lo em docs/hf-jobs.md | 4 | F2.2, F2.4, F1.1, F4.6.T7 |
| F4.6.T3 | MLOps | Executar um job de bench por motor na t4-small e conferir o envio dos resultados com linhagem | 6 | F4.6.T1, F4.6.T2, F2.8 |
| F4.6.T4 | Data Science | Preencher a tabela do ADR 0001 a partir das linhas TOTAL, com a unidade de cada coluna e a origem de cada número | 4 | F4.6.T3 |
| F4.6.T5 | Machine Learning | Redigir no ADR 0001 a escolha do motor de produção e do de reserva, com os motivos | 4 | F4.6.T4 |
| F4.6.T6 | QA | Conferir os números do ADR 0001 contra os CSVs e a linhagem | 4 | F4.6.T5 |
| F4.6.T7 | DevOps | Publicar por tag de release a imagem ou as imagens de motor com o código de F4.1 a F4.5 e F4.7 e registrar os digests | 3 | F2.2, F4.1, F4.2, F4.4, F4.5, F4.7 (só se acionado) |

<details><summary>F4.6.T1 · [Data Science] Conferir os pré-requisitos do bench do conjunto de teste e preparar o plano de execução para aprovação</summary>

**Objetivo:** O dono recebe um plano com motores, parâmetros, vídeos e número de jobs para aprovar.

**Passos previstos:**
1. Conferir no git a assinatura de F1.3 e o commit dos limiares de F4.5.
2. Listar os motores que ficaram depois de F4.1, F4.2 e F4.3.
3. Fixar a tag dos rótulos de teste (F3.4, ou F3.7 se acionado), a lista de exclusão (clipes 07 a 10 e concatenado), o digest de cada motor publicado em F4.6.T7, o hash dos pesos e a configuração do detector (F4.7 ou a atual).
4. Montar o plano com número de jobs, flavor t4-small e timeout, e pedir a aprovação do dono (P7).

**Definição de pronto:** O plano está anexado ao PBI com a aprovação do dono.

**Dependências:** F1.3, F4.5, F4.6.T7, F3.4, F3.7 (só se acionado)

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.6.T2 · [DevOps] Montar o comando do bench do gate pela imagem com digest e registrá-lo em docs/hf-jobs.md</summary>

**Objetivo:** O comando do gate fica documentado e é o mesmo que os jobs usam.

**Passos previstos:**
1. Escrever o comando 'hf jobs run' com a imagem pelo digest publicado em F4.6.T7, flavor t4-small, timeout, segredos só pelo nome e comando explícito do bench.
2. Apontar --corpus para a pasta do corpus e --labels para a tag dos rótulos de teste, com --excluir para os clipes 07 a 10 e o concatenado.
3. Substituir em docs/hf-jobs.md o laço atual de 'hf jobs uv run' para o bench do gate.
4. Passar pelo script de lançamento de F1.1.

**Definição de pronto:** docs/hf-jobs.md tem o comando do gate sem caminho local nem valor de segredo, e o PR cita F4.6.

**Dependências:** F2.2, F2.4, F1.1, F4.6.T7

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.6.T3 · [MLOps] Executar um job de bench por motor na t4-small e conferir o envio dos resultados com linhagem</summary>

**Objetivo:** Cada motor tem o CSV e a linhagem no repositório de resultados.

**Passos previstos:**
1. Lançar um job por motor com o comando de T2, depois da aprovação de T1.
2. Acompanhar os jobs e registrar JOB_ID, estado e duração.
3. Conferir no repositório de resultados de F2.8 o CSV, o run_log e a linhagem de cada job, inclusive o digest e a configuração do detector.
4. Registrar os jobs que falharam, com etapa e mensagem.

**Definição de pronto:** O repositório de resultados tem um CSV por motor com linhagem completa, e os jobs que falharam estão no registro.

**Dependências:** F4.6.T1, F4.6.T2, F2.8

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F4.6.T4 · [Data Science] Preencher a tabela do ADR 0001 a partir das linhas TOTAL, com a unidade de cada coluna e a origem de cada número</summary>

**Objetivo:** A tabela do ADR 0001 fica preenchida com valores iguais aos das linhas TOTAL e com a unidade declarada em cada coluna.

**Passos previstos:**
1. Copiar de cada CSV os valores de recall_ge64_max, frac_eventos_riso_ok, jitter_dp_pp, fps e custo_por_hora_video_usd.
2. Renomear a coluna 'sensibilidade (p.p.)' para 'frac_eventos_riso_ok (fração de eventos, 0 a 1)' e declarar a unidade de cada coluna: recall em fração, jitter em p.p., fps em quadros por segundo e custo em US$ por hora de vídeo.
3. Registrar a fórmula de custo usada na coluna custo/h.
4. Trazer a licença de F4.3.
5. Citar em cada número o arquivo, o JOB_ID e o digest.

**Definição de pronto:** A tabela tem uma linha por motor, a unidade em cada coluna e a origem em cada célula.

**Dependências:** F4.6.T3

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.6.T5 · [Machine Learning] Redigir no ADR 0001 a escolha do motor de produção e do de reserva, com os motivos</summary>

**Objetivo:** O ADR 0001 registra a decisão e o arquivo de onde F6.1 lê os critérios 1, 2a e 2b.

**Passos previstos:**
1. Comparar os motores pelas metas dos critérios 1, 2a e 2b, por fps, custo e licença.
2. Registrar produção e reserva, citando os números e a licença, ou registrar quais metas dos critérios 1, 2a e 2b cada motor não atingiu.
3. Indicar o arquivo e a linha dos critérios 1, 2a e 2b para F6.1.
4. Colher a aprovação de Fabio no PR.

**Definição de pronto:** O ADR 0001 tem a decisão preenchida, e o PR tem a aprovação de Fabio.

**Dependências:** F4.6.T4

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.6.T6 · [QA] Conferir os números do ADR 0001 contra os CSVs e a linhagem</summary>

**Objetivo:** Os onze critérios ficam verificados e anotados no PBI.

**Passos previstos:**
1. Baixar os CSVs do repositório de resultados e comparar cada célula da tabela com a linha TOTAL e com a unidade declarada.
2. Conferir que todos os CSVs têm a mesma lista de vídeos, sem os clipes 07 a 10 nem o concatenado.
3. Conferir as datas do primeiro job contra os commits de F1.3 e de F4.5.
4. Conferir que a configuração do detector na linhagem de cada job é a registrada em F4.7, ou a atual se F4.7 não foi acionado.
5. Conferir que o digest de cada job é o publicado em F4.6.T7 e que o commit da release contém os PRs de F4.1, F4.2, F4.4, F4.5 e F4.7 (se acionado).
6. Conferir o comando em docs/hf-jobs.md e o registro dos jobs que falharam.
7. Anotar no PBI o resultado de cada critério.

**Definição de pronto:** Os onze critérios estão marcados como passou ou não passou, com as evidências anotadas no PBI.

**Dependências:** F4.6.T5

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.6.T7 · [DevOps] Publicar por tag de release a imagem ou as imagens de motor com o código de F4.1 a F4.5 e F4.7 e registrar os digests</summary>

**Objetivo:** O bench do gate tem imagens com digest que contêm os providers adaptados, o pré-filtro corrigido, o limiar por motor calibrado e, se acionado, o detector de F4.7.

**Passos previstos:**
1. Conferir que os PRs de F4.1, F4.2, F4.4 e F4.5, inclusive o commit dos limiares de F4.5.T5, e de F4.7, se acionado, estão mesclados em main e que o CI desse commit passou.
2. Criar a tag de release nesse commit, pelo processo de publicação de F2.2 e na composição de imagem do ADR de F2.4.
3. Conferir no log do build que as imagens foram construídas com o lock de F2.1.
4. Registrar no PBI a tag, o commit e o digest de cada imagem, para F4.6.T1 e F4.6.T2.

**Definição de pronto:** O PBI tem a tag de release, o commit e o digest de cada imagem, e o workflow de publicação desse commit terminou com sucesso.

**Dependências:** F2.2, F4.1, F4.2, F4.4, F4.5, F4.7 (só se acionado)

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- bench.py:5-31,102-265,176
- docs/hf-jobs.md:4,23-29
- docs/adr/0001-motor.md:8-14
- docs/poc-gate.md:3-14,46-48
- reacao/cost.py:5
- Dockerfile:8-11
- .github/workflows/docker.yml:3-4,19-25
- https://huggingface.co/docs/hub/jobs-pricing
- https://huggingface.co/docs/hub/jobs-manage#persist-your-results
- 'hf jobs ps -a' sem resultados (2026-09-23)
- premissas P7 e P31

#### Verificação INVEST: pontos que falharam
- Independente: depende de treze PBIs.
- Small: 8 pontos, no limite de uma sprint.
- Estimável: o esforço de execução depende de quantos motores ficam na comparação.

#### Premissas
- QA entrou em relação à árvore (que previa Machine Learning, MLOps, DevOps e Data Science) porque os números do ADR precisam ser conferidos contra os CSVs e a linhagem, e a regra do épico exige task de QA.
- F1.1 entrou nas dependências do PBI porque F4.6.T2 já dependia dele e ele não chega por F1.4, que depende só de F1.3.
- O número de jobs depende de quantos motores ficam depois de F4.1, F4.2 e F4.3 (até três).
- Não existe regra pré-registrada de escolha do motor. A escolha registrada cita números e licença, e a pendência vai para F1.3.
- Se F2.4 decidir por uma imagem por motor, cada linha do ADR cita o seu digest.
- É dedução que o registro dos jobs que falharam (RN06) fica no repositório de resultados de F2.8; a confirmação é pendência da Feature com F2.8.
- A task F4.6.T7 (DevOps, disciplina já prevista na árvore para este PBI) entrou na revisão 3 para publicar a release com o código de F4.1 a F4.5 e F4.7.
- Story points e horas são sugestão, a validar no refinamento.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável, Story Points (sugestão: 8) e vínculo Parent com a Feature F4.
- F1.3: regra de escolha do motor de produção e do de reserva, a pré-registrar.
- F2.8: registro dos jobs que falharam, com etapa e mensagem (RN06).
- F6.1: arquivo e linha dos critérios 1, 2a e 2b, e o nome novo da coluna frac_eventos_riso_ok.
- F5.3 e F5.4: motor escolhido, fps na T4 e tag de release de F4.6.T7.

## Preview — PBI F4.7 (novo) · Substituir o detector, ampliar a resolução de detecção ou adotar ladrilhos quando a licença ou a medição de F4.4 exigirem

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Substituir o detector, ampliar a resolução de detecção ou adotar ladrilhos quando a licença ou a medição de F4.4 exigirem |
| Tipo | Product Backlog Item |
| Pai | F4 |
| Tags | F4; condicional; detector; ladrilhos; regra-2; visao-computacional; PBI-000D |
| Estimativa | 8 pts (sugestão); tasks: 43 h |
| Dependências | F1.1 – fixture sintética publicada no dataset privado (F1.1.T6), usada por T8 no job de sessão do detector, quando T8 assumir os critérios 6 e 13 de F2.3 (acrescentada na revisão 4), F1.6 – teste da regra 2, a estender ao detector em uso, F2.2 – processo de publicação da imagem por tag com digest, usado por T9 (acrescentada na revisão 3), F2.3.T3 – mecanismo de pesos por revisão fixa e hash (no lugar do PBI F2.3 inteiro, revisão 4), F2.8 – repositório de resultados com linhagem, exigido para números no ADR 0001 e para o critério 8 (acrescentada na revisão 3), F4.3 – licença do SCRFD e decisão de uso no piloto, F4.4 – medição e regra de acionamento, Aprovação de Fabio (P7), com flavor, duração e custo previstos, para os jobs de T7 e T8 (acrescentada na revisão 4) |
| Substitui | PBI-000D |

#### Descrição

Como integrante do time de visão computacional  
Quero implementar a opção de detecção registrada no ADR 0001 (ladrilhos com o SCRFD, det_size na largura nativa do quadro ou outro detector só de detecção) quando F4.3 ou F4.4 a exigirem  
Para que o critério 1 seja medido com um detector que o piloto possa usar e que alcance rostos de 34 a 96 px

**Contexto:** Este PBI é condicional. Ele entra se F4.3 vetar os pesos do SCRFD no piloto ou se a regra registrada em F4.4 indicar perda que o piso proporcional não resolve (P29). Enquanto a decisão sobre o enquadramento do piloto estiver pendente em F4.3, o gatilho de licença fica em espera. O detector atual é o buffalo_sc do insightface, carregado só com o módulo de detecção, com det_thresh 0,5 e um assert contra o módulo de reconhecimento (reacao/detect.py:9-18). Os modelos pré-treinados do insightface servem só para pesquisa não comercial (insightface-2.0.dist-info/METADATA:52-54). A passada plena usa det_size 1280, e o SCRFD redimensiona o quadro de 1920 px para 1280 px antes de detectar (reacao/detect.py:27; model_zoo/scrfd.py:809-819). F4.4.T3 mede det_size na largura nativa como diagnóstico. A detecção por ladrilhos está como TODO (reacao/detect.py:28, PBI-000D) e só pode ser medida depois de implementada. A agregação conta cada observação de rosto por quadro (reacao/aggregate.py:25-26), então um rosto contado duas vezes em ladrilhos sobrepostos inflaria n_mensuravel e poderia fazer uma janela passar o k-mínimo indevidamente (dedução). A detecção plena a 1280 já custa cerca de 8 vezes a de 640 (docs/poc-gate.md:42-44), e ladrilhos ou det_size maior aumentam o tempo por quadro, que entra no critério 5. Se a causa for a licença, só a troca de detector resolve, porque ladrilhos e det_size maior continuam usando os pesos do SCRFD. O critério 1 vale só para o detector medido (P31). A imagem copia o código no build (Dockerfile:8-11) e é publicada a cada tag v* (.github/workflows/docker.yml:3-4), então a opção implementada só entra na medição de T7 depois de publicada numa imagem nova. Com o veto de F4.3 ao espelhamento de det_500m.onnx, F2.3 fecha com o mecanismo (F2.3.T3) e os pesos permitidos, e os critérios 6 e 13 de F2.3 passam a este PBI (revisão 4).

**Regras de negócio:**
- RN01 – Condicional: o PBI entra só se F4.3 vetar o SCRFD no piloto ou o espelhamento de det_500m.onnx (gatilho por licença), ou se a regra de F4.4 acionar a troca.
- RN02 – A opção implementada é a registrada no ADR 0001. Se o gatilho for a licença, a opção é outro detector.
- RN03 – O detector novo faz só detecção: nenhum módulo de reconhecimento, de identidade ou de embedding (CLAUDE.md, regra 2).
- RN04 – Os pesos são carregados por revisão fixa com hash (F2.3), e a licença de cada candidato é verificada antes da escolha (F4.3).
- RN05 – Com ladrilhos, um rosto que aparece em dois ladrilhos conta uma vez.
- RN06 – A medição de F4.4 é repetida nos clipes 07 a 10 (ou nos clipes públicos de desenvolvimento usados em F4.4, se valer a P13), com os mesmos parâmetros, pela imagem publicada em F4.7.T9, e registrada no ADR 0001 com a linhagem de F2.8.
- RN07 – O tempo de detecção por quadro, antes e depois, fica registrado.
- RN08 – Nenhum clipe de teste entra nas execuções deste PBI.
- RN09 – A escolha da opção usa os números já medidos em F4.4 e não roda jobs novos. Se for preciso comparar mais de uma opção implementada, cada uma ganha uma task de protótipo antes da escolha.
- RN10 – Se F4.3 vetar o espelhamento de det_500m.onnx, os critérios 6 e 13 de F2.3 passam a este PBI: T5 publica no manifesto de pesos de F2.3 o detector escolhido, e T8 verifica, pela imagem de T9, a sessão do detector do manifesto com CUDAExecutionProvider e o teste da regra 2 com o detector carregado do arquivo do manifesto (F2.3, critérios 6 e 13).

**Fora de escopo:**
- Treinar ou ajustar um detector
- Rodar o bench no conjunto de teste (F4.6)
- Medir o critério 5 em cultos inteiros (F5.4)
- Detectores com módulo de reconhecimento acoplado

#### Critérios de aceite

- Com a opção implementada, um HF Job pela imagem publicada em F4.7.T9 sobre os clipes 07 a 10 termina com código de saída 0, e o ADR 0001 registra, ao lado dos números de F4.4, os quadros descartados e o recall_ge64_max, com o digest.
- (erro) Um teste com detecção simulada mostra que um rosto na região de sobreposição de dois ladrilhos conta uma vez (se a opção for ladrilhos).
- O teste da regra 2 cobre o detector em uso e passa com a configuração escolhida.
- (erro) O teste da regra 2 falha quando a configuração do detector pede módulo de reconhecimento ou de identidade, antes de qualquer carga e sem baixar nem carregar esse módulo (dublê do detector ou validação da configuração).
- (erro) Com um peso do detector cujo SHA-256 difere do fixado, o job falha antes do primeiro quadro.
- A linha do detector no ADR 0001 tem a licença, com fonte, e a decisão de uso no piloto vinda de F4.3.
- O registro de resultados traz o tempo de detecção por quadro com a opção anterior e com a nova.
- A configuração do detector aparece na linhagem das execuções deste PBI.
- (erro) Se nenhuma opção avaliada atender à regra de F4.4, o ADR 0001 registra os números de cada opção e diz qual detector o bench de F4.6 usa, com o motivo.
- Se F4.3 vetar o espelhamento de det_500m.onnx: o manifesto de pesos de F2.3 lista o detector escolhido com origem, revisão ou URL fixa, SHA-256, licença, decisão de espelhamento e seção do ADR 0001, e um job t4-small pela imagem de F4.7.T9, com a fixture sintética de F1.1, registra a sessão desse detector com CUDAExecutionProvider (critério 6 de F2.3).
- Se F4.3 vetar o espelhamento de det_500m.onnx: o teste da regra 2 passa com o detector carregado a partir do arquivo do manifesto (critério 13 de F2.3).

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F4.7.T1 | Visão Computacional | Listar as opções de detecção compatíveis com o gatilho e os detectores candidatos só de detecção | 3 | F4.3, F4.4 |
| F4.7.T2 | Governança e Privacidade | Verificar a licença e a ausência de módulo de reconhecimento de cada detector candidato | 4 | F4.7.T1 |
| F4.7.T3 | Visão Computacional | Escolher a opção de detecção e registrar a escolha no ADR 0001 | 3 | F4.7.T2 |
| F4.7.T4 | Visão Computacional | Implementar a opção de detecção escolhida, com contagem única de rostos entre ladrilhos | 12 | F4.7.T3, F2.8 |
| F4.7.T5 | MLOps | Hospedar os pesos do detector escolhido por revisão fixa com SHA-256 | 5 | F2.3.T3, F4.7.T3 |
| F4.7.T6 | Governança e Privacidade | Revisar a implementação do detector contra as regras 1, 2 e 6 do CLAUDE.md | 2 | F4.7.T4 |
| F4.7.T7 | Visão Computacional | Repetir a medição de F4.4 com a opção implementada e registrar o tempo por quadro | 4 | F4.7.T9, Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F4.7.T8 | QA | Estender o teste da regra 2 ao detector em uso e verificar os critérios de aceite de F4.7 | 8 | F1.6, F4.7.T6, F4.7.T7, F4.7.T5 (só se a opção for troca de detector), F4.7.T9, F1.1.T6 (só se F4.3 vetar o espelhamento de det_500m.onnx), Aprovação de Fabio (P7), com flavor, duração e custo previstos (só se F4.3 vetar o espelhamento de det_500m.onnx) |
| F4.7.T9 | DevOps | Publicar por tag de pré-release a imagem com a opção de detecção de F4.7.T4 e registrar o digest | 2 | F2.2, F4.7.T6, F4.7.T5 (só se a opção for troca de detector) |

<details><summary>F4.7.T1 · [Visão Computacional] Listar as opções de detecção compatíveis com o gatilho e os detectores candidatos só de detecção</summary>

**Objetivo:** Existe a lista de opções e de candidatos, com os números já disponíveis de F4.4, sem jobs novos.

**Passos previstos:**
1. Ler no ADR 0001 o gatilho registrado por F4.3 e F4.4.
2. Se o gatilho for a licença, listar só detectores candidatos só de detecção. Se for a medição, listar ladrilhos com o SCRFD, det_size na largura nativa e detectores candidatos.
3. Anexar os números de det_size na largura nativa medidos em F4.4.T3.
4. Entregar a lista de candidatos a F4.7.T2.

**Definição de pronto:** A lista está no PR do ADR 0001 com, por opção, o gatilho que ela atende e a origem dos números disponíveis.

**Dependências:** F4.3, F4.4

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F4.7.T2 · [Governança e Privacidade] Verificar a licença e a ausência de módulo de reconhecimento de cada detector candidato</summary>

**Objetivo:** Cada candidato tem a licença registrada para o piloto e a confirmação de que faz só detecção, antes da escolha.

**Passos previstos:**
1. Registrar a licença do código e dos pesos de cada candidato, com fonte e data, na tabela de F4.3.
2. Conferir na documentação e no código de cada candidato que ele não carrega módulo de reconhecimento nem de identidade.
3. Marcar os candidatos vetados para o piloto, com a cláusula.

**Definição de pronto:** A tabela de F4.3 no ADR 0001 tem uma linha por candidato, com licença, fonte, data e decisão de uso no piloto.

**Dependências:** F4.7.T1

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.7.T3 · [Visão Computacional] Escolher a opção de detecção e registrar a escolha no ADR 0001</summary>

**Objetivo:** O ADR 0001 registra a opção escolhida, com os números usados e a aprovação de Fabio.

**Passos previstos:**
1. Aplicar a regra de F4.4 e o resultado de F4.7.T2 às opções de F4.7.T1, sem rodar jobs novos.
2. Se a escolha exigir comparar opções ainda não implementadas, registrar no PBI uma task de protótipo por opção antes da escolha.
3. Registrar a escolha e os números usados no ADR 0001 e colher a aprovação de Fabio.

**Definição de pronto:** O ADR 0001 tem a escolha, os números usados e a aprovação de Fabio no PR.

**Dependências:** F4.7.T2

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F4.7.T4 · [Visão Computacional] Implementar a opção de detecção escolhida, com contagem única de rostos entre ladrilhos</summary>

**Objetivo:** O pipeline e o bench usam a opção escolhida, com a mesma configuração.

**Passos previstos:**
1. Implementar a opção no módulo de detecção: ladrilhos com sobreposição e supressão de duplicatas, det_size configurado ou adaptador do detector novo.
2. Manter o piso de detecção e a saída com só t, caixa e confiança por rosto.
3. Registrar a configuração do detector na linhagem de F2.8.
4. Escrever testes com detecção simulada, inclusive rosto na sobreposição.

**Definição de pronto:** Os testes passam. ruff check e pytest passam. O PR cita F4.7 e PBI-000D.

**Dependências:** F4.7.T3, F2.8

**Estimativa sugerida:** 12 h (sugestão; validar com o time)

</details>

<details><summary>F4.7.T5 · [MLOps] Hospedar os pesos do detector escolhido por revisão fixa com SHA-256</summary>

**Objetivo:** O detector novo carrega pesos com revisão e hash conferidos e fica registrado no manifesto de pesos de F2.3 (só se a opção for troca de detector).

**Passos previstos:**
1. Conforme F4.3, espelhar os pesos no repositório de modelo privado de F2.3, ou fixar a origem e o SHA-256.
2. Acrescentar ao manifesto de pesos de F2.3 a entrada do detector escolhido, com origem, revisão ou URL fixa, SHA-256, licença, decisão de espelhamento e seção do ADR 0001, no formato do critério 1 de F2.3.
3. Conferir o hash antes da carga e fazer o job falhar se ele diferir.
4. Registrar a origem, a revisão e o hash no log e na linhagem.

**Definição de pronto:** O manifesto de F2.3 tem a entrada do detector escolhido. Com um peso adulterado, o job falha antes do primeiro quadro, e com o peso correto o log mostra origem, revisão e hash.

**Dependências:** F2.3.T3, F4.7.T3

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F4.7.T6 · [Governança e Privacidade] Revisar a implementação do detector contra as regras 1, 2 e 6 do CLAUDE.md</summary>

**Objetivo:** O PR da implementação tem a aprovação da revisão de governança.

**Passos previstos:**
1. Conferir no PR de F4.7.T4 que o detector em uso não carrega módulo de reconhecimento nem de identidade.
2. Conferir que nenhuma imagem é gravada fora de /dev/shm e que a saída por rosto tem só t, caixa e confiança.
3. Aprovar o PR ou devolvê-lo com os pontos a corrigir.

**Definição de pronto:** O PR de F4.7.T4 tem a aprovação da revisão de governança.

**Dependências:** F4.7.T4

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F4.7.T7 · [Visão Computacional] Repetir a medição de F4.4 com a opção implementada e registrar o tempo por quadro</summary>

**Objetivo:** O ADR 0001 tem os números da opção implementada ao lado dos de F4.4, junto com o tempo por quadro.

**Passos previstos:**
1. Pedir ao dono aprovação dos jobs, com flavor, duração e custo previstos (P7).
2. Rodar pela imagem com o digest de F4.7.T9, nos clipes 07 a 10, as mesmas execuções de F4.4 com a opção implementada.
3. Registrar os quadros descartados, o recall_ge64_max e o tempo de detecção por quadro antes e depois.
4. Atualizar o ADR 0001.

**Definição de pronto:** O ADR 0001 tem os números e o tempo por quadro, com arquivo, JOB_ID e digest de origem.

**Dependências:** F4.7.T9, Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F4.7.T8 · [QA] Estender o teste da regra 2 ao detector em uso e verificar os critérios de aceite de F4.7</summary>

**Objetivo:** Os onze critérios ficam verificados e anotados no PBI; os dois que vêm de F2.3 só quando F4.3 vetar o espelhamento de det_500m.onnx.

**Passos previstos:**
1. Estender o teste da regra 2 de F1.6 ao detector em uso, com o caso negativo por configuração (dublê do detector ou validação antes da carga), sem baixar nem carregar módulo de reconhecimento.
2. Rodar os testes de contagem única de F4.7.T4.
3. Conferir a falha do job com peso de hash errado.
4. Conferir no ADR 0001 os números, o tempo por quadro, a licença e o registro das opções.
5. Conferir que a configuração do detector está na linhagem, que o digest dos jobs é o de F4.7.T9 e que só clipes 07 a 10 foram usados.
6. Se F4.3 vetar o espelhamento de det_500m.onnx: pedir aprovação do job t4-small, com flavor, duração e custo previstos (P7), lançá-lo pela imagem de F4.7.T9 com a fixture sintética de F1.1, conferir no log a sessão do detector do manifesto com CUDAExecutionProvider e conferir que o teste da regra 2 passa com o detector carregado do arquivo do manifesto (critérios 6 e 13 de F2.3).
7. Anotar no PBI o resultado de cada critério.

**Definição de pronto:** Os onze critérios estão marcados como passou, não passou ou não se aplica (os dois de F2.3, quando não houver veto ao espelhamento), com as evidências anotadas no PBI.

**Dependências:** F1.6, F4.7.T6, F4.7.T7, F4.7.T5 (só se a opção for troca de detector), F4.7.T9, F1.1.T6 (só se F4.3 vetar o espelhamento de det_500m.onnx), Aprovação de Fabio (P7), com flavor, duração e custo previstos (só se F4.3 vetar o espelhamento de det_500m.onnx)

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F4.7.T9 · [DevOps] Publicar por tag de pré-release a imagem com a opção de detecção de F4.7.T4 e registrar o digest</summary>

**Objetivo:** A medição de F4.7.T7 tem uma imagem com digest que contém a opção de detecção implementada e, se houver troca de detector, a carga dos pesos de F4.7.T5.

**Passos previstos:**
1. Conferir que os PRs de F4.7.T4 e, se a opção for troca de detector, de F4.7.T5 estão mesclados em main, com a aprovação de governança de F4.7.T6, e que o CI desse commit passou.
2. Criar a tag de pré-release nesse commit, pelo processo de publicação de F2.2 e na composição de imagem do ADR de F2.4.
3. Registrar no PBI a tag, o commit e o digest publicado.

**Definição de pronto:** O PBI tem a tag, o commit e o digest, e o workflow de publicação desse commit terminou com sucesso.

**Dependências:** F2.2, F4.7.T6, F4.7.T5 (só se a opção for troca de detector)

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- reacao/detect.py:9-18,27-28,34
- reacao/aggregate.py:25-31
- insightface 2.0 instalado: insightface/model_zoo/scrfd.py:809-819; insightface-2.0.dist-info/METADATA:52-54
- docs/adr/0001-motor.md:4,6
- docs/poc-gate.md:42-44
- processar_culto.py:73-76
- Dockerfile:8-11
- .github/workflows/docker.yml:3-4
- premissas P29 e P31
- F2.3, critérios 6 e 13, e F2.3.T3 no detalhamento atual de F2 (feature_det_F2.json no scratchpad); consolidacao.json, item do ciclo F2.3→F4.7

#### Verificação INVEST: pontos que falharam
- Estimável: a opção só é conhecida depois de F4.3 e F4.4.
- Independente: depende de F1.1, F2.2, F2.3.T3, F2.8, F4.3 e F4.4.
- Negociável: a opção é escolhida fora do PBI, no ADR 0001.

#### Premissas
- Disciplinas: Visão Computacional, MLOps, Governança e Privacidade e QA vêm da árvore. Machine Learning saiu: listar, escolher, implementar e medir opções de detecção é Visão Computacional pela regra de disciplinas, e nenhuma task do PBI trata motor de expressão ou limiar. O efeito do detector novo sobre os limiares fica em F4.5 (RN08). DevOps entrou pela task F4.7.T9, que publica a imagem com a opção implementada antes da medição de T7 (revisão 3).
- F1.6 entrou porque o teste da regra 2 precisa cobrir o detector em uso. F2.8 entrou porque o PBI registra números no ADR 0001 com arquivo de resultado e linhagem (RN06 da Feature), e F2.2 pela task de publicação.
- A opção det_size na largura nativa entrou pela evidência de scrfd.py:809-819. Que ela reduz a perda de rostos pequenos é hipótese que F4.4 mede como diagnóstico.
- A inflação de n_mensuravel por rosto duplicado entre ladrilhos é dedução do código de agregação.
- Se o PBI não for acionado, ele é fechado com o motivo registrado e sai das dependências de F4.5 e F4.6 (P29).
- Story points e horas são sugestão, válidos só se o PBI for acionado. Até lá a opção é desconhecida e a estimativa é incerta.
- Revisão 4: é dedução que o veto de F4.3 ao espelhamento de det_500m.onnx conta como gatilho por licença deste PBI, porque a revisão da árvore o trata assim e F2.3 passa a este PBI os critérios 6 e 13 nesse caso.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável, Story Points (sugestão: 8, se acionado) e vínculo Parent com a Feature F4. Marcar como condicional (tag 'condicional').
- F4.6: critério da configuração do detector na linhagem dos jobs do bench (movido de F4.7).
- F6.1: acrescentar a dependência de F4.7 (crítica da árvore).
- F5.4: tempo de detecção por quadro com a opção nova, para o critério 5.
- F2.8: configuração do detector na linhagem.
- F2.3: conferir que os critérios 6 e 13 dizem que, com o veto, passam a F4.7 (verificados em F4.7.T8), e que F2.3 não depende de F4.7 (revisão 4).
