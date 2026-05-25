#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
META_SKILL="$SCRIPT_DIR/../skills/using-this-pack/SKILL.md"

python3 - "$META_SKILL" <<'EOF'
import json, sys
path = sys.argv[1]
try:
    with open(path) as f:
        content = f.read()
    msg = "Shaper pack loaded. Use the skill discovery flowchart to find the right skill for your task.\n\n" + content
    print(json.dumps({"priority": "IMPORTANT", "message": msg}))
except Exception:
    print(json.dumps({"priority": "INFO", "message": "Shaper: using-this-pack meta-skill not found at " + path}))
EOF
