#!/usr/bin/env python3
"""Mapas do Ato 1 (docs/roteiro/02_bosque.md): Rota 1 (3 caminhos), Túnel das
Raízes, Raizal, Bosque Velho e interiores. Também liga a Vila Maré à Rota 1."""
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class Grid:
    def __init__(self, w, h, base):
        self.w, self.h = w, h
        self.g = [[base] * w for _ in range(h)]

    def fill(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if 0 <= x < self.w and 0 <= y < self.h:
                    self.g[y][x] = c

    def at(self, x, y):
        return self.g[y][x]

    def rows(self):
        return ["".join(r) for r in self.g]


def scatter_trees(grid, props, area, n, seed, avoid=()):
    r = random.Random(seed)
    x0, y0, x1, y1 = area
    placed = 0
    tries = 0
    taken = set()
    while placed < n and tries < 2000:
        tries += 1
        x, y = r.randint(x0, x1), r.randint(y0, y1)
        if grid.at(x, y) not in "gf" or grid.at(x - 1, y) not in "gf":
            continue
        if any(abs(x - ax) <= 2 and abs(y - ay) <= 2 for ax, ay in list(taken) + list(avoid)):
            continue
        taken.add((x, y))
        props.append({"type": r.choice(["tree_oak", "tree_oak2", "tree_pine"]), "x": x, "y": y})
        placed += 1


LEG_OUT = {"g": "grass", "f": "flowers", "B": "bush", "p": "path", "~": "water", ".": "sand"}

# ------------------------------------------------------------------ Rota 1
W, H = 40, 50
r1 = Grid(W, H, "B")
r1.fill(2, 36, 37, 48, "g")           # zona sul
r1.fill(19, 36, 20, 49, "p")          # estrada que vem da vila
# corredor central: só a estrada (2 células), fechada pelas raízes nas duas pontas
r1.fill(19, 14, 20, 35, "p")
r1.fill(3, 39, 18, 41, "g"); r1.fill(3, 40, 18, 40, "p")      # caminho dos domadores
r1.fill(2, 9, 8, 41, "g"); r1.fill(4, 10, 5, 40, "p")
r1.fill(4, 9, 18, 12, "g"); r1.fill(4, 10, 18, 11, "p")
r1.fill(21, 39, 35, 41, "g"); r1.fill(21, 40, 34, 40, "p")    # caminho selvagem (campo de flores)
r1.fill(25, 9, 38, 39, "f")
r1.fill(33, 10, 34, 40, "p")
r1.fill(21, 9, 34, 12, "g"); r1.fill(21, 10, 34, 11, "p")
for (x, y) in [(27, 15), (29, 22), (36, 30), (28, 33), (37, 18), (26, 27)]:
    r1.fill(x, y, x + 1, y + 1, "g")
r1.fill(2, 2, 37, 13, "g")            # zona norte
r1.fill(19, 0, 20, 13, "p")
r1.fill(22, 36, 26, 38, "g")          # boca sul do túnel
r1.fill(22, 12, 27, 14, "g")          # boca norte do túnel
p1 = [
    {"type": "root_wall", "x": 20, "y": 35, "if_not": "ramalho_beaten", "dialog": "bosque/raizes"},
    {"type": "root_wall", "x": 20, "y": 15, "if_not": "ramalho_beaten", "dialog": "bosque/raizes"},
    {"type": "root_arch", "x": 24, "y": 37},
    {"type": "root_arch", "x": 24, "y": 12},
    {"type": "sign", "x": 18, "y": 42, "dialog": "bosque/placa_bifurcacao"},
    {"type": "stump", "x": 23, "y": 43}, {"type": "log", "x": 10, "y": 44},
    {"type": "mushrooms", "x": 7, "y": 27}, {"type": "mushrooms", "x": 30, "y": 6},
]
scatter_trees(r1, p1, (3, 43, 36, 47), 9, 1, avoid=[(19, 44), (20, 44), (22, 42)])
scatter_trees(r1, p1, (3, 2, 36, 8), 10, 2, avoid=[(19, 4), (20, 4), (26, 13), (10, 6)])
scatter_trees(r1, p1, (2, 12, 8, 38), 6, 3, avoid=[(6, 30), (3, 20)])
npc1 = [
    {"id": "lenhador_velho", "x": 22, "y": 42, "facing": "left"},
    {"id": "rufo", "x": 6, "y": 30, "facing": "left"},
    {"id": "iris", "x": 3, "y": 20, "facing": "right"},
    {"id": "cipo", "x": 12, "y": 9, "facing": "down"},
    {"id": "rival_lia_b", "x": 26, "y": 13, "facing": "left", "if": "partner_taro", "if_none": ["partner_lia", "rival_bosque_done"]},
    {"id": "rival_taro_b", "x": 26, "y": 13, "facing": "left", "if": "partner_lia", "if_none": ["partner_taro", "rival_bosque_done"]},
]
rota_1 = {"id": "rota_1", "region": "bosque", "name_key": "MAP_ROTA_1", "tileset": "overworld", "legend": LEG_OUT,
          "ground": r1.rows(), "spawn": {"x": 19, "y": 47, "facing": "up"}, "props": p1, "npcs": npc1,
          "warps": [{"x": 19, "y": 49, "to": "vila_mare", "tx": 19, "ty": 1, "facing": "down", "sfx": ""},
                    {"x": 20, "y": 49, "to": "vila_mare", "tx": 20, "ty": 1, "facing": "down", "sfx": ""},
                    {"x": 19, "y": 0, "to": "raizal", "tx": 19, "ty": 30, "facing": "up", "sfx": ""},
                    {"x": 20, "y": 0, "to": "raizal", "tx": 20, "ty": 30, "facing": "up", "sfx": ""},
                    {"x": 24, "y": 37, "to": "tunel_raizes", "tx": 3, "ty": 12, "facing": "up", "sfx": "door"},
                    {"x": 24, "y": 12, "to": "tunel_raizes", "tx": 27, "ty": 1, "facing": "down", "sfx": "door"}],
          "spawns": [{"id": "r1_sul", "table": "rota1_sul", "x": 10, "y": 45, "radius": 3, "count": 2},
                     {"id": "r1_oeste", "table": "rota1_oeste", "x": 5, "y": 25, "radius": 2, "count": 1},
                     {"id": "r1_campo_a", "table": "rota1_campo", "x": 30, "y": 32, "radius": 4, "count": 3},
                     {"id": "r1_campo_b", "table": "rota1_campo", "x": 30, "y": 18, "radius": 4, "count": 3},
                     {"id": "r1_norte", "table": "rota1_norte", "x": 10, "y": 6, "radius": 3, "count": 2}],
          "ambient": ["leaves"]}

# ------------------------------------------------------------------ Túnel das Raízes
tw, th = 32, 14
tu = Grid(tw, th, "B")
tu.fill(3, 9, 4, 13, "p"); tu.fill(3, 9, 20, 10, "p"); tu.fill(19, 4, 20, 10, "p")
tu.fill(19, 4, 28, 5, "p"); tu.fill(27, 0, 28, 5, "p")
tu.fill(10, 8, 14, 11, "p")  # salão do selvagem forte
tunel = {"id": "tunel_raizes", "region": "bosque", "name_key": "MAP_TUNEL", "tileset": "overworld", "legend": LEG_OUT,
         "ground": tu.rows(), "tint": [0.42, 0.42, 0.58], "spawn": {"x": 3, "y": 12, "facing": "up"},
         "props": [{"type": "glow_shroom", "x": x, "y": y} for (x, y) in [(5, 9), (9, 10), (15, 9), (20, 7), (22, 4), (26, 5), (28, 2), (12, 11)]],
         "npcs": [{"id": "lia_tunel", "x": 4, "y": 11, "facing": "up", "if": "partner_taro", "if_none": ["partner_lia", "tunel_visto"]}],
         "warps": [{"x": 3, "y": 13, "to": "rota_1", "tx": 24, "ty": 38, "facing": "down", "sfx": "door"},
                   {"x": 4, "y": 13, "to": "rota_1", "tx": 24, "ty": 38, "facing": "down", "sfx": "door"},
                   {"x": 27, "y": 0, "to": "rota_1", "tx": 24, "ty": 13, "facing": "down", "sfx": "door"},
                   {"x": 28, "y": 0, "to": "rota_1", "tx": 24, "ty": 13, "facing": "down", "sfx": "door"}],
         "spawns": [{"id": "tunel", "table": "tunel", "x": 12, "y": 9, "radius": 1, "count": 1}],
         "on_enter": [{"if": "partner_lia", "if_not": "tunel_visto", "dialog": "bosque/tunel_lia"},
                      {"if": "partner_taro", "if_none": ["partner_lia", "tunel_visto"], "dialog": "bosque/tunel_taro"}]}

# ------------------------------------------------------------------ Raizal
RW, RH = 40, 32
rz = Grid(RW, RH, "g")
rz.fill(0, 0, RW - 1, 0, "B"); rz.fill(0, 0, 0, RH - 1, "B"); rz.fill(RW - 1, 0, RW - 1, RH - 1, "B"); rz.fill(0, RH - 1, RW - 1, RH - 1, "B")
rz.fill(19, 0, 20, RH - 1, "p")
rz.fill(12, 1, 27, 6, "f"); rz.fill(14, 2, 25, 5, "g")      # Clareira do Machado
rz.fill(14, 12, 25, 18, "p"); rz.fill(9, 11, 30, 11, "p"); rz.fill(6, 21, 33, 21, "p")
rz.fill(9, 11, 9, 21, "p"); rz.fill(30, 11, 30, 21, "p")
rz.fill(0, 15, 14, 16, "p")                                  # trilha do Bosque Velho
rz.fill(14, 21, 14, 27, "p")
pr = [{"type": "log_cabin_ranch", "x": 12, "y": 10}, {"type": "log_cabin_shop", "x": 27, "y": 10},
      {"type": "log_cabin", "x": 8, "y": 20}, {"type": "log_cabin_b", "x": 31, "y": 20}, {"type": "log_cabin", "x": 14, "y": 27},
      {"type": "sign", "x": 18, "y": 28, "dialog": "bosque/placa_raizal"}, {"type": "sign", "x": 18, "y": 7, "dialog": "bosque/placa_clareira"},
      {"type": "stall", "x": 23, "y": 17}, {"type": "lamp_post", "x": 13, "y": 13}, {"type": "lamp_post", "x": 26, "y": 13},
      {"type": "log", "x": 24, "y": 3}, {"type": "stump", "x": 15, "y": 3}, {"type": "stump", "x": 23, "y": 5},
      {"type": "mushrooms", "x": 5, "y": 26}, {"type": "flower_box", "x": 10, "y": 11}]
scatter_trees(rz, pr, (2, 1, 11, 9), 5, 4)
scatter_trees(rz, pr, (28, 1, 37, 9), 5, 5)
scatter_trees(rz, pr, (2, 23, 11, 29), 3, 6, avoid=[(8, 20)])
scatter_trees(rz, pr, (25, 23, 37, 29), 4, 7, avoid=[(31, 20)])
raizal = {"id": "raizal", "region": "bosque", "name_key": "MAP_RAIZAL", "tileset": "overworld", "legend": LEG_OUT,
          "ground": rz.rows(), "spawn": {"x": 19, "y": 29, "facing": "up"}, "props": pr,
          "npcs": [{"id": "graveto", "x": 17, "y": 16, "facing": "right"}, {"id": "hera", "x": 23, "y": 13, "facing": "down"},
                   {"id": "guarda_raiz", "x": 21, "y": 8, "facing": "left", "if_not": "ramalho_beaten"},
                   {"id": "ramalho", "x": 19, "y": 3, "facing": "down", "if_not": "ramalho_beaten"},
                   {"id": "ramalho_depois", "x": 22, "y": 3, "facing": "left", "if": "ramalho_beaten"}],
          "warps": [{"x": 12, "y": 10, "to": "raizal_rancho", "tx": 6, "ty": 8, "facing": "up", "sfx": "door"},
                    {"x": 27, "y": 10, "to": "raizal_loja", "tx": 6, "ty": 8, "facing": "up", "sfx": "door"},
                    {"x": 8, "y": 20, "to": "raizal_casa_galho", "tx": 6, "ty": 8, "facing": "up", "sfx": "door"},
                    {"x": 31, "y": 20, "to": "raizal_casa_musgo", "tx": 6, "ty": 8, "facing": "up", "sfx": "door"},
                    {"x": 14, "y": 27, "to": "raizal_casa_salvia", "tx": 6, "ty": 8, "facing": "up", "sfx": "door"},
                    {"x": 19, "y": RH - 1, "to": "rota_1", "tx": 19, "ty": 1, "facing": "down", "sfx": ""},
                    {"x": 20, "y": RH - 1, "to": "rota_1", "tx": 20, "ty": 1, "facing": "down", "sfx": ""},
                    {"x": 0, "y": 15, "to": "bosque_velho", "tx": 22, "ty": 8, "facing": "left", "sfx": ""},
                    {"x": 0, "y": 16, "to": "bosque_velho", "tx": 22, "ty": 9, "facing": "left", "sfx": ""},
                    {"x": 19, "y": 0, "to": "rota_2", "tx": -1, "ty": -1, "facing": "up", "sfx": "", "locked_message": "MSG_ROUTE2_LOCKED"},
                    {"x": 20, "y": 0, "to": "rota_2", "tx": -1, "ty": -1, "facing": "up", "sfx": "", "locked_message": "MSG_ROUTE2_LOCKED"}],
          "ambient": ["leaves"]}

# ------------------------------------------------------------------ Bosque Velho
bw, bh = 24, 18
bv = Grid(bw, bh, "B")
bv.fill(2, 2, 22, 15, "g"); bv.fill(4, 3, 20, 13, "f"); bv.fill(6, 5, 18, 12, "g")
bv.fill(12, 8, 23, 9, "p")
pb = [{"type": "raizerno_tree", "x": 11, "y": 6, "dialog": "bosque/raizerno"},
      {"type": "herb_blue", "x": 16, "y": 11, "dialog": "bosque/erva", "if": "salvia_quest", "if_not": "salvia_herb"},
      {"type": "mushrooms", "x": 7, "y": 11}, {"type": "mushrooms", "x": 17, "y": 5}, {"type": "glow_shroom", "x": 5, "y": 7}]
scatter_trees(bv, pb, (3, 2, 21, 14), 7, 8, avoid=[(11, 6), (12, 6), (10, 6), (16, 11), (14, 8), (15, 9)])
bosque_velho = {"id": "bosque_velho", "region": "bosque", "name_key": "MAP_BOSQUE_VELHO", "tileset": "overworld", "legend": LEG_OUT,
                "ground": bv.rows(), "tint": [0.82, 0.92, 0.85], "spawn": {"x": 21, "y": 8, "facing": "left"}, "props": pb, "npcs": [],
                "warps": [{"x": 23, "y": 8, "to": "raizal", "tx": 1, "ty": 15, "facing": "right", "sfx": ""},
                          {"x": 23, "y": 9, "to": "raizal", "tx": 1, "ty": 16, "facing": "right", "sfx": ""}],
                "ambient": ["leaves"]}


def room(mid, name_key, back, props, npcs):
    rows = ["TTTTTTTTTTTT", "TwwnwwwwwnwT"] + ["T..........T"] * 7 + ["TTTTTTmTTTTT"]
    return {"id": mid, "region": "bosque", "name_key": name_key, "tileset": "overworld",
            "legend": {"T": "wall_top", "w": "wall", "n": "wall_window", ".": "floor", "m": "mat"},
            "ground": rows, "spawn": {"x": 6, "y": 8, "facing": "up"}, "props": props, "npcs": npcs,
            "warps": [{"x": 6, "y": 9, "to": "raizal", "tx": back[0], "ty": back[1] + 1, "facing": "down", "sfx": "door"}]}


maps = {
    "rota_1": rota_1, "tunel_raizes": tunel, "raizal": raizal, "bosque_velho": bosque_velho,
    "raizal_rancho": room("raizal_rancho", "MAP_RAIZAL_RANCHO", (12, 10),
                          [{"type": "bed", "x": 2, "y": 3}, {"type": "bed", "x": 4, "y": 3}, {"type": "plant", "x": 10, "y": 2},
                           {"type": "rug", "x": 6, "y": 6}, {"type": "lamp", "x": 1, "y": 7}], [{"id": "tilia", "x": 7, "y": 3, "facing": "down"}]),
    "raizal_loja": room("raizal_loja", "MAP_RAIZAL_LOJA", (27, 10),
                        [{"type": "shelf", "x": 3, "y": 2}, {"type": "shelf", "x": 10, "y": 2}, {"type": "table", "x": 7, "y": 4},
                         {"type": "crate", "x": 10, "y": 7}, {"type": "barrel", "x": 1, "y": 7}], [{"id": "toco", "x": 6, "y": 3, "facing": "down"}]),
    "raizal_casa_galho": room("raizal_casa_galho", "MAP_RAIZAL_CASA_GALHO", (8, 20),
                              [{"type": "table", "x": 7, "y": 5}, {"type": "stump", "x": 3, "y": 6}, {"type": "log", "x": 9, "y": 2}],
                              [{"id": "irmao_galho", "x": 6, "y": 3, "facing": "down"}]),
    "raizal_casa_musgo": room("raizal_casa_musgo", "MAP_RAIZAL_CASA_MUSGO", (31, 20),
                              [{"type": "table", "x": 7, "y": 4}, {"type": "plant", "x": 1, "y": 2}, {"type": "mushrooms", "x": 9, "y": 7}],
                              [{"id": "pai_musgo", "x": 5, "y": 3, "facing": "down"}]),
    "raizal_casa_salvia": room("raizal_casa_salvia", "MAP_RAIZAL_CASA_SALVIA", (14, 27),
                               [{"type": "shelf", "x": 3, "y": 2}, {"type": "plant", "x": 10, "y": 2}, {"type": "plant", "x": 1, "y": 7},
                                {"type": "table", "x": 7, "y": 5}], [{"id": "salvia", "x": 6, "y": 3, "facing": "down"}]),
}
for mid, m in maps.items():
    for r in m["ground"]:
        assert len(r) == len(m["ground"][0]), mid
    (ROOT / "data/maps" / f"{mid}.json").write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

# Vila Maré: a estrada norte agora leva à Rota 1
v = json.loads((ROOT / "data/maps/vila_mare.json").read_text())
v["warps"] = [w for w in v["warps"] if w["to"] != "rota_1"]
v["warps"] += [{"x": 19, "y": 0, "to": "rota_1", "tx": 19, "ty": 48, "facing": "up", "sfx": ""},
               {"x": 20, "y": 0, "to": "rota_1", "tx": 20, "ty": 48, "facing": "up", "sfx": ""}]
(ROOT / "data/maps/vila_mare.json").write_text(json.dumps(v, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("mapas:", ", ".join(maps))
