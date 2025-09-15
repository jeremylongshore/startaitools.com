---
title: "Home"
---

# Welcome to Intent Solutions Inc

Deploy AI solutions in days, not months. We specialize in rapid AI implementation, automation workflows, and custom AI tools for businesses.

## Our Services

- **AI Implementation** - Quick deployment of AI solutions
- **Automation Workflows** - Streamline your business processes
- **Custom AI Tools** - Tailored solutions for your needs
- **Consulting** - Expert guidance on AI strategy

## Get Started

Contact us today to transform your business with AI.

---

<div id="arcade-glossary" style="position: fixed; bottom: 20px; left: 20px; background: #000000; border: 2px solid #2121FF; padding: 15px; max-width: 300px; font-family: 'Courier New', monospace; z-index: 999;">
  <div style="color: #FFCC00; font-weight: bold; text-transform: uppercase; margin-bottom: 10px; font-size: 14px;">
    👾 TECH GLOSSARY 👾
  </div>
  <div id="glossary-term" style="color: #00FFFF; margin-bottom: 5px; font-size: 12px;">
    <!-- Term appears here -->
  </div>
  <div id="glossary-definition" style="color: #FFFFFF; font-size: 11px; line-height: 1.4;">
    Hover over any yellow highlighted term to see its definition here!
  </div>
  <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #2121FF;">
    <span style="color: #FFB897; font-size: 10px;">SCORE: </span>
    <span id="terms-learned" style="color: #00FFFF; font-size: 10px;">0</span>
    <span style="color: #FFB897; font-size: 10px;"> TERMS</span>
  </div>
</div>

<script>
// Simple glossary display - no bubbles, just update the box
document.addEventListener('DOMContentLoaded', function() {
  const glossaryBox = document.getElementById('arcade-glossary');
  const termDisplay = document.getElementById('glossary-term');
  const definitionDisplay = document.getElementById('glossary-definition');
  const scoreDisplay = document.getElementById('terms-learned');

  let viewedTerms = JSON.parse(localStorage.getItem('viewed-terms') || '[]');
  scoreDisplay.textContent = viewedTerms.length;

  // Listen for glossary term hovers
  document.addEventListener('mouseenter', function(e) {
    if (e.target.classList.contains('glossary-term')) {
      const term = e.target.dataset.term;
      const definition = e.target.dataset.definition || window.techGlossary?.[term]?.definition;

      if (definition) {
        termDisplay.textContent = term.toUpperCase();
        definitionDisplay.textContent = definition;

        // Track viewed terms
        if (!viewedTerms.includes(term)) {
          viewedTerms.push(term);
          localStorage.setItem('viewed-terms', JSON.stringify(viewedTerms));
          scoreDisplay.textContent = viewedTerms.length;
        }
      }
    }
  }, true);

  // Reset display when not hovering
  document.addEventListener('mouseleave', function(e) {
    if (e.target.classList.contains('glossary-term')) {
      setTimeout(() => {
        termDisplay.textContent = '';
        definitionDisplay.textContent = 'Hover over any yellow highlighted term to see its definition here!';
      }, 100);
    }
  }, true);
});
</script>