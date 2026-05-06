# Plan review: Remove unused Vue components (starting with PrizeCategorySelector)

## Verdict

**Do not approve as written.** The plan is too thin to act on safely. There's a reasonable chance this is a one-hour task and a non-trivial chance it's a multi-day rabbit hole that breaks production. Tighten the spec before greenlighting.

---

## What the plan actually says

- Remove "unused" Vue components.
- Start with `PrizeCategorySelector` under `app/javascript/components/`.
- Estimated ~1 day.
- Asking for approval.

That's it. There's no evidence presented, no scope bound, no rollback plan, no definition of "unused," and no test or verification strategy. Approving this is approving a vibe, not a plan.

---

## Top concerns (in priority order)

### 1. "Unused" is undefined — and the most common source of incident reports

How was "unused" determined? In a Rails + Vue codebase living under `app/javascript/components/`, components can be referenced via:

- Static `import` statements (greppable, easy)
- Dynamic `import()` with computed paths (not greppable)
- Server-rendered Rails views injecting component names as strings (`data-component="PrizeCategorySelector"`, or similar mounting patterns common in Rails+Vue setups using packs or view helpers)
- ERB/HAML/Slim partials referencing the component by name
- Background jobs or mailers rendering server-side previews
- Feature-flagged code paths only loaded for certain accounts
- Admin tools, internal back-office screens, or rarely-trafficked flows
- Tests, Storybook, or design-system documentation

A simple `grep PrizeCategorySelector app/javascript` will miss most of these. A component called `PrizeCategorySelector` sounds like it lives on a customer-facing flow (prize/promotion selection?) — exactly the kind of thing that's quiet 90% of the time and load-bearing during a campaign.

**Required before approval:** the actual evidence that this component is unused. Greps across `app/views/`, `app/controllers/`, all template languages, dynamic mount patterns, and production telemetry (e.g. a frontend log/analytic confirming it hasn't rendered in N days). Without that evidence, "unused" is a guess.

### 2. The estimate is suspiciously round, and the scope is open-ended

"About a day" for "remove unused Vue components" is the classic pattern of a task whose true scope is unknown. Two failure modes:

- **Underrun reality:** if it really is unused and the audit is clean, this is a 30-minute PR, not a day. The day estimate suggests the author hasn't actually looked.
- **Overrun reality:** "starting with PrizeCategorySelector" implies a list. How many components? Have they all been audited? If the answer is "we'll find out as we go," the appetite is uncapped and this turns into a multi-day archaeology project.

**Required before approval:** either (a) confirm this is a single-component PR with the rest deferred to follow-ups, or (b) produce the full candidate list with per-component evidence before any deletions land.

### 3. No rollback plan, no blast radius statement

If this component is in fact used by something the audit missed, what happens? Best case: a build fails in CI and you revert. Realistic case: it ships, and a customer flow that runs once a week (or once a quarter, for a "prize" feature) silently 500s. Worst case: the deletion cascades — removing the component lets you delete its API endpoint, its serializer, its DB-backed config — and the revert is no longer a one-line revert.

**Required before approval:** confirmation that the deletion is a single atomic PR (component file + its imports + its tests), no upstream cleanups bundled in, and that revert is a `git revert` away. If anything beyond the component file is being touched, list it explicitly.

### 4. No verification that "deleted" works

What does "done" mean for this PR?

- CI green (necessary, not sufficient)
- Full test suite green including any system/integration tests that exercise the relevant flow
- A staging deploy, with a manual smoke of the flow that *would* have used this component, to confirm nothing 500s
- Ideally: production canary or feature-flag gate (delete the import first, observe for a release cycle, then delete the file)

The "delete behind a flag" pattern is overkill for some components and the right call for others. Which is this? The plan doesn't say.

### 5. The Rails + Vue context introduces specific failure modes

Components in `app/javascript/components/` in a Rails app are typically mounted in one of a few ways — Webpacker/Shakapacker packs, ViewComponent + Stimulus controllers that hand off to Vue, or direct `data-vue-component` mount helpers. Each has different "unused" detection requirements:

- If mounted by name via a string lookup, static analysis won't find it
- If lazy-loaded via a route map, the route map needs auditing
- If part of a pack that's bundled wholesale, removing the file may not even change the bundle if the pack still imports it transitively

**Required before approval:** the author should name the mounting mechanism for `PrizeCategorySelector` specifically. If they can't, they don't yet know enough to delete it.

### 6. "Prize" naming suggests possible compliance/audit surface

Not certain, but worth flagging: anything called "Prize" in a product often touches promotions, sweepstakes, raffles, or rewards — areas with legal/compliance review surface (terms & conditions, eligibility rules, regional restrictions). If this component is part of a promotional flow that lawyers signed off on, deleting it without sign-off is a different kind of risk than deleting a generic UI widget.

**Required before approval:** confirm whether this component is in a regulated/compliance-reviewed flow. If yes, loop in the relevant owner before deletion.

---

## Smaller concerns

- **No mention of tests.** Are there unit tests, snapshot tests, or e2e tests for `PrizeCategorySelector`? They need to come out too, and their absence in the plan is suspicious.
- **No mention of docs/Storybook.** Component libraries often have parallel doc artefacts that drift if you only delete the source.
- **No mention of translations / i18n keys.** Vue components often own their own i18n keys — orphaned keys are noise but easy to clean up in the same PR.
- **No mention of CSS / SCSS / styles.** Component-scoped styles usually go with the component, but global styles referenced only by it become orphan CSS that won't error but adds bundle weight.
- **"Approve?" framing.** This reads like the author wants a rubber stamp, not a review. Push back on the framing — the right ask is "here's the audit evidence, here's the PR, here's the rollback plan."

---

## What I'd require to approve

A revised plan that includes:

1. **Evidence of disuse**: greps across all template languages and JS/TS, plus a production telemetry check (or an explicit statement that no telemetry exists and the author accepts the residual risk).
2. **Scope cap**: this PR removes exactly one component (`PrizeCategorySelector`) and its directly-coupled artefacts (tests, styles, i18n keys, Storybook). Other "unused" components are out of scope and get their own audits.
3. **Mounting mechanism named**: how the component was wired up, so the deletion is complete.
4. **Rollback statement**: "single revert restores prior behaviour" — and confirmation that no upstream API/DB cleanup is bundled.
5. **Verification plan**: which tests must pass, what manual smoke is required, whether a staged rollout (delete imports → observe → delete file) is warranted.
6. **Compliance check**: confirm whether the component is in a regulated flow (promotional/legal/financial). One-line answer is fine.

If the author can produce the above in 30 minutes, the actual deletion is probably 30 minutes more and you're done in an hour, not a day. If they can't produce it, the day estimate is optimistic and the risk is real.

---

## Bottom line

Don't approve. Send back with: "Looks plausible — show me the evidence the component is actually unused (grep results across all template languages + a production-telemetry check), scope this PR to exactly one component, and tell me how to revert if we're wrong. Then it's a yes."
