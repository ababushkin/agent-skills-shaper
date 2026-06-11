---
layer: node
id: N02
type: refactor
title: Rename two collaborators for clarity
parent: lite-refactor-nongoals
maps_to: linear-issue
completion:
  form: invariant
delegates_to: at-pickup task breakdown (refactor — invariant-preserving)
---

# N02 — Rename two collaborators for clarity

## What

Rename `Mgr` → `RateLimitRegistry` and `Acc` → `RateLimitAccountant` in the
module's internal API. Callers outside the module continue to import the same
public names.

## Why

The current short names obscure the role each collaborator plays and were
flagged twice in recent reviews. The bet: clearer names cut review time on
this module enough to pay back the rename churn within a cycle. Rejected: a
glossary comment in lieu of renaming — comments rot, identifiers don't.

## Completion

**Invariant:** every public import path continues to resolve to the same
behaviour. **Verified by:** the existing module + integration suites,
unchanged. **Out of scope:** the public exports — only internal references
are renamed.

## Non-goals

- Reorganising the module's file layout.
- Changing public exports or import paths.

## Assumptions

- No downstream code reflects over the internal names *(verified)*.

## Key Risks

- **Risk:** a string-based serialiser embeds the old class names. *Falsifier:* a
  grep for the old names across the repo returns only the rename sites.
