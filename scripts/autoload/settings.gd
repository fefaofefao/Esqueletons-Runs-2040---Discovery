extends Node
## Configurações do jogador, salvas em user://settings.json.
## O idioma vazio significa "seguir o aparelho" (fallback: inglês).

signal changed(key: String)

const PATH := "user://settings.json"
const LANGUAGES: Array[String] = ["pt_BR", "en", "es"]
const TEXT_SPEEDS: Array[String] = ["slow", "normal", "fast"]
## Caracteres por segundo em 1x (o 2x dobra porque o diálogo usa o delta escalado).
const TEXT_CPS := {"slow": 24.0, "normal": 45.0, "fast": 110.0}

const DEFAULTS := {
	"language": "",
	"music_volume": 0.8,
	"sfx_volume": 0.9,
	"text_speed": "normal",
	"fast_forward": false,
	"vibration": true,
	"touch_controls": "auto",
}

var values: Dictionary = DEFAULTS.duplicate(true)
## Caminho do arquivo (os testes usam outro).
var path := PATH


func _ready() -> void:
	load_settings()
	apply_all()


func load_settings() -> void:
	values = DEFAULTS.duplicate(true)
	if not FileAccess.file_exists(path):
		return
	var parsed = JSON.parse_string(FileAccess.get_file_as_string(path))
	if parsed is Dictionary:
		for k in DEFAULTS.keys():
			if parsed.has(k) and typeof(parsed[k]) == typeof(DEFAULTS[k]):
				values[k] = parsed[k]


func save_settings() -> void:
	var f := FileAccess.open(path, FileAccess.WRITE)
	if f:
		f.store_string(JSON.stringify(values, "\t"))


func get_value(key: String) -> Variant:
	return values.get(key, DEFAULTS.get(key))


func set_value(key: String, value: Variant) -> void:
	if values.get(key) == value:
		return
	values[key] = value
	save_settings()
	apply(key)
	changed.emit(key)


func device_language() -> String:
	match OS.get_locale_language():
		"pt":
			return "pt_BR"
		"es":
			return "es"
		"en":
			return "en"
	return "en"


func current_language() -> String:
	var lang: String = values.get("language", "")
	return lang if lang in LANGUAGES else device_language()


func cycle_language(direction: int) -> void:
	var idx := LANGUAGES.find(current_language())
	idx = wrapi(idx + direction, 0, LANGUAGES.size())
	set_value("language", LANGUAGES[idx])


func text_cps() -> float:
	return TEXT_CPS.get(values.get("text_speed", "normal"), 45.0)


func apply_all() -> void:
	for k in DEFAULTS.keys():
		apply(k)


func apply(key: String) -> void:
	match key:
		"language":
			TranslationServer.set_locale(current_language())
		"music_volume":
			_set_bus_volume("Music", values.music_volume)
		"sfx_volume":
			_set_bus_volume("SFX", values.sfx_volume)


func _set_bus_volume(bus: String, linear: float) -> void:
	var idx := AudioServer.get_bus_index(bus)
	if idx < 0:
		return
	AudioServer.set_bus_mute(idx, linear <= 0.001)
	AudioServer.set_bus_volume_db(idx, linear_to_db(maxf(linear, 0.001)))
