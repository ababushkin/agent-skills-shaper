# Handoff: `plan-review` skill — ready to implement

**Status:** Plan finalized and skill-creator-reviewed. Implementation NOT yet started.
**Date saved:** 2026-05-04
**Pick-up location:** /Users/anton/src/pde-skills (this repo)

---

## What this is

Building a new pde-skill: `plan-review`. Adversarial review of an
LLM-produced plan/spec/design BEFORE the user approves it. Catches
scope drift, unstated assumptions, unaddressed one-way doors.

Adapted from the `phase4-devils-advocate` agent in
/Users/anton/src/ai-thesis-research/.claude/agents/, which is a working
4-pattern adversarial-review template the user already trusts.

Fills backlog item #14 (`problem-first-reviewer`, confidence 3) in
PROJECT_PLAN.md. Partially absorbs item #19 (`roadmap-review`).

## Where the spec lives

**Authoritative spec:** `_briefs/plan-review-skill-spec.md` (this repo)

That file contains:
- Full frontmatter draft (description, principles_implemented, predecessor)
- 13-section body structure list (matches design-doc / idea-triage pack standard)
- Tier auto-selection rules (NOT user-pick)
- Workflow with `[GATE]` markers
- Three drafted evals (roadmap-without-triage, PrizeCategorySelector,
  clean-gem-bump for false-positive check)
- Implementation verification steps

A copy of the same file lives at
`/Users/anton/.claude/plans/yes-but-do-some-quirky-allen.md` — the
two should remain identical until implementation starts.

## Why we're doing this

User identified plan-review as a current weakness in /insights data:
approves coherent-looking plans that contain unstated assumptions or
scope drift, then pays for it in mid-execution rework. Two recent
real failures captured the pattern:

1. Roadmap shaped without running idea-triage on candidates → forced redo.
2. Vue removal task picked PrizeCategorySelector, which touched
   competition code user had abandoned → mid-task re-scope.

Both share root cause: plan looked plausible, user green-lit, mismatch
surfaced after work began.

## Decisions already locked (do NOT relitigate)

- **One skill, not multiple.** Splitting by plan TYPE creates competing
  skills for same mental slot.
- **Location: `pde-skills/skills/engineering/plan-review/`.** Versioned,
  inherits eng-principles auto.
- **No hook in v1.** Ship skill first, observe adoption, add nudge-hook
  only after skill earns muscle memory.
- **Tier auto-select, not user-pick.** User-pick produces skip rate;
  under pressure user always picks Quick.
- **Pre-mortem in BOTH tiers.** Klein research: highest single-move
  diagnostic value (+30% risk detection).
- **Predecessor: phase4-devils-advocate** (NOT problem-first-reviewer
  — that backlog item was never built).
- **Free of `references/` subdirectory in v1.** Refactor only if
  SKILL.md crosses 400 lines.

## Reviews completed

1. ✅ Devil's advocate pre-plan (in conversation) — confirmed one skill
   not multiple; auto-tier not user-pick; Klein pre-mortem placement.
2. ✅ Skill-creator review (skill-creator:skill-creator) — surfaced 12
   issues; all required + high-value ones folded into spec. Polish
   items (worked example, evals, length_target) included.
3. ⏳ User approval to start implementation — PENDING.

## Next session — exact next steps

1. **Read this handoff first**, then read `_briefs/plan-review-skill-spec.md`.
2. **Confirm with user** they're ready to start implementation. Do NOT
   start without confirmation.
3. **Implement in this order:**
   a. `skills/engineering/plan-review/SKILL.md` — paste full frontmatter
      from spec, write body following 13-section structure
   b. `skills/engineering/plan-review/evals/evals.json` — paste 3 evals
      from spec
   c. `.claude/commands/plan-review.md` — copy structure from
      `.claude/commands/design-doc.md`, swap skill reference
   d. `install.sh` — add `/pde:plan-review` line in printed-commands
      list (around line 62)
   e. `PROJECT_PLAN.md` — mark #14 in-progress (rename `plan-review`),
      downgrade #19 confidence
   f. `skills/using-this-pack/SKILL.md` — add routing entry
4. **Verify per spec §Verification:** install correctness, fresh-session
   load, retro-test against eval-1 + eval-2, false-positive check on
   eval-3, tier auto-select works, docs updated.
5. **Optional:** run skill-creator's eval loop on `evals/evals.json`
   to generate iteration-1 benchmark.

## Reference files to load on resume

- `_briefs/plan-review-skill-spec.md` — the full plan
- `skills/engineering/design-doc/SKILL.md` — frontmatter + body
  structure template (style anchor)
- `skills/product/idea-triage/SKILL.md` — artefact template + common
  rationalisations table format (style anchor)
- `.claude/commands/design-doc.md` — wrapper command pattern
- `install.sh` — wrapper-generation logic to mirror
- `/Users/anton/src/ai-thesis-research/.claude/agents/phase4-devils-advocate.md`
  — predecessor; source of 4-pattern template + SUSTAINED/OVERTURNED/
  PARTIAL verdict format

## Open items (non-blocking)

- None blocking implementation.
- Post-v1: decide on ExitPlanMode nudge-hook. Reassess after 1–2 weeks
  of real use.
- Post-v1: decide whether `roadmap-review` (#19) still warrants its own
  skill once `plan-review` has ≥5 uses against roadmaps.
