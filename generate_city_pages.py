#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de generation des pages de villes pour Seksitreffit Suomessa
Genere une page HTML optimisee SEO pour chaque ville de Finlande
"""

import json
import os
import re
from urllib.parse import quote
from datetime import datetime
import random

# Configuration
CTA_URL = "https://www.seksitreffitsuomessa.fi/offer"
OUTPUT_DIR = "villes"
REGIONS_FILE = "regions.json"

# Regions de Finlande avec leurs prefixes de code postal
REGIONS = {
    "Uusimaa": {
        "slug": "uusimaa",
        "prefixes": ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10"],
        "main_city": "Helsinki"
    },
    "Varsinais-Suomi": {
        "slug": "varsinais-suomi",
        "prefixes": ["20", "21", "22", "23", "24", "25", "26", "27"],
        "main_city": "Turku"
    },
    "Satakunta": {
        "slug": "satakunta",
        "prefixes": ["28", "29", "38"],
        "main_city": "Pori"
    },
    "Kanta-Hame": {
        "slug": "kanta-hame",
        "prefixes": ["11", "12", "13", "14", "30", "31"],
        "main_city": "Hameenlinna"
    },
    "Pirkanmaa": {
        "slug": "pirkanmaa",
        "prefixes": ["33", "34", "35", "36", "37", "39"],
        "main_city": "Tampere"
    },
    "Paijat-Hame": {
        "slug": "paijat-hame",
        "prefixes": ["15", "16", "17", "18", "19"],
        "main_city": "Lahti"
    },
    "Kymenlaakso": {
        "slug": "kymenlaakso",
        "prefixes": ["45", "46", "47", "48", "49"],
        "main_city": "Kouvola"
    },
    "Etela-Karjala": {
        "slug": "etela-karjala",
        "prefixes": ["53", "54", "55", "56"],
        "main_city": "Lappeenranta"
    },
    "Etela-Savo": {
        "slug": "etela-savo",
        "prefixes": ["50", "51", "52", "57", "58"],
        "main_city": "Mikkeli"
    },
    "Pohjois-Savo": {
        "slug": "pohjois-savo",
        "prefixes": ["70", "71", "72", "73", "74", "75", "76", "77", "78"],
        "main_city": "Kuopio"
    },
    "Pohjois-Karjala": {
        "slug": "pohjois-karjala",
        "prefixes": ["80", "81", "82", "83"],
        "main_city": "Joensuu"
    },
    "Keski-Suomi": {
        "slug": "keski-suomi",
        "prefixes": ["40", "41", "42", "43", "44"],
        "main_city": "Jyvaskyla"
    },
    "Etela-Pohjanmaa": {
        "slug": "etela-pohjanmaa",
        "prefixes": ["60", "61", "62", "63"],
        "main_city": "Seinajoki"
    },
    "Pohjanmaa": {
        "slug": "pohjanmaa",
        "prefixes": ["64", "65", "66", "67", "68"],
        "main_city": "Vaasa"
    },
    "Keski-Pohjanmaa": {
        "slug": "keski-pohjanmaa",
        "prefixes": ["67", "68", "69"],
        "main_city": "Kokkola"
    },
    "Pohjois-Pohjanmaa": {
        "slug": "pohjois-pohjanmaa",
        "prefixes": ["84", "85", "86", "90", "91", "92", "93"],
        "main_city": "Oulu"
    },
    "Kainuu": {
        "slug": "kainuu",
        "prefixes": ["87", "88", "89"],
        "main_city": "Kajaani"
    },
    "Lappi": {
        "slug": "lappi",
        "prefixes": ["94", "95", "96", "97", "98", "99"],
        "main_city": "Rovaniemi"
    },
    "Ahvenanmaa": {
        "slug": "ahvenanmaa",
        "prefixes": ["22"],
        "main_city": "Mariehamn"
    }
}

# FAQ templates en finnois
FAQ_TEMPLATES = [
    {
        "question": "Miten loydan seuraa kaupungissa {city}?",
        "answer": "Rekisteroidy palveluumme ilmaiseksi ja selaa paikallisia profiileja. Voit suodattaa hakutuloksia ian, kiinnostuksen kohteiden ja sijainnin mukaan. Laheta viesti kiinnostaville henkiloille ja aloita keskustelu."
    },
    {
        "question": "Onko palvelu turvallinen kayttaa?",
        "answer": "Kylla, turvallisuus on meille erittain tarkeaa. Kaikki profiilit tarkistetaan, ja tarjoamme tyokaluja epaasiallisenkaytoksen ilmoittamiseen. Henkilokohtaiset tietosi ovat aina suojattuja."
    },
    {
        "question": "Paljonko palvelu maksaa?",
        "answer": "Rekisteroityminen ja peruskaytto ovat ilmaisia. Voit selata profiileja ja lahettaa rajoitetun maaran viesteja ilmaiseksi. Premium-jasenyydellaavaat kaikki ominaisuudet."
    },
    {
        "question": "Kuinka monta jasentakaupungissa {city} on?",
        "answer": "Kaupungissa {city} on satoja aktiivisia jasenia. Maara kasvaa jatkuvasti, kun uusia kayttajia liittyy palveluun paivittain. Loyda oma kumppanisi jo tanaan!"
    },
    {
        "question": "Miten voin parantaa profiiliani?",
        "answer": "Lisaa selkea profiilikuva, kirjoita rehellinen ja kiinnostava kuvaus itsestasi, ja kerro harrastuksistasi. Aktiivisuus palvelussa ja nopea vastaaminen viesteihin parantavat nakyvyyttasi."
    }
]

# SEO intro templates
INTRO_TEMPLATES = [
    "Etsitkö aikuisten seuraa kaupungissa {city}? Olet oikeassa paikassa! {city} on tunnettu aktiivisesta sinkku-yhteisöstään, ja tuhannet paikalliset etsivät kumppania juuri nyt. Palvelumme tarjoaa turvallisen ja helpon tavan löytää seuraa omasta kaupungistasi.",
    "Tervetuloa {city}n suurimpaan aikuisten treffipalveluun! Täällä voit tutustua satoihin paikallisiin sinkkuihin, jotka etsivät samaa kuin sinä. {city} tarjoaa loistavan ympäristön uusiin tuttavuuksiin – aloita etsintä jo tänään!",
    "{city} on yksi Suomen aktiivisimmista seuranhakukaupungeista. Paikallinen yhteisömme kasvaa päivittäin, ja uusia mielenkiintoisia profiileja lisätään jatkuvasti. Liity mukaan ja löydä kumppanisi {city}sta!",
    "Haluatko tavata uusia ihmisiä kaupungissa {city}? Palvelumme yhdistää tuhansia suomalaisia sinkkuja, jotka etsivät seuraa. {city}n alueella on satoja aktiivisia käyttäjiä valmiina tutustumaan sinuun.",
    "Seksitreffit {city}ssa – löydä kumppanisi helposti ja turvallisesti! Tarjoamme Suomen laajimman valikoiman paikallisia profiileja. {city}n sinkkuyhteisö odottaa sinua – rekisteröidy ilmaiseksi!"
]


def slugify(text):
    """Convert text to URL-safe slug"""
    text = text.lower()
    # Remove special Finnish characters
    replacements = {
        'ä': 'a', 'ö': 'o', 'å': 'a',
        'Ä': 'a', 'Ö': 'o', 'Å': 'a'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Remove non-alphanumeric characters
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def get_region_for_city(zip_code):
    """Determine region based on postal code prefix"""
    if not zip_code:
        return "Uusimaa", REGIONS["Uusimaa"]

    prefix = zip_code[:2]

    for region_name, region_data in REGIONS.items():
        if prefix in region_data["prefixes"]:
            return region_name, region_data

    return "Uusimaa", REGIONS["Uusimaa"]


def get_nearby_cities(current_city, all_cities, zip_code, limit=10):
    """Get nearby cities based on postal code proximity"""
    if not zip_code:
        return []

    current_prefix = int(zip_code[:2])
    nearby = []

    for city in all_cities:
        if city["name"] == current_city:
            continue
        if city.get("zip"):
            try:
                city_prefix = int(city["zip"][:2])
                distance = abs(city_prefix - current_prefix)
                nearby.append((city, distance))
            except (ValueError, IndexError):
                continue

    # Sort by distance and get unique city names
    nearby.sort(key=lambda x: x[1])
    seen_names = set()
    result = []

    for city, _ in nearby:
        if city["name"] not in seen_names:
            seen_names.add(city["name"])
            result.append(city)
            if len(result) >= limit:
                break

    return result


def generate_city_page(city_name, city_data, profiles, all_cities, region_name, region_data):
    """Generate HTML page for a city"""

    slug = slugify(city_name)
    zip_code = city_data.get("zip", "")

    # Get nearby cities
    nearby_cities = get_nearby_cities(city_name, all_cities, zip_code)

    # Get profiles for this city
    city_profiles = [p for p in profiles if p.get("kaupunki") == city_name][:10]

    # Random intro and FAQ
    intro_text = random.choice(INTRO_TEMPLATES).format(city=city_name)

    # Generate profiles HTML
    profiles_html = ""
    for i, profile in enumerate(city_profiles):
        profiles_html += f'''
                <div class="col-md-6 col-lg-4 mb-4">
                    <div class="profile-card">
                        <div class="profile-avatar">
                            <i class="bi bi-person-circle"></i>
                            <span class="age-badge">{profile.get("ika", "?")} v</span>
                        </div>
                        <div class="card-body">
                            <h5>{profile.get("nimi", "Tuntematon")}</h5>
                            <p class="location"><i class="bi bi-geo-alt me-1"></i>{city_name}</p>
                            <p class="description">{profile.get("kuvaus", "")}</p>
                            <a href="{CTA_URL}" class="btn btn-primary">
                                <i class="bi bi-chat-heart me-1"></i>Ota yhteytta
                            </a>
                        </div>
                    </div>
                </div>'''

    # Generate nearby cities HTML
    nearby_html = ""
    for nearby in nearby_cities:
        nearby_slug = slugify(nearby["name"])
        nearby_html += f'''
                <div class="col-6 col-md-4 col-lg-3 mb-3">
                    <a href="{nearby_slug}.html" class="nearby-city-card">
                        <i class="bi bi-geo-alt"></i>
                        <h5>{nearby["name"]}</h5>
                    </a>
                </div>'''

    # Generate FAQ HTML
    faq_html = ""
    for i, faq in enumerate(FAQ_TEMPLATES):
        question = faq["question"].format(city=city_name)
        answer = faq["answer"].format(city=city_name)
        collapsed = "" if i == 0 else "collapsed"
        show = "show" if i == 0 else ""
        faq_html += f'''
                <div class="accordion-item">
                    <h2 class="accordion-header">
                        <button class="accordion-button {collapsed}" type="button" data-bs-toggle="collapse" data-bs-target="#faq{i}">
                            {question}
                        </button>
                    </h2>
                    <div id="faq{i}" class="accordion-collapse collapse {show}" data-bs-parent="#faqAccordion">
                        <div class="accordion-body">
                            {answer}
                        </div>
                    </div>
                </div>'''

    # Google Maps URL
    maps_url = f"https://www.google.com/maps/embed/v1/place?key=AIzaSyBFw0Qbyq9zTFTd-tUY6dZWTgaQzuU17R8&q={quote(city_name + ', Finland')}&zoom=12"

    # Member count (simulated)
    member_count = random.randint(150, 800)
    active_today = random.randint(20, 100)
    new_members = random.randint(5, 30)
    success_rate = random.randint(85, 98)

    html_content = f'''<!DOCTYPE html>
<html lang="fi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Seksitreffit {city_name} - Loyda aikuisten seuraa kaupungissa {city_name}. {member_count}+ aktiivista jasentä. Liity ilmaiseksi!">
    <meta name="keywords" content="seksitreffit {city_name}, aikuisten treffit {city_name}, seuranhaku {city_name}, deittailu {city_name}">
    <meta name="robots" content="index, follow">

    <meta property="og:title" content="Seksitreffit {city_name} - Aikuisten Treffipalvelu">
    <meta property="og:description" content="Loyda aikuisten seuraa kaupungissa {city_name}. {member_count}+ jasentä.">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="fi_FI">

    <title>Seksitreffit {city_name} - Aikuisten Seuranhaku | {member_count}+ Jasentä</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
    <link href="../style.css" rel="stylesheet">

    <link rel="canonical" href="https://www.seksitreffitsuomessa.fi/villes/{slug}.html">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark sticky-top">
        <div class="container">
            <a class="navbar-brand" href="../index.html">
                <i class="bi bi-heart-fill me-2"></i>Seksitreffit Suomessa
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="../index.html">Etusivu</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="../index.html#hakemisto">Hakemisto</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link btn btn-primary ms-lg-3" href="{CTA_URL}">
                            <i class="bi bi-person-plus me-1"></i>Liity nyt
                        </a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Breadcrumb -->
    <section class="breadcrumb-section">
        <div class="container">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="../index.html">Etusivu</a></li>
                    <li class="breadcrumb-item"><a href="../index.html#hakemisto">Hakemisto</a></li>
                    <li class="breadcrumb-item"><a href="../regions/{region_data['slug']}.html">{region_name}</a></li>
                    <li class="breadcrumb-item active">{city_name}</li>
                </ol>
            </nav>
        </div>
    </section>

    <!-- Hero Section -->
    <section class="hero-section hero-city">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6 hero-content">
                    <h1>Seksitreffit <span>{city_name}</span></h1>
                    <p>Loyda aikuisten seuraa kaupungissa {city_name}. {member_count}+ aktiivista jasentä odottaa tutustumista sinuun!</p>
                    <a href="{CTA_URL}" class="btn-cta">
                        <i class="bi bi-heart-fill me-2"></i>Liity ilmaiseksi
                    </a>
                </div>
                <div class="col-lg-6 mt-4 mt-lg-0">
                    <div class="map-container">
                        <iframe src="{maps_url}" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Intro Section -->
    <section class="intro-section">
        <div class="container">
            <div class="row">
                <div class="col-lg-8">
                    <h2>Aikuisten Seuranhaku {city_name}ssa</h2>
                    <p>{intro_text}</p>
                </div>
                <div class="col-lg-4">
                    <div class="intro-stats">
                        <div class="intro-stat">
                            <i class="bi bi-people-fill"></i>
                            <h4>{member_count}+</h4>
                            <p>Jasentä</p>
                        </div>
                        <div class="intro-stat">
                            <i class="bi bi-activity"></i>
                            <h4>{active_today}</h4>
                            <p>Aktiivista tanaan</p>
                        </div>
                        <div class="intro-stat">
                            <i class="bi bi-person-plus-fill"></i>
                            <h4>{new_members}</h4>
                            <p>Uutta viikossa</p>
                        </div>
                        <div class="intro-stat">
                            <i class="bi bi-star-fill"></i>
                            <h4>{success_rate}%</h4>
                            <p>Tyytyvaisia</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Profiles Section -->
    <section class="profiles-section">
        <div class="container">
            <h2><i class="bi bi-people me-2"></i>Profiileja kaupungissa {city_name}</h2>
            <p class="text-muted mb-4">Naiset etsivat seuraa - ota yhteytta ja aloita keskustelu</p>
            <div class="row">
                {profiles_html}
            </div>
            <div class="text-center mt-4">
                <a href="{CTA_URL}" class="btn btn-primary btn-lg">
                    <i class="bi bi-search me-2"></i>Nayta kaikki profiilit
                </a>
            </div>
        </div>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section">
        <div class="container">
            <h2>Usein Kysytyt Kysymykset</h2>
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="accordion faq-accordion" id="faqAccordion">
                        {faq_html}
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Nearby Cities Section -->
    <section class="nearby-section">
        <div class="container">
            <h2><i class="bi bi-geo me-2"></i>Kaupungit lahella</h2>
            <p class="text-muted mb-4">Loyda seuraa myos naista kaupungeista</p>
            <div class="row">
                {nearby_html}
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
        <div class="container">
            <h2>Valmis Loytamaan Seuraa {city_name}sta?</h2>
            <p>Liity tuhansien paikallisten sinkkujen joukkoon ja aloita etsinta jo tanaan.</p>
            <a href="{CTA_URL}" class="btn btn-lg">
                <i class="bi bi-heart-fill me-2"></i>Rekisteroidy ilmaiseksi
            </a>
        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 mb-4 mb-lg-0">
                    <h5><i class="bi bi-heart-fill me-2 text-danger"></i>Seksitreffit Suomessa</h5>
                    <p>Suomen suosituin aikuisten treffipalvelu. Loyda seuraa turvallisesti ja helposti.</p>
                </div>
                <div class="col-6 col-lg-2">
                    <h5>Suosituimmat</h5>
                    <a href="helsinki.html">Helsinki</a>
                    <a href="espoo.html">Espoo</a>
                    <a href="tampere.html">Tampere</a>
                    <a href="oulu.html">Oulu</a>
                    <a href="turku.html">Turku</a>
                </div>
                <div class="col-6 col-lg-2">
                    <h5>Kaupungit</h5>
                    <a href="jyvaskyla.html">Jyvaskyla</a>
                    <a href="lahti.html">Lahti</a>
                    <a href="kuopio.html">Kuopio</a>
                    <a href="pori.html">Pori</a>
                    <a href="joensuu.html">Joensuu</a>
                </div>
                <div class="col-6 col-lg-2">
                    <h5>Maakunnat</h5>
                    <a href="../regions/uusimaa.html">Uusimaa</a>
                    <a href="../regions/pirkanmaa.html">Pirkanmaa</a>
                    <a href="../regions/varsinais-suomi.html">Varsinais-Suomi</a>
                    <a href="../regions/lappi.html">Lappi</a>
                </div>
                <div class="col-6 col-lg-2">
                    <h5>Tietoa</h5>
                    <a href="#">Kayttoehdot</a>
                    <a href="#">Tietosuoja</a>
                    <a href="#">Yhteystiedot</a>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Seksitreffit Suomessa. Kaikki oikeudet pidatetaan. Vain yli 18-vuotiaille.</p>
            </div>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="../script.js"></script>
</body>
</html>'''

    return html_content


def update_index_html(cities_by_region, all_cities):
    """Update index.html with region accordion and cities data"""

    with open("index.html", "r", encoding="utf-8") as f:
        index_content = f.read()

    # Generate accordion HTML
    accordion_html = ""
    for i, (region_name, region_data) in enumerate(REGIONS.items()):
        cities = cities_by_region.get(region_name, [])
        if not cities:
            continue

        collapsed = "" if i == 0 else "collapsed"
        show = "show" if i == 0 else ""

        cities_links = ""
        for city in sorted(cities, key=lambda x: x["name"])[:20]:
            city_slug = slugify(city["name"])
            cities_links += f'<a href="villes/{city_slug}.html" class="dept-link">{city["name"]}</a>\n'

        accordion_html += f'''
                <div class="accordion-item">
                    <h2 class="accordion-header">
                        <button class="accordion-button {collapsed}" type="button" data-bs-toggle="collapse" data-bs-target="#region{i}">
                            <i class="bi bi-geo-alt-fill me-2"></i>{region_name}
                            <span class="badge bg-primary ms-2">{len(cities)}</span>
                        </button>
                    </h2>
                    <div id="region{i}" class="accordion-collapse collapse {show}" data-bs-parent="#regionAccordion">
                        <div class="accordion-body">
                            <a href="regions/{region_data['slug']}.html" class="btn btn-sm btn-outline-primary mb-3">
                                <i class="bi bi-list me-1"></i>Nayta kaikki ({len(cities)})
                            </a>
                            <div>
                                {cities_links}
                            </div>
                        </div>
                    </div>
                </div>'''

    # Generate cities data for search
    unique_cities = {}
    for city in all_cities:
        if city["name"] not in unique_cities:
            unique_cities[city["name"]] = {
                "name": city["name"],
                "slug": slugify(city["name"])
            }

    cities_js = ",\n            ".join([
        f'{{"name": "{c["name"]}", "slug": "{c["slug"]}"}}'
        for c in sorted(unique_cities.values(), key=lambda x: x["name"])
    ])

    # Replace placeholders
    index_content = index_content.replace(
        "<!-- REGION_ACCORDION_PLACEHOLDER -->",
        accordion_html
    )
    index_content = index_content.replace(
        "<!-- CITIES_DATA_PLACEHOLDER -->",
        cities_js
    )

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_content)

    print("Updated index.html with region accordion and cities data")


def main():
    """Main function to generate all city pages"""

    print("=" * 50)
    print("Generating city pages for Seksitreffit Suomessa")
    print("=" * 50)

    # Load data
    print("\nLoading data...")
    with open("villes_finlande.json", "r", encoding="utf-8") as f:
        cities = json.load(f)

    with open("profiilit_kaikki_kaupungit.json", "r", encoding="utf-8") as f:
        profiles = json.load(f)

    print(f"Loaded {len(cities)} city entries")
    print(f"Loaded {len(profiles)} profiles")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Group cities by name (remove duplicates)
    unique_cities = {}
    for city in cities:
        name = city["name"]
        if name not in unique_cities:
            unique_cities[name] = city

    print(f"Found {len(unique_cities)} unique cities")

    # Organize cities by region
    cities_by_region = {region: [] for region in REGIONS}

    for city_name, city_data in unique_cities.items():
        region_name, _ = get_region_for_city(city_data.get("zip"))
        cities_by_region[region_name].append(city_data)

    # Generate pages
    print("\nGenerating city pages...")
    generated = 0

    for city_name, city_data in unique_cities.items():
        region_name, region_data = get_region_for_city(city_data.get("zip"))

        html_content = generate_city_page(
            city_name,
            city_data,
            profiles,
            cities,
            region_name,
            region_data
        )

        slug = slugify(city_name)
        filepath = os.path.join(OUTPUT_DIR, f"{slug}.html")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        generated += 1
        if generated % 50 == 0:
            print(f"  Generated {generated} pages...")

    print(f"\nGenerated {generated} city pages in '{OUTPUT_DIR}/' directory")

    # Save regions data
    regions_data = {}
    for region_name, region_data in REGIONS.items():
        region_cities = cities_by_region.get(region_name, [])
        regions_data[region_name] = {
            "slug": region_data["slug"],
            "main_city": region_data["main_city"],
            "cities": [{"name": c["name"], "slug": slugify(c["name"])} for c in region_cities]
        }

    with open(REGIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(regions_data, f, ensure_ascii=False, indent=2)

    print(f"Saved regions data to '{REGIONS_FILE}'")

    # Update index.html
    update_index_html(cities_by_region, cities)

    print("\n" + "=" * 50)
    print("Generation complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
