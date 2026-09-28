#!/usr/bin/env python3
"""Generate the service, service-area and city/county pages for the site.

Run from anywhere:  python3 tools/build_pages.py

Writes:
  /<service-slug>/index.html               (4 service pages)
  /service-areas/index.html                (area hub)
  /service-areas/<city>-ms/index.html      (city pages)
  /service-areas/<county>-county-ms/index.html
  /404.html, /sitemap.xml
and refreshes the BUILD-marked blocks (nav, areas, footer) inside index.html
so the homepage shares the same navigation and internal links.
"""
import html as html_lib
import json
import os
import re
from datetime import date

from site_data import (
    CITIES, COUNTIES, COUNTY_ORDER, EMAIL, FEATURED_COUNTIES, PHONE, PHOTOS,
    QUOTE_URL, REGION_ORDER, REGIONS, SERVICES, SITE, TEL,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = date.today().isoformat()
BIZ_ID = SITE + "/#business"
SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}


# ---------------------------------------------------------------------------
# URL helpers
# ---------------------------------------------------------------------------
def city_url(slug):
    return f"/service-areas/{slug}-ms/"


def county_url(slug):
    return f"/service-areas/{slug}-county-ms/"


def service_url(slug):
    return f"/{slug}/"


def cities_in(county):
    return [s for s, c in CITIES.items() if c["county"] == county]


def plain(text):
    """Decode HTML entities used in copy so text reads cleanly inside JSON-LD."""
    return html_lib.unescape(text)


# ---------------------------------------------------------------------------
# Shared schema
# ---------------------------------------------------------------------------
def business_schema():
    area = [{"@type": "AdministrativeArea", "name": f"{COUNTIES[c]['name']} County, MS"} for c in COUNTY_ORDER]
    area += [{"@type": "City", "name": f"{c['name']}, MS"} for c in CITIES.values()]
    return {
        "@type": ["LocalBusiness", "HomeAndConstructionBusiness"],
        "@id": BIZ_ID,
        "name": "D&Z Sealcoating LLC",
        "alternateName": "Mississippi Sealcoating",
        "url": SITE + "/",
        "logo": SITE + "/favicon.svg",
        "image": SITE + "/og-image.png",
        "telephone": "+1-662-587-3525",
        "email": EMAIL,
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "addressLocality": "Ripley", "addressRegion": "MS",
                    "postalCode": "38663", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": 34.7298, "longitude": -88.9509},
        "openingHoursSpecification": [{
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            "opens": "07:00", "closes": "18:00"}],
        "areaServed": area,
        "sameAs": [QUOTE_URL],
    }


def breadcrumb_schema(crumbs):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": plain(name), "item": SITE + url}
            for i, (name, url) in enumerate(crumbs)
        ],
    }


def faq_schema(faqs):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": plain(q),
             "acceptedAnswer": {"@type": "Answer", "text": plain(re.sub(r"<[^>]+>", "", a))}}
            for q, a in faqs
        ],
    }


# ---------------------------------------------------------------------------
# Layout pieces
# ---------------------------------------------------------------------------
def head(title, desc, path, graph, geo_place="Ripley, Mississippi"):
    schema = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    url = SITE + path
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="{url}">
    <meta name="geo.region" content="US-MS">
    <meta name="geo.placename" content="{geo_place}">
    <meta name="theme-color" content="#0A0A0F">
    <link rel="icon" href="/favicon.svg" type="image/svg+xml">

    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{url}">
    <meta property="og:locale" content="en_US">
    <meta property="og:image" content="{SITE}/og-image.png">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">
    <meta property="og:site_name" content="Mississippi Sealcoating - D&amp;Z Sealcoating LLC">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{SITE}/og-image.png">

    <script type="application/ld+json">
{schema}
    </script>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Inter:wght@400;500;600;700&family=Bebas+Neue&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
"""


LOGO_SVG = """<svg viewBox="0 0 260 70" xmlns="http://www.w3.org/2000/svg" class="logo-svg" role="img" aria-label="D&amp;Z Sealcoating - Mississippi">
                        <path d="M10 8 L35 2 L35 42 Q35 58 22.5 65 Q10 58 10 42 Z" fill="none" stroke="#C9A84C" stroke-width="2.5"/>
                        <text x="22.5" y="38" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="22" fill="#C9A84C" font-weight="700">D&amp;Z</text>
                        <line x1="18" y1="48" x2="27" y2="48" stroke="#C9A84C" stroke-width="1.5" stroke-dasharray="2,2"/>
                        <text x="48" y="30" font-family="Playfair Display, serif" font-size="24" fill="#FFFFFF" font-weight="700">SEALCOATING</text>
                        <text x="48" y="50" font-family="Inter, sans-serif" font-size="9" fill="#C9A84C" letter-spacing="4" font-weight="500">MISSISSIPPI</text>
                        <line x1="48" y1="55" x2="185" y2="55" stroke="#C9A84C" stroke-width="0.5"/>
                        <text x="48" y="64" font-family="Inter, sans-serif" font-size="7" fill="#8A8A8A" letter-spacing="2">EST. 2020</text>
                    </svg>"""


def nav_html(current="/"):
    items = [("/", "Home")] + [(service_url(s["slug"]), s["nav"]) for s in SERVICES] + [
        ("/service-areas/", "Service Areas"), ("/#contact", "Contact")]
    links = []
    for href, label in items:
        active = href == current or (href == "/service-areas/" and current.startswith("/service-areas/"))
        attr = ' class="active" aria-current="page"' if active and href == current else (' class="active"' if active else "")
        links.append(f'                <li><a href="{href}"{attr}>{label}</a></li>')
    links.append(f'                <li><a href="{QUOTE_URL}" target="_blank" rel="noopener" class="nav-cta">Free Quote</a></li>')
    return f"""    <a class="skip-link" href="#main">Skip to content</a>
    <div class="top-bar">
        <div class="container top-bar-inner">
            <div class="top-bar-left">
                <span class="badge">&#9733; Veteran Owned &amp; Operated</span>
                <span class="separator">|</span>
                <span>Serving North Mississippi from Ripley, MS</span>
            </div>
            <div class="top-bar-right">
                <a href="tel:{TEL}"><span class="icon" aria-hidden="true">&#9742;</span> {PHONE}</a>
                <a href="mailto:{EMAIL}"><span class="icon" aria-hidden="true">&#9993;</span> {EMAIL}</a>
            </div>
        </div>
    </div>

    <nav class="navbar" id="navbar" aria-label="Main">
        <div class="container nav-inner">
            <a href="/" class="logo" aria-label="Mississippi Sealcoating home">
                <div class="logo-mark">
                    {LOGO_SVG}
                </div>
            </a>
            <button class="nav-toggle" id="navToggle" aria-label="Toggle navigation" aria-controls="navLinks" aria-expanded="false">
                <span></span><span></span><span></span>
            </button>
            <ul class="nav-links" id="navLinks">
{chr(10).join(links)}
            </ul>
        </div>
    </nav>
"""


def footer_html():
    svc = "\n".join(f'                        <li><a href="{service_url(s["slug"])}">{s["name"]}</a></li>' for s in SERVICES)
    cities = "\n".join(f'                        <li><a href="{city_url(k)}">{c["name"]}, MS</a></li>'
                       for k, c in CITIES.items() if c.get("featured"))
    counties = "\n".join(f'                        <li><a href="{county_url(k)}">{COUNTIES[k]["name"]} County</a></li>'
                         for k in FEATURED_COUNTIES)
    return f"""    <footer class="footer">
        <div class="container">
            <div class="footer-grid">
                <div class="footer-brand">
                    <svg viewBox="0 0 200 70" xmlns="http://www.w3.org/2000/svg" class="footer-logo" role="img" aria-label="D&amp;Z Sealcoating">
                        <path d="M10 8 L35 2 L35 42 Q35 58 22.5 65 Q10 58 10 42 Z" fill="none" stroke="#C9A84C" stroke-width="2"/>
                        <text x="22.5" y="38" text-anchor="middle" font-family="Bebas Neue, sans-serif" font-size="22" fill="#C9A84C" font-weight="700">D&amp;Z</text>
                        <line x1="18" y1="48" x2="27" y2="48" stroke="#C9A84C" stroke-width="1.5" stroke-dasharray="2,2"/>
                        <text x="48" y="30" font-family="Playfair Display, serif" font-size="20" fill="#FFFFFF" font-weight="700">SEALCOATING</text>
                        <text x="48" y="48" font-family="Inter, sans-serif" font-size="8" fill="#C9A84C" letter-spacing="3">MISSISSIPPI</text>
                    </svg>
                    <p>Veteran-owned asphalt sealcoating, asphalt repair and parking lot sealing company based in Ripley, MS and serving North Mississippi since 2020.</p>
                    <a href="{QUOTE_URL}" target="_blank" rel="noopener" class="btn btn-gold btn-sm footer-cta">Get a Free Quote &rarr;</a>
                </div>
                <div class="footer-links">
                    <h4>Services</h4>
                    <ul>
{svc}
                        <li><a href="/#process">Our Process</a></li>
                    </ul>
                </div>
                <div class="footer-links">
                    <h4>Popular Cities</h4>
                    <ul>
{cities}
                        <li><a href="/service-areas/">All Service Areas</a></li>
                    </ul>
                </div>
                <div class="footer-links">
                    <h4>Counties</h4>
                    <ul>
{counties}
                    </ul>
                </div>
                <div class="footer-contact">
                    <h4>Contact</h4>
                    <ul>
                        <li><a href="tel:{TEL}">{PHONE}</a></li>
                        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
                        <li>Ripley, MS 38663</li>
                        <li>Mon&ndash;Sat: 7AM &ndash; 6PM</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; <span data-year>{date.today().year}</span> D&amp;Z Sealcoating, LLC &middot; Veteran-owned asphalt sealcoating, repair &amp; parking lot sealing in North Mississippi</p>
            </div>
        </div>
    </footer>

    <div class="mobile-cta-bar" aria-label="Quick contact">
        <a href="tel:{TEL}" class="mobile-cta-call">&#9742; Call Now</a>
        <a href="{QUOTE_URL}" target="_blank" rel="noopener" class="mobile-cta-quote">Free Quote &rarr;</a>
    </div>
"""


def page_end():
    return """
    <script src="/script.js" defer></script>
</body>
</html>
"""


def breadcrumb_html(crumbs):
    parts = []
    for i, (name, url) in enumerate(crumbs):
        if i == len(crumbs) - 1:
            parts.append(f'<li aria-current="page">{name}</li>')
        else:
            parts.append(f'<li><a href="{url}">{name}</a></li>')
    return f'<nav class="breadcrumb" aria-label="Breadcrumb"><ol>{"".join(parts)}</ol></nav>'


def page_hero(crumbs, tag, h1, sub, cta_label="Get Your Free Estimate"):
    return f"""    <header class="page-hero">
        <div class="container">
            {breadcrumb_html(crumbs)}
            <span class="hero-badge">{tag}</span>
            <h1>{h1}</h1>
            <p class="hero-sub">{sub}</p>
            <div class="hero-btns">
                <a href="{QUOTE_URL}" target="_blank" rel="noopener" class="btn btn-gold btn-lg">{cta_label} &rarr;</a>
                <a href="tel:{TEL}" class="btn btn-outline btn-lg">Call {PHONE}</a>
            </div>
            <ul class="trust-row">
                <li>&#9733; Veteran owned</li>
                <li>&#10003; Licensed &amp; insured</li>
                <li>&#10003; Free, no-obligation estimates</li>
            </ul>
        </div>
    </header>
"""


def cta_banner(title, text, label="Request a Free Quote"):
    return f"""    <section class="cta-banner cta-banner-2">
        <div class="container cta-inner">
            <div class="cta-text">
                <h2>{title}</h2>
                <p>{text}</p>
            </div>
            <a href="{QUOTE_URL}" target="_blank" rel="noopener" class="btn btn-gold btn-lg">{label} &rarr;</a>
        </div>
    </section>
"""


def final_cta(title, text):
    return f"""    <section class="cta-banner cta-banner-5">
        <div class="container">
            <div class="cta-centered">
                <h2>{title}</h2>
                <p>{text}</p>
                <div class="cta-btns">
                    <a href="{QUOTE_URL}" target="_blank" rel="noopener" class="btn btn-gold btn-xl">Get Your Free Estimate Now</a>
                </div>
                <p class="cta-sub">Or call us directly: <a href="tel:{TEL}"><strong>{PHONE}</strong></a></p>
            </div>
        </div>
    </section>
"""


def faq_html(faqs, heading):
    items = "\n".join(
        f"""                <details class="faq-item">
                    <summary>{q}</summary>
                    <div class="faq-answer"><p>{a}</p></div>
                </details>""" for q, a in faqs)
    return f"""    <section class="section faq">
        <div class="container narrow">
            <div class="section-header">
                <span class="section-tag">FAQ</span>
                <h2>{heading}</h2>
                <div class="section-line"></div>
            </div>
            <div class="faq-list">
{items}
            </div>
        </div>
    </section>
"""


SERVICE_ICONS = {
    "asphalt-sealcoating": '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><rect x="8" y="40" width="48" height="8" rx="2" stroke="#C9A84C" stroke-width="2"/><path d="M16 40V28a2 2 0 012-2h28a2 2 0 012 2v12" stroke="#C9A84C" stroke-width="2"/><path d="M24 26V20M32 26V16M40 26V20" stroke="#C9A84C" stroke-width="2" stroke-linecap="round"/><line x1="8" y1="52" x2="56" y2="52" stroke="#C9A84C" stroke-width="2" stroke-dasharray="4,3"/></svg>',
    "asphalt-repair": '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><ellipse cx="32" cy="44" rx="20" ry="6" stroke="#C9A84C" stroke-width="2"/><path d="M12 44V36c0-4 9-8 20-8s20 4 20 8v8" stroke="#C9A84C" stroke-width="2"/><path d="M32 16V28M26 22L32 16L38 22" stroke="#C9A84C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "asphalt-driveways": '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><path d="M32 8L10 24H54L32 8Z" stroke="#C9A84C" stroke-width="2" stroke-linejoin="round"/><rect x="16" y="24" width="32" height="18" stroke="#C9A84C" stroke-width="2"/><path d="M27 42L20 58H44L37 42" stroke="#C9A84C" stroke-width="2"/><line x1="32" y1="44" x2="32" y2="57" stroke="#C9A84C" stroke-width="1.5" stroke-dasharray="3,3"/></svg>',
    "parking-lot-sealing": '<svg viewBox="0 0 64 64" fill="none" aria-hidden="true"><rect x="8" y="16" width="48" height="36" rx="2" stroke="#C9A84C" stroke-width="2"/><path d="M20 16V34M32 16V34M44 16V34" stroke="#C9A84C" stroke-width="2"/><text x="32" y="47" text-anchor="middle" font-size="10" fill="#C9A84C" font-family="Inter">P</text></svg>',
}


def service_cards(place):
    cards = []
    for s in SERVICES:
        cards.append(f"""                <div class="service-card">
                    <div class="service-icon">{SERVICE_ICONS[s['slug']]}</div>
                    <h3>{s['name']} in {place}</h3>
                    <p>{s['card'].format(place=place)}</p>
                    <a href="{service_url(s['slug'])}" class="service-link">{s['link_text']} details &rarr;</a>
                </div>""")
    return "\n".join(cards)


def link_chips(items):
    return "\n".join(f'                <li><a href="{u}">{n}</a></li>' for n, u in items)


# ---------------------------------------------------------------------------
# Location pages
# ---------------------------------------------------------------------------
INTRO_VARIANTS = [
    "Whether you need a cracked driveway brought back to life, potholes patched before they spread, or a commercial lot sealed and restriped, D&amp;Z Sealcoating brings veteran-owned workmanship and commercial-grade materials to every job in {place}.",
    "Asphalt is one of the biggest investments on any property, and in {place} it takes a beating from summer heat, heavy rain and daily traffic. Our veteran-owned crew keeps driveways and parking lots protected with professional sealcoating, crack sealing and pothole repair.",
    "From single-family driveways to large commercial parking lots, property owners in {place} call D&amp;Z Sealcoating when they want asphalt work done right the first time &mdash; clean edges, even coverage and honest pricing.",
]

WEATHER = "North Mississippi averages well over 50 inches of rain a year, and summer sun pushes pavement temperatures far past what you feel in the air. Add winter freeze&ndash;thaw cycles and you get oxidized, brittle asphalt that cracks, lets water into the base and eventually fails. A professional sealcoat and timely crack repair stop that cycle before it costs you a full replacement."


def location_faqs(place, county_label, nearby):
    near = ", ".join(nearby[:5]) if nearby else "the surrounding communities"
    return [
        (f"How much does asphalt sealcoating cost in {place}, MS?",
         f"Pricing depends on the square footage, the condition of the asphalt and how much crack or pothole repair is needed first. Most residential driveways in {place} cost far less to seal than to replace. We provide free, no-obligation estimates &mdash; request yours at dandzsealcoating.com or call {PHONE}."),
        (f"When is the best time to sealcoat a driveway or parking lot in {place}?",
         "In North Mississippi the sealcoating season typically runs from late spring through early fall, when temperatures stay above about 50&deg;F and there's no rain in the forecast for at least 24 hours. Spring and summer book up quickly, so it pays to get on the schedule early."),
        (f"Do you do asphalt repair and parking lot sealing in {county_label}?",
         f"Yes. We provide asphalt sealcoating, hot-pour crack sealing, pothole repair, driveway restoration, parking lot sealing and line striping throughout {county_label}, for homeowners, businesses, churches, schools and HOAs."),
        (f"How often should asphalt be sealcoated in {place}?",
         "Most driveways and parking lots should be sealcoated every two to three years, with cracks sealed as soon as they appear. New asphalt should cure for roughly 6&ndash;12 months before its first sealcoat."),
        (f"Do you serve areas near {place}?",
         f"Absolutely. In addition to {place}, we regularly work in {near} and communities across North Mississippi."),
    ]


def photo_block(i, place):
    src, alt = PHOTOS[i % len(PHOTOS)]
    return f'<figure class="page-img"><img src="{src}" alt="{alt} &ndash; D&amp;Z Sealcoating, serving {place}" loading="lazy" decoding="async" width="800" height="500"></figure>'


def location_page(kind, key, idx):
    if kind == "city":
        c = CITIES[key]
        county = COUNTIES[c["county"]]
        place = c["name"]
        place_full = f"{place}, MS"
        county_label = f"{county['name']} County"
        path = city_url(key)
        crumbs = [("Home", "/"), ("Service Areas", "/service-areas/"),
                  (f"{county_label}", county_url(c["county"])), (place_full, path)]
        region = REGIONS[county["region"]]
        blurb = c["blurb"]
        # Related: other cities in the county, then cities in neighboring counties
        related = [k for k in cities_in(c["county"]) if k != key]
        for n in county["neighbors"]:
            related += [k for k in cities_in(n) if k not in related and k != key]
        related = related[:8]
        nearby_names = [CITIES[k]["name"] for k in related] or county["towns"]
        extra_towns = [t for t in county["towns"] if t != place and t not in [CITIES[k]["name"] for k in CITIES]]
        area_type = {"@type": "City", "name": place_full,
                     "containedInPlace": {"@type": "AdministrativeArea", "name": f"{county_label}, MS"}}
        title = f"Asphalt Sealcoating &amp; Repair in {place}, MS | Driveways &amp; Parking Lots"
        desc = (f"Asphalt sealcoating, asphalt repair, driveway sealing and parking lot sealing in {place}, MS "
                f"({county_label}). Veteran-owned D&amp;Z Sealcoating. Free estimates &ndash; call {PHONE}.")
        h1 = f"Asphalt Sealcoating &amp; Repair in <span class=\"text-gold\">{place}, MS</span>"
        sub = f"Asphalt driveways, crack &amp; pothole repair, sealcoating and parking lot sealing for homes and businesses in {place} and across {county_label}."
        tag = f"{county_label} &middot; North Mississippi"
    else:
        county = COUNTIES[key]
        place = f"{county['name']} County"
        place_full = f"{place}, MS"
        county_label = place
        path = county_url(key)
        crumbs = [("Home", "/"), ("Service Areas", "/service-areas/"), (place_full, path)]
        region = REGIONS[county["region"]]
        blurb = county["blurb"]
        related = cities_in(key)
        for n in county["neighbors"]:
            related += [k for k in cities_in(n) if k not in related]
        related = related[:8]
        nearby_names = county["towns"]
        extra_towns = [t for t in county["towns"] if t not in [CITIES[k]["name"] for k in cities_in(key)]]
        area_type = {"@type": "AdministrativeArea", "name": place_full}
        title = f"{place}, MS Asphalt Sealcoating, Repair &amp; Parking Lot Sealing"
        desc = (f"Asphalt sealcoating, asphalt repair, driveway sealing and parking lot sealing across {place}, MS "
                f"&ndash; {', '.join(county['towns'][:3])} and more. Veteran owned. Call {PHONE}.")
        h1 = f"<span class=\"text-gold\">{place}</span> Asphalt Sealcoating, Repair &amp; Parking Lot Sealing"
        seat_word = "county seats" if " and " in county["seat"] else "county seat"
        sub = f"Serving {county['seat']} ({seat_word}) and every community in {place} with professional asphalt driveway, repair, sealcoating and parking lot services."
        tag = f"{region['name']}"

    faqs = location_faqs(place, county_label, nearby_names)
    graph = [
        business_schema(),
        {"@type": "Service", "@id": SITE + path + "#service",
         "name": plain(f"Asphalt Sealcoating & Repair in {place_full}"),
         "serviceType": ["Asphalt sealcoating", "Asphalt repair", "Asphalt driveway sealing", "Parking lot sealing",
                         "Crack sealing", "Pothole repair", "Line striping"],
         "provider": {"@id": BIZ_ID}, "areaServed": area_type, "url": SITE + path},
        breadcrumb_schema(crumbs),
        faq_schema(faqs),
    ]

    # Links: county / cities in county / neighboring counties
    link_items = []
    if kind == "city":
        link_items.append((f"{county_label} (all towns)", county_url(CITIES[key]["county"])))
    link_items += [(f"{CITIES[k]['name']}, MS", city_url(k)) for k in related]
    neighbor_links = [(f"{COUNTIES[n]['name']} County", county_url(n)) for n in county["neighbors"]]

    towns_line = ""
    if extra_towns:
        towns_line = f"<p>We also serve {', '.join(extra_towns[:-1]) + (' and ' if len(extra_towns) > 1 else '') + extra_towns[-1]}{' and the rest of ' + county_label if kind == 'city' else ''}.</p>"

    city_list = ""
    if kind == "county" and cities_in(key):
        chips = link_chips([(f"{CITIES[k]['name']}, MS", city_url(k)) for k in cities_in(key)])
        city_list = f"""                    <h3>Cities we serve in {place}</h3>
                    <ul class="link-chips">
{chips}
                    </ul>"""

    html = head(title, desc, path, graph, geo_place=f"{place}, Mississippi")
    html += nav_html(path)
    html += '    <main id="main">\n'
    html += page_hero(crumbs, tag, h1, sub)
    html += f"""
    <section class="section intro-section">
        <div class="container">
            <div class="split-section">
                <div class="split-content prose">
                    <span class="section-tag">Local Asphalt Experts</span>
                    <h2>Trusted Asphalt Contractor for {place_full}</h2>
                    <p class="lead">{blurb}</p>
                    <p>{INTRO_VARIANTS[idx % len(INTRO_VARIANTS)].format(place=place)}</p>
                    {towns_line}
{city_list}
                    <a href="{QUOTE_URL}" target="_blank" rel="noopener" class="btn btn-gold">Get a Free {place} Estimate &rarr;</a>
                </div>
                <div class="split-image">
                    {photo_block(idx, place_full)}
                </div>
            </div>
        </div>
    </section>

    <section class="section services">
        <div class="container">
            <div class="section-header">
                <span class="section-tag">Our Services in {place}</span>
                <h2>Asphalt Driveways, Repair, Sealcoating &amp; <span class="text-gold">Parking Lot Sealing</span></h2>
                <div class="section-line"></div>
            </div>
            <div class="services-grid">
{service_cards(place)}
            </div>
        </div>
    </section>

"""
    html += cta_banner(f"Need Asphalt Work in {place}?",
                       f"Get a fast, free estimate for sealcoating, asphalt repair or parking lot sealing in {place_full}.")
    html += f"""
    <section class="section why-local">
        <div class="container">
            <div class="two-col">
                <div class="prose">
                    <span class="section-tag">{region['name']}</span>
                    <h2>{region['heading']}</h2>
                    <p>{region['text']}</p>
                    <p>{WEATHER}</p>
                </div>
                <div class="checklist-card">
                    <h3>What's included with every {place} job</h3>
                    <ul class="service-list">
                        <li>Free on-site inspection &amp; written estimate</li>
                        <li>Power cleaning, edging &amp; oil-spot treatment</li>
                        <li>Hot-pour rubberized crack sealing</li>
                        <li>Pothole &amp; soft-spot patching</li>
                        <li>Two coats of commercial-grade sealer</li>
                        <li>Line striping &amp; ADA markings for lots</li>
                        <li>Barricades &amp; clear cure-time guidance</li>
                    </ul>
                    <a href="{QUOTE_URL}" target="_blank" rel="noopener" class="btn btn-gold btn-block">Schedule Your Estimate</a>
                </div>
            </div>
        </div>
    </section>

"""
    html += faq_html(faqs, f"Asphalt Questions from <span class=\"text-gold\">{place}</span> Property Owners")
    html += f"""
    <section class="section nearby">
        <div class="container">
            <div class="section-header">
                <span class="section-tag">Nearby Service Areas</span>
                <h2>Also Serving Communities Near {place}</h2>
                <div class="section-line"></div>
            </div>
            <ul class="link-chips center">
{link_chips(link_items)}
            </ul>
            <h3 class="chips-heading">Neighboring counties</h3>
            <ul class="link-chips center">
{link_chips(neighbor_links)}
                <li><a href="/service-areas/">All North Mississippi service areas</a></li>
            </ul>
        </div>
    </section>

"""
    html += final_cta(f"Ready to Protect Your {place} Asphalt?",
                      "Veteran owned, fully insured and proud to serve North Mississippi. Get your free, no-obligation estimate today.")
    html += "    </main>\n\n"
    html += footer_html()
    html += page_end()
    return path, html


# ---------------------------------------------------------------------------
# Service pages
# ---------------------------------------------------------------------------
SERVICE_CONTENT = {
    "asphalt-sealcoating": {
        "title": "Asphalt Sealcoating in North Mississippi | Driveways &amp; Parking Lots | D&amp;Z",
        "desc": f"Professional asphalt sealcoating for driveways and parking lots in North Mississippi &ndash; Ripley, Corinth, Tupelo, Oxford, Southaven &amp; more. Veteran owned. Free estimates: {PHONE}.",
        "h1": "Asphalt Sealcoating in <span class=\"text-gold\">North Mississippi</span>",
        "sub": "Commercial-grade sealcoating that protects driveways and parking lots from sun, rain and oil &mdash; and makes them look brand new.",
        "body": """
                    <h2>Why Asphalt Sealcoating Matters in Mississippi</h2>
                    <p>Asphalt is held together by a petroleum-based binder. Sun, rain, and chemicals such as oil and gasoline slowly break that binder down &mdash; the surface turns gray, becomes brittle and starts to crack. Once water gets through those cracks it softens the base underneath, and that's when potholes and crumbling edges show up.</p>
                    <p>A professional <strong>asphalt sealcoating</strong> puts a protective layer over the pavement that blocks UV rays, sheds water, resists oil and fuel, and restores a deep black finish. It's the single most cost-effective way to extend the life of a driveway or parking lot.</p>
                    <h3>Our Sealcoating Process</h3>
                    <ol class="steps-list">
                        <li><strong>Inspection &amp; estimate.</strong> We measure the area, note every crack and soft spot, and give you a clear written price.</li>
                        <li><strong>Cleaning &amp; prep.</strong> Blowing and sweeping, edging back grass, and treating oil spots so the sealer bonds.</li>
                        <li><strong>Repairs first.</strong> Cracks are filled with hot-pour rubberized sealant and potholes are patched &mdash; see <a href="/asphalt-repair/">asphalt repair</a>.</li>
                        <li><strong>Two coats of sealer.</strong> Commercial-grade sealer applied edge to edge for uniform coverage and a rich black finish.</li>
                        <li><strong>Cure &amp; reopen.</strong> We barricade the area and tell you exactly when it's ready for traffic &mdash; typically 24&ndash;48 hours.</li>
                    </ol>
                    <h3>How Often Should You Sealcoat?</h3>
                    <p>For most North Mississippi driveways and parking lots, every <strong>two to three years</strong> is the sweet spot. High-traffic commercial lots may benefit from a shorter cycle. Brand-new asphalt should cure for about 6&ndash;12 months before its first coat.</p>
                    <h3>Sealcoating for Homes and Businesses</h3>
                    <p>We sealcoat <a href="/asphalt-driveways/">residential asphalt driveways</a> of every size &mdash; from short in-town drives to long rural driveways &mdash; as well as <a href="/parking-lot-sealing/">commercial parking lots</a> for retail centers, churches, schools, apartment communities and industrial sites.</p>
""",
        "faqs": [
            ("What is asphalt sealcoating?", "Sealcoating is a protective liquid coating applied over asphalt pavement. It blocks UV damage, repels water, oil and gasoline, and restores the pavement's black color, extending its useful life."),
            ("How long does sealcoating last?", "A quality sealcoat typically lasts two to three years on driveways and one to three years on busy parking lots, depending on traffic and weather."),
            ("How long before I can drive on a freshly sealcoated surface?", "Foot traffic is usually fine after several hours, and vehicles can return in about 24&ndash;48 hours depending on temperature and humidity. We'll give you specific guidance for your job."),
            ("Is sealcoating worth it?", "Yes. Sealcoating costs a small fraction of repaving and, done regularly with crack repair, can add many years to the life of your asphalt."),
        ],
    },
    "asphalt-repair": {
        "title": "Asphalt Repair in North Mississippi | Crack Sealing &amp; Pothole Repair | D&amp;Z",
        "desc": f"Asphalt repair in North Mississippi: hot-pour crack sealing, pothole patching and edge repair for driveways and parking lots in Ripley, Corinth, Tupelo, Oxford &amp; more. Call {PHONE}.",
        "h1": "Asphalt Repair: Crack Sealing &amp; <span class=\"text-gold\">Pothole Repair</span>",
        "sub": "Stop small cracks from becoming big, expensive failures. Professional asphalt repair for driveways, parking lots and private roads across North Mississippi.",
        "body": """
                    <h2>Fix It Now, Save Thousands Later</h2>
                    <p>Every crack in your asphalt is an open door for water. In North Mississippi's heavy rains, that water soaks into the base, and each freeze&ndash;thaw cycle or heavy vehicle pushes the damage further. What starts as a hairline crack becomes alligator cracking, then a pothole. Timely <strong>asphalt repair</strong> stops the cycle at a fraction of the cost of replacement.</p>
                    <h3>Hot-Pour Crack Sealing</h3>
                    <p>We clean out each crack and fill it with a hot-applied, rubberized sealant that stays flexible through summer heat and winter cold. It bonds to the crack walls, keeps water out and moves with the pavement instead of popping loose like cheap pour-in fillers.</p>
                    <h3>Pothole Repair &amp; Patching</h3>
                    <p>Potholes are a safety hazard and a liability, especially on commercial property. We remove loose material, square up the edges, and patch with asphalt compacted in lifts so the repair is level, solid and built to handle traffic.</p>
                    <h3>Edge &amp; Surface Repairs</h3>
                    <p>Crumbling driveway edges, low spots that hold water and areas of alligator cracking all get assessed honestly. If an area needs more than a surface repair, we'll tell you &mdash; no upselling, just straight answers.</p>
                    <h3>Finish with Sealcoating</h3>
                    <p>Repairs are the foundation of a lasting sealcoat. Most customers pair crack sealing and patching with <a href="/asphalt-sealcoating/">asphalt sealcoating</a> for a uniform, fully protected surface &mdash; whether it's a <a href="/asphalt-driveways/">home driveway</a> or a <a href="/parking-lot-sealing/">commercial parking lot</a>.</p>
""",
        "faqs": [
            ("Can cracked asphalt be repaired instead of replaced?", "In most cases, yes. Cracks and isolated potholes can be sealed and patched for far less than replacement. We'll only recommend bigger work when the base has truly failed."),
            ("What's the best way to seal asphalt cracks?", "Hot-pour rubberized crack sealant is the professional standard. It stays flexible in heat and cold and bonds to the crack, which makes it last much longer than cold-pour fillers."),
            ("How soon should I repair a pothole?", "As soon as possible. Water and traffic enlarge potholes quickly, and on commercial property they create trip and vehicle-damage liability."),
            ("Do you repair asphalt for businesses and HOAs?", "Yes. We repair parking lots, private roads and common areas for businesses, churches, schools, apartment communities and HOAs across North Mississippi."),
        ],
    },
    "asphalt-driveways": {
        "title": "Asphalt Driveway Sealing &amp; Repair in North Mississippi | D&amp;Z Sealcoating",
        "desc": f"Asphalt driveway sealcoating, crack repair and restoration in North Mississippi &ndash; Ripley, Corinth, Booneville, Pontotoc, Oxford, Tupelo, Southaven &amp; more. Veteran owned. Call {PHONE}.",
        "h1": "Asphalt Driveways: Sealing, Repair &amp; <span class=\"text-gold\">Restoration</span>",
        "sub": "Give your home's asphalt driveway a rich, jet-black finish and years of extra life with professional driveway sealcoating and repair.",
        "body": """
                    <h2>Your Driveway Is Your Home's First Impression</h2>
                    <p>A faded, cracked driveway drags down the look of an otherwise beautiful home. A freshly sealed <strong>asphalt driveway</strong> does the opposite &mdash; it adds instant curb appeal and helps protect your property value, whether you're staying for decades or getting ready to sell.</p>
                    <h3>Complete Driveway Care</h3>
                    <ul class="service-list">
                        <li><strong>Driveway sealcoating</strong> &ndash; two coats of commercial-grade sealer for a uniform black finish (<a href="/asphalt-sealcoating/">learn about sealcoating</a>)</li>
                        <li><strong>Crack sealing</strong> &ndash; hot-pour rubberized sealant that keeps water out of the base</li>
                        <li><strong>Pothole &amp; edge repair</strong> &ndash; patching crumbling edges and soft spots (<a href="/asphalt-repair/">learn about asphalt repair</a>)</li>
                        <li><strong>Oil-stain treatment</strong> &ndash; priming stains so the sealer bonds properly</li>
                        <li><strong>Clean edging</strong> &ndash; crisp lines along lawns, sidewalks and garage aprons</li>
                    </ul>
                    <h3>Built for Mississippi Driveways</h3>
                    <p>From short in-town driveways to long, sloped rural drives in the hills of North Mississippi, we've seen it all. Steep grades and long runs shed a lot of water, so we pay special attention to cracks and edges where runoff does the most damage.</p>
                    <h3>Protect Your Investment</h3>
                    <p>Replacing an asphalt driveway can cost thousands. Sealcoating every two to three years &mdash; with cracks sealed as they appear &mdash; is the most affordable way to get the longest possible life out of the driveway you already have.</p>
                    <h3>Homeowner Tips After Sealing</h3>
                    <p>Keep vehicles off for 24&ndash;48 hours, avoid sharp turns with the steering wheel while parked for the first few weeks in hot weather, and keep sprinklers off the surface until the sealer has fully cured. We'll walk you through everything when we finish.</p>
""",
        "faqs": [
            ("How often should I seal my asphalt driveway?", "Every two to three years for most homes. If your driveway looks gray and you can see the stones in the surface, it's time."),
            ("How long does driveway sealcoating take?", "Most residential driveways are cleaned, repaired and sealed in a single day. You'll then need to stay off the surface for about 24&ndash;48 hours while it cures."),
            ("Can you fix cracks in my driveway before sealing?", "Yes &mdash; and we recommend it. We seal cracks with hot-pour rubberized sealant and patch potholes before sealcoating so the finished surface lasts."),
            ("Do you work on long rural driveways?", "Absolutely. We regularly seal and repair long country driveways throughout North Mississippi, including steep and sloped drives."),
        ],
    },
    "parking-lot-sealing": {
        "title": "Parking Lot Sealing &amp; Striping in North Mississippi | Commercial Sealcoating | D&amp;Z",
        "desc": f"Commercial parking lot sealing, sealcoating, crack repair and line striping in North Mississippi &ndash; Tupelo, Oxford, Corinth, Southaven, DeSoto County &amp; more. Call {PHONE}.",
        "h1": "Parking Lot Sealing &amp; <span class=\"text-gold\">Line Striping</span>",
        "sub": "Commercial parking lot sealcoating, crack repair and striping that keeps your lot safe, compliant and looking professional.",
        "body": """
                    <h2>Your Parking Lot Is Your Front Door</h2>
                    <p>Customers, tenants and employees see your parking lot before they ever walk inside. Faded, cracked asphalt sends the wrong message and creates real liability. Professional <strong>parking lot sealing</strong> keeps your property sharp and dramatically extends the life of one of your biggest capital investments.</p>
                    <h3>Commercial Services</h3>
                    <ul class="service-list">
                        <li><strong>Parking lot sealcoating</strong> &ndash; commercial-grade sealer applied for heavy traffic (<a href="/asphalt-sealcoating/">about sealcoating</a>)</li>
                        <li><strong>Crack sealing &amp; pothole repair</strong> &ndash; eliminate trip hazards and stop water damage (<a href="/asphalt-repair/">about asphalt repair</a>)</li>
                        <li><strong>Line striping</strong> &ndash; crisp stall lines, arrows, fire lanes and crosswalks</li>
                        <li><strong>ADA markings</strong> &ndash; accessible stalls, access aisles and symbols</li>
                        <li><strong>Ongoing maintenance plans</strong> &ndash; scheduled inspections and resealing to budget ahead</li>
                    </ul>
                    <h3>Minimal Disruption to Your Business</h3>
                    <p>We plan every commercial job around your hours. Larger lots can often be completed in sections so part of the lot stays open, and we coordinate barricades and signage so customers know exactly where to park.</p>
                    <h3>Who We Work With</h3>
                    <p>Retail centers, restaurants, medical offices, churches, schools, apartment and HOA communities, warehouses and industrial sites, and municipal properties across North Mississippi &mdash; from Tupelo and Corinth to Oxford and the DeSoto County suburbs.</p>
                    <h3>Protect Your Budget</h3>
                    <p>Sealcoating a parking lot every two to three years, with cracks sealed in between, can add many years to its life and costs a fraction of repaving. It's preventive maintenance that pays for itself.</p>
""",
        "faqs": [
            ("How often should a parking lot be sealcoated?", "Most commercial lots should be sealcoated every two to three years. High-traffic areas like drive lanes and entrances may need attention sooner."),
            ("Can you seal our lot without shutting down our business?", "In many cases, yes. We can work in phases and schedule around your peak hours so part of the lot stays open."),
            ("Do you restripe after sealcoating?", "Yes. Sealcoating covers existing lines, so we restripe stalls, arrows, fire lanes and ADA markings as part of the job."),
            ("Do you offer free estimates for commercial parking lots?", "Yes. We'll inspect your lot, measure it and provide a detailed written estimate at no cost."),
        ],
    },
}


def all_area_chips():
    return link_chips([(f"{c['name']}, MS", city_url(k)) for k, c in CITIES.items()])


def service_page(slug):
    s = SERVICE_BY_SLUG[slug]
    content = SERVICE_CONTENT[slug]
    path = service_url(slug)
    crumbs = [("Home", "/"), (s["name"], path)]
    graph = [
        business_schema(),
        {"@type": "Service", "@id": SITE + path + "#service", "name": s["name"], "serviceType": s["name"],
         "provider": {"@id": BIZ_ID}, "url": SITE + path,
         "areaServed": [{"@type": "AdministrativeArea", "name": f"{COUNTIES[c]['name']} County, MS"} for c in COUNTY_ORDER]},
        breadcrumb_schema(crumbs),
        faq_schema(content["faqs"]),
    ]
    others = "\n".join(
        f'                    <li><a href="{service_url(o["slug"])}">{o["name"]}</a></li>' for o in SERVICES if o["slug"] != slug)
    counties = link_chips([(f"{COUNTIES[k]['name']} County", county_url(k)) for k in COUNTY_ORDER])
    img_src, img_alt = PHOTOS[[x["slug"] for x in SERVICES].index(slug) % len(PHOTOS)]

    html = head(content["title"], content["desc"], path, graph)
    html += nav_html(path)
    html += '    <main id="main">\n'
    html += page_hero(crumbs, "North Mississippi &middot; Veteran Owned", content["h1"], content["sub"])
    html += f"""
    <section class="section">
        <div class="container">
            <div class="content-with-aside">
                <article class="prose">
{content['body']}
                    <a href="{QUOTE_URL}" target="_blank" rel="noopener" class="btn btn-gold">Get a Free {s['name']} Quote &rarr;</a>
                </article>
                <aside class="aside">
                    <figure class="page-img"><img src="{img_src}" alt="{img_alt}" loading="lazy" decoding="async" width="800" height="500"></figure>
                    <div class="checklist-card">
                        <h3>Free Estimate</h3>
                        <p>Tell us about your project and get a no-obligation quote.</p>
                        <a href="{QUOTE_URL}" target="_blank" rel="noopener" class="btn btn-gold btn-block">Request a Quote</a>
                        <a href="tel:{TEL}" class="btn btn-outline btn-block">Call {PHONE}</a>
                    </div>
                    <div class="checklist-card">
                        <h3>Related Services</h3>
                        <ul class="aside-links">
{others}
                    <li><a href="/service-areas/">Service areas</a></li>
                        </ul>
                    </div>
                </aside>
            </div>
        </div>
    </section>

"""
    html += cta_banner(f"Get {s['name']} on the Schedule",
                       "Spring and summer fill up fast across North Mississippi. Lock in your date today.",
                       "Reserve Your Date")
    html += faq_html(content["faqs"], f"{s['name']} <span class=\"text-gold\">FAQ</span>")
    html += f"""
    <section class="section nearby">
        <div class="container">
            <div class="section-header">
                <span class="section-tag">Service Areas</span>
                <h2>{s['name']} Near You in <span class="text-gold">North Mississippi</span></h2>
                <div class="section-line"></div>
                <p class="section-desc">Based in Ripley, we provide {s['name'].lower()} throughout these North Mississippi cities and counties.</p>
            </div>
            <ul class="link-chips center">
{all_area_chips()}
            </ul>
            <h3 class="chips-heading">Counties</h3>
            <ul class="link-chips center">
{counties}
            </ul>
        </div>
    </section>

"""
    html += final_cta(f"Ready for Professional {s['name']}?",
                      "Veteran owned, fully insured and proud to serve North Mississippi. Get your free, no-obligation estimate today.")
    html += "    </main>\n\n"
    html += footer_html()
    html += page_end()
    return path, html


# ---------------------------------------------------------------------------
# Service area hub + homepage areas block
# ---------------------------------------------------------------------------
def region_cards(detailed=False):
    cards = []
    for r in REGION_ORDER:
        counties = [c for c in COUNTY_ORDER if COUNTIES[c]["region"] == r]
        rows = []
        for c in counties:
            city_links = ", ".join(f'<a href="{city_url(k)}">{CITIES[k]["name"]}</a>' for k in cities_in(c))
            rows.append(f'                        <li><a href="{county_url(c)}"><strong>{COUNTIES[c]["name"]} County</strong></a>'
                        + (f'<span class="area-cities">{city_links}</span>' if city_links else "") + "</li>")
        extra = f'\n                    <p class="area-note">{REGIONS[r]["text"]}</p>' if detailed else ""
        cards.append(f"""                <div class="area-card">
                    <h3>{REGIONS[r]['name']}</h3>{extra}
                    <ul>
{chr(10).join(rows)}
                    </ul>
                </div>""")
    return "\n".join(cards)


def hub_page():
    path = "/service-areas/"
    crumbs = [("Home", "/"), ("Service Areas", path)]
    graph = [business_schema(), breadcrumb_schema(crumbs),
             {"@type": "ItemList", "name": "North Mississippi service areas",
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": f"{c['name']}, MS",
                                   "url": SITE + city_url(k)} for i, (k, c) in enumerate(CITIES.items())]}]
    title = "Service Areas | Asphalt Sealcoating &amp; Repair Across North Mississippi"
    desc = ("D&amp;Z Sealcoating serves North Mississippi: Ripley, Corinth, Booneville, Pontotoc, Oxford, Tupelo, Southaven "
            "and 19 counties including Tippah, Alcorn, Prentiss, Lee, Lafayette and DeSoto. Free estimates.")
    html = head(title, desc, path, graph)
    html += nav_html(path)
    html += '    <main id="main">\n'
    html += page_hero(crumbs, "Based in Ripley, MS", "North Mississippi <span class=\"text-gold\">Service Areas</span>",
                      "Asphalt driveways, asphalt repair, sealcoating and parking lot sealing in 19 North Mississippi counties &mdash; from Tippah and Alcorn to Lee, Lafayette and DeSoto.")
    html += f"""
    <section class="section service-areas">
        <div class="container">
            <div class="section-header">
                <span class="section-tag">Where We Work</span>
                <h2>Find Your <span class="text-gold">City or County</span></h2>
                <div class="section-line"></div>
                <p class="section-desc">Select your area for local details, services and answers to common questions. Don't see your town? We likely serve it &mdash; just ask.</p>
            </div>
            <div class="areas-grid areas-grid-detailed">
{region_cards(detailed=True)}
            </div>
        </div>
    </section>

    <section class="section services">
        <div class="container">
            <div class="section-header">
                <span class="section-tag">Services</span>
                <h2>What We Do Across <span class="text-gold">North Mississippi</span></h2>
                <div class="section-line"></div>
            </div>
            <div class="services-grid">
{service_cards("North Mississippi")}
            </div>
        </div>
    </section>

"""
    html += final_cta("Don't See Your Town Listed?",
                      "We travel throughout North Mississippi for driveway, repair, sealcoating and parking lot projects. Reach out for a free estimate.")
    html += "    </main>\n\n"
    html += footer_html()
    html += page_end()
    return path, html


def not_found_page():
    html = head("Page Not Found | Mississippi Sealcoating", "The page you're looking for couldn't be found.", "/404.html",
                [business_schema()]).replace('content="index, follow, max-image-preview:large"', 'content="noindex"')
    html += nav_html("")
    html += '    <main id="main">\n'
    html += page_hero([("Home", "/"), ("Page not found", "/404.html")], "404", "Page Not Found",
                      "Sorry, we couldn't find that page. Try one of our services or service areas below.")
    html += f"""
    <section class="section nearby">
        <div class="container">
            <ul class="link-chips center">
{link_chips([(s['name'], service_url(s['slug'])) for s in SERVICES] + [('Service Areas', '/service-areas/'), ('Home', '/')])}
            </ul>
        </div>
    </section>
    </main>

"""
    html += footer_html()
    html += page_end()
    return html


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def write(path, html):
    rel = path.strip("/")
    out = os.path.join(ROOT, rel, "index.html") if rel else os.path.join(ROOT, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)


def replace_block(text, name, content):
    pattern = re.compile(rf"(<!-- BUILD:{name} -->).*?([ \t]*<!-- /BUILD:{name} -->)", re.S)
    if not pattern.search(text):
        raise SystemExit(f"index.html is missing the BUILD:{name} markers")
    return pattern.sub(lambda m: m.group(1) + "\n" + content.rstrip("\n") + "\n" + m.group(2), text)


def update_index():
    p = os.path.join(ROOT, "index.html")
    with open(p, encoding="utf-8") as f:
        text = f.read()
    text = replace_block(text, "nav", nav_html("/"))
    text = replace_block(text, "areas", region_cards())
    text = replace_block(text, "footer", footer_html())
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    urls = [("/", "1.0", "weekly")]
    for s in SERVICES:
        path, html = service_page(s["slug"])
        write(path, html)
        urls.append((path, "0.9", "monthly"))

    path, html = hub_page()
    write(path, html)
    urls.append((path, "0.8", "monthly"))

    idx = 0
    for key in COUNTY_ORDER:
        path, html = location_page("county", key, idx)
        write(path, html)
        urls.append((path, "0.7", "monthly"))
        idx += 1
    for key in CITIES:
        path, html = location_page("city", key, idx)
        write(path, html)
        urls.append((path, "0.8" if CITIES[key].get("featured") else "0.7", "monthly"))
        idx += 1

    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8") as f:
        f.write(not_found_page())

    update_index()

    entries = "\n".join(
        f"  <url>\n    <loc>{SITE}{u}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
        f"    <changefreq>{freq}</changefreq>\n    <priority>{prio}</priority>\n  </url>"
        for u, prio, freq in urls)
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n'
                f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}\n</urlset>\n')

    print(f"Generated {len(urls) - 1} pages + 404 + sitemap ({len(urls)} URLs).")


if __name__ == "__main__":
    main()
