class_name TitleButton
extends Control
## Botão da tela inicial (estilo moderno, desenhado em alta resolução):
## vidro escuro com borda fina; o selecionado ganha brilho ciano; o principal é laranja.

signal pressed

const RADIUS := 6.0

var key := ""
var primary := false
var selected := false:
	set(v):
		if selected == v:
			return
		selected = v
		_update_selected()
var _label: Label
var _pulse := 0.0


func setup(text_key: String, is_primary: bool, font: Font, font_size: int) -> TitleButton:
	key = text_key
	primary = is_primary
	_label = Label.new()
	_label.auto_translate_mode = Node.AUTO_TRANSLATE_MODE_DISABLED
	_label.set_anchors_preset(Control.PRESET_FULL_RECT)
	_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	_label.add_theme_font_override("font", font)
	_label.add_theme_font_size_override("font_size", font_size)
	_label.add_theme_color_override("font_shadow_color", Color(0.03, 0.01, 0.1, 0.55))
	_label.add_theme_constant_override("shadow_offset_x", 0)
	_label.add_theme_constant_override("shadow_offset_y", 1)
	_label.mouse_filter = Control.MOUSE_FILTER_IGNORE
	add_child(_label)
	mouse_filter = Control.MOUSE_FILTER_STOP
	refresh_text()
	_update_selected()
	return self


func refresh_text() -> void:
	if _label:
		_label.text = tr(key).to_upper() if primary else tr(key)


func _notification(what: int) -> void:
	if what == NOTIFICATION_TRANSLATION_CHANGED:
		refresh_text()
	elif what == NOTIFICATION_RESIZED:
		pivot_offset = size / 2.0


func _update_selected() -> void:
	if _label:
		_label.add_theme_color_override("font_color", Color.WHITE if (selected or primary) else Color(0.86, 0.84, 0.95))
	queue_redraw()


func _process(delta: float) -> void:
	_pulse += delta
	if selected:
		queue_redraw()


func _gui_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		accept_event()
		pressed.emit()


static func rounded_rect(r: Rect2, radius: float, steps: int = 6) -> PackedVector2Array:
	var pts := PackedVector2Array()
	var rad := minf(radius, minf(r.size.x, r.size.y) / 2.0)
	var corners := [
		[r.position + Vector2(r.size.x - rad, rad), -PI / 2.0],
		[r.position + Vector2(r.size.x - rad, r.size.y - rad), 0.0],
		[r.position + Vector2(rad, r.size.y - rad), PI / 2.0],
		[r.position + Vector2(rad, rad), PI],
	]
	for c in corners:
		for i in steps + 1:
			var a: float = c[1] + (PI / 2.0) * i / steps
			pts.append(c[0] + Vector2(cos(a), sin(a)) * rad)
	return pts


func _draw() -> void:
	var r := Rect2(Vector2.ZERO, size)
	var pts := rounded_rect(r, RADIUS)
	var glow_a := 0.5 + 0.5 * sin(_pulse * 4.0)
	if selected:
		# halo ciano pulsando
		for i in range(4, 0, -1):
			var g := rounded_rect(r.grow(i * 0.9), RADIUS + i * 0.9)
			draw_colored_polygon(g, Color(0.2, 0.9, 1.0, 0.05 + 0.03 * glow_a))
	var top: Color
	var bottom: Color
	if primary:
		top = Color(1.0, 0.68, 0.25, 0.97)
		bottom = Color(0.93, 0.25, 0.32, 0.97)
	elif selected:
		top = Color(0.18, 0.5, 0.78, 0.85)
		bottom = Color(0.1, 0.18, 0.45, 0.85)
	else:
		top = Color(0.13, 0.08, 0.3, 0.62)
		bottom = Color(0.05, 0.03, 0.14, 0.62)
	var cols := PackedColorArray()
	for p in pts:
		cols.append(top.lerp(bottom, clampf(p.y / maxf(size.y, 1.0), 0.0, 1.0)))
	draw_polygon(pts, cols)
	# reflexo de vidro na metade de cima
	var gloss := rounded_rect(Rect2(Vector2(1.2, 1.0), Vector2(size.x - 2.4, size.y * 0.45)), RADIUS - 1.0)
	draw_colored_polygon(gloss, Color(1, 1, 1, 0.10 if not primary else 0.16))
	var outline := pts.duplicate()
	outline.append(pts[0])
	var border := Color(0.45, 0.95, 1.0, 0.95) if selected else (Color(1.0, 0.9, 0.6, 0.9) if primary else Color(1, 1, 1, 0.28))
	draw_polyline(outline, border, 0.45 if not selected else 0.7, true)
	if selected:
		# setinha à esquerda
		var cy := size.y / 2.0
		var x := 5.0 + 0.8 * glow_a
		draw_colored_polygon(PackedVector2Array([Vector2(x, cy - 2.6), Vector2(x + 3.4, cy), Vector2(x, cy + 2.6)]), Color(0.6, 1.0, 1.0, 0.95))
