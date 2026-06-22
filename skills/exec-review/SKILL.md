---
name: exec:review
description: >
  Multi-persona execution review — dispatches spec-compliance, security-auditor, and
  code-quality personas over a working-tree diff and aggregates a single deduped GO/NO-GO
  verdict. Spec compliance is reviewed first so built-the-wrong-thing is caught before
  built-it-badly. Use before any issue is transitioned to Done.
  Trigger phrases: "review this diff", "run execution review", "review before Done",
  "multi-persona review", "fan-out review", "check the diff against AC and security".
---

# Execution Review

## Purpose

A single lens misses defect classes it is not oriented to find. This skill dispatches three narrow personas in a fixed order — spec compliance, then security, then code quality — so the aggregate surfaces what any one reviewer would miss alone. Spec compliance runs first because built-the-wrong-thing must be caught before built-it-badly (the wrong sequence means the code-quality pass validates work that will be thrown away). The three personas emit structured finding triples; this skill deduplicates and aggregates them into one GO/NO-GO verdict.

## When to use

- Before any issue is transitioned to Done — the minimum review gate.
- When an implementing agent claims the diff satisfies the ticket and you want an independent multi-lens check before committing.
- Any time you need a defensible review trail that separates spec, security, and quality concerns.

## When not to use

- **Threat modelling or full security audit** — exec:review's security-auditor persona catches structural patterns; it does not replace a dedicated security audit on high-risk surfaces.
- **Style or formatting review** — use the `code-simplify` skill for readability-only pass.
- **Plan or spec review** — use `plan-review` or `exec:verify` for AC verification outside a diff.

## Inputs

- The working-tree diff (`git diff HEAD` or equivalent)
- The issue or task statement (for the spec-compliance lens)
- The acceptance criteria from the issue (spec-compliance reads these before the code; pass them explicitly if not embedded in the issue)

## Outputs

A review-summary block with:

- **Verdict**: `GO` / `NO-GO`
- **Finding count by severity**: `Critical: N · Required: N · Suggested: N`
- **Findings** (deduped, ordered spec → security → quality): each on one line — `<file> <class> <severity>`
- **Next step**: one sentence on what the implementing agent must do

## Workflow

**1. Load context.**
Before reading the diff: load `docs/adr/0003-persona-contract-and-dispatch-protocol.md` (dispatch rules), the issue statement, and the acceptance criteria.

**2. Dispatch personas — spec compliance first.**
Dispatch in this fixed order: `spec-compliance` → `security-auditor` → `code-quality`. On **Claude Code**, dispatch all three via the `Agent` tool in a single batched message (one `Agent` call per persona, parallel); the fixed order governs the *reporting* sequence, not the runtime sequence. On **non-Claude workers** (codex, kimi, or any worker without an Agent fan-out tool), run the personas inline-sequentially: load `personas/spec-compliance.md`, apply it to the diff, capture findings; then repeat for `personas/security-auditor.md`; then `personas/code-quality.md`.

Each persona receives:
- The working-tree diff as its primary input
- The issue statement and AC list (spec-compliance uses these; the other two may reference them for context)

**2a. Mark the active persona (display marker).**
On entry to each persona — before applying it to the diff — write the `_active` pointer into `exec-state.json` at the worktree root, so the live swimlanes view shows the active review persona on every worker, not just Claude Code:

```json
{"_active": {"step": "review", "persona": "spec-compliance"}}
```

Set only the `_active` key, preserving the phase sections (`pickup`, `breakdown`, `build`, …); write a temp file and rename it over `exec-state.json` so the update is atomic. `persona` is a single string under last-write-wins: on Claude Code's parallel dispatch each persona sub-agent writes its own name on entry and the most-recent write is the one shown; on a non-Claude worker running inline-sequentially, write the pointer before each persona in turn. The write is one local file per persona — the pointer is sub-1 KB — with no network call. The renderer reads this pointer for display only — it never gates the run, so a missed or stale write degrades the view, never the work.

**3. [GATE] Collect and deduplicate findings.**
Gather the raw finding triples from all three personas. Deduplicate on the match key `(file · defect_class · severity)` — if two personas surface the same triple, count it once. A finding that appears in two personas is not more severe; it is one finding with corroboration.

**4. Aggregate verdict.**
- **NO-GO** if any Critical or Required finding remains after deduplication.
- **GO** if all remaining findings are Suggested or Note.

**5. Emit the review-summary block.**
Use the template below. Report findings in order: spec-compliance findings first, then security-auditor, then code-quality. Within each group, Critical before Required before Suggested.

## Artefact template

```markdown
## Review summary

**Verdict:** GO / NO-GO
**Findings:** Critical: N · Required: N · Suggested: N

### Spec compliance
- `<file>` · `ac-violation` · Required — <one sentence>
  (or: *none*)

### Security
- `<file>` · `security-hole` · Critical — <one sentence>
  (or: *none*)

### Code quality
- `<file>` · `type-suppression` · Critical — <one sentence>
  (or: *none*)

**Next step:** <one sentence — what the implementing agent must do, or "ready to commit" on GO>
```

## Common rationalisations

| Rationalisation | Counter |
|---|---|
| "Tests are passing so the spec compliance lens is unnecessary." | Tests verify what was tested, not what the AC required. The spec-compliance persona reads the AC directly against the diff — it cannot be substituted by a test run. |
| "I already did a code review — running three personas is overkill." | A single reviewer has a single orientation. The three lenses are narrow by design; overlap is deduped, not double-counted. The cost is one extra dispatch; the benefit is two defect classes the single reviewer wasn't looking for. |
| "Security is obvious — I'd have caught it manually." | Security findings have a strong availability bias: the obvious ones get caught; the structural ones (hardcoded secrets, string-concatenated queries) get normalised. The security-auditor persona's orientation is to find what the implementing agent normalised. |
| "The spec-compliance persona needs the full AC list, which I don't have." | If the AC is not in context, stop and retrieve it. A spec-compliance check run without the AC is a security theatre exercise: it will find nothing because it has nothing to check against. |

## Red flags

- Findings emitted by one persona and ignored because the other personas didn't flag them — deduplication merges, it does not suppress.
- NO-GO verdict issued without naming the specific finding that blocks merge — the implementing agent needs a file and a class to act on.
- GO verdict on a diff with non-trivial changes and zero findings — check that all three personas actually ran and received the diff.
- Spec-compliance persona run without the issue's AC list in context — it cannot check compliance against AC it has not loaded.

## Verification / exit criteria

The skill has run correctly when:

1. All three personas ran and received the same diff.
2. The finding list is deduplicated on `(file · defect_class · severity)`.
3. The verdict is NO-GO if any Critical or Required finding is present.
4. The review-summary block names the file and defect class for every finding.
5. `bin/grade-execution-review fixtures/execution-review --persona fan-out` exits 0 with ≥9/10 recall.

## References

- `docs/adr/0003-persona-contract-and-dispatch-protocol.md` — dispatch protocol and finding-triple format
- `personas/spec-compliance.md` — spec-compliance persona prompt
- `personas/security-auditor.md` — security-auditor persona prompt
- `personas/code-quality.md` — code-quality persona prompt
- `fixtures/execution-review/` — seeded-defect corpus and grader
- `bin/grade-execution-review` — grader script (exit 0 = ≥9/10 recall, the KR2 gate)
- `rules/eng-principles-agentic.md` — P4 (evidence beats vibes), P6 (stop the line on first failure)
- `rules/eng-principles-universal.md` — P1 (shipped is not done; observed is done)
