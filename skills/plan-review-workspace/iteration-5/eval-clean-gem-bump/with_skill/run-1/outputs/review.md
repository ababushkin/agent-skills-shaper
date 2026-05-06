# Plan review: bump-rubocop-1.60-to-1.65

## Plan reference
> "bump rubocop from 1.60 to 1.65 in Gemfile, run bundle update, run full test suite, commit. Should take 30 minutes. Approve?"

---

**Step 1 — Trigger check**
Trigger fires: plan will take ~30 minutes (exceeds trivial; owner is about to approve). Proceeding to fast-track gate.

**Step 1a — Fast-track gate**
Checking all four preconditions:

1. **Class is KTLO/maintenance.** rubocop 1.60 → 1.65 is a minor SemVer bump (1.x → 1.y). PASS.
2. **Fully reversible.** One-commit revert restores Gemfile and Gemfile.lock; no production data, schema, auth, or vendor topology touched. PASS.
3. **Appetite ≤1 day.** Owner states "30 minutes." PASS.
4. **No major-version anything.** 1.60 → 1.65 is minor, no major-version bump, no breaking-API call-out in the plan. PASS.

All four hold. Fast-track gate fires.

---

# Plan review: bump-rubocop-1.60-to-1.65

**Fast-track gate fired** — KTLO/minor-version class, fully reversible, ≤1 day. CI/CD is the runtime gate; this review is proportionate to that risk.

**Cynefin domain**: Clear
**Tier**: Quick (fast-track sub-form)

## Verdict: APPROVE

## Sanity checks
- Scope the update: run `bundle update rubocop --conservative` rather than bare `bundle update`, to avoid inadvertently pulling in unrelated gem upgrades that could mask failures or widen blast radius.
- After the bump, run `bundle exec rubocop --parallel` in addition to the test suite — rubocop 1.61–1.65 may introduce new cops that trigger offenses not caught by RSpec/minitest. A green test suite with new rubocop violations would result in a red CI and a stalled commit.
- Check whether any rubocop extension gems (e.g. `rubocop-rails`, `rubocop-rspec`, `rubocop-performance`) also need a version bump for compatibility with 1.65; a pinned extension at an older minor can cause cop-version mismatches that produce obscure errors.

## B8 — Pre-mortem (one line)
Top failure mode: new cops introduced between 1.60 and 1.65 produce autocorrect conflicts or false-positive failures that block CI after commit. Kill-switch: run rubocop before committing; if offense count is non-zero, run `rubocop --auto-correct-all` and review diff before finalising.
