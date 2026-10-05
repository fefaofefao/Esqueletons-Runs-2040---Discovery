#!/usr/bin/env python3
"""Refinamento dos mapas externos (pedido do Fernando: "o mapa tem que ser refinado").

Roda depois de todos os geradores (tools/maps/build_all.py chama no fim) e, para
cada mapa externo:
  1. quebra as bordas retas da mata/rocha com reentrâncias irregulares;
  2. espalha manchas de flores e detalhes da região (pedras, tocos, cogumelos,
     conchas, juncos, cactos...) nas áreas vazias.

Segurança: nada é colocado em trilhas (nem ao lado delas), perto de portas, NPCs,
objetos interativos, zonas de selvagens ou do ponto de chegada. Cada mudança que
bloqueia passagem só é aceita se todos os destinos que eram alcançáveis continuam
alcançáveis e nenhum bolsão de chão fica isolado. Determinístico (semente = id do
mapa) e marcado com "refined": true para não rodar duas vezes.

Uso: python3 tools/maps/refine.py [mapa ...]
"""
import json
import random
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TILES = json.loads((ROOT / "data/tilesets/overworld.json").read_text(encoding="utf-8"))["terrains"]
PROPS = json.loads((ROOT / "data/props.json").read_text(encoding="utf-8"))
PROPS = PROPS.get("props", PROPS)

WALLS = {"bush", "rock", "snow_rock", "sandstone"}          # bordas que ganham reentrâncias
OPEN = {"grass", "flowers", "sand", "ash", "mud", "snow", "dune"}  # chão natural que recebe detalhes
PATHS = {"path", "dock", "stone", "ice", "castle_floor", "carpet", "floor", "mat"}

# detalhes por região: (tipo de objeto, terrenos onde pode ir, peso)
DECOR = {
    "praia": [("starfish", {"sand"}, 3), ("driftwood", {"sand"}, 2), ("rock_small", {"sand", "grass"}, 2), ("plant", {"grass"}, 1)],
    "vila_mare": [("rock_small", {"grass"}, 2), ("plant", {"grass"}, 2), ("starfish", {"sand"}, 1), ("stump", {"grass"}, 1)],
    "bosque": [("mushrooms", {"grass", "flowers"}, 3), ("stump", {"grass"}, 2), ("rock_small", {"grass"}, 2), ("log", {"grass"}, 1),
               ("tree_pine", {"grass"}, 1), ("tree_oak2", {"grass"}, 1)],
    "minas": [("rock_small", {"ash"}, 4), ("rubble", {"ash"}, 2), ("dead_tree", {"ash"}, 1)],
    "pantano": [("reeds", {"mud", "grass"}, 3), ("mushrooms", {"mud", "grass"}, 2), ("glow_shroom", {"mud", "grass"}, 1), ("dead_tree", {"mud"}, 1)],
    "ossorio": [("rock_small", {"grass"}, 2), ("plant", {"grass"}, 2), ("broken_column", {"grass"}, 1), ("stump", {"grass"}, 1)],
    "picos": [("rock_small", {"snow"}, 3), ("snow_pine", {"snow"}, 2)],
    "deserto": [("cactus", {"dune", "sand"}, 3), ("rock_small", {"dune", "sand"}, 2), ("dead_tree", {"dune"}, 1)],
    "castelo": [("rubble", {"grass", "ash", "stone"}, 2), ("broken_column", {"grass", "ash"}, 1)],
}
FLOWER_REGIONS = {"praia", "vila_mare", "bosque", "ossorio"}
# copas sobre a mata (e pedras sobre a rocha): dão volume sem mudar a passagem
CANOPY = {
    "bush": {"bosque": ["tree_oak", "tree_oak2", "tree_pine", "tree_pine"], "vila_mare": ["tree_oak", "tree_oak2", "palm"],
             "praia": ["palm", "tree_oak2"], "ossorio": ["tree_oak", "tree_oak2", "tree_pine"], "pantano": ["willow", "dead_tree"],
             "castelo": ["dead_tree", "tree_pine"], "minas": ["dead_tree"], "picos": ["snow_pine"], "deserto": ["palm"]},
    "rock": {"minas": ["rock_big", "rock_small", "dead_tree"]},
    "snow_rock": {"picos": ["snow_pine", "snow_pine", "rock_big"]},
    "sandstone": {"deserto": ["rock_big", "cactus"]},
}


def solid_terrain(t):
    return bool(TILES.get(t, {}).get("solid", True))


class MapGrid:
    def __init__(self, m):
        self.m = m
        legend = m["legend"]
        self.rows = [list(r) for r in m["ground"]]
        self.h = len(self.rows)
        self.w = max(len(r) for r in self.rows)
        self.legend = legend
        self.char_of = {}
        for ch, t in legend.items():
            self.char_of.setdefault(t, ch)
        self.prop_cells = {}   # célula -> objeto (colisão)
        self.near_props = set()
        for p in m.get("props", []):
            info = PROPS.get(p["type"], {})
            cond = any(k in p for k in ("if", "if_not", "if_all", "if_any", "if_none"))
            for dx, dy in info.get("collision", []):
                c = (p["x"] + dx, p["y"] + dy)
                if not cond:
                    self.prop_cells[c] = p
                for ox in (-1, 0, 1):
                    for oy in (-1, 0, 1):
                        self.near_props.add((c[0] + ox, c[1] + oy))
            self.near_props.add((p["x"], p["y"]))

    def terrain(self, x, y):
        if 0 <= y < self.h and 0 <= x < len(self.rows[y]):
            return self.legend.get(self.rows[y][x], "void")
        return "void"

    def set_terrain(self, x, y, t):
        if t not in self.char_of:
            used = set(self.legend) | {c for r in self.rows for c in r}
            ch = next(c for c in "fFkKqQzZjJ0123456789" if c not in used)
            self.legend[ch] = t
            self.char_of[t] = ch
        self.rows[y][x] = self.char_of[t]

    def walkable(self, c):
        x, y = c
        return not solid_terrain(self.terrain(x, y)) and c not in self.prop_cells

    def reach(self, start):
        if not self.walkable(start):
            return set()
        seen = {start}
        q = deque([start])
        while q:
            x, y = q.popleft()
            for n in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if n not in seen and 0 <= n[0] < self.w and 0 <= n[1] < self.h and self.walkable(n):
                    seen.add(n)
                    q.append(n)
        return seen


def refine(m):
    if m.get("refined") or m.get("tileset", "overworld") != "overworld":
        return False
    g = MapGrid(m)
    cells = [(x, y) for y in range(g.h) for x in range(g.w)]
    open_cells = [c for c in cells if g.terrain(*c) in OPEN]
    if g.w * g.h < 300 or len(open_cells) < 0.2 * len(cells):
        return False  # interiores e salões
    region = m.get("region", "")
    rng = random.Random("refine:" + m["id"])

    # células protegidas
    prot = set(g.near_props)

    def protect(cx, cy, r):
        for ox in range(-r, r + 1):
            for oy in range(-r, r + 1):
                prot.add((cx + ox, cy + oy))

    for c in cells:
        if g.terrain(*c) in PATHS or g.terrain(*c) in {"water", "deep", "swamp"}:
            protect(c[0], c[1], 1)
    for w in m.get("warps", []):
        protect(w["x"], w["y"], 2)
    for n in m.get("npcs", []):
        protect(n["x"], n["y"], 2)
    for sp in m.get("spawns", []):
        protect(int(sp["x"]), int(sp["y"]), 1)
    sp0 = m.get("spawn", {})
    start = (int(sp0.get("x", 0)), int(sp0.get("y", 0)))
    protect(start[0], start[1], 2)
    for p in m.get("props", []):
        if p.get("dialog") or PROPS.get(p["type"], {}).get("interactive"):
            protect(p["x"], p["y"], 2)

    # NPCs e conteúdo condicional contam como passagem livre no teste de alcance
    if not g.walkable(start):
        for w in m.get("warps", []):
            if g.walkable((w["x"], w["y"])):
                start = (w["x"], w["y"])
                break
    targets = {(w["x"], w["y"]) for w in m.get("warps", [])}
    for n in m.get("npcs", []) + [p for p in m.get("props", []) if p.get("dialog")]:
        for d in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            targets.add((n["x"] + d[0], n["y"] + d[1]))
    targets |= {(int(s["x"]), int(s["y"])) for s in m.get("spawns", [])}
    base = g.reach(start)
    goal = targets & base

    def safe(block):
        """block: células que deixam de ser passáveis. Aceita se não corta nada."""
        after = g.reach(start)
        return goal <= after and len(after) >= len(base) - len(block)

    changed = 0
    # 1. reentrâncias nas bordas da mata/rocha
    edge = []
    for (x, y) in open_cells:
        if (x, y) in prot:
            continue
        walls = [g.terrain(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if g.terrain(x + dx, y + dy) in WALLS]
        if walls:
            edge.append(((x, y), walls[0]))
    rng.shuffle(edge)
    grown = []
    for (x, y), wall in edge[: int(len(edge) * 0.45)]:
        old = g.terrain(x, y)
        g.set_terrain(x, y, wall)
        if safe({(x, y)}):
            base = g.reach(start)
            changed += 1
            grown.append(((x, y), wall))
        else:
            g.set_terrain(x, y, old)
    # segunda camada: algumas reentrâncias viram "dentes" mais fundos
    for (x, y), wall in grown[: len(grown) // 3]:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if g.terrain(*n) in OPEN and n not in prot and rng.random() < 0.5:
                old = g.terrain(*n)
                g.set_terrain(n[0], n[1], wall)
                if safe({n}):
                    base = g.reach(start)
                    changed += 1
                else:
                    g.set_terrain(n[0], n[1], old)
                break

    # copas: árvores e pedras por cima da mata/rocha (só onde tudo em volta já é parede)
    taken = [(p["x"], p["y"]) for p in m.get("props", [])]
    for (x, y) in cells:
        t = g.terrain(x, y)
        kinds = CANOPY.get(t, {}).get(region)
        if not kinds or rng.random() > 0.22:
            continue
        if any(g.terrain(x + dx, y + dy) != t for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
            continue
        if any(abs(x - px) < 2 and abs(y - py) < 2 for px, py in taken):
            continue
        kind = rng.choice(kinds)
        if kind not in PROPS:
            continue
        m.setdefault("props", []).append({"type": kind, "x": x, "y": y})
        taken.append((x, y))
        changed += 1

    # 2. manchas de flores
    if region in FLOWER_REGIONS:
        grass = [c for c in open_cells if g.terrain(*c) == "grass" and c not in prot]
        for _ in range(max(1, len(grass) // 140)):
            if not grass:
                break
            cx, cy = rng.choice(grass)
            for ox in range(-1, 2):
                for oy in range(-1, 2):
                    if rng.random() < 0.6 and g.terrain(cx + ox, cy + oy) == "grass" and (cx + ox, cy + oy) not in prot:
                        g.set_terrain(cx + ox, cy + oy, "flowers")
                        changed += 1

    # 3. detalhes da região
    palette = DECOR.get(region, [])
    if palette:
        free = [c for c in cells if g.terrain(*c) in OPEN and c not in prot and c not in g.prop_cells]
        rng.shuffle(free)
        want = len(free) // 26
        placed = []
        for (x, y) in free:
            if want <= 0:
                break
            if any(abs(x - px) <= 2 and abs(y - py) <= 2 for px, py in placed):
                continue
            opts = [(t, w) for t, terr, w in palette if g.terrain(x, y) in terr and t in PROPS]
            if not opts:
                continue
            t = rng.choices([o[0] for o in opts], weights=[o[1] for o in opts])[0]
            coll = [(x + dx, y + dy) for dx, dy in PROPS[t].get("collision", [])]
            if any(c in prot or c in g.prop_cells or g.terrain(*c) not in OPEN for c in coll):
                continue
            prop = {"type": t, "x": x, "y": y}
            for c in coll:
                g.prop_cells[c] = prop
            if coll and not safe(set(coll)):
                for c in coll:
                    del g.prop_cells[c]
                continue
            if coll:
                base = g.reach(start)
            m.setdefault("props", []).append(prop)
            placed.append((x, y))
            want -= 1
            changed += 1

    m["ground"] = ["".join(r) for r in g.rows]
    m["legend"] = g.legend
    m["refined"] = True
    return changed


def main(ids):
    total = 0
    for f in sorted((ROOT / "data/maps").glob("*.json")):
        if ids and f.stem not in ids:
            continue
        m = json.loads(f.read_text(encoding="utf-8"))
        n = refine(m)
        if n is False:
            continue
        f.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        total += 1
        print(f"refine: {f.stem} ({n} mudanças)")
    print(f"refine: {total} mapas refinados")


if __name__ == "__main__":
    main(sys.argv[1:])
