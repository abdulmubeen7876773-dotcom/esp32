function closeAccordionItem(item) {
  if (!item) return;
  item.classList.remove('open');
  var btn = item.querySelector('.acc-btn');
  var body = item.querySelector('.acc-body');
  if (btn) btn.setAttribute('aria-expanded', 'false');
  if (body) body.style.maxHeight = '0px';
}

function openAccordionItem(item) {
  if (!item) return;
  item.classList.add('open');
  var btn = item.querySelector('.acc-btn');
  var body = item.querySelector('.acc-body');
  if (btn) btn.setAttribute('aria-expanded', 'true');
  if (body) {
    body.style.maxHeight = body.scrollHeight + 'px';
    window.requestAnimationFrame(function () {
      body.style.maxHeight = body.scrollHeight + 'px';
    });
  }
}

function toggleAccordion(btn) {
  var item = btn.closest('.acc-item');
  if (!item) return;
  var willOpen = !item.classList.contains('open');
  var group = item.closest('.level-panel') || item.closest('.section-accordions');
  if (group && willOpen) {
    group.querySelectorAll('.acc-item.open').forEach(function (el) {
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
  panel.querySelectorAll('.acc-item').forEach(closeAccordionItem);
  var overview = panel.querySelector('.acc-item[data-section="overview"]');
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
  if (target.classList.contains('acc-item')) {
    var group = target.closest('.level-panel') || target.closest('.section-accordions');
    if (group) {
      group.querySelectorAll('.acc-item.open').forEach(closeAccordionItem);
      openAccordionItem(target);
    }
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

function setDifficultyLevel(level, animate) {
  if (!level) return;
  if (animate === undefined) animate = true;
  var slot = document.getElementById('level-slot');
  var archive = document.getElementById('level-archive');
  var target = document.getElementById('level-' + level);
  if (!slot || !archive || !target) return;

  document.querySelectorAll('.difficulty-tab').forEach(function (tab) {
    var on = tab.dataset.level === level;
    tab.classList.toggle('active', on);
    tab.setAttribute('aria-selected', on ? 'true' : 'false');
    tab.setAttribute('tabindex', on ? '0' : '-1');
  });

  document.querySelectorAll('[data-level-link]').forEach(function (link) {
    link.classList.toggle('is-active', link.dataset.levelLink === level);
  });

  var current = slot.querySelector('.level-panel');
  if (current && current !== target) {
    current.classList.remove('is-active');
    current.setAttribute('aria-hidden', 'true');
    archive.appendChild(current);
  }

  if (target.parentElement !== slot) {
    slot.appendChild(target);
  }

  target.classList.add('is-active');
  target.removeAttribute('hidden');
  target.setAttribute('aria-hidden', 'false');

  if (animate) {
    slot.classList.remove('is-switching');
    void slot.offsetWidth;
    slot.classList.add('is-switching');
  }

  updateSectionToc(level);
  resetPanelAccordions(level);

  if (history.replaceState) {
    history.replaceState(null, '', '#' + level);
  }
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

function initProjectPage() {
  document.querySelectorAll('.acc-item.open .acc-body').forEach(function (body) {
    body.style.maxHeight = body.scrollHeight + 'px';
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

  var tabs = document.querySelectorAll('.difficulty-tab');
  if (!tabs.length) return;

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

  document.querySelectorAll('[data-level-link]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      setDifficultyLevel(link.dataset.levelLink);
      var slot = document.getElementById('level-slot');
      if (slot) slot.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

  var hash = (location.hash || '').replace('#', '').toLowerCase();
  if (hash === 'beginner' || hash === 'intermediate' || hash === 'advanced') {
    setDifficultyLevel(hash, false);
  } else {
    setDifficultyLevel('beginner', false);
  }

  initScrollSpy();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initProjectPage);
} else {
  initProjectPage();
}
