class_name RingMenu
extends Control
## Menu em anel ao redor do esqueleto ativo: Golpes (cima), Itens (direita),
## Trocar (baixo) e Fugir (esquerda). A direção do D-pad escolhe a opção na
## hora; A confirma. Cada ícone também aceita toque.

signal chosen(id: String)

const RADIUS := 23.0
const OPTIONS := [
	{"id": "moves", "dir": Vector2i.UP, "key": "BTL_RING_MOVES"},
	{"id": "items", "dir": Vector2i.RIGHT, "key": "BTL_RING_ITEMS"},
	{"id": "switch", "dir": Vector2i.DOWN, "key": "BTL_RING_SWITCH"},
	{"id": "flee", "dir": Vector2i.LEFT, "key": "BTL_RING_FLEE"},
]

var selected := "moves"
var disabled := {}
var _icons := {}
var _label: Label
var _label_panel: PanelContainer
var _t := 0.0


func _init() -> void:
	theme = UiTheme.build()
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func _ready() -> void:
	for o in OPTIONS:
		var r := TextureRect.new()
		r.texture = load("res://assets/battle/ring_%s.png" % o.id)
		# área de toque de 24×24 em volta do ícone de 16 (desenho igual)
		r.custom_minimum_size = Vector2(24, 24)
		r.size = Vector2(24, 24)
		r.stretch_mode = TextureRect.STRETCH_KEEP_CENTERED
		r.mouse_filter = Control.MOUSE_FILTER_STOP
		r.gui_input.connect(_on_icon_input.bind(str(o.id)))
		add_child(r)
		_icons[o.id] = r
	_label_panel = PanelContainer.new()
	_label_panel.add_theme_stylebox_override("panel", UiTheme.frame("dark"))
	_label = UiTheme.label("", UiTheme.TEXT_LIGHT)
	_label_panel.add_child(_label)
	add_child(_label_panel)
	refresh()


func open_at(center: Vector2, disabled_ids: Dictionary) -> void:
	position = center
	disabled = disabled_ids
	selected = "moves"
	visible = true
	scale = Vector2(0.4, 0.4)
	modulate.a = 0.0
	var tw := create_tween().set_parallel(true)
	tw.tween_property(self, "scale", Vector2.ONE, 0.14).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	tw.tween_property(self, "modulate:a", 1.0, 0.1)
	refresh()


func select_dir(d: Vector2i) -> void:
	for o in OPTIONS:
		if o.dir == d:
			if selected != o.id:
				selected = o.id
				Audio.sfx("cursor")
			refresh()


func refresh() -> void:
	if _label == null:
		return
	for o in OPTIONS:
		var r: TextureRect = _icons[o.id]
		var sel: bool = o.id == selected
		r.position = Vector2(o.dir) * RADIUS * (1.12 if sel else 1.0) - Vector2(12, 12)
		r.modulate = Color(1, 1, 1, 0.35) if disabled.has(o.id) else (Color(1.25, 1.25, 1.1) if sel else Color(1, 1, 1, 0.92))
		r.scale = Vector2.ONE
	_label.text = tr(_key(selected))
	_label_panel.reset_size()
	_label_panel.position = Vector2(-_label_panel.size.x / 2.0, -RADIUS - 28)
	queue_redraw()


func _key(id: String) -> String:
	for o in OPTIONS:
		if o.id == id:
			return o.key
	return ""


func _process(delta: float) -> void:
	_t += delta
	if visible:
		queue_redraw()


func _draw() -> void:
	# anel tracejado girando
	var n := 24
	for i in n:
		if i % 2 == 0:
			var a0 := _t * 0.8 + i * TAU / n
			draw_arc(Vector2.ZERO, RADIUS, a0, a0 + TAU / n, 3, Color(1, 1, 1, 0.55), 1.0)
	for o in OPTIONS:
		if o.id == selected:
			var c := Vector2(o.dir) * RADIUS * 1.12
			draw_circle(c, 10.5 + sin(_t * 8.0) * 0.6, Color(1, 0.85, 0.35, 0.55))


func _on_icon_input(event: InputEvent, id: String) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		accept_event()
		selected = id
		refresh()
		confirm()


func confirm() -> void:
	if disabled.has(selected):
		Audio.sfx("bump")
		return
	Audio.sfx("confirm")
	chosen.emit(selected)
