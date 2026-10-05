"""Leitor mínimo da fonte BMFont gerada, para pré-visualizações e para o logo."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
FONT_DIR = ROOT / "assets" / "fonts"


class PixFont:
    def __init__(self):
        self.page = Image.open(FONT_DIR / "pixel.png").convert("RGBA")
        self.chars = {}
        self.line_h = 12
        for line in (FONT_DIR / "pixel.fnt").read_text(encoding="utf-8").splitlines():
            if line.startswith("common "):
                for kv in line.split()[1:]:
                    k, v = kv.split("=")
                    if k == "lineHeight":
                        self.line_h = int(v)
            if not line.startswith("char "):
                continue
            d = {}
            for kv in line.split()[1:]:
                k, v = kv.split("=")
                d[k] = int(v)
            self.chars[chr(d["id"])] = d

    def width(self, text):
        return sum(self.chars.get(c, self.chars["?"])["xadvance"] for c in text)

    def draw(self, img, x, y, text, color=(255, 255, 255, 255)):
        for c in text:
            d = self.chars.get(c, self.chars["?"])
            glyph = self.page.crop((d["x"], d["y"], d["x"] + d["width"], d["y"] + d["height"]))
            tint = Image.new("RGBA", glyph.size, color)
            img.paste(tint, (x, y), glyph)
            x += d["xadvance"]
        return x
