(function () {
  function showReveal(el) {
    el.classList.add('is-visible');
  }

  function showInViewReveals() {
    document.querySelectorAll('.reveal:not(.is-visible)').forEach(function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight && rect.bottom > 0) {
        showReveal(el);
      }
    });
  }

  function initReveals() {
    var reveals = document.querySelectorAll('.reveal');
    if (!reveals.length) return;

    if (!('IntersectionObserver' in window)) {
      reveals.forEach(showReveal);
      return;
    }

    var revealObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            showReveal(entry.target);
            revealObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.05, rootMargin: '0px 0px -20px 0px' }
    );

    reveals.forEach(function (el) {
      if (!el.classList.contains('is-visible')) {
        revealObserver.observe(el);
      }
    });

    showInViewReveals();
    window.addEventListener('load', showInViewReveals);
    setTimeout(function () {
      reveals.forEach(showReveal);
    }, 1200);
  }

  initReveals();

  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.top-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        nav.classList.remove('is-open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  var sticky = document.querySelector('.site-nav-sticky');
  if (sticky) {
    var onScroll = function () {
      sticky.classList.toggle('is-scrolled', window.scrollY > 8);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }
})();
