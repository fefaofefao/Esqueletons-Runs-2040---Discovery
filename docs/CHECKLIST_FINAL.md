# Checklist final (seção 17 do AGENTS.md)

Estado em 05/10/2026. ✅ = feito e verificado por ferramenta ou teste · 🟡 = feito, falta um passo do Fernando · ⬜ = pendente.

| Item | Estado | Como foi verificado |
|---|---|---|
| Conteúdo 100% original; `CREDITS.md` completo | ✅ | Arte, sons e música gerados pelos scripts em `tools/art` e `tools/audio`; fontes OFL e o plugin AdMob (MIT) registrados em `CREDITS.md` |
| `validate_data.py` passando | ✅ | CI, job "Validação e testes" |
| `check_placeholders.py` passando | 🟡 | Passa no debug. No release falha de propósito até o Fernando preencher `[URL]` e `[ADMOB_PUB_ID]` em `config/publisher.json` |
| Simulador dentro das metas (Guardiões 60–85%, 2h45–3h15, sem grind) | ✅ | `python3 tools/simulate.py --check` → `docs/BALANCEAMENTO.md` (com Lia e Taro juntos, +5%) |
| 3 idiomas completos, sem overflow, troca em tempo real | ✅ | `tests/test_i18n.gd` e `tests/test_text_overflow.gd`; a revisão humana das traduções fica no teste fechado |
| Golden: taxa 1/40, regra de 99%, shader em todos os estágios | ✅ | `tests/test_growth.gd` (100 mil sorteios ±5%, direito ao Golden) |
| Crescimento no nível certo, animação ao lado do jogador, respeita 2x | ✅ | `tests/test_growth.gd` |
| Toda cidade com rancho, loja e 2–3 casas; rotas com caminhos alternativos | ✅ | `validate_data.py` e `tests/test_regions.gd` |
| Rei entra na equipe nos dois finais; pós-jogo | ✅ | `tests/test_regions.gd` |
| targetSdk ≥ 35, AAB assinado, 16 KB | 🟡 | Preset com targetSdk 36 e `tools/check_16kb.py` no CI. O AAB assinado sai quando os Secrets da keystore existirem (`docs/BUILD.md`) |
| UMP antes dos anúncios; IDs reais só no release; anúncios só nos pontos permitidos | ✅ | `tests/test_ads.gd`; `tools/admob_ids.py` recusa IDs de teste no release; `tools/check_manifest.py` confere as permissões do APK |
| Jogo completável offline; save/load testado | ✅ | Sem rede no código do jogo (só o SDK de anúncios, opcional); `tests/test_save.gd` (inclui migração v1 → v2) |
| Política de privacidade publicada; `PLAY_CONSOLE.md` pronto | 🟡 | Gerados (`privacy/`, `PLAY_CONSOLE.md`). Falta publicar a política e o `app-ads.txt` no site |

## O que só o Fernando pode fazer
1. Comprar/definir o site e preencher `website`, `privacy_policy_url` e `admob.publisher_id` em `config/publisher.json`; depois rodar `python3 tools/sync_publisher.py`.
2. Publicar `privacy/*.html` e `app-ads.txt` no site.
3. Criar o app e os 3 blocos no AdMob e gravar os Secrets `ADMOB_APP_ID`, `ADMOB_BANNER_ID`, `ADMOB_INTERSTITIAL_ID` e `ADMOB_REWARDED_ID`.
4. Criar a keystore e gravar `ANDROID_KEYSTORE_BASE64`, `ANDROID_KEYSTORE_PASSWORD` e `ANDROID_KEY_ALIAS`.
5. Criar a tag `v0.1.0` para gerar o AAB e seguir o `PLAY_CONSOLE.md` (teste fechado de 12 testadores por 14 dias se a conta for nova).
6. Ouvir as músicas e jogar o teste fechado; anotar ajustes em `docs/FEEDBACK.md`.
