# Replicação on-premises (após a aprovação da igreja)

Objetivo: rodar no templo exatamente o que rodou no Hugging Face Jobs, com a mesma imagem Docker,
sem nenhuma dependência de nuvem além do Supabase (agregados) e, opcionalmente, da API de linguagem.

## 1. Dimensionamento a partir das medições do PoC
Preencher com os números do `run_log` dos jobs na T4 small (PBI-103/TSK-207):

| Medida na T4 small | Valor medido |
|---|---|
| Segundos de GPU por hora de vídeo (detecção + expressão) | |
| Rostos mensuráveis por quadro (mediana) | |
| Pico de memória de GPU (GB) | |
| Custo por culto (US$) | |

Fator aproximado de desempenho em inferência FP16 em relação à T4 (ordem de grandeza; medir na prática):

| GPU | Memória | Fator vs T4 | Serve para | Custo estimado (cotar; set/2026) |
|---|---|---|---|---|
| RTX 4070 / 4070 Super | 12 GB | ~2–3× | lote semanal de 5 cultos (fase 1) | R$ 4–5 mil (placa) |
| RTX 4070 Ti Super | 16 GB | ~3–4× | lote + folga para 4K e batch maior | R$ 6–7 mil |
| RTX 4090 / RTX 3090 usada | 24 GB | ~5–8× / ~3–4× | tempo real com 3 câmeras a 1–2 fps (fase seguinte) | R$ 12–16 mil / R$ 5–7 mil |
| Jetson Orin (AGX/NX) | 16–64 GB unificada | ~0,5–2× | edge compacto, baixo consumo; validar throughput | R$ 8–15 mil |

Regra: se o PoC mediu ≤ 2 h de T4 por hora de vídeo, uma RTX 4070 processa os 5 cultos da semana em
menos de uma noite. Só a fase seguinte (tempo real) justifica 24 GB.

Estação completa (CPU 8 núcleos, 32 GB RAM, SSD 1 TB, fonte, gabinete): somar R$ 5–7 mil. Preços são
estimativas para orientar a cotação; registrar a cotação real com data.

## 2. Instalação (Ubuntu 24.04)
```
sudo apt install -y ubuntu-drivers-common && sudo ubuntu-drivers install     # driver NVIDIA
# Docker Engine (docs.docker.com/engine/install/ubuntu) e NVIDIA Container Toolkit
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
# (repositório conforme docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
sudo apt install -y nvidia-container-toolkit && sudo nvidia-ctk runtime configure --runtime=docker && sudo systemctl restart docker
docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi   # verificação
```

## 3. Mesma imagem, mesmo comando
```
docker pull ghcr.io/ds-fabiopinheiro/church-sentiment-analysis:latest
docker run --rm --gpus all \
  -e SUPABASE_URL -e SUPABASE_SERVICE_KEY -e ANTHROPIC_API_KEY \
  -v /dados/cultos:/videos:ro --shm-size=8g \
  ghcr.io/ds-fabiopinheiro/church-sentiment-analysis:latest --video /videos/2026-09-06-19h.mp4 --culto 2026-09-06-19h --provider hsemotion
```
`--shm-size` importa: recortes temporários vivem em `/dev/shm` (regra 1 do CLAUDE.md), nunca em disco.
Se a igreja preferir não usar API de linguagem em nuvem, basta não passar `-e ANTHROPIC_API_KEY`: sem a chave,
os momentos são segmentados por heurística de palavras-chave (`reacao/moments.py`) e os insights usam o modelo
de frase fixo (`reacao/insights.py`), ambos locais e sujeitos ao lint. Suporte a um modelo de linguagem local
(Ollama com qwen/llama) ainda não existe; se for implementado, a qualidade dos insights deve ser reavaliada com o pregador.

## 4. Teste de paridade (critério de aceite de PBI-103 e PBI-106)
1. Processar o mesmo vídeo público do corpus na HF (`t4-small`) e no servidor local.
2. Comparar `window_aggregate` janela a janela: diferença ≤ 1 p.p. em todos os percentuais e mesmo `n`.
3. Registrar tempo de GPU nos dois ambientes; o fator medido alimenta a tabela da seção 1.

## 5. Operação semanal
- Gravação do OBS copiada para `/dados/cultos/<culto>.mp4` ao fim de cada culto (Produção).
- `cron` de segunda 03:00: processa os cultos do fim de semana; relatório disponível para revisão até 11:00.
- Após o job, o mp4 segue a política de retenção da igreja; o sistema não guarda cópia (guard verifica).
- Atualização da imagem: `docker pull` após cada release marcada no GitHub; nunca `latest` sem tag em produção.

## 6. O que não muda entre HF e on-premises
Código, modelo, k-mínimo, lint, schema do Supabase. O que muda: origem do vídeo (dataset HF → pasta local),
segredos (via `--secret` → via `-e`), e a base legal (nuvem → local), tratada no RIPD.
