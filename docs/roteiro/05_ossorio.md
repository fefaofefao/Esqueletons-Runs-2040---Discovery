# Roteiro — Ato 4: Rota 4 e Cidade Murada de Ossório

Fase 4e. **Gerado por `tools/maps/ossorio.py`**, a mesma fonte que grava os mapas, NPCs e diálogos do jogo, portanto o jogo implementa exatamente o que está aqui. Diálogos em `data/dialogs/ossorio.json`.

**Duração alvo:** 25 min. **Idades:** chegada 46–54; selvagens 45–51; domadores 48–55; Guardião ~62 (protótipo do balance.json).

## 1. Problema local
**Ossório**, a antiga capital do reino, vive em **lei marcial**: o Guardião **Caliço** pôs os moradores de guarda na muralha à espera de um inimigo que nunca vem, impôs toque de recolher e fechou o portão norte. O **Arquivo Real** está lacrado por ordem do Rei: "ninguém lê o passado". O Rei esconde ali o motivo de tudo: a profecia do herdeiro.

## 2. Pista de 2040 (nº 5)
**A revelação de 2040.** No Arquivo Real, o registro: "Quando a coroa rachar, o eco chamará o último do sangue, onde o farol virar museu." Ao lado, o retrato do príncipe Ossárion menino, com o rosto do protagonista. Ele lembra do vidro vibrando e da coroa cantando no museu: veio de 2040 porque é do sangue do Rei. (Pistas 1–4 fecham aqui: ingresso, brasão, mapa, "cheiro de família".)

## 3. Momento de Lia e Taro
- **Lia:** no Arquivo, o diário da Rainha Duna conta que ela ergueu o farol para o marido sempre achar o caminho de casa. Parceira: "Então o Rei não é mau. Ele só tem medo do escuro. Igual eu tinha." Recorrente: ela está no Arquivo e promete acender o farol "até pro Rei".
- **Recorrente:** batalha opcional no norte da Rota 4 (Taro: "vou passar por todos"; Lia: "uma batalha pra dar coragem"). Depois, Taro deixa o jogador ir na frente "só hoje" — primeiro sinal de confiança.
- Arco de Lia: medo → coragem → começa a ver o Rei como alguém com medo, e não como vilão.

## 4. Guardião: Comandante Caliço (irmão do Rei)
- **Parentesco:** irmão
- **Personalidade:** orgulhoso, militar, honrado; fala em ordens ("Atenção!", "Em formação!")
- **Motivo para servir ao Rei:** **Honra:** "A família não abandona a família." Jurou que o irmão nunca mais perderia ninguém.
- **Mecânica-tema:** **Sintonia.** A equipe age em pares seguidos na timeline (+25%). Ensina a **montar** Sintonia e a **quebrá-la** com golpes de atraso. A Capitã Viseira e os Gêmeos Elo treinam isso antes.
- **Equipe:** Bastião 62, Escrivélio 61, Carrilhão 62, Troncalho 63.
- **Recompensa:** 1600 moedas; o Arquivo abre e o portão norte também.

## 5. Mapas
| Mapa | Conteúdo |
|---|---|
| **Rota 4** (`rota_4`) | Estrada real de pedra. 3 caminhos: **Cadetes** (oeste: Elmo, Malva, Bigode), **Campo das Bandeiras** (leste) e **Aqueduto Velho** (centro, curto, com um selvagem forte). Recorrente no norte. Placa e o Mensageiro Trote dão a dica. |
| **Ossório** (`ossorio`) | Cidade murada: Rancho (Ameia), Empório (Dobrão), casas da Capitã Viseira e dos Gêmeos Elo, o **Arquivo Real** (abre após o Guardião), praça com chafariz, estátua do príncipe e torre do sino; Clarim (escolha 4) e Selo (missão do farol). |
| **Quartel** (`quartel`) | Salão com selvagens, Sargento Grade, câmara sul com o único **Bufardo** e o pátio do Caliço. |
| Interiores | Rancho da Ameia, Empório do Dobrão, casas da Viseira e dos Elo, Arquivo Real. |

## 6. NPCs e motivo de existir
| NPC | Função | Por que existe |
|---|---|---|
| Mensageiro Trote | dica | Explica os 3 caminhos; mostra o quartel que só carimba e não responde |
| Elmo, Malva, Bigode | domadores da rota | Caminho dos Cadetes; soldados entediados pela lei marcial |
| Dona Ameia | Rancho | Cura; o toque de recolher até no Rancho |
| Mercador Dobrão | Loja | Comércio com autorização do quartel (humor burocrático) |
| Fivela | humor | O pai vigia a muralha; muda depois do Guardião |
| Velho Brasão | lore | Conheceu o príncipe menino que só olhava o mar |
| Pregoeiro Clarim | escolha 4 | Lê (ou não) o Registro Real na praça |
| Arquivista Selo | missão | Pergunta quem ergueu o farol (só acerta quem leu o diário) |
| Sargento Grade | capanga | Guarda o pátio do Guardião |
| Caliço | Guardião | Sintonia; abre o Arquivo por honra |

## 7. Casas de domadores
| Dono | Tema da equipe | Recompensa |
|---|---|---|
| Capitã Viseira | Sintonia em fileira (Broquel + Badaleiro) | 760 moedas + 2 Poções G |
| Gêmeos Elo | Sintonia de iguais (dois Escrivélios) | 740 moedas + 1 Reviver + 2 Antídotos |

## 8. Escolhas e consequências
| Escolha | Opções | Consequência |
|---|---|---|
| Caminho da Rota 4 | Cadetes / Campo das Bandeiras / Aqueduto | Moedas e itens / XP e marcadores / curto, com um selvagem forte |
| Recorrente | Lutar / recusar | 700 moedas e +10% no marcador |
| **Escolha 4: o Registro Real** | Contar à cidade / Guardar segredo | Contar: a cidade se rebela, guardas leais ao Rei passam a vigiar a Rota 5 (**mais batalhas**), Caliço promete ficar do seu lado no Castelo; **+1 Redenção** (`red_ossorio`). Segredo: menos batalhas, e Caliço fica neutro. |
| Missão do farol (Selo) | Responder / ignorar | Acertar (Rainha Duna): 2 Poções G + 1 Reviver |

## 9. Falas (PT-BR, na ordem dos roteiros)

### `ossorio/placa_bifurcacao`
- *(narração)* ← Caminho dos Cadetes · ↑ Aqueduto Velho · → Campo das Bandeiras

### `ossorio/chegada_rota`
- **SPK_LIA:** Bandeiras azuis em todo canto! Alguém muito importante morava aqui. *(if partner_lia)*
- **SPK_TARO:** Estrada de pedra, gasta no meio. Muita gente marchou por aqui. *(if partner_taro)*
- *[flag rota4_vista = True]*

### `ossorio/trote`
- **Mensageiro Trote:** Três caminhos pra Ossório: o dos cadetes, o do campo e o aqueduto. No aqueduto mora coisa velha.
- **Mensageiro Trote:** Eu levo recado pro quartel. Ninguém responde. Só carimbam e devolvem.

### `ossorio/elmo`
- **Cadete Elmo:** Cadete Elmo, em serviço! Identificação ou batalha!
- *[batalha tamer: Broquel 48, Escrivélio 48 · 640 moedas]*
- **Cadete Elmo:** Identificação aceita... por derrota.

### `ossorio/elmo_depois`
- **Cadete Elmo:** Identificação aceita... por derrota.

### `ossorio/malva`
- **Escudeira Malva:** Escudo pra cima, esqueleto pra frente. É assim que se marcha em Ossório!
- *[batalha tamer: Broquel 49, Badaleiro 49 · 660 moedas]*
- **Escudeira Malva:** Marchei pra trás. Acontece com as melhores.

### `ossorio/malva_depois`
- **Escudeira Malva:** Marchei pra trás. Acontece com as melhores.

### `ossorio/bigode`
- **Recruta Bigode:** Três semanas de guarda e nenhuma aventura. Você é minha aventura!
- *[batalha tamer: Forjalma 50, Broquel 50 · 700 moedas + 1× pocao_g]*
- **Recruta Bigode:** Melhor aventura da semana. Única, mas a melhor.

### `ossorio/bigode_depois`
- **Recruta Bigode:** Melhor aventura da semana. Única, mas a melhor.

### `ossorio/rival_taro`
- **SPK_TARO:** Ossório tem soldado em cada esquina. Vou passar por todos. Começando por você.
  - (escolha) "`OPT_P_FIGHT`" → `ossorio/rival_taro_luta` / "`OPT_P_NOT_NOW`"

### `ossorio/rival_taro_luta`
- *[batalha tamer: Timonaço 52, Broquel 51 · 700 moedas]*
- **SPK_TARO:** ...Vai na frente. Só hoje.
- *[ação hide_npc: {"id": "rival_taro_o"}]*

### `ossorio/rival_lia`
- **SPK_LIA:** Ossório tem um arquivo com todos os livros do reino! Mas antes, uma batalha. Pra dar coragem!
  - (escolha) "`OPT_P_FIGHT`" → `ossorio/rival_lia_luta` / "`OPT_P_NOT_NOW`"

### `ossorio/rival_lia_luta`
- *[batalha tamer: Faroleza 52, Espinhardo 51 · 700 moedas]*
- **SPK_LIA:** Te vejo no arquivo! Quer dizer... se um dia abrirem.
- *[ação hide_npc: {"id": "rival_lia_o"}]*

### `ossorio/placa_cidade`
- *(narração)* Ossório. Antiga capital do reino. Toque de recolher ao pôr do sol.

### `ossorio/placa_quartel`
- *(narração)* ← Quartel. Proibida a entrada de civis.

### `ossorio/estatua`
- *(narração)* Estátua do príncipe Ossárion, ainda menino. O tempo apagou o rosto.

### `ossorio/chegada_cidade`
- **SPK_LIA:** Uma cidade inteira de muralha. Eles têm medo de quê? *(if partner_lia)*
- **SPK_TARO:** Soldado na muralha, soldado no portão. Eles esperam uma guerra. *(if partner_taro)*
- *[flag ossorio_visto = True]*

### `ossorio/ameia`
- *[ação heal: {}]*
- *[ação respawn: {}]*
- **Dona Ameia:** Sem toque de recolher! Hoje o Rancho fica aberto até tarde. *(if calico_beaten)*
- **Dona Ameia:** Toque de recolher ao pôr do sol. Até os esqueletos do Rancho dormem em formação. *(if_not calico_beaten)*
- **Dona Ameia:** Quer deixar alguém descansando? Aqui ninguém dorme fora de hora... mas eu deixo.
  - (escolha) "`OPT_P_RANCH`" → `vila_mare/rancho` / "`OPT_P_LEAVE`"

### `ossorio/dobrao`
- **Mercador Dobrão:** Comércio só com autorização do quartel. Eu tenho autorização. Custou caro.
- *[ação shop: {"id": "ossorio"}]*
- **Mercador Dobrão:** Volte quando quiser. Em fila, de preferência.

### `ossorio/fivela`
- **Fivela:** Meu pai voltou da muralha! Ele disse que o inimigo era a gente mesmo. Não entendi. *(if calico_beaten)*
- **Fivela:** Meu pai monta guarda na muralha faz três semanas. Esperando inimigo. O único inimigo é o tédio. *(if_not calico_beaten)*

### `ossorio/brasao`
- **Velho Brasão:** Varri este pátio no tempo do reino. O príncipe era um menino tristinho, sempre olhando o mar.
- **Velho Brasão:** Dizem que ele virou o Rei. Eu digo que ele nunca parou de olhar o mar.

### `ossorio/clarim`
- **Pregoeiro Clarim:** A cidade inteira sabe. E ninguém foi pra casa dormir! *(if ossorio_revelou)*
- **Pregoeiro Clarim:** Meu clarim continua mudo. Combinamos, né? *(if ossorio_segredo)*
- **Pregoeiro Clarim:** Esse papel tem o selo real! Quer que eu leia na praça? A cidade inteira vai ouvir. *(if has_registro_real; if_none ossorio_revelou, ossorio_segredo)*
  - (escolha) "Contar à cidade" → `ossorio/contar` / "Guardar segredo" → `ossorio/segredo`
- **Pregoeiro Clarim:** Ouçam, ouçam! Toque de recolher ao pôr do sol, por ordem do Comandante Caliço! *(if_none has_registro_real, ossorio_revelou, ossorio_segredo)*
- **Pregoeiro Clarim:** Desculpa, é força do hábito. Eu grito até pra pedir pão. *(if_none has_registro_real, ossorio_revelou, ossorio_segredo)*

### `ossorio/contar`
- **Pregoeiro Clarim:** Ouçam, ouçam! "Quando a coroa rachar, o eco chamará o último do sangue..."
- *[ação sfx: {"name": "exclaim"}]*
- *(narração)* A praça cochicha, depois grita. No alto da muralha, guardas tiram o elmo e descem.
- *(narração)* Agora todo mundo sabe que o Rei procura um herdeiro. Alguns vão ficar do seu lado. Outros, do lado dele.
- *[flag ossorio_revelou = True]*
- *[flag red_ossorio = True]*

### `ossorio/segredo`
- **Pregoeiro Clarim:** Segredo de Estado. Meu clarim fica mudo. Pela primeira vez na vida.
- *[flag ossorio_segredo = True]*

### `ossorio/selo`
- **Arquivista Selo:** O Arquivo guarda mil anos de história. O Rei mandou lacrar tudo. Ninguém lê o passado. *(if_not calico_beaten)*
- **Arquivista Selo:** O Comandante abriu o Arquivo! Leia com cuidado. Livro velho morde. *(if calico_beaten; if_not livro_farol_lido)*
- **Arquivista Selo:** Leu o diário da estante? Então me diga: quem ergueu o farol da praia? *(if livro_farol_lido)*
  - (escolha) "O próprio Rei" → `ossorio/selo_rei` / "A Rainha Duna" → `ossorio/selo_certo` / "A Tia Fornalha" → `ossorio/selo_tia`

### `ossorio/selo_certo`
- **Arquivista Selo:** Exato! A Rainha Duna. Quem lê, merece. Tome, para a viagem.
- *[ação give_item: {"item": "pocao_g", "n": 2}]*
- *[ação give_item: {"item": "reviver", "n": 1}]*
- *[flag selo_done = True]*

### `ossorio/selo_rei`
- **Arquivista Selo:** Errado. O Rei só olhava o mar. Quem construiu foi outra pessoa. Volte a ler.

### `ossorio/selo_tia`
- **Arquivista Selo:** A Fornalha forja sinos, não faróis. Volte a ler, jovem.

### `ossorio/selo_depois`
- **Arquivista Selo:** Mil anos de livros, e ninguém lia. Agora tem fila. Fila de leitor!

### `ossorio/viseira`
- **Capitã Viseira:** Em Ossório, dois agem como um. Sintonia é disciplina! Vamos ver a sua.
- *[batalha tamer: Broquel 53, Badaleiro 53 · 760 moedas + 2× pocao_g]*
- **Capitã Viseira:** Quebrou nossa fileira com atraso. Isso é que é estudar o inimigo.

### `ossorio/viseira_depois`
- **Capitã Viseira:** Quebrou nossa fileira com atraso. Isso é que é estudar o inimigo.

### `ossorio/elo`
- **Gêmeos Elo:** A gente fala junto, luta junto, perde... separado?
- *[batalha tamer: Escrivélio 53, Escrivélio 52 · 740 moedas + 1× reviver, 2× antidoto]*
- **Gêmeos Elo:** Ensaiamos tudo. Menos perder.

### `ossorio/elo_depois`
- **Gêmeos Elo:** Ensaiamos tudo. Menos perder.

### `ossorio/registro`
- *(narração)* Um livro de registros, aberto há mil anos na mesma página.
- *(narração)* "Quando a coroa rachar, o eco chamará o último do sangue, onde o farol virar museu."
- *(narração)* Ao lado, o retrato do príncipe Ossárion, menino. O rosto é o seu.
- *(narração)* O vidro vibrando. A coroa cantando na vitrine. Agora você lembra: você veio de 2040.
- *(narração)* E foi chamado porque é do sangue do Rei.
- **SPK_LIA:** Esse menino... é você? Mas o quadro tem mil anos! *(if partner_lia)*
- **SPK_LIA:** Onde o farol virar museu... O meu farol vira museu um dia? *(if partner_lia)*
- **SPK_TARO:** Tá. Isso é estranho até pra mim. *(if partner_taro)*
- **SPK_TARO:** Se você é da família dele... ele te quer pra quê? *(if partner_taro)*
- *[flag pista_5 = True]*
- *[ação give_item: {"item": "registro_real", "n": 1}]*

### `ossorio/registro_de_novo`
- *(narração)* "...onde o farol virar museu." O retrato continua olhando pra você.

### `ossorio/livro_farol`
- *(narração)* Diário da Rainha Duna: "Ergui o farol para que meu marido, quando saísse ao mar, sempre achasse o caminho de casa."
- **SPK_LIA:** A família do Rei construiu o farol! Eles também queriam que ninguém se perdesse. *(if partner_lia)*
- **SPK_LIA:** Então o Rei não é mau. Ele só tem medo do escuro. Igual eu tinha. *(if partner_lia)*
- **SPK_TARO:** Farol. A Lia ia gostar de ler isso. *(if partner_taro)*
- *[flag livro_farol_lido = True]*

### `ossorio/lia_arquivo`
- **SPK_LIA:** Lê o diário da estante! A rainha construiu o farol pro marido sempre voltar pra casa!
- **SPK_LIA:** Eu vou acender ele. Pra todo mundo voltar pra casa. Até o Rei.
- *[flag lia_arquivo_visto = True]*
- *[ação hide_npc: {"id": "lia_arquivo"}]*

### `ossorio/cronicas`
- *(narração)* Crônicas da Família Real, volume único. As páginas cheiram a poeira e a mar.
- *(narração)* "Ramalho, primo do rei, lenhador. Perdia toda queda de braço e ria mais alto que o vencedor."
- *(narração)* "Fornalha, tia do rei, ferreira. Forjou o sino de Brasal e criou o príncipe quando a mãe dele adoeceu."
- *(narração)* "Musga, sobrinha do rei, herbalista. Curava a corte inteira; ninguém lembrava de visitá-la na torre."
- *(narração)* "Caliço, irmão do rei, capitão. Jurou nunca abandonar a família. Cumpriu até depois do fim."
- *(narração)* "Duna, a rainha, veio do deserto com tambores. Ergueu o farol. Alva, a filha, nasceu na noite em que ele acendeu."
- *(narração)* A última página está em branco. Alguém escreveu a lápis, com letra de menino: "Volta."

### `ossorio/chegada_quartel`
- **SPK_LIA:** Todo mundo no mesmo passo... parece música sem melodia. *(if partner_lia)*
- **SPK_TARO:** Disciplina. Meu pai ia gostar. Eu não. *(if partner_taro)*
- *[flag quartel_visto = True]*

### `ossorio/grade`
- **Sargento Grade:** Ninguém passa da grade sem senha. A senha é: vencer o Sargento Grade.
- *[batalha tamer: Broquel 55, Escrivélio 54 · 720 moedas]*
- **Sargento Grade:** Senha correta. Infelizmente.

### `ossorio/grade_depois`
- **Sargento Grade:** Senha correta. Infelizmente.

### `ossorio/bufardo`
- *(narração)* Um esqueleto corneteiro, de bochechas infladas, ensaia um toque que ninguém ouve há mil anos.
  - (escolha) "Ouvir o toque" → `ossorio/bufardo_luta` / "`OPT_M_LEAVE`"

### `ossorio/bufardo_luta`
- *[batalha wild: Bufardo 53]*

### `ossorio/calico`
- **Comandante Caliço:** Atenção! Civil não entra no quartel! Identifique-se!
- **Comandante Caliço:** Sou Caliço, irmão do Rei. A família não abandona a família. Nunca.
- **Comandante Caliço:** Em formação! Vamos ver se você sabe quebrar uma fileira.
- *[batalha boss: Bastião 62, Escrivélio 61, Carrilhão 62, Troncalho 63 · 1600 moedas]*
- **Comandante Caliço:** Fileira rompida... Recuar com honra!
- **Comandante Caliço:** Meu irmão perdeu todos uma vez. Eu jurei que ele nunca mais perderia ninguém.
- **Comandante Caliço:** Regra do quartel: o vencedor tem direito ao Arquivo. Leia o que meu irmão escondeu.
- **Comandante Caliço:** Honra exige verdade. Mesmo a verdade que dói.
- *[ação refresh_map: {}]*

### `ossorio/calico_depois`
- **Comandante Caliço:** Você contou à cidade. Insubordinação... e verdade. Quando chegar a hora, conte comigo. *(if ossorio_revelou)*
- **Comandante Caliço:** Você guardou o segredo. Discrição. Um soldado agradece. *(if ossorio_segredo)*
- **Comandante Caliço:** Honra exige verdade. Mesmo a verdade que dói. *(if_none ossorio_revelou, ossorio_segredo)*

## 10. Contagem
Cerca de **1033 palavras** de texto de jogo em PT-BR nesta região.
