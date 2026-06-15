(function () {
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

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initProjectFilters);
  } else {
    initProjectFilters();
  }
})();
