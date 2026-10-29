/* Traffic beacon for the one page. Fires count.php once per band
   reached, with the band's anchor name as the page value, so the daily
   table keeps one row per band. Without script the page's noscript
   pixel fires one beacon for the page instead. */
(function () {
  function send(p) {
    var i = new Image();
    i.src = '/count.php?p=' + encodeURIComponent(p);
  }
  var bands = document.querySelectorAll('.band[id]');
  if (!('IntersectionObserver' in window)) { send('/'); return; }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        send(entry.target.id);
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -40% 0px' });
  Array.prototype.forEach.call(bands, function (band) { io.observe(band); });
})();
