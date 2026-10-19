// Hollow Hill: checkpoint 1 (static shell).
// One state object drives behavior: phase is 'start' -> 'running' <-> 'paused'.
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
    credits: document.getElementById('credits'),
  };

  // Reduced-motion preference is read before Enter and kept in state.
  const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
  const state = { phase: 'start', reducedMotion: motionQuery.matches };

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

  // ---- Hotspots: placeholder feedback only (light-up) ----
  const LIT_MS = 450;
  const litTimers = new WeakMap();

  function activate(hotspot) {
    if (state.phase !== 'running') return;
    hotspot.classList.add('lit');
    clearTimeout(litTimers.get(hotspot));
    litTimers.set(hotspot, setTimeout(() => hotspot.classList.remove('lit'), LIT_MS));
    console.info('[hollow-hill] tapped', hotspot.dataset.kind, hotspot.dataset.id);
  }

  el.scene.addEventListener('click', (e) => {
    const hotspot = e.target.closest('.hotspot');
    if (hotspot) activate(hotspot);
  });

  el.scene.addEventListener('keydown', (e) => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const hotspot = e.target.closest('.hotspot');
    if (!hotspot) return;
    e.preventDefault();               // stop Space from scrolling
    activate(hotspot);
  });

  // ---- Credits ----
  el.creditsOpen.addEventListener('click', () => el.credits.showModal());
  el.creditsClose.addEventListener('click', () => el.credits.close());

  render();
  console.info('[hollow-hill] ready | reducedMotion:', state.reducedMotion);
})();
