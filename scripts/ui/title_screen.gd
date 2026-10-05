class_name TitleScreen
extends Control
## Tela inicial da série, em alta resolução (o mapa continua pixel-perfect):
## pôr do sol retrô em camadas com parallax, raios de sol, brasas, estrela
## cadente, logo HD com brilho e botões modernos. Enquanto ela está aberta a
## janela usa CONTENT_SCALE_MODE_CANVAS_ITEMS; ao sair volta para VIEWPORT.
## Três toques no logo abrem o menu de debug (só em build de debug).

const ART_W := 2400.0
const ART_H := 1080.0
const SUN := Vector2(1200, 376)
const TAPS_FOR_DEBUG := 3
const TAP_WINDOW_MS := 1200
const REPEAT_DELAY_MS := 320
const REPEAT_RATE_MS := 110

const SEA_SHADER := """
shader_type canvas_item;
uniform float horizon = 0.5926;
void fragment() {
	vec2 uv = UV;
	float d = uv.y - horizon;
	if (d > 0.0) {
		uv.x += sin(uv.y * 520.0 + TIME * 1.6) * 0.0009 * (0.4 + d * 3.0);
	}
	COLOR = texture(TEXTURE, uv);
}
"""

const SHINE_SHADER := """
shader_type canvas_item;
uniform float progress = -1.0;
void fragment() {
	vec4 c = texture(TEXTURE, UV);
	float x = UV.x + UV.y * 0.35;
	float band = 1.0 - smoothstep(0.0, 0.07, abs(x - progress));
	c.rgb = mix(c.rgb, vec3(1.0), band * 0.55 * c.a);
	COLOR = c;
}
"""

var _stage: Node2D
var _clouds: Array[Sprite2D] = []
var _castle: Sprite2D
var _fore: Sprite2D
var _rays: Sprite2D
var _logo: TextureRect
var _logo_mat: ShaderMaterial
var _version: Label
var _flash: ColorRect
var _buttons: Array[TitleButton] = []
## posição de cada botão na grade: linha 0 = principal, linha 1 = secundários
var _grid: Array[Vector2i] = []
var _index := 0
var _font: FontVariation
var _time := 0.0
var _intro_done := false
var _taps: Array[int] = []
var _held := Vector2i.ZERO
var _next_ms := 0
var _logo_base_y := 0.0


func _enter_tree() -> void:
	get_tree().root.content_scale_mode = Window.CONTENT_SCALE_MODE_CANVAS_ITEMS


func _exit_tree() -> void:
	get_tree().root.content_scale_mode = Window.CONTENT_SCALE_MODE_VIEWPORT


func _ready() -> void:
	set_anchors_preset(Control.PRESET_FULL_RECT)
	mouse_filter = Control.MOUSE_FILTER_IGNORE
	texture_filter = CanvasItem.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS
	_font = FontVariation.new()
	_font.base_font = load("res://assets/fonts/nunito/Nunito.ttf")
	_font.variation_opentype = {TextServerManager.get_primary_interface().name_to_tag("wght"): 850}
	_build_stage()
	_build_ui()
	_build_menu()
	get_viewport().size_changed.connect(_layout)
	_layout()
	_intro()


# ------------------------------------------------------------------ cenário
func _sprite(path: String, pos: Vector2 = Vector2.ZERO) -> Sprite2D:
	var s := Sprite2D.new()
	s.texture = load(path)
	s.centered = false
	s.position = pos
	_stage.add_child(s)
	return s


func _build_stage() -> void:
	_stage = Node2D.new()
	add_child(_stage)
	var bg := _sprite("res://assets/title/bg.png")
	var sea := ShaderMaterial.new()
	sea.shader = Shader.new()
	sea.shader.code = SEA_SHADER
	bg.material = sea
	_rays = _sprite("res://assets/title/rays.png")
	_rays.centered = true
	_rays.position = SUN
	_rays.scale = Vector2(1.6, 1.6)
	var add := CanvasItemMaterial.new()
	add.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	_rays.material = add
	_rays.modulate.a = 0.35
	for i in 2:
		var c := _sprite("res://assets/title/clouds.png", Vector2(i * ART_W, 40))
		_clouds.append(c)
	_castle = _sprite("res://assets/title/castle.png")
	_stage.add_child(_embers())
	_fore = _sprite("res://assets/title/fore.png")


func _embers() -> CPUParticles2D:
	var p := CPUParticles2D.new()
	p.texture = load("res://assets/title/glow_dot.png")
	p.amount = 46
	p.lifetime = 7.0
	p.preprocess = 7.0
	p.emission_shape = CPUParticles2D.EMISSION_SHAPE_RECTANGLE
	p.emission_rect_extents = Vector2(ART_W / 2.0, 80)
	p.position = Vector2(ART_W / 2.0, 1000)
	p.direction = Vector2(0.15, -1)
	p.spread = 25.0
	p.gravity = Vector2(6, -4)
	p.initial_velocity_min = 25.0
	p.initial_velocity_max = 70.0
	p.scale_amount_min = 0.12
	p.scale_amount_max = 0.42
	var ramp := Gradient.new()
	ramp.set_color(0, Color(1.0, 0.75, 0.35, 0.0))
	ramp.set_color(1, Color(1.0, 0.3, 0.6, 0.0))
	ramp.add_point(0.25, Color(1.0, 0.7, 0.35, 0.9))
	ramp.add_point(0.7, Color(1.0, 0.45, 0.6, 0.6))
	p.color_ramp = ramp
	var add := CanvasItemMaterial.new()
	add.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	p.material = add
	return p


# ------------------------------------------------------------------ interface
func _build_ui() -> void:
	_logo = TextureRect.new()
	_logo.texture = load("res://assets/title/logo.png")
	_logo.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
	_logo.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	_logo.mouse_filter = Control.MOUSE_FILTER_STOP
	_logo.gui_input.connect(_on_logo_input)
	_logo_mat = ShaderMaterial.new()
	_logo_mat.shader = Shader.new()
	_logo_mat.shader.code = SHINE_SHADER
	_logo.material = _logo_mat
	add_child(_logo)
	_version = Label.new()
	_version.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	_version.text = "v" + str(ProjectSettings.get_setting("application/config/version", ""))
	_version.add_theme_font_override("font", _font)
	_version.add_theme_font_size_override("font_size", 6)
	_version.add_theme_color_override("font_color", Color(1, 1, 1, 0.55))
	add_child(_version)
	_flash = ColorRect.new()
	_flash.color = Color(1, 0.95, 0.85, 0)
	_flash.mouse_filter = Control.MOUSE_FILTER_IGNORE
	_flash.set_anchors_preset(Control.PRESET_FULL_RECT)
	add_child(_flash)


func _build_menu() -> void:
	for b in _buttons:
		b.queue_free()
	_buttons.clear()
	_grid.clear()
	var has_save := SaveGame.has_save()
	var primary_key := "MENU_CONTINUE" if has_save else "MENU_NEW_GAME"
	_add_button("continue" if has_save else "new", primary_key, true, Vector2i(0, 0))
	var col := 0
	if has_save:
		_add_button("new", "MENU_NEW_GAME", false, Vector2i(col, 1))
		col += 1
	_add_button("settings", "MENU_SETTINGS", false, Vector2i(col, 1))
	_add_button("about", "MENU_ABOUT", false, Vector2i(col + 1, 1))
	_index = 0
	_select(0, false)
	_layout()


func _add_button(id: String, key: String, primary: bool, cell: Vector2i) -> void:
	var b := TitleButton.new().setup(key, primary, _font, 11 if primary else 8)
	b.name = "Btn_" + id
	b.set_meta("id", id)
	b.pressed.connect(func() -> void:
		_select(_buttons.find(b), false)
		_activate()
	)
	add_child(b)
	move_child(b, _flash.get_index())
	_buttons.append(b)
	_grid.append(cell)


func _layout() -> void:
	var vp := get_viewport_rect().size
	# cenário cobre a tela (corta as laterais em 16:9)
	var s := maxf(vp.x / ART_W, vp.y / ART_H)
	_stage.scale = Vector2(s, s)
	_stage.position = Vector2((vp.x - ART_W * s) / 2.0, (vp.y - ART_H * s) / 2.0)
	var tex := _logo.texture.get_size()
	var lw := minf(vp.x * 0.74, 236.0)
	var lh := lw * tex.y / tex.x
	_logo.size = Vector2(lw, lh)
	_logo_base_y = 7.0
	_logo.position = Vector2((vp.x - lw) / 2.0, _logo_base_y)
	_logo.pivot_offset = _logo.size / 2.0
	var top := _logo_base_y + lh + 10.0
	var row := []
	for i in _buttons.size():
		if _grid[i].y == 1:
			row.append(_buttons[i])
	var primary: TitleButton = _buttons[0]
	primary.size = Vector2(118, 21)
	primary.position = Vector2((vp.x - primary.size.x) / 2.0, top)
	var bw := 86.0
	var gap := 5.0
	var total := row.size() * bw + (row.size() - 1) * gap
	var y2 := top + primary.size.y + 7.0
	for i in row.size():
		var b: TitleButton = row[i]
		b.size = Vector2(bw, 15)
		b.position = Vector2((vp.x - total) / 2.0 + i * (bw + gap), y2)
	for b in _buttons:
		b.set_meta("base_y", b.position.y)
	_version.position = Vector2(5, vp.y - 11)


# ------------------------------------------------------------------ animação
func _intro() -> void:
	_logo.modulate.a = 0.0
	_logo.scale = Vector2(0.55, 0.55)
	for b in _buttons:
		b.modulate.a = 0.0
		b.position.y = float(b.get_meta("base_y")) + 18.0
	var tw := create_tween().set_parallel(true)
	tw.tween_property(_logo, "modulate:a", 1.0, 0.45).set_delay(0.25)
	tw.tween_property(_logo, "scale", Vector2.ONE, 0.75).set_delay(0.25).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_property(_flash, "color:a", 0.45, 0.08).set_delay(0.7)
	tw.tween_property(_flash, "color:a", 0.0, 0.5).set_delay(0.78)
	for i in _buttons.size():
		var b := _buttons[i]
		var d := 0.9 + i * 0.08
		tw.tween_property(b, "modulate:a", 1.0, 0.35).set_delay(d)
		tw.tween_property(b, "position:y", float(b.get_meta("base_y")), 0.45).set_delay(d).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
	tw.chain().tween_callback(func() -> void: _intro_done = true)
	_shine_loop()


func _skip_intro() -> void:
	if _intro_done:
		return
	for t in get_tree().get_processed_tweens():
		if t.is_valid() and t.is_running():
			t.custom_step(10.0)
	_intro_done = true


func _shine_loop() -> void:
	while is_inside_tree():
		await get_tree().create_timer(3.6, true, false, true).timeout
		if not is_inside_tree():
			return
		_logo_mat.set_shader_parameter("progress", -0.3)
		var tw := create_tween()
		tw.tween_property(_logo_mat, "shader_parameter/progress", 1.5, 0.9).set_trans(Tween.TRANS_SINE)
		await tw.finished


func _process(delta: float) -> void:
	_time += delta
	_rays.rotation = _time * 0.04
	_rays.modulate.a = 0.28 + 0.07 * sin(_time * 0.9)
	for i in _clouds.size():
		var x := fmod(-_time * 14.0, ART_W) + i * ART_W
		_clouds[i].position.x = x
	# parallax leve
	var sway := sin(_time * 0.25)
	_castle.position.x = sway * 10.0
	_fore.position.x = sway * 24.0
	if _intro_done:
		_logo.position.y = _logo_base_y + sin(_time * 1.6) * 1.2
	_maybe_shooting_star(delta)
	_handle_navigation()


var _star_cd := 4.0


func _maybe_shooting_star(delta: float) -> void:
	_star_cd -= delta
	if _star_cd > 0.0:
		return
	_star_cd = randf_range(5.0, 10.0)
	var line := Line2D.new()
	line.width = 4.0
	line.default_color = Color(1, 1, 1, 0.9)
	var g := Gradient.new()
	g.set_color(0, Color(1, 1, 1, 0))
	g.set_color(1, Color(1, 0.95, 0.85, 1))
	line.gradient = g
	line.points = PackedVector2Array([Vector2(-140, -50), Vector2(0, 0)])
	line.position = Vector2(randf_range(300, 2100), randf_range(60, 260))
	var add := CanvasItemMaterial.new()
	add.blend_mode = CanvasItemMaterial.BLEND_MODE_ADD
	line.material = add
	_stage.add_child(line)
	_stage.move_child(line, 2)
	var tw := create_tween().set_parallel(true)
	tw.tween_property(line, "position", line.position + Vector2(520, 185), 0.9)
	tw.tween_property(line, "modulate:a", 0.0, 0.9).set_ease(Tween.EASE_IN)
	tw.chain().tween_callback(line.queue_free)


# ------------------------------------------------------------------ navegação
func _active() -> bool:
	return Game.top_overlay() == null and not Game.transitioning


func _handle_navigation() -> void:
	if not _active():
		_held = Vector2i(9, 9)
		return
	var d := Vector2i(
		int(Input.is_action_pressed("move_right")) - int(Input.is_action_pressed("move_left")),
		int(Input.is_action_pressed("move_down")) - int(Input.is_action_pressed("move_up")))
	if _held == Vector2i(9, 9):
		_held = d  # não reage a uma direção que já vinha pressionada
		return
	var now := Time.get_ticks_msec()
	if d != Vector2i.ZERO and d == _held and now >= _next_ms:
		_next_ms = now + REPEAT_RATE_MS
		_move(d)
	_held = d


func _move(d: Vector2i) -> void:
	_skip_intro()
	var cur := _grid[_index]
	var target := -1
	if d.y != 0:
		var want_row := clampi(cur.y + d.y, 0, 1)
		if want_row != cur.y:
			# vai para o botão mais próximo da outra linha (o do meio, de baixo para cima)
			var best := INF
			for i in _buttons.size():
				if _grid[i].y == want_row:
					var dist := absf(_buttons[i].position.x + _buttons[i].size.x / 2.0 - (_buttons[_index].position.x + _buttons[_index].size.x / 2.0))
					if dist < best:
						best = dist
						target = i
	elif d.x != 0 and cur.y == 1:
		for i in _buttons.size():
			if _grid[i] == Vector2i(cur.x + d.x, 1):
				target = i
	if target >= 0:
		_select(target, true)


func _select(i: int, sound: bool) -> void:
	_index = clampi(i, 0, _buttons.size() - 1)
	for k in _buttons.size():
		var b := _buttons[k]
		b.selected = k == _index
		var tw := b.create_tween()
		tw.tween_property(b, "scale", Vector2(1.06, 1.06) if k == _index else Vector2.ONE, 0.12)
	if sound:
		Audio.sfx("cursor")


func _unhandled_input(event: InputEvent) -> void:
	if not _active():
		return
	for dir_action in Controls.DIRS.keys():
		if event.is_action_pressed(dir_action, false):
			get_viewport().set_input_as_handled()
			var d: Vector2i = Controls.DIRS[dir_action]
			_move(d)
			_held = d
			_next_ms = Time.get_ticks_msec() + REPEAT_DELAY_MS
			return
	if event.is_action_pressed("btn_a", false):
		get_viewport().set_input_as_handled()
		if not _intro_done:
			_skip_intro()
			return
		_activate()
	elif event is InputEventScreenTouch and event.pressed and not _intro_done:
		_skip_intro()


func _activate() -> void:
	if not _active():
		return
	_skip_intro()
	Audio.sfx("confirm")
	Haptics.tap()
	var b := _buttons[_index]
	var pop := b.create_tween()
	pop.tween_property(b, "scale", Vector2(0.96, 0.96), 0.06)
	pop.tween_property(b, "scale", Vector2(1.06, 1.06), 0.1)
	match str(b.get_meta("id")):
		"continue":
			Game.continue_game()
		"new":
			if SaveGame.has_save():
				var answer := await ChoiceBox.ask("CONFIRM_OVERWRITE", ["OPT_YES", "OPT_NO"])
				if answer != 0:
					return
			var entry := NameEntry.new()
			Game.open_overlay(entry)
			var player_name: String = await entry.confirmed
			if player_name != "":
				SaveGame.delete_save()
				Game.start_new_game(player_name)
		"settings":
			Game.open_overlay(SettingsMenu.new())
		"about":
			Game.open_overlay(AboutScreen.new())


func _on_logo_input(event: InputEvent) -> void:
	if not (event is InputEventMouseButton and event.pressed):
		return
	_skip_intro()
	var now := Time.get_ticks_msec()
	_taps.append(now)
	_taps = _taps.filter(func(t: int) -> bool: return now - t <= TAP_WINDOW_MS)
	if _taps.size() >= TAPS_FOR_DEBUG:
		_taps.clear()
		Game.open_debug()
