# Triage record: role-based-review-panel

## Raw intake
<!-- Verbatim capture of the idea as received. Do not edit. -->
a multi-axis review using different personas focused on different components of the build. gated to avoid any ineffiencies and similar to how a professional team would conduct a review. the existing one seems to capture most things well, but i want a sub-agent focused on each component with a distinct persona (eg. "you are a system architect and reviewing this implementation). this should remove any redundant personas not used and improve on the one we have.

## Refined intent
<!-- The confirmed six-line restate from the elicitation loop, in the user's own words. -->
- **Outcome:** `exec:review` catches the defect disciplines a senior review team would catch — spec, architecture, correctness, performance, reliability/resilience, security, readability — not just the three narrow defect classes it checks now.
- **User:** the implementing/review agents, and the human who trusts the GO/NO-GO verdict, who run `exec:review` before an issue transitions to Done.
- **Why now:** the gate gives false confidence — three narrow personas pass diffs a senior team would block, and a 5-axis persona already exists but is unwired and duplicated.
- **Success:** each discipline is its own role-based sub-agent persona (incl. a new reliability/resilience reviewer); personas dispatch **conditionally** by the surface the diff touches; output is **judgement-based** (prose verdict + severity); no persona is defined twice.
- **Constraint:** judgement-based output changes the machine-graded finding-triple contract (ADR 0003). The confirmed recommendation extends that contract rather than retiring it, so the fixture grader survives — but it is still a contract change needing a design decision, not an in-place edit.
- **Out of scope:** full security audit / threat modelling; measurement-driven performance profiling; the tracker/Done workflow; any non-review skill.

**Assumptions surfaced:**
- "Component of the build" means review **role/discipline**, not system module — confirmed by the user adding "reliability/resilience reviewer" (a role) to the roster.
- Conditional dispatch needs a reliable way to detect which surfaces a diff touches (path + content heuristics). Assumed feasible.
- Judgement-based personas must still run on non-Claude workers (ADR 0003's portability premise). Assumed, unverified.

**Confirmed in review:**
- **Always-on:** spec-compliance, correctness, and intent-alignment run on every diff; the rest dispatch conditionally by the surface the diff touches.
- **spec-compliance vs correctness are distinct lenses.** spec-compliance asks *did we build what the AC asked for* — the diff against the acceptance criteria. correctness asks *does what we built actually work* — logic, edge cases, broken behaviour, regardless of what the spec wanted. Code can be spec-compliant but buggy, or correct but solving the wrong requirement, so both run on every diff.
- **Model tier:** every review persona runs on the Frontier model. Only a mechanical, deterministic leaf check (enumerable pass/fail, no judgement) drops to Fast. This overrides `sub-agent-anatomy.md`'s current "focused lane = Balanced" default — the spike updates that doc.
- **Role roster:** always-on — spec-compliance, correctness, intent-alignment. Conditional by surface — system-architect, security-engineer, performance, reliability/resilience, readability/quality.
- **Intent-alignment reviewer — scoped in.** A high-level reviewer that asks *did the work achieve the intent behind the AC*, not just the literal AC. It exists because an agent can satisfy the literal AC yet miss the real intent when the AC itself is a subtly-wrong proxy for the end-state — which happened recently (journal, 2026-06-18): a "done when: no file references `<old-name>`" AC passed trivially (grep-for-absence is satisfiable by doing nothing) while the real coupling survived under a second name. It escalates to a human on a critical intent/result deviation and is expected to stay silent on most diffs. Spike detail: stand it up as its own persona (leaning this way, given it's a distinct high-level lens) or fold the check into correctness.

**Recommendation — keep the fixture grader** (the operator does not run it; `bin/grade-execution-review` runs programmatically during persona authoring, not on every live review):
- Don't retire it. It proves the panel still catches the three enumerable defect classes (security-hole, type-suppression, ac-violation) at ≥9/10 recall on the seeded corpus — a cheap regression guard against the panel silently losing coverage on those classes.
- Have the personas that now do judgement *also* emit the gradable triple for those three classes, so the grader keeps running unchanged.
- The judgement-only axes (architecture, correctness, performance, reliability, intent) can't be scored by seeded-defect recall. Evaluate those separately — held-out diffs with expected verdicts, or a periodic human spot-check — not through this grader.
- Net: the grader stays as the floor for the mechanical classes; judgement is layered on top. ADR 0003's contract is *extended* (prose findings alongside the triple), not retired — so no superseding ADR is needed as long as the triple survives for those three classes.

**Open questions:**
- **Downstream coupling with `~/src/drain-cycle`.** drain-cycle consumes this pack's review output programmatically — `drain_cycle/handoff.py` parses structured verdict shapes, and `kr2_check.py` / `grade.py` / `runlog.py` run the grader and record the verdict into the scorecard (ADR 0031). Any change to the verdict format or grader output forces changes in those modules. The spike must scope that downstream impact before any contract edit lands.

## Problem restatement
<!-- "For [customer segment], we believe [problem] is causing [negative outcome]." -->
For the agents and reviewers who rely on `exec:review`'s GO/NO-GO gate before marking an issue Done, we believe the gate's three narrow defect-class personas (plus one dormant duplicate) cause whole defect disciplines — architecture, correctness, performance, reliability — to pass unreviewed, giving false confidence that a diff is ready to merge.

*(No measurable baseline: this is a Markdown skill pack with no `docs/app-context.md` and no runtime metrics. The aim is qualitative — discipline coverage, not a metric delta.)*

## Evidence
<!-- What evidence exists that this problem is real and affects the named customer? -->
Direct inspection of the artefacts (verifiable, read at intake):
- `skills/exec-review/SKILL.md` dispatches exactly three personas; `personas/code-quality.md` states "Your only job is to find type-suppression defects."
- `agents/code-reviewer/AGENT.md` is a complete 5-axis persona that no skill dispatches.

The claim that this lets real defects through is **inferred, not measured** — there's no recorded review that passed an architecture/performance/reliability defect.

Confidence score (Gilad): **~2** — structured observation of the system plus inference; no validated outcome data. Grounding is qualitative (no app-context for a Markdown pack).

## Routing
<!-- idea bank | validation slot -->
**Validation slot — `shape:design` (technical spike → design doc; ADR 0003 extended).**

Confidence < 5, so this earns a validation slot, not a build slot (Rule B6). The dominant unknown is architectural, and there's a potential one-way door: *fully* retiring ADR 0003's triple contract and the fixture grader would break initiative D1's acceptance harness. The recommendation above avoids that door — extend the contract and keep the grader — but the spike must design and confirm it, not edit it in place.

The spike must resolve:
1. **Contract change** — confirm the recommendation: extend ADR 0003 to allow prose findings alongside the triple, keep the grader scoring the three enumerable classes, and design a separate evaluation for the judgement axes. Write a superseding ADR only if the triple is dropped entirely (not recommended).
2. **Role roster + dispatch** — final persona list (including the intent-alignment placement); which are always-on vs conditional; the surface-detection heuristic that decides "did this diff touch the DB / UI / auth?".
3. **Portability** — how judgement-based personas stay usable on non-Claude workers (ADR 0003's reason for the prompt-file format) when output is prose, not triples.
4. **De-duplication** — split `code-reviewer`'s 5 axes into individual role personas; delete the standalone agent so there's one review surface.
5. **Model tiers** — apply the confirmed rule (Frontier for every review persona; Fast only for a mechanical leaf check) and update `sub-agent-anatomy.md` to match.
6. **drain-cycle impact** — audit `~/src/drain-cycle`'s consumption surface (`handoff.py` verdict parsing, `kr2_check.py`, `grade.py`, `runlog.py` scorecard ingestion) against the extended contract, and land any required drain-cycle changes in lockstep so the two repos don't drift.

## Notes
<!-- Anything a future reader needs: related items, strategic context. -->
- The current three personas and the fixture grader serve initiative D1 (`docs/adr/0003-persona-contract-and-dispatch-protocol.md`). This idea extends that work; it does not undo it.
- Related artefacts: `skills/exec-review/SKILL.md` (the skill improved), `agents/code-reviewer/AGENT.md` (the dormant 5-axis persona to split up), `docs/sub-agent-anatomy.md` (authoring spec for the new role personas).
- No `docs/app-context.md` present; impact grounding is qualitative (flagged per shape:idea step 4).
- No comparative score ran (no ranking requested), so no Score section is filed.
