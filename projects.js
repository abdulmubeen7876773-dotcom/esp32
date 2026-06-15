(function () {
  function esc(text) {
    var d = document.createElement('div');
    d.textContent = text || '';
    return d.innerHTML;
  }

  function shortCategory(cat) {
    var c = (cat || 'ESP32').replace(' Projects', '');
    if (c === 'Home Automation') return 'Smart Home';
    return c;
  }

  function badgeClass(difficulty) {
    var d = (difficulty || '').replace(' build', '').trim().toLowerCase();
    if (d === 'advanced') return 'badge-advanced';
    if (d === 'intermediate') return 'badge-intermediate';
    return 'badge-beginner';
  }

  function thumbHtml(category) {
    var icons = window.PROJECT_ICONS || {};
    var thumbs = window.PROJECT_THUMBS || {};
    var svg = icons[category] || icons.__default__ || '';
    var cls = thumbs[category] || 'thumb-esp32';
    return '<div class="card-thumb ' + cls + '">' + svg + '</div>';
  }

  function cardHtml(p) {
    var diff = (p.difficulty || 'Beginner').replace(' build', '');
    var desc = p.desc || '';
    var descHtml = desc ? '<p class="card-desc">' + esc(desc) + '</p>' : '';
    var readMin = p.readMin || 6;
    return (
      '<a class="card project-card modern-card" href="' +
      esc(p.href) +
      '" data-title="' +
      esc((p.title || '').toLowerCase()) +
      '" data-category="' +
      esc(p.category || '') +
      '" data-difficulty="' +
      esc(diff) +
      '">' +
      thumbHtml(p.category) +
      '<div class="card-body"><div class="card-badges"><span class="badge badge-cat">' +
      esc(shortCategory(p.category)) +
      '</span><span class="badge ' +
      badgeClass(diff) +
      '">' +
      esc(diff) +
      '</span><span class="badge badge-time">' +
      readMin +
      ' min read</span></div><h3>' +
      esc(p.title) +
      '</h3>' +
      descHtml +
      '<div class="card-footer"><span class="card-read-more">Read More<span aria-hidden="true">→</span></span></div></div></a>'
    );
  }

  function renderProjects(projects) {
    var grid = document.getElementById('grid');
    if (!grid) return;
    var html = projects.map(cardHtml).join('');
    grid.innerHTML = html;
  }

  function initProjectFilters() {
    var q = document.getElementById('q');
    var cat = document.getElementById('cat');
    var diff = document.getElementById('diff');
    var count = document.getElementById('count');
    if (!q || !cat || !diff || !count) return;

    function slug(text) {
      return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    }

    function getCards() {
      return Array.prototype.slice.call(document.querySelectorAll('.project-card'));
    }

    function applyHashCategory() {
      if (!location.hash.startsWith('#cat-')) return;
      var hashSlug = location.hash.slice(5);
      for (var i = 0; i < cat.options.length; i++) {
        var opt = cat.options[i];
        var label = (opt.textContent || opt.innerText || '').trim();
        if (slug(label) === hashSlug) {
          cat.value = opt.value || label;
          break;
        }
      }
    }

    function filterProjects() {
      var search = q.value.toLowerCase().trim();
      var category = cat.value;
      var difficulty = diff.value;
      var visible = 0;
      getCards().forEach(function (card) {
        var title = card.dataset.title || '';
        var cardCat = card.dataset.category || '';
        var cardDiff = card.dataset.difficulty || '';
        var ok =
          (!search || title.indexOf(search) !== -1) &&
          (!category || cardCat === category) &&
          (!difficulty || cardDiff === difficulty);
        card.classList.toggle('hidden', !ok);
        if (ok) visible++;
      });
      count.textContent = visible + ' projects found';
    }

    [q, cat, diff].forEach(function (el) {
      el.addEventListener('input', filterProjects);
      el.addEventListener('change', filterProjects);
    });

    applyHashCategory();
    filterProjects();

    var params = new URLSearchParams(window.location.search);
    if (params.get('q')) {
      q.value = params.get('q');
      filterProjects();
    }

    window.addEventListener('hashchange', function () {
      applyHashCategory();
      filterProjects();
    });

    window.filterProjects = filterProjects;
  }

  function loadProjects() {
    var grid = document.getElementById('grid');
    var count = document.getElementById('count');
    if (!grid) return;

    fetch('projects.json')
      .then(function (res) {
        if (!res.ok) throw new Error('Failed to load projects');
        return res.json();
      })
      .then(function (projects) {
        renderProjects(projects);
        initProjectFilters();
      })
      .catch(function () {
        grid.innerHTML = '<p class="meta">Could not load the project library. Please refresh the page.</p>';
        if (count) count.textContent = '';
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadProjects);
  } else {
    loadProjects();
  }
})();
