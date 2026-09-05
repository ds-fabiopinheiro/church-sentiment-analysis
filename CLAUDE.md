# CLAUDE.md — regras do repositório (lidas pelo Claude Code antes de qualquer alteração)

## O que este sistema é
Pipeline em lote que lê um vídeo de culto, mede a reação *observada* da plateia de forma
agregada e anônima e a liga ao trecho da mensagem (transcrição do púlpito). Só vídeo e imagem.
Nenhum áudio de plateia. Roda no Hugging Face Jobs (PoC) e em servidor local com GPU (produção),
com o mesmo script e a mesma imagem Docker.

## Regras que nunca mudam (falha de CI se violadas)
1. **Nenhum quadro, recorte ou vídeo em disco.** Recortes temporários só em `/dev/shm`. `reacao/guard.py`
   bloqueia `cv2.imwrite` e `PIL.Image.save` fora de `/dev/shm` e verifica o sistema de arquivos ao fim.
2. **Nenhuma identificação.** Proibido carregar modelo de reconhecimento facial, calcular embedding,
   rastrear rostos entre quadros ou persistir qualquer id por rosto. O detector é carregado com
   `allowed_modules=["detection"]` e há teste que falha se um módulo de reconhecimento aparecer.
3. **k-mínimo.** Janela com menos de 10 rostos *mensuráveis* (altura ≥ 64 px) sai com `insuficiente=True`
   e sem percentuais. Nenhuma métrica por assento, setor pequeno ou pessoa.
4. **Linguagem controlada.** Todo texto para pastores passa por `reacao/lint.py`: proibido "sentiram",
   "entediad", "emocionad", "estavam felizes/tristes" etc. referindo-se à congregação; obrigatório minuto,
   momento, trecho citado e sinais.
5. **Sem áudio de plateia.** A única entrada de áudio é a trilha do arquivo, usada só para transcrever o púlpito.
6. **Schema sem pessoa.** Tabelas do Supabase não têm campo por pessoa; `tests/test_schema.py` verifica.

## Como rodar
- Local (CPU, para testes): `uv run processar_culto.py --video samples/x.mp4 --culto teste --provider hsemotion --out out/`
- Hugging Face Jobs (GPU T4, US$ 0,40/h): ver `docs/hf-jobs.md`.
- Testes: `uv run pytest -q`.

## Estilo
- Português nos textos de produto, inglês só em identificadores de biblioteca.
- Funções pequenas, tipos explícitos, sem frameworks além do necessário.
- Antes de abrir PR: `ruff check`, `pytest`, e o PR cita o PBI (ex.: `PBI-104`).
