---
layer: deliverable
id: D3
title: No dangling references
parent: ..
serves_kr: KR3
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR3 holds — the grep for deleted/folded skill names over tracked markdown returns only
    intentional predecessor-frontmatter and historical-record mentions per the allowlist
    the sweep note defines, and a fresh install/uninstall round-trip yields exactly the
    survivor set.
---

# D3 — No dangling references

**Serves:** KR3 *(brake)* — "zero dangling references to deleted/folded skills in README,
install.sh, commands, hooks, or cross-skill citations."

The verified reference surface (2026-06-10, tracked files only): `README.md`,
`rules/PRODUCT_RULES.md`, `CHANGELOG.md`, three `references/*.md` files (task-sizing,
app-context-schema, portfolio-themes), two command wrappers (`roadmap.md`,
`backlog-manage.md`), `docs/idea-bank/triage-baseline-data.md`, `using-this-pack`'s routing
table, and the five affected SKILL.md files themselves. One node — **N08** — sweeps it after
the deletions land; the door nodes delete their own dirs and wrappers, so this deliverable
owns only the cross-cutting citations and the install/uninstall round-trip proof. No Rule A1
trigger: every edit is reversible and single-repo.

## Nodes

- [N08 — Reference sweep + fresh-install check](N08-reference-sweep.md) · `story`

## Done when

KR3 is observed: the grep gate returns only allowlisted mentions and the install/uninstall
round-trip is clean. Reducible to N08 done; no acceptance node needed.
