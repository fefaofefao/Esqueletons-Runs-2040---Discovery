#!/usr/bin/env python3
"""Falas do Prólogo (docs/roteiro/01_prologo.md) em PT-BR/EN/ES e os roteiros
(data/dialogs/prologo.json e vila_mare.json), com as ações de roteiro.
Rodar de novo regenera a seção do Prólogo em i18n/dialogue.csv."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

T = {
    # falantes
    "SPK_BENTO": ("Bento", "Bento", "Bento"),
    "SPK_LIA": ("Lia", "Lia", "Lia"),
    "SPK_TARO": ("Taro", "Taro", "Taro"),
    "SPK_MAROLA": ("Marola", "Marola", "Marola"),
    "SPK_ANZOL": ("Anzol", "Hook", "Anzuelo"),
    "SPK_PIPA": ("Pipa", "Kite", "Cometa"),
    "SPK_CASCALHO": ("Prof. Cascalho", "Prof. Gravel", "Prof. Guijarro"),
    "SPK_JUREMA": ("Jurema", "Jurema", "Jurema"),
    "SPK_BRAS": ("Fiscal Brás", "Inspector Brás", "Inspector Brás"),
    "SPK_REMO": ("Seu Remo", "Mr. Oar", "Don Remo"),
    "SPK_CONCHA": ("Vó Concha", "Granny Shell", "Abuela Concha"),
    # despertar
    "DLG_P_WAKE_1": ("Areia fria. Gaivotas. Você não lembra como chegou aqui.",
                     "Cold sand. Seagulls. You don't remember how you got here.",
                     "Arena fría. Gaviotas. No recuerdas cómo llegaste aquí."),
    "DLG_P_WAKE_2": ("No bolso, um papel amassado: \"Museu do Litoral — O Reino Perdido de Ossório — 12/10/2040.\"",
                     "In your pocket, a crumpled paper: \"Coast Museum — The Lost Kingdom of Ossório — 10/12/2040.\"",
                     "En el bolsillo, un papel arrugado: \"Museo del Litoral — El Reino Perdido de Ossório — 12/10/2040.\""),
    # Bento
    "DLG_P_BENTO_1": ("Opa! Achei que era um tronco que a maré trouxe. Você tá inteiro?",
                      "Whoa! I thought you were driftwood. You in one piece?",
                      "¡Epa! Creí que eras un tronco que trajo la marea. ¿Estás entero?"),
    "DLG_P_BENTO_2": ("Eu sou o Bento. Pesco aqui desde que o mar era raso.",
                      "I'm Bento. Been fishing here since the sea was shallow.",
                      "Soy Bento. Pesco aquí desde que el mar era bajito."),
    "DLG_P_BENTO_3": ("Cuidado por aí. O continente é dos esqueletos agora. Quem manda neles é o Rei Esqueleto, lá do castelo.",
                      "Watch yourself. The continent belongs to skeletons now. The Skeleton King rules them from his castle.",
                      "Ten cuidado. El continente es de los esqueletos ahora. Los manda el Rey Esqueleto, desde su castillo."),
    "OPT_P_KING": ("Rei Esqueleto?", "Skeleton King?", "¿Rey Esqueleto?"),
    "OPT_P_PAPER": ("E esse papel?", "And this paper?", "¿Y este papel?"),
    "DLG_P_BENTO_KING": ("Ninguém vê o Rei faz tempo. Mas a lei dele todo mundo conhece: \"Ninguém sai, ninguém se perde.\"",
                         "Nobody's seen the King in ages. But everyone knows his law: \"No one leaves, no one gets lost.\"",
                         "Nadie ve al Rey hace tiempo. Pero todos conocen su ley: \"Nadie sale, nadie se pierde.\""),
    "DLG_P_BENTO_PAPER": ("\"Museu\"? Nunca ouvi falar. Parece nome de peixe. Guarda isso aí, vai que é importante.",
                          "\"Museum\"? Never heard of it. Sounds like a fish. Keep it, just in case it matters.",
                          "¿\"Museo\"? Nunca lo oí. Suena a nombre de pez. Guárdalo, por si es importante."),
    "DLG_P_BENTO_4": ("Vem pra cabana, {player}. Gente sozinha na praia vira janta de gaivota.",
                      "Come to my hut, {player}. Folks alone on the beach end up as seagull dinner.",
                      "Ven a la cabaña, {player}. Quien anda solo en la playa termina de cena de gaviota."),
    "DLG_P_BENTO_HUT": ("A cabana é ali, ó. A porta range, mas é boa gente.",
                        "The hut's right there. The door creaks, but it means well.",
                        "La cabaña está ahí. La puerta cruje, pero es buena gente."),
    "DLG_P_BENTO_LATER": ("A vila fica pro norte. Fala com a Marola no Rancho se o time cansar.",
                          "The village is up north. Talk to Marola at the Ranch if your team gets tired.",
                          "La villa está al norte. Habla con Marola en el Rancho si tu equipo se cansa."),
    # cabana
    "DLG_P_KNOCK": ("Toc, toc. Duas cabecinhas de osso espiam pela porta.",
                    "Knock, knock. Two little bony heads peek through the door.",
                    "Toc, toc. Dos cabecitas de hueso se asoman por la puerta."),
    "DLG_P_BENTO_KIDS": ("Ah, os pequenos. Despertaram faz poucos dias. Ainda tão procurando alguém.",
                         "Ah, the little ones. They woke up a few days ago. Still looking for someone.",
                         "Ah, los pequeños. Despertaron hace pocos días. Todavía buscan a alguien."),
    "DLG_P_LIA_1": ("Oi! Eu sou a Lia. Acordei sozinha, no escuro. Agora eu não largo minha lamparina.",
                    "Hi! I'm Lia. I woke up alone, in the dark. Now I never let go of my lamp.",
                    "¡Hola! Soy Lia. Desperté sola, a oscuras. Ahora no suelto mi lamparita."),
    "DLG_P_LIA_2": ("Um dia eu vou acender o farol velho da praia. Aí ninguém mais se perde no mar!",
                    "Someday I'll light the old lighthouse on the beach. Then no one will get lost at sea!",
                    "¡Un día voy a encender el faro viejo de la playa! Así nadie más se pierde en el mar."),
    "DLG_P_TARO_1": ("Taro. Levaram meus pais pro castelo. Eu vou buscar.",
                     "Taro. They took my parents to the castle. I'm getting them back.",
                     "Taro. Se llevaron a mis padres al castillo. Voy a buscarlos."),
    "DLG_P_TARO_2": ("Se você for pro norte, eu vou junto. Se não for, vou sozinho mesmo.",
                     "If you're heading north, I'm coming. If not, I'll go alone.",
                     "Si vas al norte, voy contigo. Si no, voy solo."),
    "DLG_P_CHOOSE": ("Esqueleto sozinho não vai longe. Gente sozinha, menos ainda. Leva os dois, {player}.",
                     "A skeleton alone won't get far. A person alone, even less. Take them both, {player}.",
                     "Un esqueleto solo no llega lejos. Una persona sola, menos aún. Llévate a los dos, {player}."),
    "DLG_P_LIA_YES": ("Sério?! Eu vou iluminar o caminho, prometo!", "Really?! I'll light the way, I promise!", "¡¿En serio?! ¡Voy a iluminar el camino, lo prometo!"),
    "DLG_P_TARO_YES": ("...Valeu. Não fica pra trás.", "...Thanks. Don't fall behind.", "...Gracias. No te quedes atrás."),
    "DLG_P_DUO_LIA": ("Eu ilumino, você corre, Taro. Combinado?", "I'll light the way, you run, Taro. Deal?", "Yo ilumino y tú corres, Taro. ¿Trato?"),
    "DLG_P_DUO_TARO": ("Tá. Mas eu vou na frente.", "Fine. But I'm going first.", "Vale. Pero yo voy delante."),
    "DLG_P_POTIONS": ("Toma três poções. Esqueleto também rala o joelho.", "Take three potions. Skeletons scrape their knees too.", "Toma tres pociones. Los esqueletos también se raspan las rodillas."),
    "DLG_P_WILD": ("Na praia tem esqueleto selvagem. Encosta num, que ele vem brigar. Treina um pouco antes da vila.",
                   "There are wild skeletons on the beach. Bump into one and it'll fight. Train a bit before the village.",
                   "En la playa hay esqueletos salvajes. Choca con uno y vendrá a pelear. Entrena antes de ir a la villa."),
    # marcador (depois da 1ª vitória)
    "DLG_P_MARK_1": ("Viu aquela barrinha de ossos? É o marcador. Cada vitória sobre uma espécie enche um pouco.",
                     "See that little bone bar? That's the marker. Every win over a species fills it a bit.",
                     "¿Viste esa barrita de huesos? Es el marcador. Cada victoria sobre una especie lo llena un poco."),
    "DLG_P_MARK_2": ("Quando enche, o esqueleto pede pra ir com você. Ninguém é obrigado: é amizade, não ordem.",
                     "When it's full, the skeleton asks to come with you. Nobody's forced: it's friendship, not orders.",
                     "Cuando se llena, el esqueleto pide ir contigo. Nadie está obligado: es amistad, no una orden."),
    # placas e objetos
    "SIGN_VILA_ENTRANCE": ("Vila Maré. Peixe fresco, quando o mar deixa.", "Tidemark Village. Fresh fish, when the sea allows.", "Villa Marea. Pescado fresco, cuando el mar deja."),
    "SIGN_VILA_RANCH": ("Rancho da Marola. Cura grátis e cama pra esqueleto.", "Marola's Ranch. Free healing and beds for skeletons.", "Rancho de Marola. Curación gratis y camas para esqueletos."),
    "SIGN_VILA_SHOP": ("Armazém do Anzol. Fiado só pra quem pesca.", "Hook's General Store. Credit only for those who fish.", "Almacén Anzuelo. Fiado solo para quien pesca."),
    "SIGN_VILA_DOCK": ("Cais fechado por ordem do Rei. — Fiscal Brás", "Dock closed by order of the King. — Inspector Brás", "Muelle cerrado por orden del Rey. — Inspector Brás"),
    "SIGN_VILA_NORTH": ("Estrada do Bosque das Raízes.", "Road to the Rootwood Forest.", "Camino al Bosque de las Raíces."),
    "OBJ_VILA_WELL": ("O poço tem eco. Você ouve a própria voz chegar atrasada.", "The well echoes. Your own voice comes back late.", "El pozo tiene eco. Tu propia voz vuelve con retraso."),
    "OBJ_LIGHTHOUSE": ("O farol velho. A lente está apagada e coberta de sal.", "The old lighthouse. Its lens is dark and crusted with salt.", "El faro viejo. La lente está apagada y cubierta de sal."),
    "OBJ_NET_FREED": ("Você soltou a rede da Jurema.", "You freed Jurema's net.", "Soltaste la red de Jurema."),
    # Marola
    "DLG_P_MAROLA_1": ("Tá todo mundo cansado? Deita aí, que eu cuido.", "Everyone tired? Lie down, I'll take care of you.", "¿Todos cansados? Acuéstense, que yo los cuido."),
    "DLG_P_MAROLA_2": ("Esqueleto também tem aniversário, sabia? Cada ano que passa, eles crescem um pouco.",
                       "Skeletons have birthdays too, you know. Every year that passes, they grow a little.",
                       "Los esqueletos también cumplen años, ¿sabías? Cada año que pasa, crecen un poco."),
    "OPT_P_RANCH": ("Ver o Rancho", "Open the Ranch", "Ver el Rancho"),
    "OPT_P_LEAVE": ("Tchau", "Bye", "Adiós"),
    # Anzol
    "DLG_P_ANZOL_1": ("Bem-vindo ao Anzol! Se não tiver, eu invento. Se inventar, eu cobro.",
                      "Welcome to Hook's! If I don't have it, I'll invent it. If I invent it, I'll charge for it.",
                      "¡Bienvenido a Anzuelo! Si no lo tengo, lo invento. Si lo invento, lo cobro."),
    "DLG_P_ANZOL_2": ("Volte sempre! Ou pelo menos volte com moedas.", "Come again! Or at least come back with coins.", "¡Vuelve pronto! O al menos vuelve con monedas."),
    # Pipa
    "DLG_P_PIPA_1": ("Meu esqueleto é rapidinho! Ele usa golpe leve e bate de novo antes do outro acordar.",
                     "My skeleton is super quick! It uses light moves and hits again before the other one wakes up.",
                     "¡Mi esqueleto es rapidísimo! Usa golpes ligeros y pega otra vez antes de que el otro despierte."),
    "DLG_P_PIPA_2": ("Golpe pesado é bom pra quem é lento. Aí pelo menos dói.", "Heavy moves are for slowpokes. At least they hurt.", "Los golpes pesados son para los lentos. Al menos duelen."),
    # Cascalho
    "DLG_P_CASCALHO_1": ("Os esqueletos não são mortos tristes, jovem. É uma segunda vida: nascem bebês e envelhecem de novo.",
                         "Skeletons aren't sad dead folk, young one. It's a second life: they're born as babies and grow old again.",
                         "Los esqueletos no son muertos tristes, joven. Es una segunda vida: nacen bebés y envejecen de nuevo."),
    "DLG_P_CASCALHO_2": ("Antes, faziam aniversário em paz. Agora obedecem a uma coroa que ninguém vê.",
                         "They used to celebrate birthdays in peace. Now they obey a crown no one has seen.",
                         "Antes cumplían años en paz. Ahora obedecen a una corona que nadie ve."),
    # Jurema
    "DLG_P_JUREMA_ASK": ("Minha rede ficou presa nas pedras da praia, perto dos esqueletos bravos. Você pega pra mim?",
                         "My net got stuck on the rocks down at the beach, near the grumpy skeletons. Could you get it?",
                         "Mi red quedó atrapada en las rocas de la playa, cerca de los esqueletos bravos. ¿Me la traes?"),
    "DLG_P_JUREMA_WHERE": ("Pedras do leste da praia. Cuidado com os espinhudos!", "The rocks on the east side of the beach. Watch out for the spiky ones!", "Las rocas del este de la playa. ¡Cuidado con los espinosos!"),
    "DLG_P_JUREMA_THANKS": ("Minha rede! Toma, duas poções e um antídoto. Pescador paga em dobro quando tá feliz.",
                            "My net! Here, two potions and an antidote. A happy fisher pays double.",
                            "¡Mi red! Toma, dos pociones y un antídoto. Un pescador feliz paga el doble."),
    "DLG_P_JUREMA_AFTER": ("Quando o cais abrir, o primeiro peixe é seu.", "When the dock opens, the first fish is yours.", "Cuando abra el muelle, el primer pescado es tuyo."),
    # Brás
    "BTL_TAMER_BRAS": ("Fiscal Brás", "Inspector Brás", "Inspector Brás"),
    "DLG_P_BRAS_1": ("Alto lá! Ordem do Rei: ninguém sai, ninguém se perde. Nem barco, nem peixe, nem você.",
                     "Halt! King's orders: no one leaves, no one gets lost. Not boats, not fish, not you.",
                     "¡Alto ahí! Orden del Rey: nadie sale, nadie se pierde. Ni barcos, ni peces, ni tú."),
    "DLG_P_BRAS_WIN": ("Tá bom, tá bom! O cais tá aberto. Mas o Ramalho não vai gostar nada disso.",
                       "Okay, okay! The dock's open. But Ramalho won't like this one bit.",
                       "¡Vale, vale! El muelle está abierto. Pero a Ramalho no le va a gustar nada."),
    "DLG_P_BRAS_AFTER": ("O Ramalho é primo do Rei. Lá no Bosque ele te ensina a esperar.",
                         "Ramalho is the King's cousin. Out in the forest, he'll teach you how to wait.",
                         "Ramalho es primo del Rey. En el bosque te va a enseñar a esperar."),
    # Seu Remo
    "BTL_TAMER_REMO": ("Seu Remo", "Mr. Oar", "Don Remo"),
    "DLG_P_REMO_1": ("Aqui em casa todo mundo é rápido. Até a sopa esfria correndo.", "Everyone in this house is fast. Even the soup cools off in a hurry.", "En esta casa todos son rápidos. Hasta la sopa se enfría corriendo."),
    "DLG_P_REMO_AFTER": ("Rápido não é tudo. Mas ajuda a chegar primeiro na mesa.", "Speed isn't everything. But it gets you to the table first.", "La rapidez no lo es todo. Pero ayuda a llegar primero a la mesa."),
    # Vó Concha
    "BTL_TAMER_CONCHA": ("Vó Concha", "Granny Shell", "Abuela Concha"),
    "DLG_P_CONCHA_1": ("Meus netinhos jogam juntos. Um cura, o outro bate. Família é isso.", "My little grandkids play together. One heals, the other hits. That's family.", "Mis nietecitos juegan juntos. Uno cura, el otro pega. Eso es familia."),
    "DLG_P_CONCHA_AFTER": ("Volta pra comer bolo. Aniversário de esqueleto é toda semana aqui.", "Come back for cake. There's a skeleton birthday here every week.", "Vuelve a comer pastel. Aquí hay cumpleaños de esqueleto cada semana."),
    "OPT_P_FIGHT": ("Lutar", "Battle", "Pelear"),
    "OPT_P_NOT_NOW": ("Agora não", "Not now", "Ahora no"),
    # recorrente
    "BTL_TAMER_LIA": ("Lia", "Lia", "Lia"),
    "BTL_TAMER_TARO": ("Taro", "Taro", "Taro"),
    "DLG_P_RIVAL_TARO": ("Você demorou. Vamos ver se essa luz aguenta um soco.", "You took your time. Let's see if that light can take a punch.", "Tardaste. A ver si esa luz aguanta un golpe."),
    "DLG_P_RIVAL_LIA": ("Antes de ir: deixa eu ver se você me acha no escuro!", "Before you go: let's see if you can find me in the dark!", "Antes de irte: ¡a ver si me encuentras en la oscuridad!"),
    "DLG_P_RIVAL_BYE": ("A gente se vê no Bosque. Não se perde, hein!", "See you in the forest. Don't get lost, okay!", "Nos vemos en el bosque. ¡No te pierdas, eh!"),
    "DLG_P_RIVAL_LATER": ("Tá bom. Mas eu vou estar te esperando!", "Fine. But I'll be waiting for you!", "Vale. ¡Pero te voy a estar esperando!"),
    "MSG_ROUTE1_LOCKED": ("A estrada do Bosque abre na próxima atualização (fase 4b).", "The road to the forest opens in the next update (phase 4b).", "El camino al bosque se abre en la próxima actualización (fase 4b)."),
    "MSG_DOCK_BLOCKED": ("O Fiscal Brás está bloqueando a estrada.", "Inspector Brás is blocking the road.", "El Inspector Brás está bloqueando el camino."),
}


def say(key, spk=None):
    n = {"say": key}
    if spk:
        n["speaker"] = spk
    return n


P = {
    "despertar": [say("DLG_P_WAKE_1"), say("DLG_P_WAKE_2"), {"action": "give_item", "item": "ingresso", "n": 1}, {"set_flag": "intro_done"}],
    "bento_primeira": [say("DLG_P_BENTO_1", "SPK_BENTO"), say("DLG_P_BENTO_2", "SPK_BENTO"),
                       {"say": "DLG_P_BENTO_3", "speaker": "SPK_BENTO",
                        "choice": [{"text": "OPT_P_KING", "goto": "prologo/bento_rei"}, {"text": "OPT_P_PAPER", "goto": "prologo/bento_papel"}]}],
    "bento_rei": [say("DLG_P_BENTO_KING", "SPK_BENTO"), {"goto": "prologo/bento_convite"}],
    "bento_papel": [say("DLG_P_BENTO_PAPER", "SPK_BENTO"), {"goto": "prologo/bento_convite"}],
    "bento_convite": [{"set_flag": "bento_met"}, say("DLG_P_BENTO_4", "SPK_BENTO")],
    "bento_repete": [say("DLG_P_BENTO_HUT", "SPK_BENTO")],
    "bento_depois": [say("DLG_P_BENTO_LATER", "SPK_BENTO")],
    "escolha": [say("DLG_P_KNOCK"), say("DLG_P_BENTO_KIDS", "SPK_BENTO"),
                say("DLG_P_LIA_1", "SPK_LIA"), say("DLG_P_LIA_2", "SPK_LIA"),
                say("DLG_P_TARO_1", "SPK_TARO"), say("DLG_P_TARO_2", "SPK_TARO"),
                say("DLG_P_CHOOSE", "SPK_BENTO"),
                say("DLG_P_LIA_YES", "SPK_LIA"), say("DLG_P_TARO_YES", "SPK_TARO"),
                {"action": "give_partner", "species": "faroleira_1", "age": 5, "nickname": "Lia", "flag": "partner_lia"},
                {"action": "give_partner", "species": "grumete_1", "age": 5, "nickname": "Taro", "flag": "partner_taro"},
                say("DLG_P_DUO_LIA", "SPK_LIA"), say("DLG_P_DUO_TARO", "SPK_TARO"),
                {"goto": "prologo/depois_escolha"}],
    "depois_escolha": [{"set_flag": "has_partner"}, {"action": "hide_npc", "id": "lia_cabana"}, {"action": "hide_npc", "id": "taro_cabana"},
                       say("DLG_P_POTIONS", "SPK_BENTO"), {"action": "give_item", "item": "pocao_p", "n": 3},
                       say("DLG_P_WILD", "SPK_BENTO")],
    "marcador": [say("DLG_P_MARK_1", "SPK_BENTO"), say("DLG_P_MARK_2", "SPK_BENTO"), say("DLG_P_BENTO_LATER", "SPK_BENTO")],
    "farol": [say("OBJ_LIGHTHOUSE")],
    "rede": [say("OBJ_NET_FREED"), {"set_flag": "jurema_net"}],
    "cama_bento": [say("OBJ_BENTO_BED")],
    "estante_bento": [say("OBJ_BENTO_SHELF")],
    "varas_bento": [say("OBJ_BENTO_RODS")],
}

V = {
    "placa_entrada": [say("SIGN_VILA_ENTRANCE")],
    "placa_rancho": [say("SIGN_VILA_RANCH")],
    "placa_loja": [say("SIGN_VILA_SHOP")],
    "placa_cais": [say("SIGN_VILA_DOCK")],
    "placa_norte": [say("SIGN_VILA_NORTH")],
    "poco": [say("OBJ_VILA_WELL")],
    "marola": [{"action": "heal"}, {"action": "respawn"}, say("DLG_P_MAROLA_1", "SPK_MAROLA"),
               {"say": "DLG_P_MAROLA_2", "speaker": "SPK_MAROLA",
                "choice": [{"text": "OPT_P_RANCH", "goto": "vila_mare/rancho"}, {"text": "OPT_P_LEAVE"}]}],
    "rancho": [{"action": "ranch"}],
    "anzol": [say("DLG_P_ANZOL_1", "SPK_ANZOL"), {"action": "shop", "id": "vila_mare"}, say("DLG_P_ANZOL_2", "SPK_ANZOL")],
    "pipa": [say("DLG_P_PIPA_1", "SPK_PIPA"), say("DLG_P_PIPA_2", "SPK_PIPA")],
    "cascalho": [say("DLG_P_CASCALHO_1", "SPK_CASCALHO"), say("DLG_P_CASCALHO_2", "SPK_CASCALHO")],
    "jurema_pede": [say("DLG_P_JUREMA_ASK", "SPK_JUREMA"), {"set_flag": "jurema_quest"}, say("DLG_P_JUREMA_WHERE", "SPK_JUREMA")],
    "jurema_onde": [say("DLG_P_JUREMA_WHERE", "SPK_JUREMA")],
    "jurema_obrigada": [say("DLG_P_JUREMA_THANKS", "SPK_JUREMA"), {"action": "give_item", "item": "pocao_p", "n": 2},
                        {"action": "give_item", "item": "antidoto", "n": 1}, {"set_flag": "jurema_done"}],
    "jurema_depois": [say("DLG_P_JUREMA_AFTER", "SPK_JUREMA")],
    "bras": [say("DLG_P_BRAS_1", "SPK_BRAS"),
             {"action": "battle", "kind": "tamer", "tamer_key": "BTL_TAMER_BRAS", "enemies": [["marisqueiro_1", 6], ["lenhador_1", 7]],
              "reward": 150, "win_flag": "bras_beaten"},
             say("DLG_P_BRAS_WIN", "SPK_BRAS"), {"action": "hide_npc", "id": "bras"}],
    "bras_depois": [say("DLG_P_BRAS_AFTER", "SPK_BRAS")],
    "remo": [say("DLG_P_REMO_1", "SPK_REMO"),
             {"action": "battle", "kind": "tamer", "tamer_key": "BTL_TAMER_REMO", "enemies": [["grumete_1", 6], ["rendeira_1", 6]],
              "reward": 200, "items": [["pocao_p", 2]], "win_flag": "remo_beaten"},
             say("DLG_P_REMO_AFTER", "SPK_REMO")],
    "remo_depois": [say("DLG_P_REMO_AFTER", "SPK_REMO")],
    "concha": [say("DLG_P_CONCHA_1", "SPK_CONCHA"),
               {"action": "battle", "kind": "tamer", "tamer_key": "BTL_TAMER_CONCHA", "enemies": [["rendeira_1", 7], ["marisqueiro_1", 7]],
                "reward": 150, "items": [["reviver", 1]], "win_flag": "concha_beaten"},
               say("DLG_P_CONCHA_AFTER", "SPK_CONCHA")],
    "concha_depois": [say("DLG_P_CONCHA_AFTER", "SPK_CONCHA")],
    "rival_taro": [{"say": "DLG_P_RIVAL_TARO", "speaker": "SPK_TARO",
                    "choice": [{"text": "OPT_P_FIGHT", "goto": "vila_mare/rival_taro_luta"}, {"text": "OPT_P_NOT_NOW", "goto": "vila_mare/rival_depois_taro"}]}],
    "rival_taro_luta": [{"action": "battle", "kind": "tamer", "tamer_key": "BTL_TAMER_TARO", "enemies": [["grumete_1", 7]],
                         "reward": 100, "win_flag": "rival_vila_done", "marker": {"species": "grumete_1", "amount": 10}},
                        say("DLG_P_RIVAL_BYE", "SPK_TARO"), {"action": "hide_npc", "id": "rival_taro"}],
    "rival_depois_taro": [say("DLG_P_RIVAL_LATER", "SPK_TARO")],
    "rival_lia": [{"say": "DLG_P_RIVAL_LIA", "speaker": "SPK_LIA",
                   "choice": [{"text": "OPT_P_FIGHT", "goto": "vila_mare/rival_lia_luta"}, {"text": "OPT_P_NOT_NOW", "goto": "vila_mare/rival_depois_lia"}]}],
    "rival_lia_luta": [{"action": "battle", "kind": "tamer", "tamer_key": "BTL_TAMER_LIA", "enemies": [["faroleira_1", 7]],
                        "reward": 100, "win_flag": "rival_vila_done", "marker": {"species": "faroleira_1", "amount": 10}},
                       say("DLG_P_RIVAL_BYE", "SPK_LIA"), {"action": "hide_npc", "id": "rival_lia"}],
    "rival_depois_lia": [say("DLG_P_RIVAL_LATER", "SPK_LIA")],
}


def main():
    (ROOT / "data/dialogs/prologo.json").write_text(json.dumps({"_comment": "Gerado por tools/maps/prologo_text.py a partir de docs/roteiro/01_prologo.md.", "dialogs": P}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (ROOT / "data/dialogs/vila_mare.json").write_text(json.dumps({"_comment": "Gerado por tools/maps/prologo_text.py a partir de docs/roteiro/01_prologo.md.", "dialogs": V}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    path = ROOT / "i18n/dialogue.csv"
    rows = list(csv.reader(open(path, encoding="utf-8")))
    header, body = rows[0], rows[1:]
    obsolete = {"DLG_BENTO_01", "DLG_BENTO_02", "DLG_BENTO_03", "DLG_BENTO_04", "DLG_BENTO_05", "DLG_BENTO_06", "DLG_BENTO_07",
                "OPT_BENTO_ASK_KING", "OPT_BENTO_THANKS", "DLG_BENTO_KING_01", "DLG_BENTO_R1", "DLG_BENTO_R2", "SIGN_VILA_MARE",
                "OPT_P_LIA", "OPT_P_TARO", "DLG_P_TARO_BYE", "DLG_P_LIA_BYE"}
    body = [r for r in body if r and r[0] not in T and r[0] not in obsolete]
    body += [[k, *v] for k, v in T.items()]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(body)
    words = sum(len(v[0].split()) for k, v in T.items() if not k.startswith(("SPK_", "BTL_TAMER_", "MSG_")))
    print(f"prólogo: {len(T)} textos, ~{words} palavras PT-BR")


if __name__ == "__main__":
    main()
