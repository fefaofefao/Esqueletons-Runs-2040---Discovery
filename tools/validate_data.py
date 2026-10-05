#!/usr/bin/env python3
"""Validação automática dos dados do jogo (AGENTS.md, seção 12).

Falha (código 1) se encontrar:
  - IDs duplicados ou referências quebradas (mapas, props, NPCs, diálogos, regiões);
  - total de espécies diferente de 80; linha sem 3 estágios;
  - níveis de crescimento fora de ordem; selvagem de estágio 2/3 abaixo do crescimento;
  - atributos fora da banda do estágio; tipos desbalanceados (mais de ±1 linha);
  - prefixo de nome repetido mais de 2 vezes; golpe assinatura repetido;
  - chave de tradução faltando, vazia ou não traduzida em EN/ES;
  - cidade sem rancho, loja ou com menos de 2 casas de domadores;
  - rota sem caminho alternativo.

Arquivos de fases futuras (species/moves/encounters/cities/routes/balance) são
validados assim que existirem; enquanto não existem, aparecem como PENDENTE.
O formato esperado está em docs/DADOS.md.

Uso: python3 tools/validate_data.py
"""
import csv
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
LANGS = ["pt_BR", "en", "es"]
TYPES = ["fisico", "magico", "cura", "veneno"]
STAGE_BANDS = {1: (250, 320), 2: (360, 430), 3: (470, 540)}
UNIQUE_BAND = (450, 520)
KING_TOTAL = (590, 610)
STATS = ["hp", "atk", "mag", "def", "res", "spd"]

errors: list[str] = []
pending: list[str] = []
infos: list[str] = []


def err(msg):
    errors.append(msg)


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        err(f"{path.relative_to(ROOT)}: JSON inválido ({e})")
        return None


def res_path(p: str) -> Path:
    return ROOT / p.replace("res://", "")


# ---------------------------------------------------------------- traduções
def load_translations():
    keys = {}
    for csv_path in sorted((ROOT / "i18n").glob("*.csv")):
        with csv_path.open(encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            header = next(reader)
            if header[:1] != ["keys"] or any(lang not in header for lang in LANGS):
                err(f"{csv_path.name}: cabeçalho deve ser keys,{','.join(LANGS)}")
                continue
            idx = {lang: header.index(lang) for lang in LANGS}
            for row in reader:
                if not row or not row[0].strip():
                    continue
                key = row[0].strip()
                if key in keys:
                    err(f"tradução: chave duplicada {key} ({csv_path.name})")
                keys[key] = {lang: (row[idx[lang]] if idx[lang] < len(row) else "") for lang in LANGS}
    allow = set()
    allow_file = ROOT / "i18n" / "allow_identical.txt"
    if allow_file.exists():
        for line in allow_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                allow.add(line)
    for key, t in keys.items():
        for lang in LANGS:
            if not t[lang].strip():
                err(f"tradução: {key} vazia em {lang}")
        for lang in ("en", "es"):
            if t[lang].strip() and t[lang] == t["pt_BR"] and key not in allow:
                err(f"tradução: {key} em {lang} igual ao PT-BR (esquecida? ou adicione em i18n/allow_identical.txt)")
        for lang in ("en", "es"):
            ph_pt = set(re.findall(r"\{(\w+)\}", t["pt_BR"]))
            ph = set(re.findall(r"\{(\w+)\}", t[lang]))
            if ph_pt != ph:
                err(f"tradução: {key} em {lang} com placeholders diferentes do PT ({sorted(ph)} vs {sorted(ph_pt)})")
    # project.godot precisa registrar os .translation de cada CSV
    proj = (ROOT / "project.godot").read_text(encoding="utf-8")
    for csv_path in (ROOT / "i18n").glob("*.csv"):
        for lang in LANGS:
            ref = f"res://i18n/{csv_path.stem}.{lang}.translation"
            if ref not in proj:
                err(f"project.godot não registra {ref}")
    return keys


def need_key(keys, key, where):
    if key not in keys:
        err(f"{where}: chave de tradução inexistente '{key}'")


def check_code_keys(keys):
    """Chaves literais usadas no código (ex.: "MENU_NEW_GAME") precisam existir."""
    pattern = re.compile(r'"([A-Z][A-Z0-9]*_[A-Z0-9_]*[A-Z0-9])"')
    ignore = {"res", "user"}
    for gd in list((ROOT / "scripts").rglob("*.gd")):
        text = gd.read_text(encoding="utf-8")
        for m in pattern.finditer(text):
            key = m.group(1)
            if key in ignore or key.startswith(("KEY_", "JOY_", "MOUSE_", "NOTIFICATION_")):
                continue
            need_key(keys, key, gd.relative_to(ROOT).as_posix())


# ---------------------------------------------------------------- mundo
def check_world(keys):
    props = (load(DATA / "props.json") or {}).get("props", {})
    npcs = (load(DATA / "npcs.json") or {}).get("npcs", {})
    regions = (load(DATA / "regions.json") or {}).get("regions", {})
    tileset_cache = {}
    planned_maps = set()
    for rid, r in regions.items():
        need_key(keys, r.get("name_key", ""), f"regions.json:{rid}")
        for m in r.get("maps", []):
            if m in planned_maps:
                err(f"regions.json: mapa {m} listado em duas regiões")
            planned_maps.add(m)
    dialogs = {}
    for dfile in sorted((DATA / "dialogs").glob("*.json")):
        d = load(dfile) or {}
        for did, nodes in d.get("dialogs", {}).items():
            ref = f"{dfile.stem}/{did}"
            dialogs[ref] = nodes
    for ref, nodes in dialogs.items():
        for n in nodes:
            for k in ("say", "speaker"):
                if k in n:
                    need_key(keys, n[k], f"diálogo {ref}")
            if "goto" in n and n["goto"] not in dialogs:
                err(f"diálogo {ref}: goto quebrado '{n['goto']}'")
            for opt in n.get("choice", []):
                need_key(keys, opt.get("text", ""), f"diálogo {ref} (opção)")
                if "goto" in opt and opt["goto"] not in dialogs:
                    err(f"diálogo {ref}: goto de opção quebrado '{opt['goto']}'")
    for nid, n in npcs.items():
        need_key(keys, n.get("name_key", ""), f"npcs.json:{nid}")
        if not res_path(n.get("sprite", "")).exists():
            err(f"npcs.json:{nid}: sprite inexistente {n.get('sprite')}")
        if not n.get("role"):
            err(f"npcs.json:{nid}: todo NPC precisa de uma função (role)")
        dl = n.get("dialog", [])
        for entry in ([{"dialog": dl}] if isinstance(dl, str) else dl):
            if entry.get("dialog") not in dialogs:
                err(f"npcs.json:{nid}: diálogo inexistente {entry.get('dialog')}")
    maps = {}
    for mfile in sorted((DATA / "maps").glob("*.json")):
        m = load(mfile)
        if not m:
            continue
        mid = mfile.stem
        if m.get("id") != mid:
            err(f"mapa {mid}: id interno '{m.get('id')}' diferente do nome do arquivo")
        maps[mid] = m
    for mid, m in maps.items():
        where = f"mapa {mid}"
        if mid not in planned_maps:
            err(f"{where}: não está em nenhuma região de regions.json")
        if m.get("region") not in regions:
            err(f"{where}: região inexistente {m.get('region')}")
        if "name_key" in m:
            need_key(keys, m["name_key"], where)
        ts_id = m.get("tileset", "overworld")
        if ts_id not in tileset_cache:
            tileset_cache[ts_id] = load(DATA / "tilesets" / f"{ts_id}.json") or {}
        terrains = tileset_cache[ts_id].get("terrains", {})
        legend = m.get("legend", {})
        for ch, t in legend.items():
            if t not in terrains:
                err(f"{where}: legenda '{ch}' aponta para terreno inexistente '{t}'")
        rows = m.get("ground", [])
        width = len(rows[0]) if rows else 0
        for y, row in enumerate(rows):
            if len(row) != width:
                err(f"{where}: linha {y} com largura {len(row)} (esperado {width})")
            for ch in row:
                if ch not in legend:
                    err(f"{where}: caractere '{ch}' fora da legenda (linha {y})")
                    break

        def terrain(x, y):
            if 0 <= y < len(rows) and 0 <= x < len(rows[y]):
                return legend.get(rows[y][x])
            return None

        solid = set()
        for p in m.get("props", []):
            if p.get("type") not in props:
                err(f"{where}: prop desconhecido {p.get('type')}")
                continue
            for c in props[p["type"]].get("collision", []):
                solid.add((p["x"] + c[0], p["y"] + c[1]))
            if "dialog" in p and p["dialog"] not in dialogs:
                err(f"{where}: diálogo do prop inexistente {p['dialog']}")
            if p.get("dialog") and not props[p["type"]].get("collision"):
                err(f"{where}: prop interativo {p['type']} sem célula sólida para interagir")
        ids = Counter()
        for n in m.get("npcs", []):
            ids[n.get("id")] += 1
            if n.get("id") not in npcs:
                err(f"{where}: NPC desconhecido {n.get('id')}")
            solid.add((n["x"], n["y"]))
        for nid, c in ids.items():
            if c > 1:
                err(f"{where}: NPC {nid} duplicado")

        def walkable(x, y):
            t = terrain(x, y)
            return t is not None and not terrains.get(t, {}).get("solid", True) and (x, y) not in solid

        sp = m.get("spawn", {})
        if not walkable(sp.get("x", -1), sp.get("y", -1)):
            err(f"{where}: spawn em célula bloqueada")
        for w in m.get("warps", []):
            if not walkable(w["x"], w["y"]):
                err(f"{where}: porta ({w['x']},{w['y']}) em célula bloqueada")
            to = w.get("to")
            if to in maps:
                tm = maps[to]
                if w.get("tx", -1) >= 0:
                    trows = tm.get("ground", [])
                    tleg = tm.get("legend", {})
                    tt = tleg.get(trows[w["ty"]][w["tx"]]) if 0 <= w["ty"] < len(trows) and 0 <= w["tx"] < len(trows[w["ty"]]) else None
                    tts = tileset_cache.get(tm.get("tileset", "overworld")) or load(DATA / "tilesets" / f"{tm.get('tileset', 'overworld')}.json") or {}
                    if tt is None or tts.get("terrains", {}).get(tt, {}).get("solid", True):
                        err(f"{where}: porta para {to} chega em célula bloqueada ({w['tx']},{w['ty']})")
            elif to not in planned_maps:
                err(f"{where}: porta para mapa inexistente e não planejado '{to}'")
            if "locked_message" in w:
                need_key(keys, w["locked_message"], where)
    infos.append(f"{len(maps)} mapas, {len(npcs)} NPCs, {len(dialogs)} diálogos")


# ---------------------------------------------------------------- esqueletos (fase 3)
def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def check_species(keys):
    path = DATA / "species.json"
    if not path.exists():
        pending.append("species.json (fase 3b/3c): 80 espécies, estágios, bandas, tipos, prefixos, assinaturas")
        return None
    d = load(path) or {}
    lines = d.get("lines", [])
    uniques = d.get("uniques", [])
    king = d.get("king")
    all_ids = Counter()
    total = 0
    type_count = Counter()
    signatures = Counter()
    growth = {}
    for ln in lines:
        lid = ln.get("id", "?")
        stages = ln.get("stages", [])
        if len(stages) != 3:
            err(f"espécies: linha {lid} sem 3 estágios ({len(stages)})")
        gl = ln.get("growth_levels", [])
        if len(gl) != 2 or not (0 < gl[0] < gl[1] <= 100):
            err(f"espécies: linha {lid} com níveis de crescimento fora de ordem {gl}")
        growth[lid] = gl
        if ln.get("type") not in TYPES:
            err(f"espécies: linha {lid} com tipo inválido {ln.get('type')}")
        type_count[ln.get("type")] += 1
        if ln.get("signature_move"):
            signatures[ln["signature_move"]] += 1
        else:
            err(f"espécies: linha {lid} sem golpe assinatura")
        for i, st in enumerate(stages, start=1):
            all_ids[st.get("id")] += 1
            total += 1
            need_key(keys, st.get("name_key", ""), f"espécie {st.get('id')}")
            _check_band(st, STAGE_BANDS.get(i, (0, 9999)), f"{st.get('id')} (estágio {i})")
            growth[st.get("id")] = (i, gl)
    for u in uniques:
        all_ids[u.get("id")] += 1
        total += 1
        need_key(keys, u.get("name_key", ""), f"único {u.get('id')}")
        _check_band(u, UNIQUE_BAND, f"{u.get('id')} (único)")
    if king:
        all_ids[king.get("id")] += 1
        total += 1
        need_key(keys, king.get("name_key", ""), "Rei Esqueleto")
        _check_band(king, KING_TOTAL, "Rei Esqueleto")
    for sid, c in all_ids.items():
        if c > 1:
            err(f"espécies: ID duplicado {sid}")
    if total != 80:
        err(f"espécies: total {total} (esperado 80)")
    if len(lines) != 24:
        err(f"espécies: {len(lines)} linhas de 3 estágios (esperado 24)")
    if len(uniques) != 7:
        err(f"espécies: {len(uniques)} únicos/raros (esperado 7)")
    for t in TYPES:
        if abs(type_count[t] - 6) > 1:
            err(f"espécies: tipo {t} com {type_count[t]} linhas (esperado 6 ±1)")
    for mv, c in signatures.items():
        if c > 1:
            err(f"espécies: golpe assinatura {mv} repetido em {c} linhas")
    # prefixos de nome, por idioma
    for lang in LANGS:
        prefixes = Counter()
        for key in [st.get("name_key") for ln in lines for st in ln.get("stages", [])] + [u.get("name_key") for u in uniques]:
            name = keys.get(key, {}).get(lang, "")
            if len(name) >= 3:
                prefixes[strip_accents(name[:3]).lower()] += 1
            if re.search(r"\d", name) or re.match(r"(?i)^(esqueleto|skeleton|ossinho)\b", name):
                err(f"espécies: nome numerado/descritivo proibido '{name}' ({lang})")
        for p, c in prefixes.items():
            if c > 2:
                err(f"espécies: prefixo '{p.capitalize()}-' usado {c} vezes em {lang} (máx. 2)")
    return growth


def _check_band(entry, band, where):
    stats = entry.get("stats", {})
    missing = [s for s in STATS if s not in stats]
    if missing:
        err(f"espécies: {where} sem atributos {missing}")
        return
    total = sum(stats[s] for s in STATS)
    if not band[0] <= total <= band[1]:
        err(f"espécies: {where} com total {total} fora da banda {band[0]}–{band[1]}")


def check_moves(keys):
    path = DATA / "moves.json"
    if not path.exists():
        pending.append("moves.json (fase 3c): 56 golpes (16 físicos, 16 mágicos, 12 cura, 12 veneno)")
        return set()
    d = load(path) or {}
    ids = Counter(m.get("id") for m in d.get("moves", []))
    for mid, c in ids.items():
        if c > 1:
            err(f"golpes: ID duplicado {mid}")
    counts = Counter(m.get("type") for m in d.get("moves", []))
    want = {"fisico": 16, "magico": 16, "cura": 12, "veneno": 12}
    for t, n in want.items():
        if counts[t] != n:
            err(f"golpes: {counts[t]} do tipo {t} (esperado {n})")
    for m in d.get("moves", []):
        need_key(keys, m.get("name_key", ""), f"golpe {m.get('id')}")
        for f in ("power", "accuracy", "pp", "target", "effect"):
            if f not in m:
                err(f"golpes: {m.get('id')} sem o campo {f}")
    return set(ids)


def check_encounters(growth):
    path = DATA / "encounters.json"
    if not path.exists():
        pending.append("encounters.json (fase 4): tabelas por área com espécie, estágio, níveis e raridade")
        return
    d = load(path) or {}
    for zone, entries in d.get("tables", {}).items():
        for e in entries:
            sid = e.get("species")
            if growth is not None and sid not in growth:
                err(f"encontros {zone}: espécie inexistente {sid}")
                continue
            if growth is None:
                continue
            info = growth[sid]
            if isinstance(info, tuple):
                stage, gl = info
                if stage >= 2 and e.get("min_level", 0) < gl[stage - 2]:
                    err(f"encontros {zone}: {sid} (estágio {stage}) no nível {e.get('min_level')} abaixo do crescimento {gl[stage - 2]}")
            if e.get("min_level", 0) > e.get("max_level", 0):
                err(f"encontros {zone}: {sid} com faixa de nível invertida")


def check_cities(keys):
    path = DATA / "cities.json"
    if not path.exists():
        pending.append("cities.json (fase 4): rancho, loja e 2–3 casas de domadores por cidade")
        return
    d = load(path) or {}
    for c in d.get("cities", []):
        cid = c.get("id", "?")
        if not c.get("ranch"):
            err(f"cidade {cid}: sem rancho")
        if not c.get("shop"):
            err(f"cidade {cid}: sem loja")
        houses = c.get("tamer_houses", [])
        if not 2 <= len(houses) <= 3:
            err(f"cidade {cid}: {len(houses)} casas de domadores (esperado 2 ou 3)")
        if not 3 <= len(c.get("npcs", [])) <= 6:
            err(f"cidade {cid}: {len(c.get('npcs', []))} NPCs (esperado 3 a 6)")


def check_routes():
    path = DATA / "routes.json"
    if not path.exists():
        pending.append("routes.json (fase 4): 2–3 caminhos por rota (domadores, selvagem, atalho)")
        return
    d = load(path) or {}
    for r in d.get("routes", []):
        paths = r.get("paths", [])
        if len(paths) < 2:
            err(f"rota {r.get('id')}: sem caminho alternativo ({len(paths)} caminho)")
        if any(p.get("required") for p in paths):
            err(f"rota {r.get('id')}: nenhum caminho pode ser obrigatório")


def check_balance():
    path = DATA / "balance.json"
    if not path.exists():
        pending.append("balance.json (fase 3c): metas de nível por região e constantes")
        return
    load(path)


def check_battle(keys):
    """Regras de batalha, itens e dados de teste da fase 2."""
    b = load(DATA / "battle.json") or {}
    if sorted(b.get("types", [])) != sorted(TYPES):
        err(f"battle.json: tipos {b.get('types')} diferentes de {TYPES}")
    beats = b.get("type_chart", {}).get("beats", {})
    if beats != {"fisico": "magico", "magico": "veneno", "veneno": "fisico"}:
        err("battle.json: ciclo de vantagens deve ser Físico > Mágico > Veneno > Físico (Cura neutro)")
    if b.get("level_max") != 100 or b.get("enemy_level_max") != 120 or b.get("party_size") != 4 or b.get("active_per_side") != 2:
        err("battle.json: idade máxima 100 (chefe final 120), time de 4 e 2 em campo")
    need_key(keys, b.get("struggle", {}).get("name_key", ""), "battle.json (struggle)")
    for iid, it in ((load(DATA / "items.json") or {}).get("items", {})).items():
        need_key(keys, it.get("name_key", ""), f"item {iid}")
        need_key(keys, it.get("desc_key", ""), f"item {iid}")
        if it.get("kind") not in ("heal", "cure", "revive", "key"):
            err(f"item {iid}: tipo desconhecido {it.get('kind')}")
    moves = {}
    for path in [DATA / "moves.json", DATA / "test" / "moves_test.json"]:
        if path.exists():
            d = load(path) or {}
            lst = d.get("moves", {})
            for mid, mv in (lst.items() if isinstance(lst, dict) else ((m.get("id"), m) for m in lst)):
                if mid in moves:
                    err(f"golpes: ID duplicado {mid}")
                moves[mid] = mv
                need_key(keys, mv.get("name_key", ""), f"golpe {mid}")
                need_key(keys, mv.get("desc_key", ""), f"golpe {mid}")
                if mv.get("type") not in TYPES:
                    err(f"golpe {mid}: tipo inválido {mv.get('type')}")
                if mv.get("weight", "normal") not in ("light", "normal", "heavy"):
                    err(f"golpe {mid}: peso inválido {mv.get('weight')}")
                if mv.get("target") not in ("enemy", "all_enemies", "self", "ally", "all_allies"):
                    err(f"golpe {mid}: alvo inválido {mv.get('target')}")
    tpath = DATA / "test" / "species_test.json"
    if tpath.exists():
        for sid, sp in ((load(tpath) or {}).get("species", {})).items():
            need_key(keys, sp.get("name_key", ""), f"boneco {sid}")
            if not res_path(sp.get("sprite", "")).exists():
                err(f"boneco {sid}: sprite inexistente")
            for lvl, mid in sp.get("learnset", []):
                if mid not in moves:
                    err(f"boneco {sid}: learnset com golpe inexistente {mid}")


def check_publisher():
    p = load(ROOT / "config" / "publisher.json") or {}
    for f in ("game_name", "edition", "producer", "contact_email", "website", "privacy_policy_url", "package_name", "version_name"):
        if f not in p:
            err(f"publisher.json: campo obrigatório ausente '{f}'")
    for lang in LANGS:
        if lang not in p.get("edition", {}):
            err(f"publisher.json: edição sem o idioma {lang}")
    pkg = p.get("package_name", "")
    if not re.fullmatch(r"[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+", pkg) and "[" not in pkg:
        err(f"publisher.json: package_name inválido '{pkg}'")


def main():
    keys = load_translations()
    check_code_keys(keys)
    check_world(keys)
    growth = check_species(keys)
    check_moves(keys)
    check_encounters(growth)
    check_cities(keys)
    check_routes()
    check_balance()
    check_battle(keys)
    check_publisher()
    infos.append(f"{len(keys)} chaves de tradução × {len(LANGS)} idiomas")
    for i in infos:
        print(f"info: {i}")
    for p in pending:
        print(f"PENDENTE: {p}")
    if errors:
        for e in errors:
            print(f"ERRO: {e}")
        print(f"\nvalidate_data: {len(errors)} erro(s).")
        return 1
    print("validate_data: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
