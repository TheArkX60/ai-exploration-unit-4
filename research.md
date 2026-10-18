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

### Assets (all unverified)
- Ambient wind loop: not yet sourced.
- Owl hoot: not yet sourced.
- Story sound effects (tones, rumble, puff, creak, party sounds): not yet sourced.
- For each: record source link, license (CC0 or public domain only) and any required credit here before use.

## Revisions

Update decisions when new evidence changes the direction, linking to playtest observations in `plan.md` rather than copying them. Keep chosen behavior and asset requirements in `spec.md`. The Developer confirms when the inquiry is sufficient to continue building; exhaustive research is not a prerequisite.

## Saving the transcript

When directed, save the complete conversation as `transcripts/research-YYYY-MM-DD_HHMMSS.md`, label messages `Developer` and `Agent`, and confirm the path.
