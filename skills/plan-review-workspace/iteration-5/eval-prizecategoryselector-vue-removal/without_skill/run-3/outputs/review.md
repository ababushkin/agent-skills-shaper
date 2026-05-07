# Plan Review: Remove Unused Vue Components (PrizeCategorySelector)

## Summary judgment

**Not approved as stated.** The plan is directionally reasonable but underspecified. One day is plausible if the component is genuinely unused and the scope is narrow — but the plan as written gives me no basis to verify either claim. Before approving, I want answers to the questions below.

---

## What the plan gets right

- Scoping to a single named component (`PrizeCategorySelector`) rather than "all unused components" is good. Removing dead code is healthy, and doing it in small, targeted batches is the right approach.
- A one-day appetite is appropriately small and forces a natural scope constraint.

---

## What I'm not satisfied with

### 1. "Unused" needs to be verified, not assumed

The most important question is: how was "unused" determined? Vue components can be referenced in ways that static analysis misses:

- Dynamic `<component :is="...">` with a string component name
- Registration via `Vue.component('PrizeCategorySelector', ...)` in a plugin or initializer
- References in non-JS files: ERB templates, Haml, server-rendered HTML that mounts components by name string
- Feature-flagged paths that are currently off but still wired up
- Test files, Storybook, or visual regression fixtures

If "unused" means "I grepped the string `PrizeCategorySelector` and found no hits," that's not sufficient. I'd want a confirmation that the search covered all of the above, especially the Rails view layer if this is a Rails + Vue app (the path `app/javascript/` is a strong signal it is).

### 2. Scope is stated as singular but opened as plural

The plan title says "remove unused Vue components" (plural), then names one. Is PrizeCategorySelector the only one being removed in this task, or is it the first of a set? If it's a batched cleanup, the one-day estimate needs to account for the full batch, not just one component. If it's truly just one component, fix the title.

### 3. No mention of tests

If there are any tests importing or rendering `PrizeCategorySelector` directly, those need to be removed too. Deleting the component without deleting associated tests will break CI. If there are no tests (which is possible for legacy components), that's worth noting — not as a blocker, but as a data point about coverage.

### 4. No mention of what happens after deletion

- Does anything need to be re-registered or de-registered in a component registry or plugin file?
- Is there an index file (`components/index.js` or similar) that re-exports it?
- Is there a Webpack/Vite chunk configuration that references it?

None of these are blockers, but a complete plan names them.

### 5. No rollback consideration

For a deletion task this is low stakes, but worth a sentence: is there a straightforward way to verify the removal didn't break anything before merging? Running the full test suite and doing a quick smoke-test of the affected feature area (prize categories) would be the minimum bar.

---

## Recommended pre-approval steps

1. Run a comprehensive usage search covering JS, TS, ERB, Haml, Vue templates, and any dynamic component registration. Share the output.
2. Confirm whether this is one component or a batch — and if a batch, which ones.
3. Confirm test coverage (or absence) for the component.
4. Note any barrel exports or registry entries that also need updating.

If those come back clean, approve immediately — this is the right kind of housekeeping and the one-day estimate is fine.
