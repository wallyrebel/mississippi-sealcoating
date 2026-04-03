/* ============================================
   D&Z SEALCOATING - INTERACTIVE SCRIPTS
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

    // ====== NAVBAR SCROLL EFFECT ======
    const navbar = document.getElementById('navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        if (currentScroll > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        lastScroll = currentScroll;
    });

    // ====== MOBILE NAV TOGGLE ======
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    navToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        navToggle.classList.toggle('active');
    });

    // Close mobile nav on link click
    navLinks.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            navLinks.classList.remove('active');
            navToggle.classList.remove('active');
        });
    });

    // ====== SMOOTH SCROLL ======
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });

    // ====== SCROLL REVEAL ANIMATION ======
    const revealElements = document.querySelectorAll(
        '.service-card, .why-card, .testimonial-card, .process-step, .benefit, ' +
        '.area-card, .contact-card, .about-content, .about-image, ' +
        '.split-content, .split-image, .gallery-item, .section-header'
    );

    revealElements.forEach(el => el.classList.add('reveal'));

    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                revealObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => revealObserver.observe(el));

    // ====== COUNTER ANIMATION ======
    const counters = document.querySelectorAll('.stat-number');
    let countersAnimated = false;

    const animateCounters = () => {
        if (countersAnimated) return;
        countersAnimated = true;

        counters.forEach(counter => {
            const target = parseInt(counter.dataset.target);
            const duration = 2000;
            const start = performance.now();

            const updateCounter = (timestamp) => {
                const elapsed = timestamp - start;
                const progress = Math.min(elapsed / duration, 1);
                // Ease out cubic
                const eased = 1 - Math.pow(1 - progress, 3);
                counter.textContent = Math.round(target * eased);

                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target;
                }
            };

            requestAnimationFrame(updateCounter);
        });
    };

    const statsSection = document.querySelector('.hero-stats');
    if (statsSection) {
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
    if (particlesContainer) {
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

        // Add particle animation keyframes
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

    // ====== ACTIVE NAV LINK ON SCROLL ======
    const sections = document.querySelectorAll('section[id], header[id]');
    const navLinksAll = document.querySelectorAll('.nav-links a[href^="#"]');

    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop - 100;
            if (window.pageYOffset >= sectionTop) {
                current = section.getAttribute('id');
            }
        });

        navLinksAll.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });

    // ====== CONTACT FORM (demo handler) ======
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();

            const btn = this.querySelector('button[type="submit"]');
            const originalText = btn.textContent;
            btn.textContent = 'Sending...';
            btn.disabled = true;

            // Simulate form submission
            setTimeout(() => {
                btn.textContent = 'Request Sent!';
                btn.style.background = '#22c55e';

                setTimeout(() => {
                    btn.textContent = originalText;
                    btn.style.background = '';
                    btn.disabled = false;
                    contactForm.reset();
                }, 3000);
            }, 1500);
        });
    }

    // ====== NAVBAR TOGGLE ANIMATION ======
    const style2 = document.createElement('style');
    style2.textContent = `
        .nav-toggle.active span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
        .nav-toggle.active span:nth-child(2) { opacity: 0; }
        .nav-toggle.active span:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); }
        .nav-links a.active { color: var(--gold) !important; }
    `;
    document.head.appendChild(style2);
});
