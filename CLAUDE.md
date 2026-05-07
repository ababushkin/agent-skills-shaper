# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## What this repo is

A Markdown-only skill pack — no build system, no tests, no CI. Every artefact is a `.md` file. The deliverable is well-authored prose, not runnable code.

---

## Skill Development

- Version-control all command/skill files in the repo (not `~/.claude/commands/`)
- Always include proper frontmatter on new skill files on first pass

---

## Repo structure

```
skills/             Flat layout — one dir per skill, each with SKILL.md
                    (matches Claude Code plugin auto-discovery convention)
rules/              Persistently-loaded rule files (PRODUCT_RULES.md, eng-principles-*.md)
hooks/
  stop-the-line/    HOOK.md
references/         Standalone reference files cited by skills
docs/               Anatomy specs and authoring guidance (skill-anatomy.md, hook-anatomy.md, …)
.claude-plugin/     plugin.json — manifest for marketplace install
.claude/commands/   Slash-command wrappers
```

Skills live at `skills/<name>/SKILL.md`. Hooks at `hooks/<name>/HOOK.md`. References at `references/<name>.md`. Rule files (`PRODUCT_RULES.md`, `eng-principles-*.md`) live at `rules/<name>.md`.

The flat skills layout matches the convention used by every other Claude Code plugin (verified across `addyosmani/agent-skills`, `claude-plugins-official/skill-creator`, etc.) — the plugin loader scans `<plugin_root>/skills/<name>/SKILL.md` and does not recurse into category subdirs. Product/engineering taxonomy is preserved in README tables, not in the filesystem.

---

## Authoring a new skill

Follow `docs/skill-anatomy.md` exactly. Required sections in order: Title → Purpose → When to use → When not to use → Inputs → Outputs → Workflow → Artefact template → Common rationalisations → Red flags → Verification / exit criteria → References.

Required frontmatter fields: `name`, `description`, `pack`, `lifecycle_stage`, `principles_implemented` (each with `source`, `id`, `bucket`), `length_target`, `author`, `predecessor` (with `relation`).

Length target: 100–300 lines. Hard cap 350. Below 100 triggers under-specification check. Above 300 triggers redundancy check.

Gates in the workflow section are marked `[GATE]` — do not remove them or make them optional.

---

## Authoring a hook

Follow `docs/hook-anatomy.md`. Hooks have deterministic pass/fail criteria. Fail criteria that are non-deterministic are a reject trigger — flag and fix before shipping.

---

## Commit style

Conventional-commit-ish prefixes: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`. Push directly to main; PRs only when the owner asks. Subject line ≤ 70 chars; details in the body if needed.

---

## Key constraints

- No stack-prescriptive content in skill prose. Skills are stack-agnostic.
- No verbatim copy from `addyosmani/agent-skills`. Every artefact must declare its predecessor relation in frontmatter.
- Voice must match the existing skills — direct, principle-named, no generic AI filler. Read two existing SKILL.md files before authoring a new one.
- `rules/eng-principles-universal.md` is the canonical source for principle IDs cited in engineering skills. Read it before referencing any principle.
