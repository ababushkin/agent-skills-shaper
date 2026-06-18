# Triage record: eval-trajectory-verification

## Raw intake
<!-- Verbatim capture of the idea as received. Do not edit. -->
A new Verify-stage skill for Shaper that adds an eval layer: rubric-scored output evaluation plus trajectory verification (did the agent run its gates, in order, without skipping). Motivation: gap analysis against the Google/Addy Osmani "New SDLC with Vibe Coding" paper found Shaper rigorously verifies deterministic correctness (tests via build) and applies human judgment (execution-review personas, verify-implementation AC check), but has no eval layer (no rubric-scored, LM-judge, non-deterministic output evaluation) and no trajectory check — the two mechanisms the paper names as what separates agentic engineering from sophisticated vibe coding. Would slot into the Verify stage alongside verify-implementation and execution-review.

## Refined intent
<!-- The confirmed six-line restate from the elicitation loop, in the user's own words. -->
- Outcome: Shaper can verify the *non-deterministic* parts of an agentic build — whether the agent followed its own process (ran each gate, in order, without skipping) and whether artefacts with no deterministic test meet a quality bar (rubric / LM-judge scored).
- User: Supervisors and orchestrators (drain-cycle) that need a "Done" signal they can trust — plus anyone relying on Shaper's "gates are halts" claim.
- Why now: Gap analysis vs the Osmani/Google "New SDLC with Vibe Coding" paper (May 2026): it names trajectory eval + output eval as the line between agentic engineering and sophisticated vibe coding. Shaper has tests (`build`) + persona review (`exec:review`) + AC check (`exec:verify`) but neither of these two.
- Success: A Verify-stage capability that, from a run's durable artefacts (commit trail / `exec-state.json` / AC), emits pass/fail on "gates ran in order, none skipped" and a rubric-scored verdict on non-deterministic outputs — so a ticket can't reach Done on an unproven trajectory.
- Constraint: Markdown-only, stack-agnostic; no guaranteed transcript/runtime access — must work from durable artefacts, can't prescribe an eval framework.
- Out of scope: The consolidation door (`exec:pickup` already provides it); deterministic test running (`build` already does it); building agents-as-products eval suites (separate idea).

**Assumptions surfaced:**
- The durable artefacts of a run (commit trail, `exec-state.json`, ticket AC) capture *enough* to prove a gate ran in order — unverified.
- A rubric-scored / LM-judge eval can be expressed without prescribing a stack or eval framework, consistent with the pack's stack-agnostic constraint.
- This belongs as a distinct Verify-stage capability rather than folded into `exec:review` as a fourth persona — left open as a design question.

**Open questions:**
- Does `exec:state` (or the commit trail) record gate execution order with enough fidelity to detect a skipped or out-of-order gate?
- Own skill vs. a fourth `exec:review` persona vs. an extension of `exec:verify`?
- What is "trajectory" from artefacts alone when no transcript is guaranteed — is the commit/gate trail a sufficient proxy?

## Problem restatement
<!-- "For [customer segment], we believe [problem] is causing [negative outcome]." -->
For supervisors and orchestrators draining Shaper-shaped work, we believe the absence of trajectory and non-deterministic-output verification is causing a trust gap at the Done gate: an agent can claim its gates passed, or ship an artefact with no deterministic test, and nothing independently proves it — which directly undercuts Shaper's "gates are halts" positioning.

## Evidence
<!-- What evidence exists that this problem is real and affects the named customer?
     Be specific: quote, data point, observation. Name the source. -->
- **Direct repo observation (high confidence the gap is real):** `grep` across `skills/build`, `skills/verify-implementation`, `skills/execution-review` for `eval|rubric|LM judge|trajectory` returns nothing. Verification today is deterministic tests (`build` RED/GREEN), AC-vs-diff (`exec:verify`), and human-persona review (`exec:review`). No trajectory check; no rubric-scored eval of non-deterministic output.
- **Expert framework (the why):** Osmani, Saboo, Kartakis — "The New SDLC With Vibe Coding" (Google, May 2026). Names *tests verify the deterministic parts; evals (output + trajectory) verify the non-deterministic parts* as the differentiator between agentic engineering and vibe coding; "set the bar at the eval, not the demo"; "a fluent output that skipped its verification steps is a more dangerous failure than one with a visible error."

Confidence score (Gilad): **2–3** — the gap is a verified fact, but the *value/impact* of closing it rests on an expert framework (no validated behavioural data on Shaper specifically), and feasibility within the stack-agnostic constraint is unproven. Treated as the binding low number for routing.

## Routing
<!-- idea bank | validation slot -->
**Validation slot.** Confidence < 5, and the dominant unknown is **technical feasibility** — can trajectory verification and a stack-agnostic rubric eval be done from Shaper's durable artefacts (commit trail / `exec-state.json` / AC) without prescribing an eval framework or runtime/transcript access?

- Method: **`shape:design` — technical spike.**
- Dominant unknown it resolves: whether the durable run artefacts carry enough signal to prove gate order/completeness and to anchor a rubric eval, and the cleanest insertion point (own skill vs. `exec:review` persona vs. `exec:verify` extension).

## Notes
<!-- Anything a future reader needs: related items, strategic context. -->
- Sibling finding from the same gap analysis (deferred, not triaged here): observability of agent runs (token cost / latency / drift), and two under-used context types (Memory, Examples). The paper defers Memory to its Day-3 companion.
- Related shipped/planned architecture: `exec:pickup` (front door), `exec:review` (= `execution-review`, "best way"), `exec:verify` (= `verify-implementation`, "right thing"), `exec:simplify`. ADR 0004 (execution-verb namespace); rename tracked in ABA-405.
- This idea is the *third* verify axis the paper names — "did the agent build it the way it claimed to" — distinct from "right thing" and "best way."
- No `docs/app-context.md` present; impact grounding is therefore ungrounded (flagged per shape:idea step 4).
