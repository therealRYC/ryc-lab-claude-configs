#!/usr/bin/env python3
"""Safely remove .pi-stack.json after pi-stack completion.

Called by /long-run after verifying pi-stack completed successfully.
Guards against accidental deletion by checking that all phases are
in a terminal state before removing the file.

This prevents a common failure mode (long-run gotcha #5): leaving a stale
.pi-stack.json that causes the next /pi-stack invocation to resume an
old pipeline instead of starting fresh.

Usage:
    python3 cleanup_pi_stack_state.py [--project-dir /path/to/project]
"""

import json
import os
import sys
from pathlib import Path

TERMINAL_STATUSES = {"done", "skipped"}


def main() -> None:
    project_dir = Path(
        os.environ.get("CLAUDE_PROJECT_DIR", ".")
    ).resolve()

    if len(sys.argv) > 1 and sys.argv[1] == "--project-dir" and len(sys.argv) > 2:
        project_dir = Path(sys.argv[2]).resolve()

    state_path = project_dir / ".pi-stack.json"

    if not state_path.exists():
        print("No .pi-stack.json found — nothing to clean up")
        sys.exit(0)

    # Safety check: only delete if all phases are terminal
    state = json.loads(state_path.read_text())
    phases = state.get("phases", {})
    non_terminal = [
        name for name, phase in phases.items()
        if phase.get("status") not in TERMINAL_STATUSES
    ]

    if non_terminal:
        print(f"BLOCKED: Cannot clean up — {len(non_terminal)} phases not terminal:")
        for name in non_terminal:
            status = phases[name].get("status", "missing")
            print(f"  - {name}: {status}")
        print("Run verify_pi_stack_completion.py first to diagnose.")
        sys.exit(1)

    # Safe to delete
    feature_name = state.get("feature", "unknown")
    state_path.unlink()
    print(f"Cleaned up .pi-stack.json for feature: {feature_name}")


if __name__ == "__main__":
    main()
