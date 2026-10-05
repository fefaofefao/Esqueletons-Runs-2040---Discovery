#!/usr/bin/env python3
"""Falas transversais (fase 4h): o mundo reage à história em todas as regiões.
  - o parceiro comenta a 1ª visita ao Prólogo e ao Bosque;
  - NPCs da Vila Maré e de Raizal mudam de fala depois do Brás e do Ramalho;
  - cartas do Bento chegam ao Rancho de cada cidade depois do Guardião;
  - pós-jogo: falas novas de lore em todas as cidades, Lia no farol e a
    família do Taro na Vila Maré.
Roda depois de todas as regiões (tools/maps/build_all.py) porque acrescenta
entradas às listas de diálogo de NPCs e mapas que as outras fontes gravam."""
import json

from regionkit import ROOT, Region, say, act, flag, goto, human, skel

R = Region("extras", 9, "extras", [])
t = R.t
ref = R.ref


def lia(k):
    return say(k, "SPK_LIA") | {"if": "partner_lia"}


def taro(k):
    return say(k, "SPK_TARO") | {"if": "partner_taro"}


MAP_ENTER = {}     # mapa -> entrada de on_enter (vai para o início da lista)
NPC_PRE = {}       # npc -> entrada de diálogo (vai para o início da lista)
MAP_NPCS = {}      # mapa -> NPCs novos

# ------------------------------------------------------------------ o parceiro comenta (Prólogo e Bosque)
for mid, key, lia_lines, taro_lines in [
    ("vila_mare", "VILA", [("Uma vila de verdade! Tem cheiro de peixe e de pão. Qual dos dois a gente come primeiro?",
                            "A real village! It smells like fish and bread. Which one do we eat first?",
                            "¡Un pueblo de verdad! Huele a pescado y a pan. ¿Cuál comemos primero?")],
     [("Barcos parados. Gente parada. Esse lugar tá esperando alguém fazer alguma coisa.",
       "Boats stuck. People stuck. This place is waiting for someone to do something.",
       "Barcos parados. Gente parada. Este lugar está esperando que alguien haga algo.")]),
    ("rota_1", "ROTA1", [("Árvores! Lá na praia só tinha coqueiro. Essas têm braço pra todo lado.",
                          "Trees! The beach only had palms. These have arms everywhere.", "¡Árboles! En la playa solo había palmeras. Estos tienen brazos por todos lados."),
                         ("Será que elas lembram de quando eram sementinhas?", "Do you think they remember being little seeds?", "¿Se acordarán de cuando eran semillitas?")],
     [("Três caminhos. Eu ia pelo do meio, mas tá cheio de raiz.", "Three paths. I'd take the middle one, but it's full of roots.",
       "Tres caminos. Iría por el del medio, pero está lleno de raíces.")]),
    ("raizal", "RAIZAL", [("Cheiro de chá e de madeira molhada. Eu gosto daqui.", "Smells like tea and wet wood. I like it here.",
                           "Huele a té y a madera mojada. Me gusta este lugar.")],
     [("Raiz em cima de raiz. Isso não é floresta, é prisão com folha.", "Roots on top of roots. This isn't a forest, it's a jail with leaves.",
       "Raíz sobre raíz. Esto no es un bosque, es una cárcel con hojas.")]),
    ("bosque_velho", "BVELHO", [("Shhh... Esse lugar parece que tá dormindo.", "Shhh... This place feels like it's asleep.", "Shhh... Este lugar parece estar dormido.")],
     [("Tem alguém grande aqui. Dá pra sentir no chão.", "Someone big is here. You can feel it in the ground.", "Hay alguien grande aquí. Se siente en el suelo.")]),
]:
    nodes = []
    for i, (pt, en, es) in enumerate(lia_lines):
        nodes.append(lia(t(f"DLG_X_ARR_{key}_L{i}", pt, en, es)))
    for i, (pt, en, es) in enumerate(taro_lines):
        nodes.append(taro(t(f"DLG_X_ARR_{key}_T{i}", pt, en, es)))
    nodes.append(flag(f"x_{mid}_visto"))
    R.d(f"chegada_{mid}", nodes)
    MAP_ENTER[mid] = {"if": "has_partner", "if_not": f"x_{mid}_visto", "dialog": ref(f"chegada_{mid}")}

# ------------------------------------------------------------------ o mundo reage (Vila Maré depois do Brás; Raizal depois do Ramalho)
for npc, cond, spk, pt, en, es in [
    ("marola", "bras_beaten", "SPK_MAROLA", "O cais abriu! Hoje teve peixe fresco no Rancho. Os esqueletos só comeram o cheiro, mas adoraram.",
     "The dock is open! We had fresh fish at the Ranch today. The skeletons only ate the smell, but they loved it.",
     "¡El muelle abrió! Hoy hubo pescado fresco en el Rancho. Los esqueletos solo se comieron el olor, pero les encantó."),
    ("anzol", "bras_beaten", "SPK_ANZOL", "Com o cais aberto, chegou anzol novo. Pena que eu vendo poção.",
     "With the dock open, new fishhooks arrived. Shame I sell potions.", "Con el muelle abierto llegaron anzuelos nuevos. Lástima que yo venda pociones."),
    ("pipa", "bras_beaten", "SPK_PIPA", "Meu esqueleto ficou mais rápido. Ou eu fiquei mais lenta? Tô confusa.",
     "My skeleton got faster. Or did I get slower? I'm confused.", "Mi esqueleto se volvió más rápido. ¿O yo más lenta? Estoy confundida."),
    ("cascalho", "bras_beaten", "SPK_CASCALHO", "O Brás perdeu? Então a lei do Rei tem fresta. Toda lei tem, jovem.",
     "Brás lost? Then the King's law has a crack. Every law does, young one.", "¿Brás perdió? Entonces la ley del Rey tiene una grieta. Toda ley la tiene, joven."),
    ("tilia", "ramalho_beaten", "SPK_TILIA", "As raízes soltaram! Hoje mesmo mandei o primeiro doente pra casa, andando.",
     "The roots let go! Today I sent my first patient home, on foot.", "¡Las raíces se soltaron! Hoy mismo mandé al primer enfermo a casa, caminando."),
    ("toco", "ramalho_beaten", "SPK_TOCO", "Estrada aberta, preço baixando. Não muito. Um pouquinho.", "Road open, prices dropping. Not much. A tiny bit.",
     "Camino abierto, precios bajando. No mucho. Un poquito."),
    ("graveto", "ramalho_beaten", "SPK_GRAVETO", "As raízes foram embora levando a minha marca de dente. Que orgulho.",
     "The roots left, taking my tooth marks with them. So proud.", "Las raíces se fueron llevándose mis marcas de dientes. Qué orgullo."),
    ("hera", "ramalho_beaten", "SPK_HERA", "O Ramalho veio pedir desculpas pra vila. Trouxe lenha. Primo do Rei, mas educado.",
     "Ramalho came to apologize to the village. He brought firewood. The King's cousin, but polite.",
     "Ramalho vino a pedirle disculpas al pueblo. Trajo leña. Primo del Rey, pero educado."),
    ("lenhador_velho", "ramalho_beaten", "SPK_LENHADOR_VELHO", "Estrada livre de novo. Agora só falta eu lembrar onde deixei o machado.",
     "The road's clear again. Now I just need to remember where I left my axe.", "El camino está libre otra vez. Ahora solo me falta recordar dónde dejé el hacha."),
]:
    k = t(f"DLG_X_REACT_{npc.upper()}", pt, en, es)
    npc_data = json.loads((ROOT / "data/npcs.json").read_text())["npcs"][npc]
    original = [x for x in npc_data["dialog"] if not str(x.get("dialog", "")).startswith("extras/")][-1]["dialog"]
    R.d(f"reage_{npc}", [say(k, spk), goto(original)])
    NPC_PRE.setdefault(npc, []).append({"if": cond, "if_not": "game_cleared", "dialog": ref(f"reage_{npc}")})

# ------------------------------------------------------------------ cartas do Bento (no Rancho, depois de cada Guardião)
t("DLG_X_LETTER", "Chegou carta pra você! Do tal do Bento, lá da praia. Lê aí.", "A letter came for you! From that Bento fellow, down by the beach. Go ahead and read it.",
  "¡Te llegó una carta! De un tal Bento, allá de la playa. Léela.")
LETTERS = [
    ("tilia", "ramalho_beaten", "SPK_TILIA",
     ("\"Moleque! O cais abriu e a Jurema pescou um peixe do tamanho do Brás. O Brás não gostou da comparação.\"",
      "\"Kid! The dock opened and Jurema caught a fish the size of Brás. Brás didn't like the comparison.\"",
      "\"¡Chaval! El muelle abrió y Jurema pescó un pez del tamaño de Brás. A Brás no le gustó la comparación.\""),
     ("\"Rede boa não é a mais forte, é a que tem nó bem dado. Cuida do teu parceiro. Bento.\"",
      "\"A good net isn't the strongest one, it's the one with well-tied knots. Look after your partner. Bento.\"",
      "\"La buena red no es la más fuerte, es la de nudos bien hechos. Cuida a tu compañero. Bento.\"")),
    ("rubi", "fornalha_beaten", "SPK_RUBI",
     ("\"A Marola jura que esqueleto cresce mais rápido quando é bem tratado. Eu juro que é a sopa dela.\"",
      "\"Marola swears skeletons grow faster when treated well. I swear it's her soup.\"",
      "\"Marola jura que los esqueletos crecen más rápido si los tratan bien. Yo juro que es su sopa.\""),
     ("\"Ouvi falar de mina e fumaça. Mar calmo nunca fez bom marinheiro. Segue em frente. Bento.\"",
      "\"I heard about mines and smoke. Calm seas never made a good sailor. Keep going. Bento.\"",
      "\"Oí hablar de minas y humo. El mar en calma nunca hizo buen marinero. Sigue adelante. Bento.\"")),
    ("garca", "musga_beaten", "SPK_GARCA",
     ("\"Chegou chá de Raizal aqui. Tá todo mundo tomando, até quem não tava doente.\"",
      "\"Tea arrived here from Rootvale. Everyone's drinking it, even those who weren't sick.\"",
      "\"Llegó té de Raizal. Todos lo están tomando, hasta los que no estaban enfermos.\""),
     ("\"Uma coisa que eu não te contei: aquele teu papel de 'museu' tem o desenho do farol velho. Pensa nisso. Bento.\"",
      "\"Something I never told you: that 'museum' paper of yours has the old lighthouse drawn on it. Think about it. Bento.\"",
      "\"Algo que no te conté: ese papel tuyo del 'museo' tiene el dibujo del faro viejo. Piénsalo. Bento.\"")),
    ("ameia", "calico_beaten", "SPK_AMEIA",
     ("\"Meu avô dizia que o mar já foi de um rei menino que só olhava pra ele. Nunca entendi. Agora acho que entendo.\"",
      "\"My grandpa used to say the sea once belonged to a boy king who only gazed at it. I never understood. Now I think I do.\"",
      "\"Mi abuelo decía que el mar fue de un rey niño que solo lo miraba. Nunca lo entendí. Ahora creo que sí.\""),
     ("\"Se descobriu alguma coisa sobre você, guarda com carinho. Ou conta. Tu que sabe. Bento.\"",
      "\"If you found out something about yourself, keep it close. Or share it. Your call. Bento.\"",
      "\"Si descubriste algo sobre ti, guárdalo con cariño. O cuéntalo. Tú decides. Bento.\"")),
    ("lareira", "alva_beaten", "SPK_LAREIRA",
     ("\"Esfriou por aqui também. A vila fez fogueira na praia e cantou. O Brás cantou desafinado, claro.\"",
      "\"It got cold here too. The village built a bonfire on the beach and sang. Brás sang off-key, of course.\"",
      "\"Aquí también refrescó. El pueblo hizo una fogata en la playa y cantó. Brás desafinó, claro.\""),
     ("\"Tô velho, mas reconheço quem tá chegando perto do fim da viagem. Não corre. Chega. Bento.\"",
      "\"I'm old, but I can tell when someone's nearing the end of a journey. Don't rush. Arrive. Bento.\"",
      "\"Estoy viejo, pero reconozco a quien se acerca al final del viaje. No corras. Llega. Bento.\"")),
    ("moringa", "duna_beaten", "SPK_MORINGA",
     ("\"Subi no farol pra limpar a lente. Pela primeira vez, ela brilhou um pouquinho. Sozinha.\"",
      "\"I climbed the lighthouse to clean the lens. For the first time, it glowed a little. On its own.\"",
      "\"Subí al faro a limpiar la lente. Por primera vez, brilló un poquito. Sola.\""),
     ("\"Seja o que for que te espera no castelo: quem tem pra onde voltar nunca tá perdido. Bento.\"",
      "\"Whatever waits for you at the castle: whoever has somewhere to return to is never lost. Bento.\"",
      "\"Sea lo que sea que te espera en el castillo: quien tiene adónde volver nunca está perdido. Bento.\"")),
]
for i, (npc, cond, spk, a, b) in enumerate(LETTERS, 1):
    ka = t(f"DLG_X_LETTER_{i}A", *a)
    kb = t(f"DLG_X_LETTER_{i}B", *b)
    npc_data = json.loads((ROOT / "data/npcs.json").read_text())["npcs"][npc]
    original = [x for x in npc_data["dialog"] if not str(x.get("dialog", "")).startswith("extras/")][-1]["dialog"]
    R.d(f"carta_{i}", [say("DLG_X_LETTER", spk), say(ka), say(kb), flag(f"carta_bento_{i}"), goto(original)])
    NPC_PRE.setdefault(npc, []).insert(0, {"if": cond, "if_not": f"carta_bento_{i}", "dialog": ref(f"carta_{i}")})

# ------------------------------------------------------------------ pós-jogo: o mundo sem coroa
for npc, spk, pt, en, es in [
    ("cascalho", "SPK_CASCALHO", "Esqueletos livres, fazendo aniversário em paz de novo. Era só isso que eu queria ver antes de virar um.",
     "Free skeletons, celebrating birthdays in peace again. That's all I wanted to see before becoming one.",
     "Esqueletos libres, celebrando cumpleaños en paz otra vez. Era lo único que quería ver antes de convertirme en uno."),
    ("hera", "SPK_HERA", "Sem coroa, os esqueletos do Bosque ficaram. Por amizade. Isso vale mais que qualquer ordem.",
     "Without the crown, the Forest skeletons stayed. Out of friendship. That's worth more than any order.",
     "Sin corona, los esqueletos del Bosque se quedaron. Por amistad. Eso vale más que cualquier orden."),
    ("turmalina", "SPK_TURMALINA", "O sino da cidade tocou sozinho no dia em que a coroa quebrou. Acho que foi a Tia se despedindo.",
     "The town bell rang by itself the day the crown broke. I think it was Auntie saying goodbye.",
     "La campana del pueblo sonó sola el día que se rompió la corona. Creo que era la Tía despidiéndose."),
    ("sape", "SPK_SAPE", "A névoa nunca mais voltou. Mas às vezes alguém escreve \"que fofo\" nas cartas. Não sei quem.",
     "The fog never came back. But sometimes someone writes \"how sweet\" on the letters. I don't know who.",
     "La niebla nunca volvió. Pero a veces alguien escribe \"qué tierno\" en las cartas. No sé quién."),
    ("brasao", "SPK_BRASAO", "O menino que só olhava o mar agora viaja com você. Eu sabia que um dia ele saía desse pátio.",
     "The boy who only gazed at the sea now travels with you. I knew one day he'd leave this courtyard.",
     "El niño que solo miraba el mar ahora viaja contigo. Sabía que un día saldría de este patio."),
    ("pinhao", "SPK_PINHAO", "Primavera nos picos! A primeira em mil anos. As flores nem sabem direito o que fazer.",
     "Spring on the peaks! The first in a thousand years. The flowers don't quite know what to do.",
     "¡Primavera en los picos! La primera en mil años. Las flores no saben muy bien qué hacer."),
    ("miragem", "SPK_MIRAGEM", "Os tambores tocam toda noite agora. Sempre com uma batida a mais. Pela rainha.",
     "The drums play every night now. Always with one extra beat. For the queen.",
     "Los tambores suenan todas las noches. Siempre con un golpe de más. Por la reina."),
]:
    k = t(f"DLG_X_POST_{npc.upper()}", pt, en, es)
    R.d(f"pos_{npc}", [say(k, spk)])
    NPC_PRE.setdefault(npc, []).insert(0, {"if": "game_cleared", "dialog": ref(f"pos_{npc}")})

# Lia no farol (quando o parceiro é o Taro) e a família do Taro na Vila Maré (quando a parceira é a Lia)
t("DLG_X_LIA_FAROL_1", "Fui eu! Subi os duzentos degraus sozinha, no escuro. Nem tremi. Quer dizer, tremi um pouquinho.",
  "It was me! I climbed the two hundred steps alone, in the dark. Didn't even shake. Well, I shook a little.",
  "¡Fui yo! Subí los doscientos escalones sola, a oscuras. Ni temblé. Bueno, temblé un poquito.")
t("DLG_X_LIA_FAROL_2", "Agora, quando alguém se perder, é só olhar pra cá. Até você, se um dia voltar pra 2040.",
  "Now, whenever someone gets lost, they just have to look this way. Even you, if you ever go back to 2040.",
  "Ahora, cuando alguien se pierda, solo tiene que mirar hacia aquí. Hasta tú, si algún día vuelves a 2040.")
t("DLG_X_PAIS_1", "Você é o amigo do nosso Taro! Ele fala de você o tempo todo. Bom, \"o tempo todo\" pro Taro é três frases.",
  "You're our Taro's friend! He talks about you all the time. Well, \"all the time\" for Taro is three sentences.",
  "¡Eres el amigo de nuestro Taro! Habla de ti todo el tiempo. Bueno, \"todo el tiempo\" para Taro son tres frases.")
t("DLG_X_PAIS_2", "Estamos fazendo os cem bolos que devemos. Já vamos no sétimo.", "We're baking the hundred cakes we owe him. We're on number seven.",
  "Estamos haciendo los cien pasteles que le debemos. Vamos por el séptimo.")
t("DLG_X_TARO_VILA", "Eles tão aqui. Inteiros. ...Eu tô bem. Para de me olhar assim.", "They're here. In one piece. ...I'm fine. Stop looking at me like that.",
  "Están aquí. Enteros. ...Estoy bien. Deja de mirarme así.")
R.d("lia_farol", [say("DLG_X_LIA_FAROL_1", "SPK_LIA"), say("DLG_X_LIA_FAROL_2", "SPK_LIA")])
R.d("pais_vila", [say("DLG_X_PAIS_1", "SPK_MAE_TARO"), say("DLG_X_PAIS_2", "SPK_PAI_TARO")])
R.d("taro_vila", [say("DLG_X_TARO_VILA", "SPK_TARO")])
R.NPCS["lia_farol"] = skel("skel_faroleira_3", "SPK_LIA", [{"dialog": ref("lia_farol")}])
R.NPCS["pais_vila"] = skel("skel_grumete_3", "SPK_MAE_TARO", [{"dialog": ref("pais_vila")}])
R.NPCS["taro_vila"] = skel("skel_grumete_3", "SPK_TARO", [{"dialog": ref("taro_vila")}])
MAP_NPCS["praia_despertar"] = [{"id": "lia_farol", "x": 8, "y": 17, "facing": "down", "if_all": ["game_cleared", "partner_taro"]}]
MAP_NPCS["vila_mare"] = [{"id": "pais_vila", "x": 23, "y": 15, "facing": "down", "if": "game_cleared"},
                         {"id": "taro_vila", "x": 24, "y": 15, "facing": "down", "if_all": ["game_cleared", "partner_lia"]}]

# ------------------------------------------------------------------ células livres para os NPCs e objetos novos
_TS = json.loads((ROOT / "data/tilesets/overworld.json").read_text())["terrains"]
_PROPS = json.loads((ROOT / "data/props.json").read_text())["props"]


def free_cell(mid, near, extra_taken=()):
    """Célula andável mais próxima de 'near' (sem objeto, NPC, porta ou caminho de 2 células)."""
    m = json.loads((ROOT / "data/maps" / f"{mid}.json").read_text())
    g, leg = m["ground"], m["legend"]
    taken = set(extra_taken)
    for p in m["props"]:
        for c in _PROPS.get(p["type"], {}).get("collision", []):
            taken.add((p["x"] + c[0], p["y"] + c[1]))
        taken.add((p["x"], p["y"]))
    taken |= {(n["x"], n["y"]) for n in m["npcs"]} | {(w["x"], w["y"]) for w in m["warps"]}
    best = None
    for y in range(1, len(g) - 1):
        for x in range(1, len(g[0]) - 1):
            terr = leg.get(g[y][x])
            if terr is None or _TS.get(terr, {}).get("solid", True) or (x, y) in taken:
                continue
            if x in (19, 20):  # não bloquear a estrada principal
                continue
            dd = abs(x - near[0]) + abs(y - near[1])
            if best is None or dd < best[0]:
                best = (dd, x, y)
    return best[1], best[2]


def add_npc(mid, nid, near, facing="down", **cond):
    x, y = free_cell(mid, near, [(e["x"], e["y"]) for e in MAP_NPCS.get(mid, [])] + [(e["x"], e["y"]) for e in MAP_PROPS.get(mid, [])])
    MAP_NPCS.setdefault(mid, []).append({"id": nid, "x": x, "y": y, "facing": facing} | cond)


def add_prop(mid, ptype, near, dialog, **cond):
    x, y = free_cell(mid, near, [(e["x"], e["y"]) for e in MAP_NPCS.get(mid, [])] + [(e["x"], e["y"]) for e in MAP_PROPS.get(mid, [])])
    MAP_PROPS.setdefault(mid, []).append({"type": ptype, "x": x, "y": y, "dialog": dialog} | cond)


MAP_PROPS = {}

# ------------------------------------------------------------------ crescimento do parceiro (lido pela cerimônia de aniversário)
t("GROW_PARTNER_FAROLEIRA_2", "Lia: Eu tô maior! E a lamparina virou lampião. Agora ilumina até o fim da rua!",
  "Lia: I'm bigger! And my little lamp became a lantern. Now it lights up the whole street!",
  "Lia: ¡Estoy más grande! Y el farolillo se volvió linterna. ¡Ahora alumbra toda la calle!")
t("GROW_PARTNER_FAROLEIRA_3", "Lia: Olha essa luz! Parece um farol. Acho que nunca mais vou ter medo do escuro.",
  "Lia: Look at this light... it's like a real lighthouse. I don't think I'll ever be afraid of the dark again.",
  "Lia: Mira esta luz... parece un faro de verdad. Creo que nunca más tendré miedo a la oscuridad.")
t("GROW_PARTNER_GRUMETE_2", "Taro: Maior. Mais forte. ...Meu pai ia gostar de ver isso.", "Taro: Bigger. Stronger. ...My dad would've liked to see this.",
  "Taro: Más grande. Más fuerte. ...A mi papá le habría gustado ver esto.")
t("GROW_PARTNER_GRUMETE_3", "Taro: Remo duplo. Agora eu remo pelos dois: por mim e por quem ficou pra trás.",
  "Taro: Double oar. Now I row for two: for me and for those left behind.", "Taro: Remo doble. Ahora remo por los dos: por mí y por los que se quedaron atrás.")

# ------------------------------------------------------------------ viajantes das rotas (lore do continente antes da coroa)
for mid, nid, sprite, spk, lines in [
    ("rota_2", "romeiro_cinza", "seixo", ("Romeiro da Cinza", "Ash Pilgrim", "Peregrino de la Ceniza"),
     [("Antes da coroa, as minas davam cristal pra todo o reino. A rainha usou um deles na lente do farol.",
       "Before the crown, the mines gave crystal to the whole kingdom. The queen used one for the lighthouse lens.",
       "Antes de la corona, las minas daban cristal a todo el reino. La reina usó uno para la lente del faro."),
      ("Por isso a luz do farol é meio azulada. Pedra de mina tem lembrança.", "That's why the lighthouse light is a bit bluish. Mine stone has memories.",
       "Por eso la luz del faro es algo azulada. La piedra de mina tiene recuerdos.")]),
    ("rota_3", "barqueira_lua", "traira", ("Barqueira Lua", "Boatwoman Moon", "Barquera Luna"),
     [("No tempo do reino, as palafitas eram casas de verão da corte. A princesa vinha pescar sapo.",
       "Back in the kingdom days, the stilt houses were the court's summer homes. The princess came to catch frogs.",
       "En tiempos del reino, los palafitos eran casas de verano de la corte. La princesa venía a pescar ranas."),
      ("Nunca pescou nenhum. Soltava todos. Dizia que sapo também tem família.", "She never kept a single one. Let them all go. Said frogs have families too.",
       "Nunca se quedó con ninguno. Los soltaba todos. Decía que las ranas también tienen familia.")]),
    ("rota_4", "historiadora_pena", "rosa", ("Historiadora Tinta", "Historian Ink", "Historiadora Tinta"),
     [("Esta estrada foi feita pro casamento do rei com a rainha do deserto. Mil bandeiras, uma pra cada convidado.",
       "This road was built for the king's wedding to the desert queen. A thousand banners, one for each guest.",
       "Este camino se hizo para la boda del rey con la reina del desierto. Mil banderas, una por invitado."),
      ("Hoje sobraram poucas. Mas os esqueletos ainda marcham por ela como quem vai pra festa.",
       "Only a few are left today. But the skeletons still march down it like they're heading to a party.",
       "Hoy quedan pocas. Pero los esqueletos aún marchan por él como quien va a una fiesta.")]),
    ("rota_5", "pastora_neve", "camelia", ("Pastora Neve", "Shepherdess Snow", "Pastora Nieve"),
     [("Lá no alto tem um mosteiro onde o sino nunca toca. Dizem que ele espera uma voz de muito longe.",
       "High up there's a monastery whose bell never rings. They say it waits for a voice from very far away.",
       "Allá arriba hay un monasterio cuya campana nunca suena. Dicen que espera una voz de muy lejos."),
      ("De quanto longe? Ninguém sabe. Talvez de mil anos.", "How far? No one knows. Maybe a thousand years.", "¿Qué tan lejos? Nadie lo sabe. Quizá mil años.")]),
    ("rota_6", "colecionador_eco", "pa", ("Colecionador de Ecos", "Echo Collector", "Coleccionista de Ecos"),
     [("Eu guardo ecos em garrafas. Este aqui é a risada de uma rainha, de mil anos atrás.",
       "I keep echoes in bottles. This one is a queen's laughter, from a thousand years ago.",
       "Guardo ecos en botellas. Este es la risa de una reina, de hace mil años."),
      ("Se a tempestade passar, eu solto. Risada presa fica triste.", "If the storm passes, I'll let it out. Trapped laughter gets sad.",
       "Si pasa la tormenta, la suelto. La risa encerrada se pone triste.")]),
]:
    pt, en, es = spk
    sk = t(f"SPK_X_{nid.upper()}", pt, en, es)
    nodes = [say(t(f"DLG_X_{nid.upper()}_{i}", *ln), sk) for i, ln in enumerate(lines)]
    R.d(nid, nodes)
    R.NPCS[nid] = human(sprite, sk, [{"dialog": ref(nid)}], role="lore")
    add_npc(mid, nid, (12, 44), "right")

# ------------------------------------------------------------------ Vila Maré e Raizal: mais 2 moradores cada
for mid, nid, sprite, spk, near, lines in [
    ("vila_mare", "salina", "moringa", ("Dona Salina", "Mrs. Saline", "Doña Salina"), (25, 22),
     [("Vendo sal desde menina. No tempo dos meus avós, esqueleto fazia aniversário com festa na praia inteira.",
       "I've sold salt since I was a girl. In my grandparents' day, skeletons had birthday parties across the whole beach.",
       "Vendo sal desde niña. En tiempos de mis abuelos, los esqueletos celebraban cumpleaños con fiesta en toda la playa."),
      ("Agora é tudo baixinho, com medo do Rei. Bolo sem vela é só pão triste.", "Now it's all hushed, out of fear of the King. Cake without candles is just sad bread.",
       "Ahora todo es en voz baja, por miedo al Rey. Pastel sin velas es solo pan triste.")]),
    ("vila_mare", "siri", "girino", ("Siri", "Crabby", "Cangrejito"), (14, 22),
     [("Eu tinha medo de esqueleto. Aí vi um soprando vela de aniversário. Não dá pra ter medo de quem sopra vela.",
       "I used to be scared of skeletons. Then I saw one blowing out birthday candles. You can't be scared of someone blowing out candles.",
       "Les tenía miedo a los esqueletos. Luego vi uno soplando velas de cumpleaños. No puedes temerle a quien sopla velas.")]),
    ("raizal", "seiva", "camelia", ("Seiva", "Sap", "Savia"), (25, 24),
     [("O Raizerno dorme no Bosque Velho desde antes da vila existir. Minha avó levava chá pra ele.",
       "Raizerno has slept in the Old Grove since before the village existed. My grandma used to bring him tea.",
       "Raizerno duerme en el Bosque Viejo desde antes de que existiera el pueblo. Mi abuela le llevaba té."),
      ("Ele nunca bebeu. Mas a árvore em volta dele cresceu cheirosa.", "He never drank it. But the tree around him grew fragrant.",
       "Nunca lo bebió. Pero el árbol a su alrededor creció perfumado.")]),
    ("raizal", "cavaco", "cobre", ("Seu Cavaco", "Old Woodchip", "Don Viruta"), (12, 24),
     [("Sou marceneiro. Fiz o berço de três gerações daqui. E agora faço berço pra esqueleto bebê.",
       "I'm a carpenter. I made cradles for three generations here. Now I make cradles for baby skeletons.",
       "Soy carpintero. Hice las cunas de tres generaciones aquí. Y ahora hago cunas para esqueletos bebé."),
      ("Eles chutam a madeira dormindo. Igual criança. Igualzinho.", "They kick the wood in their sleep. Just like kids. Exactly like kids.",
       "Patean la madera dormidos. Como los niños. Igualito.")]),
]:
    pt, en, es = spk
    sk = t(f"SPK_X_{nid.upper()}", pt, en, es)
    R.d(nid, [say(t(f"DLG_X_{nid.upper()}_{i}", *ln), sk) for i, ln in enumerate(lines)])
    R.NPCS[nid] = human(sprite, sk, [{"dialog": ref(nid)}], role="lore" if nid in ("salina", "seiva") else "humor")
    add_npc(mid, nid, near)

# ------------------------------------------------------------------ livros de lore nas cidades
for mid, near, key, title, lines in [
    ("brasal_casa_carvao", (3, 3), "SINO", ("Caderno de forja da Tia Fornalha", "Aunt Furnace's forge notebook", "Cuaderno de fragua de la Tía Fragua"),
     [("\"Sino de Brasal: bronze, cristal moído e uma risada do sobrinho. Sem a risada, o sino não afina.\"",
       "\"Bell of Embervale: bronze, ground crystal and one laugh from my nephew. Without the laugh, the bell won't tune.\"",
       "\"Campana de Brasal: bronce, cristal molido y una risa de mi sobrino. Sin la risa, la campana no afina.\"")]),
    ("brejo_casa_bagre", (3, 6), "MUSGA", ("Receitas da Musga (roubadas pelo Bagre)", "Musga's recipes (stolen by Catfish)", "Recetas de Musga (robadas por Bagre)"),
     [("\"Chá de esquecer a tristeza: hortelã, mel e uma visita. A visita é o ingrediente principal.\"",
       "\"Tea to forget sadness: mint, honey and one visit. The visit is the main ingredient.\"",
       "\"Té para olvidar la tristeza: menta, miel y una visita. La visita es el ingrediente principal.\""),
      ("Na margem, a letra do Bagre: \"Nunca consegui o terceiro ingrediente.\"", "In the margin, in Catfish's handwriting: \"I never managed the third ingredient.\"",
       "En el margen, la letra de Bagre: \"Nunca conseguí el tercer ingrediente.\"")]),
    ("geada_casa_lamina", (9, 3), "NEVE", ("Canções de inverno", "Winter songs", "Canciones de invierno"),
     [("\"Dorme, princesa, que a neve te cobre; quando acordar, o papai já sorriu.\" Uma canção de ninar da serra.",
       "\"Sleep, princess, let the snow tuck you in; when you wake, Papa will have smiled.\" A lullaby from the mountains.",
       "\"Duerme, princesa, que la nieve te arrope; cuando despiertes, papá ya habrá sonreído.\" Una canción de cuna de la sierra.")]),
    ("palmeiral_casa_rosa", (3, 3), "ESTRELAS", ("Mapa das estrelas da Rosa", "Rose's star chart", "Mapa de estrellas de Rosa"),
     [("Constelações com nomes à mão: \"o Remo\", \"a Lamparina\", \"a Coroa Rachada\".",
       "Constellations with handwritten names: \"the Oar\", \"the Lantern\", \"the Cracked Crown\".",
       "Constelaciones con nombres a mano: \"el Remo\", \"el Farolillo\", \"la Corona Agrietada\"."),
      ("Ao pé da página: \"Toda estrela é um farol de quem já se foi.\"", "At the foot of the page: \"Every star is a lighthouse for those who are gone.\"",
       "Al pie de la página: \"Cada estrella es un faro de quienes ya se fueron.\"")]),
]:
    nodes = [say(t(f"OBJ_X_BOOK_{key}_T", *title))] + [say(t(f"OBJ_X_BOOK_{key}_{i}", *ln)) for i, ln in enumerate(lines)]
    R.d(f"livro_{key.lower()}", nodes)
    add_prop(mid, "bookshelf", near, ref(f"livro_{key.lower()}"))

# ------------------------------------------------------------------ 2ª missão em Geada e em Palmeiral
# Geada: a eleição do Prefeito (boneco de neve) — o Floquinho pede votos de 3 moradores
t("DLG_X_FLOQ_ASK", "Vai ter eleição pra prefeito de neve! Pergunta pra Lareira, pro Pinhão e pro Degelo em quem eles votam?",
  "There's going to be a snow-mayor election! Ask Hearth, Pinecone and Thaw who they're voting for?",
  "¡Habrá elección de alcalde de nieve! ¿Les preguntas a Hoguera, a Piñón y a Deshielo por quién votan?")
t("DLG_X_FLOQ_WAIT", "Faltam votos! Lareira no Rancho, Pinhão e Degelo na praça.", "Still missing votes! Hearth at the Ranch, Pinecone and Thaw in the square.",
  "¡Faltan votos! Hoguera en el Rancho, Piñón y Deshielo en la plaza.")
t("DLG_X_FLOQ_WIN", "Três votos pro Prefeito! Ganhou por unanimidade. Ele não disse nada, mas tá feliz. Toma, presente do gabinete.",
  "Three votes for the Mayor! A unanimous win. He didn't say anything, but he's happy. Here, a gift from the office.",
  "¡Tres votos para el Alcalde! Ganó por unanimidad. No dijo nada, pero está feliz. Toma, regalo del despacho.")
t("DLG_X_FLOQ_DONE", "O Prefeito já assinou três decretos. Todos de neve.", "The Mayor has already signed three decrees. All made of snow.",
  "El Alcalde ya firmó tres decretos. Todos de nieve.")
t("DLG_X_VOTE_LAREIRA", "Voto no Prefeito. Pelo menos ele não reclama da sopa.", "I vote for the Mayor. At least he doesn't complain about the soup.",
  "Voto por el Alcalde. Al menos no se queja de la sopa.")
t("DLG_X_VOTE_PINHAO", "No meu tempo, prefeito tinha nariz de cenoura e honra. Esse tem os dois. Voto nele.",
  "In my day, a mayor had a carrot nose and honor. This one has both. He's got my vote.",
  "En mis tiempos, el alcalde tenía nariz de zanahoria y honor. Este tiene las dos. Voto por él.")
t("DLG_X_VOTE_DEGELO", "Votar num boneco de neve? ...Tá, ele é mais rápido que o prefeito de verdade.",
  "Vote for a snowman? ...Fine, he's quicker than the real mayor.", "¿Votar por un muñeco de nieve? ...Vale, es más rápido que el alcalde de verdad.")
R.d("floq_pede", [{"say": "DLG_PI_FLOQUINHO_AFTER", "speaker": "SPK_FLOQUINHO", "if": "alva_beaten"},
                  {"say": "DLG_PI_FLOQUINHO", "speaker": "SPK_FLOQUINHO", "if_not": "alva_beaten"},
                  say("DLG_X_FLOQ_ASK", "SPK_FLOQUINHO"), flag("eleicao_quest")])
R.d("floq_espera", [say("DLG_X_FLOQ_WAIT", "SPK_FLOQUINHO")])
R.d("floq_ganhou", [say("DLG_X_FLOQ_WIN", "SPK_FLOQUINHO"), act("give_item", item="reviver", n=1), act("give_item", item="pocao_g", n=1), flag("eleicao_done")])
R.d("floq_depois", [say("DLG_X_FLOQ_DONE", "SPK_FLOQUINHO")])
VOTE = {"lareira": "SPK_LAREIRA", "pinhao": "SPK_PINHAO", "degelo": "SPK_DEGELO"}
for npc, spk in VOTE.items():
    npc_data = json.loads((ROOT / "data/npcs.json").read_text())["npcs"][npc]
    original = [x for x in npc_data["dialog"] if not str(x.get("dialog", "")).startswith("extras/")][-1]["dialog"]
    R.d(f"voto_{npc}", [say(f"DLG_X_VOTE_{npc.upper()}", spk), flag(f"voto_{npc}"), goto(original)])
    NPC_PRE.setdefault(npc, []).append({"if": "eleicao_quest", "if_not": f"voto_{npc}", "dialog": ref(f"voto_{npc}")})
NPC_PRE.setdefault("floquinho", []).extend([
    {"if": "eleicao_done", "dialog": ref("floq_depois")},
    {"if_all": ["voto_lareira", "voto_pinhao", "voto_degelo"], "dialog": ref("floq_ganhou")},
    {"if": "eleicao_quest", "dialog": ref("floq_espera")},
    {"if_not": "game_cleared", "dialog": ref("floq_pede")}])

# Palmeiral: os tambores de volta — o Grão conta os tambores da cidade depois da Duna
t("DLG_X_GRAO_ASK", "A rainha liberou os tambores! Mas ninguém lembra o ritmo de guiar caravana. Os Batuque sabem. Pergunta pra eles?",
  "The queen allowed the drums again! But nobody remembers the caravan-guiding rhythm. The Drumbeats know it. Will you ask them?",
  "¡La reina liberó los tambores! Pero nadie recuerda el ritmo para guiar caravanas. Los Tamborrada lo saben. ¿Les preguntas?")
t("DLG_X_BATUQUE_RHYTHM", "O ritmo da caravana? Tum, tum-tum, PÁ. Três batidas e uma de esperança. Leva pro Grão.",
  "The caravan rhythm? Boom, boom-boom, BAP. Three beats and one for hope. Take it to Grain.",
  "¿El ritmo de la caravana? Pum, pum-pum, PAM. Tres golpes y uno de esperanza. Llévaselo a Grano.")
t("DLG_X_GRAO_DONE", "Tum, tum-tum, PÁ! Ouviu? Lá longe, uma caravana respondeu! Toma, a cidade agradece.",
  "Boom, boom-boom, BAP! Hear that? Far away, a caravan answered! Here, the town thanks you.",
  "¡Pum, pum-pum, PAM! ¿Oíste? ¡A lo lejos, una caravana respondió! Toma, el pueblo te lo agradece.")
t("DLG_X_GRAO_AFTER", "Já contei: hoje chegaram onze caravanas. Bem mais fácil que contar areia.", "I counted: eleven caravans arrived today. Much easier than counting sand.",
  "Ya conté: hoy llegaron once caravanas. Mucho más fácil que contar arena.")
R.d("grao_pede", [say("DLG_X_GRAO_ASK", "SPK_GRAO"), flag("ritmo_quest")])
R.d("grao_feito", [say("DLG_X_GRAO_DONE", "SPK_GRAO"), {"action": "sfx", "name": "birthday"}, act("give_item", item="pocao_g", n=2), flag("ritmo_done")])
R.d("grao_depois", [say("DLG_X_GRAO_AFTER", "SPK_GRAO")])
npc_data = json.loads((ROOT / "data/npcs.json").read_text())["npcs"]["batuque"]
orig_b = [x for x in npc_data["dialog"] if not str(x.get("dialog", "")).startswith("extras/")]
R.d("batuque_ritmo", [say("DLG_X_BATUQUE_RHYTHM", "SPK_BATUQUE"), flag("ritmo_aprendido")])
NPC_PRE.setdefault("batuque", []).append({"if": "ritmo_quest", "if_not": "ritmo_aprendido", "dialog": ref("batuque_ritmo")})
NPC_PRE.setdefault("grao", []).extend([
    {"if": "ritmo_done", "dialog": ref("grao_depois")},
    {"if": "ritmo_aprendido", "dialog": ref("grao_feito")},
    {"if": "duna_beaten", "if_not": "ritmo_quest", "dialog": ref("grao_pede")}])

# ------------------------------------------------------------------ conversa no Rancho (cama): o parceiro reflete, uma por cidade
PROP_DIALOG = {}   # mapa -> [(tipo, x, y, diálogo)]
for mid, key, lia_line, taro_line in [
    ("vila_rancho", "VILA", ("Cama de verdade! Eu acordei numa caverna fria, sabia? Aqui é bem melhor.", "A real bed! I woke up in a cold cave, did you know? This is way better.",
                             "¡Una cama de verdad! Yo desperté en una cueva fría, ¿sabías? Aquí es mucho mejor."),
     ("Eu durmo de botas. Vai que alguém precisa de ajuda no meio da noite.", "I sleep with my boots on. In case someone needs help in the middle of the night.",
      "Duermo con las botas puestas. Por si alguien necesita ayuda a medianoche.")),
    ("raizal_rancho", "RAIZAL", ("No túnel eu tremi. Mas fui. Tremer e ir ao mesmo tempo conta como coragem?",
                                 "In the tunnel I shook. But I went. Does shaking and going at the same time count as courage?",
                                 "En el túnel temblé. Pero fui. ¿Temblar e ir a la vez cuenta como valentía?"),
     ("O Ramalho riu o tempo todo. Meu pai também ria assim. Alto demais.", "Ramalho laughed the whole time. My dad laughed like that too. Way too loud.",
      "Ramalho se rió todo el tiempo. Mi papá también se reía así. Demasiado fuerte.")),
    ("brasal_rancho", "BRASAL", ("A Tia Fornalha cuida demais. Será que eu cuido demais da minha lamparina?",
                                 "Aunt Furnace cares too much. Do you think I care too much about my lamp?",
                                 "La Tía Fragua cuida demasiado. ¿Crees que yo cuido demasiado mi farolillo?"),
     ("Guardei o lenço da minha mãe na mochila. Não conta pra ninguém. Ele cheira a casa.",
      "I kept my mom's scarf in my bag. Don't tell anyone. It smells like home.", "Guardé el pañuelo de mi mamá en la mochila. No se lo digas a nadie. Huele a casa.")),
    ("brejo_rancho", "BREJO", ("A Musga só queria visita. Se eu morasse numa torre, eu ia querer também.", "Musga just wanted visitors. If I lived in a tower, I'd want them too.",
                               "Musga solo quería visitas. Si yo viviera en una torre, también querría."),
     ("Castelo. Eles tão no castelo. Agora eu sei pra onde correr. Isso já ajuda.", "The castle. They're at the castle. Now I know where to run. That helps already.",
      "El castillo. Están en el castillo. Ahora sé hacia dónde correr. Eso ya ayuda.")),
    ("ossorio_rancho", "OSSORIO", ("Você é da família do Rei... Mas pra mim você continua sendo você. Tá?",
                                   "You're the King's family... But to me you're still just you. Okay?",
                                   "Eres de la familia del Rey... Pero para mí sigues siendo tú. ¿Vale?"),
     ("Neto de rei. Tá. Continua chato igual.", "A king's grandkid. Okay. Still just as annoying.", "Nieto de rey. Vale. Sigues igual de pesado.")),
    ("geada_rancho", "GEADA", ("A Alva congelou tudo pra esperar o pai. Eu também esperei, no escuro. Esperar sozinho é o pior.",
                               "Alva froze everything to wait for her father. I waited too, in the dark. Waiting alone is the worst.",
                               "Alva congeló todo para esperar a su padre. Yo también esperé, a oscuras. Esperar sola es lo peor."),
     ("Eu disse que tinha medo. Em voz alta. Não foi tão ruim quanto eu achava.", "I said I was scared. Out loud. It wasn't as bad as I thought.",
      "Dije que tenía miedo. En voz alta. No fue tan malo como pensaba.")),
    ("palmeiral_rancho", "PALMEIRAL", ("Amanhã é o castelo. Promete uma coisa? Não coloca aquela coroa.", "Tomorrow is the castle. Promise me something? Don't put on that crown.",
                                       "Mañana es el castillo. ¿Me prometes algo? No te pongas esa corona."),
     ("Amanhã eu vejo meus pais. Ou não. ...Dorme logo, que eu não consigo.", "Tomorrow I see my parents. Or not. ...Go to sleep already, because I can't.",
      "Mañana veo a mis padres. O no. ...Duérmete ya, que yo no puedo.")),
]:
    kl = t(f"DLG_X_BED_{key}_L", *lia_line)
    kt = t(f"DLG_X_BED_{key}_T", *taro_line)
    R.d(f"cama_{key.lower()}", [say(kl, "SPK_LIA") | {"if": "partner_lia"}, say(kt, "SPK_TARO") | {"if": "partner_taro"}])
    PROP_DIALOG.setdefault(mid, []).append(("bed", 2, 3, ref(f"cama_{key.lower()}")))

# ------------------------------------------------------------------ pós-jogo: Ranchos, lojas e capangas
for npc, spk, pt, en, es in [
    ("marola", "SPK_MAROLA", "O Rei Esqueleto no meu Rancho! Deita aí, Majestade. Aqui todo mundo é igual na hora da sopa.",
     "The Skeleton King in my Ranch! Lie down, Your Majesty. Here everyone's equal at soup time.", "¡El Rey Esqueleto en mi Rancho! Acuéstese, Majestad. Aquí todos somos iguales a la hora de la sopa."),
    ("tilia", "SPK_TILIA", "Os esqueletos não obedecem mais ninguém, e mesmo assim vêm deitar aqui. Isso é confiança.",
     "The skeletons obey no one now, and still they come to lie down here. That's trust.", "Los esqueletos ya no obedecen a nadie y aun así vienen a acostarse aquí. Eso es confianza."),
    ("rubi", "SPK_RUBI", "O Rancho encheu de novo! Mineiro com esqueleto no colo, igual antigamente.", "The Ranch is full again! Miners with skeletons on their laps, just like old times.",
     "¡El Rancho se llenó otra vez! Mineros con esqueletos en el regazo, como antes."),
    ("garca", "SPK_GARCA", "Ninguém tosse mais. Agora o barulho do Rancho é ronco. Prefiro mil vezes.", "Nobody coughs anymore. Now the Ranch noise is snoring. I much prefer it.",
     "Ya nadie tose. Ahora el ruido del Rancho son ronquidos. Lo prefiero mil veces."),
    ("ameia", "SPK_AMEIA", "Acabou o toque de recolher, acabou o dormir em formação. Agora cada um dorme torto, do jeito que gosta.",
     "No more curfew, no more sleeping in formation. Now everyone sleeps crooked, however they like.", "Se acabó el toque de queda y dormir en formación. Ahora cada uno duerme torcido, como le gusta."),
    ("lareira", "SPK_LAREIRA", "Primavera! Apaguei a lareira pela primeira vez em um ano. Até estranhei.", "Spring! I put out the fire for the first time in a year. Felt strange.",
     "¡Primavera! Apagué la chimenea por primera vez en un año. Hasta me resultó raro."),
    ("moringa", "SPK_MORINGA", "Com as caravanas de volta, tem água, tem tâmara e tem fofoca. Rancho cheio é Rancho feliz.",
     "With the caravans back, there's water, dates and gossip. A full Ranch is a happy Ranch.", "Con las caravanas de vuelta hay agua, dátiles y chismes. Rancho lleno, Rancho feliz."),
    ("anzol", "SPK_ANZOL", "Vendo até pro Rei agora. Ele pediu desconto. Rei pedindo desconto, veja só.", "I even sell to the King now. He asked for a discount. A king asking for a discount, imagine.",
     "Ahora hasta le vendo al Rey. Me pidió descuento. Un rey pidiendo descuento, fíjate."),
    ("toco", "SPK_TOCO", "Estrada cheia, preço justo. Quase justo. Justo pra mim.", "Busy road, fair prices. Almost fair. Fair to me.", "Camino lleno, precio justo. Casi justo. Justo para mí."),
    ("cobre", "SPK_COBRE", "Minério voltou, freguês voltou, até o sino voltou a tocar. Só o meu bigode não voltou ao normal.",
     "The ore's back, the customers are back, even the bell rings again. Only my mustache hasn't recovered.", "Volvió el mineral, volvió la clientela, hasta la campana volvió a sonar. Solo mi bigote no se recuperó."),
    ("junco", "SPK_JUNCO", "Antídoto de volta na prateleira! Ninguém compra. Ninguém precisa. Melhor problema do mundo.",
     "Antidotes back on the shelf! Nobody buys them. Nobody needs them. Best problem in the world.", "¡Antídotos de vuelta en el estante! Nadie los compra. Nadie los necesita. El mejor problema del mundo."),
    ("dobrao", "SPK_DOBRAO", "Sem autorização do quartel! Rasguei a minha. Emoldurei os pedaços.", "No barracks permit needed! I tore mine up. Framed the pieces.",
     "¡Sin permiso del cuartel! Rompí el mío. Enmarqué los pedazos."),
    ("cachecol", "SPK_CACHECOL", "Primavera é péssimo pra quem vende cachecol. Vou vender chapéu de sol.", "Spring is terrible for scarf sellers. I'll sell sun hats.",
     "La primavera es pésima para quien vende bufandas. Venderé sombreros de sol."),
    ("canela", "SPK_CANELA", "Caravana nova todo dia. O preço agora é o da alegria: um pouco mais baixo.", "A new caravan every day. Prices are set by joy now: a little lower.",
     "Una caravana nueva cada día. El precio ahora es el de la alegría: un poco más bajo."),
    ("jurema", "SPK_JUREMA", "Prometi o primeiro peixe pra você. Guardei o maior. Tá salgado há uma semana, mas é seu.",
     "I promised you the first fish. I saved the biggest one. It's been salted for a week, but it's yours.",
     "Te prometí el primer pescado. Guardé el más grande. Lleva una semana en sal, pero es tuyo."),
    ("seu_remo", "SPK_REMO", "Os meninos cresceram tanto que agora a sopa esfria esperando eles. Volta pra uma revanche quando quiser.",
     "The kids have grown so much that now the soup goes cold waiting for them. Come back for a rematch anytime.",
     "Los chicos crecieron tanto que ahora la sopa se enfría esperándolos. Vuelve a por la revancha cuando quieras."),
    ("vo_concha", "SPK_CONCHA", "Fiz um bolo com cem velas pro Rei. Ele demorou meia hora pra soprar. Família é isso.",
     "I baked a cake with a hundred candles for the King. It took him half an hour to blow them out. That's family.",
     "Hice un pastel con cien velas para el Rey. Tardó media hora en soplarlas. Eso es familia."),
    ("irmao_galho", "SPK_GALHO", "A gente aprendeu a não empurrar o turno de ninguém. Agora a gente só empurra balanço.",
     "We learned not to push anyone's turn around. Now we only push swings.", "Aprendimos a no empujar el turno de nadie. Ahora solo empujamos columpios."),
    ("pai_musgo", "SPK_MUSGO", "Esporo continua sendo tempero. Mas agora é por gosto, não por veneno.", "Spores are still seasoning. But now it's for flavor, not poison.",
     "Las esporas siguen siendo condimento. Pero ahora por sabor, no por veneno."),
    ("bigorna", "SPK_BIGORNA", "Forjei um sino novo pra cidade. Pus uma risada dentro, igual à receita da Tia.",
     "I forged a new bell for the town. Put a laugh inside, just like Auntie's recipe.", "Forjé una campana nueva para el pueblo. Le puse una risa dentro, como en la receta de la Tía."),
    ("viseira", "SPK_VISEIRA", "Dispensei a tropa. Agora a gente treina Sintonia dançando. Funciona melhor, vai entender.",
     "I dismissed the troops. Now we train Sync by dancing. Works better, go figure.", "Licencié a la tropa. Ahora entrenamos Sintonía bailando. Funciona mejor, quién lo diría."),
    ("tamara", "SPK_TAMARA", "Meu camelo voltou! Trouxe três amigos. Agora quem precisa trocar de montaria sou eu.",
     "My camel came back! Brought three friends. Now I'm the one who has to switch mounts.", "¡Mi camello volvió! Trajo tres amigos. Ahora la que tiene que cambiar de montura soy yo."),
    ("agata", "SPK_AGATA", "Sem gás na mina, meu perfume acabou. Agora uso lavanda. Os esqueletos estranharam.",
     "No more gas in the mine, so my perfume is gone. I wear lavender now. The skeletons find it odd.",
     "Sin gas en la mina se acabó mi perfume. Ahora uso lavanda. A los esqueletos les parece raro."),
    ("bagre", "SPK_BAGRE", "Pesquei um peixe tão grande que ele me pescou de volta. Brincadeira. Mais ou menos.",
     "I caught a fish so big it caught me back. Just kidding. Sort of.", "Pesqué un pez tan grande que me pescó de vuelta. Es broma. Más o menos."),
    ("lamina", "SPK_LAMINA", "Sem gelo, eu patino na lama. É mais lento, mas muito mais engraçado.", "No ice, so I skate on mud. It's slower, but way funnier.",
     "Sin hielo, patino en el barro. Es más lento, pero mucho más divertido."),
    ("batuque", "SPK_BATUQUE", "Tum, tum-tum, PÁ! A gente toca toda noite. Os vizinhos reclamam com ritmo.", "Boom, boom-boom, BAP! We play every night. The neighbors complain in rhythm.",
     "¡Pum, pum-pum, PAM! Tocamos todas las noches. Los vecinos se quejan con ritmo."),
    ("bras_depois", "SPK_BRAS", "Agora eu fiscalizo peixe fresco. Peixe não reclama. Quase sempre.", "Now I inspect fresh fish. Fish don't complain. Almost never.",
     "Ahora fiscalizo pescado fresco. El pescado no se queja. Casi nunca."),
    ("bloqueio", "SPK_BLOQUEIO", "Saí da cidade pela primeira vez em um ano. Voltei no mesmo dia. Saudade da cinza.", "I left town for the first time in a year. Came back the same day. Missed the ash.",
     "Salí del pueblo por primera vez en un año. Volví el mismo día. Extrañaba la ceniza."),
    ("fel", "SPK_FEL", "Agora faço xarope de mel. A receita da Musga era: um pouco de tudo e muita saudade.",
     "Now I make honey syrup. Musga's recipe was: a little of everything and a lot of longing.", "Ahora hago jarabe de miel. La receta de Musga era: un poco de todo y mucha nostalgia."),
    ("grade", "SPK_GRADE", "A senha agora é \"bom dia\". Todo mundo acerta. Que tédio maravilhoso.", "The password is now \"good morning\". Everyone gets it right. What wonderful boredom.",
     "La contraseña ahora es \"buenos días\". Todos aciertan. Qué aburrimiento maravilloso."),
    ("pingente", "SPK_PINGENTE", "Derreti um pouco também. Não o corpo, o coração. Não conta pro sargento.", "I melted a little too. Not my body, my heart. Don't tell the sergeant.",
     "Yo también me derretí un poco. No el cuerpo, el corazón. No se lo digas al sargento."),
    ("sandalo", "SPK_SANDALO", "Pode entrar de sandália. Pode até dançar. A rainha deixou um bilhete dizendo isso.",
     "You may come in wearing sandals. You may even dance. The queen left a note saying so.", "Puede entrar con sandalias. Hasta puede bailar. La reina dejó una nota diciéndolo."),
]:
    k = t(f"DLG_X_POST_{npc.upper()}", pt, en, es)
    npc_data = json.loads((ROOT / "data/npcs.json").read_text())["npcs"][npc]
    original = [x for x in npc_data["dialog"] if not str(x.get("dialog", "")).startswith("extras/")][-1]["dialog"]
    nodes = [say(k, spk)]
    if npc in ("marola", "tilia", "rubi", "garca", "ameia", "lareira", "moringa", "anzol", "toco", "cobre", "junco", "dobrao", "cachecol", "canela"):
        nodes.append(goto(original))   # Rancho e loja continuam funcionando
    R.d(f"pos_{npc}", nodes)
    NPC_PRE.setdefault(npc, []).insert(0, {"if": "game_cleared", "dialog": ref(f"pos_{npc}")})

# ------------------------------------------------------------------ objetos de lore: sala do trono e museu de 2040
for mid, ptype, x, y, key, cond, lines in [
    ("sala_trono", "portrait", 6, 1, "TR_PORTRAIT1", None, [("Retrato da família: sete pessoas sorrindo na praia, diante de um farol novinho.",
                                                             "A family portrait: seven people smiling on the beach, in front of a brand-new lighthouse.",
                                                             "Retrato familiar: siete personas sonriendo en la playa, frente a un faro nuevecito.")]),
    ("sala_trono", "portrait", 13, 1, "TR_PORTRAIT2", None, [("Um desenho de giz: a família inteira, feita por uma criança. O menino se desenhou maior que todos.",
                                                              "A chalk drawing: the whole family, made by a child. The boy drew himself bigger than everyone.",
                                                              "Un dibujo de tiza: toda la familia, hecho por un niño. El niño se dibujó más grande que todos.")]),
    ("sala_trono", "throne", 10, 3, "TR_THRONE", None, [("O trono está vazio. Pela primeira vez em mil anos, ninguém precisa sentar nele.",
                                                         "The throne is empty. For the first time in a thousand years, no one has to sit on it.",
                                                         "El trono está vacío. Por primera vez en mil años, nadie tiene que sentarse en él.")]),
    ("museu_2040", "portrait", 3, 1, "MU_DUNA", None, [("\"Rainha Duna, construtora do Farol do Litoral (restaurado em 2031).\"",
                                                        "\"Queen Duna, builder of the Coastal Lighthouse (restored in 2031).\"",
                                                        "\"Reina Duna, constructora del Faro del Litoral (restaurado en 2031).\"")]),
    ("museu_2040", "portrait", 11, 1, "MU_KING", None, [("\"Ossárion, último rei de Ossório. Morreu sem herdeiros, dizem os livros.\"",
                                                         "\"Ossárion, last king of Ossório. Died without heirs, or so the books say.\"",
                                                         "\"Ossárion, último rey de Ossório. Murió sin herederos, dicen los libros.\"")]),
    ("museu_2040", "map_board", 4, 4, "MU_MAP", None, [("Mapa do litoral em 2040: as mesmas três baías. A do meio se chama Baía do Farol.",
                                                        "A map of the coast in 2040: the same three bays. The middle one is called Lighthouse Bay.",
                                                        "Mapa del litoral en 2040: las mismas tres bahías. La del medio se llama Bahía del Faro.")]),
]:
    R.d(f"obj_{key.lower()}", [say(t(f"OBJ_X_{key}_{i}", *ln)) for i, ln in enumerate(lines)])
    PROP_DIALOG.setdefault(mid, []).append((ptype, x, y, ref(f"obj_{key.lower()}")))


# ------------------------------------------------------------------ documento simples (sem Guardião)
def write_doc():
    L = ["# Roteiro — Falas transversais (o mundo reage)", "",
         "Fase 4h. **Gerado por `tools/maps/extras.py`**, que roda depois de todas as regiões (`tools/maps/build_all.py`). "
         "Reúne falas que atravessam o jogo inteiro: o parceiro comentando o Prólogo e o Bosque, NPCs que mudam depois do Brás e do Ramalho, "
         "as **cartas do Bento** que chegam ao Rancho de cada cidade depois do Guardião, e o **pós-jogo** (lore nova em todas as cidades, "
         "Lia no farol e a família do Taro na Vila Maré).", "",
         "## Falas (PT-BR)", ""]
    for r in R.order:
        L.append(f"### `extras/{r}`")
        for n in R.D[r]:
            L.append(R._node_line(n))
        L.append("")
    L += ["## Contagem", f"Cerca de **{R.words()} palavras** de texto de jogo em PT-BR."]
    (ROOT / "docs/roteiro/09_extras.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def patch():
    p = ROOT / "data/npcs.json"
    d = json.loads(p.read_text())
    for npc, pre in NPC_PRE.items():
        n = d["npcs"][npc]
        n["dialog"] = list(pre) + [x for x in n["dialog"] if not str(x.get("dialog", "")).startswith("extras/")]
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    p = ROOT / "data/cities.json"
    c = json.loads(p.read_text())
    for city in c["cities"]:
        extra = {"geada": "floquinho", "palmeiral": "grao"}.get(city["id"])
        if extra and extra not in city["quests"]:
            city["quests"].append(extra)
    p.write_text(json.dumps(c, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for mid in set(MAP_ENTER) | set(MAP_NPCS) | set(MAP_PROPS) | set(PROP_DIALOG):
        p = ROOT / "data/maps" / f"{mid}.json"
        m = json.loads(p.read_text())
        if mid in MAP_ENTER:
            oe = [x for x in m.get("on_enter", []) if not str(x.get("dialog", "")).startswith("extras/")]
            m["on_enter"] = oe + [MAP_ENTER[mid]]
        if mid in MAP_NPCS:
            ids = {x["id"] for x in MAP_NPCS[mid]}
            m["npcs"] = [x for x in m["npcs"] if x["id"] not in ids] + MAP_NPCS[mid]
        for (ptype, x, y, dlg) in PROP_DIALOG.get(mid, []):
            for pr in m["props"]:
                if pr["type"] == ptype and pr["x"] == x and pr["y"] == y:
                    pr["dialog"] = dlg
        if mid in MAP_PROPS:
            m["props"] = [x for x in m["props"] if not str(x.get("dialog", "")).startswith("extras/livro_")] + MAP_PROPS[mid]
        p.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    R._write_doc = write_doc
    R.write()
    patch()
