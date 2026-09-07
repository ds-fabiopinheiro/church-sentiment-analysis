# Fixtures de teste

`curto.mp4` não é versionado (`*.mp4` está no `.gitignore`). O CI o gera nesse caminho, com o comando abaixo,
antes de rodar o pipeline; o teste `tests/test_pipeline_mock.py` gera uma cópia própria no diretório temporário
do pytest (`tmp_path`). Para gerar à mão:

```
uv run python tests/fixtures/gerar_curto.py tests/fixtures/curto.mp4
```

Conteúdo: 10 s a 15 fps, 320x240, quadros de cor sólida com o número do quadro; não há rosto. Serve para
exercitar ingestão, guarda de não-persistência, agregação e gravação com o motor `mock`, que fabrica as
observações. Não serve para medir detecção nem expressão.
