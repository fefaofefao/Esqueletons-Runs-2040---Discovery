#!/usr/bin/env python3
"""Gera o tileset do mundo (assets/tiles/overworld.png) e sua descrição
(data/tilesets/overworld.json).

Terrenos são tiles 16x16 (alguns animados). As transições entre terrenos
(espuma, areia molhada, franja de grama, água funda) são "overlays" de 47
variações (máscara de 8 vizinhos canônica), gerados aqui a partir dos
próprios tiles de terreno. Tudo é procedural e original.
"""
import json
import math
from pathlib import Path

from draw import new, put, rect, hash01, mix, bayer, rgba

ROOT = Path(__file__).resolve().parents[2]
T = 16
COLS = 16

N, E, S, W, NE, SE, SW, NW = 1, 2, 4, 8, 16, 32, 64, 128

# ---------------------------------------------------------------- paletas
SAND = (236, 212, 160)
SAND_L = (247, 230, 188)
SAND_D = (216, 186, 132)
SAND_DD = (196, 164, 112)
WET = (204, 172, 120)
WET_D = (186, 152, 104)
WATER = (76, 186, 206)
WATER_L = (138, 222, 226)
WATER_D = (58, 160, 192)
DEEP = (44, 124, 186)
DEEP_L = (84, 160, 214)
DEEP_D = (34, 100, 164)
FOAM = (244, 252, 250)
FOAM_2 = (204, 238, 242)
GRASS = (104, 180, 76)
GRASS_L = (146, 206, 94)
GRASS_D = (72, 146, 62)
GRASS_DD = (52, 116, 56)
BUSH = (52, 128, 70)
BUSH_L = (84, 164, 84)
BUSH_LL = (128, 196, 100)
BUSH_D = (34, 92, 60)
DIRT = (206, 172, 122)
DIRT_L = (222, 192, 144)
DIRT_D = (178, 142, 96)
WOOD = (170, 116, 70)
WOOD_L = (196, 144, 90)
WOOD_D = (128, 84, 50)
WOOD_DD = (86, 56, 38)
WALL = (156, 108, 68)
WALL_L = (182, 132, 84)
WALL_D = (116, 78, 50)


# ---------------------------------------------------------------- terrenos
def tile_sand(variant):
    img = new(T, T)
    for y in range(T):
        for x in range(T):
            h = hash01(x, y, 11 + variant)
            c = SAND
            if h > 0.93:
                c = SAND_L
            elif h < 0.07:
                c = SAND_D
            put(img, x, y, c)
    if variant == 1:  # ondulações do vento
        for (x0, y0) in [(2, 4), (8, 10), (11, 3)]:
            for i in range(4):
                put(img, (x0 + i) % T, y0 + (i // 2), SAND_D)
                put(img, (x0 + i) % T, y0 + (i // 2) - 1, SAND_L)
    elif variant == 2:  # concha pequena
        for (dx, dy, c) in [(0, 0, (250, 222, 214)), (1, 0, (240, 196, 190)), (2, 0, (250, 222, 214)),
                            (0, 1, (226, 170, 164)), (1, 1, (250, 236, 230)), (2, 1, (226, 170, 164)),
                            (1, 2, (200, 150, 140))]:
            put(img, 9 + dx, 6 + dy, c)
        put(img, 10, 9, SAND_DD)
    elif variant == 3:  # pedrinhas
        for (x, y) in [(3, 11), (4, 11), (12, 5), (7, 2)]:
            put(img, x, y, (170, 160, 150))
            put(img, x, y + 1, (130, 120, 112))
    return [img]


def water_frames(base, light, dark, seed, count, highlight_len):
    frames = []
    spots = []
    for i in range(count):
        spots.append((int(hash01(i, 1, seed) * 16), int(hash01(i, 2, seed) * 16)))
    for f in range(4):
        img = new(T, T)
        for y in range(T):
            for x in range(T):
                # ondulação suave em faixas diagonais que se deslocam
                wv = math.sin((x + y * 2 + f * 4) * math.pi / 8)
                c = base
                if wv > 0.85 and bayer(x, y) > 0.5:
                    c = mix(base, light, 0.35)
                elif wv < -0.9 and bayer(x, y) > 0.6:
                    c = dark
                put(img, x, y, c)
        for i, (sx, sy) in enumerate(spots):
            ph = (f + i) % 4
            ln = highlight_len if ph in (1, 2) else highlight_len - 1
            if ph == 3:
                continue
            ox = (sx + f) % T
            for k in range(ln):
                put(img, (ox + k) % T, sy, light)
            put(img, (ox + 1) % T, (sy + 1) % T, mix(base, dark, 0.5))
        frames.append(img)
    return frames


def tile_water():
    return water_frames(WATER, WATER_L, WATER_D, 3, 3, 3)


def tile_deep():
    return water_frames(DEEP, DEEP_L, DEEP_D, 7, 2, 2)


def tile_grass(variant, flowers=False):
    frames = []
    blades = []
    for i in range(9):
        blades.append((int(hash01(i, 3, variant + 40) * 15), int(hash01(i, 4, variant + 40) * 14) + 1))
    for f in range(2):
        img = new(T, T)
        for y in range(T):
            for x in range(T):
                h = hash01(x, y, 70 + variant)
                c = GRASS
                if h > 0.9:
                    c = GRASS_L
                elif h < 0.08:
                    c = GRASS_D
                put(img, x, y, c)
        for i, (bx, by) in enumerate(blades):
            lean = (f + i) % 2
            put(img, bx, by, GRASS_D)
            put(img, bx + lean, by - 1, GRASS_L)
            put(img, bx + 1, by, GRASS_D)
        if flowers:
            for i, (fx, fy, col) in enumerate([(3, 4, (250, 240, 120)), (11, 9, (250, 150, 170)), (6, 12, (250, 250, 250))]):
                ox = fx + (1 if (f + i) % 2 else 0)
                put(img, ox, fy, col)
                put(img, ox - 1, fy, mix(col, (255, 255, 255), 0.3))
                put(img, ox + 1, fy, mix(col, (255, 255, 255), 0.3))
                put(img, ox, fy - 1, mix(col, (255, 255, 255), 0.3))
                put(img, ox, fy + 1, GRASS_DD)
        frames.append(img)
    return frames


def tile_bush(variant):
    img = new(T, T)
    rect(img, 0, 0, T, T, BUSH_D)
    blobs = []
    for i in range(7):
        blobs.append((hash01(i, 5, variant + 90) * 16, hash01(i, 6, variant + 90) * 16, 3 + hash01(i, 7, variant) * 2))
    for y in range(T):
        for x in range(T):
            best = None
            for (bx, by, r) in blobs:
                for ox in (-16, 0, 16):
                    for oy in (-16, 0, 16):
                        d = math.hypot(x + 0.5 - (bx + ox), y + 0.5 - (by + oy))
                        if d <= r:
                            t = (x + 0.5 - (bx + ox)) * -0.6 + (y + 0.5 - (by + oy)) * -0.8
                            v = t / r
                            if best is None or v > best:
                                best = v
            if best is None:
                continue
            c = BUSH
            if best > 0.45:
                c = BUSH_LL if best > 0.75 else BUSH_L
            elif best < -0.55:
                c = BUSH_D
            put(img, x, y, c)
    return [img]


def tile_path(variant):
    img = new(T, T)
    for y in range(T):
        for x in range(T):
            h = hash01(x, y, 120 + variant)
            c = DIRT
            if h > 0.9:
                c = DIRT_L
            elif h < 0.1:
                c = DIRT_D
            put(img, x, y, c)
    for (x, y) in ([(4, 5), (11, 12)] if variant == 0 else [(7, 3), (2, 10), (12, 7)]):
        put(img, x, y, (150, 140, 128))
        put(img, x + 1, y, (176, 166, 152))
        put(img, x, y + 1, (120, 110, 100))
    return [img]


def tile_dock():
    img = new(T, T)
    for y in range(T):
        band = y // 4
        for x in range(T):
            c = WOOD if band % 2 == 0 else mix(WOOD, WOOD_L, 0.4)
            if y % 4 == 3:
                c = WOOD_DD
            elif y % 4 == 0:
                c = WOOD_L
            if hash01(x, y, 200) > 0.93 and y % 4 in (1, 2):
                c = WOOD_D
            put(img, x, y, c)
    for y in (1, 5, 9, 13):
        put(img, 2, y, (210, 200, 180))
        put(img, 13, y, (210, 200, 180))
    return [img]


def tile_floor(variant):
    img = new(T, T)
    for x in range(T):
        board = x // 4
        for y in range(T):
            c = mix(WOOD, WOOD_L, 0.25 if (board + variant) % 2 else 0.0)
            if x % 4 == 3:
                c = WOOD_D
            if hash01(x, y, 300 + variant) > 0.94:
                c = WOOD_D
            put(img, x, y, c)
    seam = 6 if variant == 0 else 11
    for x in range(T):
        if x // 4 % 2 == 0:
            put(img, x, seam, WOOD_D)
    return [img]


def tile_wall(kind):
    img = new(T, T)
    if kind == "top":
        for y in range(T):
            for x in range(T):
                c = (70, 48, 36) if y < 13 else (96, 66, 46)
                if y == 13:
                    c = (120, 84, 58)
                if hash01(x, y, 400) > 0.95 and y < 12:
                    c = (82, 58, 42)
                put(img, x, y, c)
        return [img]
    for x in range(T):
        for y in range(T):
            board = x // 5
            c = mix(WALL, WALL_L, 0.3 if board % 2 else 0.0)
            if x % 5 == 4:
                c = WALL_D
            if y >= 14:
                c = (96, 64, 44)
            elif y == 0:
                c = WALL_L
            put(img, x, y, c)
    if kind == "window":
        rect(img, 3, 3, 10, 8, (60, 40, 32))
        for y in range(4, 10):
            for x in range(4, 12):
                sky = mix((140, 208, 240), (210, 240, 250), (y - 4) / 6.0)
                put(img, x, y, sky)
        rect(img, 7, 4, 2, 6, (90, 60, 42))
        rect(img, 4, 6, 8, 1, (90, 60, 42))
        put(img, 5, 4, (250, 250, 255))
        rect(img, 3, 11, 10, 1, WALL_L)
    return [img]


def tile_void():
    img = new(T, T)
    rect(img, 0, 0, T, T, (16, 12, 20))
    return [img]


def tile_mat():
    img = new(T, T)
    for y in range(T):
        for x in range(T):
            c = (176, 80, 60) if (x // 2 + y // 2) % 2 else (200, 120, 70)
            if x in (0, 15) or y in (0, 15):
                c = (120, 56, 44)
            put(img, x, y, c)
    return [img]


# ---------------------------------------------------------------- overlays
def canonical(mask):
    m = mask & 15
    for bit, a, b in ((NE, N, E), (SE, S, E), (SW, S, W), (NW, N, W)):
        if mask & bit and not (mask & a) and not (mask & b):
            m |= bit
    return m


ALL_MASKS = sorted({canonical(m) for m in range(256)} - {0})


def edge_distance(x, y, mask):
    px, py = x + 0.5, y + 0.5
    ds = []
    if mask & N:
        ds.append(py)
    if mask & S:
        ds.append(T - py)
    if mask & W:
        ds.append(px)
    if mask & E:
        ds.append(T - px)
    corners = {NE: (T, 0), SE: (T, T), SW: (0, T), NW: (0, 0)}
    for bit, (cx, cy) in corners.items():
        if mask & bit:
            ds.append(math.hypot(px - cx, py - cy))
    return min(ds) if ds else 99.0


def along(x, y, mask):
    """Coordenada ao longo da borda mais próxima (para variar o recorte)."""
    px, py = x + 0.5, y + 0.5
    best = None
    for bit, d, a in ((N, py, x), (S, T - py, x), (W, px, y), (E, T - px, y)):
        if mask & bit and (best is None or d < best[0]):
            best = (d, a)
    return best[1] if best else x + y


def overlay_foam(mask, frame):
    img = new(T, T)
    for y in range(T):
        for x in range(T):
            d = edge_distance(x, y, mask)
            a = along(x, y, mask)
            band = 1.6 + 0.9 * math.sin(2 * math.pi * (frame / 4.0) + a * math.pi / 4)
            if d < band:
                put(img, x, y, FOAM if d < band - 0.8 else FOAM_2)
            elif d < band + 1.2 and bayer(x, y) > 0.45:
                put(img, x, y, WATER_L)
            # segunda linha de espuma, a onda que volta
            wave = 4.2 + (frame % 4) * 0.7
            if abs(d - wave) < 0.5 and hash01(int(a), frame, 9) > 0.35 and frame != 3:
                put(img, x, y, FOAM_2)
    return img


def overlay_wet(mask):
    img = new(T, T)
    for y in range(T):
        for x in range(T):
            d = edge_distance(x, y, mask)
            if d < 2.2:
                put(img, x, y, WET_D if d < 1.0 else WET)
            elif d < 4.5 and bayer(x, y) > (d - 2.2) / 2.3:
                put(img, x, y, WET)
    return img


def overlay_grass(mask):
    img = new(T, T)
    for y in range(T):
        for x in range(T):
            d = edge_distance(x, y, mask)
            a = int(along(x, y, mask)) % T
            reach = 1.5 + hash01(a, 0, 55) * 2.5
            if d < reach - 1:
                put(img, x, y, GRASS if hash01(x, y, 56) > 0.15 else GRASS_L)
            elif d < reach:
                put(img, x, y, GRASS_D)
            elif d < reach + 1 and hash01(a, 1, 57) > 0.7:
                put(img, x, y, GRASS_DD)
    return img


def overlay_path(mask, path_tile):
    img = new(T, T)
    for y in range(T):
        for x in range(T):
            d = edge_distance(x, y, mask)
            if d < 1.2 or (d < 3.5 and bayer(x, y) > (d - 1.2) / 2.3):
                img.putpixel((x, y), path_tile.getpixel((x, y)))
    return img


def overlay_deep(mask, water_frame):
    img = new(T, T)
    for y in range(T):
        for x in range(T):
            d = edge_distance(x, y, mask)
            if d < 2 or (d < 5 and bayer(x, y) > (d - 2) / 3.0):
                img.putpixel((x, y), water_frame.getpixel((x, y)))
    return img


# ---------------------------------------------------------------- atlas
class Atlas:
    def __init__(self):
        self.entries = []  # (frames)
        self.col = 0
        self.row = 0
        self.placed = []

    def add(self, frames):
        n = len(frames)
        if self.col + n > COLS:
            self.col = 0
            self.row += 1
        pos = (self.col, self.row)
        self.placed.append((pos, frames))
        self.col += n
        return [pos[0], pos[1]]

    def image(self):
        rows = self.row + 1
        img = new(COLS * T, rows * T)
        for (c, r), frames in self.placed:
            for i, fr in enumerate(frames):
                img.alpha_composite(fr, ((c + i) * T, r * T))
        return img


# ---------------------------------------------------------------- terrenos das regiões (fase 4c+)
def tile_noise(base, light, dark, seed, specks=(), ripples=None):
    """Chão com ruído (cinza, lama, neve, duna, calçamento...)."""
    img = new(T, T)
    for y in range(T):
        for x in range(T):
            h = hash01(x, y, seed)
            c = base
            if h > 0.88:
                c = light
            elif h < 0.1:
                c = dark
            if ripples and (y + int(2 * math.sin((x + seed) / 3))) % ripples == 0:
                c = dark
            put(img, x, y, c)
    for i, col in enumerate(specks):
        x, y = int(hash01(i, 1, seed) * 14) + 1, int(hash01(i, 2, seed) * 14) + 1
        put(img, x, y, col)
        put(img, x + 1, y, mix(col, base, 0.5))
    return [img]


def tile_cobble(base, light, dark, seed):
    img = new(T, T)
    rect(img, 0, 0, T, T, dark)
    for (x0, y0, w, h) in [(0, 0, 7, 5), (8, 0, 8, 5), (0, 6, 4, 4), (5, 6, 6, 4), (12, 6, 4, 4), (0, 11, 8, 5), (9, 11, 7, 5)]:
        c = mix(base, light, hash01(x0, y0, seed) * 0.6)
        rect(img, x0, y0, w - 1, h - 1, c)
        rect(img, x0, y0, w - 1, 1, light)
    return [img]


def tile_blocks(base, light, dark, seed, snow=False):
    """Parede de blocos de pedra (sólida)."""
    img = new(T, T)
    rect(img, 0, 0, T, T, dark)
    for row in range(4):
        off = 4 if row % 2 else 0
        for col in range(-1, 3):
            x0 = col * 8 + off
            c = mix(base, light, hash01(col, row, seed) * 0.5)
            rect(img, max(0, x0), row * 4, min(7, 7 + x0) if x0 < 0 else 7, 3, c)
    if snow:
        rect(img, 0, 0, T, 3, (240, 246, 252))
        for x in range(0, T, 3):
            put(img, x, 3, (220, 232, 246))
    return [img]


def tile_murky(base, light, dark, seed):
    frames = []
    for f in range(4):
        img = new(T, T)
        for y in range(T):
            for x in range(T):
                v = math.sin((x + f * 2) * 0.7 + y * 0.4 + seed)
                c = base if v < 0.6 else light
                if hash01(x, y, seed + f) < 0.06:
                    c = dark
                put(img, x, y, c)
        frames.append(img)
    return frames


def tile_carpet():
    img = new(T, T)
    rect(img, 0, 0, T, T, (150, 40, 60))
    rect(img, 0, 0, 2, T, (214, 170, 70))
    rect(img, 14, 0, 2, T, (214, 170, 70))
    for y in range(2, T, 6):
        put(img, 8, y, (214, 170, 70))
        put(img, 7, y + 1, (214, 170, 70))
        put(img, 9, y + 1, (214, 170, 70))
    return [img]


def main():
    atlas = Atlas()
    terrains = {}

    def terrain(name, variant_frames, solid, fps=0.0, weights=None):
        variants = [atlas.add(fr) for fr in variant_frames]
        terrains[name] = {
            "solid": solid,
            "variants": variants,
            "weights": weights or [1] * len(variants),
            "frames": len(variant_frames[0]),
            "fps": fps,
        }

    terrain("sand", [tile_sand(i) for i in range(4)], False, weights=[10, 3, 1, 1])
    water = tile_water()
    terrain("water", [water], True, fps=3.0)
    terrain("deep", [tile_deep()], True, fps=2.5)
    terrain("grass", [tile_grass(0), tile_grass(1)], False, fps=1.5, weights=[3, 2])
    terrain("flowers", [tile_grass(2, flowers=True)], False, fps=1.5)
    terrain("path", [tile_path(0), tile_path(1)], False, weights=[3, 1])
    terrain("bush", [tile_bush(0), tile_bush(1)], True)
    terrain("dock", [tile_dock()], False)
    terrain("floor", [tile_floor(0), tile_floor(1)], False, weights=[3, 1])
    terrain("wall", [tile_wall("plain")], True)
    terrain("wall_window", [tile_wall("window")], True)
    terrain("wall_top", [tile_wall("top")], True)
    terrain("mat", [tile_mat()], False)
    terrain("void", [tile_void()], True)
    # regiões (fase 4c+)
    terrain("ash", [tile_noise((122, 116, 112), (150, 144, 138), (96, 90, 88), 300, [(200, 120, 60)]), tile_noise((118, 112, 108), (146, 140, 134), (92, 86, 84), 301)], False, weights=[3, 1])
    terrain("rock", [tile_blocks((92, 84, 82), (120, 112, 106), (52, 46, 48), 310), tile_blocks((88, 80, 80), (116, 108, 104), (50, 44, 46), 311)], True)
    terrain("mud", [tile_noise((104, 96, 64), (128, 120, 80), (78, 72, 48), 320, [(90, 140, 70)]), tile_noise((100, 92, 62), (124, 116, 78), (74, 68, 46), 321)], False, weights=[3, 1])
    terrain("swamp", [tile_murky((70, 104, 74), (98, 132, 88), (46, 70, 52), 330)], True, fps=2.0)
    terrain("stone", [tile_cobble((176, 170, 160), (204, 198, 186), (110, 104, 98), 340), tile_cobble((170, 164, 156), (198, 192, 182), (106, 100, 94), 341)], False, weights=[3, 1])
    terrain("city_wall", [tile_blocks((196, 186, 168), (226, 218, 200), (120, 112, 100), 350)], True)
    terrain("snow", [tile_noise((232, 240, 248), (250, 252, 255), (200, 214, 232), 360), tile_noise((228, 236, 246), (248, 250, 255), (196, 210, 230), 361, [(170, 190, 220)])], False, weights=[3, 1])
    terrain("ice", [tile_noise((176, 214, 238), (226, 244, 252), (140, 186, 220), 370, [(255, 255, 255), (255, 255, 255)])], False)
    terrain("snow_rock", [tile_blocks((120, 128, 144), (156, 164, 180), (70, 76, 92), 380, snow=True)], True)
    terrain("dune", [tile_noise((232, 196, 128), (246, 216, 150), (204, 166, 102), 390, ripples=6), tile_noise((228, 192, 124), (244, 212, 146), (200, 162, 98), 391, ripples=5)], False, weights=[2, 1])
    terrain("sandstone", [tile_blocks((198, 140, 88), (222, 170, 112), (130, 86, 54), 400)], True)
    terrain("castle_floor", [tile_cobble((150, 140, 160), (176, 166, 186), (96, 88, 108), 410)], False)
    terrain("castle_wall", [tile_blocks((70, 62, 88), (98, 88, 118), (36, 30, 48), 420)], True)
    terrain("carpet", [tile_carpet()], False)

    overlays = []

    def overlay(oid, on, near, make, frames, fps):
        masks = {}
        for m in ALL_MASKS:
            masks[str(m)] = atlas.add([make(m, f) for f in range(frames)])
        overlays.append({"id": oid, "on": on, "near": near, "frames": frames, "fps": fps, "masks": masks})

    path0 = tile_path(0)[0]
    overlay("path_edge", ["sand"], ["path"], lambda m, f: overlay_path(m, path0), 1, 0.0)
    overlay("wet", ["sand"], ["water", "deep"], lambda m, f: overlay_wet(m), 1, 0.0)
    overlay("grass_edge", ["sand", "path"], ["grass", "flowers", "bush"], lambda m, f: overlay_grass(m), 1, 0.0)
    overlay("deep_edge", ["deep"], ["water"], lambda m, f: overlay_deep(m, water[f]), 4, 2.5)
    overlay("foam", ["water"], ["sand", "grass", "path", "flowers", "bush"], lambda m, f: overlay_foam(m, f), 4, 3.0)

    out_png = ROOT / "assets" / "tiles" / "overworld.png"
    out_png.parent.mkdir(parents=True, exist_ok=True)
    atlas.image().save(out_png)
    desc = {
        "_comment": "Gerado por tools/art/gen_tiles.py. Não editar à mão.",
        "texture": "res://assets/tiles/overworld.png",
        "tile_size": T,
        "mask_bits": {"N": N, "E": E, "S": S, "W": W, "NE": NE, "SE": SE, "SW": SW, "NW": NW},
        "terrains": terrains,
        "overlays": overlays,
    }
    out_json = ROOT / "data" / "tilesets" / "overworld.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(desc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"tileset: {len(atlas.placed)} entradas, {len(ALL_MASKS)} máscaras -> {out_png}")


if __name__ == "__main__":
    main()
