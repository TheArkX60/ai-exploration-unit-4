# Project Verification

> EDITING DIRECTIVE: DEVELOPER AND AGENT EDIT THIS FILE COLLABORATIVELY. THE DEVELOPER MUST REVIEW AND APPROVE ITS CONTENT.

Purpose: show, requirement by requirement, what was verified for the deployed Phase 1 prototype and the completed three-story build against `brief.md` and `spec.md`, with evidence and gaps stated plainly.

- **Deployed build checked:** https://thearkx60.github.io/ai-exploration-unit-4/ (GitHub Pages, `main`), 2026-10-19, commits `3475ae7` and later (version stamp `20261019-11`/`-12`).
- **Final three-story build:** deployed 2026-10-25 from commit `be44546` (version stamp `20261025-01`); final phone review reported below.
- **How it was checked:** the Agent drove the live site in headless Chrome with real mouse clicks, real key presses and touch events at 360x640, 390x844 and 430x932, and the same code in Playwright WebKit (iPhone's engine; it has no Web Audio, so sound is not testable there). Pass/fail comes from measured values (element sizes, computed styles, animation states, audio clock and level), not from looking. The Developer checked each step on a physical iPhone and on a computer, and judged looks and sound by eye and ear.
- **Repeatable:** the checks were saved as scripts in `tests/` (see `tests/README.md`), so they can be re-run after the playtest fixes and extended for stories 2 and 3. `tests/test_audit_live.py` is this audit's live-site run.
- **Not checkable by the Agent:** how the sound actually sounds, and real-iPhone behavior beyond what the Developer reported. The Developer reports a final phone review of the deployed three-story build below.

## Brief: Phase 1 requirements

| # | Requirement (`brief.md`) | Result | Evidence |
|---|---|---|---|
| B1 | One cohesive scene that fits a vertical phone without scrolling or page changes | Pass | No scrolling at 360x640, 390x844, 430x932 (live run, scrollHeight/Width within the viewport). Stage fills the screen at every size; landscape phones get a "turn your phone upright" message. |
| B2 | Strong focal point and at least three distinct environmental features | Pass | Haunted house against a large moon; graveyard (3 tombstones), pumpkin patch (4 pumpkins), tree with hanging lantern. Screenshot: `screenshots/audit/live-390x844.png`. |
| B3 | At least three ambient effects | Pass (five) | Running on the live site: stars (18 elements), window and lantern flicker (4), fog (5), bats (3), falling leaves (12). |
| B4 | Looping ambient background sound | Pass | Wind (chained CC0 gusts with random pitch and loudness) and an occasional owl. 20 s after Enter: 7 gusts, 1 hoot, level -28 dB; in a 40 s run there were no silent gaps. |
| B5 | Start screen whose Enter button launches the scene and enables audio and animation | Pass | Before Enter: scene hidden, 0 animations running, no audio context. Enter button 56 px tall. After Enter: all effects and sound start. |
| B6 | Honor the reduced-motion preference before the experience begins | Pass | With the setting on, the page records it before Enter and shows "Reduced motion is on."; after Enter 0 ambient elements animate, bats and leaves stay offscreen, and sound still plays (sound is not motion). |
| B7 | One unobtrusive Play/Pause that pauses all motion, sound, effects, timers and scene interaction together | Pass | While paused: 0 animations running, audio suspended with its clock frozen, the hint idle clock and the trigger-sequence timeout frozen, taps ignored. Resumes together. Auto-pauses when the page is hidden. |
| B8 | Reliable by touch and keyboard; readable text; sufficient contrast; appropriately sized targets | Pass | Touch events completed the story 3 times in a row; Tab, Enter and Space complete it from the keyboard. No text under 16 px. Contrast ratios: title 14.5, notes 12.4, Enter button 7.4, Pause and Credits 15.9, hint 13.6, story note 13.6, sound note 13.6, credits 18.3 (minimum 4.5). Hotspots at least 48 px, buttons 44 px or more, Enter 56 px. |
| B9 | Public HTTPS URL | Pass | `https:` and a secure context on the live site. |
| B10 | Credit the Developer and all external code, visual and audio assets; only original, AI-generated, public-domain or licensed material | Pass | Credits panel names the Developer, the two CC0 sound sources with links, and states that visuals and story sounds are original and made in code. The page loads only from its own host; no images; no outside scripts, fonts or libraries. Source and license records: `research.md`. |
| B11 | No specific branding | Pass | No brand names in the page. "Virtual Hallo'weenie" is the brief's own project title. |
| B12 | Appropriate for ages 10 and over; no gore or realistic violence | Pass (by review) | A friendly party-hat ghost, jack-o-lanterns, smoke. Judged by review, to be confirmed by playtesters. |
| B13 | Browser-based HTML, CSS and JavaScript; 2D | Pass | Plain HTML, CSS and JavaScript, inline SVG, no build step, no libraries. |

## Brief: story requirements (one story for Phase 1)

| # | Requirement | Result | Evidence |
|---|---|---|---|
| S1 | A discoverable audiovisual story using animation, sound and a visual effect, with a clear beginning, middle and end | Pass | Pumpkin story: faces and glow (beginning), lid pops and ghost rises (middle), smoke and everything fading back (end). CSS animation plus synthesized sound plus glow and smoke. Frames inspected at 12 moments. |
| S2 | Lasts 5 to 10 seconds | Pass | 8.0 to 8.1 s in every run, including three touch runs on the live site (8.04, 8.05, 8.06 s). |
| S3 | Replayable without reloading | Pass | Played 3 times in a row by touch and by mouse; the patch was restored exactly each time (all story elements back to their idle values). |
| S4 | Triggered through scene interaction; all interactions give audiovisual feedback; triggers respond uniquely and show progress | Pass | Four pumpkins smallest to biggest; each correct tap gives its own note (C, E, G, C) and a golden light that stays on as progress. Wrong tap: "nope" sound and wobble. Tombstones and windows also flash and tick. |
| S5 | Progressive text hints over time that are hints, not instructions | Pass | At 14.9, 29.7 and 44.8 s (real-time run): "The hill is restless tonight…", "Look near the pumpkin patch…", "Size matters… patterns wake them." Any tap resets them; Pause and stories stop the clock. |
| S6 | Disable other interactions while a story plays, then return clearly | Pass | Taps ignored during the story and a second start refused; the note "A story is playing…" explains why; "Your turn: keep exploring" shows when it ends; taps work the instant it ends. Pause freezes the story mid-sequence. |

## Spec checks (`spec.md`)

| Group | Result | Evidence |
|---|---|---|
| Checkpoint 1, checks 1 to 10 | Pass | Zero console errors on the live site at three sizes; start screen and Enter; reduced-motion read; fits without scrolling; focal point and features; empty fog, particle and story layers existed (now filled); Tab order, focus ring, Enter, Space and touch on every hotspot; Play/Pause with `aria-pressed`; credits; text size and contrast. |
| A1 to A7 (ambient audio) | Pass | No audio before Enter; continuous wind; owl at 10 to 16 s then every 22 to 44 s; Pause silences and the clock stops; with audio blocked, the "Sound unavailable" note appears while taps, progress lights and Pause still work; reduced motion does not affect sound; credits name both sources. |
| H1 to H6 (hints) | Pass | Timings above; a tap on empty sky, a wrong pumpkin, or a keyboard Enter each restarted them at level 1; no level 4 or cycling (level 3 still showing at 52 s); Pause froze the clock; a story hid the hint and restarted the clock at 0; one 16 px line that fits at 360 px; fade-in becomes a plain swap under reduced motion. |
| F1 to F7 (failure and edge behavior) | Pass | F1 wrong tap resets with a distinct cue; F2 unique tones with lights that stay lit; F3 the partial sequence resets between 7 and 8.8 s of idle; F4 audio blocked or failed: note and everything else still works; F5 taps ignored while a story plays, with a visible note; F6 hiding the tab pauses it and it stays paused until Play; F7 reduced motion keeps the story with fades. |
| S1 to S7 and T1 to T4 (story checks) | Pass for story 1 | Runtime 8.0 s; clear beats; animation, sound and effect together; replays identically; other input ignored but Pause works; control returns with a cue and the hint clock restarts at 0; trigger responses are unique and keyboard-operable. See the T4 note below. |

## Phase 2: completed stories and final review

| Story | Trigger and feedback | Automated browser evidence (2026-10-25) |
|---|---|---|
| Pumpkin Patch | Four pumpkins, smallest to largest; unique tones and persistent progress lights; wrong-order reset | Existing trigger and story tests passed in the quick suite; the story ran about 8.1 s and replayed with its scene restored. |
| Graveyard | Tombstones left -> right -> center; three distinct notes and progress lights; wrong-order reset | `test_graveyard.py`: about 8.03 s; correct order, wrong tap, replay, reduced-motion variant, Pause freeze, and zero browser exceptions. |
| The House | Windows right -> left -> upper-middle; distinct notes and progress lights; wrong-order reset | `test_house.py`: about 8.01 s; correct order, wrong tap, replay, reduced-motion variant, Pause freeze, and zero browser exceptions. |

`python tests/run_all.py --quick` completed all 13 checks without a crash. Both new story tests were corrected to wait for the browser to commit the paused frame and measure the animation clock; they confirmed that story animation remained frozen during Pause.

**Developer phone review (2026-10-25):** The Developer opened the deployed three-story build on a phone and reported, "Everything works as intended." This is a report of the Developer's device check, not a cross-device peer study.

**Informal showcase (Developer report, 2026-10-26):** The Developer showed the finished version to other people and reports that they liked it. This was not a structured usability session and produced no individual observations or device details. The Phase 2 peer-playtesting requirement in `brief.md` was not completed; the informal reactions are recorded without treating them as a substitute.

The earlier Phase 1 audit below is retained as a historical snapshot; it is not a complete audit of every final-build requirement. Story-specific automated checks and the Developer's final phone report above provide the recorded Phase 2 evidence.

## Bugs found and fixed during verification

Each was found by testing, fixed, and re-tested; the details are in `plan.md`. The notable ones: a stylesheet priority problem that stopped Pause from freezing the story's pictures; the first sound request stalling and silencing everything (each file now loads independently with a timeout); a fresh page paired with a cached old stylesheet breaking the bats on a phone (version stamps on the stylesheet and scripts); Enter after a mouse click re-tapping the clicked pumpkin (focus is now released after a pointer tap, and key repeat is ignored).

## Remaining judgment calls and limitations

1. **T4 (trigger not stated in any text).** Hints do not state it, but the pumpkins' accessible names are "Pumpkin 1" to "Pumpkin 4", left to right, which implies an order to screen-reader users. This remains a judgment call; distinct accessible names are necessary.
2. **Window and lantern sliver (accepted open issue).** A thin yellow edge on the left of lit windows appeared on the Developer's computer, but was not reproduced by the Agent in headless Chrome, a real Edge window, or WebKit. The Developer did not specifically report it during the final phone review; revisit only if it becomes noticeable or users mention it.
3. **Landscape message is not tied to Pause.** If a phone is turned sideways during play, the scene keeps running behind the message. Low risk; not revisited after Stories 2 and 3 were added.
4. **Sound levels and character are provisional.** The wind, owl and synthesized cue levels were initially set by the Agent's estimate; the Developer judged the build's sound on-device. They can still be tuned in `audio.js` and `cues.js` if needed.
5. **Silent switch.** The iPhone ringer switch mutes web audio. The start screen says "Best with sound on."; a reminder can be considered if users report "no sound".
6. **Formal Phase 2 peer playtesting was skipped.** The Developer chose not to run structured sessions. Informal positive reactions from the showcase are recorded above but do not establish discoverability or usability across users and devices.
7. **Resume latency in the test browser.** After a long pause, headless Chrome took up to a few seconds to restart audio. The Developer reported that Pause and Play work on a phone.
