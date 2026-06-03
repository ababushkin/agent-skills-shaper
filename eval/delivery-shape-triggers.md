# delivery-shape trigger eval set

Validates trigger-phrase exclusivity between `delivery-shape`, `initiative-shape`, and
`execution-breakdown` in both directions. `bin/eval-triggers` reads this table,
scores each phrasing against the trigger-phrase lists extracted from the three skills'
SKILL.md descriptions, and prints matched-skill vs expected-skill per row. Exits 0 only
on 0 collisions.

## Discriminating factors

- **delivery-shape** fires when a committed initiative already exists and needs to be
  decomposed into a delivery hierarchy. Key markers: "initiative", "deliverables",
  "delivery plan", "nodes".
- **initiative-shape** fires when defining or shaping a new initiative from a vague idea.
  Key markers: "I want to work on", "new initiative", "create a project",
  "shape this for the next cycle".
- **execution-breakdown** fires when a single design or spec needs task-level
  breakdown. Key markers: "tasks", "task list", "build this in order", "steps".

## Eval table

| ID  | Phrasing                                            | Expected                    | Notes                                     |
|-----|-----------------------------------------------------|-----------------------------|-------------------------------------------|
| P01 | Turn this initiative into a delivery plan           | delivery-shape              | core trigger phrase — exact match         |
| P02 | Decompose this initiative into deliverables         | delivery-shape              | "decompose this initiative" substring     |
| P03 | Break the initiative into deliverables              | delivery-shape              | exact trigger phrase                      |
| P04 | What are the deliverables for this initiative       | delivery-shape              | exact trigger phrase                      |
| P05 | I want to work on improving onboarding quality      | initiative-shape            | "I want to work on" substring             |
| P06 | Create a new initiative for the authentication work | initiative-shape            | "new initiative" substring                |
| P07 | Shape this for the next cycle                       | initiative-shape            | exact trigger phrase                      |
| P08 | Break this down into tasks                          | execution-breakdown | exact trigger phrase                      |
| P09 | Give me a task list for this node                   | execution-breakdown | "give me a task list" substring           |
| P10 | What order should we build this in                  | execution-breakdown | exact trigger phrase                      |
