# Checklist final (seção 17 do AGENTS.md)

Estado em 06/10/2026. ✅ = feito e verificado por ferramenta ou teste · 🟡 = feito, falta um passo do Fernando · ⬜ = pendente.

| Item | Estado | Como foi verificado |
|---|---|---|
| Conteúdo 100% original; `CREDITS.md` completo | ✅ | Arte, sons e música gerados pelos scripts em `tools/art` e `tools/audio`; fontes OFL e o plugin AdMob (MIT) registrados em `CREDITS.md` |
| `validate_data.py` passando | ✅ | CI, job "Validação e testes" |
| `check_placeholders.py` passando | ✅ | Site definido (`https://fefaofefao.github.io`); o ID de editor sai do Secret `ADMOB_APP_ID` no release |
| Simulador dentro das metas (Guardiões 60–85%, 2h45–3h15, sem grind) | ✅ | `python3 tools/simulate.py --check` → `docs/BALANCEAMENTO.md` (com Lia e Taro juntos, +5%) |
| 3 idiomas completos, sem overflow, troca em tempo real | ✅ | `tests/test_i18n.gd` e `tests/test_text_overflow.gd`; a revisão humana das traduções fica no teste fechado |
| Golden: taxa 1/40, regra de 99%, shader em todos os estágios | ✅ | `tests/test_growth.gd` (100 mil sorteios ±5%, direito ao Golden) |
| Crescimento no nível certo, animação ao lado do jogador, respeita 2x | ✅ | `tests/test_growth.gd` |
| Toda cidade com rancho, loja e 2–3 casas; rotas com caminhos alternativos | ✅ | `validate_data.py` e `tests/test_regions.gd` |
| Rei entra na equipe nos dois finais; pós-jogo | ✅ | `tests/test_regions.gd` |
| targetSdk ≥ 35, AAB assinado, 16 KB | 🟡 | Preset com targetSdk 36 e `tools/check_16kb.py` no CI. O AAB assinado sai quando os Secrets existirem (keystore gerada pelo workflow **Gerar keystore de upload**) |
| UMP antes dos anúncios; IDs reais só no release; anúncios só nos pontos permitidos | ✅ | `tests/test_ads.gd` (inclui público 13+ não infantil e teto PG dos anúncios); `tools/admob_ids.py` recusa IDs de teste no release; `tools/check_manifest.py` confere as permissões do APK |
| Jogo completável offline; save/load testado | ✅ | Sem rede no código do jogo (só o SDK de anúncios, opcional); `tests/test_save.gd` (inclui migração v1 → v2) |
| Política de privacidade publicada; `PLAY_CONSOLE.md` pronto | 🟡 | Gerados (`privacy/`, `PLAY_CONSOLE.md`); capturas da loja refeitas com a versão atual (`tools/store/gen_store_shots.py`). Falta publicar a política e o `app-ads.txt` no site |

## O que falta (tudo pelo navegador)
Passo a passo em **`docs/PUBLICAR_PELO_NAVEGADOR.md`**, com um prompt pronto para a sessão que controla o navegador:
1. Site no GitHub Pages (`https://fefaofefao.github.io`, arquivos em `site/`).
2. AdMob: app, 3 blocos, classificação PG, mensagens de consentimento; Secrets `ADMOB_*`.
3. Keystore pelo workflow **Gerar keystore de upload** e os 3 Secrets `ANDROID_*`.
4. AAB pelo **Build** com *release* marcado (o ID de editor sai do `ADMOB_APP_ID`).
5. Play Console: app, conteúdo do app (`PLAY_CONSOLE.md`), ficha nos 3 idiomas e teste fechado (12 testadores por 14 dias).
