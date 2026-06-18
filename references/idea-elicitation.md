---
name: idea-elicitation
description: >
  Interview-style elicitation loop for sharpening a raw idea before it is scored or routed.
  Ported from agent-skills:interview-me, voice-matched to this pack.
type: reference
cited_by:
  - skills/idea/SKILL.md
---

# Idea elicitation loop

A raw idea is almost always under-articulated. The person asks for "a dashboard" because that is what one asks for, not because a dashboard solves their problem. They say "we should build X" without naming who hurts when we don't. The cheapest moment to close that gap is at intake, before any evidence is taken or any score is assigned. Once a score exists, the conversation anchors on the number; once a build is in flight, switching costs are real.

This loop sharpens the idea by asking one question at a time, each carrying the skill's own best guess, until the person can confirm a six-line restate in their own words.

## When to run the loop

Run on every fresh idea unless the ask is unambiguous and self-contained (a renamed metric, a typo, a mechanical fix). If the request is conventional ("build me X", "make it faster", "we should add Y") and you cannot unpack the convention without guessing, run the loop.

Do not run in non-interactive contexts (CI, scheduled jobs, drain workers). If you are in one of those and the ask is underspecified, flag that as a blocker rather than guess.

## The loop

### 1. Hypothesise, with a confidence number

Before asking anything, write the current best read of the idea in one sentence, plus an honest confidence number (0–100%). Below ~70%, append a one-line reason — what is still unresolved or missing.

```
HYPOTHESIS: You want a way to answer "how are we doing?" in standup; "dashboard" was the convention that came to mind.
CONFIDENCE: ~30% — missing: who it's for, what "metrics" means, what success looks like.
```

The number forces honesty. If the number is high but you cannot predict the person's reaction to the next three questions you would ask, the number is wrong.

### 2. Ask one question at a time, each with a guess attached

Format:

```
Q: <one focused question>
GUESS: <your hypothesis for the answer, with the reasoning that produced it>
```

Wait for the person to react before the next question. Batches encourage skim-reading; the third question often depends on the answer to the first. Attaching a guess is faster for the person (react vs. generate) and exposes the skill's assumptions, which is the point.

Risk: a polite person agrees with the guess to be agreeable. Mitigate by being visibly willing to be wrong and occasionally guessing in a direction you expect push-back.

### 3. Listen for want vs. should-want

The most dangerous answers sound like a thoughtful answer rather than what the person actually wants. Watch for:

- Pattern-match phrases ("scalable", "clean architecture", "modern") without specifics
- Deferrals to convention ("the way most teams do it", "the standard approach")
- Should-language ("I should probably…", "good practice says…")

When you hear these, the next question is:

> "If you didn't have to justify this to anyone, what would you actually want?"

One question often does more work than the previous five.

### 4. Restate intent in their own words

When confidence is high, write back what you now think the person wants. Five to eight lines, their language where possible, structured so they can confirm or correct line by line:

```
Here's what I now think you want:

- Outcome:      <one line>
- User:         <one line — who benefits>
- Why now:      <one line — what changed>
- Success:      <one line — how we know it worked>
- Constraint:   <one line — the binding limit>
- Out of scope: <one line — what we're explicitly not doing>

Yes / no / refine?
```

Out of scope is non-negotiable. Half of misalignment is silent disagreement about what is *not* being built.

### 5. Confirm — explicit yes, not "whatever you think"

The gate is an explicit yes. The following are not yes:

- "Whatever you think is best." — delegation, not decision. Re-ask with two concrete options framed as a choice.
- "Sounds good." — ambiguous. Ask: "Anything you'd refine?"
- "Sure, let's go." — often a polite exit. Same follow-up.
- Silence followed by "okay let's start." — given-up, not converged. Ask what you missed.

Fold corrections in and restate. Loop until an explicit yes.

## The 95% stop

You are done when the answer is yes to: *can I predict the person's reaction to the next three questions I would ask?* If yes, stop interviewing and produce the restate. If no, ask the next question.

Floor: if you have gone several rounds and still cannot predict, that is information about the ask, not a reason to keep grinding. Stop and say: "I have asked N questions and still cannot predict your reactions. Something foundational is missing — want to step back?"

## Output of the loop

The output is a confirmed six-line restate (Outcome / User / Why now / Success / Constraint / Out of scope) with an explicit yes attached. Everything downstream in `shape:idea` — evidence interrogation, problem statement, routing, optional scoring — consumes this restate, not the original raw intake.

## Source

- `agent-skills:interview-me` (Addy Osmani, MIT) — original elicitation loop; ported here with voice-matched edits.
