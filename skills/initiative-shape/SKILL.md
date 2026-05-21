---
name: initiative-shape
description: >
  Shapes a vague idea into a properly formed Linear initiative — goal sentence, 3 measurable
  key results (each with baseline / target / window / source and a committed/aspirational tag),
  affected repos, appetite, kill condition, and project type — then creates the Linear project.
  OKR-shaped: the goal is the Objective, the key results are observable states. Use when
  starting any sustained body of work, converting a repo-aliased project into a goal-oriented
  initiative, or preparing for cycle planning. Trigger phrases: "I want to work on",
  "new initiative", "create a project", "we should tackle", "shape this for the next cycle",
  "what should the next initiative be".
pack: product
lifecycle_stage: define
principles_implemented:
  - source: product
    id: P2
    bucket: embedded
  - source: product
    id: P3
    bucket: embedded
  - source: product
    id: A2
    bucket: embedded
  - source: product
    id: A3
    bucket: embedded
  - source: product
    id: C1
    bucket: embedded
  - source: eng-agentic
    id: 3
    bucket: embedded
length_target: 200–260
author: Anton Babushkin
predecessor:
  repo: none
  skill: none
  relation: new
kept_from_predecessor: "n/a"
changed_from_predecessor: "n/a"
---

# Initiative shape

## Purpose

initiative-shape is the entry point for creating a new initiative. It takes a vague idea — a sentence, a direction, a problem — and shapes it into a properly formed Linear project with a goal sentence (Objective), 3 measurable key results (each with baseline / target / window / source and a committed/aspirational tag), affected repos, bounded appetite, kill condition, and project type. The shaped initiative is then created in Linear.

The skill exists because initiatives shaped without key results become repo-aliased backlogs, and backlogs without observable outcomes don't drive decisions. The Objective and KRs must be defined before the work begins — not inferred once the issues are closed (Rules P2, A3, C1, agentic Principle 3).

## When to use

- Starting any body of work that will span 5 or more issues.
- Converting an existing repo-project into a properly formed initiative.
- Preparing 3 initiatives for an upcoming cycle — run this once per initiative.
- When "I want to work on X" and X is clearly bigger than a single issue or bug fix.

## When not to use

- **Single-issue, bug, or KTLO work** — create the issue directly and put it in the ops slot. The ops slot has no goal/KR requirement.
- **Unvalidated ideas that haven't cleared idea-triage** — run `idea-triage` first if you're unsure the problem is worth pursuing at all.
- **Scoping an already-formed initiative** — use `planning-and-task-breakdown` once goal + key results are confirmed.

## Inputs

The vague idea in any form: a sentence, a project name, a direction, a problem statement fragment. The skill probes for everything else — do not require the user to pre-format anything.

Optional: a list of existing open issues the user expects to belong to this initiative.

## Outputs

A Linear project (via `mcp__claude_ai_Linear__save_project`) whose description follows the six-field initiative format: Goal / Key results / Affected repos / Appetite / Kill condition / Project type. Each KR carries five sub-fields (state, baseline, target, window, source) and a `[committed|aspirational]` tag. The project starts in Planned state — it does not enter a cycle until cycle planning.

## Workflow

**1. Capture the raw idea.**
Write it down verbatim. Do not reframe it yet.

**2. [GATE] Problem or solution?**
Read the raw idea. Is it framed as something to build ("add X", "integrate Y") or a problem to solve ("users can't Z", "the model output isn't usable")? If solution, probe: "What goes wrong if we don't build this?" If the underlying problem can't be articulated, the initiative is not ready. Return for clarification; do not proceed.

**2.5. Probe — project type.**
Before asking outcome questions, capture which of the six project types this initiative belongs to. The type sets the Objective shape and the rubric the KRs are judged against — a methodology skill pack and a personal product can both pass cycle close, but they pass on different KRs, because their theories of success are different.

Ask:

> "Which type? `1` methodology skill pack · `2` personal product · `3` utility skill pack · `4` research/thesis · `5` equity research · `6` production / customer-facing."

One-paragraph descriptions of each type are in `references/initiative-types.md` — load it if the user wants the longer form. If the user can't pick a single type, the initiative likely contains two outcomes — flag and split before proceeding.

**3. Probe — outcome questions.**

**Load the type-specific playbook first.** Open `references/initiative-types.md` and read the Objective shape, default KR mix, and anti-patterns for the type chosen at Step 2.5. The KR mix names which leading + lagging dimensions this initiative is scored along — propose KRs from those dimensions rather than from a blank page.

Default KR mix by type:

- **Type 1 (methodology skill pack)** — invocation-rate KR (leading) + decision-quality KR (lagging) + anti-output guard KR (committed). See playbook for a worked example on `/initiative-shape` itself.
- **Types 2–6** — playbooks land in later slices; for now, use the generic outcome frame below and avoid type-specific KR-mix claims.

Then ask explicitly. Do not infer. Wait for a response before synthesising.

- **Who is affected?** Which users, operators, or contexts does this problem touch?
- **What's the negative outcome if this isn't solved?** What task fails, what decision can't be made, what workflow breaks?
- **What 3 observable states would tell you it worked?** (Cap at 5; default 3 — per Wodtke.) Each one should be something a future agent can verify by looking at the system — a binary pass/fail, a fitness function firing, or a measurable delta. Avoid "improve X" / "better Y" language and avoid arbitrary "run N times" thresholds. **For Type 1, propose the default mix from the playbook (invocation-rate + decision-quality + anti-output guard) and ask the user to confirm or reshape — do not start from a blank page when a playbook applies.**
- **For each KR, fill all four sub-fields:**
  - **baseline** — current value or state (if unknown, the first issue in the initiative is to measure it)
  - **target** — value or state we expect at the end
  - **window** — when this is judged ("by end of cycle", "across next 4 cycles", "within 30 days")
  - **source** — where the evidence will live (a file path, a Linear query, a log, a cached report)
  - And tag each KR `[committed]` (must hit 1.0 — operability, no-silent-failure, baseline tracking) or `[aspirational]` (0.6–0.7 is success — outcome KRs, behaviour change, forecast calibration). A mixed OKR with 1–2 committed + 1–2 aspirational is the common shape.
- **Which repos does this touch?** Name them. Cross-repo scope is allowed; name it explicitly.

**4. Probe — scope and kill condition.**
Two separate questions:

- **Appetite — how many issues?** Guide: 5 ≈ small (1–2 days), 10 ≈ medium (full cycle slot), 15 ≈ large (fills the whole cycle). If the answer exceeds 15, the initiative needs splitting — flag this now.
- **Kill condition — when do we stop?** Name the observable state that says "the bet didn't work, walk away." An initiative with KRs but no kill condition becomes a zombie. Phrasing: "If [KR] fails for [N] consecutive cycles" / "If we ship [X] and [baseline metric] doesn't move" / "If we learn [Y] in research".

**5. Synthesise into initiative format.**
Draft the six fields (OKR-shaped — Goal is the Objective; Key results are 3 observable states with full sub-field discipline). Use the template in the next section.

Each KR's state should be one of: a binary pass/fail ("X works on the common path with no manual intervention"), a fitness function firing ("the guard fails the run loudly when Y"), or a measurable delta ("token footprint drops vs baseline"). No "improve X" / "better Y" / "run N times" language. Every KR must have all four sub-fields (baseline / target / window / source) and a `[committed|aspirational]` tag.

Present the draft. Do not create the Linear project yet.

**6. [GATE] User confirms the draft.**
Ask explicitly: "Does this capture the initiative correctly? Any changes to the Objective, the Key results, kill condition, or project type before I create the project?" Do not proceed until confirmed. Fixing a wrong problem statement, vague KR, or missing kill condition here takes one minute; fixing it mid-cycle costs days.

**7. Create the Linear project.**
Call `mcp__claude_ai_Linear__save_project` with:
- `name`: goal or problem label — not a solution name, not a repo name
- `description`: the six-field initiative format (see template below)
- Status: Planned

Confirm the project URL and share it.

**8. Optional: assign known issues.**
If the user listed existing issues for this initiative, list them and offer to reassign them to the new project via `mcp__claude_ai_Linear__save_issue`. Assign only the ones the user confirms.

## Initiative description template

```markdown
**Goal:** For [who], we want to [solve problem / achieve outcome].

**Key results:**

**KR1 [committed|aspirational]** — [observable state — binary pass/fail, fitness function firing, or measurable delta]
- baseline: [current value/state]
- target:   [target value/state]
- window:   [time frame]
- source:   [where the evidence will live — file path, Linear query, log, cached report]

**KR2 [committed|aspirational]** — [observable state]
- baseline: ...
- target:   ...
- window:   ...
- source:   ...

**KR3 [committed|aspirational]** — [observable state]
- baseline: ...
- target:   ...
- window:   ...
- source:   ...

(3 KRs default; cap at 5. When the key results hold — or are definitively ruled out — the initiative is Done.)

**Affected repos:** [list]

**Appetite:** ~[N] issues

**Kill condition:** [the observable state that says "stop pursuing this Objective"]

**Project type:** [1: methodology | 2: personal product | 3: utility skill pack | 4: research/thesis | 5: equity research | 6: production]
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "I know what the goal is — I don't need to write it down." | The KRs aren't for you right now; they're for the agent in the next session who has no memory of this conversation. Write them down. |
| "The key results will be obvious once the work is done." | Defining them after the work is done is how "shipped = done" creeps in. KRs are what convert a list of closed issues into an achieved outcome. |
| "One KR is enough — the goal sentence covers the rest." | One KR collapses easily into a single arbitrary threshold. 3 KRs force you to name the dimensions that actually matter (correctness, no-blocking, no-silent-failure, speed) — and that's the discipline. |
| "I don't know the baseline — I'll add it later." | If baseline isn't known, the first issue in the initiative is to measure it. A KR without a baseline is an aspiration, not a result — you can't grade it at cycle close. |
| "The target is obvious from the goal — I don't need to spell it out separately." | The target is what makes the KR scoreable. Without it, "we'll know it when we see it" replaces a binary pass/fail, and the post-launch review degrades to vibes. |
| "I don't need a window — we'll just keep at it until it lands." | Without a window, a KR cannot be closed. Open-ended KRs become zombies — they neither succeed nor fail, they just live on the project page forever. |
| "The source of evidence is obvious — it's just whether the feature works." | Name the artefact. A file path, a Linear query, a log line, a cached report. If you can't name where the evidence lives, the KR isn't inspectable — and an uninspectable KR is a feeling, not a result. |
| "Why a kill condition? We're going to make this work." | Most bets don't pay off on the first try. The kill condition is what protects the next quarter from a sunk-cost zombie. Naming it up front costs one sentence; not naming it costs an entire cycle. |
| "Project type is bureaucratic — we know what kind of thing this is." | The field exists so the next agent — or you in three weeks — can apply the right rubric without re-deriving the taxonomy. It's a one-token tag and a downstream skill needs it. |
| "We just need to author N new skills this cycle — the pack is the deliverable." | For methodology skill packs (Type 1), volume of skills authored is output, not outcome. Success is invocation accuracy at the decision moment + decision quality when invoked. Reshape into invocation-rate + decision-quality KRs — see Type 1 playbook in `references/initiative-types.md`. |
| "Improving skill quality this cycle is enough — we don't need a KR for it." | "Improve quality" fails Wodtke's weekly-trackable test. Reshape into a decision-quality KR: in ≥X of last N sampled invocations, the skill surfaced an issue or produced an artefact that would otherwise not have appeared. Now it has a sample, target, and window — and can be graded at cycle close. |
| "This is too big for 15 issues but it's one coherent thing." | Split by outcome: which key result do you want first? That's one initiative. The rest follow. |
| "I'll sort out the KRs after we create the project." | Step 6 is a gate. The project doesn't get created until the KRs (with all sub-fields) and kill condition are confirmed. |
| "The affected repo is obvious — we only work in one repo here." | Name it anyway. The field exists for cross-repo legibility, not to teach you something you don't know. |

## Red flags

- A KR says "improve X" or "better Y" with no observable state to verify.
- KRs are arbitrary "run N times" thresholds rather than common-path correctness, no-silent-failure, or measurable-delta states.
- Only 1 or 2 KRs — the initiative is probably under-specified along the dimensions that actually matter (default 3; cap 5).
- A KR is missing one or more of baseline / target / window / source.
- A KR is missing its `[committed]` or `[aspirational]` tag — the rubric for grading it at cycle close is undefined.
- No kill condition — the initiative has no defined off-ramp and will become a zombie when the bet doesn't pay off.
- The Project type field is missing or set to a free-text label that doesn't match the six-type taxonomy.
- For Type 1 (methodology skill pack), every KR scores artefact volume (skills authored, lines written, files edited) — no invocation-rate (leading) or decision-quality (lagging) KR. The OKR is then measuring output, not outcome.
- The initiative name describes a solution ("Build the X feature") rather than a goal or problem.
- The appetite is expressed as a time duration ("2 weeks") rather than an issue count.
- The Linear project was created before Step 6 confirmed the draft.
- An initiative with > 15 issues in appetite was created without a split decision.

## Verification / exit criteria

The skill has run correctly when:

1. A Linear project exists with a description containing all six canonical fields (Goal / Key results / Affected repos / Appetite / Kill condition / Project type).
2. The goal sentence names who is affected and what the outcome is — not a solution.
3. The Key results list contains 3 entries (cap 5), each an observable state (binary pass/fail, fitness function firing, or measurable delta) — no "improve X" / "better Y" / "run N times" language.
4. Every KR carries all four sub-fields — baseline, target, window, source — and a `[committed]` or `[aspirational]` tag.
5. The kill condition is present and names an observable state that says "stop pursuing this Objective."
6. The project type is set to one of the six values (1–6).
7. The appetite is expressed in issues (not days or weeks).
8. The user confirmed the draft before the project was created (Step 6 gate honoured).
9. For type=1 (methodology skill pack), at least one KR is an invocation-rate (leading) indicator and at least one is a decision-quality (lagging) indicator — the OKR is not measuring only artefact volume.

## References

- `rules/linear-workflow.md` — initiative definition, lifecycle, cycle model, ops slot (source of truth)
- `rules/PRODUCT_RULES.md` — P2 (problems not solutions), P3 (bets), A2 (problem format), A3 (measurable success criteria — applied here as 3 KRs with baseline/target/window/source discipline), C1 (appetite)
- `rules/eng-principles-agentic.md` — Principle 3 (spec as seatbelt; goal must precede work)
- `references/initiative-types.md` — six-type taxonomy and per-type playbooks (Objective shape, default KR mix, anti-patterns, verification rubric) — loaded at Step 2.5 and Step 3
- `skills/idea-triage/SKILL.md` — upstream: run when confidence is low before committing to an initiative
- `skills/planning-and-task-breakdown/SKILL.md` — downstream: breaks a confirmed initiative into issues
