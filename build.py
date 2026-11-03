#!/usr/bin/env python3
"""Gera as páginas do site da Cirmed a partir das partes comuns (cabeçalho, rodapé, traço do mapa).

Uso:  python3 build.py
Quando o domínio próprio estiver no ar, troque SITE_URL abaixo e rode de novo:
canonical, og:url, og:image e sitemap passam a usar o endereço novo.
"""
import json, pathlib, datetime

SITE_URL = "https://dudugomes-student.github.io/cirmed-site"   # sem barra no fim

WA_NUMBER = "5511991243655"
WA_SHOW = "(11) 99124-3655"
WA = f"https://wa.me/{WA_NUMBER}"
TEL = "tel:+5511991243655"
EMAIL = "rh@cirmed.com.br"
INSTAGRAM = "https://www.instagram.com/cirmedbrasil/"
CNPJ = "22.911.232/0001-34"

ROOT = pathlib.Path(__file__).parent
BR = json.loads((ROOT / "tools" / "brasil.json").read_text())

# ---------- ícones (traço arredondado, 24x24) ----------
I = {
    "wa": '<path d="M4 19.5 5.3 15.6A8 8 0 1 1 8.6 18.8Z"/><path d="M9 10.5h6M9 13.5h4"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/>',
    "phone": '<path d="M6.5 3.5h3l1.5 4-2 1.5a11 11 0 0 0 6 6l1.5-2 4 1.5v3a2 2 0 0 1-2 2A16 16 0 0 1 4.5 5.5a2 2 0 0 1 2-2Z"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "steth": '<path d="M6 3v5a4 4 0 0 0 8 0V3"/><path d="M10 12v3a5 5 0 0 0 10 0v-2"/><circle cx="20" cy="11" r="2"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4M8 14h2M12 14h2M8 17h2"/>',
    "building": '<path d="M4 21V8l8-5 8 5v13"/><path d="M9 21v-5h6v5M12 7.5v4M10 9.5h4"/>',
    "ambulance": '<path d="M2.5 6.5h11v10h-11z"/><path d="M13.5 9.5h4l3.5 3.5v3.5h-7.5"/><circle cx="7" cy="17.5" r="2"/><circle cx="17" cy="17.5" r="2"/><path d="M8 9v5M5.5 11.5h5"/>',
    "shield": '<path d="M12 3 4.5 6v5.5c0 4.8 3.2 8.2 7.5 9.5 4.3-1.3 7.5-4.7 7.5-9.5V6Z"/><path d="m8.8 12 2.4 2.4 4.2-4.6"/>',
    "map": '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    "insta": '<rect x="3.5" y="3.5" width="17" height="17" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.3" cy="6.7" r=".6"/>',
    "menu": '<path d="M4 8h16M4 16h16"/>',
    "close": '<path d="m6 6 12 12M18 6 6 18"/>',
}
def icon(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{I[name]}</svg>'

NEW_TAB = '<span class="sr-only"> (abre em nova aba)</span>'
def wa_btn(label="Falar no WhatsApp", cls="btn btn-primary", text=None):
    href = WA if text is None else f"{WA}?text={text}"
    return f'<a class="{cls}" href="{href}" target="_blank" rel="noopener noreferrer">{icon("wa")}<span>{label}</span>{NEW_TAB}</a>'

def stroke(word):
    """Palavra-chave em azul com o traço que se desenha embaixo."""
    return (f'<span class="stroke">{word}<svg viewBox="0 0 100 10" preserveAspectRatio="none" aria-hidden="true">'
            '<path class="draw" pathLength="1" style="--delay:.5s;--dur:1.1s" d="M2 6.5C26 2.5 62 8.5 98 4"/></svg></span>')

# ---------- o traço: estetoscópio que leva até o mapa do Brasil ----------
def line_map(label):
    ox, oy = 150, 30
    bx, by = BR["bauru"][0] + ox, BR["bauru"][1] + oy
    return f'''<figure class="hero-art" data-draw role="img" aria-label="{label}">
<svg class="line-art" viewBox="0 0 560 470">
  <path class="map draw" pathLength="1" style="--delay:.6s" transform="translate({ox} {oy})" d="{BR['d']}"/>
  <path class="tube draw" pathLength="1" style="--dur:1.4s" d="M34 36c-6 40 6 78 36 96M106 36c6 40-6 78-36 96"/>
  <path class="tube draw" pathLength="1" style="--delay:.5s;--dur:1.6s" d="M70 132c0 70-52 96-40 168 10 58 78 70 88 18"/>
  <circle class="pop" style="--delay:1.6s" cx="34" cy="34" r="7" fill="var(--blue)"/>
  <circle class="pop" style="--delay:1.6s" cx="106" cy="34" r="7" fill="var(--blue)"/>
  <path class="link fade" style="--delay:2s" d="M142 318C220 300 320 330 {bx:.1f} {by:.1f}"/>
  <g class="pop" style="--delay:1.7s"><circle class="piece" cx="118" cy="318" r="22"/><circle class="dot" cx="118" cy="318" r="7"/></g>
  <circle class="ring" style="--delay:3s" cx="{bx:.1f}" cy="{by:.1f}" r="10"/>
  <circle class="ring r2" style="--delay:3s" cx="{bx:.1f}" cy="{by:.1f}" r="10"/>
  <circle class="dot pop" style="--delay:3s" cx="{bx:.1f}" cy="{by:.1f}" r="8"/>
</svg></figure>'''

DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
        '<linearGradient id="traco" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8DBBD9"/>'
        '<stop offset="1" stop-color="#2475A3"/></linearGradient></defs></svg>')

NAV = [("index.html", "Início"), ("para-hospitais.html", "Para hospitais"), ("para-medicos.html", "Para médicos"),
       ("sobre.html", "Sobre"), ("contato.html", "Contato")]

def header(active):
    on = ' aria-current="page"'
    items = "".join(f'<li><a href="{h}"{on if h == active else ""}>{t}</a></li>' for h, t in NAV)
    cur = ' aria-current="page"' if active == "index.html" else ""
    return f'''<header class="site-header">
  <div class="wrap header-bar">
    <a class="brand" href="index.html"{cur}><picture><source type="image/webp" srcset="assets/logo-64.webp 181w, assets/logo-128.webp 361w" sizes="158px"><img src="assets/logo-64.png" srcset="assets/logo-64.png 181w, assets/logo-128.png 361w" sizes="158px" width="181" height="64" alt="Cirmed Serviços Médicos: página inicial"></picture></a>
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="menu-principal" aria-label="Abrir menu">{icon("menu", "icon i-open")}{icon("close", "icon i-close")}</button>
    <nav class="nav" id="menu-principal" aria-label="Principal">
      <ul class="nav-list">{items}</ul>
      {wa_btn("WhatsApp", "btn btn-primary header-cta")}
    </nav>
  </div>
</header>'''

FOOTER = f'''<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="assets/logo-128.png" width="361" height="128" alt="Cirmed Serviços Médicos" loading="lazy">
        <p>Plantões e equipes médicas para hospitais e unidades de saúde em todo o Brasil.</p>
      </div>
      <div>
        <h2>Navegue</h2>
        <ul>
          <li><a href="para-hospitais.html">Para hospitais e unidades</a></li>
          <li><a href="para-medicos.html">Plantões para médicos</a></li>
          <li><a href="sobre.html">Sobre a Cirmed</a></li>
          <li><a href="programa-de-integridade.html">Programa de Integridade</a></li>
          <li><a href="privacidade.html">Política de Privacidade</a></li>
        </ul>
      </div>
      <div>
        <h2>Fale com a Cirmed</h2>
        <ul>
          <li><a href="{WA}" target="_blank" rel="noopener noreferrer">WhatsApp {WA_SHOW}{NEW_TAB}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">Instagram @cirmedbrasil{NEW_TAB}</a></li>
          <li>Segunda a sexta, das 8h às 19h</li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>© <span data-year>{datetime.date.today().year}</span> CIRMED Serviços Médicos LTDA · CNPJ {CNPJ}</span>
      <span>Bauru (SP) · atendimento em todo o Brasil</span>
    </div>
  </div>
</footer>
<div class="mobile-bar">
  {wa_btn("WhatsApp")}
  <a class="btn btn-outline" href="para-medicos.html">{icon("steth")}<span>Plantões</span></a>
</div>'''

def page(slug, title, desc, body, scripts=("main", "paths-bg")):
    url = f"{SITE_URL}/" if slug == "index.html" else f"{SITE_URL}/{slug}"
    js = "".join(f'<script src="js/{s}.js" defer></script>' for s in scripts)
    org = json.dumps({
        "@context": "https://schema.org", "@type": "MedicalOrganization", "name": "CIRMED Serviços Médicos LTDA",
        "alternateName": "Cirmed", "url": f"{SITE_URL}/", "logo": f"{SITE_URL}/assets/logo.png",
        "telephone": "+55-11-99124-3655", "email": EMAIL, "taxID": CNPJ, "areaServed": "BR",
        "address": {"@type": "PostalAddress", "addressLocality": "Bauru", "addressRegion": "SP", "addressCountry": "BR"},
        "sameAs": [INSTAGRAM]}, ensure_ascii=False) if slug == "index.html" else None
    ld = f'<script type="application/ld+json">{org}</script>' if org else ""
    html = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>document.documentElement.classList.add('js');</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#FFFFFF">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE_URL}/assets/og-cirmed.png">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="fonts/nunito-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/nunito-latin-900-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/cirmed.css">
{ld}{js}
</head>
<body>
<a class="skip-link" href="#conteudo">Pular para o conteúdo</a>
{DEFS}
{header(slug)}
<main id="conteudo" tabindex="-1">
{body}
</main>
{FOOTER}
</body>
</html>
'''
    (ROOT / slug).write_text(html, encoding="utf-8")
    return slug

def cta(title_html, text, button=None):
    button = button or wa_btn("Falar no WhatsApp", "btn btn-white")
    return f'''<section class="section" aria-labelledby="cta-title"><div class="wrap">
  <div class="cta reveal"><div class="paths-bg paths-light" data-paths aria-hidden="true"></div>
    <h2 class="title" id="cta-title">{title_html}</h2>
    <p class="lede">{text}</p>
    <div class="btn-row">{button}<a class="btn btn-outline" href="mailto:{EMAIL}">{icon("mail")}<span>{EMAIL}</span></a></div>
  </div>
</div></section>'''

def form_result():
    return (f'<div class="form-result" data-form-result hidden><p role="status"></p>'
            f'<a class="btn btn-primary" href="{WA}" target="_blank" rel="noopener noreferrer">{icon("wa")}<span>Abrir no WhatsApp</span>{NEW_TAB}</a></div>')

ESPECIALIDADES = ["Anestesiologia", "Clínica Geral", "Pediatria", "Ortopedia", "Ginecologia", "Cardiologia",
                  "Emergências", "Traumatologia", "Oftalmologia", "Pulmonar", "Diagnóstico", "Dental"]
UFS = "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split()

def chips():
    return '<ul class="chips">' + "".join(f"<li>{e}</li>" for e in ESPECIALIDADES) + "</ul>"

SERVICOS = [
    ("steth", "Plantões e equipes médicas", "Médicos plantonistas para cobrir a escala da sua unidade, em uma especialidade ou na equipe inteira."),
    ("calendar", "Terceirização da escala", "A Cirmed monta a escala médica, acompanha as trocas e repõe quem não pode ir."),
    ("building", "Administração de unidades", "Gestão de unidades de saúde, do quadro de profissionais à rotina de atendimento."),
    ("ambulance", "Unidades móveis e SAMU", "Equipes para unidades móveis e serviços de resgate."),
]
def service_cards():
    return '<div class="cards">' + "".join(
        f'<article class="card reveal" style="--d:{i*0.08:.2f}s"><div class="card-icon">{icon(ic)}</div><h3>{t}</h3><p>{p}</p></article>'
        for i, (ic, t, p) in enumerate(SERVICOS)) + "</div>"

STEPS = [
    ("Visita técnica", "A Cirmed vai até a unidade para entender a demanda, o perfil de atendimento e onde a escala costuma ficar descoberta."),
    ("Projeto", "Com o que viu, monta o plano de ação: quantos médicos, de quais especialidades, em quais turnos."),
    ("Começo do serviço", "A equipe é montada, o pessoal é treinado na rotina da unidade e a escala entra em andamento."),
    ("Acompanhamento", "A escala é acompanhada de perto, com ajustes quando a demanda muda e auditoria do que foi feito."),
]
def steps():
    return '<ol class="steps">' + "".join(f"<li><h3>{t}</h3><p>{p}</p></li>" for t, p in STEPS) + "</ol>"

TRUST = f'''<div class="trust reveal">
  <div class="seal">{icon("shield")}</div>
  <div><h2 class="subtitle">Programa de Integridade publicado</h2>
  <p>Quem contrata pela administração pública precisa de regras claras. A Cirmed tem código de ética e conduta, controles internos e um canal para relatar qualquer irregularidade. CNPJ {CNPJ}.</p></div>
  <a class="btn btn-outline" href="programa-de-integridade.html"><span>Ler o programa</span>{icon("arrow")}</a>
</div>'''

# =====================================================================
# Início
# =====================================================================
page("index.html",
 "Cirmed | Plantões e equipes médicas para todo o Brasil",
 "A Cirmed fornece médicos plantonistas e terceiriza a escala médica de hospitais, UPAs e unidades de saúde em todo o Brasil. Médico, cadastre-se para receber plantões.",
 f'''<section class="hero" aria-labelledby="hero-title"><div class="paths-bg" data-paths aria-hidden="true"></div>
  <div class="wrap hero-grid">
    <div>
      <p class="kicker">Plantões e equipes médicas</p>
      <h1 class="display" id="hero-title" data-draw>Médicos para o seu plantão, em {stroke("todo o Brasil")}</h1>
      <p class="lede">A Cirmed coloca médicos plantonistas nas escalas de hospitais, UPAs e unidades de saúde, e pode assumir a escala inteira. Para médicos, abre plantões no horário que cada um pode.</p>
      <div class="doors">
        <a class="door" href="para-hospitais.html"><small>Para hospitais e unidades</small><strong>Preciso cobrir plantões ou terceirizar a escala</strong><span class="go">Ver como funciona {icon("arrow")}</span></a>
        <a class="door" href="para-medicos.html"><small>Para médicos</small><strong>Quero receber plantões na minha especialidade</strong><span class="go">Fazer cadastro {icon("arrow")}</span></a>
      </div>
    </div>
    {line_map("Ilustração: o traço de um estetoscópio se desenha até o mapa do Brasil, com um ponto azul pulsando no interior de São Paulo.")}
  </div>
</section>

<section class="section" aria-labelledby="servicos-title"><div class="wrap">
  <div class="section-head reveal">
    <p class="kicker">Para hospitais e unidades de saúde</p>
    <h2 class="title" id="servicos-title">O que a <span class="blue">Cirmed</span> faz</h2>
    <p class="lede">Do plantão de um fim de semana à escala de uma unidade inteira.</p>
  </div>
  {service_cards()}
</div></section>

<section class="section section-sky" aria-labelledby="esp-title"><div class="wrap split">
  <div class="reveal">
    <p class="kicker">Especialidades</p>
    <h2 class="title" id="esp-title">Da anestesia à <span class="blue">clínica geral</span></h2>
    <p class="lede">Essas são as áreas em que a Cirmed atua. Precisa de outra especialidade? Pergunte pelo WhatsApp.</p>
  </div>
  <div class="reveal" style="--d:.1s">{chips()}</div>
</div></section>

<section class="section" aria-labelledby="como-title"><div class="wrap">
  <div class="section-head reveal">
    <p class="kicker">Como começa</p>
    <h2 class="title" id="como-title">Da visita à <span class="blue">escala rodando</span></h2>
  </div>
  {steps()}
</div></section>

<section class="section section-sky" aria-labelledby="medicos-title"><div class="wrap split">
  <div class="reveal">
    <p class="kicker">Para médicos</p>
    <h2 class="title" id="medicos-title">Médico, quer <span class="blue">plantão?</span></h2>
    <p class="lede">Mande seu CRM, sua especialidade e o estado onde quer trabalhar. A equipe da Cirmed responde com os plantões disponíveis, e você pega os que cabem na sua agenda.</p>
    <div class="btn-row"><a class="btn btn-primary" href="para-medicos.html">{icon("steth")}<span>Quero receber plantões</span></a></div>
  </div>
  <ul class="checklist reveal" style="--d:.1s">
    <li>Plantões no horário que você pode: dia, noite ou fim de semana.</li>
    <li>Vagas em várias especialidades e estados.</li>
    <li>Cadastro direto pelo WhatsApp, sem baixar aplicativo.</li>
  </ul>
</div></section>

<section class="section" aria-label="Programa de Integridade"><div class="wrap">{TRUST}</div></section>

{cta('Tem plantão <span class="blue">descoberto?</span>', "Conte qual unidade, qual especialidade e para quando. A Cirmed responde pelo WhatsApp, de segunda a sexta, das 8h às 19h.")}
''')

# =====================================================================
# Para hospitais
# =====================================================================
page("para-hospitais.html",
 "Para hospitais e unidades de saúde | Cirmed",
 "Plantonistas, terceirização da escala médica, administração de unidades e equipes para unidades móveis e SAMU. Veja como a Cirmed trabalha e peça um contato.",
 f'''<section class="page-hero" aria-labelledby="hero-title"><div class="paths-bg" data-paths aria-hidden="true"></div><div class="wrap">
  <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a> / Para hospitais</nav>
  <p class="kicker">Para hospitais, UPAs e unidades de saúde</p>
  <h1 class="display" id="hero-title" data-draw>Faltou plantonista {stroke("hoje?")}</h1>
  <p class="lede">A Cirmed fornece médicos para cobrir a escala da sua unidade e pode assumir a escala inteira: monta, acompanha as trocas e repõe quem não pode ir.</p>
  <div class="btn-row">{wa_btn()}<a class="btn btn-outline" href="#pedido">{icon("calendar")}<span>Montar o pedido</span></a></div>
</div></section>

<section class="section" aria-labelledby="sit-title"><div class="wrap">
  <div class="section-head reveal">
    <p class="kicker">Situações</p>
    <h2 class="title" id="sit-title">Quando a <span class="blue">Cirmed</span> entra</h2>
  </div>
  <ul class="situations">
    <li class="reveal"><strong>Quem cobre o fim de semana?</strong><span>A escala de sábado e domingo é a primeira a ficar com buraco.</span></li>
    <li class="reveal" style="--d:.06s"><strong>O médico desmarcou em cima da hora?</strong><span>Plantão sem reposição vira hora extra de quem já está cansado.</span></li>
    <li class="reveal" style="--d:.12s"><strong>Abriu leito, ala ou unidade nova?</strong><span>A equipe precisa estar pronta no dia da abertura, não um mês depois.</span></li>
    <li class="reveal" style="--d:.18s"><strong>A escala depende de uma pessoa só?</strong><span>Se ela sai de férias, ninguém sabe quem chamar.</span></li>
  </ul>
</div></section>

<section class="section section-sky" aria-labelledby="serv-title"><div class="wrap">
  <div class="section-head reveal">
    <p class="kicker">Serviços</p>
    <h2 class="title" id="serv-title">O que dá para <span class="blue">contratar</span></h2>
  </div>
  {service_cards()}
</div></section>

<section class="section" aria-labelledby="como-title"><div class="wrap">
  <div class="section-head reveal">
    <p class="kicker">Como funciona</p>
    <h2 class="title" id="como-title">Quatro etapas, <span class="blue">uma conversa</span> de cada vez</h2>
  </div>
  {steps()}
</div></section>

<section class="section section-sky" aria-labelledby="esp-title"><div class="wrap split">
  <div class="reveal">
    <p class="kicker">Especialidades</p>
    <h2 class="title" id="esp-title">Áreas <span class="blue">atendidas</span></h2>
    <p class="lede">Para outra especialidade, pergunte no pedido abaixo.</p>
  </div>
  <div class="reveal" style="--d:.1s">{chips()}</div>
</div></section>

<section class="section" id="pedido" aria-labelledby="pedido-title"><div class="wrap split">
  <div class="reveal">
    <p class="kicker">Pedido</p>
    <h2 class="title" id="pedido-title">Conte o que a unidade <span class="blue">precisa</span></h2>
    <p class="lede">Preencha e continue no WhatsApp. A mensagem sai pronta, e você confere antes de enviar.</p>
    <ul class="checklist" style="margin-top:24px">
      <li>Não escreva dados de pacientes.</li>
      <li>O site não guarda o que você digita.</li>
    </ul>
  </div>
  <form class="form-card reveal" data-whatsapp-form="hospital" style="--d:.1s" novalidate>
    <div class="form-grid">
      <div class="field"><label for="h-nome">Seu nome</label><input id="h-nome" name="nome" autocomplete="name" required maxlength="120" data-label="Nome"></div>
      <div class="field"><label for="h-cargo">Cargo <span class="muted">(opcional)</span></label><input id="h-cargo" name="cargo" autocomplete="organization-title" maxlength="120" data-label="Cargo"></div>
      <div class="field"><label for="h-inst">Instituição</label><input id="h-inst" name="instituicao" autocomplete="organization" required maxlength="160" data-label="Instituição"></div>
      <div class="field"><label for="h-cidade">Cidade e estado</label><input id="h-cidade" name="cidade" required maxlength="120" placeholder="Ex.: Bauru (SP)" data-label="Cidade"></div>
      <div class="field full"><fieldset><legend>O que você precisa</legend><div class="options">
        <label><input type="checkbox" value="Cobrir plantões" data-label="Preciso de"> Cobrir plantões</label>
        <label><input type="checkbox" value="Terceirizar a escala" data-label="Preciso de"> Terceirizar a escala</label>
        <label><input type="checkbox" value="Administrar unidade" data-label="Preciso de"> Administrar unidade</label>
        <label><input type="checkbox" value="Unidade móvel ou SAMU" data-label="Preciso de"> Unidade móvel ou SAMU</label>
      </div></fieldset></div>
      <div class="field full"><label for="h-esp">Especialidades</label><input id="h-esp" name="especialidades" maxlength="200" placeholder="Ex.: anestesiologia e clínica geral" data-label="Especialidades"></div>
      <div class="field full"><label for="h-msg">Detalhes</label><textarea id="h-msg" name="mensagem" maxlength="1200" placeholder="Turnos, a partir de quando, quantos plantões por mês…" data-label="Detalhes"></textarea></div>
    </div>
    <div class="form-foot"><button class="btn btn-primary" type="submit" disabled>{icon("wa")}<span>Preparar mensagem</span></button>
    <p>Os dados só entram na mensagem que você decidir enviar. Veja a <a href="privacidade.html">Política de Privacidade</a>.</p></div>
    {form_result()}
  </form>
</div></section>

<section class="section" aria-label="Programa de Integridade" style="padding-top:0"><div class="wrap">{TRUST}</div></section>
''', scripts=("main", "paths-bg", "forms"))

# =====================================================================
# Para médicos
# =====================================================================
uf_opts = "".join(f'<option value="{u}">{u}</option>' for u in UFS)
esp_opts = "".join(f"<option>{e}</option>" for e in ESPECIALIDADES) + "<option>Outra</option>"
page("para-medicos.html",
 "Plantões para médicos | Cirmed",
 "Médico, receba plantões na sua especialidade e no estado onde quer trabalhar, no horário que você pode. Cadastro rápido pelo WhatsApp com CRM, especialidade e estado.",
 f'''<section class="page-hero" aria-labelledby="hero-title"><div class="paths-bg" data-paths aria-hidden="true"></div><div class="wrap">
  <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a> / Para médicos</nav>
  <p class="kicker">Para médicos</p>
  <h1 class="display" id="hero-title" data-draw>Plantão no horário {stroke("que você pode")}</h1>
  <p class="lede">A Cirmed tem plantões em hospitais e unidades de saúde de vários estados. Você diz a especialidade, o estado e quando está livre; a equipe responde com o que tem disponível.</p>
  <div class="btn-row"><a class="btn btn-primary" href="#cadastro">{icon("steth")}<span>Fazer cadastro</span></a>{wa_btn("Tirar uma dúvida", "btn btn-outline")}</div>
</div></section>

<section class="section" aria-labelledby="como-title"><div class="wrap">
  <div class="section-head reveal">
    <p class="kicker">Como funciona</p>
    <h2 class="title" id="como-title">Três passos até o <span class="blue">primeiro plantão</span></h2>
  </div>
  <ol class="steps steps-3">
    <li><h3>Cadastro</h3><p>Mande CRM, UF, especialidade, estado de interesse e os turnos em que você pode.</p></li>
    <li><h3>Plantões disponíveis</h3><p>A equipe da Cirmed responde pelo WhatsApp com os plantões abertos na sua área.</p></li>
    <li><h3>Você escolhe</h3><p>Você pega os que cabem na sua agenda e combina os detalhes com a equipe.</p></li>
  </ol>
</div></section>

<section class="section section-sky" id="cadastro" aria-labelledby="cad-title"><div class="wrap split">
  <div class="reveal">
    <p class="kicker">Cadastro</p>
    <h2 class="title" id="cad-title">Seus dados, <span class="blue">em um minuto</span></h2>
    <p class="lede">Preencha e continue no WhatsApp. A mensagem sai pronta, e você confere antes de enviar.</p>
    <ul class="checklist" style="margin-top:24px">
      <li>Prefere e-mail? Mande os mesmos dados para <a href="mailto:{EMAIL}">{EMAIL}</a>.</li>
      <li>O site não guarda o que você digita.</li>
    </ul>
  </div>
  <form class="form-card reveal" data-whatsapp-form="medico" style="--d:.1s" novalidate>
    <div class="form-grid">
      <div class="field full"><label for="m-nome">Nome completo</label><input id="m-nome" name="nome" autocomplete="name" required maxlength="120" data-label="Nome"></div>
      <div class="field"><label for="m-crm">CRM</label><input id="m-crm" name="crm" inputmode="numeric" required maxlength="12" pattern="[0-9]{{3,10}}" data-label="CRM"><span class="hint">Só os números.</span></div>
      <div class="field"><label for="m-uf">UF do CRM</label><select id="m-uf" name="uf" required data-label="UF do CRM"><option value="">Escolha</option>{uf_opts}</select></div>
      <div class="field"><label for="m-esp">Especialidade</label><select id="m-esp" name="especialidade" required data-label="Especialidade"><option value="">Escolha</option>{esp_opts}</select></div>
      <div class="field"><label for="m-estado">Estado onde quer trabalhar</label><select id="m-estado" name="estado" required data-label="Estado de interesse"><option value="">Escolha</option>{uf_opts}</select></div>
      <div class="field full"><fieldset><legend>Turnos em que você pode</legend><div class="options">
        <label><input type="checkbox" value="Dia" data-label="Turnos"> Dia</label>
        <label><input type="checkbox" value="Noite" data-label="Turnos"> Noite</label>
        <label><input type="checkbox" value="Fim de semana" data-label="Turnos"> Fim de semana</label>
      </div></fieldset></div>
      <div class="field full"><label for="m-msg">Algo mais? <span class="muted">(opcional)</span></label><textarea id="m-msg" name="mensagem" maxlength="1200" placeholder="Cidades de preferência, RQE, experiência em pronto-socorro…" data-label="Observações"></textarea></div>
    </div>
    <div class="form-foot"><button class="btn btn-primary" type="submit" disabled>{icon("wa")}<span>Preparar mensagem</span></button>
    <p>Os dados só entram na mensagem que você decidir enviar. Veja a <a href="privacidade.html">Política de Privacidade</a>.</p></div>
    {form_result()}
  </form>
</div></section>

<section class="section" aria-labelledby="esp-title"><div class="wrap split">
  <div class="reveal">
    <p class="kicker">Especialidades</p>
    <h2 class="title" id="esp-title">Onde há <span class="blue">plantão</span></h2>
    <p class="lede">As áreas em que a Cirmed atua. A disponibilidade muda conforme o estado e o mês.</p>
  </div>
  <div class="reveal" style="--d:.1s">{chips()}</div>
</div></section>
''', scripts=("main", "paths-bg", "forms"))

# =====================================================================
# Sobre
# =====================================================================
page("sobre.html",
 "Sobre a Cirmed | Plantões e equipes médicas",
 "Quem é a CIRMED Serviços Médicos LTDA: sede em Bauru (SP), atuação em todo o Brasil, serviços, diretoria e Programa de Integridade.",
 f'''<section class="page-hero" aria-labelledby="hero-title"><div class="paths-bg" data-paths aria-hidden="true"></div><div class="wrap split">
  <div>
    <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a> / Sobre</nav>
    <p class="kicker">Sobre</p>
    <h1 class="display" id="hero-title" data-draw>Sobre a {stroke("Cirmed")}</h1>
    <p class="lede">A Cirmed é uma empresa de serviços médicos com sede em Bauru, no interior de São Paulo. Leva médicos plantonistas e equipes para hospitais e unidades de saúde de todo o país e cuida da escala de quem prefere não fazer isso sozinho.</p>
  </div>
  {line_map("Ilustração: o traço de um estetoscópio se desenha até o mapa do Brasil, com um ponto azul pulsando em Bauru, no interior de São Paulo.")}
</div></section>

<section class="section" aria-labelledby="faz-title"><div class="wrap">
  <div class="section-head reveal">
    <p class="kicker">Atuação</p>
    <h2 class="title" id="faz-title">O que a <span class="blue">Cirmed</span> faz</h2>
  </div>
  {service_cards()}
</div></section>

<section class="section section-sky" aria-labelledby="dados-title"><div class="wrap split">
  <div class="reveal">
    <p class="kicker">Empresa</p>
    <h2 class="title" id="dados-title">Dados da <span class="blue">empresa</span></h2>
    <p class="lede">Para cadastro de fornecedor, licitação ou contrato.</p>
  </div>
  <dl class="facts reveal" style="--d:.1s">
    <div><dt>Razão social</dt><dd>CIRMED Serviços Médicos LTDA</dd></div>
    <div><dt>CNPJ</dt><dd>{CNPJ}</dd></div>
    <div><dt>Sede</dt><dd>Bauru (SP)</dd></div>
    <div><dt>Atuação</dt><dd>Todo o Brasil</dd></div>
    <div><dt>Diretor presidente</dt><dd>Dr. Carlos Azevedo Silva</dd></div>
    <div><dt>Contato</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{WA}" target="_blank" rel="noopener noreferrer">{WA_SHOW}{NEW_TAB}</a></dd></div>
  </dl>
</div></section>

<section class="section" aria-label="Programa de Integridade"><div class="wrap">{TRUST}</div></section>

{cta('Quer conversar com a <span class="blue">Cirmed?</span>', "Hospital, unidade de saúde ou médico: o caminho é o mesmo. Mande uma mensagem e diga o que você precisa.")}
''')

# =====================================================================
# Contato
# =====================================================================
page("contato.html",
 "Contato | Cirmed",
 f"Fale com a Cirmed pelo WhatsApp {WA_SHOW} ou pelo e-mail {EMAIL}, de segunda a sexta, das 8h às 19h.",
 f'''<section class="page-hero" aria-labelledby="hero-title"><div class="paths-bg" data-paths aria-hidden="true"></div><div class="wrap">
  <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a> / Contato</nav>
  <p class="kicker">Contato</p>
  <h1 class="display" id="hero-title" data-draw>Fale com a {stroke("Cirmed")}</h1>
  <p class="lede">De segunda a sexta, das 8h às 19h. Fora desse horário, pode deixar a mensagem.</p>
</div></section>

<section class="section" aria-labelledby="canais-title"><div class="wrap">
  <h2 class="sr-only" id="canais-title">Canais</h2>
  <div class="channels">
    <a class="channel reveal" href="{WA}" target="_blank" rel="noopener noreferrer"><small>WhatsApp</small><strong>{WA_SHOW}</strong><span>O caminho mais rápido.</span>{NEW_TAB}</a>
    <a class="channel reveal" style="--d:.06s" href="mailto:{EMAIL}"><small>E-mail</small><strong>{EMAIL}</strong><span>Para propostas e documentos.</span></a>
    <a class="channel reveal" style="--d:.12s" href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer"><small>Instagram</small><strong>@cirmedbrasil</strong><span>Novidades e plantões.</span>{NEW_TAB}</a>
    <div class="channel reveal" style="--d:.18s"><small>Dados pessoais (LGPD)</small><strong>Marciano Rodrigues Morais</strong><span>Encarregado: <a href="mailto:marcio@cirmed.com.br">marcio@cirmed.com.br</a></span></div>
  </div>
</div></section>

<section class="section section-sky" aria-labelledby="atalhos-title"><div class="wrap">
  <div class="section-head reveal"><h2 class="title" id="atalhos-title">Já sabe o que <span class="blue">precisa?</span></h2>
  <p class="lede">Cada página tem um formulário que já monta a mensagem certa.</p></div>
  <div class="doors" style="max-width:none;margin-top:0">
    <a class="door reveal" href="para-hospitais.html#pedido"><small>Hospitais e unidades</small><strong>Pedir plantonistas ou terceirizar a escala</strong><span class="go">Montar o pedido {icon("arrow")}</span></a>
    <a class="door reveal" style="--d:.06s" href="para-medicos.html#cadastro"><small>Médicos</small><strong>Receber os plantões disponíveis</strong><span class="go">Fazer cadastro {icon("arrow")}</span></a>
  </div>
</div></section>
''')

# =====================================================================
# Programa de Integridade (texto da empresa, organizado em seções)
# =====================================================================
page("programa-de-integridade.html",
 "Programa de Integridade | Cirmed",
 "Programa de Integridade da CIRMED Serviços Médicos LTDA: princípios, diretrizes, relação com a administração pública e canal para relatar irregularidades.",
 f'''<section class="page-hero" aria-labelledby="hero-title"><div class="paths-bg" data-paths aria-hidden="true"></div><div class="wrap">
  <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a> / Programa de Integridade</nav>
  <p class="kicker">CIRMED Serviços Médicos LTDA · CNPJ {CNPJ}</p>
  <h1 class="title" id="hero-title">Programa de <span class="blue">Integridade</span></h1>
</div></section>
<section class="section" style="padding-top:clamp(32px,5vw,56px)"><div class="wrap prose">
<p>A CIRMED Serviços Médicos LTDA presta serviços médicos com base em princípios de ética, transparência, responsabilidade e respeito às normas legais e regulatórias.</p>
<p>O Programa de Integridade é o conjunto de políticas, procedimentos e controles que a empresa adota para prevenir, detectar e corrigir irregularidades, de modo que todas as atividades sejam conduzidas de forma íntegra e de acordo com a legislação.</p>
<p>Ele vale para as relações com pacientes, parceiros, colaboradores, fornecedores e órgãos públicos.</p>
<h2>Objetivos</h2>
<ul>
<li>Promover uma cultura organizacional baseada na ética e na legalidade.</li>
<li>Prevenir fraudes, corrupção e conflitos de interesse.</li>
<li>Cumprir as leis, normas e regulamentos aplicáveis.</li>
<li>Dar transparência às relações institucionais e contratuais.</li>
<li>Proteger a reputação e a credibilidade da empresa.</li>
</ul>
<h2>Princípios</h2>
<ul>
<li><strong>Ética profissional:</strong> atuação responsável, respeitando os valores da medicina e as normas profissionais.</li>
<li><strong>Legalidade:</strong> cumprimento rigoroso das leis, contratos e regulamentações aplicáveis.</li>
<li><strong>Transparência:</strong> relações claras e íntegras com clientes, parceiros e órgãos públicos.</li>
<li><strong>Responsabilidade social:</strong> compromisso com os serviços prestados e com o bem-estar da sociedade.</li>
<li><strong>Integridade nas relações institucionais:</strong> proibição de qualquer forma de vantagem indevida, suborno ou prática ilícita.</li>
</ul>
<h2>Diretrizes</h2>
<ul>
<li>Cumprimento das leis anticorrupção e das normas administrativas aplicáveis.</li>
<li>Código de Ética e Conduta para colaboradores e parceiros.</li>
<li>Controles internos e processos de verificação.</li>
<li>Transparência em processos licitatórios e contratos públicos.</li>
<li>Monitoramento contínuo das práticas da empresa.</li>
</ul>
<h2>Relação com a administração pública</h2>
<p>Nas relações com a administração pública, a CIRMED respeita os princípios da legalidade, impessoalidade, moralidade, publicidade e eficiência, e repudia qualquer prática que possa caracterizar corrupção, fraude em licitações ou obtenção de vantagens indevidas.</p>
<h2>Como relatar uma irregularidade</h2>
<p>Qualquer situação que possa representar descumprimento de normas éticas ou legais pode ser comunicada à empresa pelo e-mail <a href="mailto:{EMAIL}">{EMAIL}</a> ou pelo WhatsApp <a href="{WA}" target="_blank" rel="noopener noreferrer">{WA_SHOW}{NEW_TAB}</a>. Todas as comunicações são tratadas com seriedade e confidencialidade.</p>
<h2>Revisão</h2>
<p>O programa é revisto à medida que a empresa, os contratos e a legislação mudam.</p>
</div></section>
''')

# =====================================================================
# Política de Privacidade (deste site)
# =====================================================================
page("privacidade.html",
 "Política de Privacidade | Cirmed",
 "Como o site da Cirmed trata dados pessoais: o que é coletado, para quê, por quanto tempo e como pedir acesso, correção ou exclusão.",
 f'''<section class="page-hero" aria-labelledby="hero-title"><div class="paths-bg" data-paths aria-hidden="true"></div><div class="wrap">
  <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a> / Política de Privacidade</nav>
  <p class="kicker">Atualizada em 3 de novembro de 2026</p>
  <h1 class="title" id="hero-title">Política de <span class="blue">Privacidade</span></h1>
</div></section>
<section class="section" style="padding-top:clamp(32px,5vw,56px)"><div class="wrap prose">
<h2>Quem trata os dados</h2>
<p>CIRMED Serviços Médicos LTDA, CNPJ {CNPJ}, com sede na Rua Gerson França, 12-18, Vila Mesquita, Bauru (SP), CEP 17014-380.</p>
<p>Encarregado pelo tratamento de dados pessoais: Marciano Rodrigues Morais, <a href="mailto:marcio@cirmed.com.br">marcio@cirmed.com.br</a>.</p>
<h2>O que este site coleta</h2>
<p>Nada fica guardado no site. Os formulários das páginas Para hospitais e Para médicos só montam uma mensagem no seu navegador. Ela é enviada apenas se você decidir mandá-la pelo seu WhatsApp, e a partir daí chega à Cirmed como qualquer outra mensagem.</p>
<p>Os dados que você pode incluir são: nome, cargo, instituição, cidade, CRM, UF, especialidade, estado de interesse, turnos disponíveis e o texto que escrever. Não envie dados de pacientes.</p>
<p>O site não usa cookies de publicidade nem ferramentas de análise de audiência. A hospedagem (GitHub Pages) pode registrar dados técnicos de acesso, como endereço IP, para segurança e funcionamento do serviço.</p>
<h2>Para que os dados são usados</h2>
<ul>
<li>Responder ao seu contato.</li>
<li>Para instituições: preparar propostas e prestar os serviços contratados.</li>
<li>Para médicos: apresentar plantões compatíveis com o seu perfil e organizar a escala.</li>
</ul>
<p>A Cirmed não vende dados pessoais.</p>
<h2>Por quanto tempo</h2>
<ul>
<li>Dados cadastrais: até 5 anos após o fim da relação (arts. 12 e 34 do Código de Defesa do Consumidor).</li>
<li>Demais dados: enquanto durar a relação e não houver pedido de exclusão ou revogação do consentimento (art. 9º, II, da LGPD).</li>
</ul>
<p>Terminado o prazo, os dados são excluídos de forma segura ou mantidos apenas de forma anonimizada.</p>
<h2>Seus direitos</h2>
<p>Pela Lei Geral de Proteção de Dados (Lei 13.709/2018), você pode pedir a confirmação do tratamento, o acesso, a correção, a anonimização, a portabilidade e a exclusão dos seus dados, além de revogar o consentimento. Para isso, escreva para <a href="mailto:marcio@cirmed.com.br">marcio@cirmed.com.br</a> ou <a href="mailto:{EMAIL}">{EMAIL}</a> com o assunto "Dados pessoais".</p>
<p>Os pedidos são atendidos de segunda a sexta, das 8h às 19h, exceto feriados nacionais.</p>
<h2>Segurança</h2>
<p>Os dados recebidos são acessados apenas por pessoas autorizadas da Cirmed, na medida do necessário. A Cirmed nunca pede senhas nem envia arquivos executáveis por e-mail ou mensagem.</p>
<h2>Mudanças nesta política</h2>
<p>Esta política pode ser atualizada. A data no topo da página mostra a versão em vigor.</p>
<h2>Foro</h2>
<p>Esta política segue a legislação brasileira. Fica eleito o foro do domicílio do titular dos dados, salvo disposição legal em contrário.</p>
</div></section>
''')

# =====================================================================
# 404
# =====================================================================
page("404.html",
 "Página não encontrada | Cirmed",
 "Esta página não existe ou mudou de endereço.",
 f'''<section class="page-hero" aria-labelledby="hero-title" style="min-height:60vh"><div class="paths-bg" data-paths aria-hidden="true"></div><div class="wrap">
  <p class="kicker">Erro 404</p>
  <h1 class="display" id="hero-title" data-draw>Página {stroke("não encontrada")}</h1>
  <p class="lede">O endereço pode ter mudado. Escolha um caminho:</p>
  <div class="btn-row"><a class="btn btn-primary" href="index.html"><span>Ir para o início</span></a><a class="btn btn-outline" href="para-medicos.html">{icon("steth")}<span>Plantões para médicos</span></a></div>
</div></section>
''')

# ---------- sitemap e robots ----------
pages = ["index.html", "para-hospitais.html", "para-medicos.html", "sobre.html", "contato.html",
         "programa-de-integridade.html", "privacidade.html"]
today = datetime.date.today().isoformat()
urls = "".join(f"<url><loc>{SITE_URL}/{'' if p == 'index.html' else p}</loc><lastmod>{today}</lastmod></url>" for p in pages)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
print("ok:", ", ".join(pages + ["404.html"]))
