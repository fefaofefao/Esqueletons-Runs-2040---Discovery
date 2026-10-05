class_name SettingsMenu
extends Overlay
## Configurações: idioma (troca na hora, sem reiniciar), música, efeitos,
## velocidade do texto, 2x padrão, vibração e privacidade e anúncios.

const VOLUME_STEP := 0.1

var _menu: MenuList
var _title: Label


func _init() -> void:
	super._init()
	pauses_game = true


func _ready() -> void:
	dim_background(0.45)
	var panel := centered_panel(UiTheme.MENU_LABEL_WIDTH + UiTheme.MENU_VALUE_WIDTH + 24)
	var box := VBoxContainer.new()
	panel.add_child(box)
	_title = UiTheme.label("", UiTheme.TEXT_ACCENT)
	_title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(_title)
	_menu = MenuList.new()
	_menu.overlay = self
	_menu.label_width = UiTheme.MENU_LABEL_WIDTH
	box.add_child(_menu)
	_menu.set_items([
		{"id": "language", "key": "SET_LANGUAGE", "value": func() -> String: return tr("LANG_NAME_" + Settings.current_language())},
		{"id": "music", "key": "SET_MUSIC", "value": func() -> String: return _pct("music_volume")},
		{"id": "sfx", "key": "SET_SFX", "value": func() -> String: return _pct("sfx_volume")},
		{"id": "text_speed", "key": "SET_TEXT_SPEED", "value": func() -> String: return tr("SET_TEXT_" + str(Settings.get_value("text_speed")).to_upper())},
		{"id": "fast", "key": "SET_FAST_DEFAULT", "value": func() -> String: return _onoff(Speed.fast)},
		{"id": "vibration", "key": "SET_VIBRATION", "value": func() -> String: return _onoff(bool(Settings.get_value("vibration")))},
		{"id": "privacy", "key": "SET_PRIVACY"},
		{"id": "back", "key": "SET_BACK"},
	])
	_menu.value_step.connect(_on_value_step)
	_menu.activated.connect(_on_activated)
	_menu.cancelled.connect(close)
	Speed.changed.connect(func(_m: float) -> void: _menu.refresh())
	_refresh_title()


func _refresh_title() -> void:
	_title.text = tr("SET_TITLE")


func _notification(what: int) -> void:
	if what == NOTIFICATION_TRANSLATION_CHANGED and _title:
		_refresh_title()


func _pct(key: String) -> String:
	return "%d%%" % roundi(float(Settings.get_value(key)) * 100.0)


func _onoff(v: bool) -> String:
	return tr("VAL_ON") if v else tr("VAL_OFF")


func _on_value_step(id: String, dir: int) -> void:
	match id:
		"language":
			Settings.cycle_language(dir)
		"music":
			Settings.set_value("music_volume", snappedf(clampf(float(Settings.get_value("music_volume")) + dir * VOLUME_STEP, 0.0, 1.0), 0.01))
		"sfx":
			Settings.set_value("sfx_volume", snappedf(clampf(float(Settings.get_value("sfx_volume")) + dir * VOLUME_STEP, 0.0, 1.0), 0.01))
			Audio.sfx("confirm")
		"text_speed":
			var i := Settings.TEXT_SPEEDS.find(str(Settings.get_value("text_speed")))
			Settings.set_value("text_speed", Settings.TEXT_SPEEDS[wrapi(i + dir, 0, Settings.TEXT_SPEEDS.size())])
		"fast":
			Speed.toggle()
		"vibration":
			Settings.set_value("vibration", not bool(Settings.get_value("vibration")))
			Haptics.tap()


func _on_activated(id: String) -> void:
	match id:
		"privacy":
			# Fase 5: reabre o formulário de consentimento do UMP.
			await Game.show_message("SET_PRIVACY_INFO")
		"back":
			close()
