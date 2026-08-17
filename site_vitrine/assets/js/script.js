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
});
