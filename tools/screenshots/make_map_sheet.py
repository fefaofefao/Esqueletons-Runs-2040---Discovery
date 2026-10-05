#!/usr/bin/env python3
"""Folha de revisão dos mapas (docs/mapas_sheet.png): renderiza todos os mapas
externos com tools/screenshots/map_sheet.tscn (zonas de selvagens e faixa de
idade marcadas) e monta uma grade na ordem da história.

Uso: python3 tools/screenshots/make_map_sheet.py   (precisa de godot e xvfb-run)
"""
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
ORDER = ["praia_despertar", "vila_mare", "rota_1", "tunel_raizes", "raizal", "bosque_velho",
         "rota_2", "brasal", "mina_funda", "rota_3", "brejo", "caldeirao", "rota_4", "ossorio", "quartel",
         "rota_5", "geada", "jardim_gelo", "rota_6", "palmeiral", "templo_areias", "castelo_portao", "castelo_salao", "sala_trono"]


def main():
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(["xvfb-run", "-a", "godot", "--rendering-driver", "opengl3", "res://tools/screenshots/map_sheet.tscn",
                        "--", f"--out={td}", "--maps=" + ",".join(ORDER)], cwd=ROOT, check=True, capture_output=True)
        ims = [(m, Image.open(Path(td) / f"{m}.png").convert("RGB")) for m in ORDER if (Path(td) / f"{m}.png").exists()]
        scale, cols = 0.5, 4
        ims = [(m, i.resize((int(i.width * scale), int(i.height * scale)))) for m, i in ims]
        cw = max(i.width for _, i in ims)
        ch = max(i.height for _, i in ims) + 14
        rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * (cw + 8), rows * (ch + 8)), (24, 22, 30))
        d = ImageDraw.Draw(sheet)
        for k, (m, i) in enumerate(ims):
            x, y = (k % cols) * (cw + 8), (k // cols) * (ch + 8)
            d.text((x + 2, y + 1), f"{k + 1:02d} {m}", fill=(240, 236, 220))
            sheet.paste(i, (x, y + 14))
        out = ROOT / "docs/mapas_sheet.png"
        sheet.save(out, optimize=True)
        print(f"{out.relative_to(ROOT)}: {len(ims)} mapas, {sheet.width}x{sheet.height}")


if __name__ == "__main__":
    main()
