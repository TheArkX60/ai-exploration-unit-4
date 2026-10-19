// Hollow Hill: ambient audio (checkpoint 4).
// Wind: IgnasD's single gusts, chained so one starts before the previous fades, with random pitch and
// loudness, so there is always some wind and it never repeats exactly. Owl: an occasional hoot.
// app.js announces state changes ('hollow:phase'); this file only reacts to them, so Play/Pause stays
// governed by the single state rule. Sources and licenses: research.md and the Credits panel.
(() => {
  'use strict';

  const WIND_FILES = ['assets/audio/wind-gust-1.m4a', 'assets/audio/wind-gust-2.m4a', 'assets/audio/wind-gust-3.m4a'];
  const OWL_FILE = 'assets/audio/owl-hoot.mp3';
  const FETCH_TIMEOUT_MS = 20000;

  // Levels. The source files are quiet (peaks around -21 dBFS, the owl around -28), so they are boosted;
  // a compressor keeps overlapping gusts from clipping. Tune these by ear.
  const MASTER_GAIN = 0.9;
  const WIND_GAIN = 4;
  const OWL_GAIN = 7;

  // Timing (seconds). Each gust starts when the previous one is 55-75% done, so they overlap.
  const GUST_OVERLAP_MIN = 0.55;
  const GUST_OVERLAP_MAX = 0.75;
  const OWL_FIRST_MIN = 10, OWL_FIRST_MAX = 16;     // first hoot after Enter
  const OWL_GAP_MIN = 22, OWL_GAP_MAX = 44;         // then one every 22-44 s

  const note = document.getElementById('sound-note');
  const rand = (min, max) => min + Math.random() * (max - min);

  let ctx = null;
  let master = null;
  let analyser = null;
  const windBuffers = [];      // by index into WIND_FILES; a slot stays empty if that file failed to load
  let owlBuffer = null;
  let started = false;
  let wantPaused = false;      // Pause pressed before the audio context existed
  let lastGust = -1;
  let nextGustAt = 0;
  let nextOwlAt = 0;
  const counts = { gusts: 0, hoots: 0 };

  // Download the files now (no user gesture needed). Each has its own timeout, so one slow or stalled
  // file cannot hold up the rest. Decoding waits for the audio context created at Enter.
  function fetchBytes(url) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
    return fetch(url, { signal: controller.signal })
      .then((response) => {
        if (!response.ok) throw new Error(`${url}: HTTP ${response.status}`);
        return response.arrayBuffer();
      })
      .finally(() => clearTimeout(timer));
  }
  const downloads = [...WIND_FILES, OWL_FILE].map(fetchBytes);
  downloads.forEach((d) => d.catch(() => {}));         // failures are handled in start()

  function showUnavailable(error) {
    console.warn('[hollow-hill] sound unavailable:', error);
    if (note) note.hidden = false;
  }

  const hasWind = () => windBuffers.some(Boolean);

  function playGust() {
    // Pick among the loaded gusts, not the one just played; the 1.7 s flutter (index 2) is played less often.
    const choices = [0, 1, 2].filter((i) => windBuffers[i] && (i !== lastGust || windBuffers.filter(Boolean).length === 1));
    const weights = choices.map((i) => (i === 2 ? 0.25 : 1));
    let pick = Math.random() * weights.reduce((a, b) => a + b, 0);
    let index = choices[choices.length - 1];
    for (let k = 0; k < choices.length; k++) {
      pick -= weights[k];
      if (pick <= 0) { index = choices[k]; break; }
    }
    lastGust = index;

    const buffer = windBuffers[index];
    const rate = rand(0.92, 1.08);
    const level = rand(0.65, 1) * WIND_GAIN;
    const when = Math.max(nextGustAt, ctx.currentTime + 0.05);
    const length = buffer.duration / rate;

    const source = ctx.createBufferSource();
    source.buffer = buffer;
    source.playbackRate.value = rate;
    const gain = ctx.createGain();
    // Short fades at both ends so no gust can click, whatever the file's first and last samples are.
    gain.gain.setValueAtTime(0, when);
    gain.gain.linearRampToValueAtTime(level, when + 0.15);
    gain.gain.setValueAtTime(level, when + length - 0.3);
    gain.gain.linearRampToValueAtTime(0, when + length);
    source.connect(gain).connect(master);
    source.start(when);
    counts.gusts += 1;
    nextGustAt = when + length * rand(GUST_OVERLAP_MIN, GUST_OVERLAP_MAX);
  }

  function playOwl() {
    const source = ctx.createBufferSource();
    source.buffer = owlBuffer;
    const gain = ctx.createGain();
    gain.gain.value = OWL_GAIN * rand(0.8, 1);
    let tail = gain;
    if (ctx.createStereoPanner) {                      // somewhere left or right, as if in a nearby tree
      const pan = ctx.createStereoPanner();
      pan.pan.value = rand(-0.7, 0.7);
      gain.connect(pan);
      tail = pan;
    }
    source.connect(gain);
    tail.connect(master);
    source.start(ctx.currentTime + 0.05);
    counts.hoots += 1;
    nextOwlAt = ctx.currentTime + rand(OWL_GAP_MIN, OWL_GAP_MAX);
  }

  // Runs every 250 ms. It follows the audio clock, which stops while the context is suspended,
  // so nothing new is scheduled during Pause. Sounds join as soon as their files are decoded.
  function schedule() {
    if (!ctx || ctx.state !== 'running') return;
    if (hasWind()) {
      while (nextGustAt < ctx.currentTime + 0.6) playGust();
    }
    if (owlBuffer && ctx.currentTime >= nextOwlAt) playOwl();
  }

  async function start() {
    if (started) return;
    started = true;
    try {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (!AudioCtx) throw new Error('Web Audio is not available');
      ctx = new AudioCtx();
      const resumed = ctx.resume();                    // called inside the Enter tap, which iOS requires
      console.info('[hollow-hill] audio: context created, state', ctx.state);

      master = ctx.createGain();
      master.gain.value = MASTER_GAIN;
      const limiter = ctx.createDynamicsCompressor();
      analyser = ctx.createAnalyser();
      analyser.fftSize = 2048;
      master.connect(limiter).connect(analyser);
      limiter.connect(ctx.destination);

      nextGustAt = ctx.currentTime;
      nextOwlAt = ctx.currentTime + rand(OWL_FIRST_MIN, OWL_FIRST_MAX);
      setInterval(schedule, 250);
      if (wantPaused) ctx.suspend();

      // Decode each file as it arrives; the sounds start as soon as their own file is ready.
      const loads = downloads.map((download, i) => download
        .then((bytes) => ctx.decodeAudioData(bytes.slice(0)))
        .then((buffer) => {
          if (i < WIND_FILES.length) windBuffers[i] = buffer;
          else owlBuffer = buffer;
          console.info('[hollow-hill] audio: ready', i < WIND_FILES.length ? `wind ${i + 1}` : 'owl');
          schedule();
        })
        .catch((error) => console.warn('[hollow-hill] audio: could not load file', i, error)));
      await resumed;
      await Promise.allSettled(loads);
      if (!hasWind()) showUnavailable('no wind sound could be loaded');
    } catch (error) {
      showUnavailable(error);
    }
  }

  document.addEventListener('hollow:phase', (event) => {
    const phase = event.detail.phase;
    if (phase === 'running') {
      wantPaused = false;
      if (!started) start();
      else if (ctx) ctx.resume();
    } else if (phase === 'paused') {
      wantPaused = true;
      if (ctx) ctx.suspend();                          // freezes every sound and the scheduling clock together
    }
  });

  // Read-only view for testing and troubleshooting from the browser console.
  window.hollowAudio = {
    status: () => ({ started, state: ctx && ctx.state, time: ctx && ctx.currentTime, ...counts, loaded: windBuffers.filter(Boolean).length + (owlBuffer ? 1 : 0) }),
    levelDb: () => {
      if (!analyser) return -Infinity;
      const samples = new Float32Array(analyser.fftSize);
      analyser.getFloatTimeDomainData(samples);
      const meanSquare = samples.reduce((sum, v) => sum + v * v, 0) / samples.length;
      return 10 * Math.log10(meanSquare + 1e-12);
    },
  };
})();
