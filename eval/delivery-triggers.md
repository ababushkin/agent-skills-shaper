# delivery trigger eval set

Validates trigger-phrase exclusivity between `delivery` and `project`.
`bin/eval-triggers` reads this table, scores each phrasing against the trigger-phrase lists
extracted from the skills' SKILL.md descriptions, and prints matched-skill vs expected-skill
per row. Exits 0 only on 0 collisions.

## Discriminating factors

- **delivery** fires when committed work already exists and needs to be decomposed into a
  delivery hierarchy. Key markers: "delivery plan", "deliverables", "nodes", "tasks",
  "committed work", "delivery hierarchy".
- **project** fires when defining or shaping a new initiative from a vague idea.
  Key markers: "I want to work on", "new initiative", "create a project",
  "shape this for the next cycle".

## Eval table

| ID  | Phrasing                                            | Expected                    | Notes                                     |
|-----|-----------------------------------------------------|-----------------------------|-------------------------------------------|
| P01 | Turn this initiative into a delivery plan           | delivery              | core trigger phrase — exact match         |
| P02 | Decompose this initiative into deliverables         | delivery              | "decompose this initiative" substring     |
| P03 | Break the initiative into deliverables              | delivery              | exact trigger phrase                      |
| P04 | What are the deliverables for this initiative       | delivery              | exact trigger phrase                      |
| P05 | I want to work on improving onboarding quality      | project            | "I want to work on" substring             |
| P06 | Create a new initiative for the authentication work | project            | "new initiative" substring                |
| P07 | Shape this for the next cycle                       | project            | exact trigger phrase                      |
