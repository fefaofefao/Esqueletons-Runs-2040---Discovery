class_name TeamMenu
extends Overlay
## Equipe (menu de pausa): lista com idade e PV; A abre a ficha (sprite,
## tipo, atributos, golpes); na ficha, A troca a ordem (vira o 1º do time).

var _menu: MenuList
var _detail: Control


func _init() -> void:
	super._init()
	pauses_game = true


func _ready() -> void:
	dim_background(0.45)
	var panel := centered_panel(240)
	var box := VBoxContainer.new()
	panel.add_child(box)
	box.add_child(UiTheme.label(tr("TEAM_TITLE"), UiTheme.TEXT_ACCENT))
	_menu = MenuList.new()
	_menu.overlay = self
	_menu.label_width = 120
	box.add_child(_menu)
	_menu.activated.connect(_on_activated)
	_menu.cancelled.connect(close)
	_fill()


func _fill() -> void:
	var items := []
	var party: Array = SaveGame.data.get("party", [])
	for i in party.size():
		var m := Monster.from_dict(party[i])
		items.append({"id": str(i), "key": ("★" if m.golden else "") + m.display_name(),
			"value": func() -> String: return "%s · %d/%d" % [UnitCard.age_text(m.level), m.hp, m.max_hp()], "fixed": true})
	if party.is_empty():
		items.append({"id": "_none", "key": "TEAM_EMPTY", "enabled": false})
	items.append({"id": "_back", "key": "SET_BACK"})
	_menu.set_items(items, _menu.index)


func _on_activated(id: String) -> void:
	if id == "_back":
		close()
		return
	var party: Array = SaveGame.data.get("party", [])
	var i := int(id)
	var sheet := TeamSheet.new().setup(Monster.from_dict(party[i]), i)
	Game.open_overlay(sheet)
	var lead: bool = await sheet.done
	if lead and i > 0:
		var m = party[i]
		party.remove_at(i)
		party.insert(0, m)
		SaveGame.data["party"] = party
		_menu.index = 0
	_fill()
