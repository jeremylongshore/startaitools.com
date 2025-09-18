// Dark/Light Mode Toggle for StartAITools
(function() {
    'use strict';

    // Create the toggle button
    function createToggleButton() {
        const button = document.createElement('button');
        button.className = 'theme-toggle';
        button.setAttribute('aria-label', 'Toggle dark/light mode');
        button.innerHTML = '🌙';

        // Add click event
        button.addEventListener('click', toggleTheme);

        // Add to page
        document.body.appendChild(button);

        return button;
    }

    // Get current theme
    function getCurrentTheme() {
        return localStorage.getItem('theme') || 'auto';
    }

    // Set theme
    function setTheme(theme) {
        localStorage.setItem('theme', theme);
        document.documentElement.setAttribute('data-theme', theme);
        updateToggleButton(theme);
    }

    // Update toggle button appearance
    function updateToggleButton(theme) {
        const button = document.querySelector('.theme-toggle');
        if (!button) return;

        switch(theme) {
            case 'dark':
                button.innerHTML = '☀️';
                break;
            case 'light':
                button.innerHTML = '🌙';
                break;
            case 'auto':
                button.innerHTML = '🔄';
                break;
        }
    }

    // Toggle between themes
    function toggleTheme() {
        const current = getCurrentTheme();
        let next;

        switch(current) {
            case 'auto':
                next = 'light';
                break;
            case 'light':
                next = 'dark';
                break;
            case 'dark':
                next = 'auto';
                break;
            default:
                next = 'light';
        }

        setTheme(next);
    }

    // Initialize theme on page load
    function initTheme() {
        const savedTheme = getCurrentTheme();
        setTheme(savedTheme);

        // Also apply auto detection if needed
        if (savedTheme === 'auto') {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            document.documentElement.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
        }
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            createToggleButton();
            initTheme();
        });
    } else {
        createToggleButton();
        initTheme();
    }

    // Listen for system theme changes when in auto mode
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function(e) {
        if (getCurrentTheme() === 'auto') {
            document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
        }
    });
})();