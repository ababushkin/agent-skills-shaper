---
name: html-patterns
description: >
  Pattern catalogue for the render-html skill. Each entry maps a recognisable
  markdown shape — found in implementation plans and design docs — to a
  product-UI HTML treatment: section-header tags, hover cards, decision
  panels, summary strips, SVG diagrams, mockup frames, code panels, risk
  tables. The skill consults this file during conversion (Step 4) and
  substitutes the matching markup into {{body-html}}.
type: reference
cited_by:
  - skills/render-html/SKILL.md
---

# HTML pattern catalogue

The render-html skill walks the markdown body section by section. For each section, it checks the patterns below in order. The **first match wins** — if no pattern matches, the section renders with the shell's prose defaults (which are themselves styled — see `html-skeleton.md`).

Every pattern is defined by:

1. **Detect** — the markdown signal that triggers the treatment. Cheap to check; conservative (false-negative is fine, false-positive is bad — wrongly-treated content is harder to debug than untreated).
2. **HTML** — the output markup. All class names are prefixed `p-` so they don't collide with the shell's utilities.
3. **CSS** — additions appended to the shell's inline `<style>` block. The shell's prose styles remain the fallback; pattern CSS only adds, never overrides.

The hard self-containment rule from `html-skeleton.md` applies to every pattern: no external CSS, no external JS, no remote images. Inline SVG is preferred for visual elements. Colour tokens come from the shell's `:root` palette (`--accent`, `--ok`, `--warn`, `--info`, `--danger`, each with a `-soft` variant) — patterns must not introduce ad-hoc hex values.

---

## P1 — Alternatives considered → side-by-side cards

**Detect.** A section whose heading text matches `/alternatives?( considered)?/i`, OR a section containing two-to-four sibling H3s each followed by a bulleted list whose first item starts with `Pros:` or `Cons:` (case-insensitive). Maximum four columns — beyond that, fall back to prose (columns become unreadable). **Does not match** ADR `Rationale` sections whose options use bold-paragraph headers (`**Why X:**`) rather than H3 — those go to P11.

**HTML.** Each alternative becomes a hover-state card in an auto-fit grid; pros/cons/cost/reversibility render as a small definition list inside.

```html
<div class="p-alt-grid">
  <article class="p-alt-card">
    <header><h3>Alternative A — short name</h3><span class="p-alt-verdict p-alt-verdict-chosen">Chosen</span></header>
    <dl>
      <dt>Pros</dt><dd><ul><li>…</li></ul></dd>
      <dt>Cons</dt><dd><ul><li>…</li></ul></dd>
      <dt>Cost</dt><dd>…</dd>
      <dt>Reversibility</dt><dd>…</dd>
    </dl>
  </article>
  <!-- repeat per alternative -->
</div>
```

The verdict pill (`Chosen` / `Rejected` / em-dash) is optional — apply only if the source explicitly marks one option as chosen.

**CSS.**

```css
.p-alt-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin: 20px 0; }
.p-alt-card { background: var(--surface); border: 1px solid var(--rule); border-radius: 10px; padding: 18px 20px; transition: border-color 0.15s, transform 0.15s; }
.p-alt-card:hover { border-color: var(--accent); }
.p-alt-card > header { display: flex; justify-content: space-between; align-items: baseline; gap: 8px; margin-bottom: 12px; }
.p-alt-card h3 { margin: 0; font-size: 16px; font-weight: 700; color: var(--fg); }
.p-alt-card dl { margin: 0; }
.p-alt-card dt { font-size: 12px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--muted); margin-top: 12px; font-weight: 700; }
.p-alt-card dd { margin: 4px 0 0; font-size: 15px; color: var(--fg-soft); line-height: 1.55; }
.p-alt-card ul { margin: 4px 0; padding-left: 20px; }
.p-alt-verdict { font: 700 12px/1 "Inter", ui-sans-serif, sans-serif; letter-spacing: 0.04em; text-transform: uppercase; padding: 4px 8px; border-radius: 4px; }
.p-alt-verdict-chosen { background: var(--ok-soft); color: var(--ok); }
.p-alt-verdict-rejected { background: var(--rule-soft); color: var(--muted); }
```

**Accessibility.** Each card is an `<article>` with a unique `<h3>`; cards appear in DOM order so screen readers read them sequentially. The verdict pill text carries the meaning; colour is supplemental.

---

## P2 — Task list with dependencies → vertical timeline

**Detect.** A section containing an ordered list (or sequence of H3s named `Task N — title` / `Step N`) where two or more entries mention "depends on", "after", "blocks", or "blocked by" in their first paragraph. Pure task lists without dependency language stay as ordinary ordered lists.

**HTML.** Three-column row per task: optional `when` (date/sprint label), dot-and-line rail, body. The rail column is always present so the timeline reads as a connected sequence; the `when` column is omitted across the whole timeline if no task has scheduling info.

```html
<ol class="p-timeline">
  <li class="p-task" id="task-1">
    <div class="p-task-when">Week 1 · Mon–Tue</div>
    <div class="p-task-rail" aria-hidden="true">
      <span class="p-task-dot p-task-dot-done"></span>
      <span class="p-task-line"></span>
    </div>
    <div class="p-task-body">
      <h3>Schema &amp; API contract</h3>
      <p>New <code>comments</code> and <code>comment_reads</code> tables, migrations, tRPC router stubs. Contract reviewed before anything else lands.</p>
      <p class="p-task-deps">Depends on: <em>none</em></p>
      <div class="p-task-tags">
        <span class="p-task-tag">packages/db</span>
        <span class="p-task-tag">packages/api</span>
        <span class="p-task-tag">migration 0042</span>
      </div>
    </div>
  </li>
  <!-- repeat per task; final <li> drops the trailing line -->
</ol>
```

The dot has two states: default (`p-task-dot`, hollow ring in `--accent`) and done (`p-task-dot-done`, solid `--ok`). The line is omitted on the final task. Tag chips are optional — emit them when the source mentions concrete packages, components, file paths, or migration IDs.

**CSS.**

```css
.p-timeline { list-style: none; padding: 0; margin: 24px 0; }
.p-task { display: grid; grid-template-columns: 132px 28px 1fr; gap: 0 18px; }
.p-task[data-no-when] { grid-template-columns: 28px 1fr; }
.p-task-when { text-align: right; font: 12.5px ui-monospace, SFMono-Regular, monospace; color: var(--muted); padding-top: 6px; }
.p-task-rail { display: flex; flex-direction: column; align-items: center; }
.p-task-dot { width: 14px; height: 14px; border-radius: 50%; background: var(--bg); border: 3px solid var(--accent); margin-top: 6px; flex-shrink: 0; }
.p-task-dot-done { background: var(--ok); border-color: var(--ok); }
.p-task-line { width: 2px; flex: 1; background: var(--rule); margin: 4px 0; }
.p-task:last-child .p-task-line { display: none; }
.p-task-body { padding-bottom: 28px; }
.p-task-body h3 { margin: 0 0 6px; font-size: 17px; font-weight: 600; color: var(--fg); }
.p-task-body p { font-size: 14.5px; color: var(--fg-soft); margin: 0 0 10px; line-height: 1.55; max-width: 65ch; }
.p-task-deps { color: var(--muted); font-size: 13.5px; }
.p-task-deps a { color: var(--accent); text-decoration: none; }
.p-task-deps a:hover { text-decoration: underline; }
.p-task-tags { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
.p-task-tag { font: 11.5px ui-monospace, SFMono-Regular, monospace; background: var(--rule-soft); border: 1px solid var(--rule); border-radius: 6px; padding: 3px 8px; color: var(--fg-soft); }
@media (max-width: 720px) { .p-task, .p-task[data-no-when] { grid-template-columns: 22px 1fr; } .p-task-when { display: none; } }
```

**Accessibility.** Still an `<ol>` — screen readers announce the task count and order. Dependency phrases become inline links (`<a href="#task-2">Task 2</a>`); rail (`p-task-rail`) is `aria-hidden`. The `when` label is plain text and reads as part of each task.

---

## P3 — Design-doc blocks → tagged H2 + accent panel

**Detect.** H2 headings whose text matches one of: `Problem`, `Context`, `Constraints`, `Decision` (or `Recommended approach`), `Consequences`, `Open questions`. Apply per matching H2 — sibling non-matching H2s render with the shell's plain section header.

**HTML.** The H2 picks up a small tag pill matching the section type. For `Decision`, the body wraps in a **decision panel** (gradient-filled, indigo border, with a `→ We will` label). Other matches use a thin coloured left-border on the section body but otherwise inherit prose defaults — the type-tag does the visual work.

```html
<section class="s p-block p-block-decision" id="decision">
  <header>
    <span class="ix">02</span>
    <h2>Decision <span class="p-block-tag p-block-tag-decision">Chosen</span></h2>
  </header>
  <div class="p-decision-panel">
    <span class="p-decision-label">→ We will</span>
    Build as a Ruby on Rails 8 monolith using Rails defaults wherever possible.
  </div>
</section>
```

```html
<section class="s p-block p-block-context" id="context">
  <header>
    <span class="ix">01</span>
    <h2>Context <span class="p-block-tag p-block-tag-context">Background</span></h2>
  </header>
  <p>…</p>
</section>
```

Tag-label mapping: `Problem` → `Problem` (danger), `Context` → `Background` (muted), `Constraints` → `Limits` (warn), `Decision` → `Chosen` (info / accent), `Consequences` → `Outcomes` (ok), `Open questions` → `Open` (accent-soft).

**CSS.**

```css
.p-block-tag { margin-left: 12px; font: 700 12px/1 "Inter", ui-sans-serif, sans-serif; letter-spacing: 0.05em; text-transform: uppercase; vertical-align: 3px; padding: 4px 8px; border-radius: 4px; }
.p-block-tag-problem    { background: var(--danger-soft); color: var(--danger); }
.p-block-tag-context    { background: var(--rule-soft);   color: var(--muted); }
.p-block-tag-constraints{ background: var(--warn-soft);   color: var(--warn); }
.p-block-tag-decision   { background: var(--info-soft);   color: var(--info); }
.p-block-tag-consequences{ background: var(--ok-soft);    color: var(--ok); }
.p-block-tag-open-questions { background: var(--accent-soft); color: var(--accent); }

.p-decision-panel {
  background: linear-gradient(180deg, var(--info-soft), transparent 80%);
  border: 1px solid var(--info); border-radius: 12px;
  padding: 22px 24px; margin: 14px 0;
  font-size: 18px; line-height: 1.5; color: var(--fg); font-weight: 500;
}
.p-decision-panel .p-decision-label { display: block; font: 700 13px/1 "Inter", ui-sans-serif, sans-serif; letter-spacing: 0.08em; text-transform: uppercase; color: var(--info); margin-bottom: 10px; }
```

**Accessibility.** Colour is supplemental; the tag text carries the meaning. The decision panel's label (`→ We will`) is a real text node, not a pseudo-element, so screen readers announce it.

**Sub-buckets inside `Consequences`.** When a `Consequences` section's body contains H3s (or bold-paragraph headings) named `Positive`, `Negative`, `Neutral` / `Open`, render each as a coloured sub-card rather than as nested H3s:

```html
<div class="p-conseq-grid">
  <div class="p-conseq p-conseq-positive"><h4>Positive</h4><ul>…</ul></div>
  <div class="p-conseq p-conseq-negative"><h4>Negative</h4><ul>…</ul></div>
  <div class="p-conseq p-conseq-neutral"><h4>Neutral</h4><ul>…</ul></div>
</div>
```

```css
.p-conseq-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 14px; margin: 20px 0; }
.p-conseq { background: var(--surface); border: 1px solid var(--rule); border-left-width: 4px; border-radius: 8px; padding: 14px 16px; }
.p-conseq h4 { margin: 0 0 10px; font: 700 12px/1 "Inter", ui-sans-serif, sans-serif; letter-spacing: 0.06em; text-transform: uppercase; }
.p-conseq-positive { border-left-color: var(--ok);     } .p-conseq-positive h4 { color: var(--ok); }
.p-conseq-negative { border-left-color: var(--danger); } .p-conseq-negative h4 { color: var(--danger); }
.p-conseq-neutral  { border-left-color: var(--muted);  } .p-conseq-neutral h4  { color: var(--muted); }
```

This is a P3 extension, not a separate pattern — the parent section is still `p-block-consequences`.

**Consequences as checklist (when flat).** If the `Consequences` body is a single flat bullet list with no sub-buckets, render each bullet as a checklist-card row:

```html
<div class="p-conseq-list">
  <div class="p-conseq-item"><span class="p-conseq-check">→</span><span>All code lives in one repo and deploys as one unit</span></div>
</div>
```

```css
.p-conseq-list { display: grid; gap: 10px; margin: 14px 0; }
.p-conseq-item { display: grid; grid-template-columns: 32px 1fr; gap: 14px; align-items: start; padding: 14px 16px; background: var(--surface); border: 1px solid var(--rule); border-radius: 8px; font-size: 15px; line-height: 1.55; color: var(--fg); }
.p-conseq-check { width: 24px; height: 24px; border-radius: 50%; background: var(--ok-soft); color: var(--ok); display: grid; place-items: center; font-size: 14px; font-weight: 700; }
```

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
.p-nfr td.p-num { font-family: ui-monospace, SFMono-Regular, monospace; text-align: right; white-space: nowrap; font-size: 14px; }
.p-nfr tbody tr:hover { background: var(--rule-soft); }
```

The shell already styles `<table>` cleanly; P4 only adds numeric-cell alignment + hover. **Accessibility.** Standard table semantics; `<thead>`/`<tbody>` preserved.

---

## P5 — Open questions → left-accent decision cards

**Detect.** Section heading matches `/open questions?|outstanding questions?|to decide|decisions? to make/i`. Body is either a bullet list (one item per question) or a sequence of bold-paragraph headers (`**Do we allow editing?**`) each followed by a short paragraph of context. Optional trailing metadata `(decide with: design, before slice 2)` or `(owner: @anton, due: 2026-06-01)` lifts into a footer line.

**HTML.** Each question becomes a vertically-stacked card with a clay accent on the left, a bold question, a context paragraph, and an optional owner/deadline footer in mono.

```html
<div class="p-questions">
  <div class="p-q">
    <div class="p-q-title">Do we allow editing, or only delete-and-repost?</div>
    <div class="p-q-body">Editing needs an <code>edited_at</code> column and an "edited" affordance. Delete-and-repost is simpler but loses the reply anchor. Leaning toward delete-only for v1.</div>
    <div class="p-q-owner">Decide with · design, before slice 2</div>
  </div>
  <div class="p-q">
    <div class="p-q-title">Email digest cadence when a user has the app closed</div>
    <div class="p-q-body">Immediate-per-mention will be noisy. Proposal: batch on a 15-minute window, collapse to one email per task, and respect quiet hours from the existing settings table.</div>
    <div class="p-q-owner">Decide with · platform, before slice 4</div>
  </div>
</div>
```

The `p-q-owner` footer is optional. When metadata isn't present in the source, omit the `<div>` entirely rather than render an empty footer.

**CSS.**

```css
.p-questions { display: flex; flex-direction: column; gap: 14px; margin: 20px 0; max-width: 820px; }
.p-q { background: var(--surface); border: 1px solid var(--rule); border-left: 4px solid var(--accent); border-radius: 10px; padding: 16px 20px; }
.p-q-title { font-weight: 600; font-size: 15.5px; color: var(--fg); margin-bottom: 6px; }
.p-q-body { font-size: 14px; color: var(--fg-soft); line-height: 1.55; }
.p-q-body code { font-size: 0.92em; padding: 1px 5px; background: var(--rule-soft); border-radius: 3px; }
.p-q-owner { font: 11.5px ui-monospace, SFMono-Regular, monospace; color: var(--muted); margin-top: 10px; }
```

**Accessibility.** Plain text hierarchy (title → body → owner). The accent border is decorative — the bold title carries the visual weight and reads cleanly on screen readers.

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
.p-diff { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 20px 0; }
.p-diff-side header { font: 700 12px/1 "Inter", ui-sans-serif, sans-serif; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin-bottom: 8px; }
.p-diff-before pre { border-left: 3px solid var(--danger); }
.p-diff-after  pre { border-left: 3px solid var(--ok); }
.p-diff-add { background: var(--ok-soft); color: var(--ok); display: block; }
.p-diff-del { background: var(--danger-soft); color: var(--danger); display: block; }
@media (max-width: 720px) { .p-diff { grid-template-columns: 1fr; } }
```

**Accessibility.** Headers (`Before` / `After`) carry the meaning; colour stripe is supplemental.

---

<!-- P7 (Now/Next/Later kanban) and P8 (ICE scores) are out of scope for v1
     — they belong to a future render-roadmap skill. P-numbers are not reused;
     downstream patterns keep P9–P12 so cross-references stay stable. -->

---

## P9 — YAML frontmatter → metadata grid (lifted into doc head)

**Detect.** Source markdown begins with a YAML frontmatter block delimited by `---` on its own line, before the H1. Common in ADRs and design docs (fields like `id`, `status`, `date`, `authors`, `linear`, `supersedes`).

**HTML.** Frontmatter fields **lift into the shell's `{{meta-grid}}` slot** under the doc head — they do not render as a separate block in the body. The shell's `.meta-grid` styles already cover the visual treatment; P9 only specifies the *lifting* behaviour. The `status` field also lifts into `{{header-pills}}` via the P10 pill treatment.

```html
<!-- inside the shell's <dl class="meta-grid"> -->
<dt>id</dt>      <dd>ADR-engagement-modifier-constants</dd>
<dt>authors</dt> <dd>Anton Babushkin</dd>
<dt>linear</dt>  <dd><a href="https://linear.app/…">ABA-110</a></dd>
<dt>supersedes</dt><dd>—</dd>
<dt>source</dt>  <dd>docs/adrs/engagement-modifier-constants.md</dd>
<dt>rendered</dt><dd>2026-05-17</dd>
```

`source` and `rendered` are always included; frontmatter fields fold in alphabetically after them, except `status` (which becomes a header pill, not a grid row) and `date` (which becomes a date pill in the header). **Do not drop frontmatter on the floor** — readers use it to anchor the doc.

**Accessibility.** Definition-list semantics; screen readers announce each key-value pair.

---

## P10 — Status / state values → coloured pill

**Detect.** A frontmatter `status:` field, OR a top-of-doc bold line matching `/\*\*Status:\*\*\s+(\w+)/i`, OR a single-cell `Status` column in a table. Recognised values (case-insensitive): `accepted`, `proposed`, `draft`, `rejected`, `superseded`, `deprecated`, `flagged`, `ok`.

**HTML.** When detected from frontmatter or top-of-doc bold line, the pill **lifts into the shell's `{{header-pills}}` slot** (using the shell's `.pill` utility — no new CSS needed):

```html
<span class="pill pill-accepted"><span class="dot"></span>Accepted</span>
```

When detected inside a table cell, render in-place:

```html
<td><span class="pill pill-accepted"><span class="dot"></span>Accepted</span></td>
```

The shell already defines `.pill-accepted`, `.pill-proposed`, `.pill-rejected`, `.pill-superseded`, etc. P10 adds no new CSS — it specifies the *detection + placement* contract. **Accessibility.** Label text carries the meaning; colour is supplemental.

---

## P11 — Rationale "Why X" blocks → hover-state cards

**Detect.** A section heading matches `/rationale/i` AND its body contains two-or-more bold-paragraph headers (`**Why X:**` / `**Why not Y:**`) each followed by a bullet list. Common in ADRs that consider multiple alternatives without dedicated H3s per option.

**HTML.** Each bold paragraph becomes a card heading; the following list is the card body. Cards stack in a single-column grid (one per row) so each option gets full line-length for its bullets, but pick up an indigo border on hover and a directional chevron in the title — `✓` for `Why X`, `✗` for `Why not Y`.

```html
<div class="p-why-grid">
  <div class="p-why-card p-why-pro">
    <h3><span class="p-why-chev">✓</span>Why Rails</h3>
    <ul><li>…</li></ul>
  </div>
  <div class="p-why-card p-why-con">
    <h3><span class="p-why-chev">✗</span>Why not a separate frontend</h3>
    <ul><li>…</li></ul>
  </div>
</div>
```

**CSS.**

```css
.p-why-grid { display: grid; grid-template-columns: 1fr; gap: 14px; margin: 20px 0; }
.p-why-card { background: var(--surface); border: 1px solid var(--rule); border-radius: 10px; padding: 18px 22px; transition: border-color 0.15s; }
.p-why-card:hover { border-color: var(--accent); }
.p-why-card h3 { margin: 0 0 14px; font-size: 16px; font-weight: 700; display: flex; align-items: center; gap: 10px; color: var(--fg); }
.p-why-chev { font-size: 18px; line-height: 1; font-weight: 700; }
.p-why-pro .p-why-chev { color: var(--ok); }
.p-why-con .p-why-chev { color: var(--warn); }
.p-why-card ul { margin: 0; padding: 0; list-style: none; }
.p-why-card li { position: relative; padding: 6px 0 6px 20px; font-size: 15px; color: var(--fg-soft); line-height: 1.6; }
.p-why-card li::before { content: ""; position: absolute; left: 4px; top: 15px; width: 5px; height: 5px; border-radius: 50%; background: var(--muted); }
```

**Precedence.** P11 ranks below P1 (Alternatives). When both could match (`Rationale` section whose options also have `Pros:`/`Cons:`), P1's side-by-side card grid is the stronger treatment.

**Accessibility.** `<h3>` keeps headings in the document outline; lists keep list semantics; chevron is a real text node (not pseudo-content) so screen readers announce it.

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
.p-rubric { background: var(--surface); border: 1px solid var(--rule); border-left: 4px solid var(--accent); border-radius: 10px; padding: 18px 22px; margin: 20px 0; transition: border-color 0.15s; }
.p-rubric:hover { border-color: var(--accent); }
.p-rubric h3 { margin: 0 0 10px; display: flex; gap: 12px; align-items: baseline; font-size: 17px; font-weight: 700; color: var(--fg); }
.p-rubric-id { font-family: ui-monospace, SFMono-Regular, monospace; font-size: 13px; padding: 4px 9px; background: var(--accent); color: white; border-radius: 4px; letter-spacing: 0.02em; font-weight: 700; }
.p-rubric h4 { font: 700 12px/1 "Inter", ui-sans-serif, sans-serif; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin: 16px 0 6px; }
.p-rubric-formula { background: var(--accent-soft); border-left: 3px solid var(--accent); padding: 12px 16px; margin: 12px 0; font-family: ui-monospace, SFMono-Regular, monospace; font-size: 14px; line-height: 1.55; border-radius: 0 6px 6px 0; color: var(--fg); }
.p-rubric p { margin: 0 0 10px; font-size: 15px; line-height: 1.6; color: var(--fg-soft); }
```

**Why a dedicated pattern.** Plain-prose rendering of a 6-card ADR section (C1–C6 with Reasoning / Alternative / Revision trigger each) produces a wall of repeating H3+H4 that the reader has to mentally segment. The card boundary plus the identifier pill makes "which constant am I reading" answerable at a glance.

**Accessibility.** Heading levels (`<h3>` outer, `<h4>` inner) preserve the document outline; the card boundary is decorative.

---

## P13 — Summary strip → top-of-doc KPI cells

**Detect.** The first content block after the doc header is a short bullet list or definition list of 3–6 key:value pairs where keys are short labels (`Effort`, `Surfaces touched`, `New tables`, `Feature flag`, `Owner`, `Decision deadline`, `Cost`, `Status`) and values are short atomic phrases (a duration, a count, a flag name, a date, a dollar figure). Also matches when the source uses a YAML-frontmatter-style block under a `## Summary` or `## At a glance` heading. **Does not apply** when the same shape appears mid-doc — only the first such block lifts into the summary strip; subsequent ones render as ordinary `<dl>`s.

**HTML.** Lifts into a 4-up grid directly under the doc head (above the first `<section>`):

```html
<div class="p-summary">
  <div class="p-summary-cell"><div class="p-summary-k">Effort</div><div class="p-summary-v p-summary-v-accent">~2 weeks</div></div>
  <div class="p-summary-cell"><div class="p-summary-k">Surfaces touched</div><div class="p-summary-v">3 packages</div></div>
  <div class="p-summary-cell"><div class="p-summary-k">New tables</div><div class="p-summary-v">2</div></div>
  <div class="p-summary-cell"><div class="p-summary-k">Feature flag</div><div class="p-summary-v">task_comments_v1</div></div>
</div>
```

The first cell's value gets `p-summary-v-accent` when it carries the headline number (effort, cost, deadline) — at most one per strip. Strip auto-collapses to 2-up at narrow widths.

**CSS.**

```css
.p-summary { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin: 0 0 32px; }
.p-summary-cell { background: var(--surface); border: 1px solid var(--rule); border-radius: 10px; padding: 16px 18px; }
.p-summary-k { font: 700 11px/1 "Inter", ui-sans-serif, sans-serif; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); margin-bottom: 8px; }
.p-summary-v { font-size: 17px; font-weight: 600; color: var(--fg); line-height: 1.3; }
.p-summary-v-accent { color: var(--accent); }
@media (max-width: 720px) { .p-summary { grid-template-columns: repeat(2, 1fr); } }
```

**Accessibility.** Each cell is plain text; label and value are independent text nodes. **Why a dedicated pattern.** A plan or design doc that opens with "this will take two weeks, touch three packages, and ship behind `task_comments_v1`" gives every subsequent reader an anchor for "is this proportionate?" before they hit the first detail.

---

## P14 — Data flow / architecture → inline SVG diagram

**Detect.** A section heading matches `/data flow|architecture|sequence|system( context)?|fan[- ]?out|pipeline/i` AND its body contains EITHER (a) a fenced code block tagged ` ```svg ` containing literal `<svg>` markup, OR (b) a markdown description of nodes-and-edges that the agent has already converted to SVG during conversion. The skill **does not** auto-generate SVG from prose — agents author the SVG explicitly when they identify a diagram-worthy concept.

**HTML.** The SVG is wrapped in a framed panel with a caption beneath. Solid lines and dashed lines carry semantic meaning by convention; the caption explains the convention used.

```html
<div class="p-diagram">
  <svg viewBox="0 0 860 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Comment write path and realtime fan-out">
    <defs>
      <marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10z" fill="currentColor"/>
      </marker>
      <marker id="arr-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
        <path d="M0,0 L10,5 L0,10z" fill="var(--accent)"/>
      </marker>
    </defs>
    <!-- Node template -->
    <g class="p-node">
      <rect x="20" y="20" width="180" height="54" rx="10"/>
      <text x="110" y="43" text-anchor="middle" class="p-node-title">&lt;Composer&gt;</text>
      <text x="110" y="60" text-anchor="middle" class="p-node-sub">apps/web</text>
    </g>
    <!-- Edges: stroke="currentColor" = solid request path; class="p-edge-async" = dashed realtime path -->
    <path d="M110 74 L110 150" marker-end="url(#arr)" class="p-edge"/>
    <path d="M520 177 L660 177" marker-end="url(#arr-accent)" class="p-edge-async"/>
    <!-- Edge label -->
    <text x="240" y="170" class="p-edge-label">mutate</text>
  </svg>
  <p class="p-diagram-caption">Solid = request/response. Dashed = realtime fan-out. The composer never waits on the dashed path.</p>
</div>
```

**CSS.**

```css
.p-diagram { background: var(--surface); border: 1px solid var(--rule); border-radius: 12px; padding: 24px; margin: 20px 0; overflow-x: auto; }
.p-diagram svg { display: block; min-width: 100%; max-width: 100%; height: auto; color: var(--muted); }
.p-diagram .p-node rect { fill: var(--bg); stroke: var(--rule); stroke-width: 1.5; }
.p-diagram .p-node-title { font: 600 12px ui-sans-serif, system-ui, sans-serif; fill: var(--fg); }
.p-diagram .p-node-sub { font: 10.5px ui-monospace, monospace; fill: var(--muted); }
.p-diagram .p-edge { stroke: currentColor; stroke-width: 1.5; fill: none; }
.p-diagram .p-edge-async { stroke: var(--accent); stroke-width: 1.5; fill: none; stroke-dasharray: 5 4; }
.p-diagram .p-edge-label { font: 10.5px ui-monospace, monospace; fill: var(--muted); }
.p-diagram-caption { font-size: 13.5px; color: var(--muted); margin: 12px 0 0; line-height: 1.55; }
```

**Authoring guidance for the agent.** Use the four node-classes (`p-node` for default, `p-node p-node-emphasis` for the persistence layer or any single "focus" box — fills with `var(--fg)` background and `var(--bg)` text). Limit to ~7 nodes and ~10 edges; if the diagram needs more, split it. Edge labels must be ≤ 24 chars; longer explanations go in the caption.

**Accessibility.** `<svg role="img" aria-label="…">` provides a short description; the caption beneath provides the long description. Text inside the SVG is selectable. **No remote fonts** — the SVG inherits the page font stack.

---

## P15 — Mockup frame → labelled UI sketch

**Detect.** Section heading matches `/mockup|wireframe|sketch|prototype/i` AND body contains 1–3 sub-blocks separated by H3s or bold paragraph headers that look like artefact labels (`A · Thread inside a task card`, `Variant 1`, `Empty state`). Mockup contents can be either (a) inline HTML the agent has authored to approximate the UI, or (b) an inline SVG sketch.

**HTML.** Each mockup is a framed card with a small label bar and a body area. Two-up grid by default; collapses to single column at narrow widths.

```html
<div class="p-mocks">
  <figure class="p-mock">
    <figcaption class="p-mock-label">A · Thread inside a task card</figcaption>
    <div class="p-mock-body">
      <!-- agent-authored UI sketch goes here -->
    </div>
  </figure>
  <figure class="p-mock">
    <figcaption class="p-mock-label">B · Sidebar unread digest</figcaption>
    <div class="p-mock-body"> … </div>
  </figure>
</div>
```

**CSS.**

```css
.p-mocks { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px; margin: 20px 0; }
.p-mock { margin: 0; background: var(--surface); border: 1px solid var(--rule); border-radius: 12px; overflow: hidden; }
.p-mock-label { padding: 10px 16px; border-bottom: 1px solid var(--rule); background: var(--rule-soft); font: 700 12px/1 "Inter", ui-sans-serif, sans-serif; letter-spacing: 0.06em; text-transform: uppercase; color: var(--muted); }
.p-mock-body { padding: 20px; background: var(--bg); }
```

**Authoring guidance.** Mockups are deliberately sketchy — they exist to align reviewers on layout, not to look pixel-final. Real UI primitives the agent can lean on: rounded `<div>`s for cards, small circular `<div>`s for avatars (initials inside), dashed-border divs for "image goes here," `<input disabled>` for form fields. The aim is "we agree on the shape," not "this is the final design."

**Accessibility.** `<figure>` + `<figcaption>` keeps the label tied to the mockup for screen readers. Mockup bodies should be ARIA-`role="presentation"` if they contain non-functional interactive-looking elements (a `<button>` that doesn't do anything is worse than a styled `<div>`).

---

## P16 — Code panel → file-labelled dark block

**Detect.** Any fenced code block that has BOTH (a) an info string naming the language AND (b) a preceding line or paragraph that names a file path (`apps/web/hooks/useAddComment.ts`, `packages/db/migrations/0042_comments.sql`). The file path is detected as a relative-path-looking token containing at least one `/` and ending in a recognised extension. Plain fenced blocks without a file label fall through to the shell's default `<pre>` styling. The P6 two-column diff treatment takes precedence when both apply.

**HTML.**

```html
<figure class="p-code">
  <figcaption class="p-code-file">apps/web/hooks/useAddComment.ts</figcaption>
  <pre class="p-code-body"><code class="language-ts">…</code></pre>
</figure>
```

When two or more code panels appear in the same section back-to-back, they render in a 2-up grid so reviewers can scan them in parallel (e.g. migration + hook):

```html
<div class="p-code-grid">
  <figure class="p-code"> … </figure>
  <figure class="p-code"> … </figure>
</div>
```

**CSS.**

```css
.p-code { margin: 16px 0; display: flex; flex-direction: column; }
.p-code-file { font: 12px ui-monospace, SFMono-Regular, monospace; color: var(--muted); margin-bottom: 8px; }
.p-code-body { background: var(--fg); color: #e8e6de; border-radius: 12px; padding: 18px 20px; overflow-x: auto; margin: 0; }
.p-code-body code { font: 12.5px/1.65 ui-monospace, SFMono-Regular, monospace; color: inherit; background: transparent; padding: 0; }
.p-code-body .tok-kw  { color: var(--accent); }
.p-code-body .tok-str { color: var(--ok); }
.p-code-body .tok-cm  { color: var(--muted); font-style: italic; }
.p-code-body .tok-fn  { color: #c9b98a; }
.p-code-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 16px 0; }
@media (max-width: 900px) { .p-code-grid { grid-template-columns: 1fr; } }
```

**Token wrapping.** The agent applies four span classes inline (`tok-kw` for keywords, `tok-str` for string literals, `tok-cm` for comments, `tok-fn` for function/identifier names). Don't attempt full lexer-grade highlighting — the four tokens are enough to give the panel hierarchy without misleading the reader. If the agent isn't confident about a token, leave it un-spanned (the default body colour reads cleanly).

**Accessibility.** `<figure>` + `<figcaption>` ties the file path to the code. Dark background + light text passes AA at 14.5:1 (`#e8e6de` on `var(--fg)` `#0a0a0f`).

---

## P17 — Risks & mitigations → severity-tagged table

**Detect.** Section heading matches `/risks?( ?(and|&) ?mitigations?)?|threats?|failure modes?/i` AND body is a markdown table with at least these columns (case-insensitive, partial match OK): `Risk` (or `Description`), `Severity` (or `Sev` / `Likelihood`), `Mitigation` (or `Response`). An optional `Owner` column is preserved. Severity values are matched against `high|med(ium)?|low|critical` (case-insensitive).

**HTML.** Three- or four-column grid (not a real `<table>`, because we want the severity cell to be a chip in a narrow centred column). Borders form the visual table.

```html
<div class="p-risks">
  <div class="p-risks-row p-risks-head">
    <div>Risk</div><div>Sev</div><div>Mitigation</div>
  </div>
  <div class="p-risks-row">
    <div>Realtime duplicate: socket append races with HTTP response.</div>
    <div><span class="p-sev p-sev-high">HIGH</span></div>
    <div>Dedupe on server-assigned <code>id</code>; temp rows filtered on reconcile.</div>
  </div>
  <!-- repeat rows -->
</div>
```

**CSS.**

```css
.p-risks { border: 1px solid var(--rule); border-radius: 12px; overflow: hidden; background: var(--surface); margin: 20px 0; }
.p-risks-row { display: grid; grid-template-columns: 1.6fr 80px 1.6fr; }
.p-risks-row + .p-risks-row { border-top: 1px solid var(--rule); }
.p-risks-row > div { padding: 14px 18px; font-size: 14px; line-height: 1.55; color: var(--fg-soft); }
.p-risks-row > div + div { border-left: 1px solid var(--rule); }
.p-risks-head > div { background: var(--rule-soft); color: var(--fg); font: 700 12px/1 "Inter", ui-sans-serif, sans-serif; letter-spacing: 0.05em; text-transform: uppercase; padding: 12px 18px; }
.p-sev { display: inline-block; font: 700 11px/1 ui-monospace, monospace; padding: 4px 9px; border-radius: 6px; letter-spacing: 0.04em; }
.p-sev-high     { background: var(--danger-soft); color: var(--danger); }
.p-sev-critical { background: var(--danger);      color: white; }
.p-sev-med      { background: var(--warn-soft);   color: var(--warn); }
.p-sev-low      { background: var(--ok-soft);     color: var(--ok); }
@media (max-width: 720px) {
  .p-risks-row { grid-template-columns: 1fr; }
  .p-risks-row > div + div { border-left: none; border-top: 1px dashed var(--rule); }
  .p-risks-head { display: none; }
}
```

**Optional owner column.** When the source table has an Owner column, switch the grid to `1.5fr 80px 1.5fr 120px` and add a fourth `<div>` per row. Owner renders as plain text or a `pill pill-meta` if it looks like a handle (`@anton`).

**Accessibility.** Severity label text (`HIGH` / `MED` / `LOW`) carries the meaning; colour is supplemental. The grid uses `<div>`s rather than `<table>` because the severity column is intentionally narrow and centre-aligned — a real table here forces awkward column-width compromises. Screen readers still announce each row's content in order; for users who require table semantics, the source markdown table is the canonical form.

---

## P18 — Segment-mix horizontal stack bar

**Detect.** Section H2 matches `/business architecture|segment mix|revenue mix/i` AND the section contains a markdown table whose first column header matches `Segment` (case-insensitive) and second column header contains `%`, `share`, or `mix`. Pattern fires on the table; the bar inserts immediately before it, and the table renders below as the canonical legend.

**HTML.** Parse each data row's second-column value (format `~XX%` or `XX%`); normalise all shares to sum to exactly 100%. Render a flex-row container where each segment is a coloured `<div>` with inline `style="width:N%"`. Include a `<span class="p-seg-bar-lbl">` only on segments with normalised share ≥8% (first significant word of the segment name). Wrap in a `<div role="img" aria-label="Segment mix: [name] N%, …">`. Six colour slots `.p-seg-s0`–`.p-seg-s5` cycle through the shell's primary tokens; use the first N slots for N segments.

```html
<div class="p-seg-bar-fig" role="img" aria-label="Segment mix: EUV systems 50%, Advanced DUV 25%, Mature DUV 10%, Installed Base Management 15%">
  <div class="p-seg-bar">
    <div class="p-seg-s0" style="width:50%" title="EUV systems ~50%">
      <span class="p-seg-bar-lbl">EUV</span>
    </div>
    <div class="p-seg-s1" style="width:25%" title="Advanced DUV ~25%">
      <span class="p-seg-bar-lbl">Adv DUV</span>
    </div>
    <div class="p-seg-s2" style="width:10%" title="Mature DUV ~10%">
      <span class="p-seg-bar-lbl">Mature</span>
    </div>
    <div class="p-seg-s3" style="width:15%" title="Installed Base Management ~15%">
      <span class="p-seg-bar-lbl">IBM</span>
    </div>
  </div>
</div>
<!-- source table renders immediately below as canonical legend -->
```

**CSS.**

```css
.p-seg-bar-fig { margin: 0.5rem 0 0.25rem; }
.p-seg-bar { display: flex; height: 36px; border-radius: 4px; overflow: hidden; gap: 1px; background: var(--rule); }
.p-seg-s0 { background: var(--accent);  flex-shrink: 0; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.p-seg-s1 { background: var(--info);    flex-shrink: 0; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.p-seg-s2 { background: var(--warn);    flex-shrink: 0; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.p-seg-s3 { background: var(--ok);      flex-shrink: 0; display: flex; align-items: center; justify-content: center; overflow: hidden; }
.p-seg-s4 { background: var(--danger);  flex-shrink: 0; overflow: hidden; }
.p-seg-s5 { background: var(--muted);   flex-shrink: 0; overflow: hidden; }
.p-seg-bar-lbl { color: white; font-size: 0.68rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding: 0 6px; }
```

**Accessibility.** The `role="img" aria-label` on the wrapper div provides a text summary for screen readers; segment divs are presentational. The source table that follows is the canonical data record.

**When to use.** Playbook §1 "Business Architecture" segment-mix tables. Fires on the first `Segment`-headed table in the section. Does not fire on tables whose second column is growth rate, margin, or another non-share metric.

---

## P20 — Catalyst probability × IV-impact mini-bars

**Detect.** Section H2 matches `/catalysts?/i` AND the section contains a markdown table with headers matching `Catalyst`, `Probability`, and `IV impact` (case-insensitive, partial match on each header).

**HTML.** Render the standard 4-column table augmented with inline mini-bar `<div>`s below the text value in two cells per row. Probability bar: `width = parsed_probability_percent%` (e.g., `~35%` → `width:35%`). IV-impact bar: `width = min(midpoint_of_range, 30) / 30 × 100%` — midpoint is the average of the two endpoint values in a range like `−10–20%` (using absolute values, e.g. midpoint = 15); a 30%-absolute range fills the bar fully. IV bar class: `p-cat-bar-pos` if range starts with `+`; `p-cat-bar-neg` if it starts with `−` or `-`. Direction cell becomes a pill: text containing `positive` → `.p-cat-dir-pos`; `negative` → `.p-cat-dir-neg`; `mixed`, `neutral`, or `modest` → `.p-cat-dir-mixed`.

```html
<table class="p-cat-table">
  <thead>
    <tr><th>Catalyst</th><th>Probability</th><th>IV impact</th><th>Direction</th></tr>
  </thead>
  <tbody>
    <tr>
      <td>DOJ Search remedies finalised (default-payment restrictions, Chrome leverage…)</td>
      <td>~35% by end-2027
        <div class="p-cat-bar-track"><div class="p-cat-bar-fill p-cat-bar-prob" style="width:35%"></div></div>
      </td>
      <td>−10–20%
        <div class="p-cat-bar-track"><div class="p-cat-bar-fill p-cat-bar-neg" style="width:50%"></div></div>
      </td>
      <td><span class="p-cat-dir p-cat-dir-neg">Strongly negative</span></td>
    </tr>
    <tr>
      <td>GCP margin print sustains above 15% for 2+ consecutive quarters</td>
      <td>~55% by end-2027
        <div class="p-cat-bar-track"><div class="p-cat-bar-fill p-cat-bar-prob" style="width:55%"></div></div>
      </td>
      <td>+5–8%
        <div class="p-cat-bar-track"><div class="p-cat-bar-fill p-cat-bar-pos" style="width:22%"></div></div>
      </td>
      <td><span class="p-cat-dir p-cat-dir-pos">Positive</span></td>
    </tr>
  </tbody>
</table>
```

**CSS.**

```css
.p-cat-table { width: 100%; border-collapse: collapse; font-size: 0.875rem; }
.p-cat-table th, .p-cat-table td { padding: 0.5rem 0.65rem; border-bottom: 1px solid var(--rule); vertical-align: top; }
.p-cat-table th { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); font-weight: 600; border-bottom: 2px solid var(--rule); white-space: nowrap; }
.p-cat-bar-track { height: 4px; background: var(--rule); border-radius: 2px; margin-top: 5px; overflow: hidden; }
.p-cat-bar-fill  { height: 100%; border-radius: 2px; }
.p-cat-bar-prob  { background: var(--accent); }
.p-cat-bar-pos   { background: var(--ok); }
.p-cat-bar-neg   { background: var(--danger); }
.p-cat-bar-mixed { background: var(--warn); }
.p-cat-dir { display: inline-block; padding: 0.15rem 0.5rem; border-radius: 4px; font-size: 0.75rem; font-weight: 600; }
.p-cat-dir-pos   { background: var(--ok-soft);    color: var(--ok); }
.p-cat-dir-neg   { background: var(--danger-soft); color: var(--danger); }
.p-cat-dir-mixed { background: var(--warn-soft);   color: var(--warn); }
```

**Accessibility.** Table semantic structure (`<table>/<thead>/<tbody>`) is preserved. Mini-bar `<div>`s are presentational; the text value in each cell already carries the numeric content. Direction pills are text spans; colour is supplemental.

**When to use.** Playbook §3 "Active Catalysts" tables with the `Catalyst | Probability | IV impact | Direction` header shape. Does not fire on catalyst sections with a different table structure; those fall through to standard prose table rendering.

---

## P21 — Sell-side disagreement axes → bull/bear/NVS cards

**Detect.** Section H2 matches `/sell[- ]side disagreement|disagreement axes/i` AND the section body contains at least one H3 followed by both a `**Bull:**` and a `**Bear:**` marker (case-insensitive) within that H3's scope.

**HTML.** Any introductory paragraph before the first axis H3 renders as plain prose. Each H3 becomes a `.p-axis-card`. The card header carries the axis title and the `**The question:**` paragraph (with the `**The question:**` bold prefix stripped). The card body has a two-column grid for Bull and Bear views, and a full-width Noise-vs-Structural strip if present. The list-item prefixes `- **Bull:**`, `- **Bear:**`, and `- **Noise vs. structural:**` are stripped; their inline content fills the respective blocks.

```html
<p>The real arguments the sell-side is having…</p>

<div class="p-axis-card">
  <div class="p-axis-head">
    <h3 id="axis-1">1. Capex-cycle trough timing</h3>
    <p class="p-axis-q">Does the capex cycle trough in H2 2026…</p>
  </div>
  <div class="p-axis-body">
    <div class="p-axis-views">
      <div class="p-axis-bull">
        <div class="p-axis-view-label">Bull</div>
        TSMC has sustained its 2025 and 2026 capex guidance…
      </div>
      <div class="p-axis-bear">
        <div class="p-axis-view-label">Bear</div>
        Memory oversupply is slower-than-consensus…
      </div>
    </div>
    <div class="p-axis-nvs">
      <div class="p-axis-nvs-label">Noise vs. Structural</div>
      A single quarter of order intake recovery is noise…
    </div>
  </div>
</div>
<!-- one .p-axis-card per H3 axis -->
```

Omit `.p-axis-nvs` if the H3 has no `**Noise vs. structural:**` block. H3 anchors use the same slug rules as Step 3 of the render-html workflow.

**CSS.**

```css
.p-axis-card { border: 1px solid var(--rule); border-radius: 8px; margin: 1.25rem 0; overflow: hidden; }
.p-axis-head { padding: 0.8rem 1rem; background: var(--surface); border-bottom: 1px solid var(--rule); }
.p-axis-head h3 { margin: 0; font-size: 1rem; scroll-margin-top: 1.5rem; }
.p-axis-q { font-size: 0.85rem; color: var(--muted); font-style: italic; margin: 0.25rem 0 0; }
.p-axis-body { padding: 1rem; }
.p-axis-views { display: grid; grid-template-columns: 1fr 1fr; gap: 0.65rem; margin-bottom: 0.65rem; }
.p-axis-bull, .p-axis-bear { border-radius: 6px; padding: 0.75rem; font-size: 0.84rem; line-height: 1.6; }
.p-axis-bull { background: var(--ok-soft); border: 1px solid var(--ok); }
.p-axis-bear { background: var(--danger-soft); border: 1px solid var(--danger); }
.p-axis-view-label { font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; margin-bottom: 0.35rem; }
.p-axis-bull .p-axis-view-label { color: var(--ok); }
.p-axis-bear .p-axis-view-label { color: var(--danger); }
.p-axis-nvs { background: var(--rule-soft); border: 1px solid var(--rule); border-radius: 6px; padding: 0.75rem; font-size: 0.84rem; line-height: 1.6; }
.p-axis-nvs-label { font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; color: var(--muted); margin-bottom: 0.3rem; }
@media (max-width: 720px) { .p-axis-views { grid-template-columns: 1fr; } }
```

**Accessibility.** Each card contains a unique `<h3>` that remains in the TOC navigation. The view labels (`Bull` / `Bear`) carry meaning as text, not colour alone. The NVS strip's purpose is stated in its label text.

**When to use.** Playbook §4 "Sell-Side Disagreement Axes" sections with 2–8 numbered or lettered axes, each having a question, bull view, bear view, and optional NVS falsifiability criterion. ASML §4 and GOOG §4 are the canonical cases. Do not apply to generic sections that happen to mention "bull" or "bear" inline — the H3-level structure with explicit `**Bull:**` / `**Bear:**` markers is the required signal.

---

## P22 — Failure-mode bullets → layer-tagged cards

**Detect.** Section H2 matches `/failure modes?/i` AND the section body is a bullet list where ≥50% of items end with a `[xxx layer]` tag (regex `\[[\w ]+layer\]` at the end of the trimmed item text). P17 takes precedence when the failure-modes content is a markdown table rather than a bullet list.

**HTML.** Any intro paragraph renders as prose above the list. Each bullet item becomes a `.p-fm-card`. The `[xxx layer]` suffix is extracted from the item text, lowercased, and " layer" is stripped to produce the tag slug (e.g. `[demand layer]` → `demand`, `[FX layer]` → `fx`). The slug drives the CSS modifier class and the chip label text. The `[xxx layer]` suffix is removed from the rendered card body. Unknown slugs fall back to `.p-fm-tag-other`. Bullets without a `[xxx layer]` tag render as plain `<li>` items inside a `<ul>` fallback.

```html
<p>These are the thesis-breaking scenarios that the DCF does not capture…</p>
<div class="p-fm-list">
  <div class="p-fm-card">
    <span class="p-fm-tag p-fm-tag-demand" aria-label="demand layer">demand</span>
    <strong>Customer concentration shock:</strong> TSMC + Samsung + Intel represent the dominant share…
  </div>
  <div class="p-fm-card">
    <span class="p-fm-tag p-fm-tag-regulatory" aria-label="regulatory layer">regulatory</span>
    <strong>China service/spare-parts export controls:</strong> Current restrictions primarily cover new EUV…
  </div>
  <!-- one .p-fm-card per tagged bullet -->
</div>
```

**CSS.**

```css
.p-fm-list { display: flex; flex-direction: column; gap: 0.6rem; margin-top: 0.75rem; }
.p-fm-card { border: 1px solid var(--rule); border-radius: 6px; padding: 0.7rem 0.9rem 0.7rem 3.75rem; font-size: 0.88rem; line-height: 1.6; position: relative; }
.p-fm-tag { position: absolute; left: 0.65rem; top: 0.7rem; font-size: 0.58rem; text-transform: uppercase; font-weight: 700; padding: 0.15rem 0.45rem; border-radius: 4px; white-space: nowrap; }
.p-fm-tag-demand       { background: var(--danger-soft); color: var(--danger); }
.p-fm-tag-interface    { background: var(--danger-soft); color: var(--danger); }
.p-fm-tag-regulatory   { background: var(--warn-soft);   color: var(--warn); }
.p-fm-tag-monetisation { background: var(--warn-soft);   color: var(--warn); }
.p-fm-tag-technology   { background: var(--accent-soft); color: var(--accent); }
.p-fm-tag-cost         { background: var(--accent-soft); color: var(--accent); }
.p-fm-tag-ecosystem    { background: var(--info-soft);   color: var(--info); }
.p-fm-tag-fx           { background: var(--info-soft);   color: var(--info); }
.p-fm-tag-accounting   { background: var(--rule-soft);   color: var(--muted); }
.p-fm-tag-other        { background: var(--rule-soft);   color: var(--muted); }
```

**Accessibility.** Each chip carries `aria-label="[slug] layer"` so screen readers announce the category before the body text. Layer distinctions are conveyed by both the text label and colour.

**When to use.** Playbook §5 "Failure Modes" sections where bullets are tagged with `[xxx layer]` per the playbook convention. Do not apply to untagged bullet lists (fall through to prose) or table-format risk registers (P17 handles those).

---

## P24 — Historical reset-and-recover scatter

**Detect.** Section H2 matches `/historical reset|reset[- ]and[- ]recover|recovery prior/i` AND the section contains a markdown table with headers matching `Episode`, `Drawdown`, and `Recovery` (case-insensitive, partial match).

**HTML.** Inline SVG scatter (`viewBox="0 0 500 260"`) rendered immediately before the source table. Plot area: x ∈ [55, 470], y ∈ [20, 220] (width 415, height 200). X-axis: recovery months, default max 18 (extend to `maxMonths + 2` if any value exceeds 16). Y-axis: drawdown magnitude %, default max 50 (extend to `maxPct + 5` if any value exceeds 45). Coordinate formulas: `cx = 55 + months / maxMonths × 415`; `cy = 220 − pct / maxPct × 200`. Parse drawdown from `~−XX%` or `~−XX–YY%` (midpoint of range). Parse recovery months from `~N months` or `~N–M months` (midpoint). Dot colour: drawdown ≤ 20% → `.p-sc-warn`; > 20% → `.p-sc-danger`. Episodes with non-numeric recovery (e.g. "Partial", "Ongoing") render as hollow circles at `cx = 478` with class `.p-sc-partial`. Each circle has a `<title>` child naming the episode. The `<figure aria-label>` summarises all plotted episodes; the SVG is `aria-hidden="true"`.

```html
<figure class="p-sc-fig" aria-label="Reset-and-recover: 2022 ad recession −45% recovered 12 months; 2023 Bing scare −15% recovered 6 months; 2024 DOJ partial recovery not plotted">
  <svg class="p-sc-svg" viewBox="0 0 500 260" role="img" aria-hidden="true">
    <!-- horizontal grid lines at 10/20/30/40% drawdown levels -->
    <line x1="55" y1="180" x2="470" y2="180" class="p-sc-grid"/>
    <line x1="55" y1="140" x2="470" y2="140" class="p-sc-grid"/>
    <line x1="55" y1="100" x2="470" y2="100" class="p-sc-grid"/>
    <line x1="55" y1="60"  x2="470" y2="60"  class="p-sc-grid"/>
    <!-- axes -->
    <line x1="55" y1="20"  x2="55"  y2="220" class="p-sc-axis"/>
    <line x1="55" y1="220" x2="470" y2="220" class="p-sc-axis"/>
    <!-- Y axis labels (drawdown %) -->
    <text x="50" y="221" class="p-sc-lbl" text-anchor="end">0</text>
    <text x="50" y="181" class="p-sc-lbl" text-anchor="end">10</text>
    <text x="50" y="141" class="p-sc-lbl" text-anchor="end">20</text>
    <text x="50" y="101" class="p-sc-lbl" text-anchor="end">30</text>
    <text x="50" y="61"  class="p-sc-lbl" text-anchor="end">40</text>
    <text x="50" y="24"  class="p-sc-lbl" text-anchor="end">50%</text>
    <!-- X axis labels (months) -->
    <text x="55"  y="237" class="p-sc-lbl" text-anchor="middle">0</text>
    <text x="193" y="237" class="p-sc-lbl" text-anchor="middle">6</text>
    <text x="332" y="237" class="p-sc-lbl" text-anchor="middle">12</text>
    <text x="470" y="237" class="p-sc-lbl" text-anchor="middle">18 mo</text>
    <!-- axis titles -->
    <text x="262" y="254" class="p-sc-lbl" text-anchor="middle">Recovery (months)</text>
    <text x="14"  y="120" class="p-sc-lbl" text-anchor="middle" transform="rotate(-90 14 120)">Drawdown</text>
    <!-- data points (cx/cy from formulas above; example uses GOOG data) -->
    <circle cx="332" cy="40"  r="7" class="p-sc-danger"><title>2022 ad recession: −45%, ~12 months</title></circle>
    <circle cx="193" cy="160" r="7" class="p-sc-warn"><title>2023 Bing scare: −15%, ~6 months</title></circle>
    <!-- partial recovery: hollow circle beyond right axis edge -->
    <circle cx="478" cy="132" r="7" class="p-sc-partial"><title>2024–25 DOJ: ~−22%, partial recovery</title></circle>
  </svg>
  <p class="p-sc-note">† Open circles beyond axis edge = recovery not yet complete. Source table below is the canonical record.</p>
</figure>
```

**CSS.**

```css
.p-sc-fig { margin: 0.75rem 0 0; }
.p-sc-svg { width: 100%; max-width: 500px; height: auto; display: block; }
.p-sc-axis { stroke: var(--fg); stroke-width: 1.5; }
.p-sc-grid { stroke: var(--rule); stroke-width: 1; stroke-dasharray: 3 3; }
.p-sc-lbl    { fill: var(--muted); font-size: 11px; }
.p-sc-danger { fill: var(--danger); opacity: 0.8; }
.p-sc-warn   { fill: var(--warn);   opacity: 0.8; }
.p-sc-partial { fill: none; stroke: var(--muted); stroke-width: 2; stroke-dasharray: 3 2; }
.p-sc-note { font-size: 0.75rem; color: var(--muted); margin: 0.3rem 0 0; }
```

**Accessibility.** The `<figure aria-label>` summarises all episodes; the SVG is `aria-hidden="true"`. Each `<circle>` has a `<title>` child for hover tooltips. The source table that follows is the canonical record.

**When to use.** Playbook §7 "Historical Reset-and-Recover Priors" tables with `Episode | Drawdown | … | Recovery | …` headers. Does not fire without a parseable drawdown column.

---

## Fallback

A section that matches no pattern renders with the shell's section-header treatment (`<section class="s"><header><span class="ix">NN</span><h2>…</h2></header>`) and the shell's prose defaults (`<p>`, `<ul>`, `<table>`, `<pre>`, `<blockquote>`). The fallback is "well-typeset doc," not raw HTML — false-positive pattern matches degrade review trust faster than missing treatments.

## Adding a new pattern

When a new pattern earns its slot:

1. Add a section here following the same six-part structure: heading, **Detect**, **HTML**, **CSS**, **Accessibility**, brief rationale.
2. Number it sequentially (`P13 — …`) so cross-references stay stable.
3. Confirm the CSS uses shell colour tokens (`--accent`, `--ok`, `--warn`, `--info`, `--danger`, `-soft` variants) — no ad-hoc hex values.
4. Confirm the CSS only adds new selectors prefixed `p-` — it must not override any rule in `html-skeleton.md`.
5. If the detection signal could overlap an existing pattern, document the precedence rule explicitly. The first-match-wins ordering of this file is the resolution mechanism.
