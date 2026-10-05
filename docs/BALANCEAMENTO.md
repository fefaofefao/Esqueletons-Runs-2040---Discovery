# Balanceamento

Gerado por `tools/simulate.py` (simulador `tools/sim/simulate.gd`, que usa o motor e a IA reais da batalha e os dados reais). Metas em `data/balance.json`; regras em `data/battle.json`. Repita a simulação ao fim de cada tarefa das fases 3c e 4.

**40 jogadas simuladas** (Lia e Taro juntos na equipe, com +5% de inicial), 10 tentativas por Guardião em cada jogada.

## Critérios de aceite

- ✅ Todos os critérios da seção 11 foram atendidos.

## Por região

| Região | Chegada (meta) | Idade no Guardião (meta) | Vitória contra o Guardião | Batalhas | Derrotas | Tempo (min) |
|---|---|---|---|---|---|---|
| Prólogo | 5.0 (5–5) | 9.5 (—) | — | 5 | 0.0 | 15.1 |
| Bosque | 9.6 (10–18) | 20.5 (22.0) | 68% | 14 | 1.1 | 23.3 |
| Minas | 22.6 (22–30) | 33.6 (34.0) | 74% | 14 | 0.8 | 22.8 |
| Pântano | 36.1 (34–42) | 46.8 (46.0) | 81% | 13 | 0.2 | 20.9 |
| Ossório | 50.4 (46–54) | 59.5 (58.0) | 66% | 11 | 0.1 | 22.5 |
| Picos | 62.3 (58–66) | 71.1 (70.0) | 60% | 10 | 0.1 | 22.1 |
| Deserto | 73.9 (68–76) | 82.3 (80.0) | 72% | 10 | 0.1 | 21.0 |
| Castelo | 85.6 (80–86) | 90.4 (90.0) | 80% · Rei 68% | 7 | 0.1 | 21.6 |
| **Total** | | | | | | **169 min (2h49)** |

Tempo = batalhas × duração simulada (ação do jogador 4.5 s, do inimigo 2.4 s, +9 s de abertura/fim) + caminhada + leitura a 180 palavras/min. Caminhada e leitura são o **orçamento** de cada região para a fase 4 (mapas e roteiro ainda não existem); a fase 4 deve medir os valores reais e repetir a simulação.

## Tipos (duelos 2×2 na mesma idade: 20, 50 e 80 anos)

| Tipo | Vitória geral | vs Físico | vs Mágico | vs Cura | vs Veneno |
|---|---|---|---|---|---|
| Físico | 48% | — | 67% | 62% | 16% |
| Mágico | 65% | 41% | — | 75% | 79% |
| Cura/Suporte | 35% | 35% | 31% | — | 38% |
| Veneno | 54% | 86% | 19% | 57% | — |

Ciclo de vantagem: Físico > Mágico > Veneno > Físico; Cura é neutra (vale ×1,35 / ×0,8). Cura perde duelos de dano por definição: é tipo de suporte e brilha em equipe mista.

## Golpes mais usados pelo jogador

| Golpe | Uso |
|---|---|
| remada_dupla (fisico, normal) | 27.3% |
| facho_do_farol (magico, normal) | 11.5% |
| chama_fria (magico, normal) | 10.3% |
| chuva_de_brasas (magico, normal) | 8.6% |
| explosao_arcana (magico, heavy) | 6.8% |
| investida (fisico, heavy) | 5.5% |
| soco_seco (fisico, heavy) | 3.2% |
| cabecada (fisico, normal) | 2.8% |
| osso_bumerangue (fisico, normal) | 2.7% |
| raio_lunar (magico, heavy) | 2.7% |

Limite: nenhum golpe acima de 30%.

## Modelo da jogada típica
- Enfrenta ~70% dos selvagens que cruzam a rota (`wild_crossings`) e todos os domadores (`tamers`); 30% dos encontros têm 2 selvagens.
- Equipe recrutada mais provável por região (`team` em `balance.json`); quem entra no time chega com a idade dos selvagens da região.
- IA do jogador: melhor dano esperado, cura abaixo de 35% de PV, valor por tempo (peso do golpe). Selvagens erram 25% das vezes.
- Após cada batalha a equipe é curada (poções/Rancho), os crescimentos acontecem e golpes novos substituem o de menor poder.
- Guardiões: protótipos com linhas da região na idade-meta, até a fase 4 definir as equipes do roteiro.

## O que foi ajustado

| Assunto | Problema encontrado | Ajuste |
|---|---|---|
| XP por inimigo | base_xp por estágio 50/110/180 e divisor 5 faziam a idade disparar (Bosque aos 44 anos). | base_xp achatado (60/68/68) e `xp.reward_div` = 18: a recompensa cresce na mesma proporção da curva (n−1)^2,2. |
| Faixa de idade dos selvagens | Selvagens de até 18 anos no Bosque (já adolescentes) derrotavam o time de 10 anos. | Selvagens começam na idade de chegada e vão até +5; domadores +2 acima disso. |
| Golpes de veneno | Todos eram mágicos: Veneno batia na RES alta dos magos e ainda tinha desvantagem de tipo (Mágico vencia 97%). | Picada, Cuspe Ácido, Chuva de Espinhos e Ferrão das Dunas passaram a ser físicos. |
| Ordem de aprendizado | A rotação dos golpes deixava o Físico com golpes fracos nas idades em que o Mágico já tinha os médios. | Escadas de poder iguais entre os tipos; a variedade vem do tipo secundário e da assinatura. |
| Perfis de atributo | 3 das 6 linhas físicas são tanques lentos; as duas linhas velozes eram mágicas. | Tanque: ATQ 1,25 e VEL 0,85; mago: MAG 1,15; veloz: VEL 1,25; Escultor passou a astuto. |
| Vantagem de tipo | ×1,5 / ×0,75 criava duelos decididos só pelo tipo. | ×1,35 / ×0,8. |
| Cura/Suporte | Sem dano próprio, as linhas de cura só perdiam duelos. | Jato Fresco (drena) e Badalada Serena (atinge todos) viraram golpes de dano; as linhas de cura aprendem ataques do tipo secundário. |
| Taro × Lia | Com a mesma equipe, Lia vencia ~100% dos Guardiões e Taro 0–50%. | Taro (Grumete) virou perfil tanque e ganhou Cura como secundário (como Lia); Remada Dupla 2×50, Facho do Farol 60. |
| Guardiões (protótipos) | Bosque e Minas cheios de Veneno anulavam times físicos; os últimos Guardiões ficavam fáceis. | Bosque com um de cada tipo (o Pântano continua temático de Veneno); Ossório +4 anos, Deserto +5, Pântano +2; Rei com uma escolta de suporte. |
| Os dois iniciais juntos (+5%) | Com Lia e Taro na equipe desde o Prólogo, a equipe vencia 100% dos Guardiões, perdia menos e chegava 4–7 anos acima da meta; Remada Dupla passou de 30% de uso. | `xp.reward_div` 18 → 21; Guardiões com +7% em todos os atributos (`enemy_bonus.boss`, o Rei fica de fora); Remada Dupla 2×50/15 PP → 2×40/12 PP. |
