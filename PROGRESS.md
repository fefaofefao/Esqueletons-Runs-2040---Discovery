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
| 4c–4h — Regiões, Castelo e finais | ⏳ próxima (4c) |
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

### Próxima tarefa: Fase 4c — Minas de Cinzas
`03_minas.md`, Rota 2, Minas, Tia Fornalha (Defesa), escolha 2 (quebrar a corrente ou negociar), pista do mapa antigo e o lenço da mãe do Taro.
