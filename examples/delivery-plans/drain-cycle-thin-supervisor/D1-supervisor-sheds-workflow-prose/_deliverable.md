---
layer: deliverable
id: D1
title: Supervisor sheds workflow prose
parent: ..
serves_kr: KR3
maps_to: linear-milestone
completion:
  form: kr-observed
  criterion: >
    KR3 holds — the worker prompt template is ≤15 lines, a grep for procedure verbs
    (review/fix/commit/push sequences) over drain_cycle/ returns empty, and the test
    suite is green. Observed mechanically: wc -l + grep + pytest exit code.
---

# D1 — Supervisor sheds workflow prose

**Serves:** KR3 *(brake)* — "the supervisor carries zero workflow prose: worker prompt template
≤15 lines, no skill-procedure steps, test suite green."

This deliverable is the re-scope itself: the supervisor↔worker contract is decided once, then
the prompt drops everything the pack now owns. It trips **one Rule A1 trigger** — a
**one-way-door decision touching shared infrastructure**: the contract (what the ≤15-line prompt
carries, what `.drain-handoff.json` carries, which concerns are process vs workflow) is what
every pack skill, the supervisor, and any future non-Claude worker bind to, across two repos. So
its **first node is a `design-doc` node (N01)** and the build nodes — N02 here, N03–N04 in D2 —
are blocked by it: their task breakdown waits until the design doc is accepted.

**N01** (design-doc) decides the prompt-segment allocation, the handoff schema v2, and the
process/workflow boundary chart. **N02** (story, `skeleton: true`) collapses the inlined
preamble/tail procedure in `drain_cycle/prompt.py` into the pointer-only template and
smoke-drains one issue through it.

## Nodes

- [N01 — Thin-supervisor contract design doc](N01-thin-supervisor-contract-design-doc.md) · `design-doc`
- [N02 — Pointer-only prompt template](N02-pointer-only-prompt-template.md) · `story` · `skeleton`

## Done when

KR3 is observed mechanically: `wc -l` on the emitted worker prompt template ≤15, grep for
procedure-verb sequences over `drain_cycle/` empty, pytest exit 0. Reducible to N02's
completion — no acceptance node needed; the milestone closing is the verification.
