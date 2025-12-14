#!/usr/bin/env python3
"""
Script de génération des pages départements pour l'annuaire Agence Web France
Génère une page HTML pour chaque département avec la liste de toutes ses villes
"""

import json
import os

def generate_dept_page(dept):
    """Génère le HTML pour une page département"""
    code = dept["code"]
    name = dept["name"]
    villes = dept["villes"]
    count = len(villes)

    # Générer la grille des villes
    villes_html = ""
    for v in sorted(villes, key=lambda x: x["name"]):
        villes_html += f'''
                <div class="col-6 col-md-4 col-lg-3">
                    <a href="../villes/agence-web-{v["slug"]}.html" class="ville-card">
                        <span class="ville-name">{v["name"]}</span>
                        <span class="ville-zip">{v["zip"]}</span>
                    </a>
                </div>'''

    return f'''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">

    <title>Agence Web {name} ({code}) - Création de Sites Internet</title>
    <meta name="description" content="Agence web dans le {name} ({code}). Création de sites internet et solutions digitales pour {count} villes du département. Devis gratuit.">
    <meta name="keywords" content="agence web {name}, création site internet {code}, développement web {name}">
    <meta name="author" content="Agence Web France">

    <meta property="og:type" content="website">
    <meta property="og:title" content="Agence Web {name} ({code}) - Toutes les villes">
    <meta property="og:description" content="Trouvez votre agence web dans le {name} - {count} villes couvertes">

    <link rel="canonical" href="https://www.agencewebfrance.fr/departements/annuaire-departement-{code}.html">

    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css">
    <link rel="stylesheet" href="../style.css">

    <style>
        .ville-card {{
            display: block;
            padding: 12px 15px;
            background: #f8f9fa;
            border-radius: 8px;
            text-decoration: none;
            color: #212529;
            transition: all 0.3s ease;
            margin-bottom: 10px;
        }}
        .ville-card:hover {{
            background: #0d6efd;
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
        }}
        .ville-card:hover .ville-zip {{
            color: rgba(255,255,255,0.8);
        }}
        .ville-name {{
            display: block;
            font-weight: 500;
        }}
        .ville-zip {{
            font-size: 0.85rem;
            color: #6c757d;
        }}
        .dept-stats {{
            background: linear-gradient(135deg, #0d6efd 0%, #0a58ca 100%);
            color: white;
            border-radius: 15px;
            padding: 30px;
        }}
        .search-filter {{
            position: sticky;
            top: 80px;
            z-index: 100;
            background: white;
            padding: 20px 0;
            margin-bottom: 20px;
            border-bottom: 1px solid #e9ecef;
        }}
    </style>
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

    <section class="section-padding" style="padding-top: 120px; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
        <div class="container">
            <nav aria-label="breadcrumb" class="mb-4">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="../index.html">Accueil</a></li>
                    <li class="breadcrumb-item"><a href="../index.html#annuaire">Annuaire</a></li>
                    <li class="breadcrumb-item active" aria-current="page">{name} ({code})</li>
                </ol>
            </nav>

            <div class="row align-items-center mb-5">
                <div class="col-lg-8">
                    <h1 class="display-5 fw-bold mb-3">
                        <i class="bi bi-geo-alt-fill text-primary"></i>
                        Agence Web dans le <span class="text-primary">{name}</span>
                    </h1>
                    <p class="lead text-muted">
                        Découvrez nos services de création de sites internet et solutions digitales
                        dans les {count} villes du département {name} ({code}).
                    </p>
                </div>
                <div class="col-lg-4">
                    <div class="dept-stats text-center">
                        <div class="display-4 fw-bold">{count}</div>
                        <div>villes couvertes</div>
                        <hr class="my-3 opacity-50">
                        <div class="h5 mb-0">{name} ({code})</div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="py-4">
        <div class="container">
            <div class="search-filter">
                <div class="row justify-content-center">
                    <div class="col-lg-6">
                        <div class="input-group">
                            <span class="input-group-text bg-white"><i class="bi bi-search"></i></span>
                            <input type="text" id="filterVilles" class="form-control"
                                   placeholder="Filtrer les villes du {name}...">
                        </div>
                    </div>
                </div>
            </div>

            <h2 class="h4 fw-bold mb-4">
                <i class="bi bi-building text-primary"></i>
                Toutes les villes du {name}
            </h2>

            <div class="row g-3" id="villesGrid">
                {villes_html}
            </div>
        </div>
    </section>

    <section class="cta-section section-padding bg-primary text-white mt-5">
        <div class="container text-center">
            <h2 class="display-6 fw-bold mb-4">Besoin d'une agence web dans le {name} ?</h2>
            <p class="lead mb-4">Contactez-nous pour un devis gratuit et personnalisé.</p>
            <a href="../index.html#contact" class="btn btn-light btn-lg px-5">
                <i class="bi bi-envelope"></i> Demander un Devis
            </a>
        </div>
    </section>

    <footer class="footer bg-dark text-white py-5">
        <div class="container">
            <div class="row g-4">
                <div class="col-lg-4">
                    <h5 class="fw-bold mb-3"><i class="bi bi-globe2"></i> Agence Web France</h5>
                    <p class="text-white-50">
                        Votre partenaire de confiance pour tous vos projets web dans le {name} et partout en France.
                    </p>
                </div>
                <div class="col-lg-4">
                    <h5 class="fw-bold mb-3">Navigation</h5>
                    <ul class="list-unstyled">
                        <li class="mb-2"><a href="../index.html" class="text-white-50 text-decoration-none">Accueil</a></li>
                        <li class="mb-2"><a href="../index.html#services" class="text-white-50 text-decoration-none">Services</a></li>
                        <li class="mb-2"><a href="../index.html#annuaire" class="text-white-50 text-decoration-none">Annuaire</a></li>
                        <li class="mb-2"><a href="../index.html#contact" class="text-white-50 text-decoration-none">Contact</a></li>
                    </ul>
                </div>
                <div class="col-lg-4">
                    <h5 class="fw-bold mb-3">Contact</h5>
                    <ul class="list-unstyled text-white-50">
                        <li class="mb-2"><i class="bi bi-geo-alt"></i> France</li>
                        <li class="mb-2"><a href="tel:+33641127926" class="text-white-50 text-decoration-none"><i class="bi bi-telephone"></i> 06 41 12 79 26</a></li>
                        <li class="mb-2"><a href="mailto:contact.capitainepub@gmail.com" class="text-white-50 text-decoration-none"><i class="bi bi-envelope"></i> contact.capitainepub@gmail.com</a></li>
                    </ul>
                </div>
            </div>
            <hr class="my-4 bg-white opacity-25">
            <p class="text-center text-white-50 mb-0">
                &copy; 2024 Agence Web France - Annuaire {name}. Tous droits réservés.
            </p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Filtrage des villes
        document.getElementById('filterVilles').addEventListener('input', function() {{
            const filter = this.value.toLowerCase();
            const cards = document.querySelectorAll('#villesGrid > div');

            cards.forEach(card => {{
                const name = card.querySelector('.ville-name').textContent.toLowerCase();
                const zip = card.querySelector('.ville-zip').textContent.toLowerCase();

                if (name.includes(filter) || zip.includes(filter)) {{
                    card.style.display = '';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }});
    </script>
</body>
</html>'''

def main():
    print("=" * 60)
    print("Génération des pages départements - Agence Web France")
    print("=" * 60)

    # Charger les départements
    with open('departements.json', 'r', encoding='utf-8') as f:
        departements = json.load(f)

    print(f"\n✓ {len(departements)} départements chargés")
    print("\nGénération des pages en cours...")

    # Créer le dossier departements si nécessaire
    os.makedirs('departements', exist_ok=True)

    for i, dept in enumerate(departements, 1):
        filename = f"departements/annuaire-departement-{dept['code']}.html"

        html_content = generate_dept_page(dept)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"  [{i}/{len(departements)}] {filename} ({len(dept['villes'])} villes)")

    print(f"\n{'=' * 60}")
    print(f"TERMINÉ !")
    print(f"- {len(departements)} pages départements générées")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
