"""_delivery_plan — shared parser for the delivery-plan file-set.

Holds the reader primitives both `walk-delivery-plan` (the gate) and
`plan-to-linear-manifest` (the filing adapter) build on: the front-matter
reader, the task-line reader, and the directory walk. Keeping them in one
module means a plan parses the same way for the gate and for filing — the
manifest can never derive a label off a different reading of the file-set.

Stdlib only, by the same reasoning `walk-delivery-plan` carries: the
front-matter the contract pins down is a small fixed key set, and a targeted
reader for those keys is more honest about what it relies on than a YAML
dependency.
"""

from __future__ import annotations

import re
from pathlib import Path

# --- schema constants (read off docs/delivery-shape-contract.md) -------------

DELIVERABLE_DIR_RE = re.compile(r"^D(\d+)-")
NODE_FILE_RE = re.compile(r"^N(\d+)-.*\.md$")
DELIVERABLE_FILE = "_deliverable.md"
TASK_RE = re.compile(r"^\s*- \[([ xX])\]\s*(.*)$")
SKELETON_TAG = "`skeleton`"

# Required front-matter keys per layer. A file missing any of these is
# "unparseable" — the seam is not mechanical, so callers stop the line.
REQUIRED = {
    "deliverable": ("layer", "id", "serves_kr", "maps_to"),
    "node": ("layer", "id", "type", "serves_kr", "maps_to", "completion.form"),
}

# Task `Model:` tier → the tracker model label it maps to, and a rank so a
# node's label is the *max* tier across its tasks (a node is as heavy as its
# heaviest task).
TIER_TO_MODEL = {"Frontier": "opus", "Balanced": "sonnet", "Fast": "haiku"}
MODEL_RANK = {"haiku": 0, "sonnet": 1, "opus": 2}

TASK_MODEL_RE = re.compile(r"\bModel:\s*(Frontier|Balanced|Fast)\b")
TASK_REVIEW_RE = re.compile(r"\breview\s+(elevated|standard)\b")
# A `Blocked by:` callout names the node ids that gate this one. Only the ids
# in the callout clause count, so the parse stops at the first sentence end —
# a trailing "Graded against the D1 eval (N01/N02)." must not be read as a
# blocker.
BLOCKED_BY_RE = re.compile(r"Blocked by:\s*\**\s*(.+)", re.IGNORECASE)
NODE_ID_RE = re.compile(r"\bN\d+\b")


class PlanError(Exception):
    """A structural / parse failure: the file-set does not walk mechanically."""


# --- front-matter reader -----------------------------------------------------

def _dequote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def read_front_matter(path: Path) -> dict[str, str]:
    """Extract the contract's front-matter keys from a layer file.

    Top-level scalars are read at column 0; the one nested key the manifest
    needs (`completion.form`) is read from the indented `form:` line under
    `completion:`. Block-scalar prose (`>` / `|`) is indented, so it never
    matches the column-0 key pattern and cannot pollute the result.
    """
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise PlanError(f"{path}: cannot read ({exc})") from exc

    if not lines or lines[0].strip() != "---":
        raise PlanError(f"{path}: missing opening '---' front-matter fence")

    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        raise PlanError(f"{path}: front-matter fence not closed with '---'")
    block = lines[1:end]

    fm: dict[str, str] = {}
    for line in block:
        m = re.match(r"^([A-Za-z_][\w]*):(?:[ \t]+(.*))?$", line)
        if m and m.group(2):
            value = m.group(2).strip()
            if value not in (">", "|"):
                fm[m.group(1)] = _dequote(value)

    in_completion = False
    for line in block:
        if re.match(r"^completion:\s*$", line):
            in_completion = True
            continue
        if in_completion:
            if re.match(r"^\S", line):  # dedent to column 0 — left the block
                break
            m = re.match(r"^\s+form:[ \t]+(.+)$", line)
            if m:
                fm["completion.form"] = _dequote(m.group(1).strip())
                break
    return fm


def require_keys(fm: dict[str, str], layer: str, path: Path) -> None:
    missing = [k for k in REQUIRED[layer] if k not in fm]
    if missing:
        raise PlanError(f"{path}: {layer} missing required front-matter {missing}")


# --- task (sub-issue) reader -------------------------------------------------

def read_tasks(path: Path) -> list[dict]:
    tasks: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = TASK_RE.match(line)
        if not m:
            continue
        text = m.group(2).strip()
        skeleton = text.startswith(SKELETON_TAG)
        if skeleton:
            # The inline marker is promoted to the structured `skeleton` field;
            # strip it (and its `— ` / `- ` separator) so the text is the bare task.
            text = text[len(SKELETON_TAG):].lstrip(" —-").strip()
        tasks.append({
            "done": m.group(1).lower() == "x",
            "skeleton": skeleton,
            "text": text,
        })
    return tasks


# --- routing parse (filing adapter only) -------------------------------------

def parse_task_routing(text: str) -> dict:
    """Read the `Model:` tier and `review` flag off one task line.

    Returns the mapped model label (or None when the line carries no `Model:`
    annotation) and whether the task asks for an elevated review. The manifest
    folds these across a node's tasks into its `<model>` and `high` labels.
    """
    tm = TASK_MODEL_RE.search(text)
    tier = tm.group(1) if tm else None
    rm = TASK_REVIEW_RE.search(text)
    return {
        "tier": tier,
        "model": TIER_TO_MODEL[tier] if tier else None,
        "review_elevated": bool(rm and rm.group(1) == "elevated"),
    }


def parse_blocked_by(path: Path) -> list[str]:
    """Read the node ids named in a node's `Blocked by:` callout.

    Returns an ordered, de-duplicated list of `N<nn>` ids. Reads only the
    callout clause — the text up to the first sentence end — so a later
    reference to other nodes in the same line is not mistaken for a blocker.
    """
    blockers: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = BLOCKED_BY_RE.search(line)
        if not m:
            continue
        clause = re.split(r"\.\s", m.group(1), maxsplit=1)[0]
        for node_id in NODE_ID_RE.findall(clause):
            if node_id not in blockers:
                blockers.append(node_id)
    return blockers


# --- walk --------------------------------------------------------------------

def _order(pattern: re.Pattern, name: str) -> int:
    m = pattern.match(name)
    return int(m.group(1)) if m else 0


def walk_lite(root: Path) -> list[dict]:
    """Walk a lite-tier plan: flat N<nn>-*.md files at root, no deliverables.

    Lite plans are the small-scale path delivery-shape emits for single-outcome
    work — no KR/deliverable tagging, no task layer, no manifest. The walker
    returns a list of node records directly; there is no milestone wrapper, and
    the README is not required to carry a hand-count manifest table.
    """
    node_files = sorted(
        (f for f in root.iterdir() if f.is_file() and NODE_FILE_RE.match(f.name)),
        key=lambda f: _order(NODE_FILE_RE, f.name),
    )
    items: list[dict] = []
    for nfile in node_files:
        nfm = read_front_matter(nfile)
        if nfm.get("layer") != "node":
            raise PlanError(f"{nfile}: layer is not 'node'")
        # Lite nodes need layer + id + type + completion.form. They have no
        # parent deliverable so serves_kr / maps_to are optional.
        missing = [k for k in ("layer", "id", "type", "completion.form") if k not in nfm]
        if missing:
            raise PlanError(f"{nfile}: lite node missing required front-matter {missing}")
        tasks = read_tasks(nfile)
        items.append({
            "id": nfm["id"],
            "title": nfm.get("title", ""),
            "type": nfm["type"],
            "completion_form": nfm["completion.form"],
            "path": str(nfile.relative_to(root)),
            "sub_issues": tasks,
        })
    return items


def walk(root: Path) -> list[dict]:
    """Walk the plan into milestones → issues → sub-issues."""
    deliverable_dirs = sorted(
        (d for d in root.iterdir() if d.is_dir() and DELIVERABLE_DIR_RE.match(d.name)),
        key=lambda d: _order(DELIVERABLE_DIR_RE, d.name),
    )
    if not deliverable_dirs:
        raise PlanError(f"{root}: no deliverable directories (D<n>-*) found")

    milestones: list[dict] = []
    for ddir in deliverable_dirs:
        dfile = ddir / DELIVERABLE_FILE
        if not dfile.exists():
            raise PlanError(f"{ddir}: missing {DELIVERABLE_FILE}")
        dfm = read_front_matter(dfile)
        if dfm.get("layer") != "deliverable":
            raise PlanError(f"{dfile}: layer is not 'deliverable'")
        require_keys(dfm, "deliverable", dfile)

        node_files = sorted(
            (f for f in ddir.iterdir() if NODE_FILE_RE.match(f.name)),
            key=lambda f: _order(NODE_FILE_RE, f.name),
        )
        issues: list[dict] = []
        for nfile in node_files:
            nfm = read_front_matter(nfile)
            if nfm.get("layer") != "node":
                raise PlanError(f"{nfile}: layer is not 'node'")
            require_keys(nfm, "node", nfile)
            tasks = read_tasks(nfile)
            issues.append({
                "id": nfm["id"],
                "title": nfm.get("title", ""),
                "type": nfm["type"],
                "serves_kr": nfm["serves_kr"],
                "completion_form": nfm["completion.form"],
                "maps_to": nfm["maps_to"],
                "skeleton": nfm.get("skeleton", "").lower() == "true",
                "tracker_ref": nfm.get("tracker_ref"),
                "path": str(nfile.relative_to(root)),
                "sub_issues": tasks,
            })
        milestones.append({
            "id": dfm["id"],
            "title": dfm.get("title", ""),
            "serves_kr": dfm["serves_kr"],
            "maps_to": dfm["maps_to"],
            "path": str(dfile.relative_to(root)),
            "issues": issues,
        })
    return milestones


def counts(milestones: list[dict]) -> dict[str, int]:
    issues = [i for m in milestones for i in m["issues"]]
    return {
        "milestones": len(milestones),
        "issues": len(issues),
        "sub_issues": sum(len(i["sub_issues"]) for i in issues),
    }
