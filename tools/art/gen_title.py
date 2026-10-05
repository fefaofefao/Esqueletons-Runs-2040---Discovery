#!/usr/bin/env python3
"""Gera o logo HD ("Esqueletons Runs 2040" + "Edition — Discovery") e as camadas
da tela inicial (céu de pôr do sol retrô, sol listrado, mar, ilha com o castelo
do Rei Esqueleto, nuvens, coqueiros e raios de luz).

Saída: assets/title/*.png. Fontes usadas só para desenhar o logo (não vão no
jogo): Lilita One e Orbitron, ambas SIL OFL 1.1 (tools/art/fonts/).
"""
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from hd import (comp, dilate, fill, font, glow, hexc, pad, scale_alpha, shift, skew,
                subtract, supersample, text_mask, union, vgrad)

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "title"

INK = hexc("#170f2e")
INK_DEEP = hexc("#0b0719")
BONE = [(0.0, hexc("#fffef6")), (0.55, hexc("#f3ead2")), (1.0, hexc("#c9b993"))]
FIRE = [(0.0, hexc("#fff3a0")), (0.4, hexc("#ffb43a")), (0.75, hexc("#ff5a2c")), (1.0, hexc("#d8213f"))]
NEON = [(0.0, hexc("#f2ffff")), (0.35, hexc("#7ff6ff")), (0.7, hexc("#22c8ee")), (1.0, hexc("#1673c9"))]
GOLD = [(0.0, hexc("#fff6c8")), (0.5, hexc("#ffd35a")), (1.0, hexc("#d98a1c"))]


# ------------------------------------------------------------------ caveira (o "O")
def skull_layers(h):
    """Caveira com viseira de 2040, altura h. Retorna (máscara da silhueta, detalhes RGBA)."""
    w = int(h * 0.92)
    ss = 4
    W, H = w * ss, h * ss

    def shape(img, _):
        d = ImageDraw.Draw(img)
        # crânio
        d.ellipse((0, 0, W - 1, int(H * 0.78)), fill=(255, 255, 255, 255))
        # mandíbula
        jw0, jw1 = int(W * 0.2), int(W * 0.8)
        d.rounded_rectangle((jw0, int(H * 0.55), jw1, H - 1), radius=int(W * 0.12), fill=(255, 255, 255, 255))
    sil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shape(sil, ss)
    mask = sil.getchannel("A").resize((w, h), Image.LANCZOS)

    det = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(det)
    ink = INK
    # viseira (faixa com brilho), no lugar dos olhos
    vy0, vy1 = int(H * 0.30), int(H * 0.50)
    d.rounded_rectangle((int(W * 0.06), vy0, int(W * 0.94), vy1), radius=int((vy1 - vy0) / 2), fill=ink)
    d.rounded_rectangle((int(W * 0.10), vy0 + int(H * 0.03), int(W * 0.90), vy1 - int(H * 0.03)),
                        radius=int((vy1 - vy0) / 2), fill=hexc("#33e3f2"))
    d.rounded_rectangle((int(W * 0.14), vy0 + int(H * 0.045), int(W * 0.60), vy0 + int(H * 0.085)),
                        radius=int(H * 0.02), fill=hexc("#e6ffff"))
    # nariz
    nx, ny = W // 2, int(H * 0.57)
    d.polygon([(nx, ny - int(H * 0.05)), (nx - int(W * 0.06), ny + int(H * 0.04)), (nx + int(W * 0.06), ny + int(H * 0.04))], fill=ink)
    # dentes
    ty0, ty1 = int(H * 0.72), int(H * 0.92)
    d.rounded_rectangle((int(W * 0.27), ty0 - int(H * 0.012), int(W * 0.73), ty0 + int(H * 0.012)), radius=4, fill=ink)
    for i in range(1, 5):
        x = int(W * (0.27 + 0.46 * i / 5))
        d.rounded_rectangle((x - int(W * 0.012), ty0, x + int(W * 0.012), ty1), radius=4, fill=ink)
    # rachadura charmosa no crânio
    d.line([(int(W * 0.70), int(H * 0.05)), (int(W * 0.64), int(H * 0.14)), (int(W * 0.69), int(H * 0.19))],
           fill=ink, width=int(W * 0.025))
    det = det.resize((w, h), Image.LANCZOS)
    return mask, det


# ------------------------------------------------------------------ estilos
def styled(mask, grad, stroke, depth, extra_glow=None, scan=False, bevel=6):
    """Letras com contorno grosso, extrusão 3D, brilho interno e sombra."""
    P = stroke + depth + 40
    m = pad(mask, P)
    outer = dilate(m, stroke)
    canvas = Image.new("RGBA", m.size, (0, 0, 0, 0))
    # sombra projetada suave
    sh = shift(dilate(m, stroke + 2), 0, depth + 10).filter(ImageFilter.GaussianBlur(9))
    comp(canvas, fill(scale_alpha(sh, 0.75), INK_DEEP))
    if extra_glow:
        comp(canvas, glow(outer, extra_glow, 26, 1.3))
    # extrusão: várias cópias do contorno deslocadas para baixo
    for i in range(depth, 0, -1):
        t = i / max(depth, 1)
        col = tuple(int(INK[c] * (1 - 0.35 * t) + INK_DEEP[c] * 0.35 * t) for c in range(3)) + (255,)
        comp(canvas, fill(shift(outer, 0, i), col))
    comp(canvas, fill(outer, INK))
    # aro claro fino entre o contorno e o preenchimento
    rim = dilate(m, max(2, stroke // 5))
    comp(canvas, fill(rim, hexc("#ffffff", 70)))
    # preenchimento com gradiente
    bbox = mask.getbbox()
    top = P + bbox[1]
    g = vgrad(m.size, grad, top=top, height=bbox[3] - bbox[1])
    comp(canvas, fill(m, g))
    if scan:
        lines = Image.new("L", m.size, 0)
        dl = ImageDraw.Draw(lines)
        for y in range(0, m.size[1], 7):
            dl.line([(0, y), (m.size[0], y)], fill=70, width=2)
        comp(canvas, fill(Image.fromarray(np.minimum(np.asarray(lines), np.asarray(m)).astype(np.uint8)), hexc("#0b3d6b")))
    # bisel: luz em cima, sombra embaixo
    hi = subtract(m, shift(m, 0, bevel))
    comp(canvas, fill(scale_alpha(hi, 0.85), hexc("#ffffff")))
    lo = subtract(m, shift(m, 0, -bevel))
    comp(canvas, fill(scale_alpha(lo, 0.35), INK))
    # brilho "glossy" na metade de cima
    gloss = Image.new("L", m.size, 0)
    ImageDraw.Draw(gloss).rectangle((0, 0, m.size[0], top + int((bbox[3] - bbox[1]) * 0.42)), fill=60)
    comp(canvas, fill(Image.fromarray(np.minimum(np.asarray(gloss), np.asarray(m)).astype(np.uint8)), hexc("#ffffff")))
    return canvas, P


def word_with_skull(text_before, text_after, f, gap):
    """Máscara de 'ESQUELET' + caveira + 'NS', com os detalhes da caveira."""
    a = text_mask(text_before, f, tracking=gap)
    b = text_mask(text_after, f, tracking=gap)
    o = text_mask("O", f)
    sh = int(o.height * 1.12)
    smask, sdet = skull_layers(sh)
    H = max(a.height, sh, b.height)
    base = max(a.height, b.height)
    W = a.width + smask.width + b.width + gap * 2
    m = Image.new("L", (W, H + sh // 3), 0)
    y_text = H - base
    m.paste(a, (0, y_text))
    sx = a.width + gap
    sy = H - sh + int(o.height * 0.10)
    m.paste(smask, (sx, sy), smask)
    m.paste(b, (sx + smask.width + gap, y_text))
    return m, sdet, (sx, sy)


def speed_lines(w, h, color):
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    def draw(big, ss):
        d = ImageDraw.Draw(big)
        rnd = random.Random(4)
        for i in range(7):
            y = int((0.15 + 0.7 * i / 6) * h * ss)
            length = rnd.uniform(0.45, 1.0) * w * ss
            th = rnd.uniform(0.018, 0.04) * h * ss
            x1 = w * ss
            d.polygon([(x1 - length, y), (x1, y - th), (x1, y + th)], fill=color)
    return supersample(draw, (w, h), 2)


def ribbon(text_small, text_big, width_hint):
    fs = font("Orbitron.ttf", 64, 700)
    fb = font("Orbitron.ttf", 92, 900)
    ms = text_mask(text_small, fs, tracking=14)
    mb = text_mask(text_big, fb, tracking=10)
    dia = 34
    gap = 36
    inner_w = ms.width + gap + dia + gap + mb.width
    W = max(width_hint, inner_w + 160)
    H = 150
    out = Image.new("RGBA", (W + 80, H + 80), (0, 0, 0, 0))

    def draw(big, ss):
        d = ImageDraw.Draw(big)
        x0, y0, x1, y1 = 40 * ss, 40 * ss, (40 + W) * ss, (40 + H) * ss
        r = H * ss // 2
        d.rounded_rectangle((x0, y0 + 10 * ss, x1, y1 + 10 * ss), radius=r, fill=hexc("#05030f", 200))
        d.rounded_rectangle((x0, y0, x1, y1), radius=r, fill=hexc("#ffcf5a"))
        d.rounded_rectangle((x0 + 7 * ss, y0 + 7 * ss, x1 - 7 * ss, y1 - 7 * ss), radius=r - 7 * ss, fill=hexc("#1b1238"))
        d.rounded_rectangle((x0 + 13 * ss, y0 + 13 * ss, x1 - 13 * ss, y1 - 13 * ss), radius=r - 13 * ss,
                            outline=hexc("#ffcf5a", 90), width=2 * ss)
    out = comp(out, supersample(draw, out.size, 3))
    gl = vgrad(out.size, GOLD, top=40 + (H - mb.height) // 2, height=mb.height)
    cx = 40 + (W - inner_w) // 2
    cy = 40 + H // 2
    comp(out, fill(pad_to(ms, out.size, (cx, cy - ms.height // 2)), hexc("#ffe7a6")))
    # losango separador
    dm = Image.new("L", out.size, 0)
    dx = cx + ms.width + gap
    ImageDraw.Draw(dm).polygon([(dx + dia // 2, cy - dia // 2), (dx + dia, cy), (dx + dia // 2, cy + dia // 2), (dx, cy)], fill=255)
    comp(out, fill(dm, hexc("#4ff0ff")))
    comp(out, glow(dm, hexc("#4ff0ff"), 10, 1.4))
    bx = dx + dia + gap
    bm = pad_to(mb, out.size, (bx, cy - mb.height // 2))
    comp(out, fill(dilate(bm, 3), hexc("#0b0719")))
    comp(out, fill(bm, gl))
    return out


def pad_to(mask, size, xy):
    out = Image.new("L", size, 0)
    out.paste(mask, xy)
    return out


def make_logo():
    f_main = font("LilitaOne-Regular.ttf", 300)
    m1, sdet, (sx, sy) = word_with_skull("ESQUELET", "NS", f_main, 6)
    l1, p1 = styled(m1, BONE, stroke=20, depth=16, extra_glow=hexc("#ff9a5a", 140))
    comp(l1, sdet, (p1 + sx, p1 + sy))
    # brilho extra na viseira
    vis = Image.new("L", l1.size, 0)
    vis.paste(sdet.getchannel("A").point(lambda v: 0), (0, 0))

    f_runs = font("LilitaOne-Regular.ttf", 250)
    m2 = text_mask("RUNS", f_runs, tracking=8)
    l2, p2 = styled(m2, FIRE, stroke=18, depth=14, extra_glow=hexc("#ff5a2c", 150))
    f_year = font("Orbitron.ttf", 230, 900)
    m3 = text_mask("2040", f_year, tracking=14)
    l3, p3 = styled(m3, NEON, stroke=18, depth=14, extra_glow=hexc("#22d8ff", 255), scan=True)
    sp = speed_lines(520, l2.height // 2, hexc("#ffcf6a", 230))

    gap = 10
    row2_w = sp.width // 2 + l2.width + gap + l3.width
    W = max(l1.width, row2_w) + 40
    rb = ribbon("EDITION", "DISCOVERY", int(W * 0.62))
    H = l1.height + l2.height + rb.height - 260
    logo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    comp(logo, l1, ((W - l1.width) // 2, 0))
    y2 = l1.height - 150
    x2 = (W - row2_w) // 2 + sp.width // 2
    comp(logo, sp, (x2 - sp.width + 120, y2 + l2.height // 4))
    comp(logo, l2, (x2, y2))
    comp(logo, l3, (x2 + l2.width + gap, y2 + (l2.height - l3.height) // 2))
    y3 = y2 + l2.height - 110
    comp(logo, rb, ((W - rb.width) // 2, y3))
    logo = skew(logo, -0.10)
    logo = logo.crop(logo.getbbox())
    target_w = 1600
    logo = logo.resize((target_w, int(logo.height * target_w / logo.width)), Image.LANCZOS)
    return logo


# ------------------------------------------------------------------ cenário
BW, BH = 2400, 1080
HORIZON = 640
SUN_X = 1200


def sky_and_sea():
    img = vgrad((BW, BH), [(0.0, hexc("#0b0826")), (0.30, hexc("#24124f")), (0.52, hexc("#6a2580")),
                            (0.66, hexc("#d24a6a")), (0.75, hexc("#ff9a5c")), (HORIZON / BH, hexc("#ffcf7a")),
                            (HORIZON / BH + 0.001, hexc("#3a2466")), (0.80, hexc("#2a1b55")), (1.0, hexc("#0a0a24"))])
    rnd = random.Random(7)
    d = ImageDraw.Draw(img)
    # estrelas
    for i in range(420):
        x = rnd.uniform(0, BW)
        y = rnd.uniform(0, HORIZON * 0.62) ** 1.05
        a = int(255 * (1 - y / (HORIZON * 0.7)) * rnd.uniform(0.3, 1))
        r = rnd.choice([0.8, 1.0, 1.2, 1.6, 2.2])
        d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 245, 235, max(0, a)))
    for i in range(14):
        x, y = rnd.uniform(0, BW), rnd.uniform(20, HORIZON * 0.45)
        star = Image.new("RGBA", (60, 60), (0, 0, 0, 0))
        sd = ImageDraw.Draw(star)
        sd.line([(30, 6), (30, 54)], fill=(255, 255, 255, 170), width=2)
        sd.line([(6, 30), (54, 30)], fill=(255, 255, 255, 170), width=2)
        star = star.filter(ImageFilter.GaussianBlur(1.2))
        sd = ImageDraw.Draw(star)
        sd.ellipse((26, 26, 34, 34), fill=(255, 255, 255, 255))
        img.alpha_composite(star, (int(x) - 30, int(y) - 30))
    # brilho do sol
    halo = Image.new("L", (BW, BH), 0)
    ImageDraw.Draw(halo).ellipse((SUN_X - 520, HORIZON - 520, SUN_X + 520, HORIZON + 300), fill=200)
    halo = halo.filter(ImageFilter.GaussianBlur(160))
    img.alpha_composite(fill(halo, hexc("#ff7a5a", 200)))
    img = img.copy()
    sun = sun_disc(300)
    img.alpha_composite(sun, (SUN_X - sun.width // 2, HORIZON - sun.height + 36))
    # mar por cima da base do sol
    sea = vgrad((BW, BH - HORIZON), [(0.0, hexc("#5a2f7a")), (0.12, hexc("#3a2466")), (0.5, hexc("#1d1648")), (1.0, hexc("#090920"))])
    img.alpha_composite(sea, (0, HORIZON))
    # reflexo do sol: faixas horizontais tremidas
    refl = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))

    def draw_refl(big, ss):
        dd = ImageDraw.Draw(big)
        r2 = random.Random(3)
        y = HORIZON + 6
        while y < BH:
            depth = (y - HORIZON) / (BH - HORIZON)
            half = (230 - 120 * depth) * r2.uniform(0.5, 1.15)
            cx = SUN_X + r2.uniform(-40, 40) * (1 + depth)
            th = 3 + 7 * depth
            col = (255, int(200 - 80 * depth), int(130 + 20 * depth), int(230 * (1 - depth) ** 1.3))
            dd.rounded_rectangle(((cx - half) * ss, y * ss, (cx + half) * ss, (y + th) * ss), radius=th * ss / 2, fill=col)
            y += th + 6 + 10 * depth
        # ondinhas espalhadas
        for i in range(260):
            x = r2.uniform(0, BW)
            yy = r2.uniform(HORIZON + 10, BH)
            depth = (yy - HORIZON) / (BH - HORIZON)
            ln = r2.uniform(20, 90) * (0.5 + depth)
            dd.rounded_rectangle((x * ss, yy * ss, (x + ln) * ss, (yy + 2 + 3 * depth) * ss), radius=3 * ss,
                                 fill=(190, 150, 255, int(70 * (1 - depth * 0.5))))
    refl = supersample(draw_refl, (BW, BH), 2)
    img.alpha_composite(refl)
    # linha do horizonte brilhante
    hl = Image.new("L", (BW, BH), 0)
    ImageDraw.Draw(hl).rectangle((0, HORIZON - 2, BW, HORIZON + 2), fill=255)
    img.alpha_composite(glow(hl, hexc("#ffb27a"), 6, 0.9))
    return img


def sun_disc(r):
    size = 2 * r
    disc = vgrad((size, size), [(0.0, hexc("#fff4a8")), (0.45, hexc("#ffc45a")), (0.75, hexc("#ff7a5a")), (1.0, hexc("#ff3d7f"))])
    mask = Image.new("L", (size * 3, size * 3), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((0, 0, size * 3 - 1, size * 3 - 1), fill=255)
    # listras retrô na metade de baixo, cada vez mais grossas
    y = int(size * 3 * 0.52)
    k = 0
    while y < size * 3:
        th = int(6 + k * 5)
        d.rectangle((0, y, size * 3, y + th), fill=0)
        y += th + int(46 - k * 3)
        k += 1
    mask = mask.resize((size, size), Image.LANCZOS)
    return fill(mask, disc)


def island_with_castle():
    img = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))

    def draw(big, ss):
        d = ImageDraw.Draw(big)
        s = ss
        far = hexc("#3b2163")
        near = hexc("#24143f")
        # ilhas distantes à esquerda
        d.polygon([(250 * s, HORIZON * s), (420 * s, 598 * s), (560 * s, 612 * s), (700 * s, 584 * s),
                   (900 * s, HORIZON * s)], fill=far)
        d.polygon([(0, HORIZON * s), (90 * s, 612 * s), (200 * s, 624 * s), (260 * s, HORIZON * s)], fill=far)
        # rochedo do castelo, à direita
        OX = 1390
        rock = [(120, HORIZON), (210, 560), (260, 545), (300, 470), (360, 455), (420, 430), (520, 438), (560, 470),
                (600, 520), (660, 560), (740, 600), (820, HORIZON)]
        d.polygon([((x + OX) * s, y * s) for x, y in rock], fill=near)
        # castelo: torres e pináculos
        def tower(cx, base, w, h, spire):
            cx += OX
            d.rectangle(((cx - w / 2) * s, (base - h) * s, (cx + w / 2) * s, base * s), fill=near)
            d.polygon([((cx - w / 2 - 6) * s, (base - h) * s), (cx * s, (base - h - spire) * s), ((cx + w / 2 + 6) * s, (base - h) * s)], fill=near)
            for i in range(3):  # ameias
                bx = cx - w / 2 + i * w / 2.5
                d.rectangle((bx * s, (base - h - 8) * s, (bx + w / 6) * s, (base - h) * s), fill=near)
        d.rectangle(((330 + OX) * s, 330 * s, (560 + OX) * s, 440 * s), fill=near)
        tower(345, 440, 34, 150, 70)
        tower(545, 440, 34, 140, 64)
        tower(445, 440, 52, 230, 110)
        tower(395, 440, 26, 170, 60)
        tower(495, 440, 26, 160, 56)
        # janelas acesas do castelo
        win = hexc("#ff4fd8")
        for (x, y) in [(445, 260), (445, 300), (395, 330), (495, 340), (345, 360), (545, 370), (430, 400), (460, 400)]:
            d.rounded_rectangle(((x + OX - 5) * s, (y - 9) * s, (x + OX + 5) * s, (y + 9) * s), radius=4 * s, fill=win)
        # olho da caveira no topo da torre principal
        d.ellipse(((433 + OX) * s, 205 * s, (457 + OX) * s, 229 * s), fill=hexc("#9b5cff"))
    img = supersample(draw, (BW, BH), 2)
    # brilho mágico das janelas
    a = img.getchannel("A")
    pinks = Image.fromarray((np.asarray(img)[:, :, 0] > 200).astype(np.uint8) * 255).convert("L")
    pinks = Image.fromarray(np.minimum(np.asarray(pinks), np.asarray(a)))
    img.alpha_composite(glow(pinks, hexc("#ff4fd8"), 12, 1.6))
    # névoa na base
    haze = vgrad((BW, 140), [(0.0, hexc("#ff9a6a", 0)), (1.0, hexc("#ffb27a", 90))])
    hz = Image.new("RGBA", (BW, BH), (0, 0, 0, 0))
    hz.alpha_composite(haze, (0, HORIZON - 140))
    hz.putalpha(Image.fromarray(np.minimum(np.asarray(hz.getchannel("A")), np.asarray(a))))
    img.alpha_composite(hz)
    return img.crop((0, 0, BW, HORIZON + 4))


def clouds():
    img = Image.new("RGBA", (BW, 520), (0, 0, 0, 0))
    rnd = random.Random(11)
    for c in range(9):
        cx = rnd.uniform(0, BW)
        cy = rnd.uniform(140, 470)
        w = rnd.uniform(260, 620)
        layer = Image.new("L", img.size, 0)
        d = ImageDraw.Draw(layer)
        for i in range(10):
            ex = cx + rnd.uniform(-w / 2, w / 2)
            ey = cy + rnd.uniform(-18, 10)
            rx = rnd.uniform(60, 150)
            ry = rx * rnd.uniform(0.18, 0.32)
            for off in (-BW, 0, BW):  # repete nas bordas: a camada emenda sem corte
                d.ellipse((ex + off - rx, ey - ry, ex + off + rx, ey + ry), fill=255)
        layer = layer.filter(ImageFilter.GaussianBlur(10))
        lit = vgrad(img.size, [(0.0, hexc("#7b3a9a", 150)), (0.6, hexc("#e0608a", 170)), (1.0, hexc("#ffb07a", 190))],
                    top=int(cy - 40), height=80)
        img.alpha_composite(fill(layer, lit))
    return img


def palm(img_draw, s, base, height, lean, flip=False, col=hexc("#120a24")):
    d = img_draw
    bx, by = base
    tx = bx + lean
    ty = by - height
    pts = []
    for i in range(41):
        t = i / 40
        x = (1 - t) ** 2 * bx + 2 * (1 - t) * t * (bx + lean * 0.15) + t * t * tx
        y = (1 - t) ** 2 * by + 2 * (1 - t) * t * (by - height * 0.55) + t * t * ty
        pts.append((x, y, 26 - 12 * t))
    left = [((x - w / 2) * s, y * s) for x, y, w in pts]
    right = [((x + w / 2) * s, y * s) for x, y, w in reversed(pts)]
    d.polygon(left + right, fill=col)
    for i in range(0, 40, 4):
        x, y, w = pts[i]
        d.line([((x - w / 2) * s, y * s), ((x + w / 2) * s, (y + 4) * s)], fill=hexc("#2a1846"), width=2 * s)
    # folhas
    for k, ang in enumerate([-175, -150, -125, -100, -75, -50, -25, 0, 25, 205, 155]):
        a = math.radians(ang)
        length = 300 if k % 2 == 0 else 250
        leaf = []
        upper, lower = [], []
        for i in range(25):
            t = i / 24
            droop = 95 * t * t
            x = tx + math.cos(a) * length * t
            y = ty + math.sin(a) * length * t + droop
            wdt = 46 * math.sin(math.pi * min(1, t * 1.05)) + 3
            nx, ny = -math.sin(a), math.cos(a)
            upper.append(((x + nx * wdt) * s, (y + ny * wdt * 0.4 - wdt * 0.5) * s))
            lower.append(((x - nx * wdt) * s, (y - ny * wdt * 0.4 + wdt * 0.5) * s))
        d.polygon(upper + list(reversed(lower)), fill=col)
    d.ellipse(((tx - 22) * s, (ty - 10) * s, (tx + 22) * s, (ty + 26) * s), fill=col)


def foreground():
    def draw(big, ss):
        d = ImageDraw.Draw(big)
        col = hexc("#120a24")
        # dunas
        d.polygon([(0, 860 * ss), (300 * ss, 830 * ss), (620 * ss, 905 * ss), (900 * ss, 1080 * ss), (0, 1080 * ss)], fill=col)
        d.polygon([(2400 * ss, 820 * ss), (2120 * ss, 860 * ss), (1840 * ss, 960 * ss), (1700 * ss, 1080 * ss), (2400 * ss, 1080 * ss)], fill=col)
        palm(d, ss, (180, 880), 640, 220)
        palm(d, ss, (420, 900), 470, 160)
        palm(d, ss, (2330, 840), 600, -170)
        # barquinho encalhado à direita
        d.polygon([(1930 * ss, 935 * ss), (2130 * ss, 915 * ss), (2100 * ss, 960 * ss), (1960 * ss, 968 * ss)], fill=col)
        d.line([(2025 * ss, 922 * ss), (2010 * ss, 830 * ss)], fill=col, width=6 * ss)
    img = supersample(draw, (BW, BH), 2)
    # contraluz: borda alaranjada nas silhuetas
    a = img.getchannel("A")
    rim = subtract(a, shift(a, -3, 3))
    img.alpha_composite(fill(scale_alpha(rim, 0.6), hexc("#ff8a5a")))
    return img


def rays():
    size = 1024
    img = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(img)
    c = size / 2
    rnd = random.Random(5)
    for i in range(18):
        a0 = i * 2 * math.pi / 18 + rnd.uniform(-0.05, 0.05)
        wa = rnd.uniform(0.04, 0.09)
        d.polygon([(c, c), (c + math.cos(a0 - wa) * c * 1.5, c + math.sin(a0 - wa) * c * 1.5),
                   (c + math.cos(a0 + wa) * c * 1.5, c + math.sin(a0 + wa) * c * 1.5)], fill=rnd.randint(90, 160))
    img = img.filter(ImageFilter.GaussianBlur(10))
    # some com a distância do centro
    yy, xx = np.mgrid[0:size, 0:size]
    falloff = np.clip(1 - np.hypot(xx - c, yy - c) / c, 0, 1) ** 1.4
    arr = (np.asarray(img, np.float32) * falloff).astype(np.uint8)
    return fill(Image.fromarray(arr), hexc("#ffe0a8"))


def soft_dot(size=64):
    yy, xx = np.mgrid[0:size, 0:size]
    c = (size - 1) / 2
    a = np.clip(1 - np.hypot(xx - c, yy - c) / c, 0, 1) ** 2
    arr = np.zeros((size, size, 4), np.uint8)
    arr[:, :, :3] = 255
    arr[:, :, 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    make_logo().save(OUT / "logo.png", optimize=True)
    print("logo ok")
    sky_and_sea().convert("RGB").save(OUT / "bg.png", optimize=True)
    island_with_castle().save(OUT / "castle.png", optimize=True)
    clouds().save(OUT / "clouds.png", optimize=True)
    foreground().save(OUT / "fore.png", optimize=True)
    rays().save(OUT / "rays.png", optimize=True)
    soft_dot().save(OUT / "glow_dot.png")
    print("tela inicial gerada em", OUT)


if __name__ == "__main__":
    main()
