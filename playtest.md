# Phase 1 Playtest Guide

> EDITING DIRECTIVE: DEVELOPER AND AGENT EDIT THIS FILE COLLABORATIVELY. THE DEVELOPER MUST REVIEW AND APPROVE ITS CONTENT.

Purpose: run the same neutral session with each peer, observe first, ask afterwards, and record what happened without coaching. Results go into `plan.md` ("Evidence and revisions"); this file is the protocol and the note template.

## 1. What this playtest should find out

The Phase 1 prototype is the ambient scene plus **one** story (the pumpkins). The questions:

1. **Discovery.** Can someone who knows nothing find and complete the pumpkin story without help? How long does it take, and what do they try first?
2. **Hints.** Do the three idle hints get noticed, and do they move people toward the pumpkins without giving it away?
3. **Feedback.** Do the tap tones and lingering lights show progress? Is the "nope" understood? Is the "A story is playing" / "Your turn" note understood?
4. **Story.** Is it enjoyable and the right length? Is anything confusing, scary beyond "playful", or too slow?
5. **Atmosphere and controls.** Do the visuals and sound feel spooky and playful? Do they find and understand Play/Pause? Are the tap targets comfortable on their phone?
6. **Promotion.** Does it make them curious about a Halloween visit to the park? (The client's goal.)

Things that exist but are **not** built yet, so do not count them as findings: tombstones and windows only flash and tick (no stories), and there is no "ghosts found" counter.

## 2. Before each session (about 5 minutes)

- [ ] Use the live address, not a local copy: https://thearkx60.github.io/ai-exploration-unit-4/. On a spare phone or your own, open it in a **private tab**, press Enter, and check that the scene, sound and a full pumpkin run work. Close it afterwards.
- [ ] Ask the tester to use **their own phone** (so you see real sizes, browsers and habits). Note the phone model and browser, not their name.
- [ ] Phone check, done for them without hints about the content: volume up, **iPhone silent switch off** (it mutes web audio), screen brightness up, auto-rotate fine.
- [ ] Give each tester an ID (P1, P2, P3...). Do not write names.
- [ ] Ask permission to take notes. Do not record audio or video unless they clearly agree.
- [ ] Clear the page on their phone before they start: have them open the address in a private tab so it loads fresh (an old cached copy has fooled us before).

## 3. What you say at the start

Read it as written, in a relaxed voice:

> "This is an early version of a Halloween scene for a phone. Explore it however you like. There are no right or wrong ways to use it, and you can't break anything. If you can, say out loud what you're looking at and what you're thinking. I won't be able to answer questions while you play, because I want to see what it's like without help. I'll ask you some questions afterwards. Tell me when you're done, or when you'd like to stop."

Then give them the address and let them go. **Do not say** anything about pumpkins, tapping order, hints, stories, or sound.

## 4. While they play (observe, do not help)

- Sit beside or just behind them so you can see the screen. Stay quiet. If they ask a question, say "What would you do if I weren't here?" or "I'll answer that afterwards."
- Stop the session after **10 minutes**, or sooner if they ask to stop or are clearly frustrated. If they are stuck for **3 minutes** with no progress, you may note "stuck 3 min" and ask if they'd like to carry on or move to the questions.
- Fill in the observation table below as you go. A short phrase is enough; times are rough (use the clock).

| Moment | Time | What happened (what they did or said, not what you think) |
|---|---|---|
| Pressed Enter on the start screen | | |
| First tap on the scene, and on what | | |
| What they explored or tried first (objects, order, repeats) | | |
| First hint appeared (about 15 s idle): did they notice it? Read it aloud? React? | | |
| Second and third hints: noticed? What did they do next? | | |
| Pumpkin attempts: orders tried, wrong taps ("nope"), did the tone/light progress show? | | |
| Story triggered (time since start) | | |
| Reaction to the story (words, face, did they watch to the end?) | | |
| Tried to tap during the story? Reaction to "A story is playing" and "Your turn" | | |
| Replayed the story? Tried other objects (tombstones, windows)? | | |
| Found Play/Pause? Used it? Credits? | | |
| Sound: heard it? (note without asking) Any complaint | | |
| Confusion, mis-taps, bugs, anything surprising (device, browser) | | |

## 5. After they stop: questions

Ask in this order. Start open, wait through silences, and do not explain the design until the end.

1. "What was that like? What did you notice?"
2. "What did you try, and why?"
3. "How did you figure out what to do?" (If they never found the story: "What did you think was supposed to happen?")
4. "Was there anything that confused you or didn't work the way you expected?"
5. "Did you notice any text on the screen? What did it say, and did it help?"
6. "Tell me about the sounds. Anything too loud, too quiet, or odd?"
7. "How did the story feel: too short, too long, or about right? Was anything too scary or not scary enough?"
8. "Was there a moment you weren't sure whether it was your turn to tap?"
9. "Did you notice the Pause button? What did you think it did?"
10. "Did the scene make you curious about visiting a Halloween event at a park? Why or why not?"
11. "What would you change first?"
12. (Optional, last) "On a scale of 1 to 5, how fun was it?" and "Is there anything you'd tell a friend about it?"

Only after question 12, if they never found the story, you may show them how it works, and ask what they would have needed to find it.

## 6. Recording a session

Keep **what they did or said** separate from **your interpretation**. No names. Copy one block per tester into `plan.md` under "Evidence and revisions", then add the summary after all sessions.

```
### P1 (phone and browser, e.g. iPhone 13 / Safari), date
Duration: __ min. Story completed: yes / no, at __ min.
Observed / said:
- ...
Hints: noticed at __, effect: ...
Wrong taps before success: __
Sound: ...
Their answers to the questions (short quotes are best):
- Q1 ...
Interpretation (mine, kept separate): ...
Bugs or oddities: ...
```

## 7. After all sessions

1. Aim for **3 to 5 testers**. Stop sooner only if the same problems repeat in every session.
2. List each problem once, with how many testers hit it. Mark each as: blocked the story / slowed them / annoyed them / cosmetic.
3. Choose revision priorities in this order: (a) anything that stopped someone from completing the story or using the controls, (b) anything several testers misunderstood, (c) bugs or comfort problems on phones, (d) taste items.
4. Record each consequential change in `plan.md`: what you saw, what you changed, how you checked it. Update `spec.md` if the intended behavior changes and `research.md` if a decision changes.
5. Known open issue: a thin yellow sliver on the left edge of the lit windows on the Developer's computer. Do **not** ask about it; note it only if a tester volunteers it.

## 8. Ethics reminders

Keep the tone playful, never press someone to continue, thank them, and keep notes anonymous. If a tester finds anything upsetting, stop and ask whether they want to continue.
