class_name PauseMenu
extends Overlay
## Pausa: Continuar, Configurações, Salvar e sair. O título do painel aceita
## três toques para abrir o menu de debug (só em build de debug).

var _menu: MenuList
var _taps: Array[int] = []


func _init() -> void:
	super._init()
	pauses_game = true


func _ready() -> void:
	dim_background(0.35)
	var panel := centered_panel(150)
	var box := VBoxContainer.new()
	panel.add_child(box)
	var title := UiTheme.label(tr("PAUSE_TITLE"), UiTheme.TEXT_ACCENT)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	title.mouse_filter = Control.MOUSE_FILTER_STOP
	title.gui_input.connect(_on_title_input)
	box.add_child(title)
	_menu = MenuList.new()
	_menu.overlay = self
	box.add_child(_menu)
	_menu.set_items([
		{"id": "resume", "key": "PAUSE_RESUME"},
		{"id": "team", "key": "PAUSE_TEAM"},
		{"id": "bag", "key": "PAUSE_BAG"},
		{"id": "ossuary", "key": "PAUSE_OSSUARY"},
		{"id": "settings", "key": "MENU_SETTINGS"},
		{"id": "quit", "key": "PAUSE_SAVE_QUIT"},
	])
	_menu.activated.connect(_on_activated)
	_menu.cancelled.connect(close)


func _on_activated(id: String) -> void:
	match id:
		"resume":
			close()
		"team":
			Game.open_overlay(TeamMenu.new())
		"bag":
			Game.open_overlay(BagMenu.new())
		"ossuary":
			Game.open_overlay(OssuaryScreen.new())
		"settings":
			Game.open_overlay(SettingsMenu.new())
		"quit":
			Game.autosave()
			Game.goto_title()


func _unhandled_input(event: InputEvent) -> void:
	if accepts_input() and event.is_action_pressed("btn_menu", false):
		get_viewport().set_input_as_handled()
		Audio.sfx("cancel")
		close()


func _on_title_input(event: InputEvent) -> void:
	if not (event is InputEventMouseButton and event.pressed):
		return
	var now := Time.get_ticks_msec()
	_taps.append(now)
	_taps = _taps.filter(func(t: int) -> bool: return now - t <= 1200)
	if _taps.size() >= 3:
		_taps.clear()
		Game.open_debug()
