#!/usr/bin/env python3
"""Falas do Ato 1 (docs/roteiro/02_bosque.md) em PT-BR/EN/ES, roteiros
(data/dialogs/bosque.json), NPCs do Bosque, encontros e loja de Raizal."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

T = {
    "SPK_LENHADOR_VELHO": ("Lenhador Velho", "Old Woodcutter", "Leñador Viejo"),
    "SPK_RUFO": ("Rufo", "Rufus", "Rufo"),
    "SPK_IRIS": ("Íris", "Iris", "Iris"),
    "SPK_CIPO": ("Cipó", "Vine", "Bejuco"),
    "SPK_TILIA": ("Dona Tília", "Mrs. Linden", "Doña Tilia"),
    "SPK_TOCO": ("Seu Toco", "Mr. Stump", "Don Tocón"),
    "SPK_SALVIA": ("Sálvia", "Sage", "Salvia"),
    "SPK_GRAVETO": ("Graveto", "Twig", "Ramita"),
    "SPK_HERA": ("Dona Hera", "Mrs. Ivy", "Doña Hiedra"),
    "SPK_GUARDA_RAIZ": ("Guarda-raiz", "Root Guard", "Guardarraíz"),
    "SPK_GALHO": ("Irmãos Galho", "Branch Brothers", "Hermanos Rama"),
    "SPK_MUSGO": ("Pai Musgo", "Papa Moss", "Papá Musgo"),
    "SPK_RAMALHO": ("Ramalho", "Ramalho", "Ramalho"),
    "BTL_TAMER_RUFO": ("Rufo", "Rufus", "Rufo"),
    "BTL_TAMER_IRIS": ("Íris", "Iris", "Iris"),
    "BTL_TAMER_CIPO": ("Cipó", "Vine", "Bejuco"),
    "BTL_TAMER_GALHO": ("Irmãos Galho", "Branch Brothers", "Hermanos Rama"),
    "BTL_TAMER_MUSGO": ("Pai Musgo", "Papa Moss", "Papá Musgo"),
    "BTL_TAMER_RAMALHO": ("Guardião Ramalho", "Guardian Ramalho", "Guardián Ramalho"),
    "MAP_ROTA_1": ("Rota 1", "Route 1", "Ruta 1"),
    "MAP_TUNEL": ("Túnel das Raízes", "Root Tunnel", "Túnel de Raíces"),
    "MAP_RAIZAL": ("Raizal", "Rootvale", "Raizal"),
    "MAP_BOSQUE_VELHO": ("Bosque Velho", "Old Grove", "Bosque Viejo"),
    "MAP_RAIZAL_RANCHO": ("Rancho da Tília", "Linden's Ranch", "Rancho de Tilia"),
    "MAP_RAIZAL_LOJA": ("Venda do Toco", "Stump's Shop", "Tienda de Tocón"),
    "MAP_RAIZAL_CASA_GALHO": ("Casa dos Irmãos Galho", "Branch Brothers' House", "Casa de los Hermanos Rama"),
    "MAP_RAIZAL_CASA_MUSGO": ("Casa da Família Musgo", "Moss Family House", "Casa de la Familia Musgo"),
    "MAP_RAIZAL_CASA_SALVIA": ("Casa da Sálvia", "Sage's House", "Casa de Salvia"),
    "MSG_ROUTE2_LOCKED": ("A estrada das Minas abre na próxima atualização (fase 4c).", "The road to the mines opens in the next update (phase 4c).", "El camino a las minas se abre en la próxima actualización (fase 4c)."),
    "ITEM_ROOT_CHIP": ("Lasca de Raiz", "Root Chip", "Astilla de Raíz"),
    "ITEM_ROOT_CHIP_TEXT": ("Uma lasca do machado do Ramalho. Prova que você venceu o Guardião do Bosque.",
                            "A chip from Ramalho's axe. Proof that you beat the Forest Guardian.",
                            "Una astilla del hacha de Ramalho. Prueba que venciste al Guardián del Bosque."),
    # Rota 1
    "SIGN_B_FORK": ("← Caminho dos Domadores · ↑ Túnel das Raízes · → Campo das Flores",
                    "← Tamers' Trail · ↑ Root Tunnel · → Flower Field",
                    "← Senda de Domadores · ↑ Túnel de Raíces · → Campo de Flores"),
    "OBJ_ROOT_WALL": ("Raízes trançadas fecham a estrada. Só o Guardião manda desfazer.", "Braided roots block the road. Only the Guardian can undo them.", "Raíces trenzadas cierran el camino. Solo el Guardián puede deshacerlas."),
    "DLG_B_VELHO_1": ("Três caminhos, um destino. Domador dá moeda, flor dá esqueleto, túnel dá medo.", "Three paths, one destination. Tamers give coins, flowers give skeletons, the tunnel gives chills.", "Tres caminos, un destino. Los domadores dan monedas, las flores dan esqueletos, el túnel da miedo."),
    "DLG_B_VELHO_2": ("As raízes fecharam a estrada inteira. Só o Ramalho manda desfazer.", "The roots closed the whole road. Only Ramalho can undo them.", "Las raíces cerraron todo el camino. Solo Ramalho puede deshacerlas."),
    "DLG_B_RUFO_1": ("Ei! Você tem cara de quem perde. Prova que eu tô errado!", "Hey! You look like a loser. Prove me wrong!", "¡Eh! Tienes cara de perdedor. ¡Demuestra que me equivoco!"),
    "DLG_B_RUFO_2": ("Tá, tá. Cara de quem ganha. Satisfeito?", "Fine, fine. You look like a winner. Happy?", "Vale, vale. Cara de ganador. ¿Contento?"),
    "DLG_B_IRIS_1": ("Meus esqueletos são lentos, mas quando batem...", "My skeletons are slow, but when they hit...", "Mis esqueletos son lentos, pero cuando pegan..."),
    "DLG_B_IRIS_2": ("Lentos e derrotados. Vou repensar a estratégia.", "Slow and beaten. Time to rethink my strategy.", "Lentos y derrotados. Voy a repensar mi estrategia."),
    "DLG_B_CIPO_1": ("Primo do Rei mandou vigiar. Eu vigio... batalhando!", "The King's cousin told me to keep watch. I watch... by battling!", "El primo del Rey me mandó vigilar. Yo vigilo... ¡peleando!"),
    "DLG_B_CIPO_2": ("Vigiei mal. Não conta pro Ramalho.", "I watched badly. Don't tell Ramalho.", "Vigilé mal. No se lo cuentes a Ramalho."),
    "DLG_B_TUNEL_LIA_1": ("Tá escuro... muito escuro.", "It's dark... really dark.", "Está oscuro... muy oscuro."),
    "DLG_B_TUNEL_LIA_2": ("Tudo bem. Eu tenho luz. Eu vou na frente!", "It's okay. I have light. I'll go first!", "Está bien. Tengo luz. ¡Yo voy delante!"),
    "DLG_B_TUNEL_TARO_1": ("Escuro? Melhor. Ninguém me vê chegando.", "Dark? Good. Nobody sees me coming.", "¿Oscuro? Mejor. Nadie me ve llegar."),
    "DLG_B_TUNEL_LIAR_1": ("Eu... eu tava só olhando a entrada. Não tô com medo!", "I... I was just looking at the entrance. I'm not scared!", "Yo... solo miraba la entrada. ¡No tengo miedo!"),
    "DLG_B_TUNEL_LIAR_2": ("Vai logo.", "Just go.", "Ve ya."),
    "DLG_B_TUNEL_LIAR_3": ("Tá bom, tá bom!", "Okay, okay!", "¡Vale, vale!"),
    "DLG_B_RIVAL_TARO": ("Ramalho sabe pra onde levaram os mais velhos. Eu vou perguntar do meu jeito.", "Ramalho knows where they took the elders. I'll ask him my way.", "Ramalho sabe adónde llevaron a los mayores. Le voy a preguntar a mi manera."),
    "DLG_B_RIVAL_LIA": ("Atravessei sozinha! Agora me enfrenta, que eu tô corajosa!", "I crossed it alone! Now fight me, I'm feeling brave!", "¡Lo crucé sola! Ahora enfréntame, que estoy valiente."),
    "DLG_B_RIVAL_BYE": ("Te vejo em Ossório. Fica vivo... quer dizer, fica inteiro!", "See you in Ossório. Stay alive... I mean, stay in one piece!", "Nos vemos en Ossório. Sigue vivo... digo, ¡sigue entero!"),
    # Raizal
    "SIGN_B_RAIZAL": ("Raizal. Madeira boa, chá melhor.", "Rootvale. Good wood, better tea.", "Raizal. Buena madera, mejor té."),
    "SIGN_B_CLEARING": ("↑ Clareira do Machado (Guardião Ramalho)", "↑ Axe Clearing (Guardian Ramalho)", "↑ Claro del Hacha (Guardián Ramalho)"),
    "DLG_B_TILIA_1": ("Raiz trançada não deixa ninguém sair, nem doente. Deita aí que eu cuido.", "Braided roots don't let anyone out, not even the sick. Lie down, I'll take care of you.", "Las raíces trenzadas no dejan salir a nadie, ni a los enfermos. Acuéstate, que yo te cuido."),
    "DLG_B_TILIA_2": ("Seu esqueleto tá crescendo forte. Já viu quando faz aniversário? Vira festa.", "Your skeleton's growing strong. Ever seen its birthday? It's a party.", "Tu esqueleto crece fuerte. ¿Viste cuando cumple años? Es una fiesta."),
    "DLG_B_TOCO_1": ("Com a estrada fechada, eu vendo o que sobrou. E o que sobrou é caro.", "With the road closed, I sell what's left. And what's left is pricey.", "Con el camino cerrado, vendo lo que sobra. Y lo que sobra es caro."),
    "DLG_B_TOCO_2": ("Volta quando o Ramalho cansar dessa brincadeira.", "Come back when Ramalho gets tired of this game.", "Vuelve cuando Ramalho se canse de este juego."),
    "DLG_B_SALVIA_ASK": ("Meu estoque de erva-de-febre acabou. Tem um pé no Bosque Velho, perto do tronco grande. Traz pra mim?", "I'm out of feverweed. There's a patch in the Old Grove, near the big trunk. Could you bring me some?", "Se me acabó la hierba de fiebre. Hay una mata en el Bosque Viejo, cerca del tronco grande. ¿Me la traes?"),
    "DLG_B_SALVIA_WHERE": ("Bosque Velho, atrás da vila. A erva tem flor azul.", "The Old Grove, behind the village. It has blue flowers.", "El Bosque Viejo, detrás de la villa. Tiene flores azules."),
    "DLG_B_SALVIA_THANKS": ("Isso! Com isso eu curo meia vila. Toma, um Reviver e meu muito obrigada.", "Yes! With this I can heal half the village. Here, a Revive and my heartfelt thanks.", "¡Eso! Con esto curo a media villa. Toma, un Revivir y mi más sincero gracias."),
    "DLG_B_SALVIA_AFTER": ("Quando a estrada abrir, vou mandar chá pra Vila Maré.", "When the road opens, I'll send tea to Tidemark Village.", "Cuando abra el camino, voy a mandar té a Villa Marea."),
    "OBJ_HERB": ("Você colheu a erva-de-febre de flor azul.", "You picked the blue-flowered feverweed.", "Recogiste la hierba de fiebre de flor azul."),
    "DLG_B_GRAVETO": ("Eu tentei desfazer as raízes com os dentes. Agora as raízes têm marca de dente.", "I tried to undo the roots with my teeth. Now the roots have teeth marks.", "Intenté deshacer las raíces con los dientes. Ahora las raíces tienen marcas de dientes."),
    "DLG_B_HERA_1": ("O Ramalho não é mau. É primo do Rei, e todo primo quer agradar.", "Ramalho isn't bad. He's the King's cousin, and every cousin wants to please.", "Ramalho no es malo. Es primo del Rey, y todo primo quiere agradar."),
    "DLG_B_HERA_2": ("Dizem que todos os Guardiões são da família. Família grande dá briga grande.", "They say all the Guardians are family. Big families, big fights.", "Dicen que todos los Guardianes son familia. Familia grande, pelea grande."),
    "DLG_B_GUARDA": ("O Ramalho tá na Clareira. Ele adora visita... pra derrubar.", "Ramalho is in the Clearing. He loves visitors... to knock over.", "Ramalho está en el Claro. Le encantan las visitas... para tumbarlas."),
    "DLG_B_GALHO_1": ("A gente empurra seu turno pra lá e pra cá. Treino pro Ramalho!", "We'll push your turn back and forth. Ramalho training!", "Te empujamos el turno de aquí para allá. ¡Entrenamiento para Ramalho!"),
    "DLG_B_GALHO_2": ("Viu? Golpe leve escapa do atraso.", "See? Light moves dodge the delay.", "¿Viste? Los golpes ligeros escapan del retraso."),
    "DLG_B_MUSGO_1": ("Esporo aqui é tempero.", "Spores are seasoning around here.", "Aquí las esporas son condimento."),
    "DLG_B_MUSGO_2": ("Leva antídoto pras Minas. Lá o ar é pior.", "Bring antidotes to the Mines. The air there is worse.", "Lleva antídotos a las Minas. Allí el aire es peor."),
    # Ramalho
    "DLG_B_RAMALHO_1": ("Primo do Rei, campeão de queda de braço do Bosque e dono deste machado! Você é o tal que abriu o cais?",
                        "Cousin of the King, the forest's arm-wrestling champ, and owner of this axe! Are you the one who opened the dock?",
                        "¡Primo del Rey, campeón de pulso del Bosque y dueño de esta hacha! ¿Eres tú quien abrió el muelle?"),
    "DLG_B_RAMALHO_2": ("Aqui a gente espera. Quem espera não se perde. Deixa eu te ensinar a esperar!", "Around here, we wait. Those who wait don't get lost. Let me teach you how to wait!", "Aquí se espera. Quien espera no se pierde. ¡Déjame enseñarte a esperar!"),
    "DLG_B_RAMALHO_WIN": ("Ha! Bateu antes de eu levantar o machado. Assim não vale... vale, vale.", "Ha! You hit before I could lift my axe. That's not fair... fine, it's fair.", "¡Ja! Pegaste antes de que levantara el hacha. Así no vale... vale, vale."),
    "DLG_B_RAMALHO_MOTIVE": ("O primo me trouxe de volta primeiro. Eu devo tudo a ele. Mas trançar o bosque inteiro... foi demais.", "My cousin brought me back first. I owe him everything. But braiding the whole forest... that was too much.", "Mi primo me trajo de vuelta primero. Se lo debo todo. Pero trenzar el bosque entero... fue demasiado."),
    "DLG_B_RAMALHO_ROOTS": ("Pronto: mandei desfazer as raízes da estrada. Vai, antes que eu mude de ideia!", "There: I've ordered the road roots undone. Go, before I change my mind!", "Listo: mandé deshacer las raíces del camino. ¡Vete antes de que cambie de idea!"),
    "DLG_B_RAMALHO_AFTER": ("Se for às Minas, cuidado com a Tia Fornalha. Ela não ri de nada.", "If you head to the Mines, watch out for Aunt Furnace. She doesn't laugh at anything.", "Si vas a las Minas, cuidado con la Tía Fragua. No se ríe de nada."),
    # Raizerno
    "DLG_B_RAIZERNO_1": ("Um esqueleto enorme dorme fundido ao tronco. Na casca, um brasão: uma coroa sobre uma onda.", "A huge skeleton sleeps fused to the trunk. Carved in the bark: a crown over a wave.", "Un esqueleto enorme duerme fundido al tronco. En la corteza, un escudo: una corona sobre una ola."),
    "DLG_B_RAIZERNO_2": ("O desenho é igual ao do ingresso do museu.", "The design matches the one on the museum ticket.", "El dibujo es igual al de la entrada del museo."),
    "OPT_B_WAKE": ("Acordar", "Wake it", "Despertarlo"),
    "OPT_B_LET_SLEEP": ("Deixar dormir", "Let it sleep", "Dejarlo dormir"),
}


def say(k, spk=None):
    n = {"say": k}
    if spk:
        n["speaker"] = spk
    return n


def battle(tamer, enemies, reward, flag, items=None, kind="tamer", marker=None):
    a = {"action": "battle", "kind": kind, "tamer_key": tamer, "enemies": enemies, "reward": reward}
    if flag:
        a["win_flag"] = flag
    if items:
        a["items"] = items
    if marker:
        a["marker"] = marker
    return a


D = {
    "placa_bifurcacao": [say("SIGN_B_FORK")],
    "raizes": [say("OBJ_ROOT_WALL")],
    "velho": [say("DLG_B_VELHO_1", "SPK_LENHADOR_VELHO"), say("DLG_B_VELHO_2", "SPK_LENHADOR_VELHO")],
    "rufo": [say("DLG_B_RUFO_1", "SPK_RUFO"), battle("BTL_TAMER_RUFO", [["lenhador_1", 12], ["cogumeleiro_1", 12]], 300, "rufo_beaten"), say("DLG_B_RUFO_2", "SPK_RUFO")],
    "rufo_depois": [say("DLG_B_RUFO_2", "SPK_RUFO")],
    "iris": [say("DLG_B_IRIS_1", "SPK_IRIS"), battle("BTL_TAMER_IRIS", [["mineiro_1", 13], ["lenhador_1", 13]], 320, "iris_beaten"), say("DLG_B_IRIS_2", "SPK_IRIS")],
    "iris_depois": [say("DLG_B_IRIS_2", "SPK_IRIS")],
    "cipo": [say("DLG_B_CIPO_1", "SPK_CIPO"), battle("BTL_TAMER_CIPO", [["herborista_1", 14], ["cogumeleiro_1", 14]], 350, "cipo_beaten", [["pocao_m", 1]]), say("DLG_B_CIPO_2", "SPK_CIPO")],
    "cipo_depois": [say("DLG_B_CIPO_2", "SPK_CIPO")],
    "tunel_lia": [say("DLG_B_TUNEL_LIA_1", "SPK_LIA"), say("DLG_B_TUNEL_LIA_2", "SPK_LIA"), {"set_flag": "tunel_visto"}],
    "tunel_taro": [say("DLG_B_TUNEL_TARO_1", "SPK_TARO"), say("DLG_B_TUNEL_LIAR_1", "SPK_LIA"), say("DLG_B_TUNEL_LIAR_2", "SPK_TARO"),
                   say("DLG_B_TUNEL_LIAR_3", "SPK_LIA"), {"set_flag": "tunel_visto"}, {"action": "hide_npc", "id": "lia_tunel"}],
    "rival_taro": [{"say": "DLG_B_RIVAL_TARO", "speaker": "SPK_TARO", "choice": [{"text": "OPT_P_FIGHT", "goto": "bosque/rival_taro_luta"}, {"text": "OPT_P_NOT_NOW", "goto": "vila_mare/rival_depois_taro"}]}],
    "rival_taro_luta": [battle("BTL_TAMER_TARO", [["grumete_1", 14], ["lenhador_1", 13]], 200, "rival_bosque_done", marker={"species": "grumete_1", "amount": 10}),
                        say("DLG_B_RIVAL_BYE", "SPK_TARO"), {"action": "hide_npc", "id": "rival_taro_b"}],
    "rival_lia": [{"say": "DLG_B_RIVAL_LIA", "speaker": "SPK_LIA", "choice": [{"text": "OPT_P_FIGHT", "goto": "bosque/rival_lia_luta"}, {"text": "OPT_P_NOT_NOW", "goto": "vila_mare/rival_depois_lia"}]}],
    "rival_lia_luta": [battle("BTL_TAMER_LIA", [["faroleira_1", 14], ["herborista_1", 13]], 200, "rival_bosque_done", marker={"species": "faroleira_1", "amount": 10}),
                       say("DLG_B_RIVAL_BYE", "SPK_LIA"), {"action": "hide_npc", "id": "rival_lia_b"}],
    "placa_raizal": [say("SIGN_B_RAIZAL")],
    "placa_clareira": [say("SIGN_B_CLEARING")],
    "tilia": [{"action": "heal"}, {"action": "respawn"}, say("DLG_B_TILIA_1", "SPK_TILIA"),
              {"say": "DLG_B_TILIA_2", "speaker": "SPK_TILIA", "choice": [{"text": "OPT_P_RANCH", "goto": "vila_mare/rancho"}, {"text": "OPT_P_LEAVE"}]}],
    "toco": [say("DLG_B_TOCO_1", "SPK_TOCO"), {"action": "shop", "id": "raizal"}, say("DLG_B_TOCO_2", "SPK_TOCO")],
    "salvia_pede": [say("DLG_B_SALVIA_ASK", "SPK_SALVIA"), {"set_flag": "salvia_quest"}, say("DLG_B_SALVIA_WHERE", "SPK_SALVIA")],
    "salvia_onde": [say("DLG_B_SALVIA_WHERE", "SPK_SALVIA")],
    "salvia_obrigada": [say("DLG_B_SALVIA_THANKS", "SPK_SALVIA"), {"action": "give_item", "item": "reviver", "n": 1}, {"set_flag": "salvia_done"}],
    "salvia_depois": [say("DLG_B_SALVIA_AFTER", "SPK_SALVIA")],
    "erva": [say("OBJ_HERB"), {"set_flag": "salvia_herb"}],
    "graveto": [say("DLG_B_GRAVETO", "SPK_GRAVETO")],
    "hera": [say("DLG_B_HERA_1", "SPK_HERA"), say("DLG_B_HERA_2", "SPK_HERA")],
    "guarda": [say("DLG_B_GUARDA", "SPK_GUARDA_RAIZ")],
    "galho": [say("DLG_B_GALHO_1", "SPK_GALHO"), battle("BTL_TAMER_GALHO", [["lenhador_1", 17], ["herborista_1", 16]], 400, "galho_beaten", [["pocao_m", 2]]), say("DLG_B_GALHO_2", "SPK_GALHO")],
    "galho_depois": [say("DLG_B_GALHO_2", "SPK_GALHO")],
    "musgo": [say("DLG_B_MUSGO_1", "SPK_MUSGO"), battle("BTL_TAMER_MUSGO", [["cogumeleiro_1", 16], ["herborista_1", 16]], 350, "musgo_beaten", [["antidoto", 2]]), say("DLG_B_MUSGO_2", "SPK_MUSGO")],
    "musgo_depois": [say("DLG_B_MUSGO_2", "SPK_MUSGO")],
    "ramalho": [say("DLG_B_RAMALHO_1", "SPK_RAMALHO"), say("DLG_B_RAMALHO_2", "SPK_RAMALHO"),
                battle("BTL_TAMER_RAMALHO", [["lenhador_2", 22], ["flautista_2", 22], ["herborista_2", 23]], 800, "ramalho_beaten", kind="boss"),
                say("DLG_B_RAMALHO_WIN", "SPK_RAMALHO"), say("DLG_B_RAMALHO_MOTIVE", "SPK_RAMALHO"),
                {"action": "give_item", "item": "lasca_raiz", "n": 1}, say("DLG_B_RAMALHO_ROOTS", "SPK_RAMALHO"),
                {"action": "hide_npc", "id": "ramalho"}, {"action": "hide_npc", "id": "guarda_raiz"}],
    "ramalho_depois": [say("DLG_B_RAMALHO_MOTIVE", "SPK_RAMALHO"), say("DLG_B_RAMALHO_AFTER", "SPK_RAMALHO")],
    "raizerno": [say("DLG_B_RAIZERNO_1"), {"say": "DLG_B_RAIZERNO_2", "choice": [{"text": "OPT_B_WAKE", "goto": "bosque/raizerno_luta"}, {"text": "OPT_B_LET_SLEEP"}]}],
    "raizerno_luta": [battle("", [["raizerno", 20]], 0, None, kind="wild")],
}


def human(sid, name, dialog, behavior="look_around", tamer=None, role="hint"):
    e = {"name_key": name, "role": role, "sprite": f"res://assets/sprites/npc/{sid}.png", "frames": 2, "idle_fps": 1.2,
         "behavior": behavior, "look_dirs": ["down", "left", "right"], "dialog": dialog}
    if tamer:
        e["tamer"] = tamer
    return e


def tamer_npc(sid, name, ref, flag, vision=4):
    return human(sid, name, [{"if": flag, "dialog": f"bosque/{ref}_depois"}, {"dialog": f"bosque/{ref}"}], "stand",
                 {"vision": vision, "flag": flag}, "tamer")


NPCS = {
    "lenhador_velho": human("lenhador_velho", "SPK_LENHADOR_VELHO", [{"dialog": "bosque/velho"}]),
    "rufo": tamer_npc("rufo", "SPK_RUFO", "rufo", "rufo_beaten"),
    "iris": tamer_npc("iris", "SPK_IRIS", "iris", "iris_beaten"),
    "cipo": tamer_npc("cipo", "SPK_CIPO", "cipo", "cipo_beaten", 3),
    "tilia": human("tilia", "SPK_TILIA", [{"dialog": "bosque/tilia"}], role="ranch"),
    "toco": human("toco", "SPK_TOCO", [{"dialog": "bosque/toco"}], "stand", role="shop"),
    "salvia": human("salvia", "SPK_SALVIA", [{"if": "salvia_done", "dialog": "bosque/salvia_depois"}, {"if": "salvia_herb", "dialog": "bosque/salvia_obrigada"},
                                             {"if": "salvia_quest", "dialog": "bosque/salvia_onde"}, {"dialog": "bosque/salvia_pede"}], role="quest"),
    "graveto": human("graveto", "SPK_GRAVETO", [{"dialog": "bosque/graveto"}]),
    "hera": human("hera", "SPK_HERA", [{"dialog": "bosque/hera"}], role="lore"),
    "guarda_raiz": human("guarda_raiz", "SPK_GUARDA_RAIZ", [{"dialog": "bosque/guarda"}], "stand"),
    "irmao_galho": tamer_npc("irmao_galho", "SPK_GALHO", "galho", "galho_beaten", 3),
    "pai_musgo": tamer_npc("pai_musgo", "SPK_MUSGO", "musgo", "musgo_beaten", 3),
    "ramalho": {"name_key": "SPK_RAMALHO", "role": "guardian", "sprite": "res://assets/sprites/npc/skel_ramalho.png", "frames": 2, "idle_fps": 2.0,
                "behavior": "stand", "dialog": [{"dialog": "bosque/ramalho"}], "tamer": {"vision": 3, "flag": "ramalho_beaten"}},
    "ramalho_depois": {"name_key": "SPK_RAMALHO", "role": "guardian", "sprite": "res://assets/sprites/npc/skel_ramalho.png", "frames": 2, "idle_fps": 2.0,
                       "behavior": "stand", "dialog": [{"dialog": "bosque/ramalho_depois"}]},
    "lia_tunel": {"name_key": "SPK_LIA", "role": "story", "sprite": "res://assets/sprites/npc/skel_lia.png", "frames": 2, "idle_fps": 2.0,
                  "behavior": "stand", "dialog": [{"dialog": "bosque/tunel_taro"}]},
    "rival_lia_b": {"name_key": "SPK_LIA", "role": "story", "sprite": "res://assets/sprites/npc/skel_lia.png", "frames": 2, "idle_fps": 2.0,
                    "behavior": "stand", "dialog": [{"dialog": "bosque/rival_lia"}]},
    "rival_taro_b": {"name_key": "SPK_TARO", "role": "story", "sprite": "res://assets/sprites/npc/skel_taro.png", "frames": 2, "idle_fps": 2.0,
                     "behavior": "stand", "dialog": [{"dialog": "bosque/rival_taro"}]},
}

TABLES = {
    "rota1_sul": [{"species": "lenhador_1", "stage": 1, "min_level": 10, "max_level": 12, "rarity": "comum"},
                  {"species": "herborista_1", "stage": 1, "min_level": 10, "max_level": 12, "rarity": "comum"}],
    "rota1_oeste": [{"species": "lenhador_1", "stage": 1, "min_level": 11, "max_level": 13, "rarity": "comum"}],
    "rota1_campo": [{"species": "herborista_1", "stage": 1, "min_level": 11, "max_level": 14, "rarity": "comum"},
                    {"species": "cogumeleiro_1", "stage": 1, "min_level": 11, "max_level": 14, "rarity": "incomum"},
                    {"species": "flautista_1", "stage": 1, "min_level": 12, "max_level": 15, "rarity": "raro"},
                    {"species": "rendeira_1", "stage": 1, "min_level": 11, "max_level": 13, "rarity": "incomum"}],
    "rota1_norte": [{"species": "lenhador_1", "stage": 1, "min_level": 13, "max_level": 15, "rarity": "comum"},
                    {"species": "cogumeleiro_1", "stage": 1, "min_level": 13, "max_level": 15, "rarity": "incomum"}],
    "tunel": [{"species": "flautista_1", "stage": 1, "min_level": 16, "max_level": 17, "rarity": "raro", "weight": 60},
              {"species": "cogumeleiro_1", "stage": 1, "min_level": 16, "max_level": 17, "rarity": "incomum", "weight": 40}],
}


def main():
    (ROOT / "data/dialogs/bosque.json").write_text(json.dumps({"_comment": "Gerado por tools/maps/bosque_text.py a partir de docs/roteiro/02_bosque.md.", "dialogs": D}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    npcs = json.loads((ROOT / "data/npcs.json").read_text())
    npcs["npcs"].update(NPCS)
    (ROOT / "data/npcs.json").write_text(json.dumps(npcs, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    enc = json.loads((ROOT / "data/encounters.json").read_text())
    enc["tables"].update(TABLES)
    (ROOT / "data/encounters.json").write_text(json.dumps(enc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    shops = json.loads((ROOT / "data/shops.json").read_text())
    shops["shops"]["raizal"] = ["pocao_p", "pocao_m", "antidoto", "reviver"]
    (ROOT / "data/shops.json").write_text(json.dumps(shops, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    items = json.loads((ROOT / "data/items.json").read_text())
    items["items"]["lasca_raiz"] = {"name_key": "ITEM_ROOT_CHIP", "desc_key": "ITEM_ROOT_CHIP_TEXT", "kind": "key", "price": 0, "battle": False, "target": "none"}
    (ROOT / "data/items.json").write_text(json.dumps(items, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    path = ROOT / "i18n/dialogue.csv"
    rows = list(csv.reader(open(path, encoding="utf-8")))
    header, body = rows[0], [r for r in rows[1:] if r and r[0] not in T]
    body += [[k, *v] for k, v in T.items()]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(body)
    words = sum(len(v[0].split()) for k, v in T.items() if k.startswith(("DLG_", "SIGN_", "OBJ_")))
    print(f"bosque: {len(T)} textos, ~{words} palavras PT-BR")


if __name__ == "__main__":
    main()
