---
name: initiative-shape
description: "Shapes a vague idea into a properly formed initiative with a clear goal and measurable criteria for success"
---

# Initiative shape

## Purpose

Shape a vague idea into an initiative before work begins, so the work is governed by observable outcomes instead of becoming a repo-aliased backlog. The skill owns the product shape: Goal, Key results, Affected repos, Appetite, Kill condition, and Project type. A tracker binding may record the result, but it does not define the shape.

## When to use

- Starting work expected to span 5 or more issues.
- Converting an existing repo-project into a goal-oriented initiative.
- Preparing initiatives for an upcoming cycle, once per initiative.
- "I want to work on X" where X is bigger than a single issue or bug fix.

## Do not use when

- The work is a single issue, bug, or KTLO item.
- The initiative is already formed and needs deliverables, nodes, or tasks. Use `delivery-shape`.

## Inputs

The user may provide a sentence, project name, direction, problem fragment, or list of existing open issues. Do not require a preformatted brief. Probe for the missing pieces.

## Outputs

A confirmed **initiative shape** that passes the Step 8 verification rubric.

- **Tracker binding present**: hand the confirmed six-field shape to the bound capture procedure in a planning/not-yet-in-cycle state. That procedure owns tracker calls and issue attachment.
- **No tracker binding**: emit the filled markdown block from the template section. This is a valid terminal state.

The result should read as a product OKR: PM-readable field names, observable KRs, and rubric vocabulary confined to the italic audit footer.

## Workflow

### 1. Capture the raw idea

Write the idea down verbatim. Do not reframe it yet.

### 2. Gate: problem or solution?

If the idea is framed as a solution ("add X", "integrate Y"), ask: "What goes wrong if we don't build this?" If the underlying problem cannot be articulated, stop and ask for clarification.

### 3. Probe: project type

Capture one of the six canonical project types before asking outcome questions. The type sets the Objective shape and the KR rubric.

> "Which type? `1` methodology skill pack | `2` personal product | `3` utility skill pack | `4` research/thesis | `5` equity research | `6` production / customer-facing."

Read `references/initiative-types.md` for the selected type's Objective shape, default KR mix, and anti-patterns. If the user cannot pick one type, the idea likely contains two initiatives; flag and split before proceeding.

### 4. Probe: outcome questions

Ask explicitly and wait for answers. Do not infer missing commitments.

- **Who is affected?** Which users, operators, or contexts does this problem touch?
- **What breaks if this is not solved?** What task fails, what decision cannot be made, or what workflow remains broken?
- **Which repos does this touch?** Name each repo. Cross-repo initiatives are allowed, but must be explicit.
- **What 3 observable states would tell us it worked?** Default to 3 KRs; cap at 5. Each KR must be verifiable from the system: a binary pass/fail, a fitness function firing, or a measurable delta.
- **Which KR is the bet, which are brakes, and which is foundation?** `bet` is what changes this cycle. `brake` protects a working property from regression. `foundation` makes the bet measurable. Most initiatives have at most 1-2 bets.
- **For each KR, fill the four required sub-fields:** `baseline`, `target`, `measured over`, and `how we'll know`.
- **For each KR, assign one delivery tag:** `(commit)` for must-hit operability, no-silent-failure, or baseline-tracking KRs; `(stretch)` for aspirational outcome, behavior-change, or calibration KRs.

Default KR mix by type:

- **Type 1, methodology skill pack**: invocation-rate + decision-quality + anti-output guard.
- **Type 2, personal product**: correctness + no-silent-failure + maintenance-burden. Availability may be a 4th KR. Growth metrics do not apply to a single-user product.
- **Type 3, utility skill pack**: first-shot correctness + coverage + use-log discipline. The use log must name a concrete location and record input, generated artefact, final-posted artefact, and edit-or-not outcome.
- **Type 4, research/thesis**: knowledge-claim + critique-survivability + source-discipline. Defer adoption until the thesis survives critique.
- **Type 5, equity research tooling**: pre-registration + calibration + hit-rate. BUY/WATCH/AVOID calls must be logged to dated, immutable artefacts before outcomes are visible.
- **Type 6, production/customer-facing**: activation/retention/conversion + paired quality + telemetry-discipline. Every value KR needs a quality counterweight, and telemetry must exist before the cycle starts.

### 5. Probe: scope and kill condition

Ask two separate questions:

- **Appetite:** how many issues? Guide: `~5` small, `~10` medium, `~15` large. If the answer exceeds 15, flag that the initiative needs splitting.
- **Kill condition:** what observable state says the bet did not work and we should stop? Examples: "If [KR] fails for [N] consecutive cycles", "If we ship [X] and [baseline metric] does not move", or "If the research establishes [Y]."

### 6. Synthesise into initiative format

Draft the six fields using the template below. The Goal is the Objective. Each KR headline is the observable claim; do not add a separate `state:` field.

Keep KR language concrete. Avoid "improve", "better", "enhance", and arbitrary "run N times" thresholds unless paired with a correctness or quality dimension.

Add the italic `Layer 1` / `Layer 2` audit footer under each KR and the dimensions summary after the KR list. Use `references/kr-quality-templates.md` for dimensions, templates, KR roles, and grader-backed patterns.

Optional note: include **Dominant model tier** when task routing matters. Use `Fast` for mostly mechanical rewrites, `Balanced` for bounded but non-trivial reasoning, and `Frontier` for one-way doors such as schema migrations, public APIs, auth, production data, or orchestrator-level decomposition. See `references/task-sizing.md`.

Present the draft. Do not record or emit it yet.

### 7. Gate: user confirms the draft

Ask explicitly: "Does this capture the initiative correctly? Any changes to the Objective, Key results, kill condition, or project type before I create the project?"

Do not proceed until the user confirms.

### 8. Gate: verification rubric — 11 cross-cutting rules

Run these checks against the confirmed draft. Each is pass/fail. Any failure returns the draft to Step 6 for repair. The shape is not captured until every hard rule passes.

| #   | Rule | Pass condition |
| --- | --- | --- |
| 1   | All six fields present | Goal / Key results / Affected repos / Appetite / Kill condition / Project type are non-empty |
| 2   | Goal names who + outcome | Goal contains an affected party and desired outcome, with no solution verb such as "build", "add", "integrate", or "ship" |
| 3   | Initiative name is a goal/problem | Name does not open with a solution verb |
| 4   | KR count | At least 3 KRs and no more than 5 |
| 5a  | No degenerate KRs | `target != baseline` numerically or by state change |
| 5b  | Distinct Layer 1 dimensions | No two KRs share a Layer 1 dimension, unless the referenced template explicitly permits it |
| 5c  | KRs are not Goal restatements | Each KR measures a property of the Goal, not the Goal itself |
| 5d  | KR matches Layer 2 template | Each KR's claim matches the cited template in `references/kr-quality-templates.md` |
| 5e  | Language ban | No vague "improve", "better", "enhance", or arbitrary "run N times" threshold |
| 5f  | Grader-backed or carved out | `how we'll know` points to a command, script, query, metric, or concrete artefact that can emit or support a verdict; manual grading is explicitly carved out only when the verdict is irreducibly qualitative or the initiative is one-shot |
| 6   | KR sub-fields complete | Every KR has non-placeholder `baseline`, `target`, `measured over`, and `how we'll know` values |
| 7   | Delivery tag present | Every KR has exactly one of `(commit)` or `(stretch)` |
| 8   | Kill condition is observable | Kill condition names a concrete stop state, not "if it doesn't work" |
| 9   | Project type is canonical | Project type is one of 1-6 |
| 10  | Appetite is in issues | Appetite is expressed as `~N issues`, not days, weeks, or sprints |
| 11  | Role tag present | Every KR has exactly one of `bet`, `brake`, or `foundation` |

Soft warning: if every KR is tagged `bet`, ask whether a brake or foundation KR is missing. Do not force one of each role; some shapes are honestly 2 bets + 1 foundation, or 1 bet + 2 brakes.

Report failing rules by number and quote the specific text that failed. For rule 5, name the sub-rule.

### 9. Capture or hand off the shape

Take exactly one branch:

- **Tracker binding installed**: follow the loaded tracker-capture procedure. Pass the confirmed six-field shape as the `description`, the goal/problem label as the name, and the planning/not-yet-in-cycle state. Confirm with the locator returned by that procedure.
- **No tracker binding**: emit the confirmed shape as the markdown block below. Do not attempt a tracker call.

## Initiative description template

The shape reads as a product OKR — a non-pack-author should be able to grade each KR in 30 seconds. Each KR's headline *is* the observable claim (no separate `state:` field). The four sub-fields use customer/business friendly names.

```markdown
**Goal:** For [who], we want to [solve problem / achieve outcome].

**Key results:**

**KR1 (commit|stretch)** - [observable claim: binary pass/fail, fitness function firing, or measurable delta] *(bet|brake|foundation)*
- baseline: [current value/state]
- target: [target value/state]
- measured over: [time frame or N units]
- how we'll know: [file path / query / log / cached report / metric + system; if grader-backed, include the command that emits the verdict]

**KR2 (commit|stretch)** - [observable claim] *(bet|brake|foundation)*
- baseline: ...
- target: ...
- measured over: ...
- how we'll know: ...

**KR3 (commit|stretch)** - [observable claim] *(bet|brake|foundation)*
- baseline: ...
- target: ...
- measured over: ...
- how we'll know: ...

**Affected repos:** [list]

**Kill condition:** [observable state that says to stop pursuing this Objective]
```

## Red flags

- The Goal or initiative name describes a solution instead of a problem or outcome.
- A KR is vague, output-count based, or cannot be graded from evidence.
- The draft lacks a kill condition, issue appetite, project type, KR role tags, or commit/stretch tags.
- The type-specific KR mix conflicts with `references/initiative-types.md`.
- The shape is about to be recorded or emitted before user confirmation.

## Exit criteria

The skill is complete when Step 8 passes and Step 9 has either recorded the shape through the bound tracker procedure or emitted the filled markdown block.

## Related

- `delivery-shape`: downstream; shapes a confirmed initiative into deliverables, nodes, and tasks.
- `references/initiative-types.md`: six-type taxonomy, Objective shapes, default KR mixes, and anti-patterns.
- `references/kr-quality-templates.md`: Layer 1 dimensions, Layer 2 templates, KR roles, and grader-backed KR patterns.
- `references/task-sizing.md`: model-tier routing rubric.
- Tracker capture and cycle model: owned by the Workflow pack when installed.
