# Roteiro — Final: Castelo do Rei Esqueleto, os 2 finais e o pós-jogo

Fase 4h. **Gerado por `tools/maps/castelo.py`**, a mesma fonte que grava os mapas, NPCs e diálogos do jogo, portanto o jogo implementa exatamente o que está aqui. Diálogos em `data/dialogs/castelo.json`.

**Duração alvo:** 20 min. **Idades:** chegada 80–86; selvagens 79–84; domadores 86–87; Provador Real ~90; Rei 120 (com escolta de 78).

## 1. Problema local
O castelo inteiro obedece à coroa rachada. Os levados (entre eles os **pais do Taro**) servem de guardas sem lembrar de ninguém. O Rei Ossárion espera o herdeiro na sala do trono, com uma mesa posta para sete que ninguém usa há mil anos.

## 2. Pista de 2040 (nº 8)
O Rei confirma tudo: o herdeiro foi chamado de 2040 para colocar a coroa e prendê-la de novo. A coroa racha diante dele com o mesmo som de vidro do museu, e a escolha é do jogador (recusar, ou tentar colocar e ser impedido pelo parceiro).

## 3. Momento de Lia e Taro
- **Portão:** os pais do Taro guardam a porta e não o reconhecem. Parceiro: "Então eu vou quebrar essa coroa." Recorrente: Taro chegou primeiro e espera ali.
- **Sala do trono:** o parceiro acende as velas (Lia com coragem; Taro com raiva) para o Rei ver o que perdeu.
- **Final:** quando a coroa se quebra, os pais reconhecem o Taro; ele **perdoa** (os pais e o Rei). A Lia acende o farol da Praia nos dois finais.
- Lia e Taro estão os dois na equipe (decisão do Fernando): tocam as falas de parceiro dos dois; as cenas de "recorrente" só aparecem em saves antigos, com um parceiro só.
- Arcos fechados: Lia medo → coragem → **luz para os outros**; Taro raiva → entendimento → **perdão**.

## 4. Guardião: Provador Real Degustor e o Rei Ossárion
- **Parentesco:** Degustor serve o Rei; Ossárion é o patriarca da família
- **Personalidade:** Degustor: guloso e dedicado (prova a comida do Rei todo dia, há mil anos). Rei: solitário, imponente, ferido.
- **Motivo para servir ao Rei:** O Rei não quer perder a família de novo; a lei "Ninguém sai, ninguém se perde" nasceu desse medo.
- **Mecânica-tema:** **Sequência de chefes:** os pais do Taro no portão, o Provador Real (equipe veneno/defesa/cura) e o Rei (120) com escolta. A fonte do Grande Salão cura e marca o ponto de volta; se a cidade de Ossório soube do registro, o **Caliço** está no portão e cura a equipe.
- **Equipe:** Pais do Taro: Timonaço 88 e 87 · Provador Real: Degustor 90, Bastião 89, Pergamor 90, Samovarão 89 · Rei Esqueleto 120 + Aguapéu 78.
- **Recompensa:** O Rei entra na equipe (idade 100) nos dois finais; créditos; pós-jogo livre.

## 5. Mapas
| Mapa | Conteúdo |
|---|---|
| **Portão** (`castelo_portao`) | Pátio diante da muralha; pais do Taro na porta; Taro (recorrente) e Caliço (se a escolha 4 foi contar). |
| **Grande Salão** (`castelo_salao`) | Guarda Real Ébano, Arauto Real, Cozinheiro Tempero, selvagens, a fonte (cura e ponto de volta) e o Provador Real diante da porta do trono. |
| **Sala do Trono** (`sala_trono`) | O Rei, a coroa no pedestal, velas acesas pelo parceiro, retratos e a mesa posta para sete. |
| **Museu de 2040** (`museu_2040`) | Epílogo: a vitrine vazia, "Peça em restauração" (gancho para o próximo jogo). |
| **Praia (pós-jogo)** | Farol aceso, Bento e o epílogo; os Guardiões viram **ecos** para revanche nos mesmos lugares. |

## 6. NPCs e motivo de existir
| NPC | Função | Por que existe |
|---|---|---|
| Pais do Taro | chefes do portão | Fecham o arco do Taro: não o reconhecem até a coroa quebrar |
| Caliço (condicional) | aliado | Consequência da escolha 4: cura a equipe no portão |
| Ébano, Arauto, Tempero | domadores do castelo | Os últimos capangas, com humor de mil anos de rotina |
| Provador Real Degustor | chefe | O guardião do trono; no pós-jogo vira o único Degustor (selvagem, recrutável) |
| Rei Ossárion | chefe final | Pede que o herdeiro coloque a coroa; entra na equipe nos dois finais |
| Bento (pós-jogo) | lore | Epílogo na Praia e dica dos ecos dos Guardiões |

## 7. Casas de domadores
| Dono | Tema da equipe | Recompensa |
|---|---|---|
| — | O Castelo não tem casas de domadores | — |

## 8. Escolhas e consequências
| Escolha | Opções | Consequência |
|---|---|---|
| A coroa | Colocar / Recusar | Colocar: o parceiro impede ("Se você colocar, nunca mais sai daqui!"). Os dois caminhos levam à batalha final. |
| **Final A — Redimir** | Carta da Alva + pelo menos 2 de: `red_minas`, `red_pantano`, `red_ossorio` | O Rei lê a carta, quebra a coroa por vontade própria, a família se despede (uma fala de cada Guardião) e ele pede para seguir o herdeiro. |
| **Final B — Derrotar** | Sem os requisitos | A coroa se parte com o golpe final, a família some sem despedida e o Rei entra na equipe em silêncio ("Não tenho mais ninguém"). |
| Nos dois finais | — | Os pais do Taro o reconhecem; Lia acende o farol; epílogo no museu de 2040 com a vitrine vazia; créditos; pós-jogo. |
| Pós-jogo | — | Ecos dos 6 Guardiões (revanche, idades 95–100, 3000 moedas), Degustor recrutável no salão, Ossário e casas restantes. |

## 9. Falas (PT-BR, na ordem dos roteiros)

### `castelo/chegada_portao`
- **SPK_TARO:** São eles. Meu pai. Minha mãe. *(if partner_taro)*
- **SPK_TARO:** Pai! Mãe! Sou eu, o Taro! *(if partner_taro)*
- *(narração)* Os dois guardas olham através dele, como se ele fosse vento. *(if partner_taro)*
- **SPK_TARO:** ...Eles não lembram. A coroa apagou eles. *(if partner_taro)*
- **SPK_TARO:** Então eu vou quebrar essa coroa. *(if partner_taro)*
- **SPK_TARO:** Cheguei primeiro. Como eu disse. *(if partner_lia; if_not partner_taro)*
- **SPK_TARO:** Aqueles dois no portão... são meus pais. Eles não me reconhecem. *(if partner_lia; if_not partner_taro)*
- **SPK_LIA:** Taro... a gente vai consertar isso. Juntos. *(if partner_lia)*
- **SPK_TARO:** ...Juntos. Tá. *(if partner_lia)*
- *[flag portao_visto = True]*

### `castelo/taro_portao`
- **SPK_TARO:** Vai. Eu fico aqui com eles. Se a coroa quebrar, quero ser a primeira cara que eles veem.

### `castelo/guardas`
- *(narração)* Dois esqueletos enormes de remo cruzam os remos diante da porta.
- **Guardas do Portão:** Ninguém entra. Ninguém sai. Ninguém se perde.
- *[batalha tamer: Timonaço 88, Timonaço 87 · 1200 moedas]*
- *(narração)* Os guardas abaixam os remos e se afastam, sem uma palavra.
- **SPK_TARO:** Desculpa, pai. Desculpa, mãe. Já, já eu volto. *(if partner_taro)*
- *[ação hide_npc: {"id": "pai_taro"}]*
- *[ação hide_npc: {"id": "mae_taro"}]*

### `castelo/calico_aliado`
- **SPK_CALICO:** Prometi e cumpro. Estou aqui.
- **SPK_CALICO:** Deixe-me cuidar dos seus. Um soldado também sabe tratar feridas.
- *[ação heal: {}]*

### `castelo/ebano`
- **Guarda Real Ébano:** Guarda Real Ébano. Ninguém chega ao trono. Ninguém sai, ninguém se perde.
- *[batalha tamer: Bastião 86, Forjalma 86 · 1000 moedas]*
- **Guarda Real Ébano:** Perdi. ...Isso conta como me perder?

### `castelo/ebano_depois`
- **Guarda Real Ébano:** Perdi. ...Isso conta como me perder?

### `castelo/arauto`
- **Arauto Real:** Anuncio a sua chegada: derrotado!
- *[batalha tamer: Pergamor 86, Aguilhão 86 · 1000 moedas]*
- **Arauto Real:** Corrijo o anúncio: vitorioso. Que vergonha pro arauto.

### `castelo/arauto_depois`
- **Arauto Real:** Corrijo o anúncio: vitorioso. Que vergonha pro arauto.

### `castelo/tempero`
- **Cozinheiro Tempero:** Mil anos cozinhando pra um Rei que não come. Hoje eu cozinho uma batalha!
- *[batalha tamer: Samovarão 87, Aguilhão 86 · 1050 moedas + 2× pocao_g]*
- **Cozinheiro Tempero:** Queimou. Como sempre.

### `castelo/tempero_depois`
- **Cozinheiro Tempero:** Queimou. Como sempre.

### `castelo/fonte`
- *(narração)* Uma fonte de água fresca no meio do castelo. Seus esqueletos bebem e descansam.
- *[ação heal: {}]*
- *[ação respawn: {}]*

### `castelo/degustor`
- **Provador Real Degustor:** Provador Real Degustor. Provo tudo antes do Rei: sopa, chá, veneno. Agora vou provar você.
- **Provador Real Degustor:** Hmm. Tempero de 2040. Picante.
- *[batalha boss: Degustor 90, Bastião 89, Pergamor 90, Samovarão 89 · 2500 moedas]*
- **Provador Real Degustor:** Amargo... A derrota tem gosto de chá frio.
- **Provador Real Degustor:** O Rei não come há mil anos. Eu provo a comida dele todo dia assim mesmo. Esperança tem gosto de pão quente.
- *[ação refresh_map: {}]*

### `castelo/degustor_depois`
- **Provador Real Degustor:** O Rei não come há mil anos. Eu provo a comida dele todo dia assim mesmo. Esperança tem gosto de pão quente.

### `castelo/degustor_livre`
- **Provador Real Degustor:** Sem coroa, sem patrão, sem cardápio. Quer provar uma batalha de verdade, só por gosto?
  - (escolha) "Provar" → `castelo/degustor_luta` / "`OPT_P_NOT_NOW`"

### `castelo/degustor_luta`
- *[batalha wild: Degustor 88]*

### `castelo/trono`
- *(narração)* A sala do trono é fria e escura. No alto, um esqueleto imenso de coroa rachada.
- **SPK_LIA:** Tá escuro aqui. Deixa eu acender. *(if partner_lia)*
- *(narração)* Lia acende as velas, uma por uma. A sala inteira aparece: retratos, brinquedos, uma mesa posta para sete. *(if partner_lia)*
- **SPK_LIA:** Pronto. Agora o senhor consegue ver o que perdeu? *(if partner_lia)*
- *(narração)* Taro acende as velas com raiva, uma por uma. A sala inteira aparece: retratos, brinquedos, uma mesa posta para sete. *(if partner_taro; if_not partner_lia)*
- **SPK_TARO:** Pronto. Agora olha pra gente. *(if partner_taro; if_not partner_lia)*
- **SPK_TARO:** E olha pra gente também. A gente não é quadro na parede. *(if_all partner_lia, partner_taro)*
- *[flag trono_iluminado = True]*
- **Rei Ossárion:** Então você veio. O último do meu sangue, de mil anos depois.
- **Rei Ossárion:** Eu sou Ossárion. Perdi minha família uma vez. Não vou perder de novo.
- *(narração)* A coroa racha mais um pouco, com um som de vidro. O mesmo som do museu.
- *[vai para `castelo/trono_coroa`]*

### `castelo/trono_de_novo`
- **Rei Ossárion:** Voltou. A coroa ainda espera por você.
- *[vai para `castelo/trono_coroa`]*

### `castelo/trono_coroa`
- **Rei Ossárion:** Coloque a coroa. Fique. Ninguém mais se perde.
  - (escolha) "Colocar a coroa" → `castelo/coroa_tentar` / "Recusar" → `castelo/recusar`

### `castelo/coroa_tentar`
- *(narração)* Você estende a mão para a coroa...
- **SPK_LIA:** Não! Se você colocar, nunca mais sai daqui! *(if partner_lia)*
- **SPK_TARO:** Eu avisei. Eu mesmo tiro ela da sua cabeça. *(if partner_taro)*
- *(narração)* Você recua a mão. Seus parceiros não soltam a sua.
- *[vai para `castelo/recusar`]*

### `castelo/recusar`
- **Rei Ossárion:** Então você é igual a todos. Vai embora e me deixa sozinho.
- **Rei Ossárion:** Não. Desta vez, ninguém sai.
- *[flag rei_falou = True]*
- *[batalha boss: Ossárion 120, Aguapéu 78]*
- *(narração)* O Rei cai de joelhos. A coroa pende, torta, da cabeça dele.
- **Rei Ossárion:** Mil anos... e perco de novo.
- *[vai para `castelo/final_a`]* *(if has_carta_alva; pelo menos 2 de red_minas, red_pantano, red_ossorio)*
- *[vai para `castelo/final_b`]*

### `castelo/final_a`
- *(narração)* Você tira do bolso a carta da Alva e a entrega ao Rei.
- *[ação take_item: {"item": "carta_alva", "n": 1}]*
- **Rei Ossárion:** A letra da minha filha...
- *(narração)* "Pai. Não precisa segurar a gente. A gente já está com o senhor, em tudo o que o senhor construiu."
- *(narração)* "Deixa a gente descansar. Deixa o senhor viver. Com amor, Alva."
- **Rei Ossárion:** Ela sempre escreveu melhor do que eu reinei.
- **Rei Ossárion:** Minha tia soltou os mineiros só porque você pediu. *(if red_minas)*
- **Rei Ossárion:** Você deu remédio a quem minha sobrinha adoeceu. *(if red_pantano)*
- **Rei Ossárion:** E Ossório leu a verdade em voz alta. Meu irmão ficou do seu lado. *(if red_ossorio)*
- **Rei Ossárion:** Você não veio tomar o meu lugar. Veio devolver o lugar de todos.
- *(narração)* O Rei tira a coroa. Por um instante, ela canta, como no museu.
- **Rei Ossárion:** Ninguém sai, ninguém se perde... Que lei boba. Todo mundo se perde um pouco. É assim que se acha o caminho.
- *[ação sfx: {"name": "golden"}]*
- *(narração)* Ele mesmo quebra a coroa nas mãos. A rachadura vira luz.
- *(narração)* Seis figuras de luz aparecem na sala. A família veio se despedir.
- **SPK_RAMALHO:** Primo! Valeu a segunda volta. A terceira eu dispenso!
- **SPK_FORNALHA:** Regra final: descansar. Até que enfim.
- **SPK_MUSGA:** Não me esqueçam, tá? ...Brincadeira. Eu sei que não vão, queridos.
- **SPK_CALICO:** Família não abandona família. Por isso agora a gente te deixa ir, irmão.
- **SPK_ALVA:** Pai, o senhor sorriu. Eu vi.
- **SPK_DUNA:** Ergui um farol pra você voltar. Agora volta pra vida, meu amor.
- *(narração)* A família vira poeira de luz. Os esqueletos do continente continuam vivos, mas agora ninguém manda neles.
- **Rei Ossárion:** Não tenho coroa, nem família, nem reino. Tenho um herdeiro teimoso.
- **Rei Ossárion:** Posso ir com você? Quero conhecer o mundo que eu fechei.
- *[flag final_a = True]*
- *[vai para `castelo/rei_entra`]*

### `castelo/final_b`
- *(narração)* O último golpe acerta a coroa. Ela se parte em mil pedaços.
- *[ação sfx: {"name": "grow_flash"}]*
- *(narração)* Um vento atravessa o castelo. Em todo o continente, os Guardiões somem de uma vez, sem despedida.
- **Rei Ossárion:** Tia... Musga... Caliço... Alva... Duna...
- *(narração)* Ninguém responde. O Rei fica sozinho no chão do trono.
- **Rei Ossárion:** Eu prendi todos para não perder ninguém. E perdi todos assim mesmo.
- *(narração)* Os esqueletos do continente continuam vivos, livres da coroa.
- **Rei Ossárion:** Não tenho mais ninguém.
- *(narração)* Ele se levanta devagar e caminha até você, em silêncio.
- *[flag final_b = True]*
- *[vai para `castelo/rei_entra`]*

### `castelo/rei_entra`
- *(narração)* O marcador de ossos do Rei se enche de uma vez.
- *[ação marker: {"species": "rei_esqueleto", "amount": 100}]*
- *[ação give_monster: {"species": "rei_esqueleto", "age": 100}]*
- *[flag rei_recrutado = True]*
- *[ação hide_npc: {"id": "rei"}]*
- *[vai para `castelo/final_comum`]*

### `castelo/final_comum`
- *(narração)* Lá embaixo, no portão, dois guardas soltam os remos ao mesmo tempo.
- **Pai do Taro:** Taro? É você?
- **Mãe do Taro:** Nosso pequeno remador! Você cresceu tanto!
- **SPK_TARO:** Pai. Mãe. ...Eu achei vocês. *(if partner_taro)*
- **Pai do Taro:** Foi você que nos achou, filho. A gente é que tava perdido.
- **SPK_TARO:** Passei o caminho todo com raiva dele. Agora... ele só queria a família de volta. Igual eu.
- **SPK_TARO:** Tá perdoado. Mas vocês me devem uns cem bolos de aniversário.
- **SPK_LIA:** O Taro achou eles! Agora só falta o meu farol. *(if partner_lia)*
- **SPK_LIA:** Vamos pra casa? Eu quero acender o farol com você do lado. *(if partner_lia)*
- **SPK_TARO:** A Lia prometeu acender o farol. Aposto que já tá lá em cima, toda orgulhosa. *(if partner_taro; if_not partner_lia)*
- *[ação fade: {"out": true}]*
- *[ação wait: {"s": 0.6}]*
- *[ação warp: {"map": "museu_2040", "x": 7, "y": 6, "facing": "up", "hide_player": true}]*
- *(narração)* 2040. Museu do Litoral. Exposição "O Reino Perdido de Ossório".
- *(narração)* Uma vitrine está vazia. Na plaquinha: "Peça em restauração".
- *(narração)* Lá fora, sem ninguém tocar no interruptor, a luz do velho farol se acende.
- *(narração)* O eco ainda chama. Esta história continua.
- *[flag game_cleared = True]*
- *[ação credits: {}]*
- *[ação heal_all: {}]*
- *[ação warp: {"map": "praia_despertar", "x": 10, "y": 17, "facing": "left"}]*

### `castelo/vitrine`
- *(narração)* "Coroa de osso, Reino de Ossório. Peça em restauração."

### `castelo/epilogo_praia`
- *(narração)* Praia do Despertar. O farol está aceso, girando devagar sobre o mar.
- **SPK_BENTO:** Olha só quem voltou! E olha o farol: aceso, depois de mil anos.
- **SPK_LIA:** Eu disse que ia acender! Agora ninguém se perde no mar. *(if partner_lia)*
- **SPK_BENTO:** Foi a pequena da lamparina. Subiu lá ontem à noite, toda orgulhosa. *(if partner_taro; if_not partner_lia)*
- **SPK_TARO:** Ela conseguiu. ...Não conta pra ela que eu fiquei feliz. *(if partner_taro)*
- **Rei Ossárion:** Minha Duna ergueu este farol. Ela ia gostar de vê-lo aceso. *(if final_a)*
- *(narração)* O Rei olha para o farol em silêncio, por muito tempo. *(if final_b)*
- **SPK_BENTO:** O continente é livre. Vai, completa teu Ossário. Dizem que os ecos dos Guardiões ainda esperam uma revanche.
- **SPK_BENTO:** E quando quiser voltar pra casa... o farol fica aceso. Vai que ele chama de volta.
- *[flag epilogo_visto = True]*
- *[ação respawn: {}]*

### `castelo/bento_final`
- **SPK_BENTO:** Farol aceso dá até vontade de pescar de noite. Os peixes é que não gostaram muito.
- **SPK_BENTO:** O continente é livre. Vai, completa teu Ossário. Dizem que os ecos dos Guardiões ainda esperam uma revanche.

### `castelo/farol_aceso`
- *(narração)* O farol está aceso. A luz gira devagar sobre o mar, como quem procura alguém.

### `castelo/eco_ramalho`
- **SPK_RAMALHO:** Sou só um eco do Ramalho, preso no cabo do machado. Mas eco também quer revanche!
  - (escolha) "`OPT_P_FIGHT`" → `castelo/eco_ramalho_luta` / "`OPT_P_NOT_NOW`"

### `castelo/eco_ramalho_luta`
- *[batalha tamer: Troncalho 95, Silvanor 95, Floralma 95 · 3000 moedas + 2× pocao_g]*
- *(narração)* O eco sorri e se desfaz no vento... até a próxima.

### `castelo/eco_fornalha`
- **SPK_FORNALHA:** Um eco da Tia. Regra do eco: repetir a última luta. Mais forte.
  - (escolha) "`OPT_P_FIGHT`" → `castelo/eco_fornalha_luta` / "`OPT_P_NOT_NOW`"

### `castelo/eco_fornalha_luta`
- *[batalha tamer: Rochedão 95, Forjalma 95, Miasmor 96, Cisternão 95 · 3000 moedas + 2× pocao_g]*
- *(narração)* O eco sorri e se desfaz no vento... até a próxima.

### `castelo/eco_musga`
- **SPK_MUSGA:** Eco da Musga, querido. Até eco fofoca: dizem que você ficou forte. Prova?
  - (escolha) "`OPT_P_FIGHT`" → `castelo/eco_musga_luta` / "`OPT_P_NOT_NOW`"

### `castelo/eco_musga_luta`
- *[batalha tamer: Caldeona 96, Palafitor 95, Aguapéu 95, Cogumestre 96 · 3000 moedas + 2× pocao_g]*
- *(narração)* O eco sorri e se desfaz no vento... até a próxima.

### `castelo/eco_calico`
- **SPK_CALICO:** Eco do Comandante. Em formação, uma última vez!
  - (escolha) "`OPT_P_FIGHT`" → `castelo/eco_calico_luta` / "`OPT_P_NOT_NOW`"

### `castelo/eco_calico_luta`
- *[batalha tamer: Bastião 97, Pergamor 96, Carrilhão 96, Troncalho 97 · 3000 moedas + 2× pocao_g]*
- *(narração)* O eco sorri e se desfaz no vento... até a próxima.

### `castelo/eco_alva`
- **SPK_ALVA:** Sou o eco da Alva. Meu pai está com você? Então me mostra que ele está em boas mãos.
  - (escolha) "`OPT_P_FIGHT`" → `castelo/eco_alva_luta` / "`OPT_P_NOT_NOW`"

### `castelo/eco_alva_luta`
- *[batalha tamer: Alpinor 98, Cristalor 97, Samovarão 98, Rochedão 97 · 3000 moedas + 2× pocao_g]*
- *(narração)* O eco sorri e se desfaz no vento... até a próxima.

### `castelo/eco_duna`
- **SPK_DUNA:** O eco da rainha ainda dança na areia. Dança comigo?
  - (escolha) "`OPT_P_FIGHT`" → `castelo/eco_duna_luta` / "`OPT_P_NOT_NOW`"

### `castelo/eco_duna_luta`
- *[batalha tamer: Aguilhão 99, Astrolar 99, Ecoarca 100, Palafitor 99 · 3000 moedas + 2× pocao_g]*
- *(narração)* O eco sorri e se desfaz no vento... até a próxima.

## 10. Contagem
Cerca de **1200 palavras** de texto de jogo em PT-BR nesta região.
