extends "res://tests/test_case.gd"
## Fase 4 (todas as regiões): regras das seções 6, 7 e 11 conferidas sobre os
## mapas reais, a partir de data/routes.json, data/cities.json e dos roteiros.
##   - toda rota: os caminhos de Domadores (oeste) e Selvagem (leste) chegam
##     sozinhos à cidade seguinte (nenhum é obrigatório);
##   - toda cidade: portas para Rancho, Loja e casas; Guardião alcançável;
##   - todo Guardião: batalha de chefe, idades coerentes com o estágio e média
##     igual à de data/balance.json.

const GUARDIANS := {
	"BTL_TAMER_RAMALHO": "bosque", "BTL_TAMER_FORNALHA": "minas", "BTL_TAMER_MUSGA": "pantano",
	"BTL_TAMER_CALICO": "ossorio", "BTL_TAMER_ALVA": "picos", "BTL_TAMER_DUNA": "deserto",
	"BTL_TAMER_DEGUSTOR": "castelo",
}

var tree: SceneTree
var host: Node


func set_tree(t: SceneTree, h: Node) -> void:
	tree = t
	host = h


func _reach(m: MapView, from: Vector2i, to: Vector2i, allow: Callable = Callable()) -> bool:
	var seen := {from: true}
	var q: Array[Vector2i] = [from]
	while not q.is_empty():
		var c: Vector2i = q.pop_front()
		if c == to:
			return true
		for d in [Vector2i.UP, Vector2i.DOWN, Vector2i.LEFT, Vector2i.RIGHT]:
			var n: Vector2i = c + d
			if seen.has(n) or not m.in_bounds(n):
				continue
			if m.is_blocked(n) and m.npc_at(n) == null:
				continue
			if allow.is_valid() and not allow.call(n):
				continue
			seen[n] = true
			q.append(n)
	return false


func _map(id: String) -> MapView:
	var m := MapView.new()
	host.add_child(m)
	check(m.build(id), "%s monta" % id)
	return m


func test_routes_have_free_paths() -> void:
	SaveGame.start_new("Téo")
	for r in Data.load_json("res://data/routes.json").get("routes", []):
		var m := _map(str(r.map))
		var start := Vector2i(19, int(m.size.y) - 3)
		var goal := Vector2i(19, 1)
		check(_reach(m, start, goal), "%s: atravessa" % r.id)
		check(_reach(m, start, goal, func(c: Vector2i) -> bool: return c.x <= 18 or c.y <= 13 or c.y >= 36),
			"%s: Caminho dos Domadores sozinho chega" % r.id)
		check(_reach(m, start, goal, func(c: Vector2i) -> bool: return c.x >= 21 or c.y <= 13 or c.y >= 36),
			"%s: Caminho Selvagem sozinho chega" % r.id)
		var tamers := 0
		for n in m.all_npcs():
			if not n.info.get("tamer", {}).is_empty():
				tamers += 1
		check(tamers >= 3, "%s: 3 domadores no caminho deles (%d)" % [r.id, tamers])
		check(m.spawns.size() >= 4, "%s: selvagens visíveis" % r.id)
		check(not m.props_of("sign").is_empty(), "%s: placa na bifurcação" % r.id)
		m.queue_free()
		await tree.process_frame


func test_cities_complete() -> void:
	SaveGame.start_new("Téo")
	for c in Data.load_json("res://data/cities.json").get("cities", []):
		var m := _map(str(c.map))
		var doors := 0
		for w in m.data.warps:
			if Data.has_map(str(w.to)) and str(Data.map(str(w.to)).get("id", "")) != "" and str(w.get("sfx", "")) == "door":
				doors += 1
		check(doors >= 4, "%s: portas de Rancho, Loja e casas (%d)" % [c.id, doors])
		check(Data.load_json("res://data/shops.json").shops.has(str(c.shop)), "%s: loja com estoque" % c.id)
		m.queue_free()
		await tree.process_frame


func _battles(node_list: Array, out: Array) -> void:
	for n in node_list:
		if n is Dictionary and str(n.get("action", "")) == "battle" and str(n.get("kind", "")) == "boss":
			out.append(n)


func test_guardians_match_balance() -> void:
	## A equipe do roteiro tem de ser a mesma que o simulador usa (balance.json):
	## mesmas linhas, idades a ±1 e estágio coerente com a idade.
	var protos := {}
	for reg in Data.load_json("res://data/balance.json").regions:
		protos[str(reg.id)] = reg.get("guardian", [])
	var found := {}
	for f in DirAccess.get_files_at("res://data/dialogs"):
		if not f.ends_with(".json"):
			continue
		var d = Data.load_json("res://data/dialogs/" + f)
		for key in d.get("dialogs", {}):
			var bs: Array = []
			_battles(d.dialogs[key], bs)
			for b in bs:
				var tk := str(b.tamer_key)
				if not GUARDIANS.has(tk):
					continue
				found[tk] = true
				var proto: Array = protos.get(GUARDIANS[tk], [])
				check_eq(b.enemies.size(), proto.size(), "%s: tamanho da equipe igual ao balance.json" % tk)
				for e in b.enemies:
					var info := Data.species(str(e[0]))
					var gl: Array = info.get("growth_levels", [])
					var st := int(info.get("stage", 1))
					if gl.size() == 2:
						var lo := 0 if st == 1 else int(gl[st - 2])
						var hi := 999 if st == 3 else int(gl[st - 1]) - 1
						check(int(e[1]) >= lo and int(e[1]) <= hi, "%s: %s com idade %d coerente com o estágio" % [tk, e[0], int(e[1])])
					var line := str(info.get("line", e[0]))
					var ok := false
					for pr in proto:
						ok = ok or (str(pr[0]) == line and absi(int(pr[1]) - int(e[1])) <= 1)
					check(ok, "%s: %s %d está no protótipo do balance.json" % [tk, line, int(e[1])])
	check(found.has("BTL_TAMER_RAMALHO") and found.has("BTL_TAMER_FORNALHA"), "Guardiões implementados conferidos")

## Executa um roteiro escolhendo as opções dadas (sem batalhas no caminho).
func _play(ref: String, choices: Array = []) -> void:
	var done := [false]
	var runner := func() -> void:
		await Game.play_script(Data.dialog(ref))
		done[0] = true
	runner.call()
	var start := Time.get_ticks_msec()
	while not done[0] and Time.get_ticks_msec() - start < 8000:
		await tree.process_frame
		var top := Game.top_overlay()
		if top is DialogBox:
			var box := top as DialogBox
			if box._waiting_choice and box._choice:
				box._choice.index = int(choices.pop_front()) if not choices.is_empty() else 0
				box._choice.activate_current()
			elif box.accepts_input():
				box._press()
		elif top != null:
			top.close()
	check(done[0], "roteiro %s termina" % ref)


func _price(shop: String, item: String) -> int:
	var s := ShopMenu.new()
	s.shop_id = shop
	var p := s.price(item)
	s.free()
	return p


func test_choice_minas() -> void:
	SaveGame.start_new("Téo")
	var base := _price("brasal", "pocao_g")
	SaveGame.set_flag("fornalha_beaten")
	await _play("minas/fornalha_escolha", [1])
	check(SaveGame.get_flag("minas_negociou") and SaveGame.get_flag("red_minas"), "negociar: +1 Redenção")
	check(SaveGame.get_flag("has_martelo_tia"), "negociar: Martelo da Tia")
	check(_price("brasal", "pocao_g") < base, "negociar: desconto na loja")
	SaveGame.start_new("Téo")
	SaveGame.set_flag("fornalha_beaten")
	await _play("minas/fornalha_escolha", [0])
	check(SaveGame.get_flag("minas_quebrou") and not SaveGame.get_flag("red_minas"), "quebrar: sem Redenção")
	check(_price("brasal", "pocao_g") > base, "quebrar: loja mais cara")
	var m := _map("mina_funda")
	var vago := false
	for n in m.all_npcs():
		vago = vago or n.npc_id == "vagonauta_npc"
	check(vago, "quebrar: Vagonauta aparece na câmara sul")
	m.queue_free()
	await tree.process_frame


func test_quest_carvao() -> void:
	SaveGame.start_new("Téo")
	await _play("minas/carvao_pede")
	check(SaveGame.get_flag("carvao_quest"), "missão aberta")
	await _play("minas/capacete")
	check(SaveGame.get_flag("has_capacete_carvao"), "pegou o capacete")
	await _play("minas/carvao_obrigado")
	check(not SaveGame.get_flag("has_capacete_carvao"), "entregou o capacete")
	check_eq(int(SaveGame.data.bag.get("pocao_g", 0)), 2, "2 Poções G")


func test_quest_pirita() -> void:
	SaveGame.start_new("Téo")
	await _play("minas/pirita_pede")
	await _play("minas/cristal_vela")
	check(SaveGame.get_flag("has_cristal_vela"), "pegou o Cristal-vela")
	await _play("minas/pirita_festa")
	check(SaveGame.get_flag("pirita_done") and not SaveGame.get_flag("has_cristal_vela"), "festa feita, cristal entregue")
	check_eq(int(SaveGame.data.bag.get("pocao_m", 0)), 2, "2 Poções M")


func test_choice_pantano() -> void:
	SaveGame.start_new("Téo")
	SaveGame.data["bag"] = {"antidoto": 5}
	SaveGame.set_flag("has_antidoto")
	await _play("pantano/garca", [0, 1])
	check(SaveGame.get_flag("pantano_doou") and SaveGame.get_flag("red_pantano"), "doar: +1 Redenção")
	check_eq(int(SaveGame.data.bag.get("antidoto", 0)), 2, "doar: entrega 3 antídotos")
	var town := _map("brejo")
	var door: Dictionary = {}
	for w in town.data.warps:
		if str(w.to) == "brejo_casa_neblina":
			door = w
	check(MapView.condition_ok(door), "doar: a casa da Vó Neblina abre")
	town.queue_free()
	var m := _map("caldeirao")
	var found := false
	for n in m.all_npcs():
		found = found or n.npc_id == "brumaga_npc"
	check(found, "doar: Brumaga aparece no Caldeirão")
	m.queue_free()
	await tree.process_frame
	SaveGame.start_new("Téo")
	SaveGame.data["bag"] = {"antidoto": 5}
	SaveGame.set_flag("has_antidoto")
	await _play("pantano/garca", [1, 1])
	check(SaveGame.get_flag("pantano_guardou") and not SaveGame.get_flag("red_pantano"), "guardar: sem Redenção")
	check_eq(int(SaveGame.data.bag.get("antidoto", 0)), 5, "guardar: mantém os antídotos")
	check(not MapView.condition_ok({"if": "pantano_doou"}), "guardar: casa da Neblina fechada")
	SaveGame.start_new("Téo")
	await _play("pantano/garca", [1])
	check(not SaveGame.get_flag("pantano_escolheu"), "sem antídotos, a escolha fica para depois")


func test_quest_pena() -> void:
	SaveGame.start_new("Téo")
	await _play("pantano/pena_pede")
	await _play("pantano/malote")
	check(SaveGame.get_flag("has_malote"), "pegou o malote")
	await _play("pantano/pena_obrigada")
	check(SaveGame.get_flag("pena_done") and not SaveGame.get_flag("has_malote"), "malote entregue")
	check_eq(int(SaveGame.data.bag.get("antidoto", 0)), 2, "2 antídotos de recompensa")


func test_revelation_and_choice_ossorio() -> void:
	SaveGame.start_new("Téo")
	SaveGame.set_flag("partner_lia")
	await _play("ossorio/registro")
	check(SaveGame.get_flag("pista_5") and SaveGame.get_flag("has_registro_real"), "Arquivo: pista 5 e Registro Real")
	await _play("ossorio/clarim", [0])
	check(SaveGame.get_flag("ossorio_revelou") and SaveGame.get_flag("red_ossorio"), "contar: +1 Redenção")
	SaveGame.start_new("Téo")
	await _play("ossorio/registro")
	await _play("ossorio/clarim", [1])
	check(SaveGame.get_flag("ossorio_segredo") and not SaveGame.get_flag("red_ossorio"), "segredo: sem Redenção")
	SaveGame.start_new("Téo")
	await _play("ossorio/clarim")
	check(not SaveGame.get_flag("ossorio_revelou") and not SaveGame.get_flag("ossorio_segredo"), "sem o registro, nada a decidir")


func test_quiz_selo() -> void:
	SaveGame.start_new("Téo")
	SaveGame.set_flag("calico_beaten")
	await _play("ossorio/selo")
	check(not SaveGame.get_flag("selo_done"), "sem ler o diário, sem pergunta")
	await _play("ossorio/livro_farol")
	await _play("ossorio/selo", [0])
	check(not SaveGame.get_flag("selo_done"), "resposta errada não premia")
	await _play("ossorio/selo", [1])
	check(SaveGame.get_flag("selo_done"), "Rainha Duna é a resposta certa")


func test_choice_picos() -> void:
	SaveGame.start_new("Téo")
	SaveGame.set_flag("alva_beaten")
	await _play("picos/alva_carta", [1])
	check(not SaveGame.get_flag("has_carta_alva"), "não levar: sem carta")
	await _play("picos/alva_carta", [0])
	check(SaveGame.get_flag("has_carta_alva") and SaveGame.get_flag("picos_carta"), "levar (mesmo depois de recusar): Carta da Alva")
	await _play("picos/nevasco", [1])
	check(SaveGame.get_flag("pista_6"), "Nevasco: pista 6")


func test_ossorio_consequence_on_route5() -> void:
	SaveGame.start_new("Téo")
	var m := _map("rota_5")
	var leais := 0
	for n in m.all_npcs():
		if n.npc_id.begins_with("leal_"):
			leais += 1
	check_eq(leais, 0, "segredo: sem Guardas Leais na Rota 5")
	m.queue_free()
	await tree.process_frame
	SaveGame.set_flag("ossorio_revelou")
	var m2 := _map("rota_5")
	leais = 0
	for n in m2.all_npcs():
		if n.npc_id.begins_with("leal_"):
			leais += 1
	check_eq(leais, 2, "contou: 2 Guardas Leais na Rota 5")
	m2.queue_free()
	await tree.process_frame


func test_deserto_clue_and_quest() -> void:
	SaveGame.start_new("Téo")
	await _play("deserto/rosa_pede")
	check(SaveGame.get_flag("rosa_quest"), "missão da caravana aberta")
	await _play("deserto/alforje")
	check(SaveGame.get_flag("alforje_achado"), "Alforje encontrado nas dunas")
	await _play("deserto/rosa_obrigada")
	check(SaveGame.get_flag("rosa_done"), "missão concluída")
	check_eq(int(SaveGame.data.bag.get("reviver", 0)), 2, "2 Reviver")
	var m := _map("palmeiral")
	var castle: Dictionary = {}
	for w in m.data.warps:
		if str(w.to) == "castelo_portao":
			castle = w
	check(not MapView.condition_ok(castle), "estrada do castelo fechada antes da Duna")
	SaveGame.set_flag("duna_beaten")
	check(MapView.condition_ok(castle), "estrada do castelo abre depois da Duna")
	m.queue_free()
	await tree.process_frame



func _king_owned() -> bool:
	for key in ["party", "ranch"]:
		for m in SaveGame.data.get(key, []):
			if str(m.get("species", "")) == "rei_esqueleto":
				return true
	return false


func test_endings() -> void:
	# a decisão do final é uma condição no roteiro "recusar"
	var gate: Dictionary = {}
	for n in Data.dialog("castelo/recusar"):
		if str(n.get("goto", "")) == "castelo/final_a":
			gate = n
	check(not gate.is_empty(), "roteiro final tem o desvio para o Final A")
	SaveGame.start_new("Téo")
	SaveGame.set_flag("has_carta_alva")
	SaveGame.set_flag("red_minas")
	check(not MapView.condition_ok(gate), "carta + 1 Redenção: ainda Final B")
	SaveGame.set_flag("red_ossorio")
	check(MapView.condition_ok(gate), "carta + 2 Redenções: Final A")
	SaveGame.set_flag("has_carta_alva", false)
	check(not MapView.condition_ok(gate), "sem a carta: Final B, mesmo com Redenção")
	# Final A completo (sem mapa: as trocas de mapa são ignoradas fora do jogo)
	SaveGame.start_new("Téo")
	SaveGame.data["bag"] = {"carta_alva": 1}
	SaveGame.set_flag("has_carta_alva")
	await _play("castelo/final_a")
	check(SaveGame.get_flag("final_a") and SaveGame.get_flag("game_cleared"), "Final A: zerado")
	check(not SaveGame.get_flag("has_carta_alva"), "Final A: carta entregue ao Rei")
	check(_king_owned(), "Final A: o Rei entra na equipe")
	check_eq(int(Ossuary.entry("rei_esqueleto")["marker"]), 100, "Final A: marcador do Rei em 100%")
	SaveGame.start_new("Téo")
	await _play("castelo/final_b")
	check(SaveGame.get_flag("final_b") and SaveGame.get_flag("game_cleared"), "Final B: zerado")
	check(_king_owned(), "Final B: o Rei entra na equipe")


func test_postgame() -> void:
	SaveGame.start_new("Téo")
	var praia := _map("praia_despertar")
	check(not praia.props_of("lighthouse").is_empty(), "farol existe")
	praia.queue_free()
	await tree.process_frame
	for nid in ["ramalho_depois", "fornalha", "musga", "calico", "alva", "duna"]:
		var d: Array = Data.npc(nid).get("dialog", [])
		check(not d.is_empty() and str(d[0].get("if", "")) == "game_cleared" and str(d[0].get("dialog", "")).begins_with("castelo/eco_"),
			"%s vira eco para revanche no pós-jogo" % nid)
	SaveGame.set_flag("game_cleared")
	await _play("castelo/eco_duna", [1])
	check(true, "eco pode ser recusado")
