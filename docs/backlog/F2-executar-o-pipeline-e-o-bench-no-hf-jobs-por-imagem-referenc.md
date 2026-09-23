[Voltar ao épico](README.md)

# Preview — Feature F2 (novo) · Executar o pipeline e o bench no HF Jobs por imagem referenciada por digest, com código, pesos e dados fixados e resultados com linhagem

### Campos
| Campo | Conteúdo |
|---|---|
| Título | Executar o pipeline e o bench no HF Jobs por imagem referenciada por digest, com código, pesos e dados fixados e resultados com linhagem |
| Tipo | Feature |
| Pai | Epic |
| Tags | Épico: gate da Fase 0 e piloto; HF Jobs; Docker; DevOps; MLOps; reprodutibilidade; linhagem; segredos |
| Estimativa | 58 pts / 233 h (soma dos PBIs, sugestão) |

### Descrição

**Problema:** Os comandos de docs/hf-jobs.md usam 'hf jobs uv run', que roda na imagem padrão ghcr.io/astral-sh/uv:python3.12-bookworm, baixa o script de main por raw.githubusercontent.com e instala reacao do HEAD de main sem commit fixado (docs/hf-jobs.md:13-29; processar_culto.py:4; huggingface_hub/_jobs_api.py:96). main ainda tem a quebra da pose: o PR #3 está aberto como rascunho e o commit 5176bc3 não está em origin/main. Não há lockfile, porque uv.lock está no .gitignore (.gitignore:223). O extra [gpu] resolve onnxruntime junto com onnxruntime-gpu e instala opencv em duplicidade (uv pip compile do levantamento). Os três motores do bench não cabem numa mesma resolução: libreface 0.2.0 fixa torch==2.0.0, opencv-python==4.10.0.84 e mediapipe==0.10.5 (https://pypi.org/pypi/libreface/0.2.0/json), py-feat 2.1.3 exige torch>=2.5 (https://pypi.org/pypi/py-feat/2.1.3/json), e a resolução de .[gpu,pyfeat,libreface], o conjunto do cabeçalho de bench.py:3, cai para py-feat 0.6.1 e torch 2.0.0 com pacotes nvidia-*-cu11 e três pacotes opencv (lock310.txt do levantamento, linhas 205-230, 245-253, 296 e 392). A imagem do Dockerfile nunca rodou no HF, nunca foi publicada e instala só [gpu,llm] (Dockerfile:11; nenhuma tag no GitHub), e o workflow docker publica :latest a cada tag v* (.github/workflows/docker.yml:2-4,22-25). Os pesos vêm de GitHub, cloud.ovgu.de e do instalador do insightface, sem hash, e o zip buffalo_sc traz o w600k_mbf.onnx de reconhecimento. O CSV do bench some com o contêiner (bench.py:255), e o tamanho de /dev/shm e o timeout máximo no HF Jobs não estão documentados. As tabelas de resultado se ligam só pelo texto culto, então reprocessar um culto mistura linhas (supabase/migrations/0001_init.sql:6-18; reacao/store.py:24-26). Nada compara os agregados de duas execuções. Os comandos passam segredos com valor na linha de comando, inclusive ANTHROPIC_API_KEY (docs/hf-jobs.md:14-17), e a forma sem valor '--secrets HF_TOKEN' envia ao job o token com que a própria CLI se autentica (huggingface_hub/cli/_cli_utils.py:926-933,953-969). Com ANTHROPIC_API_KEY, a transcrição do culto, até 60000 caracteres, vai à API da Anthropic (reacao/moments.py:48-61); para cultos públicos, esse envio é exceção à P3 que ainda precisa da confirmação de Fabio (P26). Sem credenciais, o Store grava em arquivo local que se perde ao fim do job (reacao/store.py:19-23). Não há decisão registrada sobre o modo de execução, a composição e o registro da imagem, o namespace e o acesso aos recursos do HF, quais dados, tabelas e credenciais cada ambiente recebe agora que o painel web do produto fica na Vercel (P3 revisada), nem sobre a exceção da P26. O time 'Fabio Pinheiro's projects' da Vercel tem só o projeto ai-guitar-coach-pilot, sem relação com este sistema (Vercel, list_teams e list_projects, 2026-09-23).

**Solução proposta:** Registrar no ADR 0002 o modo de execução dos jobs, a composição e o registro da imagem, com as versões exatas de libreface e py-feat, o namespace e o acesso no HF, a divisão de dados e credenciais entre HF, Supabase e o painel web na Vercel, com as tabelas do Supabase que o painel lê e escreve, o local do vínculo entre conta e papel e a aplicação da regra 6 às contas da equipe, as decisões do painel (projeto, framework, método de login do Supabase Auth, proteção de deployment e validade do token de acesso), a pendência do plano da Vercel com a task que a resolve e a decisão de Fabio sobre o envio da transcrição de cultos públicos à API da Anthropic (P26). Mesclar o PR #3, travar as dependências conforme a composição de imagem do ADR, fixar por tag o caminho de desenvolvimento e, depois da importação dos itens no Azure DevOps, trocar os IDs antigos citados no código e na documentação. Configurar, antes do primeiro job pago, tokens de escopo mínimo e a entrega de segredos aos jobs a partir do local de guarda de quem lança, com um inventário único de credenciais, preparar o Supabase de desenvolvimento com RLS habilitada e subir no CI o Supabase local com as migrações. Publicar por digest, por tag de release ou de pré-release, a imagem ou as imagens de motor decididas no ADR, usadas por todos os jobs do gate e do piloto, e validá-las em jobs de fumaça com a fixture sintética lida do dataset por revisão. Carregar os pesos por revisão fixa com SHA-256 conferido antes do primeiro quadro, de repositórios de modelo privados quando a decisão de licença de F4.3 permitir, sem o arquivo de reconhecimento. Separar por run_id as linhas de cada execução no Supabase e enviar a um repositório privado de resultados o conjunto de cada execução com linhagem, inclusive o registro das falhas. Comparar execuções com um script de paridade.

**Usuários impactados:** Fabio Pinheiro (dono da conta HF ds-fabiopinheiro, aprovador de custo de cada job e de projeto Supabase, e quem decide a exceção da P26), Time de DevOps e MLOps, Time de ML e visão computacional que roda o bench e lê os números do gate, Time de back end e front end do painel web na Vercel, que usa a divisão de dados, tabelas e credenciais registrada no ADR 0002

**Valor de negócio:** Hoje nenhum número do gate pode ser atribuído a uma versão de código, imagem, peso e dado: nenhum job foi executado no HF ('hf jobs ps -a', 2026-09-23) e o run_log não tem commit, revisão de dataset nem versão de modelo (supabase/migrations/0001_init.sql:18; processar_culto.py:104-106). Com F2, cada número que vai ao gate e ao ADR 0001 cita um run_id com script, commit, digest da imagem, vídeo, revisão do dataset, hash dos pesos e JOB_ID, que é a métrica de linhagem do épico. A mesma imagem roda no HF Jobs e fora dele, requisito que o épico mantém para a produção local (P3). A chave de serviço do Supabase entra só nos jobs do HF, a partir do local de guarda de quem lança, e o painel web na Vercel lê com a chave pública sob RLS (P3 revisada).

**Regras de negócio:**
- RN01 – Os jobs do gate e do piloto rodam com 'hf jobs run' pela imagem referenciada por digest. 'hf jobs uv run' fica só para desenvolvimento (decisão a registrar no ADR 0002, F2.4).
- RN02 – Toda execução paga no HF Jobs é aprovada por Fabio antes do lançamento, com flavor e timeout explícitos (P7). A criação de projeto Supabase, que tem custo mensal (https://supabase.com/docs/guides/platform/billing-faq), também é aprovada por Fabio, com o custo mensal previsto.
- RN03 – Jobs de fumaça, validação e paridade usam só os vídeos que F1.3 fixa: fixture sintética, vídeos públicos ou, depois de F3.1, os clipes 07 a 10 (árvore, F1.3). Dentro do HF, a fixture sintética é lida por URI hf://datasets/ do dataset ds-fabiopinheiro/reacao-poc-corpus, na revisão registrada em tests/fixtures/README.md (F1.1.T6), porque F1.1 recusa caminho local com JOB_ID, inclusive arquivo gerado dentro do contêiner (F1.1 RN08 e RN11).
- RN04 – Nenhum quadro, recorte ou vídeo em disco (regra 1 do CLAUDE.md): vídeos baixados só para /dev/shm, sem montar o dataset com -v, porque a montagem guarda em cache no disco do job (https://huggingface.co/docs/hub/jobs-large-datasets#mount-a-dataset-model-or-bucket).
- RN05 – Nenhum arquivo de reconhecimento facial, como w600k_mbf.onnx, na imagem, nos repositórios de modelo, no CI ou no job (regra 2 do CLAUDE.md). Exceção temporária: entre F1.6 e F2.3, o CI de F1.6 baixa da origem o buffalo_sc.zip, que traz w600k_mbf.onnx; F2.3 encerra a exceção.
- RN06 – Segredos entram nos jobs só pelo nome (--secrets NOME) ou por --secrets-file, nunca na forma NOME=valor. O HF_TOKEN do job entra por '--secrets-file -' com o valor do token dos jobs, porque '--secrets HF_TOKEN' envia o token de quem lança (F2.6).
- RN07 – A chave de serviço do Supabase fica só nos segredos dos jobs do HF e no local de guarda de quem lança, registrado no inventário de F2.6, de onde entra no job por '--secrets-file -' a cada lançamento. Nos Jobs do piloto sem quem lance (Job agendado de F7.4.T4 e Job de origem do webhook de F7.5.T4), os segredos ficam guardados na especificação do Job no HF e entram no inventário com o id do Job e a rotação. O painel web na Vercel recebe só a URL do projeto e a chave pública e não recebe vídeo, quadro, recorte de rosto nem observação por rosto (P3 revisada).
- RN08 – Os resultados gravados no Supabase e no repositório privado de resultados carregam run_id e não têm campo por pessoa (regra 6 do CLAUDE.md).
- RN09 – Imagens são referenciadas por tag de release ou digest, nunca por :latest (docs/onprem.md:64).
- RN10 – Fora do HF, o docker run e as execuções locais deste épico usam só a fixture sintética, e o CI usa também o vídeo licenciado de F1.6 (P26). Testes fora do HF gravam no destino local, sem a chave de serviço.
- RN11 – A ANTHROPIC_API_KEY só entra nos jobs se o ADR 0002 registrar a confirmação de Fabio sobre a exceção da P26 (envio da transcrição de cultos públicos à API da Anthropic na Fase 0), e entra por '--secrets-file -' a partir do local de guarda de quem lança. Sem a confirmação, os jobs rodam sem a chave, com a heurística de momentos e o modelo de frase dos insights (reacao/moments.py:48-50; reacao/insights.py:32-36; P26).
- RN12 – O painel web na Vercel lê e escreve só as tabelas listadas na decisão D7 do ADR 0002: lê window_aggregate, event e insight e, se D7 registrar, moment (P3 revisada: 'e momentos, se o ADR de F2.4 registrar'), além da tabela de execuções liberadas de F5.6 e, na Fase 1, dos indicadores de qualidade de F7.6; escreve insight_feedback e, na Fase 1, o estado de revisão do insight (F7.3). transcript_segment, run_log e service ficam fora, porque a P3 revisada limita a leitura a agregados, eventos, insights e momentos, e o trecho citado do relatório está em insight.trecho (supabase/migrations/0001_init.sql:3-4,13,16,18; reacao/insights.py:25).
- RN13 – Nenhum job pago de F2 é lançado com o token clássico de escrita: a CLI de quem lança usa o token de lançamento de F2.6 desde os jobs de fumaça de F2.2 (F2.2.T4).
- RN14 – O inventário de F2.6.T6 é o registro único das credenciais do épico, sem valores. Cada PBI que cria credencial a registra nele com nome, local, escopo, dono, validade e rotação ou revogação: os tokens de uso único com escrita no dataset do corpus (F1.1.T6, F5.1.T3 e F3.6.T3), o token de leitura do Space de rotulagem (F3.3.T1), as variáveis do projeto do painel na Vercel (F5.6.T2: só a URL e a chave pública do Supabase), a credencial da equipe de mídia (F7.1.T2) e os segredos guardados nos Jobs do piloto, com o id do Job (F7.4.T4 e F7.5.T4).
- RN15 – Depois da importação dos itens no Azure DevOps, o código e a documentação citam os IDs novos: nenhum arquivo mantém PBI-000D, PBI-000H, PBI-041, PBI-057, PBI-103, TSK-207, PBI-105 ou PBI-106 (F2.1.T8). O exemplo PBI-104 de CLAUDE.md:31 e CONTRIBUTING.md:20 só muda com a aprovação de Fabio.

**Fora de escopo:**
- Execução da paridade no servidor local (lado local do PBI-106, premissa P3)
- SBOM e varredura de vulnerabilidades da imagem
- Versionamento do corpus e dos rótulos (F3.5)
- Disparo por webhook dos jobs do piloto (F7.5)
- Mecanismo de papel e políticas de RLS do avaliador do gate (F5.6 e F5.7) e dos perfis do piloto (F7.2 e F7.8); o ADR 0002 decide só o local do vínculo entre conta e papel e a aplicação da regra 6 às contas da equipe (D7)
- Criação do projeto na Vercel e cadastro da URL e da chave pública do Supabase no painel (F5.6)
- Confirmação do plano e dos termos de uso da Vercel, feita pela task de F5.6 movida de F7.2.T2; D8 do ADR 0002 aponta para ela
- Construção do Space de rotulagem (F3.3) e do destino dos vídeos do piloto (F7.1)
- Carga dos pesos de LibreFace e Py-Feat (F4.1 e F4.2), que reutilizam o mecanismo de F2.3
- Troca do detector quando a licença vetar o espelhamento (F4.7)
- Decisão sobre o uso da API da Anthropic nos cultos do piloto (F6.3, P26)
- Projeto Supabase de produção
- Implementação do painel, do diretório com lockfile e do CI do painel (F5.6.T1 e F5.6.T2); o ADR 0002 só decide projeto, framework, login, proteção de deployment e validade do token (D9)
- Definição dos segredos guardados nos Jobs automáticos do piloto (F7.4.T4 e F7.5.T4), que só usam o inventário de F2.6.T6
- Testes de política de F5.6, F5.7 e F7.2, que rodam no job de CI com o Supabase local de F2.6.T4

**Dependências técnicas:**
- Conta HF ds-fabiopinheiro com saldo positivo de créditos, visível só na página de billing (https://huggingface.co/docs/hub/jobs-pricing), e aprovação de Fabio para cada job pago (P7)
- Assinatura PRO da conta (periodEnd 2026-10-01 no whoami do HF de 2026-09-23; renovação a confirmar com Fabio), exigida por Space Gradio ou Docker pessoal e pela visibilidade protected (https://huggingface.co/docs/hub/spaces-overview)
- Organização no HF com papel de escrita, se o ADR 0002 escolher organização; o usuário tem papel read em impacto-cognitivo (whoami do HF, 2026-09-23)
- Repositório GitHub ds-fabiopinheiro/church-sentiment-analysis com permissão admin para tags e publicação no GHCR (P11)
- Organização Supabase de Fabio no plano Pro (Supabase get_organization, 2026-09-23). O projeto de desenvolvimento deste sistema não foi encontrado (Supabase list_projects, 2026-09-23), embora supabase/migrations/0001_init.sql:2 diga que foi criado; criá-lo depende da aprovação de custo (RN02)
- Time 'Fabio Pinheiro's projects' na Vercel, onde F5.6 cria o projeto do painel; plano e termos de uso a confirmar na task de F5.6 movida de F7.2.T2, para a qual D8 do ADR 0002 aponta
- Decisão de Fabio sobre a exceção da P26 na Fase 0, registrada em D7 do ADR 0002 (F2.4.T4)
- F1.1 (guarda corrigida antes de qualquer job e, em F1.1.T6, fixture sintética no dataset por revisão, lida pelos jobs de fumaça), F1.3 (vídeos permitidos por tipo de job), F1.5 (contrato do run_log e flavor real; configuração local do Supabase CLI em F1.5.T1, usada pelo CI de F2.6.T4), F1.6 (motores reais no CI), F3.1 (uso dos clipes 07 a 10), F3.5 (revisão do dataset), F4.3 (licença e decisão de espelhamento de todos os pesos, inclusive o faster-whisper) e F5.1 (vídeo público no dataset, se F3.1 vetar os clipes). F4.7 não é dependência: com o veto de F4.3 ao espelhamento do detector, os critérios de detector de F2.3 passam a F4.7
- Importação dos itens da árvore no Azure DevOps, que gera os IDs novos usados em F2.1.T8

**Riscos:**
- A assinatura PRO tem periodEnd 2026-10-01 (whoami do HF, 2026-09-23), sem campo que indique cancelamento; a renovação está a confirmar com Fabio. Sem renovação, Space Gradio ou Docker pessoal e a visibilidade protected deixam de estar disponíveis, o que muda o modelo de acesso do ADR 0002 para o Space de rotulagem (F3.3).
- O tamanho de /dev/shm e o timeout máximo de um job não estão documentados (https://huggingface.co/docs/hub/jobs-configuration#timeout). Se /dev/shm não comportar um culto inteiro (dedução de cerca de 2,3 GB por hora de vídeo, P19), o download para memória precisa mudar antes de F5.4.
- A documentação de Jobs não descreve credencial para imagem em registro privado, e com imagem hospedada em Docker Space os Jobs usam sempre o último build, sem referência por digest (https://huggingface.co/docs/hub/jobs-images). Se o ADR 0002 exigir imagem privada, nenhuma opção conhecida cumpre RN01 e RN09.
- Os motores não cabem numa mesma resolução: libreface 0.2.0 fixa torch==2.0.0, opencv-python==4.10.0.84 e mediapipe==0.10.5 (https://pypi.org/pypi/libreface/0.2.0/json), e py-feat 2.1.3 exige torch>=2.5 (https://pypi.org/pypi/py-feat/2.1.3/json). Com os três numa imagem, o Py-Feat cai para 0.6.1 e o torch para 2.0.0 com runtime CUDA 11 (lock310.txt do levantamento), o que condiciona a composição de D2 e a versão que F4.1 e F4.2 fixam.
- O onnxruntime de CPU resolvido junto com o onnxruntime-gpu pode esconder o CUDAExecutionProvider, e o torch com runtime CUDA 13 pode não casar com a base CUDA 12.4.1 (uv pip compile do levantamento; Dockerfile:3). Os jobs t4-small de F2.2 e F2.3 confirmam.
- Os modelos pré-treinados do insightface, inclusive o detector comum aos três motores, servem só para pesquisa não comercial (insightface-2.0.dist-info/METADATA:50-54). Se F4.3 vetar o espelhamento, o detector não é carregado, F4.7 é acionado e recebe os critérios de detector de F2.3.
- Pela documentação do Supabase, chave publishable ou secret enviada em 'Authorization: Bearer' é rejeitada por não ser JWT (https://supabase.com/docs/guides/getting-started/api-keys, seção Known limitations). O Store envia a chave nos cabeçalhos apikey e Authorization (reacao/store.py:24-25) e pode falhar com as chaves novas; F2.6 ajusta.
- A documentação do Supabase anuncia a descontinuação das chaves legadas anon e service_role até o fim de 2026 (https://supabase.com/docs/guides/getting-started/migrating-to-new-api-keys). Usar a service_role legada exigiria troca de chave durante o piloto.
- Sem SUPABASE_URL ou chave, o Store grava em arquivo local que some ao fim do job (reacao/store.py:19-23). Até F2.6, um segredo esquecido perde os resultados sem erro.
- Na forma '--secrets HF_TOKEN', a CLI envia ao job o token com que ela se autentica (huggingface_hub/cli/_cli_utils.py:926-933,953-969); hoje esse token é clássico, com papel write (whoami do HF, 2026-09-23). Até F2.6, um job lançado assim recebe permissão de escrita em todos os repositórios da conta.
- Sem a confirmação de Fabio sobre a exceção da P26, os jobs rodam sem ANTHROPIC_API_KEY, e os momentos e insights saem da heurística e do modelo de frase (reacao/moments.py:48-50; reacao/insights.py:32-36), o que muda a comparação entre segmentação por LLM e por heurística de F5.5 (árvore, F5.5).
- Criar o projeto Supabase de desenvolvimento acrescenta custo mensal: a organização está no plano Pro, com um projeto ativo (Supabase get_organization e list_projects, 2026-09-23), e projetos adicionais começam em cerca de US$ 10 por mês, cobrados por hora (https://supabase.com/docs/guides/platform/billing-faq).
- O saldo de créditos só aparece na página de billing, e o valor 'US$ 20 cobrem o PoC' (docs/hf-jobs.md:3) não tem cálculo registrado (P7).
- Plano e termos de uso da Vercel para este projeto não estão confirmados. Se não servirem, a hospedagem do painel registrada no ADR 0002 muda.
- Jobs parados por timeout ou cancelados podem terminar sem o registro de falha próprio (premissa); o estado deles vem do HF (F7.5).
- Entre F1.6 e F2.3, o CI baixa o buffalo_sc.zip com w600k_mbf.onnx (exceção registrada em RN05).
- O build da imagem com torch, CUDA e motores pode não caber no disco do runner padrão do GitHub Actions (premissa não verificada).
- A documentação de CI do Supabase usa o CLI em 'version: latest' (https://supabase.com/docs/guides/deployment/ci/testing). Sem versão fixa, o job de F2.6.T4 pode mudar de comportamento sem PR (dedução); F2.6.T4 fixa a versão.
- supabase/migrations/0001_init.sql já foi aplicada, segundo a linha 2 do arquivo. F2.1.T8 muda só a linha de comentário 21, e tests/test_schema.py ignora comentários (tests/test_schema.py:11); se o time não aceitar mexer em migração aplicada, o ID novo vai para um comentário da próxima migração.

**Estratégia de fatiamento:** Por passo do fluxo de execução de um job (estratégia 1 do TaskFlow): decisão do modo de execução, da composição da imagem, do acesso, da fronteira de dados, das tabelas e das decisões do painel e da exceção da P26 (F2.4); código e dependências, com a troca dos IDs antigos depois da importação no Azure DevOps (F2.1); segredos, inventário, destino dos agregados e Supabase local no CI (F2.6); imagem (F2.2); pesos (F2.3); separação das execuções no Supabase (F2.5); conjunto de resultados com linhagem (F2.8); comparação entre execuções (F2.7). Ordem sugerida: F2.4 e F2.1 em paralelo, com as tasks de lock de F2.1 depois da decisão D2; F2.6.T1 a F2.6.T6 (tokens, entrega de segredos, Supabase, RLS com o job de CI, Store e inventário); F2.2, cujo primeiro job pago (F2.2.T4) usa o token de lançamento de F2.6 e a fixture publicada em F1.1.T6; F2.6.T7, que verifica em job pela imagem publicada por F2.2.T2; F2.3 e F2.5 em paralelo; F2.8; F2.7. F2.1.T8 roda quando a importação no Azure DevOps gerar os IDs novos. F2.2 e F2.6 dependem um do outro só no nível de task, sem ciclo entre tasks (ver premissas). Cada PBI entrega um passo verificável sozinho; as dependências entre eles estão registradas em cada PBI. A Feature tem 8 PBIs, um acima do limite de 7 (ver premissas).

### Critérios de aceite
- Um job de validação lançado com 'hf jobs run' pela imagem referenciada por digest, com o motor hsemotion sobre um vídeo do dataset permitido por F1.3, grava no repositório privado de resultados o conjunto do run_id com tag e SHA do script, commit do pacote, digest, caminho e SHA-256 do vídeo, revisão do dataset, SHA-256 de cada peso carregado e JOB_ID.
- O mesmo digest executa processar_culto.py no HF Jobs e com docker run fora do HF, com a fixture sintética.
- Depois de F2.3, nenhum job, imagem ou execução do CI contém w600k_mbf.onnx.
- Um peso com SHA-256 diferente do manifesto interrompe a execução antes do primeiro quadro, com código de saída diferente de zero.
- Nenhum comando documentado e nenhum 'hf jobs inspect' dos jobs mostra valor de segredo.
- Todos os jobs de F2, inclusive os de fumaça de F2.2, são lançados pela CLI autenticada com o token de lançamento de F2.6.
- Dentro de um job lançado pelo comando documentado, a identificação do token mostra o token dos jobs; o token de quem lança não aparece.
- O token usado pelos jobs recebe erro de permissão ao tentar escrever no dataset do corpus.
- No Supabase de desenvolvimento, uma leitura com a chave pública e sem sessão de usuário retorna zero linhas nas 8 tabelas.
- Nenhum arquivo do repositório, secret do GitHub Actions, variável de ambiente de projeto na Vercel ou Space contém a chave de serviço do Supabase.
- O inventário de credenciais registra o local de guarda da chave de serviço e do token dos jobs do lado de quem lança e tem os campos usados pelos tokens de uso único e pelos segredos guardados nos Jobs automáticos do piloto (validade, rotação ou revogação e id do Job).
- O procedimento de lançamento documentado só passa ANTHROPIC_API_KEY se o ADR 0002 registrar a confirmação de Fabio sobre a exceção da P26.
- Um job que falha com exceção, ou que termina com código diferente de zero sem exceção, deixa no repositório de resultados o run_id, a etapa e a mensagem.
- Existe relatório de paridade de window_aggregate entre duas execuções do mesmo digest na t4-small e entre t4-small e cpu-basic.
- O ADR 0002 está aceito em main e lista o que o HF, o Supabase e o painel web na Vercel recebem, as tabelas que o painel lê e escreve, o local do vínculo entre conta e papel, a aplicação da regra 6 às contas da equipe, as decisões do painel (projeto, framework, login, proteção de deployment e validade do token), a pendência do plano da Vercel com a task que a resolve e a decisão sobre a exceção da P26.
- Em cada push e pull request, o CI sobe o Supabase local, aplica as migrações em ordem e roda os testes de banco, e uma tabela nova sem RLS reprova esse job.
- Uma tag de pré-release num commit de branch publica as imagens de D2 e registra os digests na release marcada como pré-release, sem publicar tag latest.
- Depois de F2.1.T8, a busca por 'PBI-' e 'TSK-' no código e na documentação só encontra o exemplo de CLAUDE.md:31 e CONTRIBUTING.md:20, e só se Fabio não tiver aprovado a troca.

### Alterações em relação à árvore
- Feature F2, problema e solução: 'acesso aos Spaces' passou a 'acesso aos recursos do HF', e o ADR registra a divisão de dados e credenciais entre HF, Supabase e painel web na Vercel (P3 revisada). Acrescentados os fatos do Store sem credencial (reacao/store.py:19-23), do time da Vercel (list_projects, 2026-09-23), do conflito entre libreface 0.2.0 e py-feat 2.1.3 (PyPI; lock310.txt do levantamento), do workflow docker que publica :latest em tag v* (docker.yml:2-4,22-25), do envio do token de quem lança por '--secrets HF_TOKEN' (cli/_cli_utils.py:926-933,953-969) e do envio da transcrição à API da Anthropic com ANTHROPIC_API_KEY (docs/hf-jobs.md:16; reacao/moments.py:48-61; P26).
- Feature F2, solução, F2.2 e F2.4: 'imagem com os três motores' passou a 'imagem ou imagens de motor conforme D2 do ADR 0002', porque libreface 0.2.0 fixa torch==2.0.0 e py-feat 2.1.3 exige torch>=2.5.
- Feature F2, regras: RN02 cobre também a criação de projeto Supabase, que tem custo mensal (billing FAQ do Supabase); RN03 cita a lista de F1.3 como está na árvore (fixture sintética, vídeos públicos ou, depois de F3.1, clipes 07 a 10); RN05 registra a exceção temporária do CI de F1.6 até F2.3; RN06 acrescenta a entrega do HF_TOKEN por '--secrets-file -'; RN07 registra que a chave de serviço fica também no local de guarda de quem lança; RN10 estende a regra da fixture às execuções locais e aos testes que gravam resultados. Nesta rodada: RN11 (ANTHROPIC_API_KEY só com a confirmação da P26), RN12 (tabelas do painel conforme D7) e RN13 (jobs lançados com o token de lançamento).
- Feature F2, critérios: o critério do 'job do gate' passou a job de validação com motor hsemotion sobre vídeo do dataset permitido por F1.3, porque o bench do gate é F4.6; o de w600k_mbf.onnx vale depois de F2.3; acrescentado o critério do token dentro do job; o da chave de serviço cobre repositório, GitHub Actions, Vercel e Space, com critério separado para o inventário; o de falha cobre também término com código diferente de zero sem exceção. Nesta rodada: acrescentados os critérios do token de lançamento em todos os jobs e da ANTHROPIC_API_KEY condicionada à P26; o critério do ADR passou a exigir a lista de tabelas do painel e a decisão sobre a P26.
- Feature F2, riscos e premissas: a assinatura PRO passou a 'periodEnd 2026-10-01, renovação a confirmar'; a afirmação de que um job parado por timeout não passa pelo código foi para as premissas como dedução; acrescentados os riscos do conflito de pacotes dos motores, do custo de projeto Supabase adicional, da descontinuação das chaves legadas do Supabase até o fim de 2026, do envio do token de quem lança, da janela do CI de F1.6 e, nesta rodada, dos jobs sem ANTHROPIC_API_KEY se a P26 não for confirmada.
- Feature F2, fora de escopo: acrescentados o projeto na Vercel (F5.6), as políticas para usuários autenticados (F5.6 e F7.2), o Space de rotulagem e o destino do piloto (F3.3 e F7.1), os pesos de LibreFace e Py-Feat (F4.1 e F4.2), a troca do detector (F4.7), o projeto Supabase de produção e, nesta rodada, a decisão sobre a API da Anthropic nos cultos do piloto (F6.3).
- F2.1: título e escopo passam a travar as dependências conforme D2; RN01 a RN04 condicionadas a D2, com exceções registradas por imagem e registro de torch, CUDA e base antes do lock (o critério 'CUDA do torch igual à base' virou registro, porque a base muda em F2.2, que depende de F2.1). Acrescentados a fixação das versões no script baixado pela URL, com critério de resolução igual ao lock; --python nos comandos; a suspensão do workflow docker antes da primeira tag, com critério de que a tag não publica imagem. O critério do --dry-run passou a comparar a URL mostrada com o cabeçalho do arquivo baixado. O comando de desenvolvimento do bench deixou de rodar o conjunto de teste. O critério da pose descreve comportamento. Dependência de D2 (F2.4) nas tasks de lock; story points de 5 para 8. Nesta rodada: F2.1.T6 retira ANTHROPIC_API_KEY dos comandos de desenvolvimento, com RN11 e o critério 15.
- F2.2: composição por D2; a Docker Space só com exceção a RN01 e RN09 (passo de publicação por Space retirado de T2). /dev/shm registrado também na t4-small; o critério de timeout exige o valor registrado em 'hf jobs inspect' e a mensagem de recusa; o critério de GPU sem CUDA passou a teste unitário, como a task de QA verifica. A task de diagnóstico passou de Visão Computacional para DevOps; os dois jobs de fumaça ficaram numa task e o registro dos JOB_IDs só na task de MLOps, com 7 tasks. Mantidos do ajuste anterior: diagnóstico sem pesos, sessão do detector em F2.3, dependência F1.1. Nesta rodada: F2.2.T4 depende de F2.6.T1 e F2.6.T2 e autentica a CLI com o token de lançamento, com RN10 e o critério 14.
- F2.3: RN04 e RN05 separam os pesos não espelhados: HSEmotion, 6DRepNet e faster-whisper vêm da origem por URL ou revisão fixa com hash; det_500m.onnx nunca vem da origem, e sem permissão de espelhar F4.3 aciona F4.7, que recebe os critérios de detector deste PBI. O critério de download ficou restrito aos pesos espelhados. Acrescentados a conferência de todos os pesos antes do primeiro quadro (o detector carrega dentro do laço e o Whisper depois do vídeo), a verificação dos pesos da transcrição sem decodificar áudio (a fixture não tem trilha de áudio), o teste do caminho de reserva 'small', o caso de detector não espelhável e o teste negativo com arquivo vazio. Comparação de saídas no CI com o vídeo licenciado (P26), execuções locais só com a fixture. As tasks de detector e de HSEmotion/6DRepNet foram fundidas (7 tasks). Mantidos do ajuste anterior: dependências F1.6, F2.2 e F2.4, task de QA, modelo 'small' no manifesto.
- F2.3, revisão de dependências (ciclo com F4.7): F4.7 saiu das dependências de F2.3 e da Feature. F2.3 fecha com o mecanismo de F2.3.T3 e os pesos permitidos; com o veto ao espelhamento de det_500m.onnx, os critérios 6 e 13 passam a F4.7 (F4.7.T5 e F4.7.T8). O critério 5 passou a exigir o registro dos demais pesos antes do veto; RN04, RN05, contexto, premissas e as tasks T3, T4 e T7 foram ajustados ao caso de veto, com comparação de saídas sobre entradas fixas em memória quando não há detector.
- F2.3.T1: deixou de levantar licença e passou a copiar para o manifesto a decisão de F4.3 registrada no ADR 0001, com 1 h (antes 3 h) e dependência de F4.3.T4. A verificação da licença do faster-whisper saiu de F2.3 e fica em F4.3 (pendência de confirmar F4.3.T1). O critério 1 passou a exigir a referência ao ADR 0001.
- F2.4: D2 recebe o conflito entre libreface e py-feat; D3 registra que a Docker Space não permite referência por digest; acrescentados critérios para a avaliação de D3 contra o digest e para as versões de Py-Feat e torch em D2; PRO descrito por periodEnd com renovação a confirmar; dependência de organização criada por Fabio para o Space de teste; nova task de consolidação, aceite e merge do ADR; story points de 3 para 5. Mantidos do ajuste anterior: SDK e acesso só para rotulagem e destino do piloto, D7 e D8.
- F2.4, nesta rodada: título, quero e contexto passam a incluir as tabelas do painel e o envio da transcrição à API da Anthropic. D7 (F2.4.T4) lista as tabelas que o painel lê (window_aggregate, event, insight, execuções liberadas de F5.6 e, na Fase 1, indicadores de F7.6) e escreve (insight_feedback), exclui transcript_segment e run_log e deixa moment e service a confirmar com o usuário; D7 também registra a decisão de Fabio sobre a exceção da P26 na Fase 0. RN11, RN12 e os critérios 6 e 7 novos; F2.4.T6 confere os critérios 2 a 12; F2.4.T4 de 4 h para 5 h.
- F2.5 da árvore dividido em F2.5 (run_id, regravação por upsert e falha no Supabase) e F2.8 (linhagem, envio ao repositório de resultados, falha do bench e comando de lançamento), pela falha de INVEST em Small e pela espera de F3.5 que só a linhagem tem.
- F2.5: a regravação é por upsert na chave única, sem apagar insight, porque insight_feedback referencia insight(id) sem ON DELETE (0001_init.sql:17), com critério de notas inalteradas; o run_id pode vir do lançamento para regravar a mesma execução; o critério de schema foi reescrito como comportamento; testes fora do HF com fixture, mock e destino local; gravação no Supabase verificada por job; falha por timeout como premissa. Disciplinas: Backend e QA.
- F2.8 (novo): linhagem com caminho e SHA-256 do vídeo; dependência de F2.3 (hash dos pesos); run_id e registro de falha do bench, inclusive retornos com código 1 sem exceção (bench.py:209,239); verificação do CSV do bench com fixture e rótulos sintéticos; task de DevOps que passa o digest por -e e o confere com 'hf jobs inspect' fora do job, porque o token dos jobs não tem permissão de Jobs; critério para o mapa de docs/poc-gate.md, que liga a task de Data Science a um critério.
- F2.6: dependências F1.1, F2.1.T6 e F2.2.T2 acrescentadas e limitadas às tasks que as usam (F2.6.T2 e F2.6.T7), porque o job de verificação precisa da guarda corrigida, da forma dos segredos e da imagem que gera a fixture; T7 descreve o comando de lançamento. Acrescentados o token de lançamento, a entrega do HF_TOKEN e da chave de serviço por '--secrets-file -' a partir do local de guarda de quem lança, o critério do token dentro do job, a aprovação do custo do projeto Supabase e as linhas de teste em service e insight_feedback. Os critérios de chave ausente e inválida passaram a execução local com a fixture, como a task de QA faz. T2 deixou de repetir a forma geral dos segredos, que fica em F2.1.T6. Mantidos do ajuste anterior: repositórios vazios, falha sem credencial, cabeçalho por tipo de chave, inventário.
- F2.6, nesta rodada: F2.6.T1 e F2.6.T2 passam a ser pré-requisito de F2.2.T4 (RN12 do PBI), e a dependência de F2.6 sobre F2.2 ficou só em F2.6.T7 (F2.2.T2). F2.6.T2 documenta a entrega da ANTHROPIC_API_KEY por '--secrets-file -' conforme D7 (2 h para 3 h), e F2.6.T6 a inclui no inventário; RN04 e RN11 e o critério 12 novos; o critério do inventário cita a chave.
- F2.7: vídeo de paridade segundo F1.3 (vídeo público de F5.1 ou, depois de F3.1, clipes 07 a 10), no lugar do vídeo licenciado de F1.6; 'vídeos diferentes' definido pelo caminho e SHA-256 do vídeo na linhagem de F2.8; digest e flavor lidos da linhagem; pedido de aprovação com duração e custo por job; dependências F2.8 e 'F3.1 ou F5.1'. Mantido do ajuste anterior: 'mesmo n' lido como n_total e n_mensuravel; script lê arquivos, sem chave de serviço fora dos jobs.
- Estratégia de fatiamento: a ordem sugerida passou a F2.6.T1 a F2.6.T6 antes de F2.2 e F2.6.T7 depois de F2.2.T2, como no ordem_sugerida da árvore (F2.6 antes de F2.2 e F2.3).
- Reconciliação, P3 revisada: D7 decide a leitura de moment sem nova consulta ao usuário ('e momentos, se o ADR de F2.4 registrar'); service passa a ficar fora do painel; o estado de revisão do insight (F7.3) entra entre as escritas. RN12 da Feature, RN11 de F2.4, critério 6 de F2.4 e as premissas foram ajustados, e a pendência sobre moment e service saiu.
- Reconciliação, vínculo entre conta e papel (revisão sobre F5.6.T2, F6.2, F7.2 e F7.8): D7 (F2.4.T4) decide, antes de F5.6, o local do vínculo e se a regra 6 vale para as contas da equipe. F2.4 ganhou RN13, um critério e um passo em F2.4.T4 (5 h para 6 h).
- Reconciliação, plano da Vercel (revisão sobre F7.2.T2): D8 registra a pendência com Fabio como responsável e aponta para a task de F5.6 movida de F7.2.T2. F2.4 ganhou RN14 e o critério da pendência passou a exigir o apontamento.
- Reconciliação, front end na Vercel (revisão sobre F5.6): nova F2.4.T8 (Front end) redige D9 com projeto, framework, método de login, proteção de deployment e validade do token de acesso, que F5.6 lê do ADR. F2.4 ganhou RN15 e um critério, passou a 8 tasks e de 5 para 8 pontos; título, quero e para citam as decisões do painel.
- Reconciliação, lock de libreface e py-feat (revisão sobre F4.1.T5 e F4.2.T1): RN01, F2.1.T2 e um critério novo de F2.1 exigem libreface==0.2.0 e a versão exata do py-feat decidida em D2, diferente de 0.6.2; D2 (F2.4 RN10, F2.4.T1 e critério 4) decide essa versão; F2.2 ganhou RN11 e o passo de F2.2.T1 que instala as ferramentas de compilação do dlib 19.24.6 na imagem com o libreface (8 h para 9 h).
- Reconciliação, IDs antigos: nova F2.1.T8 (DevOps) troca os IDs antigos pelos do Azure DevOps nos arquivos citados, depois da importação; o exemplo de CLAUDE.md:31 e CONTRIBUTING.md:20 só com a aprovação de Fabio. F2.1 ganhou RN12, dois critérios, dependências, premissas e a falha de INVEST correspondente; F2.1.T7 confere (4 h para 5 h); a Feature ganhou RN15, um critério e uma dependência técnica.
- Reconciliação, fixture (revisão sobre F1.1.T6 e F2.6): os jobs de fumaça e de verificação de F2.2, F2.3, F2.5 e F2.6 leem a fixture por URI hf://datasets/ na revisão de tests/fixtures/README.md (F1.1.T6); o docker run fora do HF gera a fixture em /dev/shm (F1.1 RN10). F2.2 RN07, RN10, os critérios 13 e 14 e F2.2.T4 foram ajustados, e o job de fumaça passa a receber só o HF_TOKEN dos jobs; F2.2.T4 e F2.6.T6 dependem de F1.1.T6; o texto da dependência de F2.6 e o contexto foram corrigidos; RN02 de F2.8 deixou de citar 'fixture gerada no contêiner'; RN03 da Feature cita a URI.
- Reconciliação, inventário de credenciais (revisões sobre F5.1.T3, F3.6.T3, F7.5.T4, F7.4.T4 e F5.6): F2.6 ganhou RN13 (segredos guardados em Jobs sem quem lance), RN14 (inventário único) e a exceção dos tokens de uso único na RN02; F2.6.T6 define os campos (validade, rotação ou revogação e id do Job) e transcreve o token de F1.1.T6 (2 h para 3 h); a Feature ganhou RN14 e RN07 cita os Jobs do piloto.
- Reconciliação, Supabase local no CI (revisão sobre F7.2.T4): F2.6.T4 cria o job de CI que sobe o Supabase local com a configuração de F1.5.T1, aplica as migrações e roda o teste de RLS, onde F5.6.T4, F5.7.T1 e F7.2.T4 acrescentam os seus; dependência de F1.5.T1; 3 h para 6 h; F2.6 ganhou RN15 e dois critérios e passou de 5 para 8 pontos; a Feature ganhou um critério e um risco.
- Reconciliação, publicação de imagem em F4, F5 e F7: F2.2.T2 documenta e testa a publicação por tag de pré-release num commit de branch, usada por F4.1.T10, F4.2.T9, F4.4.T8, F4.4.T9, F4.5.T9, F4.7.T9, F5.3.T3 e F7.4.T4 (6 h para 7 h); F2.2 ganhou RN12 e um critério; a Feature ganhou um critério.
- Reconciliação, fora de escopo e pendências: 'Políticas de RLS por perfil e JWT de papel (F7.2)' passou a 'mecanismo de papel e políticas do avaliador (F5.6 e F5.7) e dos perfis do piloto (F7.2 e F7.8)', em F2 e em F2.6, e o item sobre políticas de leitura foi fundido nele. Pendências já resolvidas nas Features detalhadas (F1.6, F3.3, F4.1, F4.2, F4.3, F4.6, F5.6, F5.8, F7.2 e F7.6) saíram; as que faltam foram reescritas com as refs atuais, inclusive F5.6.T7 no lugar de F5.6.T6.

### Premissas
- A P3 revisada pelo usuário prevalece sobre P3, P9, P10 e P11 da árvore onde falam de Space para o front end do produto: relatório, notas do critério 4, revisão e liberação de insights, sinalização de qualidade e telas por perfil ficam no painel web na Vercel. O Space fica só para a ferramenta de rotulagem (F3.3), e o envio dos vídeos do piloto vai direto ao HF (F7.1).
- A P3 revisada diz que a chave de serviço fica só nos jobs do HF. O HF Jobs lê o valor de cada segredo do ambiente de quem lança, a cada lançamento (https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets; huggingface_hub/cli/jobs.py:286), então a chave também fica guardada do lado de quem lança. A Feature trata esse local de guarda como o único fora do HF e o registra no inventário de F2.6.
- As premissas P6, P7, P16, P17, P19, P21, P24, P26, P27 e P29 da árvore continuam válidas para F2.
- A P26 continua válida: o envio da transcrição de cultos públicos à API da Anthropic depende da confirmação de Fabio, registrada em D7 do ADR 0002 (F2.4.T4). Até essa confirmação, nenhum comando documentado passa ANTHROPIC_API_KEY (F2.1.T6), e os jobs usam a heurística e o modelo de frase.
- Story points (Fibonacci) e horas das tasks são sugestões para o refinamento. A duração da sprint e a capacidade do time não estão registradas (P6).
- Toda execução no HF Jobs citada nas tasks só acontece depois da aprovação de Fabio, com flavor e timeout explícitos (P7). Nada foi executado ao escrever este backlog.
- Cada verificação em job usa uma imagem publicada por tag de release que já contém o código do PBI verificado (F2.2); por isso cada PBI que altera código e verifica em job gera uma tag nova.
- F2.2 e F2.6 dependem um do outro só no nível de task: F2.2.T4 depende de F2.6.T1 e F2.6.T2, e F2.6.T7 depende de F2.2.T2. Nenhuma dessas tasks depende das outras por outro caminho, então não há ciclo entre tasks. Num grafo por PBI o par aparece como dependência mútua, e a verificação de ciclos desse par precisa usar as tasks.
- F2.3 não depende de F4.7. F2.3 fecha com o mecanismo de F2.3.T3 e com os pesos que F4.3 permite espelhar. Com o veto de F4.3 ao espelhamento de det_500m.onnx, os critérios 6 e 13 de F2.3 passam a F4.7 (F4.7.T5 publica no manifesto o detector escolhido e F4.7.T8 verifica). Isso desfaz os ciclos F2.3→F4.7→F2.3 e F2.3→F4.7→F4.4→F2.3 encontrados na verificação do grafo (deps_check.py).
- Nesta rodada, as Features F1 a F7 detalhadas (feature_det_F1.json a feature_det_F7.json) foram lidas. F4.3.T1 lista os modelos faster-whisper medium e small e o Silero VAD embutido, então a pendência sobre o faster-whisper saiu. F4.4.T3 e F4.7.T5 ainda dependem do PBI F2.3 inteiro, e não de F2.3.T3, e F4.7 ainda não cita os critérios 6 e 13 de F2.3 (pendência para F4).
- Dedução: um job parado por timeout ou cancelado pode terminar sem executar o código de registro de falha. A documentação diz só que o job para ao atingir o timeout e deixa de ser cobrado (https://huggingface.co/docs/hub/jobs-configuration#timeout). O estado desses jobs vem do HF (F7.5).
- A criação do projeto na Vercel e o cadastro da URL e da chave pública do Supabase ficam em F5.6, o primeiro PBI que usa o painel web.
- Plano e termos de uso da Vercel para este projeto são pendência a confirmar, e não fato.
- O processo do Azure DevOps é Scrum (Epic, Feature, Product Backlog Item, Task), inferido do uso de 'PBI-' e 'TSK-' no repositório (P1).
- F2 passa a ter 8 PBIs, acima do limite de 7 filhos por nível (taskflow.md, seção 2). A divisão de F2.5 foi mantida porque o PBI de 13 pontos falhava em Small e esperava F3.5 por causa de uma só task, e cada parte entrega um passo verificável sozinho. Para voltar a 7, a opção registrada em pendências é mover F2.7 para F5, junto do seu primeiro uso em F5.3.
- Revisão não aplicada: F2.2.T1 (declarar pandas num extra de toda imagem que roda bench.py) — a resolução de .[gpu,llm] do levantamento traz pandas por sixdrepnet (req-gpu-py310.txt:201-202), então uma imagem com o extra gpu tem pandas; o critério de F2.2 que exige bench.py --help com código 0 em cada imagem detecta a falta se a composição de D2 mudar isso.
- Revisão não aplicada: F2.1, texto sugerido para o critério 1 ('o pipeline com o motor real processa um quadro com plateia') — fora do HF só a fixture sintética é permitida (P26), e ela não tem rosto (tests/fixtures/README.md:11-13). O critério descreve o comportamento da conversão da pose com arrays de um elemento, verificado pelo teste do CI com modelo falso (tests/test_pose.py:6-16).
- Revisão não aplicada: F2.6.T7 (inserir linhas de teste em service e insight_feedback com a chave de serviço dentro de um job) — as linhas são inseridas pelo editor SQL do projeto na sessão de Fabio, que não usa a chave de serviço e não exige job pago; o objetivo da revisão, ter linhas nas 8 tabelas antes da leitura com a chave pública, é atendido.
- Revisão não aplicada: F2.3, opção (b) da revisão (obter det_500m.onnx da origem sem que w600k_mbf.onnx chegue ao disco) — a origem é o buffalo_sc.zip, que contém w600k_mbf.onnx (insightface/utils/storage.py:8-10,21-36); mesmo extraindo só o detector em memória, o arquivo de reconhecimento entraria no job dentro do zip, contra RN05. Foi adotada a opção (a): sem permissão de espelhar, o detector não é carregado e F4.7 é acionado.
- Revisão não aplicada em parte: F2.5.T6 (troca de motor verificada em job no HF) — a separação por run_id não depende do motor, e F2.5 a verifica com duas execuções do motor mock para não depender dos pesos de F2.3; a execução com motor real está no job de validação de F2.8.
- Revisão não aplicada em parte: F2.2 e F2.6 (tasks de credencial do CI e de fixação do build para Docker Space) — D3 do ADR registra que a Docker Space não permite referência por digest e só pode ser escolhida com exceção declarada a RN01 e RN09; as tasks só são criadas se o ADR fizer essa escolha (pendência).
- Revisão aplicada: F2.4.T4 (lista de tabelas do painel). D7 inclui entre as escritas insight_feedback (notas do critério 4 e do pastor) e, na Fase 1, o estado de revisão do insight (F7.3). Com a P3 revisada ('e momentos, se o ADR de F2.4 registrar'), moment é decidido em D7, sem nova consulta ao usuário, e service fica fora, porque não está na lista da P3 revisada e tem o campo pregador (supabase/migrations/0001_init.sql:3-4).
- A tabela de execuções liberadas de F5.6 e os indicadores de qualidade de F7.6 não têm observação por rosto e entram na lista de D7 porque a P3 revisada põe a revisão e liberação e a sinalização de qualidade no painel (dedução). F5.6 registra a leitura da tabela de execuções liberadas como pendência com o dono da P3.
- O plano e os termos de uso da Vercel são confirmados pela task que a revisão move de F7.2.T2 para o início de F5.6. No estado atual de F5 (feature_det_F5.json), essa task ainda não existe, e F5.6 pede que o ADR registre o plano com Fabio como responsável. D8 registra a pendência com Fabio como responsável e aponta para a task de F5.6 pelo título, até a ref existir.
- As decisões do painel web (projeto, framework, método de login, proteção de deployment e validade do token de acesso) entram no ADR 0002 como D9 (F2.4.T8), porque F5.6.T1, F5.6.T2, F5.6.T3 e as premissas de F5.6 já as leem do ADR de F2.4 (Feature F5 detalhada).
- F2.1.T8 troca os IDs antigos numa só task, depois da importação, porque os IDs novos só existem depois dela e nenhuma task das Features detalhadas faz essa troca. O destino de cada ID antigo vem do campo ids_antigos dos PBIs: PBI-000D em F4.1, F4.2, F4.4 e F4.7; PBI-000H em F4.6; PBI-041 e PBI-057 em F7.2 e F7.8; PBI-103 em F2.7 e F5.4; TSK-207 em F5.4; PBI-104 em F4.4; PBI-105 em F6.1; PBI-106 em F2.2, F2.4 e F2.7.
- O modelo 'segredos a partir de quem lança' não cobre Jobs sem quem lance. No Job agendado de F7.4.T4 e no Job de origem do webhook de F7.5.T4, os segredos ficam na especificação do Job no HF, com escopo mínimo e rotação por recriação definidos em F7; F2.6 define o formato do inventário que os registra (F2.6 RN13 e RN14).

### Pendências para sincronizar
- Item pai: ID do épico no Azure DevOps (não informado).
- Area Path, Iteration Path e Responsável da Feature e dos 8 PBIs.
- Campo Activity das tasks: mapear as disciplinas usadas (Backend, QA, DevOps, MLOps, Visão Computacional, Data Science, Governança e Privacidade e Front end) para os valores aceitos no processo do projeto.
- Registrar a tabela ID antigo → ID novo gerada pela importação e entregá-la a F2.1.T8.
- Criar no Azure DevOps o PBI novo F2.8. As referências que citavam F2.5 para linhagem ou repositório de resultados já passaram a F2.8 em F4 (F4.4, F4.5, F4.6 e F4.7). Pela revisão, faltam F5.4 (T4), F5.5.T2, F5.7.T4, F6.1 (T1 e T2), F7.1 e F7.7 (T4), e também F5.6 (critério 9 e F5.6.T7, que citam 'registro de linhagem de F2.5'). F7.4.T4, F7.5 e F7.6 mantêm F2.5, porque o assunto é run_id ou falha no Supabase.
- Atualizar F5.6: criar a task que confirma o plano e os termos de uso da Vercel (movida de F7.2.T2), antes de F5.6.T1, e informar a ref para D8 do ADR 0002 (F2.4.T4); F5.6.T1, F5.6.T2 e F5.6.T3 leem de D9 (F2.4.T8) o framework, a proteção de deployment, o método de login e a validade do token, e F5.6.T3 lê de D7 o local do vínculo entre conta e papel.
- Atualizar F6.2, F7.2 e F7.8: o local do vínculo entre conta e papel e a aplicação da regra 6 às contas da equipe são decididos em D7 (F2.4.T4); F6.2 só confirma ou ajusta, e F7.2 (dependências e RN06) e F7.8 (dependências e RN06) citam D7 no lugar de F6.2.
- Atualizar F7.2 (RN03): D7 deixa transcript_segment, run_log e service fora do painel (P3 revisada); uma exceção da matriz de F7.2.T1 para essas tabelas exige nova decisão do usuário.
- Atualizar F3.3 (F3.3.T1) e F3.6 (F3.6.T3 e F3.6.T5): registrar o token de leitura do Space e o token de escrita de uso único no inventário de F2.6.T6 (RN14 da Feature); hoje F3.6.T3 registra só no dataset card.
- Atualizar F5.6.T4, F5.7.T1 e F7.2.T4: os testes de banco e a seed rodam no job de CI com o Supabase local criado em F2.6.T4.
- Atualizar F4 (F4.1.T10, F4.2.T9, F4.4.T8, F4.4.T9, F4.5.T9, F4.7.T9 e F4.6.T7), F5 (F5.3.T3, F5.4.T3 e F5.6.T7) e F7 (F7.4.T4 e a task de release do piloto em F7.7): a publicação por tag de pré-release ou de release segue o procedimento documentado em F2.2.T2.
- Atualizar F5.4.T4, F5.5.T3 e F5.6.T7 (antes F5.6.T6): dependem da decisão de D7 sobre a exceção da P26 (F2.4.T4) e da entrega da ANTHROPIC_API_KEY documentada em F2.6.T2.
- Atualizar F4.4 e F4.7: F4.4.T3 e F4.7.T5 passam a depender de F2.3.T3 (mecanismo), e não do PBI F2.3 inteiro. Com o veto de F4.3 ao espelhamento de det_500m.onnx, F4.7 recebe os critérios 6 e 13 de F2.3 (sessão do detector do manifesto com CUDAExecutionProvider em job t4-small e teste da regra 2 com o detector do manifesto): F4.7.T5 publica no manifesto o detector escolhido e F4.7.T8 verifica.
- Atualizar F1.6: se F4.3 vetar o espelhamento do detector, deixar de carregar o SCRFD da origem quando F2.3 for concluído.
- Atualizar F7.5: falha por timeout ou término forçado é lida do estado do job no HF (premissa da Feature).
- Atualizar o grafo usado na verificação de ciclos (deps_check.py): retirar F4.7 das dependências de F2.3; registrar o par F2.2 e F2.6 no nível de task (F2.2.T4 → F2.6.T1 e F2.6.T2; F2.6.T7 → F2.2.T2); acrescentar F2.2.T4 → F1.1.T6, F2.6.T6 → F1.1.T6 e F2.6.T4 → F1.5.T1.
- Obter de Fabio a decisão sobre a exceção da P26 na Fase 0 (F2.4.T4).
- Confirmar com o usuário a leitura, pelo painel, da tabela de execuções liberadas de F5.6 na Fase 0 (premissa de D7).
- Confirmar com Fabio a renovação da assinatura PRO (periodEnd 2026-10-01).
- Se o ADR 0002 escolher Docker Space com exceção a RN01 e RN09, criar em F2.2 e F2.6 as tasks de credencial do CI (Trusted Publishers) e de fixação do build.
- Se o time quiser voltar a 7 PBIs em F2, avaliar mover F2.7 para F5, junto de F5.3.

## Preview — PBI F2.1 (novo) · Mesclar o PR #3, travar as dependências conforme a composição de imagem do ADR 0002 e fixar por tag o caminho uv de desenvolvimento

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Mesclar o PR #3, travar as dependências conforme a composição de imagem do ADR 0002 e fixar por tag o caminho uv de desenvolvimento |
| Tipo | Product Backlog Item |
| Pai | F2 |
| Tags | F2; dependências; lock; HF Jobs; DevOps; MLOps |
| Estimativa | 8 pts (sugestão); tasks: 35 h |
| Dependências | Aprovação de Fabio (dono do repositório) para tirar o PR #3 de rascunho e mesclá-lo, F2.4, decisão D2 (composição das imagens), antes das tasks de lock F2.1.T2 e F2.1.T3; o restante do PBI corre em paralelo a F2.4, Importação dos itens da árvore no Azure DevOps, que gera os IDs novos, só para F2.1.T8, Aprovação de Fabio para trocar o exemplo de CLAUDE.md:31 e CONTRIBUTING.md:20, só para esse passo de F2.1.T8 |
| Substitui | PR #3 (commit 5176bc3; o título cita PBI-105, que na árvore corresponde ao gate em F6.1) |

#### Descrição

Como integrante do time de ML e visão computacional que roda jobs de desenvolvimento no HF Jobs  
Quero que main contenha a correção da pose do PR #3, que as dependências fiquem travadas num lock versionado com uma versão por pacote em cada imagem de motor, e que o caminho 'hf jobs uv run' use script e pacote da mesma tag de release, com a versão de Python do lock, e que o código e a documentação citem os IDs do Azure DevOps no lugar dos IDs antigos  
Para que dois jobs de desenvolvimento lançados em dias diferentes instalem as mesmas versões e não parem no primeiro quadro com plateia pelo erro de conversão da pose, e que as referências no código levem a itens que existem no Azure DevOps

**Contexto:** O PR #3 corrige em reacao/pose.py a conversão de pitch e yaw, que no NumPy 2.4.6 levanta TypeError no primeiro quadro com plateia. Ele está aberto como rascunho, com mergeable_state 'clean' e um commit (5176bc3) que não está em origin/main (PR #3; git merge-base, 2026-09-23). O teste do PR usa um modelo falso que devolve arrays de forma (1,), como o SixDRepNet (tests/test_pose.py:6-16). Os cabeçalhos PEP 723 instalam reacao por git+https sem commit nem tag (processar_culto.py:4; bench.py:3), e os comandos baixam o script de main por raw.githubusercontent.com (docs/hf-jobs.md:18,27). Um arquivo não pode conter o SHA do próprio commit, por isso a fixação é por tag. Com metadados inline, o uv ignora as dependências do projeto, e 'uv lock --script' cria o lock ao lado do script (https://docs.astral.sh/uv/guides/scripts/); um job que baixa o script pela URL não recebe esse arquivo (dedução). Não há lock: uv.lock está no .gitignore (.gitignore:223), e o pyproject só declara limites inferiores (pyproject.toml:6-24). A resolução de .[gpu,llm] para Python 3.10 traz onnxruntime junto com onnxruntime-gpu, opencv-python junto com opencv-python-headless e torch 2.14.0 com runtime CUDA 13, enquanto a base da imagem é CUDA 12.4.1 (uv pip compile do levantamento; Dockerfile:3). Os extras dos motores não cabem numa mesma resolução: libreface 0.2.0 fixa torch==2.0.0, opencv-python==4.10.0.84 e mediapipe==0.10.5 (https://pypi.org/pypi/libreface/0.2.0/json), py-feat 2.1.3 exige torch>=2.5 (https://pypi.org/pypi/py-feat/2.1.3/json), e a resolução de .[gpu,pyfeat,libreface] cai para py-feat 0.6.1 e torch 2.0.0 com pacotes nvidia-*-cu11, com onnxruntime e onnxruntime-gpu e três pacotes opencv (lock310.txt do levantamento, linhas 205-230, 238-253, 296 e 392). O uv aceita declarar extras em conflito (https://docs.astral.sh/uv/concepts/projects/config/#conflicting-dependencies), e a composição das imagens é a decisão D2 do ADR 0002 (F2.4). A versão de Python varia: 3.12 na imagem padrão do uv no HF (huggingface_hub/_jobs_api.py:96), 3.11 no venv local e nenhuma fixada no CI (.github/workflows/ci.yml:8-9). O CI instala opencv-python-headless e numpy sem versão (.github/workflows/ci.yml:9). Os comandos documentados passam segredos na forma NOME=valor (docs/hf-jobs.md:14-17,26), que a CLI desaconselha com aviso (huggingface_hub/cli/_cli_utils.py:831-838), e não usam o separador '--' (https://huggingface.co/docs/hub/jobs-configuration#passing-arguments). A docstring e o onprem.md escrevem '--secret' no singular, opção que a CLI não declara (processar_culto.py:12-13; docs/onprem.md:68). O comando documentado do bench aponta --corpus para a raiz do dataset, embora os vídeos estejam em pib/ e o bench não busque em subpastas (docs/hf-jobs.md:25-29; bench.py:206), e os 19 clipes de teste da PIB são a medição do gate (docs/poc-gate.md:46-48). O --dry-run de 'hf jobs uv run' mostra script, argumentos, imagem, flavor, python (só quando informado), timeout, env e os segredos mascarados, sem as dependências do cabeçalho (huggingface_hub/cli/jobs.py:365-402,1331-1349). O workflow docker dispara em push de tag v* e publica as tags latest e a da ref (.github/workflows/docker.yml:2-4,22-25). O comando documentado de um culto passa ANTHROPIC_API_KEY (docs/hf-jobs.md:16); com a chave, a transcrição vai à API da Anthropic (reacao/moments.py:48-61), envio que depende da confirmação de Fabio (P26), registrada em D7 do ADR 0002 (F2.4). Na Feature F4 detalhada, F4.1.T5 saiu e F4.2.T1 só confere a API na versão que este PBI fixa, para que o lock não mude depois que F2.2 publicar os digests; a 0.6.2 do py-feat fica fora das opções pela regra 2 (F4.2). O código e a documentação citam IDs antigos do backlog: PBI-000D (reacao/providers/pyfeat.py:1, reacao/providers/libreface.py:2 e reacao/detect.py:28), PBI-000H (bench.py:5), PBI-041/PBI-057 (supabase/migrations/0001_init.sql:21), PBI-103/TSK-207 (docs/onprem.md:7), PBI-103 e PBI-106 (docs/onprem.md:55), PBI-105 (docs/poc-gate.md:1) e o exemplo PBI-104 (CLAUDE.md:31; CONTRIBUTING.md:20). Os IDs novos só existem depois da importação dos itens no Azure DevOps. tests/test_schema.py ignora comentários das migrações (tests/test_schema.py:11).

**Regras de negócio:**
- RN01 – O lock é versionado e cobre os extras gpu, llm, pyfeat, libreface e dev, com libreface==0.2.0 e a versão exata do py-feat decidida em D2 do ADR 0002, diferente de 0.6.2 (F4.2). A forma do lock segue D2: um lock com os extras pyfeat e libreface declarados em conflito no uv, ou um lock por imagem de motor. F4.1 e F4.2 só conferem essas versões.
- RN02 – Cada conjunto de extras instalado numa mesma imagem tem uma única versão por pacote.
- RN03 – Em cada imagem com o extra gpu, o módulo onnxruntime vem só do pacote onnxruntime-gpu e só um pacote opencv é instalado. Quando um pacote fixado por um motor impedir isso, a exceção fica registrada para aquela imagem, com o pacote que a exige.
- RN04 – Para cada imagem de D2, a versão do torch travada, a versão principal de CUDA do torch e a base CUDA que F2.2 vai usar ficam registradas antes de gerar o lock; F2.2 aplica a base registrada.
- RN05 – A versão de Python é a mesma no lock, no CI e no caminho uv de desenvolvimento.
- RN06 – A URL do script e a referência git+https do cabeçalho PEP 723 apontam para a mesma tag de release. Nenhum comando documentado aponta para main.
- RN07 – O script baixado pela URL da tag resolve as mesmas versões do lock.
- RN08 – Comandos documentados passam segredos só pelo nome ou por --secrets-file, usam '--' antes dos argumentos do script, têm --flavor, --timeout e --python explícitos e não passam arquivo local como argumento, porque 'hf jobs uv run' copia arquivo local para o bucket jobs-artifacts (P27).
- RN09 – O caminho de desenvolvimento não roda o bench sobre o conjunto de teste; a medição do gate fica no caminho por 'hf jobs run' com digest (F4.6). Um comando de desenvolvimento do bench só aparece se apontar para vídeos que F1.3 permite em desenvolvimento.
- RN10 – Criar tag de release não publica imagem enquanto F2.2 não refizer o workflow docker.
- RN11 – Os comandos de desenvolvimento não passam ANTHROPIC_API_KEY. F2.6.T2 acrescenta a chave ao procedimento de lançamento se o ADR 0002 registrar a confirmação de Fabio sobre a exceção da P26.
- RN12 – Depois da importação no Azure DevOps, os IDs antigos citados no código e na documentação são trocados pelo ID novo do PBI correspondente da árvore. Na migração já aplicada, só a linha de comentário muda. O exemplo de CLAUDE.md:31 e CONTRIBUTING.md:20 só muda com a aprovação de Fabio registrada no PR.

**Fora de escopo:**
- Construção e publicação da imagem, reativação da publicação por tag e caminho do gate por 'hf jobs run' (F2.2, F2.4)
- Comando do bench sobre o conjunto de teste (F4.6)
- Pesos com revisão e hash (F2.3)
- CI com motores reais (F1.6)
- Caminho dos rótulos no dataset e leitura por revisão (F3.5)
- Correção de tools/rodar_teste.sh:59-61, que aponta o clipe 11 para o critério 5 (F1.3)
- Entrega da ANTHROPIC_API_KEY aos jobs, que depende de D7 (F2.6.T2)
- Execução de qualquer job pago
- Troca de IDs antigos em mensagens de commit e títulos de PR já existentes, como o do PR #3, que não são reescritos

#### Critérios de aceite

- Em main, com o NumPy do lock, a pose converte em números o pitch e o yaw que o modelo devolve como arrays de um elemento, sem TypeError, e o CI de main aprova esse caso.
- O lock está versionado no repositório, e o .gitignore não o ignora.
- Para cada conjunto de extras que uma imagem de D2 instala, o lock resolve uma única versão de cada pacote.
- O lock fixa libreface==0.2.0 e a versão do py-feat registrada em D2, e nenhuma resolução do lock contém py-feat 0.6.2.
- Na resolução de cada imagem com o extra gpu, só onnxruntime-gpu fornece onnxruntime e só um pacote opencv aparece, ou a exceção está registrada com o pacote que a exige.
- Para cada imagem de D2, CONTRIBUTING.md registra a versão do torch, a versão principal de CUDA do torch e a base CUDA que F2.2 vai usar.
- Um PR que altera pyproject.toml sem atualizar o lock faz o CI falhar com mensagem que cita o lock.
- A versão de Python é a mesma no lock, no log do CI e no campo python do --dry-run de cada comando de desenvolvimento.
- A lista de pacotes e versões resolvida para cada script baixado da URL da tag é igual à do lock para os mesmos extras.
- Para cada comando de desenvolvimento, a URL do script mostrada no --dry-run e a referência git+https no cabeçalho do arquivo baixado dessa URL apontam para a mesma tag.
- Cada comando documentado tem --flavor e --timeout explícitos, e o --dry-run mostra o timeout pedido.
- O --dry-run de cada comando documentado roda sem o aviso da CLI sobre segredo com valor na linha de comando.
- Nenhum texto em docs/hf-jobs.md, docs/onprem.md e na docstring de processar_culto.py contém '--secret' no singular.
- Nenhum comando de desenvolvimento de docs/hf-jobs.md roda o bench sobre os clipes do conjunto de teste.
- Criar a tag de F2.1 não gera execução do workflow docker nem imagem em registro.
- Nenhum comando de desenvolvimento documentado passa ANTHROPIC_API_KEY.
- Em reacao/providers/pyfeat.py, reacao/providers/libreface.py, reacao/detect.py, bench.py, supabase/migrations/0001_init.sql, docs/onprem.md e docs/poc-gate.md, nenhum ID antigo aparece, cada referência cita o ID novo do PBI correspondente, e o diff de 0001_init.sql muda só a linha de comentário.
- CLAUDE.md:31 e CONTRIBUTING.md:20 só mudam se o PR registrar a aprovação de Fabio; sem ela, continuam iguais.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F2.1.T1 | DevOps | Mesclar o PR #3 em main | 1 | Aprovação de Fabio |
| F2.1.T2 | MLOps | Resolver os conflitos de pacotes por imagem de D2 e registrar torch, CUDA e base de cada imagem | 10 | F2.4 (decisão D2) |
| F2.1.T3 | MLOps | Gerar o lock, fixar as versões nos scripts baixados pela URL e comparar as resoluções | 6 | F2.1.T2 |
| F2.1.T4 | DevOps | Fazer o CI verificar e instalar a partir do lock | 4 | F2.1.T3 |
| F2.1.T5 | DevOps | Suspender a publicação por tag, criar a tag de release e apontar script e pacote para ela | 3 | F2.1.T1, F2.1.T3 |
| F2.1.T6 | DevOps | Reescrever os comandos de desenvolvimento de docs/hf-jobs.md, retirar a ANTHROPIC_API_KEY e corrigir '--secret' | 4 | F2.1.T5 |
| F2.1.T7 | QA | Verificar os critérios de aceite de F2.1 | 5 | F2.1.T1, F2.1.T2, F2.1.T3, F2.1.T4, F2.1.T5, F2.1.T6, F2.1.T8 |
| F2.1.T8 | DevOps | Trocar as referências aos IDs antigos pelos IDs novos do Azure DevOps no código e na documentação | 2 | Importação dos itens da árvore no Azure DevOps, que gera os IDs novos, Aprovação de Fabio, só para CLAUDE.md:31 e CONTRIBUTING.md:20 |

<details><summary>F2.1.T1 · [DevOps] Mesclar o PR #3 em main</summary>

**Objetivo:** main com a correção da conversão da pose e o teste tests/test_pose.py.

**Passos previstos:**
1. Obter a aprovação de Fabio e tirar o PR #3 de rascunho.
2. Atualizar o branch com main, se houver commits novos.
3. Confirmar ruff check e pytest verdes no CI do PR.
4. Mesclar e confirmar o CI verde em main.

**Definição de pronto:** Commit da correção em main e execução do CI de main aprovada com tests/test_pose.py.

**Dependências:** Aprovação de Fabio

**Estimativa sugerida:** 1 h (sugestão; validar com o time)

</details>

<details><summary>F2.1.T2 · [MLOps] Resolver os conflitos de pacotes por imagem de D2 e registrar torch, CUDA e base de cada imagem</summary>

**Objetivo:** Resolução com uma versão por pacote em cada imagem de D2, com libreface==0.2.0 e a versão exata do py-feat de D2, sem onnxruntime de CPU nem opencv duplicado (ou com a exceção registrada), e registro de torch, CUDA e base por imagem.

**Passos previstos:**
1. Ler a decisão D2 do ADR 0002 (uma imagem por motor ou imagem com os três motores e a versão de Py-Feat que ela aceita).
2. Fixar libreface==0.2.0 e a versão exata do py-feat decidida em D2 (diferente de 0.6.2) nos extras libreface e pyfeat do pyproject, conforme a imagem de cada um.
3. Declarar no pyproject os extras pyfeat e libreface em conflito no uv (https://docs.astral.sh/uv/concepts/projects/config/#conflicting-dependencies), ou preparar um lock por imagem, conforme D2.
4. Listar pela árvore de dependências do uv quais pacotes puxam onnxruntime e opencv e aplicar no pyproject a forma de impedir o onnxruntime de CPU e o opencv duplicado (por exemplo, sobrescrita de dependência do uv), registrando as exceções que um pino de motor impuser, como opencv-python==4.10.0.84 do libreface.
5. Para cada imagem, escolher a origem do torch e registrar em CONTRIBUTING.md a versão do torch, a versão principal de CUDA do torch e a base CUDA que F2.2 vai usar.
6. Fixar a versão de Python em requires-python e na configuração do uv.

**Definição de pronto:** Resolução de cada imagem de D2 com uma versão por pacote, libreface==0.2.0 e o py-feat de D2 fixados, exceções registradas e registro de torch, CUDA e base em CONTRIBUTING.md.

**Dependências:** F2.4 (decisão D2)

**Estimativa sugerida:** 10 h (sugestão; validar com o time)

</details>

<details><summary>F2.1.T3 · [MLOps] Gerar o lock, fixar as versões nos scripts baixados pela URL e comparar as resoluções</summary>

**Objetivo:** Lock versionado e scripts cuja resolução, baixados pela URL, é igual ao lock.

**Passos previstos:**
1. Retirar uv.lock do .gitignore (linha 223).
2. Gerar o lock conforme F2.1.T2.
3. Decidir e aplicar como o script baixado pela URL fixa as versões (por exemplo, versões exatas do lock no cabeçalho PEP 723 de processar_culto.py e bench.py), registrando a decisão e o procedimento de atualização do lock em CONTRIBUTING.md.
4. Comparar a resolução de cada script (uv export --script) com o lock para os mesmos extras.

**Definição de pronto:** Lock em main e comparação sem diferença entre a resolução de cada script e o lock.

**Dependências:** F2.1.T2

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F2.1.T4 · [DevOps] Fazer o CI verificar e instalar a partir do lock</summary>

**Objetivo:** CI que reprova lock desatualizado e instala as versões travadas.

**Passos previstos:**
1. Fixar a versão de Python no setup-uv.
2. Acrescentar passo que falha quando o lock não corresponde ao pyproject.
3. Trocar a instalação avulsa de .github/workflows/ci.yml:9 pela instalação a partir do lock.
4. Abrir um PR de teste que muda o pyproject sem atualizar o lock.

**Definição de pronto:** CI verde com o lock e PR de teste reprovado com mensagem que cita o lock.

**Dependências:** F2.1.T3

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F2.1.T5 · [DevOps] Suspender a publicação por tag, criar a tag de release e apontar script e pacote para ela</summary>

**Objetivo:** URL do script e referência git+https do cabeçalho na mesma tag, sem imagem publicada pela tag.

**Passos previstos:**
1. Desativar em .github/workflows/docker.yml o gatilho de tag e o disparo manual até F2.2.T2, porque o workflow atual publica :latest a cada tag v* (docker.yml:2-4,22-25).
2. Definir o padrão da tag e atualizar a versão em pyproject.toml:3.
3. Trocar a referência git+https dos cabeçalhos de processar_culto.py e bench.py pela tag.
4. Criar a tag no commit que contém esses cabeçalhos e conferir que o workflow docker não rodou.
5. Documentar o procedimento de release: cabeçalho atualizado antes da tag.

**Definição de pronto:** O script baixado pela URL raw na tag tem cabeçalho que referencia a mesma tag, e a aba de execuções do workflow docker não mostra execução para a tag.

**Dependências:** F2.1.T1, F2.1.T3

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F2.1.T6 · [DevOps] Reescrever os comandos de desenvolvimento de docs/hf-jobs.md, retirar a ANTHROPIC_API_KEY e corrigir &#x27;--secret&#x27;</summary>

**Objetivo:** Comandos de desenvolvimento com tag, Python do lock, segredos por nome ou por --secrets-file, '--', flavor e timeout, sem ANTHROPIC_API_KEY e sem medir o conjunto de teste.

**Passos previstos:**
1. Marcar a seção como caminho de desenvolvimento e apontar o caminho do gate para o ADR 0002 e F4.6.
2. Usar a URL na tag, --python com a versão do lock, segredos pelo nome ou por --secrets-file, '--' antes dos argumentos do script, --flavor e --timeout explícitos.
3. Retirar ANTHROPIC_API_KEY dos comandos de desenvolvimento (docs/hf-jobs.md:16) e registrar que F2.6.T2 a acrescenta ao procedimento se o ADR 0002 aceitar a exceção da P26.
4. Retirar da seção de desenvolvimento o comando do bench sobre o dataset; manter um comando do bench só se apontar para vídeos que F1.3 permite em desenvolvimento.
5. Corrigir '--secret' em processar_culto.py:12-13 e docs/onprem.md:68.
6. Rodar o --dry-run de cada comando.

**Definição de pronto:** O --dry-run de cada comando termina sem erro e sem o aviso de segredo com valor na linha de comando, mostra python igual ao do lock e não lista ANTHROPIC_API_KEY entre os segredos.

**Dependências:** F2.1.T5

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F2.1.T7 · [QA] Verificar os critérios de aceite de F2.1</summary>

**Objetivo:** Evidência de cada critério de aceite anexada ao PBI.

**Passos previstos:**
1. Conferir o CI de main com o caso da pose.
2. Conferir no lock libreface==0.2.0, a versão do py-feat de D2 e a ausência de py-feat 0.6.2.
3. Inspecionar o lock por imagem: versões únicas, provedores de onnxruntime, pacotes opencv e exceções registradas; conferir o registro de torch, CUDA e base em CONTRIBUTING.md.
4. Conferir o PR de teste com lock desatualizado reprovado e a versão de Python no log do CI.
5. Baixar cada script da URL da tag, ler a referência git+https do cabeçalho e comparar a resolução dele com o lock.
6. Rodar o --dry-run de cada comando documentado (URL, python, timeout, aviso de segredo, lista de segredos sem ANTHROPIC_API_KEY) e buscar '--secret' no singular nos arquivos citados.
7. Conferir que nenhum comando de desenvolvimento roda o bench sobre o conjunto de teste.
8. Conferir que a tag de F2.1 não tem execução do workflow docker e que o registro não recebeu imagem.
9. Buscar 'PBI-' e 'TSK-' nos arquivos de F2.1.T8, conferir o ID novo de cada referência contra a tabela da importação, o diff de 0001_init.sql e, se CLAUDE.md e CONTRIBUTING.md mudaram, a aprovação de Fabio no PR.

**Definição de pronto:** Checklist dos 18 critérios com evidência (link do CI, trecho do lock, cabeçalho baixado, saída do --dry-run, resultado da busca por IDs antigos) anexada ao PBI.

**Dependências:** F2.1.T1, F2.1.T2, F2.1.T3, F2.1.T4, F2.1.T5, F2.1.T6, F2.1.T8

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F2.1.T8 · [DevOps] Trocar as referências aos IDs antigos pelos IDs novos do Azure DevOps no código e na documentação</summary>

**Objetivo:** Código e documentação citam os IDs gerados na importação dos itens no Azure DevOps, sem ID antigo, e o exemplo de CLAUDE.md e CONTRIBUTING.md só muda com a aprovação de Fabio.

**Passos previstos:**
1. Montar a tabela ID antigo → ID novo com os IDs gerados na importação e o campo ids_antigos dos PBIs: PBI-000D em reacao/providers/pyfeat.py:1 → F4.2, em reacao/providers/libreface.py:2 → F4.1 e em reacao/detect.py:28 (detecção por ladrilhos) → F4.7; PBI-000H em bench.py:5 → F4.6; PBI-041/PBI-057 em supabase/migrations/0001_init.sql:21 (RLS e perfis pastor, mídia e DPO) → F2.6 (RLS), F7.2 e F7.8 (perfis); PBI-103/TSK-207 em docs/onprem.md:7 → F5.4; PBI-103 e PBI-106 em docs/onprem.md:55 (teste de paridade) → F2.7; PBI-105 em docs/poc-gate.md:1 → F6.1.
2. Trocar os IDs nesses arquivos. Em supabase/migrations/0001_init.sql, migração já aplicada, alterar só a linha de comentário e conferir no diff que nenhuma instrução SQL mudou.
3. Propor a Fabio o novo exemplo para CLAUDE.md:31 e CONTRIBUTING.md:20, no formato dos IDs gerados, e trocar os dois só com a aprovação dele registrada no PR.
4. Buscar 'PBI-' e 'TSK-' no repositório e registrar o resultado no PR.
5. Rodar ruff check e pytest e abrir o PR citando o ID novo de F2.1.

**Definição de pronto:** PR mesclado; a busca por 'PBI-' e 'TSK-' não encontra ID antigo nos arquivos de código e documentação citados, cada referência cita o ID novo do PBI correspondente, o diff de 0001_init.sql muda só o comentário, e CLAUDE.md e CONTRIBUTING.md só mudaram se o PR registra a aprovação de Fabio.

**Dependências:** Importação dos itens da árvore no Azure DevOps, que gera os IDs novos, Aprovação de Fabio, só para CLAUDE.md:31 e CONTRIBUTING.md:20

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- PR #3 (GitHub, estado open, draft, mergeable_state clean, 2026-09-23)
- git merge-base --is-ancestor 5176bc3 origin/main (falso, 2026-09-23)
- tests/test_pose.py:6-16
- processar_culto.py:1-14
- bench.py:1-4,206
- .gitignore:223
- pyproject.toml:3-24
- Dockerfile:3
- .github/workflows/ci.yml:8-11
- .github/workflows/docker.yml:2-4,22-25
- docs/hf-jobs.md:13-30
- docs/onprem.md:68
- docs/poc-gate.md:46-48
- reacao/moments.py:48-61
- premissa P26
- huggingface_hub/_jobs_api.py:96 (instalado)
- huggingface_hub/cli/jobs.py:186-256,365-402,1331-1349 e cli/_cli_utils.py:831-838 (instalados)
- https://pypi.org/pypi/libreface/0.2.0/json
- https://pypi.org/pypi/py-feat/2.1.3/json
- lock310.txt do levantamento (resolução de .[gpu,pyfeat,libreface] para Python 3.10), linhas 205-230, 238-253, 296 e 392
- uv pip compile de .[gpu,llm] (levantamento, mapa_infra.jsonl)
- https://docs.astral.sh/uv/guides/scripts/
- https://docs.astral.sh/uv/concepts/projects/config/#conflicting-dependencies
- https://huggingface.co/docs/hub/jobs-configuration#passing-arguments
- Busca por 'PBI-' e 'TSK-' no repositório (2026-09-23): reacao/providers/pyfeat.py:1, reacao/providers/libreface.py:2, reacao/detect.py:28, bench.py:5, supabase/migrations/0001_init.sql:21, docs/onprem.md:7,55, docs/poc-gate.md:1, CLAUDE.md:31, CONTRIBUTING.md:20
- tests/test_schema.py:9-12
- Campo ids_antigos dos PBIs das Features F1 a F7 detalhadas
- Feature F4 detalhada: F4.1.T5 retirada, F4.2.T1 e pendência para F2.1 (libreface==0.2.0 e py-feat exato, diferente de 0.6.2)

#### Verificação INVEST: pontos que falharam
- Independent: as tasks de lock (F2.1.T2 e F2.1.T3) esperam a decisão D2 de F2.4; as demais tasks correm em paralelo.
- Independent: F2.1.T8 espera a importação dos itens no Azure DevOps, feita fora do time de desenvolvimento.

#### Premissas
- A versão de Python do lock é a da imagem base (Ubuntu 22.04, Python 3.10, dedução pela versão padrão da distribuição), ou a que F2.1.T2 registrar se a base de alguma imagem mudar.
- O caminho 'hf jobs uv run' fica só para desenvolvimento, como proposto para o ADR 0002 (F2.4). Se o ADR decidir diferente, a fixação por tag continua válida.
- O padrão de nome da tag de release é decisão deste PBI (P24). O gatilho de tag do workflow docker fica desativado de F2.1.T5 até F2.2.T2.
- A forma de fixar as versões no script baixado pela URL é decidida em F2.1.T3; a sugestão é gerar no cabeçalho PEP 723 as versões exatas do lock.
- O critério 1 descreve o comportamento da conversão da pose; fora do HF só a fixture sintética é permitida (P26), e ela não tem rosto.
- A retirada da ANTHROPIC_API_KEY dos comandos de desenvolvimento segue a P26: até a confirmação de Fabio registrada em D7, os jobs rodam sem a chave. F2.6.T2 a devolve ao procedimento se a exceção for aceita.
- O PBI tem 18 critérios. Se o refinamento julgar que não cabe numa sprint, a divisão sugerida é (a) PR #3, lock e CI, (b) tag, fixação dos scripts e comandos de desenvolvimento e (c) troca dos IDs antigos (F2.1.T8), que espera a importação no Azure DevOps.
- Disciplinas: DevOps, MLOps e QA, como previsto na árvore.
- Story points e horas são sugestão, a validar no refinamento.
- O ID novo de cada referência segue o PBI da árvore que trata daquele trecho: F4.2 em pyfeat.py, F4.1 em libreface.py, F4.7 em detect.py (detecção por ladrilhos), F4.6 em bench.py, F2.6 (RLS), F7.2 e F7.8 (perfis) em 0001_init.sql, F5.4 em docs/onprem.md:7, F2.7 em docs/onprem.md:55 e F6.1 em docs/poc-gate.md:1 (campo ids_antigos dos PBIs).
- O formato do novo exemplo de CLAUDE.md e CONTRIBUTING.md depende dos IDs gerados na importação; o texto é proposto a Fabio em F2.1.T8.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável.
- Item pai: Feature F2 (ID no Azure DevOps).
- Vincular o PR #3 ao PBI.
- Confirmar a versão de Python com o time antes de gerar o lock.
- Registrar a decisão D2 do ADR 0002 antes de iniciar F2.1.T2.
- Registrar a tabela ID antigo → ID novo gerada pela importação antes de iniciar F2.1.T8.

## Preview — PBI F2.2 (novo) · Construir e publicar por digest a imagem ou as imagens de motor do ADR 0002 e validá-las em jobs de fumaça com a fixture sintética

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Construir e publicar por digest a imagem ou as imagens de motor do ADR 0002 e validá-las em jobs de fumaça com a fixture sintética |
| Tipo | Product Backlog Item |
| Pai | F2 |
| Tags | F2; Docker; imagem; HF Jobs; DevOps; MLOps; PBI-106 |
| Estimativa | 8 pts (sugestão); tasks: 35 h |
| Dependências | F2.1 (lock, base registrada por imagem e tag), F2.4 (ADR 0002: composição D2 e registro D3), F1.1 (guarda corrigida antes de qualquer job; fixture sintética no dataset por revisão, F1.1.T6, antes de F2.2.T4), F2.6.T1 e F2.6.T2 (token de lançamento e procedimento de lançamento), antes de F2.2.T4; o restante de F2.6 não é pré-requisito deste PBI, Aprovação de Fabio para os jobs cpu-basic e t4-small |
| Substitui | PBI-106 (parte: imagem publicada e usada nos dois ambientes; a paridade está em F2.7) |

#### Descrição

Como integrante do time de DevOps e MLOps que prepara os jobs do gate  
Quero a imagem ou as imagens de motor decididas em D2 do ADR 0002 publicadas por tag de release, com digest registrado e com os motores hsemotion, LibreFace e Py-Feat distribuídos conforme D2, validadas no HF Jobs e fora dele com a fixture sintética  
Para que os jobs do gate e do piloto e a execução fora do HF usem os mesmos artefatos, e que o tamanho de /dev/shm na cpu-basic e na t4-small, o timeout aceito e a disponibilidade de CUDA sejam conhecidos antes do primeiro culto inteiro

**Contexto:** O Dockerfile usa a base nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04 por tag, sem digest, instala só .[gpu,llm], copia reacao/, processar_culto.py e bench.py e fixa o ENTRYPOINT em processar_culto.py (Dockerfile:3-12). O workflow docker.yml publica as tags latest e a do ref no GHCR, só por tag v* ou disparo manual, e nunca rodou; o repositório não tem tag (.github/workflows/docker.yml:1-25; GitHub list_tags vazio). F2.1 desativa esse gatilho até este PBI refazer o workflow. Os três motores não cabem numa mesma resolução sem rebaixar o Py-Feat para 0.6.1 e o torch para 2.0.0 com runtime CUDA 11 (https://pypi.org/pypi/libreface/0.2.0/json; https://pypi.org/pypi/py-feat/2.1.3/json; lock310.txt do levantamento, linhas 296 e 392), por isso a composição segue D2 do ADR 0002 e a base de cada imagem segue o registro de F2.1. O caminho documentado 'hf jobs uv run' não usa a imagem do Dockerfile (huggingface_hub/_jobs_api.py:96). 'hf jobs run IMAGEM COMANDO' aceita imagem pública de qualquer registro; uma Docker Space pode hospedar imagem privada, mas os Jobs usam sempre o último build dela, e a documentação de Jobs não descreve credencial para registro privado (https://huggingface.co/docs/hub/jobs-images). O timeout padrão é 30 minutos e o máximo não é documentado (https://huggingface.co/docs/hub/jobs-configuration#timeout); o tamanho de /dev/shm no contêiner também não (P19). A t4-small tem 15 GB de RAM (https://huggingface.co/docs/hub/jobs-configuration#hardware-flavor). A especificação do job guarda imagem e timeout (huggingface_hub/_jobs_api.py:324-346). O pipeline baixa o vídeo para /dev/shm/reacao-in (processar_culto.py:30), e o servidor local usa --shm-size=8g (docs/onprem.md:46). A documentação usa :latest (docs/hf-jobs.md:34-36; docs/onprem.md:43,47), embora docs/onprem.md:64 proíba latest em produção. A fixture sintética tem 10 s, 320x240 e nenhum rosto e não é versionada no repositório (tests/fixtures/README.md:3-13); F1.1.T6 a publica no dataset ds-fabiopinheiro/reacao-poc-corpus com revisão e SHA-256 registrados em tests/fixtures/README.md, porque dentro de job do HF processar_culto.py recusa caminho local, inclusive arquivo gerado dentro do contêiner (F1.1 RN08, RN11 e critério 11). Fora do HF, sem JOB_ID, o caminho local continua aceito (F1.1 RN10). O motor mock não carrega modelo (reacao/providers/mock.py:1; processar_culto.py:70-71). O bench sempre carrega o detector real (bench.py:109), e o instalador do insightface baixa o buffalo_sc.zip com w600k_mbf.onnx (insightface/utils/storage.py:8-10,21-36); por isso nenhuma execução deste PBI carrega pesos, e a sessão do detector em CUDA é verificada em F2.3. A guarda observa o cwd e /tmp (processar_culto.py:61; reacao/guard.py:60-81), e a issue #2 registra '[guard] ok' mesmo em execução que falhou (corrigida em F1.1). O token hoje usado pela CLI é clássico, com papel write (whoami do HF, 2026-09-23), e F3.1.T3 o revoga depois de F2.6 (Feature F3, F3.1.T3); por isso o primeiro job pago deste PBI é lançado com o token de lançamento de F2.6. Um job não recebe token do HF se nenhum for passado (https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets), e o dataset do corpus é privado, então os jobs de fumaça recebem o HF_TOKEN com o token dos jobs de F2.6, que lê o dataset e não escreve nele (F2.6 RN01 e RN02), e a CLI mostra o token com que está autenticada por 'hf auth whoami' (huggingface_hub/cli/auth.py:162). libreface 0.2.0 depende de dlib==19.24.6 e cmake==3.30.3 (https://pypi.org/pypi/libreface/0.2.0/json), e o dlib 19.24.6 só tem código-fonte no PyPI (https://pypi.org/pypi/dlib/19.24.6/json), então a imagem que instala o libreface compila o dlib. F4 (F4.1.T10, F4.2.T9, F4.4.T8, F4.4.T9, F4.5.T9, F4.7.T9 e F4.6.T7), F5 (F5.3.T3, F5.4.T3 e F5.6.T7) e F7 (F7.4.T4 e a release do piloto em F7.7) publicam imagens por tag de pré-release ou de release pelo processo deste PBI, e F5.3.T3 publica por pré-release a imagem de uma branch (Features detalhadas).

**Regras de negócio:**
- RN01 – As imagens seguem a composição (D2) e o registro (D3) decididos no ADR 0002 (F2.4).
- RN02 – Cada imagem instala as dependências a partir do lock de F2.1 e usa a base registrada em F2.1.
- RN03 – O comando do job escolhe o script: a mesma imagem executa processar_culto.py e bench.py.
- RN04 – Os jobs usam a imagem por digest; nenhum arquivo do repositório usa :latest (docs/onprem.md:64).
- RN05 – Build de PR não publica imagem.
- RN06 – Nenhum peso de modelo é baixado nem incluído nesta etapa; a carga de pesos entra em F2.3.
- RN07 – Os jobs de fumaça leem a fixture sintética por URI hf://datasets/ do dataset ds-fabiopinheiro/reacao-poc-corpus, na revisão registrada em tests/fixtures/README.md (F1.1.T6). O docker run fora do HF, sem JOB_ID, usa a fixture gerada em /dev/shm do contêiner (F1.1 RN10). Nenhum arquivo local é enviado ao job.
- RN08 – Cada job é aprovado por Fabio antes do lançamento, com flavor e timeout explícitos (P7).
- RN09 – Registro que não permite referência por digest, como a Docker Space, só é usado se o ADR 0002 declarar exceção a RN01 e RN09 da Feature; nesse caso as tasks de credencial do CI e de fixação do build entram antes da publicação.
- RN10 – Os jobs de fumaça são lançados pela CLI autenticada com o token de lançamento de F2.6 e recebem só o HF_TOKEN com o token dos jobs, por '--secrets-file -', para ler a fixture no dataset privado; não recebem a chave de serviço nem a ANTHROPIC_API_KEY, porque não gravam no Supabase e rodam com --no-transcribe. As submissões de timeout não recebem segredo.
- RN11 – A imagem que instala o libreface tem as ferramentas de compilação do dlib 19.24.6, que só tem código-fonte no PyPI (https://pypi.org/pypi/dlib/19.24.6/json).
- RN12 – O workflow publica por tag de release e por tag de pré-release, no padrão de tag de F2.1.T5. A tag de pré-release pode estar num commit de branch, gera release marcada como pré-release com os digests e não altera as imagens publicadas por tags de release.

**Fora de escopo:**
- Carga de pesos com hash e verificação da sessão do detector em CUDA (F2.3)
- Bench com rótulos e motores reais (F4.6)
- SBOM e varredura de vulnerabilidades
- Paridade entre execuções (F2.7) e execução no servidor local com GPU (fora do épico)
- Expressão e pose na GPU em lote (F5.3)
- Criação dos tokens e do procedimento de lançamento (F2.6.T1 e F2.6.T2)
- Credencial do CI para publicar em Docker Space (só se o ADR declarar a exceção)

#### Critérios de aceite

- Um PR que altera Dockerfile, pyproject.toml ou o lock constrói as imagens no CI sem publicá-las.
- Um PR com Dockerfile que não constrói tem o check de build reprovado.
- Uma tag de release publica cada imagem de D2 no registro do ADR 0002, e o digest de cada uma fica registrado na release dessa tag.
- Nenhum arquivo do repositório referencia imagem pela tag :latest.
- Para cada imagem de D2, a lista de pacotes impressa por um job pela imagem publicada mostra os pacotes dos motores dela nas versões do lock.
- Em cada imagem, pelo mesmo digest, o comando do job executa processar_culto.py --help e bench.py --help, os dois com código de saída 0.
- O tamanho de /dev/shm na cpu-basic e na t4-small, cada um com o seu JOB_ID, está em docs/hf-jobs.md.
- 'hf jobs inspect' de cada submissão com --timeout 3h e 4h mostra o timeout registrado igual ao pedido; se uma delas for recusada, docs/hf-jobs.md registra a mensagem de recusa e, se ela não informar o máximo, registra que o máximo não é informado.
- Um job t4-small por imagem registra CUDAExecutionProvider entre os providers disponíveis do onnxruntime e torch.cuda.is_available() verdadeiro.
- O diagnóstico, num teste unitário que simula flavor com GPU sem CUDAExecutionProvider ou sem CUDA no torch, termina com código diferente de zero.
- processar_culto.py com o motor mock e sem transcrição, sobre a fixture sintética, termina com código 0 no HF Jobs e com docker run fora do HF, pelo mesmo digest, e a guarda não acusa violação.
- O log dos jobs de fumaça mostra os diretórios de cache de pesos (insightface, hsemotion, torch hub, faster-whisper) sem arquivo.
- O único vídeo processado nos jobs de fumaça é a fixture sintética lida por URI hf://datasets/ na revisão registrada em tests/fixtures/README.md; no docker run fora do HF, é a fixture gerada em /dev/shm do contêiner.
- Os jobs de fumaça são lançados pela CLI autenticada com o token de lançamento de F2.6; 'hf jobs inspect' de cada job de fumaça lista só o segredo HF_TOKEN, sem valor, e o das submissões de timeout não lista segredo.
- Uma tag de pré-release num commit de branch publica as imagens de D2, registra os digests na release marcada como pré-release e não altera as imagens das tags de release.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F2.2.T1 | DevOps | Ajustar o Dockerfile à composição de D2, à base registrada e ao lock | 9 | F2.1 (lock e base registrada), F2.4 (ADR 0002) |
| F2.2.T2 | DevOps | Construir as imagens no CI em PR e publicá-las por tag com digest | 7 | F2.2.T1 |
| F2.2.T3 | DevOps | Escrever o diagnóstico de runtime da imagem sem carregar pesos | 4 | — |
| F2.2.T4 | DevOps | Rodar os jobs de fumaça cpu-basic e t4-small e as submissões de timeout com o token de lançamento | 5 | F2.2.T1, F2.2.T2, F2.2.T3, F2.6.T1, F2.6.T2, F1.1.T6, F1.1, Aprovação de Fabio |
| F2.2.T5 | DevOps | Rodar o mesmo digest com docker run fora do HF e trocar :latest por tag fixa | 3 | F2.2.T2 |
| F2.2.T6 | MLOps | Registrar em docs/hf-jobs.md os resultados dos jobs de fumaça e comparar pacotes com o lock | 3 | F2.2.T4 |
| F2.2.T7 | QA | Verificar os critérios de aceite de F2.2 | 4 | F2.2.T1, F2.2.T2, F2.2.T3, F2.2.T4, F2.2.T5, F2.2.T6 |

<details><summary>F2.2.T1 · [DevOps] Ajustar o Dockerfile à composição de D2, à base registrada e ao lock</summary>

**Objetivo:** Imagens com os extras de cada motor instalados do lock e comando escolhido no lançamento.

**Passos previstos:**
1. Usar em cada imagem a base registrada por F2.1, fixada por digest.
2. Instalar a partir do lock os extras de cada imagem, conforme D2.
3. Na imagem que instala o libreface, instalar os pacotes de sistema para compilar o dlib 19.24.6 (build-essential, cmake e python3-dev, segundo F4) e registrar o tempo de build.
4. Trocar o ENTRYPOINT para permitir escolher processar_culto.py ou bench.py no comando do job.
5. Incluir tests/fixtures/gerar_curto.py e o script de diagnóstico de F2.2.T3.
6. Criar o usuário de UID 1000 só se o ADR escolher Docker Space com exceção declarada (https://huggingface.co/docs/hub/spaces-sdks-docker#permissions).
7. Gravar o commit do build como label e variável de ambiente da imagem.

**Definição de pronto:** docker build local de cada imagem conclui, e processar_culto.py --help e bench.py --help saem com código 0 no contêiner.

**Dependências:** F2.1 (lock e base registrada), F2.4 (ADR 0002)

**Estimativa sugerida:** 9 h (sugestão; validar com o time)

</details>

<details><summary>F2.2.T2 · [DevOps] Construir as imagens no CI em PR e publicá-las por tag com digest</summary>

**Objetivo:** Build sem publicação em PR e publicação por tag com digest registrado.

**Passos previstos:**
1. Acrescentar job de build sem push em pull_request, filtrado por Dockerfile, pyproject.toml e lock.
2. Reativar em .github/workflows/docker.yml o gatilho de tag v* desativado em F2.1.T5, sem a tag latest e sem disparo manual que publique.
3. Aceitar tag de pré-release no padrão de F2.1.T5, inclusive em commit de branch, gerando release marcada como pré-release com os digests e sem alterar as imagens das tags de release.
4. Registrar o digest de cada imagem na release da tag.
5. Documentar em CONTRIBUTING.md o procedimento de release e de pré-release usado por F4, F5 e F7.
6. Conferir o espaço em disco do runner e liberar espaço antes do build se preciso.

**Definição de pronto:** PR de teste mostra o build sem push; uma tag de teste de release e uma de pré-release num commit de branch publicam as imagens, e as duas releases contêm os digests.

**Dependências:** F2.2.T1

**Estimativa sugerida:** 7 h (sugestão; validar com o time)

</details>

<details><summary>F2.2.T3 · [DevOps] Escrever o diagnóstico de runtime da imagem sem carregar pesos</summary>

**Objetivo:** Script que registra /dev/shm, providers do onnxruntime, CUDA no torch, versões e caches de pesos.

**Passos previstos:**
1. Imprimir o tamanho e o espaço livre de /dev/shm.
2. Imprimir onnxruntime.get_available_providers(), torch.cuda.is_available() e o nome da GPU.
3. Imprimir as versões dos pacotes dos motores.
4. Listar os diretórios de cache de pesos do insightface, hsemotion, torch hub e faster-whisper.
5. Sair com código diferente de zero quando ACCELERATOR indicar GPU e CUDA não estiver disponível no onnxruntime ou no torch.
6. Escrever teste unitário que simula GPU esperada sem CUDA.

**Definição de pronto:** Execução local em CPU com código 0 e teste unitário que simula GPU esperada sem CUDA e obtém código diferente de zero.

**Dependências:** nenhuma

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F2.2.T4 · [DevOps] Rodar os jobs de fumaça cpu-basic e t4-small e as submissões de timeout com o token de lançamento</summary>

**Objetivo:** Logs dos jobs de fumaça e resposta às submissões de 3h e 4h entregues para registro, com todos os jobs lançados pelo token de lançamento, os de fumaça com só o HF_TOKEN dos jobs e os de timeout sem segredo.

**Passos previstos:**
1. Pedir aprovação a Fabio com flavors, timeouts e custo previsto pelo preço do flavor (docs/hf-jobs.md:4).
2. Autenticar a CLI com o token de lançamento de F2.6.T1, conforme o procedimento de F2.6.T2, e registrar o nome do token mostrado por 'hf auth whoami' antes de lançar.
3. Lançar 'hf jobs run --flavor cpu-basic' pela imagem com digest, com o HF_TOKEN do token dos jobs entregue por '--secrets-file -' (F2.6.T2) e o comando validado pelo lançador de F1.1.T4: diagnóstico e processar_culto.py com o motor mock, --no-transcribe e --video na URI hf://datasets/ da fixture, com a revisão de tests/fixtures/README.md (F1.1.T6).
4. Lançar o mesmo comando com --flavor t4-small e timeout curto, um job por imagem de D2.
5. Submeter jobs curtos com --timeout 3h e 4h, sem segredo, ler 'hf jobs inspect' de cada um e cancelá-los logo depois do aceite; guardar a mensagem de recusa, se houver.
6. Entregar JOB_IDs, nome do token de lançamento e trechos de log a F2.2.T6.

**Definição de pronto:** Jobs lançados com o token de lançamento, os de fumaça com só o HF_TOKEN dos jobs e os de timeout sem segredo, concluídos com o diagnóstico em código 0; JOB_IDs, trechos de log (/dev/shm, providers, pacotes, caches) e respostas das submissões de timeout entregues a F2.2.T6.

**Dependências:** F2.2.T1, F2.2.T2, F2.2.T3, F2.6.T1, F2.6.T2, F1.1.T6, F1.1, Aprovação de Fabio

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F2.2.T5 · [DevOps] Rodar o mesmo digest com docker run fora do HF e trocar :latest por tag fixa</summary>

**Objetivo:** Mesmo digest executado fora do HF e documentação sem :latest.

**Passos previstos:**
1. Baixar a imagem pelo digest numa máquina fora do HF.
2. Rodar o diagnóstico e processar_culto.py com o motor mock sobre a fixture gerada em /dev/shm, sem JOB_ID (F1.1 RN10).
3. Trocar :latest por tag fixa em docs/hf-jobs.md:34-36 e docs/onprem.md:43,47.

**Definição de pronto:** Log local com código 0 e guarda sem violação; busca por ':latest' no repositório sem resultado.

**Dependências:** F2.2.T2

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F2.2.T6 · [MLOps] Registrar em docs/hf-jobs.md os resultados dos jobs de fumaça e comparar pacotes com o lock</summary>

**Objetivo:** Tabela única que liga tag, digest, lock, flavor, JOB_ID, /dev/shm e timeout.

**Passos previstos:**
1. Montar em docs/hf-jobs.md a tabela tag, digest, versão do lock, flavor, JOB_ID, tamanho de /dev/shm por flavor e resposta às submissões de timeout.
2. Comparar a lista de pacotes impressa em cada job com o lock da imagem correspondente.

**Definição de pronto:** docs/hf-jobs.md com a tabela completa e comparação sem diferença entre pacotes do job e lock.

**Dependências:** F2.2.T4

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F2.2.T7 · [QA] Verificar os critérios de aceite de F2.2</summary>

**Objetivo:** Evidência de cada critério de aceite anexada ao PBI.

**Passos previstos:**
1. Conferir o PR de build sem push e um PR com Dockerfile quebrado.
2. Conferir as releases de release e de pré-release com digests e a busca por ':latest'.
3. Ler os logs dos jobs cpu-basic e t4-small: pacotes, --help, providers, /dev/shm, caches vazios e vídeo processado.
4. Conferir em 'hf jobs inspect' o timeout de cada submissão, só HF_TOKEN nos jobs de fumaça, nenhum segredo nas submissões de timeout e o registro em docs/hf-jobs.md.
5. Conferir o nome do token de lançamento registrado antes dos lançamentos.
6. Rodar o teste unitário do diagnóstico com CUDA ausente.
7. Conferir o log do docker run fora do HF.

**Definição de pronto:** Checklist dos 15 critérios com links de CI, releases e JOB_IDs anexada ao PBI.

**Dependências:** F2.2.T1, F2.2.T2, F2.2.T3, F2.2.T4, F2.2.T5, F2.2.T6

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- Dockerfile:1-12
- .github/workflows/docker.yml:1-25
- GitHub list_tags vazio e workflow docker sem execuções (levantamento, 2026-09-23)
- https://pypi.org/pypi/libreface/0.2.0/json
- https://pypi.org/pypi/py-feat/2.1.3/json
- lock310.txt do levantamento, linhas 296 e 392
- huggingface_hub/_jobs_api.py:96,324-346 (instalado)
- huggingface_hub/cli/auth.py:162 (hf auth whoami, instalado)
- https://huggingface.co/docs/hub/jobs-images
- https://huggingface.co/docs/hub/jobs-configuration#timeout
- https://huggingface.co/docs/hub/jobs-configuration#hardware-flavor
- https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets
- https://huggingface.co/docs/hub/spaces-sdks-docker#permissions
- whoami do HF, 2026-09-23 (token clássico write)
- Feature F3 detalhada, F3.1.T3 (revogação do token clássico depois de F2.6)
- processar_culto.py:30,61,70-71
- bench.py:109
- reacao/providers/mock.py:1
- reacao/guard.py:60-81
- insightface/utils/storage.py:8-10,21-36 (instalado)
- docs/hf-jobs.md:34-38
- docs/onprem.md:43-49,64
- tests/fixtures/README.md:3-13
- issue #2
- premissa P19
- https://pypi.org/pypi/dlib/19.24.6/json (só sdist, 2026-09-23)
- https://pypi.org/pypi/libreface/0.2.0/json (requires_dist com dlib==19.24.6 e cmake==3.30.3)
- Feature F1 detalhada: F1.1 RN08, RN10, RN11 e F1.1.T6
- Feature F4 detalhada: pendência para F2.2 (ferramentas de compilação do dlib e publicação por pré-release) e tasks de publicação F4.1.T10, F4.2.T9, F4.4.T8, F4.4.T9, F4.5.T9, F4.7.T9 e F4.6.T7
- Feature F5 detalhada: F5.3.T3 e pendência para F2.2 (pré-release em commit de branch)

#### Verificação INVEST: pontos que falharam
- Independent: F2.2.T4 espera F2.6.T1, F2.6.T2 e F1.1.T6; as demais tasks não dependem de F2.6.

#### Premissas
- A carga de pesos fica fora deste PBI porque carregar o detector antes de F2.3 baixaria o buffalo_sc.zip com w600k_mbf.onnx. Por isso a fumaça usa o motor mock e a sessão do detector em CUDA é verificada em F2.3.
- O valor de 4h no teste de timeout é dedução do levantamento: um culto de 2 h no limite do critério 5 (2 h por hora de vídeo) levaria 4 h. O valor de 3h vem de docs/hf-jobs.md:13.
- Roda um job t4-small por imagem de D2; a cpu-basic roda com uma só imagem, porque /dev/shm e o timeout dependem do ambiente do job e não da imagem (dedução).
- O build cabe no disco do runner padrão do GitHub Actions; se não couber, o build de PR libera espaço antes ou passa a rodar por disparo manual (a verificar na task).
- F1.1 entra como dependência porque a issue #2 registra '[guard] ok' mesmo em execução que falhou, o que impede ler o resultado da guarda nos jobs de fumaça.
- F2.2.T4 depende de F2.6.T1 e F2.6.T2 para que o primeiro job pago seja lançado com o token de lançamento, e não com o token clássico de escrita que F3.1.T3 revoga. As demais tasks deste PBI não esperam F2.6, e F2.6 só espera F2.2 em F2.6.T7 (F2.2.T2); entre tasks não há ciclo.
- Disciplinas: DevOps, MLOps e QA. Visão Computacional saiu das disciplinas previstas na árvore porque a única task que a usava é diagnóstico de imagem e runtime (DevOps), e a verificação da sessão do detector passou para F2.3.
- Story points e horas são sugestão.
- Os pacotes de sistema para compilar o dlib seguem a pendência de F4 para F2.2 (build-essential, cmake e python3-dev); o nome exato depende da base registrada em F2.1 (dedução).
- Os jobs de fumaça passam a receber o HF_TOKEN com o token dos jobs, porque a fixture fica no dataset privado; esse token lê o dataset e não escreve nele (F2.6 RN01 e RN02).

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável.
- Item pai: Feature F2.
- Registrar no PBI a aprovação de custo de Fabio e os JOB_IDs dos jobs de fumaça.
- Vincular a release e os digests publicados ao PBI.
- Se o ADR 0002 escolher Docker Space com exceção a RN01 e RN09, criar as tasks de credencial do CI (Trusted Publishers, F2.6 RN08) e de fixação do build.
- Informar F4, F5 e F7 do padrão de tag de pré-release documentado em F2.2.T2.

## Preview — PBI F2.3 (novo) · Carregar os pesos do detector, da expressão, da pose e da transcrição por revisão fixa com SHA-256 conferido antes do primeiro quadro, de repositórios de modelo privados quando a licença permitir

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Carregar os pesos do detector, da expressão, da pose e da transcrição por revisão fixa com SHA-256 conferido antes do primeiro quadro, de repositórios de modelo privados quando a licença permitir |
| Tipo | Product Backlog Item |
| Pai | F2 |
| Tags | F2; pesos; MLOps; Visão Computacional; regra 2; licenças |
| Estimativa | 8 pts (sugestão); tasks: 38 h |
| Dependências | F2.1 (lock), F2.2 (imagem com digest para os jobs de verificação), F2.4 (namespace dos repositórios de modelo), F2.6 (repositórios privados vazios e token de leitura do CI), F4.3 (licença e decisão de espelhamento de todos os pesos, inclusive o faster-whisper, registradas no ADR 0001; F4.3.T4 antes de F2.3.T1), F1.6 (motores reais no CI e vídeo licenciado, cuja origem de pesos este PBI troca), Aprovação de Fabio para o job t4-small de verificação |
| Substitui | nenhum |

#### Descrição

Como integrante do time de MLOps responsável pela reprodutibilidade dos jobs  
Quero que cada peso usado pelo pipeline venha de um repositório de modelo privado, ou da origem quando a licença não permitir espelhar e a origem não trouxer arquivo de reconhecimento, por revisão fixa e com SHA-256 conferido antes do primeiro quadro, sem o arquivo de reconhecimento facial no ambiente  
Para que o gate e o piloto usem os mesmos pesos em qualquer execução, que um peso alterado interrompa a execução antes de processar o vídeo e que nenhum modelo de reconhecimento facial esteja disponível no contêiner (regra 2 do CLAUDE.md)

**Contexto:** O detector carrega buffalo_sc por FaceAnalysis com allowed_modules=['detection'] e verifica que o reconhecimento não foi carregado (reacao/detect.py:12-18). O instalador do insightface baixa buffalo_sc.zip dos releases do GitHub sem hash e extrai det_500m.onnx e w600k_mbf.onnx, o modelo de reconhecimento (insightface/utils/storage.py:8-10,21-36; ~/.insightface/models/buffalo_sc no ambiente do levantamento); não há outra origem conhecida para det_500m.onnx. O HSEmotion baixa enet_b0_8_best_afew.onnx de github.com sem hash; o proxy do levantamento recusou a URL, e o contorno por raw.githubusercontent.com existe só em tools/rodar_teste.sh:29-33 (hsemotion_onnx/facial_emotions.py:15-24). O 6DRepNet baixa 6DRepNet_300W_LP_AFLW2000.pth de cloud.ovgu.de sem check_hash (sixdrepnet/regressor.py:35). O faster-whisper 'medium' vem de Systran/faster-whisper-medium sem revisão, e qualquer exceção troca em silêncio para 'small' em CPU (reacao/transcribe.py:6-12). O HSEmotion e o 6DRepNet são carregados antes do laço de quadros (processar_culto.py:64; reacao/providers/hsemotion.py:10-16), o detector na primeira chamada de detect, dentro do laço (processar_culto.py:73; reacao/detect.py:27-29), e o faster-whisper só depois de todo o vídeo (processar_culto.py:86-89). A fixture sintética não tem trilha de áudio, porque é gravada só com cv2.VideoWriter (tests/fixtures/gerar_curto.py:24-39), e a transcrição decodifica a trilha de áudio 0 (faster_whisper/audio.py:47); com o motor mock ou --no-transcribe, o Whisper não é carregado (processar_culto.py:86). A conta não tem repositório de modelo (HfApi.list_models, 2026-09-23). Os modelos pré-treinados do insightface servem só para pesquisa não comercial (insightface-2.0.dist-info/METADATA:50-54). F4.3 registra no ADR 0001 a licença e a decisão de uso no PoC, no espelhamento e no piloto de cada modelo carregado na execução, inclusive o Whisper, e aciona F4.7 se vetar o SCRFD (árvore, F4.3 e F4.7; F4.3.T3 segundo a revisão da árvore). F4.7 usa o mecanismo de carga deste PBI (F4.7.T5), por isso F2.3 não depende de F4.7: com o veto ao espelhamento de det_500m.onnx, os critérios do detector deste PBI passam a F4.7. F1.6 põe os motores reais no CI com pesos da origem e deixa para este PBI a verificação de ausência de w600k_mbf.onnx. Downloads podem ser fixados por revisão (https://huggingface.co/docs/huggingface_hub/guides/manage-cache#pin-a-revision-advanced).

**Regras de negócio:**
- RN01 – Cada peso carregado tem entrada num manifesto versionado com origem, revisão ou URL fixa, SHA-256, licença e decisão de espelhamento; peso sem entrada não é carregado.
- RN02 – O SHA-256 de todos os pesos que a execução vai usar, inclusive os da transcrição quando ela estiver ligada, é conferido antes da leitura do primeiro quadro; divergência interrompe a execução.
- RN03 – w600k_mbf.onnx e qualquer outro arquivo de reconhecimento não entram nos repositórios, na imagem, no CI nem no job (regra 2). O teste negativo usa um arquivo vazio com esse nome.
- RN04 – Um peso só é espelhado em repositório privado se a licença permitir, conforme a decisão de F4.3 registrada no ADR 0001; este PBI não faz novo levantamento de licença. Sem permissão, HSEmotion, 6DRepNet e faster-whisper vêm da origem por URL ou revisão fixa, com SHA-256 conferido e registrado no log.
- RN05 – O det_500m.onnx nunca vem da origem, porque a origem é o buffalo_sc.zip, que traz w600k_mbf.onnx. Sem permissão de espelhar, o detector SCRFD não é carregado em nenhum ambiente; F4.3 aciona F4.7, que recebe os critérios 6 e 13 deste PBI.
- RN06 – Enquanto o fallback de reacao/transcribe.py:11-12 existir, o modelo de reserva 'small' segue as mesmas regras do 'medium'.
- RN07 – O detector continua carregado só com o módulo de detecção e com a verificação de que nenhum módulo de reconhecimento foi carregado.
- RN08 – Se o ADR 0002 decidir imagem pública, nenhum peso entra na imagem.
- RN09 – O mecanismo de carga serve também aos pesos de LibreFace e Py-Feat (F4.1 e F4.2) e ao detector de F4.7, se acionado.
- RN10 – Execuções locais deste PBI usam só a fixture sintética (P26). Comparações de saída sobre rostos rodam no CI com o vídeo licenciado de F1.6 (P26) ou em job no HF, sem gravar recorte fora de /dev/shm (regra 1).

**Fora de escopo:**
- Pesos de LibreFace e Py-Feat (F4.1 e F4.2)
- Troca do detector ou detecção por ladrilhos, inclusive a publicação e a verificação do detector escolhido quando F4.3 vetar o SCRFD (F4.7)
- Levantamento e decisão de licença dos pesos do detector, dos motores e do Whisper (F4.3)
- Criação dos repositórios privados vazios e dos tokens (F2.6)
- Mudança de det_size ou det_thresh

#### Critérios de aceite

- O manifesto versionado lista det_500m.onnx, enet_b0_8_best_afew.onnx, 6DRepNet_300W_LP_AFLW2000.pth, faster-whisper medium e faster-whisper small, cada um com origem, revisão ou URL fixa, SHA-256, licença, decisão de espelhamento e referência à seção do ADR 0001 em que F4.3 registrou a decisão.
- Os repositórios de modelo do projeto são privados, e nenhum contém w600k_mbf.onnx.
- O log de um job pela imagem registra, para cada peso carregado, a origem, a revisão ou URL fixa e o SHA-256 conferido.
- Para os pesos espelhados, o log do job não mostra download do instalador do insightface, de cloud.ovgu.de nem de github.com.
- Com o detector marcado como não espelhável no manifesto, a execução confere e registra os demais pesos e termina antes do primeiro quadro, com código diferente de zero e mensagem que cita o veto de licença, sem baixar o buffalo_sc.zip.
- Se F4.3 permitir espelhar det_500m.onnx, um job t4-small pela imagem, com a fixture sintética lida do dataset por revisão (F1.1.T6), registra a sessão do detector do manifesto com CUDAExecutionProvider. Com o veto, este critério passa a F4.7.
- Com SHA-256 divergente em qualquer peso que a execução vai usar, inclusive só no modelo de transcrição, a execução para antes do primeiro quadro, com mensagem que nomeia o arquivo, e termina com código diferente de zero.
- No job, a verificação dos pesos carrega os modelos faster-whisper medium e small do manifesto sem decodificar áudio e registra a revisão de cada um.
- Quando o carregamento do medium falha, a transcrição carrega o small do manifesto, e o log registra a troca.
- No CI e no job, a verificação de ausência de w600k_mbf.onnx passa.
- Com um arquivo vazio chamado w600k_mbf.onnx no diretório de pesos, a mesma verificação falha.
- O CI carrega os pesos espelhados dos repositórios privados com o token somente leitura de F2.6.
- Se F4.3 permitir espelhar det_500m.onnx, o teste da regra 2 continua aprovado com o detector carregado a partir do arquivo do manifesto. Com o veto, este critério passa a F4.7.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F2.3.T1 | Governança e Privacidade | Copiar para o manifesto a licença e a decisão de espelhamento registradas por F4.3 no ADR 0001 | 1 | F4.3.T4 |
| F2.3.T2 | MLOps | Publicar os pesos permitidos nos repositórios privados e completar o manifesto | 5 | F2.3.T1, F2.6.T1 (repositórios e tokens) |
| F2.3.T3 | MLOps | Implementar a carga por revisão com SHA-256 e a conferência de todos os pesos antes do primeiro quadro | 8 | F2.3.T2 |
| F2.3.T4 | Visão Computacional | Carregar o detector SCRFD só de det_500m.onnx, quando espelhável, e o HSEmotion e o 6DRepNet pelos arquivos verificados | 10 | F2.3.T3, F1.6 |
| F2.3.T5 | MLOps | Carregar o faster-whisper medium e small por revisão fixa e verificá-los sem decodificar áudio | 5 | F2.3.T3 |
| F2.3.T6 | DevOps | Ligar o CI e a imagem ao manifesto e verificar a ausência de w600k_mbf.onnx | 5 | F2.3.T4, F2.3.T5, F1.6, F2.6.T2 (token do CI cadastrado no GitHub Actions) |
| F2.3.T7 | QA | Verificar os critérios de aceite de F2.3 | 4 | F2.3.T6, Aprovação de Fabio |

<details><summary>F2.3.T1 · [Governança e Privacidade] Copiar para o manifesto a licença e a decisão de espelhamento registradas por F4.3 no ADR 0001</summary>

**Objetivo:** Manifesto com licença, fonte e decisão de espelhamento de cada peso, com referência ao ADR 0001, sem novo levantamento de licença.

**Passos previstos:**
1. Ler no ADR 0001 a decisão de F4.3 para det_500m.onnx, enet_b0_8_best_afew.onnx, 6DRepNet_300W_LP_AFLW2000.pth e faster-whisper medium e small.
2. Copiar para o manifesto licença, fonte, 'espelhar: sim ou não' e a referência à seção do ADR 0001.
3. Se algum desses pesos faltar no registro de F4.3, registrar a falta no PBI como pendência de F4.3, sem decidir a licença aqui.
4. Se o registro vetar o espelhamento de det_500m.onnx, marcar o detector como não espelhável no manifesto.

**Definição de pronto:** Manifesto com licença, fonte, decisão de espelhamento e referência ao ADR 0001 para os cinco pesos, conferido contra o ADR 0001 na revisão do PR pelo time de MLOps.

**Dependências:** F4.3.T4

**Estimativa sugerida:** 1 h (sugestão; validar com o time)

</details>

<details><summary>F2.3.T2 · [MLOps] Publicar os pesos permitidos nos repositórios privados e completar o manifesto</summary>

**Objetivo:** Pesos permitidos nos repositórios privados com revisão marcada e SHA-256 no manifesto; pesos não espelhados com URL ou revisão de origem e SHA-256.

**Passos previstos:**
1. Calcular o SHA-256 de cada arquivo.
2. Enviar det_500m.onnx sem o restante do buffalo_sc, se permitido, e os demais pesos permitidos.
3. Criar tag de revisão em cada repositório.
4. Registrar revisão e hash no manifesto; para HSEmotion, 6DRepNet e faster-whisper não espelhados, registrar URL ou revisão de origem e hash.

**Definição de pronto:** Repositórios com os arquivos e a tag, sem w600k_mbf.onnx, e manifesto versionado.

**Dependências:** F2.3.T1, F2.6.T1 (repositórios e tokens)

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F2.3.T3 · [MLOps] Implementar a carga por revisão com SHA-256 e a conferência de todos os pesos antes do primeiro quadro</summary>

**Objetivo:** Função única que obtém o peso pelo manifesto e passo que confere todos os pesos da execução antes de ler o vídeo.

**Passos previstos:**
1. Implementar a função que recebe a entrada do manifesto, baixa por revisão ou URL fixa para o diretório de pesos e confere o SHA-256, com erro que nomeia o arquivo.
2. Chamar, no início de processar_culto.py e de bench.py e antes de ler o primeiro quadro, a conferência de todos os pesos que a execução vai usar, inclusive os da transcrição quando ela estiver ligada.
3. Conferir e registrar no log os pesos permitidos antes de acusar um detector não espelhável, que termina a execução antes do primeiro quadro, com mensagem que cita o veto, sem baixar o buffalo_sc.zip.
4. Registrar no log origem, revisão e hash de cada peso.
5. Escrever testes com hash correto, hash divergente, hash divergente só no modelo de transcrição e detector não espelhável.

**Definição de pronto:** Testes unitários aprovados nos quatro casos; nos casos de erro a execução termina antes do primeiro quadro com código diferente de zero, e no caso do detector não espelhável os demais pesos aparecem no log antes da mensagem de veto.

**Dependências:** F2.3.T2

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F2.3.T4 · [Visão Computacional] Carregar o detector SCRFD só de det_500m.onnx, quando espelhável, e o HSEmotion e o 6DRepNet pelos arquivos verificados</summary>

**Objetivo:** Detector (quando F4.3 permitir espelhar), expressão e pose carregados pelos arquivos do manifesto, com a verificação da regra 2 mantida.

**Passos previstos:**
1. Se o manifesto permitir o detector: preparar o diretório de modelo só com det_500m.onnx obtido pela função de F2.3.T3, mantendo allowed_modules=['detection'], a verificação de que o reconhecimento não foi carregado e det_size e det_thresh atuais (reacao/detect.py:9,16), e registrar no log os providers da sessão do detector.
2. Com o veto de F4.3, não carregar o detector e registrar no PBI que a carga do detector escolhido passa a F4.7.T5.
3. Passar ao HSEmotion o arquivo verificado e carregar o state dict do 6DRepNet a partir do arquivo verificado.
4. Rodar localmente só com a fixture sintética e confirmar que nenhum download das origens antigas acontece.
5. Comparar as saídas de HSEmotion e 6DRepNet entre o carregamento antigo e o novo no CI, com o vídeo licenciado de F1.6 (P26), sem gravar recorte fora de /dev/shm; com o veto do detector, comparar sobre entradas fixas geradas em memória.

**Definição de pronto:** Teste da regra 2 aprovado com o detector do manifesto ou, com o veto, registro no PBI da passagem a F4.7; execução local com a fixture sem download das origens antigas; saídas iguais no CI.

**Dependências:** F2.3.T3, F1.6

**Estimativa sugerida:** 10 h (sugestão; validar com o time)

</details>

<details><summary>F2.3.T5 · [MLOps] Carregar o faster-whisper medium e small por revisão fixa e verificá-los sem decodificar áudio</summary>

**Objetivo:** Transcrição com os dois modelos por revisão e hash do manifesto e verificação no job sem vídeo com áudio.

**Passos previstos:**
1. Obter os arquivos de cada modelo pela função de F2.3.T3, conforme o manifesto, e passar o caminho local ao WhisperModel.
2. Expor em reacao/transcribe.py qual modelo foi carregado e registrar no log a troca para o small.
3. Acrescentar ao passo de verificação dos pesos o carregamento do medium e do small a partir do caminho verificado, sem decodificar áudio.
4. Escrever teste que força falha no medium e confere o carregamento do small do manifesto.

**Definição de pronto:** Teste do caminho de reserva aprovado; a verificação local registra a revisão dos dois modelos.

**Dependências:** F2.3.T3

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F2.3.T6 · [DevOps] Ligar o CI e a imagem ao manifesto e verificar a ausência de w600k_mbf.onnx</summary>

**Objetivo:** CI e job obtêm os pesos pelo manifesto e reprovam a presença de arquivo de reconhecimento.

**Passos previstos:**
1. Usar no CI o secret com o token de leitura de F2.6.
2. Trocar no CI de F1.6 a origem dos pesos pelo manifesto.
3. Acrescentar ao CI e ao início do job a busca por w600k_mbf.onnx e outros arquivos de reconhecimento nos diretórios de pesos, com falha se encontrar.
4. Executar um teste negativo com um arquivo vazio chamado w600k_mbf.onnx no diretório.

**Definição de pronto:** CI verde com pesos do manifesto e teste negativo reprovado com o arquivo vazio.

**Dependências:** F2.3.T4, F2.3.T5, F1.6, F2.6.T2 (token do CI cadastrado no GitHub Actions)

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F2.3.T7 · [QA] Verificar os critérios de aceite de F2.3</summary>

**Objetivo:** Evidência de cada critério de aceite anexada ao PBI.

**Passos previstos:**
1. Conferir o manifesto, a referência ao ADR 0001 e a listagem dos repositórios privados.
2. Pedir aprovação a Fabio e rodar um job t4-small pela imagem com a fixture sintética lida por URI hf://datasets/ na revisão de tests/fixtures/README.md (F1.1.T6), o motor hsemotion e a verificação dos pesos da transcrição.
3. Ler no log origem, revisão e hash de cada peso, a ausência de download das origens antigas para os pesos espelhados, os modelos medium e small verificados e, se o detector for espelhável, os providers da sessão do detector; com o veto, conferir que o job termina com a mensagem de veto depois de registrar os demais pesos.
4. Rodar localmente os casos de hash divergente (inclusive só na transcrição), detector não espelhável, reserva small e arquivo vazio w600k_mbf.onnx.
5. Conferir no CI a carga pelos repositórios privados e, se o detector for espelhável, o teste da regra 2.

**Definição de pronto:** Checklist dos 13 critérios com JOB_ID, trechos de log e links de CI anexada ao PBI; com o veto do detector, os critérios 6 e 13 marcados como transferidos a F4.7.

**Dependências:** F2.3.T6, Aprovação de Fabio

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- reacao/detect.py:9-29
- insightface/utils/storage.py:8-10,21-36 (instalado)
- ~/.insightface/models/buffalo_sc com det_500m.onnx e w600k_mbf.onnx (ambiente do levantamento)
- hsemotion_onnx/facial_emotions.py:15-24 (instalado)
- sixdrepnet/regressor.py:35 (instalado)
- reacao/pose.py:11-16
- reacao/providers/hsemotion.py:10-16
- reacao/transcribe.py:6-12
- processar_culto.py:64,73,86-89
- tests/fixtures/gerar_curto.py:24-39
- faster_whisper/audio.py:47 (instalado)
- tools/rodar_teste.sh:29-33
- insightface-2.0.dist-info/METADATA:50-54
- HfApi.list_models(author='ds-fabiopinheiro'): 0 repositórios (2026-09-23)
- SHA-256 dos arquivos em cache (mapa_infra.jsonl)
- https://huggingface.co/docs/huggingface_hub/guides/manage-cache#pin-a-revision-advanced
- Árvore: F1.6, F4.1, F4.2, F4.3, F4.7
- Revisão da árvore: F4.3.T1, F4.3.T3, F4.3.T4, F4.4.T3, F4.7.T5 e F4.7.T8; verificação de ciclos do grafo (deps_check.py: F2.3→F4.7→F2.3 e F2.3→F4.7→F4.4→F2.3)

#### Premissas
- Os repositórios privados vazios de modelo e o token de leitura do CI são criados em F2.6; este PBI publica os pesos neles.
- F2.3.T1 só copia para o manifesto a decisão de licença e espelhamento que F4.3 registra no ADR 0001. F4.3.T1 lista os modelos faster-whisper medium e small e o Silero VAD embutido (Feature F4 detalhada), então a verificação da licença do Whisper fica toda em F4.3.
- F2.3 não depende de F4.7. O PBI fecha com o mecanismo de F2.3.T3 e os pesos que F4.3 permite espelhar. Com o veto de F4.3 ao espelhamento de det_500m.onnx, os critérios 6 e 13 passam a F4.7: F4.7.T5 publica no manifesto o detector escolhido pelo mecanismo de F2.3.T3 e F4.7.T8 verifica.
- Para o detector não espelhável não foi adotada a extração só de det_500m.onnx em memória, porque o zip de origem já contém w600k_mbf.onnx.
- Com o veto, a conferência dos pesos registra os demais pesos antes de acusar o veto, para que os critérios 3, 4, 7 e 8 sejam verificados no job, e a comparação de saídas de F2.3.T4 usa entradas fixas geradas em memória, porque sem detector não há recorte de rosto (dedução).
- A verificação dos pesos da transcrição no job carrega os modelos sem decodificar áudio, porque a fixture não tem trilha de áudio e nenhum vídeo com áudio está disponível para jobs antes de F3.1 ou F5.1.
- F1.6, F2.2 e F2.4 entram como dependências: F1.6 carrega os motores reais no CI e fornece o vídeo licenciado da comparação, os jobs de verificação usam a imagem de F2.2 e os repositórios ficam no namespace do ADR 0002.
- As tasks de carga do detector e de carga do HSEmotion e do 6DRepNet foram fundidas numa task de Visão Computacional para manter 7 tasks.
- QA foi acrescentada às disciplinas da árvore (MLOps, Visão Computacional, Governança e Privacidade, DevOps) porque todo PBI precisa de verificação dos critérios. Governança e Privacidade fica na task que copia e confere contra o ADR 0001 a decisão de licença.
- Story points e horas são sugestão.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável.
- Item pai: Feature F2.
- Registrar no PBI a aprovação de custo e o JOB_ID do job t4-small.
- Sincronizar com F4.1 e F4.2 o uso do manifesto e da função de carga.
- Se F4.3 vetar o espelhamento de det_500m.onnx: passar a F4.7 os critérios 6 e 13 (F4.7.T5 publica o detector escolhido no manifesto, F4.7.T8 verifica) e informar F1.6 de que o CI deixa de carregar o SCRFD da origem quando F2.3 for concluído.
- Informar F4.4 e F4.7 de que F4.4.T3 e F4.7.T5 dependem de F2.3.T3 (mecanismo), e não do PBI F2.3 inteiro.

## Preview — PBI F2.4 (novo) · Registrar em ADR o modo de execução dos jobs, a composição e o registro da imagem, o namespace e o acesso no HF, a fronteira de dados entre HF, Supabase e Vercel, as decisões do painel web e o envio da transcrição à API da Anthropic

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Registrar em ADR o modo de execução dos jobs, a composição e o registro da imagem, o namespace e o acesso no HF, a fronteira de dados entre HF, Supabase e Vercel, as decisões do painel web e o envio da transcrição à API da Anthropic |
| Tipo | Product Backlog Item |
| Pai | F2 |
| Tags | F2; ADR; arquitetura; acesso; HF; Vercel; Supabase; PBI-106 |
| Estimativa | 8 pts (sugestão); tasks: 29 h |
| Dependências | Disponibilidade de Fabio para decidir e aprovar o ADR, inclusive a exceção da P26, Uma conta de teste fora da lista de acesso para o teste do Space, Organização no HF criada por Fabio, com papel de escrita para quem cria o Space de teste, se D4 ou D6 escolherem organização |
| Substitui | PBI-106 (parte: decisão de rodar os jobs pela mesma imagem) |

#### Descrição

Como Fabio Pinheiro, dono da conta HF e aprovador de custo  
Quero um ADR aceito que decida como os jobs rodam, como as imagens são compostas, com as versões exatas de libreface e py-feat, e onde ficam, em que namespace ficam os repositórios, o Space de rotulagem e o destino do piloto, quem acessa o quê no HF, quais dados e credenciais o HF, o Supabase e o painel web na Vercel recebem, quais tabelas do Supabase o painel lê e escreve, onde fica o vínculo entre conta e papel e se a regra 6 vale para as contas da equipe, com que projeto, framework, login, proteção de deployment e validade de token o painel funciona e se a transcrição de cultos públicos vai à API da Anthropic na Fase 0  
Para que F2.1, F2.2, F2.3, F2.5, F2.6, F2.8, F3.3, F5.4, F5.5, F5.6, F6.2, F7.1, F7.2 e F7.8 comecem sem decisão pendente, e que a chave de serviço, o texto completo da transcrição e os dados brutos fiquem fora do painel web

**Contexto:** Decisões a registrar no ADR 0002, próximo número depois de docs/adr/0001-motor.md. D1: modo de execução; 'hf jobs uv run' usa a imagem padrão do uv e não a do Dockerfile (huggingface_hub/_jobs_api.py:96), e 'hf jobs run IMAGEM COMANDO' roda qualquer imagem (https://huggingface.co/docs/hub/jobs-images). D2: uma imagem com os três motores ou uma por motor, e se os pesos entram na imagem. Os motores não cabem numa mesma resolução sem rebaixar o Py-Feat: libreface 0.2.0 fixa torch==2.0.0, opencv-python==4.10.0.84 e mediapipe==0.10.5 (https://pypi.org/pypi/libreface/0.2.0/json), py-feat 2.1.3 exige torch>=2.5 (https://pypi.org/pypi/py-feat/2.1.3/json), e a resolução conjunta cai para py-feat 0.6.1 e torch 2.0.0 com runtime CUDA 11 (lock310.txt do levantamento, linhas 205-230, 296 e 392); F4.2 prevê a API 0.6 ou a 2.x (árvore, F4.2). D2 decide a versão exata do py-feat (0.6.1 ou 2.1.3; a 0.6.2 fica fora pela regra 2, conforme F4.2) e registra libreface 0.2.0, que F2.1 fixa no lock; na Feature F4 detalhada, F4.1.T5 saiu e F4.2.T1 só confere a API na versão fixada, e F4 entrega os insumos das duas opções (Python, torch e dlib de cada uma). D3: registro; GHCR (workflow existente e nunca executado, .github/workflows/docker.yml) ou Docker Space privada, que hospeda imagem sem conta em registro, mas pode ficar indisponível e faz os Jobs usarem sempre o último build, sem referência por digest; a documentação de Jobs não descreve credencial para registro privado (https://huggingface.co/docs/hub/jobs-images). Publicar numa Docker Space pelo CI exigiria credencial de escrita no Hub, que o token do CI de F2.6 não tem. O repositório GitHub é público (API do GitHub, levantamento). D4: namespace pessoal ou de organização para repositórios de modelo, repositório de resultados, Space de rotulagem, destino dos vídeos do piloto e bucket jobs-artifacts (P27). Rodar Jobs de uma organização exige papel de escrita nela (https://huggingface.co/docs/huggingface_hub/guides/jobs#run-a-job), e o usuário tem papel read em impacto-cognitivo (whoami do HF, 2026-09-23). D5: SDK do Space de rotulagem (Gradio ou Docker; Streamlit só pelo template Docker, https://huggingface.co/docs/hub/spaces-config-reference). D6: acesso no HF de rotuladores (Space de rotulagem) e da equipe de mídia (destino do piloto). Um repositório de usuário só é alterado pelo dono, e dar acesso a outras pessoas passa por organização (https://huggingface.co/docs/hub/repositories-settings); Space privado só abre para dono e colaboradores, protected exige PRO ou Team (https://huggingface.co/docs/hub/spaces-overview#space-visibility); hf_oauth_authorized_org restringe o login a membros de organizações (https://huggingface.co/docs/hub/spaces-oauth); Space Gradio ou Docker pessoal exige PRO, cujo periodEnd é 2026-10-01, sem indicação de cancelamento e com renovação a confirmar (whoami do HF). D7: fronteira de dados e credenciais, decidida pelo usuário na P3 revisada: processamento e ferramentas que exibem ou recebem vídeo ou quadro ficam no HF; o painel web na Vercel lê do Supabase só agregados, eventos e insights e, se o ADR registrar, momentos, com Supabase Auth, RLS por perfil e chave pública, e recebe as notas do critério 4 (insight_feedback); a chave de serviço fica só nos jobs do HF e no local de guarda de quem lança; a Vercel não recebe vídeo, quadro, recorte de rosto nem observação por rosto. O trecho citado de cada insight fica na coluna insight.trecho, com até 200 caracteres (supabase/migrations/0001_init.sql:16; reacao/insights.py:25); transcript_segment guarda o texto da transcrição, run_log os dados da execução, moment os momentos (nome, início e fim) e service os dados do culto, com o campo pregador (0001_init.sql:3-4,14-15,18). F5.6 cria a tabela de execuções liberadas (F5.6.T3, segundo a revisão da árvore) e F7.6 os indicadores de qualidade por culto, parte deles hoje no run_log (cobertura_pct, processar_culto.py:105; árvore, F7.6). D7 também registra a decisão sobre a exceção da P26: com ANTHROPIC_API_KEY, a transcrição do culto, até 60000 caracteres, e os sinais agregados vão à API da Anthropic (reacao/moments.py:48-61), e os insights são reescritos por ela (reacao/insights.py:32-36); sem a chave, os momentos saem da heurística e os insights do modelo de frase (P26; docs/onprem.md:50-52). Os comandos documentados passam a chave hoje (docs/hf-jobs.md:16), e F5.5 compara a segmentação por LLM e por heurística (árvore, F5.5). Pela documentação do Supabase, a chave publishable pode ficar no navegador com RLS habilitada e a secret ignora RLS e só pode ficar em componente de servidor (https://supabase.com/docs/guides/getting-started/api-keys). A região das funções de um projeto na Vercel é configurável (https://vercel.com/docs/functions/configuring-functions/region), dado que o RIPD de F6.3 precisa. O time 'Fabio Pinheiro's projects' da Vercel tem só o projeto ai-guitar-coach-pilot (Vercel list_projects, 2026-09-23). D7 também decide onde fica o vínculo entre conta e papel e se a regra 6 do CLAUDE.md ('Tabelas do Supabase não têm campo por pessoa', CLAUDE.md:21) vale para as contas da equipe. F5.6 grava na Fase 0 o papel de avaliador do gate de Fabio e Filipe e propõe guardá-lo em app_metadata do Supabase Auth, campo que o usuário não altera (F5.6 RN05 e F5.6.T3; https://supabase.com/docs/guides/database/postgres/row-level-security); na árvore essa decisão ficava em F6.2, depois do gate, e F7.2 RN06 prevê as duas saídas (app_metadata, se a regra valer; exceção no CLAUDE.md e tests/test_schema.py ampliado, se não valer). tests/test_schema.py lê só supabase/migrations/*.sql (tests/test_schema.py:9-12). D8: plano e termos de uso da Vercel para este projeto, a confirmar pela task que a revisão move de F7.2.T2 para o início de F5.6; times Hobby só podem ter uso pessoal não comercial (https://vercel.com/docs/limits/fair-use-guidelines). D9: decisões do painel web que F5.6 lê do ADR (F5.6.T1, F5.6.T2, F5.6.T3 e premissas de F5.6): projeto novo no time 'Fabio Pinheiro's projects', framework ('sem frameworks além do necessário', CLAUDE.md:30), método de login do Supabase Auth, proteção de deployment (no Hobby, a Vercel Authentication admite um usuário externo por conta, https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/vercel-authentication) e validade do token de acesso (a documentação recomenda o padrão de 1 hora, https://supabase.com/docs/guides/auth/sessions, e um papel retirado de app_metadata só some do JWT quando o token é renovado, https://supabase.com/docs/guides/database/postgres/row-level-security).

**Regras de negócio:**
- RN01 – O ADR 0002 registra a fronteira da P3 revisada como decisão do usuário, sem reabri-la.
- RN02 – A chave de serviço do Supabase fica só nos segredos dos jobs do HF e no local de guarda de quem lança; o painel web usa a chave pública, com Supabase Auth e RLS por perfil.
- RN03 – A Vercel não recebe vídeo, quadro, recorte de rosto nem observação por rosto.
- RN04 – Fabio e Filipe acessam relatório e notas pelo painel web na Vercel; o acesso por Space vale só para a ferramenta de rotulagem.
- RN05 – O envio dos vídeos do piloto vai direto ao destino privado no HF, sem passar pela Vercel.
- RN06 – Cada decisão cita as opções avaliadas e a fonte de cada restrição.
- RN07 – Plano e termos de uso da Vercel ficam como pendência com responsável até confirmação; o ADR não os trata como fato.
- RN08 – Se a imagem for pública, os pesos não entram nela e são carregados dos repositórios privados de F2.3.
- RN09 – Uma opção de registro que não permite referência por digest, como a Docker Space, só é escolhida com exceção declarada a RN01 e RN09 da Feature, e a exceção cita as tasks que F2.2 e F2.6 precisam ganhar.
- RN10 – D2 registra, para cada composição avaliada, a versão do Py-Feat e do torch que a resolução de pacotes permite, e decide a versão exata do py-feat, diferente de 0.6.2, e a do libreface (0.2.0), que F2.1 fixa no lock.
- RN11 – D7 lista as tabelas do Supabase que o painel web lê e escreve. Lê window_aggregate, event e insight e, se D7 registrar, moment (P3 revisada), a tabela de execuções liberadas de F5.6 e, na Fase 1, os indicadores de qualidade de F7.6. Escreve insight_feedback (notas do critério 4 e do pastor) e, na Fase 1, só o estado de revisão do insight (F7.3). transcript_segment, run_log e service ficam fora.
- RN12 – D7 registra a decisão de Fabio sobre a exceção da P26 na Fase 0 (envio da transcrição de cultos públicos à API da Anthropic). Sem a confirmação, os jobs rodam sem ANTHROPIC_API_KEY. A decisão para os cultos do piloto fica com F6.3 (P26).
- RN13 – D7 decide, antes de F5.6, se a regra 6 vale para as contas da equipe (Fabio, Filipe, contas de teste e, na Fase 1, pastor, revisor, mídia e DPO) e onde fica o vínculo entre conta e papel. F5.6.T3 grava os papéis conforme essa decisão, e F6.2 só a confirma ou ajusta, com migração se mudar.
- RN14 – D8 registra plano e termos de uso da Vercel como pendência com Fabio como responsável e aponta para a task de F5.6, movida de F7.2.T2, que os confirma antes de F5.6.T1.
- RN15 – D9 registra as decisões do painel web que F5.6 aplica: projeto, framework, método de login do Supabase Auth, proteção de deployment e validade do token de acesso, cada uma com as opções avaliadas e a fonte.

**Fora de escopo:**
- Criação do projeto na Vercel e do painel (F5.6)
- Implementação das políticas de RLS e gravação dos papéis (F5.6, F7.2 e F7.8); D7 decide só o local do vínculo e a regra 6 para as contas da equipe
- Schema da tabela de execuções liberadas (F5.6) e dos indicadores de qualidade (F7.6)
- Construção do Space de rotulagem (F3.3)
- Criação do destino dos vídeos do piloto (F7.1)
- Publicação da imagem (F2.2)
- Entrega da ANTHROPIC_API_KEY aos jobs (F2.6.T2)
- Decisão sobre a API da Anthropic nos cultos do piloto (F6.3)
- Criação de organização no HF ou contratação de plano, que dependem de Fabio
- Confirmação do plano e dos termos de uso da Vercel (task de F5.6 movida de F7.2.T2)
- Implementação do painel, do diretório com lockfile e do CI do painel (F5.6.T1 e F5.6.T2)

#### Critérios de aceite

- docs/adr/0002-*.md está em main, com status aceito, data e aprovação de Fabio.
- O ADR tem uma decisão para cada item de D1 a D7 e de D9 do contexto, com as opções avaliadas e a fonte de cada restrição citada.
- Cada opção de D3 está avaliada contra a referência por digest exigida por RN01 e RN09 da Feature, com fonte.
- D2 registra, para cada composição avaliada, a versão do Py-Feat e do torch que a resolução de pacotes permite, e decide a versão exata do py-feat, diferente de 0.6.2, e a do libreface.
- O ADR lista o que o painel web na Vercel recebe (URL do projeto Supabase e chave pública) e o que não recebe (chave de serviço, vídeo, quadro, recorte de rosto e observação por rosto).
- O ADR lista as tabelas do Supabase que o painel web lê e as que escreve, registra a decisão sobre moment e exclui transcript_segment, run_log e service.
- O ADR registra a decisão de Fabio sobre a exceção da P26 na Fase 0 (aceita ou não aceita), com data, e o que os jobs usam sem ANTHROPIC_API_KEY (heurística de momentos e modelo de frase).
- O ADR registra se a regra 6 vale para as contas da equipe e onde fica o vínculo entre conta e papel, com as opções avaliadas e a fonte de cada uma.
- O ADR registra plano e termos de uso da Vercel como pendência com Fabio como responsável, e não como decisão tomada, e aponta para a task de F5.6 que os confirma.
- D9 registra o projeto do painel no time 'Fabio Pinheiro's projects', o framework, o método de login do Supabase Auth, a proteção de deployment e a validade do token de acesso.
- O ADR diz o que muda no modelo de acesso se a assinatura PRO não for renovada depois do periodEnd de 2026-10-01.
- Num Space vazio de teste criado com o modelo de acesso escolhido para a rotulagem, uma conta da lista de acesso abre o Space.
- No mesmo Space, uma conta fora da lista não abre o Space e recebe acesso negado ou 404.
- O resultado do teste de acesso está registrado no ADR, e o Space de teste foi apagado depois do teste.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F2.4.T1 | DevOps | Redigir as decisões D1 a D3: modo de execução, composição da imagem e registro | 6 | — |
| F2.4.T2 | MLOps | Redigir a decisão D4: namespace dos repositórios, do Space de rotulagem e do destino do piloto | 3 | — |
| F2.4.T3 | DevOps | Redigir a decisão D5: SDK do Space de rotulagem | 2 | — |
| F2.4.T4 | Governança e Privacidade | Redigir D6 a D8: acesso no HF, fronteira de dados e credenciais, tabelas do painel, vínculo entre conta e papel, exceção da P26 e pendência da Vercel | 6 | — |
| F2.4.T5 | DevOps | Criar o Space vazio de teste com o modelo de acesso escolhido | 2 | F2.4.T2, F2.4.T3, F2.4.T4, Organização criada por Fabio, se D4 ou D6 escolherem organização |
| F2.4.T6 | QA | Testar o acesso ao Space de teste e conferir o rascunho do ADR contra os critérios 2 a 14 | 3 | F2.4.T1, F2.4.T5, F2.4.T8 |
| F2.4.T7 | Governança e Privacidade | Consolidar o ADR 0002, obter o aceite de Fabio e mesclar em main | 3 | F2.4.T6 |
| F2.4.T8 | Front end | Redigir a decisão D9: projeto, framework, login, proteção de deployment e validade do token do painel web | 4 | F2.4.T4 (D7: tabelas do painel e vínculo entre conta e papel) |

<details><summary>F2.4.T1 · [DevOps] Redigir as decisões D1 a D3: modo de execução, composição da imagem e registro</summary>

**Objetivo:** Seções D1 a D3 do ADR 0002 com opções e fontes.

**Passos previstos:**
1. Comparar 'hf jobs run' pela imagem com 'hf jobs uv run' para o gate, o piloto e o desenvolvimento.
2. Comparar uma imagem com os três motores e uma imagem por motor (tamanho, tempo de build, jobs por motor) e registrar para cada uma a versão do Py-Feat e do torch que a resolução permite.
3. Decidir em D2 a versão exata do py-feat (0.6.1 ou 2.1.3, nunca 0.6.2) e registrar libreface 0.2.0, com os insumos de F4 para as duas opções (Python, torch e dlib).
4. Comparar GHCR público, GHCR privado e Docker Space privada, avaliando cada um contra a referência por digest (RN01 e RN09 da Feature) e contra as restrições de https://huggingface.co/docs/hub/jobs-images.
5. Registrar onde ficam os pesos conforme a visibilidade da imagem.

**Definição de pronto:** Seções D1 a D3 no rascunho, com fonte para cada restrição, avaliação de digest por opção de registro e a versão exata do py-feat e do libreface em D2.

**Dependências:** nenhuma

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F2.4.T2 · [MLOps] Redigir a decisão D4: namespace dos repositórios, do Space de rotulagem e do destino do piloto</summary>

**Objetivo:** Tabela recurso, namespace, quem escreve e quem lê.

**Passos previstos:**
1. Listar repositórios de modelo, repositório de resultados, Space de rotulagem, destino dos vídeos do piloto e bucket jobs-artifacts.
2. Comparar namespace pessoal e de organização, considerando papel de escrita para Jobs de organização.
3. Propor nomes dos recursos.

**Definição de pronto:** Seção D4 no rascunho com a tabela completa.

**Dependências:** nenhuma

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F2.4.T3 · [DevOps] Redigir a decisão D5: SDK do Space de rotulagem</summary>

**Objetivo:** Seção D5 com o SDK escolhido e o plano que ele exige.

**Passos previstos:**
1. Comparar Gradio e Docker (https://huggingface.co/docs/hub/spaces-config-reference).
2. Registrar o requisito de arquivos temporários só em /dev/shm (P9).
3. Registrar o plano exigido pelo SDK escolhido.

**Definição de pronto:** Seção D5 no rascunho com fonte.

**Dependências:** nenhuma

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F2.4.T4 · [Governança e Privacidade] Redigir D6 a D8: acesso no HF, fronteira de dados e credenciais, tabelas do painel, vínculo entre conta e papel, exceção da P26 e pendência da Vercel</summary>

**Objetivo:** Seções D6 a D8 do ADR revisadas por Fabio, com a lista de tabelas do painel, o local do vínculo entre conta e papel, a regra 6 para as contas da equipe e a decisão dele sobre a exceção da P26.

**Passos previstos:**
1. D6: comparar organização com papel de escrita, Space protected com OAuth e hf_oauth_authorized_org e token fine-grained restrito ao destino do piloto, e descrever o que muda se a assinatura PRO não for renovada depois do periodEnd de 2026-10-01.
2. D7: montar a tabela dado ou credencial por HF, Supabase, Vercel e local de guarda de quem lança, conforme a P3 revisada, incluindo a ANTHROPIC_API_KEY e a região das funções na Vercel para o RIPD de F6.3.
3. D7: listar as tabelas que o painel lê (window_aggregate, event, insight, moment se D7 registrar, execuções liberadas de F5.6 e, na Fase 1, indicadores de F7.6) e escreve (insight_feedback e, na Fase 1, o estado de revisão do insight de F7.3), excluir transcript_segment, run_log e service e levar ao usuário a confirmação da leitura da tabela de execuções liberadas na Fase 0.
4. D7: decidir se a regra 6 vale para as contas da equipe e, com isso, onde fica o vínculo entre conta e papel: em app_metadata do Supabase Auth, fora das tabelas do produto (proposta de F5.6), ou numa tabela de vínculo, com a exceção registrada no CLAUDE.md e tests/test_schema.py ampliado (F7.2 RN06).
5. D7: apresentar a Fabio a exceção da P26 (o que vai à API da Anthropic, conforme reacao/moments.py:48-61 e reacao/insights.py:32-36, e o caminho sem a chave) e registrar a decisão dele para a Fase 0, com data.
6. D8: registrar plano e termos de uso da Vercel como pendência com Fabio como responsável e apontar para a task de F5.6, movida de F7.2.T2, que os confirma antes de F5.6.T1.
7. Revisar com Fabio.

**Definição de pronto:** Seções D6 a D8 no rascunho, com a lista de tabelas do painel, o local do vínculo entre conta e papel, a regra 6 para as contas da equipe, a decisão sobre a exceção da P26 e o apontamento de D8 para a task de F5.6, revisadas por Fabio.

**Dependências:** nenhuma

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F2.4.T5 · [DevOps] Criar o Space vazio de teste com o modelo de acesso escolhido</summary>

**Objetivo:** Space vazio configurado com a visibilidade e o acesso de D6.

**Passos previstos:**
1. Confirmar que o namespace de D4 existe e que quem cria tem papel de escrita nele.
2. Criar o Space vazio no namespace de D4 com a visibilidade e o acesso de D6.
3. Cadastrar a lista de acesso de teste.
4. Apagar o Space depois de F2.4.T6.

**Definição de pronto:** Space criado e, depois do teste, apagado.

**Dependências:** F2.4.T2, F2.4.T3, F2.4.T4, Organização criada por Fabio, se D4 ou D6 escolherem organização

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F2.4.T6 · [QA] Testar o acesso ao Space de teste e conferir o rascunho do ADR contra os critérios 2 a 14</summary>

**Objetivo:** Resultado do teste de acesso registrado e conferência do rascunho anexada.

**Passos previstos:**
1. Abrir o Space com uma conta da lista.
2. Abrir o Space com uma conta fora da lista e registrar a resposta.
3. Registrar o resultado no rascunho do ADR.
4. Conferir o rascunho contra os critérios 2 a 14, inclusive a lista de tabelas do painel, o vínculo entre conta e papel, a decisão sobre a exceção da P26, o apontamento de D8 e as decisões de D9.

**Definição de pronto:** Resultado dos dois acessos no rascunho do ADR e checklist dos critérios 2 a 14 anexada ao PBI.

**Dependências:** F2.4.T1, F2.4.T5, F2.4.T8

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F2.4.T7 · [Governança e Privacidade] Consolidar o ADR 0002, obter o aceite de Fabio e mesclar em main</summary>

**Objetivo:** ADR 0002 em main com status aceito.

**Passos previstos:**
1. Juntar as seções D1 a D9 e o resultado do teste de acesso em docs/adr/0002-<nome>.md, com status e data.
2. Abrir o PR citando o PBI.
3. Obter a revisão e a aprovação de Fabio no PR.
4. Mesclar em main.

**Definição de pronto:** docs/adr/0002-*.md em main com status aceito, data e aprovação de Fabio registrada no PR.

**Dependências:** F2.4.T6

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F2.4.T8 · [Front end] Redigir a decisão D9: projeto, framework, login, proteção de deployment e validade do token do painel web</summary>

**Objetivo:** Seção D9 do ADR 0002 com as decisões que F5.6 aplica no painel web na Vercel, com opções avaliadas e fontes.

**Passos previstos:**
1. Registrar o projeto novo do painel no time 'Fabio Pinheiro's projects', separado de ai-guitar-coach-pilot (Vercel list_projects, 2026-09-23), e propor o nome.
2. Comparar as opções de framework do painel pela regra 'sem frameworks além do necessário' (CLAUDE.md:30), considerando a leitura com a chave pública e a sessão do Supabase Auth no navegador (https://supabase.com/docs/guides/getting-started/api-keys).
3. Comparar os métodos de login do Supabase Auth para contas convidadas com cadastro fechado (F5.6 RN04).
4. Decidir se a Vercel Authentication fica ligada no domínio de produção, registrando que no Hobby ela admite um usuário externo por conta (https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/vercel-authentication).
5. Decidir a validade do token de acesso (manter o padrão de 1 hora, reduzi-la ou conferir a sessão nas políticas), registrando que um papel retirado só some do JWT quando o token é renovado (https://supabase.com/docs/guides/auth/sessions; https://supabase.com/docs/guides/database/postgres/row-level-security).
6. Registrar o que fica para F5.6.T1 decidir (gerenciador de pacotes, versão do Node, lint e executor de testes).

**Definição de pronto:** Seção D9 no rascunho do ADR com projeto, framework, método de login, proteção de deployment e validade do token, cada um com opções avaliadas e fonte.

**Dependências:** F2.4.T4 (D7: tabelas do painel e vínculo entre conta e papel)

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- docs/adr/0001-motor.md
- Dockerfile:1-2,11-12
- .github/workflows/docker.yml:1-25
- docs/hf-jobs.md:13-38
- docs/onprem.md:50-52
- supabase/migrations/0001_init.sql:3-4,14-18
- reacao/insights.py:25,32-36
- reacao/moments.py:48-61
- processar_culto.py:105
- huggingface_hub/_jobs_api.py:96 e hf_api.py:12165,12818,13590-13680 (instalados)
- https://pypi.org/pypi/libreface/0.2.0/json
- https://pypi.org/pypi/py-feat/2.1.3/json
- lock310.txt do levantamento
- https://huggingface.co/docs/hub/jobs-images
- https://huggingface.co/docs/huggingface_hub/guides/jobs#run-a-job
- https://huggingface.co/docs/hub/spaces-sdks-docker#permissions
- https://huggingface.co/docs/hub/spaces-overview#space-visibility
- https://huggingface.co/docs/hub/spaces-oauth
- https://huggingface.co/docs/hub/spaces-config-reference
- https://huggingface.co/docs/hub/repositories-settings
- whoami do HF: papel read em impacto-cognitivo e periodEnd do PRO 2026-10-01 (2026-09-23)
- https://supabase.com/docs/guides/getting-started/api-keys
- https://vercel.com/docs/functions/configuring-functions/region
- Vercel list_teams e list_projects (2026-09-23)
- P3 revisada pelo usuário
- Árvore: F4.2, F5.5, F7.6; premissas P11, P24, P26 e P27
- Revisão da árvore: F5.6.T3 (tabela de execuções liberadas) e F5.8
- CLAUDE.md:21 (regra 6) e CLAUDE.md:30
- tests/test_schema.py:9-12
- https://vercel.com/docs/limits/fair-use-guidelines
- https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/vercel-authentication
- https://supabase.com/docs/guides/auth/sessions
- Feature F4 detalhada: F4.2 e pendência para F2.4 (py-feat 0.6.1 ou 2.1.3; 0.6.2 excluída pela regra 2)
- Feature F5 detalhada: F5.6 (RN05, RN06, F5.6.T1 a F5.6.T3 e premissas sobre framework, login, proteção de deployment, validade do token e vínculo)
- Feature F7 detalhada: F7.2 (RN03, RN06 e F7.2.T2) e pendência para F5.6 e D8

#### Verificação INVEST: pontos que falharam
- Small: 8 tasks e cerca de 29 h sugeridas, uma task acima do limite de 7 (ver premissas).

#### Premissas
- A fronteira de dados e credenciais entre HF, Supabase e Vercel é decisão do usuário (P3 revisada); o ADR a registra.
- Fabio e Filipe não precisam de acesso ao HF para o relatório e as notas, que ficam no painel web. Se Filipe também rotular, entra na lista de acesso do Space de rotulagem (a confirmar).
- Como o repositório GitHub é público, uma imagem pública no GHCR não pode conter pesos de licença restrita (dedução).
- O periodEnd do PRO devolvido pelo whoami não indica cancelamento; que a assinatura termine nessa data é hipótese a confirmar com Fabio.
- Nomes de repositórios e tags são decididos aqui ou nos PBIs que os criam (P24).
- Com a P3 revisada ('e momentos, se o ADR de F2.4 registrar'), D7 decide a leitura de moment sem nova consulta ao usuário; o relatório de F5.8 mostra momentos. service fica fora porque não está na lista da P3 revisada e tem o campo pregador (0001_init.sql:3-4). transcript_segment fica fora porque o trecho citado vem de insight.trecho (0001_init.sql:16; reacao/insights.py:25). insight_feedback entra porque a P3 revisada põe as notas do critério 4 no painel.
- A tabela de execuções liberadas (F5.6) e os indicadores de F7.6 são citados pelo PBI que os cria; D7 não define o schema deles.
- A tabela de execuções liberadas de F5.6 e os indicadores de F7.6 entram em D7 porque a P3 revisada põe a revisão e liberação e a sinalização de qualidade no painel e porque não têm observação por rosto (dedução); a leitura da tabela de execuções liberadas na Fase 0 fica a confirmar com o usuário, como F5.6 registra.
- O critério 1 é verificado na definição de pronto de F2.4.T7, com revisão e aceite de Fabio; F2.4.T6 (QA) confere os critérios 2 a 14 no rascunho, antes do aceite.
- Disciplinas: DevOps, MLOps, Governança e Privacidade e QA, como na árvore, e Front end, por D9.
- Story points e horas são sugestão.
- A proposta de F5.6 para o vínculo (e-mails em auth.users do Supabase Auth; papel e código de avaliador sem nome em app_metadata) é o ponto de partida de D7. A leitura de que a regra 6 e tests/test_schema.py não alcançam o schema auth é dedução, que D7 confirma ou recusa.
- D9 existe porque F5.6.T1, F5.6.T2, F5.6.T3 e as premissas de F5.6 leem do ADR de F2.4 o framework, a proteção de deployment, o método de login e a validade do token de acesso (Feature F5 detalhada).
- A task de F5.6 que confirma plano e termos não existe no estado atual de F5 (feature_det_F5.json); D8 a cita pelo título até a ref existir.
- Com F2.4.T8, o PBI tem 8 tasks, uma acima do limite de 7 (taskflow.md, seção 2). Se o refinamento preferir 7, D9 pode ir para F2.4.T3, que já redige a decisão de SDK do Space.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável.
- Item pai: Feature F2.
- Depois do aceite, citar o ADR 0002 nos PBIs F2.1, F2.2, F2.3, F2.5, F2.6, F2.8, F3.3, F5.4, F5.5, F5.6, F5.8, F6.2, F7.1, F7.2, F7.6 e F7.8.
- Plano e termos de uso da Vercel: confirmados por Fabio na task de F5.6 movida de F7.2.T2; preencher em D8 a ref dessa task quando F5 a criar.
- Renovação da assinatura PRO: confirmar com Fabio.
- Confirmar com o usuário a leitura da tabela de execuções liberadas de F5.6 pelo painel na Fase 0.
- Informar F5.4 (F5.4.T4), F5.5 (F5.5.T3) e F5.6 (F5.6.T7, antes F5.6.T6) de que dependem da decisão de D7 sobre a exceção da P26.
- Informar F5.8 (F5.8.T2) de que confere as tabelas lidas pelo painel contra a lista de D7.
- Informar F7.6 de que o painel não lê run_log.
- Informar F5.6 (F5.6.T1, F5.6.T2 e F5.6.T3) de que D9 e D7 trazem as decisões que essas tasks aplicam.
- Informar F6.2, F7.2 e F7.8 de que o vínculo entre conta e papel e a regra 6 para as contas da equipe estão em D7.
- Informar F7.2 (RN03) de que D7 deixa transcript_segment, run_log e service fora do painel.

## Preview — PBI F2.5 (novo) · Separar por run_id as linhas de cada execução no Supabase, com regravação sem duplicar e registro da falha com etapa e mensagem

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Separar por run_id as linhas de cada execução no Supabase, com regravação sem duplicar e registro da falha com etapa e mensagem |
| Tipo | Product Backlog Item |
| Pai | F2 |
| Tags | F2; run_id; Supabase; Backend; linhagem |
| Estimativa | 5 pts (sugestão); tasks: 19 h |
| Dependências | F1.5 (contrato do run_log e flavor real), F2.6 (Supabase de desenvolvimento com RLS, destino explícito e entrega da chave de serviço ao job), F2.2 (imagem com digest para o job de verificação), Aprovação de Fabio para os jobs de verificação |
| Substitui | nenhum |

#### Descrição

Como integrante do time de ML e visão computacional que lê os resultados de cada execução no Supabase  
Quero que cada execução de processar_culto.py grave um run_id em todas as tabelas de resultado, que regravar a mesma execução não duplique linhas nem altere as notas do critério 4 e que uma falha deixe no run_log a etapa e a mensagem  
Para que reprocessar um culto, com o mesmo motor ou com outro, não misture linhas, e que uma execução que falhou seja identificável pelo run_id

**Contexto:** window_aggregate, transcript_segment, moment, event, insight e run_log se ligam só pelo texto culto (supabase/migrations/0001_init.sql:6-18). O Store faz POST sem upsert, e o destino local grava JSON em modo append (reacao/store.py:20,24-26). insight_feedback referencia insight(id) sem ON DELETE (0001_init.sql:17), então apagar um insight que tem nota falha por chave estrangeira. O run_log só é gravado no caminho de sucesso (processar_culto.py:103-107), e as etapas marcadas no tempo são carga, video, transcricao e analise (processar_culto.py:65,79,90,101). tests/test_schema.py proíbe campos por pessoa nas migrações. Pela P3 revisada, a chave de serviço só entra nos jobs do HF, então a gravação no Supabase é verificada por job, e os testes fora do HF usam o destino local. F2.6 torna explícito o destino dos resultados e faz o job falhar sem credencial. A documentação diz só que um job para ao atingir o timeout (https://huggingface.co/docs/hub/jobs-configuration#timeout).

**Regras de negócio:**
- RN01 – Cada execução tem um run_id único, gerado no início ou recebido do lançamento quando se reexecuta a mesma execução, gravado em todas as linhas de window_aggregate, transcript_segment, moment, event, insight e run_log.
- RN02 – Regravar a mesma execução não duplica linhas: a gravação é por upsert na chave única de cada tabela (run_id mais os campos que identificam a linha), sem apagar linhas de insight.
- RN03 – Regravar um run_id não altera nem apaga notas de insight_feedback.
- RN04 – Nenhuma coluna nova identifica pessoa (regra 6); tests/test_schema.py continua valendo.
- RN05 – Uma exceção numa etapa grava no run_log registro com run_id, estado de falha, etapa, tipo e mensagem do erro, sem valor de segredo, e o processo termina com código diferente de zero.
- RN06 – O estado de jobs parados por timeout ou cancelados vem do HF (F7.5); o registro deste PBI cobre o que o processo consegue gravar.
- RN07 – Testes fora do HF usam a fixture sintética, o motor mock e o destino local (RN10 da Feature). A gravação no Supabase é verificada por job no HF, com aprovação de Fabio.

**Fora de escopo:**
- Linhagem e envio ao repositório de resultados (F2.8)
- run_id e registro de falha do bench, que não grava no Supabase (F2.8)
- Disparo e consulta dos jobs do piloto (F7.5)
- Escolha do run_id exibido no painel web (F5.6)
- Retenção dos resultados (F7.4)

#### Critérios de aceite

- Cada linha gravada em window_aggregate, transcript_segment, moment, event, insight e run_log tem run_id preenchido.
- Duas execuções do mesmo culto geram linhas com run_id diferentes, e a consulta por run_id devolve só as linhas de cada execução.
- Regravar a mesma execução, com o mesmo run_id, não aumenta o número de linhas de nenhuma tabela.
- Regravar um run_id cujos insights têm nota em insight_feedback termina sem erro, e as notas continuam iguais.
- Nenhuma coluna das tabelas de resultado tem nome da lista proibida da regra 6.
- Quando uma etapa levanta exceção, o run_log recebe registro com run_id, etapa, tipo e mensagem do erro, e o processo termina com código diferente de zero.
- Com um segredo definido no ambiente e um erro que o incluiria na mensagem, o registro de falha não contém o valor do segredo.
- Com destino local, duas execuções do mesmo culto ficam separadas por run_id nos arquivos JSON.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F2.5.T1 | Backend | Adicionar run_id e chave única às seis tabelas de resultado e gravar por upsert | 8 | F1.5, F2.6 |
| F2.5.T2 | Backend | Gerar o run_id no início de processar_culto.py e gravar a falha por etapa | 6 | F2.5.T1 |
| F2.5.T3 | QA | Verificar os critérios de aceite de F2.5 | 5 | F2.5.T2, Aprovação de Fabio |

<details><summary>F2.5.T1 · [Backend] Adicionar run_id e chave única às seis tabelas de resultado e gravar por upsert</summary>

**Objetivo:** Linhas separadas por run_id e regravação sem duplicar nem apagar insight.

**Passos previstos:**
1. Criar migração com run_id, chave única por tabela (run_id mais os campos que identificam a linha) e índice em window_aggregate, transcript_segment, moment, event, insight e run_log, e colunas de estado, etapa, tipo e mensagem do erro no run_log.
2. Alterar o Store para enviar run_id e gravar por upsert na chave única, sem apagar linhas de insight.
3. Separar por run_id o destino local.
4. Escrever testes de upsert e de consulta por run_id com o destino local e manter tests/test_schema.py aprovado.

**Definição de pronto:** Migração aplicada no Supabase de desenvolvimento pela conta de Fabio, testes locais aprovados e tests/test_schema.py aprovado.

**Dependências:** F1.5, F2.6

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F2.5.T2 · [Backend] Gerar o run_id no início de processar_culto.py e gravar a falha por etapa</summary>

**Objetivo:** run_id único por execução e registro de falha com etapa e mensagem sem segredo.

**Passos previstos:**
1. Gerar o run_id no início de processar_culto.py ou recebê-lo do lançamento.
2. Envolver as etapas carga, video, transcricao e analise para capturar exceção com etapa, tipo e mensagem.
3. Remover da mensagem qualquer valor de variável de segredo antes de gravar.
4. Gravar a falha no run_log (Supabase ou destino local) e terminar com código diferente de zero.
5. Escrever teste que injeta erro contendo o valor de um segredo.

**Definição de pronto:** Testes locais aprovados com destino local: falha gravada com etapa, sem o valor do segredo, e código de saída diferente de zero.

**Dependências:** F2.5.T1

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F2.5.T3 · [QA] Verificar os critérios de aceite de F2.5</summary>

**Objetivo:** Evidência de cada critério de aceite anexada ao PBI.

**Passos previstos:**
1. Rodar localmente, com a fixture, o motor mock e o destino local, duas execuções do mesmo culto, uma regravação com o mesmo run_id e os casos de falha (exceção numa etapa e segredo na mensagem).
2. Inserir pelo editor SQL do projeto de desenvolvimento, na sessão de Fabio, um insight e uma nota de teste ligados a um run_id.
3. Pedir aprovação a Fabio e rodar, pela imagem com digest que contém F2.5.T1 e F2.5.T2, dois jobs com o motor mock sobre a fixture lida por URI hf://datasets/ na revisão de tests/fixtures/README.md (F1.1.T6) para o mesmo culto, uma reexecução com o mesmo run_id e um job com vídeo inexistente no dataset.
4. Conferir run_id nas seis tabelas, a contagem de linhas, as notas de teste inalteradas e o registro de falha na etapa carga.
5. Apagar as linhas de teste.

**Definição de pronto:** Checklist dos 8 critérios com JOB_IDs, consultas e contagens anexada ao PBI.

**Dependências:** F2.5.T2, Aprovação de Fabio

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- supabase/migrations/0001_init.sql:6-18
- reacao/store.py:16-44
- processar_culto.py:59-65,79,90,101,103-107
- tests/test_schema.py
- https://huggingface.co/docs/hub/jobs-configuration#timeout
- P3 revisada pelo usuário
- Árvore: F1.5, F5.6, F7.5; premissa P6

#### Premissas
- F2.5 da árvore foi dividido em F2.5 (este PBI) e F2.8 (linhagem e repositório de resultados), candidato registrado em P6.
- O run_id é gerado pelo próprio job no início e não depende de JOB_ID, para valer também fora do HF; o lançamento pode informar um run_id para reexecutar a mesma execução. O formato é decisão da task.
- A separação por run_id não depende do motor; o job de verificação usa o motor mock duas vezes para não depender dos pesos de F2.3. O job com motor real está em F2.8.
- O critério 4 é verificado com um insight e uma nota de teste inseridos pelo editor SQL do projeto de desenvolvimento, na sessão de Fabio e sem a chave de serviço, porque a fixture com o motor mock pode não gerar insight (dedução).
- A migração é aplicada por Fabio pela conta do Supabase, sem a chave de serviço.
- Disciplinas: Backend e QA. MLOps, DevOps e Data Science, previstas na árvore para o F2.5 original, ficaram com F2.8, que recebeu a linhagem, o envio e o comando de lançamento.
- Story points e horas são sugestão.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável.
- Item pai: Feature F2.
- Informar F5.6 de que o painel escolhe o run_id exibido por culto.
- Informar F7.5 da RN06.

## Preview — PBI F2.6 (novo) · Configurar tokens de escopo mínimo, a entrega de segredos aos jobs a partir de quem lança, o inventário de credenciais e o projeto Supabase de desenvolvimento com RLS habilitada e testada no CI

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Configurar tokens de escopo mínimo, a entrega de segredos aos jobs a partir de quem lança, o inventário de credenciais e o projeto Supabase de desenvolvimento com RLS habilitada e testada no CI |
| Tipo | Product Backlog Item |
| Pai | F2 |
| Tags | F2; segredos; tokens; Supabase; RLS; DevOps; Governança |
| Estimativa | 8 pts (sugestão); tasks: 29 h |
| Dependências | F1.5 (migração com insights_rejeitados_pelo_lint, para F2.6.T3, e configuração local do Supabase CLI em F1.5.T1, para F2.6.T4), F2.4 (namespace dos repositórios, que define o escopo dos tokens; fronteira D7 e decisão sobre a exceção da P26), F2.1.T6 (forma dos segredos em docs/hf-jobs.md), para F2.6.T2, F2.2.T2 (publicação da imagem por tag com digest), só para F2.6.T7; F2.6.T1 a F2.6.T6 não dependem de F2.2, F1.1 (guarda corrigida antes de qualquer job e fixture sintética no dataset por revisão, F1.1.T6), para F2.6.T7; F1.1.T6 também para F2.6.T6, que registra o token de uso único do envio, Acesso de Fabio às contas do HF e do Supabase, Aprovação de Fabio para o job de fumaça e, se o projeto Supabase for criado, para o custo mensal |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro, dono das contas do HF e do Supabase  
Quero tokens do HF separados por uso e com escopo mínimo, prontos antes do primeiro job pago; o token dos jobs, a chave de serviço e, se o ADR 0002 aceitar a exceção da P26, a ANTHROPIC_API_KEY entregues ao job por '--secrets-file -' a partir do local de guarda de quem lança; e o projeto Supabase de desenvolvimento com as migrações aplicadas e RLS habilitada em todas as tabelas; um inventário único de credenciais que também receba os tokens de uso único e os segredos guardados em Jobs automáticos; e um job de CI que suba o Supabase local com as migrações e teste a RLS  
Para que um token vazado dos jobs ou do CI não escreva no corpus, que o job não receba o token de quem lança, que nenhum valor de segredo apareça em comando ou log e que a chave pública, a única que o painel web na Vercel recebe, não leia nada sem política, e que as políticas de F5.6, F5.7 e F7.2 tenham onde ser testadas antes do gate

**Contexto:** O HF_TOKEN do ambiente de levantamento é um token clássico com papel write (whoami do HF, 2026-09-23). A documentação recomenda tokens fine-grained, um por uso (https://huggingface.co/docs/hub/security-tokens#best-practices), e o CI pode publicar no Hub por Trusted Publishers com token de 1 h (https://huggingface.co/docs/hub/trusted-publishers). Os valores dos segredos saem do ambiente de quem lança, a cada lançamento (https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets; huggingface_hub/cli/jobs.py:286), e um job não recebe token do HF se nenhum for passado (mesma página). Na forma '--secrets HF_TOKEN', a CLI resolve o nome num ambiente em que HF_TOKEN recebe o token com que ela própria se autentica (huggingface_hub/cli/_cli_utils.py:926-933,953-969; a documentação descreve a forma como 'pass your local Hugging Face token implicitly'); para enviar ao job outro token, o valor vai por '--secrets-file -', lido do stdin (cli/_cli_utils.py:936-951). O resumo do --dry-run mascara os valores dos segredos (cli/jobs.py:392-402), e 'hf jobs inspect' mostra os valores de -e e só os nomes dos segredos (https://huggingface.co/docs/hub/jobs-manage#inspect-a-job). docs/hf-jobs.md:14-17 passa segredos com valor, inclusive ANTHROPIC_API_KEY (docs/hf-jobs.md:16); sem a chave, os momentos usam a heurística e os insights o modelo de frase (reacao/moments.py:48-50; reacao/insights.py:32-36), e o envio da transcrição de cultos públicos à API da Anthropic depende da confirmação de Fabio, registrada em D7 do ADR 0002 (P26; F2.4). Os tokens de F2.6.T1 e o procedimento de F2.6.T2 são pré-requisito do primeiro job pago (F2.2.T4), para que ele não seja lançado com o token clássico de escrita que F3.1.T3 revoga (Feature F3, F3.1.T3). O projeto Supabase deste sistema não foi encontrado na conta conectada (Supabase list_projects, 2026-09-23), embora supabase/migrations/0001_init.sql:2 diga que foi criado em São Paulo. A organização está no plano Pro, com um projeto ativo e cinco inativos (Supabase get_organization e list_projects, 2026-09-23); cada organização paga tem créditos para um projeto no tamanho padrão, e projetos adicionais começam em cerca de US$ 10 por mês, cobrados por hora (https://supabase.com/docs/guides/platform/billing-faq). A migração não habilita RLS (0001_init.sql:21). Tabelas criadas por SQL não recebem RLS automaticamente, e com RLS habilitada e sem políticas a chave publishable não lê nada (https://supabase.com/docs/guides/database/postgres/row-level-security). A chave publishable pode ficar no navegador com RLS; a secret ignora RLS e só pode ficar em componente de servidor; chave publishable ou secret enviada em 'Authorization: Bearer' é rejeitada por não ser JWT (https://supabase.com/docs/guides/getting-started/api-keys). A documentação anuncia a descontinuação das chaves legadas anon e service_role até o fim de 2026 (https://supabase.com/docs/guides/getting-started/migrating-to-new-api-keys). O Store lê SUPABASE_SERVICE_KEY e a envia nos cabeçalhos apikey e Authorization (reacao/store.py:11-12,24-25) e, sem URL ou chave, grava em arquivo local que se perde ao fim do job (reacao/store.py:19-23). O pipeline grava em seis tabelas (reacao/store.py:28-44); service e insight_feedback ficam vazias (0001_init.sql:3-4,17). A fixture sintética não é versionada no repositório (tests/fixtures/README.md:3-9); F1.1.T6 a publica no dataset ds-fabiopinheiro/reacao-poc-corpus com revisão e SHA-256, porque F1.1 recusa caminho local dentro de job do HF, inclusive arquivo gerado no contêiner (F1.1 RN08 e RN11), e o token dos jobs a lê. Pela P3 revisada, o painel web na Vercel usa a chave pública e a chave de serviço fica só nos jobs do HF. F1.5 cria a migração com a coluna insights_rejeitados_pelo_lint. Outras Features criam credenciais depois deste PBI: o token de uso único de F1.1.T6 para enviar a fixture, o token de escrita de uso único dos jobs de cópia de F5.1.T3 (revogado em F5.1.T5), repetido por F3.6.T3 e F3.6.T5, o token de leitura do Space de rotulagem de F3.3.T1, as variáveis do projeto do painel na Vercel de F5.6.T2, a credencial da equipe de mídia de F7.1.T2 e os segredos do Job agendado de F7.4.T4 e do Job de origem do webhook de F7.5.T4, que não têm quem lance e ficam guardados na especificação do Job no HF (Features F1, F3, F5 e F7 detalhadas). O Supabase CLI sobe o banco local e roda testes pgTAP no GitHub Actions com 'supabase db start' e 'supabase test db' (https://supabase.com/docs/guides/deployment/ci/testing; https://supabase.com/docs/guides/database/testing), e F1.5.T1 gera a configuração local do Supabase CLI (Feature F1 detalhada). As políticas de F5.6.T4 e F5.7.T1 são criadas na Fase 0, antes do gate.

**Regras de negócio:**
- RN01 – O token dos jobs lê o dataset do corpus e os repositórios de modelo e escreve só no repositório de resultados. O token do CI só lê os repositórios de modelo. O token de lançamento, com que a CLI de quem lança se autentica, tem permissão para lançar Jobs e não é enviado ao job.
- RN02 – Nenhum token de job ou do CI escreve no dataset do corpus. Exceção: tokens de uso único criados pela conta dona só para enviar ao dataset (fixture de F1.1.T6, cópias de F5.1.T3 e transferência de F3.6.T3), com escrita só nele, revogados depois do uso e registrados no inventário.
- RN03 – Os segredos seguem a forma de F2.1 (RN08). O HF_TOKEN do job entra por '--secrets-file -' com o valor do token dos jobs; '--secrets HF_TOKEN' não é usado, porque envia o token de lançamento.
- RN04 – A chave de serviço do Supabase, o token dos jobs e, se aceita a exceção da P26, a ANTHROPIC_API_KEY ficam guardados só no local de guarda de quem lança, escolhido em F2.6.T6 e registrado no inventário, e entram no job por '--secrets-file -'; nos Jobs sem quem lance, vale a RN13. A chave de serviço não vai para arquivo do repositório, secret do GitHub Actions, variável de ambiente de projeto na Vercel nem Space.
- RN05 – O painel web na Vercel recebe só a URL do projeto e a chave pública; o cadastro é feito em F5.6.
- RN06 – RLS habilitada nas 8 tabelas, sem política para o papel anon. Políticas para usuários autenticados ficam em F5.6, F5.7 e F7.2.
- RN07 – Uma execução configurada para gravar no Supabase falha no início se a URL ou a chave faltarem, em vez de gravar em arquivo local.
- RN08 – Se o CI passar a publicar no Hub, usa Trusted Publishers, sem token de escrita guardado.
- RN09 – O projeto Supabase de desenvolvimento só é criado com aprovação de Fabio e com o custo mensal previsto (RN02 da Feature).
- RN10 – Testes fora do HF usam o destino local ou uma chave falsa; a gravação com a chave real só acontece em job no HF.
- RN11 – A ANTHROPIC_API_KEY só entra no procedimento de lançamento se o ADR 0002 registrar a confirmação de Fabio sobre a exceção da P26; sem ela, o procedimento não a menciona e os jobs usam a heurística e o modelo de frase.
- RN12 – F2.6.T1 e F2.6.T2 terminam antes do primeiro job pago de F2 (F2.2.T4), que é lançado com o token de lançamento.
- RN13 – Jobs sem quem lance (Job agendado de F7.4.T4 e Job de origem do webhook de F7.5.T4) guardam os segredos na especificação do Job no HF, com o escopo mínimo das RN01 e RN02 e rotação por recriação do Job, definidos em F7.4.T4 e F7.5.T4. Cada segredo guardado entra no inventário com o id do Job.
- RN14 – O inventário de F2.6.T6 é o registro único das credenciais do épico, sem valores, com nome, local, escopo, dono, validade, rotação ou revogação e, para segredo guardado em Job, o id do Job. Cada PBI que cria credencial depois de F2.6 a acrescenta: F1.1.T6, F3.3.T1, F3.6.T3, F5.1.T3, F5.6.T2 (só a URL e a chave pública do Supabase), F7.1.T2, F7.4.T4 e F7.5.T4.
- RN15 – O CI sobe o Supabase local com a configuração de F1.5.T1, aplica as migrações em ordem e roda os testes de banco em push e pull request, só com as chaves que o Supabase local gera; F5.6.T4, F5.7.T1 e F7.2.T4 acrescentam os próprios testes e a seed a esse job.

**Fora de escopo:**
- Políticas de RLS e papéis do avaliador do gate (F5.6 e F5.7) e dos perfis do piloto (F7.2 e F7.8), cujos testes rodam no job de CI deste PBI
- Projeto na Vercel e suas variáveis de ambiente (F5.6)
- Credencial da equipe de mídia para o destino do piloto (F7.1)
- Projeto Supabase de produção
- Publicação da imagem pelo CI (F2.2)
- Decisão sobre a exceção da P26 (F2.4, D7)
- Forma geral de passar segredos nos comandos documentados (F2.1.T6)
- Criação das credenciais de outros PBIs (F1.1.T6, F3.3.T1, F3.6.T3, F5.1.T3, F5.6.T2 e F7.1.T2) e dos segredos guardados nos Jobs do piloto (F7.4.T4 e F7.5.T4); este PBI define o inventário onde eles são registrados

#### Critérios de aceite

- Um job de fumaça lançado com 'hf jobs run' pela imagem referenciada por digest, com o motor mock e a fixture sintética lida por URI hf://datasets/ na revisão de tests/fixtures/README.md (F1.1.T6), grava run_log e window_aggregate no projeto Supabase de desenvolvimento, com a chave de serviço entregue por '--secrets-file -'.
- 'hf jobs inspect' desse job mostra os nomes dos segredos e nenhum valor, e o comando de lançamento registrado não contém valor de segredo.
- Dentro de um job lançado pelo comando documentado, a identificação do token (whoami) mostra o nome do token dos jobs; o token de quem lança não aparece.
- Uma tentativa de enviar arquivo ao dataset do corpus com o token dos jobs recebe erro de permissão.
- Com o token do CI, a leitura de um repositório de modelo do projeto funciona.
- Com o token do CI, a escrita num repositório de modelo e a leitura do dataset do corpus recebem erro de permissão.
- Com linhas existentes em cada uma das 8 tabelas, uma leitura com a chave pública e sem sessão de usuário retorna zero linhas em todas.
- O Security Advisor do projeto Supabase de desenvolvimento não aponta tabela do schema public sem RLS.
- Nenhum arquivo do repositório, secret do GitHub Actions, variável de ambiente de projeto na Vercel ou Space contém a chave de serviço.
- Uma execução local com a fixture sintética e destino Supabase, sem a chave, termina com código diferente de zero antes de ler o vídeo, e o log não mostra valor de segredo.
- Uma execução local com a fixture sintética e uma chave falsa termina com código diferente de zero, e o log mostra o código HTTP sem o valor da chave.
- O procedimento de lançamento documentado entrega a ANTHROPIC_API_KEY por '--secrets-file -' quando o ADR 0002 registra a confirmação de Fabio sobre a exceção da P26, e não a menciona quando não registra; no --dry-run, a chave aparece só pelo nome.
- Existe um inventário versionado, sem valores, com cada credencial (inclusive a ANTHROPIC_API_KEY, se a exceção da P26 for aceita), onde fica guardada (inclusive o local de guarda de quem lança), seu escopo, seu responsável, sua validade e sua rotação ou revogação, com campo para o id do Job dos segredos guardados em Job.
- O inventário traz o token de uso único de F1.1.T6, com escopo e datas de criação e de revogação.
- Em cada push e pull request, o CI sobe o Supabase local, aplica as migrações em ordem e roda os testes de banco; um PR de teste com uma tabela nova sem RLS reprova nesse job.
- O job do Supabase local usa só as chaves que o Supabase local gera, e a lista de secrets do repositório no GitHub não tem chave do projeto Supabase de desenvolvimento.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F2.6.T1 | DevOps | Criar os repositórios privados vazios de modelo e de resultados e os tokens dos jobs, do CI e de lançamento | 3 | F2.4 |
| F2.6.T2 | DevOps | Cadastrar o token do CI no GitHub Actions e documentar a entrega do HF_TOKEN, da chave de serviço e, se aceita a exceção da P26, da ANTHROPIC_API_KEY por '--secrets-file -' | 3 | F2.6.T1, F2.1.T6, F2.4 (D7) |
| F2.6.T3 | DevOps | Identificar ou criar o projeto Supabase de desenvolvimento e aplicar as migrações | 3 | F1.5, Aprovação de Fabio, se o projeto for criado |
| F2.6.T4 | Backend | Habilitar RLS nas 8 tabelas por migração e subir no CI o Supabase local com as migrações e o teste de RLS | 6 | F2.6.T3, F1.5.T1 |
| F2.6.T5 | Backend | Ajustar o Store ao tipo de chave e fazê-lo falhar sem credencial | 5 | F2.6.T3 |
| F2.6.T6 | Governança e Privacidade | Escolher o local de guarda de quem lança e registrar o inventário único de credenciais | 3 | F2.6.T1, F2.6.T3, F2.4 (D7), F1.1.T6 |
| F2.6.T7 | QA | Verificar os critérios de aceite de F2.6 | 6 | F2.6.T2, F2.6.T4, F2.6.T5, F2.6.T6, F2.2.T2, F1.1, Aprovação de Fabio |

<details><summary>F2.6.T1 · [DevOps] Criar os repositórios privados vazios de modelo e de resultados e os tokens dos jobs, do CI e de lançamento</summary>

**Objetivo:** Repositórios no namespace do ADR 0002 e três tokens fine-grained com escopo mínimo, prontos antes do primeiro job pago.

**Passos previstos:**
1. Criar vazios e privados os repositórios de modelo e de resultados com os nomes do ADR 0002.
2. Criar o token dos jobs: leitura do dataset do corpus e dos repositórios de modelo e escrita só no repositório de resultados.
3. Criar o token do CI: leitura só dos repositórios de modelo.
4. Criar o token de lançamento: permissão para lançar Jobs no namespace do ADR, usado só pela CLI de quem lança.
5. Registrar nomes e escopos no inventário de F2.6.T6.

**Definição de pronto:** Repositórios criados e privados; três tokens criados com os escopos registrados.

**Dependências:** F2.4

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F2.6.T2 · [DevOps] Cadastrar o token do CI no GitHub Actions e documentar a entrega do HF_TOKEN, da chave de serviço e, se aceita a exceção da P26, da ANTHROPIC_API_KEY por &#x27;--secrets-file -&#x27;</summary>

**Objetivo:** Secret do CI cadastrado e procedimento de lançamento, usado desde o primeiro job pago, que autentica a CLI com o token de lançamento e envia ao job os segredos sem valor em comando.

**Passos previstos:**
1. Cadastrar o token do CI como secret do GitHub Actions.
2. Documentar em docs/hf-jobs.md que a CLI de quem lança se autentica com o token de lançamento e que o HF_TOKEN do job e a chave de serviço entram por '--secrets-file -', com os valores lidos do local de guarda de quem lança.
3. Ler a decisão D7 do ADR 0002 sobre a exceção da P26: se aceita, incluir a ANTHROPIC_API_KEY no mesmo '--secrets-file -'; se não aceita, registrar que os comandos não passam a chave.
4. Rodar o --dry-run do comando documentado e conferir que os segredos aparecem mascarados.

**Definição de pronto:** Secret do CI cadastrado e procedimento em docs/hf-jobs.md conforme D7, com --dry-run que mostra os segredos só pelo nome.

**Dependências:** F2.6.T1, F2.1.T6, F2.4 (D7)

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F2.6.T3 · [DevOps] Identificar ou criar o projeto Supabase de desenvolvimento e aplicar as migrações</summary>

**Objetivo:** Projeto de desenvolvimento com as 8 tabelas e as migrações corrigidas.

**Passos previstos:**
1. Procurar o projeto citado em supabase/migrations/0001_init.sql:2; se não existir, pedir a Fabio aprovação com o custo mensal previsto (https://supabase.com/docs/guides/platform/billing-faq) e criar na região São Paulo.
2. Aplicar 0001_init.sql e a migração de F1.5 pela conta de Fabio.
3. Obter a URL, a chave publishable e a chave secret, guardando a secret só no local de guarda de quem lança.
4. Registrar a URL no PBI.

**Definição de pronto:** A listagem de tabelas do projeto mostra as 8 tabelas com a coluna de F1.5 em run_log.

**Dependências:** F1.5, Aprovação de Fabio, se o projeto for criado

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F2.6.T4 · [Backend] Habilitar RLS nas 8 tabelas por migração e subir no CI o Supabase local com as migrações e o teste de RLS</summary>

**Objetivo:** RLS habilitada em todas as tabelas, teste que cobre tabelas novas e job de CI com o Supabase local, onde os testes de banco de F5.6, F5.7 e F7.2 passam a rodar.

**Passos previstos:**
1. Criar migração que habilita RLS nas 8 tabelas, sem política para anon.
2. Escrever teste estático que exige RLS habilitada para cada tabela criada nas migrações, no estilo de tests/test_schema.py.
3. Criar o job de CI que instala o Supabase CLI em versão fixa, sobe o banco local com a configuração de F1.5.T1, aplica as migrações em ordem e roda 'supabase test db' (https://supabase.com/docs/guides/deployment/ci/testing), em push e pull request.
4. Escrever um teste pgTAP que confere RLS habilitada e nenhuma política para anon nas 8 tabelas (https://supabase.com/docs/guides/database/testing).
5. Usar no job só as chaves que o Supabase local gera, sem secret do projeto de desenvolvimento.
6. Abrir um PR de teste com uma tabela nova sem RLS e conferir que o job reprova.
7. Aplicar a migração no projeto de desenvolvimento.

**Definição de pronto:** Migração aplicada; teste estático e teste pgTAP aprovados no job do Supabase local; PR de teste com tabela sem RLS reprovado no job; nenhuma secret do projeto de desenvolvimento no GitHub.

**Dependências:** F2.6.T3, F1.5.T1

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F2.6.T5 · [Backend] Ajustar o Store ao tipo de chave e fazê-lo falhar sem credencial</summary>

**Objetivo:** Cabeçalho aceito pela chave secret e falha explícita sem credencial.

**Passos previstos:**
1. Enviar a chave secret só no cabeçalho apikey, conforme a documentação de API keys do Supabase, ajustando reacao/store.py:24-25.
2. Tornar explícito o destino dos resultados (Supabase ou local).
3. Com destino Supabase, falhar antes de ler o vídeo se a URL ou a chave faltarem.
4. Garantir que mensagens de erro mostrem o código HTTP sem o valor da chave.
5. Escrever testes locais de chave ausente e de chave falsa, sem a chave real.

**Definição de pronto:** Testes locais aprovados; a gravação com a chave real é verificada no job de F2.6.T7.

**Dependências:** F2.6.T3

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F2.6.T6 · [Governança e Privacidade] Escolher o local de guarda de quem lança e registrar o inventário único de credenciais</summary>

**Objetivo:** Inventário sem valores, conferido com a decisão D7 do ADR 0002, com os campos que as credenciais criadas por outros PBIs usam.

**Passos previstos:**
1. Escolher com Fabio o local de guarda da chave de serviço, do token dos jobs e, se aceita a exceção da P26, da ANTHROPIC_API_KEY do lado de quem lança.
2. Definir os campos do inventário: nome, onde fica (local de guarda de quem lança, segredos do job no HF, especificação de Job agendado ou de Job de origem de webhook, GitHub Actions, Vercel, Space), escopo, dono, validade, rotação ou revogação e id do Job, quando o segredo fica guardado num Job.
3. Listar cada credencial deste PBI (token de lançamento e seu escopo de Jobs, token dos jobs, token do CI, chave secret, chave publishable, ANTHROPIC_API_KEY se a exceção da P26 for aceita, credencial da conta Supabase usada nas migrações).
4. Transcrever o token de uso único de F1.1.T6 a partir do registro no PR de F1.1, com escopo e datas de criação e de revogação.
5. Registrar no inventário que cada PBI que cria credencial a acrescenta (F3.3.T1, F3.6.T3, F5.1.T3, F5.6.T2, F7.1.T2, F7.4.T4 e F7.5.T4) e que as variáveis do projeto do painel na Vercel são só a URL e a chave pública do Supabase.
6. Conferir que a chave de serviço aparece só no local de guarda e nos segredos dos jobs.
7. Revisar com Fabio.

**Definição de pronto:** Inventário versionado, sem valores, com os campos definidos e o token de F1.1.T6, conferido com D7 e revisado por Fabio.

**Dependências:** F2.6.T1, F2.6.T3, F2.4 (D7), F1.1.T6

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F2.6.T7 · [QA] Verificar os critérios de aceite de F2.6</summary>

**Objetivo:** Evidência de cada critério de aceite anexada ao PBI.

**Passos previstos:**
1. Pedir aprovação a Fabio e lançar o job de fumaça com 'hf jobs run' pela imagem da tag que contém F2.6.T5, referenciada por digest, com --video na URI hf://datasets/ da fixture na revisão de tests/fixtures/README.md (F1.1.T6), comando que imprime o nome do token pelo whoami e roda processar_culto.py com --provider mock e --no-transcribe, entregando o HF_TOKEN e a chave de serviço por '--secrets-file -'.
2. Conferir 'hf jobs inspect', o comando de lançamento e o nome do token impresso no log.
3. Testar as permissões dos tokens dos jobs e do CI, inclusive os casos negados.
4. Inserir pelo editor SQL do projeto, na sessão de Fabio, uma linha de teste em service e em insight_feedback; ler as 8 tabelas com a chave publishable sem sessão; apagar as linhas de teste; consultar o Security Advisor.
5. Buscar a chave de serviço no repositório e listar os secrets do GitHub Actions e os projetos do time na Vercel.
6. Rodar localmente, com a fixture, os casos sem chave e com chave falsa.
7. Conferir no procedimento documentado e no --dry-run a presença ou a ausência da ANTHROPIC_API_KEY conforme D7.
8. Conferir no CI o job do Supabase local, o PR de teste com tabela sem RLS reprovado e a lista de secrets do repositório no GitHub.
9. Conferir o inventário, inclusive os campos de validade, rotação ou revogação e id do Job e o token de F1.1.T6.

**Definição de pronto:** Checklist dos 16 critérios com JOB_ID, respostas das leituras, links do CI e mensagens de erro anexada ao PBI, sem valor de segredo.

**Dependências:** F2.6.T2, F2.6.T4, F2.6.T5, F2.6.T6, F2.2.T2, F1.1, Aprovação de Fabio

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- docs/hf-jobs.md:14-17
- reacao/moments.py:48-50
- reacao/insights.py:32-36
- huggingface_hub/cli/_cli_utils.py:831-838,926-969 e cli/jobs.py:286,392-402 (instalados)
- whoami do HF, 2026-09-23 (token clássico write)
- Feature F3 detalhada, F3.1.T3 (revogação do token clássico)
- https://huggingface.co/docs/hub/security-tokens#best-practices
- https://huggingface.co/docs/hub/trusted-publishers
- https://huggingface.co/docs/hub/jobs-manage#inspect-a-job
- https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets
- https://supabase.com/docs/guides/database/postgres/row-level-security
- https://supabase.com/docs/guides/getting-started/api-keys
- https://supabase.com/docs/guides/getting-started/migrating-to-new-api-keys
- https://supabase.com/docs/guides/platform/billing-faq
- Supabase get_organization (plano pro) e list_projects (sem projeto deste sistema; um ativo, cinco inativos), 2026-09-23
- supabase/migrations/0001_init.sql:2-21
- reacao/store.py:11-44
- tests/fixtures/README.md:3-9
- P3 revisada pelo usuário
- premissas P17 e P26
- https://supabase.com/docs/guides/deployment/ci/testing
- https://supabase.com/docs/guides/database/testing
- Feature F1 detalhada: F1.1 RN08, RN11, RN14, F1.1.T6 e F1.5.T1
- Feature F3 detalhada: F3.3.T1, F3.6.T3 e F3.6.T5
- Feature F5 detalhada: F5.1.T3, F5.1.T5, F5.6.T2, F5.6.T4 e F5.7.T1
- Feature F7 detalhada: F7.1.T2, F7.2.T4, F7.4.T4 e F7.5.T4

#### Verificação INVEST: pontos que falharam
- Independent: F2.6.T7 espera a publicação de imagem de F2.2.T2, e F2.2.T4 espera F2.6.T1 e F2.6.T2; a dependência entre os dois PBIs é só entre essas tasks.

#### Premissas
- A permissão por repositório de um token fine-grained é escolhida entre repositórios existentes, por isso este PBI cria vazios os repositórios privados de modelo e de resultados (dedução, a confirmar na criação).
- A região do projeto Supabase de desenvolvimento é São Paulo, como registra supabase/migrations/0001_init.sql:2.
- A chave de serviço usada é a secret (sb_secret_); a service_role legada só é usada se o teste de cabeçalho mostrar impedimento, com o prazo de descontinuação registrado nos riscos da Feature.
- O local de guarda de quem lança é escolhido em F2.6.T6 (por exemplo, o gerenciador de senhas de Fabio). Dedução pela documentação de segredos: o HF Jobs não guarda o valor para o lançamento seguinte de um job não agendado.
- Com a P3 revisada, a chave de serviço deixa de ir para o Space de F5.6. O painel web lê com a chave pública e depende de políticas para usuários autenticados, criadas em F5.6 ou F7.2.
- F2.4 entra como dependência porque o escopo dos tokens depende do namespace e a entrega da ANTHROPIC_API_KEY depende de D7. F2.1.T6, F2.2.T2, F1.1 e F1.5.T1 entram só nas tasks que os usam: F2.6.T2 segue a forma dos segredos de F2.1.T6, F2.6.T4 usa a configuração local do Supabase CLI de F1.5.T1, F2.6.T6 transcreve o token de F1.1.T6, e F2.6.T7 usa a imagem publicada por F2.2.T2, a guarda corrigida e a fixture no dataset. F2.2.T4 depende de F2.6.T1 e F2.6.T2; entre tasks não há ciclo.
- As linhas de teste em service e insight_feedback são inseridas pelo editor SQL do projeto, na sessão de Fabio, sem a chave de serviço.
- Disciplinas: DevOps, Backend, Governança e Privacidade e QA, como na árvore.
- Story points e horas são sugestão.
- A versão do Supabase CLI no job de CI é fixada, porque o exemplo da documentação usa 'version: latest' (https://supabase.com/docs/guides/deployment/ci/testing) e uma versão nova poderia mudar o job sem PR (dedução).
- F2.6.T4 entrega o job com o teste de RLS habilitada; os testes de política de F5.6.T4, F5.7.T1 e F7.2.T4 entram nesse job quando esses PBIs rodarem.
- O inventário é criado antes de parte das credenciais que registra. F1.1.T6 pode acontecer antes e deixa o registro no PR, que F2.6.T6 transcreve; as demais Features acrescentam os seus registros.
- Com o job de CI do Supabase local e o inventário único, a sugestão passou de 5 para 8 pontos.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável.
- Item pai: Feature F2.
- Registrar no PBI a URL do projeto Supabase de desenvolvimento (sem chaves).
- Informar F5.4 (F5.4.T4), F5.5 (F5.5.T3) e F5.6 (F5.6.T7) de que a ANTHROPIC_API_KEY é entregue pelo procedimento de F2.6.T2 só se D7 aceitar a exceção da P26.
- Decidir o destino do token clássico write usado no levantamento (revogar ou restringir), em F3.1.T3.
- Informar F3.3 (F3.3.T1) e F3.6 (F3.6.T3 e F3.6.T5) de que o token entra no inventário de F2.6.T6, além do dataset card.
- Informar F5.6.T4, F5.7.T1 e F7.2.T4 de que os testes de banco rodam no job de CI de F2.6.T4.

## Preview — PBI F2.7 (novo) · Comparar window_aggregate de duas execuções janela a janela com um script de paridade

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Comparar window_aggregate de duas execuções janela a janela com um script de paridade |
| Tipo | Product Backlog Item |
| Pai | F2 |
| Tags | F2; paridade; MLOps; QA; Data Science; PBI-106; PBI-103 |
| Estimativa | 5 pts (sugestão); tasks: 19 h |
| Dependências | F2.2 (imagem com digest), F2.3 (pesos por revisão fixa, porque a comparação usa os motores reais), F2.5 (run_id), F2.8 (conjunto de resultados e linhagem com o vídeo), F1.3 (vídeos permitidos por tipo de job), F3.1 (clipes 07 a 10) ou F5.1 (vídeo público no dataset), Aprovação de Fabio para os três jobs, com duração e custo previstos |
| Substitui | PBI-106 (parte: script de paridade e execução do lado HF), PBI-103 (critério de aceite de paridade, docs/onprem.md:55) |

#### Descrição

Como integrante do time de MLOps que precisa mostrar que trocar flavor ou ambiente não altera os agregados  
Quero um script que compare window_aggregate de dois run_id janela a janela e diga se a diferença fica em até 1 p.p. com o mesmo n  
Para que F5.3 e, depois do épico, o servidor local mostrem com um relatório que a troca de dispositivo ou de ambiente não muda os agregados

**Contexto:** O teste de paridade existe só em texto: processar o mesmo vídeo nos dois ambientes, comparar window_aggregate janela a janela com diferença de no máximo 1 p.p. em todos os percentuais e mesmo n e registrar o tempo de GPU nos dois (docs/onprem.md:55-58; docs/hf-jobs.md:38). Não existe script, teste nem job que faça a comparação (levantamento de infraestrutura). Os percentuais da janela são pct_voltados, pct_sorrindo, expressividade e pct_olhos_fechados, de 0 a 100 com uma casa decimal (reacao/aggregate.py:39-42), e a janela tem n_total e n_mensuravel (reacao/types.py:46-47). Janelas com menos de 10 rostos mensuráveis saem com insuficiente verdadeiro e sem percentuais (regra 3 do CLAUDE.md; reacao/types.py:7). A fixture sintética não tem rosto (tests/fixtures/README.md:11-13), então compará-la daria só janelas sem percentual; a paridade usa um vídeo com rostos que F1.3 permite para jobs de paridade: vídeo público (F5.1) ou, depois de F3.1, os clipes 07 a 10 (árvore, F1.3). processar_culto.py não tem opção para limitar o trecho processado (processar_culto.py:35-46), então um culto público inteiro é processado inteiro em cada job. O caminho e o SHA-256 do vídeo, o digest e o flavor ficam no arquivo de linhagem de F2.8, e o tempo total no run_log (segundos_total, supabase/migrations/0001_init.sql:18). F5.3 usa este script para mostrar que a expressão e a pose na GPU não alteram os agregados.

**Regras de negócio:**
- RN01 – A comparação é por janela, pareada por culto, fonte e t_ini.
- RN02 – A paridade passa quando, em toda janela, cada percentual difere no máximo 1,0 p.p. e n_total e n_mensuravel são iguais (docs/onprem.md:57).
- RN03 – Uma janela com insuficiente diferente entre as execuções, ou com percentual presente numa e ausente na outra, reprova.
- RN04 – Execuções com número de janelas diferente, ou com caminho ou SHA-256 do vídeo diferentes na linhagem de F2.8, reprovam antes da comparação por janela.
- RN05 – Os vídeos das execuções de paridade seguem F1.3: vídeo público (F5.1) ou, depois de F3.1, os clipes 07 a 10.
- RN06 – O relatório de paridade mostra os dois run_id, o digest, o flavor, a maior diferença por percentual, as janelas divergentes, a diferença de n e o tempo total de cada execução.
- RN07 – O PBI entrega a medição; um resultado reprovado fica registrado com as janelas divergentes e não é ajustado para passar.
- RN08 – O script lê arquivos de agregados e de linhagem e não usa a chave de serviço do Supabase fora dos jobs do HF.
- RN09 – O pedido de aprovação dos jobs traz a duração do vídeo e o custo previsto de cada job; um culto inteiro não é tratado como job curto.

**Fora de escopo:**
- Execução no servidor local (P3; lado local do PBI-106)
- Paridade de eventos, momentos e insights
- Correção de divergências encontradas (F5.3 ou item novo)
- Medida de tempo de GPU separada da etapa de vídeo (F5.4)

#### Critérios de aceite

- Com dois run_id do mesmo vídeo, o script lista por janela a diferença de cada percentual, de n_total e de n_mensuravel e informa 'passou' ou 'não passou' pela regra de 1 p.p. e mesmo n.
- Nos testes com dados sintéticos, uma diferença de 1,0 p.p. passa e uma de 1,1 p.p. reprova.
- Uma janela marcada como insuficiente numa execução e não na outra reprova, e o relatório a lista.
- Execuções com número de janelas diferente, ou com caminho ou SHA-256 do vídeo diferentes, reprovam, com mensagem que diz o motivo.
- Um run_id inexistente faz o script terminar com código diferente de zero e mensagem que nomeia o run_id.
- O script aceita os arquivos do repositório de resultados de F2.8 e arquivos locais no mesmo formato, com o mesmo resultado para a mesma execução.
- O repositório de resultados tem um relatório de paridade entre duas execuções do mesmo digest na t4-small e outro entre t4-small e cpu-basic, sobre um vídeo com rostos que F1.3 permite para paridade.
- Cada relatório traz os dois run_id, o digest, o flavor, a maior diferença por percentual, a diferença de n e o tempo total de cada execução.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F2.7.T1 | Data Science | Definir a regra de comparação e registrá-la em docs/onprem.md seção 4 | 3 | — |
| F2.7.T2 | MLOps | Implementar o script de paridade | 6 | F2.7.T1, F2.8 |
| F2.7.T3 | QA | Escrever os testes do script com dados sintéticos | 4 | F2.7.T2 |
| F2.7.T4 | MLOps | Rodar as execuções de paridade no HF e publicar os relatórios | 4 | F2.7.T2, F2.2, F2.3, F1.3, F3.1 ou F5.1, Aprovação de Fabio |
| F2.7.T5 | QA | Verificar os critérios de aceite de F2.7 | 2 | F2.7.T3, F2.7.T4 |

<details><summary>F2.7.T1 · [Data Science] Definir a regra de comparação e registrá-la em docs/onprem.md seção 4</summary>

**Objetivo:** Regra de paridade sem ambiguidade, escrita antes do script.

**Passos previstos:**
1. Listar as colunas comparadas: os quatro percentuais, n_total, n_mensuravel e insuficiente.
2. Definir o pareamento por culto, fonte e t_ini e a verificação de mesmo vídeo pelo caminho e SHA-256 da linhagem.
3. Definir o tratamento de percentual ausente e de janela insuficiente.
4. Fixar o limite de 1,0 p.p. sobre os valores arredondados a uma casa.
5. Atualizar docs/onprem.md seção 4.

**Definição de pronto:** Seção 4 de docs/onprem.md atualizada e revisada pelo time de MLOps.

**Dependências:** nenhuma

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F2.7.T2 · [MLOps] Implementar o script de paridade</summary>

**Objetivo:** Script que compara dois run_id e produz o relatório da RN06.

**Passos previstos:**
1. Ler os agregados de dois run_id a partir do repositório de resultados de F2.8 ou de arquivos locais no mesmo formato.
2. Ler da linhagem de F2.8 o caminho e o SHA-256 do vídeo, o digest e o flavor, e do run_log o tempo total.
3. Aplicar a regra de F2.7.T1 e gerar relatório em JSON e em texto.
4. Usar código de saída 0 para passou, 1 para não passou e 2 para erro de entrada.

**Definição de pronto:** Script em main com os três códigos de saída exercitados pelos testes de F2.7.T3.

**Dependências:** F2.7.T1, F2.8

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F2.7.T3 · [QA] Escrever os testes do script com dados sintéticos</summary>

**Objetivo:** Testes que cobrem limites e caminhos de erro.

**Passos previstos:**
1. Caso de 1,0 p.p. que passa e de 1,1 p.p. que reprova.
2. Caso de n_total ou n_mensuravel diferente.
3. Caso de insuficiente divergente e de percentual ausente numa execução.
4. Caso de número de janelas diferente, SHA-256 do vídeo diferente e run_id inexistente.

**Definição de pronto:** Testes em tests/ aprovados no CI.

**Dependências:** F2.7.T2

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F2.7.T4 · [MLOps] Rodar as execuções de paridade no HF e publicar os relatórios</summary>

**Objetivo:** Dois relatórios de paridade no repositório de resultados.

**Passos previstos:**
1. Escolher o vídeo com rostos que F1.3 permite para paridade: um dos clipes 07 a 10 depois de F3.1, ou um vídeo público de F5.1.
2. Pedir aprovação a Fabio para dois jobs t4-small e um cpu-basic, com timeout explícito, duração do vídeo e custo previsto de cada job.
3. Rodar os três jobs pela imagem com digest e o mesmo motor.
4. Rodar o script para t4-small contra t4-small e para t4-small contra cpu-basic.
5. Enviar os relatórios ao repositório de resultados.

**Definição de pronto:** Dois relatórios no repositório de resultados, com os run_id e JOB_IDs registrados no PBI.

**Dependências:** F2.7.T2, F2.2, F2.3, F1.3, F3.1 ou F5.1, Aprovação de Fabio

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F2.7.T5 · [QA] Verificar os critérios de aceite de F2.7</summary>

**Objetivo:** Evidência de cada critério de aceite anexada ao PBI.

**Passos previstos:**
1. Conferir a saída do script nos casos dos testes.
2. Conferir que a mesma execução dá o mesmo resultado lida do repositório e de arquivo local.
3. Conferir o vídeo usado contra a lista de F1.3 e o conteúdo dos dois relatórios publicados.

**Definição de pronto:** Checklist dos 8 critérios com os caminhos dos relatórios anexada ao PBI.

**Dependências:** F2.7.T3, F2.7.T4

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- docs/onprem.md:55-58
- docs/hf-jobs.md:38
- reacao/aggregate.py:30,39-42
- reacao/types.py:7,38-53
- tests/fixtures/README.md:11-13
- processar_culto.py:35-46
- supabase/migrations/0001_init.sql:18
- CLAUDE.md (regra 3)
- mapa_infra.jsonl (paridade só em texto)
- Árvore: F1.3, F3.1, F5.1, F5.3

#### Premissas
- 'mesmo n' em docs/onprem.md:57 é lido como n_total e n_mensuravel iguais.
- A paridade usa um vídeo com rostos que F1.3 permite, porque a fixture sintética não tem rosto. O vídeo licenciado de F1.6 não entra, porque é exceção da P26 para o CI e não está na lista de F1.3.
- Com um culto público inteiro de F5.1, cada job processa o culto inteiro, porque o script não limita o trecho; o pedido de aprovação traz a duração e o custo previstos.
- F2.8, F1.3, F2.3 e 'F3.1 ou F5.1' entram como dependências pelos motivos acima e porque a comparação carrega os pesos reais e lê a linhagem.
- Disciplinas: QA, MLOps e Data Science, como na árvore.
- Story points e horas são sugestão.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável.
- Item pai: Feature F2.
- Registrar no PBI a aprovação de custo e os JOB_IDs das execuções de paridade.
- Informar F5.3 do formato do relatório de paridade.

## Preview — PBI F2.8 (novo) · Enviar ao repositório privado de resultados o conjunto de cada execução com linhagem, inclusive o registro das falhas do pipeline e do bench

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Enviar ao repositório privado de resultados o conjunto de cada execução com linhagem, inclusive o registro das falhas do pipeline e do bench |
| Tipo | Product Backlog Item |
| Pai | F2 |
| Tags | F2; linhagem; run_id; MLOps; Backend; DevOps; Data Science |
| Estimativa | 8 pts (sugestão); tasks: 29 h |
| Dependências | F2.5 (run_id e registro de falha no processar_culto.py), F2.2 (digest da imagem e commit gravado no build), F2.3 (manifesto e carga de pesos com hash), F2.4 (namespace e tipo do repositório de resultados), F2.6 (repositório de resultados e token de escrita só nele), F3.5 (revisão do dataset), F1.5 (flavor real), F3.1 (clipes 07 a 10) ou F5.1 (vídeo público no dataset), para o vídeo do job de validação, Aprovação de Fabio para os jobs de verificação |
| Substitui | nenhum |

#### Descrição

Como integrante do time de ML e visão computacional que lê os números do gate e do ADR 0001  
Quero que cada execução de processar_culto.py e de bench.py envie a um repositório privado um conjunto do run_id com linhagem, resultados agregados e, quando falhar, o registro da falha  
Para que qualquer número do gate ou do ADR 0001 aponte para o script, o código, a imagem, o vídeo, os pesos e os dados de onde veio, e que os resultados do bench não se percam com o contêiner

**Contexto:** O run_log não tem commit, revisão do dataset, versão de modelo, JOB_ID nem parâmetros (processar_culto.py:104-106; supabase/migrations/0001_init.sql:18), e o culto é argumento livre (processar_culto.py:37). O bench grava o CSV em out/bench dentro do contêiner, só no caminho de sucesso, e imprime no log uma tabela sem flavor, inferencia_s e pares_ge64 (bench.py:254-256). O bench termina com código 1 sem exceção quando não encontra .mp4 ou vídeo rotulado (bench.py:207-209,237-239) e não grava no Supabase. O sistema de arquivos do job é apagado ao fim, e a documentação recomenda gravar resultados num Storage Bucket ou num repositório do Hub (https://huggingface.co/docs/hub/jobs-manage#persist-your-results). O HF injeta JOB_ID e ACCELERATOR no job (https://huggingface.co/docs/hub/jobs-configuration#built-in-environment-variables), e F1.5 grava o flavor a partir de ACCELERATOR. A transcrição troca em silêncio de 'medium' para 'small' (reacao/transcribe.py:9-12); F2.3 expõe qual modelo carregou. A guarda lista as extensões de imagem e vídeo (reacao/guard.py:8). A especificação do job guarda a imagem usada (huggingface_hub/_jobs_api.py:324-346), e o token dos jobs de F2.6 não tem permissão de Jobs (F2.6 RN01), então a conferência do digest com 'hf jobs inspect' é feita por quem lança. 'hf jobs run' também aceita --dry-run (huggingface_hub/cli/jobs.py:660,712). A flag --stdout (commit b834dd0) imprime janelas, eventos e insights no log. F2.7 compara execuções pelo vídeo e lê digest e flavor da linhagem.

**Regras de negócio:**
- RN01 – O conjunto enviado ao repositório privado de resultados tem só dados agregados: linhagem, run_log, agregados por janela, eventos, insights, CSV completo do bench e registro de falha. Nenhum quadro, recorte, vídeo ou observação por rosto.
- RN02 – Campos de linhagem: tag e SHA do script, commit do pacote, digest da imagem recebido no lançamento, caminho do vídeo no repositório de origem (nos jobs, inclusive a fixture sintética, lida do dataset por revisão em F1.1.T6; fora do HF, o caminho local) e SHA-256 do arquivo, revisão do dataset, SHA-256 de cada peso carregado (manifesto de F2.3), JOB_ID, flavor (F1.5), fps, min-faces-plateia, det_size, det_thresh, K_MIN, WINDOW_S, modelo Whisper efetivo e, a partir de F5.2, o caminho de LLM. Fora do HF, JOB_ID fica nulo e o ambiente é 'local'.
- RN03 – bench.py gera run_id no início e registra falha com etapa e mensagem tanto em exceção quanto nos retornos com código diferente de zero sem exceção.
- RN04 – processar_culto.py envia ao conjunto do run_id o registro de falha de F2.5.
- RN05 – Uma falha no envio ao repositório de resultados faz o processo terminar com código diferente de zero.
- RN06 – O digest é passado ao job no lançamento (-e) e conferido fora do job com 'hf jobs inspect' por quem lança.
- RN07 – O número que vai ao gate ou ao ADR 0001 cita o run_id.
- RN08 – Testes fora do HF usam a fixture sintética e montam o conjunto num diretório local, sem token do HF (RN10 da Feature).

**Fora de escopo:**
- Disparo e consulta automática dos jobs do piloto (F7.5)
- Versionamento do corpus e dos rótulos (F3.5)
- Escolha do run_id exibido no painel web (F5.6)
- Retenção dos resultados (F7.4)
- Registro do caminho de LLM (F5.2)
- Criação do repositório de resultados e do token de escrita (F2.6)
- Gravação dos resultados do bench no Supabase

#### Critérios de aceite

- Ao fim de um job concluído de processar_culto.py, o repositório de resultados tem um conjunto do run_id com linhagem, run_log e agregados.
- Um job de validação lançado com 'hf jobs run' pela imagem referenciada por digest, com o motor hsemotion sobre um vídeo do dataset permitido por F1.3, gera um conjunto cuja linhagem traz revisão do dataset, caminho e SHA-256 do vídeo e SHA-256 de cada peso carregado.
- Numa execução do bench com a fixture sintética e rótulos sintéticos, o conjunto do run_id contém o CSV com as colunas flavor, inferencia_s e pares_ge64.
- O arquivo de linhagem traz todos os campos da RN02, e o teste de contrato falha se um deles faltar.
- Numa execução fora do HF, JOB_ID fica nulo e o campo de ambiente diz 'local'.
- Quando um job falha com exceção numa etapa, o repositório de resultados recebe o registro de falha com run_id, etapa, tipo e mensagem, e o job termina com código diferente de zero.
- Quando o bench não encontra vídeo rotulado, o conjunto do run_id recebe registro de falha com a etapa e a mensagem, e o código de saída é diferente de zero.
- Uma falha no envio ao repositório de resultados faz o job terminar com código diferente de zero, com a mensagem no log.
- Nenhum arquivo enviado ao repositório de resultados é imagem, vídeo ou observação por rosto.
- Para um job lançado pelo comando documentado, o digest registrado na linhagem é igual ao da imagem mostrada por 'hf jobs inspect'.
- docs/poc-gate.md indica, para cada critério do gate lido do bench (1, 2a, 2b e 5), o arquivo e a coluna do conjunto do run_id e como citar o run_id.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F2.8.T1 | MLOps | Coletar a linhagem de cada execução | 8 | F2.5, F2.2, F2.3, F3.5 |
| F2.8.T2 | Backend | Gerar run_id no bench e registrar como falha os retornos com código diferente de zero | 4 | F2.5 |
| F2.8.T3 | MLOps | Enviar o conjunto do run_id ao repositório privado de resultados | 6 | F2.8.T1, F2.8.T2, F2.6 |
| F2.8.T4 | DevOps | Documentar o lançamento que passa o digest ao job e o confere com 'hf jobs inspect' | 3 | F2.2, F2.6 |
| F2.8.T5 | Data Science | Indicar em docs/poc-gate.md o arquivo e a coluna do conjunto do run_id para cada critério do gate | 3 | F1.3 e F1.4 (regras de leitura e veredito da linha TOTAL) |
| F2.8.T6 | QA | Verificar os critérios de aceite de F2.8 | 5 | F2.8.T3, F2.8.T4, F2.8.T5, Aprovação de Fabio |

<details><summary>F2.8.T1 · [MLOps] Coletar a linhagem de cada execução</summary>

**Objetivo:** Arquivo de linhagem com os campos da RN02 e teste de contrato.

**Passos previstos:**
1. Ler o commit gravado na imagem no build (F2.2) e a tag e o SHA do script.
2. Ler o digest da variável de ambiente definida no lançamento.
3. Registrar o caminho do vídeo no repositório de origem, o SHA-256 do arquivo calculado em /dev/shm e a revisão do dataset lida por F3.5.
4. Registrar o SHA-256 de cada peso carregado, obtido da função de carga de F2.3, e o modelo Whisper efetivo exposto por F2.3.
5. Registrar JOB_ID, flavor de F1.5 e parâmetros.
6. Escrever o teste de contrato que falha se um campo faltar.

**Definição de pronto:** Execução local com a fixture gera a linhagem completa com JOB_ID nulo e ambiente 'local', e o teste de contrato é aprovado.

**Dependências:** F2.5, F2.2, F2.3, F3.5

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F2.8.T2 · [Backend] Gerar run_id no bench e registrar como falha os retornos com código diferente de zero</summary>

**Objetivo:** Bench com run_id e registro de falha em exceção e nos retornos sem exceção.

**Passos previstos:**
1. Gerar o run_id no início de bench.py.
2. Capturar exceções com etapa e mensagem e transformar os retornos com código 1 (bench.py:209,239) em registro de falha.
3. Remover da mensagem qualquer valor de variável de segredo.
4. Escrever testes locais para corpus sem .mp4, corpus sem vídeo rotulado e exceção.

**Definição de pronto:** Testes locais aprovados nos três casos, com registro de falha e código de saída diferente de zero.

**Dependências:** F2.5

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F2.8.T3 · [MLOps] Enviar o conjunto do run_id ao repositório privado de resultados</summary>

**Objetivo:** Conjunto por run_id no repositório de resultados, inclusive em falha.

**Passos previstos:**
1. Montar a pasta do run_id com linhagem, run_log, agregados, eventos, insights, CSV completo do bench e registro de falha, quando houver.
2. Recusar no envio qualquer arquivo com extensão de imagem ou vídeo da lista da guarda (reacao/guard.py:8).
3. Enviar com o token de escrita de F2.6; nos testes fora do HF, gravar num diretório local.
4. Terminar com código diferente de zero se o envio falhar.

**Definição de pronto:** Teste local com a fixture e rótulos sintéticos monta o conjunto com o CSV do bench, e o teste de falha de envio termina com código diferente de zero.

**Dependências:** F2.8.T1, F2.8.T2, F2.6

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F2.8.T4 · [DevOps] Documentar o lançamento que passa o digest ao job e o confere com &#x27;hf jobs inspect&#x27;</summary>

**Objetivo:** Comando de lançamento dos jobs de gate e piloto que registra o digest na linhagem e a conferência feita por quem lança.

**Passos previstos:**
1. Documentar em docs/hf-jobs.md o lançamento com 'hf jobs run' pela imagem com digest, -e com o digest e segredos entregues por '--secrets-file -' (F2.6).
2. Documentar o passo de quem lança que, ao fim do job, compara a imagem mostrada por 'hf jobs inspect' com o digest passado e registra a divergência.
3. Rodar o --dry-run do comando.

**Definição de pronto:** Procedimento em docs/hf-jobs.md, --dry-run sem erro e sem valor de segredo, revisado pelo time de MLOps.

**Dependências:** F2.2, F2.6

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F2.8.T5 · [Data Science] Indicar em docs/poc-gate.md o arquivo e a coluna do conjunto do run_id para cada critério do gate</summary>

**Objetivo:** Mapa de critério para arquivo e coluna do conjunto de resultados, com a regra de citação do run_id.

**Passos previstos:**
1. Mapear os critérios 1, 2a, 2b e 5 e as colunas do ADR 0001 para colunas do CSV do bench e do run_log no conjunto do run_id.
2. Conferir que o CSV enviado mantém flavor, inferencia_s e pares_ge64.
3. Registrar em docs/poc-gate.md como citar o run_id junto de cada resultado.

**Definição de pronto:** docs/poc-gate.md com o mapa e a regra de citação do run_id, revisado pelo time de MLOps.

**Dependências:** F1.3 e F1.4 (regras de leitura e veredito da linha TOTAL)

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F2.8.T6 · [QA] Verificar os critérios de aceite de F2.8</summary>

**Objetivo:** Evidência de cada critério de aceite anexada ao PBI.

**Passos previstos:**
1. Rodar localmente, com destino em diretório local, processar_culto.py com a fixture, o bench com a fixture e rótulos sintéticos, o bench sem vídeo rotulado e o caso de falha de envio.
2. Conferir o teste de contrato da linhagem e o JOB_ID nulo com ambiente 'local'.
3. Pedir aprovação a Fabio e rodar, pelo comando documentado, um job de validação com o motor hsemotion sobre um vídeo do dataset permitido por F1.3 e um job com vídeo inexistente.
4. Conferir no repositório de resultados os conjuntos, o registro de falha, os tipos de arquivo e o digest da linhagem contra 'hf jobs inspect'.
5. Conferir o mapa em docs/poc-gate.md.

**Definição de pronto:** Checklist dos 11 critérios com JOB_IDs e caminhos no repositório de resultados anexada ao PBI.

**Dependências:** F2.8.T3, F2.8.T4, F2.8.T5, Aprovação de Fabio

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- supabase/migrations/0001_init.sql:18
- processar_culto.py:37,45,103-115
- bench.py:123-183,197-200,207-209,237-239,254-256
- reacao/guard.py:8
- reacao/transcribe.py:9-12
- huggingface_hub/_jobs_api.py:324-346 e cli/jobs.py:660,712 (instalados)
- commit b834dd0
- https://huggingface.co/docs/hub/jobs-manage#persist-your-results
- https://huggingface.co/docs/hub/jobs-configuration#built-in-environment-variables
- Árvore: F1.3, F1.4, F1.5, F3.5, F5.2, F7.5 e F2.5 original (disciplinas MLOps, Backend, DevOps, Data Science)
- Feature F1 detalhada: F1.1 RN11 e F1.1.T6 (fixture no dataset por revisão)

#### Premissas
- F2.8 recebe do F2.5 original a linhagem, o envio ao repositório de resultados, o registro de falha no repositório e o comando de lançamento; o run_id vem de F2.5.
- O digest da imagem não é visível de dentro do contêiner; ele é passado no lançamento e conferido com 'hf jobs inspect' por quem lança (dedução).
- O tipo do repositório de resultados (dataset privado ou Storage Bucket, que não tem versionamento, P30) segue o ADR 0002.
- O run_id e o registro de falha do bench ficam aqui, porque o bench não grava no Supabase.
- A task de Data Science complementa F1.3 e F1.4, que fixam a leitura dos critérios e o veredito da linha TOTAL; ela só aponta onde cada coluna está no conjunto do run_id (critério 11).
- Os critérios 3, 5 e 7 são verificados localmente com a fixture e rótulos sintéticos, montando o conjunto num diretório local.
- Disciplinas: MLOps, Backend, DevOps e Data Science, previstas na árvore para o F2.5 original, mais QA para verificar os critérios.
- Story points e horas são sugestão.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável.
- Item pai: Feature F2.
- Criar o PBI no Azure DevOps (item novo, dividido do F2.5 da árvore).
- Informar F4.6 de que os números do gate citam o run_id dos jobs do bench e são lidos do conjunto de F2.8.
- Informar F2.7 e F7.5 de que o conjunto e o registro de falha estão em F2.8.
