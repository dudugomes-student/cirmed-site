#!/usr/bin/env python3
"""Gera as páginas do site da Cirmed a partir das partes comuns e dos dados.

Uso:  python3 build.py
- Plantões abertos: tools/plantoes.json  ([unidade, cidade, UF, tipo (hospital|ubs|upa), [especialidades]])
- Ilustrações 3D:   tools/3d/render.py (gera assets/3d/*.webp)
Quando o domínio próprio estiver no ar, troque SITE_URL e rode de novo.
"""
import json, pathlib, datetime, html, unicodedata
from urllib.parse import quote, urlparse

SITE_URL = "https://dudugomes-student.github.io/cirmed-site"   # sem barra no fim

# Atendimento a instituições e contato geral
WA_NUMBER = "5511991243655"
WA_SHOW = "(11) 99124-3655"
WA = f"https://wa.me/{WA_NUMBER}"
# Plantões para médicos (número usado no "Quero Plantão" do site original)
WA_PLANTAO = "5511951531000"
WA_PLANTAO_SHOW = "(11) 95153-1000"
EMAIL = "rh@cirmed.com.br"
INSTAGRAM = "https://www.instagram.com/cirmedbrasil/"
CNPJ = "22.911.232/0001-34"

ROOT = pathlib.Path(__file__).parent
PLANTOES = json.loads((ROOT / "tools" / "plantoes.json").read_text())
N_UNIDADES = len(PLANTOES)
UFS_ATIVAS = sorted({p[2] for p in PLANTOES})
ESP_ATIVAS = sorted({e for p in PLANTOES for e in p[4]}, key=lambda s: unicodedata.normalize("NFD", s))
UF_NOMES = {"CE": "Ceará", "ES": "Espírito Santo", "MG": "Minas Gerais", "MS": "Mato Grosso do Sul", "MT": "Mato Grosso",
            "RS": "Rio Grande do Sul", "SP": "São Paulo"}
TIPOS = {"hospital": "Hospital", "ubs": "UBS e postos", "upa": "UPA e pronto atendimento"}
esc = html.escape

# ---------- ícones de interface (traço arredondado, 24x24) ----------
I = {
    "wa": '<path d="M4 19.5 5.3 15.6A8 8 0 1 1 8.6 18.8Z"/><path d="M9 10.5h6M9 13.5h4"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="m4 7 8 6 8-6"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
    "pin": '<path d="M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0c0 5.4-6.5 11-6.5 11Z"/><circle cx="12" cy="10" r="2.4"/>',
    "steth": '<path d="M6 3v5a4 4 0 0 0 8 0V3"/><path d="M10 12v3a5 5 0 0 0 10 0v-2"/><circle cx="20" cy="11" r="2"/>',
    "menu": '<path d="M4 8h16M4 16h16"/>',
    "close": '<path d="m6 6 12 12M18 6 6 18"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "minus": '<path d="M5 12h14"/>',
}
def icon(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{I[name]}</svg>'

NEW_TAB = '<span class="sr-only"> (abre em nova aba)</span>'
def wa_btn(label="Falar no WhatsApp", cls="btn btn-primary", number=WA_NUMBER):
    return f'<a class="{cls}" href="https://wa.me/{number}" target="_blank" rel="noopener noreferrer">{icon("wa")}<span>{label}</span>{NEW_TAB}</a>'

def stroke(word):
    """Palavra-chave em azul com o traço que se desenha embaixo."""
    return (f'<span class="stroke">{word}<svg viewBox="0 0 100 10" preserveAspectRatio="none" aria-hidden="true">'
            '<path class="draw" pathLength="1" style="--delay:.5s;--dur:1.1s" d="M2 6.5C26 2.5 62 8.5 98 4"/></svg></span>')

# ---------- ilustrações 3D (assets/3d) ----------
SIZES = {}
def img3d(name, alt="", cls="art3d", eager=False, sizes=None):
    from PIL import Image
    if name not in SIZES:
        SIZES[name] = Image.open(ROOT / "assets" / "3d" / f"{name}.webp").size
    w, h = SIZES[name]
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    alt_attr = f'alt="{esc(alt)}"' if alt else 'alt="" aria-hidden="true"'
    return f'<img class="{cls}" src="assets/3d/{name}.webp" width="{w}" height="{h}" {alt_attr} {load}>'

def float3d(name, cls="", depth=0.3, delay=0.0, alt=""):
    """Ícone 3D que flutua (CSS) e se mexe com o mouse e a rolagem (data-depth)."""
    return (f'<span class="float {cls}" data-depth="{depth}" style="--fd:{delay:.2f}s">'
            f'{img3d(name, alt, cls="float-img")}</span>')

ORBITA = ["estetoscopio", "prancheta", "ambulancia", "calendario", "coracao", "pino"]
def orbit(label):
    n = len(ORBITA)
    items = "".join(
        f'<li style="--i:{i};--n:{n}"><span class="orbit-item">{img3d(x, cls="orbit-img")}</span></li>' for i, x in enumerate(ORBITA))
    return f'''<figure class="orbit-stage" role="img" aria-label="{label}">
  <span class="orbit-glow" aria-hidden="true"></span>
  <svg class="orbit-ring" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="49"/></svg>
  <svg class="orbit-ring orbit-ring-2" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="49"/></svg>
  <ul class="orbit" aria-hidden="true">{items}</ul>
  <span class="orbit-center" data-depth="0.15">{img3d("hospital", cls="orbit-hub", eager=True)}</span>
</figure>'''

def map_stage(label):
    # Globo mostrando as Américas; os pinos ficam sobre o Brasil e se movem junto com o globo.
    return f'''<figure class="map-stage" role="img" aria-label="{label}">
  <span class="map-glow" aria-hidden="true"></span>
  <span class="map-move" data-depth="0.12">
    {img3d("globo", cls="map-globe")}
    <span class="map-pin mp-b">{img3d("pino", cls="pin-img")}</span>
    <span class="map-pin mp-c">{img3d("pino", cls="pin-img")}</span>
    <span class="map-pin mp-a">{img3d("pino", cls="pin-img")}<span class="pin-pulse"></span></span>
  </span>
</figure>'''

ESP_ICONES = [("coracao", "Cardiologia"), ("bebe", "Pediatria"), ("seringa", "Anestesiologia"), ("osso", "Ortopedia"),
              ("gestante", "Ginecologia e Obstetrícia"), ("estetoscopio", "Clínica Geral"), ("ambulancia", "Emergência"),
              ("pulmoes", "Pulmonar"), ("cerebro", "Neurologia"), ("microscopio", "Diagnóstico"), ("dente", "Dental")]
def marquee():
    row = "".join(f'<li>{img3d(n, cls="mq-img")}<span>{t}</span></li>' for n, t in ESP_ICONES)
    return (f'<div class="marquee" aria-label="Especialidades"><ul class="mq-track">{row}</ul>'
            f'<ul class="mq-track" aria-hidden="true">{row}</ul></div>')

PATHS = '<div class="paths-bg" data-paths aria-hidden="true"></div>'
DEFS = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>'
        '<linearGradient id="traco" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8DBBD9"/>'
        '<stop offset="1" stop-color="#2475A3"/></linearGradient></defs></svg>')

NAV = [("index.html", "Início"), ("plantoes.html", "Plantões"), ("para-hospitais.html", "Para hospitais"),
       ("sobre.html", "Sobre"), ("contato.html", "Contato")]

def header(active):
    on = ' aria-current="page"'
    items = "".join(f'<li><a href="{h}"{on if h == active else ""}>{t}</a></li>' for h, t in NAV)
    cur = on if active == "index.html" else ""
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
        <p>Plantões e equipes médicas em todo o Brasil.</p>
      </div>
      <div>
        <h2>Navegue</h2>
        <ul>
          <li><a href="plantoes.html">Plantões abertos</a></li>
          <li><a href="para-hospitais.html">Para hospitais</a></li>
          <li><a href="sobre.html">Sobre a Cirmed</a></li>
          <li><a href="programa-de-integridade.html">Programa de Integridade</a></li>
          <li><a href="privacidade.html">Política de Privacidade</a></li>
        </ul>
      </div>
      <div>
        <h2>Fale com a Cirmed</h2>
        <ul>
          <li><a href="{WA}" target="_blank" rel="noopener noreferrer">Instituições: {WA_SHOW}{NEW_TAB}</a></li>
          <li><a href="https://wa.me/{WA_PLANTAO}" target="_blank" rel="noopener noreferrer">Plantões: {WA_PLANTAO_SHOW}{NEW_TAB}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">@cirmedbrasil{NEW_TAB}</a></li>
          <li>Seg. a sex., 8h às 19h</li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>© <span data-year>{datetime.date.today().year}</span> CIRMED Serviços Médicos LTDA · CNPJ {CNPJ}</span>
      <span>Bauru (SP)</span>
    </div>
  </div>
</footer>
<nav class="mobile-bar" aria-label="Atalhos">
  {wa_btn("WhatsApp")}
  <a class="btn btn-outline" href="plantoes.html">{icon("search")}<span>Plantões</span></a>
</nav>'''

def page(slug, title, desc, body, scripts=("main", "paths-bg", "motion"), noindex=False):
    url = f"{SITE_URL}/" if slug == "index.html" else f"{SITE_URL}/{slug}"
    js = "".join(f'<script src="js/{s}.js" defer></script>' for s in scripts)
    ld = ""
    if slug == "index.html":
        ld = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "MedicalOrganization", "name": "CIRMED Serviços Médicos LTDA",
            "alternateName": "Cirmed", "url": f"{SITE_URL}/", "logo": f"{SITE_URL}/assets/logo.png",
            "telephone": "+55-11-99124-3655", "email": EMAIL, "taxID": CNPJ, "areaServed": "BR",
            "address": {"@type": "PostalAddress", "addressLocality": "Bauru", "addressRegion": "SP", "addressCountry": "BR"},
            "sameAs": [INSTAGRAM]}, ensure_ascii=False) + "</script>"
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    if slug == "404.html":
        robots += f'<base href="{urlparse(SITE_URL).path.rstrip("/")}/">'
    out = f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<script>document.documentElement.classList.add('js');try{{if(sessionStorage.getItem('cirmed-nav')==='1'&&!matchMedia('(prefers-reduced-motion: reduce)').matches){{document.documentElement.classList.add('arriving');}}sessionStorage.removeItem('cirmed-nav')}}catch(e){{}}</script>
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">{robots}
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
<div class="curtain" aria-hidden="true"><div class="curtain-panel"><span class="curtain-badge"><img src="assets/logo-128.png" width="361" height="128" alt=""></span><span class="curtain-line"></span></div></div>
<div class="progress" aria-hidden="true"></div>
{DEFS}
{header(slug)}
<main id="conteudo" tabindex="-1">
{body}
</main>
{FOOTER}
</body>
</html>
'''
    (ROOT / slug).write_text(out, encoding="utf-8")

def cta(title_html, text, button=None):
    button = button or wa_btn("Falar no WhatsApp", "btn btn-white")
    return f'''<section class="section" aria-labelledby="cta-title"><div class="wrap">
  <div class="cta reveal">{PATHS.replace('paths-bg', 'paths-bg paths-light')}
    <h2 class="title" id="cta-title">{title_html}</h2>
    <p class="lede">{text}</p>
    <div class="btn-row">{button}</div>
  </div>
</div></section>'''

def form_result():
    return (f'<div class="form-result" data-form-result hidden><p role="status"></p>'
            f'<a class="btn btn-primary" href="{WA}" target="_blank" rel="noopener noreferrer">{icon("wa")}<span>Abrir no WhatsApp</span>{NEW_TAB}</a></div>')

SERVICOS = [
    ("estetoscopio", "Plantonistas", "Um plantão ou a equipe inteira."),
    ("calendario", "Escala terceirizada", "A Cirmed monta e repõe faltas."),
    ("hospital", "Gestão de unidades", "Do quadro de pessoal à rotina."),
    ("ambulancia", "Unidades móveis e SAMU", "Equipes para resgate."),
]
def service_tiles():
    return '<div class="tiles">' + "".join(
        f'<article class="tile{" tile-blue" if i == 1 else ""} reveal" data-tilt style="--d:{i*0.08:.2f}s"><span class="tile-art">{img3d(n)}</span><h3>{t}</h3><p>{p}</p></article>'
        for i, (n, t, p) in enumerate(SERVICOS)) + "</div>"

def stats():
    return f'''<dl class="stats">
  <div class="reveal"><dt>Unidades com plantão aberto</dt><dd data-count-to="{N_UNIDADES}">{N_UNIDADES}</dd></div>
  <div class="reveal" style="--d:.07s"><dt>Estados</dt><dd data-count-to="{len(UFS_ATIVAS)}">{len(UFS_ATIVAS)}</dd></div>
  <div class="reveal" style="--d:.14s"><dt>Especialidades nas escalas</dt><dd data-count-to="{len(ESP_ATIVAS)}">{len(ESP_ATIVAS)}</dd></div>
</dl>'''

TRUST = f'''<div class="trust reveal">
  <span class="float trust-float" data-depth="0.2">{img3d("escudo", cls="trust-art")}</span>
  <div><h2 class="subtitle">Programa de Integridade publicado</h2>
  <p>Código de ética, controles internos e canal para relatar irregularidades. CNPJ {CNPJ}.</p></div>
  <a class="btn btn-outline" href="programa-de-integridade.html"><span>Ler o programa</span>{icon("arrow")}</a>
</div>'''

def slug_txt(s):
    return unicodedata.normalize("NFD", s.lower()).encode("ascii", "ignore").decode()

# =====================================================================
# Início
# =====================================================================
page("index.html",
 "Cirmed | Plantões e equipes médicas para todo o Brasil",
 f"Plantonistas para hospitais, UPAs e unidades de saúde e {N_UNIDADES} unidades com plantão aberto para médicos. Busque por estado e especialidade.",
 f'''<section class="hero" aria-labelledby="hero-title">{PATHS}
  <div class="wrap hero-grid">
    <div>
      <p class="kicker">Plantões e equipes médicas</p>
      <h1 class="display" id="hero-title" data-draw>Médicos para o seu plantão, em {stroke("todo o Brasil")}</h1>
      <div class="doors">
        <a class="door" data-tilt href="para-hospitais.html">{img3d("hospital", cls="door-img")}<small>Sou hospital ou unidade</small><strong>Preciso de médicos</strong><span class="go">Montar equipe {icon("arrow")}</span></a>
        <a class="door door-blue" data-tilt href="plantoes.html">{img3d("estetoscopio", cls="door-img")}<small>Sou médico</small><strong>Quero plantão</strong><span class="go">Buscar plantões {icon("arrow")}</span></a>
      </div>
    </div>
    {orbit("Hospital em 3D no centro, com estetoscópio, prancheta, ambulância, calendário, coração e pino girando em volta.")}
  </div>
</section>

<section class="band-navy" aria-label="Números e especialidades"><div class="wrap">{stats()}</div>{marquee()}</section>

<section class="section" aria-labelledby="plantoes-title"><div class="wrap split">
  {map_stage("Globo em 3D mostrando as Américas, com pinos azuis sobre o Brasil.")}
  <div class="reveal" style="--d:.1s">
    <p class="kicker">Para médicos</p>
    <h2 class="title" id="plantoes-title">Ache seu <span class="blue">plantão</span></h2>
    <form class="quick-search" action="plantoes.html" role="search">
      <label class="sr-only" for="q">Buscar por cidade, unidade ou especialidade</label>
      {icon("search")}<input id="q" name="q" type="search" placeholder="Cidade, unidade ou especialidade" autocomplete="off">
      <button class="btn btn-primary" type="submit">Buscar</button>
    </form>
    <ul class="chips chips-link">{"".join(f'<li><a href="plantoes.html?esp={esc(e)}">{esc(e)}</a></li>' for e in ["Clínica Geral", "Pediatria", "Ginecologia", "Anestesiologia", "Emergência", "Ortopedia"])}</ul>
  </div>
</div></section>

<section class="section section-sky" aria-labelledby="servicos-title"><div class="wrap">
  <div class="section-head reveal">
    <p class="kicker">Para hospitais e unidades</p>
    <h2 class="title" id="servicos-title">O que a <span class="blue">Cirmed</span> faz</h2>
  </div>
  {service_tiles()}
  <div class="btn-row reveal"><a class="btn btn-primary" href="para-hospitais.html"><span>Montar minha equipe</span>{icon("arrow")}</a></div>
</div></section>

<section class="section" aria-label="Programa de Integridade" style="padding-top:0"><div class="wrap">{TRUST}</div></section>

{cta('Tem plantão <span class="blue">descoberto?</span>', "Diga a unidade, a especialidade e a data.")}
''')

# =====================================================================
# Plantões (busca para médicos)
# =====================================================================
# Palavras que as pessoas digitam além do nome da especialidade
SINONIMOS = {"Anestesiologia": "anestesia anestesista", "Pediatria": "pediatra", "Ginecologia": "ginecologista go",
    "Ginecologia e Obstetrícia": "ginecologista obstetra obstetricia go", "Clínica Geral": "clinico geral clinico",
    "Emergência": "pronto socorro ps emergencista", "Ortopedia": "ortopedista traumatologia", "Cardiologia": "cardiologista",
    "Cirurgia Geral": "cirurgiao", "Infectologia": "infectologista", "Nefrologia": "nefrologista", "Neurologia": "neurologista",
    "Dermatologia": "dermatologista", "Psiquiatria": "psiquiatra", "Neonatologia": "neonatologista neo", "Oftalmologia": "oftalmologista",
    "Oncologia": "oncologista", "Neuropediatria": "neuropediatra", "UTI diarista": "intensivista uti", "UTI pediátrica": "intensivista uti",
    "Cirurgia Vascular": "vascular cirurgiao", "Cirurgia Torácica": "toracica cirurgiao", "Proctologia": "proctologista",
    "GO alto risco": "ginecologia obstetricia", "Fonoaudiologia": "fono", "Enfermagem diarista": "enfermeira enfermeiro",
    "Enfermagem pediátrica": "enfermeira enfermeiro"}

TIPO_IMG = {"hospital": "hospital", "ubs": "predio", "upa": "ambulancia"}

def unit_card(i, nome, cidade, uf, tipo, esps):
    lugar = f"{cidade} · {uf}" if cidade else UF_NOMES[uf]
    busca = slug_txt(" ".join([nome, cidade, uf, UF_NOMES[uf], TIPOS[tipo]] + esps + [SINONIMOS.get(e, "") for e in esps]))
    chips = "".join(f'<li data-esp="{esc(e)}">{esc(e)}</li>' for e in esps)
    return (f'<li class="unit" data-tilt data-uf="{uf}" data-tipo="{tipo}" data-esps="{esc("|".join(esps))}" data-busca="{esc(busca)}" data-nome="{esc(nome)}" data-lugar="{esc(lugar)}">'
            f'<div class="unit-art">{img3d(TIPO_IMG[tipo], cls="unit-img")}</div>'
            f'<div class="unit-body"><p class="unit-type">{TIPOS[tipo]}</p><h3>{esc(nome)}</h3>'
            f'<p class="unit-place">{icon("pin")}{esc(lugar)}</p><ul class="mini-chips">{chips}</ul></div>'
            f'<a class="btn btn-primary unit-cta" href="https://wa.me/{WA_PLANTAO}?text=' + esc(
                quote(f"Olá, Cirmed. Tenho interesse no plantão em {nome} ({lugar}).")) +
            f'" target="_blank" rel="noopener noreferrer">{icon("wa")}<span>Quero plantão</span><span class="sr-only"> em {esc(nome)} (abre em nova aba)</span></a></li>')

uf_opts = "".join(f'<option value="{u}">{UF_NOMES[u]}</option>' for u in UFS_ATIVAS)
esp_opts = "".join(f'<option value="{esc(e)}">{esc(e)}</option>' for e in ESP_ATIVAS)
cards = "".join(unit_card(i, *p) for i, p in enumerate(sorted(PLANTOES, key=lambda p: (p[2] != "SP", slug_txt(p[1] or "zz"), slug_txt(p[0])))))
ALL_UFS = "AC AL AP AM BA CE DF ES GO MA MT MS MG PA PB PR PE PI RJ RN RS RO RR SC SP SE TO".split()
all_uf_opts = "".join(f'<option value="{u}">{u}</option>' for u in ALL_UFS)

page("plantoes.html",
 "Plantões abertos | Cirmed",
 f"{N_UNIDADES} unidades com plantão aberto em {len(UFS_ATIVAS)} estados. Busque por cidade, estado e especialidade e fale com a Cirmed pelo WhatsApp.",
 f'''<section class="page-hero page-hero-split" aria-labelledby="hero-title">{PATHS}<div class="wrap split">
  <div>
    <p class="kicker">Para médicos</p>
    <h1 class="display" id="hero-title" data-draw>Plantões {stroke("abertos")}</h1>
    <p class="lede">{N_UNIDADES} unidades em {len(UFS_ATIVAS)} estados. Escolha e chame no WhatsApp.</p>
  </div>
  <figure class="hero-cluster" aria-hidden="true">{float3d("estetoscopio", "c-main", 0.25)}{float3d("seringa", "c-a", 0.5, 0.6)}{float3d("calendario", "c-b", 0.4, 1.2)}{float3d("pino", "c-c", 0.7, 1.8)}</figure>
</div></section>

<section class="section section-search" aria-labelledby="busca-title"><div class="wrap">
  <h2 class="sr-only" id="busca-title">Buscar plantões</h2>
  <form class="filters" data-filters role="search" onsubmit="return false">
    <div class="filter-q">{icon("search")}<label class="sr-only" for="f-q">Buscar</label><input id="f-q" name="q" type="search" placeholder="Cidade, unidade ou especialidade" autocomplete="off"></div>
    <div class="filter-sel"><label for="f-uf">Estado</label><select id="f-uf" name="uf"><option value="">Todos</option>{uf_opts}</select></div>
    <div class="filter-sel"><label for="f-esp">Especialidade</label><select id="f-esp" name="esp"><option value="">Todas</option>{esp_opts}</select></div>
    <fieldset class="filter-tipo"><legend class="sr-only">Tipo de unidade</legend>
      <label><input type="radio" name="tipo" value="" checked> Todas</label>
      {"".join(f'<label><input type="radio" name="tipo" value="{k}"> {v.split(" ")[0]}</label>' for k, v in TIPOS.items())}
    </fieldset>
  </form>
  <div class="results-bar"><p class="results-count" role="status" aria-live="polite" data-count>{N_UNIDADES} unidades</p><button class="link-btn" type="button" data-clear hidden>Limpar filtros</button></div>
  <ul class="units" data-units>{cards}</ul>
  <div class="empty" data-empty hidden>
    <span class="float">{img3d("lupa", cls="empty-art")}</span>
    <h3 class="subtitle">Nada com esses filtros, por enquanto</h3>
    <p class="muted">Deixe seu cadastro com a especialidade e o estado onde quer trabalhar.</p>
    <div class="btn-row" style="justify-content:center"><button class="btn btn-outline" type="button" data-clear>Limpar filtros</button><a class="btn btn-primary" href="#cadastro">Fazer cadastro</a></div>
  </div>
</div></section>

<section class="section section-sky" id="cadastro" aria-labelledby="cad-title"><div class="wrap split">
  <div class="reveal">
    <p class="kicker">Cadastro</p>
    <h2 class="title" id="cad-title">Não achou? <span class="blue">Cadastre-se</span></h2>
    <p class="lede">A mensagem sai pronta no WhatsApp.</p>
  </div>
  <form class="form-card reveal" data-whatsapp-form="medico" data-number="{WA_PLANTAO}" style="--d:.1s" novalidate>
    <div class="form-grid">
      <div class="field full"><label for="m-nome">Nome completo</label><input id="m-nome" name="nome" autocomplete="name" required maxlength="120" data-label="Nome"></div>
      <div class="field"><label for="m-crm">CRM</label><input id="m-crm" name="crm" inputmode="numeric" required maxlength="12" pattern="[0-9]{{3,10}}" data-label="CRM"></div>
      <div class="field"><label for="m-uf">UF do CRM</label><select id="m-uf" name="uf" required data-label="UF do CRM"><option value="">Escolha</option>{all_uf_opts}</select></div>
      <div class="field"><label for="m-esp">Especialidade</label><input id="m-esp" name="especialidade" list="lista-esp" required maxlength="80" data-label="Especialidade"><datalist id="lista-esp">{esp_opts}</datalist></div>
      <div class="field"><label for="m-estado">Onde quer trabalhar</label><select id="m-estado" name="estado" required data-label="Estado de interesse"><option value="">Escolha</option>{all_uf_opts}</select></div>
      <div class="field full"><fieldset><legend>Turnos</legend><div class="options">
        <label><input type="checkbox" value="Dia" data-label="Turnos"> Dia</label>
        <label><input type="checkbox" value="Noite" data-label="Turnos"> Noite</label>
        <label><input type="checkbox" value="Fim de semana" data-label="Turnos"> Fim de semana</label>
      </div></fieldset></div>
    </div>
    <div class="form-foot"><button class="btn btn-primary" type="submit" disabled>{icon("wa")}<span>Preparar mensagem</span></button>
    <p>Nada fica guardado no site. <a href="privacidade.html">Privacidade</a></p></div>
    {form_result()}
  </form>
</div></section>
''', scripts=("main", "paths-bg", "motion", "plantoes", "forms"))

# página antiga -> nova
(ROOT / "para-medicos.html").write_text(f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><title>Plantões | Cirmed</title>
<meta http-equiv="refresh" content="0; url=plantoes.html"><link rel="canonical" href="{SITE_URL}/plantoes.html"><meta name="robots" content="noindex"></head>
<body><p><a href="plantoes.html">Ir para os plantões abertos</a></p></body></html>
''', encoding="utf-8")

# =====================================================================
# Para hospitais (montar equipe)
# =====================================================================
ESP_PEDIDO = ["Clínica Geral", "Pediatria", "Ginecologia e Obstetrícia", "Anestesiologia", "Emergência", "Ortopedia",
              "Cirurgia Geral", "Cardiologia", "Neonatologia", "Infectologia", "Nefrologia", "Psiquiatria",
              "Oftalmologia", "Neurologia", "Dermatologia", "UTI"]
def cobertura(e):
    base = "UTI" if e == "UTI" else e
    us = [p for p in PLANTOES if any(x == base or x.startswith(base) or (base == "UTI" and x.startswith("UTI")) or (base == "Ginecologia e Obstetrícia" and x.startswith("Ginecologia")) for x in p[4])]
    return len(us), len({p[2] for p in us})

picker = "".join(
    f'<label class="pick"><input type="checkbox" name="esp" value="{esc(e)}" data-label="Especialidades" data-units="{cobertura(e)[0]}" data-ufs="{cobertura(e)[1]}"><span>{esc(e)}</span></label>'
    for e in ESP_PEDIDO)

STEPS = [("Visita técnica", "Entender a demanda."), ("Projeto", "Médicos, turnos e escala."),
         ("Começo", "Equipe treinada na rotina."), ("Acompanhamento", "Ajustes e auditoria.")]

page("para-hospitais.html",
 "Para hospitais e unidades de saúde | Cirmed",
 "Escolha as especialidades e os turnos e monte o pedido de plantonistas. Terceirização da escala, gestão de unidades e equipes para SAMU.",
 f'''<section class="page-hero page-hero-split" aria-labelledby="hero-title">{PATHS}<div class="wrap split">
  <div>
    <p class="kicker">Para hospitais, UPAs e unidades</p>
    <h1 class="display" id="hero-title" data-draw>Faltou plantonista {stroke("hoje?")}</h1>
    <div class="btn-row">{wa_btn()}<a class="btn btn-outline" href="#equipe"><span>Montar equipe</span>{icon("arrow")}</a></div>
  </div>
  <figure class="hero-cluster" aria-hidden="true">{float3d("hospital", "c-main", 0.25)}{float3d("ambulancia", "c-a", 0.55, 0.5)}{float3d("calendario", "c-b", 0.45, 1.1)}{float3d("prancheta", "c-c", 0.7, 1.7)}</figure>
</div></section>

<section class="section" id="equipe" aria-labelledby="equipe-title"><div class="wrap">
  <div class="section-head reveal">
    <p class="kicker">Monte sua equipe</p>
    <h2 class="title" id="equipe-title">Quais médicos <span class="blue">você precisa?</span></h2>
  </div>
  <form class="team-builder" data-whatsapp-form="hospital" data-number="{WA_NUMBER}" data-team novalidate>
    <fieldset class="picks"><legend class="sr-only">Especialidades</legend>{picker}</fieldset>
    <div class="team-side">
      <div class="team-summary" aria-live="polite">
        <p class="team-big" data-team-count>0</p>
        <p class="muted" data-team-text>Escolha uma ou mais especialidades.</p>
      </div>
      <div class="field"><fieldset><legend>Turnos</legend><div class="options">
        <label><input type="checkbox" value="Dia" data-label="Turnos"> Dia</label>
        <label><input type="checkbox" value="Noite" data-label="Turnos"> Noite</label>
        <label><input type="checkbox" value="Fim de semana" data-label="Turnos"> Fim de semana</label>
      </div></fieldset></div>
      <div class="field"><label for="h-inst">Instituição</label><input id="h-inst" name="instituicao" autocomplete="organization" required maxlength="160" data-label="Instituição"></div>
      <div class="field"><label for="h-cidade">Cidade e estado</label><input id="h-cidade" name="cidade" required maxlength="120" placeholder="Ex.: Bauru (SP)" data-label="Cidade"></div>
      <div class="field"><label for="h-nome">Seu nome</label><input id="h-nome" name="nome" autocomplete="name" required maxlength="120" data-label="Nome"></div>
      <button class="btn btn-primary" type="submit" disabled>{icon("wa")}<span>Enviar pedido</span></button>
      <p class="hint muted">Sem dados de pacientes. Nada fica guardado no site.</p>
      {form_result()}
    </div>
  </form>
</div></section>

<section class="band-navy band-thin" aria-label="Especialidades">{marquee()}</section>

<section class="section section-sky" aria-labelledby="serv-title"><div class="wrap">
  <div class="section-head reveal"><p class="kicker">Serviços</p><h2 class="title" id="serv-title">O que dá para <span class="blue">contratar</span></h2></div>
  {service_tiles()}
</div></section>

<section class="section" aria-labelledby="como-title"><div class="wrap">
  <div class="section-head reveal"><p class="kicker">Como funciona</p><h2 class="title" id="como-title">Da visita à <span class="blue">escala rodando</span></h2></div>
  <ol class="steps">{"".join(f"<li><h3>{t}</h3><p>{p}</p></li>" for t, p in STEPS)}</ol>
</div></section>

<section class="section" aria-label="Programa de Integridade" style="padding-top:0"><div class="wrap">{TRUST}</div></section>
''', scripts=("main", "paths-bg", "motion", "forms"))

# =====================================================================
# Sobre
# =====================================================================
page("sobre.html",
 "Sobre a Cirmed | Plantões e equipes médicas",
 "CIRMED Serviços Médicos LTDA: sede em Bauru (SP), plantões em todo o Brasil, diretoria e Programa de Integridade.",
 f'''<section class="page-hero page-hero-split" aria-labelledby="hero-title">{PATHS}<div class="wrap split">
  <div>
    <p class="kicker">Sobre</p>
    <h1 class="display" id="hero-title" data-draw>Sobre a {stroke("Cirmed")}</h1>
    <p class="lede">Sede em Bauru (SP). Plantões em {len(UFS_ATIVAS)} estados.</p>
  </div>
  {map_stage("Globo em 3D mostrando as Américas, com pinos azuis sobre o Brasil.")}
</div></section>

<section class="band-navy" aria-label="Números"><div class="wrap">{stats()}</div></section>

<section class="section" aria-labelledby="faz-title"><div class="wrap">
  <div class="section-head reveal"><h2 class="title" id="faz-title">O que a <span class="blue">Cirmed</span> faz</h2></div>
  {service_tiles()}
</div></section>

<section class="section section-sky" aria-labelledby="dados-title"><div class="wrap split">
  <div class="reveal"><p class="kicker">Empresa</p><h2 class="title" id="dados-title">Dados da <span class="blue">empresa</span></h2></div>
  <dl class="facts reveal" style="--d:.1s">
    <div><dt>Razão social</dt><dd>CIRMED Serviços Médicos LTDA</dd></div>
    <div><dt>CNPJ</dt><dd>{CNPJ}</dd></div>
    <div><dt>Sede</dt><dd>Bauru (SP)</dd></div>
    <div><dt>Diretor presidente</dt><dd>Dr. Carlos Azevedo Silva</dd></div>
    <div><dt>E-mail</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
  </dl>
</div></section>

<section class="section" aria-label="Programa de Integridade"><div class="wrap">{TRUST}</div></section>
''')

# =====================================================================
# Contato
# =====================================================================
page("contato.html",
 "Contato | Cirmed",
 f"WhatsApp {WA_SHOW} para instituições, {WA_PLANTAO_SHOW} para plantões e {EMAIL}. Segunda a sexta, das 8h às 19h.",
 f'''<section class="page-hero" aria-labelledby="hero-title">{PATHS}<div class="wrap">
  <p class="kicker">Contato · seg. a sex., 8h às 19h</p>
  <h1 class="display" id="hero-title" data-draw>Fale com a {stroke("Cirmed")}</h1>
</div></section>
<section class="section" aria-labelledby="canais-title" style="padding-top:clamp(32px,5vw,56px)"><div class="wrap">
  <h2 class="sr-only" id="canais-title">Canais</h2>
  <div class="channels">
    <a class="channel channel-art reveal" data-tilt href="{WA}" target="_blank" rel="noopener noreferrer">{img3d("hospital", cls="channel-img")}<small>Instituições</small><strong>{WA_SHOW}</strong><span>WhatsApp</span>{NEW_TAB}</a>
    <a class="channel channel-art reveal" data-tilt style="--d:.06s" href="https://wa.me/{WA_PLANTAO}" target="_blank" rel="noopener noreferrer">{img3d("estetoscopio", cls="channel-img")}<small>Médicos e plantões</small><strong>{WA_PLANTAO_SHOW}</strong><span>WhatsApp</span>{NEW_TAB}</a>
    <a class="channel channel-art reveal" data-tilt style="--d:.12s" href="mailto:{EMAIL}">{img3d("envelope", cls="channel-img")}<small>E-mail</small><strong>{EMAIL}</strong><span>Propostas e documentos</span></a>
  </div>
  <p class="muted contact-note">Instagram <a href="{INSTAGRAM}" target="_blank" rel="noopener noreferrer">@cirmedbrasil{NEW_TAB}</a> · Dados pessoais (LGPD): Marciano Rodrigues Morais, <a href="mailto:marcio@cirmed.com.br">marcio@cirmed.com.br</a></p>
</div></section>
''')

# =====================================================================
# Programa de Integridade e Privacidade (textos legais, mantidos completos)
# =====================================================================
LEGAL_HERO = lambda kicker, t1, t2: f'''<section class="page-hero" aria-labelledby="hero-title"><div class="wrap">
  <nav class="crumbs" aria-label="Você está em"><a href="index.html">Início</a> / {t1} {t2}</nav>
  <p class="kicker">{kicker}</p>
  <h1 class="title" id="hero-title">{t1} <span class="blue">{t2}</span></h1>
</div></section>'''

page("programa-de-integridade.html",
 "Programa de Integridade | Cirmed",
 "Programa de Integridade da CIRMED Serviços Médicos LTDA: princípios, diretrizes, relação com a administração pública e canal para relatar irregularidades.",
 LEGAL_HERO(f"CIRMED Serviços Médicos LTDA · CNPJ {CNPJ}", "Programa de", "Integridade") + f'''
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
<p>Qualquer situação que possa representar descumprimento de normas éticas ou legais pode ser comunicada pelo e-mail <a href="mailto:{EMAIL}">{EMAIL}</a> ou pelo WhatsApp <a href="{WA}" target="_blank" rel="noopener noreferrer">{WA_SHOW}{NEW_TAB}</a>. Todas as comunicações são tratadas com seriedade e confidencialidade.</p>
<h2>Revisão</h2>
<p>O programa é revisto à medida que a empresa, os contratos e a legislação mudam.</p>
</div></section>
''')

page("privacidade.html",
 "Política de Privacidade | Cirmed",
 "Como o site da Cirmed trata dados pessoais: o que é coletado, para quê, por quanto tempo e como pedir acesso, correção ou exclusão.",
 LEGAL_HERO("Atualizada em 3 de novembro de 2026", "Política de", "Privacidade") + f'''
<section class="section" style="padding-top:clamp(32px,5vw,56px)"><div class="wrap prose">
<h2>Quem trata os dados</h2>
<p>CIRMED Serviços Médicos LTDA, CNPJ {CNPJ}, com sede na Rua Gerson França, 12-18, Vila Mesquita, Bauru (SP), CEP 17014-380.</p>
<p>Encarregado pelo tratamento de dados pessoais: Marciano Rodrigues Morais, <a href="mailto:marcio@cirmed.com.br">marcio@cirmed.com.br</a>.</p>
<h2>O que este site coleta</h2>
<p>Nada fica guardado no site. A busca de plantões funciona no seu navegador, e os formulários só montam uma mensagem. Ela é enviada apenas se você decidir mandá-la pelo seu WhatsApp, e a partir daí chega à Cirmed como qualquer outra mensagem.</p>
<p>Os dados que você pode incluir são: nome, instituição, cidade, CRM, UF, especialidade, estado de interesse, turnos e especialidades de que a instituição precisa. Não envie dados de pacientes.</p>
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
<p>Pela Lei Geral de Proteção de Dados (Lei 13.709/2018), você pode pedir a confirmação do tratamento, o acesso, a correção, a anonimização, a portabilidade e a exclusão dos seus dados, além de revogar o consentimento. Escreva para <a href="mailto:marcio@cirmed.com.br">marcio@cirmed.com.br</a> ou <a href="mailto:{EMAIL}">{EMAIL}</a> com o assunto "Dados pessoais".</p>
<p>Os pedidos são atendidos de segunda a sexta, das 8h às 19h, exceto feriados nacionais.</p>
<h2>Segurança</h2>
<p>Os dados recebidos são acessados apenas por pessoas autorizadas da Cirmed, na medida do necessário. A Cirmed nunca pede senhas nem envia arquivos executáveis por e-mail ou mensagem.</p>
<h2>Mudanças nesta política</h2>
<p>Esta política pode ser atualizada. A data no topo da página mostra a versão em vigor.</p>
<h2>Foro</h2>
<p>Esta política segue a legislação brasileira. Fica eleito o foro do domicílio do titular dos dados, salvo disposição legal em contrário.</p>
</div></section>
''')

page("404.html",
 "Página não encontrada | Cirmed",
 "Esta página não existe ou mudou de endereço.",
 f'''<section class="page-hero page-hero-split" aria-labelledby="hero-title" style="min-height:60vh">{PATHS}<div class="wrap split">
  <div>
    <p class="kicker">Erro 404</p>
    <h1 class="display" id="hero-title" data-draw>Página {stroke("não encontrada")}</h1>
    <div class="btn-row"><a class="btn btn-primary" href="index.html"><span>Início</span></a><a class="btn btn-outline" href="plantoes.html">{icon("search")}<span>Plantões</span></a></div>
  </div>
  <figure class="hero-cluster" aria-hidden="true">{float3d("lupa", "c-main", 0.3)}{float3d("pino", "c-a", 0.6, 0.7)}</figure>
</div></section>
''', noindex=True)

# ---------- sitemap e robots ----------
pages = ["index.html", "plantoes.html", "para-hospitais.html", "sobre.html", "contato.html",
         "programa-de-integridade.html", "privacidade.html"]
today = datetime.date.today().isoformat()
urls = "".join(f"<url><loc>{SITE_URL}/{'' if p == 'index.html' else p}</loc><lastmod>{today}</lastmod></url>" for p in pages)
(ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
print("ok:", N_UNIDADES, "unidades,", len(UFS_ATIVAS), "estados,", len(ESP_ATIVAS), "especialidades")
