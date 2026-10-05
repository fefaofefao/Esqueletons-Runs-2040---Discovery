class_name OssuaryEntry
extends Overlay
## Ficha do Ossário: sprite, número, nome, tipo, estágio, marcador e a entrada
## (até 3 linhas). Golden recrutado mostra o sprite dourado.

var species_id := ""
var number := 0


func setup(id: String, n: int) -> OssuaryEntry:
	species_id = id
	number = n
	return self


func _init() -> void:
	super._init()
	pauses_game = true
	mouse_filter = Control.MOUSE_FILTER_STOP


func _ready() -> void:
	dim_background(0.6)
	var info := Data.species(species_id)
	var e: Dictionary = SaveGame.data.get("ossuary", {}).get(species_id, {})
	var panel := centered_panel(300)
	var col := VBoxContainer.new()
	panel.add_child(col)
	var top := HBoxContainer.new()
	top.add_theme_constant_override("separation", 8)
	col.add_child(top)
	# sprite 32×32 em 2x
	var frame := Control.new()
	frame.custom_minimum_size = Vector2(64, 64)
	top.add_child(frame)
	var spr := Sprite2D.new()
	spr.texture = load(str(info.get("sprite", "")))
	spr.region_enabled = true
	spr.region_rect = Rect2(0, 0, 32, 32)
	spr.centered = false
	spr.scale = Vector2(2, 2)
	frame.add_child(spr)
	if e.get("golden_recruited", false):
		GoldenFX.apply(spr, Vector2(16, 16), Vector2(10, 12))
	var right := VBoxContainer.new()
	top.add_child(right)
	var name_text := "%03d  %s" % [number, tr(str(info.get("name_key", "")))]
	if e.get("golden_recruited", false):
		name_text += " ★"
	right.add_child(UiTheme.label(name_text, UiTheme.TEXT_ACCENT))
	var stage := int(info.get("stage", 0))
	var kind := tr("OSS_STAGE_%d" % stage) if stage > 0 else tr("OSS_UNIQUE")
	right.add_child(UiTheme.label("%s · %s" % [tr("TYPE_" + str(info.get("type", "fisico")).to_upper()), kind]))
	var status := "OSS_RECRUITED" if e.get("recruited", false) else ("OSS_DEFEATED" if e.get("defeated", false) else "OSS_SEEN")
	right.add_child(UiTheme.label(tr(status), UiTheme.TEXT_VALUE))
	right.add_child(UiTheme.label(tr("OSS_MARKER").format({"p": int(e.get("marker", 0))}), UiTheme.TEXT_VALUE))
	var text := UiTheme.label("\n".join(TextFit.wrap_lines(tr(str(info.get("entry_key", ""))), UiTheme.DIALOG_TEXT_WIDTH)))
	col.add_child(text)


func _unhandled_input(event: InputEvent) -> void:
	if not accepts_input():
		return
	if event.is_action_pressed("btn_a", false) or event.is_action_pressed("btn_b", false):
		get_viewport().set_input_as_handled()
		Audio.sfx("cancel")
		close()


func _gui_input(event: InputEvent) -> void:
	if accepts_input() and event is InputEventMouseButton and event.pressed:
		close()
