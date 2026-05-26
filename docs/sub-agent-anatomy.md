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
  - source: <eng-universal | eng-agentic | roadmap | product>
    id: <principle or rule id>
    bucket: sub-agent
length_target: <e.g. 150-200>
author: Anton Babushkin
predecessor:
  repo: <URL or "none">
  skill: <skill name in source repo, or "none">
  relation: <derivative | adjacent | new>
kept_from_predecessor: <list, or "n/a">
changed_from_predecessor: <list, or "n/a">
---
```

## Sections

In this exact order:

1. **Title** — `# <Persona Name>`
2. **Purpose** — one paragraph: what this review catches and why the original agent can't
3. **Review posture** — the stance this persona takes (adversarial, fresh-eyes, no investment in the original work). Names the rationalisations the original agent has structural reasons to miss.
4. **Context to load** — what files, ADRs, or specs the persona reads *before* seeing the original agent's output. The point is to form an independent view first, then check it against the work.
5. **Trigger** — when this review fires
6. **Inputs** — what the persona is given
7. **Outputs** — review verdict (`accept`, `accept with notes`, `reject`) and structured notes
8. **Workflow** — numbered steps the persona walks through
9. **Common rationalisations** — patterns the *original* agent will use that this persona is on the lookout for
10. **Red flags** — signals that warrant a `reject`
11. **Out of scope** — what other artefacts cover; this persona's specific lane
12. **References** — principles enforced

## Model tier

Every persona declares `model:` in frontmatter. The tier follows the orchestrator/worker distinction from `references/task-sizing.md`:

| Role | Tier |
|---|---|
| Orchestrating review — integrates findings across multiple axes or sub-passes | **Frontier** |
| Focused worker — one bounded review lane, single axis | **Balanced** |
| Mechanical leaf — deterministic checks with enumerable pass/fail criteria | **Fast** |

The rule of thumb: if this persona's verdict propagates to downstream decisions (the next agent acts on it), route **Frontier**. Single-axis, bounded-lane personas route **Balanced**; deterministic pass/fail checks route **Fast**. The tier mapping — `Fast = Haiku 4.5 · Balanced = Sonnet 4.6 · Frontier = Opus 4.7` — is canonical in `references/task-sizing.md`; a model bump is a one-line edit there.

## Length

Target 150–200 lines. Hard cap 250.

## Reject triggers specific to sub-agents

- `model:` field absent from frontmatter, or tier not justified against the orchestrator/worker distinction.
- Missing the "Review posture" section.
- Missing the "Context to load" section, or context loading happens after seeing the original work (this pollutes the independent view).
- The persona's lane overlaps another sub-agent's without an explicit `Out of scope` boundary.
- The persona is a thin wrapper around an existing skill rather than a genuine adversarial second pass.
- The persona's review verdict criteria reduce to "does this match my interpretation" — should be principle-grounded.

## See also

- `docs/skill-anatomy.md`, `docs/hook-anatomy.md`
- `docs/brief-template.md`
- `docs/authoring-learnings.md`
