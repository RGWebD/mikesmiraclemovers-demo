#!/usr/bin/env python3
"""Static generator: python3 generator/build.py -> writes the site into the repo root."""
import os, json, html, sys, math, shutil
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *
G = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(os.path.join(G, '..'))
BASE = os.environ.get('BASE', BASE)
VER = '1'
e = html.escape

I = {
 'phone':'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/>',
 'msg':'<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/>',
 'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
 'left':'<path d="M19 12H5M11 6l-6 6 6 6"/>',
 'x':'<path d="M6 6l12 12M18 6L6 18"/>',
 'plus':'<path d="M12 5v14M5 12h14"/>',
 'pin':'<path d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'star':'<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/>',
 'home':'<path d="M3 11l9-7 9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
 'route':'<circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H15a3 3 0 0 0 0-6H9a3 3 0 0 1 0-6h6.5"/>',
 'bldg':'<path d="M4 21V5l8-2v18M12 8h8v13"/><path d="M7 8h2M7 12h2M7 16h2M15 12h2M15 16h2M2 21h20"/>',
 'box':'<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
 'brief':'<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2M3 13h18"/>',
 'weight':'<path d="M6 9h12l2 11H4z"/><circle cx="12" cy="6" r="2.5"/>',
 'wrap':'<rect x="4" y="4" width="16" height="16" rx="2"/><path d="M4 9l16 6M4 15l16-6"/>',
 'truck':'<path d="M2 6h11v10H2zM13 9h4l4 4v3h-8z"/><circle cx="6" cy="17.5" r="2"/><circle cx="17" cy="17.5" r="2"/>',
 'bolt':'<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 'dolly':'<path d="M5 3l3 14h11"/><circle cx="9" cy="19.5" r="2"/><rect x="10" y="6" width="8" height="8" rx="1" transform="rotate(-12 14 10)"/>',
 'heart':'<path d="M12 20s-7-4.4-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.6-7 10-7 10z"/>',
 'check':'<path d="M5 12.5l4.5 4.5L19 7"/>',
 'cal':'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 'g':'<path d="M20 12.2c0-.6 0-1.2-.2-1.7H12v3.3h4.5a3.9 3.9 0 0 1-1.7 2.5"/><path d="M19.6 8A8.5 8.5 0 1 0 20.4 13"/>',
}
def ic(n, cls=''):
    return f'<svg class="ic {cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[n]}</svg>'

_dims = {}
def dims(name):
    if name not in _dims: _dims[name] = Image.open(os.path.join(R, 'img', name)).size
    return _dims[name]
def img(k, alt, small=False, eager=False, cls='', sizes=None):
    f = f'{k}-s.webp' if small else f'{k}.webp'
    w, h = dims(f)
    ld = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    srcset = '' if small else f' srcset="img/{k}-s.webp {dims(k+"-s.webp")[0]}w, img/{k}.webp {w}w" sizes="{sizes or "(max-width:860px) 100vw, 50vw"}"'
    c = f' class="{cls}"' if cls else ''
    return f'<img src="img/{f}"{srcset} width="{w}" height="{h}" alt="{e(alt)}" {ld}{c}>'

PAGES = [('index.html','Home'),('services.html','Services'),('work.html','Our Work'),('about.html','About'),('reviews.html','Reviews'),('contact.html','Contact')]
STAR5 = '<span class="stars" aria-hidden="true">' + ''.join(f'<svg viewBox="0 0 24 24">{I["star"]}</svg>' for _ in range(5)) + '</span>'
def stars(n=4.7, label=True):
    pct = n/5*100
    return f'<span class="stars-w" role="img" aria-label="{n} out of 5 stars"><span class="stars-bg">{STAR5}</span><span class="stars-fg" style="width:{pct:.0f}%">{STAR5}</span></span>'

def head(page, title, desc, crumbs_ld, extra_ld=None):
    url = BASE + ('' if page == 'index.html' else page)
    lds = [business_ld()] + ([crumbs_ld] if crumbs_ld else []) + (extra_ld or [])
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}"><meta name="theme-color" content="#F6EEDF">
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(NAME)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}img/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}img/og.jpg">
<link rel="icon" href="favicon.svg" type="image/svg+xml"><link rel="icon" href="favicon.ico" sizes="any"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Alfa+Slab+One&family=DM+Sans:opsz,wght@9..40,400..800&family=Permanent+Marker&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css?v={VER}">{ld}</head>'''

def hours_spec():
    out = []
    for d,o,c,ho,hc in HOURS:
        out.append({"@type":"OpeningHoursSpecification","dayOfWeek":d,"opens":f"{ho:02d}:00","closes":f"{hc:02d}:00"})
    return out

def business_ld():
    return {"@context":"https://schema.org","@type":"MovingCompany","@id":BASE+"#business","name":LEGAL,"alternateName":NAME,"slogan":TAGLINE,
      "description":"Jacksonville, Florida moving company: local, apartment, storage-unit, office and long-distance moves, packing and wrapping, hot tubs and heavy items, single-item pickups and loading help. Online estimates. Asian-owned and LGBTQ+ friendly.",
      "url":BASE,"telephone":TEL,"image":BASE+"img/og.jpg","logo":BASE+"brand/logo-stacked-light.svg",
      "address":{"@type":"PostalAddress","addressLocality":CITY,"addressRegion":REGION,"addressCountry":"US"},
      "areaServed":[{"@type":"City","name":"Jacksonville, FL"},{"@type":"City","name":"Orange Park, FL"}],
      "openingHoursSpecification":hours_spec(),"hasMap":MAPS_LONG,"sameAs":[MAPS_LONG],
      "aggregateRating":{"@type":"AggregateRating","ratingValue":RATING,"reviewCount":str(REVIEWS),"bestRating":"5"},
      "hasOfferCatalog":{"@type":"OfferCatalog","name":"Moving services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":html.unescape(s[1]),"description":s[3]}} for s in SVC]},
      "review":[{"@type":"Review","author":{"@type":"Person","name":r['name']},"reviewRating":{"@type":"Rating","ratingValue":"5","bestRating":"5"},"reviewBody":r['text']} for r in REVIEWS_LIST]}

def crumbs(page, label):
    items = [{"@type":"ListItem","position":1,"name":"Home","item":BASE}]
    if page != 'index.html': items.append({"@type":"ListItem","position":2,"name":label,"item":BASE+page})
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}

def nav(page):
    links = ''.join(f'<li><a href="{p}"{" aria-current=page" if p==page else ""}>{l}</a></li>' for p,l in PAGES)
    mlinks = ''.join(f'<a class="mm-l" href="{p}"{" aria-current=page" if p==page else ""} style="--d:{i}"><span>BOX 0{i+1}</span>{l}</a>' for i,(p,l) in enumerate(PAGES))
    return f'''<a class="skip" href="#main">Skip to content</a><div class="tapebar" aria-hidden="true"><i></i></div>
<header class="nav"><div class="nav-in"><a class="brand" href="index.html" aria-label="{e(NAME)} home"><img src="brand/logo-horizontal-light.svg" alt="{e(LEGAL)}" width="400" height="92"></a>
<nav aria-label="Main"><ul>{links}</ul></nav>
<div class="acts"><a class="btn line sm" href="contact.html#estimate">{ic('cal')}<span>Estimate</span></a><a class="btn red sm mag" href="tel:{TEL}">{ic('phone')}<span>{PHONE}</span></a></div>
<button class="menu-btn" aria-expanded="false" aria-controls="mmenu" aria-label="Open menu"><i></i><i></i></button></div></header>
<div class="mmenu" id="mmenu" aria-hidden="true"><nav aria-label="Mobile">{mlinks}</nav>
<div class="mm-foot"><a class="btn red" href="tel:{TEL}">{ic('phone')}Call {PHONE}</a><a class="btn line-l" href="contact.html#estimate">{ic('cal')}Get an online estimate</a></div></div>'''

def badge(cls=''):
    return f'<span class="live {cls}" data-live><i></i><span>Hours today</span></span>'

def hours_table():
    rows = ''.join(f'<tr data-day="{i}"><th scope="row">{d}</th><td>{o} \u2013 {c}</td></tr>' for i,(d,o,c,_,_) in enumerate(HOURS))
    order = rows  # Sunday first matches JS getDay
    return f'<table class="hrs"><caption class="sr">Business hours (Eastern time)</caption>{order}</table>'

def footer():
    links = ''.join(f'<li><a href="{p}">{l}</a></li>' for p,l in PAGES)
    hrs = '<br>'.join(['Mon\u2013Fri 6 AM \u2013 10 PM','Sat 6 AM \u2013 9 PM','Sun 8 AM \u2013 8 PM'])
    return f'''<footer class="foot"><div class="tape-strip" aria-hidden="true"><span>{'FRAGILE \u00b7 HANDLE WITH CARE \u00b7 THIS SIDE UP \u00b7 WE MAKE IT LOOK EASY! \u00b7 '*6}</span></div><div class="wrap">
<div class="foot-top"><img src="brand/logo-stacked-dark.svg" alt="{e(LEGAL)}" width="300" height="200" loading="lazy" class="foot-logo">
<p class="foot-big">{SLOGAN}.<a href="tel:{TEL}">{PHONE}</a></p></div>
<div class="foot-grid">
<div><h3>Pages</h3><ul>{links}</ul></div>
<div><h3>Call or estimate</h3><p><a href="tel:{TEL}">{PHONE}</a></p><p><a href="contact.html#estimate">Request an online estimate</a></p><p><a href="{MAPS}" rel="noopener" target="_blank">See us on Google</a></p></div>
<div><h3>Hours</h3><p>{hrs}</p><p>{badge('sm')}</p></div>
<div><h3>Service area</h3><p>Based in {CITY}, {REGION}. Moves across Jacksonville, Orange Park and beyond, including long-distance runs like Jacksonville to Savannah.</p></div>
</div>
<div class="foot-bot"><span>\u00a9 2026 {e(LEGAL)}</span><span>Asian-owned \u00b7 LGBTQ+ friendly</span><span>Demo design by RGWebD</span></div></div></footer>
<div class="mbar"><a href="tel:{TEL}" class="btn red">{ic('phone')}Call now</a><a href="contact.html#estimate" class="btn line-d">{ic('cal')}Estimate</a></div>
<div class="demo"><span>Design preview by <b>RGWebD</b></span><button aria-label="Dismiss design preview notice">{ic('x')}</button></div>
<script src="script.js?v={VER}" defer></script></body></html>'''

def page_hero(eyebrow, h1, lede, photo, alt, label='CONTENTS'):
    return f'''<section class="phero"><div class="wrap phero-in"><div class="ph-copy">
<span class="eyebrow">{eyebrow}</span><h1 class="h1 split"><span class="ln"><span>{h1}</span></span></h1><p class="lede rv">{lede}</p>
<div class="cta-row rv"><a class="btn red mag" href="tel:{TEL}">{ic('phone')}Call {PHONE}</a><a class="btn line" href="contact.html#estimate">{ic('cal')}Online estimate</a></div></div>
<figure class="ph-photo rv"><div class="label-card"><div class="lc-head"><span>{label}</span><span class="lc-code">MMM\u00b7JAX</span></div>{img(photo, alt, eager=True, sizes="(max-width:860px) 92vw, 40vw")}</div><span class="tape t1"></span><span class="tape t2"></span></figure></div></section>'''

def cta_band():
    return f'''<section class="cta" aria-labelledby="cta-h"><div class="cta-tape" aria-hidden="true"></div><div class="wrap cta-in">
<span class="marker rv">\u201c{SLOGAN}\u201d</span><h2 class="h2 split" id="cta-h"><span class="ln"><span>Moving soon? Let\u2019s get it on the truck.</span></span></h2>
<p class="lede rv">Call or text for a quick, honest estimate. Open early, open late, seven days a week.</p>
<div class="cta-row rv"><a class="btn ink xl mag" href="tel:{TEL}">{ic('phone')}{PHONE}</a><a class="btn line-l xl" href="contact.html#estimate">{ic('cal')}Request an online estimate</a></div></div></section>'''

def marq(items, cls='marq'):
    s = ''.join(f'<span>{x}</span><i>\u2726</i>' for x in items)
    return f'<div class="{cls}" aria-hidden="true"><div class="mq-t">{s*3}</div></div>'

def excerpt(t, n=230):
    if len(t) <= 420: return t, False
    cut = t[:n]; cut = cut[:cut.rfind(' ')]
    return cut.rstrip(',;:') + '\u2026', True
def rv_slides():
    out = ''
    for r in REVIEWS_LIST:
        body, cut = excerpt(r['text'])
        more = f'<a class="sl-more" href="reviews.html#r-{slug(r["name"])}">Read {r["name"].split()[0]}\u2019s full review</a>' if cut else ''
        out += f'''<article class="slide" aria-roledescription="slide"><div class="sl-head"><span class="sl-from">FROM</span><b>{e(r["name"])}</b><span class="sl-tag">{e(r["tag"])}</span></div>
<div class="sl-body">{stars(5)}<p class="sl-pull">\u201c{e(r["pull"])}\u201d</p><blockquote><p>{e(body).replace(chr(10),"<br>")}</p></blockquote>{more}</div><div class="sl-foot"><span class="barcode" aria-hidden="true"></span><span>Google review \u00b7 {e(r["age"])}</span></div></article>'''
    return out
def slug(n): return ''.join(c.lower() if c.isalnum() else '-' for c in n).strip('-')

def route_svg():
    # simple projection: x=(lon+82.2)*200, y=(32.4-lat)*200
    P = lambda lat, lon: ((lon+82.2)*200, (32.4-lat)*200)
    sav = P(32.08,-81.09); jax = P(30.33,-81.66); op = P(30.17,-81.71)
    coast = "M300 -10 C262 40 252 70 236 110 C224 150 214 190 196 232 C182 268 170 300 160 340 C150 380 146 420 140 470 C136 500 134 520 132 560"
    rt = f"M{op[0]:.0f} {op[1]:.0f} C{op[0]+8:.0f} {op[1]-12:.0f} {jax[0]-6:.0f} {jax[1]+10:.0f} {jax[0]:.0f} {jax[1]:.0f} C{jax[0]+10:.0f} {jax[1]-90:.0f} {sav[0]-70:.0f} {sav[1]+120:.0f} {sav[0]:.0f} {sav[1]:.0f}"
    pin = lambda p, name, sub, side: f'<g class="rm-pin" transform="translate({p[0]:.0f} {p[1]:.0f})"><circle r="7"/><circle r="15" class="rm-halo"/><text x="{16 if side>0 else -16}" y="5" text-anchor="{"start" if side>0 else "end"}">{name}</text><text class="rm-sub" x="{16 if side>0 else -16}" y="22" text-anchor="{"start" if side>0 else "end"}">{sub}</text></g>'
    return f'''<svg class="rmap" viewBox="0 0 340 560" role="img" aria-label="Map sketch: moves from Orange Park and Jacksonville up the coast to Savannah, Georgia">
<defs><pattern id="rm-g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="currentColor" stroke-width=".5" opacity=".18"/></pattern></defs>
<rect width="340" height="560" fill="url(#rm-g)"/>
<g transform="translate(40 0)"><path class="rm-sea" d="{coast} L400 560 L400 -10Z"/><path class="rm-coast" d="{coast}"/>
<text class="rm-lbl" x="250" y="380" transform="rotate(-72 250 380)">ATLANTIC OCEAN</text>
<path class="rm-state" d="M-40 {P(30.71,-82.2)[1]:.0f} L{P(30.71,-81.45)[0]:.0f} {P(30.71,-81.45)[1]:.0f}"/><text class="rm-st" x="-30" y="{P(30.71,-82.2)[1]-8:.0f}">GEORGIA</text><text class="rm-st" x="-30" y="{P(30.71,-82.2)[1]+20:.0f}">FLORIDA</text>
<path class="rm-route-bg" d="{rt}"/><path class="rm-route" id="rm-route" d="{rt}" pathLength="1"/>
{pin(sav,"Savannah","Long-distance move",-1)}{pin(jax,"Jacksonville","Home base",1)}{pin(op,"Orange Park","Local moves",-1)}
<g class="rm-truck" transform="translate({op[0]:.0f} {op[1]:.0f})"><rect x="-13" y="-9" width="17" height="13" rx="2"/><path d="M4 -5h5l4 4v5H4z"/><circle cx="-7" cy="5" r="2.6"/><circle cx="8" cy="5" r="2.6"/></g></g></svg>'''

def home():
    t, d = f'{NAME} | Jacksonville Movers \u00b7 4.7\u2605 from {REVIEWS} reviews', f'Jacksonville movers rated {RATING}\u2605 on Google from {REVIEWS} reviews. Local, apartment, storage, office and long-distance moves, packing, hot tubs and heavy items. Open 7 days. Call {PHONE}.'
    why = [('clock','Early starts, late finishes','Open from 6 AM on weekdays and Saturdays, 8 AM on Sundays, and into the evening.'),
           ('wrap','Wrapped, padded, stacked tight','Blankets and shrink wrap on the furniture, and a truck packed like a puzzle.'),
           ('bolt','Last-minute? Still yes.','Reviewers tell us about canceled movers and two-day deadlines we still made.'),
           ('heart','Fair, clear pricing','Customers keep using the words \u201cfair\u201d, \u201ctransparent\u201d and \u201cno hidden fees\u201d.')]
    whyh = ''.join(f'<li class="why-i rv" style="--d:{i}"><span class="why-n">0{i+1}</span>{ic(a)}<h3>{b}</h3><p>{c}</p></li>' for i,(a,b,c) in enumerate(why))
    cards = ''
    for i,k in enumerate(['local','apt','storage','office','heavy','pack']):
        s = next(x for x in SVC if x[0]==k)
        cards += f'''<a class="scard tilt rv" style="--d:{i%3}" href="services.html#{k}"><span class="sc-tape"></span><figure class="sc-img">{img(s[2], html.unescape(s[1]), small=True)}</figure>
<div class="sc-b"><span class="sc-lbl">BOX {i+1:02d}</span><h3>{s[1]}</h3><p>{s[3]}</p><span class="more">Details {ic('arrow')}</span></div></a>'''
    gauges = [('4.7','1','Google rating','\u2605 average'),(str(REVIEWS),'0','Google reviews','and counting'),('7','0','Days a week','open every day'),('6','0','AM start','Mon\u2013Sat')]
    gh = ''.join(f'<div class="crate rv" style="--d:{i}"><span class="cr-top"></span><b><span data-to="{v}" data-dec="{dc}">0</span>{"" if i!=0 else ""}</b><span class="cr-l">{l}</span><span class="cr-s marker">{s}</span></div>' for i,(v,dc,l,s) in enumerate(gauges))
    tet = ''.join(f'<i style="--x:{x};--y:{y};--w:{w};--h:{h};--d:{n}" class="tb c{c}"></i>' for n,(x,y,w,h,c) in enumerate([(0,4,2,2,1),(2,5,2,1,2),(4,4,1,2,3),(2,4,2,1,1),(5,3,1,3,2),(0,2,1,2,3),(1,3,1,1,2),(1,2,3,1,1),(4,2,1,2,1),(0,0,2,2,2),(2,0,1,2,3),(3,1,2,1,2),(5,0,1,3,1),(3,0,2,1,3)]))
    body = f'''{head('index.html', t, d, crumbs('index.html','Home'))}<body class="home">
<div class="loader" aria-hidden="true"><div class="ld-box"><span class="ld-flap l"></span><span class="ld-flap r"></span><span class="ld-body"><span class="ld-tape"></span><span class="ld-txt">MIKE\u2019S</span></span></div><span class="ld-cap marker">We make it look easy!</span></div>
{nav('index.html')}<main id="main">
<section class="hero" aria-labelledby="h1"><div class="hero-bg" aria-hidden="true"><span class="bigout">MIRACLE</span></div>
<div class="wrap hero-in"><div class="h-copy">
<span class="eyebrow">Jacksonville movers \u00b7 Orange Park \u00b7 Long distance</span>
<h1 class="h1 split" id="h1"><span class="ln"><span>Moving day,</span></span><span class="ln"><span>made to look</span></span><span class="ln"><span><em class="marker">easy.</em></span></span></h1>
<p class="lede rv">Local moves, apartments, storage units, offices, hot tubs and long hauls, wrapped up and packed tight by a crew with {REVIEWS} Google reviews behind it.</p>
<div class="cta-row rv"><a class="btn red xl mag" href="tel:{TEL}">{ic('phone')}Call {PHONE}</a><a class="btn line xl" href="contact.html#estimate">{ic('cal')}Online estimate</a></div>
<div class="trust rv"><div class="tr-score"><b>{RATING}</b>{stars(4.7)}</div><div class="tr-t"><b>{REVIEWS} Google reviews</b><span>Asian-owned \u00b7 LGBTQ+ friendly</span></div>{badge()}</div></div>
<figure class="h-art rv"><div class="label-card big"><div class="lc-head"><span>FROM: Mike\u2019s Miracle Movers</span><span class="lc-code">904\u2011710\u20111565</span></div>
<div class="h-photo">{img('g01','The Mike\u2019s Miracle Movers box truck with three crew members in green team shirts',eager=True,sizes="(max-width:860px) 92vw, 48vw")}
<button class="pin" style="--x:90%;--y:40%" aria-expanded="false"><span class="sr">About the truck lettering</span>{ic('plus')}<span class="pin-tip">Our number, painted right on the truck. You can\u2019t miss us.</span></button>
<button class="pin" style="--x:52%;--y:62%" aria-expanded="false"><span class="sr">About the crew</span>{ic('plus')}<span class="pin-tip">The crew, in team shirts, ready to roll.</span></button>
<button class="pin" style="--x:16%;--y:66%" aria-expanded="false"><span class="sr">About the truck</span>{ic('plus')}<span class="pin-tip">Our own box truck, lettered with everything we do.</span></button></div>
<div class="lc-foot"><span>TO: <b>Your new place</b></span><span class="barcode" aria-hidden="true"></span></div></div>
<span class="tape t1"></span><span class="tape t2"></span><span class="stamp" aria-hidden="true"><svg viewBox="0 0 120 120"><defs><path id="st-c" d="M60 60m-44 0a44 44 0 1 1 88 0a44 44 0 1 1-88 0"/></defs><text><textPath href="#st-c">HANDLE WITH CARE \u2022 HANDLE WITH CARE \u2022 </textPath></text><path d="M60 38l14 18h-9v24h-10V56h-9z"/></svg></span></figure>
</div></section>
<div class="tape-marq">{marq(['We make it look EASY!']+TRUCK_LINES+['Online estimates','Open 7 days'],'marq')}</div>
<section class="sec why" aria-labelledby="why-h"><div class="wrap"><div class="sec-head"><span class="eyebrow rv">Why Jacksonville calls Mike\u2019s</span><h2 class="h2 split" id="why-h"><span class="ln"><span>Careful hands. <em>Strong backs.</em></span></span></h2></div>
<ul class="why-g">{whyh}</ul></div></section>
<section class="sec crates" aria-label="By the numbers"><div class="wrap crate-g">{gh}</div></section>
<section class="tetris" aria-labelledby="tet-h"><div class="wrap tet-in">
<figure class="tet-photo rv">{img('g04','Truck interior packed with blue blanket-wrapped furniture while a crew member loads an iron gate',sizes="(max-width:860px) 92vw, 40vw")}<figcaption class="marker">Packed tight. Nothing shifting.</figcaption></figure>
<div class="tet-copy"><span class="eyebrow light rv">Loading like a puzzle</span><h2 class="h2 split" id="tet-h"><span class="ln"><span>\u201cThey are <em>Tetris masters!</em>\u201d</span></span></h2>
<p class="lede rv">That\u2019s Laura Mitchell on Google. Her 2 bed, 2 bath was <b>packed and unloaded in three hours total.</b> Every piece is blanket-wrapped, strapped and stacked so it rides safe and comes off fast.</p>
<div class="tet-grid rv" aria-hidden="true"><div class="tg-truck">{tet}</div><span class="tg-cab"></span></div>
<a class="btn sap mag rv" href="services.html#pack">{ic('wrap')}How we pack &amp; wrap</a></div></div></section>
<section class="sec svcs" aria-labelledby="sv-h"><div class="wrap"><div class="sec-head row"><div><span class="eyebrow rv">What we move</span><h2 class="h2 split" id="sv-h"><span class="ln"><span>Whatever\u2019s going, <em>we\u2019ve got it.</em></span></span></h2></div><a class="btn line rv" href="services.html">All 10 services {ic('arrow')}</a></div>
<div class="sc-grid">{cards}</div><p class="sc-hint" aria-hidden="true">Swipe for more {ic("arrow")}</p></div></section>
<section class="route" aria-labelledby="rt-h"><div class="wrap rt-in"><div class="rt-copy"><span class="eyebrow rv">Across town or up the coast</span><h2 class="h2 split" id="rt-h"><span class="ln"><span>Orange Park to <em>Savannah,</em> and everywhere between.</span></span></h2>
<p class="lede rv">Most of our days are local, across Jacksonville and Orange Park. When you\u2019re leaving town, the same crew makes the long drive. Manzima Jain\u2019s family went all the way from Jacksonville to Savannah:</p>
<blockquote class="rt-q rv"><p>\u201cHe handled our furniture and belongings with great care, and everything arrived safely.\u201d</p><cite>Manzima Jain \u00b7 Google review</cite></blockquote>
<a class="btn red mag rv" href="services.html#long">{ic('route')}Long-distance moves</a></div>
<div class="rt-map rv">{route_svg()}</div></div></section>
<section class="sec rvband" aria-labelledby="rv-h"><div class="wrap rv-wrap"><div class="rv-score rv"><span class="eyebrow">Google reviews</span><b data-to="4.7" data-dec="1">0</b>{stars(4.7)}<p>from <strong>{REVIEWS}</strong> reviews</p><a class="btn line sm" href="reviews.html">Read reviews {ic('arrow')}</a></div>
<div class="car" data-car aria-roledescription="carousel" aria-label="Customer reviews"><h2 class="sr" id="rv-h">What customers say</h2><div class="car-track">{rv_slides()}</div>
<div class="car-nav"><button class="prev" aria-label="Previous review">{ic('left')}</button><div class="car-dots"></div><button class="next" aria-label="Next review">{ic('arrow')}</button></div></div></div></section>
<section class="sec teasers" aria-label="More"><div class="wrap ts-g">
<a class="ts rv" href="work.html" style="--d:0"><span class="ts-flap"></span><span class="ts-l">Box 07 \u00b7 Our Work</span>{ic('box')}<b>Real jobs, real photos</b><span class="ts-m marker">No stock photos</span><span class="more">See the gallery {ic('arrow')}</span></a>
<a class="ts rv" href="about.html" style="--d:1"><span class="ts-flap"></span><span class="ts-l">Box 08 \u00b7 About</span>{ic('heart')}<b>Who\u2019s behind the truck</b><span class="ts-m marker">Asian-owned \u00b7 LGBTQ+ friendly</span><span class="more">Meet us {ic('arrow')}</span></a>
<a class="ts rv" href="contact.html#estimate" style="--d:2"><span class="ts-flap"></span><span class="ts-l">Box 09 \u00b7 Contact</span>{ic('cal')}<b>Get your estimate</b><span class="ts-m marker">Online estimates</span><span class="more">Start here {ic('arrow')}</span></a>
</div></section>
{cta_band()}</main>{footer()}'''
    return body

def services():
    t = f'Moving Services in Jacksonville | {NAME}'
    d = f'Local, long-distance, apartment, storage, office and commercial moves, hot tubs and heavy items, packing and wrapping, Marketplace pickups and loading help in Jacksonville, FL. Call {PHONE}.'
    secs = ''
    for i,s in enumerate(SVC):
        k,title,ph,short,long,proof,icn = s
        q = ''
        if proof:
            r = next(x for x in REVIEWS_LIST if x['name']==proof)
            q = f'<blockquote class="sv-q"><p>\u201c{e(r["pull"])}\u201d</p><cite>{e(proof)} \u00b7 Google</cite></blockquote>'
        media = f'<figure class="sv-img">{img(ph, html.unescape(title), sizes="(max-width:860px) 92vw, 44vw")}<span class="tape t1"></span></figure>' if ph else f'<div class="sv-ic" aria-hidden="true">{ic(icn)}<span class="marker">{["","","","","","","","Grab it","Call us","Heave-ho"][i]}</span></div>'
        secs += f'''<section class="sv{" flip" if i%2 else ""}{" noimg" if not ph else ""}" id="{k}" aria-labelledby="sv-{k}"><div class="wrap sv-in">{media}
<div class="sv-copy rv"><span class="sv-n">BOX {i+1:02d}</span><h2 class="h2s" id="sv-{k}">{ic(icn)}{title}</h2><p class="sv-short">{short}</p><p>{long}</p>{q}
<a class="btn red sm mag" href="tel:{TEL}">{ic('phone')}Call about {html.unescape(title).split(" &")[0].split(" (")[0].lower()}</a></div></div></section>'''
    steps = [('phone','Call or request an estimate','Tell us what\u2019s moving, from where to where, and when. Online estimates are available.'),
             ('cal','Lock in the day','Early mornings, evenings and weekends: we\u2019re open seven days.'),
             ('wrap','Wrap, pad &amp; load','Furniture gets blankets and shrink wrap, then the truck gets packed tight.'),
             ('home','Set down where you want it','We place everything where you want it in the new place.')]
    sth = ''.join(f'<li class="step rv" style="--d:{i}"><span class="st-dot">{ic(a)}</span><div><span class="st-n">Step {i+1}</span><h3>{b}</h3><p>{c}</p></div></li>' for i,(a,b,c) in enumerate(steps))
    il = {"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"name":html.unescape(s[1]),"url":BASE+"services.html#"+s[0]} for i,s in enumerate(SVC)]}
    jump = ''.join(f'<a href="#{s[0]}">{s[1]}</a>' for s in SVC)
    return f'''{head('services.html', t, d, crumbs('services.html','Services'), [il])}<body>{nav('services.html')}<main id="main">
{page_hero('Services','Ten ways we <em>make it easy.</em>','From a single Marketplace hutch to a whole house headed for Savannah. Everything below comes straight from what our customers hired us for.','g11','A hot tub moved into place on a back patio','PACKING LIST')}
<nav class="jump" aria-label="Jump to a service"><div class="wrap jump-in">{jump}</div></nav>
{secs}
<section class="sec how" aria-labelledby="how-h"><div class="wrap how-in"><div><span class="eyebrow rv">How it works</span><h2 class="h2 split" id="how-h"><span class="ln"><span>Four steps to <em>moved in.</em></span></span></h2><p class="lede rv">No mystery, no runaround. Amy Crum (eight years a customer) says we gave her \u201ca clear breakdown of the pricing and moving process\u201d from the first phone call.</p></div>
<ol class="steps">{sth}</ol></div></section>
{cta_band()}</main>{footer()}'''

def work():
    t = f'Our Work: Real Moving Photos | {NAME}'
    d = f'Photos from real Mike\u2019s Miracle Movers jobs in the Jacksonville area: the truck and crew, wrapped and stacked loads, hot tubs, storage units and finished rooms.'
    order = ['g04','g05','g03','g06','g07','g02','g11','g09']
    filt = [('all','All'),('crew','Truck &amp; crew'),('pack','Packing'),('heavy','Hot tubs'),('rooms','Rooms &amp; units')]
    fb = ''.join(f'<button class="fbtn" data-f="{k}" aria-pressed="{"true" if k=="all" else "false"}">{l}</button>' for k,l in filt)
    gi = ''.join(f'<figure class="gi rv" data-tag="{CAP[k][1]}" style="--d:{i%3}"><button class="gi-b" data-full="img/{k}.webp" data-cap="{e(CAP[k][0])}" aria-label="Open photo: {e(CAP[k][0])}">{img(k, CAP[k][0], small=True)}</button><figcaption>{e(CAP[k][0])}</figcaption></figure>' for i,k in enumerate(order))
    return f'''{head('work.html', t, d, crumbs('work.html','Our Work'))}<body>{nav('work.html')}<main id="main">
{page_hero('Our Work','Real moves. <em>Real photos.</em>','No stock photos here: just our truck, our crew and the stuff we\u2019ve carried, from customers\u2019 living rooms to the back patio.','g01','The Mike\u2019s Miracle Movers truck and crew','PHOTO LOG')}
<section class="sec gal" aria-label="Photo gallery"><div class="wrap"><div class="filters" role="group" aria-label="Filter photos">{fb}</div><div class="g-grid">{gi}</div>
<p class="muted small gal-n">Photos from our Google Business Profile. Plates and other businesses\u2019 signs blurred for privacy.</p></div></section>
<div class="lbx" hidden role="dialog" aria-modal="true" aria-label="Photo viewer"><figure><img alt=""><figcaption></figcaption></figure><button class="lbx-x" aria-label="Close">{ic('x')}</button><button class="lbx-p" aria-label="Previous photo">{ic('left')}</button><button class="lbx-n" aria-label="Next photo">{ic('arrow')}</button></div>
{cta_band()}</main>{footer()}'''

def about():
    t = f'About Us | {NAME}, Jacksonville FL'
    d = f'{LEGAL} is an Asian-owned, LGBTQ+ friendly Jacksonville moving company with a {RATING}\u2605 Google rating from {REVIEWS} reviews. Online estimates. Open 7 days.'
    vals = [('heart','Asian-owned','Listed on Google as an Asian-owned business.'),('check','LGBTQ+ friendly','Everyone\u2019s welcome on our schedule and on our truck.'),('cal','Online estimates','Start with an estimate before anyone lifts a box.'),('clock','Open 7 days','Weekdays 6 AM to 10 PM, Saturdays to 9 PM, Sundays 8 AM to 8 PM.')]
    vh = ''.join(f'<li class="val rv" style="--d:{i}">{ic(a)}<h3>{b}</h3><p>{c}</p></li>' for i,(a,b,c) in enumerate(vals))
    return f'''{head('about.html', t, d, crumbs('about.html','About'))}<body>{nav('about.html')}<main id="main">
{page_hero('About Mike\u2019s','The crew behind <em>the truck.</em>','A Jacksonville moving company with a big white truck, a phone number you\u2019ll remember, and a motto we try to live up to on every job.','g02','The Mike\u2019s Miracle Movers truck parked on a commercial job','ABOUT US')}
<section class="sec story" aria-labelledby="st-h"><div class="wrap story-in"><div class="story-copy"><span class="eyebrow rv">Our story, in our customers\u2019 words</span><h2 class="h2 split" id="st-h"><span class="ln"><span>\u201cWe make it look <em class="marker">EASY!</em>\u201d</span></span></h2>
<p class="lede rv">It\u2019s painted on the side of our truck, and it\u2019s the promise behind every move: show up on time, wrap everything, pack the truck tight, and set it all down where you want it.</p>
<p class="rv">Customers come back. Amy Crum wrote that she\u2019s used us <b>for 8 years</b>. Laura Mitchell has \u201cused them several times.\u201d Erin Montgomery found us because a neighbor recommended us, and plans to call us again for her next home.</p>
<blockquote class="pull rv"><p>\u201cIt gave me so much peace of mind knowing I had these 2 awesome guys taking care of my move.\u201d</p><cite>Erin Montgomery \u00b7 Google review</cite></blockquote></div>
<figure class="story-img rv">{img('g05','Two movers carrying a shrink-wrapped hot tub with orange lifting straps',sizes="(max-width:860px) 92vw, 44vw")}<figcaption class="marker">Straps, wrap and teamwork.</figcaption></figure></div></section>
<section class="sec vals" aria-labelledby="vl-h"><div class="wrap"><div class="sec-head"><span class="eyebrow rv">Good to know</span><h2 class="h2 split" id="vl-h"><span class="ln"><span>Straight from <em>our Google profile.</em></span></span></h2></div><ul class="val-g">{vh}</ul></div></section>
<section class="sec truckl" aria-labelledby="tk-h"><div class="wrap tk-in"><div class="tk-side"><span class="tk-name">MIKE\u2019S<br>MIRACLE<br>MOVERS</span><span class="tk-tag marker">We make it look EASY!</span><span class="tk-ph">904-710-1565</span><span class="tk-lines">{" \u00b7 ".join(TRUCK_LINES)}</span><span class="tk-w w1"></span><span class="tk-w w2"></span></div>
<div><span class="eyebrow rv">What\u2019s on the truck</span><h2 class="h2 split" id="tk-h"><span class="ln"><span>Six words, <em>one crew.</em></span></span></h2><p class="lede rv">Moving, commercial, residential, local, storage, business: it\u2019s all lettered on the side of the truck, and it\u2019s all work we do. See the full list on our services page.</p><a class="btn red mag rv" href="services.html">{ic('box')}See all services</a></div></div></section>
{cta_band()}</main>{footer()}'''

def reviews():
    t = f'Reviews: {RATING}\u2605 from {REVIEWS} Google Reviews | {NAME}'
    d = f'{NAME} is rated {RATING} out of 5 from {REVIEWS} Google reviews. Read what Jacksonville customers say, quoted word for word.'
    cards = ''
    for i,r in enumerate(REVIEWS_LIST):
        paras = ''.join(f'<p>{e(p)}</p>' for p in r['text'].split('\n') if p.strip())
        cards += f'''<article class="rcard rv" id="r-{slug(r["name"])}" style="--d:{i%2}"><div class="rc-head"><span class="rc-av" aria-hidden="true">{r["name"][0]}</span><div><b>{e(r["name"])}</b><span>{e(r["age"])} \u00b7 Google</span></div><span class="rc-tag">{e(r["tag"])}</span></div>
{stars(5)}<blockquote>{paras}</blockquote><span class="barcode" aria-hidden="true"></span></article>'''
    return f'''{head('reviews.html', t, d, crumbs('reviews.html','Reviews'))}<body>{nav('reviews.html')}<main id="main">
<section class="phero rvhero"><div class="wrap rvh-in"><div><span class="eyebrow">Reviews</span><h1 class="h1 split"><span class="ln"><span>{REVIEWS} reviews. <em>One theme:</em> easy.</span></span></h1><p class="lede rv">Ten of our five-star Google reviews, quoted word for word. Read all {REVIEWS} on Google.</p>
<div class="cta-row rv"><a class="btn red mag" href="{MAPS}" rel="noopener" target="_blank">{ic('g')}All reviews on Google</a><a class="btn line" href="tel:{TEL}">{ic('phone')}{PHONE}</a></div></div>
<div class="big-score rv"><b data-to="4.7" data-dec="1">0</b>{stars(4.7)}<span>{REVIEWS} Google reviews</span></div></div></section>
<section class="sec rvlist" aria-label="Customer reviews"><div class="wrap rc-grid">{cards}</div></section>
{cta_band()}</main>{footer()}'''

def contact():
    t = f'Contact & Online Estimate | {NAME}, Jacksonville'
    d = f'Call {PHONE} or request an online estimate from {NAME}. Open Mon\u2013Fri 6 AM\u201310 PM, Sat 6 AM\u20139 PM, Sun 8 AM\u20138 PM. Serving Jacksonville, Orange Park and long-distance moves.'
    faqs = [('What areas do you serve?','We\u2019re based in Jacksonville, FL and move people across Jacksonville and Orange Park. We also do long-distance moves; customers have hired us for Jacksonville to Savannah.'),
            ('What are your hours?','Monday to Friday 6 AM to 10 PM, Saturday 6 AM to 9 PM and Sunday 8 AM to 8 PM (Eastern). Holiday hours may vary, so give us a call.'),
            ('Do you give estimates?','Yes. Online estimates are available. Use the form on this page or call '+PHONE+'.'),
            ('Can you help with a last-minute move?','Often, yes. Reviewers tell us about stepping in after their original movers canceled, and about a two-day deadline we still made. Call as early as you can.'),
            ('Do you move hot tubs and pianos?','Yes. Jacuzzis, hot tubs, pianos and other heavy items are part of what we do.'),
            ('Do you wrap furniture?','Yes. We use moving blankets and shrink wrap to protect furniture before it goes on the truck.'),
            ('Can you just help load or unload my rental truck?','Yes. We can load or unload a truck you\u2019ve rented, or pick up a single item like a Marketplace purchase.')]
    faqh = ''.join(f'<details class="faq rv"><summary>{q}{ic("plus")}</summary><p>{a}</p></details>' for q,a in faqs)
    fld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    opts = ''.join(f'<option>{html.unescape(s[1])}</option>' for s in SVC)
    return f'''{head('contact.html', t, d, crumbs('contact.html','Contact'), [fld])}<body>{nav('contact.html')}<main id="main">
{page_hero('Contact','Let\u2019s make <em>a move.</em>',f'Call or text {PHONE}, or send the details below and we\u2019ll get back to you with an estimate.','g06','A storage unit neatly loaded with furniture','GET IN TOUCH')}
<section class="sec ct" id="estimate" aria-labelledby="ct-h"><div class="wrap ct-in"><div class="ct-info"><h2 class="h2s rv" id="ct-h">Reach us</h2>
<a class="ct-line rv" href="tel:{TEL}"><span>{ic('phone')}</span><div><small>Call or text</small><b>{PHONE}</b></div></a>
<div class="ct-line rv"><span>{ic('clock')}</span><div><small>Hours (Eastern)</small>{badge('sm')}{hours_table()}<p class="hol" data-hol hidden></p></div></div>
<div class="ct-line rv"><span>{ic('pin')}</span><div><small>Service area</small><b>Jacksonville, Orange Park &amp; beyond</b><p class="muted">We come to you. Long-distance moves too (Jacksonville to Savannah and more).</p></div></div>
<p class="muted rv small">No email listed. The fastest way to reach us is a call or text.</p></div>
<form class="ct-form rv" data-sms="{TEL}" novalidate><span class="cf-tape"></span><h3>Request an online estimate</h3>
<div class="fr"><label>Your name<input name="name" autocomplete="name" required></label><label>Phone<input name="phone" type="tel" autocomplete="tel" required></label></div>
<div class="fr"><label>Moving from<input name="from" placeholder="e.g. Orange Park"></label><label>Moving to<input name="to" placeholder="e.g. Jacksonville Beach"></label></div>
<div class="fr"><label>Move date<input name="date" type="date"></label><label>What kind of move?<select name="svc">{opts}<option>Something else</option></select></label></div>
<label>What\u2019s moving?<textarea name="msg" rows="4" placeholder="Bedrooms, big items (piano, hot tub), stairs or elevator..."></textarea></label>
<button class="btn red xl mag" type="submit">{ic('msg')}Open text message</button><p class="muted small">This opens your phone\u2019s messaging app with the details filled in. Nothing is sent until you hit send.</p></form>
</div></section>
<section class="sec faqs" aria-labelledby="fq-h"><div class="wrap faq-in"><div><span class="eyebrow rv">FAQ</span><h2 class="h2 split" id="fq-h"><span class="ln"><span>Quick <em>answers.</em></span></span></h2></div><div class="faq-list">{faqh}</div></div></section>
<section class="sec mapsec" aria-label="Service area map"><div class="wrap"><div class="map rv"><iframe title="Map of the Jacksonville, FL area we serve" src="https://maps.google.com/maps?q=Jacksonville,+FL&amp;z=10&amp;output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe><span class="map-l marker">Our service area</span></div></div></section>
{cta_band()}</main>{footer()}'''

def notfound():
    b = '/mikesmiraclemovers-demo/'
    s = f'''{head('404.html','Page not found | '+NAME,'This page could not be found.',None)}<body class="nf">{nav('404.html')}<main id="main"><section class="nf-in"><div class="wrap"><span class="nf-box" aria-hidden="true">?</span><span class="eyebrow">404 \u00b7 Lost in the move</span><h1 class="h1">This box went <em class="marker">missing.</em></h1><p class="lede">The page you\u2019re looking for isn\u2019t here. Head back home or give us a call.</p><div class="cta-row"><a class="btn red" href="index.html">Back to home</a><a class="btn line" href="tel:{TEL}">{ic('phone')}{PHONE}</a></div></div></section></main>{footer()}'''
    s = s.replace('<head><meta charset="utf-8">', f'<head><meta charset="utf-8"><base href="{b}">',1).replace('<link rel="canonical"', '<meta name="robots" content="noindex"><link rel="canonical"',1)
    return s

def main():
    out = {'index.html':home(),'services.html':services(),'work.html':work(),'about.html':about(),'reviews.html':reviews(),'contact.html':contact(),'404.html':notfound()}
    for k,v in out.items(): open(os.path.join(R,k),'w').write(v)
    shutil.copy(os.path.join(G,'styles.css'), os.path.join(R,'styles.css')); shutil.copy(os.path.join(G,'script.js'), os.path.join(R,'script.js'))
    open(os.path.join(R,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {BASE}sitemap.xml\n')
    urls=''.join(f'<url><loc>{BASE}{"" if p=="index.html" else p}</loc><changefreq>monthly</changefreq><priority>{"1.0" if p=="index.html" else "0.8"}</priority></url>' for p,_ in PAGES)
    open(os.path.join(R,'sitemap.xml'),'w').write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    llm=f"""# {LEGAL}
> Moving company in Jacksonville, Florida (service-area business; no storefront address published). Rated {RATING}/5 from {REVIEWS} Google reviews. Online estimates. Asian-owned and LGBTQ+ friendly. Truck motto: "{TAGLINE}"

- Phone (call or text): {PHONE}
- Hours (Eastern): Mon-Fri 6 AM-10 PM; Sat 6 AM-9 PM; Sun 8 AM-8 PM. Holiday hours may vary.
- Service area: Jacksonville and Orange Park, FL, plus long-distance moves (customers report Jacksonville to Savannah, GA).
- Email / website: none currently published.
- Pricing: not published; call for an estimate.

## Services
""" + ''.join(f"- {html.unescape(s[1])}: {html.unescape(s[3])}\n" for s in SVC) + f"""
## Pages
- [Home]({BASE}): overview, why choose us, services, long-distance route, reviews
- [Services]({BASE}services.html): each service and how a move works
- [Our Work]({BASE}work.html): photo gallery of real jobs
- [About]({BASE}about.html): who we are, attributes, what's on the truck
- [Reviews]({BASE}reviews.html): ten Google reviews quoted word for word
- [Contact]({BASE}contact.html): phone, estimate form (opens a text message), hours, FAQ
- [Google listing]({MAPS_LONG})
"""
    open(os.path.join(R,'llms.txt'),'w').write(llm)
    print('built', len(out), 'pages')
if __name__ == '__main__': main()
