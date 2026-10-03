/* Dispatch — measure.js
   Site action events for the self-hosted Umami tracker. No dependencies, no
   third-party script, no network call of its own: it only labels elements so
   Umami's own click handler records them, and calls window.umami.track() for
   the two server-acknowledged outcomes.

   WHAT THESE EVENTS MEAN (read before reporting on them):
   - *_click events are ATTEMPTS. A click on Subscribe is not a subscriber; a
     click on an outbound link is not a visit to the destination; a click on the
     support widget is not a payment.
   - *_accepted events mean the shared forms-api answered 2xx to the POST. That
     is the strongest outcome observable from the page. It is still NOT a
     confirmed subscriber (no double opt-in exists) and NOT a delivered lead.
   - /subscribe-success/ is not part of the current subscribe flow (the footer
     form posts with fetch and never navigates), so its pageviews are not a
     confirmation signal.

   Event catalogue (docs/analytics-events.md is the long form):
     outbound_click        any link to another host; data: dest, host
     email_click           any mailto: link
     subscribe_click       footer Subscribe button (static attribute)
     subscribe_accepted    forms-api 2xx for /api/forms/signup (main.js)
     contact_submit_click  end-of-post CTA or /contact/ submit (static attribute)
     contact_accepted      forms-api 2xx for /api/forms/contact (main.js)
     work_with_us_click    header "Work with us" (static attribute)
     support_widget_click  focus moved into the Ko-fi floating widget (heuristic)
*/
(function (root) {
  'use strict';

  var SITE_HOSTS = ['startaitools.com', 'www.startaitools.com'];

  /* Destination classes. Order matters: first match wins. Keep in sync with
     tests/test_site_events.py, which executes this function under node. */
  var CLASSES = [
    ['tonsofskills', /(^|\.)tonsofskills\.com$/],
    ['intentsolutions', /(^|\.)intentsolutions\.io$/],
    ['github', /(^|\.)(github\.com|github\.io|githubusercontent\.com)$/],
    ['support', /(^|\.)(ko-fi\.com|buymeacoffee\.com)$/]
  ];

  function classifyHost(host) {
    host = String(host || '').toLowerCase().replace(/\.$/, '');
    for (var i = 0; i < CLASSES.length; i++) {
      if (CLASSES[i][1].test(host)) return CLASSES[i][0];
    }
    return 'other';
  }

  /* Returns the Umami event for a link, or null when it should not be tracked.
     href must be absolute (anchor.href already is in the browser). */
  function eventForHref(href, pageHost) {
    var m = /^([a-z][a-z0-9+.-]*):/i.exec(String(href || ''));
    if (!m) return null;
    var scheme = m[1].toLowerCase();
    if (scheme === 'mailto') return { name: 'email_click', data: {} };
    if (scheme !== 'http' && scheme !== 'https') return null;
    var hm = /^https?:\/\/([^\/?#:]+)/i.exec(href);
    if (!hm) return null;
    var host = hm[1].toLowerCase();
    if (host === String(pageHost || '').toLowerCase() || SITE_HOSTS.indexOf(host) !== -1) return null;
    return { name: 'outbound_click', data: { dest: classifyHost(host), host: host } };
  }

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = { classifyHost: classifyHost, eventForHref: eventForHref, SITE_HOSTS: SITE_HOSTS };
    return;
  }

  var doc = root.document;

  /* Label every untagged link once. Elements a template already tagged keep
     their own event; Umami reads the attributes at click time. */
  function annotate() {
    var links = doc.querySelectorAll('a[href]:not([data-umami-event])');
    for (var i = 0; i < links.length; i++) {
      var ev = eventForHref(links[i].href, root.location.hostname);
      if (!ev) continue;
      links[i].setAttribute('data-umami-event', ev.name);
      for (var k in ev.data) links[i].setAttribute('data-umami-event-' + k, ev.data[k]);
    }
  }
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', annotate);
  else annotate();

  /* Ko-fi draws its button inside an iframe, so a click never reaches this
     document. The observable proxy is focus moving into that iframe, which
     blurs this window. Fires at most once per page view. */
  var supportSent = false;
  root.addEventListener('blur', function () {
    if (supportSent) return;
    var el = doc.activeElement;
    if (!el || el.tagName !== 'IFRAME') return;
    if (!el.closest('.floatingchat-container-wrap, .floatingchat-container-wrap-mobi')) return;
    supportSent = true;
    if (root.umami && typeof root.umami.track === 'function') {
      root.umami.track('support_widget_click', { provider: 'kofi' });
    }
  });
})(typeof window !== 'undefined' ? window : this);
