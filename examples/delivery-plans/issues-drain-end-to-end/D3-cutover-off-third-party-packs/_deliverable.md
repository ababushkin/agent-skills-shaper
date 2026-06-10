---
layer: deliverable
id: D3
title: Cutover off third-party packs
parent: ..
serves_kr: KR3
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR3 holds — 100% of drained issues in the window invoke the new execution skills,
    both packs are uninstalled, and grep for their skill names across drain_cycle/,
    skills/, and .claude/ returns empty.
---

# D3 — Cutover off third-party packs

**Serves:** KR3 *(brake)* — "100% of drained issues in the window invoke the new execution
skills and zero invoke superpowers/agent-skills; both packs uninstalled and zero references to
their skill names remain in the Shaper repo or drain-cycle prompts."

The brake on the initiative's claim: first-party coverage is proven **by absence**, not asserted
while the safety net stays installed. Two deliberately thin nodes in two repos: **N10** (story,
drain-cycle repo) swaps the hardcoded `/code-review-and-quality` reference and inlined procedure
tail for a one-line pointer at the entry skill — the conflict that currently makes uninstalling
agent-skills break drains. **N11** (story, this repo + plugin state) uninstalls both packs,
purges remaining references, and writes the KR3 invocation audit from the validation-drain
transcripts.

Scope fence: only the pointer swap lives here — the full ≤15-line prompt-template re-scope
belongs to initiative C.

## Nodes

- [N10 — drain-cycle prompt pointer](N10-drain-cycle-prompt-pointer.md) · `story`
- [N11 — Uninstall both packs + purge references](N11-uninstall-and-purge.md) · `story`

## Done when

KR3 is observed: `grep -rn 'code-review-and-quality\|superpowers' drain_cycle/ skills/ .claude/`
returns empty, the plugin list shows neither pack, and the KR3 audit note records 100%
first-party skill invocation across the validation-drain transcripts — reducible to N10 + N11's
criteria, so no acceptance node exists here.
