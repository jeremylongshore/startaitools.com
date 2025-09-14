/**
 * Tech Glossary Auto-Linking System
 * Automatically links technical terms to their definitions
 * Features: tooltips, progress tracking, and interactive learning
 */

(function() {
  'use strict';

  // Configuration
  const CONFIG = {
    glossaryPath: '/data/glossary.json',
    maxTermsPerPage: 100,  // Limit terms processed per page for performance
    minWordLength: 3,      // Minimum word length to consider
    tooltipDelay: 200,     // Delay before showing tooltip (ms)
    progressKey: 'glossary-progress',
    enabledKey: 'glossary-enabled',
    cacheKey: 'glossary-data',
    cacheExpiry: 24 * 60 * 60 * 1000  // 24 hours
  };

  // State
  let glossaryData = null;
  let termsMap = new Map();
  let processedNodes = new WeakSet();
  let tooltipTimeout = null;
  let currentTooltip = null;

  /**
   * Initialize the glossary system
   */
  async function init() {
    // Check if glossary is enabled
    if (localStorage.getItem(CONFIG.enabledKey) === 'false') {
      return;
    }

    // Load glossary data
    glossaryData = await loadGlossaryData();
    if (!glossaryData || !glossaryData.terms) {
      console.error('Failed to load glossary data');
      return;
    }

    // Build terms map for efficient lookup
    buildTermsMap();

    // Process initial content
    processContent();

    // Add simple glossary toggle
    addSimpleGlossaryToggle();

    // Watch for dynamic content
    observeContentChanges();

    // Add styles
    addStyles();
  }

  /**
   * Load glossary data from JSON
   */
  async function loadGlossaryData() {
    // Check cache first
    const cached = localStorage.getItem(CONFIG.cacheKey);
    if (cached) {
      try {
        const data = JSON.parse(cached);
        if (data.timestamp && Date.now() - data.timestamp < CONFIG.cacheExpiry) {
          return data.glossary;
        }
      } catch (e) {
        console.error('Failed to parse cached glossary:', e);
      }
    }

    // Fetch fresh data
    try {
      const response = await fetch(CONFIG.glossaryPath);
      if (!response.ok) throw new Error('Failed to fetch glossary');

      const glossary = await response.json();

      // Cache the data
      localStorage.setItem(CONFIG.cacheKey, JSON.stringify({
        glossary: glossary,
        timestamp: Date.now()
      }));

      return glossary;
    } catch (error) {
      console.error('Error loading glossary:', error);
      return null;
    }
  }

  /**
   * Build terms map for efficient lookup
   */
  function buildTermsMap() {
    glossaryData.terms.forEach(term => {
      // Store by lowercase for case-insensitive matching
      const key = term.term.toLowerCase();
      termsMap.set(key, term);

      // Also store common variations
      if (key.includes(' ')) {
        // Store hyphenated version
        termsMap.set(key.replace(/ /g, '-'), term);
        // Store underscore version
        termsMap.set(key.replace(/ /g, '_'), term);
      }

      // Store acronyms in uppercase
      if (key.length <= 5 && !key.includes(' ')) {
        termsMap.set(key.toUpperCase(), term);
      }
    });
  }

  /**
   * Process content and add glossary links
   */
  function processContent() {
    const content = document.querySelector('.book-page, .content, article, main') || document.body;
    processNode(content);
  }

  /**
   * Process a DOM node and its children
   */
  function processNode(node) {
    if (processedNodes.has(node)) return;
    processedNodes.add(node);

    // Skip certain elements
    const skipTags = ['SCRIPT', 'STYLE', 'CODE', 'PRE', 'A', 'BUTTON', 'INPUT', 'TEXTAREA'];
    if (skipTags.includes(node.tagName)) return;

    // Process text nodes
    if (node.nodeType === Node.TEXT_NODE) {
      processTextNode(node);
    } else {
      // Process children
      const children = Array.from(node.childNodes);
      children.forEach(child => processNode(child));
    }
  }

  /**
   * Process a text node and add glossary links
   */
  function processTextNode(textNode) {
    const text = textNode.textContent;
    if (!text || text.trim().length < CONFIG.minWordLength) return;

    // Find terms in the text
    const matches = findTermsInText(text);
    if (matches.length === 0) return;

    // Create document fragment with linked terms
    const fragment = document.createDocumentFragment();
    let lastIndex = 0;

    matches.forEach(match => {
      // Add text before the match
      if (match.index > lastIndex) {
        fragment.appendChild(
          document.createTextNode(text.substring(lastIndex, match.index))
        );
      }

      // Add the linked term
      const link = createGlossaryLink(match.term, match.text);
      fragment.appendChild(link);

      lastIndex = match.index + match.text.length;
    });

    // Add remaining text
    if (lastIndex < text.length) {
      fragment.appendChild(
        document.createTextNode(text.substring(lastIndex))
      );
    }

    // Replace the text node
    textNode.parentNode.replaceChild(fragment, textNode);
  }

  /**
   * Find glossary terms in text
   */
  function findTermsInText(text) {
    const matches = [];
    const words = text.split(/\\b/);
    let currentIndex = 0;

    for (let i = 0; i < words.length; i++) {
      const word = words[i];
      const lowerWord = word.toLowerCase();

      // Check single word
      if (termsMap.has(lowerWord)) {
        matches.push({
          index: currentIndex,
          text: word,
          term: termsMap.get(lowerWord)
        });
      }
      // Check multi-word terms (up to 3 words)
      else if (i < words.length - 2) {
        const twoWords = words.slice(i, i + 3).join('').toLowerCase();
        const threeWords = words.slice(i, i + 5).join('').toLowerCase();

        if (termsMap.has(threeWords)) {
          const matchText = words.slice(i, i + 5).join('');
          matches.push({
            index: currentIndex,
            text: matchText,
            term: termsMap.get(threeWords)
          });
          i += 4;  // Skip processed words
          currentIndex += matchText.length - word.length;
        } else if (termsMap.has(twoWords)) {
          const matchText = words.slice(i, i + 3).join('');
          matches.push({
            index: currentIndex,
            text: matchText,
            term: termsMap.get(twoWords)
          });
          i += 2;  // Skip processed words
          currentIndex += matchText.length - word.length;
        }
      }

      currentIndex += word.length;
    }

    // Limit number of matches per page
    return matches.slice(0, CONFIG.maxTermsPerPage);
  }

  /**
   * Create a glossary link element
   */
  function createGlossaryLink(term, text) {
    const link = document.createElement('span');
    link.className = 'glossary-term';
    link.textContent = text;
    link.dataset.term = term.term;
    link.dataset.category = term.category;
    link.tabIndex = 0;
    link.setAttribute('role', 'button');
    link.setAttribute('aria-label', `Definition of ${term.term}`);

    // Add event listeners
    link.addEventListener('mouseenter', (e) => showTooltip(e, term));
    link.addEventListener('mouseleave', hideTooltip);
    link.addEventListener('focus', (e) => showTooltip(e, term));
    link.addEventListener('blur', hideTooltip);
    link.addEventListener('click', (e) => {
      e.preventDefault();
      showFullDefinition(term);
    });

    return link;
  }

  /**
   * Show tooltip with term definition
   */
  function showTooltip(event, term) {
    clearTimeout(tooltipTimeout);
    tooltipTimeout = setTimeout(() => {
      // Remove existing tooltip
      hideTooltip();

      // Create tooltip
      const tooltip = document.createElement('div');
      tooltip.className = 'glossary-tooltip';
      tooltip.innerHTML = `
        <div class="glossary-tooltip-header">
          <strong>${term.term}</strong>
          <span class="glossary-category">${term.category}</span>
        </div>
        <div class="glossary-tooltip-definition">
          ${term.definition.substring(0, 200)}${term.definition.length > 200 ? '...' : ''}
        </div>
        <div class="glossary-tooltip-footer">
          Click for full definition
        </div>
      `;

      // Position tooltip
      const rect = event.target.getBoundingClientRect();
      tooltip.style.position = 'fixed';
      tooltip.style.left = `${rect.left}px`;
      tooltip.style.top = `${rect.bottom + 5}px`;
      tooltip.style.zIndex = '10000';

      // Add to page
      document.body.appendChild(tooltip);
      currentTooltip = tooltip;

      // No tracking needed

      // Adjust position if tooltip goes off screen
      const tooltipRect = tooltip.getBoundingClientRect();
      if (tooltipRect.right > window.innerWidth) {
        tooltip.style.left = `${window.innerWidth - tooltipRect.width - 10}px`;
      }
      if (tooltipRect.bottom > window.innerHeight) {
        tooltip.style.top = `${rect.top - tooltipRect.height - 5}px`;
      }
    }, CONFIG.tooltipDelay);
  }

  /**
   * Hide tooltip
   */
  function hideTooltip() {
    clearTimeout(tooltipTimeout);
    if (currentTooltip) {
      currentTooltip.remove();
      currentTooltip = null;
    }
  }

  /**
   * Show full definition in modal
   */
  function showFullDefinition(term) {
    // Create modal
    const modal = document.createElement('div');
    modal.className = 'glossary-modal';
    modal.innerHTML = `
      <div class="glossary-modal-content">
        <button class="glossary-modal-close" aria-label="Close">&times;</button>
        <h2>${term.term}</h2>
        <div class="glossary-modal-meta">
          <span class="glossary-category">${term.category}</span>
          <span class="glossary-source">Source: ${term.source}</span>
        </div>
        <div class="glossary-modal-definition">
          ${term.definition}
        </div>
        <div class="glossary-modal-actions">
          <button class="glossary-btn glossary-btn-related">Find Related Terms</button>
        </div>
      </div>
    `;

    // Add event listeners
    modal.querySelector('.glossary-modal-close').addEventListener('click', () => {
      modal.remove();
    });

    // Removed learn button handler

    modal.querySelector('.glossary-btn-related').addEventListener('click', () => {
      showRelatedTerms(term);
      modal.remove();
    });

    // Close on background click
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        modal.remove();
      }
    });

    // Add to page
    document.body.appendChild(modal);

    // No tracking needed
  }

  /**
   * Show related terms
   */
  function showRelatedTerms(term) {
    const related = glossaryData.terms.filter(t =>
      t.category === term.category && t.term !== term.term
    ).slice(0, 10);

    const modal = document.createElement('div');
    modal.className = 'glossary-modal';
    modal.innerHTML = `
      <div class="glossary-modal-content">
        <button class="glossary-modal-close" aria-label="Close">&times;</button>
        <h2>Related to "${term.term}"</h2>
        <div class="glossary-related-list">
          ${related.map(t => `
            <div class="glossary-related-item" data-term="${t.term}">
              <strong>${t.term}</strong>
              <p>${t.definition.substring(0, 100)}...</p>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    // Add event listeners
    modal.querySelector('.glossary-modal-close').addEventListener('click', () => {
      modal.remove();
    });

    modal.querySelectorAll('.glossary-related-item').forEach(item => {
      item.addEventListener('click', () => {
        const termName = item.dataset.term;
        const relatedTerm = termsMap.get(termName.toLowerCase());
        if (relatedTerm) {
          modal.remove();
          showFullDefinition(relatedTerm);
        }
      });
    });

    document.body.appendChild(modal);
  }

  /**
   * Add simple glossary toggle to page
   */
  function addSimpleGlossaryToggle() {
    const controls = document.createElement('div');
    controls.className = 'glossary-controls';
    controls.innerHTML = `
      <button class="glossary-toggle" aria-label="Toggle Glossary">
        <span class="glossary-icon">📚</span>
        <span class="glossary-label">Glossary</span>
      </button>
      <div class="glossary-panel" hidden>
        <h3>Tech Glossary</h3>
        <div class="glossary-info">
          <p><strong>${glossaryData.terms.length}</strong> technical terms available</p>
          <p>Hover over highlighted terms for definitions</p>
        </div>
        <div class="glossary-actions">
          <button class="glossary-btn" id="glossary-toggle-enable">
            ${localStorage.getItem(CONFIG.enabledKey) !== 'false' ? 'Disable' : 'Enable'} Auto-Linking
          </button>
          <button class="glossary-btn" id="glossary-browse">Browse All Terms</button>
        </div>
      </div>
    `;

    // Add event listeners
    const toggle = controls.querySelector('.glossary-toggle');
    const panel = controls.querySelector('.glossary-panel');

    toggle.addEventListener('click', () => {
      panel.hidden = !panel.hidden;
    });

    controls.querySelector('#glossary-toggle-enable').addEventListener('click', (e) => {
      const enabled = localStorage.getItem(CONFIG.enabledKey) !== 'false';
      localStorage.setItem(CONFIG.enabledKey, !enabled);
      e.target.textContent = enabled ? 'Enable Glossary' : 'Disable Glossary';
      if (!enabled) {
        location.reload();
      }
    });

    // Removed reset button since we're not tracking

    controls.querySelector('#glossary-browse').addEventListener('click', () => {
      showGlossaryBrowser();
    });

    document.body.appendChild(controls);
  }

  /**
   * Show glossary browser
   */
  function showGlossaryBrowser() {
    const categories = [...new Set(glossaryData.terms.map(t => t.category))].sort();

    const modal = document.createElement('div');
    modal.className = 'glossary-modal glossary-browser';
    modal.innerHTML = `
      <div class="glossary-modal-content glossary-browser-content">
        <button class="glossary-modal-close" aria-label="Close">&times;</button>
        <h2>Browse Glossary</h2>
        <div class="glossary-browser-filters">
          <select id="glossary-category-filter">
            <option value="">All Categories</option>
            ${categories.map(cat => `<option value="${cat}">${cat}</option>`).join('')}
          </select>
          <input type="search" id="glossary-search" placeholder="Search terms...">
        </div>
        <div class="glossary-browser-list" id="glossary-browser-list">
          ${renderTermsList(glossaryData.terms.slice(0, 100))}
        </div>
      </div>
    `;

    // Add event listeners
    modal.querySelector('.glossary-modal-close').addEventListener('click', () => {
      modal.remove();
    });

    const categoryFilter = modal.querySelector('#glossary-category-filter');
    const searchInput = modal.querySelector('#glossary-search');
    const list = modal.querySelector('#glossary-browser-list');

    const filterTerms = () => {
      const category = categoryFilter.value;
      const search = searchInput.value.toLowerCase();

      const filtered = glossaryData.terms.filter(term => {
        const matchesCategory = !category || term.category === category;
        const matchesSearch = !search ||
          term.term.toLowerCase().includes(search) ||
          term.definition.toLowerCase().includes(search);
        return matchesCategory && matchesSearch;
      });

      list.innerHTML = renderTermsList(filtered);
      attachTermClickHandlers(list);
    };

    categoryFilter.addEventListener('change', filterTerms);
    searchInput.addEventListener('input', filterTerms);

    attachTermClickHandlers(list);
    document.body.appendChild(modal);
  }

  /**
   * Render terms list HTML
   */
  function renderTermsList(terms) {
    return terms.map(term => `
      <div class="glossary-browser-item" data-term="${term.term}">
        <div class="glossary-browser-item-header">
          <strong>${term.term}</strong>
          <span class="glossary-category">${term.category}</span>
        </div>
        <p>${term.definition.substring(0, 150)}...</p>
      </div>
    `).join('');
  }

  /**
   * Attach click handlers to term items
   */
  function attachTermClickHandlers(container) {
    container.querySelectorAll('.glossary-browser-item').forEach(item => {
      item.addEventListener('click', () => {
        const termName = item.dataset.term;
        const term = glossaryData.terms.find(t => t.term === termName);
        if (term) {
          showFullDefinition(term);
        }
      });
    });
  }

  // Removed all progress tracking functions

  /**
   * Show notification
   */
  function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'glossary-notification';
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.classList.add('fade-out');
      setTimeout(() => notification.remove(), 300);
    }, 2000);
  }

  /**
   * Observe content changes for dynamic content
   */
  function observeContentChanges() {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach(mutation => {
        mutation.addedNodes.forEach(node => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            processNode(node);
          }
        });
      });
    });

    const content = document.querySelector('.book-page, .content, article, main') || document.body;
    observer.observe(content, {
      childList: true,
      subtree: true
    });
  }

  /**
   * Add glossary styles
   */
  function addStyles() {
    const style = document.createElement('style');
    style.textContent = `
      /* Glossary term highlights */
      .glossary-term {
        border-bottom: 2px dotted var(--pac-yellow, #FFFF00);
        cursor: help;
        transition: all 0.3s ease;
        position: relative;
      }

      .glossary-term:hover {
        background: rgba(255, 255, 0, 0.1);
        border-bottom-color: var(--pac-orange, #FFB847);
      }

      .glossary-term:focus {
        outline: 2px solid var(--pac-yellow, #FFFF00);
        outline-offset: 2px;
      }

      /* Tooltips */
      .glossary-tooltip {
        background: var(--maze-blue-dark, #000080);
        color: var(--power-pellet, #FFFFFF);
        border: 2px solid var(--pac-yellow, #FFFF00);
        border-radius: 8px;
        padding: 12px;
        max-width: 400px;
        box-shadow: 0 4px 20px rgba(0, 255, 255, 0.3);
        font-size: 14px;
        animation: ghost-float 2s ease-in-out infinite;
      }

      .glossary-tooltip-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--pac-yellow, #FFFF00);
      }

      .glossary-tooltip-header strong {
        color: var(--pac-yellow, #FFFF00);
        font-size: 16px;
      }

      .glossary-category {
        background: var(--ghost-cyan, #00FFFF);
        color: var(--screen-black, #000000);
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: bold;
        text-transform: uppercase;
      }

      .glossary-tooltip-definition {
        line-height: 1.5;
        margin-bottom: 8px;
      }

      .glossary-tooltip-footer {
        font-size: 12px;
        color: var(--ghost-cyan, #00FFFF);
        font-style: italic;
      }

      /* Modal */
      .glossary-modal {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 100000;
        animation: fadeIn 0.3s ease;
      }

      .glossary-modal-content {
        background: var(--maze-blue-dark, #000080);
        color: var(--power-pellet, #FFFFFF);
        border: 3px solid var(--pac-yellow, #FFFF00);
        border-radius: 12px;
        padding: 24px;
        max-width: 600px;
        max-height: 80vh;
        overflow-y: auto;
        position: relative;
        box-shadow: 0 0 30px var(--ghost-cyan, #00FFFF);
      }

      .glossary-browser-content {
        max-width: 800px;
      }

      .glossary-modal-close {
        position: absolute;
        top: 12px;
        right: 12px;
        background: var(--ghost-red, #FF0000);
        color: white;
        border: none;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
      }

      .glossary-modal-close:hover {
        transform: rotate(90deg);
        background: var(--pac-orange, #FFB847);
      }

      .glossary-modal h2 {
        color: var(--pac-yellow, #FFFF00);
        margin-top: 0;
        margin-bottom: 16px;
        text-shadow: 0 0 10px var(--pac-orange, #FFB847);
      }

      .glossary-modal-meta {
        display: flex;
        gap: 12px;
        margin-bottom: 16px;
      }

      .glossary-source {
        color: var(--ghost-pink, #FFB8FF);
        font-size: 12px;
      }

      .glossary-modal-definition {
        line-height: 1.6;
        margin-bottom: 20px;
      }

      .glossary-modal-actions {
        display: flex;
        gap: 12px;
      }

      /* Buttons */
      .glossary-btn {
        background: linear-gradient(45deg, var(--pac-yellow, #FFFF00), var(--pac-orange, #FFB847));
        color: var(--screen-black, #000000);
        border: 2px solid var(--ghost-cyan, #00FFFF);
        padding: 8px 16px;
        font-weight: bold;
        text-transform: uppercase;
        cursor: pointer;
        border-radius: 20px;
        transition: all 0.3s ease;
      }

      .glossary-btn:hover {
        background: linear-gradient(45deg, var(--ghost-cyan, #00FFFF), var(--ghost-pink, #FFB8FF));
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 255, 0, 0.4);
      }

      /* Controls */
      .glossary-controls {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 10000;
      }

      .glossary-toggle {
        background: var(--maze-blue-dark, #000080);
        color: var(--pac-yellow, #FFFF00);
        border: 2px solid var(--pac-yellow, #FFFF00);
        border-radius: 50px;
        padding: 12px 20px;
        font-size: 16px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 255, 255, 0.3);
      }

      .glossary-toggle:hover {
        background: var(--pac-yellow, #FFFF00);
        color: var(--screen-black, #000000);
        transform: scale(1.05);
      }

      .glossary-icon {
        font-size: 20px;
      }

      .glossary-panel {
        position: absolute;
        bottom: 60px;
        right: 0;
        background: var(--maze-blue-dark, #000080);
        color: var(--power-pellet, #FFFFFF);
        border: 2px solid var(--pac-yellow, #FFFF00);
        border-radius: 12px;
        padding: 20px;
        min-width: 300px;
        box-shadow: 0 4px 20px rgba(0, 255, 255, 0.3);
      }

      .glossary-panel h3 {
        color: var(--pac-yellow, #FFFF00);
        margin-top: 0;
        margin-bottom: 16px;
      }

      .glossary-stats {
        margin-bottom: 16px;
        font-size: 14px;
      }

      .glossary-stats div {
        margin-bottom: 8px;
      }

      .glossary-stats strong {
        color: var(--ghost-cyan, #00FFFF);
      }

      .glossary-progress-bar {
        background: var(--screen-black, #000000);
        border: 1px solid var(--pac-yellow, #FFFF00);
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
        margin-bottom: 16px;
      }

      .glossary-progress-fill {
        background: linear-gradient(90deg, var(--pac-yellow, #FFFF00), var(--pac-orange, #FFB847));
        height: 100%;
        transition: width 0.5s ease;
        box-shadow: 0 0 10px var(--pac-yellow, #FFFF00);
      }

      .glossary-actions {
        display: flex;
        flex-direction: column;
        gap: 8px;
      }

      /* Browser */
      .glossary-browser-filters {
        display: flex;
        gap: 12px;
        margin-bottom: 20px;
      }

      .glossary-browser-filters select,
      .glossary-browser-filters input {
        flex: 1;
        background: var(--screen-black, #000000);
        color: var(--screen-glow, #00FF41);
        border: 1px solid var(--pac-yellow, #FFFF00);
        padding: 8px;
        border-radius: 4px;
      }

      .glossary-browser-list {
        max-height: 400px;
        overflow-y: auto;
      }

      .glossary-browser-item {
        background: rgba(0, 0, 128, 0.3);
        border: 1px solid var(--maze-blue, #0000FF);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
      }

      .glossary-browser-item:hover {
        background: rgba(255, 255, 0, 0.1);
        border-color: var(--pac-yellow, #FFFF00);
        transform: translateX(4px);
      }

      .glossary-browser-item.viewed {
        opacity: 0.7;
        border-left: 4px solid var(--screen-glow, #00FF41);
      }

      .glossary-browser-item-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
      }

      .glossary-browser-item p {
        margin: 0;
        font-size: 14px;
        color: var(--ghost-cyan, #00FFFF);
      }

      /* Related terms */
      .glossary-related-list {
        max-height: 400px;
        overflow-y: auto;
      }

      .glossary-related-item {
        background: rgba(0, 0, 128, 0.3);
        border: 1px solid var(--maze-blue, #0000FF);
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
      }

      .glossary-related-item:hover {
        background: rgba(255, 255, 0, 0.1);
        border-color: var(--pac-yellow, #FFFF00);
      }

      /* Notification */
      .glossary-notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--screen-glow, #00FF41);
        color: var(--screen-black, #000000);
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: bold;
        z-index: 100001;
        animation: slideIn 0.3s ease;
      }

      .glossary-notification.fade-out {
        animation: fadeOut 0.3s ease;
      }

      /* Animations */
      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }

      @keyframes fadeOut {
        from { opacity: 1; }
        to { opacity: 0; }
      }

      @keyframes slideIn {
        from {
          transform: translateX(100%);
          opacity: 0;
        }
        to {
          transform: translateX(0);
          opacity: 1;
        }
      }

      @keyframes ghost-float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
      }

      /* Mobile responsiveness */
      @media (max-width: 768px) {
        .glossary-tooltip {
          max-width: 90vw;
        }

        .glossary-modal-content {
          max-width: 90vw;
          margin: 20px;
        }

        .glossary-controls {
          bottom: 10px;
          right: 10px;
        }

        .glossary-panel {
          width: 90vw;
          right: -10px;
        }
      }
    `;
    document.head.appendChild(style);
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();