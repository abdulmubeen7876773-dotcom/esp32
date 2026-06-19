(function () {
  'use strict';

  var SEARCH_URL = window.ESP32_SEARCH_URL || '';
  var debounceTimer = null;
  var DEBOUNCE_MS   = 280;
  var activeIndex   = -1;
  var currentResults = [];

  /* ─── Highlight matching text ─── */
  function highlight(text, q) {
    if (!q) return escHtml(text);
    var re = new RegExp('(' + q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + ')', 'gi');
    return escHtml(text).replace(re, '<mark class="search-result-highlight">$1</mark>');
  }

  function escHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /* ─── Render results into a given results container ─── */
  function renderResults(container, items, q) {
    currentResults = items;
    activeIndex    = -1;
    if (!items || !items.length) {
      container.innerHTML = '<p class="search-no-results">No results found for <strong>' + escHtml(q) + '</strong></p>';
    } else {
      container.innerHTML = items.map(function (r, i) {
        return '<a class="search-result-item" href="' + escHtml(r.url) + '" data-idx="' + i + '">'
          + '<span class="search-result-type">' + escHtml(r.type) + (r.phase ? ' · ' + escHtml(r.phase) : '') + '</span>'
          + '<span class="search-result-title">' + highlight(r.title, q) + '</span>'
          + (r.excerpt ? '<span class="search-result-excerpt">' + escHtml(r.excerpt) + '</span>' : '')
          + '</a>';
      }).join('');
    }
    container.removeAttribute('hidden');
  }

  /* ─── Fetch from REST endpoint ─── */
  function doSearch(q, container) {
    if (q.length < 2) {
      container.setAttribute('hidden', '');
      container.innerHTML = '';
      return;
    }
    container.innerHTML = '<p class="search-loading">Searching…</p>';
    container.removeAttribute('hidden');

    var url = SEARCH_URL + '?q=' + encodeURIComponent(q);
    fetch(url, { method: 'GET', headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.json(); })
      .then(function (data) { renderResults(container, data, q); })
      .catch(function () {
        container.innerHTML = '<p class="search-no-results">Search unavailable. Try again.</p>';
      });
  }

  /* ─── Keyboard navigation within results ─── */
  function moveFocus(items, dir) {
    items.forEach(function (el) { el.classList.remove('is-focused'); });
    activeIndex += dir;
    if (activeIndex < 0) activeIndex = items.length - 1;
    if (activeIndex >= items.length) activeIndex = 0;
    items[activeIndex].classList.add('is-focused');
    items[activeIndex].scrollIntoView({ block: 'nearest' });
  }

  /* ─── Wire up a search input + results container pair ─── */
  function attachSearch(input, container) {
    if (!input || !container) return;

    input.addEventListener('input', function () {
      var q = input.value.trim();
      clearTimeout(debounceTimer);
      if (!q) {
        container.setAttribute('hidden', '');
        container.innerHTML = '';
        return;
      }
      debounceTimer = setTimeout(function () { doSearch(q, container); }, DEBOUNCE_MS);
    });

    input.addEventListener('keydown', function (e) {
      var items = Array.from(container.querySelectorAll('.search-result-item'));
      if (!items.length) return;
      if (e.key === 'ArrowDown')  { e.preventDefault(); moveFocus(items,  1); }
      if (e.key === 'ArrowUp')    { e.preventDefault(); moveFocus(items, -1); }
      if (e.key === 'Enter' && activeIndex >= 0) {
        e.preventDefault();
        items[activeIndex].click();
      }
      if (e.key === 'Escape') {
        container.setAttribute('hidden', '');
        container.innerHTML = '';
        input.blur();
      }
    });

    /* Close when clicking outside */
    document.addEventListener('click', function (e) {
      if (!input.contains(e.target) && !container.contains(e.target)) {
        container.setAttribute('hidden', '');
      }
    });
  }

  /* ─── Header overlay search ─── */
  function initOverlaySearch() {
    var overlay = document.getElementById('search-overlay');
    var input   = document.getElementById('search-overlay-input');
    if (!overlay || !input) return;

    var results = document.getElementById('overlay-search-results');
    if (!results) {
      results = document.createElement('div');
      results.id = 'overlay-search-results';
      results.className = 'hero-search-results';
      results.setAttribute('hidden', '');
      input.parentNode.appendChild(results);
    }
    attachSearch(input, results);
  }

  /* ─── Hero page search ─── */
  function initHeroSearch() {
    var input   = document.getElementById('hero-search-input');
    var results = document.getElementById('hero-search-results');
    if (!input || !results) return;
    attachSearch(input, results);
  }

  /* ─── Keyboard shortcut: / opens overlay or focuses hero search ─── */
  function initKeyboardShortcut() {
    document.addEventListener('keydown', function (e) {
      var tag = (document.activeElement && document.activeElement.tagName) || '';
      if (e.key !== '/' || tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT') return;
      e.preventDefault();

      /* Try hero search first */
      var hero = document.getElementById('hero-search-input');
      if (hero) {
        hero.focus();
        hero.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
      }

      /* Fallback: open overlay */
      var openBtn = document.querySelector('[data-search-open]');
      if (openBtn) openBtn.click();
    });
  }

  /* ─── Copy-code buttons ─── */
  function initCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var pre = btn.closest('.code-block') && btn.closest('.code-block').querySelector('pre');
        if (!pre) return;
        var text = pre.textContent || '';
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(function () {
            btn.textContent = 'Copied!';
            btn.classList.add('copied');
            setTimeout(function () {
              btn.textContent = 'Copy';
              btn.classList.remove('copied');
            }, 2000);
          });
        } else {
          /* Fallback */
          var ta = document.createElement('textarea');
          ta.value = text;
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          document.body.appendChild(ta);
          ta.select();
          try { document.execCommand('copy'); } catch (ex) { /* silent fail */ }
          document.body.removeChild(ta);
          btn.textContent = 'Copied!';
          btn.classList.add('copied');
          setTimeout(function () { btn.textContent = 'Copy'; btn.classList.remove('copied'); }, 2000);
        }
      });
    });
  }

  /* ─── FAQ accordion (guide pages) ─── */
  function initFAQAccordion() {
    document.querySelectorAll('.faq-q').forEach(function (btn) {
      /* Skip already initialised */
      if (btn.dataset.faqInit) return;
      btn.dataset.faqInit = '1';
      btn.addEventListener('click', function () {
        var answer  = btn.nextElementSibling;
        var isOpen  = btn.getAttribute('aria-expanded') === 'true';
        /* Close all */
        document.querySelectorAll('.faq-q').forEach(function (b) {
          b.setAttribute('aria-expanded', 'false');
          var a = b.nextElementSibling;
          if (a) a.style.maxHeight = '0';
          var plus = b.querySelector('.plus');
          if (plus) plus.textContent = '+';
        });
        if (!isOpen && answer) {
          btn.setAttribute('aria-expanded', 'true');
          answer.style.maxHeight = answer.scrollHeight + 'px';
          var plus = btn.querySelector('.plus');
          if (plus) plus.textContent = '−';
        }
      });
    });
  }

  /* ─── Init ─── */
  document.addEventListener('DOMContentLoaded', function () {
    initHeroSearch();
    initOverlaySearch();
    initKeyboardShortcut();
    initCopyButtons();
    initFAQAccordion();
  });
})();
