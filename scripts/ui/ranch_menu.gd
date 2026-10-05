class_name RanchMenu
extends Overlay
## Rancho: cura gratuita e guarda os esqueletos que não cabem no time de 4.
## Escolha alguém da equipe para guardar, ou alguém do Rancho para levar
## (se o time estiver cheio, troca com o primeiro escolhido).

var _menu: MenuList
var _title: Label
var _picked := ""  # "p:i" ou "r:i" aguardando o par para trocar


func _init() -> void:
	super._init()
	pauses_game = true


func _ready() -> void:
	_heal_all()
	dim_background(0.55)
	var panel := centered_panel(250)
	var box := VBoxContainer.new()
	panel.add_child(box)
	_title = UiTheme.label("", UiTheme.TEXT_ACCENT)
	box.add_child(_title)
	_menu = MenuList.new()
	_menu.overlay = self
	_menu.label_width = 150
	_menu.max_visible = 9
	box.add_child(_menu)
	_menu.activated.connect(_on_activated)
	_menu.cancelled.connect(func() -> void:
		if _picked != "":
			_picked = ""
			_fill()
		else:
			close())
	_fill()


func _heal_all() -> void:
	for key in ["party", "ranch"]:
		var arr: Array = SaveGame.data.get(key, [])
		for i in arr.size():
			var m := Monster.from_dict(arr[i])
			m.heal_full()
			arr[i] = m.to_dict()


func _row(prefix: String, i: int, d: Dictionary) -> Dictionary:
	var m := Monster.from_dict(d)
	var mark := "▶ " if _picked == "%s:%d" % [prefix, i] else ""
	return {"id": "%s:%d" % [prefix, i], "key": mark + m.display_name(),
		"value": func() -> String: return UnitCard.age_text(m.level), "fixed": true}


func _fill() -> void:
	_title.text = tr("RANCH_PICK_SWAP") if _picked != "" else tr("RANCH_TITLE")
	var items := [{"id": "_hp", "key": "RANCH_PARTY", "enabled": false}]
	var party: Array = SaveGame.data.get("party", [])
	for i in party.size():
		items.append(_row("p", i, party[i]))
	items.append({"id": "_hr", "key": "RANCH_STORED", "enabled": false})
	var ranch: Array = SaveGame.data.get("ranch", [])
	for i in ranch.size():
		items.append(_row("r", i, ranch[i]))
	if ranch.is_empty():
		items.append({"id": "_none", "key": "RANCH_EMPTY", "enabled": false})
	items.append({"id": "_back", "key": "SET_BACK"})
	_menu.set_items(items, _menu.index)


func _on_activated(id: String) -> void:
	if id == "_back":
		close()
		return
	var party: Array = SaveGame.data.get("party", [])
	var ranch: Array = SaveGame.data.get("ranch", [])
	if not SaveGame.data.has("ranch"):
		SaveGame.data["ranch"] = ranch
	var side := id.substr(0, 1)
	var idx := int(id.substr(2))
	if _picked == "":
		if side == "p" and party.size() > 1:
			_picked = id
		elif side == "r" and party.size() < int(Data.battle_rules().get("party_size", 4)):
			party.append(ranch[idx])
			ranch.remove_at(idx)
		elif side == "r":
			_picked = id
		else:
			Audio.sfx("bump")
	elif _picked == id:
		# escolher de novo: guardar no Rancho (se for da equipe)
		if side == "p" and party.size() > 1:
			ranch.append(party[idx])
			party.remove_at(idx)
		_picked = ""
	else:
		var a_side := _picked.substr(0, 1)
		var a_idx := int(_picked.substr(2))
		if a_side != side:
			var pi := a_idx if a_side == "p" else idx
			var ri := idx if a_side == "p" else a_idx
			var tmp = party[pi]
			party[pi] = ranch[ri]
			ranch[ri] = tmp
		_picked = ""
	SaveGame.data["party"] = party
	SaveGame.data["ranch"] = ranch
	_fill()
