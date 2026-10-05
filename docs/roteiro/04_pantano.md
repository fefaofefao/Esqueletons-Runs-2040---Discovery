# Roteiro — Ato 3: Rota 3 e Pântano Verde-Musgo

Fase 4d. **Gerado por `tools/maps/pantano.py`**, a mesma fonte que grava os mapas, NPCs e diálogos do jogo, portanto o jogo implementa exatamente o que está aqui. Diálogos em `data/dialogs/pantano.json`.

**Duração alvo:** 25 min. **Idades:** chegada 34–42; selvagens 33–39; domadores 36–43; Guardiã ~48.

## 1. Problema local
Toda noite a **névoa verde** do caldeirão da Guardiã **Musga** desce sobre **Brejo Alto**. Quem respira tosse, e de manhã a vila faz fila na porta dela para buscar o remédio que só ela sabe fazer. Quem sai da vila perde a dose do dia: "Ninguém sai, ninguém se perde" do jeito da Musga. O Rancho e a loja estão sem antídoto (ela compra todos). A névoa também esconde a estrada do norte.

## 2. Pista de 2040 (nº 4)
Antes da luta, a Musga **cheira o ar** e diz: "Você tem cheiro de casa. De família." Os esqueletos da família real sentem os parentes: o protagonista é do sangue do Rei.

## 3. Momento de Lia e Taro
- **Taro** descobre pela fofoca da Musga que os levados (inclusive os pais dele) estão **no castelo**. Parceiro: "Castelo. Eu sabia... Eles tão inteiros." Recorrente (parceira Lia): Lia quer contar a ele; Taro aparece na saída norte, já sabendo, e aceita seguir junto ("Mas eu chego primeiro").
- **Lia** (parceira) vê os vaga-lumes da Rota 3: "acendem um pro outro achar o caminho", o mesmo desejo do farol.
- Arco de Taro: raiva → entendimento começa (os pais estão vivos, servindo, como a família do Rei).

## 4. Guardião: Musga (sobrinha do Rei)
- **Parentesco:** sobrinha
- **Personalidade:** irônica, fofoqueira, solitária; chama todo mundo de "querido" e solta fofocas (o tique dela)
- **Motivo para servir ao Rei:** **Medo** de ser esquecida de novo: da primeira vez morreu sozinha numa torre. "Quem precisa de mim não me esquece."
- **Mecânica-tema:** **Veneno e cura.** A equipe envenena e se cura (Ervaçal, Regalírio). Ensina o **tempo do veneno** (3–5 turnos), o uso de **antídotos** e a bater primeiro em quem cura. Lodo e as Irmãs Taboa dão a dica.
- **Equipe:** Ervaçal 49, Marretão 48, Regalírio 47, Cogumestre 48.
- **Recompensa:** 1300 moedas; a névoa para e a estrada norte (Rota 4) aparece.

## 5. Mapas
| Mapa | Conteúdo |
|---|---|
| **Rota 3** (`rota_3`) | Sai de Brasal (depois da Tia). 3 caminhos: **Trilha das Tábuas** (oeste: Traíra, Caniço, Marreco), **Capinzal** (leste, mais selvagens) e **Passagem do Desmoronamento** (centro: entulho que só some com o **Martelo da Tia**, com um selvagem forte). Placa e o Barqueiro Remanso dão a dica. |
| **Brejo Alto** (`brejo`) | Vila de palafitas: Rancho (Garça, onde acontece a escolha 3), Loja sem antídoto (Junco), casas das Irmãs Taboa e do Bagre, a casa da Vó Neblina (abre se você doar), NPCs, missão do malote e saída oeste para o Caldeirão. |
| **Caldeirão da Musga** (`caldeirao`) | Salão com selvagens, o malote roubado, Boticário Fel, câmara sul (Brumaga, se você doou) e o caldeirão da Musga ao norte. |
| Interiores | Rancho da Garça, Venda do Junco, casas das Irmãs Taboa, do Bagre e da Vó Neblina. |

## 6. NPCs e motivo de existir
| NPC | Função | Por que existe |
|---|---|---|
| Barqueiro Remanso | dica | Explica os 3 caminhos e reconhece o Martelo da Tia |
| Traíra, Caniço, Marreco | domadores da rota | Trilha das Tábuas; Marreco dá antídotos (que podem ir para a doação) |
| Dona Garça | Rancho + escolha 3 | Cura; pede os antídotos para as crianças |
| Seu Junco | Loja | Mostra o problema: a Musga compra todo antídoto |
| Girino | humor | Recorde de fôlego; muda depois da Guardiã |
| Seu Sapé | lore | Conta como a Musga morreu esquecida numa torre |
| Lodo | dica | Ensina o tempo do veneno e a bater em quem cura |
| Dona Pena | missão | Malote roubado: mostra a solidão da Musga ("que fofo" nas cartas) |
| Boticário Fel | capanga | Guarda o caminho até o caldeirão |
| Musga | Guardiã | Veneno e cura; pista 4; fofoca que move o arco do Taro |

## 7. Casas de domadores
| Dono | Tema da equipe | Recompensa |
|---|---|---|
| Irmãs Taboa | Veneno em dobro (Ervaçal + Esporito) | 640 moedas + 2 Antídotos |
| Pescador Bagre | Aguentar e curar (Marretão + Regalírio) | 660 moedas + 2 Poções G |
| Vó Neblina (só se doar) | Névoa: veneno e cura (Ervaçal + Regalírio) | 700 moedas + 2 Reviver; conta onde está a Brumaga |

## 8. Escolhas e consequências
| Escolha | Opções | Consequência |
|---|---|---|
| Caminho da Rota 3 | Tábuas / Capinzal / Desmoronamento | Moedas e itens / XP e marcadores / curto, só com o Martelo da Tia |
| **Escolha 3: os antídotos** | Doar / Guardar | Doar (até 3): as crianças e a Vó Neblina se curam, a casa dela abre (3ª casa de domadores) e a única **Brumaga** aparece no Caldeirão; **+1 Redenção** (`red_pantano`). Guardar: você fica com os itens. |
| Missão do malote | Fazer / ignorar | 1 Reviver + 2 Antídotos (que podem ajudar na doação) |

## 9. Falas (PT-BR, na ordem dos roteiros)

### `pantano/placa_bifurcacao`
- *(narração)* ← Trilha das Tábuas · ↑ Passagem do Desmoronamento · → Capinzal

### `pantano/entulho`
- *(narração)* Entulho de um desmoronamento antigo. Um martelo forte daria conta.

### `pantano/chegada_rota`
- **SPK_LIA:** Vaga-lumes! Olha, eles acendem um pro outro achar o caminho. *(if partner_lia)*
- **SPK_LIA:** Igual farol. Só que pequenininho. *(if partner_lia)*
- **SPK_TARO:** Lama até o joelho. Ótimo. *(if partner_taro)*
- **SPK_TARO:** Se meu pai tivesse aqui, já tinha feito uma ponte. *(if partner_taro)*
- *[flag rota3_vista = True]*

### `pantano/remanso`
- **Barqueiro Remanso:** Esse martelo é da Tia Fornalha? Então a pedra do meio já era! *(if has_martelo_tia)*
- **Barqueiro Remanso:** Três trilhas: na das tábuas tem gente brava, no capim tem bicho, e no meio tem pedra caída.
- **Barqueiro Remanso:** Antes eu levava todo mundo de barco. Agora a névoa não deixa nem o barco sair.

### `pantano/traira`
- **Traíra:** Pesco esqueleto, não peixe. Peixe não revida. Vamos!
- *[batalha tamer: Marretão 36, Ervaçal 36 · 520 moedas]*
- **Traíra:** Escapou do anzol. Dessa vez.

### `pantano/traira_depois`
- **Traíra:** Escapou do anzol. Dessa vez.

### `pantano/canico`
- **Caniço:** Eu tinha uma vara de pescar. Agora tenho um esqueleto que segura a vara pra mim.
- *[batalha tamer: Regalírio 37, Esporito 37 · 540 moedas]*
- **Caniço:** Ele também não pesca nada. Mas é ótima companhia.

### `pantano/canico_depois`
- **Caniço:** Ele também não pesca nada. Mas é ótima companhia.

### `pantano/marreco`
- **Marreco:** Meus patos fugiram da névoa. Meus esqueletos ficaram. Sabe por quê? Lealdade!
- *[batalha tamer: Fumarel 38, Marretão 38 · 570 moedas + 2× antidoto]*
- **Marreco:** Leva esses antídotos. Lá na vila tão precisando mais que eu.

### `pantano/marreco_depois`
- **Marreco:** Leva esses antídotos. Lá na vila tão precisando mais que eu.

### `pantano/placa_brejo`
- *(narração)* Brejo Alto. Casa com perna, gente com fôlego.

### `pantano/placa_caldeirao`
- *(narração)* ← Caldeirão da Musga. Fila do remédio: de manhã.

### `pantano/chegada_brejo`
- **SPK_LIA:** Casas de perna comprida! Será que elas andam quando ninguém tá olhando? *(if partner_lia)*
- **SPK_TARO:** Todo mundo tossindo. Isso não é doença. É alguém fazendo. *(if partner_taro)*
- *[flag brejo_visto = True]*

### `pantano/garca`
- *[ação heal: {}]*
- *[ação respawn: {}]*
- **Dona Garça:** A névoa parou! Agora é só esperar a tosse ir embora sozinha. *(if musga_beaten)*
- **Dona Garça:** A névoa desce toda noite. De manhã, fila na porta da Musga pra buscar o remédio dela. *(if_not musga_beaten)*
- **Dona Garça:** Meu antídoto acabou. As crianças tossem e eu só tenho chá de capim. *(if_not pantano_escolheu)*
- **Dona Garça:** Você carrega antídotos... Doaria alguns pras crianças? Até três já curam a rua inteira. *(if has_antidoto; if_not pantano_escolheu)*
  - (escolha) "Doar antídotos" → `pantano/doar` / "Guardar" → `pantano/guardar`
- **Dona Garça:** Se arranjar antídoto, as crianças agradecem. A Vó Neblina também. *(if_none has_antidoto, pantano_escolheu)*
- *[vai para `pantano/garca_rancho`]*

### `pantano/garca_rancho`
- **Dona Garça:** Quer deixar algum esqueleto descansando? Cama de palafita balança, mas embala.
  - (escolha) "`OPT_P_RANCH`" → `vila_mare/rancho` / "`OPT_P_LEAVE`"

### `pantano/doar`
- *[ação take_item: {"item": "antidoto", "n": 3}]*
- **Dona Garça:** Isso cura a rua das crianças inteirinha. E sobra pra Vó Neblina!
- **Dona Garça:** Ela era domadora das boas. Quando melhorar, vai querer te conhecer.
- *[flag pantano_doou = True]*
- *[flag red_pantano = True]*
- *[flag pantano_escolheu = True]*
- *[vai para `pantano/garca_rancho`]*

### `pantano/guardar`
- **Dona Garça:** Entendo. Estrada longa pede bolso cheio. O chá vai ter que dar conta.
- *[flag pantano_guardou = True]*
- *[flag pantano_escolheu = True]*
- *[vai para `pantano/garca_rancho`]*

### `pantano/junco`
- **Seu Junco:** Antídoto? Acabou faz uma semana. A Musga compra tudo pra ninguém mais ter.
- *[ação shop: {"id": "brejo"}]*
- **Seu Junco:** Poção eu tenho. Remédio de verdade, só ela. Esperta, a moça.

### `pantano/girino`
- **Girino:** Agora eu respiro à vontade! Já tô no recorde de mil segundos. *(if musga_beaten)*
- **Girino:** Eu prendo a respiração quando a névoa desce. Meu recorde é três segundos. *(if_not musga_beaten)*

### `pantano/sape`
- **Seu Sapé:** A Musga é sobrinha do Rei. Dizem que da primeira vez ela se foi sozinha, numa torre que ninguém visitava.
- **Seu Sapé:** Gente esquecida faz cada coisa pra ser lembrada...

### `pantano/lodo`
- **Lodo:** Veneno dura de três a cinco turnos. Antídoto cedo poupa vida; tarde, poupa antídoto.
- **Lodo:** A equipe da Musga se cura enquanto você se envenena. Bate primeiro em quem cura.

### `pantano/pena_pede`
- **Dona Pena:** O capanga da Musga levou meu malote! Ela lê as cartas de todo mundo.
- *[flag pena_quest = True]*
- **Dona Pena:** Fica no Caldeirão, a oeste. Cuidado com o boticário de óculos.

### `pantano/pena_onde`
- **Dona Pena:** Sem malote, sem carta. Sem carta, a vila fica muda.
- **Dona Pena:** Fica no Caldeirão, a oeste. Cuidado com o boticário de óculos.

### `pantano/pena_obrigada`
- **Dona Pena:** Meu malote! E olha só: alguém escreveu "que fofo" em todas as cartas.
- *[ação take_item: {"item": "malote", "n": 1}]*
- **Dona Pena:** Toma, um Reviver e dois antídotos. Carteira paga em dobro quando a carta chega.
- *[ação give_item: {"item": "reviver", "n": 1}]*
- *[ação give_item: {"item": "antidoto", "n": 2}]*
- *[flag pena_done = True]*

### `pantano/pena_depois`
- **Dona Pena:** Hoje entreguei uma carta até pra Musga. Ela chorou. De alegria, eu acho. *(if musga_beaten)*
- **Dona Pena:** Sem malote, sem carta. Sem carta, a vila fica muda. *(if_not musga_beaten)*

### `pantano/malote`
- *(narração)* O malote da Dona Pena. As cartas estão abertas... e anotadas.
- *[ação give_item: {"item": "malote", "n": 1}]*
- *[flag malote_pego = True]*

### `pantano/taboa`
- **Irmãs Taboa:** Uma envenena, a outra também! Treino de antídoto, cortesia da casa.
- *[batalha tamer: Ervaçal 41, Esporito 41 · 640 moedas + 2× antidoto]*
- **Irmãs Taboa:** Veneno em dobro acaba rápido... pra quem tem antídoto.

### `pantano/taboa_depois`
- **Irmãs Taboa:** Veneno em dobro acaba rápido... pra quem tem antídoto.

### `pantano/bagre`
- **Pescador Bagre:** Meu Marretão aguenta pancada e meu Regalírio cura. Quero ver você cansar a gente.
- *[batalha tamer: Marretão 42, Regalírio 41 · 660 moedas + 2× pocao_g]*
- **Pescador Bagre:** Cansou a gente. Peixe grande cansa, sabia?

### `pantano/bagre_depois`
- **Pescador Bagre:** Cansou a gente. Peixe grande cansa, sabia?

### `pantano/neblina`
- **Vó Neblina:** Foi você que mandou os antídotos? Que a névoa nunca te ache, criança.
- **Vó Neblina:** Agradeço do jeito antigo: com uma boa batalha!
- *[batalha tamer: Ervaçal 42, Regalírio 42 · 700 moedas + 2× reviver]*
- **Vó Neblina:** Minha velha Brumaga fugiu pro caldeirão quando a névoa veio. Se ela te achar digno, vai com você.

### `pantano/neblina_depois`
- **Vó Neblina:** Minha velha Brumaga fugiu pro caldeirão quando a névoa veio. Se ela te achar digno, vai com você.

### `pantano/taro_brejo`
- **SPK_TARO:** Eu ouvi a bruxa da névoa. Castelo. Meus pais tão no castelo.
- **SPK_TARO:** Não faz essa cara. Eu já sabia que era longe.
- **SPK_LIA:** Taro! A gente vai junto até lá, tá? Ninguém se perde se for junto.
- **SPK_TARO:** ...Tá. Mas eu chego primeiro.
- *[flag taro_brejo_visto = True]*
- *[ação hide_npc: {"id": "taro_brejo"}]*

### `pantano/chegada_caldeirao`
- **SPK_LIA:** Cheira a sopa estragada... e a alguém muito sozinho. *(if partner_lia)*
- **SPK_TARO:** Ela tá aí. Dá pra ouvir ela cantando com a panela. *(if partner_taro)*
- *[flag caldeirao_visto = True]*

### `pantano/fel`
- **Boticário Fel:** Receita da Musga: uma pitada de névoa, duas de segredo, e nenhum intruso.
- *[batalha tamer: Ervaçal 43, Fumarel 43 · 600 moedas]*
- **Boticário Fel:** Errei a dose. Pode passar, mas não conta pra ela.

### `pantano/fel_depois`
- **Boticário Fel:** Errei a dose. Pode passar, mas não conta pra ela.

### `pantano/brumaga`
- *(narração)* Uma névoa com olhos se enrola nos juncos. Ela te encara... curiosa.
  - (escolha) "Enfrentar a névoa" → `pantano/brumaga_luta` / "`OPT_M_LEAVE`"

### `pantano/brumaga_luta`
- *[batalha wild: Brumaga 41]*

### `pantano/musga`
- **Musga:** Visita! Ninguém me visita, querido. Só vêm buscar remédio e vão embora.
- **Musga:** Snif, snif... Que estranho. Você tem cheiro de casa. De família.
- *[flag pista_4 = True]*
- **Musga:** Sabia que a névoa é minha? Quem respira, precisa de mim. Quem precisa, não esquece.
- *[batalha boss: Ervaçal 49, Marretão 48, Regalírio 47, Cogumestre 48 · 1300 moedas]*
- **Musga:** Ai, que deselegante. Ganhar de uma dama no próprio caldeirão.
- **Musga:** Da primeira vez, a família me esqueceu numa torre. Mil anos de silêncio. De novo, não, querido.
- **Musga:** Quer uma fofoca de graça? Os levados, mineiros e pescadores, foram todos pro castelo servir o titio.
- **Musga:** Os pais daquele baixinho do remo também. Sabia? Eu sei de tudo, querido.
- **SPK_TARO:** Castelo. Eu sabia. *(if partner_taro)*
- **SPK_TARO:** ...Eles tão inteiros. É isso que importa. Vamos. *(if partner_taro)*
- **SPK_LIA:** Os pais do Taro! A gente precisa contar pra ele! *(if partner_lia)*
- **Musga:** Tá bom, tá bom. Desligo a névoa. Mas alguém vai ter que vir me visitar. Combinado?
- **Musga:** A Tia mandou eu comer direito? Ela manda isso há mil anos. Fofa. *(if_any minas_quebrou, minas_negociou)*
- *[ação refresh_map: {}]*

### `pantano/musga_depois`
- **Musga:** Volta pra fofocar, querido. Sabia que o primo Caliço ensaia discurso no espelho?

## 10. Contagem
Cerca de **838 palavras** de texto de jogo em PT-BR nesta região.
