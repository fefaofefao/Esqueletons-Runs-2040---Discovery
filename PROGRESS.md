# Progresso

Jogo: **Esqueletons Runs 2040 — Edição Discovery** (primeiro da série).
Especificação: `AGENTS.md`. Decisões: `docs/DECISOES.md`. Correções do Fernando: `docs/FEEDBACK.md`.

| Fase | Estado |
|---|---|
| 1 — Base | ✅ concluída (APK de debug pelo CI) |
| 2 — Batalha | ✅ concluída |
| 3a — Sistemas dos esqueletos | ✅ concluída |
| 3b — Bestiário | ✅ concluída |
| 3c — Golpes e balanceamento | ✅ concluída |
| 4a — Arco e Prólogo | ✅ concluída |
| 4b — Bosque das Raízes | ✅ concluída |
| 4c — Minas de Cinzas | ✅ concluída |
| 4d — Pântano Verde-Musgo | ✅ concluída |
| 4e — Cidade Murada de Ossório | ✅ concluída |
| 4f — Picos Gelados | ✅ concluída |
| 4g — Deserto dos Ecos | ✅ concluída |
| 4h — Castelo, finais e pós-jogo | ✅ concluída |
| 5 — Monetização e conformidade | — |
| 6 — Polimento e publicação | — |

## Fase 1 — Base (concluída)

### Feito
- **Projeto Godot 4.7.2** (GDScript, Compatibility), 320×180 com escala inteira pixel-perfect, paisagem e `aspect expand` para telas 20:9.
- **Controles:** D-pad virtual de 4 direções (deslizar troca a direção), A e B, MENU e ⏩ 2x no topo; multitoque; área ≥ 48dp (testada); semitransparentes. Teclado e gamepad. Botão voltar do Android = B, ou pausa no mapa. Segurar B corre.
- **Movimento em grade** estilo GBA (toque vira, segurar anda), colisão com terreno, objetos e NPCs, portas com fade e câmera presa ao mapa.
- **Praia do Despertar** (48×30) com cabana do Bento por dentro: água e grama animadas, espuma e areia molhada automáticas, coqueiros balançando, folhas ao vento, brilho no mar, fogueira e lamparina com luz, poeira ao correr, tom de luz por região. A saída norte para a Vila Maré leva a uma mensagem de "área fechada" até a fase 4a.
- **Diálogos:** máquina de escrever (velocidade configurável, respeita o 2x), até 3 linhas por caixa, quebra automática, A acelera/avança, nome do falante, escolhas, flags, `goto` e condições. Tocar na caixa também avança.
- **i18n PT-BR/EN/ES:** todo texto visível usa chave; idioma do aparelho com fallback para inglês; troca na hora, sem reiniciar; fonte pixel própria com acentos, ç, ñ, ¿ e ¡; teste de overflow com 30% de folga.
- **Save** JSON versionado em `user://`, com arquivo temporário + backup, recuperação de arquivo corrompido, migrações e tempo de jogo por região (real e em 1x). Salva ao trocar de mapa, ao pausar o app, ao sair e ao fechar.
- **Fast forward 1x/2x** salvo (é a mesma opção "2x padrão"); menus não aceleram.
- **Telas:** título (Continuar, Novo jogo, Configurações, Sobre), nome do protagonista, pausa, configurações (idioma, música, efeitos, velocidade do texto, 2x padrão, vibração, privacidade e anúncios), Sobre (lido de `config/publisher.json`) e créditos.
- **Menu de debug** (só no debug; 3 toques no logo, F1 ou Select): teleporte, 10x, raios de patrulha, tabelas de encontro, controles de toque, tempo por região, salvar/apagar save. Itens das fases 2 e 3 aparecem desativados.
- **Ferramentas:** `tools/validate_data.py` (todas as regras da seção 12, com autoteste), `tools/check_placeholders.py`, `tools/sync_publisher.py`, `tools/check_16kb.py`, `tools/check_manifest.py`, `tools/setup_codex.sh`, `tools/check_all.sh`, geradores de arte em `tools/art/` e capturas de tela em `tools/screenshots/`.
- **CI:** validação + testes headless + APK de debug a cada push; AAB assinado em tag `v*`, com keystore via Secrets.

### Verificação desta tarefa
- Importação headless do Godot sem erros de script.
- `tests/run_tests.tscn`: 1785 verificações, 0 falhas (save, i18n, overflow, controles, toque/48dp, 2x, mapas, diálogos, movimento real com frames).
- `tools/validate_data.py`: OK (regras de fases futuras marcadas como PENDENTE).
- Capturas de tela reais (Xvfb + OpenGL) conferidas nos 3 idiomas.
- **APK de debug gerado pelo GitHub Actions** (execução nº 3, verde), com páginas de 16 KB conferidas e manifesto verificado no CI (package, minSdk 24, targetSdk ≥ 35, só as 3 permissões). O APK não é gerado localmente porque o Android SDK (`dl.google.com`) é bloqueado neste ambiente.
- O job do AAB de release ainda não rodou: ele precisa dos Secrets do keystore e do `publisher.json` sem placeholders (ver `docs/BUILD.md`).

### Ajuste pós-fase 1: tela inicial HD
- Logo HD novo ("ESQUELETONS RUNS 2040" + "EDITION · DISCOVERY") e tela inicial moderna em alta resolução, com cenário animado e botões novos. Detalhes em `docs/DECISOES.md`.

### Pendências e observações
- **Package name** `com.fsamplabs.esqueletonsruns2040.discovery`: confirmar antes da primeira publicação (não muda depois).
- `config/publisher.json`: produtora (FSamp Labs), responsável e e-mail preenchidos. Falta só o **site** (usado na política de privacidade e no app-ads.txt). O release fica bloqueado até preencher.
- Os diálogos do Bento e os objetos da cabana são provisórios. A fase 4a escreve `docs/roteiro/00_arco.md` e o roteiro do Prólogo, e eles podem ser substituídos.
- Música: nenhuma ainda (fase 6). O sistema de áudio já tem barramentos Music/SFX e volume.
- Vibração usa `performHapticFeedback` (sem permissão extra). Precisa ser conferida num aparelho real.
- "Privacidade e anúncios" mostra um aviso até a fase 5 (UMP).


## Fase 2 — Batalha (concluída)

### Feito
- **Batalha em dupla 2×2:** time de até 4, com 2 em campo e 2 na reserva. Selvagens vêm em 1 ou 2; domadores e chefes em 2, com reservas.
- **Motor de regras** (`BattleEngine`) separado da tela, com a fórmula da seção 9 (tipo ×1,5/×0,75, mesmo tipo ×1,25, variação 0,85–1,0, crítico ×1,5 com 6,25%), ordem por prioridade e VEL, veneno de 3 a 5 turnos, buffs/debuffs, cura, itens, troca que gasta o turno, fuga por VEL (só de selvagens), XP (participantes 100%, reservas 50%), níveis até 50, aprender golpe (com escolha de qual esquecer) e derrota.
- **IA** de golpe: melhor dano esperado, cura abaixo de 35% de PV; selvagens às vezes agem ao acaso.
- **Tela:** timeline de turnos no topo, menu em anel, prévia do golpe com efetividade/efeito/alvo, alvo pelo D-pad ou toque, "Repetir último turno" (MENU), caixas com barra de PV animada, números de dano, partículas por tipo, lunge/tremida/queda, log com máquina de escrever. Respeita o 2x.
- **Integração:** `Game.start_battle()` abre a batalha sobre o mapa com transição em flash, devolve a equipe para o save, aplica a derrota (−10% de moedas, cura, volta ao ponto de retorno) e salva.
- **Debug:** batalhas de teste, equipe de teste, definir nível, vencer batalha.
- **Arte de teste:** fundo de batalha da praia, 4 bonecos de treino (frente/costas), ícones de tipo, do anel e de veneno.

### Verificação
- `tests/run_tests.tscn`: 2582 verificações, 0 falhas. Inclui `test_battle.gd` (regras) e `test_battle_ui.gd`, que joga batalhas completas pela interface: selvagem, domador com troca forçada, derrota e aprendizado de golpe.
- O CI agora falha se houver qualquer `SCRIPT ERROR` durante os testes.
- `validate_data.py` também confere `battle.json`, `items.json` e os dados de teste.
- Capturas de tela em 16:9 e 20:9 conferidas.

### Pendências
- Esqueletos selvagens no mapa, crescimento, marcador, Golden, Rancho e Ossário: fase 3a.
- Espécies, golpes e números reais (substituem os bonecos de teste) e o simulador: fases 3b/3c.
- Música de batalha: fase 6.

### Depois da fase 2: idade e batalha nova (pedido do Fernando)
- Nível exibido como **idade** (máx. 100; Rei 120), aniversário a cada idade, estágios Bebê/Adolescente/Adulto.
- Batalha refeita em **turnos por tempo** (timeline de 8 ações, peso Leve/Normal/Pesado, Atraso, Sintonia +25%) e arena lateral. Detalhes em `docs/DECISOES.md`.

## Fase 3a — Sistemas dos esqueletos (concluída)

### Feito
- **Crescimento por idade:** ao atingir a idade da linha, o esqueleto cresce para o próximo estágio ao voltar ao mapa. A proporção de PV é mantida e ele aprende o golpe exclusivo do estágio novo (escolhe qual esquecer se já sabe 4).
- **Cerimônia "Aniversário e Crescimento"** (`scripts/systems/growth_ceremony.gd`): o esqueleto sai do chão ao lado do jogador; aparecem bolo com velas, confete e o balão "Feliz aniversário, X!"; ele sopra as velas; a silhueta alterna entre os estágios até um flash; por fim, a revelação. Respeita o 2x e não pode ser pulada.
- **Marcador de ossos** (`scripts/systems/ossuary.gd`): cada vitória sobre um selvagem soma de 20% a 50% conforme a raridade e a diferença de idade. Em 100%, a espécie pede para entrar no time. Recusar mantém o marcador cheio. Time cheio manda o recruta para o Rancho.
- **Golden:** chance de 1/40 só em selvagens, com shader dourado, brilho, faíscas, som ao entrar na tela e +10% de atributos. Derrotar um Golden deixa o marcador em 99%, e a próxima vitória sobre a espécie oferece a **versão Golden** (direito ao Golden).
- **Selvagens visíveis no mapa** (`scripts/world/wild_skeleton.gd`) com comportamentos patrulha, ronda, persegue, tímido e rápido. Encostar inicia a batalha (30% de chance de vir um segundo). Fugir deixa o selvagem atordoado por 3 s; vencer o remove do mapa.
- **Ossário** (menu de pausa): cada espécie aparece como vista, derrotada (○), recrutada (●) ou Golden (☆ vista / ★ recrutada), com o marcador e o % de conclusão.
- **Rancho:** cura todos e troca esqueletos entre o time e o Rancho. No jogo, ele entra nas cidades da fase 4; por enquanto abre pelo debug.
- **Debug:** Forçar Golden, Forçar crescimento, Time de crescimento, Selvagens de teste aqui, Abrir Rancho, Adicionar esqueleto. "Vencer batalha" agora dá a XP normal.
- **Correção:** o fim da batalha não roda duas vezes quando "Vencer batalha" chega no meio de uma ação.
- **Fonte:** novos glifos ● ○ ☆.

### Verificação
- `tests/run_tests.tscn`: 2985 verificações, 0 falhas. O novo `test_growth.gd` cobre:
  - crescimento 6/12 anos e idade máxima 100;
  - Golden em 1/40 ± 5% (100 mil sorteios) e domadores nunca Golden;
  - marcador entre 20% e 50% (de 2 a 5 vitórias), além de recusar e aceitar;
  - a regra dos 99%;
  - time/Rancho e Ossário;
  - a cerimônia completa;
  - selvagens nascendo no mapa.
- Capturas com `capture.tscn -- --phase3`: Golden na batalha, marcador e pedido para entrar, bolo/balão, silhuetas, revelação, selvagens com raios, Ossário e Rancho.

### Pendências
- Espécies reais, sprites de mapa e tabelas de encontro reais: fase 3b. O Ossário só lista os bonecos de teste até lá (em build de debug).
- Rancho nas cidades: fase 4.

## Fase 3b — Bestiário (concluída)

### Feito
- **`docs/BESTIARIO.md`:** a bíblia com as 24 linhas, os 7 únicos e o Rei. Cada linha tem conceito, silhueta, arco Bebê → Adolescente → Adulto, personalidade, comportamento no mapa, tipo, região, raridade, idades de crescimento, golpe assinatura, nomes nos 3 idiomas e entrada do Ossário por estágio.
- **Fonte única:** `tools/bestiary/bestiary.py`. O `build.py` gera `data/species.json`, `i18n/species.csv` (160 textos × 3 idiomas) e o próprio BESTIARIO.md.
- **Tipos:** Físico 6, Mágico 6, Cura 7, Veneno 5 (dentro de 6 ± 1). **Regiões:** Praia 4 (com Taro e Lia), Bosque 4, Minas 4, Pântano 3, Ossório 3, Picos 3 e Deserto 3; um único por região a partir do Bosque, mais um no Castelo.
- **Sprites originais das 80 espécies** (`tools/art/gen_skeletons.py`, motor em `tools/art/skel.py`):
  - batalha 32×32 (folha frente/costas);
  - mapa 16×16 com 2 quadros;
  - corpo de bebê, adolescente ou adulto, mais as peças que contam o arco de cada linha.
- **Folha de revisão:** `docs/bestiario_sheet.png`, com mapa e batalha lado a lado em ordem do Ossário.
- **Atributos provisórios dentro das bandas** (Bebê 262–300, Adolescente 372–412, Adulto 482–522, únicos 490, Rei 600), distribuídos pelo papel de cada linha. A fase 3c ajusta com o simulador.
- **Ossário:** ficha de cada espécie com sprite (dourado se recrutado Golden), número, tipo, estágio, situação, marcador e entrada.
- **Selvagens do mapa** usam o sprite de mapa animado.

### Verificação
- `validate_data.py`: OK. Confere 80 espécies, 3 estágios por linha, idades em ordem, bandas, tipos 6 ± 1, prefixos (máx. 2 por idioma), nomes não descritivos, assinaturas únicas e traduções.
- `tests/run_tests.tscn`: 0 falhas. Todos os nomes cabem na carta da batalha e as entradas cabem na caixa de 3 linhas, nos 3 idiomas.
- Capturas `capture.tscn -- --bestiary`: lista do Ossário, fichas e selvagens reais no mapa.

### Pendências
- Golpes reais (learnsets e as 24 assinaturas): fase 3c. Até lá as espécies reais só lutam com "Esforço".
- Tabelas de encontro das regiões: fase 4.

## Fase 3c — Golpes e balanceamento (concluída)

### Feito
- **56 golpes** (16 Físicos, 16 Mágicos, 12 de Cura/Suporte, 12 de Veneno), entre eles as 24 assinaturas. Cada golpe tem peso (leve/normal/pesado), alvo, PP, precisão e efeitos.
- **Fonte única:** `tools/bestiary/moves.py`. Gera `data/moves.json`, `i18n/moves.csv` e os learnsets. As descrições saem dos próprios efeitos (setas ↑↓), então nunca mentem.
- **Novas mecânicas no motor:** golpes de 2 acertos, dreno (recupera % do dano) e efeitos em quem usa (`on: self`). A IA leva as três em conta.
- **Learnsets das 80 espécies:**
  - escada de poder igual entre os tipos, mais ataques de um tipo secundário por linha;
  - a assinatura vem ao crescer para Adolescente, e o golpe mais forte do tipo ao virar Adulto;
  - únicos e Rei têm conjuntos próprios, sem assinaturas.
- **`data/balance.json`:**
  - metas da seção 11 por região (chegada, Guardião);
  - plano de encontros (selvagens, domadores, faixa de idade);
  - equipe mais provável e protótipos dos Guardiões;
  - orçamento de tempo.
- **Simulador** (`tools/sim/simulate.gd` com o motor e a IA reais; `tools/simulate.py` confere os critérios e gera `docs/BALANCEAMENTO.md`). 40 jogadas e 10 tentativas por Guardião rodam em cerca de 1 min.
- **Ajustes feitos com o simulador:** XP, faixas de idade, golpes de veneno físicos, perfis de atributo, vantagem de tipo ×1,35/×0,8, Cura com dano próprio e Taro × Lia. A tabela completa está no BALANCEAMENTO.md.
- **Batalha:** lista de golpes mais larga (nomes longos cabem). A carta mostra ★ e o nome sem o sufixo Golden.

### Resultado (simulação, 40 jogadas)
- Idade no Guardião dentro de ~1,5 ano da meta em todas as regiões (20/34/47/60/70/81/88).
- Vitória contra os Guardiões entre 67% e 85%; Rei 64%.
- Tempo estimado: 2h54.
- Golpe mais usado: 15%.
- Diferença máxima entre tipos: Mágico +16 pontos (limite 20).

### Verificação
- `tests/run_tests.tscn`: 4763 verificações, 0 falhas. O novo `test_moves.gd` cobre:
  - 2 acertos, dreno e efeito em si mesmo;
  - golpes de todas as espécies e assinatura só da própria linha;
  - batalhas completas entre espécies reais.
- O teste de overflow confere os nomes de golpe na lista e as descrições na faixa, nos 3 idiomas.
- `validate_data.py`: confere `moves.json` (tipos, pesos, alvos, efeitos), learnsets e `balance.json`.
- `python3 tools/simulate.py --check`: todos os critérios OK.

### Pendências
- Os Guardiões são protótipos, e caminhada e leitura são orçamento. A fase 4 define as equipes do roteiro, mede os mapas reais e repete a simulação.

## Fase 4a — Arco da história e Prólogo (concluída)

### Feito
- **`docs/roteiro/00_arco.md`:**
  - a verdade de 2040: o protagonista é o último herdeiro do Rei, puxado pelo eco da coroa;
  - as 8 pistas em ordem;
  - os arcos de Lia (medo → luz) e de Taro (raiva → perdão);
  - os **6 Guardiões parentes do Rei**: primo, tia, sobrinha, irmão, filha e esposa, com motivo e mecânica-tema;
  - 5 escolhas e os 2 finais, com o Rei entrando na equipe nos dois.
- **`docs/roteiro/01_prologo.md`:** problema local (o cais fechado), pista (o ingresso do museu), momento de Lia e Taro, NPCs, domadores, escolhas e todas as falas.
- **Sistemas de roteiro:**
  - **ações no diálogo:** dar parceiro, batalha (com vitória, recompensa e marcador), curar, item, moedas, Rancho, loja, ponto de volta, sumir NPC;
  - **eventos de entrada** no mapa;
  - **condições de flag** em NPCs, objetos e zonas de selvagens;
  - **domador com campo de visão** ("!", caminha até o jogador e desafia, uma vez só).
- **Novas telas:** Loja, Mochila (usar poções fora da batalha; o ingresso é item-chave) e Equipe (ficha e ordem do time). Dicas do Bento na 1ª batalha e tutorial do marcador.
- **Vila Maré:**
  - cidade com Rancho, Loja, 2 casas de domadores, 4 NPCs de praça, a missão da rede da Jurema e o Fiscal Brás;
  - o recorrente com batalha opcional;
  - mapas gerados por `tools/maps/make_prologo.py`.
- **Praia:** farol velho, selvagens bebês (depois da escolha do parceiro), rede da missão e o despertar.
- **Arte nova:**
  - prédios (Rancho, Loja, 2 casas), farol, cerca, poste com luz, poço, banca e floreira;
  - 8 NPCs humanos (`tools/art/gen_npcs.py`) e Lia/Taro como NPC;
  - sons de cura, compra e "!".
- **Texto:** 82 chaves nos 3 idiomas (`tools/maps/prologo_text.py`), cerca de 690 palavras PT-BR.

### Verificação
- `tests/run_tests.tscn`: 0 falhas. O novo `test_prologue.gd` roda os roteiros de verdade:
  - despertar, Bento, escolha de Lia e de Taro;
  - missão da Jurema, ordem das falas dos NPCs;
  - loja, mochila, condições de mapa e visão do Brás.
- Captura `capture.tscn -- --prologo` joga o Prólogo inteiro: despertar, Bento, escolha, praia, dica da 1ª batalha, vila, Marola, Anzol, Brás e Equipe.
- `validate_data.py`: OK (mapas, portas, NPCs, diálogos, encontros e traduções).

### Pendências
- A estrada norte leva à Rota 1, que é a fase 4b; por enquanto aparece uma mensagem de "próxima atualização".
- Os tempos reais do Prólogo devem ser medidos e passados ao `balance.json` (orçamento atual: 15 min).

## Fase 4b — Bosque das Raízes (concluída)

### Feito
- **`docs/roteiro/02_bosque.md`:**
  - problema local: as raízes trançadas isolam Raizal e falta remédio;
  - pista nº 2: o brasão no Raizerno, igual ao do ingresso;
  - momento de Lia: o túnel escuro;
  - Guardião Ramalho, primo do Rei, que ensina o Atraso;
  - NPCs, casas de domadores e escolhas.
- **Rota 1 com 3 caminhos** que se reencontram antes de Raizal:
  - Domadores (Rufo, Íris, Cipó);
  - Campo das Flores (mais selvagens, inclusive Flautim raro);
  - Túnel das Raízes (escuro, com cogumelos luminosos e um selvagem forte).
  A estrada central fica fechada por raízes até o Guardião perder. Placa na bifurcação e Lenhador Velho com a dica.
- **Raizal (cidade completa):**
  - Rancho (Tília), Loja com Poção M (Toco);
  - 2 casas de domadores (Irmãos Galho, Família Musgo);
  - Sálvia com a missão da erva-de-febre, Graveto (humor) e Hera (lore: os Guardiões são família);
  - a Clareira do Machado com o Guardião.
- **Ramalho:** equipe Toreiro 22, Vagalú 22 e Raizela 23; vê o jogador e desafia. A vitória dá 800 moedas e a Lasca de Raiz, e desfaz as raízes da Rota 1.
- **Bosque Velho:** Raizerno (único, batalha selvagem com marcador) e o brasão.
- **Recorrente:** cena no túnel e batalha opcional na saída.
- **Arte:**
  - carvalhos, pinheiros, raízes trançadas, bocas de túnel, tocos, troncos, cogumelos (inclusive luminosos), erva azul e o tronco do Raizerno;
  - 12 NPCs novos (Ramalho é um esqueleto);
  - **fundo de batalha da floresta**, escolhido pela região.
- **Texto:** 79 chaves nos 3 idiomas (`tools/maps/bosque_text.py`), cerca de 490 palavras PT-BR.
- **Ferramentas:** o executor de testes aceita `--only=` e não trava mais quando um teste não compila.

### Verificação
- `tests/run_tests.tscn`: 0 falhas. O novo `test_bosque.gd`:
  - percorre a Rota 1 por busca em largura: o oeste sozinho e o leste sozinho chegam a Raizal, o centro fica fechado e abre depois do Ramalho, e o Túnel atravessa;
  - confere a cidade completa e as idades coerentes da equipe do Guardião.
- Captura `capture.tscn -- --bosque`: bifurcação, campo, túnel com Lia, Raizal, Ramalho vendo o jogador, a batalha do Guardião e o brasão do Raizerno.

### Pendências
- A estrada norte de Raizal leva às Minas (fase 4c). O vigia da Rota 2 vai pedir a Lasca de Raiz.

## Fase 4c — Minas de Cinzas (concluída)

### Feito
- **Kit de região** (`tools/maps/regionkit.py`): uma fonte única por região gera o roteiro `docs/roteiro/NN_<id>.md`, as falas nos 3 idiomas, NPCs, encontros, loja, itens, mapas e as fichas de cidade/rota (`data/cities.json`, `data/routes.json`). O roteiro e o jogo não podem divergir.
- **`docs/roteiro/03_minas.md`** (gerado por `tools/maps/minas.py`):
  - problema local: a Tia Fornalha acorrentou os esqueletos mineiros à forja, onde martelam as correntes que fecham as estradas;
  - pista nº 3: o mapa antigo do Seu Carvão com as três baías da cidade do protagonista;
  - momento de Taro: o lenço da mãe na Mina Funda (como parceiro ou recorrente);
  - Guardiã Tia Fornalha (Defesa), NPCs, casas e a **escolha 2**.
- **Rota 2** com 3 caminhos (Domadores Graxa/Brita/Fuligem; Campo de Cascalho; Galeria Velha com um selvagem forte). O Vigia confere a Lasca de Raiz. A saída norte de Raizal só abre depois do Ramalho (saídas agora aceitam condições).
- **Brasal:** Rancho (Rubi), Loja com Poção G (Cobre, preço muda com a escolha), casas do Mestre Bigorna (Defesa) e da Ágata (gás e cura), 2 missões (capacete do Carvão, bolo do Gasito da Pirita), NPCs de dica/humor/lore e falas que mudam depois da Guardiã.
- **Mina Funda:** salão de selvagens, Capataz Bloqueio, câmara sul (lenço, capacete, Vagonauta) e a forja da Tia.
- **Escolha 2:** quebrar a corrente (loja +25%, Vagonauta recrutável) ou pedir que ela solte (Martelo da Tia, loja −10%, +1 Redenção).
- **Parceiro comenta** a primeira visita de cada lugar (falas diferentes para Lia e Taro).
- **Arte:** casas de pedra, trilhos, vagonete, lampião de mina, cristais, vigas, bigorna, forja animada, corrente, entulho, quadro do mapa, lenço, capacete; 16 NPCs; sprites dos 6 Guardiões, do Rei, dos únicos e de Lia/Taro crescidos; **fundos de batalha de todas as regiões** (Minas, Pântano, Ossório, Picos, Deserto, Castelo); terrenos de todas as regiões; clima por região (cinza, névoa, neve, areia, brasas).
- **Sistemas:** `take_item`, `give_monster`, `refresh_map`, `fade`, `wait`, `credits`, `heal_all`; condições `if_all`/`if_any`/`if_count`; preço da loja por flag; tela de créditos.
- **Texto:** ~1.130 palavras PT-BR na região.

### Verificação
- `tests/run_tests.tscn`: 0 falhas. Novo `test_regions.gd`, genérico para todas as regiões: caminhos de cada rota por busca em largura, cidades completas, idades e média dos Guardiões contra o `balance.json`, as duas opções da escolha 2 e as missões.
- `tools/validate_data.py`: OK, agora também com `cities.json` e `routes.json` (rancho, loja, 2–3 casas, 3–6 NPCs, 1–2 missões e NPCs presentes de verdade nos mapas).
- `tools/simulate.py --check`: 174 min, 0 critérios falhando.
- Capturas: `capture.tscn -- --region=minas` (roteiro em `tools/screenshots/regions.json`).

### Pendências
- O volume de texto do Prólogo (~690) e do Bosque (~490) está abaixo do orçamento do arco; será completado na revisão de texto da fase 6, junto com as regiões novas, para atingir 12–18 mil palavras no total.

## Fase 4d — Pântano Verde-Musgo (concluída)

### Feito
- **`docs/roteiro/04_pantano.md`** (gerado por `tools/maps/pantano.py`):
  - problema local: a névoa do caldeirão da Musga adoece Brejo Alto toda noite, e só ela tem o remédio;
  - pista nº 4: a Musga sente "cheiro de casa, de família" no protagonista;
  - Taro descobre pela fofoca da Musga que os pais estão no castelo (parceiro ou recorrente); Lia vê os vaga-lumes;
  - Guardiã Musga (Veneno e cura) e a **escolha 3** (doar ou guardar os antídotos).
- **Rota 3** com 3 caminhos: Trilha das Tábuas (Traíra, Caniço, Marreco), Capinzal e a Passagem do Desmoronamento, que só abre com o **Martelo da Tia** (escolha 2).
- **Brejo Alto** (palafitas): Rancho da Garça (onde acontece a escolha), Loja sem antídoto, casas das Irmãs Taboa e do Bagre, casa da Vó Neblina (abre se você doar), missão do malote, NPCs de dica, humor e lore.
- **Caldeirão da Musga:** Boticário Fel, malote roubado, Brumaga (se você doou) e a Guardiã.
- **Escolha 3:** doar (até 3 antídotos; +1 Redenção, 3ª casa de domadores e Brumaga recrutável) ou guardar.
- **Arte:** juncos, vitórias-régias, salgueiro, árvore seca, caldeirão animado com luz verde, casas de palafita, lampião do pântano, malote; 14 NPCs; props das regiões seguintes (Ossório, Picos, Deserto, Castelo e epílogo) já desenhados.
- **Sistema:** condição `if_none` (nenhuma das flags).

### Verificação
- `tests/run_tests.tscn`: 7842 verificações, 0 falhas (inclui as duas opções da escolha 3, a escolha adiada sem antídotos e a missão do malote).
- `tools/validate_data.py`: OK. `tools/simulate.py --check`: 174 min, 0 critérios falhando.
- Capturas: `capture.tscn -- --region=pantano`.

## Fase 4e — Cidade Murada de Ossório (concluída)

### Feito
- **`docs/roteiro/05_ossorio.md`** (gerado por `tools/maps/ossorio.py`):
  - problema local: lei marcial do Caliço (toque de recolher, moradores de guarda na muralha) e o Arquivo Real lacrado pelo Rei;
  - **pista nº 5, a revelação de 2040:** o registro "Quando a coroa rachar, o eco chamará o último do sangue, onde o farol virar museu" e o retrato do príncipe com o rosto do protagonista;
  - Lia: o diário da Rainha Duna (ela ergueu o farol); "o Rei só tem medo do escuro, igual eu tinha";
  - recorrente com batalha opcional (Lia/Taro já no estágio adulto);
  - Guardião Caliço (Sintonia) e a **escolha 4** (contar o registro à cidade ou guardar segredo).
- **Rota 4** (Cadetes, Campo das Bandeiras, Aqueduto Velho), **Ossório** (Rancho, Empório, casas da Viseira e dos Elo, Arquivo Real, praça com chafariz, estátua e torre do sino), **Quartel** (Sargento Grade, Bufardo, Caliço).
- **Missão do Selo:** uma pergunta sobre o diário (só acerta quem leu).
- **Escolha 4:** contar (+1 Redenção, guardas leais na Rota 5, Caliço aliado no Castelo) ou segredo.
- 13 NPCs novos; chapéus novos (elmo, capuz, turbante).
- Testes: o guardião precisa ter a mesma equipe que o `balance.json` (linha e idade ±1), para o simulador simular a luta real. Capturas: o roteiro de capturas agora fecha telas de "aprender golpe" e outras sobreposições.

### Verificação
- `tests/run_tests.tscn`: 0 falhas (revelação, escolha 4 nos dois sentidos, missão do Selo).
- `tools/validate_data.py`: OK. `tools/simulate.py --check`: 0 critérios falhando.
- Capturas: `capture.tscn -- --region=ossorio` (Rota 4, recorrente, cidade, Caliço, revelação, diário).

## Fase 4f — Picos Gelados (concluída)

### Feito
- **`docs/roteiro/06_picos.md`** (gerado por `tools/maps/picos.py`):
  - problema local: a Alva congelou os picos para "nada mudar" até o pai melhorar; Geada está sem chá e sem estrada;
  - pista nº 6: o monge Nevasco explica que o eco da coroa atravessa o tempo (o vidro do museu vibrando);
  - **reencontro com o recorrente** (batalha opcional; a cena acontece mesmo sem lutar): Taro admite o medo de os pais não lembrarem dele; Lia ensina a "seguir a luz";
  - Guardiã Alva (Velocidade) e a **escolha 5** (levar ou não a carta ao pai; dá para voltar e aceitar depois).
- **Consequência da escolha 4:** se Ossório soube do registro, 2 Guardas Leais vigiam a Rota 5.
- **Geada:** Rancho, Armarinho (só itens fortes), casas da Patinadora Lâmina e dos Irmãos Granizo, Mosteiro do Eco (Nevasco, único recrutável), missão do broto de chá.
- **Jardim de Gelo:** Guarda Pingente, broto e Alva. 13 NPCs novos.

### Verificação
- `tests/run_tests.tscn`: 9535 verificações, 0 falhas (carta aceita depois de recusar, pista 6, Guardas Leais só com a escolha 4).
- `tools/validate_data.py`: OK. Capturas: `capture.tscn -- --region=picos`.

## Fase 4g — Deserto dos Ecos (concluída)

### Feito
- **`docs/roteiro/07_deserto.md`** (gerado por `tools/maps/deserto.py`):
  - problema local: a tempestade de areia da Rainha Duna esconde o castelo e os tambores-guia foram calados; as caravanas se perdem no eco;
  - pista nº 7: a Duna conta para que o Rei quer o herdeiro (a coroa se refaz na cabeça dele e o prende no trono para sempre);
  - fogueira de Palmeiral: Lia e Taro perguntam se o protagonista vai embora;
  - Guardiã Rainha Duna (Resistência: trocas e cura em grupo); ela reage à Carta da Alva.
- **Rota 6** (Caravanas, Dunas Altas, Passagem do Eco), **Palmeiral** (oásis de tendas, 2 casas, missão de encontrar o Seu Alforje perdido nas dunas), **Templo das Areias** (Sândalo, Ampulhor, Duna). 13 NPCs.

### Verificação
- `tests/run_tests.tscn`: 10217 verificações, 0 falhas. `tools/validate_data.py`: OK. `tools/simulate.py --check`: 0 critérios falhando.
- Capturas: `capture.tscn -- --region=deserto`.

## Fase 4h — Castelo, finais e pós-jogo (concluída)

### Feito
- **`docs/roteiro/08_castelo.md`** (gerado por `tools/maps/castelo.py`):
  - **Portão:** os pais do Taro guardam a porta e não o reconhecem (batalha); o Caliço cura a equipe se Ossório soube do registro (escolha 4).
  - **Grande Salão:** Ébano, Arauto, Tempero, selvagens, a fonte (cura e ponto de volta) e o **Provador Real Degustor** (chefe; no pós-jogo vira o único Degustor recrutável).
  - **Sala do Trono:** o parceiro acende as velas; o Rei pede "Coloque. Fique."; colocar a coroa é impedido pelo parceiro; batalha final (Rei 120 + escolta 78).
  - **Final A (Redimir):** exige a Carta da Alva + 2 de 3 Redenções. O Rei lê a carta, quebra a coroa, a família se despede (uma fala de cada Guardião) e ele pede para seguir o herdeiro.
  - **Final B (Derrotar):** a coroa se parte no golpe, a família some sem despedida, o Rei entra em silêncio.
  - **Nos dois:** o marcador do Rei enche até 100% e ele entra na equipe (idade 100); os pais reconhecem o Taro, que perdoa; Lia acende o farol; epílogo no **Museu de 2040** (vitrine vazia, "Peça em restauração"); créditos; pós-jogo na Praia com o farol aceso.
- **Pós-jogo:** os 6 Guardiões viram **ecos** para revanche (idades 95–100), Degustor recrutável, Lia no farol e a família do Taro na Vila Maré, falas novas em todas as cidades.
- **`docs/roteiro/09_extras.md`** (gerado por `tools/maps/extras.py`): o mundo reage à história — comentários do parceiro no Prólogo e no Bosque, NPCs que mudam depois do Brás e do Ramalho, **cartas do Bento** em cada Rancho, conversa com o parceiro na cama de cada Rancho, viajantes com lore em cada rota, 4 moradores novos, livros de lore, a 2ª missão de Geada (eleição do Prefeito de neve) e de Palmeiral (o ritmo dos tambores), fala do parceiro quando ele cresce.
- **Crônicas da Família Real** no Arquivo de Ossório (a primeira vida de cada Guardião).
- `tools/maps/build_all.py` regera todas as regiões na ordem certa.
- Sistema: ação `warp` (com `hide_player`); a batalha não mostra mais "recuperou 0 PV"; piso do castelo mais claro que as paredes.
- **Volume de texto:** 12.040 palavras PT-BR no jogo (meta 12–18 mil).

### Verificação
- `tests/run_tests.tscn`: 12125 verificações, 0 falhas (condição dos finais, Final A e B completos, o Rei na equipe com marcador 100%, ecos no pós-jogo).
- `tools/validate_data.py`: OK. `tools/simulate.py --check`: 174 min, 0 critérios falhando.
- Captura `capture.tscn -- --region=castelo`: portão, pais do Taro, salão, Provador Real, trono e o Final A.

## Correção urgente — conversa que recomeçava sozinha (concluída)

- Causa: no celular, um toque no botão A virtual também gerava um clique de mouse
  emulado. O clique fechava o diálogo e o A em seguida falava de novo com o NPC.
- Correção: os controles de toque descartam o clique emulado sobre os botões
  virtuais, e o A no mapa espera 0,3 s depois de fechar qualquer diálogo.
  Teste de regressão: `tests/test_player.gd`.
- Jogada de ponta a ponta verificada por captura (`--prologo` e `--bosque`): da praia
  até Vila Maré, Brás, Rota 1, Túnel, Raizal, Ramalho e o brasão do Raizerno, sem travar.

## Fase 5 — Monetização e conformidade (concluída, falta preencher dados reais)

### Feito
- AdMob 5.1.0 (Poing Studios, MIT) com UMP antes do SDK; regras da seção 14 no autoload `Ads`.
- Premiados opcionais: dobrar a XP, +25% no marcador, reviver sem perder moedas.
- Política de privacidade em 3 idiomas (`privacy/`), `app-ads.txt`, fichas da loja
  (`store/listing.*.md`), ícone 512, gráfico 1024×500 e 7 capturas por idioma.
- Exportação remove permissões extras (AD_ID duplicada, READ_BASIC_PHONE_STATE,
  ACCESS_ADSERVICES_*); o `tools/check_manifest.py` confere o APK no CI.

### Pendências do Fernando
- Secrets do release: `ADMOB_APP_ID`, `ADMOB_BANNER_ID`, `ADMOB_INTERSTITIAL_ID`,
  `ADMOB_REWARDED_ID` e a keystore.
- `config/publisher.json`: `[URL]` do site e `[ADMOB_PUB_ID]`. O build de release
  falha até que sejam preenchidos (`check_placeholders.py`).

### Próximo
- Fase 6 (abaixo).

## Lia e Taro juntos na equipe (pedido do Fernando, concluído)
- Bento entrega os dois no Prólogo (sem escolha); os dois são iniciais fixos com +5% em todos os atributos.
- Falas revisadas para a dupla; cenas de "recorrente" só em saves antigos (save v2 migra o parceiro único).
- Balanceamento refeito: XP `reward_div` 21, Guardiões +7% (o Rei fica de fora), Remada Dupla 2×40. Simulador: todos os critérios OK.

## Fase 6 — Polimento e publicação (em andamento)

### Feito
- **Música original** (`tools/audio/gen_music.py`): título, 7 temas de região, batalha, Guardião, Rei e vinhetas de aniversário e Golden. A música do mapa volta de onde parou depois da batalha. `tests/test_audio.gd`.
- **`PLAY_CONSOLE.md`** gerado do `publisher.json` (segurança dos dados, anúncios, IARC, público 13+, acesso sem login, ID de publicidade, teste fechado de 12 testadores por 14 dias).
- `tools/sync_publisher.py` agora regera todos os documentos da loja.
- **`docs/CHECKLIST_FINAL.md`** com o estado de cada item da seção 17.

### Pendências
- Do Fernando: site, ID de editor do AdMob, Secrets (keystore e IDs reais) e a tag `v0.1.0` (ver `docs/CHECKLIST_FINAL.md`).
- Ouvir as músicas e revisar as traduções no teste fechado (anotar em `docs/FEEDBACK.md`).

## Progressão dos selvagens e refinamento dos mapas (pedidos do Fernando)
- Selvagens e domadores em rampa: cada rota começa perto da idade do último líder e fica abaixo do próximo (Rota 1 agora 7–9 → 12–14). Regra conferida pelo `validate_data.py`.
- Mapas: 1º passe de refinamento (`tools/maps/refine.py`), tiles com mais variação, casas de toras em Raizal e a folha `docs/mapas_sheet.png` para revisão.
