# Plan Review: Remove unused Vue components (starting with PrizeCategorySelector)

**Verdict: Do not approve as written. Reshape first.**

## Summary

The plan is to delete Vue components believed to be "unused," beginning with `PrizeCategorySelector` under `app/javascript/components/`, with an estimated effort of about a day. As stated, this is a one-way door (deletion) being approved on the basis of an unverified claim ("unused"). That gap is the central problem.

---

## What is missing or under-specified

### 1. No definition of "unused"

The plan does not state how "unused" was determined. In a Rails + Vue codebase, components can be referenced via:

- Direct ES imports (`import X from '...'`)
- Dynamic imports / lazy loading (`() => import('...')`)
- String-based component registration (`Vue.component('prize-category-selector', ...)`)
- Webpacker/Shakapacker pack entrypoints
- Server-rendered HTML referencing components by tag name (`<prize-category-selector>`) — these will NOT be caught by a JS-only grep
- ERB / HAML / Slim templates that emit the component tag conditionally
- Stimulus controllers, Turbo frames, or `data-` attributes that mount Vue dynamically
- Tests, fixtures, Storybook stories
- Feature-flagged code paths that are dormant in production but still wired up
- External consumers (admin tools, internal apps, partner embeds) if any pack is shared

A grep for `PrizeCategorySelector` across `.js`, `.ts`, `.vue` files alone is insufficient. The search must also cover `.erb`, `.haml`, `.html`, `.rb` (for `render` or string references), and the kebab-case form (`prize-category-selector`).

### 2. No evidence the component is actually unused

Required before approval:

- Output of the search (commands run, files matched, files NOT matched)
- Confirmation that runtime telemetry / production logs show no references to the component or any route that mounts it
- Git log: when was it last modified? Who owned it? Is there a recent PR that staged it for removal vs. one that just landed it?
- Check whether it is exported from a public pack or an index file consumed elsewhere

### 3. No reversibility plan

Deletion is a one-way door at the working-copy level but two-way at the VCS level — provided we know how to find the deletion later. The plan should state:

- Single commit per component (so revert is trivial)
- Commit message includes the search evidence
- Deploy behind a window where the team is watching production for errors (not on a Friday afternoon)

### 4. No observation step

After deploy, what are we watching? Candidate signals:

- 500s / JS exceptions in error tracking (Sentry, Bugsnag, etc.)
- Asset pipeline errors (missing chunk, failed dynamic import)
- Specific page flows that historically used the component (if any are suspected)

"No errors after deploy" is the success criterion. Without naming the dashboard and the time window, "done" is undefined.

### 5. "Starting with PrizeCategorySelector" implies more deletions

The phrasing suggests this is the first of N. That changes the shape of the work:

- Is there a list of candidates? How was it produced?
- Is the day estimate for one component, or for the batch?
- One component per PR is the correct batch size — not "delete all unused components in one PR"

If the day estimate covers a batch, the estimate is almost certainly low once each candidate goes through proper verification.

### 6. Day estimate is uncalibrated

For one component, with proper verification (multi-extension grep, runtime check, git archaeology, deploy and observation window), one day is plausible. For a batch, it is not. The plan should either narrow scope explicitly to one component, or expand the appetite.

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Component is referenced from ERB/HAML and grep missed it | Medium | High — production page breaks | Multi-extension search; production smoke after deploy |
| Component is dynamically imported via string | Low-Medium | High | Search for kebab-case and string literals |
| Component is consumed by an internal admin tool not in this repo | Low | Medium-High | Check ownership; ask in #frontend before deleting |
| Deletion lands in a large batch PR that's hard to revert | Medium | Medium | One component per commit, ideally per PR |
| "Unused" was determined by a tool (e.g. ts-prune, knip) that doesn't understand Vue SFCs or Rails templates | Medium | High | Verify tool's coverage; cross-check manually |

---

## What I'd want before approving

1. The exact search command(s) and their output
2. Confirmation the search covered `.erb`, `.haml`, `.html`, `.rb`, `.vue`, `.js`, `.ts`, `.jsx`, `.tsx` for both PascalCase and kebab-case
3. Last-modified date and author of the component (and any associated test/story files)
4. A statement of which production signals will be watched post-deploy and for how long
5. Scope clarified: this PR removes exactly `PrizeCategorySelector` (and its test/story if present); subsequent components are separate PRs
6. Confirmation no feature flag references the component

---

## Recommendation

**Reshape, then approve.** The intent is fine — dead code is a liability, and removing it is virtuous work. But "unused" in a hybrid Rails + Vue codebase is a non-trivial claim, and approving deletion on an unverified claim is exactly the failure mode where a "quick cleanup" causes a production incident on a page nobody on the current team remembers exists.

The reshaped plan is small: do the verification, write it down in the commit message, deploy with a watch window, one component per PR. That is genuinely a day of work for the first one — and probably faster for subsequent ones once the search-and-verify recipe is established.
