/**
 * Layout Selector - Clean visual preferences
 * No tracking, just CSS class switching
 */

(function() {
  'use strict';

  const LAYOUTS = {
    compact: {
      name: 'Compact',
      icon: '📱',
      class: 'layout-compact'
    },
    standard: {
      name: 'Standard',
      icon: '💻',
      class: 'layout-standard'
    },
    wide: {
      name: 'Wide',
      icon: '🖥️',
      class: 'layout-wide'
    }
  };

  function init() {
    // Get saved preference or default
    const saved = localStorage.getItem('layout-preference') || 'standard';
    applyLayout(saved);

    // Add selector to page
    addLayoutSelector(saved);
  }

  function addLayoutSelector(current) {
    const selector = document.createElement('div');
    selector.className = 'layout-selector';
    selector.innerHTML = `
      ${Object.entries(LAYOUTS).map(([key, layout]) => `
        <button class="layout-btn ${current === key ? 'active' : ''}"
                data-layout="${key}"
                title="${layout.name} View">
          ${layout.icon}
        </button>
      `).join('')}
    `;

    // Add to page (top right corner)
    document.body.appendChild(selector);

    // Handle clicks
    selector.querySelectorAll('.layout-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const layout = btn.dataset.layout;

        // Update active state
        selector.querySelectorAll('.layout-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        // Apply layout
        applyLayout(layout);
        localStorage.setItem('layout-preference', layout);
      });
    });
  }

  function applyLayout(layout) {
    // Remove all layout classes
    Object.values(LAYOUTS).forEach(l => {
      document.body.classList.remove(l.class);
    });

    // Add selected layout class
    if (LAYOUTS[layout]) {
      document.body.classList.add(LAYOUTS[layout].class);
    }
  }

  // Add styles
  const style = document.createElement('style');
  style.textContent = `
    /* Layout Selector */
    .layout-selector {
      position: fixed;
      top: 20px;
      right: 20px;
      display: flex;
      gap: 4px;
      background: rgba(0, 0, 0, 0.8);
      padding: 4px;
      border-radius: 8px;
      z-index: 1000;
      border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .layout-btn {
      background: transparent;
      border: 1px solid transparent;
      padding: 8px 12px;
      cursor: pointer;
      font-size: 18px;
      border-radius: 4px;
      transition: all 0.2s ease;
      opacity: 0.7;
    }

    .layout-btn:hover {
      opacity: 1;
      background: rgba(255, 255, 255, 0.1);
    }

    .layout-btn.active {
      background: rgba(255, 255, 0, 0.2);
      border-color: var(--pac-yellow, #FFFF00);
      opacity: 1;
    }

    /* Compact Layout */
    .layout-compact {
      font-size: 14px;
    }

    .layout-compact .book-page {
      max-width: 100%;
      padding: 1rem;
    }

    .layout-compact h1 { font-size: 1.8em; }
    .layout-compact h2 { font-size: 1.5em; }
    .layout-compact h3 { font-size: 1.2em; }

    .layout-compact .book-menu {
      width: 200px;
    }

    .layout-compact pre {
      padding: 0.5rem;
      font-size: 12px;
    }

    /* Wide Layout */
    .layout-wide .book-page {
      max-width: 1400px;
    }

    .layout-wide .book-columns {
      margin: 0 auto;
      max-width: 1600px;
    }

    .layout-wide pre {
      max-width: none;
    }

    /* Mobile - hide selector */
    @media (max-width: 768px) {
      .layout-selector {
        display: none;
      }
    }
  `;
  document.head.appendChild(style);

  // Initialize
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();