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
    updateEffectRanges();
    setPhase('running');
    el.stage.focus({ preventScroll: true });
  });

  // ---- Leaves (ambient particles) ----
  // Fixed table, not random, so every load behaves the same. Each row:
  // [x in scene units, size, seconds to fall, sway distance, sway seconds, tumble seconds]
  const LEAVES = [
    [22, 1.2, 24, 14, 3.2, 2.4], [58, 0.9, 20, 18, 2.8, 2.0], [96, 1.4, 27, 12, 3.8, 2.9],
    [132, 1.0, 22, 20, 3.0, 2.2], [168, 1.3, 26, 16, 4.0, 3.0], [204, 0.9, 19, 22, 2.6, 1.9],
    [238, 1.5, 29, 12, 3.6, 2.7], [270, 1.1, 23, 18, 3.4, 2.5], [302, 1.3, 25, 14, 2.9, 2.3],
    [336, 1.0, 21, 20, 3.1, 2.1], [78, 1.2, 28, 16, 3.9, 2.8], [218, 1.1, 18, 18, 2.7, 2.0],
  ];
  const LEAF_COLORS = ['#ff7a1a', '#ffc247'];       // pumpkin orange and glow yellow from the palette
  const LEAF_PATH = 'M0 -7 C6 -5 7 3 0 8 C-7 3 -6 -5 0 -7 Z';
  const SVG_NS = 'http://www.w3.org/2000/svg';

  function svgEl(name, attrs) {
    const node = document.createElementNS(SVG_NS, name);
    Object.entries(attrs).forEach(([key, value]) => node.setAttribute(key, value));
    return node;
  }

  // Nested groups so the three motions never fight: translate (x) > fall > sway > tumble > shape.
  function buildLeaves() {
    const group = svgEl('g', { id: 'leaves', class: 'fx' });
    LEAVES.forEach(([x, size, fall, sway, swayDur, spinDur], i) => {
      // Spread the leaves down the screen at the start (negative delay = already mid-fall).
      const phase = ((i * 5) % LEAVES.length) / LEAVES.length;
      const outer = svgEl('g', { transform: `translate(${x} 0)` });
      const fallG = svgEl('g', { class: 'leaf-fall', style: `--fall:${fall}s;--delay:${(-fall * phase).toFixed(1)}s` });
      const swayG = svgEl('g', { class: 'leaf-sway', style: `--sway:${sway}px;--sway-dur:${swayDur}s;--sway-delay:${(-swayDur * phase).toFixed(1)}s` });
      const spinG = svgEl('g', { class: 'leaf-spin', style: `--spin-dur:${spinDur}s` });
      const shape = svgEl('g', { transform: `scale(${size})` });
      shape.appendChild(svgEl('path', { d: LEAF_PATH, fill: LEAF_COLORS[i % LEAF_COLORS.length] }));
      shape.appendChild(svgEl('path', { d: 'M0 -5 L0 6', stroke: '#0e0720', 'stroke-opacity': '0.35', 'stroke-width': '0.8', fill: 'none' }));
      spinG.appendChild(shape); swayG.appendChild(spinG); fallG.appendChild(swayG); outer.appendChild(fallG);
      group.appendChild(outer);
    });
    document.getElementById('layer-particles').appendChild(group);
  }

  // ---- Effect ranges (bats and leaves) ----
  // The art is centered in the stage and scaled to fit, so how much of the scene is visible depends on the
  // window shape. Bats start and end just past the visible left/right edges (+40 units covers the wingspan);
  // leaves start just above the visible top and end just below the visible bottom.
  function updateEffectRanges() {
    const w = el.stage.clientWidth;
    const h = el.stage.clientHeight;
    if (!w || !h) return;
    const scale = Math.min(w / 360, h / 640);
    const halfWidth = w / scale / 2;
    const halfHeight = h / scale / 2;
    root.style.setProperty('--bat-left', `${180 - halfWidth - 40}px`);
    root.style.setProperty('--bat-right', `${180 + halfWidth + 40}px`);
    root.style.setProperty('--fall-top', `${320 - halfHeight - 30}px`);
    root.style.setProperty('--fall-bottom', `${320 + halfHeight + 30}px`);
  }
  window.addEventListener('resize', updateEffectRanges);

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

  // ---- Auto-pause when the page is hidden or the phone is locked (spec F6) ----
  // Same state as pressing Pause, and it stays paused until the User presses Play. That Play tap is also the
  // gesture iOS needs to restart web audio, which it interrupts whenever the page leaves the screen.
  function pauseIfHidden() {
    if (document.hidden && state.phase === 'running') setPhase('paused');
  }
  document.addEventListener('visibilitychange', pauseIfHidden);
  window.addEventListener('pagehide', pauseIfHidden);

  // ---- Hotspots: placeholder feedback only (light-up) ----
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

  buildLeaves();
  render();
  console.info('[hollow-hill] ready | reducedMotion:', state.reducedMotion);
})();
