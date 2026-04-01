#!/usr/bin/env python3
"""PostToolUse hook for the Skill tool — verifies pi-stack handoff state.

After the Skill tool returns from invoking pi-stack, this hook reads
.pi-stack.json and warns if phases aren't in a terminal state. This catches
handoff failures that the scripts can't prevent (e.g., pi-stack erroring out
mid-pipeline without updating state).

This hook NEVER blocks — it only adds context warnings. For all non-pi-stack
Skill invocations, it exits silently.

Output protocol (JSON on stdout):
  - No output → silent pass (most invocations)
  - {"hookSpecificOutput": {"message": "..."}} → warning injected into context
"""

import json
import os
import sys
from pathlib import Path

TERMINAL_STATUSES = {"done", "skipped"}


def main() -> None:
    try:
        # Read hook input from stdin
        hook_input = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        # Can't parse input — exit silently, don't block
        sys.exit(0)

    # Only care about Skill tool calls for pi-stack
    tool_name = hook_input.get("tool_name", "")
    if tool_name != "Skill":
        sys.exit(0)

    # Check if this was a pi-stack invocation
    tool_input = hook_input.get("tool_input", {})
    skill_name = tool_input.get("skill", "")
    if skill_name != "pi-stack":
        sys.exit(0)

    # Find the project directory
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")).resolve()
    state_path = project_dir / ".pi-stack.json"

    if not state_path.exists():
        # No state file after pi-stack ran — this might be normal
        # (standalone mode deletes it on completion) or a problem
        # (orchestrated mode should keep it). Don't warn — the
        # verify_pi_stack_completion.py script will catch this.
        sys.exit(0)

    # Read state and check for non-terminal phases
    try:
        state = json.loads(state_path.read_text())
    except json.JSONDecodeError:
        # Corrupt state file — warn
        output = {
            "hookSpecificOutput": {
                "message": "WARNING: .pi-stack.json exists but is not valid JSON. "
                "The pi-stack handoff may have failed mid-write."
            }
        }
        print(json.dumps(output))
        sys.exit(0)

    phases = state.get("phases", {})
    invocation_mode = state.get("invocation_mode", "standalone")

    # In orchestrated mode, all phases should be terminal after pi-stack completes
    if invocation_mode == "orchestrated":
        non_terminal = [
            f"{name}: {phase.get('status', 'missing')}"
            for name, phase in phases.items()
            if phase.get("status") not in TERMINAL_STATUSES
        ]

        if non_terminal:
            output = {
                "hookSpecificOutput": {
                    "message": (
                        f"WARNING: Pi-stack completed in orchestrated mode but "
                        f"{len(non_terminal)} phases are not terminal: "
                        f"{', '.join(non_terminal)}. "
                        f"Run verify_pi_stack_completion.py to diagnose."
                    )
                }
            }
            print(json.dumps(output))

    # In standalone mode, state file existing is fine (user is mid-pipeline)
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Never crash — hooks must degrade gracefully
        sys.exit(0)
