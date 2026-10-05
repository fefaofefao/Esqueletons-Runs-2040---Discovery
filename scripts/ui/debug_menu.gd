class_name DebugMenu
extends Overlay
## Menu de debug (só em build de debug; 3 toques no logo ou F1/Select).
## Itens das fases 2 e 3 aparecem desativados até existirem.

var _menu: MenuList
var _title: Label
var _submenu := ""


func _init() -> void:
	super._init()
	pauses_game = true


func _ready() -> void:
	dim_background(0.55)
	var panel := centered_panel(UiTheme.MENU_LABEL_WIDTH + UiTheme.MENU_VALUE_WIDTH + 24)
	var box := VBoxContainer.new()
	panel.add_child(box)
	_title = UiTheme.label("", UiTheme.TEXT_ACCENT)
	box.add_child(_title)
	_menu = MenuList.new()
	_menu.overlay = self
	_menu.label_width = UiTheme.MENU_LABEL_WIDTH
	_menu.max_visible = 9
	box.add_child(_menu)
	_menu.activated.connect(_on_activated)
	_menu.value_step.connect(_on_value_step)
	_menu.cancelled.connect(_on_cancel)
	_show_main()


func _show_main() -> void:
	_submenu = ""
	_title.text = tr("DBG_TITLE")
	var phase2 := tr("DBG_PHASE").format({"n": 2})
	var phase3 := tr("DBG_PHASE").format({"n": 3})
	_menu.set_items([
		{"id": "teleport", "key": "DBG_TELEPORT", "enabled": Game.world != null},
		{"id": "speed10", "key": "DBG_SPEED10", "value": func() -> String: return _onoff(Speed.debug_multiplier > 1.0)},
		{"id": "radii", "key": "DBG_RADII", "value": func() -> String: return _onoff(DebugDraw.show_radii)},
		{"id": "encounters", "key": "DBG_ENCOUNTERS", "value": func() -> String: return _onoff(DebugDraw.show_encounters)},
		{"id": "touch", "key": "DBG_TOUCH", "value": func() -> String: return tr("VAL_" + str(Settings.get_value("touch_controls")).to_upper())},
		{"id": "times", "key": "DBG_TIMES"},
		{"id": "level", "key": "DBG_SET_LEVEL", "enabled": false, "suffix": phase2},
		{"id": "add", "key": "DBG_ADD_SKELETON", "enabled": false, "suffix": phase3},
		{"id": "golden", "key": "DBG_FORCE_GOLDEN", "enabled": false, "suffix": phase3},
		{"id": "growth", "key": "DBG_FORCE_GROWTH", "enabled": false, "suffix": phase3},
		{"id": "win", "key": "DBG_WIN_BATTLE", "enabled": false, "suffix": phase2},
		{"id": "save", "key": "DBG_SAVE_NOW", "enabled": Game.world != null},
		{"id": "wipe", "key": "DBG_DELETE_SAVE"},
		{"id": "close", "key": "DBG_CLOSE"},
	])


func _show_teleport() -> void:
	_submenu = "teleport"
	_title.text = tr("DBG_TELEPORT")
	var items := []
	var regions := Data.regions()
	for rid in regions.keys():
		for m in regions[rid].get("maps", []):
			var map_id := str(m)
			if Data.has_map(map_id):
				var key := str(Data.map(map_id).get("name_key", map_id))
				items.append({"id": map_id, "key": key})
	items.append({"id": "_back", "key": "SET_BACK"})
	_menu.set_items(items)


func _onoff(v: bool) -> String:
	return tr("VAL_ON") if v else tr("VAL_OFF")


func _on_value_step(id: String, _dir: int) -> void:
	match id:
		"speed10":
			Speed.set_debug_multiplier(1.0 if Speed.debug_multiplier > 1.0 else 10.0)
		"radii":
			DebugDraw.show_radii = not DebugDraw.show_radii
		"encounters":
			DebugDraw.show_encounters = not DebugDraw.show_encounters
		"touch":
			var opts := ["auto", "on", "off"]
			var i := opts.find(str(Settings.get_value("touch_controls")))
			Settings.set_value("touch_controls", opts[wrapi(i + 1, 0, opts.size())])


func _on_activated(id: String) -> void:
	if _submenu == "teleport":
		if id == "_back":
			_show_main()
			return
		close()
		var m := Data.map(id)
		var sp: Dictionary = m.get("spawn", {})
		Game.warp(id, Vector2i(int(sp.get("x", -1)), int(sp.get("y", -1))), str(sp.get("facing", "down")))
		return
	match id:
		"teleport":
			_show_teleport()
		"times":
			await Game.show_message("DBG_TIMES_BODY", {"lines": _times_text()})
		"save":
			Game.autosave()
			await Game.show_message("MSG_SAVED")
		"wipe":
			SaveGame.delete_save()
			await Game.show_message("DBG_SAVE_DELETED")
		"close":
			close()


func _on_cancel() -> void:
	if _submenu != "":
		_show_main()
	else:
		close()


static func _fmt_time(seconds: float) -> String:
	var s := int(seconds)
	return "%d:%02d" % [s / 60, s % 60]


func _times_text() -> String:
	var lines := PackedStringArray()
	var times := SaveGame.region_times()
	if times.is_empty():
		return tr("DBG_TIMES_EMPTY")
	for rid in times.keys():
		var r := Data.region(str(rid))
		var label := tr(str(r.get("name_key", rid)))
		lines.append("%s: %s (1x: %s)" % [label, _fmt_time(float(times[rid].get("real", 0.0))), _fmt_time(float(times[rid].get("game", 0.0)))])
	return "\n".join(lines)
