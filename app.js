// Hollow Hill: app state and input.
// One state object drives behavior: phase is 'start' -> 'running' <-> 'paused', and a story flag is set while a
// story plays. This file owns that state, Enter, Play/Pause, auto-pause, and which taps are accepted; other parts
// follow by listening to its events ('hollow:phase', 'hollow:story', 'hollow:tap'):
//   audio.js (ambient sound), cues.js (synthesized sounds), ambient.js (leaves), story.js (stories and triggers),
//   hints.js (idle hints).
(() => {
  'use strict';

  const root = document.documentElement;
  const el = {
    start: document.getElementById('start'),
    enter: document.getElementById('enter'),
    motionNote: document.getElementById('motion-note'),
    stage: document.getElementById('stage'),
    scene: document.getElementById('scene'),
    toggle: document.getElementById('toggle'),
    creditsOpen: document.getElementById('credits-open'),
    creditsClose: document.getElementById('credits-close'),
    storyNote: document.getElementById('story-note'),
    credits: document.getElementById('credits'),
  };

  // Reduced-motion preference is read before Enter and kept in state.
  const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  // phase: start | running | paused. story: null, or the name of the story now playing (it can be paused mid-way).
  const state = { phase: 'start', story: null, reducedMotion: motionQuery.matches };

  function render() {
    root.dataset.phase = state.phase;
    root.dataset.reducedMotion = String(state.reducedMotion);
    el.motionNote.hidden = !(state.reducedMotion && state.phase === 'start');
    const paused = state.phase === 'paused';
    el.toggle.setAttribute('aria-pressed', String(paused));
    el.toggle.textContent = paused ? 'Play' : 'Pause';
  }

  function setPhase(phase) {
    state.phase = phase;
    render();
    // Announce the change so other parts (audio.js) follow the same single state rule.
    document.dispatchEvent(new CustomEvent('hollow:phase', { detail: { phase } }));
    console.info('[hollow-hill] phase:', phase, '| reducedMotion:', state.reducedMotion);
  }

  motionQuery.addEventListener('change', (e) => {
    state.reducedMotion = e.matches;
    render();
    console.info('[hollow-hill] reducedMotion changed:', state.reducedMotion);
  });

  // ---- Start / Enter ----
  el.enter.addEventListener('click', () => {
    el.start.hidden = true;
    el.stage.hidden = false;
    setPhase('running');
    el.stage.focus({ preventScroll: true });
  });

  // ---- Play / Pause ----
  el.toggle.addEventListener('click', () => {
    if (state.phase === 'running') setPhase('paused');
    else if (state.phase === 'paused') setPhase('running');
  });

  // ---- Story flag ----
  // Stories (story.js) start and end through this one place: it sets the flag that locks scene taps and the
  // data-story attribute that CSS uses to run the story's animation timeline.
  function setStory(name) {
    state.story = name;
    if (name) root.dataset.story = name;
    else delete root.dataset.story;
    document.dispatchEvent(new CustomEvent('hollow:story', { detail: { story: name } }));
    console.info('[hollow-hill] story:', name || 'none');
  }
  window.hollowApp = {
    canStartStory: () => state.phase === 'running' && !state.story,
    setStory,
    state: () => ({ phase: state.phase, story: state.story, reducedMotion: state.reducedMotion }),
  };

  // ---- "Story playing" note (spec F5, S6) ----
  // While a story plays, say why taps do nothing; when it ends, say control is back, then let the note fade away.
  document.addEventListener('hollow:story', (event) => {
    const note = el.storyNote;
    note.hidden = false;
    if (event.detail.story) {
      note.textContent = 'A story is playing…';
      note.dataset.state = 'playing';
    } else {
      note.textContent = 'Your turn: keep exploring';
      note.dataset.state = 'done';
    }
  });
  // The "done" note removes itself when its fade finishes (an animation event, so Pause can freeze it).
  el.storyNote.addEventListener('animationend', () => {
    if (el.storyNote.dataset.state === 'done') el.storyNote.hidden = true;
  });

  // ---- Auto-pause when the page is hidden or the phone is locked (spec F6) ----
  // Same state as pressing Pause, and it stays paused until the User presses Play. That Play tap is also the
  // gesture iOS needs to restart web audio, which it interrupts whenever the page leaves the screen.
  function pauseIfHidden() {
    if (document.hidden && state.phase === 'running') setPhase('paused');
  }
  document.addEventListener('visibilitychange', pauseIfHidden);
  window.addEventListener('pagehide', pauseIfHidden);

  // ---- Hotspots: taps by mouse, touch or keyboard ----
  const LIT_MS = 450;
  const litTimers = new WeakMap();

  function activate(hotspot) {
    if (state.phase !== 'running' || state.story) return;       // ignored while paused or while a story plays
    console.info('[hollow-hill] tapped', hotspot.dataset.kind, hotspot.dataset.id);
    // Announce the tap. A story's trigger rules (story.js) set detail.handled and give their own feedback;
    // every other object gets a short flash and a soft tick so no tap is silent or invisible.
    const detail = { kind: hotspot.dataset.kind, id: Number(hotspot.dataset.id), element: hotspot, handled: false };
    document.dispatchEvent(new CustomEvent('hollow:tap', { detail }));
    if (detail.handled) return;
    hotspot.classList.add('lit');
    clearTimeout(litTimers.get(hotspot));
    litTimers.set(hotspot, setTimeout(() => hotspot.classList.remove('lit'), LIT_MS));
    if (window.hollowCues) window.hollowCues.tick();
  }

  el.scene.addEventListener('click', (e) => {
    const hotspot = e.target.closest('.hotspot');
    if (!hotspot) return;
    activate(hotspot);
    // A mouse or touch tap (detail > 0; a keyboard-made click has detail 0) should not leave the object holding
    // keyboard focus: otherwise a later Enter or Space would silently tap it again, and in a trigger sequence
    // that counts as a wrong tap.
    if (e.detail > 0) hotspot.blur();
  });

  el.scene.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const hotspot = e.target.closest('.hotspot');
    if (!hotspot) return;
    e.preventDefault();               // stop Space from scrolling
    if (e.repeat) return;             // holding the key down is one tap, not a stream of taps
    activate(hotspot);
  });

  // ---- Credits ----
  el.creditsOpen.addEventListener('click', () => el.credits.showModal());
  el.creditsClose.addEventListener('click', () => el.credits.close());

  render();
  console.info('[hollow-hill] ready | reducedMotion:', state.reducedMotion);
})();
