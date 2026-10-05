class_name DialogBox
extends Overlay
## Caixa de diálogo com efeito de máquina de escrever, até 3 linhas por caixa,
## quebra automática e paginação de segurança. A acelera o texto / avança.
##
## Roteiro (lista de nós vindos de data/dialogs/*.json):
##   {"say": KEY, "speaker": KEY?, "args": {}?}
##   {"choice": [{"text": KEY, "goto": "arquivo/id"?, "set_flag": "flag"?}], "say": KEY?, "speaker": KEY?}
##   {"set_flag": "nome", "value": true?}
##   {"goto": "arquivo/id"}
##   {"action": "nome", ...}  ação de roteiro (batalha, loja, dar parceiro...):
##       a caixa fecha, o Game executa a ação e reabre o diálogo no nó seguinte
##       (ver Game.play_script e docs/DADOS.md).
## Qualquer nó aceita "if": "flag" ou "if_not": "flag".

signal choice_made(index: int)

var _script: Array = []
## Ação encontrada (o Game executa e continua com pending_rest).
var pending_action: Dictionary = {}
var pending_rest: Array = []
var _node_i := -1
var _pages := PackedStringArray()
var _page_i := 0
var _shown := 0.0
var _typing := false
var _waiting_choice := false
var _blink := 0.0

var _panel: PanelContainer
var _text: Label
var _name_panel: PanelContainer
var _name_label: Label
var _arrow: Label
var _choice: MenuList
var _choice_panel: PanelContainer


func setup(script_nodes: Array) -> void:
	_script = script_nodes.duplicate(true)


func _ready() -> void:
	_build()
	_panel.visible = false
	_name_panel.visible = false
	_advance_node()


func _build() -> void:
	var box_w := UiTheme.DIALOG_TEXT_WIDTH + 14
	var box_h := UiTheme.LINE_HEIGHT * UiTheme.DIALOG_LINES + 10
	_panel = PanelContainer.new()
	_panel.mouse_filter = Control.MOUSE_FILTER_STOP
	_panel.custom_minimum_size = Vector2(box_w, box_h)
	_panel.size = _panel.custom_minimum_size
	_panel.gui_input.connect(_on_panel_input)
	add_child(_panel)
	_text = UiTheme.label()
	_text.vertical_alignment = VERTICAL_ALIGNMENT_TOP
	_text.custom_minimum_size = Vector2(UiTheme.DIALOG_TEXT_WIDTH, UiTheme.LINE_HEIGHT * UiTheme.DIALOG_LINES)
	_panel.add_child(_text)
	_name_panel = PanelContainer.new()
	_name_panel.add_theme_stylebox_override("panel", UiTheme.frame("name"))
	_name_label = UiTheme.label("", UiTheme.TEXT_ACCENT)
	_name_panel.add_child(_name_label)
	add_child(_name_panel)
	_arrow = UiTheme.label("▼", UiTheme.TEXT_ACCENT)
	add_child(_arrow)
	_layout()
	get_viewport().size_changed.connect(_layout)
	if Game.touch:
		Game.touch.layout_changed.connect(_layout)


## Com controles de toque visíveis a caixa sobe para o topo, para não ficar sob o D-pad.
func _layout() -> void:
	var vp := get_viewport_rect().size
	var at_top := Game.touch != null and Game.touch.pad_visible()
	var x := floorf((vp.x - _panel.size.x) / 2.0)
	var y := 22.0 if at_top else vp.y - _panel.size.y - 4.0
	_panel.position = Vector2(x, y)
	_name_panel.position = Vector2(x + 6, y - 15 if not at_top else y + _panel.size.y - 2)
	_arrow.position = Vector2(x + _panel.size.x - 14, y + _panel.size.y - 15)
	if _choice_panel:
		_choice_panel.position = Vector2(x + _panel.size.x - _choice_panel.size.x, (y - _choice_panel.size.y - 2) if not at_top else (y + _panel.size.y + 2))


func _process(delta: float) -> void:
	_blink += delta
	_arrow.visible = not _typing and not _waiting_choice and fmod(_blink, 0.8) < 0.5
	if not _typing:
		return
	_shown += delta * Settings.text_cps()
	var total := _text.get_total_character_count()
	var before := _text.visible_characters
	_text.visible_characters = mini(int(_shown), total)
	if _text.visible_characters != before and _text.visible_characters % 2 == 0:
		Audio.sfx("text", 45)
	if _text.visible_characters >= total:
		_finish_page()


func _unhandled_input(event: InputEvent) -> void:
	if not accepts_input() or _waiting_choice:
		return
	if event.is_action_pressed("btn_a", false) or event.is_action_pressed("btn_b", false):
		get_viewport().set_input_as_handled()
		_press()


func _on_panel_input(event: InputEvent) -> void:
	if not accepts_input() or _waiting_choice:
		return
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		accept_event()
		_press()


func _press() -> void:
	if _typing:
		# A acelera: completa a caixa atual de uma vez
		_text.visible_characters = -1
		_finish_page()
		return
	Audio.sfx("cursor")
	_page_i += 1
	if _page_i < _pages.size():
		_show_page()
	else:
		_advance_node()


func _finish_page() -> void:
	_typing = false
	_text.visible_characters = -1
	if _page_i == _pages.size() - 1 and _current_node().has("choice"):
		_open_choice()


func _current_node() -> Dictionary:
	if _node_i < 0 or _node_i >= _script.size():
		return {}
	return _script[_node_i]


func _advance_node() -> void:
	while true:
		_node_i += 1
		if _node_i >= _script.size():
			close()
			return
		var n: Dictionary = _script[_node_i]
		if n.has("if") and not SaveGame.get_flag(str(n["if"])):
			continue
		if n.has("if_not") and SaveGame.get_flag(str(n["if_not"])):
			continue
		if n.has("set_flag") and not n.has("say") and not n.has("choice"):
			SaveGame.set_flag(str(n["set_flag"]), bool(n.get("value", true)))
			continue
		if n.has("action"):
			pending_action = n
			pending_rest = _script.slice(_node_i + 1)
			close()
			return
		if n.has("goto"):
			_jump(str(n["goto"]))
			return
		if n.has("say") or n.has("choice"):
			_start_node(n)
			return


func _jump(ref: String) -> void:
	_script = Data.dialog(ref).duplicate(true)
	_node_i = -1
	_advance_node()


func _start_node(n: Dictionary) -> void:
	_panel.visible = true
	var speaker := str(n.get("speaker", ""))
	_name_panel.visible = speaker != ""
	_name_label.text = tr(speaker) if speaker != "" else ""
	_name_panel.reset_size()
	var text := ""
	if n.has("say"):
		text = format_text(str(n["say"]), n.get("args", {}))
	_pages = TextFit.paginate(text, UiTheme.DIALOG_TEXT_WIDTH, UiTheme.DIALOG_LINES)
	_page_i = 0
	_show_page()


static func format_text(key: String, args: Dictionary = {}) -> String:
	var vars := {"player": SaveGame.player_name()}
	vars.merge(args, true)
	return TranslationServer.translate(key).format(vars)


func _show_page() -> void:
	_text.text = _pages[_page_i]
	_text.visible_characters = 0
	_shown = 0.0
	_typing = true
	_blink = 0.0


func _open_choice() -> void:
	_waiting_choice = true
	var options: Array = _current_node()["choice"]
	_choice_panel = PanelContainer.new()
	_choice_panel.mouse_filter = Control.MOUSE_FILTER_STOP
	_choice = MenuList.new()
	_choice.overlay = self
	var list := []
	for i in options.size():
		list.append({"id": str(i), "key": str(options[i].get("text", ""))})
	_choice.set_items(list)
	_choice.activated.connect(_on_choice)
	_choice_panel.add_child(_choice)
	add_child(_choice_panel)
	_choice_panel.reset_size()
	_layout()


func _on_choice(id: String) -> void:
	var i := int(id)
	var opt: Dictionary = _current_node()["choice"][i]
	_choice_panel.queue_free()
	_choice_panel = null
	_choice = null
	_waiting_choice = false
	choice_made.emit(i)
	if opt.has("set_flag"):
		SaveGame.set_flag(str(opt["set_flag"]), true)
	if opt.has("goto"):
		_jump(str(opt["goto"]))
	else:
		_advance_node()


func on_back() -> void:
	if not _waiting_choice:
		_press()
