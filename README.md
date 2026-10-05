# Esqueletons Runs 2040 — Edição Discovery

RPG mobile de coleta de esqueletos, com pixel art no estilo "GBA aprimorado". Primeiro jogo da série *Esqueletons Runs 2040*. Feito em Godot 4.7, para Android (Google Play).

- Especificação completa: [`AGENTS.md`](AGENTS.md)
- Progresso: [`PROGRESS.md`](PROGRESS.md) · Decisões: [`docs/DECISOES.md`](docs/DECISOES.md)
- Build e publicação: [`docs/BUILD.md`](docs/BUILD.md) · Formato dos dados: [`docs/DADOS.md`](docs/DADOS.md)
- Correções para a próxima tarefa: [`docs/FEEDBACK.md`](docs/FEEDBACK.md)

## Começo rápido
```bash
tools/setup_codex.sh     # baixa o Godot 4.7.2 e importa o projeto
tools/check_all.sh       # validação de dados + testes headless
godot --path .           # jogar no desktop
```
Teclado: setas/WASD, **Z** = A, **X** = B (segurar corre), **Esc** = menu, **F** = 2x, **F1** = debug.

O APK de debug é gerado pelo GitHub Actions a cada push (aba *Actions* → *Artifacts*).
