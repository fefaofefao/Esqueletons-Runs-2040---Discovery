class_name MoveList
extends Control
## Lista de golpes no centro da arena: tipo, nome, peso (» leve, ■ pesado) e PP.
## Toque: 1º toque seleciona, 2º confirma.

signal tapped(index: int)

const ROW := Vector2(120, 15)

var monster: Monster
var engine: BattleEngine
var index := 0
var move_ids: Array = []
var _rows: Array = []


func _init() -> void:
	theme = UiTheme.build()
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func _ready() -> void:
	for i in 4:
		var r := Control.new()
		r.size = ROW
		r.position = Vector2(0, i * (ROW.y + 1))
		r.mouse_filter = Control.MOUSE_FILTER_STOP
		r.gui_input.connect(_on_row_input.bind(i))
		r.draw.connect(_draw_row.bind(r, i))
		var icon := TextureRect.new()
		icon.position = Vector2(4, 3)
		icon.name = "Icon"
		r.add_child(icon)
		var name_l := UiTheme.label("")
		name_l.position = Vector2(15, 1)
		name_l.size = Vector2(70, 12)
		name_l.clip_text = true
		name_l.name = "Name"
		r.add_child(name_l)
		var pp_l := UiTheme.label("", UiTheme.TEXT_VALUE)
		pp_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
		pp_l.position = Vector2(ROW.x - 34, 1)
		pp_l.size = Vector2(30, 12)
		pp_l.name = "PP"
		r.add_child(pp_l)
		add_child(r)
		_rows.append(r)
	size = Vector2(ROW.x, 4 * (ROW.y + 1))


func open(m: Monster, e: BattleEngine) -> void:
	monster = m
	engine = e
	move_ids = []
	for mv in m.moves:
		move_ids.append(str(mv["id"]))
	if engine.usable_moves(m) == ["struggle"]:
		move_ids = ["struggle"]
	index = clampi(index, 0, move_ids.size() - 1)
	for i in 4:
		var r: Control = _rows[i]
		r.visible = i < move_ids.size()
		if not r.visible:
			continue
		var mv := engine.move_data(move_ids[i])
		(r.get_node("Name") as Label).text = tr(str(mv.get("name_key", "")))
		var pp := _pp(i)
		var pp_l: Label = r.get_node("PP")
		pp_l.text = "%d/%d" % [pp, int(mv.get("pp", 1))] if move_ids[i] != "struggle" else ""
		pp_l.add_theme_color_override("font_color", UiTheme.TEXT_VALUE if pp > 0 else Color8(200, 60, 60))
		var t := str(mv.get("type", ""))
		(r.get_node("Icon") as TextureRect).texture = load("res://assets/battle/type_%s.png" % t) if t != "" else null
		r.queue_redraw()
	visible = true


func _pp(i: int) -> int:
	if move_ids[i] == "struggle":
		return 1
	for mv in monster.moves:
		if mv["id"] == move_ids[i]:
			return int(mv["pp"])
	return 0


func usable(i: int) -> bool:
	return i >= 0 and i < move_ids.size() and _pp(i) > 0


func current_move() -> String:
	return move_ids[index]


func move_cursor(dy: int) -> void:
	var ni := clampi(index + dy, 0, move_ids.size() - 1)
	if ni != index:
		index = ni
		Audio.sfx("cursor")
	for r in _rows:
		r.queue_redraw()


func _draw_row(r: Control, i: int) -> void:
	var sel := i == index
	r.draw_style_box(UiTheme.frame("light"), Rect2(Vector2.ZERO, r.size))
	if sel:
		r.draw_rect(Rect2(Vector2(2, 2), r.size - Vector2(4, 4)), Color(1, 0.8, 0.3, 0.4))
	if not usable(i):
		r.draw_rect(Rect2(Vector2(2, 2), r.size - Vector2(4, 4)), Color(0.5, 0.5, 0.5, 0.35))
	if i < move_ids.size():
		var w := str(engine.move_data(move_ids[i]).get("weight", "normal"))
		var x := 88.0
		if w == "light":
			for k in 2:
				r.draw_polyline(PackedVector2Array([Vector2(x + k * 3, 4), Vector2(x + k * 3 + 2, 7), Vector2(x + k * 3, 10)]), Color8(40, 150, 200), 1.0)
		elif w == "heavy":
			r.draw_rect(Rect2(x, 4, 5, 6), Color8(200, 110, 40))


func _on_row_input(event: InputEvent, i: int) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		accept_event()
		tapped.emit(i)
