#!/usr/bin/env python3
"""
PreToolUse hook for Edit and Write tools — enforces /freeze directory boundary.

When ~/.claude/.freeze-dir.txt exists, blocks Edit/Write operations on files
outside the frozen directory. Read-only tools (Read, Grep, Glob) are unaffected.

Output protocol (JSON on stdout):
  - {"hookSpecificOutput": {"permissionDecision": "allow", ...}}  → permit
  - {"hookSpecificOutput": {"permissionDecision": "deny", ...}}   → block
  - (no output) → defer to normal system (when no freeze is active)
"""

import sys
import json
from pathlib import Path

# State file written by /freeze skill, removed by /unfreeze
FREEZE_STATE = Path.home() / ".claude" / ".freeze-dir.txt"


def make_decision(decision: str, reason: str) -> None:
    """Print a hook decision as JSON and exit.

    Args:
        decision: One of "allow" or "deny".
        reason: Human-readable explanation shown to the user.
    """
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }
    print(json.dumps(output))
    sys.exit(0)


def main() -> None:
    """Check if the target file is inside the frozen directory.

    If no freeze state file exists, exit silently (allow all).
    If the target file is inside the frozen directory, allow.
    If outside, deny with an explanation.
    """
    # No freeze active — allow everything
    if not FREEZE_STATE.exists():
        return

    # Read the frozen directory
    try:
        frozen_dir = FREEZE_STATE.read_text().strip()
    except Exception:
        return  # Can't read state — don't interfere

    if not frozen_dir:
        return  # Empty state file — allow all

    frozen_path = Path(frozen_dir).resolve()

    # Parse tool input from stdin
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return  # Can't parse — don't interfere

    tool_input = input_data.get("tool_input", {})

    # Get the target file path from the tool input
    # Edit uses "file_path", Write uses "file_path"
    target_file = tool_input.get("file_path", "")
    if not target_file:
        return  # No file path in input — allow (shouldn't happen)

    target_path = Path(target_file).resolve()

    # Check if the target is inside the frozen directory
    try:
        target_path.relative_to(frozen_path)
        # Inside the frozen directory — allow
        make_decision("allow", f"Inside frozen directory: {frozen_dir}")
    except ValueError:
        # Outside the frozen directory — deny
        make_decision(
            "deny",
            f"Blocked: editing outside frozen directory ({frozen_dir}). "
            f"Target: {target_file}. Use /unfreeze to remove restriction.",
        )


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # On any error, exit silently — don't block normal operation
        sys.exit(0)
