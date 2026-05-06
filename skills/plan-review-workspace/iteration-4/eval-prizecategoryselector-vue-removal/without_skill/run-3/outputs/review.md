# Plan Review: Remove unused Vue components (starting with PrizeCategorySelector)

**Verdict: Do not approve as written. Reshape and re-submit.**

The plan is too thin to approve responsibly. "Remove unused Vue components" sounds like routine cleanup, but deletion is a one-way door against a runtime-dynamic frontend stack, and the plan doesn't address the things that make these deletions safe.

---

## What's missing

### 1. Definition of "unused" is not stated
This is the load-bearing question. Vue components can be referenced in ways static analysis misses:
- Dynamic component resolution: `<component :is="someName">`, where `someName` is a string built at runtime.
- Async/lazy registration: `defineAsyncComponent(() => import(...))` with computed paths.
- Server-rendered templates (Rails ERB, Slim, HAML) that mount Vue components by name string.
- Stimulus controllers, ViewComponents, or partials that reference the Vue component by tag name.
- Tests, Storybook stories, fixture data, or i18n keys that reference the component.
- External consumers: emails, admin tools, marketing pages, embedded iframes.
- Feature-flagged code paths that are off in production but still shipped.

**Required before approval:** the exact method used to determine "unused" — grep patterns run, file types searched (`.vue`, `.erb`, `.html`, `.rb`, `.ts`, `.js`, `.json`, `.yml`), and whether the search covered string references (kebab-case, PascalCase, snake_case variants of the component name).

### 2. PrizeCategorySelector smells like a domain feature, not infrastructure
The name suggests it was built for a real product purpose ("prize categories"). Plans to delete domain-named components warrant a higher bar:
- Was the feature it supported deprecated? When? Is there a ticket or ADR?
- Does the backend still expose `prize_category` endpoints, models, or admin pages? If yes, the component may be the only consumer that's been removed prematurely from one surface but still expected elsewhere.
- Are there active feature flags gating prize-category UX?

### 3. No rollback plan
Component deletion in a Rails+Vue app is reversible via `git revert`, but only if you find out fast. The plan doesn't say:
- How will we know if something broke? (Frontend error monitoring — Sentry/Rollbar — set up to alert on `Failed to resolve component` warnings?)
- What's the canary/staged rollout plan? Is this going straight to production behind no flag?
- Who owns watching the dashboards for 24–48 hours post-deploy?

### 4. "Starting with PrizeCategorySelector" implies more deletions, but no list
The plan teases a broader sweep without naming the other components. Reviewing one deletion is meaningfully different from approving an open-ended cleanup pass. Either:
- (a) Scope this PR to PrizeCategorySelector only, and treat each subsequent deletion as a separate review, or
- (b) Provide the full list now with the "unused" evidence per component.

### 5. "About a day" estimate has no breakdown
For a single component deletion the work is minutes, not a day. If it's a day, where is the time going? Verification? Multiple components? Test updates? The estimate either understates scope (more components than stated) or overstates it (in which case, what's the actual work?). Either reading suggests the plan isn't fully thought through.

### 6. No mention of related artefacts
Removing a Vue component usually involves more than the `.vue` file:
- Associated tests (`PrizeCategorySelector.spec.ts` or similar)
- Storybook stories
- TypeScript types or interfaces it exported
- Translations / i18n keys used only by it
- CSS modules or scoped styles that may have been imported elsewhere
- Backend controller actions / serializers that exist only to feed it
- Routes that pointed at pages using it

Are these in scope? If the answer is "we'll see what comes up," that's exploratory work, not a planned day.

---

## What I'd want to see before approving

1. **Evidence of unused-ness:** the exact search commands run and their output (zero hits across all reference patterns and file types listed above).
2. **Domain context:** confirmation from the team that owned `prize_category` features that the feature is dead, with a link to the deprecation decision.
3. **Scope fence:** either "PrizeCategorySelector only, this PR" or a complete list with per-item evidence.
4. **Backend audit:** confirmation that backend code paths feeding this component are also dead (or a stated decision to leave them for separate cleanup).
5. **Rollback signal:** how a regression would be detected within 24 hours, and who's watching.
6. **Related-artefact list:** tests, stories, types, i18n, styles, routes — explicitly enumerated and either included or explicitly out-of-scope.

---

## What's fine

- Deletion-as-default is the right instinct. Code is a liability, and unused components rot — they get edited by mistake, mislead new contributors, and inflate bundle size.
- A day is a reasonable appetite for a careful single-component removal with verification, and a reasonable circuit breaker if scope creeps.
- The instinct to start small ("starting with PrizeCategorySelector") rather than a big-bang cleanup is correct.

---

## Recommendation

**Reshape the plan** to answer the six questions above and resubmit. If the evidence is solid, this becomes a 30-minute approval. If the evidence isn't solid, you've just avoided a production incident from a "trivial" cleanup. Either outcome is good.

If under time pressure, an acceptable minimum is: (a) paste the grep output proving zero references across `.vue`, `.erb`, `.html`, `.rb`, `.ts`, `.js`, `.json`, `.yml` for both `PrizeCategorySelector` and `prize-category-selector`; (b) confirm with backend owner that no API consumer remains; (c) ship behind a single revert-ready commit with someone watching error rates for 48 hours.
