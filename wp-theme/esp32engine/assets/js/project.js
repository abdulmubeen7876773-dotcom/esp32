(function () {
  'use strict';

  function getLevelRadio(level) {
    return document.getElementById('level-radio-' + level);
  }

  function resetDifficultyAccordions(level) {
    var panel = document.querySelector('.difficulty-content[data-level="' + level + '"]');
    if (!panel) return;
    panel.querySelectorAll('details.accordion-item[open]').forEach(function (el) {
      el.open = false;
    });
    var overview = panel.querySelector('details.accordion-item[data-section="overview"]');
    if (overview) overview.open = true;
  }

  function setDifficultyLevel(level) {
    if (!level) return;
    var radio = getLevelRadio(level);
    if (radio) radio.checked = true;

    document.querySelectorAll('[data-level-link]').forEach(function (link) {
      link.classList.toggle('is-active', link.dataset.levelLink === level);
    });

    updateSectionToc(level);
    resetDifficultyAccordions(level);

    if (history.replaceState) {
      history.replaceState(null, '', '#' + level);
    }
  }

  function updateSectionToc(level) {
    document.querySelectorAll('#section-toc a[data-section]').forEach(function (link) {
      var sec = link.dataset.section;
      link.href = '#sec-' + level + '-' + sec;
    });
    var mobile = document.getElementById('mobile-nav-select');
    if (!mobile) return;
    var labels = {
      overview: 'Overview',
      components: 'Components',
      wiring: 'Wiring',
      code: 'Arduino Code',
      how: 'How It Works',
      apps: 'Applications',
      troubleshooting: 'Troubleshooting',
      upgrades: 'Upgrades',
      faq: 'FAQ'
    };
    mobile.innerHTML = '<option value="">Jump to section…</option>';
    Object.keys(labels).forEach(function (sec) {
      var opt = document.createElement('option');
      opt.value = 'sec-' + level + '-' + sec;
      opt.textContent = labels[sec];
      mobile.appendChild(opt);
    });
    mobile.innerHTML += '<option value="related">Related Projects</option>';
  }

  function openDetailsSection(detailsEl) {
    if (!detailsEl || detailsEl.tagName !== 'DETAILS') return;
    var group = detailsEl.closest('.difficulty-content') || detailsEl.closest('.footer-accordions');
    if (group) {
      group.querySelectorAll('details.accordion-item[open]').forEach(function (el) {
        if (el !== detailsEl) el.open = false;
      });
    }
    detailsEl.open = true;
  }

  function jumpToSection(targetId) {
    if (!targetId) return;
    if (targetId.indexOf('sec-') === 0) {
      var level = targetId.split('-')[1];
      if (level === 'beginner' || level === 'intermediate' || level === 'advanced') {
        setDifficultyLevel(level);
      }
    }
    var target = document.getElementById(targetId);
    if (!target) return;
    var details = target.tagName === 'DETAILS' ? target : target.closest('details.accordion-item');
    if (details) openDetailsSection(details);
    (details || target).scrollIntoView({ behavior: 'smooth', block: 'start' });
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
          if (a) a.style.display = 'none';
        }
      });
    item.classList.toggle('open', willOpen);
    if (ans) ans.style.display = willOpen ? 'block' : 'none';
  }

  function copyCode(btn) {
    var block = btn.closest('.code-block');
    var pre = block ? block.querySelector('pre') : null;
    if (!pre) return;
    navigator.clipboard.writeText(pre.innerText).then(function () {
      var orig = btn.textContent;
      btn.textContent = 'Copied';
      setTimeout(function () {
        btn.textContent = orig;
      }, 1600);
    });
  }

  function initExclusiveAccordions() {
    document.querySelectorAll('details.accordion-item').forEach(function (details) {
      details.addEventListener('toggle', function () {
        if (!details.open) return;
        var group = details.closest('.difficulty-content') || details.closest('.footer-accordions');
        if (!group) return;
        group.querySelectorAll('details.accordion-item[open]').forEach(function (el) {
          if (el !== details) el.open = false;
        });
      });
    });
  }

  function syncActiveTabStyles() {
    document.querySelectorAll('.level-radio').forEach(function (radio) {
      radio.addEventListener('change', function () {
        if (!radio.checked) return;
        var level = radio.id.replace('level-radio-', '');
        document.querySelectorAll('[data-level-link]').forEach(function (link) {
          link.classList.toggle('is-active', link.dataset.levelLink === level);
        });
        updateSectionToc(level);
        resetDifficultyAccordions(level);
        if (history.replaceState) {
          history.replaceState(null, '', '#' + level);
        }
      });
    });
  }

  function initProjectPage() {
    initExclusiveAccordions();
    syncActiveTabStyles();

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

    document.querySelectorAll('[data-level-link]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        setDifficultyLevel(link.dataset.levelLink);
      });
    });

    document.querySelectorAll('.copy-btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        copyCode(btn);
      });
    });

    document.querySelectorAll('.faq-q').forEach(function (btn) {
      btn.addEventListener('click', function () {
        toggleFaq(btn);
      });
    });

    var radios = document.querySelectorAll('.level-radio');
    if (radios.length) {
      var hash = (location.hash || '').replace('#', '').toLowerCase();
      if (hash === 'beginner' || hash === 'intermediate' || hash === 'advanced') {
        setDifficultyLevel(hash);
      } else {
        setDifficultyLevel('beginner');
      }
    }
  }

  window.setDifficultyLevel = setDifficultyLevel;
  window.copyCode = copyCode;
  window.toggleFaq = toggleFaq;

  document.addEventListener('DOMContentLoaded', initProjectPage);
})();
