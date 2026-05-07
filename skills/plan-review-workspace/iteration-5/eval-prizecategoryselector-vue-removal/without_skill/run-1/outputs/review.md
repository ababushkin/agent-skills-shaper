# Plan Review: Remove PrizeCategorySelector Vue Component

## Summary verdict

**Not approved as stated.** The intent is reasonable, but the plan is underspecified for safe execution. One day is plausible only if the component is genuinely unused — which has not been verified in this plan. That verification step needs to happen before the work is scoped, not during it.

---

## What the plan gets right

- Removing dead code is a legitimate, low-glamour engineering task that improves codebase health.
- Scoping to a single component is appropriately narrow.
- A one-day appetite is not unreasonable for a removal task if the groundwork is done.

---

## What's missing or risky

### 1. "Unused" hasn't been defined or verified

The plan asserts the component is unused, but doesn't say how that was determined. "Unused" in a Vue/Rails app can mean different things:

- Not imported anywhere in JS/TS files (static analysis)
- Not rendered in any template (`.vue`, `.erb`, `.html`)
- Not dynamically referenced (string-based component registration, `resolveComponent()`, dynamic `<component :is="...">`)
- Not loaded via a backend-driven component registry or feature flag that assembles component names at runtime

Static grep for imports is not sufficient. If any of these dynamic patterns exist in the codebase, a component can appear unused while still being rendered in production. The plan should document what analysis was done.

### 2. No mention of tests

Is there a test file for this component? Spec files, Cypress/Playwright tests, or Storybook stories that reference `PrizeCategorySelector` would break after removal. The plan doesn't address this.

### 3. No rollback or verification step

Removing a component is a one-way door only if it's not in version control — and it is, so reverting is trivially cheap. But the plan should still name how you'll verify the removal was safe: does the app boot, do relevant tests pass, is there a staging environment to spot-check?

### 4. Scope is unclear beyond the single file

A component removal often involves:
- The component file itself (`PrizeCategorySelector.vue`)
- Any associated test files
- Any index re-exports that reference it
- Any route or view that may import it indirectly
- Any i18n keys or translation strings used only by that component
- CSS/SCSS that may be scoped to it or co-located

The plan says "starting with PrizeCategorySelector" — which implies more work to follow — but doesn't say what the full surface is, even for this one component.

### 5. No mention of why now

Why is this being done today? Is it blocking something? Is it part of a larger cleanup? The answer matters for prioritisation, not execution — but "approve?" implies someone is making a prioritisation call and they should have the context.

---

## Recommended changes before approval

1. **Show the usage analysis.** Run `grep -r "PrizeCategorySelector" app/javascript/` and `grep -r "PrizeCategorySelector" app/views/` and share the output. If zero hits (beyond the component definition), say so explicitly.
2. **Check for dynamic registration patterns.** A quick scan for `resolveComponent`, `components:` registrations, and `<component :is>` usages that could reference this component by string.
3. **List all files in scope.** The component file, its test file(s), any re-exports. The checklist should be enumerable before the work starts.
4. **Add a verification step.** "Run test suite, boot app locally, check staging" — whatever the team's standard is. Name it.

---

## Bottom line

The work itself is low-risk and the appetite is plausible. The gap is that "unused" is an assertion, not a demonstrated fact. Thirty minutes of analysis before approval would make this a clean, confident removal rather than a removal that might cause a production incident from a dynamically-referenced component that nobody knew was still live.

Approve after the usage analysis is shared.
