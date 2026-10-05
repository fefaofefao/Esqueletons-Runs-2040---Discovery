class_name AboutScreen
extends Overlay
## Sobre: dados do config/publisher.json, versão, política de privacidade e créditos.

var _menu: MenuList
var _box: VBoxContainer
var _info: VBoxContainer


func _ready() -> void:
	dim_background(0.5)
	var panel := centered_panel(250)
	_box = VBoxContainer.new()
	panel.add_child(_box)
	_info = VBoxContainer.new()
	_box.add_child(_info)
	_menu = MenuList.new()
	_menu.overlay = self
	_box.add_child(_menu)
	_menu.set_items([
		{"id": "privacy", "key": "ABOUT_PRIVACY"},
		{"id": "credits", "key": "ABOUT_CREDITS"},
		{"id": "back", "key": "SET_BACK"},
	])
	_menu.activated.connect(_on_activated)
	_menu.cancelled.connect(close)
	_fill()


func _fill() -> void:
	for c in _info.get_children():
		c.queue_free()
	var p := Data.publisher()
	var ed: Dictionary = p.get("edition", {})
	var title := UiTheme.label("%s — %s" % [p.get("game_name", ""), ed.get(Settings.current_language(), "")], UiTheme.TEXT_ACCENT)
	_info.add_child(title)
	for line in [
		tr("ABOUT_VERSION").format({"v": ProjectSettings.get_setting("application/config/version", "")}),
		tr("ABOUT_PRODUCER").format({"v": p.get("producer", "")}),
		tr("ABOUT_CONTACT").format({"v": p.get("contact_email", "")}),
		tr("ABOUT_SITE").format({"v": p.get("website", "")}),
	]:
		_info.add_child(UiTheme.label(str(line)))
	_info.add_child(Control.new())


func _notification(what: int) -> void:
	if what == NOTIFICATION_TRANSLATION_CHANGED and _info:
		_fill()


func _on_activated(id: String) -> void:
	match id:
		"privacy":
			var url := str(Data.publisher().get("privacy_policy_url", ""))
			if url.contains("[") or url == "":
				await Game.show_message("ABOUT_PRIVACY_PENDING")
			else:
				OS.shell_open(url)
		"credits":
			await Game.show_dialog("sistema/creditos")
		"back":
			close()
