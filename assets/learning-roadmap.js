/* Optional Learning-page tools. No analytics, network requests or automatic completion. */
(() => {
  'use strict';
  const root = document.querySelector('#learning-roadmap');
  const source = document.querySelector('#lr-data');
  if (!root || !source) return;
  let data;
  try { data = JSON.parse(source.textContent); } catch { return; }
  const $ = s => root.querySelector(s);
  const all = s => [...root.querySelectorAll(s)];
  const topics = data.paths.flatMap(path => path.topics.map(topic => ({...topic, path})));
  const ready = topics.filter(t => t.href);
  const byId = new Map(ready.map(t => [t.id, t]));
  const order = [...new Set([...data.starter_ids, ...ready.map(t => t.id)])].filter(id => byId.has(id));
  const key = 'esp32-learning-roadmap-v1';
  let completed = new Set();
  let last = null;
  let active = null;
  let saving = false;
  try {
    const saved = JSON.parse(localStorage.getItem(key) || 'null');
    if (saved && saved.version === 1 && Array.isArray(saved.completed)) {
      completed = new Set(saved.completed.filter(id => byId.has(id)));
      last = byId.has(saved.last) ? saved.last : null;
      saving = true;
    }
  } catch { /* Progress remains usable in memory if storage is blocked/corrupt. */ }
  function status(message) { $('#lr-status').textContent = message; }
  function save() {
    if (!saving) return;
    try {
      localStorage.setItem(key, JSON.stringify({version:1, completed:[...completed], last}));
    } catch {
      saving = false;
      $('#lr-save').checked = false;
      $('#lr-storage-note').textContent = 'Saving is unavailable in this browser. Progress will last only while this page stays open.';
      status('Progress still works in this tab; it could not be saved.');
    }
  }
  function nextId() {
    if (last && !completed.has(last)) return last;
    return order.find(id => !completed.has(id));
  }
  function update() {
    all('[data-complete]').forEach(input => { input.checked = completed.has(input.dataset.complete); });
    all('.lr-topic').forEach(row => { row.dataset.completed = String(completed.has(row.id)); });
    $('#lr-progress').value = completed.size;
    $('#lr-progress').max = ready.length;
    $('#lr-progress-label').textContent = `${completed.size} of ${ready.length} linked topics completed`;
    const next = byId.get(nextId());
    $('#lr-next-label').textContent = next ? next.title : 'You marked every linked topic complete. Revisit a path or try another build.';
    $('#lr-next').href = next ? next.href : '/projects.html';
    $('#lr-next').textContent = next ? (completed.size || last ? 'Continue learning →' : 'Start with Arduino IDE →') : 'Explore projects →';
    $('#lr-continue-title').textContent = completed.size ? 'Keep your momentum.' : 'Your next step is ready.';
    if (active) $('#lr-desk-done').textContent = completed.has(active.id) ? 'Mark as not complete' : 'Mark topic complete';
  }
  function toggleComplete(id, done) {
    if (!byId.has(id)) return;
    if (done) completed.add(id); else completed.delete(id);
    if (done && last === id) last = null;
    save(); update();
    status(`${byId.get(id).title}: ${done ? 'marked complete' : 'marked not complete'}.`);
  }
  function openDesk(id, focus = true) {
    const topic = byId.get(id);
    if (!topic) return;
    active = topic; last = id;
    const path = topic.path;
    $('#lr-desk-topic').textContent = `${path.label} · ${topic.title}`;
    $('#lr-outcome').textContent = path.outcome;
    $('#lr-parts').textContent = path.parts;
    $('#lr-challenge').textContent = path.challenge;
    $('#lr-desk-guide').href = topic.href;
    $('#lr-question').textContent = path.quiz.question;
    $('#lr-answers').replaceChildren();
    path.quiz.answers.forEach((answer, index) => {
      const label = document.createElement('label');
      const input = document.createElement('input');
      input.type = 'radio'; input.name = 'lr-answer'; input.value = String(index); input.required = true;
      label.append(input, document.createTextNode(answer));
      $('#lr-answers').append(label);
    });
    $('#lr-feedback').textContent = '';
    $('#learning-desk').hidden = false;
    save(); update();
    if (focus) {
      $('#learning-desk').scrollIntoView({behavior:'instant', block:'start'});
      $('#lr-desk-title').focus({preventScroll:true});
    }
  }
  all('[data-preview]').forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => openDesk(button.dataset.preview));
  });
  all('.lr-done').forEach(label => { label.hidden = false; });
  all('[data-complete]').forEach(input => {
    input.addEventListener('change', () => toggleComplete(input.dataset.complete, input.checked));
  });
  all('[data-study]').forEach(link => {
    link.addEventListener('click', () => { last = link.dataset.study; save(); });
  });
  $('#lr-next').addEventListener('click', () => { last = nextId() || null; save(); });
  $('#lr-save').checked = saving;
  $('#lr-save').addEventListener('change', event => {
    saving = event.target.checked;
    if (saving) {
      save();
      if (saving) status('Progress saving enabled for this browser on this device.');
    } else {
      try {
        localStorage.removeItem(key);
        status('Saved progress removed. Your current tab keeps its progress until closed.');
      } catch {
        status('Saving turned off. Browser storage could not be accessed to clear the saved copy.');
      }
    }
  });
  let resetRequested = false;
  $('#lr-reset').addEventListener('click', () => {
    if (!resetRequested) {
      resetRequested = true;
      $('#lr-reset').textContent = 'Confirm: clear my progress';
      status('Click Confirm to clear completed topics and your resume point.');
      return;
    }
    completed.clear(); last = null; resetRequested = false;
    $('#lr-reset').textContent = 'Clear my progress';
    save(); update(); status('Progress cleared. Choose a topic to start again.');
  });
  $('#lr-desk-done').addEventListener('click', () => {
    if (active) toggleComplete(active.id, !completed.has(active.id));
  });
  $('#lr-desk-next').addEventListener('click', () => {
    if (!active) return;
    const index = ready.findIndex(t => t.id === active.id);
    const following = ready.slice(index + 1).find(t => !completed.has(t.id)) || ready.find(t => t.id !== active.id && !completed.has(t.id));
    if (following) openDesk(following.id);
    else $('#lr-feedback').textContent = 'No other incomplete linked topics remain. You can revisit any study guide.';
  });
  $('#lr-quiz').addEventListener('submit', event => {
    event.preventDefault();
    if (!active) return;
    const selected = $('#lr-answers input:checked');
    if (!selected) return;
    const correct = Number(selected.value) === active.path.quiz.correct;
    $('#lr-feedback').textContent = `${correct ? 'That’s right.' : 'Not quite — try again.'} ${active.path.quiz.explanation}`;
  });
  const kits = {board:'topic-011', led:'topic-031', button:'topic-034', dht:'topic-051', oled:'topic-063'};
  $('#lr-kit-form').addEventListener('submit', event => {
    event.preventDefault();
    const topic = byId.get(kits[$('#lr-kit-select').value]);
    $('#lr-kit-result').replaceChildren(document.createTextNode('Suggested exercise: '));
    const link = document.createElement('a'); link.href = topic.href; link.textContent = topic.title;
    $('#lr-kit-result').append(link, document.createTextNode('. Complete the earlier beginner steps first if you have not already.'));
    openDesk(topic.id, false);
  });
  const pathNodes = all('.lr-path');
  const initialOpen = new Map(pathNodes.map(p => [p.id, p.open]));
  function filter() {
    const query = $('#lr-search').value.trim().toLocaleLowerCase();
    const level = $('#lr-level').value;
    const availability = $('#lr-availability').value;
    const filtering = !!query || level !== 'all' || availability !== 'all';
    let count = 0, paths = 0;
    pathNodes.forEach(path => {
      let matches = 0;
      path.querySelectorAll('.lr-topic').forEach(topic => {
        const text = topic.querySelector('h4').textContent.toLocaleLowerCase();
        const show = (!query || text.includes(query)) && (level === 'all' || path.dataset.level === level) && (availability === 'all' || (availability === 'ready') === (topic.dataset.ready === 'true'));
        topic.hidden = !show;
        if (show) matches++;
      });
      path.hidden = matches === 0;
      if (matches) { paths++; count += matches; }
      path.open = filtering && !!matches ? true : initialOpen.get(path.id);
    });
    $('#lr-results').textContent = `${count} topic${count === 1 ? '' : 's'} across ${paths} path${paths === 1 ? '' : 's'}`;
    $('#lr-no-results').hidden = count !== 0;
  }
  $('#lr-search').addEventListener('input', filter);
  $('#lr-level').addEventListener('change', filter);
  $('#lr-availability').addEventListener('change', filter);
  $('#lr-clear').addEventListener('click', () => {
    $('#lr-search').value = ''; $('#lr-level').value = 'all'; $('#lr-availability').value = 'all'; filter();
  });
  all('.lr-path-nav a').forEach(link => link.addEventListener('click', () => {
    $('#lr-search').value = ''; $('#lr-level').value = 'all'; $('#lr-availability').value = 'all'; filter();
    const target = root.querySelector(link.getAttribute('href'));
    if (target) target.open = true;
    all('.lr-path-nav a').forEach(a => a.removeAttribute('aria-current'));
    link.setAttribute('aria-current', 'location');
  }));
  function revealHash() {
    if (!location.hash) return;
    let fragment;
    try { fragment = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = document.getElementById(fragment);
    const path = target && (target.classList.contains('lr-path') ? target : target.closest('.lr-path'));
    if (path) path.open = true;
  }
  window.addEventListener('hashchange', revealHash);
  ['.lr-continue', '.lr-kit', '.lr-filters'].forEach(s => { $(s).hidden = false; });
  update(); revealHash();
})();
