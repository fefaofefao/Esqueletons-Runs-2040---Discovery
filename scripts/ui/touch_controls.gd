class_name TouchControls
extends Control
## Controles virtuais: D-pad (4 direções) à esquerda, A e B à direita, MENU e 2x
## no topo. Multitoque, deslizar no D-pad troca a direção. Os botões viram
## InputEventAction, então o resto do jogo não distingue toque de teclado/gamepad.
## Área mínima de 48dp garantida pela escala (ver _layout).

signal layout_changed

const ALPHA_IDLE := 0.5
const ALPHA_PRESSED := 0.9
const MIN_DP := 48.0
const MARGIN := 6.0

var world_mode := false
## Na batalha tudo é tocável: some o D-pad e o A/B, ficam MENU (repetir) e 2x.
var battle_mode := false
var ui_scale := 1

var _dpad: TextureRect
var _glow: TextureRect
var _a: TextureRect
var _b: TextureRect
var _menu: TextureRect
var _speed: TextureRect
var _tex := {}
## índice do toque -> ação ("move_up", "btn_a"...)
var _touches := {}
var _pressed := {}


func _init() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func _ready() -> void:
	for n in ["dpad", "dpad_glow", "btn_a", "btn_a_pressed", "btn_b", "btn_b_pressed", "btn_menu", "btn_speed_1x", "btn_speed_2x"]:
		_tex[n] = load("res://assets/ui/%s.png" % n)
	_dpad = _rect("dpad")
	_glow = _rect("dpad_glow")
	_glow.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_a = _rect("btn_a")
	_b = _rect("btn_b")
	_menu = _rect("btn_menu")
	_speed = _rect("btn_speed_1x")
	_menu.gui_input.connect(_on_top_button.bind("btn_menu"))
	_speed.gui_input.connect(_on_top_button.bind("btn_speed"))
	Controls.input_mode_changed.connect(func(_t: bool) -> void: _refresh_visibility())
	Settings.changed.connect(func(k: String) -> void:
		if k == "touch_controls":
			_refresh_visibility()
	)
	Speed.changed.connect(func(_m: float) -> void: _update_speed_icon())
	get_viewport().size_changed.connect(_layout)
	_layout()
	_update_speed_icon()
	_refresh_visibility()


func _rect(tex_name: String) -> TextureRect:
	var r := TextureRect.new()
	r.texture = _tex[tex_name]
	r.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	r.stretch_mode = TextureRect.STRETCH_SCALE
	r.mouse_filter = Control.MOUSE_FILTER_STOP
	r.modulate.a = ALPHA_IDLE
	add_child(r)
	return r


func set_world_mode(value: bool) -> void:
	world_mode = value
	_refresh_visibility()


func set_battle_mode(value: bool) -> void:
	battle_mode = value
	_refresh_visibility()


func pad_visible() -> bool:
	return _dpad != null and _dpad.visible


func _want_pad() -> bool:
	match str(Settings.get_value("touch_controls")):
		"on":
			return true
		"off":
			return false
	return Controls.touch_mode


func _refresh_visibility() -> void:
	if _dpad == null:
		return
	var pad := world_mode and _want_pad() and not battle_mode
	for n in [_dpad, _a, _b]:
		n.visible = pad
	_glow.visible = false
	_menu.visible = world_mode
	_speed.visible = world_mode
	if not pad:
		_release_all()
	layout_changed.emit()


## Quantos pixels de base são necessários para 48dp nesta tela.
func required_base_px() -> float:
	return base_px_for_48dp(float(DisplayServer.screen_get_dpi()), DisplayServer.window_get_size().y, get_viewport_rect().size.y)


## 48dp em pixels físicos = 48 * dpi / 160; dividido pela escala inteira da tela.
static func base_px_for_48dp(dpi: float, window_height: int, viewport_height: float) -> float:
	var screen_scale := maxf(floorf(float(window_height) / maxf(viewport_height, 1.0)), 1.0)
	return MIN_DP * dpi / 160.0 / screen_scale


func _layout() -> void:
	if _dpad == null:
		return
	var vp := get_viewport_rect().size
	# O braço do D-pad tem 24 px de base e os botões 30 px. Com a escala inteira
	# (180 px de altura), 24 px de base passam de 48dp em telas de celular e tablet.
	ui_scale = 1
	if required_base_px() > 24.5 and DisplayServer.get_name() != "headless":
		push_warning("TouchControls: tela pede %.1f px de base para 48dp" % required_base_px())
	var s := float(ui_scale)
	var safe := _safe_insets(vp)
	for r in [_dpad, _glow, _a, _b, _menu, _speed]:
		r.size = (r.texture as Texture2D).get_size() * s
	_dpad.position = Vector2(safe.x + MARGIN, vp.y - _dpad.size.y - MARGIN)
	_a.position = Vector2(vp.x - safe.y - MARGIN - _a.size.x, vp.y - _a.size.y - MARGIN - 20 * s)
	_b.position = Vector2(_a.position.x - _b.size.x - 2 * s, vp.y - _b.size.y - MARGIN)
	_menu.position = Vector2(safe.x + 4, 3)
	_speed.position = Vector2(vp.x - safe.y - 4 - _speed.size.x, 3)
	layout_changed.emit()


## Recuos (esquerda, direita) do recorte da tela, em pixels de base.
func _safe_insets(vp: Vector2) -> Vector2:
	if not OS.has_feature("mobile"):
		return Vector2.ZERO
	var win := DisplayServer.window_get_size()
	var safe := DisplayServer.get_display_safe_area()
	var k := vp.x / maxf(float(win.x), 1.0)
	var left := float(safe.position.x) * k
	var right := float(win.x - safe.end.x) * k
	return Vector2(clampf(left, 0, 40), clampf(right, 0, 40))


func _input(event: InputEvent) -> void:
	if not pad_visible():
		return
	# No celular, o Android também gera um clique de mouse "emulado" para cada
	# toque. Se o toque foi num botão virtual (A, B, D-pad), esse clique não pode
	# chegar aos menus/diálogos que estão por baixo do botão: senão o mesmo toque
	# conta duas vezes (fecha o diálogo e, no mapa, o A abre a conversa de novo).
	if (event is InputEventMouseButton or event is InputEventMouseMotion) and event.device == InputEvent.DEVICE_ID_EMULATION:
		if _action_at(event.position) != "" or not _touches.is_empty():
			get_viewport().set_input_as_handled()
		return
	if event is InputEventScreenTouch:
		var t := event as InputEventScreenTouch
		if t.pressed:
			var action := _action_at(t.position)
			if action != "":
				_touches[t.index] = action
				_apply()
				get_viewport().set_input_as_handled()
		elif _touches.has(t.index):
			_touches.erase(t.index)
			_apply()
			get_viewport().set_input_as_handled()
	elif event is InputEventScreenDrag:
		var d := event as InputEventScreenDrag
		if _touches.has(d.index):
			var prev: String = _touches[d.index]
			var action := _action_at(d.position)
			if prev.begins_with("move_"):
				# desliza no D-pad: troca a direção; fora dele, solta
				var dir := _dpad_action(d.position, true)
				if dir != "":
					_touches[d.index] = dir
				else:
					_touches.erase(d.index)
			elif action != prev:
				_touches.erase(d.index)
			_apply()
			get_viewport().set_input_as_handled()


func _action_at(pos: Vector2) -> String:
	var dir := _dpad_action(pos, false)
	if dir != "":
		return dir
	if _hit_circle(_a, pos):
		return "btn_a"
	if _hit_circle(_b, pos):
		return "btn_b"
	return ""


func _dpad_action(pos: Vector2, sliding: bool) -> String:
	var grow := 10.0 * ui_scale if sliding else 4.0 * ui_scale
	var rect := Rect2(_dpad.position, _dpad.size).grow(grow)
	if not rect.has_point(pos):
		return ""
	var v := pos - (_dpad.position + _dpad.size / 2.0)
	if v.length() < 4.0 * ui_scale:
		return ""
	if absf(v.x) > absf(v.y):
		return "move_right" if v.x > 0 else "move_left"
	return "move_down" if v.y > 0 else "move_up"


func _hit_circle(r: TextureRect, pos: Vector2) -> bool:
	var c := r.position + r.size / 2.0
	return pos.distance_to(c) <= r.size.x / 2.0 + 4.0 * ui_scale


func _apply() -> void:
	var want := {}
	for action in _touches.values():
		want[action] = true
	for action in _pressed.keys():
		if not want.has(action):
			Controls.emit_action(action, false)
	for action in want.keys():
		if not _pressed.has(action):
			Controls.emit_action(action, true)
			if action in ["btn_a", "btn_b"]:
				Haptics.tap()
	_pressed = want
	_update_visuals()


func _release_all() -> void:
	_touches.clear()
	_apply()


func _update_visuals() -> void:
	_a.texture = _tex["btn_a_pressed" if _pressed.has("btn_a") else "btn_a"]
	_b.texture = _tex["btn_b_pressed" if _pressed.has("btn_b") else "btn_b"]
	_a.modulate.a = ALPHA_PRESSED if _pressed.has("btn_a") else ALPHA_IDLE
	_b.modulate.a = ALPHA_PRESSED if _pressed.has("btn_b") else ALPHA_IDLE
	var arm := ""
	for k in _pressed.keys():
		if str(k).begins_with("move_"):
			arm = k
	_glow.visible = arm != "" and pad_visible()
	_dpad.modulate.a = ALPHA_PRESSED if arm != "" else ALPHA_IDLE
	if arm != "":
		var cell := Vector2.ZERO
		match arm:
			"move_up":
				cell = Vector2(1, 0)
			"move_down":
				cell = Vector2(1, 2)
			"move_left":
				cell = Vector2(0, 1)
			"move_right":
				cell = Vector2(2, 1)
		var s := float(ui_scale)
		_glow.position = _dpad.position + (cell * 24.0 + Vector2(1, 1)) * s


func _update_speed_icon() -> void:
	if _speed:
		_speed.texture = _tex["btn_speed_2x" if Speed.fast else "btn_speed_1x"]
		_speed.modulate.a = 0.95 if Speed.fast else 0.75


func _on_top_button(event: InputEvent, action: String) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		accept_event()
		Haptics.tap()
		Controls.tap_action(action)


func _notification(what: int) -> void:
	if what == NOTIFICATION_APPLICATION_FOCUS_OUT:
		_release_all()
