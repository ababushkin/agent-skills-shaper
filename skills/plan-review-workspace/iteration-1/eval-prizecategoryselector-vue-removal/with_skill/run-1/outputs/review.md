# Plan review: prizecategoryselector-vue-removal

## Plan reference

Pasted plan text (verbatim):

> "Review this plan: remove unused Vue components, starting with PrizeCategorySelector under app/javascript/components/. Should take about a day. Approve?"

No external plan document was supplied. This review treats the pasted text as the entire plan.

## Inputs

- **Appetite**: ~1 day (stated as "about a day"). NOTE: "about a day" is a range, not a fixed cap — this itself is a B7 finding.
- **Cynefin domain**: **Complicated**. Removing dead code is a knowable-with-expertise problem (cause-effect: if no caller exists, removal is safe; if a caller exists, removal breaks). Emphasis falls on dependency/usage detection, not emergent feedback loops.
- **Tier**: **Quick** — selected because appetite is ≤1 week, no explicit one-way doors flagged in the plan, no production data/auth/schema touch declared, and no cross-team dependencies named. Quick runs B0, B1, B2, B3, and a short B8.

Note on trigger: trigger #2 fires (work exceeds one day on the high side of "about a day" if the search proves wide), and trigger #3 plausibly fires (the plan touches code the owner has not declared they have personally traced this week — the framing "remove unused" is itself an unverified claim). Review proceeds.

## B1 — Problem framing

**Verdict: SUSTAINED.**

The plan opens with a solution ("remove unused Vue components, starting with PrizeCategorySelector"), not with a problem or a measurable outcome. There is no statement of:

- What outcome removal is meant to produce (bundle-size reduction? cognitive-load reduction in the components directory? unblocking a Vue-to-X migration? reducing maintenance surface area?)
- A target metric (e.g. "reduce app/javascript/components/ file count by N", "reduce JS bundle size by X KB", "remove the last Vue components so we can drop the Vue dependency")
- Why now versus later

Universal P2: design starts with the problem, not the stack. "Remove unused X" is a verb-led solution statement.

**Falsifying condition:** The plan author produces a one-line problem statement of the form "For [audience], [problem] is causing [negative outcome]; if we remove these components, we expect [measurable outcome] to improve by [target]" — for example, "Vue components in app/javascript/components/ are blocking removal of the Vue runtime from the bundle (~XX KB); removing the last N unused components lets us drop Vue entirely." If such a statement exists and was simply omitted from the review request, the verdict is OVERTURNED.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| Scope of "unused" — is it (a) zero imports from JS/TS, (b) zero references including ERB/HAML/Slim templates and Stimulus controllers, (c) zero references including dynamic component resolution / string-keyed registries, or (d) all of the above? Removing under definition (a) when (c) is needed is a runtime break. | SUSTAINED | The plan author specifies the exact "unused" definition AND names the search command(s) that will be used (e.g. `rg "PrizeCategorySelector" --type-add 'tmpl:*.{erb,slim,haml}' -t js -t ts -t vue -t tmpl -t rb`). |
| "Starting with PrizeCategorySelector" implies a list of further components, but the list is not enumerated or sized. The scope could be 1 component or 30. "About a day" cannot be true for both. | SUSTAINED | The plan author lists every component slated for removal in this batch with a per-component effort estimate, OR explicitly bounds the batch to PrizeCategorySelector only and defers the rest. |
| Test impact undeclared. Removing a component typically removes (or invalidates) co-located unit tests, fixture references, Storybook stories, and possibly Cypress/Playwright e2e selectors. Plan does not declare which test artefacts are in-scope. | SUSTAINED | Plan names the test files / story files / e2e specs that will be removed alongside the component, OR confirms via search that none exist. (Concrete check the plan author should run: `grep -r PrizeCategorySelector spec/ test/ cypress/ e2e/ stories/` returns no hits.) |
| Build manifest / bundling config (webpack, vite, esbuild, importmap, sprockets, jsbundling-rails) may have explicit references. Plan does not declare check. | SUSTAINED | Plan confirms search across `config/`, `webpack.config.*`, `vite.config.*`, `package.json`, `app/assets/config/manifest.js`, and any importmap pin file returns no hits. |
| Server-rendered references (ERB/HAML partials referencing the component by name, or Rails view helpers like `vue_component "PrizeCategorySelector"`) are the most common silent breakage path for Vue-in-Rails apps. Plan does not declare check. | SUSTAINED | The plan author runs `grep -r PrizeCategorySelector app/views/ app/components/ app/helpers/` and includes the result. Any hit changes the verdict from "unused" to "used by server template." |
| "App/javascript/components/" — is this the only directory holding Vue components, or are there parallel paths (`app/javascript/packs/`, `app/javascript/vue/`, `app/frontend/`)? Plan asserts directory but does not justify it as exhaustive. | PARTIAL | The plan author confirms the components directory is the canonical and sole location for Vue SFCs in this app, OR scopes the cleanup to that directory only and acknowledges others remain. |

Out-of-scope touches the plan implicitly makes (without declaring):

- Test files, fixtures, stories
- Server-side templates that may render the component
- Build/bundler config that may list the component as an entry point
- i18n keys scoped to the component (if any)

In-scope items vague enough to expand silently:

- "Unused Vue components" — without a definition of unused, the agent will pick the most permissive one
- "Starting with PrizeCategorySelector" — the implied tail is unbounded
- "About a day" — a range, not a cap

Six SUSTAINED/PARTIAL verdicts on a 1-day plan is high. The skill's own guidance says "zero hits usually means lenient review"; six hits suggests the plan has been written at a level of abstraction below what one-day execution requires.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| PrizeCategorySelector is genuinely unused (no JS imports, no template references, no dynamic resolution, no test references). | 0.1 — opinion / assertion. The plan asserts "unused" without naming the evidence. | 5-min test: run a multi-extension grep across `app/`, `config/`, `spec/`, `test/`, `cypress/`, `stories/`, `lib/`, package.json, importmap pins, and any view-helper invocations. Concrete check: `rg -uu "PrizeCategorySelector"` from repo root returns hits ONLY in the component file itself and its co-located test/story. | SUSTAINED |
| The set of "unused Vue components" is small enough to fit in ~1 day. | 0.1 — opinion. No enumeration provided. | 5-min test: list the candidate components and grep each. If the list is >5 components, appetite is wrong; if it is 1, "starting with" is misleading. | SUSTAINED |
| Removal is reversible cheaply if a regression is discovered post-merge (i.e. this is a two-way door). | 0.5 — anecdote-level. True in most cases (`git revert`), but Vue components sometimes carry state-shape contracts consumed by other components or by serialized user state (e.g. saved filter URLs), which are not reversed by a code revert. | 5-min test: confirm the component's props/emits are not part of any persisted contract — no URL params, no localStorage keys, no server-stored user preference shapes reference its prop names. | PARTIAL |

Untested assumptions with Confidence < 5 block APPROVE. Two of the three are at 0.1.

## B4 — Dependencies (Full only)

Skipped — Quick tier. (Note: if a Full review were run, the dependencies bucket would likely return empty for cross-team work but would surface dependency on whoever owns the Vue removal initiative, if one exists, and on any QA gate for Vue changes.)

## B5 — Reversibility + ADR pairing (Full only)

Skipped — Quick tier. Brief note: deleting a component is generally a two-way door (revert restores it), but removing the last instance of a framework's usage tips into one-way-door territory because the next step is usually "remove Vue from the bundle," and that has a non-trivial reversal cost. The plan should declare whether this is intended as a step toward Vue removal or a standalone cleanup.

## B6 — Operability + success metrics (Full only)

Skipped — Quick tier. Brief note: an operability-aware version of this plan would name (a) the bundle-size delta to be observed post-merge, (b) a smoke-test path covering any page that historically rendered the removed component, and (c) a rollback condition (which page-error rate or which user report would trigger revert).

## B7 — Sequencing + capacity (Full only)

Skipped — Quick tier. Brief note: "about a day" is a range, not a fixed cap. A Full review would push this to a single number with a defined circuit-breaker (Universal Principle 8 / Shape Up appetite).

## B8 — Pre-mortem

**Top 1 reason this plan failed by end-of-week:**

The component was referenced by a server-rendered template (an ERB partial calling a `vue_component` helper, or a string-keyed dynamic-component registry) that the JS-only grep missed. Production rendered the page, the component failed to mount, the surrounding view broke, and the regression was caught by a customer rather than by CI because no test exercised the page at the integration level.

**Kill-switch condition (catches it early):**

Before merging, run a pre-merge check that looks for the component name as a string literal anywhere in the repo (`rg -uu "PrizeCategorySelector"`) AND deploys to staging with the path/page that historically used the component exercised by smoke test. If either returns a hit or a render error, abort the removal.

## Recommendation

**REVISE** — the plan is solution-led, scope-vague, and rests on an unevidenced "unused" claim. Removal is plausible and probably cheap, but the plan as written would let an executor delete a component still referenced by a server template or a dynamic registry. Five-minute checks turn most of these SUSTAINED verdicts into OVERTURNED ones — but they have not been done yet.

### Conditions

The plan must satisfy all of the following before APPROVE:

1. **Problem statement (B1).** One line in the plan stating the outcome the removal is meant to produce and the metric that will indicate success (e.g. bundle-size delta, file-count delta, "removes last Vue dep so we can drop the runtime").
2. **Definition of "unused" (B2).** Name the exact search command and file extensions covered. At minimum: JS/TS/Vue, ERB/HAML/Slim, Ruby (for view helpers), and bundler config files.
3. **Server-template check executed (B2/B3).** `grep -r PrizeCategorySelector app/views/ app/components/ app/helpers/` returns zero hits, included in the plan as evidence.
4. **Dynamic-resolution check executed (B2/B3).** Confirm the codebase has no string-keyed component registry (e.g. `Vue.component(name, …)` with name resolved at runtime) that could reference PrizeCategorySelector by string. If such a registry exists, audit it explicitly.
5. **Bundler/manifest check executed (B2).** Confirm webpack/vite/importmap/manifest configs do not reference the component as an entry.
6. **Test artefact scope declared (B2).** Either name the co-located tests/stories that will be removed, or confirm none exist.
7. **Batch size declared (B2/B7).** Either restrict scope to PrizeCategorySelector only and defer the "starting with" tail to a separate plan, OR enumerate the full batch with per-component effort estimates so "about a day" can be checked against reality.
8. **Appetite fixed (B7).** Replace "about a day" with a single-number cap (e.g. "1 day; if not done, ship what's removed and re-plan"). The default at the cap is to ship-or-stop, not extend.
9. **Pre-merge smoke path identified (B8).** Name the page or flow that historically used the component, and run it on staging post-removal.

Once 1–7 are satisfied, the residual work fits inside ~1 day at high confidence, and the plan can be APPROVED on Quick tier without further escalation. If 7 reveals a batch >3 components, re-tier to Full and re-run.
