#!/usr/bin/env python3
"""Validação automática dos dados do jogo (AGENTS.md, seção 12).

Falha (código 1) se encontrar:
  - IDs duplicados ou referências quebradas (mapas, props, NPCs, diálogos, regiões);
  - total de espécies diferente de 95 (80 + 15 da decisão 10); linha sem 3 estágios;
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
    # 80 da seção 8 + 15 da decisão 10 do Fernando (3 linhas novas e os 6 ases dos Guardiões)
    if total != 95:
        err(f"espécies: total {total} (esperado 95)")
    if len(lines) != 27:
        err(f"espécies: {len(lines)} linhas de 3 estágios (esperado 27)")
    if len(uniques) != 13:
        err(f"espécies: {len(uniques)} únicos/raros (esperado 13)")
    for t in TYPES:
        if abs(type_count[t] - len(lines) / 4) > 1.25:
            err(f"espécies: tipo {t} com {type_count[t]} linhas (esperado {len(lines) / 4:.1f} ±1)")
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
    # 56 da seção 8 + as 3 assinaturas das linhas novas (decisão 10)
    want = {"fisico": 17, "magico": 17, "cura": 12, "veneno": 13}
    for t, n in want.items():
        if counts[t] != n:
            err(f"golpes: {counts[t]} do tipo {t} (esperado {n})")
    kinds = {"poison", "stat", "heal", "cure", "delay", "drain"}
    for m in d.get("moves", []):
        mid = m.get("id")
        need_key(keys, m.get("name_key", ""), f"golpe {mid}")
        need_key(keys, m.get("desc_key", ""), f"descrição do golpe {mid}")
        for f in ("power", "accuracy", "pp", "target", "effects", "weight", "category"):
            if f not in m:
                err(f"golpes: {mid} sem o campo {f}")
        if m.get("weight") not in ("light", "normal", "heavy"):
            err(f"golpes: {mid} com peso inválido {m.get('weight')}")
        if m.get("target") not in ("enemy", "all_enemies", "self", "ally", "all_allies"):
            err(f"golpes: {mid} com alvo inválido {m.get('target')}")
        if m.get("category") not in ("physical", "magical", "status"):
            err(f"golpes: {mid} com categoria inválida {m.get('category')}")
        if m.get("category") == "status" and m.get("power", 0) != 0:
            err(f"golpes: {mid} é de status mas tem poder")
        if m.get("category") != "status" and not 0 < m.get("power", 0) <= 150:
            err(f"golpes: {mid} com poder fora de 1–150")
        if not m.get("effects") and m.get("category") == "status":
            err(f"golpes: {mid} de status sem efeito")
        for e in m.get("effects", []):
            if e.get("kind") not in kinds:
                err(f"golpes: {mid} com efeito desconhecido {e.get('kind')}")
    return set(ids)


def check_learnsets(move_ids):
    """Learnsets, golpes de crescimento e assinaturas apontam para golpes reais;
    cada assinatura é aprendida só pela própria linha."""
    path = DATA / "species.json"
    if not path.exists() or not move_ids:
        return
    d = load(path) or {}
    by_sig = {}
    for ln in d.get("lines", []):
        sig = ln.get("signature_move")
        if sig not in move_ids:
            err(f"espécies: linha {ln.get('id')} com assinatura inexistente {sig}")
        by_sig[sig] = ln.get("id")
    entries = [(st, ln.get("id")) for ln in d.get("lines", []) for st in ln.get("stages", [])]
    entries += [(u, u.get("id")) for u in d.get("uniques", [])]
    if d.get("king"):
        entries.append((d["king"], "rei"))
    for st, line_id in entries:
        ls = st.get("learnset")
        if not ls:
            err(f"espécies: {st.get('id')} sem learnset")
            continue
        ages = [a for a, _ in ls]
        if ages != sorted(ages):
            err(f"espécies: {st.get('id')} com learnset fora de ordem")
        for age, mid in ls:
            if mid not in move_ids:
                err(f"espécies: {st.get('id')} aprende golpe inexistente {mid}")
            elif mid in by_sig and by_sig[mid] != line_id:
                err(f"espécies: {st.get('id')} aprende a assinatura de outra linha ({mid})")
            if not 1 <= age <= 100:
                err(f"espécies: {st.get('id')} aprende {mid} com idade inválida {age}")
        gm = st.get("growth_move")
        if gm and gm not in move_ids:
            err(f"espécies: {st.get('id')} com golpe de crescimento inexistente {gm}")


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
        if not 1 <= len(c.get("quests", [])) <= 2:
            err(f"cidade {cid}: {len(c.get('quests', []))} missões secundárias (esperado 1 ou 2)")
        # tudo o que a ficha da cidade cita precisa existir de verdade
        npc_db = (load(DATA / "npcs.json") or {}).get("npcs", {})
        shops = (load(DATA / "shops.json") or {}).get("shops", {})
        if c.get("shop") and c["shop"] not in shops:
            err(f"cidade {cid}: loja '{c['shop']}' não existe em shops.json")
        placed = set()
        mp = DATA / "maps" / f"{c.get('map', '')}.json"
        if not mp.exists():
            err(f"cidade {cid}: mapa '{c.get('map')}' não existe")
            continue
        town = load(mp) or {}
        rooms = [load(DATA / "maps" / f"{w['to']}.json") or {} for w in town.get("warps", []) if (DATA / "maps" / f"{w['to']}.json").exists()]
        for m in [town] + rooms:
            placed |= {n["id"] for n in m.get("npcs", [])}
        for nid in [c.get("ranch")] + houses + c.get("npcs", []):
            if nid not in npc_db:
                err(f"cidade {cid}: NPC '{nid}' não existe em npcs.json")
            elif nid not in placed:
                err(f"cidade {cid}: NPC '{nid}' não está na cidade nem nos interiores")


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
        if not (DATA / "maps" / f"{r.get('map', '')}.json").exists():
            err(f"rota {r.get('id')}: mapa '{r.get('map')}' não existe")


def check_balance():
    path = DATA / "balance.json"
    if not path.exists():
        pending.append("balance.json (fase 3c): metas de nível por região e constantes")
        return
    b = load(path) or {}
    t = b.get("targets", {})
    if t.get("guardian_winrate") != [0.60, 0.85] or t.get("max_move_usage", 1) > 0.30 or t.get("max_type_gap", 1) > 0.20:
        err("balance.json: metas da seção 11 alteradas (vitória 60–85%, golpe ≤30%, tipo ≤20 pontos)")
    tm = t.get("total_minutes", [0, 0])
    if tm != [165, 195]:
        err("balance.json: tempo total deve mirar 2h45–3h15 (165–195 min)")
    spp = load(DATA / "species.json") or {}
    known = {st["id"] for ln in spp.get("lines", []) for st in ln.get("stages", [])} | {ln["id"] for ln in spp.get("lines", [])}
    known |= {u["id"] for u in spp.get("uniques", [])} | ({spp["king"]["id"]} if spp.get("king") else set())
    last = 0
    for r in b.get("regions", []):
        a = r.get("arrive", [0, 0])
        if a[0] < last - 5:
            err(f"balance.json: {r.get('id')} chega com idade menor que a região anterior")
        last = a[0]
        g = r.get("guardian_age", 0)
        if g and g > 100:
            err(f"balance.json: Guardião de {r.get('id')} acima de 100 anos")
        for key in ("guardian", "final_boss"):
            for e in r.get(key, []):
                if e[0] not in known:
                    err(f"balance.json: {r.get('id')}.{key} usa espécie/linha inexistente {e[0]}")
        for ln in r.get("wild_lines", []) + [x for x in r.get("team", []) if x != "@starters"]:
            if ln not in known:
                err(f"balance.json: {r.get('id')} usa linha inexistente {ln}")


def check_progression():
    """Selvagens e domadores acompanham a história: cada região começa perto da
    idade do último líder vencido e fica abaixo do próximo líder."""
    b = load(DATA / "balance.json") or {}
    pr = b.get("progression")
    if not pr:
        return
    regions = (load(DATA / "regions.json") or {}).get("regions", {})
    tables = (load(DATA / "encounters.json") or {}).get("tables", {})
    skip = tuple(pr.get("skip_battles", []))

    def battles(nodes):
        if isinstance(nodes, dict):
            if nodes.get("action") == "battle":
                yield nodes
            for v in nodes.values():
                yield from battles(v)
        elif isinstance(nodes, list):
            for v in nodes:
                yield from battles(v)

    dialogs = {}
    for f in (DATA / "dialogs").glob("*.json"):
        dialogs[f.stem] = (load(f) or {}).get("dialogs", {})

    def leader_ages(ref):
        f, did = ref.split("/")
        ages = [int(e[1]) for bt in battles(dialogs.get(f, {}).get(did, [])) for e in bt.get("enemies", [])]
        if not ages:
            err(f"balance.json: líder {ref} sem batalha")
        return ages or [0]

    # tabelas e arquivos de diálogo de cada região da história
    region_tables = {}
    region_files = {}
    for rid, reg in regions.items():
        bid = pr.get("map_region", {}).get(rid, rid)
        region_files.setdefault(bid, set()).add(rid)
        for mid in reg.get("maps", []):
            m = load(DATA / "maps" / f"{mid}.json") or {}
            for sp in m.get("spawns", []):
                if sp.get("table"):
                    region_tables.setdefault(bid, set()).add(sp["table"])
    prev = int(pr.get("start_age", 5))
    for r in b.get("regions", []):
        rid = r["id"]
        # média da equipe do líder: o ás (único) vem mais novo porque tem atributos de único
        la = leader_ages(r["leader"])
        nxt = int(sum(la) / len(la))
        lv = [(t, e) for t in sorted(region_tables.get(rid, [])) for e in tables.get(t, [])]
        if lv:
            low = min(e["min_level"] for _, e in lv)
            if low > prev + int(pr["entry_above_prev_leader"]):
                err(f"progressão: {rid} começa com selvagens de {low} anos, mas o último líder tinha {prev} (máx. {prev + int(pr['entry_above_prev_leader'])})")
            limit = nxt - int(pr["wild_below_next_leader"]) if rid != "prologo" else nxt
            for t, e in lv:
                if e["max_level"] > limit:
                    err(f"progressão: {t} tem {e['species']} com {e['max_level']} anos; o próximo líder ({r['leader']}) tem {nxt} (máx. {limit})")
        lead_top = max(leader_ages(r["leader"]))
        lead_file, lead_id = r["leader"].split("/")
        files = region_files.get(rid, set()) | {lead_file}
        if rid == "prologo":
            files |= {"prologo", "vila_mare"}
        for f in files:
            for did, nodes in dialogs.get(f, {}).items():
                if did == lead_id or did.startswith(skip):
                    continue
                for bt in battles(nodes):
                    if bt.get("kind") == "wild":
                        continue
                    top = max(int(e[1]) for e in bt.get("enemies", [[0, 0]]))
                    if top > lead_top - int(pr["tamer_below_next_leader"]):
                        err(f"progressão: domador {f}/{did} com {top} anos; o mais velho do próximo líder ({r['leader']}) tem {lead_top}")
        prev = max(leader_ages(r["leader"]))


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
    check_learnsets(check_moves(keys))
    check_encounters(growth)
    check_cities(keys)
    check_routes()
    check_balance()
    check_progression()
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
