#!/usr/bin/env python3
"""Ato 2 — Rota 2 e Minas de Cinzas (fase 4c). Fonte única: gera o roteiro
docs/roteiro/03_minas.md, as falas (PT/EN/ES), NPCs, encontros, loja, itens e
mapas (Rota 2, Brasal e interiores, Mina Funda)."""
import json

from regionkit import (ROOT, Region, make_lair, make_route, make_town, room, town_doors, team,
                       say, ask, battle, act, flag, goto, human, skel)

R = Region("minas", 3, "minas", ["minas"])
t = R.t
ref = R.ref

# ------------------------------------------------------------------ nomes
t("SPK_VIGIA_LASCA", "Vigia da Trilha", "Trail Lookout", "Vigía del Sendero")
t("SPK_SEIXO", "Seu Seixo", "Old Pebble", "Don Guijarro")
t("SPK_BRITA", "Brita", "Grit", "Grava")
t("SPK_GRAXA", "Graxa", "Grease", "Grasa")
t("SPK_FULIGEM", "Fuligem", "Soot", "Hollín")
t("SPK_RUBI", "Dona Rubi", "Mrs. Ruby", "Doña Rubí")
t("SPK_COBRE", "Seu Cobre", "Mr. Copper", "Don Cobre")
t("SPK_PIRITA", "Pirita", "Pyrite", "Pirita")
t("SPK_FAGULHA", "Fagulha", "Spark", "Chispa")
t("SPK_TURMALINA", "Vó Turmalina", "Granny Tourmaline", "Abuela Turmalina")
t("SPK_CARVAO", "Seu Carvão", "Old Coal", "Don Carbón")
t("SPK_AGATA", "Ágata", "Agate", "Ágata")
t("SPK_BIGORNA", "Mestre Bigorna", "Master Anvil", "Maestro Yunque")
t("SPK_BLOQUEIO", "Capataz Bloqueio", "Foreman Blockade", "Capataz Bloqueo")
t("SPK_FORNALHA", "Tia Fornalha", "Aunt Furnace", "Tía Fragua")
for k, pt, en, es in [("BRITA", "Brita", "Grit", "Grava"), ("GRAXA", "Graxa", "Grease", "Grasa"), ("FULIGEM", "Fuligem", "Soot", "Hollín"),
                      ("BIGORNA", "Mestre Bigorna", "Master Anvil", "Maestro Yunque"), ("AGATA", "Ágata", "Agate", "Ágata"),
                      ("BLOQUEIO", "Capataz Bloqueio", "Foreman Blockade", "Capataz Bloqueo")]:
    t(f"BTL_TAMER_{k}", pt, en, es)
t("BTL_TAMER_FORNALHA", "Guardiã Tia Fornalha", "Guardian Aunt Furnace", "Guardiana Tía Fragua")
t("MAP_ROTA_2", "Rota 2 — Trilha da Cinza", "Route 2 — Ash Trail", "Ruta 2 — Sendero de Ceniza")
t("MAP_BRASAL", "Brasal", "Embervale", "Brasal")
t("MAP_MINA_FUNDA", "Mina Funda", "Deep Mine", "Mina Honda")
t("MAP_BRASAL_RANCHO", "Rancho da Rubi", "Ruby's Ranch", "Rancho de Rubí")
t("MAP_BRASAL_LOJA", "Armazém do Cobre", "Copper's Store", "Almacén de Cobre")
t("MAP_BRASAL_CASA_BIGORNA", "Oficina do Bigorna", "Anvil's Workshop", "Taller de Yunque")
t("MAP_BRASAL_CASA_AGATA", "Casa da Ágata", "Agate's House", "Casa de Ágata")
t("MAP_BRASAL_CASA_CARVAO", "Casa do Carvão", "Coal's House", "Casa de Carbón")
t("MSG_FORNALHA_ROAD", "Correntes fecham a estrada do norte. Ordem da Tia Fornalha.",
  "Chains block the north road. Aunt Furnace's orders.", "Cadenas cierran el camino del norte. Órdenes de la Tía Fragua.")
t("MSG_CLEARING_ROAD", "O Ramalho não deixa ninguém passar pela Clareira.", "Ramalho won't let anyone through the Clearing.",
  "Ramalho no deja pasar a nadie por el Claro.")
t("MSG_ROUTE3_LOCKED", "Lama funda demais. O caminho para o Pântano ainda não está pronto.",
  "The mud is too deep. The way to the swamp isn't ready yet.", "El barro es demasiado hondo. El camino al pantano aún no está listo.")
t("ITEM_HAMMER", "Martelo da Tia", "Auntie's Hammer", "Martillo de la Tía")
t("ITEM_HAMMER_TEXT", "Presente da Tia Fornalha. Quebra pedra, não quebra promessa. Abre passagens de entulho.",
  "A gift from Aunt Furnace. Breaks stone, never a promise. Clears rubble passages.",
  "Regalo de la Tía Fragua. Rompe piedra, no promesas. Abre pasos de escombros.")
t("ITEM_HELMET", "Capacete do Carvão", "Coal's Helmet", "Casco de Carbón")
t("ITEM_HELMET_TEXT", "Capacete de mineiro com lanterna. Ainda cheira a café.",
  "A miner's helmet with a lamp. It still smells of coffee.", "Casco de minero con linterna. Todavía huele a café.")
R.ITEMS["martelo_tia"] = {"name_key": "ITEM_HAMMER", "desc_key": "ITEM_HAMMER_TEXT", "kind": "key", "price": 0, "battle": False, "target": "none"}
R.ITEMS["capacete_carvao"] = {"name_key": "ITEM_HELMET", "desc_key": "ITEM_HELMET_TEXT", "kind": "key", "price": 0, "battle": False, "target": "none"}

# opções
t("OPT_M_BREAK", "Quebrar a corrente", "Break the chain", "Romper la cadena")
t("OPT_M_TALK", "Pedir que ela solte", "Ask her to let go", "Pedirle que los suelte")
t("OPT_M_RIDE", "Encarar o vagonete", "Face the cart", "Enfrentar la vagoneta")
t("OPT_M_LEAVE", "Deixar quieto", "Leave it be", "Dejarlo tranquilo")

# ------------------------------------------------------------------ Rota 2
t("SIGN_M_FORK", "← Trilha dos Domadores · ↑ Galeria Velha · → Campo de Cascalho",
  "← Tamers' Trail · ↑ Old Gallery · → Gravel Field", "← Senda de Domadores · ↑ Galería Vieja · → Campo de Grava")
t("DLG_M_VIGIA_1", "Alto! Lasca de Raiz? Deixa eu ver... É do machado do Ramalho, sim.",
  "Halt! A Root Chip? Let me see... Yep, that's from Ramalho's axe.", "¡Alto! ¿Astilla de Raíz? A ver... Sí, es del hacha de Ramalho.")
t("DLG_M_VIGIA_2", "Pode passar. Mas lá em cima não é o Bosque. Lá a Tia não ri.",
  "You may pass. But up there it's not the Forest. Up there, Auntie doesn't laugh.", "Puedes pasar. Pero allá arriba no es el Bosque. Allá la Tía no se ríe.")
t("DLG_M_VIGIA_3", "Eu só vigio a trilha. A cinza vigia o resto.", "I just watch the trail. The ash watches everything else.",
  "Yo solo vigilo el sendero. La ceniza vigila lo demás.")
t("DLG_M_SEIXO_1", "Domador paga em moeda, cascalho paga em esqueleto, e a Galeria Velha... paga em susto.",
  "Tamers pay in coins, gravel pays in skeletons, and the Old Gallery... pays in frights.",
  "Los domadores pagan en monedas, la grava paga en esqueletos y la Galería Vieja... paga en sustos.")
t("DLG_M_SEIXO_2", "Lá dentro mora um aguadeiro que canta no escuro. Bonito. Mas bate forte.",
  "A water-carrier lives in there, singing in the dark. Pretty. But it hits hard.",
  "Ahí dentro vive un aguador que canta en la oscuridad. Bonito. Pero pega fuerte.")
t("DLG_M_BRITA_1", "Capacete na cabeça, esqueleto na mão. Bora ver quem cava mais fundo!",
  "Helmet on the head, skeleton in hand. Let's see who digs deeper!", "Casco en la cabeza, esqueleto en mano. ¡A ver quién cava más hondo!")
t("DLG_M_BRITA_2", "Cavei meu próprio buraco. Que vergonha.", "I dug my own hole. How embarrassing.", "Cavé mi propio hoyo. Qué vergüenza.")
t("DLG_M_GRAXA_1", "Esse vagonete não anda há meses. Eu também não. Bora mexer!",
  "This cart hasn't moved in months. Neither have I. Let's get moving!", "Esta vagoneta no se mueve hace meses. Yo tampoco. ¡A movernos!")
t("DLG_M_GRAXA_2", "Pelo menos agora eu tô suado de verdade.", "At least now I'm actually sweaty.", "Al menos ahora sí estoy sudado.")
t("DLG_M_FULIGEM_1", "Limpo chaminé da forja. Respiro fumaça. Meus esqueletos também. Prepara o pulmão!",
  "I sweep the forge chimney. I breathe smoke. So do my skeletons. Brace your lungs!",
  "Limpio la chimenea de la fragua. Respiro humo. Mis esqueletos también. ¡Prepara los pulmones!")
t("DLG_M_FULIGEM_2", "Cof, cof. Leva um antídoto pra Mina. Lá o ar morde.",
  "Cough, cough. Take an antidote to the Mine. The air bites in there.", "Cof, cof. Lleva un antídoto a la Mina. Allí el aire muerde.")

R.d("placa_bifurcacao", [say("SIGN_M_FORK")])
R.d("vigia_entrada", [say("DLG_M_VIGIA_1", "SPK_VIGIA_LASCA"), say("DLG_M_VIGIA_2", "SPK_VIGIA_LASCA"), flag("vigia_lasca_ok")])
R.d("vigia", [say("DLG_M_VIGIA_3", "SPK_VIGIA_LASCA")])
R.d("seixo", [say("DLG_M_SEIXO_1", "SPK_SEIXO"), say("DLG_M_SEIXO_2", "SPK_SEIXO")])
R.d("brita", [say("DLG_M_BRITA_1", "SPK_BRITA"), battle("BTL_TAMER_BRITA", team([("mineiro", 25), ("gasista", 24)]), 420, "brita_beaten"),
              say("DLG_M_BRITA_2", "SPK_BRITA")])
R.d("brita_depois", [say("DLG_M_BRITA_2", "SPK_BRITA")])
R.d("graxa", [say("DLG_M_GRAXA_1", "SPK_GRAXA"), battle("BTL_TAMER_GRAXA", team([("lenhador", 26), ("mineiro", 25)]), 450, "graxa_beaten"),
              say("DLG_M_GRAXA_2", "SPK_GRAXA")])
R.d("graxa_depois", [say("DLG_M_GRAXA_2", "SPK_GRAXA")])
R.d("fuligem", [say("DLG_M_FULIGEM_1", "SPK_FULIGEM"),
                battle("BTL_TAMER_FULIGEM", team([("gasista", 27), ("ferreiro", 26)]), 480, "fuligem_beaten", [["pocao_m", 1], ["antidoto", 1]]),
                say("DLG_M_FULIGEM_2", "SPK_FULIGEM")])
R.d("fuligem_depois", [say("DLG_M_FULIGEM_2", "SPK_FULIGEM")])

R.NPCS["vigia_lasca"] = human("vigia_lasca", "SPK_VIGIA_LASCA", [{"dialog": ref("vigia")}], "stand")
R.NPCS["seixo"] = human("seixo", "SPK_SEIXO", [{"dialog": ref("seixo")}])
R.tamer("brita", "brita", "SPK_BRITA", "brita", "brita_beaten")
R.tamer("graxa", "graxa", "SPK_GRAXA", "graxa", "graxa_beaten")
R.tamer("fuligem", "fuligem", "SPK_FULIGEM", "fuligem", "fuligem_beaten", 3)

# ------------------------------------------------------------------ Brasal
t("SIGN_M_BRASAL", "Brasal. Aqui o fogo nunca dorme. Nem a gente.", "Embervale. The fire never sleeps here. Neither do we.",
  "Brasal. Aquí el fuego nunca duerme. Nosotros tampoco.")
t("SIGN_M_MINE", "← Mina Funda. Entrada proibida por ordem da Tia.", "← Deep Mine. Entry forbidden by Auntie's orders.",
  "← Mina Honda. Entrada prohibida por orden de la Tía.")
t("DLG_M_RUBI_1", "Cinza no cabelo, cinza no chá, cinza no travesseiro. Deita, que pelo menos aqui é quentinho.",
  "Ash in your hair, ash in your tea, ash on your pillow. Lie down, at least it's cozy here.",
  "Ceniza en el pelo, en el té, en la almohada. Acuéstate, que al menos aquí está calentito.")
t("DLG_M_RUBI_2", "Antes, o Rancho vivia cheio de mineiro com esqueleto no colo. Agora só tem você.",
  "This Ranch used to be full of miners with skeletons on their laps. Now it's just you.",
  "Antes el Rancho vivía lleno de mineros con esqueletos en el regazo. Ahora solo estás tú.")
t("DLG_M_COBRE_1", "Minério? Não tem. Mas poção grande eu arranjo. Do jeito que o povo apanha...",
  "Ore? None. But I can get you big potions. The way folks get knocked around...",
  "¿Mineral? No hay. Pero pociones grandes sí consigo. Con lo que la gente recibe...")
t("DLG_M_COBRE_BROKE", "Com os mineiros fugidos, tudo encareceu. Não me olha assim, a culpa é de quem quebrou.",
  "With the miners gone, everything got pricier. Don't look at me like that, blame whoever broke things.",
  "Con los mineros huidos, todo subió. No me mires así, la culpa es de quien rompió.")
t("DLG_M_COBRE_DEAL", "Os mineiros voltaram e o minério também. Pra você, desconto de amigo.",
  "The miners came back, and so did the ore. Friend's discount for you.", "Volvieron los mineros y el mineral también. Para ti, descuento de amigo.")
t("DLG_M_COBRE_2", "Volte sempre. E bata a cinza da bota antes de entrar.", "Come back anytime. And knock the ash off your boots first.",
  "Vuelve cuando quieras. Y sacúdete la ceniza de las botas antes de entrar.")
t("DLG_M_PIRITA", "Fiz bolo pro aniversário do meu esqueleto. Ficou com gosto de cinza. Tudo aqui tem.",
  "I baked a cake for my skeleton's birthday. It tasted like ash. Everything here does.",
  "Hice un pastel para el cumpleaños de mi esqueleto. Sabía a ceniza. Aquí todo sabe así.")
t("DLG_M_PIRITA_AFTER", "A fumaça baixou! Vou fazer outro bolo. Com cobertura de verdade, dessa vez.",
  "The smoke's gone down! I'm baking another cake. With real frosting this time.",
  "¡Bajó el humo! Voy a hacer otro pastel. Con cobertura de verdad esta vez.")
t("DLG_M_FAGULHA_1", "Os esqueletos da Tia são duros feito pedra. Soco nem faz cócegas!",
  "Auntie's skeletons are hard as rock. Punches don't even tickle!", "¡Los esqueletos de la Tía son duros como piedra! ¡Los golpes ni les hacen cosquillas!")
t("DLG_M_FAGULHA_2", "Mas faísca entra em qualquer fresta. Golpe Mágico bate na RES, não na DEF. Anota!",
  "But a spark gets into any crack. Magic moves hit RES, not DEF. Write that down!",
  "Pero una chispa entra por cualquier rendija. Los golpes Mágicos van contra RES, no DEF. ¡Apúntalo!")
t("DLG_M_TURMALINA_1", "A Fornalha forjou o sino desta cidade, no tempo do reino. Agora só forja corrente.",
  "Furnace forged this town's bell, back in the kingdom days. Now she only forges chains.",
  "La Fragua forjó la campana de este pueblo, en tiempos del reino. Ahora solo forja cadenas.")
t("DLG_M_TURMALINA_2", "Tia do Rei, dizem. Cuidava dele quando ele era menino. Quem cuida demais, prende.",
  "The King's aunt, they say. She looked after him as a boy. Those who care too much end up caging.",
  "Tía del Rey, dicen. Lo cuidaba de niño. Quien cuida de más, termina encerrando.")
t("DLG_M_CARVAO_ASK", "A Tia expulsou os mineiros de gente. Na correria, larguei meu capacete na Mina Funda. Busca pra mim?",
  "Auntie threw out all the human miners. In the rush, I left my helmet in the Deep Mine. Fetch it for me?",
  "La Tía echó a los mineros humanos. Con las prisas, dejé mi casco en la Mina Honda. ¿Me lo traes?")
t("DLG_M_CARVAO_WHERE", "Na câmara do sul da mina, perto dos trilhos. A lanterna ainda deve estar acesa.",
  "In the mine's south chamber, by the rails. The lamp should still be lit.", "En la cámara sur de la mina, junto a los rieles. La linterna debe seguir encendida.")
t("DLG_M_CARVAO_THANKS", "Meu capacete! Quarenta anos de mina nessa lata. Toma, duas Poções G. E olha o mapa ali na parede.",
  "My helmet! Forty years of mining in this tin. Here, two Potions L. And take a look at the map on the wall.",
  "¡Mi casco! Cuarenta años de mina en esta lata. Toma, dos Pociones G. Y mira el mapa de la pared.")
t("DLG_M_CARVAO_AFTER", "Esse mapa é mais velho que a mina. Meu avô dizia que o mar desenhou ele sozinho.",
  "That map is older than the mine. My grandpa said the sea drew it by itself.", "Ese mapa es más viejo que la mina. Mi abuelo decía que el mar lo dibujó solo.")
t("OBJ_M_HELMET", "Um capacete com a lanterna acesa, caído entre os trilhos.", "A helmet with its lamp still lit, lying between the rails.",
  "Un casco con la linterna encendida, tirado entre los rieles.")
t("DLG_M_MAP_1", "Um mapa antigo da costa, com três baías lado a lado e um farol na do meio.",
  "An old map of the coast, with three bays side by side and a lighthouse on the middle one.",
  "Un mapa antiguo de la costa, con tres bahías una al lado de otra y un faro en la del medio.")
t("DLG_M_MAP_2", "Você conhece essas três baías. São as da sua cidade, em 2040. Só os nomes estão errados.",
  "You know these three bays. They're your hometown's, in 2040. Only the names are wrong.",
  "Conoces estas tres bahías. Son las de tu ciudad, en 2040. Solo los nombres están mal.")
t("DLG_M_MAP_3", "Coincidência... não é?", "Just a coincidence... right?", "Una coincidencia... ¿no?")
t("DLG_M_BIGORNA_1", "Aqui se treina defesa. Meus esqueletos sobem a guarda até você cansar de bater.",
  "We train defense here. My skeletons raise their guard until you're tired of hitting.",
  "Aquí se entrena defensa. Mis esqueletos suben la guardia hasta que te canses de pegar.")
t("DLG_M_BIGORNA_2", "Contra parede, não empurra: procura a fresta. A Tia luta igualzinho.",
  "Against a wall, don't push: find the crack. Auntie fights the same way.", "Contra un muro, no empujes: busca la grieta. La Tía pelea igualito.")
t("DLG_M_AGATA_1", "Gás de mina é perfume pra mim. Aguenta três rodadas de veneno?",
  "Mine gas is perfume to me. Can you take three rounds of poison?", "El gas de mina es perfume para mí. ¿Aguantas tres rondas de veneno?")
t("DLG_M_AGATA_2", "Aguentou. Leva esses antídotos, você mereceu respirar.", "You held out. Take these antidotes, you've earned some fresh air.",
  "Aguantaste. Llévate estos antídotos, te ganaste respirar.")
t("DLG_M_ROAD_GUARD", "Ordem da Tia: ninguém sai. Nem eu. E olha que eu queria.", "Auntie's orders: nobody leaves. Not even me. And believe me, I'd like to.",
  "Orden de la Tía: nadie sale. Ni yo. Y mira que me gustaría.")

R.d("placa_brasal", [say("SIGN_M_BRASAL")])
R.d("placa_mina", [say("SIGN_M_MINE")])
R.d("rubi", [act("heal"), act("respawn"), say("DLG_M_RUBI_1", "SPK_RUBI"),
             ask("DLG_M_RUBI_2", "SPK_RUBI", [("OPT_P_RANCH", "vila_mare/rancho"), ("OPT_P_LEAVE", None)])])
R.d("cobre", [{"say": "DLG_M_COBRE_BROKE", "speaker": "SPK_COBRE", "if": "minas_quebrou"},
              {"say": "DLG_M_COBRE_DEAL", "speaker": "SPK_COBRE", "if": "minas_negociou"},
              {"say": "DLG_M_COBRE_1", "speaker": "SPK_COBRE", "if_not": "fornalha_beaten"},
              act("shop", id="brasal"), say("DLG_M_COBRE_2", "SPK_COBRE")])
R.d("pirita", [{"say": "DLG_M_PIRITA_AFTER", "speaker": "SPK_PIRITA", "if": "fornalha_beaten"},
               {"say": "DLG_M_PIRITA", "speaker": "SPK_PIRITA", "if_not": "fornalha_beaten"}])
R.d("fagulha", [say("DLG_M_FAGULHA_1", "SPK_FAGULHA"), say("DLG_M_FAGULHA_2", "SPK_FAGULHA")])
R.d("turmalina", [say("DLG_M_TURMALINA_1", "SPK_TURMALINA"), say("DLG_M_TURMALINA_2", "SPK_TURMALINA")])
R.d("carvao_pede", [say("DLG_M_CARVAO_ASK", "SPK_CARVAO"), flag("carvao_quest"), say("DLG_M_CARVAO_WHERE", "SPK_CARVAO")])
R.d("carvao_onde", [say("DLG_M_CARVAO_WHERE", "SPK_CARVAO")])
R.d("carvao_obrigado", [say("DLG_M_CARVAO_THANKS", "SPK_CARVAO"), act("take_item", item="capacete_carvao", n=1),
                        act("give_item", item="pocao_g", n=2), flag("carvao_done")])
R.d("carvao_depois", [say("DLG_M_CARVAO_AFTER", "SPK_CARVAO")])
R.d("capacete", [say("OBJ_M_HELMET"), act("give_item", item="capacete_carvao", n=1)])
R.d("mapa_antigo", [say("DLG_M_MAP_1"), say("DLG_M_MAP_2"), say("DLG_M_MAP_3"), flag("pista_3")])
R.d("bigorna", [say("DLG_M_BIGORNA_1", "SPK_BIGORNA"),
                battle("BTL_TAMER_BIGORNA", team([("ferreiro", 30), ("mineiro", 30)]), 620, "bigorna_beaten", [["pocao_m", 2]]),
                say("DLG_M_BIGORNA_2", "SPK_BIGORNA")])
R.d("bigorna_depois", [say("DLG_M_BIGORNA_2", "SPK_BIGORNA")])
R.d("agata", [say("DLG_M_AGATA_1", "SPK_AGATA"),
              battle("BTL_TAMER_AGATA", team([("gasista", 30), ("aguadeiro", 29)]), 560, "agata_beaten", [["antidoto", 3], ["reviver", 1]]),
              say("DLG_M_AGATA_2", "SPK_AGATA")])
R.d("agata_depois", [say("DLG_M_AGATA_2", "SPK_AGATA")])
R.d("guarda_estrada", [say("DLG_M_ROAD_GUARD", "SPK_BLOQUEIO")])

R.NPCS["rubi"] = human("rubi", "SPK_RUBI", [{"dialog": ref("rubi")}], role="ranch")
R.NPCS["cobre"] = human("cobre", "SPK_COBRE", [{"dialog": ref("cobre")}], "stand", role="shop")
R.NPCS["pirita"] = human("pirita", "SPK_PIRITA", [{"dialog": ref("pirita")}], role="humor")
R.NPCS["fagulha"] = human("fagulha", "SPK_FAGULHA", [{"dialog": ref("fagulha")}])
R.NPCS["turmalina"] = human("turmalina", "SPK_TURMALINA", [{"dialog": ref("turmalina")}], "stand", role="lore")
R.NPCS["carvao"] = human("carvao", "SPK_CARVAO", [{"if": "carvao_done", "dialog": ref("carvao_depois")},
                                                  {"if": "has_capacete_carvao", "dialog": ref("carvao_obrigado")},
                                                  {"if": "carvao_quest", "dialog": ref("carvao_onde")}, {"dialog": ref("carvao_pede")}], "stand", role="quest")
R.tamer("bigorna", "bigorna", "SPK_BIGORNA", "bigorna", "bigorna_beaten", 3)
R.tamer("agata", "agata", "SPK_AGATA", "agata", "agata_beaten", 3)
R.NPCS["guarda_estrada"] = human("bloqueio", "SPK_BLOQUEIO", [{"dialog": ref("guarda_estrada")}], "stand")

# ------------------------------------------------------------------ Mina Funda: capataz, Taro, Vagonauta
t("DLG_M_BLOQ_1", "Turno da noite, turno do dia, turno de bater em intruso. Hoje é o terceiro.",
  "Night shift, day shift, intruder-bashing shift. Today's the third one.", "Turno de noche, turno de día, turno de golpear intrusos. Hoy toca el tercero.")
t("DLG_M_BLOQ_2", "Tá. Pode ir até a forja. Mas eu não vi você.", "Fine. Go on to the forge. But I never saw you.", "Vale. Sigue hasta la fragua. Pero yo no te vi.")
R.d("bloqueio", [say("DLG_M_BLOQ_1", "SPK_BLOQUEIO"), battle("BTL_TAMER_BLOQUEIO", team([("mineiro", 31), ("ferreiro", 31)]), 500, "bloqueio_beaten"),
                 say("DLG_M_BLOQ_2", "SPK_BLOQUEIO")])
R.d("bloqueio_depois", [say("DLG_M_BLOQ_2", "SPK_BLOQUEIO")])
R.tamer("bloqueio", "bloqueio", "SPK_BLOQUEIO", "bloqueio", "bloqueio_beaten", 3)

t("DLG_M_SCARF_0", "Um lenço vermelho com bolinhas amarelas, preso num prego da viga.", "A red scarf with yellow dots, caught on a nail in the beam.",
  "Un pañuelo rojo con lunares amarillos, enganchado en un clavo de la viga.")
t("DLG_M_SCARF_T1", "Esse lenço... é da minha mãe. Ela amarrava no meu pescoço quando eu tinha frio.",
  "This scarf... it's my mom's. She'd tie it around my neck when I was cold.", "Este pañuelo... es de mi mamá. Me lo ataba al cuello cuando tenía frío.")
t("DLG_M_SCARF_T2", "Ela passou por aqui. Então ela tá... inteira. Tá inteira.", "She came through here. So she's... in one piece. She's in one piece.",
  "Pasó por aquí. Entonces está... entera. Está entera.")
t("DLG_M_SCARF_T3", "Vamos mais rápido. Por favor.", "Let's go faster. Please.", "Vamos más rápido. Por favor.")
t("DLG_M_SCARF_R1", "Ei. Não encosta. Esse lenço é da minha mãe.", "Hey. Don't touch that. That scarf is my mom's.",
  "Eh. No lo toques. Ese pañuelo es de mi mamá.")
t("DLG_M_SCARF_R2", "Os capangas trouxeram os levados por esta mina, rumo ao norte. Ela tá viva... quer dizer, inteira.",
  "The henchmen brought the ones they took through this mine, heading north. She's alive... I mean, in one piece.",
  "Los secuaces trajeron a los que se llevaron por esta mina, rumbo al norte. Está viva... digo, entera.")
t("DLG_M_SCARF_L1", "A gente ajuda a procurar, Taro! Eu ilumino, você corre.", "We'll help you look, Taro! I'll light the way, you run.",
  "¡Te ayudamos a buscar, Taro! Yo ilumino, tú corres.")
t("DLG_M_SCARF_R3", "...Valeu. Mas eu vou na frente. Sempre vou.", "...Thanks. But I'm going ahead. I always do.", "...Gracias. Pero yo voy delante. Siempre.")
R.d("lenco_parceiro", [say("DLG_M_SCARF_0"), say("DLG_M_SCARF_T1", "SPK_TARO"), say("DLG_M_SCARF_T2", "SPK_TARO"), say("DLG_M_SCARF_T3", "SPK_TARO"),
                       flag("lenco_visto")])
R.d("lenco_recorrente", [say("DLG_M_SCARF_R1", "SPK_TARO"), say("DLG_M_SCARF_R2", "SPK_TARO"), say("DLG_M_SCARF_L1", "SPK_LIA"),
                         say("DLG_M_SCARF_R3", "SPK_TARO"), flag("lenco_visto"), act("hide_npc", id="taro_mina")])
R.NPCS["taro_mina"] = skel("skel_taro", "SPK_TARO", [{"dialog": ref("lenco_recorrente")}])

t("DLG_M_VAGO_1", "Um vagonete com cara de esqueleto desce os trilhos sozinho, livre e furioso.",
  "A cart with a skeleton's face rolls down the rails on its own, free and furious.",
  "Una vagoneta con cara de esqueleto baja sola por los rieles, libre y furiosa.")
R.d("vagonauta", [ask("DLG_M_VAGO_1", None, [("OPT_M_RIDE", ref("vagonauta_luta")), ("OPT_M_LEAVE", None)])])
R.d("vagonauta_luta", [battle("", [["vagonauta", 30]], 0, kind="wild")])
R.NPCS["vagonauta_npc"] = skel("skel_vagonauta", "SPECIES_VAGONAUTA", [{"dialog": ref("vagonauta")}], role="wild")

# ------------------------------------------------------------------ Guardiã: Tia Fornalha
t("DLG_M_FOR_1", "Regra um: ninguém entra na forja sem bater. Você não bateu.",
  "Rule one: nobody enters the forge without knocking. You didn't knock.", "Regla uno: nadie entra en la fragua sin llamar. Tú no llamaste.")
t("DLG_M_FOR_2", "Eu forjo as correntes que fecham as estradas. Estrada fechada, ninguém se perde. Simples.",
  "I forge the chains that close the roads. Closed road, nobody gets lost. Simple.",
  "Yo forjo las cadenas que cierran los caminos. Camino cerrado, nadie se pierde. Simple.")
t("DLG_M_FOR_3", "Regra dois: quem quer passar, aguenta o calor. Vamos ver.", "Rule two: whoever wants through, takes the heat. Let's see.",
  "Regla dos: quien quiere pasar, aguanta el calor. A ver.")
t("DLG_M_FOR_WIN", "Hmpf. Regra três: quem vence, fala. Fala logo.", "Hmph. Rule three: the winner speaks. Speak, then.",
  "Hmpf. Regla tres: quien gana, habla. Habla ya.")
t("DLG_M_FOR_MOTIVE", "O Rei é meu sobrinho. Quando a coroa rachar, a família vai embora de novo. Enquanto houver corrente, ninguém vai.",
  "The King is my nephew. When the crown cracks, the family goes away again. As long as there are chains, nobody goes.",
  "El Rey es mi sobrino. Cuando la corona se rompa, la familia se irá otra vez. Mientras haya cadenas, nadie se va.")
t("DLG_M_FOR_CHOICE", "A corrente mestra prende todos os mineiros à forja. O que você vai fazer?",
  "The master chain binds every miner to the forge. What will you do?", "La cadena maestra ata a todos los mineros a la fragua. ¿Qué vas a hacer?")
t("DLG_M_BREAK_1", "Você puxa a alavanca da forja. A corrente mestra estoura com um estrondo.",
  "You pull the forge lever. The master chain bursts with a bang.", "Tiras de la palanca de la fragua. La cadena maestra revienta con un estruendo.")
t("DLG_M_BREAK_2", "Sem ordem, eles vão correr pro escuro! Olha só!", "Without orders, they'll run off into the dark! Look!",
  "¡Sin órdenes, van a correr a la oscuridad! ¡Mira!")
t("DLG_M_BREAK_3", "Os esqueletos mineiros fogem pelas galerias. Um vagonete desgovernado some trilho abaixo.",
  "The miner skeletons flee down the galleries. A runaway cart vanishes down the rails.",
  "Los esqueletos mineros huyen por las galerías. Una vagoneta desbocada se pierde rieles abajo.")
t("DLG_M_BREAK_4", "Vai. A estrada tá aberta. E não volta pedindo desconto.", "Go. The road is open. And don't come back asking for a discount.",
  "Vete. El camino está abierto. Y no vuelvas pidiendo descuento.")
t("DLG_M_TALK_1", "Pedir? Faz cem anos que ninguém me pede nada. Só obedecem.",
  "Ask? Nobody's asked me anything in a hundred years. They just obey.", "¿Pedir? Hace cien años que nadie me pide nada. Solo obedecen.")
t("DLG_M_TALK_2", "...Regra quatro, que eu acabei de inventar: quem pede direito, recebe direito.",
  "...Rule four, which I just made up: whoever asks properly, gets properly.", "...Regla cuatro, que acabo de inventar: quien pide bien, recibe bien.")
t("DLG_M_TALK_3", "Turno encerrado! Soltem as correntes e vão pra casa. Amanhã, quem quiser, volta.",
  "Shift's over! Drop the chains and go home. Tomorrow, whoever wants to, comes back.",
  "¡Se acabó el turno! Suelten las cadenas y a casa. Mañana, quien quiera, vuelve.")
t("DLG_M_TALK_4", "Leva meu martelo. Quebra pedra, não quebra promessa. Vai ter entulho no caminho do Pântano.",
  "Take my hammer. It breaks stone, never a promise. There'll be rubble on the way to the Swamp.",
  "Llévate mi martillo. Rompe piedra, no promesas. Habrá escombros camino al Pantano.")
t("DLG_M_FOR_BYE", "Se encontrar a Musga no Pântano, manda ela comer direito. É ordem da tia.",
  "If you see Musga in the Swamp, tell her to eat properly. Auntie's orders.", "Si ves a Musga en el Pantano, dile que coma bien. Orden de la tía.")
t("DLG_M_FOR_AFTER_DEAL", "Os mineiros voltaram sozinhos. Trabalham mais rápido sem corrente. Não conta pra ninguém.",
  "The miners came back on their own. They work faster without chains. Don't tell anyone.",
  "Los mineros volvieron solos. Trabajan más rápido sin cadenas. No se lo cuentes a nadie.")
t("DLG_M_FOR_AFTER_BREAK", "As galerias estão vazias. Espero que você saiba o que fez.", "The galleries are empty. I hope you know what you did.",
  "Las galerías están vacías. Espero que sepas lo que hiciste.")

FORNALHA_TEAM = team([("mineiro", 34), ("ferreiro", 33), ("gasista", 35), ("aguadeiro", 34)])
R.d("fornalha", [say("DLG_M_FOR_1", "SPK_FORNALHA"), say("DLG_M_FOR_2", "SPK_FORNALHA"), say("DLG_M_FOR_3", "SPK_FORNALHA"),
                 battle("BTL_TAMER_FORNALHA", FORNALHA_TEAM, 1000, "fornalha_beaten", kind="boss"),
                 say("DLG_M_FOR_WIN", "SPK_FORNALHA"), say("DLG_M_FOR_MOTIVE", "SPK_FORNALHA"),
                 ask("DLG_M_FOR_CHOICE", None, [("OPT_M_BREAK", ref("quebrar")), ("OPT_M_TALK", ref("negociar"))])])
R.d("quebrar", [say("DLG_M_BREAK_1"), say("DLG_M_BREAK_2", "SPK_FORNALHA"), say("DLG_M_BREAK_3"), flag("minas_quebrou"),
                say("DLG_M_BREAK_4", "SPK_FORNALHA"), say("DLG_M_FOR_BYE", "SPK_FORNALHA"), act("refresh_map")])
R.d("negociar", [say("DLG_M_TALK_1", "SPK_FORNALHA"), say("DLG_M_TALK_2", "SPK_FORNALHA"), say("DLG_M_TALK_3", "SPK_FORNALHA"),
                 flag("minas_negociou"), flag("red_minas"), act("give_item", item="martelo_tia", n=1),
                 say("DLG_M_TALK_4", "SPK_FORNALHA"), say("DLG_M_FOR_BYE", "SPK_FORNALHA"), act("refresh_map")])
R.d("fornalha_depois", [{"say": "DLG_M_FOR_AFTER_DEAL", "speaker": "SPK_FORNALHA", "if": "minas_negociou"},
                        {"say": "DLG_M_FOR_AFTER_BREAK", "speaker": "SPK_FORNALHA", "if": "minas_quebrou"},
                        say("DLG_M_FOR_BYE", "SPK_FORNALHA")])
# se a escolha for interrompida (app fechado), a Tia repete a pergunta
R.d("fornalha_escolha", [say("DLG_M_FOR_MOTIVE", "SPK_FORNALHA"),
                         ask("DLG_M_FOR_CHOICE", None, [("OPT_M_BREAK", ref("quebrar")), ("OPT_M_TALK", ref("negociar"))])])
R.NPCS["fornalha"] = {"name_key": "SPK_FORNALHA", "role": "guardian", "sprite": "res://assets/sprites/npc/skel_fornalha.png", "frames": 2,
                      "idle_fps": 2.0, "behavior": "stand",
                      "dialog": [{"if_any": ["minas_quebrou", "minas_negociou"], "dialog": ref("fornalha_depois")},
                                 {"if": "fornalha_beaten", "dialog": ref("fornalha_escolha")}, {"dialog": ref("fornalha")}],
                      "tamer": {"vision": 3, "flag": "fornalha_beaten"}}
# mineiros esqueletos: acorrentados antes, voltando por vontade própria depois de negociar
t("DLG_M_MINER_CHAINED", "Clang. Clang. Clang. O esqueleto não para de martelar. Nem olha pra você.",
  "Clang. Clang. Clang. The skeleton won't stop hammering. It doesn't even look at you.",
  "Clang. Clang. Clang. El esqueleto no deja de martillar. Ni te mira.")
t("DLG_M_MINER_FREE", "O esqueleto mineiro martela devagar, cantarolando. Ninguém mandou: ele quis.",
  "The miner skeleton hammers slowly, humming. Nobody ordered it: it wanted to.",
  "El esqueleto minero martilla despacio, tarareando. Nadie se lo ordenó: quiso.")
R.d("mineiro_preso", [say("DLG_M_MINER_CHAINED")])
R.d("mineiro_livre", [say("DLG_M_MINER_FREE")])
R.NPCS["mineiro_forja"] = skel("skel_mineiro", "SPECIES_MINEIRO_2", [{"if": "minas_negociou", "dialog": ref("mineiro_livre")},
                                                                     {"dialog": ref("mineiro_preso")}], role="story")


# ------------------------------------------------------------------ parceiro comenta (1ª visita) e mundo que reage
t("DLG_M_ARR_R2_L1", "Por que tudo aqui é cinza? Até a grama! Será que alguém pintou?", "Why is everything gray here? Even the grass! Did someone paint it?",
  "¿Por qué aquí todo es gris? ¡Hasta la hierba! ¿Alguien la pintó?")
t("DLG_M_ARR_R2_L2", "Ah, é fumaça. Tem uma chaminé enorme lá no norte. Quem acende um fogo desse tamanho?",
  "Oh, it's smoke. There's a huge chimney up north. Who lights a fire that big?", "Ah, es humo. Hay una chimenea enorme al norte. ¿Quién enciende un fuego tan grande?")
t("DLG_M_ARR_R2_T1", "Cheiro de forja. Meu pai cheirava assim quando voltava do trabalho.", "Smells like a forge. My dad smelled like this when he came home from work.",
  "Huele a fragua. Mi papá olía así cuando volvía del trabajo.")
t("DLG_M_ARR_R2_T2", "...Anda. Tô com pressa.", "...Come on. I'm in a hurry.", "...Vamos. Tengo prisa.")
t("DLG_M_ARR_BR_L1", "Ninguém na rua... As janelas tão fechadas por causa da cinza?", "Nobody in the streets... Are the windows shut because of the ash?",
  "Nadie en la calle... ¿Las ventanas están cerradas por la ceniza?")
t("DLG_M_ARR_BR_L2", "Se eu fosse uma cidade, ia querer alguém pra abrir as janelas.", "If I were a town, I'd want someone to open my windows.",
  "Si yo fuera un pueblo, querría que alguien abriera mis ventanas.")
t("DLG_M_ARR_BR_T1", "Cidade parada. Mina fechada. A Tia manda em tudo aqui.", "Town's stuck. Mine's shut. Auntie runs everything here.",
  "Pueblo parado. Mina cerrada. La Tía manda en todo aquí.")
t("DLG_M_ARR_BR_T2", "Ótimo. Mais uma pra eu derrubar.", "Great. One more for me to knock down.", "Genial. Una más para tumbar.")
t("DLG_M_ARR_MI_L1", "Escuro de novo. Mas agora eu sei: escuro é só lugar sem lamparina ainda.",
  "Dark again. But now I know: dark is just a place that doesn't have a lamp yet.", "Oscuro otra vez. Pero ahora lo sé: lo oscuro es solo un lugar sin farol todavía.")
t("DLG_M_ARR_MI_T1", "Ouviu? Martelo. Muito martelo. Tem gente trabalhando sem parar lá dentro.",
  "Hear that? Hammering. Lots of it. Someone's working nonstop in there.", "¿Oyes? Martillos. Muchos. Alguien trabaja sin parar ahí dentro.")
R.d("chegada_brasal", [say("DLG_M_ARR_BR_L1", "SPK_LIA") | {"if": "partner_lia"}, say("DLG_M_ARR_BR_L2", "SPK_LIA") | {"if": "partner_lia"},
                       say("DLG_M_ARR_BR_T1", "SPK_TARO") | {"if": "partner_taro"}, say("DLG_M_ARR_BR_T2", "SPK_TARO") | {"if": "partner_taro"},
                       flag("brasal_visto")])
R.d("chegada_mina", [say("DLG_M_ARR_MI_L1", "SPK_LIA") | {"if": "partner_lia"}, say("DLG_M_ARR_MI_T1", "SPK_TARO") | {"if": "partner_taro"},
                     flag("mina_vista")])
R.D["vigia_entrada"][-1:-1] = [say("DLG_M_ARR_R2_L1", "SPK_LIA") | {"if": "partner_lia"}, say("DLG_M_ARR_R2_L2", "SPK_LIA") | {"if": "partner_lia"},
                               say("DLG_M_ARR_R2_T1", "SPK_TARO") | {"if": "partner_taro"}, say("DLG_M_ARR_R2_T2", "SPK_TARO") | {"if": "partner_taro"}]

t("DLG_M_RUBI_AFTER", "A fumaça baixou! Hoje de manhã vi o céu. Era azul, imagina.", "The smoke went down! This morning I saw the sky. It was blue, can you imagine.",
  "¡Bajó el humo! Esta mañana vi el cielo. Era azul, imagínate.")
t("DLG_M_TURMALINA_AFTER", "Ouvi o sino da cidade tocar de novo. Quem será que lembrou dele?",
  "I heard the town bell ring again. I wonder who remembered it.", "Oí la campana del pueblo sonar otra vez. ¿Quién se habrá acordado de ella?")
t("DLG_M_FAGULHA_AFTER", "Você venceu a Tia? Com faísca ou com soco? Fala que foi com faísca!",
  "You beat Auntie? With sparks or punches? Say it was sparks!", "¿Venciste a la Tía? ¿Con chispa o con puñetazo? ¡Di que fue con chispa!")
R.D["rubi"].insert(2, {"say": "DLG_M_RUBI_AFTER", "speaker": "SPK_RUBI", "if": "fornalha_beaten"})
R.D["turmalina"] = [{"say": "DLG_M_TURMALINA_AFTER", "speaker": "SPK_TURMALINA", "if": "fornalha_beaten"}] + R.D["turmalina"]
R.D["fagulha"] = [{"say": "DLG_M_FAGULHA_AFTER", "speaker": "SPK_FAGULHA", "if": "fornalha_beaten"}] + R.D["fagulha"]

# ------------------------------------------------------------------ missão 2: o aniversário do Gasito da Pirita
t("DLG_M_PIRITA_ASK", "Amanhã é aniversário do meu Gasito, e vela nenhuma acende com tanta cinza.",
  "Tomorrow is my Gasito's birthday, and no candle stays lit with all this ash.",
  "Mañana es el cumpleaños de mi Gasito, y ninguna vela prende con tanta ceniza.")
t("DLG_M_PIRITA_ASK1", "Dizem que na Galeria Velha tem cristal que brilha sozinho...", "They say the Old Gallery has crystals that glow on their own...",
  "Dicen que en la Galería Vieja hay cristales que brillan solos...")
t("DLG_M_PIRITA_ASK2", "Traz um pra mim? Vela que não apaga é a melhor vela.", "Would you bring me one? A candle that never goes out is the best candle.",
  "¿Me traes uno? Una vela que no se apaga es la mejor vela.")
t("DLG_M_PIRITA_WHERE", "Galeria Velha, no meio da Rota 2. O cristal fica perto da saída norte.", "The Old Gallery, in the middle of Route 2. The crystal is near the north exit.",
  "La Galería Vieja, en medio de la Ruta 2. El cristal está cerca de la salida norte.")
t("OBJ_M_CRYSTAL", "Um cristal do tamanho de um polegar, quentinho e brilhando sozinho.", "A thumb-sized crystal, warm and glowing on its own.",
  "Un cristal del tamaño de un pulgar, tibio y brillando solo.")
t("DLG_M_PIRITA_PARTY1", "Achou! Gasito, olha a vela! Parabéns pra você, nessa cinza tão...", "You found it! Gasito, look at the candle! Happy birthday to you, in this ash so...",
  "¡Lo encontraste! ¡Gasito, mira la vela! Cumpleaños feliz, en esta ceniza tan...")
t("DLG_M_PIRITA_PARTY2", "O Gasito sopra o cristal. Não apaga, claro. Ele sopra de novo, mais forte. Todo mundo ri.",
  "Gasito blows on the crystal. It doesn't go out, of course. He blows harder. Everyone laughs.",
  "Gasito sopla el cristal. No se apaga, claro. Sopla otra vez, más fuerte. Todos se ríen.")
t("DLG_M_PIRITA_PARTY3", "Toma, duas Poções M. E um pedaço de bolo... com só um pouquinho de cinza.",
  "Here, two Potions M. And a slice of cake... with just a little bit of ash.", "Toma, dos Pociones M. Y un trozo de pastel... con solo un poquito de ceniza.")
t("ITEM_CRYSTAL", "Cristal-vela", "Candle Crystal", "Cristal Vela")
t("ITEM_CRYSTAL_TEXT", "Brilha sozinho e não apaga com sopro. A Pirita quer para um bolo.", "Glows on its own and won't blow out. Pyrite wants it for a cake.",
  "Brilla solo y no se apaga al soplar. Pirita lo quiere para un pastel.")
R.ITEMS["cristal_vela"] = {"name_key": "ITEM_CRYSTAL", "desc_key": "ITEM_CRYSTAL_TEXT", "kind": "key", "price": 0, "battle": False, "target": "none"}
R.d("pirita_pede", [say("DLG_M_PIRITA_ASK", "SPK_PIRITA"), say("DLG_M_PIRITA_ASK1", "SPK_PIRITA"), say("DLG_M_PIRITA_ASK2", "SPK_PIRITA"), flag("pirita_quest")])
R.d("pirita_onde", [say("DLG_M_PIRITA_WHERE", "SPK_PIRITA")])
R.d("pirita_festa", [say("DLG_M_PIRITA_PARTY1", "SPK_PIRITA"), act("take_item", item="cristal_vela", n=1), {"action": "sfx", "name": "birthday"},
                     say("DLG_M_PIRITA_PARTY2"), say("DLG_M_PIRITA_PARTY3", "SPK_PIRITA"), act("give_item", item="pocao_m", n=2), flag("pirita_done")])
R.d("cristal_vela", [say("OBJ_M_CRYSTAL"), act("give_item", item="cristal_vela", n=1), flag("cristal_pego")])
R.NPCS["pirita"]["dialog"] = [{"if": "pirita_done", "dialog": ref("pirita")}, {"if": "has_cristal_vela", "dialog": ref("pirita_festa")},
                              {"if": "pirita_quest", "dialog": ref("pirita_onde")}, {"dialog": ref("pirita_pede")}]
R.NPCS["pirita"]["role"] = "quest"

# ------------------------------------------------------------------ Caminho Selvagem: dica do Golden
t("SPK_CASCUDO", "Cascudo", "Pebbles", "Pedrusco")
t("DLG_M_CASCUDO_1", "Eu cato cristal aqui. Uma vez vi um esqueleto dourado brilhando mais que todos eles juntos!",
  "I collect crystals here. Once I saw a golden skeleton shining brighter than all of them together!",
  "Aquí recojo cristales. ¡Una vez vi un esqueleto dorado que brillaba más que todos juntos!")
t("DLG_M_CASCUDO_2", "Ele piscava e fazia tlin-tlin. Se ouvir esse som, corre atrás!", "It sparkled and went ting-ting. If you hear that sound, chase it!",
  "Centelleaba y hacía tilín-tilín. ¡Si oyes ese sonido, corre tras él!")
R.d("cascudo", [say("DLG_M_CASCUDO_1", "SPK_CASCUDO"), say("DLG_M_CASCUDO_2", "SPK_CASCUDO")])
R.NPCS["cascudo"] = human("fagulha", "SPK_CASCUDO", [{"dialog": ref("cascudo")}])
R.NPCS["cascudo"]["sprite"] = "res://assets/sprites/npc/cascudo.png"

# ------------------------------------------------------------------ encontros (balance.json: selvagens 21–27)
def e(sp, st, a, b, rar, w=None):
    d = {"species": sp, "stage": st, "min_level": a, "max_level": b, "rarity": rar}
    if w:
        d["weight"] = w
    return d


R.TABLES.update({
    "rota2_sul": [e("mineiro_1", 1, 21, 23, "comum"), e("gasista_1", 1, 21, 23, "comum")],
    "rota2_oeste": [e("lenhador_2", 2, 22, 24, "comum"), e("gasista_1", 1, 22, 23, "comum")],
    "rota2_campo": [e("mineiro_1", 1, 22, 23, "comum"), e("gasista_1", 1, 22, 23, "comum"), e("ferreiro_1", 1, 22, 23, "incomum"),
                    e("aguadeiro_1", 1, 23, 25, "raro"), e("mineiro_2", 2, 24, 25, "comum")],
    "rota2_galeria": [e("aguadeiro_1", 1, 26, 27, "raro", 60), e("gasista_2", 2, 26, 27, "comum", 40)],
    "rota2_norte": [e("ferreiro_2", 2, 24, 26, "incomum"), e("mineiro_2", 2, 24, 26, "comum")],
    "mina_salao": [e("mineiro_2", 2, 25, 27, "comum"), e("ferreiro_2", 2, 25, 27, "incomum"), e("gasista_2", 2, 25, 27, "comum")],
    "mina_sul": [e("aguadeiro_1", 1, 25, 27, "raro"), e("gasista_2", 2, 25, 27, "comum")],
})

R.SHOPS["brasal"] = {"items": ["pocao_p", "pocao_m", "pocao_g", "antidoto", "reviver"],
                     "price_mul": {"minas_quebrou": 1.25, "minas_negociou": 0.9}}

# ------------------------------------------------------------------ mapas
LEG = {"g": "ash", "f": "mud", "B": "rock", "p": "path", ".": "floor"}
rota = make_route("rota_2", "minas", "MAP_ROTA_2", LEG, ("raizal", 19, 1), ("brasal", 19, 30),
                  tamers=[("graxa", {}), ("brita", {}), ("fuligem", {})], hint="seixo", sign=R.ref("placa_bifurcacao"),
                  spawns=[{"id": "r2_sul", "table": "rota2_sul", "x": 10, "y": 45, "radius": 3, "count": 2},
                          {"id": "r2_oeste", "table": "rota2_oeste", "x": 5, "y": 25, "radius": 2, "count": 1},
                          {"id": "r2_campo_a", "table": "rota2_campo", "x": 30, "y": 32, "radius": 4, "count": 3},
                          {"id": "r2_campo_b", "table": "rota2_campo", "x": 30, "y": 18, "radius": 4, "count": 3},
                          {"id": "r2_galeria", "table": "rota2_galeria", "x": 19, "y": 25, "radius": 2, "count": 1},
                          {"id": "r2_norte", "table": "rota2_norte", "x": 10, "y": 6, "radius": 3, "count": 2}],
                  extra_npcs=[{"id": "vigia_lasca", "x": 22, "y": 46, "facing": "left"}, {"id": "cascudo", "x": 28, "y": 25, "facing": "down"}],
                  extra_props=[{"type": "mine_lamp", "x": 18, "y": 36}, {"type": "mine_lamp", "x": 21, "y": 13},
                               {"type": "rails", "x": 33, "y": 44}, {"type": "rails", "x": 34, "y": 44}, {"type": "mine_cart", "x": 34, "y": 46},
                               {"type": "crystal", "x": 27, "y": 24}, {"type": "crystal", "x": 37, "y": 12}],
                  deco=("rock_small", "rock_big", "rock_small"), tint=[0.92, 0.88, 0.86], seed=21)
rota["on_enter"] = [{"if_not": "vigia_lasca_ok", "dialog": R.ref("vigia_entrada")}]
rota["ambient"] = ["ash"]
rota["props"].append({"type": "crystal", "x": 21, "y": 16, "dialog": R.ref("cristal_vela"), "if": "pirita_quest", "if_not": "cristal_pego"})

town = make_town("brasal", "minas", "MAP_BRASAL", dict(LEG, s="stone"),
                 south=("rota_2", 19, 1), north=("rota_3", 19, 48), west=("mina_funda", 32, 10),
                 houses=["house_stone_ranch", "house_stone_shop", "house_stone", "house_stone", "house_stone"],
                 npcs=[{"id": "pirita", "x": 16, "y": 16, "facing": "right"}, {"id": "fagulha", "x": 23, "y": 14, "facing": "down"},
                       {"id": "turmalina", "x": 25, "y": 18, "facing": "left"},
                       {"id": "guarda_estrada", "x": 21, "y": 2, "facing": "left", "if_not": "fornalha_beaten"}],
                 props=[{"type": "sign", "x": 18, "y": 28, "dialog": R.ref("placa_brasal")}, {"type": "sign", "x": 3, "y": 14, "dialog": R.ref("placa_mina")},
                        {"type": "anvil", "x": 22, "y": 16}, {"type": "mine_lamp", "x": 13, "y": 13}, {"type": "mine_lamp", "x": 26, "y": 13},
                        {"type": "rails", "x": 5, "y": 15}, {"type": "rails", "x": 6, "y": 15}, {"type": "mine_cart", "x": 7, "y": 13},
                        {"type": "chain_gate", "x": 20, "y": 1, "if_not": "fornalha_beaten"}],
                 deco=("rock_small", "rock_big", "crystal"), north_guard=None, tint=[0.9, 0.84, 0.82], seed=31, plaza="s")
for w in town["warps"]:
    if w["to"] == "rota_3":
        w["if"] = "fornalha_beaten"
        w["locked_message"] = "MSG_FORNALHA_ROAD"
town["ambient"] = ["ash"]
town["on_enter"] = [{"if_not": "brasal_visto", "dialog": R.ref("chegada_brasal")}]
town_doors(town, "brasal", {"rancho": "brasal_rancho", "loja": "brasal_loja", "a": "brasal_casa_bigorna", "b": "brasal_casa_agata", "c": "brasal_casa_carvao"})

lair = make_lair("mina_funda", "minas", "MAP_MINA_FUNDA", dict(LEG, f="stone"), east=("brasal", 1, 15),
                 guardian_npc={"id": "fornalha", "x": 10, "y": 3, "facing": "down"},
                 extra_npcs=[{"id": "bloqueio", "x": 14, "y": 10, "facing": "right"},
                             {"id": "mineiro_forja", "x": 4, "y": 2, "facing": "right", "if_not": "minas_quebrou"},
                             {"id": "taro_mina", "x": 6, "y": 17, "facing": "right", "if": "partner_lia", "if_not": "lenco_visto"},
                             {"id": "vagonauta_npc", "x": 11, "y": 14, "facing": "left", "if": "minas_quebrou"}],
                 props=[{"type": "forge", "x": 10, "y": 1}, {"type": "anvil", "x": 7, "y": 3}, {"type": "anvil", "x": 13, "y": 3},
                        {"type": "chain_gate", "x": 15, "y": 5, "if_not": "minas_quebrou"},
                        {"type": "mine_lamp", "x": 18, "y": 7}, {"type": "mine_lamp", "x": 27, "y": 8}, {"type": "crystal", "x": 22, "y": 13},
                        {"type": "crystal", "x": 4, "y": 19}, {"type": "beam_frame", "x": 24, "y": 9},
                        {"type": "rails", "x": 8, "y": 13}, {"type": "rails", "x": 8, "y": 14}, {"type": "rails", "x": 8, "y": 15},
                        {"type": "mine_cart", "x": 10, "y": 18},
                        {"type": "scarf", "x": 5, "y": 15, "dialog": R.ref("lenco_parceiro"), "if": "partner_taro", "if_not": "lenco_visto"}],
                 spawns=[{"id": "mina_salao", "table": "mina_salao", "x": 23, "y": 11, "radius": 3, "count": 2},
                         {"id": "mina_sul", "table": "mina_sul", "x": 6, "y": 14, "radius": 2, "count": 1}],
                 tint=[0.62, 0.56, 0.62])
lair["ambient"] = ["ash"]
lair["on_enter"] = [{"if_not": "mina_vista", "dialog": R.ref("chegada_mina")}]
# capacete: só enquanto a missão está aberta e ninguém o pegou
lair["props"].append({"type": "helmet_lamp", "x": 12, "y": 17, "dialog": R.ref("capacete"), "if": "carvao_quest", "if_not": "carvao_helmet_taken"})
R.D["capacete"].append(flag("carvao_helmet_taken"))

R.MAPS.update({
    "rota_2": rota, "brasal": town, "mina_funda": lair,
    "brasal_rancho": room("brasal_rancho", "minas", "MAP_BRASAL_RANCHO", "brasal", (12, 10),
                          [{"type": "bed", "x": 2, "y": 3}, {"type": "bed", "x": 4, "y": 3}, {"type": "lamp", "x": 10, "y": 2},
                           {"type": "rug", "x": 6, "y": 6}], [{"id": "rubi", "x": 7, "y": 3, "facing": "down"}]),
    "brasal_loja": room("brasal_loja", "minas", "MAP_BRASAL_LOJA", "brasal", (27, 10),
                        [{"type": "shelf", "x": 3, "y": 2}, {"type": "shelf", "x": 10, "y": 2}, {"type": "table", "x": 7, "y": 4},
                         {"type": "crate", "x": 10, "y": 7}, {"type": "crystal", "x": 1, "y": 7}], [{"id": "cobre", "x": 6, "y": 3, "facing": "down"}]),
    "brasal_casa_bigorna": room("brasal_casa_bigorna", "minas", "MAP_BRASAL_CASA_BIGORNA", "brasal", (8, 20),
                                [{"type": "anvil", "x": 3, "y": 4}, {"type": "anvil", "x": 9, "y": 4}, {"type": "barrel", "x": 10, "y": 7}],
                                [{"id": "bigorna", "x": 6, "y": 3, "facing": "down"}]),
    "brasal_casa_agata": room("brasal_casa_agata", "minas", "MAP_BRASAL_CASA_AGATA", "brasal", (31, 20),
                              [{"type": "table", "x": 7, "y": 4}, {"type": "crystal", "x": 2, "y": 3}, {"type": "barrel", "x": 10, "y": 7}],
                              [{"id": "agata", "x": 5, "y": 3, "facing": "down"}]),
    "brasal_casa_carvao": room("brasal_casa_carvao", "minas", "MAP_BRASAL_CASA_CARVAO", "brasal", (14, 27),
                               [{"type": "map_board", "x": 9, "y": 2, "dialog": R.ref("mapa_antigo")}, {"type": "table", "x": 4, "y": 5},
                                {"type": "stool", "x": 3, "y": 6}, {"type": "lamp", "x": 1, "y": 7}],
                               [{"id": "carvao", "x": 6, "y": 3, "facing": "down"}]),
})
R.BATTLE_BG["minas"] = "res://assets/battle/bg_minas.png"

R.CITIES.append({"id": "brasal", "map": "brasal", "ranch": "rubi", "shop": "brasal",
                 "tamer_houses": ["bigorna", "agata"], "npcs": ["pirita", "fagulha", "turmalina", "carvao"], "quests": ["carvao", "pirita"]})
R.ROUTES.append({"id": "rota_2", "map": "rota_2", "from": "raizal", "to": "brasal",
                 "paths": [{"kind": "domadores", "required": False}, {"kind": "selvagem", "required": False},
                           {"kind": "atalho", "required": False, "note": "Galeria Velha: curta, com um selvagem forte"}]})

# ------------------------------------------------------------------ documento
R.DOC = {
    "title": "Ato 2: Rota 2 e Minas de Cinzas", "phase": "4c", "duration": "25 min",
    "ages": "chegada 22–30; selvagens 21–27; domadores 24–31; Guardiã ~34",
    "problem": "**Brasal** vivia das minas. A Guardiã **Tia Fornalha** prendeu os esqueletos mineiros à forja com a **corrente mestra**: "
               "eles martelam dia e noite as correntes que fecham as estradas do continente (\"Ninguém sai, ninguém se perde\"). "
               "Os mineiros humanos foram expulsos, não há minério, e a fumaça cobre a cidade de cinza. A estrada do norte, para o Pântano, "
               "está fechada por correntes até a Tia perder.",
    "clue_n": 3,
    "clue": "Na casa do **Seu Carvão** há um **mapa antigo** da costa: três baías lado a lado e um farol na do meio. "
            "O protagonista reconhece as baías da própria cidade em 2040, com outros nomes. (Mesmo lugar, mil anos antes.)",
    "moment": ["**Taro** acha o **lenço da mãe** preso numa viga da Mina Funda (câmara sul). Parceiro: ele segura o choro e pede para irem mais rápido. "
               "Recorrente (parceira Lia): Taro já está lá, conta que os levados passaram pela mina rumo ao norte; Lia promete ajudar a procurar.",
               "Arco de Taro: raiva → primeiro sinal de esperança (\"ela tá inteira\")."],
    "guardian": {"name": "Tia Fornalha (tia do Rei)", "kin": "tia; cuidou do Rei quando ele era menino",
                 "personality": "severa, justa, sem paciência; fala em \"regras\" numeradas (o tique dela)",
                 "motive": "**Dever**: acredita que a ordem do Rei mantém todos seguros. Enquanto houver corrente, a família não vai embora.",
                 "mechanic": "**Defesa.** A equipe sobe DEF (Picaréu, Bigornel) e aguenta muito. Ensina a baixar atributos e a usar golpes "
                             "**Mágicos** (contra RES) em quem tem DEF alta. Fagulha e o Mestre Bigorna dão a dica antes.",
                 "team": "Picaréu 34, Bigornel 33, Fumarel 35, Bilheiro 34 (os capangas usam Picaréu/Bigornel em versão menor).",
                 "reward": "1000 moedas; a estrada do norte abre; e a **escolha 2**."},
    "maps": [("**Rota 2** (`rota_2`)", "Sai de Raizal (exige a vitória sobre Ramalho; o Vigia confere a Lasca de Raiz). 3 caminhos: **Domadores** (oeste: Graxa, Brita, Fuligem), "
              "**Selvagem** (leste, Campo de Cascalho com lama e mais esqueletos) e **Atalho** (Galeria Velha, central, curta, com um selvagem forte). Placa e Seu Seixo dão a dica."),
             ("**Brasal** (`brasal`)", "Cidade mineira: Rancho, Loja (Poção G; preço muda com a escolha 2), 2 casas de domadores, a casa do Carvão (missão + pista), NPCs, "
              "saída oeste para a Mina Funda e saída norte acorrentada."),
             ("**Mina Funda** (`mina_funda`)", "Salão com selvagens, Capataz Bloqueio, câmara sul (lenço de Taro, capacete da missão, Vagonauta se a corrente for quebrada) e a forja da Tia ao norte."),
             ("Interiores", "Rancho da Rubi, Armazém do Cobre, Oficina do Bigorna, Casa da Ágata, Casa do Carvão.")],
}
R.NPC_DOC = [
    ("Vigia da Trilha", "dica/porteiro", "Liga o Bosque às Minas: confere a Lasca de Raiz"),
    ("Seu Seixo", "dica", "Explica os 3 caminhos e avisa do selvagem forte da Galeria"),
    ("Graxa, Brita, Fuligem", "domadores da rota", "Caminho dos Domadores; Fuligem avisa do gás da mina"),
    ("Dona Rubi", "Rancho", "Cura; mostra a cidade esvaziada pela Tia"),
    ("Seu Cobre", "Loja", "Loja com Poção G; reage à escolha 2 (preço e fala)"),
    ("Pirita", "humor + missão", "Bolo com gosto de cinza; pede o Cristal-vela para o aniversário do Gasito"),
    ("Cascudo", "dica", "No Caminho Selvagem: ensina a reconhecer o som do Golden"),
    ("Fagulha", "dica", "Ensina a mecânica da Guardiã: Mágico contra DEF alta"),
    ("Vó Turmalina", "lore", "A Tia cuidou do Rei menino; planta o motivo dela"),
    ("Seu Carvão", "missão + pista", "Missão do capacete; dono do mapa antigo (pista 3)"),
    ("Capataz Bloqueio", "domador/capanga", "Guarda a forja; também vigia a estrada norte"),
    ("Tia Fornalha", "Guardiã", "Mecânica de Defesa e a escolha 2"),
]
R.HOUSES = [
    ("Mestre Bigorna (Oficina)", "Defesa: Bigornel e Picaréu sobem a guarda", "620 moedas + 2 Poções M"),
    ("Ágata", "Veneno de gás e cura (Fumarel + Cantilho)", "560 moedas + 3 Antídotos + 1 Reviver"),
]
R.CHOICES = [
    ("Caminho da Rota 2", "Domadores / Cascalho / Galeria Velha", "Moedas e itens / XP e marcadores / curto, com um selvagem forte"),
    ("**Escolha 2: a corrente mestra**", "Quebrar / Pedir que ela solte",
     "Quebrar: os mineiros fogem, a loja fica 25% mais cara e o único **Vagonauta** aparece na câmara sul (recrutável). "
     "Pedir: a Tia dá o **Martelo da Tia** (abre o atalho de entulho da Rota 3), a loja dá 10% de desconto e soma **+1 Redenção** (`red_minas`)."),
    ("Missão do capacete", "Fazer / ignorar", "2 Poções G"),
    ("Missão do bolo da Pirita", "Fazer / ignorar", "2 Poções M e uma festa de aniversário"),
]

if __name__ == "__main__":
    R.write()
    # Raizal: a estrada norte agora leva à Rota 2 (só depois do Ramalho)
    p = ROOT / "data/maps/raizal.json"
    m = json.loads(p.read_text())
    for w in m["warps"]:
        if w["to"] == "rota_2":
            w.update({"tx": w["x"], "ty": 48, "if": "ramalho_beaten", "locked_message": "MSG_CLEARING_ROAD"})
    p.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
