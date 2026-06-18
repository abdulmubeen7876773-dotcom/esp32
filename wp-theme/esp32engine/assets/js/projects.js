/* ESP32 Engine — Projects archive filter (loaded on archive + taxonomy pages) */
(function () {
  'use strict';

  var grid    = document.getElementById('projects-grid');
  var search  = document.getElementById('project-search');
  var catSel  = document.getElementById('filter-category');
  var diffSel = document.getElementById('filter-difficulty');
  var count   = document.getElementById('filter-count');
  var noRes   = document.getElementById('no-results');
  var clear   = document.getElementById('clear-filters');

  if ( !grid ) return;

  var cards = Array.from(grid.querySelectorAll('.project-card-item'));

  function filter() {
    var q    = search  ? search.value.toLowerCase().trim() : '';
    var cat  = catSel  ? catSel.value  : '';
    var diff = diffSel ? diffSel.value : '';
    var shown = 0;

    cards.forEach(function (card) {
      var title    = card.dataset.title       || '';
      var cardCat  = card.dataset.category    || '';
      var cardDiff = (card.dataset.difficulties || '').split(',');
      var ok = (!q    || title.includes(q))
            && (!cat  || cardCat === cat)
            && (!diff || cardDiff.indexOf(diff) !== -1);
      card.classList.toggle('hidden', !ok);
      if (ok) shown++;
    });

    if (count) count.textContent = shown + ' project' + (shown !== 1 ? 's' : '');
    if (noRes) noRes.classList.toggle('hidden', shown > 0);
  }

  if (search)  search.addEventListener('input',  filter);
  if (catSel)  catSel.addEventListener('change', filter);
  if (diffSel) diffSel.addEventListener('change', filter);

  if (clear) {
    clear.addEventListener('click', function () {
      if (search)  search.value  = '';
      if (catSel)  catSel.value  = '';
      if (diffSel) diffSel.value = '';
      filter();
    });
  }

  // Seed from URL ?s= param
  var params = new URLSearchParams(window.location.search);
  var qs = params.get('s') || params.get('q') || '';
  if (qs && search) { search.value = qs; }

  filter();
})();
