# Plan Review: RuboCop 1.60 → 1.65 Bump

**Plan under review:** Bump rubocop from 1.60 to 1.65 in Gemfile, run bundle update, run full test suite, commit. Estimated 30 minutes.

**Verdict:** Approve with modifications. The shape is right, but the plan as written has a few gaps that will likely cost you the 30-minute estimate.

---

## What's good

- Scope is small and well-bounded: a single dev-tooling gem, a five-version bump, no production code path involved.
- Sequencing is correct: edit Gemfile → bundle → verify → commit.
- 30 minutes is a plausible appetite for a dev-dependency bump in isolation.

## What's missing or wrong

### 1. Wrong verification target

Running the **full test suite** is not what verifies a RuboCop bump. RuboCop is a static analysis / linting tool — it doesn't run during your tests (unless you've wired it into a test runner, which is unusual). The test suite passing tells you almost nothing about whether the upgrade succeeded.

What actually verifies a RuboCop bump:

- `bundle exec rubocop` on the codebase — does it still run cleanly?
- Are there new cops enabled by default in 1.61–1.65 that now flag existing code?
- Are there cops that were renamed, removed, or had their defaults changed?
- Does your `.rubocop.yml` still parse without warnings?

The full test suite is fine to run as a smoke check, but it shouldn't be the primary verification step. Swap the order: lint first, tests second (or skip tests if CI will catch regressions).

### 2. `bundle update` is too broad

`bundle update` with no argument updates **every** gem in the Gemfile.lock to the latest version compatible with your Gemfile constraints. That's not a RuboCop bump — that's a "bump everything and hope" change, which:

- Conflates the RuboCop change with whatever else moved.
- Makes the diff noisy and the rollback harder.
- Means a test failure could be caused by any of N gems, not the one you intended to change.

Use `bundle update rubocop` (and likely `bundle update rubocop --conservative` if you want to minimize transitive movement). Inspect the Gemfile.lock diff before committing — you want to see rubocop and its direct deps move, not 40 unrelated gems.

### 3. No accounting for new cops / config drift

RuboCop minor releases routinely add new cops in `pending` or `enabled` state. Going 1.60 → 1.65 spans five minor versions — that's a non-trivial number of new cops. You will likely encounter one of:

- New offenses surfaced on existing code.
- A `pending` cops warning telling you to opt in or disable each one.
- A deprecated configuration key in `.rubocop.yml`.

The plan should include a step for reading the RuboCop changelog (or release notes) for 1.61, 1.62, 1.63, 1.64, 1.65 and deciding how to handle new cops. Auto-correcting is fine for safe cops; for unsafe ones, you need a deliberate call.

### 4. No mention of related gems

RuboCop has an ecosystem: `rubocop-rails`, `rubocop-rspec`, `rubocop-performance`, `rubocop-minitest`, etc. These extensions track RuboCop's API and frequently need to move together. A 1.60 → 1.65 jump on the core may break an extension pinned to an older API.

Check the Gemfile for `rubocop-*` gems. If any are present, the plan needs to consider them as part of the bump, not as a follow-up surprise.

### 5. No rollback plan

It's a small change, so the rollback is just "revert the commit" — but that should be stated. If the bump introduces a flood of new offenses you don't want to fix right now, you need to either (a) revert, or (b) add the new cops to `.rubocop.yml` as disabled / pending. Decide which before you start.

### 6. 30 minutes is optimistic if anything fails

If everything goes clean: 30 minutes is generous. If new cops trigger, or an extension gem needs to move, or `.rubocop.yml` needs updates — easily 1–2 hours. The estimate doesn't reserve any budget for the most likely failure mode (new offenses on existing code).

## Suggested revised plan

1. Check Gemfile for `rubocop-*` extension gems; note versions.
2. Skim RuboCop release notes for 1.61 through 1.65 — flag any new default-enabled cops or removed cops.
3. Update Gemfile pin: `gem 'rubocop', '~> 1.65'` (or whatever your constraint style is).
4. `bundle update rubocop --conservative` (and any extension gems together if they need to move).
5. Inspect Gemfile.lock diff — confirm only intended gems moved.
6. Run `bundle exec rubocop` on the codebase. Triage new offenses:
   - Auto-correctable and safe → run `--autocorrect` or `-a`.
   - Unsafe or stylistic → either fix manually, disable in `.rubocop.yml`, or mark as pending.
7. Run the test suite as a smoke check (because `bundle update` touched the lockfile).
8. Commit Gemfile, Gemfile.lock, and any `.rubocop.yml` or autocorrect changes — ideally as separate commits (`bump rubocop`, then `address new offenses` or `disable new cops`).
9. Push.

**Realistic budget:** 30 min if no new offenses surface. Plan for up to 2 hours if they do, and have a "revert and revisit" branch ready.

## Approve?

Approve **conditionally**:

- Narrow `bundle update` to `bundle update rubocop` (plus any rubocop-* extensions in lockstep).
- Make `bundle exec rubocop` the primary verification, not the test suite.
- Add a step for reviewing new cops between 1.60 and 1.65.
- Acknowledge the 30-minute estimate is best-case.

If those four are accepted, proceed.
