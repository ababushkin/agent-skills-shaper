# Plan review: remove-unused-vue-components

## Plan reference

Inline plan: "Remove unused Vue components, starting with PrizeCategorySelector under app/javascript/components/. Should take about a day. Approve?"

## Inputs

- **Appetite**: ~1 day (fixed cap as stated)
- **Cynefin domain**: Complicated — "unused" is determinable with expert codebase analysis (grep, dynamic-load tracing, build-output check)
- **Tier**: Quick — selected because appetite ≤1 day, no one-way door, no production data/schema/auth touch, <3 external deps. Trigger: owner asked "Approve?" + plan touches code likely not traced this week.

**Step 1a fast-track gate did NOT fire.** Precondition 1 failed: "delete production component code" is not in the enumerated KTLO classes (dependency bump, lint config, doc-only, log/telemetry cleanup, test cleanup). The enumeration is deliberately narrow; deleting Vue components shipped to users sits outside it because "unused" is itself the assumption that needs verification, and getting it wrong removes user-facing behaviour. Falling through to Quick tier.

## B1 — Problem framing

**SUSTAINED.** Plan opens with a solution ("remove unused Vue components") not a problem. Why now? What outcome moves — bundle size, build time, cognitive load on the frontend team, dead-code drift in code review? Without a stated outcome, the work has no success criterion and no stop condition for "starting with PrizeCategorySelector" — i.e. how many components is the goal.

**Falsifying condition**: owner produces a one-line problem statement naming the metric (e.g. "frontend bundle size grew 18% in 6 months; reduce by removing dead components, target -8% gzipped JS") — verdict overturns.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| "Starting with PrizeCategorySelector" implies more components after — count and list undefined | SUSTAINED | Owner names the full list (or a fixed appetite-based stop rule like "as many as fit in 1 day, then stop") |
| Tests, fixtures, storybook stories, i18n keys, and route registrations referencing the component — silently in or out of scope? | SUSTAINED | Plan declares: "remove the component file plus all references found by grep `PrizeCategorySelector`" |
| Backend: any Rails view, controller action, serializer key, or ERB partial that mounts the Vue component — in scope to clean up? | PARTIAL | Plan states whether backend cleanup is in scope or deferred to a follow-up |

Three SUSTAINED/PARTIAL on a 1-day plan — typical signal that "starting with X" framing hides the real scope.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| PrizeCategorySelector is actually unused | 0.5 (anecdote — someone looked and didn't see it) | `rg -n "PrizeCategorySelector" app/ config/ spec/ test/` plus check dynamic loads (`require.context`, `defineAsyncComponent`, kebab-case `<prize-category-selector>`, snake_case in ERB). 5 minutes. | SUSTAINED until grep evidence attached |
| "About a day" is enough for the component plus follow-ups | 0.5 (gut estimate) | Time-box to 1 day as a hard cap; if first component takes >2 hrs end-to-end (find → delete → tests green → PR), reshape | SUSTAINED until appetite is named as a cap |
| No runtime references via string-keyed component registries or server-rendered HTML class hooks | 0.1 (opinion / not yet checked) | Grep production HTML/erb/haml for `prize-category-selector` and `PrizeCategorySelector` strings; check Vue router and any plugin auto-registration | SUSTAINED until checked |

All three Confidence < 5. Under normal Quick rules these block APPROVE — but see Quick-tier reversibility carve-out in the Recommendation.

## B8 — Pre-mortem (Quick: top 1)

**Top failure mode**: PrizeCategorySelector is referenced by a string-keyed dynamic loader (`defineAsyncComponent(() => import(\`./components/${name}.vue\`))`), an admin-only route, or a feature-flagged surface that grep on the kebab/PascalCase tag missed. Removal passes CI (no static reference broke), ships, and the prize-category page 500s for the subset of users who hit it — discovered by a support ticket, not by tests.

**Kill-switch**: before delete, run a production log scan (or staging smoke) for the component's rendered DOM markers / route hits over the last 30 days. If any hits, the "unused" premise is falsified — stop.

## Recommendation

**APPROVE — recommend: attach grep + dynamic-load evidence and a 30-day prod-usage check before deletion; restate as a problem (what outcome moves) and a fixed-cap appetite ("1 day, ship what's done")**

Quick-tier reversibility carve-out applies: plan is fully reversible (one-commit revert restores the deleted component), no production data / schema / auth / vendor touch. SUSTAINED B2 (scope) and B3 (assumptions) downgrade from REVISE-blockers to named recommendations alongside APPROVE. CI + the revert is the runtime safety net. B1 (problem framing) is also surfaced as a recommendation rather than a blocker because the work is bounded by the 1-day cap regardless.

### Conditions (recommendations rather than blockers under the carve-out)

1. **Evidence before delete**: paste the output of `rg -n "PrizeCategorySelector|prize-category-selector|prize_category_selector" app/ config/ spec/ test/ db/` into the PR. Zero hits outside the file itself = safe to delete. Any hit = stop and re-scope.
2. **Dynamic-load check**: confirm there is no `require.context`, `defineAsyncComponent` with template-literal path, or string-keyed registry that could load it without a static reference grep would catch.
3. **Prod-usage check**: 30-day log/analytics scan for the rendered surface, OR an explicit owner sign-off that no such surface exists. If neither is feasible, ship behind a "soft delete" first (rename + console.warn for one release) before hard-removing.
4. **Restate as problem + cap**: one line — "<outcome we want to move>; appetite 1 day as a cap; ship what's done at end of day, list remaining components in a follow-up backlog item."
5. **Stop rule for "starting with"**: name a hard cap (time or count) on follow-on components in this PR, or split into one PR per component.
