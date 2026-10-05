#!/usr/bin/env python3
"""Ato 4 — Rota 4 e Cidade Murada de Ossório (fase 4e): a revelação de 2040.
Fonte única: gera docs/roteiro/05_ossorio.md, falas (PT/EN/ES), NPCs,
encontros, loja, itens e mapas (Rota 4, Ossório e interiores, Quartel)."""
from regionkit import (Region, make_lair, make_route, make_town, room, town_doors, team,
                       say, ask, battle, act, flag, goto, human, skel)

R = Region("ossorio", 5, "ossorio", ["ossorio"])
t = R.t
ref = R.ref


def lia(k):
    return say(k, "SPK_LIA") | {"if": "partner_lia"}


def taro(k):
    return say(k, "SPK_TARO") | {"if": "partner_taro"}


# ------------------------------------------------------------------ nomes
for k, pt, en, es in [
        ("TROTE", "Mensageiro Trote", "Courier Trot", "Mensajero Trote"), ("ELMO", "Cadete Elmo", "Cadet Helm", "Cadete Yelmo"),
        ("MALVA", "Escudeira Malva", "Squire Mallow", "Escudera Malva"), ("BIGODE", "Recruta Bigode", "Recruit Whiskers", "Recluta Bigotes"),
        ("AMEIA", "Dona Ameia", "Mrs. Merlon", "Doña Almena"), ("DOBRAO", "Mercador Dobrão", "Merchant Doubloon", "Mercader Doblón"),
        ("VISEIRA", "Capitã Viseira", "Captain Visor", "Capitana Visera"), ("ELO", "Gêmeos Elo", "Link Twins", "Gemelos Eslabón"),
        ("CLARIM", "Pregoeiro Clarim", "Crier Bugle", "Pregonero Clarín"), ("FIVELA", "Fivela", "Buckle", "Hebilla"),
        ("SELO", "Arquivista Selo", "Archivist Seal", "Archivero Sello"), ("BRASAO", "Velho Brasão", "Old Crest", "Viejo Blasón"),
        ("GRADE", "Sargento Grade", "Sergeant Bars", "Sargento Reja"), ("CALICO", "Comandante Caliço", "Commander Caliço", "Comandante Caliço")]:
    t(f"SPK_{k}", pt, en, es)
for k in ("ELMO", "MALVA", "BIGODE", "VISEIRA", "ELO", "GRADE"):
    pt, en, es = R.T[f"SPK_{k}"]
    t(f"BTL_TAMER_{k}", pt, en, es)
t("BTL_TAMER_CALICO", "Guardião Caliço", "Guardian Caliço", "Guardián Caliço")
t("MAP_ROTA_4", "Rota 4 — Estrada dos Estandartes", "Route 4 — Banner Road", "Ruta 4 — Camino de los Estandartes")
t("MAP_OSSORIO", "Ossório, a Cidade Murada", "Ossório, the Walled City", "Ossório, la Ciudad Amurallada")
t("MAP_QUARTEL", "Quartel de Ossório", "Ossório Barracks", "Cuartel de Ossório")
t("MAP_OSSORIO_RANCHO", "Rancho da Ameia", "Merlon's Ranch", "Rancho de Almena")
t("MAP_OSSORIO_LOJA", "Empório do Dobrão", "Doubloon's Emporium", "Emporio de Doblón")
t("MAP_OSSORIO_CASA_VISEIRA", "Casa da Capitã Viseira", "Captain Visor's House", "Casa de la Capitana Visera")
t("MAP_OSSORIO_CASA_ELO", "Casa dos Gêmeos Elo", "Link Twins' House", "Casa de los Gemelos Eslabón")
t("MAP_ARQUIVO", "Arquivo Real", "Royal Archive", "Archivo Real")
t("MSG_CALICO_ROAD", "Guardas em formação fecham o portão norte. Ordem do Comandante Caliço.",
  "Guards in formation block the north gate. Commander Caliço's orders.", "Guardias en formación cierran la puerta norte. Orden del Comandante Caliço.")
t("MSG_ARCHIVE_SEALED", "O Arquivo Real está lacrado com o selo do Rei.", "The Royal Archive is sealed with the King's seal.",
  "El Archivo Real está sellado con el sello del Rey.")
t("ITEM_RECORD", "Registro Real", "Royal Record", "Registro Real")
t("ITEM_RECORD_TEXT", "\"Quando a coroa rachar, o eco chamará o último do sangue, onde o farol virar museu.\"",
  "\"When the crown cracks, the echo will call the last of the blood, where the lighthouse becomes a museum.\"",
  "\"Cuando la corona se agriete, el eco llamará al último de la sangre, donde el faro se vuelva museo.\"")
R.ITEMS["registro_real"] = {"name_key": "ITEM_RECORD", "desc_key": "ITEM_RECORD_TEXT", "kind": "key", "price": 0, "battle": False, "target": "none"}
t("OPT_O_TELL", "Contar à cidade", "Tell the city", "Contarlo a la ciudad")
t("OPT_O_SECRET", "Guardar segredo", "Keep it secret", "Guardar el secreto")
t("OPT_O_DUNA", "A Rainha Duna", "Queen Duna", "La Reina Duna")
t("OPT_O_KING", "O próprio Rei", "The King himself", "El propio Rey")
t("OPT_O_AUNT", "A Tia Fornalha", "Aunt Furnace", "La Tía Fragua")
t("OPT_O_TRUMPET", "Ouvir o toque", "Listen to the call", "Escuchar el toque")

# ------------------------------------------------------------------ Rota 4
t("SIGN_O_FORK", "← Caminho dos Cadetes · ↑ Aqueduto Velho · → Campo das Bandeiras",
  "← Cadets' Path · ↑ Old Aqueduct · → Banner Field", "← Camino de los Cadetes · ↑ Acueducto Viejo · → Campo de Banderas")
t("DLG_O_ARR_R_L", "Bandeiras azuis em todo canto! Alguém muito importante morava aqui.", "Blue banners everywhere! Someone very important lived here.",
  "¡Banderas azules por todas partes! Aquí vivía alguien muy importante.")
t("DLG_O_ARR_R_T", "Estrada de pedra, gasta no meio. Muita gente marchou por aqui.", "A stone road, worn down the middle. Lots of people marched here.",
  "Camino de piedra, gastado en el medio. Mucha gente marchó por aquí.")
t("DLG_O_TROTE_1", "Três caminhos pra Ossório: o dos cadetes, o do campo e o aqueduto. No aqueduto mora coisa velha.",
  "Three paths to Ossório: the cadets', the field, and the aqueduct. Something old lives in the aqueduct.",
  "Tres caminos a Ossório: el de los cadetes, el del campo y el acueducto. En el acueducto vive algo viejo.")
t("DLG_O_TROTE_2", "Eu levo recado pro quartel. Ninguém responde. Só carimbam e devolvem.", "I carry messages to the barracks. Nobody answers. They just stamp them and send them back.",
  "Llevo recados al cuartel. Nadie responde. Solo los sellan y los devuelven.")
t("DLG_O_ELMO_1", "Cadete Elmo, em serviço! Identificação ou batalha!", "Cadet Helm, on duty! Identification or battle!", "¡Cadete Yelmo, de servicio! ¡Identificación o batalla!")
t("DLG_O_ELMO_2", "Identificação aceita... por derrota.", "Identification accepted... by defeat.", "Identificación aceptada... por derrota.")
t("DLG_O_MALVA_1", "Escudo pra cima, esqueleto pra frente. É assim que se marcha em Ossório!", "Shield up, skeleton forward. That's how we march in Ossório!",
  "Escudo arriba, esqueleto al frente. ¡Así se marcha en Ossório!")
t("DLG_O_MALVA_2", "Marchei pra trás. Acontece com as melhores.", "I marched backward. It happens to the best of us.", "Marché hacia atrás. Le pasa a las mejores.")
t("DLG_O_BIGODE_1", "Três semanas de guarda e nenhuma aventura. Você é minha aventura!", "Three weeks on guard and not a single adventure. You're my adventure!",
  "Tres semanas de guardia y ninguna aventura. ¡Tú eres mi aventura!")
t("DLG_O_BIGODE_2", "Melhor aventura da semana. Única, mas a melhor.", "Best adventure of the week. The only one, but the best.",
  "La mejor aventura de la semana. La única, pero la mejor.")
t("DLG_O_RIV_T", "Ossório tem soldado em cada esquina. Vou passar por todos. Começando por você.",
  "Ossório has a soldier on every corner. I'll get past all of them. Starting with you.", "Ossório tiene un soldado en cada esquina. Pasaré por todos. Empezando por ti.")
t("DLG_O_RIV_L", "Ossório tem um arquivo com todos os livros do reino! Mas antes, uma batalha. Pra dar coragem!",
  "Ossório has an archive with every book in the kingdom! But first, a battle. For courage!",
  "¡Ossório tiene un archivo con todos los libros del reino! Pero antes, una batalla. ¡Para darme valor!")
t("DLG_O_RIV_T_BYE", "...Vai na frente. Só hoje.", "...You go first. Just today.", "...Ve tú delante. Solo hoy.")
t("DLG_O_RIV_L_BYE", "Te vejo no arquivo! Quer dizer... se um dia abrirem.", "See you at the archive! I mean... if they ever open it.",
  "¡Nos vemos en el archivo! Bueno... si algún día lo abren.")

R.d("placa_bifurcacao", [say("SIGN_O_FORK")])
R.d("chegada_rota", [lia("DLG_O_ARR_R_L"), taro("DLG_O_ARR_R_T"), flag("rota4_vista")])
R.d("trote", [say("DLG_O_TROTE_1", "SPK_TROTE"), say("DLG_O_TROTE_2", "SPK_TROTE")])
R.d("elmo", [say("DLG_O_ELMO_1", "SPK_ELMO"), battle("BTL_TAMER_ELMO", team([("sentinela", 48), ("escriba", 48)]), 640, "elmo_beaten"),
             say("DLG_O_ELMO_2", "SPK_ELMO")])
R.d("elmo_depois", [say("DLG_O_ELMO_2", "SPK_ELMO")])
R.d("malva", [say("DLG_O_MALVA_1", "SPK_MALVA"), battle("BTL_TAMER_MALVA", team([("sentinela", 49), ("sineiro", 49)]), 660, "malva_beaten"),
              say("DLG_O_MALVA_2", "SPK_MALVA")])
R.d("malva_depois", [say("DLG_O_MALVA_2", "SPK_MALVA")])
R.d("bigode", [say("DLG_O_BIGODE_1", "SPK_BIGODE"),
               battle("BTL_TAMER_BIGODE", team([("ferreiro", 50), ("sentinela", 50)]), 700, "bigode_beaten", [["pocao_g", 1]]),
               say("DLG_O_BIGODE_2", "SPK_BIGODE")])
R.d("bigode_depois", [say("DLG_O_BIGODE_2", "SPK_BIGODE")])
R.d("rival_taro", [ask("DLG_O_RIV_T", "SPK_TARO", [("OPT_P_FIGHT", ref("rival_taro_luta")), ("OPT_P_NOT_NOW", None)])])
R.d("rival_taro_luta", [battle("BTL_TAMER_TARO", team([("grumete", 52), ("sentinela", 51)]), 700, "rival_ossorio_done", marker={"species": "grumete_3", "amount": 10}),
                        say("DLG_O_RIV_T_BYE", "SPK_TARO"), act("hide_npc", id="rival_taro_o")])
R.d("rival_lia", [ask("DLG_O_RIV_L", "SPK_LIA", [("OPT_P_FIGHT", ref("rival_lia_luta")), ("OPT_P_NOT_NOW", None)])])
R.d("rival_lia_luta", [battle("BTL_TAMER_LIA", team([("faroleira", 52), ("marisqueiro", 51)]), 700, "rival_ossorio_done", marker={"species": "faroleira_3", "amount": 10}),
                       say("DLG_O_RIV_L_BYE", "SPK_LIA"), act("hide_npc", id="rival_lia_o")])
R.NPCS["trote"] = human("trote", "SPK_TROTE", [{"dialog": ref("trote")}])
R.tamer("elmo", "elmo", "SPK_ELMO", "elmo", "elmo_beaten")
R.tamer("malva", "malva", "SPK_MALVA", "malva", "malva_beaten")
R.tamer("bigode", "bigode", "SPK_BIGODE", "bigode", "bigode_beaten", 3)
R.NPCS["rival_taro_o"] = skel("skel_grumete_3", "SPK_TARO", [{"dialog": ref("rival_taro")}])
R.NPCS["rival_lia_o"] = skel("skel_faroleira_3", "SPK_LIA", [{"dialog": ref("rival_lia")}])

# ------------------------------------------------------------------ Ossório
t("SIGN_O_CITY", "Ossório. Antiga capital do reino. Toque de recolher ao pôr do sol.", "Ossório. Old capital of the kingdom. Curfew at sunset.",
  "Ossório. Antigua capital del reino. Toque de queda al atardecer.")
t("SIGN_O_BARRACKS", "← Quartel. Proibida a entrada de civis.", "← Barracks. No civilians allowed.", "← Cuartel. Prohibida la entrada de civiles.")
t("OBJ_O_STATUE", "Estátua do príncipe Ossárion, ainda menino. O tempo apagou o rosto.", "A statue of Prince Ossárion as a boy. Time has worn away the face.",
  "Estatua del príncipe Ossárion, todavía niño. El tiempo le borró la cara.")
t("DLG_O_ARR_C_L", "Uma cidade inteira de muralha. Eles têm medo de quê?", "A whole city made of walls. What are they so afraid of?",
  "Una ciudad entera de murallas. ¿De qué tienen tanto miedo?")
t("DLG_O_ARR_C_T", "Soldado na muralha, soldado no portão. Eles esperam uma guerra.", "Soldiers on the wall, soldiers at the gate. They're expecting a war.",
  "Soldados en la muralla, soldados en la puerta. Esperan una guerra.")
t("DLG_O_AMEIA_1", "Toque de recolher ao pôr do sol. Até os esqueletos do Rancho dormem em formação.",
  "Curfew at sunset. Even the Ranch skeletons sleep in formation.", "Toque de queda al atardecer. Hasta los esqueletos del Rancho duermen en formación.")
t("DLG_O_AMEIA_AFTER", "Sem toque de recolher! Hoje o Rancho fica aberto até tarde.", "No more curfew! Tonight the Ranch stays open late.",
  "¡Sin toque de queda! Hoy el Rancho abre hasta tarde.")
t("DLG_O_AMEIA_2", "Quer deixar alguém descansando? Aqui ninguém dorme fora de hora... mas eu deixo.",
  "Want to leave someone here to rest? Nobody sleeps off-schedule here... but I'll allow it.",
  "¿Quieres dejar a alguien descansando? Aquí nadie duerme fuera de hora... pero lo permito.")
t("DLG_O_DOBRAO_1", "Comércio só com autorização do quartel. Eu tenho autorização. Custou caro.",
  "Trading requires a barracks permit. I have one. It cost a fortune.", "Comerciar requiere permiso del cuartel. Yo tengo uno. Me costó caro.")
t("DLG_O_DOBRAO_2", "Volte quando quiser. Em fila, de preferência.", "Come back anytime. In line, preferably.", "Vuelve cuando quieras. En fila, de preferencia.")
t("DLG_O_FIVELA", "Meu pai monta guarda na muralha faz três semanas. Esperando inimigo. O único inimigo é o tédio.",
  "My dad's been guarding the wall for three weeks. Waiting for an enemy. The only enemy is boredom.",
  "Mi papá vigila la muralla desde hace tres semanas. Esperando al enemigo. El único enemigo es el aburrimiento.")
t("DLG_O_FIVELA_AFTER", "Meu pai voltou da muralha! Ele disse que o inimigo era a gente mesmo. Não entendi.",
  "My dad came back from the wall! He said the enemy was us all along. I didn't get it.", "¡Mi papá volvió de la muralla! Dijo que el enemigo éramos nosotros. No entendí.")
t("DLG_O_BRASAO_1", "Varri este pátio no tempo do reino. O príncipe era um menino tristinho, sempre olhando o mar.",
  "I swept this courtyard back in the kingdom days. The prince was a sad little boy, always looking at the sea.",
  "Barría este patio en tiempos del reino. El príncipe era un niño tristón, siempre mirando el mar.")
t("DLG_O_BRASAO_2", "Dizem que ele virou o Rei. Eu digo que ele nunca parou de olhar o mar.", "They say he became the King. I say he never stopped looking at the sea.",
  "Dicen que se volvió el Rey. Yo digo que nunca dejó de mirar el mar.")
t("DLG_O_SELO_1", "O Arquivo guarda mil anos de história. O Rei mandou lacrar tudo. Ninguém lê o passado.",
  "The Archive holds a thousand years of history. The King had it all sealed. Nobody reads the past.",
  "El Archivo guarda mil años de historia. El Rey mandó sellarlo todo. Nadie lee el pasado.")
t("DLG_O_SELO_OPEN", "O Comandante abriu o Arquivo! Leia com cuidado. Livro velho morde.", "The Commander opened the Archive! Read carefully. Old books bite.",
  "¡El Comandante abrió el Archivo! Lee con cuidado. Los libros viejos muerden.")
t("DLG_O_SELO_QUIZ", "Leu o diário da estante? Então me diga: quem ergueu o farol da praia?",
  "Did you read the diary on the shelf? Then tell me: who built the beach lighthouse?", "¿Leíste el diario del estante? Entonces dime: ¿quién levantó el faro de la playa?")
t("DLG_O_SELO_RIGHT", "Exato! A Rainha Duna. Quem lê, merece. Tome, para a viagem.", "Exactly! Queen Duna. Those who read deserve a reward. Here, for the road.",
  "¡Exacto! La Reina Duna. Quien lee, merece. Toma, para el viaje.")
t("DLG_O_SELO_WRONG_KING", "Errado. O Rei só olhava o mar. Quem construiu foi outra pessoa. Volte a ler.",
  "Wrong. The King only gazed at the sea. Someone else built it. Read again.", "Error. El Rey solo miraba el mar. Lo construyó otra persona. Vuelve a leer.")
t("DLG_O_SELO_WRONG_AUNT", "A Fornalha forja sinos, não faróis. Volte a ler, jovem.", "Furnace forges bells, not lighthouses. Read again, young one.",
  "La Fragua forja campanas, no faros. Vuelve a leer, joven.")
t("DLG_O_SELO_AFTER", "Mil anos de livros, e ninguém lia. Agora tem fila. Fila de leitor!", "A thousand years of books, and nobody read them. Now there's a line. A line of readers!",
  "Mil años de libros y nadie los leía. Ahora hay fila. ¡Fila de lectores!")
t("DLG_O_CLARIM_1", "Ouçam, ouçam! Toque de recolher ao pôr do sol, por ordem do Comandante Caliço!",
  "Hear ye, hear ye! Curfew at sunset, by order of Commander Caliço!", "¡Oíd, oíd! ¡Toque de queda al atardecer, por orden del Comandante Caliço!")
t("DLG_O_CLARIM_2", "Desculpa, é força do hábito. Eu grito até pra pedir pão.", "Sorry, force of habit. I even shout when I ask for bread.",
  "Perdón, es la costumbre. Grito hasta para pedir pan.")
t("DLG_O_CLARIM_ASK", "Esse papel tem o selo real! Quer que eu leia na praça? A cidade inteira vai ouvir.",
  "That paper has the royal seal! Want me to read it in the square? The whole city will hear.", "¡Ese papel tiene el sello real! ¿Quieres que lo lea en la plaza? Toda la ciudad lo oirá.")
t("DLG_O_TELL_1", "Ouçam, ouçam! \"Quando a coroa rachar, o eco chamará o último do sangue...\"", "Hear ye, hear ye! \"When the crown cracks, the echo will call the last of the blood...\"",
  "¡Oíd, oíd! \"Cuando la corona se agriete, el eco llamará al último de la sangre...\"")
t("DLG_O_TELL_2", "A praça cochicha, depois grita. No alto da muralha, guardas tiram o elmo e descem.",
  "The square whispers, then shouts. Up on the wall, guards take off their helmets and come down.", "La plaza murmura, luego grita. En lo alto de la muralla, los guardias se quitan el yelmo y bajan.")
t("DLG_O_TELL_3", "Agora todo mundo sabe que o Rei procura um herdeiro. Alguns vão ficar do seu lado. Outros, do lado dele.",
  "Now everyone knows the King is looking for an heir. Some will side with you. Others, with him.",
  "Ahora todos saben que el Rey busca un heredero. Algunos estarán de tu lado. Otros, del suyo.")
t("DLG_O_SECRET", "Segredo de Estado. Meu clarim fica mudo. Pela primeira vez na vida.", "A state secret. My bugle stays silent. For the first time in my life.",
  "Secreto de Estado. Mi clarín se queda mudo. Por primera vez en mi vida.")
t("DLG_O_CLARIM_TOLD", "A cidade inteira sabe. E ninguém foi pra casa dormir!", "The whole city knows. And nobody went home to sleep!",
  "Toda la ciudad lo sabe. ¡Y nadie se fue a dormir!")
t("DLG_O_CLARIM_KEPT", "Meu clarim continua mudo. Combinamos, né?", "My bugle is still silent. That was the deal, right?", "Mi clarín sigue mudo. Ese fue el trato, ¿no?")
R.d("placa_cidade", [say("SIGN_O_CITY")])
R.d("placa_quartel", [say("SIGN_O_BARRACKS")])
R.d("estatua", [say("OBJ_O_STATUE")])
R.d("chegada_cidade", [lia("DLG_O_ARR_C_L"), taro("DLG_O_ARR_C_T"), flag("ossorio_visto")])
R.d("ameia", [act("heal"), act("respawn"), {"say": "DLG_O_AMEIA_AFTER", "speaker": "SPK_AMEIA", "if": "calico_beaten"},
              {"say": "DLG_O_AMEIA_1", "speaker": "SPK_AMEIA", "if_not": "calico_beaten"},
              ask("DLG_O_AMEIA_2", "SPK_AMEIA", [("OPT_P_RANCH", "vila_mare/rancho"), ("OPT_P_LEAVE", None)])])
R.d("dobrao", [say("DLG_O_DOBRAO_1", "SPK_DOBRAO"), act("shop", id="ossorio"), say("DLG_O_DOBRAO_2", "SPK_DOBRAO")])
R.d("fivela", [{"say": "DLG_O_FIVELA_AFTER", "speaker": "SPK_FIVELA", "if": "calico_beaten"},
               {"say": "DLG_O_FIVELA", "speaker": "SPK_FIVELA", "if_not": "calico_beaten"}])
R.d("brasao", [say("DLG_O_BRASAO_1", "SPK_BRASAO"), say("DLG_O_BRASAO_2", "SPK_BRASAO")])
R.d("clarim", [{"say": "DLG_O_CLARIM_TOLD", "speaker": "SPK_CLARIM", "if": "ossorio_revelou"},
               {"say": "DLG_O_CLARIM_KEPT", "speaker": "SPK_CLARIM", "if": "ossorio_segredo"},
               ask("DLG_O_CLARIM_ASK", "SPK_CLARIM", [("OPT_O_TELL", ref("contar")), ("OPT_O_SECRET", ref("segredo"))])
               | {"if": "has_registro_real", "if_none": ["ossorio_revelou", "ossorio_segredo"]},
               {"say": "DLG_O_CLARIM_1", "speaker": "SPK_CLARIM", "if_none": ["has_registro_real", "ossorio_revelou", "ossorio_segredo"]},
               {"say": "DLG_O_CLARIM_2", "speaker": "SPK_CLARIM", "if_none": ["has_registro_real", "ossorio_revelou", "ossorio_segredo"]}])
R.d("contar", [say("DLG_O_TELL_1", "SPK_CLARIM"), {"action": "sfx", "name": "exclaim"}, say("DLG_O_TELL_2"), say("DLG_O_TELL_3"),
               flag("ossorio_revelou"), flag("red_ossorio")])
R.d("segredo", [say("DLG_O_SECRET", "SPK_CLARIM"), flag("ossorio_segredo")])
R.d("selo", [{"say": "DLG_O_SELO_1", "speaker": "SPK_SELO", "if_not": "calico_beaten"},
             {"say": "DLG_O_SELO_OPEN", "speaker": "SPK_SELO", "if": "calico_beaten", "if_not": "livro_farol_lido"},
             ask("DLG_O_SELO_QUIZ", "SPK_SELO", [("OPT_O_KING", ref("selo_rei")), ("OPT_O_DUNA", ref("selo_certo")), ("OPT_O_AUNT", ref("selo_tia"))])
             | {"if": "livro_farol_lido"}])
R.d("selo_certo", [say("DLG_O_SELO_RIGHT", "SPK_SELO"), act("give_item", item="pocao_g", n=2), act("give_item", item="reviver", n=1), flag("selo_done")])
R.d("selo_rei", [say("DLG_O_SELO_WRONG_KING", "SPK_SELO")])
R.d("selo_tia", [say("DLG_O_SELO_WRONG_AUNT", "SPK_SELO")])
R.d("selo_depois", [say("DLG_O_SELO_AFTER", "SPK_SELO")])

R.NPCS["ameia"] = human("ameia", "SPK_AMEIA", [{"dialog": ref("ameia")}], role="ranch")
R.NPCS["dobrao"] = human("dobrao", "SPK_DOBRAO", [{"dialog": ref("dobrao")}], "stand", role="shop")
R.NPCS["fivela"] = human("fivela", "SPK_FIVELA", [{"dialog": ref("fivela")}], role="humor")
R.NPCS["brasao"] = human("brasao", "SPK_BRASAO", [{"dialog": ref("brasao")}], "stand", role="lore")
R.NPCS["clarim"] = human("clarim", "SPK_CLARIM", [{"dialog": ref("clarim")}], role="quest")
R.NPCS["selo"] = human("selo", "SPK_SELO", [{"if": "selo_done", "dialog": ref("selo_depois")}, {"dialog": ref("selo")}], "stand", role="quest")

# casas de domadores (Sintonia)
t("DLG_O_VISEIRA_1", "Em Ossório, dois agem como um. Sintonia é disciplina! Vamos ver a sua.",
  "In Ossório, two act as one. Sync is discipline! Let's see yours.", "En Ossório, dos actúan como uno. ¡La Sintonía es disciplina! Veamos la tuya.")
t("DLG_O_VISEIRA_2", "Quebrou nossa fileira com atraso. Isso é que é estudar o inimigo.", "You broke our line with delays. Now that's studying the enemy.",
  "Rompiste nuestra fila con retrasos. Eso es estudiar al enemigo.")
t("DLG_O_ELO_1", "A gente fala junto, luta junto, perde... separado?", "We talk together, fight together, lose... separately?",
  "Hablamos juntos, peleamos juntos, perdemos... ¿por separado?")
t("DLG_O_ELO_2", "Ensaiamos tudo. Menos perder.", "We rehearsed everything. Except losing.", "Ensayamos todo. Menos perder.")
R.d("viseira", [say("DLG_O_VISEIRA_1", "SPK_VISEIRA"),
                battle("BTL_TAMER_VISEIRA", team([("sentinela", 53), ("sineiro", 53)]), 760, "viseira_beaten", [["pocao_g", 2]]),
                say("DLG_O_VISEIRA_2", "SPK_VISEIRA")])
R.d("viseira_depois", [say("DLG_O_VISEIRA_2", "SPK_VISEIRA")])
R.d("elo", [say("DLG_O_ELO_1", "SPK_ELO"),
            battle("BTL_TAMER_ELO", team([("escriba", 53), ("escriba", 52)]), 740, "elo_beaten", [["reviver", 1], ["antidoto", 2]]),
            say("DLG_O_ELO_2", "SPK_ELO")])
R.d("elo_depois", [say("DLG_O_ELO_2", "SPK_ELO")])
R.tamer("viseira", "viseira", "SPK_VISEIRA", "viseira", "viseira_beaten", 3)
R.tamer("elo", "elo", "SPK_ELO", "elo", "elo_beaten", 3)

# ------------------------------------------------------------------ Arquivo Real: a revelação (pista 5) e o farol (Lia)
t("DLG_O_REC_1", "Um livro de registros, aberto há mil anos na mesma página.", "A book of records, open on the same page for a thousand years.",
  "Un libro de registros, abierto en la misma página desde hace mil años.")
t("DLG_O_REC_2", "\"Quando a coroa rachar, o eco chamará o último do sangue, onde o farol virar museu.\"",
  "\"When the crown cracks, the echo will call the last of the blood, where the lighthouse becomes a museum.\"",
  "\"Cuando la corona se agriete, el eco llamará al último de la sangre, donde el faro se vuelva museo.\"")
t("DLG_O_REC_3", "Ao lado, o retrato do príncipe Ossárion, menino. O rosto é o seu.", "Beside it, a portrait of Prince Ossárion as a boy. The face is yours.",
  "Al lado, el retrato del príncipe Ossárion, de niño. La cara es la tuya.")
t("DLG_O_REC_4", "O vidro vibrando. A coroa cantando na vitrine. Agora você lembra: você veio de 2040.",
  "The glass trembling. The crown singing in its case. Now you remember: you came from 2040.",
  "El cristal vibrando. La corona cantando en la vitrina. Ahora lo recuerdas: viniste de 2040.")
t("DLG_O_REC_5", "E foi chamado porque é do sangue do Rei.", "And you were called because you are of the King's blood.", "Y te llamaron porque eres de la sangre del Rey.")
t("DLG_O_REC_L1", "Esse menino... é você? Mas o quadro tem mil anos!", "That boy... is you? But the painting is a thousand years old!",
  "Ese niño... ¿eres tú? ¡Pero el cuadro tiene mil años!")
t("DLG_O_REC_L2", "Onde o farol virar museu... O meu farol vira museu um dia?", "Where the lighthouse becomes a museum... My lighthouse becomes a museum someday?",
  "Donde el faro se vuelva museo... ¿Mi faro se vuelve museo algún día?")
t("DLG_O_REC_T1", "Tá. Isso é estranho até pra mim.", "Okay. That's weird even for me.", "Vale. Esto es raro hasta para mí.")
t("DLG_O_REC_T2", "Se você é da família dele... ele te quer pra quê?", "If you're his family... what does he want you for?", "Si eres de su familia... ¿para qué te quiere?")
t("DLG_O_REC_AGAIN", "\"...onde o farol virar museu.\" O retrato continua olhando pra você.", "\"...where the lighthouse becomes a museum.\" The portrait keeps looking at you.",
  "\"...donde el faro se vuelva museo.\" El retrato sigue mirándote.")
t("DLG_O_BOOK_1", "Diário da Rainha Duna: \"Ergui o farol para que meu marido, quando saísse ao mar, sempre achasse o caminho de casa.\"",
  "Queen Duna's diary: \"I raised the lighthouse so my husband, whenever he went to sea, would always find his way home.\"",
  "Diario de la Reina Duna: \"Levanté el faro para que mi esposo, cuando saliera al mar, siempre encontrara el camino a casa.\"")
t("DLG_O_BOOK_L1", "A família do Rei construiu o farol! Eles também queriam que ninguém se perdesse.",
  "The King's family built the lighthouse! They didn't want anyone to get lost either.", "¡La familia del Rey construyó el faro! Ellos tampoco querían que nadie se perdiera.")
t("DLG_O_BOOK_L2", "Então o Rei não é mau. Ele só tem medo do escuro. Igual eu tinha.", "So the King isn't evil. He's just afraid of the dark. Like I used to be.",
  "Entonces el Rey no es malo. Solo le teme a la oscuridad. Como me pasaba a mí.")
t("DLG_O_BOOK_T1", "Farol. A Lia ia gostar de ler isso.", "A lighthouse. Lia would love reading this.", "Un faro. A Lia le encantaría leer esto.")
t("DLG_O_LIA_ARQ_1", "Lê o diário da estante! A rainha construiu o farol pro marido sempre voltar pra casa!",
  "Read the diary on the shelf! The queen built the lighthouse so her husband would always come home!", "¡Lee el diario del estante! ¡La reina construyó el faro para que su esposo siempre volviera a casa!")
t("DLG_O_LIA_ARQ_2", "Eu vou acender ele. Pra todo mundo voltar pra casa. Até o Rei.", "I'm going to light it. So everyone can come home. Even the King.",
  "Voy a encenderlo. Para que todos vuelvan a casa. Hasta el Rey.")
R.d("registro", [say("DLG_O_REC_1"), say("DLG_O_REC_2"), say("DLG_O_REC_3"), say("DLG_O_REC_4"), say("DLG_O_REC_5"),
                 lia("DLG_O_REC_L1"), lia("DLG_O_REC_L2"), taro("DLG_O_REC_T1"), taro("DLG_O_REC_T2"),
                 flag("pista_5"), act("give_item", item="registro_real", n=1)])
R.d("registro_de_novo", [say("DLG_O_REC_AGAIN")])
R.d("livro_farol", [say("DLG_O_BOOK_1"), lia("DLG_O_BOOK_L1"), lia("DLG_O_BOOK_L2"), taro("DLG_O_BOOK_T1") | {"if_not": "partner_lia"}, flag("livro_farol_lido")])
R.d("lia_arquivo", [say("DLG_O_LIA_ARQ_1", "SPK_LIA"), say("DLG_O_LIA_ARQ_2", "SPK_LIA"), flag("lia_arquivo_visto"), act("hide_npc", id="lia_arquivo")])
t("DLG_O_CRON_0", "Crônicas da Família Real, volume único. As páginas cheiram a poeira e a mar.",
  "Chronicles of the Royal Family, single volume. The pages smell of dust and sea.", "Crónicas de la Familia Real, volumen único. Las páginas huelen a polvo y a mar.")
t("DLG_O_CRON_1", "\"Ramalho, primo do rei, lenhador. Perdia toda queda de braço e ria mais alto que o vencedor.\"",
  "\"Ramalho, the king's cousin, woodcutter. Lost every arm-wrestling match and laughed louder than the winner.\"",
  "\"Ramalho, primo del rey, leñador. Perdía todos los pulsos y se reía más fuerte que el ganador.\"")
t("DLG_O_CRON_2", "\"Fornalha, tia do rei, ferreira. Forjou o sino de Brasal e criou o príncipe quando a mãe dele adoeceu.\"",
  "\"Furnace, the king's aunt, blacksmith. Forged the bell of Embervale and raised the prince when his mother fell ill.\"",
  "\"Fragua, tía del rey, herrera. Forjó la campana de Brasal y crió al príncipe cuando su madre enfermó.\"")
t("DLG_O_CRON_3", "\"Musga, sobrinha do rei, herbalista. Curava a corte inteira; ninguém lembrava de visitá-la na torre.\"",
  "\"Musga, the king's niece, herbalist. She healed the whole court; nobody remembered to visit her in the tower.\"",
  "\"Musga, sobrina del rey, herbolaria. Curaba a toda la corte; nadie se acordaba de visitarla en la torre.\"")
t("DLG_O_CRON_4", "\"Caliço, irmão do rei, capitão. Jurou nunca abandonar a família. Cumpriu até depois do fim.\"",
  "\"Caliço, the king's brother, captain. Swore never to abandon the family. He kept it even after the end.\"",
  "\"Caliço, hermano del rey, capitán. Juró nunca abandonar a la familia. Lo cumplió incluso después del final.\"")
t("DLG_O_CRON_5", "\"Duna, a rainha, veio do deserto com tambores. Ergueu o farol. Alva, a filha, nasceu na noite em que ele acendeu.\"",
  "\"Duna, the queen, came from the desert with drums. She raised the lighthouse. Alva, their daughter, was born the night it was first lit.\"",
  "\"Duna, la reina, vino del desierto con tambores. Levantó el faro. Alva, su hija, nació la noche en que se encendió.\"")
t("DLG_O_CRON_6", "A última página está em branco. Alguém escreveu a lápis, com letra de menino: \"Volta.\"",
  "The last page is blank. Someone wrote in pencil, in a boy's handwriting: \"Come back.\"",
  "La última página está en blanco. Alguien escribió a lápiz, con letra de niño: \"Vuelve.\"")
R.d("cronicas", [say("DLG_O_CRON_0"), say("DLG_O_CRON_1"), say("DLG_O_CRON_2"), say("DLG_O_CRON_3"), say("DLG_O_CRON_4"),
                 say("DLG_O_CRON_5"), say("DLG_O_CRON_6")])
R.NPCS["lia_arquivo"] = skel("skel_faroleira_3", "SPK_LIA", [{"dialog": ref("lia_arquivo")}])

# ------------------------------------------------------------------ Quartel: capanga, Bufardo, Guardião Caliço
t("DLG_O_ARR_Q_L", "Todo mundo no mesmo passo... parece música sem melodia.", "Everyone in step... it's like music without a tune.",
  "Todos al mismo paso... parece música sin melodía.")
t("DLG_O_ARR_Q_T", "Disciplina. Meu pai ia gostar. Eu não.", "Discipline. My dad would like it. I don't.", "Disciplina. A mi papá le gustaría. A mí no.")
t("DLG_O_GRADE_1", "Ninguém passa da grade sem senha. A senha é: vencer o Sargento Grade.", "Nobody gets past the bars without the password. The password is: beat Sergeant Bars.",
  "Nadie pasa la reja sin contraseña. La contraseña es: vencer al Sargento Reja.")
t("DLG_O_GRADE_2", "Senha correta. Infelizmente.", "Password correct. Unfortunately.", "Contraseña correcta. Por desgracia.")
t("DLG_O_BUFARDO", "Um esqueleto corneteiro, de bochechas infladas, ensaia um toque que ninguém ouve há mil anos.",
  "A bugler skeleton with puffed-up cheeks rehearses a call nobody has heard in a thousand years.",
  "Un esqueleto corneta, de mejillas infladas, ensaya un toque que nadie oye desde hace mil años.")
R.d("chegada_quartel", [lia("DLG_O_ARR_Q_L"), taro("DLG_O_ARR_Q_T"), flag("quartel_visto")])
R.d("grade", [say("DLG_O_GRADE_1", "SPK_GRADE"), battle("BTL_TAMER_GRADE", team([("sentinela", 55), ("escriba", 54)]), 720, "grade_beaten"),
              say("DLG_O_GRADE_2", "SPK_GRADE")])
R.d("grade_depois", [say("DLG_O_GRADE_2", "SPK_GRADE")])
R.tamer("grade", "grade", "SPK_GRADE", "grade", "grade_beaten", 3)
R.d("bufardo", [ask("DLG_O_BUFARDO", None, [("OPT_O_TRUMPET", ref("bufardo_luta")), ("OPT_M_LEAVE", None)])])
R.d("bufardo_luta", [battle("", [["bufardo", 53]], 0, kind="wild")])
R.NPCS["bufardo_npc"] = skel("skel_bufardo", "SPECIES_BUFARDO", [{"dialog": ref("bufardo")}], role="wild")

t("DLG_O_CAL_1", "Atenção! Civil não entra no quartel! Identifique-se!", "Attention! No civilians in the barracks! Identify yourself!",
  "¡Atención! ¡Ningún civil entra al cuartel! ¡Identifíquese!")
t("DLG_O_CAL_2", "Sou Caliço, irmão do Rei. A família não abandona a família. Nunca.", "I am Caliço, the King's brother. Family does not abandon family. Ever.",
  "Soy Caliço, hermano del Rey. La familia no abandona a la familia. Nunca.")
t("DLG_O_CAL_3", "Em formação! Vamos ver se você sabe quebrar uma fileira.", "Fall in! Let's see if you know how to break a line.",
  "¡En formación! Veamos si sabes romper una fila.")
t("DLG_O_CAL_WIN", "Fileira rompida... Recuar com honra!", "Line broken... Retreat with honor!", "Fila rota... ¡Retirada con honor!")
t("DLG_O_CAL_MOTIVE", "Meu irmão perdeu todos uma vez. Eu jurei que ele nunca mais perderia ninguém.",
  "My brother lost everyone once. I swore he would never lose anyone again.", "Mi hermano perdió a todos una vez. Juré que nunca volvería a perder a nadie.")
t("DLG_O_CAL_OPEN", "Regra do quartel: o vencedor tem direito ao Arquivo. Leia o que meu irmão escondeu.",
  "Barracks rule: the victor earns the Archive. Read what my brother hid.", "Regla del cuartel: el vencedor tiene derecho al Archivo. Lee lo que mi hermano escondió.")
t("DLG_O_CAL_OPEN2", "Honra exige verdade. Mesmo a verdade que dói.", "Honor demands truth. Even the truth that hurts.", "El honor exige verdad. Incluso la verdad que duele.")
t("DLG_O_CAL_TOLD", "Você contou à cidade. Insubordinação... e verdade. Quando chegar a hora, conte comigo.",
  "You told the city. Insubordination... and truth. When the time comes, count on me.", "Se lo contaste a la ciudad. Insubordinación... y verdad. Cuando llegue la hora, cuenta conmigo.")
t("DLG_O_CAL_KEPT", "Você guardou o segredo. Discrição. Um soldado agradece.", "You kept the secret. Discretion. A soldier is grateful.",
  "Guardaste el secreto. Discreción. Un soldado lo agradece.")
CALICO_TEAM = team([("sentinela", 62), ("escriba", 61), ("sineiro", 62), ("lenhador", 63)])
R.d("calico", [say("DLG_O_CAL_1", "SPK_CALICO"), say("DLG_O_CAL_2", "SPK_CALICO"), say("DLG_O_CAL_3", "SPK_CALICO"),
               battle("BTL_TAMER_CALICO", CALICO_TEAM, 1600, "calico_beaten", kind="boss"),
               say("DLG_O_CAL_WIN", "SPK_CALICO"), say("DLG_O_CAL_MOTIVE", "SPK_CALICO"), say("DLG_O_CAL_OPEN", "SPK_CALICO"),
               say("DLG_O_CAL_OPEN2", "SPK_CALICO"), act("refresh_map")])
R.d("calico_depois", [{"say": "DLG_O_CAL_TOLD", "speaker": "SPK_CALICO", "if": "ossorio_revelou"},
                      {"say": "DLG_O_CAL_KEPT", "speaker": "SPK_CALICO", "if": "ossorio_segredo"},
                      {"say": "DLG_O_CAL_OPEN2", "speaker": "SPK_CALICO", "if_none": ["ossorio_revelou", "ossorio_segredo"]}])
R.NPCS["calico"] = {"name_key": "SPK_CALICO", "role": "guardian", "sprite": "res://assets/sprites/npc/skel_calico.png", "frames": 2, "idle_fps": 2.0,
                    "behavior": "stand", "dialog": [{"if": "calico_beaten", "dialog": ref("calico_depois")}, {"dialog": ref("calico")}],
                    "tamer": {"vision": 3, "flag": "calico_beaten"}}


# ------------------------------------------------------------------ encontros (balance.json: selvagens 45–51)
def e(sp, st, a, b, rar, w=None):
    d = {"species": sp, "stage": st, "min_level": a, "max_level": b, "rarity": rar}
    if w:
        d["weight"] = w
    return d


R.TABLES.update({
    "rota4_sul": [e("sentinela_2", 2, 45, 47, "comum"), e("lavadeira_2", 2, 45, 47, "comum")],
    "rota4_oeste": [e("sentinela_2", 2, 46, 48, "comum"), e("ferreiro_3", 3, 46, 48, "incomum")],
    "rota4_campo": [e("sentinela_2", 2, 46, 48, "comum"), e("sineiro_2", 2, 46, 48, "incomum"), e("escriba_2", 2, 47, 49, "raro"),
                    e("lavadeira_2", 2, 46, 48, "comum"), e("ferreiro_3", 3, 47, 49, "incomum")],
    "rota4_aqueduto": [e("escriba_2", 2, 54, 55, "raro", 60), e("sineiro_2", 2, 54, 55, "incomum", 40)],
    "rota4_norte": [e("sentinela_2", 2, 48, 50, "comum"), e("sineiro_2", 2, 48, 50, "incomum")],
    "quartel_salao": [e("sentinela_2", 2, 49, 51, "comum"), e("escriba_2", 2, 49, 51, "raro"), e("ferreiro_3", 3, 49, 51, "incomum")],
    "quartel_sul": [e("sineiro_2", 2, 50, 51, "incomum"), e("sentinela_2", 2, 50, 51, "comum")],
})
R.SHOPS["ossorio"] = ["pocao_m", "pocao_g", "antidoto", "reviver"]

# ------------------------------------------------------------------ mapas
LEG = {"g": "grass", "f": "flowers", "B": "bush", "p": "stone", ".": "floor"}
rota = make_route("rota_4", "ossorio", "MAP_ROTA_4", LEG, ("brejo", 19, 1), ("ossorio", 19, 30),
                  tamers=[("elmo", {}), ("malva", {}), ("bigode", {})], hint="trote", sign=R.ref("placa_bifurcacao"),
                  spawns=[{"id": "r4_sul", "table": "rota4_sul", "x": 10, "y": 45, "radius": 3, "count": 2},
                          {"id": "r4_oeste", "table": "rota4_oeste", "x": 5, "y": 25, "radius": 2, "count": 1},
                          {"id": "r4_campo_a", "table": "rota4_campo", "x": 30, "y": 32, "radius": 4, "count": 3},
                          {"id": "r4_campo_b", "table": "rota4_campo", "x": 30, "y": 18, "radius": 4, "count": 3},
                          {"id": "r4_aqueduto", "table": "rota4_aqueduto", "x": 19, "y": 25, "radius": 2, "count": 1},
                          {"id": "r4_norte", "table": "rota4_norte", "x": 10, "y": 6, "radius": 3, "count": 2}],
                  extra_npcs=[{"id": "rival_taro_o", "x": 24, "y": 6, "facing": "down", "if": "partner_lia", "if_none": ["partner_taro", "rival_ossorio_done"]},
                              {"id": "rival_lia_o", "x": 24, "y": 6, "facing": "down", "if": "partner_taro", "if_none": ["partner_lia", "rival_ossorio_done"]}],
                  extra_props=[{"type": "banner_blue", "x": 18, "y": 36}, {"type": "banner_blue", "x": 21, "y": 36},
                               {"type": "banner_blue", "x": 18, "y": 13}, {"type": "banner_blue", "x": 21, "y": 13},
                               {"type": "broken_column", "x": 22, "y": 30}, {"type": "broken_column", "x": 17, "y": 20}],
                  deco=("tree_oak", "tree_oak2", "rock_small", "banner_blue"), tint=[0.98, 0.97, 1.0], seed=61)
rota["on_enter"] = [{"if_not": "rota4_vista", "dialog": R.ref("chegada_rota")}]
rota["ambient"] = ["leaves"]

town = make_town("ossorio", "ossorio", "MAP_OSSORIO", {"g": "stone", "p": "path", "B": "city_wall", "s": "path", "f": "flowers"},
                 south=("rota_4", 19, 1), north=("rota_5", 19, 48), west=("quartel", 32, 10),
                 houses=["townhouse_ranch", "townhouse_shop", "townhouse", "townhouse", "townhouse"],
                 npcs=[{"id": "fivela", "x": 16, "y": 16, "facing": "right"}, {"id": "brasao", "x": 24, "y": 18, "facing": "left"},
                       {"id": "clarim", "x": 22, "y": 13, "facing": "down"}, {"id": "selo", "x": 16, "y": 24, "facing": "up"}],
                 props=[{"type": "sign", "x": 18, "y": 28, "dialog": R.ref("placa_cidade")}, {"type": "sign", "x": 3, "y": 14, "dialog": R.ref("placa_quartel")},
                        {"type": "fountain", "x": 20, "y": 16}, {"type": "statue_prince", "x": 17, "y": 13, "dialog": R.ref("estatua")},
                        {"type": "bell_tower", "x": 27, "y": 16}, {"type": "banner_blue", "x": 13, "y": 12}, {"type": "banner_blue", "x": 26, "y": 12},
                        {"type": "torch", "x": 18, "y": 2}, {"type": "torch", "x": 21, "y": 2}],
                 deco=("banner_blue", "torch", "barrel", "crate"), deco_ok="g", tint=[0.98, 0.96, 0.98], seed=71, plaza="s")
for w in town["warps"]:
    if w["to"] == "rota_5":
        w["if"] = "calico_beaten"
        w["locked_message"] = "MSG_CALICO_ROAD"
    if w["to"] == "ossorio_arquivo":
        w["if"] = "calico_beaten"
        w["locked_message"] = "MSG_ARCHIVE_SEALED"
town["on_enter"] = [{"if_not": "ossorio_visto", "dialog": R.ref("chegada_cidade")}]
town_doors(town, "ossorio", {"rancho": "ossorio_rancho", "loja": "ossorio_loja", "a": "ossorio_casa_viseira", "b": "ossorio_casa_elo", "c": "ossorio_arquivo"})
for w in town["warps"]:
    if w["to"] == "ossorio_arquivo":
        w["if"] = "calico_beaten"
        w["locked_message"] = "MSG_ARCHIVE_SEALED"

lair = make_lair("quartel", "ossorio", "MAP_QUARTEL", {"g": "stone", "p": "path", "B": "city_wall", "f": "carpet"}, east=("ossorio", 1, 15),
                 guardian_npc={"id": "calico", "x": 10, "y": 3, "facing": "down"},
                 extra_npcs=[{"id": "grade", "x": 14, "y": 10, "facing": "right"}, {"id": "bufardo_npc", "x": 9, "y": 15, "facing": "left"}],
                 props=[{"type": "banner_blue", "x": 4, "y": 2}, {"type": "banner_blue", "x": 16, "y": 2}, {"type": "torch", "x": 7, "y": 1},
                        {"type": "torch", "x": 13, "y": 1}, {"type": "pillar", "x": 18, "y": 8}, {"type": "pillar", "x": 28, "y": 8},
                        {"type": "torch", "x": 22, "y": 13}, {"type": "barrel", "x": 4, "y": 19}, {"type": "crate", "x": 12, "y": 18}],
                 spawns=[{"id": "q_salao", "table": "quartel_salao", "x": 23, "y": 10, "radius": 3, "count": 2},
                         {"id": "q_sul", "table": "quartel_sul", "x": 6, "y": 15, "radius": 2, "count": 1}],
                 tint=[0.92, 0.9, 0.96])
lair["on_enter"] = [{"if_not": "quartel_visto", "dialog": R.ref("chegada_quartel")}]

arquivo = room("ossorio_arquivo", "ossorio", "MAP_ARQUIVO", "ossorio", (14, 27),
               [{"type": "bookshelf", "x": 3, "y": 2, "dialog": R.ref("livro_farol")}, {"type": "bookshelf", "x": 10, "y": 2, "dialog": R.ref("cronicas")},
                {"type": "lectern", "x": 6, "y": 5, "dialog": R.ref("registro"), "if_not": "pista_5"},
                {"type": "lectern", "x": 6, "y": 5, "dialog": R.ref("registro_de_novo"), "if": "pista_5"},
                {"type": "portrait", "x": 8, "y": 1, "dialog": R.ref("registro_de_novo")}, {"type": "candelabra", "x": 1, "y": 7},
                {"type": "candelabra", "x": 10, "y": 7}],
               [{"id": "lia_arquivo", "x": 4, "y": 4, "facing": "up", "if": "partner_taro", "if_none": ["partner_lia", "lia_arquivo_visto"]}],
               floor="carpet")
R.MAPS.update({
    "rota_4": rota, "ossorio": town, "quartel": lair, "ossorio_arquivo": arquivo,
    "ossorio_rancho": room("ossorio_rancho", "ossorio", "MAP_OSSORIO_RANCHO", "ossorio", (12, 10),
                           [{"type": "bed", "x": 2, "y": 3}, {"type": "bed", "x": 4, "y": 3}, {"type": "bed", "x": 9, "y": 3}, {"type": "rug", "x": 6, "y": 6}],
                           [{"id": "ameia", "x": 7, "y": 3, "facing": "down"}]),
    "ossorio_loja": room("ossorio_loja", "ossorio", "MAP_OSSORIO_LOJA", "ossorio", (27, 10),
                         [{"type": "shelf", "x": 3, "y": 2}, {"type": "shelf", "x": 10, "y": 2}, {"type": "table", "x": 7, "y": 4}, {"type": "crate", "x": 10, "y": 7}],
                         [{"id": "dobrao", "x": 6, "y": 3, "facing": "down"}]),
    "ossorio_casa_viseira": room("ossorio_casa_viseira", "ossorio", "MAP_OSSORIO_CASA_VISEIRA", "ossorio", (8, 20),
                                 [{"type": "banner_blue", "x": 2, "y": 2}, {"type": "table", "x": 7, "y": 5}, {"type": "barrel", "x": 10, "y": 7}],
                                 [{"id": "viseira", "x": 6, "y": 3, "facing": "down"}]),
    "ossorio_casa_elo": room("ossorio_casa_elo", "ossorio", "MAP_OSSORIO_CASA_ELO", "ossorio", (31, 20),
                             [{"type": "bed", "x": 2, "y": 3}, {"type": "bed", "x": 4, "y": 3}, {"type": "table", "x": 8, "y": 5}],
                             [{"id": "elo", "x": 6, "y": 3, "facing": "down"}]),
})
R.BATTLE_BG["ossorio"] = "res://assets/battle/bg_ossorio.png"
R.CITIES.append({"id": "ossorio", "map": "ossorio", "ranch": "ameia", "shop": "ossorio", "tamer_houses": ["viseira", "elo"],
                 "npcs": ["fivela", "brasao", "clarim", "selo"], "quests": ["selo", "clarim"]})
R.ROUTES.append({"id": "rota_4", "map": "rota_4", "from": "brejo", "to": "ossorio",
                 "paths": [{"kind": "domadores", "required": False}, {"kind": "selvagem", "required": False},
                           {"kind": "atalho", "required": False, "note": "Aqueduto Velho: curto, com um selvagem forte"}]})

# ------------------------------------------------------------------ documento
R.DOC = {
    "title": "Ato 4: Rota 4 e Cidade Murada de Ossório", "phase": "4e", "duration": "25 min",
    "ages": "chegada 46–54; selvagens 45–51; domadores 48–55; Guardião ~62 (protótipo do balance.json)",
    "problem": "**Ossório**, a antiga capital do reino, vive em **lei marcial**: o Guardião **Caliço** pôs os moradores de guarda na muralha à espera de um inimigo "
               "que nunca vem, impôs toque de recolher e fechou o portão norte. O **Arquivo Real** está lacrado por ordem do Rei: \"ninguém lê o passado\". "
               "O Rei esconde ali o motivo de tudo: a profecia do herdeiro.",
    "clue_n": 5,
    "clue": "**A revelação de 2040.** No Arquivo Real, o registro: \"Quando a coroa rachar, o eco chamará o último do sangue, onde o farol virar museu.\" "
            "Ao lado, o retrato do príncipe Ossárion menino, com o rosto do protagonista. Ele lembra do vidro vibrando e da coroa cantando no museu: "
            "veio de 2040 porque é do sangue do Rei. (Pistas 1–4 fecham aqui: ingresso, brasão, mapa, \"cheiro de família\".)",
    "moment": ["**Lia:** no Arquivo, o diário da Rainha Duna conta que ela ergueu o farol para o marido sempre achar o caminho de casa. "
               "Parceira: \"Então o Rei não é mau. Ele só tem medo do escuro. Igual eu tinha.\" Recorrente: ela está no Arquivo e promete acender o farol \"até pro Rei\".",
               "**Recorrente:** batalha opcional no norte da Rota 4 (Taro: \"vou passar por todos\"; Lia: \"uma batalha pra dar coragem\"). "
               "Depois, Taro deixa o jogador ir na frente \"só hoje\" — primeiro sinal de confiança.",
               "Lia e Taro estão os dois na equipe (decisão do Fernando): tocam as falas de parceiro dos dois; as cenas de \"recorrente\" só aparecem em saves antigos, com um parceiro só.", "Arco de Lia: medo → coragem → começa a ver o Rei como alguém com medo, e não como vilão."],
    "guardian": {"name": "Comandante Caliço (irmão do Rei)", "kin": "irmão",
                 "personality": "orgulhoso, militar, honrado; fala em ordens (\"Atenção!\", \"Em formação!\")",
                 "motive": "**Honra:** \"A família não abandona a família.\" Jurou que o irmão nunca mais perderia ninguém.",
                 "mechanic": "**Sintonia.** A equipe age em pares seguidos na timeline (+25%). Ensina a **montar** Sintonia e a **quebrá-la** com golpes de atraso. "
                             "A Capitã Viseira e os Gêmeos Elo treinam isso antes.",
                 "team": "Bastião 62, Escrivélio 61, Carrilhão 62, Troncalho 63.",
                 "reward": "1600 moedas; o Arquivo abre e o portão norte também."},
    "maps": [("**Rota 4** (`rota_4`)", "Estrada real de pedra. 3 caminhos: **Cadetes** (oeste: Elmo, Malva, Bigode), **Campo das Bandeiras** (leste) e **Aqueduto Velho** "
              "(centro, curto, com um selvagem forte). Recorrente no norte. Placa e o Mensageiro Trote dão a dica."),
             ("**Ossório** (`ossorio`)", "Cidade murada: Rancho (Ameia), Empório (Dobrão), casas da Capitã Viseira e dos Gêmeos Elo, o **Arquivo Real** (abre após o Guardião), "
              "praça com chafariz, estátua do príncipe e torre do sino; Clarim (escolha 4) e Selo (missão do farol)."),
             ("**Quartel** (`quartel`)", "Salão com selvagens, Sargento Grade, câmara sul com o único **Bufardo** e o pátio do Caliço."),
             ("Interiores", "Rancho da Ameia, Empório do Dobrão, casas da Viseira e dos Elo, Arquivo Real.")],
}
R.NPC_DOC = [
    ("Mensageiro Trote", "dica", "Explica os 3 caminhos; mostra o quartel que só carimba e não responde"),
    ("Elmo, Malva, Bigode", "domadores da rota", "Caminho dos Cadetes; soldados entediados pela lei marcial"),
    ("Dona Ameia", "Rancho", "Cura; o toque de recolher até no Rancho"),
    ("Mercador Dobrão", "Loja", "Comércio com autorização do quartel (humor burocrático)"),
    ("Fivela", "humor", "O pai vigia a muralha; muda depois do Guardião"),
    ("Velho Brasão", "lore", "Conheceu o príncipe menino que só olhava o mar"),
    ("Pregoeiro Clarim", "escolha 4", "Lê (ou não) o Registro Real na praça"),
    ("Arquivista Selo", "missão", "Pergunta quem ergueu o farol (só acerta quem leu o diário)"),
    ("Sargento Grade", "capanga", "Guarda o pátio do Guardião"),
    ("Caliço", "Guardião", "Sintonia; abre o Arquivo por honra"),
]
R.HOUSES = [
    ("Capitã Viseira", "Sintonia em fileira (Broquel + Badaleiro)", "760 moedas + 2 Poções G"),
    ("Gêmeos Elo", "Sintonia de iguais (dois Escrivélios)", "740 moedas + 1 Reviver + 2 Antídotos"),
]
R.CHOICES = [
    ("Caminho da Rota 4", "Cadetes / Campo das Bandeiras / Aqueduto", "Moedas e itens / XP e marcadores / curto, com um selvagem forte"),
    ("Recorrente", "Lutar / recusar", "700 moedas e +10% no marcador"),
    ("**Escolha 4: o Registro Real**", "Contar à cidade / Guardar segredo",
     "Contar: a cidade se rebela, guardas leais ao Rei passam a vigiar a Rota 5 (**mais batalhas**), Caliço promete ficar do seu lado no Castelo; **+1 Redenção** (`red_ossorio`). "
     "Segredo: menos batalhas, e Caliço fica neutro."),
    ("Missão do farol (Selo)", "Responder / ignorar", "Acertar (Rainha Duna): 2 Poções G + 1 Reviver"),
]

if __name__ == "__main__":
    R.write()
