/* Busywork or judgment sorter, AI band. Vanilla, no dependencies, and
   nothing leaves the page: no requests, no storage. Without this script
   the markup reads as the two column list. With it, the cards start in
   the pool; a tap or Enter moves a card to busywork, then to judgment
   and back; Left and Right arrows place it; a drag drops it on a column.
   The busywork column sums each card's fixed data-hours value. */
(function () {
  var root = document.getElementById('sorter');
  if (!root || !root.querySelector || !window.Element || !Element.prototype.closest) return;
  var pool = root.querySelector('.sorter-pool');
  var sum = root.querySelector('.sorter-sum');
  var lists = {};
  var cols = root.querySelectorAll('.sorter-col');
  Array.prototype.forEach.call(cols, function (col) {
    lists[col.getAttribute('data-col')] = col.querySelector('.sorter-list');
  });
  var cards = Array.prototype.slice.call(root.querySelectorAll('.sorter-card'));
  var drag = null;

  function total() {
    var t = 0;
    Array.prototype.forEach.call(lists.busywork.children, function (card) {
      t += Number(card.getAttribute('data-hours')) || 0;
    });
    sum.textContent = t;
  }

  function place(card, col) {
    lists[col].appendChild(card);
    card.setAttribute('data-in', col);
    total();
    card.querySelector('button').focus({ preventScroll: true });
  }

  function colAt(x, y, card) {
    card.style.visibility = 'hidden';
    var el = document.elementFromPoint(x, y);
    card.style.visibility = '';
    return el && el.closest ? el.closest('.sorter-col') : null;
  }

  function mark(col) {
    Array.prototype.forEach.call(cols, function (c) {
      c.classList.toggle('is-over', c === col);
    });
  }

  function end(card) {
    card.classList.remove('is-dragging');
    card.style.transform = '';
    mark(null);
  }

  cards.forEach(function (card) {
    var button = document.createElement('button');
    button.type = 'button';
    button.textContent = card.textContent;
    card.textContent = '';
    card.appendChild(button);
    pool.appendChild(card);

    card.addEventListener('click', function () {
      if (card.skipClick) { card.skipClick = false; return; }
      place(card, card.getAttribute('data-in') === 'busywork' ? 'judgment' : 'busywork');
    });

    button.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); place(card, 'busywork'); }
      if (e.key === 'ArrowRight') { e.preventDefault(); place(card, 'judgment'); }
    });

    card.addEventListener('pointerdown', function (e) {
      if (e.button !== 0) return;
      drag = { card: card, x: e.clientX, y: e.clientY, moved: false };
      card.setPointerCapture(e.pointerId);
    });

    card.addEventListener('pointermove', function (e) {
      if (!drag || drag.card !== card) return;
      var dx = e.clientX - drag.x;
      var dy = e.clientY - drag.y;
      if (!drag.moved && Math.abs(dx) + Math.abs(dy) < 6) return;
      drag.moved = true;
      card.classList.add('is-dragging');
      card.style.transform = 'translate(' + dx + 'px,' + dy + 'px)';
      mark(colAt(e.clientX, e.clientY, card));
    });

    card.addEventListener('pointerup', function (e) {
      if (!drag || drag.card !== card) return;
      var moved = drag.moved;
      drag = null;
      end(card);
      if (!moved) return;
      card.skipClick = true;
      setTimeout(function () { card.skipClick = false; }, 0);
      var col = colAt(e.clientX, e.clientY, card);
      if (col) place(card, col.getAttribute('data-col'));
    });

    card.addEventListener('pointercancel', function () {
      drag = null;
      end(card);
    });
  });

  total();
  root.classList.add('is-live');
})();
