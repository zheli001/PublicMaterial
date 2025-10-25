// filepath: artifacts/shared/presenter_controls.js
// Shared presenter controls: injects presenter UI and wires keyboard shortcuts
// Usage: include <link rel="stylesheet" href="../../shared/presenter_controls.css"> in <head>
// and <script src="../../shared/presenter_controls.js"></script> before </body> in lesson_ppt.html

(function () {
  if (window.__PresenterControlsLoaded) return;
  window.__PresenterControlsLoaded = true;

  function qs(sel, ctx) { return (ctx || document).querySelector(sel); }
  function qsa(sel, ctx) { return Array.from((ctx || document).querySelectorAll(sel)); }

  // Build DOM for controls if not present
  function ensureDOM() {
    if (!qs('#presenter-controls')) {
      const pc = document.createElement('div');
      pc.id = 'presenter-controls';
      pc.setAttribute('aria-hidden','true');
      pc.style.position = 'fixed';
      pc.style.right = '12px';
      pc.style.bottom = '12px';
      pc.style.zIndex = 1200;
      pc.innerHTML = '\n        <button id="pc-toggle-notes" class="pc-btn" title="Toggle notes (N)" aria-pressed="false">📝 Notes (N)</button>\n        <button id="pc-prev" class="pc-btn" title="Previous slide">◀</button>\n        <button id="pc-next" class="pc-btn" title="Next slide">▶</button>\n        <button id="pc-toggle-presenter" class="pc-btn" title="Toggle presenter panel (Ctrl+Shift+N)">🎛 Presenter</button>\n      ';
      document.body.appendChild(pc);
    }

    if (!qs('#presenter-panel')) {
      const panel = document.createElement('div');
      panel.id = 'presenter-panel';
      panel.setAttribute('hidden','');
      panel.setAttribute('aria-hidden','true');
      panel.style.position = 'fixed';
      panel.style.left = '12px';
      panel.style.top = '12px';
      panel.style.zIndex = 1199;
      panel.style.background = 'rgba(255,255,255,0.98)';
      panel.style.border = '1px solid #ddd';
      panel.style.padding = '12px';
      panel.style.width = '360px';
      panel.style.maxHeight = '80vh';
      panel.style.overflow = 'auto';
      panel.style.boxShadow = '0 6px 18px rgba(0,0,0,0.12)';
      panel.innerHTML = '\n        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">\n          <strong>Presenter Notes</strong>\n          <span id="presenter-slide-index" style="font-size:0.9em;color:#666">1/1</span>\n        </div>\n        <div id="presenter-notes" style="white-space:pre-wrap;color:#222;line-height:1.4;font-size:14px">（无备注）</div>\n        <div style="margin-top:8px;text-align:right;"><button id="pc-close-panel">Close</button></div>\n      ';
      document.body.appendChild(panel);
    }
  }

  function init() {
    ensureDOM();

    const slides = qsa('.slide');
    if (!slides.length) return; // nothing to wire

    let current = slides.findIndex(s => s.classList.contains('active'));
    if (current < 0) current = 0;

    const notesPanel = qs('#presenter-panel');
    const notesContent = qs('#presenter-notes');
    const slideIndexEl = qs('#presenter-slide-index');
    const btnNotes = qs('#pc-toggle-notes');
    const btnPrev = qs('#pc-prev');
    const btnNext = qs('#pc-next');
    const btnPresenter = qs('#pc-toggle-presenter');
    const btnClose = qs('#pc-close-panel');

    function showSlide(idx) {
      if (idx < 0 || idx >= slides.length) return;
      slides.forEach((s, i) => s.classList.toggle('active', i === idx));
      current = idx;
      updateNotes();
    }

    function updateNotes() {
      const s = slides[current];
      const notes = (s && s.getAttribute('data-notes')) ? s.getAttribute('data-notes') : '';
      if (notesContent) notesContent.textContent = notes || '（无备注）';
      if (slideIndexEl) slideIndexEl.textContent = (current + 1) + '/' + slides.length;
    }

    function toggleNotes() {
      if (!notesPanel) return;
      const hidden = notesPanel.hasAttribute('hidden');
      if (hidden) {
        notesPanel.removeAttribute('hidden');
        notesPanel.setAttribute('aria-hidden','false');
        if (btnNotes) btnNotes.setAttribute('aria-pressed','true');
      } else {
        notesPanel.setAttribute('hidden','');
        notesPanel.setAttribute('aria-hidden','true');
        if (btnNotes) btnNotes.setAttribute('aria-pressed','false');
      }
    }

    function togglePresenterControlsVisibility() {
      const pc = qs('#presenter-controls');
      if (!pc) return;
      const isHidden = pc.getAttribute('data-visible') !== 'true';
      if (isHidden) {
        pc.setAttribute('data-visible','true');
        pc.setAttribute('aria-hidden','false');
        pc.style.opacity = 1;
      } else {
        pc.setAttribute('data-visible','false');
        pc.setAttribute('aria-hidden','true');
        pc.style.opacity = 0.9;
      }
    }

    // Wire buttons
    if (btnPrev) btnPrev.addEventListener('click', () => showSlide(current - 1));
    if (btnNext) btnNext.addEventListener('click', () => showSlide(current + 1));
    if (btnNotes) btnNotes.addEventListener('click', () => toggleNotes());
    if (btnPresenter) btnPresenter.addEventListener('click', () => togglePresenterControlsVisibility());
    if (btnClose) btnClose.addEventListener('click', () => { notesPanel.setAttribute('hidden',''); notesPanel.setAttribute('aria-hidden','true'); if (btnNotes) btnNotes.setAttribute('aria-pressed','false'); });

    // Keyboard: N toggles notes (when not focus in input), Ctrl+Shift+N toggles presenter panel
    document.addEventListener('keydown', function (ev) {
      const activeTag = document.activeElement && document.activeElement.tagName;
      if (activeTag === 'INPUT' || activeTag === 'TEXTAREA') return; // don't intercept typing

      // 'n' or 'N' without modifiers toggles notes
      if (!ev.ctrlKey && !ev.metaKey && !ev.altKey && ev.key.toLowerCase() === 'n') {
        ev.preventDefault();
        toggleNotes();
        return;
      }
      // Ctrl+Shift+N toggles presenter controls
      if ((ev.ctrlKey || ev.metaKey) && ev.shiftKey && ev.key.toLowerCase() === 'n') {
        ev.preventDefault();
        togglePresenterControlsVisibility();
        return;
      }
      // Arrow keys for navigation
      if (ev.key === 'ArrowRight') { ev.preventDefault(); showSlide(current + 1); }
      if (ev.key === 'ArrowLeft') { ev.preventDefault(); showSlide(current - 1); }
    }, { passive: false });

    // Click on slide to advance
    slides.forEach((s, i) => s.addEventListener('click', (e) => {
      if (e.target.closest('.slide')) {
        showSlide(i + 1);
      }
    }));

    // Initialize
    updateNotes();
  }

  // Initialize on DOMContentLoaded or immediately if ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    setTimeout(init, 0);
  }

})();

