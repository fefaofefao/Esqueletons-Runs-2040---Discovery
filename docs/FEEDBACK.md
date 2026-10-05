# Feedback do Fernando

Anote aqui as correções. **A próxima tarefa aplica tudo o que estiver em "Aberto" antes de qualquer outra coisa**, depois move cada item para "Resolvido", com o commit.

Formato sugerido:
```
- [ ] (fase/tela) o que está errado → o que deveria acontecer
```

## Aberto
_(vazio)_

## Resolvido
- [x] (Prólogo/equipe) Difícil passar do começo com um esqueleto só → Lia e Taro entram juntos na equipe, sem escolha, e os dois iniciais têm +5% em todos os atributos (`battle.json → starter.stat_bonus`). Falas revisadas para a dupla; simulador refeito com os dois.
- [x] (celular/diálogos) Ao terminar uma conversa, ela recomeçava sozinha e prendia o jogador → corrigido. Causa: no Android, cada toque no botão A virtual também gera um clique de mouse "emulado"; como o A fica por cima da caixa de diálogo, o clique fechava a conversa e a ação A chegava em seguida ao mapa, falando de novo com o NPC. Agora os controles de toque descartam o clique emulado que cai num botão virtual (vale para diálogos e todos os menus) e o A do mapa espera 0,3 s depois de fechar qualquer diálogo. Teste de regressão em `tests/test_player.gd`.
