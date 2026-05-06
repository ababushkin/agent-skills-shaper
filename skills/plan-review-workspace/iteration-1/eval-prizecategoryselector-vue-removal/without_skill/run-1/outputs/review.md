# Plan review — Remove unused Vue components (starting with PrizeCategorySelector)

## Plan as submitted

> "Review this plan: remove unused Vue components, starting with PrizeCategorySelector under app/javascript/components/. Should take about a day. Approve?"

## Assessment

This is not yet a plan; it is an intent. It states a direction ("remove unused Vue components"), names a starting point (`PrizeCategorySelector`), and offers an appetite ("about a day") — but it omits almost everything required to commit engineering time with confidence.

Strengths:

- The underlying intent is sound. Dead code is a liability (universal Principle 5: code is a liability; the best change is often the one you don't make — and one we don't keep is even better). Removing genuinely unused components reduces cognitive load, build times, and the surface area for future drift.
- Scoping the work to a starting component (`PrizeCategorySelector`) is the right instinct: prefer the smallest first slice over a sweeping deletion PR (universal Principle 8: small batches beat big batches).
- A one-day appetite is appropriate for an exploratory deletion sweep — large enough to do real work, small enough to circuit-break if the assumptions don't hold.

Gaps that prevent approval as written:

1. **No problem statement.** "Unused components exist" is an observation, not a problem. Why now? What outcome moves? Reduced bundle size? Reduced confusion for new contributors? Removal of a blocker for an upcoming refactor? Without the "why," there's no way to judge whether this work earns its slot over other one-day options (universal Principle 2: design starts with the problem, not the stack; agentic Principle 3: the spec is the seatbelt).
2. **"Unused" is unverified.** Vue components can be referenced via dynamic imports, string-keyed component registries, async route definitions, slot fallbacks, server-rendered template strings, or test fixtures. A file with zero static `import` references is not the same as a component that is genuinely dead. The plan does not say how "unused" was determined. This is the risky assumption that needs to be tested before commitment (universal Principle 4; agentic Principle 2: hallucination/assumption is the default — sources are the brake).
3. **No definition of done.** Is the plan "delete the file and ship," or "delete + verify build + verify route coverage + verify no runtime references in production logs over N days"? Universal Principle 1 (shipped is not done; observed is done) bites here: a deletion looks instant but its blast radius shows up in production, often via a feature path no one tested locally.
4. **No rollback plan.** Deletions are git-reversible in principle, but if the deletion ships and a rare code path 404s a component three days later, the recovery is "revert + redeploy + re-test" — which needs to be a documented step, not improvised at the time.
5. **No batch boundary.** "Starting with PrizeCategorySelector" implies more components follow. Are they each a separate PR? One sweep? What's the gate between batch 1 and batch 2? Without this, the work either grows past the one-day appetite or ships as one large deletion PR (the very pattern Principle 8 warns against).
6. **No NFR check.** Bundle size, route coverage, and Storybook/visual-regression coverage are the natural fitness functions for this work. None are named. Universal Rule A4: NFRs are specified as measurable targets, not adjectives.
7. **Cross-team / consumer check missing.** If this is a multi-app monorepo, or the component is exported from a shared package, "unused in app/javascript" is not the same as "unused everywhere." Rule B7: cross-team dependencies surfaced before commitment.

## Concerns (ranked)

1. **False-positive deletion (high impact, medium likelihood).** Deleting a component that is dynamically referenced ships a latent runtime bug. Detection latency could be days. This is the dominant risk and the only one worth a hard gate.
2. **Scope creep past the one-day appetite (medium impact, high likelihood).** Without a defined batch boundary, "starting with PrizeCategorySelector" naturally expands as the author finds neighbouring dead code. One day becomes three. Universal Rule C1: appetite is a cap, not a target.
3. **Tests deleted alongside components without checking what they covered (medium impact, medium likelihood).** Component tests sometimes exercise shared utilities, mixins, or composables. Deleting the test file can silently reduce coverage of code that stays.
4. **Storybook / docs drift (low impact, high likelihood).** If the component is referenced in stories, MDX, or design-system docs, those break or rot silently. Universal Rule D6: documentation decay is a bug.

## What I'd want before approving

A revised plan that names:

- **Problem & outcome.** One sentence: why this work, what observable thing improves.
- **Verification method for "unused."** At minimum: (a) static analysis result (e.g. `knip`, `ts-prune`, ripgrep across `app/`, `spec/`, `test/`, `stories/`, server templates, i18n keys, dynamic-component registries); (b) manual spot-check of dynamic-import patterns and string-keyed component lookups; (c) if the app has a production error tracker, a search for the component name in recent logs.
- **Scope boundary for the one-day appetite.** Either "this PR removes only `PrizeCategorySelector` and its directly-coupled tests/stories" or "this PR removes the N components on the attached list, ranked by confidence." Not both, not open-ended.
- **Definition of done.** Build passes; bundle size reported (delta noted); affected route(s) smoke-tested; Storybook builds; no references remain in `package.json` exports, route files, or i18n keys; PR description lists the verification commands and their output.
- **Rollback plan.** "Single-commit revert; deploy pipeline takes ~N minutes; on-call paged if bundle hash mismatches." One sentence is enough — the point is that it has been thought about.
- **Follow-on batch plan.** If more deletions are coming, name the second component and the gate between PRs (e.g. "merge batch 1, wait 48h on production telemetry, then batch 2").

## Recommendation

**Do not approve as written. Send back for a 30–60 minute reshape** along the lines above. This is not a "kill the work" recommendation — the underlying instinct is good and the appetite is reasonable. It is a "the plan as stated is one sentence, and one sentence is not enough to put a day of engineering time against, particularly for a deletion that has non-zero blast radius."

Reshape, don't rebuild. Once the revised plan names the problem, the verification method for "unused," the scope boundary, and the definition of done, this is a clean approval and likely a sub-day piece of work in practice.
