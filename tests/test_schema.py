"""Nenhuma tabela pode ter campo por pessoa (regra 6 do CLAUDE.md)."""
import glob
import re

BANNED = ["embedding", "face_id", "track_id", "person", "pessoa", "assento", "seat", "cpf", "member_id", "membro_id"]


def test_migrations_have_no_per_person_fields():
    for path in glob.glob("supabase/migrations/*.sql"):
        sql = re.sub(r"--[^\n]*", "", open(path, encoding="utf-8").read().lower())   # ignora comentários
        for b in BANNED:
            assert not re.search(rf"\b{b}\b", sql), f"{path}: campo proibido '{b}'"
