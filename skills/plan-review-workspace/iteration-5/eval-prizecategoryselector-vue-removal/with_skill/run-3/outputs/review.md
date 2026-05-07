# Plan review: prizecategoryselector-vue-removal

## Plan reference

> "Review this plan: remove unused Vue components, starting with PrizeCategorySelector under app/javascript/components/. Should take about a day. Approve?"

## Inputs

- **Appetite**: 1 day (stated)
- **Cynefin domain**: Complicated — "unused" is a knowable claim but requires expertise to verify (static analysis, dynamic import patterns, server-rendered references). Not self-evident.
- **Tier**: Quick — appetite ≤1 day; no one-way door explicitly stated; no ≥3 external dependencies; no schema, auth, or production data touch named.

**Fast-track gate: did not fire.** Precondition 1 fails — removing production Vue components is not in the KTLO/maintenance class (not a dependency version bump, lint config, doc-only change, log cleanup, or dead-test cleanup). Code deletion with a stated "starting with" framing implies a series of changes; fall-through to normal flow.

---

## B1 — Problem framing

The plan opens with a solution: "remove unused Vue components." No problem statement is present. There is no stated user or business outcome (e.g. "reduce bundle size by X KB", "eliminate dead-code surface that complicates onboarding", "unblock a framework migration"). Without a problem statement, it is not possible to verify that deletion is the right response, or to know when the work is complete.

**Verdict: SUSTAINED**
Falsifying condition: a written sentence of the form "we are removing these components because [observable negative outcome], and success means [measurable target]" exists before execution begins.

---

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| "Starting with PrizeCategorySelector" implies a series — the full scope of removal is undeclared | SUSTAINED | A named list of all components targeted in this work session exists, with "starting with" scoped to that list, not to an open-ended future sweep |
| "Unused" is asserted, not defined — no method of usage verification is named | SUSTAINED | The plan names the method used to establish that the component is unused (e.g. "grep + webpack bundle analysis + no references in Rails templates") |
| "Done" state is undefined — no acceptance criterion names what passes after deletion | PARTIAL | CI green + no new console errors in affected pages is named as the exit gate |

---

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| PrizeCategorySelector is truly unused across all import styles (static, dynamic, string-keyed) | 0.1 — assertion only | `grep -r "PrizeCategorySelector" .` across the full repo including ERB/Haml/Slim templates and any JSON-driven component registries; takes < 2 minutes | SUSTAINED |
| No dynamic `import(variableName)` pattern or server-rendered component string references this component at runtime | 0.1 — assertion only | Search for string `"PrizeCategorySelector"` and `'PrizeCategorySelector'` in non-JS files; check any component registry initialisation pattern | SUSTAINED |
| One day is sufficient appetite for this component and the implied follow-on sweep | 0.1 — no scope definition to anchor the estimate | Name the full list of components in scope; re-estimate only after the list is fixed | SUSTAINED |

---

## B8 — Pre-mortem

**Top failure mode (Quick tier):** The component is referenced via a string-based dynamic import (`import(componentName)` where `componentName` is assigned from a data attribute or server-rendered value) or is listed in a Vue component registry keyed by string. Static grep finds no reference; the component is deleted; the code path that loads it silently fails at runtime (blank widget, invisible error) in a state that automated tests do not exercise.

**Kill-switch condition:** Before deletion, run a full-text search for `"PrizeCategorySelector"` (quoted string) across the entire repo — including Ruby templates (`.erb`, `.haml`, `.slim`), JSON fixtures, and any component-registry initialisation files. If any hit is found outside a known import statement, pause and investigate before proceeding.

---

## Recommendation

**APPROVE — recommend: address named conditions before or immediately after deletion.**

**Rationale for APPROVE under carve-out:** The change is fully reversible (one `git revert` restores prior state); no production data, schema migration, auth, or vendor topology is touched; appetite is ≤1 day. Under the Quick-tier reversibility carve-out, SUSTAINED verdicts on B1 (framing), B2 (scope/done-state), and B3 (assumption evidence) downgrade from "block APPROVE" to named recommendations. The skill still records each finding — the owner must see and act on them — but the recommendation is APPROVE rather than REVISE.

### Conditions

1. **Before starting:** Run the full-text grep kill-switch (B8) across all file types including Ruby templates. If any string reference surfaces, stop and investigate.
2. **Before starting:** Write one sentence naming the problem being solved and the measurable outcome expected (B1). This anchors the follow-on sweep and gives future readers a reason the code was removed.
3. **Before starting:** Fix the scope to a named list of components targeted in this work session. "Starting with" is not a scope boundary (B2).
4. **Before merging:** Confirm CI is green and no new console errors appear in pages that previously rendered prize-related flows (B3 / done-state).
5. **After merging:** If bundle size reduction was the stated goal, verify the actual size delta against the expected target. If the metric doesn't move, the assumption that the component contributed to bundle weight was wrong (B1 / Product P1: outcomes not outputs).
