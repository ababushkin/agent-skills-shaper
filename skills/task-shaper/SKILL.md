---
name: task-shaper
description: >
  Enriches the acceptance-criteria checklist and adds a model-routing sizing decision to
  each task in a Linear issue, then writes the output back to the issue body as a delimited,
  idempotent section. Run at pickup — before implementation — so the analysis survives
  session restarts and drain resumes without re-shaping from scratch.
  Trigger phrases: "shape the tasks for this issue", "enrich the AC on <issue>",
  "size the tasks", "add routing annotations", "run task shaper on <issue-id>",
  "shape:task <issue-id>".
pack: engineering
lifecycle_stage: plan
principles_implemented:
  - source: eng-agentic
    id: P3
    bucket: embedded
  - source: eng-agentic
    id: P4
    bucket: embedded
  - source: eng-agentic
    id: P7
    bucket: embedded
  - source: eng-universal
    id: Rule B2
    bucket: embedded
length_target: 150–200
author: Anton Babushkin
predecessor:
  repo: none
  skill: none
  relation: new
kept_from_predecessor: "n/a"
changed_from_predecessor: "n/a"
---

# Task shaper

## Purpose

task-shaper takes a Linear issue at pickup time and produces two things: an enriched AC checklist where every "done when" criterion is specific and verifiable rather than descriptive, and a model-routing sizing decision per task from the 5-axis rubric in `references/task-sizing.md`. Both are written back to the issue body as a clearly delimited, idempotent section.

The write-back is the load-bearing part. Without it, a restarted drain or resumed session must re-run the shaper from scratch — and the analysis may diverge. Agentic P7 — memory lives in artefacts, not in agents — applies directly: the enriched output must be in the Linear issue body to be durable. Writing to a local file or keeping it in context does not satisfy this.

## When to use

- A drain or worker session picks up a Linear issue that has a task list or a `## Completion` section (delivery-shape format) and needs it enriched and sized before implementation begins.
- An operator manually runs the shaper on a specific issue before handing it to an implementation agent.

## When not to use

- **No task list or Completion section in the issue** — the shaper has nothing to enrich. Add a minimal task list or run `delivery-shape` to produce the Completion section first.
- **`ktlo` nodes** — these carry `None — roadmap A5 carve-out.` as their Completion; there are no tasks to size. Skip this skill.
- **After implementation has started** — enriched AC written after the first commit describes what was built, not what must be built. The gate exists to force the former.

## Inputs

A Linear issue ID (passed as argument, e.g. `ABA-123`, or detected from current context). The issue must contain at least one of:
- An explicit task list (`- [ ]` lines), or
- A `## Completion` section with one or more `Done when:` or `Decision:` lines (delivery-shape node format).

## Outputs

The Linear issue body updated in place, with a `<!-- shaper-output-start -->` / `<!-- shaper-output-end -->` section appended. The section contains:
- An enriched task list: each task with a specific, binary-checkable `Done when:` condition.
- A `Model:` routing annotation per task in the canonical format from `references/task-sizing.md`.
- A generation timestamp.

All operator-written content above the delimiter is preserved byte-for-byte.

## Workflow

**1. Read the issue.**
Call `get_issue(<issue-id>)`. Capture the full body (description field). This is the only permitted source — do not proceed from memory of a prior session (agentic P3). If the issue ID was not provided, resolve it from the current Linear context before continuing.

**2. [GATE] Confirm shapeable content.**
Scan the body for at least one `- [ ]` task or one `Done when:` / `Decision:` line in a Completion section. If neither is found, stop: report the gap, name which input is missing, and do not write anything.

**3. Enrich the AC checklist.**
For each task or criterion:
- Rewrite it as a specific, observable condition — not "feature is implemented" but "endpoint returns `{id, status}` for a valid payload, confirmed by an automated integration test."
- Anchor the rewrite to the issue's What and Completion sections (agentic P3); do not add scope.
- A criterion passes the enrichment bar when a reader can run a check and get a binary result.
- Preserve the walking skeleton as task 1 (eng-universal Rule B2).

**4. Apply the 5-axis sizing rubric.**
For each enriched task, score the five axes per `references/task-sizing.md` — Reasoning complexity, Specification completeness (inverted), Hallucination sensitivity, Stakes/reversibility, Orchestration role — and derive:
- Model tier: Fast / Balanced / Frontier
- Review-attention flag: standard / elevated
- Companion-skill triggers (if HS = High or SR = High)

Emit the annotation in the canonical format: `Model: <tier> · risk <reversible|one-way> · review <standard|elevated> · axes RC·SC·HS·SR·OR = <L|M|H>·<L|M|H>·<L|M|H>·<L|M|H>·<L|M|H>`.

**5. [GATE] Idempotency check.**
Scan the current body for `<!-- shaper-output-start -->`.
- **Not found:** append the shaper-output section after existing content.
- **Found:** replace the content between `<!-- shaper-output-start -->` and `<!-- shaper-output-end -->` with the new output. Everything outside the markers is untouched.

Never append a second shaper-output section; the check must run before every write.

**6. Compose the updated body.**
Construct the full body string:
1. Operator-written content before `<!-- shaper-output-start -->` (or the full body if no markers exist).
2. One blank line.
3. The shaper-output section (template below).
4. Any operator-written content after `<!-- shaper-output-end -->` (preserved verbatim).

`save_issue` replaces the description field entirely — all operator content, both before and after the markers, must be carried forward explicitly.

**7. Write back.**
Call `save_issue(id=<issue-id>, description=<updated-body>)`. Do not retry on failure; report the error and leave the issue unchanged.

**8. [GATE] Verify.**
Call `get_issue(<issue-id>)` and assert:
- `<!-- shaper-output-start -->` appears exactly once in the body.
- Every enriched task carries a `Model:` annotation.
- Operator content above the start marker is unchanged.

If any assertion fails, report it as a verification failure — do not declare the skill done.

## Artefact template

```markdown
<!-- shaper-output-start -->

## Shaper output

*Shaped: <ISO date>*

### Enriched tasks

- [ ] `skeleton` — <one-sentence description; foundational setup folded in>
  **Done when:** <specific, observable, binary-checkable condition>
  **Model:** <Fast|Balanced|Frontier> · risk <reversible|one-way> · review <standard|elevated> · axes RC·SC·HS·SR·OR = <L|M|H>·<L|M|H>·<L|M|H>·<L|M|H>·<L|M|H>

- [ ] <task name>
  **Done when:** <specific, observable condition>
  **Model:** <annotation>

### Open questions

*(none — or list items that blocked enrichment, with an owner per item)*

<!-- shaper-output-end -->
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "The AC is obvious — it doesn't need enrichment." | If it's obvious, the enriched criterion takes one line. If that line is hard to write, the task wasn't obvious — and that's when the enrichment is worth the most. |
| "I'll enrich the AC while implementing." | AC written during implementation describes what got built. AC written before constrains what gets built. The gate exists to force the latter (agentic P4). |
| "Running this twice would produce a duplicate." | The idempotency gate handles it — the second run replaces, never appends. There is no duplication risk. |
| "The Model annotation is just Balanced for everything." | Score first, conclude after. A wrong tier costs real money or misses a one-way-door risk; neither is recovered by "well it was probably Balanced." |
| "I'll write this to a local file for speed." | A local file is session-scoped. The next drain resume won't find it; the operator can't inspect it. Linear is the durable artefact (agentic P7). |

## Red flags

- Operator-written content above the `<!-- shaper-output-start -->` marker was overwritten or truncated.
- `<!-- shaper-output-start -->` appears more than once in the body — the idempotency check was skipped.
- Any enriched task is missing its `Model:` annotation.
- A `Done when:` criterion describes an implementation step ("the function is written") rather than an observable outcome.
- The walking skeleton is not the first enriched task.
- The shaper-output section was written to a local file or kept only in context rather than posted to the issue body.

## Verification / exit criteria

The skill has run correctly when:

1. `get_issue(<issue-id>)` returns a body containing `<!-- shaper-output-start -->` exactly once.
2. Every task in the shaper-output section has a specific, binary-checkable `Done when:` condition.
3. Every task carries a `Model:` annotation in the canonical format from `references/task-sizing.md`.
4. The walking skeleton (`skeleton` tag) is the first task in the enriched list.
5. All operator-written content above `<!-- shaper-output-start -->` is byte-identical to the pre-run body up to that point.
6. A second invocation of the skill on the same issue replaces the section rather than appending it, leaving `<!-- shaper-output-start -->` present exactly once.

## References

- `references/task-sizing.md` — the 5-axis routing rubric; defines model tier, review flag, annotation format, and companion-skill triggers
- `rules/eng-principles-agentic.md` — P3 (anchor to the issue, not to session memory), P4 (AC must be verifiable, not descriptive), P7 (write-back to Linear is the durability requirement)
- `rules/eng-principles-universal.md` — Rule B2 (walking skeleton first — preserved through enrichment)
- `skills/delivery-shape/SKILL.md` — upstream source of the five-section node bodies this skill enriches
- `skills/planning-and-task-breakdown/SKILL.md` — lateral skill: produces task lists for local docs; task-shaper does the same but targets a Linear issue body and writes back via the Linear MCP
