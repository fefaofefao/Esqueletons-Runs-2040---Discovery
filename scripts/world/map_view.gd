class_name MapView
extends Node2D
## Monta um mapa a partir de data/maps/<id>.json: terreno em ASCII, transições
## automáticas (espuma, areia molhada, franja de grama, água funda), props,
## NPCs, placas, portas/saídas e partículas de ambiente.

const T := 16

static var _tilesets := {}

var id := ""
var data: Dictionary = {}
var size := Vector2i.ZERO
var region_id := ""
var spawn_cell := Vector2i.ZERO
var spawn_facing := "down"

var ground: TileMapLayer
var ground_props: Node2D
var entities: Node2D

var _terrain: Array[PackedStringArray] = []
var _solid_props := {}
var _interactions := {}
var _warps := {}
var _npcs := {}
var _wilds := {}
## Zonas de spawn de selvagens (dados do mapa + as criadas pelo debug).
var spawns: Array = []
var _tileset_id := ""


func build(map_id: String) -> bool:
	id = map_id
	data = Data.map(map_id)
	if data.is_empty():
		push_error("MapView: mapa '%s' não encontrado" % map_id)
		return false
	region_id = str(data.get("region", ""))
	_tileset_id = str(data.get("tileset", "overworld"))
	_parse_terrain()
	var ts_info := tileset_info(_tileset_id)
	ground = _new_layer("Ground", ts_info.tileset)
	_paint_ground(ts_info)
	for ov in ts_info.desc.get("overlays", []):
		var layer := _new_layer("Overlay_" + str(ov["id"]), ts_info.tileset)
		_paint_overlay(layer, ov, ts_info.source_id)
	ground_props = Node2D.new()
	ground_props.name = "GroundProps"
	add_child(ground_props)
	entities = Node2D.new()
	entities.name = "Entities"
	entities.y_sort_enabled = true
	add_child(entities)
	_place_props()
	_place_npcs()
	_place_warps()
	spawns = data.get("spawns", []).duplicate(true)
	var sp: Dictionary = data.get("spawn", {})
	spawn_cell = Vector2i(int(sp.get("x", 0)), int(sp.get("y", 0)))
	spawn_facing = str(sp.get("facing", "down"))
	Ambient.add_to_map(self)
	Speed.changed.connect(_on_speed_changed)
	_on_speed_changed(Speed.multiplier())
	return true


func _parse_terrain() -> void:
	var legend: Dictionary = data.get("legend", {})
	var rows: Array = data.get("ground", [])
	size = Vector2i(0, rows.size())
	_terrain.clear()
	for r in rows:
		var line := PackedStringArray()
		var s := str(r)
		size.x = maxi(size.x, s.length())
		for ch in s:
			line.append(str(legend.get(ch, "void")))
		_terrain.append(line)


func terrain_at(cell: Vector2i) -> String:
	if cell.y < 0 or cell.y >= _terrain.size():
		return ""
	var row: PackedStringArray = _terrain[cell.y]
	if cell.x < 0 or cell.x >= row.size():
		return ""
	return row[cell.x]


func in_bounds(cell: Vector2i) -> bool:
	return cell.x >= 0 and cell.y >= 0 and cell.x < size.x and cell.y < size.y


func pixel_size() -> Vector2:
	return Vector2(size * T)


static func cell_to_pos(cell: Vector2i) -> Vector2:
	## Posição dos "pés": centro inferior da célula.
	return Vector2(cell.x * T + T / 2.0, cell.y * T + T)


# ------------------------------------------------------------ tileset
static func tileset_info(ts_id: String) -> Dictionary:
	if _tilesets.has(ts_id):
		return _tilesets[ts_id]
	var desc := Data.tileset(ts_id)
	var ts := TileSet.new()
	ts.tile_size = Vector2i(T, T)
	var src := TileSetAtlasSource.new()
	src.texture = load(str(desc["texture"]))
	src.texture_region_size = Vector2i(T, T)
	var animated: Array[Vector2i] = []
	var add_tile := func(pos: Vector2i, frames: int, fps: float) -> void:
		if src.has_tile(pos):
			return
		src.create_tile(pos)
		if frames > 1 and fps > 0.0:
			src.set_tile_animation_columns(pos, 0)
			src.set_tile_animation_frames_count(pos, frames)
			for i in frames:
				src.set_tile_animation_frame_duration(pos, i, 1.0 / fps)
			animated.append(pos)
	for tname in desc.get("terrains", {}).keys():
		var t: Dictionary = desc["terrains"][tname]
		for v in t["variants"]:
			add_tile.call(Vector2i(int(v[0]), int(v[1])), int(t.get("frames", 1)), float(t.get("fps", 0.0)))
	for ov in desc.get("overlays", []):
		for key in ov["masks"].keys():
			var p: Array = ov["masks"][key]
			add_tile.call(Vector2i(int(p[0]), int(p[1])), int(ov.get("frames", 1)), float(ov.get("fps", 0.0)))
	var sid := ts.add_source(src)
	var info := {"tileset": ts, "source": src, "source_id": sid, "desc": desc, "animated": animated}
	_tilesets[ts_id] = info
	return info


func _new_layer(layer_name: String, ts: TileSet) -> TileMapLayer:
	var l := TileMapLayer.new()
	l.name = layer_name
	l.tile_set = ts
	add_child(l)
	return l


static func cell_hash(cell: Vector2i, salt: int = 0) -> int:
	var h := (cell.x * 73856093) ^ (cell.y * 19349663) ^ (salt * 83492791)
	h = (h ^ (h >> 13)) * 1274126177
	return absi(h ^ (h >> 16))


func _paint_ground(info: Dictionary) -> void:
	var terrains: Dictionary = info.desc["terrains"]
	for y in size.y:
		for x in size.x:
			var cell := Vector2i(x, y)
			var tname := terrain_at(cell)
			if tname == "" or not terrains.has(tname):
				continue
			var t: Dictionary = terrains[tname]
			var variants: Array = t["variants"]
			var weights: Array = t.get("weights", [])
			var pick := 0
			if variants.size() > 1:
				var total := 0
				for w in weights:
					total += int(w)
				var r := cell_hash(cell, 7) % maxi(total, 1)
				for i in weights.size():
					r -= int(weights[i])
					if r < 0:
						pick = i
						break
			var v: Array = variants[pick]
			ground.set_cell(cell, info.source_id, Vector2i(int(v[0]), int(v[1])))


const _NB := [
	[Vector2i(0, -1), 1], [Vector2i(1, 0), 2], [Vector2i(0, 1), 4], [Vector2i(-1, 0), 8],
	[Vector2i(1, -1), 16], [Vector2i(1, 1), 32], [Vector2i(-1, 1), 64], [Vector2i(-1, -1), 128],
]


## Máscara canônica: bordas N/E/S/W + cantos só quando as duas bordas vizinhas estão livres.
static func canonical_mask(mask: int) -> int:
	var m := mask & 15
	for c in [[16, 1, 2], [32, 4, 2], [64, 4, 8], [128, 1, 8]]:
		if mask & c[0] and not (mask & c[1]) and not (mask & c[2]):
			m |= c[0]
	return m


func _paint_overlay(layer: TileMapLayer, ov: Dictionary, source_id: int) -> void:
	var on: Array = ov["on"]
	var near: Array = ov["near"]
	var masks: Dictionary = ov["masks"]
	for y in size.y:
		for x in size.x:
			var cell := Vector2i(x, y)
			if not terrain_at(cell) in on:
				continue
			var mask := 0
			for nb in _NB:
				var n: Vector2i = cell + nb[0]
				if in_bounds(n) and terrain_at(n) in near:
					mask |= int(nb[1])
			mask = canonical_mask(mask)
			if mask == 0 or not masks.has(str(mask)):
				continue
			var p: Array = masks[str(mask)]
			layer.set_cell(cell, source_id, Vector2i(int(p[0]), int(p[1])))


func _on_speed_changed(mult: float) -> void:
	# Animações de tiles usam o relógio do renderizador; ajusta para respeitar o 2x.
	var info := tileset_info(_tileset_id)
	var src: TileSetAtlasSource = info.source
	for pos in info.animated:
		src.set_tile_animation_speed(pos, mult)


# ------------------------------------------------------------ props, NPCs, portas
func _place_props() -> void:
	var defs := Data.props()
	var tex: Texture2D = load(Data.props_texture())
	for p in data.get("props", []):
		if not condition_ok(p):
			continue
		var pid := str(p.get("type", ""))
		if not defs.has(pid):
			push_error("MapView: prop desconhecido '%s' em %s" % [pid, id])
			continue
		var def: Dictionary = defs[pid]
		var cell := Vector2i(int(p["x"]), int(p["y"]))
		var node := PropSprite.create(def, tex, pid)
		node.position = cell_to_pos(cell)
		if str(def.get("layer", "y")) == "ground":
			ground_props.add_child(node)
		else:
			entities.add_child(node)
		var cells: Array[Vector2i] = [cell]
		for c in def.get("collision", []):
			var cc := cell + Vector2i(int(c[0]), int(c[1]))
			_solid_props[cc] = true
			cells.append(cc)
		if p.has("dialog"):
			# qualquer célula sólida do objeto aceita interação (ex.: estante de 2 tiles)
			for cc in cells:
				_interactions[cc] = {"dialog": str(p["dialog"])}


## Condição de flag (mapas, NPCs e diálogos):
##   "if": flag · "if_not": flag · "if_all": [flags] · "if_any": [flags]
##   "if_count": {"flags": [...], "min": n}  (ex.: pontos de Redenção)
static func condition_ok(entry: Dictionary) -> bool:
	if entry.has("if") and not SaveGame.get_flag(str(entry["if"])):
		return false
	if entry.has("if_not") and SaveGame.get_flag(str(entry["if_not"])):
		return false
	for f in entry.get("if_all", []):
		if not SaveGame.get_flag(str(f)):
			return false
	if entry.has("if_any"):
		var any := false
		for f in entry["if_any"]:
			any = any or SaveGame.get_flag(str(f))
		if not any:
			return false
	if entry.has("if_count"):
		var c: Dictionary = entry["if_count"]
		var n := 0
		for f in c.get("flags", []):
			if SaveGame.get_flag(str(f)):
				n += 1
		if n < int(c.get("min", 1)):
			return false
	return true


func _place_npcs() -> void:
	for n in data.get("npcs", []):
		if not condition_ok(n) or SaveGame.get_flag("npc_gone_" + str(n["id"])):
			continue
		var npc := Npc.new()
		var cell := Vector2i(int(n["x"]), int(n["y"]))
		npc.setup(str(n["id"]), n, self)
		entities.add_child(npc)
		npc.place(cell, str(n.get("facing", "down")))
		_npcs[cell] = npc


func _place_warps() -> void:
	for w in data.get("warps", []):
		_warps[Vector2i(int(w["x"]), int(w["y"]))] = w


func remove_npc(id: String) -> void:
	for c in _npcs.keys():
		var npc: Npc = _npcs[c]
		if npc.npc_id == id:
			_npcs.erase(c)
			npc.queue_free()


func all_npcs() -> Array:
	return _npcs.values()


func move_npc(npc: Npc, from: Vector2i, to: Vector2i) -> void:
	_npcs.erase(from)
	_npcs[to] = npc


## Cria os selvagens de todas as zonas (chamado pelo World depois do jogador).
func spawn_wilds(world: World, rng: RandomNumberGenerator) -> void:
	for sp in spawns:
		if condition_ok(sp):
			_spawn_zone(world, sp, rng)


func _spawn_zone(world: World, sp: Dictionary, rng: RandomNumberGenerator) -> void:
	var table := Data.encounter_table(str(sp.get("table", "")))
	if table.is_empty():
		return
	var center := Vector2i(int(sp.get("x", 0)), int(sp.get("y", 0)))
	var r := int(sp.get("radius", 3))
	for i in int(sp.get("count", 2)):
		var cell := Vector2i(-1, -1)
		for attempt in 30:
			var c := center + Vector2i(rng.randi_range(-r, r), rng.randi_range(-r, r))
			if absi(c.x - center.x) + absi(c.y - center.y) <= r and not is_blocked(c) and (world.player == null or c != world.player.cell) \
					and (world.player == null or (c - world.player.cell).length() > 3):
				cell = c
				break
		if cell.x < 0:
			continue
		var spec := pick_encounter(table, rng)
		var w := WildSkeleton.new().setup(self, spec, cell, center, r, str(sp.get("behavior", "")))
		w.world = world
		w.spawn_id = "%s#%d" % [str(sp.get("id", "zona")), i]
		entities.add_child(w)
		_wilds[cell] = w


## Sorteia espécie/idade/Golden de uma tabela (peso explícito ou pela raridade).
static func pick_encounter(table: Array, rng: RandomNumberGenerator) -> Dictionary:
	var rarity_w := {"comum": 60, "incomum": 30, "raro": 10, "unico": 4}
	var total := 0
	for e in table:
		total += int(e.get("weight", rarity_w.get(str(e.get("rarity", "comum")), 30)))
	var roll := rng.randi_range(0, maxi(total - 1, 0))
	var pick: Dictionary = table[0]
	for e in table:
		roll -= int(e.get("weight", rarity_w.get(str(e.get("rarity", "comum")), 30)))
		if roll < 0:
			pick = e
			break
	var golden := DebugDraw.force_golden or Ossuary.roll_golden(rng)
	return {"species": str(pick["species"]), "level": rng.randi_range(int(pick.get("min_level", 1)), int(pick.get("max_level", 1))), "golden": golden}


func add_spawn(world: World, sp: Dictionary, rng: RandomNumberGenerator) -> void:
	spawns.append(sp)
	_spawn_zone(world, sp, rng)


func move_wild(w: WildSkeleton, from: Vector2i, to: Vector2i) -> void:
	_wilds.erase(from)
	_wilds[to] = w


func remove_wild(w: WildSkeleton) -> void:
	_wilds.erase(w.cell)
	w.queue_free()


func wild_at(cell: Vector2i) -> WildSkeleton:
	return _wilds.get(cell)


func npc_at(cell: Vector2i) -> Npc:
	return _npcs.get(cell)


func interaction_at(cell: Vector2i) -> Dictionary:
	return _interactions.get(cell, {})


func warp_at(cell: Vector2i) -> Dictionary:
	return _warps.get(cell, {})


func is_blocked(cell: Vector2i) -> bool:
	if not in_bounds(cell):
		return true
	if _solid_props.has(cell) or _npcs.has(cell) or _wilds.has(cell):
		return true
	var tname := terrain_at(cell)
	var t: Dictionary = tileset_info(_tileset_id).desc["terrains"].get(tname, {})
	return bool(t.get("solid", true))


func cells_of(terrain_names: Array) -> Array[Vector2i]:
	var out: Array[Vector2i] = []
	for y in size.y:
		for x in size.x:
			if terrain_at(Vector2i(x, y)) in terrain_names:
				out.append(Vector2i(x, y))
	return out


func props_of(type_name: String) -> Array[Vector2i]:
	var out: Array[Vector2i] = []
	for p in data.get("props", []):
		if str(p.get("type", "")) == type_name:
			out.append(Vector2i(int(p["x"]), int(p["y"])))
	return out
