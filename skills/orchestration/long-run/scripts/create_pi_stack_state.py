#!/usr/bin/env python3
"""Generate a .pi-stack.json state file for orchestrated pi-stack dispatch.

This script is called by the /long-run skill before invoking /pi-stack on an
L/XL complexity feature. It creates the state file that pi-stack reads to know:
  - What feature to work on (name, brief path)
  - That it's in orchestrated mode (auto-implement, skip PR)
  - Which phases to start from (implement, skipping ideation/question/plan)

Usage:
    python3 create_pi_stack_state.py \
        --feature "core-calculation" \
        --feature-id "feat-03" \
        --branch "long-run/core-calculation" \
        --brief "Plans/features/feat-03-brief.md" \
        --specsheet "Plans/specsheet.md" \
        [--project-dir /path/to/project]

The script validates that the brief file exists before writing, preventing
a common failure mode where pi-stack starts without context.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def validate_inputs(args: argparse.Namespace, project_dir: Path) -> list[str]:
    """Check that required files exist before creating state.

    Args:
        args: Parsed command-line arguments.
        project_dir: Resolved project root directory.

    Returns:
        List of error messages (empty if all valid).
    """
    errors = []

    # The feature brief is the most critical file — pi-stack reads it for context
    brief_path = project_dir / args.brief
    if not brief_path.exists():
        errors.append(f"Brief file not found: {brief_path}")

    # Specsheet is important but not strictly required for pi-stack
    specsheet_path = project_dir / args.specsheet
    if not specsheet_path.exists():
        errors.append(f"Warning: Specsheet not found: {specsheet_path}")

    return errors


def create_state(args: argparse.Namespace, project_dir: Path) -> dict:
    """Build the .pi-stack.json state dictionary.

    The state file uses the "orchestrated" invocation mode, which tells pi-stack:
      - Don't ask the user to describe the feature (it's in the brief)
      - Auto-implement instead of waiting for user code (phase 3)
      - Skip PR creation in ship phase (long-run manages commits)

    Args:
        args: Parsed command-line arguments.
        project_dir: Resolved project root directory.

    Returns:
        Dictionary ready for JSON serialization.
    """
    # All 10 pi-stack phases with their initial states.
    # Ideation, question, AND plan are all skipped because long-run's decompose
    # phase already handled them interactively with the user (office-hours +
    # plan-eng-review per feature). The locked plan is embedded in the feature
    # brief. Pi-stack starts at implement.
    phases = {
        "ideation": {"status": "skipped"},
        "question": {"status": "skipped"},
        "plan": {"status": "skipped"},
        "implement": {"status": "pending"},
        "review": {"status": "pending"},
        "qa": {"status": "pending"},
        "elegance": {"status": "pending"},
        "visual": {"status": "pending"},
        "docs": {"status": "pending"},
        "ship": {"status": "pending"},
    }

    return {
        "feature": args.feature,
        "branch": args.branch,
        "started": datetime.now(timezone.utc).isoformat(),
        "invocation_mode": "orchestrated",
        "orchestrator": "long-run",
        "feature_id": args.feature_id,
        "specsheet": args.specsheet,
        "brief": args.brief,
        "skip_ship_pr": True,
        "current_phase": "implement",
        "phases": phases,
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create .pi-stack.json for orchestrated pi-stack dispatch"
    )
    parser.add_argument("--feature", required=True, help="Feature name (from brief)")
    parser.add_argument("--feature-id", required=True, help="Feature ID (e.g., feat-03)")
    parser.add_argument("--branch", required=True, help="Current git branch")
    parser.add_argument("--brief", required=True, help="Path to feature brief (relative to project)")
    parser.add_argument("--specsheet", default="Plans/specsheet.md", help="Path to specsheet")
    parser.add_argument(
        "--project-dir",
        default=None,
        help="Project root directory (defaults to cwd)",
    )

    args = parser.parse_args()

    # Resolve project directory — use CLAUDE_PROJECT_DIR if available, else cwd
    import os
    project_dir = Path(args.project_dir or os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()

    # Validate inputs before writing
    errors = validate_inputs(args, project_dir)
    hard_errors = [e for e in errors if not e.startswith("Warning:")]
    if hard_errors:
        for error in hard_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        sys.exit(1)

    # Print warnings but continue
    for warning in [e for e in errors if e.startswith("Warning:")]:
        print(warning, file=sys.stderr)

    # Build and write the state file
    state = create_state(args, project_dir)
    state_path = project_dir / ".pi-stack.json"

    # json.dumps with indent=2 makes the file human-readable for debugging
    state_path.write_text(json.dumps(state, indent=2) + "\n")

    # Confirmation output for Claude to verify
    print(f"Created {state_path}")
    print(f"  Feature: {args.feature} [{args.feature_id}]")
    print(f"  Mode: orchestrated (auto-implement, skip PR)")
    print(f"  Starting phase: implement (plan locked in brief)")
    print(f"  Brief: {args.brief}")


if __name__ == "__main__":
    main()
