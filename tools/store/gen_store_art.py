#!/usr/bin/env python3
"""Arte da ficha da Play Store, a partir da arte original do jogo:
  store/graphics/icon_512.png         ícone 512×512 (o mesmo do app, escala inteira)
  store/graphics/feature_1024x500.png gráfico de destaque (cena HD da tela inicial + logo)
"""
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/art"))
OUT = ROOT / "store/graphics"


def icon():
    import gen_ui
    base = gen_ui.app_icon(40)                    # 40×40 de pixel art
    big = base.resize((520, 520), Image.NEAREST)  # ×13, escala inteira
    return big.crop((4, 4, 516, 516)).convert("RGB")


def feature():
    t = ROOT / "assets/title"
    scene = Image.open(t / "bg.png").convert("RGBA")
    for layer in ("clouds.png", "castle.png", "fore.png"):
        im = Image.open(t / layer).convert("RGBA")
        scene.alpha_composite(im, (0, 0))
    rays = Image.open(t / "rays.png").convert("RGBA").resize((1640, 1640))
    glow = Image.new("RGBA", scene.size)
    glow.alpha_composite(rays, (1200 - 820, 376 - 820))
    a = glow.getchannel("A").point(lambda v: int(v * 0.3))
    glow.putalpha(a)
    scene = Image.alpha_composite(scene, glow)
    h = 500
    w = int(scene.width * h / scene.height)
    scene = scene.resize((w, h), Image.LANCZOS)
    x0 = (w - 1024) // 2
    scene = scene.crop((x0, 0, x0 + 1024, h))
    logo = Image.open(t / "logo.png").convert("RGBA")
    lw = 640
    logo = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
    scene.alpha_composite(logo, ((1024 - lw) // 2, 34))
    return scene.convert("RGB")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    icon().save(OUT / "icon_512.png")
    feature().save(OUT / "feature_1024x500.png")
    print("arte da loja ->", OUT)
