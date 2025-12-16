#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de generation des pages de regions pour Seksitreffit Suomessa
Genere une page HTML pour chaque region (maakunta) de Finlande
"""

import json
import os
import re
import random

# Configuration
CTA_URL = "https://www.seksitreffitsuomessa.fi/offer"
OUTPUT_DIR = "regions"
REGIONS_FILE = "regions.json"

# Region descriptions en finnois
REGION_DESCRIPTIONS = {
    "Uusimaa": "Uusimaa on Suomen väkirikkain maakunta, jossa sijaitsevat Helsinki, Espoo ja Vantaa. Alueella asuu yli 1,7 miljoonaa ihmistä, mikä tekee siitä Suomen aktiivisimman seuranhakualueen.",
    "Varsinais-Suomi": "Varsinais-Suomi on lounaisrannikolla sijaitseva historiallinen maakunta. Turun kaupunki on alueen keskus, ja saaristomeri tarjoaa ainutlaatuisen ympäristön.",
    "Satakunta": "Satakunta sijaitsee länsirannikolla Porin kaupungin ympärillä. Alue tunnetaan teollisuudestaan ja kauniista rannikkomaisemistaan.",
    "Kanta-Hame": "Kanta-Häme on historiallinen maakunta Etelä-Suomessa. Hämeenlinnan kaupunki on alueen keskus, ja järvimaisemat ovat tyypillisiä alueelle.",
    "Pirkanmaa": "Pirkanmaa on Tampereen ympärille rakentunut kasvava maakunta. Tampere on Suomen kolmanneksi suurin kaupunki ja vilkas kulttuurikeskus.",
    "Paijat-Hame": "Päijät-Häme sijaitsee Lahden kaupungin ympärillä. Alue tunnetaan talviurheiluperinteistään ja Vesijärven maisemista.",
    "Kymenlaakso": "Kymenlaakso sijaitsee Kaakkois-Suomessa. Kouvola ja Kotka ovat alueen suurimmat kaupungit, ja meri on läsnä arjessa.",
    "Etela-Karjala": "Etelä-Karjala sijaitsee Venäjän rajan tuntumassa. Lappeenranta ja Imatra ovat alueen keskukset, Saimaan rannalla.",
    "Etela-Savo": "Etelä-Savo on järvien ja metsien maakunta. Mikkeli ja Savonlinna ovat alueen tunnetuimmat kaupungit.",
    "Pohjois-Savo": "Pohjois-Savo on Kuopion ympärille rakentunut maakunta. Kallavesi ja savolaiset perinteet leimaavat aluetta.",
    "Pohjois-Karjala": "Pohjois-Karjala on itäinen maakunta Joensuun ympärillä. Koli ja karjalainen kulttuuri ovat alueen ylpeydenaiheita.",
    "Keski-Suomi": "Keski-Suomi on Jyväskylän ympärille rakentunut maakunta. Alue on tunnettu järvistään ja korkeakouluistaan.",
    "Etela-Pohjanmaa": "Etelä-Pohjanmaa on Seinäjoen ympärillä sijaitseva maakunta. Lakeudet ja pohjalaisuus leimaavat alueen identiteettiä.",
    "Pohjanmaa": "Pohjanmaa sijaitsee länsirannikolla Vaasan ympärillä. Alue on kaksikielinen, ja ruotsinkielistä kulttuuria on vahvasti läsnä.",
    "Keski-Pohjanmaa": "Keski-Pohjanmaa on pieni maakunta Kokkolan ympärillä. Rannikon ja sisämaan yhdistelmä tekee alueesta ainutlaatuisen.",
    "Pohjois-Pohjanmaa": "Pohjois-Pohjanmaa on Oulun ympärille rakentunut laaja maakunta. Oulu on Pohjois-Suomen suurin kaupunki ja teknologiakeskus.",
    "Kainuu": "Kainuu on harvaan asuttu maakunta Kajaanin ympärillä. Luonto ja erämaisemat ovat alueen vetovoimatekijöitä.",
    "Lappi": "Lappi on Suomen pohjoisin ja suurin maakunta. Rovaniemi, revontulet ja Joulupukki tekevät alueesta ainutlaatuisen.",
    "Ahvenanmaa": "Ahvenanmaa on autonominen saaristomaakunta Itämerellä. Mariehamn on alueen ainoa kaupunki, ja ruotsinkielinen kulttuuri on vahva."
}


def slugify(text):
    """Convert text to URL-safe slug"""
    text = text.lower()
    replacements = {
        'ä': 'a', 'ö': 'o', 'å': 'a',
        'Ä': 'a', 'Ö': 'o', 'Å': 'a'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text


def generate_region_page(region_name, region_data, all_regions):
    """Generate HTML page for a region"""

    slug = region_data["slug"]
    cities = region_data.get("cities", [])
    main_city = region_data.get("main_city", "")
    description = REGION_DESCRIPTIONS.get(region_name, f"{region_name} on suomalainen maakunta.")

    # Statistics
    total_cities = len(cities)
    total_members = total_cities * random.randint(100, 300)
    active_today = random.randint(50, 200)

    # Generate cities grid HTML
    cities_html = ""
    for city in sorted(cities, key=lambda x: x["name"]):
        member_count = random.randint(50, 300)
        cities_html += f'''
                <div class="col-md-6 col-lg-4 mb-3 city-item">
                    <a href="../villes/{city["slug"]}.html" class="city-list-card">
                        <div class="d-flex justify-content-between align-items-center">
                            <h5><i class="bi bi-geo-alt me-2 text-primary"></i>{city["name"]}</h5>
                            <span class="badge bg-primary">{member_count}+</span>
                        </div>
                    </a>
                </div>'''

    # Other regions for footer
    other_regions = [r for r in all_regions.items() if r[0] != region_name][:5]
    other_regions_html = ""
    for other_name, other_data in other_regions:
        other_regions_html += f'<a href="{other_data["slug"]}.html">{other_name}</a>\n'

    html_content = f'''<!DOCTYPE html>
<html lang="fi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Seksitreffit {region_name} - Loyda aikuisten seuraa {region_name}n alueelta. {total_cities} kaupunkia, {total_members}+ jasentä.">
    <meta name="keywords" content="seksitreffit {region_name}, aikuisten treffit {region_name}, seuranhaku {region_name}, {main_city}">
    <meta name="robots" content="index, follow">

    <meta property="og:title" content="Seksitreffit {region_name} - Aikuisten Treffipalvelu">
    <meta property="og:description" content="Loyda aikuisten seuraa {region_name}n alueelta. {total_cities} kaupunkia.">
    <meta property="og:type" content="website">
    <meta property="og:locale" content="fi_FI">

    <title>Seksitreffit {region_name} - {total_cities} Kaupunkia | Aikuisten Seuranhaku</title>

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css" rel="stylesheet">
    <link href="../style.css" rel="stylesheet">

    <link rel="canonical" href="https://www.seksitreffitsuomessa.fi/regions/{slug}.html">
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
                    <li class="breadcrumb-item active">{region_name}</li>
                </ol>
            </nav>
        </div>
    </section>

    <!-- Region Hero -->
    <section class="region-hero">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-8">
                    <h1><i class="bi bi-map me-3"></i>{region_name}</h1>
                    <p class="lead">{description}</p>
                    <div class="d-flex flex-wrap gap-4 mt-4">
                        <div>
                            <i class="bi bi-geo-alt-fill me-2"></i>
                            <strong>{total_cities}</strong> kaupunkia
                        </div>
                        <div>
                            <i class="bi bi-people-fill me-2"></i>
                            <strong>{total_members}+</strong> jasentä
                        </div>
                        <div>
                            <i class="bi bi-activity me-2"></i>
                            <strong>{active_today}</strong> aktiivista tanaan
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 text-center d-none d-lg-block">
                    <a href="{CTA_URL}" class="btn-cta">
                        <i class="bi bi-heart-fill me-2"></i>Liity ilmaiseksi
                    </a>
                </div>
            </div>
        </div>
    </section>

    <!-- Cities Grid -->
    <section class="cities-grid">
        <div class="container">
            <div class="row mb-4">
                <div class="col-md-6">
                    <h2><i class="bi bi-list-ul me-2"></i>Kaupungit maakunnassa {region_name}</h2>
                </div>
                <div class="col-md-6">
                    <input type="text" class="form-control filter-input" id="cityFilter"
                           placeholder="Suodata kaupunkeja...">
                </div>
            </div>

            <div class="row" id="citiesGrid">
                {cities_html}
            </div>

            <div class="text-center mt-4">
                <a href="{CTA_URL}" class="btn btn-primary btn-lg">
                    <i class="bi bi-person-plus me-2"></i>Rekisteroidy ja loyda seuraa
                </a>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
        <div class="container">
            <h2>Loyda Seuraa {region_name}n Alueelta</h2>
            <p>Tuhannet sinkut etsivat kumppania - liity mukaan jo tanaan!</p>
            <a href="{CTA_URL}" class="btn btn-lg">
                <i class="bi bi-heart-fill me-2"></i>Aloita ilmaiseksi
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
                    <a href="../villes/helsinki.html">Helsinki</a>
                    <a href="../villes/espoo.html">Espoo</a>
                    <a href="../villes/tampere.html">Tampere</a>
                    <a href="../villes/oulu.html">Oulu</a>
                    <a href="../villes/turku.html">Turku</a>
                </div>
                <div class="col-6 col-lg-2">
                    <h5>Kaupungit</h5>
                    <a href="../villes/jyvaskyla.html">Jyvaskyla</a>
                    <a href="../villes/lahti.html">Lahti</a>
                    <a href="../villes/kuopio.html">Kuopio</a>
                    <a href="../villes/pori.html">Pori</a>
                    <a href="../villes/joensuu.html">Joensuu</a>
                </div>
                <div class="col-6 col-lg-2">
                    <h5>Maakunnat</h5>
                    {other_regions_html}
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


def main():
    """Main function to generate all region pages"""

    print("=" * 50)
    print("Generating region pages for Seksitreffit Suomessa")
    print("=" * 50)

    # Load regions data
    print("\nLoading regions data...")

    if not os.path.exists(REGIONS_FILE):
        print(f"Error: {REGIONS_FILE} not found. Run generate_city_pages.py first.")
        return

    with open(REGIONS_FILE, "r", encoding="utf-8") as f:
        regions_data = json.load(f)

    print(f"Loaded {len(regions_data)} regions")

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Generate pages
    print("\nGenerating region pages...")
    generated = 0

    for region_name, region_data in regions_data.items():
        if not region_data.get("cities"):
            print(f"  Skipping {region_name} (no cities)")
            continue

        html_content = generate_region_page(region_name, region_data, regions_data)

        filepath = os.path.join(OUTPUT_DIR, f"{region_data['slug']}.html")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        generated += 1
        print(f"  Generated: {region_name} ({len(region_data['cities'])} cities)")

    print(f"\nGenerated {generated} region pages in '{OUTPUT_DIR}/' directory")
    print("\n" + "=" * 50)
    print("Generation complete!")
    print("=" * 50)


if __name__ == "__main__":
    main()
