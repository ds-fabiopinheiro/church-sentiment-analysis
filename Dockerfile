# Mesma imagem para o Hugging Face Jobs (hf jobs run --flavor t4-small <imagem> ...) e para o servidor local
# (docker run --gpus all <imagem> ...). Publicar no GHCR via GitHub Actions.
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04
ENV DEBIAN_FRONTEND=noninteractive PIP_NO_CACHE_DIR=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip ffmpeg libgl1 libglib2.0-0 git \
    && rm -rf /var/lib/apt/lists/* && pip3 install uv
WORKDIR /app
COPY pyproject.toml ./
COPY reacao ./reacao
COPY processar_culto.py bench.py ./
RUN uv pip install --system ".[gpu,llm]"
ENTRYPOINT ["python3", "processar_culto.py"]
