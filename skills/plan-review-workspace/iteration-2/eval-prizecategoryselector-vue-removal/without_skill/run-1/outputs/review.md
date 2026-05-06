# Plan review: remove unused Vue components (starting with PrizeCategorySelector)

## Verdict

**Do not approve as written.** The intent is reasonable (deleting dead code is good hygiene), but the plan as stated is too thin to greenlight. It needs concrete proof of "unused" and a defined scope before it gets a day of engineering time. I'd send it back for a short tightening pass — not kill it.

## What the plan says, restated

- Goal: remove unused Vue components from `app/javascript/components/`.
- First target: `PrizeCategorySelector`.
- Estimate: ~1 day.
- Asks for approval to proceed.

## What's good

- Deleting dead code is unambiguously a positive activity when the code is genuinely dead. It reduces cognitive load, shrinks the bundle, removes maintenance burden, and prevents future contributors from cargo-culting patterns from a component nobody uses.
- Starting with a single named component (`PrizeCategorySelector`) is the right shape — incremental, reviewable, reversible.
- A one-day appetite is appropriate for this kind of cleanup. It's small enough to not need elaborate planning, big enough to make a real dent.

## What's missing or unclear

### 1. No evidence the component is actually unused

This is the critical gap. "Unused" needs to be demonstrated, not asserted. Vue components in a Rails/Hotwire-adjacent codebase can be referenced in many non-obvious ways:

- Direct imports in other `.vue` / `.js` / `.ts` files.
- Registration in a global Vue app (`Vue.component('prize-category-selector', …)`).
- Mount points in ERB/HAML/Slim templates referencing the component name as a custom element or via `data-controller`/`data-component` attributes.
- Dynamic imports (`import(\`./components/\${name}.vue\`)`) where the component name is constructed at runtime.
- References from tests, fixtures, or Storybook stories.
- References from feature flags / experiments where it's behind a toggle that's currently off (still "used" in the codebase sense).
- References from admin tools, internal dashboards, or seldom-trafficked routes.

Before approving, the plan should include the search evidence: results of grep across `app/`, `config/`, `spec/`, `test/`, `lib/`, `db/seeds`, plus a check for kebab-case (`prize-category-selector`), snake_case, and dynamic string usage. A single `rg PrizeCategorySelector` is the minimum bar; ideally also confirmation it's not bundled by webpack/vite output.

### 2. No defined scope beyond the first component

"Starting with PrizeCategorySelector" implies more components after it, but there's no list. Is this 1 component or 12? The "about a day" estimate is meaningless without knowing the denominator. A good version of this plan either:

- Constrains to just `PrizeCategorySelector` (and re-plans afterwards), or
- Lists the candidate set up front with the same evidence-of-unused check applied to each.

### 3. No success criterion / verification plan

How will we know the removal didn't break anything? The plan should name:

- Test suite passes (unit + system).
- Asset build succeeds (webpack/vite/esbuild).
- A representative pass through any pages that historically used or might still reference the component.
- Bundle size delta as a sanity check (a real removal should shrink the bundle; if it doesn't, something is still pulling it in).

### 4. No rollback plan

This is dead code removal, so rollback is just `git revert` — but the PR should be a single, focused commit that's trivially revertable. Worth stating explicitly so it doesn't get bundled with unrelated cleanup.

### 5. Why this, why now?

What prompted picking `PrizeCategorySelector` specifically? Is it the largest? The most confusing? Recently noticed during another change? A one-line rationale helps reviewers calibrate whether this is the highest-value cleanup target or just the most convenient one. If the goal is ongoing dead-Vue cleanup, a quick survey (e.g. `webpack-unused`, `ts-prune`, or a manual audit) would identify the best candidates rather than starting with whichever one was top-of-mind.

### 6. Vue version / migration context

If the codebase is mid-migration (Vue 2 → Vue 3, or Vue → Hotwire/Stimulus, or anything similar), "unused Vue components" may actually be "components in the deprecated stack we're walking away from." That changes the framing — the plan becomes part of a larger deprecation story, not standalone hygiene. Worth a sentence either way.

## Suggested shape for an approvable plan

A revised plan I'd approve looks roughly like:

> **Goal:** remove `PrizeCategorySelector` (and any other dead Vue components surfaced during the audit).
>
> **Evidence of unused:** `rg` results across `app/`, `config/`, `spec/`, plus check of dynamic-import patterns and global registrations. Component name searched in kebab/snake/Pascal case. Findings: zero references except the file itself.
>
> **Scope this PR:** delete the `.vue` file, remove from any explicit registration list, remove associated tests/stories if any. One commit.
>
> **Verification:** `bundle exec rspec`, `yarn build`, manual smoke of [list of pages]. Bundle size delta reported.
>
> **Rollback:** `git revert <sha>`.
>
> **Follow-up:** if audit surfaces N more candidates, list them; each gets its own PR.
>
> **Appetite:** half a day for the named component; rest of day for follow-up audit if signal is strong, otherwise stop.

That's still a one-day plan. It's just defensible.

## Risks worth naming

- **False-positive "unused":** the most common failure mode. A component is grep-invisible because it's referenced by computed name or via ERB, then the removal silently breaks a page nobody noticed in QA.
- **Coupled deletions:** removing `PrizeCategorySelector` may surface that its child components or shared utilities are now also unused. Plan should either include or explicitly exclude follow-on cleanup.
- **Test coverage of the removal:** if the only thing testing that the page works is a system spec that's currently flaky or skipped, deletion can break production with green CI.

## Bottom line

Approve the *intent*. Don't approve the *plan as written*. Ask for: evidence of unused, defined scope, verification steps, and a one-line rationale for picking this component first. Once those are added, this is a 30-minute review followed by a half-day execution — easy yes.
