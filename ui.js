(function () {
  function initTheme() {
    var root = document.documentElement;
    var btn = document.getElementById('theme-toggle');
    function applyTheme(theme) {
      root.setAttribute('data-theme', theme);
      try {
        localStorage.setItem('theme', theme);
      } catch (e) {}
      if (btn) {
        btn.setAttribute(
          'aria-label',
          theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
        );
      }
      var meta = document.querySelector('meta[name="theme-color"]');
      if (meta) {
        meta.setAttribute('content', theme === 'dark' ? '#0F172A' : '#2563EB');
      }
    }
    function currentTheme() {
      return root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    }
    if (!root.getAttribute('data-theme')) {
      applyTheme('light');
    }
    if (btn) {
      btn.addEventListener('click', function () {
        applyTheme(currentTheme() === 'dark' ? 'light' : 'dark');
      });
    }
  }

  initTheme();

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

  function loadAnalytics() {
    var id = window.SITE_GA4;
    if (!id) return;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () {
      window.dataLayer.push(arguments);
    };
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(id);
    document.head.appendChild(s);
    window.gtag('js', new Date());
    window.gtag('config', id, { anonymize_ip: true });
  }

  function initCookieConsent() {
    var key = 'cookie-consent';
    if (localStorage.getItem(key) === 'accepted') {
      loadAnalytics();
      return;
    }
    if (localStorage.getItem(key) === 'rejected') return;

    var bar = document.createElement('div');
    bar.className = 'cookie-consent';
    bar.setAttribute('role', 'dialog');
    bar.setAttribute('aria-label', 'Cookie consent');
    bar.innerHTML =
      '<div class="cookie-consent-inner"><p>We use optional cookies for analytics and advertising to improve tutorials. See our <a href="privacy.html">Privacy Policy</a>.</p><div class="cookie-actions"><button type="button" class="btn btn-secondary cookie-reject">Reject optional</button><button type="button" class="btn btn-primary cookie-accept">Accept</button></div></div>';
    document.body.appendChild(bar);

    bar.querySelector('.cookie-accept').addEventListener('click', function () {
      localStorage.setItem(key, 'accepted');
      bar.remove();
      loadAnalytics();
    });
    bar.querySelector('.cookie-reject').addEventListener('click', function () {
      localStorage.setItem(key, 'rejected');
      bar.remove();
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

  var homeGrid = document.getElementById('home-grid');
  var homeMore = document.getElementById('home-load-more');
  var homeWrap = document.getElementById('home-more-wrap');
  if (homeGrid && homeMore) {
    var initial = parseInt(homeGrid.dataset.initial || '6', 10);
    var cards = homeGrid.querySelectorAll('.project-card');
    function updateHomeVisible() {
      var expanded = homeGrid.classList.contains('is-expanded');
      cards.forEach(function (card, i) {
        card.classList.toggle('home-hidden', !expanded && i >= initial);
      });
      if (homeWrap) {
        homeWrap.style.display = expanded || cards.length <= initial ? 'none' : '';
      }
    }
    updateHomeVisible();
    homeMore.addEventListener('click', function () {
      homeGrid.classList.add('is-expanded');
      updateHomeVisible();
    });
  }

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
