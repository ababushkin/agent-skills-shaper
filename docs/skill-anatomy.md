# Skill anatomy

The authoring spec for `SKILL.md` files in `skills/<name>/`.

## Frontmatter

```yaml
---
name: <skill-name>
description: <1-2 sentences. State what the skill does, then "Use when …", then trigger phrases.>
---
```

Taxonomy the dropped fields used to carry (pack, lifecycle stage, predecessor) is preserved in the README tables and git history, not in the file.

## Sections

In this exact order:

1. **Title** — `# <Skill Name>`
2. **Purpose** — one or two plain sentences: what the skill does and the one thing that must hold. No "without it…" doom paragraph, no inline principle citations.
3. **When to use** — tight bullets; explicit intents, with the size-the-work rubric where relevant
4. **Do not use when** — tight bullets; explicit non-triggers, each naming the right alternative inline
5. **Inputs** — what the skill expects to be given
6. **Outputs** — what it produces, including any artefact path; show the record/verdict shape as a fenced `json` block where the skill emits one
7. **Workflow** — `### N. <step>` headers. A hard gate is a `### N. Gate: <name>` header — the gate semantics are mandatory; only the literal `[GATE]` marker is replaced by the `Gate:` heading
8. **Artefact template** — the markdown (or JSON) the skill produces, as a fenced block
9. **Red flags** — bullet list of signs the skill is being violated
10. **Exit criteria** — how to know the skill ran correctly
11. **Related** — plain links to sibling skills and references; no principle-citation footnotes

## Length

Target 100–300 lines. Below 100, editor checks for under-specification (acceptable if genuinely complete). Above 300, editor checks for redundancy with other skills, scope creep, or over-explanation. Hard cap 350 lines; beyond that, split.

## Artefact template section name

The anatomy calls this section "Artefact template." Skills that produce a single named artefact may use a descriptive variant (e.g. "Task list template", "Finding template") — the name should identify the artefact type. The section must still appear in the required position.

## Meta-pack skills

Navigation and orientation skills (e.g. `using-this-pack`) are not workflow skills. They are exempt from the body sections Inputs, Outputs, Artefact template, Red flags, and Exit criteria. They must still have: Title, Purpose, When to use, Do not use when, and a Related or equivalent lookup table.

## See also

- `docs/hook-anatomy.md` — for hooks
- `docs/sub-agent-anatomy.md` — for sub-agent personas
- `docs/brief-template.md` — for the brief that drives authoring
- `docs/authoring-learnings.md` — calibration guidance and failure modes
