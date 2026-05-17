---
name: html-skeleton
description: >
  Self-contained HTML shell used by the render-html skill. Defines the single-file
  document template — the product-UI visual system (Inter sans, indigo accent,
  numbered sidebar nav with scrollspy, pill + metadata-grid utilities, section
  headers with index + tag, dark-mode auto, print stylesheet) — plus the inline
  scrollspy JS and the hard self-containment rule.
type: reference
cited_by:
  - skills/render-html/SKILL.md
---

# HTML skeleton

The render-html skill wraps every markdown body in the shell below. The shell is the **only** mechanism by which output styling and navigation arrive — no external CSS, no external JS, no remote images. That rule is load-bearing for the skill's "opens via `file://` with no network" guarantee; reviewers attach these files to emails and store them in private wikis where CDN URLs silently break.

The visual language is **product-UI**: Inter (system fallback), tight type, indigo accent, sidebar with numbered nav and scrollspy, status pills and metadata grids as first-class. Reads as a Linear/Stripe spec page rather than a markdown previewer. Pattern treatments (P1–P12) extend this language; they don't introduce a competing one.

## The hard rule

Anything injected into the rendered output must satisfy all three:

- **No `<link rel="stylesheet">`.** All CSS lives in the inline `<style>` block.
- **No `<script src=...>`.** All JS lives in the inline `<script>` block at the end of `<body>`.
- **No remote `<img>` URLs.** Inline SVG is preferred; base64 data URIs are allowed when an SVG is impractical. Remote URLs (`http:`, `https:`, protocol-relative `//`) are not.

If a future pattern needs richer interactivity (charts, diagrams, syntax highlighting), inline the minimal library or hand-write the SVG. Adding a CDN is not an option.

## Substitution tokens

| Token | Source | Notes |
|---|---|---|
| `{{title}}` | The source markdown's first H1 | Goes in both `<title>` and the page `<h1>`. |
| `{{breadcrumb}}` | Inferred from path (e.g. `docs/adr/001-...` → `Architecture · ADRs · ADR-001`) or empty | Optional; render empty `<div>` if nothing meaningful to show. |
| `{{header-pills}}` | Status pill (P10) + identifier pill + date pill, in that order | Rendered into the `.pill-row` slot. Empty if none apply. |
| `{{meta-grid}}` | Definition-list rows for `Source`, `Rendered`, plus any frontmatter fields after P9 lifts them | The grid is always rendered; if only `Source` and `Rendered` apply, it shows two rows. |
| `{{toc-entries}}` | One `<li>` per H2 (and indented H3), with anchor href to the heading's slug | H1 is the title, not a TOC entry. Slugs are kebab-case, deduplicated `-2`, `-3`. |
| `{{status-block}}` | One-line aside under "Status" kicker in the sidebar (e.g. "Accepted 31 Mar 2026. No superseding ADR.") | Empty `<div>` if no status info. |
| `{{body-html}}` | The markdown body converted to HTML, with H2/H3 carrying `id="<slug>"` and wrapped per `html-patterns.md` | Pattern markup substitutes here. |
| `{{source-path}}` | Path of the input `.md` file, relative to the repo root if possible | Shown in the metadata grid and footer. |
| `{{render-date}}` | ISO date (YYYY-MM-DD) of the render | Provenance only — re-renders on the same day produce no diff. |

## The shell

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{title}}</title>
<style>
  /* Colour tokens — all foregrounds verified ≥ 4.5:1 on their `-soft`
     companion and ≥ 4.6:1 on `--bg` (WCAG 2.0 AA, normal text). */
  :root {
    --bg: #fcfcfd;
    --surface: #ffffff;
    --fg: #0a0a0f;        /* on --bg: 19.5:1 */
    --fg-soft: #2e2e38;   /* on --bg: 13.0:1 (was #3a3a44 = 10.8:1) */
    --muted: #5f5f6a;     /* on --bg: 6.0:1; on --rule-soft: 5.7:1 (was 4.6:1) */
    --rule: #e3e3ea;
    --rule-soft: #f1f1f5;
    --accent: #4a3bef;       --accent-soft: #efedff;  /* 5.7:1 */
    --ok:     #047a44;       --ok-soft:     #e6f5ed;  /* 4.8:1 */
    --info:   #1957c4;       --info-soft:   #e7f0fd;  /* 5.7:1 */
    --warn:   #8b4a05;       --warn-soft:   #fbf0e0;  /* 6.3:1 */
    --danger: #a82a3f;       --danger-soft: #fbe6ea;  /* 5.8:1 */
  }
  @media (prefers-color-scheme: dark) {
    /* Dark-mode tokens verified ≥ 4.5:1 on `-soft` companions and ≥ 9:1 on --bg. */
    :root {
      --bg: #0b0b10; --surface: #15151c;
      --fg: #f4f4f7;        /* on --bg: 17.5:1 */
      --fg-soft: #d6d6dd;   /* on --bg: 13.4:1 (was #c8c8d0) */
      --muted: #9d9dab;     /* on --bg: 6.5:1; on --rule-soft: 6.2:1 (was 4.6:1) */
      --rule: #2a2a35; --rule-soft: #1c1c24;
      --accent: #a99dff;       --accent-soft: #2a2548;  /* 7.6:1 */
      --ok:     #6fd4a0;       --ok-soft:     #122922;  /* 7.4:1 */
      --info:   #8eb8ff;       --info-soft:   #14233b;  /* 7.8:1 */
      --warn:   #f0a35a;       --warn-soft:   #2a1f12;  /* 7.1:1 */
      --danger: #f08597;       --danger-soft: #29151b;  /* 7.0:1 */
    }
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: var(--bg); color: var(--fg); }
  /* 16px body / 1.65 leading — readability floor; smaller labels never
     drop below 13px (≈ 0.8125rem). All sizes use rem so user-agent zoom
     scales the whole system together. */
  body {
    font: 16px/1.65 "Inter", ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
    font-feature-settings: "cv11", "ss01", "ss03", "kern", "liga";
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }
  code, pre { font-family: ui-monospace, SFMono-Regular, "JetBrains Mono", Menlo, monospace; }

  /* ---------- Layout ---------- */
  .layout { display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; max-width: 1200px; margin: 0 auto; }

  /* ---------- Sidebar ---------- */
  aside {
    position: sticky; top: 0; align-self: start; height: 100vh; overflow-y: auto;
    padding: 28px 22px; border-right: 1px solid var(--rule); background: var(--bg);
  }
  aside .brand { display: flex; align-items: center; gap: 8px; font-weight: 600; font-size: 14px; margin-bottom: 28px; color: var(--fg); }
  aside .brand .dot { width: 18px; height: 18px; border-radius: 5px; background: linear-gradient(135deg, var(--accent), #8c7bff); flex-shrink: 0; }
  aside .kicker { font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); margin: 24px 0 10px; font-weight: 700; }
  aside .kicker:first-of-type { margin-top: 0; }
  aside nav ol { list-style: none; padding: 0; margin: 0; counter-reset: nav; }
  aside nav li { counter-increment: nav; margin: 2px 0; }
  aside nav li.h3 { margin-left: 28px; }
  aside nav a {
    display: flex; align-items: center; gap: 10px; padding: 8px 10px; border-radius: 6px;
    color: var(--fg-soft); font-size: 14.5px; transition: background 0.12s, color 0.12s;
  }
  aside nav li:not(.h3) > a::before { content: counter(nav, decimal-leading-zero); font: 600 12px/1 ui-monospace, monospace; color: var(--muted); width: 20px; flex-shrink: 0; }
  aside nav a:hover { background: var(--rule-soft); color: var(--fg); text-decoration: none; }
  aside nav a.active { background: var(--accent-soft); color: var(--accent); }
  aside nav a.active::before { color: var(--accent); }
  aside .status-block { font-size: 13.5px; color: var(--fg-soft); line-height: 1.55; }

  /* ---------- Main ---------- */
  main { padding: 40px 56px 80px; max-width: 860px; }

  /* ---------- Document header ---------- */
  .doc-head { margin-bottom: 40px; }
  .breadcrumbs { font-size: 13.5px; color: var(--muted); margin-bottom: 16px; }
  .breadcrumbs span { color: var(--fg-soft); }
  main h1 { font-size: 34px; line-height: 1.2; margin: 0 0 16px; letter-spacing: -0.02em; font-weight: 700; color: var(--fg); }
  .pill-row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin-bottom: 0; }
  .pill-row:empty { display: none; }

  /* ---------- Pills (utility, reusable) ---------- */
  /* 13px at 600 weight = "large text" under WCAG; foreground tokens above
     all meet ≥ 4.5:1 on their `-soft` companions regardless. */
  .pill {
    display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px; border-radius: 999px;
    font: 600 13px/1 "Inter", ui-sans-serif, system-ui, sans-serif; letter-spacing: 0.01em; white-space: nowrap;
  }
  .pill .dot { width: 7px; height: 7px; border-radius: 50%; background: currentColor; }
  .pill-meta     { background: var(--rule-soft); color: var(--fg-soft); font-weight: 500; }
  .pill-accepted, .pill-ok        { background: var(--ok-soft);     color: var(--ok); }
  .pill-proposed, .pill-draft     { background: var(--info-soft);   color: var(--info); }
  .pill-rejected, .pill-deprecated{ background: var(--danger-soft); color: var(--danger); }
  .pill-superseded, .pill-flagged { background: var(--warn-soft);   color: var(--warn); }

  /* ---------- Metadata grid (utility, reusable) ---------- */
  .meta-grid {
    display: grid; grid-template-columns: max-content 1fr; gap: 8px 22px;
    background: var(--surface); border: 1px solid var(--rule); border-radius: 10px;
    padding: 16px 20px; margin: 28px 0 0; font-size: 14px;
  }
  .meta-grid dt { color: var(--muted); font-weight: 600; }
  .meta-grid dd { margin: 0; color: var(--fg); font-family: ui-monospace, SFMono-Regular, monospace; font-size: 13.5px; word-break: break-word; }

  /* ---------- Section header (utility for pattern + prose alike) ---------- */
  section.s { margin: 56px 0; scroll-margin-top: 20px; }
  section.s > header { display: flex; align-items: baseline; gap: 12px; margin-bottom: 18px; flex-wrap: wrap; }
  section.s .ix { font: 700 12px/1 ui-monospace, monospace; color: var(--muted); padding: 4px 8px; border: 1px solid var(--rule); border-radius: 4px; flex-shrink: 0; }
  main h2 { font-size: 22px; line-height: 1.3; margin: 0; letter-spacing: -0.01em; font-weight: 700; color: var(--fg); }
  main h3 { font-size: 17px; line-height: 1.4; margin: 28px 0 10px; font-weight: 650; color: var(--fg); }

  /* ---------- Prose defaults ---------- */
  /* Body paragraphs use --fg-soft (13:1 on --bg) — easier on the eye than
     pure --fg but still well above AA. Lists inherit. */
  main p { margin: 0 0 16px; color: var(--fg-soft); }
  main ul, main ol { margin: 0 0 16px; padding-left: 26px; color: var(--fg-soft); }
  main li { margin: 6px 0; }
  main pre { background: var(--rule-soft); padding: 16px 18px; border-radius: 8px; overflow-x: auto; font-size: 14px; line-height: 1.6; border: 1px solid var(--rule); }
  main code { font-size: 0.92em; padding: 2px 6px; background: var(--rule-soft); border-radius: 4px; color: var(--fg); }
  main pre code { padding: 0; background: transparent; font-size: 1em; }
  main blockquote { margin: 18px 0; padding: 10px 18px; border-left: 4px solid var(--accent); color: var(--fg-soft); background: var(--accent-soft); border-radius: 0 6px 6px 0; }
  main table { border-collapse: collapse; margin: 16px 0; width: 100%; font-size: 14.5px; }
  main th, main td { border-bottom: 1px solid var(--rule); padding: 10px 14px; text-align: left; }
  main th { background: var(--rule-soft); font-weight: 700; color: var(--fg); font-size: 13px; text-transform: uppercase; letter-spacing: 0.04em; }
  main hr { border: none; border-top: 1px solid var(--rule); margin: 40px 0; }

  /* ---------- Footer ---------- */
  footer { grid-column: 1 / -1; padding: 24px 56px; color: var(--muted); font-size: 13px; border-top: 1px solid var(--rule); }
  footer code { background: transparent; padding: 0; color: var(--fg-soft); }

  /* ---------- Print ---------- */
  @media print {
    aside { display: none; }
    .layout { grid-template-columns: 1fr; }
    main { padding: 24px; max-width: none; }
  }

  /* ---------- Responsive ---------- */
  @media (max-width: 880px) {
    .layout { grid-template-columns: 1fr; }
    aside { position: static; height: auto; border-right: none; border-bottom: 1px solid var(--rule); padding: 20px; }
    aside nav ol { display: flex; flex-wrap: wrap; gap: 4px; }
    aside .kicker { margin-top: 16px; }
    main { padding: 28px 24px 60px; }
  }
</style>
</head>
<body>
<div class="layout">
  <aside>
    <div class="brand"><span class="dot"></span><span>{{breadcrumb-short}}</span></div>
    <p class="kicker">On this page</p>
    <nav aria-label="Table of contents">
      <ol>
        {{toc-entries}}
      </ol>
    </nav>
    <p class="kicker">Status</p>
    <div class="status-block">{{status-block}}</div>
  </aside>

  <main>
    <div class="doc-head">
      <div class="breadcrumbs">{{breadcrumb}}</div>
      <h1>{{title}}</h1>
      <div class="pill-row">{{header-pills}}</div>
      <dl class="meta-grid">{{meta-grid}}</dl>
    </div>

    {{body-html}}
  </main>

  <footer>Rendered from <code>{{source-path}}</code> on {{render-date}} · regenerate to update.</footer>
</div>

<script>
  // Scrollspy: highlight the TOC entry for the section currently in view.
  const links = Array.from(document.querySelectorAll('aside nav a'));
  const targets = links.map(a => document.getElementById(a.getAttribute('href').slice(1))).filter(Boolean);
  const byId = new Map(targets.map((el, i) => [el.id, links[i]]));
  const io = new IntersectionObserver(entries => {
    for (const e of entries) {
      if (e.isIntersecting) {
        links.forEach(a => a.classList.remove('active'));
        byId.get(e.target.id)?.classList.add('active');
      }
    }
  }, { rootMargin: '-30% 0px -60% 0px' });
  targets.forEach(t => io.observe(t));
</script>
</body>
</html>
```

## Design notes

- **Inter via system fallback** — the font stack starts with `"Inter"` for environments where it's installed; otherwise falls back to `ui-sans-serif` / `system-ui`. The `font-feature-settings` lines (`cv11`, `ss01`, `ss03`) activate Inter's curly-l, single-storey-a, and rounded variants when Inter is present; they're harmless no-ops otherwise. **No web-font load** — that would violate the hard rule.
- **Indigo accent** — `#5b4cff` (light) / `#8b7cff` (dark). Used for active nav, links, decision callouts (via P3), and primary card borders on hover. Soft variant `--accent-soft` for fills.
- **Semantic colour tokens** — `--ok`, `--warn`, `--info`, `--danger`, each with a soft companion for low-contrast fills. Pills, callouts, and chips draw from this palette consistently; pattern authors should not introduce ad-hoc hex values.
- **Sidebar is the primary nav** — 260px sticky column, numbered entries (`01`, `02`, …), scrollspy-highlighted. Brand block at the top is the doc family ("Nestl · ADRs", "PDE · Roadmap"). Status block at the bottom is the one-line state line.
- **Doc head is structured** — breadcrumbs, H1, pill row, metadata grid. Even minimal docs show source + render date in the metadata grid, so provenance is always visible without footer-hunting.
- **Section headers carry index + h2** — every body section wraps in `<section class="s"><header><span class="ix">01</span><h2>…</h2></header>…</section>`. Patterns that attach colour tags (P3) append a `.tag` span inside the `<h2>`.
- **Prose defaults are styled** — even a section that matches no pattern still gets readable type, table styling, blockquote, pre/code treatment. The fallback is "well-typeset doc," not "raw HTML."
- **Print** — sidebar hidden, main expands. Reviewers print-to-PDF for offline annotation get usable output.
- **Responsive** — below 880px the sidebar collapses above the body and nav becomes a horizontal pill list. Skill is desktop-first but mobile shouldn't be broken.
- **Dark mode** — `prefers-color-scheme: dark` swaps every variable. No toggle UI (out of scope).

## When pattern treatments arrive

Pattern markup substitutes into `{{body-html}}` — the shell itself does not change. Pattern CSS appends to the inline `<style>` block via additions, not replacements. Every pattern class is prefixed `p-`; the shell uses no `p-` classes, so collisions are impossible. The fallback (well-typeset prose with index + h2) is the default for any section the catalogue doesn't classify.
