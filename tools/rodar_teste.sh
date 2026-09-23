#!/usr/bin/env bash
# Executa o teste do PoC de ponta a ponta numa sessão nova: prepara o ambiente em CPU, baixa o corpus privado,
# confere os rótulos e roda o bench. Reúne o que custou tempo descobrir; não improvise em cima.
#
#   bash tools/rodar_teste.sh
#   DEV_CLIPES=igreja_simples_07,igreja_simples_08 bash tools/rodar_teste.sh
#
# Exige HF_TOKEN no ambiente. Uma sessão já em execução NÃO enxerga variável cadastrada depois: abra uma nova.
set -euo pipefail
DATASET=${DATASET:-ds-fabiopinheiro/reacao-poc-corpus}
SUB=${SUB:-pib}
CORPUS=${CORPUS:-samples/corpus}
LABELS=${LABELS:-samples/corpus/labels}
PROVIDER=${PROVIDER:-hsemotion}
# clipes usados no desenvolvimento: ficam fora da medição para o teste não ser contaminado
DEV_CLIPES=${DEV_CLIPES:-igreja_simples_07,igreja_simples_08,igreja_simples_09,igreja_simples_10}
PY=.venv/bin/python

[ -n "${HF_TOKEN:-}" ] || { echo "HF_TOKEN ausente. Cadastre no ambiente e abra uma sessão NOVA."; exit 1; }

echo "== 1. ambiente em CPU =="
[ -x "$PY" ] || uv venv
# onnxruntime (não o -gpu) e torch de CPU; `uv run` sem --no-sync re-sincroniza e desinstala estes pacotes,
# por isso todo o resto do script chama $PY diretamente.
uv pip install -q -e ".[dev]" opencv-python-headless onnxruntime insightface hsemotion-onnx faster-whisper
uv pip install -q torch torchvision --index-url https://download.pytorch.org/whl/cpu
uv pip install -q sixdrepnet

echo "== 2. modelo de expressão =="
# o pacote baixa de github.com/.../blob/...?raw=true, que o proxy recusa com 403; raw.githubusercontent funciona
mkdir -p ~/.hsemotion
[ -s ~/.hsemotion/enet_b0_8_best_afew.onnx ] || curl -fsSL -o ~/.hsemotion/enet_b0_8_best_afew.onnx \
  https://raw.githubusercontent.com/HSE-asavchenko/face-emotion-recognition/main/models/affectnet_emotions/onnx/enet_b0_8_best_afew.onnx

echo "== 3. corpus privado (não versionado; samples/ está no .gitignore) =="
$PY - "$DATASET" "$CORPUS" <<'PYEOF'
import sys
from huggingface_hub import snapshot_download
print(snapshot_download(repo_id=sys.argv[1], repo_type="dataset", local_dir=sys.argv[2]))
PYEOF
CORPUS_SUB="$CORPUS/$SUB"; [ -d "$CORPUS_SUB" ] || CORPUS_SUB="$CORPUS"
ls -1 "$CORPUS_SUB"/*.mp4 | wc -l | xargs echo "clipes baixados:"

echo "== 4. rótulos =="
if [ -d "$LABELS" ]; then
  $PY tools/validar_labels.py --labels "$LABELS" --corpus "$CORPUS_SUB"
else
  echo "pasta de rótulos ausente ($LABELS)."
  echo "Sem rótulos o bench não mede os critérios 1 e 2. Para preparar os arquivos:"
  echo "  $PY tools/preparar_rotulagem.py --corpus $CORPUS_SUB --labels $LABELS --excluir $DEV_CLIPES"
  exit 2
fi

echo "== 5. bench, sem os clipes de desenvolvimento =="
$PY bench.py --corpus "$CORPUS_SUB" --labels "$LABELS" --provider "$PROVIDER" --flavor local \
  --excluir "$DEV_CLIPES" --out out/bench
echo
echo "CSV em out/bench/bench_$PROVIDER.csv. A linha TOTAL é a do gate (docs/poc-gate.md)."
echo "Para medir o critério 5 na GPU: hf jobs uv run --flavor t4-small --timeout 1h --secrets HF_TOKEN \\"
echo "  https://raw.githubusercontent.com/ds-fabiopinheiro/church-sentiment-analysis/main/processar_culto.py \\"
echo "  --video hf://datasets/$DATASET/$SUB/igreja_simples_11.mp4 --culto poc-11 --provider $PROVIDER --stdout"
