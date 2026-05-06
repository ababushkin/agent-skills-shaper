# Plan review: rubocop-1.60-to-1.65-bump

**Fast-track gate fired** — KTLO/minor-version class (rubocop 1.60 → 1.65, minor SemVer), fully reversible (one-commit revert restores Gemfile + Gemfile.lock), ≤1 day (30-minute appetite). No production data, schema, auth, or vendor topology touched. CI/CD is the runtime gate; this review is proportionate to that risk.

## Verdict: APPROVE

## Sanity checks
- Use `bundle update --conservative rubocop` (not bare `bundle update`) — bare `bundle update` re-resolves the entire Gemfile.lock and silently bumps unrelated gems, which violates the stated scope (only rubocop is meant to move).
- After the bump, run `bundle exec rubocop` against the codebase — not just the test suite. New cops or changed defaults between 1.60 and 1.65 can introduce offenses that the test suite will not surface; running rubocop is the actual signal that the bump landed cleanly.
- Confirm rubocop ecosystem gems (rubocop-rails, rubocop-rspec, rubocop-performance, etc., if present) are compatible with rubocop 1.65 before committing — version mismatches in this family are the most common breakage mode for rubocop bumps.

## B8 — Pre-mortem (one line)
Top failure mode: new/changed cops in 1.61–1.65 flag offenses in existing code, breaking CI on the next push. Kill-switch: run `bundle exec rubocop` locally before commit; if it fails, either pin the new cops to `Enabled: false` in `.rubocop.yml` with a follow-up issue, or revert the bump.
