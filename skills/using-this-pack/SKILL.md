---
name: using-this-pack
description: >
  Meta-skill for navigating Shaper. Identifies which skill applies to the current task
  and explains the core operating behaviours that apply across all skills. Load at session
  start or when uncertain which skill to invoke.
pack: meta
lifecycle_stage: all
length_target: 120–160
author: Anton Babushkin
# meta-pack skills are exempt from principles_implemented and predecessor — see docs/skill-anatomy.md
---

# Using this pack

## Purpose

This skill is the entry point to Shaper. It answers "which skill should I invoke right now?" and defines the operating behaviours that apply to every skill in the pack. Load it at the start of a product or engineering session, or when you're uncertain which skill fires for the current task.

## Skill discovery

Identify the current task and follow the first matching branch.

```
Task arrives
    │
    ├── An idea arrived — worth pursuing?                  → idea-triage
    │       ├── Confidence ≥ 5: file in idea bank          (wait — no action until roadmap-shape runs)
    │       │       └── Idea bank needs review/curation?   → backlog-manage
    │       └── Confidence < 5: validation slot
    │               ├── product feel unknown               → shape:design (product-spike track)
    │               ├── customer reality unknown           → interview / survey
    │               ├── market signal unknown              → smoke test
    │               └── technical feasibility unknown     → shape:design (backend-spike track)
    ├── Managing the idea bank or KTLO list?               → backlog-manage
    │       └── Idea bank clean — ready to plan?           → roadmap-shape
    ├── Building or reviewing a roadmap?                   → roadmap-shape
    │       └── reads from idea bank (docs/idea-bank/)
    ├── Committed initiative (goal + KRs) exists?          → delivery-shape
    ├── Significant engineering work — how to build it?   → shape:design (design-doc track)
    ├── Have a plan/spec/design — should I trust it?       → plan-review
    └── Agent signals it's done?                          → stop-the-line (hook — fires on claims)
```

Rules and references are not skills — they are loaded as context.

| Load this | When |
|---|---|
| `PRODUCT_RULES.md` | Any product decision, roadmap work, idea evaluation |
| `eng-principles-universal.md` | Any engineering design or build work |
| `eng-principles-agentic.md` | Any agent-driven engineering work (alongside universal) |
| Reference files | When a skill explicitly invokes one |

## Core operating behaviours

These apply across every skill in the pack. They are not optional.

**Surface assumptions before acting.** Before any non-trivial action, state the assumptions being made and give the owner a chance to correct them. Wrong assumptions caught early are cheap; wrong assumptions caught after implementation are expensive.

**Stop at gates.** Each skill contains numbered gates (`[GATE]`). A gate is a hard stop — do not proceed past it until the gate condition is met. Gates exist because the work that follows them is wasted if the gate condition is false.

**Scope discipline.** Touch only what the current skill requires. Do not refactor adjacent code, remove things you don't understand, or add features not in the spec. Every deviation from scope requires explicit owner approval.

**Confirm before destructive action.** Deletion, reset, overwrite, force-push, dropping a table — pause and confirm with the owner before proceeding. The cost of confirmation is one message; the cost of an unintended destructive action can be days of recovery.

**Incomplete is not done.** A task is not complete until its verification criteria pass. "Seems right" is never sufficient. Evidence is required: passing tests, build output, measurement.

**Disagreement is required.** If an approach has a clear problem, name it, quantify the downside, and propose an alternative. Accept the owner's final decision. Sycophantic agreement with a bad plan is a worse failure mode than honest pushback.

## Common mistake: skipping skills

Skills are not ceremony — they encode the checks that prevent the most common and expensive failure modes. Skipping idea-triage produces a roadmap full of unvalidated opinions. Skipping shape:design produces implementations that solve the wrong problem or the right problem in an unmaintainable way. Skipping delivery-shape produces a task list with no outcome trace and no per-node completion framing.

The value of a skill is highest the first time you skip it and something breaks. After that, the cost of not skipping it is obvious.

## How skills chain

Most work spans more than one skill. These are the common sequences:

**Product track — from idea to roadmap:**
```
idea arrives → idea-triage → idea bank (confidence ≥ 5)
                           → validation slot (confidence < 5) → shape:design → re-score
idea bank clean → backlog-manage → roadmap-shape
```

**Engineering track — from design to delivery plan:**
```
significant work → shape:design → delivery-shape → [hand off to your build skill]
unknown risk    → shape:design (backend-spike track) → shape:design (design-doc track) → delivery-shape → [hand off]
```

**Every PR:** `stop-the-line` hook fires automatically on PR open/update — no manual invocation.

Skills at adjacent stages hand off directly: idea-triage records are read by backlog-manage, which feeds roadmap-shape; design-doc output feeds delivery-shape, whose delivery hierarchy feeds whichever build skill the team uses. Following the chain is not optional — jumping ahead skips the checks that catch expensive errors early. The persistent rule files (`eng-principles-universal.md`, `eng-principles-agentic.md`) and the `stop-the-line` hook keep applying during execution regardless of which build skill picks up the work.

## Quick reference

| Skill | Trigger phrase | Key output |
|---|---|---|
| `idea-triage` | "We should build…", "A customer asked for…", "Competitor just launched…" | Triage record with ICE score and routing decision (idea bank or validation slot) |
| `backlog-manage` | "Review the backlog", "Add to KTLO", "Promote this idea", "Kill this" | Updated idea bank records + KTLO list |
| `shape:design` | "How should we build X?", "Architecture for Y", "What's the right threshold for", "Let's prototype this", "Spike on" | Design doc, spike recommendation, or prototype finding (routed by dominant unknown) |
| `roadmap-shape` | "Let's do planning", "What should we build next?", "Review the roadmap" | Shaped Now/Next/Later roadmap with explicit capacity allocation |
| `delivery-shape` | "Turn this initiative into a delivery plan", "Decompose this initiative", "Plan the delivery" | Delivery hierarchy with deliverables, nodes, and tasks; outcomes traced to KRs |
| `plan-review` | "Review this plan", "Before I approve", "What's missing here", "Should we go with this" | Review record with APPROVE / REVISE / KILL recommendation |
| `stop-the-line` | Fires on PR open/update — catches signal-suppression moves | Completion verified or halt raised |

## References

- `rules/PRODUCT_RULES.md` — the ten product principles and operational rules; load for any product decision or roadmap work
- `rules/eng-principles-universal.md` — universal engineering principles; load for any design or build work
- `rules/eng-principles-agentic.md` — agent-specific principles; load alongside universal for any agent-driven implementation
- `skills/idea-triage/SKILL.md` — first product skill; intake gate for new ideas
- `skills/app-calibrate/SKILL.md` — creates/updates baseline metrics file; run before idea-triage on improvement-type ideas
- `skills/design/SKILL.md` — entry point for all pre-implementation shaping (design doc, backend spike, product spike)
- `hooks/stop-the-line/HOOK.md` — fires on every PR; no manual invocation required
