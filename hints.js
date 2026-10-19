// Hollow Hill: idle hints (spec H1-H6).
// After a stretch of no taps the hint line shows a vague line, then a more specific one, then a pattern hint.
// Rules: any tap on the scene restarts the clock (H1) and hides the hint, so hints restart at level 1 (H2);
// levels appear at 15, 30 and 45 s of idle time and the last one stays (H3); the clock stops while paused;
// during a story the hint is hidden and the clock stops, and afterwards it restarts at 0 with no hint (H5).
(() => {
  'use strict';

  const app = window.hollowApp;
  const hint = document.getElementById('hint');
  const scene = document.getElementById('scene');

  // Seconds of idle time at which levels 1, 2 and 3 appear. The test suite shortens these.
  const HINT_TIMES = [15, 30, 45];

  // One line each, vague to specific, never stating the trigger. Hints are about the whole scene and do not
  // depend on which stories someone has seen (H4). Edit the wording here.
  const WORDING = {
    // Used while only the pumpkin story exists, so testers are not sent to things that do nothing yet.
    pumpkinsOnly: [
      'The hill is restless tonight…',
      'Look near the pumpkin patch…',
      'Size matters… patterns wake them.',
    ],
    // The Developer's picks for the finished game (2026-10-19); switch ACTIVE to 'allStories' once stories 2 and 3 exist.
    allStories: [
      'The hill is restless tonight…',
      'Look near the patch, the graves, the house.',
      'Size, rhythm, order… patterns wake them.',
    ],
  };
  const ACTIVE = 'pumpkinsOnly';

  let idleSeconds = 0;
  let level = 0;                           // 0 = no hint showing, 1 to 3 = which hint

  function hideHint() {
    level = 0;
    hint.hidden = true;
    hint.textContent = '';
  }

  function showHint(newLevel) {
    level = newLevel;
    hint.textContent = WORDING[ACTIVE][newLevel - 1];
    hint.hidden = false;
    hint.classList.remove('fade-in');      // restart the fade-in (a plain swap under reduced motion, see style.css)
    void hint.offsetWidth;
    hint.classList.add('fade-in');
  }

  // H1 and H2: a tap restarts the idle clock and hides the hint, so the next one is level 1 again.
  function restart() {
    idleSeconds = 0;
    if (level !== 0) hideHint();
  }

  // Taps on hotspots are announced by app.js. A tap on empty scene is not, so listen for it here. Only counts
  // while the scene accepts taps (running, no story).
  const acceptingTaps = () => {
    const s = app.state();
    return s.phase === 'running' && !s.story;
  };
  document.addEventListener('hollow:tap', restart);
  scene.addEventListener('pointerdown', () => { if (acceptingTaps()) restart(); });

  // H5: a story hides the hint and stops the clock; when it ends the clock starts again from 0 with no hint.
  document.addEventListener('hollow:story', () => restart());
  document.addEventListener('hollow:story', (event) => { if (event.detail.story) hideHint(); });

  // Counts idle time with real elapsed time, only while the scene is running and no story plays.
  let lastTick = performance.now();
  setInterval(() => {
    const now = performance.now();
    const elapsed = Math.min((now - lastTick) / 1000, 0.5);
    lastTick = now;
    if (!acceptingTaps()) return;
    idleSeconds += elapsed;
    const due = HINT_TIMES.filter((t) => idleSeconds >= t).length;   // 0 to 3
    if (due > level) showHint(due);        // H3: after level 3 it stays; there is no level 4 and no cycling
  }, 200);

  // For testing and troubleshooting: HINT_TIMES can be shortened here, e.g. hollowHints.times.splice(0, 3, 2, 4, 6).
  window.hollowHints = { times: HINT_TIMES, wording: WORDING, idle: () => idleSeconds, level: () => level };
})();
