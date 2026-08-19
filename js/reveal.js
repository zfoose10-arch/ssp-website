/* Scroll reveal. This script alone creates the hidden state: sections in
   view at load are marked seen first, then the js-reveal class arms the
   stylesheet. With JavaScript absent or failed, nothing is ever hidden. */
(function () {
  if (!('IntersectionObserver' in window)) return;
  var sections = document.querySelectorAll('.site-main > section');
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-seen');
        io.unobserve(entry.target);
      }
    });
  });
  sections.forEach(function (section) {
    if (section.getBoundingClientRect().top < window.innerHeight) {
      section.classList.add('is-seen');
    } else {
      io.observe(section);
    }
  });
  document.documentElement.classList.add('js-reveal');
})();
