#!/usr/bin/env python3
"""Gera os objetos de cenário (props) da Praia e da cabana do Bento.

Saída: assets/props/props.png + data/props.json (recortes, origem, colisão,
quadros de animação e se é interativo). Procedural e original.
"""
import json
import math
from pathlib import Path

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
}


# Brilho aditivo opcional (iluminação simples por objeto)
LIGHTS = {
    "lamp": {"radius": 40, "color": [1.0, 0.82, 0.5], "intensity": 0.35, "offset": [0, -9]},
    "campfire": {"radius": 44, "color": [1.0, 0.6, 0.3], "intensity": 0.3, "offset": [0, -6]},
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
