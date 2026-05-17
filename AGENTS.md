# AGENTS.md

Instructions for any coding agent (Claude Code, Codex, etc.) working in this repository. Tool-agnostic by design — see `CLAUDE.md` for any Claude-Code-specific additions.

## What this repo is

A Markdown-only skill pack — no build system, no tests, no CI. Every artefact is a `.md` file. The deliverable is well-authored prose, not runnable code.

See `CLAUDE.md` for repo structure, authoring rules (skills, hooks), and commit style.

## Linear workflow

Linear is authoritative for status. Local task lists are fine for within-session bookkeeping; they don't replace a Linear issue.

**Project:** PDE skill pack — https://linear.app/ababushkin/project/pde-skill-pack-7616052be5d2 (team ABA / Personal).

**Cycles.** Work is planned across cycles, often spanning multiple projects at once. When picking up an issue, prefer ones already in the current cycle. If you start something not in the cycle, decide explicitly whether to pull it in or defer — don't silently expand cycle scope. Use `mcp__linear-server__list_cycles` to see the current cycle.

**On start of any issue:**
- Move to **In Progress** via `mcp__linear-server__save_issue`.
- If the issue isn't yet in the current cycle and you intend to ship it this cycle, assign it to the current cycle.

**On completion:**
- Move to **Done** only after the work is committed AND pushed to main. An issue isn't Done if the work only exists locally. (This repo pushes directly to main; PRs only when the owner asks.)
- Status updates happen at the moment of state change — not batched at end of session.

**Blocked** = leave In Progress + add a blocker comment naming the blocker. Don't silently park work.

**New work surfaced mid-flight** (a new skill, hook, or reference that emerges from the current one) becomes a new Linear issue, slotted into a cycle deliberately. Don't silently expand scope.

## Git

Conventional-commit-ish prefixes: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`. Subject line ≤ 70 chars; details in the body if needed. Do not add `Co-Authored-By` trailers.
