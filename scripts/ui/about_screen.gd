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
		{"id": "feedback", "key": "ABOUT_FEEDBACK"},
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
			var url := privacy_url(Data.publisher(), Settings.current_language())
			if url.contains("[") or url == "":
				await Game.show_message("ABOUT_PRIVACY_PENDING")
			else:
				OS.shell_open(url)
		"feedback":
			OS.shell_open(feedback_mailto(Data.publisher()))
		"credits":
			await Game.show_dialog("sistema/creditos")
		"back":
			close()


## Política no idioma do jogo (o site tem uma página por idioma; PT é a padrão).
static func privacy_url(p: Dictionary, lang: String) -> String:
	var url := str(p.get("privacy_policy_url", ""))
	var page: String = {"en": "privacy.html", "es": "privacidad.html"}.get(lang, "")
	if page != "" and url.ends_with("/privacidade.html"):
		url = url.trim_suffix("privacidade.html") + page
	return url


## E-mail de feedback já com versão, aparelho e idioma (ajuda a reproduzir erros).
static func feedback_mailto(p: Dictionary) -> String:
	var version := str(ProjectSettings.get_setting("application/config/version", ""))
	var subject := "%s %s — feedback" % [p.get("game_name", ""), version]
	var body := "%s\n\n\n---\nv%s · %s · %s %s · %s" % [
		TranslationServer.translate("ABOUT_FEEDBACK_BODY"), version, OS.get_model_name(),
		OS.get_name(), OS.get_version(), Settings.current_language()]
	return "mailto:%s?subject=%s&body=%s" % [p.get("contact_email", ""), subject.uri_encode(), body.uri_encode()]
