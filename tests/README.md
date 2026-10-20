# Tests

Automated browser checks for Hollow Hill. They drive a real (headless) Chrome with real mouse clicks, key presses and touch events, then **print what they measured**: element sizes, animation states, audio clock and level, which sound cues fired. They do not assert pass or fail, so read each result against the "Expected" column below. They were used to verify everything recorded in `plan.md` and `verification.md`, and are kept so stories 2 and 3 can be checked the same way and so story 1 can be re-checked after the playtest fixes.

## Setup (once)

1. Python 3 (already needed for `serve.bat`).
2. `python -m pip install websocket-client`
3. Google Chrome or Microsoft Edge installed. The harness looks in the usual places; otherwise set the `HOLLOW_CHROME` environment variable to the full path of `chrome.exe` or `msedge.exe`.

## Running

From the project folder:

```
python tests/test_story.py          # one test
python tests/run_all.py --quick     # the fast set (about 5 minutes)
python tests/run_all.py             # everything except the live-site audit (about 15 minutes)
python tests/run_all.py --live      # also the live-site audit (needs the deployed site to be current)
```

Notes:
- Each test starts its own temporary copy of the project on port 8777 and Chrome on port 9333, and cleans up after itself. It does **not** use your project folder directly, and it does not clash with `serve.bat` (port 8765). Close other Chrome windows that were started with remote debugging, if any.
- Screenshots and other files go to `tests/output/` (not committed).
- Headless Chrome cannot play sound to a speaker, but the Web Audio clock and level are real, which is what the audio tests read. Real sound, and real iPhone behavior, are checked by hand on a phone.
- Tests that need a real user gesture (sound only starts after one) use real mouse clicks, not scripted `.click()`.
- When you change an animation or a trigger rule, update the matching test as well as the code. Some tests contain the rules themselves (the pumpkin order, the 8 s timeout, the 15/30/45 s hint times).

## What each test checks, and what to expect

| Test | Checks | Expected | Time |
|---|---|---|---|
| `test_shell.py` | Start screen hidden scene, Enter, layout at 360x640, 390x844, 430x932 and desktop, Tab order, light-up, Play/Pause, credits, reduced-motion read | No scrolling; hotspots 48 px or more; buttons 44 px; zero console errors; Tab visits windows, tombstones, pumpkins, Credits, Pause; reduced-motion attribute `true` when emulated | 1 min |
| `test_triggers.py` | Pumpkin sequence | Cues `tap(0)` to `tap(3)` then `story(pumpkins)`; lights `1000`, `1100`, `1110`, then cleared; wrong pumpkin gives `nope` and resets; other objects give `tick` and do not disturb progress; timeout between 7 and 8.8 s; Pause freezes the timeout; keyboard completes it; reduced motion uses `nope-fade` | 2 min |
| `test_story.py` | The pumpkin story | About 8.05 s, three replays with the look restored; taps ignored and second start refused; Pause freezes pictures and sound, resumes the remaining 4.8 s; reduced motion has no movement animations | 2 min |
| `test_story_frames.py` | Look of the story | Screenshots `tests/output/story-t*.png` for you to look at | 30 s |
| `test_story_note.py`, `test_story_note_pause.py` | "A story is playing…" / "Your turn…" note | Shown during the story, switches at the end, fades by itself, freezes on Pause, 16 px text | 1 min |
| `test_enter_focus.py` | Stray Enter and key repeat | Enter after a mouse click does nothing; one tap per held key; keyboard still completes the sequence | 1 min |
| `test_hints.py` | Hints | Level 1 at about 15 s, level 2 at about 30 s, level 3 at about 45 s and stays; tap or key resets; Pause freezes; story hides and restarts; all lines fit one line | 2.5 min |
| `test_autopause.py` | Auto-pause | Switching tabs pauses; stays paused on return; Play resumes | 30 s |
| `test_audio.py` | Ambient sound | Nothing before Enter; gusts and an owl after; continuous level; Pause suspends and freezes the clock; blocked files show "Sound unavailable" while taps and Pause still work | 1.5 min |
| `test_flicker.py`, `test_fog.py`, `test_leaves.py` | Effects | Running, frozen under Pause, none or still under reduced motion; leaves 10 to 12 visible; taps pass through fog | 1 min each |
| `test_bats.py`, `test_bat_gaps.py` | Bats | Flight range follows the screen edges; a bat on screen about 76% of the time; gaps of about 2 to 3.5 s | 2 min each |
| `test_face_shake.py` | Faces shake with pumpkins | Face and pumpkin centers within about 0.15 px mid-shake; no movement under reduced motion | 20 s |
| `test_audit_live.py` | Requirements audit of the **live** site | See `verification.md` for the expected values (sizes, contrast, credits, effects running, Pause, touch story 3 times, blocked audio, hidden tab, reduced motion) | 2 min |

Known quirk: right after a long pause, headless Chrome can take a few seconds to restart audio, so a check made too soon after Play may still read "suspended". Phones are faster.

## Not covered here

- Real sound quality and real iPhone behavior (checked by hand).
- iPhone Safari's engine: a WebKit check can be run with Playwright (`pip install playwright`, `playwright install webkit`); the Windows WebKit build has no Web Audio, so it only checks pictures and layout.
- Stories 2 and 3: add tests alongside the existing ones as they are built, following `test_triggers.py` and `test_story.py`.
