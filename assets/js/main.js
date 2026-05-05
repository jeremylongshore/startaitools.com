/* Dispatch — main.js
   No dependencies. Defers cleanly. Pagefind loaded on-demand.
*/
(function () {
  'use strict';

  var prefersReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- Theme toggle ---------- */
  var themeBtn = document.getElementById('theme-toggle');
  if (themeBtn) {
    var iconDark = themeBtn.querySelector('.theme-icon-dark');
    var iconLight = themeBtn.querySelector('.theme-icon-light');
    function applyIcon() {
      var t = document.documentElement.getAttribute('data-theme') || 'dark';
      if (iconDark) iconDark.style.display = t === 'dark' ? '' : 'none';
      if (iconLight) iconLight.style.display = t === 'light' ? '' : 'none';
    }
    applyIcon();
    themeBtn.addEventListener('click', function () {
      var current = document.documentElement.getAttribute('data-theme') || 'dark';
      var next = current === 'dark' ? 'light' : 'dark';
      // Use View Transitions API where available
      if (typeof document.startViewTransition === 'function' && !prefersReduced) {
        document.startViewTransition(function () {
          document.documentElement.setAttribute('data-theme', next);
          applyIcon();
        });
      } else {
        document.documentElement.setAttribute('data-theme', next);
        applyIcon();
      }
      try { localStorage.setItem('theme', next); } catch (e) {}
    });
  }

  /* ---------- Mobile menu ---------- */
  var menuBtn = document.getElementById('mobile-menu-btn');
  var navLinks = document.getElementById('nav-links');
  if (menuBtn && navLinks) {
    menuBtn.addEventListener('click', function () {
      var open = navLinks.classList.toggle('is-open');
      menuBtn.setAttribute('aria-expanded', String(open));
    });
  }

  /* ---------- Scroll reveal ---------- */
  if ('IntersectionObserver' in window && !prefersReduced) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          io.unobserve(e.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.05 });
    document.querySelectorAll('[data-reveal]').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('[data-reveal]').forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- Reading progress ---------- */
  var progress = document.getElementById('reading-progress');
  if (progress) {
    var ticking = false;
    function update() {
      var doc = document.documentElement;
      var scrollTop = window.scrollY || doc.scrollTop;
      var height = doc.scrollHeight - doc.clientHeight;
      var pct = height > 0 ? (scrollTop / height) * 100 : 0;
      progress.style.width = pct + '%';
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }

  /* ---------- Stats counter ---------- */
  function animateCount(el) {
    if (prefersReduced) {
      el.textContent = el.dataset.count;
      return;
    }
    var target = parseInt(el.dataset.count, 10);
    if (isNaN(target)) { el.textContent = el.dataset.count; return; }
    var duration = 1200;
    var start = performance.now();
    function step(now) {
      var elapsed = now - start;
      var t = Math.min(1, elapsed / duration);
      // ease-out cubic
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(target * eased).toLocaleString();
      if (t < 1) requestAnimationFrame(step);
      else el.textContent = target.toLocaleString();
    }
    requestAnimationFrame(step);
  }
  if ('IntersectionObserver' in window) {
    var counters = document.querySelectorAll('[data-count]');
    if (counters.length) {
      var co = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { animateCount(e.target); co.unobserve(e.target); }
        });
      }, { threshold: 0.5 });
      counters.forEach(function (el) { co.observe(el); });
    }
  } else {
    document.querySelectorAll('[data-count]').forEach(function (el) { el.textContent = el.dataset.count; });
  }

  /* ---------- Search (Pagefind) ---------- */
  var searchModal = document.getElementById('search-modal');
  var searchOpen = document.getElementById('search-open');
  var pagefindMount = document.getElementById('pagefind-search');
  var pagefindLoaded = false;

  function loadPagefind() {
    if (pagefindLoaded || !pagefindMount) return Promise.resolve();
    pagefindLoaded = true;
    return import('/pagefind/pagefind-ui.js')
      .then(function () {
        // PagefindUI is global after import
        if (window.PagefindUI) {
          new window.PagefindUI({
            element: '#pagefind-search',
            showSubResults: true,
            showImages: false,
            resetStyles: false,
            translations: { placeholder: 'Search 240+ posts…' }
          });
        } else {
          renderFallback();
        }
      })
      .catch(function () { renderFallback(); });
  }

  function renderFallback() {
    if (!pagefindMount) return;
    pagefindMount.innerHTML =
      '<div style="padding:1.5rem;color:var(--fg-muted);font-family:var(--font-sans);font-size:0.95rem">' +
      '<p style="margin:0 0 0.75rem"><strong>Search index not yet built.</strong></p>' +
      '<p style="margin:0">Run <code>npx pagefind --site public</code> after <code>hugo</code> to enable on-page search. ' +
      'In the meantime, <a href="/posts/" style="color:var(--accent-warm)">browse all posts</a>.</p>' +
      '</div>';
  }

  function openSearch() {
    if (!searchModal) return;
    searchModal.classList.add('is-open');
    document.body.style.overflow = 'hidden';
    loadPagefind().then(function () {
      var input = searchModal.querySelector('input[type="text"], input[type="search"]');
      if (input) setTimeout(function () { input.focus(); }, 50);
    });
  }
  function closeSearch() {
    if (!searchModal) return;
    searchModal.classList.remove('is-open');
    document.body.style.overflow = '';
  }

  if (searchOpen) searchOpen.addEventListener('click', openSearch);
  if (searchModal) {
    searchModal.addEventListener('click', function (e) { if (e.target === searchModal) closeSearch(); });
  }
  document.addEventListener('keydown', function (e) {
    var isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
    if ((isMac ? e.metaKey : e.ctrlKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (searchModal && searchModal.classList.contains('is-open')) closeSearch();
      else openSearch();
    } else if (e.key === 'Escape' && searchModal && searchModal.classList.contains('is-open')) {
      closeSearch();
    } else if (e.key === '/' && document.activeElement === document.body) {
      e.preventDefault();
      openSearch();
    }
  });

  /* ---------- Mark current TOC heading on scroll ---------- */
  var tocLinks = document.querySelectorAll('.toc a[href^="#"]');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var headingMap = {};
    tocLinks.forEach(function (a) {
      var id = decodeURIComponent(a.getAttribute('href').slice(1));
      var heading = document.getElementById(id);
      if (heading) headingMap[id] = a;
    });
    var hIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        var id = e.target.id;
        var link = headingMap[id];
        if (link) {
          if (e.isIntersecting) link.classList.add('is-current');
          else link.classList.remove('is-current');
        }
      });
    }, { rootMargin: '-15% 0px -70% 0px' });
    Object.keys(headingMap).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) hIo.observe(el);
    });
  }
})();
