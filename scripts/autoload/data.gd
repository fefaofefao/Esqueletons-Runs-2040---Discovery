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
