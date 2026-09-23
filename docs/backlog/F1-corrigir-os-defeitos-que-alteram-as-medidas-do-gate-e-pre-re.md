[Voltar ao épico](README.md)

# Preview — Feature F1 (novo) · Corrigir os defeitos que alteram as medidas do gate e pré-registrar as regras de leitura antes do conjunto de teste

### Campos
| Campo | Conteúdo |
|---|---|
| Título | Corrigir os defeitos que alteram as medidas do gate e pré-registrar as regras de leitura antes do conjunto de teste |
| Tipo | Feature |
| Pai | Epic |
| Tags | fase-0; gate; medição; privacidade; pré-registro; qualidade |
| Estimativa | 47 pts / 151 h (soma dos PBIs, sugestão) |

### Descrição

**Problema:** As medidas do gate dependem de código com defeitos conhecidos, e as regras de leitura dos critérios ainda não foram fixadas. (1) Guarda: imprime '[guard] ok' em execução que falhou, aceita /dev/shm_x e não varre /dev/shm/reacao-in, onde o vídeo baixado fica quando o pipeline falha (issue #2; reacao/guard.py:15-16,48,68-81; processar_culto.py:30,116-118). A correção proposta na issue, baixar o vídeo dentro do diretório da guarda, faria falhar toda execução bem-sucedida com vídeo do dataset: a guarda trata como erro qualquer arquivo que sobra nesse diretório (guard.py:71-80), e o hf_hub_download com local_dir cria .cache/huggingface dentro da pasta (huggingface_hub 1.32.0, _local_folder.py:445-465). A guarda intercepta só cv2.imwrite e PIL e não restaura os originais ao sair (guard.py:19-41). (2) Lançamento: 'hf jobs uv run' envia ao bucket privado jobs-artifacts o próprio script, mesmo quando ele é dado por URL, e todo argumento que seja arquivo local, e monta tudo em /data (hf_api.py:13617-13705; cli/_uv_script_header.py:74-98; constants.py:292-293). O -v com diretório local e os volumes declarados na tabela [tool.hf-jobs] do cabeçalho do script sincronizam diretórios locais com o mesmo bucket (cli/jobs.py:96-135,239,256,692; https://huggingface.co/docs/hub/jobs-configuration#local-directories). Sem o separador '--', a CLI toma como flavor do job o --flavor escrito depois do script (--dry-run local em 2026-09-23; https://huggingface.co/docs/hub/jobs-configuration#passing-arguments). A guarda observa só o diretório de trabalho e /tmp (processar_culto.py:61). (3) Tempo: a ingestão calcula o tempo como índice/fps (reacao/ingest.py:12-21). O concatenado, com 15,0000207 quadros/s lidos pelo OpenCV, teve 31 quadros na janela 0 (out/window_aggregate.json, local, não versionado). (4) A issue #1 segue aberta, à espera da decisão sobre o commit f2d5e4a. (5) Eventos: a série descarta janelas insuficientes, então uma queda 'sustentada' e a recuperação seguinte podem juntar janelas não adjacentes, e cobertura_min é o n da terceira janela, e não o mínimo do intervalo (reacao/events.py:7-8,21-29). (6) Bench: o jitter da linha TOTAL é o maior jitter por vídeo, que exige 4 trechos neutros no mesmo vídeo e sai NaN com um trecho por clipe (bench.py:155-159,179). O bench imprime 'fps ≥ 1' enquanto o gate fixa ≤ 2 h (bench.py:261-262; docs/poc-gate.md:13). (7) run_log: envia insights_rejeitados_pelo_lint, que a migração não tem (processar_culto.py:104-106; supabase/migrations/0001_init.sql:18), e grava t4-small em execução de CPU (processar_culto.py:42; out/run_log.json, local). (8) O CI roda só o motor mock sobre vídeo sem rosto, e o teste da regra 2 citado no CLAUDE.md não existe; há só uma asserção em tempo de execução (.github/workflows/ci.yml:9-17; tests/fixtures/README.md:11-13; reacao/detect.py:17-18). Com w600k_mbf.onnx na pasta buffalo_sc, o FaceAnalysis do insightface 2.0 abre uma sessão ONNX para cada arquivo .onnx, inclusive o de reconhecimento, antes de filtrar por allowed_modules, e a asserção não percebe (insightface/app/face_analysis.py:132-140; insightface/model_zoo/model_zoo.py:121; ~/.insightface/models/buffalo_sc com det_500m.onnx e w600k_mbf.onnx nesta sessão). (9) Lint: 19 de 20 frases de sondagem com estado interno ou referência individual passam (reacao/lint.py:8-13; sondagem reproduzida em 2026-09-23). Isso infla a contagem de insights aprovados do critério 4. (10) Pré-registro: faltam as regras de leitura dos critérios 2b (meta e forma de cálculo do jitter), 3, 4 e 5 e o alvo do critério 6. docs/poc-gate.md:48 diz que 19 clipes nunca foram vistos e remete a tools/rodar_teste.sh, mas o clipe 11 e o concatenado, que contém os 23 clipes, já passaram pelo pipeline em execução local (PR #3; out/run_log.json, local). O passo 5 de tools/rodar_teste.sh roda bench.py localmente sobre os clipes fora de DEV_CLIPES, isto é, sobre o conjunto de teste (tools/rodar_teste.sh:15-16,54-56), e essa execução não aparece na listagem de jobs do HF.

**Solução proposta:** Corrigir cada defeito com teste de regressão, em sete PBIs fatiados por regra de medição. Antes de qualquer execução do bench sobre o conjunto de teste, no HF Jobs ou local, pré-registrar e assinar em docs/poc-gate.md as regras de leitura dos seis critérios (inclusive a forma de cálculo do jitter e o k-mínimo dos percentuais), a exposição já ocorrida do conjunto de teste, a composição do conjunto de teste, os vídeos permitidos em cada tipo de execução, com e sem o veto da PIB, e a regra de escolha do motor de produção e do de reserva. A revisão do pré-registro acontece depois que F3.1.T8 remove tools/rodar_teste.sh e a remissão a ele em docs/poc-gate.md, para que nenhuma edição posterior altere o documento assinado. Nenhuma task desta Feature altera tools/rodar_teste.sh, tools/preparar_rotulagem.py ou labels/README.md, que F3 remove ou reescreve. Nenhum PBI desta Feature exige job pago no HF. A verificação usa testes locais em CPU, o CI do GitHub Actions, uma pilha local do Supabase CLI e o --dry-run da CLI do HF. Os jobs de fumaça, validação e paridade leem a fixture sintética publicada no dataset privado ds-fabiopinheiro/reacao-poc-corpus por revisão fixa, sem gerá-la dentro do contêiner. O lint ampliado, com verificação só de vocabulário para textos fixos de interface, e o conjunto de frases versionado ficam prontos para o teste dos textos fixos do painel web na Vercel no CI (F5.6.T5) e para os insights exibidos no painel (F5.6, F5.7, F5.8), que é o front end do produto pela P3 revisada. Quando uma task edita arquivo que cita ID antigo do backlog, troca-o pelo ID novo (PBI-105 em docs/poc-gate.md:1 e PBI-000H em bench.py:5).

**Usuários impactados:** Fabio Pinheiro, responsável pelo gate e dono do repositório: decide sobre o commit f2d5e4a, assina as regras de leitura, declara as execuções locais sobre o conjunto de teste, confirma a exceção P26 e aprova execuções pagas, Pastor Filipe: assina as regras de leitura e o gate e lê os insights no painel web na Vercel (P3 revisada), Time de Machine Learning, Visão Computacional e Data Science, que roda o bench e lê a linha TOTAL, Responsável de governança e privacidade (encarregado ainda sem nome no épico): executa a auditoria do bucket jobs-artifacts, o registro de exposição e a lista de vídeos por tipo de execução, a condução das assinaturas, a seleção do vídeo de teste do CI e a revisão do conjunto de frases do lint

**Valor de negócio:** Os números que decidem o gate (docs/poc-gate.md:50) passam a sair de código testado e de regras escritas antes de alguém ver o resultado do conjunto de teste. Uma correção feita depois da medição invalidaria a separação entre desenvolvimento e teste (issue #1, seção 'Por que agora'; docs/poc-gate.md:46-48). A Feature também fecha três caminhos de saída de dado bruto ou de identificação: arquivo ou diretório local enviado ao bucket jobs-artifacts no lançamento, vídeo deixado em /dev/shm depois de uma falha e modelo de reconhecimento facial carregado no CI. Ela ainda impede que texto de estado interno ou de referência individual chegue ao pastor Filipe.

**Regras de negócio:**
- RN01 – Toda correção desta Feature que muda uma medida do gate entra em main antes da primeira execução do bench sobre o conjunto de teste, no HF Jobs ou local (docs/poc-gate.md:16,38-40; issue #1, seção 'Por que agora').
- RN02 – Nenhum quadro, recorte ou vídeo fica em disco fora de /dev/shm (CLAUDE.md, regra 1).
- RN03 – Nenhum modelo de reconhecimento é carregado e nenhum embedding é calculado (CLAUDE.md, regra 2).
- RN04 – Janela com menos de 10 rostos mensuráveis sai insuficiente e sem percentuais (CLAUDE.md, regra 3).
- RN05 – Todo texto para pastores passa por reacao/lint.py, inclusive o que o painel web na Vercel exibir. Texto de insight passa pela verificação completa, com minuto, momento, trecho citado e sinais (CLAUDE.md, regra 4; reacao/lint.py:23-49; P3 revisada).
- RN06 – Nenhum teste desta Feature usa áudio de plateia. Os testes com vídeo rodam sem transcrição (CLAUDE.md, regra 5).
- RN07 – Migração nova não cria campo por pessoa (CLAUDE.md, regra 6; tests/test_schema.py).
- RN08 – O lançamento de um job não envia ao Hugging Face vídeo, quadro, rótulo, arquivo do corpus nem diretório local. Em 'hf jobs uv run', só o script (processar_culto.py ou bench.py) vai ao bucket jobs-artifacts, também quando é dado por URL (hf_api.py:13619,13663-13705; cli/_uv_script_header.py:87-91; P27 refinada).
- RN09 – Mudança em reacao/guard.py, reacao/aggregate.py ou no schema do Supabase é precedida de issue que a descreve (CONTRIBUTING.md:13).
- RN10 – Toda execução paga no HF Jobs exige aprovação prévia do dono (P7). Os PBIs desta Feature são verificados sem job pago.
- RN11 – Cada PR cita o ID do PBI e passa em ruff check e pytest (CLAUDE.md, seção Estilo).
- RN12 – Execução local de pipeline ou de bench, em qualquer máquina, usa só a fixture sintética, e o vídeo licenciado de F1.6 roda só no CI do GitHub Actions (P3 revisada; P26). Só o bench de F4.6, no HF Jobs, processa clipes do conjunto de teste (F1.3).
- RN13 – Nenhum teste nem branch de verificação carrega peso de reconhecimento facial. A barreira da regra 2 é verificada com dublê do detector (CLAUDE.md, regra 2).
- RN14 – Cada arquivo tem um só destino no backlog. Nenhuma task desta Feature altera tools/rodar_teste.sh (removido em F3.1.T8), tools/preparar_rotulagem.py nem labels/README.md (retirado e reescrito em F3.5.T6) (F3 revisada).
- RN15 – Task desta Feature que edita arquivo com ID antigo do backlog troca-o pelo ID do Azure DevOps do item de destino na árvore: PBI-105 de docs/poc-gate.md:1 pelo de F6.1 (F1.3.T4) e PBI-000H de bench.py:5 pelo de F4.6 (F1.4.T1). O exemplo PBI-104 de CLAUDE.md:31 não é alterado aqui; a revisão o atribui a uma task de F2.1, com aprovação de Fabio Pinheiro (árvore, destino dos IDs antigos).

**Fora de escopo:**
- Mudança de limiares de sinal e de evento (calibração em F4.5)
- Recall pareado por IoU com caixas (docs/poc-gate.md:20-21)
- Linhagem completa por execução e envio ao repositório de resultados (F2.8); run_id no Supabase (F2.5)
- Redação legível e ordem cronológica dos insights (F5.2)
- Verificação de ausência de w600k_mbf.onnx nos jobs do HF e na imagem, e troca da origem dos pesos (F2.3). No CI, F1.6 apaga o arquivo antes do teste e do cache
- Leitura das licenças dos pesos do detector e dos motores (F4.3)
- Escolha do modo de execução dos jobs (ADR de F2.4) e reescrita dos comandos de docs/hf-jobs.md (F2.1)
- Remoção de tools/rodar_teste.sh (F3.1.T8) e retirada das cópias locais do corpus (F3.1). F1.3 depende de F3.1.T8 e nenhuma task desta Feature altera o script
- Retirada de tools/preparar_rotulagem.py e reescrita de labels/README.md:25-41, inclusive o comando da linha 36 (F3.5.T6)
- Estrutura de pastas e padrão de tags do dataset privado (F3.5.T2). F1.1.T6 usa o que F3.5.T2 definir
- Painel web na Vercel e suas telas (F5.6, F5.7, F5.8, F7.2, F7.3, F7.6, F7.8), inclusive o arquivo de textos fixos e o teste que os passa pelo lint (F5.6.T1, F5.6.T5). Esta Feature entrega o lint e as regras de leitura que ele usa
- Execução do bench sobre o conjunto de teste e medição dos critérios (F4.6, F5.4, F5.5, F5.7)
- Criação do projeto Supabase de desenvolvimento e RLS (F2.6), papéis e políticas do avaliador do gate (F5.6.T3, F5.6.T4) e perfis do piloto (F7.2, F7.8)
- Implementação do k-mínimo por percentual (F4.1.T7) e registro da escolha do motor no ADR 0001 (F4.6). F1.3 só pré-registra as regras
- Seleção e rotulagem dos clipes públicos do caminho de veto da PIB (F3.6, F3.7). F1.3 só fixa os vídeos permitidos por tipo de execução

**Dependências técnicas:**
- huggingface_hub 1.32.0 (versão instalada): comportamento de 'hf jobs run', 'hf jobs uv run', -v, [tool.hf-jobs], '--' e --dry-run (hf_api.py:13617-13790; cli/jobs.py:96-135,188-256,692,1354-1355; cli/_uv_script_header.py:74-129)
- GitHub Actions (.github/workflows/ci.yml) para os testes de regressão e o passo de integração em CPU de F1.6
- Supabase CLI com runtime compatível com Docker para a pilha local de F1.5 (https://supabase.com/docs/guides/local-development/cli-workflows)
- F2.1 (merge do PR #3 e dependências travadas) e F4.3 (licenças dos pesos) antes de F1.6
- F3.1.T8 (remoção de tools/rodar_teste.sh e da remissão em docs/poc-gate.md:47-48, sem dependência na F3 revisada) antes de F1.3.T4 e da revisão de F1.3.T5
- F3.5.T2 (estrutura de pastas e padrão de tags do dataset ds-fabiopinheiro/reacao-poc-corpus, sem dependência na F3 revisada) e F2.6.T1 (token criado pela conta dona com escopo mínimo, depois do ADR 0002 de F2.4) antes de F1.1.T6
- F1.3 assinado antes de F1.4
- Definition of Ready: decisão de Fabio Pinheiro sobre o commit f2d5e4a registrada na issue #1 e regra para contêiner sem tempo de quadro (F1.2); comportamento de job só de CPU sem --flavor (F1.5); leitura da regra 4 para textos fixos de interface (F1.7); confirmação da exceção P26 sob a P3 revisada (F1.6)
- Assinaturas de Fabio Pinheiro e do pastor Filipe e declaração datada de Fabio Pinheiro sobre execuções locais para F1.3
- Responsável de governança (encarregado ainda sem nome, conforme o épico) para F1.1.T5, F1.3.T3, F1.3.T5, F1.6.T1 e F1.7.T2
- Vídeo curto com rostos, com licença para teste e sem pessoas da congregação, para F1.6 (P18; tests/fixtures/README.md:11-13)
- IDs do Azure DevOps de F6.1 e de F4.6, gerados na sincronização da árvore, antes de F1.3.T4 e de F1.4.T1 (RN15)

**Riscos:**
- A assinatura do pastor Filipe atrasa F1.3 e, com ela, o bench do conjunto de teste (F4.6). Mitigação: preparar a proposta completa em F1.3.T1 a T4 antes de marcar a reunião.
- F3.1.T8 pertence a F3.1, PBI com dependências de governança (F3 revisada). Se F3.1.T8 não entrar na sprint de F1.3, F1.3.T4 e a revisão de F1.3.T5 esperam, e o pré-registro atrasa. Mitigação: F3.1.T8 não tem dependência, tem 3 h sugeridas e pode ser planejada na sprint de F1.3; o vínculo fica registrado no Azure DevOps.
- F3.5.T2 atrasar e bloquear F1.1.T6 e, com ela, os jobs de fumaça de F2.2. Mitigação: F3.5.T2 não tem dependência (F3 revisada).
- Não aparecer vídeo com rostos, com licença para teste e sem pessoas da congregação, o que bloqueia F1.6 (P18). Mitigação: F1.6.T1 é a primeira task do PBI.
- A licença dos pesos do insightface (só pesquisa não comercial, insightface-2.0.dist-info/METADATA:50-54) pode restringir o uso no CI. Mitigação: F1.6 depende de F4.3; se F4.3 vetar o uso no CI, F1.6 volta ao refinamento. F4.3 registra hoje três usos (PoC no HF Jobs, espelhamento e piloto; F4.3 RN03), sem o CI, e a pendência pede esse uso.
- Fabio Pinheiro pode não confirmar a exceção P26 sob a P3 revisada. Nesse caso F1.6 volta ao refinamento, porque mover o teste para um job do HF contraria a RN10.
- As origens de pesos de terceiros podem falhar no CI: tools/rodar_teste.sh:30 (commit 5176bc3) registra 403 do proxy para a URL do HSEmotion nesta sessão. Mitigação: cache de pesos no CI até F2.3, sem o modelo de reconhecimento.
- O tempo do CI cresce com os motores reais em CPU. O valor não foi medido; F1.6.T3 o registra.
- Algum contêiner de vídeo pode não informar o tempo do quadro e mudar a grade de rótulos. Mitigação: regra de fallback decidida no Definition of Ready de F1.2 e coberta por critério.
- O lint ampliado pode reprovar texto legítimo e reduzir os insights do critério 4. Mitigação: o conjunto de frases inclui os textos do modelo de frase ('atenção aparente'), citações do púlpito e frases com os mesmos termos em uso comum ('por outro lado', 'banco de dados', 'setor de mídia'), com o resultado decidido pela governança.
- Reverter f2d5e4a sem outra correção violaria a regra 3. Mitigação: o critério de F1.2 exige a regra 3 em main qualquer que seja a decisão, e a task condicional F1.2.T5 cobre a correção substituta.
- A exposição já ocorrida do conjunto de teste (concatenado com os 23 clipes) pode levar à troca do conjunto e atrasar o gate. A decisão é de F1.3.
- Em job só de CPU, ACCELERATOR vale none (https://huggingface.co/docs/hub/jobs-configuration#built-in-environment-variables). O flavor gravado depende do --flavor que o lançamento passa ao script depois de '--' (F1.1, F1.5).
- F2.6.T1 depende do ADR 0002 inteiro (F2.4). F1.1.T6 e o fechamento de F1.1 esperam o ADR. Mitigação: os jobs que leem a fixture (F2.2.T4, F2.6.T7) já dependem de F2.6.T1; F1.1.T1 a F1.1.T5 não dependem dela, e o refinamento pode separar F1.1.T4 e F1.1.T6 num PBI próprio (INVEST de F1.1).
- Com onze itens de decisão em F1.3, inclusive o k-mínimo dos percentuais, a escolha do motor e as regras de nota do critério 4 pedidos por F4 e F5, a revisão com os dois responsáveis pode exigir mais de uma reunião. Mitigação: F1.3.T1 entrega alternativas com justificativa, e item sem decisão fica pendente com responsável e data (critério de F1.3).

**Estratégia de fatiamento:** Por regra de negócio: um PBI por regra de medição afetada (guarda e lançamento, tempo do quadro e eventos, pré-registro, métricas do bench e validador, contrato do run_log e hardware, cobertura do CI, linguagem controlada). Nenhum PBI foi fatiado por camada técnica. Ordem sugerida dentro da Feature, a validar pelo time: F1.1 e F1.3 primeiro, porque a guarda é o critério 6 e o pré-registro precisa vir antes de qualquer contato com o conjunto de teste. F3.1.T8 entra na sprint de F1.3, antes de F1.3.T4, e F3.5.T2 e F2.6.T1 entram antes de F1.1.T6. Depois F1.2, F1.5 e F1.7 em paralelo, cada um com o seu Definition of Ready cumprido. Depois F1.4, que depende dos valores assinados em F1.3. Por fim F1.6, depois de F2.1 mesclar o PR #3, de F4.3 registrar as licenças e de Fabio Pinheiro confirmar a exceção P26.

### Critérios de aceite
- As issues #1 e #2 estão fechadas, cada uma com o PR ou a decisão que a fecha.
- docs/poc-gate.md traz as regras de leitura dos seis critérios, inclusive a meta e a forma de cálculo do jitter do critério 2b e o k-mínimo dos percentuais, a exposição do conjunto de teste, a composição do conjunto de teste, os vídeos permitidos por tipo de execução (jobs e execução local, com e sem o veto da PIB) e a regra de escolha do motor de produção e do de reserva, assinados por Fabio Pinheiro e pelo pastor Filipe com data anterior à primeira execução do bench sobre o conjunto de teste.
- Na data da assinatura de F1.3, tools/rodar_teste.sh não está em main, e docs/poc-gate.md não o cita.
- Nenhuma execução do bench sobre o conjunto de teste ocorreu antes da entrada em main de F1.1, F1.2, F1.4, F1.5, F1.6 e F1.7. A conferência usa a listagem de jobs do namespace, as datas dos merges e a declaração datada de Fabio Pinheiro sobre execuções locais; se alguma execução anterior existir, F1.3 a registra como exposição do conjunto de teste.
- Num teste com dados sintéticos de 4 clipes, com 1 trecho neutro e 1 riso por clipe, a linha TOTAL do bench mostra valor numérico em recall_ge64_max e frac_eventos_riso_ok, calcula jitter_dp_pp pela forma assinada em F1.3 e mostra a regra do critério 5 pré-registrada.
- O CI roda o detector, o HSEmotion e o 6DRepNet reais em CPU sobre vídeo com rostos, e falha quando o detector expõe um módulo de reconhecimento, verificado com dublê, sem carregar peso de reconhecimento. Nem a pasta de modelos no passo de integração nem o cache do CI contêm w600k_mbf.onnx.
- Nenhuma das 20 frases da sondagem, versionadas em F1.7 e medidas com o embrulho fixo versionado, passa no lint.
- O script de lançamento recusa, sem nenhuma chamada à API do HF, caminho local em --video, --corpus e --labels, qualquer argumento do script que seja arquivo local, -v de origem local e volume de origem local declarado no cabeçalho do script. A auditoria do bucket jobs-artifacts está registrada.
- A fixture sintética dos jobs de fumaça, validação e paridade está no dataset ds-fabiopinheiro/reacao-poc-corpus, com URI, revisão e SHA-256 registrados em tests/fixtures/README.md.
- Uma execução local em CPU grava o run_log numa pilha local do Supabase sem erro, com flavor 'local' e custo 0.
- Nenhum job pago foi executado para entregar esta Feature.
- docs/poc-gate.md e bench.py citam os IDs do Azure DevOps de F6.1 e de F4.6 no lugar de PBI-105 e PBI-000H.

### Alterações em relação à árvore
- Feature, usuários: o pastor Filipe lê os insights no painel web na Vercel (P3 revisada).
- Feature, problema: acrescentados três fatos conferidos na etapa anterior. (a) O -v com diretório local também sincroniza com o bucket jobs-artifacts em 'hf jobs run' (cli/jobs.py:96-135,692; hf_api.py:13715-13790; https://huggingface.co/docs/hub/jobs-configuration#local-directories). (b) A guarda não restaura os gravadores originais (guard.py:19-41). (c) docs/poc-gate.md:48 afirma que 19 clipes nunca foram vistos.
- F1.1, título: 'bloquear vídeo local' passou a 'bloquear caminho local' e, nesta revisão, a 'impedir que o lançamento e a execução dos jobs usem arquivo ou diretório local'. Isso refina a P27.
- F1.1: a barreira dentro do job passou de 'recusar vídeo lido de /data' para 'recusar caminho local em --video, --corpus e --labels quando JOB_ID estiver definido'. A guarda passa a verificar /data em job do HF.
- F1.1: acrescentada a restauração de cv2.imwrite, cv2.VideoWriter e PIL ao sair da guarda, para não quebrar tests/test_pipeline_mock.py:22-26.
- F1.2: ultimo_tempo_amostrado segue a mesma regra da ingestão (ingest.py:34-42; tools/validar_labels.py:158-169; tools/preparar_rotulagem.py:20-24). A causa dos 31 quadros é a taxa de 15,0000207 quadros/s do concatenado. O critério da issue #1 vale qualquer que seja o destino de f2d5e4a.
- F1.3: título com 'a exposição do conjunto de teste'; correção de docs/poc-gate.md:48; calibração (P8) e ferramenta de rotulagem na lista de vídeos; 'jobs do Space' passou a 'job que gera o relatório exibido no painel web na Vercel', restrito a cultos públicos (P10).
- F1.4: exclusão padrão do concatenado estendida a preparar_rotulagem.py e bench.py; validador aceita URI hf://datasets/ (labels/README.md:36).
- F1.5: em job só de CPU o flavor vem do --flavor do lançamento; a confirmação da P20 passou para uma pilha local do Supabase CLI; issue prévia de schema (CONTRIBUTING.md:13).
- F1.6: dependência de F2.1 (PR #3 e conflito onnxruntime-gpu, pyproject.toml:14-20).
- F1.7: verificação só de vocabulário por linha de comando e conjunto de frases em arquivo legível fora do Python; textos do modelo de frase no conjunto de aceitas (reacao/insights.py:8).
- Todos os PBIs: story points (Fibonacci) e horas por task como sugestões (P6).
- Revisão 2, F1.1: o download deixa de ir para dentro do diretório de resíduos sem remoção. Ele fica numa subpasta de /dev/shm/reacao que o pipeline apaga, inclusive .cache/huggingface, antes de sair do bloco da guarda, no sucesso e na falha, porque guard.py:71-80 trata sobra como erro e hf_hub_download cria .cache/huggingface (_local_folder.py:445-465). Acrescentado o critério do caminho de sucesso com download simulado e reescrito o critério de gravação em /dev/shm com o resultado para arquivo que sobra.
- Revisão 2, F1.1: o script de lançamento passa a separar com '--' as opções do Jobs do script e seus argumentos, porque sem o separador a CLI toma o --flavor do script como flavor do job (--dry-run local em 2026-09-23). O critério do --dry-run exige o valor na linha dos argumentos do script e na linha do flavor do job.
- Revisão 2, F1.1 e Feature RN08: o script recusa também qualquer argumento que seja arquivo local existente e volume local declarado em [tool.hf-jobs] (hf_api.py:13619; cli/jobs.py:239,256). A RN08 da Feature foi reescrita: em 'hf jobs uv run' só o script vai ao bucket, também quando dado por URL (cli/_uv_script_header.py:87-91). O critério 7 da Feature lista os casos recusados.
- Revisão 2, F1.1: RN13 exige comentário na issue #2 para os itens que ela não descreve (VideoWriter, restauração, /data, novo local do download) antes do commit em guard.py.
- Revisão 2, F1.1: acrescentada a task DevOps F1.1.T6, que publica a fixture sintética num dataset privado com SHA-256, porque a fixture não é versionada (tests/fixtures/README.md:3) e seria recusada como caminho local dentro dos jobs de fumaça, validação e paridade (F1.3 RN05; F2.2; F2.7). A task de QA passou a F1.1.T7. Story points sugeridos de 8 para 13.
- Revisão 2, F1.2: a decisão sobre f2d5e4a e a regra para contêiner sem tempo de quadro foram para o Definition of Ready. F1.2.T3 ficou só com a conferência da regra 3 em main e o fechamento da issue. Acrescentada a task condicional F1.2.T5 (Backend) e os critérios do fallback do tempo do quadro e da recuperação sem janela adjacente.
- Revisão 2, F1.3: a forma de cálculo do jitter da linha TOTAL entrou no item (b) de RN03, assinada com a meta. 'Execução local' entrou como tipo em RN05, com a regra de que nenhuma execução local processa clipe de teste. O critério de data usa também uma declaração datada de Fabio Pinheiro sobre execuções locais. F1.3.T4 bloqueia o passo 5 de tools/rodar_teste.sh. As definições de pronto de F1.3.T5 e F1.3.T6 não dependem mais de decisão de terceiros.
- Revisão 2, F1.4: título e critério do critério 5 cobrem os dois resultados possíveis de F1.3 (fórmula do bench ou do run_log). RN01 implementa a forma de jitter assinada. F1.4.T3 deixa de executar tools/rodar_teste.sh, que baixa o corpus privado para disco e roda o bench sobre clipes de teste (tools/rodar_teste.sh:35-40,54-56); a exclusão do concatenado é testada com arquivos sintéticos.
- Revisão 2, F1.5: o critério 7 passou a um único comportamento (sair com erro antes de abrir o vídeo), proposto para confirmação no Definition of Ready, e F1.5.T2 deixou de remeter à proposta.
- Revisão 2, F1.6: dependência de F4.3 acrescentada e leitura de licenças retirada de F1.6.T1. A barreira da regra 2 é verificada com dublê do FaceAnalysis, sem carregar w600k_mbf.onnx. O CI apaga w600k_mbf.onnx e buffalo_sc.zip antes do teste e do cache, porque o FaceAnalysis abre sessão ONNX para todo .onnx da pasta (insightface/app/face_analysis.py:132-140). O teste de integração não pode ser pulado no CI. A busca mantém --include=*.py (tools/rodar_teste.sh:33 contém 'face-emotion-recognition'). O critério da pose foi retirado e creditado a F2.1 (tests/test_pose.py do PR #3). Registrada a confirmação pendente da exceção P26 sob a P3 revisada.
- Revisão 2, F1.7: a verificação só de vocabulário ficou restrita aos textos fixos de interface; texto de insight, inclusive o editado em F7.3, passa pelo check(Insight) completo. A leitura da regra 4 vai ao Definition of Ready, com atualização do CLAUDE.md. O critério de referências a pessoa ou setor usa a lista exata do conjunto, e o conjunto ganhou frases de uso comum com resultado decidido pela governança. O embrulho da linha de base é versionado. As URLs da Vercel foram trocadas para as de projeto novo.
- Revisão 2, todos os PBIs: cada task de desenvolvimento escreve os testes dos seus critérios, e a task de QA confere antes e depois, o que remove a dependência circular entre definição de pronto e task de QA.
- Revisão 2, Feature: o responsável de governança passou a constar de forma única nas dependências e pendências (F1.1.T5, F1.3.T3, F1.3.T5, F1.6.T1, F1.7.T2), e as revisões dessas tasks são de Fabio Pinheiro.
- Revisão 3, F1.3: tools/rodar_teste.sh passou a ter um só destino, a remoção em F3.1.T8 (F3 revisada), que não tem dependência e já atualiza docs/poc-gate.md:47-48. F1.3.T4 deixou de alterar o script e passou a reescrever o parágrafo 'Separação entre desenvolvimento e teste' (docs/poc-gate.md:46-48), com a composição do conjunto de teste e a exclusão dos clipes 07 a 10 pelo --excluir do bench (bench.py:195-211), depois de F3.1.T8 e antes da revisão de F1.3.T5. Assim nenhuma edição de F3.1.T8 cai no documento já assinado (F1.3 RN07). A correção de docs/poc-gate.md:48 passou de F1.3.T3 para F1.3.T4. RN06, os critérios 5 e 7, F1.3.T6 e as premissas foram reescritos; F1.3 passou a depender de F3.1.T8.
- Revisão 3, F1.4: F1.4.T3 cobre só tools/validar_labels.py e bench.py. tools/preparar_rotulagem.py e labels/README.md:36 ficam com F3.5.T6, que retira a ferramenta e reescreve labels/README.md:25-41. RN06, RN10, os critérios 5 e 8, o contexto e a estimativa de F1.4.T3 (de 3 h para 2 h) foram ajustados. O passo de bash -n sobre tools/rodar_teste.sh saiu, porque o script é removido antes de F1.3, do qual F1.4 depende.
- Revisão 3, F1.1: a fixture dos jobs de fumaça, validação e paridade tem uma só fonte, o dataset ds-fabiopinheiro/reacao-poc-corpus lido por revisão fixa (P3 revisada). F1.1.T6 passou a depender de F3.5.T2 (pastas e padrão de tags), a usar um token fine-grained de uso único restrito ao dataset, revogado depois do envio, e a registrá-lo para o inventário de tokens de F2.6. RN11 e o critério 13 exigem a revisão; o critério 11 cobre arquivo gerado dentro do contêiner; acrescentados RN14 e o critério 15 (token). Estimativa de F1.1.T6 de 3 h para 4 h. A correção do texto de F2.6 ficou em pendências.
- Revisão 3, F1.6: as citações a tools/rodar_teste.sh:30,33 passaram a indicar o commit 5176bc3, porque F3.1.T8 remove o script.
- Revisão 3, Feature: acrescentados RN14 (um só destino por arquivo), o critério 3 (script fora de main na assinatura) e o critério 9 (fixture no dataset com revisão), as dependências de F3.1.T8 e F3.5.T2, dois riscos, duas linhas 'Revisão não aplicada' em premissas e as pendências para F2.6, F3.1.T8, F3.3 e F3.5.T2. A pendência sobre os passos 3 e 4 de tools/rodar_teste.sh saiu, porque o script é removido antes da assinatura de F1.3.
- Reconciliação, F1.1: F1.1.T6 passou a depender de F2.6.T1, e RN14, a premissa de F1.1 e a da Feature foram reescritas. O motivo anterior para não aplicar essa parte da revisão (ciclo via F2.2) caiu depois que F2 limitou a dependência de F2.6 sobre F2.2 a F2.6.T7. O token segue as regras de F5.1.T3 e F3.6.T3. O contexto e a pendência sobre a fixture gerada no contêiner passaram a listar os trechos de F2.2, F2.6 e F2.8 que ainda a descrevem.
- Reconciliação, F1.3: RN03 ganhou os itens (j), k-mínimo dos percentuais (F4.1 RN11), e (k), regra de escolha do motor (pendência de F4.6), e o item (e) passou a incluir as regras de relatórios, nota repetida, visibilidade e nota faltante que F5.7 deixa para F1.3. RN05 ganhou o caminho de veto da PIB e o acionamento de F3.6 pela falta de risos, a validação de F2.8, F4.1.T9 e F4.2.T8, a execução local só com a fixture sintética (P3 revisada; P26) e a remissão a F3.1 RN06. RN06 descreve a composição do conjunto de teste nos três casos. RN08 nova: F1.3.T4 troca PBI-105 do título pelo ID de F6.1. Título, critérios, F1.3.T1, T3, T4 e T6, estimativas (T1 de 8 h para 11 h, T3 de 4 h para 5 h, T4 de 2 h para 3 h, T6 de 2 h para 3 h) e story points (de 5 para 8) ajustados.
- Reconciliação, F1.4: F1.4.T1 troca PBI-000H da docstring de bench.py:5 pelo ID de F4.6 (RN12 e critério novos), e F1.4.T4 confere.
- Reconciliação, F1.5: a linhagem passou de F2.5 para F2.8 no fora de escopo e na RN09. RN10 e o fora de escopo apontam RLS para F2.6, papéis e políticas do avaliador para F5.6 e perfis do piloto para F7.2 e F7.8, e registram que o painel não lê run_log (D7 de F2.4.T4).
- Reconciliação, F1.6: a execução do teste de integração com o vídeo licenciado fica só no CI (RN11 nova e definições de pronto de F1.6.T2 e F1.6.T3), como F5.3 lê a P26. RN10 exige a decisão de uso no CI em F4.3. Pendências para F2.4.T4 (confirmação da exceção do CI junto da decisão da P26) e para F4.3 (uso no CI).
- Reconciliação, F1.7: RN09, F1.7.T3, F1.7.T4 e o critério 10 passam a oferecer a verificação só de vocabulário também como função pública que devolve os termos apontados, usada pelo teste de F5.6.T5 sobre o arquivo de textos fixos de F5.6.T1. A premissa sobre como o painel executa a verificação e o fora de escopo apontam para F5.6.T1 e F5.6.T5, e saíram as referências ao runtime Python da Vercel. F1.7.T3 não altera o exemplo PBI-104 de CLAUDE.md:31. Estimativa de F1.7.T3 de 7 h para 8 h.
- Reconciliação, Feature: solução, RN12 reescrita (execução local só com a fixture sintética), RN15 nova (IDs antigos), fora de escopo com F2.8, F5.6, F5.8, F7.8, F4.1.T7, F4.6, F3.6 e F3.7, dependências técnicas de F2.6.T1 e dos IDs do Azure DevOps, risco da licença para o CI ajustado e dois riscos novos, critério 2 reescrito e critério 12 novo, estratégia de fatiamento com F2.6.T1, premissas 9 a 12 reescritas e duas novas, e pendências para F2.2, F2.6, F2.8, F2.4.T4, F4.3, F5.6.T5, F6.4.T3, F3.6, F2.8.T5, F4.1.T7, F4.6.T5 e F5.7.

### Premissas
- A P3 revisada prevalece sobre P3, P9, P10 e P11 onde falam de Space para o front end do produto. O relatório, as notas do critério 4 e a revisão ficam no painel web na Vercel. Nenhum PBI desta Feature cria recurso na Vercel ou no Supabase remoto.
- A P3 revisada diz que todo processamento de vídeo roda no ambiente de desenvolvimento do HF. F1.6 processa no GitHub Actions um vídeo licenciado, sem pessoas da congregação, com os motores reais, apoiado na exceção P26 da árvore. A P3 revisada não cita a P26; a exceção precisa da confirmação de Fabio Pinheiro antes da sprint de F1.6. Sem ela, F1.6 volta ao refinamento.
- Story points e horas são sugestões, a validar no refinamento. A duração da sprint e a capacidade do time não estão registradas (P6).
- Nenhum PBI desta Feature executa job pago no HF (P7). As verificações usam testes locais em CPU, CI, a pilha local do Supabase e o --dry-run da CLI, que não envia nada (cli/jobs.py:1354-1355). A publicação da fixture sintética no dataset privado (F1.1.T6) não gera custo.
- A sondagem das 20 frases não estava versionada. Ela foi reconstruída a partir da lista do levantamento (mapa_produto, fato 20) e reproduzida em 2026-09-23 com reacao.lint.check, com cada frase dentro de um Insight válido: 19 de 20 frases passaram. O texto exato das frases originais e o embrulho usado podem diferir; F1.7.T1 versiona o embrulho.
- O PR #3 está aberto em rascunho e fora de main. F2.1 o mescla, e F1.6 depende disso. O teste tests/test_pose.py do PR #3 cobre a regressão do float() na pose; esse crédito é de F2.1.
- As disciplinas das tasks são as previstas na árvore para cada PBI, com uma exceção: Backend foi acrescentada em F1.2 para a task condicional F1.2.T5, que altera reacao/aggregate.py. F1.3.T4 fica em Data Science, com o motivo registrado em F1.3.
- Cada task de desenvolvimento escreve os testes unitários dos seus critérios. A task de QA confere que eles falham antes e passam depois, cobre casos de borda e olha o CI.
- Nesta reconciliação, os textos das outras Features são os de feature_det_F2.json a feature_det_F7.json da sessão (2026-09-23), e os problemas entre Features vêm de consolidacao.json (29 itens). Os textos de F3.1.T8, F3.5.T2 e F3.5.T6 citados continuam os da F3 revisada.
- Revisão não aplicada: dependência de F1.1.T6 no namespace de F2.4 (F2.4.T2, D4) — a P3 revisada fixa o dataset privado ds-fabiopinheiro/reacao-poc-corpus, e o ADR de F2.4 decide o namespace de Spaces, repositório de resultados, destino dos vídeos do piloto e bucket jobs-artifacts (árvore, F2.4), e não o do dataset do corpus. Com a dependência de F2.6.T1, que depende de F2.4, F1.1.T6 já vem depois do ADR 0002. Se o ADR mudar o dataset, F1.1.T6 republica a fixture e atualiza tests/fixtures/README.md.
- F1.1.T6 depende de F2.6.T1 e cria o token de uso único pela conta dona, com as regras de F5.1.T3 e F3.6.T3: escrita só no dataset, revogação depois do uso e registro no inventário de F2.6.T6 (https://huggingface.co/docs/hub/security-tokens#best-practices). A dependência não cria ciclo entre tasks: na F2 detalhada, F2.6.T1 depende só de F2.4, e F2.6 depende de F1.1 e de F2.2.T2 só em F2.6.T7. F1.1.T6 não depende de F2.6.T6, que espera o projeto Supabase de F2.6.T3, que o envio da fixture não usa.
- Plano e termos de uso da Vercel para o projeto: a confirmar (P3 revisada). A pendência está em D8 do ADR 0002 (F2.4.T4) e é tratada em F5.6 antes do uso do painel. Nenhum PBI desta Feature cria recurso na Vercel, e isso não bloqueia a Feature.
- Os IDs do Azure DevOps de F6.1 e de F4.6 existem antes de F1.3.T4 e de F1.4.T1, porque a sincronização da árvore cria todos os itens antes da sprint (pendências desta Feature).
- Execução local de pipeline ou de bench restrita à fixture sintética segue a leitura da P3 revisada e da P26 feita por F2 (RN10), F4.1 (RN10) e F5.3 (premissas): as exceções da P26 são o CI com o vídeo licenciado, o docker run com a fixture e o envio da transcrição à API da Anthropic.

### Pendências para sincronizar
- Criar a Feature no Azure DevOps como filha do Epic e preencher Area Path, Iteration Path, Responsável, Prioridade e Valor de negócio, que não estão definidos no repositório.
- Criar os 7 PBIs como filhos da Feature e as tasks como filhas de cada PBI, com a disciplina no campo Activity quando o processo o tiver.
- Registrar os IDs gerados e usar o ID do PBI no título de cada PR (CLAUDE.md, seção Estilo; CONTRIBUTING.md:20).
- Vincular a issue #2 a F1.1 e a issue #1 a F1.2 como links externos do GitHub.
- Registrar os vínculos de dependência F2.1 → F1.6, F4.3 → F1.6, F1.3 → F1.4, F3.1.T8 → F1.3.T4, F3.5.T2 → F1.1.T6 e F2.6.T1 → F1.1.T6.
- Planejar F3.1.T8 na sprint de F1.3.
- Pedir a F3.1.T8 que a atualização de docs/poc-gate.md:47-48 se limite a retirar a remissão ao script; a redação do parágrafo de separação entre desenvolvimento e teste é de F1.3.T4, porque o documento é assinado em F1.3.
- Pedir a F3.5.T2 que a estrutura de pastas do dataset inclua a pasta da fixture sintética.
- Corrigir em F2.2 (RN07, critério do único vídeo processado e F2.2.T4), F2.6 (contexto, critério do job de fumaça, dependência de F2.2.T2 e F2.6.T7) e F2.8 (RN02) a fixture gerada dentro do contêiner: nos jobs do HF ela é lida do dataset por URI hf://datasets/ com revisão (F1.1.T6), porque F1.1.T3 recusa caminho local com JOB_ID. O docker run fora do HF (F2.2.T5) pode continuar gerando a fixture, porque sem JOB_ID o caminho local é aceito (F1.1 RN10).
- Registrar no inventário de credenciais de F2.6.T6 o token de uso único de F1.1.T6, como F5.1.T3 faz com o dela.
- Avisar F3.3 de que a ferramenta de rotulagem não deve listar igreja_simples_concat.mp4. F1.4 deixa de alterar tools/preparar_rotulagem.py, que F3.5.T6 retira.
- Levar ao Definition of Ready as decisões de F1.2 (f2d5e4a e fallback do tempo do quadro), F1.5 (job de CPU sem --flavor), F1.7 (leitura da regra 4 para textos fixos) e F1.6 (confirmação da P26).
- Validar no refinamento os story points e as horas sugeridos.
- Indicar o responsável de governança (encarregado ainda sem nome) para F1.1.T5, F1.3.T3, F1.3.T5, F1.6.T1 e F1.7.T2.
- Avisar F2.3 de que, com w600k_mbf.onnx na pasta buffalo_sc, o FaceAnalysis abre sessão ONNX para o modelo de reconhecimento em toda execução com motor real, inclusive nos jobs (insightface/app/face_analysis.py:132-140).
- Plano e termos de uso da Vercel: a confirmar (P3 revisada); pendência em D8 de F2.4.T4 e em F5.6.
- Pedir a F2.4.T4 (D7), que registra a decisão de Fabio Pinheiro sobre a exceção da Anthropic na P26, que registre também a confirmação da exceção do CI com vídeo licenciado (F1.6, P18), de que F1.6 depende.
- Pedir a F4.3 (RN03 e F4.3.T3) a decisão de uso no CI do GitHub Actions para det_500m.onnx, o peso do HSEmotion e o do 6DRepNet, exigida pelo Definition of Ready de F1.6.
- Pedir a F5.6.T5 que use a função de vocabulário de F1.7.T3 em vez de acrescentar outra verificação de texto livre em reacao/lint.py, e a F6.4.T3 que avalie o mesmo reuso.
- Pedir a F3.6 que a RN03 (nenhum vídeo passa por job antes de F4.6) valha só para o conjunto de teste, porque o de desenvolvimento serve à calibração (F3.6 RN01) e à validação com o veto (F4.1 RN10), como F1.3 RN05 registra.
- F2.8.T5 altera docs/poc-gate.md depois da assinatura de F1.3. Pela RN07 de F1.3, isso exige nova assinatura; decidir no refinamento se o mapa de arquivo e coluna vai para outro documento.
- Avisar F4.1.T7, F4.6.T5 e F5.7 de que as regras de k-mínimo por percentual, de escolha do motor e de notas do critério 4 ficam nos itens (j), (k) e (e) de F1.3 RN03.

## Preview — PBI F1.1 (novo) · Corrigir as três falhas da guarda da issue #2 e impedir que o lançamento e a execução dos jobs usem arquivo ou diretório local

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Corrigir as três falhas da guarda da issue #2 e impedir que o lançamento e a execução dos jobs usem arquivo ou diretório local |
| Tipo | Product Backlog Item |
| Pai | F1 |
| Tags | fase-0; gate; critério-6; regra-1; hf-jobs; issue-2 |
| Estimativa | 13 pts (sugestão); tasks: 33 h |
| Dependências | F3.5.T2 (estrutura de pastas e padrão de tags do dataset), só para F1.1.T6, F2.6.T1 (token criado pela conta dona com escopo mínimo, depois do ADR 0002), só para F1.1.T6 |
| Substitui | issue #2 |

#### Descrição

Como Fabio Pinheiro, responsável pelo gate e pelos jobs no Hugging Face  
Quero que a guarda de não-persistência informe sucesso só quando a execução termina bem, bloqueie gravação de imagem e de vídeo fora de /dev/shm e não deixe o vídeo baixado em /dev/shm, com ou sem falha. Quero também que nenhum job receba vídeo, rótulo, arquivo do corpus ou diretório local, nem no lançamento nem dentro do contêiner  
Para que o critério 6 do gate meça a guarda corrigida e que nenhum dado local seja copiado para o bucket jobs-artifacts ao lançar um job

**Contexto:** A guarda (reacao/guard.py) é o critério 6 do gate (docs/poc-gate.md:14). A issue #2, aberta pelo dono em 2026-09-07, lista três falhas. (1) O print final está no finally e sai também em execução que falhou (guard.py:68-81). (2) _allowed compara prefixo de texto e aceita /dev/shm_x (guard.py:15-16); o mesmo prefixo aparece no filtro de _snapshot (guard.py:48). (3) O vídeo baixado vai para /dev/shm/reacao-in, fora do diretório que a guarda varre, e só é apagado no caminho de sucesso (processar_culto.py:30,116-118). A issue propõe baixar para dentro do shm_dir, 'que já é varrido e limpo'. Mas a guarda trata qualquer arquivo que sobra em /dev/shm/reacao como resíduo: apaga e levanta PersistenceViolation, também em execução bem-sucedida (guard.py:71-80). tests/test_guard.py:24-27 apaga o arquivo antes de sair do bloco por isso. O hf_hub_download com local_dir cria .cache/huggingface (metadados, .lock, .gitignore, CACHEDIR.TAG) dentro da pasta de destino (huggingface_hub 1.32.0: file_download.py:903-906; _local_folder.py:249-259,445-465). O teste de ponta a ponta usa a fixture por caminho local, sem download (tests/test_pipeline_mock.py:30-36). A guarda troca cv2.imwrite e Image.save e nunca restaura os originais (guard.py:19-41). cv2.VideoWriter não é interceptado, e tests/test_pipeline_mock.py:22-26 grava a fixture com ele no mesmo processo da suíte. No lançamento, 'hf jobs uv run' envia ao bucket privado {namespace}/jobs-artifacts o script e todo argumento que seja arquivo local, e os monta em /data (hf_api.py:13617-13705; constants.py:292-293). Um script dado por URL é baixado e enviado como script local (cli/_uv_script_header.py:74-98). O -v com diretório local sincroniza o diretório com o mesmo bucket em 'hf jobs run' e em 'hf jobs uv run' (cli/jobs.py:96-135,256,692; https://huggingface.co/docs/hub/jobs-configuration#local-directories). Volumes declarados na tabela [tool.hf-jobs] do cabeçalho PEP 723 do script são somados aos do -v (cli/jobs.py:239; cli/_uv_script_header.py:129; https://huggingface.co/docs/hub/jobs-configuration#define-the-launch-config-in-the-script). Um --dry-run local em 2026-09-23 de 'hf jobs uv run --flavor cpu-basic s.py --video hf://... --flavor t4-small' mostrou 'flavor t4-small' e os argumentos do script sem --flavor; com '--' antes do script, os argumentos mantiveram --flavor e o job ficou em cpu-basic (https://huggingface.co/docs/hub/jobs-configuration#passing-arguments). O --dry-run não envia nada (cli/jobs.py:1354-1355). A guarda observa só o diretório de trabalho e /tmp (processar_culto.py:61). Todo job do HF recebe a variável JOB_ID (https://huggingface.co/docs/hub/jobs-configuration#built-in-environment-variables). A fixture sintética não é versionada e é gerada a cada execução (tests/fixtures/README.md:3). Em 2026-09-23, a listagem de hf://buckets/ds-fabiopinheiro veio vazia. A P3 revisada fixa o dataset privado ds-fabiopinheiro/reacao-poc-corpus. Na F3 revisada, F3.5.T2 define a estrutura de pastas e o padrão de tags do dataset, e F3.5.T4 passa a exigir revisão nas leituras do dataset em bench.py e processar_culto.py. Na F2 detalhada, F2.2 (RN07 e F2.2.T4), F2.6 (contexto, dependência de F2.2.T2 e F2.6.T7) e F2.8 (RN02) ainda descrevem a fixture gerada dentro do contêiner em /dev/shm, o que RN08 recusaria, porque o arquivo gerado é caminho local. F2.6.T1 cria os tokens de escopo mínimo pela conta dona e depende só de F2.4. F5.1.T3 e F3.6.T3 criam por esse procedimento tokens de escrita de uso único no dataset e os registram no inventário de F2.6.T6.

**Regras de negócio:**
- RN01 – A mensagem '[guard] ok' aparece só quando o bloco protegido termina sem exceção. A verificação de arquivos novos e a limpeza de /dev/shm continuam acontecendo também na falha (issue #2, item 1).
- RN02 – Um caminho conta como memória compartilhada só se for /dev/shm ou estiver dentro de /dev/shm/, com separador (issue #2, item 2).
- RN03 – O vídeo baixado do dataset fica numa subpasta de /dev/shm/reacao. O pipeline apaga essa subpasta inteira, inclusive .cache/huggingface, antes de sair do bloco da guarda, no sucesso e na falha. O que sobrar é tratado pela guarda como resíduo: é apagado e a execução sai com erro (guard.py:71-80).
- RN04 – Dentro da guarda, gravação de imagem (cv2.imwrite, PIL) e de vídeo (cv2.VideoWriter) fora de /dev/shm é bloqueada. Ao sair da guarda, os três voltam ao comportamento original.
- RN05 – O script de lançamento recusa, antes de qualquer chamada à API do HF: caminho local em --video, --corpus e --labels; qualquer argumento do script que seja arquivo local existente (o mesmo teste Path.is_file() da CLI, hf_api.py:13619); -v cuja origem não seja URI hf://; volume de origem local declarado em [tool.hf-jobs] do script.
- RN06 – O script de lançamento separa com '--' as opções do Jobs do script e seus argumentos, e passa ao script o mesmo --flavor do job. F1.5 usa esse valor em job só de CPU, em que ACCELERATOR vale none.
- RN07 – O script de lançamento aceita como script só processar_culto.py ou bench.py, por caminho do repositório ou por URL. Em 'hf jobs uv run', esse script é o único arquivo que vai ao bucket jobs-artifacts (hf_api.py:13619,13663-13705).
- RN08 – Dentro de um job do HF (JOB_ID definido), processar_culto.py e bench.py aceitam vídeo, corpus e rótulos só por URI hf:// de origem permitida. A lista começa com hf://datasets/ e fica num único lugar, para F7.1 acrescentar a origem dos vídeos do piloto.
- RN09 – Em job do HF, a guarda também verifica /data quando o diretório existir.
- RN10 – Fora do HF (sem JOB_ID), caminho local continua aceito, para a fixture sintética do CI e do teste de ponta a ponta.
- RN11 – Os jobs de fumaça, validação e paridade leem a fixture sintética por URI hf://datasets/ do dataset ds-fabiopinheiro/reacao-poc-corpus, com revisão fixa e SHA-256 registrados em tests/fixtures/README.md. Nenhum job gera a fixture dentro do contêiner, porque RN08 recusa caminho local com JOB_ID (F1.3 RN05; F2.2; F2.7).
- RN12 – Apagamento no bucket jobs-artifacts só com aprovação do dono, porque em Storage Buckets o apagamento é imediato e permanente (P30; https://huggingface.co/docs/hub/storage-buckets).
- RN13 – Toda mudança em reacao/guard.py cita a issue #2. Os itens que a issue não descreve (interceptação do VideoWriter, restauração dos gravadores, /data nas raízes, novo local e remoção do download) são acrescentados a ela em comentário antes do commit (CONTRIBUTING.md:13).
- RN14 – O envio da fixture ao dataset usa um token fine-grained com escrita só nesse dataset, criado pela conta dona pelo procedimento de F2.6.T1, como exceção de uso único à política de F2.6, com as mesmas regras de F5.1.T3 e F3.6.T3, e revogado depois do envio. Nome, escopo e datas vão para o inventário de credenciais de F2.6.T6 (https://huggingface.co/docs/hub/security-tokens#best-practices).

**Fora de escopo:**
- Escolha entre 'hf jobs run' e 'hf jobs uv run' para os jobs do gate (ADR de F2.4)
- Reescrita dos comandos de docs/hf-jobs.md (F2.1)
- Origem dos vídeos do piloto e sua inclusão na lista de origens permitidas (F7.1)
- Disponibilizar por URI hf:// os vídeos públicos de docs/corpus.csv (F5.1)
- Estrutura de pastas e padrão de tags do dataset (F3.5.T2)
- Novas extensões na lista IMAGE_EXT da guarda (guard.py:8)
- Execução de job no HF para exercitar a barreira. Os jobs de fumaça de F2.2 usam o script e a fixture publicada depois

#### Critérios de aceite

- Quando o pipeline falha depois de um download simulado de hf://datasets/, a saída não contém '[guard] ok', o código de saída é diferente de 0 e nenhum arquivo do download, inclusive .cache/huggingface, fica em /dev/shm ao fim.
- Quando o pipeline termina sem erro depois de um download simulado de hf://datasets/, a saída contém '[guard] ok', o código de saída é 0 e nenhum arquivo do download, inclusive .cache/huggingface, fica em /dev/shm ao fim.
- Dentro da guarda, gravar imagem em /dev/shm_x/arquivo.jpg ou em /dev/shmfoo/arquivo.jpg é bloqueado com erro de persistência.
- Dentro da guarda, gravar vídeo pelo OpenCV fora de /dev/shm é bloqueado com erro de persistência.
- Dentro da guarda, gravar vídeo pelo OpenCV em /dev/shm/reacao e apagá-lo antes do fim do bloco termina sem erro. Se o arquivo sobrar ao fim do bloco, a guarda o apaga e sai com erro de resíduo.
- Depois que a guarda termina, gravar imagem e vídeo fora de /dev/shm no mesmo processo volta a funcionar, e a suíte completa de testes passa.
- Uma execução bem-sucedida com a fixture local continua imprimindo '[guard] ok' (tests/test_pipeline_mock.py:36), e o passo do CI do critério 6 passa.
- O script de lançamento, chamado com caminho local em --video, --corpus ou --labels, com qualquer argumento do script que seja arquivo local existente ou com -v de origem local, sai com erro que nomeia o argumento. Nenhuma chamada à API do HF é feita (criação de bucket, envio de arquivo, sincronização de volume ou criação de job).
- O script de lançamento, chamado com um script cujo cabeçalho declara em [tool.hf-jobs] um volume de origem local, sai com erro que nomeia o volume, sem chamada à API do HF.
- O script de lançamento, chamado com URI hf://datasets/ e --dry-run, imprime um comando com '--' entre as opções do Jobs e o script. A saída do --dry-run da CLI mostra --flavor <valor> na linha dos argumentos do script e o mesmo valor na linha do flavor do job, e nenhum job é criado.
- Com JOB_ID definido, processar_culto.py e bench.py recusam --video, --corpus ou --labels com caminho local, inclusive sob /data ou num arquivo gerado dentro do contêiner, antes de abrir o arquivo, e saem com código diferente de 0.
- Sem JOB_ID, o pipeline aceita a fixture sintética por caminho local, como hoje.
- A fixture sintética está no dataset ds-fabiopinheiro/reacao-poc-corpus, na pasta definida em F3.5.T2, e tests/fixtures/README.md registra a URI hf://datasets/, a revisão e o SHA-256. O arquivo baixado com essa revisão tem o mesmo SHA-256, e o script de lançamento aceita a URI no --dry-run.
- O registro da auditoria do bucket jobs-artifacts lista cada namespace verificado, a data e o conteúdo encontrado. Se houver arquivo, o registro traz o apagamento e a aprovação do dono.
- O token usado para enviar a fixture é fine-grained, com escrita só no dataset, e está revogado. O PR registra nome, escopo e datas de criação e de revogação, e o registro é entregue ao inventário de credenciais de F2.6.T6.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F1.1.T1 | Backend | Corrigir em reacao/guard.py e processar_culto.py as três falhas da issue #2 | 5 | — |
| F1.1.T2 | Backend | Interceptar a gravação de vídeo fora de /dev/shm e restaurar os gravadores ao sair da guarda | 3 | — |
| F1.1.T3 | Backend | Recusar caminho local dentro de job do HF e verificar /data na guarda | 5 | — |
| F1.1.T4 | DevOps | Criar o script de lançamento de jobs que recusa dado local e repassa o flavor depois de '--' | 8 | — |
| F1.1.T5 | Governança e Privacidade | Auditar o bucket jobs-artifacts dos namespaces usados e registrar o resultado | 2 | — |
| F1.1.T6 | DevOps | Publicar a fixture sintética no dataset ds-fabiopinheiro/reacao-poc-corpus, na pasta definida em F3.5.T2, com revisão fixa e SHA-256 | 4 | F1.1.T4, F3.5.T2, F2.6.T1 |
| F1.1.T7 | QA | Verificar os critérios de aceite da guarda e do lançamento | 6 | F1.1.T1, F1.1.T2, F1.1.T3, F1.1.T4, F1.1.T5, F1.1.T6 |

<details><summary>F1.1.T1 · [Backend] Corrigir em reacao/guard.py e processar_culto.py as três falhas da issue #2</summary>

**Objetivo:** A guarda imprime '[guard] ok' só no sucesso, compara caminhos com separador, e o vídeo baixado fica numa subpasta de /dev/shm/reacao que o pipeline apaga antes de sair do bloco, no sucesso e na falha.

**Passos previstos:**
1. Comentar na issue #2, antes do commit, que o item 3 muda de solução: o download fica numa subpasta de /dev/shm/reacao e é apagado pelo pipeline antes da checagem de resíduos, porque guard.py:71-80 trata sobra como erro e o hf_hub_download cria .cache/huggingface na pasta.
2. Mover o print final para o caminho sem exceção (else), mantendo a verificação de arquivos novos e a limpeza de /dev/shm no finally (guard.py:68-81).
3. Trocar a comparação de prefixo por comparação com separador em _allowed e no filtro de _snapshot (guard.py:16,48).
4. Fazer resolve_video baixar para uma subpasta do diretório devolvido por no_persistence e envolver o processamento em try/finally, dentro do bloco da guarda, que apaga a subpasta inteira, inclusive .cache/huggingface.
5. Retirar a limpeza manual de /dev/shm/reacao-in (processar_culto.py:116-118).
6. Escrever os testes unitários: falha forçada depois de download simulado, execução sem erro depois de download simulado, e gravação em /dev/shm_x e /dev/shmfoo.

**Definição de pronto:** Os testes escritos na task passam; tests/test_guard.py e tests/test_pipeline_mock.py passam; ruff check sem erro; o comentário na issue #2 tem data anterior ao commit.

**Dependências:** nenhuma

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F1.1.T2 · [Backend] Interceptar a gravação de vídeo fora de /dev/shm e restaurar os gravadores ao sair da guarda</summary>

**Objetivo:** Dentro da guarda, cv2.VideoWriter segue a mesma regra de caminho de cv2.imwrite e PIL. Ao sair, os três voltam ao original.

**Passos previstos:**
1. Comentar na issue #2, antes do commit, a interceptação do VideoWriter e a restauração dos gravadores (CONTRIBUTING.md:13).
2. Envolver a criação e a abertura de cv2.VideoWriter com a mesma checagem de caminho de _allowed.
3. Guardar as referências originais de cv2.imwrite, cv2.VideoWriter e Image.Image.save antes de trocá-las e restaurá-las no finally.
4. Escrever os testes: vídeo em tmp_path bloqueado; vídeo em /dev/shm/reacao apagado antes do fim sem erro; vídeo que sobra em /dev/shm/reacao apagado pela guarda com erro de resíduo; tests/fixtures/gerar_curto.py gravando em tmp_path no mesmo processo depois do bloco.

**Definição de pronto:** Os testes escritos na task passam; a suíte completa passa; ruff check sem erro; o comentário na issue #2 tem data anterior ao commit.

**Dependências:** nenhuma

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F1.1.T3 · [Backend] Recusar caminho local dentro de job do HF e verificar /data na guarda</summary>

**Objetivo:** Com JOB_ID definido, processar_culto.py e bench.py aceitam entrada só por URI hf:// permitida, e a guarda inclui /data nas raízes verificadas.

**Passos previstos:**
1. Comentar na issue #2, antes do commit em guard.py, a inclusão de /data nas raízes (CONTRIBUTING.md:13).
2. Criar uma lista única de prefixos permitidos, começando por hf://datasets/.
3. Em processar_culto.py e bench.py, validar --video, --corpus e --labels contra a lista quando JOB_ID estiver definido, antes de abrir qualquer arquivo.
4. Emitir mensagem de erro que nomeia o argumento e sair com código diferente de 0.
5. Incluir /data nas raízes da guarda quando JOB_ID estiver definido e o diretório existir.
6. Escrever os testes com JOB_ID simulado: /data/x.mp4, caminho relativo e arquivo gerado em tmp_path recusados, hf://datasets/... aceito, nos dois scripts.

**Definição de pronto:** Os testes escritos na task passam; sem JOB_ID, o passo do CI com a fixture sintética passa; ruff check sem erro.

**Dependências:** nenhuma

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F1.1.T4 · [DevOps] Criar o script de lançamento de jobs que recusa dado local e repassa o flavor depois de &#x27;--&#x27;</summary>

**Objetivo:** Existe em tools/ um script que monta o comando do HF Jobs com '--' e recusa, antes de qualquer chamada à API, caminho local, argumento que seja arquivo local e volume de origem local, inclusive o declarado no cabeçalho do script.

**Passos previstos:**
1. Receber tipo de job, flavor, timeout e argumentos do pipeline, e montar 'hf jobs run' ou 'hf jobs uv run' com '--' entre as opções do Jobs e o script com seus argumentos.
2. Aceitar como script só processar_culto.py ou bench.py, por caminho do repositório ou URL, e registrar no cabeçalho que em 'hf jobs uv run' o script vai ao bucket jobs-artifacts mesmo quando dado por URL.
3. Antes de importar HfApi ou chamar a CLI, recusar caminho local em --video, --corpus e --labels, qualquer argumento que seja arquivo local existente e -v cuja origem não comece com hf://.
4. Ler a tabela [tool.hf-jobs] do cabeçalho PEP 723 do script e recusar volume de origem local.
5. Passar ao script --flavor com o mesmo valor do flavor do job.
6. Oferecer --dry-run que repassa --dry-run à CLI e não cria job.
7. Escrever os testes com a API simulada (zero chamadas nos casos recusados) e um teste com o --dry-run da CLI que confere --flavor nos argumentos e no flavor do job.

**Definição de pronto:** Os testes escritos na task passam; nos casos recusados a API simulada registra zero chamadas; o --dry-run com URI hf:// mostra o mesmo --flavor nos argumentos do script e no flavor do job; nenhum job é criado.

**Dependências:** nenhuma

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F1.1.T5 · [Governança e Privacidade] Auditar o bucket jobs-artifacts dos namespaces usados e registrar o resultado</summary>

**Objetivo:** Fica registrado se algum arquivo local já foi enviado ao bucket jobs-artifacts e, se houver, que foi apagado com aprovação do dono.

**Passos previstos:**
1. Listar os buckets de ds-fabiopinheiro e, se o ADR de F2.4 escolher organização, os do namespace da organização, sem criar recurso.
2. Se jobs-artifacts existir, listar o conteúdo e procurar vídeo, quadro, rótulo ou arquivo do corpus.
3. Se houver, pedir aprovação de Fabio Pinheiro, apagar e registrar a aprovação.
4. Registrar data, namespaces e resultado no PR do PBI e na issue #2.

**Definição de pronto:** O registro traz data, namespaces verificados e conteúdo encontrado ('nenhum bucket jobs-artifacts', se for o caso) e está revisado por Fabio Pinheiro.

**Dependências:** nenhuma

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F1.1.T6 · [DevOps] Publicar a fixture sintética no dataset ds-fabiopinheiro/reacao-poc-corpus, na pasta definida em F3.5.T2, com revisão fixa e SHA-256</summary>

**Objetivo:** Os jobs de F2.2 e F2.7 leem a fixture sintética por uma URI hf://datasets/ com revisão e SHA-256 registrados, sem caminho local e sem gerar a fixture dentro do contêiner.

**Passos previstos:**
1. Conferir em F3.5.T2 a pasta e o padrão de tag definidos para a fixture.
2. Gerar a fixture com tests/fixtures/gerar_curto.py e calcular o SHA-256.
3. Criar, pela conta dona e pelo procedimento de F2.6.T1, um token fine-grained com escrita só no dataset ds-fabiopinheiro/reacao-poc-corpus, para este envio, como F5.1.T3 e F3.6.T3.
4. Enviar a fixture à pasta definida e registrar a revisão do envio (commit ou tag no padrão de F3.5.T2).
5. Revogar o token e registrar no PR nome, escopo e datas de criação e de revogação, para o inventário de credenciais de F2.6.T6.
6. Registrar URI hf://datasets/, revisão e SHA-256 em tests/fixtures/README.md.
7. Conferir que o --dry-run do script de lançamento aceita a URI e que o arquivo baixado para /dev/shm com essa revisão tem o SHA-256 registrado.

**Definição de pronto:** tests/fixtures/README.md traz URI, revisão e SHA-256; o arquivo baixado com a revisão tem o mesmo SHA-256; o --dry-run do script de lançamento aceita a URI; o PR registra o token usado, com escopo e data de revogação.

**Dependências:** F1.1.T4, F3.5.T2, F2.6.T1

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F1.1.T7 · [QA] Verificar os critérios de aceite da guarda e do lançamento</summary>

**Objetivo:** Cada critério de aceite de F1.1 tem teste automatizado ou evidência registrada, e os testes de regressão falham sem as correções.

**Passos previstos:**
1. Rodar os testes escritos em F1.1.T1 a T4 no commit anterior às correções e no commit final e registrar que falham antes e passam depois.
2. Acrescentar casos de borda: /dev/shm/../tmp/x.jpg dentro da guarda, argumento de arquivo local com espaço no nome e -v com :rw.
3. Conferir o passo do CI do critério 6 e tests/test_pipeline_mock.py no PR.
4. Conferir o registro da auditoria (F1.1.T5), a URI, a revisão e o SHA-256 da fixture e a revogação do token (F1.1.T6).

**Definição de pronto:** Registro no PR com o resultado de cada critério de aceite; os testes falham no commit anterior e passam no final (verificado nos dois commits); CI verde.

**Dependências:** F1.1.T1, F1.1.T2, F1.1.T3, F1.1.T4, F1.1.T5, F1.1.T6

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- issue #2 (https://github.com/ds-fabiopinheiro/church-sentiment-analysis/issues/2), item 3 com a proposta 'baixar para dentro do shm_dir'
- reacao/guard.py:7-16,19-41,44-53,56-81
- processar_culto.py:23-31,61,116-118
- tests/test_guard.py:20-27
- tests/test_pipeline_mock.py:22-36
- tests/fixtures/README.md:3,11-13
- huggingface_hub 1.32.0 instalado: hf_api.py:13617-13713 e 13715-13790; constants.py:292-293; cli/jobs.py:96-135,188-256,692,1354-1355; cli/_uv_script_header.py:74-129; file_download.py:903-906; _local_folder.py:249-259,445-465
- --dry-run local de 'hf jobs uv run' com e sem '--' em 2026-09-23 (sem envio)
- https://huggingface.co/docs/hub/jobs-configuration#passing-arguments
- https://huggingface.co/docs/hub/jobs-configuration#define-the-launch-config-in-the-script
- https://huggingface.co/docs/hub/jobs-configuration#local-directories
- https://huggingface.co/docs/hub/jobs-configuration#built-in-environment-variables
- https://huggingface.co/docs/hub/security-tokens#best-practices
- Listagem hf://buckets/ds-fabiopinheiro em 2026-09-23: vazia
- docs/poc-gate.md:14
- CONTRIBUTING.md:13
- F3.5.T2 e F3.5.T4 (F3 revisada)
- feature_det_F2.json da sessão: F2.2 RN07 e F2.2.T4, F2.6 (dependências, contexto e F2.6.T7), F2.8 RN02 e F2.6.T1 (dependência só de F2.4)
- Premissas P27 e P30 da árvore; P3 revisada (dataset ds-fabiopinheiro/reacao-poc-corpus)
- feature_det_F5.json e feature_det_F3.json da sessão: F5.1.T3, F5.1.T5 e F3.6.T3 (token de escrita de uso único no dataset)

#### Verificação INVEST: pontos que falharam
- Small: com 13 story points sugeridos, o PBI pode não caber numa sprint. O candidato à divisão é o lançamento (F1.1.T4 e F1.1.T6). Como a Feature já tem 7 PBIs, o PBI novo iria para F2, junto de F2.1, que reescreve os comandos; a decisão é do refinamento.
- Independente: o modo padrão do script depende do ADR de F2.4. A dependência foi contornada com o suporte aos dois modos.
- Independente: F1.1.T6 depende de F3.5.T2 e de F2.6.T1, tasks de outras Features. F3.5.T2 não tem dependência, e F2.6.T1 depende de F2.4.

#### Premissas
- Estimativas (story points e horas) são sugestão, a validar no refinamento.
- O local do download (subpasta de /dev/shm/reacao removida pelo pipeline antes da checagem de resíduos) difere da proposta da issue #2. A escolha segue guard.py:71-80, que trata sobra como erro, e mantém a guarda como segunda barreira. F1.1.T1 registra a mudança na issue.
- O script de lançamento aceita os dois modos ('hf jobs run' e 'hf jobs uv run') até o ADR de F2.4 escolher o modo do gate. Assim a task não espera a decisão.
- O nome e o caminho do script de lançamento em tools/ são decisão da task. Não há nome definido no repositório.
- A fixture sintética não tem rosto (tests/fixtures/README.md:11-13), então publicá-la no dataset privado não expõe dado pessoal. O dataset é ds-fabiopinheiro/reacao-poc-corpus (P3 revisada), e a pasta segue a estrutura de F3.5.T2.
- O nome da pasta da fixture não está definido no repositório nem em F3.5.T2. A pendência vai a F3.5.T2.
- F1.1.T6 depende de F2.6.T1. Não há ciclo entre tasks: F2.6.T1 depende só de F2.4, e F2.6 depende de F1.1 só em F2.6.T7 (F2 detalhada). F1.1.T6 não depende de F2.6.T6, que espera o projeto Supabase de F2.6.T3; o registro do token no inventário fica em pendência.
- Os vídeos públicos de docs/corpus.csv só podem ser usados em job depois de disponíveis por URI hf://datasets/. A árvore atribui o registro desses vídeos a F5.1 (índice de PBIs).
- bench.py já apaga /dev/shm/reacao-bench no finally (bench.py:233-234). A issue #2 não pede que a guarda varra esse diretório.
- A auditoria usa só listagem, sem custo. Se o ADR de F2.4 escolher namespace de organização, a auditoria cobre também esse namespace.
- Os testes de download usam hf_hub_download simulado, que grava o arquivo e .cache/huggingface na pasta de destino, e não acessam o dataset privado.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável no Azure DevOps
- Vincular a issue #2 ao PBI e citar o ID do PBI no título do PR
- Vínculo de dependência F3.5.T2 → F1.1.T6 no Azure DevOps
- Vínculo de dependência F2.6.T1 → F1.1.T6 no Azure DevOps
- Pedir a F3.5.T2 a pasta da fixture sintética na estrutura do dataset
- Registrar o token de uso único de F1.1.T6 no inventário de credenciais de F2.6.T6
- Corrigir em F2.2 (RN07 e F2.2.T4), F2.6 (contexto, dependência de F2.2.T2 e F2.6.T7) e F2.8 (RN02) o texto que diz que a fixture é gerada dentro do contêiner nos jobs do HF
- Responsável de governança para F1.1.T5
- Validar os 13 story points sugeridos e decidir no refinamento se o PBI é dividido

## Preview — PBI F1.2 (novo) · Corrigir o tempo dos quadros, fechar a issue #1 e exigir janelas adjacentes nos eventos sustentados

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Corrigir o tempo dos quadros, fechar a issue #1 e exigir janelas adjacentes nos eventos sustentados |
| Tipo | Product Backlog Item |
| Pai | F1 |
| Tags | fase-0; gate; critério-1; critério-2; eventos; issue-1 |
| Estimativa | 5 pts (sugestão); tasks: 20 h |
| Dependências | nenhuma |
| Substitui | issue #1 |

#### Descrição

Como membro do time de Machine Learning e Visão Computacional que roda o bench  
Quero que cada quadro amostrado tenha o tempo real do vídeo, que a issue #1 tenha decisão registrada e que um evento sustentado e a recuperação seguinte só juntem janelas consecutivas medidas  
Para que as janelas de 30 s tenham o número certo de quadros e que o 'n ≥' citado no insight valha para todo o intervalo do evento

**Contexto:** reacao/ingest.py:12-21 calcula o tempo do quadro como índice/fps e amostra a cada round(fps) quadros. O OpenCV lê 15,0000207 quadros/s e 3543 quadros no igreja_simples_concat.mp4 (leitura de metadados em 2026-09-23, cópia local não versionada). Com essa taxa, o quadro 450 cai em 29,99996 s e entra na janela 0, que teve 31 quadros na execução local (out/window_aggregate.json:2, não versionado). Os 23 clipes têm 15 quadros/s (samples/corpus/pib/ffprobe.csv, não versionado). A mesma regra está duplicada em ultimo_tempo_amostrado (ingest.py:34-42), que o validador e o preparador de rotulagem usam (tools/validar_labels.py:158-169; tools/preparar_rotulagem.py:20-24). A issue #1 (k-mínimo com round e denominador com quadros de púlpito em reacao/aggregate.py) foi corrigida em main no commit f2d5e4a, com três testes (tests/test_aggregate.py:31-50). O comentário de 2026-09-07 deixa a issue aberta para a decisão do dono ('git revert f2d5e4a desfaz') e registra o efeito no clipe 07: de 37 para 41 rostos por quadro, com percentuais iguais. Em reacao/events.py:7-8 a série descarta as janelas insuficientes, então a contagem de 'sustain' (events.py:21-25) pode juntar janelas separadas por uma janela insuficiente. A recuperação é emitida na primeira janela da série sem queda, sem conferir adjacência (events.py:26-29). O evento grava em cobertura_min o n da janela em que a contagem chega a 3 (events.py:25), e o insight escreve 'n ≥ cobertura_min' (reacao/insights.py:21-24).

**Regras de negócio:**
- RN01 – O tempo de cada quadro amostrado vem do tempo de apresentação do quadro no vídeo. Para cada segundo alvo (0 s, 1 s, 2 s…), a ingestão amostra o primeiro quadro que alcança esse tempo.
- RN02 – A função que informa o último tempo amostrado, usada pelo validador e pelo preparador de rotulagem, segue a mesma regra da ingestão.
- RN03 – Quando a captura não informa o tempo do quadro, a ingestão usa índice/fps e registra no log um aviso que nomeia o vídeo (regra a confirmar no Definition of Ready).
- RN04 – Um evento sustentado só junta janelas adjacentes e suficientes. Janela insuficiente ou ausente entre duas quedas zera a sequência.
- RN05 – A recuperação de atenção só é emitida quando a janela seguinte à queda é adjacente e suficiente.
- RN06 – cobertura_min é o menor n_mensuravel entre as janelas do intervalo do evento.
- RN07 – A regra 3 (menos de 10 rostos mensuráveis leva a insuficiente e sem percentuais) vale em main qualquer que seja a decisão sobre f2d5e4a (CLAUDE.md, regra 3).
- RN08 – Os limiares de queda, subida, pico e sustentação não mudam (events.py:11-12).
- RN09 – A mudança entra em main antes da primeira execução do bench sobre o conjunto de teste (RN01 da Feature).

**Fora de escopo:**
- Calibração de limiares (F4.5)
- Regra do pico de sorriso (mediana das 6 janelas anteriores, events.py:31-37)
- Detector e pré-filtro de plateia (F4.4)
- Reprocessamento do corpus da PIB para conferir a mudança. A verificação usa captura simulada ou vídeo sintético

#### Critérios de aceite

- Para um vídeo com taxa de 15,0000207 quadros/s, cada janela cheia de 30 s tem 30 quadros.
- Para um vídeo com 15 quadros/s exatos, taxa dos clipes da PIB, os tempos amostrados continuam 0, 1, 2 … s.
- Para o mesmo vídeo, o último tempo amostrado informado ao validador é igual ao último tempo produzido pela ingestão.
- Com uma captura simulada que não informa o tempo do quadro, a ingestão usa índice/fps e o log traz um aviso que nomeia o vídeo e diz que o tempo veio de índice/fps.
- Com quedas de 20 p.p. nas janelas 4, 6 e 7 e a janela 5 insuficiente, nenhum evento de queda sustentada é emitido.
- Com quedas nas janelas 4, 5 e 6, todas suficientes e consecutivas, um evento de queda é emitido, como em tests/test_events.py:9-15.
- Com queda sustentada nas janelas 4 a 6, janela 7 insuficiente e subida na janela 8, nenhum evento de recuperação de atenção é emitido.
- Num evento cujas janelas têm n_mensuravel 30, 12 e 20, cobertura_min é 12, e o texto do insight gerado pelo modelo de frase traz 'n ≥ 12'.
- A issue #1 está fechada com comentário que remete à decisão de Fabio Pinheiro sobre f2d5e4a e à data.
- Em main, uma janela com média de 9,5 rostos mensuráveis sai insuficiente e sem percentuais.
- Os testes existentes de tests/test_events.py e tests/test_aggregate.py passam.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F1.2.T1 | Visão Computacional | Usar o tempo do quadro na ingestão e no cálculo do último tempo amostrado | 6 | — |
| F1.2.T2 | Machine Learning | Exigir janelas adjacentes e gravar o menor n do intervalo nos eventos sustentados e na recuperação | 5 | — |
| F1.2.T3 | QA | Conferir a regra 3 em main e fechar a issue #1 com a decisão registrada | 1 | F1.2.T5 (só se a decisão registrada for reverter f2d5e4a) |
| F1.2.T4 | QA | Verificar os critérios de aceite de tempo do quadro e de eventos sustentados | 4 | F1.2.T1, F1.2.T2 |
| F1.2.T5 | Backend | Reimplementar o k-mínimo sem arredondamento em reacao/aggregate.py (só se a decisão for reverter f2d5e4a) | 4 | — |

<details><summary>F1.2.T1 · [Visão Computacional] Usar o tempo do quadro na ingestão e no cálculo do último tempo amostrado</summary>

**Objetivo:** reacao/ingest.py amostra por tempo real do quadro, ultimo_tempo_amostrado segue a mesma regra, e a captura sem tempo de quadro usa a regra de RN03.

**Passos previstos:**
1. Ler o tempo do quadro informado pela captura em vez de idx/src_fps (ingest.py:12-21).
2. Amostrar o primeiro quadro que alcança cada segundo alvo.
3. Aplicar a mesma regra em ultimo_tempo_amostrado (ingest.py:34-42).
4. Implementar a regra de RN03 para captura sem tempo de quadro, com aviso no log.
5. Conferir que bench.py:119 e tools/preparar_rotulagem.py:20-24 continuam casando com segundos inteiros.
6. Escrever os testes com captura simulada para os critérios 1 a 4.

**Definição de pronto:** Os testes escritos na task para os critérios 1 a 4 passam; ruff check sem erro.

**Dependências:** nenhuma

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F1.2.T2 · [Machine Learning] Exigir janelas adjacentes e gravar o menor n do intervalo nos eventos sustentados e na recuperação</summary>

**Objetivo:** reacao/events.py interrompe a sequência em janela insuficiente ou não adjacente, só emite recuperação em janela adjacente e grava em cobertura_min o menor n do intervalo.

**Passos previstos:**
1. Zerar a sequência de queda quando a janela atual não for adjacente à anterior da série, comparando t_ini com o t_fim anterior.
2. Emitir recuperação só quando a janela seguinte à queda for adjacente e suficiente (events.py:26-29).
3. Acumular o menor n_mensuravel da sequência e gravá-lo em cobertura_min.
4. Manter os limiares de events.py:11-12.
5. Escrever os testes para os critérios 5 a 8.

**Definição de pronto:** Os testes escritos na task para os critérios 5 a 8 passam; tests/test_events.py passa; ruff check sem erro.

**Dependências:** nenhuma

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F1.2.T3 · [QA] Conferir a regra 3 em main e fechar a issue #1 com a decisão registrada</summary>

**Objetivo:** A regra 3 vale em main, e a issue #1 está fechada com remissão à decisão registrada no Definition of Ready.

**Passos previstos:**
1. Conferir na issue #1 o comentário de decisão de Fabio Pinheiro, com data.
2. Rodar tests/test_aggregate.py em main, inclusive o caso da média de 9,5.
3. Fechar a issue com comentário que cita a decisão, o commit que vale em main e o resultado dos testes.

**Definição de pronto:** Issue #1 fechada com comentário que remete à decisão e à data; o teste da média de 9,5 passa em main.

**Dependências:** F1.2.T5 (só se a decisão registrada for reverter f2d5e4a)

**Estimativa sugerida:** 1 h (sugestão; validar com o time)

</details>

<details><summary>F1.2.T4 · [QA] Verificar os critérios de aceite de tempo do quadro e de eventos sustentados</summary>

**Objetivo:** Cada critério de aceite de tempo e de eventos tem teste, e os testes falham sem as correções.

**Passos previstos:**
1. Rodar os testes de F1.2.T1 e F1.2.T2 no commit anterior e no final e registrar que falham antes e passam depois.
2. Acrescentar casos de borda: vídeo com uma única janela, última janela incompleta e série que começa com janela insuficiente.
3. Conferir o texto do insight gerado pelo modelo de frase para cobertura_min 12.
4. Rodar a suíte completa e conferir o CI.

**Definição de pronto:** Registro no PR com o resultado de cada critério; os testes falham no commit anterior e passam no final (verificado nos dois commits); CI verde.

**Dependências:** F1.2.T1, F1.2.T2

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F1.2.T5 · [Backend] Reimplementar o k-mínimo sem arredondamento em reacao/aggregate.py (só se a decisão for reverter f2d5e4a)</summary>

**Objetivo:** Depois da reversão de f2d5e4a, a regra 3 continua valendo em main.

**Passos previstos:**
1. Comentar na issue #1, antes do commit, a correção substituta (CONTRIBUTING.md:13).
2. Comparar a média de rostos mensuráveis com K_MIN sem round() ao decidir insuficiente (aggregate.py:24-31).
3. Escrever o teste da média de 9,5 rostos mensuráveis.
4. Rodar tests/test_aggregate.py.

**Definição de pronto:** O teste da média de 9,5 passa; tests/test_aggregate.py passa; o comentário na issue #1 tem data anterior ao commit.

**Dependências:** nenhuma

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- issue #1 e comentário de 2026-09-07 (https://github.com/ds-fabiopinheiro/church-sentiment-analysis/issues/1)
- commit f2d5e4a (em main)
- reacao/ingest.py:8-23,34-42
- reacao/aggregate.py:21-31
- reacao/events.py:7-8,11-29
- reacao/insights.py:21-24
- tests/test_events.py; tests/test_aggregate.py:31-50
- out/window_aggregate.json:2 (local, não versionado)
- Leitura de CAP_PROP_FPS e CAP_PROP_FRAME_COUNT de samples/corpus/pib/igreja_simples_concat.mp4 em 2026-09-23 (cópia local, não versionada)
- tools/validar_labels.py:158-169; tools/preparar_rotulagem.py:20-24
- CONTRIBUTING.md:13
- references/taskflow.md:38 (task começa e termina sem esperar decisão)

#### Verificação INVEST: pontos que falharam
- Independente: depende da decisão de Fabio Pinheiro sobre f2d5e4a, levada ao Definition of Ready.
- Small: o PBI junta dois comportamentos (tempo do quadro e eventos sustentados). Se o time preferir, vira dois PBIs.

#### Premissas
- Estimativas (story points e horas) são sugestão, a validar no refinamento.
- Definition of Ready: Fabio Pinheiro registra na issue #1, com data, a decisão sobre f2d5e4a (manter ou reverter) antes da sprint. Nenhuma task espera essa decisão.
- Definition of Ready: a regra de RN03 (índice/fps com aviso) é proposta desta árvore e é confirmada no refinamento. Se a decisão for outra, RN03 e o critério 4 são reescritos antes da sprint.
- F1.2.T5 só entra na sprint se a decisão registrada for reverter f2d5e4a. Ela usa a disciplina Backend, que a árvore não previa para F1.2 (Visão Computacional, Machine Learning e QA), porque reacao/aggregate.py é código Python do pipeline (regras das tasks).
- A mudança de tempo pode deslocar a grade de rótulos. Por isso a regra vale também para ultimo_tempo_amostrado, e F1.4 herda a função sem mudança.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Vincular a issue #1 ao PBI e citar o ID do PBI no título do PR
- Registrar no Definition of Ready a decisão sobre f2d5e4a e a regra de RN03
- Validar os 5 story points sugeridos

## Preview — PBI F1.3 (novo) · Pré-registrar em docs/poc-gate.md as regras de leitura dos seis critérios, a exposição e a composição do conjunto de teste, os vídeos permitidos por tipo de execução e a regra de escolha do motor

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Pré-registrar em docs/poc-gate.md as regras de leitura dos seis critérios, a exposição e a composição do conjunto de teste, os vídeos permitidos por tipo de execução e a regra de escolha do motor |
| Tipo | Product Backlog Item |
| Pai | F1 |
| Tags | fase-0; gate; pré-registro; governança; conjunto-de-teste |
| Estimativa | 8 pts (sugestão); tasks: 27 h |
| Dependências | F3.1.T8 (remoção de tools/rodar_teste.sh e da remissão em docs/poc-gate.md:47-48), antes de F1.3.T4 e da revisão de F1.3.T5 |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro e pastor Filipe, que assinam o gate  
Quero as regras de leitura dos seis critérios, a exposição já ocorrida do conjunto de teste, a composição do conjunto de teste, os vídeos permitidos em cada tipo de execução e a regra de escolha do motor de produção e do de reserva escritos e assinados antes da primeira execução do bench sobre o conjunto de teste  
Para decidir o gate (seguir, ajustar e repetir ou parar) por regras fixadas antes de ver os números, como pede docs/poc-gate.md:16,38-40

**Contexto:** docs/poc-gate.md:16 diz que as notas foram fixadas antes de o conjunto de teste existir, e :38-40 exige assinar a meta do 2b antes de rodar o conjunto de teste. Faltam as regras abaixo. Critério 2b: há sugestão de 2,0 p.p. em :38-39, deduzida para o desvio-padrão de uma série (:35-40). O bench calcula o jitter da linha TOTAL como o pior vídeo (bench.py:167,179, comentário 'pior vídeo, não a média'), o que exige 4 trechos neutros no mesmo clipe (bench.py:155-159), e os clipes têm de 1,3 s a 23,1 s (samples/corpus/pib/README.md:7, não versionado). Mínimo de risos: labels/README.md:13 e tools/validar_labels.py:216-217 exigem só 1. Pareamento e denominador do critério 3 (:11). Leitura de '≥ 3/5' do critério 4 (:12). Fórmula única do critério 5: o bench mede só inferência (bench.py:181-183) e imprime 'fps ≥ 1' (bench.py:261-262), o run_log mede o tempo total (reacao/cost.py:20-25) e o gate fixa ≤ 2 h (:13). Alvo do critério 6, hoje 'passa no CI' com motor mock (:14). Origem do novo conjunto de teste em 'ajustar e repetir' (:50). Caixas nos rótulos na Fase 1 (:20-21). docs/poc-gate.md:46-48 define a separação entre desenvolvimento e teste pelo --excluir do bench (bench.py:195-211), remete a tools/rodar_teste.sh e afirma que sobram 19 clipes nunca vistos, mas o clipe 11 e o concatenado passaram pelo pipeline com hsemotion em execução local (PR #3; out/run_log.json, não versionado). O concatenado contém os 23 clipes (samples/corpus/pib/README.md:12, não versionado). tools/rodar_teste.sh baixa o corpus privado para disco local (:35-40) e, no passo 5, roda bench.py localmente sobre os clipes fora de DEV_CLIPES, isto é, sobre o conjunto de teste (:15-16,54-56). Essa execução não aparece na listagem de jobs do HF. tools/rodar_teste.sh:59-61 sugere processar o clipe 11 para o critério 5. Na F3 revisada, F3.1.T8, sem dependência, remove tools/rodar_teste.sh e as referências a ele, inclusive docs/poc-gate.md:47-48. Como docs/poc-gate.md é o documento que F1.3 assina, e mudança depois da assinatura exige nova assinatura (RN07), a remoção precisa entrar em main antes da revisão de F1.3.T5. Pela P3 revisada, o relatório e as notas do critério 4 ficam no painel web na Vercel (F5.6, F5.7). Na F4 detalhada, F4.1 (RN11 e F4.1.T7) propõe aplicar o k-mínimo a cada percentual, a confirmar por Fabio Pinheiro, e F4.6 registra que não existe regra pré-registrada de escolha do motor (F4.6, premissas; F4, riscos). Na F5 detalhada, F5.7 deixa para F1.3 quais relatórios entram no critério 4, a nota repetida do mesmo avaliador, a visibilidade das notas e a nota faltante (F5.7, premissas e critérios). Com o veto da PIB por F3.1 (P13), F3.6 seleciona clipes públicos de desenvolvimento e de teste sem vídeo em comum (F3.6 RN01), F3.7 os rotula em pastas separadas (F3.7.T4 e F3.7.T5), e F4.4 e F4.5 passam a depender dos rótulos públicos de desenvolvimento (F4 detalhada). Pela P3 revisada e pela P26, execução local usa só a fixture sintética, e o vídeo licenciado de F1.6 só roda no CI (F2 RN10; F4.1 RN10; F5.3, premissas). Na Fase 0, job sobre clipe da PIB não grava no Supabase (F3.1 RN06). O título do documento cita PBI-105 (docs/poc-gate.md:1), que a árvore destina a F6.1.

**Regras de negócio:**
- RN01 – O documento é assinado e datado por Fabio Pinheiro e pelo pastor Filipe antes da primeira execução do bench sobre o conjunto de teste, no HF Jobs ou local.
- RN02 – Cada item traz uma decisão. Valor sugerido e não assinado não conta como decisão (docs/poc-gate.md:38-40).
- RN03 – Itens obrigatórios: (a) leitura do critério 1, que vale só para o detector medido (P31); (b) meta do 2b em p.p. e forma de cálculo do jitter_dp_pp na linha TOTAL (desvio-padrão agrupado dos trechos neutros do corpus, ou pior vídeo com mínimo de 4 trechos no mesmo clipe), assinadas juntas; (c) mínimo de eventos de riso para o 2a ser conclusivo e efeito de um 2a inconclusivo na decisão; (d) regra de pareamento e denominador do critério 3; (e) leitura de '≥ 3/5' do critério 4, sobre as notas registradas no painel web na Vercel (F5.7): quais relatórios de culto entram, nota repetida do mesmo avaliador, visibilidade das notas entre avaliadores e tratamento de nota faltante; (f) fórmula única de tempo e custo por hora de vídeo do critério 5 (inferência do bench ou tempo total do run_log) e o limite equivalente em quadros por segundo; (g) alvo do critério 6 com o caminho real de detecção e recorte; (h) origem do novo conjunto de teste em 'ajustar e repetir'; (i) se a Fase 1 exige caixas nos rótulos; (j) k-mínimo dos percentuais lidos nos critérios 2a e 2b: só pela altura (regra 3; reacao/aggregate.py:26-31) ou também por percentual, com média de pelo menos K_MIN rostos mensuráveis com aquele valor (F4.1 RN11); (k) regra de escolha do motor de produção e do de reserva em F4.6 a partir da linha TOTAL e da decisão de licença de F4.3, inclusive quando nenhum motor atinge as metas.
- RN04 – O registro de exposição cita as execuções locais do clipe 11 e do concatenado, diz se o clipe 11 continua no conjunto de teste e traz declaração datada de Fabio Pinheiro sobre as execuções locais de pipeline e de bench sobre clipes de teste até a data da assinatura.
- RN05 – Vídeos permitidos por tipo de execução. Fumaça (F2.2), validação (F2.8, F4.1.T9, F4.2.T8) e paridade (F2.7): só fixture sintética lida do dataset por revisão (F1.1.T6), vídeos públicos de docs/corpus.csv fora do conjunto de teste ou, depois de F3.1 permitir o uso da PIB, os clipes 07 a 10. Job que gera o relatório exibido no painel web na Vercel antes do gate (F5.6): só cultos públicos de docs/corpus.csv (P10). Calibração e medição do pré-filtro (F4.4, F4.5): só os clipes 07 a 10 (P8). Bench do conjunto de teste (F4.6), no HF Jobs: única execução que processa clipes de teste. Execução local de pipeline ou de bench, em qualquer máquina: só a fixture sintética, e o vídeo licenciado de F1.6 roda só no CI (P3 revisada; P26); nenhuma execução local processa clipe de teste. Ferramenta de rotulagem (F3.3): mostra os clipes a rotular sem rodar o pipeline sobre eles. Na Fase 0, job sobre clipe da PIB não grava no Supabase (F3.1 RN06). Com o veto da PIB por F3.1 (P13), nenhum clipe da PIB é processado; validação, calibração e medição do pré-filtro usam só o conjunto de desenvolvimento dos clipes públicos de F3.6 (rótulos de F3.7.T4), e o conjunto de teste público de F3.6 (rótulos de F3.7.T5) só é processado pelo bench de F4.6. Com F3.6 acionado pela falta de risos em F3.4, os clipes públicos de teste entram no conjunto de teste e seguem a regra dos clipes de teste.
- RN06 – tools/rodar_teste.sh, cujo passo 5 roda bench.py localmente sobre os clipes de teste (linhas 54-56), sai de main por F3.1.T8 antes da revisão de F1.3.T5. Nenhuma task de F1.3 altera o script. O parágrafo de separação entre desenvolvimento e teste de docs/poc-gate.md não remete ao script e descreve a composição do conjunto de teste com a PIB permitida (os 23 clipes menos 07 a 10, excluídos da linha TOTAL pelo --excluir do bench de F4.6; bench.py:195-211), com o veto da PIB (pasta de teste dos clipes públicos de F3.6 e F3.7) e com F3.6 acionado pela falta de risos (clipes de teste da PIB mais os clipes públicos de teste).
- RN07 – Mudança depois da assinatura exige nova assinatura, com motivo e data.
- RN08 – O título de docs/poc-gate.md passa a citar o ID do Azure DevOps de F6.1 no lugar de PBI-105, destino desse ID na árvore (RN15 da Feature).

**Fora de escopo:**
- Medir qualquer critério (F4.6, F5.4, F5.5, F5.7)
- Implementar as regras no bench e no validador (F1.4)
- Definir a granularidade de cobrança do HF Jobs (F5.4, P21)
- Registrar a decisão do gate (F6.1)
- Recall pareado por IoU (docs/poc-gate.md:20-21)
- Remover tools/rodar_teste.sh (F3.1.T8) e retirar as cópias locais do corpus (F3.1)
- Implementar o k-mínimo por percentual (F4.1.T7) e registrar a escolha do motor no ADR 0001 (F4.6)
- Selecionar e rotular os clipes públicos do caminho de veto (F3.6, F3.7)

#### Critérios de aceite

- Cada um dos onze itens de RN03 aparece em docs/poc-gate.md com uma decisão, sem 'a definir'.
- A regra do critério 2b traz a meta como número em p.p. e diz a forma de cálculo do jitter_dp_pp na linha TOTAL.
- A regra do critério 2a diz o mínimo de eventos de riso rotulados e o efeito de um 2a inconclusivo na decisão do gate.
- A regra do critério 5 dá uma única fórmula de tempo e de custo por hora de vídeo, diz se ela vem do bench ou do run_log e dá o limite equivalente em quadros por segundo.
- O registro de exposição cita as execuções locais do clipe 11 e do concatenado e diz se o clipe 11 continua no conjunto de teste. A frase 'Sobram 19 clipes nunca vistos' (docs/poc-gate.md:48) foi trocada por remissão ao registro de exposição, e o parágrafo de separação lista os clipes do conjunto de teste, diz que o bench de F4.6 exclui os clipes 07 a 10 pelo --excluir e descreve a composição com o veto da PIB e com F3.6 acionado pela falta de risos.
- A lista de vídeos permitidos cobre fumaça, validação (F2.8, F4.1.T9, F4.2.T8), paridade, relatório do painel web na Vercel, calibração, execução local, bench do conjunto de teste e ferramenta de rotulagem, com a PIB permitida e com o veto da PIB. Só o bench do conjunto de teste, no HF Jobs, processa clipes de teste, e a execução local usa só a fixture sintética.
- Na data da revisão de F1.3.T5, tools/rodar_teste.sh não está em main e docs/poc-gate.md não o cita, conferido com git ls-files e busca por 'rodar_teste'. Se F3.1.T8 não estiver em main nessa data, a revisão é adiada e a pendência fica registrada com responsável e data.
- O documento traz a data e as assinaturas de Fabio Pinheiro e do pastor Filipe. A data é anterior à criação do primeiro job do bench sobre o conjunto de teste, conferida na listagem de jobs do namespace, e o documento traz a declaração datada de Fabio Pinheiro de que nenhuma execução local processou clipe de teste depois do registro de exposição.
- Se algum item estiver sem decisão na revisão, o documento não é assinado, o item fica listado como pendente com responsável e data, e nenhuma execução do bench sobre o conjunto de teste ocorre enquanto houver pendência.
- Se um job ou uma execução local do bench sobre o conjunto de teste tiver ocorrido antes da assinatura, o documento registra o JOB_ID ou a data e a máquina e trata essa execução como exposição do conjunto de teste.
- A regra do critério 4 diz quais relatórios de culto entram, como tratar nota repetida do mesmo avaliador, se um avaliador vê as notas do outro e como tratar nota faltante. A regra do k-mínimo diz se ele vale só pela altura ou também por percentual. A regra de escolha do motor diz como produção e reserva saem da linha TOTAL e da licença e o que acontece quando nenhum motor atinge as metas.
- O título de docs/poc-gate.md cita o ID do Azure DevOps de F6.1, e a busca por 'PBI-105' no documento não tem resultado.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F1.3.T1 | Data Science | Redigir a proposta das regras de leitura dos critérios 1 a 5, do k-mínimo dos percentuais e da escolha do motor | 11 | — |
| F1.3.T2 | Data Science | Redigir o alvo do critério 6, a origem do novo conjunto de teste e a decisão sobre caixas na Fase 1 | 3 | — |
| F1.3.T3 | Governança e Privacidade | Registrar a exposição do conjunto de teste e a lista de vídeos permitidos por tipo de execução | 5 | — |
| F1.3.T4 | Data Science | Reescrever em docs/poc-gate.md:46-48 a composição do conjunto de teste e a exclusão dos clipes de desenvolvimento, depois da remoção de tools/rodar_teste.sh, e trocar o ID antigo do título | 3 | F3.1.T8, F1.3.T3 |
| F1.3.T5 | Governança e Privacidade | Conduzir a revisão das propostas com Fabio Pinheiro e o pastor Filipe e registrar o resultado | 2 | F1.3.T1, F1.3.T2, F1.3.T3, F1.3.T4 |
| F1.3.T6 | QA | Verificar o documento contra os critérios de aceite e registrar o resultado | 3 | F1.3.T5 |

<details><summary>F1.3.T1 · [Data Science] Redigir a proposta das regras de leitura dos critérios 1 a 5, do k-mínimo dos percentuais e da escolha do motor</summary>

**Objetivo:** docs/poc-gate.md traz, para os critérios 1 a 5, o k-mínimo dos percentuais e a escolha do motor, uma proposta de regra com alternativa e justificativa, pronta para decisão.

**Passos previstos:**
1. Critério 1: escrever que o número vale só para o detector medido e o que acontece se F4.7 trocar o detector (P31).
2. Critério 2b: propor a meta em p.p., partindo da sugestão de 2,0 p.p. (docs/poc-gate.md:38-39), e a forma de cálculo do jitter na linha TOTAL. Comparar o desvio-padrão agrupado do corpus, que soma a diferença de base entre clipes, com o pior vídeo (bench.py:179), que exige 4 trechos neutros no mesmo clipe (bench.py:155-159).
3. Critério 2a: propor o mínimo de eventos de riso e o efeito de um 2a inconclusivo na decisão.
4. Critério 3: propor a regra de pareamento das fronteiras e o denominador dos 80%.
5. Critério 4: propor a leitura de '≥ 3/5' sobre as notas registradas no painel web na Vercel (F5.7), quem precisa concordar, quais relatórios de culto entram, o tratamento de nota repetida do mesmo avaliador e de nota faltante e se um avaliador vê as notas do outro (premissas de F5.7).
6. Critério 5: propor a fórmula única (inferência do bench ou tempo total do run_log) e o limite em quadros por segundo equivalente a ≤ 2 h.
7. k-mínimo dos percentuais: comparar o k-mínimo só pela altura (regra 3; reacao/aggregate.py:26-31) com o k-mínimo por percentual de F4.1 RN11 e mostrar o efeito de cada um nos critérios 2a e 2b.
8. Escolha do motor: propor a regra que define o motor de produção e o de reserva a partir da linha TOTAL de F4.6 e da decisão de licença de F4.3, inclusive quando nenhum motor atinge as metas dos critérios 1, 2a e 2b (pendência de F4.6).

**Definição de pronto:** Os critérios 1 a 5, o k-mínimo dos percentuais e a escolha do motor têm proposta, alternativa e justificativa no PR, revisadas por Fabio Pinheiro.

**Dependências:** nenhuma

**Estimativa sugerida:** 11 h (sugestão; validar com o time)

</details>

<details><summary>F1.3.T2 · [Data Science] Redigir o alvo do critério 6, a origem do novo conjunto de teste e a decisão sobre caixas na Fase 1</summary>

**Objetivo:** docs/poc-gate.md traz proposta para os itens (g), (h) e (i) de RN03.

**Passos previstos:**
1. Propor o alvo do critério 6 com o caminho real de detecção e recorte e as falhas da issue #2 corrigidas (F1.1, F1.6).
2. Propor de onde vem o novo conjunto de teste se a decisão for 'ajustar e repetir'.
3. Propor se a Fase 1 exige caixas nos rótulos (docs/poc-gate.md:20-21).

**Definição de pronto:** Os três itens têm proposta e justificativa no PR, revisadas por Fabio Pinheiro.

**Dependências:** nenhuma

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F1.3.T3 · [Governança e Privacidade] Registrar a exposição do conjunto de teste e a lista de vídeos permitidos por tipo de execução</summary>

**Objetivo:** docs/poc-gate.md registra o que já foi exposto, traz o texto da declaração sobre execuções locais e lista os vídeos que cada tipo de execução pode usar, com a PIB permitida e com o veto da PIB.

**Passos previstos:**
1. Registrar as execuções locais do clipe 11 e do concatenado com hsemotion (PR #3; out/run_log.json).
2. Preparar as opções para a decisão sobre o clipe 11 continuar ou sair do conjunto de teste.
3. Redigir o texto da declaração de Fabio Pinheiro sobre execuções locais de pipeline e de bench sobre clipes de teste.
4. Escrever a lista de vídeos permitidos de RN05, com a validação de F2.8, F4.1.T9 e F4.2.T8, a execução local só com a fixture sintética, a fixture lida do dataset por revisão (F1.1.T6), a regra de F3.1 RN06 para clipes da PIB e a referência a P8, P10 e F3.1.
5. Escrever o caminho de veto da PIB (P13) e o de F3.6 acionado pela falta de risos: conjunto de desenvolvimento público (F3.7.T4) para validação, calibração e medição do pré-filtro, e conjunto de teste público (F3.7.T5) só para o bench de F4.6.

**Definição de pronto:** O registro de exposição, as opções sobre o clipe 11, o texto da declaração e a lista estão no PR, revisados por Fabio Pinheiro.

**Dependências:** nenhuma

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F1.3.T4 · [Data Science] Reescrever em docs/poc-gate.md:46-48 a composição do conjunto de teste e a exclusão dos clipes de desenvolvimento, depois da remoção de tools/rodar_teste.sh, e trocar o ID antigo do título</summary>

**Objetivo:** O parágrafo 'Separação entre desenvolvimento e teste' diz quais clipes formam o conjunto de teste, com a PIB permitida e no caminho de clipes públicos, e como o bench de F4.6 deixa os clipes de desenvolvimento fora da linha TOTAL, sem remissão a tools/rodar_teste.sh e sem a frase 'Sobram 19 clipes nunca vistos'. O título cita o ID de F6.1 no lugar de PBI-105.

**Passos previstos:**
1. Conferir em main que F3.1.T8 removeu tools/rodar_teste.sh e a remissão a ele em docs/poc-gate.md:47-48.
2. Listar os clipes do conjunto de teste (os 23 clipes menos 07 a 10), com as duas opções para o clipe 11 preparadas em F1.3.T3, e registrar que igreja_simples_concat.mp4 não faz parte do conjunto (F1.4 RN06).
3. Escrever que a exclusão dos clipes 07 a 10 na linha TOTAL é feita pelo --excluir do bench (bench.py:195-211) no job de F4.6, com a lista escrita no pré-registro.
4. Descrever a composição com o veto da PIB (pasta de teste dos clipes públicos de F3.6 e F3.7, pela tag de F3.5.T2) e com F3.6 acionado pela falta de risos (clipes de teste da PIB mais os clipes públicos de teste).
5. Trocar a frase 'Sobram 19 clipes nunca vistos, com 195 dos 248 quadros do corpus' (docs/poc-gate.md:48) por remissão ao registro de exposição de F1.3.T3.
6. Trocar 'PBI-105' do título (docs/poc-gate.md:1) pelo ID do Azure DevOps de F6.1, destino de PBI-105 na árvore.

**Definição de pronto:** O diff de docs/poc-gate.md no PR traz a lista dos clipes de teste, a composição com o veto e com a falta de risos, a regra do --excluir, a remissão ao registro de exposição e o ID de F6.1 no título; busca por 'rodar_teste', 'nunca vistos' e 'PBI-105' em docs/poc-gate.md sem resultado; texto revisado por Fabio Pinheiro.

**Dependências:** F3.1.T8, F1.3.T3

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F1.3.T5 · [Governança e Privacidade] Conduzir a revisão das propostas com Fabio Pinheiro e o pastor Filipe e registrar o resultado</summary>

**Objetivo:** O PR registra o que foi decidido, o que ficou pendente e a forma de assinatura do pastor Filipe.

**Passos previstos:**
1. Conferir em main, antes de marcar a revisão, que tools/rodar_teste.sh foi removido (F3.1.T8).
2. Apresentar as propostas de F1.3.T1 a T4 aos dois responsáveis.
3. Registrar a decisão de cada item tomada na revisão e a decisão sobre o clipe 11.
4. Listar os itens sem decisão, com responsável e data.
5. Registrar a forma de assinatura do pastor Filipe e o local onde a evidência será anexada.

**Definição de pronto:** Revisão realizada; decisões tomadas registradas no PR; itens sem decisão listados com responsável e data; forma de assinatura do pastor Filipe registrada.

**Dependências:** F1.3.T1, F1.3.T2, F1.3.T3, F1.3.T4

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F1.3.T6 · [QA] Verificar o documento contra os critérios de aceite e registrar o resultado</summary>

**Objetivo:** Cada critério de aceite de F1.3 é conferido, e o resultado fica registrado, inclusive os que ainda não passam.

**Passos previstos:**
1. Conferir os onze itens de RN03 com decisão, inclusive as regras de nota do critério 4, do k-mínimo e da escolha do motor.
2. Conferir a lista de vídeos: só o bench do conjunto de teste, no HF Jobs, processa clipes de teste; a execução local usa só a fixture sintética; o caminho de veto e o de falta de risos estão cobertos.
3. Conferir o parágrafo de separação: lista dos clipes de teste, composição com o veto e com a falta de risos, regra do --excluir e remissão ao registro de exposição.
4. Conferir com git ls-files e busca por 'rodar_teste' que tools/rodar_teste.sh não está em main e que docs/poc-gate.md não o cita na data da revisão.
5. Conferir o ID de F6.1 no título e a busca por 'PBI-105' em docs/poc-gate.md sem resultado.
6. Comparar a data das assinaturas com a criação do primeiro job do bench sobre o conjunto de teste na listagem de jobs e conferir a declaração sobre execuções locais.

**Definição de pronto:** Checklist dos critérios anexado ao PR, com 'passou' ou 'não passou' e o motivo em cada um, aprovado por Fabio Pinheiro.

**Dependências:** F1.3.T5

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- docs/poc-gate.md:1-50 (o título cita PBI-105, que a árvore mapeou para F6.1)
- labels/README.md:12-14
- tools/validar_labels.py:215-220
- bench.py:155-159,167,179,181-183,195-211,261-262
- reacao/cost.py:20-25
- out/run_log.json e out/window_aggregate.json (locais, não versionados)
- PR #3 (seção Verificação)
- samples/corpus/pib/README.md:7,12 (não versionado)
- tools/rodar_teste.sh:15-16,35-40,54-56,59-61 (commit 5176bc3)
- F3.1.T8 (F3 revisada): remove tools/rodar_teste.sh e atualiza docs/poc-gate.md:47-48, sem dependência
- insightface-2.0.dist-info/METADATA:50-54 (instalado)
- Premissas P8, P10, P28 e P31 da árvore; P3 revisada
- reacao/aggregate.py:24-42
- arvore_v1.json, destino dos IDs antigos: PBI-105 → F6.1
- feature_det_F4.json da sessão: F4.1 RN11 e F4.1.T7; F4.6, premissas e pendências; riscos da F4 (sem regra pré-registrada de escolha do motor)
- feature_det_F5.json da sessão: F5.7, premissas e critérios (relatórios, nota repetida, visibilidade e nota faltante); F5.3, premissas (leitura da P26)
- feature_det_F3.json da sessão: F3.1 RN06; F3.6 RN01 e RN03; F3.7.T4 e F3.7.T5
- feature_det_F2.json da sessão: RN10 da F2 (execução local só com a fixture sintética); F2.8 (job de validação)

#### Verificação INVEST: pontos que falharam
- Independente: a conclusão depende das assinaturas de duas pessoas e de F3.1.T8, task de outra Feature.
- Estimável: o prazo depende da disponibilidade do pastor Filipe.
- Small: com onze itens de decisão, 12 critérios sobre o mesmo documento e 27 h de tasks, a revisão com os dois responsáveis pode exigir mais de uma reunião.

#### Premissas
- Estimativas (story points e horas) são sugestão, a validar no refinamento.
- PBI documental. A verificação é feita por QA (F1.3.T6) e aprovada por Fabio Pinheiro, além das assinaturas.
- A forma de assinatura do pastor Filipe (comentário, e-mail ou documento anexado ao PR) não está definida e é registrada em F1.3.T5.
- As propostas de F1.3.T1 e T2 trazem alternativas com justificativa. Os valores são decisão de Fabio Pinheiro e do pastor Filipe. As assinaturas são critério do PBI, e nenhuma task espera por elas para terminar.
- F1.3.T4 fica em Data Science, disciplina prevista na árvore para F1.3, porque a redação define a composição do conjunto de teste e a exclusão dos clipes de desenvolvimento no plano de medição. Ela não mexe em imagem, CI, segredos nem HF Jobs.
- F3.1.T8 não tem dependência na F3 revisada e pode entrar na sprint de F1.3. Se não entrar, F1.3.T4 e a revisão de F1.3.T5 esperam, e nenhuma execução do bench sobre o conjunto de teste ocorre (RN01; critério 9).
- Se F3.1.T8 também reescrever o parágrafo de docs/poc-gate.md:46-48, F1.3.T4 parte do texto que estiver em main. A pendência pede que F3.1.T8 só retire a remissão ao script.
- A listagem de jobs do namespace é consulta sem custo.
- Os itens (e), (j) e (k) de RN03 vêm de pedidos de F5 (F5.7) e de F4 (F4.1 RN11 e F4.6), para que a decisão venha antes do bench do conjunto de teste. Se Fabio Pinheiro recusar a RN11 de F4.1 no refinamento de F4, o item (j) registra o k-mínimo só pela altura.
- Os clipes públicos de F3.6 não existem na data do pré-registro. A composição com o veto e com a falta de risos é descrita pela pasta e pela tag de F3.5.T2, sem lista de arquivos.
- O ID do Azure DevOps de F6.1 existe antes de F1.3.T4, porque a sincronização da árvore cria os itens antes da sprint.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Vínculo de dependência F3.1.T8 → F1.3.T4 no Azure DevOps e F3.1.T8 na sprint de F1.3
- Responsável de governança para F1.3.T3 e F1.3.T5
- Agenda com o pastor Filipe para a assinatura
- Validar os 8 story points sugeridos
- ID do Azure DevOps de F6.1 criado antes de F1.3.T4
- Pedir a F3.6 que a RN03 valha só para o conjunto de teste, como RN05 deste PBI registra
- Avisar F4.1.T7, F4.6.T5 e F5.7 de que as regras dos itens (j), (k) e (e) de RN03 ficam aqui
- F2.8.T5 altera docs/poc-gate.md depois da assinatura; pela RN07, isso exige nova assinatura. Decidir no refinamento se o mapa de arquivo e coluna vai para outro documento

## Preview — PBI F1.4 (novo) · Corrigir o bench e o validador para que a linha TOTAL dê número nos critérios 1, 2a e 2b e mostre a regra do critério 5 pré-registrada

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Corrigir o bench e o validador para que a linha TOTAL dê número nos critérios 1, 2a e 2b e mostre a regra do critério 5 pré-registrada |
| Tipo | Product Backlog Item |
| Pai | F1 |
| Tags | fase-0; gate; bench; rótulos; critério-2; critério-5 |
| Estimativa | 5 pts (sugestão); tasks: 17 h |
| Dependências | F1.3 |
| Substitui | nenhum |

#### Descrição

Como membro do time de Data Science que lê a linha TOTAL do bench  
Quero que o jitter da linha TOTAL siga a forma de cálculo assinada em F1.3, que o bench mostre a regra do critério 5 pré-registrada e que o validador recuse rótulos que o bench mediria errado  
Para que a linha TOTAL do bench sobre o conjunto de teste dê número nos critérios 1, 2a e 2b, sem NaN causado pelo formato do corpus, e não mostre regra do critério 5 diferente da assinada

**Contexto:** O jitter por vídeo exige 4 trechos neutros no mesmo vídeo (bench.py:155-159), e a linha TOTAL usa o maior jitter por vídeo (bench.py:167,179). Com clipes de 1,3 s a 23,1 s (samples/corpus/pib/README.md:7) e um trecho neutro por clipe, a linha TOTAL sai NaN, embora labels/README.md:12-14 e tests/test_validar_labels.py:66-68 digam que os mínimos valem para o corpus inteiro. A forma de cálculo do jitter é uma regra de leitura do critério 2b e é assinada em F1.3 (RN03, item b). O bench imprime 'fps ≥ 1' (bench.py:261-262) e o gate fixa ≤ 2 h (docs/poc-gate.md:13). F1.3 decide se a fórmula do critério 5 vem da inferência do bench (bench.py:181-183) ou do tempo total do run_log (reacao/cost.py:20-25). A saída no terminal descarta flavor e inferencia_s (bench.py:256). O validador exige só 1 riso (tools/validar_labels.py:216-217) e não acusa intervalo sem segundo inteiro amostrado (validar_labels.py:99-123). O bench conta esse riso como não atingido (bench.py:73-81,137-151). validar_labels.py:189 e bench.py:206 incluem todo *.mp4 da pasta, inclusive igreja_simples_concat.mp4, que contém os clipes de desenvolvimento e de teste (samples/corpus/pib/README.md:12). tools/preparar_rotulagem.py:43 faz o mesmo, e labels/README.md:36 manda validar com --corpus samples/, mas os vídeos estão na subpasta pib. Na F3 revisada, F3.5.T6 retira preparar_rotulagem.py e reescreve labels/README.md:25-41. O bench já resolve URI hf://datasets/ para /dev/shm (bench.py:58-70). F3.1.T8 remove tools/rodar_teste.sh, que baixava o corpus privado para disco local e rodava o bench sobre os clipes de teste (tools/rodar_teste.sh:35-40,54-56), antes da assinatura de F1.3, da qual F1.4 depende.

**Regras de negócio:**
- RN01 – O jitter_dp_pp da linha TOTAL segue a forma de cálculo assinada em F1.3. Forma agrupada: desvio-padrão de pct_sorrindo entre todos os trechos neutros medidos do corpus, com mínimo de 4 trechos. Forma por vídeo: maior desvio-padrão entre os vídeos com pelo menos 4 trechos neutros (bench.py:155-159,179).
- RN02 – Quando o mínimo da forma assinada não é atingido, a linha TOTAL mostra NaN no jitter, e o validador sai com erro que cita a regra (validar_labels.py:218-220).
- RN03 – Se a fórmula assinada do critério 5 usar a inferência do bench, o bench imprime o limite assinado. Se usar o tempo total do run_log, o bench informa que o critério 5 é lido no run_log e não imprime limite de velocidade.
- RN04 – O validador sai com erro quando o corpus tem menos eventos de riso que o mínimo pré-registrado em F1.3.
- RN05 – O validador sai com erro quando um intervalo de evento não contém nenhum segundo inteiro amostrado.
- RN06 – validar_labels.py e bench.py deixam igreja_simples_concat.mp4 de fora por padrão e informam isso na saída. tools/preparar_rotulagem.py não muda, porque F3.5.T6 o retira.
- RN07 – O validador aceita o corpus por URI hf://datasets/, como o bench, com os vídeos em /dev/shm (regra 1).
- RN08 – A saída do bench no terminal mantém as colunas flavor e inferencia_s.
- RN09 – As linhas por vídeo continuam diagnóstico. O gate lê só a linha TOTAL (docs/poc-gate.md:3-4).
- RN10 – A verificação deste PBI usa arquivos sintéticos e download simulado e não lê o corpus privado (RN12 da Feature).
- RN11 – Este PBI não altera tools/preparar_rotulagem.py nem labels/README.md (RN14 da Feature; F3.5.T6).
- RN12 – A docstring de bench.py passa a citar o ID do Azure DevOps de F4.6 no lugar de PBI-000H, destino desse ID na árvore (RN15 da Feature).

**Fora de escopo:**
- Comparador do critério 3 e validação de pasta só com _momentos.csv (F5.1, F5.5)
- Decisão dos valores do critério 5, do mínimo de risos e da forma de cálculo do jitter (F1.3)
- Execução do bench no HF (F4.6)
- Mudança nas métricas do critério 1 (recall_ge64_max)
- Retirada de tools/preparar_rotulagem.py e reescrita de labels/README.md:25-41, inclusive o comando da linha 36 (F3.5.T6)
- Exclusão do concatenado na lista de clipes da ferramenta de rotulagem (F3.3)
- Onde o validador roda depois que F3.1 retirar as cópias locais (F3.1, F3.4)

#### Critérios de aceite

- Se F1.3 assinar a forma agrupada: num teste com 4 clipes e 1 trecho neutro medido em cada um, a linha TOTAL mostra jitter_dp_pp numérico igual ao desvio-padrão dos 4 valores; com 3 trechos neutros no corpus, a linha TOTAL mostra NaN no jitter, e o validador sai com código 1 e cita o mínimo de 4.
- Se F1.3 assinar a forma por vídeo: num teste em que nenhum vídeo tem 4 trechos neutros, a linha TOTAL mostra NaN no jitter, e o validador sai com código 1 e cita a exigência de 4 trechos no mesmo vídeo.
- Um riso rotulado de 3,2 s a 3,8 s faz o validador sair com código 1, com mensagem que cita o arquivo e a linha.
- Um corpus com menos risos que o mínimo pré-registrado em F1.3 faz o validador sair com código 1, com mensagem que cita o mínimo.
- Com igreja_simples_concat.mp4 numa pasta de corpus sintética, o validador e o bench o deixam de fora e dizem isso na saída.
- Se a fórmula assinada do critério 5 usar a inferência do bench, o limite impresso pelo bench é o mesmo de docs/poc-gate.md. Se usar o run_log, a saída do bench diz que o critério 5 é lido no run_log e não imprime limite de velocidade.
- A saída do bench no terminal traz as colunas flavor e inferencia_s.
- tools/validar_labels.py, chamado com --corpus hf://datasets/ (download simulado) e rótulos válidos de teste sobre vídeos sintéticos, sai com código 0 e não deixa arquivo do download em /dev/shm ao fim.
- O diff do PR não altera tools/preparar_rotulagem.py nem labels/README.md.
- A docstring de bench.py cita o ID do Azure DevOps de F4.6, e a busca por 'PBI-000H' no repositório não tem resultado.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F1.4.T1 | Data Science | Calcular o jitter da linha TOTAL pela forma assinada e alinhar a saída do bench à regra do critério 5 | 5 | — |
| F1.4.T2 | Backend | Fazer o validador exigir os mínimos assinados, acusar intervalo sem segundo amostrado e aceitar URI do dataset | 6 | — |
| F1.4.T3 | Backend | Excluir o concatenado por padrão no validador e no bench | 2 | — |
| F1.4.T4 | QA | Verificar os critérios de aceite do bench e do validador | 4 | F1.4.T1, F1.4.T2, F1.4.T3 |

<details><summary>F1.4.T1 · [Data Science] Calcular o jitter da linha TOTAL pela forma assinada e alinhar a saída do bench à regra do critério 5</summary>

**Objetivo:** A linha TOTAL calcula o jitter pela forma assinada em F1.3, e o bench mostra a regra do critério 5 assinada.

**Passos previstos:**
1. Implementar em linha_total a forma de cálculo do jitter assinada em F1.3 (bench.py:155-159,167,179).
2. Manter o jitter por vídeo como diagnóstico.
3. Trocar 'fps ≥ 1' pelo limite assinado ou pela indicação de que o critério 5 é lido no run_log, conforme a fórmula assinada (bench.py:261-262).
4. Manter flavor e inferencia_s na impressão (bench.py:256).
5. Trocar 'PBI-000H' na docstring de bench.py:5 pelo ID do Azure DevOps de F4.6.
6. Escrever em tests/test_bench_metricas.py os testes dos critérios 1 ou 2 (ramo assinado), 6 e 7.

**Definição de pronto:** Os testes escritos na task passam; busca por 'PBI-000H' em bench.py sem resultado; ruff check sem erro.

**Dependências:** nenhuma

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F1.4.T2 · [Backend] Fazer o validador exigir os mínimos assinados, acusar intervalo sem segundo amostrado e aceitar URI do dataset</summary>

**Objetivo:** tools/validar_labels.py recusa os rótulos que o bench mediria errado e lê o corpus do dataset.

**Passos previstos:**
1. Trocar a exigência de 1 riso pelo mínimo assinado em F1.3 (validar_labels.py:216-217).
2. Aplicar o mínimo de trechos neutros da forma de jitter assinada (corpus inteiro ou mesmo vídeo) (validar_labels.py:218-220).
3. Em validar_eventos, acusar intervalo que não contém nenhum segundo inteiro dentro da grade do vídeo (validar_labels.py:99-123).
4. Aceitar --corpus hf://datasets/... reaproveitando a resolução de bench.py:58-70 e apagando /dev/shm ao fim.
5. Escrever em tests/test_validar_labels.py os testes dos critérios 3, 4 e 8 e do mínimo de neutros, com download simulado.

**Definição de pronto:** Os testes escritos na task passam; ruff check sem erro.

**Dependências:** nenhuma

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F1.4.T3 · [Backend] Excluir o concatenado por padrão no validador e no bench</summary>

**Objetivo:** igreja_simples_concat.mp4 fica fora da validação e do bench por padrão, com aviso na saída.

**Passos previstos:**
1. Deixar igreja_simples_concat.mp4 fora por padrão em tools/validar_labels.py:189 e bench.py:206, com mensagem na saída.
2. Escrever testes unitários das duas ferramentas com uma pasta de arquivos sintéticos que inclui um igreja_simples_concat.mp4.
3. Não alterar tools/preparar_rotulagem.py nem labels/README.md, que F3.5.T6 retira e reescreve.

**Definição de pronto:** Os testes escritos na task passam nas duas ferramentas; o diff do PR não altera tools/preparar_rotulagem.py nem labels/README.md; ruff check sem erro.

**Dependências:** nenhuma

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F1.4.T4 · [QA] Verificar os critérios de aceite do bench e do validador</summary>

**Objetivo:** Cada critério de aceite de F1.4 do ramo assinado em F1.3 tem teste, e os testes falham sem as correções.

**Passos previstos:**
1. Rodar os testes de F1.4.T1 a T3 no commit anterior e no final e registrar que falham antes e passam depois.
2. Acrescentar casos de borda: riso que termina exatamente num segundo inteiro, clipe sem nenhum rótulo e pasta só com o concatenado.
3. Capturar a saída do bench e conferir a regra do critério 5 e as colunas flavor e inferencia_s.
4. Conferir no diff que tools/preparar_rotulagem.py e labels/README.md não mudaram.
5. Conferir o ID de F4.6 na docstring de bench.py e a busca por 'PBI-000H' no repositório sem resultado.
6. Conferir o CI no PR.

**Definição de pronto:** Registro no PR com o resultado de cada critério; os testes falham no commit anterior e passam no final; CI verde.

**Dependências:** F1.4.T1, F1.4.T2, F1.4.T3

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- bench.py:5-31 (docstring cita PBI-000H, mapeado pela árvore a F4.6), 58-81,137-159,162-183,206,254-264
- tools/validar_labels.py:17-21,99-133,158-169,189,215-220
- tests/test_validar_labels.py:66-68
- labels/README.md:3-14,28,36
- tools/preparar_rotulagem.py:43-60
- tools/rodar_teste.sh:35-40,54-56 (commit 5176bc3)
- F3.5.T6 e F3.1.T8 (F3 revisada)
- docs/poc-gate.md:3-4,10,13,35-40
- samples/corpus/pib/README.md:7,11-12 (não versionado)
- mapa_medicao do levantamento, fatos 15-17 e lacuna 51
- arvore_v1.json, destino dos IDs antigos: PBI-000H → F4.6

#### Verificação INVEST: pontos que falharam
- Independente: depende dos valores assinados em F1.3.

#### Premissas
- Estimativas (story points e horas) são sugestão, a validar no refinamento.
- A forma do jitter, o mínimo de risos e a fórmula do critério 5 são lidos dos valores assinados em F1.3. Sem F1.3 assinado, o PBI não começa. Só os critérios do ramo assinado são verificados.
- O validador usa a função de grade de reacao/ingest.py. Se F1.2 entrar antes, a regra nova do tempo do quadro vale sem mudança neste PBI.
- Até F3.5.T6, os comandos de labels/README.md:28,36 continuam como estão. Este PBI não os corrige, para que cada arquivo tenha um só destino no backlog.
- F1.4.T2 e F3.5.T6 alteram tools/validar_labels.py em trechos diferentes: código de validação e leitura por URI aqui, docstring (linhas 4-5) em F3.5.T6.
- Onde o validador roda depois que F3.1 retirar as cópias locais (Space de rotulagem ou job) é decisão de F3.1 e F3.4.
- O ID do Azure DevOps de F4.6 existe antes de F1.4.T1, porque a sincronização da árvore cria os itens antes da sprint.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Vínculo de dependência com F1.3 no Azure DevOps
- Avisar F3.3 de que a ferramenta de rotulagem não deve listar igreja_simples_concat.mp4
- ID do Azure DevOps de F4.6 criado antes de F1.4.T1
- Validar os 5 story points sugeridos

## Preview — PBI F1.5 (novo) · Alinhar o run_log à migração do Supabase e gravar o hardware real de cada execução

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Alinhar o run_log à migração do Supabase e gravar o hardware real de cada execução |
| Tipo | Product Backlog Item |
| Pai | F1 |
| Tags | fase-0; gate; supabase; run-log; critério-4; critério-5 |
| Estimativa | 3 pts (sugestão); tasks: 15 h |
| Dependências | nenhuma |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro, que lê custo e tempo por hora de vídeo no run_log  
Quero que o run_log seja gravado no Supabase sem erro e registre o hardware em que a execução rodou  
Para que o critério 4 leia insights_rejeitados_pelo_lint e o critério 5 não confunda execução em CPU com t4-small

**Contexto:** processar_culto.py:104-106 envia insights_rejeitados_pelo_lint ao run_log, e a tabela de supabase/migrations/0001_init.sql:18 não tem essa coluna. O Store levanta exceção quando o envio falha (reacao/store.py:24-26). O critério 4 usa esse campo (docs/poc-gate.md:12). O flavor vem de HF_JOB_FLAVOR ou do padrão t4-small (processar_culto.py:42). O HF Jobs define JOB_ID e ACCELERATOR, e ACCELERATOR vale none em job só de CPU (https://huggingface.co/docs/hub/jobs-configuration#built-in-environment-variables). O script de lançamento de F1.1 passa --flavor ao script depois de '--' (F1.1 RN06). As duas execuções locais em CPU ficaram em out/run_log.json com flavor t4-small e custo da T4. reacao/cost.py:5 tem preço 0 para 'local'. O projeto Supabase de desenvolvimento não foi encontrado (épico, dependências), e F2.6, que o cria, depende deste PBI. Por isso a confirmação é feita numa pilha local do Supabase CLI, que aplica as migrações do repositório (https://supabase.com/docs/guides/local-development/cli-workflows). O repositório tem supabase/migrations/ e não tem supabase/config.toml. CONTRIBUTING.md:13 pede issue antes de mudar o schema.

**Regras de negócio:**
- RN01 – Uma migração nova acrescenta insights_rejeitados_pelo_lint (inteiro) ao run_log, sem campo por pessoa (CLAUDE.md, regra 6).
- RN02 – Uma issue é aberta antes da mudança de schema (CONTRIBUTING.md:13).
- RN03 – Todo campo que o Store envia a uma tabela existe nas migrações. Um teste de contrato verifica isso.
- RN04 – Em job do HF (JOB_ID definido) com ACCELERATOR diferente de none, o flavor gravado é o valor de ACCELERATOR.
- RN05 – Em job do HF com ACCELERATOR igual a none, o flavor gravado é o --flavor passado pelo script de lançamento de F1.1.
- RN06 – Em job do HF com ACCELERATOR igual a none e sem --flavor, processar_culto.py sai com erro antes de abrir o vídeo e não grava run_log (regra a confirmar no Definition of Ready).
- RN07 – Fora do HF, o flavor gravado é 'local', com custo 0 (reacao/cost.py:5), salvo se --flavor for informado.
- RN08 – HF_JOB_FLAVOR deixa de ser lida, porque o HF não a define.
- RN09 – F2.5 (run_id e registro de falha) e F2.8 (linhagem) reutilizam o flavor resolvido aqui, sem ler ACCELERATOR de novo.
- RN10 – A migração só acrescenta a coluna, sem grant nem política. RLS fica em F2.6; papéis e políticas do avaliador do gate, em F5.6 (F5.6.T3, F5.6.T4); perfis do piloto, em F7.2 e F7.8. run_log não está entre as tabelas que o painel web na Vercel lê (D7 de F2.4.T4; F5.6 RN01).

**Fora de escopo:**
- Linhagem por execução (F2.8) e run_id (F2.5)
- Criar o projeto Supabase de desenvolvimento e aplicar nele as migrações (F2.6)
- RLS (F2.6), papéis e políticas do avaliador do gate (F5.6) e perfis do piloto (F7.2, F7.8)
- Granularidade de cobrança do HF Jobs (F5.4, P21)
- Preços de flavors que não estão em reacao/cost.py:5

#### Critérios de aceite

- Numa pilha local do Supabase com as migrações do repositório aplicadas, uma execução com a URL e a chave da pilha grava uma linha em run_log com insights_rejeitados_pelo_lint preenchido e termina com código 0.
- O teste de contrato passa com o código e as migrações do PR.
- O teste de contrato falha, citando a tabela e o campo, quando o código envia a uma tabela um campo que nenhuma migração cria.
- Uma execução local em CPU sem --flavor grava flavor 'local' e custo_usd 0.
- Com JOB_ID definido e ACCELERATOR=t4-small, o run_log grava t4-small e o custo pelo preço de t4-small em reacao/cost.py.
- Com JOB_ID definido, ACCELERATOR=none e --flavor cpu-basic, o run_log grava cpu-basic.
- Com JOB_ID definido, ACCELERATOR=none e sem --flavor, processar_culto.py sai com código diferente de 0 antes de abrir o vídeo, com mensagem que pede o --flavor, e nenhuma linha de run_log é gravada.
- tests/test_schema.py passa com a nova migração.
- O PR cita a issue aberta antes da mudança de schema.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F1.5.T1 | Backend | Abrir a issue de schema, criar a migração com insights_rejeitados_pelo_lint e a configuração local do Supabase CLI | 3 | — |
| F1.5.T2 | MLOps | Gravar no run_log o hardware real a partir de JOB_ID, ACCELERATOR e --flavor | 4 | — |
| F1.5.T3 | QA | Escrever o teste de contrato entre os registros do Store e as colunas das migrações | 4 | F1.5.T1 |
| F1.5.T4 | QA | Verificar a gravação do run_log numa pilha local do Supabase e os critérios de hardware | 4 | F1.5.T1, F1.5.T2 |

<details><summary>F1.5.T1 · [Backend] Abrir a issue de schema, criar a migração com insights_rejeitados_pelo_lint e a configuração local do Supabase CLI</summary>

**Objetivo:** Existe supabase/migrations/0002 com a coluna nova, e o repositório permite subir a pilha local com as migrações.

**Passos previstos:**
1. Abrir a issue que descreve a mudança de schema (CONTRIBUTING.md:13).
2. Criar a migração que acrescenta insights_rejeitados_pelo_lint int ao run_log, sem grant nem política.
3. Gerar a configuração local do Supabase CLI (supabase init) sem segredo versionado.
4. Rodar tests/test_schema.py.

**Definição de pronto:** A pilha local sobe e aplica 0001 e 0002 sem erro; tests/test_schema.py passa; a issue está citada no PR.

**Dependências:** nenhuma

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F1.5.T2 · [MLOps] Gravar no run_log o hardware real a partir de JOB_ID, ACCELERATOR e --flavor</summary>

**Objetivo:** O flavor gravado reflete onde a execução rodou, o custo sai do preço desse flavor, e job de CPU sem --flavor sai com erro.

**Passos previstos:**
1. Trocar a leitura de HF_JOB_FLAVOR (processar_culto.py:42) pelas regras RN04 a RN07.
2. Validar o flavor antes de abrir o vídeo, para que a saída com erro de RN06 não grave run_log.
3. Manter o cálculo de custo em reacao/cost.py com o flavor resolvido.
4. Documentar no --help a origem do flavor.
5. Escrever os testes com variáveis de ambiente simuladas para os critérios 4 a 7.

**Definição de pronto:** Os testes escritos na task para os critérios 4 a 7 passam; ruff check sem erro.

**Dependências:** nenhuma

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F1.5.T3 · [QA] Escrever o teste de contrato entre os registros do Store e as colunas das migrações</summary>

**Objetivo:** Um teste falha quando o código envia a uma tabela um campo que as migrações não criam.

**Passos previstos:**
1. Ler as colunas de cada tabela a partir de supabase/migrations/*.sql, em ordem.
2. Montar os registros que processar_culto.py e o Store enviam para window_aggregate, transcript_segment, moment, event, insight e run_log.
3. Comparar os campos e falhar citando tabela e campo.
4. Conferir que o teste falha sem a migração 0002 e passa com ela.

**Definição de pronto:** O teste roda no pytest do CI, falha sem 0002 e passa com 0002.

**Dependências:** F1.5.T1

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F1.5.T4 · [QA] Verificar a gravação do run_log numa pilha local do Supabase e os critérios de hardware</summary>

**Objetivo:** Fica demonstrado que o run_log grava sem erro com as migrações do repositório, que o envio falha sem a coluna e que os critérios de hardware passam.

**Passos previstos:**
1. Subir a pilha local só com a 0001 e rodar processar_culto.py com a fixture sintética e o motor mock; registrar a falha do envio (confirma a P20).
2. Aplicar a 0002 e repetir; registrar código 0 e a linha gravada.
3. Conferir flavor 'local' e custo 0 na linha gravada.
4. Rodar os testes de F1.5.T2 no commit anterior e no final e registrar que falham antes e passam depois.

**Definição de pronto:** As duas execuções e seus resultados estão registrados no PR; os critérios 1 e 4 a 7 passam.

**Dependências:** F1.5.T1, F1.5.T2

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- processar_culto.py:42,59,103-107
- reacao/store.py:9-44
- reacao/cost.py:1-25
- supabase/migrations/0001_init.sql:17-18,21
- tests/test_schema.py
- out/run_log.json (local, não versionado)
- https://huggingface.co/docs/hub/jobs-configuration#built-in-environment-variables
- https://supabase.com/docs/guides/local-development/cli-workflows
- docs/poc-gate.md:12-13
- CONTRIBUTING.md:13
- references/work-items.md:174 (critério que depende de decisão não tomada vira premissa)
- Premissa P20 da árvore
- feature_det_F2.json da sessão: F2.4.T4 (D7, tabelas do painel), F2.5 e F2.8 (dependência de F1.5)
- feature_det_F5.json da sessão: F5.6 RN01, F5.6.T3 e F5.6.T4

#### Premissas
- Estimativas (story points e horas) são sugestão, a validar no refinamento.
- Definition of Ready: RN06 e o critério 7 (sair com erro quando o job só de CPU não recebe --flavor) são proposta desta revisão, a confirmar por Fabio Pinheiro antes da sprint. Motivo: o script de lançamento de F1.1 sempre passa --flavor, então um job de CPU sem --flavor foi lançado fora dele e gravaria custo sem base. Se a decisão for outra, RN06 e o critério 7 são reescritos com o valor exato de flavor e custo_usd antes da sprint.
- A falha do envio sem a coluna (P20) é dedução do levantamento. F1.5.T4 a confirma na pilha local, e F2.6 repete a conferência no projeto de desenvolvimento.
- A pilha local exige Supabase CLI e runtime compatível com Docker na máquina de quem testa (https://supabase.com/docs/guides/local-development).
- O valor de ACCELERATOR num job real é conferido nos jobs de fumaça de F2.2 (cpu-basic e t4-small). Aqui ele é simulado por variável de ambiente.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Número da issue de schema aberta em F1.5.T1
- Registrar no Definition of Ready a decisão sobre job de CPU sem --flavor
- Validar os 3 story points sugeridos

## Preview — PBI F1.6 (novo) · Executar no CI os motores reais em CPU e um teste da regra 2 sobre vídeo de teste com rostos

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Executar no CI os motores reais em CPU e um teste da regra 2 sobre vídeo de teste com rostos |
| Tipo | Product Backlog Item |
| Pai | F1 |
| Tags | fase-0; gate; critério-6; regra-2; ci; visão-computacional |
| Estimativa | 8 pts (sugestão); tasks: 20 h |
| Dependências | F2.1, F4.3 |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro, que revisa os PRs antes dos jobs pagos  
Quero que o CI rode o detector, o motor de expressão e a pose reais em CPU, dentro da guarda, sobre um vídeo curto com rostos, sem nenhum modelo de reconhecimento no ambiente, e falhe se o detector expuser um módulo de reconhecimento  
Para que regressões nos motores reais e na barreira da regra 2 apareçam no PR, antes de qualquer job pago, e que o critério 6 exercite o caminho real de detecção e recorte

**Contexto:** .github/workflows/ci.yml:9 instala só dev, opencv e numpy. Os passos 12-17 geram a fixture sem rosto e rodam o pipeline com o motor mock, que fabrica as observações (processar_culto.py:70-71; tests/fixtures/README.md:11-13). A busca por termos de reconhecimento cobre só reacao/ e usa --include=*.py (ci.yml:17). tools/rodar_teste.sh:33 (commit 5176bc3; F3.1.T8 remove o script) contém 'face-emotion-recognition' na URL do HSEmotion. O CLAUDE.md, na regra 2, diz que há teste que falha se um módulo de reconhecimento aparecer. Hoje existe só a asserção em tempo de execução de reacao/detect.py:17-18, que roda depois de FaceAnalysis e prepare (detect.py:14-16), e nenhum teste a exercita. O insightface baixa e extrai o zip buffalo_sc inteiro, com w600k_mbf.onnx, e não apaga o zip (insightface/utils/storage.py:27-36, linha 34 comentada). O FaceAnalysis do insightface 2.0 abre uma sessão ONNX para cada .onnx da pasta, inclusive o de reconhecimento, antes de filtrar por allowed_modules (insightface/app/face_analysis.py:132-140; insightface/model_zoo/model_zoo.py:121). A asserção de detect.py:17-18 olha só app.models e não percebe essa carga. O PR #3, em rascunho, corrige a pose que quebra com float() sobre array de forma (1,) no NumPy 2.4 (reacao/pose.py no branch do PR) e traz tests/test_pose.py, com modelo falso, que falha com float() e roda no pytest do CI (ci.yml:11). F2.1 mescla o PR #3. O extra gpu instala onnxruntime-gpu (pyproject.toml:14-20), e F2.1 resolve o conflito com o onnxruntime de CPU. O pré-filtro de plateia descarta quadro com menos de 5 rostos no quadro reduzido, e o limite é configurável por --min-faces-plateia (processar_culto.py:41,73-75). Os pesos pré-treinados do insightface servem só para pesquisa não comercial (insightface-2.0.dist-info/METADATA:50-54); F4.3 registra as licenças. O PBI se apoia na exceção P26 da árvore (CI no GitHub Actions com vídeo licenciado sem pessoas da congregação), que a P3 revisada não cita.

**Regras de negócio:**
- RN01 – O vídeo de teste tem licença que permite uso em teste e não contém pessoas da congregação. Origem, licença e SHA-256 ficam registrados em tests/fixtures/README.md, e o vídeo não é versionado (P18; *.mp4 no .gitignore).
- RN02 – O vídeo é baixado para /dev/shm com verificação de SHA-256 antes de rodar. Divergência falha o passo antes do pipeline.
- RN03 – O teste roda sem transcrição (CLAUDE.md, regra 5).
- RN04 – Do insightface, só o módulo de detecção pode ser carregado (CLAUDE.md, regra 2; reacao/detect.py:14-18). No CI, w600k_mbf.onnx e buffalo_sc.zip são apagados depois do download e antes do teste e do salvamento do cache, e o cache guarda só det_500m.onnx e os pesos de expressão e pose.
- RN05 – A barreira do detector é verificada com um dublê do FaceAnalysis cujo app.models contém a chave 'recognition'. Nenhum teste nem branch de verificação carrega peso de reconhecimento.
- RN06 – A busca por termos de reconhecimento cobre reacao/, bench.py, processar_culto.py e tools/, mantendo --include=*.py.
- RN07 – No passo de integração do CI, o teste não pode ser pulado: a falta de uma dependência dos motores falha o passo.
- RN08 – O passo do critério 6 com o motor mock continua no CI.
- RN09 – A verificação de ausência de w600k_mbf.onnx nos jobs do HF e na imagem, e a troca da origem dos pesos, ficam em F2.3.
- RN10 – O PBI só entra numa sprint com a exceção P26 do CI confirmada por Fabio Pinheiro sob a P3 revisada e com a decisão de uso no CI dos pesos do detector, do HSEmotion e do 6DRepNet registrada em F4.3.
- RN11 – O vídeo de teste é processado só no CI do GitHub Actions, que é a exceção da P26. Nenhuma task o processa na máquina de quem desenvolve (P3 revisada).

**Fora de escopo:**
- Troca da origem dos pesos para repositórios de modelo privados (F2.3)
- Leitura das licenças dos pesos (F4.3)
- Teste de regressão do float() na pose (tests/test_pose.py, entregue pelo PR #3 via F2.1)
- Motores LibreFace e Py-Feat (F4.1, F4.2)
- Execução em GPU
- Medir acurácia com o vídeo de teste

#### Critérios de aceite

- O CI tem um passo que roda o detector SCRFD, o HSEmotion e o 6DRepNet em CPU, dentro da guarda, sobre o vídeo de teste com rostos, e termina com '[guard] ok' e código 0.
- Nesse passo, pelo menos um rosto com altura ≥ 64 px recebe probabilidade de sorriso, pitch e yaw numéricos.
- Com um dublê do FaceAnalysis cujo app.models contém 'recognition', o carregamento do detector falha, e nenhum peso de reconhecimento é carregado.
- No passo de integração, antes da criação do FaceAnalysis, a pasta de modelos do insightface não contém w600k_mbf.onnx nem buffalo_sc.zip; se contiver, o passo falha antes de criar o FaceAnalysis. O cache do Actions salvo não contém esses arquivos.
- No passo de integração do CI, o teste não é pulado. Com uma dependência dos motores ausente, o passo falha.
- A busca textual por termos de reconhecimento cobre reacao/, bench.py, processar_culto.py e tools/, mantém --include=*.py e falha quando encontra um termo fora das exceções atuais.
- Se o vídeo baixado não bater com o SHA-256 registrado, o passo falha antes de rodar o pipeline.
- tests/fixtures/README.md registra origem, licença, SHA-256 e a ausência de pessoas da congregação no vídeo de teste.
- O passo do critério 6 com o motor mock continua passando.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F1.6.T1 | Governança e Privacidade | Selecionar e registrar o vídeo de teste com rostos | 3 | — |
| F1.6.T2 | Visão Computacional | Escrever o teste de integração dos motores reais em CPU e o teste da barreira com dublê | 7 | F1.6.T1 |
| F1.6.T3 | DevOps | Criar no CI o passo de integração em CPU sem modelo de reconhecimento e estender a busca por reconhecimento | 7 | F1.6.T1, F1.6.T2 |
| F1.6.T4 | QA | Verificar por mutação que o CI falha nas regressões da barreira, do hash e das dependências | 3 | F1.6.T3 |

<details><summary>F1.6.T1 · [Governança e Privacidade] Selecionar e registrar o vídeo de teste com rostos</summary>

**Objetivo:** Há um vídeo curto com rostos, com licença para teste, sem pessoas da congregação, com origem, licença e SHA-256 registrados.

**Passos previstos:**
1. Levantar candidatos com licença que permita uso em teste e rostos com altura ≥ 64 px.
2. Confirmar que o vídeo não contém pessoas da congregação.
3. Calcular o SHA-256 e registrar origem, licença e hash em tests/fixtures/README.md.

**Definição de pronto:** tests/fixtures/README.md com origem, licença, SHA-256 e declaração sobre a congregação, revisado por Fabio Pinheiro.

**Dependências:** nenhuma

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F1.6.T2 · [Visão Computacional] Escrever o teste de integração dos motores reais em CPU e o teste da barreira com dublê</summary>

**Objetivo:** Um teste roda detecção, recorte, expressão e pose reais sobre o vídeo de teste sem modelo de reconhecimento no ambiente, e outro verifica a barreira da regra 2 com dublê.

**Passos previstos:**
1. Antes de criar o FaceAnalysis, conferir que a pasta de modelos do insightface não contém w600k_mbf.onnx nem buffalo_sc.zip e falhar se contiver.
2. Rodar o provider hsemotion com pose sobre quadros do vídeo, dentro da guarda, e conferir p_smile, pitch e yaw numéricos em rostos mensuráveis.
3. Rodar processar_culto.py com --no-transcribe e --min-faces-plateia 1 sobre o vídeo e conferir '[guard] ok' e código 0.
4. Escrever o teste que troca FaceAnalysis por um dublê cujo app.models contém 'recognition' e confere que o carregamento do detector falha.
5. Fazer o teste de integração pular só quando faltarem as dependências dos motores e virar falha quando uma variável de ambiente do CI estiver definida.

**Definição de pronto:** O teste do dublê passa localmente, sem vídeo; com a variável de ambiente definida e uma dependência ausente, o teste de integração falha em vez de pular; a execução do teste de integração com o vídeo registrado acontece no CI, em F1.6.T3 (RN11).

**Dependências:** F1.6.T1

**Estimativa sugerida:** 7 h (sugestão; validar com o time)

</details>

<details><summary>F1.6.T3 · [DevOps] Criar no CI o passo de integração em CPU sem modelo de reconhecimento e estender a busca por reconhecimento</summary>

**Objetivo:** O CI instala os motores em CPU, baixa o vídeo com verificação de hash, apaga o modelo de reconhecimento antes do teste e do cache, roda o teste de integração sem pulo e busca termos de reconhecimento no código Python do produto.

**Passos previstos:**
1. Instalar as dependências travadas por F2.1, com onnxruntime e torch de CPU.
2. Baixar o vídeo para /dev/shm e verificar o SHA-256 antes de rodar.
3. Depois do download dos pesos do insightface, apagar w600k_mbf.onnx e buffalo_sc.zip, antes do teste e antes de salvar o cache.
4. Guardar em cache do Actions só det_500m.onnx e os pesos de expressão e pose.
5. Definir no passo a variável de ambiente que transforma o pulo do teste em falha.
6. Rodar os testes de F1.6.T2 e registrar a duração do passo.
7. Estender a busca de ci.yml:17 a bench.py, processar_culto.py e tools/, mantendo --include=*.py.

**Definição de pronto:** O CI verde no PR mostra o passo novo, com o teste de integração executado sobre o vídeo registrado, e o passo do motor mock; a listagem do cache salvo não tem w600k_mbf.onnx nem buffalo_sc.zip; a duração do passo novo está registrada no PR.

**Dependências:** F1.6.T1, F1.6.T2

**Estimativa sugerida:** 7 h (sugestão; validar com o time)

</details>

<details><summary>F1.6.T4 · [QA] Verificar por mutação que o CI falha nas regressões da barreira, do hash e das dependências</summary>

**Objetivo:** Fica demonstrado que o CI falha quando a barreira do detector some, quando o hash do vídeo diverge, quando o modelo de reconhecimento fica na pasta e quando falta uma dependência dos motores, sem carregar peso de reconhecimento.

**Passos previstos:**
1. Abrir um branch que retira a asserção de reacao/detect.py:17-18 e registrar a falha do teste do dublê no CI.
2. Abrir um branch que deixa de apagar w600k_mbf.onnx e registrar a falha antes da criação do FaceAnalysis.
3. Abrir um branch com SHA-256 errado do vídeo e registrar a falha antes do pipeline.
4. Abrir um branch que retira uma dependência dos motores do passo e registrar a falha, sem pulo.
5. Apagar os branches de mutação depois do registro.

**Definição de pronto:** Os links das quatro execuções que falharam e da execução verde estão no PR; os critérios 3, 4, 5 e 7 são conferidos.

**Dependências:** F1.6.T3

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- .github/workflows/ci.yml:9-17
- processar_culto.py:41,70-76
- tests/fixtures/README.md:11-13
- CLAUDE.md (regra 2)
- reacao/detect.py:9-19
- reacao/pose.py e tests/test_pose.py:6-16 (branch do PR #3)
- reacao/providers/hsemotion.py:10-34 (branch do PR #3)
- insightface/utils/storage.py:27-36 (instalado)
- insightface/app/face_analysis.py:132-140 e insightface/model_zoo/model_zoo.py:121 (insightface 2.0 instalado)
- ~/.insightface/models/buffalo_sc com det_500m.onnx e w600k_mbf.onnx, e ~/.insightface/models/buffalo_sc.zip, nesta sessão
- insightface-2.0.dist-info/METADATA:50-54 (instalado)
- tools/rodar_teste.sh:30,33 (commit 5176bc3)
- pyproject.toml:14-20
- PR #3
- Premissas P18 e P26 da árvore; P3 revisada
- feature_det_F4.json da sessão: F4.3 RN03 (três usos registrados)
- feature_det_F2.json da sessão: F2.4.T4 (D7, decisão sobre a exceção da P26)
- feature_det_F5.json da sessão: F5.3, premissas (leitura da P26)

#### Verificação INVEST: pontos que falharam
- Independente: depende de F2.1, de F4.3, da confirmação da P26 e de uma fonte de vídeo ainda a definir (P18).

#### Premissas
- Estimativas (story points e horas) são sugestão, a validar no refinamento.
- Definition of Ready: Fabio Pinheiro confirma que a exceção P26 continua valendo sob a P3 revisada. Sem essa confirmação, o PBI volta ao refinamento, porque mover o teste para um job do HF contraria a RN10 da Feature (sem job pago). F2.4.T4 (D7) registra a decisão de Fabio Pinheiro sobre a exceção da Anthropic da P26; a pendência pede que registre também a do CI, e então o Definition of Ready passa a apontar para o ADR 0002.
- Definition of Ready: F4.3 registrou a licença dos pesos do insightface, do HSEmotion e do 6DRepNet para uso no CI. Se a leitura vetar o uso, o PBI volta ao refinamento. F4.3 registra hoje três usos (PoC no HF Jobs, espelhamento e piloto; F4.3 RN03), e a pendência pede o uso no CI.
- O teste pode usar --min-faces-plateia 1 para não exigir 5 rostos por quadro no vídeo de teste.
- Até F2.3, os pesos são baixados das origens atuais com cache no CI, sem o modelo de reconhecimento. tools/rodar_teste.sh:30 (commit 5176bc3) registra 403 do proxy desta sessão para a URL do HSEmotion usada pelo pacote; F3.1.T8 leva essa nota para docs/hf-jobs.md ao remover o script. O comportamento no GitHub Actions não foi medido.
- Apagar w600k_mbf.onnx dentro de buffalo_sc não dispara novo download, porque o insightface só baixa quando a pasta não existe (insightface/utils/storage.py:22-24).
- O tempo do passo em CPU não foi medido; F1.6.T3 o registra.
- O vídeo de teste fica fora do repositório e é baixado em /dev/shm.
- A execução só no CI segue a leitura da P26 feita em F5.3 (premissas): as exceções cobrem o CI e o docker run com a fixture sintética; execução local com o motor real fica fora delas.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Vínculos de dependência com F2.1 e F4.3 no Azure DevOps
- Confirmação de Fabio Pinheiro sobre a exceção P26 sob a P3 revisada
- Fonte do vídeo de teste (P18)
- Responsável de governança para F1.6.T1
- Pedir a F2.4.T4 (D7) o registro da confirmação da exceção do CI da P26, junto da decisão sobre a exceção da Anthropic
- Pedir a F4.3 a decisão de uso no CI (RN03 e F4.3.T3)
- Validar os 8 story points sugeridos

## Preview — PBI F1.7 (novo) · Bloquear no lint conjugações, sinônimos de estado interno e referências a pessoa ou setor

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Bloquear no lint conjugações, sinônimos de estado interno e referências a pessoa ou setor |
| Tipo | Product Backlog Item |
| Pai | F1 |
| Tags | fase-0; gate; critério-4; regra-4; lint; linguagem-controlada |
| Estimativa | 5 pts (sugestão); tasks: 19 h |
| Dependências | nenhuma |
| Substitui | nenhum |

#### Descrição

Como pastor Filipe, que lê os insights no painel web na Vercel  
Quero que nenhum texto do sistema diga o que a congregação sentiu ou aponte uma pessoa ou um setor  
Para receber só descrição de reação observada, com minuto, momento, trecho citado e sinais, como exige a regra 4 do CLAUDE.md

**Contexto:** reacao/lint.py:8-13 proíbe radicais de estado interno e algumas referências individuais, por expressão regular aplicada ao texto fora da citação, sem contexto (lint.py:25-31). A regex '\bfelizes?\b' exige o 'e' e não pega 'feliz' no singular (lint.py:9). Numa sondagem de 20 frases reproduzida em 2026-09-23 com reacao.lint.check, com cada frase dentro de um Insight válido, 19 passaram. Estado interno: estava feliz, se entediou, se emocionou, se alegrou, gostou, cansou, se distraiu, se comoveu, ficou concentrada, engajada ou interessada, prestou atenção, amou a mensagem, ficou com sono. Pessoa ou setor: um membro, um jovem no banco da frente, o lado esquerdo da igreja, a irmã da ala direita, uma criança. Só 'ficou entediada' foi rejeitada. check() reprova frase solta por falta de minuto, momento, trecho ou aspas, qualquer que seja o vocabulário (lint.py:32-48). A citação literal do púlpito fica isenta (lint.py:16-20; tests/test_lint.py:60-85). O modelo de frase usa 'queda de atenção aparente', 'recuperação de atenção aparente' e 'pico de sorriso' (reacao/insights.py:8,21-24), então 'atenção' sozinha não pode ser proibida. Termos como 'lado', 'banco' e 'setor' também aparecem em uso comum ('por outro lado', 'banco de dados', 'setor de mídia'). O critério 4 conta os insights aprovados pelo lint (docs/poc-gate.md:12). A regra 4 do CLAUDE.md exige minuto, momento, trecho citado e sinais em todo texto para pastores (CLAUDE.md:17-19). Pela P3 revisada, os textos para pastores aparecem no painel web na Vercel, e os textos fixos de interface (rótulos, títulos, mensagens) não têm minuto, momento nem trecho.

**Regras de negócio:**
- RN01 – O conjunto versionado de frases aceitas e rejeitadas contém, no mínimo, as 20 frases da sondagem. A governança o revisa antes da mudança no lint.
- RN02 – 'feliz' no singular é rejeitado.
- RN03 – São rejeitados, no mínimo, estes termos de estado interno e suas conjugações: se entediou, se emocionou, se alegrou, gostou, cansou, se distraiu, se comoveu, ficou concentrada, engajada ou interessada, prestou atenção, amou, ficou com sono.
- RN04 – São rejeitadas, no mínimo, as frases do conjunto com estas referências a pessoa ou setor: membro, jovem, criança, irmão, irmã, banco, lado, ala, setor (CLAUDE.md, regra 3: nenhuma métrica por assento, setor pequeno ou pessoa).
- RN05 – O conjunto inclui frases com os mesmos termos em uso que não se refere a pessoas ('por outro lado', 'banco de dados', 'setor de mídia'). O resultado esperado de cada uma é decidido pela governança em F1.7.T2.
- RN06 – Continuam aprovados os textos do modelo de frase dos três tipos de evento (reacao/insights.py:8,21-24).
- RN07 – A citação literal do púlpito continua isenta. O mesmo termo fora da citação é rejeitado (lint.py:16-20).
- RN08 – O conjunto roda como teste no CI.
- RN09 – O lint oferece verificação só de vocabulário, como função pública que devolve os termos apontados e por linha de comando com código de saída diferente de 0 quando há termo proibido, apenas para textos fixos de interface do painel web na Vercel. O teste de F5.6.T5 usa essa função sobre o arquivo de textos fixos criado em F5.6.T1, no pytest do CI. Texto de insight, inclusive o editado na revisão (F7.3), passa pelo check(Insight) completo, com minuto, momento, trecho citado e sinais (CLAUDE.md:17-19; reacao/lint.py:23-49).
- RN10 – O conjunto de frases e o embrulho fixo usado para medir frases soltas (minuto, momento e trecho) ficam num arquivo legível fora do Python (CSV ou JSON). Uma frase conta como aprovada quando não tem erro de vocabulário.

**Fora de escopo:**
- Redação legível e ordem cronológica dos insights (F5.2)
- Arquivo de textos fixos do painel (F5.6.T1), teste que os passa pelo lint no CI (F5.6.T5) e aplicação do lint à edição de texto na revisão (F7.3)
- Prompt do LLM de insights (F5.2)
- Lint em outros idiomas

#### Critérios de aceite

- As 20 frases da sondagem estão no conjunto versionado, marcadas como rejeitadas. O registro da linha de base, medido com o embrulho fixo versionado, mostra 19 delas aprovadas pelo lint antes da mudança, e depois da mudança nenhuma é aprovada.
- 'A congregação estava feliz' é rejeitada.
- Frases com se entediou, se emocionou, prestou atenção, ficou com sono, engajada e concentrada são rejeitadas.
- Todas as frases do conjunto marcadas como rejeitadas por referência a pessoa ou setor (com membro, jovem, criança, irmão, irmã, banco, lado, ala e setor) são rejeitadas.
- As frases do conjunto com esses termos em uso que não se refere a pessoas têm no lint o resultado registrado pela governança em F1.7.T2.
- Os textos do modelo de frase para queda de atenção aparente, recuperação de atenção aparente e pico de sorriso continuam aprovados.
- Uma citação literal do púlpito com vocabulário proibido continua isenta, e o mesmo termo fora da citação é rejeitado. Os testes de tests/test_lint.py passam.
- O registro de revisão da governança tem data anterior ao commit que altera reacao/lint.py.
- O conjunto roda no CI, e uma frase marcada como rejeitada que passe no lint faz o CI falhar.
- Um texto fixo de interface verificado pela linha de comando sai com código diferente de 0 quando contém termo proibido e com código 0 quando não contém, e a função pública devolve os termos apontados no primeiro caso e nenhum no segundo.
- Um insight sem minuto ou sem trecho citado é rejeitado pelo check(Insight), mesmo sem termo proibido; a verificação só de vocabulário não é usada para texto de insight.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F1.7.T1 | Data Science | Montar o conjunto versionado de frases e o embrulho fixo e medir a linha de base | 6 | — |
| F1.7.T2 | Governança e Privacidade | Revisar e aprovar o conjunto de frases antes da implementação | 2 | F1.7.T1 |
| F1.7.T3 | Backend | Ampliar o vocabulário do lint e expor a verificação de textos fixos por linha de comando | 8 | F1.7.T2 |
| F1.7.T4 | QA | Rodar o conjunto como teste no CI e verificar os critérios de aceite | 3 | F1.7.T3 |

<details><summary>F1.7.T1 · [Data Science] Montar o conjunto versionado de frases e o embrulho fixo e medir a linha de base</summary>

**Objetivo:** Existe um arquivo com as frases, o rótulo esperado e o embrulho fixo, e a linha de base medida no lint atual.

**Passos previstos:**
1. Definir o embrulho fixo (minuto, momento e trecho entre aspas) que transforma cada frase num Insight válido e gravá-lo no arquivo.
2. Incluir as 20 frases da sondagem como rejeitadas.
3. Incluir conjugações e sinônimos de RN03 e referências de RN04.
4. Incluir frases de uso comum de RN05 marcadas para decisão da governança.
5. Incluir como aceitas os textos do modelo de frase dos três tipos de evento e frases com citação do púlpito que contém vocabulário proibido.
6. Gravar o arquivo em CSV ou JSON.
7. Rodar o lint atual sobre o conjunto com o embrulho e registrar quantas rejeitadas passam sem erro de vocabulário.

**Definição de pronto:** Arquivo versionado no PR com o embrulho e linha de base registrada (19 de 20 frases da sondagem sem erro de vocabulário no lint atual).

**Dependências:** nenhuma

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F1.7.T2 · [Governança e Privacidade] Revisar e aprovar o conjunto de frases antes da implementação</summary>

**Objetivo:** O conjunto está aprovado pela governança, com o resultado de cada frase de uso comum decidido, data e nome do revisor.

**Passos previstos:**
1. Conferir se cada frase rejeitada descreve estado interno ou aponta pessoa ou setor.
2. Conferir se as aceitas descrevem só reação observada.
3. Decidir o resultado esperado de cada frase de uso comum de RN05.
4. Registrar ajustes, data e nome do revisor no PR.

**Definição de pronto:** Aprovação registrada no PR, com todas as frases rotuladas e data anterior ao commit que altera reacao/lint.py.

**Dependências:** F1.7.T1

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F1.7.T3 · [Backend] Ampliar o vocabulário do lint e expor a verificação de textos fixos por linha de comando</summary>

**Objetivo:** reacao/lint.py rejeita as frases rejeitadas do conjunto, aprova as aceitas e verifica textos fixos de interface por linha de comando, sem afrouxar a verificação de insights.

**Passos previstos:**
1. Corrigir a regex de 'feliz' (lint.py:9).
2. Acrescentar conjugações, sinônimos e referências a pessoa ou setor, sem proibir 'atenção aparente' e seguindo o resultado das frases de uso comum.
3. Separar a verificação de vocabulário da verificação de campos do Insight, mantendo check(Insight) com as duas.
4. Expor a verificação só de vocabulário como função pública que devolve os termos apontados, usada pela linha de comando e pelo teste de F5.6.T5.
5. Criar a entrada de linha de comando para textos fixos de interface, que sai com código diferente de 0 quando há termo proibido.
6. Atualizar a regra 4 do CLAUDE.md com a leitura aprovada no Definition of Ready, sem alterar o exemplo PBI-104 da linha 31 (RN15 da Feature).
7. Escrever os testes da função pública, da linha de comando e do check(Insight) sem minuto.

**Definição de pronto:** Rodar o lint sobre o arquivo do conjunto com o embrulho dá 0 divergência; os testes escritos na task e tests/test_lint.py passam; ruff check sem erro.

**Dependências:** F1.7.T2

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F1.7.T4 · [QA] Rodar o conjunto como teste no CI e verificar os critérios de aceite</summary>

**Objetivo:** O CI executa o conjunto de frases e a verificação por linha de comando, e cada critério de aceite fica conferido.

**Passos previstos:**
1. Criar teste parametrizado que lê o arquivo do conjunto, aplica o embrulho e compara com o resultado do lint.
2. Conferir que um rótulo trocado no conjunto faz o CI falhar.
3. Conferir a função pública e a linha de comando com texto aceito e rejeitado e o check(Insight) com insight sem minuto.
4. Registrar a medida depois da mudança: 0 de 20 frases da sondagem aprovadas.

**Definição de pronto:** CI verde no PR com o teste novo; registro da linha de base e do resultado final anexado ao PR.

**Dependências:** F1.7.T3

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- reacao/lint.py:1-49
- reacao/insights.py:8,21-24
- tests/test_lint.py
- CLAUDE.md:17-19 (regra 4) e regra 3
- README.pt-BR.md:19-21
- docs/poc-gate.md:12
- Sondagem de 20 frases com reacao.lint.check em 2026-09-23 (levantamento, revisão da árvore e reprodução nesta etapa)
- mapa_produto do levantamento, fatos 19 e 20
- P3 revisada (painel web na Vercel)
- feature_det_F5.json da sessão: F5.6.T1 (arquivo de textos fixos do painel) e F5.6.T5 (teste do lint no CI)
- feature_det_F6.json da sessão: F6.4.T3 (checagem frase a frase com PROIBIDO e PROIBIDO_INDIVIDUAL)
- CLAUDE.md:31 (exemplo PBI-104)

#### Verificação INVEST: pontos que falharam
- Independente: a implementação espera a revisão da governança sobre o conjunto de frases, e o revisor ainda não tem nome.

#### Premissas
- Estimativas (story points e horas) são sugestão, a validar no refinamento.
- Definition of Ready: Fabio Pinheiro aprova a leitura da regra 4 para textos fixos de interface (só vocabulário, porque não são insights e não têm minuto, momento nem trecho). Aprovada a leitura, F1.7.T3 atualiza a regra 4 do CLAUDE.md no mesmo PR. Sem a aprovação, RN09 e o critério 10 saem do PBI antes da sprint.
- O texto exato das 20 frases do levantamento e o embrulho usado na sondagem não estavam versionados. O conjunto usa a reconstrução feita a partir da lista do levantamento, que reproduziu 19 de 20 aprovadas, e F1.7.T1 versiona o embrulho.
- A verificação dos textos fixos do painel roda no pytest do CI Python (F5.6.T5), sobre o arquivo de textos fixos criado no diretório do painel (F5.6.T1), fora da Vercel. F5.6.T5 depende de F1.7. O passo 1 de F5.6.T5 acrescenta outra verificação de texto livre em reacao/lint.py; a pendência pede que use a função de F1.7.T3. O texto de insight editado em F7.3 usa o check(Insight) completo.
- O revisor de governança é o encarregado de dados, ainda sem nome no épico, ou quem Fabio Pinheiro indicar.
- F1.7.T3 altera só a regra 4 do CLAUDE.md. O exemplo PBI-104 de CLAUDE.md:31 fica com a task de F2.1 prevista na revisão dos IDs antigos, com aprovação de Fabio Pinheiro.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Responsável de governança para F1.7.T2
- Registrar no Definition of Ready a aprovação da leitura da regra 4 para textos fixos
- Pedir a F5.6.T5 que use a função de vocabulário de F1.7.T3 em vez de acrescentar outra em reacao/lint.py, e a F6.4.T3 que avalie o mesmo reuso
- Validar os 5 story points sugeridos
