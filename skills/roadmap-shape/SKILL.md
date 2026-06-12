---
name: roadmap-shape
description: >
  Builds or reviews a roadmap using portfolio-theme classification and explicit capacity
  allocation. Use at the start of a planning cycle, during a roadmap review, or when
  new candidates need to be evaluated against current commitments.
  Trigger phrases: "let's do planning", "what should we build next?", "review the roadmap",
  "planning cycle", "what's on the roadmap".
pack: product
lifecycle_stage: decide
principles_implemented:
  - source: product
    id: A1
    bucket: embedded
  - source: product
    id: A2
    bucket: embedded
  - source: product
    id: A3
    bucket: embedded
  - source: product
    id: A4
    bucket: embedded
  - source: product
    id: A6
    bucket: embedded
  - source: product
    id: B1
    bucket: embedded
  - source: product
    id: B2
    bucket: embedded
  - source: product
    id: B3
    bucket: standalone
  - source: product
    id: B4
    bucket: embedded
  - source: product
    id: B5
    bucket: embedded
  - source: product
    id: B6
    bucket: embedded
  - source: product
    id: C1
    bucket: embedded
  - source: product
    id: C3
    bucket: standalone
length_target: 250–320
author: Anton Babushkin
predecessor:
  repo: none
  skill: none
  relation: new
kept_from_predecessor: "n/a"
changed_from_predecessor: "n/a"
---

# Roadmap shape

## Purpose

roadmap-shape is the planning skill. It takes the idea bank and strategic context as inputs and produces a Now/Next/Later roadmap with an explicit capacity allocation across portfolio themes. Its job is to make the implicit explicit: every roadmap is a portfolio of bets with a hidden theme mix and hidden capacity allocation — this skill names them out loud before committing.

The key moves this skill enforces: problems on the roadmap, not solutions (Rule A4); every item scored before it claims a slot (Rules B2, B4); low-confidence items routed to validation rather than build slots (Rule B6); capacity allocated by theme stated numerically, not just implied (Rule C3).

## When to use

- Start of a planning cycle: building a new Now/Next/Later from scratch or from the previous cycle's output.
- Mid-cycle roadmap review: new candidates have arrived or existing items need re-evaluation.
- Retrospective: checking whether the current roadmap's theme mix and capacity allocation reflect the team's stated strategy.
- When a stakeholder request needs to be evaluated against existing commitments.

## When not to use

- **A single incoming idea** — run `idea-triage` first. roadmap-shape assumes candidates have already been triaged.
- **Evaluating feasibility of a specific solution** — that is design-doc territory. roadmap-shape operates at the problem/outcome level.
- **Decomposing a committed initiative into deliverables and nodes** — that is delivery-shape territory.

## Inputs

- The idea bank (`docs/idea-bank/`): triaged ideas, each with an ICE score and routing decision.
- Current strategic priorities: stated goals the team is trying to achieve this cycle.
- Capacity: available team capacity for the cycle, by role if relevant.
- Previous roadmap (if it exists): what was committed to, what shipped, what carried over.

If any of these are missing, surface the gap before proceeding. A roadmap built without knowing the strategic priorities or available capacity is a guess, not a plan.

## Outputs

A roadmap document at `docs/roadmap.md` containing:
- Now items: concrete, fully scoped, with appetite and success criterion
- Next items: directional, validated but not yet scoped in full detail
- Later items: hypotheses and strategic optionality
- Explicit capacity allocation: % of capacity per portfolio theme, % for KTLO, % for validation
- Theme distribution table: which items belong to which theme

## Workflow

**1. Load strategic context.**
Confirm you have the current strategic priorities documented. If they are not written down anywhere, stop and ask the owner to state them before proceeding. A roadmap built without strategic priorities is a collection of opportunities with no coherent direction. The priorities do not need to be elaborate — "grow activation in the SMB segment" or "stabilise the platform for the current scale" is sufficient.

**2. List all candidates.**
Pull every item from the idea bank that is marked as ready for roadmap consideration (confidence ≥ 5, or in a validation slot). Include any items carried over from the previous cycle. Do not pre-filter — classification happens next.

**3. [GATE] Strip any solution framing.**
Read each candidate. Any item whose name or description describes a solution ("integrate Stripe," "add a dashboard," "rebuild the search UI") must be rewritten as a problem before proceeding. Apply Rule A2: "For [customer segment], we believe [problem] is causing [negative outcome]." If you cannot write the problem statement for an item, it is not ready for the roadmap. Park it in the idea bank with a note.

**4. Classify each candidate by portfolio theme (Rule B3).**
Label every candidate with one of the seven Doshi themes:

| Theme | Label |
|---|---|
| Differentiators | `diff` |
| Table-stakes | `ts` |
| Incrementals | `incr` |
| Embarrassments | `emb` |
| Customer specials | `cs` |
| Tech foundation | `tech` |
| Speculative bets | `spec` |

Produce a simple table: candidate → theme label. This is the first moment you can see the portfolio mix. Look at the distribution — does it reflect intention, or drift?

**5. Apply ICE scores (Rule B2).**
Every candidate needs an ICE score: Impact × Confidence × Ease. Use scores already in the triage records; re-score only if material new evidence has arrived since triage. Do not re-score upward because an item looks attractive during planning — that is HIPPO reasoning.

**6. [GATE] Confidence gate (Rule B6).**
Separate any candidate whose Confidence score is below 5. Those candidates do not get a build slot on the roadmap. They get a validation slot: a time-boxed discovery task whose output is higher-confidence evidence. A validation slot is on the roadmap; a build slot for a low-confidence item is not.

**7. Apply Kano classification for customer-facing items (Rule B4).**
For any candidate in `diff`, `ts`, `incr`, or `cs` that affects a customer-facing experience, classify it:

- **Must-be**: absence causes dissatisfaction; presence is invisible
- **Performance**: linear satisfaction — more is better
- **Excitement**: unexpected, disproportionate positive effect
- **Indifferent**: customers don't notice

Must-be gaps take priority over everything else in their category. A product with excitement features and unfixed must-be gaps will churn customers regardless of the delighters. Flag any must-be gap not already in the Now slot.

**8. Set capacity allocation (Rule C3).**
State explicitly what percentage of team capacity goes to each theme for this cycle, plus what percentage is reserved for KTLO and validation work. The numbers must add up to 100%. This step is often skipped because it makes uncomfortable tradeoffs visible — that is the point.

Example allocation (not a target — every team's is different):
```
Differentiators:    25%
Table-stakes:       15%
Tech foundation:    20%
Incrementals:       10%
Embarrassments:      5%
Customer specials:  10%
Speculative bets:    5%
KTLO:               10%
            Total: 100%
```

**9. Shape Now.**
Select items for Now based on: ICE score, confidence, strategic fit, and capacity allocation. For each Now item:
- Set an appetite (Rule C1): how much time is this problem worth? The appetite is a cap, not an estimate.
- Attach a success criterion (Rule A3): what metric, measured how, over what window, tells us the bet paid off?
- Confirm that solution detail is in the working documents, not the roadmap entry (Rule A4).
- Update the item's `## Routing` status in its idea bank file to `on roadmap — Now — placed YYYY-MM-DD`.

Do not fill Now beyond the available capacity. A full Now slot is a failing Now slot.

**10. Shape Next.**
Select directional candidates for Next. These are validated (confidence ≥ 5) but not yet fully scoped. Do not set appetites for Next items — the point of Now-Next-Later is that Next still has room to be reshaped as you learn. Do record the problem statement and the ICE score.
- Update each item's `## Routing` status in its idea bank file to `on roadmap — Next — placed YYYY-MM-DD`.

**11. Shape Later.**
Place remaining validated candidates and high-interest low-confidence items in Later. Later items are hypotheses, not commitments. They should feel intentionally sparse — if Later has 30 items, it is not a Later section, it is a second backlog.
- Update each item's `## Routing` status in its idea bank file to `on roadmap — Later — placed YYYY-MM-DD`.

**12. [GATE] Shape review.**
Read the shaped roadmap against the following named failure patterns:

| Pattern | Check |
|---|---|
| Customer-specials dominance | Is more than 30–35% of capacity in `cs`? If yes: name it explicitly. Is this intended? |
| Tech foundation starvation | Is `tech` at zero or near-zero? If yes: when does velocity degradation arrive? |
| Differentiators at low confidence | Are `diff` items in Now with Confidence < 7? If yes: they need more validation first. |
| No speculative bets | Is `spec` entirely absent? If yes: this is a maintenance roadmap. Is that the intent? |
| Must-be gaps unfixed | Are there Kano Must-be gaps not in Now? If yes: explain why or fix them. |
| Validation items missing | Are there low-confidence items in build slots? If yes: move them to validation slots. |

If any check fails, either fix the roadmap or document why the pattern is intentional.

**13. Write and file the roadmap.**
Use the template below. File at `docs/roadmap.md`. Write each item and milestone against the `writing-refinement` skill — `skills/writing-refinement/references/style-rules.md` and the Milestones section of `skills/writing-refinement/references/plans-okrs.md`: name milestones as summary achievements, never labels such as "Phase 1" or "Research."

**14. [GATE] Writing-editor pass.**
Before the roadmap goes to its shape review and the user, perform a writing review as a sub-agent over the drafted roadmap, using the `writing-editor` persona (`agents/writing-editor/AGENT.md`), and apply its rewrites. On `reject`, repair and re-run once, then carry any remaining notes forward as `accept with notes`.

## Roadmap template

```markdown
# Roadmap

Last updated: <date>
Cycle: <period>

## Capacity allocation

| Category | % of capacity |
|---|---|
| Differentiators | |
| Table-stakes | |
| Tech foundation | |
| Incrementals | |
| Embarrassments | |
| Customer specials | |
| Speculative bets | |
| KTLO | |
| Validation | |
| **Total** | **100%** |

## Theme distribution

| Item | Theme | ICE | Confidence | Kano | Model tier | Slot |
|---|---|---|---|---|---|---|
| | | | | | | |

## Now

### [Item name]
**Problem:** For [customer segment], we believe [problem] is causing [negative outcome].
**Success criterion:** [metric] moves from [baseline] to [target] within [window], measured by [method].
**Appetite:** [time budget] — this is a cap, not an estimate.
**Theme:** [portfolio theme]
**ICE:** [I×C×E]

## Next

### [Item name]
**Problem:** For [customer segment], we believe [problem] is causing [negative outcome].
**Theme:** [portfolio theme]
**ICE:** [I×C×E]

## Later

### [Item name]
**Problem / hypothesis:** [one sentence]
**Theme:** [portfolio theme]

## Validation slots

### [Item name]
**Hypothesis:** [what we're trying to learn]
**Validation method:** [customer interview / smoke test / experiment / prototype test]
**Confidence target:** raise from [current] to [target] before scheduling as a build slot

## Shape review

| Pattern | Status | Notes |
|---|---|---|
| Customer-specials dominance | [ok / flagged] | |
| Tech foundation starvation | [ok / flagged] | |
| Differentiators at low confidence | [ok / flagged] | |
| No speculative bets | [ok / flagged] | |
| Must-be gaps unfixed | [ok / flagged] | |
| Validation items in build slots | [ok / flagged] | |
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "We know our priorities — we don't need to classify by theme." | Classification takes 10 minutes. It surfaces the portfolio mix you already have but haven't named. The value is in seeing it, not in the labelling itself. |
| "The capacity allocation will just be what it ends up being." | Implicit allocation is how roadmaps drift to 60% customer specials. The allocation doesn't need to be precise; it needs to be stated before work begins, not inferred after the cycle ends. |
| "This item is high impact — the confidence score doesn't matter yet." | Impact × Confidence × Ease. A high Impact score with a 0.1 Confidence score is a 0.3 ICE score. Confidence matters. Route to validation and raise it. |
| "Now is full but this item is urgent." | 'Urgent' is a cost-of-delay argument (Rule B5). Name the actual cost of delay: revenue, churn, competitive position, a deadline. If the cost is real, displace something from Now explicitly. Do not add to a full Now slot. |
| "Later is where we park things we're not sure about." | Later is not a parking lot (Rule A6). Items in Later are strategic hypotheses. Unvalidated ideas with no strategic rationale go in the idea bank. |

## Red flags

- Items in Now have no success criterion.
- Items in Now are framed as solutions ("build X", "add Y") rather than problems.
- Capacity allocation section is missing or doesn't add to 100%.
- Customer specials occupy >35% of capacity without an explicit statement that this is intended.
- Low-confidence items (< 5) appear in build slots rather than validation slots.
- Must-be gaps exist and are not in Now.
- The shape review section is skipped or all rows are marked "ok" without explanation.

## Verification / exit criteria

The skill has run correctly when:

1. A roadmap document exists at `docs/roadmap.md`.
2. Every Now item has: a problem statement (Rule A2 format), a success criterion (Rule A3), and an appetite (Rule C1).
3. Every candidate has a portfolio theme label and an ICE score.
4. Capacity allocation is stated and adds to 100%.
5. All items with Confidence < 5 are in validation slots, not build slots.
6. The shape review table is complete and any flagged pattern has a note.
7. The Step 14 writing-editor pass returned `accept` or `accept with notes`.

## References

- `rules/PRODUCT_RULES.md` — A1 (time horizons), A2 (problem framing), A3 (success criteria), A4 (solutions held loosely), A6 (no parking lot), B1–B7 (prioritisation), C1 (appetite), C3 (explicit capacity allocation)
- `references/portfolio-themes.md` — Doshi's seven themes, capacity allocation patterns, anti-patterns
- `references/confidence-meter.md` — Gilad's scale for evidence quality scoring
- `references/ice-scoring.md` — ICE = Impact × Confidence × Ease mechanics
- `references/kano-classification.md` — five-category feature taxonomy for customer-facing work
- `references/task-sizing.md` — model tier / risk routing rubric for roadmap item prioritisation
- `writing-refinement` — prose skill items and milestones are written and reviewed against (`references/plans-okrs.md`, `style-rules.md`)
- `agents/writing-editor/AGENT.md` — the writing-editor persona dispatched at Step 14
- Janna Bastow — Now-Next-Later roadmap format
- Ryan Singer — "Shape Up" (appetite and fixed-time planning)
- Shreyas Doshi — portfolio themes framework
