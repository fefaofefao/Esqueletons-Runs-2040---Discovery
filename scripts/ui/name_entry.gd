class_name NameEntry
extends Overlay
## Tela para nomear o protagonista: grade de letras (com acentos, ç e ñ)
## navegável por D-pad ou por toque. B apaga; B com o nome vazio cancela.

signal confirmed(player_name: String)

const MAX_LEN := 10
const COLS := 10
const PAGES := [
	["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
	 "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
	 "U", "V", "W", "X", "Y", "Z", "Á", "É", "Í", "Ó",
	 "Ú", "Ã", "Õ", "Â", "Ê", "Ô", "Ç", "Ñ", "-", "."],
	["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
	 "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
	 "u", "v", "w", "x", "y", "z", "á", "é", "í", "ó",
	 "ú", "ã", "õ", "â", "ê", "ô", "ç", "ñ", "'", " "],
]
const ACTIONS := ["case", "delete", "ok"]
const ACTION_KEYS := {"case": "NAME_CASE", "delete": "NAME_DELETE", "ok": "NAME_OK"}

var player_name := ""
var page := 0
var cursor := Vector2i.ZERO
var _cells: Array = []
var _action_labels: Array = []
var _name_label: Label
var _title: Label
var _held := Vector2i.ZERO
var _next_ms := 0
var _done := false


func _ready() -> void:
	dim_background(0.6)
	var panel := centered_panel(240)
	var box := VBoxContainer.new()
	box.add_theme_constant_override("separation", 3)
	panel.add_child(box)
	_title = UiTheme.label(tr("NAME_TITLE"), UiTheme.TEXT_ACCENT)
	_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(_title)
	_name_label = UiTheme.label("")
	_name_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(_name_label)
	var grid := GridContainer.new()
	grid.columns = COLS
	grid.add_theme_constant_override("h_separation", 0)
	grid.add_theme_constant_override("v_separation", 0)
	box.add_child(grid)
	for i in PAGES[0].size():
		var cell := UiTheme.label("")
		cell.custom_minimum_size = Vector2(22, 13)
		cell.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
		cell.mouse_filter = Control.MOUSE_FILTER_STOP
		cell.gui_input.connect(_on_cell_input.bind(Vector2i(i % COLS, i / COLS)))
		grid.add_child(cell)
		_cells.append(cell)
	var actions := HBoxContainer.new()
	actions.alignment = BoxContainer.ALIGNMENT_CENTER
	actions.add_theme_constant_override("separation", 10)
	box.add_child(actions)
	for i in ACTIONS.size():
		var l := UiTheme.label("")
		l.mouse_filter = Control.MOUSE_FILTER_STOP
		l.gui_input.connect(_on_cell_input.bind(Vector2i(i, rows())))
		actions.add_child(l)
		_action_labels.append(l)
	_refresh()


func rows() -> int:
	return PAGES[0].size() / COLS


func _refresh() -> void:
	var shown := player_name
	if shown.length() < MAX_LEN:
		shown += "_"
	_name_label.text = shown
	_title.text = tr("NAME_TITLE")
	for i in _cells.size():
		var l: Label = _cells[i]
		var p := Vector2i(i % COLS, i / COLS)
		var ch: String = PAGES[page][i]
		l.text = "·" if ch == " " else ch
		l.add_theme_color_override("font_color", UiTheme.TEXT_ACCENT if p == cursor else UiTheme.TEXT_DARK)
		l.modulate = Color(1, 1, 1, 1)
	for i in _action_labels.size():
		var l: Label = _action_labels[i]
		var sel := cursor == Vector2i(i, rows())
		l.text = ("▶" if sel else " ") + tr(ACTION_KEYS[ACTIONS[i]])
		l.add_theme_color_override("font_color", UiTheme.TEXT_ACCENT if sel else UiTheme.TEXT_VALUE)


func _process(_delta: float) -> void:
	if not accepts_input():
		return
	var d := Vector2i(
		int(Input.is_action_pressed("move_right")) - int(Input.is_action_pressed("move_left")),
		int(Input.is_action_pressed("move_down")) - int(Input.is_action_pressed("move_up")))
	var now := Time.get_ticks_msec()
	if d != Vector2i.ZERO and (d != _held or now >= _next_ms):
		_next_ms = now + (300 if d != _held else 90)
		_move(d)
	_held = d


func _move(d: Vector2i) -> void:
	var old_y := cursor.y
	cursor.y = wrapi(cursor.y + d.y, 0, rows() + 1)
	if cursor.y == rows() and old_y != rows():
		cursor.x = clampi(cursor.x * ACTIONS.size() / COLS, 0, ACTIONS.size() - 1)
	elif old_y == rows() and cursor.y != rows():
		cursor.x = clampi(cursor.x * COLS / ACTIONS.size() + 1, 0, COLS - 1)
	var width := ACTIONS.size() if cursor.y == rows() else COLS
	cursor.x = wrapi(cursor.x + d.x, 0, width)
	Audio.sfx("cursor")
	_refresh()


func _unhandled_input(event: InputEvent) -> void:
	if not accepts_input():
		return
	if event.is_action_pressed("btn_a", false):
		get_viewport().set_input_as_handled()
		_select()
	elif event.is_action_pressed("btn_b", false):
		get_viewport().set_input_as_handled()
		_delete_or_cancel()
	elif event.is_action_pressed("btn_menu", false):
		get_viewport().set_input_as_handled()
		cursor = Vector2i(2, rows())
		_refresh()


func _select() -> void:
	if cursor.y == rows():
		match ACTIONS[cursor.x]:
			"case":
				page = 1 - page
				Audio.sfx("cursor")
			"delete":
				_delete_or_cancel()
				return
			"ok":
				_confirm()
				return
	else:
		if player_name.length() >= MAX_LEN:
			Audio.sfx("bump")
			return
		player_name += PAGES[page][cursor.y * COLS + cursor.x]
		Audio.sfx("confirm")
		# depois da primeira letra maiúscula, passa para minúsculas
		if player_name.length() == 1 and page == 0:
			page = 1
		if player_name.length() >= MAX_LEN:
			cursor = Vector2i(2, rows())
	_refresh()


func _delete_or_cancel() -> void:
	if player_name.is_empty():
		Audio.sfx("cancel")
		_finish("")
		return
	player_name = player_name.substr(0, player_name.length() - 1)
	if player_name.is_empty():
		page = 0
	Audio.sfx("cancel")
	_refresh()


func _confirm() -> void:
	var final := player_name.strip_edges()
	if final.is_empty():
		final = tr("NAME_DEFAULT")
	Audio.sfx("save")
	_finish(final)


func _finish(value: String) -> void:
	if _done:
		return
	_done = true
	confirmed.emit(value)
	close()


func _on_cell_input(event: InputEvent, pos: Vector2i) -> void:
	if not accepts_input():
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		accept_event()
		cursor = pos
		_select()


func on_back() -> void:
	_delete_or_cancel()


func _notification(what: int) -> void:
	if what == NOTIFICATION_TRANSLATION_CHANGED and _name_label:
		_refresh()
