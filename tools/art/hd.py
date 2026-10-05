"""Utilitários de arte em alta resolução (logo e tela inicial): máscaras, dilatação
redonda, gradientes, sombras e brilho. Usa Pillow + numpy."""
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONTS = Path(__file__).resolve().parent / "fonts"


def hexc(h, a=255):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


def font(name, size, weight=None):
    f = ImageFont.truetype(str(FONTS / name) if not str(name).startswith("/") else name, size)
    if weight is not None:
        f.set_variation_by_axes([weight])
    return f


def text_mask(text, f, tracking=0):
    """Máscara L do texto, letra a letra com espaçamento extra."""
    asc, desc = f.getmetrics()
    w = int(sum(f.getlength(c) + tracking for c in text)) + 40
    m = Image.new("L", (w, asc + desc + 40), 0)
    d = ImageDraw.Draw(m)
    x = 20
    for c in text:
        d.text((x, 20), c, font=f, fill=255)
        x += f.getlength(c) + tracking
    return m.crop(m.getbbox())


def pad(mask, p):
    out = Image.new("L", (mask.width + 2 * p, mask.height + 2 * p), 0)
    out.paste(mask, (p, p))
    return out


def dilate(mask, r):
    """Dilatação circular de raio r (px), com borda suave."""
    if r <= 0:
        return mask.copy()
    a = np.asarray(mask, dtype=np.float32) / 255.0
    out = a.copy()
    h, w = a.shape
    ri = int(math.ceil(r))
    for dy in range(-ri, ri + 1):
        for dx in range(-ri, ri + 1):
            d = math.hypot(dx, dy)
            if d > r + 0.5:
                continue
            k = min(1.0, r + 0.5 - d)
            sy0, sy1 = max(0, -dy), min(h, h - dy)
            sx0, sx1 = max(0, -dx), min(w, w - dx)
            src = a[sy0:sy1, sx0:sx1] * k
            dst = out[sy0 + dy:sy1 + dy, sx0 + dx:sx1 + dx]
            np.maximum(dst, src, out=dst)
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), "L")


def shift(mask, dx, dy):
    out = Image.new("L", mask.size, 0)
    out.paste(mask, (dx, dy))
    return out


def subtract(a, b):
    return Image.fromarray(np.clip(np.asarray(a, np.int16) - np.asarray(b, np.int16), 0, 255).astype(np.uint8), "L")


def union(*masks):
    arr = np.asarray(masks[0])
    for m in masks[1:]:
        arr = np.maximum(arr, np.asarray(m))
    return Image.fromarray(arr.astype(np.uint8), "L")


def scale_alpha(mask, k):
    return Image.fromarray(np.clip(np.asarray(mask, np.float32) * k, 0, 255).astype(np.uint8), "L")


def vgrad(size, stops, top=0, height=None):
    """Gradiente vertical RGBA. stops: [(t, (r,g,b,a)), ...]."""
    w, h = size
    height = height or h
    arr = np.zeros((h, w, 4), np.float32)
    ts = np.clip((np.arange(h) - top) / max(1, height - 1), 0, 1)
    pos = [s[0] for s in stops]
    for ch in range(4):
        vals = [s[1][ch] if len(s[1]) > ch else 255 for s in stops]
        col = np.interp(ts, pos, vals)
        arr[:, :, ch] = col[:, None]
    return Image.fromarray(arr.astype(np.uint8), "RGBA")


def fill(mask, color_or_img):
    """Camada RGBA: cor/imagem recortada pela máscara."""
    if isinstance(color_or_img, Image.Image):
        src = color_or_img.resize(mask.size) if color_or_img.size != mask.size else color_or_img
    else:
        src = Image.new("RGBA", mask.size, color_or_img)
    out = src.copy()
    a = np.asarray(src.getchannel("A"), np.float32) * (np.asarray(mask, np.float32) / 255.0)
    out.putalpha(Image.fromarray(a.astype(np.uint8), "L"))
    return out


def glow(mask, color, radius, strength=1.0):
    blurred = mask.filter(ImageFilter.GaussianBlur(radius))
    return fill(scale_alpha(blurred, strength), color)


def comp(base, layer, xy=(0, 0)):
    base.alpha_composite(layer, xy)
    return base


def supersample(draw_fn, size, ss=3):
    """Desenha em ss× e reduz com LANCZOS (bordas suaves)."""
    big = Image.new("RGBA", (size[0] * ss, size[1] * ss), (0, 0, 0, 0))
    draw_fn(big, ss)
    return big.resize(size, Image.LANCZOS)


def skew(img, k):
    """Inclina para a direita (itálico) mantendo a base."""
    w, h = img.size
    extra = int(abs(k) * h) + 2
    out = img.transform((w + extra, h), Image.AFFINE, (1, k, -extra if k < 0 else 0, 0, 1, 0), Image.BICUBIC)
    return out
