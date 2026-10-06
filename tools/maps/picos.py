#!/usr/bin/env python3
"""Ato 5 — Rota 5 e Picos Gelados (fase 4f). Fonte única: gera
docs/roteiro/06_picos.md, falas (PT/EN/ES), NPCs, encontros, loja, itens e mapas
(Rota 5, Geada e interiores, Mosteiro do Eco, Jardim de Gelo)."""
from regionkit import (Region, make_lair, make_route, make_town, room, town_doors, team,
                       say, ask, battle, act, flag, goto, human, skel)

R = Region("picos", 6, "picos", ["picos"])
t = R.t
ref = R.ref


def lia(k):
    return say(k, "SPK_LIA") | {"if": "partner_lia"}


def taro(k):
    return say(k, "SPK_TARO") | {"if": "partner_taro"}


# ------------------------------------------------------------------ nomes
for k, pt, en, es in [
        ("TRENO", "Guia Trenó", "Guide Sled", "Guía Trineo"), ("GRAMPO", "Alpinista Grampo", "Climber Piton", "Alpinista Clavija"),
        ("RAJADA", "Rajada", "Gust", "Ráfaga"), ("BRISA", "Monja Brisa", "Sister Breeze", "Monja Brisa"),
        ("LAREIRA", "Dona Lareira", "Mrs. Hearth", "Doña Hoguera"), ("CACHECOL", "Seu Cachecol", "Mr. Muffler", "Don Bufanda"),
        ("LAMINA", "Patinadora Lâmina", "Skater Blade", "Patinadora Cuchilla"), ("GRANIZO", "Irmãos Granizo", "Hail Brothers", "Hermanos Granizo"),
        ("FLOQUINHO", "Floquinho", "Flurry", "Copito"), ("CAMELIA", "Camélia", "Camellia", "Camelia"),
        ("PINHAO", "Vô Pinhão", "Grandpa Pinecone", "Abuelo Piñón"), ("DEGELO", "Degelo", "Thaw", "Deshielo"),
        ("PINGENTE", "Guarda Pingente", "Guard Icicle", "Guardia Carámbano"), ("LEAL", "Guarda Leal", "Loyal Guard", "Guardia Leal"),
        ("NEVASCO", "Nevasco", "Nevasco", "Nevasco"), ("ALVA", "Alva", "Alva", "Alva")]:
    t(f"SPK_{k}", pt, en, es)
for k in ("GRAMPO", "RAJADA", "BRISA", "LAMINA", "GRANIZO", "PINGENTE", "LEAL"):
    pt, en, es = R.T[f"SPK_{k}"]
    t(f"BTL_TAMER_{k}", pt, en, es)
t("BTL_TAMER_ALVA", "Guardiã Alva", "Guardian Alva", "Guardiana Alva")
t("MAP_ROTA_5", "Rota 5 — Trilha da Nevasca", "Route 5 — Blizzard Trail", "Ruta 5 — Sendero de la Ventisca")
t("MAP_GEADA", "Geada", "Frostholm", "Escarcha")
t("MAP_JARDIM_GELO", "Jardim de Gelo", "Ice Garden", "Jardín de Hielo")
t("MAP_GEADA_RANCHO", "Rancho da Lareira", "Hearth's Ranch", "Rancho de Hoguera")
t("MAP_GEADA_LOJA", "Armarinho do Cachecol", "Muffler's Goods", "Mercería de Bufanda")
t("MAP_GEADA_CASA_LAMINA", "Casa da Patinadora Lâmina", "Skater Blade's House", "Casa de la Patinadora Cuchilla")
t("MAP_GEADA_CASA_GRANIZO", "Casa dos Irmãos Granizo", "Hail Brothers' House", "Casa de los Hermanos Granizo")
t("MAP_MOSTEIRO", "Mosteiro do Eco", "Monastery of the Echo", "Monasterio del Eco")
t("MSG_ALVA_ROAD", "Uma parede de gelo fecha a descida para o deserto.", "A wall of ice blocks the way down to the desert.",
  "Un muro de hielo cierra la bajada al desierto.")
t("ITEM_LETTER", "Carta da Alva", "Alva's Letter", "Carta de Alva")
t("ITEM_LETTER_TEXT", "Uma carta lacrada, endereçada \"ao meu pai\". A letra treme um pouco.", "A sealed letter addressed \"to my father\". The handwriting trembles a little.",
  "Una carta sellada, dirigida \"a mi padre\". La letra tiembla un poco.")
t("ITEM_SPROUT", "Broto de Chá", "Tea Sprout", "Brote de Té")
t("ITEM_SPROUT_TEXT", "Um broto verde que sobreviveu debaixo do gelo. A Camélia quer plantar.", "A green sprout that survived under the ice. Camellia wants to plant it.",
  "Un brote verde que sobrevivió bajo el hielo. Camelia quiere plantarlo.")
R.ITEMS["carta_alva"] = {"name_key": "ITEM_LETTER", "desc_key": "ITEM_LETTER_TEXT", "kind": "key", "price": 0, "battle": False, "target": "none"}
R.ITEMS["broto_cha"] = {"name_key": "ITEM_SPROUT", "desc_key": "ITEM_SPROUT_TEXT", "kind": "key", "price": 0, "battle": False, "target": "none"}
t("OPT_PI_TAKE", "Levar a carta", "Take the letter", "Llevar la carta")
t("OPT_PI_LEAVE", "Não levar", "Don't take it", "No llevarla")
t("OPT_PI_DUEL", "Aceitar o desafio", "Accept the challenge", "Aceptar el desafío")

# ------------------------------------------------------------------ Rota 5
t("SIGN_PI_FORK", "← Trilha dos Alpinistas · ↑ Ponte de Gelo · → Campo Branco",
  "← Climbers' Trail · ↑ Ice Bridge · → White Field", "← Sendero de Alpinistas · ↑ Puente de Hielo · → Campo Blanco")
t("DLG_PI_ARR_R_L", "Neve! Ela cai devagar, como se tivesse medo de chegar no chão.", "Snow! It falls so slowly, like it's afraid of reaching the ground.",
  "¡Nieve! Cae despacito, como si le diera miedo llegar al suelo.")
t("DLG_PI_ARR_R_T", "Frio. Meu pai dizia que frio é só vento sem educação.", "Cold. My dad used to say cold is just wind with no manners.",
  "Frío. Mi papá decía que el frío es solo viento sin modales.")
t("DLG_PI_TRENO_1", "Pelos alpinistas tem briga, pelo campo branco tem bicho, e a Ponte de Gelo... range. Muito.",
  "The climbers' trail has fights, the white field has critters, and the Ice Bridge... creaks. A lot.",
  "Por los alpinistas hay pelea, por el campo blanco hay bichos, y el Puente de Hielo... cruje. Mucho.")
t("DLG_PI_TRENO_2", "Antes eu descia com chá pras cidades. Agora o gelo não deixa nem o trenó sair.", "I used to sled tea down to the towns. Now the ice won't even let the sled leave.",
  "Antes bajaba té a los pueblos. Ahora el hielo no deja salir ni al trineo.")
t("DLG_PI_GRAMPO_1", "Escalei três picos esta semana. Falta escalar você!", "I climbed three peaks this week. You're next!", "Escalé tres picos esta semana. ¡Me faltas tú!")
t("DLG_PI_GRAMPO_2", "Escorreguei. Acontece até com quem tem grampo.", "I slipped. Happens even to people with pitons.", "Me resbalé. Les pasa hasta a los que llevan clavijas.")
t("DLG_PI_RAJADA_1", "Eu corro mais que o vento! Meus esqueletos também. Tenta acompanhar!", "I run faster than the wind! So do my skeletons. Try to keep up!",
  "¡Corro más que el viento! Mis esqueletos también. ¡Intenta seguirnos!")
t("DLG_PI_RAJADA_2", "Você leu a timeline. Que falta de educação com o vento.", "You read the timeline. How rude to the wind.", "Leíste la línea de turnos. Qué falta de respeto al viento.")
t("DLG_PI_BRISA_1", "Medito na neve há vinte anos. Hoje vou meditar batalhando.", "I've meditated in the snow for twenty years. Today I'll meditate by battling.",
  "Medito en la nieve desde hace veinte años. Hoy meditaré peleando.")
t("DLG_PI_BRISA_2", "Perder também é um caminho. Um caminho frio, mas é.", "Losing is also a path. A cold one, but a path.", "Perder también es un camino. Uno frío, pero lo es.")
t("DLG_PI_LEAL_1", "O Rei procura o herdeiro? Então o herdeiro não sobe a serra!", "The King is looking for his heir? Then the heir doesn't climb this mountain!",
  "¿El Rey busca a su heredero? ¡Entonces el heredero no sube la sierra!")
t("DLG_PI_LEAL_2", "Ossório falou demais. A gente ouviu tudo. Alto lá!", "Ossório talked too much. We heard everything. Halt!", "Ossório habló de más. Lo oímos todo. ¡Alto ahí!")
t("DLG_PI_LEAL_AFTER", "Lealdade não esquenta ninguém nesse frio. Pode passar.", "Loyalty doesn't keep anyone warm in this cold. Go on.",
  "La lealtad no calienta a nadie con este frío. Pasa.")

R.d("placa_bifurcacao", [say("SIGN_PI_FORK")])
R.d("chegada_rota", [lia("DLG_PI_ARR_R_L"), taro("DLG_PI_ARR_R_T"), flag("rota5_vista")])
R.d("treno", [say("DLG_PI_TRENO_1", "SPK_TRENO"), say("DLG_PI_TRENO_2", "SPK_TRENO")])
R.d("grampo", [say("DLG_PI_GRAMPO_1", "SPK_GRAMPO"), battle("BTL_TAMER_GRAMPO", team([("carregador", 60), ("mineiro", 60)]), 760, "grampo_beaten"),
               say("DLG_PI_GRAMPO_2", "SPK_GRAMPO")])
R.d("grampo_depois", [say("DLG_PI_GRAMPO_2", "SPK_GRAMPO")])
R.d("rajada", [say("DLG_PI_RAJADA_1", "SPK_RAJADA"), battle("BTL_TAMER_RAJADA", team([("escultor", 61), ("sineiro", 61)]), 780, "rajada_beaten"),
               say("DLG_PI_RAJADA_2", "SPK_RAJADA")])
R.d("rajada_depois", [say("DLG_PI_RAJADA_2", "SPK_RAJADA")])
R.d("brisa", [say("DLG_PI_BRISA_1", "SPK_BRISA"),
              battle("BTL_TAMER_BRISA", team([("chazeiro", 62), ("carregador", 62)]), 800, "brisa_beaten", [["pocao_g", 1]]),
              say("DLG_PI_BRISA_2", "SPK_BRISA")])
R.d("brisa_depois", [say("DLG_PI_BRISA_2", "SPK_BRISA")])
R.d("leal_a", [say("DLG_PI_LEAL_1", "SPK_LEAL"), battle("BTL_TAMER_LEAL", team([("sentinela", 63), ("escriba", 62)]), 600, "leal_a_beaten"),
               say("DLG_PI_LEAL_AFTER", "SPK_LEAL")])
R.d("leal_a_depois", [say("DLG_PI_LEAL_AFTER", "SPK_LEAL")])
R.d("leal_b", [say("DLG_PI_LEAL_2", "SPK_LEAL"), battle("BTL_TAMER_LEAL", team([("ferreiro", 63), ("sentinela", 63)]), 600, "leal_b_beaten"),
               say("DLG_PI_LEAL_AFTER", "SPK_LEAL")])
R.d("leal_b_depois", [say("DLG_PI_LEAL_AFTER", "SPK_LEAL")])
R.NPCS["treno"] = human("treno", "SPK_TRENO", [{"dialog": ref("treno")}])
R.tamer("grampo", "grampo", "SPK_GRAMPO", "grampo", "grampo_beaten")
R.tamer("rajada", "rajada", "SPK_RAJADA", "rajada", "rajada_beaten")
R.tamer("brisa", "brisa", "SPK_BRISA", "brisa", "brisa_beaten", 3)
R.tamer("leal_a", "elmo", "SPK_LEAL", "leal_a", "leal_a_beaten", 4)
R.tamer("leal_b", "grade", "SPK_LEAL", "leal_b", "leal_b_beaten", 4)

# reencontro com o recorrente (batalha opcional + o momento do arco)
t("DLG_PI_RT_1", "Você de novo. Ótimo. Tô precisando bater em alguém.", "You again. Great. I need to hit something.", "Tú otra vez. Genial. Necesito golpear a alguien.")
t("DLG_PI_RT_2", "...Desculpa. Não é com você.", "...Sorry. It's not about you.", "...Perdón. No es contigo.")
t("DLG_PI_RT_3", "Eu tenho medo. De chegar no castelo e meus pais não lembrarem de mim.", "I'm scared. Of reaching the castle and my parents not remembering me.",
  "Tengo miedo. De llegar al castillo y que mis padres no me recuerden.")
t("DLG_PI_RT_L", "Eles vão lembrar, Taro. Ninguém esquece quem faz falta.", "They'll remember, Taro. Nobody forgets someone they miss.",
  "Te recordarán, Taro. Nadie olvida a quien le hace falta.")
t("DLG_PI_RT_4", "...Vê se não se perde, então. A gente se vê no castelo.", "...Don't get lost, then. See you at the castle.", "...No te pierdas, entonces. Nos vemos en el castillo.")
t("DLG_PI_RL_1", "Achei vocês! Nessa nevasca, a única coisa que dava pra ver era a minha lamparina.", "Found you! In this blizzard, the only thing you could see was my lamp.",
  "¡Los encontré! Con esta ventisca, lo único que se veía era mi farolillo.")
t("DLG_PI_RL_2", "Quando a neve fecha tudo, não olha pra neve. Olha pra luz. É só seguir a luz.",
  "When the snow closes everything in, don't look at the snow. Look at the light. Just follow the light.",
  "Cuando la nieve lo cierra todo, no mires la nieve. Mira la luz. Solo sigue la luz.")
t("DLG_PI_RL_T", "...Isso foi bonito, Lia. Não conta pra ninguém que eu disse.", "...That was nice, Lia. Don't tell anyone I said so.",
  "...Eso fue bonito, Lia. No le digas a nadie que lo dije.")
t("DLG_PI_RL_3", "Agora eu vou pro farol. Quando vocês voltarem, ele vai estar aceso!", "Now I'm heading to the lighthouse. When you come back, it'll be lit!",
  "Ahora me voy al faro. ¡Cuando vuelvan, estará encendido!")
t("DLG_PI_RL_PRE", "Antes de ir: uma batalha, pra eu saber que vocês aguentam o frio!", "Before you go: a battle, so I know you can handle the cold!",
  "Antes de irte: una batalla, ¡para saber que aguantan el frío!")
t("DLG_PI_RT_PRE", "Luta comigo. Agora. Ou só me escuta, tanto faz.", "Fight me. Now. Or just listen, whatever.", "Pelea conmigo. Ahora. O solo escúchame, da igual.")
R.d("rival_taro", [say("DLG_PI_RT_1", "SPK_TARO"), ask("DLG_PI_RT_PRE", "SPK_TARO", [("OPT_P_FIGHT", ref("rival_taro_luta")), ("OPT_P_NOT_NOW", ref("rival_taro_fala"))])])
R.d("rival_taro_luta", [battle("BTL_TAMER_TARO", team([("grumete", 66), ("carregador", 65)]), 900, "rival_picos_done", marker={"species": "grumete_3", "amount": 10}),
                        goto(ref("rival_taro_fala"))])
R.d("rival_taro_fala", [say("DLG_PI_RT_2", "SPK_TARO"), say("DLG_PI_RT_3", "SPK_TARO"), say("DLG_PI_RT_L", "SPK_LIA"), say("DLG_PI_RT_4", "SPK_TARO"),
                        flag("rival_picos_done"), act("hide_npc", id="rival_taro_p")])
R.d("rival_lia", [say("DLG_PI_RL_1", "SPK_LIA"), ask("DLG_PI_RL_PRE", "SPK_LIA", [("OPT_P_FIGHT", ref("rival_lia_luta")), ("OPT_P_NOT_NOW", ref("rival_lia_fala"))])])
R.d("rival_lia_luta", [battle("BTL_TAMER_LIA", team([("faroleira", 66), ("escultor", 65)]), 900, "rival_picos_done", marker={"species": "faroleira_3", "amount": 10}),
                       goto(ref("rival_lia_fala"))])
R.d("rival_lia_fala", [say("DLG_PI_RL_2", "SPK_LIA"), say("DLG_PI_RL_T", "SPK_TARO"), say("DLG_PI_RL_3", "SPK_LIA"),
                       flag("rival_picos_done"), act("hide_npc", id="rival_lia_p")])
R.NPCS["rival_taro_p"] = skel("skel_grumete_3", "SPK_TARO", [{"dialog": ref("rival_taro")}])
R.NPCS["rival_lia_p"] = skel("skel_faroleira_3", "SPK_LIA", [{"dialog": ref("rival_lia")}])

# ------------------------------------------------------------------ Geada
t("SIGN_PI_TOWN", "Geada. Chá quente, gente quente, todo o resto congelado.", "Frostholm. Hot tea, warm people, everything else frozen.",
  "Escarcha. Té caliente, gente cálida, todo lo demás congelado.")
t("SIGN_PI_GARDEN", "← Jardim de Gelo. A princesa não recebe visitas.", "← Ice Garden. The princess receives no visitors.",
  "← Jardín de Hielo. La princesa no recibe visitas.")
t("OBJ_PI_SNOWMAN", "Um boneco de neve com cachecol. Alguém escreveu na barriga: \"Prefeito\".", "A snowman with a scarf. Someone wrote \"Mayor\" on its belly.",
  "Un muñeco de nieve con bufanda. Alguien escribió en la barriga: \"Alcalde\".")
t("DLG_PI_ARR_C_L", "Fumaça nas chaminés! Pelo menos aqui dentro tem calor.", "Smoke from the chimneys! At least it's warm in here.",
  "¡Humo en las chimeneas! Al menos aquí dentro hace calor.")
t("DLG_PI_ARR_C_T", "O gelo parou tudo. Até o tempo, parece.", "The ice stopped everything. Even time, it seems.", "El hielo paró todo. Hasta el tiempo, parece.")
t("DLG_PI_LAREIRA_1", "Entra, entra, antes que a porta congele aberta. Tem sopa e cama pros seus esqueletos.",
  "Come in, come in, before the door freezes open. There's soup and beds for your skeletons.",
  "Pasa, pasa, antes de que la puerta se congele abierta. Hay sopa y camas para tus esqueletos.")
t("DLG_PI_LAREIRA_2", "Faz um ano que é inverno. Desde que a princesa Alva chegou triste no jardim.",
  "It's been winter for a year. Ever since Princess Alva arrived sad in the garden.", "Hace un año que es invierno. Desde que la princesa Alva llegó triste al jardín.")
t("DLG_PI_LAREIRA_3", "Quer guardar alguém no Rancho? Aqui ninguém passa frio, prometo.", "Want to leave someone at the Ranch? Nobody gets cold here, I promise.",
  "¿Quieres dejar a alguien en el Rancho? Aquí nadie pasa frío, lo prometo.")
t("DLG_PI_LAREIRA_AFTER", "Ouviu? Goteira! Nunca fiquei tão feliz com uma goteira.", "Hear that? A leak! I've never been so happy about a leak.",
  "¿Oíste? ¡Una gotera! Nunca me alegró tanto una gotera.")
t("DLG_PI_CACHECOL_1", "Cachecol, luva, gorro. E caldo quente, claro. Frio não mata, mas cansa.", "Scarves, gloves, hats. And hot broth, of course. Cold doesn't hurt, but it wears you out.",
  "Bufanda, guantes, gorro. Y caldo caliente, claro. El frío no duele, pero cansa.")
t("DLG_PI_CACHECOL_2", "Volta logo. E fecha a porta!", "Come back soon. And close the door!", "Vuelve pronto. ¡Y cierra la puerta!")
t("DLG_PI_FLOQUINHO", "Eu fiz um boneco de neve e chamei de Prefeito. Ele manda melhor que o de verdade.",
  "I built a snowman and named it Mayor. It does a better job than the real one.", "Hice un muñeco de nieve y lo llamé Alcalde. Manda mejor que el de verdad.")
t("DLG_PI_FLOQUINHO_AFTER", "O Prefeito tá derretendo! Vou ter que fazer eleição.", "The Mayor is melting! I'll have to hold an election.",
  "¡El Alcalde se está derritiendo! Voy a tener que convocar elecciones.")
t("DLG_PI_PINHAO_1", "A Alva é filha do Rei. Quando menina, descia a serra pra brincar com as crianças daqui.",
  "Alva is the King's daughter. As a girl, she'd come down the mountain to play with the kids here.",
  "Alva es hija del Rey. De niña, bajaba la sierra a jugar con los niños de aquí.")
t("DLG_PI_PINHAO_2", "Ela não é má. Tá triste. E tristeza de princesa vira inverno.", "She isn't wicked. She's sad. And a princess's sadness turns into winter.",
  "No es mala. Está triste. Y la tristeza de una princesa se vuelve invierno.")
t("DLG_PI_DEGELO_1", "A equipe da Alva é rápida e congela. Esqueleto congelado anda devagar na fila.",
  "Alva's team is fast and freezes. A frozen skeleton moves slowly in the turn order.", "El equipo de Alva es rápido y congela. Un esqueleto congelado avanza despacio en la fila.")
t("DLG_PI_DEGELO_2", "Leva quem aguenta pancada e golpe pesado que vale a espera. Correr atrás do vento não dá.",
  "Bring someone sturdy and heavy moves worth the wait. You can't outrun the wind.", "Lleva a quien aguante golpes y golpes pesados que valgan la espera. Al viento no se le gana corriendo.")
t("DLG_PI_CAMELIA_ASK", "Minha horta de chá congelou inteira. Dizem que no Jardim de Gelo ainda tem um broto vivo.",
  "My whole tea garden froze. They say there's still a living sprout in the Ice Garden.", "Mi huerta de té se congeló entera. Dicen que en el Jardín de Hielo aún queda un brote vivo.")
t("DLG_PI_CAMELIA_ASK2", "Traz pra mim? Com um broto eu começo tudo de novo.", "Would you bring it to me? With one sprout I can start over.",
  "¿Me lo traes? Con un brote vuelvo a empezar.")
t("DLG_PI_CAMELIA_WHERE", "No canto sul do Jardim de Gelo. É verdinho, não tem erro.", "In the south corner of the Ice Garden. It's bright green, you can't miss it.",
  "En la esquina sur del Jardín de Hielo. Es verdecito, no tiene pérdida.")
t("OBJ_PI_SPROUT", "Debaixo de uma casquinha de gelo, um broto verde teimoso.", "Under a thin crust of ice, a stubborn green sprout.",
  "Bajo una costrita de hielo, un brote verde y testarudo.")
t("DLG_PI_CAMELIA_THANKS", "Ele tá vivo! Toma duas fatias de bolo. E volta daqui a um ano pro primeiro chá.",
  "It's alive! Take two cake slices. And come back in a year for the first cup of tea.", "¡Está vivo! Toma dos porciones de pastel. Y vuelve en un año por el primer té.")
t("DLG_PI_CAMELIA_AFTER", "O broto cresceu dois dedos! Chá, daqui a pouco. Paciência de chazeira.", "The sprout grew two fingers! Tea, soon. A tea-grower's patience.",
  "¡El brote creció dos dedos! Té, dentro de poco. Paciencia de tetera.")
t("DLG_PI_LAMINA_1", "No gelo, quem é rápido chega primeiro. Quer apostar corrida na timeline?",
  "On ice, the fast arrive first. Want to race me on the timeline?", "En el hielo, el rápido llega primero. ¿Apostamos una carrera en la línea de turnos?")
t("DLG_PI_LAMINA_2", "Você freou na hora certa. Isso é que é patinar.", "You braked at just the right time. Now that's skating.",
  "Frenaste justo a tiempo. Eso sí es patinar.")
t("DLG_PI_GRANIZO_1", "A gente congela, você esquenta. Vamos ver quem derrete primeiro!", "We freeze, you heat up. Let's see who melts first!",
  "Nosotros congelamos, tú te calientas. ¡A ver quién se derrite primero!")
t("DLG_PI_GRANIZO_2", "Derretemos. Era pra ser só um pouquinho.", "We melted. It was only supposed to be a little.", "Nos derretimos. Se suponía que solo un poquito.")
R.d("placa_cidade", [say("SIGN_PI_TOWN")])
R.d("placa_jardim", [say("SIGN_PI_GARDEN")])
R.d("boneco", [say("OBJ_PI_SNOWMAN")])
R.d("chegada_cidade", [lia("DLG_PI_ARR_C_L"), taro("DLG_PI_ARR_C_T"), flag("geada_vista")])
R.d("lareira", [act("heal"), act("respawn"), {"say": "DLG_PI_LAREIRA_AFTER", "speaker": "SPK_LAREIRA", "if": "alva_beaten"},
                {"say": "DLG_PI_LAREIRA_1", "speaker": "SPK_LAREIRA", "if_not": "alva_beaten"},
                {"say": "DLG_PI_LAREIRA_2", "speaker": "SPK_LAREIRA", "if_not": "alva_beaten"},
                ask("DLG_PI_LAREIRA_3", "SPK_LAREIRA", [("OPT_P_RANCH", "vila_mare/rancho"), ("OPT_P_LEAVE", None)])])
R.d("cachecol", [say("DLG_PI_CACHECOL_1", "SPK_CACHECOL"), act("shop", id="geada"), say("DLG_PI_CACHECOL_2", "SPK_CACHECOL")])
R.d("floquinho", [{"say": "DLG_PI_FLOQUINHO_AFTER", "speaker": "SPK_FLOQUINHO", "if": "alva_beaten"},
                  {"say": "DLG_PI_FLOQUINHO", "speaker": "SPK_FLOQUINHO", "if_not": "alva_beaten"}])
R.d("pinhao", [say("DLG_PI_PINHAO_1", "SPK_PINHAO"), say("DLG_PI_PINHAO_2", "SPK_PINHAO")])
R.d("degelo", [say("DLG_PI_DEGELO_1", "SPK_DEGELO"), say("DLG_PI_DEGELO_2", "SPK_DEGELO")])
R.d("camelia_pede", [say("DLG_PI_CAMELIA_ASK", "SPK_CAMELIA"), say("DLG_PI_CAMELIA_ASK2", "SPK_CAMELIA"), flag("camelia_quest")])
R.d("camelia_onde", [say("DLG_PI_CAMELIA_WHERE", "SPK_CAMELIA")])
R.d("camelia_obrigada", [act("take_item", item="broto_cha", n=1), say("DLG_PI_CAMELIA_THANKS", "SPK_CAMELIA"),
                         act("give_item", item="pocao_g", n=2), flag("camelia_done")])
R.d("camelia_depois", [say("DLG_PI_CAMELIA_AFTER", "SPK_CAMELIA")])
R.d("broto", [say("OBJ_PI_SPROUT"), act("give_item", item="broto_cha", n=1), flag("broto_pego")])
R.d("lamina", [say("DLG_PI_LAMINA_1", "SPK_LAMINA"),
               battle("BTL_TAMER_LAMINA", team([("carregador", 66), ("escultor", 65)]), 820, "lamina_beaten", [["pocao_g", 2]]),
               say("DLG_PI_LAMINA_2", "SPK_LAMINA")])
R.d("lamina_depois", [say("DLG_PI_LAMINA_2", "SPK_LAMINA")])
R.d("granizo", [say("DLG_PI_GRANIZO_1", "SPK_GRANIZO"),
                battle("BTL_TAMER_GRANIZO", team([("escultor", 66), ("chazeiro", 65)]), 800, "granizo_beaten", [["reviver", 2]]),
                say("DLG_PI_GRANIZO_2", "SPK_GRANIZO")])
R.d("granizo_depois", [say("DLG_PI_GRANIZO_2", "SPK_GRANIZO")])
R.NPCS["lareira"] = human("lareira", "SPK_LAREIRA", [{"dialog": ref("lareira")}], role="ranch")
R.NPCS["cachecol"] = human("cachecol", "SPK_CACHECOL", [{"dialog": ref("cachecol")}], "stand", role="shop")
R.NPCS["floquinho"] = human("floquinho", "SPK_FLOQUINHO", [{"dialog": ref("floquinho")}], role="humor")
R.NPCS["pinhao"] = human("pinhao", "SPK_PINHAO", [{"dialog": ref("pinhao")}], "stand", role="lore")
R.NPCS["degelo"] = human("degelo", "SPK_DEGELO", [{"dialog": ref("degelo")}])
R.NPCS["camelia"] = human("camelia", "SPK_CAMELIA", [{"if": "camelia_done", "dialog": ref("camelia_depois")},
                                                     {"if": "has_broto_cha", "dialog": ref("camelia_obrigada")},
                                                     {"if": "camelia_quest", "dialog": ref("camelia_onde")}, {"dialog": ref("camelia_pede")}], role="quest")
R.tamer("lamina", "lamina", "SPK_LAMINA", "lamina", "lamina_beaten", 3)
R.tamer("granizo", "granizo", "SPK_GRANIZO", "granizo", "granizo_beaten", 3)

# ------------------------------------------------------------------ Mosteiro do Eco: Nevasco e a pista 6
t("DLG_PI_NEV_1", "Sou Nevasco. Guardo este mosteiro e o sino do eco, que não toca há mil anos.",
  "I am Nevasco. I keep this monastery and the bell of the echo, which hasn't rung in a thousand years.",
  "Soy Nevasco. Guardo este monasterio y la campana del eco, que no suena desde hace mil años.")
t("DLG_PI_NEV_2", "A coroa do Rei não chama só de longe. O eco dela atravessa o tempo.", "The King's crown doesn't only call from afar. Its echo crosses time.",
  "La corona del Rey no llama solo desde lejos. Su eco atraviesa el tiempo.")
t("DLG_PI_NEV_3", "Quem a ouviu cantar foi chamado. E você ouviu, não ouviu?", "Whoever heard it sing was called. And you heard it, didn't you?",
  "Quien la oyó cantar fue llamado. Y tú la oíste, ¿verdad?")
t("DLG_PI_NEV_4", "O vidro do museu vibrando. A coroa cantando só pra você. Alguém te chamou de propósito.",
  "The museum glass trembling. The crown singing only for you. Someone called you on purpose.",
  "El cristal del museo vibrando. La corona cantando solo para ti. Alguien te llamó a propósito.")
t("DLG_PI_NEV_L", "Chamou pra quê? Pra ajudar... ou pra prender?", "Called for what? To help... or to trap?", "¿Llamó para qué? ¿Para ayudar... o para atrapar?")
t("DLG_PI_NEV_T", "Ninguém chama ninguém de mil anos de distância à toa.", "Nobody calls someone from a thousand years away for nothing.",
  "Nadie llama a alguien desde mil años de distancia por nada.")
t("DLG_PI_NEV_5", "Essa resposta está no deserto, com a rainha. Antes, mostre se seu coração aguenta.",
  "That answer lies in the desert, with the queen. First, show me your heart can bear it.",
  "Esa respuesta está en el desierto, con la reina. Antes, muéstrame que tu corazón lo aguanta.")
t("DLG_PI_NEV_AGAIN", "O sino do eco espera. Seu coração aguenta mais uma?", "The bell of the echo waits. Can your heart bear one more?",
  "La campana del eco espera. ¿Tu corazón aguanta una más?")
R.d("nevasco", [say("DLG_PI_NEV_1", "SPK_NEVASCO"), say("DLG_PI_NEV_2", "SPK_NEVASCO"), say("DLG_PI_NEV_3", "SPK_NEVASCO"), say("DLG_PI_NEV_4"),
                lia("DLG_PI_NEV_L"), taro("DLG_PI_NEV_T"), flag("pista_6"),
                ask("DLG_PI_NEV_5", "SPK_NEVASCO", [("OPT_PI_DUEL", ref("nevasco_luta")), ("OPT_P_NOT_NOW", None)])])
R.d("nevasco_de_novo", [ask("DLG_PI_NEV_AGAIN", "SPK_NEVASCO", [("OPT_PI_DUEL", ref("nevasco_luta")), ("OPT_P_NOT_NOW", None)])])
R.d("nevasco_luta", [battle("", [["nevasco", 64]], 0, kind="wild")])
R.NPCS["nevasco_npc"] = {"name_key": "SPECIES_NEVASCO", "role": "wild", "sprite": "res://assets/sprites/npc/skel_nevasco.png", "frames": 2, "idle_fps": 2.0,
                         "behavior": "stand", "dialog": [{"if": "pista_6", "dialog": ref("nevasco_de_novo")}, {"dialog": ref("nevasco")}]}

# ------------------------------------------------------------------ Jardim de Gelo: capanga e Guardiã Alva (escolha 5)
t("DLG_PI_ARR_J_L", "Tá tudo branco. Segue a minha luz, eu vou na frente!", "Everything's white. Follow my light, I'll go first!",
  "Todo está blanco. ¡Sigue mi luz, yo voy delante!")
t("DLG_PI_ARR_J_T", "Estátuas de gelo de todo mundo da cidade. Que coisa triste.", "Ice statues of everyone in town. How sad.",
  "Estatuas de hielo de toda la gente del pueblo. Qué cosa más triste.")
t("DLG_PI_PING_1", "A princesa não recebe visitas. Ordem dela. E minha também, que eu tô com frio.",
  "The princess receives no visitors. Her orders. Mine too, because I'm cold.", "La princesa no recibe visitas. Orden suya. Y mía también, que tengo frío.")
t("DLG_PI_PING_2", "Tá, passa. Mas fala baixo, ela tá cantando.", "Fine, go. But keep it down, she's singing.", "Vale, pasa. Pero habla bajito, está cantando.")
# Com os dois na equipe, o "reencontro" dos Picos vira esta cena: Taro admite o medo e Lia guia pela neve.
DUO = {"if_all": ["partner_lia", "partner_taro"]}
t("DLG_PI_DUO_T1", "Eu tenho medo, sabia? De chegar no castelo e meus pais me olharem igual essas estátuas.",
  "I'm scared, you know? Of reaching the castle and my parents looking at me like these statues.",
  "Tengo miedo, ¿sabes? De llegar al castillo y que mis padres me miren como estas estatuas.")
t("DLG_PI_DUO_L1", "Eles vão lembrar, Taro. Quem faz falta não vira estátua.", "They'll remember, Taro. Someone who's missed doesn't turn into a statue.",
  "Se acordarán, Taro. Quien hace falta no se vuelve estatua.")
t("DLG_PI_DUO_T2", "...Falei em voz alta. Pronto. Agora anda, antes que eu me arrependa.", "...I said it out loud. There. Now move, before I regret it.",
  "...Lo dije en voz alta. Listo. Ahora camina, antes de que me arrepienta.")
R.d("chegada_jardim", [taro("DLG_PI_ARR_J_T"), say("DLG_PI_DUO_T1", "SPK_TARO") | DUO, say("DLG_PI_DUO_L1", "SPK_LIA") | DUO,
                       say("DLG_PI_DUO_T2", "SPK_TARO") | DUO, lia("DLG_PI_ARR_J_L"), flag("jardim_visto")])
R.d("pingente", [say("DLG_PI_PING_1", "SPK_PINGENTE"), battle("BTL_TAMER_PINGENTE", team([("escultor", 67), ("carregador", 67)]), 840, "pingente_beaten"),
                 say("DLG_PI_PING_2", "SPK_PINGENTE")])
R.d("pingente_depois", [say("DLG_PI_PING_2", "SPK_PINGENTE")])
R.tamer("pingente", "pingente", "SPK_PINGENTE", "pingente", "pingente_beaten", 3)

t("DLG_PI_ALVA_1", "Você veio de muito longe. Dá pra ver nos seus olhos.", "You've come from very far away. I can see it in your eyes.", "Vienes de muy lejos. Se te nota en los ojos.")
t("DLG_PI_ALVA_2", "Sou Alva, filha do Rei. Meu pai está triste há mil anos. Se nada mudar, talvez ele melhore.",
  "I'm Alva, the King's daughter. My father has been sad for a thousand years. If nothing changes, maybe he'll get better.",
  "Soy Alva, hija del Rey. Mi padre lleva mil años triste. Si nada cambia, quizá mejore.")
t("DLG_PI_ALVA_3", "Por isso congelei tudo aqui em cima. Desculpa. Não posso deixar você passar.", "That's why I froze everything up here. I'm sorry. I can't let you through.",
  "Por eso congelé todo aquí arriba. Lo siento. No puedo dejarte pasar.")
t("DLG_PI_ALVA_WIN", "Você é rápido... mais rápido que o inverno.", "You're fast... faster than winter.", "Eres rápido... más rápido que el invierno.")
t("DLG_PI_ALVA_MOTIVE", "Eu só queria ver meu pai sorrir de novo. Quando a coroa rachou, ele parou de vez.",
  "I just wanted to see my father smile again. When the crown cracked, he stopped for good.",
  "Solo quería ver a mi padre sonreír otra vez. Cuando la corona se agrietó, dejó de hacerlo para siempre.")
t("DLG_PI_ALVA_ECHO", "Você é o eco que a coroa chamou, não é? Então você vai ver meu pai.", "You're the echo the crown called, aren't you? Then you'll see my father.",
  "Eres el eco que llamó la corona, ¿verdad? Entonces verás a mi padre.")
t("DLG_PI_ALVA_ASK", "Leva isto pra ele? Ele não lê as minhas cartas. Talvez leia, se vier de você.",
  "Will you take this to him? He doesn't read my letters. Maybe he will, if it comes from you.",
  "¿Le llevas esto? No lee mis cartas. Quizá la lea si se la llevas tú.")
t("DLG_PI_ALVA_THANKS", "Obrigada. Diz que a filha dele está esperando. Que sempre esperou.", "Thank you. Tell him his daughter is waiting. That she always has been.",
  "Gracias. Dile que su hija lo está esperando. Que siempre lo esperó.")
t("DLG_PI_ALVA_NO", "Entendo. Ninguém gosta de carregar a tristeza dos outros. Se mudar de ideia, ela fica aqui.",
  "I understand. Nobody likes carrying someone else's sadness. If you change your mind, it'll be here.",
  "Lo entiendo. A nadie le gusta cargar la tristeza ajena. Si cambias de idea, aquí estará.")
t("DLG_PI_ALVA_THAW", "O gelo da estrada vai derreter. Lá embaixo fica o deserto. Minha mãe mora lá.",
  "The ice on the road will melt. Down below is the desert. My mother lives there.", "El hielo del camino se derretirá. Allá abajo está el desierto. Mi madre vive allí.")
t("DLG_PI_ALVA_AFTER", "Diz pra minha mãe que eu tô bem. Mais ou menos bem.", "Tell my mother I'm all right. More or less.", "Dile a mi madre que estoy bien. Más o menos.")
ALVA_TEAM = team([("carregador", 72), ("escultor", 71), ("chazeiro", 73), ("mineiro", 72)])
R.d("alva", [say("DLG_PI_ALVA_1", "SPK_ALVA"), say("DLG_PI_ALVA_2", "SPK_ALVA"), say("DLG_PI_ALVA_3", "SPK_ALVA"),
             battle("BTL_TAMER_ALVA", ALVA_TEAM, 1900, "alva_beaten", kind="boss"),
             say("DLG_PI_ALVA_WIN", "SPK_ALVA"), say("DLG_PI_ALVA_MOTIVE", "SPK_ALVA"), say("DLG_PI_ALVA_ECHO", "SPK_ALVA"),
             say("DLG_PI_ALVA_THAW", "SPK_ALVA"), goto(ref("alva_carta"))])
R.d("alva_carta", [ask("DLG_PI_ALVA_ASK", "SPK_ALVA", [("OPT_PI_TAKE", ref("carta_sim")), ("OPT_PI_LEAVE", ref("carta_nao"))])])
R.d("carta_sim", [act("give_item", item="carta_alva", n=1), say("DLG_PI_ALVA_THANKS", "SPK_ALVA"), flag("picos_carta"), act("refresh_map")])
R.d("carta_nao", [say("DLG_PI_ALVA_NO", "SPK_ALVA"), act("refresh_map")])
R.d("alva_depois", [say("DLG_PI_ALVA_AFTER", "SPK_ALVA")])
R.NPCS["alva"] = {"name_key": "SPK_ALVA", "role": "guardian", "sprite": "res://assets/sprites/npc/skel_alva.png", "frames": 2, "idle_fps": 2.0,
                  "behavior": "stand", "dialog": [{"if": "picos_carta", "dialog": ref("alva_depois")}, {"if": "alva_beaten", "dialog": ref("alva_carta")},
                                                  {"dialog": ref("alva")}],
                  "tamer": {"vision": 3, "flag": "alva_beaten"}}


# ------------------------------------------------------------------ encontros (balance.json: selvagens 57–63)
def e(sp, st, a, b, rar, w=None):
    d = {"species": sp, "stage": st, "min_level": a, "max_level": b, "rarity": rar}
    if w:
        d["weight"] = w
    return d


R.TABLES.update({
    "rota5_sul": [e("carregador_2", 2, 57, 59, "comum"), e("mineiro_3", 3, 57, 59, "comum")],
    "rota5_oeste": [e("carregador_2", 2, 58, 60, "comum"), e("sineiro_3", 3, 58, 60, "incomum")],
    "rota5_campo": [e("carregador_2", 2, 58, 60, "comum"), e("escultor_2", 2, 58, 60, "incomum"), e("chazeiro_2", 2, 59, 61, "raro"),
                    e("mineiro_3", 3, 58, 60, "comum"), e("sineiro_3", 3, 59, 61, "incomum")],
    "rota5_ponte": [e("chazeiro_2", 2, 66, 67, "raro", 60), e("escultor_3", 3, 66, 67, "incomum", 40)],
    "rota5_norte": [e("escultor_2", 2, 60, 62, "incomum"), e("carregador_2", 2, 60, 62, "comum")],
    "jardim_salao": [e("escultor_2", 2, 61, 63, "incomum"), e("carregador_2", 2, 61, 63, "comum"), e("mineiro_3", 3, 61, 63, "comum")],
    "jardim_sul": [e("chazeiro_2", 2, 62, 63, "raro"), e("escultor_2", 2, 62, 63, "incomum")],
})
R.SHOPS["geada"] = ["pocao_g", "antidoto", "reviver"]

# ------------------------------------------------------------------ mapas
LEG = {"g": "snow", "f": "ice", "B": "snow_rock", "p": "stone", ".": "floor"}
rota = make_route("rota_5", "picos", "MAP_ROTA_5", LEG, ("ossorio", 19, 1), ("geada", 19, 30),
                  tamers=[("grampo", {}), ("rajada", {}), ("brisa", {})], hint="treno", sign=R.ref("placa_bifurcacao"),
                  spawns=[{"id": "r5_sul", "table": "rota5_sul", "x": 10, "y": 45, "radius": 3, "count": 2},
                          {"id": "r5_oeste", "table": "rota5_oeste", "x": 5, "y": 25, "radius": 2, "count": 1},
                          {"id": "r5_campo_a", "table": "rota5_campo", "x": 30, "y": 32, "radius": 4, "count": 3},
                          {"id": "r5_campo_b", "table": "rota5_campo", "x": 30, "y": 18, "radius": 4, "count": 3},
                          {"id": "r5_ponte", "table": "rota5_ponte", "x": 19, "y": 25, "radius": 2, "count": 1},
                          {"id": "r5_norte", "table": "rota5_norte", "x": 10, "y": 6, "radius": 3, "count": 2}],
                  extra_npcs=[{"id": "leal_a", "x": 16, "y": 4, "facing": "right", "if": "ossorio_revelou"},
                              {"id": "leal_b", "x": 23, "y": 8, "facing": "left", "if": "ossorio_revelou"},
                              {"id": "rival_taro_p", "x": 26, "y": 6, "facing": "left", "if": "partner_lia", "if_none": ["partner_taro", "rival_picos_done"]},
                              {"id": "rival_lia_p", "x": 26, "y": 6, "facing": "left", "if": "partner_taro", "if_none": ["partner_lia", "rival_picos_done"]}],
                  extra_props=[{"type": "prayer_flags", "x": 20, "y": 36}, {"type": "prayer_flags", "x": 20, "y": 14},
                               {"type": "snowman", "x": 24, "y": 44, "dialog": R.ref("boneco")}],
                  deco=("snow_pine", "snow_pine", "rock_small"), tint=[0.96, 0.98, 1.0], seed=81)
rota["on_enter"] = [{"if_not": "rota5_vista", "dialog": R.ref("chegada_rota")}]
rota["ambient"] = ["snow"]

town = make_town("geada", "picos", "MAP_GEADA", dict(LEG, s="stone"),
                 south=("rota_5", 19, 1), north=("rota_6", 19, 48), west=("jardim_gelo", 32, 10),
                 houses=["chalet_ranch", "chalet_shop", "chalet", "chalet", "chalet"],
                 npcs=[{"id": "floquinho", "x": 16, "y": 16, "facing": "right"}, {"id": "pinhao", "x": 24, "y": 18, "facing": "left"},
                       {"id": "degelo", "x": 22, "y": 13, "facing": "down"}, {"id": "camelia", "x": 26, "y": 24, "facing": "left"}],
                 props=[{"type": "sign", "x": 18, "y": 28, "dialog": R.ref("placa_cidade")}, {"type": "sign", "x": 3, "y": 14, "dialog": R.ref("placa_jardim")},
                        {"type": "snowman", "x": 17, "y": 15, "dialog": R.ref("boneco")}, {"type": "kettle", "x": 23, "y": 16},
                        {"type": "prayer_flags", "x": 20, "y": 12}, {"type": "lamp_post", "x": 13, "y": 13}, {"type": "lamp_post", "x": 26, "y": 13},
                        {"type": "monastery_gate", "x": 14, "y": 25}],
                 deco=("snow_pine", "rock_small"), tint=[0.95, 0.97, 1.0], seed=91, plaza="s")
for w in town["warps"]:
    if w["to"] == "rota_6":
        w["if"] = "alva_beaten"
        w["locked_message"] = "MSG_ALVA_ROAD"
town["on_enter"] = [{"if_not": "geada_vista", "dialog": R.ref("chegada_cidade")}]
town["ambient"] = ["snow"]
town_doors(town, "geada", {"rancho": "geada_rancho", "loja": "geada_loja", "a": "geada_casa_lamina", "b": "geada_casa_granizo", "c": "mosteiro_eco"})

lair = make_lair("jardim_gelo", "picos", "MAP_JARDIM_GELO", {"g": "snow", "p": "stone", "B": "snow_rock", "f": "ice"}, east=("geada", 1, 15),
                 guardian_npc={"id": "alva", "x": 10, "y": 3, "facing": "down"},
                 extra_npcs=[{"id": "pingente", "x": 14, "y": 10, "facing": "right"}],
                 props=[{"type": "statue_prince", "x": 5, "y": 2}, {"type": "statue_prince", "x": 15, "y": 2}, {"type": "crystal", "x": 7, "y": 5},
                        {"type": "crystal", "x": 13, "y": 5}, {"type": "snow_pine", "x": 20, "y": 9}, {"type": "snow_pine", "x": 27, "y": 13},
                        {"type": "crystal", "x": 22, "y": 13}, {"type": "snowman", "x": 4, "y": 19, "dialog": R.ref("boneco")},
                        {"type": "herb_blue", "x": 11, "y": 18, "dialog": R.ref("broto"), "if": "camelia_quest", "if_not": "broto_pego"}],
                 spawns=[{"id": "j_salao", "table": "jardim_salao", "x": 23, "y": 10, "radius": 3, "count": 2},
                         {"id": "j_sul", "table": "jardim_sul", "x": 6, "y": 15, "radius": 2, "count": 1}],
                 tint=[0.86, 0.92, 1.0])
lair["on_enter"] = [{"if_not": "jardim_visto", "dialog": R.ref("chegada_jardim")}]
lair["ambient"] = ["snow"]

R.MAPS.update({
    "rota_5": rota, "geada": town, "jardim_gelo": lair,
    "geada_rancho": room("geada_rancho", "picos", "MAP_GEADA_RANCHO", "geada", (12, 10),
                         [{"type": "bed", "x": 2, "y": 3}, {"type": "bed", "x": 4, "y": 3}, {"type": "campfire", "x": 10, "y": 6}, {"type": "rug", "x": 6, "y": 6}],
                         [{"id": "lareira", "x": 7, "y": 3, "facing": "down"}]),
    "geada_loja": room("geada_loja", "picos", "MAP_GEADA_LOJA", "geada", (27, 10),
                       [{"type": "shelf", "x": 3, "y": 2}, {"type": "shelf", "x": 10, "y": 2}, {"type": "table", "x": 7, "y": 4}, {"type": "kettle", "x": 1, "y": 7}],
                       [{"id": "cachecol", "x": 6, "y": 3, "facing": "down"}]),
    "geada_casa_lamina": room("geada_casa_lamina", "picos", "MAP_GEADA_CASA_LAMINA", "geada", (8, 20),
                              [{"type": "table", "x": 7, "y": 5}, {"type": "plant", "x": 2, "y": 3}, {"type": "lamp", "x": 10, "y": 7}],
                              [{"id": "lamina", "x": 6, "y": 3, "facing": "down"}]),
    "geada_casa_granizo": room("geada_casa_granizo", "picos", "MAP_GEADA_CASA_GRANIZO", "geada", (31, 20),
                               [{"type": "bed", "x": 2, "y": 3}, {"type": "bed", "x": 4, "y": 3}, {"type": "table", "x": 8, "y": 5}],
                               [{"id": "granizo", "x": 6, "y": 3, "facing": "down"}]),
    "mosteiro_eco": room("mosteiro_eco", "picos", "MAP_MOSTEIRO", "geada", (14, 27),
                         [{"type": "bell_tower", "x": 6, "y": 2}, {"type": "candelabra", "x": 2, "y": 4}, {"type": "candelabra", "x": 10, "y": 4},
                          {"type": "rug", "x": 6, "y": 6}, {"type": "prayer_flags", "x": 6, "y": 8}],
                         [{"id": "nevasco_npc", "x": 6, "y": 4, "facing": "down"}], floor="carpet"),
})
R.BATTLE_BG["picos"] = "res://assets/battle/bg_picos.png"
R.CITIES.append({"id": "geada", "map": "geada", "ranch": "lareira", "shop": "geada", "tamer_houses": ["lamina", "granizo"],
                 "npcs": ["floquinho", "pinhao", "degelo", "camelia", "nevasco_npc"], "quests": ["camelia"]})
R.ROUTES.append({"id": "rota_5", "map": "rota_5", "from": "ossorio", "to": "geada",
                 "paths": [{"kind": "domadores", "required": False}, {"kind": "selvagem", "required": False},
                           {"kind": "atalho", "required": False, "note": "Ponte de Gelo: curta, com um selvagem forte"}]})

# ------------------------------------------------------------------ documento
R.DOC = {
    "title": "Ato 5: Rota 5 e Picos Gelados", "phase": "4f", "duration": "25 min",
    "ages": "chegada 58–66; selvagens 57–63; domadores 60–67; Guardiã ~72 (protótipo do balance.json)",
    "problem": "Faz um ano que é inverno em **Geada**. A Guardiã **Alva**, filha do Rei, congelou os picos para que \"nada mude\" até o pai melhorar da tristeza. "
               "As hortas de chá morreram, os trenós não descem e a estrada para o deserto está fechada por uma parede de gelo.",
    "clue_n": 6,
    "clue": "No **Mosteiro do Eco**, o monge-esqueleto **Nevasco** explica que o eco da coroa **atravessa o tempo**: quem a ouviu cantar foi chamado. "
            "O protagonista lembra do vidro do museu vibrando: alguém o chamou de propósito. (Para quê? A resposta está no deserto.)",
    "moment": ["**Jardim de Gelo (dupla):** diante das estátuas, Taro admite: \"Eu tenho medo... de meus pais me olharem igual essas estátuas.\" Lia: \"Quem faz falta não vira estátua.\" "
               "Taro: \"Falei em voz alta. Pronto.\" Depois Lia vai na frente: \"Segue a minha luz!\" (o medo dela virou coragem).",
               "**Saves antigos (recorrente):** reencontro com batalha opcional na Rota 5:",
               "Taro (parceira Lia) chega brigando e depois admite: \"Tenho medo de chegar no castelo e meus pais não lembrarem de mim.\" Lia: \"Ninguém esquece quem faz falta.\"",
               "Lia (parceiro Taro) guia pela nevasca e ensina: \"Quando a neve fecha tudo, olha pra luz. É só seguir a luz.\" Depois vai acender o farol.",
               "Parceira Lia, no Jardim de Gelo: \"Segue a minha luz, eu vou na frente!\" (o medo virou coragem)."],
    "guardian": {"name": "Alva (filha do Rei, a herdeira)", "kin": "filha",
                 "personality": "melancólica, doce, firme; pede desculpas antes de lutar",
                 "motive": "**Esperança:** se nada mudar, o pai talvez se cure da tristeza. Congelar é a forma dela de \"parar o tempo\".",
                 "mechanic": "**Velocidade.** Golpes leves e congelamento (VEL ↓): a equipe dela age mais vezes na timeline. Ensina controle de velocidade "
                             "e a escolher golpes pesados que valham a espera. Degelo, a Patinadora Lâmina e os Irmãos Granizo preparam.",
                 "team": "Alpinor 72, Cristalor 71, Samovarão 73, Rochedão 72.",
                 "reward": "1900 moedas; o gelo derrete e a descida para o deserto abre; e a **escolha 5**."},
    "maps": [("**Rota 5** (`rota_5`)", "Trilha nevada. 3 caminhos: **Alpinistas** (oeste: Grampo, Rajada, Monja Brisa), **Campo Branco** (gelo, leste) e **Ponte de Gelo** "
              "(centro, curta, com um selvagem forte). Se a cidade de Ossório soube do registro (escolha 4), **dois Guardas Leais** vigiam a saída norte. "
              "Reencontro com o recorrente. Placa e o Guia Trenó dão a dica."),
             ("**Geada** (`geada`)", "Vila de chalés: Rancho (Lareira), Armarinho (Cachecol), casas da Patinadora Lâmina e dos Irmãos Granizo, o **Mosteiro do Eco** "
              "(Nevasco), boneco de neve \"Prefeito\", chaleira de chá e a missão do broto."),
             ("**Jardim de Gelo** (`jardim_gelo`)", "Estátuas e cristais, Guarda Pingente, o broto de chá ao sul e a Alva ao norte."),
             ("Interiores", "Rancho da Lareira, Armarinho do Cachecol, casas da Lâmina e dos Granizo, Mosteiro do Eco.")],
}
R.NPC_DOC = [
    ("Guia Trenó", "dica", "Explica os 3 caminhos; mostra o comércio parado pelo gelo"),
    ("Grampo, Rajada, Monja Brisa", "domadores da rota", "Caminho dos Alpinistas; Rajada introduz a velocidade"),
    ("Guardas Leais (2)", "domadores condicionais", "Consequência da escolha 4 (só se Ossório soube)"),
    ("Dona Lareira", "Rancho", "Cura; conta desde quando é inverno"),
    ("Seu Cachecol", "Loja", "Loja só com itens fortes (Fatia de Bolo, Erva Amarga, Vela de Aniversário)"),
    ("Floquinho", "humor", "O boneco de neve \"Prefeito\""),
    ("Vô Pinhão", "lore", "A Alva menina; \"tristeza de princesa vira inverno\""),
    ("Degelo", "dica", "Ensina a mecânica da Guardiã (velocidade e congelamento)"),
    ("Camélia", "missão", "O broto de chá: a vila recomeça"),
    ("Nevasco", "único + pista 6", "O eco que atravessa o tempo; batalha opcional (recrutável)"),
    ("Guarda Pingente", "capanga", "Guarda o Jardim"),
    ("Alva", "Guardiã", "Velocidade; a carta para o pai (escolha 5)"),
]
R.HOUSES = [
    ("Patinadora Lâmina", "Velocidade (Cargueiro + Cinzelvo)", "820 moedas + 2 Fatias de Bolo"),
    ("Irmãos Granizo", "Congelamento e cura (Cinzelvo + Chaleirel)", "800 moedas + 2 Vela de Aniversário"),
]
R.CHOICES = [
    ("Caminho da Rota 5", "Alpinistas / Campo Branco / Ponte de Gelo", "Moedas e itens / XP e marcadores / curto, com um selvagem forte"),
    ("Recorrente", "Lutar / só conversar", "900 moedas e +10% no marcador; a cena do arco acontece nos dois casos"),
    ("Consequência da escolha 4", "—", "Se contou o registro em Ossório: 2 Guardas Leais na Rota 5 (mais batalhas)"),
    ("**Escolha 5: a carta da Alva**", "Levar / Não levar",
     "Levar: o item-chave **Carta da Alva**, que no Castelo pode ser entregue ao Rei (diálogo exclusivo). **Obrigatória para o Final A (Redimir).** "
     "Não levar: a Alva guarda a carta, e o jogador pode voltar e aceitar depois."),
    ("Missão do broto", "Fazer / ignorar", "2 Fatias de Bolo"),
]

if __name__ == "__main__":
    R.write()
