class_name BattleScreen
extends CanvasLayer
## Batalha 2×2 com turnos por tempo, numa arena lateral:
##   topo: timeline das próximas 8 ações (Sintonia = elo ciano; fantasma =
##         onde cai o próximo turno de quem está escolhendo);
##   faixa: mensagens e detalhes do golpe;
##   arena: aliados à esquerda, inimigos à direita (menu em anel em quem age,
##          golpes no centro, etiquetas Forte/Normal/Fraco sobre os inimigos);
##   base: cartas com nome, idade e PV.
## Controles: D-pad/teclado/gamepad e toque em tudo. MENU repete a última ação
## de quem está agindo.

signal finished(result: String)

const ALLY_POS := [Vector2(98, 118), Vector2(58, 134)]
const ALLY_SINGLE := Vector2(78, 126)
const ENEMY_POS := [Vector2(222, 118), Vector2(262, 134)]
const ENEMY_SINGLE := Vector2(242, 126)
const RIBBON_POS := Vector2(40, 22)
const RIBBON_SIZE := Vector2(240, 34)

var engine: BattleEngine
var info: Dictionary = {}
var views := {}
var cards := {}
var state := "busy"

var _root: Control
var _field: Node2D
var _bg: Sprite2D
var _ox := 0.0
var _timeline: TimelineBar
var _ring: RingMenu
var _log: BattleLog
var _detail: PanelContainer
var _detail_label: Label
var _moves: MoveList
var _list_panel: PanelContainer
var _list_title: Label
var _list: MenuList
var _repeat: PanelContainer
var _tags := {}
var _actor: Monster
var _chosen: Dictionary = {}
var _targets: Array = []
var _target_i := 0
var _pending_item := ""
var _list_mode := ""
var _list_cb: Callable
var _held := Vector2i.ZERO
var _next_ms := 0
var _ended := false
var _debug_taps: Array[int] = []
## Recrutas aceitos nesta batalha (o Game coloca na equipe ou no Rancho).
var recruits: Array = []


## info: {"kind": "wild"|"tamer"|"boss", "enemies": [[species, idade, golden?], ...],
##        "tamer_key": chave do nome, "reward": moedas, "seed": opcional}
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
	_build_ui()
	get_viewport().size_changed.connect(_layout)
	_spawn_units()
	_layout()
	_run()


# ------------------------------------------------------------------ construção
func _build_ui() -> void:
	_timeline = TimelineBar.new()
	_timeline.mouse_filter = Control.MOUSE_FILTER_STOP
	_timeline.gui_input.connect(_on_timeline_input)
	_root.add_child(_timeline)
	_log = BattleLog.new()
	_log.visible = false
	_root.add_child(_log)
	_detail = PanelContainer.new()
	_detail.add_theme_stylebox_override("panel", UiTheme.frame("dark"))
	_detail.visible = false
	_detail_label = UiTheme.label("", UiTheme.TEXT_LIGHT)
	_detail_label.custom_minimum_size = Vector2(BattleLog.TEXT_WIDTH, 24)
	_detail.add_child(_detail_label)
	_root.add_child(_detail)
	_moves = MoveList.new()
	_moves.visible = false
	_moves.tapped.connect(_on_move_tapped)
	_root.add_child(_moves)
	_ring = RingMenu.new()
	_ring.visible = false
	_ring.chosen.connect(_on_ring_chosen)
	_root.add_child(_ring)
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
	for p in [_log, _detail]:
		p.position = Vector2(_ox, 0) + RIBBON_POS
		p.custom_minimum_size = RIBBON_SIZE
		p.size = RIBBON_SIZE
	_moves.position = Vector2(_ox + 44, 64)
	_list_panel.position = Vector2(_ox + 62, 30)
	_repeat.position = Vector2(_ox + 2, 124)
	_place_timeline()
	for uid in cards.keys():
		_place_card(engine.find(uid))


func _place_timeline() -> void:
	var vp := get_viewport().get_visible_rect().size
	_timeline.position = Vector2(floorf((vp.x - _timeline.size.x) / 2.0), 1)


func _slot_pos(side: int, slot: int) -> Vector2:
	var count: int = engine.active[side].filter(func(i: int) -> bool: return i >= 0).size()
	if side == BattleEngine.ENEMY:
		return ENEMY_SINGLE if count <= 1 and slot == 0 else ENEMY_POS[slot]
	return ALLY_SINGLE if count <= 1 and slot == 0 else ALLY_POS[slot]


func _place_card(m: Monster) -> void:
	if m == null or not cards.has(m.uid):
		return
	var c: UnitCard = cards[m.uid]
	var slot := engine.slot_of(m)
	if slot < 0:
		c.visible = false
		return
	c.visible = true
	var x := 2.0 + slot * (UnitCard.W + 1) if m.side == BattleEngine.PLAYER else 320.0 - 2.0 - (2 - slot) * (UnitCard.W + 1) + 1
	c.position = Vector2(_ox + x, 180 - UnitCard.H)


func _spawn_units() -> void:
	for side in 2:
		for m in engine.teams[side]:
			var v := UnitView.new().setup(m, side == BattleEngine.ENEMY)
			v.visible = false
			_field.add_child(v)
			views[m.uid] = v
			var c := UnitCard.new().setup(m, side == BattleEngine.PLAYER)
			c.visible = false
			_root.add_child(c)
			cards[m.uid] = c
	for c in [_moves, _ring, _list_panel, _repeat]:
		_root.move_child(c, -1)


func _view(uid: int) -> UnitView:
	return views.get(uid)


func _name(uid: int) -> String:
	var m := engine.find(uid)
	return m.display_name() if m else "?"


func _say(key: String, args: Dictionary = {}) -> void:
	_detail.visible = false
	await _log.say(tr(key).format(args))


# ------------------------------------------------------------------ fluxo
func _run() -> void:
	Audio.sfx("menu_open")
	await _intro()
	while not _ended:
		var actor := engine.next_actor()
		if actor == null:
			break
		_refresh_timeline()
		_mark_actor(actor)
		var evs: Array
		if actor.side == BattleEngine.PLAYER:
			var action: Dictionary = await _choose_action(actor)
			if _ended:
				break
			evs = engine.act(action)
		else:
			await get_tree().create_timer(0.25).timeout
			evs = engine.act_enemy()
		_log.visible = true
		for e in evs:
			await _play_event(e)
		_mark_actor(null)
		for uid in cards:
			cards[uid].refresh()
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
	for m in engine.teams[BattleEngine.ENEMY]:
		Ossuary.mark_seen(m)
		if engine.is_wild():
			cards[m.uid].marker = int(Ossuary.entry(m.species_id).get("marker", 0))
	for m in enemies:
		_place_card(m)
	if enemies.any(func(x: Monster) -> bool: return x.golden):
		Audio.sfx("golden")
		await _say("BTL_GOLDEN_APPEARS")
	if engine.is_wild():
		if enemies.size() > 1:
			await _say("BTL_WILD_APPEARS_2", {"a": enemies[0].display_name(), "b": enemies[1].display_name()})
		else:
			await _say("BTL_WILD_APPEARS", {"name": enemies[0].display_name()})
	else:
		await _say("BTL_TAMER_CHALLENGE", {"tamer": tr(str(info.get("tamer_key", "BTL_TAMER_DEFAULT")))})
	for m in allies:
		var v := _view(m.uid)
		v.position = _slot_pos(m.side, engine.slot_of(m))
		v.enter(true)
		_place_card(m)
	await _say("BTL_GO", {"name": " & ".join(allies.map(func(x: Monster) -> String: return x.display_name()))})


func _refresh_timeline(ghost_weight: float = -1.0) -> void:
	var override := {}
	var ghost := -1
	if ghost_weight > 0.0 and _actor:
		override[_actor.uid] = ghost_weight
		ghost = _actor.uid
	_timeline.set_order(engine.predict(int(engine.rules.get("timing", {}).get("preview", 8)), override), views, ghost)
	_place_timeline()


func _mark_actor(m: Monster) -> void:
	for uid in cards:
		cards[uid].set_acting(m != null and uid == m.uid, m != null and engine.sintonia_for(m))


func _choose_action(actor: Monster) -> Dictionary:
	_actor = actor
	_chosen = {}
	_open_ring()
	if engine.sintonia_for(actor):
		_show_detail(tr("BTL_SINTONIA_READY").format({"name": actor.display_name()}))
	while _chosen.is_empty() and not _ended:
		await get_tree().process_frame
	_hide_menus()
	state = "busy"
	return _chosen


func _choose(action: Dictionary) -> void:
	_chosen = action


func _open_ring() -> void:
	_hide_menus()
	var v := _view(_actor.uid)
	var disabled := {}
	if not engine.is_wild():
		disabled["flee"] = true
	if engine.reserves(BattleEngine.PLAYER).is_empty():
		disabled["switch"] = true
	if _battle_items().is_empty():
		disabled["items"] = true
	_ring.open_at(v.position + _field.position + Vector2(0, -34), disabled)
	_repeat.visible = not _repeat_action().is_empty()
	(_repeat.get_node("L") as Label).text = tr("BTL_REPEAT")
	_refresh_timeline()
	state = "ring"


func _hide_menus() -> void:
	_ring.visible = false
	_moves.visible = false
	_detail.visible = false
	_list_panel.visible = false
	_repeat.visible = false
	_clear_tags()
	for uid in views:
		views[uid].set_selected(false)


func _show_detail(text: String) -> void:
	_log.visible = false
	_detail.visible = true
	_detail_label.text = "\n".join(TextFit.wrap_lines(text, BattleLog.TEXT_WIDTH).slice(0, 2))


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
			if d.y != 0:
				_moves.move_cursor(d.y)
				_update_move_detail()
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


# ------------------------------------------------------------------ anel e golpes
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
			_choose({"kind": "flee"})


func _open_moves() -> void:
	_hide_menus()
	_pending_item = ""
	_moves.open(_actor, engine)
	_update_move_detail()
	state = "moves"


## Detalhes do golpe na faixa, etiquetas de efetividade sobre os alvos e
## fantasma na timeline mostrando quando quem escolhe vai agir de novo.
func _update_move_detail() -> void:
	var mid := _moves.current_move()
	var mv := engine.move_data(mid)
	var t := str(mv.get("type", ""))
	var power := int(mv.get("power", 0))
	var line1 := tr("BTL_DETAIL").format({
		"type": tr("TYPE_" + t.to_upper()) if t != "" else "—",
		"p": power if power > 0 else "—",
		"acc": int(mv.get("accuracy", 100)),
		"weight": tr("BTL_WEIGHT_" + str(mv.get("weight", "normal")).to_upper())})
	var line2 := "%s · %s" % [tr("BTL_TARGET_" + str(mv.get("target", "enemy")).to_upper()), tr(str(mv.get("desc_key", "")))]
	_show_detail(line1 + "\n" + line2)
	_show_tags(mv)
	_refresh_timeline(engine.move_weight(mid))


func _show_tags(mv: Dictionary) -> void:
	_clear_tags()
	var foes := str(mv.get("target", "enemy")) in ["enemy", "all_enemies"]
	if not foes or int(mv.get("power", 0)) <= 0:
		return
	for m in engine.active_units(BattleEngine.ENEMY):
		var mult := engine.effectiveness(str(mv.get("type", "")), m.type())
		var tag := PanelContainer.new()
		tag.add_theme_stylebox_override("panel", UiTheme.frame("dark"))
		var l := UiTheme.label(tr(BattleEngine.effectiveness_label(mult)),
			Color8(110, 230, 120) if mult > 1.01 else (Color8(255, 120, 110) if mult < 0.99 else UiTheme.TEXT_LIGHT))
		tag.add_child(l)
		_root.add_child(tag)
		tag.reset_size()
		var v := _view(m.uid)
		tag.position = v.position + _field.position + Vector2(-tag.size.x / 2.0, -10)
		_tags[m.uid] = tag


func _clear_tags() -> void:
	for t in _tags.values():
		t.queue_free()
	_tags = {}


func _on_move_tapped(i: int) -> void:
	if state != "moves":
		return
	if i == _moves.index:
		_choose_move()
	else:
		_moves.index = i
		_moves.move_cursor(0)
		_update_move_detail()
		Audio.sfx("cursor")


func _choose_move() -> void:
	if not _moves.usable(_moves.index):
		Audio.sfx("bump")
		return
	Audio.sfx("confirm")
	var mid := _moves.current_move()
	var tk := str(engine.move_data(mid).get("target", "enemy"))
	_targets = engine.legal_targets(_actor, tk)
	if BattleEngine.target_needs_choice(tk) and _targets.size() > 1:
		_target_i = 0
		_moves.visible = false
		state = "target"
		_show_target()
		return
	_choose({"kind": "move", "move": mid, "target": _targets[0].uid if not _targets.is_empty() else 0})


func _show_target() -> void:
	for uid in views:
		views[uid].set_selected(false)
	var t: Monster = _targets[_target_i]
	var v := _view(t.uid)
	if v:
		v.set_selected(true)


func _confirm_target() -> void:
	Audio.sfx("confirm")
	var t: Monster = _targets[_target_i]
	if _pending_item != "":
		_choose({"kind": "item", "item": _pending_item, "target": t.uid})
		_pending_item = ""
	else:
		_choose({"kind": "move", "move": _moves.current_move(), "target": t.uid})


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
		rows.append({"id": str(i), "key": "", "suffix": "%s · %s" % [m.display_name(), UnitCard.age_text(m.level)],
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
			var kind := str(Data.item(id).get("target", "ally"))
			var rows := _party_rows(func(_i: int, m: Monster) -> bool:
				return m.is_fainted() if kind == "fainted_ally" else not m.is_fainted())
			_open_list("item_target", "BTL_ITEM_TARGET", rows)
		"item_target":
			var t: Monster = engine.teams[BattleEngine.PLAYER][int(id)]
			_list_panel.visible = false
			_choose({"kind": "item", "item": _pending_item, "target": t.uid})
			_pending_item = ""
		"switch":
			_list_panel.visible = false
			_choose({"kind": "switch", "to": int(id)})
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
func _repeat_action() -> Dictionary:
	if _actor == null or not engine.last_actions.has(_actor.uid):
		return {}
	var a: Dictionary = engine.last_actions[_actor.uid]
	if a.get("kind") != "move":
		return {}
	for mv in _actor.moves:
		if mv["id"] == a.get("move") and int(mv["pp"]) > 0:
			return a.duplicate()
	return {}


func _repeat_last() -> void:
	if state != "ring":
		return
	var a := _repeat_action()
	if a.is_empty():
		Audio.sfx("bump")
		return
	Audio.sfx("confirm")
	_choose(a)


# ------------------------------------------------------------------ eventos
func _play_event(e: Dictionary) -> void:
	match str(e.t):
		"turn":
			if bool(e.get("sintonia", false)):
				_sparkles(_view(int(e.user)).center())
				await _say("BTL_SINTONIA", {"name": _name(int(e.user))})
		"move":
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
			await cards[int(e.target)].animate_hp(int(e.hp))
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
		"delayed":
			_arrows(_view(int(e.target)).center(), false)
			_refresh_timeline()
			await _say("BTL_DELAYED", {"name": _name(int(e.target))})
		"poisoned":
			_burst(_view(int(e.target)).center(), Color8(170, 90, 210))
			cards[int(e.target)].refresh()
			await _say("BTL_POISONED", {"name": _name(int(e.target))})
		"already_poisoned":
			await _say("BTL_ALREADY_POISONED", {"name": _name(int(e.target))})
		"poison_tick":
			_bubbles(_view(int(e.target)).center())
			await cards[int(e.target)].animate_hp(int(e.hp), 0.35)
			await _say("BTL_POISON_TICK", {"name": _name(int(e.target))})
		"poison_end":
			cards[int(e.target)].refresh()
			await _say("BTL_POISON_END", {"name": _name(int(e.target))})
		"stat":
			var up := int(e.requested) > 0
			var key := ("BTL_STAT_UP" if up else "BTL_STAT_DOWN") if int(e.delta) != 0 else ("BTL_STAT_MAX" if up else "BTL_STAT_MIN")
			_arrows(_view(int(e.target)).center(), up)
			if str(e.stat) == "spd":
				_refresh_timeline()
			await _say(key, {"name": _name(int(e.target)), "stat": tr("STAT_" + str(e.stat).to_upper())})
		"heal":
			_sparkles(_view(int(e.target)).center())
			await cards[int(e.target)].animate_hp(int(e.hp))
			await _say("BTL_HEALED", {"name": _name(int(e.target)), "n": int(e.amount)})
		"cured":
			cards[int(e.target)].refresh()
			await _say("BTL_CURED", {"name": _name(int(e.target))})
		"revived":
			cards[int(e.target)].shown_hp = 0
			await cards[int(e.target)].animate_hp(int(e.hp))
			await _say("BTL_REVIVED", {"name": _name(int(e.target))})
		"item":
			await _say("BTL_ITEM_USED", {"item": tr(str(Data.item(str(e.item)).get("name_key", ""))), "name": _name(int(e.target))})
		"item_fail":
			await _say("BTL_NO_ITEMS")
		"switch_out":
			var v := _view(int(e.target))
			if int(e.side) == BattleEngine.PLAYER:
				await _say("BTL_COME_BACK", {"name": _name(int(e.target))})
			if v and v.visible:
				await v.leave(int(e.side) == BattleEngine.PLAYER)
			cards[int(e.target)].visible = false
		"switch_in":
			var m := engine.find(int(e.target))
			var v := _view(m.uid)
			v.position = _slot_pos(m.side, int(e.slot))
			v.modulate.a = 1.0
			if m.side == BattleEngine.ENEMY and not engine.is_wild():
				await _say("BTL_TAMER_SENDS", {"tamer": tr(str(info.get("tamer_key", "BTL_TAMER_DEFAULT"))), "name": m.display_name()})
			elif m.side == BattleEngine.PLAYER:
				await _say("BTL_GO", {"name": m.display_name()})
			cards[m.uid].bind(m)
			_place_card(m)
			await v.enter(m.side == BattleEngine.PLAYER)
			_refresh_timeline()
		"faint":
			var v := _view(int(e.target))
			Audio.sfx("cancel")
			if v:
				await v.faint()
			cards[int(e.target)].visible = false
			await _say("BTL_FAINT", {"name": _name(int(e.target))})
		"xp":
			var m := engine.find(int(e.target))
			await _say("BTL_XP", {"name": m.display_name(), "n": int(e.amount)})
			for lvl in e.get("levels", []):
				Audio.sfx("save")
				if _view(m.uid).visible:
					_confetti(_view(m.uid).center())
				await _say("BTL_LEVEL_UP", {"name": m.display_name(), "n": int(lvl)})
			cards[m.uid].refresh()
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
	for side in 2:
		for m in engine.active_units(side):
			var v := _view(m.uid)
			var target := _slot_pos(side, engine.slot_of(m))
			if v.position != target:
				var tw := create_tween()
				tw.tween_property(v, "position", target, 0.25)
			_place_card(m)


func _finish() -> void:
	# debug_win pode chegar com uma ação no meio: só termina uma vez
	if _ended:
		return
	_ended = true
	_hide_menus()
	match engine.result:
		"win":
			Audio.sfx("save")
			await _say("BTL_WIN")
			var reward := int(info.get("reward", 0))
			if reward > 0:
				SaveGame.data["money"] = int(SaveGame.data.get("money", 0)) + reward
				await _say("BTL_MONEY", {"n": reward})
			if engine.is_wild():
				await _markers_and_recruits()
			else:
				for m in engine.teams[BattleEngine.ENEMY]:
					Ossuary.entry(m.species_id)["defeated"] = true
		"lose":
			await _say("BTL_LOSE")
	finished.emit(engine.result)


func _party_level() -> float:
	var team: Array = engine.teams[BattleEngine.PLAYER]
	var total := 0.0
	for m in team:
		total += m.level
	return total / maxf(1.0, team.size())


## Marcador de ossos de cada espécie derrotada e pedido para entrar em 100%.
func _markers_and_recruits() -> void:
	var party_size: int = engine.teams[BattleEngine.PLAYER].size()
	for m in engine.teams[BattleEngine.ENEMY]:
		if not m.is_fainted():
			continue
		var r := Ossuary.register_win(m, _party_level())
		await _say("RECRUIT_MARKER", {"name": tr(str(m.info().get("name_key", ""))), "a": r.before, "b": r.after})
		if not r.offer:
			continue
		Audio.sfx("recruit")
		var preview := Monster.create(r.species, int(r.level), bool(r.golden))
		var answer := await ChoiceBox.ask("RECRUIT_ASK", ["RECRUIT_ACCEPT", "RECRUIT_REFUSE"], {"name": preview.display_name()})
		if answer == 0:
			var rec := Ossuary.accept(r.species, int(r.level))
			recruits.append(rec)
			var to_party := party_size + recruits.size() <= int(engine.rules.get("party_size", 4))
			await _say("RECRUIT_JOINED" if to_party else "RECRUIT_TO_RANCH", {"name": rec.display_name()})
		else:
			Ossuary.refuse(r.species)
			await _say("RECRUIT_REFUSED", {"name": preview.display_name()})


## Vence na hora (menu de debug).
## Dá a XP normal dos inimigos (para testar aniversários e crescimento).
func debug_win() -> void:
	if _ended:
		return
	engine.events = []
	for m in engine.teams[BattleEngine.ENEMY]:
		if not m.is_fainted():
			m.hp = 0
			engine._award_xp(m)
	var evs: Array = engine.events
	engine.events = []
	engine.result = "win"
	_hide_menus()
	state = "busy"
	_log.visible = true
	for e in evs:
		await _play_event(e)
	await _finish()


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
	_particles(at, Color8(140, 255, 220), 12, 30.0, Vector2(0, -40), "sparkle")


func _confetti(at: Vector2) -> void:
	for c in [Color8(255, 120, 140), Color8(255, 220, 90), Color8(120, 200, 255), Color8(150, 240, 140)]:
		_particles(at - Vector2(0, 20), c, 6, 60.0, Vector2(0, 90))


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
