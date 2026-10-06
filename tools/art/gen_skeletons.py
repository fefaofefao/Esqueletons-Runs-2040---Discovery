#!/usr/bin/env python3
"""Sprites das 80 espécies do Bestiário (arte original, gerada por código).

Para cada espécie gera:
  assets/skeletons/<id>.png      folha 64×32 (frente 0–31, costas 32–63)
  assets/skeletons/map/<id>.png  folha 32×16 (2 quadros 16×16 para o mapa)
e a folha de revisão docs/bestiario_sheet.png (mapa + batalha, lado a lado).

Cada linha tem uma função que desenha os 3 estágios seguindo o "arco de
crescimento" de tools/bestiary/bestiary.py: o que muda é a peça que conta a
história (ferramenta, roupa, objeto), nunca só cor ou tamanho.
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parents[1] / "bestiary"))
from skel import (Layer, Sprite, body_frame, draw_body, draw_skull, back_view, darken, lighten,  # noqa: E402
                  OUTL, BONE, W)
import bestiary as B  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/skeletons"

WOOD = (168, 114, 64)
WOOD_D = (120, 80, 46)
IRON = (150, 156, 170)
GOLD = (240, 196, 72)
WHITE = (246, 246, 240)
GLASS = (190, 236, 250)
FLAME = (255, 168, 60)


# ------------------------------------------------------------------ ajudantes
def H(f):
    hx, hy = f["head"]
    rx, ry = f["hr"]
    return hx, hy, rx, ry


def cap(L, f, c, depth=0.35, extra=0.6, lift=0):
    """Chapéu que cobre o topo do crânio até a altura `depth` (fração do raio)."""
    hx, hy, rx, ry = H(f)
    cut = hy - ry * depth
    for yy in range(int(hy - ry - 3 - lift), int(cut) + 1):
        for xx in range(int(hx - rx - 2), int(hx + rx + 3)):
            dx = (xx + 0.5 - hx) / (rx + extra)
            dy = (yy + 0.5 - (hy - lift)) / (ry + extra)
            if dx * dx + dy * dy <= 1.0:
                L.px(xx, yy, c)


def tunic(L, f, c, bottom=None, flare=1):
    sx, sy = f["shoulder"]
    rx_, ry_ = f["shoulder_r"]
    b = bottom if bottom is not None else f["pelvis"] + 1
    L.poly([(sx, sy - 1), (rx_, ry_ - 1), (rx_ + flare, b), (sx - flare, b)], c)


def cape(L, f, c, bottom=28, spread=3):
    sx, sy = f["shoulder"]
    rx_, ry_ = f["shoulder_r"]
    L.poly([(sx, sy - 1), (rx_, ry_ - 1), (rx_ + spread, bottom), (sx - spread, bottom)], c)


def stick(L, x0, y0, x1, y1, c=WOOD, w=1):
    L.line(x0, y0, x1, y1, c, w)


def sparkle(L, pts, c=GOLD):
    for x, y in pts:
        L.px(x, y, c)


def new(stage, lean=0, wide=0):
    return Sprite(), body_frame(stage, lean, wide)


# ------------------------------------------------------------------ PRAIA
def grumete(st):
    sp, f = new(st, wide=1 if st == 3 else 0)
    navy, red, canvas = (52, 86, 150), (214, 72, 60), (206, 178, 120)
    if st == 3:
        L = Layer(); stick(L, 3, 27, 28, 2, WOOD, 2); L.ell(4, 26, 2, 3, WOOD); L.ell(27, 3, 2, 3, WOOD); sp.add(L)
    hands = {2: {"r": (23, 19), "l": (9, 20)}, 3: {"l": (7, 18), "r": (25, 18)}}.get(st)
    draw_body(sp, f, hands, legs="wide" if st == 3 else "stand")
    L = Layer()
    if st == 1:
        tunic(L, f, navy, flare=0)
    elif st == 2:
        tunic(L, f, red); L.rect(15, 14, 3, 8, (250, 200, 80))
    else:
        tunic(L, f, canvas, bottom=23, flare=2); L.rect(15, 11, 2, 12, darken(canvas, .3))
    sp.add(L)
    if st == 1:
        D = Layer(shade=False, outline=False)
        for y in (21, 23):
            L2 = None
            D.rect(13, y, 7, 1, WHITE)
        sp.add(D)
    draw_skull(sp, f, mood="angry" if st == 3 else "calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        cap(L, f, navy, depth=0.25); L.rect(int(hx - rx), int(hy - ry * 0.3), int(rx * 2) + 1, 2, WHITE); L.ell(hx, hy - ry - 1.5, 1.8, 1.8, red)
    elif st == 2:
        L.rect(int(hx - rx), int(hy - ry + 1), int(rx * 2) + 1, 3, red)
        L.poly([(hx + rx - 1, hy - ry + 2), (hx + rx + 4, hy - ry + 5), (hx + rx + 1, hy - ry + 6)], red)
    else:
        L.rect(int(hx - rx - 2), int(hy - ry + 1), int(rx * 2) + 5, 2, navy)
        L.poly([(hx - rx + 1, hy - ry + 1), (hx + rx - 1, hy - ry + 1), (hx + rx - 2, hy - ry - 3), (hx - rx + 2, hy - ry - 3)], navy)
    sp.add(L)
    L = Layer()
    if st == 1:
        stick(L, 22, 28, 25, 17); L.ell(25.5, 15.5, 1.6, 2.6, WOOD)
    elif st == 2:
        stick(L, 25, 29, 21, 4, WOOD, 2); L.ell(21, 4, 2, 3.5, WOOD)
    sp.add(L)
    if st == 3:
        D = Layer(shade=False, outline=False); hx, hy, rx, ry = H(f); D.px(int(hx), int(hy - ry - 1), GOLD); sp.add(D)
    return sp.image()


def faroleira(st):
    sp, f = new(st)
    teal, cream, purple, red = (64, 170, 180), (250, 236, 200), (120, 80, 170), (200, 64, 64)
    hands = {1: {"r": (22, 16)}, 3: {"r": (25, 10)}}.get(st)
    if st == 2:
        L = Layer(); stick(L, 20, 14, 25, 6, (80, 84, 110)); L.poly([(22, 0), (29, 0), (30, 9), (21, 9)], (80, 84, 110)); L.poly([(23, 1), (28, 1), (29, 8), (22, 8)], GLASS); sp.add(L)
        G = Layer(shade=False, outline=False); G.poly([(24, 3), (27, 3), (27, 7), (24, 7)], (255, 236, 130)); G.px(24, 2, WHITE)
        sparkle(G, [(31, 3), (20, 1), (31, 8)], (255, 236, 130)); sp.add(G)
    if st >= 2:
        L = Layer(); cape(L, f, teal if st == 2 else purple, bottom=24 if st == 2 else 29); sp.add(L)
    draw_body(sp, f, hands)
    L = Layer()
    if st == 1:
        tunic(L, f, teal, bottom=27, flare=2)
    elif st == 3:
        tunic(L, f, darken(purple, .2), bottom=24, flare=1); L.rect(15, 11, 3, 13, GOLD)
    sp.add(L)
    draw_skull(sp, f)
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        cap(L, f, cream, depth=0.15, extra=1.0)
        L.poly([(hx + rx, hy - 2), (hx + rx + 3, hy + 1), (hx + rx + 1, hy + 2)], cream)
    elif st == 2:
        L.rect(int(hx - rx), int(hy - ry + 1), int(rx * 2) + 1, 2, teal)
    else:
        L.rect(int(hx - 3), int(hy - ry - 5), 7, 6, (80, 84, 110)); L.rect(int(hx - 2), int(hy - ry - 4), 5, 4, (255, 236, 130))
        L.poly([(hx - 4, hy - ry - 5), (hx + 4, hy - ry - 5), (hx, hy - ry - 9)], red)
    sp.add(L)
    L = Layer()
    if st == 1:
        L.line(22, 16, 22, 14, (80, 84, 110)); L.rect(20, 17, 5, 6, (80, 84, 110)); L.rect(21, 18, 3, 4, (255, 236, 130))
    elif st == 3:
        stick(L, 25, 29, 25, 8); L.ell(25, 6, 3, 3, GLASS)
    sp.add(L)
    G = Layer(shade=False, outline=False)
    if st == 3:
        sparkle(G, [(11, 0), (21, 0), (8, 2), (24, 2)], (255, 236, 130)); G.px(24, 5, WHITE)
    elif st == 1:
        sparkle(G, [(25, 16), (19, 15)], (255, 236, 130))
    sp.add(G)
    return sp.image()


def marisqueiro(st):
    sp, f = new(st, wide=1 if st == 3 else 0)
    shell, urchin, sea = (240, 170, 150), (92, 52, 120), (70, 150, 160)
    hands = {3: {"r": (26, 16), "l": (7, 20)}}.get(st)
    draw_body(sp, f, hands, legs="wide" if st >= 2 else "stand")
    L = Layer()
    if st == 2:
        tunic(L, f, sea, flare=1)
    elif st == 3:
        tunic(L, f, urchin, bottom=23, flare=3)
    sp.add(L)
    if st == 3:
        S = Layer(shade=False, outline=False)
        for (x, y) in [(8, 11), (6, 15), (7, 19), (24, 11), (26, 14), (25, 19), (11, 9), (21, 9)]:
            S.line(x, y, x + (-2 if x < 16 else 2), y - 1, (140, 100, 170))
        sp.add(S)
    draw_skull(sp, f, mood="sleepy" if st == 1 else ("angry" if st == 3 else "calm"))
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        cap(L, f, shell, depth=0.3, extra=1)
    elif st == 2:
        cap(L, f, darken(sea, .2), depth=0.4)
    else:
        cap(L, f, urchin, depth=0.35, extra=0.8)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    if st == 1:
        for x in range(int(hx - rx), int(hx + rx) + 1, 2):
            D.line(hx, hy - ry - 1, x, hy - ry * 0.3, darken(shell, .25))
    elif st >= 2:
        n = 7 if st == 2 else 11
        for i in range(n):
            import math
            a = math.pi * (0.1 + 0.8 * i / (n - 1))
            x0 = hx - math.cos(a) * (rx + 0.5)
            y0 = hy - ry * 0.3 - math.sin(a) * (ry * 0.8)
            D.line(x0, y0, x0 - math.cos(a) * (2 if st == 2 else 3), y0 - math.sin(a) * (2 if st == 2 else 3), (60, 30, 80))
    sp.add(D)
    L = Layer()
    if st == 1:
        L.rect(20, 24, 6, 5, (120, 160, 190)); L.rect(20, 23, 6, 1, IRON); D2 = None
    elif st == 2:
        for hd in ((9, 22.5), (23, 22.5)):
            L.ell(hd[0], hd[1], 2.4, 2.4, urchin)
        stick(L, 25, 22, 28, 8, WOOD); L.ell(28, 7, 2.5, 2.5, (220, 220, 200))
    else:
        stick(L, 26, 29, 26, 3, IRON); L.line(23, 5, 29, 5, IRON)
        for x in (23, 26, 29):
            L.line(x, 5, x, 1, IRON)
    sp.add(L)
    return sp.image()


def rendeira(st):
    sp, f = new(st)
    yarn, net, rose, moon = (226, 120, 150), (220, 200, 160), (196, 80, 120), (200, 220, 255)
    if st == 3:
        L = Layer()
        L.poly([(15, 10), (3, 2), (1, 16), (9, 20)], moon); L.poly([(17, 10), (29, 2), (31, 16), (23, 20)], moon)
        sp.add(L)
        D = Layer(shade=False, outline=False)
        for i in range(4, 17, 3):
            D.line(3, i, 12, 12, (150, 170, 230)); D.line(29, i, 20, 12, (150, 170, 230))
        sp.add(D)
        L = Layer(); L.rect(11, 6, 10, 3, WOOD); sp.add(L)
    hands = {2: {"r": (24, 14)}, 3: {"l": (9, 18), "r": (23, 18)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st == 1:
        L.ell(16, 23, 6, 5, yarn)
    elif st == 2:
        L.poly([(11, 13), (21, 13), (25, 29), (7, 29)], rose)
    else:
        L.poly([(10, 11), (22, 11), (26, 29), (6, 29)], (92, 70, 140))
    sp.add(L)
    D = Layer(shade=False, outline=False)
    if st == 1:
        for (x0, y0, x1, y1) in [(11, 21, 21, 24), (12, 25, 20, 20), (11, 23, 19, 27)]:
            D.line(x0, y0, x1, y1, darken(yarn, .25))
    elif st >= 2:
        c = darken(rose, .3) if st == 2 else (150, 170, 230)
        for x in range(9, 25, 3):
            D.line(x, 18 if st == 2 else 14, x + 2, 28, c)
            D.line(x + 2, 18 if st == 2 else 14, x, 28, c)
    sp.add(D)
    draw_skull(sp, f)
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        L.ell(hx + rx - 1, hy - ry + 1, 2.2, 2.2, yarn)
    elif st == 2:
        cap(L, f, net, depth=0.1, extra=1.2); L.rect(int(hx - rx - 1), int(hy + 1), 2, 4, net); L.rect(int(hx + rx), int(hy + 1), 2, 4, net)
    else:
        cap(L, f, moon, depth=0.35, extra=0.8)
    sp.add(L)
    L = Layer()
    if st == 1:
        stick(L, 22, 26, 26, 19, (230, 230, 230))
    elif st == 2:
        stick(L, 24, 14, 27, 3, (230, 230, 230), 1); L.px(27, 4, (230, 230, 230)); L.ell(9, 22, 2, 2, yarn)
    sp.add(L)
    if st == 3:
        G = Layer(shade=False, outline=False); sparkle(G, [(2, 5), (30, 6), (4, 14), (28, 13)], WHITE); sp.add(G)
    return sp.image()


# ------------------------------------------------------------------ BOSQUE
def lenhador(st):
    sp, f = new(st, wide=1.5 if st == 3 else 0)
    plaid, plaid2, moss = (196, 60, 52), (120, 30, 36), (90, 150, 70)
    if st == 2:
        L = Layer()
        for i, y in enumerate((9, 12, 15)):
            L.ell(13 + i % 2, y, 6, 1.6, WOOD)
        sp.add(L)
    if st == 3:
        L = Layer(); L.poly([(19, 4), (30, 0), (31, 5), (21, 9)], WOOD); L.ell(30, 2, 2, 2.5, lighten(WOOD, .25)); sp.add(L)
    hands = {2: {"r": (24, 17)}, 3: {"r": (24, 9)}}.get(st)
    draw_body(sp, f, hands, legs="wide" if st == 3 else "stand")
    L = Layer()
    tunic(L, f, plaid, bottom=None if st < 3 else 23, flare=1 if st < 3 else 2)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    sx = int(f["shoulder"][0]); ex = int(f["shoulder_r"][0])
    for x in range(sx, ex + 1, 3):
        D.line(x, int(f["shoulder"][1]), x, int(f["pelvis"]), plaid2)
    sp.add(D)
    draw_skull(sp, f, mood="angry" if st >= 2 else "calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        cap(L, f, plaid, depth=0.2); L.ell(hx, hy - ry - 1, 1.6, 1.6, plaid2)
    elif st == 2:
        cap(L, f, (90, 70, 50), depth=0.35)
    else:
        L.poly([(hx - rx, hy + ry * 0.3), (hx + rx, hy + ry * 0.3), (hx + 3, hy + ry + 5), (hx - 3, hy + ry + 5)], moss)
        cap(L, f, (70, 110, 60), depth=0.35)
    sp.add(L)
    L = Layer()
    if st == 1:
        stick(L, 21, 26, 27, 29, WOOD_D); L.line(25, 28, 26, 26, WOOD_D)
    elif st == 2:
        stick(L, 24, 17, 26, 5, WOOD); L.poly([(24, 4), (29, 3), (29, 9), (25, 8)], IRON)
    sp.add(L)
    if st == 3:
        D = Layer(shade=False, outline=False); hx, hy, rx, ry = H(f)
        for x in range(int(hx - 2), int(hx + 3), 2):
            D.px(x, int(hy + ry + 2), darken(moss, .3))
        sp.add(D)
    return sp.image()


def herborista(st):
    sp, f = new(st)
    leaf, apron, flower, bark = (98, 176, 80), (230, 220, 180), (250, 150, 190), (120, 86, 60)
    if st == 3:
        L = Layer()
        stick(L, 16, 12, 16, 3, bark, 2); L.ell(16, 3, 6, 3, leaf); L.ell(11, 5, 3, 2.5, leaf); L.ell(21, 5, 3, 2.5, leaf)
        sp.add(L)
    hands = {2: {"l": (8, 19)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st == 2:
        tunic(L, f, apron, bottom=25, flare=2); L.rect(13, 16, 6, 4, darken(leaf, .1))
    elif st == 3:
        tunic(L, f, (70, 130, 80), bottom=27, flare=2)
    sp.add(L)
    if st == 3:
        D = Layer(shade=False, outline=False)
        for (x, y) in [(13, 15), (19, 16), (16, 18)]:
            D.px(x, y, leaf)
        sp.add(D)
    hx, hy, rx, ry = H(f)
    draw_skull(sp, f, mood="sleepy" if st == 2 else "calm")
    L = Layer()
    if st == 1:
        stick(L, hx, hy - ry, hx, hy - ry - 4, (80, 140, 60)); L.ell(hx - 2.5, hy - ry - 4, 2.5, 1.5, leaf); L.ell(hx + 2.5, hy - ry - 4.5, 2.5, 1.5, leaf)
    elif st == 2:
        L.rect(int(hx - rx), int(hy - ry + 1), int(rx * 2) + 1, 2, leaf)
    else:
        for i, x in enumerate(range(int(hx - rx), int(hx + rx) + 1, 3)):
            L.ell(x + 0.5, hy - ry + 1, 1.5, 1.5, flower if i % 2 == 0 else (255, 230, 120))
    sp.add(L)
    L = Layer()
    if st == 2:
        L.poly([(4, 19), (12, 19), (11, 25), (5, 25)], (190, 150, 90))
        D = None
        L.ell(6, 18, 1.5, 1.5, leaf); L.ell(9, 17, 1.5, 1.5, (200, 120, 80)); L.ell(11, 18, 1.5, 1.5, leaf)
    sp.add(L)
    return sp.image()


def cogumeleiro(st):
    sp, f = new(st)
    red, spot, stem, purple = (210, 60, 70), WHITE, (236, 220, 190), (150, 110, 180)
    if st == 2:
        L = Layer()
        for (x, y, r) in [(10, 13, 2.5), (22, 12, 3), (19, 18, 2)]:
            L.ell(x, y, r + 0.5, r * 0.7, purple)
        sp.add(L)
    hands = {3: {"r": (25, 14)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st >= 2:
        tunic(L, f, (110, 90, 70), flare=1)
    sp.add(L)
    draw_skull(sp, f, mood="sleepy")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        L.ell(hx, hy - ry, rx * 0.8, 3.2, red)
    elif st == 2:
        L.ell(hx, hy - ry + 0.5, rx + 1, 3.0, purple)
    else:
        L.ell(16, 2.5, 15, 4.5, red); L.rect(14, 5, 4, 2, stem)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    if st == 1:
        D.px(int(hx - 2), int(hy - ry - 1), spot); D.px(int(hx + 2), int(hy - ry), spot)
    elif st == 3:
        for (x, y) in [(5, 2), (10, 1), (16, 0), (21, 2), (27, 1), (13, 4)]:
            D.rect(x, y, 2, 1, spot)
    sp.add(D)
    L = Layer()
    if st == 3:
        stick(L, 25, 29, 26, 12, (200, 190, 230)); L.ell(26, 11, 2, 2, purple)
    sp.add(L)
    G = Layer(shade=False, outline=False)
    pts = {1: [(24, 10), (6, 14)], 2: [(4, 6), (27, 5), (25, 9), (7, 10)], 3: [(2, 10), (29, 11), (4, 18), (28, 20), (30, 15)]}[st]
    sparkle(G, pts, (190, 230, 120))
    sp.add(G)
    return sp.image()


def flautista(st):
    sp, f = new(st, lean=0)
    green, leaf, flute, glow = (70, 130, 90), (120, 170, 70), (176, 120, 70), (240, 250, 120)
    if st == 3:
        L = Layer(); cape(L, f, leaf, bottom=29, spread=4); sp.add(L)
    hx, hy, rx, ry = H(f)
    my = int(hy + ry * 0.55)
    hands = {"l": (hx - 4, my + 2), "r": (hx + 6, my + 2)}
    draw_body(sp, f, hands)
    L = Layer()
    if st >= 2:
        tunic(L, f, green, flare=1)
    sp.add(L)
    draw_skull(sp, f, mood="calm")
    L = Layer()
    if st == 1:
        L.ell(hx + 1, hy - ry - 1, 1.5, 1.2, (60, 60, 40))
    elif st == 2:
        cap(L, f, green, depth=0.3); L.poly([(hx + rx - 1, hy - ry + 1), (hx + rx + 4, hy - ry - 3), (hx + rx + 1, hy - ry + 3)], green)
    else:
        stick(L, hx - 3, hy - ry + 1, hx - 7, hy - ry - 4, WOOD); stick(L, hx - 6, hy - ry - 2, hx - 9, hy - ry - 2, WOOD)
        stick(L, hx + 3, hy - ry + 1, hx + 7, hy - ry - 4, WOOD); stick(L, hx + 6, hy - ry - 2, hx + 9, hy - ry - 2, WOOD)
    sp.add(L)
    L = Layer()
    ln_ = {1: 7, 2: 12, 3: 14}[st]
    L.rect(int(hx - 3), my + 1, ln_, 2, flute)
    if st == 3:
        stick(L, hx + ln_ - 3, my + 2, hx + ln_ - 1, 29, WOOD)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    for i in range(int(hx - 1), int(hx - 3 + ln_), 2):
        D.px(i, my + 1, (90, 70, 60))
    sp.add(D)
    G = Layer(shade=False, outline=False)
    pts = {1: [(int(hx + 1), int(hy - ry - 2))], 2: [(4, 6), (27, 4), (29, 14), (3, 16)], 3: [(2, 4), (29, 3), (30, 12), (1, 14), (28, 22), (3, 24)]}[st]
    for (x, y) in pts:
        G.px(x, y, glow); G.px(x + 1, y, (200, 220, 90))
    sp.add(G)
    return sp.image()


# ------------------------------------------------------------------ MINAS
def mineiro(st):
    sp, f = new(st, wide=2 if st == 3 else 0)
    pail, helm, stone, stone2 = (130, 150, 170), (230, 190, 60), (130, 120, 112), (100, 92, 86)
    if st == 2:
        L = Layer(); stick(L, 6, 18, 24, 6, WOOD); L.poly([(21, 3), (27, 7), (25, 9), (22, 6)], IRON); sp.add(L)
    hands = {2: {"r": (21, 10), "l": (9, 20)}, 3: {"r": (26, 18), "l": (6, 18)}}.get(st)
    draw_body(sp, f, hands, legs="wide" if st == 3 else "stand")
    L = Layer()
    if st == 2:
        tunic(L, f, (90, 110, 150))
    elif st == 3:
        tunic(L, f, stone, bottom=23, flare=3)
        L.ell(f["shoulder"][0], f["shoulder"][1], 3.5, 2.5, stone2); L.ell(f["shoulder_r"][0], f["shoulder_r"][1], 3.5, 2.5, stone2)
    sp.add(L)
    if st == 3:
        D = Layer(shade=False, outline=False)
        for (x0, y0, x1, y1) in [(10, 15, 14, 17), (18, 13, 21, 16), (12, 20, 19, 21)]:
            D.line(x0, y0, x1, y1, stone2)
        sp.add(D)
    draw_skull(sp, f, mood="angry" if st == 3 else "calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        L.poly([(hx - rx, hy - ry * 0.25), (hx + rx, hy - ry * 0.25), (hx + rx - 1.5, hy - ry - 3), (hx - rx + 1.5, hy - ry - 3)], pail)
        stick(L, hx - rx, hy - ry * 0.25, hx - rx - 1, hy - 1, IRON)
    else:
        cap(L, f, helm if st == 2 else stone2, depth=0.3, extra=0.9)
        L.rect(int(hx - rx - 1), int(hy - ry * 0.3), int(rx * 2) + 3, 1, helm if st == 2 else stone2)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    if st >= 2:
        D.rect(int(hx - 1), int(hy - ry - 0.5), 3, 2, (255, 250, 200))
    sp.add(D)
    L = Layer()
    if st == 3:
        stick(L, 26, 29, 26, 9, WOOD, 2); L.poly([(21, 8), (31, 8), (31, 10), (21, 10)], IRON); L.px(21, 11, IRON); L.px(31, 11, IRON)
    sp.add(L)
    return sp.image()


def ferreiro(st):
    sp, f = new(st, wide=1 if st == 3 else 0)
    leather, coal = (130, 84, 50), (60, 56, 60)
    if st == 2:
        L = Layer(); L.poly([(7, 6), (17, 6), (19, 9), (15, 10), (15, 13), (9, 13), (9, 10), (5, 9)], IRON); sp.add(L)
    hands = {1: {"r": (24, 16)}, 2: {"r": (24, 22), "l": (8, 22)}, 3: {"r": (25, 7)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st == 1:
        L.poly([(11, 18), (21, 18), (23, 30), (9, 30)], leather)
    elif st == 2:
        tunic(L, f, leather, bottom=26, flare=1)
    else:
        L.ell(f["ribs"][0], f["ribs"][1], f["rr"][0], f["rr"][1], coal)
    sp.add(L)
    if st == 3:
        G = Layer(shade=False, outline=False)
        cx, cy = f["ribs"]
        G.ell(cx, cy + 1, 3.5, 2.5, FLAME); G.ell(cx, cy + 1.5, 2, 1.4, (255, 236, 130))
        for y in range(int(cy - 4), int(cy + 5), 2):
            G.line(cx - 6, y, cx + 6, y, BONE)
        sp.add(G)
    draw_skull(sp, f, mood="angry" if st >= 2 else "calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st >= 2:
        L.rect(int(hx - rx), int(hy - ry * 0.6), int(rx * 2) + 1, 2, (70, 60, 70))
    sp.add(L)
    D = Layer(shade=False, outline=False)
    if st >= 2:
        D.rect(int(hx - 3), int(hy - ry * 0.6), 2, 2, GLASS); D.rect(int(hx + 1), int(hy - ry * 0.6), 2, 2, GLASS)
    sp.add(D)
    L = Layer()
    if st == 1:
        stick(L, 24, 16, 25, 11, WOOD); L.rect(23, 9, 5, 3, IRON)
    elif st == 2:
        L.poly([(24, 18), (29, 20), (29, 24), (24, 25)], leather); stick(L, 22, 22, 24, 21, WOOD)
    else:
        stick(L, 25, 7, 26, 18, WOOD, 2); L.rect(22, 2, 9, 5, (90, 70, 70))
    sp.add(L)
    G = Layer(shade=False, outline=False)
    if st == 1:
        sparkle(G, [(28, 8), (22, 7), (27, 13)], FLAME)
    elif st == 3:
        G.rect(23, 3, 7, 3, FLAME); sparkle(G, [(21, 1), (31, 2), (29, 0)], (255, 236, 130))
    sp.add(G)
    return sp.image()


def gasista(st):
    sp, f = new(st)
    suit, mask, fog, tank = (196, 170, 90), (90, 96, 104), (150, 210, 110), (110, 140, 100)
    if st == 2:
        L = Layer(); L.rect(19, 9, 6, 12, tank); L.ell(22, 9, 3, 1.5, lighten(tank, .2)); sp.add(L)
    if st == 3:
        L = Layer(); L.rect(5, 1, 4, 14, IRON); L.rect(23, 1, 4, 14, IRON); L.rect(4, 0, 6, 2, darken(IRON, .2)); L.rect(22, 0, 6, 2, darken(IRON, .2)); sp.add(L)
    hands = {1: {"r": (22, 22)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st >= 2:
        tunic(L, f, suit, flare=1)
    sp.add(L)
    draw_skull(sp, f, mood="calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    my = hy + ry * 0.35
    L.ell(hx, my, rx * 0.7, ry * 0.5, mask)
    r = {1: 2.2, 2: 2.0, 3: 2.6}[st]
    L.ell(hx, my + ry * 0.4 + 1, r, r, darken(mask, .25))
    if st == 3:
        L.ell(hx - 4, my + 2, 2, 1.6, mask); L.ell(hx + 4, my + 2, 2, 1.6, mask)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    D.px(int(hx), int(my + ry * 0.4 + 1), (40, 40, 40))
    sp.add(D)
    L = Layer()
    if st == 1:
        L.rect(21, 22, 6, 6, (180, 150, 80)); L.rect(21, 22, 6, 1, IRON)
    elif st == 2:
        stick(L, 20, 17, 13, 20, (60, 60, 60))
    sp.add(L)
    if st == 1:
        D = Layer(shade=False, outline=False)
        for x in (22, 24, 26):
            D.line(x, 23, x, 27, (120, 100, 60))
        sp.add(D)
    G = Layer(shade=False, outline=False)
    if st == 2:
        sparkle(G, [(22, 6), (24, 4), (21, 3)], fog)
    elif st == 3:
        for (x, y) in [(6, -1), (24, -1)]:
            G.ell(x + 2, 1, 3, 1.5, fog)
        sparkle(G, [(2, 3), (30, 2), (9, 4)], fog)
    sp.add(G)
    return sp.image()


def aguadeiro(st):
    sp, f = new(st, wide=1 if st == 3 else 0)
    canteen, water, clay, cist = (90, 140, 120), (100, 180, 230), (190, 110, 80), (120, 150, 180)
    if st == 3:
        L = Layer(); L.ell(16, 11, 10, 9, cist); L.rect(13, 1, 6, 2, IRON); sp.add(L)
        D = Layer(shade=False, outline=False)
        for y in (6, 11, 16):
            D.line(7, y, 25, y, darken(cist, .3))
        sp.add(D)
    hands = {2: {"l": (6, 22), "r": (8, 23)}, 3: {"r": (26, 21)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st == 1:
        stick(L, 12, 19, 20, 24, (110, 80, 50)); L.ell(19, 25, 4, 4, canteen); L.rect(18, 20, 2, 2, IRON)
    elif st == 2:
        tunic(L, f, (120, 160, 190))
    else:
        tunic(L, f, (60, 100, 140), bottom=23, flare=2)
    sp.add(L)
    draw_skull(sp, f, mood="calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        cap(L, f, (200, 200, 220), depth=0.4)
    elif st == 2:
        cap(L, f, (220, 200, 140), depth=0.3, extra=1.5)
    else:
        L.rect(int(hx - rx), int(hy - ry + 1), int(rx * 2) + 1, 2, water)
    sp.add(L)
    L = Layer()
    if st == 2:
        L.poly([(1, 22), (14, 22), (13, 27), (2, 27)], WOOD); L.ell(4, 28.5, 1.5, 1.5, (80, 80, 80))
        L.ell(5, 20, 2.5, 3, clay); L.ell(10, 20, 2.5, 3, clay)
    elif st == 3:
        stick(L, 24, 8, 27, 20, (70, 90, 110)); L.rect(25, 20, 3, 3, IRON)
    sp.add(L)
    G = Layer(shade=False, outline=False)
    if st == 3:
        sparkle(G, [(28, 24), (29, 26), (27, 27), (30, 23)], water)
    elif st == 1:
        G.px(18, 23, WHITE)
    sp.add(G)
    return sp.image()


# ------------------------------------------------------------------ PÂNTANO
def lavadeira(st):
    sp, f = new(st)
    tub, herb, dress, kerchief = (150, 170, 190), (110, 160, 70), (110, 90, 150), (230, 150, 70)
    if st == 3:
        L = Layer(); L.ell(16, 12, 10, 7, (90, 96, 104)); L.rect(6, 7, 20, 3, darken((90, 96, 104), .2)); stick(L, 3, 1, 29, 1, WOOD); stick(L, 3, 1, 3, 9, WOOD); stick(L, 29, 1, 29, 9, WOOD); sp.add(L)
        G = Layer(shade=False, outline=False)
        G.ell(16, 7, 8, 1.5, (150, 220, 100))
        for x in (6, 11, 20, 25):
            G.line(x, 2, x, 5, herb)
        sp.add(G)
    hands = {2: {"l": (8, 18), "r": (23, 18)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st == 1:
        tunic(L, f, dress, bottom=27, flare=2)
    else:
        L.poly([(f["shoulder"][0], f["shoulder"][1] - 1), (f["shoulder_r"][0], f["shoulder_r"][1] - 1), (24, 29), (8, 29)], dress)
    sp.add(L)
    draw_skull(sp, f)
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        L.poly([(hx - rx - 1, hy - ry + 2), (hx + rx + 1, hy - ry + 2), (hx + rx - 1, hy - ry - 2), (hx - rx + 1, hy - ry - 2)], tub)
    else:
        cap(L, f, kerchief, depth=0.25, extra=0.8); L.poly([(hx + rx - 1, hy - ry * 0.3), (hx + rx + 3, hy), (hx + rx, hy + 1)], kerchief)
    sp.add(L)
    L = Layer()
    if st == 2:
        L.rect(9, 17, 14, 4, (200, 190, 150))
        for x in range(10, 22, 2):
            L.px(x, 18, darken((200, 190, 150), .2))
        L.ell(5, 23, 3, 2.5, (190, 150, 90)); L.ell(4, 21, 1.5, 1.5, herb); L.ell(6, 20.5, 1.5, 1.5, herb)
    sp.add(L)
    return sp.image()


def palafiteiro(st):
    sp, f = new(st)
    straw, shirt = (230, 200, 110), (110, 140, 90)
    if st == 3:
        # pernas-de-pau: o corpo sobe e as estacas vão até o chão
        f = body_frame(2)
        for k in ("head", "ribs", "shoulder", "shoulder_r", "hand_l", "hand_r", "head_top"):
            f[k] = (f[k][0], f[k][1] - 3)
        f["pelvis"] -= 3
        f["stage"] = 3
        L = Layer(); stick(L, 13, 17, 12, 31, WOOD, 2); stick(L, 19, 17, 20, 31, WOOD, 2); L.rect(10, 22, 5, 1, WOOD_D); L.rect(18, 22, 5, 1, WOOD_D); sp.add(L)
    if st == 2:
        L = Layer()
        for x in (7, 9, 11):
            stick(L, x, 4, x + 1, 20, WOOD)
        sp.add(L)
    hands = {1: {"r": (21, 19)}, 2: {"r": (24, 19)}, 3: {"r": (24, 14)}}.get(st)
    if st == 3:
        draw_body(sp, f, hands, legs="none")
    else:
        draw_body(sp, f, hands)
    L = Layer()
    if st >= 2:
        tunic(L, f, shirt, flare=1)
    sp.add(L)
    draw_skull(sp, f, mood="sleepy" if st == 1 else "calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 3:
        L.ell(hx, hy - ry * 0.4, rx + 4, 1.6, straw); L.ell(hx, hy - ry * 0.8, rx * 0.7, 2.2, straw)
    elif st == 2:
        L.rect(int(hx - rx), int(hy - ry + 1), int(rx * 2) + 1, 2, shirt)
    sp.add(L)
    L = Layer()
    if st == 1:
        stick(L, 18, 25, 25, 13, WOOD, 2); L.px(25, 12, WOOD_D)
    elif st == 2:
        stick(L, 24, 19, 26, 9, WOOD); L.rect(23, 6, 7, 4, IRON)
    else:
        stick(L, 24, 14, 26, 2, WOOD, 2); L.rect(22, 0, 9, 5, (110, 100, 96))
    sp.add(L)
    return sp.image()


def jardineiro_lirios(st):
    sp, f = new(st)
    pad, pad2, lily, gourd = (90, 170, 100), (60, 130, 80), (250, 190, 220), (210, 170, 90)
    if st == 3:
        L = Layer(); stick(L, 25, 26, 25, 4, (90, 140, 80), 1); L.ell(16, 3.5, 15, 4, pad); sp.add(L)
        D = Layer(shade=False, outline=False); D.line(16, 3, 30, 1, pad2); D.ell(9, 2, 2, 1.2, lily); sp.add(D)
    hands = {2: {"r": (23, 16)}, 3: {"r": (25, 15)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st >= 2:
        tunic(L, f, (70, 110, 120), flare=1)
    if st == 2:
        L.ell(f["shoulder"][0], f["shoulder"][1] - 0.5, 2, 2, lily); L.ell(f["shoulder_r"][0] - 1, f["shoulder_r"][1] - 0.5, 2, 2, lily)
    sp.add(L)
    draw_skull(sp, f, mood="sleepy")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        L.ell(hx, hy - ry + 0.5, rx + 2.5, 2.2, pad)
    elif st == 2:
        L.ell(hx, hy - ry + 0.5, rx + 1, 1.8, pad2); L.ell(hx + 2, hy - ry - 1, 1.5, 1.5, lily)
    sp.add(L)
    if st == 1:
        D = Layer(shade=False, outline=False); D.line(hx, hy - ry, hx + rx + 2, hy - ry + 1, pad2); sp.add(D)
    L = Layer()
    if st == 2:
        L.ell(25, 17, 3, 3.5, gourd); stick(L, 27, 15, 30, 12, gourd)
    sp.add(L)
    G = Layer(shade=False, outline=False)
    if st == 2:
        sparkle(G, [(30, 14), (31, 16), (29, 17)], (130, 200, 240))
    sp.add(G)
    return sp.image()


# ------------------------------------------------------------------ OSSÓRIO
def sentinela(st):
    sp, f = new(st, wide=1 if st == 3 else 0)
    steel, blue, red = (170, 176, 190), (60, 80, 150), (180, 60, 60)
    if st == 3:
        L = Layer(); stick(L, 26, 30, 26, 0, WOOD); L.poly([(27, 0), (31, 2), (27, 5)], red); sp.add(L)
    hands = {2: {"r": (24, 20)}, 3: {"r": (26, 15)}}.get(st)
    draw_body(sp, f, hands, legs="wide" if st == 3 else "stand")
    L = Layer()
    if st >= 2:
        tunic(L, f, blue, flare=1)
    sp.add(L)
    draw_skull(sp, f, mood="angry" if st >= 2 else "calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        L.rect(int(hx - rx * 0.6), int(hy - ry - 1), int(rx * 1.2) + 1, 2, red)
    else:
        cap(L, f, steel, depth=0.15, extra=0.8)
        L.rect(int(hx - 0.5), int(hy - ry - 3), 2, 3, red)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    if st >= 2:
        D.line(hx, hy - ry, hx, hy - ry * 0.2, darken(steel, .3))
    sp.add(D)
    L = Layer()
    if st == 1:
        L.ell(9, 23, 4, 4, IRON); L.ell(9, 23, 1, 1, darken(IRON, .3))
    elif st == 2:
        L.poly([(3, 12), (12, 12), (12, 26), (7.5, 29), (3, 26)], steel)
        stick(L, 24, 29, 24, 4, WOOD); L.poly([(23, 4), (25, 4), (24, 1)], IRON)
    else:
        L.rect(1, 6, 13, 22, (120, 96, 70)); L.rect(1, 6, 13, 2, IRON); L.rect(1, 26, 13, 2, IRON)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    if st == 2:
        D.line(7, 14, 7, 25, red); D.line(4, 18, 11, 18, red)
    elif st == 3:
        for x in (4, 8, 11):
            D.line(x, 8, x, 25, darken((120, 96, 70), .25))
        D.ell(7.5, 16, 2, 2, GOLD)
    sp.add(D)
    return sp.image()


def escriba(st):
    sp, f = new(st)
    robe, ink, parch, quill = (90, 80, 120), (40, 40, 70), (236, 220, 180), (250, 250, 250)
    if st == 3:
        L = Layer()
        for i, x in enumerate((6, 10, 22, 26)):
            L.rect(x - 2, 8 + (i % 2) * 2, 4, 20 - (i % 2) * 2, parch)
        sp.add(L)
    hands = {2: {"l": (9, 21), "r": (23, 21)}, 3: {"r": (24, 16)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st >= 2:
        L.poly([(f["shoulder"][0], f["shoulder"][1] - 1), (f["shoulder_r"][0], f["shoulder_r"][1] - 1), (23, 29), (9, 29)], robe)
    sp.add(L)
    draw_skull(sp, f, mood="calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        L.poly([(hx + 2, hy - ry + 1), (hx + 7, hy - ry - 6), (hx + 6, hy - ry - 1)], quill)
    elif st == 2:
        cap(L, f, robe, depth=0.35)
    else:
        L.rect(int(hx - 3), int(hy - ry - 4), 7, 5, ink); L.rect(int(hx - 2), int(hy - ry - 5), 5, 1, IRON)
        L.poly([(hx + 1, hy - ry - 5), (hx + 6, hy - ry - 11), (hx + 4, hy - ry - 5)], quill)
    sp.add(L)
    L = Layer()
    if st == 2:
        L.poly([(9, 17), (16, 18), (16, 25), (9, 24)], parch); L.poly([(16, 18), (23, 17), (23, 24), (16, 25)], parch)
    elif st == 3:
        stick(L, 24, 16, 28, 8, quill)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    if st == 2:
        for y in (19, 21):
            D.line(10, y, 14, y + 0.5, ink); D.line(18, y + 0.5, 22, y, ink)
        sparkle(D, [(8, 15), (24, 14), (16, 16)], GOLD)
    elif st == 3:
        for x in (6, 10, 22, 26):
            D.line(x - 1, 12, x + 1, 12, ink); D.line(x - 1, 15, x + 1, 15, ink)
    sp.add(D)
    return sp.image()


def sineiro(st):
    sp, f = new(st)
    bronze, robe, rope = (200, 150, 70), (150, 70, 60), (220, 200, 150)
    if st == 3:
        L = Layer(); L.poly([(9, 3), (23, 3), (27, 22), (5, 22)], bronze); L.rect(4, 21, 24, 3, darken(bronze, .1)); L.rect(14, 0, 4, 3, darken(bronze, .2)); sp.add(L)
        D = Layer(shade=False, outline=False); D.line(7, 18, 25, 18, darken(bronze, .3)); sp.add(D)
    hands = {2: {"r": (23, 9)}, 3: {"r": (26, 20)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st >= 2:
        tunic(L, f, robe, bottom=26, flare=2)
    sp.add(L)
    draw_skull(sp, f, mood="calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        L.rect(12, 19, 9, 2, robe); L.poly([(14.5, 20), (18.5, 20), (19.5, 25), (13.5, 25)], bronze)
    elif st == 2:
        cap(L, f, robe, depth=0.3)
    sp.add(L)
    L = Layer()
    if st == 2:
        stick(L, 23, 9, 24, 4, WOOD); L.poly([(21, 0), (27, 0), (29, 6), (19, 6)], bronze)
    elif st == 3:
        stick(L, 26, 20, 26, 28, rope, 1); L.ell(26, 28, 2, 2, IRON)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    if st == 1:
        D.px(16, 25, OUTL)
    elif st == 2:
        D.px(24, 7, OUTL); sparkle(D, [(18, 1), (30, 2)], GOLD)
    sp.add(D)
    return sp.image()


# ------------------------------------------------------------------ PICOS
def carregador(st):
    sp, f = new(st, wide=1 if st == 3 else 0)
    pack, scarf, pot = (170, 110, 70), (200, 70, 70), (120, 124, 130)
    L = Layer()
    if st == 1:
        L.rect(16, 18, 9, 9, pack)
    elif st == 2:
        L.rect(15, 3, 12, 20, pack); L.ell(21, 3, 6, 2, darken(pack, .1)); L.ell(28, 9, 2.5, 2, pot); L.ell(28, 14, 2.5, 2, pot)
    else:
        L.rect(10, 0, 16, 25, (150, 100, 70)); L.poly([(9, 1), (18, -4), (27, 1)], (180, 70, 60)); L.rect(16, 6, 5, 5, (240, 220, 140))
    sp.add(L)
    hands = {2: {"l": (7, 19)}, 3: {"l": (5, 16)}}.get(st)
    draw_body(sp, f, hands, legs="wide" if st == 3 else "stand")
    L = Layer()
    tunic(L, f, (90, 110, 140), flare=1)
    L.rect(int(f["shoulder"][0]), int(f["shoulder"][1] - 1), int(f["shoulder_r"][0] - f["shoulder"][0]) + 1, 2, scarf)
    if st == 1:
        L.rect(int(f["shoulder_r"][0] - 2), int(f["shoulder"][1] + 1), 2, 4, scarf)
    sp.add(L)
    draw_skull(sp, f, mood="calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    cap(L, f, (230, 220, 200) if st < 3 else (120, 90, 70), depth=0.3)
    if st == 1:
        L.ell(hx, hy - ry - 1, 1.6, 1.6, scarf)
    sp.add(L)
    L = Layer()
    if st == 2:
        stick(L, 7, 19, 4, 29, WOOD); L.poly([(3, 18), (9, 17), (9, 18), (4, 20)], IRON)
    elif st == 3:
        stick(L, 5, 16, 4, 30, (180, 220, 240), 2); L.ell(5, 14, 2.5, 2.5, GLASS)
    sp.add(L)
    return sp.image()


def escultor(st):
    sp, f = new(st)
    ice, ice2, smock, crystal = (190, 230, 250), (130, 190, 230), (90, 130, 170), (220, 246, 255)
    if st == 2:
        L = Layer(); L.poly([(12, 13), (1, 5), (2, 13), (9, 18)], ice); L.poly([(20, 13), (31, 5), (30, 13), (23, 18)], ice); sp.add(L)
        D = Layer(shade=False, outline=False); D.line(3, 7, 10, 14, ice2); D.line(29, 7, 22, 14, ice2); sp.add(D)
    hands = {1: {"r": (22, 22)}, 3: {"r": (25, 12)}}.get(st)
    bone = crystal if st == 3 else BONE
    draw_body(sp, f, hands, bone=bone)
    L = Layer()
    if st < 3:
        tunic(L, f, smock, flare=1)
    else:
        tunic(L, f, ice2, bottom=22, flare=2)
    sp.add(L)
    draw_skull(sp, f, mood="calm", bone=bone)
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        L.rect(int(hx - rx + 1), int(hy - ry - 3), int(rx * 2) - 1, 5, ice)
    elif st == 2:
        cap(L, f, smock, depth=0.4)
    else:
        for i, x in enumerate(range(int(hx - rx), int(hx + rx) + 1, 2)):
            L.poly([(x, hy - ry + 1), (x + 1.5, hy - ry + 1), (x + 0.75, hy - ry - 3 - (i % 2) * 2)], ice)
    sp.add(L)
    L = Layer()
    if st == 1:
        stick(L, 22, 22, 25, 18, IRON)
    elif st == 3:
        L.poly([(25, 12), (29, 4), (31, 6)], crystal)
    sp.add(L)
    G = Layer(shade=False, outline=False)
    if st == 1:
        G.px(int(hx - rx + 2), int(hy - ry - 2), WHITE)
    elif st == 3:
        sparkle(G, [(3, 6), (28, 18), (5, 22), (30, 2)], WHITE)
    sp.add(G)
    return sp.image()


def chazeiro(st):
    sp, f = new(st, wide=1 if st == 3 else 0)
    cup, blanket, kettle, sam = (240, 240, 250), (170, 90, 80), (200, 120, 70), (200, 150, 60)
    if st == 3:
        L = Layer(); L.ell(16, 12, 9, 10, sam); L.rect(13, 0, 6, 3, darken(sam, .2)); L.rect(24, 13, 4, 2, darken(sam, .2)); sp.add(L)
        D = Layer(shade=False, outline=False); D.line(8, 9, 24, 9, darken(sam, .3)); D.line(8, 15, 24, 15, darken(sam, .3)); sp.add(D)
    hands = {2: {"r": (23, 19)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st == 2:
        L.poly([(f["shoulder"][0] - 2, f["shoulder"][1] - 2), (f["shoulder_r"][0] + 2, f["shoulder_r"][1] - 2), (24, 27), (8, 27)], blanket)
    elif st == 3:
        tunic(L, f, (110, 70, 60), bottom=23, flare=2)
    sp.add(L)
    if st == 2:
        D = Layer(shade=False, outline=False)
        for y in (17, 21, 25):
            D.line(9, y, 23, y, darken(blanket, .25))
        sp.add(D)
    draw_skull(sp, f, mood="sleepy" if st == 2 else "calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        L.poly([(hx - rx + 1, hy - ry + 1), (hx + rx - 1, hy - ry + 1), (hx + rx - 2, hy - ry - 4), (hx - rx + 2, hy - ry - 4)], cup)
        L.ell(hx + rx, hy - ry - 1.5, 1.5, 1.5, cup)
    elif st == 3:
        cap(L, f, (110, 70, 60), depth=0.35)
    sp.add(L)
    if st == 1:
        D = Layer(shade=False, outline=False); D.line(hx - rx + 2, hy - ry - 1, hx + rx - 2, hy - ry - 1, (120, 160, 220)); sp.add(D)
    L = Layer()
    if st == 2:
        L.ell(25, 20, 4, 3.5, kettle); L.poly([(28, 19), (31, 16), (31, 18), (29, 21)], kettle); L.rect(24, 15, 3, 2, darken(kettle, .2))
    sp.add(L)
    G = Layer(shade=False, outline=False)
    steam = {1: [], 2: [(30, 13), (31, 11), (30, 9)], 3: [(15, -1), (17, 0), (28, 10), (30, 8), (29, 6)]}[st]
    sparkle(G, [p for p in steam if p[1] >= 0], WHITE)
    sp.add(G)
    return sp.image()


# ------------------------------------------------------------------ DESERTO
def domador_escorpioes(st):
    sp, f = new(st, lean=1 if st == 3 else 0)
    sand, cloth, scorp, scorp2 = (220, 180, 110), (190, 120, 60), (180, 90, 50), (140, 60, 40)
    if st == 3:
        L = Layer()
        L.ell(16, 24, 12, 4, scorp)
        for x in (5, 9, 23, 27):
            stick(L, x, 25, x + (-2 if x < 16 else 2), 29, scorp2)
        L.poly([(2, 20), (6, 18), (7, 22)], scorp); L.poly([(30, 20), (26, 18), (25, 22)], scorp)
        sp.add(L)
        L = Layer()
        pts = [(26, 22), (29, 15), (28, 7), (23, 2), (18, 2)]
        for a, b in zip(pts, pts[1:]):
            stick(L, a[0], a[1], b[0], b[1], scorp, 2)
        L.poly([(18, 0), (14, 3), (18, 5)], scorp2)
        sp.add(L)
    hands = {2: {"r": (24, 21)}}.get(st)
    draw_body(sp, f, hands, legs="wide" if st == 3 else "stand")
    L = Layer()
    tunic(L, f, cloth if st < 3 else (120, 70, 50), flare=1)
    sp.add(L)
    draw_skull(sp, f, mood="angry" if st >= 2 else "calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    cap(L, f, sand, depth=0.15 if st == 1 else 0.3, extra=0.9)
    if st == 1:
        pts = [(hx + rx - 1, hy - ry + 1), (hx + rx + 3, hy - ry - 2), (hx + rx + 2, hy - ry - 6), (hx + rx - 1, hy - ry - 7)]
        for a, b in zip(pts, pts[1:]):
            stick(L, a[0], a[1], b[0], b[1], cloth)
        L.poly([(hx + rx - 1, hy - ry - 9), (hx + rx - 4, hy - ry - 7), (hx + rx - 1, hy - ry - 5)], cloth)
    sp.add(L)
    L = Layer()
    if st == 2:
        sx, sy = f["shoulder"]
        L.ell(sx - 1, sy - 2, 3, 2, scorp); L.ell(sx - 3, sy - 5, 1.5, 3, scorp)
        stick(L, sx - 3, sy - 8, sx, sy - 9, scorp); L.px(int(sx + 1), int(sy - 9), scorp2)
        stick(L, 24, 21, 27, 29, (120, 80, 50)); stick(L, 27, 29, 30, 26, (120, 80, 50))
    sp.add(L)
    return sp.image()


def cartografo(st):
    sp, f = new(st)
    coat, brass, mapc = (90, 110, 90), (210, 170, 80), (236, 220, 170)
    if st == 3:
        L = Layer(); cape(L, f, mapc, bottom=29, spread=4); sp.add(L)
        D = Layer(shade=False, outline=False)
        for (x0, y0, x1, y1) in [(7, 18, 12, 24), (21, 17, 26, 22), (8, 26, 14, 27), (20, 25, 25, 28)]:
            D.line(x0, y0, x1, y1, (180, 120, 90))
        sp.add(D)
        L = Layer(); L.ell(16, 16, 15, 3, (0, 0, 0)); sp.base  # placeholder (não usado)
    hands = {1: {"l": (12, 25), "r": (20, 25)}, 2: {"r": (22, 8), "l": (9, 20)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st == 2:
        tunic(L, f, coat, flare=1)
    elif st == 3:
        tunic(L, f, (70, 80, 110), bottom=24, flare=2)
    sp.add(L)
    draw_skull(sp, f, mood="calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st >= 2:
        cap(L, f, (150, 110, 70), depth=0.4); L.rect(int(hx - rx - 2), int(hy - ry * 0.4), int(rx * 2) + 5, 1, (150, 110, 70))
    sp.add(L)
    L = Layer()
    if st == 1:
        L.ell(16, 25, 5, 4.5, brass); L.ell(16, 25, 3.5, 3, (240, 240, 230))
    elif st == 2:
        stick(L, 22, 8, 27, 3, brass, 2); L.rect(4, 19, 8, 3, mapc)
    else:
        # astrolábio em volta do corpo
        for i in range(40):
            import math
            a = i / 40 * math.tau
            x = 16 + math.cos(a) * 14
            y = 15 + math.sin(a) * 4
            if not (11 < x < 21 and y > 15):
                L.px(int(x), int(y), brass)
        L.ell(29, 15, 1.8, 1.8, GOLD); L.ell(3, 15, 1.5, 1.5, GLASS)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    if st == 1:
        D.line(16, 25, 18, 23, (200, 60, 60)); D.line(16, 25, 14, 27, OUTL)
    sp.add(D)
    return sp.image()


def tamborileiro(st):
    sp, f = new(st)
    drum, skin, band, sash = (190, 90, 60), (240, 220, 170), (240, 196, 72), (80, 160, 190)
    if st == 3:
        L = Layer(); L.ell(16, 9, 11, 8, drum); L.ell(16, 4, 11, 3, skin); sp.add(L)
        D = Layer(shade=False, outline=False)
        for x in range(7, 26, 4):
            D.line(x, 6, x + 2, 16, band)
        sp.add(D)
    hands = {2: {"l": (8, 10), "r": (24, 10)}, 3: {"l": (7, 19), "r": (25, 19)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st >= 2:
        tunic(L, f, (220, 200, 160) if st == 2 else (200, 80, 70), flare=1)
    sp.add(L)
    if st == 3:
        L = Layer(); L.poly([(8, 12), (10, 12), (4, 26), (2, 25)], sash); L.poly([(22, 12), (24, 12), (30, 26), (28, 27)], (230, 120, 60)); sp.add(L)
    draw_skull(sp, f, mood="calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st >= 2:
        L.rect(int(hx - rx), int(hy - ry + 1), int(rx * 2) + 1, 2, sash)
        L.poly([(hx - rx, hy - ry + 2), (hx - rx - 4, hy - ry + 5), (hx - rx - 1, hy - ry + 4)], sash)
    sp.add(L)
    L = Layer()
    if st == 1:
        L.ell(16, 23.5, 5, 3.5, drum); L.ell(16, 21.5, 5, 1.5, skin)
    elif st == 2:
        L.ell(11, 23, 3.5, 3, drum); L.ell(21, 23, 3.5, 3, drum); L.ell(11, 21.5, 3.5, 1.2, skin); L.ell(21, 21.5, 3.5, 1.2, skin)
        stick(L, 8, 10, 6, 4, WOOD); stick(L, 24, 10, 26, 4, WOOD); L.px(6, 3, skin); L.px(26, 3, skin)
    sp.add(L)
    G = Layer(shade=False, outline=False)
    if st == 2:
        sparkle(G, [(4, 2), (28, 2)], WHITE)
    sp.add(G)
    return sp.image()


# ------------------------------------------------------------------ ÚNICOS e REI
# ------------------------------------------------------------------ novas linhas (refino geral)
def apicultora(st):
    sp, f = new(st)
    honey, veil, straw, comb = (240, 180, 50), (226, 232, 220), (210, 180, 110), (230, 170, 60)
    hands = {1: {"l": (11, 22), "r": (21, 22)}, 2: {"r": (24, 18)}, 3: {"l": (7, 16), "r": (25, 16)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st == 2:
        tunic(L, f, (236, 226, 190))
    elif st == 3:
        cape(L, f, comb, bottom=27, spread=4)
    sp.add(L)
    if st == 3:
        D = Layer(shade=False, outline=False)
        for (x, y) in [(10, 18), (14, 20), (18, 18), (22, 20), (12, 23), (20, 23)]:
            D.rect(x, y, 2, 2, darken(comb, .25))
        sp.add(D)
    draw_skull(sp, f, mood="happy" if st == 1 else "calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        L.ell(16, 23, 4.5, 3.5, honey); L.rect(13, 19, 7, 2, straw)
    elif st == 2:
        L.ell(hx, hy - ry + 1, rx + 4, 2, straw); cap(L, f, straw, depth=0.45)
    else:
        L.ell(hx, hy - ry + 0.5, 5.5, 4.2, comb); L.ell(hx, hy - ry - 2.5, 3.8, 2.6, comb); L.rect(int(hx - 6), int(hy - ry + 3), 13, 2, straw)
    sp.add(L)
    D = Layer(shade=False, outline=False); hx, hy, rx, ry = H(f)
    if st == 2:
        for x in range(int(hx - rx - 3), int(hx + rx + 4), 2):
            D.line(x, hy - ry + 2, x, hy + 1, veil)
        D.rect(24, 15, 2, 3, IRON); sparkle(D, [(25, 13), (26, 11)], (210, 210, 210))
    elif st == 3:
        for y in (int(hy - ry - 3), int(hy - ry), int(hy - ry + 2)):
            D.line(hx - 4, y, hx + 4, y, darken(comb, .35))
        D.rect(int(hx - 1), int(hy - ry + 1), 2, 2, (60, 40, 20))
        sparkle(D, [(5, 8), (27, 6), (24, 3)], (60, 50, 30))
    else:
        sparkle(D, [(21, 18), (23, 15)], (60, 50, 30))
    sp.add(D)
    return sp.image()


def vitralista(st):
    sp, f = new(st)
    blue, red, green, gold, leather = (90, 150, 230), (220, 80, 90), (90, 190, 120), (240, 200, 80), (140, 96, 64)
    if st == 3:
        L = Layer(); hx, hy, rx, ry = H(f)
        L.ell(hx, hy, rx + 6, ry + 6, gold); sp.add(L)
        D = Layer(shade=False, outline=False)
        for k, c in enumerate([blue, red, green, blue, red, green, blue, red]):
            import math as _m
            a = k / 8 * 6.283
            D.ell(hx + _m.cos(a) * (rx + 3.5), hy + _m.sin(a) * (ry + 3.5), 2, 2, c)
        sp.add(D)
    if st == 2:
        L = Layer(); L.rect(19, 9, 9, 13, gold); sp.add(L)
        D = Layer(shade=False, outline=False); D.rect(20, 10, 3, 5, blue); D.rect(24, 10, 3, 5, red); D.rect(20, 16, 7, 5, green); sp.add(D)
    hands = {1: {"r": (21, 13)}, 3: {"l": (8, 21), "r": (24, 21)}}.get(st)
    draw_body(sp, f, hands)
    L = Layer()
    if st == 2:
        tunic(L, f, leather)
    elif st == 3:
        cape(L, f, (120, 90, 170), bottom=28, spread=3)
    sp.add(L)
    if st == 3:
        D = Layer(shade=False, outline=False); D.line(11, 20, 21, 26, blue); D.line(21, 20, 11, 26, red); sp.add(D)
    draw_skull(sp, f, mood="happy" if st == 2 else "calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        L.ell(hx + 3, hy, 2.5, 2.2, blue); L.line(hx + 1, hy, hx - 2, hy, IRON)
    sp.add(L)
    return sp.image()


def oleiro(st):
    sp, f = new(st, wide=1 if st == 3 else 0)
    clay, clay_d, cloth, goldc = (190, 110, 70), (150, 80, 52), (236, 220, 180), (240, 196, 72)
    if st == 3:
        L = Layer(); L.ell(16, 16, 11, 10, clay); L.rect(11, 5, 10, 3, clay_d); sp.add(L)
        D = Layer(shade=False, outline=False); D.line(9, 12, 13, 18, goldc); D.line(23, 11, 20, 19, goldc); D.line(14, 22, 19, 24, goldc); sp.add(D)
    hands = {1: {"l": (12, 22), "r": (20, 22)}, 2: {"l": (10, 6), "r": (22, 6)}}.get(st)
    draw_body(sp, f, hands, legs="wide" if st == 3 else "stand")
    L = Layer()
    if st == 2:
        tunic(L, f, cloth); L.rect(13, 16, 7, 6, clay_d)
    elif st == 3:
        tunic(L, f, cloth, bottom=24, flare=2)
    sp.add(L)
    draw_skull(sp, f, mood="angry" if st == 3 else "calm")
    L = Layer(); hx, hy, rx, ry = H(f)
    if st == 1:
        L.ell(16, 23, 4, 3.5, clay); L.rect(14, 19, 5, 2, clay_d)
    elif st == 2:
        L.ell(hx, hy - ry - 4, 4.5, 4, clay); L.rect(int(hx - 2), int(hy - ry - 9), 5, 2, clay_d)
    else:
        L.ell(hx, hy - ry + 0.5, rx + 1.5, 2.2, cloth); L.ell(hx + 2, hy - ry - 1.5, 2, 1.6, cloth)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    if st == 1:
        sparkle(D, [(11, 27), (21, 28), (8, 24)], clay_d)
    sp.add(D)
    return sp.image()


# ------------------------------------------------------------------ ases dos Guardiões
def troncudo(_):
    sp, f = new(3, wide=2)
    bark, moss, shirt = (120, 82, 54), (100, 150, 80), (170, 60, 50)
    L = Layer(); stick(L, 1, 10, 31, 6, bark, 4); L.ell(1.5, 10, 2, 3, darken(bark, .2)); L.ell(30.5, 6, 2, 3, darken(bark, .2)); sp.add(L)
    draw_body(sp, f, {"l": (6, 10), "r": (26, 8)}, legs="wide")
    L = Layer(); tunic(L, f, shirt, bottom=23, flare=2); sp.add(L)
    D = Layer(shade=False, outline=False)
    for x in (12, 16, 20):
        D.line(x, 13, x, 22, darken(shirt, .25))
    sp.add(D)
    draw_skull(sp, f, mood="angry")
    L = Layer(); hx, hy, rx, ry = H(f); L.poly([(hx - 3, hy + ry - 1), (hx + 3, hy + ry - 1), (hx + 1, hy + ry + 4), (hx - 1, hy + ry + 4)], moss); sp.add(L)
    return sp.image()


def bigornao(_):
    sp, f = new(3, lean=0, wide=2)
    iron, glove = (110, 114, 126), (150, 100, 60)
    draw_body(sp, f, {"l": (6, 20), "r": (26, 20)}, legs="wide")
    L = Layer(); L.poly([(8, 12), (24, 12), (22, 16), (19, 17), (19, 21), (13, 21), (13, 17), (10, 16)], iron); L.rect(11, 21, 10, 3, darken(iron, .2)); sp.add(L)
    L = Layer(); L.ell(6, 20, 3, 3, glove); L.ell(26, 20, 3, 3, glove); sp.add(L)
    draw_skull(sp, f, mood="calm")
    D = Layer(shade=False, outline=False); D.line(9, 13, 23, 13, lighten(iron, .35)); sparkle(D, [(4, 6), (28, 5)], FLAME); sp.add(D)
    return sp.image()


def caldeirona(_):
    sp, f = new(3)
    pot, green, ladle = (60, 56, 64), (130, 210, 110), (190, 190, 200)
    draw_body(sp, f, {"r": (26, 12)}, legs="stand")
    L = Layer(); L.ell(16, 19, 8.5, 7, pot); L.rect(7, 12, 18, 2, darken(pot, .2)); sp.add(L)
    D = Layer(shade=False, outline=False); D.ell(16, 13, 6.5, 1.5, green); sparkle(D, [(12, 9), (17, 7), (21, 10), (15, 4)], lighten(green, .2)); sp.add(D)
    L = Layer(); stick(L, 26, 12, 22, 4, ladle); L.ell(21.5, 3.5, 2, 1.5, ladle); sp.add(L)
    draw_skull(sp, f, mood="happy")
    L = Layer(); cap(L, f, (120, 160, 90), depth=0.3); sp.add(L)
    return sp.image()


def bandeirao(_):
    sp, f = new(3)
    banner, gold, steel = (60, 100, 190), (230, 190, 80), (176, 182, 196)
    L = Layer(); stick(L, 25, 30, 25, 0, WOOD_D, 1); L.poly([(26, 1), (31, 2), (30, 6), (31, 10), (26, 9)], banner); sp.add(L)
    D = Layer(shade=False, outline=False); D.ell(28.5, 5.5, 1.2, 1.2, gold); sp.add(D)
    draw_body(sp, f, {"r": (25, 16)})
    L = Layer(); tunic(L, f, banner); L.rect(15, 13, 2, 10, gold); sp.add(L)
    draw_skull(sp, f, mood="calm")
    L = Layer(); cap(L, f, steel, depth=0.15, extra=0.8); hx, hy, rx, ry = H(f); L.poly([(hx - 1, hy - ry - 1), (hx + 1, hy - ry - 1), (hx - 3, hy - ry - 7)], (220, 70, 70)); sp.add(L)
    return sp.image()


def patinora(_):
    sp, f = new(3, lean=-1)
    ice, ice_d, blade = (196, 230, 250), (140, 190, 230), (220, 226, 236)
    draw_body(sp, f, {"l": (3, 11), "r": (29, 9)}, legs="stand")
    L = Layer(); L.poly([(10, 14), (22, 14), (27, 22), (5, 22)], ice); sp.add(L)
    D = Layer(shade=False, outline=False)
    for x in (8, 12, 16, 20, 24):
        D.line(x, 21, x + 1, 16, ice_d)
    D.line(9, 30, 14, 30, blade); D.line(18, 30, 23, 30, blade)
    sparkle(D, [(2, 6), (30, 4), (27, 26), (4, 25)], (255, 255, 255))
    sp.add(D)
    draw_skull(sp, f, mood="sleepy")
    L = Layer(); hx, hy, rx, ry = H(f); L.ell(hx, hy - ry - 1, 3, 1.5, ice); sp.add(L)
    return sp.image()


def miragina(_):
    sp, f = new(3)
    veil, veil2, bronze = (250, 214, 160), (236, 170, 120), (200, 140, 70)
    L = Layer(); L.poly([(5, 10), (8, 9), (7, 27), (3, 26)], veil2); L.poly([(27, 10), (24, 9), (25, 27), (29, 26)], veil2); sp.add(L)
    draw_body(sp, f, {"l": (12, 19), "r": (20, 19)})
    L = Layer(); tunic(L, f, veil, bottom=25, flare=1); sp.add(L)
    D = Layer(shade=False, outline=False); D.line(13, 24, 19, 24, (180, 60, 90)); D.line(12, 14, 20, 14, (180, 60, 90)); sp.add(D)
    L = Layer(); L.ell(16, 20, 3.5, 3.5, bronze); sp.add(L)
    D = Layer(shade=False, outline=False); D.ell(16, 20, 2, 2, (250, 240, 200)); sparkle(D, [(6, 4), (26, 3), (16, 30)], (250, 230, 180)); sp.add(D)
    draw_skull(sp, f, mood="calm")
    L = Layer(); cap(L, f, veil2, depth=0.2); sp.add(L)
    return sp.image()


def raizerno(_):
    sp = Sprite(); f = body_frame(3, wide=2)
    bark, bark2, leaf = (120, 86, 60), (90, 62, 44), (90, 160, 80)
    L = Layer(); L.ell(16, 4, 14, 5, leaf); L.ell(6, 7, 5, 3, leaf); L.ell(26, 7, 5, 3, leaf); sp.add(L)
    L = Layer(); L.poly([(9, 6), (23, 6), (25, 26), (7, 26)], bark)
    for (x0, x1) in [(8, 2), (12, 9), (20, 23), (24, 30)]:
        stick(L, x0, 25, x1, 30, bark, 2)
    stick(L, 9, 12, 2, 8, bark, 2); stick(L, 23, 12, 30, 8, bark, 2)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    for x in (11, 15, 20):
        D.line(x, 8, x + 1, 25, bark2)
    sp.add(D)
    f["head"] = (16, 15)
    draw_skull(sp, f, mood="sleepy")
    G = Layer(shade=False, outline=False); sparkle(G, [(4, 4), (27, 3), (16, 0)], (250, 160, 190)); sp.add(G)
    return sp.image()


def vagonauta(_):
    sp, f = new(3)
    for k in ("head", "ribs", "shoulder", "shoulder_r", "head_top"):
        f[k] = (f[k][0], f[k][1] + 2)
    hands = {"l": (6, 13), "r": (26, 13)}
    draw_body(sp, f, hands, legs="none")
    draw_skull(sp, f, mood="angry")
    L = Layer(); hx, hy, rx, ry = H(f); cap(L, f, (230, 190, 60), depth=0.3, extra=0.9); sp.add(L)
    D = Layer(shade=False, outline=False); D.rect(int(hx - 1), int(hy - ry - 0.5), 3, 2, (255, 250, 200)); sp.add(D)
    L = Layer(); L.poly([(3, 17), (29, 17), (27, 27), (5, 27)], (110, 100, 96)); L.rect(2, 16, 28, 2, IRON); sp.add(L)
    D = Layer(shade=False, outline=False)
    for x in (9, 16, 23):
        D.line(x, 18, x, 26, (80, 74, 70))
    sp.add(D)
    L = Layer(); L.ell(9, 28, 2.5, 2.5, (60, 60, 64)); L.ell(23, 28, 2.5, 2.5, (60, 60, 64)); sp.add(L)
    G = Layer(shade=False, outline=False); sparkle(G, [(0, 22), (1, 25), (31, 24)], FLAME); sp.add(G)
    return sp.image()


def brumaga(_):
    sp, f = new(3)
    cloak, hat, fog = (70, 90, 80), (60, 50, 80), (180, 220, 190)
    L = Layer(); L.poly([(9, 10), (23, 10), (28, 29), (4, 29)], cloak); sp.add(L)
    D = Layer(shade=False, outline=False)
    for x in (6, 11, 16, 21, 26):
        D.px(x, 29, (0, 0, 0)); D.px(x + 1, 28, fog)
    sp.add(D)
    draw_body(sp, f, {"r": (25, 14), "l": (8, 20)}, legs="none")
    draw_skull(sp, f, mood="sleepy")
    L = Layer(); hx, hy, rx, ry = H(f)
    L.ell(hx, hy - ry * 0.4, rx + 4, 1.6, hat)
    L.poly([(hx - rx + 1, hy - ry * 0.5), (hx + rx - 1, hy - ry * 0.5), (hx + 7, hy - ry - 6), (hx + 3, hy - ry - 4)], hat)
    sp.add(L)
    L = Layer(); stick(L, 25, 14, 28, 30, WOOD, 2); L.ell(28, 29, 2.5, 1.6, WOOD); sp.add(L)
    G = Layer(shade=False, outline=False); sparkle(G, [(2, 20), (29, 6), (1, 24), (30, 22)], fog); sp.add(G)
    return sp.image()


def bufardo(_):
    sp, f = new(3)
    red, yel = (200, 60, 80), (240, 200, 70)
    draw_body(sp, f, {"r": (24, 6), "l": (9, 20)})
    L = Layer(); tunic(L, f, red, flare=2); sp.add(L)
    D = Layer(shade=False, outline=False)
    for y in range(11, 22, 3):
        D.line(11, y, 21, y + 1, yel)
    sp.add(D)
    draw_skull(sp, f, mood="angry")
    L = Layer(); hx, hy, rx, ry = H(f)
    cap(L, f, yel, depth=0.4)
    L.poly([(hx - rx, hy - ry), (hx - rx - 5, hy - ry - 4), (hx - 2, hy - ry - 1)], red)
    L.poly([(hx + rx, hy - ry), (hx + rx + 5, hy - ry - 4), (hx + 2, hy - ry - 1)], (60, 120, 200))
    L.poly([(hx - 1.5, hy - ry), (hx, hy - ry - 6), (hx + 1.5, hy - ry)], red)
    sp.add(L)
    G = Layer(shade=False, outline=False); sparkle(G, [(int(hx - rx - 5), int(hy - ry - 4)), (int(hx + rx + 5), int(hy - ry - 4)), (int(hx), int(hy - ry - 6))], GOLD); sp.add(G)
    L = Layer(); L.rect(21, 4, 8, 2, WOOD); L.rect(24, 1, 2, 8, WOOD); sp.add(L)
    D = Layer(shade=False, outline=False); D.line(22, 6, 22, 14, (200, 200, 220)); D.line(28, 6, 28, 14, (200, 200, 220)); sp.add(D)
    L = Layer(); L.ell(25, 16, 3, 2.5, (230, 210, 170)); L.rect(23, 18, 5, 4, (90, 140, 200)); sp.add(L)
    return sp.image()


def nevasco(_):
    sp, f = new(3)
    fur, fur2, beads = (240, 244, 250), (200, 212, 230), (150, 90, 60)
    L = Layer(); L.poly([(16, 6), (30, 29), (2, 29)], fur); sp.add(L)
    D = Layer(shade=False, outline=False)
    for (x, y) in [(10, 18), (20, 16), (14, 24), (24, 25), (7, 26), (17, 12)]:
        D.line(x, y, x + 2, y + 1, fur2)
    sp.add(D)
    f["head"] = (16, 7)
    draw_skull(sp, f, mood="sleepy")
    L = Layer(); hx, hy, rx, ry = H(f); L.ell(hx, hy + ry + 2, 6, 2.5, fur); sp.add(L)
    L = Layer()
    for i in range(9):
        L.px(12 + i, 15 + abs(4 - i) // 2, beads)
    L.ell(16, 18, 1.5, 1.5, beads)
    sp.add(L)
    L = Layer(); L.ell(10, 21, 2.2, 1.6, BONE); L.ell(22, 21, 2.2, 1.6, BONE); sp.add(L)
    G = Layer(shade=False, outline=False); sparkle(G, [(4, 6), (28, 4), (2, 14), (30, 15), (25, 1)], WHITE); sp.add(G)
    return sp.image()


def ampulhor(_):
    sp, f = new(3)
    stripe, stripe2, robe, sand = (60, 90, 170), (240, 200, 90), (230, 220, 190), (240, 200, 120)
    L = Layer(); hx, hy, rx, ry = H(f)
    L.poly([(hx - rx - 1, hy - ry + 1), (hx + rx + 1, hy - ry + 1), (hx + rx + 4, hy + 7), (hx - rx - 4, hy + 7)], stripe)
    sp.add(L)
    D = Layer(shade=False, outline=False)
    for y in range(int(hy - ry + 2), int(hy + 7), 2):
        D.line(hx - rx - 3, y, hx + rx + 3, y, stripe2)
    sp.add(D)
    draw_body(sp, f, {"r": (24, 9)})
    L = Layer(); L.poly([(f["shoulder"][0], f["shoulder"][1] - 1), (f["shoulder_r"][0], f["shoulder_r"][1] - 1), (23, 29), (9, 29)], robe); L.rect(14, 11, 4, 18, GOLD); sp.add(L)
    draw_skull(sp, f, mood="angry")
    L = Layer(); L.rect(int(hx - rx), int(hy - ry), int(rx * 2) + 1, 2, GOLD); sp.add(L)
    L = Layer()
    L.rect(22, 0, 8, 1, WOOD); L.rect(22, 8, 8, 1, WOOD)
    L.poly([(23, 1), (29, 1), (26, 4.5)], GLASS); L.poly([(23, 8), (29, 8), (26, 4.5)], GLASS)
    sp.add(L)
    G = Layer(shade=False, outline=False); G.poly([(24, 7), (28, 7), (26, 5)], sand); G.px(26, 2, sand); sp.add(G)
    return sp.image()


def degustor(_):
    sp, f = new(3)
    coat, collar, silver = (110, 50, 90), (240, 240, 230), (200, 206, 216)
    draw_body(sp, f, {"r": (25, 7), "l": (8, 18)})
    L = Layer(); tunic(L, f, coat, bottom=27, flare=2); sp.add(L)
    L = Layer(); hx, hy, rx, ry = H(f); L.poly([(hx - 6, hy + ry + 3), (hx + 6, hy + ry + 3), (hx + 8, hy + 1), (hx - 8, hy + 1)], collar); sp.add(L)
    draw_skull(sp, f, mood="sleepy")
    L = Layer(); L.rect(19, 7, 12, 1, silver); L.ell(25, 6, 5, 4, silver); L.px(25, 1, silver); sp.add(L)
    L = Layer(); L.poly([(5, 17), (9, 17), (9, 24), (6, 22)], collar); sp.add(L)
    G = Layer(shade=False, outline=False); sparkle(G, [(22, 4), (19, 9), (30, 9)], (170, 230, 110)); G.px(23, 3, WHITE); sp.add(G)
    return sp.image()


def rei_esqueleto(_):
    sp, f = new(3, wide=2)
    robe, fur, gold, orb = (110, 40, 70), (240, 236, 230), (240, 196, 72), (150, 90, 220)
    L = Layer(); cape(L, f, robe, bottom=30, spread=6); sp.add(L)
    draw_body(sp, f, {"r": (26, 12), "l": (6, 20)}, legs="wide")
    L = Layer(); tunic(L, f, darken(robe, .2), bottom=24, flare=2); sp.add(L)
    L = Layer(); L.ell(f["shoulder"][0] + 1, f["shoulder"][1], 4, 2.5, fur); L.ell(f["shoulder_r"][0] - 1, f["shoulder_r"][1], 4, 2.5, fur); L.rect(10, 11, 12, 2, fur); sp.add(L)
    D = Layer(shade=False, outline=False)
    for (x, y) in [(8, 11), (12, 12), (20, 12), (24, 11)]:
        D.px(x, y, OUTL)
    sp.add(D)
    draw_skull(sp, f, mood="angry")
    L = Layer(); hx, hy, rx, ry = H(f)
    L.rect(int(hx - rx), int(hy - ry - 1), int(rx * 2) + 1, 3, gold)
    for x in (int(hx - rx), int(hx - 2), int(hx + 2), int(hx + rx)):
        L.poly([(x - 0.5, hy - ry - 1), (x + 1.5, hy - ry - 1), (x + 0.5, hy - ry - 5)], gold)
    sp.add(L)
    D = Layer(shade=False, outline=False); D.px(int(hx), int(hy - ry), (220, 60, 80)); sp.add(D)
    L = Layer(); stick(L, 26, 12, 27, 30, gold, 2); L.ell(26.5, 9, 3, 3, orb); sp.add(L)
    G = Layer(shade=False, outline=False); G.px(25, 8, WHITE); sparkle(G, [(30, 5), (22, 6), (29, 12)], (200, 160, 255)); sp.add(G)
    return sp.image()


LINE_FUNCS = {fn.__name__: fn for fn in [grumete, faroleira, marisqueiro, rendeira, lenhador, herborista,
                                         cogumeleiro, flautista, mineiro, ferreiro, gasista, aguadeiro,
                                         lavadeira, palafiteiro, jardineiro_lirios, sentinela, escriba, sineiro,
                                         carregador, escultor, chazeiro, domador_escorpioes, cartografo, tamborileiro,
                                         apicultora, vitralista, oleiro]}
SINGLE_FUNCS = {fn.__name__: fn for fn in [raizerno, vagonauta, brumaga, bufardo, nevasco, ampulhor, degustor, rei_esqueleto,
                                           troncudo, bigornao, caldeirona, bandeirao, patinora, miragina]}


def map_frames(img):
    """Sprite de mapa 16×16 em 2 quadros: redução 2:1 que prioriza as cores
    das peças (não o contorno), mantém os olhos e recontorna por fora."""
    def reduce(src, dy):
        out = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        for y in range(16):
            for x in range(16):
                px = [src.getpixel((x * 2 + a, min(31, y * 2 + b + dy))) for b in (0, 1) for a in (0, 1)]
                op = [p for p in px if p[3] > 128]
                if not op:
                    continue
                body = [p for p in op if p[:3] != OUTL]
                eyes = [p for p in body if p[:3] == (40, 30, 48)]
                if len(op) >= 2 and body:
                    out.putpixel((x, y), max(set(body), key=body.count))
                elif len(op) >= 3:
                    out.putpixel((x, y), op[0])
        # contorno interno de 1 px onde o desenho toca o vazio
        res = out.copy()
        for y in range(16):
            for x in range(16):
                if out.getpixel((x, y))[3] == 0:
                    continue
                for ax, ay in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + ax, y + ay
                    if not (0 <= nx < 16 and 0 <= ny < 16) or out.getpixel((nx, ny))[3] == 0:
                        res.putpixel((x, y), OUTL + (255,))
                        break
        return res
    a = reduce(img, 0)
    b = reduce(img, 1)
    sheet = Image.new("RGBA", (32, 16), (0, 0, 0, 0))
    sheet.alpha_composite(a, (0, 0))
    sheet.alpha_composite(b, (16, 0))
    return sheet


def all_species():
    """[(id, função, estágio)] na ordem do Ossário."""
    out = []
    for reg in B.REGION_ORDER:
        for ln in B.LINES:
            if ln["region"] == reg:
                for st in (1, 2, 3):
                    out.append((f"{ln['id']}_{st}", LINE_FUNCS[ln["id"]], st))
        for u in B.UNIQUES:
            if u["region"] == reg:
                out.append((u["id"], SINGLE_FUNCS[u["id"]], 0))
    out.append((B.KING["id"], SINGLE_FUNCS[B.KING["id"]], 0))
    return out


def main():
    (OUT / "map").mkdir(parents=True, exist_ok=True)
    items = all_species()
    imgs = []
    for sid, fn, st in items:
        front = fn(st)
        sheet = Image.new("RGBA", (64, 32), (0, 0, 0, 0))
        sheet.alpha_composite(front, (0, 0))
        sheet.alpha_composite(back_view(front), (32, 0))
        sheet.save(OUT / f"{sid}.png")
        m = map_frames(front)
        m.save(OUT / "map" / f"{sid}.png")
        imgs.append((sid, front, m))
    # folha de revisão: 8 colunas (cada célula = mapa 16 + batalha 32), fundo em tom de grama/areia alternado
    cols = 8
    cw, ch = 56, 40
    rows = (len(imgs) + cols - 1) // cols
    sheet = Image.new("RGBA", (cols * cw, rows * ch), (0, 0, 0, 255))
    d = ImageDraw.Draw(sheet)
    for i, (sid, front, m) in enumerate(imgs):
        x, y = (i % cols) * cw, (i // cols) * ch
        bg = (122, 168, 108) if ((i // 3) % 2 == 0) else (214, 196, 150)
        d.rectangle([x, y, x + cw - 1, y + ch - 1], fill=bg + (255,))
        sheet.alpha_composite(m.crop((0, 0, 16, 16)), (x + 2, y + 18))
        sheet.alpha_composite(front, (x + 22, y + 4))
        d.text((x + 2, y + 1), str(i + 1), fill=(30, 30, 40, 255))
    sheet = sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST)
    sheet.save(ROOT / "docs/bestiario_sheet.png")
    print(f"esqueletos: {len(imgs)} espécies -> {OUT}")


if __name__ == "__main__":
    main()
