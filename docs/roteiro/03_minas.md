# Roteiro — Ato 2: Rota 2 e Minas de Cinzas

Fase 4c. **Gerado por `tools/maps/minas.py`**, a mesma fonte que grava os mapas, NPCs e diálogos do jogo, portanto o jogo implementa exatamente o que está aqui. Diálogos em `data/dialogs/minas.json`.

**Duração alvo:** 25 min. **Idades:** chegada 22–30; selvagens 21–27; domadores 24–31; Guardiã ~34.

## 1. Problema local
**Brasal** vivia das minas. A Guardiã **Tia Fornalha** prendeu os esqueletos mineiros à forja com a **corrente mestra**: eles martelam dia e noite as correntes que fecham as estradas do continente ("Ninguém sai, ninguém se perde"). Os mineiros humanos foram expulsos, não há minério, e a fumaça cobre a cidade de cinza. A estrada do norte, para o Pântano, está fechada por correntes até a Tia perder.

## 2. Pista de 2040 (nº 3)
Na casa do **Seu Carvão** há um **mapa antigo** da costa: três baías lado a lado e um farol na do meio. O protagonista reconhece as baías da própria cidade em 2040, com outros nomes. (Mesmo lugar, mil anos antes.)

## 3. Momento de Lia e Taro
- **Taro** acha o **lenço da mãe** preso numa viga da Mina Funda (câmara sul). Parceiro: ele segura o choro e pede para irem mais rápido. Recorrente (parceira Lia): Taro já está lá, conta que os levados passaram pela mina rumo ao norte; Lia promete ajudar a procurar.
- Lia e Taro estão os dois na equipe (decisão do Fernando): tocam as falas de parceiro dos dois; as cenas de "recorrente" só aparecem em saves antigos, com um parceiro só.
- Arco de Taro: raiva → primeiro sinal de esperança ("ela tá inteira").

## 4. Guardião: Tia Fornalha (tia do Rei)
- **Parentesco:** tia; cuidou do Rei quando ele era menino
- **Personalidade:** severa, justa, sem paciência; fala em "regras" numeradas (o tique dela)
- **Motivo para servir ao Rei:** **Dever**: acredita que a ordem do Rei mantém todos seguros. Enquanto houver corrente, a família não vai embora.
- **Mecânica-tema:** **Defesa.** A equipe sobe DEF (Picaréu, Bigornel) e aguenta muito. Ensina a baixar atributos e a usar golpes **Mágicos** (contra RES) em quem tem DEF alta. Fagulha e o Mestre Bigorna dão a dica antes.
- **Equipe:** Picaréu 34, Bigornel 33, Fumarel 35, Bilheiro 34 (os capangas usam Picaréu/Bigornel em versão menor).
- **Recompensa:** 1000 moedas; a estrada do norte abre; e a **escolha 2**.

## 5. Mapas
| Mapa | Conteúdo |
|---|---|
| **Rota 2** (`rota_2`) | Sai de Raizal (exige a vitória sobre Ramalho; o Vigia confere a Lasca de Raiz). 3 caminhos: **Domadores** (oeste: Graxa, Brita, Fuligem), **Selvagem** (leste, Campo de Cascalho com lama e mais esqueletos) e **Atalho** (Galeria Velha, central, curta, com um selvagem forte). Placa e Seu Seixo dão a dica. |
| **Brasal** (`brasal`) | Cidade mineira: Rancho, Loja (Poção G; preço muda com a escolha 2), 2 casas de domadores, a casa do Carvão (missão + pista), NPCs, saída oeste para a Mina Funda e saída norte acorrentada. |
| **Mina Funda** (`mina_funda`) | Salão com selvagens, Capataz Bloqueio, câmara sul (lenço de Taro, capacete da missão, Vagonauta se a corrente for quebrada) e a forja da Tia ao norte. |
| Interiores | Rancho da Rubi, Armazém do Cobre, Oficina do Bigorna, Casa da Ágata, Casa do Carvão. |

## 6. NPCs e motivo de existir
| NPC | Função | Por que existe |
|---|---|---|
| Vigia da Trilha | dica/porteiro | Liga o Bosque às Minas: confere a Lasca de Raiz |
| Seu Seixo | dica | Explica os 3 caminhos e avisa do selvagem forte da Galeria |
| Graxa, Brita, Fuligem | domadores da rota | Caminho dos Domadores; Fuligem avisa do gás da mina |
| Dona Rubi | Rancho | Cura; mostra a cidade esvaziada pela Tia |
| Seu Cobre | Loja | Loja com Poção G; reage à escolha 2 (preço e fala) |
| Pirita | humor + missão | Bolo com gosto de cinza; pede o Cristal-vela para o aniversário do Gasito |
| Cascudo | dica | No Caminho Selvagem: ensina a reconhecer o som do Golden |
| Fagulha | dica | Ensina a mecânica da Guardiã: Mágico contra DEF alta |
| Vó Turmalina | lore | A Tia cuidou do Rei menino; planta o motivo dela |
| Seu Carvão | missão + pista | Missão do capacete; dono do mapa antigo (pista 3) |
| Capataz Bloqueio | domador/capanga | Guarda a forja; também vigia a estrada norte |
| Tia Fornalha | Guardiã | Mecânica de Defesa e a escolha 2 |

## 7. Casas de domadores
| Dono | Tema da equipe | Recompensa |
|---|---|---|
| Mestre Bigorna (Oficina) | Defesa: Bigornel e Picaréu sobem a guarda | 620 moedas + 2 Poções M |
| Ágata | Veneno de gás e cura (Fumarel + Cantilho) | 560 moedas + 3 Antídotos + 1 Reviver |

## 8. Escolhas e consequências
| Escolha | Opções | Consequência |
|---|---|---|
| Caminho da Rota 2 | Domadores / Cascalho / Galeria Velha | Moedas e itens / XP e marcadores / curto, com um selvagem forte |
| **Escolha 2: a corrente mestra** | Quebrar / Pedir que ela solte | Quebrar: os mineiros fogem, a loja fica 25% mais cara e o único **Vagonauta** aparece na câmara sul (recrutável). Pedir: a Tia dá o **Martelo da Tia** (abre o atalho de entulho da Rota 3), a loja dá 10% de desconto e soma **+1 Redenção** (`red_minas`). |
| Missão do capacete | Fazer / ignorar | 2 Poções G |
| Missão do bolo da Pirita | Fazer / ignorar | 2 Poções M e uma festa de aniversário |

## 9. Falas (PT-BR, na ordem dos roteiros)

### `minas/placa_bifurcacao`
- *(narração)* ← Trilha dos Domadores · ↑ Galeria Velha · → Campo de Cascalho

### `minas/vigia_entrada`
- **Vigia da Trilha:** Alto! Lasca de Raiz? Deixa eu ver... É do machado do Ramalho, sim.
- **Vigia da Trilha:** Pode passar. Mas lá em cima não é o Bosque. Lá a Tia não ri.
- **SPK_LIA:** Por que tudo aqui é cinza? Até a grama! Será que alguém pintou? *(if partner_lia)*
- **SPK_LIA:** Ah, é fumaça. Tem uma chaminé enorme lá no norte. Quem acende um fogo desse tamanho? *(if partner_lia)*
- **SPK_TARO:** Cheiro de forja. Meu pai cheirava assim quando voltava do trabalho. *(if partner_taro)*
- **SPK_TARO:** ...Anda. Tô com pressa. *(if partner_taro)*
- *[flag vigia_lasca_ok = True]*

### `minas/vigia`
- **Vigia da Trilha:** Eu só vigio a trilha. A cinza vigia o resto.

### `minas/seixo`
- **Seu Seixo:** Domador paga em moeda, cascalho paga em esqueleto, e a Galeria Velha... paga em susto.
- **Seu Seixo:** Lá dentro mora um aguadeiro que canta no escuro. Bonito. Mas bate forte.

### `minas/brita`
- **Brita:** Capacete na cabeça, esqueleto na mão. Bora ver quem cava mais fundo!
- *[batalha tamer: Picaréu 25, Fumarel 24 · 420 moedas]*
- **Brita:** Cavei meu próprio buraco. Que vergonha.

### `minas/brita_depois`
- **Brita:** Cavei meu próprio buraco. Que vergonha.

### `minas/graxa`
- **Graxa:** Esse vagonete não anda há meses. Eu também não. Bora mexer!
- *[batalha tamer: Toreiro 26, Picaréu 25 · 450 moedas]*
- **Graxa:** Pelo menos agora eu tô suado de verdade.

### `minas/graxa_depois`
- **Graxa:** Pelo menos agora eu tô suado de verdade.

### `minas/fuligem`
- **Fuligem:** Limpo chaminé da forja. Respiro fumaça. Meus esqueletos também. Prepara o pulmão!
- *[batalha tamer: Fumarel 27, Bigornel 26 · 480 moedas + 1× pocao_m, 1× antidoto]*
- **Fuligem:** Cof, cof. Leva um antídoto pra Mina. Lá o ar morde.

### `minas/fuligem_depois`
- **Fuligem:** Cof, cof. Leva um antídoto pra Mina. Lá o ar morde.

### `minas/placa_brasal`
- *(narração)* Brasal. Aqui o fogo nunca dorme. Nem a gente.

### `minas/placa_mina`
- *(narração)* ← Mina Funda. Entrada proibida por ordem da Tia.

### `minas/rubi`
- *[ação heal: {}]*
- *[ação respawn: {}]*
- **Dona Rubi:** A fumaça baixou! Hoje de manhã vi o céu. Era azul, imagina. *(if fornalha_beaten)*
- **Dona Rubi:** Cinza no cabelo, cinza no chá, cinza no travesseiro. Deita, que pelo menos aqui é quentinho.
- **Dona Rubi:** Antes, o Rancho vivia cheio de mineiro com esqueleto no colo. Agora só tem você.
  - (escolha) "`OPT_P_RANCH`" → `vila_mare/rancho` / "`OPT_P_LEAVE`"

### `minas/cobre`
- **Seu Cobre:** Com os mineiros fugidos, tudo encareceu. Não me olha assim, a culpa é de quem quebrou. *(if minas_quebrou)*
- **Seu Cobre:** Os mineiros voltaram e o minério também. Pra você, desconto de amigo. *(if minas_negociou)*
- **Seu Cobre:** Minério? Não tem. Mas poção grande eu arranjo. Do jeito que o povo apanha... *(if_not fornalha_beaten)*
- *[ação shop: {"id": "brasal"}]*
- **Seu Cobre:** Volte sempre. E bata a cinza da bota antes de entrar.

### `minas/pirita`
- **Pirita:** A fumaça baixou! Vou fazer outro bolo. Com cobertura de verdade, dessa vez. *(if fornalha_beaten)*
- **Pirita:** Fiz bolo pro aniversário do meu esqueleto. Ficou com gosto de cinza. Tudo aqui tem. *(if_not fornalha_beaten)*

### `minas/fagulha`
- **Fagulha:** Você venceu a Tia? Com faísca ou com soco? Fala que foi com faísca! *(if fornalha_beaten)*
- **Fagulha:** Os esqueletos da Tia são duros feito pedra. Soco nem faz cócegas!
- **Fagulha:** Mas faísca entra em qualquer fresta. Golpe Mágico bate na RES, não na DEF. Anota!

### `minas/turmalina`
- **Vó Turmalina:** Ouvi o sino da cidade tocar de novo. Quem será que lembrou dele? *(if fornalha_beaten)*
- **Vó Turmalina:** A Fornalha forjou o sino desta cidade, no tempo do reino. Agora só forja corrente.
- **Vó Turmalina:** Tia do Rei, dizem. Cuidava dele quando ele era menino. Quem cuida demais, prende.

### `minas/carvao_pede`
- **Seu Carvão:** A Tia expulsou os mineiros de gente. Na correria, larguei meu capacete na Mina Funda. Busca pra mim?
- *[flag carvao_quest = True]*
- **Seu Carvão:** Na câmara do sul da mina, perto dos trilhos. A lanterna ainda deve estar acesa.

### `minas/carvao_onde`
- **Seu Carvão:** Na câmara do sul da mina, perto dos trilhos. A lanterna ainda deve estar acesa.

### `minas/carvao_obrigado`
- **Seu Carvão:** Meu capacete! Quarenta anos de mina nessa lata. Toma, duas Poções G. E olha o mapa ali na parede.
- *[ação take_item: {"item": "capacete_carvao", "n": 1}]*
- *[ação give_item: {"item": "pocao_g", "n": 2}]*
- *[flag carvao_done = True]*

### `minas/carvao_depois`
- **Seu Carvão:** Esse mapa é mais velho que a mina. Meu avô dizia que o mar desenhou ele sozinho.

### `minas/capacete`
- *(narração)* Um capacete com a lanterna acesa, caído entre os trilhos.
- *[ação give_item: {"item": "capacete_carvao", "n": 1}]*
- *[flag carvao_helmet_taken = True]*

### `minas/mapa_antigo`
- *(narração)* Um mapa antigo da costa, com três baías lado a lado e um farol na do meio.
- *(narração)* Você conhece essas três baías. São as da sua cidade, em 2040. Só os nomes estão errados.
- *(narração)* Coincidência... não é?
- *[flag pista_3 = True]*

### `minas/bigorna`
- **Mestre Bigorna:** Aqui se treina defesa. Meus esqueletos sobem a guarda até você cansar de bater.
- *[batalha tamer: Bigornel 30, Picaréu 30 · 620 moedas + 2× pocao_m]*
- **Mestre Bigorna:** Contra parede, não empurra: procura a fresta. A Tia luta igualzinho.

### `minas/bigorna_depois`
- **Mestre Bigorna:** Contra parede, não empurra: procura a fresta. A Tia luta igualzinho.

### `minas/agata`
- **Ágata:** Gás de mina é perfume pra mim. Aguenta três rodadas de veneno?
- *[batalha tamer: Fumarel 30, Bilheiro 29 · 560 moedas + 3× antidoto, 1× reviver]*
- **Ágata:** Aguentou. Leva esses antídotos, você mereceu respirar.

### `minas/agata_depois`
- **Ágata:** Aguentou. Leva esses antídotos, você mereceu respirar.

### `minas/guarda_estrada`
- **Capataz Bloqueio:** Ordem da Tia: ninguém sai. Nem eu. E olha que eu queria.

### `minas/bloqueio`
- **Capataz Bloqueio:** Turno da noite, turno do dia, turno de bater em intruso. Hoje é o terceiro.
- *[batalha tamer: Picaréu 31, Bigornel 31 · 500 moedas]*
- **Capataz Bloqueio:** Tá. Pode ir até a forja. Mas eu não vi você.

### `minas/bloqueio_depois`
- **Capataz Bloqueio:** Tá. Pode ir até a forja. Mas eu não vi você.

### `minas/lenco_parceiro`
- *(narração)* Um lenço vermelho com bolinhas amarelas, preso num prego da viga.
- **SPK_TARO:** Esse lenço... é da minha mãe. Ela amarrava no meu pescoço quando eu tinha frio.
- **SPK_TARO:** Ela passou por aqui. Então ela tá... inteira. Tá inteira.
- **SPK_TARO:** Vamos mais rápido. Por favor.
- *[flag lenco_visto = True]*

### `minas/lenco_recorrente`
- **SPK_TARO:** Ei. Não encosta. Esse lenço é da minha mãe.
- **SPK_TARO:** Os capangas trouxeram os levados por esta mina, rumo ao norte. Ela tá viva... quer dizer, inteira.
- **SPK_LIA:** A gente ajuda a procurar, Taro! Eu ilumino, você corre.
- **SPK_TARO:** ...Valeu. Mas eu vou na frente. Sempre vou.
- *[flag lenco_visto = True]*
- *[ação hide_npc: {"id": "taro_mina"}]*

### `minas/vagonauta`
- *(narração)* Um vagonete com cara de esqueleto desce os trilhos sozinho, livre e furioso.
  - (escolha) "Encarar o vagonete" → `minas/vagonauta_luta` / "Deixar quieto"

### `minas/vagonauta_luta`
- *[batalha wild: Vagonauta 30]*

### `minas/fornalha`
- **Tia Fornalha:** Regra um: ninguém entra na forja sem bater. Você não bateu.
- **Tia Fornalha:** Eu forjo as correntes que fecham as estradas. Estrada fechada, ninguém se perde. Simples.
- **Tia Fornalha:** Regra dois: quem quer passar, aguenta o calor. Vamos ver.
- *[batalha boss: Picaréu 34, Bigornel 33, Fumarel 35, Bilheiro 34 · 1000 moedas]*
- **Tia Fornalha:** Hmpf. Regra três: quem vence, fala. Fala logo.
- **Tia Fornalha:** O Rei é meu sobrinho. Quando a coroa rachar, a família vai embora de novo. Enquanto houver corrente, ninguém vai.
- *(narração)* A corrente mestra prende todos os mineiros à forja. O que você vai fazer?
  - (escolha) "Quebrar a corrente" → `minas/quebrar` / "Pedir que ela solte" → `minas/negociar`

### `minas/quebrar`
- *(narração)* Você puxa a alavanca da forja. A corrente mestra estoura com um estrondo.
- **Tia Fornalha:** Sem ordem, eles vão correr pro escuro! Olha só!
- *(narração)* Os esqueletos mineiros fogem pelas galerias. Um vagonete desgovernado some trilho abaixo.
- *[flag minas_quebrou = True]*
- **Tia Fornalha:** Vai. A estrada tá aberta. E não volta pedindo desconto.
- **Tia Fornalha:** Se encontrar a Musga no Pântano, manda ela comer direito. É ordem da tia.
- *[ação refresh_map: {}]*

### `minas/negociar`
- **Tia Fornalha:** Pedir? Faz cem anos que ninguém me pede nada. Só obedecem.
- **Tia Fornalha:** ...Regra quatro, que eu acabei de inventar: quem pede direito, recebe direito.
- **Tia Fornalha:** Turno encerrado! Soltem as correntes e vão pra casa. Amanhã, quem quiser, volta.
- *[flag minas_negociou = True]*
- *[flag red_minas = True]*
- *[ação give_item: {"item": "martelo_tia", "n": 1}]*
- **Tia Fornalha:** Leva meu martelo. Quebra pedra, não quebra promessa. Vai ter entulho no caminho do Pântano.
- **Tia Fornalha:** Se encontrar a Musga no Pântano, manda ela comer direito. É ordem da tia.
- *[ação refresh_map: {}]*

### `minas/fornalha_depois`
- **Tia Fornalha:** Os mineiros voltaram sozinhos. Trabalham mais rápido sem corrente. Não conta pra ninguém. *(if minas_negociou)*
- **Tia Fornalha:** As galerias estão vazias. Espero que você saiba o que fez. *(if minas_quebrou)*
- **Tia Fornalha:** Se encontrar a Musga no Pântano, manda ela comer direito. É ordem da tia.

### `minas/fornalha_escolha`
- **Tia Fornalha:** O Rei é meu sobrinho. Quando a coroa rachar, a família vai embora de novo. Enquanto houver corrente, ninguém vai.
- *(narração)* A corrente mestra prende todos os mineiros à forja. O que você vai fazer?
  - (escolha) "Quebrar a corrente" → `minas/quebrar` / "Pedir que ela solte" → `minas/negociar`

### `minas/mineiro_preso`
- *(narração)* Clang. Clang. Clang. O esqueleto não para de martelar. Nem olha pra você.

### `minas/mineiro_livre`
- *(narração)* O esqueleto mineiro martela devagar, cantarolando. Ninguém mandou: ele quis.

### `minas/chegada_brasal`
- **SPK_LIA:** Ninguém na rua... As janelas tão fechadas por causa da cinza? *(if partner_lia)*
- **SPK_LIA:** Se eu fosse uma cidade, ia querer alguém pra abrir as janelas. *(if partner_lia)*
- **SPK_TARO:** Cidade parada. Mina fechada. A Tia manda em tudo aqui. *(if partner_taro)*
- **SPK_TARO:** Ótimo. Mais uma pra eu derrubar. *(if partner_taro)*
- *[flag brasal_visto = True]*

### `minas/chegada_mina`
- **SPK_LIA:** Escuro de novo. Mas agora eu sei: escuro é só lugar sem lamparina ainda. *(if partner_lia)*
- **SPK_TARO:** Ouviu? Martelo. Muito martelo. Tem gente trabalhando sem parar lá dentro. *(if partner_taro)*
- *[flag mina_vista = True]*

### `minas/pirita_pede`
- **Pirita:** Amanhã é aniversário do meu Gasito, e vela nenhuma acende com tanta cinza.
- **Pirita:** Dizem que na Galeria Velha tem cristal que brilha sozinho...
- **Pirita:** Traz um pra mim? Vela que não apaga é a melhor vela.
- *[flag pirita_quest = True]*

### `minas/pirita_onde`
- **Pirita:** Galeria Velha, no meio da Rota 2. O cristal fica perto da saída norte.

### `minas/pirita_festa`
- **Pirita:** Achou! Gasito, olha a vela! Parabéns pra você, nessa cinza tão...
- *[ação take_item: {"item": "cristal_vela", "n": 1}]*
- *[ação sfx: {"name": "birthday"}]*
- *(narração)* O Gasito sopra o cristal. Não apaga, claro. Ele sopra de novo, mais forte. Todo mundo ri.
- **Pirita:** Toma, duas Poções M. E um pedaço de bolo... com só um pouquinho de cinza.
- *[ação give_item: {"item": "pocao_m", "n": 2}]*
- *[flag pirita_done = True]*

### `minas/cristal_vela`
- *(narração)* Um cristal do tamanho de um polegar, quentinho e brilhando sozinho.
- *[ação give_item: {"item": "cristal_vela", "n": 1}]*
- *[flag cristal_pego = True]*

### `minas/cascudo`
- **Cascudo:** Eu cato cristal aqui. Uma vez vi um esqueleto dourado brilhando mais que todos eles juntos!
- **Cascudo:** Ele piscava e fazia tlin-tlin. Se ouvir esse som, corre atrás!

## 10. Contagem
Cerca de **1131 palavras** de texto de jogo em PT-BR nesta região.
