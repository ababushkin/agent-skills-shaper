---
name: simplify
description: >
  Reduce complexity after code is green. Use after build passes but the implementation is
  heavier than it needs to be — simplify for clarity while preserving exact behaviour,
  leaving a reviewable before/after rationale. Trigger phrases: "clean this up", "simplify
  this", "this is over-engineered", "post-green pass", "make it readable".
---

# Simplify

## Purpose

The post-green pass that strips accidental complexity from working code while preserving exact behaviour. The one thing that must hold: every change carries a before/after rationale a reviewer can read to see why clarity improved without behaviour changing.

## When to use

- After `build` completes and all tests pass.
- The implementation feels heavier than it needs to be — unnecessary nesting, duplication, unclear names.
- A review flags readability or complexity in a working diff.

## Do not use when

- The code is already clear — don't simplify for its own sake. If a new teammate would understand it fast, leave it.
- You don't understand it yet — comprehend first (Chesterton's Fence); if you don't know why it's written this way, don't change it.
- It's a hot path where "simpler" would be slower — benchmark before trading performance for clarity.
- You're about to rewrite the module, or it's throwaway code — simplifying it wastes effort.
- Adding a feature or fixing a bug — open `build`; this skill changes no behaviour.

## Inputs

- Working code: all tests pass, the verification command exits 0.
- The diff to simplify: recently changed code, or code explicitly scoped by the task.
- Project conventions: CLAUDE.md, existing patterns, naming standards.

## Outputs

- Simplified code: reduced complexity, identical behaviour, tests still pass.
- A before/after rationale (see Artefact template) per logical simplification group.
- Reviewable commits: one per logical group (e.g. "extract helper", "rename for clarity"), each passing all tests.

## Workflow

### 1. Gate: confirm working state

Run the verification command from `build`. Confirm exit 0. Do not simplify broken code — fix it first. Record `Verification: <command>`.

### 2. Gate: understand before touching (Chesterton's Fence)

Before changing anything, answer: what is this code's responsibility, what calls it and what does it call, what are the edge cases and error paths, what tests define its behaviour, and why might it be written this way (performance, platform constraint, history — check `git blame`)? If you can't answer, read more context first; you're not ready to simplify.

### 3. Gate: identify opportunities by concrete signal

Each change must match a named signal, not a vibe:

- **Structure** — deep nesting (3+ levels) → guard clauses or helpers; long functions (50+ lines) → focused functions; nested ternaries → if/else or lookup; boolean flag params → options object or separate functions; repeated conditionals → named predicate.
- **Naming** — generic names (`data`, `result`, `temp`) → describe content; abbreviations (`usr`, `cfg`) → full words (keep `id`, `url`); misleading names → rename to actual behaviour; "what" comments → delete; "why" comments → keep.
- **Redundancy** — duplicated logic (5+ lines) → shared function; dead code → remove; value-free wrappers → inline; over-engineered patterns → direct approach; redundant type assertions → remove.

### 4. Gate: apply incrementally, one at a time

Make one simplification, run the verification command, and commit if green; revert and reconsider if it fails. Don't batch untested changes — if something breaks you must know which change caused it. If a refactor would touch more than ~500 lines, automate it (codemod, AST transform) rather than editing by hand.

### 5. Gate: verify the result

After all changes, step back: is the result genuinely easier to understand, consistent with the codebase, and a clean reviewable diff a teammate would approve? If the "simplified" version is harder to follow, revert — not every attempt succeeds.

### 6. Gate: write the before/after rationale

For each logical group, write the rationale (Artefact template below). This is what the reviewer reads to understand the improvement.

## Artefact template

No file artefact. Produce, per logical simplification group:

```
SIMPLIFICATION: <brief title>
Verification: <command> → exit 0

What changed:
- <change, with the signal it matched from step 3>

Why this improves clarity:
- <readability improvement>

Evidence:
- All tests pass ✓
- Diff is clean, no unrelated changes ✓
- Project conventions followed ✓
```

## Red flags

- A simplification that requires editing tests to pass (behaviour likely changed).
- "Simplified" code that is longer or harder to follow than the original.
- Renaming to personal preference rather than project conventions.
- Removing error handling because "it makes the code cleaner."
- Simplifying code you don't fully understand (skipped Chesterton's Fence).
- Batching many simplifications into one large, hard-to-review commit.
- Refactoring code outside the task scope without being asked.
- A before/after rationale that is missing or vague ("cleaned up").

## Exit criteria

1. Working code confirmed at step 1 (verification exits 0).
2. Chesterton's Fence answered — the code's responsibility is understood.
3. Each change matches a concrete signal from step 3.
4. Tests pass after each change; the final verification exits 0 with behaviour unchanged.
5. A before/after rationale is written for each logical group, and each commit names an observable outcome.
6. The diff is clean and reviewable — no unrelated changes.

## Related

- `skills/build/SKILL.md` — source of the working code; simplify is its post-green exit point.
