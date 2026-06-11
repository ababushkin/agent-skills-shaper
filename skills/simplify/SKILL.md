---
name: simplify
description: >
  Reduce complexity after code is green. Use after build passes but implementation is heavier
  than it needs to be — simplify for clarity while preserving exact behavior, leaving a
  reviewable before/after rationale.
pack: engineering
lifecycle_stage: refactor
principles_implemented:
  - source: eng-agentic
    id: P5
    bucket: embedded
  - source: eng-universal
    id: Rule B1
    bucket: embedded
  - source: eng-universal
    id: Rule C3
    bucket: embedded
length_target: 300–350
author: Anton Babushkin
predecessor:
  repo: https://github.com/addyosmani/agent-skills
  skill: code-simplification
  relation: port
kept_from_predecessor: "Five principles (preserve behavior, follow conventions, clarity over cleverness, balance, scope); Chesterton's Fence pattern analysis; concrete simplification table patterns; language-specific examples; common rationalisations and red flags (agent-skills)"
changed_from_predecessor: "[GATE] markers on verification steps; before/after rationale requirement; post-green-build context; anatomy-compliant section order; integration as build skill exit point; verification checklist tied to build-skill handoff"
---

# Simplify

## Purpose

simplify is the post-green pass that reduces accidental complexity while preserving exact behaviour.
It is not refactoring for its own sake — it is clarifying code written under build pressure, making
it easier to read, modify, and review. The gate is the before/after rationale: a reviewer must be
able to read your explanation and understand why each change improves comprehension without changing
what the code does.

## When to use

- After `build` skill completes and all tests pass (post-green-build pass).
- When implementation feels heavier than it needs to be.
- When code is working but contains unnecessary nesting, duplication, or unclear names.
- When reviewing a diff and readability or complexity issues are flagged.

## When not to use

- **Code is already clear** — don't simplify for the sake of it. "Would a new team member understand
  this faster?" If yes, don't touch it.
- **You don't understand it yet** — comprehend before you simplify. Chesterton's Fence: if you don't
  understand why it's written this way, don't change it.
- **Performance-critical path and "simpler" would be slower** — benchmark first. Don't trade performance
  for clarity without measurement.
- **You're about to rewrite the module** — simplifying throwaway code wastes effort.
- **Feature or bug fix** — this skill does not add behaviour or fix broken tests. Open `build` instead.

## Inputs

- Working code: all tests pass, verification command exits 0.
- The diff to simplify: recently changed code, or code explicitly scoped by task.
- Project conventions: CLAUDE.md, existing codebase patterns, naming standards.

## Outputs

- Simplified code: reduced complexity, same behaviour, tests still pass.
- Before/after rationale: a written explanation of what changed and why each change improves clarity.
- Reviewable commit: one commit per logical simplification group (e.g., "extract helper", "rename
  for clarity"), each passing all tests, with a message naming the simplification outcome.

## Workflow

**1. [GATE] Verify working state — all tests pass before simplifying.**

Run the verification command from `build` skill context. Confirm exit 0. Do not simplify broken
code — fix it first.

Record: `Verification: <command>` (from build skill).

**2. [GATE] Understand Before Touching (Chesterton's Fence).**

Before changing or removing anything, understand why it exists.

Answer these questions about the code to simplify:
- What is this code's responsibility?
- What calls it? What does it call?
- What are the edge cases and error paths?
- Are there tests that define the expected behaviour?
- Why might it have been written this way? (Performance? Platform constraint? Historical reason?)
- Check git blame: what was the original context for this code?

If you can't answer these, read more context first. You're not ready to simplify.

**3. [GATE] Identify Simplification Opportunities — Concrete Patterns Only.**

Scan for these signals — each one is a concrete pattern, not a vague smell:

**Structural complexity signals:**
- Deep nesting (3+ levels) → Extract conditions into guard clauses or helper functions
- Long functions (50+ lines) → Split into focused functions with descriptive names
- Nested ternaries → Replace with if/else chains, switch, or lookup objects
- Boolean parameter flags → Replace with options objects or separate functions
- Repeated conditionals → Extract to a well-named predicate function

**Naming and readability signals:**
- Generic names (`data`, `result`, `temp`, `val`) → Rename to describe content
- Abbreviated names (`usr`, `cfg`, `btn`) → Use full words (except universal abbreviations: `id`, `url`)
- Misleading names (function named `get` that mutates state) → Rename to reflect actual behaviour
- Comments explaining "what" → Delete; the code is clear enough
- Comments explaining "why" → Keep; they carry intent the code can't express

**Redundancy signals:**
- Duplicated logic (5+ lines repeated) → Extract to a shared function
- Dead code (unreachable branches, unused variables, commented blocks) → Remove
- Unnecessary abstractions (wrapper that adds no value) → Inline the underlying function
- Over-engineered patterns (factory-for-a-factory) → Replace with the simple direct approach
- Redundant type assertions (casting to already-inferred type) → Remove

Do NOT simplify on vibes. Each change must match a signal from the patterns above.

**4. [GATE] Apply Changes Incrementally — One at a Time, With Tests.**

Make one simplification. Run the verification command. If tests pass, commit (or continue to next
simplification). If tests fail, revert and reconsider.

DO NOT batch multiple simplifications into one untested change. If something breaks, you must know
which simplification caused it.

**The Rule of 500:** If a refactoring would touch more than 500 lines, invest in automation (codemods,
sed scripts, AST transforms) rather than making changes by hand. Manual edits at that scale are
error-prone and exhausting to review.

**5. [GATE] Verify Result — Before and After Comparison.**

After all simplifications, step back and evaluate:

- Is the simplified version genuinely easier to understand?
- Did you introduce patterns inconsistent with the codebase?
- Is the diff clean and reviewable?
- Would a teammate approve this change?

If the "simplified" version is harder to understand or review, revert. Not every simplification
attempt succeeds.

**6. [GATE] Write Before/After Rationale — Gate Artefact.**

For each logical group of simplifications (e.g., "extract helper functions", "rename for clarity"),
write a brief before/after rationale. This is what reviewers read to understand the improvement.

Format:
```
SIMPLIFICATION: <brief title>

What changed:
- <change 1>
- <change 2>

Why this improves clarity:
- <readability improvement 1>
- <readability improvement 2>

Evidence:
- All tests pass ✓
- Diff is clean ✓
- Project conventions followed ✓
```

Example:
```
SIMPLIFICATION: Extract multi-layer validation into predicate function

What changed:
- Extracted nested if-chain at lines 45–67 into `isValidUser(user)` helper

Why this improves clarity:
- Call site now reads `if (isValidUser(user)) { ... }` instead of nested 3-level conditions
- Validation logic has a name that describes intent, not just control flow
- New team member can understand "is user valid?" without parsing nesting

Evidence:
- All tests pass ✓
- Helper is used only in one place (no over-engineering)
- Predicate name matches project naming conventions ✓
```

## Artefact template

No file artefact. Produce:

```
Verification: <command>

[CHESTERTON'S FENCE]
Code responsibility: <description>
Why written this way: <reason or "no reason found">
Ready to simplify: Yes/No (if No, explain what to research first)

[SIMPLIFICATIONS ATTEMPTED]
1. <Simplification 1>
   - Signal: <pattern from step 3>
   - Change: <what changed>
   - Tests: PASS/FAIL
   - Commit: <message if PASS>

2. <Simplification 2>
   ...

[BEFORE/AFTER RATIONALE]
Simplification 1: <rationale per step 6 template>
Simplification 2: <rationale per step 6 template>
...

Final verification: <command exit code>
```

## Common rationalisations

| Rationalization | Reality |
|---|---|
| "It's working, no need to touch it" | Working code that's hard to read will be hard to fix when it breaks. Simplifying now saves time on every future change. |
| "Fewer lines is always simpler" | A 1-line nested ternary is not simpler than a 5-line if/else. Simplicity is about comprehension speed, not line count. |
| "I'll just quickly simplify this unrelated code too" | Unscoped simplification creates noisy diffs and risks regressions. Stay focused on recently changed code. |
| "The types make it self-documenting" | Types document structure, not intent. A well-named function explains *why* better than a type signature explains *what*. |
| "This abstraction might be useful later" | Don't preserve speculative abstractions. If it's not used now, it's complexity without value. Remove and re-add when needed. |
| "The original author must have had a reason" | Check git blame. But complexity often has no reason; it's residue of iteration under pressure. |
| "I'll refactor while adding this feature" | Separate refactoring from feature work. Mixed changes are harder to review, revert, and understand in history. |

## Red flags

- Simplification that requires modifying tests to pass (you likely changed behaviour).
- "Simplified" code that is longer and harder to follow than the original.
- Renaming things to match your preferences rather than project conventions.
- Removing error handling because "it makes the code cleaner."
- Simplifying code you don't fully understand (skipped Chesterton's Fence).
- Batching many simplifications into one large, hard-to-review commit.
- Refactoring code outside the scope of the current task without being asked.
- Before/after rationale missing or vague ("cleaned up" without explaining what or why).

## Verification / exit criteria

The skill has run correctly when:

1. Working code confirmed at step 1 (verification command exits 0).
2. Chesterton's Fence questions answered — code responsibility understood.
3. Each simplification matches a concrete signal from step 3 patterns.
4. All tests pass after each change (step 4 incremental verification).
5. Before/after rationale written for each logical simplification group.
6. Final verification command exits 0 — behaviour unchanged, tests still pass.
7. Each simplification commit passes verification and names an observable outcome.
8. Diff is clean and reviewable — no unrelated changes mixed in.

## References

- `skills/build/SKILL.md` — source of working code; simplify is the exit point after GREEN
- `rules/eng-principles-agentic.md` — P5 (polish when green)
- `rules/eng-principles-universal.md` — Rule B1 (readability is a feature), Rule C3 (code as prose)
- Predecessor: `agent-skills/code-simplification` (MIT) — five principles, pattern analysis,
  Chesterton's Fence, concrete simplification table
