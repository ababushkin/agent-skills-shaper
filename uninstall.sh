#!/usr/bin/env bash
# Uninstall the shaper plugin from the current user's Claude Code config.
# Safe to run multiple times.

set -euo pipefail

SETTINGS="$HOME/.claude/settings.json"
HOOK_SCRIPT="$HOME/.claude/hooks/shape-session-start.sh"

echo "Uninstalling shaper..."

# 1. Remove the SessionStart hook entry from settings.json
if [ -f "$SETTINGS" ]; then
  python3 - "$SETTINGS" <<'EOF'
import json, sys

path = sys.argv[1]
with open(path) as f:
    d = json.load(f)

hooks = d.get("hooks", {})
session_start = hooks.get("SessionStart", [])

before = len(session_start)
session_start = [
    entry for entry in session_start
    if not any(
        isinstance(h.get("command", ""), str) and "shape-session-start" in h.get("command", "")
        for hook in entry.get("hooks", [])
        for h in [hook]
    )
]

if len(session_start) < before:
    hooks["SessionStart"] = session_start
    if not hooks["SessionStart"]:
        del hooks["SessionStart"]
    if not hooks:
        del d["hooks"]
    else:
        d["hooks"] = hooks
    with open(path, "w") as f:
        json.dump(d, f, indent=2)
        f.write("\n")
    print("  Removed SessionStart hook from settings.json")
else:
    print("  SessionStart hook not found in settings.json (already removed?)")
EOF
fi

# 2. Remove the hook script
if [ -f "$HOOK_SCRIPT" ]; then
  rm "$HOOK_SCRIPT"
  echo "  Removed $HOOK_SCRIPT"
else
  echo "  Hook script not found (already removed?)"
fi

echo "Done. Run /reload-plugins in Claude Code to apply."
