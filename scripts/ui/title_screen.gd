class_name TitleScreen
extends Node2D
## Tela inicial: a Praia ao fundo com a câmera passeando, logo, edição e menu
## (Continuar, Novo jogo, Configurações, Sobre). Três toques no logo abrem o
## menu de debug (só em build de debug).

const TAPS_FOR_DEBUG := 3
const TAP_WINDOW_MS := 1200

var _map: MapView
var _camera: Camera2D
var _menu: MenuList
var _ui: CanvasLayer
var _logo: TextureRect
var _edition: Label
var _pan_t := 0.0
var _taps: Array[int] = []


func _ready() -> void:
	_map = MapView.new()
	add_child(_map)
	_map.build("praia_despertar")
	var tint := CanvasModulate.new()
	tint.color = Color(0.92, 0.86, 0.95)
	add_child(tint)
	_camera = Camera2D.new()
	add_child(_camera)
	_camera.make_current()
	_ui = CanvasLayer.new()
	_ui.layer = 4
	add_child(_ui)
	var root := Control.new()
	root.set_anchors_preset(Control.PRESET_FULL_RECT)
	root.mouse_filter = Control.MOUSE_FILTER_IGNORE
	root.theme = UiTheme.build()
	_ui.add_child(root)
	var col := VBoxContainer.new()
	col.set_anchors_preset(Control.PRESET_FULL_RECT)
	col.alignment = BoxContainer.ALIGNMENT_CENTER
	col.mouse_filter = Control.MOUSE_FILTER_IGNORE
	col.add_theme_constant_override("separation", 2)
	root.add_child(col)
	_logo = TextureRect.new()
	_logo.texture = load("res://assets/ui/logo.png")
	_logo.stretch_mode = TextureRect.STRETCH_KEEP_CENTERED
	_logo.mouse_filter = Control.MOUSE_FILTER_STOP
	_logo.gui_input.connect(_on_logo_input)
	col.add_child(_logo)
	_edition = UiTheme.label("", Color8(255, 214, 120))
	_edition.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	_edition.add_theme_color_override("font_shadow_color", Color8(40, 30, 48))
	_edition.add_theme_constant_override("shadow_offset_x", 1)
	_edition.add_theme_constant_override("shadow_offset_y", 1)
	col.add_child(_edition)
	var spacer := Control.new()
	spacer.custom_minimum_size.y = 4
	col.add_child(spacer)
	var center := CenterContainer.new()
	center.mouse_filter = Control.MOUSE_FILTER_IGNORE
	col.add_child(center)
	var panel := PanelContainer.new()
	panel.custom_minimum_size.x = 130
	center.add_child(panel)
	_menu = MenuList.new()
	panel.add_child(_menu)
	_menu.activated.connect(_on_activated)
	var version := UiTheme.label("v" + str(ProjectSettings.get_setting("application/config/version", "")), UiTheme.TEXT_LIGHT)
	version.set_anchors_preset(Control.PRESET_BOTTOM_RIGHT)
	version.position = Vector2(-4, -14)
	version.grow_horizontal = Control.GROW_DIRECTION_BEGIN
	version.grow_vertical = Control.GROW_DIRECTION_BEGIN
	version.modulate.a = 0.7
	root.add_child(version)
	_refresh_texts()
	_build_menu()


func _build_menu() -> void:
	var items := []
	if SaveGame.has_save():
		items.append({"id": "continue", "key": "MENU_CONTINUE"})
	items.append({"id": "new", "key": "MENU_NEW_GAME"})
	items.append({"id": "settings", "key": "MENU_SETTINGS"})
	items.append({"id": "about", "key": "MENU_ABOUT"})
	_menu.set_items(items)


func _refresh_texts() -> void:
	var ed: Dictionary = Data.publisher().get("edition", {})
	_edition.text = str(ed.get(Settings.current_language(), ed.get("en", "")))


func _notification(what: int) -> void:
	if what == NOTIFICATION_TRANSLATION_CHANGED and _edition:
		_refresh_texts()


func _process(delta: float) -> void:
	if _map == null or _map.size == Vector2i.ZERO:
		return
	_pan_t += delta * 0.05
	var vp := get_viewport_rect().size
	var mp := _map.pixel_size()
	var x := lerpf(vp.x / 2.0, mp.x - vp.x / 2.0, 0.5 + 0.5 * sin(_pan_t))
	_camera.position = Vector2(roundf(x), roundf(clampf(mp.y * 0.55, vp.y / 2.0, mp.y - vp.y / 2.0)))


func _on_activated(id: String) -> void:
	match id:
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
	var now := Time.get_ticks_msec()
	_taps.append(now)
	_taps = _taps.filter(func(t: int) -> bool: return now - t <= TAP_WINDOW_MS)
	if _taps.size() >= TAPS_FOR_DEBUG:
		_taps.clear()
		Game.open_debug()
