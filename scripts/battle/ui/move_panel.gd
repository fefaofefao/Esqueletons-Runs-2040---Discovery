class_name MovePanel
extends Control
## Golpes (2×2, com PP) e a prévia: tipo, poder/precisão, efetividade contra o
## alvo marcado (Fraco/Normal/Forte), efeito e alvo. Toque: 1º toque seleciona,
## 2º confirma.

signal tapped(index: int)

const ROW := Vector2(95, 22)
## Medidas usadas também pelo teste de overflow.
const PREVIEW_TEXT_WIDTH := 106.0
const DESC_WIDTH := 178.0

var monster: Monster
var engine: BattleEngine
var index := 0
var move_ids: Array = []
var _rows: Array = []
var preview: Control
var _pv_type: TextureRect
var _pv_lines: Array = []
var _desc_panel: PanelContainer
var _desc: Label


func _init() -> void:
	theme = UiTheme.build()
	mouse_filter = Control.MOUSE_FILTER_IGNORE


func build(parent_preview: Control) -> void:
	for i in 4:
		var r := Control.new()
		r.size = ROW
		r.position = Vector2(4 + (i % 2) * (ROW.x + 2), 3 + (i / 2) * (ROW.y + 1))
		r.mouse_filter = Control.MOUSE_FILTER_STOP
		r.gui_input.connect(_on_row_input.bind(i))
		r.draw.connect(_draw_row.bind(r, i))
		var name_l := UiTheme.label("")
		name_l.position = Vector2(12, -1)
		name_l.name = "Name"
		r.add_child(name_l)
		var pp_l := UiTheme.label("", UiTheme.TEXT_VALUE)
		pp_l.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
		pp_l.position = Vector2(ROW.x - 62, 9)
		pp_l.size = Vector2(58, 12)
		pp_l.name = "PP"
		r.add_child(pp_l)
		var icon := TextureRect.new()
		icon.position = Vector2(2, 2)
		icon.name = "Icon"
		r.add_child(icon)
		add_child(r)
		_rows.append(r)
	_desc_panel = PanelContainer.new()
	_desc_panel.add_theme_stylebox_override("panel", UiTheme.frame("dark"))
	_desc_panel.position = Vector2(0, -16)
	_desc_panel.custom_minimum_size = Vector2(192, 16)
	_desc = UiTheme.label("", UiTheme.TEXT_LIGHT)
	_desc_panel.add_child(_desc)
	add_child(_desc_panel)
	preview = parent_preview
	_pv_type = TextureRect.new()
	_pv_type.position = Vector2(6, 5)
	preview.add_child(_pv_type)
	for i in 4:
		var l := UiTheme.label("")
		l.position = Vector2(6 if i > 0 else 17, 1 + i * 12)
		preview.add_child(l)
		_pv_lines.append(l)


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
		(r.get_node("PP") as Label).text = "PP %d/%d" % [pp, int(mv.get("pp", 1))] if move_ids[i] != "struggle" else ""
		(r.get_node("PP") as Label).add_theme_color_override("font_color", UiTheme.TEXT_VALUE if pp > 0 else Color8(200, 60, 60))
		var t := str(mv.get("type", ""))
		(r.get_node("Icon") as TextureRect).texture = load("res://assets/battle/type_%s.png" % t) if t != "" else null
		r.queue_redraw()
	visible = true
	preview.visible = true


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


func move_cursor(d: Vector2i) -> void:
	var col := index % 2
	var row := index / 2
	col = clampi(col + d.x, 0, 1)
	row = clampi(row + d.y, 0, 1)
	var ni := row * 2 + col
	if ni < move_ids.size() and ni != index:
		index = ni
		Audio.sfx("cursor")
	for r in _rows:
		r.queue_redraw()


func update_preview(target: Monster) -> void:
	var mv := engine.move_data(current_move())
	var t := str(mv.get("type", ""))
	_pv_type.texture = load("res://assets/battle/type_%s.png" % t) if t != "" else null
	(_pv_lines[0] as Label).text = tr("TYPE_" + t.to_upper()) if t != "" else "—"
	var stats := tr("BTL_PREVIEW_STATS").format({"p": int(mv.get("power", 0)) if int(mv.get("power", 0)) > 0 else "—", "acc": int(mv.get("accuracy", 100))})
	(_pv_lines[1] as Label).text = stats
	var eff_l: Label = _pv_lines[2]
	var foes := str(mv.get("target", "enemy")) in ["enemy", "all_enemies"]
	if target and foes and int(mv.get("power", 0)) > 0:
		var mult := engine.effectiveness(t, target.type())
		eff_l.text = tr(BattleEngine.effectiveness_label(mult))
		eff_l.add_theme_color_override("font_color", Color8(40, 150, 60) if mult > 1.01 else (Color8(190, 60, 60) if mult < 0.99 else UiTheme.TEXT_DARK))
	else:
		eff_l.text = "—"
		eff_l.add_theme_color_override("font_color", UiTheme.TEXT_DISABLED)
	(_pv_lines[3] as Label).text = tr("BTL_TARGET_" + str(mv.get("target", "enemy")).to_upper())
	_desc.text = tr(str(mv.get("desc_key", "")))


func _draw_row(r: Control, i: int) -> void:
	var sel := i == index
	var sb := UiTheme.frame("light")
	r.draw_style_box(sb, Rect2(Vector2.ZERO, r.size))
	if sel:
		r.draw_rect(Rect2(Vector2(2, 2), r.size - Vector2(4, 4)), Color(1, 0.8, 0.3, 0.35))
	if not usable(i):
		r.draw_rect(Rect2(Vector2(2, 2), r.size - Vector2(4, 4)), Color(0.5, 0.5, 0.5, 0.35))


func _on_row_input(event: InputEvent, i: int) -> void:
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		accept_event()
		tapped.emit(i)
