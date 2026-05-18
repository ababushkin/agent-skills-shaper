#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
COMMANDS_DIR="${CLAUDE_DIR}/commands"
CLAUDE_MD="${CLAUDE_DIR}/CLAUDE.md"

echo "Installing pde-skills from ${REPO_DIR}"

# 1. Generate wrapper command files in ~/.claude/commands/pde/
#    A directory symlink breaks @include resolution: Claude Code resolves @../../ against
#    the virtual path through the symlink (~/.claude/commands/pde/../../ = ~/.claude/),
#    not the real path. Generated wrappers use absolute @paths instead.
mkdir -p "${COMMANDS_DIR}"

if [ -L "${COMMANDS_DIR}/pde" ]; then
  echo "Removing existing symlink: ${COMMANDS_DIR}/pde"
  rm "${COMMANDS_DIR}/pde"
elif [ -d "${COMMANDS_DIR}/pde" ]; then
  echo "Refreshing: ${COMMANDS_DIR}/pde"
  rm -rf "${COMMANDS_DIR}/pde"
fi

mkdir -p "${COMMANDS_DIR}/pde"

for src in "${REPO_DIR}/.claude/commands/"*.md; do
  fname="$(basename "$src")"
  dest="${COMMANDS_DIR}/pde/${fname}"
  sed "s|@../../|@${REPO_DIR}/|g" "$src" > "$dest"
  echo "Generated: ${dest}"
done

# 2. Add rule file references to ~/.claude/CLAUDE.md if not already present.
#    Also strips stale refs from the pre-flatten layout
#    (skills/engineering/eng-principles-*.md, skills/product/PRODUCT_RULES.md)
#    so re-runners don't end up with broken @-includes.
RULE_REFS=(
  "@${REPO_DIR}/rules/PRODUCT_RULES.md"
  "@${REPO_DIR}/rules/eng-principles-universal.md"
  "@${REPO_DIR}/rules/eng-principles-agentic.md"
)

touch "${CLAUDE_MD}"

# Strip stale refs from pre-flatten layout.
STALE_PATTERNS=(
  "@${REPO_DIR}/skills/product/PRODUCT_RULES.md"
  "@${REPO_DIR}/skills/engineering/eng-principles-universal.md"
  "@${REPO_DIR}/skills/engineering/eng-principles-agentic.md"
)
for stale in "${STALE_PATTERNS[@]}"; do
  if grep -qF "${stale}" "${CLAUDE_MD}"; then
    # Use sed with | as delimiter since paths contain /
    sed -i '' "\|^${stale}\$|d" "${CLAUDE_MD}"
    echo "Removed stale ref: ${stale}"
  fi
done

for ref in "${RULE_REFS[@]}"; do
  if grep -qF "${ref}" "${CLAUDE_MD}"; then
    echo "Already present: ${ref}"
  else
    echo "${ref}" >> "${CLAUDE_MD}"
    echo "Added: ${ref}"
  fi
done

# 3. Symlink each skill dir into ~/.claude/skills/ as pde-<name>
#    Enables Claude Code's auto-discovery of model-invocable Skills.
#    Symlinks (not generated files) are correct here — SKILL.md is loaded by
#    the runtime through the symlink and doesn't use the relative @../../
#    pattern that broke the commands/ wrappers above.
SKILLS_DIR="${CLAUDE_DIR}/skills"
mkdir -p "${SKILLS_DIR}"

# Prune stale pde-* symlinks (target removed/renamed in the repo).
for link in "${SKILLS_DIR}"/pde-*; do
  [ -L "${link}" ] || continue
  if [ ! -e "${link}" ]; then
    echo "Pruning stale symlink: ${link}"
    rm "${link}"
  fi
done

# Create/refresh symlinks for skill dirs containing a SKILL.md.
# This filter excludes non-skill workspace dirs (e.g. plan-review-workspace).
for skill_dir in "${REPO_DIR}/skills/"*/; do
  [ -f "${skill_dir}SKILL.md" ] || continue
  name="$(basename "${skill_dir}")"
  link="${SKILLS_DIR}/pde-${name}"
  if [ -e "${link}" ] && [ ! -L "${link}" ]; then
    echo "WARNING: ${link} exists and is not a symlink — skipping"
    continue
  fi
  target="${skill_dir%/}"
  if [ -L "${link}" ] && [ "$(readlink "${link}")" = "${target}" ]; then
    echo "Already linked: ${link}"
  else
    ln -sfn "${target}" "${link}"
    echo "Linked: ${link} -> ${target}"
  fi
done

echo ""
echo "Done. Restart Claude Code to pick up changes."
echo ""
echo "Available commands:"
echo "  /pde:idea-triage           Triage an incoming idea"
echo "  /pde:roadmap-shape         Shape a planning-cycle roadmap"
echo "  /pde:prototype-to-validate Answer a product question before designing"
echo "  /pde:backend-spike         Investigate a backend correctness question before implementing"
echo "  /pde:design-doc            Structure significant engineering work"
echo "  /pde:planning-and-task-breakdown  Break a design into tasks"
echo "  /pde:incremental-implementation  Build in thin vertical slices"
echo "  /pde:plan-review           Review a plan/spec/design before approval"
echo "  /pde:stop-the-line         Scan a diff for quality red flags"
echo "  /pde:backlog-manage        Review and curate the idea bank"
echo ""
echo "Auto-invocable skills (model-triggered, namespaced as pde-<name>):"
for link in "${SKILLS_DIR}"/pde-*; do
  [ -L "${link}" ] || continue
  echo "  $(basename "${link}")"
done
echo ""
echo "To install via Claude Code marketplace instead:"
echo "  /plugin install github@ababushkin/pde-skills"
