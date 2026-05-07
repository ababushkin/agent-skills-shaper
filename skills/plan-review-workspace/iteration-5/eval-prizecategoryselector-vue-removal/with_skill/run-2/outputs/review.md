# Plan review: prizecategoryselector-vue-removal

## Plan reference

> "Review this plan: remove unused Vue components, starting with PrizeCategorySelector under app/javascript/components/. Should take about a day. Approve?"

## Inputs

- **Appetite**: ~1 day (stated; cap not yet fixed — see B7 note)
- **Cynefin domain**: Clear — known cause-effect; find unused component, delete it, verify tests pass
- **Tier**: Quick — no one-way-door decision stated, appetite ≤1 week, no production-data/schema/auth touch

## Fast-track gate: did not fire

Precondition 2 fails. "Fully reversible" requires that the component is confirmed to have zero consumers before deletion. The plan contains no such evidence. A deletion of code believed-unused-but-actually-used breaks a user-visible feature; a git revert after the fact does not prevent the incident. Proceeding to normal Quick flow.

## B0 — Cynefin classification

**Clear.** Known cause-effect chain: identify unused component → delete file → verify no breakage → ship. Review is checklist-level coverage.

## B1 — Problem framing

**SUSTAINED.**

The plan opens with a solution ("remove unused Vue components") and states no problem. There is no user or business outcome named. Why does a single unused component matter? Possible answers: build-time overhead, dead-code maintenance burden, confusion for future authors, bundle size. Any of these would be a legitimate problem statement — but none is present.

*Falsifying condition*: A revised plan that opens with "For [audience], [unused component X] causes [measurable negative outcome]. Removing it is expected to [outcome target]" would overturn this verdict.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| "starting with PrizeCategorySelector" — the word "starting" implies a multi-component sweep, but no list of candidates, no stopping condition, and no criteria for inclusion are stated | SUSTAINED | Plan names the complete candidate list or explicitly limits this plan to PrizeCategorySelector only, with separate planning for any subsequent components |
| "unused" is undefined — no definition of what zero-consumer means (static import, dynamic string key, route registration, plugin registry, template literal reference) | SUSTAINED | Plan states the exact search method used and its coverage (e.g. "grep + vue-i18n key scan + webpack bundle analysis") |
| Associated artefacts — test files, SCSS, i18n keys, and Storybook stories colocated with the component are not mentioned | PARTIAL | Plan explicitly enumerates which associated files will be removed alongside the `.vue` file, or states a rationale for leaving them |

Three SUSTAINED items surfaced on a ≤1-day plan. B2 re-run is not needed; the plan is narrow enough that these are material, not noise.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| PrizeCategorySelector has zero consumers (no static import, no dynamic `() => import(...)`, no string-keyed registration) | 0.1 — assertion; no evidence cited in the plan | Run: `grep -r "PrizeCategorySelector" app/javascript/ --include="*.{js,vue,ts}"` and `grep -r "prize-category-selector" app/javascript/ --include="*.{html,erb,haml}"`. Also check for dynamic registration via string keys in any plugin/router config. Owner must confirm results before deletion. | SUSTAINED |
| ~1 day is a reliable appetite for this scope | 0.1 — no basis given; multi-component scope ("starting with") makes this especially uncertain | Owner names the concrete tasks and confirms each fits the day budget: discovery scan + deletion + test run + PR review | SUSTAINED |
| Deletion (vs. archive or feature-flag removal) is the right remediation | 0.1 — no alternatives considered | Owner confirms no active A/B test, no rollback scenario, and no contract with a downstream consumer (e.g. a native wrapper or an iframe embed) that references the component path | SUSTAINED |

All three assumptions score 0.1 on Gilad's scale. Per B3 rules, untested assumptions with Confidence < 5 block APPROVE.

## B8 — Pre-mortem

**The plan has already failed. Top reason:**

PrizeCategorySelector is dynamically imported via an async chunk or registered under a string key in a plugin/router configuration that the static grep did not scan. The component is deleted; no CI test exercises that code path (common for feature-gated or role-gated UI). The failure surfaces in production when a user with the relevant role or feature flag reaches the view — not in the test suite, and not in the PR review.

**Kill-switch condition:** Run the application in staging (or run the full integration test suite, if it covers this feature path) with the component file deleted — not just the unit test suite — before merging. If the staging environment is unavailable or the feature is behind a flag that isn't toggled in staging, the kill-switch is: confirm via codebase search (grep + AST analysis) that every reference path is covered before proceeding.

## Recommendation

**REVISE**

Three conditions must be addressed before APPROVE:

1. **State the problem.** Add a one-sentence problem statement that names the outcome the deletion is expected to produce (e.g. "Removing dead code reduces ongoing maintenance surface and eliminates confusion for new contributors").

2. **Evidence unusedness.** Run and attach the output of a multi-pass consumer search — static imports, dynamic imports, string-keyed registrations, ERB/Haml templates, and any native or iframe embed that references the component path. Owner signs off on the search coverage.

3. **Fix scope.** Either (a) limit this plan explicitly to PrizeCategorySelector and commit to a separate plan for subsequent components, or (b) name the complete candidate list and the criteria used to select it, with an appetite that reflects the full sweep.

### Conditions

| # | Condition | Blocks |
|---|---|---|
| 1 | Problem statement with named outcome | B1 SUSTAINED |
| 2 | Consumer search output attached and confirmed zero-hit by owner | B3 Assumption 1 SUSTAINED |
| 3 | Scope boundary fixed (single component or named list with criteria) | B2 item 1 SUSTAINED + B3 Assumption 2 SUSTAINED |
| 4 | Deletion confirmed over archive/flag: no active A/B test, no downstream contract on component path | B3 Assumption 3 SUSTAINED |
