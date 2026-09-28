/* ============================================
   D&Z SEALCOATING - INTERACTIVE SCRIPTS
   Shared by the homepage and all generated pages.
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // ====== NAVBAR SCROLL EFFECT ======
    const navbar = document.getElementById('navbar');
    const onScroll = () => {
        if (navbar) navbar.classList.toggle('scrolled', window.pageYOffset > 50);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();

    // ====== MOBILE NAV TOGGLE ======
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');
    const closeNav = () => {
        navLinks.classList.remove('active');
        navToggle.classList.remove('active');
        navToggle.setAttribute('aria-expanded', 'false');
    };

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            const open = navLinks.classList.toggle('active');
            navToggle.classList.toggle('active', open);
            navToggle.setAttribute('aria-expanded', String(open));
        });
        navLinks.querySelectorAll('a').forEach(link => link.addEventListener('click', closeNav));
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') closeNav();
        });
    }

    // ====== SMOOTH SCROLL (same-page links, incl. "/#section" on the homepage) ======
    document.querySelectorAll('a[href*="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            if (this.pathname !== window.location.pathname || !this.hash || this.hash.length < 2) return;
            const target = document.getElementById(this.hash.slice(1));
            if (!target) return;
            e.preventDefault();
            target.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'start' });
            history.pushState(null, '', this.hash);
        });
    });

    // ====== SCROLL REVEAL ANIMATION ======
    if (!reduceMotion && 'IntersectionObserver' in window) {
        const revealElements = document.querySelectorAll(
            '.service-card, .why-card, .testimonial-card, .process-step, .benefit, ' +
            '.area-card, .contact-card, .about-content, .about-image, ' +
            '.split-content, .split-image, .gallery-item, .section-header, .faq-item, .checklist-card'
        );
        revealElements.forEach(el => el.classList.add('reveal'));

        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        revealElements.forEach(el => revealObserver.observe(el));
    }

    // ====== COUNTER ANIMATION ======
    const counters = document.querySelectorAll('.stat-number');
    const statsSection = document.querySelector('.hero-stats');
    if (statsSection && counters.length && !reduceMotion && 'IntersectionObserver' in window) {
        const animateCounters = () => {
            counters.forEach(counter => {
                const target = parseInt(counter.dataset.target, 10);
                const duration = 2000;
                const start = performance.now();
                const updateCounter = (timestamp) => {
                    const progress = Math.min((timestamp - start) / duration, 1);
                    const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
                    counter.textContent = Math.round(target * eased);
                    if (progress < 1) requestAnimationFrame(updateCounter);
                };
                requestAnimationFrame(updateCounter);
            });
        };
        const statsObserver = new IntersectionObserver((entries) => {
            if (entries[0].isIntersecting) {
                animateCounters();
                statsObserver.disconnect();
            }
        }, { threshold: 0.5 });
        statsObserver.observe(statsSection);
    }

    // ====== HERO PARTICLES ======
    const particlesContainer = document.getElementById('particles');
    if (particlesContainer && !reduceMotion) {
        for (let i = 0; i < 30; i++) {
            const particle = document.createElement('div');
            particle.style.cssText = `
                position: absolute;
                width: ${Math.random() * 3 + 1}px;
                height: ${Math.random() * 3 + 1}px;
                background: rgba(201, 168, 76, ${Math.random() * 0.3 + 0.05});
                border-radius: 50%;
                left: ${Math.random() * 100}%;
                top: ${Math.random() * 100}%;
                animation: particleFloat ${Math.random() * 8 + 6}s ease-in-out infinite;
                animation-delay: ${Math.random() * 4}s;
            `;
            particlesContainer.appendChild(particle);
        }

        const style = document.createElement('style');
        style.textContent = `
            @keyframes particleFloat {
                0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.3; }
                25% { transform: translate(${Math.random() * 60 - 30}px, -${Math.random() * 40 + 20}px) scale(1.2); opacity: 0.6; }
                50% { transform: translate(${Math.random() * 40 - 20}px, -${Math.random() * 60 + 30}px) scale(0.8); opacity: 0.2; }
                75% { transform: translate(-${Math.random() * 30 + 10}px, -${Math.random() * 20 + 10}px) scale(1.1); opacity: 0.5; }
            }
        `;
        document.head.appendChild(style);
    }

    // ====== ACTIVE NAV LINK ON SCROLL (homepage sections) ======
    const sectionLinks = document.querySelectorAll('.nav-links a[href^="/#"]');
    if (sectionLinks.length && window.location.pathname === '/') {
        const sections = document.querySelectorAll('section[id], header[id]');
        window.addEventListener('scroll', () => {
            let current = '';
            sections.forEach(section => {
                if (window.pageYOffset >= section.offsetTop - 100) current = section.id;
            });
            sectionLinks.forEach(link => {
                link.classList.toggle('active', link.getAttribute('href') === `/#${current}`);
            });
        }, { passive: true });
    }

    // ====== CONTACT FORM ======
    // No backend: compose an email with the visitor's details so the request
    // actually reaches the business instead of silently disappearing.
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();
            if (!this.reportValidity()) return;

            const data = new FormData(this);
            const get = (k) => (data.get(k) || '').toString().trim();
            const name = `${get('firstName')} ${get('lastName')}`.trim();
            const subject = `Free estimate request - ${get('serviceType') || 'Asphalt services'}${get('city') ? ' - ' + get('city') : ''}`;
            const body = [
                `Name: ${name}`,
                `Email: ${get('email')}`,
                `Phone: ${get('phone')}`,
                `City/Town: ${get('city')}`,
                `Service: ${get('serviceType')}`,
                `Property type: ${get('propertyType')}`,
                '',
                'Project details:',
                get('message'),
            ].join('\n');

            const to = this.dataset.email;
            window.location.href = `mailto:${to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

            const note = document.getElementById('formNote');
            if (note) {
                note.innerHTML = 'Your email app should open with your request ready to send. ' +
                    'If it didn\'t, call <a href="tel:+16625873525">(662) 587-3525</a> or ' +
                    '<a href="https://dandzsealcoating.com/" target="_blank" rel="noopener">request a quote online</a>.';
            }
        });
    }

    // ====== FOOTER YEAR ======
    document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
});
