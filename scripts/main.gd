extends Node
## Cena principal: entrega o controle ao Game, que monta as camadas e abre o título.


func _ready() -> void:
	Game.boot(self)
