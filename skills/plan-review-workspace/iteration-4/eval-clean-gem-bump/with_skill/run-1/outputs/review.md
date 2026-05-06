# Plan review: rubocop-bump-1.60-to-1.65

**Fast-track gate fired** — KTLO/minor-version class (rubocop 1.60 → 1.65 is a minor SemVer bump), fully reversible (one-commit revert of Gemfile + Gemfile.lock restores prior state), ≤1 day appetite (stated 30 min), no production data / schema / auth / vendor topology touched. CI/CD is the runtime gate; this review is proportionate to that risk.

## Verdict: APPROVE

## Sanity checks
- Use `bundle update --conservative rubocop` (not bare `bundle update`) — bare `bundle update` walks every transitive gem in the lockfile, which is out of scope for a rubocop bump and turns a 30-min change into an unbounded delta to review.
- Run `bundle exec rubocop` after the bump, not just the test suite — rubocop 1.60 → 1.65 typically introduces new cops or changes defaults; the test suite will not surface lint regressions, only `rubocop` will. Pin the cop changes via `.rubocop.yml` (`NewCops: disable` or explicit enable list) before committing if new cops fire.
- Confirm related ecosystem gems (rubocop-rails, rubocop-rspec, rubocop-performance, standard) are compatible with rubocop 1.65 — version pins on those gems are the most common cause of `bundle update --conservative rubocop` resolving back to an older rubocop or failing outright.

## B8 — Pre-mortem (one line)
Top failure mode: bare `bundle update` upgrades unrelated gems and a non-rubocop regression slips through under the cover of a "rubocop bump" commit. Kill-switch: scope the command to `--conservative rubocop` and inspect `git diff Gemfile.lock` before committing — if the diff touches gems other than rubocop and its direct deps, stop and revert.
