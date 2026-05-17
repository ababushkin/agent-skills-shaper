# Tasks: render-html

Design doc: /Users/anton/.claude/plans/expressive-knitting-quiche.md (approved plan; serves as the design doc for this skill)
Implementation tool: `/skill-creator:skill-creator` (used for drafting, evals, iteration, and description tuning)
Last updated: 2026-05-17

## How skill-creator changes the shape

skill-creator's loop is: draft → test prompts → run skill against prompts → quantitative + qualitative eval → rewrite → repeat → finally run the description-improver. That replaces the sequential "author one pattern at a time" structure with an iterate-on-evals loop. Each HTML pattern becomes a test case in the eval suite, not a discrete authoring task. Pattern coverage is then measured rather than asserted.

## Task list

### Task 1 — Walking skeleton via skill-creator draft
**Description:** Invoke `/skill-creator:skill-creator` to draft `skills/render-html/SKILL.md` and `.claude/commands/render-html.md` covering anatomy compliance (per `docs/skill-anatomy.md`) and a minimal inline HTML shell that converts any md file to a self-contained `<source>.html` with TOC of H2/H3 + prose body.
**Done when:** Running `/render-html <some-existing-md-in-this-repo>` writes a sibling `.html` that (a) opens via `file://` in Chrome with no console errors and zero network requests, (b) contains a TOC listing every H2/H3 from the source, (c) renders every md heading and paragraph, (d) if the target `.html` already exists, the skill prompts for overwrite confirmation before writing. SKILL.md passes a manual anatomy check (all required sections present in order, `[GATE]`s preserved, frontmatter validates).
**Dependencies:** none

### Task 2 — Extract HTML shell into reference file
**Description:** Move the inline `<!doctype html>` shell out of SKILL.md into `references/html-skeleton.md` (system font stack, ~70ch prose cap, sticky TOC sidebar, scrollspy JS ≤ 50 lines, prefers-color-scheme dark mode, print stylesheet). Document the hard rule: no external `<link>`/`<script src>`/remote images. SKILL.md cites the reference.
**Done when:** Re-rendering the Task 1 fixture produces an HTML byte-identical to before (modulo provenance/timestamp lines); SKILL.md line count drops accordingly and stays inside the 180–240 target.
**Dependencies:** Task 1

### Task 3 — Build the fixture + expectations set for the iterate loop
**Description:** Create one synthetic md fixture per HTML pattern from the approved plan (alternatives-considered, task-list-with-dependencies, design-doc-blocks, NFRs-table, open-questions, diff/before-after, roadmap-now-next-later, ICE-scores) plus two control fixtures: an unstructured bulleted brainstorm (must degrade to clean prose) and an omnibus fixture combining every pattern. For each fixture, write a plaintext expectations file describing what the rendered HTML must contain (specific structures, no console errors, size < 500KB). v0.1 evaluation is by eyeball — run the skill against each fixture, open the output in a browser, check against the expectations file. No automated scoring harness yet (see Resolved decisions).
**Done when:** Fixtures live under `skills/render-html/evals/fixtures/`; each has a sibling expectations file; the Task 1 walking-skeleton draft has been eyeballed against every fixture and the baseline (most pattern fixtures fail, prose + control fixtures pass) recorded in a notes file.
**Dependencies:** Task 1

### Task 4 — Scaffold the pattern catalogue
**Description:** Create `references/html-patterns.md` with an introduction and one empty section per pattern (matching the fixtures from Task 3). Each section template: *when to apply*, *source md shape*, *HTML/CSS treatment*, *accessibility notes*. SKILL.md cites this reference in its workflow step 3.
**Done when:** `references/html-patterns.md` exists with 8 named sections; SKILL.md references it.
**Dependencies:** Task 2, Task 3

### Task 5 — Iterate via skill-creator until all pattern fixtures pass
**Description:** Run the skill-creator iterate loop with eyeball evaluation. Each iteration: render every fixture → inspect failures against the expectations file → extend SKILL.md and/or `html-patterns.md` and/or `html-skeleton.md` to cover the failing pattern → re-render. Repeat until every pattern fixture and both control fixtures pass.
**Done when:** Every pattern fixture and both control fixtures pass on two consecutive runs (a light-touch variance check appropriate to eyeball evaluation). SKILL.md still inside the 180–240 line target.
**Dependencies:** Task 4

### Task 6 — Description-improver pass
**Description:** Run skill-creator's description-improver to tune the SKILL.md `description:` frontmatter for triggering accuracy on trigger phrases from the approved plan ("render this doc as HTML", "make this reviewable", "convert design doc to HTML", "I want to share this plan").
**Done when:** Description-improver reports an improved or equal triggering score vs. baseline; the tuned description is committed to SKILL.md.
**Dependencies:** Task 5

### Task 7 — Wire up routing in README and using-this-pack
**Description:** Add a `render-html` row to the engineering/review table in `README.md`; add a routing entry to `skills/using-this-pack/SKILL.md` mapping the trigger phrases above to `render-html`.
**Done when:** `README.md` lists render-html with its one-line description; `using-this-pack/SKILL.md` routes the trigger phrases to `render-html`.
**Dependencies:** Task 6

### Task 8 — End-to-end verification on a real artefact
**Description:** Run `/render-html` on a real artefact already in the repo (an existing `docs/designs/*.md` or `docs/tasks/*.md`, not a synthetic fixture). Validate against the full verification checklist from the approved plan in two browsers.
**Done when:** All checks pass: (a) output written alongside source, (b) opens in Chrome AND Safari via `file://` with zero network requests in DevTools Network tab, (c) no console errors/warnings, (d) every H2/H3 reachable via TOC, (e) every applicable pattern renders correctly, (f) file size < 500KB, (g) print preview hides the TOC and breaks pages reasonably, (h) re-rendering the same source produces a diff only in provenance/timestamp lines.
**Dependencies:** Task 7

## Resolved decisions

- **Fixtures location:** `skills/render-html/evals/` (co-located with the skill). Safe because the Claude Code plugin loader only auto-loads `SKILL.md` from each skill directory — subdirectory contents are read on demand by the agent, not eagerly loaded into context. Confirmed against the loader behaviour observed in `.claude-plugin/plugin.json` discovery. Re-check if skill-creator publishes contrary best-practice guidance.
- **Pattern detection:** hybrid — heading-name heuristics are the primary signal, with an optional explicit override via a fenced annotation (` ```pattern:alternatives `) for cases where authors want precision or where their headings don't match the catalogue. Rationale: pde skills already produce consistent heading names (design-doc enforces "Problem", "Alternatives considered", etc. by anatomy), so heading-name detection works out of the box for the most common inputs. The annotation escape hatch preserves the "any structured md" property without forcing every author to mark up their docs. Pure-heuristic loses on renames; pure-annotation breaks zero-effort rendering; hybrid avoids both failure modes.
- **Output file collision:** overwrite with a confirmation prompt. When `<source>.html` exists, the skill must prompt before writing. Affects Task 1's acceptance criterion (below).
- **Eval harness scope for v0.1:** define fixtures + expected-output descriptions and *eyeball* results during iteration. Defer automated scoring to v0.2. Context: skill-creator's full loop wants (a) fixture inputs, (b) machine-checkable expectations, (c) running claude-with-the-skill against each fixture, (d) automated pass/fail scoring, (e) iterate until scores stabilise. Automated scoring catches regressions when the pattern catalogue grows, but for the initial 8 patterns the iteration cost of eyeballing is lower than the cost of building the scoring harness. Revisit once we add a 9th pattern or a regression appears.
