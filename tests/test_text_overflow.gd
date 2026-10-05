extends "res://tests/test_case.gd"
## Overflow de texto: cada texto cabe no seu espaço nos 3 idiomas, e o
## PT-BR (origem) deixa 30% de folga para traduções mais longas.

const LANGS := ["pt_BR", "en", "es"]
## Textos exibidos na caixa de diálogo (até 3 linhas de 288 px).
const DIALOG_PREFIXES := ["DLG_", "SIGN_", "OBJ_", "MSG_", "CREDITS_", "OSS_"]
const DIALOG_KEYS := ["DBG_TEAM_GIVEN", "SET_PRIVACY_INFO", "ABOUT_PRIVACY_PENDING", "DBG_TIMES_EMPTY", "DBG_SAVE_DELETED", "DBG_GROWTH_TEAM_GIVEN"]
## Perguntas da ChoiceBox (206 px, até 4 linhas).
const CHOICE_PREFIXES := ["CONFIRM_", "RECRUIT_ASK"]
## Nomes de lugares (letreiro e teleporte do debug).
const PLACE_PREFIXES := ["REGION_", "MAP_"]
const PLACE_WIDTH := 240.0
## Valores exibidos como "< valor >" na coluna de valores.
const VALUE_PREFIXES := ["LANG_NAME_", "VAL_", "SET_TEXT_SLOW", "SET_TEXT_NORMAL", "SET_TEXT_FAST"]
## Fora do teste (texto montado com dados de fora ou só de debug).
## Batalha: mensagens (log de 3 linhas), prévia do golpe, descrições e listas.
const BATTLE_LOG_PREFIXES := ["BTL_WILD", "BTL_TAMER_", "BTL_GO", "BTL_COME", "BTL_USED", "BTL_MISS", "BTL_NO_", "BTL_CRIT",
	"BTL_EFF_STRONG_MSG", "BTL_EFF_WEAK_MSG", "BTL_POISON", "BTL_ALREADY", "BTL_STAT_", "BTL_HEALED", "BTL_CURED",
	"BTL_REVIVED", "BTL_ITEM_USED", "BTL_FAINT", "BTL_XP", "BTL_LEVEL_UP", "BTL_LEARNED", "BTL_LEARN_PROMPT",
	"BTL_DID_NOT", "BTL_FLED", "BTL_FLEE", "BTL_CANT", "BTL_WIN", "BTL_MONEY", "BTL_LOSE", "BTL_SINTONIA", "BTL_DELAYED",
	"BTL_GOLDEN_APPEARS", "RECRUIT_MARKER", "RECRUIT_JOINED", "RECRUIT_TO_RANCH", "RECRUIT_REFUSED"]
## Cerimônia de crescimento: balão de uma linha e texto de até 2 linhas.
const BALLOON_WIDTH := 240.0
## Cabeçalho do Ossário (painel de 280 px).
const OSS_HEADER_WIDTH := 260.0
const PREVIEW_PREFIXES := ["TYPE_", "BTL_EFF_STRONG", "BTL_EFF_NORMAL", "BTL_EFF_WEAK", "BTL_TARGET_", "BTL_WEIGHT_", "BTL_DETAIL", "BTL_AGE"]
## Nome de esqueleto/golpe no pior caso para as mensagens da batalha.
const WORST_UNIT := "Wwwwwwwwwww"
const SKIP_KEYS := ["BTL_LOSE_MONEY", "BTL_NO_PARTY", "DBG_TIMES_BODY", "ABOUT_VERSION", "ABOUT_PRODUCER", "ABOUT_CONTACT", "ABOUT_SITE", "NAME_DEFAULT", "SPK_BENTO"]
## Pior caso do nome do jogador (10 caracteres largos).
const WORST_NAME := "WWWWWWWWWW"


func _has_prefix(key: String, prefixes: Array) -> bool:
	for p in prefixes:
		if key.begins_with(p):
			return true
	return false


func _fill(text: String) -> String:
	return text.format({"player": WORST_NAME, "n": 30, "name": WORST_UNIT, "user": WORST_UNIT, "a": WORST_UNIT, "b": WORST_UNIT,
		"move": "Wwwwwwwwwww", "item": "Wwwwwwwww", "tamer": "Wwwwwwwwwwwww", "stat": "WWW", "p": 100, "acc": 100,
		"species": WORST_UNIT, "r": 100, "t": 100, "g": 100})


func test_texts_fit() -> void:
	var all := all_translations()
	for key: String in all.keys():
		if key in SKIP_KEYS:
			continue
		for lang in LANGS:
			var text := _fill(str(all[key][lang]))
			var is_pt: bool = lang == "pt_BR"
			if key.ends_with("_DESC"):
				# golpes: 2ª linha da faixa = "Alvo: ... · descrição"; itens: descrição sozinha
				# a folga de 30% vale para a descrição; o prefixo do alvo é fixo
				var tkey := _target_key_for_desc(key)
				var prefix := (str(all[tkey][lang]) + " · ") if tkey != "" else ""
				var w := UiTheme.text_width(prefix + text)
				check(w <= BattleLog.TEXT_WIDTH, "%s [%s] não cabe na faixa (%.0f px): '%s'" % [key, lang, w, prefix + text])
				if is_pt:
					var grown := UiTheme.text_width(prefix) + UiTheme.text_width(text) * UiTheme.TEXT_GROWTH
					check(grown <= BattleLog.TEXT_WIDTH, "%s [pt_BR] sem 30%% de folga na descrição (%.0f px)" % [key, grown])
			elif key.begins_with("BTL_EFF_") and key.ends_with("_MSG") or (_has_prefix(key, BATTLE_LOG_PREFIXES) and not _has_prefix(key, PREVIEW_PREFIXES)):
				var lines := TextFit.wrap_lines(text, BattleLog.TEXT_WIDTH).size()
				check(lines <= BattleLog.LINES, "%s [%s] usa %d linhas no log da batalha" % [key, lang, lines])
			elif key == "BTL_DETAIL":
				var worst := str(all[key][lang]).format({"type": _longest(all, ["TYPE_FISICO", "TYPE_MAGICO", "TYPE_CURA", "TYPE_VENENO"], lang),
					"p": 120, "acc": 100, "weight": _longest(all, ["BTL_WEIGHT_LIGHT", "BTL_WEIGHT_NORMAL", "BTL_WEIGHT_HEAVY"], lang)})
				_check_width(key, lang, worst, BattleLog.TEXT_WIDTH, is_pt)
			elif key == "GROW_BIRTHDAY":
				_check_width(key, lang, text, BALLOON_WIDTH, is_pt)
			elif key == "GROW_DONE":
				var lines := TextFit.wrap_lines(text, UiTheme.DIALOG_TEXT_WIDTH).size()
				check(lines <= 2, "%s [%s] usa %d linhas na cerimônia" % [key, lang, lines])
			elif key == "OSS_HEADER":
				_check_width(key, lang, text, OSS_HEADER_WIDTH, false)
			elif key.begins_with("BTL_AGE"):
				_check_width(key, lang, text.replace("30", "100"), UnitCard.W - 34.0, false)
			elif _has_prefix(key, PREVIEW_PREFIXES):
				_check_width(key, lang, text, 120.0, is_pt)
			elif _has_prefix(key, DIALOG_PREFIXES) or key in DIALOG_KEYS:
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


## Nomes de esqueletos (bonecos de teste e, na fase 3, as espécies) cabem na caixa da batalha.
func test_species_names_fit_panel() -> void:
	var all := all_translations()
	for id in Data.all_species_ids():
		var key := str(Data.species(id).get("name_key", ""))
		for lang in LANGS:
			var name := str(all.get(key, {}).get(lang, ""))
			check(UiTheme.text_width(name) <= UnitCard.NAME_WIDTH, "nome %s [%s] '%s' não cabe na caixa (%.0f px)" % [id, lang, name, UiTheme.text_width(name)])


func _longest(all: Dictionary, keys: Array, lang: String) -> String:
	var best := ""
	for k in keys:
		var t := str(all[k][lang])
		if UiTheme.text_width(t) > UiTheme.text_width(best):
			best = t
	return best


## Chave do texto de alvo do golpe que usa esta descrição ("" se não for golpe).
func _target_key_for_desc(desc_key: String) -> String:
	if desc_key == "BTL_STRUGGLE_DESC":
		return "BTL_TARGET_ENEMY"
	for path in ["res://data/moves.json", "res://data/test/moves_test.json"]:
		if not FileAccess.file_exists(path):
			continue
		var d = Data.load_json(path)
		var lst = d.get("moves", {})
		for mv in (lst.values() if lst is Dictionary else lst):
			if str(mv.get("desc_key", "")) == desc_key:
				return "BTL_TARGET_" + str(mv.get("target", "enemy")).to_upper()
	return ""
