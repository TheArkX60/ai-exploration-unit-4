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
- [ ] **3. Ambient visuals.** Fog, bats, flicker, leaves, stars, one at a time. Verify: each visible, loops cleanly, honors reduced motion, Play/Pause freezes them.
- [ ] **4. Ambient audio.** Source and verify CC0 wind and owl (record in `research.md`), loop, gated by Enter, paused by Play/Pause.
- [ ] **5. Story 1 (pumpkins)** as a standalone sequence first, then triggers, progress feedback, hints, input lock. Then Phase 1 playtest.

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

**Open issue (carried over):** the left-edge sliver on windows and lantern (see above) was accepted and not fixed. Not checked on the phone result above beyond the Developer's "everything looks good"; ask again if it comes up.

**Decision on flicker:** the flicker moves only on a soft halo behind each light; the window and lantern shapes stay solid. Reason: animating the hard-edged shapes (first `opacity`, then `fill-opacity`) coincided with a thin yellow sliver on the left of each light on the Developer's Edge display. The sliver remained with all animation stopped and with the halos hidden, so the flicker only made it more visible.

**Open issue (accepted by the Developer, 2026-10-19):** a thin yellow sliver on the left edge of the windows and lantern, in Edge on the Developer's display, cleared by clicking a window. Not reproducible by the Agent in headless Chrome at 1x to 1.75x scale or in a real Edge window at 125% (zoomed captures), so the cause is unknown. Developer judged it not very noticeable and chose to move on. Revisit if playtesters mention it, starting with a native-size screenshot of the window.

Keep implementation progress and verification here. Update `research.md` when evidence changes a decision and `spec.md` when intended behavior changes; link to those updates rather than duplicating them. Record consequential changes, not every small adjustment.

## Saving transcripts

When directed, save the complete conversation as `transcripts/plan-YYYY-MM-DD_HHMMSS.md` or `transcripts/build-YYYY-MM-DD_HHMMSS.md`, label messages `Developer` and `Agent`, and confirm the path.
