# Decisões técnicas

Registro das escolhas feitas sem consulta (AGENTS.md, seção A). Cada item diz o quê, por quê e onde mexer se for preciso mudar.

## Fase 1 — Base

### Identidade
- **Nome definido pelo Fernando:** *Esqueletons Runs 2040 — Edição Discovery*, primeiro jogo de uma série. O nome provisório "Reino dos Ossos" deixa de valer. `config/publisher.json` guarda `game_name`, `series` e `edition` (localizada: Edição/Discovery Edition/Edición). O logo diz "ESQUELETONS RUNS 2040" e a edição aparece como texto traduzido abaixo dele.
- **Package name:** `com.fsamplabs.esqueletonsruns2040.discovery`. Cada edição da série vira um app separado na loja (`.discovery`, depois outras). **Atenção:** depois da primeira publicação o package não pode mudar. Se o Fernando preferir outro, a troca é só no `publisher.json` + `python3 tools/sync_publisher.py`.

### Motor e projeto
- **Godot 4.7.2** (estável mais recente em out/2026), GDScript, renderer Compatibility. A versão fica em `.github/workflows/build.yml`, `.github/actions/setup-godot-android/action.yml` e `tools/setup_codex.sh`.
- **Resolução 320×180**, `stretch mode = viewport`, `aspect = expand`, `scale mode = integer`. Em celulares 20:9 a área visível vira ~400×180: o mundo aparece mais largo e os controles ficam nas laterais. Orientação: paisagem com sensor.
- **Autoloads** (ordem importa): `Data` → `Settings` → `Speed` → `Controls` → `SaveGame` → `Audio` → `Haptics` → `Game`. O `Game` monta as camadas (tela, overlays, toque, fade) e controla o fluxo.
- **UI construída em código**, com poucas cenas `.tscn`. Isso deixa os diffs legíveis e evita erros de edição manual de cenas.
- **Tema aplicado em cada raiz de UI:** o tema do Godot não atravessa `CanvasLayer`, então `Overlay`, a tela de título e o letreiro do mundo recebem `UiTheme.build()` diretamente.

### Arte, fonte e som
- **Tudo é original e gerado por script** em `tools/art/` (Python + Pillow): fonte, tileset, transições, personagens, objetos, UI, ícones e efeitos sonoros. Nenhum pack externo foi usado. Para regenerar: `tools/art/gen_all.sh`.
- **Fonte própria "OssosPixel"** em formato BMFont (`assets/fonts/pixel.fnt`), célula de 12 px, com acentos, ç, ñ, ¿, ¡, aspas curvas, setas e ★. É renderizada só em escala inteira (`FIXED_SIZE_SCALE_INTEGER_ONLY`).
- **Transições de terreno automáticas:** espuma, areia molhada, franja de grama, borda da trilha e água funda são *overlays* com 46 máscaras canônicas (8 vizinhos), escolhidas em tempo de execução. Os mapas só descrevem o terreno.
- **Animação de tiles e 2x:** as animações de tile usam o relógio do renderizador, que ignora `Engine.time_scale`. Por isso o `MapView` ajusta `set_tile_animation_speed` quando a velocidade muda.
- **Iluminação simples:** `CanvasModulate` por região/mapa, brilho aditivo em lamparinas e fogueiras e sombra suave sob os personagens. Partículas: brilho na água, folhas dos coqueiros, poeira ao correr e poeira na luz em interiores.

### Mapas e conteúdo
- **Mapas em JSON com terreno em ASCII** (`data/maps/*.json`) + legenda. O `TileSet` é montado em código a partir de `data/tilesets/overworld.json`, que é gerado pelo `gen_tiles.py`. Objetos, NPCs, portas e partículas de ambiente ficam no mesmo JSON.
- **Diálogos** em `data/dialogs/<arquivo>.json`, referenciados como `"arquivo/id"`, com nós `say`, `choice`, `set_flag`, `goto`, `if` e `if_not`. Os textos são chaves de tradução.
- **Os diálogos da Praia são provisórios** e servem para testar o sistema. O roteiro definitivo do Prólogo sai na fase 4a (`docs/roteiro/`), que pode reescrevê-los.
- **A saída norte para a Vila Maré** existe no mapa, mas o destino ainda não foi construído (fase 4a). Ao pisar nela, aparece a mensagem `MSG_AREA_LOCKED` e o jogador volta um passo. O validador aceita portas para mapas *planejados* em `data/regions.json`.

### Controles
- **Ações próprias** (`move_*`, `btn_a`, `btn_b`, `btn_menu`, `btn_speed`, `dbg_menu`), registradas em código (`Controls`). Os controles virtuais injetam `InputEventAction`, então o resto do jogo não distingue toque, teclado ou gamepad.
- **Teclado:** setas/WASD; A = Z/Espaço/Enter; B = X/Backspace/Shift; MENU = Esc/C; 2x = F/Tab; debug = F1. **Gamepad:** D-pad/analógico; A/B; Start = MENU; RB = 2x; Select = debug.
- **Toque:** D-pad à esquerda (deslizar troca a direção), A e B à direita, MENU e 2x no topo, com multitoque. O braço do D-pad tem 24 px de base: com a escala inteira, isso passa de 48dp nos aparelhos de referência (teste `test_touch_targets_48dp`). Os controles aparecem ao tocar e somem ao usar teclado ou gamepad (modo "auto"); o debug força "sim/não".
- **Caixa de diálogo:** com os controles de toque visíveis, ela vai para o topo da tela, para não ficar embaixo do D-pad e dos botões. Sem toque, fica embaixo.
- **Movimento estilo GBA:** um toque rápido numa direção nova só vira o personagem; segurar anda (0,26 s por tile); B segurado corre (0,13 s por tile).
- **Botão voltar do Android:** num overlay, equivale a B; no mapa, abre a pausa; no título, sai. Ao ir para segundo plano, o jogo salva e abre a pausa.

### Fast forward
- **"2x padrão" e o estado do botão são a mesma configuração** (`fast_forward`). O botão alterna e salva, e a opção do menu mostra e muda o mesmo valor. Assim "o estado fica salvo" e "2x padrão" nunca se contradizem.
- **Menus em tempo real:** a repetição do D-pad nos menus usa `Time.get_ticks_msec()`, então não acelera no 2x. Texto, caminhada, animações, partículas e fades usam o tempo escalado.
- **Debug 10x substitui o 1x/2x** enquanto estiver ligado (não é salvo).

### Vibração sem permissão extra (contradição resolvida)
- A especificação pede a opção "Vibração" e restringe as permissões a INTERNET, ACCESS_NETWORK_STATE e AD_ID. `Input.vibrate_handheld` exigiria `VIBRATE`. **Solução:** `Haptics` usa `View.performHapticFeedback` via o singleton `AndroidRuntime` do Godot 4.4+, que não precisa de permissão. Respeita a opção do jogo e também a de toque do sistema.

### Idiomas
- CSV do Godot em `i18n/ui.csv` e `i18n/dialogue.csv` (`keys,pt_BR,en,es`). Os `.translation` são gerados na importação e não entram no git.
- Idioma inicial = do aparelho (`pt*` → pt_BR, `es*` → es, `en*` → en; outros → en). A troca acontece na hora: menus e telas reagem a `NOTIFICATION_TRANSLATION_CHANGED`.
- **Nomes de lugares localizados:** Vila Maré = *Tidemark Village* / *Villa Marea*; Bosque das Raízes = *Rootwood Forest* / *Bosque de las Raíces*; Minas de Cinzas = *Ashen Mines* / *Minas de Ceniza*; Pântano Verde-Musgo = *Mossgreen Marsh* / *Pantano Verdemusgo*; Cidade Murada de Ossório = *Walled City of Ossorio* / *Ciudad Amurallada de Osorio*; Picos Gelados = *Frostbite Peaks* / *Picos Helados*; Deserto dos Ecos = *Desert of Echoes* / *Desierto de los Ecos*.
- **Espaço de texto:** diálogo = até 3 linhas de 288 px; rótulos de menu = 160 px; valores = 90 px. O teste `test_text_overflow` mede com a fonte real nos 3 idiomas e exige que o PT-BR caiba com 30% de folga. Palavras iguais em PT e EN/ES de propósito (ex.: "Continuar" em espanhol) ficam listadas em `i18n/allow_identical.txt`.

### Save
- `user://save.json` (JSON indentado, campo `version`). A gravação passa por `save.tmp`, e o save anterior vira `save.bak.json`. Se o principal estiver corrompido, o jogo carrega o backup. As migrações ficam em `SaveGame._migrations` (versão → função); já existe a v0 → v1 como modelo, com teste.
- O save é automático ao trocar de mapa, ao ir para segundo plano, ao sair para o título e ao fechar o app. As fases 3a+ acrescentam crescimento e recrutamento.
- **Tempo de jogo por região** em duas medidas: `real` (relógio) e `game` (equivalente a 1x, comparável ao simulador). O menu de debug mostra as duas.

### Debug
- Só em build de debug (`OS.is_debug_build()`). Abre com 3 toques no logo (título ou painel de pausa) ou F1/Select. Itens das fases 2 e 3 aparecem desativados e marcados com a fase.

### Testes e validação
- **Runner próprio, sem dependências** (`tests/run_tests.tscn`). Cada `tests/test_*.gd` herda de `test_case.gd`. Os testes usam arquivos próprios de save e configurações, sem tocar no save real.
- `tools/validate_data.py` implementa todas as regras da seção 12. As regras de espécies, golpes, encontros, cidades e rotas já existem e passam a valer quando os arquivos forem criados (até lá aparecem como PENDENTE). O formato esperado está em `docs/DADOS.md`. `tools/tests/test_validate_data.py` quebra dados de propósito para provar que o validador pega os erros.

### Build Android
- **Gradle build** (necessário para AAB e para o plugin do AdMob na fase 5) com `min_sdk 24` e `target_sdk 36`, arquiteturas arm64-v8a e armeabi-v7a. O template de build é instalado no CI (`--install-android-build-template`) e não vai para o git.
- **APK de debug** a cada push, assinado com um keystore de debug gerado no próprio CI. **AAB de release** em tag `v*` ou execução manual, com o keystore vindo de Secrets. O release falha se houver placeholders.
- **Páginas de 16 KB:** `tools/check_16kb.py` lê os cabeçalhos ELF das `.so` de 64 bits dentro do APK/AAB e falha se algum segmento LOAD tiver alinhamento menor que 16 KB.
- `config/publisher.json` → `export_presets.cfg`/`project.godot` via `tools/sync_publisher.py`. O CI confere com `--check` e define `version/code` = número do build.
- **JSON no pacote:** `include_filter="*.json"` nos presets, e `tests/*` e `tools/*` excluídos.

### Créditos e marcas
- O jogo cita o Godot nos créditos (licença MIT, que exige o aviso de copyright). É obrigação de licença, não propaganda de marca. O texto completo da licença entra na tela de créditos/licenças na fase 6.

## Tela inicial HD (pedido do Fernando após a fase 1)
- **A tela inicial não é pixel art:** logo e cenário em alta resolução, para servir de vitrine da série. Enquanto ela está aberta, a janela usa `CONTENT_SCALE_MODE_CANVAS_ITEMS` (desenha na resolução nativa); ao sair, volta para `VIEWPORT` e o mundo segue pixel-perfect em 320×180. As telas sobrepostas (configurações, Sobre, nome) continuam no estilo pixel do jogo.
- **Logo:** "ESQUELETONS" em osso com uma caveira de viseira ciana no lugar do "O" (a mesma do ícone), "RUNS" em fogo com linhas de velocidade, "2040" em neon e a faixa "EDITION · DISCOVERY" em dourado. Tudo com contorno, extrusão 3D, bisel e brilho. O nome da edição fica em inglês, como marca da série. Gerado por `tools/art/gen_title.py` em 1600 px de largura, com mipmaps.
- **Cenário:** pôr do sol retrô "2040" com sol listrado, mar com reflexo ondulando (shader), ilha com o castelo do Rei Esqueleto (janelas acesas), nuvens em parallax, coqueiros em contraluz, raios de sol girando, brasas subindo e estrela cadente de vez em quando. As camadas têm 2400×1080 e cobrem telas 16:9 a 20:9.
- **Botões modernos** (`TitleButton`): vidro escuro com borda fina e antialiasing; o principal (Continuar/Novo jogo) é laranja e o selecionado ganha brilho ciano pulsando. Há animação de entrada (logo com quique e flash, botões subindo), que A ou um toque pulam.
- **Fontes OFL:** Nunito no jogo; Lilita One e Orbitron só para desenhar o logo, então não vão no pacote. A especificação pede assets próprios ou CC0. Fontes OFL são o padrão do mercado e permitem uso comercial e empacotamento; a origem está registrada em `CREDITS.md`. Se o Fernando quiser 100% CC0, troco a Nunito por uma fonte CC0.

## Fase 2 — Batalha

### Arquitetura
- **Regras separadas da tela.** `BattleEngine` (RefCounted, sem nós) resolve a rodada e devolve uma lista de eventos (`move`, `damage`, `miss`, `poisoned`, `poison_tick`, `stat`, `heal`, `switch_in`, `faint`, `xp`, `learn_prompt`, `fled`, `win`...). A `BattleScreen` só anima esses eventos. O simulador da fase 3c vai usar o mesmo motor e a mesma IA (`BattleAI`), então a batalha simulada e a jogada são idênticas.
- **Sorteios com semente** (`RandomNumberGenerator`): os testes são determinísticos.
- **Constantes em `data/battle.json`:** fórmula, STAB 1,25, variação 0,85–1,0, crítico 1,5/6,25%, tabela de tipos, estágios −3..+3, veneno, prioridades, XP, fuga, derrota e IA. O balanceamento por região (`balance.json`) vem na fase 3c.

### Regras que precisei definir (a especificação não fixa)
- **Atributos por nível:** PV = 2·base·N/100 + N + 10; demais = 2·base·N/100 + 5. Golden: +10% em tudo.
- **Categoria do golpe:** cada golpe tem `type` (vantagem e mesmo tipo) e `category` (`physical` usa ATQ×DEF, `magical` usa MAG×RES, `status` não causa dano). Golpes de Veneno são `magical` por padrão.
- **Alvos:** `enemy`, `all_enemies` (×0,75 em cada um quando há 2 alvos), `self`, `ally`, `all_allies`. Se o alvo cai antes, o golpe vai para o outro inimigo.
- **Ordem:** prioridade (fuga 7, troca 6, item 5, golpes 0 ou o valor do golpe), depois VEL com estágios, empate por sorteio.
- **Veneno:** 3 a 5 turnos (sorteado), 1/12 do PV máximo no fim de cada rodada.
- **Estágios:** +1 = ×1,5, +2 = ×2, +3 = ×2,5; −1 = ×0,67, −2 = ×0,5, −3 = ×0,4. Zeram ao trocar.
- **XP ao derrotar cada inimigo:** base_xp × nível/5 (×1,5 contra domadores e chefes). Quem participou recebe 100% e as reservas vivas 50%. Curva: XP do nível N = 0,8·(N−1)³. Ao subir de nível aprende o golpe do learnset; com 4 golpes, pergunta qual esquecer.
- **Fuga** (só de selvagens): 50% + 40% × (VEL mais rápida minha − deles)/deles + 12% por tentativa, entre 15% e 95%. Gasta a vez de quem tentou.
- **Derrota:** perde 10% das moedas, a equipe é curada e volta para o ponto de retorno do save (`respawn`, hoje a Praia). O Rancho de cada cidade passa a ser o ponto de retorno na fase 3a/4. O anúncio premiado "reviver sem perder moedas" entra na fase 5.
- **Sem PP:** o esqueleto usa "Debater-se" (poder 30).
- **Inimigo que cai é substituído na hora** pela reserva. Quando cai um aliado, o jogador escolhe quem entra no fim da rodada.

### Interface
- **Timeline** no topo, com os rostos na ordem prevista. Ela se atualiza enquanto você escolhe (uma troca ou um golpe com prioridade sobe na fila) e destaca quem está agindo.
- **Menu em anel** ao redor do esqueleto ativo: Golpes ↑, Itens →, Trocar ↓, Fugir ←. A direção escolhe e A confirma. Opções impossíveis ficam apagadas (fugir de domador, trocar sem reserva, itens sem estoque).
- **Prévia do golpe:** tipo, poder e precisão, efetividade contra o alvo marcado (Fraco/Normal/Forte, em cores), alvo e uma faixa com o efeito. O alvo é escolhido pelo D-pad ou tocando no esqueleto (1º toque marca, 2º confirma).
- **Repetir último turno:** botão MENU (ou o chip "Repetir turno"). Só aparece quando os dois aliados podem repetir o golpe e o alvo da rodada anterior.
- **Toque na batalha:** tudo é tocável (anel, golpes, alvos, listas, mensagens), então o D-pad e o A/B somem durante a batalha; ficam MENU (repetir) e 2x. Teclado e gamepad seguem iguais.
- **Debug:** F1/Select ou 3 toques na timeline abrem o menu, que agora tem batalhas de teste (1 selvagem, 2 selvagens, domador com 3, chefe +4 níveis), equipe de teste, definir nível da equipe e vencer a batalha.

### Conteúdo de teste (não é conteúdo do jogo)
- As espécies e os golpes reais são das fases 3b/3c. Para testar a batalha agora existem **4 bonecos de treino** (um por tipo) e **12 golpes de teste** em `data/test/`, com nomes próprios de teste nos 3 idiomas (`i18n/test.csv`). Eles só aparecem pelo menu de debug e **ficam fora do AAB de release** (`exclude_filter`). A fase 3 os substitui.
- **Itens reais** (`data/items.json`): Poção P/M/G (30/80/200 PV), Antídoto e Reviver (50%).

## Decisões do Fernando após a fase 2 (idade e batalha nova)

### Nível = idade
- O jogo mostra **idade** ("12 anos", "Age 12", "12 años"); cada nível ganho é um **aniversário** ("Feliz aniversário! X fez 13 anos!", com confete).
- **Idade máxima do jogador: 100.** Inimigos especiais podem chegar a **120** (Rei Esqueleto). O motor limita a criação a 120 e a XP a 100.
- **Estágios:** Bebê → Adolescente → Adulto. As idades de crescimento são por linha (ex.: 28/60).
- **Metas reescaladas ×2** (seção 11 do AGENTS.md): Guardiões aos 22, 34, 46, 58, 70 e 80 anos; Castelo 88–92; Rei 120. A história termina com a equipe por volta dos 80–90 anos.
- **Curva de XP:** XP(idade n) = (n−1)^2,2. Com 100 idades, uma curva cúbica exigiria grind; a final é calibrada pelo simulador na fase 3c.

### Batalha inovadora (não parecer Pokémon)
- **Turnos por tempo, não por rodada.** Cada esqueleto tem um relógio próprio: quem está mais perto de zero age. Depois de agir, volta para a fila com espera = base ÷ VEL × **peso** da ação. Esqueletos rápidos agem mais vezes. A timeline mostra as **próximas 8 ações**.
- **Peso dos golpes:** **Leve** (×0,65, volta logo), **Normal** e **Pesado** (×1,45, demora). Ao escolher um golpe, a timeline mostra um **fantasma** de onde o próximo turno vai cair. Esse é o lugar da "prioridade" da especificação: golpes leves fazem o esqueleto agir de novo mais cedo.
- **Atraso:** golpes com o efeito `delay` empurram o próximo turno do alvo na fila. Servem para quebrar a Sintonia inimiga.
- **Sintonia:** se dois aliados (ou dois inimigos) agem em sequência na timeline, o segundo ganha **+25%** de dano e cura. A timeline liga os dois com um elo ciano. Assim a ordem vira estratégia: golpes leves, trocas e atrasos servem para montar ou desfazer Sintonias.
- **Veneno** conta os turnos do próprio envenenado (3 a 5) e causa dano no início de cada um.
- **Trocar** custa o turno; quem entra espera 0,8 de um turno. **Fugir** e **itens** têm peso normal.
- **Visual:** arena lateral (aliados à esquerda virados para a direita, inimigos espelhados à direita), timeline no topo, faixa de mensagens e detalhes logo abaixo, cartas de nome/idade/PV na base, lista de golpes no centro, etiquetas Forte/Normal/Fraco **sobre os próprios inimigos** e menu em anel em quem age.
- **Repetir:** MENU repete a última ação de quem está agindo.
- **A IA** pondera o valor do golpe pelo peso (valor ÷ √peso) e valoriza atrasar o inimigo.

## Fase 3a — Sistemas dos esqueletos
- **Crescimento acontece no mapa, depois da batalha**, um esqueleto por vez (não no meio do combate), para a cerimônia ter espaço. O aniversário de cada idade continua sendo anunciado na batalha.
- **Marcador:** a base vem da raridade (comum 30%, incomum 25%, raro/único 20%), com +2% por ano que o selvagem tem acima da média do time, entre 20% e 50%. Assim são 2 a 5 vitórias por espécie, e vale a pena enfrentar selvagens mais velhos.
- **Recusar** mantém o marcador em 100%, e a próxima vitória pergunta de novo (`refuse_keeps` em `battle.json`).
- **Direito ao Golden:** guardado por espécie (`golden_right`). Ele só é usado quando o jogador aceita o recruta.
- **Rancho** cura de graça ao abrir. Na troca, escolher o mesmo esqueleto duas vezes o guarda no Rancho; o time nunca fica vazio.
- **Ossário** conta como concluídas só as espécies reais recrutadas; Golden é contado à parte (★).
- **Selvagens no mapa** nascem por zona (`spawns` no JSON do mapa: `{id, table, x, y, radius, count, behavior?}`) e nunca a menos de 3 células do jogador.

## Fase 3b — Bestiário
- **Fonte única em Python** (`tools/bestiary/bestiary.py`). Conceito, nomes, entradas, sprites e dados saem do mesmo lugar, e o validador confere o resultado.
- **Lia e Taro são linhas do bestiário** (Faroleira e Grumete): o parceiro inicial é um bebê da linha com o apelido Lia ou Taro. As duas linhas são "incomuns" e não aparecem selvagens na Praia.
- **Sprites por peças, não por recolor:** cada estágio troca a peça que conta a história (remo de brinquedo → remo → remo duplo; balde → capacete e picareta → armadura de pedra). O corpo segue as proporções da seção C: bebê de cabeça grande, adolescente esguio, adulto de ombros largos.
- **Mapa 16×16 por redução** do sprite de batalha, priorizando as cores das peças. Assim mapa e batalha nunca divergem.
- **Atributos provisórios por papel** (tanque, bruto, veloz, equilibrado, mago, suporte, astuto), escalados para o centro da banda do estágio. A raridade puxa o total para cima. A calibragem final fica para o simulador da fase 3c.
- **Únicos** não crescem e ficam em 490 (banda 450–520). O **Rei** fica em 600. Nenhum deles aparece como selvagem comum.

## Fase 3c — Golpes e balanceamento
- **Golpes de veneno físicos e mágicos:** metade ataca DEF e metade RES. Com todos mágicos, Veneno perdia para tudo (Mágico vencia 97%).
- **Vantagem de tipo ×1,35 / ×0,8** (antes ×1,5 / ×0,75): o tipo ainda pesa, mas não decide sozinho; a timeline e a Sintonia também contam.
- **Cura tem dano próprio** em duas assinaturas (Jato Fresco drena e Badalada Serena atinge todos). As linhas de cura aprendem ataques do tipo secundário. Mesmo assim, Cura perde duelos puros, porque é tipo de suporte.
- **Taro × Lia:** com o mesmo time, Lia vencia quase sempre. Taro (Grumete) virou perfil tanque e ganhou Cura como secundário. Agora os dois ficam entre ~65% e 90% contra os Guardiões.
- **XP achatada por estágio** (60/68/68 × idade ÷ 18). A curva (n−1)^2,2 já cresce com a idade; a base por estágio não precisa crescer junto.
- **Simulador em GDScript headless:** usa o mesmo `BattleEngine` e a mesma `BattleAI` do jogo, então um ajuste de regra entra na simulação sem duplicar código.
- **Guardiões e tempo são protótipos.** As equipes, os mapas e o roteiro da fase 4 substituem os valores do `balance.json`, e a simulação é repetida a cada tarefa da fase 4.

## Fase 4a — Arco e Prólogo
- **Por que o protagonista veio de 2040:** ele é o último descendente do Rei. A coroa está rachando e só se refaz na cabeça de alguém do mesmo sangue; por isso o eco dela o puxou do museu onde ela estava exposta mil anos depois. Isso amarra o título, o farol de Lia (que em 2040 é o museu) e os Guardiões-família pedidos pelo Fernando.
- **Esqueletos = segunda vida:** os mortos renascem bebês e envelhecem de novo, e isso explica "nível = idade" e os aniversários dentro da história.
- **Ações dentro do diálogo** (em vez de cenas em código): todo o roteiro fica em JSON, e o Prólogo inteiro é dado. Novas regiões só precisam de mapas, NPCs e roteiros.
- **Domador por linha de visão** (seção 7): enxerga N células à frente até o primeiro obstáculo; cada um luta uma vez só (flag).
- **Parceiro inicial tem apelido** (Lia/Taro) e é uma espécie comum do Bestiário. O recorrente usa a outra linha.
- **Estrada norte bloqueada pelo Brás** (arbusto + NPC numa célula só): obriga a 1ª batalha contra domador sem parede invisível.

## Fase 4b — Bosque
- **Raízes no lugar de "estrada fechada por NPC":** o problema local (o Guardião isolou a vila) vira o motivo dos 3 caminhos da Rota 1. Vencer o Guardião abre o atalho central, que muda o mundo de forma visível.
- **Túnel escuro por tinta do mapa** (`tint`) com cogumelos que emitem luz: o momento de Lia ("eu tenho luz") acontece no próprio cenário.
- **Guardiões são esqueletos no mapa** (sprite adulto da linha que lideram), coerente com o arco: são a família ressuscitada pela coroa.
- **Fundo de batalha por região** (`battle_bg` em `regions.json`).
- **Idades coerentes com o estágio** também em domadores e Guardiões (o teste confere). Por isso Vagalú aparece aos 22 e os Irmãos Galho usam bebês.

## Fase 4c — Minas e kit de região
- **Uma fonte por região** (`tools/maps/<regiao>.py` + `regionkit.py`): o documento de roteiro é gerado das mesmas estruturas que viram JSON do jogo. A regra "implemente exatamente o roteiro" vira garantia mecânica, não disciplina.
- **Layouts padrão** de rota (3 caminhos que se reencontram), cidade (Rancho, Loja, 3 casas, praça) e covil do Guardião. Cada região muda terreno, objetos, clima, NPCs e história; a forma constante ajuda o jogador a se orientar e permite testes genéricos.
- **Saídas com condição** (`if` no warp + `locked_message`) em vez de NPC bloqueando: o mundo abre por história sem paredes invisíveis.
- **Escolha 2 sem "certo e errado" óbvio:** quebrar dá um único recrutável (Vagonauta) e encarece a loja; negociar dá atalho, desconto e Redenção. Os dois têm ganho.
- **Clima por região** com uma única função de partículas (cinza, névoa, neve, areia, brasas), limitada pela área do mapa para manter 60 FPS.

## Fases 4d–4h — Regiões, finais e pós-jogo
- **Escolhas com custo dos dois lados.** Doar antídotos (escolha 3) só é possível se o jogador os tiver: a loja do Brejo não vende antídoto (a Musga compra todos), então a escolha pesa de verdade. Contar o registro (escolha 4) dá Redenção mas cria batalhas extras na Rota 5.
- **A carta da Alva pode ser aceita depois.** Recusar não fecha o Final A para sempre; o jogador pode voltar ao Jardim de Gelo. A escolha continua sendo do jogador, sem punição por curiosidade.
- **Colocar a coroa não é um terceiro final.** A especificação pede 2 finais; tentar colocar a coroa leva o parceiro a impedir, o que reforça o arco dele e evita um "game over" narrativo.
- **Guardiões viram "ecos" no pós-jogo.** Nos dois finais a família descansa ou some; a revanche pedida pela seção 6 acontece com os ecos deles, coerente com a coroa do eco e o Deserto dos Ecos.
- **O Rei entra com idade 100** (a idade máxima do jogo), não 120: o 120 é a idade dele como chefe.
- **Texto transversal numa fonte só** (`extras.py`): reações do mundo, cartas do Bento e pós-jogo são acrescentadas às listas de diálogo dos NPCs, sem editar as fontes de cada região. `build_all.py` garante a ordem.

## Correção — toque duplo no celular
- **Um toque, uma ação.** O Android emula um clique de mouse para cada toque; os botões virtuais ficam sobre a caixa de diálogo e os menus. Os controles de toque (que recebem a entrada antes da interface) descartam o clique emulado quando ele cai num botão virtual. Além disso, o A do mapa ignora toques nos 300 ms depois de fechar qualquer tela sobreposta, para nenhuma conversa reabrir sozinha.

## Os dois iniciais na equipe (decisão do Fernando)

- **Problema:** começar com um esqueleto só deixava o Prólogo difícil demais nas batalhas 2×2.
- **Decisão:** Bento entrega **Lia e Taro juntos**; a escolha do Prólogo deixou de existir (o jogo continua com 4 escolhas relevantes: Minas, Pântano, Ossório e Picos). Os dois são parceiros fixos, marcados como `starter` no save, com **+5% em todos os atributos** (`battle.json → starter.stat_bonus`, somado ao +10% do Golden quando houver).
- **Falas:** como as duas flags (`partner_lia` e `partner_taro`) ficam ligadas, as falas de parceiro dos dois tocam em todas as cenas. Revisamos as cenas em que um falava do outro como ausente (portão e trono do Castelo, epílogo, livro do farol em Ossório, revelação da Musga) e criamos 4 falas novas para a versão em dupla.
- **Recorrente:** as aparições do "recorrente" (lutas opcionais na Vila, no Bosque, em Ossório e nos Picos; Lia no túnel e no arquivo; Taro na mina, no brejo e no portão; pós-jogo) só aparecem em saves antigos com um parceiro só (`if_none: [flag do próprio]`). Não somem do código para que esses saves continuem coerentes.
- **Save v2:** `partner_uid` virou a lista `partner_uids`; a migração marca o parceiro antigo como inicial.
- **Simulador:** a equipe típica passa a ser Lia + Taro + 2 recrutas da região (`balance.json → team` com `@starters`).

## Refinamento dos mapas (pedido do Fernando)

- **Revisão:** `tools/screenshots/make_map_sheet.py` gera `docs/mapas_sheet.png` com os 24 mapas externos na ordem da história, com as zonas dos selvagens e a faixa de idade marcadas (a mesma ideia do `bestiario_sheet.png`).
- **Primeiro passe (automático, `tools/maps/refine.py`, último passo do `build_all.py`):** bordas de mata/rocha irregulares (duas camadas), árvores e pedras por cima das massas de mata/rocha (dão volume sem mudar a passagem), manchas de flores e detalhes por região (conchas, tocos, cogumelos, juncos, cactos, pinheiros nevados...). Cada objeto que bloqueia só entra se todos os destinos continuam alcançáveis e nenhum bolsão de chão fica isolado; trilhas, portas, NPCs, objetos interativos e zonas de selvagens ficam protegidos.
- **Tiles:** grama com tufos, pedrinhas e trevos (variantes raras), 4 variantes de mata e uma trilha com marcas de roda.
- **Raizal** ganhou casas próprias de toras com telhado de musgo (antes repetia as casas da Vila Maré).
- Próximos passes dependem do retorno do Fernando no teste (traçado das trilhas, tamanho das áreas, pontos de interesse).
- **Segundo passe (retorno do Fernando: trilhas retas, áreas vazias, falta de pontos de interesse):** trilhas longas das rotas viram curvas suaves (trilha e chão são passáveis, então a passagem não muda; as pontas perto de portas, cruzamentos e portões ficam no lugar); riachos com ponte de tábuas atravessando as rotas; pontos de interesse nas áreas vazias, por região (lagos com vitórias-régias e juncos, ruínas, bosquinhos, fogueiras, cristais e vagonete abandonado nas Minas, lago gelado e boneco de neve nos Picos, oásis no Deserto). Eles podem substituir decoração simples (árvores, tocos, pedras), nunca algo interativo. O tamanho dos mapas foi mantido: as áreas grandes agora têm o que explorar, e mudar o tamanho mexeria em todas as portas e roteiros.

## Viagem rápida (pedido do Fernando)

- **Onde:** pausa → **Viajar**, desde o começo do jogo. Lista só as cidades já visitadas, na ordem da história; a cidade atual aparece apagada ("você está aqui"). Sem cidades visitadas, o menu explica que elas aparecem depois da primeira visita.
- **Visitada** = entrou no mapa da cidade (`visited_cities` no save). Saves antigos: o progresso conta (venceu o líder da região → a cidade dele vale como visitada; `data/travel.json → visited_by_flag`).
- **Chegada:** na porta do Rancho (cura e equipe logo ali), com autosave e o evento de entrada do mapa, como uma porta comum.
- **Bloqueios:** nas cenas finais (`museu_2040`, `sala_trono`) a opção fica apagada. Nada mais é bloqueado: como só há destinos já visitados, a viagem nunca adianta a história.
- Testes: `tests/test_travel.gd`. Captura: `capture.tscn -- --travel`.

## Retorno do teste do Fernando (troca, itens e derrota)

- **Troca quando um esqueleto desmaia não aceitava o A:** as linhas da equipe e dos itens na batalha mostravam o PV/quantidade como um "valor ajustável" (como nas Configurações), e o A tentava ajustar o valor em vez de escolher. Agora essas linhas são só informativas (`fixed`). O teste de interface passa pelo mesmo caminho do botão A (`MenuList.activate_current`), e há um teste específico da troca forçada; os dois falham sem a correção.
- **Itens renomeados** (decisão 8 da seção C): nomes ligados à praia, aos ossos e aos aniversários. Todas as falas que citavam poção, antídoto ou reviver foram reescritas nos 3 idiomas. As descrições continuam curtas porque precisam caber na faixa da loja e da mochila.
- **Fala do resgate** (decisão 9): `Game._rescue_talk`. A taxa é a mesma da regra de derrota (`battle.json → defeat.money_loss`); com o premiado "reviver sem perder moedas", a fala diz que não cobrou nada.

## Refino geral (pedido do Fernando)

- **Toque na batalha:** golpes em linhas de 18 px com 3 px de folga (antes 15 px colados); listas de troca/itens com linhas de 17 px; ícones do anel com área de toque de 24 px.
- **Apresentação de Lia e Taro:** entrada com briga de quem chegou primeiro, a Lia percebendo que o protagonista "não é esqueleto" (roupa de 2040), o remo do Taro quase apagando a lamparina e um pacto de mãos (escolha: pôr a mão ou hesitar).
- **Batalha final:** fundo próprio (sala do trono com o trono gigante, a coroa rachada e velas) e momentos roteirizados (`info.script`, `BattleScreen._run_script`): abertura do Rei; a 70% do PV a coroa "pesa o tempo" (atrasa a dupla em campo); a 40% Lia e Taro viram o jogo (+1 ATQ/MAG/VEL e 30% de cura neles); a 15% a coroa racha (Rei com −1 DEF/RES/VEL) e ele confessa que só queria a família de volta. Com flash e tremor de tela.
- **+15 esqueletos (decisão 10):** 3 linhas novas, uma por região que tinha só 3 linhas e em tipos que estavam abaixo (Veneno, Mágico, Físico → 7/7/6/7 linhas), e 6 ases dos Guardiões. O ás lidera a equipe do Guardião e entra mais novo (únicos têm atributos de adulto); o validador agora compara os selvagens com a **idade média** da equipe do líder. Ajustes no simulador: Troncudo 16 (Ramalho estava em 42%), Miragina 86 (Duna em 85%); resultado dentro das metas. No pós-jogo, vencer o eco de um Guardião dá o ás dele (uma vez), com uma fala de despedida de cada Guardião.

### Revisão de conformidade (06/10/2026)
- **Teto de conteúdo dos anúncios: PG** (antes T). A política de anúncios do Google Play pede anúncios adequados à classificação do app, e o jogo deve sair como 10+/PEGI 7/Livre–10; anúncios "T" (adolescente) passariam disso. Vale no código (`data/ads.json → audience.max_rating`, teste em `tests/test_ads.gd`) e deve ser repetido no AdMob (Bloqueio de controles → Classificação de conteúdo). Política de privacidade e `PLAY_CONSOLE.md` atualizados; política vigente desde 06/10/2026.
- **Clarão de entrada na batalha:** eram 3 clarões brancos de tela inteira em 0,4 s (~7 por segundo), acima do limite usual de 3 por segundo para fotossensibilidade. Agora são 2 clarões mais suaves (60%) em ~0,7 s, e um só no 2x.
- **Capturas da loja** refeitas com a versão atual (batalha com alvos maiores, 95 espécies, sala do trono): `tools/store/gen_store_shots.py` gera as 7 capturas 1280×720 nos 3 idiomas a partir do jogo rodando.

### Publicação só pelo navegador (06/10/2026)
- **Site da produtora:** GitHub Pages grátis em `https://fefaofefao.github.io` (repositório público `fefaofefao.github.io`), com a política em PT/EN/ES e o `app-ads.txt` na raiz. `github.io` está na Public Suffix List, então o `app-ads.txt` na raiz do subdomínio vale para o AdMob. Arquivos gerados em `site/` pelo `gen_store_docs.py`; para outro domínio, basta trocar o `publisher.json`.
- **ID de editor:** não fica no repositório; o release o deriva do Secret `ADMOB_APP_ID` (`ca-app-pub-<16 dígitos>~…` → `pub-<16 dígitos>`) só no runner, e publica o artefato `site-da-produtora` com o `app-ads.txt` pronto.
- **Keystore de upload:** gerada pelo workflow `keystore.yml` (Java do runner, RSA 4096, PKCS12, ~30 anos), entregue num artefato de 1 dia para virar Secrets. Recusa sobrescrever uma keystore que já esteja nos Secrets. Com a Assinatura de apps do Google Play, é só a chave de upload.
- Roteiro completo em `docs/PUBLICAR_PELO_NAVEGADOR.md`.
