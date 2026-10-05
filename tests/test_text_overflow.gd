extends "res://tests/test_case.gd"
## Overflow de texto: cada texto cabe no seu espaço nos 3 idiomas, e o
## PT-BR (origem) deixa 30% de folga para traduções mais longas.

const LANGS := ["pt_BR", "en", "es"]
## Textos exibidos na caixa de diálogo (até 3 linhas de 288 px).
const DIALOG_PREFIXES := ["DLG_", "SIGN_", "OBJ_", "MSG_", "CREDITS_"]
const DIALOG_KEYS := ["SET_PRIVACY_INFO", "ABOUT_PRIVACY_PENDING", "DBG_TIMES_EMPTY", "DBG_SAVE_DELETED"]
## Perguntas da ChoiceBox (206 px, até 4 linhas).
const CHOICE_PREFIXES := ["CONFIRM_"]
## Nomes de lugares (letreiro e teleporte do debug).
const PLACE_PREFIXES := ["REGION_", "MAP_"]
const PLACE_WIDTH := 240.0
## Valores exibidos como "< valor >" na coluna de valores.
const VALUE_PREFIXES := ["LANG_NAME_", "VAL_", "SET_TEXT_SLOW", "SET_TEXT_NORMAL", "SET_TEXT_FAST"]
## Fora do teste (texto montado com dados de fora ou só de debug).
const SKIP_KEYS := ["DBG_TIMES_BODY", "ABOUT_VERSION", "ABOUT_PRODUCER", "ABOUT_CONTACT", "ABOUT_SITE", "NAME_DEFAULT", "SPK_BENTO"]
## Pior caso do nome do jogador (10 caracteres largos).
const WORST_NAME := "WWWWWWWWWW"


func _has_prefix(key: String, prefixes: Array) -> bool:
	for p in prefixes:
		if key.begins_with(p):
			return true
	return false


func _fill(text: String) -> String:
	return text.format({"player": WORST_NAME, "n": 3})


func test_texts_fit() -> void:
	var all := all_translations()
	for key: String in all.keys():
		if key in SKIP_KEYS:
			continue
		for lang in LANGS:
			var text := _fill(str(all[key][lang]))
			var is_pt: bool = lang == "pt_BR"
			if _has_prefix(key, DIALOG_PREFIXES) or key in DIALOG_KEYS:
				var lines := TextFit.wrap_lines(text, UiTheme.DIALOG_TEXT_WIDTH).size()
				check(lines <= UiTheme.DIALOG_LINES, "%s [%s] usa %d linhas (máx. %d)" % [key, lang, lines, UiTheme.DIALOG_LINES])
				if is_pt and not key.begins_with("DBG_"):
					var slack := TextFit.wrap_lines(text, UiTheme.DIALOG_TEXT_WIDTH / UiTheme.TEXT_GROWTH).size()
					check(slack <= UiTheme.DIALOG_LINES, "%s [pt_BR] sem 30%% de folga (%d linhas a 1/1,3 da largura)" % [key, slack])
			elif _has_prefix(key, CHOICE_PREFIXES):
				var lines := TextFit.wrap_lines(text, 206.0).size()
				check(lines <= 4, "%s [%s] usa %d linhas na pergunta" % [key, lang, lines])
			elif _has_prefix(key, PLACE_PREFIXES):
				_check_width(key, lang, text, PLACE_WIDTH, is_pt)
			elif _has_prefix(key, VALUE_PREFIXES):
				_check_width(key, lang, "< %s >" % text, UiTheme.MENU_VALUE_WIDTH, is_pt)
			else:
				_check_width(key, lang, text, UiTheme.MENU_LABEL_WIDTH, is_pt and not key.begins_with("DBG_"))


func _check_width(key: String, lang: String, text: String, limit: float, need_slack: bool) -> void:
	var w := UiTheme.text_width(text)
	check(w <= limit, "%s [%s] tem %.0f px (máx. %.0f): '%s'" % [key, lang, w, limit, text])
	if need_slack:
		check(w * UiTheme.TEXT_GROWTH <= limit, "%s [pt_BR] sem 30%% de folga: %.0f px × 1,3 > %.0f" % [key, w, limit])


func test_wrap_respects_width() -> void:
	var text := "Uma frase longa o bastante para quebrar em várias linhas dentro da caixa de diálogo do jogo."
	for line in TextFit.wrap_lines(text, 120.0):
		check(UiTheme.text_width(line) <= 120.0, "linha cabe: '%s'" % line)
	var pages := TextFit.paginate(text + " " + text + " " + text, 120.0, 3)
	check(pages.size() > 1, "paginação cria mais de uma caixa quando precisa")
	for p in pages:
		check(p.split("\n").size() <= 3, "cada página tem até 3 linhas")


## Botões HD da tela inicial (fonte Nunito): o texto cabe com folga nos 3 idiomas.
func test_title_buttons_fit() -> void:
	var f := FontVariation.new()
	f.base_font = load("res://assets/fonts/nunito/Nunito.ttf")
	f.variation_opentype = {TextServerManager.get_primary_interface().name_to_tag("wght"): 850}
	var all := all_translations()
	var specs := [
		["MENU_CONTINUE", 11, 118.0 - 18.0, true],
		["MENU_NEW_GAME", 11, 118.0 - 18.0, true],
		["MENU_NEW_GAME", 8, 86.0 - 14.0, false],
		["MENU_SETTINGS", 8, 86.0 - 14.0, false],
		["MENU_ABOUT", 8, 86.0 - 14.0, false],
	]
	for spec in specs:
		for lang in LANGS:
			var text := str(all[spec[0]][lang])
			if spec[3]:
				text = text.to_upper()
			var w := f.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, spec[1]).x
			check(w <= spec[2], "título: %s [%s] %.1f > %.1f" % [spec[0], lang, w, spec[2]])
			if lang == "pt_BR":
				check(w * UiTheme.TEXT_GROWTH <= spec[2], "título: %s [pt_BR] sem 30%% de folga (%.1f)" % [spec[0], w])
