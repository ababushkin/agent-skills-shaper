# Plan review: clean-gem-bump

**Fast-track gate fired** — KTLO/minor-version class (rubocop 1.60 → 1.65 minor SemVer bump), fully reversible (one-commit revert of Gemfile + Gemfile.lock), ≤1 day appetite (30 min stated). CI/CD is the runtime gate; this review is proportionate to that risk.

**Cynefin domain**: Clear (known cause-effect; dev-only dependency bump on a linter).

## Verdict: APPROVE

## Sanity checks
- Use `bundle update --conservative rubocop` rather than bare `bundle update` — bare form will move every gem in the lockfile that isn't pinned, expanding scope from one gem to the entire dep graph.
- After the bump, run `bundle exec rubocop` (not just the test suite) — rubocop changes surface as lint failures, not test failures. New cops between 1.60 and 1.65 may flag existing code.
- If your project pins ecosystem gems (`rubocop-rails`, `rubocop-rspec`, `rubocop-performance`), confirm whether they need to move in lockstep — version-skew between rubocop and its plugins is the usual breakage source.

## B8 — Pre-mortem (one line)
Top failure mode: new/changed cops between 1.60 and 1.65 fail CI on existing code. Kill-switch: revert the two-file commit; re-bump with `--conservative` plus targeted `.rubocop_todo.yml` regeneration.
