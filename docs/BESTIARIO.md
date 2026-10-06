# Bestiário — Esqueletons Runs 2040: Edição Discovery

A bíblia de criaturas (seção 8 do AGENTS.md). **Fonte única:** `tools/bestiary/bestiary.py`; este arquivo, `data/species.json` e `i18n/species.csv` são gerados por `tools/bestiary/build.py`. Sprites: `tools/art/gen_skeletons.py`. Folha de revisão visual: `docs/bestiario_sheet.png`.

**95 espécies no Ossário:** 27 linhas × 3 estágios (Bebê → Adolescente → Adulto), 13 únicos (6 deles são os ases dos Guardiões) e o Rei.

| Tipo | Linhas |
|---|---|
| Físico | 7 |
| Mágico | 7 |
| Cura/Suporte | 7 |
| Veneno | 6 |

| Região | Linhas novas | Único |
|---|---|---|
| Praia do Despertar / Vila Maré | 4: Remito/Timonaço, Lumiça/Faroleza, Mariscote/Espinhardo, Novelita/Redentora | — |
| Bosque das Raízes | 4: Lasquinho/Troncalho, Brotim/Floralma, Fungote/Cogumestre, Flautim/Silvanor | Raizerno, Troncudo |
| Minas de Cinzas | 4: Baldinho/Rochedão, Faisquim/Forjalma, Gasito/Miasmor, Cantilho/Cisternão | Vagonauta, Bigornão |
| Pântano Verde-Musgo | 4: Tinhinha/Caldeona, Estaquim/Palafitor, Lirito/Aguapéu, Zunzim/Colmeira | Brumaga, Caldeirona |
| Cidade Murada de Ossório | 4: Tampinha/Bastião, Rabisquim/Pergamor, Tilintim/Carrilhão, Caquinho/Rosáceo | Bufardo, Bandeirão |
| Picos Gelados | 3: Mochilim/Alpinor, Gelinho/Cristalor, Xicrim/Samovarão | Nevasco, Patinora |
| Deserto dos Ecos | 4: Ferrim/Aguilhão, Bussolito/Astrolar, Tambim/Ecoarca, Barrico/Urnadão | Ampulhor, Miragina |
| Castelo do Rei Esqueleto | 0: — | Degustor, Ossárion (Rei) |

## Praia do Despertar / Vila Maré

### Remito → Vogaréu → Timonaço
*Linha de **Taro**, parceiro inicial.*

- **Conceito:** Esqueleto de grumete dos barcos de pesca da Vila Maré, que nunca larga o remo.
- **Silhueta:** Remo vertical maior que o corpo ao lado direito; chapéu muda de touca de pompom para bandana e para quepe de capitão.
- **Arco de crescimento:** Bebê de touca e camiseta listrada com um remo de brinquedo → Adolescente de bandana e colete vermelho com um remo de verdade apoiado no chão → Adulto de casaco de lona e quepe, com o remo duplo atravessado nas costas como uma arma.
- **Personalidade:** Teimoso, leal, barulhento. **No mapa:** persegue o jogador.
- **Tipo:** Físico · **Raridade:** incomum · **Cresce aos** 16 e 36 anos
- **Golpe assinatura:** Remada Dupla / Double Stroke / Remada Doble

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 001 | Bebê | Remito | Oarlet | Remiño | 281 | Treina remadas no ar enquanto dorme. Ainda confunde o remo com uma colher. |
| 002 | Adolescente | Vogaréu | Strokeby | Bogador | 392 | Desafia qualquer um para uma corrida de barco. Perde a calma, nunca o ritmo. |
| 003 | Adulto | Timonaço | Helmsbone | Timonazo | 502 | Já atravessou tempestades sem barco, só com o remo. A tripulação dele são as ondas. |

### Lumiça → Prismela → Faroleza
*Linha de **Lia**, parceiro inicial.*

- **Conceito:** Esqueleto de aprendiz de faroleira do velho farol apagado da praia, guiada por uma lamparina.
- **Silhueta:** Luz sempre à direita e acima do corpo: lamparina na mão, depois lanterna de prisma nas costas, depois o próprio farol como coroa e um cajado-lente.
- **Arco de crescimento:** Bebê de touca de pano com uma lamparina pequena → Adolescente com a lanterna de prisma presa às costas e capa curta → Adulta de manto violeta, coroa-farol acesa e cajado com lente.
- **Personalidade:** Curiosa, sonhadora, corajosa. **No mapa:** patrulha.
- **Tipo:** Mágico · **Raridade:** incomum · **Cresce aos** 16 e 36 anos
- **Golpe assinatura:** Facho do Farol / Beacon Beam / Haz del Faro

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 004 | Bebê | Lumiça | Glimmet | Chispela | 281 | Acende a lamparina quando tem medo do escuro, ou seja, sempre. |
| 005 | Adolescente | Prismela | Prismae | Prismina | 392 | Desvia a luz do prisma para escrever recados no céu. Ninguém consegue ler a letra dela. |
| 006 | Adulto | Faroleza | Beaconne | Farolesa | 502 | A coroa dela gira devagar a noite inteira. Barcos perdidos chegam à praia seguindo esse brilho. |

### Mariscote → Ouriçal → Espinhardo

- **Conceito:** Esqueleto de catador de mariscos das pedras da praia, que aprendeu a usar os espinhos dos ouriços.
- **Silhueta:** Corpo largo e baixo coberto de espinhos que crescem a cada estágio; concha na cabeça vira capacete de ouriço espetado.
- **Arco de crescimento:** Bebê com uma concha na cabeça e um baldinho → Adolescente com luvas de ouriço e uma rede de catar → Adulto com armadura de ouriços e um tridente de espinhos.
- **Personalidade:** Desconfiado, paciente, espinhoso. **No mapa:** tímido (foge).
- **Tipo:** Veneno · **Raridade:** comum · **Cresce aos** 14 e 34 anos
- **Golpe assinatura:** Chuva de Espinhos / Spine Shower / Lluvia de Púas

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 007 | Bebê | Mariscote | Shellby | Almejito | 262 | Esconde-se dentro da concha quando alguém olha. A concha é bem menor que ele. |
| 008 | Adolescente | Ouriçal | Urchip | Erizón | 372 | Usa luvas de ouriço para cumprimentar. Por isso ninguém aperta a mão dele. |
| 009 | Adulto | Espinhardo | Spinnacle | Pinchardo | 482 | Fica imóvel nas pedras até a maré baixar. Quem pisa nele sente o veneno por três dias. |

### Novelita → Tramela → Redentora

- **Conceito:** Esqueleto de rendeira de redes da Vila Maré, que remenda redes e, com o mesmo fio, os amigos feridos.
- **Silhueta:** Formato de sino por causa da saia de rede; agulha de rede longa e novelo; rede vira xale e depois um tear nas costas como asas.
- **Arco de crescimento:** Bebê enrolada num novelo de fio → Adolescente com a agulha grande e a rede jogada nos ombros → Adulta com um tear portátil nas costas e a rede brilhante aberta como asas.
- **Personalidade:** Atenciosa, tagarela, caprichosa. **No mapa:** ronda em círculo.
- **Tipo:** Cura/Suporte · **Raridade:** comum · **Cresce aos** 14 e 34 anos
- **Golpe assinatura:** Remendo de Rede / Net Mend / Remiendo de Red

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 010 | Bebê | Novelita | Knotling | Ovillita | 262 | Rola pela areia quando se enrosca no próprio fio. Desenrolar leva a tarde toda. |
| 011 | Adolescente | Tramela | Shuttla | Tramona | 372 | Costura rasgos em velas, redes e mangas, sem pedir licença. |
| 012 | Adulto | Redentora | Tapestrix | Redencia | 482 | Tece com fios de luz da lua. Dizem que remenda até promessas quebradas. |

## Bosque das Raízes

### Lasquinho → Toreiro → Troncalho

- **Conceito:** Esqueleto de lenhador do Bosque das Raízes que só derruba árvores mortas, e defende as vivas no machado.
- **Silhueta:** Ferramenta de corte cada vez mais pesada à direita; ombros crescem até virar um tronco no ombro; barba de musgo no adulto.
- **Arco de crescimento:** Bebê de gorro xadrez arrastando um graveto → Adolescente com machado e mochila de toras → Adulto de barba de musgo carregando um tronco inteiro como clava.
- **Personalidade:** Teimoso, protetor, ruidoso. **No mapa:** persegue o jogador.
- **Tipo:** Físico · **Raridade:** comum · **Cresce aos** 18 e 40 anos
- **Golpe assinatura:** Golpe de Tora / Log Slam / Golpe de Tronco

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 013 | Bebê | Lasquinho | Twiglet | Astillo | 262 | Bate o graveto em tudo para ver o que é oco. Inclusive na própria cabeça. |
| 014 | Adolescente | Toreiro | Hatchley | Hachón | 372 | Empilha toras em torres perfeitas e fica bravo se o vento derruba. |
| 015 | Adulto | Troncalho | Timbrawl | Troncazo | 482 | O musgo da barba dele tem vida própria. Um golpe da tora abre clareiras. |

### Brotim → Raizela → Floralma

- **Conceito:** Esqueleto de herborista do bosque que colhe raízes medicinais e acaba virando parte do jardim.
- **Silhueta:** Algo verde brotando de cima: broto na cabeça, depois cesto de raízes, e por fim uma arvorezinha saindo das costelas com coroa de flores.
- **Arco de crescimento:** Bebê com um broto de duas folhas na cabeça → Adolescente de avental com cesto de raízes no braço → Adulta com uma arvorezinha crescendo entre as costelas e coroa de flores.
- **Personalidade:** Calma, gentil, distraída. **No mapa:** tímido (foge).
- **Tipo:** Cura/Suporte · **Raridade:** comum · **Cresce aos** 18 e 40 anos
- **Golpe assinatura:** Seiva Viva / Living Sap / Savia Viva

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 016 | Bebê | Brotim | Sproutle | Brotín | 262 | Fica parada ao sol para o broto crescer. Às vezes esquece de sair da chuva. |
| 017 | Adolescente | Raizela | Rootessa | Raicera | 372 | Sabe o nome de cada raiz do bosque e o chá certo para cada dor. |
| 018 | Adulto | Floralma | Bloomsoul | Floránima | 482 | A árvore dentro dela floresce quando alguém por perto se cura. Abelhas a seguem por todo canto. |

### Fungote → Esporito → Cogumestre

- **Conceito:** Esqueleto de colhedor de cogumelos que provou o cogumelo errado e passou a soltar esporos.
- **Silhueta:** Chapéu de cogumelo que cresce até virar um guarda-chuva largo que cobre o corpo todo; esporos flutuando em volta.
- **Arco de crescimento:** Bebê com um cogumelinho pintado na cabeça → Adolescente com cogumelos brotando nas costas e soltando esporos → Adulto sob um chapéu-cogumelo enorme, com cajado de micélio.
- **Personalidade:** Sonolento, misterioso, guloso. **No mapa:** patrulha.
- **Tipo:** Veneno · **Raridade:** incomum · **Cresce aos** 20 e 42 anos
- **Golpe assinatura:** Nuvem de Esporos / Spore Cloud / Nube de Esporas

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 019 | Bebê | Fungote | Mushkin | Hongüito | 281 | Espirra esporos quando ri. Ri de quase tudo. |
| 020 | Adolescente | Esporito | Sporeling | Esporín | 392 | Dorme encostado em troncos úmidos e acorda com cogumelos novos nas costas. |
| 021 | Adulto | Cogumestre | Fungaroth | Setarca | 502 | Debaixo do chapéu dele nunca chove. Quem fica tempo demais ali dorme por um dia inteiro. |

### Flautim → Vagalú → Silvanor

- **Conceito:** Esqueleto de flautista da floresta que chama vaga-lumes com uma flauta de osso.
- **Silhueta:** Flauta sempre na horizontal diante do rosto; vaga-lumes em volta; o adulto ganha chifres de galhos e capa de folhas.
- **Arco de crescimento:** Bebê com uma flautinha e um vaga-lume pousado na cabeça → Adolescente com flauta longa e um enxame de vaga-lumes em órbita → Adulto com chifres de galho, capa de folhas e flauta-cajado.
- **Personalidade:** Brincalhão, vaidoso, inquieto. **No mapa:** rápido.
- **Tipo:** Mágico · **Raridade:** raro · **Cresce aos** 22 e 46 anos
- **Golpe assinatura:** Melodia Vaga-lume / Firefly Tune / Melodía Luciérnaga

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 022 | Bebê | Flautim | Pipkin | Pitillo | 300 | Só sabe uma nota. Toca essa nota com muito sentimento. |
| 023 | Adolescente | Vagalú | Glowfife | Luciérnago | 412 | Os vaga-lumes dançam no ritmo da flauta. Quando erra a nota, eles apagam de vergonha. |
| 024 | Adulto | Silvanor | Sylvarch | Selvanor | 522 | Rege a floresta à noite como uma orquestra. As árvores se curvam para ouvir. |

## Minas de Cinzas

### Baldinho → Picaréu → Rochedão

- **Conceito:** Esqueleto de mineiro das Minas de Cinzas, do balde de ajudante à armadura de pedra.
- **Silhueta:** Balde na cabeça vira capacete com picareta no ombro e, no adulto, um corpo largo coberto de placas de pedra.
- **Arco de crescimento:** Bebê ajudante com um balde na cabeça → Adolescente mineiro de capacete com picareta → Adulto mestre de minas com armadura de pedra e picareta dupla.
- **Personalidade:** Trabalhador, sério, resistente. **No mapa:** patrulha.
- **Tipo:** Físico · **Raridade:** comum · **Cresce aos** 24 e 46 anos
- **Golpe assinatura:** Desmoronar / Cave-In / Derrumbe

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 027 | Bebê | Baldinho | Pailet | Cubetín | 262 | Usa o balde como capacete e como cama. Ainda não decidiu qual é o certo. |
| 028 | Adolescente | Picaréu | Pickard | Picador | 372 | Escuta a rocha antes de bater. Diz que cada pedra tem uma veia preferida. |
| 029 | Adulto | Rochedão | Bouldron | Peñascón | 482 | As placas de pedra da armadura foram arrancadas da mina mais funda. Desmoronamentos o contornam. |

### Faisquim → Bigornel → Forjalma

- **Conceito:** Esqueleto de ferreiro das forjas das Minas de Cinzas, cujo fogo nunca apaga.
- **Silhueta:** Avental de couro grande; martelo erguido à direita; no adulto, as costelas viram uma forja acesa no peito.
- **Arco de crescimento:** Bebê com martelinho e avental de couro grande demais → Adolescente com bigorna nas costas e fole na mão → Adulto com a forja acesa dentro das costelas e um martelo de lava.
- **Personalidade:** Orgulhoso, esquentado, generoso. **No mapa:** patrulha.
- **Tipo:** Mágico · **Raridade:** incomum · **Cresce aos** 24 e 46 anos
- **Golpe assinatura:** Martelo de Brasa / Ember Hammer / Martillo de Brasa

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 030 | Bebê | Faisquim | Sparkit | Chispín | 281 | Bate o martelinho em pedras para ver faíscas. Aplaude cada uma. |
| 031 | Adolescente | Bigornel | Anvillo | Yunquero | 392 | Carrega a bigorna para todo lado, caso precise consertar algo de repente. |
| 032 | Adulto | Forjalma | Kilnhart | Fraguador | 502 | A forja no peito dele aquece a mina inteira no inverno. Martela feitiços como quem martela ferro. |

### Gasito → Fumarel → Miasmor

- **Conceito:** Esqueleto de vigia de gás das galerias, que de tanto farejar o gás das minas passou a produzi-lo.
- **Silhueta:** Máscara de gás com um filtro redondo na frente; tanque nas costas que cresce até virar chaminés soltando névoa verde.
- **Arco de crescimento:** Bebê com uma mascarinha e uma gaiolinha vazia → Adolescente com um tanque de gás nas costas e uma mangueira → Adulto com máscara de foles e duas chaminés de névoa verde.
- **Personalidade:** Ansioso, metódico, abafado. **No mapa:** ronda em círculo.
- **Tipo:** Veneno · **Raridade:** comum · **Cresce aos** 24 e 46 anos
- **Golpe assinatura:** Vazamento / Gas Leak / Fuga de Gas

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 033 | Bebê | Gasito | Whiffle | Humito | 262 | Fareja tudo antes de entrar. A gaiolinha dele está sempre vazia, e ele prefere assim. |
| 034 | Adolescente | Fumarel | Fumehorn | Fumarón | 372 | O tanque das costas faz um apito agudo antes de vazar. Mineiros correm quando escutam. |
| 035 | Adulto | Miasmor | Miasmar | Miasmón | 482 | As chaminés soltam uma névoa verde que cobre galerias inteiras. Ele mesmo respira por filtros. |

### Cantilho → Bilheiro → Cisternão

- **Conceito:** Esqueleto de aguadeiro que leva água fresca aos mineiros nas galerias quentes das Minas de Cinzas.
- **Silhueta:** Recipiente de água cada vez maior: cantil a tiracolo, carrinho com bilhas, e uma cisterna redonda nas costas com mangueiras.
- **Arco de crescimento:** Bebê com um cantil maior que ele → Adolescente empurrando um carrinho com bilhas → Adulto com uma cisterna redonda nas costas e mangueiras de cura.
- **Personalidade:** Prestativo, tímido, refrescante. **No mapa:** tímido (foge).
- **Tipo:** Cura/Suporte · **Raridade:** raro · **Cresce aos** 28 e 50 anos
- **Golpe assinatura:** Jato Fresco / Cool Spray / Chorro Fresco

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 036 | Bebê | Cantilho | Sippet | Cantimplín | 300 | Oferece água a todos, até às pedras. Diz que elas parecem cansadas. |
| 037 | Adolescente | Bilheiro | Jugworth | Botijero | 412 | As bilhas tilintam no carrinho como um sino. Mineiros com sede seguem o som. |
| 038 | Adulto | Cisternão | Cisterno | Aljibón | 522 | A cisterna das costas nunca esvazia. Um banho de mangueira dele apaga até fogo de forja. |

## Pântano Verde-Musgo

### Tinhinha → Ervaçal → Caldeona

- **Conceito:** Esqueleto de lavadeira do pântano com cesto de ervas venenosas, que lava a roupa na água parada.
- **Silhueta:** Bacia na cabeça vira cesto e tábua de lavar nas mãos; a adulta carrega uma tina-caldeirão nas costas com um varal de ervas por cima.
- **Arco de crescimento:** Bebê com uma bacia na cabeça → Adolescente com cesto de ervas no quadril e tábua de lavar → Adulta com uma tina-caldeirão nas costas e um varal de ervas pendurado.
- **Personalidade:** Fofoqueira, prática, cheirosa. **No mapa:** patrulha.
- **Tipo:** Veneno · **Raridade:** comum · **Cresce aos** 30 e 52 anos
- **Golpe assinatura:** Anil Tóxico / Toxic Bluing / Añil Tóxico

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 041 | Bebê | Tinhinha | Tubbit | Tinita | 262 | A bacia na cabeça vira barquinho quando o pântano enche. |
| 042 | Adolescente | Ervaçal | Herbwash | Hierbera | 372 | Esfrega as roupas com ervas do pântano. Elas ficam limpas, e um pouco venenosas. |
| 043 | Adulto | Caldeona | Cauldra | Caldreona | 482 | A tina dela borbulha dia e noite. O vapor verde espanta até mosquitos. |

### Estaquim → Marretão → Palafitor

- **Conceito:** Esqueleto de construtor de palafitas do Pântano Verde-Musgo, que fincou tantas estacas que acabou andando sobre elas.
- **Silhueta:** Cada vez mais alto: estaquinha no ombro, feixe de estacas e marreta, e por fim o adulto sobre pernas-de-pau com a marreta pesada.
- **Arco de crescimento:** Bebê carregando uma estaquinha no ombro → Adolescente com um feixe de estacas nas costas e uma marreta → Adulto sobre pernas-de-pau, com marreta grande e chapéu de palha.
- **Personalidade:** Paciente, firme, desajeitado. **No mapa:** patrulha.
- **Tipo:** Físico · **Raridade:** comum · **Cresce aos** 30 e 52 anos
- **Golpe assinatura:** Estaca Firme / Pile Driver / Estaca Firme

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 044 | Bebê | Estaquim | Stakelet | Estaquín | 262 | Finca a estaquinha no chão e senta nela para descansar. Sempre afunda. |
| 045 | Adolescente | Marretão | Malleteer | Mazón | 372 | Cada martelada dele crava uma estaca inteira. O pântano treme junto. |
| 046 | Adulto | Palafitor | Stiltwarden | Palafitero | 482 | Anda sobre as pernas-de-pau como se fossem dele. Do alto, vigia as casas que ajudou a erguer. |

### Lirito → Regalírio → Aguapéu

- **Conceito:** Esqueleto de jardineiro aquático que cuida dos lírios do pântano com um regador de cabaça.
- **Silhueta:** Folha redonda de lírio na cabeça que cresce até virar um guarda-sol enorme; regador de cabaça na mão.
- **Arco de crescimento:** Bebê com uma folha de lírio como chapéu → Adolescente com regador de cabaça e flores nos ombros → Adulto sob uma folha gigante de lírio como escudo e guarda-sol.
- **Personalidade:** Sereno, poético, devagar. **No mapa:** ronda em círculo.
- **Tipo:** Cura/Suporte · **Raridade:** incomum · **Cresce aos** 32 e 56 anos
- **Golpe assinatura:** Orvalho de Lírio / Lily Dew / Rocío de Lirio

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 047 | Bebê | Lirito | Lilypip | Nenufito | 281 | Boia de costas no pântano usando a folha como travesseiro. |
| 048 | Adolescente | Regalírio | Pondrella | Regadora | 392 | Rega cada flor do pântano uma por uma, cantando o nome delas. |
| 049 | Adulto | Aguapéu | Lotusage | Lotomayor | 502 | Debaixo da folha gigante dele as feridas fecham devagar. Viajantes fazem fila para descansar ali. |

### Zunzim → Melíria → Colmeira

- **Conceito:** Esqueleto de apicultora do mangue que cria abelhas de ferrão verde nas árvores do Pântano Verde-Musgo.
- **Silhueta:** Chapéu de aba larga com véu de tela que cresce a cada estágio; no último, uma colmeia inteira no alto da cabeça.
- **Arco de crescimento:** Bebê abraçado a um pote de mel maior que o crânio → Adolescente de chapéu com véu e fumegador na mão → Adulta com a colmeia presa no alto da cabeça e um manto de favos.
- **Personalidade:** Doce, protetora, zangada. **No mapa:** rápido.
- **Tipo:** Veneno · **Raridade:** incomum · **Cresce aos** 32 e 54 anos
- **Golpe assinatura:** Enxame / Swarm / Enjambre

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 050 | Bebê | Zunzim | Buzzlet | Zumbito | 281 | Rouba mel e lambe o pote até brilhar. As abelhas fingem que não viram. |
| 051 | Adolescente | Melíria | Honeyveil | Mielina | 392 | Acalma o enxame com fumaça e cantoria. Quem mexe na colmeia conhece o ferrão verde. |
| 052 | Adulto | Colmeira | Hivequeen | Colmenara | 502 | Leva a colmeia na cabeça e chama cada abelha pelo nome. O mel dela cura; o ferrão, nem tanto. |

## Cidade Murada de Ossório

### Tampinha → Broquel → Bastião

- **Conceito:** Esqueleto de sentinela da muralha de Ossório, que nunca saiu do posto, nem depois de virar esqueleto.
- **Silhueta:** Escudo à esquerda que cresce de tampa de panela até um escudo-portão que cobre metade do corpo; lança com bandeira à direita.
- **Arco de crescimento:** Bebê com uma tampa de panela de escudo → Adolescente de elmo com escudo de torre → Adulto com um escudo-portão gigante e lança com bandeira de Ossório.
- **Personalidade:** Disciplinado, rígido, fiel. **No mapa:** patrulha.
- **Tipo:** Físico · **Raridade:** comum · **Cresce aos** 34 e 58 anos
- **Golpe assinatura:** Muralha Viva / Living Wall / Muralla Viva

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 055 | Bebê | Tampinha | Liddle | Tapita | 262 | Bate continência para tudo que passa, inclusive para pombos. |
| 056 | Adolescente | Broquel | Bulwarkin | Rodelón | 372 | Dorme de pé, encostado no escudo. Acorda com um único ruído estranho. |
| 057 | Adulto | Bastião | Bastionel | Baluartón | 482 | O escudo dele já foi o portão de uma torre. Enquanto ele estiver de pé, a muralha não cai. |

### Rabisquim → Escrivélio → Pergamor

- **Conceito:** Esqueleto de escriba dos arquivos de Ossório, que copia leis e feitiços sem parar.
- **Silhueta:** Pena de escrever enorme apontando para cima; um livro aberto flutuando; o adulto tem uma capa de pergaminhos e tinteiro como coroa.
- **Arco de crescimento:** Bebê com uma pena de escrever espetada na cabeça → Adolescente com um livro aberto flutuando diante dele → Adulto com capa de pergaminhos e um tinteiro como coroa.
- **Personalidade:** Meticuloso, reservado, sabichão. **No mapa:** tímido (foge).
- **Tipo:** Mágico · **Raridade:** raro · **Cresce aos** 38 e 62 anos
- **Golpe assinatura:** Decreto Selado / Sealed Decree / Decreto Sellado

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 058 | Bebê | Rabisquim | Scribbit | Garabatín | 300 | Escreve no ar com a pena da cabeça. Nunca termina uma frase. |
| 059 | Adolescente | Escrivélio | Quillian | Plumario | 412 | O livro que o segue registra tudo o que ele vê. Inclusive o que você disse dele. |
| 060 | Adulto | Pergamor | Tomeward | Pergaminor | 522 | Cada pergaminho da capa é uma lei antiga de Ossório. Quando lê uma em voz alta, ela acontece. |

### Tilintim → Badaleiro → Carrilhão

- **Conceito:** Esqueleto de sineiro da torre de Ossório, cujas badaladas acalmam e curam quem as ouve.
- **Silhueta:** Sino como peça central que cresce: sininho no pescoço, sino de mão erguido, e um sino enorme nas costas como uma carapaça.
- **Arco de crescimento:** Bebê com um sininho no pescoço → Adolescente erguendo um sino de mão grande → Adulto com um sino de torre nas costas como uma carapaça e um badalo-cajado.
- **Personalidade:** Pontual, alegre, surdo de um lado. **No mapa:** ronda em círculo.
- **Tipo:** Cura/Suporte · **Raridade:** incomum · **Cresce aos** 34 e 58 anos
- **Golpe assinatura:** Badalada Serena / Serene Toll / Campanada Serena

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 061 | Bebê | Tilintim | Dingle | Tilín | 281 | O sininho toca a cada passo, então nunca consegue se esconder. |
| 062 | Adolescente | Badaleiro | Clapperton | Badajo | 392 | Toca o sino na hora certa, todos os dias. A cidade acerta os relógios por ele. |
| 063 | Adulto | Carrilhão | Carillon | Carillón | 502 | O sino das costas ressoa por dentro dos ossos. Uma badalada acalma uma briga inteira. |

### Caquinho → Vitralho → Rosáceo

- **Conceito:** Esqueleto de vitralista que conserta os vitrais da Cidade Murada de Ossório e prende a luz em cacos coloridos.
- **Silhueta:** Caco de vidro colorido que cresce até virar uma rosácea redonda atrás da cabeça, como uma auréola de vitral.
- **Arco de crescimento:** Bebê com um caco de vidro azul usado como óculos → Adolescente de avental de couro com um painel de vitral nas costas → Adulta com uma rosácea inteira brilhando atrás do crânio e um manto que muda de cor com a luz.
- **Personalidade:** Sonhadora, meticulosa, vaidosa. **No mapa:** ronda em círculo.
- **Tipo:** Mágico · **Raridade:** incomum · **Cresce aos** 36 e 60 anos
- **Golpe assinatura:** Luz de Vitral / Stained Light / Luz de Vidriera

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 064 | Bebê | Caquinho | Shardling | Cristalín | 281 | Olha o mundo através de um caco azul. Jura que assim tudo fica mais bonito. |
| 065 | Adolescente | Vitralho | Paneglow | Vitralito | 392 | Conserta vitrais de madrugada. Quando o sol bate, assina o trabalho em arco-íris. |
| 066 | Adulto | Rosáceo | Roseglass | Rosetón | 502 | A rosácea nas costas guarda a luz de mil manhãs. Quando ela brilha, as sombras pedem licença. |

## Picos Gelados

### Mochilim → Cargueiro → Alpinor

- **Conceito:** Esqueleto de carregador de montanha que leva mantimentos aos refúgios dos Picos Gelados.
- **Silhueta:** Mochila cada vez mais alta que o próprio corpo; no adulto, uma cargueira do tamanho de uma casinha e um cajado de gelo.
- **Arco de crescimento:** Bebê de cachecol com uma mochilinha → Adolescente com uma mochila alta cheia de panelas e um piolet → Adulto com uma cargueira enorme nas costas e um cajado de gelo.
- **Personalidade:** Incansável, quieto, confiável. **No mapa:** patrulha.
- **Tipo:** Físico · **Raridade:** comum · **Cresce aos** 40 e 64 anos
- **Golpe assinatura:** Avalanche de Carga / Cargo Avalanche / Alud de Carga

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 069 | Bebê | Mochilim | Packlet | Mochilín | 262 | Leva na mochila uma pedra de estimação. Diz que é para treinar. |
| 070 | Adolescente | Cargueiro | Haulster | Cargadón | 372 | As panelas da mochila batem no ritmo dos passos. É assim que os refúgios sabem que a sopa está chegando. |
| 071 | Adulto | Alpinor | Summitor | Cumbrero | 482 | Já subiu todos os picos com a casa nas costas. Quando para, monta um abrigo para quem precisar. |

### Gelinho → Cinzelvo → Cristalor

- **Conceito:** Esqueleto de escultor de gelo dos Picos Gelados, que talha estátuas no gelo eterno com um cinzel.
- **Silhueta:** Cubo de gelo na cabeça; o adolescente ganha asas de gelo esculpidas; o adulto vira cristal, com coroa de pingentes.
- **Arco de crescimento:** Bebê com um cubo de gelo de capacete e um cinzelzinho → Adolescente com asas de gelo que esculpiu para si mesmo → Adulto com armadura cristalina e coroa de pingentes de gelo.
- **Personalidade:** Perfeccionista, frio, sensível. **No mapa:** rápido.
- **Tipo:** Mágico · **Raridade:** incomum · **Cresce aos** 40 e 64 anos
- **Golpe assinatura:** Estátua de Gelo / Ice Statue / Estatua de Hielo

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 072 | Bebê | Gelinho | Cubbit | Hielito | 281 | Esculpe bonecos de neve parecidos com quem encontra. Os bonecos sempre saem sorrindo. |
| 073 | Adolescente | Cinzelvo | Chiselle | Cincelón | 392 | Esculpiu as próprias asas e ainda não aprendeu a voar com elas. Plana nas descidas. |
| 074 | Adulto | Cristalor | Glacior | Glaciarco | 502 | Transformou o próprio corpo em escultura. A luz que atravessa o cristal congela o que toca. |

### Xicrim → Chaleirel → Samovarão

- **Conceito:** Esqueleto de estalajadeiro de um refúgio dos picos, que serve chá quente a viajantes congelados.
- **Silhueta:** Xícara virada na cabeça; chaleira fumegante com cobertor nos ombros; samovar redondo e alto nas costas soltando vapor.
- **Arco de crescimento:** Bebê com uma xícara na cabeça → Adolescente enrolado num cobertor, com uma chaleira fumegante → Adulto com um samovar nas costas soltando vapor curativo.
- **Personalidade:** Acolhedor, lento, hospitaleiro. **No mapa:** tímido (foge).
- **Tipo:** Cura/Suporte · **Raridade:** raro · **Cresce aos** 44 e 68 anos
- **Golpe assinatura:** Chá de Abrigo / Shelter Tea / Té de Refugio

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 075 | Bebê | Xicrim | Cuplet | Tacita | 300 | Usa a xícara de chapéu e oferece chá imaginário a quem passa. |
| 076 | Adolescente | Chaleirel | Kettleby | Teterón | 412 | A chaleira dele assobia quando alguém por perto está com frio. |
| 077 | Adulto | Samovarão | Samovaron | Samovarón | 522 | O vapor do samovar derrete a neve num raio de dez passos. Nenhum viajante congela perto dele. |

## Deserto dos Ecos

### Ferrim → Escorpeiro → Aguilhão

- **Conceito:** Esqueleto de domador de escorpiões das caravanas do Deserto dos Ecos.
- **Silhueta:** Cauda curva com ferrão sobre a cabeça em todos os estágios: de pano, depois um escorpião no ombro, e no adulto um escorpião gigante unido às costas.
- **Arco de crescimento:** Bebê com uma cauda de escorpião de pano presa no capuz → Adolescente com um escorpião vivo no ombro e um chicote → Adulto unido a um escorpião gigante de areia, com o ferrão sobre a cabeça.
- **Personalidade:** Ousado, exibido, ágil. **No mapa:** persegue o jogador.
- **Tipo:** Veneno · **Raridade:** comum · **Cresce aos** 44 e 68 anos
- **Golpe assinatura:** Ferrão das Dunas / Dune Sting / Aguijón de Dunas

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 080 | Bebê | Ferrim | Stingle | Aguijín | 262 | Finge que a cauda de pano é de verdade e ameaça os outros com ela. |
| 081 | Adolescente | Escorpeiro | Whipclaw | Alacranero | 372 | O escorpião do ombro obedece ao estalo do chicote. Na verdade, quem manda é o escorpião. |
| 082 | Adulto | Aguilhão | Venomarch | Aguijonazo | 482 | Já não se sabe onde termina o domador e começa o escorpião. Ataca antes da areia assentar. |

### Bussolito → Lunetário → Astrolar

- **Conceito:** Esqueleto de cartógrafo do Deserto dos Ecos, que mapeia as dunas ouvindo os ecos.
- **Silhueta:** Instrumento redondo sempre à frente: bússola gigante, depois luneta e rolo de mapa, e no adulto um astrolábio girando em volta do corpo com capa de mapas.
- **Arco de crescimento:** Bebê abraçado a uma bússola gigante → Adolescente com uma luneta e um rolo de mapa debaixo do braço → Adulto com um astrolábio girando em volta dele e uma capa feita de mapas.
- **Personalidade:** Curioso, distraído, preciso. **No mapa:** tímido (foge).
- **Tipo:** Mágico · **Raridade:** raro · **Cresce aos** 48 e 70 anos
- **Golpe assinatura:** Rota dos Ecos / Echo Route / Ruta de Ecos

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 083 | Bebê | Bussolito | Compip | Brujulín | 300 | A bússola dele aponta para o lanche mais próximo, não para o norte. |
| 084 | Adolescente | Lunetário | Scopewright | Catalejón | 412 | Mede as dunas gritando e escutando o eco. Os mapas dele mudam toda vez que venta. |
| 085 | Adulto | Astrolar | Astrolux | Astrolario | 522 | O astrolábio gira em volta dele e mostra caminhos que ainda não existem. Nunca se perdeu. |

### Tambim → Batucão → Ecoarca

- **Conceito:** Esqueleto de tamborileiro das caravanas, cujo ritmo mantém os viajantes de pé no calor do deserto.
- **Silhueta:** Tambor como barriga; o adolescente tem tambores pendurados e baquetas erguidas; o adulto, um grande tambor de dunas nas costas e faixas esvoaçando.
- **Arco de crescimento:** Bebê com um tamborzinho preso na barriga → Adolescente com tambores pendurados e duas baquetas erguidas → Adulto com um grande tambor de dunas nas costas e faixas coloridas ao vento.
- **Personalidade:** Animado, rítmico, incansável. **No mapa:** ronda em círculo.
- **Tipo:** Cura/Suporte · **Raridade:** incomum · **Cresce aos** 44 e 68 anos
- **Golpe assinatura:** Ritmo da Caravana / Caravan Rhythm / Ritmo de Caravana

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 086 | Bebê | Tambim | Drumlet | Tamborín | 281 | Toca a barriga como tambor quando está feliz. Fica feliz com muita facilidade. |
| 087 | Adolescente | Batucão | Bongard | Batucón | 392 | Marca o passo das caravanas. Quando ele toca, ninguém sente cansaço. |
| 088 | Adulto | Ecoarca | Echoarch | Resonarca | 502 | O tambor das dunas ecoa por quilômetros. Quem ouve recupera o fôlego, amigo ou inimigo. |

### Barrico → Rodaleiro → Urnadão

- **Conceito:** Esqueleto de oleiro do Deserto dos Ecos que molda jarras com a areia molhada do oásis.
- **Silhueta:** Jarro de barro sempre presente e crescendo: no colo, depois equilibrado na cabeça, por fim uma urna enorme presa às costas como um casco.
- **Arco de crescimento:** Bebê sujo de barro abraçando um potinho torto → Adolescente de avental com uma jarra equilibrada na cabeça → Adulto de turbante com uma urna gigante nas costas, as rachaduras remendadas a ouro.
- **Personalidade:** Paciente, teimoso, caprichoso. **No mapa:** patrulha.
- **Tipo:** Físico · **Raridade:** comum · **Cresce aos** 46 e 70 anos
- **Golpe assinatura:** Jarro Pesado / Heavy Jar / Tinaja Pesada

| Nº | Estágio | PT-BR | EN | ES | Total | Entrada do Ossário (PT-BR) |
|---|---|---|---|---|---|---|
| 089 | Bebê | Barrico | Claylet | Barrito | 262 | Faz potes tortos e diz que é de propósito. Fica emburrado se alguém pisa no barro dele. |
| 090 | Adolescente | Rodaleiro | Spinpot | Tornero | 372 | Gira a roda de oleiro o dia inteiro. Diz que o deserto é só barro esperando água. |
| 091 | Adulto | Urnadão | Urnstone | Tinajón | 482 | Carrega uma urna que guarda o eco de cada caravana perdida. Remenda as rachaduras com ouro. |

## Únicos e Rei

Não crescem. Aparecem uma vez por região (a partir do Bosque) e no Castelo.

### 025 · Raizerno / Elderoot / Raizeño
- **Conceito:** Esqueleto de um eremita tão velho que se fundiu à árvore mais antiga do Bosque das Raízes.
- **Silhueta:** Tronco largo com raízes no lugar das pernas e galhos no lugar dos braços; crânio no meio do tronco.
- **Personalidade:** Ancestral, paciente, lento. **No mapa:** patrulha.
- **Tipo:** Cura/Suporte · **Região:** Bosque das Raízes
- **Ossário:** Dizem que plantou o Bosque inteiro com uma semente só. Mexe-se uma vez por estação.

### 039 · Vagonauta / Cartwraith / Vagonero
- **Conceito:** Esqueleto de capataz que nunca saiu do vagonete e corre pelos trilhos abandonados das minas.
- **Silhueta:** Vagonete de mina com rodas; o esqueleto de capacete com lanterna saindo de dentro, braços para frente.
- **Personalidade:** Afobado, mandão, veloz. **No mapa:** rápido.
- **Tipo:** Físico · **Região:** Minas de Cinzas
- **Ossário:** Corre pelos trilhos à noite dando ordens a mineiros que já se foram. O vagonete nunca descarrila.

### 053 · Brumaga / Fogmara / Brumaja
- **Conceito:** Esqueleto de bruxa da névoa que mora no coração do pântano e cozinha brumas venenosas.
- **Silhueta:** Chapéu pontudo torto e longo, manto em farrapos se desfazendo em névoa, colher de pau gigante.
- **Personalidade:** Misteriosa, irônica, solitária. **No mapa:** tímido (foge).
- **Tipo:** Veneno · **Região:** Pântano Verde-Musgo
- **Ossário:** A névoa do pântano sai do caldeirão dela. Quando ri, o pântano inteiro fica mais denso.

### 067 · Bufardo / Jestrel / Bufonel
- **Conceito:** Esqueleto de bobo da corte de Ossório que comanda marionetes com fios mágicos.
- **Silhueta:** Chapéu de bobo de três pontas com guizos; cruzeta de marionete erguida com um bonequinho pendurado.
- **Personalidade:** Debochado, imprevisível, teatral. **No mapa:** rápido.
- **Tipo:** Mágico · **Região:** Cidade Murada de Ossório
- **Ossário:** As marionetes dele imitam quem as olha. Algumas imitam bem demais.

### 078 · Nevasco / Blizzabbot / Nevadón
- **Conceito:** Esqueleto de monge das neves que medita no pico mais alto, coberto por um manto de pelo branco.
- **Silhueta:** Manto peludo branco e largo em forma de montanha; contas de oração; cabeça raspada pequena no topo.
- **Personalidade:** Sábio, silencioso, bondoso. **No mapa:** patrulha.
- **Tipo:** Cura/Suporte · **Região:** Picos Gelados
- **Ossário:** Medita há tanto tempo que a neve se acumula nos ombros sem derreter. Uma palavra dele acalma tempestades.

### 092 · Ampulhor / Sandkeeper / Arenario
- **Conceito:** Esqueleto de guardião das ampulhetas dos templos do Deserto dos Ecos, que mede o tempo em areia.
- **Silhueta:** Toucado de faixas listradas até os ombros; ampulheta grande flutuando acima da mão erguida.
- **Personalidade:** Solene, impaciente, antigo. **No mapa:** patrulha.
- **Tipo:** Mágico · **Região:** Deserto dos Ecos
- **Ossário:** Vira a ampulheta e a batalha fica mais lenta para todos, menos para ele.

### 094 · Degustor / Tastrel / Catadón
- **Conceito:** Esqueleto do provador oficial do Rei, que provou tantos pratos envenenados que virou o próprio veneno.
- **Silhueta:** Gola alta de corte e uma bandeja coberta (cloche) erguida numa mão; guardanapo no braço.
- **Personalidade:** Refinado, desconfiado, ácido. **No mapa:** persegue o jogador.
- **Tipo:** Veneno · **Região:** Castelo do Rei Esqueleto
- **Ossário:** Provou cada prato do Rei por cem anos. Hoje é ele quem tempera os inimigos do castelo.

### 026 · Troncudo / Timberlord / Troncazo
- **Conceito:** O parceiro do Guardião Ramalho: um lenhador gigante que carrega um tronco inteiro no ombro e grita "madeira!" antes de cada golpe.
- **Silhueta:** Tronco atravessado nos ombros, mais largo que o corpo; barba de musgo pendurada no queixo.
- **Personalidade:** Barulhento, leal, exibido. **No mapa:** persegue o jogador.
- **Tipo:** Físico · **Região:** Bosque das Raízes
- **Ossário:** Avisa antes de bater, por educação. Depois bate do mesmo jeito.

### 040 · Bigornão / Anvilord / Yunquero
- **Conceito:** O parceiro da Tia Fornalha: um guarda de forja com uma bigorna no lugar do peito, que aguenta qualquer pancada.
- **Silhueta:** Bigorna de ferro presa ao peito e luvas enormes de couro; anda curvado com o peso.
- **Personalidade:** Firme, calado, protetor. **No mapa:** patrulha.
- **Tipo:** Físico · **Região:** Minas de Cinzas
- **Ossário:** Serviu de bigorna para a Tia por cem anos. Nunca reclamou de uma martelada.

### 054 · Caldeirona / Cauldrona / Calderona
- **Conceito:** A parceira da Musga: uma cozinheira do brejo com um caldeirão fumegante no lugar da barriga, que tanto envenena quanto cura.
- **Silhueta:** Caldeirão redondo no tronco soltando vapor verde; concha de sopa na mão.
- **Personalidade:** Fofoqueira, maternal, imprevisível. **No mapa:** tímido (foge).
- **Tipo:** Veneno · **Região:** Pântano Verde-Musgo
- **Ossário:** Ninguém sabe o que tem na sopa dela. Ela também não, e é isso que a deixa feliz.

### 068 · Bandeirão / Bannerguard / Banderón
- **Conceito:** O parceiro do Comandante Caliço: um porta-estandarte que ergue a bandeira de Ossório e faz os aliados lutarem no mesmo compasso.
- **Silhueta:** Mastro alto com uma bandeira azul tremulando acima da cabeça; elmo com penacho.
- **Personalidade:** Honrado, solene, inspirador. **No mapa:** patrulha.
- **Tipo:** Cura/Suporte · **Região:** Cidade Murada de Ossório
- **Ossário:** Enquanto a bandeira está de pé, ninguém do lado dele recua. Ele nunca deixou a bandeira cair.

### 079 · Patinora / Glidefrost / Patinieve
- **Conceito:** A parceira de Alva: uma patinadora que dança sobre o gelo do Jardim e congela o tempo a cada pirueta.
- **Silhueta:** Saia rodada de gelo e patins de lâmina; braços abertos em pose de giro.
- **Personalidade:** Graciosa, melancólica, veloz. **No mapa:** rápido.
- **Tipo:** Mágico · **Região:** Picos Gelados
- **Ossário:** Dança sozinha no lago congelado esperando uma música que nunca toca. Gira tão rápido que o frio a segue.

### 093 · Miragina / Mirageen / Espejina
- **Conceito:** A parceira da Rainha Duna: uma dançarina de miragens que troca de lugar com o próprio reflexo e cura quem dança com ela.
- **Silhueta:** Véus longos flutuando em volta e um espelho redondo de bronze nas mãos.
- **Personalidade:** Serena, misteriosa, gentil. **No mapa:** patrulha.
- **Tipo:** Cura/Suporte · **Região:** Deserto dos Ecos
- **Ossário:** Ninguém sabe se a viu de verdade ou só o reflexo. Dizem que as duas são boa gente.

### 095 · Ossárion / Ossarion / Osarión
- **Conceito:** O Rei Esqueleto, senhor do castelo, que dominou o continente e guarda o segredo de 2040.
- **Silhueta:** Coroa alta de pontas, manto real com gola de pele até o chão, cetro com orbe; o maior sprite do jogo.
- **Personalidade:** Solitário, imponente, ferido. **No mapa:** patrulha.
- **Tipo:** Mágico · **Região:** Castelo do Rei Esqueleto
- **Ossário:** O Rei Esqueleto. A coroa dele pesa mais do que deveria, e ninguém nunca perguntou por quê.
