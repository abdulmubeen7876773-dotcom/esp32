(function () {
  document.querySelectorAll('.btn-copy[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var panel = btn.closest('.code-panel');
      var code = panel && panel.querySelector('code');
      if (!code) return;
      var text = code.textContent;
      var label = btn.querySelector('.btn-copy-label');
      function done() {
        btn.classList.add('is-copied');
        btn.setAttribute('aria-label', 'Code copied to clipboard');
        if (label) label.textContent = 'Copied!';
        setTimeout(function () {
          btn.classList.remove('is-copied');
          btn.setAttribute('aria-label', 'Copy code to clipboard');
          if (label) label.textContent = 'Copy';
        }, 2000);
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
    var correctFeedback = block.getAttribute('data-correct-feedback') || '';
    var wrongFeedback = block.getAttribute('data-wrong-feedback') || '';
    block.querySelectorAll('.quiz-option').forEach(function (opt) {
      opt.addEventListener('click', function () {
        if (block.classList.contains('answered')) return;
        block.classList.add('answered');
        var correct = opt.getAttribute('data-correct') === '1';
        opt.classList.add(correct ? 'is-correct' : 'is-wrong');
        opt.setAttribute('aria-pressed', 'true');
        if (!correct) {
          block.querySelectorAll('.quiz-option[data-correct="1"]').forEach(function (c) {
            c.classList.add('is-correct');
            c.setAttribute('aria-pressed', 'true');
          });
        }
        block.querySelectorAll('.quiz-option').forEach(function (o) {
          o.disabled = true;
        });
        if (feedback) {
          feedback.hidden = false;
          if (correct) {
            feedback.textContent = correctFeedback
              ? correctFeedback + (explanation ? ' ' + explanation : '')
              : 'Correct! ' + explanation;
          } else {
            feedback.textContent = wrongFeedback
              ? wrongFeedback + (explanation ? ' ' + explanation : '')
              : 'Not quite — ' + explanation;
          }
          feedback.classList.toggle('is-success', correct);
          feedback.classList.toggle('is-error', !correct);
        }
      });
    });
  });
})();
