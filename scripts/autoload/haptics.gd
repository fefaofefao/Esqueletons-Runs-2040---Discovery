extends Node
## Vibração leve sem a permissão VIBRATE: usa View.performHapticFeedback do
## Android (via singleton AndroidRuntime do Godot 4.4+). Em outras plataformas
## não faz nada. Respeita a opção "Vibração" das configurações.

const KEYBOARD_TAP := 3
const LONG_PRESS := 0

var _runtime: Object = null


func _ready() -> void:
	if OS.get_name() == "Android" and Engine.has_singleton("AndroidRuntime"):
		_runtime = Engine.get_singleton("AndroidRuntime")


func tap() -> void:
	_feedback(KEYBOARD_TAP)


func strong() -> void:
	_feedback(LONG_PRESS)


func _feedback(kind: int) -> void:
	if _runtime == null or not bool(Settings.get_value("vibration")):
		return
	var activity = _runtime.getActivity()
	if activity == null:
		return
	var callback := func() -> void:
		var view = activity.getWindow().getDecorView()
		if view:
			view.performHapticFeedback(kind)
	activity.runOnUiThread(_runtime.createRunnableFromGodotCallable(callback))
