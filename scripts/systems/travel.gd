class_name Travel
extends RefCounted
## Viagem rápida: o jogador volta a qualquer cidade que já visitou (pausa → Viajar).
## Nunca leva para frente na história: só cidades visitadas aparecem. A chegada é
## na porta do Rancho da cidade. Regras em data/travel.json.


static func _cfg() -> Dictionary:
	var d = Data.load_json("res://data/travel.json")
	return d if d is Dictionary else {}


static func cities() -> Array:
	var d = Data.load_json("res://data/cities.json")
	return d.get("cities", []) if d is Dictionary else []


static func city_of_map(map_id: String) -> String:
	for c in cities():
		if str(c.get("map", "")) == map_id:
			return str(c["id"])
	return ""


## Chamado ao entrar em qualquer mapa: se for uma cidade, ela vira destino.
static func mark_visited(map_id: String) -> void:
	var cid := city_of_map(map_id)
	if cid == "":
		return
	var v: Array = SaveGame.data.get("visited_cities", [])
	if not v.has(cid):
		v.append(cid)
		SaveGame.data["visited_cities"] = v


static func is_visited(city_id: String) -> bool:
	if SaveGame.data.get("visited_cities", []).has(city_id):
		return true
	var flag := str(_cfg().get("visited_by_flag", {}).get(city_id, ""))
	return flag != "" and SaveGame.get_flag(flag)


## Cidades visitadas, na ordem da história.
static func destinations() -> Array:
	var out := []
	for c in cities():
		if is_visited(str(c["id"])):
			out.append(str(c["id"]))
	return out


static func allowed_here(map_id: String) -> bool:
	return not _cfg().get("blocked_maps", []).has(map_id)


## Nome do destino (o nome do mapa da cidade, já traduzido pela chave).
static func name_key(city_id: String) -> String:
	for c in cities():
		if str(c["id"]) == city_id:
			return str(Data.map(str(c["map"])).get("name_key", city_id))
	return city_id


## Chegada: a célula logo abaixo da porta do Rancho, virado para baixo.
static func arrival(city_id: String) -> Dictionary:
	for c in cities():
		if str(c["id"]) != city_id:
			continue
		var map_id := str(c["map"])
		for w in Data.map(map_id).get("warps", []):
			if str(w.get("to", "")).ends_with("_rancho"):
				return {"map": map_id, "cell": Vector2i(int(w.x), int(w.y) + 1), "facing": "down"}
		var sp: Dictionary = Data.map(map_id).get("spawn", {})
		return {"map": map_id, "cell": Vector2i(int(sp.get("x", -1)), int(sp.get("y", -1))), "facing": "down"}
	return {}
