# Progresso

Jogo: **Esqueletons Runs 2040 — Edição Discovery** (primeiro da série).
Especificação: `AGENTS.md`. Decisões: `docs/DECISOES.md`. Correções do Fernando: `docs/FEEDBACK.md`.

| Fase | Estado |
|---|---|
| 1 — Base | ✅ concluída (APK de debug pelo CI) |
| 2 — Batalha | ✅ concluída |
| 3a — Sistemas dos esqueletos | ✅ concluída |
| 3b/3c — Bestiário e balanceamento | ⏳ próxima (3b) |
| 4a–4h — História e mundo | — |
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

### Próxima tarefa: Fase 3b — Bestiário
24 linhas × 3 estágios + 7 únicos + Rei, nomes nos 3 idiomas, sprites de batalha e de mapa, `species.json` e folha de revisão.
