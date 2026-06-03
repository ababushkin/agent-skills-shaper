# Changelog

All notable changes to this project are documented in this file. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Renamed `planning-and-task-breakdown` → `execution-breakdown` and repositioned it as the agent-facing breakdown that runs at pickup, right before the build. Ends the name clash with the upstream `addyosmani/agent-skills` skill it derives from, and signals the audience split: `-shape` skills (e.g. `delivery-shape`) are the product-facing artefacts a human reviews; `execution-breakdown` is the engineering breakdown an agent runs. See `docs/designs/shaping-pipeline.md`.

## [0.1.0] — 2026-05-07

First public release. Soft fork of [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) — the structural conventions (frontmatter, anatomy specs, the `SKILL.md` pattern) are inherited; no paragraphs are copied verbatim.

### Skills (10)

Product:

- `idea-triage` — interrogates incoming ideas through confidence gates, ICE scoring, and Kano classification. Routes to idea bank or validation.
- `backlog-manage` — curates the idea bank between triage and planning.
- `roadmap-shape` — builds a Now/Next/Later roadmap with explicit portfolio-theme mix and capacity allocation.
- `app-calibrate` — grounds idea-triage Impact scores in app-specific context.

Engineering:

- `product-spike` — throwaway artefact to answer one product question before committing to a design.
- `design-doc` — structures significant work before building (problem → constraints → alternatives → decision → operability).
- `planning-and-task-breakdown` — decomposes a design or spec into small, verifiable tasks.
- `incremental-implementation` — thin vertical slices, walking-skeleton-first; bug-fix sub-workflow for KTLO work.
- `plan-review` — reviews a plan, spec, or design before approval.

Meta:

- `using-this-pack` — meta-skill for finding the right skill.

### Hooks (1)

- `stop-the-line` — catches type suppressions, compiler directives, test skips, deleted assertions, and static-analysis suppressions in a diff. Fires when an agent signals work is done.

### Rule files (3)

- `rules/PRODUCT_RULES.md` — idea filtering, roadmap discipline, capacity allocation.
- `rules/eng-principles-universal.md` — design before build, small-batch, explicit contracts, technical quality.
- `rules/eng-principles-agentic.md` — agent-specific scope discipline, no speculative refactoring, confirmation before destructive action.

### References (7)

- `confidence-meter` — Gilad's 1–5 evidence-quality scale.
- `ice-scoring` — Impact × Confidence × Ease formula and scoring guide.
- `kano-classification` — five-category feature taxonomy with decay behaviour.
- `portfolio-themes` — Doshi's seven strategic themes with capacity-allocation guidance.
- `nfr-categories` — NFR taxonomy with measurable targets and fitness-function types.
- `dora-metrics` — four DORA metrics with elite/high/medium/low benchmarks.
- `app-context-schema` — schema for grounding app-specific context, used by `app-calibrate` and `idea-triage`.

### Install paths

- Marketplace: `/plugin install github@ababushkin/agent-skills-shaper` (from a Claude Code session).
- Local dev: `./install.sh` from a clone — generates command wrappers, symlinks skills as `shape-<name>`, appends rule-file `@`-refs to `~/.claude/CLAUDE.md`. Idempotent.
- Other agents (Cursor, Gemini CLI, Windsurf, …): paste rule files into the agent's instructions; load skills situationally.

[Unreleased]: https://github.com/ababushkin/agent-skills-shaper/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/ababushkin/agent-skills-shaper/releases/tag/v0.1.0
