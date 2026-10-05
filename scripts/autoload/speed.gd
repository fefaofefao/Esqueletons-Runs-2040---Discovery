extends Node
## Fast forward (1x/2x) via Engine.time_scale. O estado fica salvo nas
## configurações ("fast_forward"), que é também a opção "2x padrão".
## Menus e cronômetros de anúncio usam tempo real (Time.get_ticks_msec) e não são afetados.

signal changed(multiplier: float)

var fast := false
## Velocidade forçada pelo menu de debug (10x); substitui o 1x/2x. Não é salva.
var debug_multiplier := 1.0


func _ready() -> void:
	fast = bool(Settings.get_value("fast_forward"))
	Settings.changed.connect(_on_settings_changed)
	_apply()


func toggle() -> void:
	set_fast(not fast)


func set_fast(value: bool) -> void:
	fast = value
	Settings.set_value("fast_forward", value)
	_apply()


func set_debug_multiplier(value: float) -> void:
	debug_multiplier = value
	_apply()


func multiplier() -> float:
	if debug_multiplier > 1.0:
		return debug_multiplier
	return 2.0 if fast else 1.0


func _apply() -> void:
	Engine.time_scale = multiplier()
	changed.emit(multiplier())


func _on_settings_changed(key: String) -> void:
	if key == "fast_forward" and bool(Settings.get_value("fast_forward")) != fast:
		fast = bool(Settings.get_value("fast_forward"))
		_apply()
