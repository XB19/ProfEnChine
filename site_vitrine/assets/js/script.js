// =========================================================
// LE PROF EN CHINE — SITE VITRINE
// =========================================================

document.addEventListener("DOMContentLoaded", function () {

    // ---------------------------------------------------
    // Menu mobile
    // ---------------------------------------------------
    var navToggle = document.getElementById("navToggle");
    var navLinks = document.getElementById("navLinks");

    if (navToggle && navLinks) {
        navToggle.addEventListener("click", function () {
            var isOpen = navLinks.classList.toggle("open");
            navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
        });

        navLinks.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", function () {
                navLinks.classList.remove("open");
                navToggle.setAttribute("aria-expanded", "false");
            });
        });
    }

    // ---------------------------------------------------
    // Année dans le footer
    // ---------------------------------------------------
    var yearEl = document.getElementById("year");
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }

    // ---------------------------------------------------
    // Apparition au scroll
    // ---------------------------------------------------
    var reveals = document.querySelectorAll(".reveal");

    if ("IntersectionObserver" in window && reveals.length) {
        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        observer.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.15 }
        );

        reveals.forEach(function (el) {
            observer.observe(el);
        });
    } else {
        reveals.forEach(function (el) {
            el.classList.add("is-visible");
        });
    }

    var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // ---------------------------------------------------
    // En-tête : ombre progressive + lien de nav actif
    // ---------------------------------------------------
    var header = document.querySelector(".site-header");
    var sections = document.querySelectorAll("section[id]");
    var navAnchors = document.querySelectorAll(".nav-links a");

    function onScroll() {
        if (header) {
            header.classList.toggle("is-scrolled", window.scrollY > 12);
        }

        var current = "";
        sections.forEach(function (section) {
            var top = section.offsetTop - 130;
            if (window.scrollY >= top) {
                current = section.id;
            }
        });

        navAnchors.forEach(function (link) {
            link.classList.toggle("active", link.getAttribute("href") === "#" + current);
        });
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();

    // ---------------------------------------------------
    // Parallax discret sur le fond du hero
    // ---------------------------------------------------
    var hero = document.querySelector(".hero");

    if (hero && !reducedMotion) {
        window.addEventListener(
            "scroll",
            function () {
                var offset = Math.min(window.scrollY, 600);
                hero.style.backgroundPosition = "center " + (offset * 0.25) + "px";
            },
            { passive: true }
        );
    }
});
