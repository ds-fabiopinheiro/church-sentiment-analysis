[Voltar ao épico](README.md)

# Preview — Feature F5 (novo) · Gerar no HF Jobs, exibir no painel web na Vercel e avaliar o relatório de cultos públicos inteiros (critérios 3, 4 e 5)

### Campos
| Campo | Conteúdo |
|---|---|
| Título | Gerar no HF Jobs, exibir no painel web na Vercel e avaliar o relatório de cultos públicos inteiros (critérios 3, 4 e 5) |
| Tipo | Feature |
| Pai | Epic |
| Tags | fase-0; gate; criterio-3; criterio-4; criterio-5; hf-jobs; painel-vercel; supabase |
| Estimativa | 49 pts / 227 h (soma dos PBIs, sugestão) |

### Descrição

**Problema:** O critério 3 do gate precisa de culto inteiro (docs/poc-gate.md:11), e o README do corpus da PIB diz o mesmo para os critérios 3 e 4 (samples/corpus/pib/README.md:16-18, não versionado). O corpus da PIB tem só clipes de 1,3 a 23,1 s (samples/corpus/pib/README.md:7, não versionado), e docs/corpus.csv tem só o cabeçalho (docs/corpus.csv:1). Nenhum código compara os momentos detectados com os rotulados, e o validador recusa uma pasta que só tem _momentos.csv (tools/validar_labels.py:197-201,215-220). A chamada ao LLM de momentos fica fora do try (reacao/moments.py:63-69). Por isso, um erro da API interrompe a execução antes de gravar momentos, eventos e insights (processar_culto.py:92-100). O id do modelo está fixo em dois lugares (reacao/moments.py:63; reacao/insights.py:48), e o run_log não registra se o LLM foi usado (processar_culto.py:104-106). O texto do insight mostra identificadores técnicos, como pct_voltados e oracao, e os insights saem em ordem de magnitude (reacao/insights.py:22-24,30). O pastor não tem onde ler o relatório. Não há front end no repositório (git ls-files, 2026-09-23), e o CI instala e testa só o código Python (.github/workflows/ci.yml:8-17). O time 'Fabio Pinheiro's projects' da Vercel tem só o projeto ai-guitar-coach-pilot, que não tem relação com este sistema (Vercel list_projects, 2026-09-23). Nenhum código grava em insight_feedback (supabase/migrations/0001_init.sql:17). Não existe medição em T4 de um culto com transcrição, nem as medidas de dimensionamento pedidas em docs/onprem.md:9-14 ('hf jobs ps -a' sem resultados em 2026-09-23). O HSEmotion cria a sessão ONNX só com CPUExecutionProvider (hsemotion_onnx/facial_emotions.py:40, pacote instalado), o que pode reprovar o critério 5.

**Solução proposta:** Selecionar três cultos públicos pt-BR inteiros, registrar a licença de cada um, copiar os vídeos para o dataset privado e marcar os momentos à mão. A cópia usa um token de escrita de uso único, registrado no inventário de credenciais de F2.6 e revogado ao fim, e o script de cópia fica pronto para F3.6 reutilizar. Fazer a geração de momentos e insights usar rótulos em português, entregar os insights em ordem de tempo e continuar quando a API de linguagem falhar. Processar os cultos no HF Jobs pela imagem com digest, medindo tempo, custo e uso de GPU na t4-small. Se o critério 5 reprovar, levar expressão e pose para a GPU. Comparar as fronteiras de momento com a marcação manual. Mostrar o relatório num painel web, num projeto novo no time 'Fabio Pinheiro's projects' da Vercel. O código do painel fica num diretório próprio do repositório, com lockfile e um passo de CI com lint, testes e build, e o projeto da Vercel publica a partir desse diretório. O painel lê do Supabase agregados, eventos e insights, a lista de execuções liberadas (listada em D7 de F2.4.T4) e, se o usuário confirmar a pendência de D7, momentos, usando a chave pública, Supabase Auth e RLS. Fabio e Filipe registram nele as notas do critério 4. Vídeo, transcrição completa e cálculo dos critérios ficam no Hugging Face e no Supabase. Todos os jobs, inclusive a cópia dos vídeos e os cálculos dos critérios, rodam pela imagem com digest. A Vercel não recebe vídeo, quadro, recorte de rosto nem observação por rosto.

**Usuários impactados:** Fabio Pinheiro, responsável pelo gate: lê o relatório, dá nota aos insights e assina o gate, Pastor Filipe: lê o relatório, dá nota aos insights e assina o gate, Time de Data Science, Machine Learning, Visão Computacional, MLOps, DevOps, Backend, Front end, QA e Governança e Privacidade, que produz as medidas dos critérios 3, 4 e 5

**Valor de negócio:** Preenche os critérios 3, 4 e 5 do gate, que hoje estão sem valor (docs/poc-gate.md:11-13). Sem eles, a decisão de F6.1 não pode ser assinada. Antes do gate, entrega a Fabio e ao pastor Filipe um relatório de um culto público num painel com acesso restrito, que é o insumo do critério 4. Também preenche a tabela de dimensionamento de docs/onprem.md:9-14, pedida pelo PBI-103 e pela TSK-207.

**Regras de negócio:**
- RN01 – O sistema usa só vídeo e imagem da plateia. A trilha de áudio do arquivo serve só para transcrever o púlpito (CLAUDE.md, regra 5; reacao/transcribe.py:1).
- RN02 – Uma janela com menos de 10 rostos mensuráveis (altura >= 64 px) sai marcada como insuficiente e sem percentuais, também no painel (CLAUDE.md, regra 3; reacao/types.py:5-7).
- RN03 – Todo texto mostrado a Fabio e Filipe passa pelo lint, inclusive os textos fixos do painel (CLAUDE.md, regra 4).
- RN04 – Antes da decisão do gate, o painel mostra só os cultos públicos de docs/corpus.csv, e só para Fabio e o pastor Filipe (premissa P10).
- RN05 – O painel na Vercel lê do Supabase agregados, eventos e insights (P3 revisada) e a tabela de execuções liberadas, conforme a lista de tabelas de D7 (F2.4.T4). A leitura dos momentos é pendência de D7 com o usuário. O painel usa a chave pública, Supabase Auth e RLS. A chave secreta ou de serviço do Supabase fica só nos jobs do HF. A Vercel não recebe vídeo, quadro, recorte de rosto nem observação por rosto (P3 revisada).
- RN06 – Todo processamento roda no HF Jobs: cópia dos vídeos públicos, pipeline, medida da transcrição, comparação de momentos e cálculo dos critérios. Todos os jobs desta Feature rodam com 'hf jobs run <imagem>@<digest>' e comando explícito, pela imagem publicada no fluxo de F2.2, que passa a incluir tools/ (F5.1.T4). 'hf jobs uv run' não é usado, porque F2.4 o reserva ao desenvolvimento.
- RN07 – Cada job pago precisa de aprovação prévia do dono da conta (P7).
- RN08 – Até a decisão de F6.2, o campo avaliador das notas guarda um código de papel, e não o nome (P12).
- RN09 – As notas do critério 4 usam o relatório do motor escolhido em F4.6 (P10).
- RN10 – A transcrição de culto público só vai à API da Anthropic com a confirmação de Fabio. Sem ela, momentos e insights usam a heurística e o modelo de frase (P26; docs/onprem.md:50-52).
- RN11 – Cada valor dos critérios 3, 4 e 5 leva o run_id e o arquivo de resultado de origem no repositório de resultados, com linhagem (F2.8).
- RN12 – Gravações administrativas no Supabase (papel em app_metadata, liberação de execução ao painel e marcação da execução em avaliação) são feitas por migração versionada ou pelo SQL Editor, com a conta dona do projeto Supabase e sem a chave de serviço, ou dentro de um job do HF. Nenhuma pessoa usa a chave de serviço fora de um job (P3 revisada).
- RN13 – A migração que libera uma execução ao painel cita o culto por extenso, e esse culto precisa estar na coluna video de docs/corpus.csv. Um teste do CI confere isso (F5.6).

**Fora de escopo:**
- Perfis pastor, mídia e DPO com políticas de RLS, e revisão antes de liberar ao pastor (F7.2 e F7.3)
- Sinalização de qualidade por culto (F7.6)
- Vídeo ou resultado da PIB no painel antes da decisão do gate e do RIPD (P10)
- Ferramenta de rotulagem e qualquer tela que mostre vídeo ou quadro. Elas ficam em Space privado no HF (F3.3)
- Envio do vídeo do piloto, que vai direto a um destino privado no HF, sem passar pela Vercel (F7.1)
- Seleção e transferência dos clipes públicos dos critérios 1 e 2 (F3.6), que reutiliza o script de cópia e o procedimento de token de F5.1
- Modelo de linguagem local (Ollama) ou hospedado no HF (P26)
- Separação de falantes na transcrição
- Eventos de aplauso, pé ou cabeça baixa. Os rótulos aceitam esses eventos, mas o gate não os mede (labels/README.md:11; docs/poc-gate.md:6-14)
- Relatório em PDF ou por e-mail
- Execução no servidor local e paridade entre HF e servidor local (P3)

**Dependências técnicas:**
- PBIs de outras Features: F1.1, F1.2, F1.3, F1.5, F1.7, F2.2, F2.3, F2.4, F2.5, F2.6, F2.7, F2.8, F3.5 e F4.6, e F1.6 se F5.3 for acionado (P29). A árvore também lista F2.3 como dependência de F5.4
- F2.4 revisto pela P3 revisada: o ADR 0002 registra, como critérios de F2.4, o projeto do painel na Vercel, o framework, o método de login do Supabase Auth, a proteção de deployment e a validade do token de acesso. O plano e os termos de uso da Vercel ficam como pendência em D8 de F2.4.T4, resolvida com Fabio em F5.6.T9 antes da criação do projeto. F5.6 fica fora da sprint até esse ADR ser mesclado
- F2.4.T4 (decisão D7, fronteira de dados e credenciais): registra, antes de F5.6, onde fica o vínculo entre conta e papel e se a regra 6 do CLAUDE.md vale para as contas da equipe. F5.6.T3 depende dessa decisão, e F6.2 só a confirma ou ajusta, com migração se mudar
- F2.6.T1 (procedimento de token fine-grained) e F2.6.T6 (inventário de credenciais): F5.1.T3 cria por esse procedimento o token de escrita dos jobs de cópia e o registra no inventário, e F5.6.T2 registra lá as variáveis do projeto do painel na Vercel (URL e chave pública do Supabase)
- F2.4.T4 (D7): lista das tabelas lidas pelo painel (moment como pendência com o usuário) e decisão de Fabio sobre a exceção da P26, da qual dependem F5.4.T4, F5.5.T3 e F5.6.T7
- F2.6.T4: job de CI com Supabase local e as migrações, no qual rodam os testes pgTAP de F5.6.T4 e F5.7.T1 (pendência em F2)
- F2.8: linhagem de cada execução e repositório privado de resultados, onde ficam os valores dos critérios 3, 4 e 5 e as medidas de F5.4
- F2.2 aceita pré-release por tag num commit de branch sem mover :latest, para a remedição de F5.3. Hoje o workflow publica em qualquer tag v* e também marca :latest (.github/workflows/docker.yml:2-5,23-25)
- Projeto Supabase de desenvolvimento com RLS habilitada (F2.6). Ele não aparece na conta Supabase conectada, embora supabase/migrations/0001_init.sql:2 diga que foi criado (Supabase list_projects, 2026-09-23)
- Time Vercel 'Fabio Pinheiro's projects' (team_TFJpulVK8Dcufy5SIecwChUh). Hoje ele só tem o projeto ai-guitar-coach-pilot (Vercel list_teams e list_projects, 2026-09-23). O plano e os termos de uso para este projeto são confirmados em F5.6.T9
- Node.js e um gerenciador de pacotes para o painel. A Vercel escolhe o gerenciador pelo lockfile (https://vercel.com/docs/package-managers) e usa a versão do Node do campo engines.node do package.json, que prevalece sobre a configuração do projeto (https://vercel.com/docs/functions/runtimes/node-js/node-js-versions)
- Supabase Auth do projeto de desenvolvimento, com as contas de Fabio, de Filipe e duas contas de teste da QA
- Dataset privado ds-fabiopinheiro/reacao-poc-corpus, lido por tag ou revisão (F3.5)
- Saldo de créditos no HF Jobs, visível só na página de billing (https://huggingface.co/docs/hub/jobs-pricing)
- Chave da API da Anthropic, opcional, com a confirmação de Fabio (P26)
- Três vídeos públicos pt-BR de culto inteiro, com download permitido e planos de plateia (CONTRIBUTING.md:11)

**Riscos:**
- R1 – Pode não haver três cultos públicos pt-BR com download permitido e planos de plateia. docs/corpus.csv está vazio (docs/corpus.csv:1). Nesse caso, os critérios 3 e 4 ficam sem medida.
- R2 – A transcrição pode passar do corte de 60000 caracteres (reacao/moments.py:61). O fim do culto fica então sem momento, moment_at devolve 'desconhecido' (reacao/moments.py:72-76) e o lint rejeita os insights desse trecho (reacao/lint.py:34-35). F5.4 mede esse risco.
- R3 – O tamanho de /dev/shm e o timeout máximo de um job não estão documentados (P19; https://huggingface.co/docs/hub/jobs-configuration#timeout). Um culto inteiro pode não caber no job.
- R4 – A expressão do HSEmotion roda em CPU mesmo na T4 (hsemotion_onnx/facial_emotions.py:40, instalado) e pode reprovar o critério 5. F5.3, condicional, cobre esse caso.
- R5 – Times Hobby da Vercel só podem ter uso pessoal não comercial. A Vercel define uso comercial pelo ganho financeiro de qualquer pessoa na produção do projeto, inclusive quem é pago para escrever o código (https://vercel.com/docs/limits/fair-use-guidelines, seção Commercial usage). O plano deste projeto ainda precisa ser confirmado, e F5.6.T9 o confirma com Fabio antes da criação do projeto.
- R6 – Se a Vercel Authentication ficar ligada no domínio de produção, só entram membros do time ou do projeto, usuários Vercel com acesso concedido e quem tiver link compartilhável. No Hobby, cada conta pode ter só um usuário externo (https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/vercel-authentication).
- R7 – O Supabase anuncia a descontinuação das chaves anon e service_role até o fim de 2026, e as chaves legadas continuam válidas até serem desativadas no painel do Supabase (https://supabase.com/docs/guides/getting-started/api-keys). O Store lê SUPABASE_SERVICE_KEY (reacao/store.py:12). O painel usa a chave sb_publishable_.
- R8 – Depois de uma mudança em app_metadata, o JWT só reflete a mudança quando é renovado (https://supabase.com/docs/guides/database/postgres/row-level-security). A retirada de um papel não vale na hora.
- R9 – No Postgres, uma view ignora a RLS a menos que tenha security_invoker = true (https://supabase.com/docs/guides/database/postgres/row-level-security). Uma view no painel sem essa opção expõe dados.
- R10 – O saldo de créditos do HF não está confirmado, e o valor 'US$ 20 cobrem o PoC' não tem cálculo registrado (docs/hf-jobs.md:3; P7).
- R11 – Se a exceção P26 não for aceita, o critério 3 fica medido só com a heurística.
- R12 – Um atraso na escolha do motor em F4.6 atrasa F5.4, F5.5 e F5.7.
- R13 – Apagar uma conta ou fazer signOut global impede novos tokens, mas o token de acesso já emitido continua válido até o exp (https://supabase.com/docs/guides/auth/managing-user-data; https://supabase.com/docs/guides/auth/signout). A retirada de acesso de uma conta não vale na hora.
- R14 – Com Root Directory definido, o app na Vercel não acessa arquivos fora desse diretório (https://vercel.com/docs/builds/configure-a-build#root-directory). Um arquivo compartilhado com o pipeline, como os rótulos de F5.2.T4, precisa de uma cópia no diretório do painel, e a cópia pode divergir do original. F5.8.T1 cria um teste que compara os dois.
- R15 – O repositório é público (GitHub API, visibility=public, 2026-09-23). Um PR vindo de fork só ganha deployment com autorização de um membro do time enquanto a Git Fork Protection estiver ligada, e ela pode ser desligada nas configurações do projeto (https://vercel.com/docs/git#deploying-forks-of-public-git-repositories; https://vercel.com/docs/git/vercel-for-github). F5.6.T2 a mantém ligada.

**Estratégia de fatiamento:** Fatiamento por passo do fluxo de um culto público, a estratégia 1 do TaskFlow. Os passos são: obter e rotular o vídeo (F5.1); gerar momentos e insights com rótulos em português, em ordem de tempo e com volta à heurística (F5.2); entrar no painel web na Vercel e ver a lista de execuções liberadas, com o primeiro culto processado (F5.6); ler o relatório (F5.8); medir tempo, custo e uso de GPU (F5.4), com otimização de GPU condicional (F5.3); comparar os momentos (F5.5); e registrar as notas e calcular o critério 4 (F5.7). F5.6 e F5.8 não esperam a escolha do motor, para que Filipe leia um relatório real antes do gate. A divisão do antigo F5.6 em F5.6 e F5.8 leva a Feature a 8 PBIs, um acima do limite de 2 a 7 filhos por nível (4us-backlog-ai/references/taskflow.md:40). O refinamento decide entre manter essa exceção ou mover F5.3, que é condicional e alimenta F6.1, para F6, que tem 6 PBIs. F5.1 ficou com 8 tasks e F5.6 com 9, acima do mesmo limite: em F5.1, a revogação do token só pode acontecer depois das cópias; em F5.6, a montagem do diretório do painel precisa vir antes do projeto na Vercel e do CI, e a confirmação do plano e dos termos da Vercel (F5.6.T9) precisa vir antes da criação do projeto. O refinamento trata essas exceções junto com o número de PBIs. A divisão por disciplina fica nas Tasks.

### Critérios de aceite
- docs/corpus.csv tem três cultos públicos pt-BR inteiros, cada um com URL, licença e permissão de download. Cada vídeo está no dataset privado sob tag, com o arquivo de momentos marcado à mão numa pasta separada dos rótulos dos clipes, e o token de escrita usado na cópia está revogado (F5.1).
- Com a API de linguagem indisponível, com chave inválida ou com resposta sem momento da lista, a sequência de momentos, eventos e insights termina sem exceção, os momentos vêm da heurística e o registro da execução mostra o caminho usado e o motivo (F5.2).
- Nenhum insight de um relatório de teste contém pct_voltados, pct_sorrindo ou oracao, e a lista sai ordenada pelo minuto (F5.2).
- Para cada um dos três cultos processados na t4-small pela imagem da release de F5.4, o repositório de resultados tem o tempo e o custo por hora de vídeo, calculados pela fórmula pré-registrada em F1.3 (F5.4).
- A tabela da seção 1 de docs/onprem.md tem os quatro valores preenchidos, cada um com a execução de origem, e a primeira linha traz o dispositivo de cada etapa (F5.4).
- O critério 3 tem valor em cada um dos três vídeos, calculado pela regra de pareamento de F1.3 (F5.5).
- Fabio e o pastor Filipe entram no painel web na Vercel com as próprias contas, veem a lista de execuções liberadas (F5.6) e leem o relatório de um culto público (F5.8).
- O painel tem diretório próprio no repositório, com lockfile, o CI roda lint, testes e build dele em cada PR, e o projeto na Vercel publica a partir desse diretório (F5.6).
- Uma conta sem o papel de avaliador e um visitante anônimo não recebem nenhum dado, nem pelo painel nem por consulta direta ao banco, e nenhuma sessão de cliente grava nas tabelas lidas pelo painel (F5.6).
- O projeto do painel na Vercel não tem a chave secreta nem a chave de serviço do Supabase (F5.6), e, no domínio de produção, o painel não recebe resposta com Content-Type video/* ou image/* além dos próprios arquivos estáticos (F5.8).
- O critério 4 tem valor calculado a partir das notas gravadas de Fabio e de Filipe e do registro da execução do relatório do motor escolhido (F5.7).
- Se F5.3 for acionado, a nova medição tem relatório de paridade com diferença de até 1 p.p. e o mesmo n (F5.3).

### Alterações em relação à árvore
- Título da Feature: 'no HF' foi trocado por 'no HF Jobs', para o processamento, e 'no painel web na Vercel', para a exibição (P3 revisada).
- Problema e solução: o Space privado deu lugar a um painel web num projeto novo na Vercel, no time 'Fabio Pinheiro's projects'. Hoje esse time só tem o projeto ai-guitar-coach-pilot (Vercel list_projects, 2026-09-23).
- Problema: a exigência de culto inteiro passou a citar docs/poc-gate.md:11 para o critério 3 e samples/corpus/pib/README.md:16-18 (não versionado) para os critérios 3 e 4. A linha 12 de docs/poc-gate.md não fala de culto inteiro.
- F5.6 da árvore foi dividido em F5.6 (acesso ao painel, políticas de RLS, lista de execuções liberadas e primeiro culto processado) e F5.8 (tela do relatório). O PBI tinha 13 story points, 9 tasks, 41 h e 13 critérios sobre assuntos diferentes (taskflow.md, seções 1 e 2). A Feature passou a ter 8 PBIs, um acima do limite de 2 a 7 (taskflow.md:40), e a escolha entre manter a exceção ou mover F5.3 para F6 fica para o refinamento.
- F5.6: o título, as regras, os critérios e as tasks trocam o Space privado pelo painel web na Vercel. O acesso deixa de usar OAuth do HF com a chave de serviço guardada como secret do Space e passa a usar Supabase Auth com cadastro fechado, chave pública e RLS com o papel de avaliador do gate. As fontes de Space foram trocadas pelas da Vercel e do Supabase.
- F5.6: a política de leitura do avaliador do gate, que na árvore só surgiria em F7.2, entra neste PBI. A P3 revisada proíbe a chave de serviço fora dos jobs, e, com RLS ligada e sem política, a chave pública não lê nada (https://supabase.com/docs/guides/database/postgres/row-level-security).
- F5.6: novas dependências de F2.5, porque sem run_id o relatório do hsemotion e o do motor escolhido se misturam (reacao/store.py:24-26; supabase/migrations/0001_init.sql:6-16), e de F2.3, porque a P3 revisada põe os pesos em repositórios de modelo privados.
- F5.6: nova tabela de execuções liberadas (culto, run_id, motor e origem), com RLS, grants revogados de anon e authenticated e só select para o avaliador. Ela dá o motor ao cabeçalho sem ler run_log (o provider só existe em run_log; supabase/migrations/0001_init.sql:18) e define qual execução o relatório mostra. As tabelas lidas pelo painel também perderam os grants de escrita dos clientes.
- F5.6: nenhuma task usa mais a chave dos jobs fora de um job. A liberação de execução é uma migração versionada aplicada pelo dono do projeto Supabase, o papel é gravado pelo SQL Editor em auth.users.raw_app_meta_data, sem a API admin, e a QA verifica só com sessões de usuário e com a chave pública. A busca de chaves no build usa o prefixo sb_secret_ e a claim role dos JWT, sem o valor das chaves.
- F5.6: entraram duas contas de teste da QA (uma avaliadora e uma sem papel) para os critérios de acesso negado. Fabio e Filipe verificam os critérios de entrada com as próprias contas, acompanhados pela QA. Um teste do CI compara as migrações de liberação com docs/corpus.csv.
- F5.6: a premissa de revogação foi corrigida (o token já emitido vale até o exp; https://supabase.com/docs/guides/auth/managing-user-data; https://supabase.com/docs/guides/auth/signout), e a das chaves legadas e o R7 passaram a dizer 'descontinuação anunciada até o fim de 2026' (https://supabase.com/docs/guides/getting-started/api-keys). A leitura de que a regra 6 cobre só o schema public virou dedução, hoje a cargo da decisão D7 de F2.4.T4.
- F5.6: o passo de confirmar o plano da Vercel saiu da task que cria o projeto na Vercel (hoje F5.6.T2) e virou critério do ADR de F2.4 revisto, com Fabio como responsável. A fonte 'mapa de infraestrutura' foi trocada por 'GitHub API, visibility=public, 2026-09-23' e 'git ls-files'.
- F5.6, numeração em relação ao F5.6 anterior à divisão (tasks 'antigas'): T1 é nova (diretório, pilha e lockfile do painel); T2 é a antiga T1, com integração Git, CI do front end e registro no inventário de credenciais; T3 é a antiga T2; T4 é a antiga T3, com a tabela de execuções liberadas e os grants; T5 é a antiga T6 (lint dos textos fixos); T6 é a antiga T4 (login e lista); T7 é a antiga T7 (processamento e liberação); T8 é a QA do acesso. A antiga T5 virou F5.8.T1, a antiga T8 virou F5.8.T2, e F5.8.T3 é QA nova. Em relação à versão revisada antes desta rodada, as tasks T1 a T7 de F5.6 são hoje T2 a T8.
- F5.8: o critério de rede vale no domínio de produção e usa o Content-Type das respostas, e F5.6.T2 desliga a Vercel Toolbar em preview (https://vercel.com/docs/vercel-toolbar/managing-toolbar). A tela depende agora da task que processa e libera o culto.
- F5.7: no título, 'no Space' virou 'no painel web na Vercel'. A nota é gravada por uma política de RLS que confere o código de papel lido do JWT, e o cálculo do critério 4 roda em job no HF pela imagem com digest.
- F5.7: a marcação da execução em avaliação virou coluna da tabela de execuções liberadas, e insight_feedback recebeu grants explícitos, sem delete. F5.7.T1 depende do registro das regras em F1.3, o critério da nota faltante cita a regra de F1.3, o cálculo usa só os códigos de Fabio e de Filipe, e as contas e notas de teste são apagadas ao fim. Nova dependência de F5.8.
- F5.1: novas dependências de F2.2, porque a cópia passa por /dev/shm (P19), e de F1.1, porque a definição de pronto usa a linha '[guard] ok'. A disciplina DevOps foi acrescentada para o token de escrita restrito ao dataset.
- F5.1: foi acrescentada a coluna de licença em docs/corpus.csv, porque CONTRIBUTING.md:11 pede a licença e o cabeçalho de docs/corpus.csv:1 não tem esse campo. Também entrou a conferência do início de cada momento contra a duração do vídeo, porque validar_momentos recebe o último tempo e não o usa (tools/validar_labels.py:136-155).
- F5.1: a cópia roda dentro de reacao.guard.no_persistence, pela imagem com digest, que passa a incluir tools/. O id do job, a duração e a revogação do token ficam na seção de vídeos públicos do dataset card, e duracao_min entra em docs/corpus.csv por PR. Os momentos dos cultos ficam numa pasta separada de labels/. As antigas T1 e T5 foram unidas em T1. As antigas T6, T7 e T8 mantêm o número, e T5 é a revogação do token, nova (entrada seguinte). Em relação à versão revisada antes desta rodada, T5, T6 e T7 de F5.1 são hoje T6, T7 e T8.
- F5.1 (revisão sobre a sobreposição com F3.6): F5.1.T3 passou a depender de F2.6.T1 e F2.6.T6, registra o token no inventário de credenciais como exceção de uso único e descreve lá o procedimento para F3.6.T3 e F3.6.T5. A revogação saiu de F5.1.T3 e virou F5.1.T5, porque só pode acontecer depois de F5.1.T4. O script de F5.1.T4 recebe a lista de vídeos e o destino no dataset como parâmetros, o comando é validado pelo lançador de F1.1 e os parâmetros ficam em docs/hf-jobs.md para F3.6.T4. F5.1 ganhou a dependência de F2.6, as regras RN08 (token) e RN09 (exclusão dos vídeos marcados como usados em F3.6, pedida em F3.6), o passo de exclusão em F5.1.T1, o token revogado no critério 3 e a exclusão no critério 1. O PBI passou a ter 8 tasks, uma acima do limite de 7 (taskflow.md:40).
- F5.2: título com termos verificáveis ('rótulos em português' e 'ordem de tempo'). Nova dependência de F1.5, porque os campos novos do run_log precisam de migração e F1.5 cria o teste de contrato.
- F5.2: a sequência de processar_culto.py:92-100 é extraída para uma função testável (F5.2.T3), e o critério 1 passou a usar segmentos e agregados sintéticos sobre essa função. Entraram a volta à heurística quando o JSON não traz momento da lista (reacao/moments.py:67) e o critério do conteúdo do log. F5.2.T1 tem os próprios testes, o que desfaz a dependência circular com F5.2.T5. A confirmação de Fabio sobre as duas regras propostas virou item de Definition of Ready.
- F5.2: a seleção dos 8 insights de maior magnitude continua (reacao/insights.py:30). Só a ordem da lista entregue passa a ser a de tempo.
- F5.2 e F5.8 (efeito do Root Directory): o arquivo de rótulos de F5.2.T4 fica no pacote reacao, e o painel usa uma cópia no próprio diretório, conferida por um teste criado em F5.8.T1, porque o app na Vercel não acessa arquivos fora do Root Directory (https://vercel.com/docs/builds/configure-a-build#root-directory).
- F5.3: novas dependências de F5.4, quando o acionamento vier dessa medição, e de F1.6, porque os testes em CPU precisam dos motores reais no CI (.github/workflows/ci.yml:9). O dispositivo da pose passa a ser registrado, os providers vão para o log e para a linhagem de F2.5, sem coluna nova no run_log, e a imagem medida é publicada por pré-release antes do merge.
- F5.4: a disciplina QA foi acrescentada, porque todo PBI tem task de QA. O valor do critério 5 vai para o repositório de resultados, e a escrita em docs/poc-gate.md fica com F6.1.
- F5.4: saiu a premissa de que detecção e expressão rodam na GPU; a primeira linha de docs/onprem.md passa a ser o tempo de parede com o dispositivo de cada etapa. Entrou a task de release antes dos jobs. A coleta de 'hf jobs stats' passou para a task de lançamento. A medida da transcrição passou para dentro do job e conta eventos, e não insights, com momento 'desconhecido'. Numeração: T1 mantém o número; T2 é a antiga T5 redefinida; T3 é nova; T4 junta as antigas T2 e T3; T5, T6 e T7 são as antigas T4, T6 e T7.
- F5.5: F5.5.T1 passou de Backend para Data Science, e Backend saiu das disciplinas do PBI. Os momentos segmentados de novo vão como arquivo ao repositório de resultados, sem gravar na tabela moment. A comparação usa a transcrição e os agregados do run_id de F5.4, sem processar o vídeo de novo, e roda pela imagem com digest.
- F5.6 (revisão sobre o front end na Vercel): nova F5.6.T1 (Front end) cria o diretório do painel com o framework do ADR de F2.4, o lockfile, os comandos de lint, teste e build, o arquivo de textos fixos e as entradas do .gitignore, que hoje não tem entrada para dependências de Node. F5.6.T2 passou a ligar o projeto ao repositório com Root Directory e main como branch de produção, manter a Git Fork Protection ligada, criar o job de CI do painel e registrar as variáveis no inventário de F2.6.T6. F5.6.T5 e F5.6.T6 dependem de F5.6.T1. Os critérios 8 e 10 de F5.6 foram ampliados com a configuração do projeto e o CI do painel, e a QA confere os dois. O PBI passou a ter 8 tasks.
- F5.6 (revisão sobre o vínculo entre conta e papel): F5.6.T3 passou a depender de F2.4.T4 (D7), e a dependência de F2.4 no PBI cita essa decisão. O item de Definition of Ready 'Fabio confirma a leitura da regra 6' foi trocado pela decisão D7 registrada no ADR 0002. F6.2 só confirma ou ajusta. F5.8.T2 e o critério 9 de F5.8 conferem o painel contra D7. As correções de texto em F6.2, F7.2 e F7.8 ficaram em pendências, porque estão fora de F5.
- Feature: RN05 separa o que a P3 revisada permite (agregados, eventos e insights) do que é premissa (momentos e execuções liberadas); RN06 põe todos os jobs na imagem com digest; RN12 e RN13 são novas. Os critérios 2, 3, 5 e 7 a 10 da Feature foram reescritos, R7 foi corrigido e R13 é novo.
- Feature (revisões de F3.6, D7 e front end): a solução cita o token de uso único, o script reutilizável e o diretório do painel com CI; o critério 1 inclui o token revogado; entrou o critério do diretório e do CI do painel; entraram as dependências técnicas F2.4.T4 (D7), F2.6.T1 e F2.6.T6 e a de Node.js com lockfile; entraram R14 (Root Directory) e R15 (PR de fork em repositório público); F3.6 entrou em fora de escopo.
- Fora de escopo: 'no Space' virou 'no painel'. Foram acrescentados a ferramenta de rotulagem (F3.3) e o envio do vídeo do piloto (F7.1), que ficam no HF, e a sinalização de qualidade (F7.6).
- Reconciliação (linhagem em F2.8): as referências a 'registro de linhagem de F2.5' e 'repositório de resultados de F2.5' passaram a citar F2.8 em F5.2 (RN05), F5.3 (RN02, premissa, T1 e T2), F5.4 (RN07, premissa, T3 e T4), F5.5 (RN04 e T2), F5.6 (critério 9, premissa e T7), F5.7 (RN06 e T4) e na Feature (RN11 e premissa do repositório de resultados). F2.8 entrou nas dependências de F5.4, F5.5, F5.6 e F5.7 e das tasks F5.4.T1, F5.4.T2 (F2.8.T1), F5.4.T4, F5.6.T7 e F5.7.T4. F5.5.T2 trocou F2.5 por F2.8. F2.5 ficou onde o assunto é run_id ou falha no Supabase (F5.4.T4, passo da falha; F5.5 RN03; F5.6 contexto).
- Reconciliação (plano da Vercel): nova task F5.6.T9 (Governança e Privacidade, 2 h), que confirma com Fabio o plano e os termos de uso da Vercel e fecha a pendência D8 de F2.4.T4, com a retenção de logs do plano. Ela vem de F7.2.T2, que em F7 ficou só com a reconfirmação para os dados do piloto. F5.6.T2 passou a depender de F5.6.T9. F5.6 ganhou RN12, um critério de aceite, um passo na QA (F5.6.T8) e as fontes https://vercel.com/docs/logs/runtime e README.pt-BR.md:48. A premissa que punha o plano como critério do ADR de F2.4 foi reescrita. F5.6 passou a ter 9 tasks.
- Reconciliação (P26): F5.4.T4, F5.5.T3 e F5.6.T7 passaram a depender de F2.4.T4 (D7: decisão de Fabio sobre a exceção da P26), com um passo que lê a decisão antes de passar ou não a ANTHROPIC_API_KEY. F5.5.T2 cita D7 como fonte da decisão.
- Reconciliação (P7): 'Aprovação de Fabio (P7), com flavor, duração e custo previstos' entrou nas dependências de F5.1.T4, F5.3.T3, F5.4.T4, F5.5.T3, F5.6.T7 e F5.7.T4. F5.3.T3 não estava na lista da revisão, mas roda job na t4-small.
- Reconciliação (Supabase local no CI): F5.6.T4 e F5.7.T1 passaram a rodar os testes pgTAP no job de CI com Supabase local de F2.6.T4 e a depender dele; as definições de pronto e a QA de F5.6.T8 conferem o resultado no CI.
- Reconciliação (tabelas do painel em D7): F5.8.T2 compara as tabelas lidas pelo painel com a lista de D7 do ADR 0002 e depende de F2.4.T4. RN05 da Feature, RN01 de F5.6, RN06 e contexto de F5.8, F5.6.T4 e as premissas passaram a dizer que D7 lista a tabela de execuções liberadas e deixa moment como pendência com o usuário.
- Reconciliação (IDs antigos): F5.4.T6 troca '(PBI-103/TSK-207)' por 'F5.4' em docs/onprem.md:7, e o PR cita só F5.4. A linha 55 do mesmo arquivo ficou em pendência para F2.7.T1.

### Premissas
- P3 revisada, que prevalece sobre P3, P9, P10 e P11 no que tratam do front end: o processamento fica no HF (HF Jobs, dataset privado ds-fabiopinheiro/reacao-poc-corpus e repositórios de modelo privados). O painel do produto fica num projeto novo na Vercel, no time 'Fabio Pinheiro's projects', e lê do Supabase agregados, eventos e insights, com Supabase Auth, RLS e chave pública. A chave de serviço fica só nos jobs do HF.
- P10 aplicada ao painel: antes da decisão do gate, o painel mostra só cultos públicos de docs/corpus.csv, e só para Fabio e o pastor Filipe. O primeiro relatório (F5.6 e F5.8) pode vir do motor padrão hsemotion. As notas do critério 4 (F5.7) usam o relatório do motor escolhido em F4.6.
- P11, sobre o acesso a Space, deixa de valer para F5.6, F5.7 e F5.8, mas continua valendo para a ferramenta de rotulagem (F3.3).
- A tabela de momentos (nome, início e fim; supabase/migrations/0001_init.sql:14) e a tabela de execuções liberadas criada em F5.6 (culto, run_id, motor e origem) não têm texto da transcrição nem dado por rosto. D7 de F2.4.T4 lista a tabela de execuções liberadas entre as que o painel lê, exclui transcript_segment e run_log e deixa moment como pendência com o usuário. Se o usuário recusar os momentos, o painel mostra o momento só pelo campo momento de eventos e insights.
- No período do gate, a proposta que F5.6 implementa guarda o papel e o código de avaliador em app_metadata do Supabase Auth (coluna auth.users.raw_app_meta_data), campo que o usuário não consegue alterar (https://supabase.com/docs/guides/database/postgres/row-level-security), e os e-mails em auth.users. A árvore deixava a decisão sobre o local desse vínculo para F6.2 ('onde fica o vínculo entre usuário e papel exigido por F7.2 (regra 6)'), que só começa depois de F6.1. A decisão passa para F2.4.T4 (D7, fronteira de dados e credenciais), antes de F5.6, junto com a de se a regra 6 (CLAUDE.md:21) vale para as contas da equipe. A leitura de que a regra 6 e tests/test_schema.py, que só lê supabase/migrations/*.sql (tests/test_schema.py:9), não alcançam o schema auth é dedução, que D7 confirma ou recusa. Se D7 escolher outro local para o vínculo, F5.6.T3, F5.6.T4 e F5.7.T1 são ajustados no refinamento, antes da sprint. F6.2 só confirma ou ajusta a decisão, com migração se mudar.
- O identificador do culto (--culto) de cada execução desta Feature é o valor da coluna video de docs/corpus.csv, para que a liberação ao painel possa ser conferida contra esse arquivo. É proposta, a confirmar no refinamento.
- tools/ entra na imagem em F5.1.T4. Cada script novo de tools/ usado em job exige uma release nova pelo fluxo de F2.2 (F5.4.T3, F5.5.T3 e F5.7.T4).
- As premissas P7, P12, P15, P19, P21, P26 e P29 valem como na árvore.
- O valor de cada critério (3, 4 e 5) vai para o repositório de resultados de F2.8, com linhagem. A escrita em docs/poc-gate.md fica com F6.1.
- Story points e horas são sugestões para o refinamento. A capacidade do time não está registrada (P6).
- Os IDs F2.4.T4 (D7), F2.6.T1, F2.6.T6, F3.6.T3, F3.6.T4, F3.6.T5 e F7.8 vêm do detalhamento das outras Features citado nas revisões. A árvore (arvore_v1.json) não tem tasks e não tem F7.8. O escopo foi conferido no nível de PBI na árvore (F2.4, F2.6, F6.2 e F7.2) e, para F3.6, no detalhamento da Feature F3.
- Revisão não aplicada: F5.6.T7 (processamento e liberação) como dependente da task de publicação da imagem em F5.4 — F5.6 roda antes de F5.4, não espera F4.6, e F5.4 só entra na sprint depois de 11 PBIs. F5.6.T7 publica a própria release com o código de F5.2, e F5.4.T3 publica outra com F5.4.T1 e F5.4.T2.
- Revisão não aplicada: F5.4.T5, contar pela tabela event depois do job e pedir aprovação de custo para um job próprio — a contagem dos eventos com momento 'desconhecido' depois do corte passou para dentro do job de processamento (F5.4.T2), que já tem os eventos em memória (processar_culto.py:94-97). Ler a tabela event depois exigiria outro job com a chave de serviço. Sem job próprio, não há custo a aprovar.
- Revisão não aplicada em parte: F5.1.T3, 'não tem revogação' — o último passo da task já revogava o token. O defeito confirmado é outro: a revogação só pode acontecer depois de F5.1.T4, que depende de F5.1.T3, então T3 não podia terminar antes de T4 começar. A revogação virou a task F5.1.T5, e F5.1.T3 passou a depender de F2.6.T1 e F2.6.T6, como pedido.
- Revisão não aplicada em parte: F5.1.T4 como job de transferência único para F5.1 e F3.6 — o script de F5.1.T4 recebe a lista de vídeos e o destino no dataset como parâmetros e fica documentado para F3.6.T4 reutilizá-lo. O recorte por intervalo, que só F3.6 usa, fica com F3.6.T4 sobre o mesmo script (a imagem já tem ffmpeg; Dockerfile:5), para F5.1 não carregar código que não usa.
- Revisão não aplicada em parte: F5.6, task nova de Front end para 'decidir' a pilha — a escolha do framework continua no ADR de F2.4 revisto, que já a tem como critério (dependências técnicas). F5.6.T1 escolhe só o que o ADR não cobre (gerenciador de pacotes, versão do Node, lint e executor de testes) e registra por que cada dependência é necessária (CLAUDE.md:30).
- Revisão não aplicada em parte: F5.6, task nova de DevOps para o CI do front end e a integração Git — esse trabalho entrou em F5.6.T2, que já criava o projeto na Vercel ligado à pasta do painel. Uma task separada levaria F5.6 a 9 tasks. F5.6.T5 (lint dos textos fixos) depende só de F5.6.T1, porque o teste do lint roda no pytest do job Python que o CI já tem (.github/workflows/ci.yml:11).
- Cada task que roda job pago depende de 'Aprovação de Fabio (P7), com flavor, duração e custo previstos': F5.1.T4, F5.3.T3, F5.4.T4, F5.5.T3, F5.6.T7 e F5.7.T4. F5.3.T3 não foi citada na revisão, mas roda job na t4-small e segue a mesma regra (RN07).

### Pendências para sincronizar
- Azure DevOps: preencher Area Path (Time), Iteration Path (Sprint), Responsável e Prioridade da Feature e de cada PBI. Confirmar os story points sugeridos (P1).
- Azure DevOps: vincular F5 ao épico, criar F5.8 e vincular F5.1 a F5.8 como filhos de F5. Criar as tasks novas F5.1.T5, F5.6.T1 e F5.6.T9 e renumerar as demais tasks de F5.1 e F5.6.
- Refinamento: F5 tem 8 PBIs, F5.1 tem 8 tasks e F5.6 tem 9. Decidir entre manter as exceções ao limite de 7 ou mover F5.3 para F6 e F5.6.T7 para F5.8.
- Revisar F2.4 conforme a P3 revisada: o ADR 0002 registra, como critérios, o projeto Vercel, o framework do painel, o método de login do Supabase Auth, a proteção de deployment e a validade do token de acesso. D8 de F2.4.T4 registra o plano e os termos da Vercel como pendência e aponta F5.6.T9 como a task que a resolve. F2.4.T4 (D7) decide, antes de F5.6, onde fica o vínculo entre conta e papel e se a regra 6 vale para as contas da equipe. SDK e acesso de Space ficam só para F3.3. Até o ADR ser mesclado, F5.6, F5.7 e F5.8 não estão prontos para a sprint.
- Revisar F2.2: aceitar pré-release por tag num commit de branch, sem mover :latest (.github/workflows/docker.yml:23-25), para F5.3.
- Revisar F2.6: a chave de serviço não vai ao painel (o texto atual diz 'até F7.2, do Space de F5.6'). O painel usa a chave pública, e F5.6.T4 revoga os grants de anon e authenticated nas 8 tabelas. O inventário de credenciais de F2.6.T6 recebe o token de escrita dos jobs de cópia de F5.1 e de F3.6, como exceção de uso único, e as variáveis do projeto do painel na Vercel (só URL e chave pública). F2.6.T4 passa a subir o Supabase local no CI com as migrações, onde rodam os testes pgTAP de F5.6.T4 e F5.7.T1.
- Revisar F7.2, F7.3 e F7.6: trocar 'Space' por 'painel web na Vercel'. Os papéis pastor, mídia e DPO passam a ficar no local decidido em D7 de F2.4.T4 (hoje proposto em app_metadata do Supabase Auth) e estendem o papel de avaliador do gate e a tabela de execuções liberadas criados em F5.6. A ligação por OAuth do HF sai. As telas de F7.6 partem de F5.8.
- Revisar F7.2 e F7.8: as dependências de F6.2 para o local do vínculo entre conta e perfil passam a citar a decisão D7 de F2.4.T4, que F6.2 confirma ou ajusta.
- Revisar F6.2: a decisão sobre o local do vínculo entre conta e papel e sobre a regra 6 para as contas da equipe passa para F2.4.T4 (D7), antes de F5.6. F6.2 só confirma ou ajusta a decisão, com migração se mudar.
- Revisar F3.6: F3.6.T4 reutiliza o script de cópia de F5.1.T4, acrescentando o recorte por intervalo, e passa a depender de F5.1.T4 e de F2.2. F3.6.T3 e F3.6.T5 repetem o procedimento de token registrado por F5.1.T3 no inventário de F2.6.T6. F5.1.T1 já exclui os vídeos marcados como usados em F3.6.
- F1.3: incluir quais relatórios de culto entram no critério 4, a regra para nota repetida do mesmo avaliador, a visibilidade das notas entre avaliadores e o tratamento de nota faltante.
- Obter a confirmação de Fabio sobre o envio da transcrição de cultos públicos à API da Anthropic (P26).
- Resposta do usuário sobre a leitura da tabela moment pelo painel, registrada como pendência em D7 de F2.4.T4. A tabela de execuções liberadas já está na lista de D7.
- Identificar quem é o dono do projeto Supabase de desenvolvimento, que aplica as migrações e usa o SQL Editor.
- Revisar F6.2 (T1 e T2), F6.3.T1, F7.2.T2 e F7.4.T1: trocar 'F5.6 (primeira task: confirmação do plano e dos termos da Vercel; pendência)' pela ref F5.6.T9.
- Revisar F2.7.T1: trocar em docs/onprem.md:55 as referências a PBI-103 e PBI-106 (F5.4.T6 troca só a linha 7).

## Preview — PBI F5.1 (novo) · Selecionar três cultos públicos pt-BR inteiros e registrar licença, vídeo e momentos rotulados

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Selecionar três cultos públicos pt-BR inteiros e registrar licença, vídeo e momentos rotulados |
| Tipo | Product Backlog Item |
| Pai | F5 |
| Tags | fase-0; criterio-3; criterio-4; corpus; rotulagem |
| Estimativa | 8 pts (sugestão); tasks: 44 h |
| Dependências | F1.3, F3.5, F2.2, F1.1, F2.6 |
| Substitui | nenhum |

#### Descrição

Como responsável pelo gate da Fase 0 (Fabio Pinheiro)  
Quero três cultos públicos pt-BR inteiros, com a licença registrada, uma cópia no dataset privado sob tag e os momentos marcados à mão  
Para medir os critérios 3 e 4 sobre culto inteiro, o que os clipes da PIB não permitem

**Contexto:** docs/corpus.csv tem só o cabeçalho (docs/corpus.csv:1), e esse cabeçalho não tem coluna de licença, embora CONTRIBUTING.md:11 peça a licença em cada linha. O corpus da PIB é declarado insuficiente para os critérios 3 e 4 (samples/corpus/pib/README.md:16-18, não versionado; labels/README.md:16-17). O arquivo <video>_momentos.csv tem as colunas t_ini_s, t_fim_s e nome, e os nomes aceitos são louvor, oracao, avisos, palavra, apelo, ceia e encerramento (labels/README.md:16). O validador junta os arquivos da pasta pelo nome do vídeo e exige _faces.csv de cada vídeo e, no corpus, pelo menos um riso e quatro trechos neutros (tools/validar_labels.py:182-201,215-220). Por isso, uma pasta só com momentos sai com código 1, e momentos de cultos postos na pasta labels/ dos clipes, que o bench lê (docs/hf-jobs.md:28), também. validar_momentos recebe o último tempo do vídeo e não o usa (tools/validar_labels.py:136-155). A guarda reacao.guard.no_persistence procura, ao fim, arquivo de vídeo novo nas pastas vigiadas e resíduo em /dev/shm/reacao (reacao/guard.py:56-81). A imagem tem ffmpeg (Dockerfile:5) e copia só reacao/, processar_culto.py e bench.py (Dockerfile:9-10). Copiar um vídeo inteiro para o dataset passa por /dev/shm, cujo tamanho F2.2 mede (P19). Pela árvore, o token dos jobs não escreve no dataset do corpus (arvore_v1.json, F2.6). F3.6, na Feature F3, também copia vídeos públicos para o dataset por job no HF com um token de escrita de uso único, e pede que os cultos de F5.1 não incluam os vídeos que ela marcar em observacoes de docs/corpus.csv (detalhamento da Feature F3, F3.6, RN03).

**Regras de negócio:**
- RN01 – Só entram vídeos públicos, em pt-BR, de culto inteiro, com planos de plateia e com download permitido pela licença ou pelos termos da origem (CONTRIBUTING.md:11; docs/poc-gate.md:11).
- RN02 – Cada vídeo aceito tem em docs/corpus.csv a URL, a licença e a URL de onde a licença foi lida. Candidato sem licença verificável fica fora, com o motivo registrado.
- RN03 – Nenhum vídeo é gravado em disco local nem versionado no git. A cópia vai da origem ao dataset privado por um job no HF, passa só por /dev/shm e roda dentro de reacao.guard.no_persistence (CLAUDE.md, regra 1; reacao/guard.py:56-81; P3).
- RN04 – Vídeos e rótulos ficam sob tag e são lidos por tag ou revisão fixa, no padrão de F3.5.
- RN05 – Os momentos usam só os nomes de labels/README.md:16, com tempos em segundos, numa pasta do dataset separada da pasta labels/ dos clipes.
- RN06 – Os tipos de job que podem usar estes vídeos seguem a lista pré-registrada em F1.3.
- RN07 – O job de cópia roda com 'hf jobs run <imagem>@<digest>' pela imagem publicada no fluxo de F2.2 (RN06 da Feature).
- RN08 – O token de escrita dos jobs de cópia é fine-grained, com escrita só no dataset do corpus, criado pelo procedimento de F2.6.T1, registrado no inventário de credenciais de F2.6.T6 como exceção de uso único à política de F2.6 e revogado depois das três cópias.
- RN09 – Vídeos marcados em observacoes de docs/corpus.csv como usados em F3.6 ficam fora desta seleção, porque F3.6 os reserva ao bench de F4.6 e não permite que passem por job de pipeline antes dele (detalhamento da Feature F3, F3.6, RN03).

**Fora de escopo:**
- Rótulos de rostos e eventos (_faces.csv e _eventos.csv) desses cultos
- Comparação das fronteiras de momento (F5.5)
- Processamento dos cultos no pipeline (F5.4 e F5.6)
- Recorte de trechos por intervalo, usado só pela transferência de clipes de F3.6 (F3.6.T4)
- Vídeos em outros idiomas

#### Critérios de aceite

- docs/corpus.csv tem três linhas de vídeo com idioma pt-BR, permissão de download 'sim', licença e URL da fonte da licença preenchidas, e nenhuma delas é de vídeo marcado como usado em F3.6.
- Um candidato sem licença verificável ou sem permissão de download fica fora de docs/corpus.csv. A lista dos recusados, com o motivo, está na seção de vídeos públicos do dataset card.
- Os três vídeos estão no dataset privado sob uma tag. A seção de vídeos públicos do dataset card traz o id do job de cada cópia, a duração lida no job e a data da revogação do token de escrita, e o token aparece revogado na lista de tokens da conta e no inventário de credenciais de F2.6.T6.
- O log de cada job de cópia mostra '[guard] ok' e /dev/shm vazio ao fim, e 'hf jobs inspect' de cada job mostra a imagem com digest.
- Nenhum arquivo de vídeo aparece nos arquivos versionados do repositório git.
- Cada vídeo tem, no dataset e sob tag, um arquivo de momentos com nomes da lista de labels/README.md:16, numa pasta separada da pasta labels/ dos clipes.
- O validador de rótulos sai com código 0 na pasta de momentos dos cultos.
- O validador sai com código 1 quando um arquivo de momentos tem nome fora da lista, fim menor ou igual ao início, ou um momento que começa depois da duração registrada em docs/corpus.csv.
- O validador continua saindo com código 1 numa pasta de clipes que tem arquivo de eventos e não tem arquivo de rostos.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F5.1.T1 | Data Science | Levantar cultos públicos pt-BR inteiros candidatos e escrever o guia de marcação de momentos | 9 | F1.3 |
| F5.1.T2 | Governança e Privacidade | Conferir licença e permissão de download dos candidatos e registrar os aprovados em docs/corpus.csv | 4 | F5.1.T1 |
| F5.1.T3 | DevOps | Criar o token fine-grained com escrita só no dataset do corpus para os jobs de cópia e registrá-lo no inventário de credenciais | 2 | F2.6.T1, F2.6.T6 |
| F5.1.T4 | MLOps | Copiar os três vídeos para o dataset privado por job cpu-basic pela imagem com digest, dentro da guarda, e marcar com tag | 9 | F5.1.T2, F5.1.T3, F1.1, F2.2, F3.5, Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F5.1.T5 | DevOps | Revogar o token de escrita dos jobs de cópia e registrar a revogação no dataset card e no inventário de credenciais | 1 | F5.1.T4 |
| F5.1.T6 | Data Science | Fazer o validador aceitar a pasta de momentos dos cultos e conferir o início pela duração de docs/corpus.csv | 4 | — |
| F5.1.T7 | Data Science | Marcar os momentos dos três cultos e publicar os _momentos.csv sob tag | 12 | F5.1.T1, F5.1.T4, F5.1.T6 |
| F5.1.T8 | QA | Verificar os critérios de aceite de F5.1 | 3 | F5.1.T5, F5.1.T7 |

<details><summary>F5.1.T1 · [Data Science] Levantar cultos públicos pt-BR inteiros candidatos e escrever o guia de marcação de momentos</summary>

**Objetivo:** Entregar à governança a lista de candidatos com os campos de docs/corpus.csv e deixar escrito, antes da marcação, onde começa e onde termina cada momento.

**Passos previstos:**
1. Buscar vídeos públicos de culto inteiro em pt-BR que mostrem a plateia em parte do tempo.
2. Deixar de fora os vídeos marcados em observacoes de docs/corpus.csv como usados em F3.6 (RN09).
3. Para cada candidato, anotar url, duracao_min, resolucao, enquadramento, altura_rosto_mediana_px_estimada, idioma e observacoes (cabeçalho de docs/corpus.csv:1), assistindo na URL de origem, sem baixar.
4. Anotar onde a página de origem informa a licença e a permissão de download e entregar à governança mais de três candidatos, para cobrir recusas.
5. Escrever em labels/README.md o guia de marcação: regra de início e de fim para cada um dos 7 nomes de labels/README.md:16, alinhada à regra de pareamento de fronteiras pré-registrada em F1.3, com um exemplo de _momentos.csv.
6. Abrir PR citando F5.1 e pedir a revisão de Fabio no guia.

**Definição de pronto:** A lista de candidatos, sem vídeo marcado como usado em F3.6, com todos os campos de docs/corpus.csv e a fonte da licença de cada um, foi entregue à governança, e o PR do guia, revisado por Fabio, foi mesclado.

**Dependências:** F1.3

**Estimativa sugerida:** 9 h (sugestão; validar com o time)

</details>

<details><summary>F5.1.T2 · [Governança e Privacidade] Conferir licença e permissão de download dos candidatos e registrar os aprovados em docs/corpus.csv</summary>

**Objetivo:** Fazer docs/corpus.csv listar só vídeos com licença verificada e deixar registrados os recusados, com o motivo.

**Passos previstos:**
1. Para cada candidato, ler a licença e os termos da origem e registrar a URL onde foram lidos.
2. Recusar o candidato sem licença verificável ou sem permissão de download e anotar o motivo.
3. Acrescentar a docs/corpus.csv as colunas de licença e de fonte da licença (CONTRIBUTING.md:11) e as três linhas aprovadas, com permite_download = sim.
4. Redigir a seção de vídeos públicos do dataset card: URL, licença, data da coleta, recusados com o motivo e o registro de que os vídeos mostram a congregação.
5. Abrir PR citando F5.1.

**Definição de pronto:** O PR foi mesclado, docs/corpus.csv tem três linhas completas e o texto da seção de vídeos públicos do dataset card está pronto para F5.1.T4.

**Dependências:** F5.1.T1

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F5.1.T3 · [DevOps] Criar o token fine-grained com escrita só no dataset do corpus para os jobs de cópia e registrá-lo no inventário de credenciais</summary>

**Objetivo:** Dar aos jobs de cópia permissão de escrita só em ds-fabiopinheiro/reacao-poc-corpus, com o token registrado no inventário de F2.6.T6 e o procedimento descrito para F3.6 repetir.

**Passos previstos:**
1. Criar, pela conta dona e pelo procedimento de F2.6.T1, um token fine-grained com escrita só em ds-fabiopinheiro/reacao-poc-corpus (https://huggingface.co/docs/hub/security-tokens#best-practices).
2. Registrar o token no inventário de credenciais de F2.6.T6: nome, escopo, uso nos jobs de cópia de F5.1, exceção de uso único à política de F2.6 e revogação prevista em F5.1.T5.
3. Descrever no mesmo registro o procedimento de criação, de passagem ao job e de revogação, para F3.6.T3 e F3.6.T5 o repetirem.
4. Deixar o token pronto para ser passado ao job só pelo nome do secret (--secrets NOME), sem valor na linha de comando (https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets).

**Definição de pronto:** O token existe com escopo só no dataset do corpus, conferido na página de tokens da conta, e o inventário de F2.6.T6 traz o registro do token e o procedimento.

**Dependências:** F2.6.T1, F2.6.T6

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F5.1.T4 · [MLOps] Copiar os três vídeos para o dataset privado por job cpu-basic pela imagem com digest, dentro da guarda, e marcar com tag</summary>

**Objetivo:** Deixar os três vídeos no dataset privado sob tag, sem cópia em disco local e sem arquivo de vídeo fora de /dev/shm no job, com um script que F3.6.T4 possa reutilizar.

**Passos previstos:**
1. Escrever em tools/ um script que recebe a lista de vídeos (URL de origem e caminho de destino no dataset) e, para cada vídeo, dentro de reacao.guard.no_persistence com o diretório de trabalho, /tmp e o diretório de cache do usuário como raízes, baixa o vídeo da URL de origem direto para /dev/shm, envia ao dataset com upload_file e apaga o arquivo de /dev/shm, inclusive quando falha (reacao/guard.py:56-81).
2. Acrescentar ao Dockerfile a cópia de tools/ (hoje só reacao/, processar_culto.py e bench.py; Dockerfile:9-10) e, se o download exigir um programa que a imagem não tem, instalá-lo com versão fixa. Publicar a imagem por tag de release pelo fluxo de F2.2 e registrar o digest.
3. Conferir que o tamanho de cada vídeo cabe no /dev/shm medido em F2.2.
4. Pedir ao dono da conta a aprovação de custo (P7).
5. Rodar um job cpu-basic por vídeo com 'hf jobs run <imagem>@<digest>' e o comando explícito do script, com o token de F5.1.T3 pelo nome do secret, validando o comando com o lançador de F1.1 antes de submeter.
6. Ler a duração de cada cópia com ffprobe dentro do job e registrar, na seção de vídeos públicos do dataset card, o id do job e a duração de cada cópia. Abrir PR citando F5.1 que atualiza duracao_min em docs/corpus.csv.
7. Documentar em docs/hf-jobs.md os parâmetros do script e o comando do job, para F3.6.T4 reutilizá-los.
8. Publicar a seção do dataset card de F5.1.T2 e criar a tag no padrão de F3.5.

**Definição de pronto:** Os três vídeos estão no dataset sob tag, o log de cada job mostra '[guard] ok' e /dev/shm vazio ao fim, 'hf jobs inspect' mostra a imagem com digest, o dataset card traz o id do job e a duração de cada cópia, e o PR de duracao_min e dos parâmetros do script em docs/hf-jobs.md foi mesclado.

**Dependências:** F5.1.T2, F5.1.T3, F1.1, F2.2, F3.5, Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 9 h (sugestão; validar com o time)

</details>

<details><summary>F5.1.T5 · [DevOps] Revogar o token de escrita dos jobs de cópia e registrar a revogação no dataset card e no inventário de credenciais</summary>

**Objetivo:** Encerrar a permissão de escrita no dataset do corpus depois das três cópias.

**Passos previstos:**
1. Conferir no dataset que os três vídeos de F5.1.T4 estão sob tag.
2. Revogar pela conta dona o token de F5.1.T3.
3. Registrar a data da revogação na seção de vídeos públicos do dataset card e no inventário de credenciais de F2.6.T6.

**Definição de pronto:** O token aparece revogado na lista de tokens da conta, e a data da revogação está no dataset card e no inventário de F2.6.T6.

**Dependências:** F5.1.T4

**Estimativa sugerida:** 1 h (sugestão; validar com o time)

</details>

<details><summary>F5.1.T6 · [Data Science] Fazer o validador aceitar a pasta de momentos dos cultos e conferir o início pela duração de docs/corpus.csv</summary>

**Objetivo:** Fazer o validador aprovar a pasta de rótulos só de momentos dos cultos inteiros e recusar momentos fora da duração do vídeo, sem baixar vídeo.

**Passos previstos:**
1. Definir no PR a pasta do dataset que recebe os _momentos.csv dos cultos inteiros, separada da pasta labels/ dos clipes (docs/hf-jobs.md:28).
2. Em tools/validar_labels.py, deixar de exigir _faces.csv e os mínimos de riso e neutro quando a pasta só tiver _momentos.csv (hoje nas linhas 197-201 e 215-220).
3. Ler a duração do vídeo em docs/corpus.csv quando o vídeo não estiver disponível.
4. Recusar momento que começa depois da duração (hoje validar_momentos não usa o último tempo; linhas 136-155).
5. Acrescentar a tests/test_validar_labels.py cinco casos, com a pasta definida no primeiro passo: pasta só de momentos válida (código 0); nome fora da lista, fim menor ou igual ao início e início depois da duração (código 1); e pasta de clipes sem _faces.csv (código 1).
6. Rodar ruff check e pytest e abrir PR citando F5.1.

**Definição de pronto:** O PR foi mesclado, a pasta de momentos está definida nele, e os cinco casos de teste passam no CI.

**Dependências:** nenhuma

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F5.1.T7 · [Data Science] Marcar os momentos dos três cultos e publicar os _momentos.csv sob tag</summary>

**Objetivo:** Ter a marcação manual de momentos dos três cultos no dataset, sob tag, como referência do critério 3.

**Passos previstos:**
1. Assistir a cada culto na URL de origem e marcar os momentos pelo guia de F5.1.T1.
2. Gravar um <video>_momentos.csv por vídeo, com o nome do vídeo no dataset, na pasta definida em F5.1.T6.
3. Rodar o validador de F5.1.T6 na pasta de momentos.
4. Enviar os três arquivos ao dataset e criar a tag dos rótulos no padrão de F3.5.

**Definição de pronto:** Os três _momentos.csv estão no dataset sob tag, na pasta de momentos dos cultos, e o validador sai com código 0 nessa pasta.

**Dependências:** F5.1.T1, F5.1.T4, F5.1.T6

**Estimativa sugerida:** 12 h (sugestão; validar com o time)

</details>

<details><summary>F5.1.T8 · [QA] Verificar os critérios de aceite de F5.1</summary>

**Objetivo:** Dizer, para cada critério de aceite de F5.1, se passou ou não passou.

**Passos previstos:**
1. Conferir em docs/corpus.csv as três linhas com pt-BR, permissão de download, licença e fonte, e que nenhuma é de vídeo marcado como usado em F3.6.
2. Conferir na seção de vídeos públicos do dataset card os recusados com o motivo, os ids dos jobs de cópia, as durações e a data da revogação do token, e conferir com Fabio o token revogado na lista de tokens da conta e no inventário de F2.6.T6.
3. Conferir no Hub a tag dos vídeos e a tag dos rótulos. Conferir com 'hf jobs inspect' o digest da imagem de cada job de cópia e, no log, '[guard] ok' e /dev/shm vazio.
4. Rodar git ls-files e confirmar que não há arquivo .mp4.
5. Rodar o validador nos cenários dos critérios 7 a 9 e registrar os códigos de saída.

**Definição de pronto:** O relatório de verificação, com passou ou não passou por critério, está anexado ao PBI.

**Dependências:** F5.1.T5, F5.1.T7

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- docs/corpus.csv:1
- CONTRIBUTING.md:11
- README.pt-BR.md:34
- docs/poc-gate.md:11
- docs/hf-jobs.md:28
- labels/README.md:16-17
- tools/validar_labels.py:136-155,182-201,215-220
- reacao/guard.py:56-81
- Dockerfile:5,9-12
- samples/corpus/pib/README.md:16-18 (não versionado)
- CLAUDE.md (regra 1)
- arvore_v1.json: F2.6 (token dos jobs sem escrita no dataset do corpus)
- detalhamento da Feature F3: F3.6 (RN03 e tasks F3.6.T3 a F3.6.T5)
- premissas P19, P24 e P27
- https://huggingface.co/docs/hub/security-tokens#best-practices
- https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets

#### Verificação INVEST: pontos que falharam
- S: o esforço de marcação depende da duração dos três cultos, ainda desconhecida. Se não couber na sprint, dividir por culto.
- Decomposição: 8 tasks, uma acima do limite de 7 (taskflow.md:40). A revogação do token fica separada porque só acontece depois das cópias.

#### Premissas
- A disciplina DevOps foi acrescentada para criar e revogar um token de escrita restrito ao dataset do corpus. F2.6 cria tokens de jobs sem escrita no corpus, então este token é exceção de uso único, registrada no inventário de F2.6.T6.
- F2.6 entrou como dependência porque F5.1.T3 segue o procedimento de token de F2.6.T1 e registra o token no inventário de F2.6.T6.
- F2.2 entrou como dependência porque o job de cópia guarda o vídeo inteiro em /dev/shm, cujo tamanho não está documentado (P19).
- F1.1 entrou como dependência porque a definição de pronto do job de cópia usa a linha '[guard] ok', que hoje é impressa no finally da guarda mesmo quando o corpo falha (reacao/guard.py:66-81), e F1.1 corrige isso (issue #2). O lançador de F1.1 também valida o comando do job.
- tools/ entra na imagem em F5.1.T4, porque o job de cópia é o primeiro job desta Feature que roda um script de tools/. Se a origem dos vídeos exigir um programa de download que a imagem não tem, ele entra com versão fixa na mesma release.
- O script de F5.1.T4 recebe a lista de vídeos e o destino no dataset como parâmetros, para F3.6.T4 reutilizá-lo em vez de escrever outro job. O recorte por intervalo, que só F3.6 usa, é acrescentado por F3.6.T4 ao mesmo script.
- O nome da pasta de momentos dos cultos é decisão do PR de F5.1.T6 (P24).
- As antigas tasks de levantamento de candidatos e de guia de marcação foram unidas em F5.1.T1 (mesma disciplina e mesma pessoa).
- A revogação do token saiu de F5.1.T3 e virou F5.1.T5, porque só pode acontecer depois de F5.1.T4, que depende de F5.1.T3. Com isso o PBI tem 8 tasks, uma acima do limite de 7 (taskflow.md:40). A task tem 1 h e é feita pela conta dona, como F3.6.T5.
- Os momentos são marcados assistindo ao vídeo na URL pública de origem, sem download local. É dedução, a confirmar com Fabio. Se a governança exigir marcar sobre a cópia do dataset, a marcação passa pela ferramenta de F3.3 no Space privado.
- A cópia no dataset é o mesmo arquivo da origem, então os tempos marcados na URL pública valem para a cópia. O job de cópia registra a duração para conferência.
- Vídeos públicos de culto mostram a congregação, e convicção religiosa é dado pessoal sensível (LGPD, art. 5º, II; https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm). A governança registra no dataset card como esses vídeos são usados na Fase 0. Se o encarregado, que ainda não tem nome, pedir análise adicional, ela vira pendência antes de F5.4.
- A duração dos cultos é desconhecida, então a estimativa de marcação é sugestão.
- Story points e horas são sugestões.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável e vínculo com a Feature F5
- Azure DevOps: criar F5.1.T5 (revogação do token) e renumerar as tasks seguintes
- Nomes das tags dos vídeos públicos e dos rótulos de momento e nome da pasta de momentos dos cultos (P24)
- Confirmar com Fabio a marcação pela URL pública
- F2.6.T6: registrar no inventário de credenciais o token de escrita dos jobs de cópia de F5.1 e de F3.6 como exceção de uso único
- F3.6: F3.6.T4 passa a reutilizar o script de F5.1.T4 e a depender de F5.1.T4 e de F2.2; F3.6.T3 e F3.6.T5 repetem o procedimento de F5.1.T3 e F5.1.T5
- Refinamento: F5.1 tem 8 tasks, uma acima do limite de 7

## Preview — PBI F5.2 (novo) · Gerar momentos e insights com rótulos em português e em ordem de tempo, com volta à heurística quando o LLM falha

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Gerar momentos e insights com rótulos em português e em ordem de tempo, com volta à heurística quando o LLM falha |
| Tipo | Product Backlog Item |
| Pai | F5 |
| Tags | fase-0; criterio-4; llm; insights; linguagem-controlada |
| Estimativa | 8 pts (sugestão); tasks: 33 h |
| Dependências | F1.7, F1.5 |
| Substitui | nenhum |

#### Descrição

Como pastor Filipe, leitor do relatório do culto  
Quero ler os insights com rótulos em português e na ordem do culto, e receber o relatório mesmo quando a API de linguagem falhar  
Para ligar cada reação observada ao trecho da mensagem sem precisar decifrar identificadores técnicos

**Contexto:** Em reacao/moments.py, a chamada client.messages.create (linha 63) fica fora do try (linhas 65-69). Um erro da API interrompe processar_culto.py depois de gravar as janelas e antes de gravar momentos, eventos e insights (processar_culto.py:83,92-100). A linha 67 filtra os momentos pela lista e pode devolver lista vazia sem voltar à heurística; nesse caso todo evento fica com momento 'desconhecido' (reacao/moments.py:72-76), e o lint rejeita todos os insights (reacao/lint.py:34-35). Em reacao/insights.py:52-53, as exceções são descartadas sem log. O id 'claude-sonnet-4-6' está fixo em reacao/moments.py:63 e em reacao/insights.py:48, e o run_log não registra se houve LLM (processar_culto.py:104-106). O texto do modelo de frase põe o sinal e o momento crus no texto, como pct_voltados e oracao (reacao/insights.py:22-24; reacao/moments.py:7). Os insights são ordenados por magnitude (reacao/insights.py:30). O README promete de 3 a 8 insights (README.pt-BR.md:14), mas o código só limita o máximo. A sequência de momentos, eventos e insights fica dentro de main() (processar_culto.py:92-100). Com --provider mock, o pipeline não transcreve (processar_culto.py:86), e segment() volta à heurística sem chamar o LLM quando não há segmentos (reacao/moments.py:48-50). O vídeo sintético do teste tem 10 s (tests/test_pipeline_mock.py:26), o que dá uma janela de 30 s, e um evento exige 3 janelas de queda sustentada ou 6 janelas anteriores para um pico (reacao/events.py:11-12,31-37). Os testes removem ANTHROPIC_API_KEY de propósito, e o caminho com LLM não tem teste (tests/test_insights.py:11-13; tests/test_pipeline_mock.py:19). O README usa 'voltados ao palco', 'sorrindo' e 'oração' (README.pt-BR.md:12-13).

**Regras de negócio:**
- RN01 – Quando a API de linguagem falha na segmentação de momentos (autenticação, limite, rede, resposta sem JSON válido ou JSON sem nenhum momento da lista), os momentos vêm da heurística de palavras-chave (reacao/moments.py:18-44), e a execução continua.
- RN02 – Quando a API falha na redação de um insight, fica o texto do modelo de frase (reacao/insights.py:21-25).
- RN03 – Toda exceção da API vai para o log do job com o tipo e a mensagem, sem o prompt e sem trecho da transcrição. F6.2 decide sobre trechos em log.
- RN04 – O id do modelo de linguagem vem da configuração da execução. O código não tem id fixo.
- RN05 – Cada execução registra o caminho dos momentos (LLM ou heurística), quantos insights vieram do LLM e quantos do modelo de frase, o id do modelo, a versão de cada prompt e o motivo de falha, se houver. F2.8 leva esses campos à linhagem.
- RN06 – O texto para o pastor mostra sinais e momentos por rótulos em português: pct_voltados vira 'rostos voltados ao palco', pct_sorrindo vira 'rostos sorrindo' e oracao vira 'oração' (README.pt-BR.md:12-13).
- RN07 – Com mais de 8 eventos, ficam os 8 de maior magnitude (reacao/insights.py:30). A lista entregue sai em ordem de tempo.
- RN08 – O comportamento com menos de 3 eventos segue a regra confirmada por Fabio antes da sprint (premissa), fica escrito no README.pt-BR.md e é coberto por teste. O código não cria insight sem evento.
- RN09 – Todo texto continua passando pelo lint (CLAUDE.md, regra 4).
- RN10 – A transcrição só vai à API com a confirmação de Fabio (P26).

**Fora de escopo:**
- Modelo de linguagem local ou hospedado no HF (P26)
- Troca do modelo de linguagem em uso
- Medição da transcrição de culto inteiro contra o corte de 60000 caracteres (F5.4)
- Comparação das fronteiras de momento (F5.5)
- Exibição no painel (F5.6 e F5.8)

#### Critérios de aceite

- Com segmentos de transcrição sintéticos, agregados sintéticos que geram pelo menos um evento e um cliente simulado que levanta erro de autenticação, a função que reúne momentos, eventos e insights termina sem exceção, devolve momentos da heurística, eventos e insights, e o registro da execução mostra o caminho 'heurística' e o motivo da falha.
- Com resposta sem JSON válido, ou com JSON válido sem nenhum momento da lista (lista vazia ou só nomes fora da lista), os momentos vêm da heurística, e o registro da execução mostra o caminho e o motivo.
- Com um cliente simulado que levanta exceção, o log registra o tipo e a mensagem da exceção e não contém nenhum texto da transcrição sintética nem do prompt.
- Com um cliente simulado que devolve uma frase reprovada pelo lint, o insight fica com o texto do modelo de frase e é contado como modelo de frase no registro da execução.
- O id do modelo vem só da configuração: trocar o id na configuração muda o id registrado na execução, e uma busca em reacao/*.py não encontra id de modelo de linguagem.
- Nenhum texto de insight de teste contém pct_voltados, pct_sorrindo ou oracao. No lugar, aparecem 'rostos voltados ao palco', 'rostos sorrindo' e 'oração'.
- Com eventos nos minutos 40, 10 e 25, de magnitudes diferentes, os insights saem na ordem 10, 25 e 40.
- Com 9 eventos, saem 8 insights, e o de menor magnitude fica de fora.
- O README.pt-BR.md descreve o que acontece com menos de 3 eventos, conforme a regra confirmada por Fabio, e um teste com 2 eventos verifica esse comportamento.
- ruff check e pytest passam, inclusive o teste de contrato do registro da execução criado em F1.5 e tests/test_pipeline_mock.py.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F5.2.T1 | Backend | Pôr a chamada do LLM de momentos no tratamento de erro, voltar à heurística sem momento válido e testar os caminhos de exceção | 6 | — |
| F5.2.T2 | MLOps | Ler o id do modelo da configuração da execução e calcular a versão de cada prompt | 3 | — |
| F5.2.T3 | Backend | Extrair a sequência de momentos, eventos e insights para uma função e gravar no run_log o caminho, o modelo e a versão dos prompts | 8 | F5.2.T1, F5.2.T2, F1.5 |
| F5.2.T4 | Backend | Mostrar sinais e momentos em português e listar os insights em ordem de tempo | 4 | — |
| F5.2.T5 | Machine Learning | Ajustar o prompt aos rótulos em português e testar com cliente simulado a resposta sem JSON, a frase reprovada e a função completa | 5 | F5.2.T1, F5.2.T3, F5.2.T4 |
| F5.2.T6 | Data Science | Documentar e testar o comportamento com menos de 3 eventos | 3 | F5.2.T4 |
| F5.2.T7 | QA | Verificar os critérios de aceite de F5.2 | 4 | F5.2.T3, F5.2.T5, F5.2.T6 |

<details><summary>F5.2.T1 · [Backend] Pôr a chamada do LLM de momentos no tratamento de erro, voltar à heurística sem momento válido e testar os caminhos de exceção</summary>

**Objetivo:** Fazer uma falha da API, ou uma resposta sem momento da lista, levar à heurística nos momentos e ao modelo de frase nos insights, com a exceção registrada no log sem texto da transcrição.

**Passos previstos:**
1. Em reacao/moments.py, mover client.messages.create (linha 63) para dentro do try (linhas 65-69), com volta a _heuristic.
2. Tratar também a falha ao criar o cliente, a resposta sem bloco de texto e o JSON válido que, depois do filtro da linha 67, não deixa nenhum momento. Nos três casos, voltar a _heuristic.
3. Em reacao/insights.py:52-53, trocar 'except Exception: pass' por um registro do tipo e da mensagem da exceção, sem o prompt e sem trecho da transcrição.
4. Devolver ao chamador o caminho usado e o motivo da falha, para F5.2.T3 gravar.
5. Escrever testes com cliente simulado para erro de autenticação, falha ao criar o cliente, resposta sem bloco de texto e JSON válido sem momento da lista. Em cada um, conferir os momentos da heurística, o caminho devolvido e que o log não contém texto da transcrição sintética nem do prompt.

**Definição de pronto:** Os testes desta task passam no CI sem chamada de rede, e ruff check e pytest estão verdes.

**Dependências:** nenhuma

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F5.2.T2 · [MLOps] Ler o id do modelo da configuração da execução e calcular a versão de cada prompt</summary>

**Objetivo:** Tirar o id do modelo do código e ter uma versão de prompt que possa ser registrada por execução.

**Passos previstos:**
1. Tirar 'claude-sonnet-4-6' de reacao/moments.py:63 e reacao/insights.py:48 e ler o id de uma variável de configuração da execução.
2. Com a chave presente e sem id configurado, seguir a regra confirmada por Fabio antes da sprint (premissa) e registrar o motivo.
3. Calcular a versão de cada prompt a partir do texto do modelo do prompt (hash curto) e passá-la ao registro.
4. Documentar a variável em docs/hf-jobs.md, passada por -e ou como secret pelo nome.

**Definição de pronto:** Uma busca pelo id do modelo em reacao/*.py não encontra nada, e um teste mostra que trocar a variável troca o id passado ao registro.

**Dependências:** nenhuma

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F5.2.T3 · [Backend] Extrair a sequência de momentos, eventos e insights para uma função e gravar no run_log o caminho, o modelo e a versão dos prompts</summary>

**Objetivo:** Ter a sequência de processar_culto.py:92-100 testável sem vídeo e deixar registrado em cada execução se houve LLM, com qual modelo e com qual versão de prompt.

**Passos previstos:**
1. Extrair as linhas 92-100 de processar_culto.py para uma função que recebe segmentos, agregados, duração e culto e devolve momentos, eventos, insights, rejeitados e o caminho usado, sem gravar. main() continua gravando pelo Store.
2. Abrir uma issue antes de mexer no schema (CONTRIBUTING.md:13).
3. Criar uma migração nova com colunas no run_log para o caminho dos momentos, o número de insights do LLM e do modelo de frase, o id do modelo, as versões dos prompts e o motivo de falha.
4. Montar esses campos em processar_culto.py (linhas 103-107) e enviá-los pelo Store.
5. Atualizar o teste de contrato de F1.5 e confirmar que tests/test_schema.py e tests/test_pipeline_mock.py passam.

**Definição de pronto:** A função existe e é chamada por main(), a migração está no repositório, o teste de contrato, o test_schema e o test_pipeline_mock passam, e uma execução local com provider mock grava os campos novos em out/run_log.json.

**Dependências:** F5.2.T1, F5.2.T2, F1.5

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F5.2.T4 · [Backend] Mostrar sinais e momentos em português e listar os insights em ordem de tempo</summary>

**Objetivo:** Fazer o texto do insight usar rótulos em português e a lista seguir a ordem do culto.

**Passos previstos:**
1. Criar no pacote reacao um arquivo versionado de rótulos (pct_voltados para 'rostos voltados ao palco', pct_sorrindo para 'rostos sorrindo', oracao para 'oração' e os demais momentos), que o pipeline lê e que o painel usa por uma cópia no próprio diretório (F5.8.T1).
2. Usar os rótulos no texto do modelo de frase (reacao/insights.py:22-24) e manter o campo momento com o código.
3. Manter a seleção dos 8 de maior magnitude (reacao/insights.py:30) e ordenar a lista final por início do evento.
4. Passar os textos novos pelo lint e ajustar tests/test_insights.py.

**Definição de pronto:** Os testes de rótulos, de ordem e de 9 eventos passam, e nenhum texto de teste contém pct_voltados, pct_sorrindo ou oracao.

**Dependências:** nenhuma

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F5.2.T5 · [Machine Learning] Ajustar o prompt aos rótulos em português e testar com cliente simulado a resposta sem JSON, a frase reprovada e a função completa</summary>

**Objetivo:** Cobrir com testes sem rede os demais caminhos do LLM e a função de F5.2.T3, e manter os rótulos em português na reescrita.

**Passos previstos:**
1. Ajustar o prompt de insights (reacao/insights.py:41-45) para manter os rótulos em português do texto de entrada.
2. Estender o cliente simulado de F5.2.T1 com duas respostas: texto sem JSON válido e frase reprovada pelo lint.
3. Escrever um teste para cada resposta, conferindo os momentos da heurística, o texto do modelo de frase e o caminho devolvido.
4. Escrever um teste da função de F5.2.T3 com segmentos sintéticos, agregados sintéticos que geram pelo menos um evento (reacao/events.py:11-37) e o cliente simulado que levanta erro de autenticação, conferindo que ela termina sem exceção e devolve momentos, eventos e insights.

**Definição de pronto:** Os testes novos passam no CI sem chamada de rede.

**Dependências:** F5.2.T1, F5.2.T3, F5.2.T4

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F5.2.T6 · [Data Science] Documentar e testar o comportamento com menos de 3 eventos</summary>

**Objetivo:** Deixar escrito e testado o que o relatório entrega quando o culto tem menos de 3 eventos.

**Passos previstos:**
1. Escrever no README.pt-BR.md:14 a regra confirmada por Fabio antes da sprint (premissa).
2. Escrever um teste com 2 eventos que verifica o comportamento.
3. Abrir PR citando F5.2.

**Definição de pronto:** O README.pt-BR.md está atualizado, e o teste com 2 eventos passa no CI.

**Dependências:** F5.2.T4

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F5.2.T7 · [QA] Verificar os critérios de aceite de F5.2</summary>

**Objetivo:** Dizer, para cada critério de aceite de F5.2, se passou ou não passou.

**Passos previstos:**
1. Rodar ruff check e pytest e localizar o teste de cada critério, inclusive o da função com agregados sintéticos e o do conteúdo do log.
2. Conferir, no out/run_log.json de uma execução de teste, os campos de caminho, modelo, versão de prompt e motivo.
3. Ler um relatório de teste e conferir os rótulos em português e a ordem de tempo.
4. Buscar o id do modelo em reacao/*.py.
5. Conferir a regra de menos de 3 eventos no README.pt-BR.md.

**Definição de pronto:** O relatório de verificação, com passou ou não passou por critério, está anexado ao PBI.

**Dependências:** F5.2.T3, F5.2.T5, F5.2.T6

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- reacao/moments.py:7,18-44,47-69,72-76
- reacao/insights.py:8,21-59
- reacao/lint.py:34-35
- reacao/events.py:11-12,31-37
- processar_culto.py:83,86,92-107
- tests/test_insights.py:11-13
- tests/test_pipeline_mock.py:18-19,26
- README.pt-BR.md:12-14
- docs/poc-gate.md:12
- docs/onprem.md:50-52
- CONTRIBUTING.md:13
- Dockerfile:9
- https://vercel.com/docs/builds/configure-a-build#root-directory
- premissa P26

#### Verificação INVEST: pontos que falharam
- S: pela P6, F5.2 está entre os PBIs mais largos. Se não couber na sprint, separar 'tolerância a falha e registro do caminho' de 'rótulos em português e ordem de tempo'.

#### Premissas
- F1.5 entrou como dependência porque os campos novos do run_log precisam de migração, e F1.5 cria o teste de contrato entre o Store e as migrações.
- A sequência de processar_culto.py:92-100 é extraída para uma função testável em F5.2.T3, porque o pipeline com --provider mock não transcreve (processar_culto.py:86) e não tem como receber uma transcrição injetada.
- Regra proposta para menos de 3 eventos, a confirmar por Fabio: o relatório traz um insight por evento que passar no lint, sem completar até 3, e o registro da execução guarda o número de eventos.
- Com a chave presente e sem id de modelo configurado, a execução usa a heurística e o modelo de frase e registra o motivo. É uma proposta, a confirmar por Fabio.
- As duas regras acima são item de Definition of Ready: F5.2 só entra na sprint depois que Fabio as confirmar por escrito no PBI, porque F5.2.T2 e F5.2.T6 as implementam.
- A versão de cada prompt é calculada a partir do texto do prompt, para mudar sempre que o texto mudar.
- O rótulo 'rostos sorrindo' segue README.pt-BR.md:12. Fabio e Filipe revisam os rótulos na leitura de F5.8.
- O arquivo de rótulos em português fica no pacote reacao, que a imagem copia (Dockerfile:9). O painel usa uma cópia no próprio diretório, conferida por um teste criado em F5.8.T1, porque o app na Vercel não acessa arquivos fora do Root Directory (https://vercel.com/docs/builds/configure-a-build#root-directory).
- Story points e horas são sugestões.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável e vínculo com a Feature F5
- Definition of Ready: Fabio confirma a regra para menos de 3 eventos e o comportamento sem id de modelo configurado antes da sprint
- Fabio confirma o envio da transcrição à API da Anthropic (P26)

## Preview — PBI F5.3 (novo) · Executar a expressão e a pose na GPU com processamento em lote se o critério 5 reprovar

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Executar a expressão e a pose na GPU com processamento em lote se o critério 5 reprovar |
| Tipo | Product Backlog Item |
| Pai | F5 |
| Tags | fase-0; criterio-5; gpu; condicional |
| Estimativa | 5 pts (sugestão); tasks: 19 h |
| Dependências | F2.7, F4.6, F1.6, F5.4 (só quando o acionamento vier da medição de F5.4) |
| Substitui | nenhum |

#### Descrição

Como responsável pelo gate e pelo dimensionamento (Fabio Pinheiro)  
Quero que a expressão e a pose rodem na GPU da T4, com a pose processada em lote  
Para reduzir o tempo e o custo por hora de vídeo quando o critério 5 reprovar, sem mudar os agregados

**Contexto:** O hsemotion-onnx 0.3.1 cria a sessão ONNX com providers=['CPUExecutionProvider'] (hsemotion_onnx/facial_emotions.py:40, instalado). A expressão já é inferida em lote por quadro (facial_emotions.py:65-67), mas roda em CPU. A pose chama SixDRepNet.predict um recorte por vez (reacao/pose.py:21-23), e predict não usa torch.no_grad (sixdrepnet/regressor.py:51-80, instalado). A pose escolhe o dispositivo sem registrá-lo (reacao/pose.py:15). O detector tenta CUDA primeiro (reacao/detect.py:15). O CI instala só .[dev], opencv e numpy e roda o pipeline com o motor mock (.github/workflows/ci.yml:9,15). hsemotion-onnx e sixdrepnet, que requer torch, estão só no extra gpu (pyproject.toml:14-20; sixdrepnet-0.1.6.dist-info/METADATA, instalado). A imagem é publicada em qualquer tag v* ou por workflow_dispatch, e o workflow também marca :latest (.github/workflows/docker.yml:2-5,23-25). A meta do critério 5 é até US$ 1,50 e até 2 h por hora de vídeo na t4-small (docs/poc-gate.md:13). A paridade aceita diferença de até 1 p.p. em todos os percentuais, com o mesmo n (docs/onprem.md:57).

**Regras de negócio:**
- RN01 – O PBI só é acionado se o critério 5 medido em F4.6 ou em F5.4 passar de US$ 1,50 ou de 2 h por hora de vídeo (P15; docs/poc-gate.md:13).
- RN02 – Sem GPU disponível, expressão e pose rodam em CPU, e o log e o registro de linhagem de F2.8 dizem o dispositivo usado em cada uma.
- RN03 – A troca de dispositivo não pode alterar os agregados: a diferença fica em até 1 p.p. em todos os percentuais, com o mesmo n, janela a janela (docs/onprem.md:57). O script de F2.7 faz essa medida.
- RN04 – A nova medição usa o mesmo vídeo, o mesmo motor e a mesma fórmula de F1.3 da medição que reprovou.
- RN05 – Só mudam o dispositivo e o lote da expressão e da pose. Detector, limiares, k-mínimo e janela ficam iguais.
- RN06 – A imagem medida é publicada com digest antes do merge, por tag de pré-release no commit da branch, pelo fluxo de F2.2. A mudança só entra em main se a paridade passar.

**Fora de escopo:**
- Troca de motor ou de detector (F4.7)
- Detecção por ladrilhos
- Otimização da decodificação e da transcrição
- Outras otimizações além de dispositivo e lote

#### Critérios de aceite

- O log de um job t4-small mostra a sessão de expressão com CUDAExecutionProvider e a pose em CUDA.
- No teste de integração em CPU do CI (F1.6), o pipeline termina com código 0, e o log registra CPU como dispositivo da expressão e da pose.
- O teste de equivalência da pose em lote e o teste de scores da sessão ONNX passam no job do CI que instala os motores reais (F1.6).
- O relatório de paridade entre a execução anterior e a nova, com o mesmo vídeo, mostra diferença máxima de até 1 p.p. em cada percentual e o mesmo n em todas as janelas.
- Se a paridade reprovar, a mudança não é mesclada em main, e o valor anterior do critério 5 continua valendo.
- O tempo e o custo por hora de vídeo da nova execução estão no repositório de resultados, ao lado dos valores anteriores, com os dois run_id e o digest da pré-release.
- O tempo por hora de vídeo da nova execução é menor que o da execução anterior com o mesmo vídeo.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F5.3.T1 | Visão Computacional | Processar a pose em lote na GPU com torch.no_grad e registrar o dispositivo da pose | 6 | F1.6 |
| F5.3.T2 | Machine Learning | Criar a sessão ONNX do HSEmotion com CUDAExecutionProvider e volta para CPU e registrar os providers efetivos | 5 | F1.6 |
| F5.3.T3 | MLOps | Publicar a imagem da branch por pré-release, remedir tempo e custo e rodar a paridade | 5 | F5.3.T1, F5.3.T2, F2.7, Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F5.3.T4 | QA | Verificar os critérios de aceite de F5.3 | 3 | F5.3.T3 |

<details><summary>F5.3.T1 · [Visão Computacional] Processar a pose em lote na GPU com torch.no_grad e registrar o dispositivo da pose</summary>

**Objetivo:** Fazer a pose de todos os recortes de um quadro sair de uma única inferência, sem cálculo de gradiente, com o dispositivo registrado.

**Passos previstos:**
1. Em reacao/pose.py, trocar o laço de predict por recorte (linhas 21-23) por um tensor único com todos os recortes do quadro.
2. Reproduzir o pré-processamento de SixDRepNet.predict (BGR para RGB, redimensionamento, recorte de 224 e normalização; regressor.py:45-48,64-68) e chamar o modelo dentro de torch.no_grad.
3. Manter o caminho em CPU quando torch.cuda não estiver disponível (reacao/pose.py:15).
4. Registrar no log e no registro de linhagem de F2.8 o dispositivo efetivo da pose.
5. Testar, no job do CI com os motores reais de F1.6, que o lote dá os mesmos ângulos que a chamada um a um, com a tolerância registrada no teste.

**Definição de pronto:** O teste de equivalência passa no job do CI de F1.6, o dispositivo da pose aparece no log desse job, e o PR cita F5.3.

**Dependências:** F1.6

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F5.3.T2 · [Machine Learning] Criar a sessão ONNX do HSEmotion com CUDAExecutionProvider e volta para CPU e registrar os providers efetivos</summary>

**Objetivo:** Fazer a expressão rodar na GPU quando houver GPU, com os mesmos scores da sessão em CPU.

**Passos previstos:**
1. Em reacao/providers/hsemotion.py, recriar a sessão do HSEmotionRecognizer com os providers de CUDA e de CPU, porque o pacote fixa CPU (facial_emotions.py:40).
2. Registrar no log e no registro de linhagem de F2.8 os providers efetivos da sessão, sem coluna nova no run_log.
3. Testar, no job do CI de F1.6, que os scores dos mesmos recortes não mudam em relação à sessão original.
4. Conferir na imagem de F2.2 que onnxruntime.get_available_providers() inclui CUDAExecutionProvider.

**Definição de pronto:** O teste de scores passa no job do CI de F1.6, e os providers efetivos aparecem no log desse job.

**Dependências:** F1.6

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F5.3.T3 · [MLOps] Publicar a imagem da branch por pré-release, remedir tempo e custo e rodar a paridade</summary>

**Objetivo:** Medir o efeito da mudança sobre o critério 5 e provar que os agregados não mudaram, antes de mesclar.

**Passos previstos:**
1. Publicar a imagem da branch com digest antes do merge, por tag de pré-release no commit da branch, pelo fluxo de F2.2 (hoje .github/workflows/docker.yml:2-5 publica em qualquer tag v*), e registrar o digest.
2. Pedir ao dono da conta a aprovação de custo (P7).
3. Rodar na t4-small, com 'hf jobs run <imagem>@<digest>', o mesmo culto da medição que reprovou, com o mesmo motor e a fórmula de F1.3.
4. Rodar o script de paridade de F2.7 entre os dois run_id.
5. Gravar no repositório de resultados o tempo, o custo, o relatório de paridade, os dois run_id e o digest.
6. Se a paridade passar, mesclar o PR. Se reprovar, fechar o PR sem merge e registrar o motivo no repositório de resultados.

**Definição de pronto:** O repositório de resultados tem o tempo e o custo de antes e de depois, o relatório de paridade, os dois run_id e o digest da pré-release, e o PR foi mesclado só se a paridade passou.

**Dependências:** F5.3.T1, F5.3.T2, F2.7, Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F5.3.T4 · [QA] Verificar os critérios de aceite de F5.3</summary>

**Objetivo:** Dizer, para cada critério de aceite de F5.3, se passou ou não passou.

**Passos previstos:**
1. Conferir no log do job t4-small a sessão de expressão com CUDAExecutionProvider e a pose em CUDA.
2. Conferir no log do teste de integração do CI de F1.6 o código 0 e o dispositivo CPU da expressão e da pose, e o resultado dos testes de equivalência e de scores.
3. Conferir o relatório de paridade: diferença máxima por percentual e n de cada janela.
4. Se a paridade reprovar, conferir que o PR não foi mesclado.
5. Comparar o tempo por hora de vídeo de antes e de depois e conferir o digest da pré-release com 'hf jobs inspect'.

**Definição de pronto:** O relatório de verificação, com passou ou não passou por critério, está anexado ao PBI.

**Dependências:** F5.3.T3

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- hsemotion_onnx/facial_emotions.py:40,65-67 (instalado, 0.3.1)
- reacao/pose.py:15-24
- sixdrepnet/regressor.py:45-80 (instalado, 0.1.6)
- sixdrepnet-0.1.6.dist-info/METADATA (Requires-Dist: torch; instalado)
- reacao/providers/hsemotion.py:10-33
- reacao/detect.py:14-15
- .github/workflows/ci.yml:9,15
- .github/workflows/docker.yml:2-5,23-25
- pyproject.toml:14-20
- CONTRIBUTING.md:13
- docs/onprem.md:11,57
- docs/poc-gate.md:13
- premissas P15, P26 e P29

#### Verificação INVEST: pontos que falharam
- V: o PBI só tem valor se o critério 5 reprovar (P15).
- E: o ganho não pode ser estimado antes da medição de F4.6 ou F5.4.

#### Premissas
- O PBI é condicional (P15). As dependências valem só se ele for acionado (P29).
- F5.4 entrou como dependência quando o acionamento vem dessa medição, porque a nova medição repete o mesmo culto.
- F1.6 entrou como dependência (só se F5.3 for acionado, P29), porque os testes em CPU desta mudança precisam de torch, sixdrepnet, hsemotion-onnx e dos pesos, que o CI atual não instala (.github/workflows/ci.yml:9).
- Os providers efetivos da expressão e o dispositivo da pose vão para o log e para o registro de linhagem de F2.8, e não para uma coluna do run_log, para não exigir migração (CONTRIBUTING.md:13; F1.5). F2.7, do qual este PBI depende, já depende de F2.5 e de F2.8.
- A execução sem GPU usa o CI de F1.6, e não uma execução local com o motor real, porque as exceções da P26 cobrem só o CI e o docker run com a fixture sintética.
- A imagem publicada para a remedição vem de tag de pré-release no commit da branch. Como .github/workflows/docker.yml:23-25 também marca :latest, F2.2 precisa aceitar a pré-release sem mover :latest (pendência). Os jobs usam só o digest.
- A imagem de F2.2 precisa ter o CUDAExecutionProvider disponível no onnxruntime. O levantamento mostrou onnxruntime de CPU e onnxruntime-gpu instalados juntos na resolução de .[gpu,llm], o que pode esconder o provider de CUDA.
- A tolerância numérica entre a pose em lote e a pose um a um fica registrada no próprio teste. A tolerância que decide o PBI é a da paridade de docs/onprem.md:57.
- Story points e horas são sugestões.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável e vínculo com a Feature F5
- Marcar o PBI como condicional no Azure DevOps e mantê-lo fora da sprint até o resultado do critério 5 em F4.6 ou F5.4
- F2.2: aceitar pré-release por tag num commit de branch sem mover :latest
- Aprovação de custo dos jobs de remedição (P7)

## Preview — PBI F5.4 (novo) · Processar os três cultos públicos na t4-small e medir o critério 5 e as medidas de dimensionamento

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Processar os três cultos públicos na t4-small e medir o critério 5 e as medidas de dimensionamento |
| Tipo | Product Backlog Item |
| Pai | F5 |
| Tags | fase-0; criterio-5; hf-jobs; dimensionamento; PBI-103 |
| Estimativa | 5 pts (sugestão); tasks: 26 h |
| Dependências | F1.1, F1.2, F1.3, F2.2, F2.3, F2.4, F2.5, F2.6, F4.6, F5.1, F5.2, F2.8 |
| Substitui | PBI-103, TSK-207 |

#### Descrição

Como responsável pelo gate e pelo dimensionamento on-premises (Fabio Pinheiro)  
Quero os três cultos públicos processados na t4-small pela imagem com digest, com a transcrição ligada, e o tempo, o custo e o uso de GPU medidos  
Para obter o valor do critério 5 em T4 e preencher a tabela de dimensionamento de docs/onprem.md

**Contexto:** Nenhum job rodou no namespace ('hf jobs ps -a' sem resultados em 2026-09-23). A meta do critério 5 é até US$ 1,50 e até 2 h por hora de vídeo na t4-small (docs/poc-gate.md:13). A tabela de docs/onprem.md:9-14 pede segundos de GPU por hora de vídeo (detecção + expressão), a mediana de rostos mensuráveis por quadro, o pico de memória de GPU e o custo por culto, a partir do run_log (docs/onprem.md:7; PBI-103/TSK-207). O run_log não tem essas medidas: a etapa 'video' junta decodificação, detecção, expressão e pose (processar_culto.py:65,79,90,101; reacao/cost.py:15-25). A expressão do HSEmotion roda em CPU (hsemotion_onnx/facial_emotions.py:40, instalado), e o uso de CUDA pelo detector na T4 não foi verificado; F2.2 verifica. A imagem instala o pacote reacao no build (Dockerfile:9-11) e é publicada por tag v* ou por workflow_dispatch (.github/workflows/docker.yml:2-5), então os jobs só rodam o código de F5.2 e das medições novas depois de uma release. 'hf jobs stats' mostra CPU, memória e GPU (https://huggingface.co/docs/hub/jobs-manage#monitor-resource-usage). As fontes divergem sobre a cobrança: por minuto na documentação do Hub, por segundo em docs/hf-jobs.md:4 e em reacao/cost.py (P21). O timeout padrão é de 30 minutos, e o máximo não é documentado (https://huggingface.co/docs/hub/jobs-configuration#timeout). docs/hf-jobs.md:13 usa --timeout 3h. O prompt de momentos corta a transcrição em 60000 caracteres (reacao/moments.py:61). Um insight com momento 'desconhecido' é rejeitado pelo lint e não é gravado (reacao/lint.py:34-35; reacao/insights.py:54-59), mas o momento de cada evento é gravado (processar_culto.py:94-97).

**Regras de negócio:**
- RN01 – Os jobs rodam com 'hf jobs run <imagem>@<digest>' pela imagem da release de F5.4.T3, com o motor escolhido em F4.6 e a transcrição ligada.
- RN02 – Os vídeos são lidos do dataset por tag ou revisão (F3.5), nunca de caminho local (F1.1; P27).
- RN03 – O tempo e o custo por hora de vídeo seguem a fórmula pré-registrada em F1.3. O registro diz qual granularidade de cobrança vale e cita a fonte (P21).
- RN04 – Cada número da tabela de docs/onprem.md aponta o run_id e o id do job de origem.
- RN05 – Cada job pago tem aprovação prévia do dono da conta (P7).
- RN06 – Os segredos passam pelo nome, sem valor na linha de comando (https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets).
- RN07 – O resultado vai para o repositório de resultados (F2.8), e F6.1 leva o valor ao gate.
- RN08 – O critério 5 usa só execuções concluídas, salvo se a fórmula de F1.3 disser outra coisa.
- RN09 – A primeira linha da tabela de docs/onprem.md é o tempo de parede da detecção e da expressão com pose, com o dispositivo de cada etapa ao lado. O valor não é chamado de segundos de GPU enquanto alguma dessas etapas rodar em CPU (docs/onprem.md:11).

**Fora de escopo:**
- Expressão e pose na GPU (F5.3)
- Comparação de momentos (F5.5)
- Notas do critério 4 (F5.7)
- Execução no servidor local e paridade entre HF e servidor local (P3)
- Decisão sobre o corte de 60000 caracteres. Este PBI só mede o tamanho das transcrições
- Escrita do valor em docs/poc-gate.md (F6.1)

#### Critérios de aceite

- Há três execuções concluídas na t4-small, uma por culto de docs/corpus.csv, pela imagem da release de F5.4.T3. Cada uma tem, no registro de linhagem, o id do job, o run_id, o digest da imagem e a revisão do dataset.
- Para cada culto, o repositório de resultados tem o tempo e o custo por hora de vídeo pela fórmula de F1.3, com o veredito contra até US$ 1,50 e até 2 h por hora de vídeo.
- O registro do critério 5 diz se a cobrança é por minuto ou por segundo e cita a fonte.
- A tabela da seção 1 de docs/onprem.md tem os quatro valores preenchidos, cada um com o run_id de origem, e a primeira linha traz o dispositivo de cada etapa (detecção e expressão com pose).
- Para cada culto, o registro de resultados traz quantos caracteres tem a transcrição enviada ao prompt de momentos, se ela passa de 60000, o minuto em que o corte cai e quantos eventos ficaram com momento 'desconhecido' depois desse minuto.
- Um job que falhar ou estourar o timeout aparece no registro de resultados com a etapa e a mensagem.
- Nenhum job foi lançado com vídeo de caminho local ou com imagem sem digest.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F5.4.T1 | Visão Computacional | Separar o tempo das etapas, registrar o dispositivo de cada uma e a mediana de rostos mensuráveis por quadro | 6 | F1.5, F2.5, F2.8.T1 |
| F5.4.T2 | Data Science | Registrar em cada execução o tamanho da transcrição do prompt de momentos e os eventos sem momento depois do corte | 3 | F5.2, F2.5, F2.8.T1 |
| F5.4.T3 | DevOps | Publicar por tag de release a imagem com F5.2, F5.4.T1 e F5.4.T2 e registrar o digest | 2 | F5.4.T1, F5.4.T2, F2.2 |
| F5.4.T4 | DevOps | Lançar os três jobs na t4-small pela imagem da release, coletar 'hf jobs stats' durante cada job e registrar id do job e run_id | 6 | F5.4.T3, F2.8, F2.4.T4 (D7: decisão de Fabio sobre a exceção da P26), Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F5.4.T5 | Data Science | Calcular o critério 5 pela fórmula de F1.3 com a granularidade de cobrança registrada | 4 | F5.4.T4 |
| F5.4.T6 | MLOps | Preencher a tabela de dimensionamento de docs/onprem.md com a origem e o dispositivo de cada número | 2 | F5.4.T4, F5.4.T5 |
| F5.4.T7 | QA | Verificar os critérios de aceite de F5.4 | 3 | F5.4.T6 |

<details><summary>F5.4.T1 · [Visão Computacional] Separar o tempo das etapas, registrar o dispositivo de cada uma e a mediana de rostos mensuráveis por quadro</summary>

**Objetivo:** Fazer o registro de cada execução trazer o tempo e o dispositivo das etapas de detecção e de expressão com pose e a mediana de rostos mensuráveis por quadro.

**Passos previstos:**
1. Em processar_culto.py, marcar em separado a decodificação, o pré-filtro, a detecção plena e a expressão com pose, que hoje ficam juntas na etapa 'video' (linha 79).
2. Registrar o dispositivo efetivo de cada etapa (providers da sessão onnxruntime do detector e da expressão; torch.cuda na pose) no log e no registro de linhagem de F2.8.
3. Contar os rostos mensuráveis em cada quadro com plateia e calcular a mediana, sem guardar nada por rosto além da contagem.
4. Gravar os tempos em etapas (jsonb; supabase/migrations/0001_init.sql:18). Abrir issue (CONTRIBUTING.md:13) e criar migração com a coluna da mediana no run_log, atualizando o teste de contrato de F1.5.
5. Testar com o provider mock.

**Definição de pronto:** Uma execução local com mock grava as etapas separadas e a mediana em out/run_log.json, o log mostra o dispositivo de cada etapa, e os testes e o contrato passam.

**Dependências:** F1.5, F2.5, F2.8.T1

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F5.4.T2 · [Data Science] Registrar em cada execução o tamanho da transcrição do prompt de momentos e os eventos sem momento depois do corte</summary>

**Objetivo:** Saber, a partir do próprio job, se algum culto perde o fim da transcrição no prompt de momentos e quantos eventos ficam sem momento por isso.

**Passos previstos:**
1. Calcular, no processamento, o número de caracteres da transcrição montada como reacao/moments.py:53 monta e comparar com 60000 (reacao/moments.py:61).
2. Se passar do corte, calcular o minuto em que o corte cai e contar os eventos com momento 'desconhecido' que começam depois desse minuto (processar_culto.py:94-97). Esses eventos não viram insight, porque o lint rejeita momento 'desconhecido' (reacao/lint.py:34-35).
3. Gravar os valores no registro de linhagem de F2.8, ao lado de insights_rejeitados_pelo_lint do run_log.
4. Testar com segmentos sintéticos que somam mais de 60000 caracteres.

**Definição de pronto:** O teste com transcrição sintética longa passa no CI e mostra o tamanho, o minuto do corte e a contagem de eventos sem momento.

**Dependências:** F5.2, F2.5, F2.8.T1

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F5.4.T3 · [DevOps] Publicar por tag de release a imagem com F5.2, F5.4.T1 e F5.4.T2 e registrar o digest</summary>

**Objetivo:** Fazer os jobs de F5.4 rodarem o código de F5.2 e das medições novas por uma imagem com digest.

**Passos previstos:**
1. Conferir que F5.2, F5.4.T1 e F5.4.T2 estão mesclados em main.
2. Criar a tag de release e publicar a imagem pelo fluxo de F2.2 (.github/workflows/docker.yml:2-5).
3. Registrar o digest no registro de linhagem de F2.8 e na documentação dos jobs (docs/hf-jobs.md).

**Definição de pronto:** A imagem da release está publicada, o commit da tag contém F5.2, F5.4.T1 e F5.4.T2, e o digest está no registro de linhagem e em docs/hf-jobs.md.

**Dependências:** F5.4.T1, F5.4.T2, F2.2

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F5.4.T4 · [DevOps] Lançar os três jobs na t4-small pela imagem da release, coletar &#x27;hf jobs stats&#x27; durante cada job e registrar id do job e run_id</summary>

**Objetivo:** Processar os três cultos na t4-small com a configuração do gate, medir o uso de recursos durante cada job e deixar cada execução rastreável.

**Passos previstos:**
1. Confirmar o saldo de créditos na página de billing e a aprovação do dono (P7).
2. Ler em D7 do ADR 0002 (F2.4.T4) a decisão de Fabio sobre a exceção da P26 e passar ou não a ANTHROPIC_API_KEY pelo nome do secret, conforme essa decisão e F2.6.T2.
3. Montar o comando 'hf jobs run' com a imagem@digest de F5.4.T3, --flavor t4-small, o timeout confirmado em F2.2, os segredos pelo nome, labels de culto e motor, o vídeo por tag do dataset e o --provider do motor de F4.6.
4. Validar o comando com o lançador de F1.1 antes de submeter.
5. Rodar um job por culto e, enquanto 'hf jobs wait' acompanha o job, coletar CPU, memória e GPU com 'hf jobs stats' (https://huggingface.co/docs/hub/jobs-manage#monitor-resource-usage).
6. Guardar a série e o pico de memória de GPU no repositório de resultados de F2.8, junto com o conjunto do run_id e a linhagem, com o id do job e o run_id.
7. Registrar o id do job, o run_id e o estado de cada execução. Um job que falhar fica no registro de F2.5 com a etapa e a mensagem.

**Definição de pronto:** Os três jobs terminaram, 'hf jobs inspect' de cada um mostra o digest de F5.4.T3, e o id do job, o run_id, a série de 'hf jobs stats' e o pico de memória de GPU de cada um estão no repositório de resultados.

**Dependências:** F5.4.T3, F2.8, F2.4.T4 (D7: decisão de Fabio sobre a exceção da P26), Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F5.4.T5 · [Data Science] Calcular o critério 5 pela fórmula de F1.3 com a granularidade de cobrança registrada</summary>

**Objetivo:** Produzir o valor e o veredito do critério 5 em T4, com a origem de cada número.

**Passos previstos:**
1. Registrar se a cobrança vale por minuto ou por segundo, com a URL da documentação ou a página de billing (P21).
2. Aplicar a fórmula de F1.3 aos tempos de cada culto para obter o tempo e o custo por hora de vídeo.
3. Calcular o custo por culto e o tempo de parede de detecção e de expressão com pose por hora de vídeo, com o dispositivo de cada etapa.
4. Gravar no repositório de resultados os valores e o veredito contra até US$ 1,50 e até 2 h, com os run_id.

**Definição de pronto:** O arquivo de resultado do critério 5 tem os três cultos, o veredito, a granularidade de cobrança e a fonte.

**Dependências:** F5.4.T4

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F5.4.T6 · [MLOps] Preencher a tabela de dimensionamento de docs/onprem.md com a origem e o dispositivo de cada número</summary>

**Objetivo:** Fechar a tabela da seção 1 de docs/onprem.md com valores medidos e rastreáveis.

**Passos previstos:**
1. Preencher o tempo de parede de detecção e de expressão por hora de vídeo, com o dispositivo de cada etapa ao lado (docs/onprem.md:11), a mediana de rostos mensuráveis por quadro, o pico de memória de GPU e o custo por culto.
2. Indicar ao lado de cada valor o run_id e o id do job de origem.
3. Trocar em docs/onprem.md:7 a referência '(PBI-103/TSK-207)' por 'F5.4'. A relação com os IDs antigos fica no campo de IDs antigos do Azure DevOps.
4. Abrir PR citando F5.4.

**Definição de pronto:** O PR com a tabela preenchida, as origens e os dispositivos e sem 'PBI-103/TSK-207' em docs/onprem.md:7 foi mesclado.

**Dependências:** F5.4.T4, F5.4.T5

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F5.4.T7 · [QA] Verificar os critérios de aceite de F5.4</summary>

**Objetivo:** Dizer, para cada critério de aceite de F5.4, se passou ou não passou.

**Passos previstos:**
1. Conferir, no registro de linhagem, o id do job, o run_id, o digest e a revisão do dataset de cada culto.
2. Conferir com 'hf jobs inspect' que nenhum job usou caminho local nem imagem sem digest e que os três usaram o digest de F5.4.T3.
3. Conferir o arquivo do critério 5, a granularidade de cobrança e a fonte.
4. Conferir a tabela de docs/onprem.md, as origens e os dispositivos.
5. Conferir o registro do tamanho das transcrições e dos eventos sem momento, e o registro dos jobs que falharam, se houver.

**Definição de pronto:** O relatório de verificação, com passou ou não passou por critério, está anexado ao PBI.

**Dependências:** F5.4.T6

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- docs/poc-gate.md:13,42-44
- docs/onprem.md:6-14
- docs/hf-jobs.md:4,13
- Dockerfile:9-11
- .github/workflows/docker.yml:2-5
- reacao/cost.py:1-25
- reacao/moments.py:53,61
- reacao/lint.py:34-35
- reacao/insights.py:54-59
- processar_culto.py:65,79,90,94-97,101,103-107
- hsemotion_onnx/facial_emotions.py:40 (instalado, 0.3.1)
- https://huggingface.co/docs/hub/jobs-pricing
- https://huggingface.co/docs/hub/jobs-manage#monitor-resource-usage
- https://huggingface.co/docs/hub/jobs-configuration#timeout
- https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets
- premissas P7, P19, P21 e P27

#### Verificação INVEST: pontos que falharam
- I: o PBI depende de 11 PBIs e só entra numa sprint depois de todos.

#### Premissas
- A disciplina QA foi acrescentada porque todo PBI tem task de QA.
- O valor do critério 5 vai para o repositório de resultados. A escrita em docs/poc-gate.md fica com F6.1, para não repetir o trabalho de F6.1.
- Sem F5.3, a expressão roda em CPU (hsemotion_onnx/facial_emotions.py:40, instalado), e o uso de CUDA pelo detector na T4 é verificado em F2.2. Por isso, o tempo de parede das etapas de detecção e de expressão com pose é registrado como tempo da etapa, com o dispositivo efetivo de cada uma (providers da sessão onnxruntime e torch.cuda), e não como segundos de GPU. A utilização de GPU de 'hf jobs stats' fica ao lado.
- O dispositivo de cada etapa e a medida da transcrição vão para o registro de linhagem de F2.8, sem coluna nova. A mediana de rostos mensuráveis vai para uma coluna nova do run_log, porque docs/onprem.md:7 pede os números do run_log.
- A medida da transcrição é feita dentro do job de processamento, com os eventos ainda em memória, para não exigir outro job nem leitura da tabela event com a chave de serviço.
- A coleta de 'hf jobs stats' fica na task de lançamento, porque ela acontece durante o job.
- Se a exceção P26 não for aceita, os jobs rodam sem ANTHROPIC_API_KEY.
- O custo total dos três jobs não foi calculado, e cada job precisa de aprovação (P7).
- A lista de dependências segue a árvore, que inclui F2.3.
- Story points e horas são sugestões.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável e vínculo com a Feature F5
- Registrar no Azure DevOps a relação com os IDs antigos PBI-103 e TSK-207
- Confirmação do saldo de créditos na página de billing e aprovação do dono da conta (P7)
- Fórmula do critério 5 assinada em F1.3 e granularidade de cobrança (P21)

## Preview — PBI F5.5 (novo) · Comparar as fronteiras de momento com a marcação manual e registrar o critério 3

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Comparar as fronteiras de momento com a marcação manual e registrar o critério 3 |
| Tipo | Product Backlog Item |
| Pai | F5 |
| Tags | fase-0; criterio-3; momentos; avaliacao |
| Estimativa | 5 pts (sugestão); tasks: 18 h |
| Dependências | F1.3, F5.1, F5.4, F2.8 |
| Substitui | nenhum |

#### Descrição

Como responsável pelo gate da Fase 0 (Fabio Pinheiro)  
Quero comparar as fronteiras de momento geradas pelo pipeline com a marcação manual dos três cultos, com a segmentação por LLM e pela heurística  
Para obter o valor do critério 3 e saber se o LLM muda o resultado

**Contexto:** O critério 3 pede que pelo menos 80% das fronteiras de momento fiquem a até 60 s da marcação manual, em 3 vídeos pt-BR (docs/poc-gate.md:11). Nenhum código compara momentos detectados com rotulados. Só existe o validador de formato (tools/validar_labels.py:136-155). A segmentação tem dois caminhos: o LLM, quando há chave (reacao/moments.py:47-69), e a heurística por palavras-chave com histerese de 2 segmentos (reacao/moments.py:18-44). A transcrição e os agregados de cada culto ficam guardados (supabase/migrations/0001_init.sql:6-13), então dá para segmentar de novo sem processar o vídeo. A tabela moment não tem coluna de caminho nem de modelo (supabase/migrations/0001_init.sql:14). A imagem não copia tools/ hoje (Dockerfile:10); F5.1.T4 acrescenta essa cópia. O caminho com LLM depende da exceção P26.

**Regras de negócio:**
- RN01 – A regra de pareamento das fronteiras e o denominador são os pré-registrados em F1.3.
- RN02 – Uma fronteira conta como acerto se estiver a 60 s ou menos da marcação manual. Exatos 60 s contam como acerto (docs/poc-gate.md:11).
- RN03 – A comparação usa os arquivos de momentos por tag (F5.1) e os momentos de um run_id (F2.5).
- RN04 – Os dois caminhos são medidos sobre a mesma transcrição e os mesmos agregados do run_id de F5.4, sem processar o vídeo de novo. Os momentos segmentados de novo vão, como arquivo, para o repositório de resultados de F2.8, e não para a tabela moment do Supabase.
- RN05 – O caminho de cada conjunto de momentos vem do registro de F5.2. Momentos de uma execução em que o LLM falhou contam como heurística.
- RN06 – O caminho com LLM só é medido se a exceção P26 for aceita. Sem ela, o registro diz que só a heurística foi medida.
- RN07 – O job de comparação roda com 'hf jobs run <imagem>@<digest>' por uma imagem que contém os scripts de F5.5.T1 e F5.5.T2 (RN06 da Feature).

**Fora de escopo:**
- Ajuste do prompt ou da heurística para melhorar o número
- Troca do modelo de linguagem
- Notas do critério 4 (F5.7)
- Escrita do valor em docs/poc-gate.md (F6.1)

#### Critérios de aceite

- Para cada um dos três cultos, o arquivo de resultado traz a fração de fronteiras a até 60 s da marcação manual com a heurística, calculada pela regra de F1.3.
- Com a exceção P26 aceita, o mesmo arquivo traz a fração com o LLM e a diferença entre os dois caminhos. Sem ela, o arquivo registra que o caminho com LLM não foi medido.
- O arquivo traz, para cada conjunto de momentos, o run_id, a tag dos rótulos, o caminho, o id do modelo e a versão do prompt.
- Nos testes do comparador, uma fronteira a 60 s da marcação conta como acerto, e uma a 61 s não conta.
- Quando falta o arquivo de momentos de um vídeo ou o run_id não tem momentos, o comparador sai com código diferente de 0, diz o que falta e não grava valor.
- O valor total do critério 3 nos três vídeos está calculado pela regra de F1.3.
- Os dois conjuntos de momentos segmentados de novo estão, como arquivo, no repositório de resultados, e o script de nova segmentação não grava no Supabase.
- O job de comparação rodou com 'hf jobs run <imagem>@<digest>', e o digest está no arquivo de resultado.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F5.5.T1 | Data Science | Implementar o comparador de fronteiras de momento com a regra de F1.3 | 6 | F1.3 |
| F5.5.T2 | Machine Learning | Segmentar de novo os momentos de um run_id pelos dois caminhos e gravá-los como arquivo no repositório de resultados | 4 | F5.2, F2.8 |
| F5.5.T3 | Data Science | Rodar a comparação nos três cultos pela imagem com digest e registrar o critério 3 | 5 | F5.5.T1, F5.5.T2, F5.4, F2.4.T4 (D7: decisão de Fabio sobre a exceção da P26), Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F5.5.T4 | QA | Verificar os critérios de aceite de F5.5 | 3 | F5.5.T3 |

<details><summary>F5.5.T1 · [Data Science] Implementar o comparador de fronteiras de momento com a regra de F1.3</summary>

**Objetivo:** Ter um script testado que calcula a fração de fronteiras a até 60 s da marcação manual.

**Passos previstos:**
1. Escrever um script em tools/ que lê os momentos de um run_id e o _momentos.csv por tag, na pasta de momentos dos cultos de F5.1.
2. Extrair as fronteiras e parear pela regra de F1.3, com tolerância de 60 s inclusiva.
3. Sair com código diferente de 0 e mensagem quando faltar rótulo ou momentos do run_id, sem gravar valor.
4. Escrever testes com casos sintéticos: fronteira a 60 s conta, a 61 s não conta, fronteira sem par e os dois casos de erro.
5. Abrir PR citando F5.5.

**Definição de pronto:** Os testes do comparador passam no CI, e o PR foi mesclado.

**Dependências:** F1.3

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F5.5.T2 · [Machine Learning] Segmentar de novo os momentos de um run_id pelos dois caminhos e gravá-los como arquivo no repositório de resultados</summary>

**Objetivo:** Ter, para o mesmo run_id, um conjunto de momentos pela heurística e outro pelo LLM, sem processar o vídeo de novo e sem misturá-los aos momentos da execução.

**Passos previstos:**
1. Escrever em tools/ um script que lê a transcrição e os agregados do run_id, dentro do job, com a chave dos jobs.
2. Chamar a segmentação pela heurística e, se a exceção P26 estiver aceita em D7 do ADR 0002 (F2.4.T4), pelo LLM, registrando o caminho, o modelo e a versão do prompt de F5.2.
3. Gravar os dois conjuntos como arquivo no repositório de resultados de F2.8, com run_id, caminho, id do modelo e versão do prompt, sem gravar na tabela moment do Supabase.
4. Testar com o cliente simulado de F5.2.

**Definição de pronto:** O script e os testes com cliente simulado passam no CI, e o script não chama o Store.

**Dependências:** F5.2, F2.8

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F5.5.T3 · [Data Science] Rodar a comparação nos três cultos pela imagem com digest e registrar o critério 3</summary>

**Objetivo:** Produzir o valor do critério 3 por vídeo e no total, por caminho.

**Passos previstos:**
1. Publicar por tag de release a imagem com os scripts de F5.5.T1 e F5.5.T2 pelo fluxo de F2.2 (tools/ já está na imagem desde F5.1.T4) e registrar o digest.
2. Pedir ao dono da conta a aprovação de custo de um job cpu-basic (P7).
3. Ler em D7 do ADR 0002 (F2.4.T4) a decisão sobre a exceção da P26: sem ela, rodar só o caminho da heurística e registrar que o caminho do LLM não foi medido.
4. Rodar, com 'hf jobs run <imagem>@<digest>' e comando explícito, com a chave dos jobs pelo nome, F5.5.T2 e F5.5.T1 para os três run_id de F5.4.
5. Calcular o valor por vídeo e o total pela regra de F1.3, em cada caminho, e a diferença entre os caminhos.
6. Gravar no repositório de resultados o valor, o run_id, a tag dos rótulos, o caminho, o modelo, a versão do prompt e o digest da imagem.

**Definição de pronto:** O arquivo de resultado do critério 3, com o digest da imagem, está no repositório de resultados, pronto para F6.1.

**Dependências:** F5.5.T1, F5.5.T2, F5.4, F2.4.T4 (D7: decisão de Fabio sobre a exceção da P26), Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F5.5.T4 · [QA] Verificar os critérios de aceite de F5.5</summary>

**Objetivo:** Dizer, para cada critério de aceite de F5.5, se passou ou não passou.

**Passos previstos:**
1. Conferir no arquivo de resultado os três vídeos, os caminhos medidos e a diferença.
2. Conferir, em cada conjunto, o run_id, a tag, o caminho, o modelo e a versão do prompt.
3. Rodar os testes de 60 s e de 61 s.
4. Rodar o comparador sem o arquivo de momentos e com um run_id sem momentos e registrar o código de saída.
5. Conferir no repositório de resultados os dois arquivos de momentos segmentados de novo e, no código de F5.5.T2, que não há gravação no Supabase.
6. Conferir com 'hf jobs inspect' o digest do job de comparação.

**Definição de pronto:** O relatório de verificação, com passou ou não passou por critério, está anexado ao PBI.

**Dependências:** F5.5.T3

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- docs/poc-gate.md:11
- labels/README.md:16-17
- reacao/moments.py:18-69
- tools/validar_labels.py:136-155
- supabase/migrations/0001_init.sql:6-14
- Dockerfile:10
- premissa P26

#### Verificação INVEST: pontos que falharam
- I: depende de F5.4, que tem 11 dependências.

#### Premissas
- Backend saiu das disciplinas previstas na árvore. O comparador em tools/ calcula a métrica do critério 3, que é trabalho de Data Science pela regra das tasks, e o PBI não altera código do pipeline, schema nem API. F5.5.T1 passou para Data Science.
- A nova segmentação roda em job cpu-basic no HF, com a chave dos jobs, e precisa de aprovação de custo (P7).
- F5.2 chega por F5.4, que depende dele, e fornece o registro de caminho, modelo e versão do prompt.
- Story points e horas são sugestões.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável e vínculo com a Feature F5
- Regra de pareamento e denominador assinados em F1.3
- Fabio confirma a exceção P26

## Preview — PBI F5.6 (novo) · Dar a Fabio e ao pastor Filipe acesso ao painel web na Vercel, com Supabase Auth e RLS, e listar o primeiro culto público processado

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Dar a Fabio e ao pastor Filipe acesso ao painel web na Vercel, com Supabase Auth e RLS, e listar o primeiro culto público processado |
| Tipo | Product Backlog Item |
| Pai | F5 |
| Tags | fase-0; criterio-4; painel-vercel; supabase-auth; rls; front-end |
| Estimativa | 8 pts (sugestão); tasks: 42 h |
| Dependências | F1.1, F1.7, F2.2, F2.3, F2.4 (inclusive a decisão D7 de F2.4.T4), F2.5, F2.6, F5.1, F5.2, F2.8 |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro e o pastor Filipe  
Quero entrar com a própria conta num painel web e ver a lista das execuções liberadas, com o culto e o motor de cada uma  
Para ter acesso restrito aos relatórios dos cultos públicos antes da escolha do motor e da decisão do gate

**Contexto:** Não há front end no repositório (git ls-files, 2026-09-23). O CI instala e testa só o código Python: uv, ruff, pytest, o pipeline com o motor mock e a busca por modelo de reconhecimento (.github/workflows/ci.yml:8-17), e o .gitignore não tem entrada para dependências de Node (.gitignore, 2026-09-23). O time 'Fabio Pinheiro's projects' da Vercel (team_TFJpulVK8Dcufy5SIecwChUh) tem só o projeto ai-guitar-coach-pilot, sem relação com este sistema (Vercel list_teams e list_projects, 2026-09-23). Pela P3 revisada, o painel fica num projeto novo nesse time, lê do Supabase agregados, eventos e insights, com Supabase Auth, RLS e chave pública, e não recebe vídeo, quadro, recorte nem observação por rosto. A Vercel escolhe o gerenciador de pacotes pelo lockfile (https://vercel.com/docs/package-managers). Com Root Directory definido, o app não acessa arquivos fora desse diretório (https://vercel.com/docs/builds/configure-a-build#root-directory). Um projeto novo ligado a um repositório usa main como branch de produção quando ela existe (https://vercel.com/docs/git#production-branch). Num repositório público, um PR vindo de fork só ganha deployment com autorização de um membro do time, e essa proteção pode ser desligada nas configurações do projeto (https://vercel.com/docs/git#deploying-forks-of-public-git-repositories; https://vercel.com/docs/git/vercel-for-github). F2.6 habilita RLS nas 8 tabelas sem política de leitura anônima. Com RLS ligada e sem política, a chave pública não lê nada. Num projeto existente, uma tabela nova em public nasce com select, insert, update e delete concedidos a anon e a authenticated, e acrescentar política não retira esses grants (https://supabase.com/docs/guides/database/postgres/row-level-security, seção Grants and policies). A chave pública pode ficar no navegador quando a RLS está ligada; a chave secreta e a service_role ignoram a RLS e não vão ao navegador, e a service_role legada é um JWT (https://supabase.com/docs/guides/getting-started/api-keys). O Store grava com SUPABASE_SERVICE_KEY (reacao/store.py:11-12,24-25). O motor só existe em run_log.provider; window_aggregate, moment, event e insight não têm essa coluna (supabase/migrations/0001_init.sql:6-18). As tabelas se ligam só pelo texto do culto, e o Store grava sem upsert (reacao/store.py:24-26), por isso o painel precisa do run_id de F2.5. O repositório GitHub é público (GitHub API, ds-fabiopinheiro/church-sentiment-analysis, visibility=public, 2026-09-23). Na árvore, o local do vínculo entre conta e papel ficava para F6.2, que depende de F6.1 (arvore_v1.json, F6.2 e F7.2).

**Regras de negócio:**
- RN01 – O painel lê do Supabase agregados por janela, eventos e insights (P3 revisada), a tabela de execuções liberadas (listada em D7 de F2.4.T4) e, se o usuário confirmar a pendência registrada em D7, momentos, com a chave pública e a sessão do usuário do Supabase Auth. Ele não lê transcript_segment, run_log, service nem insight_feedback (esta até F5.7).
- RN02 – A chave secreta ou de serviço do Supabase não entra no projeto da Vercel nem no código do painel. Ela fica só nos jobs do HF (P3 revisada).
- RN03 – A Vercel não recebe vídeo, quadro, recorte de rosto nem observação por rosto (P3 revisada).
- RN04 – Só entram contas convidadas: Fabio, o pastor Filipe e duas contas de teste da QA, uma com o papel de avaliador e código de teste e outra sem papel. O cadastro aberto fica desligado. As contas de teste são apagadas ao fim de F5.7.
- RN05 – O papel de avaliador do gate fica no local decidido em D7 de F2.4.T4, hoje proposto em app_metadata do Supabase Auth, campo que o usuário não altera, e as políticas de RLS exigem esse papel (https://supabase.com/docs/guides/database/postgres/row-level-security). O papel é gravado pelo SQL Editor, com a conta dona do projeto Supabase, e nunca pela API admin, que exige a chave secreta.
- RN06 – Uma execução só aparece no painel se estiver na tabela de execuções liberadas (culto, run_id, motor e origem). A liberação é uma migração versionada que cita o culto e o run_id por extenso e copia o motor de run_log.provider, aplicada pelo dono do projeto Supabase, sem a chave de serviço.
- RN07 – Antes da decisão do gate, só são liberados cultos da coluna video de docs/corpus.csv (P10), e um teste do CI falha se uma migração de liberação citar outro culto.
- RN08 – Nas tabelas lidas pelo painel e na de execuções liberadas, anon e authenticated não têm grant de insert, update nem delete. authenticated tem só select, filtrado pela política do avaliador.
- RN09 – Os textos fixos do painel passam pelo lint no CI (CLAUDE.md, regra 4).
- RN10 – A primeira execução liberada vem de um job com 'hf jobs run <imagem>@<digest>', com o motor padrão hsemotion e os pesos de F2.3 (P10; P3 revisada).
- RN11 – O código do painel fica num diretório próprio do repositório, com as dependências fixadas num lockfile e só as necessárias (CLAUDE.md:30), e passa por lint, testes e build no CI antes do merge.
- RN12 – O projeto do painel na Vercel só é criado depois que Fabio confirma o plano e os termos de uso da Vercel para este projeto, registrados em D8 do ADR 0002 (F5.6.T9).

**Fora de escopo:**
- Tela do relatório com momentos, janelas e insights (F5.8)
- Notas dos insights (F5.7)
- Perfis pastor, mídia e DPO e revisão antes de liberar ao pastor (F7.2 e F7.3)
- Sinalização de qualidade por culto (F7.6)
- Vídeo ou resultado da PIB (P10)
- Ferramenta de rotulagem, que fica em Space privado no HF (F3.3)
- Envio do vídeo do piloto (F7.1)
- Exibição da transcrição completa
- Relatório em PDF ou por e-mail

#### Critérios de aceite

- Fabio e o pastor Filipe entram no painel com as próprias contas, acompanhados pela QA, e veem a lista de execuções liberadas, com o culto, o motor e o identificador da execução, incluindo o culto público processado neste PBI.
- Um e-mail fora da lista não consegue criar conta nem entrar.
- A conta de teste sem papel e um visitante anônimo com a chave pública não recebem nenhuma linha em consulta direta à API do Supabase, em nenhuma tabela.
- Com a sessão da conta de teste avaliadora, uma consulta direta a transcript_segment, run_log, service ou insight_feedback não retorna linhas.
- Com a chave pública, sem sessão ou com a sessão de qualquer conta de teste, insert, update e delete em window_aggregate, moment, event, insight e na tabela de execuções liberadas são recusados.
- Uma execução que não está na tabela de execuções liberadas não aparece no painel nem numa consulta direta com a sessão da conta de teste avaliadora.
- Todo culto da tabela de execuções liberadas está na coluna video de docs/corpus.csv, e o teste do CI falha quando uma migração de liberação cita um culto fora desse arquivo.
- O projeto na Vercel publica a partir do diretório do painel, com main como branch de produção e a Git Fork Protection ligada. As variáveis do projeto têm só a URL e a chave pública (sb_publishable_) do Supabase, além da variável que desliga a Vercel Toolbar em preview, e estão registradas no inventário de credenciais de F2.6.T6. Os arquivos gerados pelo build não contêm o prefixo sb_secret_ nem JWT com role service_role.
- A execução liberada tem o id do job, o run_id e o digest da imagem registrados, e o registro de linhagem de F2.8 mostra os pesos de F2.3.
- O diretório do painel tem lockfile versionado. Em cada PR, o CI instala o painel pelo lockfile e roda lint, testes e build, e falha quando o build do painel quebra ou quando um texto fixo do painel tem termo proibido pelo lint.
- Antes da criação do projeto na Vercel, D8 do ADR 0002 registra o plano do time 'Fabio Pinheiro's projects', a decisão de Fabio sobre os termos de uso da Vercel para este projeto, com data, e a retenção de logs do plano.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F5.6.T1 | Front end | Criar o diretório do painel com o framework do ADR de F2.4, o lockfile e os comandos de lint, teste e build | 4 | F2.4 |
| F5.6.T2 | DevOps | Criar o projeto do painel na Vercel ligado ao diretório do painel, com só a URL e a chave pública do Supabase, e o passo de CI do front end | 5 | F5.6.T9, F5.6.T1, F2.4, F2.6 |
| F5.6.T3 | DevOps | Configurar o Supabase Auth com cadastro fechado, convidar Fabio e Filipe, criar as contas de teste e gravar os papéis no local decidido em D7 | 4 | F5.6.T2, F2.4.T4 |
| F5.6.T4 | Backend | Criar a tabela de execuções liberadas e as políticas de RLS e os grants do avaliador do gate | 8 | F2.5, F2.6, F2.6.T4 (job de CI com Supabase local e migrações; pendência) |
| F5.6.T5 | Backend | Submeter os textos fixos do painel ao lint no CI | 3 | F1.7, F5.6.T1 |
| F5.6.T6 | Front end | Implementar o login e a lista de execuções liberadas no painel | 4 | F5.6.T1, F5.6.T2, F5.6.T3, F5.6.T4, F5.6.T5 |
| F5.6.T7 | DevOps | Publicar a imagem com F5.2, processar um culto público com o motor padrão e liberá-lo no painel por migração | 5 | F5.6.T4, F1.1, F2.2, F2.3, F5.1, F5.2, F2.8, F2.4.T4 (D7: decisão de Fabio sobre a exceção da P26), Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F5.6.T8 | QA | Verificar os critérios de aceite de F5.6, incluindo os acessos negados e o CI do painel | 7 | F5.6.T6, F5.6.T7 |
| F5.6.T9 | Governança e Privacidade | Confirmar com Fabio o plano e os termos de uso da Vercel para o projeto do painel, antes de criar o projeto | 2 | F2.4.T7 (ADR 0002 mesclado, com a pendência D8 de F2.4.T4) |

<details><summary>F5.6.T1 · [Front end] Criar o diretório do painel com o framework do ADR de F2.4, o lockfile e os comandos de lint, teste e build</summary>

**Objetivo:** Ter no repositório um diretório do painel que instala pelo lockfile e passa em lint, testes e build, para o projeto na Vercel e o CI apontarem para ele.

**Passos previstos:**
1. Criar o diretório do painel no repositório com o framework decidido no ADR de F2.4.
2. Escolher o gerenciador de pacotes e a versão do Node e registrá-los: o lockfile versionado define o gerenciador que a Vercel usa (https://vercel.com/docs/package-managers), e o campo engines.node do package.json define a versão do Node, acima da configuração do projeto (https://vercel.com/docs/functions/runtimes/node-js/node-js-versions).
3. Acrescentar só as dependências necessárias (o cliente do Supabase, a ferramenta de lint e o executor de testes), com versões fixadas no lockfile, e registrar no README do painel por que cada uma é necessária (CLAUDE.md:30).
4. Definir no package.json os comandos de lint, teste e build e criar uma página inicial sem dado que passa no build.
5. Criar no diretório do painel o arquivo versionado de textos fixos, que o painel lê e F5.6.T5 passa pelo lint.
6. Não referenciar arquivo fora do diretório do painel, porque o app não acessa arquivos fora do Root Directory (https://vercel.com/docs/builds/configure-a-build#root-directory).
7. Acrescentar ao .gitignore a pasta de dependências e a de build do painel, que hoje não têm entrada, e abrir PR citando F5.6.

**Definição de pronto:** O PR foi mesclado, e numa cópia limpa do repositório a instalação pelo lockfile, o lint, os testes e o build do diretório do painel terminam sem erro.

**Dependências:** F2.4

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F5.6.T2 · [DevOps] Criar o projeto do painel na Vercel ligado ao diretório do painel, com só a URL e a chave pública do Supabase, e o passo de CI do front end</summary>

**Objetivo:** Ter um projeto novo no time 'Fabio Pinheiro's projects', separado de ai-guitar-coach-pilot, que publica o painel a partir do diretório do painel e da branch main e só conhece a URL e a chave pública do Supabase, e um CI que roda lint, testes e build do painel em cada PR.

**Passos previstos:**
1. Criar o projeto no time team_TFJpulVK8Dcufy5SIecwChUh ligado ao repositório ds-fabiopinheiro/church-sentiment-analysis, com Root Directory no diretório de F5.6.T1 (https://vercel.com/docs/builds/configure-a-build#root-directory) e main como branch de produção (https://vercel.com/docs/git#production-branch).
2. Manter ligada a Git Fork Protection, para que um PR vindo de fork do repositório público só ganhe deployment com autorização de um membro do time (https://vercel.com/docs/git#deploying-forks-of-public-git-repositories).
3. Cadastrar para produção e preview a URL do projeto Supabase de desenvolvimento e a chave pública (sb_publishable_), sem nenhuma chave secreta ou service_role.
4. Cadastrar VERCEL_PREVIEW_FEEDBACK_ENABLED=0 nas variáveis de preview, para que a Vercel Toolbar, que carrega recursos de vercel.live, não entre nas páginas de preview (https://vercel.com/docs/vercel-toolbar/managing-toolbar).
5. Aplicar a proteção de deployment decidida no ADR de F2.4.
6. Acrescentar ao CI um job para o diretório do painel que instala pelo lockfile e roda lint, testes e build, nos mesmos eventos do job Python (push e pull_request; .github/workflows/ci.yml:2).
7. Registrar no inventário de credenciais de F2.6.T6 as variáveis do projeto: a URL e a chave pública do Supabase, e nenhuma outra credencial.
8. Registrar o id do projeto e o domínio de produção na documentação do painel.

**Definição de pronto:** 'vercel env ls' do projeto lista só a URL e a chave pública do Supabase e a variável da toolbar; as configurações do projeto mostram o Root Directory do painel, main como branch de produção e a Git Fork Protection ligada; o job do painel passa no CI de um PR; o inventário de F2.6.T6 lista as variáveis; e o id do projeto e o domínio de produção estão na documentação do painel.

**Dependências:** F5.6.T9, F5.6.T1, F2.4, F2.6

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F5.6.T3 · [DevOps] Configurar o Supabase Auth com cadastro fechado, convidar Fabio e Filipe, criar as contas de teste e gravar os papéis no local decidido em D7</summary>

**Objetivo:** Fazer com que só as contas convidadas entrem, com o papel de avaliador do gate e um código sem nome nas contas avaliadoras, gravados no local decidido em D7 de F2.4.T4.

**Passos previstos:**
1. Desligar o cadastro aberto no projeto de desenvolvimento ou bloquear a criação de usuário fora da lista com o hook Before User Created (https://supabase.com/docs/guides/auth/auth-hooks/before-user-created-hook).
2. Cadastrar o domínio do painel como Site URL e nas URLs de redirecionamento.
3. Convidar os e-mails de Fabio e de Filipe pelo método de login do ADR de F2.4.
4. Criar duas contas de teste para a QA: uma avaliadora, com código de teste, e outra sem papel.
5. Gravar, com a conta dona do projeto Supabase e pelo SQL Editor, em auth.users.raw_app_meta_data de Fabio, de Filipe e da conta de teste avaliadora, o papel de avaliador do gate e um código de avaliador sem nome (P12), conforme a decisão D7 de F2.4.T4. Não usar a API admin, que exige a chave secreta. Confirmar depois de novo login que auth.jwt() -> 'app_metadata' traz o papel.
6. Registrar os códigos de avaliador, sem os e-mails, e a remoção prevista das contas de teste ao fim de F5.7 na documentação do painel.

**Definição de pronto:** As quatro contas entram, um e-mail fora da lista recebe erro ao tentar criar conta, o JWT das três contas avaliadoras traz o papel e o código em app_metadata, e o da conta sem papel não traz.

**Dependências:** F5.6.T2, F2.4.T4

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F5.6.T4 · [Backend] Criar a tabela de execuções liberadas e as políticas de RLS e os grants do avaliador do gate</summary>

**Objetivo:** Fazer o banco entregar ao avaliador só agregados, eventos, insights e, se confirmado, momentos das execuções liberadas, recusar escrita de qualquer cliente e não entregar nada a quem não tem o papel.

**Passos previstos:**
1. Abrir uma issue antes de mexer no schema (CONTRIBUTING.md:13).
2. Criar uma migração com a tabela de execuções liberadas (culto, run_id, motor, origem e data da liberação, sem campo por pessoa), com enable row level security, revoke all de anon e authenticated, grant select a authenticated e política SELECT que exige o papel em auth.jwt() -> 'app_metadata'.
3. Na mesma migração, em window_aggregate, event, insight e, se o usuário confirmar a pendência de moment registrada em D7 de F2.4.T4, moment: revoke all de anon e authenticated, grant select a authenticated e política SELECT que exige o papel e o par culto e run_id na tabela de execuções liberadas.
4. Em transcript_segment, run_log, service e insight_feedback: revoke all de anon e authenticated, sem política. Se usar view, criá-la com security_invoker = true.
5. Escrever testes das políticas com pgTAP, rodados por 'supabase test db' (https://supabase.com/docs/guides/database/postgres/row-level-security), com dados sintéticos que incluem uma execução não liberada: select, insert, update e delete em todas as tabelas com sessão de avaliador, sessão sem papel e anônimo.
6. Fazer os testes pgTAP rodarem no job de CI com Supabase local de F2.6.T4, que aplica as migrações em cada PR, e conferir que o job falha com uma política removida num PR de teste.
7. Escrever um teste em pytest que lê as migrações de liberação e falha se alguma citar culto fora da coluna video de docs/corpus.csv.
8. Conferir que tests/test_schema.py passa.

**Definição de pronto:** A migração está aplicada no projeto de desenvolvimento pelo dono do projeto Supabase, os testes das políticas passam no job de CI com Supabase local, o teste de liberação passa, e o test_schema está verde.

**Dependências:** F2.5, F2.6, F2.6.T4 (job de CI com Supabase local e migrações; pendência)

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F5.6.T5 · [Backend] Submeter os textos fixos do painel ao lint no CI</summary>

**Objetivo:** Fazer todo texto fixo do painel passar pelo mesmo vocabulário proibido do lint.

**Passos previstos:**
1. Acrescentar em reacao/lint.py uma verificação de texto livre que aplica PROIBIDO e PROIBIDO_INDIVIDUAL (reacao/lint.py:8-13), sem as exigências próprias de insight.
2. Escrever um teste em pytest que passa pela verificação todos os textos do arquivo de textos fixos criado em F5.6.T1. O CI já roda pytest (.github/workflows/ci.yml:11).
3. Escrever um teste negativo com um termo proibido.

**Definição de pronto:** O CI está verde com os textos atuais, e o teste negativo falha como esperado.

**Dependências:** F1.7, F5.6.T1

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F5.6.T6 · [Front end] Implementar o login e a lista de execuções liberadas no painel</summary>

**Objetivo:** Permitir que o avaliador entre e veja as execuções que o banco libera para ele, com culto e motor.

**Passos previstos:**
1. Implementar no diretório de F5.6.T1 o login pelo Supabase Auth com a chave pública e a sessão do usuário, pelo método do ADR de F2.4.
2. Listar as execuções que a API devolve ao avaliador, com culto, motor, identificador da execução e data da liberação, sem filtro no cliente no lugar da RLS.
3. Mostrar mensagem de acesso negado quando a conta não tiver papel ou a sessão expirar.
4. Colocar os textos fixos no arquivo de textos de F5.6.T1.

**Definição de pronto:** Num deploy de preview, a conta de teste avaliadora vê a lista de execuções, e a conta de teste sem papel vê a mensagem de acesso negado.

**Dependências:** F5.6.T1, F5.6.T2, F5.6.T3, F5.6.T4, F5.6.T5

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F5.6.T7 · [DevOps] Publicar a imagem com F5.2, processar um culto público com o motor padrão e liberá-lo no painel por migração</summary>

**Objetivo:** Ter no Supabase de desenvolvimento uma execução liberada de um culto público, para a primeira leitura de Fabio e Filipe, sem usar a chave de serviço fora do job.

**Passos previstos:**
1. Se ainda não houver release com o código de F5.2, publicar a imagem por tag de release pelo fluxo de F2.2 e registrar o digest.
2. Pedir ao dono da conta a aprovação de custo (P7).
3. Ler em D7 do ADR 0002 (F2.4.T4) a decisão de Fabio sobre a exceção da P26: se aceita, passar a ANTHROPIC_API_KEY pelo nome do secret, como documentado em F2.6.T2; se não aceita, lançar sem a chave e registrar que momentos e insights vieram da heurística.
4. Rodar 'hf jobs run <imagem>@<digest>' com --flavor t4-small, --provider hsemotion, o timeout confirmado em F2.2, os segredos pelo nome, o vídeo por tag de F5.1, o --culto igual à coluna video de docs/corpus.csv e os pesos de F2.3, validando o comando com o lançador de F1.1.
5. Registrar o id do job e o run_id e conferir, no registro de linhagem de F2.8, o digest e o hash dos pesos.
6. Abrir PR com a migração de liberação, que cita o culto e o run_id por extenso e copia o motor de run_log.provider. Depois do merge, o dono do projeto Supabase aplica a migração.

**Definição de pronto:** As linhas do run_id estão no Supabase de desenvolvimento, a migração de liberação foi mesclada e aplicada, e o id do job, o run_id e o digest estão registrados.

**Dependências:** F5.6.T4, F1.1, F2.2, F2.3, F5.1, F5.2, F2.8, F2.4.T4 (D7: decisão de Fabio sobre a exceção da P26), Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F5.6.T8 · [QA] Verificar os critérios de aceite de F5.6, incluindo os acessos negados e o CI do painel</summary>

**Objetivo:** Dizer, para cada critério de aceite de F5.6, se passou ou não passou, usando só sessões de usuário e a chave pública.

**Passos previstos:**
1. Acompanhar Fabio e Filipe entrando com as próprias contas e conferir a lista de execuções (critério 1).
2. Tentar criar conta com um e-mail fora da lista.
3. Com a chave pública, sem sessão e com as sessões das contas de teste, fazer consultas diretas à API do Supabase: nenhuma linha para anônimo e para a conta sem papel; nenhuma linha em transcript_segment, run_log, service e insight_feedback para a avaliadora; recusa de insert, update e delete em todas as tabelas.
4. Conferir que as linhas do culto de fumaça gravado por F2.6 com a fixture sintética, fora da lista de liberadas, não aparecem para a conta de teste avaliadora, e conferir o resultado dos testes pgTAP de F5.6.T4 no job de CI com Supabase local. Se essas linhas não existirem no projeto, registrar que o critério ficou coberto só pelos testes pgTAP.
5. Comparar a tabela de execuções liberadas, lida com a conta de teste avaliadora, com a coluna video de docs/corpus.csv, e conferir o teste de liberação no CI.
6. Conferir nas configurações do projeto na Vercel o Root Directory, main como branch de produção e a Git Fork Protection ligada, as variáveis com 'vercel env ls' e o registro delas no inventário de F2.6.T6. Nos arquivos do build, procurar o prefixo sb_secret_ e decodificar as cadeias que começam com eyJ para conferir que nenhuma tem role service_role, sem usar o valor de nenhuma chave (https://supabase.com/docs/guides/getting-started/api-keys).
7. Conferir no CI de um PR o job do painel (instalação pelo lockfile, lint, testes e build) e, num PR de teste, que um build quebrado e um texto fixo com termo proibido fazem o CI falhar.
8. Conferir em D8 do ADR 0002 o registro de F5.6.T9 (plano, decisão de Fabio com data e retenção de logs) e que a data é anterior à criação do projeto na Vercel.
9. Conferir o registro do job de F5.6.T7.

**Definição de pronto:** O relatório de verificação, com passou ou não passou por critério, está anexado ao PBI.

**Dependências:** F5.6.T6, F5.6.T7

**Estimativa sugerida:** 7 h (sugestão; validar com o time)

</details>

<details><summary>F5.6.T9 · [Governança e Privacidade] Confirmar com Fabio o plano e os termos de uso da Vercel para o projeto do painel, antes de criar o projeto</summary>

**Objetivo:** Fechar, antes de F5.6.T2, a pendência D8 do ADR 0002: plano do time 'Fabio Pinheiro's projects', decisão de Fabio sobre os termos de uso da Vercel para este projeto na Fase 0 e retenção de logs do plano.

**Passos previstos:**
1. Ler a pendência D8 registrada em F2.4.T4 no ADR 0002.
2. Com Fabio, que tem acesso à cobrança do time, ler o plano atual do time team_TFJpulVK8Dcufy5SIecwChUh na página de billing da Vercel.
3. Apresentar a Fabio a regra de uso dos times Hobby (só uso pessoal não comercial) e a definição de uso comercial, que inclui quem é pago para escrever o código (https://vercel.com/docs/limits/fair-use-guidelines, seção Commercial usage), junto com README.pt-BR.md:48 (projeto voluntário).
4. Registrar, para o plano escolhido, a retenção dos runtime logs (https://vercel.com/docs/logs/runtime) e o limite de usuários externos da Vercel Authentication (https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/vercel-authentication), que F6.2, F6.3.T1 e F7.4.T1 usam.
5. Registrar a decisão de Fabio, com data, em D8 do ADR 0002, por PR citando F5.6. Se Fabio decidir mudar de plano, a compra é dele; esta task não compra nem cria recurso.

**Definição de pronto:** D8 do ADR 0002 traz o plano do time, a decisão de Fabio sobre os termos de uso com data e a retenção de logs do plano, em PR mesclado antes do início de F5.6.T2.

**Dependências:** F2.4.T7 (ADR 0002 mesclado, com a pendência D8 de F2.4.T4)

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- reacao/store.py:10-26
- supabase/migrations/0001_init.sql:3-21
- reacao/lint.py:8-13
- .github/workflows/ci.yml:1-17
- .gitignore (sem entrada para node_modules, 2026-09-23)
- CLAUDE.md:21 (regra 6), CLAUDE.md:30 (sem frameworks além do necessário) e regras 3 e 4
- tests/test_schema.py:9
- CONTRIBUTING.md:13
- git ls-files (2026-09-23)
- GitHub API, ds-fabiopinheiro/church-sentiment-analysis, visibility=public (2026-09-23)
- Vercel list_teams e list_projects(teamId=team_TFJpulVK8Dcufy5SIecwChUh), 2026-09-23
- arvore_v1.json: F6.2 e F7.2 (vínculo entre conta e papel decidido em F6.2)
- https://vercel.com/docs/builds/configure-a-build#root-directory
- https://vercel.com/docs/git#production-branch
- https://vercel.com/docs/git#deploying-forks-of-public-git-repositories
- https://vercel.com/docs/git/vercel-for-github
- https://vercel.com/docs/package-managers
- https://vercel.com/docs/functions/runtimes/node-js/node-js-versions
- https://vercel.com/docs/environment-variables/sensitive-environment-variables
- https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/vercel-authentication
- https://vercel.com/docs/limits/fair-use-guidelines
- https://vercel.com/docs/vercel-toolbar/managing-toolbar
- https://supabase.com/docs/guides/database/postgres/row-level-security
- https://supabase.com/docs/guides/database/secure-data
- https://supabase.com/docs/guides/getting-started/api-keys
- https://supabase.com/docs/guides/auth/auth-hooks/before-user-created-hook
- https://supabase.com/docs/guides/auth/managing-user-data
- https://supabase.com/docs/guides/auth/signout
- https://supabase.com/docs/guides/auth/sessions
- https://supabase.com/docs/guides/platform/migrating-to-supabase/auth0
- sixdrepnet/regressor.py:35 (instalado, 0.1.6)
- premissas P3 revisada, P10 e P12
- https://vercel.com/docs/logs/runtime
- README.pt-BR.md:48

#### Verificação INVEST: pontos que falharam
- I: depende de 10 PBIs, entre eles F2.4, que precisa ser revisto pela P3 revisada e registrar a decisão D7 antes de F5.6 ficar pronto para a sprint, F2.3 e F2.8.
- S: 9 tasks e cerca de 42 h sugeridas, duas tasks acima do limite de 7 (taskflow.md:40). Se não couber na sprint, o processamento do culto (F5.6.T7) pode ir para F5.8, e a lista de execuções fica verificada só pelos testes das políticas.

#### Premissas
- O antigo F5.6 foi dividido. Este PBI entrega o acesso, a lista de execuções liberadas e o primeiro culto processado; a tela do relatório foi para F5.8 (taskflow.md, seção 1: critérios acima de ~10 cobrindo assuntos diferentes).
- F2.5 entrou como dependência porque, sem run_id, o relatório do hsemotion deste PBI e o do motor escolhido em F5.4 se misturam no mesmo culto.
- F2.3 entrou como dependência porque o job de F5.6.T7 processa um culto inteiro e a P3 revisada põe os pesos em repositórios de modelo privados. Sem F2.3, o job baixaria pesos de terceiros sem revisão fixa (sixdrepnet/regressor.py:35, instalado; insightface/utils/storage.py:10, instalado), e o hash dos pesos ficaria fora da linhagem de F2.8.
- A política de leitura do avaliador do gate entra aqui, e não em F7.2. A P3 revisada proíbe a chave de serviço fora dos jobs, e sem política a chave pública não lê nada. F7.2 estende essas políticas aos perfis pastor, mídia e DPO.
- O motor vem da tabela de execuções liberadas, que copia run_log.provider na migração de liberação. Assim o painel mostra o motor sem ler run_log. A marcação de execução em avaliação de F5.7 é uma coluna dessa mesma tabela, para não criar outra tabela exposta.
- D7 de F2.4.T4 lista a tabela de execuções liberadas entre as que o painel lê e deixa a tabela moment como pendência com o usuário. Até a resposta, a leitura de moment é premissa.
- O local do vínculo entre conta e papel e a aplicação da regra 6 (CLAUDE.md:21) às contas da equipe são decididos em F2.4.T4 (D7), antes deste PBI, e F5.6.T3 depende dessa decisão. A proposta que este PBI implementa guarda os e-mails de Fabio, de Filipe e das contas de teste em auth.users do Supabase Auth, para o login, e o código de avaliador, sem nome (P12), em app_metadata. A leitura de que a regra 6 e tests/test_schema.py (tests/test_schema.py:9) não alcançam o schema auth é dedução, que D7 confirma ou recusa. F6.2 só confirma ou ajusta a decisão, com migração se mudar.
- Gravar app_metadata com UPDATE em auth.users.raw_app_meta_data pelo SQL Editor é dedução. A documentação diz que essa coluna guarda papéis de acesso e que o usuário não a altera (https://supabase.com/docs/guides/platform/migrating-to-supabase/auth0; https://supabase.com/docs/guides/database/postgres/row-level-security) e mostra consulta a auth.users pelo SQL Editor (https://supabase.com/docs/guides/auth/managing-user-data), mas não mostra a atualização por SQL. F5.6.T3 confirma no projeto de desenvolvimento. A API admin não é usada, porque exige a chave secreta.
- O plano e os termos de uso da Vercel para este projeto ainda precisam ser confirmados. F2.4.T4 registra a pendência em D8, e F5.6.T9 a resolve com Fabio antes de F5.6.T2, que cria o projeto. F7.2.T2 só reconfirma para os dados da igreja do piloto. Times Hobby só podem ter uso pessoal não comercial, e a definição de uso comercial inclui quem é pago para escrever o código (https://vercel.com/docs/limits/fair-use-guidelines). O README diz que o projeto é voluntário (README.pt-BR.md:48). Se a definição se aplica é decisão de Fabio.
- O acesso aos dados depende do Supabase Auth e da RLS. O ADR de F2.4 decide se a Vercel Authentication também fica ligada. Se ficar ligada no domínio de produção, Filipe precisa de conta Vercel com acesso concedido, e no Hobby cada conta pode ter só um usuário externo (https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/vercel-authentication).
- Apagar a conta ou fazer signOut global impede novos tokens, mas o token de acesso já emitido vale até o exp (https://supabase.com/docs/guides/auth/managing-user-data; https://supabase.com/docs/guides/auth/signout). A retirada de um papel em app_metadata só aparece em auth.jwt() quando o token é renovado (https://supabase.com/docs/guides/database/postgres/row-level-security). Para limitar essa janela, o ADR de F2.4 decide entre manter a validade padrão do token de acesso, que é de 1 hora, reduzi-la, ou conferir o session_id do JWT contra auth.sessions nas políticas (https://supabase.com/docs/guides/auth/sessions).
- O Supabase anuncia a descontinuação das chaves anon e service_role até o fim de 2026, e elas continuam válidas até serem desativadas no painel do Supabase (https://supabase.com/docs/guides/getting-started/api-keys). O painel usa a chave sb_publishable_.
- O framework do painel e o método de login do Supabase Auth são decisões do ADR de F2.4. F5.6.T1 escolhe só o que o ADR não cobre (gerenciador de pacotes, versão do Node, lint e executor de testes) e registra por que cada dependência é necessária (CLAUDE.md:30). O nome do diretório do painel é decisão do PR de F5.6.T1.
- O passo de CI do front end e a integração Git do projeto na Vercel ficaram em F5.6.T2, junto com a criação do projeto, que já ligava o projeto à pasta do painel. F5.6.T5 depende só de F5.6.T1, porque o teste do lint roda no pytest do job Python que o CI já tem (.github/workflows/ci.yml:11).
- Com 9 tasks, o PBI passa em duas o limite de 7 (taskflow.md:40): o diretório do painel (F5.6.T1) precisa existir antes do projeto na Vercel e do CI (F5.6.T2), e a confirmação do plano e dos termos (F5.6.T9) precisa vir antes da criação do projeto. O refinamento decide entre manter a exceção ou mover o processamento do culto (F5.6.T7) para F5.8.
- O identificador do culto é o valor da coluna video de docs/corpus.csv (premissa da Feature).
- O código do painel fica no repositório GitHub público, sem segredo no código.
- Governança sai deste PBI e fica em F5.8.T2, que revisa o painel completo, inclusive as tabelas liberadas aqui.
- Story points e horas são sugestões. A sugestão de 8 pontos não mudou com as tasks novas (F5.6.T1 e F5.6.T9); o refinamento pode subir para 13 ou mover F5.6.T7 para F5.8.
- F2.8 entrou como dependência porque a linhagem de cada execução (digest da imagem e hash dos pesos) e o repositório de resultados ficam em F2.8. F2.5 continua como dependência pelo run_id.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável e vínculo com a Feature F5
- Azure DevOps: criar F5.6.T1 (diretório do painel) e F5.6.T9 (confirmação do plano e dos termos da Vercel) e renumerar as tasks seguintes a F5.6.T1
- Revisar F2.4: o ADR 0002 registra o projeto Vercel, o framework, o método de login, a proteção de deployment e a validade do token de acesso; D8 de F2.4.T4 registra o plano e os termos da Vercel como pendência e aponta F5.6.T9 como a task que a resolve. Até o ADR ser mesclado, o PBI não está pronto para a sprint
- Definition of Ready: decisão D7 de F2.4.T4 (local do vínculo entre conta e papel, regra 6 para as contas da equipe, tabelas lidas pelo painel e exceção da P26) registrada no ADR 0002
- Revisar F2.6: tirar o trecho 'até F7.2, do Space de F5.6', registrar a chave pública do painel e as variáveis do projeto na Vercel no inventário de F2.6.T6, e levar a F2.6.T4 o job de CI com Supabase local e as migrações, usado pelos testes pgTAP de F5.6.T4 e F5.7.T1
- Revisar F6.2, F7.2 e F7.8: F6.2 confirma ou ajusta a decisão D7 de F2.4.T4, e F7.2 e F7.8 passam a citar D7 no lugar de F6.2 para o local do vínculo entre conta e perfil
- Revisar F6.2 (T1 e T2), F6.3.T1, F7.2.T2 e F7.4.T1: trocar 'F5.6 (primeira task: confirmação do plano e dos termos da Vercel; pendência)' por F5.6.T9
- Revisar F7.2, F7.3 e F7.6: trocar Space por painel web na Vercel e usar papéis no local decidido em D7
- E-mails de Fabio, de Filipe e das duas contas de teste para o convite
- Resposta do usuário sobre a leitura da tabela moment pelo painel, registrada como pendência em D7 de F2.4.T4
- Identificar o dono do projeto Supabase de desenvolvimento, que aplica as migrações e grava app_metadata
- Refinamento: F5.6 tem 9 tasks, duas acima do limite de 7

## Preview — PBI F5.7 (novo) · Registrar no painel web na Vercel a nota de cada insight e calcular o critério 4 sobre o relatório do motor escolhido

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Registrar no painel web na Vercel a nota de cada insight e calcular o critério 4 sobre o relatório do motor escolhido |
| Tipo | Product Backlog Item |
| Pai | F5 |
| Tags | fase-0; criterio-4; painel-vercel; insight-feedback; rls |
| Estimativa | 5 pts (sugestão); tasks: 26 h |
| Dependências | F1.3, F1.5, F5.4, F5.6, F5.8, F2.8 |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro e o pastor Filipe  
Quero dar no painel uma nota de 1 a 5 e um comentário a cada insight do relatório do motor escolhido  
Para que o critério 4 seja calculado a partir das notas gravadas e ligado à execução avaliada

**Contexto:** O critério 4 pede um relatório de sermão público com pelo menos 3 insights e concordância de Fabio e Filipe de '>= 3/5', medida em insight_feedback (docs/poc-gate.md:12). F1.3 pré-registra como ler essa fração. A tabela insight_feedback tem insight_id, avaliador, nota inteira de 1 a 5 (check no banco) e comentário (supabase/migrations/0001_init.sql:17). Nenhum código grava nela. processar_culto.py envia insights_rejeitados_pelo_lint ao run_log (processar_culto.py:104-107), e F1.5 cria a coluna. Até F6.2, o avaliador é gravado como código de papel (P12). O login, o papel de avaliador, as contas de teste e a tabela de execuções liberadas vêm de F5.6, e a tela do relatório vem de F5.8. Num projeto existente, uma tabela em public tem todos os grants para anon e authenticated, e política não os retira (https://supabase.com/docs/guides/database/postgres/row-level-security).

**Regras de negócio:**
- RN01 – A nota é um inteiro de 1 a 5, e o comentário é opcional (supabase/migrations/0001_init.sql:17).
- RN02 – O campo avaliador recebe o código de papel lido da sessão do avaliador, e nunca o nome ou o e-mail (P12).
- RN03 – Um avaliador só grava nota com o próprio código. A política de RLS confere esse código.
- RN04 – Só recebem nota os insights de execuções marcadas em avaliação na tabela de execuções liberadas de F5.6, que são relatórios do motor escolhido em F4.6 (P10). A marcação é uma migração versionada aplicada pelo dono do projeto Supabase, sem a chave de serviço.
- RN05 – O critério 4 é calculado pela regra pré-registrada em F1.3. O cálculo usa a contagem de insights aprovados pelo lint e o valor de insights_rejeitados_pelo_lint do registro da mesma execução (docs/poc-gate.md:12), e só as notas dos códigos de Fabio e de Filipe. Notas com código de teste ficam fora.
- RN06 – O cálculo roda em job no HF, com 'hf jobs run <imagem>@<digest>' e a chave dos jobs, e grava o resultado no repositório de resultados com o run_id (P3; F2.8; RN06 da Feature).
- RN07 – Os textos fixos novos do formulário passam pelo lint (F5.6.T5).
- RN08 – insight_feedback fica com RLS, sem grant a anon e com grant de select, insert e update a authenticated, filtrados pelas políticas do avaliador. Delete não é concedido a nenhum cliente.

**Fora de escopo:**
- Nota do pastor da igreja do piloto (F7.3)
- Revisão e liberação de insights ao perfil pastor (F7.3)
- Mudança dos insights a partir das notas
- Escrita do valor em docs/poc-gate.md (F6.1)

#### Critérios de aceite

- Fabio e Filipe, acompanhados pela QA, dão com as próprias contas nota de 1 a 5 a um insight do relatório em avaliação, e a nota aparece gravada depois que a página é recarregada.
- Uma nota fora de 1 a 5 é recusada com mensagem, e nada é gravado.
- O registro gravado da nota tem como avaliador o código de papel, sem nome nem e-mail.
- Com a sessão da conta de teste avaliadora, uma tentativa direta pela API do Supabase de gravar nota com o código de outro avaliador é recusada.
- Um insight de uma execução que não está em avaliação não aceita nota.
- Com a chave pública, sem sessão ou com a conta de teste sem papel, leitura e gravação em insight_feedback são recusadas, e nenhuma sessão de cliente consegue apagar nota.
- O arquivo de resultado do critério 4 traz o run_id, a contagem de insights aprovados pelo lint, o número de insights rejeitados pelo lint do registro da execução, o número de notas por avaliador e a concordância pela regra de F1.3.
- O cálculo trata a falta de nota de um dos dois avaliadores conforme a regra assinada em F1.3, e um teste com uma nota faltando verifica esse tratamento.
- O cálculo ignora as notas com código de teste, e, ao fim do PBI, as contas de teste e essas notas foram apagadas.
- O teste de schema sem campo por pessoa continua passando depois das migrações.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F5.7.T1 | Backend | Criar as políticas e os grants de insight_feedback e a marcação da execução em avaliação | 7 | F5.6.T4, F1.3, F5.4, F2.6.T4 (job de CI com Supabase local e migrações; pendência) |
| F5.7.T2 | Front end | Implementar o formulário de nota e comentário por insight no relatório | 6 | F5.7.T1, F5.8.T1 |
| F5.7.T3 | Data Science | Implementar o cálculo do critério 4 pela regra de F1.3 | 5 | F1.3, F1.5 |
| F5.7.T4 | Data Science | Rodar o cálculo do critério 4 em job no HF pela imagem com digest e gravar o resultado com o run_id | 3 | F5.7.T2, F5.7.T3, F2.8, Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F5.7.T5 | QA | Verificar os critérios de aceite de F5.7 | 5 | F5.7.T4 |

<details><summary>F5.7.T1 · [Backend] Criar as políticas e os grants de insight_feedback e a marcação da execução em avaliação</summary>

**Objetivo:** Fazer o banco aceitar só notas válidas, com o código do próprio avaliador, em insights de execução em avaliação, e recusar qualquer outro acesso.

**Passos previstos:**
1. Abrir uma issue antes de mexer no schema (CONTRIBUTING.md:13).
2. Criar uma migração que, em insight_feedback, faz revoke all de anon e authenticated, concede select, insert e update a authenticated e cria políticas INSERT e UPDATE que exigem o papel de avaliador, avaliador igual ao código de auth.jwt() -> 'app_metadata' e insight de execução em avaliação, e uma política SELECT conforme a regra de visibilidade registrada em F1.3.
3. Criar a restrição de unicidade por insight e avaliador, se F1.3 confirmar a regra de nota única.
4. Acrescentar à tabela de execuções liberadas de F5.6 a coluna que marca a execução em avaliação, mantendo os grants de F5.6 (só select para authenticated).
5. Escrever testes pgTAP com 'supabase test db': nota válida, notas 0 e 6, código de outro avaliador, insight fora da execução em avaliação, delete, e acesso com a chave pública sem sessão e com sessão sem papel.
6. Acrescentar esses testes ao job de CI com Supabase local de F2.6.T4.
7. Depois de F5.4 e da lista de F1.3, abrir PR com a migração que libera e marca em avaliação os run_id escolhidos, citando culto e run_id por extenso, para o dono do projeto Supabase aplicar.
8. Conferir que tests/test_schema.py passa.

**Definição de pronto:** As migrações estão aplicadas no projeto de desenvolvimento, os testes das políticas passam no job de CI com Supabase local, o test_schema passa, e a execução em avaliação está marcada.

**Dependências:** F5.6.T4, F1.3, F5.4, F2.6.T4 (job de CI com Supabase local e migrações; pendência)

**Estimativa sugerida:** 7 h (sugestão; validar com o time)

</details>

<details><summary>F5.7.T2 · [Front end] Implementar o formulário de nota e comentário por insight no relatório</summary>

**Objetivo:** Permitir que Fabio e Filipe gravem e revejam a nota de cada insight no painel.

**Passos previstos:**
1. Em cada insight da execução em avaliação, mostrar o campo de nota de 1 a 5 e o comentário opcional.
2. Gravar com a sessão do usuário, preenchendo o avaliador com o código lido da sessão, sem campo editável.
3. Mostrar a nota gravada ao recarregar a página e o número de insights ainda sem nota.
4. Mostrar mensagens de erro para nota fora de 1 a 5 e para recusa da API.
5. Pôr no arquivo de textos de F5.6.T1 a orientação de não citar pessoas no comentário.

**Definição de pronto:** Num deploy de preview, com a conta de teste avaliadora, a nota fica gravada e as recusas aparecem, e os textos novos passam no lint do CI.

**Dependências:** F5.7.T1, F5.8.T1

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F5.7.T3 · [Data Science] Implementar o cálculo do critério 4 pela regra de F1.3</summary>

**Objetivo:** Ter um script testado que calcula o critério 4 a partir das notas de Fabio e de Filipe e do registro da execução.

**Passos previstos:**
1. Escrever um script em tools/ que lê insight, insight_feedback e run_log do run_id.
2. Contar os insights aprovados pelo lint e ler insights_rejeitados_pelo_lint.
3. Calcular a concordância pela regra de F1.3, só com as notas dos códigos de Fabio e de Filipe, e o número de notas por avaliador.
4. Tratar a falta de nota conforme a regra de F1.3 (proposta: sair com código diferente de 0, listar os insights sem nota e não gravar valor).
5. Escrever testes com dados sintéticos, inclusive notas com código de teste e uma nota faltando.

**Definição de pronto:** Os testes do cálculo passam no CI.

**Dependências:** F1.3, F1.5

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F5.7.T4 · [Data Science] Rodar o cálculo do critério 4 em job no HF pela imagem com digest e gravar o resultado com o run_id</summary>

**Objetivo:** Produzir o valor do critério 4 para F6.1.

**Passos previstos:**
1. Conferir que as notas de Fabio e de Filipe foram gravadas.
2. Publicar por tag de release a imagem com o script de F5.7.T3 pelo fluxo de F2.2 e registrar o digest.
3. Pedir ao dono da conta a aprovação de custo de um job cpu-basic (P7).
4. Rodar o script de F5.7.T3 com 'hf jobs run <imagem>@<digest>' e comando explícito, com a chave dos jobs pelo nome.
5. Gravar o resultado no repositório de resultados de F2.8 com o run_id, o digest e a linhagem.

**Definição de pronto:** O arquivo de resultado do critério 4, com o run_id e o digest, está no repositório de resultados.

**Dependências:** F5.7.T2, F5.7.T3, F2.8, Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F5.7.T5 · [QA] Verificar os critérios de aceite de F5.7</summary>

**Objetivo:** Dizer, para cada critério de aceite de F5.7, se passou ou não passou, usando só sessões de usuário e a chave pública.

**Passos previstos:**
1. Acompanhar Fabio e Filipe gravando uma nota com as próprias contas e conferir a nota depois de recarregar a página.
2. Com a conta de teste avaliadora, tentar gravar as notas 0 e 6 pelo painel, gravar pela API do Supabase com o código de outro avaliador, gravar num insight de outra execução e apagar uma nota.
3. Com a chave pública sem sessão e com a conta de teste sem papel, tentar ler e gravar em insight_feedback.
4. Conferir, com a conta de teste avaliadora, que a própria nota tem como avaliador o código de teste, e, no arquivo de resultado, que as notas aparecem por código, sem nome nem e-mail, e sem o código de teste.
5. Conferir o arquivo de resultado do critério 4 e o teste do cálculo com uma nota faltando.
6. Rodar tests/test_schema.py.
7. Pedir ao dono do projeto Supabase a remoção das contas de teste e das notas com código de teste e registrar a remoção no relatório.

**Definição de pronto:** O relatório de verificação, com passou ou não passou por critério e o registro da remoção das contas de teste, está anexado ao PBI.

**Dependências:** F5.7.T4

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- docs/poc-gate.md:12
- supabase/migrations/0001_init.sql:16-18
- processar_culto.py:98-107
- tests/test_schema.py:5
- CONTRIBUTING.md:13
- 4us-backlog-ai/references/work-items.md, seção 4
- https://supabase.com/docs/guides/database/postgres/row-level-security
- premissas P10 e P12

#### Verificação INVEST: pontos que falharam
- I: depende de F5.4, de F5.6, de F5.8, da escolha do motor em F4.6 e das regras de F1.3.

#### Premissas
- Cada avaliador tem uma nota por insight, que pode alterar até o cálculo do critério 4. É uma proposta, a confirmar em F1.3; F5.7.T1 depende desse registro.
- Cada avaliador vê só as próprias notas, para que uma nota não influencie a outra. É uma proposta, a confirmar em F1.3; F5.7.T1 depende desse registro.
- Quais relatórios de culto entram no critério 4 é decisão de F1.3. Sem essa definição, o PBI não está pronto.
- A proposta para nota faltante é o cálculo sair com código diferente de 0, listar os insights sem nota e não gravar valor. O critério de aceite cita a regra assinada em F1.3, que prevalece (work-items.md, seção 4).
- O comentário é texto livre de Fabio e Filipe. O formulário orienta a não citar pessoas, e F6.2 decide a minimização desse campo.
- A marcação em avaliação é uma coluna da tabela de execuções liberadas de F5.6, e não uma tabela nova, para não criar outra tabela exposta.
- As notas de teste da QA ficam em insights reais da execução em avaliação, porque a política só aceita nota nessas execuções. Por isso o cálculo filtra pelos códigos de Fabio e de Filipe, e as notas de teste são apagadas ao fim.
- O cálculo roda em job cpu-basic no HF e precisa de aprovação de custo (P7).
- Story points e horas são sugestões.

#### Pendências para sincronizar
- Azure DevOps: Area Path, Iteration Path, Responsável e vínculo com a Feature F5
- F1.3: definir quais relatórios de culto entram no critério 4, a regra de nota repetida, a visibilidade das notas entre avaliadores e o tratamento de nota faltante
- Agendar com Fabio e Filipe a sessão de notas depois de F5.4
- O dono do projeto Supabase apaga as contas de teste e as notas com código de teste ao fim do PBI

## Preview — PBI F5.8 (novo) · Mostrar no painel web na Vercel o relatório de uma execução liberada, com momentos, janelas agregadas e insights

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Mostrar no painel web na Vercel o relatório de uma execução liberada, com momentos, janelas agregadas e insights |
| Tipo | Product Backlog Item |
| Pai | F5 |
| Tags | fase-0; criterio-4; painel-vercel; front-end; linguagem-controlada |
| Estimativa | 5 pts (sugestão); tasks: 19 h |
| Dependências | F5.6, F5.2 |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro e o pastor Filipe  
Quero abrir no painel o relatório de uma execução liberada, com momentos, janelas agregadas e insights em ordem de tempo  
Para conhecer o formato do relatório e dar retorno sobre ele antes da escolha do motor e da decisão do gate

**Contexto:** F5.6 entrega o diretório do painel, o login, a lista de execuções liberadas com culto, motor e run_id, as políticas de RLS e a primeira execução liberada. Uma janela insuficiente sai com os percentuais nulos (reacao/aggregate.py:31-34). Nenhum motor preenche eyes_closed, então pct_olhos_fechados fica vazio (reacao/aggregate.py:38-42; reacao/types.py:25; reacao/providers/base.py:14). F5.2 entrega os rótulos em português, num arquivo do pacote reacao, e a ordem de tempo dos insights. Com Root Directory definido, o app na Vercel não acessa arquivos fora desse diretório (https://vercel.com/docs/builds/configure-a-build#root-directory), então o painel precisa de uma cópia do arquivo de rótulos. A leitura da tabela moment depende da resposta do usuário à pendência registrada em D7 de F2.4.T4, que lista as tabelas lidas pelo painel; sem ela, o momento vem do campo momento de event e insight (supabase/migrations/0001_init.sql:14-16). Em deploy de preview, a Vercel Toolbar aparece e carrega recursos de vercel.live; F5.6.T2 a desliga em preview (https://vercel.com/docs/vercel-toolbar/managing-toolbar).

**Regras de negócio:**
- RN01 – A tela lê só as tabelas e colunas liberadas por F5.6, com a sessão do usuário e a chave pública.
- RN02 – O relatório mostra só as linhas do run_id escolhido na lista de execuções liberadas.
- RN03 – Uma janela marcada como insuficiente aparece sem percentual (CLAUDE.md, regra 3).
- RN04 – A medida de olhos fechados não aparece enquanto nenhum motor preencher esse campo.
- RN05 – Os insights aparecem em ordem de tempo, com minuto, momento, trecho citado e sinais, e com os rótulos em português de F5.2.
- RN06 – Os momentos vêm da tabela moment se o usuário confirmar a pendência de moment registrada em D7 de F2.4.T4. Sem essa confirmação, a tela mostra o momento de cada evento e insight pelo campo momento.
- RN07 – No domínio de produção, o navegador só requisita o domínio do painel e o do projeto Supabase, e nenhuma resposta tem Content-Type video/* ou image/*, exceto os arquivos estáticos do próprio painel (P3 revisada).
- RN08 – Os textos fixos novos passam pelo lint no CI (F5.6.T5).

**Fora de escopo:**
- Notas dos insights (F5.7)
- Perfis pastor, mídia e DPO (F7.2 e F7.3)
- Sinalização de qualidade por culto (F7.6)
- Vídeo ou resultado da PIB (P10)
- Exibição da transcrição completa
- Relatório em PDF ou por e-mail

#### Critérios de aceite

- Fabio e o pastor Filipe, acompanhados pela QA, abrem com as próprias contas o relatório da execução liberada em F5.6.
- O cabeçalho mostra o culto, o motor e o identificador da execução, lidos da tabela de execuções liberadas.
- O relatório mostra só as linhas do run_id escolhido. Num teste com dados sintéticos de duas execuções do mesmo culto, as linhas da outra execução não aparecem.
- O relatório mostra as janelas agregadas e os insights em ordem de tempo, cada insight com minuto, momento, trecho citado e sinais. Os momentos aparecem como linha do tempo se a leitura da tabela moment for confirmada; senão, só pelo campo momento de eventos e insights.
- Nenhum texto do relatório mostra pct_voltados, pct_sorrindo ou oracao. No lugar, aparecem os rótulos em português de F5.2, e um teste no CI falha se a cópia do arquivo de rótulos no diretório do painel diferir do original.
- Uma janela marcada como insuficiente aparece com essa marcação e sem nenhum percentual.
- Nenhuma coluna ou indicador de olhos fechados aparece.
- No domínio de produção, um HAR da navegação pelo relatório mostra requisições só ao domínio do painel e ao do projeto Supabase, e nenhuma resposta com Content-Type video/* ou image/*, exceto os arquivos estáticos do próprio painel.
- A revisão da governança, com a lista de tabelas e colunas lidas pelo painel e a conferência contra a decisão D7 de F2.4.T4 sobre o vínculo entre conta e papel e a regra 6, foi aprovada no PR.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F5.8.T1 | Front end | Implementar a tela do relatório com momentos, janelas e insights | 11 | F5.6.T6, F5.6.T7, F5.2 |
| F5.8.T2 | Governança e Privacidade | Revisar os dados lidos e os textos fixos do painel contra as regras do CLAUDE.md, a P3 revisada e a decisão D7 | 3 | F5.8.T1, F5.6.T5, F2.4.T4 (D7: lista de tabelas lidas pelo painel) |
| F5.8.T3 | QA | Verificar os critérios de aceite de F5.8, incluindo a rede do navegador no domínio de produção | 5 | F5.8.T1, F5.8.T2 |

<details><summary>F5.8.T1 · [Front end] Implementar a tela do relatório com momentos, janelas e insights</summary>

**Objetivo:** Mostrar o relatório de uma execução liberada conforme as regras 3 e 4 do CLAUDE.md e os rótulos de F5.2.

**Passos previstos:**
1. Montar o cabeçalho com o culto, o motor e o run_id lidos da tabela de execuções liberadas.
2. Buscar as linhas por culto e run_id da execução escolhida na lista de F5.6.T6.
3. Copiar para o diretório do painel o arquivo de rótulos de F5.2.T4, porque o painel não lê arquivo fora do Root Directory (https://vercel.com/docs/builds/configure-a-build#root-directory), e escrever um teste, rodado no CI, que falha se a cópia divergir do original.
4. Montar a linha do tempo de momentos com os rótulos de F5.2.T4, se a leitura da tabela moment for confirmada; senão, mostrar o momento pelo campo momento de eventos e insights.
5. Mostrar as janelas de 30 s com percentuais só quando a janela não for insuficiente. A janela insuficiente aparece marcada e sem percentual, e a medida de olhos fechados não aparece.
6. Listar os insights em ordem de tempo, com minuto, momento, trecho citado e sinais, usando os rótulos em português.
7. Não carregar recursos de fora do domínio do painel e do Supabase, e pôr os textos fixos no arquivo de F5.6.T1.
8. Escrever um teste com dados sintéticos de duas execuções do mesmo culto, que confere que só as linhas do run_id escolhido aparecem.

**Definição de pronto:** Um deploy de preview mostra o relatório da execução liberada em F5.6.T7 conforme os critérios 2 a 7, e o teste com duas execuções e o teste da cópia dos rótulos passam no CI.

**Dependências:** F5.6.T6, F5.6.T7, F5.2

**Estimativa sugerida:** 11 h (sugestão; validar com o time)

</details>

<details><summary>F5.8.T2 · [Governança e Privacidade] Revisar os dados lidos e os textos fixos do painel contra as regras do CLAUDE.md, a P3 revisada e a decisão D7</summary>

**Objetivo:** Deixar registrado o que o painel lê e confirmar que isso cabe nas regras do CLAUDE.md, na P3 revisada e na decisão D7 de F2.4.T4.

**Passos previstos:**
1. Listar as tabelas e colunas que o painel lê, inclusive a de execuções liberadas e, se for o caso, moment, e comparar com a lista de tabelas de D7 do ADR 0002 (F2.4.T4) e com a P3 revisada: nenhuma tabela fora da lista, e nenhuma leitura de transcript_segment ou run_log.
2. Confirmar que o painel não acessa transcrição completa, registro de execução, vídeo, quadro, recorte nem observação por rosto.
3. Revisar os textos fixos quanto à linguagem controlada.
4. Conferir que o painel segue a decisão D7 de F2.4.T4 sobre o local do vínculo entre conta e papel e sobre a regra 6 (CLAUDE.md:21) para as contas da equipe, e registrar onde ficam os e-mails de Fabio, de Filipe e das contas de teste e o código de avaliador. Se F6.2 ajustar a decisão, registrar o que muda no painel.
5. Registrar a revisão na documentação do painel.

**Definição de pronto:** O registro da revisão, com a lista de tabelas e colunas lidas pelo painel e a conferência contra a lista de tabelas e a decisão D7, foi aprovado no PR.

**Dependências:** F5.8.T1, F5.6.T5, F2.4.T4 (D7: lista de tabelas lidas pelo painel)

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F5.8.T3 · [QA] Verificar os critérios de aceite de F5.8, incluindo a rede do navegador no domínio de produção</summary>

**Objetivo:** Dizer, para cada critério de aceite de F5.8, se passou ou não passou.

**Passos previstos:**
1. Acompanhar Fabio e Filipe abrindo o relatório com as próprias contas (critério 1).
2. Com a conta de teste avaliadora, conferir o cabeçalho, os momentos, as janelas, os insights, a ordem, os rótulos, uma janela insuficiente e a ausência da medida de olhos fechados.
3. Rodar o teste com duas execuções do mesmo culto e conferir no CI o teste da cópia do arquivo de rótulos.
4. No domínio de produção, gravar um HAR da navegação pelo relatório e conferir os domínios e o Content-Type das respostas.
5. Conferir o PR da revisão da governança.

**Definição de pronto:** O relatório de verificação, com passou ou não passou por critério e o HAR anexado, está no PBI.

**Dependências:** F5.8.T1, F5.8.T2

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- reacao/aggregate.py:31-42
- reacao/types.py:5-8,25,52
- reacao/providers/base.py:14
- supabase/migrations/0001_init.sql:14-16
- CLAUDE.md:21 (regra 6) e regras 3 e 4
- tests/test_schema.py:9
- https://vercel.com/docs/builds/configure-a-build#root-directory
- https://vercel.com/docs/vercel-toolbar/managing-toolbar
- F2.4.T4 (decisão D7, citada na revisão)
- premissas P3 revisada e P10

#### Verificação INVEST: pontos que falharam
- I: depende de F5.6 e de F5.2.
- V: sozinho, entrega a primeira leitura de Filipe. O valor para o gate vem com as notas de F5.7.

#### Premissas
- F5.8 nasce da divisão do antigo F5.6 (taskflow.md, seção 1). F5.8.T1 vem da antiga F5.6.T5 (tela), F5.8.T2 vem da antiga F5.6.T8 (governança), e F5.8.T3 é uma task de QA nova.
- O critério de rede vale no domínio de produção. Em preview, a Vercel Toolbar pode carregar recursos de vercel.live, e F5.6.T2 a desliga com VERCEL_PREVIEW_FEEDBACK_ENABLED=0 (https://vercel.com/docs/vercel-toolbar/managing-toolbar).
- O arquivo de rótulos de F5.2.T4 fica no pacote reacao, que a imagem copia. O painel usa uma cópia no próprio diretório, porque o app não acessa arquivos fora do Root Directory, e um teste no CI compara a cópia com o original.
- A governança fica neste PBI e revisa o painel completo, inclusive as tabelas liberadas em F5.6 e o registro de e-mails em auth.users, contra a decisão D7 de F2.4.T4.
- Os rótulos em português são revisados por Fabio e Filipe nesta leitura (premissa de F5.2).
- Story points e horas são sugestões.

#### Pendências para sincronizar
- Azure DevOps: criar o PBI F5.8, preencher Area Path, Iteration Path e Responsável e vincular à Feature F5
- Resposta do usuário sobre a leitura da tabela moment, registrada como pendência em D7 de F2.4.T4
