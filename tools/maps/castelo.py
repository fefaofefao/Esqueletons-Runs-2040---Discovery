#!/usr/bin/env python3
"""Final — Castelo do Rei Esqueleto, os 2 finais, créditos e pós-jogo (fase 4h).
Fonte única: gera docs/roteiro/08_castelo.md, falas (PT/EN/ES), NPCs,
encontros e mapas (Portão, Salão, Sala do Trono, Museu de 2040). Também liga o
pós-jogo às regiões anteriores (farol aceso na Praia e os "ecos" dos
Guardiões para revanche); por isso roda por último (tools/maps/build_all.py)."""
import json

from regionkit import ROOT, Grid, Region, team, say, ask, battle, act, flag, goto, human, skel

R = Region("castelo", 8, "castelo", ["castelo"])
t = R.t
ref = R.ref


def lia(k):
    return say(k, "SPK_LIA") | {"if": "partner_lia"}


def taro(k):
    return say(k, "SPK_TARO") | {"if": "partner_taro"}


def nar(k, **cond):
    return say(k) | cond


# ------------------------------------------------------------------ nomes
for k, pt, en, es in [
        ("REI", "Rei Ossárion", "King Ossárion", "Rey Ossárion"), ("DEGUSTOR", "Provador Real Degustor", "Royal Taster Degustor", "Catador Real Degustor"),
        ("EBANO", "Guarda Real Ébano", "Royal Guard Ebony", "Guardia Real Ébano"), ("ARAUTO", "Arauto Real", "Royal Herald", "Heraldo Real"),
        ("TEMPERO", "Cozinheiro Tempero", "Cook Seasoning", "Cocinero Aderezo"), ("PAI_TARO", "Pai do Taro", "Taro's Dad", "Papá de Taro"),
        ("MAE_TARO", "Mãe do Taro", "Taro's Mom", "Mamá de Taro"), ("GUARDAS", "Guardas do Portão", "Gate Guards", "Guardias de la Puerta")]:
    t(f"SPK_{k}", pt, en, es)
for k in ("DEGUSTOR", "EBANO", "ARAUTO", "TEMPERO", "GUARDAS"):
    pt, en, es = R.T[f"SPK_{k}"]
    t(f"BTL_TAMER_{k}", pt, en, es)
t("BTL_TAMER_REI", "Rei Esqueleto Ossárion", "Skeleton King Ossárion", "Rey Esqueleto Ossárion")
t("MAP_CASTELO_PORTAO", "Castelo do Rei — Portão", "King's Castle — Gate", "Castillo del Rey — Puerta")
t("MAP_CASTELO_SALAO", "Castelo do Rei — Grande Salão", "King's Castle — Great Hall", "Castillo del Rey — Gran Salón")
t("MAP_SALA_TRONO", "Sala do Trono", "Throne Room", "Sala del Trono")
t("MAP_MUSEU", "Museu do Litoral — 2040", "Coastal Museum — 2040", "Museo del Litoral — 2040")
t("OPT_C_CROWN", "Colocar a coroa", "Put on the crown", "Ponerse la corona")
t("OPT_C_REFUSE", "Recusar", "Refuse", "Negarse")
t("OPT_C_TASTE", "Provar", "Taste it", "Probarlo")

# ------------------------------------------------------------------ Portão: os pais do Taro (e Caliço, se Ossório soube)
t("DLG_C_ARR_P_T1", "São eles. Meu pai. Minha mãe.", "It's them. My dad. My mom.", "Son ellos. Mi papá. Mi mamá.")
t("DLG_C_ARR_P_T2", "Pai! Mãe! Sou eu, o Taro!", "Dad! Mom! It's me, Taro!", "¡Papá! ¡Mamá! ¡Soy yo, Taro!")
t("DLG_C_ARR_P_N", "Os dois guardas olham através dele, como se ele fosse vento.", "The two guards look right through him, as if he were wind.",
  "Los dos guardias miran a través de él, como si fuera viento.")
t("DLG_C_ARR_P_T3", "...Eles não lembram. A coroa apagou eles.", "...They don't remember. The crown erased them.", "...No me recuerdan. La corona los borró.")
t("DLG_C_ARR_P_T4", "Então eu vou quebrar essa coroa.", "Then I'm going to break that crown.", "Entonces voy a romper esa corona.")
t("DLG_C_ARR_P_R1", "Cheguei primeiro. Como eu disse.", "I got here first. Like I said.", "Llegué primero. Como dije.")
t("DLG_C_ARR_P_R2", "Aqueles dois no portão... são meus pais. Eles não me reconhecem.", "Those two at the gate... they're my parents. They don't recognize me.",
  "Esos dos de la puerta... son mis padres. No me reconocen.")
t("DLG_C_ARR_P_L", "Taro... a gente vai consertar isso. Juntos.", "Taro... we're going to fix this. Together.", "Taro... vamos a arreglarlo. Juntos.")
t("DLG_C_ARR_P_R3", "...Juntos. Tá.", "...Together. Okay.", "...Juntos. Vale.")
t("DLG_C_TARO_WAIT", "Vai. Eu fico aqui com eles. Se a coroa quebrar, quero ser a primeira cara que eles veem.",
  "Go. I'll stay here with them. If the crown breaks, I want to be the first face they see.",
  "Ve. Yo me quedo aquí con ellos. Si la corona se rompe, quiero ser la primera cara que vean.")
t("DLG_C_GUARDS_1", "Dois esqueletos enormes de remo cruzam os remos diante da porta.", "Two huge oar-wielding skeletons cross their oars in front of the door.",
  "Dos enormes esqueletos con remos cruzan los remos frente a la puerta.")
t("DLG_C_GUARDS_2", "Ninguém entra. Ninguém sai. Ninguém se perde.", "No one enters. No one leaves. No one gets lost.", "Nadie entra. Nadie sale. Nadie se pierde.")
t("DLG_C_GUARDS_3", "Os guardas abaixam os remos e se afastam, sem uma palavra.", "The guards lower their oars and step aside without a word.",
  "Los guardias bajan los remos y se apartan, sin decir palabra.")
t("DLG_C_GUARDS_T", "Desculpa, pai. Desculpa, mãe. Já, já eu volto.", "Sorry, Dad. Sorry, Mom. I'll be right back.", "Perdón, papá. Perdón, mamá. Ya vuelvo.")
t("DLG_C_CAL_1", "Prometi e cumpro. Estou aqui.", "I promised, and I keep my word. I'm here.", "Lo prometí y lo cumplo. Aquí estoy.")
t("DLG_C_CAL_2", "Deixe-me cuidar dos seus. Um soldado também sabe tratar feridas.", "Let me tend to your team. A soldier knows how to treat wounds too.",
  "Déjame atender a los tuyos. Un soldado también sabe curar heridas.")
R.d("chegada_portao", [taro("DLG_C_ARR_P_T1"), taro("DLG_C_ARR_P_T2"), nar("DLG_C_ARR_P_N", **{"if": "partner_taro"}), taro("DLG_C_ARR_P_T3"),
                       taro("DLG_C_ARR_P_T4"), say("DLG_C_ARR_P_R1", "SPK_TARO") | {"if": "partner_lia"},
                       say("DLG_C_ARR_P_R2", "SPK_TARO") | {"if": "partner_lia"}, lia("DLG_C_ARR_P_L"),
                       say("DLG_C_ARR_P_R3", "SPK_TARO") | {"if": "partner_lia"}, flag("portao_visto")])
R.d("taro_portao", [say("DLG_C_TARO_WAIT", "SPK_TARO")])
R.d("guardas", [say("DLG_C_GUARDS_1"), say("DLG_C_GUARDS_2", "SPK_GUARDAS"),
                battle("BTL_TAMER_GUARDAS", team([("grumete", 88), ("grumete", 87)]), 1200, "pais_beaten"),
                say("DLG_C_GUARDS_3"), taro("DLG_C_GUARDS_T"), act("hide_npc", id="pai_taro"), act("hide_npc", id="mae_taro")])
R.d("calico_aliado", [say("DLG_C_CAL_1", "SPK_CALICO"), say("DLG_C_CAL_2", "SPK_CALICO"), act("heal")])
R.NPCS["pai_taro"] = skel("skel_grumete_3", "SPK_PAI_TARO", [{"dialog": ref("guardas")}], {"vision": 2, "flag": "pais_beaten"})
R.NPCS["mae_taro"] = skel("skel_grumete_3", "SPK_MAE_TARO", [{"dialog": ref("guardas")}], {"vision": 2, "flag": "pais_beaten"})
R.NPCS["taro_portao"] = skel("skel_grumete_3", "SPK_TARO", [{"dialog": ref("taro_portao")}])
R.NPCS["calico_aliado"] = skel("skel_calico", "SPK_CALICO", [{"dialog": ref("calico_aliado")}])

# ------------------------------------------------------------------ Grande Salão: guardas, fonte e o Provador Real
t("DLG_C_EBANO_1", "Guarda Real Ébano. Ninguém chega ao trono. Ninguém sai, ninguém se perde.", "Royal Guard Ebony. No one reaches the throne. No one leaves, no one gets lost.",
  "Guardia Real Ébano. Nadie llega al trono. Nadie sale, nadie se pierde.")
t("DLG_C_EBANO_2", "Perdi. ...Isso conta como me perder?", "I lost. ...Does that count as getting lost?", "Perdí. ...¿Eso cuenta como perderse?")
t("DLG_C_ARAUTO_1", "Anuncio a sua chegada: derrotado!", "I announce your arrival: defeated!", "Anuncio tu llegada: ¡derrotado!")
t("DLG_C_ARAUTO_2", "Corrijo o anúncio: vitorioso. Que vergonha pro arauto.", "Correction to the announcement: victorious. How embarrassing for the herald.",
  "Corrijo el anuncio: victorioso. Qué vergüenza para el heraldo.")
t("DLG_C_TEMPERO_1", "Mil anos cozinhando pra um Rei que não come. Hoje eu cozinho uma batalha!",
  "A thousand years cooking for a King who doesn't eat. Today I'm cooking up a battle!", "Mil años cocinando para un Rey que no come. ¡Hoy cocino una batalla!")
t("DLG_C_TEMPERO_2", "Queimou. Como sempre.", "Burnt. As usual.", "Se quemó. Como siempre.")
t("OBJ_C_FOUNTAIN", "Uma fonte de água fresca no meio do castelo. Seus esqueletos bebem e descansam.",
  "A fountain of fresh water in the middle of the castle. Your skeletons drink and rest.", "Una fuente de agua fresca en medio del castillo. Tus esqueletos beben y descansan.")
t("DLG_C_DEG_1", "Provador Real Degustor. Provo tudo antes do Rei: sopa, chá, veneno. Agora vou provar você.",
  "Royal Taster Degustor. I taste everything before the King: soup, tea, poison. Now I'll taste you.",
  "Catador Real Degustor. Pruebo todo antes que el Rey: sopa, té, veneno. Ahora te voy a probar a ti.")
t("DLG_C_DEG_2", "Hmm. Tempero de 2040. Picante.", "Hmm. A 2040 flavor. Spicy.", "Mmm. Sabor de 2040. Picante.")
t("DLG_C_DEG_WIN", "Amargo... A derrota tem gosto de chá frio.", "Bitter... Defeat tastes like cold tea.", "Amargo... La derrota sabe a té frío.")
t("DLG_C_DEG_AFTER", "O Rei não come há mil anos. Eu provo a comida dele todo dia assim mesmo. Esperança tem gosto de pão quente.",
  "The King hasn't eaten in a thousand years. I taste his food every day anyway. Hope tastes like warm bread.",
  "El Rey no come desde hace mil años. Pruebo su comida cada día de todos modos. La esperanza sabe a pan caliente.")
t("DLG_C_DEG_FREE", "Sem coroa, sem patrão, sem cardápio. Quer provar uma batalha de verdade, só por gosto?",
  "No crown, no master, no menu. Want to taste a real battle, just for the flavor?", "Sin corona, sin patrón, sin menú. ¿Quieres probar una batalla de verdad, solo por el gusto?")
R.d("ebano", [say("DLG_C_EBANO_1", "SPK_EBANO"), battle("BTL_TAMER_EBANO", team([("sentinela", 86), ("ferreiro", 86)]), 1000, "ebano_beaten"),
              say("DLG_C_EBANO_2", "SPK_EBANO")])
R.d("ebano_depois", [say("DLG_C_EBANO_2", "SPK_EBANO")])
R.d("arauto", [say("DLG_C_ARAUTO_1", "SPK_ARAUTO"), battle("BTL_TAMER_ARAUTO", team([("escriba", 86), ("domador_escorpioes", 86)]), 1000, "arauto_beaten"),
               say("DLG_C_ARAUTO_2", "SPK_ARAUTO")])
R.d("arauto_depois", [say("DLG_C_ARAUTO_2", "SPK_ARAUTO")])
R.d("tempero", [say("DLG_C_TEMPERO_1", "SPK_TEMPERO"),
                battle("BTL_TAMER_TEMPERO", team([("chazeiro", 87), ("domador_escorpioes", 86)]), 1050, "tempero_beaten", [["pocao_g", 2]]),
                say("DLG_C_TEMPERO_2", "SPK_TEMPERO")])
R.d("tempero_depois", [say("DLG_C_TEMPERO_2", "SPK_TEMPERO")])
R.d("fonte", [say("OBJ_C_FOUNTAIN"), act("heal"), act("respawn")])
DEG_TEAM = [["degustor", 90]] + team([("sentinela", 89), ("escriba", 90), ("chazeiro", 89)])
R.d("degustor", [say("DLG_C_DEG_1", "SPK_DEGUSTOR"), say("DLG_C_DEG_2", "SPK_DEGUSTOR"),
                 battle("BTL_TAMER_DEGUSTOR", DEG_TEAM, 2500, "degustor_beaten", kind="boss"),
                 say("DLG_C_DEG_WIN", "SPK_DEGUSTOR"), say("DLG_C_DEG_AFTER", "SPK_DEGUSTOR"), act("refresh_map")])
R.d("degustor_depois", [say("DLG_C_DEG_AFTER", "SPK_DEGUSTOR")])
R.d("degustor_livre", [ask("DLG_C_DEG_FREE", "SPK_DEGUSTOR", [("OPT_C_TASTE", ref("degustor_luta")), ("OPT_P_NOT_NOW", None)])])
R.d("degustor_luta", [battle("", [["degustor", 88]], 0, kind="wild")])
R.tamer("ebano", "elmo", "SPK_EBANO", "ebano", "ebano_beaten", 3)
R.tamer("arauto", "clarim", "SPK_ARAUTO", "arauto", "arauto_beaten", 3)
R.tamer("tempero", "cobre", "SPK_TEMPERO", "tempero", "tempero_beaten", 3)
R.NPCS["degustor"] = {"name_key": "SPK_DEGUSTOR", "role": "guardian", "sprite": "res://assets/sprites/npc/skel_degustor.png", "frames": 2, "idle_fps": 2.0,
                      "behavior": "stand", "dialog": [{"dialog": ref("degustor")}], "tamer": {"vision": 3, "flag": "degustor_beaten"}}
R.NPCS["degustor_depois"] = {"name_key": "SPK_DEGUSTOR", "role": "story", "sprite": "res://assets/sprites/npc/skel_degustor.png", "frames": 2, "idle_fps": 2.0,
                             "behavior": "stand", "dialog": [{"if": "game_cleared", "dialog": ref("degustor_livre")}, {"dialog": ref("degustor_depois")}]}

# ------------------------------------------------------------------ Sala do Trono
t("DLG_C_T_0", "A sala do trono é fria e escura. No alto, um esqueleto imenso de coroa rachada.",
  "The throne room is cold and dark. Up high sits an immense skeleton wearing a cracked crown.",
  "La sala del trono es fría y oscura. En lo alto, un esqueleto inmenso con una corona agrietada.")
t("DLG_C_T_L1", "Tá escuro aqui. Deixa eu acender.", "It's dark in here. Let me light it up.", "Está oscuro aquí. Déjame encenderlo.")
t("DLG_C_T_LN", "Lia acende as velas, uma por uma. A sala inteira aparece: retratos, brinquedos, uma mesa posta para sete.",
  "Lia lights the candles one by one. The whole room appears: portraits, toys, a table set for seven.",
  "Lia enciende las velas, una por una. Aparece toda la sala: retratos, juguetes, una mesa puesta para siete.")
t("DLG_C_T_L2", "Pronto. Agora o senhor consegue ver o que perdeu?", "There. Now can you see what you lost?", "Listo. ¿Ahora puede ver lo que perdió?")
t("DLG_C_T_TN", "Taro acende as velas com raiva, uma por uma. A sala inteira aparece: retratos, brinquedos, uma mesa posta para sete.",
  "Taro angrily lights the candles one by one. The whole room appears: portraits, toys, a table set for seven.",
  "Taro enciende las velas con rabia, una por una. Aparece toda la sala: retratos, juguetes, una mesa puesta para siete.")
t("DLG_C_T_T1", "Pronto. Agora olha pra gente.", "There. Now look at us.", "Listo. Ahora míranos.")
t("DLG_C_REI_1", "Então você veio. O último do meu sangue, de mil anos depois.", "So you came. The last of my blood, from a thousand years ahead.",
  "Así que viniste. El último de mi sangre, de mil años después.")
t("DLG_C_REI_2", "Eu sou Ossárion. Perdi minha família uma vez. Não vou perder de novo.", "I am Ossárion. I lost my family once. I will not lose them again.",
  "Soy Ossárion. Perdí a mi familia una vez. No la perderé de nuevo.")
t("DLG_C_REI_3", "A coroa racha mais um pouco, com um som de vidro. O mesmo som do museu.", "The crown cracks a little more, with a sound like glass. The same sound as in the museum.",
  "La corona se agrieta un poco más, con un sonido de cristal. El mismo sonido del museo.")
t("DLG_C_REI_4", "Coloque a coroa. Fique. Ninguém mais se perde.", "Put on the crown. Stay. No one will ever be lost again.", "Ponte la corona. Quédate. Nadie volverá a perderse.")
t("DLG_C_TRY_0", "Você estende a mão para a coroa...", "You reach out for the crown...", "Extiendes la mano hacia la corona...")
t("DLG_C_TRY_L", "Não! Se você colocar, nunca mais sai daqui!", "No! If you put it on, you'll never leave this place!", "¡No! ¡Si te la pones, nunca saldrás de aquí!")
t("DLG_C_TRY_T", "Eu avisei. Eu mesmo tiro ela da sua cabeça.", "I warned you. I'll pull it off your head myself.", "Te lo advertí. Yo mismo te la quito de la cabeza.")
t("DLG_C_TRY_1", "Você recua a mão. Seu parceiro não solta a sua.", "You pull your hand back. Your partner won't let go of it.", "Retiras la mano. Tu compañero no suelta la tuya.")
t("DLG_C_REI_5", "Então você é igual a todos. Vai embora e me deixa sozinho.", "Then you're like all the rest. You'll leave and let me be alone.",
  "Entonces eres como todos. Te irás y me dejarás solo.")
t("DLG_C_REI_6", "Não. Desta vez, ninguém sai.", "No. This time, no one leaves.", "No. Esta vez, nadie sale.")
t("DLG_C_REI_AGAIN", "Voltou. A coroa ainda espera por você.", "You've returned. The crown is still waiting for you.", "Volviste. La corona aún te espera.")
t("DLG_C_REI_DOWN", "O Rei cai de joelhos. A coroa pende, torta, da cabeça dele.", "The King falls to his knees. The crown hangs crooked from his head.",
  "El Rey cae de rodillas. La corona le cuelga, torcida, de la cabeza.")
t("DLG_C_REI_DOWN2", "Mil anos... e perco de novo.", "A thousand years... and I lose again.", "Mil años... y vuelvo a perder.")

# Final A — Redimir
t("DLG_C_A_1", "Você tira do bolso a carta da Alva e a entrega ao Rei.", "You take Alva's letter from your pocket and hand it to the King.",
  "Sacas del bolsillo la carta de Alva y se la entregas al Rey.")
t("DLG_C_A_2", "A letra da minha filha...", "My daughter's handwriting...", "La letra de mi hija...")
t("DLG_C_A_3", "\"Pai. Não precisa segurar a gente. A gente já está com o senhor, em tudo o que o senhor construiu.\"",
  "\"Father. You don't need to hold on to us. We're already with you, in everything you built.\"",
  "\"Padre. No necesitas retenernos. Ya estamos contigo, en todo lo que construiste.\"")
t("DLG_C_A_4", "\"Deixa a gente descansar. Deixa o senhor viver. Com amor, Alva.\"", "\"Let us rest. Let yourself live. With love, Alva.\"",
  "\"Déjanos descansar. Déjate vivir. Con amor, Alva.\"")
t("DLG_C_A_5", "Ela sempre escreveu melhor do que eu reinei.", "She always wrote better than I ruled.", "Ella siempre escribió mejor de lo que yo reiné.")
t("DLG_C_A_RM", "Minha tia soltou os mineiros só porque você pediu.", "My aunt released the miners just because you asked.",
  "Mi tía soltó a los mineros solo porque tú se lo pediste.")
t("DLG_C_A_RP", "Você deu remédio a quem minha sobrinha adoeceu.", "You gave medicine to those my niece made ill.", "Diste remedio a quienes mi sobrina enfermó.")
t("DLG_C_A_RO", "E Ossório leu a verdade em voz alta. Meu irmão ficou do seu lado.", "And Ossório read the truth out loud. My brother stood by your side.",
  "Y Ossório leyó la verdad en voz alta. Mi hermano se puso de tu lado.")
t("DLG_C_A_6", "Você não veio tomar o meu lugar. Veio devolver o lugar de todos.", "You didn't come to take my place. You came to give everyone back theirs.",
  "No viniste a quitarme el lugar. Viniste a devolverle el suyo a todos.")
t("DLG_C_A_7", "O Rei tira a coroa. Por um instante, ela canta, como no museu.", "The King takes off the crown. For a moment it sings, just like in the museum.",
  "El Rey se quita la corona. Por un instante canta, como en el museo.")
t("DLG_C_A_8", "Ninguém sai, ninguém se perde... Que lei boba. Todo mundo se perde um pouco. É assim que se acha o caminho.",
  "No one leaves, no one gets lost... What a silly law. Everyone gets a little lost. That's how you find your way.",
  "Nadie sale, nadie se pierde... Qué ley tan tonta. Todos nos perdemos un poco. Así se encuentra el camino.")
t("DLG_C_A_9", "Ele mesmo quebra a coroa nas mãos. A rachadura vira luz.", "He breaks the crown in his own hands. The crack turns into light.",
  "Él mismo rompe la corona con sus manos. La grieta se vuelve luz.")
t("DLG_C_A_10", "Seis figuras de luz aparecem na sala. A família veio se despedir.", "Six figures of light appear in the room. The family has come to say goodbye.",
  "Seis figuras de luz aparecen en la sala. La familia vino a despedirse.")
t("DLG_C_BYE_RAM", "Primo! Valeu a segunda volta. A terceira eu dispenso!", "Cousin! Thanks for the second round. I'll pass on a third!",
  "¡Primo! Gracias por la segunda vuelta. ¡La tercera la paso!")
t("DLG_C_BYE_FOR", "Regra final: descansar. Até que enfim.", "Final rule: rest. At long last.", "Regla final: descansar. Por fin.")
t("DLG_C_BYE_MUS", "Não me esqueçam, tá? ...Brincadeira. Eu sei que não vão, queridos.", "Don't forget me, okay? ...Just kidding. I know you won't, darlings.",
  "No me olviden, ¿eh? ...Es broma. Sé que no lo harán, queridos.")
t("DLG_C_BYE_CAL", "Família não abandona família. Por isso agora a gente te deixa ir, irmão.", "Family doesn't abandon family. That's why we're letting you go now, brother.",
  "La familia no abandona a la familia. Por eso ahora te dejamos ir, hermano.")
t("DLG_C_BYE_ALV", "Pai, o senhor sorriu. Eu vi.", "Father, you smiled. I saw it.", "Padre, sonreíste. Lo vi.")
t("DLG_C_BYE_DUN", "Ergui um farol pra você voltar. Agora volta pra vida, meu amor.", "I raised a lighthouse so you'd come home. Now come back to life, my love.",
  "Levanté un faro para que volvieras. Ahora vuelve a la vida, mi amor.")
t("DLG_C_A_11", "A família vira poeira de luz. Os esqueletos do continente continuam vivos, mas agora ninguém manda neles.",
  "The family turns into dust of light. The continent's skeletons live on, but now no one commands them.",
  "La familia se vuelve polvo de luz. Los esqueletos del continente siguen vivos, pero ya nadie los manda.")
t("DLG_C_A_12", "Não tenho coroa, nem família, nem reino. Tenho um herdeiro teimoso.", "I have no crown, no family, no kingdom. I have a stubborn heir.",
  "No tengo corona, ni familia, ni reino. Tengo un heredero testarudo.")
t("DLG_C_A_13", "Posso ir com você? Quero conhecer o mundo que eu fechei.", "May I come with you? I want to see the world I shut away.",
  "¿Puedo ir contigo? Quiero conocer el mundo que cerré.")

# Final B — Derrotar
t("DLG_C_B_1", "O último golpe acerta a coroa. Ela se parte em mil pedaços.", "The final blow strikes the crown. It shatters into a thousand pieces.",
  "El último golpe alcanza la corona. Se rompe en mil pedazos.")
t("DLG_C_B_2", "Um vento atravessa o castelo. Em todo o continente, os Guardiões somem de uma vez, sem despedida.",
  "A wind sweeps through the castle. All across the continent, the Guardians vanish at once, without a goodbye.",
  "Un viento atraviesa el castillo. En todo el continente, los Guardianes desaparecen de golpe, sin despedirse.")
t("DLG_C_B_3", "Tia... Musga... Caliço... Alva... Duna...", "Auntie... Musga... Caliço... Alva... Duna...", "Tía... Musga... Caliço... Alva... Duna...")
t("DLG_C_B_4", "Ninguém responde. O Rei fica sozinho no chão do trono.", "No one answers. The King is left alone on the throne room floor.",
  "Nadie responde. El Rey se queda solo en el suelo del trono.")
t("DLG_C_B_5", "Eu prendi todos para não perder ninguém. E perdi todos assim mesmo.", "I held everyone captive so I wouldn't lose anyone. And I lost them all anyway.",
  "Retuve a todos para no perder a nadie. Y los perdí a todos igual.")
t("DLG_C_B_6", "Os esqueletos do continente continuam vivos, livres da coroa.", "The continent's skeletons live on, free of the crown.",
  "Los esqueletos del continente siguen vivos, libres de la corona.")
t("DLG_C_B_7", "Não tenho mais ninguém.", "I have no one left.", "Ya no tengo a nadie.")
t("DLG_C_B_8", "Ele se levanta devagar e caminha até você, em silêncio.", "He slowly gets up and walks over to you, in silence.",
  "Se levanta despacio y camina hacia ti, en silencio.")
t("DLG_C_KING_MARK", "O marcador de ossos do Rei se enche de uma vez.", "The King's bone gauge fills all at once.", "El marcador de huesos del Rey se llena de golpe.")

# Comum: pais do Taro, Lia e o epílogo de 2040
t("DLG_C_E_1", "Lá embaixo, no portão, dois guardas soltam os remos ao mesmo tempo.", "Down at the gate, two guards drop their oars at the same moment.",
  "Abajo, en la puerta, dos guardias sueltan los remos a la vez.")
t("DLG_C_E_PAI", "Taro? É você?", "Taro? Is that you?", "¿Taro? ¿Eres tú?")
t("DLG_C_E_MAE", "Nosso pequeno remador! Você cresceu tanto!", "Our little rower! You've grown so much!", "¡Nuestro pequeño remero! ¡Cuánto creciste!")
t("DLG_C_E_T1", "Pai. Mãe. ...Eu achei vocês.", "Dad. Mom. ...I found you.", "Papá. Mamá. ...Los encontré.")
t("DLG_C_E_PAI2", "Foi você que nos achou, filho. A gente é que tava perdido.", "You're the one who found us, son. We were the lost ones.",
  "Fuiste tú quien nos encontró, hijo. Los perdidos éramos nosotros.")
t("DLG_C_E_T2", "Passei o caminho todo com raiva dele. Agora... ele só queria a família de volta. Igual eu.",
  "I spent the whole journey angry at him. Now... he just wanted his family back. Same as me.",
  "Pasé todo el camino enojado con él. Ahora... solo quería a su familia de vuelta. Igual que yo.")
t("DLG_C_E_T3", "Tá perdoado. Mas vocês me devem uns cem bolos de aniversário.", "You're forgiven. But you owe me about a hundred birthday cakes.",
  "Están perdonados. Pero me deben como cien pasteles de cumpleaños.")
t("DLG_C_E_L1", "O Taro achou eles! Agora só falta o meu farol.", "Taro found them! Now there's just my lighthouse left.", "¡Taro los encontró! Ahora solo falta mi faro.")
t("DLG_C_E_L2", "Vamos pra casa? Eu quero acender o farol com você do lado.", "Shall we go home? I want to light the lighthouse with you beside me.",
  "¿Vamos a casa? Quiero encender el faro contigo al lado.")
t("DLG_C_E_TL", "A Lia prometeu acender o farol. Aposto que já tá lá em cima, toda orgulhosa.", "Lia promised to light the lighthouse. I bet she's already up there, all proud.",
  "Lia prometió encender el faro. Apuesto a que ya está allá arriba, toda orgullosa.")
t("DLG_C_M_1", "2040. Museu do Litoral. Exposição \"O Reino Perdido de Ossório\".", "2040. Coastal Museum. Exhibition: \"The Lost Kingdom of Ossório\".",
  "2040. Museo del Litoral. Exposición \"El Reino Perdido de Ossório\".")
t("DLG_C_M_2", "Uma vitrine está vazia. Na plaquinha: \"Peça em restauração\".", "One display case is empty. The little sign reads: \"Piece under restoration\".",
  "Una vitrina está vacía. En el cartelito: \"Pieza en restauración\".")
t("DLG_C_M_3", "Lá fora, sem ninguém tocar no interruptor, a luz do velho farol se acende.", "Outside, with no one touching the switch, the old lighthouse's light turns on.",
  "Afuera, sin que nadie toque el interruptor, la luz del viejo faro se enciende.")
t("DLG_C_M_4", "O eco ainda chama. Esta história continua.", "The echo still calls. This story continues.", "El eco aún llama. Esta historia continúa.")
t("OBJ_C_VITRINE", "\"Coroa de osso, Reino de Ossório. Peça em restauração.\"", "\"Bone crown, Kingdom of Ossório. Piece under restoration.\"",
  "\"Corona de hueso, Reino de Ossório. Pieza en restauración.\"")

RED = {"flags": ["red_minas", "red_pantano", "red_ossorio"], "min": 2}
R.d("trono", [say("DLG_C_T_0"), lia("DLG_C_T_L1"), nar("DLG_C_T_LN", **{"if": "partner_lia"}), lia("DLG_C_T_L2"),
              nar("DLG_C_T_TN", **{"if": "partner_taro"}), taro("DLG_C_T_T1"), flag("trono_iluminado"),
              say("DLG_C_REI_1", "SPK_REI"), say("DLG_C_REI_2", "SPK_REI"), say("DLG_C_REI_3"), goto(ref("trono_coroa"))])
R.d("trono_de_novo", [say("DLG_C_REI_AGAIN", "SPK_REI"), goto(ref("trono_coroa"))])
R.d("trono_coroa", [ask("DLG_C_REI_4", "SPK_REI", [("OPT_C_CROWN", ref("coroa_tentar")), ("OPT_C_REFUSE", ref("recusar"))])])
R.d("coroa_tentar", [say("DLG_C_TRY_0"), lia("DLG_C_TRY_L"), taro("DLG_C_TRY_T"), say("DLG_C_TRY_1"), goto(ref("recusar"))])
R.d("recusar", [say("DLG_C_REI_5", "SPK_REI"), say("DLG_C_REI_6", "SPK_REI"), flag("rei_falou"),
                battle("BTL_TAMER_REI", [["rei_esqueleto", 120], ["jardineiro_lirios_3", 78]], 0, "rei_beaten", kind="boss"),
                say("DLG_C_REI_DOWN"), say("DLG_C_REI_DOWN2", "SPK_REI"),
                {"goto": ref("final_a"), "if": "has_carta_alva", "if_count": RED},
                goto(ref("final_b"))])
R.d("final_a", [say("DLG_C_A_1"), act("take_item", item="carta_alva", n=1), say("DLG_C_A_2", "SPK_REI"), say("DLG_C_A_3"), say("DLG_C_A_4"),
                say("DLG_C_A_5", "SPK_REI"),
                say("DLG_C_A_RM", "SPK_REI") | {"if": "red_minas"}, say("DLG_C_A_RP", "SPK_REI") | {"if": "red_pantano"},
                say("DLG_C_A_RO", "SPK_REI") | {"if": "red_ossorio"}, say("DLG_C_A_6", "SPK_REI"),
                say("DLG_C_A_7"), say("DLG_C_A_8", "SPK_REI"), {"action": "sfx", "name": "golden"}, say("DLG_C_A_9"), say("DLG_C_A_10"),
                say("DLG_C_BYE_RAM", "SPK_RAMALHO"), say("DLG_C_BYE_FOR", "SPK_FORNALHA"), say("DLG_C_BYE_MUS", "SPK_MUSGA"),
                say("DLG_C_BYE_CAL", "SPK_CALICO"), say("DLG_C_BYE_ALV", "SPK_ALVA"), say("DLG_C_BYE_DUN", "SPK_DUNA"), say("DLG_C_A_11"),
                say("DLG_C_A_12", "SPK_REI"), say("DLG_C_A_13", "SPK_REI"), flag("final_a"), goto(ref("rei_entra"))])
R.d("final_b", [say("DLG_C_B_1"), {"action": "sfx", "name": "grow_flash"}, say("DLG_C_B_2"), say("DLG_C_B_3", "SPK_REI"), say("DLG_C_B_4"),
                say("DLG_C_B_5", "SPK_REI"), say("DLG_C_B_6"), say("DLG_C_B_7", "SPK_REI"), say("DLG_C_B_8"), flag("final_b"), goto(ref("rei_entra"))])
R.d("rei_entra", [say("DLG_C_KING_MARK"), act("marker", species="rei_esqueleto", amount=100),
                  act("give_monster", species="rei_esqueleto", age=100), flag("rei_recrutado"), act("hide_npc", id="rei"), goto(ref("final_comum"))])
R.d("final_comum", [say("DLG_C_E_1"), say("DLG_C_E_PAI", "SPK_PAI_TARO"), say("DLG_C_E_MAE", "SPK_MAE_TARO"),
                    taro("DLG_C_E_T1"), say("DLG_C_E_PAI2", "SPK_PAI_TARO"), say("DLG_C_E_T2", "SPK_TARO"), say("DLG_C_E_T3", "SPK_TARO"),
                    lia("DLG_C_E_L1"), lia("DLG_C_E_L2"), taro("DLG_C_E_TL"),
                    act("fade", out=True), act("wait", s=0.6),
                    act("warp", map="museu_2040", x=7, y=6, facing="up", hide_player=True),
                    say("DLG_C_M_1"), say("DLG_C_M_2"), say("DLG_C_M_3"), say("DLG_C_M_4"),
                    flag("game_cleared"), act("credits"), act("heal_all"),
                    act("warp", map="praia_despertar", x=10, y=17, facing="left")])
R.NPCS["rei"] = {"name_key": "SPK_REI", "role": "guardian", "sprite": "res://assets/sprites/npc/skel_rei.png", "frames": 2, "idle_fps": 1.5,
                 "behavior": "stand", "dialog": [{"if": "rei_falou", "dialog": ref("trono_de_novo")}, {"dialog": ref("trono")}]}
R.d("vitrine", [say("OBJ_C_VITRINE")])

# ------------------------------------------------------------------ Pós-jogo: Praia, Bento, farol e ecos dos Guardiões
t("DLG_C_EP_0", "Praia do Despertar. O farol está aceso, girando devagar sobre o mar.", "Shore of Awakening. The lighthouse is lit, turning slowly over the sea.",
  "Playa del Despertar. El faro está encendido, girando despacio sobre el mar.")
t("DLG_C_EP_B1", "Olha só quem voltou! E olha o farol: aceso, depois de mil anos.", "Look who's back! And look at the lighthouse: lit, after a thousand years.",
  "¡Mira quién volvió! Y mira el faro: encendido, después de mil años.")
t("DLG_C_EP_L", "Eu disse que ia acender! Agora ninguém se perde no mar.", "I told you I'd light it! Now no one gets lost at sea.",
  "¡Te dije que lo encendería! Ahora nadie se pierde en el mar.")
t("DLG_C_EP_B2", "Foi a pequena da lamparina. Subiu lá ontem à noite, toda orgulhosa.", "It was the little one with the lamp. She climbed up last night, so proud of herself.",
  "Fue la pequeña del farolillo. Subió anoche, toda orgullosa.")
t("DLG_C_EP_T", "Ela conseguiu. ...Não conta pra ela que eu fiquei feliz.", "She did it. ...Don't tell her I'm happy about it.", "Lo logró. ...No le digas que me alegré.")
t("DLG_C_EP_KA", "Minha Duna ergueu este farol. Ela ia gostar de vê-lo aceso.", "My Duna raised this lighthouse. She would have loved to see it lit.",
  "Mi Duna levantó este faro. Le habría encantado verlo encendido.")
t("DLG_C_EP_KB", "O Rei olha para o farol em silêncio, por muito tempo.", "The King looks at the lighthouse in silence for a long time.",
  "El Rey mira el faro en silencio durante mucho tiempo.")
t("DLG_C_EP_B3", "O continente é livre. Vai, completa teu Ossário. Dizem que os ecos dos Guardiões ainda esperam uma revanche.",
  "The continent is free. Go on, finish your Ossuary. They say the Guardians' echoes are still waiting for a rematch.",
  "El continente es libre. Anda, completa tu Osario. Dicen que los ecos de los Guardianes aún esperan una revancha.")
t("DLG_C_EP_B4", "E quando quiser voltar pra casa... o farol fica aceso. Vai que ele chama de volta.",
  "And whenever you want to go home... the lighthouse stays lit. Who knows, maybe it'll call you back.",
  "Y cuando quieras volver a casa... el faro sigue encendido. A lo mejor te llama de vuelta.")
t("DLG_C_BENTO_POST", "Farol aceso dá até vontade de pescar de noite. Os peixes é que não gostaram muito.",
  "A lit lighthouse makes me want to fish at night. The fish aren't too thrilled about it.",
  "Con el faro encendido dan ganas de pescar de noche. A los peces no les hizo mucha gracia.")
t("OBJ_C_LIGHTHOUSE_LIT", "O farol está aceso. A luz gira devagar sobre o mar, como quem procura alguém.",
  "The lighthouse is lit. The light turns slowly over the sea, as if searching for someone.",
  "El faro está encendido. La luz gira despacio sobre el mar, como quien busca a alguien.")
R.d("epilogo_praia", [say("DLG_C_EP_0"), say("DLG_C_EP_B1", "SPK_BENTO"), lia("DLG_C_EP_L"),
                      say("DLG_C_EP_B2", "SPK_BENTO") | {"if": "partner_taro"}, taro("DLG_C_EP_T"),
                      say("DLG_C_EP_KA", "SPK_REI") | {"if": "final_a"}, say("DLG_C_EP_KB") | {"if": "final_b"},
                      say("DLG_C_EP_B3", "SPK_BENTO"), say("DLG_C_EP_B4", "SPK_BENTO"), flag("epilogo_visto"), act("respawn")])
R.d("bento_final", [say("DLG_C_BENTO_POST", "SPK_BENTO"), say("DLG_C_EP_B3", "SPK_BENTO")])
R.d("farol_aceso", [say("OBJ_C_LIGHTHOUSE_LIT")])

ECOS = {
    "ramalho": ("Sou só um eco do Ramalho, preso no cabo do machado. Mas eco também quer revanche!",
                "I'm just an echo of Ramalho, stuck in the axe handle. But echoes want rematches too!",
                "Solo soy un eco de Ramalho, atrapado en el mango del hacha. ¡Pero los ecos también quieren revancha!",
                [("lenhador", 95), ("flautista", 95), ("herborista", 95)]),
    "fornalha": ("Um eco da Tia. Regra do eco: repetir a última luta. Mais forte.", "An echo of Auntie. Rule of echoes: repeat the last fight. Stronger.",
                 "Un eco de la Tía. Regla del eco: repetir la última pelea. Más fuerte.",
                 [("mineiro", 95), ("ferreiro", 95), ("gasista", 96), ("aguadeiro", 95)]),
    "musga": ("Eco da Musga, querido. Até eco fofoca: dizem que você ficou forte. Prova?",
              "Musga's echo, darling. Even echoes gossip: they say you got strong. Prove it?",
              "Eco de Musga, querido. Hasta los ecos chismean: dicen que te hiciste fuerte. ¿Lo demuestras?",
              [("lavadeira", 96), ("palafiteiro", 95), ("jardineiro_lirios", 95), ("cogumeleiro", 96)]),
    "calico": ("Eco do Comandante. Em formação, uma última vez!", "Echo of the Commander. Fall in, one last time!",
               "Eco del Comandante. ¡En formación, una última vez!", [("sentinela", 97), ("escriba", 96), ("sineiro", 96), ("lenhador", 97)]),
    "alva": ("Sou o eco da Alva. Meu pai está com você? Então me mostra que ele está em boas mãos.",
             "I'm Alva's echo. Is my father with you? Then show me he's in good hands.",
             "Soy el eco de Alva. ¿Mi padre está contigo? Entonces muéstrame que está en buenas manos.",
             [("carregador", 98), ("escultor", 97), ("chazeiro", 98), ("mineiro", 97)]),
    "duna": ("O eco da rainha ainda dança na areia. Dança comigo?", "The queen's echo still dances on the sand. Will you dance with me?",
             "El eco de la reina aún baila en la arena. ¿Bailas conmigo?",
             [("domador_escorpioes", 99), ("cartografo", 99), ("tamborileiro", 100), ("palafiteiro", 99)]),
}
SPK = {"ramalho": "SPK_RAMALHO", "fornalha": "SPK_FORNALHA", "musga": "SPK_MUSGA", "calico": "SPK_CALICO", "alva": "SPK_ALVA", "duna": "SPK_DUNA"}
NPC_ID = {"ramalho": "ramalho_depois", "fornalha": "fornalha", "musga": "musga", "calico": "calico", "alva": "alva", "duna": "duna"}
t("DLG_C_ECO_BYE", "O eco sorri e se desfaz no vento... até a próxima.", "The echo smiles and dissolves into the wind... until next time.",
  "El eco sonríe y se deshace en el viento... hasta la próxima.")
for g, (pt, en, es, tm) in ECOS.items():
    key = f"DLG_C_ECO_{g.upper()}"
    t(key, pt, en, es)
    pt2, en2, es2 = R.T[SPK[g]] if SPK[g] in R.T else (None, None, None)
    R.d(f"eco_{g}", [ask(key, SPK[g], [("OPT_P_FIGHT", ref(f"eco_{g}_luta")), ("OPT_P_NOT_NOW", None)])])
    R.d(f"eco_{g}_luta", [battle(f"BTL_TAMER_ECO_{g.upper()}", team(tm), 3000, f"eco_{g}_vencido", [["pocao_g", 2]]), say("DLG_C_ECO_BYE")])
# nomes de batalha dos ecos com acento e tradução corretos
for g, (pt, en, es) in {"RAMALHO": ("Eco de Ramalho", "Echo of Ramalho", "Eco de Ramalho"),
                        "FORNALHA": ("Eco da Tia Fornalha", "Echo of Aunt Furnace", "Eco de la Tía Fragua"),
                        "MUSGA": ("Eco de Musga", "Echo of Musga", "Eco de Musga"), "CALICO": ("Eco de Caliço", "Echo of Caliço", "Eco de Caliço"),
                        "ALVA": ("Eco de Alva", "Echo of Alva", "Eco de Alva"), "DUNA": ("Eco da Rainha Duna", "Echo of Queen Duna", "Eco de la Reina Duna")}.items():
    t(f"BTL_TAMER_ECO_{g}", pt, en, es)


# ------------------------------------------------------------------ encontros (balance.json: selvagens 79–84)
def e(sp, st, a, b, rar, w=None):
    d = {"species": sp, "stage": st, "min_level": a, "max_level": b, "rarity": rar}
    if w:
        d["weight"] = w
    return d


R.TABLES.update({
    "castelo_leste": [e("sentinela_3", 3, 79, 82, "comum"), e("escriba_3", 3, 80, 83, "raro"), e("ferreiro_3", 3, 79, 82, "incomum")],
    "castelo_oeste": [e("domador_escorpioes_3", 3, 81, 84, "comum"), e("sentinela_3", 3, 81, 84, "comum")],
})

# ------------------------------------------------------------------ mapas
# Portão: pátio diante da muralha do castelo
g = Grid(40, 30, "s")
g.fill(0, 0, 39, 0, "B"); g.fill(0, 0, 0, 29, "B"); g.fill(39, 0, 39, 29, "B"); g.fill(0, 29, 39, 29, "B")
g.fill(4, 0, 35, 8, "W")
g.fill(6, 9, 33, 26, "c")
g.fill(19, 8, 20, 29, "p")
portao = {"id": "castelo_portao", "region": "castelo", "name_key": "MAP_CASTELO_PORTAO", "tileset": "overworld",
          "legend": {"s": "sand", "B": "sandstone", "W": "castle_wall", "c": "castle_floor", "p": "carpet"},
          "ground": g.rows(), "spawn": {"x": 19, "y": 27, "facing": "up"}, "tint": [0.85, 0.8, 0.9],
          "props": [{"type": "castle_door", "x": 20, "y": 7}, {"type": "pillar", "x": 9, "y": 11}, {"type": "pillar", "x": 30, "y": 11},
                    {"type": "pillar", "x": 9, "y": 20}, {"type": "pillar", "x": 30, "y": 20}, {"type": "torch", "x": 16, "y": 9},
                    {"type": "torch", "x": 23, "y": 9}, {"type": "statue_prince", "x": 13, "y": 23}, {"type": "statue_prince", "x": 26, "y": 23}],
          "npcs": [{"id": "pai_taro", "x": 19, "y": 10, "facing": "down"}, {"id": "mae_taro", "x": 20, "y": 10, "facing": "down"},
                   {"id": "taro_portao", "x": 23, "y": 12, "facing": "left", "if": "partner_lia", "if_not": "game_cleared"},
                   {"id": "calico_aliado", "x": 14, "y": 15, "facing": "right", "if": "ossorio_revelou", "if_not": "game_cleared"}],
          "warps": [{"x": 19, "y": 29, "to": "palmeiral", "tx": 19, "ty": 1, "facing": "down", "sfx": ""},
                    {"x": 20, "y": 29, "to": "palmeiral", "tx": 20, "ty": 1, "facing": "down", "sfx": ""},
                    {"x": 19, "y": 8, "to": "castelo_salao", "tx": 14, "ty": 22, "facing": "up", "sfx": "door"},
                    {"x": 20, "y": 8, "to": "castelo_salao", "tx": 15, "ty": 22, "facing": "up", "sfx": "door"}],
          "on_enter": [{"if_not": "portao_visto", "dialog": ref("chegada_portao")}], "ambient": ["embers"]}

# Grande Salão
g = Grid(30, 24, "W")
g.fill(3, 2, 26, 21, "c")
g.fill(14, 0, 15, 23, "p")
salao = {"id": "castelo_salao", "region": "castelo", "name_key": "MAP_CASTELO_SALAO", "tileset": "overworld",
         "legend": {"W": "castle_wall", "c": "castle_floor", "p": "carpet"}, "ground": g.rows(), "spawn": {"x": 14, "y": 22, "facing": "up"},
         "tint": [0.72, 0.66, 0.8],
         "props": [{"type": "pillar", "x": 12, "y": 6}, {"type": "pillar", "x": 17, "y": 6}, {"type": "pillar", "x": 12, "y": 13},
                   {"type": "pillar", "x": 17, "y": 13}, {"type": "pillar", "x": 12, "y": 19}, {"type": "pillar", "x": 17, "y": 19},
                   {"type": "candelabra", "x": 4, "y": 3}, {"type": "candelabra", "x": 25, "y": 3}, {"type": "candelabra", "x": 4, "y": 12},
                   {"type": "candelabra", "x": 25, "y": 12}, {"type": "fountain", "x": 6, "y": 20, "dialog": ref("fonte")},
                   {"type": "table", "x": 22, "y": 4}, {"type": "barrel", "x": 25, "y": 6}, {"type": "kettle", "x": 20, "y": 4}],
         "npcs": [{"id": "ebano", "x": 11, "y": 16, "facing": "right"}, {"id": "arauto", "x": 18, "y": 10, "facing": "left"},
                  {"id": "tempero", "x": 20, "y": 6, "facing": "left"},
                  {"id": "degustor", "x": 14, "y": 3, "facing": "down", "if_not": "degustor_beaten"},
                  {"id": "degustor_depois", "x": 17, "y": 3, "facing": "left", "if": "degustor_beaten"}],
         "warps": [{"x": 14, "y": 23, "to": "castelo_portao", "tx": 19, "ty": 9, "facing": "down", "sfx": "door"},
                   {"x": 15, "y": 23, "to": "castelo_portao", "tx": 20, "ty": 9, "facing": "down", "sfx": "door"},
                   {"x": 14, "y": 0, "to": "sala_trono", "tx": 9, "ty": 14, "facing": "up", "sfx": "door"},
                   {"x": 15, "y": 0, "to": "sala_trono", "tx": 10, "ty": 14, "facing": "up", "sfx": "door"}],
         "spawns": [{"id": "c_leste", "table": "castelo_leste", "x": 22, "y": 15, "radius": 3, "count": 2},
                    {"id": "c_oeste", "table": "castelo_oeste", "x": 7, "y": 8, "radius": 2, "count": 1}],
         "ambient": ["embers"]}

# Sala do Trono
g = Grid(20, 16, "W")
g.fill(2, 2, 17, 14, "c")
g.fill(9, 4, 10, 15, "p")
trono = {"id": "sala_trono", "region": "castelo", "name_key": "MAP_SALA_TRONO", "tileset": "overworld",
         "legend": {"W": "castle_wall", "c": "castle_floor", "p": "carpet"}, "ground": g.rows(), "spawn": {"x": 9, "y": 14, "facing": "up"},
         "tint": [0.6, 0.55, 0.7],
         "props": [{"type": "throne", "x": 10, "y": 3}, {"type": "crown_pedestal", "x": 13, "y": 4, "if_not": "rei_beaten"},
                   {"type": "pillar", "x": 3, "y": 7}, {"type": "pillar", "x": 16, "y": 7}, {"type": "pillar", "x": 3, "y": 12},
                   {"type": "pillar", "x": 16, "y": 12},
                   {"type": "candelabra", "x": 5, "y": 4, "if": "trono_iluminado"}, {"type": "candelabra", "x": 15, "y": 4, "if": "trono_iluminado"},
                   {"type": "candelabra", "x": 5, "y": 10, "if": "trono_iluminado"}, {"type": "candelabra", "x": 14, "y": 10, "if": "trono_iluminado"},
                   {"type": "table", "x": 7, "y": 7}, {"type": "portrait", "x": 6, "y": 1}, {"type": "portrait", "x": 13, "y": 1}],
         "npcs": [{"id": "rei", "x": 10, "y": 4, "facing": "down", "if_not": "rei_recrutado"}],
         "warps": [{"x": 9, "y": 15, "to": "castelo_salao", "tx": 14, "ty": 1, "facing": "down", "sfx": "door"},
                   {"x": 10, "y": 15, "to": "castelo_salao", "tx": 15, "ty": 1, "facing": "down", "sfx": "door"}],
         "on_enter": [{"if": "rei_falou", "if_not": "rei_beaten", "dialog": ref("trono_de_novo")},
                      {"if_not": "rei_beaten", "dialog": ref("trono")}],
         "ambient": ["embers"]}

museu = {"id": "museu_2040", "region": "castelo", "name_key": "MAP_MUSEU", "tileset": "overworld",
         "legend": {"T": "wall_top", "w": "wall", "n": "wall_window", ".": "floor", "m": "mat"},
         "ground": ["TTTTTTTTTTTTTT", "TwwnwwwwwwnwwT"] + ["T............T"] * 6 + ["TTTTTTTTTTTTTT"],
         "spawn": {"x": 7, "y": 6, "facing": "up"},
         "props": [{"type": "vitrine_empty", "x": 7, "y": 3, "dialog": ref("vitrine")}, {"type": "portrait", "x": 3, "y": 1},
                   {"type": "portrait", "x": 11, "y": 1}, {"type": "rug", "x": 7, "y": 6}, {"type": "plant", "x": 1, "y": 7}, {"type": "plant", "x": 12, "y": 7},
                   {"type": "map_board", "x": 4, "y": 4}],
         "npcs": [], "warps": [], "ambient": ["dust_motes"]}

R.MAPS.update({"castelo_portao": portao, "castelo_salao": salao, "sala_trono": trono, "museu_2040": museu})
R.BATTLE_BG["castelo"] = "res://assets/battle/bg_castelo.png"

R.NPCS["bento_final"] = human("bento_final", "SPK_BENTO", [{"dialog": ref("bento_final")}], "stand", role="lore")
R.NPCS["bento_final"]["sprite"] = "res://assets/sprites/bento.png"

# ------------------------------------------------------------------ documento
R.DOC = {
    "title": "Final: Castelo do Rei Esqueleto, os 2 finais e o pós-jogo", "phase": "4h", "duration": "20 min",
    "ages": "chegada 80–86; selvagens 79–84; domadores 86–87; Provador Real ~90; Rei 120 (com escolta de 78)",
    "problem": "O castelo inteiro obedece à coroa rachada. Os levados (entre eles os **pais do Taro**) servem de guardas sem lembrar de ninguém. "
               "O Rei Ossárion espera o herdeiro na sala do trono, com uma mesa posta para sete que ninguém usa há mil anos.",
    "clue_n": 8,
    "clue": "O Rei confirma tudo: o herdeiro foi chamado de 2040 para colocar a coroa e prendê-la de novo. A coroa racha diante dele com o mesmo som de vidro do museu, "
            "e a escolha é do jogador (recusar, ou tentar colocar e ser impedido pelo parceiro).",
    "moment": ["**Portão:** os pais do Taro guardam a porta e não o reconhecem. Parceiro: \"Então eu vou quebrar essa coroa.\" Recorrente: Taro chegou primeiro e espera ali.",
               "**Sala do trono:** o parceiro acende as velas (Lia com coragem; Taro com raiva) para o Rei ver o que perdeu.",
               "**Final:** quando a coroa se quebra, os pais reconhecem o Taro; ele **perdoa** (os pais e o Rei). A Lia acende o farol da Praia nos dois finais.",
               "Arcos fechados: Lia medo → coragem → **luz para os outros**; Taro raiva → entendimento → **perdão**."],
    "guardian": {"name": "Provador Real Degustor e o Rei Ossárion", "kin": "Degustor serve o Rei; Ossárion é o patriarca da família",
                 "personality": "Degustor: guloso e dedicado (prova a comida do Rei todo dia, há mil anos). Rei: solitário, imponente, ferido.",
                 "motive": "O Rei não quer perder a família de novo; a lei \"Ninguém sai, ninguém se perde\" nasceu desse medo.",
                 "mechanic": "**Sequência de chefes:** os pais do Taro no portão, o Provador Real (equipe veneno/defesa/cura) e o Rei (120) com escolta. "
                             "A fonte do Grande Salão cura e marca o ponto de volta; se a cidade de Ossório soube do registro, o **Caliço** está no portão e cura a equipe.",
                 "team": "Pais do Taro: Timonaço 88 e 87 · Provador Real: Degustor 90, Bastião 89, Pergamor 90, Samovarão 89 · Rei Esqueleto 120 + Aguapéu 78.",
                 "reward": "O Rei entra na equipe (idade 100) nos dois finais; créditos; pós-jogo livre."},
    "maps": [("**Portão** (`castelo_portao`)", "Pátio diante da muralha; pais do Taro na porta; Taro (recorrente) e Caliço (se a escolha 4 foi contar)."),
             ("**Grande Salão** (`castelo_salao`)", "Guarda Real Ébano, Arauto Real, Cozinheiro Tempero, selvagens, a fonte (cura e ponto de volta) e o Provador Real diante da porta do trono."),
             ("**Sala do Trono** (`sala_trono`)", "O Rei, a coroa no pedestal, velas acesas pelo parceiro, retratos e a mesa posta para sete."),
             ("**Museu de 2040** (`museu_2040`)", "Epílogo: a vitrine vazia, \"Peça em restauração\" (gancho para o próximo jogo)."),
             ("**Praia (pós-jogo)**", "Farol aceso, Bento e o epílogo; os Guardiões viram **ecos** para revanche nos mesmos lugares.")],
}
R.NPC_DOC = [
    ("Pais do Taro", "chefes do portão", "Fecham o arco do Taro: não o reconhecem até a coroa quebrar"),
    ("Caliço (condicional)", "aliado", "Consequência da escolha 4: cura a equipe no portão"),
    ("Ébano, Arauto, Tempero", "domadores do castelo", "Os últimos capangas, com humor de mil anos de rotina"),
    ("Provador Real Degustor", "chefe", "O guardião do trono; no pós-jogo vira o único Degustor (selvagem, recrutável)"),
    ("Rei Ossárion", "chefe final", "Pede que o herdeiro coloque a coroa; entra na equipe nos dois finais"),
    ("Bento (pós-jogo)", "lore", "Epílogo na Praia e dica dos ecos dos Guardiões"),
]
R.HOUSES = [("—", "O Castelo não tem casas de domadores", "—")]
R.CHOICES = [
    ("A coroa", "Colocar / Recusar", "Colocar: o parceiro impede (\"Se você colocar, nunca mais sai daqui!\"). Os dois caminhos levam à batalha final."),
    ("**Final A — Redimir**", "Carta da Alva + pelo menos 2 de: `red_minas`, `red_pantano`, `red_ossorio`",
     "O Rei lê a carta, quebra a coroa por vontade própria, a família se despede (uma fala de cada Guardião) e ele pede para seguir o herdeiro."),
    ("**Final B — Derrotar**", "Sem os requisitos", "A coroa se parte com o golpe final, a família some sem despedida e o Rei entra na equipe em silêncio (\"Não tenho mais ninguém\")."),
    ("Nos dois finais", "—", "Os pais do Taro o reconhecem; Lia acende o farol; epílogo no museu de 2040 com a vitrine vazia; créditos; pós-jogo."),
    ("Pós-jogo", "—", "Ecos dos 6 Guardiões (revanche, idades 95–100, 3000 moedas), Degustor recrutável no salão, Ossário e casas restantes."),
]


def patch_other_regions():
    """Pós-jogo nas regiões anteriores: farol aceso e Bento na Praia; os
    Guardiões viram ecos (revanche) depois do jogo zerado."""
    p = ROOT / "data/maps/praia_despertar.json"
    m = json.loads(p.read_text())
    props = [x for x in m["props"] if x.get("type") != "lighthouse_lit"]
    for x in props:
        if x.get("type") == "lighthouse":
            x["if_not"] = "game_cleared"
            lit = {"type": "lighthouse_lit", "x": x["x"], "y": x["y"], "dialog": ref("farol_aceso"), "if": "game_cleared"}
    props.append(lit)
    m["props"] = props
    m["npcs"] = [n for n in m["npcs"] if n["id"] != "bento_final"] + [{"id": "bento_final", "x": 12, "y": 17, "facing": "left", "if": "epilogo_visto"}]
    oe = [x for x in m.get("on_enter", []) if x.get("dialog") != ref("epilogo_praia")]
    m["on_enter"] = [{"if": "game_cleared", "if_not": "epilogo_visto", "dialog": ref("epilogo_praia")}] + oe
    p.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    p = ROOT / "data/npcs.json"
    d = json.loads(p.read_text())
    for g, nid in NPC_ID.items():
        n = d["npcs"][nid]
        n["dialog"] = [x for x in n["dialog"] if x.get("dialog") != ref(f"eco_{g}")]
        n["dialog"].insert(0, {"if": "game_cleared", "dialog": ref(f"eco_{g}")})
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    R.write()
    patch_other_regions()
