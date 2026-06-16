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
  if (history.replaceState) {
    history.replaceState(null, '', '#' + level);
  }
}

window.addEventListener('load', function () {
  document.querySelectorAll('.faq-item.open .faq-a').forEach(function (a) {
    a.style.maxHeight = a.scrollHeight + 'px';
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
