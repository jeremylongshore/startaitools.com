/**
 * Simple Tech Glossary - No Bubbles, Just Highlights
 * Works with the glossary box on the index page
 */

(function() {
  'use strict';

  // Simple glossary terms - add more as needed
  const glossaryTerms = {
    'api': 'Application Programming Interface - a set of protocols for building software',
    'rest': 'Representational State Transfer - architectural style for web services',
    'javascript': 'Programming language for web development',
    'python': 'High-level programming language known for readability',
    'docker': 'Platform for developing and running applications in containers',
    'kubernetes': 'Container orchestration platform for automating deployment',
    'ai': 'Artificial Intelligence - machines simulating human intelligence',
    'machine learning': 'Method of data analysis that automates model building',
    'neural network': 'Computing model inspired by biological neural networks',
    'algorithm': 'Step-by-step procedure for solving a problem',
    'database': 'Organized collection of structured data',
    'sql': 'Structured Query Language for managing databases',
    'html': 'HyperText Markup Language - standard markup for web pages',
    'css': 'Cascading Style Sheets - styling language for web pages',
    'git': 'Version control system for tracking code changes',
    'github': 'Web-based platform for version control and collaboration',
    'json': 'JavaScript Object Notation - data interchange format',
    'xml': 'Extensible Markup Language - markup language for data',
    'http': 'HyperText Transfer Protocol - foundation of web communication',
    'https': 'HTTP Secure - encrypted version of HTTP',
    'framework': 'Pre-written code structure for building applications',
    'library': 'Collection of pre-written code for common tasks',
    'frontend': 'Client-side part of a web application',
    'backend': 'Server-side part of a web application',
    'fullstack': 'Development of both frontend and backend',
    'cloud': 'Internet-based computing services',
    'devops': 'Practices combining software development and IT operations',
    'agile': 'Iterative approach to software development',
    'scrum': 'Framework for managing product development',
    'ci/cd': 'Continuous Integration/Continuous Deployment',
    'testing': 'Process of evaluating software functionality',
    'debugging': 'Process of finding and fixing errors in code',
    'deployment': 'Process of making software available for use',
    'server': 'Computer that provides services to other computers',
    'client': 'Computer that requests services from a server',
    'encryption': 'Process of encoding data for security',
    'authentication': 'Process of verifying identity',
    'authorization': 'Process of granting access permissions',
    'webhook': 'Automated messages sent when events occur',
    'microservices': 'Architecture of small, independent services',
    'monolith': 'Single-tier software application',
    'scalability': 'Ability to handle increased workload',
    'latency': 'Time delay in data communication',
    'bandwidth': 'Maximum data transfer rate',
    'cache': 'Temporary storage for faster data access',
    'cookie': 'Small data stored on user\'s computer by websites',
    'session': 'Period of interaction between user and application',
    'token': 'Digital authentication credential',
    'oauth': 'Open standard for access delegation',
    'regex': 'Regular Expression - pattern matching in text',
    'dom': 'Document Object Model - programming interface for HTML',
    'ajax': 'Asynchronous JavaScript and XML - web development technique',
    'spa': 'Single Page Application - web app that loads once',
    'pwa': 'Progressive Web App - web app with native features',
    'responsive': 'Design that adapts to different screen sizes',
    'bootstrap': 'Popular CSS framework for responsive design',
    'react': 'JavaScript library for building user interfaces',
    'angular': 'TypeScript-based web application framework',
    'vue': 'Progressive JavaScript framework for UIs',
    'node': 'JavaScript runtime for server-side development',
    'npm': 'Node Package Manager - package manager for JavaScript',
    'yarn': 'Alternative package manager for JavaScript',
    'webpack': 'Module bundler for JavaScript applications',
    'babel': 'JavaScript compiler for using new features',
    'typescript': 'Typed superset of JavaScript',
    'sass': 'CSS preprocessor with additional features',
    'less': 'CSS preprocessor language',
    'graphql': 'Query language for APIs',
    'websocket': 'Protocol for real-time communication',
    'mqtt': 'Lightweight messaging protocol for IoT',
    'iot': 'Internet of Things - network of physical devices',
    'blockchain': 'Distributed ledger technology',
    'cryptocurrency': 'Digital currency using cryptography',
    'bitcoin': 'First and most known cryptocurrency',
    'ethereum': 'Blockchain platform with smart contracts',
    'nft': 'Non-Fungible Token - unique digital asset',
    'metaverse': 'Virtual shared space in digital world',
    'ar': 'Augmented Reality - digital overlay on real world',
    'vr': 'Virtual Reality - simulated experience',
    'ml': 'Machine Learning - subset of AI',
    'dl': 'Deep Learning - subset of machine learning',
    'nlp': 'Natural Language Processing - AI for language',
    'computer vision': 'AI for analyzing visual data',
    'chatbot': 'AI program simulating human conversation',
    'llm': 'Large Language Model - AI for text generation',
    'gpt': 'Generative Pre-trained Transformer - AI model type',
    'bert': 'Bidirectional Encoder Representations from Transformers',
    'tensorflow': 'Open-source machine learning framework',
    'pytorch': 'Open-source machine learning library',
    'jupyter': 'Interactive computing notebook environment',
    'pandas': 'Python library for data manipulation',
    'numpy': 'Python library for numerical computing',
    'scikit-learn': 'Python machine learning library',
    'flask': 'Lightweight Python web framework',
    'django': 'High-level Python web framework',
    'fastapi': 'Modern Python web API framework'
  };

  // Make glossary available globally
  window.techGlossary = glossaryTerms;

  /**
   * Process page content and add glossary term highlights
   */
  function processContent() {
    const contentAreas = document.querySelectorAll('.book-page, .markdown, article, .content, main');

    contentAreas.forEach(area => {
      if (area.dataset.glossaryProcessed) return;

      const walker = document.createTreeWalker(
        area,
        NodeFilter.SHOW_TEXT,
        {
          acceptNode: function(node) {
            // Skip if inside code, pre, script, or style
            const parent = node.parentElement;
            if (parent && parent.closest('code, pre, script, style, .glossary-term')) {
              return NodeFilter.FILTER_REJECT;
            }
            return NodeFilter.FILTER_ACCEPT;
          }
        }
      );

      const nodesToProcess = [];
      let node;
      while (node = walker.nextNode()) {
        nodesToProcess.push(node);
      }

      nodesToProcess.forEach(textNode => {
        let text = textNode.textContent;
        let hasMatch = false;

        // Check for glossary terms (case-insensitive)
        Object.keys(glossaryTerms).forEach(term => {
          const regex = new RegExp(`\\b(${escapeRegex(term)})\\b`, 'gi');
          if (regex.test(text)) {
            text = text.replace(regex, (match) => {
              return `<span class="glossary-term" data-term="${term}" data-definition="${glossaryTerms[term]}">${match}</span>`;
            });
            hasMatch = true;
          }
        });

        if (hasMatch) {
          const span = document.createElement('span');
          span.innerHTML = text;
          textNode.parentNode.replaceChild(span, textNode);
        }
      });

      area.dataset.glossaryProcessed = 'true';
    });
  }

  /**
   * Escape special regex characters
   */
  function escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  /**
   * Add simple styles for glossary terms
   */
  function addStyles() {
    const style = document.createElement('style');
    style.textContent = `
      .glossary-term {
        color: #FFCC00 !important;
        border-bottom: 1px dotted #FFCC00;
        cursor: help;
        transition: all 0.2s ease;
      }

      .glossary-term:hover {
        background: #2121FF;
        color: #FFCC00;
        border-bottom-color: #FF0000;
        padding: 0 2px;
      }
    `;
    document.head.appendChild(style);
  }

  /**
   * Initialize when DOM is ready
   */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      processContent();
      addStyles();
    });
  } else {
    processContent();
    addStyles();
  }

  // Watch for dynamic content
  const observer = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
      if (mutation.addedNodes.length) {
        processContent();
      }
    });
  });

  observer.observe(document.body, {
    childList: true,
    subtree: true
  });

})();