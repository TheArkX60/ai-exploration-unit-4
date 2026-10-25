# Implementation Plan

> EDITING DIRECTIVE: DEVELOPER AND AGENT EDIT THIS FILE COLLABORATIVELY. THE DEVELOPER MUST REVIEW AND APPROVE ITS CONTENT.

Purpose: Track the next useful build checkpoints, verification, and consequential revisions.

## Working agreement

Developer: Keep the browser preview running, choose priorities, test results directly, and plan only the next few checkpoints.

Agent: Read the project documents and inspect the files. Keep each checkpoint small enough to run and judge. Do not expand scope or mark Developer verification complete.

Start or continue a fresh chat with:

`Read the project documents, inspect the current build, and help me complete the next unchecked checkpoint.`

## Checkpoints

Create your own checklist for the next few results, using the workflow in `brief.md` and the current `spec.md`. Name the main risk, what each checkpoint should produce, and how you will verify it. Review and approve the approach before implementation.

Status: Approved by Developer 2026-10-19. Main risk across these: layout or layer structure that fails on real phones, found late. So deploy and check on a phone early.

- [x] **1. Static shell.** Start screen, state variable, reduced-motion read, static SVG scene in layers, placeholder hotspots, Play/Pause stub, credits stub. Verify: acceptance checks 1-10 in `spec.md`, screenshots at three phone sizes.
- [x] **2. Early deploy.** Push to GitHub Pages and open the HTTPS URL on a physical phone. Verify: scene fits, Enter works, tap targets usable. Catches viewport/address-bar issues before effects are added.
- [x] **3. Ambient visuals.** Fog, bats, flicker, leaves, stars, one at a time. Verify: each visible, loops cleanly, honors reduced motion, Play/Pause freezes them.
- [x] **4. Ambient audio.** Source and verify CC0 wind and owl (record in `research.md`), loop, gated by Enter, paused by Play/Pause.
- [x] **5. Story 1 (pumpkins)** as a standalone sequence first, then triggers, progress feedback, hints, input lock. Then Phase 1 playtest.
- [x] **6. Story 2 (graveyard).** Tombstones left -> right -> center, then ground rumble, yawning stones and three dancing ghosts. Verify the sequence, replay, Pause, reduced motion and feedback before reviewing it on a phone.
- [x] **7. Story 3 (house).** Windows right -> left -> upper-middle, then a shudder, blinking windows, door-party and light snap. Verify the sequence, replay, Pause, reduced motion and feedback before reviewing it on a phone.

Test each result before continuing, including related behavior that already works. Update priorities as evidence emerges and preserve meaningful working checkpoints in git. Before delivery, verify the deployed app against the brief and specification.

## Evidence and revisions

Record non-identifying playtest observations, separating what Users did or said from your interpretation. Use the findings to choose revision priorities and record what changed and how you verified the improvement.

### Checkpoints 1-2 (2026-10-19)

Live URL: https://thearkx60.github.io/ai-exploration-unit-4/ (GitHub Pages, `main`, root). Commits `242cffb`, `05c283b`, `4d496d3`. Screenshots: `screenshots/checkpoint-1/`, `screenshots/checkpoint-2/`.

**Verified by Agent (headless Chrome via DevTools protocol, not a physical phone):** `spec.md` checks 1-9 pass at 360x640, 390x844, 430x932 and 1280x720 (no console errors, no scrolling, hotspots >= 48 px, Tab/Enter/Space/click work, Play/Pause toggles and ignores taps while paused, credits opens); reduced-motion state reads `true` when emulated; the deployed HTTPS page loads, Enter works, 0 console errors. Check 10 (contrast): text sizes verified, ratios not re-measured beyond the spec's computed values.

**Developer observations (physical iPhone, Safari), and changes made:**
| What the Developer saw | Interpretation | Change | How verified |
|---|---|---|---|
| Green box around the scene after pressing Enter | Programmatic focus on the stage showed a keyboard focus ring | Removed the ring from the stage (kept on controls) | Keyboard Enter test: stage outline none, next Tab lands on "Window 1" |
| Tree very faint | Dark tree on dark ground, thick-line "tube" drawing | Redrawn as a tapered silhouette with a thin outer rim | Developer: "looks great" |
| Empty bars above/below on tall phones | 9:16 box on taller screens | Sky/ground extended into the extra height | Screenshots at 390x844, 430x932 |
| Bars at left and right, most noticeable when paused (top/bottom hidden behind Safari bars) | Stage width was capped at 9:16 of the dynamic viewport height, which shrinks while Safari's bars show; pause dimming covered only the scene | Stage always fills the viewport, art overshoots the `viewBox` on all sides, UI in a centered column (see `spec.md` Structure) | Headless at 390x664 (bars shown), 390x844, 844x390, 1280x720; Developer re-checked on iPhone: "Looks good" |
| (Agent finding, not seen by the Developer) Hotspots ~29 px in phone landscape | Scene scales to the short side | "Turn your phone upright" overlay for touch devices in landscape (see `spec.md`) | Headless: shown at 844x390 touch, hidden in portrait and on desktop (incl. a short desktop window); Developer re-checked on iPhone: "Looks good" |

**Not yet checked:** Safari on iPhone with Reduce Motion enabled; keyboard use on a physical device.

**Open for later:** the landscape overlay is not tied to Play/Pause; revisit when ambient effects and audio exist.

### Checkpoint 3: ambient visuals (all five effects built and phone-checked, 2026-10-19; awaiting Developer tick)

**Shared rule (done):** any element with class `fx` freezes under Play/Pause (`html[data-phase="paused"]`) and loses its animation under reduced motion (`html[data-reduced-motion="true"]`). New effects only add the class. See `style.css`.

| Effect | Status | Verified |
|---|---|---|
| Stars (twinkle: opacity and size, varied timing) | Done | Agent: values change while running, frozen when paused, steady under reduced motion. Developer: visible (after opening the right copy of the files; a stale preview showed no stars). Strength raised once after the Developer could not see it. |
| Window and lantern flicker | Done | Agent: halos dip to ~0.5 and recover, frozen when paused, steady under reduced motion, tapping still lights the window. Developer: "looks good". |
| Fog (five soft drifting patches, in the fog layer) | Done | Agent: patches move, frozen when paused, still under reduced motion, taps pass through to hotspots. Developer: "I like it"; fog stops at the house base as intended. First version read as three full-width stripes, so bands were shortened and staggered. |
| Bats (three, in the particle layer) | Done | Agent: wings flap, frozen when paused, offscreen under reduced motion, on screen ~76% of a 110 s run with gaps of 2.3-3.3 s. Developer: "looks good". |
| Leaves (twelve, built from a fixed table in `app.js`) | Done | Agent: all falling at ~30-45 scene units/s, frozen when paused, none visible under reduced motion, taps still reach pumpkins. Developer on iPhone: "Everything looks good." |

**Developer observations and changes during checkpoint 3:**
| What the Developer saw | Interpretation | Change | How verified |
|---|---|---|---|
| Stars: "I cannot see that change" | Two causes: the twinkle was subtle (100% to 25% opacity on ~2 px stars), and the browser was showing a stale copy | Dimming deepened to 10% and stars also change size; Developer opened the file directly and saw it | Zoomed captures 1.5 s apart; Developer saw the effect |
| Bats: saw one bat, then none | Bats flew a range far wider than the phone, so most of each pass was offscreen (about 13 s empty after the first) | Range now follows the visible screen edges (set in `app.js`); shorter cycles | 75 s sampled run: on screen 85% of the time |
| Bat wings "look funny" | Flap squashed and flipped the wing shape, so it collapsed to a thin sliver midway | Wings now rotate up and down from the shoulder | Frozen frames at three flap phases |
| Bat gaps "inconsistent", longer over time | Three different cycle lengths (28/37/49 s) drifted apart | One shared 36 s cycle, evenly staggered | 110 s run: nine gaps, all 2.3-3.3 s |
| iPhone: "three bats on the left", not moving | New `index.html` paired with a cached older `style.css` (GitHub Pages caches 10 min), so bats had no styles or motion | `?v=` version stamps on `style.css` and `app.js`, bumped before each push (rule in `AGENTS.md`) | Reproduced in WebKit with the old stylesheet; then confirmed bats and leaves move on the live URL in WebKit; Developer confirmed on iPhone |

**Testing note:** since the cache bug, Agent checks also run in Playwright WebKit (iPhone's engine) in the scratchpad, not only in Chrome.

### Checkpoint 4: ambient audio (built and phone-checked, 2026-10-19; awaiting Developer tick)

Sounds (CC0, recorded in `research.md`): IgnasD wind gusts, chained with overlap and random pitch/loudness into a continuous bed; Breviceps owl hoot every 22-44 s. Code: `audio.js`; checks A1-A7 in `spec.md`.

**Verified by Agent:** no audio context before Enter; after Enter all four files load and a 40 s Chrome run played 11 gusts and 1 hoot with continuous level (silent only at the first instant); Pause suspends the audio clock and every sound, Play resumes; blocked files show the "Sound unavailable" note while the scene, taps and Pause still work; reduced motion does not silence audio; the live site serves the files with correct types and plays. **Not testable by the Agent:** real iPhone sound (the Windows WebKit build used for testing has no Web Audio).

**Developer observations and changes:**
| What the Developer saw | Interpretation | Change | How verified |
|---|---|---|---|
| Sound plays on the phone, not on the computer; "Sound unavailable" | Page opened straight from the folder (`file://`); browsers block loading the sound files that way. Reproduced by the Agent | `serve.bat` one-click local server; `AGENTS.md` says not to open `index.html` directly; the console now names the failing file, page address and prints a `file://` hint | Agent: serve.bat serves the audio (HTTP 200); Developer: "It works" on the computer |
| On the phone, music stops when leaving the page and does not come back | iOS interrupts web audio when the page leaves the screen; nothing told the app or restarted it | Spec F6 built: hiding the page or locking the phone auto-pauses (button reads Play, stays paused); the Play tap restarts audio | Agent: tab-switch test, stays paused until Play, then audio runs. Developer on phone: "works now" |
| (Agent finding) first sound request in a fresh test browser stalled, which silenced everything because startup waited for all four files | Fragile startup | Each file loads independently with a 20 s timeout; sounds start as their own file is ready; the note shows only if no wind file loads | Agent: tests above |

**Not yet confirmed by the Developer:** how the wind sounds (continuous and natural versus gappy or pulsing), whether the owl was heard, and whether levels are right. Levels are `MASTER_GAIN`, `WIND_GAIN`, `OWL_GAIN` at the top of `audio.js`.

### Checkpoint 5: Story 1, pumpkins (in progress, started 2026-10-19)

Spec: "Story 1 build spec" in `spec.md` (Developer chose all four pumpkins smallest to biggest, synthesized sounds, no ghost voice). Stages: (1) sequence alone, (2) triggers and progress feedback, (3) input lock and return, (4) hints, then the Phase 1 playtest.

**Stage 1, sequence alone (built, awaiting Developer review):** `hollowStory.play('pumpkins')` in the console, or open the page with `#play-pumpkins` (temporary, removed at stage 2). Art in the story overlay layer; timeline in `style.css`; sounds in `cues.js`; controller in `story.js`.
- Agent verified (Chrome, real time): runs 8.06-8.08 s; replayed three times with the patch restored exactly each time; scene taps ignored while it plays and a second `play()` refused; Pause freezes pictures and sound together and Play finishes the remaining 4.81 s; reduced motion removes all movement (no shake, flying or rising) and still plays with fades; sound peaks at the pop; no errors. WebKit renders the clipped ghost and flying lid correctly (no sound test possible there).
- Bugs found and fixed while testing: the ghost's hat showed above the pumpkin before the ghost rose (hidden position too shallow); the smoke looked like flat discs (now soft gradient); Pause did not stop the story's pictures, because the story's `animation:` shorthand outranked the pause rule (pause rule is now `!important`).
- Developer to judge by eye and ear: look of the faces, ghost and smoke; whether 8 s feels right; the sounds (levels and character are provisional, tunable in `cues.js`).

**Stage 1 review (Developer):** "It's good" with one change: the faces did not shake with the pumpkins, and it was obvious. Cause: faces were a separate layer with their own position transform. Fix: faces now share the pumpkins' shake (same keyframes and pivot); Agent measured each face within 0.06-0.14 px of its pumpkin's center mid-shake. Developer then confirmed it works.

**Stage 2, triggers and progress feedback (built, awaiting Developer review):** rules are in `spec.md` (Story 1 build spec). The temporary `#play-pumpkins` shortcut is gone.
- Agent verified (Chrome, real clicks and key presses, with the sound cues spied on): taps 1-4 in order give `tap(0)`..`tap(3)` and lights `1000`, `1100`, `1110`, then the story starts and the lights clear; the story lasted about 8.1 s and the patch was restored. A wrong pumpkin (1 then 3) gives a `nope` cue and wobble, resets, and the wobble class clears itself; the same pumpkin twice also resets. Tombstone and window taps give `tick`, flash, and leave the pumpkin progress alone. A half-finished sequence reset between 7 s and 8.8 s; with Pause held 10 s the progress stayed and taps were ignored, and the count resumed after Play. The keyboard (Tab, Enter and Space) completes the sequence and starts the story. Under reduced motion the wrong-tap wobble becomes a fade. No errors.
- Also changed: the tap glow on every object is now soft-edged instead of a flat disc.
- Developer to judge by eye and ear: the four tones and the "nope" sound, the lingering lights, and whether 8 s before reset feels right.

**Stage 2 review (Developer):** "It's good." Found: pressing Enter after mouse-clicking a pumpkin counted as a wrong tap (the clicked pumpkin kept keyboard focus, so Enter re-tapped it, and the same pumpkin twice is wrong); holding Enter would repeat it. Fix: a mouse or touch tap releases focus, and key auto-repeat is ignored (Agent verified with real clicks and key events: Enter after a click does nothing; Enter plus two auto-repeats counts once; keyboard Tab and Enter or Space still completes the sequence). Developer clarified that Enter after all four pumpkins doing nothing until the story ends is the expected behavior.

**Stage 3, input lock and return (built, awaiting Developer review):** a note under the buttons says "A story is playing…" while taps are ignored, then "Your turn: keep exploring" for about 1.6 s and fades. Agent verified: note appears with the story, stays through Pause, taps work the moment the story ends, the closing fade freezes under Pause and completes after Play (normal and reduced motion), a replay takes over cleanly, text is 16 px, no errors.

**Stage 4, hints (built, awaiting Developer review):** the Developer picked the wording (table in `spec.md`) and chose pumpkin-only hints for now ("Right now, just this story"), with the all-stories wording stored for later. Code: `hints.js`.
- Agent verified (Chrome): in a real-time run the hints appeared at 14.9, 29.7 and 44.8 s and level 3 was still showing at 52 s (no level 4, no cycling). With shortened timers: a tap on empty sky, on a wrong pumpkin, and a keyboard Enter on a window each hid the hint and restarted the clock at level 1; Pause held the idle clock at 2.8 s for 8 s and it continued after Play; a story hid the hint, the clock restarted at 0 after it and level 1 came back 2.4 s later (timers shortened); under reduced motion the hint has no animation, otherwise it fades in; all six lines fit on one 16 px line at 360 px; no errors.
- Developer to judge: whether the hints actually lead a first-time player to the pumpkins without giving it away (this is what the Phase 1 playtest is for), and the 15/30/45 s timing.

**Phase 1 cleanup and verification (2026-10-19):** behavior-preserving cleanup (leaves and effect ranges moved to `ambient.js`, stale comments and two unused CSS variables fixed; the full test suite re-run with unchanged results), then a requirement-by-requirement audit of the live site against `brief.md` and `spec.md`. Results and open items: `verification.md`.

**Saved for Phase 2 (2026-10-19):** the test scripts used throughout are now in `tests/` with a README, a shared harness and a runner (`python tests/run_all.py --quick`), and the full build-session transcript is in `transcripts/build-2026-10-19_194148.md`.

**Peer playtests:** protocol, script, observation table and note template are in `playtest.md` (drafted by the Agent 2026-10-19; the Developer runs the sessions). Purpose (Developer): find every issue in story 1, fix story 1, and apply the lessons to stories 2 and 3; tag each finding as "story 1 only" or "applies to every story". Record each tester's session in this section. `playtest.md` must be updated once stories 2 and 3 exist.

### Phase 1 peer-playtest summary (Developer report, 2026-10-25)

**Observed / said:** Every tester eventually completed the pumpkin sequence. Completion time varied, but nobody made a consequential wrong-order error. Testers saw only the first hint; the Developer did not infer that the hint caused completion, because they recognized that the pumpkins were the relevant interactive set. The house windows and tombstones responded only with the prototype feedback, which confused testers because they appeared to invite fuller interactions. No problems were reported with the pumpkin story, sound, Pause, or other intended behavior. Testers used the same or similar phone types.

**Interpretation and priority:** Story 1 is sufficiently discoverable for this sample. The inactive house and graveyard are a whole-scene expectation gap, not a pumpkin-story defect; completing the other two promised stories takes priority over changing the pumpkin trigger or hints. Device variety and individual session details were not recorded, so these observations do not establish behavior across phone/browser types.

**Revision chosen:** Build the graveyard story next. Its approved trigger is a fixed left -> right -> center tombstone order, not a timing/rhythm puzzle, so ordinary variation in tap speed cannot cause a false failure.

### Checkpoint 6: Story 2, graveyard (built and Developer-reviewed 2026-10-25; automated browser checks pass; physical-phone review pending)

The Developer verified the left -> right -> center trigger, wrong-tap reset, story playback, Pause/Play and reduced-motion version on the local build. The story's ground rumble, yawning stones, dancing ghosts, mist, reset and synthesized sound are approved as the current direction. A review finding showed that the cross on the center tombstone did not move with a wrong-tap shake; the shake now belongs to the complete tombstone hotspot, so its cross stays attached, and the Developer rechecked it. The correct-tap notes are intentionally G -> C -> B-flat: an upward movement during the left/right part of the path, settling lower at the center; the Developer accepted this for now and may revisit it later.

**Shared story-pause repair (2026-10-25):** Developer testing found that the House shudder and the Graveyard stones kept animating during Pause, even though the overlay ghosts froze. Cause: their new animations lived outside the existing `.sfx` pause scope. Tombstone hotspots and the House building now carry that shared scope, so their story and wrong-tap animations freeze with every other story element. The far hill was also in the House animation group, making it move with the building; the building is now a separate animated group and the hill stays still. The Developer rechecked the repair successfully in the local preview (see Developer recheck below).

**Hint revision (2026-10-25):** Once all stories existed, the third all-stories hint still said "rhythm," although the Developer chose fixed orders for both the graveyard and house. It now reads "Size and position matter… patterns wake them.": direct enough to point toward the relevant attributes, but it does not reveal any exact sequence.

**Developer recheck (2026-10-25):** The House sequence, Graveyard sequence, shared Pause repair, all-stories hint wording, and the restored "patterns wake them" ending all work as intended in the local preview.

**Automated verification (Agent, 2026-10-25):** `python tests/run_all.py --quick` completed all 13 checks without a crash. The graveyard and house checks measured story runs of about 8.03 s and 8.01 s, confirmed the correct trigger orders and progress lights, wrong-tap resets, replay, reduced-motion variants, and zero browser exceptions. Both animation clocks stayed frozen during Pause. The first focused run sampled transforms too soon after toggling Pause and falsely reported movement; the checks now wait for the browser to commit the paused frame and compare animation clock time. Physical-phone review is recorded below.

**Physical-phone review (Developer, 2026-10-25):** The deployed three-story build was opened on the phone; Developer report: "Everything works as intended." Checkpoints 6 and 7 are complete.

**Open issue (carried over):** the left-edge sliver on windows and lantern (see above) was accepted and not fixed. It was not specifically called out in the phone review; revisit only if it becomes noticeable or testers mention it.

**Decision on flicker:** the flicker moves only on a soft halo behind each light; the window and lantern shapes stay solid. Reason: animating the hard-edged shapes (first `opacity`, then `fill-opacity`) coincided with a thin yellow sliver on the left of each light on the Developer's Edge display. The sliver remained with all animation stopped and with the halos hidden, so the flicker only made it more visible.

**Open issue (accepted by the Developer, 2026-10-19):** a thin yellow sliver on the left edge of the windows and lantern, in Edge on the Developer's display, cleared by clicking a window. Not reproducible by the Agent in headless Chrome at 1x to 1.75x scale or in a real Edge window at 125% (zoomed captures), so the cause is unknown. Developer judged it not very noticeable and chose to move on. Revisit if playtesters mention it, starting with a native-size screenshot of the window.

Keep implementation progress and verification here. Update `research.md` when evidence changes a decision and `spec.md` when intended behavior changes; link to those updates rather than duplicating them. Record consequential changes, not every small adjustment.

## Saving transcripts

When directed, save the complete conversation as `transcripts/plan-YYYY-MM-DD_HHMMSS.md` or `transcripts/build-YYYY-MM-DD_HHMMSS.md`, label messages `Developer` and `Agent`, and confirm the path.
