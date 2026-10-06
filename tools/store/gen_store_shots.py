#!/usr/bin/env python3
"""Capturas da ficha da Play Store nos 3 idiomas (paisagem, 1280×720).

Roda o jogo de verdade (tools/screenshots/capture.tscn --store) em cada idioma e
amplia as telas de jogo (320×180) em escala inteira ×4, sem suavizar o pixel.
Rode de novo sempre que a interface ou o conteúdo mostrado mudar, para a ficha
retratar o jogo atual (política do Google Play).

Uso: python3 tools/store/gen_store_shots.py   (precisa de godot e xvfb-run)
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "store/screenshots"
LANGS = ["pt_BR", "en", "es"]
SHOTS = {
    "01_titulo": "01_titulo",
    "s2_vila": "02_vila",
    "s3_batalha": "03_batalha",
    "s4_aniversario": "04_aniversario",
    "s5_ossario": "05_ossario",
    "s6_revelacao": "06_revelacao",
    "s7_trono": "07_trono",
}
SIZE = (1280, 720)


def capture(lang: str, tmp: Path) -> None:
    cmd = ["xvfb-run", "-a", "-s", "-screen 0 1280x720x24", "godot", "--rendering-driver", "opengl3",
           "--resolution", "1280x720", "--path", str(ROOT), "res://tools/screenshots/capture.tscn",
           "--", f"--out={tmp}", "--store", f"--lang={lang}"]
    subprocess.run(cmd, check=True, timeout=600, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main() -> int:
    for lang in LANGS:
        with tempfile.TemporaryDirectory() as d:
            tmp = Path(d)
            capture(lang, tmp)
            dest = OUT / lang
            dest.mkdir(parents=True, exist_ok=True)
            for src, name in SHOTS.items():
                p = tmp / f"{src}.png"
                if not p.exists():
                    print(f"ERRO {lang}: captura {src} não saiu")
                    return 1
                im = Image.open(p).convert("RGB")
                if im.size != SIZE:
                    k = SIZE[0] // im.width
                    if im.width * k != SIZE[0] or im.height * k != SIZE[1]:
                        print(f"ERRO {lang}: {src} tem {im.size}, não amplia em escala inteira para {SIZE}")
                        return 1
                    im = im.resize(SIZE, Image.NEAREST)
                im.save(dest / f"{name}.png")
            print(f"{lang}: {len(SHOTS)} capturas em {dest.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    if not shutil.which("godot"):
        print("godot não encontrado no PATH")
        sys.exit(1)
    sys.exit(main())
