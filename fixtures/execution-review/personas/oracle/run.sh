#!/bin/sh
# Oracle stub persona: reads the fixture manifest and emits all seeded findings.
# Used to verify the grader correctly awards 100% recall for a perfect reviewer.
#
# Usage: run.sh <diff-path> <manifest-path>
# Output: one finding per line — "file class severity"
set -e
manifest="$2"
python3 - "$manifest" <<'EOF'
import json, sys
data = json.load(open(sys.argv[1]))
for f in data["findings"]:
    print(f["file"] + " " + f["class"] + " " + f["severity"])
EOF
