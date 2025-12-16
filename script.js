/* ========================================
   SEKSITREFFIT SUOMESSA - JavaScript
   Site de rencontre adulte en Finlande
======================================== */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initSearchAutocomplete();
    initCityFilter();
    initSmoothScroll();
    initAnimations();
    initNavbarScroll();
});

/* ========================================
   SEARCH AUTOCOMPLETE
======================================== */
function initSearchAutocomplete() {
    const searchInput = document.getElementById('citySearch');
    const searchResults = document.getElementById('searchResults');

    if (!searchInput || !searchResults) return;

    // Get cities data from the page
    let citiesData = [];
    if (typeof window.citiesData !== 'undefined') {
        citiesData = window.citiesData;
    }

    searchInput.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();

        if (query.length < 2) {
            searchResults.classList.remove('show');
            return;
        }

        const matches = citiesData.filter(city =>
            city.name.toLowerCase().includes(query)
        ).slice(0, 10);

        if (matches.length > 0) {
            searchResults.innerHTML = matches.map(city =>
                `<a href="/villes/${city.slug}.html">
                    <i class="bi bi-geo-alt me-2"></i>${city.name}
                </a>`
            ).join('');
            searchResults.classList.add('show');
        } else {
            searchResults.innerHTML = '<div class="p-3 text-muted">Ei tuloksia</div>';
            searchResults.classList.add('show');
        }
    });

    // Close results when clicking outside
    document.addEventListener('click', function(e) {
        if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
            searchResults.classList.remove('show');
        }
    });

    // Keyboard navigation
    searchInput.addEventListener('keydown', function(e) {
        const items = searchResults.querySelectorAll('a');
        const currentActive = searchResults.querySelector('a.active');
        let index = Array.from(items).indexOf(currentActive);

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (currentActive) currentActive.classList.remove('active');
            index = (index + 1) % items.length;
            items[index]?.classList.add('active');
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (currentActive) currentActive.classList.remove('active');
            index = index <= 0 ? items.length - 1 : index - 1;
            items[index]?.classList.add('active');
        } else if (e.key === 'Enter' && currentActive) {
            e.preventDefault();
            window.location.href = currentActive.href;
        }
    });
}

/* ========================================
   CITY FILTER (Region Pages)
======================================== */
function initCityFilter() {
    const filterInput = document.getElementById('cityFilter');

    if (!filterInput) return;

    filterInput.addEventListener('input', function() {
        const query = this.value.toLowerCase().trim();
        const cityCards = document.querySelectorAll('.city-list-card');

        cityCards.forEach(card => {
            const cityName = card.querySelector('h5').textContent.toLowerCase();
            if (cityName.includes(query)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}

/* ========================================
   SMOOTH SCROLL
======================================== */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/* ========================================
   SCROLL ANIMATIONS
======================================== */
function initAnimations() {
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fadeInUp');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements with animation class
    document.querySelectorAll('.animate-on-scroll').forEach(el => {
        observer.observe(el);
    });
}

/* ========================================
   NAVBAR SCROLL EFFECT
======================================== */
function initNavbarScroll() {
    const navbar = document.querySelector('.navbar');

    if (!navbar) return;

    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
            navbar.style.padding = '0.5rem 0';
        } else {
            navbar.classList.remove('navbar-scrolled');
            navbar.style.padding = '1rem 0';
        }
    });
}

/* ========================================
   MODAL FUNCTIONS
======================================== */
function showCitiesModal(regionName, cities) {
    const modalTitle = document.getElementById('citiesModalLabel');
    const modalBody = document.getElementById('citiesModalBody');

    if (modalTitle && modalBody) {
        modalTitle.textContent = `Kaupungit: ${regionName}`;
        modalBody.innerHTML = cities.map(city =>
            `<a href="/villes/${city.slug}.html" class="dept-link">
                <i class="bi bi-geo-alt me-1"></i>${city.name}
            </a>`
        ).join('');

        const modal = new bootstrap.Modal(document.getElementById('citiesModal'));
        modal.show();
    }
}

/* ========================================
   STATISTICS COUNTER ANIMATION
======================================== */
function animateCounters() {
    const counters = document.querySelectorAll('.stat-counter');

    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const updateCounter = () => {
            current += step;
            if (current < target) {
                counter.textContent = Math.floor(current).toLocaleString('fi-FI');
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target.toLocaleString('fi-FI');
            }
        };

        updateCounter();
    });
}

/* ========================================
   UTILITY FUNCTIONS
======================================== */

// Format number with Finnish locale
function formatNumber(num) {
    return num.toLocaleString('fi-FI');
}

// Debounce function for search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Check if element is in viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

/* ========================================
   LAZY LOADING IMAGES
======================================== */
function initLazyLoading() {
    const lazyImages = document.querySelectorAll('img[data-src]');

    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.removeAttribute('data-src');
                imageObserver.unobserve(img);
            }
        });
    });

    lazyImages.forEach(img => imageObserver.observe(img));
}

/* ========================================
   COOKIE CONSENT (GDPR)
======================================== */
function initCookieConsent() {
    const consent = localStorage.getItem('cookieConsent');

    if (!consent) {
        const banner = document.getElementById('cookieBanner');
        if (banner) {
            banner.style.display = 'block';
        }
    }
}

function acceptCookies() {
    localStorage.setItem('cookieConsent', 'accepted');
    const banner = document.getElementById('cookieBanner');
    if (banner) {
        banner.style.display = 'none';
    }
}

/* ========================================
   FORM VALIDATION
======================================== */
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;

    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required]');

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }

        if (input.type === 'email' && !validateEmail(input.value)) {
            input.classList.add('is-invalid');
            isValid = false;
        }
    });

    return isValid;
}
