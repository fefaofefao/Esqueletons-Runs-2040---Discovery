# AGENTS.md — RPG mobile "Esqueletons Runs 2040 — Edição Discovery"

> Especificação completa do jogo para o **Codex**. Este arquivo fica na raiz do repositório e vale para todas as tarefas. Siga as fases da seção 16, em ordem, uma por tarefa.

---

## A. Como trabalhar neste repositório (Codex)

- **Uma fase ou subfase por tarefa.** Antes de codar, leia este arquivo inteiro, o `PROGRESS.md` e o `docs/DECISOES.md`. Ao terminar, atualize o `PROGRESS.md` com o que foi feito, o que falta e as decisões tomadas.
- **Não pare para pedir decisões técnicas.** Escolha a melhor opção, registre em `docs/DECISOES.md` e siga em frente. Só pergunte se algo desta especificação for contraditório.
- **Verificação obrigatória ao fim de cada tarefa:**
  - Importação e testes do Godot em modo headless.
  - `tools/validate_data.py` sem erros (seção 12).
  - `tools/simulate.py` dentro das metas, a partir da fase 3c (seção 11).
  - APK de debug gerado pelo GitHub Actions.
  - Se o ambiente não tiver Godot, Android SDK ou rede, crie o `tools/setup_codex.sh`, deixe a validação para o CI e avise no resumo.
- **Commits** pequenos, com mensagens claras em português. Nunca faça commit de keystore, senhas ou IDs reais do AdMob: use GitHub Secrets.
- **Resumo final de cada tarefa:** o que mudou, a **ficha de revisão** (seção 13) e as pendências.

## B. Regra de ouro sobre qualidade de conteúdo

O maior risco deste projeto é a IA gerar **conteúdo genérico**: esqueletos sem identidade, nomes repetitivos, diálogos vazios e balanceamento no chute. Todas as regras das seções 8, 10 e 11 existem para impedir isso.

Se uma regra de qualidade não puder ser cumprida, **não entregue conteúdo de preenchimento**. Entregue menos, marque como pendente e explique o motivo.

---

## C. Decisões do Fernando (valem por cima do texto abaixo)

Registradas na ordem em que chegaram. Em caso de conflito com as seções seguintes, **vale o que está aqui**.

1. **Nome:** *Esqueletons Runs 2040 — Edição Discovery*, primeiro jogo de uma série. Produtora FSamp Labs.
2. **Tela inicial e logo em alta resolução** (não pixel art), com cara de abertura de série.
3. **Nível = idade.** O jogo chama o nível de **idade**: cada nível ganho é um **aniversário** ("fez 13 anos!"). Ao atingir a idade de crescimento, o esqueleto cresce para o estágio seguinte. Isso faz parte da lore e do desenvolvimento.
   - **Idade máxima 100**; o **chefe final (Rei Esqueleto) tem 120**.
   - Estágio 1 = **bebê** (pequeno), estágio 2 = **adolescente**, estágio 3 = **adulto em força total**.
   - As metas de nível da seção 11 passam a ser idades (escala ×2): ver a tabela da seção 11.
4. **Os 6 Guardiões são parentes do Rei Esqueleto.** Quanto mais perto do Rei (na história e no mapa), mais difícil o líder e os capangas. Quem viaja de cidade em cidade é o **jogador**. Detalhes em `docs/roteiro/00_notas_do_fernando.md`.
5. **A batalha não pode parecer Pokémon.** Deve ser inovadora: ver `docs/DECISOES.md` (timeline por tempo, peso dos golpes, atraso, Sintonia e arena lateral).
6. **Os dois iniciais entram juntos na equipe.** No Prólogo, Lia e Taro viram parceiros ao mesmo tempo (não há escolha entre eles). Os dois são fixos e têm **+5% em todos os atributos** em relação aos demais esqueletos (`data/battle.json` → `starter.stat_bonus`). Os arcos dos dois avançam em todas as regiões. Isso substitui o "parceiro escolhido + recorrente" da seção 6.

---

## 0. Regras gerais

- Você é o desenvolvedor líder. O Fernando delega as decisões técnicas e espera tudo pronto para gerar o AAB e publicar, sem configuração manual que possa ser automatizada.
- **Gênero:** RPG de coleta de monstros, com a era GBA do gênero como referência: exploração top-down, batalhas por turno, recrutamento, níveis e crescimento. Todo o conteúdo deve ser **100% original**, incluindo personagens, nomes, sprites, sons, textos e UI. Não use nomes, sprites, sons, fontes, logos ou telas de jogos existentes. Não mencione marcas de terceiros no código, no jogo ou na ficha da loja.
- **Visual "GBA aprimorado":** pixel art com o charme do GBA, porém mais rica. Isso inclui:
  - paleta ampliada e sombras suaves;
  - iluminação simples por região;
  - partículas (folhas, poeira, brilho);
  - água e grama animadas;
  - animações com mais quadros.
- **Assets:** pixel art própria ou packs **CC0** (ex.: Kenney). Registre a origem e a licença de cada um em `CREDITS.md`.
- **Dados em JSON:** monstros, golpes, NPCs, encontros, lojas e balanceamento ficam em arquivos JSON. Textos ficam em arquivos de tradução. Nada de conteúdo hardcoded.

## 1. Dados da publicação

Centralize tudo em **`config/publisher.json`**. Os campos de contato serão preenchidos depois pelo Fernando, então use placeholders e faça o jogo, a política de privacidade e o `PLAY_CONSOLE.md` lerem deste arquivo, ou gerarem a partir dele.

| Campo | Valor |
|---|---|
| Nome do jogo | Esqueletons Runs 2040 — Edição Discovery (1º jogo da série *Esqueletons Runs 2040*) |
| Produtora / desenvolvedor | FSamp Labs |
| Responsável | Fernando Martins Sampaio |
| E-mail de contato e suporte | fe.m.sampaio@hotmail.com |
| Site (app-ads.txt e política) | `[URL]` |
| Package name | `com.fsamplabs.esqueletonsruns2040.discovery` |
| Plataforma | Android / Google Play (AAB) |
| Monetização | Google AdMob (banner, intersticial, premiado) |
| Idiomas | Português (Brasil), Inglês, Espanhol |

Crie `tools/check_placeholders.py`, que **falha o build de release** se ainda houver algum `[PLACEHOLDER]`. O build de debug não é afetado.

## 2. Stack técnica

- **Godot 4**, versão estável mais recente (4.5+), com GDScript e renderer Compatibility.
- **Plugin AdMob para Godot 4** mantido ativamente, com **UMP SDK**.
- **Tela:** resolução base **320×180**, tiles de 16×16, escala inteira pixel-perfect e orientação **paisagem**.
- **Build:** **GitHub Actions** gera o AAB assinado (keystore via Secrets) e o APK de debug. Repositório privado na conta fefaofefao.
- **Android:** targetSdk 36 (mínimo 35), minSdk 24, compatível com **páginas de 16 KB**.
- **Save** local em `user://` (JSON, versionado para migração). Sem login, sem servidor e sem coleta própria de dados.

## 3. Idiomas (PT-BR, EN, ES)

- Use o sistema de tradução do Godot com CSV ou PO em `i18n/`. **Todo texto visível usa chave**, nunca string literal. Isso inclui nomes de esqueletos, golpes, itens e NPCs, diálogos, UI e mensagens de anúncio.
- **Idioma inicial:** o do aparelho, com fallback para inglês. O jogador troca nas Configurações a qualquer momento, sem reiniciar.
- **Fonte pixel** com suporte a acentos, ç, ñ, ¿ e ¡, testada nos três idiomas.
- **Layout:** caixas de diálogo e menus aceitam até **30% de texto a mais**, porque o espanhol tende a ser mais longo. Há quebra automática de linha e um teste que detecta overflow.
- **Nomes de esqueletos:** cada idioma tem nome próprio, adaptado como trocadilho e não traduzido literalmente. O nome precisa soar natural nos três idiomas.
- **Qualidade da tradução:** tradução natural e localizada, não literal. Expressões e piadas são adaptadas. PT-BR é o idioma de origem.
- `tools/validate_data.py` verifica se **toda chave existe nos 3 idiomas**, sem textos vazios ou iguais ao PT por esquecimento.
- Loja e documentos também saem nos 3 idiomas: ficha da Play Store (título, descrição curta, descrição longa) e política de privacidade.

## 4. Controles

- **D-pad virtual** (4 direções) à esquerda e botões **A** e **B** à direita. Ficam semitransparentes, com área de toque mínima de 48dp e sem sobreposição com anúncios.
- **A:** confirmar, interagir ou avançar. **B:** voltar ou cancelar; segurar B no mapa faz correr.
- Botão **MENU** e botão **⏩ 2x** no topo.
- Suporte a gamepad Bluetooth e teclado.
- O botão voltar do Android funciona como B; no mapa, abre a pausa.

## 5. Fast forward 2x

- O botão alterna entre 1x e 2x (`Engine.time_scale`), e o estado fica salvo. O ícone sempre mostra o estado atual.
- **Afeta:** caminhada, animações de mapa e batalha, texto, transições e animações de crescimento.
- **Não afeta:** a resposta dos menus e os cronômetros de anúncios.

## 6. História (≈3 horas)

### Premissa
Um rapaz do ano **2040** acorda numa praia. O velho pescador **Bento** explica que o continente foi dominado por esqueletos e que o **Rei Esqueleto** está por trás disso. O jogador nomeia o protagonista.

### Parceiro inicial
Dois jovens esqueletos se apresentam:
- **Lia:** órfã de pais, procura um parceiro. Tipo **Mágico**.
- **Taro:** pais desaparecidos, procura um parceiro. Tipo **Físico**.

O escolhido vira o parceiro fixo e não pode ser liberado. O outro se torna **personagem recorrente**, aliado e rival amistoso, com batalhas opcionais. O destino dos pais de Taro se conecta ao Rei Esqueleto, seja qual for a escolha.

### Estrutura
| Ato | Região | Duração | Destaque |
|---|---|---|---|
| Prólogo | Praia do Despertar + Vila Maré | 15 min | Tutorial, escolha do parceiro, 1ª batalha, marcador |
| 1 | Bosque das Raízes | 25 min | 1º Guardião |
| 2 | Minas de Cinzas | 25 min | 2º Guardião, item de travessia |
| 3 | Pântano Verde-Musgo | 25 min | 3º Guardião (Veneno) |
| 4 | Cidade Murada de Ossório | 25 min | 4º Guardião, revelação sobre 2040 |
| 5 | Picos Gelados | 25 min | 5º Guardião, reencontro com Lia/Taro |
| 6 | Deserto dos Ecos | 25 min | 6º Guardião |
| Final | Castelo do Rei Esqueleto | 20 min | Sequência de chefes, luta final |
| Pós-jogo | Mundo livre | — | Usar o Rei, completar o Ossário e as casas de domadores |

### Cidades
Toda cidade tem obrigatoriamente:
- **Rancho:** cura gratuita e armazenamento dos parceiros excedentes, onde o jogador monta o time de 4.
- **Loja:** estoque que melhora a cada cidade.
- **2 ou 3 casas de domadores:** batalhas opcionais com **boas recompensas** (moedas, itens raros, golpes, bônus de marcador). Cada casa é vencida uma vez.
- **3 a 6 NPCs** e **1 ou 2 missões secundárias**.

### Escolhas e finais
- Há pelo menos 3 decisões relevantes que mudam diálogos, recompensas e recrutas disponíveis.
- Elas levam a **2 finais**: derrotar ou redimir o Rei Esqueleto.
- Mistério central: por que o protagonista veio de 2040, resolvido no final.

### Classificação
Fantasia leve, **sem sangue**, sem violência realista e sem linguagem imprópria.

## 7. Mapa, rotas e encontros

- Mapa top-down em grade, nas 4 direções, com colisões, portas e transições com fade.
- **Esqueletos selvagens visíveis**: patrulham dentro de um **raio** em torno do ponto de spawn e iniciam a batalha **ao encostar** no jogador. Não há encontros invisíveis. Depois de derrotados, reaparecem quando o jogador sai e volta à área.
- **Tabelas de encontro em JSON:** espécie, **estágio**, faixa de nível e raridade.
- **Progressão do mundo:** no início aparecem só esqueletos de estágio 1. Com o avanço da história surgem estágios 2 e 3 de nível mais alto. O estágio é sempre coerente com o nível de crescimento da espécie.
- **Domadores** (NPCs que controlam esqueletos) têm cone de visão. Ao ver o jogador, vão até ele e batalham, uma única vez.

### Rotas entre cidades
Cada rota entre cidades tem **2 ou 3 caminhos** que se reencontram antes da próxima cidade:
- **Caminho dos Domadores:** mais NPCs, com batalhas obrigatórias se o jogador for avistado. Rende mais moedas e itens, e as equipes são fixas e mais fortes.
- **Caminho Selvagem:** mais esqueletos selvagens. Rende mais XP e marcadores, e é possível desviar dos inimigos.
- **Atalho** (em algumas rotas): curto e escondido. Exige um item-chave ou tem poucos inimigos fortes.

Regras dos caminhos:
- Eles são sinalizados por placas e por um NPC que dá dicas.
- São equilibrados: **nenhum é obrigatório** para concluir a história.
- É possível desviar de parte dos inimigos com boa leitura do mapa.

## 8. Esqueletos: espécies, crescimento e Golden

### Composição (80 espécies no Ossário, cada estágio conta como uma)
- **24 linhas de 3 estágios = 72.** Lia e Taro estão entre elas.
- **7 únicos/raros**, que não crescem.
- **1 Rei Esqueleto** (nº 80).

### Bíblia de criaturas — obrigatória ANTES de criar sprites ou dados
Primeiro, gere o `docs/BESTIARIO.md`. Cada **linha** tem uma ficha com:

1. **Conceito em uma frase**, ligado ao mundo: profissão ou papel em vida, objeto característico e habitat da região. Exemplos: "esqueleto de mineiro que carrega uma lanterna de cristal", "esqueleto de lavadeira do pântano com cesto de ervas venenosas".
2. **Silhueta distinta**: descreva o formato que o diferencia dos outros a 32×32 pixels (chapéu, ferramenta, postura, tamanho). Duas linhas não podem ter silhuetas parecidas.
3. **Arco de crescimento**: o que muda de Bebê para Adolescente e de Adolescente para Adulto, contando uma história visual de amadurecimento. Exemplo: o ajudante com balde vira mineiro com picareta, que vira mestre de minas com armadura de pedra. É **proibido** que um estágio seja só um recolor ou um aumento de tamanho.
4. **Personalidade** em 3 palavras e um **comportamento no mapa**: rápido, tímido, patrulha em círculo ou persegue o jogador.
5. **Tipo**, **região de origem**, **raridade** e **níveis de crescimento**.
6. **Golpe assinatura**, que só a linha aprende.
7. **Nomes nos 3 idiomas** e uma **entrada de Ossário** (máx. 2 frases) por estágio.

**Proibido:**
- nomes numerados ou descritivos ("Esqueleto de Fogo", "Ossinho 2");
- mais de 2 nomes que começam com "Oss-", "Cav-" ou o mesmo prefixo;
- linhas sem relação com a região onde aparecem;
- dois conceitos com a mesma profissão.

**Distribuição**: os 4 tipos em proporção parecida (6 linhas cada, com variação de ±1). Cada região apresenta 3 a 5 linhas novas.

**Revisão visual**: gere o `docs/bestiario_sheet.png`, uma grade com todos os sprites de mapa e de batalha lado a lado, para conferir a variedade de silhuetas e cores de uma só vez.

### Crescimento em 3 estágios
- Os estágios são **Bebê → Adolescente → Adulto** (ver seção C).
- As idades de crescimento são definidas **por linha** em JSON (ex.: 28/60 ou 36/72). Linhas raras crescem mais tarde.
- **Ao crescer:**
  - atributos maiores e sprite novo;
  - golpe exclusivo, quando houver;
  - o crescimento fica pendente e acontece **ao voltar ao mapa após a batalha**; se mais de um esqueleto crescer, um de cada vez.
- **Animação "Aniversário e Crescimento"**, feita no mapa:
  1. O controle é congelado e o esqueleto **aparece ao lado do jogador**, saindo do chão.
  2. Surgem **bolo com velas**, confetes e o balão "Feliz aniversário, [nome]!", com música curta. Ele sopra as velas.
  3. Brilho pulsante, com a silhueta alternando entre o estágio atual e o novo, acelerando até um flash.
  4. A nova forma é revelada com o texto "[nome] cresceu e virou [espécie]!".
  5. Se houver golpe novo, abre a tela de aprender golpe.
- A animação dura de 6 a 8 s em 1x e respeita o 2x. O botão A acelera o texto, mas não pula a revelação.

### Variante Golden (Dourada)
- **Aparição:** cada esqueleto **selvagem** tem **1 chance em 40** de surgir como **Golden**. Isso não vale para esqueletos de domadores, Guardiões nem para o Rei. A chance fica em JSON.
- **Implementação simples**: um único **shader de paleta dourada**, aplicado sobre o sprite normal de qualquer espécie e estágio, sem sprites novos. Ele tem:
  - mapeamento de luminância para uma rampa de dourado;
  - um brilho que percorre o sprite a cada 2 s;
  - partículas de faísca douradas.
- **No mapa:** o Golden pisca com faíscas e toca um som característico quando entra na tela, para que o jogador o perceba e vá atrás.
- **Na batalha:** entra com um jingle especial e mostra o selo "★ Golden" ao lado do nome. O nome ganha um sufixo localizado: "Dourado(a)", "Golden" e "Dorado(a)".
- **Atributos:** +10% em todos, para recompensar sem quebrar o balanceamento.
- **Marcador:** derrotar um Golden adiciona **+99%** ao marcador da espécie.
  - Se o marcador chegar a 100%, o recruta oferecido é a **versão Golden**.
  - Se ficar em 99%, a próxima vitória sobre aquela espécie, normal ou Golden, completa o marcador e oferece a **versão Golden**. O jogo guarda o "direito ao Golden" para aquela espécie.
- **Depois de recrutado**, continua Golden em todos os estágios de crescimento, porque o shader se aplica a qualquer sprite.
- **Ossário:** marca "Golden visto" e "Golden recrutado" separadamente e mostra a contagem de Goldens.
- **Testes:**
  - forçar Golden pelo menu de debug;
  - um teste estatístico que roda 100 mil encontros e confirma a taxa de 1/40 ±5%.

### Marcador de recrutamento
- Cada vitória sobre uma espécie aumenta o **marcador de ossos** dela, de +20% a +50% conforme a raridade e a diferença de nível (valores em JSON).
- **Em 100%:** o esqueleto pede para se juntar, com as opções Aceitar (A) e Recusar (B). Se o time estiver cheio, ele vai para o **Rancho**.
- O marcador fica visível no Ossário e na batalha.
- Guardiões e chefes não são recrutáveis.
- **Rei Esqueleto:** depois da batalha final, o marcador dele **enche para 100%** com uma cena especial e ele **vira parceiro** nos dois finais, com diálogo diferente em cada um. Em seguida vêm os créditos e o **pós-jogo livre**.

### Golpes e progressão
- **56 golpes:** 16 Físicos, 16 Mágicos, 12 de Cura/Suporte e 12 de Veneno. Cada golpe tem nome nos 3 idiomas, tipo, poder, precisão, PP, alvo e efeito.
- Cada esqueleto tem até 4 golpes e aprende novos por nível.
- **Idade máxima 100** (o Rei Esqueleto tem 120). A história termina com a equipe por volta dos **80–90 anos**. (Ver seção C.)
- **XP:** os participantes recebem 100% e as reservas, 50%.
- **Itens:** poções (P/M/G), antídoto, reviver e itens-chave.
- **Ossário:** mostra cada espécie como vista, derrotada, recrutada ou Golden, com o % de conclusão.

## 9. Sistema de batalha

- **Batalhas em dupla (2×2).** O time tem **4 esqueletos**: 2 em campo e 2 na reserva. Trocar custa o turno daquele esqueleto.
- Batalhas selvagens têm 1 ou 2 inimigos; chefes sempre vêm em 2. Só é possível fugir de selvagens, com chance baseada em VEL.
- **Menu inovador**, sem copiar o 2×2 clássico:
  - **Timeline de turnos** no topo.
  - **Menu em anel** ao redor do esqueleto ativo, com as opções Golpes, Trocar, Itens e Fugir.
  - **Prévia do golpe**: efetividade (Fraco/Normal/Forte), efeito e alvo, que é escolhido pelo D-pad.
  - Atalho **"Repetir último turno"**.
- **Tipos:** Físico usa ATQ contra DEF. Mágico usa MAG contra RES. Cura recupera PV, remove status ou dá buffs. Veneno aplica dano por turno durante 3 a 5 turnos, além de debuffs.
- **Vantagens** (em JSON): ×1,5 a favor e ×0,75 contra. Físico > Mágico > Veneno > Físico; Cura é neutro.
- **Atributos:** PV, ATQ, MAG, DEF, RES e VEL.
- **Dano:** `((2×Nível/5+2) × Poder × Ataque/Defesa)/50 + 2`, multiplicado pela vantagem de tipo, pelo bônus de mesmo tipo (×1,25), por uma variação de 0,85 a 1,0 e pelo crítico (×1,5, com 6,25% de chance).
- A ordem dos turnos segue a VEL, mas certos golpes têm prioridade.

## 10. Roteiro e diálogos — regras de qualidade

**Antes de implementar cada região**, escreva o `docs/roteiro/<regiao>.md` e implemente exatamente o que está nele. Cada roteiro deve conter:

1. **Problema local** da cidade, ligado à trama principal. Exemplo: as minas pararam porque os esqueletos mineiros obedecem ao Guardião. Nada de cidade sem motivo.
2. **Pista do mistério de 2040**: uma por região, seguindo uma lista de pistas definida no `docs/roteiro/00_arco.md`, escrito na fase 4a. As pistas devem fazer sentido em retrospecto no final.
3. **Momento de Lia ou Taro** (o parceiro e o recorrente), com uma evolução no arco emocional deles.
4. **Guardião**:
   - nome, personalidade, motivo para servir ao Rei;
   - **mecânica-tema** da equipe, que ensina algo ao jogador. Exemplo: o Guardião do pântano usa veneno e cura, para ensinar o uso de antídotos.
5. **Lista de NPCs**: nome, função (dica, humor, lore, missão, domador) e no máximo 3 falas cada. Cada NPC precisa ter **uma razão para existir**.
6. **Casas de domadores**: o dono, o tema da equipe dele e a recompensa.
7. **Escolhas e consequências** daquela região, em tabela.

**Regras de escrita:**
- Caixas de diálogo com até 3 linhas.
- Frases curtas, com vozes diferentes por personagem.
- Humor leve.
- **Proibido:** "Olá, viajante!", NPCs que só descrevem o lugar, explicações longas e diálogos repetidos entre NPCs.
- **Volume total:** 12 a 18 mil palavras em PT-BR para o jogo inteiro. Cada roteiro informa a contagem da sua região.

## 11. Balanceamento — com números, não no chute

**Metas em `data/balance.json`**, que o código e o simulador usam:

| Região | Idade esperada na chegada | Idade do Guardião (média) |
|---|---|---|
| Prólogo | 1–10 | — |
| Bosque | 10–18 | 22 |
| Minas | 22–30 | 34 |
| Pântano | 34–42 | 46 |
| Ossório | 46–54 | 58 |
| Picos | 58–66 | 70 |
| Deserto | 68–76 | 80 |
| Castelo | 80–86 | 88–92 (Rei: 120) |

- **Bandas de atributos totais por estágio:**
  - Bebê ≈ 250–320;
  - Adolescente ≈ 360–430;
  - Adulto ≈ 470–540;
  - únicos ≈ 450–520;
  - Rei ≈ 600.
- **Simulador `tools/simulate.py`** (ou em GDScript headless). Usa a fórmula real e os dados reais para simular uma jogada típica:
  - um jogador que segue o caminho mais curto, vence cerca de 70% dos selvagens que cruzam a rota e usa a equipe recrutada mais provável;
  - IA de golpe simples (melhor dano esperado, cura abaixo de 35% de PV).
- **O simulador deve reportar:**
  - o nível médio da equipe na chegada a cada Guardião;
  - a **taxa de vitória contra cada Guardião**, que deve ficar entre **60% e 85%** no nível esperado;
  - o **tempo estimado por região**: batalhas × duração média, mais caminhada e mais leitura a 180 palavras por minuto.
- **Critérios de aceite:**
  - tempo total entre **2h45 e 3h15** em 1x;
  - **sem grind obrigatório:** o nível esperado é atingível sem voltar para treinar;
  - nenhum golpe com uso maior que 30% na simulação, o que indicaria um golpe dominante;
  - nenhum tipo com taxa de vitória 20 pontos acima dos outros.
- Gere o `docs/BALANCEAMENTO.md` com as tabelas e o que foi ajustado. Repita a simulação ao fim de cada tarefa das fases 3c e 4.

## 12. Validação automática (`tools/validate_data.py`)

O script falha se encontrar:
- IDs duplicados ou referências quebradas;
- total de espécies diferente de 80;
- linha sem 3 estágios;
- níveis de crescimento fora de ordem;
- selvagem de estágio 2 ou 3 com nível abaixo do crescimento;
- atributos fora da banda do estágio;
- tipos desbalanceados (mais de ±1 linha);
- prefixo de nome repetido mais de 2 vezes;
- chave de tradução faltando, vazia ou não traduzida em EN ou ES;
- golpe assinatura repetido;
- cidade sem rancho, loja ou com menos de 2 casas de domadores;
- rota sem caminho alternativo.

## 13. Revisão humana facilitada

- **Menu de debug** (só no build de debug, aberto com 3 toques no logo):
  - teleportar para qualquer região;
  - definir nível e adicionar qualquer esqueleto;
  - forçar Golden e forçar crescimento;
  - velocidade 10x;
  - mostrar raios de patrulha e tabelas de encontro;
  - vencer a batalha instantaneamente;
  - ver o tempo de jogo por região.
- **Ficha de revisão:** ao fim de cada tarefa de conteúdo (3b e 4x), inclua no resumo um **roteiro de teste de até 10 minutos** para o Fernando: o que jogar, o que observar e 3 perguntas objetivas. Exemplo: "As 4 linhas do Bosque são fáceis de distinguir?".
- Mantenha o `docs/FEEDBACK.md`. O Fernando anota correções nele e a tarefa seguinte deve aplicá-las antes de qualquer outra coisa.

## 14. AdMob e conformidade (Google Play)

### Implementação
- O **UMP** (consentimento GDPR/LGPD) vem **antes** de inicializar o SDK de anúncios.
- O menu Configurações tem a opção **"Privacidade e anúncios"**, que reabre o formulário de consentimento.
- **IDs de teste** em debug e IDs reais só no release, via Secrets.
- `tagForChildDirectedTreatment` e `tagForUnderAgeOfConsent` seguem o público declarado.
- **Permissões:** apenas INTERNET, ACCESS_NETWORK_STATE e `com.google.android.gms.permission.AD_ID`.
- O jogo funciona 100% offline.

### Posicionamento
- **Banner:** só em telas de menu (pausa, Ossário, Rancho, loja). Nunca no mapa, na batalha ou perto de botões.
- **Intersticial:**
  - só após vencer uma batalha, ao voltar ao mapa;
  - no máximo 1 a cada 3 batalhas, com pelo menos 3 minutos de intervalo;
  - nada nos primeiros 10 minutos de jogo;
  - nunca na abertura do app, em diálogos, em cutscenes, antes de chefes ou durante a animação de crescimento;
  - sempre pré-carregado.
- **Premiado:** sempre opcional, com rótulo claro. As recompensas são:
  - dobrar a XP da última batalha;
  - +25% no marcador de uma espécie derrotada;
  - reviver a equipe sem perder moedas.
  A recompensa só é entregue no callback de conclusão. O premiado **nunca** dá chance extra de Golden.
- Nenhum anúncio bloqueia a história.
- Gerar o `app-ads.txt` para o site da produtora.

### Google Play
- **Política de privacidade** em 3 idiomas, gerada a partir do `publisher.json`, cobrindo AdMob, consentimento e contato.
- **`PLAY_CONSOLE.md`** com respostas prontas para:
  - **Segurança dos dados:** ID de publicidade, interações, diagnósticos e localização aproximada coletados pelo AdMob, com criptografia em trânsito e sem contas;
  - **Contém anúncios:** sim;
  - **IARC:** violência de fantasia leve;
  - **Público-alvo:** 13+;
  - **Acesso ao app:** sem login;
  - **ID de publicidade:** sim.
- **Ficha da loja nos 3 idiomas:**
  - textos sem citar outras marcas;
  - ícone 512×512 e gráfico de destaque 1024×500;
  - 4 ou mais capturas em paisagem por idioma.
- Lembrar o Fernando do teste fechado (12 testadores por 14 dias) caso a conta seja nova.

## 15. Telas e sistemas de suporte

- **Tela inicial:** Continuar, Novo jogo, Configurações e Sobre.
- **Configurações:** idioma, volume de música e efeitos, velocidade do texto, 2x padrão, vibração e privacidade e anúncios.
- **Sobre:** dados do `publisher.json`, versão, política de privacidade e créditos.
- **Save:** automático ao trocar de mapa, após crescimento ou recrutamento e ao pausar o app. Um slot com backup.
- **Áudio:** chiptune original ou CC0, com tema por região e temas de batalha, chefe, aniversário e Golden.
- **Desempenho:** 60 FPS em aparelho médio, AAB com menos de 150 MB e carregamento em menos de 3 s.

## 16. Fases de entrega (uma por tarefa)

1. **Base:** projeto Godot, controles, movimento, tilemap da Praia, diálogos, i18n com 3 idiomas, save, 2x, menu de debug e pipeline de build.
2. **Batalha:** sistema 2×2, menu em anel, timeline, tipos, fórmula, veneno, XP, níveis, fuga e derrota.
3. **Esqueletos:**
   - **3a – Sistemas:** crescimento, animação de aniversário, marcador, Golden (shader, chance, regra de 99%), Rancho e Ossário.
   - **3b – Bíblia de criaturas:** `BESTIARIO.md` completo, nomes nos 3 idiomas, sprites e `bestiario_sheet.png`. **Pare e entregue a ficha de revisão.**
   - **3c – Golpes e números:** 56 golpes, atributos, `balance.json`, simulador e `BALANCEAMENTO.md`.
4. **História e mundo**, com roteiro antes do código em cada subtarefa:
   - **4a:** `00_arco.md` (pistas de 2040, arcos de Lia e Taro, os 6 Guardiões, escolhas, 2 finais), mais o Prólogo e a Praia;
   - **4b a 4g:** uma região por tarefa, cada uma com cidade completa, rotas com caminhos e domadores;
   - **4h:** Castelo, finais, recrutamento do Rei, créditos e pós-jogo.
5. **Monetização e conformidade:** UMP, AdMob, política, app-ads.txt e ficha da loja nos 3 idiomas.
6. **Polimento e publicação:** áudio, animações, revisão das traduções, `PLAY_CONSOLE.md`, checklist final e AAB de release.

## 17. Checklist final

- [ ] Conteúdo 100% original; `CREDITS.md` completo
- [ ] `validate_data.py` e `check_placeholders.py` passando
- [ ] Simulador dentro das metas (Guardiões de 60% a 85%, tempo de 2h45 a 3h15, sem grind)
- [ ] 3 idiomas completos, sem overflow de texto, com troca em tempo real
- [ ] Golden: taxa de 1/40 verificada, regra de 99% funcionando, shader em todos os estágios
- [ ] Crescimento no nível certo de cada linha, com animação ao lado do jogador e respeitando o 2x
- [ ] Toda cidade com rancho, loja e 2 ou 3 casas de domadores; toda rota com caminhos alternativos
- [ ] Rei Esqueleto entra na equipe nos dois finais; pós-jogo funcionando
- [ ] targetSdk ≥ 35, AAB assinado, compatível com 16 KB
- [ ] UMP antes dos anúncios; IDs reais só no release; anúncios só nos pontos permitidos
- [ ] Jogo completável offline; save/load testado
- [ ] Política de privacidade publicada; `PLAY_CONSOLE.md` pronto
