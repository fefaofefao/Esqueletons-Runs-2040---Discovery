extends Node
## Efeitos sonoros (barramento SFX) e música (barramento Music).

const SFX_DIR := "res://assets/sfx/%s.wav"
const POOL := 6

var _streams: Dictionary = {}
var _players: Array[AudioStreamPlayer] = []
var _next := 0
var _music: AudioStreamPlayer
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
		return
	var stream: AudioStream = load(path)
	if _music.stream == stream and _music.playing:
		return
	_music.stream = stream
	_music.play()


func stop_music() -> void:
	_music.stop()
