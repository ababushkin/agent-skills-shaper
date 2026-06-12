# Sub-agent persona anatomy

The authoring spec for sub-agent personas in `agents/<name>/`.

Sub-agent personas are review passes invoked with fresh context. They are the right tool when judgement is required and the original agent has structural reasons not to catch its own failure (it claimed success, it picked the exciting tech, it solved the easier problem). They are the wrong tool for mechanical checks (use a hook) or for general guidance (embed the principle in the relevant skill).

## Frontmatter

```yaml
---
name: <agent-name>
description: <1-2 sentences>
category: sub-agent
pack: <product | engineering | meta>
review_target: <design-doc | implementation | spec | other>
model: <Fast|Balanced|Frontier>
principles_implemented:
  - source: <eng-universal | eng-agentic | roadmap | product | writing-refinement | ...>
    id: <principle or rule id, or "all">
    bucket: sub-agent
author: Anton Babushkin
---
```

Add a `predecessor` block (`repo`, `skill`, `relation`, plus `kept_from_predecessor` / `changed_from_predecessor`) **only when the persona is ported from another pack**, to record provenance. A net-new persona omits it — `relation: new` with everything else `n/a` is noise. There is no `length_target` field; the length guidance below is the only target.

## Sections

A persona keeps the canonical order, but only the **required** sections are mandatory. Include an **optional** section only when it carries content not already in a required section or in a skill the persona defers to. Restating, for example, a Workflow that a cited skill's review mode already owns is a reject trigger, not thoroughness.

**Required** (omitting any is a reject):

1. **Title** — `# <Persona Name>`
2. **Purpose** — one paragraph: what this review catches and why the original agent can't
3. **Review posture** — the stance (adversarial, fresh-eyes, no investment in the original work). Names the rationalisations the original agent has structural reasons to miss, and the clean-`accept`-is-suspect rule.
4. **Context to load** — what files, ADRs, or specs the persona reads *before* seeing the original agent's output, to form an independent view first.
5. **Outputs** — review verdict (`accept`, `accept with notes`, `reject`) and the structured-notes shape.
6. **Out of scope** — what other artefacts cover; this persona's specific lane.
7. **References** — principles and source files enforced.

**Optional** (include when, and only when, they add non-redundant content):

- **Trigger** — when this review fires, if not obvious from Purpose.
- **Inputs** — what the persona is given, if more than Context-to-load and Trigger already imply.
- **Workflow** — numbered steps, **only when the persona is self-contained**. A persona that defers its steps to a cited skill's review mode omits this.
- **Common rationalisations** — the excuses the *original* agent makes, as a table with counters. Strongly recommended: this adversarial priming is often the main reason to dispatch a persona over running a skill's review mode inline.
- **Red flags** — `reject` signals, only where not already covered by Outputs or Workflow.

## Model tier

Every persona declares `model:` in frontmatter. The tier follows the orchestrator/worker distinction from `references/task-sizing.md`:

| Role | Tier |
|---|---|
| Orchestrating review — integrates findings across multiple axes or sub-passes | **Frontier** |
| Focused worker — one bounded review lane, single axis | **Balanced** |
| Mechanical leaf — deterministic checks with enumerable pass/fail criteria | **Fast** |

The rule of thumb: if this persona's verdict propagates to downstream decisions (the next agent acts on it), route **Frontier**. Single-axis, bounded-lane personas route **Balanced**; deterministic pass/fail checks route **Fast**. The tier mapping — `Fast = Haiku 4.5 · Balanced = Sonnet 4.6 · Frontier = Opus 4.7` — is canonical in `references/task-sizing.md`; a model bump is a one-line edit there.

## Length

Target under 120 lines. Hard cap 150. A persona over the cap is usually restating rules that belong in a skill or reference — cut to the required sections and the optional ones that earn their place.

## Reject triggers specific to sub-agents

- `model:` field absent from frontmatter, or tier not justified against the orchestrator/worker distinction.
- Missing any required section: Review posture, Context to load, Outputs, Out of scope, References.
- Context loading happens after seeing the original work (this pollutes the independent view).
- The persona's lane overlaps another sub-agent's without an explicit `Out of scope` boundary.
- The persona is a thin wrapper around an existing skill rather than a genuine adversarial second pass.
- An optional section restates content a cited skill or reference already owns (e.g. a Workflow duplicating a skill's review-mode steps).
- The persona's review verdict criteria reduce to "does this match my interpretation" — should be principle-grounded.

## See also

- `docs/skill-anatomy.md`, `docs/hook-anatomy.md`
- `docs/brief-template.md`
- `docs/authoring-learnings.md`
