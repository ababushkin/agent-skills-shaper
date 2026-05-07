# Plan Review: Rubocop 1.60 → 1.65 Bump

## Summary verdict

**Approve with minor additions.** The plan is directionally correct but thin on risk management for a five-minor-version jump.

---

## What the plan gets right

- Correct sequence: Gemfile edit → `bundle update` → test suite → commit.
- Scoping `bundle update` to rubocop (implied) avoids dragging in unrelated dependency changes.
- Running the full test suite is the right safety check.

---

## What's missing or underspecified

### 1. Scope of `bundle update`

"Run bundle update" is ambiguous. `bundle update rubocop` updates rubocop and its direct deps. `bundle update` with no arguments updates everything — which would make this a multi-gem bump dressed as a rubocop bump. Specify `bundle update rubocop` explicitly.

### 2. Rubocop has its own cops that change between minor versions

1.60 → 1.65 is five minor releases. Rubocop routinely introduces new cops, changes cop defaults, and moves cops between departments across minor versions. The test suite won't catch new cop violations — only rubocop itself will. The plan needs an explicit step: **run rubocop** (or `bundle exec rubocop`) after the update and before committing. New offenses need a decision: fix them, add `# rubocop:disable` with a justification, or update `.rubocop.yml` to disable the cop project-wide. That decision should be deliberate, not left implicit.

### 3. Changelog review

Five minor versions is non-trivial. Spend two minutes scanning the rubocop changelog (or GitHub releases) for deprecations, removals, or behavior changes to cops already in use. This is a low-cost, high-signal step that the plan omits entirely.

### 4. Commit granularity

If rubocop flags new offenses that require fixes, mixing the version bump and the resulting code changes in a single commit conflates two things. Preferred: one commit for the Gemfile/lockfile change, a second for any autocorrected or manually fixed violations. Easier to bisect, easier to revert selectively.

### 5. Time estimate

30 minutes is plausible *if* rubocop introduces no new offenses. If it does, 30 minutes can expand quickly depending on the volume and nature of violations. The estimate should carry that caveat: "30 minutes assuming no new cop violations; budget an additional hour if new cops need remediation."

---

## Risk level

Low-to-medium. Rubocop bumps are routine, but five minor versions without a changelog review and without running rubocop itself as a step is where teams occasionally get surprised by a flood of new violations or a changed cop behavior that masks a real issue.

---

## Recommended revised plan

1. Scan rubocop changelog for 1.61–1.65 (5 min).
2. Edit Gemfile, run `bundle update rubocop`.
3. Run `bundle exec rubocop` — review and resolve any new offenses. Commit auto-corrects separately if needed.
4. Run full test suite.
5. Commit: Gemfile/lockfile in one commit; any rubocop-driven code fixes in a second commit if present.

**Approved to proceed** with these additions folded in.
