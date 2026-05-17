---
name: html-skeleton
description: >
  Self-contained HTML shell used by the render-html skill. Defines the single-file
  document template: inline CSS (system font, sticky TOC sidebar, prose column,
  dark-mode auto, print stylesheet), inline scrollspy JS, and the hard self-containment
  rule.
type: reference
cited_by:
  - skills/render-html/SKILL.md
---

# HTML skeleton

The render-html skill wraps every markdown body in the shell below. The shell is the **only** mechanism by which output styling and navigation arrive — no external CSS, no external JS, no remote images. That rule is load-bearing for the skill's "opens via `file://` with no network" guarantee; reviewers attach these files to emails and store them in private wikis where CDN URLs silently break.

## The hard rule

Anything injected into the rendered output must satisfy all three:

- **No `<link rel="stylesheet">`.** All CSS lives in the inline `<style>` block.
- **No `<script src=...>`.** All JS lives in the inline `<script>` block at the end of `<body>`.
- **No remote `<img>` URLs.** Inline SVG is preferred; base64 data URIs are allowed when an SVG is impractical. Remote URLs (`http:`, `https:`, protocol-relative `//`) are not.

If a future pattern needs richer interactivity (charts, diagrams, syntax highlighting), inline the minimal library or hand-write the SVG. Adding a CDN is not an option.

## Substitution tokens

The skill substitutes these into the shell at render time. Treat them as the contract between the skill's workflow and this reference.

| Token | Source | Notes |
|---|---|---|
| `{{title}}` | The source markdown's first H1 | Goes in both `<title>` and the page `<h1>`. |
| `{{source-path}}` | Path of the input `.md` file, relative to the repo root if possible | Shown in the provenance meta line. |
| `{{render-date}}` | ISO date (YYYY-MM-DD) of the render | Provenance only — do not include time, so re-renders on the same day produce no diff. |
| `{{toc-entries}}` | One `<li>` per H2/H3 from the source, with class `h2` or `h3` and an `href` to the heading's slug | Slugs are kebab-case from the heading text, deduplicated with `-2`, `-3` if needed. H1 is the title, not a TOC entry. |
| `{{body-html}}` | The markdown body converted to HTML, with H2/H3 carrying `id="<slug>"` matching the TOC links | Pattern-specific treatments (later iterations) substitute richer markup here. |

## The shell

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{title}}</title>
<style>
  :root { --fg: #111; --muted: #666; --bg: #fff; --rule: #e5e5e5; --accent: #0a58ca; }
  @media (prefers-color-scheme: dark) {
    :root { --fg: #eee; --muted: #999; --bg: #111; --rule: #2a2a2a; --accent: #6ea8fe; }
  }
  html, body { margin: 0; padding: 0; background: var(--bg); color: var(--fg); }
  body { font: 16px/1.55 ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
  .layout { display: grid; grid-template-columns: 260px 1fr; max-width: 1100px; margin: 0 auto; }
  nav.toc { position: sticky; top: 0; align-self: start; max-height: 100vh; overflow-y: auto; padding: 24px 16px; border-right: 1px solid var(--rule); font-size: 14px; }
  nav.toc h2 { font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--muted); margin: 0 0 8px; }
  nav.toc ul { list-style: none; padding: 0; margin: 0; }
  nav.toc li { margin: 4px 0; }
  nav.toc li.h3 { padding-left: 12px; font-size: 13px; }
  nav.toc a { color: var(--fg); text-decoration: none; }
  nav.toc a:hover, nav.toc a.active { color: var(--accent); }
  main { padding: 32px 40px; max-width: 72ch; }
  main h1 { font-size: 28px; margin: 0 0 4px; }
  main .meta { color: var(--muted); font-size: 13px; margin-bottom: 32px; }
  main h2 { font-size: 22px; margin-top: 40px; padding-top: 8px; border-top: 1px solid var(--rule); }
  main h3 { font-size: 17px; margin-top: 24px; }
  main pre { background: rgba(127,127,127,0.08); padding: 12px 14px; border-radius: 6px; overflow-x: auto; font-size: 13px; }
  main code { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 0.92em; }
  main table { border-collapse: collapse; margin: 12px 0; }
  main th, main td { border: 1px solid var(--rule); padding: 6px 10px; text-align: left; }
  footer { grid-column: 1 / -1; padding: 24px 40px; color: var(--muted); font-size: 12px; border-top: 1px solid var(--rule); }
  @media print {
    nav.toc { display: none; }
    .layout { grid-template-columns: 1fr; }
  }
  @media (max-width: 720px) {
    .layout { grid-template-columns: 1fr; }
    nav.toc { position: static; max-height: none; border-right: none; border-bottom: 1px solid var(--rule); }
  }
</style>
</head>
<body>
<div class="layout">
<nav class="toc" aria-label="Table of contents">
<h2>Contents</h2>
<ul>
  {{toc-entries}}
</ul>
</nav>
<main>
<h1>{{title}}</h1>
<p class="meta">Rendered from <code>{{source-path}}</code> on {{render-date}}</p>
{{body-html}}
</main>
<footer>Generated by render-html. Re-render the source markdown to update.</footer>
</div>
<script>
  // Scrollspy: highlight the TOC entry for the section currently in view.
  const links = Array.from(document.querySelectorAll('nav.toc a'));
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

- **System font stack** — `ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`. Zero network, native to every platform, sensible fallbacks. Web fonts would be a CDN dependency.
- **Prose width cap** — `max-width: 72ch` on `<main>`. Long-line prose is fatigue-inducing; reviewers skim faster at typographic widths.
- **Sticky TOC** — `position: sticky; top: 0; max-height: 100vh; overflow-y: auto;`. Stays visible while scrolling, scrolls internally for very long TOCs.
- **Scrollspy** — IntersectionObserver-based, ~12 lines. Highlights the TOC entry for whichever section is in view. The `rootMargin: '-30% 0px -60% 0px'` biases the active region to the upper third of the viewport, so the active entry matches where the reader's eye actually is.
- **Dark mode** — `prefers-color-scheme: dark` media query swaps CSS custom properties. Honours OS setting; no toggle UI (out of scope for v0.1).
- **Print** — TOC hidden, grid collapses to single column. Reviewers who print to PDF for offline annotation get something usable.
- **Responsive** — below 720px the TOC moves above the body. The skill is review-oriented (desktop-first) but mobile shouldn't be broken.

## When pattern treatments arrive

Pattern-specific markup (side-by-side alternatives, kanban Now/Next/Later, callouts, dependency timelines) substitutes into `{{body-html}}` — the shell itself does not change. Pattern CSS extends the inline `<style>` block via additions, not replacements, so the prose path remains the default fallback for any markdown the skill does not classify.
