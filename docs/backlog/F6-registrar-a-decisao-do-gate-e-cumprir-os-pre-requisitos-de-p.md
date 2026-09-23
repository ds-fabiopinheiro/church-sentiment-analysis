[Voltar ao épico](README.md)

# Preview — Feature F6 (novo) · Registrar a decisão do gate e cumprir os pré-requisitos de privacidade e de medição da Fase 1

### Campos
| Campo | Conteúdo |
|---|---|
| Título | Registrar a decisão do gate e cumprir os pré-requisitos de privacidade e de medição da Fase 1 |
| Tipo | Feature |
| Pai | Epic |
| Tags | fase-0; fase-1; gate; privacidade; lgpd; ripd; medicao; vercel |
| Estimativa | 42 pts / 140 h (soma dos PBIs, sugestão) |

### Descrição

**Problema:** A coluna Resultado, a decisão, a data e as assinaturas do gate estão em branco (docs/poc-gate.md:6-14,50). O README exige RIPD e aviso à congregação antes da Fase 1 (README.pt-BR.md:35), e nenhum dos dois existe. Também não há docs/law/ (CONTRIBUTING.md:12). Nenhum item confirma a igreja do piloto, que é dedução (P14), nem identifica o controlador do tratamento da Fase 1. Pela LGPD, o RIPD é 'documentação do controlador' (art. 5º, XVII), o operador trata segundo as instruções do controlador (art. 39) e o controlador indica o encarregado (art. 41) (https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm). A transcrição é feita da trilha inteira do arquivo, sem separar quem fala (reacao/transcribe.py:13), e vai inteira para transcript_segment (supabase/migrations/0001_init.sql:13; processar_culto.py:88-89). Com --stdout, trechos vão para os logs do job (processar_culto.py:109-115), que continuam disponíveis depois do fim do job (https://huggingface.co/docs/hub/jobs-manage). Três campos texto podem guardar nome de pessoa: service.pregador, insight.revisado_por e insight_feedback.avaliador (0001_init.sql:4,16,17). Pela P12, avaliador guarda código de papel até F6.2. Nenhum deles é coberto por tests/test_schema.py:5. pct_olhos_fechados existe no schema e sai sempre nulo, porque nenhum provider preenche eyes_closed (0001_init.sql:9; reacao/aggregate.py:38,42). A retenção existe só como comentário (0001_init.sql:20). Num repositório Git do Hub, apagar um arquivo não o tira do histórico (https://huggingface.co/docs/hub/storage-buckets). Para dado sensível, a LGPD (art. 11) restringe as hipóteses sem consentimento, e nenhum item prevê como coletar consentimento ou atender oposição sem identificar a pessoa. O repositório do projeto é público (https://api.github.com/repos/ds-fabiopinheiro/church-sentiment-analysis, visibility public, consulta de 2026-09-23), e nenhum item decide onde ficam os documentos com dado da igreja do piloto. Pela P3 revisada, o front end do produto passa a ser um painel web num projeto novo na Vercel, o que acrescenta um operador de dados. Em projetos novos, as funções da Vercel rodam por padrão em iad1, Washington, EUA (https://vercel.com/docs/functions/configuring-functions/region), e os logs de execução guardam a saída de console das funções (https://vercel.com/docs/logs/runtime). Não há critério de conclusão da Fase 1 nem limites de qualidade por culto. O plano de medição da Fase 1 prevê rótulos de referência dos cultos do piloto, feitos na ferramenta do Space de F3.3, que exibe o vídeo; a regra de apagamento dos vídeos do piloto prevista em F6.2 não condiciona o apagamento ao fim dessa rotulagem, nenhum item decide onde ficam os rótulos do piloto e nenhum item de F7 executa a rotulagem (arvore_v1.json, F7).

**Solução proposta:** Preencher o gate com os resultados rastreáveis e registrar a decisão assinada. Se a decisão for seguir: registrar em ADR as decisões de minimização, o prazo de retenção de cada item do inventário, a regra de apagamento dos vídeos do piloto, que mantém o vídeo de cada culto até o fim da rotulagem prevista no plano, o destino dos rótulos do piloto e o local privado dos documentos com dado da igreja do piloto, e aplicá-las ao schema, aos logs dos jobs e do painel web na Vercel, às tabelas que o painel lê e ao dataset; confirmar com a igreja indicada a participação no piloto, o controlador e o encarregado, com o instrumento de papéis e instruções de tratamento assinado pela igreja e por Fabio Pinheiro; elaborar o RIPD a partir disso, com a Vercel entre os operadores e a lista das pendências que impedem o piloto; definir uma forma de oposição ou de consentimento sem identificação, se a base legal pedir; redigir e publicar o aviso; e assinar o plano de medição da Fase 1 antes do primeiro culto do piloto, com o prazo da rotulagem de cada culto dentro da retenção dos vídeos. Cada registro fica datado no lugar que F7.5 consulta.

**Usuários impactados:** Fabio Pinheiro, Pastor Filipe, Encarregado de dados, DPO (perfil previsto em supabase/migrations/0001_init.sql:21; nomeação em F3.1.T2, ainda sem nome), Controlador do tratamento da Fase 1 (LGPD art. 5º, VI; a identificar em F6.3.T8), Congregação da igreja do piloto, Pastor da igreja do piloto, Equipe de mídia da igreja do piloto (perfil 'midia' previsto em supabase/migrations/0001_init.sql:21; envio do vídeo em F7.1), Rotuladores dos cultos do piloto (acesso ao vídeo pelo Space privado de F3.3)

**Valor de negócio:** Sem a decisão assinada, as medições da Fase 0 não se tornam decisão registrada (docs/poc-gate.md:50). Sem RIPD e sem aviso, o README impede a Fase 1 (README.pt-BR.md:35). Esta Feature transforma os seis critérios medidos numa decisão com origem rastreável. Se a decisão for seguir, ela libera o piloto com uma igreja e 4 cultos, com a igreja e o controlador confirmados, base legal, operadores, aviso, forma de oposição (se exigida), pendências impeditivas resolvidas e critério de conclusão registrados antes do primeiro culto. Também deixa explícito o que o painel web na Vercel pode ler e guardar, onde ficam os documentos e os rótulos do piloto, já que o repositório é público, e por quanto tempo o vídeo de cada culto fica disponível para a rotulagem que o plano exige.

**Regras de negócio:**
- RN01 – F6.2 a F6.6 só começam se a decisão registrada em F6.1 for 'seguir para dados da PIB e RIPD' (docs/poc-gate.md:50; P23).
- RN02 – A decisão do gate só é registrada com cada critério acompanhado da origem aceita para o seu tipo e com as assinaturas de Fabio Pinheiro e do pastor Filipe (docs/poc-gate.md:50).
- RN03 – Nenhum culto do piloto é processado antes do RIPD, do aviso publicado, da forma de oposição ou consentimento (se acionada), do plano de medição assinado e do registro de resolução de cada pendência que o RIPD marcou como impeditiva, todos com data anterior ao culto (README.pt-BR.md:35; F7.5).
- RN04 – Nenhuma decisão desta Feature cria identificação, embedding ou rastreamento entre quadros (CLAUDE.md, regra 2). 'Tabelas do Supabase não têm campo por pessoa' (CLAUDE.md, regra 6), o que vale para campos da congregação e da equipe, como revisado_por e avaliador. A leitura da regra 6 para as contas da equipe e o local do vínculo entre conta e papel são decididos em D7 de F2.4.T4, antes de F5.6; o ADR de F6.2 confirma ou ajusta essa decisão, e qualquer leitura diferente da regra 6 fica registrada nele, com a aprovação de Fabio Pinheiro e do encarregado.
- RN05 – O painel web na Vercel lê só agregados, eventos e insights do Supabase, com Supabase Auth, chave pública e RLS por perfil. A chave de serviço fica só nos jobs do HF, e a Vercel não recebe vídeo, quadro, recorte de rosto nem observação por rosto (P3 revisada).
- RN06 – Ferramentas que exibem ou recebem vídeo ou quadro ficam no Hugging Face: a rotulagem dos cultos do piloto usa o Space privado de F3.3 (P3 revisada).
- RN07 – O aviso à congregação passa pela checagem das listas de termos proibidos do lint (CLAUDE.md, regra 4; valor observável de F6.4 na árvore). Cada termo apontado é removido ou entra como exceção aprovada pelo encarregado. Só podem ser exceção frases que negam um tratamento (garantias de README.pt-BR.md:16-21) e a descrição da forma de F6.5.
- RN08 – A forma de oposição ou consentimento não pode exigir identificação da pessoa (CLAUDE.md, regra 2).
- RN09 – Se F6.2 decidir medir olhos fechados, a medida entra como PBI novo em F4, com rótulo e bench. Esta Feature só retira a coluna ou registra a abertura desse PBI.
- RN10 – Documentos com dado da igreja do piloto ou nome de pessoa da igreja (RIPD, registro da igreja e do controlador, instrumento de instruções de tratamento, aprovações, registro de publicação do aviso, registro de F6.5 e plano da Fase 1) ficam no local privado decidido no ADR de F6.2, porque o repositório do projeto é público. No repositório público fica só o que não traz esses dados, como docs/law/br.md e o ADR de minimização.
- RN11 – O RIPD só é aprovado, e o aviso e a forma de F6.5 só são redigidos, depois que F6.3.T8 registrar a igreja do piloto, o controlador, o operador e o encarregado da Fase 1 e o instrumento entre a igreja e Fabio Pinheiro, com os papéis e as instruções de tratamento, estiver assinado pelas duas partes (LGPD art. 5º, VI, VII e XVII; art. 39; art. 41).
- RN12 – O vídeo de um culto do piloto só é apagado depois que a rotulagem prevista para ele no plano de F6.6 terminar, e nunca depois do prazo máximo de retenção fixado no ADR de F6.2. Os rótulos do piloto ficam no destino que o ADR decidir, fora do dataset do corpus.

**Fora de escopo:**
- Base legal e RIPD da produção on-premises (docs/onprem.md:68)
- Notas de lei de outros países além do Brasil (README.pt-BR.md:39)
- Medição de olhos fechados, que entra como PBI novo só se F6.2 decidir implementá-la
- Implementação do job de retenção (F7.4), das políticas de RLS por perfil (F7.2) e do destino dos vídeos do piloto (F7.1)
- Contratação de plano ou assinatura de DPA com os operadores de nuvem (Hugging Face, Supabase, Vercel e, se usada, Anthropic); o RIPD registra a situação e marca se ela impede o piloto. O instrumento entre a igreja do piloto e Fabio Pinheiro está no escopo (F6.3.T8)
- Configuração da região das funções do painel na Vercel; o RIPD registra a região que estiver em vigor
- Execução da rotulagem dos cultos do piloto (item de F7 a criar, pendência), consolidação dos 4 cultos (F7.7) e adaptação da ferramenta de F3.3 ao destino de F7.1
- Ajuste do apagamento do vídeo ao fim do job (F7.5) e registro dos rótulos do piloto no job de retenção (F7.4); esta Feature fixa a regra no ADR de F6.2
- Bloqueio do processamento de um culto sem os pré-requisitos, que é critério de F7.5; esta Feature entrega os registros datados no lugar que F7.5 consulta

**Dependências técnicas:**
- Resultados com linhagem no repositório privado de resultados (F2.8, com o run_id de F2.5), bench do motor escolhido (F4.6), comparador de fronteiras (F5.5), critério 5 em T4 (F5.4 e, se acionado, F5.3), notas do critério 4 registradas no painel web na Vercel (F5.7), CI com o caminho real de detecção e recorte (F1.1, F1.6) e regras de leitura e forma de assinatura pré-registradas (F1.3)
- Painel web na Vercel (F5.6), num projeto novo no time 'Fabio Pinheiro's projects', com Supabase Auth e chave pública
- Projeto Supabase de desenvolvimento com as migrações aplicadas (F2.6) e teste de contrato entre run_log e migração (F1.5)
- Decisão D7 do ADR 0002 (F2.4.T4): local do vínculo entre conta e papel, leitura da regra 6 para as contas da equipe e lista das tabelas que o painel lê e escreve, que F6.2 confirma ou ajusta
- Supabase local (supabase start) para aplicar as migrações em ordem num banco limpo sem mexer no projeto de F2.6 (https://supabase.com/docs/guides/local-development)
- Dataset privado ds-fabiopinheiro/reacao-poc-corpus e destino dos vídeos do piloto (F7.1)
- Lint ampliado (F1.7) para checar o aviso
- Ferramenta de rotulagem no Space privado (F3.3) e protocolo de F3.2 para os rótulos de referência dos cultos do piloto
- Item de F7 que executa a rotulagem dos cultos do piloto e a revisão por amostragem dos rótulos (F7.7 ou PBI novo; pendência)
- Encarregado de dados nomeado em F3.1.T2 (LGPD art. 41; feature_F3_v3.json); F6.3.T8 confirma se ele atende ao piloto
- Indicação da igreja do piloto pelo pastor Filipe (dependência do épico, epico.json) e um representante da igreja disponível para assinar o instrumento de F6.3.T8
- Plano e termos de uso da Vercel para o projeto do painel, confirmados na primeira task de F5.6 (movida de F7.2.T2; pendência de F5) e registrados como pendência em D8 de F2.4.T4; F7.2.T2 só os reconfirma para dados da igreja do piloto

**Riscos:**
- O encarregado é nomeado em F3.1.T2, ainda sem data. Se o controlador da Fase 1 for outro, cabe a ele indicar o encarregado do piloto (LGPD art. 41). Sem encarregado, não há aprovação do ADR de F6.2, do RIPD, das exceções do aviso nem de F6.5.
- Se a igreja indicada não confirmar a participação ou não assinar o instrumento de papéis e instruções de tratamento, o RIPD não é aprovado e o piloto não começa.
- Se a base legal do RIPD exigir consentimento ou oposição e nenhuma forma compatível com a regra 2 atender à hipótese ou for aceita pela igreja, o piloto não começa.
- O DPA da Vercel se aplica a clientes Pro e Enterprise e prevê transferência para os EUA. Ele define as leis aplicáveis como todas as leis de privacidade aplicáveis e lista como exemplos GDPR, UK DPA 2018, CCPA, PIPEDA e a lei australiana, sem citar a LGPD (https://vercel.com/legal/dpa, leitura de 2026-09-23). Cabe ao encarregado avaliar se isso basta para o art. 33. O plano do projeto é confirmado na primeira task de F5.6; se ele não for Pro ou Enterprise, o RIPD pode exigir troca de plano, com custo, antes do piloto.
- Em projetos novos, as funções da Vercel rodam em iad1, Washington, EUA. São Paulo (gru1) está disponível, mas precisa ser configurada (https://vercel.com/docs/functions/configuring-functions/region; https://vercel.com/docs/regions). O Routing Middleware é implantado em todas as regiões, qualquer que seja a região configurada (mesma página, seção Limits).
- Os logs de execução da Vercel guardam a saída de console e ficam retidos por 1 hora (Hobby), 1 dia (Pro) ou 30 dias (Observability Plus) (https://vercel.com/docs/logs/runtime). Um log com trecho de insight fica nesse prazo.
- Num repositório Git do Hub, apagar um arquivo não o tira do histórico (https://huggingface.co/docs/hub/storage-buckets). super_squash_history é irreversível e não se aplica a tags (huggingface_hub/hf_api.py:4415-4460), e permanently_delete_lfs_files apaga arquivos LFS de todos os commits que os referenciam, não pode ser desfeito e pode corromper o repositório (hf_api.py:4549-4575). Um Storage Bucket apaga de forma imediata e permanente (https://huggingface.co/docs/hub/storage-buckets).
- Se o apagamento do vídeo ao fim do job (F7.5) não seguir a regra do ADR de F6.2, a rotulagem prevista no plano de F6.6 fica sem o vídeo, e a consolidação de F7.7 fica sem os rótulos que o plano exige.
- Nenhum item de F7 executa hoje a rotulagem dos cultos do piloto, e F7 não tem a disciplina Visão Computacional (arvore_v1.json, F7). Sem esse item, o plano de F6.6 prevê rótulos que ninguém faz.
- Os logs de job continuam disponíveis depois do fim (https://huggingface.co/docs/hub/jobs-manage). Execuções com --stdout anteriores a F6.2 podem ter deixado trechos nesses logs.
- O repositório do projeto é público. Um documento do piloto versionado nele por engano expõe dado da igreja e nomes.
- A transcrição usa a trilha inteira sem separar quem fala (reacao/transcribe.py:13). Fala da congregação captada pelo microfone pode ser transcrita e guardada, e não há teste nem passo do CI ligado à regra 5 (.github/workflows/ci.yml).
- O teste de schema atual procura nomes no texto de todas as migrações (tests/test_schema.py:9-12). Proibir por nome um campo retirado reprovaria 0001_init.sql; por isso o teste precisa ler o schema final.
- Retirar pct_olhos_fechados sem ajustar o painel e tests/test_pipeline_mock.py:17 quebra o relatório e a suíte.
- Um critério 2a inconclusivo ou um 2b sem meta assinada deixa a decisão do gate dependente da regra de F1.3.
- A forma de assinatura do pastor Filipe depende do que F1.3 registrar, e a data do primeiro culto do piloto não está definida. Os critérios 'antes do primeiro culto' dependem dessa data.

**Estratégia de fatiamento:** Por passo do fluxo de aprovação (estratégia 1 do TaskFlow): decisão do gate (F6.1), minimização aplicada (F6.2), igreja, controlador e RIPD (F6.3), forma de oposição ou consentimento, condicional (F6.5), aviso (F6.4) e plano de medição (F6.6). As tasks de cada PBI são divididas por disciplina. Se F6.2 (13 pontos sugeridos) não couber numa sprint, dividir em 'ADR, schema e teste de schema' e 'logs, painel e dataset card'. Se F6.3 (13 pontos sugeridos) não couber, dividir em 'igreja, controlador e instrumento' (F6.3.T8) e 'RIPD e notas de lei' (F6.3.T1 a T7 e a verificação de QA F6.3.T9).

### Critérios de aceite
- docs/poc-gate.md tem as sete linhas de resultado (1, 2a, 2b, 3, 4, 5 e 6) preenchidas com a origem aceita para cada tipo e uma decisão marcada, com data e as assinaturas de Fabio Pinheiro e do pastor Filipe.
- Com decisão diferente de 'seguir para dados da PIB e RIPD', F6.2 a F6.6 não começam, e o registro da decisão diz o caminho seguinte.
- O ADR de minimização, a migração nova e o teste de schema refletem as decisões. O ADR fixa o prazo de retenção de cada item do inventário, o local privado dos documentos do piloto, o destino dos rótulos do piloto e a regra de que o vídeo de um culto do piloto só é apagado depois da rotulagem prevista para ele, dentro do prazo máximo. A lista de consultas do painel web na Vercel ao Supabase coincide com a tabela de acesso do ADR.
- A igreja do piloto, o controlador, o operador e o encarregado da Fase 1 estão registrados no local privado, com data anterior à aprovação do RIPD, e o instrumento entre a igreja e Fabio Pinheiro, com os papéis e as instruções de tratamento, está assinado pelas duas partes.
- O RIPD da Fase 1 está no local privado decidido no ADR de F6.2, e docs/law/br.md está no repositório público. O RIPD tem a aprovação do encarregado e do controlador, os operadores Hugging Face, Supabase, Vercel e, se usada, Anthropic, a lista das pendências que impedem o piloto e a conclusão sobre F6.5.
- Cada termo que a checagem das listas do lint aponta no aviso aprovado está registrado como 'removido' ou 'exceção aprovada' pelo encarregado. O aviso identifica o controlador, traz o contato dele e o do encarregado e tem registro de publicação anterior ao primeiro culto do piloto.
- Se F6.5 for acionado, a forma de oposição ou consentimento atende à hipótese legal do RIPD, está registrada e em vigor antes do primeiro culto e não pede identificação.
- O plano de medição da Fase 1, com critério de conclusão e limites de qualidade por culto, está assinado antes do primeiro culto. Cada rótulo previsto nele consta do inventário do RIPD, o prazo da rotulagem de cada culto cabe no prazo de retenção dos vídeos do piloto do ADR de F6.2, e o plano cita o item de F7 que executa a rotulagem.
- Cada pendência que o RIPD marcou como impeditiva tem registro de resolução com data anterior ao primeiro culto do piloto.
- Cada registro de F6.3, F6.4, F6.5 (se acionado) e F6.6 tem data e está no lugar que F7.5 consulta.
- Caminho de erro: um registro sem data, fora do lugar que F7.5 consulta ou com data posterior ao primeiro culto do piloto reprova a verificação da Feature, e o registro diz qual pré-requisito falta.
- Caminho de erro: se a igreja indicada não confirmar a participação ou não assinar o instrumento, o registro diz o motivo e a data, e F6.4, F6.5 e F6.6 não começam.

### Alterações em relação à árvore
- Problema e solução da Feature: acrescentado o painel web na Vercel como operador de dados e fonte de logs (P3 revisada; https://vercel.com/docs/functions/configuring-functions/region; https://vercel.com/docs/logs/runtime).
- Usuários da Feature: acrescentada a equipe de mídia da igreja do piloto, com fonte em supabase/migrations/0001_init.sql:21 (perfil 'midia') e em F7.1. A citação anterior a docs/onprem.md:61 foi retirada, porque a linha só fala da cópia da gravação do OBS.
- Regras da Feature: acrescentadas RN05 (limites do painel na Vercel) e RN06 (ferramentas com vídeo ficam no HF), pela P3 revisada.
- F6.1: a origem do critério 4 passa a ser as notas registradas no painel web na Vercel (F5.7), em vez do Space. O título e as dependências não mudam.
- F6.2: o título passa de 'Aplicar ao schema, aos logs e ao dataset as decisões de minimização de dados' para 'Aplicar ao schema, aos logs dos jobs e do painel web na Vercel e ao dataset as decisões de minimização de dados'. O escopo ganha a lista de tabelas e colunas lidas e escritas pelo painel (P3 revisada) e os logs de execução da Vercel.
- F6.2: o vínculo entre usuário e papel passa a considerar o Supabase Auth usado pelo painel na Vercel (auth.users, com raw_app_meta_data), em vez do login OAuth do Space (https://supabase.com/docs/guides/api/custom-claims-and-role-based-access-control-rbac).
- F6.2: acrescentada a disciplina Front end, porque retirar coluna ou proibir trecho em log exige ajustar o painel de F5.6. Acrescentadas as dependências explícitas F5.6, F1.5 e F2.6. As decisões ficam num ADR em docs/adr/ (CONTRIBUTING.md:7).
- F6.3: a Vercel entra entre os operadores, com região padrão, DPA e logs (https://vercel.com/legal/dpa). O inventário inclui as contas dos usuários do painel no Supabase Auth e os logs de execução da Vercel. Dependências F5.6 e F2.6 explicitadas. Por ser documental, a verificação é revisão do encarregado e de Fabio Pinheiro, sem task de QA.
- F6.4: o fora de escopo diz que o painel web na Vercel não é canal do aviso, porque só atende perfis autenticados.
- F6.6: o retorno do pastor passa pelo painel web na Vercel (F7.3) e o alerta de qualidade aparece no mesmo painel (F7.6). Os rótulos de rostos e eventos usam a ferramenta do Space privado (F3.3), que fica no HF por exibir vídeo. Dependências F1.3, F3.2, F3.3 e F5.4 explicitadas.
- Todos os PBIs: acrescentados story points e horas como sugestão. A árvore não trazia estimativas (P6).
- Revisão, F6.4 e RN07 da Feature: a checagem do lint no aviso registra cada termo apontado como 'removido' ou 'exceção aprovada' pelo encarregado; exceção só para garantias e para a forma de F6.5. Rodar as listas de reacao/lint.py:8-13 sobre README.pt-BR.md:19-20 aponta 'assento' e 'sentiram', e 'o sistema nunca infere sentimentos' casa com a lista.
- Revisão, F6.4: nova task de Backend F6.4.T3, que cria a checagem de texto livre, porque reacao/lint.py só expõe check(Insight), que exige minuto, momento, trecho e sinais (reacao/lint.py:23-49). A task de QA passou a F6.4.T4. Story points de 3 para 5.
- Revisão, F6.4: RN02 descreve a transcrição como da trilha de áudio do arquivo, que pode incluir falas além do púlpito (reacao/transcribe.py:13). Acrescentadas RN08 (pedido de exclusão ou oposição depois da gravação) e RN09 (documentos no local privado).
- Revisão, F6.2: o teste de schema passa a ler o schema final das migrações em ordem, com dois casos negativos, porque tests/test_schema.py:9-12 procura nomes no texto e 0001_init.sql:4,9,16,17 cria as colunas que o ADR pode retirar. RN06, critério e F6.2.T5 reescritos; estimativa de T5 de 3 h para 6 h.
- Revisão, F6.2 e RN04 da Feature: a regra 6 é citada como está escrita e vale também para campos da equipe. Id de usuário em revisado_por e avaliador e tabela ligada a auth.users deixam de ser opções neutras e só entram como exceção aprovada, com mudança do texto da regra. Acrescentados critério sobre a regra 6 e premissa sobre as contas do Supabase Auth.
- Revisão, F6.2: o ADR passa a ter oito decisões (acrescentado o local dos documentos com dado da igreja do piloto, porque o repositório é público) e uma tabela de retenção por item do inventário. Acrescentados critérios de retenção, de local, do dataset card e das consultas do painel, e a task F6.2.T8 (dataset card). Story points de 8 para 13.
- Revisão, F6.2: o critério de log aceita como verificação obrigatória o teste com insight sintético, e o job pago só com aprovação prévia (P7), porque com o motor mock não há insight (processar_culto.py:86; reacao/insights.py:38; reacao/lint.py:40-41). F6.2.T7 usa Supabase local (supabase start) e confere as consultas do painel contra o ADR; F6.2.T6 anexa a lista de consultas.
- Revisão, F6.2 e riscos: a retenção de arquivos apagados no histórico Git passa a citar https://huggingface.co/docs/hub/storage-buckets. Acrescentados list_lfs_files e permanently_delete_lfs_files (huggingface_hub/hf_api.py:4495-4575) à regra de apagamento.
- Revisão, problema da Feature e F6.2: 'três campos guardam nome de pessoa da equipe' passou a 'três campos texto podem guardar nome de pessoa' (0001_init.sql:4,16,17; P12).
- Revisão, F6.1: origem aceita por tipo de critério (arquivo e revisão para 1, 2a, 2b, 3 e 5; instantâneo versionado das notas para o 4; URL do CI com SHA para o 6). F6.1.T2 grava o instantâneo no repositório de resultados. A comparação com o ADR 0001 ficou restrita a recall ≥64 px (critério 1) e jitter (2b); sensibilidade em p.p., fps e custo do ADR são conferidos contra a própria origem (docs/adr/0001-motor.md:8; bench.py:170-182). A forma de assinatura vem de F1.3.
- Revisão, F6.5: o caminho do registro é fixado no próprio PBI, dentro do local privado do ADR de F6.2, sem depender de decisão de F7.5. Acrescentados RN06, critério e caminho de erro sobre a hipótese legal (consentimento ou oposição). A afirmação de que a equipe de mídia controla a câmera foi para premissas.
- Revisão, F6.3: operadores completados com as tabelas que o Store grava (reacao/store.py:28-44), service.pregador, o repositório de resultados de F2.5 e os logs de job. Leitura do DPA da Vercel reescrita (a definição de leis aplicáveis traz exemplos). Registro de uso de Routing Middleware. Inventário com rótulos do piloto e rotuladores. Regra 5 em F6.3.T4 como 'sem verificação automática'. Leitura de DPA passou de F6.3.T1 (DevOps) para F6.3.T3 (Governança e Privacidade). F6.3.T2 ganhou a avaliação de reidentificação. Nova task F6.3.T6 (pendências impeditivas); a revisão passou a F6.3.T7. O RIPD vai para o local privado. Story points de 5 para 8.
- Revisão, F6.6: rotulagem dos cultos do piloto sem som, porque labels/README.md:15 vale só para o PoC, salvo exceção registrada no RIPD. F3.3 limitado a rostos e eventos, e o plano diz como os momentos são marcados. Novo vínculo F6.3 → F6.6 (rótulos no inventário do RIPD). Limite de rostos mensuráveis com a ressalva de que n_mensuravel é média arredondada (reacao/aggregate.py:26-31).
- Revisão, critérios da Feature: o antigo critério 8 (processamento bloqueado por F7.5) passou a exigir que os registros tenham data e estejam no lugar que F7.5 consulta; o bloqueio ficou como pendência de F7.5, que também precisa conferir o plano de F6.6. Acrescentados o critério de resolução das pendências impeditivas do RIPD e a RN10 (documentos do piloto fora do repositório público).
- Revisão, F6.3, F6.4 e F6.5 (igreja do piloto e controlador): nova task F6.3.T8 (Governança e Privacidade), primeira na ordem de execução de F6.3, que obtém do pastor Filipe a indicação da igreja, confirma com ela a participação, registra controlador, operador e encarregado e colhe a assinatura do instrumento com os papéis e as instruções de tratamento (LGPD art. 5º, VI, VII, VIII e XVII; art. 39; art. 41). F6.3.T2, F6.3.T3, F6.3.T7, F6.4.T1, F6.4.T2 e F6.5.T1 passam a depender dela, e F6.3 passa a depender de F3.1 (encarregado de F3.1.T2). O RIPD passa a ter também a aprovação do controlador (art. 5º, XVII), e o aviso passa a identificar o controlador e trazer o contato dele (art. 9º, III e IV) e o do encarregado (art. 41, §1º). Acrescentadas RN11 da Feature, RN11 de F6.3, critérios e caminhos de erro. Story points de F6.3 de 8 para 13 (sugestão); F6.3.T7 de 3 para 4 h. As refs das tasks existentes não mudaram.
- Revisão, F6.3 (escolha entre as opções): das duas opções da revisão, a confirmação da igreja ficou numa task nova de F6.3, e não em F6.1.T4, porque o registro traz dado da igreja e precisa do local privado decidido em F6.2, enquanto docs/poc-gate.md está no repositório público. A opção marcada no gate continua nomeando a PIB, como já faz o texto de docs/poc-gate.md:50.
- Revisão, F6.2 e F6.6 (rotulagem do piloto): a regra de apagamento do ADR (F6.2 RN08, F6.2.T1 e novo critério) passa a manter o vídeo de cada culto até o fim da rotulagem prevista no plano de F6.6, dentro do prazo máximo, e a dizer o que acontece se o prazo vencer antes. O ADR passa a decidir o destino dos rótulos do piloto (F6.2 RN10 e F6.2.T2), no item 'apagamento dos vídeos do piloto e destino dos rótulos do piloto'. F6.6 ganhou RN10 (prazo da rotulagem dentro da retenção dos vídeos) e RN11 (revisão dos rótulos por amostragem e item de F7 que executa a rotulagem), com critérios, caminho de erro e passos em T2, T3 e T4, e a dependência explícita de F6.2. F6.2.T1 de 4 para 5 h e F6.6.T2 de 5 para 6 h. Acrescentada RN12 da Feature.
- Revisão, partes fora de F6: as tasks de Visão Computacional e Data Science para rotular e revisar os cultos do piloto (F7.7 ou PBI novo), a leitura do destino do piloto por F3.3 ou F7.1.T1 com a lista de acesso dos rotuladores, o adiamento do apagamento em F7.5.T2, o registro dos rótulos em F7.4.T1 e a dependência de F7.1.T3 em F6.3.T8 ficaram em pendencias_sincronizar, porque esta entrega só altera F6.
- Revisão, fontes da LGPD: os artigos citados em F6.3, F6.4 e F6.5 foram conferidos no texto da lei obtido em 2026-09-23 pela leitura web do Exa, porque o site do Planalto respondeu HTTP 503 ao acesso direto. A premissa de F6.3 que dizia não ter sido possível reler a lei foi atualizada.
- Reconciliação, F6.1 (linhagem): F2.8 entrou nas dependências do PBI, de F6.1.T1 e de F6.1.T2. O contexto, RN01, a premissa do repositório de resultados e os passos de T1 e T2 passam a citar F2.8 (envio com linhagem; F2.8.T5 indica arquivo e coluna por critério) no lugar de F2.5, que fica só para o run_id. INVEST: nove PBIs predecessores.
- Reconciliação, F6.2 e F6.3 (plano e termos da Vercel): F6.2, F6.2.T2, F6.3 e F6.3.T1 passam a depender da primeira task de F5.6, que confirma o plano e os termos de uso da Vercel na Fase 0 (movida de F7.2.T2). A ref dessa task ainda não existe em feature_det_F5.json; o texto segue o que F7 já usa. F6.2.T1 não recebeu a dependência, porque só trata de apagamento e logs no HF. Premissas, riscos e pendências da Feature, de F6.2 e de F6.3 atualizadas.
- Reconciliação, F6.2 (D7 de F2.4.T4): o vínculo entre usuário e papel, a leitura da regra 6 para as contas da equipe e a lista de tabelas do painel passam a ser decididos em D7 de F2.4.T4, antes de F5.6; o ADR de F6.2 confirma ou ajusta. Mudaram 'quero', contexto, RN01 e RN03, e entrou RN11 (ajuste com motivo, link para o ADR 0002 e migração ou procedimento). Entrou um critério de aceite sobre confirmação ou ajuste de D7. F6.2.T2 parte de D7 e depende de F2.4.T4; F6.2.T3 ganhou o passo da migração ou do procedimento de ajuste; F6.2.T6 e F6.2.T7 conferem contra a lista de D7. RN04 e a premissa da regra 6 da Feature foram alinhadas.
- Reconciliação, F6.2.T7 (P7): a dependência 'Aprovação de Fabio (P7), com flavor, duração e custo previstos' entrou só para o job opcional em culto público com --stdout, como nas tasks de job pago de F2.
- Reconciliação, F6.3 (QA): nova task F6.3.T9 [QA], 'Verificar os critérios de aceite do RIPD, do registro da igreja e de docs/law/br.md contra as fontes', com dependência de F6.3.T7 e 4 h sugeridas. A revisão propunha a ref F6.3.T8, que já é a task de confirmação da igreja; a task nova recebeu a próxima ref livre. A premissa 'sem task de QA' foi reescrita, e o total sugerido de F6.3 passou de 36 h para 40 h, sem mudar os 13 pontos.
- Reconciliação, F6.3: o repositório de resultados passa a ser citado como criado em F2.6 e alimentado por F2.8, e F6.3.T3 parte da decisão de Fabio sobre a exceção da P26 na Fase 0 registrada em D7 de F2.4.T4.
- Reconciliação, ordem: os PBIs passam a seguir a ordem das refs (F6.1 a F6.6); antes, F6.5 vinha antes de F6.4. A ordem de execução continua dada pelas dependências (F6.5, quando acionado, vem antes de F6.4).
- Reconciliação, premissas sobre F7: o estado de F7 passou a ser conferido em feature_det_F7.json, e não só no resumo de arvore_v1.json.

### Premissas
- P3 revisada: todo processamento roda no ambiente de desenvolvimento do HF (HF Jobs, dataset privado ds-fabiopinheiro/reacao-poc-corpus, repositórios de modelo privados). O front end do produto roda num projeto novo na Vercel, no time 'Fabio Pinheiro's projects', que hoje só tem o projeto ai-guitar-coach-pilot, sem relação com este. A P3 revisada prevalece sobre P3, P9, P10 e P11 onde elas falam de Space para o front end do produto.
- P23: F6.2 a F6.6 só começam se F6.1 decidir seguir.
- P29: F6.5 é condicional. As dependências dele valem só se ele for acionado.
- P14: a igreja do piloto é a PIB. É dedução, e F6.3.T8 a confirma com a igreja indicada pelo pastor Filipe.
- P12: até a decisão de F6.2, insight_feedback.avaliador guarda um código de papel.
- Leitura da regra 6 adotada nesta Feature: ela vale para as tabelas do schema public criadas por supabase/migrations/, para campos da congregação e da equipe. As contas do Supabase Auth, exigidas pela P3 revisada, ficam em auth.users, no schema auth gerido pelo Supabase. Esta árvore não as trata como violação da regra 6. A leitura é decidida em D7 de F2.4.T4, antes de F5.6, e o ADR de F6.2 a confirma ou ajusta, com a regra 6 citada e a aprovação de Fabio Pinheiro e do encarregado.
- Quem controla a posição e o enquadramento da câmera na igreja do piloto não está registrado no repositório. A árvore supõe que seja a equipe de mídia, a confirmar com a igreja.
- Quem é controlador e quem é operador no tratamento da Fase 1 não está registrado no repositório. F3.1.T2 registra o controlador do uso dos clipes na Fase 0 (feature_F3_v3.json); F6.3.T8 não parte dele, porque a Fase 1 trata cultos inteiros e acrescenta Supabase e Vercel.
- A forma escrita e assinada do instrumento de papéis e instruções de tratamento é proposta desta revisão. O art. 39 da LGPD diz que o operador trata segundo as instruções do controlador, sem fixar forma.
- O site do Planalto respondeu HTTP 503 ao acesso direto em 2026-09-23. Os arts. 5º (II, VI, VII, VIII e XVII), 9º, 11, 38, 39 e 41 da LGPD foram conferidos no texto da mesma URL obtido pela leitura web do Exa na mesma data. O art. 33 vem do levantamento.
- O plano e os termos de uso da Vercel para este projeto estão a confirmar. Não são fato. A confirmação passa para a primeira task de F5.6, na Fase 0 (revisão da árvore, problema 'F7.2.T2 (mover para F5.6)'); essa task ainda não aparece em feature_det_F5.json, e F6 a cita como F7 já faz (feature_det_F7.json, F7.4.T1).
- Estado de F7 conferido em feature_det_F7.json nesta reconciliação: F7.7 tem T1 a T8 e nenhuma task de rotulagem; F7 não tem task de Visão Computacional; F7.5.T2 ainda apaga o vídeo ao fim do job concluído; F7.1.T3 depende de F7.1.T1 e F6.3, sem F6.3.T8; F7.4.T1 não cita os rótulos do piloto. As mudanças fora de F6 continuam como pendência, porque esta entrega só altera F6.
- Revisão não aplicada em parte: F6.4 (checagem do lint no aviso) — a checagem não foi limitada às frases que descrevem a congregação, como propôs uma das revisões. Ela roda no texto inteiro, e cada termo apontado é removido ou vira exceção aprovada pelo encarregado, porque escolher antes quais frases 'descrevem a congregação' seria um julgamento sem registro.
- Revisão não aplicada em parte: F6.1 RN08 — a troca, no ADR 0001, da coluna 'sensibilidade (p.p.)' por frac_eventos_riso_ok não foi feita aqui, porque o ADR é preenchido em F4.6. Ficou como pendência para F4.6, e a comparação em F6.1 exclui essa coluna.
- Revisão não aplicada em parte: F6.2.T7 (banco limpo) — foi adotado só o Supabase local. O branch do projeto de F2.6 não foi adotado porque seria um recurso novo fora de F2.6.
- Story points e horas são sugestão, a validar no refinamento. A duração da sprint e a capacidade do time não estão registradas (P6).

### Pendências para sincronizar
- Time (Area Path), Sprint e Responsável da Feature e de cada PBI
- Vínculo da Feature F6 ao Epic no Azure DevOps (processo Scrum, P1)
- Campos Valor de negócio, Riscos e Critérios de aceite da Feature no Azure DevOps
- Vínculos Predecessor/Successor entre PBIs, conforme 'dependencias' de cada um, incluindo o vínculo F6.3 → F6.6, o vínculo F3.1 → F6.3 (encarregado de F3.1.T2) e os vínculos de F6.3.T8 com F6.4 e F6.5
- Marcar PBI-105 como substituído por F6.1, se ele existir no Azure DevOps
- Plano e termos de uso da Vercel para o projeto do painel: criar em F5 a primeira task de F5.6 (movida de F7.2.T2) e trocar, em F6.2.T2 e F6.3.T1, o texto 'primeira task de F5.6' pela ref dela
- Nome do encarregado de dados (nomeação em F3.1.T2) e confirmação de que ele atende ao piloto (F6.3.T8)
- Indicação da igreja do piloto pelo pastor Filipe e confirmação com a igreja (F6.3.T8; P14)
- Representante da igreja do piloto que assina o instrumento de F6.3.T8
- Forma de assinatura do pastor Filipe (ver F1.3)
- Data do primeiro culto do piloto
- Confirmar com a igreja quem controla a posição e o enquadramento da câmera
- Tamanho da plateia da igreja do piloto, para a avaliação de reidentificação de F6.3.T2
- F7.7 ou PBI novo em F7: acrescentar tasks de Visão Computacional para rotular os cultos do piloto pelo protocolo de F3.2 na ferramenta de F3.3 e de Data Science para revisar os rótulos por amostragem, antes de F7.7.T4, conforme o plano de F6.6
- F3.3 ou F7.1.T1: leitura dos vídeos no destino de F7.1 pela ferramenta de rotulagem, lista de acesso dos rotuladores do piloto e forma de marcar momentos
- F7.5.T2: apagar o vídeo só depois que a rotulagem prevista para aquele culto no plano de F6.6 terminar, dentro do prazo do ADR de F6.2
- F7.4.T1: registrar o destino e a retenção dos rótulos do piloto decididos no ADR de F6.2, que F6.2.T8 exclui do corpus
- F7.1.T3: passar a depender de F6.3.T8 (igreja e controlador confirmados)
- Pedir em F4.6 que o ADR 0001 traga frac_eventos_riso_ok ou diga como calcula 'sensibilidade (p.p.)' (docs/adr/0001-motor.md:8)
- Alinhar com F5.7 e F2.8 o instantâneo versionado das notas do critério 4 (F6.1.T2)
- Atualizar F7.5: ler o registro de F6.5 no caminho fixado em F6.5, conferir o plano de F6.6 e a resolução das pendências impeditivas do RIPD, e ter o critério 'culto sem esses registros não é processado'
- F2.4.T4 (D7): incluir nos passos o local do vínculo entre conta e papel e a leitura da regra 6 para as contas da equipe, que F5.6.T3 já usa e F6.2 confirma ou ajusta
- F7.2 e F7.8: trocar a dependência de F6.2 para o local do vínculo entre conta e perfil por D7 de F2.4.T4 (F6.2 só confirma ou ajusta)
- F7.1.T3 e F7.4.T1 continuam sem as mudanças pedidas (dependência de F6.3.T8; destino e retenção dos rótulos do piloto)

## Preview — PBI F6.1 (novo) · Preencher o resultado dos seis critérios do gate e registrar a decisão assinada

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Preencher o resultado dos seis critérios do gate e registrar a decisão assinada |
| Tipo | Product Backlog Item |
| Pai | F6 |
| Tags | fase-0; gate; data-science; governanca; PBI-105 |
| Estimativa | 3 pts (sugestão); tasks: 15 h |
| Dependências | F1.1, F1.3, F1.6, F2.8 (conjunto de resultados de cada execução com linhagem no repositório privado de resultados), F4.6, F5.3 (condicional, P15 e P29), F5.4, F5.5, F5.7 |
| Substitui | PBI-105 |

#### Descrição

Como Fabio Pinheiro e pastor Filipe, signatários do gate da Fase 0  
Quero ver em docs/poc-gate.md o valor medido de cada critério (1, 2a, 2b, 3, 4, 5 e 6), cada um com a origem que permite conferi-lo, e marcar ali a decisão com data e assinaturas  
Para decidir com números rastreáveis entre seguir para dados da PIB e RIPD, ajustar e repetir, ou parar

**Contexto:** A coluna Resultado das linhas de docs/poc-gate.md:6-14 está vazia, e a linha de decisão (docs/poc-gate.md:50) não tem opção marcada, data nem assinaturas. Pelo documento, os números vêm da linha TOTAL de bench_<motor>.csv (docs/poc-gate.md:3). Origem de cada valor nesta árvore: 1, 2a e 2b vêm da linha TOTAL do bench do motor escolhido em F4.6, persistido com linhagem no repositório privado de resultados por F2.8, que também indica em docs/poc-gate.md o arquivo e a coluna do conjunto do run_id para cada critério (F2.8.T5). O 3 vem do comparador de F5.5. O 4 vem das notas gravadas em insight_feedback pelo painel web na Vercel e de insights_rejeitados_pelo_lint no run_log, calculados em F5.7. insight_feedback é uma tabela do Supabase, sem revisão, que aceita notas novas depois do cálculo (docs/poc-gate.md:12; supabase/migrations/0001_init.sql:17), por isso o critério 4 precisa de um instantâneo versionado. O 5 vem da fórmula pré-registrada em F1.3, medido em T4 por F5.4 e remedido por F5.3 se ele for acionado. O 6 vem do passo do CI, com o alvo pré-registrado em F1.3 e as correções de F1.1 e F1.6. A tabela do ADR 0001 tem as colunas 'recall ≥64 px', 'sensibilidade (p.p.)', 'jitter (p.p.)', 'fps T4' e 'custo/h vídeo' (docs/adr/0001-motor.md:8) e é preenchida em F4.6 a partir do bench. Só recall_ge64_max e jitter_dp_pp da linha TOTAL (bench.py:170,179) medem o mesmo que os critérios 1 e 2b. O 2a é a fração frac_eventos_riso_ok (docs/poc-gate.md:9; bench.py:176), e não uma sensibilidade em p.p. O fps e o custo do ADR vêm do bench em clipes (bench.py:181-182), e o critério 5 vem dos cultos inteiros de F5.4. A execução local em CPU (3815 s por hora de vídeo, out/run_log.json, não versionado) não vale para o critério 5. Este PBI só lê e registra: não faz nenhuma medição nova.

**Regras de negócio:**
- RN01 – Cada resultado cita a origem aceita para o seu tipo: arquivo de resultado, identificador de execução (run_id de F2.5 ou JOB_ID) e revisão no repositório de resultados para 1, 2a, 2b, 3 e 5 (F2.8); instantâneo versionado das notas e do cálculo, com run_id e revisão, para o 4; URL da execução do CI com o SHA do commit para o 6. Número sem origem não entra no gate.
- RN02 – Cada critério é lido pela regra pré-registrada e assinada em F1.3: meta do 2b, mínimo de eventos de riso do 2a e efeito de 2a inconclusivo, leitura de '≥ 3/5' no 4, fórmula do 5 e alvo do 6. A regra não muda depois de conhecido o resultado (docs/poc-gate.md:16,38-40).
- RN03 – O critério 1 vale só para o detector medido (P31). Se F4.7 trocou o detector, o valor vem do bench rodado com o detector novo.
- RN04 – O critério 5 usa só execução em t4-small, identificada pelo flavor que F1.5 grava. A execução local em CPU não conta.
- RN05 – O critério 4 usa o relatório gerado com o motor escolhido em F4.6 e as notas de Fabio e Filipe registradas no painel web na Vercel (P10; F5.7), lidas do instantâneo versionado.
- RN06 – A decisão marca exatamente uma das três opções de docs/poc-gate.md:50, com data e as assinaturas de Fabio Pinheiro e do pastor Filipe.
- RN07 – Com 'seguir para dados da PIB e RIPD', F6.2 a F6.6 e F7 podem começar (P23). Com 'ajustar e repetir', o registro cita a origem do novo conjunto de teste definida em F1.3. Com 'parar', o registro traz o motivo.
- RN08 – Na comparação com o ADR 0001 entram só as colunas que medem o mesmo que o gate: 'recall ≥64 px' com o critério 1 e 'jitter (p.p.)' com o 2b. 'sensibilidade (p.p.)', 'fps T4' e 'custo/h vídeo' vêm de outra métrica ou de outra execução e são conferidos só contra a própria origem.
- RN09 – As assinaturas usam a forma adotada em F1.3 para as regras pré-registradas. Se F1.3 não registrar a forma, ela é definida e registrada com Fabio e Filipe antes da reunião de decisão.

**Fora de escopo:**
- Rodar bench, jobs ou qualquer nova medição (F4.6, F5.3, F5.4, F5.5)
- Alterar as regras de leitura pré-registradas em F1.3
- Escolher o motor ou mudar as colunas do ADR 0001 (F4.6)
- Calcular a concordância do critério 4 (F5.7)
- Criar os itens de 'ajustar e repetir', que entram como itens novos se essa for a decisão
- Confirmar com a igreja a participação no piloto e o controlador (F6.3.T8)

#### Critérios de aceite

- As sete linhas do gate (1, 2a, 2b, 3, 4, 5 e 6) têm valor na coluna Resultado.
- Cada valor traz a origem aceita para o seu tipo: arquivo, identificador de execução e revisão (1, 2a, 2b, 3 e 5); instantâneo versionado das notas e do cálculo, com run_id e revisão (4); URL da execução do CI com o SHA (6). Ao abrir a origem citada, o número é o mesmo do gate.
- Cada valor traz a leitura 'atingido', 'não atingido' ou 'inconclusivo', e essa é a leitura que a regra pré-registrada em F1.3 dá para aquele número.
- O valor do critério 5 vem de execução registrada com flavor t4-small.
- Os valores de recall ≥64 px e de jitter do motor escolhido no ADR 0001 coincidem com os critérios 1 e 2b do gate. O registro diz de qual execução vêm a sensibilidade, o fps e o custo do ADR, que não entram nessa comparação.
- A linha de decisão tem uma e só uma opção marcada, a data e as assinaturas de Fabio Pinheiro e do pastor Filipe, na forma adotada em F1.3 ou registrada em F6.1.T4.
- Com 'ajustar e repetir', o registro cita a origem do novo conjunto de teste. Com 'parar', traz o motivo.
- Caminho de erro: um valor sem origem, divergente da origem ou vindo de execução local reprova a verificação, e a decisão não é assinada enquanto a divergência estiver aberta.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F6.1.T1 | Data Science | Reunir os valores dos critérios 1, 2a, 2b, 3 e 5 nos arquivos de resultado com linhagem | 4 | F2.8, F1.3, F4.6, F5.4, F5.5, F5.3 (se acionado) |
| F6.1.T2 | Data Science | Registrar os critérios 4 e 6 com origem versionada | 3 | F1.1, F1.3, F1.6, F2.5, F2.8, F5.7, F6.1.T1 |
| F6.1.T3 | QA | Conferir os valores do gate contra as origens e o ADR 0001 | 4 | F6.1.T1, F6.1.T2 |
| F6.1.T4 | Governança e Privacidade | Conduzir a decisão do gate e registrar opção, data e assinaturas | 3 | F6.1.T3 |
| F6.1.T5 | QA | Conferir o registro da decisão e fechar a verificação dos critérios de aceite | 1 | F6.1.T4 |

<details><summary>F6.1.T1 · [Data Science] Reunir os valores dos critérios 1, 2a, 2b, 3 e 5 nos arquivos de resultado com linhagem</summary>

**Objetivo:** Ter no PR do gate as linhas 1, 2a, 2b, 3 e 5 preenchidas com valor, leitura e origem.

**Passos previstos:**
1. Localizar no repositório de resultados (F2.8), pelo arquivo e coluna indicados em F2.8.T5, o bench_<motor>.csv do motor escolhido em F4.6 e anotar run_id, JOB_ID e revisão
2. Ler na linha TOTAL recall_ge64_max, frac_eventos_riso_ok e jitter_dp_pp (docs/poc-gate.md:8-10)
3. Ler o resultado do comparador de fronteiras de F5.5
4. Calcular o critério 5 pela fórmula pré-registrada em F1.3 com os run_log de F5.4, ou de F5.3 se acionado, conferindo que o flavor é t4-small
5. Registrar que o fps e o custo do ADR 0001 vêm do bench de F4.6 e que o critério 5 vem de F5.4 ou F5.3
6. Aplicar a regra de leitura de F1.3 e escrever 'atingido', 'não atingido' ou 'inconclusivo'
7. Abrir PR em docs/poc-gate.md citando PBI-105 e F6.1

**Definição de pronto:** PR aberto com as linhas 1, 2a, 2b, 3 e 5 preenchidas, cada uma com arquivo, identificador de execução, revisão e leitura.

**Dependências:** F2.8, F1.3, F4.6, F5.4, F5.5, F5.3 (se acionado)

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F6.1.T2 · [Data Science] Registrar os critérios 4 e 6 com origem versionada</summary>

**Objetivo:** Ter as linhas 4 e 6 do gate preenchidas com valor, leitura e uma origem que possa ser aberta depois.

**Passos previstos:**
1. Exportar, no fim do cálculo de F5.7, um instantâneo das linhas de insight_feedback do run_id avaliado (insight_id, código de papel do avaliador e nota, sem comentário) e do cálculo da contagem e da concordância
2. Gravar o instantâneo no repositório de resultados pelo envio de F2.8, com o run_id de F2.5, e anotar caminho e revisão
3. Conferir que o run_id é do relatório gerado com o motor escolhido em F4.6
4. Localizar a execução do CI no commit da versão avaliada e anotar a URL, o SHA e o resultado do passo da guarda
5. Comparar com o alvo do critério 6 pré-registrado em F1.3 e escrever a leitura
6. Atualizar o PR de F6.1.T1

**Definição de pronto:** Linhas 4 e 6 no PR: a 4 com caminho e revisão do instantâneo e o run_id; a 6 com a URL da execução do CI e o SHA; ambas com a leitura.

**Dependências:** F1.1, F1.3, F1.6, F2.5, F2.8, F5.7, F6.1.T1

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F6.1.T3 · [QA] Conferir os valores do gate contra as origens e o ADR 0001</summary>

**Objetivo:** Garantir, antes da assinatura, que cada número do gate bate com a sua origem e que as colunas comparáveis do ADR 0001 coincidem.

**Passos previstos:**
1. Para as linhas 1, 2a, 2b, 3 e 5, abrir o arquivo de origem na revisão citada e comparar o número
2. Para a linha 4, abrir o instantâneo na revisão citada, refazer a contagem e a concordância e comparar
3. Para a linha 6, abrir a execução do CI pela URL, conferir o SHA e o resultado do passo da guarda
4. Reaplicar a regra de leitura de F1.3 e comparar com a leitura escrita
5. Conferir no run_log que o valor do critério 5 vem de flavor t4-small
6. Comparar recall ≥64 px e jitter do motor escolhido em docs/adr/0001-motor.md com os critérios 1 e 2b; conferir fps e custo do ADR contra o CSV de F4.6
7. Registrar no PR cada linha como 'passou' ou 'não passou' e devolver as divergências

**Definição de pronto:** Checklist no PR com as sete linhas e a comparação com o ADR marcadas 'passou' e nenhuma divergência aberta.

**Dependências:** F6.1.T1, F6.1.T2

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F6.1.T4 · [Governança e Privacidade] Conduzir a decisão do gate e registrar opção, data e assinaturas</summary>

**Objetivo:** Ter em docs/poc-gate.md:50 uma decisão marcada, com data e as duas assinaturas.

**Passos previstos:**
1. Confirmar a forma de assinatura adotada em F1.3; se não houver, definir e registrar a forma com Fabio e Filipe antes da reunião
2. Enviar a Fabio e Filipe o PR conferido, com a tabela e as regras pré-registradas de F1.3
3. Conduzir a reunião de decisão e anotar a opção e o motivo
4. Marcar a opção na linha de decisão, com a data
5. Colher as assinaturas na forma registrada
6. Com 'ajustar e repetir', citar a origem do novo conjunto de teste de F1.3. Com 'parar', registrar o motivo
7. Mesclar o PR

**Definição de pronto:** PR mesclado com uma opção marcada, data, a forma de assinatura registrada e as assinaturas de Fabio Pinheiro e do pastor Filipe.

**Dependências:** F6.1.T3

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F6.1.T5 · [QA] Conferir o registro da decisão e fechar a verificação dos critérios de aceite</summary>

**Objetivo:** Fechar a verificação de todos os critérios de aceite de F6.1.

**Passos previstos:**
1. Conferir que há uma e só uma opção marcada, com data e as duas assinaturas na forma registrada
2. Conferir o registro complementar: origem do novo conjunto de teste ou motivo da parada
3. Marcar no PR cada critério de aceite como 'passou' ou 'não passou'

**Definição de pronto:** Todos os critérios de aceite de F6.1 marcados 'passou' no PR mesclado.

**Dependências:** F6.1.T4

**Estimativa sugerida:** 1 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- docs/poc-gate.md:1-14,16,38-40,50
- docs/adr/0001-motor.md:8-14
- bench.py:170,176,179,181-182
- supabase/migrations/0001_init.sql:17
- epico.json (métricas de sucesso: critérios 1 a 6 e decisão do gate)
- feature_F6.json (F6.1)
- arvore_v1.json (F1.3, F4.6, F5.7)
- premissas da árvore P10, P15, P23, P29 e P31
- P3 revisada (notas do critério 4 no painel web na Vercel)
- feature_det_F2.json (F2.8 e F2.8.T5: envio com linhagem e indicação de arquivo e coluna por critério)

#### Verificação INVEST: pontos que falharam
- Independente: depende de nove PBIs e só entra na sprint depois que todos terminarem. Não dá para adiantar parte dele.

#### Premissas
- Os arquivos de resultado ficam no repositório privado de resultados, criado em F2.6 e alimentado com linhagem por F2.8. O nome e o tipo dele são decisão de F2.4 (P24).
- F1.3 exige que Filipe assine as regras pré-registradas (arvore_v1.json, F1.3), mas o texto de F1.3 não diz a forma. Se ela não estiver registrada, F6.1.T4 a define. Filipe pode não ter conta no GitHub.
- O instantâneo do critério 4 leva insight_id, código de papel do avaliador e nota, sem o comentário, que é texto livre. É proposta desta revisão, a alinhar com F5.7 e F2.8.
- docs/poc-gate.md já traz no repositório público os nomes dos signatários (docs/poc-gate.md:50) e trata da Fase 0, por isso continua no repositório público.
- A confirmação da igreja do piloto e do controlador não entra neste PBI: ela traz dado da igreja e fica no local privado decidido em F6.2, em F6.3.T8.
- Se a regra de F1.3 não disser o que fazer com critério inconclusivo, Fabio e Filipe registram a leitura adotada junto da decisão.
- Story points e horas são sugestão, a validar no refinamento (P6).

#### Pendências para sincronizar
- Time (Area Path), Sprint e Responsável
- Story Points (sugestão: 3)
- Vínculo pai: Feature F6. Predecessores: F1.1, F1.3, F1.6, F2.8, F4.6, F5.3 (se acionado), F5.4, F5.5 e F5.7
- Marcar PBI-105 como substituído por este item, se ele existir no Azure DevOps
- Forma de assinatura do pastor Filipe (ver F1.3)
- Pedir em F4.6 que o ADR 0001 traga frac_eventos_riso_ok ou diga como calcula 'sensibilidade (p.p.)'
- Alinhar com F5.7 e F2.8 o instantâneo versionado das notas

## Preview — PBI F6.2 (novo) · Aplicar ao schema, aos logs dos jobs e do painel web na Vercel e ao dataset as decisões de minimização de dados

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Aplicar ao schema, aos logs dos jobs e do painel web na Vercel e ao dataset as decisões de minimização de dados |
| Tipo | Product Backlog Item |
| Pai | F6 |
| Tags | fase-1; privacidade; lgpd; minimizacao; supabase; vercel; schema |
| Estimativa | 13 pts (sugestão); tasks: 40 h |
| Dependências | F6.1, F2.4 (D7 de F2.4.T4: vínculo entre conta e papel, leitura da regra 6 para as contas da equipe e tabelas do painel, que este PBI confirma ou ajusta), F5.6 (primeira task: confirmação do plano e dos termos de uso da Vercel, movida de F7.2.T2; pendência de F5), F5.6 (painel web na Vercel que este PBI ajusta; vem antes de F6.1), F1.5 (teste de contrato entre run_log e migração), F2.6 (projeto Supabase de desenvolvimento) |
| Substitui | nenhum |

#### Descrição

Como encarregado de dados (DPO) e Fabio Pinheiro, responsáveis pelo tratamento no piloto  
Quero decidir e aplicar: o que se guarda da transcrição, o que pode ir para os logs, como ficam os campos texto que podem guardar nome de pessoa, se confirma ou ajusta o vínculo entre usuário e papel e a lista de tabelas que o painel web na Vercel lê e escreve, decididos em D7 de F2.4.T4, o destino da coluna pct_olhos_fechados, a regra de apagamento dos vídeos do piloto e o destino dos rótulos do piloto, o local privado dos documentos do piloto e o prazo de retenção de cada item do inventário  
Para que o RIPD (F6.3) descreva um tratamento já reduzido ao necessário e que o piloto comece sem guardar dado pessoal além do decidido

**Contexto:** Transcrição: transcript_segment guarda a transcrição inteira (supabase/migrations/0001_init.sql:13; processar_culto.py:88-89; reacao/store.py:34-35), feita da trilha inteira do arquivo sem separar quem fala (reacao/transcribe.py:13). O insight guarda o trecho citado com até 200 caracteres (reacao/insights.py:25). Logs: com --stdout, janelas, eventos e insights com trecho vão para o log do job (processar_culto.py:109-115), e os logs continuam disponíveis depois do fim do job (https://huggingface.co/docs/hub/jobs-manage). Com o motor mock o pipeline não transcreve (processar_culto.py:86), o trecho sai como TRECHO_AUSENTE (reacao/insights.py:38) e o lint rejeita o insight (reacao/lint.py:40-41); um culto com insight real exige motor e transcrição, que pela P3 revisada rodam no HF Jobs, com custo e aprovação prévia (P7). No painel web na Vercel (F5.6), os logs de execução das funções guardam a saída de console por 1 hora no plano Hobby, 1 dia no Pro e até 30 dias com Observability Plus (https://vercel.com/docs/logs/runtime). O plano e os termos de uso do projeto são confirmados na primeira task de F5.6, na Fase 0. Campos texto que podem guardar nome de pessoa: service.pregador, insight.revisado_por e insight_feedback.avaliador (0001_init.sql:4,16,17), fora da lista de tests/test_schema.py:5. Até esta decisão, avaliador guarda código de papel (P12), e o README diz que o sistema nunca classifica pregadores (README.pt-BR.md:21). A regra 6 diz 'Tabelas do Supabase não têm campo por pessoa' (CLAUDE.md, regra 6; tests/test_schema.py:1). Vínculo entre usuário e papel: pela P3 revisada, o painel usa Supabase Auth e RLS por perfil. O local do vínculo e a leitura da regra 6 para as contas da equipe são decididos em D7 de F2.4.T4, antes de F5.6, e F5.6.T3 grava o papel de avaliador e um código sem nome em app_metadata das contas de Fabio, de Filipe e de teste (feature_det_F5.json, F5.6 e F5.6.T3). Este PBI confirma ou ajusta essa decisão, com migração ou procedimento se mudar. O Supabase Auth guarda os usuários no schema auth (auth.users e auth.identities), e o papel pode ficar em raw_app_meta_data, que o usuário não altera (https://supabase.com/docs/guides/platform/migrating-to-supabase/auth0; https://supabase.com/docs/guides/api/custom-claims-and-role-based-access-control-rbac). Tabelas do painel: pela P3 revisada, o painel lê só agregados, eventos e insights, com chave pública. D7 de F2.4.T4 lista o que o painel lê (window_aggregate, event, insight, execuções liberadas de F5.6 e, na Fase 1, indicadores de F7.6) e escreve (insight_feedback), exclui transcript_segment e run_log e deixa moment e service como pendência de confirmação do usuário (feature_det_F2.json, F2.4.T4); e a Vercel não recebe vídeo, quadro, recorte de rosto nem observação por rosto. pct_olhos_fechados existe no schema e no agregado (0001_init.sql:9; reacao/types.py:52; reacao/aggregate.py:38,42), mas nenhum provider preenche eyes_closed, e tests/test_pipeline_mock.py:17 inclui a coluna entre os percentuais. Teste de schema: tests/test_schema.py procura cada termo proibido no texto de todas as migrações, sem comentários (tests/test_schema.py:9-12). Como 0001_init.sql cria pregador, pct_olhos_fechados, revisado_por e avaliador fora de comentário (0001_init.sql:4,9,16,17), pôr esses nomes na lista reprovaria as migrações reais e a própria migração que os remove. Retenção e apagamento: a retenção existe só como comentário, com 12 meses para agregados e 24 para relatórios e insights (0001_init.sql:20). Num repositório Git do Hub, apagar arquivo não o tira do histórico: 'Git history retains every past version' (https://huggingface.co/docs/hub/storage-buckets). super_squash_history é irreversível e não se aplica a tags (huggingface_hub/hf_api.py:4415-4460). list_lfs_files lista os arquivos LFS e permanently_delete_lfs_files os apaga de todos os commits que os referenciam, com rewrite_history=True por padrão, sem poder ser desfeito (hf_api.py:4495-4575). Storage Buckets não têm versionamento, e o apagamento neles é imediato e permanente (https://huggingface.co/docs/hub/storage-buckets). Rotulagem do piloto: o plano de F6.6 prevê rótulos de referência dos cultos do piloto feitos na ferramenta do Space privado de F3.3, que exibe o vídeo (feature_F3_v3.json, F3.3). Por isso o vídeo de cada culto precisa continuar no destino de F7.1 até a rotulagem daquele culto terminar. F6.2.T8 exclui vídeo e rótulo do piloto do dataset do corpus, e nenhum item da árvore decide onde ficam os rótulos do piloto (arvore_v1.json, F7). Local dos documentos: o repositório do projeto é público (https://api.github.com/repos/ds-fabiopinheiro/church-sentiment-analysis, visibility public, 2026-09-23). Banco limpo: aplicar as migrações num banco limpo sem mexer no projeto de F2.6, que guarda as notas usadas no critério 4, é possível com o Supabase local (supabase start; https://supabase.com/docs/guides/local-development).

**Regras de negócio:**
- RN01 – Nenhuma decisão cria identificação, embedding ou rastreamento (CLAUDE.md, regra 2). 'Tabelas do Supabase não têm campo por pessoa' (CLAUDE.md, regra 6), e isso vale para campos da congregação e da equipe. O vínculo entre usuário e papel e a leitura da regra 6 para as contas da equipe partem de D7 de F2.4.T4, que este PBI confirma ou ajusta. As opções-padrão são as que não criam coluna por pessoa no schema public: papel em raw_app_meta_data, código de papel em revisado_por e avaliador, e service.pregador retirado ou sem nome de pessoa. Id de usuário nessas colunas ou tabela ligada a auth.users só entram como exceção à regra 6 registrada no ADR, aprovada por Fabio Pinheiro e pelo encarregado, com a mudança do texto da regra e de tests/test_schema.py.
- RN02 – Cada decisão fica num ADR em docs/adr/, com data, responsável, motivo e a aprovação do encarregado (CONTRIBUTING.md:7). O ADR não traz dado da igreja do piloto.
- RN03 – O painel web na Vercel lê e escreve só as tabelas e colunas listadas no ADR, dentro do limite da P3 revisada (leitura de agregados, eventos e insights). A tabela de acesso do ADR parte da lista de D7 de F2.4.T4 e da resposta do usuário sobre moment e service, e diz o que confirma ou ajusta. A transcrição completa não é lida pelo painel.
- RN04 – Se a decisão proibir trecho em log, nem os logs dos jobs no HF nem os logs de execução do painel na Vercel recebem trecho de transcrição ou texto de insight.
- RN05 – Se a decisão for retirar pct_olhos_fechados, a coluna sai do schema, do agregado, do painel e dos testes na mesma entrega. Se a decisão for medir olhos fechados, abre-se PBI novo em F4, com rótulo e bench, e a coluna fica oculta no painel até lá.
- RN06 – O teste de schema lê o schema final, obtido das migrações em ordem, e falha se um campo retirado ou proibido pelo ADR existir nesse estado final, inclusive se uma migração posterior o recriar. 0001_init.sql não é editado.
- RN07 – O ADR fixa o prazo de retenção de cada item do inventário: tabelas do Supabase, contas do Supabase Auth, logs de job do HF, logs de execução da Vercel, vídeos do piloto e rótulos do piloto. Onde o prazo é do operador, o ADR registra 'definido pelo operador' com a fonte. São esses os prazos que o RIPD (F6.3) registra e o job de F7.4 aplica.
- RN08 – A regra de apagamento dos vídeos do piloto vale para os dois destinos possíveis de F7.1. O vídeo de um culto só é apagado depois que a rotulagem prevista para ele no plano de F6.6 terminar, e nunca depois do prazo máximo de retenção fixado no ADR; o ADR diz o que acontece com a rotulagem se o prazo vencer antes. Para repositório, a regra diz o efeito sobre histórico e tags e qual método tira o arquivo do histórico (super_squash_history ou permanently_delete_lfs_files). Para Storage Bucket, registra que o apagamento é imediato e permanente.
- RN09 – O ADR decide o local privado dos documentos com dado da igreja do piloto ou nome de pessoa da igreja (RIPD, registro da igreja e do controlador, instrumento de instruções de tratamento, aprovações, registro de publicação do aviso, registro de F6.5 e plano da Fase 1) e quem tem acesso a ele, fora do repositório público.
- RN10 – Vídeo e rótulo dos cultos do piloto não entram no dataset ds-fabiopinheiro/reacao-poc-corpus, e o dataset card registra isso com link para o ADR. O ADR decide onde ficam os rótulos dos cultos do piloto e quem tem acesso a eles.
- RN11 – Se o ADR ajustar uma decisão de D7 de F2.4.T4 (vínculo entre usuário e papel, leitura da regra 6 ou tabelas do painel), ele registra o motivo e o link para o ADR 0002, e a mudança chega às contas e às políticas criadas em F5.6 por migração ou procedimento versionado na mesma entrega.

**Fora de escopo:**
- Implementar o job de retenção (F7.4)
- Políticas de RLS por perfil e emissão do papel no token (F7.2)
- Escolher o destino dos vídeos do piloto (F7.1)
- Alterar o apagamento do vídeo ao fim do job (F7.5); este PBI fixa a regra no ADR
- Implementar a medida de olhos fechados (PBI novo, se decidido)
- Redigir o RIPD (F6.3)
- Alterar a ferramenta de rotulagem no Space privado (F3.3)
- Alterar arquivos, revisões ou tags do corpus e dos rótulos (F3.5); só o dataset card muda
- Apagar logs de jobs já executados: este PBI só levanta se há trecho neles e registra o resultado

#### Critérios de aceite

- O ADR de minimização está em docs/adr/ com uma decisão para cada um dos oito itens (transcrição e prazo, trechos em log, campos texto que podem guardar nome de pessoa, vínculo entre usuário e papel (confirmação ou ajuste de D7 de F2.4.T4), tabelas lidas e escritas pelo painel (confirmação ou ajuste da lista de D7), pct_olhos_fechados, apagamento dos vídeos do piloto e destino dos rótulos do piloto, e local privado dos documentos do piloto). Cada decisão tem data, responsável, motivo e aprovação do encarregado.
- O ADR tem o prazo de retenção de cada item do inventário (tabelas do Supabase, contas do Supabase Auth, logs de job do HF, logs de execução da Vercel com a URL do prazo do plano, vídeos do piloto e rótulos do piloto), ou 'definido pelo operador' com a fonte.
- A regra de apagamento do ADR diz que o vídeo de um culto do piloto só é apagado depois que a rotulagem prevista para ele no plano de F6.6 terminar, dentro do prazo máximo de retenção, e diz o que acontece com a rotulagem se o prazo vencer antes. O ADR diz onde ficam os rótulos do piloto e quem os acessa.
- As decisões sobre revisado_por, avaliador, service.pregador e o vínculo entre usuário e papel cumprem a regra 6 do CLAUDE.md como está escrita, ou o ADR registra a mudança do texto da regra, aprovada por Fabio Pinheiro e pelo encarregado, e tests/test_schema.py acompanha a mudança.
- Se o ADR ajustar D7 de F2.4.T4, ele traz o motivo e o link para o ADR 0002, e as contas e políticas de F5.6 refletem o ajuste pela migração ou pelo procedimento versionado; se confirmar, diz isso para o vínculo, para a leitura da regra 6 e para a lista de tabelas.
- Uma migração nova, aplicada ao Supabase de desenvolvimento, reflete as decisões de schema, e a suíte de testes passa com ela.
- O teste de schema, que lê o schema final das migrações em ordem, passa com as migrações reais e reprova dois casos negativos: uma migração de teste que cria um campo proibido e uma migração posterior à de minimização que recria uma coluna retirada.
- O teste de contrato entre os registros gravados pelo pipeline e as colunas das migrações (F1.5) passa com a migração nova.
- Se o ADR proibir trecho em log, o teste automatizado que roda a etapa de saída com um insight sintético e a saída em log ligada passa no CI e falha se o trecho ou o texto do insight aparecer no stdout. Se houver aprovação prévia do dono da conta (P7), um job em culto público com --stdout também não mostra trecho em 'hf jobs logs'.
- Se o ADR proibir trecho em log, depois de abrir no painel web na Vercel o relatório de um culto público, a busca pelo início do trecho de um insight nos logs de execução do projeto não retorna resultado.
- Depois da migração, o painel web na Vercel abre o relatório de um culto público sem erro. A lista de consultas do painel ao Supabase (tabela, colunas, leitura ou escrita), anexada ao PR, coincide com a tabela de acesso do ADR, e as requisições registradas no Supabase durante a abertura do relatório não tocam tabela fora dela.
- Se pct_olhos_fechados for retirado, a coluna não existe no schema aplicado, as janelas agregadas não trazem o campo e o painel não o exibe. Se a decisão for medir, o PBI novo está no backlog com link para o ADR.
- O dataset card de ds-fabiopinheiro/reacao-poc-corpus registra que vídeo e rótulo dos cultos do piloto não entram no dataset, com link para o ADR, e o histórico do dataset não tem arquivo do piloto.
- Caminho de erro: sem a aprovação do encarregado registrada no ADR, a verificação reprova o PBI e a migração não é aplicada.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F6.2.T1 | MLOps | Registrar a regra de apagamento dos vídeos do piloto, a retenção dos logs de job e o levantamento de trechos em logs já existentes | 5 | F6.1 |
| F6.2.T2 | Governança e Privacidade | Redigir o ADR de minimização com as oito decisões e a tabela de retenção e obter a aprovação do encarregado | 8 | F6.1, F6.2.T1, F2.4.T4 (D7), F5.6 (primeira task: confirmação do plano e dos termos de uso da Vercel, movida de F7.2.T2; pendência de F5) |
| F6.2.T3 | Backend | Escrever a migração de minimização e ajustar o agregado e a gravação conforme o ADR | 6 | F6.2.T2, F2.6, F1.5 |
| F6.2.T4 | Backend | Retirar trecho e texto de insight da saída de log do processamento, se o ADR proibir | 3 | F6.2.T2 |
| F6.2.T5 | QA | Reescrever o teste de schema para verificar o schema final das migrações | 6 | F6.2.T2, F6.2.T3 |
| F6.2.T6 | Front end | Ajustar o painel web na Vercel às tabelas e ao log decididos no ADR e listar suas consultas | 5 | F5.6, F6.2.T2, F6.2.T3 |
| F6.2.T7 | QA | Verificar os critérios de aceite da minimização | 6 | F6.2.T3, F6.2.T4, F6.2.T5, F6.2.T6, F6.2.T8, Aprovação de Fabio (P7), com flavor, duração e custo previstos, só para o job opcional em culto público com --stdout |
| F6.2.T8 | MLOps | Registrar no dataset card do corpus que vídeo e rótulo do piloto não entram nele | 1 | F6.2.T2 |

<details><summary>F6.2.T1 · [MLOps] Registrar a regra de apagamento dos vídeos do piloto, a retenção dos logs de job e o levantamento de trechos em logs já existentes</summary>

**Objetivo:** Levar ao ADR os fatos de apagamento por destino, a condição de apagamento depois da rotulagem, a retenção dos logs de job e a situação dos logs existentes.

**Passos previstos:**
1. Descrever, para repositório privado, o efeito do apagamento sobre histórico e tags e os métodos que tiram o arquivo do histórico: super_squash_history (hf_api.py:4415-4460) e list_lfs_files com permanently_delete_lfs_files e rewrite_history=True (hf_api.py:4495-4575), citando https://huggingface.co/docs/hub/storage-buckets para a retenção no histórico Git
2. Descrever, para Storage Bucket, o apagamento imediato e permanente (https://huggingface.co/docs/hub/storage-buckets)
3. Escrever a condição de que o vídeo de um culto só é apagado depois que a rotulagem prevista para ele no plano de F6.6 terminar, com o prazo máximo de retenção proposto e o que acontece com a rotulagem se o prazo vencer antes
4. Conferir no histórico do dataset ds-fabiopinheiro/reacao-poc-corpus que não há vídeo nem rótulo do piloto
5. Listar os jobs já executados com 'hf jobs ps -a' e procurar trecho de transcrição nos logs dos que usaram --stdout, sem rodar job novo
6. Registrar o que a documentação diz sobre a retenção dos logs de job, com a fonte (https://huggingface.co/docs/hub/jobs-manage), para a tabela de retenção
7. Escrever a seção do ADR com a regra proposta e o resultado do levantamento

**Definição de pronto:** Seção do ADR com a regra de apagamento para cada destino, os métodos de remoção do histórico, a condição de apagamento depois da rotulagem com o prazo máximo, a retenção dos logs de job com fonte e a lista de jobs com trecho no log, ou 'nenhum'.

**Dependências:** F6.1

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F6.2.T2 · [Governança e Privacidade] Redigir o ADR de minimização com as oito decisões e a tabela de retenção e obter a aprovação do encarregado</summary>

**Objetivo:** Ter um ADR aprovado que decide os oito itens de minimização e o prazo de retenção de cada item do inventário.

**Passos previstos:**
1. Reunir os fatos do contexto, com arquivo:linha e URL
2. Listar as opções de cada item. Para o vínculo entre usuário e papel, partir da decisão D7 do ADR 0002 (F2.4.T4), já aplicada em F5.6.T3, e registrar se ela é confirmada ou ajustada, com motivo. Para os campos texto e para um eventual ajuste do vínculo, as opções-padrão são as que não criam coluna por pessoa no schema public: papel em raw_app_meta_data, código de papel em revisado_por e avaliador, e service.pregador retirado ou sem nome de pessoa. Id de usuário ou tabela ligada a auth.users só entram como exceção à regra 6, com a mudança do texto da regra aprovada por Fabio Pinheiro e pelo encarregado
3. Confirmar ou ajustar a leitura da regra 6 para as contas do Supabase Auth registrada em D7 de F2.4.T4
4. Montar a tabela 'tabela/coluna → lida pelo painel, escrita pelo painel' a partir da lista de D7 de F2.4.T4 e da resposta do usuário sobre moment e service, dentro do limite da P3 revisada, marcando o que é confirmado e o que é ajustado
5. Montar a tabela de retenção por item: tabelas do Supabase, contas do Supabase Auth, logs de job do HF, logs de execução da Vercel pelo plano confirmado na primeira task de F5.6 (https://vercel.com/docs/logs/runtime), vídeos do piloto e rótulos do piloto; onde o prazo é do operador, registrar 'definido pelo operador' com a fonte
6. Decidir onde ficam os rótulos dos cultos do piloto, fora do dataset do corpus, e quem tem acesso a eles
7. Decidir o local privado dos documentos do piloto e quem tem acesso a ele, registrando que o repositório do projeto é público
8. Incluir a seção de F6.2.T1, com a condição de apagamento depois da rotulagem
9. Reunir com o encarregado e Fabio e registrar decisão, data, responsável e motivo de cada item
10. Registrar a aprovação do encarregado e abrir PR citando F6.2

**Definição de pronto:** ADR mesclado em docs/adr/ com as oito decisões, a tabela de acesso do painel, a tabela de retenção por item, a condição de apagamento depois da rotulagem, o destino dos rótulos do piloto, o local privado dos documentos do piloto e a aprovação do encarregado, sem dado da igreja do piloto.

**Dependências:** F6.1, F6.2.T1, F2.4.T4 (D7), F5.6 (primeira task: confirmação do plano e dos termos de uso da Vercel, movida de F7.2.T2; pendência de F5)

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F6.2.T3 · [Backend] Escrever a migração de minimização e ajustar o agregado e a gravação conforme o ADR</summary>

**Objetivo:** Deixar o schema e o pipeline iguais às decisões de schema do ADR.

**Passos previstos:**
1. Criar a migração seguinte a 0001_init.sql, sem editar 0001_init.sql, com as mudanças do ADR em transcript_segment, service.pregador, insight.revisado_por, insight_feedback.avaliador e pct_olhos_fechados
2. Se pct_olhos_fechados sair, remover o campo de WindowAggregate (reacao/types.py:52), do cálculo (reacao/aggregate.py:38,42) e de tests/test_pipeline_mock.py:17
3. Se a transcrição deixar de ser persistida ou passar a ser parcial, ajustar Store.save_segments (reacao/store.py:34-35) e a chamada em processar_culto.py:89
4. Se o ADR ajustar D7 de F2.4.T4, escrever a migração ou o procedimento versionado que leva o ajuste às contas e às políticas criadas em F5.6 (F5.6.T3 e F5.6.T4)
5. Aplicar a migração no Supabase de desenvolvimento
6. Rodar ruff check e pytest

**Definição de pronto:** PR citando F6.2 com a migração aplicada no Supabase de desenvolvimento, 0001_init.sql sem alteração e ruff e pytest passando.

**Dependências:** F6.2.T2, F2.6, F1.5

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F6.2.T4 · [Backend] Retirar trecho e texto de insight da saída de log do processamento, se o ADR proibir</summary>

**Objetivo:** Garantir que o pipeline não escreva no log o que o ADR proibir.

**Passos previstos:**
1. Alterar a saída de --stdout (processar_culto.py:109-115) para não imprimir trecho nem texto de insight, mantendo o que o ADR permitir
2. Conferir as demais impressões do pipeline (processar_culto.py:108; reacao/insights.py:56) contra o ADR
3. Escrever um teste que roda a etapa de saída com um insight sintético, com trecho e texto conhecidos, e falha se o trecho ou o texto aparecer no stdout

**Definição de pronto:** Teste com insight sintético passando no CI, e nenhuma impressão de trecho ou texto de insight no código do pipeline.

**Dependências:** F6.2.T2

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F6.2.T5 · [QA] Reescrever o teste de schema para verificar o schema final das migrações</summary>

**Objetivo:** Fazer o teste de schema barrar a volta de campo retirado ou proibido sem reprovar as migrações que já o criaram ou removeram.

**Passos previstos:**
1. Manter a busca por texto dos termos que nunca podem aparecer (tests/test_schema.py:5) e confirmar que ela continua ignorando comentários (tests/test_schema.py:10)
2. Acrescentar um teste que lê supabase/migrations/*.sql em ordem de nome e interpreta create table, alter table ... add column e alter table ... drop column para obter as colunas finais de cada tabela
3. Proibir no estado final os campos retirados ou proibidos pelo ADR
4. Criar dois casos negativos com migrações temporárias: uma que cria um campo proibido e uma, posterior à de minimização, que recria uma coluna retirada; confirmar que o teste reprova as duas
5. Confirmar que 0001_init.sql não foi editado

**Definição de pronto:** Teste novo passa com as migrações reais, reprova os dois casos negativos e está num PR citando F6.2, com 0001_init.sql sem alteração.

**Dependências:** F6.2.T2, F6.2.T3

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F6.2.T6 · [Front end] Ajustar o painel web na Vercel às tabelas e ao log decididos no ADR e listar suas consultas</summary>

**Objetivo:** Fazer o painel consultar só o que o ADR permite, não registrar trecho em log e deixar a lista de consultas para conferência.

**Passos previstos:**
1. Restringir as consultas do painel às tabelas e colunas listadas no ADR, que confirma ou ajusta a lista de D7 de F2.4.T4
2. Retirar pct_olhos_fechados das consultas e da tela, se a coluna sair
3. Exibir revisor e avaliador conforme a decisão, com código de papel ou o campo definido
4. Remover do código de servidor do painel qualquer log com trecho ou texto de insight
5. Listar todas as consultas do painel ao Supabase (tabela, colunas, leitura ou escrita) e anexar ao PR
6. Publicar em preview no projeto do painel na Vercel e abrir o relatório de um culto público

**Definição de pronto:** O preview do painel abre o relatório de um culto público sem erro depois da migração, o código não tem log com trecho ou texto de insight, e a lista de consultas ao Supabase está anexada ao PR.

**Dependências:** F5.6, F6.2.T2, F6.2.T3

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F6.2.T7 · [QA] Verificar os critérios de aceite da minimização</summary>

**Objetivo:** Marcar cada critério de aceite de F6.2 como 'passou' ou 'não passou' com evidência.

**Passos previstos:**
1. Conferir no ADR as oito decisões, a tabela de acesso do painel, a tabela de retenção, o local privado dos documentos do piloto e a aprovação do encarregado
2. Conferir no ADR a condição de apagamento do vídeo depois da rotulagem, o prazo máximo, o que acontece se o prazo vencer antes e o destino dos rótulos do piloto
3. Conferir que as decisões sobre revisado_por, avaliador, service.pregador e o vínculo entre usuário e papel cumprem a regra 6 como está escrita, ou que a exceção está aprovada e tests/test_schema.py a acompanha
4. Conferir que o ADR diz, para o vínculo entre usuário e papel, para a leitura da regra 6 e para a lista de tabelas do painel, se confirma ou ajusta D7 de F2.4.T4, e que um ajuste tem motivo, link para o ADR 0002 e migração ou procedimento aplicado
5. Aplicar todas as migrações em ordem num Supabase local (supabase start), sem mexer no projeto de F2.6, e rodar pytest completo, incluindo schema, contrato de F1.5 e pipeline mock
6. Rodar os dois casos negativos do teste de schema
7. Rodar o teste de saída com insight sintético; só com aprovação prévia do dono da conta (P7), rodar também um job em culto público com --stdout e procurar o trecho em 'hf jobs logs'
8. Comparar a lista de consultas de F6.2.T6 com a tabela de acesso do ADR e com as requisições registradas nos logs do projeto Supabase de desenvolvimento durante a abertura do relatório no preview; tabela fora do ADR reprova
9. Buscar o início do trecho de um insight nos logs de execução do projeto na Vercel, dentro do prazo de guarda do plano
10. Conferir pct_olhos_fechados no schema, nas janelas e na tela, ou o link do PBI novo
11. Conferir o dataset card do corpus e que o histórico do dataset não tem arquivo do piloto
12. Registrar no PR o resultado de cada critério

**Definição de pronto:** Relatório de verificação no PR com 'passou' ou 'não passou' para cada critério de aceite e a evidência de cada um.

**Dependências:** F6.2.T3, F6.2.T4, F6.2.T5, F6.2.T6, F6.2.T8, Aprovação de Fabio (P7), com flavor, duração e custo previstos, só para o job opcional em culto público com --stdout

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F6.2.T8 · [MLOps] Registrar no dataset card do corpus que vídeo e rótulo do piloto não entram nele</summary>

**Objetivo:** Deixar no dataset do corpus a regra de separação decidida no ADR.

**Passos previstos:**
1. Acrescentar ao dataset card de ds-fabiopinheiro/reacao-poc-corpus a regra de que vídeo e rótulo dos cultos do piloto não entram no dataset, com link para o ADR
2. Enviar só o dataset card, sem alterar arquivos de vídeo, rótulos, revisões marcadas ou tags (F3.5)
3. Anotar a revisão do dataset gerada

**Definição de pronto:** Dataset card com a regra e o link para o ADR numa revisão do dataset que não altera vídeo, rótulo nem tag.

**Dependências:** F6.2.T2

**Estimativa sugerida:** 1 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- CLAUDE.md (regras 2 e 6)
- supabase/migrations/0001_init.sql:4,9,13,16-17,20-21
- tests/test_schema.py:1,5,9-12
- tests/test_pipeline_mock.py:17
- processar_culto.py:86,88-89,108-115
- reacao/store.py:34-35
- reacao/transcribe.py:13
- reacao/insights.py:25,38,56
- reacao/lint.py:40-41
- reacao/types.py:52
- reacao/aggregate.py:38,42
- README.pt-BR.md:21
- CONTRIBUTING.md:7
- .venv/lib/python3.11/site-packages/huggingface_hub/hf_api.py:4415-4460 (super_squash_history) e 4495-4575 (list_lfs_files, permanently_delete_lfs_files), versão 1.32.0
- https://huggingface.co/docs/hub/jobs-manage
- https://huggingface.co/docs/hub/storage-buckets
- https://vercel.com/docs/logs/runtime
- https://supabase.com/docs/guides/api/custom-claims-and-role-based-access-control-rbac
- https://supabase.com/docs/guides/platform/migrating-to-supabase/auth0
- https://supabase.com/docs/guides/local-development
- https://supabase.com/docs/guides/observability/logs
- https://api.github.com/repos/ds-fabiopinheiro/church-sentiment-analysis (visibility public, 2026-09-23)
- feature_F3_v3.json (F3.3: a ferramenta exibe o vídeo; F3.4: rotulagem de rostos em Visão Computacional e revisão por amostragem em Data Science)
- arvore_v1.json (F7: disciplinas e resumo de F7.4, F7.5 e F7.7)
- feature_F6.json (F6.2); premissas P7, P12, P30; P3 revisada
- feature_det_F2.json (F2.4.T4: D7 e D8); feature_det_F5.json (F5.6 e F5.6.T3: papéis em app_metadata); consolidacao.json (problemas 'F7.2.T2 (mover para F5.6)', 'F5.6.T2, F6.2 (F6.2.T2), F7.2 e F7.8' e 'F2.4.T4 (D7), F5.8')

#### Verificação INVEST: pontos que falharam
- Small: oito decisões e a tabela de retenção aplicadas em schema, teste, pipeline, painel e dataset card (13 pontos sugeridos). Se não couber numa sprint, dividir em 'ADR, schema e teste de schema' (T1, T2, T3, T5) e 'logs, painel e dataset card' (T4, T6, T7, T8).
- Independente: altera o painel entregue em F5.6 e condiciona F6.3, F6.6, F7.2, F7.3, F7.4 e F7.5.

#### Premissas
- A fala do púlpito pode conter nomes e pedidos de oração de terceiros, e a trilha pode captar falas da congregação; por isso a transcrição entra na minimização. É dedução do levantamento, sem medição.
- Front end foi acrescentado às disciplinas da árvore. Pela P3 revisada, o painel na Vercel lê o Supabase, e retirar coluna ou proibir trecho em log exige ajustar o código do painel criado em F5.6.
- O ADR recebe o próximo número livre em docs/adr/ depois do ADR 0002 de F2.4.
- Leitura da regra 6: as contas em auth.users são exigência da P3 revisada e ficam no schema auth, gerido pelo Supabase, fora de supabase/migrations/. D7 de F2.4.T4 registra essa leitura antes de F5.6; o ADR deste PBI a confirma ou ajusta com a regra 6 citada e a aprovação de Fabio Pinheiro e do encarregado, e o RIPD lista essas contas como dado pessoal da equipe.
- F5.6.T3 implementa o vínculo entre usuário e papel decidido em D7 de F2.4.T4, e F7.2 e F7.8 acrescentam os perfis do piloto; este PBI confirma ou ajusta a decisão. O schema auth não está em supabase/migrations/, então fica fora do alcance de tests/test_schema.py, que só lê esses arquivos (dedução de tests/test_schema.py:9).
- O teste de schema obtém o estado final interpretando em ordem create table, alter table ... add column e alter table ... drop column. É escolha desta revisão; aplicar as migrações num Postgres e ler information_schema também serviria, mas exigiria banco no CI.
- O banco limpo da verificação é o Supabase local. Um branch do projeto de F2.6 não foi adotado porque seria um recurso novo fora de F2.6.
- As requisições do painel são conferidas nos logs do projeto Supabase de desenvolvimento (https://supabase.com/docs/guides/observability/logs), além da inspeção do código.
- A verificação dos logs da Vercel precisa acontecer dentro do prazo de guarda do plano do projeto (1 hora no Hobby, https://vercel.com/docs/logs/runtime). O plano é o confirmado na primeira task de F5.6.
- A verificação obrigatória dos logs do pipeline é o teste com insight sintético. Um job pago no HF Jobs só roda com aprovação prévia do dono da conta (P7).
- A regra que mantém o vídeo até o fim da rotulagem é escrita antes do plano de F6.6: o ADR fixa o prazo máximo, e F6.6 encaixa a rotulagem nele (F6.6 RN10). É proposta desta revisão.
- Em feature_det_F7.json, F7.5.T2 ainda apaga o vídeo ao fim do job concluído e F7.4.T1 não cita os rótulos do piloto. O ajuste dessas tasks continua como pendência de F7.
- O ADR deste PBI recebe o resultado de D7 de F2.4.T4 já em uso no painel desde a Fase 0. Mantê-lo como decisão aberta aqui deixaria o mecanismo e os dados pessoais da equipe em uso antes da decisão, como apontou a revisão da árvore (consolidacao.json).
- Story points subiram de 8 para 13 (sugestão) por causa de dois itens novos no ADR, da tabela de retenção, do teste de schema por estado final, da conferência das consultas do painel e do dataset card. A condição de apagamento depois da rotulagem e o destino dos rótulos do piloto não mudaram a sugestão. Story points e horas são sugestão, a validar no refinamento (P6).

#### Pendências para sincronizar
- Time (Area Path), Sprint e Responsável
- Story Points (sugestão: 13)
- Vínculo pai: Feature F6. Predecessores: F6.1, F2.4 (D7 de F2.4.T4), F5.6 (inclusive a primeira task, de plano e termos da Vercel), F1.5 e F2.6. Sucessores: F6.3, F6.6, F7.2, F7.3, F7.4 e F7.5
- Nome do encarregado de dados
- Ref da primeira task de F5.6 (plano e termos da Vercel), que define a janela de verificação dos logs
- Aprovação do dono da conta para o job opcional de verificação dos logs (P7)
- Se a decisão for medir olhos fechados, criar o PBI novo em F4
- Pedir em F7.5.T2 que o apagamento do vídeo siga a regra do ADR: só depois da rotulagem prevista para aquele culto no plano de F6.6, dentro do prazo máximo
- Pedir em F7.4.T1 o registro do destino e da retenção dos rótulos do piloto decididos no ADR

## Preview — PBI F6.3 (novo) · Confirmar a igreja e o controlador do piloto e elaborar o RIPD da Fase 1 e as notas de lei brasileira em docs/law/br.md

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Confirmar a igreja e o controlador do piloto e elaborar o RIPD da Fase 1 e as notas de lei brasileira em docs/law/br.md |
| Tipo | Product Backlog Item |
| Pai | F6 |
| Tags | fase-1; privacidade; lgpd; ripd; governanca; vercel |
| Estimativa | 13 pts (sugestão); tasks: 40 h |
| Dependências | F6.2, F3.1 (encarregado nomeado em F3.1.T2), F5.6 (primeira task: confirmação do plano e dos termos de uso da Vercel, movida de F7.2.T2; pendência de F5), F5.6 (projeto do painel na Vercel e região das funções; transitiva via F6.2), F2.6 (projeto Supabase de desenvolvimento e região) |
| Substitui | nenhum |

#### Descrição

Como encarregado de dados (DPO), com Fabio Pinheiro, o pastor Filipe e a igreja do piloto  
Quero a igreja do piloto, o controlador, o operador e o encarregado da Fase 1 confirmados, com o instrumento de papéis e instruções de tratamento assinado, e um RIPD da Fase 1 no local privado decidido em F6.2, com inventário de dados, base legal, operadores e transferência internacional, retenção, encarregado, riscos e medidas e as pendências que impedem o piloto, além das notas de lei brasileira em docs/law/br.md no repositório público  
Para cumprir o pré-requisito do README para a Fase 1 com o RIPD escrito para o controlador certo e permitir que a decisão de iniciar o piloto e o disparo de cada culto (F7.5) citem um documento datado

**Contexto:** O README exige relatório de impacto à privacidade e aviso à congregação antes da Fase 1 (README.pt-BR.md:35), e o gate liga a decisão 'seguir' aos dados da PIB e ao RIPD (docs/poc-gate.md:50). docs/onprem.md:68 diz que a base legal é tratada no RIPD. Não há RIPD nem pasta docs/law/ no repositório (listagem de docs/ em 2026-09-23), e CONTRIBUTING.md:12 pede notas de lei em docs/law/<country>.md. O repositório é público (https://api.github.com/repos/ds-fabiopinheiro/church-sentiment-analysis, 2026-09-23), por isso o RIPD vai para o local privado decidido no ADR de F6.2. Igreja e controlador: a igreja do piloto ser a PIB é dedução (P14), e o épico põe a indicação da igreja do piloto entre as dependências do pastor Filipe (epico.json). F3.1.T2 registra o controlador do uso dos clipes na Fase 0 e obtém a nomeação do encarregado (feature_F3_v3.json). Nenhum item identifica o controlador do tratamento da Fase 1. Pontos da LGPD: convicção religiosa é dado sensível (art. 5º, II); controlador é quem toma as decisões sobre o tratamento, e operador é quem trata em nome do controlador (art. 5º, VI e VII); o RIPD é 'documentação do controlador' (art. 5º, XVII) e tem conteúdo mínimo no art. 38, parágrafo único; o operador trata segundo as instruções do controlador (art. 39); o controlador indica o encarregado (art. 41); o tratamento de dado sensível está no art. 11; a transferência internacional, no art. 33 (https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm). Operadores previstos, com a lista completa de itens e prazos vinda do ADR de F6.2: (1) Hugging Face: HF Jobs e seus logs, que continuam disponíveis depois do fim do job (https://huggingface.co/docs/hub/jobs-manage); dataset privado do corpus; repositório privado de resultados, criado em F2.6 e alimentado por F2.8, com CSV do bench, run_log e agregados; destino dos vídeos do piloto de F7.1; destino dos rótulos do piloto decidido no ADR de F6.2; e Space de rotulagem de F3.3, onde os rotuladores veem o vídeo. (2) Supabase: o pipeline grava window_aggregate, moment, transcript_segment (a transcrição inteira), event, insight e run_log (reacao/store.py:28-44); o schema tem ainda service, com pregador, e insight_feedback (0001_init.sql:4,17); e as contas do Supabase Auth ficam em auth.users (https://supabase.com/docs/guides/platform/migrating-to-supabase/auth0). A migração diz região de São Paulo (0001_init.sql:2), mas o projeto não foi encontrado na conta conectada em 2026-09-23. (3) Vercel: painel web do produto (P3 revisada). Em projetos novos, as funções rodam por padrão em iad1, Washington, EUA, e gru1, São Paulo, está disponível; o Routing Middleware é implantado em todas as regiões, qualquer que seja a região configurada (https://vercel.com/docs/functions/configuring-functions/region, seção Limits; https://vercel.com/docs/regions). O DPA vale para os planos Pro e Enterprise, prevê transferência para os EUA e define as leis aplicáveis como todas as leis de privacidade aplicáveis, com GDPR, UK DPA 2018, CCPA, PIPEDA e a lei australiana como exemplos, sem citar a LGPD (https://vercel.com/legal/dpa, leitura de 2026-09-23). Os logs de execução guardam a saída de console, o user agent e a região da requisição, e o filtro 'Logs from your browser' compara endereço IP e user agent (https://vercel.com/docs/logs/runtime). (4) Anthropic, se os jobs do piloto usarem ANTHROPIC_API_KEY: nesse caso a transcrição (até 60000 caracteres), os agregados e os trechos vão para a API (reacao/moments.py:53-63; reacao/insights.py:41-48; P26). Rótulos: os rótulos de referência do piloto (F6.6) seguem labels/README.md, com _faces.csv de um rosto por linha (labels/README.md:6), _eventos.csv e _momentos.csv, e F1.3 decide se a Fase 1 exige caixas. Regra 5: a transcrição usa a trilha inteira sem separar quem fala (reacao/transcribe.py:13), e não há teste nem passo do CI ligado a ela (.github/workflows/ci.yml). O plano e os termos de uso da Vercel para este projeto são confirmados na primeira task de F5.6, na Fase 0, e F7.2.T2 só os reconfirma para dados da igreja do piloto. D7 de F2.4.T4 registra a decisão de Fabio sobre a exceção da P26 para a Fase 0.

**Regras de negócio:**
- RN01 – A base legal para dado sensível de convicção religiosa é escolhida entre as hipóteses do art. 11 e justificada. A conclusão diz se F6.5 é acionado.
- RN02 – Cada operador aparece com o que recebe, a região onde processa e o instrumento contratual. Para a Vercel, o RIPD registra também se o painel usa Routing Middleware e, se usar, que ele roda em todas as regiões. Região ou contrato não confirmados entram como pendência com responsável, e não como fato.
- RN03 – O inventário e os prazos de retenção são os do ADR de F6.2, ou 'definido pelo operador' com a fonte. Mudar algum deles reabre F6.2.
- RN04 – O RIPD decide se a transcrição dos cultos do piloto pode ir à API da Anthropic (P26). Sem essa decisão, os jobs do piloto rodam sem a chave.
- RN05 – O RIPD registra que a Vercel não recebe vídeo, quadro, recorte de rosto nem observação por rosto, e que a chave de serviço do Supabase fica só nos jobs do HF (P3 revisada).
- RN06 – Cada uma das seis regras do CLAUDE.md aparece ligada a pelo menos um risco, à medida e ao lugar onde a medida é verificada (teste, passo do CI, RLS ou lint). Regra sem verificação automática, como a 5, é registrada como 'sem verificação automática', com a medida manual e o responsável.
- RN07 – O RIPD tem data, versão, responsável, aprovação do encarregado (LGPD art. 41) e aprovação do controlador registrado em F6.3.T8, porque o RIPD é documentação do controlador (art. 5º, XVII).
- RN08 – docs/law/br.md descreve o que uma igreja precisa fazer antes de processar as próprias gravações (CONTRIBUTING.md:12) e não traz dado da igreja do piloto.
- RN09 – O RIPD fica no local privado decidido no ADR de F6.2. docs/law/br.md fica no repositório público.
- RN10 – Cada pendência marcada como impeditiva entra num registro, no lugar que F7.5 consulta, com responsável e campo para a data de resolução.
- RN11 – Antes da base legal do RIPD (F6.3.T3), F6.3.T8 registra a igreja do piloto, o controlador, o operador e o encarregado da Fase 1, e o instrumento entre a igreja e Fabio Pinheiro, com os papéis e as instruções de tratamento (art. 5º, VI e VII; art. 39), é assinado pelas duas partes. Os registros e o instrumento ficam no local privado do ADR de F6.2.

**Fora de escopo:**
- Base legal e RIPD da produção on-premises (docs/onprem.md:68)
- Notas de lei de outros países (README.pt-BR.md:39)
- Aviso à congregação (F6.4) e forma de oposição ou consentimento (F6.5)
- Contratar plano ou assinar DPA com os operadores de nuvem (Hugging Face, Supabase, Vercel e, se usada, Anthropic); o RIPD registra a situação. O instrumento entre a igreja e Fabio Pinheiro está no escopo (F6.3.T8)
- Configurar a região das funções do painel na Vercel; o RIPD registra a que estiver em vigor
- Resolver as pendências impeditivas; este PBI só as registra com responsável

#### Critérios de aceite

- A igreja do piloto, o controlador, o operador e o encarregado da Fase 1 estão registrados no local privado decidido no ADR de F6.2, com data anterior à aprovação do RIPD, e o instrumento entre a igreja e Fabio Pinheiro, com os papéis e as instruções de tratamento, está assinado pelas duas partes.
- O RIPD está no local privado decidido no ADR de F6.2, com data, versão, responsável e as aprovações registradas do encarregado e do controlador.
- O inventário lista vídeo da plateia, transcrição, agregados e eventos, insights com trecho, notas e revisão, contas dos usuários do painel, logs (HF Jobs e Vercel), rótulos de referência do piloto (rostos, com caixas se F1.3 exigir; eventos; momentos) e rotuladores com acesso ao vídeo. Para cada item, diz onde fica, quem acessa e o prazo de retenção, que é o do ADR de F6.2 ou 'definido pelo operador' com a fonte.
- A seção de base legal cita a hipótese do art. 11 escolhida e a justificativa, e termina com 'F6.5 necessário: sim' ou 'F6.5 necessário: não'.
- Hugging Face, Supabase, Vercel e, se usada, Anthropic têm cada uma o que recebem, a região de processamento e o instrumento contratual, ou a marcação 'a confirmar' com responsável.
- A seção da Vercel diz que ela não recebe vídeo, quadro, recorte de rosto nem observação por rosto, registra a região configurada das funções do painel e diz se o painel usa Routing Middleware e, se usar, que ele roda em todas as regiões.
- A decisão sobre enviar a transcrição dos cultos do piloto à API da Anthropic está registrada como 'sim' ou 'não'.
- Cada uma das seis regras do CLAUDE.md aparece em pelo menos um risco, com medida e forma de verificação, ou 'sem verificação automática' com medida manual e responsável. A regra 5 inclui o risco de fala da congregação captada e transcrita em transcript_segment.
- docs/law/br.md está no repositório público, diz o que uma igreja deve fazer antes de processar as próprias gravações e não cita dado da igreja do piloto.
- A lista de pendências impeditivas está no lugar que F7.5 consulta, cada uma com responsável e campo de data de resolução.
- Caminho de erro: o RIPD diz, para cada pendência de região ou contrato de operador, se ela impede o início do piloto. Um RIPD sem essa indicação é reprovado na revisão.
- Caminho de erro: se a igreja indicada não confirmar a participação ou não assinar o instrumento, o registro diz o motivo e a data, o RIPD não é aprovado, e F6.4, F6.5 e F6.6 não começam.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F6.3.T8 | Governança e Privacidade | Confirmar com a igreja indicada o piloto, o controlador e o encarregado e colher a assinatura do instrumento de instruções de tratamento | 5 | F6.2 (local privado dos documentos), F3.1.T2 (encarregado nomeado) |
| F6.3.T1 | DevOps | Levantar o que cada operador recebe, a região e o plano usados no piloto | 5 | F6.2, F2.6, F5.6, F5.6 (primeira task: confirmação do plano e dos termos de uso da Vercel, movida de F7.2.T2; pendência de F5) |
| F6.3.T2 | Data Science | Descrever o inventário de dados e avaliar o risco de reidentificação por agregado, evento e insight | 5 | F6.2, F6.3.T8, F5.4 (transitiva via F6.1) |
| F6.3.T3 | Governança e Privacidade | Redigir base legal, instrumentos contratuais, transferência internacional, retenção e a conclusão sobre F6.5 | 7 | F6.3.T8, F6.3.T1, F6.3.T2 |
| F6.3.T4 | Governança e Privacidade | Redigir riscos e medidas ligados às seis regras do CLAUDE.md | 5 | F6.3.T1 |
| F6.3.T5 | Governança e Privacidade | Escrever as notas de lei brasileira em docs/law/br.md | 3 | F6.3.T3 |
| F6.3.T6 | Governança e Privacidade | Registrar as pendências impeditivas no lugar que F7.5 consulta | 2 | F6.3.T4 |
| F6.3.T7 | Governança e Privacidade | Revisar o RIPD contra os critérios de aceite e registrar a aprovação do encarregado e do controlador | 4 | F6.3.T8, F6.3.T3, F6.3.T4, F6.3.T5, F6.3.T6 |
| F6.3.T9 | QA | Verificar os critérios de aceite do RIPD, do registro da igreja e de docs/law/br.md contra as fontes | 4 | F6.3.T7 |

<details><summary>F6.3.T8 · [Governança e Privacidade] Confirmar com a igreja indicada o piloto, o controlador e o encarregado e colher a assinatura do instrumento de instruções de tratamento</summary>

**Objetivo:** Ter registrados, antes da base legal do RIPD, a igreja do piloto, o controlador, o operador, o encarregado do piloto e o instrumento com os papéis e as instruções de tratamento assinado pela igreja e por Fabio Pinheiro.

**Passos previstos:**
1. Obter do pastor Filipe a indicação da igreja do piloto (dependência do épico) e registrar se ela é a PIB, como supõe P14
2. Confirmar com o pastor da igreja indicada a participação no piloto de 4 cultos (README.pt-BR.md:35) e quem representa a igreja na assinatura
3. Registrar com o encarregado e a igreja quem é o controlador e quem é operador no tratamento da Fase 1 (LGPD art. 5º, VI e VII), sem partir do controlador da Fase 0 registrado em F3.1.T2
4. Confirmar se o encarregado nomeado em F3.1.T2 atende também ao piloto ou obter a indicação de outro (art. 5º, VIII; art. 41)
5. Redigir com o encarregado o instrumento entre a igreja e Fabio Pinheiro com os papéis, as instruções de tratamento (art. 39), as decisões do ADR de F6.2 (o que se guarda, onde e por quanto tempo) e os operadores de nuvem usados (Hugging Face, Supabase, Vercel e, se usada, Anthropic)
6. Colher a assinatura do representante da igreja e de Fabio Pinheiro, com data
7. Gravar os registros e o instrumento assinado no local privado do ADR de F6.2 e informar a F6.4 a identificação e o contato do controlador e do encarregado (art. 9º, III e IV; art. 41, §1º)
8. Se a igreja não confirmar ou não assinar, registrar o motivo e a data e avisar F6.4, F6.5 e F6.6 de que não começam

**Definição de pronto:** Registro datado no local privado com a igreja do piloto, o controlador, o operador, o encarregado e o instrumento assinado pela igreja e por Fabio Pinheiro, ou registro do motivo pelo qual a igreja não confirmou ou não assinou.

**Dependências:** F6.2 (local privado dos documentos), F3.1.T2 (encarregado nomeado)

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F6.3.T1 · [DevOps] Levantar o que cada operador recebe, a região e o plano usados no piloto</summary>

**Objetivo:** Ter a tabela técnica de operadores do RIPD com fonte para cada célula.

**Passos previstos:**
1. Para Hugging Face, listar o que vai ao HF Jobs e seus logs, ao dataset do corpus, ao repositório de resultados (F2.6 e F2.8), ao destino de F7.1, ao destino dos rótulos do piloto decidido no ADR de F6.2 e ao Space de F3.3
2. Para Supabase, listar as tabelas que o Store grava (reacao/store.py:28-44), service e insight_feedback, e as contas do Supabase Auth
3. Para Vercel e Anthropic, registrar o que recebem a partir do ADR de F6.2 e do código (reacao/moments.py:53-63; reacao/insights.py:41-48)
4. Ler a região do projeto Supabase de desenvolvimento no painel do Supabase
5. Ler a região configurada das funções do projeto do painel na Vercel (iad1 é o padrão em projetos novos), o plano e os termos confirmados na primeira task de F5.6 e se o painel usa Routing Middleware
6. Montar a tabela com fonte e data em cada célula, ou 'a confirmar' com responsável

**Definição de pronto:** Tabela de operadores anexada ao PR do RIPD, com o que cada um recebe, região, plano e uso de Routing Middleware, com fonte e data em cada célula ou 'a confirmar' com responsável.

**Dependências:** F6.2, F2.6, F5.6, F5.6 (primeira task: confirmação do plano e dos termos de uso da Vercel, movida de F7.2.T2; pendência de F5)

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F6.3.T2 · [Data Science] Descrever o inventário de dados e avaliar o risco de reidentificação por agregado, evento e insight</summary>

**Objetivo:** Escrever as seções de inventário, de agregados e de reidentificação do RIPD com fonte em cada afirmação.

**Passos previstos:**
1. Listar as categorias de dado com o campo, a tabela ou o arquivo onde ficam, a partir do ADR de F6.2, incluindo rótulos de referência do piloto e rotuladores com acesso ao vídeo
2. Descrever os agregados: janela de 30 s, k-mínimo de 10 rostos mensuráveis, altura mínima de 64 px e janela insuficiente sem percentuais (reacao/types.py:5-8; reacao/aggregate.py:24-31)
3. Descrever o que eventos e insights expõem (minuto, momento, trecho de até 200 caracteres; reacao/insights.py:25) e o risco de o trecho citar terceiros
4. Pedir à igreja confirmada em F6.3.T8 o tamanho da plateia
5. Avaliar a reidentificação por agregado, evento e insight com os rostos por janela medidos na Fase 0 (n_total e n_mensuravel de F5.4) e o tamanho de plateia informado pela igreja, e registrar a conclusão
6. Escrever as seções com arquivo:linha em cada afirmação

**Definição de pronto:** Seções de inventário, de agregados e de reidentificação no PR do RIPD, com fonte em cada afirmação e a conclusão sobre reidentificação.

**Dependências:** F6.2, F6.3.T8, F5.4 (transitiva via F6.1)

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F6.3.T3 · [Governança e Privacidade] Redigir base legal, instrumentos contratuais, transferência internacional, retenção e a conclusão sobre F6.5</summary>

**Objetivo:** Ter no RIPD as seções que decidem a base legal em nome do controlador registrado, registram os contratos e acionam, ou não, F6.5.

**Passos previstos:**
1. Ler em F6.3.T8 quem é o controlador e o operador e registrar no RIPD os papéis e o instrumento assinado
2. Escolher com o encarregado a hipótese do art. 11 e escrever a justificativa
3. Registrar, para cada operador de nuvem, o instrumento contratual aplicável ao plano usado. Para a Vercel, registrar que o DPA vale para Pro e Enterprise e lista GDPR, UK DPA 2018, CCPA, PIPEDA e a lei australiana como exemplos, sem citar a LGPD (https://vercel.com/legal/dpa), e a avaliação do encarregado para o art. 33
4. Escrever a transferência internacional (art. 33) por operador, a partir da tabela de F6.3.T1
5. Registrar a decisão sobre a Anthropic para os cultos do piloto (P26), partindo da decisão de Fabio para a Fase 0 registrada em D7 de F2.4.T4
6. Registrar a retenção (ADR de F6.2) e o encarregado (art. 41)
7. Escrever a conclusão 'F6.5 necessário: sim' ou 'não'

**Definição de pronto:** Seções de papéis, base legal, instrumentos contratuais, transferência, retenção e encarregado no PR do RIPD, com a conclusão sobre F6.5.

**Dependências:** F6.3.T8, F6.3.T1, F6.3.T2

**Estimativa sugerida:** 7 h (sugestão; validar com o time)

</details>

<details><summary>F6.3.T4 · [Governança e Privacidade] Redigir riscos e medidas ligados às seis regras do CLAUDE.md</summary>

**Objetivo:** Ter no RIPD a seção de riscos, com medida e verificação para cada regra e para cada pendência de operador.

**Passos previstos:**
1. Para cada regra do CLAUDE.md, listar o risco, a medida e onde ela é verificada: reacao/guard.py e passo do CI; allowed_modules e teste; k-mínimo em reacao/aggregate.py; reacao/lint.py; tests/test_schema.py; RLS de F7.2
2. Para a regra 5, registrar o risco de fala da congregação captada pela trilha e transcrita em transcript_segment (reacao/transcribe.py:13; reacao/store.py:34-35), a medida decidida no ADR de F6.2 e, como não há teste nem passo do CI, 'sem verificação automática' com a medida manual e o responsável
3. Acrescentar os riscos da nuvem: logs de job e da Vercel, histórico do dataset, Routing Middleware em todas as regiões e chave de serviço só nos jobs
4. Indicar, para cada pendência de operador, se ela impede o início do piloto

**Definição de pronto:** Seção de riscos no PR do RIPD, cobrindo as seis regras, com a regra 5 marcada 'sem verificação automática' e medida manual, e as pendências de operador com a indicação de impedimento.

**Dependências:** F6.3.T1

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F6.3.T5 · [Governança e Privacidade] Escrever as notas de lei brasileira em docs/law/br.md</summary>

**Objetivo:** Criar docs/law/br.md conforme CONTRIBUTING.md:12.

**Passos previstos:**
1. Resumir o que uma igreja deve fazer antes de processar as próprias gravações: definir controlador e operador, base legal para dado sensível, aviso, RIPD, encarregado e transferência internacional
2. Citar os artigos da LGPD com a URL oficial
3. Conferir que o texto não traz dado da igreja do piloto
4. Abrir PR no repositório público citando F6.3

**Definição de pronto:** docs/law/br.md no PR do repositório público, com os artigos citados e sem dado da igreja do piloto.

**Dependências:** F6.3.T3

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F6.3.T6 · [Governança e Privacidade] Registrar as pendências impeditivas no lugar que F7.5 consulta</summary>

**Objetivo:** Deixar cada pendência que impede o piloto com responsável e campo de resolução num registro que F7.5 lê.

**Passos previstos:**
1. Extrair da seção de riscos de F6.3.T4 as pendências marcadas como impeditivas
2. Criar o registro no local privado do ADR de F6.2, com pendência, responsável, data de abertura e campo para a data de resolução
3. Informar o caminho do registro a F7.5

**Definição de pronto:** Registro das pendências impeditivas no local privado, com responsável e campo de resolução, e caminho informado a F7.5.

**Dependências:** F6.3.T4

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F6.3.T7 · [Governança e Privacidade] Revisar o RIPD contra os critérios de aceite e registrar a aprovação do encarregado e do controlador</summary>

**Objetivo:** Verificar o PBI documental por revisão do encarregado e de Fabio Pinheiro, que são os revisores, e registrar as aprovações do RIPD.

**Passos previstos:**
1. O encarregado e Fabio Pinheiro conferem cada critério de aceite, incluindo o registro de F6.3.T8 e o instrumento assinado
2. Registrar a lista de critérios com 'passou' ou 'não passou'
3. Devolver à redação o que não passou
4. Registrar no RIPD a aprovação do encarregado e a do controlador registrado em F6.3.T8, a data e a versão, e gravá-lo no local privado do ADR de F6.2

**Definição de pronto:** RIPD versionado, datado e aprovado pelo encarregado e pelo controlador no local privado, docs/law/br.md mesclado no repositório público, e a lista de critérios conferida pelo encarregado e por Fabio Pinheiro.

**Dependências:** F6.3.T8, F6.3.T3, F6.3.T4, F6.3.T5, F6.3.T6

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F6.3.T9 · [QA] Verificar os critérios de aceite do RIPD, do registro da igreja e de docs/law/br.md contra as fontes</summary>

**Objetivo:** Uma pessoa de QA do time, que não redigiu o RIPD, confere cada critério de aceite de F6.3 contra a fonte citada e marca 'passou' ou 'não passou', depois das aprovações de F6.3.T7.

**Passos previstos:**
1. Receber leitura no local privado decidido no ADR de F6.2, conforme a lista de acesso desse ADR
2. Conferir o registro de F6.3.T8: igreja, controlador, operador e encarregado com data anterior à aprovação do RIPD, e o instrumento com as assinaturas da igreja e de Fabio Pinheiro, ou o registro do motivo e da data se a igreja não confirmou
3. Conferir no RIPD data, versão, responsável e as aprovações do encarregado e do controlador registrado em F6.3.T8
4. Comparar cada item do inventário e cada prazo com a tabela de retenção do ADR de F6.2; prazo diferente ou item ausente reprova
5. Conferir que a seção de base legal cita uma hipótese do art. 11 com justificativa e termina com 'F6.5 necessário: sim' ou 'não'
6. Conferir que cada célula da tabela de operadores de F6.3.T1 tem fonte e data ou 'a confirmar' com responsável, que a seção da Vercel traz a região das funções, o uso de Routing Middleware e o plano confirmado na primeira task de F5.6, e que a decisão sobre a Anthropic está como 'sim' ou 'não'
7. Para cada uma das seis regras do CLAUDE.md, abrir o arquivo ou o passo do CI citado como verificação e confirmar que existe; a regra 5 deve estar como 'sem verificação automática', com medida manual e responsável
8. Conferir que cada pendência de região ou contrato de operador diz se impede o piloto e que as impeditivas estão no registro de F6.3.T6, com responsável e campo de data de resolução, no lugar que F7.5 consulta
9. Conferir que docs/law/br.md está no repositório público e buscar nele e no histórico do repositório público o nome da igreja do piloto, do controlador e do representante; qualquer ocorrência reprova
10. Registrar no local privado a lista de critérios com 'passou' ou 'não passou' e a evidência de cada um, e devolver a F6.3.T7 o que não passou

**Definição de pronto:** Relatório de verificação no local privado com 'passou' ou 'não passou' e a evidência de cada critério de aceite de F6.3, sem divergência aberta.

**Dependências:** F6.3.T7

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- README.pt-BR.md:35,39
- docs/poc-gate.md:50
- docs/onprem.md:68
- CONTRIBUTING.md:12
- supabase/migrations/0001_init.sql:2,4,17
- reacao/store.py:28-44
- reacao/transcribe.py:13
- reacao/moments.py:53-63
- reacao/insights.py:41-48
- labels/README.md:6,11,16
- .github/workflows/ci.yml (sem passo ligado à regra 5)
- https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm (art. 5º II, VI, VII, VIII e XVII, 11, 38, 39 e 41 conferidos no texto obtido pela leitura web do Exa em 2026-09-23; art. 33 via levantamento mapa_produto)
- epico.json (dependências: indicação da igreja do piloto pelo pastor Filipe; igreja do piloto e equipe de mídia)
- feature_F3_v3.json (F3.1.T2: controlador da Fase 0 e nomeação do encarregado)
- https://huggingface.co/docs/hub/jobs-manage
- https://vercel.com/docs/functions/configuring-functions/region (seção Limits)
- https://vercel.com/docs/regions
- https://vercel.com/legal/dpa (Last Updated March 17, 2026; leitura de 2026-09-23)
- https://vercel.com/docs/logs/runtime
- https://supabase.com/docs/guides/platform/migrating-to-supabase/auth0
- https://api.github.com/repos/ds-fabiopinheiro/church-sentiment-analysis (visibility public, 2026-09-23)
- arvore_v1.json (F1.3, F2.5, F3.3, F7.1)
- feature_F6.json (F6.3); premissas P14, P26, P30; P3 revisada
- consolidacao.json (problemas 'F4.3, F6.3' e 'F7.2.T2 (mover para F5.6)'); feature_det_F2.json (F2.4.T4, D7 e D8; F2.8)

#### Verificação INVEST: pontos que falharam
- Independente: depende de F6.2, de F3.1.T2 e de informação e assinatura de fora do time (igreja do piloto, plano da Vercel, encarregado, tamanho da plateia).
- Estimável: o esforço de redação depende da base legal escolhida e do número de pendências de operador, e a duração de F6.3.T8 depende da agenda da igreja.
- Small: 40 h sugeridas. Se não couber numa sprint, dividir em 'igreja, controlador e instrumento' (F6.3.T8) e 'RIPD, notas de lei e verificação' (F6.3.T1 a T7 e T9).

#### Premissas
- O encarregado é nomeado em F3.1.T2, ainda sem nome nem data. Sem ele, o RIPD não é aprovado.
- Quem é controlador e quem é operador no tratamento da Fase 1 não está registrado no repositório. F6.3.T8 não parte do controlador da Fase 0 registrado em F3.1.T2, porque a Fase 1 trata cultos inteiros e acrescenta Supabase e Vercel.
- A forma escrita e assinada do instrumento de papéis e instruções de tratamento é proposta desta revisão. O art. 39 da LGPD diz que o operador trata segundo as instruções do controlador, sem fixar forma.
- A aprovação do RIPD pelo controlador é leitura desta revisão do art. 5º, XVII ('documentação do controlador'), a validar com o encarregado.
- A região de processamento do HF Jobs não aparece no levantamento e entra como 'a confirmar'.
- O DPA da Vercel foi lido em 2026-09-23. A definição de leis aplicáveis traz exemplos e não cita a LGPD. Cabe ao encarregado avaliar se isso basta para o art. 33.
- A igreja do piloto é a PIB (P14), a confirmar em F6.3.T8.
- Os destinos possíveis dos vídeos do piloto são repositório privado ou Storage Bucket (P30). Se F7.1 ainda não tiver escolhido, o RIPD descreve os dois.
- Proposta desta árvore, a validar com o encarregado: uma nova versão do RIPD quando mudar operador, região, base legal, prazo de retenção, controlador ou rótulo previsto em F6.6.
- As disciplinas são as da árvore. A leitura de DPA e de instrumento contratual passou de F6.3.T1 (DevOps) para F6.3.T3 (Governança e Privacidade), por ser leitura legal. A confirmação da igreja e do controlador (F6.3.T8) também é Governança e Privacidade. Por ser PBI documental, a revisão de conteúdo é do encarregado e de Fabio Pinheiro (F6.3.T7), e a verificação dos critérios de aceite contra as fontes é a task de QA F6.3.T9.
- A avaliação de reidentificação usa o tamanho de plateia informado pela igreja confirmada em F6.3.T8, que ainda não foi pedido.
- O site do Planalto respondeu HTTP 503 ao acesso direto em 2026-09-23. Os arts. 5º, 11, 38, 39 e 41 foram conferidos no texto da mesma URL obtido pela leitura web do Exa na mesma data; o art. 33 vem do levantamento.
- Quem executa F6.3.T9 é uma pessoa de QA do time sem papel na redação do RIPD, com leitura no local privado concedida conforme o ADR de F6.2. O nome não está registrado; é proposta desta reconciliação.
- Story points subiram de 5 para 8 pela avaliação de reidentificação, pelo inventário de rótulos e pela lista de pendências impeditivas, e de 8 para 13 pela task F6.3.T8, que depende de confirmação e assinatura de fora do time (36 h sugeridas no total, 40 h com a task de QA F6.3.T9). Story points e horas são sugestão, a validar no refinamento (P6).

#### Pendências para sincronizar
- Time (Area Path), Sprint e Responsável
- Story Points (sugestão: 13)
- Vínculo pai: Feature F6. Predecessores: F6.2 e F3.1. Sucessores: F6.4, F6.5, F6.6, F7.1, F7.4 e F7.5
- Nome da pessoa de QA que executa F6.3.T9 e o acesso de leitura dela ao local privado do ADR de F6.2
- Plano e termos de uso da Vercel confirmados na primeira task de F5.6 (ref a criar em F5)
- Nome do encarregado de dados (F3.1.T2)
- Indicação da igreja do piloto pelo pastor Filipe e representante da igreja que assina o instrumento
- Região de processamento do HF Jobs
- Região e contrato do projeto Supabase de desenvolvimento (F2.6)
- Tamanho da plateia da igreja do piloto
- Registrar em F7.5 o caminho da lista de pendências impeditivas
- Registrar em F7.1.T3 a dependência de F6.3.T8

## Preview — PBI F6.4 (novo) · Redigir o aviso à congregação e definir canal, prazo e atendimento a pedidos

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Redigir o aviso à congregação e definir canal, prazo e atendimento a pedidos |
| Tipo | Product Backlog Item |
| Pai | F6 |
| Tags | fase-1; privacidade; aviso; linguagem-controlada; governanca |
| Estimativa | 5 pts (sugestão); tasks: 16 h |
| Dependências | F1.7, F6.3, F6.3.T8 (igreja, controlador e encarregado confirmados; parte de F6.3), F6.5 (condicional, P29), F6.2 (local privado dos documentos; transitiva via F6.3) |
| Substitui | nenhum |

#### Descrição

Como pessoa da congregação da igreja do piloto  
Quero receber antes do primeiro culto do piloto, por um canal da igreja, um aviso que diga o que é medido, o que nunca é feito, quem é o controlador, quem vê o resultado, por quanto tempo ele fica guardado e a quem pedir informações ou a retirada de um culto  
Para saber do tratamento antes de participar do culto gravado e poder pedir informações, pedir a retirada depois da gravação ou, se F6.5 existir, usar a forma de oposição ou consentimento

**Contexto:** O README exige aviso à congregação antes da Fase 1 (README.pt-BR.md:35), e o repositório não tem texto nem modelo de aviso. O art. 9º da LGPD lista as informações a que o titular tem acesso, entre elas a identificação e o contato do controlador (incisos III e IV), e o contato do encarregado deve ser divulgado publicamente (art. 41, §1º) (https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm). A igreja do piloto, o controlador e o encarregado são confirmados em F6.3.T8. As garantias que o aviso pode citar estão em 'O que nunca faz' (README.pt-BR.md:16-21). A linguagem controlada vale para textos a pastores (CLAUDE.md, regra 4) e é aplicada pelo lint (reacao/lint.py:8-13), que F1.7 amplia. A árvore estende essa checagem ao aviso. As listas atuais apontam termos nas próprias garantias: README.pt-BR.md:19 casa com 'assento' e a linha 20 com 'sentiram', e uma frase como 'o sistema nunca infere sentimentos' também é apontada (execução das listas de reacao/lint.py:8-13 em 2026-09-23). F1.7 acrescenta termos como membro e setor, que podem atingir README.pt-BR.md:18-19,21. Por isso a checagem precisa registrar exceções aprovadas. reacao/lint.py só expõe check(Insight), que também exige minuto, momento, trecho e sinais (reacao/lint.py:23-49), e _sem_citacao só isenta aspas com conteúdo do trecho do insight (reacao/lint.py:16-20); não há checagem de texto livre. A transcrição usa a trilha inteira do arquivo, sem separar quem fala (reacao/transcribe.py:13), então o aviso não pode dizer que só o púlpito é transcrito sem que o ADR de F6.2 e o RIPD o garantam. O conteúdo sobre operadores, retenção e encarregado vem do RIPD (F6.3), e a forma de oposição ou consentimento vem de F6.5, se ele for acionado. Canais em discussão: boletim, telão ou site da igreja. Pela P3 revisada, o painel web na Vercel só atende perfis autenticados e por isso não é canal do aviso. O repositório é público, e os registros do aviso vão para o local privado do ADR de F6.2.

**Regras de negócio:**
- RN01 – O texto passa pela checagem das listas PROIBIDO e PROIBIDO_INDIVIDUAL do lint, na versão de F1.7, frase a frase. Cada termo apontado é removido pela reescrita ou entra numa lista de exceções aprovada pelo encarregado. Só podem ser exceção frases que negam um tratamento (garantias de README.pt-BR.md:16-21) e a descrição da forma de F6.5.
- RN02 – O aviso diz o que é medido (reação observada, agregada por janela de 30 s, e a transcrição da trilha de áudio do arquivo, que pode incluir falas captadas além do púlpito, conforme a decisão sobre a transcrição do ADR de F6.2 registrada no RIPD), o que o sistema nunca faz (README.pt-BR.md:16-21), quem recebe o resultado, o prazo de retenção do RIPD, a identificação e o contato do controlador confirmado em F6.3.T8 (LGPD art. 9º, III e IV) e o contato do encarregado (art. 41, §1º).
- RN03 – Se F6.5 for acionado, o aviso descreve a forma de oposição ou consentimento registrada.
- RN04 – O aviso é publicado antes do primeiro dos 4 cultos do piloto. A antecedência mínima é definida com a igreja neste PBI.
- RN05 – O atendimento a pedidos responde sem identificar ninguém na gravação (CLAUDE.md, regra 2).
- RN06 – O aviso não afirma nada que o RIPD não registre.
- RN07 – O pastor da igreja do piloto e o encarregado aprovam o texto antes da publicação.
- RN08 – Para pedido de exclusão ou de oposição feito depois da gravação, o procedimento diz as respostas possíveis sem localizar a pessoa (por exemplo, retirar o culto inteiro do processamento ou apagar o vídeo no destino de F7.1), quem decide e o prazo, com aprovação do encarregado.
- RN09 – O texto aprovado, as aprovações, a lista de exceções e o registro de publicação ficam no local privado decidido no ADR de F6.2.

**Fora de escopo:**
- Publicar o aviso no painel web na Vercel, que só atende perfis autenticados
- Definir a forma de oposição ou consentimento (F6.5)
- Confirmar a igreja do piloto e o controlador (F6.3.T8)
- Alterar a função check de reacao/lint.py; a checagem de texto livre é uma função nova que usa as mesmas listas
- Traduzir o aviso
- Aviso para outras igrejas

#### Critérios de aceite

- A checagem de texto livre com as listas PROIBIDO e PROIBIDO_INDIVIDUAL, na versão de F1.7, roda sobre cada frase do texto aprovado, e cada termo apontado tem registro 'removido' ou 'exceção aprovada' pelo encarregado. Nenhum termo apontado fica sem registro.
- As exceções aprovadas são só frases que negam um tratamento (garantias de 'O que nunca faz') ou descrevem a forma de F6.5.
- O texto diz o que é medido, incluindo que a transcrição vem da trilha de áudio do arquivo conforme o RIPD, o que nunca é feito, quem recebe o resultado, o prazo de retenção, a identificação e o contato do controlador registrado em F6.3.T8, o contato do encarregado e, se F6.5 foi acionado, qual é a forma de oposição ou consentimento.
- Cada afirmação do aviso sobre tratamento, controlador, operador ou prazo tem correspondente no RIPD ou no registro de F6.3.T8.
- O registro de publicação tem canal, data, responsável e a data do primeiro culto do piloto, e a data de publicação respeita a antecedência mínima combinada com a igreja.
- O procedimento de atendimento diz quem responde, por qual canal e em que prazo, e diz que a resposta não envolve localizar a pessoa na gravação.
- O procedimento diz as respostas possíveis a pedido de exclusão ou de oposição feito depois da gravação, sem localizar a pessoa, quem decide e o prazo, com aprovação do encarregado.
- O pastor da igreja do piloto e o encarregado aprovaram o texto, com data.
- O texto aprovado, as aprovações, a lista de exceções e o registro de publicação estão no local privado decidido no ADR de F6.2.
- Caminho de erro: uma frase com termo proibido que não é garantia nem descrição da forma de F6.5 é reprovada na checagem e volta à redação.
- Caminho de erro: sem registro de publicação anterior ao primeiro culto, o aviso não conta como em vigor, e o registro diz isso.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F6.4.T1 | Governança e Privacidade | Redigir o aviso a partir do RIPD e das garantias do README, com a lista de exceções | 5 | F1.7, F6.3, F6.3.T8, F6.5 (se acionado) |
| F6.4.T2 | Governança e Privacidade | Definir com a igreja canal, antecedência e atendimento a pedidos e registrar a publicação | 5 | F6.4.T1, F6.3.T8 |
| F6.4.T3 | Backend | Criar a checagem de texto livre com as listas do lint | 3 | F1.7 |
| F6.4.T4 | QA | Verificar o aviso com a checagem de texto livre e os critérios de aceite | 3 | F6.4.T1, F6.4.T2, F6.4.T3 |

<details><summary>F6.4.T1 · [Governança e Privacidade] Redigir o aviso a partir do RIPD e das garantias do README, com a lista de exceções</summary>

**Objetivo:** Ter o texto do aviso e a lista de exceções aprovados pelo pastor da igreja do piloto e pelo encarregado.

**Passos previstos:**
1. Listar o que o RIPD manda informar: medição, descrição da transcrição, operadores, retenção e encarregado
2. Ler em F6.3.T8 a identificação e o contato do controlador e o contato do encarregado
3. Escrever o texto a partir de 'O que nunca faz' (README.pt-BR.md:16-21), reescrevendo as garantias sem os termos das listas do lint quando possível
4. Para cada garantia que precise do termo para negar o tratamento, propor a frase como exceção ao encarregado
5. Incluir a forma de F6.5, se ela tiver sido acionada
6. Enviar ao pastor da igreja do piloto e ao encarregado para aprovação do texto e da lista de exceções

**Definição de pronto:** Texto, com a identificação e o contato do controlador e o contato do encarregado, e lista de exceções gravados no local privado do ADR de F6.2, com as aprovações datadas do pastor da igreja do piloto e do encarregado.

**Dependências:** F1.7, F6.3, F6.3.T8, F6.5 (se acionado)

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F6.4.T2 · [Governança e Privacidade] Definir com a igreja canal, antecedência e atendimento a pedidos e registrar a publicação</summary>

**Objetivo:** Ter o aviso publicado no prazo, com procedimento de atendimento definido, inclusive para pedidos depois da gravação.

**Passos previstos:**
1. Combinar com a igreja confirmada em F6.3.T8 o canal (boletim, telão ou site) e a antecedência mínima antes do primeiro culto
2. Escrever o procedimento de atendimento a pedidos de informação: quem responde, canal, prazo e resposta sem localizar a pessoa na gravação
3. Escrever as respostas possíveis a pedido de exclusão ou de oposição depois da gravação (por exemplo, retirar o culto inteiro do processamento ou apagar o vídeo no destino de F7.1), quem decide e o prazo, e obter a aprovação do encarregado
4. Registrar a publicação com canal, data e responsável
5. Registrar a data do primeiro culto do piloto

**Definição de pronto:** Registro de publicação e procedimento de atendimento, com as respostas a pedidos depois da gravação aprovadas pelo encarregado, gravados no local privado, com data de publicação anterior ao primeiro culto.

**Dependências:** F6.4.T1, F6.3.T8

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F6.4.T3 · [Backend] Criar a checagem de texto livre com as listas do lint</summary>

**Objetivo:** Permitir aplicar as listas PROIBIDO e PROIBIDO_INDIVIDUAL a um texto que não é insight.

**Passos previstos:**
1. Criar uma função que aplica só PROIBIDO e PROIBIDO_INDIVIDUAL, na versão de F1.7, a um texto livre, frase a frase, e devolve os termos apontados por frase, sem exigir minuto, momento, trecho nem sinais
2. Escrever teste com as garantias de README.pt-BR.md:19-20, com a frase 'o sistema nunca infere sentimentos' e com frases neutras, conferindo o que é apontado
3. Rodar ruff check e pytest

**Definição de pronto:** Função e teste num PR citando F6.4, com ruff e pytest passando e o teste mostrando os termos apontados nas linhas 19 e 20 do README.

**Dependências:** F1.7

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F6.4.T4 · [QA] Verificar o aviso com a checagem de texto livre e os critérios de aceite</summary>

**Objetivo:** Marcar cada critério de aceite de F6.4 como 'passou' ou 'não passou' com evidência.

**Passos previstos:**
1. Rodar a checagem de F6.4.T3 sobre cada frase do aviso aprovado e anexar a saída
2. Para cada termo apontado, conferir o registro 'removido' ou 'exceção aprovada' e que a exceção é garantia ou descrição da forma de F6.5
3. Rodar de propósito as garantias de README.pt-BR.md:16-21 e confirmar que a checagem aponta os termos das linhas 19 e 20
4. Inserir numa cópia do texto uma frase proibida que não é garantia e confirmar que ela é reprovada
5. Conferir cada afirmação do aviso contra o RIPD e o registro de F6.3.T8, incluindo a descrição da transcrição e a identificação e o contato do controlador
6. Conferir aprovações, datas, antecedência, procedimento de atendimento e respostas a pedidos depois da gravação
7. Conferir que os documentos estão no local privado do ADR de F6.2

**Definição de pronto:** Relatório no local privado com a saída da checagem e 'passou' ou 'não passou' para cada critério.

**Dependências:** F6.4.T1, F6.4.T2, F6.4.T3

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- README.pt-BR.md:16-21,35
- CLAUDE.md (regras 2 e 4)
- reacao/lint.py:8-13,16-20,23-49
- reacao/transcribe.py:13
- https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm (art. 9º, III e IV; art. 41, §1º; conferidos no texto obtido pela leitura web do Exa em 2026-09-23)
- execução das listas PROIBIDO e PROIBIDO_INDIVIDUAL sobre README.pt-BR.md:16-21 (2026-09-23): linha 19 aponta 'assento', linha 20 aponta 'sentiram'
- arvore_v1.json (F1.7, F7.1)
- feature_F6.json (F6.4); premissas P14 e P29; P3 revisada

#### Verificação INVEST: pontos que falharam
- Independente: depende de F6.3 (inclusive F6.3.T8), de F1.7 e, se ele for acionado, de F6.5.
- Testável em parte: o critério de antecedência só fecha quando a data do primeiro culto for definida.

#### Premissas
- A checagem do aviso com o lint é regra desta árvore (valor observável de F6.4). A regra 4 do CLAUDE.md fala de textos para pastores.
- Backend foi acrescentado às disciplinas da árvore, porque a checagem de texto livre precisa de uma função nova (reacao/lint.py:23-49 só aceita Insight).
- Os termos de F1.7 que atingem as garantias dependem da regex que F1.7 adotar; a checagem registra o que for apontado.
- A data do primeiro culto do piloto ainda não está definida.
- O prazo de resposta a pedidos é definido com a igreja e o encarregado. Esta árvore não fixa número.
- Incluir no aviso a identificação e o contato do controlador é leitura desta revisão do art. 9º, III e IV, a validar com o encarregado.
- A igreja do piloto é a PIB (P14), a confirmar em F6.3.T8.
- Story points subiram de 3 para 5 (sugestão) pela task de Backend e pelo procedimento de pedidos depois da gravação. Story points e horas são sugestão, a validar no refinamento (P6).

#### Pendências para sincronizar
- Time (Area Path), Sprint e Responsável
- Story Points (sugestão: 5)
- Vínculo pai: Feature F6. Predecessores: F1.7, F6.3 (com F6.3.T8) e F6.5 (se acionado). Sucessor: F7.5
- Data do primeiro culto do piloto
- Identificação e contato do controlador e contato do encarregado (F6.3.T8)
- Canal escolhido pela igreja

## Preview — PBI F6.5 (novo) · Definir com a igreja uma forma de oposição ou de consentimento que não exija identificação, conforme a base legal do RIPD

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Definir com a igreja uma forma de oposição ou de consentimento que não exija identificação, conforme a base legal do RIPD |
| Tipo | Product Backlog Item |
| Pai | F6 |
| Tags | fase-1; privacidade; lgpd; condicional; governanca |
| Estimativa | 3 pts (sugestão); tasks: 11 h |
| Dependências | F6.3, F6.3.T8 (igreja e controlador confirmados; parte de F6.3), F6.2 (local privado dos documentos; transitiva via F6.3) |
| Substitui | nenhum |

#### Descrição

Como pessoa da congregação da igreja do piloto que não quer ter a reação medida  
Quero uma forma de oposição, ou de consentimento, que eu possa usar sem dar nome, documento ou imagem  
Para exercer a escolha que a base legal do RIPD prevê sem que o sistema precise me identificar

**Contexto:** Item condicional: entra se a base legal registrada no RIPD (F6.3) exigir consentimento ou oferta de oposição (P29). Para dado sensível, o art. 11 da LGPD separa o tratamento com consentimento (inciso I) das hipóteses sem consentimento (inciso II) (https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm). A regra 2 do CLAUDE.md proíbe identificação, embedding e rastreamento, então a forma não pode depender de saber quem é a pessoa. A árvore levantou dois exemplos: área fora do enquadramento da câmera e culto sem gravação. Os dois são formas de oposição. O pipeline processa o quadro inteiro que recebe (processar_culto.py:68-78), então uma área fora do enquadramento depende da posição da câmera. O repositório não registra quem controla a câmera na igreja do piloto; a equipe de mídia existe como perfil previsto (supabase/migrations/0001_init.sql:21) e envia o vídeo em F7.1. A igreja do piloto e o controlador são confirmados em F6.3.T8. O registro precisa existir antes do primeiro culto, ser divulgado pelo aviso de F6.4 e ficar num caminho que F7.5 lê. O repositório é público, e o local privado dos documentos do piloto é decidido no ADR de F6.2.

**Regras de negócio:**
- RN01 – O item é acionado só se o RIPD registrar 'F6.5 necessário: sim'.
- RN02 – A forma não coleta nome, documento, imagem ou outro identificador da pessoa (CLAUDE.md, regra 2).
- RN03 – A forma está em vigor antes do primeiro culto do piloto e é divulgada pelo aviso de F6.4.
- RN04 – O registro diz quem confere, em cada culto, que a forma está em vigor, e fica num caminho fixado por este PBI dentro do local privado decidido no ADR de F6.2. F7.5 lê desse caminho.
- RN05 – Se a forma for área fora do enquadramento, a conferência é feita olhando o enquadramento ao vivo, sem gravar quadro (CLAUDE.md, regra 1).
- RN06 – A forma atende ao que a hipótese legal do RIPD exige (consentimento ou oferta de oposição), e o encarregado registra essa conferência com a justificativa.

**Fora de escopo:**
- Coleta de consentimento individual com identificação
- Alterar o pipeline para mascarar ou excluir regiões do quadro. Se for necessário, entra como PBI novo
- Manter lista de pessoas que se opuseram
- Alterar F7.5; este PBI só informa o caminho do registro

#### Critérios de aceite

- Se o RIPD registra 'F6.5 necessário: não', o item é fechado com o link para essa seção do RIPD e nenhum registro de forma é criado.
- Se acionado, o registro descreve a forma, onde ela vale, quem confere em cada culto e a data de início, que é anterior ao primeiro culto do piloto.
- A forma não pede nome, documento, imagem nem outro identificador, e o encarregado registra essa conferência.
- O encarregado registra que a forma atende ao que a hipótese do RIPD exige (consentimento ou oferta de oposição), com a justificativa.
- O pastor da igreja do piloto confirmada em F6.3.T8 e o encarregado aprovaram o registro, com data.
- Se a forma for área fora do enquadramento, a pessoa que a igreja indicar para operar a câmera registra, com data anterior ao primeiro culto, que a área não aparece no enquadramento da câmera usada no piloto.
- O registro está no caminho fixado neste PBI, dentro do local privado do ADR de F6.2, e o caminho foi informado a F7.5.
- Caminho de erro: se a área aparecer no enquadramento, a forma não entra em vigor, e o registro diz o motivo e a nova data prevista.
- Caminho de erro: se nenhuma forma compatível com a regra 2 atende à hipótese do RIPD, o registro diz isso, F6.3 é reaberto para rever a base legal e o piloto não começa.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F6.5.T1 | Governança e Privacidade | Levantar com a igreja e o encarregado as formas compatíveis com a regra 2 e com a hipótese legal e registrar a escolhida | 5 | F6.3, F6.3.T8 |
| F6.5.T2 | Governança e Privacidade | Redigir o registro da forma e o roteiro de conferência por culto num caminho fixo | 3 | F6.5.T1 |
| F6.5.T3 | QA | Verificar a forma em vigor antes do primeiro culto e os critérios de aceite | 3 | F6.5.T2 |

<details><summary>F6.5.T1 · [Governança e Privacidade] Levantar com a igreja e o encarregado as formas compatíveis com a regra 2 e com a hipótese legal e registrar a escolhida</summary>

**Objetivo:** Ter uma forma de oposição ou consentimento escolhida, compatível com a hipótese do RIPD e aprovada pela igreja e pelo encarregado.

**Passos previstos:**
1. Ler no RIPD a hipótese legal e o que ela exige (consentimento ou oferta de oposição)
2. Ler em F6.3.T8 qual é a igreja do piloto e quem a representa
3. Listar opções que não identificam ninguém, como área fora do enquadramento ou culto sem gravação, com o que cada uma exige da igreja
4. Registrar com o encarregado, para cada opção, se ela atende à hipótese legal, com justificativa
5. Confirmar com a igreja quem controla a posição da câmera
6. Reunir com o pastor da igreja do piloto, a equipe de mídia e o encarregado e escolher a forma
7. Registrar a escolha, com data e aprovações, ou registrar que nenhuma forma atende e pedir a reabertura de F6.3

**Definição de pronto:** Forma escolhida registrada no local privado do ADR de F6.2, com a conferência do encarregado sobre a hipótese legal e a aprovação datada do pastor da igreja do piloto e do encarregado, ou o registro de que nenhuma forma atende.

**Dependências:** F6.3, F6.3.T8

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F6.5.T2 · [Governança e Privacidade] Redigir o registro da forma e o roteiro de conferência por culto num caminho fixo</summary>

**Objetivo:** Deixar o registro pronto para F6.4 divulgar e F7.5 ler.

**Passos previstos:**
1. Descrever a forma, onde ela vale e a data de início
2. Escrever o roteiro de conferência por culto: quem confere, quando e como, sem gravar quadro
3. Fixar o caminho do registro dentro do local privado decidido no ADR de F6.2 e gravar o registro nele
4. Informar o caminho a F7.5 e o texto a F6.4

**Definição de pronto:** Registro e roteiro de conferência gravados no caminho fixado, com o caminho informado a F7.5 e o texto informado a F6.4.

**Dependências:** F6.5.T1

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F6.5.T3 · [QA] Verificar a forma em vigor antes do primeiro culto e os critérios de aceite</summary>

**Objetivo:** Confirmar que a forma atende à hipótese legal, está em vigor antes do primeiro culto e cumpre os critérios.

**Passos previstos:**
1. Conferir no registro a descrição, o responsável, a data de início e as aprovações
2. Conferir que a forma não pede nenhum identificador
3. Conferir o registro do encarregado de que a forma atende à hipótese do RIPD
4. Se a forma for área fora do enquadramento, acompanhar a pessoa indicada pela igreja na conferência ao vivo do enquadramento, sem gravar quadro, e registrar o resultado com data
5. Conferir que o registro está no caminho fixado e que o caminho foi informado a F7.5
6. Marcar cada critério como 'passou' ou 'não passou'

**Definição de pronto:** Relatório de verificação no local privado com o resultado de cada critério e a data da conferência do enquadramento, quando aplicável.

**Dependências:** F6.5.T2

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm (art. 11, I e II; conferido no texto obtido pela leitura web do Exa em 2026-09-23)
- CLAUDE.md (regras 1 e 2)
- README.pt-BR.md:35
- processar_culto.py:68-78
- supabase/migrations/0001_init.sql:21 (perfil midia)
- arvore_v1.json (F7.1, F7.5)
- feature_F6.json (F6.5); premissas P14 e P29

#### Verificação INVEST: pontos que falharam
- Valiosa só se acionado: com 'F6.5 necessário: não', o item fecha sem entrega.
- Estimável: o esforço muda com a forma escolhida. Uma área sem câmera exige conferência a cada culto, e um culto sem gravação exige combinar agenda.

#### Premissas
- Quem controla a posição e o enquadramento da câmera na igreja do piloto não está registrado no repositório. Esta árvore supõe que seja a equipe de mídia, a confirmar com a igreja.
- Área fora do enquadramento e culto sem gravação são formas de oposição. Se a hipótese for o consentimento, é dedução desta revisão que elas não bastam sozinhas; o encarregado decide.
- Dedução de RN01 a RN03: se a base legal exigir a forma e nenhuma forma compatível com a regra 2 for aceita pela igreja ou atender à hipótese, o piloto não começa.
- A igreja do piloto é a PIB (P14), a confirmar em F6.3.T8.
- Story points e horas são sugestão, a validar no refinamento (P6). O esforço muda com a forma escolhida.

#### Pendências para sincronizar
- Time (Area Path), Sprint e Responsável
- Story Points (sugestão: 3)
- Vínculo pai: Feature F6. Predecessor: F6.3 (com F6.3.T8). Sucessores: F6.4 e F7.5
- Se não for acionado, fechar com link para a seção de base legal do RIPD
- Contato da equipe de mídia da igreja do piloto e confirmação de quem controla a câmera
- Registrar em F7.5 que ele lê o registro de F6.5 no caminho fixado aqui

## Preview — PBI F6.6 (novo) · Definir o plano de medição e o critério de conclusão da Fase 1

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Definir o plano de medição e o critério de conclusão da Fase 1 |
| Tipo | Product Backlog Item |
| Pai | F6 |
| Tags | fase-1; medicao; data-science; qualidade; governanca |
| Estimativa | 5 pts (sugestão); tasks: 18 h |
| Dependências | F6.1, F6.3 (inventário de rótulos e eventual exceção de som), F6.2 (prazo de retenção e regra de apagamento dos vídeos do piloto; transitiva via F6.3), F5.4 (medições de referência; transitiva via F6.1), F1.3 (caixas nos rótulos da Fase 1), F3.2 (protocolo e uso do som), F3.3 (ferramenta de rotulagem) |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro e pastor Filipe, que decidem a conclusão da Fase 1  
Quero um plano assinado antes do primeiro culto do piloto com os rótulos de referência dos 4 cultos, o prazo e a revisão da rotulagem de cada culto, a forma de retorno do pastor, os critérios do gate que se repetem, quem decide a conclusão e os limites de alerta de qualidade por culto  
Para saber, antes de ver os resultados, o que conta como piloto concluído e quando um culto processado fica fora da qualidade, com os rótulos feitos enquanto o vídeo ainda existe

**Contexto:** O README define a Fase 1 como piloto com uma igreja e 4 cultos (README.pt-BR.md:35), e o gate cobre só a Fase 0 (docs/poc-gate.md). Não há plano de medição da Fase 1 no repositório. Os campos que os limites podem usar já são gravados: cobertura_pct no run_log, que é a porcentagem de janelas não insuficientes (processar_culto.py:103-106); e, por janela, quadros_com_plateia, n_mensuravel e altura_mediana_px (reacao/types.py:38-56; reacao/aggregate.py:24-33). n_mensuravel é a média de rostos mensuráveis por quadro de plateia arredondada (reacao/aggregate.py:30), enquanto a flag insuficiente usa a média sem arredondar (reacao/aggregate.py:26-27,31): uma janela com média 9,5 grava n_mensuravel 10 e sai insuficiente. As medições da Fase 0 que servem de referência vêm de F5.4, com três cultos públicos inteiros em T4. O retorno do pastor é a nota de 1 a 5 em cada insight (supabase/migrations/0001_init.sql:17), registrada no painel web na Vercel (F7.3), e o alerta de qualidade aparece para o revisor no mesmo painel (F7.6). Os rótulos de referência dos cultos do piloto exigem ver o vídeo e, pela P3 revisada, ficam no HF. A ferramenta do Space privado de F3.3 exporta _faces.csv e _eventos.csv e abre clipes do dataset do corpus (arvore_v1.json, F3.3); os vídeos do piloto ficam num destino separado (F7.1), e _momentos.csv é para culto inteiro (labels/README.md:16-17). O rótulo de rostos tem um rosto por linha (labels/README.md:6), e F1.3 decide se a Fase 1 exige caixas. A permissão de usar o som do vídeo na rotulagem vale só para o PoC: 'Sem áudio de plateia em produção; no PoC o som do próprio vídeo pode confirmar a marcação' (labels/README.md:15), e F3.2 registra a exceção para o PoC. O ADR de F6.2 fixa o prazo máximo de retenção dos vídeos do piloto e a regra de que o vídeo de um culto só é apagado depois da rotulagem prevista para ele neste plano. Nenhum item de F7 executa a rotulagem dos cultos do piloto, e F7 não tem a disciplina Visão Computacional (arvore_v1.json, F7). Na Fase 0, os rostos são rotulados em tasks de Visão Computacional e os rótulos são revisados por amostragem em Data Science (feature_F3_v3.json: F3.4.T4, F3.4.T5 e F3.4.T7). O gate fixa as regras de medição antes de o conjunto de teste existir (docs/poc-gate.md:16), e o plano segue a mesma lógica. O repositório é público, e o plano vai para o local privado do ADR de F6.2.

**Regras de negócio:**
- RN01 – Fabio Pinheiro e o pastor Filipe assinam o plano antes do primeiro culto do piloto, na forma de assinatura adotada em F1.3 e F6.1. Qualquer mudança depois disso é nova versão assinada, e nenhum resultado já visto muda a regra (mesma lógica de docs/poc-gate.md:16).
- RN02 – Cada limite de alerta (cobertura_pct, quadros_com_plateia, altura_mediana_px e rostos mensuráveis por quadro) tem valor, unidade, direção e origem do valor (arquivo e run_id da medição da Fase 0). O limite de rostos mensuráveis usa n_mensuravel, que é média arredondada (reacao/aggregate.py:30), e não é fixado em 10 nem na vizinhança de 10; o k-mínimo por janela é lido pela flag insuficiente (reacao/aggregate.py:31), que já entra em cobertura_pct (processar_culto.py:103).
- RN03 – Os rótulos de rostos e de eventos dos cultos do piloto são feitos na ferramenta do Space privado (F3.3), sem quadro em disco (regra 1). O plano diz como e onde os momentos são marcados. A rotulagem dos cultos do piloto não usa som (regra 5), porque a permissão de labels/README.md:15 vale só para o PoC. Uma exceção para a Fase 1 só vale se aprovada pelo encarregado e registrada no RIPD (F6.3) antes da assinatura do plano.
- RN04 – O retorno do pastor é a nota de 1 a 5 por insight liberado, no painel web na Vercel. O plano fixa o mínimo de notas por culto e a regra de leitura.
- RN05 – O plano lista os critérios do gate que se repetem nos 4 cultos, com meta e regra de leitura. Meta diferente da Fase 0 vem com justificativa.
- RN06 – O plano nomeia quem decide a conclusão e as decisões possíveis. F7.7 aplica o plano.
- RN07 – Nenhuma métrica do plano é por pessoa, assento ou setor pequeno, e janela insuficiente não entra com percentual (CLAUDE.md, regra 3).
- RN08 – Todo rótulo previsto no plano consta do inventário do RIPD (F6.3). Se não constar, F6.3 é reaberto antes da assinatura do plano.
- RN09 – O plano fica no local privado decidido no ADR de F6.2.
- RN10 – Para cada culto, o plano diz o prazo da rotulagem depois do processamento. Esse prazo cabe no prazo máximo de retenção dos vídeos do piloto do ADR de F6.2, porque o vídeo de um culto só é apagado depois da rotulagem prevista para ele. Se não couber, F6.2 é reaberto antes da assinatura.
- RN11 – O plano diz como os rótulos dos cultos do piloto são revisados (amostra e quem revisa), seguindo o protocolo de F3.2, e cita o item de F7 que executa a rotulagem e a revisão.

**Fora de escopo:**
- Mostrar o alerta no painel web na Vercel (F7.6)
- Consolidar os 4 cultos e decidir a conclusão (F7.7)
- Executar a rotulagem dos cultos do piloto e a revisão dos rótulos (item de F7 a criar; pendência)
- Adaptar a ferramenta de F3.3 para ler vídeos do destino de F7.1 ou marcar momentos
- Ajustar o apagamento do vídeo em F7.5 e a retenção dos rótulos em F7.4
- Critérios de fases seguintes (painel ao vivo, sinal ao pregador)

#### Critérios de aceite

- O plano está no local privado decidido no ADR de F6.2, com data, versão e as assinaturas de Fabio Pinheiro e do pastor Filipe, e a data é anterior à do primeiro culto do piloto.
- Para cada um dos 4 cultos, o plano diz quais rótulos de referência serão feitos, por quem e em qual ferramenta: rostos e eventos na ferramenta de F3.3 e momentos na forma descrita no plano.
- O plano diz que a rotulagem dos cultos do piloto não usa som, ou cita a exceção aprovada pelo encarregado e registrada no RIPD.
- Cada rótulo previsto no plano consta do inventário do RIPD.
- Para cada culto, o plano diz o prazo da rotulagem depois do processamento, e esse prazo cabe no prazo máximo de retenção dos vídeos do piloto do ADR de F6.2.
- O plano diz como os rótulos são revisados (amostra e quem revisa) e cita o item de F7 que executa a rotulagem e a revisão.
- O plano diz como o pastor devolve a avaliação dos insights, o mínimo de notas por culto e a regra de leitura.
- O plano lista os critérios do gate que se repetem, cada um com meta e regra de leitura.
- O plano tem os quatro limites de alerta por culto, cada um com valor, unidade, direção e origem do valor, e o limite de rostos mensuráveis traz a ressalva de que n_mensuravel é média arredondada.
- O plano diz o critério de conclusão da Fase 1, as decisões possíveis e quem decide.
- Nenhuma métrica do plano é por pessoa, assento ou setor pequeno.
- Caminho de erro: aplicados aos dados gravados de um culto público da Fase 0, os quatro limites classificam o culto como dentro ou fora e dão o motivo. Um limite que não pode ser calculado com os campos gravados reprova a verificação.
- Caminho de erro: um rótulo previsto que não conste do inventário do RIPD impede a assinatura até F6.3 ser reaberto e aprovado.
- Caminho de erro: um prazo de rotulagem que não cabe no prazo de retenção dos vídeos do piloto do ADR impede a assinatura até F6.2 ser reaberto.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F6.6.T1 | Data Science | Propor os limites de alerta de qualidade por culto a partir das medições da Fase 0 | 6 | F6.1, F5.4 |
| F6.6.T2 | Data Science | Definir rótulos de referência, prazo e revisão da rotulagem, retorno do pastor, critérios do gate repetidos e critério de conclusão | 6 | F6.1, F6.2, F6.3, F1.3, F3.2, F3.3 |
| F6.6.T3 | Governança e Privacidade | Revisar o plano contra as regras do CLAUDE.md, o RIPD e o ADR de F6.2 e colher as assinaturas antes do primeiro culto | 3 | F6.6.T1, F6.6.T2 |
| F6.6.T4 | QA | Verificar os critérios de aceite do plano de medição | 3 | F6.6.T3 |

<details><summary>F6.6.T1 · [Data Science] Propor os limites de alerta de qualidade por culto a partir das medições da Fase 0</summary>

**Objetivo:** Ter os quatro limites com valor, unidade, direção e origem, testados nos cultos da Fase 0.

**Passos previstos:**
1. Ler, pela revisão, o run_log e o window_aggregate dos três cultos de F5.4 no repositório de resultados
2. Calcular por culto cobertura_pct, quadros_com_plateia por janela, altura_mediana_px e n_mensuravel
3. Propor para cada medida valor, unidade, direção e motivo, citando arquivo e run_id, com o limite de n_mensuravel longe de 10 e a ressalva de que ele é média arredondada
4. Aplicar os limites propostos aos três cultos e registrar a classificação e o motivo

**Definição de pronto:** Tabela de limites no rascunho do plano, com a origem de cada valor, a ressalva sobre n_mensuravel e a classificação dos três cultos da Fase 0.

**Dependências:** F6.1, F5.4

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F6.6.T2 · [Data Science] Definir rótulos de referência, prazo e revisão da rotulagem, retorno do pastor, critérios do gate repetidos e critério de conclusão</summary>

**Objetivo:** Escrever as seções do plano que dizem o que se mede nos 4 cultos, até quando a rotulagem de cada culto termina e quando o piloto termina.

**Passos previstos:**
1. Definir, por culto, quais rótulos serão feitos e por quem: rostos e eventos na ferramenta de F3.3, seguindo a regra de caixas de F1.3; momentos, com a forma de marcação e a ferramenta; sem som, salvo exceção registrada no RIPD
2. Definir, por culto, o prazo da rotulagem depois do processamento e conferir que ele cabe no prazo máximo de retenção dos vídeos do piloto do ADR de F6.2; se não couber, pedir a reabertura de F6.2
3. Definir como os rótulos são revisados (amostra e quem revisa), seguindo o protocolo de F3.2
4. Citar o item de F7 que executa a rotulagem e a revisão, ou registrar a pendência se ele ainda não existir
5. Conferir que cada rótulo previsto consta do inventário do RIPD e, se faltar, pedir a reabertura de F6.3
6. Definir o mínimo de notas do pastor por culto e a regra de leitura
7. Escolher os critérios do gate que se repetem, com meta e regra de leitura
8. Escrever o critério de conclusão e as decisões possíveis

**Definição de pronto:** Seções de rótulos, prazo e revisão da rotulagem, retorno do pastor, critérios repetidos e conclusão no rascunho do plano, com a conferência contra o inventário do RIPD e contra o prazo de retenção do ADR de F6.2.

**Dependências:** F6.1, F6.2, F6.3, F1.3, F3.2, F3.3

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F6.6.T3 · [Governança e Privacidade] Revisar o plano contra as regras do CLAUDE.md, o RIPD e o ADR de F6.2 e colher as assinaturas antes do primeiro culto</summary>

**Objetivo:** Ter o plano conforme às regras 1, 3 e 5, ao RIPD e ao prazo de retenção dos vídeos e assinado antes do primeiro culto.

**Passos previstos:**
1. Conferir que nenhuma métrica é por pessoa, assento ou setor pequeno
2. Conferir que a rotulagem não grava quadro e não usa som nos cultos do piloto, ou que cita a exceção registrada no RIPD
3. Conferir que cada rótulo previsto consta do inventário do RIPD
4. Conferir que o prazo da rotulagem de cada culto cabe no prazo de retenção dos vídeos do piloto do ADR de F6.2 e que o plano cita o item de F7 que executa a rotulagem
5. Nomear quem decide a conclusão
6. Colher as assinaturas de Fabio Pinheiro e do pastor Filipe, na forma adotada em F1.3 e F6.1, com data anterior ao primeiro culto
7. Gravar o plano no local privado do ADR de F6.2

**Definição de pronto:** Plano gravado no local privado com versão, data e as duas assinaturas.

**Dependências:** F6.6.T1, F6.6.T2

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F6.6.T4 · [QA] Verificar os critérios de aceite do plano de medição</summary>

**Objetivo:** Marcar cada critério de aceite de F6.6 como 'passou' ou 'não passou' com evidência.

**Passos previstos:**
1. Conferir a presença de cada seção exigida pelos critérios, incluindo a regra de som, a ressalva sobre n_mensuravel, o prazo e a revisão da rotulagem e o item de F7 citado
2. Conferir cada rótulo previsto contra o inventário do RIPD
3. Comparar o prazo da rotulagem de cada culto com o prazo máximo de retenção dos vídeos do piloto no ADR de F6.2
4. Recalcular os quatro limites para um culto público da Fase 0 a partir dos arquivos citados e comparar com a classificação do plano
5. Conferir a data das assinaturas contra a data do primeiro culto e o local do plano
6. Registrar o resultado de cada critério e abrir nova versão do plano se algum reprovar

**Definição de pronto:** Relatório no local privado com 'passou' ou 'não passou' por critério, o recálculo dos limites e a comparação do prazo de rotulagem com o ADR anexados.

**Dependências:** F6.6.T3

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- README.pt-BR.md:35
- docs/poc-gate.md:16
- processar_culto.py:103-106
- reacao/types.py:38-56
- reacao/aggregate.py:24-33
- supabase/migrations/0001_init.sql:17
- labels/README.md:6,15,16-17
- CLAUDE.md (regras 1, 3 e 5)
- arvore_v1.json (F1.3, F3.2, F3.3, F7: disciplinas e resumo de F7.1, F7.5 e F7.7)
- feature_F3_v3.json (F3.4.T4, F3.4.T5 e F3.4.T7: rotulagem em Visão Computacional e revisão por amostragem em Data Science)
- feature_F6.json (F6.6); P3 revisada

#### Verificação INVEST: pontos que falharam
- Independente: depende de F6.1, F6.2, F6.3, F1.3, F3.2 e F3.3, e o plano só cita o item de execução da rotulagem depois que ele existir em F7.

#### Premissas
- A execução da rotulagem dos cultos do piloto não tem item em F7, e F7 não tem a disciplina Visão Computacional (arvore_v1.json, F7). Também falta a adaptação de F3.3 para ler do destino de F7.1 e marcar momentos. Se o plano exigir rótulos, é preciso abrir PBI novo em F7 ou incluir tasks de Visão Computacional e Data Science em F7.7 (pendência).
- A revisão por amostragem dos rótulos do piloto segue o padrão de F3.4 (Data Science revisa os rótulos feitos em Visão Computacional). É proposta desta revisão, a confirmar com o protocolo de F3.2.
- Os valores dos limites vêm das medições de F5.4. Esta árvore não fixa número, nem o prazo da rotulagem.
- 'Rostos mensuráveis por quadro' é lido como n_mensuravel, a média arredondada por quadro de plateia gravada por janela (reacao/aggregate.py:26-30).
- Story points e horas são sugestão, a validar no refinamento (P6). O prazo e a revisão da rotulagem acrescentaram 1 h a F6.6.T2 sem mudar os pontos.

#### Pendências para sincronizar
- Time (Area Path), Sprint e Responsável
- Story Points (sugestão: 5)
- Vínculo pai: Feature F6. Predecessores: F6.1, F6.2, F6.3, F5.4, F1.3, F3.2 e F3.3. Sucessores: F7.5, F7.6 e F7.7
- Data do primeiro culto do piloto
- F7.7 ou PBI novo em F7: tasks de Visão Computacional para rotular os cultos do piloto pelo protocolo de F3.2 na ferramenta de F3.3 e de Data Science para revisar os rótulos por amostragem, antes de F7.7.T4
- F3.3 ou F7.1.T1: leitura do destino de F7.1, lista de acesso dos rotuladores do piloto e forma de marcar momentos
- F7.5.T2: apagar o vídeo só depois da rotulagem prevista para o culto neste plano
