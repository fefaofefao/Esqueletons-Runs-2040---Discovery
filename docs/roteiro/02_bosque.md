# Roteiro — Ato 1: Rota 1 e Bosque das Raízes

Fase 4b. Implementado exatamente como está aqui. Falas em `i18n/dialogue.csv` (prefixo `DLG_B_`), roteiros em `data/dialogs/bosque.json`, mapas gerados por `tools/maps/make_bosque.py`.

**Duração alvo:** 25 min. **Idades** (`balance.json`): chegada 10–18; selvagens 10–15; domadores até 17; Guardião ~22.

## 1. Problema local
A vila **Raizal** vive de ervas e madeira. Por ordem do Guardião **Ramalho**, os esqueletos lenhadores **trançaram raízes em todas as trilhas** ("Ninguém sai, ninguém se perde"). Os mercadores não chegam, e a erva-de-febre que a curandeira Sálvia usa está acabando. A vila só respira de novo quando Ramalho perde e manda desfazer o trançado.

## 2. Pista de 2040 (nº 2)
No **Bosque Velho**, atrás da vila, o esqueleto único **Raizerno** dorme fundido ao tronco mais antigo. Um **brasão** está entalhado na casca: **uma coroa sobre uma onda**, o mesmo desenho do ingresso do museu. O jogo mostra o ingresso ao lado ("O desenho é igual ao do ingresso.").

## 3. Momento de Lia (e do recorrente)
- **Lia parceira:** no **Túnel das Raízes** (o atalho da rota), está escuro demais. Lia treme, mas acende a lamparina e diz que vai na frente. Primeiro passo do arco "medo → luz".
- **Lia recorrente (parceiro Taro):** você a encontra **parada na boca do túnel**, com medo. Taro empurra: "Vai logo." Ela entra mesmo assim. Batalha opcional na saída do túnel.
- **Taro recorrente (parceiro Lia):** espera na saída do túnel, impaciente; batalha opcional. "Ramalho sabe pra onde levaram os mais velhos. Eu vou perguntar do meu jeito."

## 4. Guardião: Ramalho (primo do Rei)
- **Personalidade:** brincalhão, competitivo e barulhento; fala alto e conta vantagem.
- **Motivo:** **dívida**. Foi o primeiro primo que o Rei trouxe de volta e acha que deve a segunda vida a ele.
- **Mecânica-tema: Atraso.** A equipe usa golpes pesados que **empurram o turno** do jogador (Golpe de Tora, Investida). Ensina a **ler a timeline** e a responder com golpes **leves**.
- **Equipe** (idade ~22): Toreiro (22, Golpe de Tora), Vagalú (22) e Raizela (23).
- **Arena:** a Clareira do Machado, no norte de Raizal.
- **Recompensa:** 800 moedas, o item-chave **Lasca de Raiz** (o passe que o vigia da Rota 2 pede na fase 4c) e as raízes da estrada principal se desfazem (caminho direto entre a Vila Maré e Raizal).

### Falas do Guardião
- **Antes:** "Primo do Rei, campeão de queda de braço do Bosque e dono deste machado! Você é o tal que abriu o cais?"
- **Antes:** "Aqui a gente espera. Quem espera não se perde. Deixa eu te ensinar a esperar!"
- **Vitória do jogador:** "Ha! Bateu antes de eu levantar o machado. Assim não vale... vale, vale."
- **Depois (motivo):** "O primo me trouxe de volta primeiro. Eu devo tudo a ele. Mas trançar o bosque inteiro... foi demais."
- **Depois (pista):** "Se for às Minas, cuidado com a Tia Fornalha. Ela não ri de nada."

## 5. Mapas
| Mapa | Conteúdo |
|---|---|
| **Rota 1** (`rota_1`) | Sai da Vila Maré e se divide em **3 caminhos** que se reencontram antes de Raizal: **Domadores** (oeste, 3 domadores), **Selvagem** (leste, campo de flores com mais esqueletos) e **Atalho** (Túnel das Raízes, escuro e curto, com 1 selvagem forte). Placas na bifurcação; o Lenhador Velho dá a dica. |
| **Raizal** (`raizal`) | Vila na floresta: Rancho, Loja (estoque com Poção M), 2 casas de domadores, NPCs e a trilha para a Clareira (Guardião) e para o Bosque Velho. |
| **Bosque Velho** (`bosque_velho`) | Clareira sagrada: Raizerno (único, batalha selvagem estática) e o brasão. |
| Interiores | Rancho, Loja, Casa dos Irmãos Galho, Casa da Sálvia (missão). |

## 6. Falas por NPC

### Rota 1
- **Placa (bifurcação):** ← Caminho dos Domadores · ↑ Túnel das Raízes · → Campo das Flores
- **Lenhador Velho (dica):** "Três caminhos, um destino. Domador dá moeda, flor dá esqueleto, túnel dá medo."
- **Lenhador Velho:** "As raízes fecharam a estrada inteira. Só o Ramalho manda desfazer."
- **Domador Rufo (Caminho dos Domadores):** "Ei! Você tem cara de quem perde. Prova que eu tô errado!" → *Lasquinho 12, Fungote 12* · 300 moedas
- **Domadora Íris:** "Meus esqueletos são lentos, mas quando batem..." → *Baldinho 13, Lasquinho 13* · 320 moedas
- **Domador Cipó:** "Primo do Rei mandou vigiar. Eu vigio... batalhando!" → *Brotim 14, Fungote 14* · 350 moedas + Poção M
- **Túnel (entrada, parceiro Lia):** Lia: "Tá escuro... muito escuro." / Lia: "Tudo bem. Eu tenho luz. Eu vou na frente!"
- **Túnel (entrada, parceiro Taro):** Taro: "Escuro? Melhor. Ninguém me vê chegando."
- **Túnel (Lia recorrente):** Lia: "Eu... eu tava só olhando a entrada. Não tô com medo!" / Taro: "Vai logo." / Lia: "Tá bom, tá bom!"
- **Recorrente (saída do túnel):** Taro: "Ramalho sabe pra onde levaram os mais velhos. Eu vou perguntar do meu jeito." *ou* Lia: "Atravessei sozinha! Agora me enfrenta, que eu tô corajosa!" → batalha opcional (idade 14) · 200 moedas
- **Depois da luta:** "Te vejo em Ossório. Fica vivo... quer dizer, fica inteiro!"

### Raizal
- **Placa:** Raizal. Madeira boa, chá melhor.
- **Rancho — Dona Tília:** "Raiz trançada não deixa ninguém sair, nem doente. Deita aí que eu cuido." / "Seu esqueleto tá crescendo forte. Já viu quando faz aniversário? Vira festa."
- **Loja — Seu Toco:** "Com a estrada fechada, eu vendo o que sobrou. E o que sobrou é caro." / "Volta quando o Ramalho cansar dessa brincadeira."
- **Sálvia (curandeira, missão "Erva-de-febre"):**
  - Antes: "Meu estoque de erva-de-febre acabou. Tem um pé no Bosque Velho, perto do tronco grande. Traz pra mim?"
  - Lembrete: "Bosque Velho, atrás da vila. A erva tem flor azul."
  - Com a erva: "Isso! Com isso eu curo meia vila. Toma, um Reviver e meu muito obrigada."
  - Depois: "Quando a estrada abrir, vou mandar chá pra Vila Maré."
- **Menino Graveto (humor):** "Eu tentei desfazer as raízes com os dentes. Agora as raízes têm marca de dente."
- **Dona Hera (lore, guardiões):** "O Ramalho não é mau. É primo do Rei, e todo primo quer agradar." / "Dizem que todos os Guardiões são da família. Família grande dá briga grande."
- **Guarda-raiz (bloqueio da Clareira, antes do Guardião):** "O Ramalho tá na Clareira. Ele adora visita... pra derrubar."

### Casas de domadores
- **Casa dos Irmãos Galho (tema: Atraso):** "A gente empurra seu turno pra lá e pra cá. Treino pro Ramalho!" → *Lasquinho 17, Brotim 16* · 400 moedas + 2 Poções M · Depois: "Viu? Golpe leve escapa do atraso."
- **Casa da Sálvia** (sem batalha; missão da erva).
- **Casa da Família Musgo (tema: veneno leve):** Pai Musgo: "Esporo aqui é tempero." → *Fungote 16, Brotim 16* · 350 moedas + 2 Antídotos · Depois: "Leva antídoto pras Minas. Lá o ar é pior."

### Bosque Velho
- **Raizerno (interagir):** narração: "Um esqueleto enorme dorme fundido ao tronco. Na casca, um brasão: uma coroa sobre uma onda." / "O desenho é igual ao do ingresso do museu." / (escolha) "Acordar" / "Deixar dormir" → **batalha selvagem** contra Raizerno (idade 20). O marcador funciona como em qualquer selvagem; ele volta a dormir no lugar depois de sair e voltar.
- **Erva-de-febre (objeto, com a missão):** "Você colheu a erva-de-febre de flor azul."

## 7. Escolhas e consequências
| Escolha | Opções | Consequência |
|---|---|---|
| Caminho da Rota 1 | Domadores / Selvagem / Túnel | Mais moedas e itens / mais XP e marcadores / mais curto, com um selvagem forte |
| Recorrente | Lutar / recusar | 200 moedas e marcador |
| Missão da erva | Fazer / ignorar | Reviver e um diálogo novo da Sálvia |
| Raizerno | Acordar / deixar | Batalha difícil por um único (recrutável com o marcador) |

## 8. NPCs e motivo de existir
| NPC | Função | Por que existe |
|---|---|---|
| Lenhador Velho | dica | Explica os 3 caminhos |
| Rufo, Íris, Cipó | domadores da rota | Caminho dos Domadores: moedas e itens |
| Tília | Rancho | Cura; liga o problema local (ninguém sai, nem doente) |
| Toco | Loja | Loja com Poção M e humor sobre a estrada fechada |
| Sálvia | missão | Problema local concreto: falta remédio |
| Graveto | humor | Alívio cômico |
| Hera | lore | Planta a ideia de que os Guardiões são família do Rei |
| Irmãos Galho, Família Musgo | casas de domadores | Treino de Atraso e de veneno, com recompensa |
| Ramalho | Guardião | Mecânica de Atraso |

## 9. Contagem
A contagem final de palavras é medida por `tools/maps/bosque_text.py` (orçamento ~1.800).
