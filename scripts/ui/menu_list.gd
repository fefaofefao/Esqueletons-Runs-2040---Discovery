class_name MenuList
extends VBoxContainer
## Lista de opções navegável por D-pad/teclado/gamepad e por toque.
## Cada item: {id, key, enabled?, value?: Callable -> String, suffix?: String}
## Itens com "value" aceitam esquerda/direita para trocar o valor
## (exceto com "fixed": true, que só exibe o valor).

signal activated(id: String)
signal cancelled
signal value_step(id: String, direction: int)
signal selection_changed(index: int)

const REPEAT_DELAY_MS := 320
const REPEAT_RATE_MS := 85

var items: Array = []
var index := 0
## Overlay dono (só aceita entrada quando ele está no topo). Nulo = sempre ativo.
var overlay: Overlay = null
var light_text := false
var label_width := 0.0
## Máximo de linhas visíveis (0 = todas). Acima disso a lista rola.
var max_visible := 0
## Espaço entre linhas e altura mínima de cada linha (em px). Na batalha, linhas
## mais altas para o toque.
var row_spacing := 0
var row_height := 0
var _offset := 0

var _rows: Array = []
var _held_v := 0
var _held_h := 0
var _next_v := 0
var _next_h := 0
var _was_active := false


func _init() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	add_theme_constant_override("separation", 0)


func set_items(list: Array, start_index: int = 0) -> void:
	items = list
	index = clampi(start_index, 0, maxi(0, items.size() - 1))
	_build()
	_ensure_enabled(1)
	refresh()


func current_id() -> String:
	return "" if items.is_empty() else str(items[index].get("id", ""))


func _build() -> void:
	add_theme_constant_override("separation", row_spacing)
	for c in get_children():
		c.queue_free()
	_rows.clear()
	for i in items.size():
		var row := HBoxContainer.new()
		row.mouse_filter = Control.MOUSE_FILTER_STOP
		if row_height > 0:
			row.custom_minimum_size.y = row_height
		row.add_theme_constant_override("separation", 1)
		var cursor := UiTheme.label("▶")
		cursor.custom_minimum_size.x = 7
		var text := UiTheme.label()
		if label_width > 0.0:
			text.custom_minimum_size.x = label_width
		text.size_flags_horizontal = Control.SIZE_EXPAND_FILL
		var value := UiTheme.label()
		value.horizontal_alignment = HORIZONTAL_ALIGNMENT_RIGHT
		row.add_child(cursor)
		row.add_child(text)
		row.add_child(value)
		row.gui_input.connect(_on_row_input.bind(i))
		add_child(row)
		_rows.append({"row": row, "cursor": cursor, "text": text, "value": value})


func refresh() -> void:
	if max_visible > 0:
		if index < _offset:
			_offset = index
		elif index >= _offset + max_visible:
			_offset = index - max_visible + 1
		_offset = clampi(_offset, 0, maxi(0, items.size() - max_visible))
	for i in _rows.size():
		(_rows[i].row as Control).visible = max_visible <= 0 or (i >= _offset and i < _offset + max_visible)
		var item: Dictionary = items[i]
		var r: Dictionary = _rows[i]
		var enabled: bool = item.get("enabled", true)
		var base := UiTheme.TEXT_LIGHT if light_text else UiTheme.TEXT_DARK
		var col := base if enabled else UiTheme.TEXT_DISABLED
		var txt := tr(str(item.get("key", "")))
		if item.has("suffix"):
			txt += " " + str(item["suffix"])
		(r.text as Label).text = txt
		(r.text as Label).add_theme_color_override("font_color", UiTheme.TEXT_ACCENT if (i == index and enabled) else col)
		(r.cursor as Label).modulate.a = 1.0 if i == index else 0.0
		(r.cursor as Label).add_theme_color_override("font_color", UiTheme.TEXT_ACCENT)
		var vtext := ""
		if item.has("value") and item["value"] is Callable:
			var v := str((item["value"] as Callable).call())
			vtext = "< %s >" % v if i == index and not item.get("fixed", false) else v
		(r.value as Label).text = vtext
		(r.value as Label).add_theme_color_override("font_color", UiTheme.TEXT_VALUE if enabled else col)


func _notification(what: int) -> void:
	if what == NOTIFICATION_TRANSLATION_CHANGED and not _rows.is_empty():
		refresh()


func is_active() -> bool:
	if not is_visible_in_tree():
		return false
	if overlay == null:
		# menu de tela (ex.: título): ativo só quando não há overlay por cima
		return Game.top_overlay() == null and not Game.transitioning
	return overlay.accepts_input()


func _process(_delta: float) -> void:
	var active := is_active()
	var v := 0
	var h := 0
	if active:
		v = int(Input.is_action_pressed("move_down")) - int(Input.is_action_pressed("move_up"))
		h = int(Input.is_action_pressed("move_right")) - int(Input.is_action_pressed("move_left"))
	if active and not _was_active:
		# não reage a uma direção que já vinha pressionada antes de o menu abrir
		_held_v = v
		_held_h = h
		_next_v = Time.get_ticks_msec() + REPEAT_DELAY_MS
		_next_h = _next_v
	_was_active = active
	if not active:
		return
	var now := Time.get_ticks_msec()
	if v != 0 and (v != _held_v or now >= _next_v):
		_next_v = now + (REPEAT_DELAY_MS if v != _held_v else REPEAT_RATE_MS)
		move_cursor(v)
	_held_v = v
	if h != 0 and (h != _held_h or now >= _next_h):
		_next_h = now + (REPEAT_DELAY_MS if h != _held_h else REPEAT_RATE_MS)
		_step_value(h)
	_held_h = h


func _unhandled_input(event: InputEvent) -> void:
	if not is_active():
		return
	if event.is_action_pressed("btn_a", false):
		get_viewport().set_input_as_handled()
		activate_current()
	elif event.is_action_pressed("btn_b", false):
		get_viewport().set_input_as_handled()
		Audio.sfx("cancel")
		cancelled.emit()


func move_cursor(dir: int) -> void:
	if items.is_empty():
		return
	var start := index
	for _i in items.size():
		index = wrapi(index + dir, 0, items.size())
		if items[index].get("enabled", true):
			break
	if index != start:
		Audio.sfx("cursor")
		selection_changed.emit(index)
	refresh()


func _ensure_enabled(dir: int) -> void:
	if items.is_empty() or items[index].get("enabled", true):
		return
	for _i in items.size():
		index = wrapi(index + dir, 0, items.size())
		if items[index].get("enabled", true):
			return


func activate_current() -> void:
	if items.is_empty():
		return
	var item: Dictionary = items[index]
	if not item.get("enabled", true):
		Audio.sfx("bump")
		return
	if item.has("value") and not item.get("fixed", false):
		_step_value(1)
		return
	Audio.sfx("confirm")
	Haptics.tap()
	activated.emit(str(item.get("id", "")))


func _step_value(dir: int) -> void:
	if items.is_empty():
		return
	var item: Dictionary = items[index]
	if not item.has("value") or item.get("fixed", false) or not item.get("enabled", true):
		return
	Audio.sfx("cursor")
	value_step.emit(str(item.get("id", "")), dir)
	refresh()


func _on_row_input(event: InputEvent, i: int) -> void:
	if not is_active():
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		accept_event()
		if not items[i].get("enabled", true):
			Audio.sfx("bump")
			return
		if index != i:
			index = i
			selection_changed.emit(index)
		refresh()
		activate_current()
