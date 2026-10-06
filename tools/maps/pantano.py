#!/usr/bin/env python3
"""Ato 3 — Rota 3 e Pântano Verde-Musgo (fase 4d). Fonte única: gera o roteiro
docs/roteiro/04_pantano.md, as falas (PT/EN/ES), NPCs, encontros, loja, itens e
mapas (Rota 3, Brejo Alto e interiores, Caldeirão da Musga)."""
import json

from regionkit import (ROOT, Region, make_lair, make_route, make_town, room, town_doors, team,
                       say, ask, battle, act, flag, goto, human, skel)

R = Region("pantano", 4, "pantano", ["pantano"])
t = R.t
ref = R.ref


def lia(k):
    return say(k, "SPK_LIA") | {"if": "partner_lia"}


def taro(k):
    return say(k, "SPK_TARO") | {"if": "partner_taro"}


# ------------------------------------------------------------------ nomes
for k, pt, en, es in [
        ("REMANSO", "Barqueiro Remanso", "Boatman Backwater", "Barquero Remanso"), ("TRAIRA", "Traíra", "Pike", "Lucio"),
        ("CANICO", "Caniço", "Rod", "Caña"), ("MARRECO", "Marreco", "Teal", "Cerceta"), ("GARCA", "Dona Garça", "Mrs. Heron", "Doña Garza"),
        ("JUNCO", "Seu Junco", "Mr. Rush", "Don Junco"), ("TABOA", "Irmãs Taboa", "Cattail Sisters", "Hermanas Totora"),
        ("BAGRE", "Pescador Bagre", "Fisher Catfish", "Pescador Bagre"), ("NEBLINA", "Vó Neblina", "Granny Fog", "Abuela Neblina"),
        ("GIRINO", "Girino", "Tadpole", "Renacuajo"), ("SAPE", "Seu Sapé", "Old Thatch", "Don Paja"), ("LODO", "Lodo", "Silt", "Limo"),
        ("PENA", "Dona Pena", "Mrs. Quill", "Doña Pluma"), ("FEL", "Boticário Fel", "Apothecary Bile", "Boticario Hiel"),
        ("MUSGA", "Musga", "Musga", "Musga")]:
    t(f"SPK_{k}", pt, en, es)
for k in ("TRAIRA", "CANICO", "MARRECO", "TABOA", "BAGRE", "NEBLINA", "FEL"):
    pt, en, es = R.T[f"SPK_{k}"]
    t(f"BTL_TAMER_{k}", pt, en, es)
t("BTL_TAMER_MUSGA", "Guardiã Musga", "Guardian Musga", "Guardiana Musga")
t("MAP_ROTA_3", "Rota 3 — Trilha das Palafitas", "Route 3 — Stilt Trail", "Ruta 3 — Sendero de Palafitos")
t("MAP_BREJO", "Brejo Alto", "Highmarsh", "Ciénaga Alta")
t("MAP_CALDEIRAO", "Caldeirão da Musga", "Musga's Cauldron", "Caldero de Musga")
t("MAP_BREJO_RANCHO", "Rancho da Garça", "Heron's Ranch", "Rancho de Garza")
t("MAP_BREJO_LOJA", "Venda do Junco", "Rush's Shop", "Tienda de Junco")
t("MAP_BREJO_CASA_TABOA", "Casa das Irmãs Taboa", "Cattail Sisters' House", "Casa de las Hermanas Totora")
t("MAP_BREJO_CASA_BAGRE", "Casa do Bagre", "Catfish's House", "Casa de Bagre")
t("MAP_BREJO_CASA_NEBLINA", "Casa da Vó Neblina", "Granny Fog's House", "Casa de la Abuela Neblina")
t("MSG_MUSGA_ROAD", "A névoa da Musga engole a estrada do norte. Ninguém acha o caminho.",
  "Musga's fog swallows the north road. Nobody can find the way.", "La niebla de Musga se traga el camino del norte. Nadie encuentra el rumbo.")
t("MSG_NEBLINA_DOOR", "Porta trancada. Lá dentro, alguém tosse baixinho.", "The door is locked. Someone inside is coughing softly.",
  "Puerta cerrada. Dentro, alguien tose bajito.")
t("ITEM_MAILBAG", "Malote da Pena", "Quill's Mailbag", "Saca de Pluma")
t("ITEM_MAILBAG_TEXT", "Cartas da vila inteira, todas abertas e com bilhetinhos da Musga.", "Letters from the whole village, all opened and with notes from Musga.",
  "Cartas de toda la aldea, todas abiertas y con notitas de Musga.")
R.ITEMS["malote"] = {"name_key": "ITEM_MAILBAG", "desc_key": "ITEM_MAILBAG_TEXT", "kind": "key", "price": 0, "battle": False, "target": "none"}
t("OPT_PA_DONATE", "Doar ervas amargas", "Donate bitterleaf", "Donar hierbas amargas")
t("OPT_PA_KEEP", "Guardar", "Keep them", "Guardarlos")
t("OPT_PA_FIGHT_MIST", "Enfrentar a névoa", "Face the fog", "Enfrentar la niebla")

# ------------------------------------------------------------------ Rota 3
t("SIGN_PA_FORK", "← Trilha das Tábuas · ↑ Passagem do Desmoronamento · → Capinzal",
  "← Boardwalk Trail · ↑ Rockfall Pass · → Tallgrass", "← Sendero de Tablas · ↑ Paso del Derrumbe · → Pastizal")
t("OBJ_PA_RUBBLE", "Entulho de um desmoronamento antigo. Um martelo forte daria conta.", "Rubble from an old rockfall. A strong hammer would do the trick.",
  "Escombros de un derrumbe antiguo. Un martillo fuerte bastaría.")
t("DLG_PA_REMANSO_1", "Três trilhas: na das tábuas tem gente brava, no capim tem bicho, e no meio tem pedra caída.",
  "Three trails: the boardwalk has grumpy folks, the tall grass has critters, and the middle has fallen rock.",
  "Tres senderos: en las tablas hay gente brava, en el pasto hay bichos y en medio hay piedras caídas.")
t("DLG_PA_REMANSO_2", "Antes eu levava todo mundo de barco. Agora a névoa não deixa nem o barco sair.",
  "I used to ferry everyone by boat. Now the fog won't even let the boat leave.", "Antes llevaba a todos en barca. Ahora la niebla no deja salir ni a la barca.")
t("DLG_PA_REMANSO_HAMMER", "Esse martelo é da Tia Fornalha? Então a pedra do meio já era!",
  "Is that Aunt Furnace's hammer? Then the middle rocks are history!", "¿Ese martillo es de la Tía Fragua? ¡Entonces las piedras del medio ya fueron!")
t("DLG_PA_TRAIRA_1", "Pesco esqueleto, não peixe. Peixe não revida. Vamos!", "I fish for skeletons, not fish. Fish don't fight back. Let's go!",
  "Pesco esqueletos, no peces. Los peces no se defienden. ¡Vamos!")
t("DLG_PA_TRAIRA_2", "Escapou do anzol. Dessa vez.", "Got off the hook. This time.", "Te escapaste del anzuelo. Esta vez.")
t("DLG_PA_CANICO_1", "Eu tinha uma vara de pescar. Agora tenho um esqueleto que segura a vara pra mim.",
  "I used to have a fishing rod. Now I have a skeleton who holds the rod for me.", "Tenía una caña de pescar. Ahora tengo un esqueleto que me sostiene la caña.")
t("DLG_PA_CANICO_2", "Ele também não pesca nada. Mas é ótima companhia.", "He doesn't catch anything either. But he's great company.",
  "Él tampoco pesca nada. Pero es muy buena compañía.")
t("DLG_PA_MARRECO_1", "Meus patos fugiram da névoa. Meus esqueletos ficaram. Sabe por quê? Lealdade!",
  "My ducks fled the fog. My skeletons stayed. Know why? Loyalty!", "Mis patos huyeron de la niebla. Mis esqueletos se quedaron. ¿Sabes por qué? ¡Lealtad!")
t("DLG_PA_MARRECO_2", "Leva essas ervas amargas. Lá na vila tão precisando mais que eu.", "Take this bitterleaf. The village needs it more than I do.",
  "Llévate estas hierbas amargas. En la aldea las necesitan más que yo.")
t("DLG_PA_ARR_L1", "Vaga-lumes! Olha, eles acendem um pro outro achar o caminho.", "Fireflies! Look, they light up so the others can find the way.",
  "¡Luciérnagas! Mira, se encienden para que los demás encuentren el camino.")
t("DLG_PA_ARR_L2", "Igual farol. Só que pequenininho.", "Like a lighthouse. Just a tiny one.", "Como un faro. Solo que chiquitito.")
t("DLG_PA_ARR_T1", "Lama até o joelho. Ótimo.", "Mud up to my knees. Great.", "Barro hasta las rodillas. Genial.")
t("DLG_PA_ARR_T2", "Se meu pai tivesse aqui, já tinha feito uma ponte.", "If my dad were here, he'd have built a bridge by now.",
  "Si mi papá estuviera aquí, ya habría hecho un puente.")

R.d("placa_bifurcacao", [say("SIGN_PA_FORK")])
R.d("entulho", [say("OBJ_PA_RUBBLE")])
R.d("chegada_rota", [lia("DLG_PA_ARR_L1"), lia("DLG_PA_ARR_L2"), taro("DLG_PA_ARR_T1"), taro("DLG_PA_ARR_T2"), flag("rota3_vista")])
R.d("remanso", [{"say": "DLG_PA_REMANSO_HAMMER", "speaker": "SPK_REMANSO", "if": "has_martelo_tia"},
                say("DLG_PA_REMANSO_1", "SPK_REMANSO"), say("DLG_PA_REMANSO_2", "SPK_REMANSO")])
R.d("traira", [say("DLG_PA_TRAIRA_1", "SPK_TRAIRA"), battle("BTL_TAMER_TRAIRA", team([("palafiteiro", 36), ("lavadeira", 36)]), 520, "traira_beaten"),
               say("DLG_PA_TRAIRA_2", "SPK_TRAIRA")])
R.d("traira_depois", [say("DLG_PA_TRAIRA_2", "SPK_TRAIRA")])
R.d("canico", [say("DLG_PA_CANICO_1", "SPK_CANICO"), battle("BTL_TAMER_CANICO", team([("jardineiro_lirios", 37), ("cogumeleiro", 37)]), 540, "canico_beaten"),
               say("DLG_PA_CANICO_2", "SPK_CANICO")])
R.d("canico_depois", [say("DLG_PA_CANICO_2", "SPK_CANICO")])
R.d("marreco", [say("DLG_PA_MARRECO_1", "SPK_MARRECO"),
                battle("BTL_TAMER_MARRECO", team([("gasista", 38), ("palafiteiro", 38)]), 570, "marreco_beaten", [["antidoto", 2]]),
                say("DLG_PA_MARRECO_2", "SPK_MARRECO")])
R.d("marreco_depois", [say("DLG_PA_MARRECO_2", "SPK_MARRECO")])
R.NPCS["remanso"] = human("remanso", "SPK_REMANSO", [{"dialog": ref("remanso")}])
R.tamer("traira", "traira", "SPK_TRAIRA", "traira", "traira_beaten")
R.tamer("canico", "canico", "SPK_CANICO", "canico", "canico_beaten")
R.tamer("marreco", "marreco", "SPK_MARRECO", "marreco", "marreco_beaten", 3)

# ------------------------------------------------------------------ Brejo Alto
t("SIGN_PA_BREJO", "Brejo Alto. Casa com perna, gente com fôlego.", "Highmarsh. Houses with legs, folks with lungs.", "Ciénaga Alta. Casas con patas, gente con pulmones.")
t("SIGN_PA_CAULDRON", "← Caldeirão da Musga. Fila do remédio: de manhã.", "← Musga's Cauldron. Medicine line: mornings.",
  "← Caldero de Musga. Fila del remedio: por la mañana.")
t("DLG_PA_ARR_BL1", "Casas de perna comprida! Será que elas andam quando ninguém tá olhando?",
  "Long-legged houses! Do you think they walk when nobody's looking?", "¡Casas de patas largas! ¿Caminarán cuando nadie mira?")
t("DLG_PA_ARR_BT1", "Todo mundo tossindo. Isso não é doença. É alguém fazendo.", "Everyone's coughing. That's no sickness. Someone's doing it.",
  "Todos tosiendo. Eso no es enfermedad. Alguien lo está haciendo.")
t("DLG_PA_GARCA_1", "A névoa desce toda noite. De manhã, fila na porta da Musga pra buscar o remédio dela.",
  "The fog rolls in every night. In the morning, everyone lines up at Musga's door for her medicine.",
  "La niebla baja cada noche. Por la mañana, fila en la puerta de Musga para buscar su remedio.")
t("DLG_PA_GARCA_2", "Minha erva amarga acabou. As crianças tossem e eu só tenho chá de capim.", "I'm out of bitterleaf. The kids are coughing and all I have is grass tea.",
  "Se me acabó la hierba amarga. Los niños tosen y solo tengo té de pasto.")
t("DLG_PA_GARCA_ASK", "Você carrega erva amarga... Doaria um pouco pras crianças? Até três maços já curam a rua inteira.",
  "You're carrying bitterleaf... Would you donate some for the kids? Up to three bunches would cure the whole street.",
  "Llevas hierba amarga... ¿Donarías un poco para los niños? Hasta tres manojos curan la calle entera.")
t("DLG_PA_GARCA_NONE", "Se arranjar erva amarga, as crianças agradecem. A Vó Neblina também.", "If you come across bitterleaf, the kids would be grateful. Granny Fog too.",
  "Si consigues hierba amarga, los niños te lo agradecerán. La abuela Neblina también.")
t("DLG_PA_DONATE_1", "Isso cura a rua das crianças inteirinha. E sobra pra Vó Neblina!", "This will cure the whole kids' street. And there's some left for Granny Fog!",
  "Esto cura toda la calle de los niños. ¡Y sobra para la abuela Neblina!")
t("DLG_PA_DONATE_2", "Ela era domadora das boas. Quando melhorar, vai querer te conhecer.", "She was a fine tamer. Once she's better, she'll want to meet you.",
  "Era una domadora de las buenas. Cuando mejore, querrá conocerte.")
t("DLG_PA_KEEP", "Entendo. Estrada longa pede bolso cheio. O chá vai ter que dar conta.", "I understand. A long road calls for full pockets. The tea will have to do.",
  "Entiendo. Camino largo pide bolsillo lleno. El té tendrá que bastar.")
t("DLG_PA_GARCA_AFTER", "A névoa parou! Agora é só esperar a tosse ir embora sozinha.", "The fog stopped! Now we just wait for the coughs to leave on their own.",
  "¡La niebla paró! Ahora solo hay que esperar que la tos se vaya sola.")
t("DLG_PA_JUNCO_1", "Erva amarga? Acabou faz uma semana. A Musga compra tudo pra ninguém mais ter.",
  "Bitterleaf? Sold out a week ago. Musga buys it all so nobody else has any.", "¿Hierba amarga? Se acabó hace una semana. Musga la compra toda para que nadie más tenga.")
t("DLG_PA_JUNCO_2", "Caldo eu tenho. Remédio de verdade, só ela. Esperta, a moça.", "Broth I've got. Real medicine, only she does. Clever girl.",
  "Caldo tengo. Remedio de verdad, solo ella. Lista, la muchacha.")
t("DLG_PA_GIRINO", "Eu prendo a respiração quando a névoa desce. Meu recorde é três segundos.",
  "I hold my breath when the fog comes down. My record is three seconds.", "Aguanto la respiración cuando baja la niebla. Mi récord es tres segundos.")
t("DLG_PA_GIRINO_AFTER", "Agora eu respiro à vontade! Já tô no recorde de mil segundos.", "Now I can breathe all I want! I'm already at a thousand-second record.",
  "¡Ahora respiro todo lo que quiero! Ya voy por el récord de mil segundos.")
t("DLG_PA_SAPE_1", "A Musga é sobrinha do Rei. Dizem que da primeira vez ela se foi sozinha, numa torre que ninguém visitava.",
  "Musga is the King's niece. They say the first time around she passed alone, in a tower nobody visited.",
  "Musga es sobrina del Rey. Dicen que la primera vez se fue sola, en una torre que nadie visitaba.")
t("DLG_PA_SAPE_2", "Gente esquecida faz cada coisa pra ser lembrada...", "Forgotten folks do the strangest things to be remembered...",
  "La gente olvidada hace cada cosa para que la recuerden...")
t("DLG_PA_LODO_1", "Veneno dura de três a cinco turnos. Erva amarga cedo poupa vida; tarde, poupa erva.",
  "Poison lasts three to five turns. Early bitterleaf saves health; late bitterleaf just saves bitterleaf.",
  "El veneno dura de tres a cinco turnos. Hierba amarga temprano ahorra vida; tarde, ahorra hierba.")
t("DLG_PA_LODO_2", "A equipe da Musga se cura enquanto você se envenena. Bate primeiro em quem cura.",
  "Musga's team heals while you get poisoned. Hit the healer first.", "El equipo de Musga se cura mientras tú te envenenas. Golpea primero al que cura.")
t("DLG_PA_PENA_ASK", "O capanga da Musga levou meu malote! Ela lê as cartas de todo mundo.", "Musga's henchman took my mailbag! She reads everybody's letters.",
  "¡El secuaz de Musga se llevó mi saca! Ella lee las cartas de todo el mundo.")
t("DLG_PA_PENA_WHERE", "Fica no Caldeirão, a oeste. Cuidado com o boticário de óculos.", "It's in the Cauldron, to the west. Watch out for the apothecary in glasses.",
  "Está en el Caldero, al oeste. Cuidado con el boticario de gafas.")
t("OBJ_PA_MAILBAG", "O malote da Dona Pena. As cartas estão abertas... e anotadas.", "Mrs. Quill's mailbag. The letters are open... and annotated.",
  "La saca de doña Pluma. Las cartas están abiertas... y anotadas.")
t("DLG_PA_PENA_THANKS", "Meu malote! E olha só: alguém escreveu \"que fofo\" em todas as cartas.",
  "My mailbag! And look: someone wrote \"how sweet\" on every single letter.", "¡Mi saca! Y mira: alguien escribió \"qué tierno\" en todas las cartas.")
t("DLG_PA_PENA_REWARD", "Toma, uma vela de aniversário e duas ervas amargas. Carteira paga em dobro quando a carta chega.",
  "Here, a birthday candle and two bunches of bitterleaf. A mail carrier pays double when the letter arrives.",
  "Toma, una vela de cumpleaños y dos hierbas amargas. La cartera paga el doble cuando llega la carta.")
t("DLG_PA_PENA_AFTER", "Hoje entreguei uma carta até pra Musga. Ela chorou. De alegria, eu acho.",
  "Today I even delivered a letter to Musga. She cried. Happy tears, I think.", "Hoy hasta le entregué una carta a Musga. Lloró. De alegría, creo.")
t("DLG_PA_PENA_WAIT", "Sem malote, sem carta. Sem carta, a vila fica muda.", "No mailbag, no letters. No letters, the village goes quiet.",
  "Sin saca, no hay cartas. Sin cartas, la aldea se queda muda.")
t("DLG_PA_TABOA_1", "Uma envenena, a outra também! Treino de erva amarga, cortesia da casa.", "One poisons, and so does the other! Bitterleaf practice, on the house.",
  "¡Una envenena y la otra también! Práctica de hierba amarga, cortesía de la casa.")
t("DLG_PA_TABOA_2", "Veneno em dobro acaba rápido... pra quem tem erva amarga.", "Double poison ends fast... for those with bitterleaf.",
  "El veneno doble se acaba rápido... para quien tiene hierba amarga.")
t("DLG_PA_BAGRE_1", "Meu Marretão aguenta pancada e meu Regalírio cura. Quero ver você cansar a gente.",
  "My Marretão takes hits and my Regalírio heals. Let's see you wear us down.", "Mi Marretão aguanta golpes y mi Regalírio cura. A ver si nos cansas.")
t("DLG_PA_BAGRE_2", "Cansou a gente. Peixe grande cansa, sabia?", "You wore us down. Big fish get tired too, you know.",
  "Nos cansaste. Los peces grandes también se cansan, ¿sabías?")
t("DLG_PA_NEBLINA_1", "Foi você que mandou as ervas amargas? Que a névoa nunca te ache, criança.",
  "Was it you who sent the bitterleaf? May the fog never find you, child.", "¿Fuiste tú quien mandó las hierbas amargas? Que la niebla nunca te encuentre, criatura.")
t("DLG_PA_NEBLINA_2", "Agradeço do jeito antigo: com uma boa batalha!", "I'll thank you the old way: with a good battle!",
  "Te lo agradezco a la antigua: ¡con una buena batalla!")
t("DLG_PA_NEBLINA_3", "Minha velha Brumaga fugiu pro caldeirão quando a névoa veio. Se ela te achar digno, vai com você.",
  "My old Brumaga fled to the cauldron when the fog came. If she finds you worthy, she'll go with you.",
  "Mi vieja Brumaga huyó al caldero cuando llegó la niebla. Si te encuentra digno, se irá contigo.")

R.d("placa_brejo", [say("SIGN_PA_BREJO")])
R.d("placa_caldeirao", [say("SIGN_PA_CAULDRON")])
R.d("chegada_brejo", [lia("DLG_PA_ARR_BL1"), taro("DLG_PA_ARR_BT1"), flag("brejo_visto")])
R.d("garca", [act("heal"), act("respawn"),
              {"say": "DLG_PA_GARCA_AFTER", "speaker": "SPK_GARCA", "if": "musga_beaten"},
              {"say": "DLG_PA_GARCA_1", "speaker": "SPK_GARCA", "if_not": "musga_beaten"},
              {"say": "DLG_PA_GARCA_2", "speaker": "SPK_GARCA", "if_not": "pantano_escolheu"},
              ask("DLG_PA_GARCA_ASK", "SPK_GARCA", [("OPT_PA_DONATE", ref("doar")), ("OPT_PA_KEEP", ref("guardar"))]) | {"if": "has_antidoto", "if_not": "pantano_escolheu"},
              {"say": "DLG_PA_GARCA_NONE", "speaker": "SPK_GARCA", "if_none": ["has_antidoto", "pantano_escolheu"]},
              goto(ref("garca_rancho"))])
t("DLG_PA_GARCA_3", "Quer deixar algum esqueleto descansando? Cama de palafita balança, mas embala.",
  "Want to leave a skeleton here to rest? Stilt beds sway, but they rock you to sleep.",
  "¿Quieres dejar algún esqueleto descansando? Las camas de palafito se mecen, pero arrullan.")
R.d("garca_rancho", [ask("DLG_PA_GARCA_3", "SPK_GARCA", [("OPT_P_RANCH", "vila_mare/rancho"), ("OPT_P_LEAVE", None)])])
R.d("doar", [act("take_item", item="antidoto", n=3), say("DLG_PA_DONATE_1", "SPK_GARCA"), say("DLG_PA_DONATE_2", "SPK_GARCA"),
             flag("pantano_doou"), flag("red_pantano"), flag("pantano_escolheu"), goto(ref("garca_rancho"))])
R.d("guardar", [say("DLG_PA_KEEP", "SPK_GARCA"), flag("pantano_guardou"), flag("pantano_escolheu"), goto(ref("garca_rancho"))])
R.d("junco", [say("DLG_PA_JUNCO_1", "SPK_JUNCO"), act("shop", id="brejo"), say("DLG_PA_JUNCO_2", "SPK_JUNCO")])
R.d("girino", [{"say": "DLG_PA_GIRINO_AFTER", "speaker": "SPK_GIRINO", "if": "musga_beaten"},
               {"say": "DLG_PA_GIRINO", "speaker": "SPK_GIRINO", "if_not": "musga_beaten"}])
R.d("sape", [say("DLG_PA_SAPE_1", "SPK_SAPE"), say("DLG_PA_SAPE_2", "SPK_SAPE")])
R.d("lodo", [say("DLG_PA_LODO_1", "SPK_LODO"), say("DLG_PA_LODO_2", "SPK_LODO")])
R.d("pena_pede", [say("DLG_PA_PENA_ASK", "SPK_PENA"), flag("pena_quest"), say("DLG_PA_PENA_WHERE", "SPK_PENA")])
R.d("pena_onde", [say("DLG_PA_PENA_WAIT", "SPK_PENA"), say("DLG_PA_PENA_WHERE", "SPK_PENA")])
R.d("pena_obrigada", [say("DLG_PA_PENA_THANKS", "SPK_PENA"), act("take_item", item="malote", n=1), say("DLG_PA_PENA_REWARD", "SPK_PENA"),
                      act("give_item", item="reviver", n=1), act("give_item", item="antidoto", n=2), flag("pena_done")])
R.d("pena_depois", [{"say": "DLG_PA_PENA_AFTER", "speaker": "SPK_PENA", "if": "musga_beaten"},
                    {"say": "DLG_PA_PENA_WAIT", "speaker": "SPK_PENA", "if_not": "musga_beaten"}])
R.d("malote", [say("OBJ_PA_MAILBAG"), act("give_item", item="malote", n=1), flag("malote_pego")])
R.d("taboa", [say("DLG_PA_TABOA_1", "SPK_TABOA"),
              battle("BTL_TAMER_TABOA", team([("lavadeira", 41), ("cogumeleiro", 41)]), 640, "taboa_beaten", [["antidoto", 2]]),
              say("DLG_PA_TABOA_2", "SPK_TABOA")])
R.d("taboa_depois", [say("DLG_PA_TABOA_2", "SPK_TABOA")])
R.d("bagre", [say("DLG_PA_BAGRE_1", "SPK_BAGRE"),
              battle("BTL_TAMER_BAGRE", team([("palafiteiro", 42), ("jardineiro_lirios", 41)]), 660, "bagre_beaten", [["pocao_g", 2]]),
              say("DLG_PA_BAGRE_2", "SPK_BAGRE")])
R.d("bagre_depois", [say("DLG_PA_BAGRE_2", "SPK_BAGRE")])
R.d("neblina", [say("DLG_PA_NEBLINA_1", "SPK_NEBLINA"), say("DLG_PA_NEBLINA_2", "SPK_NEBLINA"),
                battle("BTL_TAMER_NEBLINA", team([("lavadeira", 42), ("jardineiro_lirios", 42)]), 700, "neblina_beaten", [["reviver", 2]]),
                say("DLG_PA_NEBLINA_3", "SPK_NEBLINA")])
R.d("neblina_depois", [say("DLG_PA_NEBLINA_3", "SPK_NEBLINA")])

R.NPCS["garca"] = human("garca", "SPK_GARCA", [{"dialog": ref("garca")}], role="ranch")
R.NPCS["junco"] = human("junco", "SPK_JUNCO", [{"dialog": ref("junco")}], "stand", role="shop")
R.NPCS["girino"] = human("girino", "SPK_GIRINO", [{"dialog": ref("girino")}], role="humor")
R.NPCS["sape"] = human("sape", "SPK_SAPE", [{"dialog": ref("sape")}], "stand", role="lore")
R.NPCS["lodo"] = human("lodo", "SPK_LODO", [{"dialog": ref("lodo")}])
R.NPCS["pena"] = human("pena", "SPK_PENA", [{"if": "pena_done", "dialog": ref("pena_depois")}, {"if": "has_malote", "dialog": ref("pena_obrigada")},
                                           {"if": "pena_quest", "dialog": ref("pena_onde")}, {"dialog": ref("pena_pede")}], role="quest")
R.tamer("taboa", "taboa", "SPK_TABOA", "taboa", "taboa_beaten", 3)
R.tamer("bagre", "bagre", "SPK_BAGRE", "bagre", "bagre_beaten", 3)
R.tamer("neblina", "neblina", "SPK_NEBLINA", "neblina", "neblina_beaten", 3)

# Taro recorrente (parceira Lia): ouviu a fofoca da Musga
t("DLG_PA_TR_1", "Eu ouvi a bruxa da névoa. Castelo. Meus pais tão no castelo.", "I heard the fog witch. The castle. My parents are at the castle.",
  "Oí a la bruja de la niebla. El castillo. Mis padres están en el castillo.")
t("DLG_PA_TR_2", "Não faz essa cara. Eu já sabia que era longe.", "Don't make that face. I already knew it was far.", "No pongas esa cara. Ya sabía que era lejos.")
t("DLG_PA_TR_L", "Taro! A gente vai junto até lá, tá? Ninguém se perde se for junto.", "Taro! We'll go there together, okay? Nobody gets lost if we go together.",
  "¡Taro! Vamos juntos hasta allá, ¿sí? Nadie se pierde si vamos juntos.")
t("DLG_PA_TR_3", "...Tá. Mas eu chego primeiro.", "...Fine. But I'm getting there first.", "...Vale. Pero yo llego primero.")
R.d("taro_brejo", [say("DLG_PA_TR_1", "SPK_TARO"), say("DLG_PA_TR_2", "SPK_TARO"), say("DLG_PA_TR_L", "SPK_LIA"), say("DLG_PA_TR_3", "SPK_TARO"),
                   flag("taro_brejo_visto"), act("hide_npc", id="taro_brejo")])
R.NPCS["taro_brejo"] = skel("skel_taro", "SPK_TARO", [{"dialog": ref("taro_brejo")}])

# ------------------------------------------------------------------ Caldeirão: capanga, malote, Brumaga
t("DLG_PA_ARR_CL1", "Cheira a sopa estragada... e a alguém muito sozinho.", "Smells like spoiled soup... and like someone very lonely.",
  "Huele a sopa echada a perder... y a alguien muy solo.")
t("DLG_PA_ARR_CT1", "Ela tá aí. Dá pra ouvir ela cantando com a panela.", "She's in there. You can hear her singing to the pot.",
  "Está ahí. Se la oye cantándole a la olla.")
t("DLG_PA_FEL_1", "Receita da Musga: uma pitada de névoa, duas de segredo, e nenhum intruso.",
  "Musga's recipe: a pinch of fog, two of secrets, and no intruders.", "Receta de Musga: una pizca de niebla, dos de secreto y ningún intruso.")
t("DLG_PA_FEL_2", "Errei a dose. Pode passar, mas não conta pra ela.", "I got the dose wrong. Go ahead, but don't tell her.",
  "Me equivoqué de dosis. Pasa, pero no se lo cuentes.")
t("DLG_PA_BRUMAGA", "Uma névoa com olhos se enrola nos juncos. Ela te encara... curiosa.", "A fog with eyes curls around the reeds. It stares at you... curious.",
  "Una niebla con ojos se enrosca en los juncos. Te mira... curiosa.")
R.d("chegada_caldeirao", [lia("DLG_PA_ARR_CL1"), taro("DLG_PA_ARR_CT1"), flag("caldeirao_visto")])
R.d("fel", [say("DLG_PA_FEL_1", "SPK_FEL"), battle("BTL_TAMER_FEL", team([("lavadeira", 43), ("gasista", 43)]), 600, "fel_beaten"),
            say("DLG_PA_FEL_2", "SPK_FEL")])
R.d("fel_depois", [say("DLG_PA_FEL_2", "SPK_FEL")])
R.tamer("fel", "fel", "SPK_FEL", "fel", "fel_beaten", 3)
R.d("brumaga", [ask("DLG_PA_BRUMAGA", None, [("OPT_PA_FIGHT_MIST", ref("brumaga_luta")), ("OPT_M_LEAVE", None)])])
R.d("brumaga_luta", [battle("", [["brumaga", 41]], 0, kind="wild")])
R.NPCS["brumaga_npc"] = skel("skel_brumaga", "SPECIES_BRUMAGA", [{"dialog": ref("brumaga")}], role="wild")

# ------------------------------------------------------------------ Guardiã: Musga
t("DLG_PA_MUSGA_1", "Visita! Ninguém me visita, querido. Só vêm buscar remédio e vão embora.", "A visitor! Nobody visits me, darling. They just come for medicine and leave.",
  "¡Una visita! Nadie me visita, querido. Solo vienen por remedio y se van.")
t("DLG_PA_MUSGA_2", "Snif, snif... Que estranho. Você tem cheiro de casa. De família.", "Sniff, sniff... How odd. You smell like home. Like family.",
  "Snif, snif... Qué raro. Hueles a casa. A familia.")
t("DLG_PA_MUSGA_3", "Sabia que a névoa é minha? Quem respira, precisa de mim. Quem precisa, não esquece.",
  "Did you know the fog is mine? Whoever breathes it needs me. Whoever needs me doesn't forget.",
  "¿Sabías que la niebla es mía? Quien la respira me necesita. Quien me necesita, no olvida.")
t("DLG_PA_MUSGA_WIN", "Ai, que deselegante. Ganhar de uma dama no próprio caldeirão.", "Oh, how rude. Beating a lady at her own cauldron.",
  "Ay, qué poco elegante. Ganarle a una dama en su propio caldero.")
t("DLG_PA_MUSGA_MOTIVE", "Da primeira vez, a família me esqueceu numa torre. Mil anos de silêncio. De novo, não, querido.",
  "The first time, the family forgot me in a tower. A thousand years of silence. Not again, darling.",
  "La primera vez, la familia me olvidó en una torre. Mil años de silencio. Otra vez no, querido.")
t("DLG_PA_MUSGA_GOSSIP", "Quer uma fofoca de graça? Os levados, mineiros e pescadores, foram todos pro castelo servir o titio.",
  "Want some free gossip? The ones they took, miners and fishers, all went to the castle to serve my uncle.",
  "¿Quieres un chisme gratis? Los que se llevaron, mineros y pescadores, fueron todos al castillo a servir al tío.")
t("DLG_PA_MUSGA_GOSSIP2", "Os pais daquele baixinho do remo também. Sabia? Eu sei de tudo, querido.",
  "That little one with the oar? His parents too. Did you know? I know everything, darling.",
  "Los padres de ese bajito del remo también. ¿Sabías? Yo lo sé todo, querido.")
t("DLG_PA_MUSGA_T1", "Castelo. Eu sabia.", "The castle. I knew it.", "El castillo. Lo sabía.")
t("DLG_PA_MUSGA_T2", "...Eles tão inteiros. É isso que importa. Vamos.", "...They're in one piece. That's what matters. Let's go.",
  "...Están enteros. Eso es lo que importa. Vamos.")
t("DLG_PA_MUSGA_LT", "Ouviu, Taro? Inteiros! A gente vai junto até o castelo.", "Hear that, Taro? In one piece! We'll go to the castle together.",
  "¿Oíste, Taro? ¡Enteros! Vamos juntos hasta el castillo.")
t("DLG_PA_MUSGA_L1", "Os pais do Taro! A gente precisa contar pra ele!", "Taro's parents! We have to tell him!", "¡Los padres de Taro! ¡Tenemos que contárselo!")
t("DLG_PA_MUSGA_OFF", "Tá bom, tá bom. Desligo a névoa. Mas alguém vai ter que vir me visitar. Combinado?",
  "Fine, fine. I'll turn off the fog. But somebody has to come visit me. Deal?", "Está bien, está bien. Apago la niebla. Pero alguien tendrá que venir a visitarme. ¿Trato?")
t("DLG_PA_MUSGA_AUNT", "A Tia mandou eu comer direito? Ela manda isso há mil anos. Fofa.", "Auntie told me to eat properly? She's been saying that for a thousand years. Sweet.",
  "¿La Tía mandó que coma bien? Lo dice desde hace mil años. Qué tierna.")
t("DLG_PA_MUSGA_AFTER", "Volta pra fofocar, querido. Sabia que o primo Caliço ensaia discurso no espelho?",
  "Come back to gossip, darling. Did you know cousin Caliço rehearses speeches in the mirror?",
  "Vuelve a chismear, querido. ¿Sabías que el primo Caliço ensaya discursos frente al espejo?")
MUSGA_TEAM = [["caldeirona", 47]] + team([("palafiteiro", 48), ("jardineiro_lirios", 47), ("cogumeleiro", 48)])
R.d("musga", [say("DLG_PA_MUSGA_1", "SPK_MUSGA"), say("DLG_PA_MUSGA_2", "SPK_MUSGA"), flag("pista_4"), say("DLG_PA_MUSGA_3", "SPK_MUSGA"),
              battle("BTL_TAMER_MUSGA", MUSGA_TEAM, 1300, "musga_beaten", kind="boss"),
              say("DLG_PA_MUSGA_WIN", "SPK_MUSGA"), say("DLG_PA_MUSGA_MOTIVE", "SPK_MUSGA"), say("DLG_PA_MUSGA_GOSSIP", "SPK_MUSGA"), say("DLG_PA_MUSGA_GOSSIP2", "SPK_MUSGA"),
              taro("DLG_PA_MUSGA_T1"), taro("DLG_PA_MUSGA_T2"), lia("DLG_PA_MUSGA_L1") | {"if_not": "partner_taro"}, say("DLG_PA_MUSGA_LT", "SPK_LIA") | {"if_all": ["partner_lia", "partner_taro"]},
              say("DLG_PA_MUSGA_OFF", "SPK_MUSGA"), {"say": "DLG_PA_MUSGA_AUNT", "speaker": "SPK_MUSGA", "if_any": ["minas_quebrou", "minas_negociou"]},
              act("refresh_map")])
R.d("musga_depois", [say("DLG_PA_MUSGA_AFTER", "SPK_MUSGA")])
R.NPCS["musga"] = {"name_key": "SPK_MUSGA", "role": "guardian", "sprite": "res://assets/sprites/npc/skel_musga.png", "frames": 2, "idle_fps": 2.0,
                   "behavior": "stand", "dialog": [{"if": "musga_beaten", "dialog": ref("musga_depois")}, {"dialog": ref("musga")}],
                   "tamer": {"vision": 3, "flag": "musga_beaten"}}


# ------------------------------------------------------------------ encontros (balance.json: selvagens 33–39)
def e(sp, st, a, b, rar, w=None):
    d = {"species": sp, "stage": st, "min_level": a, "max_level": b, "rarity": rar}
    if w:
        d["weight"] = w
    return d


R.TABLES.update({
    "rota3_sul": [e("lavadeira_2", 2, 33, 35, "comum"), e("palafiteiro_2", 2, 33, 35, "comum")],
    "rota3_oeste": [e("gasista_2", 2, 34, 36, "comum"), e("lavadeira_2", 2, 34, 35, "comum")],
    "rota3_campo": [e("apicultora_2", 2, 34, 36, "incomum"), e("lavadeira_2", 2, 34, 36, "comum"), e("palafiteiro_2", 2, 34, 36, "comum"), e("jardineiro_lirios_2", 2, 34, 36, "incomum"),
                    e("cogumeleiro_2", 2, 34, 36, "incomum"), e("gasista_2", 2, 35, 37, "comum")],
    "rota3_atalho": [e("cogumeleiro_3", 3, 42, 43, "raro", 60), e("jardineiro_lirios_2", 2, 41, 42, "incomum", 40)],
    "rota3_norte": [e("apicultora_2", 2, 36, 38, "raro"), e("palafiteiro_2", 2, 36, 38, "comum"), e("jardineiro_lirios_2", 2, 36, 38, "incomum")],
    "caldeirao_salao": [e("lavadeira_2", 2, 37, 39, "comum"), e("cogumeleiro_2", 2, 37, 39, "incomum"), e("gasista_2", 2, 37, 39, "comum")],
    "caldeirao_sul": [e("jardineiro_lirios_2", 2, 38, 39, "incomum"), e("palafiteiro_2", 2, 38, 39, "comum")],
})
R.SHOPS["brejo"] = ["pocao_m", "pocao_g", "reviver"]

# ------------------------------------------------------------------ mapas
LEG = {"g": "mud", "f": "grass", "B": "swamp", "p": "dock", ".": "floor"}
rota = make_route("rota_3", "pantano", "MAP_ROTA_3", LEG, ("brasal", 19, 1), ("brejo", 19, 30),
                  gate={"type": "rubble", "if_not": "has_martelo_tia", "dialog": R.ref("entulho")},
                  tamers=[("traira", {}), ("canico", {}), ("marreco", {})], hint="remanso", sign=R.ref("placa_bifurcacao"),
                  spawns=[{"id": "r3_sul", "table": "rota3_sul", "x": 10, "y": 45, "radius": 3, "count": 2},
                          {"id": "r3_oeste", "table": "rota3_oeste", "x": 5, "y": 25, "radius": 2, "count": 1},
                          {"id": "r3_campo_a", "table": "rota3_campo", "x": 30, "y": 32, "radius": 4, "count": 3},
                          {"id": "r3_campo_b", "table": "rota3_campo", "x": 30, "y": 18, "radius": 4, "count": 3},
                          {"id": "r3_atalho", "table": "rota3_atalho", "x": 19, "y": 25, "radius": 2, "count": 1},
                          {"id": "r3_norte", "table": "rota3_norte", "x": 10, "y": 6, "radius": 3, "count": 2}],
                  extra_props=[{"type": "swamp_lantern", "x": 18, "y": 37}, {"type": "swamp_lantern", "x": 21, "y": 13},
                               {"type": "lilypad", "x": 12, "y": 20}, {"type": "lilypad", "x": 15, "y": 28}, {"type": "lilypad", "x": 23, "y": 22},
                               {"type": "lilypad", "x": 11, "y": 33}, {"type": "willow", "x": 30, "y": 25}, {"type": "reeds", "x": 36, "y": 14},
                               {"type": "reeds", "x": 27, "y": 35}],
                  deco=("reeds", "dead_tree", "reeds", "willow"), tint=[0.84, 0.94, 0.84], seed=41)
rota["on_enter"] = [{"if_not": "rota3_vista", "dialog": R.ref("chegada_rota")}]
rota["ambient"] = ["mist"]

town = make_town("brejo", "pantano", "MAP_BREJO", dict(LEG, s="dock"),
                 south=("rota_3", 19, 1), north=("rota_4", 19, 48), west=("caldeirao", 32, 10),
                 houses=["stilt_house_ranch", "stilt_house_shop", "stilt_house", "stilt_house", "stilt_house"],
                 npcs=[{"id": "girino", "x": 16, "y": 16, "facing": "right"}, {"id": "sape", "x": 24, "y": 13, "facing": "down"},
                       {"id": "lodo", "x": 22, "y": 18, "facing": "left"}, {"id": "pena", "x": 17, "y": 22, "facing": "down"},
                       {"id": "taro_brejo", "x": 21, "y": 3, "facing": "down", "if_all": ["partner_lia", "musga_beaten"], "if_none": ["partner_taro", "taro_brejo_visto"]}],
                 props=[{"type": "sign", "x": 18, "y": 28, "dialog": R.ref("placa_brejo")}, {"type": "sign", "x": 3, "y": 14, "dialog": R.ref("placa_caldeirao")},
                        {"type": "swamp_lantern", "x": 13, "y": 13}, {"type": "swamp_lantern", "x": 26, "y": 13}, {"type": "well", "x": 22, "y": 15},
                        {"type": "boat", "x": 5, "y": 27}, {"type": "lilypad", "x": 34, "y": 26}],
                 deco=("reeds", "willow", "dead_tree"), tint=[0.82, 0.92, 0.84], seed=51, plaza="s")
for w in town["warps"]:
    if w["to"] == "rota_4":
        w["if"] = "musga_beaten"
        w["locked_message"] = "MSG_MUSGA_ROAD"
town["ambient"] = ["mist"]
town["on_enter"] = [{"if_not": "brejo_visto", "dialog": R.ref("chegada_brejo")}]
town_doors(town, "brejo", {"rancho": "brejo_rancho", "loja": "brejo_loja", "a": "brejo_casa_taboa", "b": "brejo_casa_bagre", "c": "brejo_casa_neblina"})
for w in town["warps"]:
    if w["to"] == "brejo_casa_neblina":
        w["if"] = "pantano_doou"
        w["locked_message"] = "MSG_NEBLINA_DOOR"

lair = make_lair("caldeirao", "pantano", "MAP_CALDEIRAO", dict(LEG, f="grass"), east=("brejo", 1, 15),
                 guardian_npc={"id": "musga", "x": 10, "y": 3, "facing": "down"},
                 extra_npcs=[{"id": "fel", "x": 14, "y": 10, "facing": "right"},
                             {"id": "brumaga_npc", "x": 9, "y": 15, "facing": "left", "if": "pantano_doou"}],
                 props=[{"type": "cauldron", "x": 10, "y": 1}, {"type": "willow", "x": 5, "y": 3}, {"type": "dead_tree", "x": 15, "y": 3},
                        {"type": "swamp_lantern", "x": 18, "y": 7}, {"type": "swamp_lantern", "x": 27, "y": 8}, {"type": "reeds", "x": 22, "y": 13},
                        {"type": "reeds", "x": 4, "y": 19}, {"type": "reeds", "x": 12, "y": 18}, {"type": "lilypad", "x": 2, "y": 15},
                        {"type": "mail_bag", "x": 26, "y": 12, "dialog": R.ref("malote"), "if": "pena_quest", "if_not": "malote_pego"}],
                 spawns=[{"id": "cald_salao", "table": "caldeirao_salao", "x": 23, "y": 10, "radius": 3, "count": 2},
                         {"id": "cald_sul", "table": "caldeirao_sul", "x": 6, "y": 15, "radius": 2, "count": 1}],
                 tint=[0.7, 0.82, 0.7])
lair["ambient"] = ["mist"]
lair["on_enter"] = [{"if_not": "caldeirao_visto", "dialog": R.ref("chegada_caldeirao")}]

R.MAPS.update({
    "rota_3": rota, "brejo": town, "caldeirao": lair,
    "brejo_rancho": room("brejo_rancho", "pantano", "MAP_BREJO_RANCHO", "brejo", (12, 10),
                         [{"type": "bed", "x": 2, "y": 3}, {"type": "bed", "x": 4, "y": 3}, {"type": "plant", "x": 10, "y": 2}, {"type": "rug", "x": 6, "y": 6}],
                         [{"id": "garca", "x": 7, "y": 3, "facing": "down"}]),
    "brejo_loja": room("brejo_loja", "pantano", "MAP_BREJO_LOJA", "brejo", (27, 10),
                       [{"type": "shelf", "x": 3, "y": 2}, {"type": "shelf", "x": 10, "y": 2}, {"type": "table", "x": 7, "y": 4}, {"type": "barrel", "x": 1, "y": 7}],
                       [{"id": "junco", "x": 6, "y": 3, "facing": "down"}]),
    "brejo_casa_taboa": room("brejo_casa_taboa", "pantano", "MAP_BREJO_CASA_TABOA", "brejo", (8, 20),
                             [{"type": "table", "x": 7, "y": 5}, {"type": "reeds", "x": 2, "y": 3}, {"type": "plant", "x": 10, "y": 7}],
                             [{"id": "taboa", "x": 6, "y": 3, "facing": "down"}]),
    "brejo_casa_bagre": room("brejo_casa_bagre", "pantano", "MAP_BREJO_CASA_BAGRE", "brejo", (31, 20),
                             [{"type": "rod_rack", "x": 2, "y": 3}, {"type": "barrel", "x": 10, "y": 7}, {"type": "table", "x": 7, "y": 5}],
                             [{"id": "bagre", "x": 6, "y": 3, "facing": "down"}]),
    "brejo_casa_neblina": room("brejo_casa_neblina", "pantano", "MAP_BREJO_CASA_NEBLINA", "brejo", (14, 27),
                               [{"type": "bed", "x": 2, "y": 3}, {"type": "plant", "x": 10, "y": 2}, {"type": "lamp", "x": 1, "y": 7}],
                               [{"id": "neblina", "x": 6, "y": 3, "facing": "down"}]),
})
R.BATTLE_BG["pantano"] = "res://assets/battle/bg_pantano.png"
R.CITIES.append({"id": "brejo", "map": "brejo", "ranch": "garca", "shop": "brejo", "tamer_houses": ["taboa", "bagre", "neblina"],
                 "npcs": ["girino", "sape", "lodo", "pena"], "quests": ["pena", "garca"]})
R.ROUTES.append({"id": "rota_3", "map": "rota_3", "from": "brasal", "to": "brejo",
                 "paths": [{"kind": "domadores", "required": False}, {"kind": "selvagem", "required": False},
                           {"kind": "atalho", "required": False, "note": "Passagem do Desmoronamento: exige o Martelo da Tia (escolha 2)"}]})

# ------------------------------------------------------------------ documento
R.DOC = {
    "title": "Ato 3: Rota 3 e Pântano Verde-Musgo", "phase": "4d", "duration": "25 min",
    "ages": "chegada 34–42; selvagens 33–39; domadores 36–43; Guardiã ~48",
    "problem": "Toda noite a **névoa verde** do caldeirão da Guardiã **Musga** desce sobre **Brejo Alto**. Quem respira tosse, e de manhã a vila faz fila na porta dela "
               "para buscar o remédio que só ela sabe fazer. Quem sai da vila perde a dose do dia: \"Ninguém sai, ninguém se perde\" do jeito da Musga. "
               "O Rancho e a loja estão sem erva amarga (ela compra todos). A névoa também esconde a estrada do norte.",
    "clue_n": 4,
    "clue": "Antes da luta, a Musga **cheira o ar** e diz: \"Você tem cheiro de casa. De família.\" Os esqueletos da família real sentem os parentes: "
            "o protagonista é do sangue do Rei.",
    "moment": ["**Taro** descobre pela fofoca da Musga que os levados (inclusive os pais dele) estão **no castelo**. Parceiro: \"Castelo. Eu sabia... Eles tão inteiros.\" "
               "Recorrente (parceira Lia): Lia quer contar a ele; Taro aparece na saída norte, já sabendo, e aceita seguir junto (\"Mas eu chego primeiro\").",
               "**Lia** (parceira) vê os vaga-lumes da Rota 3: \"acendem um pro outro achar o caminho\", o mesmo desejo do farol.",
               "Lia e Taro estão os dois na equipe (decisão do Fernando): tocam as falas de parceiro dos dois; as cenas de \"recorrente\" só aparecem em saves antigos, com um parceiro só.", "Arco de Taro: raiva → entendimento começa (os pais estão vivos, servindo, como a família do Rei)."],
    "guardian": {"name": "Musga (sobrinha do Rei)", "kin": "sobrinha",
                 "personality": "irônica, fofoqueira, solitária; chama todo mundo de \"querido\" e solta fofocas (o tique dela)",
                 "motive": "**Medo** de ser esquecida de novo: da primeira vez morreu sozinha numa torre. \"Quem precisa de mim não me esquece.\"",
                 "mechanic": "**Veneno e cura.** A equipe envenena e se cura (Ervaçal, Regalírio). Ensina o **tempo do veneno** (3–5 turnos), o uso de "
                             "**ervas amargas** e a bater primeiro em quem cura. Lodo e as Irmãs Taboa dão a dica.",
                 "team": "Ervaçal 49, Marretão 48, Regalírio 47, Cogumestre 48.",
                 "reward": "1300 moedas; a névoa para e a estrada norte (Rota 4) aparece."},
    "maps": [("**Rota 3** (`rota_3`)", "Sai de Brasal (depois da Tia). 3 caminhos: **Trilha das Tábuas** (oeste: Traíra, Caniço, Marreco), **Capinzal** (leste, mais selvagens) "
              "e **Passagem do Desmoronamento** (centro: entulho que só some com o **Martelo da Tia**, com um selvagem forte). Placa e o Barqueiro Remanso dão a dica."),
             ("**Brejo Alto** (`brejo`)", "Vila de palafitas: Rancho (Garça, onde acontece a escolha 3), Loja sem erva amarga (Junco), casas das Irmãs Taboa e do Bagre, "
              "a casa da Vó Neblina (abre se você doar), NPCs, missão do malote e saída oeste para o Caldeirão."),
             ("**Caldeirão da Musga** (`caldeirao`)", "Salão com selvagens, o malote roubado, Boticário Fel, câmara sul (Brumaga, se você doou) e o caldeirão da Musga ao norte."),
             ("Interiores", "Rancho da Garça, Venda do Junco, casas das Irmãs Taboa, do Bagre e da Vó Neblina.")],
}
R.NPC_DOC = [
    ("Barqueiro Remanso", "dica", "Explica os 3 caminhos e reconhece o Martelo da Tia"),
    ("Traíra, Caniço, Marreco", "domadores da rota", "Trilha das Tábuas; Marreco dá ervas amargas (que podem ir para a doação)"),
    ("Dona Garça", "Rancho + escolha 3", "Cura; pede os ervas amargas para as crianças"),
    ("Seu Junco", "Loja", "Mostra o problema: a Musga compra todo erva amarga"),
    ("Girino", "humor", "Recorde de fôlego; muda depois da Guardiã"),
    ("Seu Sapé", "lore", "Conta como a Musga morreu esquecida numa torre"),
    ("Lodo", "dica", "Ensina o tempo do veneno e a bater em quem cura"),
    ("Dona Pena", "missão", "Malote roubado: mostra a solidão da Musga (\"que fofo\" nas cartas)"),
    ("Boticário Fel", "capanga", "Guarda o caminho até o caldeirão"),
    ("Musga", "Guardiã", "Veneno e cura; pista 4; fofoca que move o arco do Taro"),
]
R.HOUSES = [
    ("Irmãs Taboa", "Veneno em dobro (Ervaçal + Esporito)", "640 moedas + 2 Ervas Amargas"),
    ("Pescador Bagre", "Aguentar e curar (Marretão + Regalírio)", "660 moedas + 2 Fatias de Bolo"),
    ("Vó Neblina (só se doar)", "Névoa: veneno e cura (Ervaçal + Regalírio)", "700 moedas + 2 Vela de Aniversário; conta onde está a Brumaga"),
]
R.CHOICES = [
    ("Caminho da Rota 3", "Tábuas / Capinzal / Desmoronamento", "Moedas e itens / XP e marcadores / curto, só com o Martelo da Tia"),
    ("**Escolha 3: os ervas amargas**", "Doar / Guardar",
     "Doar (até 3): as crianças e a Vó Neblina se curam, a casa dela abre (3ª casa de domadores) e a única **Brumaga** aparece no Caldeirão; **+1 Redenção** (`red_pantano`). "
     "Guardar: você fica com os itens."),
    ("Missão do malote", "Fazer / ignorar", "1 Vela de Aniversário + 2 Ervas Amargas (que podem ajudar na doação)"),
]

if __name__ == "__main__":
    R.write()
