# AGENTS.md

Instructions for any coding agent (Claude Code, Codex, etc.) working in this repository. Tool-agnostic by design — see `CLAUDE.md` for any Claude-Code-specific additions.

## What this repo is

A Markdown-only skill pack — no build system, no tests, no CI. Every artefact is a `.md` file. The deliverable is well-authored prose, not runnable code.

See `CLAUDE.md` for repo structure, authoring rules (skills, hooks), and commit style.

## Workflow & issue tracking

Work in this repo is tracked as Linear initiatives and cycles. The governance model — the initiative shape, cycle composition, backlog convention, and issue lifecycle (including the review-before-Done gate and the issue-comment standard) — is owned by the **Workflow pack** (plugin `workflow`), whose SessionStart hook loads it into context when installed. Follow that governance for all tracker work; Shaper does not vendor a copy of it.

Repo-specific notes that supplement the generic governance:

- This repo pushes directly to **main**; open a PR only when the owner asks. An issue is not Done until the work is committed and pushed — local-only work doesn't count.
- Update issue status at the moment of state change, not batched at session end. Blocked work stays In Progress with a comment naming the blocker.
- Shape a new initiative with the `/shape:idea` skill; don't hand-create goal-directed projects. Initiative-shaped work (5+ issues, clear goal) slots into the *next* cycle; a bug or one-off (< 5 issues) goes on the backlog and into the ops slot if urgent.
- If an issue names a delegate (`Delegates to` / `On pickup`), invoke that skill to break the node into build tasks before coding (ktlo issues carry no breakdown step).

## Git

Conventional-commit-ish prefixes: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`. Subject line ≤ 70 chars; details in the body if needed. Do not add `Co-Authored-By` trailers.
