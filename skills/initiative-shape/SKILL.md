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

### 6. Synthesize the draft

Draft the six fields using the template below. The Goal is the Objective. Each KR headline is the observable claim; do not add a separate `state:` field.

Keep KR language concrete. Avoid "improve", "better", "enhance", and arbitrary "run N times" thresholds unless paired with a correctness or quality dimension.

Use `references/kr-quality-templates.md` only when you need help choosing strong KR dimensions, roles, or evidence patterns. Do not add rubric/audit annotations to the user-facing shape.

Write the Goal and KRs against the `writing-refinement` skill — `skills/writing-refinement/references/style-rules.md` and `references/plans-okrs.md`. Name the gap between the current state, the desired state, and the cost of staying put; keep the actor in the subject and use concrete verbs.

Optional note: include **Dominant model tier** when task routing matters. Use `Fast` for mostly mechanical rewrites, `Balanced` for bounded but non-trivial reasoning, and `Frontier` for one-way doors such as schema migrations, public APIs, auth, production data, or orchestrator-level decomposition. See `references/task-sizing.md`.

Present the draft. Do not record or emit it yet.

### 6b. Gate: writing-editor pass

Before showing the draft to the user, dispatch the `writing-editor` persona (`agents/writing-editor/AGENT.md`) over the synthesized draft, per the dispatch protocol in `docs/adr/0003-persona-contract-and-dispatch-protocol.md` — the `Agent` tool on Claude Code, inline self-review on a non-Claude worker. Apply its line-level rewrites. On `reject`, repair and re-run once; if it still rejects, carry the remaining notes forward as `accept with notes` rather than blocking. Do not proceed to Step 7 until the verdict is `accept` or `accept with notes`.

### 7. Gate: user confirmation

Ask: "Does this capture the initiative correctly? Any changes to the Objective, Key results, kill condition, or project type before I create the project?"

Do not proceed until the user confirms.

### 8. Gate: verification rubric — 11 cross-cutting rules

Grade the confirmed draft against these checks. Each one must pass before capture. If a check fails, repair the draft in Step 6 and re-confirm only the changed parts with the user.

| #   | Rule | Pass condition |
| --- | --- | --- |
| 1   | Goal is outcome-shaped | Names who is affected and what should be true for them; does not describe a solution to build |
| 2   | Project type fits | One of the six project types is selected, and the KRs fit that type's default mix closely enough to be useful |
| 3   | KRs are few and distinct | 3-5 KRs, each measuring a different important dimension of success |
| 4   | KRs are observable | Each KR has a real baseline, target, measurement window, and evidence source |
| 5   | KRs are not fake progress | No KR is vague, degenerate, a restatement of the Goal, or an arbitrary output count |
| 6   | KR roles are clear | Each KR is marked as a `bet`, `brake`, or `foundation`, so downstream deliverables can be sequenced correctly |
| 7   | Scope has an off-ramp | Appetite is expressed as `~N issues`, and the kill condition names an observable stop state |

If every KR is tagged `bet`, ask whether a brake or foundation KR is missing. Do not force one of each role; some shapes are honestly 2 bets + 1 foundation, or 1 bet + 2 brakes.

Report only the failing rule numbers and the shortest useful reason. Do not expose internal rubric vocabulary in the final initiative shape.

### 9. Capture or hand off the shape

Take exactly one branch:

- **Tracker binding installed**: follow the loaded tracker-capture procedure. Pass the confirmed six-field shape as the `description`, the goal/problem label as the name, and the planning/not-yet-in-cycle state. Confirm with the locator returned by that procedure.
- **No tracker binding**: emit the confirmed shape as the markdown block below. Do not attempt a tracker call.

## Initiative description template

The shape reads as a product OKR — a non-pack-author should be able to grade each KR in 30 seconds. Fill the template against the `writing-refinement` skill's `style-rules.md` and `plans-okrs.md`. Each KR's headline *is* the observable claim (no separate `state:` field). The four sub-fields use customer/business friendly names.

```markdown
**Goal:** For [who], we want to [solve problem / achieve outcome].

**Key results:**

**KR1** - [observable claim: binary pass/fail, fitness function firing, or measurable delta] *(bet|brake|foundation)*
- baseline: [current value/state]
- target: [target value/state]
- measured over: [time frame or N units]
- how we'll know: [file path / query / log / cached report / metric + system; if grader-backed, include the command that emits the verdict]

**KR2** - [observable claim] *(bet|brake|foundation)*
- baseline: ...
- target: ...
- measured over: ...
- how we'll know: ...

**KR3** - [observable claim] *(bet|brake|foundation)*
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

The skill is complete when the Step 6b writing-editor pass returns `accept` or `accept with notes`, Step 8 passes, and Step 9 has either recorded the shape through the bound tracker procedure or emitted the filled markdown block.

## Related

- `delivery-shape`: downstream; shapes a confirmed initiative into deliverables, nodes, and tasks.
- `writing-refinement`: prose skill the Goal and KRs are written and reviewed against (`references/plans-okrs.md`, `style-rules.md`).
- `agents/writing-editor/AGENT.md`: the writing-editor persona dispatched at Step 6b.
- `references/initiative-types.md`: six-type taxonomy, Objective shapes, default KR mixes, and anti-patterns.
- `references/kr-quality-templates.md`: Layer 1 dimensions, Layer 2 templates, KR roles, and grader-backed KR patterns.
- `references/task-sizing.md`: model-tier routing rubric.
- Tracker capture and cycle model: owned by the Workflow pack when installed.
