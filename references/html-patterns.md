---
name: html-patterns
description: >
  Pattern catalogue for the render-html skill. Each entry maps a recognisable
  markdown shape to a richer HTML treatment — side-by-side columns, kanban,
  timelines, callouts, score chips. The skill consults this file during
  conversion (Step 4) and substitutes the matching markup into {{body-html}}.
type: reference
cited_by:
  - skills/render-html/SKILL.md
---

# HTML pattern catalogue

The render-html skill walks the markdown body section by section. For each section, it checks the patterns below in order. The **first match wins** — if no pattern matches, the section renders as plain prose (the walking-skeleton fallback).

Every pattern is defined by:

1. **Detect** — the markdown signal that triggers the treatment. Cheap to check; conservative (false-negative is fine, false-positive is bad — wrongly-treated content is harder to debug than untreated).
2. **HTML** — the output markup. All class names are prefixed `p-` so they don't collide with prose styles.
3. **CSS** — additions appended to the shell's inline `<style>` block. The shell's prose styles remain the fallback; pattern CSS only adds, never overrides.

The hard self-containment rule from `html-skeleton.md` applies to every pattern: no external CSS, no external JS, no remote images. Inline SVG is preferred for visual elements.

---

## P1 — Alternatives considered → side-by-side columns

**Detect.** A section whose heading text matches `/alternatives?( considered)?/i`, OR a section containing two-to-four sibling H3s each followed by a bulleted list whose first item starts with `Pros:` or `Cons:` (case-insensitive). Maximum four columns — beyond that, fall back to prose (columns become unreadable). **Does not match** ADR `Rationale` sections whose options use bold-paragraph headers (`**Why X:**`) rather than H3 — those go to P11.

**HTML.**

```html
<section class="p-alternatives">
  <div class="p-alt-col">
    <h3>Alternative A — short name</h3>
    <dl>
      <dt>Pros</dt><dd><ul><li>...</li></ul></dd>
      <dt>Cons</dt><dd><ul><li>...</li></ul></dd>
      <dt>Cost</dt><dd>...</dd>
      <dt>Reversibility</dt><dd>...</dd>
    </dl>
  </div>
  <!-- repeat per alternative -->
</section>
```

**CSS.**

```css
.p-alternatives { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin: 16px 0; }
.p-alt-col { border: 1px solid var(--rule); border-radius: 6px; padding: 14px 16px; background: rgba(127,127,127,0.03); }
.p-alt-col h3 { margin-top: 0; font-size: 15px; }
.p-alt-col dl { margin: 0; }
.p-alt-col dt { font-size: 11px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); margin-top: 10px; }
.p-alt-col dd { margin: 4px 0 0; font-size: 14px; }
.p-alt-col ul { margin: 4px 0; padding-left: 18px; }
```

**Accessibility.** Each column is a `<section>` with a unique `<h3>`; the columns still appear in DOM order, so screen readers read them sequentially. No keyboard interaction needed — pure layout.

---

## P2 — Task list with dependencies → vertical timeline

**Detect.** A section containing an ordered list (or sequence of H3s named `Task N — title` / `Step N`) where two or more entries mention "depends on", "after", "blocks", or "blocked by" in their first paragraph. Pure task lists without dependency language stay as ordinary ordered lists.

**HTML.**

```html
<ol class="p-timeline">
  <li class="p-task" id="task-1">
    <div class="p-task-marker" aria-hidden="true">1</div>
    <div class="p-task-body">
      <h3>Task 1 — name</h3>
      <p class="p-task-deps">Depends on: <em>none</em></p>
      <p>Task description prose…</p>
    </div>
  </li>
  <!-- repeat per task; dependency lines link to #task-N -->
</ol>
```

**CSS.**

```css
.p-timeline { list-style: none; padding: 0; margin: 16px 0; position: relative; }
.p-timeline::before { content: ""; position: absolute; left: 14px; top: 0; bottom: 0; width: 2px; background: var(--rule); }
.p-task { position: relative; padding-left: 44px; margin-bottom: 18px; }
.p-task-marker { position: absolute; left: 0; top: 0; width: 30px; height: 30px; border-radius: 50%; background: var(--bg); border: 2px solid var(--accent); color: var(--accent); display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 13px; }
.p-task-body h3 { margin: 4px 0 6px; font-size: 16px; }
.p-task-deps { color: var(--muted); font-size: 13px; margin: 0 0 8px; }
.p-task-deps a { color: var(--accent); text-decoration: none; }
```

**Accessibility.** Still an `<ol>` — screen readers announce the task count and order. Dependency phrases become inline links (`<a href="#task-2">Task 2</a>`); marker is `aria-hidden`.

---

## P3 — Design-doc blocks → coloured callouts

**Detect.** H2 headings whose text matches one of: `Problem`, `Context`, `Constraints`, `Decision` (or `Recommended approach`), `Consequences`, `Open questions`. Apply per matching H2 — sibling non-matching H2s render as prose.

**HTML.**

```html
<section class="p-callout p-callout-problem">
  <header class="p-callout-head"><span class="p-callout-icon" aria-hidden="true">▶</span> Problem</header>
  <div class="p-callout-body">
    <!-- prose -->
  </div>
</section>
```

Mapping (used for `p-callout-<key>`): `problem` → red, `context` → grey, `constraints` → amber, `decision` → blue, `consequences` → green, `open-questions` → purple.

**CSS.**

```css
.p-callout { margin: 20px 0; border-left: 4px solid var(--cb, var(--rule)); border-radius: 0 6px 6px 0; background: var(--cbg, rgba(127,127,127,0.04)); padding: 12px 16px; }
.p-callout-head { font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--cb, var(--muted)); margin-bottom: 6px; font-weight: 600; }
.p-callout-icon { display: inline-block; margin-right: 4px; }
.p-callout-body > :first-child { margin-top: 0; }
.p-callout-body > :last-child { margin-bottom: 0; }
.p-callout-problem      { --cb: #dc3545; --cbg: rgba(220,53,69,0.06); }
.p-callout-context      { --cb: #6c757d; --cbg: rgba(108,117,125,0.06); }
.p-callout-constraints  { --cb: #fd7e14; --cbg: rgba(253,126,20,0.07); }
.p-callout-decision     { --cb: #0a58ca; --cbg: rgba(10,88,202,0.06); }
.p-callout-consequences { --cb: #198754; --cbg: rgba(25,135,84,0.06); }
.p-callout-open-questions { --cb: #6f42c1; --cbg: rgba(111,66,193,0.06); }
```

**Accessibility.** Colour is supplemental; the heading text carries the meaning. Border + label work for users who can't perceive the hue.

**Sub-buckets inside `Consequences`.** When a `Consequences` callout contains H3s (or bold-paragraph headings) named `Positive`, `Negative`, `Neutral` / `Open`, render each as a coloured sub-block inside the callout rather than as nested H3s. Sub-block CSS:

```css
.p-conseq { margin: 12px 0; padding: 10px 14px; border-radius: 6px; }
.p-conseq-positive { background: rgba(25,135,84,0.05);  border-left: 3px solid #198754; }
.p-conseq-negative { background: rgba(220,53,69,0.05);  border-left: 3px solid #dc3545; }
.p-conseq-neutral  { background: rgba(108,117,125,0.05); border-left: 3px solid #6c757d; }
```

This is a P3 extension, not a separate pattern — the parent callout is still `p-callout-consequences`.

---

## P4 — NFRs table → highlighted numeric table

**Detect.** Markdown table inside a section whose heading matches `/non-functional|NFRs?/i`, OR any table whose header row contains one of: `Target`, `SLO`, `p95`, `p99`, `Latency`, `Throughput`, `Availability`, `Budget`.

**HTML.** Standard `<table>` with `class="p-nfr"`; cells that parse as numbers (optionally with units `ms`, `s`, `%`, `/s`, `KB`, `MB`) get `class="p-num"`.

```html
<table class="p-nfr">
  <thead><tr><th>Metric</th><th>Target</th><th>Current</th></tr></thead>
  <tbody>
    <tr><td>p95 latency</td><td class="p-num">200 ms</td><td class="p-num">340 ms</td></tr>
  </tbody>
</table>
```

**CSS.**

```css
.p-nfr { width: 100%; }
.p-nfr th { background: rgba(127,127,127,0.06); font-size: 13px; text-transform: uppercase; letter-spacing: 0.03em; color: var(--muted); }
.p-nfr td.p-num { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; text-align: right; white-space: nowrap; }
.p-nfr tbody tr:hover { background: rgba(127,127,127,0.04); }
```

**Accessibility.** Standard table semantics; `<thead>`/`<tbody>` preserved.

---

## P5 — Open questions → checklist with owner / due

**Detect.** Section heading matches `/open questions?|outstanding questions?/i`. Body is a bullet list; each bullet may end with parenthetical metadata `(owner: name, due: 2026-06-01)` or markdown task-list syntax `- [ ]` / `- [x]`.

**HTML.**

```html
<ul class="p-questions">
  <li class="p-q">
    <input type="checkbox" disabled> <!-- checked if [x] -->
    <span class="p-q-text">Should we use Postgres or DynamoDB for the audit log?</span>
    <span class="p-q-meta">@anton · due 2026-06-01</span>
  </li>
</ul>
```

**CSS.**

```css
.p-questions { list-style: none; padding: 0; margin: 16px 0; }
.p-q { display: grid; grid-template-columns: auto 1fr auto; gap: 10px; align-items: baseline; padding: 8px 0; border-bottom: 1px dashed var(--rule); }
.p-q input[type=checkbox] { transform: translateY(2px); }
.p-q-text { color: var(--fg); }
.p-q-meta { color: var(--muted); font-size: 12px; font-variant-numeric: tabular-nums; }
```

**Accessibility.** The checkbox is `disabled` (read-only display); the parenthetical metadata is preserved as visible text, not buried in `title=` attributes.

---

## P6 — Diff / before-after → two-column annotated diff

**Detect.** Two adjacent fenced code blocks within the same H3 / paragraph where the first is labelled (in info string or preceding line) `before`, `was`, `old`, `current`, and the second `after`, `now`, `new`, `proposed`. Also: any code block with info string `diff` renders inline with `+`/`-` line colouring.

**HTML (two-column).**

```html
<div class="p-diff">
  <div class="p-diff-side p-diff-before">
    <header>Before</header>
    <pre><code>…</code></pre>
  </div>
  <div class="p-diff-side p-diff-after">
    <header>After</header>
    <pre><code>…</code></pre>
  </div>
</div>
```

**HTML (inline diff).** Standard `<pre><code class="language-diff">` with each line wrapped: `<span class="p-diff-add">+ …</span>`, `<span class="p-diff-del">- …</span>`.

**CSS.**

```css
.p-diff { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin: 16px 0; }
.p-diff-side header { font-size: 12px; text-transform: uppercase; color: var(--muted); margin-bottom: 4px; }
.p-diff-before pre { border-left: 3px solid #dc3545; }
.p-diff-after  pre { border-left: 3px solid #198754; }
.p-diff-add { background: rgba(25,135,84,0.12); display: block; }
.p-diff-del { background: rgba(220,53,69,0.12); display: block; }
@media (max-width: 720px) { .p-diff { grid-template-columns: 1fr; } }
```

**Accessibility.** Headers (`Before` / `After`) carry the meaning; colour stripe is supplemental.

---

## P7 — Roadmap Now / Next / Later → three-column kanban

**Detect.** Three sibling H2s or H3s with text exactly matching (case-insensitive, whitespace-tolerant): `Now`, `Next`, `Later`, **AND** each of those sections' body is predominantly a single `<ul>`/`<ol>` (no nested H3s, no Problem/Appetite/ICE callout sub-structure). If only two of the three columns are present and the bullet-only condition holds, still render as a kanban with the missing column shown empty. If the bullet-only condition fails (sections contain rich prose, callouts, or H3 sub-items per column), **do not apply** — fall back to prose so the column content stays readable. Evidence: collapsing a prose-heavy "Now" section into bullets destroys the Problem / Success criterion / Appetite / ICE structure roadmap items typically carry.

**HTML.**

```html
<div class="p-kanban">
  <div class="p-kanban-col" data-col="now">
    <header>Now</header>
    <ul>
      <li>Item one</li>
      <li>Item two</li>
    </ul>
  </div>
  <div class="p-kanban-col" data-col="next"> … </div>
  <div class="p-kanban-col" data-col="later"> … </div>
</div>
```

**CSS.**

```css
.p-kanban { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 20px 0; }
.p-kanban-col { border: 1px solid var(--rule); border-radius: 8px; padding: 12px 14px; background: rgba(127,127,127,0.03); min-height: 120px; }
.p-kanban-col header { font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); padding-bottom: 8px; border-bottom: 1px solid var(--rule); margin-bottom: 10px; font-weight: 600; }
.p-kanban-col[data-col="now"]   header { color: #198754; }
.p-kanban-col[data-col="next"]  header { color: #0a58ca; }
.p-kanban-col[data-col="later"] header { color: #6c757d; }
.p-kanban-col ul { padding-left: 18px; margin: 0; font-size: 14px; }
.p-kanban-col li { margin: 6px 0; }
@media (max-width: 720px) { .p-kanban { grid-template-columns: 1fr; } }
```

**Accessibility.** Each column is keyboard-navigable as ordinary text; the header colour is supplemental to the label.

---

## P8 — ICE scores → coloured score chips

**Detect.** Markdown table whose header row contains EITHER (a) `Impact`, `Confidence`, and `Ease` (in any order, plus an optional `Score` column), OR (b) a single `ICE` column alongside at least one of `Confidence` / `Slot` / `Theme` / `Kano` — real roadmaps frequently collapse the three sub-scores into one `ICE` total rather than listing each. Numeric cells are graded on the same red/amber/green band regardless of column. Em-dash placeholders (`—`) render as a muted chip.

**HTML.** Numeric cells become chips coloured by value (red 1–3, amber 4–6, green 7–10).

```html
<table class="p-ice">
  <thead><tr><th>Idea</th><th>Impact</th><th>Confidence</th><th>Ease</th><th>ICE</th></tr></thead>
  <tbody>
    <tr>
      <td>Onboarding revamp</td>
      <td><span class="p-chip" data-band="green">9</span></td>
      <td><span class="p-chip" data-band="amber">5</span></td>
      <td><span class="p-chip" data-band="red">3</span></td>
      <td><span class="p-chip" data-band="amber">135</span></td>
    </tr>
  </tbody>
</table>
```

**CSS.**

```css
.p-ice .p-chip { display: inline-block; min-width: 28px; padding: 2px 8px; border-radius: 999px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; text-align: center; font-weight: 600; }
.p-chip[data-band="red"]   { background: rgba(220,53,69,0.18); color: #dc3545; }
.p-chip[data-band="amber"] { background: rgba(253,126,20,0.18); color: #fd7e14; }
.p-chip[data-band="green"] { background: rgba(25,135,84,0.18); color: #198754; }
.p-chip[data-band="muted"] { background: rgba(127,127,127,0.12); color: var(--muted); }
.p-ice td:not(:first-child) { text-align: center; }
```

Chip bands: `1–3 → red`, `4–6 → amber`, `7–10 → green`, em-dash / missing → `muted`. ICE totals (any value above 10) are graded against the same 50 / 100 / 200 thresholds used for sequencing in roadmaps that follow `PRODUCT_RULES`.

**Accessibility.** Colour is supplemental; the numeric value is the source of truth. Chips render as plain numbers in print and to screen readers.

---

## P9 — YAML frontmatter → metadata grid

**Detect.** Source markdown begins with a YAML frontmatter block delimited by `---` on its own line, before the H1. Common in ADRs and design docs (fields like `id`, `status`, `date`, `authors`, `linear`, `supersedes`).

**HTML.** Render as a definition list immediately under the page title and the provenance meta line — before any body content.

```html
<dl class="p-frontmatter">
  <dt>id</dt><dd>ADR-engagement-modifier-constants</dd>
  <dt>status</dt><dd><span class="p-status p-status-accepted">accepted</span></dd>
  <dt>date</dt><dd>2026-05-14</dd>
  <dt>authors</dt><dd>Anton Babushkin</dd>
</dl>
```

**CSS.**

```css
.p-frontmatter { display: grid; grid-template-columns: auto 1fr; gap: 4px 14px; font-size: 13px; padding: 12px 14px; background: rgba(127,127,127,0.04); border-radius: 6px; margin-bottom: 24px; }
.p-frontmatter dt { color: var(--muted); text-transform: uppercase; font-size: 11px; letter-spacing: 0.04em; margin: 0; }
.p-frontmatter dd { margin: 0; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12.5px; }
```

The `status` field gets the P10 status-pill treatment automatically; other field values render as plain text. **Do not** drop frontmatter on the floor — readers use it to anchor the doc.

**Accessibility.** Definition list is the right semantic tag for key-value metadata; screen readers announce each pair.

---

## P10 — Status / state values → coloured pill

**Detect.** A frontmatter `status:` field, OR a top-of-doc bold line matching `/\*\*Status:\*\*\s+(\w+)/i`, OR a single-cell `Status` column in a table. Recognised values (case-insensitive): `accepted`, `proposed`, `draft`, `rejected`, `superseded`, `deprecated`, `flagged`, `ok`.

**HTML.**

```html
<span class="p-status p-status-accepted">Accepted</span>
```

**CSS.**

```css
.p-status { display: inline-block; padding: 2px 9px; border-radius: 999px; font-weight: 600; font-size: 11px; text-transform: uppercase; letter-spacing: 0.04em; }
.p-status-accepted, .p-status-ok        { background: rgba(25,135,84,0.18);  color: #198754; }
.p-status-proposed, .p-status-draft     { background: rgba(10,88,202,0.18);  color: #0a58ca; }
.p-status-rejected, .p-status-deprecated{ background: rgba(220,53,69,0.18);  color: #dc3545; }
.p-status-superseded, .p-status-flagged { background: rgba(253,126,20,0.18); color: #fd7e14; }
```

A pill is reusable wherever a state lives in the source — Slot columns (Now/Next/Later/Validation) in P7-rejected roadmap tables are a natural reuse site.

**Accessibility.** The label text carries the meaning; colour is supplemental.

---

## P11 — Rationale "Why X" blocks → labelled list groups

**Detect.** A section heading matches `/rationale/i` AND its body contains two-or-more bold-paragraph headers (`**Why X:**` / `**Why not Y:**`) each followed by a bullet list. Common in ADRs that consider multiple alternatives without dedicated H3s per option.

**HTML.** Each bold paragraph becomes the heading of a styled group; the following list is the group's body.

```html
<section class="p-rationale">
  <div class="p-rationale-group">
    <h4>Why Rails</h4>
    <ul><li>…</li></ul>
  </div>
  <div class="p-rationale-group">
    <h4>Why not a separate frontend</h4>
    <ul><li>…</li></ul>
  </div>
</section>
```

**CSS.**

```css
.p-rationale-group { margin: 14px 0; }
.p-rationale-group h4 { margin: 0 0 6px; font-size: 14px; color: var(--accent); font-weight: 600; }
.p-rationale-group ul { margin: 0; padding-left: 22px; }
```

**Precedence.** P11 ranks below P1 (Alternatives). When both could match (`Rationale` section whose options also have `Pros:`/`Cons:`), P1's side-by-side comparison is the stronger treatment.

**Accessibility.** `<h4>` keeps the headings in the document outline; lists keep list semantics.

---

## P12 — Labelled rubric cards (C1, C2, FR3 …) → repeated sub-field cards

**Detect.** Two or more sibling H3s whose text matches `/^([A-Z]+\d+)\s+[—–-]\s+/` (e.g. `C1 — Deadband: ±2%`, `FR3 — Idempotent writes`, `OQ5 — …`), AND each section repeats the same set of bold-paragraph sub-fields (e.g. **Reasoning**, **Alternative considered**, **Revision trigger**). The identifier prefix (`C`, `FR`, `OQ`, `NFR`, `ADR`) is rendered as a pill on the card header.

**HTML.**

```html
<div class="p-rubric" id="c1">
  <h3><span class="p-rubric-id">C1</span> Deadband: ±2% YoY</h3>
  <div class="p-rubric-formula">If <code>abs(yoy_change) &lt; 0.02</code>, set <code>direction = 0</code> …</div>
  <h4>Reasoning</h4><p>…</p>
  <h4>Alternative considered</h4><p>…</p>
  <h4>Revision trigger</h4><p>…</p>
</div>
```

The first paragraph (often a one-line formal definition or formula) becomes `p-rubric-formula`. Subsequent bold-paragraph sub-fields become `<h4>` headings inside the card.

**CSS.**

```css
.p-rubric { border: 1px solid var(--rule); border-left: 4px solid var(--accent); border-radius: 6px; padding: 14px 18px; margin: 16px 0; background: rgba(127,127,127,0.02); }
.p-rubric h3 { margin-top: 0; display: flex; gap: 12px; align-items: baseline; color: var(--fg); }
.p-rubric h3 .p-rubric-id { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; padding: 2px 8px; background: var(--accent); color: white; border-radius: 4px; }
.p-rubric h4 { font-size: 13px; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); margin: 12px 0 4px; font-weight: 600; }
.p-rubric-formula { background: rgba(10,88,202,0.06); border-left: 3px solid var(--accent); padding: 8px 12px; margin: 8px 0; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; }
```

**Why a dedicated pattern.** Plain-prose rendering of a 6-card ADR section (C1–C6 with Reasoning / Alternative / Revision trigger each) produces a wall of repeating H3+H4 that the reader has to mentally segment. The card boundary plus the identifier pill makes "which constant am I reading" answerable at a glance — which is most of what reviewers want when scanning a pre-registered constants ADR.

**Accessibility.** Heading levels (`<h3>` outer, `<h4>` inner) preserve the document outline; the card's visual boundary is decorative.

---

## Fallback

A section that matches no pattern renders with the shell's standard prose styles (`<h2>`, `<h3>`, `<p>`, `<ul>`, `<table>`, `<pre>`). Fallback is the default, not the exception — false-positive pattern matches degrade review trust faster than missing treatments.

## Adding a new pattern

When a new pattern earns its slot:

1. Add a section here following the same six-part structure: heading, **Detect**, **HTML**, **CSS**, **Accessibility**, brief rationale.
2. Number it sequentially (`P13 — …`) so cross-references stay stable.
3. Confirm the CSS only adds new selectors prefixed `p-` — it must not override any rule in `html-skeleton.md`.
4. If the detection signal could overlap an existing pattern, document the precedence rule explicitly. The first-match-wins ordering of this file is the resolution mechanism.
