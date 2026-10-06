# Publicar pelo navegador — do zero ao teste fechado

Roteiro para uma sessão do Claude que controla o navegador do Fernando (ou para o próprio Fernando). Tudo aqui se faz só no navegador: GitHub, AdMob e Google Play Console. Nada precisa ser instalado no computador.

Repositório: `github.com/fefaofefao/Esqueletons-Runs-2040---Discovery` (branch padrão `ccr-446065e1-6l6vp4`).
Respostas prontas dos formulários do Google Play: **`PLAY_CONSOLE.md`** (na raiz do repositório).

---

## Prompt para colar na sessão do navegador

> Siga o arquivo `docs/PUBLICAR_PELO_NAVEGADOR.md` do repositório `fefaofefao/Esqueletons-Runs-2040---Discovery` no GitHub, etapa por etapa, na ordem. Use as respostas do `PLAY_CONSOLE.md` e os arquivos das pastas `site/` e `store/` do mesmo repositório. **Pare e me chame** sempre que aparecer: login ou senha, pagamento, verificação de identidade, código de dois fatores, aceite de termos legais, ou qualquer dúvida. Nunca cole em lugar nenhum fora dos Secrets do GitHub o conteúdo do artefato da keystore. Ao fim de cada etapa, me diga o que foi feito e o que ficou pendente.

---

## 0. Só o Fernando faz (a sessão deve parar e chamar)

- Login nas contas (Google, GitHub) e códigos de dois fatores.
- **Conta de desenvolvedor do Google Play** (taxa única de US$ 25 e verificação de identidade com documento). Conta pessoal.
- **Conta do AdMob** com a mesma conta Google, e os dados de pagamento/impostos quando o AdMob pedir.
- Aceitar termos e declarações legais (Play Console, AdMob, GitHub Pages).
- Guardar a keystore e a senha num lugar seguro (etapa 4).
- Convidar os **12 testadores** (e-mails de pessoas reais).

## 1. Site da produtora (GitHub Pages, grátis) — ~5 min

O jogo já está configurado com o site **https://fefaofefao.github.io** e a política em **https://fefaofefao.github.io/privacidade.html**.

1. GitHub → **New repository** → nome exatamente **`fefaofefao.github.io`**, **Public**, marcar *Add a README*. Criar.
2. No repositório novo: **Add file → Upload files** e enviar os 6 arquivos da pasta `site/` do repositório do jogo: `index.html`, `privacidade.html`, `privacy.html`, `privacidad.html`, `app-ads.txt` e `.nojekyll`.
   - Para baixar cada arquivo: abra-o no GitHub e use o botão **Download raw file**. O `.nojekyll` é vazio: se não der para baixar, crie com **Add file → Create new file**, nome `.nojekyll`, sem conteúdo.
3. **Settings → Pages** → *Source*: **Deploy from a branch** → branch **main**, pasta **/ (root)** → Save.
4. Em 1–2 minutos, conferir que abrem: `https://fefaofefao.github.io/`, `/privacidade.html`, `/privacy.html`, `/privacidad.html` e `/app-ads.txt`.

O `app-ads.txt` ainda tem `[ADMOB_PUB_ID]`; ele é atualizado na etapa 6.

> Outro domínio? Troque `website` e `privacy_policy_url` em `config/publisher.json` (dá para editar no GitHub, ícone de lápis) e peça para uma sessão com o repositório rodar `python3 tools/sync_publisher.py`.

## 2. AdMob — app, 3 blocos e consentimento — ~15 min

1. **Apps → Add app** → plataforma **Android** → "O app está publicado numa loja?" **Não** → nome **Esqueletons Runs 2040** → *User metrics* ligado → Add.
2. Anotar o **App ID** (formato `ca-app-pub-XXXXXXXXXXXXXXXX~YYYYYYYYYY`).
3. **Ad units → Add ad unit**, três vezes (anotar cada **Ad unit ID**, formato `ca-app-pub-…/…`):
   | Tipo | Nome sugerido | Observação |
   |---|---|---|
   | **Banner** | `menus` | padrão |
   | **Interstitial** | `pos_vitoria` | padrão |
   | **Rewarded** | `premiado` | recompensa: quantidade `1`, item `bonus` (o jogo decide o prêmio) |
4. **Blocking controls → Content rating** (classificação de conteúdo): **PG**. O jogo também pede PG no código; aqui vale no servidor.
5. **Privacy & messaging**:
   - **GDPR (regulamentações europeias)** → *Create message* → app Esqueletons Runs 2040 → idiomas **Português (Brasil), Inglês e Espanhol** → URL da política: `https://fefaofefao.github.io/privacidade.html` → **Publish**.
   - **US states regulations** → criar e publicar para o mesmo app.
6. **Settings → Account information**: anotar o **Publisher ID** (`pub-XXXXXXXXXXXXXXXX`).
7. No site (`fefaofefao.github.io`), editar `app-ads.txt` (lápis) para ficar exatamente:
   ```
   google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0
   ```
   com o Publisher ID real. Commit.

## 3. Secrets do AdMob no GitHub — ~3 min

Repositório do jogo → **Settings → Secrets and variables → Actions → New repository secret**, um por vez:

| Nome | Valor |
|---|---|
| `ADMOB_APP_ID` | App ID (`ca-app-pub-…~…`) |
| `ADMOB_BANNER_ID` | bloco `menus` (`ca-app-pub-…/…`) |
| `ADMOB_INTERSTITIAL_ID` | bloco `pos_vitoria` |
| `ADMOB_REWARDED_ID` | bloco `premiado` |

O build recusa IDs de teste do Google e tira o Publisher ID do `ADMOB_APP_ID` sozinho.

## 4. Keystore de upload (uma vez só) — ~5 min

1. Repositório do jogo → **Actions → Gerar keystore de upload → Run workflow** (branch padrão, *substituir* desmarcado) → Run.
2. Quando terminar (verde), abrir a execução e baixar o artefato **`keystore-de-upload-APAGUE-DEPOIS`** (zip).
3. Criar os 3 Secrets (mesma tela da etapa 3), copiando o conteúdo de cada `.txt` do zip:
   | Nome | Valor |
   |---|---|
   | `ANDROID_KEYSTORE_BASE64` | conteúdo de `ANDROID_KEYSTORE_BASE64.txt` (uma linha longa) |
   | `ANDROID_KEYSTORE_PASSWORD` | conteúdo de `ANDROID_KEYSTORE_PASSWORD.txt` |
   | `ANDROID_KEY_ALIAS` | `upload` |
4. **Fernando:** guardar o zip (ou ao menos `upload-keystore.jks` e a senha) num gerenciador de senhas e numa cópia offline.
5. Voltar à execução e **apagar o artefato** (ícone de lixeira).

> Se o workflow disser que já existe keystore, ela já foi criada antes: não gere outra.

## 5. Gerar o AAB — ~12 min

1. **Actions → Build → Run workflow** → branch `ccr-446065e1-6l6vp4` → marcar **release** → Run.
2. Esperar os 3 jobs ficarem verdes (*Validação e testes*, *APK de debug*, *AAB de release*). Se o *AAB de release* falhar em "Conferir Secrets", o erro diz qual Secret falta.
3. Baixar os artefatos:
   - **`esqueletons-release-aab`** → dentro do zip está `esqueletons-release.aab` (é o arquivo do teste fechado);
   - **`site-da-produtora`** → a pasta do site já com o `app-ads.txt` preenchido (confira que bate com a etapa 2.7).

O número da versão (*versionCode*) é o número da execução do Actions, então cada novo AAB já sobe com um número maior.

## 6. Google Play Console — criar o app — ~10 min

**Criar app**:
| Campo | Valor |
|---|---|
| Nome | `Esqueletons Runs 2040: Discovery` |
| Idioma padrão | Português (Brasil) – pt-BR |
| App ou jogo | Jogo |
| Gratuito ou pago | Gratuito |
| Declarações | marcar (políticas e leis de exportação) — **Fernando aceita** |

**Configurações da loja** (Crescimento → Presença na loja → Configurações da loja): categoria **Jogos → RPG**; e-mail `fe.m.sampaio@hotmail.com`; site **`https://fefaofefao.github.io`** (é aqui que o AdMob vai procurar o `app-ads.txt`).

## 7. Conteúdo do app (Política → Conteúdo do app) — ~20 min

Use as respostas da **seção 2 e 3 do `PLAY_CONSOLE.md`**. Resumo:

| Formulário | Resposta |
|---|---|
| Política de privacidade | `https://fefaofefao.github.io/privacidade.html` |
| Acesso ao app | Todas as funcionalidades sem acesso especial |
| Anúncios | **Sim, contém anúncios** |
| Classificação do conteúdo | Questionário IARC, categoria Jogo; violência de fantasia leve, sem sangue, sem linguagem imprópria, sem apostas, sem interação entre usuários, sem compras |
| Público-alvo | **13–15, 16–17 e 18+**; atrai crianças sem querer: **Não** |
| Apps de notícias / governo / financeiro / saúde | Não |
| Segurança dos dados | Tabela da seção 3 do `PLAY_CONSOLE.md` (ID de publicidade, interações, diagnóstico e local aproximado; criptografado em trânsito; sem conta) |
| ID de publicidade | **Sim**: publicidade/marketing e análise |

## 8. Ficha da loja nos 3 idiomas — ~20 min

**Crescimento → Presença na loja → Página principal da loja** (pt-BR) e depois **Gerenciar traduções → adicionar Inglês (en-US) e Espanhol (es-419)**, cada um com seus textos e capturas.

| O quê | De onde tirar (repositório do jogo) |
|---|---|
| Título, descrição curta e longa | `store/listing.pt_BR.md`, `store/listing.en.md`, `store/listing.es.md` |
| Ícone 512×512 | `store/graphics/icon_512.png` |
| Gráfico de destaque 1024×500 | `store/graphics/feature_1024x500.png` |
| Capturas de telefone (7, paisagem 1280×720) | `store/screenshots/pt_BR/`, `en/`, `es/` (`01_titulo` … `07_trono`) |

Baixe cada imagem com **Download raw file** no GitHub.

## 9. Teste fechado — ~10 min

1. **Testar e lançar → Testes → Teste fechado** → usar a faixa *Closed testing - Alpha* (ou criar uma).
2. **Países/regiões**: Brasil (e outros, se quiser).
3. **Testadores**: criar uma lista de e-mails com **pelo menos 12 pessoas** (ou um Grupo do Google) — **Fernando informa os e-mails**. Ativar o link de participação (*opt-in*).
4. **Criar versão** → aceitar a **Assinatura de apps do Google Play** (chave gerada pelo Google) → enviar `esqueletons-release.aab` → nome da versão: `0.1.0`.
5. **Notas da versão**:
   ```
   <pt-BR>
   Primeira versão de teste! Jogue, anote o que achar e conte pra gente.
   </pt-BR>
   <en-US>
   First test build! Play, take notes and tell us what you think.
   </en-US>
   <es-419>
   ¡Primera versión de prueba! Juega, anota lo que veas y cuéntanos.
   </es-419>
   ```
6. **Revisar versão → Iniciar lançamento** e depois **Visão geral da publicação → Enviar para revisão**.
7. Mandar o **link de participação** para os testadores. Cada um precisa aceitar pelo link, instalar pela Play Store e **manter o app instalado por 14 dias seguidos**.

A primeira revisão do Google costuma levar de algumas horas a alguns dias.

## 10. Depois da aprovação

- **AdMob → Apps → (o app) → App settings → Add app store details**: ligar o app à listagem do Google Play. Depois, na aba **app-ads.txt**, clicar em *Check for updates*. A verificação pode levar até 24 h.
- Contas pessoais novas: após **12 testadores por 14 dias**, ir em **Painel → Solicitar acesso à produção** e responder ao questionário sobre o teste.
- Novas versões: repetir a etapa 5 (o *versionCode* sobe sozinho) e enviar o novo AAB na mesma faixa.

## Checklist rápido

- [ ] Site no ar com política (3 idiomas) e `app-ads.txt` com o Publisher ID
- [ ] AdMob: app, 3 blocos, classificação PG, mensagens GDPR e EUA publicadas
- [ ] 7 Secrets no GitHub (4 do AdMob + 3 da keystore); artefato da keystore apagado e cópia segura guardada
- [ ] AAB gerado (Actions verde) e baixado
- [ ] Play Console: app criado, conteúdo do app completo, ficha nos 3 idiomas
- [ ] Teste fechado com ≥ 12 testadores, enviado para revisão
