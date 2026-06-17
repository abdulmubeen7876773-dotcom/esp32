(function () {
  'use strict';

  function closeAccordionItem(item) {
    if (!item) return;
    item.classList.remove('open');
    var btn = item.querySelector('.acc-btn, .accordion-header');
    var body = item.querySelector('.acc-body, .accordion-content');
    if (btn) btn.setAttribute('aria-expanded', 'false');
    if (body) body.style.maxHeight = '0px';
  }

  function openAccordionItem(item) {
    if (!item) return;
    item.classList.add('open');
    var btn = item.querySelector('.acc-btn, .accordion-header');
    var body = item.querySelector('.acc-body, .accordion-content');
    if (btn) btn.setAttribute('aria-expanded', 'true');
    if (body) {
      body.style.maxHeight = body.scrollHeight + 'px';
      window.requestAnimationFrame(function () {
        body.style.maxHeight = body.scrollHeight + 'px';
      });
    }
  }

  function toggleAccordion(btn) {
    var item = btn.closest('.acc-item, .accordion-item');
    if (!item) return;
    var willOpen = !item.classList.contains('open');
    var group =
      item.closest('.level-panel, .difficulty-content') || item.closest('.section-accordions');
    if (group && willOpen) {
      group.querySelectorAll('.acc-item.open, .accordion-item.open').forEach(function (el) {
        if (el !== item) closeAccordionItem(el);
      });
    }
    if (willOpen) {
      openAccordionItem(item);
    } else {
      closeAccordionItem(item);
    }
  }

  function resetPanelAccordions(level) {
    var panel = document.getElementById('level-' + level);
    if (!panel) return;
    panel.querySelectorAll('.acc-item, .accordion-item').forEach(closeAccordionItem);
    var overview = panel.querySelector('[data-section="overview"]');
    if (overview) openAccordionItem(overview);
  }

  function updateSectionToc(level) {
    document.querySelectorAll('#section-toc a[data-section]').forEach(function (link) {
      var sec = link.dataset.section;
      link.href = sec === 'faq' ? '#faq' : '#sec-' + level + '-' + sec;
    });
    var mobile = document.getElementById('mobile-nav-select');
    if (!mobile) return;
    var labels = {
      overview: 'Overview',
      components: 'Components Required',
      wiring: 'Wiring Diagram',
      code: 'Arduino Code',
      how: 'How It Works',
      apps: 'Applications',
      troubleshooting: 'Troubleshooting',
      upgrades: 'Possible Upgrades'
    };
    mobile.innerHTML = '<option value="">Jump to section…</option>';
    Object.keys(labels).forEach(function (sec) {
      var opt = document.createElement('option');
      opt.value = 'sec-' + level + '-' + sec;
      opt.textContent = labels[sec];
      mobile.appendChild(opt);
    });
    ['faq', 'related'].forEach(function (sec) {
      var opt = document.createElement('option');
      opt.value = sec;
      opt.textContent = sec === 'faq' ? 'FAQ' : 'Related Projects';
      mobile.appendChild(opt);
    });
  }

  function getDifficultySections() {
    return document.querySelectorAll('.difficulty-content, .level-panel[data-level]');
  }

  function setDifficultyLevel(level, animate) {
    if (!level) return;
    if (animate === undefined) animate = true;

    var sections = getDifficultySections();
    var target = document.getElementById('level-' + level);
    if (!sections.length || !target) {
      console.warn('[project.js] Missing difficulty section for level:', level);
      return;
    }

    document.querySelectorAll('.difficulty-tab').forEach(function (tab) {
      var on = tab.dataset.level === level;
      tab.classList.toggle('active', on);
      tab.setAttribute('aria-selected', on ? 'true' : 'false');
      tab.setAttribute('tabindex', on ? '0' : '-1');
    });

    document.querySelectorAll('[data-level-link]').forEach(function (link) {
      link.classList.toggle('is-active', link.dataset.levelLink === level);
    });

    sections.forEach(function (section) {
      var on = section.dataset.level === level || section.id === 'level-' + level;
      section.classList.toggle('active', on);
      section.classList.toggle('is-active', on);
      section.setAttribute('aria-hidden', on ? 'false' : 'true');
      if (on) {
        section.removeAttribute('hidden');
      } else {
        section.setAttribute('hidden', '');
      }
    });

    if (animate && target) {
      target.classList.remove('is-switching');
      void target.offsetWidth;
      target.classList.add('is-switching');
    }

    updateSectionToc(level);
    resetPanelAccordions(level);

    if (history.replaceState) {
      history.replaceState(null, '', '#' + level);
    }
  }

  function jumpToSection(targetId) {
    if (!targetId) return;
    if (targetId.indexOf('sec-') === 0) {
      var parts = targetId.split('-');
      var level = parts[1];
      if (level === 'beginner' || level === 'intermediate' || level === 'advanced') {
        setDifficultyLevel(level, false);
      }
    }
    var target = document.getElementById(targetId);
    if (!target) return;
    if (target.classList.contains('acc-item') || target.classList.contains('accordion-item')) {
      var group =
        target.closest('.level-panel, .difficulty-content') ||
        target.closest('.section-accordions');
      if (group) {
        group.querySelectorAll('.acc-item.open, .accordion-item.open').forEach(closeAccordionItem);
        openAccordionItem(target);
      }
    }
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  function toggleFaq(btn) {
    var item = btn.closest('.faq-item');
    if (!item) return;
    var ans = item.querySelector('.faq-a');
    var willOpen = !item.classList.contains('open');
    item.closest('.faq-list')
      .querySelectorAll('.faq-item.open')
      .forEach(function (el) {
        if (el !== item) {
          el.classList.remove('open');
          var a = el.querySelector('.faq-a');
          if (a) a.style.maxHeight = null;
        }
      });
    if (willOpen) {
      item.classList.add('open');
      if (ans) ans.style.maxHeight = ans.scrollHeight + 'px';
    } else {
      item.classList.remove('open');
      if (ans) ans.style.maxHeight = null;
    }
  }

  function copyCode(btn) {
    var block = btn.closest('.code-block');
    var pre = block ? block.querySelector('pre') : document.getElementById('code-content');
    if (!pre) return;
    navigator.clipboard.writeText(pre.innerText).then(function () {
      var orig = btn.textContent;
      btn.textContent = 'Copied';
      btn.classList.add('copied');
      setTimeout(function () {
        btn.textContent = orig;
        btn.classList.remove('copied');
      }, 1600);
    });
  }

  function parseWiringText(text) {
    var rows = [];
    text.split(/[\n,;]+/).forEach(function (part) {
      var chunk = part.trim();
      if (!chunk) return;
      var m = chunk.match(/^(.+?)\s*(?:->|→|:)\s*(.+)$/);
      if (m) {
        rows.push({ comp: m[1].trim(), pin: m[2].trim(), note: '' });
      }
    });
    return rows;
  }

  function buildWiringTable(rows) {
    if (!rows.length) return '';
    var body = rows
      .map(function (row) {
        return (
          '<tr><td>' +
          row.comp +
          '</td><td><strong>' +
          row.pin +
          '</strong></td><td>' +
          (row.note || '') +
          '</td></tr>'
        );
      })
      .join('');
    return (
      '<div class="pin-table-wrap wiring-table-wrap">' +
      '<table class="pin-table pin-table-3 wiring-table">' +
      '<thead><tr><th>Component Pin</th><th>ESP32 Pin</th><th>Notes</th></tr></thead>' +
      '<tbody>' +
      body +
      '</tbody></table></div>'
    );
  }

  function initWiringTables() {
    document.querySelectorAll('[data-wiring-text]').forEach(function (el) {
      var rows = parseWiringText(el.textContent || '');
      if (!rows.length) return;
      el.innerHTML = buildWiringTable(rows);
      el.removeAttribute('data-wiring-text');
    });

    document.querySelectorAll('.acc-item[data-section="wiring"] .acc-inner').forEach(function (inner) {
      if (inner.querySelector('table')) return;
      var text = (inner.textContent || '').trim();
      if (!text || text.indexOf('->') === -1 && text.indexOf('→') === -1) return;
      var rows = parseWiringText(text);
      if (rows.length) inner.innerHTML = buildWiringTable(rows);
    });
  }

  function initScrollSpy() {
    var tocLinks = document.querySelectorAll('#section-toc a[data-section]');
    if (!tocLinks.length || !('IntersectionObserver' in window)) return;
    var targets = [];
    tocLinks.forEach(function (link) {
      var id = (link.getAttribute('href') || '').replace('#', '');
      var el = document.getElementById(id);
      if (el) targets.push({ el: el, link: link });
    });
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          var match = targets.find(function (t) {
            return t.el === entry.target;
          });
          if (!match) return;
          tocLinks.forEach(function (l) {
            l.classList.toggle('is-active', l === match.link);
          });
        });
      },
      { rootMargin: '-15% 0px -70% 0px', threshold: 0 }
    );
    targets.forEach(function (t) {
      observer.observe(t.el);
    });
  }

  function bindAccordions() {
    document.querySelectorAll('.acc-btn, .accordion-header').forEach(function (btn) {
      if (btn.dataset.bound === '1') return;
      btn.dataset.bound = '1';
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        toggleAccordion(btn);
      });
    });
  }

  function initProjectPage() {
    console.log('Project page loaded');

    var tabs = document.querySelectorAll('.difficulty-tab');
    var sections = getDifficultySections();
    var accItems = document.querySelectorAll('.acc-item, .accordion-item');

    console.log('Difficulty buttons found:', tabs.length);
    console.log('Difficulty sections found:', sections.length);
    console.log('Accordion items found:', accItems.length);

    initWiringTables();
    bindAccordions();

    document.querySelectorAll('.acc-item.open .acc-body, .accordion-item.open .accordion-content').forEach(
      function (body) {
        body.style.maxHeight = body.scrollHeight + 'px';
      }
    );

    document.querySelectorAll('#section-toc a[data-section]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        jumpToSection((link.getAttribute('href') || '').replace('#', ''));
      });
    });

    var mobile = document.getElementById('mobile-nav-select');
    if (mobile) {
      mobile.addEventListener('change', function () {
        if (mobile.value) jumpToSection(mobile.value);
        mobile.value = '';
      });
    }

    if (tabs.length) {
      tabs.forEach(function (tab) {
        tab.addEventListener('click', function () {
          setDifficultyLevel(tab.dataset.level);
        });
        tab.addEventListener('keydown', function (e) {
          if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
          e.preventDefault();
          var list = Array.prototype.slice.call(tabs);
          var idx = list.indexOf(tab);
          var next = e.key === 'ArrowRight' ? list[idx + 1] : list[idx - 1];
          if (next) {
            next.focus();
            setDifficultyLevel(next.dataset.level);
          }
        });
      });
    }

    document.querySelectorAll('[data-level-link]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        setDifficultyLevel(link.dataset.levelLink);
        var panels = document.querySelector('.level-panels');
        if (panels) panels.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });

    document.querySelectorAll('.copy-btn').forEach(function (btn) {
      if (btn.dataset.bound === '1') return;
      btn.dataset.bound = '1';
      btn.addEventListener('click', function () {
        copyCode(btn);
      });
    });

    document.querySelectorAll('.faq-q').forEach(function (btn) {
      if (btn.dataset.bound === '1') return;
      btn.dataset.bound = '1';
      btn.addEventListener('click', function () {
        toggleFaq(btn);
      });
    });

    if (tabs.length && sections.length) {
      var hash = (location.hash || '').replace('#', '').toLowerCase();
      if (hash === 'beginner' || hash === 'intermediate' || hash === 'advanced') {
        setDifficultyLevel(hash, false);
      } else {
        setDifficultyLevel('beginner', false);
      }
    }

    initScrollSpy();
  }

  window.toggleAccordion = toggleAccordion;
  window.toggleFaq = toggleFaq;
  window.copyCode = copyCode;
  window.setDifficultyLevel = setDifficultyLevel;

  document.addEventListener('DOMContentLoaded', initProjectPage);
})();
