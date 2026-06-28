(function () {
  var PAGE_SIZE = 12;

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

  function badgeClass(level) {
    var d = (level || '').toLowerCase();
    if (d === 'advanced') return 'badge-advanced';
    if (d === 'intermediate') return 'badge-intermediate';
    return 'badge-beginner';
  }

  function readTime(slug) {
    var base = 8;
    if (slug) base += slug.length % 5;
    return base + ' min read';
  }

  function thumbHtml(category, image) {
    var icons = window.PROJECT_ICONS || {};
    var thumbs = window.PROJECT_THUMBS || {};
    var svg = icons[category] || icons.__default__ || '';
    var cls = thumbs[category] || 't-default';
    if (image) {
      return (
        '<div class="card-media card-media--has-image"><img class="card-media-img" src="' +
        esc(image) +
        '" alt="" loading="lazy" decoding="async"><div class="card-media-fallback ' +
        cls +
        '">' +
        svg +
        '</div></div>'
      );
    }
    return '<div class="card-media"><div class="card-thumb ' + cls + '">' + svg + '</div></div>';
  }

  function levelBadges(levels) {
    var list = levels || ['Beginner', 'Intermediate', 'Advanced'];
    return list
      .map(function (lv) {
        return '<span class="badge ' + badgeClass(lv) + '">' + esc(lv) + '</span>';
      })
      .join('');
  }

  function cardHtml(p) {
    var desc = p.desc || '';
    var descHtml = desc ? '<p class="card-desc">' + esc(desc) + '</p>' : '';
    var levels = p.levels || ['Beginner', 'Intermediate', 'Advanced'];
    var levelsStr = levels.join(',');
    var rt = readTime(p.slug || '');
    return (
      '<a class="card project-card modern-card project-card-item" href="' +
      esc(p.href) +
      '" data-title="' +
      esc((p.title || '').toLowerCase()) +
      '" data-category="' +
      esc(p.category || '') +
      '" data-levels="' +
      esc(levelsStr) +
      '" data-featured="' +
      (p.featured ? '1' : '0') +
      '">' +
      '<div class="card-media-wrap">' +
      thumbHtml(p.category, p.featured_image || p.image || '') +
      '</div>' +
      '<div class="card-body"><div class="card-badges"><span class="badge badge-cat">' +
      esc(shortCategory(p.category)) +
      '</span>' +
      levelBadges(levels) +
      '<span class="badge badge-time">' +
      esc(rt) +
      '</span></div><h3>' +
      esc(p.title) +
      '</h3>' +
      descHtml +
      '<div class="card-footer"><span class="btn btn-card">Read More<span aria-hidden="true">→</span></span></div></div></a>'
    );
  }

  function renderProjects(projects, done) {
    var grid = document.getElementById('grid');
    if (!grid) {
      if (done) done();
      return;
    }
    grid.innerHTML = projects.map(cardHtml).join('');
    var textIndex = document.getElementById('project-text-index');
    if (textIndex) textIndex.classList.add('hidden');
    if (done) done();
  }

  function getVisibleCards() {
    return Array.prototype.slice
      .call(document.querySelectorAll('.project-card'))
      .filter(function (card) {
        return !card.classList.contains('filter-hidden');
      });
  }

  function applyPagination() {
    var g = document.getElementById('grid');
    var wrap = document.getElementById('projects-more-wrap');
    var btn = document.getElementById('projects-load-more');
    var cards = getVisibleCards();
    var expanded = g && g.dataset.expanded === '1';
    var shown = 0;
    cards.forEach(function (card, i) {
      var hide = i >= PAGE_SIZE && !expanded;
      card.classList.toggle('page-hidden', hide);
      if (!hide) shown++;
    });
    if (wrap && btn) {
      var needMore = cards.length > PAGE_SIZE && !expanded;
      wrap.style.display = needMore ? '' : 'none';
      if (needMore) {
        btn.textContent = 'Load More (' + (cards.length - PAGE_SIZE) + ')';
      }
    }
    return shown;
  }

  function initProjectFilters() {
    var q = document.getElementById('q');
    var cat = document.getElementById('cat');
    var diff = document.getElementById('diff');
    var sort = document.getElementById('sort');
    var count = document.getElementById('count');
    grid = document.getElementById('grid');
    if (!q || !cat || !diff || !count || !grid) return;

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

    function sortCards() {
      if (!sort) return;
      var cards = getCards().slice();
      var mode = sort.value || 'featured';
      cards.sort(function (a, b) {
        if (mode === 'title') {
          return (a.dataset.title || '').localeCompare(b.dataset.title || '');
        }
        if (mode === 'category') {
          return (a.dataset.category || '').localeCompare(b.dataset.category || '');
        }
        return (parseInt(b.dataset.featured || '0', 10) || 0) - (parseInt(a.dataset.featured || '0', 10) || 0);
      });
      cards.forEach(function (card) {
        grid.appendChild(card);
      });
    }

    function filterProjects() {
      var g = document.getElementById('grid');
      if (g) g.dataset.expanded = '';
      var search = q.value.toLowerCase().trim();
      var category = cat.value;
      var difficulty = diff.value;
      getCards().forEach(function (card) {
        var title = card.dataset.title || '';
        var cardCat = card.dataset.category || '';
        var levels = (card.dataset.levels || '').split(',');
        var ok =
          (!search || title.indexOf(search) !== -1) &&
          (!category || cardCat === category) &&
          (!difficulty || levels.indexOf(difficulty) !== -1);
        card.classList.toggle('filter-hidden', !ok);
      });
      sortCards();
      var visible = applyPagination();
      count.textContent = getVisibleCards().length + ' projects found · showing ' + visible;
    }

    [q, cat, diff].forEach(function (el) {
      el.addEventListener('input', filterProjects);
      el.addEventListener('change', filterProjects);
    });
    if (sort) {
      sort.addEventListener('change', filterProjects);
    }

    var loadBtn = document.getElementById('projects-load-more');
    if (loadBtn) {
      loadBtn.addEventListener('click', function () {
        var g = document.getElementById('grid');
        if (g) g.dataset.expanded = '1';
        getVisibleCards().forEach(function (card) {
          card.classList.remove('page-hidden');
        });
        var wrap = document.getElementById('projects-more-wrap');
        if (wrap) wrap.style.display = 'none';
        count.textContent = getVisibleCards().length + ' projects found';
      });
    }

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

  function showTextFallback() {
    var textIndex = document.getElementById('project-text-index');
    if (textIndex) textIndex.classList.remove('hidden');
  }

  function loadProjects() {
    grid = document.getElementById('grid');
    if (!grid) return;

    if (document.querySelectorAll('.project-card').length) {
      initProjectFilters();
      return;
    }

    fetch('projects.json')
      .then(function (res) {
        if (!res.ok) throw new Error('Failed to load projects');
        return res.json();
      })
      .then(function (projects) {
        renderProjects(projects, function () {
          initProjectFilters();
        });
      })
      .catch(function () {
        showTextFallback();
        if (!document.querySelectorAll('.project-card').length) {
          grid.innerHTML =
            '<p class="meta">Could not load the project library. Use the plain-text index below or the <a href="sitemap.html">sitemap</a>.</p>';
        }
        initProjectFilters();
      });

    if (document.querySelectorAll('.project-card').length) {
      initProjectFilters();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadProjects);
  } else {
    loadProjects();
  }
})();
