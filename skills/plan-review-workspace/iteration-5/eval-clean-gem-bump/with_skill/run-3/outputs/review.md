# Plan review: rubocop-bump-1.60-to-1.65

**Fast-track gate fired** — KTLO/minor-version class, fully reversible, ≤1 day. CI/CD is the runtime gate; this review is proportionate to that risk.

**Cynefin domain**: Clear
**Tier**: Quick (fast-track sub-form)

## Verdict: APPROVE

## Sanity checks
- Run `bundle update --conservative rubocop` rather than plain `bundle update` to avoid inadvertently pulling in unrelated gem updates
- Run `bundle exec rubocop --no-autocorrect` after the bump to surface any new cop warnings or failures introduced by 1.65 before relying solely on the test suite
- Confirm that rubocop-related peer gems (e.g. `rubocop-rails`, `rubocop-rspec`, `rubocop-performance`) are compatible with 1.65 and update them in lockstep if needed

## B8 — Pre-mortem (one line)
Top failure mode: new cops enabled in 1.61–1.65 produce failures not caught by the test suite, blocking CI on an unrelated workflow. Kill-switch: run `rubocop` explicitly as a separate step before committing; revert the Gemfile.lock if it fails.
