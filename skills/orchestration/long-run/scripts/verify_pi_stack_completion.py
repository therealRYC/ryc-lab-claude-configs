#!/usr/bin/env python3
"""Verify that pi-stack completed successfully after orchestrated dispatch.

Called by /long-run after the Skill tool returns from invoking /pi-stack.
Reads .pi-stack.json and checks that all expected phases reached a terminal
state (done or skipped).

Exit codes:
    0 — all phases terminal, feature PASSED
    1 — at least one phase is not terminal, feature FAILED

Usage:
    python3 verify_pi_stack_completion.py [--project-dir /path/to/project]
"""

import json
import os
import sys
from pathlib import Path

# Phases that must be in a terminal state for completion.
# "Terminal" means done or skipped — anything else means the pipeline
# didn't finish (pending, in_progress, or an unexpected value).
TERMINAL_STATUSES = {"done", "skipped"}

# Phases we check — all 10 pi-stack phases
EXPECTED_PHASES = [
    "ideation", "question", "plan", "implement", "review",
    "qa", "elegance", "visual", "docs", "ship",
]


def verify(state_path: Path) -> tuple[bool, str, list[str]]:
    """Check .pi-stack.json for completion.

    Args:
        state_path: Path to the .pi-stack.json file.

    Returns:
        Tuple of (passed, feature_name, list of issue descriptions).
    """
    if not state_path.exists():
        return False, "unknown", [f"State file not found: {state_path}"]

    state = json.loads(state_path.read_text())
    feature_name = state.get("feature", "unknown")
    phases = state.get("phases", {})
    issues = []

    for phase_name in EXPECTED_PHASES:
        if phase_name not in phases:
            issues.append(f"Phase '{phase_name}' missing from state file")
            continue

        status = phases[phase_name].get("status", "missing")
        if status not in TERMINAL_STATUSES:
            issues.append(f"Phase '{phase_name}' is '{status}' (expected done/skipped)")

    passed = len(issues) == 0
    return passed, feature_name, issues


def main() -> None:
    project_dir = Path(
        os.environ.get("CLAUDE_PROJECT_DIR", ".")
    ).resolve()

    # Allow override via command-line arg
    if len(sys.argv) > 1 and sys.argv[1] == "--project-dir" and len(sys.argv) > 2:
        project_dir = Path(sys.argv[2]).resolve()

    state_path = project_dir / ".pi-stack.json"
    passed, feature_name, issues = verify(state_path)

    if passed:
        print(f"PASS: {feature_name} — all phases complete")

        # Show phase summary for confirmation
        state = json.loads(state_path.read_text())
        phases = state.get("phases", {})
        done_count = sum(1 for p in phases.values() if p.get("status") == "done")
        skipped_count = sum(1 for p in phases.values() if p.get("status") == "skipped")
        print(f"  Phases: {done_count} done, {skipped_count} skipped")

        sys.exit(0)
    else:
        print(f"FAIL: {feature_name} — incomplete phases")
        for issue in issues:
            print(f"  - {issue}")
        sys.exit(1)


if __name__ == "__main__":
    main()
