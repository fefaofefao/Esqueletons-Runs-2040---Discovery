#!/usr/bin/env python3
"""Documentos de publicação gerados de config/publisher.json (fonte única):
  privacy/privacidade.pt_BR.{md,html}, privacy/privacy.en.{md,html}, privacy/privacidad.es.{md,html}
  app-ads.txt
  site/ (index.html, privacidade.html, privacy.html, privacidad.html, app-ads.txt): o site da produtora
  store/listing.<idioma>.md   (título ≤30, curta ≤80, longa ≤4000; sem marcas de terceiros)
Placeholders como [URL] e [ADMOB_PUB_ID] continuam visíveis; o build de release
falha enquanto existirem (tools/check_placeholders.py).

  python3 tools/store/gen_store_docs.py           # gera
  python3 tools/store/gen_store_docs.py --check   # só confere limites e marcas
"""
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PUB = json.loads((ROOT / "config/publisher.json").read_text(encoding="utf-8"))
# Marcas que não podem aparecer na ficha da loja (seção 0 e 14 do AGENTS.md).
FORBIDDEN = ["pokémon", "pokemon", "nintendo", "game boy", "gameboy", "gba", "digimon", "zelda", "final fantasy", "google", "admob",
             "android", "minecraft", "roblox", "sega", "sony", "playstation", "xbox"]

P = {
    "pt_BR": {
        "file": "privacidade.pt_BR", "lang": "pt-BR", "title": "Política de Privacidade",
        "sections": [
            ("Quem somos", "{game} é um jogo da {producer}. Responsável: {responsible}. Contato: {email}."),
            ("O que o jogo guarda", "O progresso do jogo fica salvo apenas no seu aparelho. O jogo não tem login, não tem servidor próprio e a {producer} não recebe nem guarda dados pessoais seus."),
            ("Anúncios", "Para continuar gratuito, o jogo exibe anúncios do Google AdMob. O SDK de anúncios pode coletar e compartilhar com o Google: o identificador de publicidade do aparelho, o endereço IP (usado para estimar a localização aproximada), informações sobre interações com anúncios e dados de diagnóstico e desempenho do app. Esses dados servem para exibir e medir anúncios, evitar fraudes e melhorar o serviço. Saiba mais em https://policies.google.com/privacy e https://policies.google.com/technologies/partner-sites."),
            ("Consentimento", "Onde a lei exige (por exemplo, LGPD no Brasil e GDPR na União Europeia e no Reino Unido), o jogo pede o seu consentimento antes de inicializar os anúncios, por meio da Plataforma de Mensagens ao Usuário do Google. Você pode rever a escolha a qualquer momento em Configurações → Privacidade e anúncios. Também é possível redefinir ou excluir o ID de publicidade nas configurações do aparelho."),
            ("Público e crianças", "O jogo é destinado a pessoas com {age} anos ou mais. Não coletamos intencionalmente dados de menores de {age} anos. Os anúncios são configurados como não direcionados a crianças e com um teto de conteúdo compatível com a classificação do jogo (PG: adequado ao público geral, com orientação dos pais)."),
            ("Segurança", "Os dados coletados pelo SDK de anúncios são transmitidos com criptografia (HTTPS). O jogo funciona totalmente offline; sem conexão, nenhum anúncio é carregado."),
            ("Seus direitos", "Você pode pedir informações, correção ou exclusão de dados pessoais pelo contato acima. Como a {producer} não guarda dados pessoais, pedidos sobre os dados de anúncios são atendidos pelo Google; para apagar o progresso do jogo, basta desinstalar o app ou apagar os dados dele."),
            ("Alterações", "Esta política pode ser atualizada; a versão vigente fica sempre neste endereço. Vigente desde {date}."),
        ]},
    "en": {
        "file": "privacy.en", "lang": "en", "title": "Privacy Policy",
        "sections": [
            ("Who we are", "{game} is a game by {producer}. Person responsible: {responsible}. Contact: {email}."),
            ("What the game stores", "Your game progress is saved only on your device. The game has no login and no server of its own, and {producer} does not receive or store any of your personal data."),
            ("Ads", "To stay free, the game shows ads from Google AdMob. The ads SDK may collect and share with Google: your device's advertising ID, your IP address (used to estimate approximate location), information about ad interactions, and app diagnostics and performance data. This data is used to show and measure ads, prevent fraud and improve the service. Learn more at https://policies.google.com/privacy and https://policies.google.com/technologies/partner-sites."),
            ("Consent", "Where the law requires it (for example, GDPR in the European Union and the UK, and LGPD in Brazil), the game asks for your consent before initializing ads, using Google's User Messaging Platform. You can review your choice at any time in Settings → Privacy and ads. You can also reset or delete your advertising ID in your device settings."),
            ("Audience and children", "The game is intended for people aged {age} and over. We do not knowingly collect data from children under {age}. Ads are set as not directed to children, with a content cap that matches the game's rating (PG: suitable for general audiences, with parental guidance)."),
            ("Security", "Data collected by the ads SDK is transmitted with encryption (HTTPS). The game works fully offline; without a connection, no ads are loaded."),
            ("Your rights", "You can request information, correction or deletion of personal data through the contact above. Since {producer} does not store personal data, requests about ad data are handled by Google; to erase your game progress, uninstall the app or clear its data."),
            ("Changes", "This policy may be updated; the current version is always at this address. Effective since {date}."),
        ]},
    "es": {
        "file": "privacidad.es", "lang": "es", "title": "Política de Privacidad",
        "sections": [
            ("Quiénes somos", "{game} es un juego de {producer}. Responsable: {responsible}. Contacto: {email}."),
            ("Qué guarda el juego", "El progreso del juego se guarda solo en tu dispositivo. El juego no tiene inicio de sesión ni servidor propio, y {producer} no recibe ni guarda tus datos personales."),
            ("Anuncios", "Para seguir siendo gratuito, el juego muestra anuncios de Google AdMob. El SDK de anuncios puede recopilar y compartir con Google: el identificador de publicidad del dispositivo, la dirección IP (usada para estimar la ubicación aproximada), información sobre interacciones con anuncios y datos de diagnóstico y rendimiento de la app. Estos datos sirven para mostrar y medir anuncios, evitar fraudes y mejorar el servicio. Más información en https://policies.google.com/privacy y https://policies.google.com/technologies/partner-sites."),
            ("Consentimiento", "Donde la ley lo exige (por ejemplo, el RGPD en la Unión Europea y el Reino Unido, y la LGPD en Brasil), el juego pide tu consentimiento antes de inicializar los anuncios, mediante la Plataforma de Mensajes al Usuario de Google. Puedes revisar tu elección en cualquier momento en Ajustes → Privacidad y anuncios. También puedes restablecer o eliminar el ID de publicidad en los ajustes del dispositivo."),
            ("Público y menores", "El juego está destinado a personas de {age} años o más. No recopilamos a sabiendas datos de menores de {age} años. Los anuncios están configurados como no dirigidos a niños y con un límite de contenido acorde con la clasificación del juego (PG: apto para todo público, con orientación de los padres)."),
            ("Seguridad", "Los datos recopilados por el SDK de anuncios se transmiten cifrados (HTTPS). El juego funciona totalmente sin conexión; sin conexión no se carga ningún anuncio."),
            ("Tus derechos", "Puedes solicitar información, corrección o eliminación de datos personales mediante el contacto indicado. Como {producer} no guarda datos personales, las solicitudes sobre los datos de anuncios las atiende Google; para borrar el progreso del juego, desinstala la app o borra sus datos."),
            ("Cambios", "Esta política puede actualizarse; la versión vigente está siempre en esta dirección. Vigente desde {date}."),
        ]},
}

L = {
    "pt_BR": {
        "title": "Esqueletons Runs 2040",
        "short": "Faça amizade com esqueletos, celebre aniversários e descubra o mistério de 2040.",
        "long": """Você acorda numa praia com um ingresso de museu no bolso: 12/10/2040. O continente foi tomado por esqueletos, e o Rei Esqueleto quer você no castelo. Por quê?

Esqueletons Runs 2040 — Edição Discovery é um RPG de aventura em pixel art, o primeiro jogo da série. Viaje com a Lia e o Taro, seus dois parceiros, por seis regiões, cada uma com um Guardião da família do Rei.

ESQUELETOS QUE CRESCEM
• 95 espécies para descobrir no Ossário, todas originais.
• Nível é idade: cada vitória pode virar um aniversário, com bolo, velas e confete.
• Na idade certa, o esqueleto cresce de Bebê para Adolescente e Adulto, com visual e golpes novos.
• Esqueletos Golden: raros, brilhantes e recrutáveis.

BATALHAS DIFERENTES
• Duplas contra duplas, com uma linha do tempo de turnos: golpes leves voltam rápido, golpes pesados demoram.
• Atrase o inimigo na fila e una aliados em sequência para ativar a Sintonia.
• Quatro tipos: Físico, Mágico, Cura e Veneno.

AMIZADE, NÃO CAPTURA
• Vença uma espécie algumas vezes e o marcador de ossos enche: o esqueleto pede para ir com você.

UMA HISTÓRIA DE ESCOLHAS
• Decisões que mudam diálogos, recompensas e recrutas.
• Dois finais: derrotar ou redimir o Rei Esqueleto.
• Cerca de 3 horas de história, com pós-jogo livre.

FEITO PARA O CELULAR
• Controles na tela, botão de velocidade 2x e partidas curtas.
• Funciona offline. Sem login.
• Português, inglês e espanhol.

Gratuito, com anúncios opcionais e não intrusivos.""",
    },
    "en": {
        "title": "Esqueletons Runs 2040",
        "short": "Befriend skeletons, celebrate their birthdays and uncover the mystery of 2040.",
        "long": """You wake up on a beach with a museum ticket in your pocket: 10/12/2040. The continent is ruled by skeletons, and the Skeleton King wants you at his castle. Why?

Esqueletons Runs 2040 — Discovery Edition is a pixel-art adventure RPG and the first game in the series. Travel with Lia and Taro, your two partners, across six regions, each guarded by a member of the King's family.

SKELETONS THAT GROW UP
• 95 original species to discover in the Ossuary.
• Level is age: every win can become a birthday, with cake, candles and confetti.
• At the right age, skeletons grow from Baby to Teen to Adult, with new looks and new moves.
• Golden skeletons: rare, shiny and recruitable.

A DIFFERENT KIND OF BATTLE
• Pairs against pairs, on a timeline of turns: light moves come back fast, heavy moves take time.
• Push enemies back in line and chain allies to trigger Sync.
• Four types: Physical, Magic, Healing and Poison.

FRIENDSHIP, NOT CAPTURE
• Beat a species a few times and its bone gauge fills up: the skeleton asks to join you.

A STORY OF CHOICES
• Decisions that change dialogue, rewards and recruits.
• Two endings: defeat or redeem the Skeleton King.
• About 3 hours of story, plus a free post-game.

MADE FOR PHONES
• On-screen controls, a 2x speed button and short sessions.
• Plays offline. No login.
• English, Portuguese and Spanish.

Free, with optional, non-intrusive ads.""",
    },
    "es": {
        "title": "Esqueletons Runs 2040",
        "short": "Hazte amigo de esqueletos, celebra cumpleaños y descubre el misterio de 2040.",
        "long": """Despiertas en una playa con una entrada de museo en el bolsillo: 12/10/2040. El continente está dominado por esqueletos, y el Rey Esqueleto te quiere en su castillo. ¿Por qué?

Esqueletons Runs 2040 — Edición Discovery es un RPG de aventura en pixel art, el primer juego de la serie. Viaja con Lia y Taro, tus dos compañeros, por seis regiones, cada una con un Guardián de la familia del Rey.

ESQUELETOS QUE CRECEN
• 95 especies originales para descubrir en el Osario.
• El nivel es la edad: cada victoria puede volverse un cumpleaños, con pastel, velas y confeti.
• A la edad justa, el esqueleto crece de Bebé a Adolescente y Adulto, con nuevo aspecto y nuevos golpes.
• Esqueletos Dorados: raros, brillantes y reclutables.

BATALLAS DIFERENTES
• Parejas contra parejas, con una línea de turnos: los golpes ligeros vuelven rápido, los pesados tardan.
• Retrasa al enemigo en la fila y encadena aliados para activar la Sintonía.
• Cuatro tipos: Físico, Mágico, Cura y Veneno.

AMISTAD, NO CAPTURA
• Vence a una especie varias veces y su marcador de huesos se llena: el esqueleto pide unirse a ti.

UNA HISTORIA DE DECISIONES
• Decisiones que cambian diálogos, recompensas y reclutas.
• Dos finales: derrotar o redimir al Rey Esqueleto.
• Unas 3 horas de historia, con un posjuego libre.

HECHO PARA EL MÓVIL
• Controles en pantalla, botón de velocidad x2 y partidas cortas.
• Funciona sin conexión. Sin inicio de sesión.
• Español, portugués e inglés.

Gratis, con anuncios opcionales y no intrusivos.""",
    },
}


def fmt(text, lang):
    return text.format(game=f"{PUB['game_name']} — {PUB['edition'][lang]}", producer=PUB["producer"], responsible=PUB["responsible"],
                       email=PUB["contact_email"], age=PUB.get("audience_min_age", 13), date=PUB.get("policy_effective_date", ""))


def check():
    errors = []
    for lang, d in L.items():
        if len(d["title"]) > 30:
            errors.append(f"{lang}: título com {len(d['title'])} caracteres (máx. 30)")
        if len(d["short"]) > 80:
            errors.append(f"{lang}: descrição curta com {len(d['short'])} caracteres (máx. 80)")
        if len(d["long"]) > 4000:
            errors.append(f"{lang}: descrição longa com {len(d['long'])} caracteres (máx. 4000)")
        blob = (d["title"] + d["short"] + d["long"]).lower()
        for b in FORBIDDEN:
            if re.search(r"\b" + re.escape(b) + r"\b", blob):
                errors.append(f"{lang}: a ficha cita a marca '{b}'")
    return errors


SITE_PAGES = {"pt_BR": "privacidade.html", "en": "privacy.html", "es": "privacidad.html"}
LANG_LABEL = {"pt_BR": "Português", "en": "English", "es": "Español"}


def write_site(site_pages, app_ads):
    """site/: o que vai para o site da produtora (GitHub Pages ou outro), na raiz:
    index.html, a política nos 3 idiomas e o app-ads.txt."""
    site = ROOT / "site"
    site.mkdir(exist_ok=True)
    for lang, page in site_pages.items():
        (site / SITE_PAGES[lang]).write_text(page, encoding="utf-8")
    (site / "app-ads.txt").write_text(app_ads, encoding="utf-8")
    (site / ".nojekyll").write_text("", encoding="utf-8")
    games = "\n".join(
        f'<section lang="{P[l]["lang"]}"><h2>{html.escape(PUB["game_name"])} — {html.escape(PUB["edition"][l])}</h2>'
        f'<p>{html.escape(L[l]["short"])}</p><p><a href="{SITE_PAGES[l]}">{html.escape(P[l]["title"])}</a></p></section>'
        for l in P)
    email = html.escape(PUB["contact_email"])
    (site / "index.html").write_text(f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(PUB['producer'])}</title>
<style>body{{font-family:system-ui,sans-serif;max-width:720px;margin:2rem auto;padding:0 16px;line-height:1.55;color:#222;background:#fff}}h1{{font-size:1.6rem}}h2{{font-size:1.1rem;margin-top:1.6rem}}a{{color:#4a3fb0}}</style>
</head><body>
<h1>{html.escape(PUB['producer'])}</h1>
{games}
<p>Contato · Contact · Contacto: <a href="mailto:{email}">{email}</a></p>
</body></html>
""", encoding="utf-8")


def write():
    out = ROOT / "privacy"
    out.mkdir(exist_ok=True)
    site_pages = {}
    for lang, d in P.items():
        title = f"{d['title']} — {PUB['game_name']} ({PUB['edition'][lang]})"
        md = [f"# {title}", ""]
        body = []
        for h, t in d["sections"]:
            t = fmt(t, lang)
            md += [f"## {h}", t, ""]
            linked = re.sub(r"(https://[^\s]+?)([.,]?)(\s|$)", lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>{m.group(2)}{m.group(3)}', html.escape(t))
            body.append(f"<h2>{html.escape(h)}</h2>\n<p>{linked}</p>")
        (out / f"{d['file']}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        page = f"""<!doctype html>
<html lang="{d['lang']}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>body{{font-family:system-ui,sans-serif;max-width:720px;margin:2rem auto;padding:0 16px;line-height:1.55;color:#222;background:#fff}}h1{{font-size:1.5rem}}h2{{font-size:1.1rem;margin-top:1.6rem}}a{{color:#4a3fb0}}</style>
</head><body>
<h1>{html.escape(title)}</h1>
{chr(10).join(body)}
</body></html>
"""
        (out / f"{d['file']}.html").write_text(page, encoding="utf-8")
        nav = " · ".join(f'<a href="{SITE_PAGES[l]}" lang="{P[l]["lang"]}">{LANG_LABEL[l]}</a>' for l in P)
        site_pages[lang] = page.replace("</head><body>\n", f"</head><body>\n<p>{nav}</p>\n", 1)
    pub_id = PUB.get("admob", {}).get("publisher_id", "[ADMOB_PUB_ID]")
    app_ads = f"google.com, {pub_id}, DIRECT, f08c47fec0942fa0\n"
    (ROOT / "app-ads.txt").write_text(app_ads, encoding="utf-8")
    write_site(site_pages, app_ads)
    st = ROOT / "store"
    st.mkdir(exist_ok=True)
    for lang, d in L.items():
        (st / f"listing.{lang}.md").write_text(
            f"# Ficha da loja — {lang}\n\n## Título ({len(d['title'])}/30)\n{d['title']}\n\n## Descrição curta ({len(d['short'])}/80)\n{d['short']}\n\n"
            f"## Descrição longa ({len(d['long'])}/4000)\n{d['long']}\n\n## Gráficos\n- Ícone: `store/graphics/icon_512.png`\n"
            f"- Gráfico de destaque: `store/graphics/feature_1024x500.png`\n- Capturas (paisagem, 1280×720): `store/screenshots/{lang}/`\n\n"
            f"## Política de privacidade\n{PUB['privacy_policy_url']}\n", encoding="utf-8")


if __name__ == "__main__":
    errs = check()
    for e in errs:
        print("ERRO", e)
    if "--check" not in sys.argv and not errs:
        write()
        print("gen_store_docs: política (3 idiomas), app-ads.txt e fichas da loja gerados")
    sys.exit(1 if errs else 0)
