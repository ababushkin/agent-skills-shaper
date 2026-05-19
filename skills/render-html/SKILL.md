---
name: render-html
description: >
  Convert a markdown design doc, plan, ADR, or roadmap into a single self-contained
  HTML file for human review. Use when an artefact is about to go to review or
  sign-off and the reviewer experience matters — markdown flattens spatial content
  (alternatives, dependency graphs, diffs, timelines) that HTML can present
  faithfully. Trigger phrases: "render this doc as HTML", "make this reviewable",
  "convert design doc to HTML", "I want to share this plan", "share this for
  review", "make a readable version". Use this skill whenever the user is about to
  hand a markdown artefact to a human reviewer, even if they don't explicitly say
  the word HTML.
pack: engineering
lifecycle_stage: review
principles_implemented:
  - source: eng-agentic
    id: P7
    bucket: standalone
  - source: eng-universal
    id: P1
    bucket: standalone
length_target: 120-180
author: Anton Babushkin
predecessor:
  repo: none
  skill: none
  relation: new
kept_from_predecessor: n/a
changed_from_predecessor: n/a
---

# Render HTML

## Purpose

This skill converts a markdown artefact — design doc, task list, ADR, roadmap, postmortem — into one self-contained HTML file written next to the source as `<source>.html`. The deliverable is for humans about to review or sign off on the artefact, not for archival or publication. It is the operational form of agentic Principle 7 (memory lives in artefacts): the doc itself, made navigable and legible, is the persistent record reviewers and future agents read. And it is a lever on universal Principle 1 (shipped is not done; observed is done): better review UX raises the rate at which review actually happens, which raises the rate at which outcomes get observed.

## When to use

- The user asks to "render", "convert to HTML", "make this reviewable", or "share this doc" and points at a markdown file.
- A markdown artefact is about to go to a human reviewer for design review, code review prep, ADR sign-off, or stakeholder alignment.
- The doc is long enough that navigation matters (more than ~3 H2 sections) or contains structure that flattens badly in markdown previewers.

## When not to use

- **Drafting** — write the markdown first. HTML rendering is for finished or near-finished artefacts, not works in progress. The output is regenerated each time the source changes; rendering mid-draft burns cycles for no review benefit.
- **Single-screen documents** — a 30-line note doesn't earn the overhead of a TOC and shell. Send the markdown.
- **Documents the reviewer will edit** — HTML round-trip back to markdown is not supported. If reviewers want to suggest edits, send the markdown or use `/crit`.
- **Multi-document sites** — one source in, one file out. For a site, use a static-site generator.

## Inputs

- Path to a single `.md` file with at least one H1 and structured H2/H3 sections.
- Optional: prior `<source>.html` exists alongside the source (triggers overwrite confirmation).

## Outputs

- A single HTML file written to `<source>.html` — same directory as the source, same basename, `.html` extension.
- The file is self-contained: inline `<style>`, inline `<script>`, no `<link rel="stylesheet">`, no `<script src=>`, no remote images. Opens correctly via `file://` with the network offline.
- Size budget: ≤ ~300KB for typical inputs; hard cap 500KB.

## Workflow

**Step 1 — Source check [GATE]**
Read the source markdown. Confirm it has at least one H1 and at least one H2. If not, stop and report: "render-html expects structured markdown — source has no H1/H2." Do not invent structure to make the doc renderable. The skill is a renderer, not a restructurer.

**Step 2 — Overwrite check [GATE]**
Compute the output path: replace the source's `.md` extension with `.html`. If a file already exists at that path, prompt the user for confirmation before proceeding: "`<output-path>` exists. Overwrite? (y/n)". Do not silently overwrite. Do not append timestamps or version suffixes — re-rendering must be idempotent so diffs are meaningful. If the user declines, stop.

**Step 3 — Inventory headings**
Walk the markdown and collect every H2 and H3 in document order. Generate a stable slug for each (kebab-case from the heading text, deduplicated with `-2`, `-3` if needed). These become both anchor IDs in the body and the TOC entries in the sidebar. H1 is the document title — it goes in the page header, not the TOC.

**Step 4 — Convert body**
Walk the markdown section by section (H2-delimited). For each section, read `<skill-base>/references/html-patterns.md` and check the patterns in declared order — first match wins. If a pattern matches, emit its HTML template and append its CSS rules to the collected pattern-CSS buffer. If nothing matches, render the section as straightforward prose using standard CommonMark semantics (H2/H3 with anchor IDs from Step 3, paragraphs, lists, blockquotes, fenced code blocks preserving language hints, inline code, tables, links). Prose is the fallback, not the exception — false-positive pattern matches degrade reviewer trust faster than missing treatments.

**Step 5 — Compose the page**
Read the HTML shell from `<skill-base>/references/html-skeleton.md`. Substitute the tokens defined there: `{{title}}` (H1 from the source), `{{source-path}}`, `{{render-date}}` (ISO date only, no time, so same-day re-renders produce no diff), `{{toc-entries}}` (one `<li class="h2|h3">` per entry from Step 3), and `{{body-html}}` (the converted body from Step 4). Append the pattern-CSS buffer from Step 4 to the end of the inline `<style>` block — patterns add new selectors prefixed `p-`, never overriding the prose styles.

**Step 6 — Self-containment check [GATE]**
Before writing the file, verify the composed HTML contains zero `<link rel="stylesheet">`, zero `<script src=>`, and no `<img src="http...">` or `<img src="//...">`. SVG and base64 data URIs are allowed; remote URLs are not. If any external reference is present, fix the shell rather than ship the violation.

**Step 7 — Write and report**
Write the file to `<source>.html`. Report the output path, file size, and the count of H2/H3 entries in the TOC. Tell the user: "Open the file in your browser to verify TOC navigation and that no console errors appear." This handoff is required — the skill cannot observe the rendered page itself (universal Principle 1: the agent has shipped, the user observes).

## Artefact template

The HTML shell — `<!doctype html>` template, inline CSS, scrollspy JS, and the substitution-token contract (`{{title}}`, `{{source-path}}`, `{{render-date}}`, `{{toc-entries}}`, `{{body-html}}`) — lives in `references/html-skeleton.md`, bundled with this skill. Read it in Step 5 using the `Base directory for this skill` path shown in the skill context header: `<skill-base>/references/html-skeleton.md`. The shell is not duplicated here so a single edit to the skeleton updates both this skill and any future pattern-aware extensions of it.

## Common rationalisations

| Rationalisation | Rebuttal |
|---|---|
| "The markdown previewer is fine — they can just read it on GitHub." | GitHub flattens side-by-side alternatives into stacked blocks, hides long task lists in scroll, and gives no in-doc navigation for 40-section design docs. The reviewer experience is the bottleneck on outcome-observation (universal Principle 1); a renderer optimised for review removes it. |
| "I'll add a CDN link for the syntax highlighter / icon font / chart library." | The self-containment rule is load-bearing. Reviewers open these files via `file://`, attach them to emails, store them in private wikis. A broken CDN reference produces a silently-degraded page that the reviewer doesn't know to distrust. Inline or omit. |
| "Let me append a timestamp to the filename so I don't overwrite." | Idempotent re-rendering is the property that makes the output diffable and the source the canonical record. Versioned filenames produce orphaned copies. Prompt before overwriting (Step 2); do not invent new names. |
| "The source has no headings yet — let me invent some structure to make it renderable." | The skill is a renderer, not a restructurer. Inventing headings creates artefacts that look authoritative but were never agreed. If the source isn't structured, fix the source first. |
| "I'll skip the TOC for short docs to save space." | The TOC is the navigation contract reviewers learn to expect. Suppressing it inconsistently trains reviewers to scroll-hunt every doc. If a doc is short enough that the TOC is useless, the doc is short enough that the skill doesn't apply (see When not to use). |

## Red flags

- Reference files read from a relative path instead of `<skill-base>/references/` — causes silent degradation when invoked cross-project.
- Output contains `<link rel="stylesheet">`, `<script src=>`, or remote `<img>` URLs.
- File written to a path other than `<source>.html` (no timestamps, no version suffixes, no other directories).
- Existing output silently overwritten without prompt.
- TOC entries do not match the H2/H3 headings in the body.
- Body markdown silently dropped (e.g., a fenced code block missing) rather than rendered.
- File size above 500KB.
- HTML claims to render structure not present in the source.

## Verification / exit criteria

The skill has run correctly when:

1. `<source>.html` exists in the same directory as the source.
2. Opening the file via `file://` in a browser produces no console errors or warnings.
3. The DevTools Network panel shows zero network requests after load.
4. Every H2 and H3 in the source appears as a TOC entry and is reachable by clicking.
5. The page renders correctly with the network disabled.
6. File size is below 500KB.
7. Re-running the skill against the same source (after declining overwrite) leaves the existing file untouched; accepting overwrite produces an HTML whose diff against the previous render is limited to the provenance line.
8. The user has been told to open the file and confirm — the skill has not declared the render verified on its own (universal Principle 1).

## References

- `<skill-base>/references/html-skeleton.md` — the self-contained HTML shell, substitution tokens, and the hard self-containment rule (bundled with this skill)
- `<skill-base>/references/html-patterns.md` — the pattern catalogue (alternatives, timelines, callouts, kanban, diffs, chips) consulted in Step 4 (bundled with this skill)
- `rules/eng-principles-agentic.md` — P7 (memory lives in artefacts)
- `rules/eng-principles-universal.md` — P1 (shipped is not done; observed is done)
- Thariq Shihipar — "HTML effectiveness" (https://thariqs.github.io/html-effectiveness/) — case for HTML as a substrate for spatial review content
- `docs/skill-anatomy.md` — frontmatter and section-order contract
- `docs/tasks/render-html.md` — task plan; later iterations build the pattern catalogue at `references/html-patterns.md`
