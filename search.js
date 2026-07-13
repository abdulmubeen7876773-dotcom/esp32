(function () {
  var index = null;
  var loading = fetch('/search-index.json')
    .then(function (r) { return r.json(); })
    .then(function (data) { index = data; return data; })
    .catch(function () { index = []; return []; });

  function normalize(s) {
    if (Array.isArray(s)) return s.map(normalize).join(' ');
    return String(s || '').toLowerCase().trim();
  }

  function haystack(item) {
    return [
      item.title,
      item.desc,
      item.type,
      item.category,
      item.slug
    ].map(normalize).join(' ');
  }

  function search(q, limit) {
    var term = normalize(q);
    if (!term || !index) return [];
    var terms = term.split(/\s+/).filter(Boolean);
    return index.filter(function (item) {
      var text = haystack(item);
      return terms.every(function (t) { return text.indexOf(t) !== -1; });
    }).slice(0, limit || 8);
  }

  function snippet(text, max) {
    if (!text) return '';
    var clean = text.replace(/\s+/g, ' ').trim();
    return clean.length <= max ? clean : clean.substring(0, max - 1).trim() + '…';
  }

  function esc(text) {
    var d = document.createElement('div');
    d.textContent = text || '';
    return d.innerHTML;
  }

  function renderResults(container, results) {
    if (!container) return;
    if (!results.length) {
      container.innerHTML = '<p class="meta">No results found. Try another word.</p>';
      container.hidden = false;
      return;
    }
    container.innerHTML = results.map(function (item) {
      var cat = item.category ? '<span class="search-result-cat">' + esc(item.category) + '</span>' : '';
      return '<a class="search-result-item" href="' + esc(item.href) + '">' +
        '<span class="search-result-head">' +
        '<span class="search-result-type">' + esc(item.type) + '</span>' + cat +
        '</span>' +
        '<strong class="search-result-title">' + esc(item.title) + '</strong>' +
        (item.desc ? '<span class="search-result-desc">' + esc(snippet(item.desc, 120)) + '</span>' : '') +
        '</a>';
    }).join('');
    container.hidden = false;
  }

  function setupLiveSearch(input, resultsEl) {
    if (!input || !resultsEl) return;
    var timer;
    input.addEventListener('input', function () {
      clearTimeout(timer);
      timer = setTimeout(function () {
        loading.then(function () {
          renderResults(resultsEl, search(input.value, 6));
        });
      }, 200);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    loading.then(function () {
      setupLiveSearch(
        document.getElementById('global-search'),
        document.getElementById('search-results-live')
      );
      var pageInput = document.getElementById('search-page-input');
      var pageResults = document.getElementById('search-page-results');
      if (pageInput && pageResults) {
        var params = new URLSearchParams(window.location.search);
        var q = params.get('q');
        if (q) {
          pageInput.value = q;
          renderResults(pageResults, search(q, 20));
        }
        setupLiveSearch(pageInput, pageResults);
      }
    });
  });
})();
