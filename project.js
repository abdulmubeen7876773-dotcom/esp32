function closeAccordionItem(item) {
  if (!item) return;
  item.classList.remove('open');
  var btn = item.querySelector('.acc-btn');
  var body = item.querySelector('.acc-body');
  if (btn) btn.setAttribute('aria-expanded', 'false');
  if (body) body.style.maxHeight = null;
}

function openAccordionItem(item) {
  if (!item) return;
  item.classList.add('open');
  var btn = item.querySelector('.acc-btn');
  var body = item.querySelector('.acc-body');
  if (btn) btn.setAttribute('aria-expanded', 'true');
  if (body) body.style.maxHeight = body.scrollHeight + 'px';
  window.requestAnimationFrame(function () {
    if (body) body.style.maxHeight = body.scrollHeight + 'px';
  });
}

function toggleAccordion(btn) {
  var item = btn.closest('.acc-item');
  if (!item) return;
  var willOpen = !item.classList.contains('open');
  var panel = item.closest('.level-panel');
  if (panel && willOpen) {
    panel.querySelectorAll('.acc-item.open').forEach(function (el) {
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
  var panel = document.querySelector('.level-panel[data-level="' + level + '"]');
  if (!panel) return;
  panel.querySelectorAll('.acc-item').forEach(closeAccordionItem);
  var overview = panel.querySelector('.acc-item[data-section="overview"]');
  if (overview) openAccordionItem(overview);
}

function getActiveLevel() {
  var panel = document.querySelector('.level-panel.is-active');
  return panel ? panel.dataset.level : 'beginner';
}

function updateSectionToc(level) {
  document.querySelectorAll('#section-toc a[data-section]').forEach(function (link) {
    var sec = link.dataset.section;
    if (sec === 'faq') {
      link.href = '#faq';
    } else {
      link.href = '#sec-' + level + '-' + sec;
    }
  });
  var mobile = document.getElementById('mobile-nav-select');
  if (!mobile) return;
  var val = mobile.value;
  var labels = {
    overview: 'Overview',
    components: 'Components',
    wiring: 'Wiring',
    code: 'Code',
    how: 'How It Works',
    apps: 'Applications',
    troubleshooting: 'Troubleshooting',
    upgrades: 'Upgrades'
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
  if (val) mobile.value = val;
}

function jumpToSection(targetId) {
  if (!targetId) return;
  var target = document.getElementById(targetId);
  if (!target) return;
  if (targetId.indexOf('sec-') === 0) {
    var parts = targetId.split('-');
    var level = parts[1];
    if (level === 'beginner' || level === 'intermediate' || level === 'advanced') {
      setDifficultyLevel(level);
    }
    target = document.getElementById(targetId);
    if (!target) return;
    var panel = target.closest('.level-panel');
    if (panel) {
      panel.querySelectorAll('.acc-item.open').forEach(closeAccordionItem);
      openAccordionItem(target);
    }
  } else {
    openAccordionItem(target);
  }
  target.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function toggleFaq(btn) {
  var item = btn.closest('.faq-item');
  var ans = item.querySelector('.faq-a');
  var willOpen = !item.classList.contains('open');
  item.closest('.faq-list')
    .querySelectorAll('.faq-item.open')
    .forEach(function (el) {
      if (el !== item) {
        el.classList.remove('open');
        el.querySelector('.faq-a').style.maxHeight = null;
      }
    });
  if (willOpen) {
    item.classList.add('open');
    ans.style.maxHeight = ans.scrollHeight + 'px';
  } else {
    item.classList.remove('open');
    ans.style.maxHeight = null;
  }
}

function copyCode(btn) {
  var block = btn.closest('.code-block');
  var pre = block ? block.querySelector('pre') : document.getElementById('code-content');
  if (!pre) return;
  var code = pre.innerText;
  navigator.clipboard.writeText(code).then(function () {
    var orig = btn.textContent;
    btn.textContent = 'Copied';
    btn.classList.add('copied');
    setTimeout(function () {
      btn.textContent = orig;
      btn.classList.remove('copied');
    }, 1600);
  });
}

function setDifficultyLevel(level) {
  if (!level) return;
  document.querySelectorAll('.difficulty-tab').forEach(function (tab) {
    var on = tab.dataset.level === level;
    tab.classList.toggle('active', on);
    tab.setAttribute('aria-selected', on ? 'true' : 'false');
  });
  document.querySelectorAll('.level-panel').forEach(function (panel) {
    var on = panel.dataset.level === level;
    panel.classList.toggle('is-active', on);
    panel.hidden = !on;
    panel.setAttribute('aria-hidden', on ? 'false' : 'true');
  });
  document.querySelectorAll('[data-level-link]').forEach(function (link) {
    link.classList.toggle('is-active', link.dataset.levelLink === level);
  });
  updateSectionToc(level);
  resetPanelAccordions(level);
  if (history.replaceState) {
    history.replaceState(null, '', '#' + level);
  }
}

function initScrollSpy() {
  var tocLinks = document.querySelectorAll('#section-toc a[data-section]');
  if (!tocLinks.length) return;
  var targets = [];
  tocLinks.forEach(function (link) {
    var id = (link.getAttribute('href') || '').replace('#', '');
    var el = document.getElementById(id);
    if (el) targets.push({ el: el, link: link, section: link.dataset.section });
  });
  if (!targets.length || !('IntersectionObserver' in window)) return;
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
    { rootMargin: '-20% 0px -65% 0px', threshold: 0 }
  );
  targets.forEach(function (t) {
    observer.observe(t.el);
  });
}

function initProjectPage() {
  document.querySelectorAll('.acc-item.open .acc-body').forEach(function (body) {
    body.style.maxHeight = body.scrollHeight + 'px';
  });

  document.querySelectorAll('#section-toc a[data-section]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      var href = link.getAttribute('href') || '';
      jumpToSection(href.replace('#', ''));
    });
  });

  var mobile = document.getElementById('mobile-nav-select');
  if (mobile) {
    mobile.addEventListener('change', function () {
      jumpToSection(mobile.value);
      mobile.value = '';
    });
  }

  var tabs = document.querySelectorAll('.difficulty-tab');
  if (tabs.length) {
    tabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        setDifficultyLevel(tab.dataset.level);
      });
    });
    document.querySelectorAll('[data-level-link]').forEach(function (link) {
      link.addEventListener('click', function (e) {
        e.preventDefault();
        setDifficultyLevel(link.dataset.levelLink);
        var panels = document.querySelector('.level-panels');
        if (panels) panels.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
    var hash = (location.hash || '').replace('#', '').toLowerCase();
    if (hash === 'beginner' || hash === 'intermediate' || hash === 'advanced') {
      setDifficultyLevel(hash);
    } else {
      setDifficultyLevel('beginner');
    }
    initScrollSpy();
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initProjectPage);
} else {
  initProjectPage();
}
