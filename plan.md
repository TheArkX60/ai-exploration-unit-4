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

Status: DRAFT for Developer approval. Main risk across these: layout or layer structure that fails on real phones, found late. So deploy and check on a phone early.

- [ ] **1. Static shell.** Start screen, state variable, reduced-motion read, static SVG scene in layers, placeholder hotspots, Play/Pause stub, credits stub. Verify: acceptance checks 1-10 in `spec.md`, screenshots at three phone sizes.
- [ ] **2. Early deploy.** Push to GitHub Pages and open the HTTPS URL on a physical phone. Verify: scene fits, Enter works, tap targets usable. Catches viewport/address-bar issues before effects are added.
- [ ] **3. Ambient visuals.** Fog, bats, flicker, leaves, stars, one at a time. Verify: each visible, loops cleanly, honors reduced motion, Play/Pause freezes them.
- [ ] **4. Ambient audio.** Source and verify CC0 wind and owl (record in `research.md`), loop, gated by Enter, paused by Play/Pause.
- [ ] **5. Story 1 (pumpkins)** as a standalone sequence first, then triggers, progress feedback, hints, input lock. Then Phase 1 playtest.

Test each result before continuing, including related behavior that already works. Update priorities as evidence emerges and preserve meaningful working checkpoints in git. Before delivery, verify the deployed app against the brief and specification.

## Evidence and revisions

Record non-identifying playtest observations, separating what Users did or said from your interpretation. Use the findings to choose revision priorities and record what changed and how you verified the improvement.

Keep implementation progress and verification here. Update `research.md` when evidence changes a decision and `spec.md` when intended behavior changes; link to those updates rather than duplicating them. Record consequential changes, not every small adjustment.

## Saving transcripts

When directed, save the complete conversation as `transcripts/plan-YYYY-MM-DD_HHMMSS.md` or `transcripts/build-YYYY-MM-DD_HHMMSS.md`, label messages `Developer` and `Agent`, and confirm the path.
