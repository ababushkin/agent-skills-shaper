# Plan review: rubocop-1.60-to-1.65-bump

## Plan reference

Inline plan from prompt:

> "bump rubocop from 1.60 to 1.65 in Gemfile, run bundle update, run full test suite, commit. Should take 30 minutes. Approve?"

## Inputs

- **Appetite**: 30 minutes (stated cap)
- **Cynefin domain**: Clear — gem version bump with known cause-effect
- **Tier**: Quick — selected because none of the Full auto-select attributes hold (appetite ≤ 1 week, no one-way door, <3 external dependencies, no production data / schema / auth touch). Plan is fully reversible by single-commit revert of Gemfile + Gemfile.lock.

Trigger: owner is about to approve a plan ("Approve?") — When-to-use trigger 1.

## B1 — Problem framing

The plan opens with a solution ("bump rubocop from 1.60 to 1.65") with no problem statement. Why this bump, why now, why this version target? Possible problems behind it — catching up to CI, picking up a security advisory, unblocking another upgrade, picking up a new cop, matching a teammate's lockfile — produce different success criteria and different scopes. Without the problem named, "done" cannot be observed (Universal P2; Product P1).

**Verdict: SUSTAINED.**
Falsifying condition: owner produces a one-line problem statement of the form "we are bumping rubocop because [observable trigger], and we will know it worked when [observable signal]." Examples that would overturn: "CVE-2024-XXXX in rubocop-ast 1.30 affects us" or "rubocop 1.65 ships cop Foo/Bar that catches the class of bug we hit last sprint." Absent that, SUSTAINED stands.

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| `Gemfile.lock` will be rewritten by `bundle update` — not declared in scope | SUSTAINED | Plan explicitly names Gemfile.lock as part of the commit, or owner confirms `bundle update --conservative rubocop` (lock-only narrowing). |
| Transitive deps (rubocop-ast, parser, etc.) are pulled in by `bundle update rubocop` — not declared | SUSTAINED | Plan declares either `bundle update rubocop --conservative` (locks transitives) or accepts and names the transitive set that will move. |
| `.rubocop_todo.yml` regeneration / new-cop disposition — RuboCop 1.60 → 1.65 spans 5 minor versions, default-enabled new cops are likely; plan does not name this | SUSTAINED | Plan adds a step "run `bundle exec rubocop` post-bump, regenerate `.rubocop_todo.yml` if new offences appear, decide per-cop." |
| "bundle update" is ambiguous — `bundle update` (no arg) updates the entire lockfile; `bundle update rubocop` is the narrow path | PARTIAL | Plan states the exact bundler invocation. |
| "full test suite" is named but RuboCop output isn't a test — the actual risk surface (lint output) is not covered by `rspec`/`minitest` | SUSTAINED | Plan adds an explicit step: run `bundle exec rubocop` against the repo and report offence delta vs. 1.60. |
| "commit" — single commit, or Gemfile + Gemfile.lock + rubocop_todo across two commits? | PARTIAL | Plan names the commit shape. |

Note: B2 returns 4 SUSTAINED items on a 30-minute plan — exactly the scope expansion vector the skill exists to surface. The plan reads small; the work likely isn't.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| `bundle update rubocop` resolves cleanly within rubocop's gem dependency constraints | 0.5 (anecdotal — usually fine on minor bumps; transitive conflicts happen) | Run `bundle update rubocop --conservative` in a scratch worktree first; check for resolver errors. ~2 min. | SUSTAINED |
| The "full test suite" covers the risk introduced by a linter bump | 0.1 (opinion — categorically wrong; tests don't exercise lint output) | None needed — the assumption is false. Lint failures are caught by running RuboCop, not tests. Add `bundle exec rubocop` step. | SUSTAINED |
| 30 minutes is sufficient | 0.5 (plausible if zero new offences; collapses to multi-hour if 1.65 enables N default cops with offences in the codebase) | Run `bundle exec rubocop` once after bump, count new offences. If >10, reshape — this is no longer a 30-minute plan. | SUSTAINED |

All three risky assumptions score Confidence < 5. Per Step 6 GATE language, this would normally block APPROVE; under Quick-tier carve-out, B3 SUSTAINED downgrades to APPROVE with named recommendation when the change is fully reversible — see Recommendation.

## B8 — Pre-mortem

**Top failure mode (failed by EOD):** RuboCop 1.65 enables one or more new default-enabled cops; `bundle exec rubocop` (run in CI, or by a teammate post-merge) reports a wave of new offences across the codebase. The "30 minute" plan turns into a multi-hour decision per offence (autocorrect / disable in `.rubocop.yml` / move to `.rubocop_todo.yml` / fix). Worst case: it lands on main, breaks CI for everyone, gets reverted, and we now have a stale-bump branch and a confused team.

Generic "things go wrong" rejected — this is the specific, named failure mode for a linter minor-bump across 5 minor versions.

**Kill-switch condition:** After `bundle update`, before commit, run `bundle exec rubocop` once. If offence count > offence count on 1.60 baseline by more than ~10, stop. Reshape the plan to either pin a transitional version, regenerate `.rubocop_todo.yml`, or decide per-cop. Do not commit.

## Recommendation

**REVISE** — the plan has SUSTAINED B1 (no problem statement). Quick-tier reversibility carve-out covers B2 and B3 SUSTAINEDs but not B1. Without a problem statement, "done" cannot be observed and the bump may be solving nothing.

If B1 is closed (one-line problem + observable signal), the verdict converts to:

**APPROVE — recommend:** (a) state the exact bundler invocation (`bundle update rubocop --conservative` recommended); (b) add explicit `bundle exec rubocop` run between `bundle update` and `commit`, with kill-switch on >10 new offences; (c) name `Gemfile.lock` as part of the commit; (d) treat the 30-minute estimate as a cap — if the rubocop run produces a non-trivial offence delta, stop and reshape rather than absorb the work into the same change.

### Conditions

1. **Add a problem statement.** One line, of the form "we are bumping rubocop because [observable trigger]; we will know it worked when [observable signal]." (B1)
2. **Specify the bundler invocation** — `bundle update rubocop --conservative` if the intent is rubocop-only, or `bundle update rubocop` if pulling its dependency tree forward is intended. (B2)
3. **Add `bundle exec rubocop` as an explicit step** between `bundle update` and `commit`. The "full test suite" doesn't cover lint output. (B2, B3)
4. **Name the kill-switch:** if `bundle exec rubocop` reports >10 offences not present on 1.60, stop, reshape, do not commit in this 30-minute window. (B8)
5. **Name the commit contents** — Gemfile + Gemfile.lock at minimum; `.rubocop_todo.yml` if regenerated. (B2)

### Surfaced findings (carve-out — would have been APPROVE-with-recommendation absent B1)

- B2 SUSTAINED: scope expands silently into Gemfile.lock, transitives, `.rubocop_todo.yml`, and lint runs not covered by "full test suite."
- B3 SUSTAINED: three risky assumptions at Confidence ≤ 0.5 — bundler resolution clean, test suite covers risk, 30 minutes sufficient.

These do not by themselves block APPROVE on a fully-reversible KTLO change (Universal Rule A5 + Quick-tier carve-out), but they materially raise the probability that the 30-minute estimate is wrong by an order of magnitude, and the owner should see them before proceeding.
