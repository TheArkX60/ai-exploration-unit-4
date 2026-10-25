// Hollow Hill: synthesized sound cues for stories and taps (no audio files, so nothing to credit or license).
// Everything is built with Web Audio on the shared context from audio.js and mixed into its output, so
// Pause (which suspends that context) freezes these sounds along with the ambience. If audio is unavailable
// (blocked, failed, or not started yet) every cue quietly does nothing and the visuals carry on.
(() => {
  'use strict';

  const LEVEL = 1;                      // overall cue loudness; tune by ear

  const audio = () => {
    const ctx = window.hollowAudio && window.hollowAudio.context();
    const out = window.hollowAudio && window.hollowAudio.output();
    return ctx && out && ctx.state === 'running' ? { ctx, out } : null;
  };

  let noise = null;                     // one second of white noise, made once and reused
  function noiseBuffer(ctx) {
    if (noise && noise.sampleRate === ctx.sampleRate) return noise;
    noise = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
    const data = noise.getChannelData(0);
    for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
    return noise;
  }

  // A soft bell-like note: a sine plus a quieter overtone, fast attack, smooth decay.
  function bell({ ctx, out }, when, freq, gain, seconds) {
    [[1, 1], [2.01, 0.3]].forEach(([ratio, part]) => {
      const osc = ctx.createOscillator();
      const env = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.value = freq * ratio;
      env.gain.setValueAtTime(0.0001, when);
      env.gain.linearRampToValueAtTime(gain * part * LEVEL, when + 0.012);
      env.gain.exponentialRampToValueAtTime(0.0001, when + seconds);
      osc.connect(env).connect(out);
      osc.start(when);
      osc.stop(when + seconds + 0.05);
    });
  }

  // A short sweep of one oscillator from one pitch to another (used for the pop and the swelling hum).
  function sweep({ ctx, out }, when, type, from, to, gain, seconds, filterFrom, filterTo) {
    const osc = ctx.createOscillator();
    const env = ctx.createGain();
    osc.type = type;
    osc.frequency.setValueAtTime(from, when);
    osc.frequency.exponentialRampToValueAtTime(to, when + seconds);
    env.gain.setValueAtTime(0.0001, when);
    env.gain.linearRampToValueAtTime(gain * LEVEL, when + Math.min(0.03, seconds / 3));
    env.gain.linearRampToValueAtTime(0.0001, when + seconds);
    let tail = osc;
    if (filterFrom) {
      const filter = ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(filterFrom, when);
      filter.frequency.exponentialRampToValueAtTime(filterTo, when + seconds);
      osc.connect(filter);
      tail = filter;
    }
    tail.connect(env).connect(out);
    osc.start(when);
    osc.stop(when + seconds + 0.05);
  }

  // A burst of filtered noise (the pop's crack and the smoke's whoosh).
  function burst({ ctx, out }, when, type, from, to, gain, seconds, attack) {
    const source = ctx.createBufferSource();
    source.buffer = noiseBuffer(ctx);
    source.loop = true;
    const filter = ctx.createBiquadFilter();
    filter.type = type;
    filter.frequency.setValueAtTime(from, when);
    filter.frequency.exponentialRampToValueAtTime(to, when + seconds);
    const env = ctx.createGain();
    env.gain.setValueAtTime(0.0001, when);
    env.gain.linearRampToValueAtTime(gain * LEVEL, when + attack);
    env.gain.exponentialRampToValueAtTime(0.0001, when + seconds);
    source.connect(filter).connect(env).connect(out);
    source.start(when);
    source.stop(when + seconds + 0.05);
  }

  // The pumpkin story's soundtrack, timed to the 8 s CSS timeline (see style.css). The audio clock and the
  // CSS animations are paused together, so they stay in step through Pause and Play.
  function pumpkinStory(a) {
    const t0 = a.ctx.currentTime + 0.03;
    [1046.5, 1318.5, 1568, 2093].forEach((f, i) => bell(a, t0 + 0.05 + i * 0.1, f, 0.05, 0.6));   // faces light up: rising sparkle
    sweep(a, t0 + 1.2, 'sawtooth', 110, 330, 0.05, 1.6, 400, 1800);                               // the pumpkins shake: swelling hum
    sweep(a, t0 + 2.8, 'sine', 520, 80, 0.3, 0.16);                                                // the lid pops: thump...
    burst(a, t0 + 2.8, 'bandpass', 1400, 600, 0.22, 0.1, 0.004);                                   // ...and crack
    bell(a, t0 + 3.3, 784, 0.07, 1.1);                                                             // the ghost appears: two soft chimes
    bell(a, t0 + 3.55, 1046.5, 0.07, 1.2);
    burst(a, t0 + 5.4, 'lowpass', 1800, 220, 0.18, 1.0, 0.08);                                     // smoke whoosh
    [2093, 1568, 1318.5].forEach((f, i) => bell(a, t0 + 6.8 + i * 0.12, f, 0.035, 0.7));           // everything settles: falling sparkle
  }

  // The graveyard story's soundtrack shares the same 8 s clock as its CSS timeline: a low rumble, three
  // sleepy stone creaks, playful ghost bells, then a soft settling puff.
  function graveyardStory(a) {
    const t0 = a.ctx.currentTime + 0.03;
    sweep(a, t0 + 0.05, 'sine', 72, 48, 0.18, 1.4, 230, 120);
    burst(a, t0 + 0.15, 'lowpass', 420, 110, 0.08, 1.2, 0.04);
    [0, 0.17, 0.34].forEach((offset, i) => sweep(a, t0 + 1.1 + offset, 'triangle', 230 + i * 45, 145 + i * 35, 0.1, 0.3, 620, 260));
    [523.25, 659.25, 783.99, 659.25, 880].forEach((f, i) => bell(a, t0 + 3.15 + i * 0.34, f, 0.055, 0.7));
    burst(a, t0 + 5.85, 'lowpass', 1250, 210, 0.14, 0.9, 0.06);
    bell(a, t0 + 6.9, 392, 0.04, 0.8);
  }

  // The house sequence: a wooden shudder, two window blinks, a tiny bright party, then the light snap.
  function houseStory(a) {
    const t0 = a.ctx.currentTime + 0.03;
    [0, 0.18, 0.36].forEach((offset, i) => sweep(a, t0 + 0.55 + offset, 'triangle', 145 - i * 10, 92 - i * 8, 0.1, 0.22, 600, 210));
    [0, 0.55].forEach((offset) => sweep(a, t0 + 1.9 + offset, 'sine', 640, 190, 0.11, 0.18, 1400, 350));
    sweep(a, t0 + 3.75, 'triangle', 250, 95, 0.12, 0.35, 800, 220);                               // door creak
    [659.25, 783.99, 880, 1046.5, 880].forEach((f, i) => bell(a, t0 + 4.35 + i * 0.28, f, 0.045, 0.55));
    burst(a, t0 + 6.35, 'lowpass', 1000, 280, 0.1, 0.16, 0.01);                                    // door shuts
    sweep(a, t0 + 6.8, 'sine', 150, 1100, 0.12, 0.09);                                             // lights return
  }

  const STORIES = { pumpkins: pumpkinStory, graveyard: graveyardStory, house: houseStory };

  const PUMPKIN_NOTES = [523.25, 659.25, 783.99, 1046.5];      // C5 E5 G5 C6: each pumpkin sounds higher than the last
  const GRAVE_NOTES = [392, 523.25, 466.16];                    // G4 C5 Bb4: distinct, more hollow tombstone taps
  const HOUSE_NOTES = [783.99, 659.25, 880];                     // G5 E5 A5: bright window taps, independent of position

  window.hollowCues = {
    story(name) {
      const a = audio();
      if (a && STORIES[name]) STORIES[name](a);
    },
    // Correct pumpkin number `step` (0 to 3) in the sequence.
    tap(step) {
      const a = audio();
      if (!a) return;
      const t = a.ctx.currentTime + 0.01;
      bell(a, t, PUMPKIN_NOTES[step % PUMPKIN_NOTES.length], 0.16, 0.9);
    },
    // Correct tombstone number `step` (0 to 2) in the left -> right -> center sequence.
    graveTap(step) {
      const a = audio();
      if (!a) return;
      bell(a, a.ctx.currentTime + 0.01, GRAVE_NOTES[step % GRAVE_NOTES.length], 0.14, 0.85);
    },
    // Correct window number `step` (0 to 2) in the right -> left -> upper-middle sequence.
    houseTap(step) {
      const a = audio();
      if (!a) return;
      bell(a, a.ctx.currentTime + 0.01, HOUSE_NOTES[step % HOUSE_NOTES.length], 0.14, 0.8);
    },
    // Wrong pumpkin: two soft, falling, muffled notes.
    nope() {
      const a = audio();
      if (!a) return;
      const t = a.ctx.currentTime + 0.01;
      sweep(a, t, 'triangle', 330, 200, 0.14, 0.2, 900, 300);
      sweep(a, t + 0.13, 'triangle', 247, 140, 0.14, 0.26, 700, 250);
    },
    // Any other object: a small muted tick, so every tap has some sound.
    tick() {
      const a = audio();
      if (a) sweep(a, a.ctx.currentTime + 0.01, 'sine', 700, 480, 0.09, 0.09);
    },
  };
})();
