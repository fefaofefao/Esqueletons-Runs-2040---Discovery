class_name BagMenu
extends Overlay
## Mochila (menu de pausa): itens com quantidade. Poções, antídoto e reviver
## são usados na equipe; itens-chave mostram a descrição.

var _menu: MenuList
var _title: Label
var _desc: Label
var _item := ""  # item escolhido aguardando o alvo


func _init() -> void:
	super._init()
	pauses_game = true


func _ready() -> void:
	dim_background(0.45)
	var panel := centered_panel(240)
	var box := VBoxContainer.new()
	panel.add_child(box)
	_title = UiTheme.label("", UiTheme.TEXT_ACCENT)
	box.add_child(_title)
	_menu = MenuList.new()
	_menu.overlay = self
	_menu.label_width = 150
	_menu.max_visible = 7
	box.add_child(_menu)
	_desc = UiTheme.label("", UiTheme.TEXT_VALUE)
	box.add_child(_desc)
	_menu.activated.connect(_on_activated)
	_menu.cancelled.connect(func() -> void:
		if _item != "":
			_item = ""
			_show_items()
		else:
			close())
	_menu.selection_changed.connect(func(_i: int) -> void: _update_desc())
	_show_items()


func _show_items() -> void:
	_title.text = tr("BAG_TITLE")
	var items := []
	var bag: Dictionary = SaveGame.data.get("bag", {})
	var ids := bag.keys()
	ids.sort()
	for id in ids:
		if int(bag[id]) <= 0:
			continue
		items.append({"id": str(id), "key": str(Data.item(str(id)).get("name_key", id)),
			"value": func() -> String: return "×%d" % int(SaveGame.data.get("bag", {}).get(id, 0)), "fixed": true})
	if items.is_empty():
		items.append({"id": "_none", "key": "BAG_EMPTY", "enabled": false})
	items.append({"id": "_back", "key": "SET_BACK"})
	_menu.set_items(items)
	_update_desc()


func _update_desc() -> void:
	if _item != "" or _menu.items.is_empty():
		_desc.text = ""
		return
	var id := str(_menu.items[_menu.index].get("id", ""))
	if id.begins_with("_"):
		_desc.text = ""
	elif str(Data.item(id).get("kind", "")) == "key":
		_desc.text = tr("BAG_KEY_ITEM")
	else:
		_desc.text = tr(str(Data.item(id).get("desc_key", "")))


func _show_targets() -> void:
	_title.text = tr("BAG_USE_ON").format({"item": tr(str(Data.item(_item).get("name_key", "")))})
	var items := []
	var party: Array = SaveGame.data.get("party", [])
	for i in party.size():
		var m := Monster.from_dict(party[i])
		items.append({"id": str(i), "key": m.display_name(), "value": func() -> String: return "%d/%d" % [m.hp, m.max_hp()], "fixed": true})
	items.append({"id": "_back", "key": "SET_BACK"})
	_menu.set_items(items)
	_desc.text = ""


func _on_activated(id: String) -> void:
	if id == "_back":
		if _item != "":
			_item = ""
			_show_items()
		else:
			close()
		return
	if _item == "":
		var it := Data.item(id)
		if str(it.get("kind", "")) in ["heal", "cure", "revive"]:
			_item = id
			_show_targets()
		else:
			await Game.show_message(str(it.get("desc_key", "")))
		return
	var party: Array = SaveGame.data.get("party", [])
	var m := Monster.from_dict(party[int(id)])
	if not BagMenu.apply_item(_item, m):
		Audio.sfx("bump")
		_desc.text = tr("BAG_NO_EFFECT")
		return
	party[int(id)] = m.to_dict()
	SaveGame.data["bag"][_item] = int(SaveGame.data["bag"][_item]) - 1
	Audio.sfx("heal")
	if int(SaveGame.data["bag"][_item]) <= 0:
		_item = ""
		_show_items()
	else:
		_show_targets()


## Usa o item fora da batalha. Devolve false se não teria efeito.
static func apply_item(item_id: String, m: Monster) -> bool:
	var it := Data.item(item_id)
	match str(it.get("kind", "")):
		"heal":
			if m.is_fainted() or m.hp >= m.max_hp():
				return false
			m.hp = mini(m.max_hp(), m.hp + int(it.get("amount", 30)))
			return true
		"cure":
			if not m.is_poisoned():
				return false
			m.poison_turns = 0
			return true
		"revive":
			if not m.is_fainted():
				return false
			m.hp = maxi(1, int(m.max_hp() * float(it.get("fraction", 0.5))))
			return true
	return false
