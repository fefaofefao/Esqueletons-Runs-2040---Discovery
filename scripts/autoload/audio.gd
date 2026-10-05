extends Node
## Efeitos sonoros (barramento SFX) e música (barramento Music).
## Música: a do mapa toca em laço; a batalha empilha o tema dela e, no fim,
## a do mapa volta de onde parou. Vinhetas (aniversário, Golden) pausam a música.

const SFX_DIR := "res://assets/sfx/%s.wav"
const POOL := 6

var _streams: Dictionary = {}
var _players: Array[AudioStreamPlayer] = []
var _next := 0
var _music: AudioStreamPlayer
var _jingle: AudioStreamPlayer
var _music_path := ""
var _stack: Array = []
var _cfg: Dictionary = {}
var _last_play: Dictionary = {}


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	for i in POOL:
		var p := AudioStreamPlayer.new()
		p.bus = &"SFX"
		add_child(p)
		_players.append(p)
	_music = AudioStreamPlayer.new()
	_music.bus = &"Music"
	add_child(_music)
	_jingle = AudioStreamPlayer.new()
	_jingle.bus = &"Music"
	add_child(_jingle)


## Caminho de um tema de data/audio.json (title, battle, boss, king, birthday...).
func theme(key: String) -> String:
	if _cfg.is_empty():
		_cfg = Data.load_json("res://data/audio.json")
	return str(_cfg.get(key, ""))


## Tema da batalha: o Rei tem o dele; Guardiões e chefes, o de chefe.
func battle_theme(info: Dictionary) -> String:
	for e in info.get("enemies", []):
		if str(e[0]) == theme("king_species"):
			return theme("king")
	return theme("boss") if str(info.get("kind", "")) == "boss" else theme("battle")


func sfx(sfx_name: String, min_interval_ms: int = 0) -> void:
	var now := Time.get_ticks_msec()
	if min_interval_ms > 0 and now - int(_last_play.get(sfx_name, -100000)) < min_interval_ms:
		return
	_last_play[sfx_name] = now
	var stream: AudioStream = _streams.get(sfx_name)
	if stream == null:
		var path := SFX_DIR % sfx_name
		if not ResourceLoader.exists(path):
			return
		stream = load(path)
		_streams[sfx_name] = stream
	var p := _players[_next]
	_next = (_next + 1) % POOL
	p.stream = stream
	p.play()


func play_music(path: String) -> void:
	if path == "" or not ResourceLoader.exists(path):
		_music.stop()
		_music_path = ""
		return
	if path == _music_path and _music.playing:
		return
	var stream: AudioStream = load(path)
	if stream is AudioStreamOggVorbis:
		stream.loop = true
	_music_path = path
	_music.stream = stream
	_music.stream_paused = false
	_music.play()


func current_music() -> String:
	return _music_path


## Troca para um tema temporário (batalha) guardando o atual e a posição.
func push_music(path: String) -> void:
	_stack.append({"path": _music_path, "pos": _music.get_playback_position() if _music.playing else 0.0})
	play_music(path)


## Volta ao tema guardado por push_music, do ponto em que parou.
func pop_music() -> void:
	if _stack.is_empty():
		return
	var prev: Dictionary = _stack.pop_back()
	play_music(str(prev.path))
	if _music.playing and float(prev.pos) > 0.0:
		_music.seek(float(prev.pos))


## Vinheta curta: pausa a música, toca e retoma.
func play_jingle(path: String) -> void:
	if path == "" or not ResourceLoader.exists(path):
		return
	var stream: AudioStream = load(path)
	if stream is AudioStreamOggVorbis:
		stream.loop = false
	_music.stream_paused = true
	_jingle.stream = stream
	_jingle.play()
	await _jingle.finished
	if not _jingle.playing:
		_music.stream_paused = false


func stop_music() -> void:
	_music.stop()
	_music_path = ""
