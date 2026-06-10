# Lifecycle expansion — shaping → execution

Status: **confirmed and parked** — all three initiatives recorded in Linear (Personal team, Planned state) on 2026-06-10:
[A — Issues drain end-to-end on first-party skills](https://linear.app/ababushkin/project/issues-drain-end-to-end-on-first-party-skills-be562671c8d8) ·
[B — Shaping consolidates to four dense front doors](https://linear.app/ababushkin/project/shaping-consolidates-to-four-dense-front-doors-9c8a65552b93) ·
[C — drain-cycle supervises; the pack owns the workflow](https://linear.app/ababushkin/project/drain-cycle-supervises-the-pack-owns-the-workflow-0f0222d99392)
Date: 2026-06-10
Inputs: deep review of obra/superpowers (5.1.0) and addyosmani/agent-skills (2e0dfbfb436e) installed plugins, audit of this repo, audit of ~/src/drain-cycle; interview-me session with confirmed intent.

---

## 1. Deep-review findings (condensed)

### Shaper today

14 skills (~3,086 lines), 2 hooks, 1 sub-agent (code-reviewer), 10 references, 3 rule files. Coverage is front-heavy by design: Define/Plan/Decide deep; **Build 0%, Deploy 0%, Ship partial** (pr-prepare, verify-implementation, code-reviewer). Three skills bust the pack's own 300-line cap: plan-review (369), initiative-shape (310), roadmap-shape (303).

The "too lengthy" instinct, measured: median skill is ~225 lines — *between* superpowers (~190) and agent-skills (~290). What differs is density, not length: superpowers makes every section a gate, dot-graph, rationalization table, or prompt template, with 2 frontmatter fields vs Shaper's 10+ and no 1,700-line rules/references sidecar.

### What the other packs have that Shaper lacks

- **superpowers execution engine** — brainstorming → writing-plans (2–5 min TDD steps, exact code) → subagent-driven-development (fresh implementer subagent per task; two-stage review: *spec compliance before code quality*; never trust the implementer's report; built-in cheap/standard/frontier model routing) → finishing-a-development-branch. Worktree isolation as prerequisite. Three-layer verification: plan-step commands → per-task dual review → claim-level fresh-evidence gate (verification-before-completion).
- **agent-skills delivery loop** — /spec → /plan → /build (per-task RED/GREEN/commit) → /ship (parallel fan-out to code-reviewer + security-auditor + test-engineer personas → GO/NO-GO with mandatory rollback plan). Personas are ~100-line portable role prompts with a composition doctrine: skills = how, personas = who, commands = when; personas never call personas.

### What neither pack has (Shaper's edge)

Both are **tracker-blind and PR-blind**: no Linear, no Graphite, no stacked PRs, no auto-merge policy, no autonomous runner. Shaper + drain-cycle already own that territory — drain-cycle spawns workers per Linear issue in worktrees, routes models via labels, and its verify-flow already expects `/shape:task`, `/shape:verify-implementation`, `/shape:pr-prepare`, `/shape:pr-respond`, with a half-built Graphite stack mode (`.drain-handoff.json`).

**Conflict to resolve:** `drain_cycle/prompt.py` hardcodes `/code-review-and-quality` (an agent-skills skill). Uninstalling that pack breaks drains unless Shaper owns a replacement.

---

## 2. Confirmed intent (interview-me output)

- **Outcome:** Shaper becomes the single pack covering the full lifecycle — `shape:*` for planning (4 front doors: `shape:idea`, `shape:project`, `shape:design`, `shape:delivery`) and a second verb namespace (e.g. `ship:*`, verb TBD) for execution: breakdown-at-pickup → TDD/incremental build → systematic debugging → simplification → reviewer fan-out → verify → Graphite-first PR finishing. superpowers and agent-skills get uninstalled.
- **User:** Headless drain-cycle workers first; interactive second. drain-cycle re-scoped to a thin vendor-agnostic supervisor (spawn, guardrails, halt, grade) whose prompt points at one skill — the workflow lives in the pack so a codex/kimi worker can follow the same prose.
- **Why now:** Planning half is deep but execution is 0%; drain-cycle's verify-flow half-expects skills that don't exist; two external packs fill the gap.
- **Success:** Both external packs uninstalled with nothing missed in practice; workers complete issues end-to-end on pack skills only; artefacts optimized for correctness and review-ease.
- **Constraints:** Linear for state; Graphite-first PRs (plain git fallback); sub-agents as portable persona prompt files (code-reviewer, security-auditor, spec-compliance) — Agent-tool dispatch on Claude Code, inline fallback elsewhere. Style reform: superpowers density, frontmatter cut to essentials, ~150-line target for execution skills, 3 over-cap skills brought under 300.
- **Pruning:** roadmap-shape, backlog-manage, app-calibrate deleted; idea-triage folds into `shape:idea`; spikes fold into `shape:design`; plan-review survives as the design/delivery exit gate; render-html survives as a utility.
- **Domain shortlist (in):** systematic debugging, code simplification, security-review persona. **(Out):** frontend/perf/browser set.
- **Out of scope this round:** deployment stage, implementer sub-agents (drain-cycle's job), cross-vendor adversarial review (future drain-cycle feature), renames (pack umbrella + drain-cycle).

### Architecture decision: drain-cycle re-scope

drain-cycle owns *processes* (cycle selection, worktree setup, vendor-agnostic worker spawning, token/time/cost guardrails, halt/resume, run logs/grading); Shaper owns *workflow* (the intra-issue procedure and reviewer personas). drain-cycle's inlined prompt procedure shrinks to "work issue X in worktree Y; follow the entry skill." Personas live as portable prompt files so non-Claude workers degrade to inline self-review with the same persona prompt. Cross-vendor adversarial review (Claude implements, codex reviews) becomes a later drain-cycle feature.

---

## 3. Split — three initiatives

Total scope exceeds the 15-issue split threshold. Cut:

| # | Initiative | Scope | Order |
|---|---|---|---|
| A | **Issues drain end-to-end on first-party skills** | Execution namespace skills (~5–6), 2–3 personas, fixture harness + grader, one-line drain-cycle prompt pointer, validation drains | first — shaped below |
| B | **Shaping pack consolidation + style reform** | 4 front doors, prune (roadmap/backlog/calibrate), fold triage→idea and spikes→design, density reform, frontmatter cut, 3 over-cap skills under 300 | second — to be shaped |
| C | **drain-cycle re-scope to thin supervisor** | Extract workflow from prompt.py, guardrail/grade cleanup, Graphite stack-mode completion, cross-vendor worker spawning | third — to be shaped |

---

## 4. Initiative A — draft shape (awaiting confirmation)

**Name:** Issues drain end-to-end on first-party skills

**Goal:** For drain-cycle workers (and Anton driving interactively), make every picked-up Linear issue flow from pickup to a merged, reviewable PR on Shaper skills alone — review trail attached, no rescue by a human and no reliance on third-party packs.

**Key results:**

**KR1 (stretch)** — ≥4 of the next 5 drained issues reach Done with a merged PR and zero manual fix commits after the worker's final push, with the full review trail present (verify verdict, What/Why/Focus PR body, review-summary comment) *(bet)*
- baseline: 0 — execution skills don't exist; current drains depend on `/code-review-and-quality` and push unreviewed to main
- target: ≥4 of 5
- measured over: the first 5 issues drained after the execution skills land (within 2 cycles)
- how we'll know: `drain-cycle grade` over `~/.drain-cycle/runs/*.json` + `git log` scan for post-push fix commits; review trail checked from Linear issue comments and PR bodies

*Layer 1: outcome · Layer 2: self-trial protocol*

**KR2 (commit)** — the review/verify skills surface ≥9 of 10 seeded Critical/Required findings when run against fixture diffs with known defects (type suppressions, AC violations, security holes) *(foundation)*
- baseline: 0/10 — fixtures don't exist; building the fixture set + grader is the first issue
- target: ≥9/10 seeded findings surfaced
- measured over: by cycle close
- how we'll know: `bin/grade-execution-review fixtures/execution-review/` runs each persona against each fixture diff and diffs surfaced findings against the seeded manifest; exit code + log cached in `fixtures/execution-review/_runs/`

*Layer 1: correctness · Layer 2: golden-path test*

**KR3 (commit)** — 100% of drained issues in the window invoke the new execution skills and zero invoke superpowers/agent-skills; both packs uninstalled and zero references to their skill names remain in the Shaper repo or drain-cycle prompts *(brake)*
- baseline: both packs installed; `drain_cycle/prompt.py` hardcodes `/code-review-and-quality`
- target: 100% first-party invocation, 0 third-party references, 0 packs installed
- measured over: by cycle close
- how we'll know: `grep -rn 'code-review-and-quality\|superpowers' drain_cycle/ skills/ .claude/` returns empty + worker transcripts in run logs show only first-party skill invocations + plugin list output

*Layer 1: discipline · Layer 2: artefact-exists / structural check*

*Dimensions: outcome / correctness / discipline — all distinct per rule 5b.*

**Affected repos:** agent-skills-shaper, drain-cycle (one-line prompt pointer only)

**Appetite:** ~10 issues

**Kill condition:** If, after the execution skills ship, 3 consecutive drained issues require manual fix commits or fall back to third-party pack skills, stop — reinstall agent-skills, keep Shaper shaping-only, and fold the learnings into the pack's README.

**Project type:** 1 — methodology skill pack

**Dominant model tier:** Balanced — most issues are bounded skill-authoring against existing anatomy specs; the persona-contract and namespace decisions are the Frontier exceptions.
