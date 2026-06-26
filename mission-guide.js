(function () {
  document.querySelectorAll('.btn-copy[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var panel = btn.closest('.code-panel');
      var code = panel && panel.querySelector('code');
      if (!code) return;
      var text = code.textContent;
      function done() {
        btn.textContent = 'Copied!';
        setTimeout(function () { btn.textContent = 'Copy'; }, 2000);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(function () {
          fallbackCopy(text, done);
        });
      } else {
        fallbackCopy(text, done);
      }
    });
  });

  function fallbackCopy(text, done) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.left = '-9999px';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); done(); } catch (e) {}
    document.body.removeChild(ta);
  }

  document.querySelectorAll('.quiz-question').forEach(function (block) {
    var feedback = block.querySelector('.quiz-feedback');
    var explanation = block.getAttribute('data-explanation') || '';
    block.querySelectorAll('.quiz-option').forEach(function (opt) {
      opt.addEventListener('click', function () {
        if (block.classList.contains('answered')) return;
        block.classList.add('answered');
        var correct = opt.getAttribute('data-correct') === '1';
        opt.classList.add(correct ? 'is-correct' : 'is-wrong');
        if (!correct) {
          block.querySelectorAll('.quiz-option[data-correct="1"]').forEach(function (c) {
            c.classList.add('is-correct');
          });
        }
        if (feedback) {
          feedback.hidden = false;
          feedback.textContent = correct
            ? 'Correct! ' + explanation
            : 'Not quite — ' + explanation;
          feedback.classList.toggle('is-success', correct);
          feedback.classList.toggle('is-error', !correct);
        }
      });
    });
  });
})();
