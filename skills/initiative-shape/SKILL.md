---
name: initiative-shape
description: "Shapes a vague idea into a properly formed initiative — goal sentence, 3 measurable key results (each with baseline / target / measured over / how we'll know, a commit/stretch tag, and a bet/brake/foundation role), affected repos, appetite, kill condition, and project type. Records the shape via the installed tracker binding when one is present, otherwise emits a paste-ready markdown block. Use when starting any sustained body of work, converting a repo-aliased project into a goal-oriented initiative, or preparing for cycle planning."
---

# Initiative shape

## Purpose

Take a vague idea — a sentence, a direction, a problem — and shape it into a properly formed initiative: a goal sentence (the Objective), 3 measurable key results (each with baseline / target / measured over / how we'll know, a commit/stretch tag, and a bet/brake/foundation role), affected repos, bounded appetite, kill condition, and project type.

The Objective and KRs must be defined before the work begins, not inferred once the issues are closed. An initiative shaped without key results becomes a repo-aliased backlog, and a backlog without observable outcomes doesn't drive decisions. The confirmed shape is recorded by the installed tracker binding if one is present, or emitted as a paste-ready markdown block when none is — the skill owns the shaping, not the tracker.

## When to use

- Starting any body of work that will span 5 or more issues.
- Converting an existing repo-project into a properly formed initiative.
- Preparing initiatives for an upcoming cycle — run once per initiative.
- "I want to work on X" where X is clearly bigger than a single issue or bug fix.

## Do not use when

- Single-issue, bug, or KTLO work — create the issue directly in the ops slot; it has no goal/KR requirement.
- Unvalidated ideas — run idea-triage first if you're unsure the problem is worth pursuing.
- Scoping an already-formed initiative into deliverables and nodes — use delivery-shape once goal + KRs are confirmed.

## Inputs

The vague idea in any form: a sentence, a project name, a direction, a problem fragment. The skill probes for everything else — do not require the user to pre-format anything.

Optional: a list of existing open issues the user expects to belong to this initiative.

## Outputs

A confirmed **initiative shape** — the six-field format (Goal / Key results / Affected repos / Appetite / Kill condition / Project type), rubric-clean per the Step 7 gate. The shape is the deliverable; where it lands depends on the environment:

- **Tracker binding present** (e.g. the Workflow pack) — hand the shape to that procedure to record as an initiative, in a planning/not-yet-in-cycle state.
- **No tracker binding** — emit the markdown block from the template section for the user to paste into their tracker. This is a correct terminal state, not a failure.

Either way the shape reads as a product OKR: PM-readable field names, with rubric vocabulary (Layer 1 dimension, Layer 2 template) confined to an italic audit-footer, never the KR body.

## Workflow

### 1. Capture the raw idea

Write it down verbatim. Do not reframe it yet.

### 2. Gate: problem or solution?

Is the idea framed as something to build ("add X", "integrate Y") or a problem to solve ("users can't Z", "the model output isn't usable")? If it's a solution, probe: "What goes wrong if we don't build this?" If the underlying problem can't be articulated, the initiative is not ready — return for clarification, do not proceed.

### 3. Probe: project type

Capture which of the six project types this initiative belongs to before asking outcome questions. The type sets the Objective shape and the rubric the KRs are judged against.

> "Which type? `1` methodology skill pack · `2` personal product · `3` utility skill pack · `4` research/thesis · `5` equity research · `6` production / customer-facing."

One-paragraph descriptions of each type are in `references/initiative-types.md`. If the user can't pick a single type, the initiative likely contains two outcomes — flag and split before proceeding.

### 4. Probe: outcome questions

**Load the type-specific playbook first.** Open `references/initiative-types.md` and read the Objective shape, default KR mix, and anti-patterns for the chosen type. Propose KRs from those dimensions, not from a blank page.

Default KR mix by type:

- **Type 1 (methodology skill pack)** — invocation-rate KR (leading) + decision-quality KR (lagging) + anti-output guard KR (committed).
- **Type 2 (personal product, single-user)** — correctness KR (lagging) + no-silent-failure KR (committed) + maintenance-burden KR (committed). Availability KR optional 4th. Growth/MAU/retention KRs are categorically inapplicable — there is one user.
- **Type 3 (utility skill pack)** — first-shot correctness KR (aspirational, lagging) + coverage KR (committed) + use-log discipline KR (committed). Use-log discipline is non-negotiable: every invocation logged at the moment of use to a named location (e.g. `listings/`, `outputs/`, `runs/`) with input, generated artefact, final-posted artefact, and edit-or-not outcome — or the lagging first-shot correctness KR is ungradable. Time-to-result KRs are usually vanity here.
- **Type 4 (research / thesis-driven)** — knowledge-claim KR (committed) + critique-survivability KR (aspirational, lagging) + source-discipline KR (committed). Adoption KR is a later-stage 4th — defer until critique-survivability holds. "Publish N essays" / "N readers" are output, not defensibility.
- **Type 5 (equity research tooling)** — pre-registration KR (committed) + calibration KR (aspirational, lagging) + hit-rate KR (aspirational, lagging). Pre-registration is non-negotiable: every BUY/WATCH/AVOID call written to a dated, immutable artefact (cached `reports/TICKER_YYYYMMDD.json` + git history) before outcomes are visible, or the lagging KRs are ungradable. This is the Tetlock standard.
- **Type 6 (production / customer-facing)** — activation/retention/conversion KR (aspirational, lagging) + quality-pair KR (committed — NPS, p95 latency, error rate, or support volume per user) + telemetry-discipline KR (committed). Every value KR must have a paired quality counterweight. Telemetry must be in place before the cycle starts.

Then ask explicitly. Do not infer. Wait for a response before synthesising.

- **Who is affected?** Which users, operators, or contexts does this problem touch?
- **What's the negative outcome if this isn't solved?** What task fails, what decision can't be made, what workflow breaks?
- **Which KR is the bet, which are brakes, which is foundation?** The **bet** is what you're actually pushing this cycle (target is a delta or new state). **Brakes** are things that already work and you only want to protect from regression (target is "stay ≥ baseline" or "stay at 0"). **Foundation** is the instrumentation that has to exist before the bet KR is measurable. Most initiatives have at most 1–2 bets; if everything feels like a bet, the brakes haven't been named. (Roles in `references/kr-quality-templates.md`.)
- **What 3 observable states would tell you it worked?** (Cap at 5; default 3.) Each one verifiable by looking at the system — a binary pass/fail, a fitness function firing, or a measurable delta. Avoid "improve X" / "better Y" and arbitrary "run N times" thresholds. Propose the default mix from the playbook and ask the user to confirm or reshape.
- **For each KR, fill all four sub-fields** (PM-readable labels — these appear in the recorded description):
  - **baseline** — current value or state (if unknown, the first issue is to measure it)
  - **target** — value or state expected at the end
  - **measured over** — when it's judged ("by end of cycle", "across next 4 cycles", "within 30 days")
  - **how we'll know** — where the evidence lives (file path, tracker query, log, cached report; if grader-backed, the named file plus the one-sentence command that emits the verdict)
  - Tag each KR `(commit)` (must hit 1.0: operability, no-silent-failure, baseline tracking) or `(stretch)` (aspirational — 0.6–0.7 is success: outcome KRs, behaviour change, forecast calibration). A mixed OKR with 1–2 `(commit)` + 1–2 `(stretch)` is the common shape.
  - Tag each KR with its **role** — `bet` / `brake` / `foundation` — appended in italics to the headline (e.g. `*(bet)*`). Role is orthogonal to `(commit|stretch)`.
- **Which repos does this touch?** Name them. Cross-repo scope is allowed; name it explicitly.

### 5. Probe: scope and kill condition

Two separate questions:

- **Appetite — how many issues?** Guide: 5 ≈ small (1–2 days), 10 ≈ medium (full cycle slot), 15 ≈ large (fills the cycle). If the answer exceeds 15, the initiative needs splitting — flag now.
- **Kill condition — when do we stop?** Name the observable state that says "the bet didn't work, walk away." An initiative with KRs but no kill condition becomes a zombie. Phrasing: "If [KR] fails for [N] consecutive cycles" / "If we ship [X] and [baseline metric] doesn't move" / "If we learn [Y] in research".

### 6. Synthesise into initiative format

Draft the six fields (OKR-shaped — Goal is the Objective; Key results are 3 observable claims with full sub-field discipline). Use the template in the next section: PM-readable field names, rubric vocabulary confined to the audit-footer.

Each KR's headline should be a binary pass/fail ("X works on the common path with no manual intervention"), a fitness function firing ("the guard fails the run loudly when Y"), or a measurable delta ("token footprint drops vs baseline"). No "improve X" / "better Y" / "run N times" language. Add the audit-footer line (`*Layer 1: … · Layer 2: …*`) under each KR and the dimensions-summary line after the list.

**Dominant model tier (optional note, not a gate).** Scan the expected task profile: mostly mechanical rewrites with no external API surface → note `Fast`; mostly bounded reasoning or reversible-but-non-trivial paths → `Balanced`; one-way doors (schema migrations, public APIs, auth, production data) or orchestrator-level decomposition → `Frontier`. Individual tasks are routed using `references/task-sizing.md`.

Present the draft. Do not record or emit the shape yet.

### 7. Gate: user confirms the draft

Ask explicitly: "Does this capture the initiative correctly? Any changes to the Objective, the Key results, kill condition, or project type before I create the project?" Do not proceed until confirmed. Fixing a wrong problem statement or vague KR here takes a minute; fixing it mid-cycle costs days.

### 8. Gate: verification rubric — 11 cross-cutting rules

Run these checks against the confirmed draft. Each is a binary pass/fail. Any failure returns the draft to Step 6 for repair — the shape is NOT captured until all 11 pass.

| # | Rule | Pass condition |
|---|---|---|
| 1 | All six fields present | Goal / Key results / Affected repos / Appetite / Kill condition / Project type are all non-empty |
| 2 | Goal names who + outcome | Sentence contains an affected party and a desired outcome — no solution verb ("build", "add", "integrate", "ship") |
| 3 | Initiative name is a goal/problem | Name does not open with a solution verb ("Build X", "Add Y", "Integrate Z") |
| 4 | At least 3 KRs, no more than 5 | KR count ≥ 3 and ≤ 5 |
| 5a | No degenerate KRs | `target ≠ baseline` numerically or by state change — bans "baseline 100%, target 100%" |
| 5b | KRs name distinct Layer 1 dimensions | No two KRs share a Layer 1 dimension. Default vocabulary: correctness / outcome / maintenance / discipline (see `references/kr-quality-templates.md`). Out-of-default dimensions (e.g. performance) permitted only when the initiative genuinely has that property |
| 5c | KRs are not Goal-restatements | Strip the Goal to its measurable noun-phrase; no KR's observable state matches it. Each KR names a *measurable property of* the Goal, not the Goal itself |
| 5d | KR matches its Layer 2 template | For each KR, name its Layer 1 dimension and confirm it matches the template (golden-path test / self-trial protocol / structural cap + revisit gate / artefact-exists + sections-complete) in `references/kr-quality-templates.md` |
| 5e | Language ban | No KR contains "improve", "better", "enhance", or arbitrary "run N times" thresholds without a correctness or quality dimension |
| 5f | KR is grader-backed (or carved out) | Each KR's `how we'll know:` points at a command/script/query that emits a verdict against the target, describable in one sentence at draft time. Manual grading is permitted only when (a) the initiative is genuinely one-shot/throwaway, OR (b) the verdict is irreducibly qualitative ("the prose reads naturally") and no honest automatable proxy exists — the carve-out must be stated. Building the grader is scoped into the initiative as one or two stories before it goes Active |
| 6 | Every KR has all four sub-fields, no placeholders | baseline, target, measured over, how we'll know — none blank, none `TBD`/`unknown`/`we'll figure it out`/`various`/`the logs`/`the dashboard`/`better than today`. `how we'll know` points to a concrete artefact: file path, directory, tracker query, log query, cached report URL, or metric name + system |
| 7 | Every KR is tagged | Each KR carries exactly one of `(commit)` or `(stretch)` |
| 8 | Kill condition is present | Non-empty; names an observable state, not "if it doesn't work" |
| 9 | Project type is canonical | One of 1–6, not free text |
| 10 | Appetite is in issues | Expressed as "~N issues", not days/weeks/sprints |
| 11 | Every KR has a role tag | Each KR carries exactly one of `bet` / `brake` / `foundation` |

**Soft check (warning, not a hard fail):** if every KR is tagged `bet`, surface a warning — most initiatives have at most 1–2 bets, and an all-bet draft usually means brakes and foundation were silently omitted. Ask whether a brake or foundation KR is missing. Do not force one of each role — some shapes are honestly 2 bets + 1 foundation, or 1 bet + 2 brakes.

Report each failing rule by number with the specific text that triggered it. For rule 5, name the sub-rule (5a–5f). When all checks pass, proceed to Step 9.

### 9. Capture or hand off the shape

The six fields are confirmed and the rubric is clean. Take exactly one branch:

- **Tracker binding installed** — follow the loaded tracker-capture procedure (e.g. the Workflow pack). Hand it the confirmed six-field shape as the `description`, the goal-or-problem label as the name (not a solution or repo name), and the planning/not-yet-in-cycle state. That procedure owns every tracker call; do not invent one. Confirm and share the locator it returns. If the user listed existing issues, defer to the same procedure to attach the confirmed ones.
- **No tracker binding** — emit the confirmed shape as the markdown block in the next section, filled in. Do not attempt a tracker call — there is none bound.

A dry run with no Workflow pack ends at the emitted markdown shape.

## Initiative description template

The shape reads as a product OKR — a non-pack-author should be able to grade each KR in 30 seconds. Each KR's headline *is* the observable claim (no separate `state:` field). The four sub-fields use PM-readable names; rubric vocabulary lives only in the italic audit-footer and the dimensions-summary line — never in the KR body.

```markdown
**Goal:** For [who], we want to [solve problem / achieve outcome].

**Key results:**

**KR1 (commit|stretch)** — [the observable claim as one readable sentence: binary pass/fail, fitness function firing, or measurable delta] *(bet|brake|foundation)*
- baseline: [current value/state]
- target:   [target value/state]
- measured over: [time frame or N units — "by cycle close", "next 10 listings", "within 30 days"]
- how we'll know: [where the evidence lives — file path / query / log / cached report; if grader-backed, the named file plus the one-sentence command that emits the verdict]

*Layer 1: [dimension] · Layer 2: [template]*

**KR2 (commit|stretch)** — [observable claim] *(bet|brake|foundation)*
- baseline: ...
- target:   ...
- measured over: ...
- how we'll know: ...

*Layer 1: [dimension] · Layer 2: [template]*

**KR3 (commit|stretch)** — [observable claim] *(bet|brake|foundation)*
- baseline: ...
- target:   ...
- measured over: ...
- how we'll know: ...

*Layer 1: [dimension] · Layer 2: [template]*

*Dimensions: [d1] / [d2] / [d3] — all distinct per rule 5b.*

(3 KRs default; cap at 5. When the key results hold — or are definitively ruled out — the initiative is Done. Each headline ends with a role — `bet` (the push), `brake` (don't regress), or `foundation` (makes the bet measurable); most initiatives have at most 1–2 bets.)

**Affected repos:** [list]

**Appetite:** ~[N] issues

**Kill condition:** [the observable state that says "stop pursuing this Objective"]

**Project type:** [1: methodology | 2: personal product | 3: utility skill pack | 4: research/thesis | 5: equity research | 6: production]

**Dominant model tier:** [Fast|Balanced|Frontier] — expected tier for the majority of tasks; informational, not a gate. See `references/task-sizing.md`.
```

The `*Layer 1 · Layer 2*` footer and `*Dimensions: …*` line are the rubric trace (they back checks 5b and 5d). They sit below the KR body, in italics, so the OKR reads cleanly. Do not put Layer/rule annotations inside a KR headline or sub-fields.

## Red flags

- A KR says "improve X" or "better Y" with no observable state to verify.
- KRs are arbitrary "run N times" thresholds rather than common-path correctness, no-silent-failure, or measurable-delta states.
- Only 1 or 2 KRs — under-specified along the dimensions that matter (default 3; cap 5).
- A KR is missing one or more of baseline / target / measured over / how we'll know.
- A KR is missing its `(commit)` or `(stretch)` tag, or its `bet` / `brake` / `foundation` role tag.
- Every KR is a forward push (no `brake`, no `foundation`) — usually means the actual bet vs the guardrails weren't named.
- No kill condition — the initiative has no off-ramp and becomes a zombie when the bet doesn't pay off.
- The Project type field is missing or a free-text label outside the six-type taxonomy.
- **Type 1:** every KR scores artefact volume (skills authored, lines written) — no invocation-rate or decision-quality KR. Measuring output, not outcome.
- **Type 2:** any KR targets growth (MAU, DAU, retention, signups) or feature volume — misclassified, or growth metrics imported from a model that doesn't apply.
- **Type 3:** every KR scores skill volume or invocation count — measuring output, not utility. Or no use-log discipline KR and no how-we'll-know location named as a file path/directory for the first-shot correctness KR — the lagging KR is ungradable.
- **Type 4:** every KR scores essay count, reader count, or subscribers — no knowledge-claim or source-discipline KR. Measuring volume or audience noise, not defensibility.
- **Type 5:** no pre-registration KR — calls aren't logged to a dated, immutable artefact before outcomes are visible, so the calibration and hit-rate KRs are ungradable. Or KRs target throughput / un-pre-registered outperformance.
- **Type 6:** a growth/conversion/retention KR has no paired quality KR (Cagan's canonical failure mode). Or a KR uses feature-rollout language ("ship X to 100%") rather than the customer behaviour the feature should change. Or telemetry isn't in place before the cycle starts and there's no telemetry-discipline KR.
- The initiative name describes a solution ("Build the X feature") rather than a goal or problem.
- The appetite is a time duration ("2 weeks") rather than an issue count.
- The shape was recorded or emitted before the Step 7 confirmation.
- An initiative with > 15 issues in appetite was created without a split decision.

## Exit criteria

The skill is complete when:

1. The confirmed shape contains all six canonical fields — recorded via the bound tracker procedure when one is present, or emitted as the markdown block when none is.
2. The goal names who is affected and the outcome — not a solution.
3. The Key results list has 3 entries (cap 5), each an observable state — no "improve X" / "better Y" / "run N times" language.
4. Every KR carries all four sub-fields, a `(commit)`/`(stretch)` tag, and a `bet`/`brake`/`foundation` role tag.
5. The kill condition names an observable state that says "stop pursuing this Objective."
6. The project type is one of 1–6.
7. The appetite is expressed in issues.
8. The user confirmed the draft before the shape was captured or emitted.
9. The type-specific KR requirement holds (see `references/initiative-types.md` for each type's mandatory leading/lagging/discipline KRs — Type 1 invocation-rate + decision-quality; Type 2 correctness + operability; Type 3 first-shot correctness + use-log discipline with a named location; Type 4 knowledge-claim + source-discipline; Type 5 pre-registration; Type 6 value + paired quality + telemetry-discipline). The OKR is gradable post-hoc from artefacts alone, without narration.

## Related

- idea-triage: upstream — run when confidence is low before committing to an initiative.
- delivery-shape: downstream — shapes a confirmed initiative into deliverables, nodes, and tasks.
- `references/initiative-types.md` — six-type taxonomy and per-type playbooks (Objective shape, default KR mix, anti-patterns); loaded at Steps 3 and 4.
- `references/kr-quality-templates.md` — Layer 1 dimensions, Layer 2 templates, KR roles, and the grader-backed KR pattern; cited by rules 5b, 5d, 5f, 11.
- `references/task-sizing.md` — model-tier routing rubric behind the dominant-tier field.
- Tracker capture + cycle model — owned by the Workflow pack when installed; the six-field shape and KR sub-field requirements are defined inline here, so the skill is self-contained when no tracker is bound.
