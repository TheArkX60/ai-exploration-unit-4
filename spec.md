# Technical Specification

> EDITING DIRECTIVE: DEVELOPER AND AGENT EDIT THIS FILE COLLABORATIVELY. THE DEVELOPER MUST REVIEW AND APPROVE ITS CONTENT.

Purpose: Keep a concise, testable description of the experience currently being built.

## Working agreement

Developer: Begin with the running prototype, approve the intended behavior, test it directly, and update this file when the intended result changes.

Agent: Read `AGENTS.md`, `brief.md`, `research.md`, and this file, then inspect the project. Turn decisions into acceptance checks without inventing product choices or freezing details that still require testing.

Start a fresh chat with:

`Read the project documents, inspect the running prototype, and help me specify the next useful build checkpoint.`

## Current build contract

Define only enough to build and verify the current direction:

- the intended User experience and chosen scene, ambience, and story behavior
- the system structure, shared rules, and states that keep audiovisual behavior and interaction coordinated
- the assets and layout needed for that structure, linking to sources and credits in `research.md`
- acceptance checks for the chosen behavior and every requirement in `brief.md`, including accessibility and failure behavior

Reference the brief's fixed requirements rather than copying them. Specify your decisions precisely enough that the Developer and Agent can judge the same result. Leave untested details open until they are needed, and distinguish provisional ideas from approved behavior.

### Status (2026-10-19): Phase 1 scope built and verified (see `verification.md`). Palette and scaling approved by Developer 2026-10-18. Stories 2 and 3 are still to be specified in detail after the story 1 playtest. Items marked (provisional) are still open.

### Experience (approved direction in `research.md`)
Scene "Hollow Hill", sheet-ghost character, three independent stories, idle hints at ~15/30/45 s. This checkpoint covers only the static shell, not effects, audio or stories.

### Structure
- Plain `index.html`, `style.css`, `app.js`; inline SVG for art; no build step. Hosted on GitHub Pages (public HTTPS).
- One fixed-ratio stage, centered, scaled to fit the viewport height and width with no scrolling (SVG `viewBox` 360×640, `preserveAspectRatio="xMidYMid meet"` (whole scene always visible); revisit `slice` only if phone testing shows distracting margins).
- Full-bleed stage (changed 2026-10-19 after iPhone Safari test showed side bars): the stage always fills the viewport; the 360×640 art is centered and sky, hills and ground overshoot the `viewBox` on every side. UI sits in a centered column (max 450 px).
- Landscape (approved 2026-10-19): touch devices in landscape (`orientation: landscape`, height ≤ 500 px, `pointer: coarse`) show a full-screen "Turn your phone upright" message over the scene, because hotspots fall to ~29 px sideways. Desktop windows are unaffected. Not yet tied to Play/Pause (revisit when audio or effects exist).
- App states: `start` -> `running` <-> `paused`, plus a story flag (`state.story`, also `data-story` on `<html>`) that is set while a story plays. Scene taps are accepted only when the phase is `running` and no story is playing. Play/Pause works during a story and pauses it mid-sequence: story animations and sounds freeze together and resume where they stopped. (Refined 2026-10-19 from a single `story` phase, because a paused story must remember that it is mid-story.)
- Layers, back to front: sky (gradient, stars, moon) / far hill + house / graveyard + tree / pumpkin patch / fog slot / particle slot (leaves, bats) / story overlay slot / UI (hint line, Play/Pause, credits link).
- Hotspots: pumpkins (3+), tombstones (3), windows (3+), each a real focusable element (`button` or SVG `role="button" tabindex="0"`) with a minimum 44x44 CSS px hit area, even if the drawing is smaller.

### Palette (approved; contrast ratios computed from WCAG luminance)
| Role | Hex |
|---|---|
| Sky top / bottom | #0b0620 / #2a1146 |
| Horizon glow (behind house, needed for silhouette separation) | #7a3a9a |
| Moon | #f4e9b8 |
| House, far hill, ground silhouettes | #0e0720, #1c0f33, #120a24 |
| Window glow | #ffb347 |
| Pumpkin / pumpkin glow | #ff7a1a / #ffc247 |
| Ghost body / eyes | #f2f0ff / #1a0f2e |
| Fog (low alpha) | #6b5a8e |
| UI panel / text / hint text | #1a0f2e / #f5ecff / #ffd9a0 |
| Button / button text / focus ring | #ff7a1a / #1a0b05 / #7dff9b |

Computed contrast: UI text on panel 15.9, hint text 13.6, button text 7.4, focus ring vs sky 13.1, window vs house 11.0, pumpkin vs ground 7.4, ghost vs sky 14.8, house vs horizon glow 2.7 (silhouette shape, not text; acceptable). Known weak spot: graveyard stones against sky are too close if both are dark purple, so stones get a lighter rim or sit against the horizon glow.

### Shared rules: hints and failure behavior (approved by Developer 2026-10-18; timings are starting values, tune in playtests)

**Hints**
- H1. Idle timer resets on any tap/key activation on the scene or a hotspot, correct or not.
- H2. After a reset, hints restart at level 1.
- H3. Levels appear at ~15, 30, 45 s idle. After level 3 it stays visible; there is no level 4 or cycling.
- H4. Hints are scene-wide and never depend on which stories were seen. Level 1: vague mood line. Level 2: names an area (graveyard, patch, house). Level 3: hints at a relevant attribute (size or position) without stating the trigger.
- H5. Timers freeze while paused. During a story they stop and the hint line is hidden; after the story ends they restart at 0 with no hint shown.
- H6. One line of text, >= 16 px, >= 4.5:1 contrast, fades in (plain swap under reduced motion).

**Hint wording (Developer chose 2026-10-19; lines live in a table in `hints.js`)**
| Level | While only the pumpkin story exists (in use) | For the finished game (switch `ACTIVE` in `hints.js` when stories 2 and 3 exist) |
|---|---|---|
| 1, about 15 s | The hill is restless tonight… | The hill is restless tonight… |
| 2, about 30 s | Look near the pumpkin patch… | Look near the patch, the graves, the house. |
| 3, about 45 s | Size matters… patterns wake them. | Size and position matter… patterns wake them. |

Rules as built (stage 4): H1 any tap on the scene, hotspot or empty sky, with the mouse, touch or keyboard, restarts the idle clock and hides the hint; H5 the clock counts only while running with no story, and a story hides the hint and restarts the clock at 0 afterwards; the hint line is `sfx`, so its fade freezes on Pause, and it is a plain swap under reduced motion. Tapping the Pause or Credits buttons does not count as a scene tap.

**Failure and edge behavior**
- F1. A wrong tap in a sequence plays a short distinct "nope" cue (soft sound + wobble) and resets that sequence.
- F2. Each correct tap gives a unique tone and a light-up that stays lit until the sequence completes or resets, so progress is visible.
- F3. A partial sequence resets after ~8 s with no taps.
- F4. If audio is blocked or fails to load, the scene and stories still work with visual feedback, and a small non-blocking "sound unavailable" note appears. Audio starts only after Enter.
- F5. Taps and keys on scene interactions are ignored while a story plays; a visible "story playing" indicator explains why. Play/Pause still works.
- F6. Hiding or backgrounding the tab auto-pauses (same state as Play/Pause) and stays paused until the User resumes.
- F7. With reduced motion on, ambient motion is off and stories still play using fades, glows, and sound instead of movement.

Test for each: H1-H6 by waiting and tapping with a shortened timer setting; F1-F3 by wrong, partial, and abandoned sequences; F4 by blocking audio files in DevTools; F5 by tapping during a story; F6 by switching tabs; F7 by toggling the reduced-motion setting.

### Story acceptance checks (DRAFT for Developer review; stories not built yet, so exact visuals and timings stay open until tested)

**Checks for every story (S1-S7)**
- S1. Total runtime from the completing tap to return to the scene is 5-10 s, measured with a stopwatch or `performance.now()` log.
- S2. Clear beginning (trigger payoff starts), middle (peak moment), and end (scene settles); the Developer can name all three when watching.
- S3. Uses animation, sound, and a visual effect together; none is missing (sound absent under F4 is the only allowed exception).
- S4. Replays without reloading: trigger it 3 times in a row and it behaves identically each time, with the scene fully restored.
- S5. While it plays, every other scene interaction is ignored (F5), including hotspots of the other stories. Play/Pause still works and pauses and resumes the story mid-sequence.
- S6. When it ends, a visible cue returns control (indicator off, hotspots interactive again) and the hint timer restarts at 0 (H5).
- S7. Triggers are independent: any story can be played first, and no story's content depends on another having been seen.

**Trigger checks (T1-T4)**
- T1. Every tap on a trigger hotspot gives its own audiovisual response (F2).
- T2. Wrong taps and timeouts follow F1 and F3.
- T3. Keyboard: the same sequence works with Tab and Enter/Space.
- T4. The trigger is not stated in any text; hints follow H4.

**Story-specific checks**
- Pumpkin Patch: pumpkins tapped smallest to biggest, each with a different tone and light-up. Beats: grins and glows -> biggest pops open -> ghost peeks out -> smoke puff -> pumpkins revert. Pass: pumpkins return to their original look.

**Story 1 build spec (approved by Developer 2026-10-19)**
- Trigger: all four pumpkins, smallest to biggest (left to right). Wrong order, timeout and hints follow F1-F3 and H1-H6.
- Trigger rules as built (stage 2, 2026-10-19): a correct tap gives that pumpkin's own tone (C5, E5, G5, C6) and a golden light-up that stays on as progress. The fourth correct tap clears the lights and starts the story. A wrong pumpkin (including the same one twice) plays a soft falling "nope", wobbles that pumpkin (a brief fade under reduced motion) and resets all progress; the wrong tap does not count toward a new sequence. A half-finished sequence is forgotten after 8 s with no taps on the scene; the 8 s count stops during Pause and during a story, and a tap on any object, not only pumpkins, restarts it. Tombstones and windows are not triggers yet: they flash and play a soft tick, and do not affect the pumpkin sequence. Keyboard (Tab, Enter, Space) works the same as touch. A mouse or touch tap releases keyboard focus from the object so a stray Enter cannot re-tap it, and a held key counts as one tap.
- Lock and return (stage 3, 2026-10-19; F5, S6): while a story plays, a note under the buttons reads "A story is playing…" (16 px, same spot as the hint line). When the story ends it reads "Your turn: keep exploring" for about 1.6 s, then fades out over 0.8 s; scene taps work from the moment the story ends. The note's fades are CSS animations, so Pause freezes them. Stage 4 (hints) must hide the hint line during stories and restart its timer at 0 when the story ends (H5).
- Sounds are synthesized with Web Audio in `cues.js` (no external files, so no new credits): rising tap tones, a "nope" cue, and story cues (sparkles, a swelling hum, a pop, chimes, a smoke whoosh). No ghost voice for now.
- Build stages, each tested before the next: (1) the sequence alone, started from the console with `hollowStory.play('pumpkins')` (done); (2) triggers and progress feedback; (3) input lock, "story playing" cue and return to the scene; (4) hints.
- Sequence (about 8 s, one 8 s clock; Pause freezes it):
  - 0-1 s: faces appear on all four pumpkins and glow.
  - 1.2-2.7 s: the pumpkins shake while the glow swells.
  - 2.8 s: the biggest pumpkin's lid pops off with a "pop"; the opening shows dark inside.
  - 3.0-3.9 s: the party-hat ghost rises out of the opening; 3.9-5.4 s it wobbles.
  - 5.4-5.9 s: the ghost sinks back as a smoke puff (5.4-7 s) covers the opening.
  - 6.8-8 s: faces and glow fade, leaving the pumpkins as they were.
- Reduced motion (F7): no shaking, flying or rising. Faces and glow still fade, the ghost fades in and out in place, the smoke only fades, and sounds still play.
- Pass: it can be played repeatedly without reloading and looks identical each time; afterwards the patch looks exactly as before.

**Story 2 build spec (approved by Developer 2026-10-25)**
- Trigger: tombstones left -> right -> center (IDs 1, 3, 2). It is a fixed order, not a rhythm/timing puzzle. Wrong order, a repeated tombstone and an 8 s idle timeout reset its three progress lights under F1-F3.
- Feedback: correct tombstones give persistent golden lights and three distinct synthesized notes, G4 -> C5 -> B-flat4. The notes rise through the left/right portion of the path then settle lower at the center. A wrong tombstone plays the shared falling "nope" cue and shakes as one whole hotspot (including the center stone's cross); under reduced motion it fades instead.
- Sequence (about 8 s, with the shared story lock and Pause): ground rumble -> stones yawn one after another -> three small ghosts rise, wobble-dance and sink -> ground mist settles -> scene resets.
- Reduced motion: the rumble, stone yawn, ghost rise/dance and mist growth become fades, while the story sound remains. The shared lock/return note, hints, keyboard and touch behavior match Story 1.
- Developer review: the sequence and sound direction are accepted for now; the music may be retuned later after more complete-scene testing.

**Story 3 build spec (approved by Developer 2026-10-25)**
- Trigger: windows right -> left -> upper-middle (IDs 3, 1, 2). It is a fixed order, not the order of the ambient flicker. Wrong order, a repeated window and an 8 s idle timeout reset the three progress lights under F1-F3.
- Feedback: correct windows give persistent golden lights and three distinct bright synthesized notes. A wrong window plays the shared falling "nope" cue and shakes as a complete window hotspot; under reduced motion it fades instead.
- Sequence (about 8 s, with the shared story lock and Pause): house shudders -> windows blink like eyes -> door opens on three tiny dancing ghosts -> door closes and the lights snap off, then back on -> scene resets.
- Reduced motion: the house shake, window squash, door fold and party dance become opacity/light changes, while sound remains. The shared lock/return note, hints, keyboard and touch behavior match Stories 1 and 2.
- Pause repair (2026-10-25): the House building and each tombstone are in the shared `.sfx` scope, so their story and wrong-tap animations freeze under Pause with the overlay art. The far hill is intentionally outside the House building group and never moves during its shudder.
- With all three stories now present, the active hint wording is the all-stories set in `hints.js` (patch, graves and house; then "Size and position matter… patterns wake them."). "Rhythm" was removed because no implemented trigger uses timing.
- Graveyard: three tombstones tapped in a fixed left -> right -> center order (approved 2026-10-25; no timing requirement). Beats: ground rumbles -> tombstones yawn -> three little ghosts wobble-dance -> sink back. Pass: stones return to their original look.
- The House: windows tapped in the order they flicker (flicker cue replays when needed; exact rule open). Beats: house shudders -> windows blink like eyes -> door opens on a tiny ghost party -> lights snap off then on. Pass: house returns to its original look.

**Brief checks that apply across stories:** content is suitable for ages 10+ with no gore or realistic violence; the three stories exist and are discoverable; and all effects are original or properly credited assets (see credits).

### Ghost design (direction approved by Developer 2026-10-18; appearance is provisional and may change after seeing it rendered)
- Classic sheet ghost as one SVG path: rounded head, wavy hem, two small nub arms. Body #f2f0ff with a faint soft glow.
- Face: two round dark eyes (#1a0f2e) and a small "o" mouth that switches to a smile or gasp during stories. Friendly and slightly clumsy, never menacing.
- Party hat on the pumpkin-story ghost to signal "wants to throw a party" (hat is a separate small shape, easy to remove or change).
- One base drawing reused: smaller copies for the graveyard ghosts and a tiny copy at the house party.
- Original, drawn in code; credit the Developer only.
- Change rule: the design lives in one reusable SVG symbol, so a redesign is one edit.

### Assets (sound approach approved 2026-10-18: use free-to-use sources first; synthesize with Web Audio only where a free source does not work)
Visuals: all original and drawn in code, no external visual assets.

| Sound | Used for | Plan |
|---|---|---|
| Wind (approved 2026-10-19: IgnasD gust recordings) | Ambient bed. The files are single gusts, so they are chained: each starts when the previous is 55-75% done, with random pitch (±8%) and loudness, so there is always wind and it never repeats exactly | CC0, see `research.md` |
| Owl hoot (approved 2026-10-19: Breviceps) | Occasional ambient: first hoot 10-16 s after Enter, then one every 22-44 s, panned left or right | CC0, see `research.md` |
| Pumpkin tones (3) and "nope" cue | Story 1, F1 | CC0/public-domain, synthesize if none fits |
| Pop, smoke puff | Story 1 | CC0/public-domain, synthesize if none fits |
| Rumble, stone yawn, wobble | Story 2 | CC0/public-domain, synthesize if none fits |
| Creak, door, party sounds, light snap | Story 3 | CC0/public-domain, synthesize if none fits |

Rule: no sound is used until its source link, license, and required credit are recorded in `research.md` (Assets section) and the Developer approves it. Sourcing is done per checkpoint (ambient audio first), not all at once.

### Acceptance checks for checkpoint 4 (ambient audio)
- A1. No sound, and no audio context, before Enter; Enter starts it (iOS only allows sound after a tap).
- A2. After Enter the wind is continuous: no silent gap longer than about a second, and consecutive gusts differ in pitch and loudness.
- A3. The owl hoots occasionally (about one per 22-44 s, first at 10-16 s), panned left or right.
- A4. Play/Pause: Pause silences everything, and the audio clock and scheduling stop with it; Play resumes the wind where it left off and starts no burst of queued sounds.
- A5. Failure (F4): with the audio files blocked, or with no Web Audio, a small non-blocking "Sound unavailable" note appears and the scene, taps and Pause still work. A file that is slow or fails alone does not silence the others.
- A6. Reduced motion does not affect sound.
- A7. Credits panel names both sound sources.
- Levels (`MASTER_GAIN`, `WIND_GAIN`, `OWL_GAIN` in `audio.js`) are provisional; the Developer tunes them by ear on a phone. Note the iPhone silent switch mutes web audio.

### Acceptance checks for this checkpoint
1. Opens from a local preview with no console errors.
2. Start screen shows title, Enter button (>=44 px), and the scene is not visible/animated until Enter is pressed.
3. The reduced-motion preference (`prefers-reduced-motion`) is read before Enter and stored in app state; with it on, nothing moves in later checkpoints. Verify by toggling the OS/DevTools setting and logging the state.
4. After Enter, the full scene fits without scrolling at 360x640, 390x844, 430x932, plus one landscape/desktop window (centered, no distortion). Screenshots at each.
5. Scene has a clear focal point (house + moon) and at least three distinct features (graveyard, pumpkin patch, tree with lantern).
6. Empty named layers exist for fog, particles and story overlay.
7. Pumpkins, tombstones and windows are reachable by Tab, show a visible focus ring, and activate with Enter/Space and with touch/click; activation gives placeholder visual feedback only.
8. Play/Pause button is present, unobtrusive, keyboard and touch operable, toggles state and its label (`aria-pressed`).
9. A credits link/panel shows the Developer name and a placeholder for assets.
10. Text is >= 16 px and meets 4.5:1 contrast.

Checkpoint 1 status: these ten checks passed on 2026-10-19 and have been re-verified on the live site since (see `verification.md`). Check 9's credits placeholder has been replaced by the real credits.

Still to build for the full brief: stories 2 (graveyard) and 3 (the house), and the final polish and re-verification pass.

## Scope and revisions

**Built and verified for Phase 1 (2026-10-19):** the static shell, five ambient effects (stars, window and lantern flicker, fog, bats, leaves), ambient audio (wind and owl), full Play/Pause plus auto-pause, story 1 (pumpkins) with triggers, progress feedback, wrong-tap and timeout behavior, input lock and return note, idle hints, and credits. Results: `verification.md`.
**Excluded for now:** stories 2 and 3, the ghosts-found counter, any 3D.
**Next:** build and verify Story 2 (graveyard), then use its completed shared pattern for Story 3 (the house). The Phase 1 playtest found no pumpkin-story revision to make; its consequential lesson was that the remaining apparently interactive areas must receive their promised stories (`plan.md`).
Requirement changes so far are recorded where they were made: full-bleed stage, landscape overlay, story flag instead of a story phase, wind built from chained gusts, auto-pause (F6), and the Phase 1 hint wording.

## Saving the transcript

When directed, save the complete conversation as `transcripts/spec-YYYY-MM-DD_HHMMSS.md`, label messages `Developer` and `Agent`, and confirm the path.
