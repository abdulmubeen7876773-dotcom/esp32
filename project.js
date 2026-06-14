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

var sections = document.querySelectorAll('main section, header.hero');
var navLinks = document.querySelectorAll('.nav-links a');
var idToLink = {};
navLinks.forEach(function (l) {
  var href = l.getAttribute('href');
  if (href && href.charAt(0) === '#') idToLink[href.slice(1)] = l;
});

if (sections.length && navLinks.length) {
  var observer = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          var id = entry.target.id;
          navLinks.forEach(function (l) {
            l.classList.remove('active');
          });
          if (idToLink[id]) idToLink[id].classList.add('active');
        }
      });
    },
    { rootMargin: '-40% 0px -55% 0px', threshold: 0 }
  );
  document.querySelectorAll('main section[id], header.hero[id]').forEach(function (s) {
    observer.observe(s);
  });
}
