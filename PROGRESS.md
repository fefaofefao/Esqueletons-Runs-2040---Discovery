# Progresso

Jogo: **Esqueletons Runs 2040 — Edição Discovery** (primeiro da série).
Especificação: `AGENTS.md`. Decisões: `docs/DECISOES.md`. Correções do Fernando: `docs/FEEDBACK.md`.

| Fase | Estado |
|---|---|
| 1 — Base | ✅ concluída (APK de debug pelo CI) |
| 2 — Batalha | ⏳ próxima |
| 3a/3b/3c — Esqueletos | — |
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

### Pendências e observações
- **Package name** `com.fsamplabs.esqueletonsruns2040.discovery`: confirmar antes da primeira publicação (não muda depois).
- `config/publisher.json` ainda tem placeholders (produtora, sobrenome, e-mail, site). O release fica bloqueado até preencher.
- Os diálogos do Bento e os objetos da cabana são provisórios. A fase 4a escreve `docs/roteiro/00_arco.md` e o roteiro do Prólogo, e eles podem ser substituídos.
- Música: nenhuma ainda (fase 6). O sistema de áudio já tem barramentos Music/SFX e volume.
- Vibração usa `performHapticFeedback` (sem permissão extra). Precisa ser conferida num aparelho real.
- "Privacidade e anúncios" mostra um aviso até a fase 5 (UMP).

### Próxima tarefa: Fase 2 — Batalha
Sistema 2×2, menu em anel, timeline de turnos, prévia do golpe, "repetir último turno", tipos e vantagens, fórmula de dano, veneno, XP, níveis, fuga e derrota.
