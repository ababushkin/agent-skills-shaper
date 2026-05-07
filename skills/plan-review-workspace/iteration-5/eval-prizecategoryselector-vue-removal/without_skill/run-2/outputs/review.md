# Plan Review: Remove Unused Vue Components (PrizeCategorySelector)

## Summary verdict

Not approved as stated. The goal is sound, but the plan is thin — it treats "remove an unused component" as a single-day task without establishing that the component is actually unused, surfacing the blast radius, or naming a verification step. A small amount of upfront work makes this safe; skipping it makes it risky.

---

## What's missing before I'd approve

### 1. Verify "unused" before deleting

"Unused" must be demonstrated, not assumed. Common failure modes:

- Dynamic imports or string-keyed component registrations that grep won't catch
- The component is registered globally (e.g. via `Vue.component('PrizeCategorySelector', ...)`) and referenced in templates by name
- It's used in a test file, a story (Storybook), or a fixture — not in production code, but still a deletion that breaks the build
- It's conditionally imported in a file that's hard to reach in dev

**Required step:** run a dead-code search that covers: `import`, `require`, `components:` blocks, `Vue.component`, dynamic `() => import(...)`, and template string usage. Show the output. If zero references, deletion is clean. If any, they each need a decision.

### 2. Name the blast radius

The plan says "remove unused Vue components" (plural) but only names one. Questions I'd want answered:

- Is this one component or a set? If a set, list them.
- Does `PrizeCategorySelector` compose other components that are only used through it? If so, those are also candidates — or they become orphaned and confusing.
- Does it import any CSS, assets, or utilities that would also become orphaned?

### 3. Define "done"

A day is a reasonable appetite for this work, but there's no exit criterion. Done should mean:

- Component file(s) deleted
- All import/registration references removed
- Build passes (no broken imports)
- Test suite green
- No dead CSS or asset references left behind
- The PR is reviewed by someone who knows the codebase well enough to catch a missed reference

### 4. Risk of the "one day" estimate

Removing a single, genuinely unused component is 30 minutes of work, not a day. If it's actually a day, that implies either:
- There are more components in scope than named
- There are references to clean up
- There's surrounding clean-up (tests, Storybook stories, CSS)

Clarify which. If it's genuinely 30 minutes, say so and use the rest of the day for something else. If it's a day, name what fills it.

---

## What's good about this

- Deleting dead code is unambiguously positive — it reduces cognitive load, bundle size, and future maintenance surface
- Starting with one named component is a good instinct (small batch, reversible)
- The appetite ("about a day") is in the right ballpark for a conservative deletion task with cleanup

---

## Approval condition

Approve this after seeing:

1. A grep/search output confirming zero live references to `PrizeCategorySelector`
2. A complete list of files to be deleted (component + any co-located tests/stories)
3. Confirmation that no downstream components become orphaned

If all three are clean, this is a green-light task with low risk. The verification work is probably 30–60 minutes, which fits within the stated appetite.
