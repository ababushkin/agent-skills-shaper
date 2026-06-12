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
- Did the pruning preserve dependencies ("blocked by AUTH-142") and assumptions?
