# Research

> EDITING DIRECTIVE: DEVELOPER AND AGENT EDIT THIS FILE COLLABORATIVELY. THE DEVELOPER MUST REVIEW AND APPROVE ITS CONTENT.

Purpose: Keep the evidence and creative decisions that currently guide the build.

## Working agreement

Developer: Run the starter first. Direct the inquiry, judge sources and options, make consequential decisions, and keep this file current.

Agent: Read `AGENTS.md`, `brief.md`, and this file, then inspect the project. Help compare possibilities, test assumptions quickly, and verify external sources without delaying the prototype for exhaustive research.

Start a fresh chat with:

`Read brief.md and research.md, inspect the running project, and help me develop the scene and three spooky stories.`

## Inquiry and decisions

Record only what informs the next build decisions:

- creative alternatives for the scene, stories, and audiovisual direction, with reasons for your choices
- useful sources and references, what they support, and important limitations
- experiments that resolve uncertainty, the results, and consequential trade-offs

Investigate unfamiliar techniques or asset sources as needed. Verify usage terms and keep source links and required credits here. Distinguish evidence from assumptions; the Agent's recommendation alone is not evidence.

### Scene and story direction (APPROVED by Developer 2026-10-17)

**Chosen scene: "Hollow Hill"** — a crooked haunted house on a hill under a big moon.
- Alternatives considered: abandoned carnival at dusk (ties to theme-park client, more assets to build); moonlit witch cottage in a swamp. Chose the haunted house for its clear focal point and simple, layerable silhouette shapes.
- Visual style: flat layered silhouettes with a glowing palette, drawn in code (SVG/CSS). No AI-generated images unless needed. Chosen for ease of building and layering.
- Focal point: the house, with glowing windows and the moon behind it.
- Environmental features: haunted house, graveyard (left), pumpkin patch (foreground), gnarled tree with hanging lantern.
- Ambient effects: drifting fog, bats crossing the moon, flickering windows and jack-o-lanterns, falling leaves, twinkling stars.
- Ambient audio: wind loop with occasional owl hoots (sources to be found and verified; see Assets).

**Recurring character:** a friendly sheet ghost (simple original design) who lives in the house and wants to throw a party. The ghost links the stories; the stories do not depend on each other.

**Three stories** (each 5–10 s, replayable, other input disabled while playing):
1. Pumpkin Patch — tap pumpkins smallest to biggest, each tap with a unique tone and light-up. Pumpkins grin and glow, the biggest pops open, the ghost peeks out, puff of smoke, pumpkins revert.
2. Graveyard — tap three tombstones in a rhythm (chosen over press-and-hold for accessibility). Ground rumbles, tombstones yawn, three little ghosts do a wobbly dance, then sink back down.
3. The House — tap the windows in the order they flicker. The house shudders, windows blink like eyes, the door swings open on a tiny ghost party, lights snap off then on.

**Hints:** after about 15, 30 and 45 s of idle time, text hints go from vague to more specific without stating the trigger.

**Decision: keep stories independent.** Story content never depends on whether another story was seen. This keeps each story simpler to build, test and replay. Trade-off: no payoff for finding all three.

**Possible later extra (not in first build):** a small "ghosts found: n/3" counter. It would show progress without changing what any story plays, so it adds little coupling. Revisit after the three stories work.

### Ambient audio candidates (found 2026-10-19; NOT approved, nothing is used until the Developer approves)

Licenses were read on each sound's own page (not a search snippet). Measurements are from decoding the file in a browser (levels in dB relative to full scale; the Agent cannot judge how any of them sounds, so listening is the Developer's call). CC0 requires no credit; the Credits panel will still name sources as a courtesy.

**Wind**
| Candidate | Source and license | Measured | Notes |
|---|---|---|---|
| "wind whoosh loop" by SketchMan3 | [OpenGameArt](https://opengameart.org/content/wind-whoosh-loop), CC0, 252 KB OGG, uploaded 2019-07-16 | 6.0 s, stereo, very steady (about 1 dB variation), start and end identical so the loop has no jump, quiet (about -30 dB) | Page says it is a looped section of wind from another recording, EQ'd to bring out the highs, so it may sound bright or hissy. 6 s is short and may sound repetitive. |
| "Wind" pack by IgnasD (Wind, Wind2, Wind3) | [OpenGameArt](https://opengameart.org/content/wind), CC0, 264 KB zip with OGG and M4A of each, uploaded 2015-03-04 | Wind and Wind2: about 6.7 s mono; swell up and fade (one gust each); Wind3: 1.7 s | Not loops: single gusts. Idea: play them at irregular intervals over a steady bed. M4A versions give Safari-safe files. |
| "Ghost Town Night Ambient" by szegvari | [Freesound](https://freesound.org/people/szegvari/sounds/557193/), CC0 | 2 min 30 s, stereo, fades in from near silence and out to near silence, loudness varies by about 12 dB | A full soundscape, not plain wind; contents not checked by ear. Larger file (3.5 MB preview). |
| "Little dark house soundscape" by szegvari | [Freesound](https://freesound.org/people/szegvari/sounds/557191/), CC0 | 2 min 29 s, large loudness swings (events) | Probably too eventful for a steady bed. |
| "Wind.wav" by chrscrwfrd18 | [Freesound](https://freesound.org/people/chrscrwfrd18/sounds/156992/), CC0 | 7+ MB even as a compressed preview (several minutes) | Likely too large for a phone bed; not examined further. |

**Owl**
| Candidate | Source and license | Measured | Notes |
|---|---|---|---|
| "Owl Hoot" by Breviceps | [Freesound](https://freesound.org/people/Breviceps/sounds/465697/), CC0 (uploader: "My sounds are Public Domain (CC0)"), WAV, uploaded 2019-04-05 | 4.4 s, stereo, very quiet (peak about -28 dB, so it needs about +20 dB of gain, which also raises noise) | Tags tawny, hooting, night. Recorded with a phone. |
| "Owl Slow Hoot" by dandman3039 | [Freesound](https://freesound.org/people/dandman3039/sounds/528623/), CC0, M4A, uploaded 2020-07-21 | 33.7 s forest recording (not measured) | "Large owl hooting high up in a tree in Vermont." Longer; would need trimming to one hoot. |
| "Owl-3" by SyntaxSeed | [Freesound](https://freesound.org/people/SyntaxSeed/sounds/871239/), CC0, WAV | 38.9 s, mono, 22 kHz | Distant hoots with crickets and neighbourhood noise in the background. |

**Not usable (checked):** OpenGameArt "Barn Owl Screech" is CC BY-SA 4.0 (needs credit and share-alike); Xeno-canto tawny owl is CC BY-NC-SA 4.0 (non-commercial, not allowed); the itch.io "Owl hooting sound effect" page states no license.

**Agent's suggestion (not evidence):** steady bed from "wind whoosh loop", gusts from IgnasD's Wind and Wind2 played at irregular intervals, owl from Breviceps. If the loop sounds too bright, too repetitive or hissy, fall back to wind synthesized with Web Audio (filtered noise), which `spec.md` already allows.

### Assets
**Approved by the Developer 2026-10-19 (ambient audio), in `assets/audio/`:**
| File in the project | Source | License | Credit |
|---|---|---|---|
| `wind-gust-1.m4a`, `wind-gust-2.m4a`, `wind-gust-3.m4a` | "Wind" pack (Wind, Wind2, Wind3, M4A versions) by IgnasD, [OpenGameArt](https://opengameart.org/content/wind), uploaded 2015-03-04 | CC0 (license field read on the page) | Not required; named in the Credits panel anyway |
| `owl-hoot.mp3` | "Owl Hoot" by Breviceps, [Freesound](https://freesound.org/people/Breviceps/sounds/465697/), uploaded 2019-04-05 | CC0 (license read on the page; uploader: "My sounds are Public Domain (CC0)") | Not required; named in the Credits panel anyway |

Notes: (1) the owl file is Freesound's public 128 kbps MP3 preview of the sound, because the full WAV download needs a login; the sound and its CC0 license are the same, only the encoding differs, and a WAV could replace it later. (2) The wind files are single gusts, not loops, so `audio.js` chains them with overlap, random pitch and loudness to make a continuous bed. (3) The Developer chose these over the steady 6 s "wind whoosh loop" (SketchMan3) and the longer soundscapes.

**Still unsourced:**
- Story sound effects (tones, rumble, puff, creak, party sounds): not yet sourced.
- For each: record source link, license (CC0 or public domain only) and any required credit here before use.

## Revisions

Update decisions when new evidence changes the direction, linking to playtest observations in `plan.md` rather than copying them. Keep chosen behavior and asset requirements in `spec.md`. The Developer confirms when the inquiry is sufficient to continue building; exhaustive research is not a prerequisite.

## Saving the transcript

When directed, save the complete conversation as `transcripts/research-YYYY-MM-DD_HHMMSS.md`, label messages `Developer` and `Agent`, and confirm the path.
