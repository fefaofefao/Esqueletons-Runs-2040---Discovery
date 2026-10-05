class_name OssuaryScreen
extends Overlay
## Ossário: cada espécie como vista, derrotada, recrutada ou Golden, com o
## marcador de recrutamento e o % de conclusão. Golden visto e recrutado contam
## separado. Selecionar uma espécie vista mostra a entrada do Ossário.

var _menu: MenuList
var _header: Label
var _ids: Array = []


func _init() -> void:
	super._init()
	pauses_game = true


func _ready() -> void:
	dim_background(0.55)
	var panel := centered_panel(280)
	var box := VBoxContainer.new()
	panel.add_child(box)
	_header = UiTheme.label("", UiTheme.TEXT_ACCENT)
	box.add_child(_header)
	_menu = MenuList.new()
	_menu.overlay = self
	_menu.label_width = 150
	_menu.max_visible = 8
	box.add_child(_menu)
	_menu.activated.connect(_on_activated)
	_menu.cancelled.connect(close)
	_fill()


func _fill() -> void:
	var c := Ossuary.completion()
	_header.text = tr("OSS_HEADER").format({"p": c.percent, "r": c.recruited, "t": c.total, "g": c.golden})
	_ids = Data.all_species_ids(false)
	if _ids.is_empty() and OS.is_debug_build():
		_ids = Data.all_species_ids(true)
	_ids.sort_custom(func(a: String, b: String) -> bool: return _order(a) < _order(b))
	var items := []
	for i in _ids.size():
		var id: String = _ids[i]
		var e: Dictionary = SaveGame.data.get("ossuary", {}).get(id, {})
		var seen: bool = e.get("seen", false)
		var name := tr(str(Data.species(id).get("name_key", ""))) if seen else "???"
		var marks := ""
		if e.get("recruited", false):
			marks += "●"
		elif e.get("defeated", false):
			marks += "○"
		if e.get("golden_recruited", false):
			marks += "★"
		elif e.get("golden_seen", false):
			marks += "☆"
		items.append({"id": id, "key": "%03d" % (i + 1), "suffix": "%s %s" % [name, marks],
			"value": func() -> String: return "%d%%" % int(e.get("marker", 0)) if seen else "", "fixed": true})
	items.append({"id": "_back", "key": "SET_BACK"})
	_menu.set_items(items)


## Ordem do Ossário: número da linha, depois estágio.
static func _order(id: String) -> String:
	var info := Data.species(id)
	return "%04d-%d-%s" % [int(info.get("number", 999)), int(info.get("stage", 1)), id]


func _on_activated(id: String) -> void:
	if id == "_back":
		close()
		return
	var e: Dictionary = SaveGame.data.get("ossuary", {}).get(id, {})
	if not e.get("seen", false):
		Audio.sfx("bump")
		return
	var entry_key := str(Data.species(id).get("entry_key", ""))
	if entry_key != "":
		await Game.show_message(entry_key)
