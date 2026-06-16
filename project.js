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

window.addEventListener('load', function () {
  document.querySelectorAll('.faq-item.open .faq-a').forEach(function (a) {
    a.style.maxHeight = a.scrollHeight + 'px';
  });

  var tocLinks = document.querySelectorAll('.side-toc a[href^="#"]');
  var sections = [];
  tocLinks.forEach(function (link) {
    var id = link.getAttribute('href').slice(1);
    var el = document.getElementById(id);
    if (el) sections.push({ id: id, el: el, link: link });
  });

  if (sections.length) {
    var ticking = false;
    function updateToc() {
      var scrollY = window.scrollY + 120;
      var current = sections[0];
      sections.forEach(function (s) {
        if (s.el.offsetTop <= scrollY) current = s;
      });
      tocLinks.forEach(function (l) {
        l.classList.remove('is-active');
      });
      if (current) current.link.classList.add('is-active');
      ticking = false;
    }
    window.addEventListener(
      'scroll',
      function () {
        if (!ticking) {
          window.requestAnimationFrame(updateToc);
          ticking = true;
        }
      },
      { passive: true }
    );
    updateToc();
  }
});

function copyCode(btn) {
  var pre = document.getElementById('code-content');
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
