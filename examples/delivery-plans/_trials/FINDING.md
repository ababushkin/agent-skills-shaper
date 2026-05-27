# Experiment finding: delivery-shape framing baked in (N07 self-trial)

Date: 2026-05-28
Node: N07 (`experiment`, `acceptance: true`, `verifies_parent: D2`) — this finding is **D2's Done
condition** (KR2 of the top-down-delivery-planning initiative).
Discipline: `product-spike` (experiment — hypothesis, success metric, written finding).
Appetite: 2 trial iterations. Used: 2.

## Question (hypothesis)

When `delivery-shape` is followed against an initiative's **goal + KRs only**, does the emitted
plan carry **acceptance criteria on every `story` node** and **at least one `skeleton`-flagged
task** — passing `bin/check-plan-framing` on first emission, with **zero framing re-prompts**?

## Success metric

2 / 2 trial initiatives pass `bin/check-plan-framing` (AC on every story + ≥1 skeleton task) at 0
re-prompts. `< 2/2`, or any re-prompt, **falsifies** the bet.

**Re-prompt, operationally:** any case where `check-plan-framing` failed on first emission and a
framing element (a missing AC block, a missing/mis-ordered skeleton task) had to be added in
response. A pass on first run = 0 re-prompts. The plan file-set was written by following the
skill's workflow end-to-end; the gate was then run **once** per trial — no peek-and-fix loop before
the recorded run. Stated precisely, "0 re-prompts" means *an agent following the skill's numbered
steps produced a gate-passing plan with no observed correction* — not that framing is impossible to
drop (see threat to validity).

## Approach

Two already-shaped Linear initiatives were chosen — deliberately from **different domains**, so a
pass can't be explained by domain familiarity alone:

| Trial | Initiative | Domain | Why chosen |
|-------|-----------|--------|-----------|
| 1 | [Per-task model routing](https://linear.app/ababushkin/project/per-task-model-routing-deliberate-not-ad-hoc-e64047e1cdf9) | methodology skill pack (in-domain) | shaped & ready; closest analog to delivery-shape's own subject matter |
| 2 | [Pipeline recovery without the database console](https://linear.app/ababushkin/project/pipeline-recovery-without-the-database-console-628d938363fa) | nestl production software (out-of-domain) | tougher test; trips Rule A1 (shared state machine, production-data mutation) and a window-bound KR |

For each, the initiative's goal + KRs (only) were fed through the `delivery-shape` workflow,
emitting a file-set under `_trials/<slug>/`. Mode: throwaway artefact — the file-sets are the
instrument that grades the skill, **not** operative delivery plans for those initiatives (each
README carries a "trial fixture, not the operative plan" banner). The single observation per trial
was `bin/check-plan-framing` (the success metric); `bin/walk-delivery-plan` was also run (skill
step 10) for completeness.

## Observations (raw)

**Trial 1 — per-task-model-routing** (`bin/check-plan-framing` exit 0):

| Signal | Observed |
|--------|----------|
| Story nodes checked | 4 (N01, N03, N04, N05) |
| Stories carrying `## Acceptance criteria` (≥1 `Done when:`) | 4 / 4 |
| `skeleton`-flagged tasks in plan | 5 |
| Nodes placing a task before their skeleton | 0 |
| `walk-delivery-plan` manifest vs README oracle | 3 / 6 / 14 — MATCH (exit 0) |
| **Framing re-prompts** | **0** |

Node types exercised: `story` ×4, `adr` ×1, `experiment` ×1. The shaping also surfaced a point the
flat 7-issue source breakdown missed: three of its issues (thread into `initiative-shape`,
`roadmap-shape`, sub-agent convention) serve **no** KR, so delivery-shape deferred them rather than
placing output-without-a-bet on the plan (product A3). delivery-shape also emitted an `adr` node
(routing-not-cascading) the flat breakdown had no slot for — Rule A1's "a short ADR may suffice."

**Trial 2 — pipeline-recovery** (`bin/check-plan-framing` exit 0):

| Signal | Observed |
|--------|----------|
| Story nodes checked | 5 (N02, N03, N04, N05, N06) |
| Stories carrying `## Acceptance criteria` (≥1 `Done when:`) | 5 / 5 |
| `skeleton`-flagged tasks in plan | 5 |
| Nodes placing a task before their skeleton | 0 |
| `walk-delivery-plan` manifest vs README oracle | 2 / 6 / 12 — MATCH (exit 0) |
| **Framing re-prompts** | **0** |

Node types exercised: `design-doc` ×1, `story` ×5 (one carrying the `acceptance` flag). D1 tripped
a Rule A1 trigger and got a `design-doc` node as its first node, with the build nodes `Blocked by`
it — the design-doc branch fired without prompting. D2's KR2 ("zero orphaned `running` rows over a
window") is a production-soak observation no single child owns, so N06 is an `acceptance` node
(`verifies_parent: D2`) carrying a genuine non-`none` `external_window` (the 30-day soak) and
closing last — not re-running the per-category proofs in N04/N05.

**Aggregate:** 2 / 2 trials pass `bin/check-plan-framing` at **0 re-prompts**. Both walk
deterministically with manifests matching their oracles.

## Finding (interpretation)

The success metric is **met exactly**: 2/2 at 0 re-prompts. The framing the skill promises —
acceptance criteria on every story, ≥1 walking-skeleton task with foundational work folded in, no
silent pre-skeleton setup task — was present on first emission for both an in-domain and an
out-of-domain initiative. The skill's gates do the work: step 6 (AC by default) and step 7
(skeleton-first, foundational work folded into the description) produce the framing inline as each
node is written, so the mechanical gate finds nothing to flag. The harder branches not exercised by
the worked example also fired correctly under goal+KRs-only input: the Rule A1 design-doc branch
(Trial 2 / D1) and the `acceptance`-flag-with-external-window pattern (Trial 2 / N06).

**Threat to validity (recorded honestly).** This is a *self-trial*: the same agent both ran
`delivery-shape` and authored the experiment, having read the skill and the gate's source. So the
result confirms the strong, useful claim — *the skill's workflow and templates, when followed,
bake the framing in by default* — but it cannot by itself isolate "skill caused the framing" from
"agent already knew the framing." Two design choices reduce (not eliminate) that risk: the framing
was emitted by following the skill's numbered steps, not by reverse-engineering the gate; and one
trial was deliberately out-of-domain (nestl production), where domain familiarity offers no shortcut
to AC/skeleton framing. A stronger future test (a follow-on, not a blocker for this node's stated
metric) would hand goal+KRs to a *fresh* agent given only the skill and check framing blind. None
of this changes the verdict against N07's stated success metric, which is purely the
`check-plan-framing` pass at 0 re-prompts.

## Recommendation

**Confirmed** (the experiment's affirmative outcome; equivalent to product-spike *proceed*).

The D2 bet (KR2) holds: delivery-shape emits framing baked-in at 0 re-prompts across 2 already-shaped
initiatives. This finding is D2's Done condition — D2 / KR2 is observed. No reshape of D2 is needed.
Next step: close N07 (the acceptance node) last so D2's milestone reaching 100% coincides with KR2
being observed, per the contract's acceptance-flag convention. The validity caveat above is logged
as a candidate follow-up (blind fresh-agent trial), not as remediation.

## Prototype artefact (disposition)

Two trial file-sets, marked non-production trial fixtures (not operative plans), kept as committed
evidence under `_tests/`-style convention:

- [`per-task-model-routing/`](per-task-model-routing/) — 3 deliverables · 6 nodes · 14 tasks
- [`pipeline-recovery/`](pipeline-recovery/) — 2 deliverables · 6 nodes · 12 tasks

Both pass `bin/check-plan-framing` and `bin/walk-delivery-plan` (exit 0). They are retained, not
deleted, because they are the reproducible evidence behind this finding — re-running the two scripts
re-verifies the result.
