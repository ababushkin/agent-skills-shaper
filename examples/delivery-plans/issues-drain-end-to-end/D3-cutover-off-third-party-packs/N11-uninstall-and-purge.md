---
layer: node
id: N11
type: story
title: Uninstall both packs + purge references
parent: D3
serves_kr: KR3
maps_to: linear-issue
external_window: none
completion:
  form: acceptance-criteria
  criterion: >
    Both third-party packs uninstalled; the KR3 grep across drain_cycle/, skills/, and
    .claude/ returns empty; a KR3 audit note records 100% first-party invocation
    across the validation-drain transcripts.
delegates_to: at-pickup task breakdown (story)
---

# N11 — Uninstall both packs + purge references

**Type:** `story`.

> **Blocked by:**
> [N03](../D1-review-gate-proven-on-seeded-defects/N03-personas-and-review-fan-out.md) (the
> review replacement must be live) and
> [N09](../D2-execution-workflow-drains-issues/N09-validation-drains.md) (the audit reads its
> transcripts).

> **▶ On pickup:** break into build tasks per the at-pickup breakdown.

## What

As the pack owner, I want both third-party packs uninstalled and every reference to them purged,
so that first-party coverage is proven by absence rather than asserted while the safety net stays
installed. The KR3 evidence set: empty grep across `drain_cycle/ skills/ .claude/`, a clean
plugin list, and an invocation audit over the validation-drain transcripts.

## Why

The bet: the uninstall is the only honest test of "nothing missed in practice" — while the packs
remain installed, any first-party gap silently falls back and the claim is unfalsifiable.
Rejected alternative: keep the packs installed "just in case" — the dependency stays invisible,
KR3 can never be observed, and the initiative's whole point (one pack) is quietly abandoned.

## Completion

- **Done when:** `grep -rn 'code-review-and-quality\|superpowers' drain_cycle/ skills/ .claude/`
  returns empty.
- **Done when:** the plugin list shows neither superpowers nor agent-skills installed.
- **Done when:** a KR3 audit note records per-issue skill invocations across the 5
  validation-drain transcripts, 100% first-party.

## Assumptions

- No tooling outside the KR3 grep surface (e.g. global `~/.claude` hooks or command wrappers) references the packs. *(to-verify — sweep global settings and hooks at pickup before uninstalling)*

## Key Risks

- **Risk:** a latent dependency surfaces only after uninstall — a hook or wrapper invoking a
  removed skill mid-drain.
  *Mitigation:* uninstall lands well before cycle close so breakage surfaces inside the window;
  reinstalling is one command — a two-way door, unlike shipping the cycle with the dependency
  hidden.

## Tasks

- [ ] `skeleton` — Uninstall both packs and purge any remaining references across the grep surface (global-settings sweep folded in) · Done when: the KR3 grep returns empty and the plugin list shows neither pack · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·M·L
- [ ] Write the KR3 audit note from the validation-drain transcripts · Done when: the note records per-issue skill invocations with 100% first-party across all 5 drains · Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
