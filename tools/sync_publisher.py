#!/usr/bin/env python3
"""Sincroniza config/publisher.json -> export_presets.cfg, project.godot e os
documentos da loja (política, app-ads.txt, fichas e PLAY_CONSOLE.md).

  python3 tools/sync_publisher.py                  # aplica
  python3 tools/sync_publisher.py --check          # só confere (falha se divergir)
  python3 tools/sync_publisher.py --version-code N # define version/code (CI usa o nº do build)
  python3 tools/sync_publisher.py --publisher-id-from-env
      # release: se o ID de editor ainda for placeholder, tira do ADMOB_APP_ID
      # (ca-app-pub-<16 dígitos>~... -> pub-<16 dígitos>) só no runner, sem commit
"""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--version-code", type=int)
    ap.add_argument("--publisher-id-from-env", action="store_true")
    args = ap.parse_args()
    pub_path = ROOT / "config" / "publisher.json"
    pub = json.loads(pub_path.read_text(encoding="utf-8"))
    if args.publisher_id_from_env and str(pub["admob"].get("publisher_id", "")).startswith("["):
        m = re.fullmatch(r"ca-app-pub-(\d{16})~\d+", os.environ.get("ADMOB_APP_ID", "").strip())
        if not m:
            print("sync_publisher: ADMOB_APP_ID ausente ou fora do formato ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY")
            return 1
        pub["admob"]["publisher_id"] = f"pub-{m.group(1)}"
        text = pub_path.read_text(encoding="utf-8")
        text = re.sub(r'"publisher_id": "\[[^"]*\]"', f'"publisher_id": "pub-{m.group(1)}"', text)
        pub_path.write_text(text, encoding="utf-8")
        print("sync_publisher: ID de editor tirado do ADMOB_APP_ID")
    presets_path = ROOT / "export_presets.cfg"
    project_path = ROOT / "project.godot"
    presets = presets_path.read_text(encoding="utf-8")
    project = project_path.read_text(encoding="utf-8")
    new_presets = presets
    new_presets = re.sub(r'package/unique_name="[^"]*"', f'package/unique_name="{pub["package_name"]}"', new_presets)
    new_presets = re.sub(r'package/name="[^"]*"', f'package/name="{pub["game_name"]}"', new_presets)
    new_presets = re.sub(r'version/name="[^"]*"', f'version/name="{pub["version_name"]}"', new_presets)
    if args.version_code is not None:
        new_presets = re.sub(r"version/code=\d+", f"version/code={args.version_code}", new_presets)
    new_project = re.sub(r'config/version="[^"]*"', f'config/version="{pub["version_name"]}"', project)
    new_project = re.sub(r'config/name="[^"]*"', f'config/name="{pub["store_title"]}"', new_project)
    changed = new_presets != presets or new_project != project
    if args.check:
        if changed:
            print("sync_publisher: export_presets.cfg/project.godot divergem de config/publisher.json. Rode tools/sync_publisher.py.")
            return 1
        print("sync_publisher: OK")
        return 0
    presets_path.write_text(new_presets, encoding="utf-8")
    project_path.write_text(new_project, encoding="utf-8")
    print("sync_publisher: aplicado" if changed else "sync_publisher: nada a mudar")
    # documentos gerados a partir do publisher.json (política, app-ads.txt, ficha da loja, Play Console)
    for gen in ["tools/store/gen_store_docs.py", "tools/store/gen_play_console.py"]:
        if subprocess.run([sys.executable, str(ROOT / gen)], cwd=ROOT).returncode != 0:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
