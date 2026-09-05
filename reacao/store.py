"""Persistência dos NÚMEROS: Supabase (REST) quando houver credenciais; senão JSON local em out/."""
from __future__ import annotations
import json
import os
from dataclasses import asdict
import httpx


class Store:
    def __init__(self, out_dir: str = "out"):
        self.url = os.environ.get("SUPABASE_URL")
        self.key = os.environ.get("SUPABASE_SERVICE_KEY")
        self.out_dir = out_dir
        os.makedirs(out_dir, exist_ok=True)

    def _post(self, table: str, rows: list[dict]):
        if not rows:
            return
        if not (self.url and self.key):
            with open(os.path.join(self.out_dir, f"{table}.json"), "a", encoding="utf-8") as fh:
                for r in rows:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            return
        r = httpx.post(f"{self.url}/rest/v1/{table}", json=rows, timeout=60,
                       headers={"apikey": self.key, "Authorization": f"Bearer {self.key}", "Prefer": "return=minimal"})
        r.raise_for_status()

    def save_windows(self, aggs):
        self._post("window_aggregate", [a.to_row() for a in aggs])

    def save_moments(self, culto, moments):
        self._post("moment", [{"culto": culto, **asdict(m)} for m in moments])

    def save_segments(self, culto, segments):
        self._post("transcript_segment", [{"culto": culto, **asdict(s)} for s in segments])

    def save_events(self, culto, events):
        self._post("event", [{"culto": culto, **asdict(e)} for e in events])

    def save_insights(self, culto, insights):
        self._post("insight", [{"culto": culto, **asdict(i)} for i in insights])

    def save_run(self, row: dict):
        self._post("run_log", [row])
