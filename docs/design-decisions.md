# Design decisions

Numbered decisions that shape this pack's architecture and skill contracts. Each entry follows the Nygard ADR pattern — Context, Decision, Consequences — compressed to one record per decision. Decisions are immutable once recorded; a superseding decision references the one it replaces.

Earlier decisions (§1–§16) predate this log; they are embedded in the relevant skill frontmatter (`predecessor`, `kept_from_predecessor`, `changed_from_predecessor`) and in the README comparison table.

---

## §17 — task-shape runs at implementation time, not at planning time

**Date:** 2026-06-01
**Status:** Accepted

### Context

Two candidate positions exist for shaping a single ticket into a verifiable AC checklist and task list:

1. **At planning time** — run the shaping step as part of `planning-and-task-breakdown` when the design doc is decomposed into tickets. All tickets arrive pre-shaped.
2. **At implementation time** — run the shaping step when a worker session picks up a ticket, just before coding begins.

### Decision

task-shape runs at **implementation time**, inside the worker session that owns the ticket. It is a separate skill (`task-shape`) distinct from `planning-and-task-breakdown`.

Rejected alternative: pre-computing the shaping output via `planning-and-task-breakdown` at planning time. This was rejected because:

- Planning-time AC has a high rate of decay before the ticket is reached. The later a ticket sits in the backlog, the more its AC diverges from what is actually true at build time (design changed, service boundaries shifted, a dependency resolved or was added).
- `planning-and-task-breakdown` consumes a design doc — it decomposes a whole design at once, producing many tickets. It is not the right shape for per-ticket AC verification at pickup.
- Running the shaping step at pickup means the agent doing the shaping has the full context of what's actually true now: current codebase, resolved dependencies, any post-planning decisions. It can surface gaps that were not visible at planning time.

### Input/output contract

**Input:** A single Linear issue — ID, URL, or pasted body — with a title, description, and at least one AC criterion or "done when" statement.

**Output (the shaping block):**

1. *Enriched AC checklist* — every criterion annotated ✓ complete / ⚠ gap / ? ambiguous; gaps listed with owner and question; ambiguities listed with assumed interpretation.
2. *Sizing decision* — single-stack or multi-stack (N stacks), naming each stack as `<repo/service> (<language>)`; one-sentence rationale.
3. *Per-stack task list* — one ordered list per stack; walking skeleton as task 1 (setup folded in, no preceding setup task); subsequent tasks one observable outcome each; cross-stack and external dependencies named on the dependent tasks.

The shaping block is appended to the issue body and posted as a comment. If irresolvable AC gaps exist, the output stops after the AC checklist and no task list is produced.

### Consequences

- Worker sessions that pick up a ticket must invoke task-shape before writing any code. An implementation that starts without a shaping block is out of process.
- The AC checklist is the canonical contract for the build; it takes precedence over the issue description if the two diverge.
- task-shape is not a replacement for `planning-and-task-breakdown`. The two skills are complementary: `planning-and-task-breakdown` decomposes a design into a ticket set at planning time; task-shape enriches one ticket at implementation time.
- The output format (shaping block template) is the stable schema the implementer and any downstream reviewer consume. Changes to the template require updating this decision record.
