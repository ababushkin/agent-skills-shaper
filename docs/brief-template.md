# Brief template

Each Now artefact gets a brief written before authoring begins, just-in-time as the artefact enters the queue. Briefs for Next items are written only at promotion time. Owner authors briefs.

## Format

Each brief starts with a plain-English summary paragraph for owner review, followed by the YAML block for agent use.

**Summary paragraph** — 3–5 sentences before the YAML. States: what the artefact does, when it fires, key scope boundary, any non-obvious decisions for the owner to confirm. Written in the pack's direct register. No YAML, no bullets.

---

```yaml
artefact: <name>
category: <skill | hook | sub-agent | rules>
pack: <product | engineering | meta>
roadmap_position: <now | next>
lifecycle_stage: <define | plan | build | ship | verify | review | meta | reference>
length_target: <range>
predecessor:
  repo: <URL or "none">
  skill: <skill name in source repo, or "none">
  relation: <derivative | adjacent | new>
  url: <direct link to predecessor artefact, if applicable>
prior_art_notes:
  read_first: <files to read before drafting>
  keep: <what's worth carrying over conceptually>
  change: <what's being changed and why>
  do_not_copy: <reminder that no paragraphs are copied verbatim>
principles_implemented:
  - source: <eng-universal | eng-agentic | roadmap | product>
    id: <principle or rule id>
    bucket: <embedded | standalone | hook | sub-agent>
    note: <one-line summary of how this principle is enforced here>
triage_record_ref: <pointer to the originating idea-bank entry or issue, if any>
purpose: <one paragraph>
scope:
  in: <what this artefact covers>
  out: <what's explicitly excluded, with sibling artefact named>
size_triggers:
  fires_for: <tiny | medium | big | combination>
  does_not_fire_for: <explicit non-triggers>
inputs: <what the artefact expects>
outputs:
  artefact_path: <docs/...>
  artefact_name: <pattern>
workflow_outline: <high-level steps with gates>
artefact_template: <skeleton markdown>
common_rationalisations: <expected pushback patterns>
references: <citations from references/ and source docs>
dependencies:
  prerequisite_artefacts: <must be authored first>
  invokes: <artefacts this one calls into>
  invoked_by: <artefacts that call this>
authoring_notes: <anything specific the author needs to know>
```

For `new` artefacts, the `prior_art_notes` block uses `n/a` for keep/change/do_not_copy.

## See also

- `docs/skill-anatomy.md`, `docs/hook-anatomy.md`, `docs/sub-agent-anatomy.md`
- `docs/authoring-learnings.md`
