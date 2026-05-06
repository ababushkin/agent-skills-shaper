---
name: app-calibrate
description: >
  Creates or updates docs/app-context.md with app-specific baseline data — key metrics,
  performance signals, user volume, and known problem areas. Run this before idea-triage
  whenever the idea involves improving, reducing, increasing, or speeding up something
  measurable — without baseline data, ICE Impact scores are ungrounded assertions.
  Also run when app-context.md is missing, stale (>90 days), or a new MCP data source
  has been connected. Trigger phrases: "calibrate the app context", "set up baseline
  metrics", "update app metrics", "prepare for triage", "what are our current metrics",
  "let's document our baseline", "I want to ground our scoring in real data".
pack: product
lifecycle_stage: define
principles_implemented:
  - source: product
    id: P4
    bucket: embedded
  - source: product
    id: B2
    bucket: embedded
  - source: product
    id: D5
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

# App calibrate

## Purpose

app-calibrate exists so that idea-triage has baseline data to work from. Without it, ICE Impact scores are assertions: a number produced by gut feel rather than evidence of the distance between where the metric is now and where it needs to go. With it, the delta from current to target becomes the measurable grounding for Impact — and the problem statement gains a specific, falsifiable target.

The skill has two modes:

- **Create**: `docs/app-context.md` does not yet exist. Walk the schema from scratch.
- **Update**: the file exists but fields are stale, blank, or out of date. Re-visit each section, preserve what's still accurate, update what isn't.

Both modes produce a file that satisfies the validity rules defined in `references/app-context-schema.md`.

## When to use

- Before running `idea-triage` on improvement-type ideas: improving, reducing, increasing, or speeding up something that has a measurable current state.
- When Key metrics rows in an existing `docs/app-context.md` carry a `Last measured` date older than 90 days and the idea in hand depends on those metrics.
- When MCP tools have been newly connected and can automate metric population.
- When the app's purpose, user base, or primary metrics have shifted significantly since the file was last updated.

## When not to use

- For new-feature ideas where no prior baseline exists. Create mode is still valid, but do not block triage on it — an empty template with no Current values does not improve scoring.
- As a substitute for `idea-triage`. Calibration is setup; triage is the gate.
- For capturing post-launch outcomes. That belongs in `post-launch-impact-review` (Rule D1).

## Inputs

Optional: an existing `docs/app-context.md`. The skill detects which mode it is in from file presence. No other required input.

## Outputs

`docs/app-context.md` at the current project root. The file follows the schema in `references/app-context-schema.md`.

## Workflow

**1. Detect mode.**
Check whether `docs/app-context.md` exists. If it exists: read it, report what sections are blank or stale, proceed in update mode. If not: proceed in create mode using the schema template.

**2. App summary.**
Ask: "In one sentence: what does this app do, and who are its primary users?" Record the answer. The summary names a domain and a user, not a solution ("we build X" is not a valid summary).

**3. Key metrics.**
Walk the table row by row. For each row, collect: metric name, current value, target, source (dashboard or tool name), date last measured. Accept partial rows if Current is filled; mark Target as `—` if not yet set. Mark Source and Last measured as `—` only as a last resort — a metric without a source is an assertion, not data.

**4. [GATE] Minimum validity check.**
At least 2 metrics must have Current values filled in with actual measurements — not `—` or placeholder text. If this is not met, stop and explain:

> Triage without baseline metrics produces ungrounded Impact scores. Add at least 2 metrics with current values before proceeding.

**5. Performance baseline.**
Prompt only if the idea domain is likely performance-related or the user mentions latency, load time, or error rates. Otherwise mark the section `<!-- not applicable -->` and move on.

**6. User volume.**
Ask: "How many active users or sessions per day does this app serve? What cohort sizes are affected by the types of improvements you typically pursue?" Record the answer in the User volume section.

**7. Known problem areas.**
Ask: "List 3–5 high-level areas where improvement ideas commonly arise in this app." Free text, no structure required.

**8. Extension: MCP data sources.**
Ask: "Do you have MCP tools connected that can fetch any of these metrics automatically? If yes, name the metric, the MCP command, and any notes." If no MCP tools are available, mark the section `<!-- not applicable -->`.

**9. Write the file.**
Before writing, display the complete populated template and confirm with the user. Write or overwrite `docs/app-context.md`.

## Artefact template

```markdown
# App context: <app-name>

## App summary
<!-- One sentence: what the app does, who uses it. -->

## Key metrics
| Metric | Current | Target | Source | Last measured |
|--------|---------|--------|--------|--------------|

## Performance baseline
| Signal | Current | Target | Tool |
|--------|---------|--------|------|

## User volume

## Known problem areas

## Extension: MCP data sources
<!-- Optional. For each metric fetchable automatically:
     Metric | MCP command | Notes                                          -->
```

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "I'll fill this in after triage." | Baseline data only grounds Impact scoring when present before triage. A score based on data you don't yet have is still an assertion. |
| "I know my metrics — I don't need to write them down." | Agent context is not your memory. The skill cannot see your head; the file is the interface. |
| "My app is too unusual for this schema." | The schema is deliberately minimal. Use the Extension section for custom fields; the core four sections are universal. |
| "The file is from three months ago — it's probably fine." | Metrics > 90 days old are treated as opinion/anecdote by idea-triage. Refresh before triage if staleness matters for the idea in hand. |

## Red flags

- `docs/app-context.md` exists but all Key metrics rows show `—` in the Current column.
- App summary names a solution ("we build X") rather than a domain and a user.
- Extension section lists MCP commands that have never been run against the live system.
- The file's most recent `Last measured` date is older than 6 months with no refresh planned.

## Verification / exit criteria

The skill has run correctly when:

1. `docs/app-context.md` exists at the project root.
2. App summary is one sentence naming what the app does and who uses it — not a solution description.
3. At least 2 Key metrics rows have Current values, a named Source, and a Last measured date.
4. If a performance baseline was collected, at least one Signal row has a Current value.
5. User volume section is not blank.
6. Any section that was skipped carries a `<!-- not applicable -->` comment rather than empty markup.

## References

- `references/app-context-schema.md` — schema definition, validity rules, and sourcing calibration
- `skills/idea-triage/SKILL.md` — downstream consumer of this file
- `rules/PRODUCT_RULES.md` — P4, B2, D5
