# Plan review: prizecategoryselector-vue-removal

## Plan reference

> "Remove unused Vue components, starting with PrizeCategorySelector under
> `app/javascript/components/`. Should take about a day. Approve?"

## Inputs

- **Appetite**: 1 day (stated; treated as fixed cap)
- **Cynefin domain**: Complicated
- **Tier**: Quick — selected because appetite ≤ 1 week and no explicit one-way-door
  declaration in the plan text; however, see B5 below

**Fast-track gate: did NOT fire.**
Precondition 1 (KTLO/maintenance class): partially met — dead-code removal is
maintenance. Precondition 2 (fully reversible) cannot be confirmed: the plan
asserts the component is "unused" but provides no evidence. If the assertion is
wrong, revert restores the file but cannot undo a production breakage that
already fired (broken route, failed render, missing dynamic import). The untested
assumption breaks the fast-track reversibility guarantee. Falling through to
normal Quick-tier flow.

---

## B0 — Cynefin classification

**Complicated.** The cause-effect is knowable with expertise but is not obvious
from the plan: "unused" must be established by static analysis and dynamic
tracing (dynamic `import()` calls, string-keyed component registrations,
server-side Rails view references). An expert can verify it; the plan does not
show the work.

---

## B1 — Problem framing

The plan opens with a solution action ("remove unused Vue components") rather
than a problem statement. There is no articulation of why the removal matters —
reduced bundle size, reduced test surface, reduced cognitive load, or something
else — and no measurable target.

**Verdict: SUSTAINED**

Falsifying condition: the plan names a measurable outcome (e.g., "reduce JS
bundle by X KB", "eliminate Y stale test fixtures") and the business or
engineering reason the change is worth a day of work now.

At Quick tier with a reversible plan this is a named recommendation, not a hard
block. However, the reversibility carve-out requires confirmed reversibility,
which B3 below puts in question.

---

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| "Starting with PrizeCategorySelector" implies a multi-component sequence — the full list is undeclared | SUSTAINED | The plan names every component in the removal sequence and confirms each will be verified unused before deletion |
| Dynamic imports (`import(/* webpackChunkName */ './PrizeCategorySelector')`) are not in-scope in the plan but are the most common source of false-positive "unused" calls | SUSTAINED | The plan confirms the static-analysis pass covers dynamic import paths, not just static `import` statements |
| Test fixtures, Storybook stories, or snapshot files that reference the component are not mentioned | PARTIAL | The plan names test/story cleanup as in-scope or explicitly states those files are absent |

**Note:** Zero clean items on a 1-day plan with no prior context would be the
failure mode; three SUSTAINED/PARTIAL hits is consistent with a Quick-tier
check on a low-context plan.

---

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| PrizeCategorySelector is unused | 0.1 — assertion only; no grep, bundle analysis, or dynamic-import trace shown | Run `grep -r "PrizeCategorySelector" app/ spec/ --include="*.{vue,js,ts,erb,rb}"` + check webpack/Vite chunk manifest for the component name | SUSTAINED — confidence below threshold |
| No other components in the declared sequence are used either | 0.1 — implied by "starting with", no evidence | Run same grep for each component before touching it | SUSTAINED — untested assumption about future work |
| Appetite of 1 day is sufficient for verify + delete + test + review for the full sequence | 0.5 — rough estimate, no component count given | Name the total component count; estimate 30–60 min per component including grep, delete, test run, PR | PARTIAL |

Confidence < 5 on two assumptions; both are SUSTAINED. These block APPROVE under
normal Quick-tier rules unless reversibility is confirmed. Reversibility is not
confirmed (see B1/B3 interaction above).

---

## B4 — Dependencies

*(Quick tier — abbreviated)*

No cross-team dependencies are visible in the plan. If PrizeCategorySelector is
referenced from a Rails view (`.erb` template) or a Stimulus controller, a
back-end team may be implicated. The plan does not mention this. Not a hard block
at Quick tier, but owners should grep `.erb` files before deleting.

---

## B5 — Reversibility + ADR pairing

*(Quick tier — abbreviated)*

Code deletion is recoverable via `git revert` — this is a two-way door in the
git sense. However, if the component is in active use (see B3), deleting it
causes a production breakage that git revert cannot roll back automatically
(deployments, CDN caches, error states in user sessions). The reversibility is
therefore conditional on the "unused" assumption being true. An ADR is not
required for dead-code removal; no one-way-door architecture decision is present.

**Verdict: PARTIAL** — reversibility is only guaranteed if the unused assumption
(B3, Confidence 0.1) is validated first. The standard Quick-tier reversibility
carve-out does not apply until that validation is done.

---

## B8 — Pre-mortem

*(Quick tier: top 1 reason + kill-switch)*

**Top failure mode:** PrizeCategorySelector is dynamically imported via a
string-based route (`import(\`./\${componentName}\`)`) or registered under a
different name in a component registry, so the static grep returns zero hits and
the team concludes it is unused. The component is deleted. A production route
that depends on the dynamic import 404s. The defect surfaces only in a specific
user flow (prize category selection) that the standard test suite does not cover.

**Kill-switch:** Before any deletion, run the full Vite/webpack production build
and confirm the component name does not appear in any generated chunk manifest.
If it appears, stop. Do not proceed with deletion until the reference is traced
and removed first.

---

## Recommendation

**REVISE** — two SUSTAINED B3 assumptions at Confidence 0.1 block APPROVE; the
Quick-tier reversibility carve-out does not apply because reversibility is
conditional on those same untested assumptions.

### Conditions

The plan must satisfy all three before re-approval:

1. **Verify "unused" before committing to deletion.** Run a grep across
   `app/`, `spec/`, and template files (`.erb`, `.html`) for
   `PrizeCategorySelector`. Run a second pass against the Vite/webpack chunk
   manifest to catch dynamic imports. Document the result inline in the PR
   description.

2. **Name the full component list.** "Starting with" implies a sequence. The
   plan must enumerate all components targeted, or scope the current plan to
   PrizeCategorySelector only and treat the sequence as a separate future plan.

3. **State the outcome.** Name the engineering reason for the removal (bundle
   reduction, dead-code hygiene, maintenance overhead) so the post-deletion
   impact review has something to measure against. A one-line addition to the PR
   description satisfies this.

None of these conditions requires significant additional work — they are
verification steps, not redesign. A revised plan that includes the grep output
and a stated reason can be re-approved immediately.
