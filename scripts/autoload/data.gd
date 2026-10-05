extends Node
## Carrega e guarda em cache os arquivos JSON de dados (data/ e config/).
## Nenhum conteúdo do jogo fica no código: mapas, NPCs, diálogos e regiões vêm daqui.

var _cache: Dictionary = {}


func load_json(path: String) -> Variant:
	if _cache.has(path):
		return _cache[path]
	if not FileAccess.file_exists(path):
		push_error("Data: arquivo inexistente %s" % path)
		return null
	var text := FileAccess.get_file_as_string(path)
	var json := JSON.new()
	var err := json.parse(text)
	if err != OK:
		push_error("Data: JSON inválido em %s (linha %d): %s" % [path, json.get_error_line(), json.get_error_message()])
		return null
	_cache[path] = json.data
	return json.data


func clear_cache() -> void:
	_cache.clear()


func map(id: String) -> Dictionary:
	var d = load_json("res://data/maps/%s.json" % id)
	return d if d is Dictionary else {}


func has_map(id: String) -> bool:
	return FileAccess.file_exists("res://data/maps/%s.json" % id)


func tileset(id: String) -> Dictionary:
	var d = load_json("res://data/tilesets/%s.json" % id)
	return d if d is Dictionary else {}


func props() -> Dictionary:
	var d = load_json("res://data/props.json")
	return d.get("props", {}) if d is Dictionary else {}


func props_texture() -> String:
	var d = load_json("res://data/props.json")
	return d.get("texture", "") if d is Dictionary else ""


func npc(id: String) -> Dictionary:
	var d = load_json("res://data/npcs.json")
	if d is Dictionary and d.get("npcs", {}).has(id):
		return d["npcs"][id]
	return {}


func regions() -> Dictionary:
	var d = load_json("res://data/regions.json")
	return d.get("regions", {}) if d is Dictionary else {}


func region(id: String) -> Dictionary:
	return regions().get(id, {})


func publisher() -> Dictionary:
	var d = load_json("res://config/publisher.json")
	return d if d is Dictionary else {}


## Diálogos são referenciados como "arquivo/id", ex.: "prologo/bento_praia".
func dialog(ref: String) -> Array:
	var parts := ref.split("/")
	if parts.size() != 2:
		push_error("Data: referência de diálogo inválida '%s'" % ref)
		return []
	var d = load_json("res://data/dialogs/%s.json" % parts[0])
	if d is Dictionary and d.get("dialogs", {}).has(parts[1]):
		return d["dialogs"][parts[1]]
	push_error("Data: diálogo '%s' não encontrado" % ref)
	return []


# ------------------------------------------------------------------ batalha
var _species_index: Dictionary = {}
var _moves_index: Dictionary = {}


func battle_rules() -> Dictionary:
	var d = load_json("res://data/battle.json")
	return d if d is Dictionary else {}


## Índice de espécies: data/species.json (fase 3, linhas achatadas por estágio)
## + data/test/species_test.json (bonecos de treino da fase 2).
func species(id: String) -> Dictionary:
	if _species_index.is_empty():
		_build_species_index()
	return _species_index.get(id, {})


func all_species_ids(include_test: bool = true) -> Array:
	if _species_index.is_empty():
		_build_species_index()
	return _species_index.keys().filter(func(k: String) -> bool: return include_test or not bool(_species_index[k].get("test", false)))


func _build_species_index() -> void:
	if FileAccess.file_exists("res://data/species.json"):
		var d = load_json("res://data/species.json")
		for line in d.get("lines", []):
			for i in line.get("stages", []).size():
				var st: Dictionary = line["stages"][i].duplicate(true)
				for k in ["type", "region", "rarity", "growth_levels", "signature_move"]:
					if line.has(k) and not st.has(k):
						st[k] = line[k]
				st["line"] = line.get("id", "")
				st["stage"] = i + 1
				_species_index[str(st["id"])] = st
		for u in d.get("uniques", []):
			_species_index[str(u["id"])] = u
		if d.get("king"):
			_species_index[str(d["king"]["id"])] = d["king"]
	var t = load_json("res://data/test/species_test.json")
	if t is Dictionary:
		for id in t.get("species", {}).keys():
			var s: Dictionary = t["species"][id].duplicate(true)
			s["id"] = id
			s["test"] = true
			_species_index[id] = s


func move(id: String) -> Dictionary:
	if _moves_index.is_empty():
		for path in ["res://data/moves.json", "res://data/test/moves_test.json"]:
			if not FileAccess.file_exists(path):
				continue
			var d = load_json(path)
			var list = d.get("moves", {})
			if list is Array:
				for m in list:
					_moves_index[str(m["id"])] = m
			else:
				for k in list.keys():
					var m: Dictionary = list[k].duplicate(true)
					m["id"] = k
					_moves_index[k] = m
	return _moves_index.get(id, {})


func item(id: String) -> Dictionary:
	var d = load_json("res://data/items.json")
	return d.get("items", {}).get(id, {}) if d is Dictionary else {}


func all_items() -> Dictionary:
	var d = load_json("res://data/items.json")
	return d.get("items", {}) if d is Dictionary else {}


## Espécies de uma linha, em ordem de estágio (Bebê, Adolescente, Adulto).
func line_stages(line_id: String) -> Array:
	if _species_index.is_empty():
		_build_species_index()
	var out := []
	for id in _species_index.keys():
		var s: Dictionary = _species_index[id]
		if str(s.get("line", "")) == line_id:
			out.append(id)
	out.sort_custom(func(a: String, b: String) -> bool: return int(_species_index[a].get("stage", 1)) < int(_species_index[b].get("stage", 1)))
	return out


## Tabela de encontros (data/encounters.json e, para testes, data/test/encounters_test.json).
func encounter_table(id: String) -> Array:
	for path in ["res://data/encounters.json", "res://data/test/encounters_test.json"]:
		if FileAccess.file_exists(path):
			var d = load_json(path)
			if d is Dictionary and d.get("tables", {}).has(id):
				return d["tables"][id]
	return []
