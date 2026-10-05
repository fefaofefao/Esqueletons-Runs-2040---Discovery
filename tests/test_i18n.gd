extends "res://tests/test_case.gd"
## Idiomas: chaves nos 3 idiomas, troca em tempo real e idioma do aparelho.

const LANGS := ["pt_BR", "en", "es"]


func test_every_key_translated_at_runtime() -> void:
	var all := all_translations()
	check(all.size() > 50, "CSV de tradução carregado")
	var old := TranslationServer.get_locale()
	for lang in LANGS:
		TranslationServer.set_locale(lang)
		for key in all.keys():
			var t := TranslationServer.translate(key)
			if t == key or t.strip_edges() == "":
				check(false, "%s sem tradução em %s" % [key, lang])
	TranslationServer.set_locale(old)


func test_switch_language_without_restart() -> void:
	var old: String = Settings.values.language
	Settings.set_value("language", "es")
	check_eq(TranslationServer.translate("MENU_NEW_GAME"), "Nueva partida", "espanhol")
	Settings.set_value("language", "en")
	check_eq(TranslationServer.translate("MENU_NEW_GAME"), "New game", "inglês")
	Settings.set_value("language", "pt_BR")
	check_eq(TranslationServer.translate("MENU_NEW_GAME"), "Novo jogo", "português")
	Settings.set_value("language", old)


func test_device_language_fallback() -> void:
	check(Settings.device_language() in LANGS, "idioma do aparelho sempre mapeia para um dos 3")
	check_eq(str(ProjectSettings.get_setting("internationalization/locale/fallback")), "en", "fallback inglês")


func test_font_has_all_characters() -> void:
	var font := UiTheme.font()
	var missing := {}
	for entry in all_translations().values():
		for lang in LANGS:
			for ch in str(entry[lang]):
				if ch == "\n" or ch == " ":
					continue
				if not font.has_char(ch.unicode_at(0)):
					missing[ch] = true
	check(missing.is_empty(), "fonte sem os caracteres: %s" % ", ".join(PackedStringArray(missing.keys())))
	for ch in "áéíóúâêôãõçñÁÉÍÓÚÂÊÔÃÕÇÑ¿¡üÜ":
		check(font.has_char(ch.unicode_at(0)), "fonte com '%s'" % ch)
