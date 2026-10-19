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
- [ ] **2. Early deploy.** Push to GitHub Pages and open the HTTPS URL on a physical phone. Verify: scene fits, Enter works, tap targets usable. Catches viewport/address-bar issues before effects are added.
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

Keep implementation progress and verification here. Update `research.md` when evidence changes a decision and `spec.md` when intended behavior changes; link to those updates rather than duplicating them. Record consequential changes, not every small adjustment.

## Saving transcripts

When directed, save the complete conversation as `transcripts/plan-YYYY-MM-DD_HHMMSS.md` or `transcripts/build-YYYY-MM-DD_HHMMSS.md`, label messages `Developer` and `Agent`, and confirm the path.
