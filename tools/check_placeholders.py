#!/usr/bin/env python3
"""Procura placeholders como [EMAIL], [URL] ou [NOME DA PRODUTORA] no que vai
para a loja e para o jogo.

  python3 tools/check_placeholders.py            # build de debug: só relata (sai 0)
  python3 tools/check_placeholders.py --release  # build de release: falha se houver algum
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# O que é publicado ou empacotado. Documentos de trabalho (AGENTS.md, docs/DECISOES.md...) ficam de fora.
SCAN = [
    "config",
    "data",
    "i18n",
    "export_presets.cfg",
    "project.godot",
    "PLAY_CONSOLE.md",
    "store",
    "privacy",
    "app-ads.txt",
]
TEXT_EXT = {".json", ".csv", ".cfg", ".godot", ".md", ".txt", ".html", ".xml", ".po"}
PATTERN = re.compile(r"\[(?:[A-ZÀ-Ý][A-ZÀ-Ý0-9_]*)(?: [A-ZÀ-Ý0-9_]+)*\]")


def files():
    for entry in SCAN:
        p = ROOT / entry
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and f.suffix in TEXT_EXT:
                    yield f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--release", action="store_true")
    args = ap.parse_args()
    found = []
    for f in files():
        for n, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for m in PATTERN.finditer(line):
                found.append(f"{f.relative_to(ROOT)}:{n}: {m.group(0)}")
    if not found:
        print("check_placeholders: nenhum placeholder.")
        return 0
    for item in found:
        print(("ERRO " if args.release else "aviso ") + item)
    if args.release:
        print(f"check_placeholders: {len(found)} placeholder(s). Preencha config/publisher.json antes do release.")
        return 1
    print(f"check_placeholders: {len(found)} placeholder(s) (permitido no debug).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
