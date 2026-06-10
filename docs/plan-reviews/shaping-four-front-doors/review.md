# Plan review: shaping-four-front-doors

## Plan reference

`examples/delivery-plans/shaping-four-front-doors/` — delivery plan for initiative B
("Shaping consolidates to four dense front doors", Linear project
`962be170-d2f2-4b4e-99e5-19f01140c3b4`). Reviewed 2026-06-10, same session as emission;
both mechanical gates passed (`3 / 8 / 19` MATCH, framing PASS) before and after the
review-driven fixes recorded below.

## Inputs

- **Appetite**: 8 nodes (fixed — matches the initiative's ~8-issue appetite)
- **Cynefin domain**: Complicated — consolidation against existing anatomy specs with a
  measurable brake (the benchmark); knowable, not emergent
- **Tier**: Full — selected because appetite > 5 slices AND the absorption map is a
  one-way-door decision (folded skills are deleted). Fast-track gate did not fire:
  fails preconditions 1 (not KTLO class) and 3 (multi-slice).
- **Trigger**: plan just produced and about to be approved/bound (trigger 1); one-way door
  (trigger 4, auto-fire).

## B1 — Problem framing

**OVERTURNED** (no defect). The plan opens with the goal (four reachable front doors, every
pruned skill's content absorbed or deliberately deleted) and three measurable KRs with
verified baselines — problem-first, not solution-first. Falsifying condition: a reader
unable to state from the README alone why 14 skills is a problem; the bet table answers it
(footprint, over-cap skills, routing ambiguity).

## B2 — Scope clarity

| Item | Verdict | Falsifying condition |
|---|---|---|
| The frontmatter cut contradicts the repo's own authoring contract (`docs/skill-anatomy.md`, CLAUDE.md's required-fields and length sections) and no node updated them | **SUSTAINED → resolved in session** | the documented required fields equal the IA's surviving set after N06 — now N06's fourth task with its own Done-when |
| KR3's sweep surface under-counted: `AGENTS.md:19` cites `initiative-shape`; `plugin.json`'s description names "idea triage, roadmap shaping" and is invisible to the `*.md` grep; KR3 names hooks but N08 didn't | **SUSTAINED → resolved in session** | the KR3 grep plus the plugin.json check return clean after N08 — N08's What and skeleton task now name AGENTS.md, hooks/, and plugin.json explicitly |
| `plugin.json` `"commands": "./.claude/commands"` ships wrapper deletions to marketplace installs automatically | OVERTURNED | covered — each door node deletes its own wrappers and N08 round-trips install/uninstall; no separate node needed |
| "Density pass" and "absorbed where the map says so" are vague enough to expand silently | PARTIAL | bounded by N01: the absorption map and frontmatter spec are fixed in an accepted doc before any door's task breakdown — vagueness is quarantined to one reviewed artefact |
| Initiative A concurrently adds skills to `skills/`, drifting KR1's `wc -l` check | PARTIAL | N01 pins the measured set explicitly (to-verify, owner confirms at doc acceptance) rather than the KR being silently rewritten |
| Memory/instruction files outside the repo (user CLAUDE.md, drain-cycle prompts) may cite folded names | PARTIAL | N08's risk section records out-of-repo citations in the sweep note as follow-ups, not silently skipped |

## B3 — Assumptions + evidence quality

| Assumption | Confidence (Gilad) | 5-min test or owner | Verdict |
|---|---|---|---|
| plan-review's 69-line overage is explanatory redundancy, not behaviour-bearing prose | 0.1 (assumption) | diff the sections eval assertions cite against the candidate cut list before compressing; the real test is N07's benchmark re-run — the brake is structural, with a defined repair loop and kill threshold | OVERTURNED as a plan defect — the plan does not *trust* this assumption, it measures it |
| The 637→≤300/350 shape:design fold closes without dropping a `[GATE]` | 0.5 (sized from line counts only) | count `[GATE]` + irreducible protocol lines across the three sources at N01 (the gate-preservation inventory is exactly this test) | OVERTURNED — tagged to-verify on N05, inventory task on N01, kill condition documented as the exit |
| KR1's measured set excludes A's execution skills | 2 (the KR baseline arithmetic only closes on the pre-A 14-skill set) | owner confirms the pinned set at N01 doc acceptance — named owner, named moment | OVERTURNED — encoded as N01's to-verify, not assumed silently |

No untested sub-5-confidence assumption survives without a named test or owner; none block.

## B4 — Dependencies (Full only)

| Dependency | Owner confirmed? | Capacity confirmed? | Verdict |
|---|---|---|---|
| A/N04 naming table (ABA-361) | yes — same owner; bound as blockedBy edge on N01 at binding | A's D2 is in the current drain stream | OVERTURNED, conditional on the edge actually being bound |
| Benchmark harness + eval set | yes — in-repo, pinned at `docs/benchmarks.md:101-104`; N06 keeps evals.json byte-identical | n/a | OVERTURNED |
| install.sh wrapper/symlink machinery | yes — in-repo, verified lines 20-38 / 69-91 | n/a | OVERTURNED |
| Initiative C's plan cites `product-spike` in a delegates_to line | yes — N08 sweeps it by name | n/a | OVERTURNED |

## B5 — Reversibility + ADR pairing (Full only)

| One-way door | Alternatives in plan? | ADR exists / committed? | Verdict |
|---|---|---|---|
| Absorption map + skill deletions | yes — alias-door rejected (N03 Why), keep-spikes-as-utilities rejected (N05 Why), keep-all-compressed rejected (N04 Why) | N01 design doc is the committed record, Rule A1 branch, blocks all builds | OVERTURNED |
| Door/wrapper/symlink naming scheme | consumed from A/N04's accepted naming table — decided once, upstream | A/N04's doc | OVERTURNED |

## B6 — Operability + success metrics (Full only)

- Metrics: named — `wc -l` cap check over a pinned set, benchmark aggregate, KR3 grep
- Alerts: n/a (markdown pack; the benchmark is the regression detector)
- Rollback path: named — git revert per node; kill condition restores the flat layout wholesale
- Runbook: n/a — single-user pack; the sweep note and watch note are the operative records
- Capacity headroom: n/a
- User-visible outcome metric: the invocation-rate outcome deliberately lives in initiative
  A's KR3 (recorded deviation in the project description); B's KRs are
  maintenance/correctness/discipline by design — named, not absent

## B7 — Sequencing + capacity (Full only)

Critical path surfaced: N01 → {N02 skeleton, N03–N05 folds} → N06 → {N07, N08}, with the
benchmark brake last because it measures final state. Appetite fixed at 8 nodes. Single-repo,
single Graphite stack; blockedBy edges give the topo order. OVERTURNED.

## B8 — Pre-mortem

Assume the initiative shipped and failed within the cycle. Top 3, ranked:

1. **The shape:design fold ships gateless to make the cap** — the 2:1 compression quietly
   drops a stop-condition and unbounded spikes return. Kill-switch: N01's gate-preservation
   inventory + N05's Done-when checks presence against that list, and the documented kill
   condition (over 350 without dropping a gate → stop) is the sanctioned exit.
2. **The benchmark drops for reasons that aren't prose loss** (runner variance at n=3, ±2%
   baseline) and the repair loop burns both attempts restoring the wrong prose. Kill-switch:
   N07's widen-to-n=5 rule when the result lands within one standard error of 90%.
3. **Concurrent initiative-A drains collide with B's renames** in the same `skills/` tree,
   producing stack conflicts and a KR1 count that moves mid-measurement. Kill-switch: the
   measured set is pinned at N01, and cycle planning sequences B's nodes behind ABA-361 via
   the bound edge; same-repo stack ordering handles the rest.

## Recommendation

**APPROVE** — both SUSTAINED findings were fixed in the plan during this review (N06's
authoring-contract task; N08's widened sweep surface), gates re-run green (`3 / 8 / 19`
MATCH, framing PASS), and every remaining risk is carried by a named brake, inventory, or
kill condition rather than by hope.

### Conditions

1. At Linear binding, the blockedBy edges must be created exactly as the plan names them —
   N01 ← ABA-361 (cross-initiative), N02–N06 ← N01, N07/N08 ← N02–N06 — because both cycle
   planning and drain-cycle's stack composition read them.
2. At N01 acceptance, the owner explicitly confirms the measured set for the ≤2,200 check
   (the to-verify) — the KR is not to be reinterpreted downstream of an unpinned set.
3. At N05 pickup, the kill-condition watch note is a deliverable of the node, not an
   informal observation — zero-clean-fold exits must be auditable.
