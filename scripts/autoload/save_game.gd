extends Node
## Save local em user:// (JSON versionado, um slot com backup).
## Grava primeiro num arquivo temporário; o save anterior vira o backup.
## Ao carregar, se o principal estiver corrompido, usa o backup.

signal saved
signal loaded

const VERSION := 2

## Caminhos (variáveis para os testes usarem arquivos próprios).
var save_path := "user://save.json"
var backup_path := "user://save.bak.json"
var tmp_path := "user://save.tmp"

var data: Dictionary = {}
## Contagem de tempo de jogo ativa (só no mapa, fora de pausa).
var tracking := false

## Migrações: versão de origem -> Callable(Dictionary) -> Dictionary.
var _migrations := {
	0: _migrate_0_to_1,
	1: _migrate_1_to_2,
}


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_PAUSABLE


func _process(delta: float) -> void:
	if not tracking or data.is_empty():
		return
	var region: String = data.get("player", {}).get("region", "")
	if region == "":
		return
	var pt: Dictionary = data["play_time"]
	var real := delta / maxf(Engine.time_scale, 0.0001)
	pt["real"] = float(pt.get("real", 0.0)) + real
	pt["game"] = float(pt.get("game", 0.0)) + delta
	var by: Dictionary = pt["by_region"]
	if not by.has(region):
		by[region] = {"real": 0.0, "game": 0.0}
	by[region]["real"] = float(by[region]["real"]) + real
	by[region]["game"] = float(by[region]["game"]) + delta


static func new_game_data(player_name: String) -> Dictionary:
	return {
		"version": VERSION,
		"created_at": Time.get_unix_time_from_system(),
		"saved_at": 0,
		"player": {
			"name": player_name,
			"map": "praia_despertar",
			"region": "praia",
			"x": -1,
			"y": -1,
			"facing": "down",
		},
		"flags": {},
		"play_time": {"real": 0.0, "game": 0.0, "by_region": {}},
		"party": [],
		"ranch": [],
		"bag": {},
		"money": 0,
		"ossuary": {},
		"respawn": {"map": "praia_despertar", "x": -1, "y": -1, "facing": "down"},
	}


func start_new(player_name: String) -> void:
	data = new_game_data(player_name)


func has_save() -> bool:
	return FileAccess.file_exists(save_path) or FileAccess.file_exists(backup_path)


func save_game() -> bool:
	if data.is_empty():
		return false
	data["version"] = VERSION
	data["saved_at"] = Time.get_unix_time_from_system()
	var text := JSON.stringify(data, "\t")
	var f := FileAccess.open(tmp_path, FileAccess.WRITE)
	if f == null:
		push_error("SaveGame: não foi possível gravar %s" % tmp_path)
		return false
	f.store_string(text)
	f.close()
	if FileAccess.file_exists(save_path):
		if FileAccess.file_exists(backup_path):
			DirAccess.remove_absolute(backup_path)
		DirAccess.rename_absolute(save_path, backup_path)
	var err := DirAccess.rename_absolute(tmp_path, save_path)
	if err != OK:
		push_error("SaveGame: falha ao renomear o save (%d)" % err)
		return false
	saved.emit()
	return true


func load_game() -> bool:
	for path in [save_path, backup_path]:
		var d := read_file(path)
		if d.is_empty():
			continue
		data = migrate(d)
		loaded.emit()
		return true
	return false


func read_file(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		return {}
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	if not parsed is Dictionary:
		push_warning("SaveGame: arquivo corrompido %s" % path)
		return {}
	if not parsed.has("player"):
		return {}
	return parsed


func delete_save() -> void:
	for p in [save_path, backup_path, tmp_path]:
		if FileAccess.file_exists(p):
			DirAccess.remove_absolute(p)


func migrate(d: Dictionary) -> Dictionary:
	var v := int(d.get("version", 0))
	while v < VERSION:
		if not _migrations.has(v):
			push_error("SaveGame: sem migração a partir da versão %d" % v)
			break
		d = _migrations[v].call(d)
		v += 1
		d["version"] = v
	# Garante as chaves da versão atual (saves antigos ou editados à mão)
	var fresh := new_game_data(str(d.get("player", {}).get("name", "")))
	for k in fresh.keys():
		if not d.has(k):
			d[k] = fresh[k]
	return d


## v1 → v2: os dois iniciais. O parceiro único vira lista e ganha o bônus de inicial.
func _migrate_1_to_2(d: Dictionary) -> Dictionary:
	var uids: Array = d.get("partner_uids", [])
	if d.has("partner_uid") and not uids.has(int(d["partner_uid"])):
		uids.append(int(d["partner_uid"]))
	d.erase("partner_uid")
	d["partner_uids"] = uids
	for key in ["party", "ranch"]:
		for m in d.get(key, []):
			if m is Dictionary and uids.has(int(m.get("uid", 0))):
				m["starter"] = true
	return d


## v0 (protótipo): {"name", "map", "x", "y"} soltos na raiz.
func _migrate_0_to_1(d: Dictionary) -> Dictionary:
	var out := new_game_data(str(d.get("name", "")))
	if d.has("player") and d["player"] is Dictionary:
		out["player"].merge(d["player"], true)
	else:
		out["player"]["map"] = str(d.get("map", "praia_despertar"))
		out["player"]["x"] = int(d.get("x", -1))
		out["player"]["y"] = int(d.get("y", -1))
	if d.has("flags") and d["flags"] is Dictionary:
		out["flags"] = d["flags"]
	return out


# ------------------------------------------------------------- acesso rápido
func player_name() -> String:
	return str(data.get("player", {}).get("name", ""))


## Lia ou Taro (os iniciais): falas próprias ao crescer.
func is_partner(uid: int) -> bool:
	for u in data.get("partner_uids", []):
		if int(u) == uid:
			return true
	return false


func get_flag(flag: String) -> bool:
	return bool(data.get("flags", {}).get(flag, false))


func set_flag(flag: String, value: bool = true) -> void:
	if not data.has("flags"):
		data["flags"] = {}
	data["flags"][flag] = value


func set_position(map_id: String, region: String, cell: Vector2i, facing: String) -> void:
	var p: Dictionary = data["player"]
	p["map"] = map_id
	p["region"] = region
	p["x"] = cell.x
	p["y"] = cell.y
	p["facing"] = facing


func region_times() -> Dictionary:
	return data.get("play_time", {}).get("by_region", {})
