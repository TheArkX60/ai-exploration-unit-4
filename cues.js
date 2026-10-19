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

  const STORIES = { pumpkins: pumpkinStory };

  window.hollowCues = {
    story(name) {
      const a = audio();
      if (a && STORIES[name]) STORIES[name](a);
    },
  };
})();
