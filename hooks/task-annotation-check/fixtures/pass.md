# Tasks: example-feature

Design doc: docs/designs/example-feature.md
Last updated: 2026-05-26

## Task list

### Task 1 — Walking skeleton
**Description:** A handler accepts the request and returns a hardcoded 200 response.
**Done when:** Smoke test hits `/api/example` and receives `{"status":"ok"}`.
Model: Fast · risk reversible · review standard · axes RC·SC·HS·SR·OR = L·L·L·L·L
**Dependencies:** none

### Task 2 — Add real query logic
**Description:** Replace the hardcoded response with data fetched from the database.
**Done when:** Integration test queries known fixture data and receives the correct response shape.
Model: Balanced · risk reversible · review standard · axes RC·SC·HS·SR·OR = M·M·L·L·L
**Dependencies:** Task 1

## Open questions
<!-- none -->
