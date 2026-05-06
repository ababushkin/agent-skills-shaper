# Plan review: vue-unused-components-removal

## Plan reference

Inline plan: "remove unused Vue components, starting with PrizeCategorySelector under app/javascript/components/. Should take about a day. Approve?"

## Inputs

- **Appetite**: ~1 day (stated as "about a day" — not a fixed cap; flagged in B7)
- **Cynefin domain**: Complicated — knowable with expertise (static analysis + grep + runtime check), but "unused" is a claim that needs verification, not a given
- **Tier**: Quick — selected because appetite ≤1 day, no one-way door declared, no schema/auth/production-data touch
- **Fast-track gate**: did not fire. Precondition 1 fails — "remove unused components" is not in the enumerated KTLO classes (dep bump, lint, doc, log/telemetry, test cleanup). Precondition 2 is conditional on the "unused" claim being true; if a component is actually referenced, removal is not one-commit reversible without user-visible regression.

## B1 — Problem framing

**Verdict: SUSTAINED.** The plan opens with a solution ("remove unused Vue components") and a target file (`PrizeCategorySelector`). No problem statement: no user, no business outcome, no metric to move. Why now? What does carrying these components cost — bundle size, build time, cognitive load, security surface, all four? Without the problem statement, there is no way to judge whether `PrizeCategorySelector` is the right starting point or whether the work is worth doing at all.

**Falsifying condition**: the plan states the problem (e.g. "JS bundle is 480 KB and we suspect ~15% is dead Vue code; we want to cut bundle size by 10% to improve TTI on 3G") with a measurable target.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| "starting with PrizeCategorySelector" implies more components after — but how many, which ones, and where does the day's appetite end? | SUSTAINED | The plan names a finite, listed set of components in scope (e.g. "PrizeCategorySelector, FooBar, Baz") OR an explicit stopping rule (e.g. "stop at end of day, ship what's removed") |
| "unused" is undefined — unused at compile time? at runtime? in any user role? in any A/B branch? in any feature flag? in any locale? | SUSTAINED | The plan defines "unused" with a verification method (e.g. "no static import in app/javascript or app/views, no dynamic mount string, zero runtime renders in last 30 days of frontend telemetry") |
| `app/javascript/components/` likely exports a public surface — index files, registries, possibly Stimulus or Vue plugin registrations. The plan does not name what else gets touched when a component file is deleted. | PARTIAL | The plan lists the dependent files (index.ts/js, registries, route configs, tests) that get edited alongside the component deletion |

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| `PrizeCategorySelector` is unused | 0.5 (anecdote — someone looked and thought so) | Run `git grep -i prizecategoryselector` across app/, config/, public/, spec/, test/, plus dynamic-string search for "PrizeCategory" and "prize-category"; check frontend telemetry (component mount events) over last 30 days; check feature-flag configs | SUSTAINED |
| The component is not loaded dynamically (string-keyed registry, route param, server-rendered partial naming the component) | 0.1 (assertion) | Grep for the kebab-case and snake_case variants of the name; check if there is a Vue component registry or dynamic `import()` pattern in this codebase | SUSTAINED |
| One day's appetite is enough for "components" (plural) — implies ≥2 and possibly many | 0.1 (assertion) | Owner names the count and confirms each one's verification has been done OR scopes the day to "PrizeCategorySelector only, evaluate after" | SUSTAINED |

All three assumptions sit at Confidence < 5. Universal P4 / Product P4: untested assumptions at this confidence block APPROVE — except under the Quick-tier reversibility carve-out (see Recommendation).

## B8 — Pre-mortem (Quick: top 1 + kill-switch)

**Top failure mode**: One of the components removed turns out to be loaded dynamically (string-keyed Vue component registry, server-rendered ERB referencing the component name, feature-flagged code path, or admin-only route the developer didn't exercise). The deploy looks clean in CI, then a user hits the path the next day and sees a blank panel or a JS console error. Because the plan has no telemetry check and no staged rollout, the regression is discovered by the user, not by the team.

**Kill-switch condition**: before merging the deletion, run a grep for every kebab-case, snake_case, and camelCase variant of each component name across the entire repo (not just `app/javascript/`) — including `app/views/`, `config/`, `public/`, `spec/`, `test/`, and any feature-flag config files. If any match exists outside the component's own file and its co-located test, stop and investigate before deleting. Secondary: if frontend telemetry exists, confirm zero mount events for the component over the last 30 days. If neither check is feasible, do not proceed.

## Recommendation

**REVISE** — three SUSTAINED B3 assumptions at Confidence ≤0.5, plus SUSTAINED B1 (no problem statement) and SUSTAINED B2 (scope and "unused" both undefined). The Quick-tier reversibility carve-out is not safely available here: although a deletion can be reverted in one commit, a user-visible regression between deploy and revert is not bounded by the revert (the user has already seen the error), so the "fully reversible" precondition does not hold in the operational sense the carve-out assumes.

### Conditions

The plan must satisfy these before APPROVE:

1. **Problem statement (B1)**: name the user or business outcome and the metric to move (e.g. bundle KB, TTI, build time, maintenance load), with a target.
2. **Define "unused" operationally (B2, B3)**: name the verification method — static grep across the full repo (not just `app/javascript/`), dynamic-string variants checked, telemetry confirmation if available, feature-flag configs checked. Document the method so the same bar applies to the next component.
3. **Scope the day (B2)**: either list the specific components in scope for this day, or declare "PrizeCategorySelector only, then re-evaluate." A vague "starting with X" is not a scope.
4. **Verification before deletion (B3)**: for each component in scope, run the verification method from condition 2 and record the result. Untested removal is the failure mode.
5. **Staged merge (B8)**: merge each component's deletion as a separate commit so revert is per-component, not all-or-nothing. Watch for client-side errors or 404s on JS chunk requests for at least one business-day window before declaring the removal done.
6. **Optional but recommended**: if there is no frontend error telemetry that would catch a missing-component runtime error within 24h of deploy, add a smoke test that exercises the routes and partials that previously rendered each removed component before merging.
