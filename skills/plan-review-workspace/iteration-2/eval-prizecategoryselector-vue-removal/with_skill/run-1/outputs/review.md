# Plan review: prizecategoryselector-vue-removal

## Plan reference

Plan stated in conversation, verbatim:

> "Review this plan: remove unused Vue components, starting with PrizeCategorySelector under app/javascript/components/. Should take about a day. Approve?"

No design doc, ADR, or written artefact was provided.

## Trigger check [GATE]

Triggers fired:

- **Trigger 1** — owner is asking for approval ("Approve?"), so a plan-review pass is owed before the answer.
- **Trigger 3** — the plan touches code (`app/javascript/components/PrizeCategorySelector*`) that has not been traced in this session. The claim "unused" is unverified.

Trigger 4 (auto-fire one-way door) does not strictly fire — code deletion in a tracked repo is git-reversible. However, see B5: a deletion is reversible only if the missing usage was actually missing. Latent runtime references (string-name dispatch, server-rendered template references, dynamic imports) make some Vue-component "removals" effectively one-way once downstream consumers have shipped against the absent component.

Proceeding with review.

## Tier selection

**Tier: Quick.**

Auto-select rules for Full do not fire on stated attributes:

- Appetite is "about a day" — not >1 week.
- No explicit one-way door named in the plan.
- No external dependencies named.
- No production data, schema migrations, or auth touched on the face of the plan.

Quick tier runs B0, B1, B2, B3, B8. Quick-tier reversibility carve-out (Step 12) is in scope and will be evaluated at recommendation.

## Inputs

- **Appetite**: "about a day" — **not a fixed cap**. "About a day" is a range; per Rule C1 / B7, this is a hope, not an appetite. SUSTAINED finding logged into B7-equivalent under B2 below.
- **Cynefin domain**: **Complicated**. Removing dead code is knowable with expertise (grep, build verification, runtime instrumentation), but verifying "unused" across a Rails + Vue codebase requires more than a static search — string-based component references, server-side template rendering, and dynamic imports are knowable but easy to miss. Not Clear.
- **Tier**: Quick — selected because appetite ≤1 week, no one-way door declared, no production-data touch declared.

## B0 — Cynefin classification

Complicated. The review treats "unused" as a claim requiring expert verification, not a given.

## B1 — Problem framing [GATE]

**Verdict: SUSTAINED.**

The plan opens with a solution ("remove unused Vue components"), not a problem. There is no stated user outcome or business outcome that improves once these components are gone. Candidate problems the plan might be solving — bundle size, cognitive load on the JS team, migration off Vue, security surface reduction, build time — are all plausible, but none is named.

**Falsifying condition**: the owner produces a written problem statement of the form "for [audience], [problem] is causing [negative outcome]; removing dead Vue components is expected to move [metric] by [target]." If that exists already and was simply omitted from this prompt, the verdict overturns.

Per Universal P2 and Product Rule A2, a plan that names only a verb-and-object ("remove X") without a problem is incomplete on its face. This is the most important finding in the review — the rest is contingent on it.

## B2 — Scope clarity [GATE]

| Item | Verdict | Falsifying condition |
|---|---|---|
| "Unused" is a claim, not a verified state. The plan does not name how "unused" will be established (grep, AST scan, runtime telemetry, server-template scan). | SUSTAINED | Owner names the verification method and shows it was run against `PrizeCategorySelector` before deletion is staged. |
| "Starting with PrizeCategorySelector" implies a sequence of further removals not enumerated. The plan's true scope is therefore open-ended, not "one component in one day." | SUSTAINED | Owner produces an enumerated list of components in scope (with the same unused-verification applied) or restricts the appetite explicitly to PrizeCategorySelector only. |
| App-wide search for component references is in-scope by implication but not declared. Templates (`.html.erb`, `.html.haml`, `.vue`), JS string references, dynamic imports, and Rails view partials are all surfaces that need scanning. | SUSTAINED | Owner names the search surfaces explicitly (file globs, search tool, regex patterns) and the expected search hits before deletion. |
| Appetite is "about a day" — a range, not a cap. | SUSTAINED | Owner converts this to a fixed appetite ("≤1 working day; ship-or-cut at end of day") with explicit cut criteria. |
| Test coverage for the deletion is not declared. Are there visual regression tests, integration tests, or E2E specs touching the prize-category UI that need to pass post-deletion? | SUSTAINED | Owner names the test suites that must pass and confirms `PrizeCategorySelector` is or is not referenced by any test fixture or spec helper. |
| Build/asset-pipeline implications (Webpacker / Vite / esbuild manifest, sourcemaps, codesplit chunks) not declared in scope. | PARTIAL | Owner confirms whether the build tool is configured to surface dead exports; if yes, deletion is mechanically safe and verdict overturns; if no, custom verification is needed. |

Five SUSTAINED items on a one-day plan is high. The plan is under-specified for its appetite.

## B3 — Assumptions + evidence quality [GATE]

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| `PrizeCategorySelector` is genuinely unused in production. | **0.1** (assertion) | Run `rg -i "prize.?category.?selector" --type-not lock` across the entire repo (not just `app/javascript/`); also grep server-rendered templates, JS string references, and CMS content; check production frontend bundle or telemetry for any runtime mount of the component over the last 30 days. | SUSTAINED — confidence < 5 blocks APPROVE pending the test. |
| The work fits in "about a day" of execution. | **0.1** (assertion) | Owner produces the enumerated list of components to remove (B2) and time-boxes deletion + verification + PR + review per component. If only `PrizeCategorySelector` is in scope, fine; if the "starting with" implies more, the appetite is wrong. | SUSTAINED. |
| Removal has no downstream consumers (other apps, npm-published packages, internal documentation referencing the component). | **0.1** (assertion) | Check whether `app/javascript/components/` is published or referenced as a library, whether any sibling app imports from this path, and whether the component is referenced in any developer docs or onboarding material. | SUSTAINED. |

All three assumptions sit at Confidence 0.1 (opinion / assertion). Per Universal P4 and Step 6, untested assumptions with Confidence < 5 block APPROVE — unless the Quick-tier reversibility carve-out applies (see Step 12).

## B8 — Pre-mortem (Quick: top 1 reason + kill-switch)

**Adopt prospective hindsight.** Assume by end-of-week the plan has failed.

**Top reason it failed:** the component was not actually unused. A latent reference — most likely a string-based component name in a Rails template (`= vue_component "PrizeCategorySelector"` or similar Vue-on-Rails dispatch), or a feature-flagged code path that is rarely-but-not-never executed — broke a user-facing flow in production. The breakage was not caught by tests because no integration test exercised the seldom-used path. The page errored on render for the affected user segment.

**Kill-switch condition (catches it early):**

1. **Pre-deletion**: deploy a one-line instrumentation that fires a structured log event whenever the component mounts in production. Run for 7 days. Zero mounts across the window → safe to delete. Any mounts → the component is not unused; investigate before proceeding.
2. **At-deletion**: stage the deletion behind a feature flag or as a no-op stub that logs and renders nothing for 24 hours before hard-deleting, so runtime references surface as logs rather than 500s.
3. **Post-deletion**: monitor frontend error rate and the prize-category-related page error count for 24 hours; revert on threshold breach.

The `rg`-based static check is necessary but not sufficient — it cannot catch string-dispatch or dynamic imports. The runtime instrumentation is the higher-confidence test.

## Recommendation

**REVISE** — the plan does not currently meet APPROVE criteria. The Quick-tier reversibility carve-out is evaluated below and does **not** apply cleanly enough to override.

**Carve-out evaluation.** The carve-out downgrades B2 and B3 SUSTAINED verdicts to "APPROVE with named recommendation" when the change is fully reversible: one-commit revert restores prior state, no production data touched, no schema/auth/vendor changes. Component deletion is git-reversible, and on its face this looks like a candidate. However:

- A revert restores the file, but does **not** restore any user-facing breakage that occurred between deployment and revert. A latent runtime reference would produce real user-visible errors — page render failures or broken UI flows — during the window the deletion was live. That is not a "bounded by the revert" cost; that is a user-impact cost.
- The plan does not name a rollback path, monitoring threshold, or blast-radius bound. Without those, the assertion "fully reversible" is itself an unverified assumption.
- Universal Rule A5 (KTLO carve-out for the roadmap) requires the work be genuinely keep-the-lights-on. A deletion claimed to improve an unstated outcome (B1 SUSTAINED) is not yet established as KTLO; it is unframed work.

The carve-out therefore does not apply, and the SUSTAINED verdicts on B1, B2, and B3 stand as REVISE-blocking.

If the owner addresses the conditions below, the plan can be re-reviewed and likely approved within the same Quick tier.

### Conditions

The plan must satisfy all of the following before APPROVE:

1. **Problem statement (B1).** State the user-or-business outcome the deletion is expected to move (bundle size? cognitive load? migration progress? security surface?). Name a measurable target where applicable.
2. **Verification method for "unused" (B2, B3).** Name the static search (tool, paths, patterns) and the runtime check (instrument-and-wait, telemetry query, or named owner sign-off). Run the static search and report hit count before deletion is staged.
3. **Enumerated scope (B2).** Either confirm the appetite covers only `PrizeCategorySelector` and other components are out-of-scope, or list the additional components and re-evaluate the appetite.
4. **Fixed appetite (B2).** Convert "about a day" to "≤1 working day, ship-or-cut at end of day" with explicit cut criteria (e.g., "if any runtime reference is found, the day is spent investigating, not deleting").
5. **Rollback + monitoring plan (pre-mortem kill-switch).** Either (a) the runtime-instrumentation pre-check (7 days of mount-event logging, zero mounts → safe), or (b) a deletion-behind-stub for 24 hours, plus the named error-rate threshold that triggers revert.
6. **Test surface confirmation (B2).** Confirm whether any test, fixture, or spec helper references `PrizeCategorySelector`. If yes, plan their handling.

If conditions 1–6 are met and the static + runtime checks return zero hits, the carve-out applies cleanly and the resulting plan is approvable at Quick tier.

### Note on the question itself

The owner asked "Approve?" — the answer is **not yet**. The cost of the conditions above is small (single-digit hours, mostly running searches and writing 3–4 lines of problem framing); the cost of skipping them is the pre-mortem failure mode — a user-visible breakage from a latent reference that the static-only review missed.
