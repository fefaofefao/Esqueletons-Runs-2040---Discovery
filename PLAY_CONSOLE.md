# Google Play Console — Esqueletons Runs 2040: Discovery

Gerado por `tools/store/gen_play_console.py` a partir de `config/publisher.json` e `data/ads.json`. Não edite à mão: mude o `publisher.json` e rode `python3 tools/sync_publisher.py`.

## 1. Criar o app

| Campo | Resposta |
|---|---|
| Nome do app | Esqueletons Runs 2040: Discovery |
| Idioma padrão | Português (Brasil) – pt-BR |
| App ou jogo | Jogo |
| Gratuito ou pago | Gratuito |
| Pacote | `com.fsamplabs.esqueletonsruns2040.discovery` |
| Desenvolvedor | FSamp Labs (Fernando Martins Sampaio) |
| E-mail de contato | fe.m.sampaio@hotmail.com |
| Site | https://fefaofefao.github.io |
| Categoria | Jogos → RPG |
| Tags sugeridas | RPG, Coleta de criaturas, Aventura, Pixel art, Single player, Offline |

## 2. Conteúdo do app (Política → Conteúdo do app)

### Política de privacidade
- URL: **https://fefaofefao.github.io/privacidade.html**
- Arquivos para a raiz de https://fefaofefao.github.io: a pasta `site/` (index, política em PT/EN/ES e `app-ads.txt`). O artefato `site-da-produtora` do build de release traz a mesma pasta já com o ID de editor no `app-ads.txt`.
- Informe https://fefaofefao.github.io como site do desenvolvedor na Play Console (é onde o AdMob procura o `https://fefaofefao.github.io/app-ads.txt`).
- Passo a passo pelo navegador: `docs/PUBLICAR_PELO_NAVEGADOR.md`.

### Acesso ao app
- **Todas as funcionalidades estão disponíveis sem acesso especial.** Não há login, conta ou assinatura.

### Anúncios
- **O app contém anúncios: Sim** (Google AdMob: banner nos menus, intersticial após vitórias e premiados opcionais).

### Classificação do conteúdo (questionário IARC)
| Pergunta | Resposta |
|---|---|
| Categoria | Jogo |
| Violência | **Sim, violência de fantasia leve**: criaturas esqueleto estilizadas batalham por turnos; sem sangue, sem morte mostrada, sem violência realista contra humanos |
| Sangue / gore | Não |
| Medo / horror | Não (esqueletos são fofos e fazem aniversário) |
| Sexualidade / nudez | Não |
| Linguagem imprópria | Não |
| Drogas, álcool, tabaco | Não |
| Apostas / jogos de azar simulados | Não (não há compra de itens aleatórios nem caixas de recompensa) |
| Interação entre usuários / chat | Não |
| Compartilha localização com outros usuários | Não |
| Compras digitais | Não |
| Conteúdo gerado por usuários | Não |
- Resultado esperado: classificação livre/10+ conforme a região (ClassInd, ESRB E10+, PEGI 7).

### Público-alvo e conteúdo
- **Faixas etárias:** 13–15, 16–17 e 18+ (público-alvo 13+).
- O app **não** é destinado a crianças e não participa do programa Famílias.
- Pode atrair crianças sem querer? **Não** — o tom é de aventura para 13+, e os anúncios seguem a configuração abaixo.
- Configuração de anúncios no código (`data/ads.json`): `tagForChildDirectedTreatment = false`, `tagForUnderAgeOfConsent = false`, conteúdo máximo dos anúncios **PG**.
- O teto **PG** do AdMob mantém os anúncios dentro da classificação do jogo (10+/PEGI 7): a política de anúncios do Google Play pede que os anúncios sejam adequados à classificação do app. No AdMob, em *Bloqueio de controles → Classificação de conteúdo*, escolha também **PG** para valer no servidor.

### ID de publicidade
- **O app usa o ID de publicidade: Sim.** Finalidade: **Publicidade ou marketing** e **Análise** (feitas pelo SDK do Google AdMob).
- O manifesto declara `com.google.android.gms.permission.AD_ID` (targetSdk 36).

### Apps de notícias, governamentais, financeiros, de saúde e de COVID-19
- Não se aplica a nenhum deles (responda **Não** em todos).

## 3. Segurança dos dados

O jogo não tem servidor nem conta e não coleta dados próprios: o save fica só no aparelho. Os dados abaixo são coletados pelo **SDK do Google AdMob** (incluindo o consentimento UMP).

| Pergunta | Resposta |
|---|---|
| O app coleta ou compartilha algum dos tipos de dados obrigatórios? | **Sim** |
| Todos os dados coletados são criptografados em trânsito? | **Sim** |
| Os usuários podem pedir a exclusão dos dados? | Não há conta nem dados guardados pelo app; o ID de publicidade é redefinido nas configurações do Android. Responda **Não** (não há mecanismo próprio) |
| O app permite criar conta? | **Não** |

| Tipo de dado | Coletado | Compartilhado | Opcional? | Finalidades |
|---|---|---|---|---|
| **Identificadores do dispositivo ou outros IDs** (ID de publicidade) | Sim | Sim | Não | Publicidade ou marketing; Análise; Prevenção de fraudes, segurança e conformidade |
| **Interações no app** (atividade do app) | Sim | Sim | Não | Publicidade ou marketing; Análise |
| **Diagnóstico** (registros de falhas e desempenho do SDK) | Sim | Sim | Não | Análise; Prevenção de fraudes, segurança e conformidade |
| **Local aproximado** (derivado do IP) | Sim | Sim | Não | Publicidade ou marketing; Análise; Prevenção de fraudes |

Nada é coletado para funcionalidade do app nem para personalização própria. Não há dados pessoais, financeiros, de saúde, mensagens, fotos, arquivos ou contatos.

## 4. Ficha da loja

| Idioma | Textos | Gráficos |
|---|---|---|
| Português (Brasil) – pt-BR | `store/listing.pt_BR.md` | `store/screenshots/pt_BR/` (7 capturas 1280×720) |
| Inglês (Estados Unidos) – en-US | `store/listing.en.md` | `store/screenshots/en/` (7 capturas 1280×720) |
| Espanhol (América Latina) – es-419 | `store/listing.es.md` | `store/screenshots/es/` (7 capturas 1280×720) |

- Ícone 512×512: `store/graphics/icon_512.png` · Gráfico de destaque 1024×500: `store/graphics/feature_1024x500.png`.
- Os textos não citam outras marcas (o `tools/store/gen_store_docs.py` confere).
- As capturas mostram o jogo atual: depois de mudar a interface ou o conteúdo mostrado, refaça com `python3 tools/store/gen_store_shots.py`.

## 5. Versões e testes

1. Configure os Secrets do GitHub (veja `docs/BUILD.md`): keystore e os 4 IDs reais do AdMob.
2. Preencha os campos entre colchetes do `config/publisher.json` e rode `python3 tools/sync_publisher.py`. O release falha enquanto houver placeholders.
3. Crie a tag `v0.1.0` (ou rode o workflow com *release* marcado) e baixe o artefato `esqueletons-release-aab`.
4. Ative a **Assinatura de apps do Google Play** e envie o `.aab` para a faixa de **teste fechado**.
5. **Conta pessoal nova (criada depois de 13/11/2023):** o Google exige um **teste fechado com pelo menos 12 testadores, ativos por 14 dias seguidos**, antes de liberar a produção. Convide os testadores por e-mail ou Grupo do Google logo no começo.
6. Depois do teste fechado, peça o acesso à produção respondendo ao questionário sobre o teste.

## 6. AdMob

- Crie o app no AdMob (Android, `com.fsamplabs.esqueletonsruns2040.discovery`) e 3 blocos: banner, intersticial e premiado.
- ID do editor para o `app-ads.txt`: `[ADMOB_PUB_ID]`.
- Em **Privacidade e mensagens**, crie as mensagens de consentimento (GDPR e estados dos EUA). O jogo já mostra o formulário UMP antes de iniciar os anúncios e reabre-o em *Configurações → Privacidade e anúncios*.
- Os IDs de teste do Google ficam no build de debug; os reais só entram no release, via Secrets.
