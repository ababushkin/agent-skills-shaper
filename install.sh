#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${HOME}/.claude"
COMMANDS_DIR="${CLAUDE_DIR}/commands"
CLAUDE_MD="${CLAUDE_DIR}/CLAUDE.md"

# Portable in-place sed: GNU sed wants `-i` with no arg, BSD/macOS sed wants
# `-i ''`. Detect once (GNU sed answers --version; BSD sed errors) and route
# accordingly so this script runs on both Linux and macOS.
if sed --version >/dev/null 2>&1; then
  sedi() { sed -i "$@"; }
else
  sedi() { sed -i '' "$@"; }
fi

echo "Installing Shaper from ${REPO_DIR}"

# 1. Generate wrapper command files in ~/.claude/commands/shape/
#    A directory symlink breaks @include resolution: Claude Code resolves @../../ against
#    the virtual path through the symlink (~/.claude/commands/shape/../../ = ~/.claude/),
#    not the real path. Generated wrappers use absolute @paths instead.
mkdir -p "${COMMANDS_DIR}"

if [ -L "${COMMANDS_DIR}/shape" ]; then
  echo "Removing existing symlink: ${COMMANDS_DIR}/shape"
  rm "${COMMANDS_DIR}/shape"
elif [ -d "${COMMANDS_DIR}/shape" ]; then
  echo "Refreshing: ${COMMANDS_DIR}/shape"
  rm -rf "${COMMANDS_DIR}/shape"
fi

mkdir -p "${COMMANDS_DIR}/shape"

# Process top-level and subdirectory command files
for src in "${REPO_DIR}/.claude/commands/"*.md "${REPO_DIR}/.claude/commands"/*/*.md; do
  [ -f "$src" ] || continue
  relpath="${src#${REPO_DIR}/.claude/commands/}"
  dest="${COMMANDS_DIR}/shape/${relpath}"
  mkdir -p "$(dirname "$dest")"
  sed "s|@../../|@${REPO_DIR}/|g; s|@../../../|@${REPO_DIR}/|g" "$src" > "$dest"
  echo "Generated: ${dest}"
done

# 2. Prune stale rule-file @-refs from ~/.claude/CLAUDE.md.
#    Rule files are now lazy-loaded: the session-start hook injects
#    using-this-pack/SKILL.md which tells the model when to read each file.
#    This step removes refs that older installs may have written.
touch "${CLAUDE_MD}"

# Strip stale refs from pre-flatten layout (outside rules/, not caught below).
STALE_PATTERNS=(
  "@${REPO_DIR}/skills/product/PRODUCT_RULES.md"
  "@${REPO_DIR}/skills/engineering/eng-principles-universal.md"
  "@${REPO_DIR}/skills/engineering/eng-principles-agentic.md"
)
for stale in "${STALE_PATTERNS[@]}"; do
  if grep -qF "${stale}" "${CLAUDE_MD}"; then
    sedi "\|^${stale}\$|d" "${CLAUDE_MD}"
    echo "Removed stale ref: ${stale}"
  fi
done

# Prune any ref into this repo's rules/ dir — previously written by this
# script; now lazy-loaded via the session-start hook instead.
if grep -qE "^@${REPO_DIR}/rules/.*\.md$" "${CLAUDE_MD}" 2>/dev/null; then
  sedi -E "\|^@${REPO_DIR}/rules/.*\.md$|d" "${CLAUDE_MD}"
  echo "Pruned lazy-loaded rule refs from ${CLAUDE_MD}"
fi

# 3. Symlink each skill dir into ~/.claude/skills/ as shape-<name>
#    Enables Claude Code's auto-discovery of model-invocable Skills.
#    Symlinks (not generated files) are correct here — SKILL.md is loaded by
#    the runtime through the symlink and doesn't use the relative @../../
#    pattern that broke the commands/ wrappers above.
SKILLS_DIR="${CLAUDE_DIR}/skills"
mkdir -p "${SKILLS_DIR}"

# Prune stale shape-* symlinks (target removed/renamed in the repo).
for link in "${SKILLS_DIR}"/shape-*; do
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
  link="${SKILLS_DIR}/shape-${name}"
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

# 4. Install SessionStart hook into ~/.claude/settings.json so shape skills
#    auto-invoke in any repo, not just agent-skills-shaper.
HOOKS_DIR="${CLAUDE_DIR}/hooks"
HOOK_SRC="${REPO_DIR}/hooks/session-start.sh"
HOOK_DEST="${HOOKS_DIR}/shape-session-start.sh"
GLOBAL_SETTINGS="${CLAUDE_DIR}/settings.json"
HOOK_COMMAND="bash ${HOOK_DEST}"

mkdir -p "${HOOKS_DIR}"
# Rewrite the meta-skill path to absolute. The source hook resolves it relative
# to its own dir ($SCRIPT_DIR/../skills/...), which is correct under the plugin
# install (${CLAUDE_PLUGIN_ROOT}/hooks/) but wrong here: install.sh copies the
# hook to ~/.claude/hooks/, where ../skills/ points at ~/.claude/skills, not the
# repo. Same fix as the command wrappers above.
sed "s|\$SCRIPT_DIR/../skills/|${REPO_DIR}/skills/|g" "${HOOK_SRC}" > "${HOOK_DEST}"
chmod +x "${HOOK_DEST}"

python3 - "${GLOBAL_SETTINGS}" "${HOOK_COMMAND}" <<'PYEOF'
import json, sys, os

settings_path = sys.argv[1]
hook_command = sys.argv[2]

if os.path.exists(settings_path):
    with open(settings_path) as f:
        settings = json.load(f)
else:
    settings = {}

hooks = settings.setdefault("hooks", {})
session_start = hooks.setdefault("SessionStart", [])

# Idempotency: skip if an entry with this exact command already exists.
for entry in session_start:
    for h in entry.get("hooks", []):
        if h.get("command") == hook_command:
            print(f"Already present: {hook_command}")
            sys.exit(0)

session_start.append({
    "matcher": "",
    "hooks": [{"type": "command", "command": hook_command}]
})

with open(settings_path, "w") as f:
    json.dump(settings, f, indent=2)
    f.write("\n")

print(f"Added SessionStart hook → {hook_command}")
PYEOF

echo "✓ SessionStart hook installed → ${HOOK_DEST}"

echo ""
echo "Done. Restart Claude Code to pick up changes."
echo ""
echo "Available commands:"
echo "  /shape:idea                         Triage an incoming idea"
echo "  /shape:design                        Work through a technical or product unknown before building (design doc, backend spike, or product spike)"
echo "  /shape:delivery                     Decompose an initiative into a delivery plan"
echo "  /shape:project                      Shape a vague idea into a goal-driven initiative"
echo "  /shape:plan-review                  Review a plan/spec/design before approval"
echo "  /shape:render-html                  Render a markdown doc as a reviewable HTML file"
echo "  /shape:stop-the-line                Scan a diff for quality red flags"
echo "  /shape:task-annotation-check        Check docs/tasks/*.md for model-tier annotations"
echo ""
echo "Auto-invocable skills (model-triggered, namespaced as shape-<name>):"
for link in "${SKILLS_DIR}"/shape-*; do
  [ -L "${link}" ] || continue
  echo "  $(basename "${link}")"
done
echo ""
echo "To install via Claude Code marketplace instead:"
echo "  /plugin install github@ababushkin/agent-skills-shaper"
