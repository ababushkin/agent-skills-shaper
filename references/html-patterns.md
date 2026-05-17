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

**Detect.** A section whose heading text matches `/alternatives?( considered)?/i`, OR a section containing two-to-four sibling H3s each followed by a bulleted list whose first item starts with `Pros:` or `Cons:` (case-insensitive). Maximum four columns — beyond that, fall back to prose (columns become unreadable).

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

**Detect.** A section whose body contains three sibling H2s or H3s with text exactly matching (case-insensitive, whitespace-tolerant): `Now`, `Next`, `Later`. If only two of the three are present, still render as a kanban with the missing column shown empty.

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

**Detect.** Markdown table whose header row contains `Impact`, `Confidence`, `Ease` (in any order, plus an optional `ICE` or `Score` column), with numeric cells `1`–`10`.

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
.p-ice td:not(:first-child) { text-align: center; }
```

**Accessibility.** Colour is supplemental; the numeric value is the source of truth. Chips render as plain numbers in print and to screen readers.

---

## Fallback

A section that matches no pattern renders with the shell's standard prose styles (`<h2>`, `<h3>`, `<p>`, `<ul>`, `<table>`, `<pre>`). Fallback is the default, not the exception — false-positive pattern matches degrade review trust faster than missing treatments.

## Adding a new pattern

When a new pattern earns its slot:

1. Add a section here following the same six-part structure: heading, **Detect**, **HTML**, **CSS**, **Accessibility**, brief rationale.
2. Number it sequentially (`P9 — …`) so cross-references stay stable.
3. Confirm the CSS only adds new selectors prefixed `p-` — it must not override any rule in `html-skeleton.md`.
4. If the detection signal could overlap an existing pattern, document the precedence rule explicitly. The first-match-wins ordering of this file is the resolution mechanism.
