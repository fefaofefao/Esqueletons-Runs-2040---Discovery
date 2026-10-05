class_name Npc
extends Node2D
## NPC parado na grade. Comportamentos: "stand" (fixo) e "look_around" (olha
## para os lados de tempos em tempos). Vira para o jogador ao conversar.
## Dados em data/npcs.json; posição e sobrescritas no mapa.

var npc_id := ""
var info: Dictionary = {}
var cell := Vector2i.ZERO
var home_facing := "down"
var sprite: CharacterSprite
var map: MapView
var talking := false
var _timer := 0.0
var _rng := RandomNumberGenerator.new()


func setup(id: String, placement: Dictionary, owner_map: MapView) -> void:
	npc_id = id
	map = owner_map
	info = Data.npc(id).duplicate(true)
	for k in placement.keys():
		if k not in ["id", "x", "y"]:
			info[k] = placement[k]
	name = "Npc_" + id
	sprite = CharacterSprite.new()
	add_child(sprite)
	sprite.setup(str(info.get("sprite", "")), int(info.get("frames", 2)), 6.0, float(info.get("idle_fps", 1.2)))
	_rng.seed = hash(id)
	_timer = _rng.randf_range(1.5, 3.5)


func place(c: Vector2i, facing: String) -> void:
	cell = c
	home_facing = facing
	position = MapView.cell_to_pos(c)
	sprite.face(facing)


func _process(delta: float) -> void:
	if talking or str(info.get("behavior", "stand")) != "look_around":
		return
	_timer -= delta
	if _timer <= 0.0:
		_timer = _rng.randf_range(1.8, 4.0)
		var dirs: Array = info.get("look_dirs", ["down", "left", "right"])
		sprite.face(str(dirs[_rng.randi() % dirs.size()]))


## Escolhe o diálogo: a primeira entrada cuja condição de flag é satisfeita.
func dialog_ref() -> String:
	var d = info.get("dialog", "")
	if d is String:
		return d
	for entry in d:
		if entry.has("if") and not SaveGame.get_flag(str(entry["if"])):
			continue
		if entry.has("if_not") and SaveGame.get_flag(str(entry["if_not"])):
			continue
		return str(entry.get("dialog", ""))
	return ""


func talk(from_dir: Vector2i) -> void:
	talking = true
	sprite.face(Controls.dir_name(-from_dir))
	var ref := dialog_ref()
	if ref != "":
		await Game.show_dialog(ref)
	talking = false
	_timer = _rng.randf_range(1.0, 2.5)


func patrol_radius() -> float:
	return float(info.get("radius", 0.0))
