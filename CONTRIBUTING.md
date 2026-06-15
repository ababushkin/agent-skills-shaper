# Contributing

Thanks for your interest in Shaper. Contributions are welcome — bug reports, skill proposals, principle gaps, or improvements to existing artefacts.

This pack is a Markdown-only skill library. There's no build system, no tests, no CI. Every artefact is a `.md` file. The work is well-authored prose, not running code.

---

## Filing an issue

Use GitHub Issues. The two main templates are:

- **Bug report** — a skill misfires, a path is broken, an example is wrong, install.sh fails, etc.
- **Skill proposal** — you have a recurring decision point that an existing skill doesn't cover, and you've used the pack enough to know the gap is real.

For "principle gap" issues — a behaviour you keep seeing that the rules don't catch — use the bug-report template and tag with the rule file you'd expect it in (`PRODUCT_RULES.md`, `eng-principles-universal.md`, `eng-principles-agentic.md`).

---

## Proposing a new skill

Skills are workflows that solve a specific decision-point problem in product, design, or engineering. Read these before proposing one:

1. **`docs/skill-anatomy.md`** — the required structure, frontmatter, and section order.
2. **Two existing `SKILL.md` files** — match the voice. Direct, principle-named, no generic AI filler. Suggested reads: `skills/idea/SKILL.md` and `skills/design/SKILL.md`.
3. **`rules/eng-principles-universal.md`** if your skill is engineering-track — it's the canonical source for principle IDs you'll cite in frontmatter.
4. **`docs/authoring-learnings.md`** — calibration guidance and failure modes surfaced during v0.1.

### Required frontmatter fields

```yaml
name: <kebab-case>
description: <one sentence; what fires it, what it produces>
pack: <product | engineering | meta>
lifecycle_stage: <define | plan | build | ship | verify | review | meta>
principles_implemented:
  - source: <eng-universal | eng-agentic | product>
    id: <principle or rule id>
    bucket: <embedded | standalone | hook | sub-agent>
length_target: <range, e.g. 150-250>
author: <github handle>
predecessor:
  repo: <URL or "none">
  skill: <skill name in source repo, or "none">
  relation: <derivative | adjacent | new>
```

### Required sections, in order

`Title → Purpose → When to use → When not to use → Inputs → Outputs → Workflow → Artefact template → Common rationalisations → Red flags → Verification / exit criteria → References`

### Length and gates

- Target: **100–300 lines**. Hard cap: **350**.
- Below 100 lines triggers an under-specification check.
- Above 300 lines triggers a redundancy check.
- **Gates are marked `[GATE]`** in the workflow section. They're stop-the-line checks — don't remove them, don't make them optional.

### Voice rules

- No stack-prescriptive content. Skills are stack-agnostic. (No "use TypeScript", no "in your Rails app", etc.)
- No verbatim copy from `addyosmani/agent-skills` or any other skill pack. Declare the predecessor relation in frontmatter (`derivative` / `adjacent` / `new`) so reviewers can audit.
- Direct, principle-named prose. Cite principle IDs from the rule files, don't restate them.

---

## Proposing a new hook

Hooks are mechanical checks that fire on events (PR open, completion claim, etc.). Read `docs/hook-anatomy.md` before proposing one.

The non-negotiable rule: **fail criteria must be deterministic.** Non-deterministic fail criteria are a reject trigger. If a human reviewer would have to make a judgement call, it's a sub-agent (review persona), not a hook.

---

## Local development setup

To work on this pack with the symlinks pointing at your clone (so edits propagate without re-running the install):

```bash
git clone https://github.com/ababushkin/agent-skills-shaper.git
cd agent-skills-shaper
./install.sh
```

This wires up:

1. Slash commands in `~/.claude/commands/shape/`
2. Auto-invocable skill symlinks in `~/.claude/skills/shape-<name>`
3. `@`-refs to the rule files in `~/.claude/CLAUDE.md`

Re-run `./install.sh` after a `git pull` or after adding a new skill — it's idempotent and prunes stale symlinks.

---

## Commits and PRs

- Conventional-commit-ish prefixes: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`.
- Subject line ≤ 70 chars. Details in the body.
- One artefact per PR is the strong default. A PR that adds a skill, a hook, and three references is harder to review than three PRs.
- The PR description should name: which problem the artefact solves, which principle(s) it implements, which existing artefact it might overlap with (if any), and how you'd verify it works in practice.

---

## What we'll likely push back on

- Skills that re-state principles instead of operationalising them. A skill is a workflow, not a doctrine.
- Skills below 100 lines that look like a checklist with no decision points.
- Skills above 350 lines that bundle multiple decision points into one workflow.
- Stack-specific examples in skill prose. References can name a stack; the workflow can't.
- Soft gates — "consider doing X" instead of `[GATE]: do X before proceeding`.
- Predecessor relation set to `new` when the artefact is clearly derivative of an upstream skill.

---

## Code of conduct

We follow the [Contributor Covenant](CODE_OF_CONDUCT.md). Be respectful; the artefacts in this pack are opinionated, but disagreements about the opinions stay on the artefact.
