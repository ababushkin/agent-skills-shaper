# Plan Review: Rubocop 1.60 → 1.65 Bump

## Verdict: Approve with minor caveats

This is a low-risk, routine maintenance task. Rubocop is a development-time linter — it doesn't ship to production, doesn't affect runtime behavior, and bumping a minor version (1.60 → 1.65) within the same major is a two-way door. The plan is sound.

## What's good

- Scope is clear and small.
- Test suite run is included.
- Time estimate (30 min) is realistic for a clean bump.
- Reversible: if it goes badly, `git revert` and you're back to 1.60.

## Caveats / suggestions

1. **Expect new cops / changed defaults.** Minor Rubocop versions routinely add new cops or enable existing ones by default. The "test suite" won't catch lint failures — you need to run `bundle exec rubocop` separately. The plan doesn't mention this. Add it.

2. **Decide upfront how to handle new offenses.** Three reasonable options:
   - Fix them inline (may blow the 30-min budget).
   - Regenerate `.rubocop_todo.yml` and address in follow-ups.
   - Pin specific cops to previous behavior.
   Pick one before starting so you don't deliberate mid-task.

3. **Check the changelog.** Skim Rubocop's release notes for 1.61–1.65 for any breaking changes to config keys or removed cops that would error on load.

4. **Bundle update scope.** `bundle update rubocop` (targeted) is safer than `bundle update` (everything). The plan says "run bundle update" — clarify it's the targeted form, otherwise you're updating unrelated gems and the 30-min estimate breaks.

5. **Check transitive deps.** Rubocop pulls `rubocop-ast`, `parser`, etc. Targeted update may also bump these — that's fine but worth eyeballing the lockfile diff.

6. **Plugins.** If the project uses `rubocop-rails`, `rubocop-rspec`, `rubocop-performance`, etc., they may need compatible version bumps too. Check for resolver complaints.

## What's missing but probably fine

- No rollback plan stated — but `git revert` covers it.
- No CI verification mentioned — assume CI runs on the commit.

## Bottom line

Approve. Tighten the plan to: (a) `bundle update rubocop` (targeted), (b) run `bundle exec rubocop` in addition to tests, (c) decide the new-offense policy before starting, (d) skim changelog. If new offenses cascade, time-box and regenerate `.rubocop_todo.yml` rather than chasing them inline.
