#!/usr/bin/env python3
"""Confere o manifesto de um APK com `aapt2 dump badging`: targetSdk, minSdk,
package e permissões (só INTERNET, ACCESS_NETWORK_STATE e AD_ID).

Uso: python3 tools/check_manifest.py caminho/aapt2 build/app.apk
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    "android.permission.INTERNET",
    "android.permission.ACCESS_NETWORK_STATE",
    "com.google.android.gms.permission.AD_ID",
}


def main():
    aapt2, apk = sys.argv[1], sys.argv[2]
    out = subprocess.run([aapt2, "dump", "badging", apk], capture_output=True, text=True, check=True).stdout
    pub = json.loads((ROOT / "config" / "publisher.json").read_text(encoding="utf-8"))
    errors = []
    pkg = re.search(r"package: name='([^']+)'", out).group(1)
    target = int(re.search(r"targetSdkVersion:'(\d+)'", out).group(1))
    min_sdk = int(re.search(r"(?:minSdkVersion|sdkVersion):'(\d+)'", out).group(1))
    perms = set(re.findall(r"uses-permission: name='([^']+)'", out))
    print(f"package={pkg} minSdk={min_sdk} targetSdk={target}")
    print("permissões:", ", ".join(sorted(perms)))
    if pkg != pub["package_name"]:
        errors.append(f"package {pkg} != {pub['package_name']}")
    if target < 35:
        errors.append(f"targetSdk {target} < 35")
    if min_sdk != 24:
        errors.append(f"minSdk {min_sdk} != 24")
    # permissões que o próprio Android adiciona a apps com targetSdk alto são internas do app
    extra = {p for p in perms - ALLOWED if not p.endswith(".DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION")}
    if extra:
        errors.append(f"permissões não permitidas: {sorted(extra)}")
    for e in errors:
        print("ERRO", e)
    print("check_manifest:", "falhou" if errors else "OK")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
