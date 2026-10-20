// Hollow Hill: code-driven ambient effects (the rest are pure CSS in style.css).
// - Builds the falling leaves from a fixed table.
// - Sets the screen-edge ranges that bats and leaves travel between, because how much of the scene is visible
//   depends on the window shape.
// Pause and reduced motion are handled by the shared `fx` rules in style.css, not here.
(() => {
  'use strict';

  const root = document.documentElement;
  const stage = document.getElementById('stage');

  // ---- Leaves ----
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
  // The art is centered in the stage and scaled to fit. Bats start and end just past the visible left/right
  // edges (+40 units covers the wingspan); leaves start just above the visible top and end just below the bottom.
  function updateEffectRanges() {
    const w = stage.clientWidth;
    const h = stage.clientHeight;
    if (!w || !h) return;                           // the stage is hidden until Enter
    const scale = Math.min(w / 360, h / 640);
    const halfWidth = w / scale / 2;
    const halfHeight = h / scale / 2;
    root.style.setProperty('--bat-left', `${180 - halfWidth - 40}px`);
    root.style.setProperty('--bat-right', `${180 + halfWidth + 40}px`);
    root.style.setProperty('--fall-top', `${320 - halfHeight - 30}px`);
    root.style.setProperty('--fall-bottom', `${320 + halfHeight + 30}px`);
  }

  buildLeaves();
  window.addEventListener('resize', updateEffectRanges);
  // The stage becomes visible just before the 'running' announcement at Enter, so its size is known then.
  document.addEventListener('hollow:phase', (event) => {
    if (event.detail.phase === 'running') updateEffectRanges();
  });
})();
