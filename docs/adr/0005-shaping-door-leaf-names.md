# ADR 0005 — Shaping door leaf names (`shape:idea` / `shape:project` / `shape:design` / `shape:delivery`)

- **Status:** Accepted
- **Date:** 2026-06-12
- **Serves:** Initiative B / KR1 — the shaping library consolidates to four phase doors plus utilities, measured set ≤2,200 lines (N01–N08).
- **Premise for:** N02–N06 (the door builds and utility pass bind these directory, wrapper, and verb names) and Initiative C (supervisor prompts cite the door verbs literally).
- **Record of:** the naming decision in `docs/designs/front-door-ia.md` (N01). The IA doc carries the full alternatives analysis, absorption map, survivor manifest, and gate inventory; this ADR is the durable decision downstream skills bind to. ADR 0004 remains the record of the `shape:`/`exec:` prefix split.

## Context

ADR 0004 reserved both halves of the verb namespace and left the shaping-half leaf names to initiative B. The names are a one-way door: `install.sh` publishes them into every install through wrapper generation and `shape-*` symlinks, `using-this-pack` and README cite them, and initiative C's supervisor prompts will bind them literally. Four alternatives were weighed in the IA doc:

1. **Bare phase-leaf directories** (`skills/idea/`, `skills/project/`, `skills/design/`, `skills/delivery/`) — wrapper leaf = directory leaf = frontmatter `name`; `install.sh` derives the rest. The pack already applies this rule (`delivery.md` → `/shape:delivery`).
2. **Suffixed directories** (`skills/idea-shape/`) — rejected: installed names stutter (`shape-idea-shape`) and the naming rule degrades from a convention to a lookup table.
3. **Keep current directories, retarget wrappers only** — rejected: permanent verb/directory drift; the zero-legacy-citations check can never pass.
4. **Do nothing** — rejected: KR1 fails by definition.

## Decision

**Adopt alternative 1.** The reserved shaping leaves:

| Verb | Directory | Wrapper | Installed symlink |
|---|---|---|---|
| `shape:idea` | `skills/idea/` | `.claude/commands/idea.md` | `~/.claude/skills/shape-idea` |
| `shape:project` | `skills/project/` | `.claude/commands/project.md` | `~/.claude/skills/shape-project` |
| `shape:design` | `skills/design/` | `.claude/commands/design.md` | `~/.claude/skills/shape-design` |
| `shape:delivery` | `skills/delivery/` | `.claude/commands/delivery.md` | `~/.claude/skills/shape-delivery` |
| `shape:plan-review` | `skills/plan-review/` (unchanged) | unchanged | `~/.claude/skills/shape-plan-review` |
| `shape:render-html` | `skills/render-html/` (unchanged) | unchanged | `~/.claude/skills/shape-render-html` |

One convention encodes the table: wrapper leaf = directory leaf = frontmatter `name`; `install.sh` derives the symlink (`shape-<leaf>`) and prunes stale links on re-install. The help text at `install.sh:161–173` is hand-owned and updated per door node.

## Consequences

**Positive**
- The naming rule stays a convention, not a lookup table; `install.sh` needs no per-skill cases.
- Leaf names never appear without the `shape-`/`shape:` prefix on any installed surface, so generic leaves ("design") stay unambiguous.

**Negative / costs**
- A future rename is a coordinated sweep across README, router, help text, and initiative C prompts. Accepted — this is why the IA doc, not a door node, decided the names.
- ADR 0004's verb column listed the pre-consolidation shaping verbs (`shape:idea-triage`, `shape:initiative`, …); this ADR supersedes that column's shaping entries. The `exec:*` half is untouched.

## Scope

This ADR pins the four door leaves and confirms the three utility leaves. The absorption map, measured set, frontmatter cut, and gate inventory live in `docs/designs/front-door-ia.md`. Any change to a leaf name requires a follow-up ADR.
