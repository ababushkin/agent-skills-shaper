---
name: app-context-schema
description: >
  Schema for docs/app-context.md — the per-project baseline data file used by
  app-calibrate to capture and by idea-triage to ground ICE Impact scores and
  measurable problem statement targets.
type: reference
cited_by:
  - skills/app-calibrate/SKILL.md
  - skills/idea-triage/SKILL.md
---

# App context schema

`docs/app-context.md` is a per-project baseline data file. It lives in the user's project repository (not in the skill pack), is created or updated by `app-calibrate`, and is read by `idea-triage` when scoring improvement-type ideas. It is not a design doc or a triage record — it is reference data that grounds evidence-quality scoring and measurable problem statement targets.

## Where it lives

At the root of the project being worked on: `docs/app-context.md`. Skills that read it look for it at this path relative to the current working directory. The path is fixed; do not rename or relocate it.

## Six-section schema

```markdown
# App context: <app-name>

## App summary
<!-- One sentence: what the app does, who uses it. -->

## Key metrics
| Metric | Current | Target | Source | Last measured |
|--------|---------|--------|--------|--------------|
<!-- Minimum 2 rows with Current values filled in before this file is valid. -->

## Performance baseline
| Signal | Current | Target | Tool |
|--------|---------|--------|------|
<!-- LCP, load time, error rate, etc. Leave blank if not relevant. -->

## User volume
<!-- Active users / sessions per day / cohort sizes that improvement ideas affect. -->

## Known problem areas
<!-- Brief list of 3–5 high-level areas where improvement ideas commonly arise. -->

## Extension: MCP data sources
<!-- Optional. For each metric fetchable automatically:
     Metric | MCP command | Notes                                          -->
```

## Validity rules

A file is **minimally valid** when:
- App summary is filled in (one sentence naming what the app does and who uses it).
- At least 2 Key metrics rows have `Current` values set to actual numbers or measurements — not `—` or placeholder text.

A file with only Target or Source values but no Current values does not ground Impact scoring. Targets without baselines are aspirations, not evidence.

## Data freshness

Each row in Key metrics carries a `Last measured` date. idea-triage applies the following calibration when reading these values:

- `Last measured` ≤ 90 days: treat as indirect data (Gilad 2–5). Current values are live enough to ground scoring.
- `Last measured` > 90 days: treat as opinion-level data (Gilad 0.5–2). Flag in the triage evidence section; recommend running `app-calibrate` to refresh before finalising the ICE score.

## Sourcing calibration

The source of each metric determines its evidence quality ceiling:

| Data source | Gilad equivalent |
|---|---|
| Manual entry from memory | 0.5–1 (opinion/anecdote) |
| Copied from dashboard (no MCP) | 2–3 (indirect data, manual) |
| Fetched via MCP from live monitoring | 4–6 (indirect data, automated) |
| Derived from A/B test or experiment | 5–8 (experiment) |

Neither manual nor MCP-automated data replaces experimental data. The Extension section of `docs/app-context.md` documents which metrics can be fetched automatically and which must be entered by hand.

## Sources

- `skills/app-calibrate/SKILL.md` — skill that creates and updates this file
- `skills/idea-triage/SKILL.md` — skill that reads this file at evidence interrogation and ICE scoring steps
