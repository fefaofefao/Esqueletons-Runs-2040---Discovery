class_name Npc
extends Node2D
## NPC parado na grade. Comportamentos: "stand" (fixo) e "look_around" (olha
## para os lados de tempos em tempos). Vira para o jogador ao conversar.
## Dados em data/npcs.json; posição e sobrescritas no mapa.
## Domador ("tamer": {"vision": N, "flag": vencido}): se o jogador entra na
## linha de visão (N células à frente, sem obstáculo), mostra "!", caminha
## até ele e começa o diálogo (que leva à batalha). Uma vez só.

var npc_id := ""
var info: Dictionary = {}
var cell := Vector2i.ZERO
var home_facing := "down"
var sprite: CharacterSprite
var map: MapView
var talking := false
var _timer := 0.0
var _rng := RandomNumberGenerator.new()
var facing := "down"
var _engaging := false


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
	self.facing = facing
	sprite.face(facing)


func _process(delta: float) -> void:
	if talking or _engaging:
		return
	if is_tamer_active():
		_watch()
	if str(info.get("behavior", "stand")) != "look_around":
		return
	_timer -= delta
	if _timer <= 0.0:
		_timer = _rng.randf_range(1.8, 4.0)
		var dirs: Array = info.get("look_dirs", ["down", "left", "right"])
		facing = str(dirs[_rng.randi() % dirs.size()])
		sprite.face(facing)


## Escolhe o diálogo: a primeira entrada cuja condição de flag é satisfeita.
func dialog_ref() -> String:
	var d = info.get("dialog", "")
	if d is String:
		return d
	for entry in d:
		if MapView.condition_ok(entry):
			return str(entry.get("dialog", ""))
	return ""


func is_tamer_active() -> bool:
	var t: Dictionary = info.get("tamer", {})
	return not t.is_empty() and not SaveGame.get_flag(str(t.get("flag", "")))


## Células que o domador enxerga (linha reta à frente, parando em obstáculos).
func vision_cells() -> Array:
	var out := []
	var dir := Controls.dir_from_name(facing)
	var c := cell
	for i in int(info.get("tamer", {}).get("vision", 4)):
		c += dir
		if map.is_blocked(c) and map.wild_at(c) == null:
			if Game.world and Game.world.player and Game.world.player.cell == c:
				out.append(c)
			break
		out.append(c)
	return out


func _watch() -> void:
	var w := Game.world
	if w == null or w.player == null or w.player.moving or not Game.world_input_enabled():
		return
	if w.player.cell in vision_cells():
		_engage(w.player)


func _engage(player: Player) -> void:
	_engaging = true
	player.frozen = true
	Audio.sfx("exclaim")
	var bang := UiTheme.label("!", UiTheme.TEXT_ACCENT)
	bang.position = Vector2(-3, -30)
	add_child(bang)
	await get_tree().create_timer(0.6).timeout
	bang.queue_free()
	var dir := Controls.dir_from_name(facing)
	while cell + dir != player.cell:
		var to := cell + dir
		map.move_npc(self, cell, to)
		cell = to
		sprite.walk(1.0)
		var tw := create_tween()
		tw.tween_property(self, "position", MapView.cell_to_pos(to), 0.22)
		await tw.finished
	sprite.idle()
	player.facing = Controls.dir_name(-dir)
	player.sprite.face(player.facing)
	player.frozen = false
	await talk(-dir)
	_engaging = false


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
