# Plan review: rubocop-bump-1.60-to-1.65

**Fast-track gate fired** — KTLO/minor-version class (rubocop 1.60→1.65 is a minor SemVer bump of a dev-only lint gem), fully reversible (one-commit revert of Gemfile + Gemfile.lock restores prior state; no production data, schema, auth, or vendor topology touched), ≤1 day (stated 30 min). CI/CD is the runtime gate; this review is proportionate to that risk.

## Verdict: APPROVE

## Sanity checks
- Use `bundle update --conservative rubocop` (not bare `bundle update`) — bare `bundle update` re-resolves every gem in the Gemfile and turns a scoped rubocop bump into a whole-Gemfile churn that is far harder to review or revert.
- After bumping, run `bundle exec rubocop` against the codebase — not just the test suite. Rubocop minor releases routinely add new cops or change defaults; the test suite will not catch new lint violations, and a green test run can mask a wall of fresh offences that block the next person's commit.
- Confirm related rubocop ecosystem gems (`rubocop-rails`, `rubocop-rspec`, `rubocop-performance`, etc., if present) are compatible with 1.65 and move in lockstep if needed — version-skew between rubocop and its plugins is the most common failure mode on these bumps.

## B8 — Pre-mortem (one line)
Top failure mode: rubocop 1.65 introduces new default cops or stricter rules that flag existing code, blocking subsequent commits via the lint gate. Kill-switch: `git revert` the bump commit (single-commit revert restores prior Gemfile.lock and prior lint baseline).
