// Hollow Hill: story controller and trigger rules.
// A story runs as a CSS timeline: setting data-story on <html> (through app.js) starts every animation for
// it, and the 8 s .s-clock element's animationend tells us it is over. Because the timeline is pure CSS, the
// shared Pause rule freezes and resumes it mid-sequence with no extra code here.
// app.js decides whether a tap is allowed (running, no story playing) and announces it as 'hollow:tap';
// this file owns what the tap means.
(() => {
  'use strict';

  const app = window.hollowApp;
  const cues = () => window.hollowCues;
  const clock = document.querySelector('.s-clock');
  let current = null;

  // ---------- Playing a story ----------

  // Starts a story if the scene is running and nothing else is playing. Returns whether it started.
  function play(name) {
    if (!app.canStartStory()) return false;
    current = name;
    app.setStory(name);                    // locks scene taps and starts the CSS timeline
    if (cues()) cues().story(name);
    return true;
  }

  function finish() {
    if (!current) return;
    current = null;
    app.setStory(null);                    // removing data-story resets every story element to its hidden base look
  }

  clock.addEventListener('animationend', finish);

  // ---------- Story 1 trigger: tap the four pumpkins smallest to biggest ----------

  const PUMPKIN_ORDER = [1, 2, 3, 4];      // data-id of each pumpkin, smallest (left) to biggest (right)
  const SEQUENCE_TIMEOUT_S = 8;            // a half-finished sequence is forgotten after this long without taps
  const pumpkins = [...document.querySelectorAll('.hotspot[data-kind="pumpkin"]')];

  let progress = 0;                        // how many pumpkins in a row are right so far
  let idleSeconds = 0;                     // time since the last tap; counts only while running with no story

  function clearProgress() {
    progress = 0;
    pumpkins.forEach((p) => p.classList.remove('progress'));
  }

  // Wrong pumpkin: the lights reset, the tapped pumpkin wobbles (or fades under reduced motion), "nope" sounds.
  function nope(element) {
    clearProgress();
    element.classList.remove('nope');
    void element.getBoundingClientRect();  // lets the wobble restart if the same pumpkin is tapped twice quickly
    element.classList.add('nope');
    if (cues()) cues().nope();
  }
  // Removed when its animation ends (not on a timer) so Pause can freeze a wobble in progress.
  pumpkins.forEach((p) => p.addEventListener('animationend', () => p.classList.remove('nope')));

  function onPumpkinTap(detail) {
    detail.handled = true;
    if (detail.id !== PUMPKIN_ORDER[progress]) {
      nope(detail.element);
      return;
    }
    detail.element.classList.add('progress');          // stays lit until the sequence completes or resets
    if (cues()) cues().tap(progress);                  // a different, higher tone for each pumpkin
    progress += 1;
    if (progress === PUMPKIN_ORDER.length) {
      clearProgress();                                 // the story's own glow takes over from the tap lights
      play('pumpkins');
    }
  }

  document.addEventListener('hollow:tap', (event) => {
    idleSeconds = 0;                                   // any tap on the scene keeps a half-finished sequence alive
    if (event.detail.kind === 'pumpkin') onPumpkinTap(event.detail);
  });

  // Counts idle time with real elapsed time, but only while the scene is running: Pause and stories stop it.
  let lastTick = performance.now();
  setInterval(() => {
    const now = performance.now();
    const elapsed = Math.min((now - lastTick) / 1000, 0.5);
    lastTick = now;
    const s = app.state();
    if (s.phase !== 'running' || s.story || progress === 0) return;
    idleSeconds += elapsed;
    if (idleSeconds >= SEQUENCE_TIMEOUT_S) clearProgress();
  }, 200);

  window.hollowStory = { play, isPlaying: () => current !== null, progress: () => progress };
})();
