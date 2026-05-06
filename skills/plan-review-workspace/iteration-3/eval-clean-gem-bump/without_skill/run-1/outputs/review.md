# Plan review: bump rubocop 1.60 → 1.65

## Verdict: APPROVE

This is a small, fully reversible maintenance change. The plan is appropriate as stated. Proceed.

## Why this is a low-stakes change

- **Scope**: rubocop is a development/lint dependency. It does not ship to production runtime. Worst case is a noisy CI step or new offences flagged in lint.
- **Reversibility**: A single `git revert` (or reverting the Gemfile/Gemfile.lock entry) returns the project to the prior state. No data, schema, or user-visible surface is touched.
- **Blast radius**: Local + CI lint output. No customer impact.
- **Appetite**: 30 minutes is realistic for a clean bump where no new offences appear. If new offences appear, the appetite may need a small extension to triage — see recommendations.

## Pre-mortem (low-likelihood failure modes)

1. **New cop rules introduced between 1.60 and 1.65 produce lint errors on existing code.** Likelihood: medium. Impact: CI red on the PR. Kill-switch: revert the bump, or pin the new cops to disabled in `.rubocop.yml` and address in a follow-up.
2. **Transitive dependency drift from `bundle update`.** A naked `bundle update` updates all gems, not just rubocop. This can pull in unrelated gem upgrades. Likelihood: high if `bundle update` is run without a target. Impact: changes outside the stated scope land in the same commit, making revert and review noisier. Mitigation: use `bundle update rubocop --conservative` (or `bundle update --conservative rubocop`) so only rubocop and its direct dependencies move.
3. **Test suite failure unrelated to rubocop.** Unlikely if scope is constrained to rubocop, but possible if `bundle update` (without `--conservative`) pulls in a breaking gem version elsewhere. Mitigation: same as #2.
4. **Rubocop autocorrect applied broadly.** Not in the plan, but worth noting: do not run `rubocop -a` as part of this commit. Keep the bump and any autocorrect in separate commits so the diff stays reviewable.

## Recommendations (non-blocking)

- Use `bundle update rubocop --conservative` instead of a bare `bundle update` to keep scope tight to rubocop and its direct dependencies. This makes the commit honest to its message and the revert clean.
- Run `bundle exec rubocop` before committing, in addition to the test suite, so any new lint offences surface during the 30-minute window rather than after the commit lands.
- If new offences appear, prefer a follow-up commit (or a targeted `.rubocop.yml` adjustment) over expanding scope of this PR.
- Commit message should mention the version delta (`bump rubocop 1.60 → 1.65`) so the changelog is self-documenting.

## What I deliberately did not flag

- No spec doc, no ADR, no design review needed. This is a routine dependency bump on a dev tool.
- No staged rollout, no feature flag, no observability plan needed. Lint tooling has no runtime presence.
- No cross-team dependency review needed.

Inventing concerns at that level for a 30-minute reversible change would be process theatre.

## Cynefin domain

**Clear (Obvious).** Best practice exists, the cause-and-effect is well-understood, and the response is sense-categorise-respond. No need for expert analysis or experimentation.

## Tier

**Quick.** Sub-hour appetite, fully reversible, no production blast radius. Full plan-review machinery would exceed the cost of the change itself.
