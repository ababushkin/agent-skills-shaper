# Plan review: clean-gem-bump

## Plan reference

Pasted plan (only available input):

> "Review this plan: bump rubocop from 1.60 to 1.65 in Gemfile, run bundle update, run full test suite, commit. Should take 30 minutes. Approve?"

## Inputs

- **Appetite**: 30 minutes (fixed cap as stated by owner)
- **Cynefin domain**: Clear — bump a dev-time linter version, run an existing test suite, observe pass/fail. Known cause-effect.
- **Tier**: Quick — selected because appetite is well under 1 week, no one-way-door decision (rubocop is a dev-time linter; reversal is reverting the Gemfile line and re-running `bundle install`), no cross-team dependencies, no production-data touch. None of the Full auto-select rules fire.

Trigger fired: a plan has been produced and the owner is about to approve (Trigger 1).

## B1 — Problem framing

**Verdict: PARTIAL.** The plan is solution-first ("bump rubocop from 1.60 to 1.65") with no problem statement. The implicit problem is plausible (stay current on linter, pick up new cops or bug fixes, avoid drift) but is not named. For a 30-minute KTLO-style change against a dev-time tool, Universal Rule A5 (KTLO carve-out) applies: minor maintenance does not require outcome framing. So this is not SUSTAINED — but it is PARTIAL because the plan doesn't even confirm this is KTLO rather than a deliberate upgrade aimed at a specific cop or fix.

**Falsifying condition**: owner names the maintenance frame ("routine version upkeep, no specific cop targeted") in one line, or names the specific cop/fix being chased. Either resolves PARTIAL.

## B2 — Scope clarity

The plan declares: edit Gemfile, run `bundle update`, run full test suite, commit. Scanning honestly for undeclared touches and silent expansion:

| Item | Verdict | Falsifying condition |
|---|---|---|
| `bundle update` (no gem name argument) updates every gem with available updates, not only rubocop | SUSTAINED | Plan is amended to `bundle update rubocop` (or `bundle update --conservative rubocop`), constraining the change to the named gem and its required transitive deps |
| `Gemfile.lock` change is unmentioned but is the actual diff that ships | OVERTURNED | The lockfile change is the natural and expected output of the workflow; no reasonable reader would think otherwise. Not a real defect. |
| New rubocop offences in 1.65 may surface and require either auto-correct, config edits, or `.rubocop_todo.yml` regeneration — none scoped | SUSTAINED | Plan adds an explicit branch: "if new offences appear, either fix, regenerate `.rubocop_todo.yml`, or pin to a version that doesn't introduce them — within the 30-minute appetite, otherwise stop and reshape" |

The first item is the real defect. `bundle update` without a gem argument is a well-known Bundler footgun: it updates every gem subject to Gemfile constraints, not just the one you care about. The diff and the blast radius are both larger than the plan implies.

The third item is the second real defect: rubocop minor-version bumps routinely add cops. The plan has no branch for the most common outcome.

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| "30 minutes is enough" — assumes no new offences, no other gem updates pulled in, suite is green and fast | 0.5 (anecdote — feels right for a clean bump but not measured) | Run `bundle outdated` and `bundle update --conservative rubocop --dry-run` (or `bundle lock --update=rubocop`) before committing, to see the actual lockfile delta in <2 minutes | SUSTAINED |
| "Full test suite covers what could break from a rubocop bump" | 0.1 (opinion — rubocop is a static analyser; the test suite typically does NOT exercise rubocop output. CI lint stage does.) | Confirm whether CI runs `rubocop` as a step, or whether running the test suite alone leaves a lint regression undetected until CI | SUSTAINED |
| "1.60 → 1.65 is a clean minor bump, no breaking changes" | 0.5 (anecdote — rubocop's own changelog and the project's `.rubocop.yml` are the authoritative sources, neither is cited) | Read rubocop CHANGELOG between 1.60 and 1.65 (5 min) and check `.rubocop.yml` for any cop pins that may now mismatch | SUSTAINED |

All three sit at Confidence < 5 with cheap tests available. Per the skill's B3 gate, untested assumptions with Confidence < 5 block APPROVE.

## B8 — Pre-mortem (Quick: top 1 reason + kill-switch)

**Top reason the plan fails by end-of-week**: `bundle update` (no gem argument) silently bumps several other gems alongside rubocop, the team merges the PR thinking it's "just a rubocop bump," and a behavioural regression from one of those other gems surfaces in production days later. The blame goes to a commit titled "bump rubocop 1.60 → 1.65," which nobody re-reads carefully.

**Kill-switch condition**: before commit, run `git diff Gemfile.lock` and confirm rubocop (and only rubocop + its required transitive deps) changed. If any other gem changed major or minor, stop and either constrain the update (`bundle update --conservative rubocop`) or split the commits.

## Recommendation

**REVISE** — The plan is small but contains two real defects: an unconstrained `bundle update` that widens the diff beyond the stated scope (B2), and an unverified assumption that the test suite catches what a rubocop bump can break (B3). Both are 5-minute fixes; neither is a reason to kill the plan.

### Conditions for APPROVE

1. Replace `bundle update` with `bundle update --conservative rubocop` (or `bundle update rubocop`), and verify the resulting `Gemfile.lock` diff is scoped to rubocop and its required dependencies.
2. Confirm that whatever runs rubocop (CI lint stage, pre-commit hook, or local `bundle exec rubocop`) is executed as part of "verify before commit" — not just the test suite. A green test suite does not validate a linter bump.
3. Add an explicit branch for new rubocop offences: fix, regenerate `.rubocop_todo.yml`, or stop and reshape — chosen within the 30-minute appetite, not allowed to expand it silently.
4. (PARTIAL on B1) State in one line whether this is routine upkeep (KTLO) or a deliberate upgrade chasing a specific cop/fix. Either is fine; the ambiguity is not.

Once these four conditions are met, this is a clean APPROVE. The plan is genuinely low-risk — most buckets (B4, B5, B6, B7) do not apply at this tier and would OVERTURN even at Full. The defects that exist are scope and assumption defects, not architectural ones.
