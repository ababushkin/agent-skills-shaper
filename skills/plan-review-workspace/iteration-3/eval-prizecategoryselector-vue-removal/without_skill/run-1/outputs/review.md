# Plan Review: Remove unused Vue components (PrizeCategorySelector)

## Summary

The plan proposes removing unused Vue components from `app/javascript/components/`, starting with `PrizeCategorySelector`, with an estimated effort of about a day. This is a small, low-risk cleanup task — but the plan has one critical unverified assumption that needs to be addressed before approval.

## Assessment

### Scope and risk
This is a Complicated-tier change (in Cynefin terms): the practice of dead-code removal is well-understood, the steps are knowable, and the change is reversible (it's just `git revert`). It's not Chaotic or Complex — there's no novel discovery required. Appetite of ~1 day is appropriate; this should be a Quick review, not a Full architectural review.

### The load-bearing assumption: "unused"

The entire plan rests on the claim that `PrizeCategorySelector` (and other components) are unused. This claim is **not verified in the plan**. In a Vue/Rails codebase mounted via `app/javascript/components/`, components can be referenced in ways that a casual `grep` will miss:

- Direct imports in other `.vue`/`.js`/`.ts` files (`import PrizeCategorySelector from ...`)
- Global registration via `Vue.component('prize-category-selector', ...)` and then used in templates by kebab-case tag name
- Mounted by name from Rails ERB/HAML/Slim templates (e.g., a `data-component="PrizeCategorySelector"` mount pattern, or a `<prize-category-selector>` custom element in a server-rendered template)
- Dynamic imports / async components: `() => import('./PrizeCategorySelector.vue')`
- Referenced by string in a registry (component map, route config, feature flag config)
- Referenced from tests, fixtures, Storybook stories
- Referenced by external code (a separate gem, engine, or admin panel) that mounts into the same JS pack

A one-day estimate that assumes "unused" without showing the verification work is the risk here, not the deletion itself.

### Verdict by axis

- **Problem framing (B1):** OK — "remove dead code to reduce maintenance surface" is a legitimate, if implicit, problem.
- **Scope (B2): SUSTAINED.** The "unused" claim is unverified. This is the central concern.
- **Reversibility:** OK — pure deletion, fully reversible via git. Two-way door.
- **Appetite/sizing:** OK — one day is reasonable for one component plus verification, possibly tight if the list of "other unused components" is long.
- **Operability:** OK — no production behaviour change if the components are genuinely unused.
- **Sequencing:** OK — starting with one component is the right call (small batch).

## What needs to change before approval

Before deleting, demonstrate the component is unused. Concrete falsifying checks:

1. **Static reference search (case- and kebab-case-aware):**
   ```
   rg -i "PrizeCategorySelector|prize-category-selector|prize_category_selector" \
      --glob '!node_modules' --glob '!*.lock'
   ```
2. **Search Rails templates (`.erb`, `.haml`, `.slim`) for component-mount patterns** — especially `data-component=`, `data-vue-component=`, or any custom mounting helper this app uses.
3. **Check the Vue component registry** — find where components are globally registered (often `app/javascript/packs/application.js` or similar) and verify `PrizeCategorySelector` is not registered there. If it is registered globally, references can be by tag name only and won't show up under the PascalCase grep.
4. **Check the asset pipeline / bundler manifest** — if the component is in a separate chunk or pack entry, it may be loaded dynamically.
5. **Check tests and fixtures** — `app/javascript/**/*.spec.*`, `*.test.*`, Storybook `*.stories.*`.
6. **Run the test suite after deletion** and exercise the app paths that historically used the prize-category feature to confirm no runtime errors.
7. **Check git log / blame** for the component to understand when and why it was added — if it was recently added behind a feature flag, "unused" may mean "not yet rolled out" rather than "dead."

If all checks come back clean, deletion is safe and the appetite holds. If any reference surfaces, the plan needs to be reshaped (either keep the component, or do the broader removal of its callers as part of the same change).

## Recommendation

**REVISE.** The work is the right work and the appetite is right, but the plan needs a verification step before the deletion step. Add:

> "Before deleting each component: run the static reference checks above (PascalCase, kebab-case, snake_case across JS, Vue, Rails templates, and the component registry). Document zero-reference confirmation in the PR description. If any reference is found, stop and reassess."

With that change, this is a one-day, two-way-door cleanup — approve. Without it, it's a one-day cleanup that has a non-trivial chance of breaking a production page that wasn't on anyone's mind.

## What this review is NOT

Not a Full architectural review — that would be over-review for a reversible, sub-day cleanup. The point is a single, concrete falsifying check, not a re-litigation of the project.
