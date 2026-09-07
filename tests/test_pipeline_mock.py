"""Pipeline completo com o motor mock, igual ao passo do CI: gera um mp4 sintético, roda processar_culto.py em
subprocesso e verifica que a guarda de não-persistência aprovou e que só números agregados foram gravados."""
from __future__ import annotations
import dataclasses
import importlib.util
import json
import os
import subprocess
import sys

from reacao.guard import IMAGE_EXT
from reacao.types import K_MIN, WindowAggregate

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GERADOR = os.path.join(RAIZ, "tests", "fixtures", "gerar_curto.py")
CAMPOS_JANELA = {f.name for f in dataclasses.fields(WindowAggregate)}
PERCENTUAIS = ("pct_voltados", "pct_sorrindo", "expressividade", "pct_olhos_fechados")
# sem credenciais o Store grava JSON local; sem chave de LLM não há chamada externa
AMBIENTE_ISOLADO = {**os.environ, "SUPABASE_URL": "", "SUPABASE_SERVICE_KEY": "", "ANTHROPIC_API_KEY": ""}


def _gerar(destino: str) -> str:
    spec = importlib.util.spec_from_file_location("gerar_curto", GERADOR)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.gerar(destino, segundos=10, fps=15)


def test_pipeline_mock_passa_na_guarda_e_grava_so_agregados(tmp_path):
    video = _gerar(str(tmp_path / "curto.mp4"))
    out = tmp_path / "out"
    cmd = [sys.executable, "processar_culto.py", "--video", video, "--culto", "teste", "--provider", "mock",
           "--no-transcribe", "--out", str(out)]
    r = subprocess.run(cmd, cwd=RAIZ, capture_output=True, text=True, timeout=300, env=AMBIENTE_ISOLADO)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "[guard] ok" in r.stdout

    linhas = (out / "window_aggregate.json").read_text(encoding="utf-8").splitlines()
    janelas = [json.loads(linha) for linha in linhas if linha.strip()]
    assert janelas and (out / "run_log.json").exists()
    for j in janelas:
        assert set(j) == CAMPOS_JANELA              # só o esquema agregado, nenhum campo por rosto (regras 2 e 6)
        if j["insuficiente"]:                        # k-mínimo (regra 3): janela insuficiente sai sem percentuais
            assert j["n_mensuravel"] < K_MIN and all(j[k] is None for k in PERCENTUAIS)
        else:
            assert j["n_mensuravel"] >= K_MIN

    # nenhum quadro, recorte ou vídeo novo na saída, com a mesma lista de extensões da guarda
    assert not [p for p in out.rglob("*") if p.suffix.lower() in IMAGE_EXT]
