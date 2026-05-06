# Plan review — rubocop 1.60 → 1.65 bump

## Assessment

This is a low-risk, narrow-scope dependency bump. Rubocop is a dev-only linter; it does not run in production and has no runtime blast radius on customers. The plan is well-scoped: single gem, minor version range (5 minors within the 1.x line, no major), with the standard verification path (bundle update + full test suite + commit). The 30-minute appetite is appropriate for the scope. This is a two-way door — trivially reversible by reverting the Gemfile/Gemfile.lock change.

## Concerns

A few things the plan does not say out loud, in roughly decreasing importance:

1. **Bundle update scope.** "Run bundle update" without a target gem will update the entire lockfile, not just rubocop. The intent here is almost certainly `bundle update rubocop` (which will also pull compatible updates to rubocop's own dependencies — `rubocop-ast`, `parser`, `regexp_parser`, etc.). Worth being explicit: a global `bundle update` is a meaningfully bigger change than a rubocop bump and would invalidate the 30-minute appetite.

2. **New cops.** Rubocop minor versions routinely ship new cops, some enabled by default, some pending. Going 1.60 → 1.65 spans roughly six months of releases. Expect new offences to appear when the linter runs. The plan doesn't say what happens then — fix, disable, or pin to `NewCops: disable` in `.rubocop.yml`. Pick a policy before starting, not after seeing the diff.

3. **Test suite vs. lint suite.** The plan says "run full test suite." That catches Ruby behaviour regressions (unlikely from a linter bump) but not the actual thing being changed: lint output. Add `bundle exec rubocop` to the verification, and review the diff in offences. If CI runs rubocop as a gate, also confirm CI is green on the branch before commit.

4. **Companion gems.** If the project uses `rubocop-rails`, `rubocop-rspec`, `rubocop-performance`, etc., those have their own version compatibility windows with the rubocop core. A core bump that breaks a companion gem's required-version constraint will fail `bundle update`. Worth a glance at the Gemfile before starting.

5. **Commit hygiene.** "Commit" in the plan is singular. Two small commits read more clearly in history: (a) Gemfile + Gemfile.lock bump, (b) any `.rubocop.yml` changes / autocorrects from new cops. Not load-bearing — flag, not block.

6. **Rollback.** Trivial here (`git revert`), so no formal plan needed, but worth confirming the branch is short-lived and the bump goes via the normal review path rather than direct-to-main.

## Recommendation

**Approve, with the following adjustments before starting:**

- Change "bundle update" to `bundle update rubocop` (and any rubocop-* companion gems, named explicitly).
- Add `bundle exec rubocop` to the verification step alongside the test suite.
- Decide the new-cops policy up front: enable, disable, or `NewCops: disable` in `.rubocop.yml`.
- Confirm no companion rubocop-* gem pins block the bump.

If new cops surface a non-trivial number of offences, the 30-minute appetite is the wrong shape — at that point, either pin `NewCops: disable` and ship, or stop and reshape into a separate piece of work to address the offences. Do not silently expand the appetite (universal Rule C5 / Shape Up appetite discipline).

The bump itself is a routine two-way-door change and should not need more ceremony than this.
