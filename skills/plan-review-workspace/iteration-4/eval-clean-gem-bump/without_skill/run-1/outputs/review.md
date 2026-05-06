# Plan review: rubocop bump 1.60 → 1.65

## Verdict

Approve with minor caveats. This is a low-risk, two-way-door change. The plan is essentially correct but the time estimate and a couple of operational details deserve a second look.

## What's good

- **Scope is tight.** A single dev-dependency version bump with no production runtime impact. Rubocop is a linter; it doesn't ship to production, doesn't touch user data, doesn't change app behaviour at runtime.
- **Reversible.** If something goes wrong, `git revert` and `bundle install` puts you back. Pure two-way door.
- **Right verification step.** Running the full test suite is the correct sanity check, even though tests are unlikely to be the thing that breaks.

## What's missing or under-specified

1. **The likely failure mode isn't tests — it's the lint run itself.** Going from 1.60 to 1.65 spans roughly a year of rubocop releases. Expect new cops enabled by default, deprecated cops, and changed defaults. The test suite will pass and then `bundle exec rubocop` will report a wall of new offences. The plan should explicitly include:
   - Run `bundle exec rubocop` after the bump.
   - Decide per-cop: fix, disable in `.rubocop.yml`, or use `--auto-gen-config` to baseline existing offences into `.rubocop_todo.yml`.
   - Confirm CI's rubocop step still passes (or the build will go red on the next push regardless of tests).

2. **`bundle update rubocop` vs `bundle update`.** The plan says "run bundle update" — unqualified, this updates *every* gem in the lockfile, which is a much larger change than advertised. Should be `bundle update rubocop` (and likely `rubocop-rails`, `rubocop-rspec`, `rubocop-performance` if present, since those track rubocop's API and often need a coordinated bump). Check which rubocop extension gems are in the Gemfile before running.

3. **Gemfile constraint style.** "Bump from 1.60 to 1.65" — is the Gemfile pinned (`'1.60'`), pessimistic (`'~> 1.60'`), or a range? `~> 1.60` already permits 1.60.x but not 1.65; `~> 1.60.0` is stricter. Worth naming what the constraint becomes (`'~> 1.65'`? `'~> 1.65.0'`?) so future bumps follow the same pattern.

4. **Changelog scan.** Five minor versions of rubocop is enough to warrant a five-minute skim of the release notes — specifically for: cops promoted to default-enabled, cops whose defaults changed, and any breaking changes to the config schema. Cheap insurance.

5. **Commit granularity.** If you end up with (a) the Gemfile/lockfile bump and (b) a regenerated `.rubocop_todo.yml` or config tweaks, those should be separate commits. Mixing them makes the bump harder to revert cleanly.

## Time estimate

30 minutes is optimistic if there are new offences to triage. Realistic ranges:

- **Best case (10–15 min):** No new offences, suite green, push.
- **Likely case (45–90 min):** A handful of new offences; decide fix-vs-disable, regenerate todo file, re-run.
- **Worst case (half day):** A new default cop fires across hundreds of files (this happens — e.g. style cops on string literals, hash syntax). You'll need to either auto-correct, baseline, or disable.

Not a reason to block, but the team should know "30 minutes" is the no-surprises floor, not the expected case.

## One-way doors

None.

## Risks worth naming

- **CI surprise after merge.** If rubocop runs in CI and the local lint check is skipped, the build goes red post-merge. Run the linter locally before pushing.
- **Coordinated extension gems.** If `rubocop-rails` etc. aren't bumped together, you may hit "incompatible rubocop version" errors at load time.
- **Editor integrations.** Team members with rubocop pinned in their editor config (Solargraph, ruby-lsp, vscode-ruby) may see different warnings until they `bundle install`. Worth a heads-up in the commit message or team channel.

## Recommended revised plan

1. Check Gemfile for rubocop and any `rubocop-*` extension gems; note the constraint style.
2. Skim rubocop CHANGELOG between 1.60 and 1.65 for default changes.
3. Update Gemfile constraint(s).
4. `bundle update rubocop rubocop-rails rubocop-rspec ...` (only the rubocop family, not the whole lockfile).
5. Run full test suite — expect green.
6. Run `bundle exec rubocop` — triage offences (fix / disable / baseline into `.rubocop_todo.yml`).
7. Commit Gemfile + lockfile changes; commit any config/todo changes separately.
8. Push and verify CI passes.

Budget: 60 minutes nominal, with the understanding that step 6 can blow up.

## Bottom line

Approve. The change is safe and reversible. Tighten the `bundle update` invocation, add an explicit "run rubocop and triage offences" step, and treat 30 minutes as the floor not the ceiling.
