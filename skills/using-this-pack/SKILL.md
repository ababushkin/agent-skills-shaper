---
name: using-this-pack
description: >
  Meta-skill for navigating Shaper. Identifies which skill applies to the current task
  and explains the core operating behaviours that apply across all skills. Load at session
  start or when uncertain which skill to invoke.
---

# Using this pack

## Purpose

This skill is the entry point to Shaper. It answers "which skill should I invoke right now?" and defines the operating behaviours that apply to every skill in the pack. Load it at the start of a product or engineering session, or when you're uncertain which skill fires for the current task.

## Skill discovery

Shaper has four phase skills and a set of utilities. Identify the current task and follow the first matching branch.

```
Task arrives
    │
    ├── An idea arrived — worth pursuing?                   → idea
    │       └── Unknown blocks commitment?                  → shape:design (spike track)
    │
    ├── Committed initiative — how to build it?             → shape:design (design-doc track)
    │       └── Plan/spec/design — should I trust it?       → plan-review
    │
    ├── Shaped initiative — break it into tasks?            → delivery
    │
    └── Linear issue in hand — pick it up and ship it?     → exec:pickup
            ├── Stuck on a failing test or behaviour?       → debugging
            ├── Need to review diff before Done?            → execution-review
            ├── Need to verify AC before closing?          → verify-implementation
            ├── Need to render an artefact for review?     → render-html
            └── Implementation is heavy — simplify it?     → simplify
```

Rules and references are not skills — they are loaded as context.

| Load this | When |
|---|---|
| `PRODUCT_RULES.md` | Any product decision or idea evaluation |
| `eng-principles-universal.md` | Any engineering design or build work |
| `eng-principles-agentic.md` | Any agent-driven engineering work (alongside universal) |
| Reference files | When a skill explicitly invokes one |

## How skills chain

**From idea to shipped:**
```
idea arrives → idea → shape:design → delivery → exec:pickup → done
```

**When a plan carries risk:**
```
shape:design → plan-review → delivery → exec:pickup
```

**Every PR:** `stop-the-line` hook fires automatically on PR open/update — no manual invocation.

The rule files (`eng-principles-universal.md`, `eng-principles-agentic.md`) and the `stop-the-line` hook apply throughout execution regardless of which skill is active.

## Core operating behaviours

These apply across every skill in the pack. They are not optional.

**Surface assumptions before acting.** Before any non-trivial action, state the assumptions being made and give the owner a chance to correct them. Wrong assumptions caught early are cheap; wrong assumptions caught after implementation are expensive.

**Stop at gates.** Each skill contains numbered gates (`[GATE]`). A gate is a hard stop — do not proceed past it until the gate condition is met. Gates exist because the work that follows them is wasted if the gate condition is false.

**Scope discipline.** Touch only what the current skill requires. Do not refactor adjacent code, remove things you don't understand, or add features not in the spec. Every deviation from scope requires explicit owner approval.

**Confirm before destructive action.** Deletion, reset, overwrite, force-push, dropping a table — pause and confirm with the owner before proceeding.

**Incomplete is not done.** A task is not complete until its verification criteria pass. "Seems right" is never sufficient. Evidence is required: passing tests, build output, measurement.

**Disagreement is required.** If an approach has a clear problem, name it, quantify the downside, and propose an alternative. Accept the owner's final decision.

## Quick reference

| Skill | Trigger phrase | Key output |
|---|---|---|
| `idea` | "We should build…", "A customer asked for…", "Competitor just launched…" | Triage record with ICE score and routing decision |
| `shape:design` | "How should we build X?", "Architecture for Y", "Spike on", "Let's prototype this" | Design doc, spike recommendation, or prototype finding |
| `delivery` | "Turn this initiative into tasks", "Decompose this", "Plan the delivery" | Delivery hierarchy with deliverables, nodes, and tasks |
| `exec:pickup` | "Pick up this issue", "Start this task", "Drain this ticket" | Shipped PR with review-summary comment on the Linear issue |
| `plan-review` | "Review this plan", "Before I approve", "What's missing here" | Review record with APPROVE / REVISE / KILL recommendation |
| `render-html` | "Render this doc as HTML", "Make this reviewable", "Share this for review" | Self-contained HTML file next to the source |
| `execution-review` | "Review this diff", "Run execution review", "Review before Done" | GO/NO-GO verdict with deduped findings |
| `verify-implementation` | "Verify this is done", "Check AC before marking Done" | Pass/fail verdict per AC item |

## Related

- `rules/PRODUCT_RULES.md` — ten product principles; load for any product decision
- `rules/eng-principles-universal.md` — universal engineering principles; load for any design or build work
- `rules/eng-principles-agentic.md` — agent-specific principles; load alongside universal for agent-driven work
- `skills/idea/SKILL.md` — idea intake and scoring
- `skills/design/SKILL.md` — design doc, backend spike, product spike
- `skills/delivery/SKILL.md` — delivery hierarchy from initiative to tasks
- `skills/exec-pickup/SKILL.md` — front door for draining a Linear issue
- `hooks/stop-the-line/HOOK.md` — fires on every PR; no manual invocation required
