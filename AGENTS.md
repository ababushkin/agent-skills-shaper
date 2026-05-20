# AGENTS.md

Instructions for any coding agent (Claude Code, Codex, etc.) working in this repository. Tool-agnostic by design — see `CLAUDE.md` for any Claude-Code-specific additions.

## What this repo is

A Markdown-only skill pack — no build system, no tests, no CI. Every artefact is a `.md` file. The deliverable is well-authored prose, not runnable code.

See `CLAUDE.md` for repo structure, authoring rules (skills, hooks), and commit style.

## Linear workflow

Linear is authoritative for status. Local task lists are fine for within-session bookkeeping; they don't replace a Linear issue.

**Governance model:** `rules/linear-workflow.md` — read it before doing any Linear work. It defines the initiative model, cycle composition (3 initiatives + 1 ops slot), backlog convention, and issue lifecycle. The summary below covers the operational mechanics; the rule file is the source of truth.

**Cycles.** Work is planned in cycles of 3–4 working days. Each cycle pulls 3 goal-oriented initiatives plus an ops slot. When picking up an issue, prefer ones already in the current cycle. If you start something not in the cycle, decide explicitly whether to pull it in or defer — don't silently expand cycle scope. Use `mcp__claude_ai_Linear__list_cycles` to see the current cycle.

**Creating a new initiative:** Use the `/initiative-shape` skill. Do not create Linear projects by hand for goal-directed work — the skill enforces the four-field check (goal / success criterion / affected repos / appetite) before creating the project.

**On start of any issue:**
- Move to **In Progress** via `mcp__claude_ai_Linear__save_issue`.
- If the issue isn't yet in the current cycle and you intend to ship it this cycle, assign it to the current cycle.
- Every issue must be either assigned to an initiative project or explicitly in the ops slot (no project). An unprojeceted issue with no cycle assignment is untracked — don't let this happen.

**On completion:**
- Move to **Done** only after the work is committed AND pushed to main. An issue isn't Done if the work only exists locally. (This repo pushes directly to main; PRs only when the owner asks.)
- Status updates happen at the moment of state change — not batched at end of session.

**Blocked** = leave In Progress + add a blocker comment naming the blocker. Don't silently park work.

**New work surfaced mid-flight:**
- Initiative-shaped (5+ issues, clear goal): create via `/initiative-shape`, slot into the *next* cycle explicitly.
- Bug or one-off (< 5 issues): create on team backlog; pull into the current cycle's ops slot if urgent.

## Git

Conventional-commit-ish prefixes: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`. Subject line ≤ 70 chars; details in the body if needed. Do not add `Co-Authored-By` trailers.
