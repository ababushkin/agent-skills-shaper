# Tasks: incomplete-feature

Design doc: docs/designs/incomplete-feature.md
Last updated: 2026-05-26

## Task list

### Task 1 — Walking skeleton
**Description:** A handler accepts the request and returns a hardcoded 200 response.
**Done when:** Smoke test hits `/api/example` and receives `{"status":"ok"}`.
**Model:** [routing annotation per references/task-sizing.md — Fast|Balanced|Frontier · risk · review · axes]
**Dependencies:** none

### Task 2 — Add real query logic
**Description:** Replace the hardcoded response with data fetched from the database.
**Done when:** Integration test queries known fixture data and receives the correct response shape.
**Dependencies:** Task 1

## Open questions
<!-- none -->
