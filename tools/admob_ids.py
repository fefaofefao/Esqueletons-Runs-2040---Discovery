#!/usr/bin/env python3
"""Grava os IDs reais do AdMob no build de release, a partir de variáveis de
ambiente (GitHub Secrets). Nunca rode isto num commit: config/admob.json está
no .gitignore.

  ADMOB_APP_ID, ADMOB_BANNER_ID, ADMOB_INTERSTITIAL_ID, ADMOB_REWARDED_ID

- config/admob.json: lido pelo autoload Ads no release (scripts/autoload/ads.gd);
- project.godot [admob] general/android/app_id: o plugin escreve no manifesto.
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEYS = {"app_id": "ADMOB_APP_ID", "banner": "ADMOB_BANNER_ID", "interstitial": "ADMOB_INTERSTITIAL_ID", "rewarded": "ADMOB_REWARDED_ID"}


def main() -> int:
    ids = {k: os.environ.get(v, "").strip() for k, v in KEYS.items()}
    missing = [KEYS[k] for k, v in ids.items() if not v]
    if missing:
        print("admob_ids: Secrets ausentes:", ", ".join(missing))
        return 1
    if "3940256099942544" in "".join(ids.values()):
        print("admob_ids: os Secrets contêm IDs de TESTE do Google; use os IDs reais do seu AdMob.")
        return 1
    (ROOT / "config/admob.json").write_text(json.dumps(ids, indent=1) + "\n", encoding="utf-8")
    p = ROOT / "project.godot"
    s = p.read_text(encoding="utf-8")
    line = f'general/android/app_id="{ids["app_id"]}"'
    if re.search(r"^general/android/app_id=.*$", s, re.M):
        s = re.sub(r"^general/android/app_id=.*$", line, s, flags=re.M)
    elif "[admob]" in s:
        s = s.replace("[admob]\n", "[admob]\n\n" + line + "\n", 1)
    else:
        s = s.rstrip("\n") + "\n\n[admob]\n\n" + line + "\n"
    p.write_text(s, encoding="utf-8")
    print("admob_ids: IDs reais gravados (config/admob.json e project.godot)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
