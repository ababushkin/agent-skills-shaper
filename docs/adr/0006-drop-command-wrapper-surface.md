# ADR 0006 — Drop the command-wrapper surface for workflow skills

- **Status:** Accepted
- **Date:** 2026-06-18
- **Supersedes (in part):** ADR 0004 (`exec:*` verb namespace) and ADR 0005 (shaping door leaf names) — specifically the part of each that realised the reserved verbs as generated `/shape:*` and `/exec:*` slash-command wrappers. The reserved verb *names* stand; only the wrapper *invocation surface* is withdrawn.
- **Serves:** Pack ergonomics — one invocation surface per workflow, so the skill picker lists each workflow once instead of three times.

## Context

Every workflow shipped on two installed surfaces:

1. **Auto-invocable skill** — `skills/<name>/SKILL.md`, installed as `~/.claude/skills/shape-<name>`, model-triggered or invoked by name via the Skill tool.
2. **Slash-command wrapper** — `.claude/commands/<name>.md`, a thin file that `@`-imports the same `SKILL.md` and invokes it, installed as `/shape:<name>` (and `/exec:<name>`).

Because the pack is loaded as a Claude Code plugin, each wrapper is also registered twice — once bare (`delivery`) and once plugin-namespaced (`shape:delivery`). The net effect in the skill picker: one workflow (e.g. delivery) appears three times — `shape-delivery` (the skill), `delivery` (bare command), and `shape:delivery` (namespaced command). Across 15 workflows that is ~45 entries for 15 capabilities. Operators read this as duplication or a caching fault.

The wrappers add no behaviour the skill does not already provide. The skill is the source of prose; the wrapper only forwards `$ARGUMENTS` into it. The duplication is pure surface, not capability.

Two wrappers are different: `stop-the-line` and `task-annotation-check` point at **hooks** (`hooks/<name>/HOOK.md`), not skills, and are not wired into `hooks/hooks.json`. For those two, the wrapper is the *only* manual invocation path, and there is no skill they duplicate.

## Decision

**Withdraw the slash-command wrapper surface for every workflow that has a backing skill.** Those workflows are invoked as `shape-<name>` skills — model-triggered on natural phrasing, or by name via the Skill tool. The reserved `shape:*` / `exec:*` verb names from ADR 0004/0005 remain the canonical identity in prose and in skill `name:` frontmatter; they are simply no longer published as typed slash commands.

**Keep exactly two wrappers** — `.claude/commands/stop-the-line.md` and `.claude/commands/task-annotation-check.md` — as the on-demand entry point for their hooks. `plugin.json` retains its `commands` key for these; `install.sh` still generates wrappers, but now only for the two that remain.

Deleted wrappers: `idea`, `project`, `design`, `delivery`, `plan-review`, `pr-prepare`, `render-html`, and `exec/{breakdown,build,debug,finish,pickup,review,simplify,verify}`.

## Consequences

**Positive**
- Each workflow appears once in the skill picker, under `shape-<name>`. The duplication is gone.
- One invocation surface to document and keep in sync; README, `install.sh` help, and CONTRIBUTING now describe a single primary surface.
- No capability lost: the two hook utilities keep their manual trigger.

**Negative / costs**
- No typed `/shape:idea`-style slash command for the core workflows. Operators who preferred typing a command now name the skill ("run shape:delivery") or let it auto-trigger. Accepted — the convenience did not justify a 3× picker.
- Prose that referenced the verbs as slash commands (README walkthrough, `references/project-types.md`, `rules/PRODUCT_RULES.md`, two SKILLs) was reworded to drop the leading `/`. The verbs remain; only the "type this command" framing changed.

## Scope

This ADR withdraws an invocation surface. It does **not** un-reserve any verb name (ADR 0004/0005 tables still govern leaf names) and does not change skill behaviour. Re-introducing typed slash commands for core workflows, or wiring the two hook utilities into `hooks/hooks.json`, would each be a follow-up decision.
