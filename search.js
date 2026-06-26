(function () {
  var index = null;
  var loading = fetch('/search-index.json')
    .then(function (r) { return r.json(); })
    .then(function (data) { index = data; return data; })
    .catch(function () { index = []; return []; });

  function normalize(s) {
    return (s || '').toLowerCase().trim();
  }

  function search(q, limit) {
    var term = normalize(q);
    if (!term || !index) return [];
    return index.filter(function (item) {
      return normalize(item.title).indexOf(term) !== -1 ||
        normalize(item.desc).indexOf(term) !== -1 ||
        normalize(item.type).indexOf(term) !== -1;
    }).slice(0, limit || 8);
  }

  function renderResults(container, results) {
    if (!container) return;
    if (!results.length) {
      container.innerHTML = '<p class="meta">No results found. Try another word.</p>';
      container.hidden = false;
      return;
    }
    container.innerHTML = results.map(function (item) {
      return '<a class="search-result-item" href="' + item.href + '">' +
        '<span class="search-result-type">' + item.type + '</span> ' +
        '<strong>' + item.title + '</strong>' +
        (item.desc ? '<br><span class="meta">' + item.desc.substring(0, 90) + '</span>' : '') +
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
