#!/bin/sh
# Harness: invoke the spec-compliance persona via Claude CLI against a diff.
# Usage: run.sh <diff-path> <manifest-path>
# Output: one finding per line — "file class severity"
set -e

diff_path="$1"
# manifest_path="$2" — not used; persona finds defects from diff alone

persona_dir="$(cd "$(dirname "$0")" && pwd)"
persona_name="$(basename "$persona_dir")"

# Resolve repo root: fixtures/execution-review/personas/<name>/ -> root is four levels up
repo_root="$(cd "$persona_dir/../../../../" && pwd)"
persona_md="$repo_root/personas/$persona_name.md"

if [ ! -f "$persona_md" ]; then
    echo "error: persona file not found: $persona_md" >&2
    exit 1
fi

# Strip YAML frontmatter (everything between the first two --- lines)
system_prompt="$(awk '/^---/{found++; if(found==2){skip=0; next} skip=1; next} skip{next} {print}' "$persona_md")"

diff_content="$(cat "$diff_path")"

# Invoke Claude in print mode; filter to valid finding lines only
claude -p \
    --dangerously-skip-permissions \
    --system-prompt "$system_prompt" \
    "Review this unified diff and emit findings:

$diff_content" 2>/dev/null \
    | grep -E '^[[:alnum:]/_.-]+ [a-z-]+ (Critical|Required)$' || true
