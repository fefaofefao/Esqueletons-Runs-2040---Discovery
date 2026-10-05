class_name BattleScreen
extends CanvasLayer
## Tela da batalha 2×2. Fluxo:
##   intro → comando (anel → golpes/alvo, itens, trocar, fugir) para cada aliado
##   → rodada (BattleEngine) → animação dos eventos → reposições → próxima rodada
##   → fim (vitória, derrota ou fuga).
## Controles: D-pad/teclado/gamepad e toque em tudo (anel, golpes, alvos, listas).
## MENU repete o último turno.

signal finished(result: String)

const ENEMY_POS := [Vector2(226, 88), Vector2(276, 80)]
const ENEMY_SINGLE := Vector2(250, 86)
const ALLY_POS := [Vector2(58, 150), Vector2(124, 156)]
const ALLY_SINGLE := Vector2(88, 152)

var engine: BattleEngine
var info: Dictionary = {}
var views := {}
var panels := {}
var state := "busy"

var _root: Control
var _field: Node2D
var _bg: Sprite2D
var _ox := 0.0
var _timeline: TimelineBar
var _ring: RingMenu
var _log: BattleLog
var _moves: MovePanel
var _preview: PanelContainer
var _list_panel: PanelContainer
var _list_title: Label
var _list: MenuList
var _repeat: PanelContainer
var _fx: Node2D
var _cmd_units: Array = []
var _cmd_i := 0
var _actions := {}
var _targets: Array = []
var _target_i := 0
var _pending_item := ""
var _list_mode := ""
var _list_cb: Callable
var _held := Vector2i.ZERO
var _next_ms := 0
var _ended := false


## info: {"kind": "wild"|"tamer"|"boss", "enemies": [[species, level], ...],
##        "tamer_key": chave do nome do domador, "reward": moedas}
func setup(battle_info: Dictionary, player_team: Array, bag: Dictionary) -> BattleScreen:
	info = battle_info
	engine = BattleEngine.new()
	var enemies := []
	for e in info.get("enemies", []):
		enemies.append(Monster.create(str(e[0]), int(e[1]), bool(e[2]) if e.size() > 2 else false))
	engine.setup(player_team, enemies, str(info.get("kind", "wild")), int(info.get("seed", -1)))
	engine.bag = bag
	return self


func _ready() -> void:
	layer = 10
	_root = Control.new()
	_root.theme = UiTheme.build()
	_root.set_anchors_preset(Control.PRESET_FULL_RECT)
	_root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_root)
	_bg = Sprite2D.new()
	_bg.texture = load(str(info.get("bg", "res://assets/battle/bg_praia.png")))
	_bg.centered = false
	_root.add_child(_bg)
	_field = Node2D.new()
	_field.y_sort_enabled = true
	_root.add_child(_field)
	_fx = Node2D.new()
	_fx.z_index = 10
	_root.add_child(_fx)
	_build_ui()
	get_viewport().size_changed.connect(_layout)
	_layout()
	_spawn_units()
	_run()


# ------------------------------------------------------------------ construção
func _build_ui() -> void:
	_timeline = TimelineBar.new()
	_timeline.mouse_filter = Control.MOUSE_FILTER_STOP
	_timeline.gui_input.connect(_on_timeline_input)
	_root.add_child(_timeline)
	_ring = RingMenu.new()
	_ring.visible = false
	_ring.chosen.connect(_on_ring_chosen)
	_root.add_child(_ring)
	_log = BattleLog.new()
	_log.visible = false
	_root.add_child(_log)
	_preview = PanelContainer.new()
	_preview.custom_minimum_size = Vector2(120, 52)
	_preview.visible = false
	var pv_inner := Control.new()
	pv_inner.custom_minimum_size = Vector2(106, 46)
	_preview.add_child(pv_inner)
	_root.add_child(_preview)
	_moves = MovePanel.new()
	_moves.visible = false
	_moves.build(pv_inner)
	_moves.tapped.connect(_on_move_tapped)
	_root.add_child(_moves)
	_list_panel = PanelContainer.new()
	_list_panel.visible = false
	_list_panel.custom_minimum_size = Vector2(196, 0)
	var box := VBoxContainer.new()
	_list_panel.add_child(box)
	_list_title = UiTheme.label("", UiTheme.TEXT_ACCENT)
	box.add_child(_list_title)
	_list = MenuList.new()
	_list.label_width = 120
	_list.max_visible = 6
	box.add_child(_list)
	_list.activated.connect(_on_list_activated)
	_list.cancelled.connect(_on_list_cancelled)
	_root.add_child(_list_panel)
	_repeat = PanelContainer.new()
	_repeat.add_theme_stylebox_override("panel", UiTheme.frame("dark"))
	_repeat.mouse_filter = Control.MOUSE_FILTER_STOP
	var rl := UiTheme.label("", UiTheme.TEXT_LIGHT)
	rl.name = "L"
	_repeat.add_child(rl)
	_repeat.gui_input.connect(func(e: InputEvent) -> void:
		if e is InputEventMouseButton and e.pressed:
			_repeat.accept_event()
			_repeat_last())
	_repeat.visible = false
	_root.add_child(_repeat)


func _layout() -> void:
	var vp := get_viewport().get_visible_rect().size
	_ox = floorf((vp.x - 320.0) / 2.0)
	_bg.position = Vector2(floorf((vp.x - _bg.texture.get_width()) / 2.0), 0)
	_field.position = Vector2(_ox, 0)
	_fx.position = Vector2(_ox, 0)
	_log.position = Vector2(_ox + 4, 128)
	_log.custom_minimum_size = Vector2(194, 50)
	_log.size = Vector2(194, 50)
	_moves.position = Vector2(_ox + 4, 128)
	_preview.position = Vector2(_ox + 196, 74)
	_list_panel.position = Vector2(_ox + 62, 34)
	_repeat.position = Vector2(_ox + 4, 21)
	_place_timeline()
	for uid in panels.keys():
		_place_panel(engine.find(uid))


func _place_timeline() -> void:
	var vp := get_viewport().get_visible_rect().size
	_timeline.position = Vector2(floorf((vp.x - _timeline.size.x) / 2.0), 1)


func _slot_pos(side: int, slot: int) -> Vector2:
	var count: int = engine.active[side].filter(func(i: int) -> bool: return i >= 0).size()
	if side == BattleEngine.ENEMY:
		return ENEMY_SINGLE if count <= 1 and slot == 0 else ENEMY_POS[slot]
	return ALLY_SINGLE if count <= 1 and slot == 0 else ALLY_POS[slot]


func _place_panel(m: Monster) -> void:
	if m == null or not panels.has(m.uid):
		return
	var p: UnitPanel = panels[m.uid]
	var slot := engine.slot_of(m)
	if slot < 0:
		p.visible = false
		return
	p.visible = true
	if m.side == BattleEngine.ENEMY:
		p.position = Vector2(_ox + 4, 40 + slot * 23)
	else:
		p.position = Vector2(_ox + 320 - 4 - UnitPanel.W, 128 + slot * 25)


func _spawn_units() -> void:
	for side in 2:
		for m in engine.teams[side]:
			var v := UnitView.new().setup(m, side == BattleEngine.ENEMY)
			v.visible = false
			_field.add_child(v)
			views[m.uid] = v
			var p := UnitPanel.new().setup(m, side == BattleEngine.PLAYER)
			p.visible = false
			_root.add_child(p)
			panels[m.uid] = p
	_root.move_child(_ring, -1)
	_root.move_child(_list_panel, -1)
	_root.move_child(_repeat, -1)


func _view(uid: int) -> UnitView:
	return views.get(uid)


func _name(uid: int) -> String:
	var m := engine.find(uid)
	return m.display_name() if m else "?"


func _say(key: String, args: Dictionary = {}) -> void:
	await _log.say(tr(key).format(args))


# ------------------------------------------------------------------ fluxo
func _run() -> void:
	Audio.sfx("menu_open")
	await _intro()
	while not _ended:
		await _command_phase()
		if _ended:
			break
		await _play_round()
		if engine.result != "":
			await _finish()
			break
		await _replacements()


func _intro() -> void:
	var enemies := engine.active_units(BattleEngine.ENEMY)
	var allies := engine.active_units(BattleEngine.PLAYER)
	for m in enemies:
		var v := _view(m.uid)
		v.position = _slot_pos(m.side, engine.slot_of(m))
		v.enter(false)
	await get_tree().create_timer(0.4).timeout
	for m in enemies:
		_place_panel(m)
	if engine.is_wild():
		if enemies.size() > 1:
			await _say("BTL_WILD_APPEARS_2", {"a": enemies[0].display_name(), "b": enemies[1].display_name()})
		else:
			await _say("BTL_WILD_APPEARS", {"name": enemies[0].display_name()})
	else:
		var tamer := tr(str(info.get("tamer_key", "BTL_TAMER_DEFAULT")))
		await _say("BTL_TAMER_CHALLENGE", {"tamer": tamer})
	for m in allies:
		var v := _view(m.uid)
		v.position = _slot_pos(m.side, engine.slot_of(m))
		v.enter(true)
		_place_panel(m)
	await _say("BTL_GO", {"name": " & ".join(allies.map(func(x: Monster) -> String: return x.display_name()))})


func _command_phase() -> void:
	_log.visible = false
	_actions = {}
	_cmd_units = engine.active_units(BattleEngine.PLAYER)
	_cmd_i = 0
	_refresh_timeline()
	_open_ring()
	while state != "done":
		await get_tree().process_frame
		if _ended:
			return
	state = "busy"
	_hide_menus()


func _refresh_timeline() -> void:
	_timeline.set_order(engine.predicted_order(_actions), views)
	_place_timeline()


func _current_unit() -> Monster:
	return _cmd_units[_cmd_i]


func _open_ring() -> void:
	_hide_menus()
	var m := _current_unit()
	for uid in views:
		views[uid].set_selected(false)
	var v := _view(m.uid)
	var disabled := {}
	if not engine.is_wild():
		disabled["flee"] = true
	if engine.reserves(BattleEngine.PLAYER).is_empty():
		disabled["switch"] = true
	if _battle_items().is_empty():
		disabled["items"] = true
	_ring.open_at(v.position + _field.position + Vector2(0, -36), disabled)
	_update_repeat_chip()
	state = "ring"


func _update_repeat_chip() -> void:
	_repeat.visible = _cmd_i == 0 and engine.round_no > 0 and _repeat_actions().size() == _cmd_units.size()
	(_repeat.get_node("L") as Label).text = tr("BTL_REPEAT")


func _hide_menus() -> void:
	_ring.visible = false
	_moves.visible = false
	_preview.visible = false
	_list_panel.visible = false
	_repeat.visible = false
	for uid in views:
		views[uid].set_selected(false)


func _next_unit() -> void:
	_refresh_timeline()
	_cmd_i += 1
	if _cmd_i >= _cmd_units.size():
		state = "done"
	else:
		_open_ring()


func _prev_unit() -> void:
	if _cmd_i == 0:
		return
	_cmd_i -= 1
	_actions.erase(_current_unit().uid)
	_refresh_timeline()
	Audio.sfx("cancel")
	_open_ring()


# ------------------------------------------------------------------ entrada
func _process(_delta: float) -> void:
	if state in ["ring", "moves", "target"]:
		var d := Vector2i(
			int(Input.is_action_pressed("move_right")) - int(Input.is_action_pressed("move_left")),
			int(Input.is_action_pressed("move_down")) - int(Input.is_action_pressed("move_up")))
		var now := Time.get_ticks_msec()
		if d != Vector2i.ZERO and d == _held and now >= _next_ms:
			_next_ms = now + 110
			_on_dir(d)
		_held = d


func _unhandled_input(event: InputEvent) -> void:
	if Game.top_overlay() != null:
		return
	if state == "busy" and (event.is_action_pressed("btn_a", false) or event.is_action_pressed("btn_b", false)):
		_log.skip()
		get_viewport().set_input_as_handled()
		return
	if not state in ["ring", "moves", "target"]:
		return
	for a in Controls.DIRS.keys():
		if event.is_action_pressed(a, false):
			get_viewport().set_input_as_handled()
			_held = Controls.DIRS[a]
			_next_ms = Time.get_ticks_msec() + 320
			_on_dir(Controls.DIRS[a])
			return
	if event.is_action_pressed("btn_a", false):
		get_viewport().set_input_as_handled()
		_on_confirm()
	elif event.is_action_pressed("btn_b", false):
		get_viewport().set_input_as_handled()
		_on_back()
	elif event.is_action_pressed("btn_menu", false) and state == "ring":
		get_viewport().set_input_as_handled()
		_repeat_last()


func _on_dir(d: Vector2i) -> void:
	match state:
		"ring":
			_ring.select_dir(d)
		"moves":
			_moves.move_cursor(d)
			_moves.update_preview(_first_target())
		"target":
			if _targets.size() > 1:
				_target_i = wrapi(_target_i + (1 if (d.x > 0 or d.y > 0) else -1), 0, _targets.size())
				Audio.sfx("cursor")
				_show_target()


func _on_confirm() -> void:
	match state:
		"ring":
			_ring.confirm()
		"moves":
			_choose_move()
		"target":
			_confirm_target()


func _on_back() -> void:
	match state:
		"ring":
			_prev_unit()
		"moves":
			Audio.sfx("cancel")
			_open_ring()
		"target":
			Audio.sfx("cancel")
			for uid in views:
				views[uid].set_selected(false)
			if _pending_item != "":
				_open_items()
			else:
				_open_moves()


# ------------------------------------------------------------------ anel
func _on_ring_chosen(id: String) -> void:
	if state != "ring":
		return
	match id:
		"moves":
			_open_moves()
		"items":
			_open_items()
		"switch":
			_open_switch(false)
		"flee":
			_actions[_current_unit().uid] = {"kind": "flee"}
			_next_unit()


func _open_moves() -> void:
	_hide_menus()
	_pending_item = ""
	_moves.open(_current_unit(), engine)
	_preview.visible = true
	_moves.update_preview(_first_target())
	_view(_current_unit().uid).set_selected(false)
	state = "moves"


func _first_target() -> Monster:
	var mv := engine.move_data(_moves.current_move())
	var t := engine.legal_targets(_current_unit(), str(mv.get("target", "enemy")))
	return t[0] if not t.is_empty() else null


func _on_move_tapped(i: int) -> void:
	if state != "moves":
		return
	if i == _moves.index:
		_choose_move()
	else:
		_moves.index = i
		_moves.move_cursor(Vector2i.ZERO)
		_moves.update_preview(_first_target())
		Audio.sfx("cursor")


func _choose_move() -> void:
	if not _moves.usable(_moves.index):
		Audio.sfx("bump")
		return
	Audio.sfx("confirm")
	var mid := _moves.current_move()
	var mv := engine.move_data(mid)
	var tk := str(mv.get("target", "enemy"))
	_targets = engine.legal_targets(_current_unit(), tk)
	if BattleEngine.target_needs_choice(tk) and _targets.size() > 1:
		_target_i = 0
		state = "target"
		_show_target()
		return
	_actions[_current_unit().uid] = {"kind": "move", "move": mid, "target": _targets[0].uid if not _targets.is_empty() else 0}
	_next_unit()


func _show_target() -> void:
	for uid in views:
		views[uid].set_selected(false)
	var t: Monster = _targets[_target_i]
	var v := _view(t.uid)
	if v:
		v.set_selected(true)
	if _pending_item == "":
		_moves.update_preview(t)


func _confirm_target() -> void:
	Audio.sfx("confirm")
	var t: Monster = _targets[_target_i]
	if _pending_item != "":
		_actions[_current_unit().uid] = {"kind": "item", "item": _pending_item, "target": t.uid}
		_pending_item = ""
	else:
		_actions[_current_unit().uid] = {"kind": "move", "move": _moves.current_move(), "target": t.uid}
	for uid in views:
		views[uid].set_selected(false)
	_next_unit()


## Toque num esqueleto durante a escolha de alvo: 1º toque marca, 2º confirma.
func _input(event: InputEvent) -> void:
	if state != "target" or not (event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT):
		return
	var pos: Vector2 = event.position
	for i in _targets.size():
		var v := _view(_targets[i].uid)
		if v and Rect2(v.global_position + Vector2(-26, -64), Vector2(52, 66)).has_point(pos):
			get_viewport().set_input_as_handled()
			if i == _target_i:
				_confirm_target()
			else:
				_target_i = i
				Audio.sfx("cursor")
				_show_target()
			return


# ------------------------------------------------------------------ listas
func _battle_items() -> Array:
	var out := []
	for id in engine.bag.keys():
		if int(engine.bag[id]) > 0 and bool(Data.item(id).get("battle", false)):
			out.append(id)
	out.sort()
	return out


func _open_list(mode: String, title_key: String, items: Array, forced: bool = false) -> void:
	_hide_menus()
	_list_mode = mode
	_list_title.text = tr(title_key)
	if not forced:
		items.append({"id": "_back", "key": "SET_BACK"})
	_list.set_items(items)
	_list_panel.visible = true
	_list_panel.reset_size()
	state = "list"


func _open_items() -> void:
	var items := []
	for id in _battle_items():
		var it := Data.item(id)
		items.append({"id": id, "key": str(it.get("name_key", id)), "value": func() -> String: return "x%d" % int(engine.bag.get(id, 0))})
	_open_list("items", "BTL_ITEMS_TITLE", items)


func _party_rows(filter: Callable) -> Array:
	var rows := []
	var team: Array = engine.teams[BattleEngine.PLAYER]
	for i in team.size():
		var m: Monster = team[i]
		rows.append({"id": str(i), "key": "", "suffix": "%s %s" % [m.display_name(), tr("BTL_LEVEL_SHORT").format({"n": m.level})],
			"value": func() -> String: return "%d/%d" % [m.hp, m.max_hp()], "enabled": filter.call(i, m)})
	return rows


func _open_switch(forced: bool) -> void:
	var rows := _party_rows(func(i: int, m: Monster) -> bool: return not m.is_fainted() and not engine.active[0].has(i))
	_open_list("switch_forced" if forced else "switch", "BTL_CHOOSE_REPLACEMENT" if forced else "BTL_SWITCH_TITLE", rows, forced)


func _on_list_activated(id: String) -> void:
	if id == "_back":
		Audio.sfx("cancel")
		_open_ring()
		return
	match _list_mode:
		"items":
			_pending_item = id
			var it := Data.item(id)
			var kind := str(it.get("target", "ally"))
			var rows := _party_rows(func(_i: int, m: Monster) -> bool:
				return m.is_fainted() if kind == "fainted_ally" else not m.is_fainted())
			_open_list("item_target", "BTL_ITEM_TARGET", rows)
		"item_target":
			var t: Monster = engine.teams[BattleEngine.PLAYER][int(id)]
			_actions[_current_unit().uid] = {"kind": "item", "item": _pending_item, "target": t.uid}
			_pending_item = ""
			_list_panel.visible = false
			_next_unit()
		"switch":
			_actions[_current_unit().uid] = {"kind": "switch", "to": int(id)}
			_list_panel.visible = false
			_next_unit()
		"switch_forced", "learn":
			if _list_cb.is_valid():
				var cb := _list_cb
				_list_cb = Callable()
				_list_panel.visible = false
				state = "busy"
				cb.call(id)


func _on_list_cancelled() -> void:
	match _list_mode:
		"items", "switch":
			_open_ring()
		"item_target":
			_open_items()
		"learn":
			_on_list_activated("-1")


# ------------------------------------------------------------------ repetir
func _repeat_actions() -> Dictionary:
	var last := engine.last_player_actions
	var out := {}
	for m in engine.active_units(BattleEngine.PLAYER):
		if not last.has(m.uid):
			return {}
		var a: Dictionary = last[m.uid]
		if a.get("kind") != "move":
			return {}
		var ok := false
		for mv in m.moves:
			if mv["id"] == a.get("move") and int(mv["pp"]) > 0:
				ok = true
		if not ok:
			return {}
		out[m.uid] = a.duplicate()
	return out


func _repeat_last() -> void:
	if state != "ring" or _cmd_i != 0:
		return
	var acts := _repeat_actions()
	if acts.is_empty() or acts.size() != _cmd_units.size():
		Audio.sfx("bump")
		return
	Audio.sfx("confirm")
	_actions = acts
	state = "done"


# ------------------------------------------------------------------ rodada
func _play_round() -> void:
	_hide_menus()
	var evs := engine.run_round(_actions)
	_log.visible = true
	_timeline.set_order(engine.predicted_order(_actions), views)
	for e in evs:
		await _play_event(e)
	for uid in panels:
		panels[uid].refresh()


func _play_event(e: Dictionary) -> void:
	match str(e.t):
		"move":
			_timeline.set_current(int(e.user))
			var mv := engine.move_data(str(e.move))
			var user := _view(int(e.user))
			await _say("BTL_USED", {"user": _name(int(e.user)), "move": tr(str(mv.get("name_key", "")))})
			if user and str(mv.get("category", "")) != "status":
				var foe_side := 1 - engine.find(int(e.user)).side
				var targets := engine.active_units(foe_side)
				if not targets.is_empty():
					await user.lunge(_view(targets[0].uid).global_position)
		"damage":
			var v := _view(int(e.target))
			if v:
				_burst(v.center(), _move_color_for(e))
				v.hurt()
				_float_number(v.center() - Vector2(0, 12), str(int(e.amount)), Color8(255, 240, 200))
			Audio.sfx("bump")
			await panels[int(e.target)].animate_hp(int(e.hp))
			if bool(e.get("crit", false)):
				await _say("BTL_CRIT")
			var eff := float(e.get("eff", 1.0))
			if eff > 1.01:
				await _say("BTL_EFF_STRONG_MSG")
			elif eff < 0.99:
				await _say("BTL_EFF_WEAK_MSG")
		"miss":
			await _say("BTL_MISS", {"user": _name(int(e.user))})
		"no_target":
			await _say("BTL_NO_TARGET")
		"poisoned":
			_burst(_view(int(e.target)).center(), Color8(170, 90, 210))
			panels[int(e.target)].refresh()
			await _say("BTL_POISONED", {"name": _name(int(e.target))})
		"already_poisoned":
			await _say("BTL_ALREADY_POISONED", {"name": _name(int(e.target))})
		"poison_tick":
			var v := _view(int(e.target))
			_bubbles(v.center())
			await panels[int(e.target)].animate_hp(int(e.hp), 0.35)
			await _say("BTL_POISON_TICK", {"name": _name(int(e.target))})
		"poison_end":
			panels[int(e.target)].refresh()
			await _say("BTL_POISON_END", {"name": _name(int(e.target))})
		"stat":
			var up := int(e.requested) > 0
			var key := ("BTL_STAT_UP" if up else "BTL_STAT_DOWN") if int(e.delta) != 0 else ("BTL_STAT_MAX" if up else "BTL_STAT_MIN")
			_arrows(_view(int(e.target)).center(), up)
			await _say(key, {"name": _name(int(e.target)), "stat": tr("STAT_" + str(e.stat).to_upper())})
		"heal":
			_sparkles(_view(int(e.target)).center())
			await panels[int(e.target)].animate_hp(int(e.hp))
			await _say("BTL_HEALED", {"name": _name(int(e.target)), "n": int(e.amount)})
		"cured":
			panels[int(e.target)].refresh()
			await _say("BTL_CURED", {"name": _name(int(e.target))})
		"revived":
			panels[int(e.target)].shown_hp = 0
			await panels[int(e.target)].animate_hp(int(e.hp))
			await _say("BTL_REVIVED", {"name": _name(int(e.target))})
		"item":
			_timeline.set_current(int(e.user))
			await _say("BTL_ITEM_USED", {"item": tr(str(Data.item(str(e.item)).get("name_key", ""))), "name": _name(int(e.target))})
		"item_fail":
			await _say("BTL_NO_ITEMS")
		"switch_out":
			var v := _view(int(e.target))
			if int(e.side) == BattleEngine.PLAYER:
				await _say("BTL_COME_BACK", {"name": _name(int(e.target))})
			if v and v.visible:
				await v.leave(int(e.side) == BattleEngine.PLAYER)
			panels[int(e.target)].visible = false
		"switch_in":
			var m := engine.find(int(e.target))
			var v := _view(m.uid)
			v.position = _slot_pos(m.side, int(e.slot))
			v.modulate.a = 1.0
			if m.side == BattleEngine.ENEMY and not engine.is_wild():
				await _say("BTL_TAMER_SENDS", {"tamer": tr(str(info.get("tamer_key", "BTL_TAMER_DEFAULT"))), "name": m.display_name()})
			elif m.side == BattleEngine.PLAYER:
				await _say("BTL_GO", {"name": m.display_name()})
			panels[m.uid].bind(m)
			_place_panel(m)
			await v.enter(m.side == BattleEngine.PLAYER)
		"faint":
			var v := _view(int(e.target))
			Audio.sfx("cancel")
			if v:
				await v.faint()
			panels[int(e.target)].visible = false
			await _say("BTL_FAINT", {"name": _name(int(e.target))})
		"xp":
			var m := engine.find(int(e.target))
			await _say("BTL_XP", {"name": m.display_name(), "n": int(e.amount)})
			for lvl in e.get("levels", []):
				Audio.sfx("save")
				if _view(m.uid).visible:
					_sparkles(_view(m.uid).center())
				await _say("BTL_LEVEL_UP", {"name": m.display_name(), "n": int(lvl)})
			panels[m.uid].refresh()
		"learned":
			await _say("BTL_LEARNED", {"name": _name(int(e.target)), "move": tr(str(Data.move(str(e.move)).get("name_key", "")))})
		"learn_prompt":
			await _learn_prompt(engine.find(int(e.target)), str(e.move))
		"fled":
			await _say("BTL_FLED")
		"flee_failed":
			await _say("BTL_FLEE_FAILED")
		"cant_flee":
			await _say("BTL_CANT_FLEE")


func _move_color_for(e: Dictionary) -> Color:
	var user := engine.find(int(e.get("user", 0)))
	match user.type() if user else "":
		"magico":
			return Color8(170, 120, 255)
		"veneno":
			return Color8(170, 90, 210)
		"cura":
			return Color8(110, 220, 130)
	return Color8(255, 236, 200)


func _learn_prompt(m: Monster, move_id: String) -> void:
	var mv_name := tr(str(Data.move(move_id).get("name_key", "")))
	await _say("BTL_LEARN_PROMPT", {"name": m.display_name(), "move": mv_name})
	var rows := []
	for i in m.moves.size():
		rows.append({"id": str(i), "key": str(Data.move(str(m.moves[i]["id"])).get("name_key", ""))})
	rows.append({"id": "-1", "key": "BTL_LEARN_GIVE_UP"})
	var done := [false]
	_list_cb = func(id: String) -> void:
		var idx := int(id)
		if idx >= 0:
			BattleEngine.learn_move(m, move_id, idx)
		done[0] = idx
	_open_list("learn", "BTL_LEARN_TITLE", rows, true)
	while typeof(done[0]) == TYPE_BOOL:
		await get_tree().process_frame
	if int(done[0]) >= 0:
		await _say("BTL_LEARNED", {"name": m.display_name(), "move": mv_name})
	else:
		await _say("BTL_DID_NOT_LEARN", {"name": m.display_name(), "move": mv_name})


func _replacements() -> void:
	for slot in engine.pending_replacements():
		var chosen := [-1]
		_list_cb = func(id: String) -> void: chosen[0] = int(id)
		_open_switch(true)
		while chosen[0] < 0:
			await get_tree().process_frame
		engine.events = []
		engine.switch_in(BattleEngine.PLAYER, slot, chosen[0])
		_log.visible = true
		for e in engine.events:
			await _play_event(e)
	# reposiciona quem ficou sozinho/em dupla
	for side in 2:
		for m in engine.active_units(side):
			var v := _view(m.uid)
			var target := _slot_pos(side, engine.slot_of(m))
			if v.position != target:
				var tw := create_tween()
				tw.tween_property(v, "position", target, 0.25)
			_place_panel(m)


func _finish() -> void:
	_ended = true
	match engine.result:
		"win":
			Audio.sfx("save")
			await _say("BTL_WIN")
			var reward := int(info.get("reward", 0))
			if reward > 0:
				SaveGame.data["money"] = int(SaveGame.data.get("money", 0)) + reward
				await _say("BTL_MONEY", {"n": reward})
		"lose":
			await _say("BTL_LOSE")
	finished.emit(engine.result)


## Vence na hora (menu de debug).
func debug_win() -> void:
	for m in engine.teams[BattleEngine.ENEMY]:
		m.hp = 0
	engine.result = "win"
	state = "busy"
	_hide_menus()
	if not _ended:
		_log.visible = true
		await _finish()


var _debug_taps: Array[int] = []


## Três toques na timeline abrem o menu de debug (só em build de debug).
func _on_timeline_input(event: InputEvent) -> void:
	if not (event is InputEventMouseButton and event.pressed):
		return
	var now := Time.get_ticks_msec()
	_debug_taps.append(now)
	_debug_taps = _debug_taps.filter(func(t: int) -> bool: return now - t <= 1200)
	if _debug_taps.size() >= 3:
		_debug_taps.clear()
		Game.open_debug()


# ------------------------------------------------------------------ efeitos
func _particles(at: Vector2, color: Color, amount: int, speed: float, gravity: Vector2, tex: String = "dot") -> void:
	var p := CPUParticles2D.new()
	p.texture = load("res://assets/ui/particle_%s.png" % tex)
	p.one_shot = true
	p.explosiveness = 0.9
	p.amount = amount
	p.lifetime = 0.55
	p.spread = 180.0
	p.initial_velocity_min = speed * 0.5
	p.initial_velocity_max = speed
	p.gravity = gravity
	p.scale_amount_min = 1.0
	p.scale_amount_max = 2.0
	p.color = color
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1, 1, 1, 1))
	ramp.set_color(1, Color(1, 1, 1, 0))
	p.color_ramp = ramp
	p.global_position = at
	_root.add_child(p)
	p.emitting = true
	get_tree().create_timer(1.2).timeout.connect(p.queue_free)


func _burst(at: Vector2, color: Color) -> void:
	_particles(at, color, 14, 70.0, Vector2(0, 60))


func _bubbles(at: Vector2) -> void:
	_particles(at + Vector2(0, 10), Color8(170, 90, 210), 10, 25.0, Vector2(0, -60))


func _sparkles(at: Vector2) -> void:
	_particles(at, Color8(140, 255, 160), 12, 30.0, Vector2(0, -40), "sparkle")


func _arrows(at: Vector2, up: bool) -> void:
	_particles(at, Color8(255, 210, 90) if up else Color8(120, 160, 255), 10, 20.0, Vector2(0, -70 if up else 70))


func _float_number(at: Vector2, text: String, color: Color) -> void:
	var l := UiTheme.label(text, color)
	l.add_theme_color_override("font_outline_color", Color8(40, 30, 48))
	l.add_theme_constant_override("outline_size", 2)
	l.position = at - Vector2(UiTheme.text_width(text) / 2.0, 0)
	_root.add_child(l)
	var tw := create_tween().set_parallel(true)
	tw.tween_property(l, "position:y", l.position.y - 14, 0.6).set_ease(Tween.EASE_OUT)
	tw.tween_property(l, "modulate:a", 0.0, 0.6).set_delay(0.25)
	tw.chain().tween_callback(l.queue_free)
