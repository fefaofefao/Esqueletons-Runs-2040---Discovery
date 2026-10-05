extends "res://tests/test_case.gd"
## Fase 5: regras de anúncios (seção 14) com um backend falso — o SDK de
## verdade só existe no Android.

var tree: SceneTree
var host: Node


func set_tree(t: SceneTree, h: Node) -> void:
	tree = t
	host = h


class FakeBackend extends Node:
	signal interstitial_closed
	signal rewarded_closed(granted: bool)
	signal privacy_closed
	var banner := false
	var shown_interstitials := 0
	var give_reward := true
	func ready_for_ads() -> bool: return true
	func set_banner_visible(v: bool) -> void: banner = v
	func interstitial_ready() -> bool: return true
	func show_interstitial() -> void:
		shown_interstitials += 1
		interstitial_closed.emit.call_deferred()
	func rewarded_ready() -> bool: return true
	func show_rewarded() -> void: rewarded_closed.emit.call_deferred(give_reward)
	func privacy_required() -> bool: return true
	func show_privacy() -> void: privacy_closed.emit.call_deferred()


func _reset() -> FakeBackend:
	SaveGame.start_new("Téo")
	var fb := FakeBackend.new()
	host.add_child(fb)
	Ads._battles_since = 0
	Ads._last_interstitial_ms = -10000000
	Ads._banner_owners.clear()
	Ads.set_backend(fb)
	return fb


func _done(fb: FakeBackend) -> void:
	Ads.backend = null
	fb.queue_free()


func test_no_backend_offline() -> void:
	Ads.backend = null
	check(not Ads.active(), "sem SDK (computador/testes): anúncios desligados")
	check_eq(Ads.banner_inset(), 0.0, "sem SDK, os menus não reservam espaço")
	check(not Ads.rewarded_available(), "sem SDK, nenhuma oferta de premiado")


func test_interstitial_rules() -> void:
	var fb := _reset()
	SaveGame.data["play_time"]["real"] = 300.0
	for i in 3:
		Ads.on_battle_finished()
	check(not Ads.interstitial_allowed(10_000_000), "nada nos primeiros 10 minutos")
	SaveGame.data["play_time"]["real"] = 700.0
	Ads._battles_since = 2
	check(not Ads.interstitial_allowed(10_000_000), "no máximo 1 a cada 3 batalhas")
	Ads.on_battle_finished()
	check(Ads.interstitial_allowed(10_000_000), "3 batalhas e 10 min: pode")
	await Ads.maybe_interstitial()
	check_eq(fb.shown_interstitials, 1, "mostrou um intersticial no mapa")
	for i in 3:
		Ads.on_battle_finished()
	check(not Ads.interstitial_allowed(Ads._last_interstitial_ms + 60_000), "pelo menos 3 minutos entre intersticiais")
	check(Ads.interstitial_allowed(Ads._last_interstitial_ms + 181_000), "depois de 3 minutos, pode de novo")
	var box := DialogBox.new()
	box.setup([{"say": "MSG_GOT_ITEM"}])
	Game.open_overlay(box)
	await Ads.maybe_interstitial()
	check_eq(fb.shown_interstitials, 1, "nunca durante diálogo")
	Game.close_all_overlays()
	_done(fb)


func test_banner_only_in_menus() -> void:
	var fb := _reset()
	check(not fb.banner, "sem menu, sem banner")
	var pm := PauseMenu.new()
	Game.open_overlay(pm)
	check(fb.banner, "menu de pausa mostra banner")
	check(Ads.banner_inset() > 0.0, "o painel do menu desce para não ficar sob o banner")
	Game.close_overlay(pm)
	check(not fb.banner, "fechou o menu, sumiu o banner")
	var box := DialogBox.new()
	box.setup([{"say": "MSG_GOT_ITEM"}])
	Game.open_overlay(box)
	check(not fb.banner, "diálogo nunca tem banner")
	Game.close_all_overlays()
	_done(fb)


func test_rewarded_only_on_completion() -> void:
	var fb := _reset()
	check(not Ads.rewarded_available(), "premiado só depois do tutorial do marcador")
	SaveGame.set_flag("tut_marker")
	check(Ads.rewarded_available(), "premiado disponível")
	fb.give_reward = false
	check(not await Ads.show_rewarded(), "fechou antes do fim: sem recompensa")
	fb.give_reward = true
	check(await Ads.show_rewarded(), "assistiu até o fim: recompensa")
	_done(fb)
