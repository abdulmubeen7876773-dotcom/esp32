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

  function grantConsent() {
    if (typeof window.gtag !== 'function') return;
    window.gtag('consent', 'update', {
      'analytics_storage':  'granted',
      'ad_storage':         'denied',
      'ad_user_data':       'denied',
      'ad_personalization': 'denied'
    });
    /* Manual page_view for users who accept mid-session after the queued
       hit already fired with denied consent */
    window.gtag('event', 'page_view', {
      'page_location': window.location.href,
      'page_title':    document.title
    });
  }

  function denyConsent() {
    if (typeof window.gtag !== 'function') return;
    window.gtag('consent', 'update', {
      'analytics_storage':  'denied',
      'ad_storage':         'denied',
      'ad_user_data':       'denied',
      'ad_personalization': 'denied'
    });
  }

  function initCookieConsent() {
    var key = 'cookie-consent';
    /* Returning visitors — consent already set via the inline head script;
       just hide the bar and do nothing */
    if (localStorage.getItem(key) === 'accepted') return;
    if (localStorage.getItem(key) === 'rejected') return;

    var bar = document.createElement('div');
    bar.className = 'cookie-consent';
    bar.setAttribute('role', 'dialog');
    bar.setAttribute('aria-label', 'Cookie consent');
    bar.innerHTML =
      '<div class="cookie-consent-inner"><p>We use optional cookies for analytics to improve tutorials. See our <a href="/privacy/">Privacy Policy</a>.</p><div class="cookie-actions"><button type="button" class="btn btn-secondary cookie-reject">Reject optional</button><button type="button" class="btn btn-primary cookie-accept">Accept</button></div></div>';
    document.body.appendChild(bar);

    bar.querySelector('.cookie-accept').addEventListener('click', function () {
      localStorage.setItem(key, 'accepted');
      bar.remove();
      grantConsent();
    });
    bar.querySelector('.cookie-reject').addEventListener('click', function () {
      localStorage.setItem(key, 'rejected');
      bar.remove();
      denyConsent();
    });
  }

  initCookieConsent();

  var btt = document.createElement('button');
  btt.type = 'button';
  btt.className = 'back-to-top';
  btt.setAttribute('aria-label', 'Back to top');
  btt.textContent = '↑';
  document.body.appendChild(btt);
  window.addEventListener(
    'scroll',
    function () {
      btt.classList.toggle('visible', window.scrollY > 320);
    },
    { passive: true }
  );
  btt.addEventListener('click', function () {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  document.querySelectorAll('.carousel-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var id = 'carousel-' + btn.dataset.carousel;
      var track = document.getElementById(id);
      if (!track) return;
      var dir = parseInt(btn.dataset.dir || '1', 10);
      var amount = Math.max(track.clientWidth * 0.75, 240);
      track.scrollBy({ left: dir * amount, behavior: 'smooth' });
    });
  });

  var searchOpen = document.getElementById('search-open');
  var searchOverlay = document.getElementById('search-overlay');
  if (searchOpen && searchOverlay) {
    var searchInput = document.getElementById('global-search');
    searchOpen.addEventListener('click', function () {
      searchOverlay.hidden = false;
      document.body.style.overflow = 'hidden';
      if (searchInput) searchInput.focus();
    });
    searchOverlay.querySelectorAll('[data-close-search]').forEach(function (el) {
      el.addEventListener('click', function () {
        searchOverlay.hidden = true;
        document.body.style.overflow = '';
      });
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !searchOverlay.hidden) {
        searchOverlay.hidden = true;
        document.body.style.overflow = '';
      }
    });
  }
})();
