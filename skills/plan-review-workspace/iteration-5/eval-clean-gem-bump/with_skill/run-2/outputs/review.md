# Plan review: rubocop-1.60-to-1.65-bump

## Plan reference
> "bump rubocop from 1.60 to 1.65 in Gemfile, run bundle update, run full test suite, commit. Should take 30 minutes. Approve?"

## Step 1 — Trigger check
Trigger 2 fires: work described (30 minutes) is within one day. The plan also touches a dependency of the Ruby linting toolchain. Proceeding.

## Step 1a — Fast-track gate check

Evaluating all four preconditions:

1. **Class is KTLO/maintenance** — rubocop 1.60 → 1.65 is a minor SemVer bump (no major-version change). Class: dependency bump at minor SemVer. ✓
2. **Fully reversible** — one-commit revert restores prior Gemfile and Gemfile.lock. No production data, schema, auth, or vendor topology touched. ✓
3. **Appetite ≤1 day** — stated "30 minutes." ✓
4. **No major-version anything** — 1.60 → 1.65, no major bump, no breaking-API call-out in the plan. ✓

**All four preconditions hold. Fast-track gate fires.**

---

**Fast-track gate fired** — KTLO/minor-version class, fully reversible, ≤1 day. CI/CD is the runtime gate; this review is proportionate to that risk.

**Cynefin domain**: Clear
**Tier**: Quick (fast-track sub-form)

## Verdict: APPROVE

## Sanity checks
- Run `bundle update --conservative rubocop` rather than bare `bundle update` to avoid inadvertently pulling in unrelated gem upgrades alongside the rubocop bump.
- After the bump, run `bundle exec rubocop --format progress` to catch any newly-enabled cops that may now fail on existing code before running the full test suite — this surfaces rubocop-specific breakage faster than waiting for test output.
- Verify that any rubocop extension gems (e.g. `rubocop-rails`, `rubocop-rspec`, `rubocop-performance`) are compatible with 1.65 and update them in lockstep if needed; minor rubocop releases frequently require matching extension bumps.

## B8 — Pre-mortem (one line)
Top failure mode: newly-enabled cops in 1.61–1.65 produce autocorrectable or non-autocorrectable violations on existing code, blocking CI. Kill-switch: if `bundle exec rubocop` exits non-zero after the bump, revert Gemfile/Gemfile.lock and open a separate branch to triage and address new violations before merging the bump.
