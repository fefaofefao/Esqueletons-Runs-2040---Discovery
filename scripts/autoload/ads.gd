extends Node
## Anúncios (seção 14). Aqui ficam as REGRAS de posicionamento; o SDK (plugin
## AdMob da Poing Studios, em addons/admob) só é tocado pelo AdMobBackend, que
## só é carregado num Android de verdade. No computador e nos testes não há
## backend: nada é exibido e o jogo funciona 100% offline.
##
## Regras:
##   - consentimento (UMP) antes de inicializar o SDK;
##   - banner só em menus (pausa, Ossário, Rancho, loja), no topo, com o painel
##     do menu deslocado para baixo (nunca em cima de botões);
##   - intersticial só depois de vencer uma batalha SELVAGEM, já de volta ao mapa
##     (fora de diálogos, cenas e crescimento), no máximo 1 a cada 3 batalhas,
##     com 3 min de intervalo e nada nos primeiros 10 min de jogo; sempre
##     pré-carregado;
##   - premiado sempre opcional; a recompensa só sai no callback de conclusão e
##     nunca mexe na chance de Golden.

signal interstitial_closed
signal rewarded_closed(granted: bool)
signal privacy_closed

var rules: Dictionary = {}
var backend: Object = null          # AdMobBackend (Android) ou um falso nos testes
var _battles_since := 0
var _last_interstitial_ms := -10000000
var _banner_owners: Array = []


func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	rules = Data.load_json("res://data/ads.json")
	if OS.get_name() == "Android" and Engine.has_singleton("PoingGodotAdMob"):
		var ids := _ad_ids()
		if not ids.is_empty():
			var b = load("res://scripts/ads/admob_backend.gd").new()
			add_child(b)
			set_backend(b)
			b.start(ids, rules.get("audience", {}))


## IDs de teste no debug; no release, os reais de config/admob.json (gerado
## pelo CI a partir dos Secrets). Sem o arquivo no release: sem anúncios.
func _ad_ids() -> Dictionary:
	if OS.is_debug_build():
		return rules.get("test_ids", {})
	var real = Data.load_json("res://config/admob.json")
	return real if real is Dictionary and not real.is_empty() else {}


func set_backend(b: Object) -> void:
	backend = b
	if b:
		b.connect("interstitial_closed", func() -> void: interstitial_closed.emit())
		b.connect("rewarded_closed", func(g: bool) -> void: rewarded_closed.emit(g))
		b.connect("privacy_closed", func() -> void: privacy_closed.emit())


func active() -> bool:
	return backend != null and backend.call("ready_for_ads")


# ------------------------------------------------------------------ banner (menus)
## Espaço (em pixels da resolução base) que os menus deixam livre no topo.
func banner_inset() -> float:
	return float(rules.get("banner", {}).get("reserve_px", 28)) if active() else 0.0


func banner_push(owner: Object) -> void:
	if owner not in _banner_owners:
		_banner_owners.append(owner)
	_update_banner()


func banner_pop(owner: Object) -> void:
	_banner_owners.erase(owner)
	_update_banner()


func _update_banner() -> void:
	_banner_owners = _banner_owners.filter(func(o: Object) -> bool: return is_instance_valid(o))
	if active():
		backend.call("set_banner_visible", not _banner_owners.is_empty())


# ------------------------------------------------------------------ intersticial
func on_battle_finished() -> void:
	_battles_since += 1


func play_seconds() -> float:
	return float(SaveGame.data.get("play_time", {}).get("real", 0.0))


## Pode mostrar agora? (as regras de frequência valem mesmo sem SDK, para teste)
func interstitial_allowed(now_ms: int = -1) -> bool:
	var r: Dictionary = rules.get("interstitial", {})
	if now_ms < 0:
		now_ms = Time.get_ticks_msec()
	if play_seconds() < float(r.get("grace_seconds", 600)):
		return false
	if _battles_since < int(r.get("min_battles", 3)):
		return false
	if now_ms - _last_interstitial_ms < int(r.get("min_seconds", 180)) * 1000:
		return false
	return true


## Chamado pelo mapa depois de uma vitória selvagem, já fora da batalha e de
## qualquer crescimento. Não mostra se houver diálogo/menu aberto.
func maybe_interstitial() -> void:
	if not active() or not interstitial_allowed() or not backend.call("interstitial_ready"):
		return
	if Game.top_overlay() != null or Game.battle != null or Game.transitioning:
		return
	_battles_since = 0
	_last_interstitial_ms = Time.get_ticks_msec()
	backend.call("show_interstitial")
	await interstitial_closed


# ------------------------------------------------------------------ premiado
func rewarded_available() -> bool:
	var flag := str(rules.get("rewarded", {}).get("after_flag", ""))
	if flag != "" and not SaveGame.get_flag(flag):
		return false
	return active() and backend.call("rewarded_ready")


## Mostra o premiado; true só se o jogador assistiu até o fim (callback do SDK).
func show_rewarded() -> bool:
	if not rewarded_available():
		return false
	backend.call("show_rewarded")
	return await rewarded_closed


# ------------------------------------------------------------------ privacidade (Configurações)
func privacy_options_required() -> bool:
	return active() and backend.call("privacy_required")


func show_privacy_options() -> void:
	if backend == null:
		return
	backend.call("show_privacy")
	await privacy_closed
