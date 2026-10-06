# Build e publicação

## O que o GitHub Actions faz (`.github/workflows/build.yml`)
| Gatilho | Jobs |
|---|---|
| Qualquer push ou PR | **Validação e testes** (validate_data, autoteste do validador, publisher sincronizado, placeholders como aviso, testes headless do Godot) → **APK de debug** (artefato `esqueletons-debug-apk`, com checagem de páginas de 16 KB) |
| Tag `v*` (ex.: `v0.1.0`) ou "Run workflow" com *release* marcado | Tudo acima + **AAB de release assinado** (artefato `esqueletons-release-aab`) |

O APK de debug fica em **Actions → execução → Artifacts**. Instale com `adb install -r esqueletons-debug.apk` ou abrindo o arquivo no aparelho.

## Secrets necessários (só para o release)
Configure em **Settings → Secrets and variables → Actions** do repositório:

| Secret | Conteúdo |
|---|---|
| `ANDROID_KEYSTORE_BASE64` | o arquivo `.keystore` em base64 |
| `ANDROID_KEYSTORE_PASSWORD` | senha do keystore (o Godot usa a mesma para a chave) |
| `ANDROID_KEY_ALIAS` | alias da chave |
| `ADMOB_APP_ID` e IDs dos blocos | fase 5 |

Para criar o keystore uma única vez **sem instalar nada**: Actions → **Gerar keystore de upload** → *Run workflow*. O artefato (vale 1 dia) traz os 3 valores; grave os Secrets, guarde `upload-keystore.jks` e a senha num lugar seguro e apague o artefato. O workflow se recusa a gerar outra chave se o Secret já existir.

Nunca faça commit do keystore: o `.gitignore` bloqueia `*.keystore`, `*.jks` e `*.p12`. Ative a **Assinatura de apps do Google Play**, para que essa chave seja só a de upload.

## Antes do primeiro release
Passo a passo completo, feito só pelo navegador: **`docs/PUBLICAR_PELO_NAVEGADOR.md`**. Em resumo:
1. O site da produtora é `https://fefaofefao.github.io` (GitHub Pages gratuito). Os arquivos estão em `site/`. Para usar outro domínio, troque `website` e `privacy_policy_url` em `config/publisher.json` e rode `python3 tools/sync_publisher.py`.
2. O ID de editor do AdMob (`pub-...`) não precisa ser editado: se estiver como placeholder, o release o tira do Secret `ADMOB_APP_ID`. O artefato `site-da-produtora` do release já traz o `app-ads.txt` preenchido.
3. Gere o AAB: Actions → **Build** → *Run workflow* com *release* marcado (ou crie a tag `v0.1.0`).

## Rodar localmente
```bash
tools/setup_codex.sh            # baixa o Godot 4.7.2 e importa o projeto
tools/check_all.sh              # mesma verificação do CI (sem o APK)
godot --path .                  # joga no desktop (teclado/gamepad; o mouse simula toque)
tools/art/gen_all.sh            # regenera toda a arte e os sons (precisa de Pillow)
```
Para exportar o APK localmente, também são necessários o Android SDK (API 36, build-tools 36), o JDK 17 e os export templates (`tools/setup_codex.sh --with-templates`).

## Requisitos Android atendidos pelo preset
- `targetSdk 36`, `minSdk 24`, build Gradle, arm64-v8a + armeabi-v7a.
- Permissões: só `INTERNET`, `ACCESS_NETWORK_STATE` e `com.google.android.gms.permission.AD_ID`.
- Páginas de 16 KB: verificadas no CI por `tools/check_16kb.py`.
