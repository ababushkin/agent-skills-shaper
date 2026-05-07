## What this PR does

<!-- One paragraph. Which problem does it solve, which artefact does it add or change. -->

## Type

- [ ] New skill
- [ ] New hook
- [ ] New reference
- [ ] Update to an existing artefact
- [ ] Docs / meta (README, CONTRIBUTING, CHANGELOG, etc.)
- [ ] Bug fix

## Checklist for new artefacts

<!-- Skip the whole block for docs/bug-fix PRs. -->

- [ ] Followed the matching anatomy doc (`docs/skill-anatomy.md`, `docs/hook-anatomy.md`, or `docs/sub-agent-anatomy.md`)
- [ ] Frontmatter has all required fields (`name`, `description`, `pack`, `lifecycle_stage`, `principles_implemented`, `length_target`, `author`, `predecessor`)
- [ ] Length is within target (skills: 100–300 lines, hard cap 350)
- [ ] Gates marked `[GATE]` are present and not optional
- [ ] No verbatim copy from `addyosmani/agent-skills` or any other source pack
- [ ] No stack-prescriptive content (skill prose is stack-agnostic)
- [ ] Predecessor relation declared (`derivative` / `adjacent` / `new`) with link
- [ ] Voice matches at least two existing skills (read them first)

## Notes for the reviewer

<!-- Anything you want flagged: a tradeoff you made, an assumption you're unsure about,
     an existing artefact this might overlap with. -->
