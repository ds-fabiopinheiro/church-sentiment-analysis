# Rodar no Hugging Face Jobs

Pré-requisitos: `pip install -U huggingface_hub`, `hf auth login`, créditos pré-pagos (US$ 20 cobrem o PoC).
Hardware mais barato com GPU: `t4-small` (US$ 0,40/h, cobrado por segundo).

## Corpus
```
hf upload <usuario>/reacao-poc-corpus ./samples --repo-type dataset --private
```

## Um culto
```
hf jobs uv run --flavor t4-small --timeout 3h \
  --secrets SUPABASE_URL=https://<proj>.supabase.co \
  --secrets SUPABASE_SERVICE_KEY=... \
  --secrets ANTHROPIC_API_KEY=... \
  --secrets HF_TOKEN=... \
  https://raw.githubusercontent.com/ds-fabiopinheiro/church-sentiment-analysis/main/processar_culto.py \
  --video hf://datasets/<usuario>/reacao-poc-corpus/culto01.mp4 --culto poc-01 --provider hsemotion
```
O script é UV (dependências no cabeçalho) e instala o pacote `reacao` a partir do próprio repositório.

## Teste comparativo (um job por motor)
```
for m in hsemotion libreface pyfeat; do
  hf jobs uv run --flavor t4-small --timeout 2h --secrets HF_TOKEN=... \
    https://raw.githubusercontent.com/ds-fabiopinheiro/church-sentiment-analysis/main/bench.py \
    --corpus hf://datasets/<usuario>/reacao-poc-corpus --labels hf://datasets/<usuario>/reacao-poc-corpus/labels --provider $m
done
```

## Servidor local (produção, após aprovação)
```
docker build -t ghcr.io/ds-fabiopinheiro/church-sentiment-analysis:latest .
docker run --gpus all -e SUPABASE_URL -e SUPABASE_SERVICE_KEY -v /dados/cultos:/videos:ro \
  ghcr.io/ds-fabiopinheiro/church-sentiment-analysis:latest --video /videos/2026-09-06-19h.mp4 --culto 2026-09-06-19h --provider hsemotion
```
Mesmo script, mesma imagem: o teste de paridade compara os agregados dos dois ambientes.
