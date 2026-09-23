[Voltar ao épico](README.md)

# Preview — Feature F3 (novo) · Rotular o corpus dos critérios 1 e 2 com base legal registrada, protocolo definido e rótulos versionados no dataset privado

### Campos
| Campo | Conteúdo |
|---|---|
| Título | Rotular o corpus dos critérios 1 e 2 com base legal registrada, protocolo definido e rótulos versionados no dataset privado |
| Tipo | Feature |
| Pai | Epic |
| Tags | fase-0; gate-poc; rotulagem; corpus; lgpd; hugging-face; fase-1 |
| Estimativa | 50 pts / 245 h (soma dos PBIs, sugestão) |

### Descrição

**Problema:** O bench mede os critérios 1 e 2 do gate (docs/poc-gate.md:8-10) sobre rótulos manuais, e não existe rótulo em lugar nenhum. A pasta labels/ do repositório só tem o README. O dataset privado ds-fabiopinheiro/reacao-poc-corpus só tem pib/ e .gitattributes na raiz, sem dataset card, sem pasta de rótulos e sem tag (hf_fs ls em 2026-09-23; HfApi.list_repo_refs no levantamento). Sem rótulos, o bench termina com 'nenhum vídeo rotulado — nada medido' e código 1 (bench.py:237-239), e tools/rodar_teste.sh sai com código 2 (tools/rodar_teste.sh:44-52). O corpus são 23 clipes de plateia da PIB (samples/corpus/pib/README.md:7, não versionado). A LGPD classifica como dado pessoal sensível o dado sobre convicção religiosa (art. 5º, II). A autorização registrada é do pastor Filipe, de 2026-09-05 e 'de uso no piloto' (samples/corpus/pib/README.md:3-4). O README descreve a Fase 0 com vídeos públicos (README.pt-BR.md:34), e o gate põe os dados da PIB depois da decisão (docs/poc-gate.md:50). Não há análise de base legal nem encarregado nomeado, e nenhum item do backlog tem a nomeação como trabalho: o encarregado só aparece em F6.3, que depende da decisão do gate. tools/rodar_teste.sh baixa o corpus para samples/corpus em disco e roda o bench em CPU fora do HF (tools/rodar_teste.sh:12,35-40,55). Nesta sessão de desenvolvimento, samples/corpus/pib tem 24 arquivos .mp4, e há cópia do dataset em ~/.cache/huggingface/hub/datasets--ds-fabiopinheiro--reacao-poc-corpus e em samples/corpus/.cache/huggingface, contra a regra 1 do CLAUDE.md. O HF_TOKEN do ambiente é um token clássico de escrita, com escopo de conta, de nome 'claude-code-teste-pib' (huggingface_hub.whoami() em 2026-09-23). O bench baixa o repositório inteiro sem revisão fixa, 299.851.242 bytes no commit 75e001af52 (bench.py:52,58-70; HfApi.dataset_info), e guarda o download só pelo repo_id (bench.py:66-70). processar_culto.py também lê sem revisão (processar_culto.py:23-31). O local dos rótulos diverge entre labels/README.md:28,36, tools/validar_labels.py:4-5, tools/rodar_teste.sh:13 e docs/hf-jobs.md:28. Não há protocolo de rotulagem (medida de altura_px, definição de riso e de neutro, rotuladores, concordância), e a ferramenta de clique citada em labels/README.md:19-20 não existe. O validador aplica à pasta inteira os mínimos do corpus, 1 riso e 4 trechos neutros (tools/validar_labels.py:215-220). Os clipes são de um único culto, e na execução local do concatenado pct_sorrindo ficou entre 0,0% e 2,4% nas 8 janelas (out/window_aggregate.json, local). Por isso os risos podem não chegar ao mínimo que F1.3 vai fixar.

**Solução proposta:** Criar o dataset card com o Dataset Viewer desligado, marcar corpus e rótulos com tag, unificar o local dos rótulos na documentação e nas ferramentas e fazer bench.py e processar_culto.py lerem o dataset só por revisão fixa e só a subpasta pedida (F3.5). Eliminar já as cópias locais dos clipes da PIB, revogar o token clássico, obter a nomeação do encarregado e, com ele, analisar a base legal do uso dos clipes da PIB na Fase 0, registrando no card autorização, conclusão, lista de acesso e retenção (F3.1). Definir o protocolo de rotulagem, com o som desligado (F3.2). Disponibilizar a ferramenta de rotulagem num Space do Hugging Face com acesso restrito à lista de rotuladores e sem gravar quadro em disco (F3.3). Medir a concordância, rotular os clipes de teste e os de desenvolvimento e publicar com tag (F3.4). Se a PIB não puder ser usada ou os risos não chegarem ao mínimo, selecionar e transferir clipes públicos (F3.6) e rotulá-los (F3.7). Toda a Feature roda no ambiente de desenvolvimento do Hugging Face. O painel web na Vercel não participa dela: não recebe vídeo, quadro, recorte, observação por rosto nem resultado dos clipes da PIB na Fase 0. Se o plano da Fase 1 (F6.6) previr rótulos de rostos ou eventos nos cultos do piloto, adaptar a mesma ferramenta para ler os vídeos do destino de F7.1 e gravar os rótulos no destino do ADR de F6.2, com a lista de acesso dos rotuladores do piloto (F3.8, condicional). F3.6 reutiliza o job de cópia e o procedimento de token de F5.1.

**Usuários impactados:** Rotuladores (identificados por código de papel nos registros), Fabio Pinheiro, dono do dataset e do repositório e responsável pelo gate, Pastor Filipe, que autorizou o uso do corpus da PIB, Encarregado de dados (DPO), ainda sem nome, Controlador do tratamento dos clipes, a identificar em F3.1, Time de Data Science, Visão Computacional e MLOps que usa os rótulos em F4.4, F4.5 e F4.6, Rotuladores dos cultos do piloto (F3.8), identificados por código de papel

**Valor de negócio:** Sem os rótulos desta Feature, os critérios 1 e 2 (docs/poc-gate.md:8-10) e a calibração nos clipes de desenvolvimento (F4.4, F4.5) ficam sem número, e a decisão do gate (F6.1, docs/poc-gate.md:50) exige o resultado dos seis critérios. Com leitura por revisão fixa, cada número do gate fica ligado ao corpus e aos rótulos de onde veio. Com a base legal registrada, o uso do vídeo da congregação na Fase 0 fica documentado antes do RIPD da Fase 1.

**Regras de negócio:**
- RN01 – Nenhum quadro, recorte ou vídeo é gravado em disco fora de /dev/shm na rotulagem, nos jobs e no Space (CLAUDE.md regra 1; reacao/guard.py:7-16).
- RN02 – Os rótulos não identificam pessoa. _faces.csv tem só t_s e altura_px, _eventos.csv tem só intervalo e tipo, e a lista de quadros revisados tem só t_s. Não há id, posição de rosto, ligação entre rostos de quadros diferentes nem métrica por assento (CLAUDE.md regras 2 e 3; labels/README.md:6-11).
- RN03 – Nenhum clipe da PIB é rotulado nem processado em job antes do parecer de F3.1 que o permita (premissa P13).
- RN04 – Os rótulos dos clipes de desenvolvimento (07 a 10) e dos clipes de teste ficam em pastas separadas. O igreja_simples_concat.mp4 não é rotulado, porque contém os 23 clipes (docs/poc-gate.md:46-48; samples/corpus/pib/README.md:12).
- RN05 – Jobs leem corpus e rótulos por tag ou commit, e cada execução registra a revisão lida.
- RN06 – Ferramentas que exibem vídeo ou quadro ficam no Hugging Face. O painel web na Vercel lê só agregados, eventos e insights do Supabase e não recebe vídeo, quadro, recorte nem observação por rosto (P3 revisada).
- RN07 – Na Fase 0, jobs sobre clipes da PIB rodam sem os segredos do Supabase, processar_culto.py recusa gravar no Supabase quando o vídeo vem de pib/ do dataset do corpus, e os resultados vão para os arquivos de saída do job (reacao/store.py:10-26). Assim nenhum resultado da PIB chega ao painel web antes da decisão do gate (P10).
- RN08 – O som do vídeo não é tocado na rotulagem. A regra 5 do CLAUDE.md está entre as 'Regras que nunca mudam' e limita a trilha do arquivo à transcrição do púlpito (CLAUDE.md:9,20). labels/README.md:15 é corrigido.
- RN09 – Nenhum limiar é calibrado e nenhum bench roda sobre os rótulos de teste antes de F4.6 (docs/poc-gate.md:38-40,46-48).
- RN10 – A publicação de rótulos exige zero erro de arquivo do validador (nomes, colunas, grade, tipos e intervalos) em cada pasta. Os mínimos do corpus (risos de F1.3 e 4 trechos neutros) são contados só na pasta de teste. A falta de risos é registrada e aciona F3.6, sem bloquear a publicação.

**Fora de escopo:**
- Caixas delimitadoras e recall pareado por IoU, salvo se F1.3 decidir que a Fase 1 exige (docs/poc-gate.md:20-21)
- Rótulos de momentos de culto inteiro (F5.1)
- Definição dos rótulos de referência dos cultos do piloto (F6.6) e execução da rotulagem deles (F7)
- Recebimento, retenção e apagamento dos vídeos do piloto (F7.1, F7.4, F7.5); a ferramenta só os lê em F3.8
- Qualquer rótulo por pessoa ou assento (regras 2 e 3 do CLAUDE.md)
- Painel web na Vercel, relatório do culto, notas do critério 4 e telas por perfil (F5.6, F5.7, F7.2, F7.3, F7.6)
- Execução do bench sobre os rótulos de teste, que é de F4.6
- Correção da guarda de não persistência (F1.1)
- Alteração da regra 5 do CLAUDE.md, para o pipeline ou para a rotulagem, que cabe ao dono do repositório

**Dependências técnicas:**
- F1.3: mínimo de eventos de riso, decisão sobre o clipe 11, exigência de caixas na Fase 1 e vídeos permitidos por tipo de job
- F1.4: validador com o mínimo de risos de F1.3, recusa de intervalo sem segundo inteiro amostrado e exclusão do concatenado. Esta Feature pede a F1.4 que separe os erros de arquivo dos mínimos do corpus (pendência).
- F1.1: guarda corrigida (comparação com /dev/shm/ com separador e '[guard] ok' só em execução bem-sucedida) e script de lançamento que recusa caminho local, usados pelo Space de F3.3 e pelo job de transferência de F3.6
- F2.4: namespace, SDK e modelo de acesso do Space de rotulagem
- F2.1.T6 e F2.6.T2: comandos de desenvolvimento de docs/hf-jobs.md e forma de passar segredos. F3.5.T5 espera as duas para acrescentar a revisão aos caminhos e retirar os segredos do Supabase dos comandos sobre pib/.
- F2.6: práticas de token fine-grained, inventário de credenciais (F2.6.T6) e projeto Supabase de desenvolvimento. O token de leitura do Space (F3.3) não está previsto em F2.6. O token de escrita no dataset do job de transferência de F3.6 segue o procedimento de F5.1.T3 e entra no inventário de F2.6.T6 como exceção de uso único, como o de F5.1.
- Dataset privado ds-fabiopinheiro/reacao-poc-corpus, commit 75e001af52
- Assinatura PRO da conta ds-fabiopinheiro (periodEnd 2026-10-01 no whoami de 2026-09-23), exigida por Space Gradio ou Docker de conta pessoal e pela visibilidade protected (https://huggingface.co/docs/hub/spaces-overview)
- Plano Team ou Enterprise de organização, se o ADR de F2.4 escolher Space private de organização: Space Gradio ou Docker de organização exige esse plano (https://huggingface.co/docs/hub/spaces-overview). Custo a confirmar.
- Encarregado de dados nomeado (LGPD art. 41), obtido na task F3.1.T2
- Rotuladores disponíveis (labels/README.md:19-20)
- Pastor Filipe para confirmar autorização e escopo
- F5.1: exclusão dos vídeos selecionados em F3.6 (pendência)
- F5.1.T3, F5.1.T4 e F5.1.T5: script de cópia parametrizado e procedimento do token de uso único, reutilizados por F3.6
- F2.2: fluxo de publicação da imagem por tag com digest, para o job de transferência de F3.6
- F6.1, F6.2.T2, F6.3, F6.6 e F7.1: decisão de seguir, destino e acesso dos rótulos do piloto, RIPD, plano da Fase 1 e destino dos vídeos do piloto, para F3.8

**Riscos:**
- O encarregado de dados não tem nome. F3.1 passa a ter a task de obter a nomeação, mas sem ela o parecer não sai, e a lista de acesso de F3.3 e toda a F3.4 ficam paradas. F3.2 e F3.5 não dependem do parecer, e a eliminação das cópias locais também não.
- O parecer pode vetar a PIB na Fase 0. Nesse caso F3.4 é cancelado, e F3.6 e F3.7 fornecem conjuntos públicos de desenvolvimento e de teste, porque F4.4 e F4.5 perdem os clipes 07 a 10.
- Poucos risos no conjunto de teste (pct_sorrindo de 0,0% a 2,4% nas 8 janelas do concatenado, execução local) deixam o 2a inconclusivo ou acionam F3.6.
- A assinatura PRO tem periodEnd 2026-10-01. Sem renovação, o Space Gradio ou Docker de conta pessoal e a visibilidade protected deixam de estar disponíveis.
- Space private com rotuladores de contas próprias exige organização, e Space Gradio ou Docker de organização exige plano Team ou Enterprise (custo a confirmar). Na alternativa protected de conta pessoal, o app fica acessível pela URL .hf.space, e o controle de acesso passa a depender do código do app em todas as rotas (https://huggingface.co/docs/hub/spaces-overview#space-visibility).
- Se o SDK for Gradio, imagens devolvidas ao navegador são salvas no cache temporário, e qualquer arquivo do cache fica disponível por URL a todos os usuários do app (https://gradio.app/guides/file-access; https://gradio.app/docs/gradio/image). Fora de /dev/shm isso fere a regra 1, e sem verificação de conta nas rotas de arquivo expõe quadros.
- O navegador do rotulador pode guardar em disco as imagens exibidas se a resposta não trouxer Cache-Control: no-store (https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control).
- A guarda atual observa só as raízes passadas (por padrão cwd e /tmp), acusa só arquivos novos em relação ao início do contexto e não tem extensão de áudio (reacao/guard.py:8,44-53,60,69-70). Sem a varredura absoluta de F3.3, um resíduo no cache do huggingface_hub ou do SDK passaria sem aviso.
- Uma altura manual diferente da altura da caixa do SCRFD muda o conjunto de rostos >= 64 px e o recall (reacao/detect.py:32-33; bench.py:123-128). Sem caixa por rosto nos rótulos, a comparação entre as duas alturas é aproximação.
- O esforço de rotulagem pode estar subestimado. labels/README.md:19-20 estima 3 a 4 h para cerca de 250 quadros com 20 a 40 rostos por quadro, sem medição.
- Concordância abaixo do limite do protocolo obriga nova rodada antes dos clipes de teste.
- Um rotulador que também calibra em F4.5 vê os clipes de teste antes do bench.
- F3.8 depende de cinco PBIs da Fase 1 em outras Features (F6.2, F6.3, F6.6, F7.1 e o item de rotulagem de F7). Se ele atrasar, o prazo de rotulagem de F6.6.T2 pode passar do prazo de retenção dos vídeos do ADR de F6.2.

**Estratégia de fatiamento:** Por passo do fluxo de rotulagem (estratégia 1 do TaskFlow): versionamento, local único dos rótulos e leitura por revisão (F3.5), base de uso do corpus (F3.1), protocolo (F3.2), ferramenta (F3.3), concordância, rotulagem validada e publicada (F3.4), mais dois PBIs condicionais, fatiados por regra de negócio e por passo: seleção, parecer e transferência de clipes públicos (F3.6) e rotulagem e publicação desses clipes (F3.7). Ordem sugerida: F3.5 (com F3.5.T5 depois de F2.1.T6 e F2.6.T2) e as tasks de F3.1 que não esperam o parecer (eliminação das cópias locais, nomeação do encarregado, inventário, remoção de tools/rodar_teste.sh) em paralelo; depois F3.2 e F3.3; o parecer e o card de F3.1; e F3.4. F3.6 e F3.7 entram só se F3.1 vetar a PIB ou se F3.4 registrar menos risos que o mínimo de F1.3. Com veto, F3.4 é cancelado. A ordem é sugestão, e a priorização é decisão do time. F3.8, condicional e da Fase 1, adapta a ferramenta aos vídeos e aos rótulos do piloto e entra só depois de F6.1 decidir seguir e de F6.6 prever rótulos de rostos ou eventos.

### Critérios de aceite
- A página do dataset privado no Hub mostra o dataset card na raiz e não mostra o Dataset Viewer. O dataset tem uma tag do corpus e uma tag por versão publicada dos rótulos.
- bench.py e processar_culto.py recusam ler o dataset sem revisão fixa, mostram em cada execução a revisão lida e baixam só a subpasta pedida, também com corpus e rótulos em revisões diferentes do mesmo dataset.
- O dataset card mostra quem autorizou o uso da PIB, o escopo, a data, a conclusão e a data do parecer do encarregado, a lista de acesso com contas e tokens e a retenção.
- Nenhum ambiente de desenvolvimento listado no inventário de F3.1 guarda cópia dos clipes da PIB, seja arquivo .mp4 ou pasta do dataset no cache do huggingface_hub. O token clássico de escrita foi revogado, e o repositório não tem mais roteiro que baixe o corpus para disco.
- O protocolo de rotulagem está versionado, fixa o som desligado e define a medida de altura_px, a comparação com a caixa do detector, riso, neutro, quadro revisado sem rosto, rotuladores, concordância e revisão. labels/README.md, tools/validar_labels.py e docs/hf-jobs.md apontam para o mesmo local de rótulos, e tools/preparar_rotulagem.py foi retirado.
- Um rotulador da lista entra no Space com a própria conta, rotula um clipe inteiro e exporta arquivos sem erro de arquivo no validador. Uma conta fora da lista, um visitante sem login e um pedido direto à URL de um quadro recebem acesso negado. O log do Space registra, ao fim da sessão e depois de um erro, a varredura absoluta sem arquivo de imagem, vídeo ou áudio fora de /dev/shm.
- Os rótulos de teste e de desenvolvimento estão publicados com tag, o validador não aponta erro de arquivo em nenhuma pasta, todo t_s da grade consta como revisado, e o registro traz a contagem de risos do conjunto de teste contra o mínimo de F1.3.
- Caminho de erro: se o parecer vetar a PIB ou a contagem de risos ficar abaixo do mínimo, o registro diz qual condição ocorreu e F3.6 é acionado. A falta de risos não bloqueia a publicação dos rótulos da PIB. Nenhum bench roda sobre os rótulos de teste antes de F4.6.
- Nenhum vídeo, quadro, recorte ou resultado dos clipes da PIB aparece no painel web na Vercel nem no Supabase durante a Fase 0: processar_culto.py recusa gravar no Supabase com vídeo de pib/, e a consulta às tabelas do Supabase de desenvolvimento não encontra culto dos clipes da PIB.
- Se F3.8 for acionado: um rotulador da lista do piloto rotula no Space um vídeo público colocado no destino de F7.1, os rótulos vão só para o destino do ADR de F6.2, e uma conta que está só na lista do PoC não abre vídeo do piloto.

### Alterações em relação à árvore
- Feature F3 (solução, RN06, RN07, fora de escopo e critério 9): fica registrado que a Feature roda toda no Hugging Face e que o painel web na Vercel não recebe vídeo, quadro, recorte, observação por rosto nem resultado dos clipes da PIB na Fase 0 (P3 revisada; P10 com 'Space' trocado por 'painel web na Vercel'). RN07 passa a ter barreira no código (F3.1.T9) e verificação no Supabase (F3.1.T10).
- Feature F3 (problema; contexto de F3.1 e F3.6): o enquadramento da imagem de plateia como dado sensível saiu da lista de fatos e foi para premissas, porque é interpretação jurídica que o parecer de F3.1 vai concluir.
- Feature F3: F3.6 da árvore foi dividido em F3.6 (seleção, parecer e transferência de clipes públicos) e F3.7 (rotulagem e publicação desses clipes), os dois condicionais. A Feature passa a ter 7 PBIs. P13 foi ajustada: com veto, F3.4 é cancelado e F3.7 rotula os conjuntos públicos.
- Feature F3 (RN08) e F3.2: o som fica desligado na rotulagem. A regra 5 está entre as 'Regras que nunca mudam' do CLAUDE.md, e a exceção prevista na árvore saiu. O controle de som saiu de F3.3.
- Feature F3 (RN10), F3.3, F3.4, F3.6 e F3.7: a validação separa erros de arquivo dos mínimos do corpus. A exportação e a publicação exigem zero erro de arquivo, e os mínimos valem só para a pasta de teste, sem bloquear a publicação.
- Feature F3 (dependências técnicas): a descrição de F2.6 foi corrigida, porque F2.6 não prevê o token de leitura do Space nem escrita no dataset. A justificativa do PRO deixou de citar o Dataset Viewer, que a Feature desliga. Entraram o plano Team ou Enterprise, se o ADR escolher organização, e F1.1 como correção da guarda.
- F3.1: a eliminação das cópias locais virou a primeira task (T1) e não espera o parecer. A verificação passou a conferir o cache do huggingface_hub por repositório e samples/corpus/.cache/huggingface, e ficou restrita aos ambientes de desenvolvimento, sem o Drive e o dataset.
- F3.1: entrou a task de obter do controlador a nomeação do encarregado (T2), com dono sugerido. 'Encarregado de dados nomeado' saiu das dependências das tasks.
- F3.1: entraram o inventário de tokens e a revogação do token clássico de escrita (T3). A lista de acesso passou a incluir tokens. 'Conta de serviço do Space e dos jobs' foi trocado por 'token fine-grained da conta dona, um por uso'.
- F3.1: o inventário passou a incluir os tratamentos já feitos (P28) e os resultados derivados locais em out/, cujo destino segue o parecer. pib/README.md do dataset perde o e-mail pessoal, e o link do Drive segue o parecer.
- F3.1: entraram a barreira em processar_culto.py para vídeo de pib/ com segredos do Supabase (T9, Backend) e a consulta às tabelas do Supabase de desenvolvimento na QA (T10). A retirada dos segredos dos comandos documentados ficou em F3.5.T5.
- F3.1: das duas opções da árvore para tools/rodar_teste.sh, foi escolhida a remoção, porque F1.1 cria o script de lançamento. As notas úteis do script vão para docs/hf-jobs.md, numa seção separada dos comandos.
- F3.1: parecer, lista de acesso e contas ficam no dataset privado, porque o repositório GitHub é público (API do GitHub, visibility public). O alinhamento do texto da Fase 0 cobre os 7 READMEs e passou de Data Science para Governança e Privacidade (P5). Entraram as disciplinas QA e Backend, e saiu Data Science.
- F3.2: a medição da concordância saiu de F3.2 e foi para o início de F3.4, porque exige abrir os clipes na ferramenta de F3.3. F3.2 fixa métrica, amostra, limite e o que acontece abaixo dele.
- F3.2: a regra de medida segue a caixa do detector (reacao/detect.py:32-33) e a convenção do WIDER FACE. Entraram o método de comparação sem pareamento entre altura manual e caixa, registrado como aproximação porque os rótulos não têm caixa por rosto, o erro máximo da medida da ferramenta e o registro de quadro revisado sem rosto.
- F3.2: passa a ser PBI documental, verificado por revisão da QA e aprovado por Fabio. A unificação do local dos rótulos saiu para F3.5 (F3.5.T6). F3.2 deixou de depender de F3.1, do encarregado e de F3.5.
- F3.3: o título e a RN01 dizem 'acesso restrito à lista de rotuladores' e registram as duas opções do ADR de F2.4. Private de organização exige Team ou Enterprise. Protected deixa o app público pela URL, e o app confere a conta em todas as rotas, inclusive as de arquivo. O critério 2 cobre visitante sem login, pedido direto à URL e membro de organização fora da lista.
- F3.3: o contexto sobre a guarda foi corrigido ('varre as raízes indicadas', não o disco). Entrou a varredura absoluta com raízes explícitas e extensões de áudio, rodada pelo app ao fim da sessão e no erro, com resultado no log do Space e sem reinício. Entraram as dependências de F1.1 e F1.4, e o Space usa o validador de F1.4 sem regra paralela.
- F3.3: o CSV parcial restaura alturas por t_s e a lista de quadros revisados, sem posição do clique. A aplicação da lista de acesso de F3.1 virou task própria (T6), para a construção não esperar o parecer. Mantidos o cache temporário do SDK e do huggingface_hub em /dev/shm, o Cache-Control: no-store e a ausência do detector.
- F3.4: o título passa a incluir a concordância. O valor da árvore 'o bench deixa de sair com código 2 por falta de rótulo' foi corrigido: o código 2 vem de tools/rodar_teste.sh:51, o bench sai com código 1 (bench.py:237-239), e rodar o bench sobre os rótulos de teste quebraria o teste cego (docs/poc-gate.md:38-40,46-48).
- F3.4: a cobertura é contada pela lista de quadros revisados, não pelas linhas de _faces.csv. As tasks passaram a ser de uma pessoa cada: marcação da amostra por rotulador, revisão por amostragem numa task só do segundo rotulador e QA depois da publicação com tag, cobrindo todos os critérios.
- F3.5: entraram a chave do cache por (repo_id, revisão, subpasta), a unificação do local dos rótulos (vinda de F3.2), a retirada de tools/preparar_rotulagem.py, a retirada dos segredos do Supabase dos comandos sobre pib/, a verificação com a fixture sintética e a disciplina QA. Os testes ficam na task do código, e a QA confere cobertura e resultado.
- F3.5.T5 (revisão sobre a sobreposição com F2.1.T6 e F2.6.T2): passou a depender de F2.1.T6 e F2.6.T2 e ficou restrita a acrescentar revisão e subpasta aos caminhos hf://, apontar os rótulos para o local de F3.5.T2, registrar que o dataset não é montado com -v e retirar os segredos do Supabase dos comandos sobre pib/. A forma de passar segredos, o separador '--' e o timeout ficam com F2.1.T6 e F2.6.T2. A task ganhou a conferência por --dry-run e passou de 3 h para 2 h. F3.5 ganhou as dependências, o item de fora de escopo e a falha de INVEST correspondentes, a Feature ganhou F2.1.T6 e F2.6.T2 nas dependências técnicas, e F3.1 (fora de escopo, dependências, INVEST e F3.1.T8) cita as três tasks.
- F3.6 e F3.7: com acionamento pelo veto de F3.1, entram conjunto de desenvolvimento e de teste públicos (P8, P13). 'Cultos de F5.1, que o Space processa' virou 'cultos de F5.1, que os jobs de F5.4 processam e cujo relatório o painel web na Vercel exibe'. Entraram a transferência por job no HF para /dev/shm, o token de escrita de uso único como exceção a F2.6, a pendência com F5.1 e as disciplinas DevOps e MLOps. O critério de jobs excetua o job de transferência pelo JOB_ID, e o mínimo de risos passou a critério condicional.
- Tasks por disciplina e estimativas sugeridas foram criadas para os sete PBIs. A árvore não trazia tasks nem estimativas (P6, P25).
- Reconciliação, F3.1.T8 (revisão, item 'F1.3.T4, F1.4.T3'): o passo sobre docs/poc-gate.md passou a retirar só a remissão ao script, sem reescrever o parágrafo de separação entre desenvolvimento e teste, que é de F1.3.T4. F3.1 ganhou o item de fora de escopo, a pendência de vínculo F3.1.T8 → F1.3.T4 e a origem.
- Reconciliação, F3.5.T2 (revisão, item 'F1.1.T6, F2.6'): a estrutura de pastas passou a incluir a pasta da fixture sintética que F1.1.T6 publica com revisão fixa e SHA-256. Título, objetivo, passos e definição de pronto ajustados; pendência de vínculo F3.5.T2 → F1.1.T6.
- Reconciliação, F3.6 (revisão, item 'F5.1.T3, F5.1.T4, F3.6.T3, F3.6.T4'): F3.6.T4 reutiliza o script de cópia de F5.1.T4, acrescenta o recorte por intervalo, publica a imagem por digest no fluxo de F2.2 e passa a depender de F5.1.T4 e F2.2. F3.6.T3 e F3.6.T5 seguem o procedimento de F5.1.T3 e F5.1.T5 e registram o token no inventário de F2.6.T6. Contexto, RN04, RN05, critérios 4 e 7, dependências, premissas, pendências, INVEST e a QA de F3.6.T6 foram ajustados.
- Reconciliação, F3.6.T4 (revisão, item 'Tasks que rodam job pago'): a dependência 'Aprovação de Fabio (P7), com flavor, duração e custo previstos' passou a constar na task, e não só no PBI.
- Reconciliação, novo PBI F3.8 (revisão, item 'F6.6 → F7'): adaptação condicional da ferramenta de F3.3 para ler os vídeos do destino de F7.1, gravar os rótulos no destino do ADR de F6.2 e aplicar a lista de acesso dos rotuladores do piloto, com 6 tasks (DevOps, Visão Computacional, MLOps, DevOps, Governança e Privacidade, QA). A Feature ganhou a tag fase-1, o usuário, a dependência técnica, o risco, o critério condicional, a premissa e as pendências correspondentes; fora de escopo ajustado.
- Reconciliação, pendências da Feature: a pendência com F1.4 registra que F1 já deixou de alterar tools/preparar_rotulagem.py e labels/README.md; a de P29 registra que F4 já cita F3.7; a de F2.6 aponta para o procedimento de F5.1.T3.

### Premissas
- A P3 revisada prevalece sobre P3, P9, P10 e P11 onde elas falam de Space para o front end do produto. Nesta Feature o único Space é o de rotulagem (F3.3), que exibe quadro e por isso fica no Hugging Face. F2.4 continua a decidir namespace, SDK e acesso desse Space.
- A P3 revisada diz que a ferramenta de rotulagem continua em Space privado. Com rotuladores de contas próprias, a visibilidade private exige Space de organização, e Space Gradio ou Docker de organização exige plano Team ou Enterprise (https://huggingface.co/docs/hub/spaces-overview). Por isso o título de F3.3 diz 'acesso restrito à lista de rotuladores': a opção private de organização atende à P3 revisada, e a opção protected de conta pessoal deixa o app acessível pela URL .hf.space e precisa da confirmação de Fabio.
- Nenhum fato sobre a plataforma Vercel é usado nesta Feature. A relação com a Vercel se resume à regra de não enviar a ela imagem nem dado da PIB. Plano e termos de uso da Vercel seguem como pendência do épico.
- P10 lida com 'Space' trocado por 'painel web na Vercel': vídeo e resultado da PIB não aparecem no painel antes da decisão do gate e do RIPD. Como o painel lê só do Supabase, a regra RN07 mantém os resultados da PIB fora do Supabase na Fase 0.
- P13 ajustada: se F3.1 vetar a PIB, F3.2, F3.3 e F3.5 seguem sem mudança, F3.4 é cancelado, e F3.6 e F3.7 fornecem conjuntos públicos de desenvolvimento e de teste. Se F3.4 registrar risos abaixo do mínimo, F3.4 fecha com os rótulos publicados, e F3.6 e F3.7 completam só o conjunto de teste.
- P29: as dependências de F3.6 e de F3.7 valem só se eles forem acionados.
- Tratar a imagem de plateia de um culto como dado pessoal sensível de convicção religiosa (LGPD art. 5º, II) é dedução deste backlog, usada até o parecer. A conclusão jurídica é do parecer de F3.1.
- Os rotuladores são identificados por código de papel nos registros. É extensão da P12, porque o repositório GitHub é público (API do GitHub: visibility public).
- As tasks que gravam no dataset, criam ou configuram o Space e criam ou revogam tokens na conta ds-fabiopinheiro são executadas pela conta dona (Fabio Pinheiro), porque um repositório de conta pessoal só pode ser alterado pelo dono (https://huggingface.co/docs/hub/repositories-settings). Se o ADR de F2.4 escolher organização, membros com papel de escrita podem executá-las. São elas: F3.1.T3, F3.1.T6, F3.1.T7 (parte do dataset), F3.3.T1, F3.3.T6, F3.4.T8, F3.5.T3, F3.6.T3, F3.6.T4, F3.6.T5 e F3.7.T8.
- Conta de serviço no Hugging Face existe só em organização com plano Enterprise (https://huggingface.co/docs/hub/enterprise-service-accounts). Nesta Feature, o Space e os jobs usam tokens fine-grained da conta dona, um por uso, identificados pelo nome do token.
- Os rótulos não guardam a posição do clique. A importação do CSV parcial restaura alturas por t_s e a lista de quadros revisados, sem posição. A lista de quadros revisados é proposta deste detalhamento, para distinguir 'rotulado sem rosto' de 'não rotulado' (labels/README.md:6-8).
- Story points (Fibonacci) e horas são sugestões a validar no refinamento. Duração de sprint e capacidade do time não estão registradas (P6).
- A estimativa de 3 a 4 h para cerca de 250 quadros (labels/README.md:19-20) não tem medição. As horas das tasks de rotulagem usam margem sobre ela.
- Revisão não aplicada em parte: F3.1 (critério dos comandos sem segredos) e F3.5.T5 — a revisão pedia retirar SUPABASE_URL e SUPABASE_SERVICE_KEY de todo comando que leia hf://datasets/ds-fabiopinheiro/reacao-poc-corpus. A regra ficou restrita a comandos e vídeos em pib/, porque F5.1 sobe cultos públicos ao mesmo dataset e os jobs de F5.4 gravam os resultados deles no Supabase para o painel (arvore_v1.json, F5.1; P10).
- Revisão não aplicada: F3.2.T3 e F3.1 (adendo datado ao parecer para registrar o uso do som) — com o som fixado como desligado pela regra 5, não há exceção à regra 5 a registrar no parecer.
- Revisão não aplicada em parte: F3.5.T5 — a retirada da instrução 'hf upload ... ./samples' (docs/hf-jobs.md:8) continua na task, embora não seja leitura por revisão nem segredo do Supabase. A linha fica fora do trecho que F2.1 reescreve (docs/hf-jobs.md:13-30 nas fontes de F2.1 em arvore_v1.json), parte de cópia local do corpus, proibida pela regra 1 do CLAUDE.md e pela RN05 de F3.1, e é exigida pelo critério 8 de F3.5. Com a nova dependência, F3.5.T5 roda depois de F2.1.T6. Se a linha já tiver saído, o passo vira conferência.
- F3.8 fica nesta Feature porque a ferramenta de rotulagem é de F3.3. A revisão da árvore aceitava F7.1.T1 como alternativa (consolidacao.json, item 5). Se o time preferir, o PBI pode ser movido para F7 sem mudar o conteúdo.

### Pendências para sincronizar
- ID do Epic pai no Azure DevOps (link System.LinkTypes.Hierarchy-Reverse)
- Area Path (Time), Iteration Path e Responsável da Feature
- Business Value e posição no backlog (Backlog Priority), campos do processo Scrum (https://learn.microsoft.com/en-us/azure/devops/boards/work-items/guidance/scrum-process-workflow)
- Confirmar se o projeto estima PBI em Effort (padrão do Scrum) ou em Story Points. As sugestões estão em pontos Fibonacci.
- Mapear a disciplina das tasks para o campo Activity ou para uma tag. As disciplinas deste backlog não são valores de Activity.
- Tags em System.Tags separadas por ';'
- Nome do encarregado de dados e de quem responde pela governança. Dono sugerido do impedimento da nomeação: Fabio Pinheiro, a confirmar.
- Pendência com F1.4: separar no validador os erros de arquivo dos mínimos de conteúdo (risos de F1.3, 4 trechos neutros e arquivo sem rosto >= 64 px) e aplicar os mínimos só à pasta de teste. F1 detalhada já deixou de alterar tools/preparar_rotulagem.py e labels/README.md (RN14 e RN11 de F1.4).
- Pendência com F1.3: na Fase 0, nenhum job que grava no Supabase (fumaça, paridade, painel) usa clipe da PIB. A lista de vídeos por tipo de job precisa refletir isso.
- Pendência com F2.6: reconhecer como uso previsto o token de leitura do Space de F3.3 e, em F3.8, os tokens do Space para o piloto. O token de escrita de F3.6 entra no inventário de F2.6.T6 pelo procedimento de F5.1.T3.
- Pendência com F5.1: excluir da seleção os vídeos marcados por F3.6 em docs/corpus.csv.
- Pendência com F4.4: medir a razão entre altura manual e altura da caixa do detector pelo método sem pareamento definido em F3.2.
- P29: as Features que citam F3.6 passam a citar também F3.7. F4 detalhada já aplicou em F4.1, F4.2, F4.4, F4.5 e F4.6; falta a métrica do critério 1 do épico.
- Custo do plano Team ou Enterprise, se o ADR de F2.4 escolher Space de organização.
- Pendência com F2.1 e F2.6: F3.5.T5 depende de F2.1.T6 e F2.6.T2. Avisar os responsáveis de que F3.5.T5 altera nos comandos só caminhos hf://, a nota sobre -v, a instrução de upload local e os segredos do Supabase sobre pib/.
- Vínculos F3.1.T8 → F1.3.T4 e F3.5.T2 → F1.1.T6 no Azure DevOps.
- F7: as tasks de rotulagem dos cultos do piloto dependem de F3.8; F7.1.T1 registra a leitura do destino pelo Space de F3.8.

## Preview — PBI F3.1 (novo) · Analisar a base legal do uso dos clipes da PIB na Fase 0 e registrar autorização, acesso e retenção no dataset card

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Analisar a base legal do uso dos clipes da PIB na Fase 0 e registrar autorização, acesso e retenção no dataset card |
| Tipo | Product Backlog Item |
| Pai | F3 |
| Tags | fase-0; lgpd; corpus; governanca |
| Estimativa | 8 pts (sugestão); tasks: 38 h |
| Dependências | F3.5.T3 (dataset card publicado, com o estado 'parecer pendente'), para F3.1.T6, F3.5.T4 (resolve_video com revisão), para F3.1.T9, F3.5.T5 (comandos de docs/hf-jobs.md sem segredos do Supabase sobre pib/, feita depois de F2.1.T6 e F2.6.T2), para a verificação de F3.1.T10, F2.6 (tokens fine-grained que substituem o token clássico; projeto Supabase de desenvolvimento para a consulta da QA), Encarregado de dados nomeado, obtido em F3.1.T2 (impedimento com dono sugerido), Pastor Filipe disponível para confirmar autorização e escopo |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro, responsável pelo gate da Fase 0 e dono do dataset privado  
Quero nenhuma cópia dos clipes da PIB fora do Hugging Face desde já, um encarregado nomeado e um parecer datado dele sobre o uso dos clipes na Fase 0, registrado no dataset card com autorização, conclusão, lista de acesso e retenção  
Para rotular e processar os clipes só dentro do que o parecer permite, ou trocar de corpus (F3.6) antes de gastar horas de rotulagem

**Contexto:** O corpus dos critérios 1 e 2 são 23 clipes de plateia da PIB (1920x1080, 15 fps, 236 s no total). O pastor Filipe os compartilhou numa pasta do Google Drive em 2026-09-05, 'com autorização de uso no piloto' (samples/corpus/pib/README.md:3-8, não versionado). Eles estão no dataset privado ds-fabiopinheiro/reacao-poc-corpus desde o commit 75e001af52, cujo título registra 'autorizado por Pastor Filipe, 2026-09-05' (HfApi.list_repo_commits no levantamento). O README descreve a Fase 0 com vídeos públicos de pregação (README.pt-BR.md:34; README.md:34), e o gate põe os dados da PIB depois da decisão (docs/poc-gate.md:50). A LGPD classifica como sensível o dado sobre convicção religiosa (art. 5º, II), e trata do dado sensível no art. 11, da transferência internacional no art. 33 e do encarregado no art. 41 (https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm). O repositório não tem análise de base legal e não nomeia encarregado nem controlador, e nenhum item do backlog tem a nomeação como trabalho. tools/rodar_teste.sh baixa o dataset para samples/corpus em disco e roda o bench em CPU fora do HF (tools/rodar_teste.sh:12,35-40,55). Nesta sessão de desenvolvimento, samples/corpus/pib tem 24 arquivos .mp4 (23 clipes e o concatenado), e há cópia do dataset em ~/.cache/huggingface/hub/datasets--ds-fabiopinheiro--reacao-poc-corpus e em samples/corpus/.cache/huggingface. No cache do huggingface_hub o conteúdo fica em blobs/ com nome de hash, e o nome do arquivo é só um link em snapshots/ (https://huggingface.co/docs/hub/local-cache). O clipe 11 e o concatenado já passaram pelo pipeline numa execução local, e os resultados estão em out/run_log.json e out/window_aggregate.json, com os cultos poc-igreja_simples_11 e poc-igreja_simples_concat (locais, fora do git por .gitignore:224; P28). O HF_TOKEN do ambiente é um token clássico de escrita com escopo de conta, 'claude-code-teste-pib' (huggingface_hub.whoami() em 2026-09-23). O pib/README.md do dataset traz o e-mail pessoal do pastor, o link da pasta do Drive e a citação a pib_drive_manifest.csv, que não está no dataset (samples/corpus/pib/README.md:3-4,13; listagem do dataset). docs/hf-jobs.md:13-19 e a docstring de processar_culto.py:12-13 mandam passar SUPABASE_URL e SUPABASE_SERVICE_KEY a um job que lê o dataset do corpus, e o Store grava no Supabase sempre que as duas variáveis existem (reacao/store.py:10-26). Um repositório de conta pessoal só aceita o dono, e dar acesso a outras pessoas exige organização (https://huggingface.co/docs/hub/repositories-settings). Por isso os rotuladores chegam aos clipes só pelo Space de F3.3. O repositório GitHub é público (API do GitHub: visibility public), então parecer, contas e nomes ficam no dataset privado.

**Regras de negócio:**
- RN01 – O parecer é do encarregado, tem data e conclui por uma de três opções: uso permitido, uso permitido com as condições listadas ou uso não permitido na Fase 0.
- RN02 – O parecer cobre rotulagem humana no Space, processamento no HF Jobs, cópia existente no dataset privado, tratamentos já feitos e resultados derivados (P28), transferência internacional (LGPD art. 33), retenção e eliminação, e lista de acesso.
- RN03 – Com a conclusão 'uso não permitido', nenhuma rotulagem ou job sobre clipes da PIB começa, F3.4 é cancelado, F3.6 é acionado, e o card registra o destino dos clipes já no dataset conforme o parecer.
- RN04 – A lista de acesso nomeia contas do Hugging Face por papel (dono, rotuladores) e os tokens fine-grained da conta dona com acesso ao dataset, pelo nome e pelo uso. Quem está fora da lista não acessa o dataset nem o Space de rotulagem, e o token clássico de escrita da conta é revogado.
- RN05 – Nenhuma cópia dos clipes fica em disco nos ambientes de desenvolvimento. A eliminação acontece já, sem esperar o parecer, porque as cópias ferem a regra 1 do CLAUDE.md, e fica registrada com data. A pasta de origem no Drive e o dataset privado não entram nessa eliminação.
- RN06 – Na Fase 0, nenhum vídeo, quadro, recorte ou resultado dos clipes da PIB vai ao Supabase nem ao painel web na Vercel. processar_culto.py recusa gravar no Supabase quando o vídeo vem de pib/ do dataset do corpus, e nenhum comando documentado sobre pib/ passa os segredos do Supabase.
- RN07 – Parecer, nomes e contas ficam no dataset privado. O repositório público recebe só texto sem dado pessoal.
- RN08 – O texto da Fase 0 nos READMEs descreve o corpus que o parecer permite.

**Fora de escopo:**
- RIPD da Fase 1 e notas de lei em docs/law/br.md (F6.3)
- Aviso à congregação e forma de oposição ou consentimento (F6.4, F6.5)
- Estrutura do dataset card, Dataset Viewer desligado e tags (F3.5)
- Revisão nos caminhos de docs/hf-jobs.md e retirada dos segredos do Supabase dos comandos sobre pib/ (F3.5.T5); forma de passar segredos nos comandos (F2.1.T6, F2.6.T2)
- Uso do som na rotulagem, que fica desligado pela regra 5 (F3.2)
- Pasta de origem no Google Drive do pastor Filipe, que o projeto não controla. O parecer pode recomendar algo sobre ela, mas este PBI não a altera.
- Vídeos do piloto (F7.1)
- Redação do parágrafo de separação entre desenvolvimento e teste de docs/poc-gate.md:46-48, que é de F1.3.T4 (F1 detalhada)

#### Critérios de aceite

- O dataset privado contém um parecer do encarregado, com data e assinatura, que conclui por uma das três opções e trata de rotulagem humana, processamento no HF Jobs, cópia no dataset, tratamentos já feitos, transferência internacional, retenção e acesso.
- O dataset card mostra quem autorizou (pastor Filipe), o escopo ('uso no piloto'), a data da autorização (2026-09-05), a conclusão e a data do parecer, a lista de acesso por papel e conta, os tokens com acesso ao dataset por nome e uso, o prazo de retenção e a data de revisão, sem e-mail pessoal.
- Enquanto o parecer não existir, o dataset card mostra o estado 'parecer pendente'.
- Caminho de erro: com a conclusão 'uso não permitido', o card registra F3.4 como cancelado, F3.6 como acionado e o destino dos clipes já no dataset, e o dataset não recebe pasta de rótulos da PIB.
- Em cada ambiente de desenvolvimento do inventário, a busca não encontra arquivo igreja_simples_*.mp4, o cache do huggingface_hub não tem a pasta datasets--ds-fabiopinheiro--reacao-poc-corpus e samples/corpus/.cache/huggingface não existe. A eliminação está registrada no card com ambiente e data.
- A lista de tokens da conta ds-fabiopinheiro não tem token clássico de escrita, e cada token com acesso ao dataset aparece no card com nome e uso.
- tools/rodar_teste.sh não existe mais no repositório, e nenhum arquivo do repositório o cita.
- O pib/README.md do dataset não cita arquivo ausente do dataset nem traz e-mail pessoal.
- A linha da Fase 0 nos 7 READMEs descreve o corpus que o parecer permite.
- O repositório público não contém nome de rotulador, conta de rotulador nem o texto do parecer.
- processar_culto.py, com SUPABASE_URL e SUPABASE_SERVICE_KEY definidos e --video na subpasta pib/ do dataset do corpus, termina com código diferente de 0 antes de baixar o vídeo e sem gravar no Supabase. Nenhum comando documentado sobre pib/ passa esses segredos.
- Se o projeto Supabase de desenvolvimento de F2.6 existir, a consulta às tabelas não encontra culto com 'igreja_simples' no nome. Se não existir, o registro da QA diz isso.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F3.1.T1 | DevOps | Eliminar já as cópias locais dos clipes da PIB nos ambientes de desenvolvimento | 3 | — |
| F3.1.T2 | Governança e Privacidade | Identificar o controlador e obter dele a nomeação do encarregado de dados | 4 | — |
| F3.1.T3 | DevOps | Revogar o token clássico de escrita e substituí-lo pelos tokens fine-grained de F2.6 | 2 | F2.6, F3.1.T4 |
| F3.1.T4 | Governança e Privacidade | Levantar o inventário de tratamento dos clipes da PIB na Fase 0 | 4 | — |
| F3.1.T5 | Governança e Privacidade | Elaborar com o encarregado o parecer de base legal do uso dos clipes da PIB na Fase 0 | 8 | F3.1.T2, F3.1.T4 |
| F3.1.T6 | Governança e Privacidade | Registrar no dataset card autorização, conclusão, lista de acesso, tokens, retenção e eliminação | 3 | F3.1.T1, F3.1.T3, F3.1.T5, F3.5.T3 |
| F3.1.T7 | Governança e Privacidade | Alinhar os READMEs e o pib/README.md do dataset ao uso decidido | 3 | F3.1.T5 |
| F3.1.T8 | DevOps | Remover tools/rodar_teste.sh e as referências a ele | 3 | — |
| F3.1.T9 | Backend | Recusar gravação no Supabase quando o vídeo vem de pib/ do dataset do corpus | 4 | F3.5.T4 |
| F3.1.T10 | QA | Verificar os critérios de aceite de F3.1 | 4 | F3.1.T6, F3.1.T7, F3.1.T8, F3.1.T9, F3.5.T5 |

<details><summary>F3.1.T1 · [DevOps] Eliminar já as cópias locais dos clipes da PIB nos ambientes de desenvolvimento</summary>

**Objetivo:** Acabar com as cópias dos clipes da PIB em disco nos ambientes de desenvolvimento, sem esperar o parecer, e deixar a eliminação registrada.

**Passos previstos:**
1. Pedir a Fabio a lista dos ambientes de desenvolvimento que já baixaram o dataset, além da sessão desta análise.
2. Em cada ambiente, apagar samples/corpus (inclusive samples/corpus/.cache/huggingface) e a pasta datasets--ds-fabiopinheiro--reacao-poc-corpus do cache do huggingface_hub (https://huggingface.co/docs/huggingface_hub/guides/manage-cache).
3. Conferir que a busca por igreja_simples_*.mp4 não encontra arquivo e que a listagem do cache do huggingface_hub não mostra o repositório.
4. Não apagar out/run_log.json nem out/window_aggregate.json, que não têm imagem e aguardam o parecer e o registro de F1.3.
5. Registrar no PBI (registro provisório) o ambiente, a data e o código de papel de quem eliminou.

**Definição de pronto:** Nos ambientes listados, busca por igreja_simples_*.mp4 sem resultado, cache sem a pasta do dataset, samples/corpus ausente e registro provisório no PBI.

**Dependências:** nenhuma

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F3.1.T2 · [Governança e Privacidade] Identificar o controlador e obter dele a nomeação do encarregado de dados</summary>

**Objetivo:** Ter um encarregado nomeado, com a nomeação registrada no dataset privado, para que o parecer possa começar.

**Passos previstos:**
1. Registrar quem é o controlador do tratamento dos clipes na Fase 0, com Fabio Pinheiro e o pastor Filipe.
2. Levar ao controlador o pedido de indicação do encarregado (LGPD art. 41).
3. Registrar no dataset privado o nome, a data da nomeação e o contato de trabalho do encarregado.
4. Se a nomeação não sair até a data combinada no refinamento, registrar o impedimento no épico com o dono sugerido (Fabio Pinheiro).

**Definição de pronto:** Nomeação registrada no dataset privado com data, ou impedimento registrado no épico com dono e data.

**Dependências:** nenhuma

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F3.1.T3 · [DevOps] Revogar o token clássico de escrita e substituí-lo pelos tokens fine-grained de F2.6</summary>

**Objetivo:** Deixar com acesso ao dataset só tokens fine-grained da conta dona, cada um com nome e uso conhecidos.

**Passos previstos:**
1. Conferir a lista de tokens do inventário de T4, com os ambientes onde cada um está.
2. Distribuir aos ambientes de desenvolvimento os tokens fine-grained de F2.6 que substituem o token clássico.
3. Revogar o token clássico de escrita 'claude-code-teste-pib' na conta ds-fabiopinheiro (https://huggingface.co/docs/hub/security-tokens).
4. Registrar no PBI os tokens restantes com nome, papel, repositórios e uso.

**Definição de pronto:** Lista de tokens da conta sem token clássico de escrita e registro dos tokens restantes no PBI.

**Dependências:** F2.6, F3.1.T4

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F3.1.T4 · [Governança e Privacidade] Levantar o inventário de tratamento dos clipes da PIB na Fase 0</summary>

**Objetivo:** Ter no dataset privado um documento com as cópias, os tratamentos feitos e previstos, os resultados derivados, os operadores, os dados, os acessos e a retenção atual dos clipes da PIB.

**Passos previstos:**
1. Listar as cópias: pasta de origem no Google Drive (samples/corpus/pib/README.md:3-4), dataset privado no commit 75e001af52 e os ambientes de desenvolvimento, com o registro de eliminação de T1.
2. Listar os tratamentos já feitos: execução local do pipeline sobre o clipe 11 e o concatenado (P28), com os resultados em out/run_log.json e out/window_aggregate.json.
3. Listar os tratamentos previstos: rotulagem humana no Space (F3.3, F3.4), bench e calibração no HF Jobs (F4.4 a F4.6) e jobs permitidos por F1.3.
4. Listar os operadores (serviços do Hugging Face) e registrar que Supabase e Vercel não recebem dado da PIB na Fase 0.
5. Registrar os dados envolvidos: imagem de plateia a 1920x1080 e trilha de áudio do vídeo editado (samples/corpus/pib/README.md:7-8).
6. Registrar quem acessa hoje: a conta dona e os tokens com acesso ao dataset, com os ambientes onde estão.
7. Registrar a retenção atual (sem prazo definido).

**Definição de pronto:** Inventário salvo no dataset privado, com as sete listas preenchidas e revisado por Fabio Pinheiro.

**Dependências:** nenhuma

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F3.1.T5 · [Governança e Privacidade] Elaborar com o encarregado o parecer de base legal do uso dos clipes da PIB na Fase 0</summary>

**Objetivo:** Ter um parecer datado e assinado que conclua se, e em que condições, os clipes da PIB podem ser rotulados e processados na Fase 0.

**Passos previstos:**
1. Apresentar o inventário de T4 ao encarregado.
2. Avaliar a autorização registrada ('de uso no piloto', 2026-09-05) frente ao uso na Fase 0 e ao art. 11 da LGPD.
3. Avaliar a transferência internacional ao Hugging Face (art. 33).
4. Avaliar os tratamentos já feitos e o destino dos resultados derivados locais.
5. Definir as condições: lista de acesso com contas e tokens, prazo de retenção e proibição de envio ao Supabase e ao painel web na Vercel na Fase 0.
6. Registrar a conclusão (permitido, permitido com condições ou não permitido) com data e assinatura do encarregado.
7. Salvar o parecer no dataset privado.

**Definição de pronto:** Parecer datado e assinado pelo encarregado no dataset privado, com uma das três conclusões e as condições.

**Dependências:** F3.1.T2, F3.1.T4

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F3.1.T6 · [Governança e Privacidade] Registrar no dataset card autorização, conclusão, lista de acesso, tokens, retenção e eliminação</summary>

**Objetivo:** Deixar o dataset card com os campos dos critérios 2 e 5 preenchidos a partir do parecer e dos registros de T1 e T3.

**Passos previstos:**
1. Preencher a seção de governança do card criado em F3.5.
2. Registrar a autorização: pastor Filipe, 'uso no piloto', 2026-09-05, sem e-mail.
3. Registrar a conclusão e a data do parecer.
4. Registrar a lista de acesso por papel e conta do Hugging Face (dono, rotuladores) e os tokens da conta dona com acesso ao dataset, por nome e uso.
5. Copiar para o card o registro provisório de eliminação de T1.
6. Registrar o prazo de retenção e a data de revisão.
7. Registrar o destino que o parecer der a out/run_log.json e out/window_aggregate.json e confirmar com quem os tem que ele foi aplicado depois do registro de F1.3.
8. Se a conclusão for 'não permitido', registrar F3.4 como cancelado, F3.6 como acionado e o destino dos clipes.
9. Publicar o card num commit do dataset, pela conta dona.

**Definição de pronto:** Card publicado no Hub com os campos dos critérios 2 e 5 e commit registrado no PBI.

**Dependências:** F3.1.T1, F3.1.T3, F3.1.T5, F3.5.T3

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F3.1.T7 · [Governança e Privacidade] Alinhar os READMEs e o pib/README.md do dataset ao uso decidido</summary>

**Objetivo:** Fazer a descrição da Fase 0 e o README do corpus corresponderem ao parecer e ao conteúdo real do dataset, sem dado pessoal desnecessário.

**Passos previstos:**
1. Reescrever a linha da Fase 0 em README.pt-BR.md:34 e README.md:34 conforme a conclusão do parecer.
2. Aplicar a mesma mudança às traduções ar, bn, hi, ja e zh-CN.
3. No pib/README.md do dataset, remover a citação ao pib_drive_manifest.csv ou publicar o arquivo, conforme o parecer. O manifesto tem nome original e ID no Drive (samples/corpus/pib/README.md:13).
4. No pib/README.md do dataset, retirar o e-mail pessoal do pastor (samples/corpus/pib/README.md:3) e tratar o link da pasta do Drive (samples/corpus/pib/README.md:4) conforme o parecer.
5. Abrir PR no repositório citando o PBI e fazer, pela conta dona, o commit no dataset.

**Definição de pronto:** PR mesclado e commit no dataset. A linha da Fase 0 diz a mesma coisa nos 7 READMEs, e pib/README.md não cita arquivo ausente nem traz e-mail pessoal.

**Dependências:** F3.1.T5

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F3.1.T8 · [DevOps] Remover tools/rodar_teste.sh e as referências a ele</summary>

**Objetivo:** Deixar o repositório sem roteiro que baixe o corpus para disco ou rode o bench fora do HF.

**Passos previstos:**
1. Mover para docs/hf-jobs.md, numa seção de notas separada dos comandos que F2.1.T6, F2.6.T2 e F3.5.T5 alteram, o que o script registra além do download: o contorno do 403 do HSEmotion (tools/rodar_teste.sh:29-33, a resolver em F2.3) e o aviso de que 'uv run' sem --no-sync desinstala os motores (tools/rodar_teste.sh:23-24).
2. Apagar tools/rodar_teste.sh.
3. Em docs/poc-gate.md:48, retirar só a remissão a tools/rodar_teste.sh, sem reescrever o parágrafo 'Separação entre desenvolvimento e teste' (docs/poc-gate.md:46-48), que F1.3.T4 reescreve e F1.3.T5 leva à assinatura. Atualizar qualquer outra referência ao script.
4. Rodar ruff check e pytest.
5. Abrir PR citando o ID do PBI.

**Definição de pronto:** PR mesclado, tools/rodar_teste.sh ausente, busca por 'rodar_teste' no repositório sem resultado, parágrafo de docs/poc-gate.md:46-48 alterado só na remissão ao script e CI verde.

**Dependências:** nenhuma

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F3.1.T9 · [Backend] Recusar gravação no Supabase quando o vídeo vem de pib/ do dataset do corpus</summary>

**Objetivo:** Transformar a regra RN06 em barreira no código: processar_culto.py não grava resultado de clipe da PIB no Supabase.

**Passos previstos:**
1. Em processar_culto.py, antes de baixar o vídeo, terminar com código diferente de 0 e mensagem que cita a regra quando --video estiver na subpasta pib/ do dataset do corpus e SUPABASE_URL ou SUPABASE_SERVICE_KEY estiverem definidos.
2. Manter a execução sem os segredos, que grava nos arquivos de saída (reacao/store.py:19-23).
3. Escrever testes com as funções do huggingface_hub substituídas: recusa com os segredos e vídeo em pib/, execução sem os segredos e execução com os segredos e vídeo fora de pib/.
4. Rodar ruff check e pytest e abrir PR citando o PBI.

**Definição de pronto:** PR mesclado, testes novos passando no CI e nenhum download nos testes de recusa.

**Dependências:** F3.5.T4

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F3.1.T10 · [QA] Verificar os critérios de aceite de F3.1</summary>

**Objetivo:** Registrar passou ou não passou para cada critério de aceite do PBI.

**Passos previstos:**
1. Conferir no card cada campo do critério 2 e o estado anterior 'parecer pendente' no histórico do dataset.
2. Conferir no parecer a data, a assinatura, a conclusão e os temas do critério 1.
3. Repetir, em cada ambiente de desenvolvimento do inventário, a busca por igreja_simples_*.mp4 e a listagem do cache do huggingface_hub, e conferir a ausência de samples/corpus/.cache/huggingface.
4. Conferir com Fabio a lista de tokens da conta e compará-la com o card.
5. Buscar no repositório público nomes e contas de rotuladores e trechos do parecer.
6. Rodar processar_culto.py com os segredos do Supabase definidos com valores de teste e --video em pib/, e conferir o código de saída e a ausência de download.
7. Conferir que os comandos documentados sobre pib/ não passam SUPABASE_URL nem SUPABASE_SERVICE_KEY.
8. Se o projeto Supabase de desenvolvimento de F2.6 existir, consultar as tabelas por culto com 'igreja_simples' no nome e registrar o resultado. Se não existir, registrar isso.
9. Conferir a ausência de tools/rodar_teste.sh e das referências a ele, os 7 READMEs e o pib/README.md do dataset.

**Definição de pronto:** Checklist dos 12 critérios anexado ao PBI, com passou ou não passou por critério.

**Dependências:** F3.1.T6, F3.1.T7, F3.1.T8, F3.1.T9, F3.5.T5

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- samples/corpus/pib/README.md:3-8,12-13,20 (não versionado; cópia de pib/README.md do dataset)
- README.pt-BR.md:34-35; README.md:34
- docs/poc-gate.md:50
- tools/rodar_teste.sh:12,23-24,29-40,55
- docs/hf-jobs.md:13-19
- processar_culto.py:12-13,23-31,56-61
- reacao/store.py:10-26
- out/run_log.json e out/window_aggregate.json (locais; cultos poc-igreja_simples_11 e poc-igreja_simples_concat); .gitignore:224
- CLAUDE.md (regras 1 e 5)
- HfApi.list_repo_commits e dataset_info (levantamento de 2026-09-23); hf_fs ls do dataset em 2026-09-23
- huggingface_hub.whoami() em 2026-09-23 (token clássico de papel write, 'claude-code-teste-pib')
- Listagem local nesta sessão: samples/corpus/pib com 24 arquivos .mp4; ~/.cache/huggingface/hub/datasets--ds-fabiopinheiro--reacao-poc-corpus; samples/corpus/.cache/huggingface
- arvore_v1.json: F6.3 (único item que cita o encarregado), F1.3 (vídeos por tipo de job), F2.6 (projeto Supabase de desenvolvimento)
- https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm (art. 5º, II; art. 11; art. 33; art. 41)
- https://huggingface.co/docs/hub/repositories-settings
- https://huggingface.co/docs/hub/local-cache
- https://huggingface.co/docs/huggingface_hub/guides/manage-cache
- https://huggingface.co/docs/hub/security-tokens
- https://huggingface.co/docs/hub/enterprise-service-accounts
- API do GitHub: ds-fabiopinheiro/church-sentiment-analysis com visibility public
- F1 detalhada: F1.3.T4 depende de F3.1.T8; F1.4.T3 cobre só tools/validar_labels.py e bench.py (RN14 de F1)

#### Verificação INVEST: pontos que falharam
- Independente: o parecer depende do encarregado, cuja nomeação é a task T2 e ainda não tem data. T6 depende do card de F3.5, T3 depende dos tokens de F2.6, e T10 espera F3.5.T5, que espera F2.1.T6 e F2.6.T2.
- Estimável: a duração do parecer depende da agenda do encarregado e da conclusão.
- Small: 10 tasks e cerca de 38 h sugeridas. Se o parecer demorar, eliminação, inventário, remoção do script e barreira fecham antes, e o parecer pode passar de uma sprint.

#### Premissas
- Disciplinas: a árvore previa Governança e Privacidade, DevOps e Data Science. Entrou QA, porque o PBI altera o repositório e o dataset. Entrou Backend, para a barreira em processar_culto.py (T9). Saiu Data Science: o alinhamento dos READMEs é documentação ligada à conclusão legal e passou a Governança e Privacidade (P5).
- A eliminação das cópias locais não espera o parecer: as cópias ferem a regra 1 do CLAUDE.md, e o dataset privado continua como cópia de referência. O registro fica no PBI até o card existir, e T6 o copia para o card.
- O destino dos resultados derivados locais (out/) segue o parecer e só é aplicado depois de F1.3 registrar a exposição do clipe 11 e do concatenado (P28).
- A barreira em processar_culto.py vale para vídeos em pib/, porque F5.1 sobe cultos públicos ao mesmo dataset e os jobs de F5.4 gravam os resultados deles no Supabase. É proposta deste detalhamento.
- Das duas opções da árvore para tools/rodar_teste.sh, a remoção foi escolhida porque F1.1 já cria o script de lançamento que recusa caminho local. Um segundo lançador duplicaria esse trabalho.
- Parecer e lista de acesso ficam no dataset privado. É dedução a partir da visibilidade pública do repositório.
- Na Fase 0, os operadores que tocam os clipes da PIB são só os serviços do Hugging Face (dataset, Jobs, Space de rotulagem). Supabase e Vercel ficam fora, pela P3 revisada e pela P10 lida com 'painel web na Vercel'.
- Só a sessão de desenvolvimento desta análise foi verificada quanto a cópias locais. Os outros ambientes de desenvolvimento são listados por Fabio em T1 e entram no inventário de T4.
- O controlador do tratamento não está identificado no repositório. Dono sugerido do impedimento da nomeação do encarregado: Fabio Pinheiro, responsável pelo gate e dono do dataset, a confirmar no refinamento.
- 'Governança' é o papel de quem conduz a análise com o encarregado. O repositório não nomeia essa pessoa.
- Com a conclusão 'uso não permitido', o destino dos clipes já no dataset (manter até o RIPD ou eliminar) segue o parecer.
- T3, T6 e a parte do dataset de T7 são executadas pela conta dona, porque um repositório de conta pessoal só pode ser alterado pelo dono.
- Estimativas (8 pontos e horas das tasks) são sugestão.

#### Pendências para sincronizar
- Nome do encarregado de dados, do controlador e de quem responde pela governança
- Area Path, Iteration Path e Responsável
- Link com a Feature F3 como pai
- Effort ou Story Points: 8 como sugestão (no Scrum o campo padrão é Effort)
- Avisar o responsável por F1.3 de que tools/rodar_teste.sh será removido aqui. Se F3.1 vier antes, a correção de tools/rodar_teste.sh:59-61 prevista em F1.3 perde o objeto.
- Alinhar com F1.3 a lista de vídeos por tipo de job: na Fase 0, nenhum job que grava no Supabase (fumaça, paridade, painel) usa clipe da PIB (RN06).
- Avisar F1.3 de que o registro de exposição do clipe 11 e do concatenado (P28) usa out/ local, cujo destino segue o parecer.
- Tags: fase-0; lgpd; corpus; governanca
- Vínculo F3.1.T8 → F1.3.T4 no Azure DevOps. F1 pede que F3.1.T8 entre na sprint de F1.3, porque F1.3.T4 e a revisão de F1.3.T5 esperam por ela (F1 detalhada, pendências).

## Preview — PBI F3.2 (novo) · Definir o protocolo de rotulagem de rostos, quadros revisados e eventos, com medida de altura comparável à caixa do detector e som desligado

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Definir o protocolo de rotulagem de rostos, quadros revisados e eventos, com medida de altura comparável à caixa do detector e som desligado |
| Tipo | Product Backlog Item |
| Pai | F3 |
| Tags | fase-0; gate-poc; rotulagem; protocolo |
| Estimativa | 3 pts (sugestão); tasks: 16 h |
| Dependências | F1.3 (mínimo de eventos de riso e exigência de caixas na Fase 1) |
| Substitui | nenhum |

#### Descrição

Como rotulador dos clipes dos critérios 1 e 2  
Quero um protocolo escrito que diga como medir a altura de cada rosto, como registrar um quadro revisado sem rosto, como marcar riso e trecho neutro, como a concordância é medida e como meu trabalho é revisado  
Para que rótulos de pessoas diferentes meçam a mesma grandeza que o bench compara com o detector, e que o recall e a sensibilidade não dependam de quem rotulou

**Contexto:** labels/README.md define os arquivos. <video>_faces.csv tem t_s e altura_px, um rosto por linha, em todos os quadros amostrados. <video>_eventos.csv tem t_ini_s, t_fim_s e tipo entre riso, aplauso, pe, cabeca_baixa e neutro. O README não diz como medir altura_px, como delimitar riso e trecho neutro, quem rotula, como se mede a concordância nem como se revisa (labels/README.md:6-17). Um quadro sem rosto visível fica sem linha em _faces.csv, e o formato não distingue 'rotulado sem rosto' de 'não rotulado' (labels/README.md:6-8; tools/validar_labels.py:92-95). O bench conta no recall só rostos marcados com altura_px >= 64 (bench.py:123-128; reacao/types.py:5) e os compara, por contagem, com os rostos que o detector acha no mesmo quadro. A altura do detector é a da caixa do SCRFD, y2 - y1 (reacao/detect.py:32-33). O SCRFD foi avaliado no WIDER FACE (https://arxiv.org/abs/2105.04714), cujas caixas contêm testa, queixo e bochechas (https://openaccess.thecvf.com/content_cvpr_2016/papers/Yang_WIDER_FACE_A_CVPR_2016_paper.pdf). _faces.csv não tem posição nem caixa por rosto, e o pareamento por caixa e IoU fica para depois do PoC (docs/poc-gate.md:20-21). Por isso a altura manual não pode ser pareada rosto a rosto com a caixa do detector. O bench descarta intervalo de evento sem segundo inteiro amostrado, e um riso nessa situação conta como não atingido (bench.py:73-81). O validador exige, no corpus inteiro, pelo menos 1 riso e 4 trechos neutros (tools/validar_labels.py:215-220). O mínimo de risos para o critério 2a ser conclusivo sai de F1.3. labels/README.md:15 diz que 'no PoC o som do próprio vídeo pode confirmar a marcação'. A regra 5 do CLAUDE.md está entre as 'Regras que nunca mudam (falha de CI se violadas)' e diz que a única entrada de áudio é a trilha do arquivo, usada só para transcrever o púlpito (CLAUDE.md:9,20). A trilha dos clipes da PIB é a do vídeo editado (samples/corpus/pib/README.md:8). Por isso o protocolo fixa o som desligado. O repositório é público, então o protocolo não leva nome nem conta de rotulador. A concordância é medida em F3.4 com a ferramenta de F3.3, porque os clipes não podem ser abertos fora dela. O local único dos rótulos é tratado em F3.5.

**Regras de negócio:**
- RN01 – altura_px é medida em pixels do quadro na resolução nativa, pela regra do protocolo, que busca a mesma grandeza da caixa do detector.
- RN02 – Todo rosto visível a partir do menor tamanho definido no protocolo recebe uma linha em _faces.csv, em todos os quadros amostrados do clipe (labels/README.md:6-8).
- RN03 – Todo t_s da grade que o rotulador termina de revisar entra na lista de quadros revisados do clipe, inclusive quadro sem rosto a marcar. A lista tem só t_s.
- RN04 – Durante a rotulagem, os rotuladores não veem a saída do detector nem do pipeline.
- RN05 – Todo intervalo de evento contém pelo menos um segundo inteiro amostrado (bench.py:73-81).
- RN06 – Os rotuladores são identificados nos registros por código de papel, não por nome.
- RN07 – O som do vídeo não é tocado na rotulagem (CLAUDE.md regra 5). Mudar isso exige alterar o CLAUDE.md, decisão do dono do repositório.
- RN08 – A concordância é medida numa amostra de quadros dos clipes de desenvolvimento, antes dos clipes de teste, com métrica e limite fixados no protocolo. Abaixo do limite, os rotuladores repetem a amostra depois de revisar o protocolo.
- RN09 – O protocolo diz se quem calibra em F4.5 pode rotular os clipes de teste.
- RN10 – A comparação entre altura manual e altura da caixa do detector é feita sem pareamento rosto a rosto, pelo método do protocolo, e é registrada como aproximação.

**Fora de escopo:**
- Caixas por rosto e recall pareado por IoU, salvo decisão de F1.3
- Rótulos de momentos de culto inteiro (F5.1)
- Medição da concordância, que acontece em F3.4
- Medição da razão entre altura manual e altura da caixa do detector nos clipes de desenvolvimento, que acontece em F4.4
- Ferramenta de rotulagem (F3.3)
- Unificação do local dos rótulos na documentação e nas ferramentas (F3.5)
- Mudança da regra 5 do CLAUDE.md

#### Critérios de aceite

- O protocolo está versionado no repositório e define a regra de medida de altura_px com exemplos, o menor rosto a marcar e o tratamento de rosto de perfil, parcialmente oculto, de cabeça baixa e cortado na borda.
- O protocolo define riso, neutro, aplauso, pe e cabeca_baixa de forma operacional, com o critério de início e fim do intervalo e a exigência de pelo menos um segundo inteiro amostrado.
- O protocolo define como registrar um quadro revisado sem rosto a marcar, pela lista de t_s revisados do clipe, sem posição de rosto.
- O protocolo diz que o som do vídeo não é tocado na rotulagem e cita a regra 5 do CLAUDE.md. labels/README.md não diz mais que o som pode confirmar a marcação.
- O protocolo define o número de rotuladores, a identificação por código de papel, a métrica de concordância para a contagem de rostos >= 64 px por quadro e para os eventos, o tamanho da amostra, o limite de aceitação, o que acontece abaixo dele e a revisão por amostragem (fração e quem revisa).
- O protocolo define o método de comparação sem pareamento entre altura manual e altura da caixa do detector, a tolerância, a correção aplicada aos rótulos antes de F4.6 se a tolerância for ultrapassada, e registra que o método é aproximação porque os rótulos não têm caixa por rosto.
- O protocolo define o erro máximo, em pixels, da medida feita pela ferramenta de F3.3 sobre um retângulo sintético de altura conhecida.
- O protocolo não contém nome, e-mail nem conta de rotulador.
- Caminho de erro: se a revisão da QA reprovar um critério, o protocolo volta ao autor da seção com o item apontado, e a aprovação de Fabio só é registrada depois de todos os critérios passarem.
- Fabio Pinheiro aprova o protocolo, com a data registrada no próprio documento.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F3.2.T1 | Visão Computacional | Redigir a regra de medida de altura_px, o método de comparação com a caixa do detector e o erro máximo da ferramenta | 6 | — |
| F3.2.T2 | Data Science | Definir eventos, quadros revisados, rotuladores, concordância e revisão no protocolo | 6 | F1.3 |
| F3.2.T3 | Governança e Privacidade | Registrar no protocolo o som desligado e corrigir labels/README.md:15 | 2 | — |
| F3.2.T4 | QA | Revisar o protocolo contra os critérios de aceite | 2 | F3.2.T1, F3.2.T2, F3.2.T3 |

<details><summary>F3.2.T1 · [Visão Computacional] Redigir a regra de medida de altura_px, o método de comparação com a caixa do detector e o erro máximo da ferramenta</summary>

**Objetivo:** Ter no protocolo uma regra de medida que busque a mesma grandeza da caixa do SCRFD, um método para comparar as duas alturas sem pareamento e o erro máximo aceito na medida da ferramenta.

**Passos previstos:**
1. Descrever a grandeza que o bench compara: altura da caixa do SCRFD, y2 - y1 (reacao/detect.py:32-33), no quadro na resolução nativa.
2. Fixar os dois pontos de clique com base na convenção de caixa do WIDER FACE (testa, queixo e bochechas).
3. Definir o tratamento de rosto de perfil, parcialmente oculto, de cabeça baixa e cortado na borda do quadro.
4. Fixar o menor rosto a marcar, com margem abaixo de 64 px para o erro de medida.
5. Definir o método de comparação sem pareamento entre alturas manuais e caixas do detector nos clipes de desenvolvimento (por exemplo, razão entre medianas ou entre quantis das alturas por quadro), a tolerância e a correção dos rótulos antes de F4.6, e registrar que é aproximação.
6. Fixar o erro máximo, em pixels, da medida da ferramenta de F3.3 sobre um retângulo sintético de altura conhecida.
7. Ilustrar com esquemas desenhados, sem quadro da PIB.

**Definição de pronto:** Seções de medida, comparação e erro máximo no protocolo, com os valores numéricos preenchidos, revisadas por Data Science.

**Dependências:** nenhuma

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F3.2.T2 · [Data Science] Definir eventos, quadros revisados, rotuladores, concordância e revisão no protocolo</summary>

**Objetivo:** Ter no protocolo as definições de evento, a regra de quadro revisado e as regras de rotuladores, concordância e revisão, com valores preenchidos.

**Passos previstos:**
1. Escrever as definições operacionais de riso, neutro, aplauso, pe e cabeca_baixa, com o critério de início e fim.
2. Exigir pelo menos um segundo inteiro amostrado por intervalo (bench.py:73-81) e registrar os mínimos do corpus: 1 riso e 4 neutros no validador e o mínimo de risos de F1.3.
3. Definir a lista de t_s revisados por clipe e quando um t_s entra nela, inclusive sem rosto a marcar.
4. Definir o número de rotuladores e a identificação por código de papel.
5. Escolher e justificar a métrica de concordância para a contagem de rostos >= 64 px por quadro e para os eventos, o tamanho da amostra nos clipes de desenvolvimento e o limite de aceitação.
6. Definir a revisão por amostragem (fração revisada e por quem) e o procedimento abaixo do limite.
7. Registrar se quem calibra em F4.5 pode rotular os clipes de teste, e a regra de os rotuladores não verem a saída do detector.

**Definição de pronto:** Seções de eventos, quadros revisados, rotuladores, concordância e revisão no protocolo, com valores preenchidos, revisadas por Visão Computacional.

**Dependências:** F1.3

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F3.2.T3 · [Governança e Privacidade] Registrar no protocolo o som desligado e corrigir labels/README.md:15</summary>

**Objetivo:** Deixar escrito no protocolo e no README de rótulos que o som não é tocado na rotulagem, com a regra 5 como motivo.

**Passos previstos:**
1. Escrever a seção de som do protocolo citando a regra 5 do CLAUDE.md (CLAUDE.md:9,20) e samples/corpus/pib/README.md:8.
2. Trocar labels/README.md:15 por texto que diga que o som não é usado na rotulagem.
3. Conferir que o protocolo não tem nome, e-mail nem conta de rotulador.
4. Abrir PR citando o PBI.

**Definição de pronto:** PR mesclado com a seção de som no protocolo e labels/README.md:15 sem a frase 'o som do próprio vídeo pode confirmar a marcação'.

**Dependências:** nenhuma

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F3.2.T4 · [QA] Revisar o protocolo contra os critérios de aceite</summary>

**Objetivo:** Confirmar por revisão que o protocolo atende aos 10 critérios antes da aprovação de Fabio Pinheiro.

**Passos previstos:**
1. Conferir cada critério contra o texto do protocolo e de labels/README.md:15.
2. Buscar no protocolo nomes, e-mails e contas.
3. Devolver ao autor da seção cada critério reprovado, com o item apontado, e revisar de novo.
4. Conferir que a aprovação de Fabio Pinheiro está datada no documento depois da última revisão.

**Definição de pronto:** Checklist dos 10 critérios anexado ao PBI e aprovação de Fabio Pinheiro registrada no protocolo.

**Dependências:** F3.2.T1, F3.2.T2, F3.2.T3

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- labels/README.md:6-17,19-20
- bench.py:73-81,123-128
- reacao/types.py:5
- reacao/detect.py:32-33
- tools/validar_labels.py:17-21,92-95,215-220
- docs/poc-gate.md:20-21
- samples/corpus/pib/README.md:8 (não versionado)
- CLAUDE.md:9,20 (regras que nunca mudam; regra 5) e regras 2 e 3
- https://arxiv.org/abs/2105.04714 (SCRFD, experimentos no WIDER FACE)
- https://openaccess.thecvf.com/content_cvpr_2016/papers/Yang_WIDER_FACE_A_CVPR_2016_paper.pdf (caixas com testa, queixo e bochechas)
- API do GitHub: repositório com visibility public

#### Verificação INVEST: pontos que falharam
- Valiosa: PBI documental. O efeito do protocolo aparece em F3.3 e F3.4.

#### Premissas
- PBI documental: entrega o protocolo. A verificação é revisão pela QA contra os critérios, com aprovação final de Fabio Pinheiro. A edição de labels/README.md:15 é texto e entra na mesma revisão.
- O protocolo é um arquivo versionado no repositório. Caminho proposto: labels/PROTOCOLO.md.
- Que a caixa prevista pelo SCRFD segue a convenção do WIDER FACE é dedução: o artigo do SCRFD relata experimentos no WIDER FACE e não descreve a convenção da caixa.
- A medição da concordância saiu deste PBI e foi para F3.4 (ver alterações em relação à árvore).
- A razão entre altura manual e altura da caixa do detector é medida em F4.4, que já roda a detecção nos clipes de desenvolvimento. Este PBI fixa o método sem pareamento, a tolerância e a correção. O método sem pareamento é aproximação, porque _faces.csv não tem posição (labels/README.md:6).
- A lista de quadros revisados é proposta deste detalhamento, para distinguir quadro rotulado sem rosto de quadro não rotulado.
- Identificação dos rotuladores por código de papel: extensão da P12 aos rotuladores, porque o repositório é público.
- A regra 'rotuladores não veem a saída do detector' é proposta deste detalhamento, para não enviesar os rótulos.
- F3.1, o encarregado e F3.5 saíram das dependências: o som ficou desligado pela regra 5, sem decisão do encarregado, e a unificação do local dos rótulos foi para F3.5.
- Disciplinas mantidas da árvore: Data Science, Visão Computacional, Governança e Privacidade e QA.
- Estimativas (3 pontos e horas das tasks) são sugestão.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Link com a Feature F3 como pai
- Effort ou Story Points: 3 como sugestão
- Acrescentar a F4.4 a medição da razão entre altura manual e altura da caixa do detector pelo método sem pareamento deste protocolo, nos clipes de desenvolvimento, antes do bench de F4.6
- Se Fabio quiser usar o som na rotulagem, isso é pendência de mudança do CLAUDE.md decidida pelo dono do repositório, fora deste PBI
- Tags: fase-0; gate-poc; rotulagem; protocolo

## Preview — PBI F3.3 (novo) · Disponibilizar em Space do Hugging Face com acesso restrito à lista de rotuladores a ferramenta de rotulagem que mede a altura do rosto em pixels sem gravar quadro

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Disponibilizar em Space do Hugging Face com acesso restrito à lista de rotuladores a ferramenta de rotulagem que mede a altura do rosto em pixels sem gravar quadro |
| Tipo | Product Backlog Item |
| Pai | F3 |
| Tags | fase-0; rotulagem; hf-space; regra-1 |
| Estimativa | 8 pts (sugestão); tasks: 44 h |
| Dependências | F1.1 (guarda corrigida), F1.4 (validador com regras por arquivo separadas dos mínimos do corpus e recusa de intervalo sem segundo inteiro amostrado), F2.4 (namespace, SDK e modelo de acesso do Space), F2.6 (práticas de token fine-grained), F3.1 (lista de acesso), só para F3.3.T6 e para o teste de aceite, F3.2 (regra de medida, erro máximo, tipos de evento e quadros revisados), F3.5 (leitura por tag), Assinatura PRO ativa (conta pessoal) ou plano Team ou Enterprise (organização), conforme o ADR de F2.4 |
| Substitui | nenhum |

#### Descrição

Como rotulador da lista de acesso de F3.1  
Quero abrir no navegador os quadros amostrados de cada clipe na resolução nativa, marcar a altura de cada rosto com cliques, marcar os quadros revisados e os intervalos de evento e exportar os arquivos no formato do bench  
Para rotular o corpus sem baixar o vídeo, sem abrir o clipe em outro programa e sem deixar quadro gravado em disco

**Contexto:** labels/README.md:19-20 estima 3 a 4 h de rotulagem 'com ferramenta de clique', e essa ferramenta não existe no repositório. Pela P3 revisada, ferramentas que exibem vídeo ou quadro ficam no Hugging Face, e a de rotulagem continua em Space privado. O painel web na Vercel não recebe vídeo nem quadro. Os SDKs de Space são gradio, docker e static (https://huggingface.co/docs/hub/spaces-config-reference). Space Gradio ou Docker exige plano pago para ser criado: PRO em conta pessoal, Team ou Enterprise em organização (https://huggingface.co/docs/hub/spaces-overview). A assinatura PRO de ds-fabiopinheiro tem periodEnd 2026-10-01 (whoami do HF, 2026-09-23). Na visibilidade private, código e app ficam só para dono e colaboradores. Na protected, o código fica privado, mas o app fica acessível pela URL de incorporação .hf.space (https://huggingface.co/docs/hub/spaces-overview#space-visibility). Um repositório de conta pessoal não aceita outras pessoas, e dar acesso passa por organização (https://huggingface.co/docs/hub/repositories-settings). O login OAuth restringe o acesso a membros de organizações com hf_oauth_authorized_org, não a uma lista de contas (https://huggingface.co/docs/hub/spaces-oauth). A escolha entre Space private de organização e Space protected de conta pessoal é do ADR de F2.4. Conta de serviço existe só em organização Enterprise (https://huggingface.co/docs/hub/enterprise-service-accounts), então o Space usa token fine-grained da conta dona. O hardware CPU Basic tem 2 vCPU, 16 GB e disco não persistente, sem custo por hora, e os logs saem por SSE (https://huggingface.co/docs/hub/spaces-overview#hardware-resources; https://huggingface.co/docs/hub/spaces-gpus). Variables de Space são públicas e secrets são privados (https://huggingface.co/docs/hub/spaces-overview#managing-secrets). Se o SDK for Gradio, imagens devolvidas como array ou PIL são salvas em arquivo para o navegador, e qualquer arquivo do cache fica disponível por URL a todos os usuários do app. O local do cache é definido por GRADIO_TEMP_DIR, e delete_cache limpa o cache (https://gradio.app/docs/gradio/image; https://gradio.app/guides/file-access; https://gradio.app/guides/environment-variables; https://gradio.app/guides/resource-cleanup). O cache do huggingface_hub fica em ~/.cache/huggingface/hub, salvo com HF_HUB_CACHE ou local_dir (https://huggingface.co/docs/hub/local-cache#cache-location). A guarda intercepta cv2.imwrite e PIL.Image.save fora de /dev/shm (reacao/guard.py:19-41). Ao sair do contexto, ela acusa só arquivos de imagem ou vídeo novos em relação ao início, nas raízes passadas, que por padrão são o cwd e /tmp (reacao/guard.py:44-53,56-81). A lista de extensões não tem áudio (reacao/guard.py:8), e a comparação com /dev/shm não usa separador (reacao/guard.py:15-16), falha que F1.1 corrige junto com o '[guard] ok' impresso em execução com falha. A grade de quadros vem de reacao.ingest.frames a 1 quadro/s (reacao/ingest.py:8-23,34-42). O validador tem regras por arquivo (tools/validar_labels.py:58-133) e mínimos do corpus aplicados à pasta inteira (tools/validar_labels.py:215-220), e sai com código 1 se houver qualquer erro (tools/validar_labels.py:229). Hoje ele não recusa intervalo sem segundo inteiro amostrado, regra que F1.4 acrescenta. O vídeo sintético de teste não tem rosto (tests/fixtures/README.md:11). O cabeçalho Cache-Control: no-store pede que nenhum cache, inclusive o do navegador, guarde a resposta (https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control).

**Regras de negócio:**
- RN01 – O Space fica no Hugging Face (P3 revisada), no namespace e com a visibilidade do ADR de F2.4. A opção que atende ao 'Space privado' da P3 revisada é um Space private numa organização, que exige plano Team ou Enterprise para Gradio ou Docker. Na opção protected de conta pessoal, o app fica acessível pela URL .hf.space e precisa da confirmação de Fabio. Em qualquer opção, o app confere em todas as rotas, inclusive as de arquivo do SDK, se a conta OAuth está na lista de F3.1.
- RN02 – O clipe é lido da revisão marcada com tag (F3.5) para /dev/shm e decodificado em memória. Nenhum arquivo de imagem, vídeo ou áudio é gravado fora de /dev/shm, inclusive o cache temporário do SDK e o do huggingface_hub.
- RN03 – A ferramenta mostra só os quadros dos segundos amostrados pela grade de reacao/ingest.py, na resolução nativa, e não oferece download do vídeo nem do quadro.
- RN04 – A altura exportada está em pixels do quadro nativo, com qualquer zoom de tela, dentro do erro máximo fixado no protocolo de F3.2.
- RN05 – A ferramenta não roda o detector nem mostra saída do pipeline.
- RN06 – A ferramenta não toca som, e nenhuma resposta leva a trilha de áudio (CLAUDE.md regra 5; protocolo de F3.2).
- RN07 – A exportação de um clipe gera <video>_faces.csv, <video>_eventos.csv e a lista de quadros revisados, com os nomes e cabeçalhos que o bench espera (labels/README.md:6-11,22-23). Ela só acontece com zero erro nas regras por arquivo do validador de F1.4. Os mínimos do corpus não bloqueiam a exportação de um clipe e são conferidos na validação de pasta.
- RN08 – Os arquivos exportados não contêm imagem, id de rosto, posição do clique nem nome de pessoa.
- RN09 – As respostas que levam imagem trazem Cache-Control: no-store.
- RN10 – O arquivo do clipe em /dev/shm é apagado ao trocar de clipe, ao fim da sessão e em erro.
- RN11 – Ao fim de cada sessão e no tratamento de erro, o app roda uma varredura absoluta, sem comparação com estado anterior, sobre as raízes fixadas (cwd do app, $HOME/.cache, inclusive ~/.cache/huggingface/hub, /tmp, o diretório de temporários do SDK e /dev/shm). A varredura procura extensões de imagem, vídeo e áudio e grava o resultado no log do Space.

**Fora de escopo:**
- A rotulagem em si (F3.4)
- Caixas por rosto e recall pareado por IoU
- Rótulos de momentos (F5.1)
- Painel web na Vercel e qualquer tela do produto
- Gravação dos rótulos direto no dataset pelo Space. A publicação com tag é de F3.4.
- Guarda do progresso no servidor. O rotulador exporta e importa o CSV parcial.
- Arquivo parcial com coordenadas de clique
- Detector no Space ou exibição de detecções
- Som na rotulagem (regra 5)
- Correção de reacao/guard.py (F1.1)

#### Critérios de aceite

- Um rotulador da lista de F3.1 entra no Space com a própria conta do Hugging Face, escolhe um clipe da revisão marcada e vê só os quadros dos segundos amostrados, na resolução nativa.
- Uma conta fora da lista, um visitante sem login e um pedido direto à URL de um quadro ou de um arquivo do cache do SDK, feito sem sessão de conta da lista, recebem acesso negado e não veem lista de clipes nem quadro. Se o ADR de F2.4 usar organização, um membro da organização que não está na lista também recebe acesso negado.
- Numa imagem sintética com um retângulo de altura conhecida, com o zoom do navegador diferente de 100%, a altura exportada difere da altura do retângulo em no máximo o erro fixado no protocolo de F3.2.
- O rotulador marca rostos, quadros revisados e intervalos de um clipe inteiro e exporta os arquivos, e as regras por arquivo do validador de F1.4 não apontam erro sobre eles com o vídeo correspondente. Os mínimos do corpus ficam fora desta condição.
- Um CSV parcial exportado e importado de novo restaura as alturas por t_s e a lista de quadros revisados do clipe, e a interface mostra quais t_s faltam revisar. A posição dos cliques não é restaurada, porque não é exportada.
- A validação de uma pasta inteira contra os clipes da tag mostra os erros por arquivo e a contagem de risos e de trechos neutros contra os mínimos do corpus.
- Caminho de erro: um intervalo sem segundo inteiro amostrado, um tipo de evento fora da lista ou um t_s fora da grade impede a exportação, e a interface mostra a mensagem do validador de F1.4.
- O log do Space mostra a varredura absoluta ao fim de uma sessão de rotulagem e depois de um erro forçado no app, sem reinício do container, sem arquivo de imagem, vídeo ou áudio fora de /dev/shm nas raízes fixadas e sem o clipe em /dev/shm.
- As respostas HTTP que levam quadro trazem o cabeçalho Cache-Control: no-store.
- A interface não tem controle de áudio, e nenhuma resposta HTTP leva a trilha de áudio.
- A interface não oferece download do vídeo nem do quadro.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F3.3.T1 | DevOps | Criar o Space com o acesso do ADR de F2.4, a verificação de conta em todas as rotas e os temporários em /dev/shm | 8 | F2.4, F2.6, F3.5.T3 |
| F3.3.T2 | Visão Computacional | Implementar a leitura em memória dos quadros amostrados, a conversão do clique para pixel nativo e a varredura absoluta | 10 | F1.1, F3.5.T4, F3.2.T1 |
| F3.3.T3 | Front end | Construir a marcação de rostos e de quadros revisados e a exportação de _faces.csv | 10 | F3.3.T2, F3.2.T1, F3.2.T2, F1.4 |
| F3.3.T4 | Front end | Construir a marcação de eventos e a validação de pasta | 6 | F3.3.T3, F3.2.T2, F1.4 |
| F3.3.T5 | Governança e Privacidade | Verificar a ferramenta contra as regras 1, 2 e 5 e registrar os riscos residuais no dataset card | 3 | F3.3.T3, F3.3.T4 |
| F3.3.T6 | DevOps | Aplicar ao Space a lista de acesso de F3.1 | 1 | F3.3.T1, F3.1.T6 |
| F3.3.T7 | QA | Executar os testes de aceite da ferramenta no Space | 6 | F3.3.T5, F3.3.T6 |

<details><summary>F3.3.T1 · [DevOps] Criar o Space com o acesso do ADR de F2.4, a verificação de conta em todas as rotas e os temporários em /dev/shm</summary>

**Objetivo:** Ter o Space no ar, com acesso só para contas permitidas em todas as rotas, token somente leitura e temporários apontando para /dev/shm.

**Passos previstos:**
1. Criar o Space, pela conta dona ou por membro com escrita na organização, no namespace, com o SDK e a visibilidade do ADR de F2.4, em cpu-basic.
2. Ativar o login OAuth (hf_oauth) e guardar a lista de contas permitidas como secret, começando só com a conta dona e a conta de teste.
3. Criar, pela conta dona, um token fine-grained somente leitura do dataset, seguindo as práticas de F2.6, e guardá-lo como secret.
4. Definir HF_HUB_CACHE e, se o SDK for Gradio, GRADIO_TEMP_DIR dentro de /dev/shm. Não anexar bucket nem volume de escrita.
5. Publicar um app mínimo que confere a conta OAuth em todas as rotas, inclusive as de arquivo do SDK, e nega acesso fora da lista.
6. Testar com conta fora da lista, visitante sem login e pedido direto à URL de um arquivo do cache.
7. Medir e registrar o tamanho de /dev/shm no container.
8. Registrar no dataset card a URL do Space, o SDK, o modelo de acesso, o nome do token e o tamanho de /dev/shm.

**Definição de pronto:** App mínimo no ar, os três testes de acesso negado registrados, secrets e variáveis configurados e registro feito no card.

**Dependências:** F2.4, F2.6, F3.5.T3

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F3.3.T2 · [Visão Computacional] Implementar a leitura em memória dos quadros amostrados, a conversão do clique para pixel nativo e a varredura absoluta</summary>

**Objetivo:** Entregar à interface os quadros da grade do bench, em memória e na resolução nativa, converter cliques em pixels do quadro nativo e registrar no log a varredura absoluta ao fim da sessão e no erro.

**Passos previstos:**
1. Baixar o clipe por tag com hf_hub_download, passando revision e local_dir em /dev/shm.
2. Gerar os quadros com reacao.ingest.frames a 1 quadro/s, a mesma grade do bench.
3. Manter em memória só o clipe aberto e apagar o arquivo de /dev/shm ao trocar de clipe, ao fim da sessão e em exceção.
4. Ativar no processo do app as interceptações de reacao/guard.py, na versão corrigida por F1.1.
5. Implementar a varredura absoluta sobre as raízes fixadas (cwd do app, $HOME/.cache, /tmp, diretório de temporários do SDK e /dev/shm), com extensões de imagem, vídeo e áudio, sem comparar com estado anterior.
6. Chamar a varredura ao fim de cada sessão e no tratamento de erro, sem reiniciar o container, e gravar o resultado no log do Space.
7. Converter as coordenadas de clique para pixels do quadro nativo, com qualquer escala de exibição.
8. Escrever testes com vídeo sintético gerado em /dev/shm por tests/fixtures/gerar_curto.py, com imagem sintética de altura conhecida e com arquivos de imagem, vídeo e áudio plantados em /tmp.

**Definição de pronto:** Testes passando no CI: altura conhecida dentro do erro máximo de F3.2, varredura que acusa os arquivos plantados e passa em estado limpo, e nenhum arquivo de imagem ou vídeo fora de /dev/shm ao fim dos testes.

**Dependências:** F1.1, F3.5.T4, F3.2.T1

**Estimativa sugerida:** 10 h (sugestão; validar com o time)

</details>

<details><summary>F3.3.T3 · [Front end] Construir a marcação de rostos e de quadros revisados e a exportação de _faces.csv</summary>

**Objetivo:** Permitir marcar a altura de cada rosto em todos os quadros amostrados de um clipe, registrar os quadros revisados e exportar os arquivos sem erro de arquivo.

**Passos previstos:**
1. Listar os clipes da tag separados em teste e desenvolvimento, sem o concatenado.
2. Permitir a navegação pelos t_s da grade e marcar cada t_s como revisado quando o rotulador o conclui, inclusive sem rosto a marcar.
3. Marcar cada rosto com dois cliques, nos pontos do protocolo, com lista editável e desfazer.
4. Exportar <video>_faces.csv com o nome e o cabeçalho do bench e a lista de t_s revisados.
5. Importar o CSV parcial e a lista de t_s revisados, restaurar as alturas por t_s e mostrar quais t_s faltam revisar.
6. Aplicar as regras por arquivo do validador de F1.4 antes de oferecer os arquivos.
7. Enviar Cache-Control: no-store nas respostas de imagem e não oferecer download de quadro ou vídeo.

**Definição de pronto:** Fluxo completo sobre o vídeo sintético, com marcações de teste que incluem ao menos uma altura >= 64 px: marcação, exportação, importação e regras por arquivo do validador sem erro; cabeçalho no-store visível nas respostas de imagem.

**Dependências:** F3.3.T2, F3.2.T1, F3.2.T2, F1.4

**Estimativa sugerida:** 10 h (sugestão; validar com o time)

</details>

<details><summary>F3.3.T4 · [Front end] Construir a marcação de eventos e a validação de pasta</summary>

**Objetivo:** Permitir marcar e exportar os intervalos de evento e validar uma pasta inteira, usando só as regras do validador de F1.4.

**Passos previstos:**
1. Marcar intervalos com os tipos riso, aplauso, pe, cabeca_baixa e neutro.
2. Exportar e importar <video>_eventos.csv.
3. Impedir a exportação quando as regras por arquivo do validador de F1.4 apontarem erro (intervalo sem segundo inteiro amostrado, tipo inválido, t_s fora da grade) e mostrar a mensagem do validador, sem regra própria.
4. Validar uma pasta inteira contra os clipes da tag, mostrando os erros por arquivo e a contagem de risos e de neutros contra os mínimos do corpus.
5. Não incluir controle de áudio e servir só imagens, sem a trilha de áudio.

**Definição de pronto:** Fluxo de eventos e validação de pasta funcionando sobre o vídeo sintético, interface sem controle de áudio e nenhuma resposta com trilha de áudio na aba de rede do navegador.

**Dependências:** F3.3.T3, F3.2.T2, F1.4

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F3.3.T5 · [Governança e Privacidade] Verificar a ferramenta contra as regras 1, 2 e 5 e registrar os riscos residuais no dataset card</summary>

**Objetivo:** Confirmar que a ferramenta cumpre as regras de não persistência, não identificação e ausência de som, e registrar o que ela não controla.

**Passos previstos:**
1. Conferir que não há download de vídeo ou quadro, que o detector não roda e que não há som.
2. Conferir que os arquivos exportados não têm coluna além das do bench e da lista de t_s revisados, nem posição de clique.
3. Conferir que os logs do Space não imprimem conteúdo de CSV nem contas de rotuladores, e que a lista de contas está como secret.
4. Registrar na seção de acesso do card os riscos que a ferramenta não controla (por exemplo, captura de tela no computador do rotulador) e a orientação dada aos rotuladores.

**Definição de pronto:** Checklist assinado pela governança e riscos residuais registrados no card.

**Dependências:** F3.3.T3, F3.3.T4

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F3.3.T6 · [DevOps] Aplicar ao Space a lista de acesso de F3.1</summary>

**Objetivo:** Trocar a lista provisória do Space pela lista de acesso registrada no card depois do parecer.

**Passos previstos:**
1. Atualizar, pela conta dona, o secret com as contas da lista de F3.1 e, se houver organização, conferir os membros.
2. Retirar do secret a conta de teste, mantendo-a fora da lista para o critério 2.
3. Registrar no card a data da aplicação.

**Definição de pronto:** Secret com a lista de F3.1, data registrada no card e um rotulador da lista com acesso confirmado.

**Dependências:** F3.3.T1, F3.1.T6

**Estimativa sugerida:** 1 h (sugestão; validar com o time)

</details>

<details><summary>F3.3.T7 · [QA] Executar os testes de aceite da ferramenta no Space</summary>

**Objetivo:** Registrar passou ou não passou para os 11 critérios de aceite no Space publicado.

**Passos previstos:**
1. Entrar com uma conta da lista, com a conta de teste fora da lista, sem login e, se houver organização, com um membro fora da lista.
2. Pedir diretamente a URL de um quadro e de um arquivo do cache do SDK sem sessão de conta da lista.
3. Medir o retângulo de altura conhecida com o zoom do navegador diferente de 100%.
4. Rotular um clipe da tag, exportar e conferir as regras por arquivo do validador.
5. Exportar, importar e comparar um CSV parcial, e validar uma pasta sem riso.
6. Provocar intervalo sem segundo inteiro, tipo inválido e t_s fora da grade.
7. Forçar um erro no app, sem reiniciar o container, e ler no log do Space a varredura ao fim da sessão e depois do erro.
8. Conferir o cabeçalho Cache-Control nas respostas de imagem e a ausência de controle de áudio, de trilha de áudio e de download.

**Definição de pronto:** Relatório com passou ou não passou para os 11 critérios anexado ao PBI.

**Dependências:** F3.3.T5, F3.3.T6

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- labels/README.md:6-11,19-20,22-23
- reacao/guard.py:8,15-16,19-41,44-53,56-81
- reacao/ingest.py:8-23,34-42
- tools/validar_labels.py:17-21,58-133,172-229
- tests/fixtures/README.md:11 e tests/fixtures/gerar_curto.py (vídeo sintético sem rosto)
- CLAUDE.md (regras 1, 2 e 5)
- P3 revisada e P9 (premissas)
- arvore_v1.json: F1.1 (falhas da guarda) e F1.4 (intervalo sem segundo inteiro amostrado)
- https://huggingface.co/docs/hub/spaces-overview (plano pago por SDK, visibilidade, hardware, secrets)
- https://huggingface.co/docs/hub/spaces-config-reference
- https://huggingface.co/docs/hub/spaces-gpus
- https://huggingface.co/docs/hub/repositories-settings
- https://huggingface.co/docs/hub/spaces-oauth
- https://huggingface.co/docs/hub/enterprise-service-accounts
- https://huggingface.co/docs/hub/local-cache#cache-location
- https://gradio.app/docs/gradio/image
- https://gradio.app/guides/file-access
- https://gradio.app/guides/environment-variables
- https://gradio.app/guides/resource-cleanup
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Cache-Control
- whoami do HF em 2026-09-23 (PRO, periodEnd 2026-10-01)

#### Verificação INVEST: pontos que falharam
- Independente: depende de F1.1, F1.4, F2.4, F2.6, F3.1, F3.2 e F3.5. A construção (T1 a T5) não espera o parecer de F3.1, só a aplicação da lista (T6) e o teste de aceite.
- Small: 8 pontos. Se o SDK escolhido em F2.4 for Docker, o esforço de interface pode crescer.

#### Premissas
- F2.4 continua a decidir namespace, SDK e acesso do Space de rotulagem. Pela P3 revisada, Filipe e a equipe de mídia usam o painel web na Vercel, e esse Space atende só rotuladores e Fabio.
- O título troca 'Space privado' por 'Space do Hugging Face com acesso restrito à lista de rotuladores', para cobrir as duas opções do ADR de F2.4 (ver premissas da Feature). A verificação da conta em todas as rotas, nas duas opções, é proposta deste detalhamento: na opção private de organização, todo membro da organização com leitura veria o Space.
- A lista de contas permitidas fica como secret do Space, porque variables de Space são públicas.
- A exportação é por download dos arquivos, sem gravação direta no dataset pelo Space. Os arquivos não têm imagem nem dado pessoal, a publicação com tag fica em F3.4, e o Space não precisa de token de escrita.
- A validação de pasta inteira no Space foi acrescentada para validar com os vídeos à mão, sem job pago e sem cópia local.
- O Space usa o validador de F1.4, importado do pacote numa revisão fixa, sem regra paralela.
- Os requisitos de cache do Gradio valem só se o ADR escolher Gradio. Para outro SDK, a task de DevOps aplica a regra equivalente.
- A varredura absoluta não inclui os diretórios de pacotes instalados, que podem trazer arquivos de imagem próprios. A lista final de raízes é registrada em T2. É dedução, a conferir na implementação.
- Sem arquivo parcial de coordenadas: a posição do clique não é gravada, por minimização. O bench não usa a posição (bench.py:123-128).
- O tamanho de /dev/shm no container do Space não está documentado e é medido na task de DevOps. Cada clipe tem alguns MB, e o dataset inteiro tem 299.851.242 bytes.
- O teste de aceite com clipe real usa um clipe de desenvolvimento se F3.1 permitir. Se não permitir, usa vídeo público de F3.6 ou sintético.
- Disciplinas mantidas da árvore: Front end, Visão Computacional, Governança e Privacidade, DevOps e QA.
- Estimativas (8 pontos e horas das tasks) são sugestão.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Link com a Feature F3 como pai
- Effort ou Story Points: 8 como sugestão
- URL do Space depois de criado, para o dataset card
- Conta de teste fora da lista para o critério 2
- Custo do plano Team ou Enterprise, se o ADR de F2.4 escolher organização; confirmação de Fabio, se escolher protected
- Pendência com F2.6: registrar o token de leitura do Space como uso previsto
- Tags: fase-0; rotulagem; hf-space; regra-1

## Preview — PBI F3.4 (novo) · Medir a concordância, rotular os clipes de teste e os clipes de desenvolvimento 07 a 10 e publicar os rótulos com tag

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Medir a concordância, rotular os clipes de teste e os clipes de desenvolvimento 07 a 10 e publicar os rótulos com tag |
| Tipo | Product Backlog Item |
| Pai | F3 |
| Tags | fase-0; gate-poc; rotulagem; criterio-1; criterio-2 |
| Estimativa | 8 pts (sugestão); tasks: 36 h |
| Dependências | F1.3 (mínimo de risos e decisão sobre o clipe 11), F1.4 (validador atualizado), F3.1 (parecer que permite o uso da PIB), F3.2 (protocolo), F3.3 (ferramenta), F3.5 (pastas e padrão de tags), Rotuladores disponíveis |
| Substitui | nenhum |

#### Descrição

Como time de Data Science e Visão Computacional que roda o bench do gate  
Quero os rótulos de rostos, quadros revisados e eventos dos clipes de teste e dos clipes 07 a 10, com concordância medida, validados e publicados com tag no dataset privado  
Para calibrar em F4.4 e F4.5 só com os clipes de desenvolvimento e medir os critérios 1 e 2 em F4.6 sobre uma revisão fixa

**Contexto:** O conjunto de teste são os 19 clipes que não foram usados no desenvolvimento, com 195 dos 248 quadros amostrados. Os clipes 07 a 10 são de desenvolvimento e ficam fora da linha TOTAL (docs/poc-gate.md:46-48). Os 53 quadros de desenvolvimento são valor derivado de samples/corpus/pib/ffprobe.csv com a regra de reacao/ingest.py:34-42. F1.3 decide se o clipe 11, que já passou pelo pipeline numa execução local, continua no teste (P28). O igreja_simples_concat.mp4 contém os 23 clipes, inclusive os de desenvolvimento (samples/corpus/pib/README.md:12). Sem rótulos, o bench termina com 'nenhum vídeo rotulado — nada medido' e código 1 (bench.py:237-239). O código 2 é de tools/rodar_teste.sh:51. O repositório estima cerca de 250 quadros, 20 a 40 rostos por quadro e 3 a 4 h com ferramenta de clique (labels/README.md:19-20), sem medição. Um quadro sem rosto visível não tem linha em _faces.csv (labels/README.md:6-8), por isso a cobertura é contada pela lista de quadros revisados definida em F3.2. O validador aplica à pasta inteira os mínimos de 1 riso e 4 neutros (tools/validar_labels.py:215-220), e F1.4 acrescenta o mínimo de risos de F1.3. A pasta de desenvolvimento tem 4 clipes, com tipicamente 1 a 3 intervalos por clipe (labels/README.md:12), e P8 prevê que ela pode não ter eventos suficientes. Com menos de 4 trechos neutros, o jitter do 2b não é calculado (bench.py:54). Na execução local do concatenado, pct_sorrindo ficou entre 0,0% e 2,4% nas 8 janelas (out/window_aggregate.json, local, não versionado). F4.4 e F4.5 usam só os rótulos de desenvolvimento (P8), e os limiares não podem ser calibrados com os de teste (docs/poc-gate.md:38-40,46-48). A concordância, que a árvore punha em F3.2, é medida aqui como primeiro passo, com a ferramenta de F3.3. Se F3.1 vetar a PIB, este PBI é cancelado, e F3.6 e F3.7 fornecem os conjuntos públicos (P13 ajustada).

**Regras de negócio:**
- RN01 – A concordância é medida primeiro, numa amostra dos clipes de desenvolvimento definida em F3.2. Os clipes de teste só começam depois de a concordância atingir o limite do protocolo.
- RN02 – Os rótulos de teste e de desenvolvimento ficam em pastas separadas. O concatenado não é rotulado, e o clipe 11 segue a decisão de F1.3.
- RN03 – Todo t_s da grade de cada clipe rotulado consta na lista de quadros revisados, e os rostos visíveis desses quadros têm linhas em _faces.csv (labels/README.md:6-8).
- RN04 – A revisão por amostragem segue o protocolo de F3.2 e é feita por um rotulador diferente do que rotulou, antes da publicação.
- RN05 – A publicação só acontece quando o validador de F1.4 não aponta erro de arquivo em nenhuma pasta. Os mínimos do corpus (risos de F1.3 e 4 trechos neutros) são contados só na pasta de teste e não bloqueiam a publicação.
- RN06 – O registro de rotulagem traz, por pasta: clipes, t_s revisados, rostos marcados, rostos >= 64 px, eventos por tipo, rotuladores por código de papel, rodadas de concordância, commit e tag.
- RN07 – Se os risos do conjunto de teste ficarem abaixo do mínimo de F1.3, o registro diz isso, F3.6 é acionado, e os rótulos publicados continuam valendo para o critério 1. Se os neutros do teste ficarem abaixo de 4, o registro diz que o jitter do 2b fica sem cálculo (bench.py:54).
- RN08 – Nenhum bench, calibração ou job de medição roda sobre a pasta de teste antes de F4.6.
- RN09 – Cada task de rotulagem é de um rotulador, identificado por código de papel.

**Fora de escopo:**
- Bench dos critérios 1 e 2 (F4.6)
- Calibração de limiares (F4.5)
- Medição do pré-filtro e da razão entre altura manual e caixa do detector (F4.4)
- Rótulos de momentos (F5.1)
- Seleção e rótulos de clipes públicos (F3.6, F3.7)
- Caixas por rosto

#### Critérios de aceite

- O registro de rotulagem traz a métrica e o valor de concordância da amostra de desenvolvimento, e a rodada aprovada tem data anterior ao início da rotulagem de teste.
- Caminho de erro: com concordância abaixo do limite, o registro mostra a rodada reprovada e a revisão do protocolo, e a rotulagem de teste só começa depois de uma rodada aprovada.
- A revisão marcada com a tag de rótulos contém uma pasta de teste com _faces.csv, _eventos.csv e a lista de t_s revisados de cada clipe de teste definido em F1.3 e uma pasta de desenvolvimento com os mesmos arquivos dos clipes 07 a 10. Não há rótulo do igreja_simples_concat.
- O validador de F1.4 não aponta erro de arquivo em nenhuma pasta da revisão marcada, com os vídeos correspondentes.
- Todo t_s da grade de cada clipe consta na lista de t_s revisados: 195 no teste com os 19 clipes (docs/poc-gate.md:48) e 53 no desenvolvimento (valor derivado, a conferir na grade).
- O registro de rotulagem traz a contagem de eventos de riso e de trechos neutros do conjunto de teste, compara os risos com o mínimo pré-registrado em F1.3 e conclui 'suficiente' ou 'F3.6 acionado'. Com 'F3.6 acionado', a revisão marcada existe mesmo assim.
- Os arquivos de rótulo têm só t_s e altura_px em _faces.csv, só t_ini_s, t_fim_s e tipo em _eventos.csv e só t_s na lista de revisados.
- A lista de jobs do namespace não tem job de bench, calibração ou pipeline que leia a pasta de teste antes de F4.6.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F3.4.T1 | Visão Computacional | Marcar a amostra de concordância nos clipes de desenvolvimento (rotulador 1) | 2 | F3.2, F3.3 |
| F3.4.T2 | Visão Computacional | Marcar a amostra de concordância nos clipes de desenvolvimento (rotulador 2) | 2 | F3.2, F3.3 |
| F3.4.T3 | Data Science | Calcular e registrar a concordância da rodada | 3 | F3.4.T1, F3.4.T2 |
| F3.4.T4 | Visão Computacional | Rotular os rostos e os quadros revisados dos clipes de desenvolvimento 07 a 10 (rotulador 1) | 3 | F3.4.T3 |
| F3.4.T5 | Visão Computacional | Rotular os rostos e os quadros revisados dos clipes de teste (rotulador 1) | 10 | F3.4.T3, F1.3 |
| F3.4.T6 | Data Science | Rotular os eventos dos clipes de teste e de desenvolvimento e registrar as contagens (rotulador 1) | 5 | F3.4.T3, F1.3 |
| F3.4.T7 | Data Science | Revisar por amostragem os rótulos de rostos e de eventos (rotulador 2) | 4 | F3.4.T4, F3.4.T5, F3.4.T6 |
| F3.4.T8 | MLOps | Validar as pastas, publicar os rótulos com tag e registrar a revisão | 3 | F3.4.T7, F1.4, F3.5.T3 |
| F3.4.T9 | QA | Verificar os critérios de aceite sobre a revisão marcada | 4 | F3.4.T8 |

<details><summary>F3.4.T1 · [Visão Computacional] Marcar a amostra de concordância nos clipes de desenvolvimento (rotulador 1)</summary>

**Objetivo:** Entregar as marcações do rotulador 1 sobre a amostra de concordância definida no protocolo.

**Passos previstos:**
1. Abrir no Space os quadros da amostra dos clipes 07 a 10 definida no protocolo.
2. Marcar rostos, t_s revisados e eventos da amostra, sem ver as marcações do rotulador 2.
3. Exportar os arquivos sem erro de arquivo e entregá-los a quem conduz a rodada.

**Definição de pronto:** Arquivos da amostra do rotulador 1 exportados sem erro de arquivo e entregues.

**Dependências:** F3.2, F3.3

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F3.4.T2 · [Visão Computacional] Marcar a amostra de concordância nos clipes de desenvolvimento (rotulador 2)</summary>

**Objetivo:** Entregar as marcações do rotulador 2 sobre a mesma amostra de concordância.

**Passos previstos:**
1. Abrir no Space os quadros da mesma amostra.
2. Marcar rostos, t_s revisados e eventos da amostra, sem ver as marcações do rotulador 1.
3. Exportar os arquivos sem erro de arquivo e entregá-los a quem conduz a rodada.

**Definição de pronto:** Arquivos da amostra do rotulador 2 exportados sem erro de arquivo e entregues.

**Dependências:** F3.2, F3.3

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F3.4.T3 · [Data Science] Calcular e registrar a concordância da rodada</summary>

**Objetivo:** Ter uma rodada de concordância aprovada, pelo limite do protocolo, antes da rotulagem de teste.

**Passos previstos:**
1. Calcular a métrica do protocolo sobre os arquivos de T1 e T2.
2. Registrar rodada, data, valor e resultado no registro de rotulagem.
3. Abaixo do limite, revisar o protocolo com o responsável por F3.2 e pedir nova rodada aos rotuladores.

**Definição de pronto:** Registro com uma rodada aprovada, com data anterior ao início da rotulagem de teste.

**Dependências:** F3.4.T1, F3.4.T2

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F3.4.T4 · [Visão Computacional] Rotular os rostos e os quadros revisados dos clipes de desenvolvimento 07 a 10 (rotulador 1)</summary>

**Objetivo:** Ter _faces.csv e a lista de t_s revisados de todos os quadros amostrados dos 4 clipes de desenvolvimento.

**Passos previstos:**
1. Rotular no Space todos os quadros amostrados dos clipes 07 a 10.
2. Marcar cada t_s como revisado, inclusive sem rosto a marcar.
3. Exportar os arquivos e conferir na validação de pasta do Space que não há erro de arquivo.

**Definição de pronto:** Pasta de desenvolvimento com _faces.csv e lista de t_s revisados dos 4 clipes, sem erro de arquivo.

**Dependências:** F3.4.T3

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F3.4.T5 · [Visão Computacional] Rotular os rostos e os quadros revisados dos clipes de teste (rotulador 1)</summary>

**Objetivo:** Ter _faces.csv e a lista de t_s revisados de todos os quadros amostrados de cada clipe de teste.

**Passos previstos:**
1. Fixar a lista de clipes de teste conforme a decisão de F1.3 sobre o clipe 11.
2. Rotular no Space todos os quadros amostrados (195 com os 19 clipes), sem abrir o concatenado.
3. Marcar cada t_s como revisado, inclusive sem rosto a marcar.
4. Exportar os arquivos e conferir na validação de pasta do Space que não há erro de arquivo.

**Definição de pronto:** Pasta de teste com _faces.csv e lista de t_s revisados de cada clipe de teste, sem erro de arquivo e com todos os t_s da grade revisados.

**Dependências:** F3.4.T3, F1.3

**Estimativa sugerida:** 10 h (sugestão; validar com o time)

</details>

<details><summary>F3.4.T6 · [Data Science] Rotular os eventos dos clipes de teste e de desenvolvimento e registrar as contagens (rotulador 1)</summary>

**Objetivo:** Ter _eventos.csv de todos os clipes das duas pastas e a conclusão sobre o mínimo de risos de F1.3.

**Passos previstos:**
1. Marcar no Space os eventos de cada clipe conforme o protocolo.
2. Conferir que cada intervalo tem pelo menos um segundo inteiro amostrado.
3. Contar risos e neutros por pasta.
4. Comparar os risos do teste com o mínimo de F1.3 e os neutros do teste com 4, e registrar 'suficiente' ou 'F3.6 acionado' e, se for o caso, o jitter sem cálculo.

**Definição de pronto:** _eventos.csv de todos os clipes das duas pastas e registro com as contagens e a conclusão.

**Dependências:** F3.4.T3, F1.3

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

<details><summary>F3.4.T7 · [Data Science] Revisar por amostragem os rótulos de rostos e de eventos (rotulador 2)</summary>

**Objetivo:** Fazer a revisão por amostragem do protocolo sobre o trabalho do rotulador 1 antes da publicação.

**Passos previstos:**
1. Sortear a fração de quadros e de intervalos fixada no protocolo, nas duas pastas.
2. Comparar no Space as marcações do rotulador 1 com a leitura do rotulador 2.
3. Registrar as divergências e as correções pedidas no registro de rotulagem.
4. Conferir as correções feitas pelo rotulador 1.

**Definição de pronto:** Registro de revisão com fração revisada, divergências e correções conferidas.

**Dependências:** F3.4.T4, F3.4.T5, F3.4.T6

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F3.4.T8 · [MLOps] Validar as pastas, publicar os rótulos com tag e registrar a revisão</summary>

**Objetivo:** Ter as duas pastas de rótulos no dataset privado, num commit marcado com tag no padrão de F3.5, só com zero erro de arquivo.

**Passos previstos:**
1. Validar cada pasta na validação de pasta do Space com o validador de F1.4 e conferir que não há erro de arquivo.
2. Subir, pela conta dona, as duas pastas ao dataset, no local definido em F3.5, num único commit.
3. Criar a tag no padrão de F3.5.
4. Atualizar a seção de rótulos do card com tag, commit, contagens e concordância.
5. Registrar no PBI o commit e a tag.

**Definição de pronto:** Tag criada, apontando para o commit com as duas pastas, card atualizado e commit e tag registrados no PBI.

**Dependências:** F3.4.T7, F1.4, F3.5.T3

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F3.4.T9 · [QA] Verificar os critérios de aceite sobre a revisão marcada</summary>

**Objetivo:** Registrar passou ou não passou para os 8 critérios de aceite depois da publicação com tag.

**Passos previstos:**
1. Conferir no registro de rotulagem a rodada aprovada, a data e, se houver, as rodadas reprovadas (critérios 1 e 2).
2. Listar o conteúdo da tag e conferir pastas, arquivos e a ausência do concatenado (critério 3).
3. Rodar a validação de pasta do Space sobre a revisão marcada (critério 4).
4. Comparar a lista de t_s revisados de cada clipe com a grade (critério 5).
5. Conferir no registro as contagens de risos e neutros e a conclusão contra F1.3 (critério 6).
6. Conferir as colunas dos arquivos (critério 7).
7. Conferir com 'hf jobs ps -a' que nenhum job leu a pasta de teste (critério 8).

**Definição de pronto:** Checklist dos 8 critérios anexado ao PBI, com passou ou não passou por critério.

**Dependências:** F3.4.T8

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- docs/poc-gate.md:38-40,46-48
- labels/README.md:6-20
- samples/corpus/pib/ffprobe.csv com reacao/ingest.py:34-42 (53 quadros de desenvolvimento, valor derivado)
- samples/corpus/pib/README.md:12
- tools/validar_labels.py:92-95,215-220,229
- bench.py:54,237-239
- tools/rodar_teste.sh:44-52
- out/window_aggregate.json (local, não versionado)
- Premissas P8, P13 e P28 da árvore
- arvore_v1.json: F1.4 (validador sai com erro abaixo do mínimo de F1.3)
- hf_fs ls do dataset em 2026-09-23 (sem labels/)

#### Verificação INVEST: pontos que falharam
- Independente: depende de F1.3, F1.4, F3.1, F3.2, F3.3 e F3.5.
- Small: se a concordância reprovar e for preciso repetir a rodada, pode passar de uma sprint.

#### Premissas
- A rodada de concordância veio de F3.2 para cá, porque só pode ser feita com a ferramenta de F3.3.
- Dois rotuladores. O protocolo de F3.2 fixa o número; se fixar mais, cada rotulador a mais recebe task própria de marcação da amostra.
- O rotulador 1 rotula rostos, quadros revisados e eventos; o rotulador 2 faz a revisão por amostragem. As correções apontadas na revisão reabrem as tasks do rotulador 1.
- Os arquivos exportados pelos rotuladores não têm imagem nem dado pessoal e são enviados ao dataset pela conta dona, que publica.
- A validação antes da publicação roda na validação de pasta do Space de F3.3, que tem os vídeos à mão, sem job pago e sem cópia local.
- Se F1.3 retirar o clipe 11 do teste, o total de t_s de teste fica menor que 195, e o critério 5 usa a grade recalculada.
- Cancelado se F3.1 vetar a PIB (P13 ajustada).
- As horas de rotulagem usam margem sobre a estimativa de labels/README.md:19-20, que não tem medição.
- Disciplinas mantidas da árvore: Data Science, Visão Computacional, QA e MLOps.
- Estimativas (8 pontos e horas das tasks) são sugestão.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Link com a Feature F3 como pai
- Effort ou Story Points: 8 como sugestão
- Códigos de papel dos rotuladores
- Pendência com F1.4: separar erros de arquivo dos mínimos do corpus e aplicar os mínimos só à pasta de teste
- Tags: fase-0; gate-poc; rotulagem; criterio-1; criterio-2

## Preview — PBI F3.5 (novo) · Versionar corpus e rótulos no dataset privado, unificar o local dos rótulos e ler sempre por revisão fixa

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Versionar corpus e rótulos no dataset privado, unificar o local dos rótulos e ler sempre por revisão fixa |
| Tipo | Product Backlog Item |
| Pai | F3 |
| Tags | fase-0; dataset; versionamento; mlops |
| Estimativa | 5 pts (sugestão); tasks: 27 h |
| Dependências | F2.1.T6 (comandos de desenvolvimento de docs/hf-jobs.md reescritos e '--secret' da docstring de processar_culto.py corrigido), só para F3.5.T5, F2.6.T2 (forma de passar segredos aos jobs), só para F3.5.T5 |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro, responsável pelos números do gate  
Quero dataset card com o Dataset Viewer desligado, tags para corpus e rótulos, um único local de rótulos na documentação e nas ferramentas, e bench.py e processar_culto.py lendo o dataset só por revisão fixa e só os arquivos da subpasta pedida  
Para ligar cada número do gate à revisão de corpus e rótulos de onde ele veio, não expor os vídeos no navegador e não baixar o repositório inteiro a cada job

**Contexto:** O dataset ds-fabiopinheiro/reacao-poc-corpus tem 2 commits, só o branch main e nenhuma tag. A raiz tem só pib/ e .gitattributes, sem README.md (HfApi.list_repo_refs e list_repo_commits no levantamento; hf_fs ls em 2026-09-23). O bench resolve hf://datasets/<usuario>/<repo>[/<sub>] com snapshot_download do repositório inteiro para /dev/shm/reacao-bench, sem revision (bench.py:52,58-70). No commit 75e001af52, isso são 299.851.242 bytes (HfApi.dataset_info). O download fica guardado num dicionário pela chave repo_id, com um local_dir por repositório (bench.py:66-70), e corpus e rótulos são resolvidos com o mesmo dicionário (bench.py:205). Com corpus e rótulos no mesmo dataset e em tags diferentes, a segunda chamada devolveria a pasta da primeira. processar_culto.py baixa o vídeo com hf_hub_download para /dev/shm/reacao-in, também sem revision (processar_culto.py:23-31). Downloads podem ser fixados por revision, por tag ou por HfApi.resolve_revision (https://huggingface.co/docs/huggingface_hub/guides/manage-cache#pin-a-revision-advanced; https://huggingface.co/docs/huggingface_hub/package_reference/hf_api). snapshot_download aceita revision, allow_patterns e ignore_patterns (https://huggingface.co/docs/huggingface_hub/package_reference/file_download), e URIs hf:// aceitam o marcador @revisão (https://huggingface.co/docs/huggingface_hub/package_reference/hf_uris). O Dataset Viewer funciona em dataset privado de conta PRO e é desligado com viewer: false no YAML do README.md (https://huggingface.co/docs/hub/datasets-viewer-configure#disable-the-viewer). Montar o dataset com -v num job grava em cache, no disco efêmero, os arquivos lidos (https://huggingface.co/docs/hub/jobs-large-datasets#mount-a-dataset-model-or-bucket), e a regra 1 do CLAUDE.md proíbe isso. docs/hf-jobs.md:8 manda subir o corpus a partir de ./samples, pasta local, e docs/hf-jobs.md:13-19 passa os segredos do Supabase a um job que lê o dataset do corpus. F2.1 reescreve os comandos de desenvolvimento de docs/hf-jobs.md (fontes: docs/hf-jobs.md:13-30) e corrige o '--secret' da docstring de processar_culto.py, e F2.6 define a passagem de segredos só pelo nome (arvore_v1.json, F2.1 e F2.6). As mesmas linhas são alteradas por F2.1.T6, F2.6.T2 e F3.5.T5. O local dos rótulos diverge: labels/ no repositório (labels/README.md:28,36; tools/validar_labels.py:4-5; tools/preparar_rotulagem.py:8-9), samples/corpus/labels (tools/rodar_teste.sh:13) e hf://datasets/<usuario>/reacao-poc-corpus/labels (docs/hf-jobs.md:28). tools/preparar_rotulagem.py só funciona com cópia local: lê os .mp4 por glob em --corpus e cria os CSVs com os.makedirs e open em --labels (tools/preparar_rotulagem.py:27-31,37-43). F5.1 sobe cultos públicos ao mesmo dataset (arvore_v1.json, F5.1). O dataset só tem pib/, e a RN03 da Feature proíbe ler clipes da PIB antes do parecer de F3.1. Os nomes das tags são decisão deste PBI (P24). As regras de revisão e tag valem para corpus e rótulos; os vídeos do piloto vão para o destino de F7.1.

**Regras de negócio:**
- RN01 – O dataset card na raiz desliga o Dataset Viewer e diz o que o dataset contém, quem acessa (preenchido em F3.1) e as regras de uso: nunca extrair quadro e nunca tornar o dataset público (samples/corpus/pib/README.md:20).
- RN02 – O corpus e cada versão publicada dos rótulos recebem tag segundo um padrão definido neste PBI e registrado no card. Tag publicada não é movida nem apagada.
- RN03 – bench.py e processar_culto.py recusam caminho hf://datasets/ sem revisão explícita, com mensagem e código de saída diferente de 0, antes de qualquer download.
- RN04 – Cada execução mostra a revisão pedida e o commit resolvido.
- RN05 – Os jobs baixam para /dev/shm só os arquivos da subpasta usada, e o dataset não é montado com -v. Cada combinação de repositório, revisão e subpasta tem pasta local própria em /dev/shm.
- RN06 – As regras de revisão e tag valem para corpus e rótulos. Os vídeos do piloto vão para o destino de F7.1.
- RN07 – Os rótulos têm um único local no dataset privado, com pastas separadas para teste e desenvolvimento, e a documentação e as ferramentas do repositório apontam para ele.
- RN08 – Nenhum comando documentado que leia pib/ passa SUPABASE_URL ou SUPABASE_SERVICE_KEY (RN07 da Feature).
- RN09 – Os testes e as execuções de verificação deste PBI usam a fixture sintética. Nenhum clipe de pib/ é lido antes do parecer de F3.1.

**Fora de escopo:**
- Base legal, autorização e lista de acesso (F3.1)
- Barreira no código contra gravação no Supabase com vídeo de pib/ (F3.1.T9)
- Linhagem completa no repositório de resultados (F2.5)
- Destino dos vídeos do piloto (F7.1)
- Publicação dos rótulos (F3.4)
- Revisão fixa dos pesos (F2.3)
- Forma de passar segredos, separador '--' e timeout dos comandos de docs/hf-jobs.md e da docstring de processar_culto.py (F2.1.T6, F2.6.T2)

#### Critérios de aceite

- A página do dataset no Hub mostra o dataset card e não mostra o Dataset Viewer.
- O dataset tem a tag do corpus apontando para o commit que contém o card, e o card registra o padrão de tag dos rótulos e a estrutura de pastas.
- bench.py e processar_culto.py, chamados com caminho hf://datasets/ sem revisão, terminam com código diferente de 0 e com mensagem que pede a revisão, sem baixar arquivo.
- Com revisão informada, o bench baixa só os arquivos da subpasta do corpus e da pasta de rótulos pedidas, e não o repositório inteiro (299.851.242 bytes no commit 75e001af52).
- Com corpus e rótulos em revisões diferentes do mesmo dataset, o bench baixa cada um da sua revisão, em pastas locais distintas em /dev/shm.
- A saída de cada execução mostra a revisão pedida e o commit resolvido.
- Caminho de erro: uma revisão inexistente termina com código diferente de 0 e com mensagem que cita a revisão.
- docs/hf-jobs.md mostra os comandos com revisão, não monta o dataset com -v, não manda subir o corpus a partir de pasta local, e nenhum comando que leia pib/ passa SUPABASE_URL ou SUPABASE_SERVICE_KEY. A docstring de processar_culto.py segue a mesma regra.
- labels/README.md, tools/validar_labels.py e docs/hf-jobs.md apontam para o mesmo local de rótulos no dataset privado. A busca no repositório por 'samples/corpus/labels', '--labels labels/', '--corpus samples' e 'preparar_rotulagem' não tem resultado, e tools/preparar_rotulagem.py foi retirado.
- Os testes do repositório cobrem a recusa sem revisão, a passagem da revisão, o filtro de arquivos e corpus e rótulos em revisões diferentes, e ruff check e pytest passam.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F3.5.T1 | Governança e Privacidade | Redigir o dataset card com o Dataset Viewer desligado e as regras de uso | 3 | — |
| F3.5.T2 | Data Science | Definir a estrutura de pastas e o padrão de tags de corpus, rótulos e fixture sintética | 2 | — |
| F3.5.T3 | MLOps | Publicar o dataset card e criar a tag do corpus | 3 | F3.5.T1, F3.5.T2 |
| F3.5.T4 | MLOps | Exigir revisão, filtrar arquivos e separar o cache por revisão nas leituras do dataset em bench.py e processar_culto.py | 10 | — |
| F3.5.T5 | MLOps | Acrescentar revisão aos caminhos hf:// de docs/hf-jobs.md e da docstring de processar_culto.py e retirar os segredos do Supabase dos comandos sobre pib/ | 2 | F3.5.T2, F3.5.T4, F2.1.T6, F2.6.T2 |
| F3.5.T6 | Data Science | Unificar o local dos rótulos em labels/README.md e tools/validar_labels.py e retirar tools/preparar_rotulagem.py | 4 | F3.5.T2 |
| F3.5.T7 | QA | Conferir a leitura por revisão, o local dos rótulos e o card no Hub | 3 | F3.5.T3, F3.5.T4, F3.5.T5, F3.5.T6 |

<details><summary>F3.5.T1 · [Governança e Privacidade] Redigir o dataset card com o Dataset Viewer desligado e as regras de uso</summary>

**Objetivo:** Ter o texto do card pronto para publicação, com as seções que F3.1 vai preencher.

**Passos previstos:**
1. Escrever o YAML com viewer: false.
2. Descrever o conteúdo: pib/ com 23 clipes, o concatenado, concat_list.txt e ffprobe.csv.
3. Registrar as regras de uso (samples/corpus/pib/README.md:20).
4. Criar as seções de autorização e parecer, com o estado 'parecer pendente', e de acesso, tokens, eliminação, retenção, rótulos e tags.
5. Conferir que o card não traz e-mail pessoal.

**Definição de pronto:** Texto do card revisado por Fabio Pinheiro.

**Dependências:** nenhuma

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F3.5.T2 · [Data Science] Definir a estrutura de pastas e o padrão de tags de corpus, rótulos e fixture sintética</summary>

**Objetivo:** Ter no card a estrutura de pastas dos rótulos (teste e desenvolvimento separados, com _faces.csv, _eventos.csv e lista de t_s revisados), a pasta da fixture sintética dos jobs e o padrão de nome das tags.

**Passos previstos:**
1. Definir as pastas de rótulos por conjunto (teste e desenvolvimento) e por origem (PIB e, se F3.6 for acionado, corpus público).
2. Definir o nome do arquivo da lista de t_s revisados por clipe.
3. Definir a pasta da fixture sintética que F1.1.T6 publica para os jobs de fumaça, validação e paridade, separada de pib/, do corpus público e dos rótulos, e a forma de registrar sua revisão e o SHA-256.
4. Definir o padrão de tag do corpus e dos rótulos, com número de versão.
5. Registrar que tag publicada não é movida nem apagada.
6. Escrever a seção no texto do card.

**Definição de pronto:** Seção de pastas (rótulos, corpus público e fixture sintética) e tags no texto do card, revisada por MLOps.

**Dependências:** nenhuma

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F3.5.T3 · [MLOps] Publicar o dataset card e criar a tag do corpus</summary>

**Objetivo:** Ter o card na raiz do dataset e a tag do corpus apontando para o commit que o contém.

**Passos previstos:**
1. Publicar, pela conta dona, o README.md na raiz do dataset num commit.
2. Criar a tag do corpus nesse commit, no padrão de T2.
3. Conferir na página do dataset que o Dataset Viewer não aparece.
4. Conferir a tag com list_repo_refs e registrar commit e tag no PBI.

**Definição de pronto:** Card visível no Hub, sem Dataset Viewer, e tag do corpus listada em list_repo_refs.

**Dependências:** F3.5.T1, F3.5.T2

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F3.5.T4 · [MLOps] Exigir revisão, filtrar arquivos e separar o cache por revisão nas leituras do dataset em bench.py e processar_culto.py</summary>

**Objetivo:** Fazer as leituras do dataset usarem sempre revisão fixa, baixarem só a subpasta pedida e não misturarem revisões do mesmo repositório.

**Passos previstos:**
1. Aceitar a revisão no caminho hf://datasets/<usuario>/<repo>@<revisão>/<sub>, no formato de hf_uris.
2. Recusar caminho hf://datasets/ sem revisão, com mensagem e código diferente de 0, antes de qualquer download.
3. Passar revision a snapshot_download e a hf_hub_download e, no bench, usar allow_patterns só com a subpasta pedida.
4. Trocar a chave do cache de resolve_pasta de repo_id para (repo_id, revisão, subpasta), com local_dir distinto em /dev/shm para cada chave (bench.py:66-70,205).
5. Resolver e mostrar o commit da revisão lida e expô-lo para a linhagem de F2.5.
6. Manter os downloads em /dev/shm, sem montagem -v.
7. Escrever testes com as funções do huggingface_hub substituídas: recusa sem revisão, revisão repassada, allow_patterns restrito e corpus e rótulos em revisões diferentes do mesmo repositório.
8. Rodar ruff check e pytest e abrir PR citando o PBI.

**Definição de pronto:** PR mesclado, testes novos passando no CI e execução local com --provider mock, contra um dataset de teste privado da conta dona só com a fixture sintética, mostrando a revisão pedida e o commit resolvido, sem leitura de pib/.

**Dependências:** nenhuma

**Estimativa sugerida:** 10 h (sugestão; validar com o time)

</details>

<details><summary>F3.5.T5 · [MLOps] Acrescentar revisão aos caminhos hf:// de docs/hf-jobs.md e da docstring de processar_culto.py e retirar os segredos do Supabase dos comandos sobre pib/</summary>

**Objetivo:** Depois de F2.1.T6 e F2.6.T2, deixar os comandos documentados lendo o dataset por revisão fixa e sem os segredos do Supabase nos comandos sobre pib/, sem mudar a forma de passar segredos definida por aquelas tasks.

**Passos previstos:**
1. Partir dos comandos de docs/hf-jobs.md e da docstring de processar_culto.py:12-13 como F2.1.T6 e F2.6.T2 os deixaram. Não alterar a forma de passar segredos, o separador '--' nem o timeout.
2. Acrescentar @<tag> e a subpasta usada a cada caminho hf://datasets/ dos comandos e da docstring, no formato aceito por F3.5.T4.
3. Apontar o caminho dos rótulos no comando do bench (hoje em docs/hf-jobs.md:28) para a pasta e a tag definidas em T2.
4. Registrar junto aos comandos que o dataset não é montado com -v.
5. Retirar a instrução 'hf upload ... ./samples' (docs/hf-jobs.md:8), que parte de cópia local, se ela ainda existir depois de F2.1.T6.
6. Retirar SUPABASE_URL e SUPABASE_SERVICE_KEY de todo comando que leia pib/, mantendo os demais segredos como F2.1.T6 e F2.6.T2 os deixaram.
7. Conferir cada comando alterado com 'hf jobs uv run --dry-run', que não lança job (.venv/lib/python3.11/site-packages/huggingface_hub/cli/jobs.py:186-256).
8. Abrir PR citando o PBI.

**Definição de pronto:** PR mesclado. Em docs/hf-jobs.md e na docstring de processar_culto.py, todo caminho hf://datasets/ tem @revisão, os rótulos apontam para o local de T2, nenhum comando sobre pib/ passa SUPABASE_URL ou SUPABASE_SERVICE_KEY, a forma de passar segredos continua a de F2.1.T6 e F2.6.T2, e o --dry-run de cada comando alterado termina sem erro.

**Dependências:** F3.5.T2, F3.5.T4, F2.1.T6, F2.6.T2

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F3.5.T6 · [Data Science] Unificar o local dos rótulos em labels/README.md e tools/validar_labels.py e retirar tools/preparar_rotulagem.py</summary>

**Objetivo:** Fazer a documentação e as ferramentas de rótulos apontarem para o mesmo local no dataset privado, sem roteiro que dependa de cópia local do vídeo.

**Passos previstos:**
1. Adotar o local no dataset privado com as pastas e o padrão de tags de T2.
2. Em labels/README.md:19-20, apontar para a ferramenta de F3.3.
3. Reescrever labels/README.md:25-41 para descrever a exportação e a validação de pasta no Space, sem '--labels labels/' e sem '--corpus samples/'.
4. Atualizar os exemplos da docstring de tools/validar_labels.py:4-5 para pastas em /dev/shm, como o Space as usa.
5. Retirar tools/preparar_rotulagem.py e as referências a ele.
6. Rodar ruff check e pytest e abrir PR citando o PBI.

**Definição de pronto:** PR mesclado, busca por 'samples/corpus/labels', '--labels labels/', '--corpus samples' e 'preparar_rotulagem' no repositório sem resultado e CI verde.

**Dependências:** F3.5.T2

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F3.5.T7 · [QA] Conferir a leitura por revisão, o local dos rótulos e o card no Hub</summary>

**Objetivo:** Registrar passou ou não passou para os 10 critérios de aceite.

**Passos previstos:**
1. Conferir no CI que os testes de T4 cobrem recusa sem revisão, revisão repassada, allow_patterns restrito e revisões diferentes de corpus e rótulos, e que passam.
2. Testar uma revisão inexistente no dataset de teste e conferir o código e a mensagem.
3. Conferir na página do dataset a ausência do Dataset Viewer e a tag com list_repo_refs.
4. Conferir com 'hf download --dry-run' que o filtro lista só a subpasta, sem baixar arquivo.
5. Conferir docs/hf-jobs.md e a docstring de processar_culto.py contra o critério 8.
6. Fazer as buscas do critério 9 no repositório.

**Definição de pronto:** Checklist dos 10 critérios anexado ao PBI, com passou ou não passou por critério.

**Dependências:** F3.5.T3, F3.5.T4, F3.5.T5, F3.5.T6

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- bench.py:52,58-70,205
- processar_culto.py:12-13,23-31
- docs/hf-jobs.md:8,13-19,23-29
- labels/README.md:19-20,25-41
- tools/validar_labels.py:4-5
- tools/preparar_rotulagem.py:8-9,27-31,37-43
- tools/rodar_teste.sh:13
- samples/corpus/pib/README.md:20 (não versionado)
- CLAUDE.md (regra 1)
- arvore_v1.json: F5.1 (cultos públicos no mesmo dataset)
- HfApi.list_repo_refs, list_repo_commits e dataset_info(files_metadata=True) no levantamento; hf_fs ls em 2026-09-23
- https://huggingface.co/docs/hub/datasets-viewer-configure#disable-the-viewer
- https://huggingface.co/docs/hub/datasets-cards#dataset-card-metadata
- https://huggingface.co/docs/hub/jobs-large-datasets#mount-a-dataset-model-or-bucket
- https://huggingface.co/docs/huggingface_hub/guides/manage-cache#pin-a-revision-advanced
- https://huggingface.co/docs/huggingface_hub/package_reference/file_download
- https://huggingface.co/docs/huggingface_hub/package_reference/hf_uris
- https://huggingface.co/docs/huggingface_hub/package_reference/hf_api
- https://huggingface.co/docs/huggingface_hub/guides/download#dry-run-mode
- arvore_v1.json: F2.1 (comandos de desenvolvimento de docs/hf-jobs.md:13-30 e '--secret' da docstring) e F2.6 (segredos só pelo nome)
- .venv/lib/python3.11/site-packages/huggingface_hub/cli/jobs.py:186-256 (--dry-run sem efeito colateral)
- F1 detalhada: F1.1.T6 depende de F3.5.T2 (pasta da fixture sintética com revisão fixa e SHA-256)

#### Verificação INVEST: pontos que falharam
- Independente: F3.5.T5 espera F2.1.T6 e F2.6.T2, que alteram as mesmas linhas de docs/hf-jobs.md e da docstring de processar_culto.py. As demais tasks não dependem de outra Feature.

#### Premissas
- A disciplina QA foi acrescentada às previstas na árvore (MLOps, Data Science, Governança e Privacidade), porque o PBI altera código Python e precisa de verificação.
- A mudança em bench.py e processar_culto.py ficou com MLOps, porque trata de versionamento de dados. Não foi acrescentada disciplina Backend.
- O commit resolvido é mostrado na saída e exposto para F2.5, que o grava na linhagem. Este PBI não cria coluna no Supabase.
- A estrutura de pastas e o padrão de tags são propostos na task de Data Science. P24 deixa os nomes a cargo deste PBI.
- tools/preparar_rotulagem.py é retirado porque exige cópia local dos .mp4, o que F3.1 proíbe, e a grade de quadros passa a vir da ferramenta de F3.3. É proposta deste detalhamento.
- A troca do local dos rótulos em docs/hf-jobs.md fica só em F3.5.T5. F2.1.T6 e F2.6.T2 alteram antes os comandos e a forma de passar segredos, e F3.1.T8 acrescenta notas numa seção separada do mesmo arquivo.
- F3.5.T5 roda depois de F2.1.T6 e F2.6.T2 e, nos comandos, altera só os caminhos hf:// (revisão, subpasta e local dos rótulos), a nota sobre -v, a instrução de upload local e os segredos do Supabase dos comandos sobre pib/. Os IDs F2.1.T6 e F2.6.T2 vêm do detalhamento de F2.1 e F2.6 citado na revisão. A árvore não tem tasks e confirma o escopo só no nível de PBI.
- Os segredos do Supabase saem só dos comandos sobre pib/, porque F5.1 sobe cultos públicos ao mesmo dataset e F5.4 grava os resultados deles no Supabase.
- A execução de verificação usa a fixture sintética num dataset de teste privado da conta dona, com --provider mock e sem job pago. O dataset do corpus só tem pib/, e RN09 proíbe lê-lo antes do parecer.
- Os testes de leitura por revisão são escritos na task do código (T4). A QA confere cobertura e resultado no CI e faz as conferências no Hub.
- A task de publicação do card é executada pela conta dona.
- Estimativas (5 pontos e horas das tasks) são sugestão.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável
- Link com a Feature F3 como pai
- Effort ou Story Points: 5 como sugestão
- Avisar os responsáveis por F2.1.T6 e F2.6.T2 de que F3.5.T5 roda depois delas e altera nos comandos só caminhos hf://, a nota sobre -v, a instrução de upload local e os segredos do Supabase sobre pib/
- Avisar os responsáveis por F2.5 e F7.5 do formato do caminho com revisão
- Combinar com F1.4: este PBI reescreve labels/README.md:19-41 e a docstring de tools/validar_labels.py:4-5 e retira tools/preparar_rotulagem.py. F1.4 deixa de alterar o preparador e de corrigir labels/README.md:36.
- Tags: fase-0; dataset; versionamento; mlops
- Vínculo F3.5.T2 → F1.1.T6 no Azure DevOps: F1.1.T6 publica a fixture sintética na pasta definida em F3.5.T2 (F1 detalhada).

## Preview — PBI F3.6 (novo) · Selecionar clipes públicos de plateia, registrar licença e parecer e transferi-los ao dataset privado quando o corpus da PIB não puder ser usado ou não tiver risos suficientes

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Selecionar clipes públicos de plateia, registrar licença e parecer e transferi-los ao dataset privado quando o corpus da PIB não puder ser usado ou não tiver risos suficientes |
| Tipo | Product Backlog Item |
| Pai | F3 |
| Tags | fase-0; condicional; corpus-publico; dataset |
| Estimativa | 5 pts (sugestão); tasks: 23 h |
| Dependências | Acionamento: F3.1 (veto da PIB) ou F3.4 (risos abaixo do mínimo), F1.3 (mínimo de risos), F1.1 (script de lançamento dos jobs), F3.5 (pastas e padrão de tags), F3.1.T2 (encarregado nomeado), F5.1.T3 e F5.1.T5 (procedimento do token de escrita de uso único, registrado no inventário de F2.6.T6), para F3.6.T3 e F3.6.T5, F5.1.T4 (script de cópia parametrizado e comando documentado em docs/hf-jobs.md), para F3.6.T4, F2.2 (fluxo de publicação da imagem por tag com digest e tamanho de /dev/shm medido), para F3.6.T4, F2.6.T6 (inventário de credenciais), F5.1 (lista de cultos, para excluí-los, se já existir), Aprovação de Fabio (P7), com flavor, duração e custo previstos, para o job de transferência |
| Substitui | nenhum |

#### Descrição

Como Fabio Pinheiro, responsável pelo gate  
Quero clipes públicos de plateia com licença e parecer registrados, versionados no dataset privado sob tag própria  
Para que F3.7 os rotule e os critérios 1 e 2 sejam medidos mesmo que o parecer vete a PIB na Fase 0 ou que o conjunto de teste da PIB não tenha risos suficientes

**Contexto:** PBI condicional. Entra se F3.1 concluir que a PIB não pode ser usada na Fase 0 (P13 ajustada) ou se F3.4 registrar menos risos que o mínimo de F1.3. O README descreve a Fase 0 com vídeos públicos de pregação que permitem download (README.pt-BR.md:34), e o CONTRIBUTING pede registrar a licença em docs/corpus.csv (CONTRIBUTING.md:11). docs/corpus.csv só tem o cabeçalho, com as colunas video, url, duracao_min, resolucao, enquadramento, altura_rosto_mediana_px_estimada, idioma, permite_download e observacoes (docs/corpus.csv:1). O critério 1 foi escrito para rostos de 34 a 96 px, condição da PIB (docs/poc-gate.md:8; docs/adr/0001-motor.md:4). O mínimo de risos para o 2a ser conclusivo sai de F1.3. F5.1 seleciona três cultos públicos inteiros, que os jobs de F5.4 processam e cujo relatório o painel web na Vercel exibe. Esses vídeos passam pelo pipeline antes do bench e por isso não servem como teste cego (docs/poc-gate.md:38-40). F5.1 não tem hoje regra para excluir os vídeos desta seleção (arvore_v1.json, F5.1). A regra 1 do CLAUDE.md proíbe vídeo em disco, então a transferência da origem ao dataset passa por job no HF com /dev/shm. F2.6 prevê para os jobs token de leitura do dataset e diz que o token dos jobs não escreve no dataset do corpus (arvore_v1.json, F2.6). F5.1 já tem o job de cópia de vídeos públicos para o dataset privado: F5.1.T4 escreve em tools/ um script que recebe a lista de vídeos e o destino no dataset, roda por job cpu-basic pela imagem com digest dentro da guarda e documenta os parâmetros em docs/hf-jobs.md para este PBI reutilizar; F5.1.T3 cria o token de escrita de uso único e registra no inventário de credenciais de F2.6.T6 o procedimento de criação, passagem e revogação, e F5.1.T5 o revoga (F5 detalhada). A imagem já instala ffmpeg (Dockerfile:5). Um token fine-grained pode ser limitado a repositórios específicos (https://huggingface.co/docs/hub/security-tokens). Este backlog trata um vídeo público de culto como dado sensível até o parecer, como os clipes da PIB (premissa da Feature). Se F3.1 vetar a PIB, os clipes 07 a 10 também deixam de valer, e F4.4 e F4.5 precisam de clipes públicos de desenvolvimento (P8).

**Regras de negócio:**
- RN01 – Acionado pelo veto de F3.1, o PBI seleciona vídeos para um conjunto de desenvolvimento e um de teste, sem vídeo em comum, para que F4.4 e F4.5 tenham onde calibrar. Acionado pela falta de risos em F3.4, completa só o conjunto de teste.
- RN02 – Cada vídeo tem download permitido pela licença ou pelos termos da origem, planos de plateia, rostos estimados entre 34 e 96 px e pelo menos um riso visível, e fica registrado em docs/corpus.csv com a licença e com a marcação do uso em F3.6 em observacoes.
- RN03 – Os vídeos são diferentes dos cultos de F5.1. Nenhum vídeo desta seleção passa por job de pipeline, bench ou calibração antes do bench de F4.6. O único job que os lê antes disso é o de transferência.
- RN04 – O vídeo vai da origem ao dataset privado por job no HF, com o script de cópia de F5.1.T4 acrescido do recorte por intervalo, pela imagem publicada com digest no fluxo de F2.2, lançado pelo script de F1.1, com download para /dev/shm e sem cópia em disco local. Cada job pago tem aprovação prévia de Fabio (P7), com flavor, duração e custo previstos.
- RN05 – O job de transferência usa um token fine-grained com escrita só neste dataset, criado pela conta dona pelo procedimento de F5.1.T3, registrado no inventário de credenciais de F2.6.T6 como exceção de uso único e revogado ao fim pelo procedimento de F5.1.T5. O card também registra o token.
- RN06 – O encarregado registra a análise de uso dos vídeos selecionados com o mesmo roteiro de F3.1.
- RN07 – Os clipes recebem tag própria no padrão de F3.5.

**Fora de escopo:**
- Rotulagem e publicação dos rótulos dos clipes públicos (F3.7)
- Cultos inteiros para os critérios 3 e 4 (F5.1)
- Rótulos de momentos
- Vídeos do piloto (F7.1)
- Bench sobre os clipes públicos (F4.6)
- Qualquer processamento local dos vídeos públicos

#### Critérios de aceite

- O registro de acionamento cita a condição (veto de F3.1 ou contagem de risos de F3.4) e a data.
- Cada vídeo selecionado tem linha em docs/corpus.csv com url, permite_download, altura_rosto_mediana_px_estimada e enquadramento preenchidos e com a licença e o uso em F3.6 em observacoes.
- Nenhum vídeo selecionado aparece na lista de cultos de F5.1, se ela existir. Se não existir, a pendência de exclusão está registrada em F5.1.
- Os clipes estão no dataset privado sob tag própria, e o registro do job de transferência mostra o download para /dev/shm, o JOB_ID e a imagem com digest em 'hf jobs inspect'.
- Com acionamento pelo veto, os clipes estão separados em desenvolvimento e teste, sem vídeo em comum.
- O dataset privado contém o parecer datado do encarregado sobre os vídeos públicos.
- O token de escrita usado no job de transferência aparece revogado na lista de tokens da conta, e o card e o inventário de credenciais de F2.6.T6 registram nome, uso e data de revogação.
- Nenhum job de pipeline, bench ou calibração leu esses vídeos antes de F4.6. O único job que os leu é o de transferência, identificado pelo JOB_ID registrado.
- Caminho de erro: um vídeo que o parecer não permite sai da lista e de docs/corpus.csv. Se nenhum vídeo restar, o registro diz isso, F3.7 não é acionado e a leitura do 2a segue a regra de F1.3.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F3.6.T1 | Data Science | Selecionar os vídeos públicos e registrar em docs/corpus.csv | 8 | Acionamento por F3.1 ou F3.4, F5.1 (lista de cultos, se já existir) |
| F3.6.T2 | Governança e Privacidade | Registrar com o encarregado a licença e a análise de uso dos vídeos públicos | 4 | F3.6.T1, F3.1.T2 |
| F3.6.T3 | DevOps | Criar pelo procedimento de F5.1.T3 o token de escrita de uso único para o job de transferência e registrá-lo no inventário de credenciais | 1 | F3.6.T2, F5.1.T3 (procedimento registrado), F2.6.T6 |
| F3.6.T4 | MLOps | Acrescentar o recorte por intervalo ao script de cópia de F5.1.T4, transferir os trechos ao dataset privado por job no HF e marcar com tag | 6 | F3.6.T3, F5.1.T4, F1.1, F2.2, F3.5, Aprovação de Fabio (P7), com flavor, duração e custo previstos |
| F3.6.T5 | DevOps | Revogar o token de escrita do job de transferência | 1 | F3.6.T4 |
| F3.6.T6 | QA | Verificar os critérios de aceite de F3.6 | 3 | F3.6.T2, F3.6.T4, F3.6.T5 |

<details><summary>F3.6.T1 · [Data Science] Selecionar os vídeos públicos e registrar em docs/corpus.csv</summary>

**Objetivo:** Ter a lista de vídeos públicos, com intervalos, licença e uso, registrada em docs/corpus.csv.

**Passos previstos:**
1. Registrar a condição de acionamento e a data.
2. Buscar vídeos públicos de culto com download permitido, planos de plateia, rostos estimados de 34 a 96 px e risos visíveis, assistindo na origem, sem baixar.
3. Excluir os vídeos da lista de F5.1, se ela existir.
4. Com acionamento pelo veto, separar vídeos de desenvolvimento e de teste, sem vídeo em comum.
5. Anotar os intervalos de cada vídeo a transferir.
6. Registrar cada vídeo em docs/corpus.csv (url, duração, resolução, enquadramento, altura estimada, idioma, permite_download, licença e uso em F3.6 em observacoes) e abrir PR citando o PBI.

**Definição de pronto:** PR mesclado com as linhas em docs/corpus.csv e a lista de intervalos por vídeo.

**Dependências:** Acionamento por F3.1 ou F3.4, F5.1 (lista de cultos, se já existir)

**Estimativa sugerida:** 8 h (sugestão; validar com o time)

</details>

<details><summary>F3.6.T2 · [Governança e Privacidade] Registrar com o encarregado a licença e a análise de uso dos vídeos públicos</summary>

**Objetivo:** Ter um parecer datado sobre o uso de cada vídeo público na Fase 0.

**Passos previstos:**
1. Conferir a licença e os termos de download de cada origem.
2. Aplicar o roteiro de F3.1 (art. 5º, II; art. 11; art. 33).
3. Registrar o parecer datado no dataset privado.
4. Retirar da lista os vídeos que o parecer não permitir e atualizar docs/corpus.csv.

**Definição de pronto:** Parecer datado no dataset privado cobrindo cada vídeo da lista final.

**Dependências:** F3.6.T1, F3.1.T2

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F3.6.T3 · [DevOps] Criar pelo procedimento de F5.1.T3 o token de escrita de uso único para o job de transferência e registrá-lo no inventário de credenciais</summary>

**Objetivo:** Dar ao job de transferência um token com escrita só neste dataset, sem ampliar os tokens de F2.6, com o mesmo procedimento e o mesmo registro de F5.1.T3.

**Passos previstos:**
1. Seguir o procedimento registrado por F5.1.T3 no inventário de F2.6.T6.
2. Criar, pela conta dona, um token fine-grained com escrita só no dataset ds-fabiopinheiro/reacao-poc-corpus (https://huggingface.co/docs/hub/security-tokens).
3. Deixá-lo disponível para ser passado ao job só pelo nome do segredo.
4. Registrar no inventário de F2.6.T6 e no card o nome, o escopo, o uso em F3.6.T4, a exceção de uso único a F2.6 e a revogação prevista em F3.6.T5.

**Definição de pronto:** Token criado, escopo conferido na página de tokens e registro no inventário de F2.6.T6 e no card.

**Dependências:** F3.6.T2, F5.1.T3 (procedimento registrado), F2.6.T6

**Estimativa sugerida:** 1 h (sugestão; validar com o time)

</details>

<details><summary>F3.6.T4 · [MLOps] Acrescentar o recorte por intervalo ao script de cópia de F5.1.T4, transferir os trechos ao dataset privado por job no HF e marcar com tag</summary>

**Objetivo:** Ter os clipes públicos no dataset privado sob tag, sem nenhuma cópia local, reutilizando o job de cópia de F5.1.

**Passos previstos:**
1. Acrescentar ao script de F5.1.T4 o recorte dos intervalos da lista com o ffmpeg da imagem (Dockerfile:5), em /dev/shm, com teste; os parâmetros de F5.1 (lista de vídeos e destino no dataset) continuam iguais.
2. Publicar a imagem com o script alterado por tag de release pelo fluxo de F2.2 e registrar o digest.
3. Conferir que o tamanho de cada vídeo cabe no /dev/shm medido em F2.2.
4. Pedir a aprovação de Fabio (P7) com flavor de CPU, duração e custo previstos.
5. Lançar o job pela imagem com digest e pelo comando documentado por F5.1.T4 em docs/hf-jobs.md, validado com o lançador de F1.1, com o token de T3 pelo nome do segredo e a pasta do corpus público como destino.
6. Apagar /dev/shm ao fim e registrar JOB_ID, digest e custo.
7. Criar a tag do corpus público no padrão de F3.5 e atualizar o card.

**Definição de pronto:** Clipes no dataset sob tag, JOB_ID, digest e custo registrados, 'hf jobs inspect' com a imagem por digest e log da guarda sem arquivo de vídeo fora de /dev/shm.

**Dependências:** F3.6.T3, F5.1.T4, F1.1, F2.2, F3.5, Aprovação de Fabio (P7), com flavor, duração e custo previstos

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F3.6.T5 · [DevOps] Revogar o token de escrita do job de transferência</summary>

**Objetivo:** Encerrar o acesso de escrita no dataset criado para o job.

**Passos previstos:**
1. Revogar, pela conta dona, o token de T3, pelo procedimento de F5.1.T5.
2. Registrar no card e no inventário de F2.6.T6 a data de revogação.

**Definição de pronto:** Token revogado na lista de tokens da conta e data registrada no card e no inventário de F2.6.T6.

**Dependências:** F3.6.T4

**Estimativa sugerida:** 1 h (sugestão; validar com o time)

</details>

<details><summary>F3.6.T6 · [QA] Verificar os critérios de aceite de F3.6</summary>

**Objetivo:** Registrar passou ou não passou para os 9 critérios antes de F3.7 começar.

**Passos previstos:**
1. Conferir o registro de acionamento e as linhas de docs/corpus.csv contra os critérios 1 e 2.
2. Conferir que nenhum vídeo está na lista de F5.1, ou que a pendência está registrada em F5.1, e que desenvolvimento e teste não têm vídeo em comum.
3. Conferir a tag, o registro do job, o JOB_ID e a imagem por digest em 'hf jobs inspect'.
4. Conferir o parecer datado no dataset.
5. Conferir com Fabio a revogação do token na lista de tokens da conta e o registro no inventário de F2.6.T6.
6. Conferir em 'hf jobs ps -a', em run_log e no registro de F2.5 que o único job sobre esses vídeos é o de transferência.

**Definição de pronto:** Checklist dos 9 critérios anexado ao PBI, com passou ou não passou por critério.

**Dependências:** F3.6.T2, F3.6.T4, F3.6.T5

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- README.pt-BR.md:34
- CONTRIBUTING.md:11
- docs/corpus.csv:1
- docs/poc-gate.md:8,9,38-40,46-48
- docs/adr/0001-motor.md:4
- CLAUDE.md (regra 1)
- arvore_v1.json: F2.6 (token dos jobs sem escrita no dataset) e F5.1 (sem exclusão dos vídeos de F3.6)
- Premissas P7, P8, P13 e P29 da árvore
- https://huggingface.co/docs/hub/security-tokens
- https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm (art. 5º, II; art. 11; art. 33)
- F5 detalhada: F5.1.T3, F5.1.T4, F5.1.T5 e premissa de F5.1 sobre o recorte por intervalo acrescentado por F3.6.T4
- Dockerfile:5 (ffmpeg instalado na imagem)

#### Verificação INVEST: pontos que falharam
- Independente: condicional a F3.1 ou F3.4 e dependente de F1.3, F1.1, F3.5, F2.2, F2.6.T6, F5.1.T3, F5.1.T4 e do encarregado.
- Estimável: o número de vídeos só é conhecido depois da seleção.

#### Premissas
- Este PBI e F3.7 vêm da divisão do F3.6 da árvore, que as invest_falhas já propunham. Disciplinas: a árvore previa Data Science, Visão Computacional, Governança e Privacidade e QA. Visão Computacional foi para F3.7, com a rotulagem. Entraram DevOps (token) e MLOps (transferência e tag).
- O conjunto de desenvolvimento público, no caso de veto, é dedução de P8 e P13: sem os clipes 07 a 10, F4.4 e F4.5 não têm onde calibrar.
- Os intervalos a recortar são escolhidos assistindo aos vídeos na origem, sem baixá-los. O recorte acontece dentro do job.
- A marcação do uso em F3.6 em observacoes de docs/corpus.csv é proposta deste detalhamento, para F5.1 excluir esses vídeos.
- O token de escrita de uso único é exceção à política de F2.6, com o mesmo procedimento de F5.1.T3 e F5.1.T5 e registro no inventário de F2.6.T6. A alternativa, gravar num destino intermediário e publicar pela conta dona, criaria outra cópia.
- As tasks de token, job e tag são executadas pela conta dona.
- Número de vídeos desconhecido até a seleção.
- Estimativas (5 pontos e horas das tasks) são sugestão.
- O recorte por intervalo, que só este PBI usa, é acrescentado ao script de F5.1.T4 por F3.6.T4, para F5.1 não carregar código que não usa (premissa de F5.1 na F5 detalhada).

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável, só quando o PBI for acionado
- Link com a Feature F3 como pai
- Effort ou Story Points: 5 como sugestão
- Aprovação de Fabio (P7) para o job de transferência, com flavor, duração e custo previstos
- Inventário de credenciais de F2.6.T6: registrar o token de F3.6.T3 e a revogação de F3.6.T5, pelo procedimento de F5.1.T3 (F5 já registra o próprio token no mesmo inventário).
- Pendência com F5.1: excluir da seleção os vídeos marcados por F3.6 em docs/corpus.csv
- Tags: fase-0; condicional; corpus-publico; dataset
- Vínculos F5.1.T3 → F3.6.T3, F5.1.T4 → F3.6.T4 e F2.2 → F3.6.T4 no Azure DevOps

## Preview — PBI F3.7 (novo) · Rotular os clipes públicos de F3.6 e publicar os rótulos com tag quando o corpus da PIB não puder ser usado ou não tiver risos suficientes

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Rotular os clipes públicos de F3.6 e publicar os rótulos com tag quando o corpus da PIB não puder ser usado ou não tiver risos suficientes |
| Tipo | Product Backlog Item |
| Pai | F3 |
| Tags | fase-0; condicional; corpus-publico; rotulagem |
| Estimativa | 8 pts (sugestão); tasks: 40 h |
| Dependências | F3.6 (clipes públicos sob tag, parecer e registro de acionamento), F1.3 (mínimo de risos), F1.4 (validador atualizado), F3.2 (protocolo), F3.3 (ferramenta), F3.5 (pastas e padrão de tags), Rotuladores disponíveis |
| Substitui | nenhum |

#### Descrição

Como time de Data Science e Visão Computacional que roda o bench do gate  
Quero os rótulos dos clipes públicos de F3.6, com concordância medida, validados e publicados com tag no dataset privado  
Para medir os critérios 1 e 2 em F4.6 e, no caso de veto da PIB, calibrar F4.4 e F4.5 nos clipes públicos de desenvolvimento

**Contexto:** PBI condicional. Entra depois de F3.6, quando há clipes públicos no dataset sob tag. Com o veto de F3.1, F3.4 é cancelado e a rodada de concordância nos clipes 07 a 10 não acontece, então a rodada é feita aqui nos clipes públicos de desenvolvimento. Com a falta de risos em F3.4, a rodada aprovada em F3.4 vale se os rotuladores forem os mesmos. O protocolo é o de F3.2 e a ferramenta é a de F3.3. A cobertura é contada pela lista de t_s revisados. O número de quadros só é conhecido depois de F3.6, por isso as horas de rotulagem são sugestão proporcional às de F3.4 (195 quadros de teste em 10 h, labels/README.md:19-20 sem medição). A publicação segue a regra da Feature: zero erro de arquivo, mínimos só na pasta de teste, sem bloquear.

**Regras de negócio:**
- RN01 – Com acionamento pelo veto, a concordância é medida primeiro, numa amostra dos clipes públicos de desenvolvimento definida no protocolo. Com acionamento pela falta de risos, vale a rodada aprovada de F3.4 se os rotuladores forem os mesmos; se não forem, faz-se nova rodada numa amostra definida no protocolo.
- RN02 – Os rótulos de desenvolvimento e de teste dos clipes públicos ficam em pastas separadas, sem vídeo em comum.
- RN03 – Todo t_s da grade de cada clipe consta na lista de t_s revisados.
- RN04 – A revisão por amostragem é feita por um rotulador diferente do que rotulou.
- RN05 – A publicação só acontece quando o validador de F1.4 não aponta erro de arquivo em nenhuma pasta. O mínimo de risos de F1.3 é contado só na pasta de teste e não bloqueia a publicação.
- RN06 – Nenhum job de pipeline, bench ou calibração lê os clipes ou os rótulos de teste antes de F4.6.
- RN07 – Rotulagem e publicação seguem F3.2, F3.3 e o padrão de tags de F3.5, com tag própria.

**Fora de escopo:**
- Seleção, parecer e transferência dos clipes (F3.6)
- Bench sobre os clipes públicos (F4.6)
- Calibração de limiares (F4.5)
- Rótulos de momentos
- Caixas por rosto

#### Critérios de aceite

- O registro de rotulagem traz a rodada de concordância aprovada nos clipes públicos ou a referência à rodada aprovada de F3.4, com os mesmos códigos de papel, com data anterior ao início da rotulagem de teste.
- Caminho de erro: com concordância abaixo do limite, o registro mostra a rodada reprovada e a revisão do protocolo, e a rotulagem de teste só começa depois de uma rodada aprovada.
- A revisão marcada com a tag dos rótulos públicos contém a pasta de teste e, com acionamento pelo veto, a pasta de desenvolvimento, com _faces.csv, _eventos.csv e a lista de t_s revisados de cada clipe.
- O validador de F1.4 não aponta erro de arquivo em nenhuma pasta publicada, com os vídeos correspondentes.
- Todo t_s da grade de cada clipe consta na lista de t_s revisados.
- O registro traz a contagem de risos do conjunto de teste contra o mínimo de F1.3 e conclui 'suficiente' ou '2a inconclusivo pela regra de F1.3'. A publicação não depende dessa conclusão.
- Os arquivos de rótulo têm só t_s e altura_px em _faces.csv, só t_ini_s, t_fim_s e tipo em _eventos.csv e só t_s na lista de revisados.
- Nenhum job de pipeline, bench ou calibração leu os clipes ou os rótulos de teste antes de F4.6. O único job anterior sobre os clipes é o de transferência de F3.6, identificado pelo JOB_ID registrado.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F3.7.T1 | Visão Computacional | Marcar a amostra de concordância nos clipes públicos (rotulador 1), quando a rodada for necessária | 2 | F3.6, F3.2, F3.3 |
| F3.7.T2 | Visão Computacional | Marcar a amostra de concordância nos clipes públicos (rotulador 2), quando a rodada for necessária | 2 | F3.6, F3.2, F3.3 |
| F3.7.T3 | Data Science | Calcular e registrar a concordância nos clipes públicos ou registrar a referência à rodada de F3.4 | 3 | F3.7.T1, F3.7.T2 |
| F3.7.T4 | Visão Computacional | Rotular os rostos e os quadros revisados dos clipes públicos de desenvolvimento (rotulador 1), com acionamento pelo veto | 4 | F3.7.T3 |
| F3.7.T5 | Visão Computacional | Rotular os rostos e os quadros revisados dos clipes públicos de teste (rotulador 1) | 12 | F3.7.T3 |
| F3.7.T6 | Data Science | Rotular os eventos dos clipes públicos e registrar a contagem de risos (rotulador 1) | 6 | F3.7.T3, F1.3 |
| F3.7.T7 | Data Science | Revisar por amostragem os rótulos dos clipes públicos (rotulador 2) | 4 | F3.7.T4 (só com acionamento pelo veto), F3.7.T5, F3.7.T6 |
| F3.7.T8 | MLOps | Validar as pastas públicas e publicar os rótulos com tag | 3 | F3.7.T7, F1.4, F3.5 |
| F3.7.T9 | QA | Verificar os critérios de aceite sobre a revisão marcada dos rótulos públicos | 4 | F3.7.T8 |

<details><summary>F3.7.T1 · [Visão Computacional] Marcar a amostra de concordância nos clipes públicos (rotulador 1), quando a rodada for necessária</summary>

**Objetivo:** Entregar as marcações do rotulador 1 sobre a amostra de concordância dos clipes públicos.

**Passos previstos:**
1. Abrir no Space os quadros da amostra definida no protocolo.
2. Marcar rostos, t_s revisados e eventos sem ver as marcações do rotulador 2.
3. Exportar os arquivos sem erro de arquivo e entregá-los a quem conduz a rodada.

**Definição de pronto:** Arquivos da amostra do rotulador 1 exportados sem erro de arquivo e entregues.

**Dependências:** F3.6, F3.2, F3.3

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F3.7.T2 · [Visão Computacional] Marcar a amostra de concordância nos clipes públicos (rotulador 2), quando a rodada for necessária</summary>

**Objetivo:** Entregar as marcações do rotulador 2 sobre a mesma amostra.

**Passos previstos:**
1. Abrir no Space os quadros da mesma amostra.
2. Marcar rostos, t_s revisados e eventos sem ver as marcações do rotulador 1.
3. Exportar os arquivos sem erro de arquivo e entregá-los a quem conduz a rodada.

**Definição de pronto:** Arquivos da amostra do rotulador 2 exportados sem erro de arquivo e entregues.

**Dependências:** F3.6, F3.2, F3.3

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F3.7.T3 · [Data Science] Calcular e registrar a concordância nos clipes públicos ou registrar a referência à rodada de F3.4</summary>

**Objetivo:** Ter uma rodada aprovada, pelo limite do protocolo, antes da rotulagem de teste dos clipes públicos.

**Passos previstos:**
1. Se a rodada de F3.4 vale (mesmos rotuladores e acionamento pela falta de risos), registrar a referência a ela com os códigos de papel.
2. Se não, calcular a métrica do protocolo sobre os arquivos de T1 e T2 e registrar rodada, data, valor e resultado.
3. Abaixo do limite, revisar o protocolo com o responsável por F3.2 e pedir nova rodada.

**Definição de pronto:** Registro com uma rodada aprovada, ou com a referência à rodada de F3.4, com data anterior ao início da rotulagem de teste.

**Dependências:** F3.7.T1, F3.7.T2

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F3.7.T4 · [Visão Computacional] Rotular os rostos e os quadros revisados dos clipes públicos de desenvolvimento (rotulador 1), com acionamento pelo veto</summary>

**Objetivo:** Ter _faces.csv e a lista de t_s revisados de cada clipe público de desenvolvimento.

**Passos previstos:**
1. Rotular no Space todos os quadros amostrados de cada clipe de desenvolvimento.
2. Marcar cada t_s como revisado, inclusive sem rosto a marcar.
3. Exportar e conferir na validação de pasta do Space que não há erro de arquivo.

**Definição de pronto:** Pasta pública de desenvolvimento com _faces.csv e lista de t_s revisados de cada clipe, sem erro de arquivo.

**Dependências:** F3.7.T3

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F3.7.T5 · [Visão Computacional] Rotular os rostos e os quadros revisados dos clipes públicos de teste (rotulador 1)</summary>

**Objetivo:** Ter _faces.csv e a lista de t_s revisados de cada clipe público de teste.

**Passos previstos:**
1. Rotular no Space todos os quadros amostrados de cada clipe de teste.
2. Marcar cada t_s como revisado, inclusive sem rosto a marcar.
3. Exportar e conferir na validação de pasta do Space que não há erro de arquivo.

**Definição de pronto:** Pasta pública de teste com _faces.csv e lista de t_s revisados de cada clipe, sem erro de arquivo e com todos os t_s da grade revisados.

**Dependências:** F3.7.T3

**Estimativa sugerida:** 12 h (sugestão; validar com o time)

</details>

<details><summary>F3.7.T6 · [Data Science] Rotular os eventos dos clipes públicos e registrar a contagem de risos (rotulador 1)</summary>

**Objetivo:** Ter _eventos.csv de cada clipe público e a comparação dos risos de teste com o mínimo de F1.3.

**Passos previstos:**
1. Marcar no Space os eventos de cada clipe conforme o protocolo.
2. Conferir que cada intervalo tem pelo menos um segundo inteiro amostrado.
3. Contar risos e neutros por pasta.
4. Comparar os risos do teste com o mínimo de F1.3 e registrar 'suficiente' ou '2a inconclusivo pela regra de F1.3'.

**Definição de pronto:** _eventos.csv de todos os clipes públicos e registro com contagens e conclusão.

**Dependências:** F3.7.T3, F1.3

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F3.7.T7 · [Data Science] Revisar por amostragem os rótulos dos clipes públicos (rotulador 2)</summary>

**Objetivo:** Fazer a revisão por amostragem do protocolo sobre o trabalho do rotulador 1 antes da publicação.

**Passos previstos:**
1. Sortear a fração de quadros e de intervalos fixada no protocolo, em cada pasta.
2. Comparar no Space as marcações do rotulador 1 com a leitura do rotulador 2.
3. Registrar as divergências e as correções pedidas.
4. Conferir as correções feitas pelo rotulador 1.

**Definição de pronto:** Registro de revisão com fração revisada, divergências e correções conferidas.

**Dependências:** F3.7.T4 (só com acionamento pelo veto), F3.7.T5, F3.7.T6

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F3.7.T8 · [MLOps] Validar as pastas públicas e publicar os rótulos com tag</summary>

**Objetivo:** Ter os rótulos públicos no dataset privado, num commit marcado com tag no padrão de F3.5, só com zero erro de arquivo.

**Passos previstos:**
1. Validar cada pasta na validação de pasta do Space com o validador de F1.4 e conferir que não há erro de arquivo.
2. Subir, pela conta dona, as pastas de rótulos públicos num único commit.
3. Criar a tag no padrão de F3.5.
4. Atualizar a seção de rótulos do card com tag, commit, contagens e concordância.

**Definição de pronto:** Tag criada e card atualizado, com commit e tag registrados no PBI.

**Dependências:** F3.7.T7, F1.4, F3.5

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F3.7.T9 · [QA] Verificar os critérios de aceite sobre a revisão marcada dos rótulos públicos</summary>

**Objetivo:** Registrar passou ou não passou para os 8 critérios depois da publicação com tag.

**Passos previstos:**
1. Conferir no registro a rodada aprovada ou a referência à rodada de F3.4 (critérios 1 e 2).
2. Listar o conteúdo da tag e conferir pastas e arquivos (critério 3).
3. Rodar a validação de pasta do Space sobre a revisão marcada (critério 4).
4. Comparar a lista de t_s revisados de cada clipe com a grade (critério 5).
5. Conferir no registro a contagem de risos e a conclusão (critério 6).
6. Conferir as colunas dos arquivos (critério 7).
7. Conferir em 'hf jobs ps -a', em run_log e no registro de F2.5 que o único job anterior sobre os clipes é o de transferência (critério 8).

**Definição de pronto:** Checklist dos 8 critérios anexado ao PBI, com passou ou não passou por critério.

**Dependências:** F3.7.T8

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- labels/README.md:6-20
- docs/poc-gate.md:38-40,46-48
- tools/validar_labels.py:215-220
- bench.py:54
- Premissas P8, P13 e P29 da árvore
- arvore_v1.json: F3.6 (uma_linha e valor observável)

#### Verificação INVEST: pontos que falharam
- Independente: condicional a F3.6 e dependente de F1.3, F1.4, F3.2, F3.3 e F3.5.
- Estimável: o número de quadros só é conhecido depois de F3.6.
- Small: com acionamento pelo veto, dois conjuntos e rodada de concordância podem não caber numa sprint.

#### Premissas
- Este PBI vem da divisão do F3.6 da árvore. Disciplinas: Data Science, Visão Computacional e QA, previstas no F3.6 da árvore, mais MLOps para a publicação com tag, como em F3.4. Governança e Privacidade ficou em F3.6, com o parecer.
- As tasks T1 a T3 (rodada de concordância) só são feitas com acionamento pelo veto ou com rotuladores diferentes dos de F3.4. Caso contrário, T3 só registra a referência à rodada de F3.4.
- A task T4 (desenvolvimento) só é feita com acionamento pelo veto.
- As horas de rotulagem são sugestão proporcional às de F3.4 e dependem do número de quadros apurado em F3.6. Se a rotulagem de teste passar de 16 h, a task é dividida por grupo de clipes.
- O rotulador 1 rotula e o rotulador 2 revisa, como em F3.4.
- A publicação é executada pela conta dona.
- Estimativas (8 pontos e horas das tasks) são sugestão.

#### Pendências para sincronizar
- Area Path, Iteration Path e Responsável, só quando o PBI for acionado
- Link com a Feature F3 como pai
- Effort ou Story Points: 8 como sugestão
- Recalcular as horas de rotulagem com o número de quadros apurado em F3.6
- Tags: fase-0; condicional; corpus-publico; rotulagem

## Preview — PBI F3.8 (novo) · Adaptar a ferramenta de rotulagem do Space para ler os vídeos do destino do piloto e gravar os rótulos no destino do ADR de F6.2, com a lista de acesso dos rotuladores do piloto

#### Campos
| Campo | Conteúdo |
|---|---|
| Título | Adaptar a ferramenta de rotulagem do Space para ler os vídeos do destino do piloto e gravar os rótulos no destino do ADR de F6.2, com a lista de acesso dos rotuladores do piloto |
| Tipo | Product Backlog Item |
| Pai | F3 |
| Tags | fase-1; condicional; rotulagem; piloto; hugging-face |
| Estimativa | 5 pts (sugestão); tasks: 21 h |
| Dependências | Acionamento: F6.1 (decisão de seguir) e plano de F6.6 com rótulos de rostos ou eventos (P29), F3.3 (ferramenta de rotulagem no Space), F7.1.T1 e F7.1.T2 (destino, padrão de nome e credenciais do destino), F7.1.T4 (envio de teste com vídeo público), para F3.8.T6, F6.2.T2 (destino e acesso dos rótulos do piloto; local privado dos documentos), F6.3 (RIPD com o Space de F3.3 e os rótulos no inventário), F6.6 (rótulos previstos por culto e plano assinado), F2.6.T6 (inventário de credenciais) |
| Substitui | nenhum |

#### Descrição

Como rotulador dos cultos do piloto, identificado por código de papel  
Quero abrir no Space de rotulagem os vídeos dos cultos do piloto direto do destino de F7.1 e exportar os rótulos para o destino decidido no ADR de F6.2  
Para que F7 produza os rótulos de referência previstos no plano de F6.6 sem copiar vídeo ou rótulo do piloto para disco ou para o dataset do corpus

**Contexto:** O plano de F6.6 define, por culto do piloto, rótulos de rostos e eventos feitos na ferramenta de F3.3 (F6.6.T2 e RN03 de F6.6, F6 detalhada). A ferramenta de F3.3 lê só o dataset do corpus por tag (F3.3.T2, com a leitura de F3.5.T4) e aplica a lista de acesso de F3.1 (F3.3.T6). Os vídeos do piloto chegam a um destino privado do HF separado do corpus, com credencial de envio de escopo mínimo (F7.1.T1 e F7.1.T2, F7 detalhada). O ADR de minimização decide onde ficam os rótulos dos cultos do piloto, fora do dataset do corpus, e quem tem acesso a eles (F6.2.T2), e o card do corpus passa a dizer que vídeo e rótulo do piloto não entram nele (F6.2.T8). O vídeo de um culto só é apagado depois da rotulagem prevista no plano (F6.2.T1). O RIPD lista o Space de F3.3 entre o que vai ao HF (F6.3.T1). A revisão da árvore apontou que nenhum item dá à ferramenta a leitura do destino do piloto nem a lista de acesso dos rotuladores do piloto (consolidacao.json, item 5).

**Regras de negócio:**
- RN01 – O PBI só entra se F6.1 decidir seguir e o plano de F6.6 previr rótulos de rostos ou eventos nos cultos do piloto (P29).
- RN02 – A ferramenta lê o vídeo do destino de F7.1 para /dev/shm, com a mesma varredura absoluta de F3.3, e não grava quadro, recorte ou vídeo fora de /dev/shm (CLAUDE.md regra 1).
- RN03 – Os rótulos do piloto vão só para o destino decidido no ADR de F6.2. A exportação recusa o dataset ds-fabiopinheiro/reacao-poc-corpus como destino (F6.2.T8).
- RN04 – Os vídeos do piloto só abrem para as contas da lista de rotuladores do piloto, guardada no local privado dos documentos do piloto (F6.2.T2) e coberta pelo RIPD (F6.3). Estar na lista do PoC (F3.1) não dá acesso a vídeo do piloto.
- RN05 – O Space lê o destino do piloto com token fine-grained só de leitura nesse destino e grava rótulos com token de escrita só no destino dos rótulos. Os dois ficam no inventário de F2.6.T6, e nenhum escreve no destino dos vídeos.
- RN06 – O som fica desligado, como em F3.2 (RN08 da Feature). Esta Feature não prevê exceção à regra 5.
- RN07 – O formato dos rótulos é o de F3.2, sem id, posição de rosto ou ligação entre rostos de quadros diferentes (CLAUDE.md regras 2 e 3).
- RN08 – A ferramenta só lista vídeos do destino que seguem o padrão de nome de F7.1 e que ainda estão no destino.

**Fora de escopo:**
- Execução da rotulagem e da revisão dos cultos do piloto (item de F7 pedido pelo plano de F6.6)
- Marcação de momentos dos cultos do piloto, cuja forma o plano de F6.6 define
- Adiamento do apagamento do vídeo até o fim da rotulagem (F7.5.T2, com a regra de F6.2.T1)
- Criação do destino dos vídeos do piloto e da credencial de envio (F7.1)
- Decisão do destino, do acesso e da retenção dos rótulos do piloto (F6.2.T2 e F7.4)
- Qualquer tela do painel web na Vercel

#### Critérios de aceite

- Um rotulador da lista do piloto abre no Space um vídeo público colocado no destino de F7.1 para teste (como em F7.1.T4), rotula e exporta arquivos sem erro de arquivo no validador, e os arquivos aparecem no destino dos rótulos do ADR de F6.2 numa revisão registrada.
- Uma conta da lista do PoC que não está na lista do piloto, um visitante sem login e um pedido direto à URL de um quadro de vídeo do piloto recebem acesso negado.
- A exportação com destino no dataset ds-fabiopinheiro/reacao-poc-corpus é recusada com mensagem, e o histórico do dataset do corpus não tem arquivo do piloto.
- O log do Space registra, ao fim da sessão e depois de um erro, a varredura absoluta sem arquivo de imagem, vídeo ou áudio fora de /dev/shm.
- O inventário de F2.6.T6 lista os dois tokens do Space para o piloto com escopo e responsável, e a página de tokens da conta confirma o escopo.
- Caminho de erro: com vídeo já apagado do destino ou token sem acesso, a ferramenta mostra mensagem de erro, não abre quadro e não deixa arquivo fora de /dev/shm.

#### Tasks

| Ref | Disciplina | Título | Estimativa (h) | Dependências |
|---|---|---|---|---|
| F3.8.T1 | DevOps | Criar os tokens de leitura do destino do piloto e de escrita no destino dos rótulos do piloto para o Space e registrá-los no inventário | 3 | F7.1.T2, F6.2.T2, F2.6.T6, F3.3.T1 |
| F3.8.T2 | Visão Computacional | Fazer a ferramenta ler para /dev/shm os vídeos do destino do piloto que seguem o padrão de nome de F7.1 | 6 | F3.3.T2, F7.1.T1, F3.8.T1 |
| F3.8.T3 | MLOps | Exportar os rótulos do piloto só para o destino do ADR de F6.2 e recusar o dataset do corpus | 4 | F3.8.T2, F3.3.T4, F6.2.T2 |
| F3.8.T4 | DevOps | Aplicar ao Space a lista de acesso dos rotuladores do piloto | 1 | F3.8.T1, F6.2.T2, F6.3 |
| F3.8.T5 | Governança e Privacidade | Conferir a adaptação contra o RIPD, o ADR de F6.2 e o plano de F6.6 | 2 | F3.8.T3, F3.8.T4, F6.6 |
| F3.8.T6 | QA | Executar os testes de aceite com vídeo público no destino do piloto | 5 | F3.8.T5, F7.1.T4 |

<details><summary>F3.8.T1 · [DevOps] Criar os tokens de leitura do destino do piloto e de escrita no destino dos rótulos do piloto para o Space e registrá-los no inventário</summary>

**Objetivo:** Dar ao Space acesso de escopo mínimo aos vídeos e aos rótulos do piloto, sem escrita no destino dos vídeos.

**Passos previstos:**
1. Criar, pela conta dona, um token fine-grained só de leitura no destino de F7.1 (https://huggingface.co/docs/hub/security-tokens).
2. Criar um token fine-grained com escrita só no destino dos rótulos decidido em F6.2.T2.
3. Guardar os dois como segredos do Space, sem valor em código ou log.
4. Registrar no inventário de F2.6.T6 nome, escopo, uso e responsável de cada token.

**Definição de pronto:** Dois tokens criados com o escopo conferido na página de tokens, segredos do Space configurados e inventário de F2.6.T6 atualizado.

**Dependências:** F7.1.T2, F6.2.T2, F2.6.T6, F3.3.T1

**Estimativa sugerida:** 3 h (sugestão; validar com o time)

</details>

<details><summary>F3.8.T2 · [Visão Computacional] Fazer a ferramenta ler para /dev/shm os vídeos do destino do piloto que seguem o padrão de nome de F7.1</summary>

**Objetivo:** Abrir no Space os vídeos do piloto com a mesma leitura em memória e a mesma varredura absoluta de F3.3.

**Passos previstos:**
1. Acrescentar a origem 'destino do piloto' à leitura de F3.3.T2, com o token de leitura de T1.
2. Listar só os vídeos que seguem o padrão de nome de F7.1 e que ainda estão no destino.
3. Baixar para /dev/shm e apagar ao fim da sessão e no erro, com a varredura absoluta de F3.3.
4. Mostrar mensagem de erro, sem quadro, quando o vídeo não existir ou o token não tiver acesso.
5. Escrever os testes com vídeo sintético e abrir PR citando o PBI.

**Definição de pronto:** PR mesclado com testes da listagem, da leitura para /dev/shm e dos dois caminhos de erro, ruff check e pytest sem erro.

**Dependências:** F3.3.T2, F7.1.T1, F3.8.T1

**Estimativa sugerida:** 6 h (sugestão; validar com o time)

</details>

<details><summary>F3.8.T3 · [MLOps] Exportar os rótulos do piloto só para o destino do ADR de F6.2 e recusar o dataset do corpus</summary>

**Objetivo:** Gravar os rótulos dos cultos do piloto no destino decidido, com revisão registrada, e nunca no dataset do corpus.

**Passos previstos:**
1. Ligar a exportação de F3.3.T3 e F3.3.T4 ao destino dos rótulos do piloto quando a origem for o destino de F7.1.
2. Recusar com mensagem qualquer destino igual a ds-fabiopinheiro/reacao-poc-corpus.
3. Registrar a revisão gerada em cada exportação.
4. Escrever os testes e abrir PR citando o PBI.

**Definição de pronto:** PR mesclado com testes da exportação ao destino do piloto e da recusa do dataset do corpus, ruff check e pytest sem erro.

**Dependências:** F3.8.T2, F3.3.T4, F6.2.T2

**Estimativa sugerida:** 4 h (sugestão; validar com o time)

</details>

<details><summary>F3.8.T4 · [DevOps] Aplicar ao Space a lista de acesso dos rotuladores do piloto</summary>

**Objetivo:** Abrir os vídeos do piloto só às contas da lista do piloto.

**Passos previstos:**
1. Ler a lista de rotuladores do piloto no local privado dos documentos do piloto (F6.2.T2).
2. Configurar a verificação de conta de F3.3.T1 com uma lista por origem: corpus (F3.1) e piloto.
3. Registrar no local privado a data da aplicação e as contas, identificadas por código de papel.

**Definição de pronto:** Space com a lista do piloto aplicada à origem 'destino do piloto' e registro no local privado.

**Dependências:** F3.8.T1, F6.2.T2, F6.3

**Estimativa sugerida:** 1 h (sugestão; validar com o time)

</details>

<details><summary>F3.8.T5 · [Governança e Privacidade] Conferir a adaptação contra o RIPD, o ADR de F6.2 e o plano de F6.6</summary>

**Objetivo:** Confirmar que a adaptação trata só o que o RIPD e o ADR permitem, antes do primeiro culto rotulado.

**Passos previstos:**
1. Conferir que o Space, os tokens e o destino dos rótulos constam do inventário do RIPD de F6.3.
2. Conferir que os rótulos exportados seguem o formato de F3.2 e os rótulos previstos no plano de F6.6.
3. Conferir que o som continua desligado.
4. Registrar o resultado no local privado dos documentos do piloto.

**Definição de pronto:** Registro datado no local privado com a conferência de cada item, ou pedido de reabertura de F6.3 ou F6.6.

**Dependências:** F3.8.T3, F3.8.T4, F6.6

**Estimativa sugerida:** 2 h (sugestão; validar com o time)

</details>

<details><summary>F3.8.T6 · [QA] Executar os testes de aceite com vídeo público no destino do piloto</summary>

**Objetivo:** Registrar passou ou não passou para os 6 critérios de aceite de F3.8.

**Passos previstos:**
1. Colocar um vídeo público no destino de F7.1 pelo procedimento de F7.1.T4.
2. Rotular e exportar com uma conta da lista do piloto e validar a pasta.
3. Tentar o acesso com uma conta só da lista do PoC, sem login e por URL direta de quadro.
4. Tentar exportar para o dataset do corpus e conferir o histórico do dataset.
5. Conferir no log do Space a varredura ao fim da sessão e depois de um erro provocado.
6. Conferir o inventário de F2.6.T6 e a página de tokens.
7. Apagar o vídeo público de teste do destino.

**Definição de pronto:** Checklist dos 6 critérios anexado ao PBI, com passou ou não passou por critério e as evidências.

**Dependências:** F3.8.T5, F7.1.T4

**Estimativa sugerida:** 5 h (sugestão; validar com o time)

</details>

#### Origem do contexto
- consolidacao.json, item 5 (revisão da árvore)
- F6 detalhada: F6.2.T1, F6.2.T2, F6.2.T8, F6.3.T1, F6.6.T2 e RN03 de F6.6
- F7 detalhada: F7.1.T1, F7.1.T2, F7.1.T4 e F7.5.T2
- F3.3 desta Feature (F3.3.T1, F3.3.T2, F3.3.T6)
- CLAUDE.md (regras 1, 2, 3 e 5)

#### Verificação INVEST: pontos que falharam
- Independente: depende de F6.1, F6.2, F6.3, F6.6 e F7.1, de outras Features, e só entra na Fase 1.
- Estimável: o esforço depende do tipo de destino escolhido em F7.1.T1 e do destino dos rótulos decidido em F6.2.T2.

#### Premissas
- A revisão aceitava F3.3 ou F7.1.T1 como lugar dessa adaptação. O código fica nesta Feature porque a ferramenta é a de F3.3. F7.1.T1 decide destino e credencial e só registra o escopo de leitura pelo Space. É escolha deste detalhamento, a validar com o time.
- O PBI é separado de F3.3 para que F3.3, que o gate espera, não dependa de itens da Fase 1.
- A verificação de conta em todas as rotas, feita em F3.3.T1, permite ao app aplicar uma lista por origem de vídeo (corpus ou piloto). É dedução a confirmar no ADR de F2.4.
- Em F3.3 a exportação é por download e a conta dona publica os rótulos, sem token de escrita no Space. Aqui a exportação grava direto no destino dos rótulos do piloto, para que os rótulos do piloto não fiquem no computador do rotulador. É proposta deste detalhamento, a confirmar no ADR de F6.2.
- O teste usa vídeo público no destino, como F7.1.T4, e nunca vídeo da igreja do piloto.
- Os tokens são da conta dona, como nos demais usos desta Feature, salvo decisão diferente do ADR de F2.4.
- Estimativas (5 pontos e horas das tasks) são sugestão.

#### Pendências para sincronizar
- Link com a Feature F3 como pai
- Area Path, Iteration Path e Responsável, só quando o PBI for acionado
- F7: as tasks de rotulagem e de revisão dos cultos do piloto, pedidas pelo plano de F6.6, passam a depender de F3.8
- F7.1.T1: registrar, na definição de escopo das credenciais, a leitura do destino pelo Space de F3.8
- F7.5.T2 e F6.2.T1: o apagamento do vídeo espera a rotulagem; fica fora deste PBI
- F2.6.T6: registrar os dois tokens do Space para o piloto
- Effort ou Story Points: 5 como sugestão
- Tags: fase-1; condicional; rotulagem; piloto; hugging-face
