(function () {
  'use strict';

  function closeAccordionContent(content) {
    if (!content) return;
    content.classList.remove('open');
    var item = content.closest('.accordion-item');
    var btn = item ? item.querySelector('.accordion-header') : null;
    if (btn) btn.setAttribute('aria-expanded', 'false');
  }

  function openAccordionContent(content) {
    if (!content) return;
    content.classList.add('open');
    var item = content.closest('.accordion-item');
    var btn = item ? item.querySelector('.accordion-header') : null;
    if (btn) btn.setAttribute('aria-expanded', 'true');
  }

  function toggleAccordionHeader(btn) {
    var item = btn.closest('.accordion-item');
    if (!item) return;
    var content = item.querySelector('.accordion-content');
    if (!content) return;
    var willOpen = !content.classList.contains('open');
    var group = item.closest('.difficulty-content') || item.closest('.footer-accordions');
    if (group && willOpen) {
      group.querySelectorAll('.accordion-content.open').forEach(function (el) {
        if (el !== content) closeAccordionContent(el);
      });
    }
    if (willOpen) {
      openAccordionContent(content);
    } else {
      closeAccordionContent(content);
    }
  }

  function resetDifficultyAccordions(level) {
    var panel = document.querySelector('.difficulty-content[data-level="' + level + '"]');
    if (!panel) return;
    panel.querySelectorAll('.accordion-content.open').forEach(closeAccordionContent);
    var overview = panel.querySelector('.accordion-item[data-section="overview"] .accordion-content');
    if (overview) openAccordionContent(overview);
  }

  function setDifficultyLevel(level) {
    if (!level) return;

    document.querySelectorAll('.difficulty-tab').forEach(function (tab) {
      tab.classList.toggle('active', tab.dataset.level === level);
    });

    document.querySelectorAll('.difficulty-content').forEach(function (section) {
      section.classList.toggle('active', section.dataset.level === level);
    });

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
    var content = target.classList.contains('accordion-item')
      ? target.querySelector('.accordion-content')
      : target.closest('.accordion-content');
    if (content) {
      var group = content.closest('.difficulty-content') || content.closest('.footer-accordions');
      if (group) {
        group.querySelectorAll('.accordion-content.open').forEach(closeAccordionContent);
        openAccordionContent(content);
      }
    }
    (target.closest('.accordion-item') || target).scrollIntoView({ behavior: 'smooth', block: 'start' });
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

  function initProjectPage() {
    var tabs = document.querySelectorAll('.difficulty-tab');
    var sections = document.querySelectorAll('.difficulty-content');

    document.querySelectorAll('.accordion-header').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        toggleAccordionHeader(btn);
      });
    });

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

    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        setDifficultyLevel(tab.dataset.level);
      });
    });

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

    if (tabs.length && sections.length) {
      var hash = (location.hash || '').replace('#', '').toLowerCase();
      if (hash === 'beginner' || hash === 'intermediate' || hash === 'advanced') {
        setDifficultyLevel(hash);
      } else {
        setDifficultyLevel('beginner');
      }
    }
  }

  window.toggleAccordion = function (btn) {
    toggleAccordionHeader(btn);
  };
  window.toggleFaq = toggleFaq;
  window.copyCode = copyCode;
  window.setDifficultyLevel = setDifficultyLevel;

  document.addEventListener('DOMContentLoaded', initProjectPage);
})();
