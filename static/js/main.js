document.addEventListener('DOMContentLoaded', function () {
    // Toast auto-dismiss
    var msgs = document.querySelectorAll('.msg');
    msgs.forEach(function (el) {
        setTimeout(function () {
            el.style.animation = 'toastOut .3s ease forwards';
            setTimeout(function () { el.remove(); }, 300);
        }, 3500);
    });

    // Navbar scroll shadow
    var navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            navbar.classList.toggle('scrolled', window.scrollY > 10);
        });
    }

    // Intersection Observer for product card fade-in
    var cards = document.querySelectorAll('.product-card');
    if ('IntersectionObserver' in window && cards.length) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    var delay = parseInt(entry.target.dataset.delay || 0) * 80;
                    setTimeout(function () {
                        entry.target.classList.add('visible');
                    }, delay);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        cards.forEach(function (c) { observer.observe(c); });
    } else {
        cards.forEach(function (c) { c.classList.add('visible'); });
    }
});
