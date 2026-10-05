#!/usr/bin/env python3
"""Arte da batalha (pixel art original):
  - fundo da praia (400x180) com plataformas;
  - bonecos de treino da fase 2 (32x32, frente e costas), um por tipo;
  - ícones de tipo (9x9), do menu em anel (16x16) e de status.
Saída em assets/battle/.
"""
import math
from pathlib import Path

from PIL import Image

from draw import new, put, rect, ellipse, line, outline, mix, bayer, hash01, mirror

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets" / "battle"
OUTL = (40, 30, 48)


def battle_bg():
    W, H = 400, 180
    img = new(W, H)
    horizon = 70
    for y in range(H):
        for x in range(W):
            if y < horizon:
                t = y / horizon
                c = mix((92, 160, 228), (186, 226, 246), t)
                if bayer(x, y) < 0.5 and y % 9 == 0:
                    c = mix(c, (210, 236, 250), 0.4)
            elif y < horizon + 22:
                t = (y - horizon) / 22
                c = mix((58, 150, 196), (92, 190, 210), t)
                wv = math.sin(x * 0.18 + y * 1.3)
                if wv > 0.92:
                    c = (210, 244, 246)
            else:
                t = (y - horizon - 22) / (H - horizon - 22)
                c = mix((228, 202, 150), (240, 218, 168), t)
                if hash01(x, y, 4) > 0.94:
                    c = (214, 186, 132)
                elif hash01(x, y, 5) > 0.97:
                    c = (250, 234, 192)
            put(img, x, y, c)
    # espuma na beira
    for x in range(W):
        y = horizon + 22 + int(1.5 * math.sin(x * 0.11))
        put(img, x, y, (244, 252, 250))
        put(img, x, y + 1, (206, 236, 240))
    # nuvens
    for (cx, cy, w) in [(60, 18, 46), (210, 30, 60), (340, 14, 40)]:
        for i in range(5):
            ellipse(img, cx + (i - 2) * w / 5, cy + (2 if i % 2 else 0), w / 4, 6, (250, 252, 255))
        for x in range(int(cx - w / 2), int(cx + w / 2)):
            put(img, x, cy + 5, (214, 228, 240))
    # ilha distante
    for x in range(300, 380):
        h = int(8 * math.sin((x - 300) / 80 * math.pi))
        for y in range(horizon - h, horizon):
            put(img, x, y, (110, 150, 160))
    # plataformas
    def platform(cx, cy, rx, ry):
        ellipse(img, cx, cy + 3, rx, ry, (196, 166, 112))
        ellipse(img, cx, cy, rx, ry, (214, 186, 132))
        ellipse(img, cx, cy - 1, rx - 4, ry - 3, (226, 200, 148))
        for k in range(14):
            a = k / 14 * 2 * math.pi
            px, py = cx + math.cos(a) * (rx - 2), cy + math.sin(a) * (ry - 1)
            put(img, int(px), int(py), (150, 190, 96))
            put(img, int(px), int(py) - 1, (120, 170, 80))
    platform(118, 130, 74, 15)
    platform(282, 130, 74, 15)
    return img


def battle_bg_forest():
    """Fundo de batalha do Bosque: céu entre copas, troncos ao fundo e chão de folhas."""
    W, H = 400, 180
    img = new(W, H)
    horizon = 92
    for y in range(H):
        for x in range(W):
            if y < horizon:
                t = y / horizon
                c = mix((150, 206, 196), (210, 236, 210), t)
            else:
                t = (y - horizon) / (H - horizon)
                c = mix((92, 140, 72), (118, 164, 86), t)
                if hash01(x, y, 6) > 0.93:
                    c = (150, 120, 70)
                elif hash01(x, y, 7) > 0.96:
                    c = (160, 196, 100)
            put(img, x, y, c)
    # troncos ao fundo (camada distante) e copas
    for i, tx in enumerate(range(-10, W + 20, 34)):
        w = 8 + (i * 7) % 6
        col = (98, 120, 96) if i % 2 else (84, 108, 88)
        rect(img, tx, 20, w, horizon - 18, col)
        rect(img, tx + w - 2, 20, 2, horizon - 18, mix(col, (40, 50, 40), 0.3))
    for i, cx in enumerate(range(-20, W + 40, 46)):
        ellipse(img, cx, 14 + (i % 3) * 6, 34, 22, (70, 124, 74))
        ellipse(img, cx - 6, 8 + (i % 3) * 6, 22, 12, (92, 150, 84))
    # raios de luz
    for x0 in (90, 230, 330):
        for y in range(20, horizon):
            for k in range(6):
                xx = x0 + (y - 20) // 3 + k
                if 0 <= xx < W and bayer(xx, y) < 0.35:
                    put(img, xx, y, mix(img.getpixel((xx, y))[:3], (250, 250, 210), 0.35))
    # raízes no chão
    for (x0, x1, y) in [(10, 70, 100), (330, 395, 104), (180, 230, 98)]:
        for x in range(x0, x1):
            put(img, x, y + int(2 * math.sin(x / 6)), (110, 80, 54))
            put(img, x, y + 1 + int(2 * math.sin(x / 6)), (88, 62, 42))
    def platform(cx, cy, rx, ry):
        ellipse(img, cx, cy + 3, rx, ry, (96, 120, 66))
        ellipse(img, cx, cy, rx, ry, (120, 150, 80))
        ellipse(img, cx, cy - 1, rx - 4, ry - 3, (138, 170, 92))
        for k in range(16):
            a = k / 16 * 2 * math.pi
            px, py = cx + math.cos(a) * (rx - 2), cy + math.sin(a) * (ry - 1)
            put(img, int(px), int(py), (196, 160, 90) if k % 3 == 0 else (90, 140, 70))
    platform(118, 130, 74, 15)
    platform(282, 130, 74, 15)
    return img


# ------------------------------------------------------------------ bonecos
TYPE_COLORS = {
    "fisico": ((214, 64, 64), (150, 36, 44)),
    "magico": ((140, 92, 214), (92, 56, 160)),
    "cura": ((80, 186, 110), (44, 128, 76)),
    "veneno": ((170, 96, 200), (112, 170, 70)),
}
BONE = (240, 236, 222)
BONE_D = (196, 188, 168)
WOOD = (160, 112, 66)
WOOD_D = (116, 78, 46)
STRAW = (230, 200, 110)


def dummy(kind, back=False):
    img = new(32, 32)
    c1, c2 = TYPE_COLORS[kind]
    # poste e base
    rect(img, 15, 18, 3, 12, WOOD)
    rect(img, 17, 18, 1, 12, WOOD_D)
    rect(img, 10, 29, 13, 2, WOOD_D)
    # corpo de palha
    ellipse(img, 16.5, 20, 7, 6, STRAW)
    for y in range(15, 26, 3):
        for x in range(10, 24):
            if img.getpixel((x, y))[3] and hash01(x, y, 2) > 0.5:
                put(img, x, y, (200, 166, 80))
    # braço (travessa)
    rect(img, 5, 17, 23, 2, WOOD)
    rect(img, 5, 18, 23, 1, WOOD_D)
    # crânio
    ellipse(img, 16.5, 9, 6.5, 6, BONE)
    rect(img, 12, 12, 9, 4, BONE)
    for x in range(12, 21):
        put(img, x, 15, BONE_D)
    if not back:
        rect(img, 12, 8, 3, 3, OUTL)
        rect(img, 18, 8, 3, 3, OUTL)
        put(img, 13, 9, (255, 255, 255))
        put(img, 16, 12, OUTL)
        for x in (14, 16, 18):
            put(img, x, 14, OUTL)
    else:
        for x in range(12, 21):
            put(img, x, 6, BONE_D)
        put(img, 18, 4, BONE_D)
    # acessório do tipo
    if kind == "fisico":
        rect(img, 10, 5, 13, 2, c1)
        rect(img, 22, 6, 3, 1, c1)
        rect(img, 23, 7, 2, 1, c2)
        ellipse(img, 4.5, 18, 3, 3, c1)
        ellipse(img, 28.5, 18, 3, 3, c1)
        put(img, 3, 16, (255, 150, 150))
        put(img, 27, 16, (255, 150, 150))
    elif kind == "magico":
        for i in range(8):
            w = 8 - i
            rect(img, 16 - w // 2 + (i // 3), 3 - i // 2 + 1 - (i % 2), w + 1, 1, c1 if i % 3 else c2)
        rect(img, 8, 4, 17, 2, c2)
        put(img, 18, 0, (255, 230, 120))
        put(img, 5, 16, (255, 230, 120))
        put(img, 28, 15, (200, 180, 255))
    elif kind == "cura":
        rect(img, 10, 15, 13, 3, c1)
        rect(img, 15, 18, 3, 4, c1)
        rect(img, 14, 19, 5, 1, (255, 255, 255))
        rect(img, 16, 18, 1, 3, (255, 255, 255))
        ellipse(img, 4.5, 18, 2.5, 2.5, (255, 255, 255))
        rect(img, 4, 17, 1, 3, c1)
        rect(img, 3, 18, 3, 1, c1)
    elif kind == "veneno":
        ellipse(img, 16.5, 4, 7, 3, c1)
        rect(img, 9, 4, 15, 2, c1)
        for (x, y) in [(10, 6), (11, 7), (22, 6), (22, 8)]:
            put(img, x, y, c2)
        ellipse(img, 28.5, 19, 2.5, 3, c2)
        put(img, 28, 22, c2)
        put(img, 5, 21, c2)
    outline(img, OUTL)
    if back:
        img = mirror(img)
    return img


# ------------------------------------------------------------------ ícones
def type_icon(kind):
    img = new(9, 9)
    c1, c2 = TYPE_COLORS[kind]
    ellipse(img, 4.5, 4.5, 4.5, 4.5, c2)
    ellipse(img, 4.5, 4.2, 3.8, 3.6, c1)
    w = (255, 255, 255)
    if kind == "fisico":
        rect(img, 3, 3, 4, 3, w)
        put(img, 2, 4, w)
    elif kind == "magico":
        for (x, y) in [(4, 1), (4, 2), (3, 3), (4, 3), (5, 3), (2, 4), (6, 4), (4, 4), (3, 5), (5, 5), (4, 6)]:
            put(img, x, y, w)
    elif kind == "cura":
        rect(img, 4, 2, 1, 5, w)
        rect(img, 2, 4, 5, 1, w)
    elif kind == "veneno":
        for (x, y) in [(4, 2), (4, 3), (3, 4), (4, 4), (5, 4), (3, 5), (4, 5), (5, 5), (4, 6)]:
            put(img, x, y, (220, 255, 160))
    return img


def ring_icon(kind):
    img = new(16, 16)
    ellipse(img, 8, 8, 7.5, 7.5, (36, 30, 60))
    ellipse(img, 8, 7.6, 6.6, 6.4, (70, 82, 128))
    w = (246, 242, 232)
    if kind == "moves":  # espada
        line(img, 4, 12, 11, 5, w)
        line(img, 5, 12, 12, 5, (200, 210, 230))
        rect(img, 4, 9, 4, 1, (230, 190, 90))
        put(img, 4, 12, (230, 190, 90))
    elif kind == "switch":  # setas trocando
        line(img, 4, 6, 11, 6, w)
        put(img, 10, 5, w)
        put(img, 10, 7, w)
        line(img, 5, 10, 12, 10, (130, 220, 240))
        put(img, 6, 9, (130, 220, 240))
        put(img, 6, 11, (130, 220, 240))
    elif kind == "items":  # bolsa
        ellipse(img, 8, 9.5, 4, 3.5, (200, 140, 80))
        rect(img, 6, 4, 4, 2, (160, 104, 60))
        rect(img, 7, 8, 2, 2, (250, 220, 120))
    elif kind == "flee":  # tênis
        rect(img, 4, 9, 8, 3, w)
        rect(img, 4, 6, 4, 3, w)
        rect(img, 4, 11, 9, 1, (130, 220, 240))
        put(img, 12, 10, w)
    outline(img, OUTL)
    return img


def status_icon():
    """Gota de veneno 7x8 (sem texto, vale para os 3 idiomas)."""
    img = new(9, 10)
    for (x, y) in [(4, 1), (4, 2), (3, 3), (4, 3), (5, 3)]:
        put(img, x, y, (170, 110, 220))
    ellipse(img, 4.5, 6, 3, 3, (150, 80, 200))
    put(img, 3, 5, (220, 190, 255))
    outline(img, OUTL)
    return img


def cake(frame):
    """Bolo de aniversário 28x26: quadros 0 e 1 = velas acesas (chama tremendo), 2 = apagadas."""
    img = new(28, 26)
    # prato
    ellipse(img, 14, 23, 13, 2.5, (220, 220, 232))
    # massa em dois andares
    rect(img, 4, 14, 20, 9, (196, 132, 84))
    rect(img, 4, 17, 20, 2, (250, 214, 150))
    rect(img, 7, 9, 14, 6, (214, 150, 100))
    # cobertura
    rect(img, 4, 13, 20, 2, (255, 170, 200))
    for x in (6, 11, 16, 21):
        put(img, x, 15, (255, 170, 200))
    rect(img, 7, 8, 14, 2, (255, 240, 246))
    for x in (8, 13, 18):
        put(img, x, 10, (255, 240, 246))
    # granulado
    for (x, y, c) in [(6, 20, (120, 200, 255)), (12, 21, (255, 220, 90)), (19, 20, (150, 240, 140)), (15, 11, (255, 120, 140))]:
        put(img, x, y, c)
    # velas
    for i, x in enumerate((9, 14, 19)):
        rect(img, x, 3, 2, 5, [(120, 200, 255), (255, 120, 160), (150, 240, 140)][i])
        if frame < 2:
            fy = 0 if (frame + i) % 2 == 0 else 1
            put(img, x, fy, (255, 240, 160))
            put(img, x + 1, fy + 1, (255, 190, 80))
            put(img, x, fy + 1, (255, 150, 60))
            put(img, x + 1, fy, (255, 250, 220))
        else:
            put(img, x, 2, (90, 90, 100))
    outline(img, OUTL)
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    battle_bg_forest().save(OUT / "bg_bosque.png")
    battle_bg().save(OUT / "bg_praia.png")
    for kind in TYPE_COLORS:
        front = dummy(kind)
        back = dummy(kind, True)
        sheet = new(64, 32)
        sheet.alpha_composite(front, (0, 0))
        sheet.alpha_composite(back, (32, 0))
        sheet.save(OUT / f"dummy_{kind}.png")
        type_icon(kind).save(OUT / f"type_{kind}.png")
    for k in ["moves", "switch", "items", "flee"]:
        ring_icon(k).save(OUT / f"ring_{k}.png")
    status_icon().save(OUT / "status_poison.png")
    sheet = new(28 * 3, 26)
    for f in range(3):
        sheet.alpha_composite(cake(f), (28 * f, 0))
    sheet.save(OUT / "cake.png")
    print("arte de batalha gerada em", OUT)


if __name__ == "__main__":
    main()
