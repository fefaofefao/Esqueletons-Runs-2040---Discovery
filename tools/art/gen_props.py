#!/usr/bin/env python3
"""Gera os objetos de cenário (props) da Praia e da cabana do Bento.

Saída: assets/props/props.png + data/props.json (recortes, origem, colisão,
quadros de animação e se é interativo). Procedural e original.
"""
import json
import math
from pathlib import Path

from draw import rng
from draw import (new, put, rect, ellipse, line, outline, shade_blob, hash01,
                  mix, quad_bezier, from_ascii)

ROOT = Path(__file__).resolve().parents[2]
OUT_C = (40, 30, 48)

LEAF = (70, 164, 84)
LEAF_L = (118, 200, 98)
LEAF_D = (40, 118, 70)
TRUNK = (168, 120, 72)
TRUNK_L = (198, 152, 98)
TRUNK_D = (120, 82, 50)


def palm(frame):
    img = new(40, 52)
    base = (20, 51)
    top = (23, 18)
    ctrl = (14, 34)
    # tronco com anéis
    for i in range(0, 34):
        t = i / 33.0
        x, y = quad_bezier(base, ctrl, top, t)
        w = 2.6 - t * 0.9
        for dx in range(-3, 4):
            if abs(dx) <= w:
                c = TRUNK
                if dx < -w + 1.2:
                    c = TRUNK_L
                elif dx > w - 1.2:
                    c = TRUNK_D
                if i % 4 == 0:
                    c = mix(c, TRUNK_D, 0.5)
                put(img, int(x + dx), int(y), c)
    # cocos
    for (cx, cy) in [(21, 20), (25, 21), (23, 22)]:
        ellipse(img, cx, cy, 1.6, 1.6, (110, 76, 44))
        put(img, int(cx) - 1, int(cy) - 1, (150, 106, 64))
    # folhas (frondes curvas)
    sway = 1 if frame == 1 else 0
    fronds = [(-17, 6), (-12, -6), (-3, -11), (7, -10), (15, -3), (17, 8), (-8, 10), (9, 11)]
    for k, (fx, fy) in enumerate(fronds):
        end = (top[0] + fx + (sway if fx > 0 else -sway * 0), top[1] + fy + (sway if abs(fx) > 10 else 0))
        mid = (top[0] + fx * 0.55, top[1] + min(fy, 0) - 5 + abs(fx) * 0.05)
        for i in range(30):
            t = i / 29.0
            x, y = quad_bezier(top, mid, end, t)
            r = 2.3 * math.sin(math.pi * min(1.0, t * 1.15)) + 0.4
            for dy in range(-3, 4):
                for dx in range(-3, 4):
                    if dx * dx + dy * dy <= r * r:
                        c = LEAF
                        if dy < 0:
                            c = LEAF_L
                        if dy > 1:
                            c = LEAF_D
                        put(img, int(x + dx), int(y + dy), c)
        # nervura
        for i in range(4, 26):
            t = i / 29.0
            x, y = quad_bezier(top, mid, end, t)
            put(img, int(x), int(y), LEAF_D if k % 2 else mix(LEAF, LEAF_D, 0.5))
    outline(img, OUT_C)
    return img


def rock(w, h, seed):
    img = new(w, h)
    ellipse(img, w / 2, h / 2 + 1, w / 2 - 1.2, h / 2 - 1.5, (140, 140, 150))
    ellipse(img, w / 2 - 2, h / 2 + 2, w / 3, h / 3, (140, 140, 150))
    shade_blob(img, (184, 184, 192), (140, 140, 152), (94, 94, 112))
    for i in range(int(w * h / 40)):
        x = int(hash01(i, 1, seed) * w)
        y = int(hash01(i, 2, seed) * h)
        if img.getpixel((x, y))[3]:
            put(img, x, y, (110, 112, 126))
    # musgo
    for x in range(w):
        for y in range(h):
            if img.getpixel((x, y))[3] and y < h / 2 and hash01(x, y, seed + 9) > 0.86:
                put(img, x, y, (104, 150, 92))
    outline(img, OUT_C)
    return img


def hut():
    W, H = 80, 66
    img = new(W, H)
    wall_top = 32
    # paredes de tábuas
    for y in range(wall_top, H - 1):
        for x in range(4, W - 4):
            board = (x - 4) // 6
            c = mix((176, 122, 74), (198, 146, 92), 0.4 if board % 2 else 0.0)
            if (x - 4) % 6 == 5:
                c = (120, 80, 50)
            if y >= H - 4:
                c = (110, 74, 48)
            put(img, x, y, c)
    # sombra do beiral
    rect(img, 4, wall_top, W - 8, 3, (110, 74, 48))
    # telhado de palha (trapézio)
    for y in range(4, wall_top + 3):
        t = (y - 4) / (wall_top - 1)
        half = 18 + t * 22
        for x in range(int(W / 2 - half), int(W / 2 + half)):
            stripe = (x + y // 3) % 5
            c = (214, 178, 96)
            if stripe == 0:
                c = (176, 138, 66)
            elif stripe == 2:
                c = (232, 202, 128)
            if y > wall_top - 1:
                c = (160, 122, 58) if x % 3 else (140, 104, 50)
            put(img, x, y, c)
    # cumeeira
    rect(img, W // 2 - 18, 3, 36, 2, (150, 112, 54))
    # porta
    door_x = W // 2 - 7
    rect(img, door_x, H - 18, 14, 17, (84, 54, 36))
    rect(img, door_x + 1, H - 17, 12, 16, (120, 78, 48))
    for x in range(door_x + 1, door_x + 13, 4):
        rect(img, x, H - 17, 1, 16, (96, 62, 40))
    put(img, door_x + 10, H - 9, (230, 200, 120))
    # janela
    rect(img, 9, wall_top + 8, 12, 10, (84, 54, 36))
    for y in range(wall_top + 9, wall_top + 17):
        for x in range(10, 20):
            put(img, x, y, mix((120, 190, 230), (230, 246, 250), (y - wall_top - 9) / 8))
    rect(img, 14, wall_top + 9, 1, 8, (84, 54, 36))
    rect(img, 8, wall_top + 18, 14, 2, (150, 104, 62))
    # rede de pesca com boias à direita
    for y in range(wall_top + 6, wall_top + 24):
        for x in range(54, 72):
            if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                put(img, x, y, (226, 220, 196))
    for (bx, by, c) in [(57, wall_top + 14, (226, 76, 60)), (64, wall_top + 19, (250, 200, 70)),
                        (69, wall_top + 10, (226, 76, 60))]:
        ellipse(img, bx, by, 1.8, 1.8, c)
    # placa com peixe acima da porta
    rect(img, W // 2 - 5, wall_top + 5, 10, 5, (150, 104, 62))
    for x in range(W // 2 - 3, W // 2 + 3):
        put(img, x, wall_top + 7, (90, 150, 190))
    put(img, W // 2 + 3, wall_top + 6, (90, 150, 190))
    put(img, W // 2 + 3, wall_top + 8, (90, 150, 190))
    outline(img, OUT_C)
    return img


def boat():
    img = new(48, 26)
    for y in range(4, 22):
        t = (y - 4) / 17.0
        inset = 3 + int(abs(t - 0.45) ** 1.6 * 14)
        for x in range(inset, 48 - inset):
            c = (70, 120, 170) if y > 14 else (226, 226, 222)
            if y in (14, 15):
                c = (200, 70, 56)
            put(img, x, y, c)
    # interior
    for y in range(7, 13):
        for x in range(10, 38):
            if img.getpixel((x, y))[3]:
                put(img, x, y, (140, 96, 60) if x % 5 else (110, 74, 48))
    rect(img, 22, 7, 4, 6, (176, 124, 76))
    # remo
    line(img, 14, 3, 30, 22, (196, 150, 96))
    line(img, 15, 3, 31, 22, (150, 108, 64))
    ellipse(img, 31, 22, 2.2, 3, (196, 150, 96))
    outline(img, OUT_C)
    return img


def sign():
    img = new(16, 18)
    rect(img, 7, 8, 2, 9, (130, 88, 54))
    rect(img, 1, 2, 14, 8, (196, 146, 88))
    rect(img, 1, 2, 14, 1, (220, 176, 118))
    rect(img, 1, 9, 14, 1, (150, 104, 62))
    for x in range(3, 13, 3):
        rect(img, x, 5, 2, 1, (120, 80, 50))
    outline(img, OUT_C)
    return img


def barrel():
    img = new(14, 16)
    ellipse(img, 7, 8, 6, 7.5, (160, 108, 64))
    shade_blob(img, (190, 138, 84), (160, 108, 64), (116, 76, 46))
    for y in (3, 12):
        for x in range(14):
            if img.getpixel((x, y))[3]:
                put(img, x, y, (90, 90, 100))
    ellipse(img, 7, 2.5, 5, 1.6, (128, 88, 54))
    outline(img, OUT_C)
    return img


def crate():
    img = new(16, 16)
    rect(img, 1, 1, 14, 14, (186, 134, 80))
    rect(img, 1, 1, 14, 2, (210, 160, 104))
    for i in range(14):
        put(img, 1 + i, 1 + i, (140, 96, 58))
    rect(img, 1, 7, 14, 1, (140, 96, 58))
    rect(img, 1, 14, 14, 1, (120, 80, 50))
    outline(img, OUT_C)
    return img


def net_rack():
    img = new(32, 24)
    for x in (3, 28):
        rect(img, x, 4, 2, 19, (130, 88, 54))
    rect(img, 2, 3, 28, 2, (150, 104, 62))
    for y in range(6, 18):
        for x in range(6, 27):
            if (x + y) % 3 == 0 or (x - y) % 3 == 0:
                put(img, x, y + (1 if 10 < x < 22 else 0), (230, 226, 206))
    for (bx, c) in [(8, (226, 76, 60)), (16, (250, 200, 70)), (24, (226, 76, 60))]:
        ellipse(img, bx, 18, 1.6, 1.6, c)
    outline(img, OUT_C)
    return img


def driftwood():
    img = new(30, 12)
    for x in range(2, 28):
        y = 6 + math.sin(x * 0.4) * 1.2
        for dy in range(-2, 2):
            put(img, x, int(y + dy), (196, 170, 136) if dy < 0 else (160, 134, 104))
    line(img, 8, 5, 4, 1, (180, 154, 120))
    line(img, 20, 5, 24, 1, (180, 154, 120))
    outline(img, OUT_C)
    return img


def starfish():
    img = new(12, 12)
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        line(img, 6, 6, 6 + math.cos(a) * 4.5, 6 + math.sin(a) * 4.5, (238, 120, 80))
    ellipse(img, 6, 6, 1.8, 1.8, (238, 120, 80))
    put(img, 6, 5, (252, 180, 140))
    outline(img, (150, 70, 50))
    return img


def campfire_stones(frame):
    img = new(16, 16)
    for k in range(7):
        a = k * 2 * math.pi / 7
        ellipse(img, 8 + math.cos(a) * 5, 11 + math.sin(a) * 2.5, 1.8, 1.4, (130, 128, 138))
    rect(img, 4, 10, 8, 2, (100, 70, 44))
    flame = [(8, 9, 3.0), (7, 7, 2.0), (9, 6, 1.5)] if frame == 0 else [(8, 9, 3.2), (9, 7, 2.0), (7, 5, 1.4)]
    for (fx, fy, r) in flame:
        ellipse(img, fx, fy, r * 0.8, r, (250, 150, 50))
    ellipse(img, 8, 9, 1.4, 2, (255, 230, 120))
    return img


# ------------------------------------------------------------- interior
def bed():
    img = new(16, 30)
    rect(img, 1, 1, 14, 28, (120, 80, 50))
    rect(img, 2, 2, 12, 7, (240, 240, 236))
    rect(img, 2, 8, 12, 1, (200, 200, 210))
    for y in range(10, 27):
        for x in range(2, 14):
            put(img, x, y, (70, 130, 170) if (x // 2 + y // 2) % 2 else (90, 150, 190))
    rect(img, 2, 10, 12, 1, (220, 220, 230))
    outline(img, OUT_C)
    return img


def table():
    img = new(32, 22)
    rect(img, 1, 1, 30, 12, (176, 122, 74))
    rect(img, 1, 1, 30, 2, (204, 150, 96))
    rect(img, 1, 12, 30, 3, (130, 86, 52))
    for x in (3, 26):
        rect(img, x, 15, 3, 6, (120, 80, 50))
    # caneca e peixe seco
    rect(img, 6, 4, 4, 4, (226, 226, 230))
    rect(img, 10, 5, 1, 2, (226, 226, 230))
    for x in range(16, 26):
        put(img, x, 6, (150, 170, 190))
        put(img, x, 7, (120, 140, 160))
    put(img, 26, 5, (150, 170, 190))
    put(img, 26, 8, (150, 170, 190))
    outline(img, OUT_C)
    return img


def stool():
    img = new(12, 12)
    ellipse(img, 6, 4, 5, 3, (186, 132, 80))
    rect(img, 2, 5, 2, 6, (130, 86, 52))
    rect(img, 8, 5, 2, 6, (130, 86, 52))
    outline(img, OUT_C)
    return img


def shelf():
    img = new(32, 30)
    rect(img, 1, 1, 30, 28, (120, 80, 50))
    for y in (9, 19):
        rect(img, 2, y, 28, 2, (176, 122, 74))
    rect(img, 2, 2, 28, 7, (90, 60, 40))
    rect(img, 2, 11, 28, 8, (90, 60, 40))
    rect(img, 2, 21, 28, 7, (90, 60, 40))
    jars = [(4, 4, (110, 180, 200)), (10, 5, (220, 190, 90)), (16, 3, (200, 110, 90)), (24, 4, (150, 200, 120)),
            (5, 13, (230, 230, 220)), (13, 14, (110, 180, 200)), (22, 13, (210, 160, 90)),
            (6, 23, (180, 140, 100)), (18, 23, (130, 160, 190))]
    for (x, y, c) in jars:
        h = 9 - (y - 2) % 10 if y < 10 else (19 - y if y < 20 else 28 - y)
        rect(img, x, y, 4, max(3, h), c)
        rect(img, x, y, 4, 1, mix(c, (255, 255, 255), 0.4))
    outline(img, OUT_C)
    return img


def plant():
    img = new(14, 18)
    rect(img, 4, 11, 6, 6, (186, 100, 70))
    rect(img, 3, 10, 8, 2, (210, 120, 84))
    for k in range(6):
        a = -math.pi * (0.15 + 0.7 * k / 5)
        line(img, 7, 10, 7 + math.cos(a) * 6, 10 + math.sin(a) * 8, (80, 160, 80))
        put(img, int(7 + math.cos(a) * 6), int(10 + math.sin(a) * 8), (120, 200, 100))
    outline(img, OUT_C)
    return img


def lamp(frame):
    img = new(10, 16)
    rect(img, 4, 0, 2, 3, (90, 90, 100))
    rect(img, 2, 3, 6, 9, (70, 70, 84))
    rect(img, 3, 4, 4, 7, (255, 210, 110) if frame == 0 else (255, 196, 90))
    put(img, 4, 6, (255, 246, 200))
    rect(img, 1, 12, 8, 2, (70, 70, 84))
    outline(img, OUT_C)
    return img


def rug():
    img = new(48, 30)
    for y in range(30):
        for x in range(48):
            c = (170, 70, 60)
            if x in (0, 47) or y in (0, 29):
                c = (110, 46, 40)
            elif x in (2, 45) or y in (2, 27):
                c = (226, 186, 100)
            elif (abs(x - 24) + abs(y - 15)) % 8 < 2:
                c = (226, 186, 100)
            put(img, x, y, c)
    return img


def rod_rack():
    img = new(16, 28)
    rect(img, 1, 22, 14, 3, (130, 86, 52))
    for (x, c) in [(3, (196, 150, 96)), (8, (150, 110, 70)), (12, (210, 170, 110))]:
        line(img, x, 24, x + 1, 1, c)
    put(img, 4, 2, (220, 220, 220))
    outline(img, OUT_C)
    return img


# ------------------------------------------------------------- vila (fase 4a)
def house(W, H, roof, roof_d, wall, wall_d, sign=None, seed=0):
    """Casa de vila: telhado de telhas, paredes, porta central, 2 janelas e placa opcional."""
    img = new(W, H)
    wall_top = H - 30
    for y in range(wall_top, H - 1):
        for x in range(3, W - 3):
            c = wall if (y // 4 + (x // 8)) % 2 else mix(wall, wall_d, 0.25)
            if y >= H - 4:
                c = wall_d
            put(img, x, y, c)
    rect(img, 3, wall_top, W - 6, 2, wall_d)
    # telhado (trapézio com fileiras de telhas)
    for y in range(2, wall_top + 3):
        t = (y - 2) / max(1, wall_top)
        half = W * 0.30 + t * (W * 0.22)
        for x in range(int(W / 2 - half), int(W / 2 + half)):
            row = (y - 2) // 4
            c = roof if ((x + row * 3) // 6) % 2 else mix(roof, roof_d, 0.3)
            if (y - 2) % 4 == 3:
                c = roof_d
            put(img, x, y, c)
    rect(img, int(W * 0.2), 1, int(W * 0.6), 2, roof_d)
    # chaminé
    rect(img, int(W * 0.72), 0, 6, 10, (150, 110, 90))
    rect(img, int(W * 0.72) - 1, 0, 8, 2, (120, 90, 74))
    # porta
    dx = W // 2 - 6
    rect(img, dx, H - 17, 12, 16, (84, 54, 36))
    rect(img, dx + 1, H - 16, 10, 15, (132, 86, 52))
    put(img, dx + 8, H - 9, (240, 210, 120))
    # janelas
    for wx in (8, W - 20):
        rect(img, wx, wall_top + 7, 12, 10, (84, 54, 36))
        for yy in range(wall_top + 8, wall_top + 16):
            for xx in range(wx + 1, wx + 11):
                put(img, xx, yy, mix((150, 200, 230), (240, 248, 250), (yy - wall_top - 8) / 8))
        rect(img, wx + 5, wall_top + 8, 1, 8, (84, 54, 36))
        rect(img, wx - 1, wall_top + 17, 14, 2, wall_d)
    if sign == "ranch":
        rect(img, W // 2 - 7, wall_top + 3, 14, 9, (246, 240, 226))
        rect(img, W // 2 - 1, wall_top + 4, 2, 7, (214, 70, 70))
        rect(img, W // 2 - 3, wall_top + 6, 6, 3, (214, 70, 70))
    elif sign == "shop":
        rect(img, W // 2 - 7, wall_top + 3, 14, 9, (246, 240, 226))
        ellipse(img, W // 2, wall_top + 7.5, 3.5, 3.5, (236, 190, 60))
        put(img, W // 2, wall_top + 7, (180, 130, 40))
    elif sign == "house":
        ellipse(img, W // 2, wall_top + 7, 3, 3, (246, 240, 226))
    outline(img, OUT_C)
    return img


def lighthouse():
    W, H = 32, 92
    img = new(W, H)
    for y in range(22, H - 1):
        t = (y - 22) / (H - 23)
        half = 6 + t * 7
        for x in range(int(16 - half), int(16 + half)):
            band = ((y - 22) // 12) % 2
            c = (236, 230, 220) if band == 0 else (196, 72, 64)
            if x > 16 + half * 0.4:
                c = mix(c, (80, 70, 80), 0.25)
            put(img, x, y, c)
    rect(img, 7, 18, 18, 5, (70, 70, 84))
    rect(img, 9, 8, 14, 10, (70, 70, 84))
    for yy in range(10, 17):
        for xx in range(11, 21):
            put(img, xx, yy, (120, 130, 140))  # lente apagada
    for xx in (13, 16, 19):
        rect(img, xx, 9, 1, 9, (70, 70, 84))
    rect(img, 8, 6, 16, 2, (60, 60, 72))
    for y in range(0, 6):
        rect(img, 16 - (6 - y), y, 2 * (6 - y), 1, (196, 72, 64))
    rect(img, 13, H - 14, 6, 13, (84, 54, 36))
    outline(img, OUT_C)
    return img


def fence():
    img = new(16, 16)
    for x in (2, 13):
        rect(img, x, 4, 2, 11, (170, 120, 76))
    rect(img, 0, 6, 16, 2, (196, 146, 92))
    rect(img, 0, 11, 16, 2, (196, 146, 92))
    outline(img, OUT_C)
    return img


def lamp_post(frame):
    img = new(10, 30)
    rect(img, 4, 8, 2, 21, (70, 70, 84))
    rect(img, 2, 27, 6, 2, (60, 60, 72))
    rect(img, 1, 1, 8, 8, (70, 70, 84))
    c = (255, 226, 140) if frame == 0 else (255, 210, 110)
    rect(img, 2, 2, 6, 6, c)
    outline(img, OUT_C)
    return img


def well():
    img = new(26, 28)
    ellipse(img, 13, 20, 11, 6, (150, 150, 160))
    ellipse(img, 13, 19, 8, 4, (40, 60, 90))
    for x in (3, 22):
        rect(img, x, 4, 2, 16, (150, 104, 62))
    rect(img, 1, 2, 24, 3, (196, 72, 64))
    rect(img, 12, 5, 2, 7, (200, 190, 160))
    rect(img, 10, 11, 6, 4, (150, 104, 62))
    outline(img, OUT_C)
    return img


def stall():
    img = new(48, 34)
    rect(img, 4, 16, 40, 16, (176, 122, 74))
    rect(img, 4, 14, 40, 3, (150, 104, 62))
    for i, x in enumerate(range(8, 42, 7)):
        ellipse(img, x + 2, 13, 3, 2.2, [(230, 120, 70), (120, 180, 220), (240, 200, 90), (150, 200, 120), (230, 120, 70)][i % 5])
    for x in (5, 41):
        rect(img, x, 2, 2, 14, (120, 80, 50))
    for x in range(2, 46):
        put(img, x, 2 + (x // 6) % 2, (196, 72, 64) if (x // 6) % 2 else (246, 240, 226))
        rect(img, x, 3, 1, 4, (196, 72, 64) if (x // 6) % 2 else (246, 240, 226))
    outline(img, OUT_C)
    return img


def flower_box():
    img = new(16, 14)
    rect(img, 1, 7, 14, 6, (150, 104, 62))
    for i, x in enumerate(range(3, 14, 3)):
        ellipse(img, x, 5, 1.8, 1.8, [(240, 120, 150), (250, 220, 90), (180, 140, 230), (240, 120, 150)][i % 4])
        put(img, x, 7, (90, 150, 70))
    outline(img, OUT_C)
    return img


def net_snag():
    img = new(20, 14)
    ellipse(img, 10, 9, 9, 5, (120, 120, 130))
    for y in range(3, 10):
        for x in range(4, 17):
            if (x + y) % 3 == 0:
                put(img, x, y, (226, 220, 196))
    ellipse(img, 6, 4, 1.6, 1.6, (226, 76, 60))
    outline(img, OUT_C)
    return img


# ------------------------------------------------------------- floresta (fase 4b)
def tree_oak(seed=0):
    W, H = 40, 52
    img = new(W, H)
    rect(img, 16, 30, 8, 21, (120, 84, 56))
    rect(img, 20, 30, 4, 21, (96, 66, 44))
    for x in (13, 25):
        rect(img, x, 47, 3, 4, (110, 76, 50))
    r = rng(seed + 11)
    blobs = [(20, 18, 17, 14), (10, 24, 9, 8), (30, 24, 9, 8), (20, 8, 11, 8)]
    for (cx, cy, rx, ry) in blobs:
        ellipse(img, cx, cy, rx, ry, (70, 132, 70))
    for (cx, cy, rx, ry) in blobs:
        ellipse(img, cx - 2, cy - 3, rx * 0.65, ry * 0.6, (96, 160, 84))
    for _ in range(26):
        x, y = r.randint(4, 36), r.randint(2, 32)
        if img.getpixel((x, y))[3]:
            put(img, x, y, (130, 190, 100) if r.random() < 0.5 else (52, 104, 58))
    outline(img, OUT_C)
    return img


def tree_pine(seed=0):
    W, H = 28, 46
    img = new(W, H)
    rect(img, 12, 36, 4, 9, (110, 76, 50))
    for i, (y, half) in enumerate([(4, 4), (11, 7), (18, 10), (25, 12), (31, 13)]):
        for yy in range(y, y + 9):
            h = half * (yy - y + 2) / 10
            for x in range(int(14 - h), int(14 + h) + 1):
                put(img, x, yy, (44, 104, 74) if x < 14 else (34, 84, 62))
    rect(img, 13, 1, 2, 4, (44, 104, 74))
    outline(img, OUT_C)
    return img


def root_wall():
    W, H = 34, 26
    img = new(W, H)
    r = rng(5)
    for i in range(14):
        y0 = r.randint(4, 22)
        y1 = r.randint(4, 22)
        c = (124, 88, 58) if i % 2 else (98, 68, 46)
        for t in range(0, 34):
            y = y0 + (y1 - y0) * t / 33 + 2 * __import__("math").sin(t / 4 + i)
            rect(img, t, int(y), 1, 3, c)
    for _ in range(8):
        ellipse(img, r.randint(4, 30), r.randint(4, 20), 2, 1.5, (90, 150, 70))
    outline(img, OUT_C)
    return img


def root_arch():
    W, H = 34, 30
    img = new(W, H)
    ellipse(img, 17, 18, 16, 13, (104, 72, 48))
    ellipse(img, 17, 22, 9, 9, (20, 14, 24))
    rect(img, 8, 22, 18, 8, (20, 14, 24))
    for x in range(2, 32, 5):
        rect(img, x, 6 + (x % 3), 2, 6, (130, 94, 62))
    ellipse(img, 8, 6, 5, 3, (80, 140, 70))
    ellipse(img, 26, 5, 6, 3, (80, 140, 70))
    outline(img, OUT_C)
    return img


def stump():
    img = new(18, 14)
    ellipse(img, 9, 9, 8, 4.5, (120, 84, 56))
    ellipse(img, 9, 6, 7, 3, (190, 150, 100))
    ellipse(img, 9, 6, 3.5, 1.5, (160, 120, 80))
    outline(img, OUT_C)
    return img


def log():
    img = new(34, 14)
    rect(img, 3, 3, 28, 9, (120, 84, 56))
    rect(img, 3, 3, 28, 2, (150, 110, 74))
    ellipse(img, 31, 7.5, 3, 4.5, (190, 150, 100))
    ellipse(img, 31, 7.5, 1.5, 2, (150, 110, 70))
    for x in (9, 18, 25):
        put(img, x, 6, (90, 150, 70))
        put(img, x + 1, 5, (90, 150, 70))
    outline(img, OUT_C)
    return img


def mushrooms(frame=0, glow=False):
    img = new(16, 14)
    cap = (120, 230, 220) if glow else (214, 70, 70)
    if glow and frame:
        cap = (160, 250, 240)
    for (cx, cy, r) in [(5, 8, 3.5), (11, 9, 2.6)]:
        rect(img, int(cx) - 1, int(cy), 2, 4, (236, 226, 200))
        ellipse(img, cx, cy, r, r * 0.7, cap)
        if not glow:
            put(img, int(cx) - 1, int(cy) - 1, (250, 250, 250))
    outline(img, OUT_C)
    return img


def herb_blue():
    img = new(14, 16)
    for (x0, x1) in [(7, 3), (7, 11), (7, 7)]:
        line(img, 7, 15, x1, 6, (70, 140, 70))
    for (x, y) in [(3, 5), (11, 5), (7, 3)]:
        ellipse(img, x, y, 2, 2, (90, 140, 230))
        put(img, x, y, (230, 240, 255))
    outline(img, OUT_C)
    return img


def raizerno_tree():
    W, H = 56, 64
    img = new(W, H)
    rect(img, 16, 18, 24, 40, (110, 78, 54))
    rect(img, 30, 18, 10, 40, (92, 64, 44))
    for (x0, x1) in [(16, 4), (20, 12), (36, 46), (40, 54)]:
        line(img, x0, 56, x1, 63, (110, 78, 54))
        line(img, x0 + 1, 56, x1 + 1, 63, (110, 78, 54))
    for (cx, cy, rx, ry) in [(28, 12, 24, 12), (12, 18, 10, 7), (44, 18, 10, 7)]:
        ellipse(img, cx, cy, rx, ry, (70, 132, 70))
        ellipse(img, cx - 3, cy - 3, rx * 0.6, ry * 0.5, (96, 160, 84))
    # rosto de osso no tronco
    ellipse(img, 28, 34, 8, 7, (226, 220, 200))
    rect(img, 23, 34, 3, 3, (40, 30, 48))
    rect(img, 30, 34, 3, 3, (40, 30, 48))
    for x in range(24, 33, 2):
        put(img, x, 40, (40, 30, 48))
    # brasão: coroa sobre onda
    for x in range(22, 35):
        put(img, x, 50 + (1 if (x // 2) % 2 else 0), (240, 200, 90))
    for x in (24, 28, 32):
        line(img, x, 47, x, 45, (240, 200, 90))
    rect(img, 23, 47, 11, 1, (240, 200, 90))
    outline(img, OUT_C)
    return img


# ------------------------------------------------------------- minas (fase 4c)
def rails():
    img = new(16, 16)
    for x in (3, 12):
        rect(img, x, 0, 1, 16, (120, 120, 130))
    for y in range(1, 16, 4):
        rect(img, 1, y, 14, 2, (110, 80, 54))
    return img


def mine_cart():
    img = new(26, 20)
    rect(img, 3, 4, 20, 10, (110, 100, 96))
    rect(img, 2, 3, 22, 2, (150, 156, 170))
    ellipse(img, 8, 11, 6, 3, (60, 54, 52))
    for x in (6, 20):
        ellipse(img, x, 16, 3, 3, (60, 60, 64))
    ellipse(img, 10, 4, 3, 2, (60, 58, 60))
    ellipse(img, 16, 3, 3, 2, (80, 76, 74))
    outline(img, OUT_C)
    return img


def mine_lamp(frame):
    img = new(12, 30)
    rect(img, 5, 6, 2, 23, (110, 80, 54))
    rect(img, 3, 27, 6, 2, (90, 64, 44))
    rect(img, 2, 2, 8, 6, (70, 70, 84))
    rect(img, 3, 3, 6, 4, (255, 210, 110) if frame == 0 else (255, 190, 90))
    outline(img, OUT_C)
    return img


def crystal(frame):
    img = new(16, 18)
    col = (150, 220, 255) if frame == 0 else (190, 240, 255)
    for (x, h, w) in [(4, 10, 3), (8, 14, 4), (12, 8, 3)]:
        for y in range(h):
            ww = max(1, int(w * (1 - y / h)) + 1)
            rect(img, x - ww // 2, 17 - y, ww, 1, col if y > 1 else (255, 255, 255))
    outline(img, OUT_C)
    return img


def beam_frame():
    img = new(48, 40)
    rect(img, 2, 6, 6, 34, (120, 84, 56))
    rect(img, 40, 6, 6, 34, (120, 84, 56))
    rect(img, 0, 2, 48, 7, (140, 100, 64))
    rect(img, 8, 9, 32, 31, (24, 20, 26))
    outline(img, OUT_C)
    return img


def anvil():
    img = new(20, 14)
    rect(img, 2, 2, 16, 4, (90, 92, 104))
    rect(img, 16, 3, 4, 2, (90, 92, 104))
    rect(img, 7, 6, 6, 4, (70, 72, 84))
    rect(img, 4, 10, 12, 3, (70, 72, 84))
    rect(img, 2, 2, 16, 1, (150, 156, 170))
    outline(img, OUT_C)
    return img


def forge(frame):
    img = new(40, 34)
    rect(img, 2, 8, 36, 25, (110, 90, 84))
    for y in range(8, 33, 5):
        rect(img, 2, y, 36, 1, (84, 66, 62))
    rect(img, 10, 16, 20, 12, (30, 20, 20))
    fire = [(255, 150, 60), (255, 210, 110), (230, 90, 40)]
    for i in range(6):
        x = 12 + i * 3
        h = 5 + ((i + frame) % 3) * 2
        rect(img, x, 28 - h, 2, h, fire[(i + frame) % 3])
    rect(img, 16, 0, 8, 9, (96, 80, 76))
    outline(img, OUT_C)
    return img


def chain_gate():
    img = new(34, 28)
    for x in (2, 30):
        rect(img, x, 0, 3, 28, (80, 76, 84))
    for row in range(5):
        for k in range(8):
            ellipse(img, 6 + k * 3.2, 4 + row * 5, 1.8, 1.4, (150, 150, 160))
            put(img, int(6 + k * 3.2), 4 + row * 5, (90, 90, 100))
    rect(img, 14, 10, 6, 7, (200, 160, 70))
    rect(img, 16, 12, 2, 3, (80, 60, 30))
    outline(img, OUT_C)
    return img


def rubble():
    img = new(34, 22)
    r = rng(17)
    for _ in range(9):
        x, y = r.randint(4, 28), r.randint(6, 18)
        ellipse(img, x, y, r.randint(3, 6), r.randint(2, 4), (120 + r.randint(-10, 10), 112, 106))
    outline(img, OUT_C)
    return img


def map_board():
    img = new(30, 24)
    rect(img, 1, 1, 28, 20, (110, 80, 54))
    rect(img, 3, 3, 24, 16, (236, 220, 170))
    for (cx, cy) in [(9, 9), (16, 7), (22, 11)]:
        ellipse(img, cx, cy, 3.5, 2.5, (110, 170, 210))
    for x in range(4, 26):
        put(img, x, 14 + int(1.5 * math.sin(x / 2)), (150, 110, 80))
    rect(img, 13, 21, 4, 3, (90, 64, 44))
    outline(img, OUT_C)
    return img


def scarf():
    img = new(16, 10)
    for x in range(1, 15):
        rect(img, x, 3 + int(1.5 * math.sin(x / 2)), 1, 3, (214, 90, 90))
    for x in range(2, 14, 3):
        put(img, x, 4 + int(1.5 * math.sin(x / 2)), (250, 220, 120))
    outline(img, OUT_C)
    return img


def helmet_lamp():
    img = new(14, 12)
    ellipse(img, 7, 7, 6, 4, (230, 190, 60))
    rect(img, 1, 8, 12, 3, (230, 190, 60))
    rect(img, 5, 3, 4, 3, (255, 250, 200))
    outline(img, OUT_C)
    return img


# ------------------------------------------------------------- pântano (4d)
def reeds(frame):
    img = new(16, 22)
    for i, x in enumerate((3, 6, 9, 12, 5, 10)):
        sway = (1 if (i + frame) % 2 else 0)
        h = 12 + (i * 5) % 8
        for y in range(h):
            put(img, x + (sway if y < h // 2 else 0), 21 - y, (90, 140, 70) if i % 2 else (70, 120, 60))
        if i < 3:
            rect(img, x - 1 + sway, 21 - h, 3, 4, (130, 90, 56))
    outline(img, OUT_C)
    return img


def lilypad():
    img = new(16, 12)
    ellipse(img, 6, 6, 5, 3, (80, 150, 80))
    ellipse(img, 11, 8, 3.5, 2.2, (70, 136, 70))
    rect(img, 6, 4, 1, 3, (50, 100, 60))
    put(img, 11, 7, (240, 170, 200)); put(img, 12, 7, (250, 210, 230))
    return img


def willow():
    W, H = 44, 56
    img = new(W, H)
    rect(img, 19, 28, 7, 27, (100, 86, 70))
    rect(img, 23, 28, 3, 27, (80, 68, 56))
    ellipse(img, 22, 18, 20, 13, (84, 120, 76))
    ellipse(img, 20, 14, 13, 8, (104, 140, 86))
    for x in range(3, 42, 3):
        h = 18 + int(8 * math.sin(x * 0.7))
        for y in range(20, 20 + h):
            put(img, x, y, (96, 136, 80) if y % 3 else (74, 110, 66))
    outline(img, OUT_C)
    return img


def dead_tree():
    img = new(30, 40)
    rect(img, 13, 14, 5, 26, (110, 96, 84))
    for (x0, y0, x1, y1) in [(15, 16, 4, 6), (15, 20, 26, 8), (15, 26, 7, 20), (16, 12, 18, 1)]:
        line(img, x0, y0, x1, y1, (110, 96, 84))
        line(img, x0 + 1, y0, x1 + 1, y1, (90, 78, 70))
    outline(img, OUT_C)
    return img


def cauldron(frame):
    img = new(26, 26)
    ellipse(img, 13, 17, 11, 8, (60, 58, 70))
    ellipse(img, 13, 11, 11, 3, (40, 40, 50))
    ellipse(img, 13, 11, 9, 2, (120, 200, 90) if frame == 0 else (150, 220, 100))
    for (bx, by) in [(9, 6), (16, 4)] if frame == 0 else [(11, 4), (15, 7)]:
        ellipse(img, bx, by, 2, 2, (170, 230, 120))
    for x in (6, 20):
        rect(img, x, 23, 3, 3, (40, 40, 50))
    outline(img, OUT_C)
    return img


def stilts(img, W, H, wood=(110, 86, 60)):
    """Acrescenta palafitas sob uma casa (as últimas 8 linhas)."""
    out = new(W, H + 8)
    out.alpha_composite(img, (0, 0))
    for x in range(6, W - 6, 12):
        rect(out, x, H - 1, 4, 9, wood)
        rect(out, x + 3, H - 1, 1, 9, mix(wood, (40, 30, 30), 0.3))
    return out


def stilt_house(kind, roof, roof_d):
    W, H = (80, 62) if kind != "house" else (64, 54)
    img = house(W, H, roof, roof_d, (176, 150, 110), (138, 112, 80), kind)
    return stilts(img, W, H)


def mail_bag():
    img = new(16, 14)
    ellipse(img, 8, 9, 7, 5, (170, 120, 70))
    rect(img, 2, 5, 12, 3, (140, 96, 56))
    rect(img, 6, 8, 4, 3, (240, 230, 200))
    line(img, 3, 5, 8, 1, (110, 80, 50)); line(img, 13, 5, 8, 1, (110, 80, 50))
    outline(img, OUT_C)
    return img


def swamp_lantern(frame):
    img = new(12, 28)
    rect(img, 5, 6, 2, 22, (90, 76, 60))
    rect(img, 2, 2, 8, 6, (60, 70, 60))
    rect(img, 3, 3, 6, 4, (170, 240, 140) if frame == 0 else (140, 220, 120))
    outline(img, OUT_C)
    return img


# ------------------------------------------------------------- Ossório (4e)
def townhouse(kind, wall, roof):
    W, H = (80, 74) if kind != "house" else (64, 70)
    img = house(W, H, roof, mix(roof, (30, 30, 40), 0.3), wall, mix(wall, (40, 40, 50), 0.25), kind)
    # segundo andar: faixa de janelas extras acima da porta
    for wx in range(10, W - 14, 14):
        rect(img, wx, H - 50, 8, 7, (60, 60, 80))
        rect(img, wx + 1, H - 49, 6, 5, (180, 210, 240))
    return img


def banner(color):
    img = new(12, 34)
    rect(img, 5, 0, 2, 34, (110, 90, 70))
    rect(img, 0, 2, 12, 2, (200, 170, 90))
    rect(img, 1, 4, 10, 18, color)
    for x in range(1, 11):
        put(img, x, 22 + abs(x - 5) // 2, color)
    rect(img, 4, 9, 4, 4, (230, 200, 90))
    outline(img, OUT_C)
    return img


def statue():
    img = new(24, 44)
    rect(img, 2, 34, 20, 9, (150, 146, 140))
    rect(img, 1, 34, 22, 2, (176, 170, 164))
    ellipse(img, 12, 12, 5, 5, (200, 196, 188))        # cabeça (menino)
    rect(img, 8, 17, 8, 14, (186, 182, 176))
    rect(img, 9, 6, 6, 2, (220, 196, 110))             # coroa pequena
    for x in (9, 11, 13):
        put(img, x, 5, (220, 196, 110))
    rect(img, 5, 19, 3, 9, (186, 182, 176)); rect(img, 16, 19, 3, 9, (186, 182, 176))
    outline(img, OUT_C)
    return img


def fountain(frame):
    img = new(40, 30)
    ellipse(img, 20, 20, 18, 8, (160, 156, 150))
    ellipse(img, 20, 19, 15, 6, (90, 150, 200))
    rect(img, 18, 6, 4, 12, (176, 170, 164))
    for k in range(5):
        a = (k + frame * 0.5) / 5 * math.pi
        x = 20 + int(9 * math.cos(a)); y = 6 + int(4 * math.sin(a))
        put(img, x, y, (200, 230, 250)); put(img, x, y + 1, (150, 200, 240))
    ellipse(img, 20, 5, 3, 2, (220, 240, 255))
    outline(img, OUT_C)
    return img


def city_gate():
    W, H = 64, 56
    img = new(W, H)
    rect(img, 0, 8, 16, 48, (168, 162, 156)); rect(img, 48, 8, 16, 48, (168, 162, 156))
    rect(img, 0, 0, W, 14, (176, 170, 164))
    for x in range(0, W, 8):
        rect(img, x, -2 if False else 0, 5, 4, (190, 184, 176))
    for y in range(14, 56, 6):
        rect(img, 0, y, 16, 1, (140, 134, 128)); rect(img, 48, y, 16, 1, (140, 134, 128))
    ellipse(img, 32, 20, 16, 10, (176, 170, 164))
    rect(img, 16, 20, 32, 36, (0, 0, 0, 0))
    for y in range(14, 22):
        for x in range(16, 48):
            if ((x - 32) / 16) ** 2 + ((y - 22) / 9) ** 2 > 1:
                put(img, x, y, (176, 170, 164))
    rect(img, 28, 3, 8, 7, (60, 80, 150)); rect(img, 31, 5, 2, 3, (230, 200, 90))
    outline(img, OUT_C)
    return img


def bookshelf():
    img = new(30, 34)
    rect(img, 1, 1, 28, 32, (110, 78, 50))
    r = rng(5)
    for row in range(4):
        y = 3 + row * 8
        rect(img, 2, y + 6, 26, 1, (80, 56, 36))
        x = 3
        while x < 26:
            w = r.randint(2, 3)
            rect(img, x, y, w, 6, [(170, 60, 60), (60, 90, 160), (70, 140, 80), (200, 170, 90)][r.randint(0, 3)])
            x += w
    outline(img, OUT_C)
    return img


def lectern():
    img = new(16, 22)
    rect(img, 6, 8, 4, 13, (110, 78, 50))
    rect(img, 3, 19, 10, 2, (90, 64, 40))
    rect(img, 1, 4, 14, 5, (130, 92, 60))
    rect(img, 2, 2, 12, 4, (240, 232, 210))
    rect(img, 8, 2, 1, 4, (180, 170, 150))
    outline(img, OUT_C)
    return img


def portrait():
    img = new(22, 26)
    rect(img, 0, 0, 22, 26, (190, 150, 70))
    rect(img, 2, 2, 18, 22, (60, 50, 80))
    ellipse(img, 11, 11, 5, 6, (232, 190, 150))       # o rosto (igual ao do protagonista)
    rect(img, 6, 4, 10, 4, (70, 50, 40))
    rect(img, 7, 3, 8, 2, (230, 200, 90))
    rect(img, 5, 17, 12, 7, (60, 80, 150))
    outline(img, OUT_C)
    return img


def bell_tower():
    img = new(26, 44)
    rect(img, 3, 12, 20, 32, (168, 162, 156))
    for y in range(14, 44, 6):
        rect(img, 3, y, 20, 1, (140, 134, 128))
    for y in range(0, 12):
        half = (y + 2) * 1.0
        rect(img, int(13 - half), y, int(half * 2), 1, (90, 80, 110))
    rect(img, 8, 16, 10, 10, (40, 36, 50))
    ellipse(img, 13, 22, 4, 4, (220, 190, 90))
    outline(img, OUT_C)
    return img


def torch(frame):
    img = new(10, 22)
    rect(img, 4, 8, 2, 14, (110, 80, 54))
    flame = [(255, 200, 90), (255, 150, 60)]
    ellipse(img, 5, 5 - frame, 3, 4, flame[frame])
    ellipse(img, 5, 6, 1.5, 2, (255, 240, 180))
    outline(img, OUT_C)
    return img


# ------------------------------------------------------------- picos (4f)
def snow_pine():
    img = tree_pine()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            c = img.getpixel((x, y))
            if c[3] and c[:3] in [(44, 104, 74)] and hash01(x, y, 3) > 0.35:
                put(img, x, y, (236, 244, 252))
    return img


def log_cabin(kind, roof, wood):
    """Cabana de toras de Raizal (Bosque): paredes de toras com as pontas redondas
    nos cantos e telhado de musgo com tufos de folhas e cogumelos."""
    W, H = (80, 70) if kind != "house" else (64, 62)
    wood_d = mix(wood, (40, 24, 16), 0.35)
    img = house(W, H, roof, mix(roof, (20, 40, 20), 0.35), wood, wood_d, kind)
    wall_top = H - 30
    for y in range(wall_top + 2, H - 1):
        for x in range(3, W - 3):
            px = img.getpixel((x, y))
            if px[3] and px[:3] in (wood, mix(wood, wood_d, 0.25), wood_d):
                ring = (y - wall_top) % 5
                c = mix(wood, (255, 230, 190), 0.18) if ring == 1 else (wood_d if ring == 0 else wood)
                if hash01(x, y, 9) > 0.93:
                    c = wood_d
                put(img, x, y, c)
    for yy in range(wall_top + 3, H - 3, 5):  # pontas das toras nos cantos
        for cx in (3, W - 4):
            ellipse(img, cx, yy + 1, 2.2, 2.2, mix(wood, (240, 214, 170), 0.35))
            put(img, cx, yy + 1, wood_d)
    for i in range(9):  # tufos de folhas no telhado
        x = int(W * 0.18 + hash01(i, 1, W) * W * 0.64)
        y = int(4 + hash01(i, 2, W) * (wall_top - 6))
        ellipse(img, x, y, 3, 2, mix(roof, (190, 230, 120), 0.45))
    for i, x in enumerate((int(W * 0.24), int(W * 0.7))):  # cogumelos na beira
        y = wall_top - 1
        rect(img, x, y, 1, 2, (236, 226, 200))
        ellipse(img, x, y - 1, 2, 1.2, (210, 60, 60) if i == 0 else (230, 160, 60))
    outline(img, OUT_C)
    return img


def chalet(kind, roof):
    W, H = (80, 70) if kind != "house" else (64, 62)
    img = house(W, H, roof, mix(roof, (30, 30, 40), 0.3), (150, 110, 74), (116, 84, 56), kind)
    for y in range(2, 10):
        for x in range(int(W * 0.25), int(W * 0.75)):
            if img.getpixel((x, y))[3]:
                put(img, x, y, (240, 246, 252) if hash01(x, y, 4) > 0.15 else (210, 226, 240))
    return img


def snowman():
    img = new(18, 26)
    ellipse(img, 9, 19, 7, 6, (240, 246, 252))
    ellipse(img, 9, 9, 5, 5, (240, 246, 252))
    put(img, 7, 8, (30, 30, 40)); put(img, 11, 8, (30, 30, 40))
    rect(img, 9, 10, 3, 1, (240, 140, 60))
    rect(img, 5, 3, 8, 2, (60, 60, 70)); rect(img, 6, 0, 6, 3, (60, 60, 70))
    rect(img, 4, 13, 10, 2, (200, 60, 60))
    outline(img, OUT_C)
    return img


def prayer_flags():
    img = new(48, 16)
    rect(img, 0, 2, 2, 14, (110, 80, 54)); rect(img, 46, 2, 2, 14, (110, 80, 54))
    cols = [(220, 70, 70), (240, 200, 70), (80, 170, 90), (70, 120, 200), (240, 240, 240)]
    for i, x in enumerate(range(3, 44, 6)):
        y = 3 + int(3 * math.sin(i / 7 * math.pi))
        rect(img, x, y, 4, 5, cols[i % 5])
    outline(img, OUT_C)
    return img


def kettle(frame):
    img = new(20, 20)
    ellipse(img, 10, 13, 7, 6, (170, 100, 70))
    rect(img, 6, 6, 8, 2, (130, 70, 50))
    line(img, 16, 12, 19, 8, (170, 100, 70))
    for k in range(3):
        put(img, 18 + (k + frame) % 2, 6 - k * 2, (230, 236, 240))
    rect(img, 4, 19, 12, 1, (200, 120, 60))
    outline(img, OUT_C)
    return img


def letter():
    img = new(12, 10)
    rect(img, 1, 1, 10, 8, (244, 236, 214))
    line(img, 1, 1, 6, 5, (190, 176, 150)); line(img, 10, 1, 6, 5, (190, 176, 150))
    rect(img, 5, 5, 2, 2, (200, 60, 70))
    outline(img, OUT_C)
    return img


def monastery_gate():
    W, H = 56, 48
    img = new(W, H)
    rect(img, 4, 14, 8, 34, (180, 60, 50)); rect(img, 44, 14, 8, 34, (180, 60, 50))
    rect(img, 0, 6, W, 6, (90, 70, 60)); rect(img, 2, 12, W - 4, 3, (200, 170, 90))
    for x in range(0, W, 4):
        put(img, x, 5, (240, 246, 252)); put(img, x + 1, 5, (240, 246, 252))
    outline(img, OUT_C)
    return img


# ------------------------------------------------------------- deserto (4g)
def cactus():
    img = new(18, 26)
    rect(img, 7, 4, 5, 22, (80, 150, 80))
    rect(img, 2, 10, 4, 3, (80, 150, 80)); rect(img, 2, 6, 3, 6, (80, 150, 80))
    rect(img, 13, 13, 4, 3, (80, 150, 80)); rect(img, 14, 8, 3, 7, (80, 150, 80))
    for y in range(6, 24, 4):
        put(img, 9, y, (120, 190, 110))
    put(img, 9, 3, (240, 120, 160))
    outline(img, OUT_C)
    return img


def tent(kind, color):
    W, H = (80, 60) if kind != "house" else (64, 52)
    img = new(W, H)
    for y in range(4, H - 1):
        half = (y - 2) * (W / 2 - 3) / (H - 4)
        for x in range(int(W / 2 - half), int(W / 2 + half)):
            stripe = ((x // 6) % 2) == 0
            put(img, x, y, color if stripe else mix(color, (250, 240, 220), 0.5))
    rect(img, W // 2 - 1, 0, 2, 6, (120, 90, 60))
    rect(img, W // 2 - 7, H - 18, 14, 17, (60, 40, 30))
    if kind == "ranch":
        rect(img, W // 2 - 6, H - 30, 12, 9, (246, 240, 226)); rect(img, W // 2 - 1, H - 29, 2, 7, (214, 70, 70)); rect(img, W // 2 - 4, H - 26, 8, 2, (214, 70, 70))
    if kind == "shop":
        rect(img, W // 2 - 6, H - 30, 12, 9, (246, 240, 226)); ellipse(img, W // 2, H - 26, 3, 3, (220, 180, 60))
    outline(img, OUT_C)
    return img


def broken_column():
    img = new(16, 36)
    rect(img, 3, 6, 10, 28, (214, 190, 150))
    for x in range(4, 13, 3):
        rect(img, x, 6, 1, 28, (190, 166, 126))
    rect(img, 1, 33, 14, 3, (196, 172, 132))
    for x in range(3, 13):
        put(img, x, 5 - (x * 7) % 4, (214, 190, 150))
    outline(img, OUT_C)
    return img


def hourglass_big():
    img = new(24, 38)
    rect(img, 1, 0, 22, 3, (150, 110, 60)); rect(img, 1, 35, 22, 3, (150, 110, 60))
    rect(img, 2, 3, 2, 32, (150, 110, 60)); rect(img, 20, 3, 2, 32, (150, 110, 60))
    for y in range(3, 35):
        half = abs(y - 19) * 0.5 + 1
        for x in range(int(12 - half), int(12 + half)):
            sand = (y > 27 and abs(x - 12) < (y - 27)) or (y < 19 and y > 10)
            put(img, x, y, (230, 196, 120) if sand else (200, 230, 240))
    outline(img, OUT_C)
    return img


def drum():
    img = new(16, 16)
    ellipse(img, 8, 11, 7, 4, (170, 80, 60))
    rect(img, 1, 6, 14, 6, (170, 80, 60))
    ellipse(img, 8, 6, 7, 3, (236, 220, 190))
    for x in range(2, 15, 3):
        line(img, x, 7, x + 1, 12, (240, 200, 90))
    outline(img, OUT_C)
    return img


def oasis_pool():
    img = new(48, 28)
    ellipse(img, 24, 14, 22, 12, (210, 180, 120))
    ellipse(img, 24, 14, 19, 9, (70, 160, 200))
    ellipse(img, 20, 11, 8, 3, (140, 210, 230))
    return img


# ------------------------------------------------------------- castelo e epílogo (4h)
def throne():
    img = new(34, 44)
    rect(img, 4, 2, 26, 34, (110, 40, 54))
    rect(img, 7, 6, 20, 26, (150, 54, 66))
    for x in (4, 12, 22, 30):
        rect(img, x - 2, 0, 4, 6, (220, 190, 90))
    rect(img, 1, 26, 32, 12, (200, 170, 80))
    rect(img, 3, 36, 28, 7, (150, 120, 60))
    outline(img, OUT_C)
    return img


def pillar():
    img = new(20, 48)
    rect(img, 4, 6, 12, 38, (96, 84, 110))
    for x in range(5, 16, 3):
        rect(img, x, 6, 1, 38, (76, 66, 90))
    rect(img, 1, 2, 18, 5, (120, 106, 136)); rect(img, 1, 43, 18, 5, (120, 106, 136))
    outline(img, OUT_C)
    return img


def candelabra(frame):
    img = new(18, 30)
    rect(img, 8, 8, 2, 20, (200, 170, 80)); rect(img, 4, 27, 10, 2, (200, 170, 80))
    rect(img, 2, 10, 14, 2, (200, 170, 80))
    for x in (2, 8, 15):
        rect(img, x, 5, 2, 5, (240, 236, 220))
        ellipse(img, x + 1, 3 - frame, 1.5, 2, (255, 200, 90))
    outline(img, OUT_C)
    return img


def castle_door():
    W, H = 48, 52
    img = new(W, H)
    rect(img, 0, 0, W, H, (96, 84, 110))
    ellipse(img, 24, 18, 18, 14, (60, 40, 30))
    rect(img, 6, 18, 36, 34, (60, 40, 30))
    for x in range(8, 41, 6):
        rect(img, x, 10, 1, 42, (90, 64, 44))
    rect(img, 22, 30, 4, 4, (220, 190, 90))
    outline(img, OUT_C)
    return img


def crown_pedestal(frame):
    img = new(22, 30)
    rect(img, 5, 14, 12, 16, (120, 106, 136)); rect(img, 3, 12, 16, 3, (150, 136, 166))
    rect(img, 5, 6, 12, 6, (236, 226, 200))                 # coroa de osso
    for x in (5, 9, 13, 16):
        rect(img, x, 3, 2, 4, (236, 226, 200))
    line(img, 8, 6, 12, 11, (90, 70, 60) if frame == 0 else (230, 120, 255))   # a rachadura
    outline(img, OUT_C)
    return img


def vitrine(empty):
    img = new(32, 36)
    rect(img, 2, 22, 28, 13, (90, 70, 60))
    rect(img, 3, 2, 26, 20, (190, 230, 240))
    rect(img, 4, 3, 24, 18, (220, 240, 248))
    line(img, 6, 4, 12, 18, (250, 255, 255))
    if not empty:
        rect(img, 10, 12, 12, 6, (236, 226, 200))
    rect(img, 9, 25, 14, 5, (240, 220, 150))
    outline(img, OUT_C)
    return img


def lighthouse_lit(frame):
    img = lighthouse()
    W, H = img.size
    out = new(W + 40, H)
    out.alpha_composite(img, (20, 0))
    cx, cy = 20 + W // 2, 10
    ellipse(out, cx, cy, 5, 4, (255, 240, 160))
    d = -1 if frame == 0 else 1
    for k in range(18):
        for w in range(-1 - k // 6, 2 + k // 6):
            put(out, cx + d * (6 + k), cy + w, mix((255, 240, 170), (255, 250, 220), k / 18))
    return out


# ------------------------------------------------------------- empacotamento
PROPS = {
    # id: (função, quadros, fps, origem em px (pés), colisão [células relativas], camada, interativo)
    "palm": (palm, 2, 0.8, (20, 50), [[0, 0]], "y", False),
    "rock_small": (lambda f: rock(16, 14, 3), 1, 0, (8, 13), [[0, 0]], "y", False),
    "rock_big": (lambda f: rock(30, 22, 8), 1, 0, (23, 21), [[0, 0], [-1, 0]], "y", False),
    "hut": (lambda f: hut(), 1, 0, (40, 65),
            [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]],
            "y", False),
    "boat": (lambda f: boat(), 1, 0, (24, 22), [[-1, 0], [0, 0], [1, 0]], "y", False),
    "sign": (lambda f: sign(), 1, 0, (8, 17), [[0, 0]], "y", True),
    "barrel": (lambda f: barrel(), 1, 0, (7, 15), [[0, 0]], "y", False),
    "crate": (lambda f: crate(), 1, 0, (8, 15), [[0, 0]], "y", False),
    "net_rack": (lambda f: net_rack(), 1, 0, (24, 23), [[-1, 0], [0, 0]], "y", False),
    "driftwood": (lambda f: driftwood(), 1, 0, (15, 11), [], "ground", False),
    "starfish": (lambda f: starfish(), 1, 0, (6, 10), [], "ground", False),
    "campfire": (campfire_stones, 2, 6.0, (8, 15), [[0, 0]], "y", False),
    "bed": (lambda f: bed(), 1, 0, (8, 29), [[0, 0], [0, -1]], "y", True),
    "table": (lambda f: table(), 1, 0, (24, 21), [[-1, 0], [0, 0]], "y", False),
    "stool": (lambda f: stool(), 1, 0, (6, 11), [[0, 0]], "y", False),
    "shelf": (lambda f: shelf(), 1, 0, (24, 29), [[-1, 0], [0, 0]], "y", True),
    "plant": (lambda f: plant(), 1, 0, (7, 17), [[0, 0]], "y", False),
    "lamp": (lamp, 2, 3.0, (5, 15), [[0, 0]], "y", False),
    "rug": (lambda f: rug(), 1, 0, (24, 29), [], "ground", False),
    "rod_rack": (lambda f: rod_rack(), 1, 0, (8, 27), [[0, 0]], "y", True),
    "house_ranch": (lambda f: house(80, 70, (200, 70, 70), (150, 46, 50), (240, 226, 196), (196, 176, 146), "ranch"), 1, 0, (40, 69),
                    [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "house_shop": (lambda f: house(80, 70, (70, 110, 180), (46, 76, 130), (236, 222, 190), (190, 172, 140), "shop"), 1, 0, (40, 69),
                   [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "house_a": (lambda f: house(64, 62, (214, 120, 60), (160, 84, 40), (240, 232, 210), (198, 184, 156), "house"), 1, 0, (32, 61),
                [[-2, 0], [-1, 0], [1, 0], [-2, -1], [-1, -1], [0, -1], [1, -1]], "y", False),
    "house_b": (lambda f: house(64, 62, (70, 150, 140), (46, 104, 98), (236, 226, 200), (190, 176, 150), "house"), 1, 0, (32, 61),
                [[-2, 0], [-1, 0], [1, 0], [-2, -1], [-1, -1], [0, -1], [1, -1]], "y", False),
    "lighthouse": (lambda f: lighthouse(), 1, 0, (16, 91), [[0, 0], [-1, 0], [0, -1], [-1, -1]], "y", True),
    "fence": (lambda f: fence(), 1, 0, (8, 15), [[0, 0]], "y", False),
    "lamp_post": (lamp_post, 2, 2.0, (5, 29), [[0, 0]], "y", False),
    "well": (lambda f: well(), 1, 0, (13, 27), [[0, 0], [-1, 0]], "y", True),
    "stall": (lambda f: stall(), 1, 0, (24, 33), [[-1, 0], [0, 0], [1, 0]], "y", False),
    "flower_box": (lambda f: flower_box(), 1, 0, (8, 13), [[0, 0]], "y", False),
    "net_snag": (lambda f: net_snag(), 1, 0, (10, 13), [[0, 0]], "y", True),
    "tree_oak": (lambda f: tree_oak(1), 1, 0, (20, 50), [[0, 0], [-1, 0]], "y", False),
    "tree_oak2": (lambda f: tree_oak(7), 1, 0, (20, 50), [[0, 0], [-1, 0]], "y", False),
    "tree_pine": (lambda f: tree_pine(), 1, 0, (14, 44), [[0, 0]], "y", False),
    "root_wall": (lambda f: root_wall(), 1, 0, (17, 24), [[-1, 0], [0, 0]], "y", True),
    "root_arch": (lambda f: root_arch(), 1, 0, (17, 29), [[-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]], "y", False),
    "stump": (lambda f: stump(), 1, 0, (9, 12), [[0, 0]], "y", False),
    "log": (lambda f: log(), 1, 0, (17, 12), [[-1, 0], [0, 0]], "y", False),
    "mushrooms": (lambda f: mushrooms(0), 1, 0, (8, 13), [], "ground", False),
    "glow_shroom": (lambda f: mushrooms(f, True), 2, 1.5, (8, 13), [], "ground", False),
    "herb_blue": (lambda f: herb_blue(), 1, 0, (7, 15), [[0, 0]], "y", True),
    "house_stone": (lambda f: house(64, 62, (110, 110, 124), (76, 76, 90), (180, 172, 160), (140, 132, 120), "house"), 1, 0, (32, 61), [[-2, 0], [-1, 0], [1, 0], [-2, -1], [-1, -1], [0, -1], [1, -1]], "y", False),
    "house_stone_ranch": (lambda f: house(80, 70, (150, 70, 60), (110, 46, 40), (180, 172, 160), (140, 132, 120), "ranch"), 1, 0, (40, 69), [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "house_stone_shop": (lambda f: house(80, 70, (70, 90, 120), (46, 62, 90), (180, 172, 160), (140, 132, 120), "shop"), 1, 0, (40, 69), [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "rails": (lambda f: rails(), 1, 0, (8, 15), [], "ground", False),
    "mine_cart": (lambda f: mine_cart(), 1, 0, (13, 19), [[0, 0]], "y", False),
    "mine_lamp": (mine_lamp, 2, 2.0, (6, 29), [[0, 0]], "y", False),
    "crystal": (crystal, 2, 1.2, (8, 17), [[0, 0]], "y", False),
    "beam_frame": (lambda f: beam_frame(), 1, 0, (24, 39), [[-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]], "y", False),
    "anvil": (lambda f: anvil(), 1, 0, (10, 13), [[0, 0]], "y", False),
    "forge": (forge, 2, 4.0, (20, 33), [[-1, 0], [0, 0], [1, 0], [-1, -1], [0, -1], [1, -1]], "y", False),
    "chain_gate": (lambda f: chain_gate(), 1, 0, (17, 27), [[-1, 0], [0, 0]], "y", True),
    "rubble": (lambda f: rubble(), 1, 0, (17, 21), [[-1, 0], [0, 0]], "y", True),
    "map_board": (lambda f: map_board(), 1, 0, (15, 23), [[0, 0], [-1, 0]], "y", True),
    "scarf": (lambda f: scarf(), 1, 0, (8, 9), [[0, 0]], "y", True),
    "helmet_lamp": (lambda f: helmet_lamp(), 1, 0, (7, 11), [[0, 0]], "y", True),
    "reeds": (reeds, 2, 1.2, (8, 21), [[0, 0]], "y", False),
    "lilypad": (lambda f: lilypad(), 1, 0, (8, 11), [], "ground", False),
    "willow": (lambda f: willow(), 1, 0, (22, 54), [[0, 0], [-1, 0]], "y", False),
    "dead_tree": (lambda f: dead_tree(), 1, 0, (15, 39), [[0, 0]], "y", False),
    "cauldron": (cauldron, 2, 2.5, (13, 25), [[0, 0], [-1, 0]], "y", True),
    "stilt_house": (lambda f: stilt_house("house", (110, 130, 80), (80, 100, 60)), 1, 0, (32, 61), [[-2, 0], [-1, 0], [1, 0], [-2, -1], [-1, -1], [0, -1], [1, -1]], "y", False),
    "stilt_house_ranch": (lambda f: stilt_house("ranch", (150, 80, 70), (110, 56, 50)), 1, 0, (40, 69), [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "stilt_house_shop": (lambda f: stilt_house("shop", (80, 110, 130), (56, 80, 100)), 1, 0, (40, 69), [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "mail_bag": (lambda f: mail_bag(), 1, 0, (8, 13), [[0, 0]], "y", True),
    "swamp_lantern": (swamp_lantern, 2, 1.5, (6, 27), [[0, 0]], "y", False),
    "townhouse": (lambda f: townhouse("house", (210, 200, 180), (90, 100, 150)), 1, 0, (32, 69), [[-2, 0], [-1, 0], [1, 0], [-2, -1], [-1, -1], [0, -1], [1, -1]], "y", False),
    "townhouse_ranch": (lambda f: townhouse("ranch", (214, 204, 186), (170, 70, 70)), 1, 0, (40, 73), [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "townhouse_shop": (lambda f: townhouse("shop", (214, 204, 186), (70, 100, 160)), 1, 0, (40, 73), [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "banner_blue": (lambda f: banner((60, 80, 150)), 1, 0, (6, 33), [[0, 0]], "y", False),
    "statue_prince": (lambda f: statue(), 1, 0, (12, 43), [[0, 0]], "y", True),
    "fountain": (fountain, 2, 3.0, (20, 27), [[-1, 0], [0, 0], [1, 0]], "y", False),
    "city_gate": (lambda f: city_gate(), 1, 0, (32, 55), [[-2, 0], [-1, 0], [1, 0], [-2, -1], [-1, -1], [0, -1], [1, -1]], "y", False),
    "bookshelf": (lambda f: bookshelf(), 1, 0, (15, 33), [[0, 0], [-1, 0]], "y", True),
    "lectern": (lambda f: lectern(), 1, 0, (8, 21), [[0, 0]], "y", True),
    "portrait": (lambda f: portrait(), 1, 0, (11, 25), [[0, 0]], "y", True),
    "bell_tower": (lambda f: bell_tower(), 1, 0, (13, 43), [[0, 0], [-1, 0]], "y", True),
    "torch": (torch, 2, 6.0, (5, 21), [[0, 0]], "y", False),
    "snow_pine": (lambda f: snow_pine(), 1, 0, (14, 44), [[0, 0]], "y", False),
    "log_cabin": (lambda f: log_cabin("house", (86, 132, 66), (150, 104, 62)), 1, 0, (32, 61), [[-2, 0], [-1, 0], [1, 0], [-2, -1], [-1, -1], [0, -1], [1, -1]], "y", False),
    "log_cabin_b": (lambda f: log_cabin("house", (122, 140, 60), (128, 86, 52)), 1, 0, (32, 61), [[-2, 0], [-1, 0], [1, 0], [-2, -1], [-1, -1], [0, -1], [1, -1]], "y", False),
    "log_cabin_ranch": (lambda f: log_cabin("ranch", (74, 124, 64), (156, 108, 64)), 1, 0, (40, 69), [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "log_cabin_shop": (lambda f: log_cabin("shop", (96, 128, 70), (144, 100, 60)), 1, 0, (40, 69), [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "chalet": (lambda f: chalet("house", (120, 70, 60)), 1, 0, (32, 61), [[-2, 0], [-1, 0], [1, 0], [-2, -1], [-1, -1], [0, -1], [1, -1]], "y", False),
    "chalet_ranch": (lambda f: chalet("ranch", (170, 60, 60)), 1, 0, (40, 69), [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "chalet_shop": (lambda f: chalet("shop", (70, 90, 150)), 1, 0, (40, 69), [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "snowman": (lambda f: snowman(), 1, 0, (9, 25), [[0, 0]], "y", True),
    "prayer_flags": (lambda f: prayer_flags(), 1, 0, (24, 15), [], "y", False),
    "kettle": (kettle, 2, 2.0, (10, 19), [[0, 0]], "y", False),
    "letter": (lambda f: letter(), 1, 0, (6, 9), [[0, 0]], "y", True),
    "monastery_gate": (lambda f: monastery_gate(), 1, 0, (28, 47), [[-1, 0], [-1, -1], [1, 0], [1, -1]], "y", False),
    "cactus": (lambda f: cactus(), 1, 0, (9, 25), [[0, 0]], "y", False),
    "tent": (lambda f: tent("house", (200, 120, 70)), 1, 0, (32, 51), [[-2, 0], [-1, 0], [1, 0], [-2, -1], [-1, -1], [0, -1], [1, -1]], "y", False),
    "tent_ranch": (lambda f: tent("ranch", (210, 90, 80)), 1, 0, (40, 59), [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "tent_shop": (lambda f: tent("shop", (80, 120, 180)), 1, 0, (40, 59), [[-2, 0], [-1, 0], [1, 0], [2, 0], [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1]], "y", False),
    "broken_column": (lambda f: broken_column(), 1, 0, (8, 35), [[0, 0]], "y", False),
    "hourglass": (lambda f: hourglass_big(), 1, 0, (12, 37), [[0, 0]], "y", True),
    "drum": (lambda f: drum(), 1, 0, (8, 15), [[0, 0]], "y", False),
    "oasis_pool": (lambda f: oasis_pool(), 1, 0, (24, 27), [[-1, 0], [0, 0], [1, 0], [-1, -1], [0, -1], [1, -1]], "ground", False),
    "throne": (lambda f: throne(), 1, 0, (17, 43), [[-1, 0], [0, 0], [1, 0]], "y", True),
    "pillar": (lambda f: pillar(), 1, 0, (10, 47), [[0, 0]], "y", False),
    "candelabra": (candelabra, 2, 5.0, (9, 29), [[0, 0]], "y", False),
    "castle_door": (lambda f: castle_door(), 1, 0, (24, 51), [[-1, 0], [1, 0], [-1, -1], [0, -1], [1, -1]], "y", False),
    "crown_pedestal": (crown_pedestal, 2, 1.0, (11, 29), [[0, 0]], "y", True),
    "vitrine_empty": (lambda f: vitrine(True), 1, 0, (16, 35), [[0, 0], [-1, 0]], "y", True),
    "lighthouse_lit": (lighthouse_lit, 2, 1.0, (36, 91), [[0, 0], [-1, 0], [0, -1], [-1, -1]], "y", True),
    "raizerno_tree": (lambda f: raizerno_tree(), 1, 0, (28, 62), [[-1, 0], [0, 0], [1, 0], [-1, -1], [0, -1], [1, -1]], "y", True),
}


# Brilho aditivo opcional (iluminação simples por objeto)
LIGHTS = {
    "lamp": {"radius": 40, "color": [1.0, 0.82, 0.5], "intensity": 0.35, "offset": [0, -9]},
    "campfire": {"radius": 44, "color": [1.0, 0.6, 0.3], "intensity": 0.3, "offset": [0, -6]},
    "glow_shroom": {"radius": 26, "color": [0.5, 1.0, 0.95], "intensity": 0.4, "offset": [0, -6]},
    "mine_lamp": {"radius": 34, "color": [1.0, 0.8, 0.5], "intensity": 0.4, "offset": [0, -24]},
    "crystal": {"radius": 24, "color": [0.6, 0.9, 1.0], "intensity": 0.35, "offset": [0, -8]},
    "forge": {"radius": 48, "color": [1.0, 0.55, 0.25], "intensity": 0.45, "offset": [0, -12]},
    "cauldron": {"radius": 30, "color": [0.6, 1.0, 0.5], "intensity": 0.35, "offset": [0, -10]},
    "swamp_lantern": {"radius": 32, "color": [0.7, 1.0, 0.6], "intensity": 0.35, "offset": [0, -22]},
    "torch": {"radius": 34, "color": [1.0, 0.7, 0.4], "intensity": 0.35, "offset": [0, -14]},
    "kettle": {"radius": 20, "color": [1.0, 0.7, 0.5], "intensity": 0.25, "offset": [0, -4]},
    "candelabra": {"radius": 40, "color": [1.0, 0.75, 0.45], "intensity": 0.4, "offset": [0, -24]},
    "crown_pedestal": {"radius": 30, "color": [0.85, 0.6, 1.0], "intensity": 0.35, "offset": [0, -20]},
    "lighthouse_lit": {"radius": 64, "color": [1.0, 0.95, 0.7], "intensity": 0.45, "offset": [0, -80]},
    "lamp_post": {"radius": 36, "color": [1.0, 0.85, 0.55], "intensity": 0.28, "offset": [0, -25]},
}


def main():
    images = {}
    for pid, (fn, frames, fps, origin, col, layer, interact) in PROPS.items():
        images[pid] = [fn(f) for f in range(frames)]
    # empacota em linhas (prateleiras simples)
    sheet_w = 256
    x = y = 0
    row_h = 0
    rects = {}
    for pid, frames in images.items():
        w, h = frames[0].size
        total = w * len(frames)
        if x + total > sheet_w:
            x = 0
            y += row_h + 1
            row_h = 0
        rects[pid] = (x, y, w, h)
        x += total + 1
        row_h = max(row_h, h)
    sheet_h = y + row_h
    p2 = 1
    while p2 < sheet_h:
        p2 *= 2
    sheet = new(sheet_w, p2)
    meta = {"_comment": "Gerado por tools/art/gen_props.py. Não editar à mão.",
            "texture": "res://assets/props/props.png", "props": {}}
    for pid, frames in images.items():
        rx, ry, w, h = rects[pid]
        for i, fr in enumerate(frames):
            sheet.alpha_composite(fr, (rx + i * w, ry))
        fn, nf, fps, origin, col, layer, interact = PROPS[pid]
        meta["props"][pid] = {
            "rect": [rx, ry, w, h], "frames": nf, "fps": fps, "origin": list(origin),
            "collision": col, "layer": layer, "interactive": interact,
        }
        if pid in LIGHTS:
            meta["props"][pid]["light"] = LIGHTS[pid]
    out = ROOT / "assets" / "props" / "props.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    (ROOT / "data" / "props.json").write_text(json.dumps(meta, indent=1) + "\n", encoding="utf-8")
    print("props:", len(images), "->", out)


if __name__ == "__main__":
    main()
