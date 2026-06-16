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

function updateSectionToc(level) {
  document.querySelectorAll('#section-toc a[data-section]').forEach(function (link) {
    link.href = '#sec-' + level + '-' + link.dataset.section;
  });
}

function toggleFaq(btn) {
  var item = btn.closest('.faq-item');
  var ans = item.querySelector('.faq-a');
  var willOpen = !item.classList.contains('open');
  document.querySelectorAll('.faq-item.open').forEach(function (el) {
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
    panel.hidden = panel.dataset.level !== level;
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

window.addEventListener('load', function () {
  document.querySelectorAll('.acc-item.open .acc-body').forEach(function (body) {
    body.style.maxHeight = body.scrollHeight + 'px';
  });

  document.querySelectorAll('#section-toc a[data-section]').forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      var activePanel = document.querySelector('.level-panel:not([hidden])');
      var level = activePanel ? activePanel.dataset.level : 'beginner';
      var sec = link.dataset.section;
      var target = document.getElementById('sec-' + level + '-' + sec);
      if (!target) return;
      var panel = target.closest('.level-panel');
      if (panel && panel.hidden) {
        setDifficultyLevel(panel.dataset.level);
      }
      panel.querySelectorAll('.acc-item.open').forEach(closeAccordionItem);
      openAccordionItem(target);
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  });

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
  }
});
