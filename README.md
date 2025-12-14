# 🌐 Agence Web France - Site Vitrine

Site web professionnel pour une agence web française, développé avec HTML5, CSS3 et JavaScript vanilla.

## 📋 Description

Site vitrine moderne et responsive pour présenter les services d'une agence web spécialisée dans la création de sites internet et les solutions digitales. Le site met l'accent sur le SEO, la performance et l'expérience utilisateur.

## ✨ Fonctionnalités

- **Design Responsive** : Adapté à tous les appareils (mobile-first)
- **Header Sticky** : Navigation fixe au scroll
- **Animations CSS** : Effets de hover et transitions fluides
- **SEO Optimisé** : Structure HTML sémantique, meta tags complets
- **Formulaire de Contact** : Validation côté client
- **Smooth Scroll** : Navigation fluide entre les sections
- **Performance** : Code optimisé et léger

## 🛠️ Technologies Utilisées

- **HTML5** : Structure sémantique
- **CSS3** : Styles personnalisés et animations
- **JavaScript (Vanilla)** : Interactions dynamiques
- **Bootstrap 5.3.2** : Framework CSS (via CDN)
- **Bootstrap Icons** : Icônes (via CDN)

## 📁 Structure du Projet

```
SITE-HTML-TEST/
│
├── index.html              # Page principale
├── style.css               # Styles personnalisés (racine)
├── script.js               # Scripts JavaScript (racine)
├── README.md               # Documentation
│
└── assets/
    ├── css/
    │   └── style.css       # Styles (copie dans assets)
    ├── js/
    │   └── script.js       # Scripts (copie dans assets)
    └── img/
        └── (images à ajouter)
```

## 🚀 Installation et Utilisation

### Prérequis

Aucun ! Le site fonctionne de manière autonome avec les CDN Bootstrap.

### Démarrage

1. Cloner le dépôt :
```bash
git clone https://github.com/up2techapp/SITE-HTML-TEST.git
```

2. Ouvrir `index.html` dans votre navigateur préféré

Ou utiliser un serveur local :
```bash
# Avec Python 3
python -m http.server 8000

# Avec Node.js (http-server)
npx http-server

# Avec PHP
php -S localhost:8000
```

3. Visiter : `http://localhost:8000`

## 📱 Sections du Site

1. **Home** : Page d'accueil avec présentation principale
2. **Services** : Présentation des services (Design, Développement, SEO, etc.)
3. **À Propos** : Informations sur l'agence et statistiques
4. **Portfolio** : Exemples de réalisations
5. **Contact** : Formulaire de contact et informations

## 🎨 Personnalisation

### Couleurs

Les couleurs principales sont définies dans `style.css` :

```css
:root {
    --primary-color: #0d6efd;
    --secondary-color: #6c757d;
    --dark-color: #212529;
    --light-color: #f8f9fa;
}
```

### Contenu

Modifier le contenu directement dans `index.html` :
- Textes : Sections HTML
- Images : Ajouter dans `/assets/img/`
- Styles : Fichier `style.css`

## 🔧 Fonctionnalités JavaScript

- **Scroll Effects** : Header sticky et bouton retour en haut
- **Smooth Scroll** : Navigation fluide entre sections
- **Navbar Highlight** : Mise en surbrillance du lien actif
- **Form Validation** : Validation du formulaire de contact
- **Animations** : Animations au scroll avec Intersection Observer
- **Notifications** : Système de toast pour les messages

## 📊 SEO

Le site est optimisé pour le référencement :

- Meta tags complets (title, description, keywords)
- Structure HTML sémantique (header, nav, main, section, footer)
- Headings hiérarchiques (H1, H2, H3)
- Open Graph tags pour les réseaux sociaux
- URLs propres et navigation claire

## 🌍 Compatibilité

- ✅ Chrome (dernières versions)
- ✅ Firefox (dernières versions)
- ✅ Safari (dernières versions)
- ✅ Edge (dernières versions)
- ✅ Mobile (iOS & Android)

## 📈 Performance

- Temps de chargement optimisé
- CSS et JS minifiables pour la production
- Utilisation de CDN pour Bootstrap (cache partagé)
- Images optimisables (à ajouter)

## 🔒 Sécurité

- Validation des formulaires côté client
- Pas de dépendances vulnérables (vanilla JS)
- HTTPS recommandé pour la production

## 📝 À Faire (Améliorations Futures)

- [ ] Ajouter de vraies images dans `/assets/img/`
- [ ] Implémenter l'envoi réel du formulaire (backend)
- [ ] Ajouter Google Analytics
- [ ] Optimiser les images (WebP, lazy loading)
- [ ] Ajouter un sitemap.xml
- [ ] Mettre en place un système de blog
- [ ] Ajouter des animations plus avancées

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit vos changements (`git commit -m 'Ajout d'une fonctionnalité'`)
4. Push vers la branche (`git push origin feature/amelioration`)
5. Ouvrir une Pull Request

## 📄 Licence

Ce projet est libre d'utilisation pour vos projets personnels et commerciaux.

## 👤 Auteur

**Agence Web France**

- Site web : [À venir]
- Email : contact@agencewebfrance.fr
- GitHub : [@up2techapp](https://github.com/up2techapp)

## 🙏 Remerciements

- Bootstrap pour le framework CSS
- Bootstrap Icons pour les icônes
- La communauté open source

---

**Made with ❤️ in France** 🇫🇷
