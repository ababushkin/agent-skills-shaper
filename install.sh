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

# 2. Add rule file references to ~/.claude/CLAUDE.md if not already present
RULE_REFS=(
  "@${REPO_DIR}/skills/product/PRODUCT_RULES.md"
  "@${REPO_DIR}/skills/engineering/eng-principles-universal.md"
  "@${REPO_DIR}/skills/engineering/eng-principles-agentic.md"
)

touch "${CLAUDE_MD}"

for ref in "${RULE_REFS[@]}"; do
  if grep -qF "${ref}" "${CLAUDE_MD}"; then
    echo "Already present: ${ref}"
  else
    echo "${ref}" >> "${CLAUDE_MD}"
    echo "Added: ${ref}"
  fi
done

echo ""
echo "Done. Restart Claude Code to pick up changes."
echo ""
echo "Available commands:"
echo "  /pde:idea-triage           Triage an incoming idea"
echo "  /pde:roadmap-shape         Shape a planning-cycle roadmap"
echo "  /pde:prototype-to-validate Answer a product question before designing"
echo "  /pde:design-doc            Structure significant engineering work"
echo "  /pde:planning-and-task-breakdown  Break a design into tasks"
echo "  /pde:incremental-implementation  Build in thin vertical slices"
echo "  /pde:plan-review           Review a plan/spec/design before approval"
echo "  /pde:stop-the-line         Scan a diff for quality red flags"
echo "  /pde:backlog-manage        Review and curate the idea bank"
echo ""
echo "To install via Claude Code marketplace instead:"
echo "  /plugin install github@ababushkin/pde-skills"
