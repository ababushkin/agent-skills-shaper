# Tasks, User Stories, Bugs, and Refactors

The objective: lean, unambiguous instructions with a verifiable success state. A task without a visualizable end product is intellectually blank — the assignee cannot know when they are finished.

## User stories

Active voice, the user as subject, the benefit quantified or visualizable.

| Bad | Good |
|---|---|
| "As a user, I want the utilization of an automated system for password recovery." | "As a user, I want to reset my password via an email link so I regain access in under 2 minutes." |
| "As an admin, I want improved visibility into system health." | "As an admin, I want a dashboard showing per-service error rates for the last 24h so I can spot a failing deploy within 5 minutes." |

## Technical tasks

Never assign an "investigation" without defining its end product. Every task carries a **Done when** the reviewer can check by looking at something.

| Bad | Good |
|---|---|
| "Perform an investigation into the latency situation." | "Profile the /orders endpoint. **Done when:** a report names the three highest-latency queries with their P95 timings." |
| "Improve test coverage." | "Add unit tests for the billing module. **Done when:** billing coverage exceeds 85% and CI passes." |
| "Look into the flaky deploy." | "Reproduce the deploy failure. **Done when:** a ticket documents the failing step, its trigger condition, and a proposed fix." |

## Sizing and shape

Keep a task small enough to verify in one pass, and front-load the story so the dense facts don't bury it.

- **Split anything over three moves.** A move is a distinct, separately-verifiable change to one concern — touching a new file, a new layer, or a new behaviour. "Add a column to the orders table, backfill it, expose it in the API, and render it in the dashboard" is four moves (schema, data, API, UI); "rename a variable and update its three call sites" is one. A task over three moves becomes two or more tasks — unless the moves must ship atomically (then say so).
- **Short opening story, then bullets.** State role, desired system behavior, and user value in one plain sentence. Move the dense implementation facts — files, functions, states, commands, slugs, model choices, logs, failure modes — into bullets below it.
- **Name the rejected approaches that prevent a wrong turn.** List the alternative the assignee should *not* take, and why, only when it heads off a likely mistake. Skip it when no plausible wrong turn exists.
- **Prove both paths.** Name the observable proof for the success path and for the failure path — what a reviewer sees when it works and when it falls back or no-ops.

## Ticket shape

For an implementation ticket, use a fixed skeleton so nothing load-bearing goes missing:

- **What** — one short user story, then the exact behavior change.
- **Where** — files, functions, states, APIs, commands, known line references.
- **Why** — the operational gap, incident, or user cost that forces the change.
- **Approach** — the smallest design that closes the gap.
- **Rejected approaches** — alternatives the assignee should not take, and why.
- **Completion** — verifiable done states for the success, fallback, and no-op cases.
- **Tasks** — small work units, one primary outcome each.
- **Risks** — concrete failure modes, each with a mitigation or a falsifier.

## Bugs

State observed behavior, expected behavior, and reproduction — facts a developer can act on. The system or user is the subject of every sentence.

> Bad: "There seems to be an issue where sometimes things don't load properly on mobile."
> Good: "On iOS Safari, the cart drawer renders empty after adding a third item. Expected: all items listed. Repro: add 3 items within 10s on a throttled connection. **Done when:** the drawer lists all items in the repro case and a regression test covers it."

## Refactors

A refactor's end product is a measurable property of the code, not a feeling of cleanliness.

> Bad: "Clean up the auth module."
> Good: "Extract token validation from `auth_handler.py` into `token_validator.py`. **Done when:** `auth_handler.py` is under 200 lines, all existing tests pass, and no module imports both."

## Task review additions

- Is the doer (user, system, developer) the grammatical subject?
- Does the "Done when" describe something a reviewer can see or run?
- Is any task with more than three distinct moves split, unless those moves must ship atomically?
- Does every success and failure path name its observable proof?
- Did the pruning preserve dependencies ("blocked by AUTH-142") and assumptions?
