# Plan Review: Bump rubocop 1.60 → 1.65

## Summary verdict

**Approve with minor caveats.** The plan is directionally correct and the scope is right-sized. A few gaps are worth addressing before or during execution.

---

## What's good

- **Scope is appropriately narrow.** Pinning the bump to a single gem and running tests before committing is the right instinct. Bundling this with unrelated changes would make rollback harder.
- **Test suite as gate.** Running the full test suite before committing is the correct control. rubocop version bumps can change cop behaviour; tests won't catch linting regressions, but they catch anything rubocop autocorrects that breaks runtime behaviour.
- **30-minute estimate is reasonable** for a clean bump with no major cop churn.

---

## Gaps worth addressing

### 1. Linting is a separate step from tests — and it's the actual risk here

rubocop is a linter, not a runtime library. The full test suite won't surface new rubocop violations. The plan as written doesn't include running `bundle exec rubocop` (or the equivalent) after the bump. Without that step, you'll commit code that may fail linting in CI.

**Recommendation:** Add an explicit `bundle exec rubocop` run (or `rubocop --parallel`) to the plan, and decide upfront what to do if new violations surface — autocorrect, manual fix, or temporarily disable the new cops in `.rubocop.yml`.

### 2. Check the rubocop changelog for the 1.60→1.65 delta

Five minor versions is a meaningful span. New cops are often introduced as `Enabled: false` by default, but some existing cops change behaviour or gain new options. It's worth a 5-minute scan of the [rubocop release notes](https://github.com/rubocop/rubocop/releases) for anything that affects your codebase's patterns before running the update — not after.

If there are extensions in play (`rubocop-rails`, `rubocop-rspec`, `rubocop-performance`), their versions may also drift under `bundle update rubocop`, depending on how they're pinned. Verify what `bundle update rubocop` actually updates before running it — consider `bundle update rubocop --conservative` or check the lockfile diff carefully.

### 3. `bundle update rubocop` vs. `bundle update --conservative rubocop`

Plain `bundle update rubocop` will also update any gem that rubocop unlocks through its dependency graph. If rubocop has transitive deps that are shared with other gems (e.g. `parser`, `regexp_parser`), you may pull in more than you intended. Check the Gemfile.lock diff before committing — if unexpected gems moved, evaluate whether that's intentional.

### 4. CI before merge

The plan ends at "commit." Presumably CI runs after push, but it's worth confirming that CI actually runs rubocop (many pipelines run tests separately from linting). If linting isn't in CI, that's a separate problem to note.

---

## Risk level

**Low.** rubocop is a dev-only tool; it doesn't affect runtime behaviour or production. The blast radius of getting this wrong is limited to broken CI or a noisy linting output. Easy to revert.

---

## Revised checklist (suggested)

1. Check rubocop 1.60→1.65 changelog for new/changed cops (~5 min)
2. `bundle update rubocop` and inspect the full Gemfile.lock diff
3. `bundle exec rubocop` — handle any new violations (autocorrect or disable intentionally)
4. Run full test suite
5. Commit Gemfile, Gemfile.lock, and any `.rubocop.yml` changes together
6. Confirm CI passes (linting + tests)

Estimate still holds at 30 minutes if the changelog scan is clean and no new violations surface. Budget an extra 15–30 minutes if cops changed behaviour that touches a lot of files.
