#!/usr/bin/env python3
"""Sincroniza config/publisher.json -> export_presets.cfg, project.godot e os
documentos da loja (política, app-ads.txt, fichas e PLAY_CONSOLE.md).

  python3 tools/sync_publisher.py                  # aplica
  python3 tools/sync_publisher.py --check          # só confere (falha se divergir)
  python3 tools/sync_publisher.py --version-code N # define version/code (CI usa o nº do build)
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--version-code", type=int)
    args = ap.parse_args()
    pub = json.loads((ROOT / "config" / "publisher.json").read_text(encoding="utf-8"))
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
