# Plan Review: rubocop 1.60 → 1.65 bump

## Verdict: Approve with minor notes

This is a routine, low-risk dev-dependency bump. RuboCop is a development/lint tool — it does not ship to production, does not affect runtime behavior, and does not touch user data. The plan is appropriate to the size of the change.

## What's right

- **Scope is bounded.** A single gem, a minor-version range (1.60 → 1.65), with `bundle update` scoped to the one gem implied.
- **Verification is included.** Running the full test suite catches any incidental coupling (e.g., a Rake task that shells out to rubocop).
- **Reversibility is high.** Two-way door — revert the Gemfile/Gemfile.lock change if anything breaks.
- **Time estimate is realistic** for the happy path.

## Minor suggestions

1. **Be explicit about the bundle command.** `bundle update rubocop` (scoped) is safer than a bare `bundle update`, which would update every gem in the lockfile. The plan says "run bundle update" — clarify it's scoped.
2. **Run `rubocop` itself, not just the test suite.** Between 1.60 and 1.65, RuboCop adds new cops, changes defaults, and may flag existing code. Expect new offenses. Decide up front: auto-correct, add to `.rubocop_todo.yml`, or pin cop versions.
3. **Check the changelog.** Five minor versions of cumulative changes — skim the RuboCop CHANGELOG.md for any cops enabled by default that will create noise.
4. **Pin or range?** If the Gemfile uses `~> 1.60`, the bump may already be implicit on `bundle update`. Confirm whether the Gemfile constraint also needs editing.
5. **CI implications.** If CI runs `rubocop` as a gate, new offenses will turn the build red. Plan to land the lockfile bump and the `.rubocop_todo.yml` regeneration (or fixes) in the same commit, or behind a feature flag in CI.

## Time estimate

30 minutes is realistic *if* there are no new cop offenses. If there are, budget another 30–60 minutes to triage them (regenerate todo file or fix in-place).

## Approve?

Yes — proceed. The risk profile justifies the lightweight plan. Just scope the `bundle update` command and be ready for new cop offenses.
