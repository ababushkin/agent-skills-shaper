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
length_target: 200–300
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
- **Type 2 (personal product, single-user)** — correctness KR (lagging) + no-silent-failure KR (committed) + maintenance-burden KR (committed). Availability KR optional 4th when scheduled-job completion is the central guarantee. Growth, MAU, retention KRs are categorically inapplicable — there is one user.
- **Type 3 (utility skill pack)** — first-shot correctness KR (aspirational, lagging) + coverage KR (committed) + use-log discipline KR (committed). Domain-specific quality KR (pricing accuracy, print acceptance, sale outcome) optional 4th when the pack has a quantifiable downstream signal. Use-log discipline is non-negotiable — every invocation must be logged at the moment of use to a named location (e.g. `listings/`, `outputs/`, `runs/`) with input, generated artefact, final-posted artefact, and edit-or-not outcome, or the lagging first-shot correctness KR is ungradable. Time-to-result KRs are usually vanity for Type 3 — only include if speed is the named bottleneck.
- **Type 4 (research / thesis-driven)** — knowledge-claim KR (committed) + critique-survivability KR (aspirational, lagging) + source-discipline KR (committed). Adoption KR (paying audience engagement, validated buyer interest) is a later-stage 4th — defer until critique-survivability has held. Readership of an undefended thesis is noise; "publish N essays" or "N readers" KRs are output, not defensibility. See Type 4 playbook in `references/initiative-types.md`.
- **Type 5 (equity research tooling)** — pre-registration KR (committed) + calibration KR (aspirational, lagging) + hit-rate KR (aspirational, lagging). Decision-quality KR (per-call postmortem) optional 4th when the cycle window covers prior 12-month outcomes. Pre-registration is non-negotiable — every BUY/WATCH/AVOID call must be written to a dated, immutable artefact (cached `reports/TICKER_YYYYMMDD.json` + git history) before outcomes are visible, or the lagging KRs are ungradable. This is the Tetlock standard: calibration over a portfolio of pre-registered calls beats accuracy on any single name.
- **Type 6 (production / customer-facing)** — activation/retention/conversion KR (aspirational, lagging) + quality-pair KR (committed — NPS, p95 latency, error rate, or support volume per user) + telemetry-discipline KR (committed). Growth without a paired quality counterweight is the canonical failure mode — every value KR must have a paired quality KR. Telemetry must be in place before the cycle starts (no telemetry = no Type 6 KR); "ship feature X to 100% of users" and un-paired MAU/DAU KRs are Cagan's canonical output-disguised-as-outcome. See Type 6 playbook in `references/initiative-types.md`.

Then ask explicitly. Do not infer. Wait for a response before synthesising.

- **Who is affected?** Which users, operators, or contexts does this problem touch?
- **What's the negative outcome if this isn't solved?** What task fails, what decision can't be made, what workflow breaks?
- **What 3 observable states would tell you it worked?** (Cap at 5; default 3 — per Wodtke.) Each one should be something a future agent can verify by looking at the system — a binary pass/fail, a fitness function firing, or a measurable delta. Avoid "improve X" / "better Y" language and avoid arbitrary "run N times" thresholds. **For all six types, propose the default mix from the playbook (Type 1: invocation-rate + decision-quality + anti-output guard; Type 2: correctness + no-silent-failure + maintenance-burden, with availability as an optional 4th; Type 3: first-shot correctness + coverage + use-log discipline, with domain-specific quality as an optional 4th — and never omit the use-log discipline KR for Type 3, and require the use-log location be named as a file path or directory in the KR's source field; Type 4: knowledge-claim + critique-survivability + source-discipline, with adoption as a later-stage 4th — defer adoption KRs until critique-survivability has held; Type 5: pre-registration + calibration + hit-rate, with decision-quality postmortem as an optional 4th — and never omit the pre-registration KR for Type 5; Type 6: activation/retention/conversion + quality-pair + telemetry-discipline — every value KR must have a paired quality KR, and telemetry must be in place before the cycle starts) and ask the user to confirm or reshape — do not start from a blank page when a playbook applies.**
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

**6.5. [GATE] Verification rubric — 10 cross-cutting rules.**
Run the following checks against the confirmed draft. Each rule is a binary pass/fail. Any failure returns the draft to Step 5 for repair — the Linear project is NOT created until all 10 pass.

| # | Rule | Pass condition |
|---|---|---|
| 1 | All six fields present | Goal / Key results / Affected repos / Appetite / Kill condition / Project type are all non-empty |
| 2 | Goal names who + outcome | Sentence contains an affected party and a desired outcome — no solution verb ("build", "add", "integrate", "ship") |
| 3 | Initiative name is a goal/problem | Name does not open with a solution verb ("Build X", "Add Y", "Integrate Z") |
| 4 | At least 3 KRs, no more than 5 | KR count ≥ 3 and ≤ 5 |
| 5 | Every KR is an observable state | No KR contains "improve", "better", "enhance", or arbitrary count thresholds without a correctness or quality dimension |
| 6 | Every KR has all four sub-fields | Each KR has baseline, target, window, source — none blank or "TBD" |
| 7 | Every KR is tagged | Each KR carries exactly one of `[committed]` or `[aspirational]` |
| 8 | Kill condition is present | Non-empty; names an observable state, not a vague clause ("if it doesn't work") |
| 9 | Project type is canonical | One of: 1, 2, 3, 4, 5, or 6 — not free text |
| 10 | Appetite is in issues | Expressed as "~N issues" — not days, weeks, or sprints |

Report each failing rule by number with the specific text that triggered the failure. When all 10 pass, proceed to Step 7.

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
| "Let's add user registration so we can onboard people to [personal product]." | Type 2 is single-user by definition — no users to register. If signup is genuinely the work, the initiative is Type 6 (production / customer-facing), not Type 2 — re-classify before proceeding. |
| "Let's set a KR to increase MAU / DAU / retention on the personal app." | Categorically inapplicable to Type 2. There is one user. The dimensions that matter are correctness, no-silent-failure, and maintenance burden — growth KRs belong to Type 6. See Type 2 playbook in `references/initiative-types.md`. |
| "We just need to add more skills to the pack this cycle — wider coverage is the win." | For utility skill packs (Type 3), volume of skills is output, not outcome. Success is first-shot correctness of the artefact and coverage of the categories the user actually encounters end-to-end. Five more skills with no use-log produce zero graded improvement. Reshape into first-shot correctness + coverage KRs over the categories actually hit — see Type 3 playbook in `references/initiative-types.md`. |
| "Let's run `/resell-au` N times this cycle as a usage drive." | Activity vanity. Twenty invocations with bad outputs is failure, not progress. Type 3 grades on the quality of each artefact, not the count of them. Reshape into a first-shot correctness KR ("≥X of next N posted without text edits") over the invocations you would have made anyway. |
| "Skip the use-log — I'll remember which invocations went well." | Memory is selective recall of the wins. Without immutable per-invocation capture at the moment of use — input, generated artefact, final-posted artefact, edit-or-not outcome — the lagging first-shot correctness KR collapses into a vibe check. For Type 3, the use-log discipline KR is non-negotiable, parallel to Type 5's pre-registration KR. Name the use-log location as a file path or directory in the KR's source field. |
| "Let's run `/stock-screen` on a bunch of new tickers this cycle." | Type 5 grades on calibration, not throughput. Twenty new screens with no pre-registration produce twenty unrecorded opinions, not twenty results. Reshape into a pre-registration KR over the names you actually call — see Type 5 playbook in `references/initiative-types.md`. |
| "We'll just check that BUY calls outperform the S&P over the next year." | Un-pre-registered and cherry-pickable. Without a dated, immutable set of names locked at call time, "outperform" becomes whatever cherry-picked window the analyst chooses post-hoc. Reshape into a hit-rate KR over the explicit pre-registered cohort and add a pre-registration KR (committed) to lock the cohort. |
| "Skip the pre-registration KR for the equity initiative — we already write reports per call." | Writing reports is not pre-registration. Pre-registration means the call is dated, committed to git, and immutable before the 12-month window closes. Without the immutability check, the lagging calibration and hit-rate KRs are arguments about what was meant, not checks of what was claimed (Tetlock). For Type 5, the pre-registration KR is non-negotiable. |
| "We just need to publish N essays this cycle to ground the thesis." | For research/thesis-driven (Type 4), essay count is output, not defensibility. A thesis with 20 unsourced essays is weaker than one with 3 source-backed claims that hold under critique. Reshape into knowledge-claim + critique-survivability KRs — see Type 4 playbook in `references/initiative-types.md`. |
| "Let's set a KR for N readers / N newsletter subscribers on the thesis." | Adoption masquerading as outcome on an undefended thesis. Readership of a thesis that hasn't cleared expert critique is noise — it tells you the headline is catchy, not that the assertions are right. Defer adoption KRs until critique-survivability has held; otherwise the wrong audience signal entrenches a wrong thesis. |
| "Just ship feature X to 100% of users this cycle as the win." | Cagan's canonical output-disguised-as-outcome for Type 6. Rollout is implementation; the OKR scores whether the customer behaviour the feature was supposed to change actually moved. Reshape into a behaviour-change KR (activation/retention/conversion) with a paired quality KR — see Type 6 playbook in `references/initiative-types.md`. |
| "Let's set a KR to increase MAU / DAU." | Type 6 value KR without a paired quality KR is half a KR. MAU can be inflated by re-engagement emails that crater NPS, or by registration prompts that bloat the denominator. Every growth KR is paired with a quality counterweight (NPS, retention, churn, support-per-user) — the pair is what makes the vanity-gain trade visible. |
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
- For Type 2 (personal product, single-user), any KR targets growth metrics (MAU, DAU, retention, signups) or feature volume — the type was misclassified, or growth metrics were imported from a product model that doesn't apply.
- For Type 3 (utility skill pack), every KR scores skill volume ("N skills authored") or invocation count ("run N times this cycle") — the OKR is measuring output, not utility. Reshape into first-shot correctness (≤ one edit before posting/printing) and coverage (zero unhandled categories) KRs.
- For Type 3, no use-log discipline KR (committed) and no source location named as a file path or directory for the first-shot correctness KR — the lagging KR is ungradable because there's no immutable per-invocation record to grade against.
- For Type 5 (equity research tooling), no pre-registration KR (committed) — every BUY/WATCH/AVOID call must be logged to a dated, immutable artefact (cached `reports/TICKER_YYYYMMDD.json` + git history) before outcomes are visible, or the lagging calibration and hit-rate KRs are ungradable by construction.
- For Type 5, KRs target throughput ("run `/stock-screen` on N tickers", "produce N reports") or un-pre-registered outperformance ("BUY calls beat the S&P") — Type 5 grades on calibration of dated, locked cohorts, not on volume of analyses or post-hoc cherry-picked windows.
- For Type 4 (research / thesis-driven), every KR scores essay count, reader count, or newsletter subscribers — no knowledge-claim or source-discipline KR. The OKR is measuring artefact volume or audience noise, not defensibility of the assertions.
- For Type 6 (production / customer-facing), a growth / conversion / retention KR has no paired quality KR — Cagan's canonical failure mode where the value KR is achieved by destroying NPS, latency, error rate, or support volume per user.
- For Type 6, a KR uses feature-rollout language ("ship X to 100%", "launch Y") rather than naming the customer behaviour the feature was supposed to change — the OKR is measuring delivery, not outcome.
- For Type 6, telemetry isn't in place before the cycle starts and there is no telemetry-discipline KR to instrument it — the value and quality KRs cannot be graded because the baseline can't be read and definitions can drift mid-cycle.
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
10. For type=2 (personal product), at least one KR scores correctness (lagging) and at least one KR scores operability (no-silent-failure, maintenance-burden, or availability) — the OKR is not measuring feature volume or growth metrics that don't apply.
11. For type=3 (utility skill pack), at least one KR is a first-shot correctness KR (aspirational, lagging — ≥X of next N artefacts used without text edits) AND at least one KR is a use-log discipline KR (committed) naming the use-log location as a file path or directory in its source field — the OKR is gradable post-hoc from the use-log alone, without narration from the operator.
12. For type=4 (research / thesis-driven), at least one KR is a knowledge-claim KR (committed — N specific defensible assertions recorded in the thesis artefact) AND at least one KR is a source-discipline KR (committed — zero uncited load-bearing claims; sources file at a named path) — the OKR is gradable post-hoc from the thesis artefact alone, without narration from the author. Adoption KRs are absent or explicitly deferred until critique-survivability has held.
13. For type=5 (equity research tooling), at least one KR is a pre-registration KR (committed) requiring every BUY/WATCH/AVOID call to be logged to a dated, immutable artefact (cached `reports/TICKER_YYYYMMDD.json` + git history) before outcomes are visible — the OKR is gradable post-hoc by a third party from artefacts alone, without narration from the original analyst.
14. For type=6 (production / customer-facing), at least one KR is an activation/retention/conversion KR (aspirational, lagging — baseline → target on a named cohort) AND at least one KR is a paired quality KR (committed — NPS, p95 latency, error rate, or support volume per user, with a tolerance) AND at least one KR is a telemetry-discipline KR (committed — cohort + metric definitions recorded before cycle start with no retroactive edits). The OKR is gradable from production telemetry alone, without narration from the team.

## References

- `rules/linear-workflow.md` — initiative definition, lifecycle, cycle model, ops slot (source of truth; six-field shape and KR sub-field requirements)
- `rules/PRODUCT_RULES.md` — P2 (problems not solutions), P3 (bets), A2 (problem format), A3 (measurable success criteria — applied here as 3 KRs with baseline/target/window/source discipline), C1 (appetite)
- `rules/eng-principles-agentic.md` — Principle 3 (spec as seatbelt; goal must precede work)
- `references/initiative-types.md` — six-type taxonomy and per-type playbooks (Objective shape, default KR mix, anti-patterns, verification rubric) — loaded at Step 2.5 and Step 3
- Research Section 5 — 10 cross-cutting verification rules (inline copy at Step 6.5); original source: Linear document "Research and implementation plan — OKR shapes by project type", Section 5 (project `Initiative quality — type-aware OKRs with KRs`)
- `skills/idea-triage/SKILL.md` — upstream: run when confidence is low before committing to an initiative
- `skills/planning-and-task-breakdown/SKILL.md` — downstream: breaks a confirmed initiative into issues
