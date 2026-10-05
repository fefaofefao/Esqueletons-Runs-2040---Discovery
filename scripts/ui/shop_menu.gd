class_name ShopMenu
extends Overlay
## Loja da cidade (data/shops.json): A compra 1 unidade; mostra moedas e quantos tem.

var shop_id := ""
var _menu: MenuList
var _money: Label
var _desc: Label


func setup(id: String) -> ShopMenu:
	shop_id = id
	return self


func _init() -> void:
	super._init()
	pauses_game = true


func _ready() -> void:
	dim_background(0.45)
	var panel := centered_panel(230)
	var box := VBoxContainer.new()
	panel.add_child(box)
	_money = UiTheme.label("", UiTheme.TEXT_ACCENT)
	box.add_child(_money)
	_menu = MenuList.new()
	_menu.overlay = self
	_menu.label_width = 120
	box.add_child(_menu)
	_desc = UiTheme.label("", UiTheme.TEXT_VALUE)
	box.add_child(_desc)
	_menu.activated.connect(_buy)
	_menu.cancelled.connect(close)
	_menu.selection_changed.connect(func(_i: int) -> void: _update_desc())
	_fill()


func _stock() -> Array:
	var d = Data.load_json("res://data/shops.json")
	return d.get("shops", {}).get(shop_id, []) if d is Dictionary else []


func _fill() -> void:
	_money.text = tr("SHOP_MONEY").format({"n": int(SaveGame.data.get("money", 0))})
	var items := []
	for id in _stock():
		var it := Data.item(id)
		var owned := int(SaveGame.data.get("bag", {}).get(id, 0))
		items.append({"id": id, "key": str(it.get("name_key", "")), "suffix": "×%d" % owned,
			"value": func() -> String: return "$%d" % int(it.get("price", 0)), "fixed": true})
	items.append({"id": "_back", "key": "SET_BACK"})
	_menu.set_items(items, _menu.index)
	_update_desc()


func _update_desc() -> void:
	var id := str(_menu.items[_menu.index].get("id", "")) if not _menu.items.is_empty() else ""
	_desc.text = tr(str(Data.item(id).get("desc_key", ""))) if id != "_back" and id != "" else ""


func _buy(id: String) -> void:
	if id == "_back":
		close()
		return
	var price := int(Data.item(id).get("price", 0))
	var money := int(SaveGame.data.get("money", 0))
	if money < price:
		Audio.sfx("bump")
		_desc.text = tr("SHOP_NO_MONEY")
		return
	SaveGame.data["money"] = money - price
	ScriptActions._add_item(id, 1)
	Audio.sfx("buy")
	_fill()
