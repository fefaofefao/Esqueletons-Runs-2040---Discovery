# Roteiro — Ato 6: Rota 6 e Deserto dos Ecos

Fase 4g. **Gerado por `tools/maps/deserto.py`**, a mesma fonte que grava os mapas, NPCs e diálogos do jogo, portanto o jogo implementa exatamente o que está aqui. Diálogos em `data/dialogs/deserto.json`.

**Duração alvo:** 25 min. **Idades:** chegada 68–76; selvagens 67–73; domadores 72–78; Guardiã ~85 (protótipo do balance.json).

## 1. Problema local
A Guardiã **Rainha Duna** ergueu uma **tempestade de areia sem fim** ao redor do castelo, para que ninguém incomode o marido em luto, e mandou calar os **tambores** que guiavam as caravanas pelas dunas. Sem os tambores, as caravanas se perdem seguindo o próprio eco: **Palmeiral** está sem comércio, e a Cartógrafa Rosa perdeu o marido na Rota 6.

## 2. Pista de 2040 (nº 7)
Depois da luta, a Rainha Duna conta **para que** o Rei chamou o herdeiro: a coroa só se refaz na cabeça de alguém do sangue, e prende quem a usa no trono **para sempre**. Ele vai pedir que o protagonista a coloque, não por crueldade, mas por medo de perder a família de novo. É o dilema do final.

## 3. Momento de Lia e Taro
- **Fogueira em Palmeiral** (cena opcional, a qualquer momento): Lia pergunta se o protagonista volta para 2040 e pede que ele acenda "o farol de lá também"; Taro pergunta se ele vai embora e quase admite que se importa ("Não tanto faz").
- Depois da revelação da Duna: Lia ("Ninguém devia ficar preso pra sempre. Nem o Rei") e Taro ("Eu mesmo tiro essa coroa da sua cabeça").
- Arcos: Lia já pensa na luz para os outros (até para o Rei); Taro já protege alguém além dos pais.

## 4. Guardião: Rainha Duna (esposa do Rei, mãe da Alva)
- **Parentesco:** esposa
- **Personalidade:** sábia, cansada, gentil; fala com imagens da natureza (chuva, areia, estrelas)
- **Motivo para servir ao Rei:** **Amor:** se ela partir, ele fica sozinho de vez. Foi ela quem ergueu o farol para ele voltar para casa.
- **Mecânica-tema:** **Resistência.** A equipe troca de lugar e cura em grupo; quem cai na timeline é substituído por um aliado descansado. Ensina a **gerir a equipe** e a **trocar na hora certa**. A Cameleira Tâmara e o Velho Cantil preparam.
- **Equipe:** Aguilhão 85, Astrolar 84, Ecoarca 86, Palafitor 85.
- **Recompensa:** 2200 moedas; a tempestade baixa e a estrada do castelo aparece.

## 5. Mapas
| Mapa | Conteúdo |
|---|---|
| **Rota 6** (`rota_6`) | Mar de dunas. 3 caminhos: **Caravanas** (oeste: Corcova, Véu, Pá), **Dunas Altas** (leste, com o Seu Alforje perdido) e **Passagem do Eco** (centro, curta, com um selvagem forte). Placa e o Velho Cantil dão a dica. |
| **Palmeiral** (`palmeiral`) | Oásis de tendas: Rancho (Moringa), Tenda da Canela, tendas da Tâmara e dos Batuque, tenda da Cartógrafa, lago, palmeiras, tambores calados e a fogueira da cena do parceiro. |
| **Templo das Areias** (`templo_areias`) | Camareiro Sândalo, o único **Ampulhor** ao sul e a Rainha Duna. |
| Interiores | Rancho da Moringa, Tenda da Canela, tendas da Tâmara, dos Batuque e da Cartógrafa. |

## 6. NPCs e motivo de existir
| NPC | Função | Por que existe |
|---|---|---|
| Velho Cantil | dica | Explica os 3 caminhos e o silêncio dos tambores |
| Corcova, Véu, Pá | domadores da rota | Caminho das Caravanas |
| Seu Alforje | missão (perdido) | O marido da Rosa, perdido nas dunas: missão de encontrar alguém, não um objeto |
| Dona Moringa | Rancho | Cura; muda quando os tambores voltam |
| Mercadora Canela | Loja | Preço "da saudade": o comércio parado |
| Grão | humor | Conta grãos de areia; depois vê o castelo |
| Vó Miragem | lore | Por que a rainha ergueu a tempestade: amor |
| Cartógrafa Rosa | missão | Pede para achar o marido; o mapa dela estava certo |
| Camareiro Sândalo | capanga | Guarda o templo |
| Rainha Duna | Guardiã | Resistência; pista 7 (para que o Rei quer o herdeiro) |

## 7. Casas de domadores
| Dono | Tema da equipe | Recompensa |
|---|---|---|
| Cameleira Tâmara | Trocas no tempo certo (Aguilhão + Ecoarca) | 940 moedas + 2 Fatias de Bolo |
| Irmãos Batuque | Cura em grupo e ritmo (Ecoarca + Astrolar) | 960 moedas + 2 Vela de Aniversário |

## 8. Escolhas e consequências
| Escolha | Opções | Consequência |
|---|---|---|
| Caminho da Rota 6 | Caravanas / Dunas Altas / Passagem do Eco | Moedas e itens / XP, marcadores e a missão do Alforje / curto, com um selvagem forte |
| Missão da caravana | Fazer / ignorar | 2 Vela de Aniversário + 2 Fatias de Bolo |
| Carta da Alva (escolha 5) | — | Se o jogador a carrega, a Duna reage com esperança (prévia do Final A) |

## 9. Falas (PT-BR, na ordem dos roteiros)

### `deserto/placa_bifurcacao`
- *(narração)* ← Trilha das Caravanas · ↑ Passagem do Eco · → Dunas Altas

### `deserto/chegada_rota`
- **SPK_LIA:** Oi! ...Oi... oi... O deserto repete tudo que a gente fala! *(if partner_lia)*
- **SPK_LIA:** Será que ele também fica sozinho? *(if partner_lia)*
- **SPK_TARO:** Areia na bota. Areia no osso. Areia em tudo. *(if partner_taro)*
- *[flag rota6_vista = True]*

### `deserto/cantil`
- **Velho Cantil:** Caravana vai pelo oeste, bicho anda pelas dunas altas, e no meio... o eco engana. Siga a parede.
- **Velho Cantil:** Antes, os tambores guiavam a gente. A rainha mandou calar todos. Agora só o vento fala.

### `deserto/corcova`
- **Cameleiro Corcova:** Meu camelo fugiu e me deixou os esqueletos. Troca justa? Vamos descobrir!
- *[batalha tamer: Aguilhão 72, Palafitor 72 · 860 moedas]*
- **Cameleiro Corcova:** Troca justa. Meio injusta pra mim.

### `deserto/corcova_depois`
- **Cameleiro Corcova:** Troca justa. Meio injusta pra mim.

### `deserto/veu`
- **Dançarina Véu:** Danço pra espantar a tempestade. Ainda não funcionou. Talvez com uma batalha!
- *[batalha tamer: Ecoarca 73, Cristalor 73 · 880 moedas]*
- **Dançarina Véu:** A tempestade ficou. Mas eu me diverti.

### `deserto/veu_depois`
- **Dançarina Véu:** A tempestade ficou. Mas eu me diverti.

### `deserto/pa`
- **Arqueólogo Pá:** Cavo atrás do reino antigo. Achei três colheres e um esqueleto bravo. Quer conhecer?
- *[batalha tamer: Astrolar 74, Aguilhão 74 · 900 moedas + 2× pocao_g]*
- **Arqueólogo Pá:** Vou catalogar essa derrota. Peça número quatro.

### `deserto/pa_depois`
- **Arqueólogo Pá:** Vou catalogar essa derrota. Peça número quatro.

### `deserto/alforje`
- **Seu Alforje:** Água! ...Ah, não é água. É gente. Também serve! Me perdi seguindo o meu próprio eco.
- **Seu Alforje:** Diz pra Rosa, lá em Palmeiral, que eu tô vivo. E que o mapa dela tava certo. Eu é que tava errado.
- *[flag alforje_achado = True]*

### `deserto/alforje_depois`
- **Seu Alforje:** Vou esperar a tempestade baixar. Sentadinho. Sem eco.

### `deserto/placa_cidade`
- *(narração)* Palmeiral. Água, sombra e notícia velha.

### `deserto/placa_templo`
- *(narração)* ← Templo das Areias. Silêncio: a rainha descansa.

### `deserto/chegada_cidade`
- **SPK_LIA:** Um lago no meio do deserto! Parece um farol de água. *(if partner_lia)*
- **SPK_TARO:** Tambores pendurados e ninguém tocando. Isso tá errado. *(if partner_taro)*
- *[flag palmeiral_visto = True]*

### `deserto/fogueira`
- *(narração)* A fogueira estala. O céu do deserto tem mais estrelas do que você lembrava.
- **SPK_LIA:** Quando isso tudo acabar... você volta pra 2040? *(if partner_lia)*
- **SPK_LIA:** Se voltar, acende o farol de lá também. Aí eu vou saber que você chegou. *(if partner_lia)*
- **SPK_TARO:** Quando isso acabar... você vai embora? *(if partner_taro)*
- **SPK_TARO:** ...Tanto faz. Quer dizer. Não tanto faz. *(if partner_taro)*

### `deserto/moringa`
- *[ação heal: {}]*
- *[ação respawn: {}]*
- **Dona Moringa:** Tão tocando tambor lá fora! Faz um ano que eu não durmo com barulho bom. *(if duna_beaten)*
- **Dona Moringa:** Bebe água primeiro, conversa depois. Seus esqueletos também: osso seco racha. *(if_not duna_beaten)*
- **Dona Moringa:** Quer deixar alguém aqui na sombra? Eu rego direitinho.
  - (escolha) "`OPT_P_RANCH`" → `vila_mare/rancho` / "`OPT_P_LEAVE`"

### `deserto/canela`
- **Mercadora Canela:** Tempero, tecido e remédio. A caravana não chega, então o preço é o da saudade.
- *[ação shop: {"id": "palmeiral"}]*
- **Mercadora Canela:** Volte com sede de compras.

### `deserto/grao`
- **Grão:** Com a tempestade embora, dá pra ver o castelo! Ele é mais feio de perto? *(if duna_beaten)*
- **Grão:** Eu contei os grãos de areia da praça. Deu um monte. Amanhã eu conto de novo pra conferir. *(if_not duna_beaten)*

### `deserto/miragem`
- **Vó Miragem:** A rainha Duna era a mais gentil da corte. Quando o Rei voltou triste, ela levantou a tempestade pra ninguém incomodar.
- **Vó Miragem:** Amor também constrói muralha. Só que de areia.

### `deserto/rosa_pede`
- **Cartógrafa Rosa:** O Alforje saiu com a caravana e sumiu na Rota 6. Meu mapa diz que ele tá nas dunas altas, mas ninguém acredita em mapa.
- **Cartógrafa Rosa:** Você acredita? Procura ele pra mim, nas dunas do leste.
- *[flag rosa_quest = True]*

### `deserto/rosa_onde`
- **Cartógrafa Rosa:** Dunas altas, a leste da Rota 6. Ele usa um turbante cor de areia. Ou seja: boa sorte.

### `deserto/rosa_obrigada`
- **Cartógrafa Rosa:** Ele disse que meu mapa tava certo? Ele disse isso? Vou emoldurar a frase.
- **Cartógrafa Rosa:** Toma: duas velas de aniversário e o meu mapa das estrelas. Quem acha gente perdida merece.
- *[ação give_item: {"item": "reviver", "n": 2}]*
- *[ação give_item: {"item": "pocao_g", "n": 2}]*
- *[flag rosa_done = True]*

### `deserto/rosa_depois`
- **Cartógrafa Rosa:** Mapa certo, marido errado. Mas é o meu marido errado.

### `deserto/tamara`
- **Cameleira Tâmara:** No deserto, quem não troca de montaria morre de cansaço. Troca de esqueleto na hora certa, vamos ver!
- *[batalha tamer: Aguilhão 77, Ecoarca 76 · 940 moedas + 2× pocao_g]*
- **Cameleira Tâmara:** Trocou no tempo certo. A rainha luta assim.

### `deserto/tamara_depois`
- **Cameleira Tâmara:** Trocou no tempo certo. A rainha luta assim.

### `deserto/batuque`
- **Irmãos Batuque:** Proibiram o tambor. Não proibiram a batalha! Tum-tum-PÁ!
- *[batalha tamer: Ecoarca 77, Astrolar 76 · 960 moedas + 2× reviver]*
- **Irmãos Batuque:** Perdemos no ritmo. Acontece.

### `deserto/batuque_depois`
- **Irmãos Batuque:** Perdemos no ritmo. Acontece.

### `deserto/chegada_templo`
- **SPK_LIA:** Que silêncio... Até meus passos têm medo de fazer barulho. *(if partner_lia)*
- **SPK_TARO:** Templo bonito. Bonito demais pra alguém triste morar. *(if partner_taro)*
- *[flag templo_visto = True]*

### `deserto/sandalo`
- **Camareiro Sândalo:** A rainha não recebe ninguém. Eu recebo por ela. Com batalha.
- *[batalha tamer: Astrolar 78, Ecoarca 78 · 980 moedas]*
- **Camareiro Sândalo:** Recebido. Pode passar. Tire as sandálias.

### `deserto/sandalo_depois`
- **Camareiro Sândalo:** Recebido. Pode passar. Tire as sandálias.

### `deserto/ampulhor`
- *(narração)* Um esqueleto-ampulheta conta grãos de areia. Perdeu a conta mil vezes e recomeçou mil e uma.
  - (escolha) "Virar a ampulheta" → `deserto/ampulhor_luta` / "`OPT_M_LEAVE`"

### `deserto/ampulhor_luta`
- *[batalha wild: Ampulhor 75]*

### `deserto/duna`
- **Rainha Duna:** Um herdeiro no meu deserto. Eu senti você chegando, como se sente a chuva.
- **Rainha Duna:** Sou Duna, esposa do Rei. Ergui o farol para ele voltar pra casa. Ele voltou... e nunca mais saiu.
- **Rainha Duna:** Se eu partir, ele fica sozinho de vez. Então eu fico. E você também fica, até me vencer.
- *[batalha boss: Aguilhão 85, Astrolar 84, Ecoarca 86, Palafitor 85 · 2200 moedas]*
- **Rainha Duna:** Você troca de lugar com os seus na hora certa. Como uma família.
- **Rainha Duna:** Você precisa saber por que ele te chamou.
- **Rainha Duna:** A coroa só se refaz na cabeça de alguém do sangue. E prende quem a usa no trono. Para sempre.
- **Rainha Duna:** Ele vai pedir que você a coloque. Não por crueldade. Ele só não aguenta perder a família de novo.
- *[flag pista_7 = True]*
- **SPK_LIA:** Ninguém devia ficar preso pra sempre. Nem você... nem o Rei. *(if partner_lia)*
- **SPK_TARO:** Se você colocar essa coroa, eu mesmo tiro ela da sua cabeça. *(if partner_taro)*
- **Rainha Duna:** Você traz uma carta da nossa filha? ...Então ainda há esperança para ele. *(if has_carta_alva)*
- **Rainha Duna:** Você viu a Alva? Ela está bem? ...Que bom. Ela sempre esperou demais por ele. *(if_not has_carta_alva)*
- **Rainha Duna:** A tempestade vai baixar. O castelo fica ao norte. Cuida dele por mim, herdeiro. Mesmo que seja dizendo não.
- *[ação refresh_map: {}]*

### `deserto/duna_depois`
- **Rainha Duna:** Os tambores voltaram. Ele vai ouvir lá do castelo. Talvez lembre de quando dançava.

## 10. Contagem
Cerca de **754 palavras** de texto de jogo em PT-BR nesta região.
