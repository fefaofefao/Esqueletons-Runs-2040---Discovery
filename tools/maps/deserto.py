#!/usr/bin/env python3
"""Ato 6 — Rota 6 e Deserto dos Ecos (fase 4g). Fonte única: gera
docs/roteiro/07_deserto.md, falas (PT/EN/ES), NPCs, encontros, loja, itens e
mapas (Rota 6, Palmeiral e interiores, Templo das Areias)."""
from regionkit import (Region, make_lair, make_route, make_town, room, town_doors, team,
                       say, ask, battle, act, flag, goto, human, skel)

R = Region("deserto", 7, "deserto", ["deserto"])
t = R.t
ref = R.ref


def lia(k):
    return say(k, "SPK_LIA") | {"if": "partner_lia"}


def taro(k):
    return say(k, "SPK_TARO") | {"if": "partner_taro"}


# ------------------------------------------------------------------ nomes
for k, pt, en, es in [
        ("CANTIL", "Velho Cantil", "Old Canteen", "Viejo Cantimplora"), ("CORCOVA", "Cameleiro Corcova", "Drover Hump", "Camellero Joroba"),
        ("VEU", "Dançarina Véu", "Dancer Veil", "Bailarina Velo"), ("PA", "Arqueólogo Pá", "Archaeologist Spade", "Arqueólogo Pala"),
        ("MORINGA", "Dona Moringa", "Mrs. Jug", "Doña Botijo"), ("CANELA", "Mercadora Canela", "Merchant Cinnamon", "Mercadera Canela"),
        ("TAMARA", "Cameleira Tâmara", "Drover Date", "Camellera Dátil"), ("BATUQUE", "Irmãos Batuque", "Drumbeat Brothers", "Hermanos Tamborrada"),
        ("ROSA", "Cartógrafa Rosa", "Cartographer Rose", "Cartógrafa Rosa"), ("ALFORJE", "Seu Alforje", "Mr. Saddlebag", "Don Alforja"),
        ("GRAO", "Grão", "Grain", "Grano"), ("MIRAGEM", "Vó Miragem", "Granny Mirage", "Abuela Espejismo"),
        ("SANDALO", "Camareiro Sândalo", "Chamberlain Sandal", "Chambelán Sándalo"), ("DUNA", "Rainha Duna", "Queen Duna", "Reina Duna")]:
    t(f"SPK_{k}", pt, en, es)
for k in ("CORCOVA", "VEU", "PA", "TAMARA", "BATUQUE", "SANDALO"):
    pt, en, es = R.T[f"SPK_{k}"]
    t(f"BTL_TAMER_{k}", pt, en, es)
t("BTL_TAMER_DUNA", "Guardiã Rainha Duna", "Guardian Queen Duna", "Guardiana Reina Duna")
t("MAP_ROTA_6", "Rota 6 — Mar de Dunas", "Route 6 — Sea of Dunes", "Ruta 6 — Mar de Dunas")
t("MAP_PALMEIRAL", "Palmeiral", "Palmgrove", "Palmeral")
t("MAP_TEMPLO", "Templo das Areias", "Temple of Sands", "Templo de las Arenas")
t("MAP_PALMEIRAL_RANCHO", "Rancho da Moringa", "Jug's Ranch", "Rancho de Botijo")
t("MAP_PALMEIRAL_LOJA", "Tenda da Canela", "Cinnamon's Tent", "Tienda de Canela")
t("MAP_PALMEIRAL_CASA_TAMARA", "Tenda da Tâmara", "Date's Tent", "Tienda de Dátil")
t("MAP_PALMEIRAL_CASA_BATUQUE", "Tenda dos Batuque", "Drumbeat Tent", "Tienda de los Tamborrada")
t("MAP_PALMEIRAL_CASA_ROSA", "Tenda da Cartógrafa", "Cartographer's Tent", "Tienda de la Cartógrafa")
t("MSG_STORM_ROAD", "Uma tempestade de areia sem fim esconde a estrada do castelo.", "An endless sandstorm hides the road to the castle.",
  "Una tormenta de arena sin fin oculta el camino al castillo.")
t("OPT_D_HOURGLASS", "Virar a ampulheta", "Turn the hourglass", "Girar el reloj de arena")

# ------------------------------------------------------------------ Rota 6
t("SIGN_D_FORK", "← Trilha das Caravanas · ↑ Passagem do Eco · → Dunas Altas",
  "← Caravan Trail · ↑ Echo Pass · → High Dunes", "← Senda de Caravanas · ↑ Paso del Eco · → Dunas Altas")
t("DLG_D_ARR_R_L", "Oi! ...Oi... oi... O deserto repete tudo que a gente fala!", "Hello! ...Hello... hello... The desert repeats everything we say!",
  "¡Hola! ...Hola... hola... ¡El desierto repite todo lo que decimos!")
t("DLG_D_ARR_R_L2", "Será que ele também fica sozinho?", "Do you think it gets lonely too?", "¿Se sentirá solo él también?")
t("DLG_D_ARR_R_T", "Areia na bota. Areia no osso. Areia em tudo.", "Sand in my boots. Sand in my bones. Sand in everything.", "Arena en las botas. Arena en los huesos. Arena en todo.")
t("DLG_D_CANTIL_1", "Caravana vai pelo oeste, bicho anda pelas dunas altas, e no meio... o eco engana. Siga a parede.",
  "Caravans go west, critters roam the high dunes, and in the middle... the echo fools you. Follow the wall.",
  "Las caravanas van por el oeste, los bichos por las dunas altas, y en medio... el eco engaña. Sigue la pared.")
t("DLG_D_CANTIL_2", "Antes, os tambores guiavam a gente. A rainha mandou calar todos. Agora só o vento fala.",
  "The drums used to guide us. The queen silenced them all. Now only the wind speaks.",
  "Antes, los tambores nos guiaban. La reina mandó callarlos. Ahora solo habla el viento.")
t("DLG_D_CORCOVA_1", "Meu camelo fugiu e me deixou os esqueletos. Troca justa? Vamos descobrir!",
  "My camel ran off and left me the skeletons. A fair trade? Let's find out!", "Mi camello se fue y me dejó los esqueletos. ¿Cambio justo? ¡Vamos a ver!")
t("DLG_D_CORCOVA_2", "Troca justa. Meio injusta pra mim.", "A fair trade. Slightly unfair for me.", "Cambio justo. Un poco injusto para mí.")
t("DLG_D_VEU_1", "Danço pra espantar a tempestade. Ainda não funcionou. Talvez com uma batalha!",
  "I dance to chase off the storm. Hasn't worked yet. Maybe with a battle!", "Bailo para espantar la tormenta. Aún no funcionó. ¡Quizá con una batalla!")
t("DLG_D_VEU_2", "A tempestade ficou. Mas eu me diverti.", "The storm stayed. But I had fun.", "La tormenta se quedó. Pero me divertí.")
t("DLG_D_PA_1", "Cavo atrás do reino antigo. Achei três colheres e um esqueleto bravo. Quer conhecer?",
  "I dig for the ancient kingdom. Found three spoons and an angry skeleton. Want to meet it?",
  "Excavo buscando el reino antiguo. Encontré tres cucharas y un esqueleto enojado. ¿Quieres conocerlo?")
t("DLG_D_PA_2", "Vou catalogar essa derrota. Peça número quatro.", "I'll catalog this defeat. Item number four.", "Catalogaré esta derrota. Pieza número cuatro.")
t("DLG_D_ALFORJE_1", "Água! ...Ah, não é água. É gente. Também serve! Me perdi seguindo o meu próprio eco.",
  "Water! ...Oh, it's not water. It's people. That works too! I got lost following my own echo.",
  "¡Agua! ...Ah, no es agua. Es gente. ¡También sirve! Me perdí siguiendo mi propio eco.")
t("DLG_D_ALFORJE_2", "Diz pra Rosa, lá em Palmeiral, que eu tô vivo. E que o mapa dela tava certo. Eu é que tava errado.",
  "Tell Rose, back in Palmgrove, that I'm alive. And that her map was right. I was the one who was wrong.",
  "Dile a Rosa, en Palmeral, que estoy vivo. Y que su mapa tenía razón. El equivocado era yo.")
t("DLG_D_ALFORJE_3", "Vou esperar a tempestade baixar. Sentadinho. Sem eco.", "I'll wait for the storm to die down. Sitting still. No echoes.",
  "Esperaré a que amaine la tormenta. Sentadito. Sin eco.")
R.d("placa_bifurcacao", [say("SIGN_D_FORK")])
R.d("chegada_rota", [lia("DLG_D_ARR_R_L"), lia("DLG_D_ARR_R_L2"), taro("DLG_D_ARR_R_T"), flag("rota6_vista")])
R.d("cantil", [say("DLG_D_CANTIL_1", "SPK_CANTIL"), say("DLG_D_CANTIL_2", "SPK_CANTIL")])
R.d("corcova", [say("DLG_D_CORCOVA_1", "SPK_CORCOVA"),
                battle("BTL_TAMER_CORCOVA", team([("domador_escorpioes", 72), ("palafiteiro", 72)]), 860, "corcova_beaten"),
                say("DLG_D_CORCOVA_2", "SPK_CORCOVA")])
R.d("corcova_depois", [say("DLG_D_CORCOVA_2", "SPK_CORCOVA")])
R.d("veu", [say("DLG_D_VEU_1", "SPK_VEU"), battle("BTL_TAMER_VEU", team([("tamborileiro", 73), ("escultor", 73)]), 880, "veu_beaten"),
            say("DLG_D_VEU_2", "SPK_VEU")])
R.d("veu_depois", [say("DLG_D_VEU_2", "SPK_VEU")])
R.d("pa", [say("DLG_D_PA_1", "SPK_PA"),
           battle("BTL_TAMER_PA", team([("cartografo", 74), ("domador_escorpioes", 74)]), 900, "pa_beaten", [["pocao_g", 2]]),
           say("DLG_D_PA_2", "SPK_PA")])
R.d("pa_depois", [say("DLG_D_PA_2", "SPK_PA")])
R.d("alforje", [say("DLG_D_ALFORJE_1", "SPK_ALFORJE"), say("DLG_D_ALFORJE_2", "SPK_ALFORJE"), flag("alforje_achado")])
R.d("alforje_depois", [say("DLG_D_ALFORJE_3", "SPK_ALFORJE")])
R.NPCS["cantil"] = human("cantil", "SPK_CANTIL", [{"dialog": ref("cantil")}])
R.tamer("corcova", "corcova", "SPK_CORCOVA", "corcova", "corcova_beaten")
R.tamer("veu", "veu", "SPK_VEU", "veu", "veu_beaten")
R.tamer("pa", "pa", "SPK_PA", "pa", "pa_beaten", 3)
R.NPCS["alforje"] = human("alforje", "SPK_ALFORJE", [{"if": "alforje_achado", "dialog": ref("alforje_depois")}, {"dialog": ref("alforje")}], "stand", role="quest")

# ------------------------------------------------------------------ Palmeiral
t("SIGN_D_TOWN", "Palmeiral. Água, sombra e notícia velha.", "Palmgrove. Water, shade and old news.", "Palmeral. Agua, sombra y noticias viejas.")
t("SIGN_D_TEMPLE", "← Templo das Areias. Silêncio: a rainha descansa.", "← Temple of Sands. Silence: the queen is resting.",
  "← Templo de las Arenas. Silencio: la reina descansa.")
t("DLG_D_ARR_C_L", "Um lago no meio do deserto! Parece um farol de água.", "A lake in the middle of the desert! It's like a lighthouse made of water.",
  "¡Un lago en medio del desierto! Parece un faro de agua.")
t("DLG_D_ARR_C_T", "Tambores pendurados e ninguém tocando. Isso tá errado.", "Drums hanging everywhere and nobody playing. That's wrong.",
  "Tambores colgados y nadie tocando. Eso está mal.")
t("DLG_D_MORINGA_1", "Bebe água primeiro, conversa depois. Seus esqueletos também: osso seco racha.",
  "Drink water first, talk later. Your skeletons too: dry bones crack.", "Primero bebe agua, luego hablamos. Tus esqueletos también: el hueso seco se agrieta.")
t("DLG_D_MORINGA_AFTER", "Tão tocando tambor lá fora! Faz um ano que eu não durmo com barulho bom.",
  "They're playing drums outside! I haven't fallen asleep to good noise in a year.", "¡Están tocando tambores afuera! Hace un año que no duermo con ruido bonito.")
t("DLG_D_MORINGA_2", "Quer deixar alguém aqui na sombra? Eu rego direitinho.", "Want to leave someone here in the shade? I'll water them properly.",
  "¿Quieres dejar a alguien aquí a la sombra? Lo riego bien.")
t("DLG_D_CANELA_1", "Tempero, tecido e remédio. A caravana não chega, então o preço é o da saudade.",
  "Spices, cloth and remedies. The caravan doesn't come anymore, so prices are set by longing.",
  "Especias, telas y remedios. La caravana no llega, así que el precio es el de la nostalgia.")
t("DLG_D_CANELA_2", "Volte com sede de compras.", "Come back thirsty for shopping.", "Vuelve con sed de compras.")
t("DLG_D_GRAO", "Eu contei os grãos de areia da praça. Deu um monte. Amanhã eu conto de novo pra conferir.",
  "I counted the grains of sand in the square. It came out to a lot. Tomorrow I'll count again to check.",
  "Conté los granos de arena de la plaza. Salieron un montón. Mañana los cuento otra vez para comprobar.")
t("DLG_D_GRAO_AFTER", "Com a tempestade embora, dá pra ver o castelo! Ele é mais feio de perto?",
  "With the storm gone, you can see the castle! Is it uglier up close?", "¡Sin la tormenta se ve el castillo! ¿Es más feo de cerca?")
t("DLG_D_MIRAGEM_1", "A rainha Duna era a mais gentil da corte. Quando o Rei voltou triste, ela levantou a tempestade pra ninguém incomodar.",
  "Queen Duna was the kindest of the court. When the King came back sad, she raised the storm so nobody would bother him.",
  "La reina Duna era la más amable de la corte. Cuando el Rey volvió triste, levantó la tormenta para que nadie lo molestara.")
t("DLG_D_MIRAGEM_2", "Amor também constrói muralha. Só que de areia.", "Love builds walls too. Only they're made of sand.", "El amor también levanta murallas. Solo que de arena.")
t("DLG_D_ROSA_ASK", "O Alforje saiu com a caravana e sumiu na Rota 6. Meu mapa diz que ele tá nas dunas altas, mas ninguém acredita em mapa.",
  "Saddlebag left with the caravan and vanished on Route 6. My map says he's in the high dunes, but nobody believes maps.",
  "Alforja salió con la caravana y desapareció en la Ruta 6. Mi mapa dice que está en las dunas altas, pero nadie cree en los mapas.")
t("DLG_D_ROSA_ASK2", "Você acredita? Procura ele pra mim, nas dunas do leste.", "Do you? Find him for me, in the eastern dunes.", "¿Tú crees? Búscalo por mí, en las dunas del este.")
t("DLG_D_ROSA_WAIT", "Dunas altas, a leste da Rota 6. Ele usa um turbante cor de areia. Ou seja: boa sorte.",
  "High dunes, east of Route 6. He wears a sand-colored turban. In other words: good luck.",
  "Dunas altas, al este de la Ruta 6. Lleva un turbante color arena. O sea: buena suerte.")
t("DLG_D_ROSA_THANKS", "Ele disse que meu mapa tava certo? Ele disse isso? Vou emoldurar a frase.",
  "He said my map was right? He actually said that? I'm framing that sentence.", "¿Dijo que mi mapa tenía razón? ¿Dijo eso? Voy a enmarcar la frase.")
t("DLG_D_ROSA_REWARD", "Toma: duas velas de aniversário e o meu mapa das estrelas. Quem acha gente perdida merece.",
  "Here: two birthday candles and my star chart. Anyone who finds lost people deserves it.", "Toma: dos velas de cumpleaños y mi mapa de estrellas. Quien encuentra a los perdidos lo merece.")
t("DLG_D_ROSA_AFTER", "Mapa certo, marido errado. Mas é o meu marido errado.", "Right map, wrong husband. But he's my wrong husband.",
  "Mapa correcto, marido equivocado. Pero es mi marido equivocado.")
t("DLG_D_TAMARA_1", "No deserto, quem não troca de montaria morre de cansaço. Troca de esqueleto na hora certa, vamos ver!",
  "In the desert, whoever doesn't switch mounts drops from exhaustion. Switch skeletons at the right time, let's see!",
  "En el desierto, quien no cambia de montura cae de cansancio. ¡Cambia de esqueleto a tiempo, a ver!")
t("DLG_D_TAMARA_2", "Trocou no tempo certo. A rainha luta assim.", "You switched at the right time. The queen fights like that.", "Cambiaste en el momento justo. La reina pelea así.")
t("DLG_D_BATUQUE_1", "Proibiram o tambor. Não proibiram a batalha! Tum-tum-PÁ!", "They banned drums. They didn't ban battles! Boom-boom-BAP!",
  "Prohibieron el tambor. ¡No prohibieron las batallas! ¡Pum-pum-PAM!")
t("DLG_D_BATUQUE_2", "Perdemos no ritmo. Acontece.", "We lost the beat. It happens.", "Perdimos el ritmo. Pasa.")
t("OBJ_D_CAMPFIRE", "A fogueira estala. O céu do deserto tem mais estrelas do que você lembrava.", "The campfire crackles. The desert sky has more stars than you remember.",
  "La hoguera chisporrotea. El cielo del desierto tiene más estrellas de lo que recordabas.")
t("DLG_D_FIRE_L1", "Quando isso tudo acabar... você volta pra 2040?", "When all this is over... will you go back to 2040?", "Cuando todo esto termine... ¿volverás a 2040?")
t("DLG_D_FIRE_L2", "Se voltar, acende o farol de lá também. Aí eu vou saber que você chegou.", "If you do, light the lighthouse there too. Then I'll know you made it.",
  "Si vuelves, enciende también el faro de allá. Así sabré que llegaste.")
t("DLG_D_FIRE_T1", "Quando isso acabar... você vai embora?", "When this is over... are you leaving?", "Cuando esto termine... ¿te vas a ir?")
t("DLG_D_FIRE_T2", "...Tanto faz. Quer dizer. Não tanto faz.", "...Whatever. I mean. Not whatever.", "...Me da igual. Digo. No me da igual.")
R.d("placa_cidade", [say("SIGN_D_TOWN")])
R.d("placa_templo", [say("SIGN_D_TEMPLE")])
R.d("chegada_cidade", [lia("DLG_D_ARR_C_L"), taro("DLG_D_ARR_C_T"), flag("palmeiral_visto")])
R.d("fogueira", [say("OBJ_D_CAMPFIRE"), lia("DLG_D_FIRE_L1"), lia("DLG_D_FIRE_L2"), taro("DLG_D_FIRE_T1"), taro("DLG_D_FIRE_T2")])
R.d("moringa", [act("heal"), act("respawn"), {"say": "DLG_D_MORINGA_AFTER", "speaker": "SPK_MORINGA", "if": "duna_beaten"},
                {"say": "DLG_D_MORINGA_1", "speaker": "SPK_MORINGA", "if_not": "duna_beaten"},
                ask("DLG_D_MORINGA_2", "SPK_MORINGA", [("OPT_P_RANCH", "vila_mare/rancho"), ("OPT_P_LEAVE", None)])])
R.d("canela", [say("DLG_D_CANELA_1", "SPK_CANELA"), act("shop", id="palmeiral"), say("DLG_D_CANELA_2", "SPK_CANELA")])
R.d("grao", [{"say": "DLG_D_GRAO_AFTER", "speaker": "SPK_GRAO", "if": "duna_beaten"}, {"say": "DLG_D_GRAO", "speaker": "SPK_GRAO", "if_not": "duna_beaten"}])
R.d("miragem", [say("DLG_D_MIRAGEM_1", "SPK_MIRAGEM"), say("DLG_D_MIRAGEM_2", "SPK_MIRAGEM")])
R.d("rosa_pede", [say("DLG_D_ROSA_ASK", "SPK_ROSA"), say("DLG_D_ROSA_ASK2", "SPK_ROSA"), flag("rosa_quest")])
R.d("rosa_onde", [say("DLG_D_ROSA_WAIT", "SPK_ROSA")])
R.d("rosa_obrigada", [say("DLG_D_ROSA_THANKS", "SPK_ROSA"), say("DLG_D_ROSA_REWARD", "SPK_ROSA"), act("give_item", item="reviver", n=2),
                      act("give_item", item="pocao_g", n=2), flag("rosa_done")])
R.d("rosa_depois", [say("DLG_D_ROSA_AFTER", "SPK_ROSA")])
R.d("tamara", [say("DLG_D_TAMARA_1", "SPK_TAMARA"),
               battle("BTL_TAMER_TAMARA", team([("domador_escorpioes", 77), ("tamborileiro", 76)]), 940, "tamara_beaten", [["pocao_g", 2]]),
               say("DLG_D_TAMARA_2", "SPK_TAMARA")])
R.d("tamara_depois", [say("DLG_D_TAMARA_2", "SPK_TAMARA")])
R.d("batuque", [say("DLG_D_BATUQUE_1", "SPK_BATUQUE"),
                battle("BTL_TAMER_BATUQUE", team([("tamborileiro", 77), ("cartografo", 76)]), 960, "batuque_beaten", [["reviver", 2]]),
                say("DLG_D_BATUQUE_2", "SPK_BATUQUE")])
R.d("batuque_depois", [say("DLG_D_BATUQUE_2", "SPK_BATUQUE")])
R.NPCS["moringa"] = human("moringa", "SPK_MORINGA", [{"dialog": ref("moringa")}], role="ranch")
R.NPCS["canela"] = human("canela", "SPK_CANELA", [{"dialog": ref("canela")}], "stand", role="shop")
R.NPCS["grao"] = human("grao", "SPK_GRAO", [{"dialog": ref("grao")}], role="humor")
R.NPCS["miragem"] = human("miragem", "SPK_MIRAGEM", [{"dialog": ref("miragem")}], "stand", role="lore")
R.NPCS["rosa"] = human("rosa", "SPK_ROSA", [{"if": "rosa_done", "dialog": ref("rosa_depois")}, {"if_all": ["rosa_quest", "alforje_achado"], "dialog": ref("rosa_obrigada")},
                                           {"if": "rosa_quest", "dialog": ref("rosa_onde")}, {"dialog": ref("rosa_pede")}], "stand", role="quest")
R.tamer("tamara", "tamara", "SPK_TAMARA", "tamara", "tamara_beaten", 3)
R.tamer("batuque", "batuque", "SPK_BATUQUE", "batuque", "batuque_beaten", 3)

# ------------------------------------------------------------------ Templo das Areias: capanga, Ampulhor, Rainha Duna (pista 7)
t("DLG_D_ARR_T_L", "Que silêncio... Até meus passos têm medo de fazer barulho.", "So quiet... Even my footsteps are afraid to make noise.",
  "Qué silencio... Hasta mis pasos tienen miedo de hacer ruido.")
t("DLG_D_ARR_T_T", "Templo bonito. Bonito demais pra alguém triste morar.", "Pretty temple. Too pretty for someone sad to live in.",
  "Templo bonito. Demasiado bonito para que viva alguien triste.")
t("DLG_D_SAND_1", "A rainha não recebe ninguém. Eu recebo por ela. Com batalha.", "The queen receives no one. I receive them for her. With a battle.",
  "La reina no recibe a nadie. Yo recibo por ella. Con batalla.")
t("DLG_D_SAND_2", "Recebido. Pode passar. Tire as sandálias.", "Received. You may pass. Take off your sandals.", "Recibido. Puede pasar. Quítese las sandalias.")
t("DLG_D_AMP", "Um esqueleto-ampulheta conta grãos de areia. Perdeu a conta mil vezes e recomeçou mil e uma.",
  "An hourglass skeleton counts grains of sand. It has lost count a thousand times and started over a thousand and one.",
  "Un esqueleto-reloj de arena cuenta granos. Perdió la cuenta mil veces y empezó de nuevo mil y una.")
R.d("chegada_templo", [lia("DLG_D_ARR_T_L"), taro("DLG_D_ARR_T_T"), flag("templo_visto")])
R.d("sandalo", [say("DLG_D_SAND_1", "SPK_SANDALO"), battle("BTL_TAMER_SANDALO", team([("cartografo", 78), ("tamborileiro", 78)]), 980, "sandalo_beaten"),
                say("DLG_D_SAND_2", "SPK_SANDALO")])
R.d("sandalo_depois", [say("DLG_D_SAND_2", "SPK_SANDALO")])
R.tamer("sandalo", "sandalo", "SPK_SANDALO", "sandalo", "sandalo_beaten", 3)
R.d("ampulhor", [ask("DLG_D_AMP", None, [("OPT_D_HOURGLASS", ref("ampulhor_luta")), ("OPT_M_LEAVE", None)])])
R.d("ampulhor_luta", [battle("", [["ampulhor", 75]], 0, kind="wild")])
R.NPCS["ampulhor_npc"] = skel("skel_ampulhor", "SPECIES_AMPULHOR", [{"dialog": ref("ampulhor")}], role="wild")

t("DLG_D_DUNA_1", "Um herdeiro no meu deserto. Eu senti você chegando, como se sente a chuva.", "An heir in my desert. I felt you coming, the way one feels the rain.",
  "Un heredero en mi desierto. Te sentí llegar, como se siente la lluvia.")
t("DLG_D_DUNA_2", "Sou Duna, esposa do Rei. Ergui o farol para ele voltar pra casa. Ele voltou... e nunca mais saiu.",
  "I am Duna, the King's wife. I raised the lighthouse so he'd come home. He came back... and never left again.",
  "Soy Duna, esposa del Rey. Levanté el faro para que volviera a casa. Volvió... y nunca más salió.")
t("DLG_D_DUNA_3", "Se eu partir, ele fica sozinho de vez. Então eu fico. E você também fica, até me vencer.",
  "If I go, he'll be alone for good. So I stay. And you stay too, until you beat me.",
  "Si me voy, se quedará solo para siempre. Así que me quedo. Y tú también, hasta que me venzas.")
t("DLG_D_DUNA_WIN", "Você troca de lugar com os seus na hora certa. Como uma família.", "You swap places with your own at just the right moment. Like a family.",
  "Cambias de lugar con los tuyos en el momento justo. Como una familia.")
t("DLG_D_DUNA_WHY1", "Você precisa saber por que ele te chamou.", "You need to know why he called you.", "Necesitas saber por qué te llamó.")
t("DLG_D_DUNA_WHY2", "A coroa só se refaz na cabeça de alguém do sangue. E prende quem a usa no trono. Para sempre.",
  "The crown only mends itself on the head of someone of the blood. And it binds whoever wears it to the throne. Forever.",
  "La corona solo se repara en la cabeza de alguien de la sangre. Y ata a quien la lleva al trono. Para siempre.")
t("DLG_D_DUNA_WHY3", "Ele vai pedir que você a coloque. Não por crueldade. Ele só não aguenta perder a família de novo.",
  "He will ask you to put it on. Not out of cruelty. He simply can't bear to lose his family again.",
  "Te pedirá que te la pongas. No por crueldad. Simplemente no soporta perder otra vez a su familia.")
t("DLG_D_DUNA_L", "Ninguém devia ficar preso pra sempre. Nem você... nem o Rei.", "Nobody should be trapped forever. Not you... and not the King.",
  "Nadie debería quedar atrapado para siempre. Ni tú... ni el Rey.")
t("DLG_D_DUNA_T", "Se você colocar essa coroa, eu mesmo tiro ela da sua cabeça.", "If you put that crown on, I'll pull it off your head myself.",
  "Si te pones esa corona, yo mismo te la quito de la cabeza.")
t("DLG_D_DUNA_LETTER", "Você traz uma carta da nossa filha? ...Então ainda há esperança para ele.", "You carry a letter from our daughter? ...Then there's still hope for him.",
  "¿Traes una carta de nuestra hija? ...Entonces aún hay esperanza para él.")
t("DLG_D_DUNA_NOLETTER", "Você viu a Alva? Ela está bem? ...Que bom. Ela sempre esperou demais por ele.",
  "Did you see Alva? Is she well? ...Good. She has always waited too long for him.", "¿Viste a Alva? ¿Está bien? ...Qué bien. Siempre lo esperó demasiado.")
t("DLG_D_DUNA_STORM", "A tempestade vai baixar. O castelo fica ao norte. Cuida dele por mim, herdeiro. Mesmo que seja dizendo não.",
  "The storm will die down. The castle lies to the north. Look after him for me, heir. Even if it means saying no.",
  "La tormenta amainará. El castillo está al norte. Cuídalo por mí, heredero. Aunque sea diciéndole que no.")
t("DLG_D_DUNA_AFTER", "Os tambores voltaram. Ele vai ouvir lá do castelo. Talvez lembre de quando dançava.",
  "The drums are back. He'll hear them from the castle. Maybe he'll remember when he used to dance.",
  "Volvieron los tambores. Los oirá desde el castillo. Quizá recuerde cuando bailaba.")
DUNA_TEAM = team([("domador_escorpioes", 85), ("cartografo", 84), ("tamborileiro", 86), ("palafiteiro", 85)])
R.d("duna", [say("DLG_D_DUNA_1", "SPK_DUNA"), say("DLG_D_DUNA_2", "SPK_DUNA"), say("DLG_D_DUNA_3", "SPK_DUNA"),
             battle("BTL_TAMER_DUNA", DUNA_TEAM, 2200, "duna_beaten", kind="boss"),
             say("DLG_D_DUNA_WIN", "SPK_DUNA"), say("DLG_D_DUNA_WHY1", "SPK_DUNA"), say("DLG_D_DUNA_WHY2", "SPK_DUNA"), say("DLG_D_DUNA_WHY3", "SPK_DUNA"),
             flag("pista_7"), lia("DLG_D_DUNA_L"), taro("DLG_D_DUNA_T"),
             {"say": "DLG_D_DUNA_LETTER", "speaker": "SPK_DUNA", "if": "has_carta_alva"},
             {"say": "DLG_D_DUNA_NOLETTER", "speaker": "SPK_DUNA", "if_not": "has_carta_alva"},
             say("DLG_D_DUNA_STORM", "SPK_DUNA"), act("refresh_map")])
R.d("duna_depois", [say("DLG_D_DUNA_AFTER", "SPK_DUNA")])
R.NPCS["duna"] = {"name_key": "SPK_DUNA", "role": "guardian", "sprite": "res://assets/sprites/npc/skel_duna.png", "frames": 2, "idle_fps": 2.0,
                  "behavior": "stand", "dialog": [{"if": "duna_beaten", "dialog": ref("duna_depois")}, {"dialog": ref("duna")}],
                  "tamer": {"vision": 3, "flag": "duna_beaten"}}


# ------------------------------------------------------------------ encontros (balance.json: selvagens 67–73)
def e(sp, st, a, b, rar, w=None):
    d = {"species": sp, "stage": st, "min_level": a, "max_level": b, "rarity": rar}
    if w:
        d["weight"] = w
    return d


R.TABLES.update({
    "rota6_sul": [e("domador_escorpioes_3", 3, 68, 69, "comum"), e("palafiteiro_3", 3, 67, 69, "comum")],
    "rota6_oeste": [e("domador_escorpioes_3", 3, 68, 70, "comum"), e("escultor_3", 3, 68, 70, "incomum")],
    "rota6_campo": [e("domador_escorpioes_3", 3, 68, 70, "comum"), e("tamborileiro_3", 3, 68, 70, "incomum"), e("cartografo_3", 3, 70, 71, "raro"),
                    e("escultor_3", 3, 68, 70, "incomum"), e("palafiteiro_3", 3, 68, 70, "comum")],
    "rota6_eco": [e("cartografo_3", 3, 76, 77, "raro", 60), e("tamborileiro_3", 3, 76, 77, "incomum", 40)],
    "rota6_norte": [e("tamborileiro_3", 3, 70, 72, "incomum"), e("domador_escorpioes_3", 3, 70, 72, "comum")],
    "templo_salao": [e("domador_escorpioes_3", 3, 71, 73, "comum"), e("cartografo_3", 3, 71, 73, "raro"), e("tamborileiro_3", 3, 71, 73, "incomum")],
    "templo_sul": [e("cartografo_2", 2, 67, 69, "raro"), e("escultor_3", 3, 72, 73, "incomum")],
})
R.SHOPS["palmeiral"] = ["pocao_g", "antidoto", "reviver"]

# ------------------------------------------------------------------ mapas
LEG = {"g": "dune", "f": "sand", "B": "sandstone", "p": "path", ".": "floor"}
rota = make_route("rota_6", "deserto", "MAP_ROTA_6", LEG, ("geada", 19, 1), ("palmeiral", 19, 30),
                  tamers=[("corcova", {}), ("veu", {}), ("pa", {})], hint="cantil", sign=R.ref("placa_bifurcacao"),
                  spawns=[{"id": "r6_sul", "table": "rota6_sul", "x": 10, "y": 45, "radius": 3, "count": 2},
                          {"id": "r6_oeste", "table": "rota6_oeste", "x": 5, "y": 25, "radius": 2, "count": 1},
                          {"id": "r6_campo_a", "table": "rota6_campo", "x": 30, "y": 32, "radius": 4, "count": 3},
                          {"id": "r6_campo_b", "table": "rota6_campo", "x": 30, "y": 18, "radius": 4, "count": 3},
                          {"id": "r6_eco", "table": "rota6_eco", "x": 19, "y": 25, "radius": 2, "count": 1},
                          {"id": "r6_norte", "table": "rota6_norte", "x": 10, "y": 6, "radius": 3, "count": 2}],
                  extra_npcs=[{"id": "alforje", "x": 36, "y": 24, "facing": "left"}],
                  extra_props=[{"type": "broken_column", "x": 18, "y": 36}, {"type": "broken_column", "x": 21, "y": 36},
                               {"type": "broken_column", "x": 18, "y": 13}, {"type": "broken_column", "x": 21, "y": 13},
                               {"type": "cactus", "x": 28, "y": 20}, {"type": "drum", "x": 35, "y": 25}],
                  deco=("cactus", "rock_small", "broken_column", "palm"), tint=[1.0, 0.96, 0.9], seed=101)
rota["on_enter"] = [{"if_not": "rota6_vista", "dialog": R.ref("chegada_rota")}]
rota["ambient"] = ["sand"]

town = make_town("palmeiral", "deserto", "MAP_PALMEIRAL", {"g": "sand", "p": "path", "B": "sandstone", "s": "path", "f": "dune"},
                 south=("rota_6", 19, 1), north=("castelo_portao", 19, 28), west=("templo_areias", 32, 10),
                 houses=["tent_ranch", "tent_shop", "tent", "tent", "tent"],
                 npcs=[{"id": "grao", "x": 16, "y": 16, "facing": "right"}, {"id": "miragem", "x": 24, "y": 18, "facing": "left"},
                       ],
                 props=[{"type": "sign", "x": 18, "y": 28, "dialog": R.ref("placa_cidade")}, {"type": "sign", "x": 3, "y": 14, "dialog": R.ref("placa_templo")},
                        {"type": "oasis_pool", "x": 20, "y": 16}, {"type": "palm", "x": 16, "y": 13}, {"type": "palm", "x": 24, "y": 15},
                        {"type": "campfire", "x": 22, "y": 19, "dialog": R.ref("fogueira")}, {"type": "drum", "x": 13, "y": 14}, {"type": "drum", "x": 26, "y": 17},
                        {"type": "well", "x": 28, "y": 24}],
                 deco=("palm", "cactus", "rock_small"), tint=[1.0, 0.97, 0.9], seed=111, plaza="s")
for w in town["warps"]:
    if w["to"] == "castelo_portao":
        w["if"] = "duna_beaten"
        w["locked_message"] = "MSG_STORM_ROAD"
town["on_enter"] = [{"if_not": "palmeiral_visto", "dialog": R.ref("chegada_cidade")}]
town["ambient"] = ["sand"]
town_doors(town, "palmeiral", {"rancho": "palmeiral_rancho", "loja": "palmeiral_loja", "a": "palmeiral_casa_tamara", "b": "palmeiral_casa_batuque",
                               "c": "palmeiral_casa_rosa"})

lair = make_lair("templo_areias", "deserto", "MAP_TEMPLO", {"g": "sand", "p": "path", "B": "sandstone", "f": "carpet"}, east=("palmeiral", 1, 15),
                 guardian_npc={"id": "duna", "x": 10, "y": 3, "facing": "down"},
                 extra_npcs=[{"id": "sandalo", "x": 14, "y": 10, "facing": "right"}, {"id": "ampulhor_npc", "x": 9, "y": 15, "facing": "left"}],
                 props=[{"type": "broken_column", "x": 4, "y": 2}, {"type": "broken_column", "x": 16, "y": 2}, {"type": "hourglass", "x": 7, "y": 2},
                        {"type": "hourglass", "x": 13, "y": 2}, {"type": "torch", "x": 18, "y": 8}, {"type": "torch", "x": 28, "y": 8},
                        {"type": "drum", "x": 22, "y": 13}, {"type": "cactus", "x": 4, "y": 19}, {"type": "broken_column", "x": 12, "y": 18}],
                 spawns=[{"id": "t_salao", "table": "templo_salao", "x": 23, "y": 10, "radius": 3, "count": 2},
                         {"id": "t_sul", "table": "templo_sul", "x": 6, "y": 15, "radius": 2, "count": 1}],
                 tint=[1.0, 0.92, 0.84])
lair["on_enter"] = [{"if_not": "templo_visto", "dialog": R.ref("chegada_templo")}]
lair["ambient"] = ["sand"]

R.MAPS.update({
    "rota_6": rota, "palmeiral": town, "templo_areias": lair,
    "palmeiral_rancho": room("palmeiral_rancho", "deserto", "MAP_PALMEIRAL_RANCHO", "palmeiral", (12, 10),
                             [{"type": "bed", "x": 2, "y": 3}, {"type": "bed", "x": 4, "y": 3}, {"type": "plant", "x": 10, "y": 2}, {"type": "rug", "x": 6, "y": 6}],
                             [{"id": "moringa", "x": 7, "y": 3, "facing": "down"}], floor="sand", wall="sandstone", top="sandstone"),
    "palmeiral_loja": room("palmeiral_loja", "deserto", "MAP_PALMEIRAL_LOJA", "palmeiral", (27, 10),
                           [{"type": "stall", "x": 4, "y": 3}, {"type": "barrel", "x": 10, "y": 2}, {"type": "crate", "x": 10, "y": 7}],
                           [{"id": "canela", "x": 6, "y": 4, "facing": "down"}], floor="sand", wall="sandstone", top="sandstone"),
    "palmeiral_casa_tamara": room("palmeiral_casa_tamara", "deserto", "MAP_PALMEIRAL_CASA_TAMARA", "palmeiral", (8, 20),
                                  [{"type": "rug", "x": 6, "y": 6}, {"type": "barrel", "x": 10, "y": 7}],
                                  [{"id": "tamara", "x": 6, "y": 3, "facing": "down"}], floor="sand", wall="sandstone", top="sandstone"),
    "palmeiral_casa_batuque": room("palmeiral_casa_batuque", "deserto", "MAP_PALMEIRAL_CASA_BATUQUE", "palmeiral", (31, 20),
                                   [{"type": "drum", "x": 3, "y": 4}, {"type": "drum", "x": 9, "y": 4}, {"type": "drum", "x": 3, "y": 7}],
                                   [{"id": "batuque", "x": 6, "y": 3, "facing": "down"}], floor="sand", wall="sandstone", top="sandstone"),
    "palmeiral_casa_rosa": room("palmeiral_casa_rosa", "deserto", "MAP_PALMEIRAL_CASA_ROSA", "palmeiral", (14, 27),
                                [{"type": "map_board", "x": 9, "y": 2}, {"type": "table", "x": 4, "y": 5}, {"type": "stool", "x": 3, "y": 6}],
                                [{"id": "rosa", "x": 6, "y": 3, "facing": "down"}], floor="sand", wall="sandstone", top="sandstone"),
})
R.BATTLE_BG["deserto"] = "res://assets/battle/bg_deserto.png"
R.CITIES.append({"id": "palmeiral", "map": "palmeiral", "ranch": "moringa", "shop": "palmeiral", "tamer_houses": ["tamara", "batuque"],
                 "npcs": ["grao", "miragem", "rosa"], "quests": ["rosa"]})
R.ROUTES.append({"id": "rota_6", "map": "rota_6", "from": "geada", "to": "palmeiral",
                 "paths": [{"kind": "domadores", "required": False}, {"kind": "selvagem", "required": False},
                           {"kind": "atalho", "required": False, "note": "Passagem do Eco: curta, com um selvagem forte"}]})

# ------------------------------------------------------------------ documento
R.DOC = {
    "title": "Ato 6: Rota 6 e Deserto dos Ecos", "phase": "4g", "duration": "25 min",
    "ages": "chegada 68–76; selvagens 67–73; domadores 72–78; Guardiã ~85 (protótipo do balance.json)",
    "problem": "A Guardiã **Rainha Duna** ergueu uma **tempestade de areia sem fim** ao redor do castelo, para que ninguém incomode o marido em luto, "
               "e mandou calar os **tambores** que guiavam as caravanas pelas dunas. Sem os tambores, as caravanas se perdem seguindo o próprio eco: "
               "**Palmeiral** está sem comércio, e a Cartógrafa Rosa perdeu o marido na Rota 6.",
    "clue_n": 7,
    "clue": "Depois da luta, a Rainha Duna conta **para que** o Rei chamou o herdeiro: a coroa só se refaz na cabeça de alguém do sangue, "
            "e prende quem a usa no trono **para sempre**. Ele vai pedir que o protagonista a coloque, não por crueldade, mas por medo de perder a família de novo. "
            "É o dilema do final.",
    "moment": ["**Fogueira em Palmeiral** (cena opcional, a qualquer momento): Lia pergunta se o protagonista volta para 2040 e pede que ele acenda \"o farol de lá também\"; "
               "Taro pergunta se ele vai embora e quase admite que se importa (\"Não tanto faz\").",
               "Depois da revelação da Duna: Lia (\"Ninguém devia ficar preso pra sempre. Nem o Rei\") e Taro (\"Eu mesmo tiro essa coroa da sua cabeça\").",
               "Arcos: Lia já pensa na luz para os outros (até para o Rei); Taro já protege alguém além dos pais."],
    "guardian": {"name": "Rainha Duna (esposa do Rei, mãe da Alva)", "kin": "esposa",
                 "personality": "sábia, cansada, gentil; fala com imagens da natureza (chuva, areia, estrelas)",
                 "motive": "**Amor:** se ela partir, ele fica sozinho de vez. Foi ela quem ergueu o farol para ele voltar para casa.",
                 "mechanic": "**Resistência.** A equipe troca de lugar e cura em grupo; quem cai na timeline é substituído por um aliado descansado. "
                             "Ensina a **gerir a equipe** e a **trocar na hora certa**. A Cameleira Tâmara e o Velho Cantil preparam.",
                 "team": "Aguilhão 85, Astrolar 84, Ecoarca 86, Palafitor 85.",
                 "reward": "2200 moedas; a tempestade baixa e a estrada do castelo aparece."},
    "maps": [("**Rota 6** (`rota_6`)", "Mar de dunas. 3 caminhos: **Caravanas** (oeste: Corcova, Véu, Pá), **Dunas Altas** (leste, com o Seu Alforje perdido) e "
              "**Passagem do Eco** (centro, curta, com um selvagem forte). Placa e o Velho Cantil dão a dica."),
             ("**Palmeiral** (`palmeiral`)", "Oásis de tendas: Rancho (Moringa), Tenda da Canela, tendas da Tâmara e dos Batuque, tenda da Cartógrafa, "
              "lago, palmeiras, tambores calados e a fogueira da cena do parceiro."),
             ("**Templo das Areias** (`templo_areias`)", "Camareiro Sândalo, o único **Ampulhor** ao sul e a Rainha Duna."),
             ("Interiores", "Rancho da Moringa, Tenda da Canela, tendas da Tâmara, dos Batuque e da Cartógrafa.")],
}
R.NPC_DOC = [
    ("Velho Cantil", "dica", "Explica os 3 caminhos e o silêncio dos tambores"),
    ("Corcova, Véu, Pá", "domadores da rota", "Caminho das Caravanas"),
    ("Seu Alforje", "missão (perdido)", "O marido da Rosa, perdido nas dunas: missão de encontrar alguém, não um objeto"),
    ("Dona Moringa", "Rancho", "Cura; muda quando os tambores voltam"),
    ("Mercadora Canela", "Loja", "Preço \"da saudade\": o comércio parado"),
    ("Grão", "humor", "Conta grãos de areia; depois vê o castelo"),
    ("Vó Miragem", "lore", "Por que a rainha ergueu a tempestade: amor"),
    ("Cartógrafa Rosa", "missão", "Pede para achar o marido; o mapa dela estava certo"),
    ("Camareiro Sândalo", "capanga", "Guarda o templo"),
    ("Rainha Duna", "Guardiã", "Resistência; pista 7 (para que o Rei quer o herdeiro)"),
]
R.HOUSES = [
    ("Cameleira Tâmara", "Trocas no tempo certo (Aguilhão + Ecoarca)", "940 moedas + 2 Fatias de Bolo"),
    ("Irmãos Batuque", "Cura em grupo e ritmo (Ecoarca + Astrolar)", "960 moedas + 2 Vela de Aniversário"),
]
R.CHOICES = [
    ("Caminho da Rota 6", "Caravanas / Dunas Altas / Passagem do Eco", "Moedas e itens / XP, marcadores e a missão do Alforje / curto, com um selvagem forte"),
    ("Missão da caravana", "Fazer / ignorar", "2 Vela de Aniversário + 2 Fatias de Bolo"),
    ("Carta da Alva (escolha 5)", "—", "Se o jogador a carrega, a Duna reage com esperança (prévia do Final A)"),
]

if __name__ == "__main__":
    R.write()
