[Voltar ao épico](README.md)

# Preview — Feature F7 (novo) · Executar o piloto de 4 cultos com o relatório revisado e liberado ao pastor no painel web na Vercel

### Campos
| Campo | Conteúdo |
|---|---|
| Título | Executar o piloto de 4 cultos com o relatório revisado e liberado ao pastor no painel web na Vercel |
| Tipo | Feature |
| Pai | Epic |
| Tags | Fase 1; piloto; privacidade; Vercel; Supabase; HF Jobs |
| Estimativa | 59 pts / 295 h (soma dos PBIs, sugestão) |

### Descrição

**Problema:** O piloto não tem por onde entregar o relatório ao pastor. O repositório não tem front end: em git ls-files e na busca por gradio, streamlit, fastapi e flask não há ocorrência fora de comentários do .gitignore (linhas 65 e 219-220), em 2026-09-23. Na Vercel, o time 'Fabio Pinheiro's projects' tem só o projeto ai-guitar-coach-pilot, que não tem relação com este sistema (Vercel list_teams e list_projects, 2026-09-23). A migração não habilita RLS nem cria os perfis pastor, mídia e DPO (supabase/migrations/0001_init.sql:21). O pipeline grava com a chave de serviço, que ignora RLS (reacao/store.py:11-12,24-25; https://supabase.com/docs/guides/database/postgres/row-level-security). As colunas revisado_por e revisado_em não têm quem as escreva (0001_init.sql:16), e a revisão humana prevista em docs/onprem.md:62 não existe. Nenhum código grava a tabela service (reacao/store.py:28-44), e processar_culto.py não recebe a data do culto (processar_culto.py:34-46). Não há caminho de envio do vídeo do culto nem destino separado do corpus: o único dataset do namespace é ds-fabiopinheiro/reacao-poc-corpus, e não há bucket (HfApi.list_datasets e list_buckets, 2026-09-23). Apagar do histórico de um repositório do Hub é irreversível e não vale para tags (huggingface_hub/hf_api.py:4415-4460). O README promete que o sistema nunca guarda uma cópia do vídeo (README.pt-BR.md:16-17). A retenção existe só como comentário (0001_init.sql:20). Não há job agendado nem webhook ('hf jobs scheduled ps -a' vazio e HfApi.list_webhooks() com lista vazia, 2026-09-23), e nenhum código sinaliza a qualidade da medição de cada culto.

**Solução proposta:** A equipe de mídia envia os vídeos do piloto a um destino privado do Hugging Face, separado do corpus, sem passar pela Vercel. Cada culto é processado no HF Jobs assim que o vídeo chega, pela imagem de release do piloto, publicada com digest antes do primeiro culto, desde que o RIPD, o aviso e, se acionada, a forma de oposição ou de consentimento estejam em vigor na data do culto. O job grava o culto e a data a partir do nome do arquivo. O vídeo sai do destino ao fim do job concluído, se o plano de F6.6 não previr rotulagem do culto; se previr, os rotuladores do piloto o leem na ferramenta do Space privado de F3.3, os rótulos vão ao destino decidido no ADR de F6.2, fora do corpus, e a varredura agendada apaga o vídeo depois do fim registrado da rotulagem ou no prazo máximo do ADR de F6.2. Os segredos que ficam guardados no Job de origem do webhook e no Job agendado de varredura têm escopo mínimo e entram no inventário de credenciais. O relatório aparece num painel web na Vercel, que estende a tela do relatório e o formulário de nota da Fase 0 (F5.8 e F5.7). O painel lê do Supabase só agregados, eventos e insights, mais as exceções aprovadas na matriz de acesso, com Supabase Auth, RLS por perfil (pastor, revisor, mídia e DPO) e a chave publicável. O projeto Supabase não é conectado à Vercel por integração. O perfil pastor recebe só os insights aprovados na revisão humana, e o revisor vê a qualidade de medição de cada culto antes de liberar. A retenção e o acesso dos quatro perfis estão prontos antes do primeiro culto. Os 4 cultos são processados, revisados e consolidados numa decisão registrada.

**Usuários impactados:** Pastor da igreja do piloto (perfil pastor), Equipe de mídia da igreja do piloto (perfil midia), Encarregado de dados, DPO (perfil dpo), Revisor humano do relatório (perfil revisor; ainda não se sabe quem ocupa), Rotuladores dos cultos do piloto (ferramenta do Space privado de F3.3, lista definida no plano de F6.6), Fabio Pinheiro (operação dos jobs e decisão de conclusão da Fase 1)

**Valor de negócio:** Executa a Fase 1 do roteiro: piloto com uma igreja e 4 cultos, depois do RIPD e do aviso à congregação (README.pt-BR.md:35). O pastor recebe um relatório que uma pessoa revisou antes, e é o banco que impõe o acesso por perfil. O resultado é a decisão registrada de conclusão da Fase 1 pelo critério de F6.6. Essa decisão é o insumo de qualquer passo seguinte do roteiro (README.pt-BR.md:36).

**Regras de negócio:**
- RN01 – Nenhum culto do piloto é processado antes de estarem em vigor, na data do culto, o RIPD (F6.3), o aviso à congregação (F6.4) e, se acionada, a forma de oposição ou de consentimento (F6.5) (README.pt-BR.md:35).
- RN02 – O painel web na Vercel lê do Supabase só com Supabase Auth, RLS por perfil e a chave publicável. A chave de serviço fica só nos jobs do HF (P3 revisada; reacao/store.py:12). O projeto na Vercel não tem as variáveis SUPABASE_SECRET_KEY, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_JWT_SECRET, POSTGRES_URL, POSTGRES_URL_NON_POOLING, POSTGRES_PRISMA_URL nem POSTGRES_PASSWORD, e o projeto Supabase não é conectado a ele pela integração do Marketplace nem pela de branching (https://supabase.com/docs/guides/integrations/vercel-marketplace; https://supabase.com/docs/guides/deployment/branching/integrations).
- RN03 – A Vercel não recebe vídeo, quadro, recorte de rosto nem observação por rosto (P3 revisada; CLAUDE.md regras 1 e 2).
- RN04 – O vídeo do piloto vai direto a um destino privado no HF, separado do dataset do corpus e dos rótulos. Ele é apagado desse destino ao fim do job concluído, ou, se o plano de F6.6 prevê rotulagem do culto, depois do fim registrado da rotulagem e nunca depois do prazo máximo do ADR de F6.2 (F6.2 RN08; P3 revisada; huggingface_hub/hf_api.py:4415-4460; README.pt-BR.md:16-17; docs/onprem.md:63).
- RN05 – O perfil pastor só vê insight aprovado na revisão humana (docs/onprem.md:62; supabase/migrations/0001_init.sql:16).
- RN06 – Janela marcada como insuficiente (sem quadro com plateia ou com média de rostos mensuráveis por quadro com plateia abaixo de 10) aparece sem percentuais em todas as telas (CLAUDE.md regra 3; reacao/aggregate.py:26-31; reacao/types.py:7).
- RN07 – Todo texto exibido ao pastor passa pelo lint, inclusive os textos fixos da interface (CLAUDE.md regra 4).
- RN08 – 'Tabelas do Supabase não têm campo por pessoa' (CLAUDE.md regra 6, texto literal; tests/test_schema.py:5). Se essa regra vale para as contas da equipe e do pastor e onde fica o vínculo entre conta e perfil são decididos em D7 de F2.4.T4, antes de F5.6, e confirmados ou ajustados por F6.2, com migração se mudar.
- RN09 – Retenção: agregados por 12 meses, relatórios e insights por 24 meses (supabase/migrations/0001_init.sql:20). As demais tabelas e os vídeos que ficarem no destino seguem F6.2 e F6.3.
- RN10 – Toda execução no HF Jobs, inclusive agendada ou disparada por webhook, exige aprovação prévia do dono da conta (P7).
- RN11 – O piloto tem uma igreja e 4 cultos (README.pt-BR.md:35).
- RN12 – Os perfis do painel leem só as tabelas da lista de D7 de F2.4.T4: window_aggregate, event, insight, a tabela de execuções liberadas de F5.6 e, na Fase 1, os indicadores de F7.6; moment e service só se a confirmação do usuário registrada em D7 os incluir. Os perfis gravam só insight_feedback e o estado de revisão do insight. Outra tabela só entra como exceção aprovada pelo encarregado e registrada na matriz de F7.2 e em D7. transcript_segment e run_log não têm leitura por nenhum perfil do painel (P3 revisada; F2.4.T4; 0001_init.sql:4,13,18).
- RN13 – A Vercel é operadora de dados do piloto. Nenhum dado do piloto chega a ela antes de o RIPD (F6.3) a incluir, com a região das funções e a transferência internacional (https://vercel.com/docs/functions/configuring-functions/region).
- RN14 – Os jobs que processam os cultos do piloto e a varredura agendada rodam com 'hf jobs run <imagem>@<digest>' (arvore_v1.json, F2.4) pela imagem de release do piloto, com o digest registrado antes do primeiro culto (F7.7.T1).
- RN15 – Os segredos guardados na especificação do Job de origem do webhook e do Job agendado têm escopo mínimo, ficam no inventário de F2.6.T6 com o id do Job, sem o valor, e são trocados recriando o Job (https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets; huggingface_hub/hf_api.py:11378-11386,13378).
- RN16 – Os rótulos de referência dos cultos do piloto são feitos na ferramenta do Space privado de F3.3, pelo protocolo de F3.2, sem som salvo exceção registrada no RIPD, e ficam no destino decidido no ADR de F6.2, fora do dataset do corpus (F6.6 RN03; F6.2.T8; CLAUDE.md regras 1 e 5).

**Fora de escopo:**
- Painel ao vivo para a cabine e sinal ao pregador (README.pt-BR.md:36)
- Operação semanal on-premises com cron de segunda-feira (docs/onprem.md:60-64)
- Mais de uma igreja ou mais de 4 cultos (README.pt-BR.md:35)
- Métrica por pessoa, assento ou setor pequeno (CLAUDE.md regra 3)
- Envio, exibição ou armazenamento na Vercel de vídeo, quadro, recorte de rosto ou observação por rosto (P3 revisada)
- Ferramenta de rotulagem (F3.3), que continua em Space privado
- Relatório do culto público e notas do critério 4 da Fase 0 para Fabio e Filipe (F5.6, F5.7 e F5.8)
- Confirmação do plano e dos termos de uso da Vercel antes de o projeto ser criado na Fase 0 (antes de F5.6.T2; D8 de F2.4.T4 registra a pendência, sem task de confirmação em F5.6 ainda)
- Job de CI com o Supabase local e as migrações (F2.6.T4)
- Relatório em PDF ou por e-mail (escopo excluído do épico)
- Edição do texto de um insight pelo revisor
- Reprocessamento de culto para atualizar indicadores de qualidade

**Dependências técnicas:**
- Imagem com digest (F2.2), ADR 0002 com namespace, acesso e modo de execução dos jobs (F2.4), run_id e registro de falhas no Supabase (F2.5) e conjunto de cada execução com linhagem no repositório de resultados (F2.8)
- Imagem de pré-release com o código de F7.5 para os testes (F7.5.T6) e imagem de release do piloto com as mudanças de F6.2, F7.5 e F7.6, publicada antes do primeiro culto (F7.7.T1)
- Projeto Supabase de desenvolvimento com RLS habilitada, tokens de escopo mínimo e inventário de credenciais que inclui os segredos guardados em Jobs (F2.6 e F2.6.T6)
- Projeto novo na Vercel no time 'Fabio Pinheiro's projects' (slug fabiopinheiro-projects, id team_TFJpulVK8Dcufy5SIecwChUh), criado em F5.6.T2, com o plano e os termos registrados como pendência em D8 de F2.4.T4 e sem task de confirmação antes de F5.6.T2 (pendência em F5.6), com o painel base de F5.6 (Supabase Auth em F5.6.T3, políticas em F5.6.T4, lint dos textos fixos em F5.6.T5, lista em F5.6.T6), a tela do relatório de F5.8.T1 e o formulário de nota de F5.7.T2, sem chave de serviço
- Supabase local no CI do GitHub Actions (https://supabase.com/docs/guides/deployment/ci/testing), montado em F2.6.T4 (pendência) e estendido em F7.2.T4 com o mecanismo de perfil e a seed do piloto
- Destino privado no HF para os vídeos do piloto: Storage Bucket (https://huggingface.co/docs/hub/storage-buckets) ou repositório de dataset próprio
- Webhooks do Hub que disparam Jobs (https://huggingface.co/docs/hub/jobs-webhooks), Jobs agendados (https://huggingface.co/docs/hub/jobs-schedule) ou pg_cron no Supabase (https://supabase.com/docs/guides/cron/quickstart)
- Decisão D7 de F2.4.T4 (vínculo entre conta e perfil, alcance da regra 6 e tabelas do painel), decisões e documentos de F6.2 (minimização, confirmação ou ajuste de D7, regra de apagamento dos vídeos e destino dos rótulos do piloto), F6.3 (RIPD com a Vercel como operadora, região das funções e transferência internacional), F6.4 (aviso), F6.5 (se acionado) e F6.6 (plano de medição, limites de qualidade e critério de conclusão)
- Lint ampliado de F1.7 (reacao/lint.py) para os textos exibidos ao pastor
- Ferramenta de rotulagem do Space privado de F3.3 e protocolo de F3.2, estendidos em F7.9 para ler o destino do piloto e gravar no destino dos rótulos do piloto do ADR de F6.2

**Riscos:**
- O plano e os termos de uso da Vercel para este projeto não estão confirmados. Times no plano Hobby só podem ter uso pessoal não comercial (https://vercel.com/docs/limits/fair-use-guidelines). O projeto é criado e usado com Filipe já na Fase 0 (F5.6.T2), D8 de F2.4.T4 registra o plano e os termos como pendência, com Fabio responsável, mas nenhuma task de F5.6 os confirma antes de F5.6.T2 (pendência). F7.2.T2 confirma ou reconfirma o plano para o uso com dados da igreja do piloto. Se o plano não permitir o uso, o painel precisa de outro plano ou de outro host.
- Se o projeto Supabase for conectado ao projeto da Vercel pela integração do Marketplace, a Vercel recebe sozinha SUPABASE_SECRET_KEY, SUPABASE_JWT_SECRET, POSTGRES_URL e POSTGRES_PASSWORD, entre outras (https://supabase.com/docs/guides/integrations/vercel-marketplace). A integração de branching também atualiza sozinha as variáveis do projeto (https://supabase.com/docs/guides/deployment/branching/integrations). A chave secreta usa o papel service_role, e o dono postgres também tem bypassrls, então essas variáveis passam por cima do RLS (https://supabase.com/docs/guides/database/postgres/row-level-security).
- Variáveis sensíveis da Vercel não podem ser lidas depois de criadas (https://vercel.com/docs/environment-variables/sensitive-environment-variables). Uma chave de serviço cadastrada com outro nome não aparece numa busca pelo nome; por isso a verificação é por lista permitida.
- As Vercel Functions rodam por padrão em iad1 (Washington, D.C., EUA) em projetos novos (https://vercel.com/docs/functions/configuring-functions/region). Se a região não for definida conforme o RIPD, insights, notas e dados de conta são tratados em outro país sem registro de transferência internacional.
- Os logs de runtime da Vercel ficam guardados por prazo que depende do plano: 1 hora no Hobby e 1 dia no Pro (https://vercel.com/docs/logs/runtime). Se o painel registrar texto de insight ou de nota em log, esse conteúdo fica na Vercel por esse prazo.
- Se o destino dos vídeos for um repositório, o squash é irreversível e não se aplica a tags (hf_api.py:4415-4460). Além disso, arquivos removidos continuam no histórico de refs de pull request (https://huggingface.co/docs/hub/storage-limits#deleting-pull-request-refs).
- create_bucket sem 'private' cria um bucket público, salvo se o padrão da organização for privado (huggingface_hub/hf_api.py:13825-13827). Um destino criado sem a opção explícita expõe os vídeos.
- O papel de escrita numa organização do HF vale para os recursos da organização conforme o papel, e resource groups só existem no Enterprise Hub (https://huggingface.co/docs/hub/security-tokens; hf_api.py:13828-13830). Se não houver token fine-grained restrito ao destino, a credencial da equipe de mídia só fica restrita numa organização que contenha apenas o destino.
- O webhook de bucket dispara em arquivos adicionados e apagados, e sobrescrever um arquivo é reportado como 'add' (https://huggingface.co/docs/hub/webhooks#buckets). O apagamento do vídeo ao fim do job ou depois da rotulagem e o da varredura de F7.4 disparam jobs pagos, que precisam terminar antes de baixar vídeo e entrar na aprovação de custo.
- Com webhook, os jobs rodam sem um humano presente, o que entra em conflito com a aprovação prévia de custo (P7). A aprovação precisa ser dada antes do primeiro envio.
- Os valores dos segredos do Job de origem do webhook e do Job agendado ficam guardados, criptografados, no HF enquanto esses Jobs existirem (https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets; huggingface_hub/_jobs_api.py:211-212). Como update_webhook não aceita job_id e a biblioteca só altera labels de um Job agendado (hf_api.py:11378-11386,13378), revogar ou trocar um segredo exige recriar o Job e, no webhook, o próprio webhook. Um segredo fora do inventário de F2.6.T6 fica sem dono e sem rotação.
- Se o Job de origem do webhook ou o Job agendado ficarem num digest anterior ao da release do piloto, os cultos são processados sem as mudanças de minimização de F6.2 ou sem os indicadores de F7.6. F7.7.T1 faz a troca antes do primeiro culto.
- Um vídeo cujo job falhou fica no destino até o reprocessamento ou até a varredura de F7.4. Enquanto isso, a promessa do README de nunca guardar cópia do vídeo (README.pt-BR.md:16-17) não vale para esse arquivo.
- O campo de comentário da nota do pastor é texto livre e pode receber nome de pessoa da congregação. F6.2 decide se o campo continua.
- A documentação do HF não informa o fuso do CRON dos Jobs agendados (P22). Os exemplos de pg_cron no Supabase estão em GMT (https://supabase.com/docs/guides/cron/quickstart).
- O projeto Supabase deste sistema não foi encontrado na conta conectada (Supabase list_projects, 2026-09-23). Tudo em F7 depende de F2.6.
- A operação dos 4 cultos (F7.7) depende de quem ocupa o perfil revisor, ainda não definido.
- Se a rotulagem de um culto não terminar no prazo máximo de retenção do ADR de F6.2, a varredura apaga o vídeo e o culto fica sem rótulos de referência; o que acontece com a rotulagem nesse caso é regra do ADR de F6.2 (F6.2.T1).
- Manter o vídeo no destino até o fim da rotulagem contraria a frase do README de que o sistema nunca guarda cópia do vídeo (README.pt-BR.md:16-17). A frase precisa ser atualizada com aprovação antes do aviso de F6.4, ou o plano de F6.6 não pode prever rotulagem que dependa do vídeo guardado.

**Estratégia de fatiamento:** Fatiamento por passo do fluxo do culto do piloto, com o acesso por perfil pronto antes da primeira leitura. Os PBIs são: envio do vídeo (F7.1), acesso dos perfis pastor e revisor (F7.2), revisão e liberação (F7.3), retenção (F7.4), processamento (F7.5), sinalização de qualidade (F7.6), operação dos 4 cultos, rotulagem e consolidação (F7.7), acesso dos perfis mídia e DPO (F7.8) e leitura do destino do piloto pela ferramenta de rotulagem (F7.9). A ordem sugerida é F7.1 e F7.2; depois F7.3, F7.5, F7.8 e F7.9, com F7.4.T1 antes de F7.5.T2 (condição de apagamento depois da rotulagem), F7.5.T1 antes de F7.4.T2 se a retenção usar service.data e F7.5.T6 (imagem de pré-release) antes de F7.5.T4; depois F7.4 e F7.6; e por fim F7.7, que começa pela imagem de release do piloto e pela troca de digest dos jobs automáticos (F7.7.T1), só processa o primeiro culto com F7.8 e F7.9 prontos e rotula cada culto antes da consolidação. F7.2 foi dividido por perfil (pastor e revisor em F7.2, mídia e DPO em F7.8). Nenhum PBI foi fatiado por camada técnica: tela, banco e teste do mesmo comportamento ficam no mesmo PBI. A construção (F7.1 a F7.6, F7.8 e F7.9) fecha com vídeo público de teste, e só F7.7 usa os cultos reais. Se F7.5 não couber numa sprint, a divisão sugerida é por modo de disparo: disparo manual com checagem de pré-requisitos primeiro, webhook depois.

### Critérios de aceite
- Cada um dos 4 cultos do piloto tem relatório revisado e liberado ao perfil pastor no painel web na Vercel, ou o motivo registrado de não ter sido liberado.
- Nenhum culto do piloto com data anterior à vigência do RIPD, do aviso e, se acionada, da forma de F6.5 tem janelas, eventos ou insights gravados.
- Uma consulta direta à API do banco com a sessão de uma conta do perfil pastor não retorna insight pendente nem rejeitado.
- Com a sessão de qualquer perfil do painel, uma consulta direta a transcript_segment retorna zero linhas ou acesso negado.
- A lista de variáveis do projeto na Vercel, em todos os ambientes, é igual à lista permitida de F7.2 (URL do projeto Supabase e chave publicável). Nenhuma destas variáveis existe no projeto: SUPABASE_SECRET_KEY, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_JWT_SECRET, POSTGRES_URL, POSTGRES_URL_NON_POOLING, POSTGRES_PRISMA_URL e POSTGRES_PASSWORD. O projeto Supabase não está conectado ao projeto da Vercel pela integração do Marketplace nem pela de branching.
- Os arquivos do deployment de produção na Vercel não contêm vídeo, quadro, recorte de rosto nem observação por rosto.
- Nenhum vídeo do piloto aparece no dataset do corpus, no bucket jobs-artifacts nem nos arquivos do deployment na Vercel, e a gravação na igreja segue o procedimento de F7.1.
- No fim do piloto, as tags e as revisões do dataset do corpus resolvem para os mesmos commits registrados antes do primeiro envio (F7.1.T4).
- A retenção está ativa antes do primeiro culto do piloto, e o teste automatizado de datas vencidas passa.
- Antes do primeiro culto, o Job de origem do webhook, ou o comando manual documentado, e o Job agendado de varredura usam o digest da imagem de release do piloto, e o inventário de F2.6.T6 lista os segredos guardados nesses Jobs, sem o valor.
- Em todas as telas, a janela marcada como insuficiente (sem quadro com plateia ou com média de rostos mensuráveis por quadro com plateia abaixo de 10) aparece sem percentual.
- Cada culto processado tem os rótulos de referência previstos no plano de F6.6 feitos e revisados, com a data do fim da rotulagem, ou o motivo registrado, e o vídeo do culto saiu do destino depois dessa data ou no prazo máximo do ADR de F6.2.
- Existe o documento de consolidação dos 4 cultos, com a decisão de conclusão da Fase 1 assinada pelas pessoas definidas em F6.6.

### Alterações em relação à árvore
- Título da Feature: 'no Space privado' passou a 'no painel web na Vercel' (P3 revisada).
- Problema e solução da Feature: o front end do produto passou do Space para o painel web na Vercel, e o login passou a ser pelo Supabase Auth. O fato de que o time da Vercel só tem o projeto ai-guitar-coach-pilot foi acrescentado com fonte.
- Problema da Feature (revisão): a busca por front end passou a dizer 'sem ocorrência fora de comentários do .gitignore (linhas 65 e 219-220)'; 'o namespace tem só o dataset' passou a 'o único dataset do namespace', com HfApi.list_datasets e list_buckets; a falta de webhook ganhou a fonte HfApi.list_webhooks(); entraram a promessa do README sobre cópia do vídeo e a falta de código que grave service.
- Usuários: o revisor humano ganhou o perfil revisor, porque com a chave pública e o RLS só um perfil com permissão de escrita consegue registrar a revisão de F7.3.
- Regras da Feature (revisão): RN02 ganhou a lista de variáveis proibidas e a proibição das integrações Marketplace e branching; RN04 ganhou o apagamento do vídeo ao fim do job; RN06 usa a definição de insuficiente do código (aggregate.py:26-31); RN08 cita a regra 6 com o texto literal, sem o qualificador 'da congregação'; entraram RN12 (tabelas lidas pelo painel) e RN13 (Vercel como operadora no RIPD).
- Critérios da Feature (revisão): o critério 2 passou a verificar a data do culto; o de variáveis virou lista permitida, lista proibida e ausência de integração; o dos vídeos passou a termos observáveis; o do corpus compara com as refs registradas em F7.1.T4; o de janela usa a marcação insuficiente; entrou o critério de transcript_segment.
- Riscos da Feature (revisão): entraram as integrações Marketplace e branching, as variáveis sensíveis ilegíveis, a região padrão iad1, a retenção de logs da Vercel, o plano Hobby, o papel de organização no HF, os eventos de apagamento no webhook de bucket e o vídeo que fica no destino depois de uma falha.
- F7.1: saiu a opção 'formulário de envio no Space'. O envio é por CLI ou pela página do destino no Hub, sem passar pela Vercel (P3 revisada). A disciplina Front end saiu, com o motivo nas premissas do PBI. Entraram o risco de bucket criado público por padrão e o 'viewer: false' se o destino for repositório de dataset. O título ganhou 'do HF'.
- F7.1 (revisão): o contexto corrigiu o fato sobre o namespace; a verificação do escopo do token foi para T1 como critério da decisão, com a exigência de organização só com o destino se só o papel de organização servir; T1 registra a região do destino; entrou o critério de recusa de escrita no repositório de resultados e em jobs-artifacts; T4 registra as refs e tags do corpus antes do primeiro envio; entrou RN09 (apagamento ao fim do job) e a premissa do conflito com o README; dependência de F2.5.
- F7.2: no título, 'Space' passou a 'painel web na Vercel' e 'JWT de papel' passou a 'Supabase Auth e RLS'. Saiu a opção de JWT assinado pelo servidor do Space e entrou o perfil revisor.
- F7.2 (revisão): dividido em F7.2 (pastor e revisor) e F7.8 (mídia e DPO). Entraram a regra de tabelas lidas pelo painel, a lista permitida e a lista proibida de variáveis, a proibição das integrações, a regra 6 literal com as duas opções de F6.2 (raw_app_meta_data ou tabela com exceção registrada), o CI só com Supabase local e sem chave de serviço (task nova de DevOps T4), a task de Governança sobre plano e termos da Vercel (T2), a região das funções conforme o RIPD, o critério de revogação, a busca por sb_secret_ e JWT service_role no bundle e a listagem dos arquivos do deployment. A URL da frase sobre variáveis sensíveis passou a sensitive-environment-variables. A dependência de F5.6 passou a incluir a base de autenticação, e saiu a criação do projeto na Vercel por F7.2. A task de lint (antiga T8) saiu. Tasks: 9 para 7; critérios: 14 para 10.
- F7.3: 'no Space' passou a 'no painel web na Vercel'. O estado de revisão (pendente, aprovado, rejeitado) ficou explícito, com migração nova, porque o schema só tem revisado_por e revisado_em (0001_init.sql:16).
- F7.3 (revisão): o revisor escreve só a coluna de estado, e o banco preenche revisado_em, revisado_por e avaliador; o valor de revisado_por (código de papel) foi para premissas como proposta a confirmar em F6.2; entraram uma nota por insight e por avaliador, a imutabilidade de texto, trecho, minuto e sinais e o campo de comentário condicionado a F6.2; F5.7 virou dependência condicional; entraram critérios de alteração de colunas, valores forjados e segunda nota.
- F7.4: entrou o fato de que transcript_segment, moment, event e insight não têm coluna de data (0001_init.sql:13-16), e a retenção por prazo exige uma data de referência. Também entraram o fuso GMT dos exemplos de pg_cron e a permanência de arquivos em refs de pull request depois do squash.
- F7.4 (revisão): o apagamento do vídeo ao fim do job saiu de F7.4.T4 e foi para F7.5.T2; F7.4.T4 cobre só a varredura por prazo dos vídeos que ficaram no destino. A aprovação de custo vem antes de criar o Job agendado ativo, ou ele é criado suspenso. Os casos de erro passaram a ser por mecanismo (papel sem permissão no banco, token inválido no job). As contagens passaram a ser persistidas (banco em T2, vídeos no registro de F2.5). T1 lista as tabelas do 'relatório' e inclui a retenção dos logs de runtime da Vercel. Entraram dependências de F7.2.T2, F7.2.T4 e, se usada service.data, de F7.5.T1.
- F7.5: 'relatório para revisão no Space' passou a 'no painel web'. Entrou a leitura do vídeo por caminho de bucket, porque resolve_video só trata hf://datasets/ (processar_culto.py:24).
- F7.5 (revisão): T1 deriva id e data do culto do nome do arquivo, grava service.culto e service.data e recusa arquivo fora do padrão; T2 confere o tamanho antes do download e apaga o vídeo ao fim do job concluído; T3 ignora eventos de apagamento e arquivos fora do padrão, fixa a validação com 'hf jobs run --dry-run' e define os parâmetros do disparo manual; T5 pede aprovação de custo dos jobs de teste. O contexto corrigiu a frase do run_log e a premissa sobre webhook de bucket. O critério de logs virou premissa. A operação dos 4 cultos (antiga T6 e critérios dos 4 cultos) foi para F7.7, e as dependências de F7.4 e F6.6 foram para F7.7.
- F7.6: 'no Space' passou a 'no painel web na Vercel'. A disciplina Backend entrou, com o motivo nas premissas do PBI. As dependências de F7.2 (perfil revisor) e F7.3 (tela de revisão onde o alerta aparece) foram acrescentadas.
- F7.6 (revisão): a comparação com os limites passou para a leitura, no banco, sem reprocessar; T1 cria o arquivo versionado de limites a partir do documento de F6.6; T2 grava só os indicadores; T3 usa tabela com RLS ou visão com security_invoker = true; a forma de agregar ficou só com F7.6.T1; o critério de mudança de limite não exige reprocessar.
- F7.7 (revisão): passou a 'Operar os 4 cultos do piloto, consolidar os resultados e registrar a decisão de conclusão da Fase 1'. Entraram tasks de disparo e acompanhamento por culto (MLOps, com o motivo nas premissas), revisão e liberação por culto (Governança e Privacidade) e coleta das notas (Data Science). A extração roda só no HF Jobs. A conferência de QA vem antes das assinaturas. O critério de lint passou a verificar as listas PROIBIDO e PROIBIDO_INDIVIDUAL. Entraram as verificações de fim de piloto dos vídeos e das refs do corpus.
- F7.8 (revisão): PBI novo com os perfis mídia e DPO, vindo da divisão de F7.2.
- Revisão 2 (plano da Vercel): F7.2.T2 passou a 'Reconfirmar o plano e os termos de uso da Vercel para o painel com dados da igreja do piloto' (3 h para 2 h) e depende da confirmação que a revisão move para a primeira task de F5.6. F7.4.T1 passou a depender dessa confirmação, e F7.4 RN07 cita as duas. O primeiro risco e a premissa do plano da Feature foram reescritos, e entrou o item de fora de escopo. A task nova em F5.6, as dependências de F6.2.T1, F6.2.T2 e F6.3.T1 e o registro em D8 de F2.4.T4 ficaram em pendências.
- Revisão 2 (imagem do piloto): entrou F7.5.T6 [DevOps], que publica por tag de pré-release a imagem com o código de F7.5 e valida o comando com --dry-run antes dos testes; a validação por --dry-run saiu de F7.5.T3, que ganhou o caso sem payload e os testes do filtro. F7.5.T6 foi numerada no fim para não mudar as referências a F7.5.T4 e F7.5.T5. Entrou F7.7.T1 [DevOps], que publica por tag de release a imagem do piloto e troca o digest do Job de origem do webhook e do Job agendado antes do primeiro culto; as antigas F7.7.T1 a F7.7.T7 passaram a F7.7.T2 a F7.7.T8. F7.7 ganhou a disciplina DevOps, com o motivo nas premissas, um critério e as regras RN10 e RN11. F7.4.T4 ganhou o script de varredura com imagem de pré-release (6 h para 8 h). A Feature ganhou RN14, um critério, um risco e a dependência técnica das duas imagens.
- Revisão 2 (segredos dos jobs automáticos): F7.5.T4 e F7.4.T4 passaram a definir os segredos guardados na especificação do Job de origem e do Job agendado, com escopo mínimo, rotação por recriação e registro no inventário de F2.6.T6, e dependem de F2.6.T6. F7.5.T4 passou de 6 h para 8 h e depende de F7.5.T6 no lugar de F7.5.T3. F7.5 RN06, os critérios de F7.4 (juntado ao de aprovação de custo do Job agendado, para manter 10) e de F7.5 e as tasks de QA F7.4.T5 e F7.5.T5 foram ajustados. A Feature ganhou RN15, um risco e uma premissa de dedução sobre o reuso dos segredos no disparo. A mudança do modelo de segredos de F2.6 ficou em pendências.
- Revisão 2 (reuso das telas de F5): a dependência de F7.3 em F5.7 ficou incondicional e entrou F5.8. F7.3.T4 passou a 'Estender ao perfil pastor a tela do relatório de F5.8.T1 e o formulário de nota de F5.7.T2, com só insights aprovados e a data da revisão' (6 h para 5 h), com dependências de F5.8.T1 e F5.7.T2. F7.3.T3 reaproveita a listagem de insights de F5.8.T1, e F7.3.T2 não altera as políticas de nota de F5.7.T1. Pelo mesmo motivo, F7.2.T6 passou a reaproveitar F5.6.T6 e F5.8.T1 (10 h para 8 h), F7.2 ganhou a dependência de F5.8, e F7.2.T1 decide a exceção da tabela de execuções liberadas de F5.6.
- Revisão 2 (Supabase local no CI): F7.2.T4 passou a 'Acrescentar ao job de Supabase local do CI o mecanismo de perfil do piloto e a seed de teste' (5 h para 3 h), sobre o job que a revisão move para F2.6.T4 (pendência). F7.2.T7 e F7.4.T3 passaram a citar esse job, e a dependência técnica da Feature foi reescrita.
- Revisão 2 (acesso de mídia e DPO antes do piloto): F7.8 entrou nas dependências de F7.7 e de F7.7.T2, que confere o acesso antes do primeiro culto (escopo do épico: perfis pastor, mídia e DPO).
- Revisão 2 (alinhamento com o detalhamento de F5): referências a 'F5.6 relido' passaram a citar as tasks de feature_F5_v3.json (F5.6.T1 a F5.6.T6, F5.7.T2 e F5.8.T1), e as pendências de F5.6 relido e F5.7 relido foram trocadas pelas pendências específicas desta revisão.
- Reconciliação (F2.5 → F2.8): F7.1 passou a depender de F2.6.T1 e F2.8 para o repositório de resultados; F7.7 e F7.7.T5 passaram a depender de F2.8 (repositório de resultados com linhagem), mantendo F2.5 para o registro de execução; F7.5.T3 ganhou F2.8 pela linhagem; 'repositório de resultados de F2.5' passou a 'de F2.8' em todo o texto; F7.7 RN04 cita F2.5 e F2.8. F7.5, F7.6 e F7.4.T4 continuam com F2.5 (run_id e registro de falha).
- Reconciliação (plano da Vercel): a 'primeira task de F5.6' não existe no detalhamento de F5; as referências passaram a D8 de F2.4.T4 (pendência registrada) e a F5.6.T2. F7.2.T2 passou a 'Confirmar para o piloto o plano e os termos de uso da Vercel do painel' (2 h para 3 h), confirma o plano se não houver registro anterior e depende de D8 e de F5.6.T2. F7.4.T1, F7.4 (dependências, RN07 e contexto), o primeiro risco, a premissa do plano, a dependência técnica e os itens de fora de escopo foram ajustados.
- Reconciliação (D7 de F2.4.T4): o vínculo entre conta e perfil e o alcance da regra 6 passaram a vir de D7 de F2.4.T4, confirmados ou ajustados por F6.2, em RN08 da Feature, F7.2 (dependências, RN06, T1, T3 e T4) e F7.8 (dependências, RN06 e T1). F7.2.T3 passou a estender o papel de avaliador de F5.6.T3 e ganhou dependências de F2.4.T4 e F5.6.T3.
- Reconciliação (tabelas do painel): RN12 da Feature, F7.2 RN03, F7.2.T1 e F7.8 RN02 passaram a partir da lista de D7 de F2.4.T4 (window_aggregate, event, insight, execuções liberadas de F5.6, indicadores de F7.6; moment e service conforme a confirmação registrada), com run_log e transcript_segment sem leitura; F7.6 (RN05, dependência de F7.2, premissa e contexto) passou a citar os indicadores na lista de D7.
- Reconciliação (IDs antigos): F7.2.T3 ganhou o passo de comentar na migração nova a troca da referência 'PBI-041/PBI-057' de supabase/migrations/0001_init.sql:21 por F7.2 e F7.8.
- Reconciliação (igreja do piloto): F7.1.T3 passou a depender de F6.3.T8 (igreja, controlador e encarregado confirmados), e as premissas sobre a PIB apontam para F6.3.T8.
- Reconciliação (aprovação P7): 'Aprovação de Fabio (P7), com flavor, duração e custo previstos' entrou nas dependências de F7.4.T4 e F7.7.T1, citadas na revisão, e também de F7.4.T5, F7.5.T5, F7.7.T2 e F7.7.T5, que também rodam jobs pagos (a revisão usou a numeração antiga de F7.7).
- Reconciliação (rotulagem do piloto): PBI novo F7.9 (5 pontos) com T1 [Visão Computacional] leitura do destino do piloto na ferramenta de F3.3, T2 [DevOps] token e lista de rotuladores, T3 [Front end] marcação de momentos se o plano pedir e T4 [QA]. F7.7 passou a 'Operar e rotular os 4 cultos...' (8 para 13 pontos), com F7.7.T9 [Visão Computacional] rotulagem e F7.7.T10 [Data Science] revisão por amostragem e registro do fim da rotulagem; F7.7.T5 depende de F7.7.T10; F7.7.T2, T5 e T7 ajustados; entraram RN12, um critério e as dependências de F7.9, F3.2 e F3.3. F7.5.T2 deixou de apagar o vídeo de culto com rotulagem prevista e grava a marca 'aguardando rotulagem' (6 h para 7 h); F7.5 RN13, critério 2 e T5 ajustados. F7.4.T1 registra destino e retenção dos rótulos do piloto e o local do registro de fim da rotulagem (4 h para 5 h); F7.4.T4 apaga os vídeos com rotulagem concluída; F7.4.T5 testa os dois casos (4 h para 5 h); F7.4 ganhou RN09 e RN10. F7.1 (para, RN09, T3 e premissa) e a Feature (usuários, solução, RN04, RN16, critério, riscos, dependência técnica, estratégia e premissas) foram ajustados.

### Premissas
- P3 revisada prevalece sobre P3, P9, P10 e P11 onde elas falam de Space para o front end do produto. O painel web fica num projeto novo do time 'Fabio Pinheiro's projects' na Vercel. Em 2026-09-23 esse time tem só o projeto ai-guitar-coach-pilot (Vercel list_teams e list_projects).
- F5.6 e F5.7, relidos pela P3 revisada, nunca usam a chave de serviço do Supabase na Vercel. Como F5.6 e F5.7 são da Fase 0 e F7 só começa depois da decisão de F6.1 (P23), F7.2 não pode ser pré-requisito de F5.6. O detalhamento de F5 (feature_F5_v3.json) já põe em F5.6 o diretório do painel e o arquivo de textos fixos (F5.6.T1), o projeto na Vercel com só a URL e a chave pública (F5.6.T2), o Supabase Auth com cadastro fechado (F5.6.T3), a tabela de execuções liberadas com as políticas do avaliador do gate (F5.6.T4), o lint dos textos fixos (F5.6.T5) e a lista de execuções (F5.6.T6), e em F5.8.T1 e F5.7.T2 a tela do relatório e o formulário de nota. F7.2 e F7.3 estendem essa base.
- Revisão não aplicada em parte: F7.2 como pré-requisito de F5.6 (separar F7.2.T2 e T3 antes de F5.6) — F5.6 é da Fase 0 e F7 só começa depois de F6.1 (P23). A base de autenticação foi atribuída a F5.6, a outra opção da própria revisão ('numa task de F5.6'), e registrada como pendência.
- Plano e termos de uso da Vercel para este projeto: pendência, não fato. A consulta ao time pela API não retornou o plano (Vercel get_team, 2026-09-23). D8 de F2.4.T4 registra a pendência com responsável, e o detalhamento de F5 põe o plano como critério do ADR 0002 (feature_det_F5.json), mas nenhuma task de F5.6 confirma o plano antes de F5.6.T2. F7.2.T2 confirma ou reconfirma o plano para o uso com dados da igreja do piloto e registra se o projeto foi usado na Fase 0 sem confirmação.
- O login do painel é pelo Supabase Auth. A opção da árvore de ligar o login OAuth de um Space a um papel no Supabase deixou de valer.
- Os PBIs de F7 só começam se a decisão de F6.1 for seguir (P23).
- A igreja do piloto é a PIB (P14); a confirmação da igreja, do controlador e do encarregado é feita em F6.3.T8.
- Story points (Fibonacci) e horas são sugestões a validar no refinamento. A duração da sprint e a capacidade do time não estão registradas (P6).
- Os testes usam vídeo público com download permitido. Vídeo real do piloto só entra depois de F6.3, de F6.4 e, se acionado, de F6.5, e só em F7.7.
- Dedução não verificada no projeto: o Supabase Auth guarda as contas da equipe e do pastor, com e-mail, no schema de autenticação, fora das tabelas do produto. São dados pessoais da equipe e do pastor e entram no inventário do RIPD (F6.3).
- F7 passou a ter 9 PBIs, dois acima do limite de 2 a 7 filhos por nível (taskflow.md §2), porque F7.2 foi dividido, a operação dos 4 cultos entrou em F7.7 e a leitura do destino do piloto pela ferramenta de rotulagem entrou em F7.9. A alternativa é levar a operação, a rotulagem e a consolidação (F7.7 e F7.9) para uma Feature própria; a decisão fica para o refinamento.
- Revisão não aplicada: F7.2.T8 (acrescentar F7.2.T7 às dependências) — a task saiu de F7.2. A árvore já põe em F5.6 'Aplicar o lint também aos textos fixos da interface', e F7.2, F7.3, F7.6 e F7.8 põem seus textos no arquivo que essa verificação lê. O diretório do painel e o arquivo de textos são criados em F5.6.T1 e a verificação em F5.6.T5 (feature_F5_v3.json), e F7.2.T5 confere que o projeto do piloto usa esse diretório.
- O padrão para os vídeos do piloto é apagá-los do destino ao fim do job concluído de F7.5, para manter a promessa do README (README.pt-BR.md:16-17) e de docs/onprem.md:63. Pela regra de F6.2 (RN08 e F6.2.T1), o vídeo de um culto com rotulagem prevista no plano de F6.6 fica no destino até o fim da rotulagem, dentro do prazo máximo do ADR. Esse prazo maior só vale com o README atualizado com aprovação, porque o aviso à congregação (F6.4) se apoia nessas promessas.
- A comparação dos indicadores de qualidade com os limites de F6.6 acontece na leitura, no banco, porque o vídeo é apagado ao fim do job e reprocessar um culto é pago (P7).
- Revisões com partes fora de F7 (task de confirmação do plano da Vercel antes de F5.6.T2, dependências de F6.2.T1 e F6.2.T2 nessa task, inventário e modelo de segredos de F2.6, adaptação de F3.3 ao destino do piloto): a parte de F7 foi aplicada, e a parte das outras Features que ainda falta está em pendencias_sincronizar, porque esta entrega altera só F7.
- Os IDs F1.5.T1, F2.4.T4, F2.6.T4, F2.6.T6, F6.2.T1 a F6.2.T4 e F6.3.T1 vêm das revisões e do detalhamento das outras Features; a árvore (arvore_v1.json) não tem tasks. F5.4.T3, F5.6.T1 a F5.6.T6, F5.7.T1, F5.7.T2 e F5.8.T1 foram conferidos em feature_F5_v3.json.
- Revisão aplicada com ajuste (Supabase local no CI): a revisão cita F5.6.T3 para os testes de política da Fase 0; no detalhamento de F5, as políticas e os testes pgTAP rodados por 'supabase test db' estão em F5.6.T4 e F5.7.T1.
- Dedução não verificada: o job disparado pelo webhook reexecuta a especificação do Job de origem, com a mesma imagem e os mesmos segredos. A docstring de create_webhook diz só 'ID of the source Job to trigger' (huggingface_hub/hf_api.py:11262-11263). F7.5.T4 confere no primeiro disparo de teste, sem imprimir o valor de nenhum segredo.
- F7.9 foi criado em vez de estender F7.1 porque o usuário é outro (rotulador, não a equipe de mídia) e porque F3.3 não prevê a leitura do destino do piloto (feature_det_F3.json). A execução da rotulagem dos 4 cultos fica em F7.7 (T9 e T10), junto com a operação dos cultos.
- Dedução: o fim da rotulagem de cada culto precisa ficar num registro que a varredura de F7.4.T4 leia para apagar o vídeo. O local é decidido em F7.4.T1, junto com o destino e a retenção dos rótulos do piloto do ADR de F6.2.

### Pendências para sincronizar
- Area Path (Time), Iteration Path (Sprint), Responsável, Prioridade e Valor de negócio numérico no Azure DevOps
- Vínculo da Feature F7 ao Epic pai e dos PBIs F7.1 a F7.9 à Feature
- Tags do projeto no Azure DevOps
- PBI novo F7.8 e novo escopo de F7.7 no índice de PBIs e na árvore
- F5.6 (ou F2.4): task que confirme o plano e os termos de uso da Vercel antes de F5.6.T2, com F5.6.T2 dependendo dela; D8 de F2.4.T4 hoje só registra a pendência (feature_det_F2.json) e F5.6 não tem essa task (feature_det_F5.json)
- F6.2.T1 e F6.2.T2: passar a depender da confirmação do plano da Vercel antes de F5.6.T2 (retenção dos logs de runtime); F6.3.T1 já depende de F5.6
- F2.6.T4: subir no CI o Supabase local com as migrações, aproveitando a configuração de F1.5.T1; os testes pgTAP de F5.6.T4 e F5.7.T1 rodam nesse job, e F7.2.T4 só acrescenta o mecanismo de perfil e a seed do piloto
- F2.6 e F2.6.T6: acrescentar ao modelo de segredos o caso sem quem lance (Job de origem do webhook de F7.5.T4 e Job agendado de F7.4.T4), com os segredos guardados na especificação do Job, e registrar no inventário o id do Job e a rotação por recriação
- F2.6 relido: retirar 'até F7.2, do Space de F5.6' do destino da chave de serviço
- F5.7 e F5.8: F7.3.T4 estende F5.8.T1 e F5.7.T2, e F7.2.T6 reaproveita F5.6.T6 e F5.8.T1; mudanças nessas tasks afetam F7.2 e F7.3
- F6.2.T3 e F6.2.T4 (mudanças no agregado e nos logs): entram na imagem de release do piloto de F7.7.T1
- F2.4.T4: os passos de D7 não citam hoje a decisão sobre o vínculo entre conta e papel nem o alcance da regra 6 sobre as contas da equipe, que F5.6.T3, F7.2 e F7.8 leem de D7 (feature_det_F2.json; feature_det_F5.json)
- F6.2: confirmação ou ajuste de D7 sobre a regra 6 para as contas da equipe e do pastor, e decisão sobre o campo de comentário de insight_feedback
- F6.3: incluir a Vercel como operadora, com a região das funções e a transferência internacional
- Nome do encarregado de dados (DPO)
- Confirmação da igreja do piloto e do controlador (F6.3.T8) e nome da pessoa da equipe de mídia que envia os vídeos
- Quem ocupa o perfil revisor
- Aprovação de custo dos jobs do piloto: testes, processamento dos 4 cultos, disparos curtos gerados por apagamento, varredura agendada, Job de origem e Job agendado recriados na troca de digest (F7.7.T1) e extração da consolidação
- PBI novo F7.9 e tasks novas F7.7.T9 e F7.7.T10 no índice de PBIs e na árvore; F6.6.T2 passa a citar F7.7.T9, F7.7.T10 e F7.9 como o item de F7 que executa a rotulagem
- F3.3: registrar que F7.9 estende a ferramenta para ler o destino do piloto e gravar no destino dos rótulos do piloto
- README.pt-BR.md:16-17: atualização aprovada da promessa de não guardar cópia do vídeo, se o ADR de F6.2 mantiver o vídeo até o fim da rotulagem, antes do aviso de F6.4
- F2.6.T6: incluir no inventário o token do Space de rotulagem para o piloto (F7.9.T2)

## Preview — PBI F7.1 (novo) · Receber o vídeo de cada culto do piloto, enviado pela equipe de mídia, num destino privado do HF separado do corpus

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Receber o vídeo de cada culto do piloto, enviado pela equipe de mídia, num destino privado do HF separado do corpus |
| Tipo | Product Backlog Item |
| Pai | F7 |
| Tags | Fase 1; piloto; HF; privacidade |
| Estimativa | 5 pts (sugestão); tasks: 17 h |
| Dependências | F2.4 (namespace e acesso da equipe de mídia no ADR 0002), F2.6 (tokens de escopo mínimo e inventário de credenciais), F2.2 (tamanho de /dev/shm medido, para o limite de tamanho), F2.6.T1 e F2.8 (repositório de resultados criado em F2.6.T1 e usado por F2.8, para o teste de escopo da credencial), F6.3 (RIPD: operador HF e retenção dos vídeos; igreja, controlador e encarregado confirmados em F6.3.T8) |
| Substitui | nenhum |

#### Descrição

Como integrante da equipe de mídia da igreja do piloto  
Quero enviar a gravação de cada culto a um destino privado no Hugging Face, seguindo um procedimento escrito, sem acesso ao dataset do corpus e sem passar pela Vercel  
Para que o culto seja processado no HF Jobs e saia desse destino ao fim do processamento, ou depois da rotulagem prevista no plano de F6.6, sem alterar as revisões e tags do corpus e dos rótulos

**Contexto:** O único dataset do namespace ds-fabiopinheiro é o privado reacao-poc-corpus, com um único branch (main) e sem tags (HfApi.list_repo_refs), e o namespace não tem bucket (HfApi.list_datasets e list_buckets, 2026-09-23; P27). F3.5 vai criar tags para o corpus e para os rótulos. super_squash_history é irreversível e não se aplica a tags (huggingface_hub/hf_api.py:4415-4460). Arquivos removidos continuam no histórico de refs de pull request (https://huggingface.co/docs/hub/storage-limits#deleting-pull-request-refs). Storage Buckets não têm versionamento, e o apagamento neles é imediato e permanente (https://huggingface.co/docs/hub/storage-buckets#deleting-files). create_bucket sem 'private' cria bucket público, salvo se o padrão da organização for privado (hf_api.py:13825-13827), e a escolha da região 'us' ou 'eu' exige plano Team ou superior (hf_api.py:13834-13836). Um bucket aceita envio por 'hf buckets cp' ou arrastando o arquivo na página do bucket (https://huggingface.co/docs/hub/storage-buckets). Um repositório de conta pessoal só pode ser alterado pelo dono (https://huggingface.co/docs/hub/repositories-settings). Um token de membro de organização lê e escreve nos recursos dela conforme o papel na organização (https://huggingface.co/docs/hub/security-tokens), e resource groups, que restringem o acesso por recurso, só existem no Enterprise Hub (hf_api.py:13828-13830). A documentação recomenda tokens fine-grained restritos a recursos específicos (https://huggingface.co/docs/hub/security-tokens#best-practices). Na operação prevista, a gravação do OBS é copiada pela equipe de Produção (docs/onprem.md:61), e o sistema não guarda cópia do mp4 (docs/onprem.md:63). O README promete que o sistema nunca guarda uma cópia do vídeo (README.pt-BR.md:16-17). Pela dedução da P19, uma hora de vídeo ocupa cerca de 2,3 GB.

**Regras de negócio:**
- RN01 – O destino é privado e diferente do dataset do corpus e dos rótulos. É um Storage Bucket ou um repositório de dataset próprio do piloto, no namespace do ADR de F2.4, e a escolha e a região são registradas neste PBI.
- RN02 – O envio não passa pela Vercel nem por serviço fora do Hugging Face (P3 revisada).
- RN03 – A credencial de envio escreve só no destino do piloto. Ela não lê nem escreve no dataset do corpus e não escreve no repositório de resultados de F2.8 nem no bucket jobs-artifacts.
- RN04 – O nome do arquivo segue o identificador de culto por data e hora já usado em docs/onprem.md:47 (ex.: 2026-09-06-19h) e não contém nome de pessoa.
- RN05 – Vídeo real de culto só é enviado depois de F6.3, de F6.4 e, se acionado, de F6.5. Antes disso, só vídeo público de teste.
- RN06 – O procedimento diz o que a equipe de mídia faz com a gravação do OBS na igreja depois do envio, conforme F6.2 e F6.3.
- RN07 – O limite de tamanho por arquivo é definido neste PBI a partir do /dev/shm medido em F2.2 (P19).
- RN08 – Se o destino for repositório de dataset, o Dataset Viewer fica desligado com 'viewer: false' (https://huggingface.co/docs/hub/datasets-viewer-configure).
- RN09 – O vídeo fica no destino só até o fim do job concluído de F7.5, que o apaga, ou, se o plano de F6.6 prevê rotulagem do culto, até o fim registrado da rotulagem, dentro do prazo máximo do ADR de F6.2 (F6.2 RN08; README.pt-BR.md:16-17; docs/onprem.md:63). O prazo maior só vale com o README atualizado com aprovação.

**Fora de escopo:**
- Formulário de envio no painel web na Vercel ou em Space
- Disparo do processamento (F7.5)
- Apagamento do vídeo ao fim do processamento (F7.5) e depois da rotulagem ou por prazo (F7.4)
- Envio de vídeo real de culto antes de F6.3 e F6.4
- Cópia do vídeo em máquina da equipe de desenvolvimento
- Leitura do vídeo pela ferramenta de rotulagem (F7.9)

#### Critérios de aceite

- O destino do piloto existe, é privado e é diferente do dataset do corpus: um acesso sem credencial recebe acesso negado ou 'não encontrado', e nenhum arquivo do piloto aparece no dataset do corpus.
- Com a credencial da equipe de mídia e seguindo o procedimento escrito, um vídeo público de teste é enviado e aparece no destino com o nome no padrão definido.
- Com a mesma credencial, uma tentativa de ler ou de escrever no dataset do corpus é recusada.
- Com a mesma credencial, uma tentativa de escrever no repositório de resultados de F2.8 e, se ele existir, no bucket jobs-artifacts é recusada.
- Uma conta sem a credencial ou o papel de envio não consegue gravar no destino, e a tentativa é recusada.
- Nenhum passo do procedimento envia o vídeo à Vercel.
- O procedimento está no repositório, aprovado por Fabio e pelo encarregado de dados, e diz quem envia, com qual credencial, o padrão de nome, o limite de tamanho, quando o envio pode começar, que o vídeo é apagado do destino ao fim do processamento ou depois da rotulagem prevista no plano de F6.6 e o destino da gravação do OBS depois do envio.
- As refs e as tags do dataset do corpus estão registradas, com a data, antes do primeiro envio.
- Depois do teste, o vídeo público de teste não existe mais no destino.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F7.1.T1 | MLOps | Decidir e registrar o tipo de destino, o escopo da credencial e a região dos vídeos do piloto | 5 | F2.4, F2.2 |
| F7.1.T2 | DevOps | Criar o destino privado e a credencial de envio de escopo mínimo | 4 | F7.1.T1, F2.6 |
| F7.1.T3 | Governança e Privacidade | Redigir o procedimento de envio da equipe de mídia | 4 | F7.1.T1, F6.3, F6.3.T8 (igreja, controlador e encarregado confirmados e instrumento assinado), F6.6 (rotulagem prevista por culto) |
| F7.1.T4 | QA | Testar o envio de ponta a ponta com vídeo público e registrar as refs do corpus antes do primeiro envio | 4 | F7.1.T2, F7.1.T3 |

<details><summary>F7.1.T1 · [MLOps] Decidir e registrar o tipo de destino, o escopo da credencial e a região dos vídeos do piloto</summary>

**Objetivo:** Deixar registrada a escolha entre Storage Bucket privado e repositório de dataset privado do piloto, com o escopo possível da credencial, a região, o padrão de nome, o limite de tamanho e as consequências para F2.5, F7.4 e F7.5.

**Passos previstos:**
1. Ler https://huggingface.co/docs/hub/storage-buckets, https://huggingface.co/docs/hub/webhooks#buckets, https://huggingface.co/docs/hub/storage-limits#deleting-pull-request-refs e https://huggingface.co/docs/hub/security-tokens.
2. Verificar se um token fine-grained pode ficar restrito a um bucket ou a um repositório de dataset e usar a resposta como critério da escolha do destino.
3. Se só o papel de escrita numa organização servir, exigir uma organização que contenha apenas o destino do piloto, porque o papel vale para os recursos da organização e resource groups só existem no Enterprise Hub (hf_api.py:13828-13830).
4. Comparar as duas opções quanto ao versionamento, ao apagamento (imediato no bucket; commit mais squash irreversível no repositório, com arquivos que continuam em refs de PR), à leitura pelo job (processar_culto.py:24 só trata hf://datasets/) e ao evento de webhook (updatedFiles com 'add' e 'delete', ou updatedRefs).
5. Registrar a região do destino para o RIPD de F6.3. Num bucket, escolher entre 'us' e 'eu' exige plano Team ou superior (hf_api.py:13834-13836); sem ele, registrar a região padrão informada pelo Hub.
6. Definir o padrão de nome pelo identificador de culto de docs/onprem.md:47 e o limite de tamanho a partir do /dev/shm medido em F2.2.
7. Registrar a decisão como adendo ao ADR 0002, com as URLs consultadas.

**Definição de pronto:** O adendo ao ADR 0002 está no repositório com a escolha do destino, o escopo da credencial, a região, o padrão de nome, o limite de tamanho e as fontes, e Fabio o revisou.

**Dependências:** F2.4, F2.2

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F7.1.T2 · [DevOps] Criar o destino privado e a credencial de envio de escopo mínimo</summary>

**Objetivo:** Deixar prontos o destino privado do piloto e uma credencial da equipe de mídia que escreve só nele.

**Passos previstos:**
1. Criar o destino no namespace do ADR com a visibilidade privada passada explicitamente, porque o bucket nasce público sem 'private' (hf_api.py:13825-13827). Se for repositório de dataset, publicar o card com 'viewer: false'.
2. Criar a credencial da equipe de mídia com o escopo decidido em F7.1.T1: token fine-grained restrito ao destino, ou papel de escrita numa organização que contém só o destino.
3. Confirmar que a credencial não tem acesso ao dataset do corpus, ao repositório de resultados de F2.8 nem ao bucket jobs-artifacts.
4. Registrar a credencial no inventário de F2.6 com nome, escopo, dono e validade, sem o valor.
5. Entregar a credencial pelo canal combinado com Fabio.

**Definição de pronto:** O destino existe e é privado, um acesso sem credencial é recusado, e o inventário de F2.6 lista a credencial com o escopo.

**Dependências:** F7.1.T1, F2.6

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F7.1.T3 · [Governança e Privacidade] Redigir o procedimento de envio da equipe de mídia</summary>

**Objetivo:** Ter um procedimento escrito e aprovado que a equipe de mídia segue a cada culto.

**Passos previstos:**
1. Descrever quem envia, com qual credencial e como: 'hf buckets cp', 'hf upload' ou a página do destino no Hub.
2. Incluir o padrão de nome, o limite de tamanho e o que fazer se o arquivo passar do limite.
3. Declarar que o envio de culto real só começa depois de F6.3, de F6.4 e, se acionado, de F6.5.
4. Declarar que o vídeo é apagado do destino ao fim do processamento concluído (F7.5), ou, se o plano de F6.6 prevê rotulagem do culto, depois do fim registrado da rotulagem, e que a varredura de F7.4 o apaga no prazo máximo se o processamento falhar ou a rotulagem não terminar.
5. Definir, conforme F6.2 e F6.3, o que acontece com a gravação do OBS na igreja depois do envio (docs/onprem.md:61,63).
6. Indicar o contato em caso de falha no envio.
7. Submeter o texto ao encarregado de dados e a Fabio.

**Definição de pronto:** O procedimento está versionado no repositório, com a aprovação de Fabio e do encarregado registrada.

**Dependências:** F7.1.T1, F6.3, F6.3.T8 (igreja, controlador e encarregado confirmados e instrumento assinado), F6.6 (rotulagem prevista por culto)

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F7.1.T4 · [QA] Testar o envio de ponta a ponta com vídeo público e registrar as refs do corpus antes do primeiro envio</summary>

**Objetivo:** Verificar todos os critérios de aceite de F7.1 com um vídeo público e deixar a linha de base do corpus para a comparação de F7.7.

**Passos previstos:**
1. Antes do primeiro envio, registrar as refs e as tags do dataset do corpus (HfApi.list_repo_refs), com a data, e anexá-las ao PBI.
2. Escolher um vídeo público com download permitido, de docs/corpus.csv ou de F5.1.
3. Enviar seguindo o procedimento, com a credencial da equipe de mídia, e confirmar o nome no padrão.
4. Com a mesma credencial, tentar ler e escrever no dataset do corpus e escrever no repositório de resultados e, se existir, no bucket jobs-artifacts; o esperado é recusa.
5. Tentar acessar o destino sem credencial e com uma conta sem papel de envio; o esperado é recusa.
6. Confirmar que nenhum passo usou a Vercel.
7. Remover o vídeo de teste e registrar as evidências sem o valor da credencial.

**Definição de pronto:** As refs e tags do corpus e as evidências de cada critério estão anexadas ao PBI, e todos os critérios passaram.

**Dependências:** F7.1.T2, F7.1.T3

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- feature_F7.json (árvore v1), PBI F7.1
- HfApi.list_datasets, list_spaces, list_buckets e list_repo_refs (2026-09-23)
- huggingface_hub/hf_api.py:4415-4460 (super_squash_history)
- huggingface_hub/hf_api.py:13825-13836 (create_bucket: visibilidade, resource groups e região)
- https://huggingface.co/docs/hub/storage-buckets
- https://huggingface.co/docs/hub/storage-limits#deleting-pull-request-refs
- https://huggingface.co/docs/hub/security-tokens
- https://huggingface.co/docs/hub/repositories-settings
- https://huggingface.co/docs/hub/datasets-viewer-configure
- docs/onprem.md:47,61,63
- README.pt-BR.md:16-17
- premissas P11, P19, P24, P27, P30 e P3 revisada

#### Premissas
- A disciplina Front end saiu deste PBI. Pela P3 revisada, o envio é feito pela CLI ou pela página do destino no Hub, e não existe interface do projeto para isso.
- Não foi verificado se um token fine-grained pode ficar restrito a um bucket. A verificação é critério da escolha do destino em F7.1.T1.
- Guardar o vídeo no destino depois do processamento contraria a promessa do README (README.pt-BR.md:16-17) e docs/onprem.md:63. Por isso, o padrão é apagar o vídeo ao fim do job concluído de F7.5. A regra de F6.2 (RN08) mantém o vídeo até o fim da rotulagem prevista no plano de F6.6, dentro do prazo máximo, o que exige o README atualizado com aprovação.
- Não se sabe o plano do namespace escolhido no ADR de F2.4, então não se sabe se a região do bucket pode ser escolhida.
- O nome do destino é decisão deste PBI (P24).
- A igreja do piloto é a PIB (P14); a confirmação da igreja, do controlador e do encarregado é feita em F6.3.T8, antes do procedimento de F7.1.T3.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Vínculo com a Feature F7
- Nome e contato da pessoa da equipe de mídia que envia os vídeos
- Canal de entrega da credencial à equipe de mídia

## Preview — PBI F7.2 (novo) · Restringir por perfil pastor e revisor o acesso aos dados do piloto no Supabase e no painel web na Vercel, com Supabase Auth e RLS

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Restringir por perfil pastor e revisor o acesso aos dados do piloto no Supabase e no painel web na Vercel, com Supabase Auth e RLS |
| Tipo | Product Backlog Item |
| Pai | F7 |
| Tags | Fase 1; piloto; Supabase; RLS; Vercel; privacidade |
| Estimativa | 8 pts (sugestão); tasks: 46 h |
| Dependências | F2.6 (projeto Supabase de desenvolvimento com RLS habilitada; job de CI com Supabase local em F2.6.T4, pendência), F2.4.T4 (D7: local do vínculo entre conta e papel, alcance da regra 6 sobre as contas da equipe e tabelas do painel; D8: plano e termos da Vercel como pendência), F5.6 (projeto na Vercel em F5.6.T2; Supabase Auth e papéis em F5.6.T3; políticas do avaliador em F5.6.T4; lint dos textos fixos em F5.6.T5; lista em F5.6.T6), F5.8 (tela do relatório, F5.8.T1), F6.2 (confirmação ou ajuste de D7 de F2.4.T4 sobre o vínculo entre conta e perfil e a regra 6, com migração se mudar), F6.3 (RIPD com a Vercel como operadora, região das funções e transferência internacional), F1.7 (lint ampliado) |
| Substitui | PBI-041, PBI-057 |

#### Descrição

Como encarregado de dados (DPO) do piloto  
Quero que o pastor e o revisor entrem no painel web com a própria conta e que o banco devolva a cada um só o que o perfil dele permite  
Para que o acesso aos resultados do piloto seja imposto pelo banco e não dependa só da lógica da interface

**Contexto:** O schema tem 8 tabelas (supabase/migrations/0001_init.sql:3-18) e não tem RLS, políticas nem papéis. Um comentário manda 'RLS e perfis (pastor, midia, dpo)' para o PBI-041/PBI-057 (0001_init.sql:21). F2.6 habilita RLS sem política de leitura anônima. O pipeline grava com a chave de serviço (reacao/store.py:11-12,24-25). A chave secreta autoriza pelo papel service_role, que tem o atributo bypassrls, e o dono postgres também tem bypassrls (https://supabase.com/docs/guides/database/postgres/row-level-security). A chave publicável tem o prefixo sb_publishable_ e a secreta o prefixo sb_secret_; as chaves legadas anon e service_role são JWT (https://supabase.com/docs/guides/getting-started/api-keys). Se o projeto Supabase for ligado à Vercel pela integração do Marketplace, as variáveis são sincronizadas sozinhas, entre elas POSTGRES_URL, POSTGRES_PRISMA_URL, POSTGRES_URL_NON_POOLING, POSTGRES_PASSWORD, SUPABASE_SECRET_KEY e SUPABASE_JWT_SECRET (https://supabase.com/docs/guides/integrations/vercel-marketplace). Com a integração de branching, o Supabase atualiza sozinho as variáveis do projeto da Vercel (https://supabase.com/docs/guides/deployment/branching/integrations). A documentação de RBAC usa um hook de token de acesso que acrescenta a claim de papel, lida pelas políticas com auth.jwt(), e guarda o papel numa tabela public.user_roles com user_id por conta (https://supabase.com/docs/guides/api/custom-claims-and-role-based-access-control-rbac). O que fica em raw_app_meta_data também chega a auth.jwt(), não pode ser alterado pelo usuário e só aparece na política depois que o token é renovado (row-level-security). Tokens de acesso duram de 5 minutos a 1 hora, com padrão de 1 hora (https://supabase.com/docs/guides/auth/sessions). Variáveis sensíveis da Vercel não podem ser lidas depois de criadas e só existem em production e preview (https://vercel.com/docs/environment-variables/sensitive-environment-variables). As Vercel Functions rodam por padrão em iad1 (Washington, D.C., EUA) em projetos novos (https://vercel.com/docs/functions/configuring-functions/region), e gru1 (São Paulo) está na lista de regiões (https://vercel.com/docs/regions). Times no plano Hobby só podem ter uso pessoal não comercial (https://vercel.com/docs/limits/fair-use-guidelines). O detalhamento de F5 (feature_F5_v3.json) cria na Fase 0 o diretório do painel e o arquivo de textos fixos (F5.6.T1), o projeto na Vercel com só a URL e a chave pública do Supabase (F5.6.T2), o Supabase Auth com cadastro fechado (F5.6.T3), a tabela de execuções liberadas com as políticas do avaliador do gate e testes pgTAP (F5.6.T4), o lint dos textos fixos (F5.6.T5), a lista de execuções liberadas (F5.6.T6) e a tela do relatório (F5.8.T1). O CI atual não tem banco (.github/workflows/ci.yml:1-17), e a documentação do Supabase roda testes de banco no GitHub Actions com 'supabase db start' e 'supabase test db' (https://supabase.com/docs/guides/deployment/ci/testing). Pela revisão, o job de CI com o Supabase local e as migrações passa a F2.6.T4, na Fase 0, e este PBI acrescenta a ele o mecanismo de perfil e a seed do piloto. Pela P3 revisada, o painel lê só agregados, eventos e insights, usa a chave pública, e a chave de serviço fica só nos jobs do HF. Os perfis mídia e DPO ficam em F7.8.

**Regras de negócio:**
- RN01 – Este PBI cobre os perfis pastor e revisor; mídia e DPO ficam em F7.8 (0001_init.sql:21). Uma conta autenticada sem perfil não lê nenhuma linha.
- RN02 – O que cada perfil lê e escreve segue a matriz de acesso aprovada pelo encarregado em F7.2.T1, que cobre os quatro perfis.
- RN03 – Os perfis do painel leem só as tabelas da lista de D7 de F2.4.T4 (window_aggregate, event, insight, a tabela de execuções liberadas de F5.6 e os indicadores de F7.6; moment e service só se a confirmação registrada em D7 os incluir) e gravam só insight_feedback (pastor) e o estado de revisão do insight (revisor, F7.3). Outra tabela entra só como exceção aprovada pelo encarregado e registrada na matriz e em D7. transcript_segment e run_log não têm política de leitura para nenhum perfil do painel (P3 revisada; 0001_init.sql:4,13,18).
- RN04 – O projeto na Vercel tem só as variáveis da lista permitida: a URL do projeto Supabase e a chave publicável. SUPABASE_SECRET_KEY, SUPABASE_SERVICE_ROLE_KEY, SUPABASE_JWT_SECRET, POSTGRES_URL, POSTGRES_URL_NON_POOLING, POSTGRES_PRISMA_URL e POSTGRES_PASSWORD são proibidas no projeto (P3 revisada; https://supabase.com/docs/guides/integrations/vercel-marketplace; https://supabase.com/docs/guides/getting-started/api-keys).
- RN05 – O projeto Supabase não é conectado ao projeto da Vercel pela integração do Marketplace nem pela de branching.
- RN06 – 'Tabelas do Supabase não têm campo por pessoa' (CLAUDE.md regra 6, texto literal). O vínculo entre conta e perfil fica onde D7 de F2.4.T4 decidiu, antes de F5.6, e onde F6.2 confirmar ou ajustar. Se a regra vale para as contas da equipe e do pastor, o perfil fica em raw_app_meta_data do Supabase Auth, lido por auth.jwt() -> 'app_metadata', fora das tabelas do produto, como os papéis de F5.6.T3. Se não valer, a exceção é registrada no CLAUDE.md e tests/test_schema.py é ampliado.
- RN07 – O perfil pastor lê só insights com revisão registrada. F7.3 acrescenta o estado 'aprovado' a essa regra.
- RN08 – Janela marcada como insuficiente (sem quadro com plateia ou com média de rostos mensuráveis por quadro com plateia abaixo de 10) aparece sem percentual em todas as telas (CLAUDE.md regra 3; reacao/aggregate.py:26-31).
- RN09 – Os textos fixos das telas ficam no arquivo de textos de F5.6.T1, lido pela verificação de lint de F5.6.T5 (CLAUDE.md regra 4).
- RN10 – A Vercel não recebe vídeo, quadro, recorte de rosto nem observação por rosto (P3 revisada).
- RN11 – A região das funções do projeto na Vercel é a registrada no RIPD de F6.3.
- RN12 – O CI não guarda chave de serviço do Supabase. O teste de políticas roda só contra o Supabase local, com contas e perfis criados pela seed local.

**Fora de escopo:**
- Perfis e telas de mídia e DPO (F7.8)
- Ação de revisão e estado de aprovação dos insights (F7.3)
- Sinalização de qualidade por culto (F7.6)
- Envio dos vídeos (F7.1)
- Login pelo OAuth do Hugging Face
- Supabase Auth, mecanismo do perfil no token e acesso de Fabio e Filipe ao relatório do culto público da Fase 0 (F5.6 relido)
- Verificação de lint dos textos fixos do painel (F5.6.T5)
- Confirmação do plano e dos termos de uso da Vercel antes de o projeto ser criado na Fase 0 (antes de F5.6.T2; D8 de F2.4.T4 registra a pendência)
- Job de CI com o Supabase local e as migrações (F2.6.T4)

#### Critérios de aceite

- Numa consulta direta à API do banco, fora do painel, com a sessão de uma conta do perfil pastor, nenhum insight sem revisão registrada é retornado, e inserir, alterar ou apagar linhas de window_aggregate, event, insight ou run_log é recusado.
- Sem login, só com a chave publicável, e com a sessão de uma conta autenticada sem perfil, as consultas diretas a todas as tabelas retornam zero linhas ou acesso negado. No painel, a conta sem perfil vê a tela de acesso negado.
- Com a sessão de uma conta pastor ou revisor, uma consulta direta a transcript_segment retorna zero linhas ou acesso negado.
- No CI, contra o Supabase local e sem chave de serviço do Supabase nas secrets do repositório, o teste automatizado de políticas confere cada linha da matriz para pastor e revisor, e tests/test_schema.py passa. Com uma política removida de propósito, o teste falha.
- O pastor entra com a própria conta e vê só as telas do perfil pastor. O endereço direto de uma tela de outro perfil mostra acesso negado.
- Depois de retirado o perfil de uma conta, ela deixa de ler os dados do perfil no prazo de expiração do token configurado no projeto.
- A lista de variáveis do projeto na Vercel, em todos os ambientes, é igual à lista permitida (URL do projeto Supabase e chave publicável), nenhuma variável da lista proibida existe, a página de integrações não mostra o Supabase conectado pelo Marketplace nem pelo branching, e a região das funções é a registrada no RIPD.
- O JavaScript entregue ao navegador não contém o prefixo sb_secret_ nem JWT com role service_role, e os arquivos do deployment de produção não incluem vídeo, imagem de quadro, recorte de rosto nem observação por rosto.
- Uma janela marcada como insuficiente aparece sem percentual nas telas do pastor, inclusive uma janela de teste com n_mensuravel=10 e insuficiente=true.
- Os textos fixos das telas deste PBI estão no arquivo lido pela verificação de lint de F5.6.T5, e a verificação passa.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F7.2.T1 | Governança e Privacidade | Definir com o encarregado a matriz de acesso dos quatro perfis | 5 | F2.4.T4 (D7), F6.2 |
| F7.2.T2 | Governança e Privacidade | Confirmar para o piloto o plano e os termos de uso da Vercel do painel | 3 | F2.4.T4 (D8: plano e termos da Vercel como pendência, com Fabio responsável), F5.6.T2 (projeto do painel criado) |
| F7.2.T3 | Backend | Levar os perfis pastor e revisor ao token e escrever as políticas de RLS desses perfis | 10 | F7.2.T1, F2.6, F2.4.T4 (D7), F5.6.T3, F5.6.T4 |
| F7.2.T4 | DevOps | Acrescentar ao job de Supabase local do CI o mecanismo de perfil do piloto e a seed de teste | 3 | F7.2.T3, F2.6.T4 |
| F7.2.T5 | DevOps | Configurar o Supabase Auth e o projeto na Vercel para o piloto, com contas, variáveis, região e proteção de previews | 5 | F7.2.T1, F7.2.T2, F5.6.T2, F5.6.T3, F6.3 |
| F7.2.T6 | Front end | Implementar a guarda por perfil e a tela de acesso negado e estender ao perfil pastor a lista e o relatório de F5 | 8 | F7.2.T3, F7.2.T5, F5.6.T6, F5.8.T1 |
| F7.2.T7 | QA | Automatizar o teste de políticas e verificar os critérios de F7.2 | 12 | F7.2.T4, F7.2.T5, F7.2.T6 |

<details><summary>F7.2.T1 · [Governança e Privacidade] Definir com o encarregado a matriz de acesso dos quatro perfis</summary>

**Objetivo:** Ter aprovada a matriz perfil × tabela × operação e as telas de cada perfil, que F7.2 aplica a pastor e revisor e F7.8 a mídia e DPO.

**Passos previstos:**
1. Listar as 8 tabelas (0001_init.sql:3-18), a tabela de execuções liberadas de F5.6.T4 e as colunas e tabelas novas de F7.3 e F7.6.
2. Partir da lista de D7 de F2.4.T4: leitura de window_aggregate, event, insight, execuções liberadas de F5.6 e indicadores de F7.6, moment e service conforme a confirmação registrada em D7, e escrita de insight_feedback e do estado de revisão. Registrar cada tabela a mais como exceção, com o motivo, e nenhuma leitura de transcript_segment nem de run_log.
3. Decidir, para cada perfil do piloto, quais tabelas da lista de D7 ele lê; a lista de F5.6.T6 e o cabeçalho do relatório de F5.8.T1 leem a tabela de execuções liberadas.
4. Para pastor, midia, dpo e revisor, marcar leitura, inclusão, alteração e exclusão por tabela.
5. Definir as telas de cada perfil, inclusive o conteúdo das telas de mídia e DPO, e o que a conta sem perfil vê.
6. Definir o método de login, quem recebe cada perfil, como o acesso é revogado e a expiração do token.
7. Registrar onde fica o vínculo entre conta e perfil, conforme D7 de F2.4.T4 e a confirmação ou o ajuste de F6.2 sobre a regra 6.

**Definição de pronto:** A matriz está no repositório, com a aprovação do encarregado e de Fabio registrada.

**Dependências:** F2.4.T4 (D7), F6.2

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F7.2.T2 · [Governança e Privacidade] Confirmar para o piloto o plano e os termos de uso da Vercel do painel</summary>

**Objetivo:** Ter registrado se o plano e os termos da Vercel cobrem o uso do painel com os dados e as contas da igreja do piloto, partindo da pendência de D8 (F2.4.T4) e da confirmação feita antes de F5.6.T2, se houver.

**Passos previstos:**
1. Ler D8 de F2.4.T4 e o registro de confirmação do plano e dos termos feito antes da criação do projeto em F5.6.T2. Se esse registro não existir, confirmar o plano agora pela conta do time e registrar que o projeto foi usado na Fase 0 sem a confirmação.
2. Conferir se esse registro cobre o uso no piloto: dados de uma igreja, conta do pastor da igreja do piloto e contas dos perfis revisor, mídia e DPO. Times Hobby só podem ter uso pessoal não comercial (https://vercel.com/docs/limits/fair-use-guidelines).
3. Registrar a retenção dos logs de runtime do plano (https://vercel.com/docs/logs/runtime) para a tabela de prazos de F7.4.T1.
4. Registrar a decisão para o piloto: seguir no plano atual, mudar de plano ou mudar de host.

**Definição de pronto:** O registro está no repositório com o plano, as URLs lidas e a decisão para o piloto, aprovado por Fabio.

**Dependências:** F2.4.T4 (D8: plano e termos da Vercel como pendência, com Fabio responsável), F5.6.T2 (projeto do painel criado)

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F7.2.T3 · [Backend] Levar os perfis pastor e revisor ao token e escrever as políticas de RLS desses perfis</summary>

**Objetivo:** Fazer o banco impor a matriz aprovada para pastor, revisor, conta sem perfil e acesso anônimo.

**Passos previstos:**
1. Guardar o perfil no local decidido em D7 de F2.4.T4 e confirmado ou ajustado por F6.2: em raw_app_meta_data do Supabase Auth, lido por auth.jwt() -> 'app_metadata', ou, se a decisão registrar a exceção à regra 6, numa tabela de vínculo com o hook de token de acesso da documentação de RBAC e o acesso de anon e authenticated revogado.
2. Estender o papel de avaliador do gate gravado em F5.6.T3 e as políticas de F5.6.T4 com os perfis pastor e revisor, no mesmo mecanismo.
3. Escrever as políticas por tabela e operação conforme a matriz, lendo o perfil com auth.jwt(). Na tabela insight, o perfil pastor lê só as linhas com revisado_em preenchido.
4. Não criar política para o papel anon nem política de leitura de transcript_segment para perfis do painel.
5. Escrever a seed local com uma conta de teste por perfil e uma sem perfil, sem dados reais.
6. Confirmar que os jobs continuam gravando com a chave de serviço.
7. Na migração nova, pôr um comentário que troca a referência 'PBI-041/PBI-057' de supabase/migrations/0001_init.sql:21 por F7.2 e F7.8, sem editar a migração já aplicada.

**Definição de pronto:** As migrações estão aplicadas no Supabase local e no projeto de desenvolvimento, o token de uma conta de teste contém o perfil, e ruff e pytest passam.

**Dependências:** F7.2.T1, F2.6, F2.4.T4 (D7), F5.6.T3, F5.6.T4

**Estimativa sugerida:** 10 h (sugestão; validar com o time)

</details>

<details><summary>F7.2.T4 · [DevOps] Acrescentar ao job de Supabase local do CI o mecanismo de perfil do piloto e a seed de teste</summary>

**Objetivo:** Dar aos testes de banco de F7.2, F7.3, F7.4, F7.6 e F7.8 as contas e os perfis do piloto no Supabase local do CI, sem chave de serviço do projeto.

**Passos previstos:**
1. Partir do job de CI com o Supabase local e as migrações criado em F2.6.T4 (https://supabase.com/docs/guides/deployment/ci/testing).
2. Aplicar nesse job as migrações e a seed de F7.2.T3 e, se D7 de F2.4.T4 ou o ajuste de F6.2 escolher a tabela de vínculo, configurar o hook no Supabase local.
3. Usar só as chaves que o Supabase local gera (https://supabase.com/docs/guides/getting-started/api-keys) e não cadastrar chave de serviço do projeto de desenvolvimento nas secrets do repositório.
4. Registrar no PBI que o CI não guarda chave de serviço do Supabase.

**Definição de pronto:** O job de F2.6.T4 roda em push e pull request com as migrações e a seed do piloto, as contas de teste de pastor, revisor e sem perfil existem no Supabase local, e a lista de secrets do repositório no GitHub não tem chave de serviço do Supabase.

**Dependências:** F7.2.T3, F2.6.T4

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F7.2.T5 · [DevOps] Configurar o Supabase Auth e o projeto na Vercel para o piloto, com contas, variáveis, região e proteção de previews</summary>

**Objetivo:** Deixar o login do piloto funcionando no domínio do painel, com o projeto na Vercel tendo só as variáveis da lista permitida e a região do RIPD.

**Passos previstos:**
1. Ativar no Supabase Auth o método de login definido em F7.2.T1, manter o cadastro fechado de F5.6.T3, convidar as contas de pastor e revisor definidas em F7.2.T1 e cadastrar as URLs de redirecionamento do domínio de produção e, se usados, dos previews.
2. Conferir que o projeto de F5.6.T2 tem só a URL do Supabase e a chave publicável nos ambientes necessários (https://vercel.com/docs/environment-variables/manage-across-environments).
3. Não conectar o projeto Supabase pela integração do Marketplace nem pela de branching, e conferir a página de integrações do projeto.
4. Listar as variáveis de cada ambiente com 'vercel env ls' (https://vercel.com/docs/cli/env) e comparar com a lista permitida.
5. Definir a região das funções conforme o RIPD de F6.3 e registrá-la (https://vercel.com/docs/functions/configuring-functions/region).
6. Decidir e registrar a proteção dos previews (https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/vercel-authentication).
7. Conferir que o projeto publica o diretório do painel de F5.6.T1.

**Definição de pronto:** A lista de nomes das variáveis de cada ambiente está anexada ao PBI e é igual à permitida, a região está registrada, e uma conta de teste faz login no domínio de produção.

**Dependências:** F7.2.T1, F7.2.T2, F5.6.T2, F5.6.T3, F6.3

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F7.2.T6 · [Front end] Implementar a guarda por perfil e a tela de acesso negado e estender ao perfil pastor a lista e o relatório de F5</summary>

**Objetivo:** Fazer o painel mostrar a cada conta só as rotas do perfil dela e dar ao pastor a lista de cultos e o relatório, reaproveitando F5.6.T6 e F5.8.T1.

**Passos previstos:**
1. Ler o perfil do token de acesso da sessão; o hook altera só o token, não a resposta de autenticação (https://supabase.com/docs/guides/api/custom-claims-and-role-based-access-control-rbac).
2. Mostrar a tela de acesso negado à conta sem perfil e proteger as rotas de cada perfil, inclusive por endereço direto.
3. Tela do pastor: reaproveitar a lista de F5.6.T6 e a tela do relatório de F5.8.T1, com janelas agregadas, eventos com o momento e insights liberados. A lista lê a tabela de execuções liberadas de F5.6 só se a matriz aprovar a exceção; senão, window_aggregate.culto. Ler service ou moment só se a matriz aprovar a exceção.
4. Mostrar sem percentual a janela com insuficiente=true.
5. Pôr os textos fixos no arquivo de textos de F5.6.T1, lido pela verificação de lint de F5.6.T5.
6. Garantir que nenhuma chamada use chave de serviço.

**Definição de pronto:** Num preview com as contas de teste, o pastor vê só as telas dele, o revisor só as rotas dele e a conta sem perfil vê acesso negado, e a verificação de lint passa.

**Dependências:** F7.2.T3, F7.2.T5, F5.6.T6, F5.8.T1

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F7.2.T7 · [QA] Automatizar o teste de políticas e verificar os critérios de F7.2</summary>

**Objetivo:** Ter um teste no CI que prova, direto na API do banco, que pastor e revisor só leem e escrevem o que a matriz permite, e conferir os demais critérios no painel e na Vercel.

**Passos previstos:**
1. Para cada linha da matriz de pastor e revisor, consultar e escrever pela API REST com a chave publicável e a sessão da conta de teste, comparando com o esperado. Incluir o caso anônimo, a conta sem perfil, transcript_segment e as escritas do pastor.
2. Incluir o caso de revogação: retirar o perfil e conferir que a leitura deixa de funcionar depois da expiração do token, reduzida no Supabase local.
3. Rodar o teste no job de Supabase local do CI (F2.6.T4, com a seed de F7.2.T4) e confirmar que ele falha com uma política removida de propósito.
4. Entrar no painel com cada conta de teste e conferir telas, rotas por endereço direto e uma janela com n_mensuravel=10 e insuficiente=true sem percentual.
5. Conferir com 'vercel env ls' a lista de variáveis de cada ambiente, a página de integrações e a região das funções.
6. Procurar sb_secret_ e JWT com role service_role no JavaScript entregue ao navegador, listar os arquivos do deployment de produção (https://vercel.com/docs/rest-api/deployments/list-deployment-files) e conferir tipos e extensões.
7. Rodar tests/test_schema.py e a verificação de lint de F5.6.T5.

**Definição de pronto:** O teste de políticas está versionado, passa no CI e falha com uma política removida de propósito, e o checklist de todos os critérios está anexado ao PBI com as evidências.

**Dependências:** F7.2.T4, F7.2.T5, F7.2.T6

**Estimativa sugerida:** 12 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- feature_F7.json (árvore v1), PBI F7.2
- feature_F5_v3.json (F5.6.T1 a F5.6.T6 e F5.8.T1)
- supabase/migrations/0001_init.sql:3-21
- reacao/store.py:11-12,24-25
- reacao/aggregate.py:26-31
- .github/workflows/ci.yml:1-17
- https://supabase.com/docs/guides/database/postgres/row-level-security
- https://supabase.com/docs/guides/getting-started/api-keys
- https://supabase.com/docs/guides/api/custom-claims-and-role-based-access-control-rbac
- https://supabase.com/docs/guides/auth/sessions
- https://supabase.com/docs/guides/integrations/vercel-marketplace
- https://supabase.com/docs/guides/deployment/branching/integrations
- https://supabase.com/docs/guides/deployment/ci/testing
- https://vercel.com/docs/environment-variables/manage-across-environments
- https://vercel.com/docs/environment-variables/sensitive-environment-variables
- https://vercel.com/docs/cli/env
- https://vercel.com/docs/functions/configuring-functions/region
- https://vercel.com/docs/regions
- https://vercel.com/docs/limits/fair-use-guidelines
- https://vercel.com/docs/logs/runtime
- https://vercel.com/docs/rest-api/deployments/list-deployment-files
- https://vercel.com/docs/deployment-protection/methods-to-protect-deployments/vercel-authentication
- Vercel list_teams, list_projects e get_team (2026-09-23)
- taskflow.md §1 e §2
- premissas P12, P17, P23 e P3 revisada

#### Verificação INVEST: pontos que falharam
- Small: com login, políticas, CI com banco, configuração da Vercel e telas do pastor, soma 46 h sugeridas e pode não caber numa sprint (P6).
- Independente: depende de D7 e D8 de F2.4.T4 e da confirmação do plano da Vercel antes de F5.6.T2, que ainda não tem task em F5.6.

#### Premissas
- O perfil revisor foi acrescentado aos três perfis da migração. Com a chave pública e o RLS, a escrita do estado de revisão em F7.3 precisa de um perfil com essa permissão. Quem ocupa o perfil está pendente.
- F7.2 foi dividido: este PBI cobre pastor e revisor, e F7.8 cobre mídia e DPO (taskflow.md §1: mais de um usuário-alvo e critérios acima de ~10 sobre assuntos diferentes; §2: mais de 7 filhos).
- O detalhamento de F5 (feature_F5_v3.json) entrega o projeto na Vercel, o Supabase Auth, as políticas do avaliador do gate, a verificação de lint dos textos fixos, a lista de execuções e a tela do relatório (F5.6.T1 a F5.6.T6 e F5.8.T1). F7.2 estende essa base com os perfis pastor e revisor.
- Revisão aplicada em parte: F7.2.T2 ficou só com a confirmação para o uso com dados da igreja do piloto. A confirmação antes de o projeto ser criado na Fase 0 não virou task em F5.6 (feature_det_F5.json); D8 de F2.4.T4 só registra a pendência. Por isso F7.2.T2 depende de D8 e, se não achar confirmação anterior, faz a confirmação e registra que o projeto foi usado sem ela.
- Revisão aplicada: o job de CI com o Supabase local e as migrações foi para F2.6.T4 (pendência), porque as políticas de F5.6.T4 e F5.7.T1 já têm testes pgTAP na Fase 0. F7.2.T4 ficou só com o mecanismo de perfil do piloto e a seed.
- O método de login do Supabase Auth (link por e-mail, senha ou provedor OAuth) é decisão de F7.2.T1 com o encarregado. Nenhuma fonte o define para o piloto.
- O uso de Vercel Authentication nos previews é decisão de F7.2.T5. O controle de acesso aos dados fica no Supabase Auth com RLS, porque o pastor não é membro do time da Vercel.
- A lista de cultos do pastor sai da tabela de execuções liberadas de F5.6, que está na lista de D7 de F2.4.T4, ou de window_aggregate.culto. service e moment só são lidos se a confirmação do usuário registrada em D7 os incluir.
- PBI-041 e PBI-057 viraram um único PBI (P17), agora dividido em F7.2 e F7.8.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Vínculo com a Feature F7
- Quem recebe os perfis pastor e revisor
- Task em F5.6 (ou em F2.4) que confirme o plano e os termos da Vercel antes de F5.6.T2
- Domínio de produção do painel
- F2.6.T4: o título atual ('Habilitar RLS nas 8 tabelas por migração, com teste') não cita o job de CI com o Supabase local de que F7.2.T4 depende

## Preview — PBI F7.3 (novo) · Liberar ao perfil pastor no painel web na Vercel só os insights aprovados na revisão humana

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Liberar ao perfil pastor no painel web na Vercel só os insights aprovados na revisão humana |
| Tipo | Product Backlog Item |
| Pai | F7 |
| Tags | Fase 1; piloto; revisão humana; Vercel; Supabase |
| Estimativa | 5 pts (sugestão); tasks: 30 h |
| Dependências | F7.2 (perfis revisor e pastor, políticas, seed no CI com Supabase local, guarda de rotas e teste de políticas), F6.2 (valor de revisado_por e do avaliador; campo de comentário), F5.6 (arquivo de textos fixos em F5.6.T1 e verificação de lint em F5.6.T5), F5.7 (políticas de nota do avaliador do gate em F5.7.T1 e formulário de nota por insight em F5.7.T2), F5.8 (tela do relatório, F5.8.T1), F1.7 (lint ampliado) |
| Substitui | nenhum |

#### Descrição

Como pastor da igreja do piloto  
Quero ver no painel web só os insights que o revisor aprovou, com a data da revisão, e dar uma nota a cada um  
Para ler um relatório conferido por uma pessoa e devolver a avaliação que o plano de medição de F6.6 usa

**Contexto:** A tabela insight tem texto, trecho, minuto, sinais, revisado_por e revisado_em na mesma linha, e nenhum código preenche revisado_por e revisado_em (supabase/migrations/0001_init.sql:16). A operação prevista inclui 'relatório disponível para revisão' antes do pastor (docs/onprem.md:62). O schema não tem campo de estado da revisão, então a rejeição não tem onde ficar registrada. A tabela insight_feedback aceita nota de 1 a 5, avaliador e comentário, sem restrição de unicidade (0001_init.sql:17). Até a decisão de F6.2, insight_feedback.avaliador guarda um código de papel, e não o nome (P12). O texto de cada insight passa pelo lint só na geração (reacao/insights.py:50,54). Uma política que permite UPDATE dá acesso a todas as colunas da linha; para restringir colunas, a documentação do Supabase usa privilégio por coluna, que exige nomear as colunas nas consultas do papel restrito (https://supabase.com/docs/guides/database/postgres/column-level-security). A política de F7.2 esconde do perfil pastor os insights sem revisão registrada. O detalhamento de F5 (feature_F5_v3.json) tem a tela do relatório de uma execução liberada, com momentos, janelas e insights (F5.8.T1), o formulário de nota e comentário por insight, que grava com a sessão do usuário (F5.7.T2), e as políticas de insight_feedback para o avaliador do gate (F5.7.T1). F5.7 produz o critério 4 do gate e roda antes de F6.1, e F7 só começa depois da decisão de F6.1 (P23). Pela P3 revisada, a revisão, a liberação e as notas ficam no painel web na Vercel.

**Regras de negócio:**
- RN01 – Cada insight tem um estado de revisão: pendente (inicial), aprovado ou rejeitado.
- RN02 – Só o perfil revisor muda o estado, e só a coluna de estado e a categoria do motivo. O banco preenche revisado_em com o horário do servidor e revisado_por a partir do perfil no token, sem aceitar valor enviado pelo cliente.
- RN03 – O perfil pastor lê só insights aprovados. O banco impõe essa regra por RLS.
- RN04 – O relatório liberado mostra a data da revisão de cada insight.
- RN05 – O pastor dá nota de 1 a 5 (0001_init.sql:17) só em insight aprovado. O banco preenche o avaliador a partir do perfil no token.
- RN06 – Cada avaliador tem no máximo uma nota por insight.
- RN07 – Texto, trecho, minuto e sinais de um insight não mudam depois da geração, porque o lint só roda na geração (reacao/insights.py:50,54; CLAUDE.md regra 4).
- RN08 – Os textos fixos das telas de revisão e de nota ficam no arquivo de textos de F5.6.T1, lido pela verificação de lint de F5.6.T5 (CLAUDE.md regra 4).
- RN09 – O campo de comentário da nota só existe se F6.2 o mantiver.

**Fora de escopo:**
- Edição do texto do insight pelo revisor
- Reimplementar a tela do relatório de F5.8.T1 ou o formulário de nota de F5.7.T2
- Alerta de qualidade por culto (F7.6), que só ocupa um espaço reservado na tela de revisão
- Cálculo do critério 4 da Fase 0 (F5.7)
- Exibição do vídeo ao revisor
- Revisão e liberação dos 4 cultos reais (F7.7)

#### Critérios de aceite

- Um insight pendente ou rejeitado não aparece para o perfil pastor no painel nem é retornado numa consulta direta à API do banco com a sessão do perfil pastor.
- Um insight aprovado aparece para o pastor com minuto, momento, trecho citado, sinais e a data da revisão.
- Ao aprovar ou rejeitar um insight, o banco registra revisado_por a partir do perfil no token e revisado_em com o horário do servidor. Valores enviados pelo cliente para essas colunas não são gravados.
- Uma conta fora do perfil revisor não vê a ação de revisão no painel, e uma tentativa dela de mudar o estado pela API do banco é recusada.
- Uma tentativa do perfil revisor de alterar texto, trecho, minuto ou sinais de um insight pela API do banco é recusada.
- A nota de 1 a 5 dada pelo pastor fica gravada ligada ao insight, com o avaliador preenchido pelo banco a partir do token, independente do valor enviado.
- Uma nota fora de 1 a 5 é recusada, e o painel mostra uma mensagem de erro sem gravar nada.
- Uma tentativa de dar nota a um insight que não está aprovado é recusada pelo banco.
- Uma segunda nota do mesmo avaliador ao mesmo insight não gera uma segunda linha em insight_feedback.
- Depois da migração, tests/test_schema.py passa, e o teste de políticas ampliado passa no CI contra o Supabase local.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F7.3.T1 | Governança e Privacidade | Definir o roteiro da revisão, quem revisa e a regra da segunda nota | 3 | F6.2 |
| F7.3.T2 | Backend | Registrar o estado de revisão do insight, restringir as colunas escritas e ajustar as políticas | 8 | F7.2.T3, F7.2.T4, F7.3.T1, F5.7.T1 |
| F7.3.T3 | Front end | Implementar a fila de revisão por culto | 8 | F7.3.T2, F7.2.T6, F5.8.T1 |
| F7.3.T4 | Front end | Estender ao perfil pastor a tela do relatório de F5.8.T1 e o formulário de nota de F5.7.T2, com só insights aprovados e a data da revisão | 5 | F7.3.T2, F7.2.T6, F5.8.T1, F5.7.T2, F6.2 |
| F7.3.T5 | QA | Verificar a liberação, a rejeição, a restrição de colunas e a nota | 6 | F7.3.T3, F7.3.T4 |

<details><summary>F7.3.T1 · [Governança e Privacidade] Definir o roteiro da revisão, quem revisa e a regra da segunda nota</summary>

**Objetivo:** Ter por escrito o que o revisor confere antes de aprovar, quem ocupa o perfil revisor e o que acontece com a segunda nota.

**Passos previstos:**
1. Listar o que o revisor confere: linguagem controlada, trecho citado coerente com o momento, nenhuma referência a pessoa ou setor e cobertura da janela.
2. Definir o registro do motivo de rejeição por categoria, sem texto livre sobre pessoas.
3. Definir quem ocupa o perfil revisor e propor a F6.2 o valor gravado em revisado_por.
4. Decidir com Fabio se a segunda nota do mesmo avaliador ao mesmo insight substitui a anterior ou é recusada.
5. Submeter o texto ao encarregado.

**Definição de pronto:** O roteiro está versionado no repositório, com a aprovação do encarregado registrada.

**Dependências:** F6.2

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F7.3.T2 · [Backend] Registrar o estado de revisão do insight, restringir as colunas escritas e ajustar as políticas</summary>

**Objetivo:** Fazer o banco guardar o estado de revisão e impor quem revisa, quais colunas mudam, o que o pastor lê e onde ele pode dar nota.

**Passos previstos:**
1. Escrever a migração com o estado de revisão (pendente, aprovado, rejeitado) e, se F7.3.T1 definir, a categoria do motivo.
2. Limitar a escrita do perfil revisor à coluna de estado e à categoria, por privilégio por coluna ou por função no banco (https://supabase.com/docs/guides/database/postgres/column-level-security).
3. Preencher no banco revisado_em com o horário do servidor e revisado_por e insight_feedback.avaliador a partir do perfil no token, ignorando valores enviados pelo cliente.
4. Mudar a política de leitura do pastor para só insights aprovados e permitir ao pastor inserir nota só em insight aprovado, sem alterar as políticas de F5.7.T1 do avaliador do gate.
5. Criar a restrição de uma nota por insight e por avaliador, com o comportamento decidido em F7.3.T1, e manter o comentário só se F6.2 o mantiver.
6. Rodar tests/test_schema.py e ruff.

**Definição de pronto:** A migração está aplicada no Supabase local e no projeto de desenvolvimento, e tests/test_schema.py e ruff passam.

**Dependências:** F7.2.T3, F7.2.T4, F7.3.T1, F5.7.T1

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F7.3.T3 · [Front end] Implementar a fila de revisão por culto</summary>

**Objetivo:** Dar ao revisor uma tela para aprovar ou rejeitar cada insight de um culto.

**Passos previstos:**
1. Listar os insights pendentes do culto com minuto, momento, trecho citado e sinais, reaproveitando a listagem de insights de F5.8.T1.
2. Oferecer as ações aprovar e rejeitar, com confirmação e categoria do motivo na rejeição.
3. Enviar só o estado e a categoria; revisado_por e revisado_em vêm do banco.
4. Mostrar o estado depois da ação e a mensagem de erro se a gravação falhar.
5. Reservar na tela o espaço do alerta de qualidade de F7.6.
6. Pôr os textos fixos no arquivo de textos de F5.6.T1, lido pela verificação de lint de F5.6.T5.

**Definição de pronto:** Num preview, uma conta revisor aprova e rejeita insights de um culto de teste, e a verificação de lint passa.

**Dependências:** F7.3.T2, F7.2.T6, F5.8.T1

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F7.3.T4 · [Front end] Estender ao perfil pastor a tela do relatório de F5.8.T1 e o formulário de nota de F5.7.T2, com só insights aprovados e a data da revisão</summary>

**Objetivo:** Entregar ao pastor o relatório só com insights aprovados, com a data da revisão e a nota, a partir das telas da Fase 0.

**Passos previstos:**
1. Partir da tela do relatório de F5.8.T1 e mostrar ao perfil pastor os insights que o banco devolve, que pela RLS de F7.3.T2 são só os aprovados, sem filtro no cliente no lugar da RLS.
2. Acrescentar a data da revisão em cada insight aprovado.
3. Reaproveitar o formulário de nota de F5.7.T2 para o perfil pastor, em insight aprovado, com o avaliador preenchido pelo banco a partir do token.
4. Mostrar o campo de comentário só se F6.2 o mantiver.
5. Mostrar mensagem de erro quando a gravação da nota for recusada.
6. Pôr os textos fixos novos no arquivo de textos de F5.6.T1, lido pela verificação de lint de F5.6.T5.

**Definição de pronto:** Num preview, uma conta pastor vê só insights aprovados, com a data da revisão, e grava uma nota pelo formulário de F5.7.T2, e a verificação de lint passa.

**Dependências:** F7.3.T2, F7.2.T6, F5.8.T1, F5.7.T2, F6.2

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F7.3.T5 · [QA] Verificar a liberação, a rejeição, a restrição de colunas e a nota</summary>

**Objetivo:** Conferir todos os critérios de aceite de F7.3.

**Passos previstos:**
1. Ampliar o teste de políticas de F7.2.T7 com: revisor alterando texto, trecho, minuto ou sinais; valores forjados de revisado_em, revisado_por e avaliador; nota em insight pendente; segunda nota; conta fora do revisor mudando o estado.
2. Com um culto de teste, deixar insights pendentes, aprovados e rejeitados e conferir o que o pastor vê no painel e numa consulta direta à API do banco.
3. Tentar gravar nota 0 e nota 6 pelo painel e conferir a mensagem de erro.
4. Rodar tests/test_schema.py.

**Definição de pronto:** O teste ampliado passa no CI, e o checklist dos critérios está anexado ao PBI com as evidências, com todos passando.

**Dependências:** F7.3.T3, F7.3.T4

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- feature_F7.json (árvore v1), PBI F7.3
- feature_F5_v3.json (F5.7.T1, F5.7.T2 e F5.8.T1)
- supabase/migrations/0001_init.sql:16-17
- docs/onprem.md:62
- tests/test_schema.py:5
- reacao/insights.py:50,54
- https://supabase.com/docs/guides/database/postgres/column-level-security
- https://supabase.com/docs/guides/database/postgres/row-level-security
- premissas P12, P23 e P3 revisada

#### Verificação INVEST: pontos que falharam
- Independente: depende das políticas, do CI e do perfil revisor de F7.2 e das telas de F5.7 e F5.8. Se F7.2 e F7.3 entrarem na mesma sprint, F7.3 só começa depois de F7.2.T4.

#### Premissas
- O revisor não edita o texto do insight: aprova ou rejeita. Editar exigiria rodar o lint de novo e rastrear a versão. É uma proposta a confirmar com Fabio.
- Proposta a confirmar em F6.2: revisado_por guarda o código de papel lido do token, como a P12 prevê para insight_feedback.avaliador. A P12 trata só de avaliador.
- Se a segunda nota do mesmo avaliador ao mesmo insight substitui a anterior ou é recusada é decisão de F7.3.T1 com Fabio. Nas duas opções fica uma nota por insight e por avaliador.
- O roteiro do que o revisor confere é escrito neste PBI, com o encarregado. Nenhuma fonte o define.
- Revisão aplicada: F5.7 roda sempre antes do gate, porque produz o critério 4, e F7 só começa depois de F6.1 (P23). Por isso a dependência de F5.7 é incondicional, e F7.3.T4 estende F5.8.T1 e F5.7.T2 em vez de reimplementá-los.
- Proposta: as políticas de nota de F5.7.T1 valem para o papel de avaliador do gate e não mudam; F7.3.T2 cria políticas próprias para o perfil pastor, em insight aprovado.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Vínculo com a Feature F7
- Quem ocupa o perfil revisor
- Decisão de F6.2 sobre revisado_por, avaliador e comentário

## Preview — PBI F7.4 (novo) · Aplicar a retenção de agregados, relatórios e vídeos do piloto com job agendado e teste de datas vencidas

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Aplicar a retenção de agregados, relatórios e vídeos do piloto com job agendado e teste de datas vencidas |
| Tipo | Product Backlog Item |
| Pai | F7 |
| Tags | Fase 1; piloto; retenção; LGPD; Supabase; HF |
| Estimativa | 5 pts (sugestão); tasks: 32 h |
| Dependências | F6.2 (regra de apagamento dos vídeos e das tabelas sem prazo), F6.3 (retenção no RIPD), F7.1 (destino dos vídeos), F2.6 (projeto Supabase de desenvolvimento, tokens e inventário de credenciais em F2.6.T6; job de CI com Supabase local em F2.6.T4), F2.5 (registro de execução do job de varredura), F7.2 (confirmação do plano da Vercel para o piloto em T2; mecanismo de perfil e seed no CI em T4), F7.5.T1 (se a data de referência for service.data), F6.6 (rotulagem prevista por culto e prazo da rotulagem) |
| Substitui | nenhum |

#### Descrição

Como encarregado de dados (DPO) do piloto  
Quero que agregados, relatórios, insights e os vídeos do piloto que ficaram no destino sejam apagados automaticamente nos prazos definidos  
Para cumprir a retenção registrada no RIPD sem depender de ação manual

**Contexto:** A retenção existe só como comentário: agregados por 12 meses e relatórios e insights por 24 meses, 'por job agendado' (supabase/migrations/0001_init.sql:20). O schema não tem tabela de relatório (0001_init.sql:3-18). Não há job, função nem pg_cron no repositório, e o namespace não tem Job agendado ('hf jobs scheduled ps -a', 2026-09-23). As tabelas transcript_segment, moment, event e insight não têm coluna de data (0001_init.sql:13-16). A retenção por prazo precisa de uma data de referência, que pode ser uma coluna nova ou service.data (0001_init.sql:4), gravada por F7.5.T1. O prazo das demais tabelas sai de F6.2 e F6.3. O vídeo é apagado do destino ao fim do job concluído (F7.5), salvo se o plano de F6.6 prevê rotulagem do culto; pela regra de F6.2 (RN08 e F6.2.T1), esse vídeo fica até o fim da rotulagem, dentro do prazo máximo do ADR. Este PBI apaga os vídeos com rotulagem concluída e, por prazo, os que ficaram no destino porque o job falhou, não rodou ou a rotulagem não terminou. O ADR de F6.2 decide o destino dos rótulos do piloto, e F6.2.T8 os exclui do corpus. No Supabase, pg_cron agenda funções SQL, e os exemplos da documentação usam horário GMT (https://supabase.com/docs/guides/cron/quickstart). No HF, Jobs agendados usam CRON, e a documentação não informa o fuso (https://huggingface.co/docs/hub/jobs-schedule; P22). Um Job agendado nasce ativo, salvo com suspend=True (huggingface_hub/hf_api.py:13042-13043), e o estado traz next_job_run_at (huggingface_hub/_jobs_api.py:368). Os segredos de um Job agendado ficam na especificação dele (hf_api.py:13015,13051; _jobs_api.py:331) e são criptografados no servidor (https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets). Na biblioteca huggingface_hub 1.32.0, os métodos de Job agendado são criar, listar, inspecionar, apagar, suspender, retomar, disparar e alterar labels (hf_api.py:13006-13422); trocar a imagem ou um segredo exige apagar e recriar o Job. O Job agendado roda sem quem o lance, então os segredos não seguem a entrega por quem lança de F2.6. Num bucket, o apagamento é imediato e permanente (https://huggingface.co/docs/hub/storage-buckets#deleting-files). Num repositório, é preciso squash, que é irreversível e não se aplica a tags (hf_api.py:4415-4460), e arquivos removidos continuam em refs de pull request (https://huggingface.co/docs/hub/storage-limits#deleting-pull-request-refs). Os logs de runtime da Vercel ficam guardados por prazo que depende do plano (https://vercel.com/docs/logs/runtime); o plano é pendência em D8 de F2.4.T4 e é confirmado para o piloto em F7.2.T2.

**Regras de negócio:**
- RN01 – Prazos: agregados por 12 meses; relatórios e insights por 24 meses (0001_init.sql:20). Como o schema não tem tabela de relatório, F7.4.T1 diz quais tabelas compõem o relatório. As demais tabelas e o prazo máximo dos vídeos que ficaram no destino seguem F6.2 e F6.3.
- RN02 – O apagamento de vídeo atua só no destino de F7.1. O dataset do corpus, suas revisões e suas tags não mudam.
- RN03 – Cada execução persiste quantas linhas ou arquivos apagou por tabela e por destino, sem o conteúdo apagado: as do banco em tabela própria ou no histórico do agendador (F7.4.T2), as dos vídeos no registro de F2.5.
- RN04 – O fuso de cada agendamento fica registrado.
- RN05 – A retenção fica ativa antes do primeiro culto do piloto.
- RN06 – Execução agendada no HF Jobs gera custo e exige aprovação prévia (P7), registrada antes de o agendamento ficar ativo.
- RN07 – A retenção dos logs de runtime da Vercel entra na tabela de prazos, conforme o plano confirmado para o piloto em F7.2.T2.
- RN08 – O Job agendado guarda na especificação só o token do HF que lista e apaga no destino do piloto e o token de escrita no repositório de resultados de F2.8, sem a chave de serviço do Supabase. Os dois ficam no inventário de F2.6.T6 com o id do Job agendado, sem o valor, e são trocados recriando o Job.
- RN09 – Um vídeo marcado 'aguardando rotulagem' só é apagado depois do fim da rotulagem registrado no local de F7.4.T1, ou no prazo máximo do ADR de F6.2, o que vier primeiro (F6.2 RN08).
- RN10 – O destino e o prazo de retenção dos rótulos do piloto seguem o ADR de F6.2 e entram na tabela de prazos; os rótulos do piloto não entram no dataset do corpus (F6.2.T8).

**Fora de escopo:**
- Retenção do dataset do corpus e dos rótulos (F3.1 e F3.5)
- Apagamento da gravação do OBS na igreja, que segue o procedimento de F7.1
- Retenção dos logs dos Jobs no HF
- Apagamento do vídeo ao fim do processamento concluído (F7.5)
- Troca do digest do Job agendado para a imagem de release do piloto (F7.7.T1)

#### Critérios de aceite

- Num banco de teste com linhas datadas antes e depois do prazo em cada tabela coberta, uma execução da retenção apaga só as vencidas, e a contagem das demais continua igual.
- O teste inclui uma linha exatamente no limite do prazo, e o resultado segue a regra de fronteira escrita no documento de prazos.
- Depois da varredura, um vídeo público de teste com prazo vencido ou com fim de rotulagem registrado no destino do piloto não existe mais, e a busca pelo arquivo retorna 'não encontrado'; um vídeo de teste marcado 'aguardando rotulagem' dentro do prazo continua no destino.
- Depois da varredura, as tags e a revisão do dataset do corpus resolvem para os mesmos commits de antes.
- Executada por um papel do banco sem permissão de apagar, a função de retenção termina com erro, a falha fica registrada e nenhuma linha é apagada.
- Executado com um token inválido, o job de varredura termina com erro, a falha aparece no registro de F2.5 e nenhum arquivo é apagado.
- O registro de cada execução mostra a contagem apagada por tabela, no local definido em F7.4.T2, e por destino, no registro de F2.5.
- O agendamento, o fuso e o prazo de cada tabela, do destino de vídeo, dos rótulos do piloto e dos logs de runtime da Vercel, e o local do registro de fim da rotulagem, estão no repositório.
- A retenção está agendada e ativa no projeto de desenvolvimento antes da data do primeiro culto do piloto.
- Nenhum Job agendado do HF fica ativo antes de a aprovação de custo estar registrada, e o inventário de F2.6.T6 lista cada segredo guardado no Job agendado, com escopo, dono, validade, id do Job e procedimento de rotação, sem o valor.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F7.4.T1 | Governança e Privacidade | Consolidar os prazos de retenção por tabela, por destino, para os rótulos do piloto e para os logs da Vercel | 5 | F6.2, F6.3, F2.4.T4 (D8), F7.2.T2, F6.6 (rotulagem prevista por culto) |
| F7.4.T2 | Backend | Criar a data de referência, a função de retenção com registro das contagens e o agendamento no banco | 8 | F7.4.T1, F2.6, F7.5.T1 |
| F7.4.T3 | QA | Automatizar o teste de datas vencidas no banco | 6 | F7.4.T2, F7.2.T4 |
| F7.4.T4 | DevOps | Agendar a varredura dos vídeos do destino do piloto com rotulagem concluída ou prazo vencido, com os segredos do Job agendado definidos e registrados | 8 | F7.4.T1, F7.1.T2, F2.5, F2.6.T6, Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F7.4.T5 | QA | Verificar a varredura de vídeo, a integridade do corpus, o erro com token inválido e os segredos registrados | 5 | F7.4.T3, F7.4.T4, Aprovação de Fabio (P7), com flavor, duração e custo previstos |

<details><summary>F7.4.T1 · [Governança e Privacidade] Consolidar os prazos de retenção por tabela, por destino, para os rótulos do piloto e para os logs da Vercel</summary>

**Objetivo:** Ter num só documento o prazo, a data de referência e a regra de fronteira de cada tabela, do destino de vídeo, dos rótulos do piloto e dos logs de runtime da Vercel, com o local onde fica registrado o fim da rotulagem de cada culto.

**Passos previstos:**
1. Registrar os prazos de 0001_init.sql:20 para agregados, relatórios e insights e listar, com o encarregado, quais tabelas compõem o 'relatório', com a fonte.
2. Trazer de F6.2 e F6.3 os prazos de transcript_segment, moment, event, run_log, insight_feedback, service e o prazo máximo dos vídeos que ficaram no destino.
3. Definir a data de referência de cada tabela e do destino de vídeo e a regra de fronteira (o dia do vencimento entra ou não).
4. Registrar a retenção dos logs de runtime da Vercel do plano confirmado para o piloto em F7.2.T2 (https://vercel.com/docs/logs/runtime).
5. Registrar o destino e a retenção dos rótulos do piloto decididos no ADR de F6.2, que F6.2.T8 exclui do corpus, e a condição de apagamento do vídeo depois da rotulagem prevista no plano de F6.6, com o prazo máximo.
6. Definir onde fica o registro 'aguardando rotulagem' e o do fim da rotulagem de cada culto, lido por F7.5.T2 e pela varredura de F7.4.T4 e escrito por F7.7.T10, sem nome de pessoa.
7. Submeter o documento ao encarregado.

**Definição de pronto:** A tabela de prazos está versionada no repositório, com a aprovação do encarregado registrada.

**Dependências:** F6.2, F6.3, F2.4.T4 (D8), F7.2.T2, F6.6 (rotulagem prevista por culto)

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F7.4.T2 · [Backend] Criar a data de referência, a função de retenção com registro das contagens e o agendamento no banco</summary>

**Objetivo:** Ter no banco uma função agendada que apaga por prazo e persiste a contagem por tabela.

**Passos previstos:**
1. Escrever a migração com a data de referência nas tabelas sem data (0001_init.sql:13-16), ou a junção com service.data gravada por F7.5.T1, conforme F7.4.T1.
2. Escrever a função que apaga as linhas vencidas por tabela e persiste a contagem por tabela, sem o conteúdo apagado, numa tabela própria ou no histórico do agendador, e registrar onde.
3. Executar a função com um papel que só tem as permissões de apagar necessárias e fazer a falha de permissão aparecer no registro.
4. Agendar a função com pg_cron (https://supabase.com/docs/guides/cron/quickstart), ou registrar por que o agendador será outro, e registrar o fuso.

**Definição de pronto:** A migração e o agendamento estão aplicados no projeto de desenvolvimento, o agendamento aparece na lista de jobs do agendador, e o local do registro das contagens e o fuso estão no repositório.

**Dependências:** F7.4.T1, F2.6, F7.5.T1

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F7.4.T3 · [QA] Automatizar o teste de datas vencidas no banco</summary>

**Objetivo:** Ter no CI um teste que prova que a retenção apaga só o que venceu e não apaga nada quando falta permissão.

**Passos previstos:**
1. Usar o job de Supabase local do CI (F2.6.T4), com as migrações e a seed de F7.2.T4.
2. Inserir por tabela linhas antes, no limite e depois do prazo.
3. Executar a função e comparar as contagens apagadas e as registradas com o esperado.
4. Executar com um papel sem permissão de apagar e conferir o erro, a falha registrada e nenhuma linha apagada.

**Definição de pronto:** O teste está versionado e passa no CI. Alterado o prazo de uma tabela sem atualizar o teste, ele falha.

**Dependências:** F7.4.T2, F7.2.T4

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F7.4.T4 · [DevOps] Agendar a varredura dos vídeos do destino do piloto com rotulagem concluída ou prazo vencido, com os segredos do Job agendado definidos e registrados</summary>

**Objetivo:** Fazer os vídeos que ficaram no destino deixarem de existir depois do fim registrado da rotulagem ou no prazo máximo de F7.4.T1, com os segredos guardados no Job agendado de escopo mínimo e registrados no inventário.

**Passos previstos:**
1. Escrever o script de varredura, versionado, que lista os arquivos do destino, apaga os que têm o fim da rotulagem registrado no local de F7.4.T1 e os que têm a data de referência vencida, e grava no registro de F2.5 a contagem por destino e motivo e as falhas, sem conteúdo.
2. Publicar o script numa imagem com digest por tag de pré-release, pelo processo de F2.2. F7.7.T1 troca depois o Job para a imagem de release do piloto.
3. Se o destino for bucket, usar a remoção de arquivo do bucket. Se for repositório, prever o squash e a remoção de refs de PR (https://huggingface.co/docs/hub/storage-limits#deleting-pull-request-refs).
4. Definir os segredos guardados na especificação do Job agendado (hf_api.py:13015,13051): o token do HF que lista e apaga só no destino e o token de escrita só no repositório de resultados de F2.8, sem a chave de serviço do Supabase.
5. Definir a rotação: a biblioteca só altera labels de um Job agendado (hf_api.py:13378), então trocar um token exige apagar e recriar o Job (hf_api.py:13246,13006).
6. Pedir a aprovação de custo antes de criar o agendamento ativo (P7). Para conferir o fuso antes da aprovação, criar o Job suspenso (suspend=True; hf_api.py:13042-13043) e registrar se next_job_run_at aparece.
7. Ativar depois da aprovação, registrar o fuso e registrar no inventário de F2.6.T6 cada segredo guardado, com o id do Job agendado, o escopo, o dono, a validade e a rotação, sem o valor.

**Definição de pronto:** O Job agendado está ativo pela imagem com o script de varredura, com a aprovação de custo registrada antes da ativação, o fuso está documentado, e o inventário de F2.6.T6 lista os segredos guardados nele, com o id do Job e a rotação.

**Dependências:** F7.4.T1, F7.1.T2, F2.5, F2.6.T6, Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F7.4.T5 · [QA] Verificar a varredura de vídeo, a integridade do corpus, o erro com token inválido e os segredos registrados</summary>

**Objetivo:** Conferir os critérios de F7.4 ligados ao destino de vídeo, ao dataset do corpus e aos segredos do Job agendado.

**Passos previstos:**
1. Registrar as refs e as tags do dataset do corpus antes do teste.
2. Pôr no destino do piloto um vídeo público de teste com prazo vencido e disparar a varredura com 'hf jobs scheduled trigger', dentro da aprovação de custo de F7.4.T4.
3. Pôr no destino um vídeo público de teste marcado 'aguardando rotulagem' dentro do prazo e outro com o fim da rotulagem registrado; conferir que a varredura apaga só o segundo.
4. Confirmar que o arquivo não existe mais e que as refs e as tags do corpus são as mesmas.
5. Executar uma cópia do job com token inválido e conferir a falha no registro de F2.5 e que nada foi apagado.
6. Conferir a contagem por destino no registro de F2.5.
7. Conferir no inventário de F2.6.T6 os segredos guardados no Job agendado, com o id do Job e a rotação, sem o valor.

**Definição de pronto:** As evidências de cada critério estão anexadas ao PBI, e todos passaram.

**Dependências:** F7.4.T3, F7.4.T4, Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- feature_F7.json (árvore v1), PBI F7.4
- supabase/migrations/0001_init.sql:3-20
- huggingface_hub/hf_api.py:13006-13422 (create_scheduled_job, suspend, secrets e métodos de Job agendado)
- huggingface_hub/_jobs_api.py:331,368 (JobSpec.secrets e next_job_run_at)
- https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets
- https://supabase.com/docs/guides/cron/quickstart
- https://huggingface.co/docs/hub/jobs-schedule
- https://huggingface.co/docs/hub/storage-buckets#deleting-files
- https://huggingface.co/docs/hub/storage-limits#deleting-pull-request-refs
- https://vercel.com/docs/logs/runtime
- huggingface_hub/hf_api.py:4415-4460
- README.pt-BR.md:16-17
- docs/onprem.md:63
- premissas P7 e P22

#### Premissas
- Os dados do Supabase podem ser apagados por pg_cron ou por Job agendado no HF, e a escolha fica registrada em F7.4.T2. Os vídeos que ficaram no destino são apagados por Job agendado no HF (F7.4.T4).
- A opção de apagar o vídeo num passo no fim do job de F7.5 saiu deste PBI. Ela é o padrão e fica em F7.5.T2, sem dependência circular entre F7.4 e F7.5.
- Para conferir o fuso do CRON do HF pelo next_job_run_at, o Job agendado precisa existir. Ele é criado depois da aprovação de custo, ou criado suspenso (suspend=True). Não foi verificado se next_job_run_at aparece num Job suspenso.
- No banco, a função agendada por pg_cron não usa credencial externa. O caso de erro testado é o de um papel sem permissão de apagar.
- Um vídeo que fica no destino depois de um job com falha contraria a promessa do README enquanto estiver lá (README.pt-BR.md:16-17). O prazo máximo da varredura vem de F6.2 e F6.3 e precisa ser compatível com essa promessa, ou vir com a atualização aprovada do README.
- O vídeo de teste é público e não contém pessoas da congregação.
- Revisão aplicada: o Job agendado roda sem quem o lance, então F7.4.T4 define os segredos guardados na especificação dele e os registra no inventário de F2.6.T6. O script de varredura entra numa imagem de pré-release em F7.4.T4, e F7.7.T1 troca o Job para a imagem de release do piloto.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Vínculo com a Feature F7
- Prazos finais de F6.2 e F6.3
- Aprovação de custo do Job agendado de varredura
- Registro dos segredos do Job agendado no inventário de F2.6.T6

## Preview — PBI F7.5 (novo) · Processar cada culto do piloto a partir da chegada do vídeo ao destino do piloto, com checagem dos pré-requisitos da Fase 1

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Processar cada culto do piloto a partir da chegada do vídeo ao destino do piloto, com checagem dos pré-requisitos da Fase 1 |
| Tipo | Product Backlog Item |
| Pai | F7 |
| Tags | Fase 1; piloto; HF Jobs; MLOps |
| Estimativa | 8 pts (sugestão); tasks: 40 h |
| Dependências | F2.2 (imagem com digest e timeout confirmado), F2.4 (modo de execução e namespace), F2.5 (registro de execução e de falhas; gravação idempotente), F2.6 (inventário de credenciais em F2.6.T6), F6.3 (RIPD, para o registro de vigência), F6.4 (aviso, para o registro de vigência), F6.5 (se acionado), F7.1 (destino, padrão de nome, limite de tamanho e procedimento de envio), F7.3 (fila de revisão), F1.1 (guarda e limpeza de /dev/shm), F6.6 (rotulagem prevista por culto) |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro, operador do piloto  
Quero que a chegada do vídeo de um culto ao destino do piloto dispare o job de processamento pela imagem com digest, ou ter o disparo manual documentado  
Para que cada culto gere agregados, eventos, insights e registro de execução para revisão no painel web sem outro passo manual além do envio, que nenhum culto seja processado sem RIPD e aviso em vigor na data do culto e que o vídeo saia do destino ao fim do processamento ou fique marcado para a rotulagem prevista

**Contexto:** Webhooks do Hub podem disparar um Job: create_webhook recebe job_id, watched e domains (huggingface_hub/hf_api.py:11244-11275; https://huggingface.co/docs/hub/jobs-webhooks). O Job recebe WEBHOOK_PAYLOAD, WEBHOOK_REPO_ID, WEBHOOK_REPO_TYPE e WEBHOOK_SECRET (hf_api.py:11262-11264), e a documentação lista WEBHOOK_REPO_TYPE só como model, dataset ou space (https://huggingface.co/docs/hub/jobs-webhooks). update_webhook não aceita job_id (hf_api.py:11378-11386); para apontar o webhook para outro Job de origem, é preciso criar outro webhook e desativar ou apagar o anterior (hf_api.py:11520,11573). Os segredos de um Job são criptografados no servidor (https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets; huggingface_hub/_jobs_api.py:211-212). F2.6 entrega os segredos aos jobs a partir de quem lança (revisão; arvore_v1.json, F2.6); no disparo por webhook não há quem lance. A documentação de webhooks descreve eventos de bucket com updatedFiles: o evento dispara em arquivos adicionados e apagados, sobrescrever é reportado como 'add', e cada entrada traz path, action e, no 'add', size (https://huggingface.co/docs/hub/webhooks#buckets). resolve_video só trata caminhos hf://datasets/ e baixa para /dev/shm/reacao-in (processar_culto.py:23-31). processar_culto.py recebe --culto, mas não recebe a data do culto (processar_culto.py:34-46), e nenhum código grava a tabela service (reacao/store.py:28-44; 0001_init.sql:4). 'hf jobs run' com imagem não copia arquivo local para o bucket jobs-artifacts (P27). 'hf jobs run --dry-run' mostra a configuração resolvida sem submeter o Job (huggingface_hub 1.32.0, cli/jobs.py:470-476,712-713; https://huggingface.co/docs/hub/jobs-configuration#define-the-launch-config-in-the-script). processar_culto.py:103-107 monta o registro com cobertura, eventos, insights e rejeitados pelo lint; run_log não tem a coluna insights_rejeitados_pelo_lint (0001_init.sql:18), e F1.5 corrige isso (P20), via F2.5. O registro de jobs que falharam é o de F2.5, que este PBI só consulta. O timeout padrão de um Job é 30 minutos, o máximo não está documentado (https://huggingface.co/docs/hub/jobs-configuration#timeout; P19), e F2.2 confirma o valor aceito. Labels e --name servem para filtrar jobs (https://huggingface.co/docs/hub/jobs-manage). O job imprime o run_log e, com --stdout, janelas, eventos e insights (processar_culto.py:108-115). O padrão de publicar imagem por tag com o código de uma etapa aparece em F5.3.T3 e F5.4.T3 (feature_F5_v3.json).

**Regras de negócio:**
- RN01 – O job roda com 'hf jobs run <imagem>@<digest>' e comando explícito (F2.4), com o motor escolhido no ADR 0001.
- RN02 – Antes de processar, o job confere que o RIPD, o aviso e, se acionada, a forma de F6.5 estão em vigor na data do culto. Se algum faltar, o job termina sem gravar resultados e registra o motivo.
- RN03 – O vídeo é lido do destino de F7.1 por caminho do Hub para /dev/shm, nunca por caminho local passado ao lançamento (CLAUDE.md regra 1; F1.1; P27).
- RN04 – Cada job leva labels de culto e de motor.
- RN05 – Falhas ficam só no registro de F2.5.
- RN06 – Os segredos são passados só pelo nome no lançamento, e a chave de serviço do Supabase fica só nos jobs (F2.6; P3 revisada). No disparo por webhook, os valores ficam guardados, criptografados, no Job de origem; cada um tem escopo mínimo e fica no inventário de F2.6.T6 com o id do Job de origem, sem o valor, e a rotação é feita recriando o Job de origem e o webhook.
- RN07 – Reprocessar o mesmo vídeo não duplica os resultados do culto (gravação idempotente de F2.5).
- RN08 – A execução paga exige aprovação prévia do dono da conta, inclusive nos jobs de teste e nos disparos gerados por apagamento de arquivo (P7).
- RN09 – O id e a data do culto saem do nome do arquivo no padrão de F7.1 (docs/onprem.md:47). Arquivo fora do padrão encerra o job sem gravar resultados, com o motivo no registro de F2.5.
- RN10 – Depois de a checagem passar, o job grava service.culto e service.data (0001_init.sql:4).
- RN11 – Evento de apagamento (action 'delete') encerra o job antes de baixar vídeo ou carregar modelos, com o motivo registrado.
- RN12 – Vídeo acima do limite de tamanho de F7.1 encerra o job antes do download, com o motivo no registro de F2.5.
- RN13 – Ao fim do job concluído, o vídeo é apagado do destino e o apagamento fica registrado em F2.5, salvo se o plano de F6.6 prevê rotulagem do culto; nesse caso o vídeo fica marcado 'aguardando rotulagem' e a varredura de F7.4 o apaga depois do fim da rotulagem ou no prazo máximo (F6.2 RN08; F7.1 RN09; README.pt-BR.md:16-17). Job com falha não apaga o vídeo.
- RN14 – Os testes deste PBI usam a imagem de pré-release de F7.5.T6; os cultos reais usam a imagem de release de F7.7.T1.

**Fora de escopo:**
- Envio do vídeo (F7.1)
- Varredura por prazo dos vídeos que ficaram no destino (F7.4)
- Escolha do motor e do flavor (F4.6 e F5.4)
- Processamento de mais de 4 cultos ou de outra igreja
- Operação dos 4 cultos reais (F7.7)
- Imagem de release do piloto e troca do digest do Job de origem antes do primeiro culto (F7.7.T1)

#### Critérios de aceite

- Com os pré-requisitos marcados como em vigor num ambiente de teste, o envio de um vídeo público ao destino do piloto gera um job pela imagem de F7.5.T6, com labels de culto e de motor, ou o disparo manual documentado gera esse job.
- Ao fim desse job, o registro de execução do culto existe, service tem o culto e a data, os insights aparecem como pendentes na fila de revisão do painel, e o vídeo não existe mais no destino ou, se o plano de F6.6 prevê rotulagem do culto de teste, continua no destino com a marca 'aguardando rotulagem'.
- Com um pré-requisito ausente ou com vigência posterior à data do culto, ou com nome de arquivo fora do padrão, o job termina sem gravar janelas, eventos nem insights, e o motivo aparece no registro de F2.5.
- Um job que falha com um arquivo de vídeo corrompido aparece no registro de F2.5 com a etapa em que parou, e o vídeo continua no destino.
- Reenviar o mesmo vídeo não duplica janelas, eventos nem insights do culto.
- Apagar um arquivo do destino não grava resultados, e o job disparado termina sem baixar vídeo.
- Um vídeo acima do limite de F7.1 termina o job antes do download, com o motivo no registro de F2.5.
- O bucket jobs-artifacts do namespace não recebe nenhum arquivo do teste.
- Se o webhook for adotado, o inventário de F2.6.T6 lista cada segredo guardado no Job de origem, com escopo, dono, validade, id do Job e rotação, sem o valor.
- Se o webhook não for adotado, o disparo manual está documentado com o comando completo e os parâmetros.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F7.5.T1 | Backend | Conferir os pré-requisitos da Fase 1 e gravar o culto e a data a partir do nome do arquivo | 8 | F2.5, F6.3, F6.4, F7.1.T1 |
| F7.5.T2 | Backend | Ler o vídeo do destino para /dev/shm, conferir o tamanho antes do download e, ao fim do job concluído, apagar o vídeo ou marcá-lo para rotulagem | 7 | F7.1.T1, F1.1, F7.4.T1 (local da marca 'aguardando rotulagem'), F6.2.T2 (regra de apagamento depois da rotulagem) |
| F7.5.T3 | MLOps | Definir a entrada e o comando do job do piloto com labels, filtros do disparo e linhagem | 6 | F2.2, F2.4, F2.5, F7.5.T1, F7.5.T2, F2.8 (linhagem da execução) |
| F7.5.T4 | DevOps | Configurar o webhook do destino que dispara o job, com os segredos guardados no Job de origem definidos e registrados, ou documentar o disparo manual | 8 | F7.5.T6, F7.1.T2, F2.6.T6 |
| F7.5.T5 | QA | Testar o disparo e os caminhos de erro com vídeo público | 8 | F7.5.T4, Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F7.5.T6 | DevOps | Publicar por tag de pré-release a imagem com o código de F7.5 e validar o comando do job com --dry-run | 3 | F7.5.T1, F7.5.T2, F7.5.T3, F2.2 |

<details><summary>F7.5.T1 · [Backend] Conferir os pré-requisitos da Fase 1 e gravar o culto e a data a partir do nome do arquivo</summary>

**Objetivo:** Fazer o pipeline derivar o culto e a data do nome do arquivo, recusar arquivo fora do padrão ou culto sem RIPD, aviso e, se acionada, a forma de F6.5 em vigor, e gravar service.

**Passos previstos:**
1. Derivar o id e a data do culto do nome do arquivo no padrão de F7.1 (docs/onprem.md:47, ex.: 2026-09-06-19h).
2. Recusar o arquivo com nome fora do padrão, sem gravar janelas, eventos nem insights, e registrar o motivo no registro de F2.5.
3. Definir o registro versionado com as datas de vigência do RIPD, do aviso e de F6.5.
4. Comparar essas datas com a data do culto e recusar se faltar registro ou se a vigência for posterior, gravando o motivo no registro de F2.5, sem janelas, eventos nem insights.
5. Depois de a checagem passar, gravar service.culto e service.data (0001_init.sql:4).
6. Escrever testes unitários para nome no padrão, nome fora do padrão e pré-requisito em vigor, ausente e posterior.

**Definição de pronto:** A checagem e a gravação de service estão no pipeline, e os testes dos cinco casos passam no CI.

**Dependências:** F2.5, F6.3, F6.4, F7.1.T1

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F7.5.T2 · [Backend] Ler o vídeo do destino para /dev/shm, conferir o tamanho antes do download e, ao fim do job concluído, apagar o vídeo ou marcá-lo para rotulagem</summary>

**Objetivo:** Fazer o pipeline ler o vídeo do destino escolhido em F7.1 sem gravar em disco, recusar vídeo acima do limite e, ao fim do processamento concluído, apagar o vídeo do destino ou, se o plano de F6.6 prevê rotulagem do culto, deixá-lo marcado 'aguardando rotulagem' para a varredura de F7.4.

**Passos previstos:**
1. Se o destino for bucket, acrescentar a resolve_video o caminho hf://buckets/, porque hoje só hf://datasets/ é tratado (processar_culto.py:24). Se for repositório, passar a revisão recebida no disparo.
2. Antes do download, conferir o tamanho do arquivo (campo size do payload no disparo por webhook, ou consulta ao destino no disparo manual) e encerrar o job acima do limite de F7.1, com o motivo no registro de F2.5.
3. Baixar para /dev/shm e limpar ao fim, inclusive quando a execução falhar (issue #2).
4. Ao fim do job concluído, consultar se o plano de F6.6 prevê rotulagem do culto. Se não prevê, apagar o vídeo do destino com a credencial do job e registrar o apagamento em F2.5. Se prevê, não apagar e gravar a marca 'aguardando rotulagem' no local de F7.4.T1. Em falha, não apagar.
5. Escrever testes com download e apagamento simulados.

**Definição de pronto:** Os testes passam. A guarda não encontra resíduo em disco nem em /dev/shm depois de uma execução com falha simulada. No caso concluído sem rotulagem prevista, o apagamento simulado é chamado uma vez; no caso concluído com rotulagem prevista, nenhuma vez e a marca é gravada; no caso com falha, nenhuma vez.

**Dependências:** F7.1.T1, F1.1, F7.4.T1 (local da marca 'aguardando rotulagem'), F6.2.T2 (regra de apagamento depois da rotulagem)

**Estimativa sugerida:** 7 h (sugestão; validar com o time)

</details>

<details><summary>F7.5.T3 · [MLOps] Definir a entrada e o comando do job do piloto com labels, filtros do disparo e linhagem</summary>

**Objetivo:** Ter um comando versionado que processa um culto pela imagem com digest, ignora disparos que não são de vídeo novo e grava a linhagem.

**Passos previstos:**
1. Montar 'hf jobs run <imagem>@<digest>' com comando explícito, com o flavor e o motor do ADR 0001 e o timeout confirmado em F2.2. O digest é preenchido em F7.5.T6.
2. Acrescentar labels de culto e de motor e passar os segredos só pelo nome, incluindo o token do HF com permissão de ler e apagar só no destino do piloto.
3. Ler de WEBHOOK_PAYLOAD o caminho do arquivo (updatedFiles) ou a revisão (updatedRefs ou headSha). Ignorar entradas com action 'delete' e arquivos fora do padrão de F7.1, terminando antes de baixar vídeo ou carregar modelos e registrando o motivo em F2.5.
4. Sem WEBHOOK_PAYLOAD e sem os parâmetros do disparo manual, terminar sem baixar vídeo nem carregar modelos, com o motivo registrado; é o caso da criação do Job de origem.
5. Definir os parâmetros do disparo manual: caminho do arquivo no destino e id do culto.
6. Garantir que o run_id de F2.5 torna o reprocessamento idempotente.
7. Escrever testes do filtro com payloads de exemplo: arquivo novo no padrão, action 'delete', arquivo fora do padrão e ausência de payload.

**Definição de pronto:** O comando e o código de entrada estão versionados, e os testes do filtro passam no CI.

**Dependências:** F2.2, F2.4, F2.5, F7.5.T1, F7.5.T2, F2.8 (linhagem da execução)

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F7.5.T4 · [DevOps] Configurar o webhook do destino que dispara o job, com os segredos guardados no Job de origem definidos e registrados, ou documentar o disparo manual</summary>

**Objetivo:** Fazer a chegada do vídeo disparar o job, com os segredos do Job de origem de escopo mínimo e registrados no inventário, ou deixar o disparo manual documentado.

**Passos previstos:**
1. Verificar na documentação se um webhook de bucket dispara Job: webhooks#buckets descreve o evento, mas jobs-webhooks lista WEBHOOK_REPO_TYPE só como model, dataset ou space.
2. Definir os segredos que ficam guardados, criptografados, no Job de origem (https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets): a chave de serviço do Supabase, o token do HF que lê e apaga só no destino do piloto e o token de escrita só no repositório de resultados de F2.8, cada um com o escopo mínimo.
3. Definir a rotação: como update_webhook não aceita job_id (hf_api.py:11378-11386), trocar um segredo exige criar outro Job de origem e outro webhook e desativar ou apagar o anterior (hf_api.py:11520,11573).
4. Pedir a aprovação de custo do Job de origem, dos jobs dos 4 cultos e dos disparos curtos gerados por apagamento (P7) antes de criar o webhook.
5. Com a aprovação, criar o Job de origem pela imagem de F7.5.T6, passando os segredos só pelo nome, e o webhook com segredo de assinatura (https://huggingface.co/docs/hub/jobs-webhooks).
6. Conferir no histórico de entregas que o evento de teste chegou e, no job disparado, que os segredos estão presentes, sem imprimir o valor.
7. Registrar no inventário de F2.6.T6 cada segredo guardado, com o id do Job de origem, o escopo, o dono, a validade e a rotação, sem o valor.
8. Se o webhook não for adotado, documentar o comando manual completo, com os parâmetros de F7.5.T3, os segredos passados só pelo nome por quem lança, como em F2.6, e quem o executa.

**Definição de pronto:** O webhook aparece na lista de webhooks da conta com a entrega de teste registrada e o inventário de F2.6.T6 lista os segredos do Job de origem, ou o procedimento manual está versionado.

**Dependências:** F7.5.T6, F7.1.T2, F2.6.T6

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F7.5.T5 · [QA] Testar o disparo e os caminhos de erro com vídeo público</summary>

**Objetivo:** Verificar os critérios de F7.5 antes do primeiro culto real.

**Passos previstos:**
1. Pedir a aprovação de custo dos jobs de teste antes de executar (P7).
2. Caminho feliz: enviar um vídeo público e conferir job, imagem de F7.5.T6, labels, registro de execução, service.culto e service.data, insights pendentes na fila e o vídeo apagado do destino.
3. Caminho com rotulagem prevista: com um culto de teste marcado no plano de teste como rotulável, conferir que o vídeo continua no destino com a marca 'aguardando rotulagem'.
4. Pré-requisito ausente, vigência posterior e nome fora do padrão: conferir que nada foi gravado e que o motivo está no registro de F2.5.
5. Arquivo corrompido: conferir a etapa no registro de F2.5 e que o vídeo continua no destino.
6. Vídeo acima do limite, com o limite reduzido no ambiente de teste: conferir que o job terminou antes do download, com o motivo registrado.
7. Reenvio do mesmo vídeo: conferir que não houve duplicação.
8. Apagamento de um arquivo do destino: conferir que o job terminou sem baixar vídeo e sem gravar resultados.
9. Conferir que jobs-artifacts não recebeu arquivo.
10. Se o webhook foi adotado, conferir no inventário de F2.6.T6 os segredos do Job de origem, sem o valor.

**Definição de pronto:** As evidências de cada caso estão anexadas ao PBI, e todos passaram.

**Dependências:** F7.5.T4, Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F7.5.T6 · [DevOps] Publicar por tag de pré-release a imagem com o código de F7.5 e validar o comando do job com --dry-run</summary>

**Objetivo:** Ter uma imagem com digest que contém a checagem de pré-requisitos, a leitura e o apagamento do vídeo e o filtro do disparo, para F7.5.T4 e F7.5.T5.

**Passos previstos:**
1. Publicar por tag de pré-release, pelo processo de F2.2, a imagem com F7.5.T1, F7.5.T2 e F7.5.T3, como F5.3.T3 faz com a imagem da branch, e registrar o digest no registro de F2.5.
2. Pôr o digest no comando versionado de F7.5.T3.
3. Validar o comando com 'hf jobs run --dry-run' (huggingface_hub/cli/jobs.py:470-476,712-713), sem submeter o Job.
4. Registrar que esta imagem serve só aos testes de F7.5 e que os cultos reais usam a imagem de release de F7.7.T1.

**Definição de pronto:** O digest está no registro de F2.5 e no comando versionado, e a saída de 'hf jobs run --dry-run' anexada ao PBI mostra a imagem com esse digest, as labels, os nomes dos segredos e o timeout.

**Dependências:** F7.5.T1, F7.5.T2, F7.5.T3, F2.2

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- feature_F7.json (árvore v1), PBI F7.5
- feature_F5_v3.json (F5.3.T3 e F5.4.T3, padrão de publicação de imagem)
- huggingface_hub/hf_api.py:11244-11275 (create_webhook)
- huggingface_hub/hf_api.py:11378-11386,11520,11573 (update_webhook sem job_id, disable_webhook e delete_webhook)
- huggingface_hub/_jobs_api.py:211-212 (segredos criptografados)
- huggingface_hub/cli/jobs.py:470-476,712-713 (--dry-run)
- https://huggingface.co/docs/hub/jobs-webhooks
- https://huggingface.co/docs/hub/webhooks#buckets
- https://huggingface.co/docs/hub/jobs-manage
- https://huggingface.co/docs/hub/jobs-configuration#timeout
- https://huggingface.co/docs/hub/jobs-configuration#environment-variables-and-secrets
- processar_culto.py:23-46,103-115
- reacao/store.py:28-44
- supabase/migrations/0001_init.sql:4,18
- docs/onprem.md:47
- README.pt-BR.md:16-17,35
- premissas P7, P19, P20, P27 e P29

#### Verificação INVEST: pontos que falharam
- Small: é um dos PBIs mais largos (P6). Se não couber numa sprint, dividir por modo de disparo: disparo manual com checagem de pré-requisitos primeiro, webhook depois.
- Independente: depende de dez PBIs, entre eles F7.1 e F7.3 da mesma Feature.

#### Premissas
- A documentação descreve webhooks de bucket (webhooks#buckets). Não foi verificado se um webhook de bucket dispara Job, porque jobs-webhooks lista WEBHOOK_REPO_TYPE só como model, dataset ou space, e a docstring de create_webhook também não lista bucket (hf_api.py:11265-11267). Se não disparar, o disparo é manual e documentado.
- create_webhook(job_id=...) dispara a partir de um Job de origem (hf_api.py:11262-11263). Criar esse Job de origem é uma execução paga que precisa de aprovação.
- Dedução não verificada: o job disparado pelo webhook reexecuta a especificação do Job de origem, com a mesma imagem e os mesmos segredos. F7.5.T4 confere no primeiro disparo de teste, sem imprimir o valor de nenhum segredo.
- Cada apagamento de arquivo no destino, inclusive o do fim do job, dispara o webhook de bucket e um job curto que termina sem baixar vídeo. Esses disparos entram na aprovação de custo.
- A aprovação de custo dos 4 cultos é dada antes do primeiro envio, porque o webhook dispara sem ninguém presente (P7).
- Um job que falha deixa o vídeo no destino para reprocessamento; a varredura de F7.4 o apaga no prazo máximo.
- Os pré-requisitos ficam num registro versionado com as datas de vigência. O formato é decidido em F7.5.T1.
- Se F6.2 proibir trechos nos logs, o log do job não pode conter texto de insight nem de transcrição. Hoje o job imprime o run_log e, com --stdout, janelas, eventos e insights (processar_culto.py:108-115). O critério entra quando F6.2 decidir.
- A dependência de F6.5 só vale se ele for acionado (P29).
- Revisão aplicada: F7.5.T6 publica a imagem com o código de F7.5 para os testes, e a validação com --dry-run saiu de F7.5.T3 e foi para F7.5.T6, porque precisa do digest dessa imagem. F7.5.T6 foi numerada no fim para não mudar as referências a F7.5.T4 e F7.5.T5; ela roda antes de F7.5.T4.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Vínculo com a Feature F7
- Aprovação de custo dos jobs de teste, do Job de origem do webhook e dos disparos por apagamento
- Registro dos segredos do Job de origem no inventário de F2.6.T6

## Preview — PBI F7.6 (novo) · Sinalizar no painel web na Vercel os cultos com qualidade de medição abaixo dos limites do plano da Fase 1

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Sinalizar no painel web na Vercel os cultos com qualidade de medição abaixo dos limites do plano da Fase 1 |
| Tipo | Product Backlog Item |
| Pai | F7 |
| Tags | Fase 1; piloto; qualidade de medição; Vercel |
| Estimativa | 5 pts (sugestão); tasks: 27 h |
| Dependências | F5.6 (painel base na Vercel e verificação de lint), F6.6 (limites de alerta por culto), F7.2 (perfil revisor, matriz com os indicadores da lista de D7 de F2.4.T4 e seed no CI com Supabase local), F7.3 (fila de revisão onde o alerta aparece), F2.5 (run_id para ligar indicadores à execução) |
| Substitui | nenhum |

#### Descrição

Como revisor do relatório do piloto  
Quero ver, antes de liberar um culto, os indicadores de qualidade da medição e um alerta com o motivo quando algum deles ficar abaixo do limite  
Para não liberar ao pastor, sem saber, um relatório de culto medido com cobertura ou rostos insuficientes

**Contexto:** O registro de execução guarda cobertura_pct, a porcentagem de janelas não insuficientes (processar_culto.py:103-106). Cada janela guarda quadros, quadros_com_plateia, n_mensuravel e altura_mediana_px (reacao/types.py:38-53). n_mensuravel é a média arredondada de rostos mensuráveis por quadro com plateia (reacao/aggregate.py:24-30), e altura_mediana_px é a mediana das alturas dos rostos da janela (reacao/aggregate.py:32-33). F6.6 entrega um documento assinado com os limites de alerta por culto (árvore, F6.6). Visões criadas do jeito padrão passam por cima do RLS; com Postgres 15 ou superior, security_invoker = true faz a visão obedecer às políticas das tabelas (https://supabase.com/docs/guides/database/postgres/row-level-security#expose-a-view-safely). O vídeo é apagado ao fim do job (F7.5), então recalcular indicadores exige reenviar o vídeo e pagar outro job (P7). Pela P3 revisada, o painel web na Vercel lê só agregados, eventos e insights, e D7 de F2.4.T4 inclui os indicadores de F7.6 na lista de tabelas do painel para a Fase 1.

**Regras de negócio:**
- RN01 – Os indicadores por culto são cobertura_pct, quadros_com_plateia, altura_mediana_px e rostos mensuráveis por quadro, calculados só a partir de agregados e do registro de execução.
- RN02 – Os limites vêm de F6.6. A forma de agregar cada indicador por culto é definida em F7.6.T1 e revisada por quem assina F6.6. Os limites ficam num arquivo versionado criado em F7.6.T1 e carregado numa tabela do Supabase; o painel não tem limite fixo no código.
- RN03 – A comparação com os limites acontece na leitura, no banco, sem reprocessar o culto.
- RN04 – O alerta aparece na fila de revisão antes da ação de aprovar e diz qual indicador ficou abaixo do limite e o valor dele.
- RN05 – Quem vê os indicadores segue a matriz de F7.2. Os indicadores de F7.6 estão na lista de tabelas do painel de D7 de F2.4.T4 para a Fase 1; os limites que não couberem nessa lista entram como exceção aprovada pelo encarregado (F7.2 RN03).
- RN06 – Os indicadores ficam em tabela com RLS, e o alerta, se exposto por visão, usa security_invoker = true sobre tabelas com RLS (https://supabase.com/docs/guides/database/postgres/row-level-security#expose-a-view-safely).

**Fora de escopo:**
- Definição dos limites (F6.6)
- Bloqueio automático da liberação, salvo se F6.6 decidir
- Indicadores por pessoa, assento ou setor
- Reprocessamento de culto para atualizar indicadores
- Publicação da imagem com o cálculo dos indicadores para os cultos reais (F7.7.T1)

#### Critérios de aceite

- Para um culto de teste com todos os indicadores dentro dos limites, a fila de revisão mostra os quatro valores e nenhum alerta.
- Para um culto de teste com um dos quatro indicadores abaixo do limite, o alerta aparece antes da ação de aprovar, com o nome do indicador e o valor. O teste é repetido para cada um dos quatro indicadores.
- Para um culto sem registro de execução ou sem janelas, a tela mostra 'indicadores indisponíveis' em vez de valores vazios.
- Os valores mostrados são iguais aos calculados pelo script de referência sobre as mesmas janelas.
- Mudar um limite no arquivo versionado de limites e carregá-lo na tabela de limites muda o alerta sem mudança no código do painel e sem reprocessar o culto.
- Uma conta fora dos perfis previstos na matriz não recebe indicadores, limites nem alertas numa consulta direta à API do banco, nem pelas tabelas nem pela visão.
- O teste de políticas ampliado cobre a tabela de indicadores, a de limites e a visão de alerta, se existir, e passa no CI contra o Supabase local.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F7.6.T1 | Data Science | Definir o cálculo por culto dos quatro indicadores e o arquivo versionado de limites | 5 | F6.6 |
| F7.6.T2 | MLOps | Calcular e gravar os indicadores de qualidade em cada execução | 4 | F7.6.T1, F7.6.T3, F2.5 |
| F7.6.T3 | Backend | Guardar indicadores e limites no Supabase com RLS e expor o alerta ao perfil revisor | 6 | F7.2.T1, F7.2.T3, F7.2.T4, F7.6.T1 |
| F7.6.T4 | Front end | Mostrar os indicadores e o alerta na fila de revisão | 6 | F7.6.T3, F7.3.T3 |
| F7.6.T5 | QA | Verificar a sinalização e o acesso aos indicadores com cultos de teste | 6 | F7.6.T2, F7.6.T4 |

<details><summary>F7.6.T1 · [Data Science] Definir o cálculo por culto dos quatro indicadores e o arquivo versionado de limites</summary>

**Objetivo:** Ter a fórmula de cada indicador por culto, um script de referência e os limites de F6.6 num arquivo legível por máquina.

**Passos previstos:**
1. Tomar cobertura_pct do registro de execução (processar_culto.py:103).
2. Definir quadros_com_plateia por culto: soma e fração sobre os quadros.
3. Definir como agregar altura_mediana_px e n_mensuravel entre janelas (reacao/aggregate.py:24-33) e submeter a fórmula a quem assina F6.6.
4. Escrever o script de referência que calcula os quatro indicadores a partir das janelas de um culto.
5. Transcrever os limites do documento assinado de F6.6 para um arquivo versionado legível por máquina, com a versão e a referência ao documento.

**Definição de pronto:** O documento das fórmulas, o script de referência com um exemplo calculado e o arquivo de limites estão versionados, e quem assina F6.6 revisou a fórmula.

**Dependências:** F6.6

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F7.6.T2 · [MLOps] Calcular e gravar os indicadores de qualidade em cada execução</summary>

**Objetivo:** Fazer cada execução gravar os quatro indicadores ligados ao run_id, sem limites nem alerta.

**Passos previstos:**
1. Ao fim do job, calcular os quatro indicadores com a fórmula de F7.6.T1.
2. Gravar os indicadores com o run_id de F2.5 na tabela de F7.6.T3.
3. Rodar com o motor mock e a fixture sintética, como no CI (.github/workflows/ci.yml:14-15), e comparar os valores gravados no JSON local do Store (reacao/store.py:19-23) com o script de referência.

**Definição de pronto:** A execução com o motor mock e a fixture sintética grava valores iguais aos do script de referência.

**Dependências:** F7.6.T1, F7.6.T3, F2.5

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F7.6.T3 · [Backend] Guardar indicadores e limites no Supabase com RLS e expor o alerta ao perfil revisor</summary>

**Objetivo:** Guardar os indicadores e os limites no Supabase com leitura só pelos perfis da matriz e comparar na leitura.

**Passos previstos:**
1. Escrever a migração com a tabela de indicadores por run_id e a tabela de limites com versão, as duas com RLS habilitada.
2. Criar a visão de alerta com security_invoker = true sobre as duas tabelas (https://supabase.com/docs/guides/database/postgres/row-level-security#expose-a-view-safely). Se o Postgres do projeto for anterior à versão 15, não criar a visão e registrar que o painel compara as duas tabelas.
3. Criar a política de leitura das tabelas para os perfis previstos na matriz de F7.2.
4. Escrever o carregamento do arquivo de limites de F7.6.T1 na tabela de limites.
5. Rodar tests/test_schema.py e ruff.

**Definição de pronto:** A migração está aplicada no Supabase local e no projeto de desenvolvimento, a visão tem security_invoker = true ou está registrado por que não existe, e ruff e pytest passam.

**Dependências:** F7.2.T1, F7.2.T3, F7.2.T4, F7.6.T1

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F7.6.T4 · [Front end] Mostrar os indicadores e o alerta na fila de revisão</summary>

**Objetivo:** Mostrar ao revisor os quatro indicadores e o alerta antes da ação de aprovar.

**Passos previstos:**
1. Mostrar os quatro valores do culto no espaço reservado em F7.3.T3.
2. Mostrar o alerta com o nome do indicador e o valor quando algum ficar abaixo do limite, lido do banco.
3. Mostrar 'indicadores indisponíveis' quando faltar registro de execução ou janela.
4. Pôr os textos fixos no arquivo de textos de F5.6.T1, lido pela verificação de lint de F5.6.T5.

**Definição de pronto:** Num preview com cultos de teste, os três casos aparecem como descrito, e a verificação de lint passa.

**Dependências:** F7.6.T3, F7.3.T3

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F7.6.T5 · [QA] Verificar a sinalização e o acesso aos indicadores com cultos de teste</summary>

**Objetivo:** Conferir os critérios de F7.6.

**Passos previstos:**
1. Ampliar o teste de políticas de F7.2.T7 com a tabela de indicadores, a de limites e a visão, para os perfis da matriz e para uma conta fora dela.
2. Preparar cultos de teste: todos os indicadores dentro, cada indicador abaixo do limite e culto sem registro de execução.
3. Comparar os valores do painel com o script de referência.
4. Mudar um limite no arquivo, carregar na tabela e conferir que o alerta muda sem reprocessar o culto.

**Definição de pronto:** O teste ampliado passa no CI, e as evidências de cada critério estão anexadas ao PBI, com todos passando.

**Dependências:** F7.6.T2, F7.6.T4

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- feature_F7.json (árvore v1), PBI F7.6
- processar_culto.py:103-106
- reacao/types.py:38-53
- reacao/aggregate.py:24-33
- https://supabase.com/docs/guides/database/postgres/row-level-security#expose-a-view-safely
- .github/workflows/ci.yml:14-15
- reacao/store.py:19-23
- README.pt-BR.md:35
- premissas P7 e P3 revisada

#### Verificação INVEST: pontos que falharam
- Independente: o alerta aparece na fila de revisão de F7.3, que precisa estar pronta antes de F7.6.T4.

#### Premissas
- A disciplina Backend entrou neste PBI. Expor os indicadores ao perfil revisor exige tabelas ou uma visão no Supabase com política de RLS, e schema e políticas são trabalho de Backend pela regra de disciplinas.
- Até F6.6 decidir se o alerta bloqueia a liberação, ele só informa o revisor.
- A forma de agregar cada indicador por culto é definida só em F7.6.T1. Quem assina F6.6 a revisa, para que os limites valham para a mesma grandeza.
- A comparação na leitura foi escolhida porque o vídeo é apagado ao fim do job (F7.5) e reprocessar um culto é pago (P7).
- A visão com security_invoker exige Postgres 15 ou superior. A versão do Postgres do projeto de desenvolvimento não foi verificada; se for anterior, o painel compara as duas tabelas com RLS, sem visão.
- Indicadores e limites não estão entre agregados, eventos e insights da P3 revisada. D7 de F2.4.T4 põe os indicadores de F7.6 na lista de tabelas do painel para a Fase 1, e a matriz de F7.2 define quais perfis os leem; os limites, se ficarem em tabela à parte, entram como exceção aprovada pelo encarregado.
- O cálculo de F7.6.T2 entra nos jobs dos cultos reais pela imagem de release de F7.7.T1.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Vínculo com a Feature F7
- Limites assinados em F6.6

## Preview — PBI F7.7 (novo) · Operar e rotular os 4 cultos do piloto, consolidar os resultados e registrar a decisão de conclusão da Fase 1

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Operar e rotular os 4 cultos do piloto, consolidar os resultados e registrar a decisão de conclusão da Fase 1 |
| Tipo | Product Backlog Item |
| Pai | F7 |
| Tags | Fase 1; piloto; operação; decisão; Data Science; Visão Computacional |
| Estimativa | 13 pts (sugestão); tasks: 64 h |
| Dependências | F6.2 (mudanças no agregado e nos logs, F6.2.T3 e F6.2.T4, incluídas na imagem de release), F6.3 (RIPD), F6.4 (aviso publicado antes do primeiro culto), F6.5 (se acionado), F6.6 (critério de conclusão, forma de devolução das notas e responsáveis), F7.1 (destino, procedimento e refs do corpus registradas), F7.2 (perfis pastor e revisor), F7.3 (revisão, liberação e notas), F7.4 (retenção ativa antes do primeiro culto e Job agendado de varredura), F7.5 (disparo, processamento e Job de origem do webhook), F7.6 (indicadores e alerta de qualidade), F7.8 (perfis mídia e DPO), F2.8 (repositório de resultados com linhagem), F2.6 (inventário de credenciais, F2.6.T6), F2.5 (registro de execução e run_id), F7.9 (leitura do destino do piloto pela ferramenta de rotulagem), F3.2 (protocolo de rotulagem), F3.3 (ferramenta de rotulagem no Space privado) |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro, operador do piloto, junto com o revisor, os rotuladores do piloto e as pessoas que F6.6 define como responsáveis pela decisão  
Quero publicar a imagem de release do piloto, processar, rotular, revisar e liberar cada um dos 4 cultos, colher as notas do pastor e ter um documento que compare os resultados com o critério de conclusão  
Para decidir, com registro assinado, se a Fase 1 está concluída

**Contexto:** O roteiro prevê a Fase 1 com uma igreja e 4 cultos e, depois dela, o painel ao vivo e o sinal ao pregador (README.pt-BR.md:35-36). O escopo do épico põe no piloto os perfis pastor, mídia e DPO (epico.json); F7.2 dá acesso a pastor e revisor e F7.8 a mídia e DPO. F7.5 constrói o disparo do processamento, F7.3 a revisão e a liberação, F7.6 o alerta de qualidade e F7.4 a retenção; este PBI os usa nos 4 cultos reais. Os testes de F7.5 usam uma imagem de pré-release (F7.5.T6), e o Job agendado de F7.4 usa a imagem de pré-release com o script de varredura (F7.4.T4). As mudanças de F6.2 no agregado e nos logs (F6.2.T3 e F6.2.T4) e o cálculo dos indicadores de F7.6.T2 ainda não estão nessas imagens. F7.7.T1 publica a imagem de release do piloto, como F5.4.T3 faz na Fase 0 (feature_F5_v3.json). update_webhook não aceita job_id (huggingface_hub/hf_api.py:11378-11386), e a biblioteca só altera labels de um Job agendado (hf_api.py:13378), então a troca de digest recria o Job de origem, o webhook e o Job agendado. O critério de conclusão, os critérios do gate que se repetem, a forma como o pastor devolve a avaliação dos insights e quem decide estão em F6.6. Os dados vêm do registro de execução de F2.5, da linhagem de F2.8, dos indicadores de F7.6 e das notas do pastor de F7.3. reacao/lint.py check() recebe um Insight e exige minuto, momento, trecho e sinais (reacao/lint.py:23-49), então um texto corrido é verificado só contra as listas PROIBIDO e PROIBIDO_INDIVIDUAL (reacao/lint.py:8-13), como em F6.4. Pela P3 revisada, toda avaliação roda no ambiente do HF. As refs e as tags do corpus antes do primeiro envio ficam registradas em F7.1.T4. O plano de F6.6 prevê rótulos de referência dos cultos do piloto, feitos na ferramenta do Space privado de F3.3 pelo protocolo de F3.2 e revisados por amostragem (F6.6 RN03 e RN11), e a regra de F6.2 mantém o vídeo de cada culto no destino até o fim dessa rotulagem, dentro do prazo máximo (F6.2 RN08). F7.9 dá à ferramenta a leitura do destino do piloto.

**Regras de negócio:**
- RN01 – Cada culto só é processado com o RIPD, o aviso e, se acionada, a forma de F6.5 em vigor na data do culto (F7.5 RN02) e com a retenção ativa (F7.4).
- RN02 – Cada culto processado é revisado pelo perfil revisor pelo roteiro de F7.3.T1. Culto não liberado tem o motivo registrado.
- RN03 – As notas do pastor são colhidas na forma e no prazo de F6.6. Culto sem nota no prazo aparece como 'sem avaliação'.
- RN04 – Cada número do documento cita o run_id (F2.5) ou o arquivo de origem no repositório de resultados com linhagem (F2.8).
- RN05 – O documento não tem número por pessoa, assento ou setor, e janelas insuficientes aparecem sem percentual (CLAUDE.md regra 3).
- RN06 – O texto do documento não contém termos das listas PROIBIDO e PROIBIDO_INDIVIDUAL de reacao/lint.py (CLAUDE.md regra 4).
- RN07 – A extração dos dados roda só no HF Jobs, pela imagem com digest, com aprovação de custo, e o resultado vai ao repositório de resultados de F2.8 (P3 revisada; P7).
- RN08 – A decisão segue as opções e os responsáveis definidos em F6.6.
- RN09 – Culto sinalizado em F7.6 ou não processado aparece no documento com o motivo.
- RN10 – Os 4 cultos e a varredura agendada rodam pela imagem de release do piloto publicada em F7.7.T1, com o digest registrado antes do primeiro culto (arvore_v1.json, F2.4).
- RN11 – O primeiro culto só é processado depois de F7.8 verificado, porque o escopo do épico põe os perfis pastor, mídia e DPO no piloto (epico.json).
- RN12 – Cada culto com rotulagem prevista no plano de F6.6 é rotulado na ferramenta de F3.3 pelo protocolo de F3.2, sem som salvo exceção registrada no RIPD, dentro do prazo do plano, e os rótulos vão ao destino do ADR de F6.2, fora do corpus. O fim da rotulagem só é registrado depois da revisão por amostragem, e é esse registro que libera o apagamento do vídeo (F6.6 RN03, RN10 e RN11; F6.2 RN08).

**Fora de escopo:**
- Definição do critério de conclusão (F6.6)
- Construção do disparo, da revisão e da sinalização (F7.5, F7.3 e F7.6)
- Planejamento das fases seguintes (README.pt-BR.md:36)
- Comparação ou classificação de pregadores (README.pt-BR.md:21)
- Mais de 4 cultos ou outra igreja

#### Critérios de aceite

- Antes do primeiro culto, o digest da imagem de release do piloto está no registro de F2.5; o Job de origem do webhook, ou o comando manual documentado, e o Job agendado de varredura usam esse digest; só o webhook novo está ativo; e F7.8 está verificado.
- Cada um dos 4 cultos tem job concluído, registro de execução e insights na fila de revisão, ou o motivo registrado de não ter sido processado. No modo manual, o comando documentado de F7.5 foi usado em cada culto.
- Cada culto processado tem todos os insights aprovados ou rejeitados pelo revisor e o relatório liberado ao pastor, ou o motivo registrado de não ter sido liberado.
- Cada culto processado com rotulagem prevista no plano de F6.6 tem os rótulos feitos e revisados por amostragem, no destino dos rótulos do piloto, com a data do fim da rotulagem, ou o motivo registrado; nenhum rótulo do piloto aparece no dataset do corpus.
- Cada culto liberado tem as notas do pastor, ou o registro 'sem avaliação' depois do prazo de F6.6.
- O documento está no repositório com uma linha para cada culto, com indicadores de qualidade, notas do pastor e critérios repetidos, cada valor com a origem, e recalcular a partir das origens reproduz todos os números.
- Cada item do critério de conclusão de F6.6 aparece com o resultado 'atingido' ou 'não atingido', e a comparação diz se a falta de nota de um culto impede a conclusão segundo F6.6.
- Um culto sinalizado ou não processado aparece no documento com o motivo.
- O texto do documento não contém termos das listas PROIBIDO e PROIBIDO_INDIVIDUAL de reacao/lint.py.
- No fim do piloto, nenhum vídeo do piloto aparece no dataset do corpus, no bucket jobs-artifacts nem nos arquivos do deployment de produção na Vercel, o vídeo de cada culto saiu do destino depois do fim da rotulagem ou no prazo máximo do ADR de F6.2, e a gravação na igreja seguiu o procedimento de F7.1.
- No fim do piloto, as tags e as revisões do dataset do corpus resolvem para os mesmos commits registrados em F7.1.T4, e nenhum culto com data anterior à vigência dos pré-requisitos tem janelas, eventos ou insights.
- A decisão está registrada com data e com as assinaturas das pessoas definidas em F6.6.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F7.7.T1 | DevOps | Publicar por tag de release a imagem do piloto e trocar para o novo digest o Job de origem do webhook e o Job agendado de varredura | 6 | F6.2.T3, F6.2.T4, F7.5.T5, F7.6.T2, F7.4.T5, F2.6.T6, Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F7.7.T2 | MLOps | Disparar e acompanhar o processamento de cada um dos 4 cultos | 6 | F7.7.T1, F7.5.T5, F7.4.T5, F7.1.T4, F7.8.T3, Aprovação de Fabio (P7), com flavor, duração e custo previstos, F7.9.T4 |
| F7.7.T3 | Governança e Privacidade | Revisar e liberar os insights de cada culto pelo roteiro de F7.3.T1 | 8 | F7.7.T2, F7.3.T5, F7.6.T5 |
| F7.7.T4 | Data Science | Acompanhar a coleta das notas do pastor em cada culto liberado | 3 | F7.7.T3, F6.6 |
| F7.7.T5 | Data Science | Extrair e consolidar no HF Jobs os dados dos 4 cultos | 8 | F7.7.T4, F7.6.T2, F2.8, Aprovação de Fabio (P7), com flavor, duração e custo previstos, F7.7.T10 |
| F7.7.T6 | Data Science | Comparar os resultados com o critério de conclusão de F6.6 e redigir o documento | 4 | F7.7.T5, F6.6 |
| F7.7.T7 | QA | Conferir o documento e as verificações de antes e de fim de piloto | 6 | F7.7.T6 |
| F7.7.T8 | Governança e Privacidade | Revisar o documento e registrar a decisão assinada | 3 | F7.7.T7 |
| F7.7.T9 | Visão Computacional | Rotular os cultos do piloto na ferramenta de F3.3 pelo protocolo de F3.2, no prazo do plano de F6.6 | 16 | F7.7.T2, F7.9.T4, F3.2, F6.6 |
| F7.7.T10 | Data Science | Revisar por amostragem os rótulos de cada culto e registrar o fim da rotulagem | 4 | F7.7.T9, F6.6, F7.4.T1 |

<details><summary>F7.7.T1 · [DevOps] Publicar por tag de release a imagem do piloto e trocar para o novo digest o Job de origem do webhook e o Job agendado de varredura</summary>

**Objetivo:** Fazer os jobs dos 4 cultos e a varredura rodarem, desde o primeiro culto, pela imagem com a minimização de F6.2, a checagem de pré-requisitos e o apagamento de F7.5, os indicadores de F7.6 e o script de varredura de F7.4.

**Passos previstos:**
1. Conferir que estão na branch main as mudanças de F6.2.T3 e F6.2.T4 (agregado e logs), de F7.5.T1 a F7.5.T3, de F7.6.T2 e o script de varredura de F7.4.T4.
2. Publicar a imagem por tag de release, como F5.4.T3, e registrar o digest no registro de F2.5.
3. Pedir a aprovação de custo (P7) do novo Job de origem e do Job agendado recriado antes de criá-los.
4. Webhook: como update_webhook não aceita job_id (hf_api.py:11378-11386), criar um Job de origem com o novo digest e os segredos definidos em F7.5.T4, criar um webhook que aponta para ele, com segredo de assinatura, e desativar ou apagar o webhook anterior (hf_api.py:11520,11573). No modo manual, trocar o digest no comando documentado de F7.5.T4.
5. Job agendado: como a biblioteca só altera labels de um Job agendado (hf_api.py:13378), apagar o Job de F7.4.T4 e criá-lo de novo com o novo digest e os segredos definidos em F7.4.T4, suspenso até a aprovação (suspend=True; hf_api.py:13042-13043), e depois retomá-lo.
6. Validar os comandos com 'hf jobs run --dry-run' e conferir com 'hf jobs scheduled inspect', com a inspeção do Job de origem e com HfApi.list_webhooks() que só o webhook novo está ativo e que os dois Jobs usam o novo digest.
7. Atualizar no inventário de F2.6.T6 os ids dos Jobs que guardam segredos e registrar a data da troca, que precisa ser anterior ao primeiro culto.

**Definição de pronto:** O digest da release está no registro de F2.5; 'hf jobs scheduled inspect' e a inspeção do Job de origem mostram esse digest; HfApi.list_webhooks() mostra um só webhook ativo, apontando para o novo Job de origem, ou o comando manual documentado usa o novo digest; e o inventário de F2.6.T6 está atualizado, com data anterior ao primeiro culto.

**Dependências:** F6.2.T3, F6.2.T4, F7.5.T5, F7.6.T2, F7.4.T5, F2.6.T6, Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F7.7.T2 · [MLOps] Disparar e acompanhar o processamento de cada um dos 4 cultos</summary>

**Objetivo:** Ter, para cada culto do piloto, o job, o run_id e o estado, com o vídeo fora do destino e o revisor avisado.

**Passos previstos:**
1. Antes do primeiro culto, confirmar que a retenção de F7.4 está ativa, que o registro de vigência de F7.5.T1 tem o RIPD, o aviso e, se acionada, a forma de F6.5, que a aprovação de custo dos 4 cultos está registrada (P7), que F7.7.T1 trocou o digest dos jobs e que os critérios de F7.8 passaram.
2. Para cada culto, depois que o vídeo chega ao destino, acompanhar o job disparado pelo webhook ou executar o comando manual documentado em F7.5.T4, com o digest de F7.7.T1.
3. Registrar por culto JOB_ID, run_id, digest da imagem, estado, a confirmação de que o vídeo saiu do destino ou recebeu a marca 'aguardando rotulagem' e, se houver, o motivo de não processamento.
4. Avisar o revisor quando o culto estiver na fila e os rotuladores quando o culto estiver marcado para rotulagem.

**Definição de pronto:** A tabela dos 4 cultos está completa no repositório de resultados de F2.8, com uma linha por culto.

**Dependências:** F7.7.T1, F7.5.T5, F7.4.T5, F7.1.T4, F7.8.T3, Aprovação de Fabio (P7), com flavor, duração e custo previstos, F7.9.T4

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F7.7.T3 · [Governança e Privacidade] Revisar e liberar os insights de cada culto pelo roteiro de F7.3.T1</summary>

**Objetivo:** Deixar cada culto processado revisado e liberado ao pastor, ou com o motivo de não liberação registrado.

**Passos previstos:**
1. Para cada culto na fila, ler os indicadores e o alerta de qualidade de F7.6 antes de agir.
2. Aprovar ou rejeitar cada insight pelo roteiro de F7.3.T1, com a categoria do motivo na rejeição.
3. Registrar o motivo quando o culto não for liberado ao pastor.
4. Avisar o pastor pelo canal combinado quando o relatório estiver liberado.

**Definição de pronto:** Para cada culto processado, nenhum insight fica pendente, e cada culto não liberado tem o motivo registrado.

**Dependências:** F7.7.T2, F7.3.T5, F7.6.T5

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F7.7.T4 · [Data Science] Acompanhar a coleta das notas do pastor em cada culto liberado</summary>

**Objetivo:** Ter, para cada culto liberado, o registro de notas dadas ou 'sem avaliação' no prazo de F6.6.

**Passos previstos:**
1. Registrar a forma e o prazo de devolução das notas definidos em F6.6.
2. Conferir no painel, com o perfil previsto na matriz de F7.2, quais insights liberados de cada culto têm nota.
3. Lembrar o pastor pelo canal combinado antes do prazo.
4. No prazo, registrar cada culto como 'com nota' ou 'sem avaliação'.

**Definição de pronto:** Cada culto liberado tem o registro 'com nota' ou 'sem avaliação' anexado ao PBI, com a data do prazo.

**Dependências:** F7.7.T3, F6.6

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F7.7.T5 · [Data Science] Extrair e consolidar no HF Jobs os dados dos 4 cultos</summary>

**Objetivo:** Ter um arquivo consolidado e reprodutível com os dados dos 4 cultos e a origem de cada valor.

**Passos previstos:**
1. Escrever um script versionado que lê o registro de execução, os indicadores de F7.6, as notas agregadas por culto, os rótulos revisados do destino dos rótulos do piloto e os critérios repetidos definidos em F6.6.
2. Anotar em cada valor o run_id ou o arquivo de origem.
3. Validar o comando com 'hf jobs run --dry-run' e, depois da aprovação de custo (P7), executar o script no HF Jobs em cpu-basic, pela imagem com digest e comando explícito (F2.4).
4. Gravar o resultado no repositório de resultados de F2.8, com o JOB_ID da extração.

**Definição de pronto:** O arquivo consolidado está no repositório de resultados, com a origem de cada valor e o JOB_ID da extração.

**Dependências:** F7.7.T4, F7.6.T2, F2.8, Aprovação de Fabio (P7), com flavor, duração e custo previstos, F7.7.T10

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F7.7.T6 · [Data Science] Comparar os resultados com o critério de conclusão de F6.6 e redigir o documento</summary>

**Objetivo:** Ter o documento de conclusão com a comparação item a item, pronto para a conferência de QA.

**Passos previstos:**
1. Montar a tabela dos 4 cultos a partir do arquivo consolidado.
2. Comparar cada item do critério de F6.6 e marcar 'atingido' ou 'não atingido'.
3. Registrar os cultos sinalizados, os não processados e os sem avaliação, com o motivo, e dizer se a falta de nota impede a conclusão segundo F6.6.
4. Redigir o texto sem termos das listas PROIBIDO e PROIBIDO_INDIVIDUAL de reacao/lint.py.

**Definição de pronto:** O documento está no repositório com a comparação completa.

**Dependências:** F7.7.T5, F6.6

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F7.7.T7 · [QA] Conferir o documento e as verificações de antes e de fim de piloto</summary>

**Objetivo:** Verificar os critérios 1 a 11 de F7.7 antes das assinaturas.

**Passos previstos:**
1. Conferir no registro de F7.7.T1 e no inventário de F2.6.T6 que a troca de digest foi feita antes do primeiro culto e que só o webhook novo ficou ativo, e no registro de F7.7.T2 que os critérios de F7.8 passaram antes do primeiro culto.
2. Recalcular os números do documento a partir das origens citadas.
3. Conferir que os 4 cultos estão presentes, com os motivos quando for o caso, e conferir as tabelas e registros de F7.7.T2, F7.7.T3 e F7.7.T4.
4. Aplicar ao texto do documento as listas PROIBIDO e PROIBIDO_INDIVIDUAL de reacao/lint.py.
5. Listar os arquivos do deployment de produção na Vercel (https://vercel.com/docs/rest-api/deployments/list-deployment-files) e conferir tipos e extensões; conferir que nenhum vídeo do piloto aparece no dataset do corpus nem em jobs-artifacts.
6. Conferir no registro de F7.7.T10 a data do fim da rotulagem de cada culto e, no registro de F2.5, que o vídeo saiu do destino depois dessa data ou no prazo máximo; conferir que nenhum rótulo do piloto aparece no dataset do corpus.
7. Comparar as refs e as tags do dataset do corpus com as registradas em F7.1.T4.
8. Conferir que nenhum culto com data anterior à vigência dos pré-requisitos tem janelas, eventos ou insights.

**Definição de pronto:** O checklist dos critérios 1 a 11 está anexado ao PBI com as evidências, e todos passaram.

**Dependências:** F7.7.T6

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F7.7.T8 · [Governança e Privacidade] Revisar o documento e registrar a decisão assinada</summary>

**Objetivo:** Deixar o documento conforme as regras 3, 4 e 6 e com a decisão assinada.

**Passos previstos:**
1. Conferir que o documento não tem número por pessoa, assento ou setor, nem percentual de janela insuficiente.
2. Conferir o resultado da conferência de QA de F7.7.T7.
3. Colher as assinaturas das pessoas definidas em F6.6, com a data.

**Definição de pronto:** A decisão está registrada no documento com data e assinaturas, e a revisão do encarregado está registrada.

**Dependências:** F7.7.T7

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F7.7.T9 · [Visão Computacional] Rotular os cultos do piloto na ferramenta de F3.3 pelo protocolo de F3.2, no prazo do plano de F6.6</summary>

**Objetivo:** Ter, para cada culto com rotulagem prevista no plano de F6.6, os rótulos de referência de rostos, quadros revisados, eventos e, se o plano pedir, momentos, no destino dos rótulos do piloto.

**Passos previstos:**
1. Para cada culto marcado 'aguardando rotulagem', abrir o vídeo na ferramenta do Space privado de F3.3 pela leitura do destino do piloto de F7.9.
2. Marcar rostos com a medida de altura de F3.2 e, se F1.3 exigir, as caixas; marcar os quadros revisados e os eventos pelos tipos de F3.2.
3. Marcar os momentos na forma e na ferramenta definidas no plano de F6.6.
4. Manter o som desligado, salvo exceção registrada no RIPD de F6.3.
5. Exportar os rótulos para o destino dos rótulos do piloto do ADR de F6.2, conferindo que nada vai ao dataset do corpus.
6. Se o prazo do plano de F6.6 ou o prazo máximo do ADR de F6.2 estiver perto de vencer, avisar Fabio e registrar o culto afetado.

**Definição de pronto:** Cada culto com rotulagem prevista tem os arquivos de rótulos no destino dos rótulos do piloto, validados pelo validador de F1.4, ou o motivo registrado de não ter sido rotulado.

**Dependências:** F7.7.T2, F7.9.T4, F3.2, F6.6

**Estimativa sugerida:** 16 h (sugestão; validar com o time)

</details>

<details><summary>F7.7.T10 · [Data Science] Revisar por amostragem os rótulos de cada culto e registrar o fim da rotulagem</summary>

**Objetivo:** Ter os rótulos de cada culto revisados pela regra de amostra do plano de F6.6 e o fim da rotulagem registrado, o que libera o apagamento do vídeo pela varredura de F7.4.T4.

**Passos previstos:**
1. Sortear a amostra de quadros e eventos de cada culto pela regra do plano de F6.6 e do protocolo de F3.2.
2. Calcular a concordância definida em F3.2 e registrar o resultado por culto, sem nome de rotulador no registro.
3. Se a concordância ficar abaixo do mínimo do protocolo, devolver o culto para correção em F7.7.T9 dentro do prazo.
4. Registrar o fim da rotulagem de cada culto, com a data, no local definido em F7.4.T1.
5. Para culto não rotulado no prazo máximo, registrar o motivo e a consequência prevista no ADR de F6.2.

**Definição de pronto:** Cada culto com rotulagem prevista tem a revisão por amostragem registrada e a data do fim da rotulagem no local de F7.4.T1, ou o motivo de não ter sido rotulado.

**Dependências:** F7.7.T9, F6.6, F7.4.T1

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- feature_F7.json (árvore v1), PBI F7.7
- epico.json (escopo do piloto: perfis pastor, mídia e DPO)
- feature_F5_v3.json (F5.4.T3, padrão de publicação por tag de release)
- huggingface_hub/hf_api.py:11378-11386,11520,11573 (update_webhook sem job_id, disable_webhook e delete_webhook)
- huggingface_hub/hf_api.py:13006-13043,13246,13378 (create_scheduled_job, suspend, delete_scheduled_job e update_scheduled_job_labels)
- README.pt-BR.md:21,35-36
- reacao/lint.py:8-13,23-49
- CLAUDE.md regras 3 e 4
- https://vercel.com/docs/rest-api/deployments/list-deployment-files
- premissas P7 e P3 revisada
- feature_det_F6.json (F6.2 RN08 e F6.2.T1; F6.6 RN03, RN10, RN11 e F6.6.T2)
- feature_det_F3.json (F3.2 e F3.3)

#### Verificação INVEST: pontos que falharam
- Small: a operação acompanha os 4 cultos e dura pelo menos o período entre o primeiro e o último culto, que pode passar de uma sprint (P6).
- Estimável: o esforço da consolidação depende do critério de conclusão de F6.6, que ainda não foi escrito.
- Small: tem 12 critérios de aceite, acima do sinal de ~10 do taskflow.md §1, porque as revisões acrescentaram a verificação de antes do primeiro culto e a rotulagem. A divisão entre operação, rotulagem e consolidação, ou a Feature própria citada nas premissas da Feature, fica para o refinamento.

#### Premissas
- A operação dos 4 cultos entrou neste PBI para que o critério principal da Feature tenha trabalho que o produza. A alternativa era um PBI de operação, que levaria F7 a 9 PBIs.
- A disciplina MLOps entrou neste PBI: disparar e acompanhar os jobs e registrar JOB_ID e run_id é trabalho de jobs e de registro de execução pela regra de disciplinas.
- A disciplina DevOps entrou neste PBI (revisão): publicar a imagem de release e recriar o Job de origem, o webhook e o Job agendado é trabalho de imagem e de HF Jobs pela regra de disciplinas.
- A revisão e a liberação por culto ficam em Governança e Privacidade porque o roteiro de F7.3.T1 confere linguagem controlada e referência a pessoa ou setor. Quem ocupa o perfil revisor está pendente.
- O prazo de coleta das notas vem de F6.6. Se F6.6 não o definir, F7.7.T4 o propõe e quem assina F6.6 aprova.
- O documento é de consolidação e decisão. Além da conferência de QA, ele passa pela revisão do encarregado.
- Os disparos, a revisão e a coleta de notas acompanham o calendário dos cultos, cujas datas não estão registradas.
- Revisão aplicada: a nova task de publicação da imagem entrou como F7.7.T1, e as antigas F7.7.T1 a F7.7.T7 passaram a F7.7.T2 a F7.7.T8. Os IDs F6.2.T3 e F6.2.T4 vêm da revisão; a árvore não tem tasks.
- Revisão aplicada: F7.8 entrou nas dependências, em vez de registrar em F7.2.T1 que a matriz dispensa as telas de mídia e DPO no piloto, porque o escopo do épico põe esses perfis no piloto.
- Revisão aplicada: a rotulagem dos cultos do piloto entrou como F7.7.T9 [Visão Computacional] e F7.7.T10 [Data Science], numeradas no fim para não mudar as referências a F7.7.T1 a F7.7.T8; elas rodam depois de F7.7.T2 e antes de F7.7.T5. A disciplina Visão Computacional entrou porque é a que rotula no corpus (F3.4).
- F7.7.T9 tem 16 h sugeridas para os 4 cultos; o volume depende dos rótulos por culto do plano de F6.6, ainda não escrito. Se passar de 16 h, a task se divide por culto.
- A revisão cita 'antes de F7.7.T4'; na numeração atual, a extração é F7.7.T5, que passa a depender de F7.7.T10.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Vínculo com a Feature F7
- Datas dos 4 cultos do piloto
- Quem ocupa o perfil revisor
- Aprovação de custo do processamento dos 4 cultos, da extração e do Job de origem e do Job agendado recriados em F7.7.T1
- Nomes de quem assina a decisão, conforme F6.6
- Nomes dos rotuladores do piloto e lista de acesso, conforme o plano de F6.6
- Atualização aprovada de README.pt-BR.md:16-17, se o vídeo ficar no destino até o fim da rotulagem

## Preview — PBI F7.8 (novo) · Dar aos perfis mídia e DPO acesso às telas do painel web na Vercel definidas na matriz de acesso do piloto

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Dar aos perfis mídia e DPO acesso às telas do painel web na Vercel definidas na matriz de acesso do piloto |
| Tipo | Product Backlog Item |
| Pai | F7 |
| Tags | Fase 1; piloto; Supabase; RLS; Vercel; privacidade |
| Estimativa | 5 pts (sugestão); tasks: 18 h |
| Dependências | F7.2 (matriz aprovada em T1, mecanismo do perfil e políticas em T3, seed no CI com Supabase local em T4, guarda de rotas em T6 e teste de políticas em T7), F5.6 (arquivo de textos fixos em F5.6.T1 e verificação de lint em F5.6.T5), F2.4.T4 (D7: local do vínculo entre conta e perfil), confirmado ou ajustado por F6.2 |
| Substitui | PBI-041, PBI-057 |

#### Descrição

Como encarregado de dados (DPO) do piloto  
Quero que as contas dos perfis mídia e DPO entrem no painel web e vejam só as telas e os dados que a matriz de acesso aprovada lhes dá  
Para que a equipe de mídia e o encarregado acompanhem o piloto sem acesso além do que a matriz permite

**Contexto:** Os perfis midia e dpo estão no comentário da migração (supabase/migrations/0001_init.sql:21). O envio dos vídeos pela equipe de mídia é feito no HF, sem passar pela Vercel (F7.1; P3 revisada), e nenhuma fonte define o que mídia e DPO veem no painel. O conteúdo das telas sai da matriz de acesso de F7.2.T1. A matriz, o mecanismo do perfil no token, a seed no CI com Supabase local, a guarda de rotas e o teste de políticas estão em F7.2. Pela P3 revisada, o painel lê só agregados, eventos e insights, com exceções aprovadas na matriz (F7.2 RN03), e transcript_segment guarda a transcrição (0001_init.sql:13).

**Regras de negócio:**
- RN01 – Os perfis midia e dpo leem e escrevem só o que a matriz aprovada em F7.2.T1 permite.
- RN02 – Valem as regras de tabelas do painel de F7.2 RN03, que seguem D7 de F2.4.T4: transcript_segment e run_log sem leitura, e cada tabela fora da lista de D7 só com exceção aprovada.
- RN03 – O painel não recebe vídeo; o envio da equipe de mídia continua no HF (F7.1; P3 revisada).
- RN04 – Janela marcada como insuficiente aparece sem percentual (CLAUDE.md regra 3; reacao/aggregate.py:26-31).
- RN05 – Os textos fixos das telas ficam no arquivo de textos de F5.6.T1, lido pela verificação de lint de F5.6.T5 (CLAUDE.md regra 4).
- RN06 – 'Tabelas do Supabase não têm campo por pessoa' (CLAUDE.md regra 6). O perfil fica no local decidido em D7 de F2.4.T4 e confirmado ou ajustado por F6.2, como em F7.2.

**Fora de escopo:**
- Envio de vídeo pelo painel (F7.1)
- Perfis pastor e revisor (F7.2)
- Definição da matriz de acesso (F7.2.T1)
- Configuração da Vercel e do CI (F7.2 e F2.6.T4)

#### Critérios de aceite

- O teste automatizado de políticas confere cada linha da matriz para midia e dpo e passa no CI contra o Supabase local.
- Uma conta midia e uma conta dpo entram com a própria conta e veem só as telas do seu perfil. O endereço direto de uma tela de outro perfil mostra acesso negado.
- Com a sessão de uma conta midia ou dpo, uma consulta direta a transcript_segment retorna zero linhas ou acesso negado.
- Nenhuma tela dos perfis mídia e DPO tem campo de envio de arquivo.
- Uma janela marcada como insuficiente, inclusive uma com n_mensuravel=10 e insuficiente=true, aparece sem percentual nas telas dos dois perfis.
- Os textos fixos das telas estão no arquivo lido pela verificação de lint de F5.6.T5, e a verificação passa.
- tests/test_schema.py continua passando depois das migrações.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F7.8.T1 | Backend | Levar os perfis midia e dpo ao token e escrever as políticas de RLS desses perfis | 5 | F7.2.T1, F7.2.T3 |
| F7.8.T2 | Front end | Implementar as telas dos perfis mídia e DPO conforme a matriz | 8 | F7.8.T1, F7.2.T6 |
| F7.8.T3 | QA | Verificar os critérios de F7.8 | 5 | F7.8.T2, F7.2.T7 |

<details><summary>F7.8.T1 · [Backend] Levar os perfis midia e dpo ao token e escrever as políticas de RLS desses perfis</summary>

**Objetivo:** Fazer o banco impor a matriz aprovada para os perfis midia e dpo.

**Passos previstos:**
1. Estender o mecanismo de F7.2.T3 com os perfis midia e dpo, no local decidido em D7 de F2.4.T4 e confirmado ou ajustado por F6.2.
2. Escrever as políticas por tabela e operação conforme a matriz de F7.2.T1, sem leitura de transcript_segment.
3. Acrescentar à seed local uma conta de teste por perfil.
4. Rodar tests/test_schema.py e ruff.

**Definição de pronto:** As migrações estão aplicadas no Supabase local e no projeto de desenvolvimento, o token de cada conta de teste contém o perfil, e ruff e pytest passam.

**Dependências:** F7.2.T1, F7.2.T3

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F7.8.T2 · [Front end] Implementar as telas dos perfis mídia e DPO conforme a matriz</summary>

**Objetivo:** Entregar as telas de mídia e DPO com os dados que a matriz permite.

**Passos previstos:**
1. Implementar as telas definidas na matriz de F7.2.T1 para cada perfil, com a guarda de rotas de F7.2.T6.
2. Não oferecer envio de arquivo em nenhuma tela.
3. Mostrar sem percentual a janela com insuficiente=true.
4. Pôr os textos fixos no arquivo de textos de F5.6.T1, lido pela verificação de lint de F5.6.T5.

**Definição de pronto:** Num preview com as contas de teste, cada perfil vê só as telas dele, e a verificação de lint passa.

**Dependências:** F7.8.T1, F7.2.T6

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F7.8.T3 · [QA] Verificar os critérios de F7.8</summary>

**Objetivo:** Conferir no banco e no painel que mídia e DPO só acessam o que a matriz permite.

**Passos previstos:**
1. Ampliar o teste de políticas de F7.2.T7 com as linhas da matriz para midia e dpo e o caso de transcript_segment.
2. Entrar com cada conta de teste e conferir telas, rotas por endereço direto e ausência de envio de arquivo.
3. Conferir que uma janela com n_mensuravel=10 e insuficiente=true aparece sem percentual.
4. Rodar tests/test_schema.py e a verificação de lint de F5.6.T5.

**Definição de pronto:** O teste ampliado passa no CI, e o checklist dos critérios está anexado ao PBI com as evidências, com todos passando.

**Dependências:** F7.8.T2, F7.2.T7

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- Divisão de F7.2 nesta revisão da árvore
- supabase/migrations/0001_init.sql:13,21
- reacao/aggregate.py:26-31
- taskflow.md §1 e §2
- premissas P17 e P3 revisada

#### Verificação INVEST: pontos que falharam
- Estimável: o conteúdo das telas depende da matriz de F7.2.T1, ainda não aprovada.

#### Premissas
- Este PBI saiu da divisão de F7.2 (taskflow.md §1: mais de um usuário-alvo e critérios acima de ~10; §2: mais de 7 filhos).
- As disciplinas vêm das previstas para F7.2 na árvore. Governança e Privacidade e DevOps não entram porque a matriz (F7.2.T1), a configuração da Vercel (F7.2.T5) e a seed no CI (F7.2.T4) ficam em F7.2.
- Nenhuma fonte define o que mídia e DPO veem no painel. Os story points e as horas de F7.8.T2 são provisórios e devem ser reestimados depois de F7.2.T1.
- PBI-041 e PBI-057 viraram um único PBI (P17), agora dividido em F7.2 e F7.8.
- F7.7.T2 depende de F7.8.T3, porque o escopo do épico põe os perfis mídia e DPO no piloto (epico.json).

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Vínculo com a Feature F7
- Quem recebe os perfis midia e dpo
- Reestimativa depois de F7.2.T1

## Preview — PBI F7.9 (novo) · Dar aos rotuladores do piloto a leitura dos vídeos do destino do piloto na ferramenta de rotulagem de F3.3, com os rótulos fora do corpus

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Dar aos rotuladores do piloto a leitura dos vídeos do destino do piloto na ferramenta de rotulagem de F3.3, com os rótulos fora do corpus |
| Tipo | Product Backlog Item |
| Pai | F7 |
| Tags | Fase 1; piloto; rotulagem; HF; privacidade |
| Estimativa | 5 pts (sugestão); tasks: 21 h |
| Dependências | F3.3 (ferramenta e Space privado com lista de acesso), F3.2 (protocolo de rotulagem), F7.1 (tipo de destino em T1 e destino criado em T2), F6.2 (destino dos rótulos do piloto e regra de apagamento depois da rotulagem), F6.6 (rótulos previstos, lista de rotuladores e forma de marcar momentos), F6.3 (rótulos e rotuladores no inventário do RIPD), F2.4.T4 (D6: acesso no HF de rotuladores), F2.6.T6 (inventário de credenciais), F1.1 (guarda e limpeza de /dev/shm) |
| Substitui | nenhum |

#### Descrição

Como rotulador dos cultos do piloto, na lista de acesso definida no plano de F6.6  
Quero abrir na ferramenta do Space privado de F3.3 o vídeo de um culto do piloto direto do destino de F7.1 e exportar os rótulos para o destino dos rótulos do piloto  
Para fazer os rótulos de referência que o plano de F6.6 exige antes de o vídeo ser apagado, sem copiar vídeo nem rótulo do piloto para o dataset do corpus

**Contexto:** A ferramenta de F3.3 roda num Space privado com acesso restrito à lista de rotuladores, lê em memória os quadros amostrados e exporta _faces.csv e _eventos.csv (feature_det_F3.json, F3.3.T2 a F3.3.T4). Ela lê clipes do dataset do corpus por tag (F3.5), e nenhuma task de F3 prevê a leitura do destino do piloto; F3 registra que os vídeos do piloto vão para o destino de F7.1 (feature_det_F3.json, RN06). O plano de F6.6 prevê rótulos de referência dos cultos do piloto feitos nessa ferramenta, sem som, com a forma de marcar momentos definida no plano (feature_det_F6.json, F6.6 RN03 e F6.6.T2). O ADR de F6.2 decide o destino dos rótulos do piloto, fora do corpus, e mantém o vídeo no destino até o fim da rotulagem (F6.2 RN08 e RN10; F6.2.T8). resolve_video só trata caminhos hf://datasets/ (processar_culto.py:24), e o destino de F7.1 pode ser Storage Bucket ou repositório de dataset (F7.1.T1). Pela P3 revisada, ferramentas que exibem vídeo ficam no HF.

**Regras de negócio:**
- RN01 – A ferramenta lê o vídeo do piloto só em memória ou em /dev/shm, sem gravar quadro, recorte nem vídeo fora de /dev/shm (CLAUDE.md regra 1; reacao/guard.py).
- RN02 – A ferramenta não carrega modelo de reconhecimento facial nem guarda id por rosto (CLAUDE.md regra 2).
- RN03 – A rotulagem dos cultos do piloto não usa som, salvo exceção aprovada pelo encarregado e registrada no RIPD de F6.3 (CLAUDE.md regra 5; F6.6 RN03).
- RN04 – Os rótulos do piloto vão ao destino decidido no ADR de F6.2, fora do dataset do corpus (F6.2.T8).
- RN05 – Só as contas da lista de rotuladores do piloto do plano de F6.6 abrem a ferramenta com vídeos do piloto, pelo modelo de acesso de D6 de F2.4.T4.
- RN06 – O token do Space para o piloto lê só o destino de F7.1 e escreve só no destino dos rótulos do piloto; fica no inventário de F2.6.T6, sem o valor.
- RN07 – Antes de F6.3 e F6.4, só vídeo público de teste entra no destino para os testes deste PBI.

**Fora de escopo:**
- Construção da ferramenta de rotulagem (F3.3) e protocolo (F3.2)
- Execução da rotulagem e da revisão dos 4 cultos (F7.7.T9 e F7.7.T10)
- Regra de apagamento dos vídeos e destino dos rótulos do piloto (F6.2)
- Envio do vídeo (F7.1) e apagamento pela varredura (F7.4)
- Qualquer tela na Vercel com vídeo ou quadro (P3 revisada)

#### Critérios de aceite

- Com uma conta da lista de rotuladores do piloto, um vídeo público de teste posto no destino do piloto abre na ferramenta, e a marcação de rostos, quadros revisados e eventos funciona como em F3.3.
- Uma conta fora da lista recebe acesso negado no Space.
- Os rótulos exportados aparecem no destino dos rótulos do piloto do ADR de F6.2, e nenhum arquivo do teste aparece no dataset do corpus.
- Depois de uma sessão de rotulagem, a verificação de reacao/guard.py não encontra quadro, recorte nem vídeo fora de /dev/shm.
- A ferramenta não reproduz o áudio do vídeo do piloto, salvo exceção registrada no RIPD.
- O token do Space para o piloto não lê o dataset do corpus e não escreve no destino dos vídeos; o inventário de F2.6.T6 o lista com escopo, dono e validade, sem o valor.
- Se o plano de F6.6 marcar momentos na ferramenta, a marcação funciona com o vídeo de teste; se o plano usar outra ferramenta, o PBI registra qual.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F7.9.T1 | Visão Computacional | Acrescentar à ferramenta de F3.3 a leitura em memória dos vídeos do destino do piloto e a exportação para o destino dos rótulos do piloto | 8 | F3.3, F7.1.T1, F7.1.T2, F6.2.T2, F1.1 |
| F7.9.T2 | DevOps | Cadastrar no Space o token do piloto de escopo mínimo e aplicar a lista de rotuladores do piloto | 3 | F7.9.T1, F3.3.T6, F2.6.T6, F6.6.T2, F2.4.T4 (D6) |
| F7.9.T3 | Front end | Acrescentar à ferramenta a marcação de momentos, se o plano de F6.6 a puser na ferramenta | 5 | F7.9.T1, F6.6.T2 |
| F7.9.T4 | QA | Verificar os critérios de F7.9 com vídeo público de teste | 5 | F7.9.T2, F7.9.T3 |

<details><summary>F7.9.T1 · [Visão Computacional] Acrescentar à ferramenta de F3.3 a leitura em memória dos vídeos do destino do piloto e a exportação para o destino dos rótulos do piloto</summary>

**Objetivo:** Fazer a ferramenta abrir um vídeo do destino de F7.1 com a mesma leitura em memória de F3.3.T2 e gravar os rótulos no destino do ADR de F6.2.

**Passos previstos:**
1. Ler o tipo de destino decidido em F7.1.T1 e o destino dos rótulos do piloto do ADR de F6.2.
2. Acrescentar a origem 'destino do piloto' à leitura de F3.3.T2, por caminho do Hub, para memória ou /dev/shm, sem cópia no dataset do corpus.
3. Gravar a exportação de _faces.csv e _eventos.csv do piloto no destino dos rótulos do piloto, e não na pasta do corpus.
4. Desligar a reprodução de áudio para vídeos do piloto, salvo exceção registrada no RIPD.
5. Escrever testes com leitura e gravação simuladas e rodar a guarda de reacao/guard.py.

**Definição de pronto:** Os testes passam, a guarda não encontra resíduo fora de /dev/shm, e ruff e pytest passam.

**Dependências:** F3.3, F7.1.T1, F7.1.T2, F6.2.T2, F1.1

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F7.9.T2 · [DevOps] Cadastrar no Space o token do piloto de escopo mínimo e aplicar a lista de rotuladores do piloto</summary>

**Objetivo:** Deixar o Space com um token que lê só o destino do piloto e escreve só no destino dos rótulos do piloto, e com o acesso restrito aos rotuladores do piloto.

**Passos previstos:**
1. Criar o token com o escopo possível registrado em F7.1.T1: leitura no destino dos vídeos e escrita no destino dos rótulos do piloto.
2. Cadastrar o token como segredo do Space, separado do token de leitura do corpus de F3.3.
3. Aplicar ao Space a lista de rotuladores do piloto do plano de F6.6, pelo modelo de acesso de D6 de F2.4.T4.
4. Registrar o token no inventário de F2.6.T6 com escopo, dono, validade e rotação, sem o valor.

**Definição de pronto:** O token está cadastrado no Space, a lista de acesso está aplicada e o inventário de F2.6.T6 está atualizado.

**Dependências:** F7.9.T1, F3.3.T6, F2.6.T6, F6.6.T2, F2.4.T4 (D6)

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F7.9.T3 · [Front end] Acrescentar à ferramenta a marcação de momentos, se o plano de F6.6 a puser na ferramenta</summary>

**Objetivo:** Permitir marcar os momentos dos cultos do piloto na forma definida no plano de F6.6, ou registrar a ferramenta que o plano usa.

**Passos previstos:**
1. Ler no plano de F6.6 a forma e a ferramenta de marcação de momentos.
2. Se for a ferramenta de F3.3, acrescentar a marcação de momento com início, fim e nome e a exportação no destino dos rótulos do piloto.
3. Se for outra ferramenta, registrar qual no PBI e encerrar a task.
4. Escrever testes da marcação e da exportação.

**Definição de pronto:** A marcação de momentos funciona com testes passando, ou o PBI registra a ferramenta que o plano usa.

**Dependências:** F7.9.T1, F6.6.T2

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F7.9.T4 · [QA] Verificar os critérios de F7.9 com vídeo público de teste</summary>

**Objetivo:** Conferir os critérios de F7.9 antes do primeiro culto real.

**Passos previstos:**
1. Pôr um vídeo público de teste no destino do piloto pela credencial de F7.1.
2. Com uma conta da lista, abrir o vídeo, marcar rostos, quadros revisados, eventos e, se for o caso, momentos, e exportar.
3. Conferir os rótulos no destino dos rótulos do piloto e que nada apareceu no dataset do corpus.
4. Com uma conta fora da lista, conferir o acesso negado.
5. Conferir que não há áudio e que a guarda não encontra resíduo fora de /dev/shm.
6. Tentar ler o corpus e escrever no destino dos vídeos com o token do piloto; o esperado é recusa. Conferir o inventário de F2.6.T6.
7. Remover o vídeo e os rótulos de teste e anexar as evidências sem o valor do token.

**Definição de pronto:** As evidências de cada critério estão anexadas ao PBI, e todos passaram.

**Dependências:** F7.9.T2, F7.9.T3

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- consolidacao.json, problema 'F6.6 (F6.6.T2) → F7'
- feature_det_F3.json (F3.3 e RN06)
- feature_det_F6.json (F6.2 RN08, RN10, F6.2.T1, F6.2.T8; F6.6 RN03, RN11, F6.6.T2)
- feature_det_F2.json (F2.4.T4, D6)
- processar_culto.py:24
- CLAUDE.md regras 1, 2 e 5
- P3 revisada

#### Verificação INVEST: pontos que falharam
- Independente: depende do plano de F6.6 (rótulos e forma de marcar momentos) e do ADR de F6.2 (destino dos rótulos), ainda não escritos.

#### Premissas
- PBI novo desta reconciliação: F6 deixou em pendência a leitura do destino do piloto 'em F3.3 ou F7.1.T1', e F3 não a incluiu. Ficou em F7 porque depende do destino de F7.1 e do ADR de F6.2, que são da Fase 1.
- Não foi verificado se um token fine-grained pode ficar restrito a um bucket; F7.1.T1 verifica. Se não puder, o acesso segue a alternativa registrada em F7.1.T1.
- Não foi verificado se o Space de F3.3 usa hardware pago. Se usar, a aprovação da P7 vale para as horas de rotulagem do piloto.
- Os testes usam vídeo público com download permitido; culto real só em F7.7.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Vínculo com a Feature F7
- PBI novo F7.9 no índice de PBIs e na árvore
- Nomes dos rotuladores do piloto (plano de F6.6)
- F3.3: registrar que F7.9 estende a ferramenta para o destino do piloto
