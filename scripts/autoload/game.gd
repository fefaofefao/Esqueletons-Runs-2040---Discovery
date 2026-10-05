extends Node
## Fluxo do jogo: telas (título/mundo), pilha de overlays, transições com fade,
## botão voltar do Android, salvamento automático e atalhos globais (2x, debug).

signal overlay_changed
signal screen_changed(screen_name: String)

const FADE_TIME := 0.22

var main: Node = null
var screen: Node = null
var world: World = null
var overlays: Array[Overlay] = []
var transitioning := false
var touch: TouchControls = null
var battle: BattleScreen = null

var _screen_root: Node
var _overlay_layer: CanvasLayer
var _touch_layer: CanvasLayer
var _fade_layer: CanvasLayer
var _fade: ColorRect


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	get_tree().set_auto_accept_quit(false)


## Chamado pela cena principal. Monta as camadas e abre a tela de título.
func boot(main_node: Node) -> void:
	main = main_node
	get_tree().root.theme = UiTheme.build()
	_screen_root = Node.new()
	_screen_root.name = "Screen"
	main.add_child(_screen_root)
	_overlay_layer = _layer("Overlays", 20)
	_touch_layer = _layer("Touch", 30)
	_fade_layer = _layer("Fade", 40)
	touch = TouchControls.new()
	_touch_layer.add_child(touch)
	_fade = ColorRect.new()
	_fade.color = Color(0.06, 0.05, 0.08, 1.0)
	_fade.set_anchors_preset(Control.PRESET_FULL_RECT)
	_fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_fade_layer.add_child(_fade)
	goto_title(false)


func _layer(layer_name: String, index: int) -> CanvasLayer:
	var l := CanvasLayer.new()
	l.name = layer_name
	l.layer = index
	l.process_mode = Node.PROCESS_MODE_ALWAYS
	main.add_child(l)
	return l


# ------------------------------------------------------------------ telas
func goto_title(with_fade: bool = true) -> void:
	await _transition(func() -> void:
		SaveGame.tracking = false
		world = null
		_set_screen(TitleScreen.new(), "title")
	, with_fade)


func start_new_game(player_name: String) -> void:
	SaveGame.start_new(player_name)
	await enter_world()


func continue_game() -> void:
	if SaveGame.load_game():
		await enter_world()


func enter_world() -> void:
	var p: Dictionary = SaveGame.data["player"]
	await _transition(func() -> void:
		var w := World.new()
		_set_screen(w, "world")
		world = w
		w.load_map(str(p.get("map", "praia_despertar")), Vector2i(int(p.get("x", -1)), int(p.get("y", -1))), str(p.get("facing", "down")))
		SaveGame.tracking = true
	)
	autosave()
	await world.run_on_enter()


## Troca de mapa com fade e salvamento automático.
func warp(map_id: String, cell: Vector2i, facing: String) -> void:
	if world == null or transitioning:
		return
	await _transition(func() -> void:
		world.load_map(map_id, cell, facing)
	)
	autosave()
	await world.run_on_enter()


func _set_screen(node: Node, screen_name: String) -> void:
	close_all_overlays()
	if screen:
		screen.queue_free()
		_screen_root.remove_child(screen)
	screen = node
	_screen_root.add_child(node)
	if touch:
		touch.set_world_mode(screen_name == "world")
	screen_changed.emit(screen_name)


func _transition(action: Callable, with_fade: bool = true) -> void:
	transitioning = true
	Controls.clear()
	if _fade and with_fade:
		_fade.mouse_filter = Control.MOUSE_FILTER_STOP
		var tw := create_tween()
		tw.tween_property(_fade, "color:a", 1.0, FADE_TIME)
		await tw.finished
	action.call()
	if _fade:
		_fade.color.a = 1.0
		await get_tree().process_frame
		var tw2 := create_tween()
		tw2.tween_property(_fade, "color:a", 0.0, FADE_TIME)
		await tw2.finished
		_fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	transitioning = false


# ------------------------------------------------------------------ overlays
func open_overlay(o: Overlay) -> Overlay:
	o.mark_opened()
	overlays.append(o)
	if _overlay_layer:
		_overlay_layer.add_child(o)
	else:
		add_child(o)
	_update_pause()
	overlay_changed.emit()
	return o


func close_overlay(o: Overlay) -> void:
	if not overlays.has(o):
		return
	overlays.erase(o)
	o.is_closed = true
	# o próximo overlay do topo ignora o quadro atual (o mesmo toque não o aciona)
	if not overlays.is_empty():
		overlays.back().mark_opened()
	o.closed.emit()
	o.queue_free()
	_update_pause()
	overlay_changed.emit()


func close_all_overlays() -> void:
	for o in overlays.duplicate():
		close_overlay(o)


func top_overlay() -> Overlay:
	return null if overlays.is_empty() else overlays.back()


func _update_pause() -> void:
	var p := false
	for o in overlays:
		if o.pauses_game:
			p = true
	get_tree().paused = p


func world_input_enabled() -> bool:
	return world != null and overlays.is_empty() and not transitioning and battle == null


# ------------------------------------------------------------------ batalha
## Abre uma batalha por cima do mapa e espera o resultado ("win", "lose", "fled").
## info: ver BattleScreen.setup. A equipe vem do save e volta para ele no fim.
func start_battle(info: Dictionary) -> String:
	if battle != null or world == null:
		return ""
	var party: Array = []
	for d in SaveGame.data.get("party", []):
		party.append(Monster.from_dict(d))
	if party.filter(func(m: Monster) -> bool: return not m.is_fainted()).is_empty():
		await show_message("BTL_NO_PARTY")
		return ""
	if not SaveGame.data.has("bag"):
		SaveGame.data["bag"] = {}
	transitioning = true
	Controls.clear()
	await _battle_flash()
	battle = BattleScreen.new().setup(info, party, SaveGame.data["bag"])
	world.visible = false
	if touch:
		touch.set_battle_mode(true)
	main.add_child(battle)
	var tw := create_tween()
	tw.tween_property(_fade, "color:a", 0.0, FADE_TIME)
	await tw.finished
	_fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	transitioning = false
	var result: String = await battle.finished
	SaveGame.data["party"] = party.map(func(m: Monster) -> Dictionary: return m.to_dict())
	for rec in battle.recruits:
		Ossuary.add_to_team(rec)
	if result == "lose":
		_apply_defeat(party)
	transitioning = true
	_fade.mouse_filter = Control.MOUSE_FILTER_STOP
	var tw2 := create_tween()
	tw2.tween_property(_fade, "color:a", 1.0, FADE_TIME)
	await tw2.finished
	battle.queue_free()
	battle = null
	world.visible = true
	if touch:
		touch.set_battle_mode(false)
	if result == "lose":
		var r: Dictionary = SaveGame.data.get("respawn", {})
		var map_id := str(r.get("map", "praia_despertar"))
		world.load_map(map_id, Vector2i(int(r.get("x", -1)), int(r.get("y", -1))), str(r.get("facing", "down")))
	var tw3 := create_tween()
	tw3.tween_property(_fade, "color:a", 0.0, FADE_TIME)
	await tw3.finished
	_fade.mouse_filter = Control.MOUSE_FILTER_IGNORE
	transitioning = false
	autosave()
	if result == "lose":
		await show_message("BTL_LOSE_MONEY", {"n": int(SaveGame.data.get("last_money_loss", 0))})
	else:
		await run_growths()
	return result


## Crescimentos pendentes acontecem ao voltar ao mapa, um de cada vez.
func run_growths() -> void:
	if world == null or world.player == null:
		return
	var party: Array = SaveGame.data.get("party", [])
	for i in party.size():
		var m := Monster.from_dict(party[i])
		while m.growth_target() != "":
			var pos := world.player.get_global_transform_with_canvas().origin
			var c := GrowthCeremony.new().setup(m, pos)
			open_overlay(c)
			await c.closed
			party[i] = m.to_dict()
			SaveGame.data["party"] = party
			autosave()


func _battle_flash() -> void:
	_fade.mouse_filter = Control.MOUSE_FILTER_STOP
	var tw := create_tween()
	for i in 3:
		tw.tween_property(_fade, "color", Color(1, 1, 1, 0.85), 0.06)
		tw.tween_property(_fade, "color", Color(1, 1, 1, 0.0), 0.08)
	tw.tween_property(_fade, "color", Color(0.06, 0.05, 0.08, 1.0), 0.22)
	await tw.finished


## Derrota: perde parte das moedas, a equipe é curada e volta ao último ponto seguro.
func _apply_defeat(party: Array) -> void:
	var loss := int(int(SaveGame.data.get("money", 0)) * float(Data.battle_rules().get("defeat", {}).get("money_loss", 0.1)))
	SaveGame.data["money"] = int(SaveGame.data.get("money", 0)) - loss
	SaveGame.data["last_money_loss"] = loss
	for m in party:
		m.heal_full()
	SaveGame.data["party"] = party.map(func(m: Monster) -> Dictionary: return m.to_dict())


# ------------------------------------------------------------------ atalhos
func show_dialog(ref: String) -> void:
	await play_script(Data.dialog(ref))


## Roteiro com falas e ações: cada ação fecha a caixa, roda e o diálogo continua.
func play_script(nodes: Array) -> void:
	var rest := nodes
	while not rest.is_empty():
		var box := DialogBox.new()
		box.setup(rest)
		open_overlay(box)
		if not box.is_closed:
			await box.closed
		var action: Dictionary = box.pending_action
		rest = box.pending_rest
		if action.is_empty():
			return
		if not await ScriptActions.run(action):
			return


func show_message(key: String, args: Dictionary = {}) -> void:
	var box := DialogBox.new()
	box.setup([{"say": key, "args": args}])
	open_overlay(box)
	await box.closed


func open_pause() -> void:
	if world and top_overlay() == null and not transitioning:
		Audio.sfx("menu_open")
		open_overlay(PauseMenu.new())


func open_debug() -> void:
	if not OS.is_debug_build():
		return
	for o in overlays:
		if o is DebugMenu:
			return
	open_overlay(DebugMenu.new())


func autosave() -> void:
	if world == null or SaveGame.data.is_empty():
		return
	world.store_position()
	SaveGame.save_game()


func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("btn_speed", false):
		Speed.toggle()
		Audio.sfx("speed_on" if Speed.fast else "speed_off")
		get_viewport().set_input_as_handled()
	elif event.is_action_pressed("dbg_menu", false) and OS.is_debug_build():
		open_debug()
		get_viewport().set_input_as_handled()


func _notification(what: int) -> void:
	match what:
		NOTIFICATION_WM_GO_BACK_REQUEST:
			_on_back()
		NOTIFICATION_WM_CLOSE_REQUEST:
			autosave()
			get_tree().quit()
		NOTIFICATION_APPLICATION_PAUSED:
			autosave()
			open_pause()
		NOTIFICATION_APPLICATION_FOCUS_OUT:
			autosave()


func _on_back() -> void:
	if transitioning:
		return
	var top := top_overlay()
	if top:
		top.on_back()
	elif battle:
		Controls.tap_action("btn_b")
	elif world:
		open_pause()
	else:
		get_tree().quit()
