# Plan review: prizecategoryselector-vue-removal

## Plan reference

> "Remove unused Vue components, starting with PrizeCategorySelector under app/javascript/components/. Should take about a day. Approve?"

## Trigger check
Trigger 2 fires (work described will take ~1 day; right at the threshold). Trigger 3 also plausibly fires (component removal touches code the owner may not have personally traced this week — "unused" is the very claim under question). Proceeding.

## Step 1a — Fast-track gate

The fast-track gate requires **all four** preconditions. Check:

1. **Class is KTLO/maintenance?** **NO.** The Step 1a precondition list is closed: dep bumps, lint/format, doc-only, log/telemetry cleanup, test cleanup. Deleting application source code (Vue components) is not on that list. Removing "unused" components is a behavioural change conditional on the unused claim being true — and verifying that claim is itself the work, not maintenance.
2. Fully reversible? Mostly (one-commit revert restores files), but precondition 1 fails first.
3. Appetite ≤1 day? Yes.
4. No major-version anything? Yes.

**Gate does NOT fire** — precondition 1 fails (component deletion is not KTLO). Falling through to normal flow.

## Inputs
- **Appetite**: ~1 day (cap, as stated)
- **Cynefin domain**: Complicated — knowable with expertise (grep, runtime trace, route audit). Cause-effect of "is this component referenced" is determinable with the right investigation; not emergent.
- **Tier**: Quick — sub-day appetite, no one-way-door auto-fire, no production-data/schema/auth touch, no >1-week appetite. (Code deletion is reversible by revert.)

## B1 — Problem framing

The plan opens with a solution ("remove unused Vue components") not a problem. The implied problem — dead code carrying maintenance/cognitive load, or perhaps a Vue-to-other-framework migration cleanup — is unstated. **Verdict: PARTIAL.** Falsifying condition: a one-line problem statement exists somewhere in the broader project context (e.g., "we are decommissioning Vue in favour of <X>", or "audit revealed N unused components costing build time"). Without that, the plan is solution-first per Universal P2.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| The word "unused" is asserted, not verified — no method named for confirming PrizeCategorySelector is actually unreferenced | **SUSTAINED** | A grep/ripgrep across the repo (templates, JS, ERB, HAML, route/controller refs, dynamic `import()` strings, asset manifests, test fixtures, seed data) shows zero references to `PrizeCategorySelector` outside its own file. Until that grep is run and pasted in, "unused" is an assumption. |
| "starting with" implies a series of removals but the series is not enumerated | **SUSTAINED** | A list exists naming the N components in scope for this day's work, with a stop condition (e.g. "today: PrizeCategorySelector + 3 others; rest in follow-up"). Otherwise "starting with" is open-ended and the day-appetite is unenforceable. |
| Dynamic component resolution not addressed (Vue supports `<component :is="name">` and string-based registration) | **SUSTAINED** | A search for `:is=`, `Vue.component(`, dynamic `require`/`import` calls, and any registry/factory pattern shows none reference PrizeCategorySelector by string. Static grep alone is insufficient when dynamic resolution is in play. |

(Three SUSTAINED on a sub-day plan is high — the plan's core claim ["unused"] is unverified, which is the same defect surfacing in different ways.)

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| PrizeCategorySelector has zero runtime references | **0.5** (anecdote — "looks unused") | `rg -n 'PrizeCategorySelector' app/ config/ db/ test/ spec/` + check for kebab-case variant `prize-category-selector` and dynamic `:is` | **SUSTAINED** — Confidence < 5 |
| The full sweep of "unused Vue components" fits in one day | **0.5** (estimation without enumeration) | Run the audit first (e.g. `vue-unused`/`unimported`/static analysis); count candidates; then commit to appetite | **SUSTAINED** — Confidence < 5 |
| No tests, fixtures, or stories cover this component (so removing it won't redden CI) | **0.1** (opinion) | `rg -n 'PrizeCategorySelector' --type=js --type=ts --type=vue test/ spec/ stories/ cypress/`; run the suite locally | **SUSTAINED** — Confidence < 5 |

All three riskiest assumptions sit at Confidence ≤ 0.5. The 5-minute tests are cheap (literally minutes) and would lift confidence to 5+ before any deletion happens.

## B8 — Pre-mortem

**Top failure mode (end-of-week):** A component flagged as "unused" by static grep is actually loaded dynamically — via `<component :is="someStringFromAPI">`, a registry lookup, or string-keyed `Vue.component()` registration. Deletion lands; QA misses it because the code path is conditional on a specific user state or feature flag; the regression surfaces in production a week later when a customer hits the path. Revert is one commit, but blast radius is "users couldn't pick prize categories" and the thing was supposed to be a cleanup.

**Kill-switch:** before deleting any component, require the deletion PR to include (a) the grep output showing zero static references, (b) explicit confirmation that no dynamic-resolution patterns exist in the file's surface area, and (c) a smoke test of the page(s) that historically used the component, even if now believed unused. If any of those is missing, the PR doesn't merge.

## Recommendation

**REVISE** — the plan's core claim ("unused") is an unverified assumption, B2 surfaces three SUSTAINED items, and the appetite is set against an unenumerated scope. This is not a Quick-tier reversibility carve-out APPROVE-with-recommendation: while the change is technically reversible by `git revert`, the pre-mortem failure mode (dynamic resolution missed by grep, regression hits production) is the kind of defect the carve-out is not designed to absorb — it's a behavioural defect, not a clean revert-and-forget.

### Conditions

1. Run the verification first: `rg -n 'PrizeCategorySelector|prize-category-selector' app/ config/ db/ test/ spec/ lib/` (or equivalent). Paste results into the plan.
2. Search for dynamic-resolution patterns: `<component :is=`, `Vue.component(`, registry/factory lookups. Confirm none reach PrizeCategorySelector by string.
3. Enumerate "starting with" — list the N components in scope today, with a stop condition that fits the one-day appetite. If the audit reveals >N candidates, the appetite is wrong and needs reshaping.
4. Each deletion PR carries the grep evidence inline, plus a one-line smoke-test note for the page(s) the component used to render on.
5. Re-submit for a 2-minute re-review once the above are in the plan; expect APPROVE.
