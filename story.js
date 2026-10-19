// Hollow Hill: story controller.
// A story runs as a CSS timeline: setting data-story on <html> (through app.js) starts every animation for
// it, and the 8 s .s-clock element's animationend tells us it is over. Because the timeline is pure CSS, the
// shared Pause rule freezes and resumes it mid-sequence with no extra code here.
(() => {
  'use strict';

  const app = window.hollowApp;
  const clock = document.querySelector('.s-clock');
  let current = null;

  // Starts a story if the scene is running and nothing else is playing. Returns whether it started.
  function play(name) {
    if (!app.canStartStory()) return false;
    current = name;
    app.setStory(name);                    // locks scene taps and starts the CSS timeline
    if (window.hollowCues) window.hollowCues.story(name);
    return true;
  }

  function finish() {
    if (!current) return;
    current = null;
    app.setStory(null);                    // removing data-story resets every story element to its hidden base look
  }

  clock.addEventListener('animationend', finish);

  window.hollowStory = { play, isPlaying: () => current !== null };

  // TEMPORARY preview for stage 1 (removed when the real triggers land): open the page with #play-pumpkins
  // and the story plays about a second after Enter.
  document.addEventListener('hollow:phase', (event) => {
    if (event.detail.phase === 'running' && location.hash === '#play-pumpkins') {
      setTimeout(() => play('pumpkins'), 1200);
    }
  }, { once: true });
})();
