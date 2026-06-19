/* ESP32 Engine — Theme JS: dark mode, TOC, reading progress, phase filter */
(function () {
  'use strict';

  /* ── Dark Mode ─────────────────────────────────────────────────────────── */
  var DARK_KEY = 'esp32-theme';

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try { localStorage.setItem(DARK_KEY, theme); } catch (e) {}
  }

  function initTheme() {
    var saved = '';
    try { saved = localStorage.getItem(DARK_KEY) || ''; } catch (e) {}
    var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(saved || (prefersDark ? 'dark' : 'light'));
  }

  /* Run before DOMContentLoaded so there is no flash of wrong theme */
  initTheme();

  document.addEventListener('DOMContentLoaded', function () {

    /* ── Dark Mode Toggle ───────────────────────────────────────────────── */
    var toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', function () {
        var current = document.documentElement.getAttribute('data-theme');
        applyTheme(current === 'dark' ? 'light' : 'dark');
      });
    }

    /* ── Reading Progress Bar ───────────────────────────────────────────── */
    var progressBar = document.getElementById('reading-progress');
    var articleBody = document.getElementById('article-body');
    if (progressBar && articleBody) {
      function updateProgress() {
        var rect     = articleBody.getBoundingClientRect();
        var start    = rect.top + window.scrollY;
        var end      = start + articleBody.offsetHeight - window.innerHeight;
        var scrolled = window.scrollY;
        var pct      = end <= start ? 0 : Math.min(100, Math.max(0, (scrolled - start) / (end - start) * 100));
        progressBar.style.width = pct + '%';
      }
      window.addEventListener('scroll', updateProgress, { passive: true });
      updateProgress();
    }

    /* ── Table of Contents ──────────────────────────────────────────────── */
    var tocContainer = document.getElementById('toc-list');
    if (tocContainer && articleBody) {
      var headings = articleBody.querySelectorAll('h2, h3');
      if (headings.length > 0) {
        var ul = document.createElement('ul');
        ul.className = 'toc-list';

        headings.forEach(function (h, i) {
          if (!h.id) h.id = 'h-' + i;
          var li  = document.createElement('li');
          li.className = h.tagName === 'H3' ? 'toc-h3' : 'toc-h2';
          var a   = document.createElement('a');
          a.href  = '#' + h.id;
          a.textContent = h.textContent.trim();
          a.dataset.hid = h.id;
          a.addEventListener('click', function (e) {
            e.preventDefault();
            var target = document.getElementById(h.id);
            if (target) {
              var top = target.getBoundingClientRect().top + window.scrollY - 90;
              window.scrollTo({ top: top, behavior: 'smooth' });
            }
          });
          li.appendChild(a);
          ul.appendChild(li);
        });

        tocContainer.appendChild(ul);

        /* Active section via IntersectionObserver */
        if ('IntersectionObserver' in window) {
          var allLinks = ul.querySelectorAll('a');
          var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
              var link = ul.querySelector('[data-hid="' + entry.target.id + '"]');
              if (link) {
                if (entry.isIntersecting) {
                  allLinks.forEach(function (l) { l.classList.remove('is-active'); });
                  link.classList.add('is-active');
                }
              }
            });
          }, { rootMargin: '-8% 0px -80% 0px', threshold: 0 });

          headings.forEach(function (h) { observer.observe(h); });
        }
      } else {
        /* No headings: hide sidebar TOC nav */
        var tocNav = tocContainer.closest('.toc-nav');
        if (tocNav) tocNav.style.display = 'none';
      }
    }

    /* ── Guide Archive Phase Filter ─────────────────────────────────────── */
    var phaseTabs     = document.querySelectorAll('.phase-tab');
    var phaseSections = document.querySelectorAll('.guide-phase-section');

    if (phaseTabs.length && phaseSections.length) {
      phaseTabs.forEach(function (btn) {
        btn.addEventListener('click', function () {
          phaseTabs.forEach(function (b) { b.classList.remove('is-active'); });
          btn.classList.add('is-active');
          var filter = btn.dataset.phaseFilter || '';

          phaseSections.forEach(function (section) {
            if (!filter) {
              section.style.display = '';
              return;
            }
            var sectionPhase = section.dataset.phaseName || '';
            section.style.display = (sectionPhase === filter) ? '' : 'none';
          });
        });
      });
    }

  });

})();
