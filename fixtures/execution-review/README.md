# Execution-Review Fixture Corpus

Seeded-defect diffs and a deterministic grader for measuring review-persona quality.
Use this corpus to score any persona against a known answer key rather than eyeballing output.

## Corpus contents

| Fixture | Findings | Defect classes |
|---------|----------|----------------|
| fix-001 | 3 | type-suppression, ac-violation, security-hole |
| fix-002 | 3 | type-suppression (×2), ac-violation |
| fix-003 | 2 | security-hole, ac-violation |
| fix-004 | 2 | type-suppression, security-hole |
| **Total** | **10** | **3 classes** |

All 10 findings are `Critical` or `Required` severity — the minimum bar a review persona must clear.

## Defect class vocabulary

| Class | Meaning |
|-------|---------|
| `type-suppression` | An error return, type assertion, or panic recovery is discarded (blank identifier, `nil` override, missing `ok` check) |
| `ac-violation` | A block explicitly marked as an acceptance criterion is removed or disabled |
| `security-hole` | A change introduces a direct security vulnerability: injection, secret exposure, sensitive-data leakage |

## Finding line format

Personas emit one finding per line:

```
<file> <class> <severity>
```

Example:

```
auth/token.go type-suppression Critical
api/handler.go ac-violation Required
db/query.go security-hole Critical
```

Matching is exact string comparison on all three fields — case-sensitive, no partial matches.

## Running the grader

```sh
# Grade all personas
bin/grade-execution-review fixtures/execution-review

# Grade a single persona
bin/grade-execution-review fixtures/execution-review --persona <name>
```

Exit codes:

| Code | Meaning |
|------|---------|
| `0` | All graded personas score 100% recall across all fixtures |
| `1` | At least one persona misses at least one seeded finding |
| `64` | Usage error (bad arguments, missing corpus/personas) |

## Interpreting a score

- **10/10** — persona surfaces every seeded finding. Passes the gate.
- **9/10** — one miss. Review the missed finding; tighten the persona prompt for that class.
- **< 9/10** — systematic gap. The persona prompt or the fixture defects need rework.
- **0/10** from the `empty` stub — falsifier passes. The corpus is not trivially solvable.

If the oracle stub ever scores < 10/10, the grader itself has a bug — file it before touching personas.

## Caching runs

Completed persona runs are cached under `_runs/<persona>/<fixture>.json`. The grader reads
the cache on subsequent invocations; delete a cache file to force a re-run.

`_runs/` is gitignored — it holds working state, not source truth.

## Adding fixtures

1. Create `fix-NNN/diff.patch` — a realistic unified diff with the defect clearly present in the `+` lines.
2. Create `fix-NNN/manifest.json` with the structure:

```json
{
  "fixture": "fix-NNN",
  "description": "one-line summary of what is seeded",
  "findings": [
    {
      "file": "path/as/it/appears/in/diff",
      "class": "<type-suppression|ac-violation|security-hole>",
      "severity": "<Critical|Required>",
      "note": "why this is a defect"
    }
  ]
}
```

3. Run the oracle stub to confirm the grader scores the new fixture correctly:

```sh
rm -f fixtures/execution-review/_runs/oracle/fix-NNN.json
bin/grade-execution-review fixtures/execution-review --persona oracle
```

## Adding personas

1. Create `personas/<name>/run.sh` — a shell script that accepts `<diff-path> <manifest-path>` and writes findings to stdout in `file class severity` format.
2. Run: `bin/grade-execution-review fixtures/execution-review --persona <name>`

The oracle and empty stubs in `personas/` serve as integration tests for the grader itself — keep them.
