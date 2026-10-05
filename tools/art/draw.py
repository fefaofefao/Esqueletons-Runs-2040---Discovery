"""Primitivas de pixel art usadas pelos geradores de arte do projeto."""
import math
import random
from PIL import Image

OUTLINE = (40, 30, 48, 255)


def rgba(c, a=255):
    return (c[0], c[1], c[2], a) if len(c) == 3 else c


def new(w, h):
    return Image.new("RGBA", (w, h), (0, 0, 0, 0))


def put(img, x, y, c):
    if 0 <= x < img.width and 0 <= y < img.height:
        img.putpixel((x, y), rgba(c))


def get(img, x, y):
    if 0 <= x < img.width and 0 <= y < img.height:
        return img.getpixel((x, y))
    return (0, 0, 0, 0)


def rect(img, x, y, w, h, c):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            put(img, xx, yy, c)


def ellipse(img, cx, cy, rx, ry, c):
    for yy in range(int(cy - ry - 1), int(cy + ry + 2)):
        for xx in range(int(cx - rx - 1), int(cx + rx + 2)):
            dx = (xx + 0.5 - cx) / max(rx, 0.01)
            dy = (yy + 0.5 - cy) / max(ry, 0.01)
            if dx * dx + dy * dy <= 1.0:
                put(img, xx, yy, c)


def line(img, x0, y0, x1, y1, c):
    x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        put(img, x0, y0, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def outline(img, c=OUTLINE, diagonal=False):
    """Adiciona contorno de 1 px por fora de todos os pixels opacos."""
    src = img.copy()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            if src.getpixel((x, y))[3] != 0:
                continue
            nb = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            if diagonal:
                nb += [(1, 1), (-1, -1), (1, -1), (-1, 1)]
            for dx, dy in nb:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and src.getpixel((nx, ny))[3] > 128:
                    img.putpixel((x, y), rgba(c))
                    break
    return img


def from_ascii(rows, palette):
    h = len(rows)
    w = len(rows[0])
    img = new(w, h)
    for y, row in enumerate(rows):
        assert len(row) == w, f"linha {y} com largura {len(row)} != {w}: {row!r}"
        for x, ch in enumerate(row):
            if ch == "." or ch == " ":
                continue
            img.putpixel((x, y), rgba(palette[ch]))
    return img


def mirror(img):
    return img.transpose(Image.FLIP_LEFT_RIGHT)


def hash01(x, y, seed=0):
    n = (x * 374761393 + y * 668265263 + seed * 2147483647) & 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((n ^ (n >> 16)) & 0xFFFF) / 65535.0


def mix(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3)) + (255,)


def bayer(x, y):
    m = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]
    return (m[y % 4][x % 4] + 0.5) / 16.0


def shade_blob(img, light, mid, dark, lx=-0.6, ly=-0.8):
    """Sombreamento por bandas para formas já preenchidas com uma cor."""
    w, h = img.size
    xs = [x for x in range(w) for y in range(h) if img.getpixel((x, y))[3]]
    ys = [y for x in range(w) for y in range(h) if img.getpixel((x, y))[3]]
    if not xs:
        return img
    cx = (min(xs) + max(xs)) / 2
    cy = (min(ys) + max(ys)) / 2
    rx = max(1, (max(xs) - min(xs)) / 2)
    ry = max(1, (max(ys) - min(ys)) / 2)
    for y in range(h):
        for x in range(w):
            if not img.getpixel((x, y))[3]:
                continue
            nx = (x + 0.5 - cx) / rx
            ny = (y + 0.5 - cy) / ry
            d = nx * lx + ny * ly
            if d > 0.45:
                img.putpixel((x, y), rgba(light))
            elif d < -0.35:
                img.putpixel((x, y), rgba(dark))
            else:
                img.putpixel((x, y), rgba(mid))
    return img


def paste(dst, src, x, y):
    dst.alpha_composite(src, (x, y))


def rng(seed):
    return random.Random(seed)


def quad_bezier(p0, p1, p2, t):
    a = (1 - t) ** 2
    b = 2 * (1 - t) * t
    c = t * t
    return (a * p0[0] + b * p1[0] + c * p2[0], a * p0[1] + b * p1[1] + c * p2[1])


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])
