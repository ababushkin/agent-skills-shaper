#!/bin/sh
# Fan-out harness: dispatches all three personas and deduplicates findings.
# Mirrors the fan-out skill's inline-sequential fallback for non-Claude workers.
# Usage: run.sh <diff-path> <manifest-path>
# Output: one finding per line — "file class severity"
set -e

diff_path="$1"
manifest_path="$2"

persona_dir="$(cd "$(dirname "$0")" && pwd)"
personas_dir="$(dirname "$persona_dir")"

# Run spec-compliance first (spec before code quality per ADR 0003 dispatch order)
sh "$personas_dir/spec-compliance/run.sh"   "$diff_path" "$manifest_path"
sh "$personas_dir/security-auditor/run.sh"  "$diff_path" "$manifest_path"
sh "$personas_dir/code-quality/run.sh"      "$diff_path" "$manifest_path"
