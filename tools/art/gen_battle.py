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


def battle_bg_region(kind):
    """Fundos das regiões 2–7, um gerador parametrizado: céu/teto, camada do
    fundo (silhuetas próprias de cada lugar) e chão com textura."""
    W, H = 400, 180
    P = {
        "minas": dict(sky=((40, 34, 44), (70, 58, 62)), ground=((86, 78, 80), (110, 100, 98)), speck=(60, 56, 60), speck2=(170, 150, 120), horizon=88,
                      plat=((80, 72, 74), (104, 96, 94), (122, 112, 108)), rim=(255, 196, 110)),
        "pantano": dict(sky=((120, 150, 130), (180, 196, 160)), ground=((64, 92, 66), (80, 110, 74)), speck=(50, 70, 52), speck2=(140, 170, 90), horizon=84,
                        plat=((70, 86, 58), (96, 112, 70), (112, 130, 80)), rim=(180, 120, 200)),
        "ossorio": dict(sky=((130, 150, 200), (220, 214, 210)), ground=((150, 146, 140), (170, 164, 156)), speck=(126, 122, 118), speck2=(196, 190, 180), horizon=86,
                        plat=((130, 124, 118), (156, 150, 142), (176, 170, 160)), rim=(210, 180, 90)),
        "picos": dict(sky=((150, 186, 230), (226, 238, 250)), ground=((220, 232, 242), (240, 246, 252)), speck=(190, 210, 228), speck2=(255, 255, 255), horizon=90,
                      plat=((180, 200, 220), (210, 226, 240), (232, 242, 250)), rim=(150, 210, 240)),
        "deserto": dict(sky=((236, 170, 110), (250, 222, 170)), ground=((226, 190, 130), (238, 206, 146)), speck=(206, 166, 108), speck2=(250, 226, 170), horizon=84,
                        plat=((200, 160, 100), (224, 186, 124), (240, 204, 142)), rim=(170, 120, 70)),
        "castelo": dict(sky=((30, 22, 40), (66, 46, 70)), ground=((70, 62, 80), (86, 76, 96)), speck=(56, 48, 66), speck2=(120, 90, 130), horizon=92,
                        plat=((110, 40, 54), (140, 54, 66), (162, 70, 80)), rim=(230, 190, 90)),
    }[kind]
    img = new(W, H)
    hz = P["horizon"]
    for y in range(H):
        for x in range(W):
            if y < hz:
                c = mix(P["sky"][0], P["sky"][1], y / hz)
            else:
                c = mix(P["ground"][0], P["ground"][1], (y - hz) / (H - hz))
                if hash01(x, y, 6) > 0.93:
                    c = P["speck"]
                elif hash01(x, y, 7) > 0.97:
                    c = P["speck2"]
            put(img, x, y, c)
    if kind == "minas":
        for i, x0 in enumerate(range(0, W, 70)):                       # vigas
            rect(img, x0 + 6, 18, 8, hz - 18, (110, 80, 54))
            rect(img, x0 - 10, 14, 40, 6, (126, 90, 60))
        for (cx, cy) in [(60, 50), (200, 40), (330, 56), (130, 70), (270, 74)]:   # cristais
            for k in range(3):
                h = 10 + k * 4
                for yy in range(h):
                    w = max(1, (h - yy) // 3)
                    rect(img, cx + k * 5 - w // 2, cy - yy, w, 1, (150, 220, 255) if yy < h - 2 else (240, 255, 255))
        for x in range(0, W):                                           # trilho
            put(img, x, hz + 6, (130, 130, 140)); put(img, x, hz + 12, (130, 130, 140))
            if x % 8 == 0:
                rect(img, x, hz + 5, 3, 9, (100, 74, 50))
        for x0 in (40, 360):                                            # lampiões
            ellipse(img, x0, 30, 10, 10, mix(P["sky"][0], (255, 200, 110), 0.35))
            rect(img, x0 - 2, 26, 4, 6, (255, 210, 120))
    elif kind == "pantano":
        for i, tx in enumerate(range(-10, W + 20, 52)):                  # árvores tortas
            col = (70, 90, 70)
            for yy in range(14, hz):
                xx = tx + int(4 * math.sin(yy / 12 + i))
                rect(img, xx, yy, 6, 1, col)
            ellipse(img, tx + 3, 16, 22, 10, (84, 112, 76))
            for k in range(4):
                line(img, tx - 8 + k * 6, 18, tx - 8 + k * 6, 34 + k * 3, (100, 130, 80))
        for (x0, x1, y) in [(0, 400, hz + 3)]:                          # água parada
            for x in range(x0, x1):
                for d in range(6):
                    if bayer(x, y + d) < 0.5:
                        put(img, x, y + d, (70, 110, 96))
        for x in range(0, W, 9):                                        # névoa
            for yy in range(hz - 12, hz):
                if bayer(x, yy) < 0.2:
                    put(img, x + (yy % 5), yy, (220, 230, 220))
    elif kind == "ossorio":
        for i, x0 in enumerate(range(0, W, 40)):                        # muralha e torres
            h = 34 if i % 3 else 52
            rect(img, x0, hz - h, 40, h, (176, 170, 164) if i % 2 else (166, 160, 154))
            for k in range(0, 40, 8):
                rect(img, x0 + k, hz - h - 5, 5, 5, (176, 170, 164))
            for yy in range(hz - h + 6, hz, 8):
                rect(img, x0, yy, 40, 1, (140, 134, 130))
        for x0 in (90, 300):                                            # estandartes
            rect(img, x0, hz - 46, 10, 22, (60, 80, 150))
            rect(img, x0 + 3, hz - 40, 4, 4, (230, 200, 90))
    elif kind == "picos":
        for (cx, h, w) in [(40, 60, 90), (150, 74, 110), (260, 58, 90), (360, 70, 100)]:
            for yy in range(h):
                ww = int(w * (yy / h))
                rect(img, cx - ww // 2, hz - h + yy, ww, 1, (150, 168, 196) if yy > 16 else (250, 252, 255))
        for k in range(40):                                             # flocos
            x = int(hash01(k, 3, 9) * W); y = int(hash01(k, 5, 9) * hz)
            put(img, x, y, (255, 255, 255))
    elif kind == "deserto":
        ellipse(img, 320, 26, 16, 16, (255, 240, 200))
        for (cx, h, w) in [(70, 18, 160), (230, 24, 200), (370, 14, 120)]:   # dunas
            for xx in range(cx - w // 2, cx + w // 2):
                hh = int(h * math.cos((xx - cx) / w * math.pi))
                for yy in range(hz - hh, hz):
                    if 0 <= xx < W:
                        put(img, xx, yy, (230, 186, 120))
        for x0 in (120, 280):                                           # colunas quebradas
            rect(img, x0, hz - 40, 10, 40, (214, 190, 150))
            rect(img, x0 - 2, hz - 42, 14, 3, (226, 204, 164))
    elif kind == "castelo":
        for i, x0 in enumerate(range(10, W, 64)):                       # colunas e vitrais
            rect(img, x0, 10, 12, hz - 10, (90, 76, 104))
            rect(img, x0 + 26, 20, 14, 30, (60, 50, 110))
            ellipse(img, x0 + 33, 20, 7, 6, (60, 50, 110))
            rect(img, x0 + 32, 22, 2, 26, (200, 170, 90))
            rect(img, x0 + 27, 34, 12, 2, (200, 170, 90))
        for x in range(0, W):                                           # tapete
            for yy in range(hz, H):
                if 170 <= x <= 230:
                    put(img, x, yy, (140, 40, 54) if 174 < x < 226 else (220, 180, 80))
    pl, pm, ph = P["plat"]

    def platform(cx, cy, rx, ry):
        ellipse(img, cx, cy + 3, rx, ry, pl)
        ellipse(img, cx, cy, rx, ry, pm)
        ellipse(img, cx, cy - 1, rx - 4, ry - 3, ph)
        for k in range(16):
            a = k / 16 * 2 * math.pi
            px, py = cx + math.cos(a) * (rx - 2), cy + math.sin(a) * (ry - 1)
            put(img, int(px), int(py), P["rim"] if k % 3 == 0 else pl)
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


def battle_bg_throne():
    """Batalha final: a sala do trono. Base do castelo, mais escura, com o trono
    gigante ao fundo, a coroa rachada brilhando e velas acesas."""
    img = battle_bg_region("castelo")
    W, H = img.size
    hz = 92
    for y in range(H):                                                   # mais escuro nas bordas
        for x in range(W):
            c = img.getpixel((x, y))
            d = abs(x - W / 2) / (W / 2)
            k = 0.55 + 0.45 * (1 - d * d)
            put(img, x, y, (int(c[0] * k), int(c[1] * k), int(c[2] * k)))
    cx = W // 2
    for y in range(8, hz):                                               # encosto do trono
        half = 30 - int((y - 8) * 0.08)
        for x in range(cx - half, cx + half):
            edge = x in (cx - half, cx + half - 1)
            put(img, x, y, (46, 34, 58) if not edge else (120, 96, 60))
    for k, x0 in enumerate(range(cx - 26, cx + 27, 13)):                 # pontas do encosto
        for y in range(0, 10):
            if abs(x0 - cx) // 13 % 2 == 0 or y > 4:
                rect(img, x0 - 2, 8 - y, 4, 1, (46, 34, 58))
    rect(img, cx - 40, hz - 18, 80, 18, (58, 44, 70))                    # assento
    rect(img, cx - 40, hz - 18, 80, 2, (150, 120, 70))
    for x in range(cx - 16, cx + 17):                                    # coroa rachada
        for y in range(18, 34):
            if y > 25 or (x - cx) % 8 in (0, 1, 2) and y > 18 + abs((x - cx) % 8 - 1):
                put(img, x, y, (230, 190, 80))
    for i in range(12):                                                  # rachadura brilhando
        put(img, cx + (i % 3) - 1, 18 + i, (170, 240, 250))
        put(img, cx + (i % 3), 18 + i, (240, 255, 255))
    for r in range(18, 3, -1):                                           # brilho em volta da coroa
        for a in range(0, 360, 6):
            x = int(cx + math.cos(math.radians(a)) * r * 1.6)
            y = int(26 + math.sin(math.radians(a)) * r)
            if 0 <= x < W and 0 <= y < hz:
                c = img.getpixel((x, y))
                put(img, x, y, mix(c[:3], (150, 220, 240), 0.06))
    for x0 in (40, 104, 296, 360):                                       # velas nas colunas
        rect(img, x0, hz - 30, 4, 10, (236, 226, 200))
        ellipse(img, x0 + 2, hz - 33, 2, 3, (255, 200, 90))
        put(img, x0 + 2, hz - 34, (255, 250, 220))
    return img


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    battle_bg_throne().save(OUT / "bg_trono.png")
    battle_bg_forest().save(OUT / "bg_bosque.png")
    battle_bg().save(OUT / "bg_praia.png")
    for kind in ("minas", "pantano", "ossorio", "picos", "deserto", "castelo"):
        battle_bg_region(kind).save(OUT / f"bg_{kind}.png")
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
