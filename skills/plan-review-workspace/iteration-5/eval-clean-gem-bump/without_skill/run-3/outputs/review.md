# Plan Review: Rubocop 1.60 → 1.65 Gem Bump

## Summary judgment

**Approve with caveats.** The core plan is sound, but it understates the work and omits several steps that matter for a dependency upgrade.

---

## What's right

- Scope is appropriately narrow: one gem, explicit version range, `bundle update`, test suite.
- Committing after tests pass is the right gate.

---

## What's missing or understated

### 1. Five minor versions is not trivial

Rubocop 1.60 → 1.65 is five releases. Each minor release typically adds new cops enabled by default or changes existing cop behavior. The test suite passing does not tell you whether new cops were added — it only tells you that existing app code still parses and tests still pass. New cops may silently not fire if the `.rubocop.yml` disables them by omission or if rubocop is only run in CI rather than as part of the test suite command.

**Action**: Review the Rubocop changelog for 1.61–1.65 before upgrading. Identify any new cops that are now `Enabled: true` by default and decide explicitly whether you want them enabled or disabled.

### 2. `bundle update rubocop` vs `bundle update`

The plan says "`bundle update`" without specifying a gem. Running `bundle update` with no arguments updates *all* gems, not just rubocop. This widens the blast radius significantly and makes the commit much harder to reason about later.

**Action**: Use `bundle update rubocop` (and any required co-dependencies) rather than bare `bundle update`.

### 3. Rubocop extensions and plugins

If the project uses rubocop extensions (`rubocop-rails`, `rubocop-rspec`, `rubocop-performance`, etc.), those may have compatibility constraints with 1.65. Blindly bumping rubocop without also checking extension compatibility can cause load errors or cop conflicts.

**Action**: List all `rubocop-*` gems in the Gemfile and verify they support 1.65 before running the update. You may need to bump them together.

### 4. `.rubocop_todo.yml` drift

Projects often have a `.rubocop_todo.yml` generated at a past version. After a rubocop bump, previously auto-corrected or suppressed violations may resurface under different cop names, or todo entries may become invalid and cause warnings. The test suite won't catch this.

**Action**: After `bundle update`, run `rubocop --display-cop-names` and check for any `Warning: unrecognized cop` messages. If the project has a todo file, consider regenerating it.

### 5. Time estimate

30 minutes is optimistic if the changelog review, extension compatibility check, and any new cops requiring `.rubocop.yml` decisions are included. 45–60 minutes is more realistic for a clean project; longer if new cops surface violations.

### 6. What "run full test suite" actually validates

The test suite validates application behavior. It does not validate that rubocop itself runs cleanly on the codebase at 1.65. These are separate:

- `bundle exec rspec` (or whatever) — application tests
- `bundle exec rubocop` — linter run at the new version

Both should be run and pass before committing. The plan implies only the first.

---

## Suggested revised plan

1. Read the Rubocop changelog for 1.61–1.65 (5 min).
2. Check all `rubocop-*` extension gems for 1.65 compatibility (5 min).
3. Run `bundle update rubocop` (and co-dependencies if needed), not bare `bundle update`.
4. Run `bundle exec rubocop` — fix or explicitly suppress any new violations.
5. Run the full test suite.
6. If `.rubocop_todo.yml` exists, check for stale entries.
7. Commit with a message that names the version range and summarises any cop changes accepted.

Revised time estimate: **45–75 minutes** depending on how many new cops fire.

---

## Verdict

Approve the *intent*. Reject the plan as written because step 3 (`bundle update` without gem name) risks a wider-than-intended update, and the plan omits the rubocop-itself linter run and changelog review which are the whole point of the exercise. Fix those two issues and it's a straightforward, low-risk upgrade.
