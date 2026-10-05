extends "res://tests/test_case.gd"
## Entradas: ações registradas, direção mais recente, 2x, controles de toque e 48dp.

var tree: SceneTree
var host: Node


func set_tree(t: SceneTree, h: Node) -> void:
	tree = t
	host = h


func test_actions_registered() -> void:
	for a in ["move_up", "move_down", "move_left", "move_right", "btn_a", "btn_b", "btn_menu", "btn_speed"]:
		check(InputMap.has_action(a), "ação %s" % a)
		var has_key := false
		var has_pad := false
		for ev in InputMap.action_get_events(a):
			if ev is InputEventKey:
				has_key = true
			if ev is InputEventJoypadButton or ev is InputEventJoypadMotion:
				has_pad = true
		check(has_key, "%s tem tecla" % a)
		check(has_pad, "%s tem gamepad" % a)


func test_last_direction_wins() -> void:
	Controls.clear()
	_send("move_up", true)
	check_eq(Controls.current_direction(), Vector2i.UP, "cima")
	_send("move_left", true)
	check_eq(Controls.current_direction(), Vector2i.LEFT, "a mais recente vence")
	_send("move_left", false)
	check_eq(Controls.current_direction(), Vector2i.UP, "solta e volta para a anterior")
	_send("move_up", false)
	check_eq(Controls.current_direction(), Vector2i.ZERO, "nada pressionado")


func _send(action: String, pressed: bool) -> void:
	var ev := InputEventAction.new()
	ev.action = action
	ev.pressed = pressed
	Input.parse_input_event(ev)
	Input.flush_buffered_events()
	Controls._input(ev)


func test_fast_forward() -> void:
	var was := Speed.fast
	Speed.set_fast(false)
	check(is_equal_approx(Engine.time_scale, 1.0), "1x")
	Speed.toggle()
	check(is_equal_approx(Engine.time_scale, 2.0), "2x")
	check(bool(Settings.get_value("fast_forward")), "estado do 2x salvo nas configurações")
	Speed.set_debug_multiplier(10.0)
	check(is_equal_approx(Engine.time_scale, 10.0), "debug 10x")
	Speed.set_debug_multiplier(1.0)
	check(is_equal_approx(Engine.time_scale, 2.0), "volta ao 2x")
	Speed.set_fast(was)


func test_touch_targets_48dp() -> void:
	# aparelhos de referência (dpi, altura da tela em paisagem)
	for dev in [[420, 1080], [400, 1080], [320, 720], [560, 1440], [480, 1440], [264, 1600], [320, 1200]]:
		var need := TouchControls.base_px_for_48dp(float(dev[0]), int(dev[1]), 180.0)
		check(need <= 24.0, "D-pad de 24 px cobre 48dp em %d dpi/%d px (precisa %.1f)" % [dev[0], dev[1], need])


func test_touch_dpad_emits_actions() -> void:
	var tc := TouchControls.new()
	host.add_child(tc)
	Settings.set_value("touch_controls", "on")
	tc.set_world_mode(true)
	check(tc.pad_visible(), "D-pad visível no mapa com toque ligado")
	var up_arm: Vector2 = tc._dpad.position + Vector2(36, 8)
	var t := InputEventScreenTouch.new()
	t.index = 0
	t.position = up_arm
	t.pressed = true
	tc._input(t)
	Input.flush_buffered_events()
	check(Input.is_action_pressed("move_up"), "tocar o braço de cima pressiona move_up")
	var drag := InputEventScreenDrag.new()
	drag.index = 0
	drag.position = tc._dpad.position + Vector2(64, 36)
	tc._input(drag)
	Input.flush_buffered_events()
	check(Input.is_action_pressed("move_right") and not Input.is_action_pressed("move_up"), "deslizar troca para direita")
	var a := InputEventScreenTouch.new()
	a.index = 1
	a.position = tc._a.position + tc._a.size / 2.0
	a.pressed = true
	tc._input(a)
	Input.flush_buffered_events()
	check(Input.is_action_pressed("btn_a") and Input.is_action_pressed("move_right"), "multitoque: A e direção juntos")
	t.pressed = false
	tc._input(t)
	a.pressed = false
	tc._input(a)
	Input.flush_buffered_events()
	check(not Input.is_action_pressed("move_right") and not Input.is_action_pressed("btn_a"), "soltar libera as ações")
	tc.set_world_mode(false)
	check(not tc.pad_visible(), "sem D-pad fora do mapa")
	Settings.set_value("touch_controls", "auto")
	tc.queue_free()
