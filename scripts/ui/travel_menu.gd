class_name TravelMenu
extends Overlay
## Pausa → Viajar: lista as cidades já visitadas. A cidade atual aparece apagada.

var _menu: MenuList


func _init() -> void:
	super._init()
	ad_banner = true
	pauses_game = true


func _ready() -> void:
	dim_background(0.35)
	var panel := centered_panel(220)
	var box := VBoxContainer.new()
	panel.add_child(box)
	var title := UiTheme.label(tr("TRAVEL_TITLE"), UiTheme.TEXT_ACCENT)
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	box.add_child(title)
	var here := Travel.city_of_map(Game.world.map_id if Game.world else "")
	var items := []
	for cid in Travel.destinations():
		var it := {"id": cid, "key": Travel.name_key(cid)}
		if cid == here:
			it["enabled"] = false
			it["suffix"] = tr("TRAVEL_HERE")
		items.append(it)
	if items.is_empty():
		var none := UiTheme.label(tr("TRAVEL_NONE"))
		none.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
		none.custom_minimum_size.x = 200
		box.add_child(none)
	items.append({"id": "_back", "key": "SET_BACK"})
	_menu = MenuList.new()
	_menu.overlay = self
	_menu.max_visible = 8
	box.add_child(_menu)
	_menu.set_items(items)
	_menu.activated.connect(_on_activated)
	_menu.cancelled.connect(close)


func _on_activated(id: String) -> void:
	if id == "_back":
		close()
		return
	Game.close_all_overlays()
	Game.travel_to(id)
