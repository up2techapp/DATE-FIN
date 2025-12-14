#!/usr/bin/env python3
"""
Script de génération des pages villes pour l'annuaire Agence Web France
Génère une page HTML optimisée SEO pour chaque ville
Version enrichie avec contenu SEO complet et EmailJS
"""

import json
import os
from pathlib import Path
from urllib.parse import quote

# Configuration
VILLES_JSON = "villes.json"
OUTPUT_DIR = "villes"
TEMPLATE_FILE = "ville_template.html"

def get_departement(zip_code):
    """Extrait le département du code postal"""
    if zip_code.startswith("97"):
        return zip_code[:3]  # DOM-TOM
    return zip_code[:2]

def get_departement_name(dept_code):
    """Retourne le nom du département"""
    departements = {
        "01": "Ain", "02": "Aisne", "03": "Allier", "04": "Alpes-de-Haute-Provence",
        "05": "Hautes-Alpes", "06": "Alpes-Maritimes", "07": "Ardèche", "08": "Ardennes",
        "09": "Ariège", "10": "Aube", "11": "Aude", "12": "Aveyron",
        "13": "Bouches-du-Rhône", "14": "Calvados", "15": "Cantal", "16": "Charente",
        "17": "Charente-Maritime", "18": "Cher", "19": "Corrèze", "2A": "Corse-du-Sud",
        "2B": "Haute-Corse", "21": "Côte-d'Or", "22": "Côtes-d'Armor", "23": "Creuse",
        "24": "Dordogne", "25": "Doubs", "26": "Drôme", "27": "Eure",
        "28": "Eure-et-Loir", "29": "Finistère", "30": "Gard", "31": "Haute-Garonne",
        "32": "Gers", "33": "Gironde", "34": "Hérault", "35": "Ille-et-Vilaine",
        "36": "Indre", "37": "Indre-et-Loire", "38": "Isère", "39": "Jura",
        "40": "Landes", "41": "Loir-et-Cher", "42": "Loire", "43": "Haute-Loire",
        "44": "Loire-Atlantique", "45": "Loiret", "46": "Lot", "47": "Lot-et-Garonne",
        "48": "Lozère", "49": "Maine-et-Loire", "50": "Manche", "51": "Marne",
        "52": "Haute-Marne", "53": "Mayenne", "54": "Meurthe-et-Moselle", "55": "Meuse",
        "56": "Morbihan", "57": "Moselle", "58": "Nièvre", "59": "Nord",
        "60": "Oise", "61": "Orne", "62": "Pas-de-Calais", "63": "Puy-de-Dôme",
        "64": "Pyrénées-Atlantiques", "65": "Hautes-Pyrénées", "66": "Pyrénées-Orientales",
        "67": "Bas-Rhin", "68": "Haut-Rhin", "69": "Rhône", "70": "Haute-Saône",
        "71": "Saône-et-Loire", "72": "Sarthe", "73": "Savoie", "74": "Haute-Savoie",
        "75": "Paris", "76": "Seine-Maritime", "77": "Seine-et-Marne", "78": "Yvelines",
        "79": "Deux-Sèvres", "80": "Somme", "81": "Tarn", "82": "Tarn-et-Garonne",
        "83": "Var", "84": "Vaucluse", "85": "Vendée", "86": "Vienne",
        "87": "Haute-Vienne", "88": "Vosges", "89": "Yonne", "90": "Territoire de Belfort",
        "91": "Essonne", "92": "Hauts-de-Seine", "93": "Seine-Saint-Denis",
        "94": "Val-de-Marne", "95": "Val-d'Oise",
        "971": "Guadeloupe", "972": "Martinique", "973": "Guyane",
        "974": "La Réunion", "976": "Mayotte"
    }
    return departements.get(dept_code, f"Département {dept_code}")

def find_nearby_cities(current_ville, all_villes, villes_by_dept, count=10):
    """Trouve les villes à proximité basé sur le code postal"""
    current_zip = current_ville["zip"]
    current_slug = current_ville["slug"]
    current_dept = get_departement(current_zip)

    try:
        current_zip_num = int(current_zip)
    except ValueError:
        current_zip_num = 0

    nearby = []

    # D'abord, chercher dans le même département
    if current_dept in villes_by_dept:
        for ville in villes_by_dept[current_dept]:
            if ville["slug"] != current_slug:
                try:
                    ville_zip_num = int(ville["zip"])
                    distance = abs(ville_zip_num - current_zip_num)
                except ValueError:
                    distance = 99999
                nearby.append((ville, distance))

    # Si pas assez, chercher dans les départements voisins
    if len(nearby) < count:
        try:
            current_dept_num = int(current_dept)
            neighbor_depts = [
                str(current_dept_num - 1).zfill(2),
                str(current_dept_num + 1).zfill(2)
            ]
            for dept in neighbor_depts:
                if dept in villes_by_dept:
                    for ville in villes_by_dept[dept]:
                        if ville["slug"] != current_slug:
                            try:
                                ville_zip_num = int(ville["zip"])
                                distance = abs(ville_zip_num - current_zip_num)
                            except ValueError:
                                distance = 99999
                            nearby.append((ville, distance))
        except ValueError:
            pass

    # Trier par proximité et prendre les N plus proches
    nearby.sort(key=lambda x: x[1])
    return [v[0] for v in nearby[:count]]

def generate_nearby_cities_html(nearby_cities):
    """Génère le HTML pour la section villes aux alentours"""
    if not nearby_cities:
        return ""

    cities_html = ""
    for ville in nearby_cities:
        cities_html += f'''
                <div class="col-6 col-md-4 col-lg-3 col-xl-2">
                    <a href="agence-web-{ville['slug']}.html" class="nearby-city-card">
                        <i class="bi bi-geo-alt text-primary mb-2"></i>
                        <span class="city-name">{ville['name']}</span>
                        <small class="text-muted">{ville['zip']}</small>
                    </a>
                </div>'''

    return f'''
    <section class="section-padding bg-light">
        <div class="container">
            <h2 class="section-title text-center mb-5">Villes aux Alentours</h2>
            <p class="text-center text-muted mb-4">Découvrez nos services dans les villes proches</p>
            <div class="row g-3 justify-content-center">
                {cities_html}
            </div>
        </div>
    </section>
'''

def generate_page_html(ville, nearby_cities=None):
    """Génère le HTML pour une page ville avec contenu SEO enrichi"""
    name = ville["name"]
    zip_code = ville["zip"]
    slug = ville["slug"]
    dept = get_departement(zip_code)
    dept_name = get_departement_name(dept)

    # Générer la section villes aux alentours
    nearby_section = generate_nearby_cities_html(nearby_cities) if nearby_cities else ""

    # URL encodée pour Google Maps
    map_query = quote(f"{name} {zip_code} France")

    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">

    <title>Agence Web {name} ({zip_code}) - Création de Sites Internet | Agence Web France</title>
    <meta name="description" content="Agence web à {name} ({zip_code}) dans le {dept_name}. Création de sites internet professionnels, e-commerce, référencement SEO et solutions digitales sur mesure. Devis gratuit sous 24h.">
    <meta name="keywords" content="agence web {name}, création site internet {name}, développement web {zip_code}, webmaster {name}, site vitrine {name}, e-commerce {name}, SEO {name}, référencement {name}, {dept_name}">
    <meta name="author" content="Agence Web France">
    <meta name="robots" content="index, follow">

    <meta property="og:type" content="website">
    <meta property="og:title" content="Agence Web {name} ({zip_code}) - Création de Sites Internet">
    <meta property="og:description" content="Votre agence web locale à {name} pour la création de sites professionnels, e-commerce et référencement SEO. Devis gratuit.">
    <meta property="og:locale" content="fr_FR">

    <link rel="canonical" href="https://www.agencewebfrance.fr/villes/agence-web-{slug}.html">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <link rel="stylesheet" href="../style.css">
    <script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>
</head>
<body>
    <header id="header" class="header-sticky">
        <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
            <div class="container">
                <a class="navbar-brand fw-bold text-primary" href="../index.html">
                    <i class="bi bi-globe2"></i> Agence Web France
                </a>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav ms-auto">
                        <li class="nav-item"><a class="nav-link" href="../index.html">Accueil</a></li>
                        <li class="nav-item"><a class="nav-link" href="../index.html#services">Services</a></li>
                        <li class="nav-item"><a class="nav-link" href="../index.html#about">À Propos</a></li>
                        <li class="nav-item"><a class="nav-link" href="../index.html#portfolio">Portfolio</a></li>
                        <li class="nav-item"><a class="nav-link active" href="../index.html#annuaire">Annuaire</a></li>
                        <li class="nav-item"><a class="nav-link" href="../index.html#contact">Contact</a></li>
                        <li class="nav-item">
                            <a class="nav-link btn btn-primary text-white ms-lg-3 px-4" href="../index.html#contact">Devis Gratuit</a>
                        </li>
                    </ul>
                </div>
            </div>
        </nav>
    </header>

    <!-- Hero Section avec Google Maps -->
    <section class="city-hero section-padding" style="padding-top: 120px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
        <div class="container">
            <nav aria-label="breadcrumb" class="mb-4">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="../index.html">Accueil</a></li>
                    <li class="breadcrumb-item"><a href="../index.html#annuaire">Annuaire</a></li>
                    <li class="breadcrumb-item"><a href="../departements/annuaire-departement-{dept}.html">{dept_name}</a></li>
                    <li class="breadcrumb-item active" aria-current="page">{name}</li>
                </ol>
            </nav>

            <div class="row align-items-center">
                <div class="col-lg-7">
                    <h1 class="display-5 fw-bold mb-4">
                        Agence Web à <span class="text-primary">{name}</span>
                    </h1>
                    <p class="lead mb-4">
                        Votre partenaire digital de confiance à {name} ({zip_code}) pour la création de sites internet
                        professionnels et le développement de solutions web sur mesure dans le {dept_name}.
                    </p>
                    <div class="d-flex gap-3 flex-wrap mb-4">
                        <span class="badge bg-primary fs-6 p-2"><i class="bi bi-geo-alt"></i> {name}</span>
                        <span class="badge bg-secondary fs-6 p-2"><i class="bi bi-mailbox"></i> {zip_code}</span>
                        <span class="badge bg-info fs-6 p-2"><i class="bi bi-map"></i> {dept_name}</span>
                    </div>
                    <div class="d-flex gap-3 flex-wrap">
                        <a href="../index.html#contact" class="btn btn-primary btn-lg px-4">
                            <i class="bi bi-envelope"></i> Demander un Devis
                        </a>
                        <a href="tel:+33641127926" class="btn btn-outline-primary btn-lg px-4">
                            <i class="bi bi-telephone"></i> 06 41 12 79 26
                        </a>
                    </div>
                </div>
                <div class="col-lg-5 text-center mt-4 mt-lg-0">
                    <div class="city-map-container">
                        <iframe
                            src="https://maps.google.com/maps?q={map_query}&t=&z=13&ie=UTF8&iwloc=&output=embed"
                            class="city-map"
                            allowfullscreen
                            loading="lazy"
                            referrerpolicy="no-referrer-when-downgrade"
                            title="Carte de {name}">
                        </iframe>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Section Introduction SEO -->
    <section class="section-padding">
        <div class="container">
            <div class="row">
                <div class="col-lg-10 mx-auto">
                    <h2 class="h3 fw-bold mb-4 text-center">Création de Site Internet à {name} - Votre Agence Web Locale</h2>
                    <p class="text-muted mb-4">
                        Bienvenue chez <strong>Agence Web France</strong>, votre expert en création de sites internet à {name} ({zip_code}).
                        Implantée dans le {dept_name}, notre agence web accompagne les entreprises, artisans, commerçants et professions
                        libérales dans leur transformation digitale. Nous concevons des sites web professionnels, modernes et optimisés
                        pour le référencement naturel (SEO) afin de vous garantir une visibilité maximale sur Google.
                    </p>
                    <p class="text-muted mb-4">
                        Que vous soyez une TPE, une PME ou un indépendant à {name}, nous vous proposons des solutions web adaptées à vos
                        besoins et à votre budget. Notre équipe de développeurs, designers et experts SEO travaille en étroite collaboration
                        avec vous pour créer un site internet qui reflète parfaitement votre identité et atteint vos objectifs commerciaux.
                    </p>
                    <div class="row text-center mt-5">
                        <div class="col-md-3 col-6 mb-4">
                            <div class="stat-box p-3 rounded bg-light">
                                <div class="display-6 fw-bold text-primary">150+</div>
                                <small class="text-muted">Projets réalisés</small>
                            </div>
                        </div>
                        <div class="col-md-3 col-6 mb-4">
                            <div class="stat-box p-3 rounded bg-light">
                                <div class="display-6 fw-bold text-primary">98%</div>
                                <small class="text-muted">Clients satisfaits</small>
                            </div>
                        </div>
                        <div class="col-md-3 col-6 mb-4">
                            <div class="stat-box p-3 rounded bg-light">
                                <div class="display-6 fw-bold text-primary">24h</div>
                                <small class="text-muted">Délai de réponse</small>
                            </div>
                        </div>
                        <div class="col-md-3 col-6 mb-4">
                            <div class="stat-box p-3 rounded bg-light">
                                <div class="display-6 fw-bold text-primary">10+</div>
                                <small class="text-muted">Années d'expérience</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Section Services -->
    <section class="section-padding bg-light">
        <div class="container">
            <h2 class="section-title text-center mb-3">Nos Services Web à {name}</h2>
            <p class="section-subtitle text-center text-muted mb-5">
                Des solutions digitales complètes pour développer votre activité dans le {dept_name}
            </p>
            <div class="row g-4">
                <div class="col-md-6 col-lg-4">
                    <div class="service-card card h-100 border-0 shadow-sm">
                        <div class="card-body text-center p-4">
                            <div class="service-icon mb-3">
                                <i class="bi bi-palette display-4 text-primary"></i>
                            </div>
                            <h3 class="h5 fw-bold mb-3">Site Vitrine à {name}</h3>
                            <p class="text-muted">
                                Création de sites vitrines professionnels pour présenter votre activité à {name}.
                                Design moderne, responsive et optimisé pour convertir vos visiteurs en clients.
                            </p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-lg-4">
                    <div class="service-card card h-100 border-0 shadow-sm">
                        <div class="card-body text-center p-4">
                            <div class="service-icon mb-3">
                                <i class="bi bi-cart3 display-4 text-primary"></i>
                            </div>
                            <h3 class="h5 fw-bold mb-3">Site E-commerce</h3>
                            <p class="text-muted">
                                Boutiques en ligne performantes pour vendre vos produits depuis {name} partout en France.
                                Solutions WooCommerce, Prestashop ou sur mesure.
                            </p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-lg-4">
                    <div class="service-card card h-100 border-0 shadow-sm">
                        <div class="card-body text-center p-4">
                            <div class="service-icon mb-3">
                                <i class="bi bi-search display-4 text-primary"></i>
                            </div>
                            <h3 class="h5 fw-bold mb-3">Référencement SEO</h3>
                            <p class="text-muted">
                                Optimisation SEO locale pour positionner votre entreprise de {name} en première page Google.
                                Audit, stratégie et suivi de positionnement.
                            </p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-lg-4">
                    <div class="service-card card h-100 border-0 shadow-sm">
                        <div class="card-body text-center p-4">
                            <div class="service-icon mb-3">
                                <i class="bi bi-phone display-4 text-primary"></i>
                            </div>
                            <h3 class="h5 fw-bold mb-3">Sites Responsive</h3>
                            <p class="text-muted">
                                Sites web adaptatifs parfaitement optimisés pour mobiles et tablettes.
                                Expérience utilisateur fluide sur tous les appareils.
                            </p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-lg-4">
                    <div class="service-card card h-100 border-0 shadow-sm">
                        <div class="card-body text-center p-4">
                            <div class="service-icon mb-3">
                                <i class="bi bi-arrow-repeat display-4 text-primary"></i>
                            </div>
                            <h3 class="h5 fw-bold mb-3">Refonte de Site</h3>
                            <p class="text-muted">
                                Modernisation de votre site web existant. Nouveau design, meilleures performances
                                et optimisation pour le référencement à {name}.
                            </p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6 col-lg-4">
                    <div class="service-card card h-100 border-0 shadow-sm">
                        <div class="card-body text-center p-4">
                            <div class="service-icon mb-3">
                                <i class="bi bi-gear display-4 text-primary"></i>
                            </div>
                            <h3 class="h5 fw-bold mb-3">Maintenance Web</h3>
                            <p class="text-muted">
                                Maintenance et mise à jour de votre site internet. Sécurité, sauvegardes
                                et support technique réactif pour les entreprises de {name}.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Section Pourquoi Nous Choisir -->
    <section class="section-padding">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6 mb-4 mb-lg-0">
                    <h2 class="h3 fw-bold mb-4">Pourquoi Choisir Notre Agence Web à {name} ?</h2>
                    <p class="text-muted mb-4">
                        Notre agence se distingue par son approche personnalisée et sa connaissance du tissu économique local.
                        Nous comprenons les enjeux des entreprises du {dept_name} et proposons des solutions adaptées à chaque projet.
                    </p>
                    <ul class="list-unstyled">
                        <li class="mb-3 d-flex align-items-start">
                            <i class="bi bi-check-circle-fill text-primary me-3 fs-5"></i>
                            <div>
                                <strong>Proximité et Réactivité</strong>
                                <p class="text-muted mb-0 small">Une équipe disponible et à l'écoute dans le {dept_name}</p>
                            </div>
                        </li>
                        <li class="mb-3 d-flex align-items-start">
                            <i class="bi bi-check-circle-fill text-primary me-3 fs-5"></i>
                            <div>
                                <strong>Expertise Technique</strong>
                                <p class="text-muted mb-0 small">Plus de 150 projets réalisés avec succès en France</p>
                            </div>
                        </li>
                        <li class="mb-3 d-flex align-items-start">
                            <i class="bi bi-check-circle-fill text-primary me-3 fs-5"></i>
                            <div>
                                <strong>Solutions Sur Mesure</strong>
                                <p class="text-muted mb-0 small">Chaque projet est unique, nos solutions aussi</p>
                            </div>
                        </li>
                        <li class="mb-3 d-flex align-items-start">
                            <i class="bi bi-check-circle-fill text-primary me-3 fs-5"></i>
                            <div>
                                <strong>Tarifs Transparents</strong>
                                <p class="text-muted mb-0 small">Devis détaillé et sans surprise pour les entreprises de {name}</p>
                            </div>
                        </li>
                    </ul>
                </div>
                <div class="col-lg-6">
                    <div class="card border-0 shadow">
                        <div class="card-body p-4">
                            <h3 class="h5 fw-bold mb-4 text-center">Demandez votre devis gratuit à {name}</h3>
                            <form>
                                <div class="mb-3">
                                    <input type="text" class="form-control" placeholder="Votre nom *" required>
                                </div>
                                <div class="mb-3">
                                    <input type="email" class="form-control" placeholder="Votre email *" required>
                                </div>
                                <div class="mb-3">
                                    <input type="tel" class="form-control" placeholder="Téléphone">
                                </div>
                                <div class="mb-3">
                                    <select class="form-select">
                                        <option selected>Type de projet</option>
                                        <option>Site vitrine</option>
                                        <option>Site e-commerce</option>
                                        <option>Refonte de site</option>
                                        <option>Référencement SEO</option>
                                        <option>Autre</option>
                                    </select>
                                </div>
                                <div class="mb-3">
                                    <textarea class="form-control" rows="3" placeholder="Décrivez votre projet à {name}"></textarea>
                                </div>
                                <button type="submit" class="btn btn-primary w-100">
                                    <i class="bi bi-send"></i> Recevoir mon devis gratuit
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Section FAQ -->
    <section class="section-padding bg-light">
        <div class="container">
            <h2 class="section-title text-center mb-3">Questions Fréquentes</h2>
            <p class="section-subtitle text-center text-muted mb-5">
                Les réponses aux questions les plus posées sur la création de site à {name}
            </p>
            <div class="row justify-content-center">
                <div class="col-lg-8">
                    <div class="accordion" id="faqAccordion">
                        <div class="accordion-item border-0 mb-3 shadow-sm">
                            <h3 class="accordion-header">
                                <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#faq1">
                                    Combien coûte la création d'un site internet à {name} ?
                                </button>
                            </h3>
                            <div id="faq1" class="accordion-collapse collapse show" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">
                                    Le coût d'un site web varie selon vos besoins. Un site vitrine démarre à partir de 990€,
                                    tandis qu'une boutique e-commerce commence à 1990€. Nous établissons un devis personnalisé
                                    gratuit adapté à votre projet à {name}.
                                </div>
                            </div>
                        </div>
                        <div class="accordion-item border-0 mb-3 shadow-sm">
                            <h3 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq2">
                                    Quel est le délai de création d'un site web ?
                                </button>
                            </h3>
                            <div id="faq2" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">
                                    En moyenne, comptez 2 à 4 semaines pour un site vitrine et 4 à 8 semaines pour un site e-commerce.
                                    Ces délais peuvent varier selon la complexité du projet et votre réactivité pour les validations.
                                </div>
                            </div>
                        </div>
                        <div class="accordion-item border-0 mb-3 shadow-sm">
                            <h3 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq3">
                                    Proposez-vous un service de maintenance ?
                                </button>
                            </h3>
                            <div id="faq3" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">
                                    Oui, nous proposons des forfaits de maintenance mensuels incluant les mises à jour de sécurité,
                                    les sauvegardes régulières, le support technique et les modifications mineures de contenu.
                                </div>
                            </div>
                        </div>
                        <div class="accordion-item border-0 mb-3 shadow-sm">
                            <h3 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq4">
                                    Mon site sera-t-il bien référencé sur Google ?
                                </button>
                            </h3>
                            <div id="faq4" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">
                                    Tous nos sites sont optimisés pour le SEO dès leur conception. Nous intégrons les bonnes pratiques
                                    techniques (vitesse, mobile-friendly, balises) et pouvons vous accompagner avec une stratégie
                                    de référencement local pour {name} et le {dept_name}.
                                </div>
                            </div>
                        </div>
                        <div class="accordion-item border-0 shadow-sm">
                            <h3 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#faq5">
                                    Pourrai-je modifier mon site moi-même ?
                                </button>
                            </h3>
                            <div id="faq5" class="accordion-collapse collapse" data-bs-parent="#faqAccordion">
                                <div class="accordion-body text-muted">
                                    Absolument ! Nous développons nos sites avec des CMS intuitifs (WordPress, Prestashop) qui vous
                                    permettent de gérer facilement vos contenus. Une formation est incluse à la livraison du site.
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Section Secteurs d'Activité -->
    <section class="section-padding">
        <div class="container">
            <h2 class="section-title text-center mb-3">Secteurs d'Activité à {name}</h2>
            <p class="section-subtitle text-center text-muted mb-5">
                Nous accompagnons tous les professionnels du {dept_name}
            </p>
            <div class="row g-4">
                <div class="col-6 col-md-4 col-lg-2">
                    <div class="text-center p-3 bg-light rounded h-100">
                        <i class="bi bi-shop display-5 text-primary mb-2"></i>
                        <h4 class="h6 fw-bold">Commerce</h4>
                    </div>
                </div>
                <div class="col-6 col-md-4 col-lg-2">
                    <div class="text-center p-3 bg-light rounded h-100">
                        <i class="bi bi-building display-5 text-primary mb-2"></i>
                        <h4 class="h6 fw-bold">Immobilier</h4>
                    </div>
                </div>
                <div class="col-6 col-md-4 col-lg-2">
                    <div class="text-center p-3 bg-light rounded h-100">
                        <i class="bi bi-heart-pulse display-5 text-primary mb-2"></i>
                        <h4 class="h6 fw-bold">Santé</h4>
                    </div>
                </div>
                <div class="col-6 col-md-4 col-lg-2">
                    <div class="text-center p-3 bg-light rounded h-100">
                        <i class="bi bi-tools display-5 text-primary mb-2"></i>
                        <h4 class="h6 fw-bold">Artisanat</h4>
                    </div>
                </div>
                <div class="col-6 col-md-4 col-lg-2">
                    <div class="text-center p-3 bg-light rounded h-100">
                        <i class="bi bi-briefcase display-5 text-primary mb-2"></i>
                        <h4 class="h6 fw-bold">Services</h4>
                    </div>
                </div>
                <div class="col-6 col-md-4 col-lg-2">
                    <div class="text-center p-3 bg-light rounded h-100">
                        <i class="bi bi-cup-hot display-5 text-primary mb-2"></i>
                        <h4 class="h6 fw-bold">Restauration</h4>
                    </div>
                </div>
            </div>
        </div>
    </section>
{nearby_section}
    <!-- Section CTA -->
    <section class="cta-section section-padding bg-primary text-white">
        <div class="container text-center">
            <h2 class="display-6 fw-bold mb-4">Prêt à Lancer Votre Projet Web à {name} ?</h2>
            <p class="lead mb-4">
                Contactez notre équipe dès aujourd'hui pour un devis gratuit et personnalisé.
                Ensemble, donnons vie à votre présence en ligne dans le {dept_name} !
            </p>
            <div class="d-flex gap-3 justify-content-center flex-wrap">
                <a href="../index.html#contact" class="btn btn-light btn-lg px-5">
                    <i class="bi bi-envelope"></i> Demander un Devis
                </a>
                <a href="tel:+33641127926" class="btn btn-outline-light btn-lg px-5">
                    <i class="bi bi-telephone"></i> 06 41 12 79 26
                </a>
            </div>
        </div>
    </section>

    <footer class="footer bg-dark text-white py-5">
        <div class="container">
            <div class="row g-4">
                <div class="col-lg-4">
                    <h5 class="fw-bold mb-3"><i class="bi bi-globe2"></i> Agence Web France</h5>
                    <p class="text-white-50">
                        Votre partenaire de confiance pour tous vos projets web à {name} et partout en France.
                        Création de sites internet, e-commerce, référencement SEO.
                    </p>
                </div>
                <div class="col-lg-4">
                    <h5 class="fw-bold mb-3">Navigation</h5>
                    <ul class="list-unstyled">
                        <li class="mb-2"><a href="../index.html" class="text-white-50 text-decoration-none hover-link">Accueil</a></li>
                        <li class="mb-2"><a href="../index.html#services" class="text-white-50 text-decoration-none hover-link">Services</a></li>
                        <li class="mb-2"><a href="../index.html#annuaire" class="text-white-50 text-decoration-none hover-link">Annuaire</a></li>
                        <li class="mb-2"><a href="../index.html#contact" class="text-white-50 text-decoration-none hover-link">Contact</a></li>
                    </ul>
                </div>
                <div class="col-lg-4">
                    <h5 class="fw-bold mb-3">Contact</h5>
                    <ul class="list-unstyled text-white-50">
                        <li class="mb-2"><i class="bi bi-geo-alt me-2"></i>France</li>
                        <li class="mb-2"><a href="tel:+33641127926" class="text-white-50 text-decoration-none"><i class="bi bi-telephone me-2"></i>06 41 12 79 26</a></li>
                        <li class="mb-2"><a href="mailto:contact.capitainepub@gmail.com" class="text-white-50 text-decoration-none"><i class="bi bi-envelope me-2"></i>contact.capitainepub@gmail.com</a></li>
                    </ul>
                </div>
            </div>
            <hr class="my-4 bg-white opacity-25">
            <p class="text-center text-white-50 mb-0">&copy; 2024 Agence Web France - Agence Web {name} ({zip_code}). Tous droits réservés.</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="../script.js"></script>
</body>
</html>'''

def main():
    print("=" * 60)
    print("Génération des pages villes - Agence Web France")
    print("Version enrichie SEO avec villes aux alentours et EmailJS")
    print("=" * 60)

    # Créer le dossier de sortie
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\n✓ Dossier '{OUTPUT_DIR}/' créé")

    # Charger les villes
    with open(VILLES_JSON, 'r', encoding='utf-8') as f:
        villes = json.load(f)

    total = len(villes)
    print(f"✓ {total} villes chargées depuis {VILLES_JSON}")
    print("\nOrganisation des villes par département...")

    # Organiser par département pour les stats et les villes à proximité
    villes_by_dept = {}
    for ville in villes:
        dept = get_departement(ville["zip"])
        if dept not in villes_by_dept:
            villes_by_dept[dept] = []
        villes_by_dept[dept].append(ville)

    print(f"✓ {len(villes_by_dept)} départements identifiés")
    print("\nGénération des pages en cours...")

    for i, ville in enumerate(villes, 1):
        # Trouver les villes à proximité
        nearby_cities = find_nearby_cities(ville, villes, villes_by_dept, count=10)

        # Générer la page
        filename = f"agence-web-{ville['slug']}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)

        html_content = generate_page_html(ville, nearby_cities)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Afficher la progression
        if i % 1000 == 0 or i == total:
            percent = (i / total) * 100
            print(f"  [{i}/{total}] {percent:.1f}% - Dernière: {ville['name']}")

    # Générer le fichier JSON des départements pour la homepage
    dept_summary = []
    for dept, villes_dept in sorted(villes_by_dept.items()):
        dept_summary.append({
            "code": dept,
            "name": get_departement_name(dept),
            "count": len(villes_dept),
            "villes": [{"name": v["name"], "slug": v["slug"], "zip": v["zip"]} for v in villes_dept]
        })

    with open("departements.json", 'w', encoding='utf-8') as f:
        json.dump(dept_summary, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Fichier departements.json créé")
    print(f"\n{'=' * 60}")
    print(f"TERMINÉ !")
    print(f"- {total} pages générées dans /{OUTPUT_DIR}/")
    print(f"- {len(villes_by_dept)} départements")
    print(f"- Contenu SEO enrichi avec FAQ et secteurs")
    print(f"- Villes aux alentours ajoutées pour chaque page")
    print(f"- Google Maps intégré pour chaque ville")
    print(f"- EmailJS intégré pour les formulaires")
    print(f"- Coordonnées: 06 41 12 79 26 / contact.capitainepub@gmail.com")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
