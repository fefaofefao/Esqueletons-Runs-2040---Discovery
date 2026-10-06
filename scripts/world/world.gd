class_name World
extends Node2D
## Tela do mapa: carrega o MapView, posiciona o jogador, controla a câmera,
## a iluminação da região (CanvasModulate), o letreiro com o nome do lugar,
## portas/saídas e interações.

var map: MapView
var player: Player
var camera: Camera2D
var map_id := ""
var region_id := ""

var _tint: CanvasModulate
var _hud: CanvasLayer
var _banner: PanelContainer
var _banner_label: Label
var _banner_tween: Tween
var _debug_draw: DebugDraw
var _rng := RandomNumberGenerator.new()


func _ready() -> void:
	name = "World"
	camera = Camera2D.new()
	add_child(camera)
	camera.make_current()
	_tint = CanvasModulate.new()
	add_child(_tint)
	_hud = CanvasLayer.new()
	_hud.layer = 5
	add_child(_hud)
	_banner = PanelContainer.new()
	_banner.theme = UiTheme.build()
	_banner.add_theme_stylebox_override("panel", UiTheme.frame("dark"))
	_banner_label = UiTheme.label("", UiTheme.TEXT_LIGHT)
	_banner.add_child(_banner_label)
	_banner.visible = false
	_hud.add_child(_banner)
	_debug_draw = DebugDraw.new()
	_debug_draw.world = self
	add_child(_debug_draw)


func load_map(id: String, cell: Vector2i, facing: String) -> void:
	if map:
		# queue_free: o jogador antigo pode estar no meio do próprio _process (porta)
		remove_child(map)
		map.queue_free()
	map = MapView.new()
	map.name = "Map"
	add_child(map)
	move_child(map, 0)
	if not map.build(id):
		push_error("World: falha ao carregar '%s'" % id)
		return
	if cell.x < 0 or cell.y < 0 or map.is_blocked(cell):
		cell = map.spawn_cell
		facing = map.spawn_facing
	player = Player.new()
	map.entities.add_child(player)
	player.setup(self, map)
	player.place(cell, facing)
	_rng.randomize()
	map.spawn_wilds(self, _rng)
	var changed_region := region_id != map.region_id
	map_id = id
	region_id = map.region_id
	_apply_lighting()
	camera.position = camera_target()
	camera.reset_smoothing()
	SaveGame.set_position(map_id, region_id, cell, facing)
	Travel.mark_visited(map_id)
	var region := Data.region(region_id)
	Audio.play_music(str(map.data.get("music", region.get("music", ""))))
	if map.data.has("name_key") and (changed_region or bool(map.data.get("always_banner", false))):
		show_banner(str(map.data["name_key"]))
	_debug_draw.queue_redraw()


## Evento de entrada do mapa ("on_enter": [{"if"/"if_not", "dialog"}]): roda o
## primeiro que valer (ex.: o despertar na Praia, Lia e Taro na cabana).
func run_on_enter() -> void:
	if map == null:
		return
	for e in map.data.get("on_enter", []):
		if MapView.condition_ok(e):
			player.frozen = true
			await Game.show_dialog(str(e["dialog"]))
			if player:
				player.frozen = false
			return


func _apply_lighting() -> void:
	var region := Data.region(region_id)
	var t: Array = map.data.get("tint", region.get("tint", [1, 1, 1]))
	_tint.color = Color(float(t[0]), float(t[1]), float(t[2]))


func camera_target() -> Vector2:
	var vp := get_viewport_rect().size
	var mp := map.pixel_size()
	var t := player.position + Vector2(0, -8)
	var out := Vector2.ZERO
	out.x = mp.x / 2.0 if mp.x <= vp.x else clampf(t.x, vp.x / 2.0, mp.x - vp.x / 2.0)
	out.y = mp.y / 2.0 if mp.y <= vp.y else clampf(t.y, vp.y / 2.0, mp.y - vp.y / 2.0)
	return out.round()


func _process(_delta: float) -> void:
	if map and player:
		camera.position = camera_target()


func show_banner(key: String) -> void:
	_banner_label.text = tr(key)
	_banner.reset_size()
	_banner.visible = true
	var left := 30.0
	_banner.position = Vector2(left, -_banner.size.y - 2)
	if _banner_tween:
		_banner_tween.kill()
	_banner_tween = create_tween()
	_banner_tween.tween_property(_banner, "position:y", 3.0, 0.3)
	_banner_tween.tween_interval(2.2)
	_banner_tween.tween_property(_banner, "position:y", -_banner.size.y - 2, 0.3)
	_banner_tween.tween_callback(func() -> void: _banner.visible = false)


func store_position() -> void:
	if map and player:
		SaveGame.set_position(map_id, region_id, player.cell, player.facing)


func on_player_arrived(cell: Vector2i) -> void:
	SaveGame.set_position(map_id, region_id, cell, player.facing)
	var w := map.warp_at(cell)
	if w.is_empty():
		return
	var to := str(w.get("to", ""))
	if not Data.has_map(to) or not MapView.condition_ok(w):
		player.frozen = true
		await Game.show_message(str(w.get("locked_message", "MSG_AREA_LOCKED")))
		player.step_back()
		player.frozen = false
		return
	player.frozen = true
	Audio.sfx(str(w.get("sfx", "door")))
	await Game.warp(to, Vector2i(int(w.get("tx", -1)), int(w.get("ty", -1))), str(w.get("facing", player.facing)))


## Um selvagem encostou no jogador (ou o jogador nele): começa a batalha.
func on_touch_wild(w: WildSkeleton) -> void:
	if not is_instance_valid(w) or w.stunned > 0.0 or Game.battle != null or Game.transitioning or not Game.world_input_enabled():
		return
	player.frozen = true
	var enemies := [[w.species, w.level, w.golden]]
	# às vezes vem uma dupla (outro da mesma zona)
	var table: Array = []
	for sp in map.spawns:
		var c := Vector2i(int(sp.get("x", 0)), int(sp.get("y", 0)))
		if (w.home - c).length() < 1.0:
			table = Data.encounter_table(str(sp.get("table", "")))
	if not table.is_empty() and _rng.randf() < 0.3:
		var extra := MapView.pick_encounter(table, _rng)
		enemies.append([extra.species, extra.level, extra.golden])
	var info := {"kind": "wild", "enemies": enemies}
	if not SaveGame.get_flag("tut_battle"):
		info["tips"] = ["BTL_TIP_TIMELINE", "BTL_TIP_WEIGHT", "BTL_TIP_SINTONIA"]
		SaveGame.set_flag("tut_battle")
	var result: String = await Game.start_battle(info)
	if result == "win" and not SaveGame.get_flag("tut_marker"):
		SaveGame.set_flag("tut_marker")
		await Game.show_dialog("prologo/marcador")
	if player:
		player.frozen = false
	if result == "win" and is_instance_valid(w):
		map.remove_wild(w)
	elif result == "fled" and is_instance_valid(w):
		w.stun(3.0)
	if result == "win":
		# intersticial: só aqui (vitória selvagem, já no mapa), com as regras de Ads
		await Ads.maybe_interstitial()


func interact(target: Vector2i, dir: Vector2i) -> void:
	var npc := map.npc_at(target)
	if npc:
		await npc.talk(dir)
		return
	var it := map.interaction_at(target)
	if not it.is_empty():
		await Game.show_dialog(str(it["dialog"]))


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("btn_menu", false) and Game.world_input_enabled():
		get_viewport().set_input_as_handled()
		Game.open_pause()
