class_name ScriptActions
extends RefCounted
## Ações de roteiro usadas nos diálogos ({"action": ...}). Formato em docs/DADOS.md.
##   give_partner {species, age, nickname, flag}  dá um dos dois iniciais (fixos, +5%)
##   battle {kind, enemies, tamer_key, reward, items, win_flag, tips, marker}
##   heal                                         cura toda a equipe
##   give_item {item, n}  ·  give_money {n}  ·  marker {species, amount}
##   ranch  ·  shop {id}  ·  respawn (Rancho atual vira o ponto de volta)
##   hide_npc {id}                                o NPC some (para sempre)
##   sfx {name}
##   take_item {item, n}       tira até n unidades (doações)
##   give_monster {species, age, nickname?, golden?}  entra no time (ou Rancho)
##   refresh_map               recarrega o mapa atual (objetos com flags mudam)
##   fade {out}                escurece/clareia a tela · wait {s}
##   credits                   rola os créditos (e volta ao mapa)
##   heal_all                  cura time e Rancho
##   warp {map,x,y,facing,hide_player}  troca de mapa no meio do roteiro
## run() devolve false se o roteiro deve parar (ex.: derrota na batalha).


static func run(n: Dictionary) -> bool:
	match str(n.get("action", "")):
		"give_partner":
			var m := Monster.create(str(n.species), int(n.get("age", 5)))
			m.nickname = TranslationServer.translate(str(n.get("nickname", "")))
			m.starter = true
			var party: Array = SaveGame.data.get("party", [])
			party.append(m.to_dict())
			SaveGame.data["party"] = party
			var uids: Array = SaveGame.data.get("partner_uids", [])
			uids.append(m.uid)
			SaveGame.data["partner_uids"] = uids
			Ossuary.mark_seen(m)
			Ossuary.entry(m.species_id)["recruited"] = true
			if n.has("flag"):
				SaveGame.set_flag(str(n.flag))
			Audio.sfx("recruit")
		"battle":
			var info := {"kind": str(n.get("kind", "tamer")), "enemies": n.get("enemies", []),
				"tamer_key": str(n.get("tamer_key", "BTL_TAMER_DEFAULT")), "reward": int(n.get("reward", 0)),
				"tips": n.get("tips", []), "script": n.get("script", [])}
			if n.has("bg"):
				info["bg"] = str(n["bg"])
			var result: String = await Game.start_battle(info)
			if result != "win":
				return false
			if n.has("win_flag"):
				SaveGame.set_flag(str(n.win_flag))
			for it in n.get("items", []):
				_add_item(str(it[0]), int(it[1]))
				await Game.show_message("MSG_GOT_ITEM", {"item": TranslationServer.translate(str(Data.item(str(it[0])).get("name_key", ""))), "n": int(it[1])})
			if n.has("marker"):
				await _marker(str(n.marker.species), int(n.marker.amount))
		"heal":
			for key in ["party"]:
				var arr: Array = SaveGame.data.get(key, [])
				for i in arr.size():
					var mm := Monster.from_dict(arr[i])
					mm.heal_full()
					arr[i] = mm.to_dict()
			Audio.sfx("heal")
		"give_item":
			_add_item(str(n.item), int(n.get("n", 1)))
			Audio.sfx("save")
			await Game.show_message("MSG_GOT_ITEM", {"item": TranslationServer.translate(str(Data.item(str(n.item)).get("name_key", ""))), "n": int(n.get("n", 1))})
		"give_money":
			SaveGame.data["money"] = int(SaveGame.data.get("money", 0)) + int(n.n)
			Audio.sfx("save")
			await Game.show_message("MSG_GOT_MONEY", {"n": int(n.n)})
		"marker":
			await _marker(str(n.species), int(n.amount))
		"ranch":
			var r := RanchMenu.new()
			Game.open_overlay(r)
			await r.closed
		"shop":
			var s := ShopMenu.new().setup(str(n.id))
			Game.open_overlay(s)
			await s.closed
		"respawn":
			if Game.world and Game.world.player:
				SaveGame.data["respawn"] = {"map": Game.world.map_id, "x": Game.world.player.cell.x,
					"y": Game.world.player.cell.y, "facing": Game.world.player.facing}
		"hide_npc":
			SaveGame.set_flag("npc_gone_" + str(n.id))
			if Game.world and Game.world.map:
				Game.world.map.remove_npc(str(n.id))
		"sfx":
			Audio.sfx(str(n.name))
		"take_item":
			var bag: Dictionary = SaveGame.data.get("bag", {})
			var id := str(n.item)
			var k := mini(int(n.get("n", 1)), int(bag.get(id, 0)))
			bag[id] = int(bag.get(id, 0)) - k
			if int(bag[id]) <= 0:
				bag.erase(id)
				SaveGame.set_flag("has_" + id, false)
			if k > 0:
				await Game.show_message("MSG_GAVE_ITEM", {"item": TranslationServer.translate(str(Data.item(id).get("name_key", ""))), "n": k})
		"give_monster":
			var m2 := Monster.create(str(n.species), int(n.get("age", 5)), bool(n.get("golden", false)))
			if n.has("nickname"):
				m2.nickname = TranslationServer.translate(str(n.nickname))
			Ossuary.mark_seen(m2)
			Ossuary.entry(m2.species_id)["recruited"] = true
			var where := Ossuary.add_to_team(m2)
			Audio.sfx("recruit")
			await Game.show_message("RECRUIT_JOINED" if where == "party" else "RECRUIT_TO_RANCH", {"name": m2.display_name()})
			Game.autosave()
		"warp":
			# leva o jogador a outro mapa; "hide_player" esconde o protagonista
			# (cenas sem ele, como o epílogo de 2040)
			await Game.warp(str(n.map), Vector2i(int(n.get("x", -1)), int(n.get("y", -1))), str(n.get("facing", "down")))
			if Game.world and Game.world.player:
				Game.world.player.visible = not bool(n.get("hide_player", false))
		"refresh_map":
			if Game.world and Game.world.player:
				await Game.warp(Game.world.map_id, Game.world.player.cell, Game.world.player.facing)
		"fade":
			await Game.fade_screen(bool(n.get("out", true)))
		"wait":
			await Game.get_tree().create_timer(float(n.get("s", 1.0))).timeout
		"credits":
			var c := CreditsScreen.new()
			Game.open_overlay(c)
			await c.closed
		"heal_all":
			for key in ["party", "ranch"]:
				var arr2: Array = SaveGame.data.get(key, [])
				for i in arr2.size():
					var mm2 := Monster.from_dict(arr2[i])
					mm2.heal_full()
					arr2[i] = mm2.to_dict()
		_:
			push_warning("ScriptActions: ação desconhecida %s" % str(n.get("action", "")))
	return true


static func _add_item(id: String, count: int) -> void:
	if not SaveGame.data.has("bag"):
		SaveGame.data["bag"] = {}
	SaveGame.data["bag"][id] = int(SaveGame.data["bag"].get(id, 0)) + count
	SaveGame.set_flag("has_" + id)


static func _marker(species: String, amount: int) -> void:
	var e := Ossuary.entry(species)
	var before := int(e["marker"])
	e["seen"] = true
	e["marker"] = mini(100, before + amount)
	await Game.show_message("RECRUIT_MARKER", {"name": TranslationServer.translate(str(Data.species(species).get("name_key", ""))), "a": before, "b": int(e["marker"])})
