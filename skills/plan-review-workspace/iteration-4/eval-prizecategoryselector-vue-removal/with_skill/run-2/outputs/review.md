# Plan review: remove-unused-vue-components

## Plan reference

Inline plan from owner: "remove unused Vue components, starting with PrizeCategorySelector under app/javascript/components/. Should take about a day. Approve?"

## Inputs

- **Appetite**: ~1 day (stated, but soft — "about a day", not a fixed cap)
- **Cynefin domain**: Complicated — deadness of a Vue component is knowable with expertise (grep, route configs, dynamic-import scan), but not a Clear deterministic checklist
- **Tier**: Quick — selected because appetite ≈1 day, no schema/auth/production-data touch, fully revertible per commit
- **Trigger fired**: #1 (owner about to approve), #2 (≈1 day, borderline), #3 (component usage not personally traced this week)

### Fast-track gate evaluation

Fast-track gate did **not** fire. Precondition #1 (KTLO class) fails: "deletion of components believed unused" is not analogous to the gate's KTLO examples (lint config, doc-only, dependency bump, deleting `.skip`'d tests). In all those cases the deadness signal is unambiguous; here, "unused" is an unverified assumption. Vue components can be referenced via `<component :is>`, route definitions, dynamic imports, server-rendered templates, or string-keyed registries — none caught by a naive grep. Falling through to Quick flow so B3 (assumptions) gets a real pass.

## B1 — Problem framing

The plan opens with a solution ("remove unused Vue components") with no stated outcome. No bundle-size target, no maintainability metric, no developer-velocity claim, no specific pain incident. **Verdict: SUSTAINED (PARTIAL)** — the activity is plausibly useful but the plan does not name what improves when it lands. **Falsifying condition:** owner names a measurable outcome (e.g. "reduce JS bundle by ≥X KB", "eliminate N components flagged by `vue-unused` audit", "remove maintenance burden of N components no team owns") and a way to observe it post-merge. Without that, "done" reduces to "files deleted" — Universal P1 / Product P1 violation.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| "starting with PrizeCategorySelector" implies an open-ended sequel — what's the full list, and where does this 1-day budget end? | SUSTAINED | Owner produces an enumerated list of N components with a per-component budget, OR explicitly scopes this PR to PrizeCategorySelector only and treats the rest as a separate plan |
| Imports, route registrations, Vuex/Pinia store entries, i18n keys, CSS partials, and tests associated with the component — are all of these in scope for deletion? | PARTIAL | Plan states "delete the component file plus all transitively-orphaned references (routes, store modules, i18n strings, sibling CSS, spec files)" |
| Storybook stories, fixture files, factories, and any backend serializer fields that exist solely to feed the component — in scope? | PARTIAL | Plan states whether backend-side cleanup (serializer attributes, GraphQL fields, API endpoints feeding only this component) is in or explicitly out of scope |

Three items surfaced; appetite is ~1 day so re-running aggressively is not required.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| `PrizeCategorySelector` is actually unused | 0.5 — anecdote / static guess | Run: `rg -l "PrizeCategorySelector" app/ config/ spec/`; check route configs, dynamic `component :is` usages, string-keyed component registries, and server-rendered ERB/HAML templates that may name it. Check git log for last reference. **Block until done.** | SUSTAINED |
| The component is not loaded by an admin-only or feature-flagged path that the dev environment doesn't exercise | 0.1 — opinion | Grep for the component name in feature-flag definitions, admin route files, and rake tasks. Confirm with whoever owns the prizes domain. | SUSTAINED |
| "About a day" covers the full sweep (find candidates + delete + verify + ship) | 0.5 — anecdote | Time-box the first component end-to-end (incl. CI + manual smoke). If it takes >2 hours, the day-budget for the whole sweep is wrong. | SUSTAINED |

All three assumptions sit at Confidence < 5. Per skill rule, untested assumptions with Confidence < 5 block APPROVE — but the Quick-tier reversibility carve-out applies (one-commit revert restores prior state, no production data / schema / auth touched).

## B8 — Pre-mortem (Quick: top 1)

**Top failure mode:** The component is referenced via a non-static path the static search missed — most likely `<component :is="dynamicName">` driven by a string from the backend, or a route that's only hit by an admin/feature-flagged user. Production users on that path see a "Failed to resolve component" console error and a broken page. The dev/CI suite never exercised it because no test covers that route.

**Kill-switch:** Before merging, run `rg -i "prizecategoryselector"` across the **entire repo** (including backend, config, i18n, public/), not just `app/javascript/`. Additionally: deploy behind a soft-delete (rename to `_deprecated_PrizeCategorySelector` or move to a `_graveyard/` folder for one release) before hard-deleting. If no errors surface in production logs / Sentry within one release cycle, hard-delete in the follow-up.

## Recommendation

**APPROVE — recommend: (1) run the full-repo grep + dynamic-usage check before any deletion; (2) soft-delete (rename / quarantine folder) for one release before hard-delete; (3) explicitly scope this PR to PrizeCategorySelector only, with the broader sweep as a separate plan; (4) name a measurable outcome (bundle bytes saved or count of components removed) that's checked post-merge.**

Quick-tier reversibility carve-out applies: SUSTAINED verdicts on B1 (problem framing — treated as a B-bucket finding), B2 (scope), and B3 (assumptions) downgrade to APPROVE-with-recommendation rather than REVISE, because the change is fully reversible by single-commit revert and touches no production data, schema, auth, or vendor topology.

### Conditions

1. Before deleting any component, run `rg -i "<component-name>"` across the whole repo (not just `app/javascript/`), check route configs, check for `<component :is>` and dynamic import patterns, and skim git log for the last meaningful reference.
2. Soft-delete first (rename or move to a `_graveyard` folder) and observe one release in production before hard-deleting.
3. Scope this PR to `PrizeCategorySelector` only; treat the wider sweep as a separate plan with its own budget.
4. Name the outcome being moved (bundle bytes / count removed / maintenance hours reclaimed) and confirm it post-merge — otherwise this is feature-factory cleanup work (Product P1).
5. If the first component takes >2 hours end-to-end (search + delete + transitive cleanup + CI green + manual smoke), revisit the 1-day appetite for the broader sweep before continuing.
