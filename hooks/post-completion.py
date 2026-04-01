#!/usr/bin/env python3
"""post-completion.py — Stop hook for task completion summaries.

When Claude finishes a task that had a plan, this hook blocks and
instructs Claude to create a completion summary comparing the
original plan with what actually happened.

Guard checks (all must pass to block):
  1. stop_hook_active is False (prevent infinite loop)
  2. Inside a git repo
  3. .claude-pending-completion marker exists (plan was made this session)
  4. NOTEBOOK.md exists (notebook-tracked project)
  5. Meaningful implementation work happened (not just plan/notebook commits)

Created by plan-mode-exit.sh writing a .claude-pending-completion marker.
The marker is deleted by Claude after writing the completion summary.
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def git(*args: str) -> str | None:
    """Run a git command and return stdout, or None on failure."""
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def main() -> None:
    """Run guard checks and block with instructions if all pass."""
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        hook_input = {}

    # Guard 1: Don't block if already blocked (prevent infinite loop)
    if hook_input.get("stop_hook_active", False):
        sys.exit(0)

    # Guard 2: Must be in a git repo
    project = os.environ.get("CLAUDE_PROJECT_DIR", ".")
    try:
        os.chdir(project)
    except OSError:
        sys.exit(0)

    if git("rev-parse", "--is-inside-work-tree") is None:
        sys.exit(0)

    # Guard 3: Marker file must exist (plan was made this session)
    marker = Path(project) / ".claude-pending-completion"
    if not marker.exists():
        sys.exit(0)

    # Guard 3b: Auto-cleanup — if a notebook commit was made AFTER the
    # marker was created, the completion summary was already written.
    # Delete the marker and allow stop. This prevents the hook from
    # repeatedly blocking after Claude writes the summary but forgets
    # to delete the marker.
    marker_mtime = marker.stat().st_mtime
    notebook_log = git(
        "log", "--oneline", "--format=%ct", "--grep=^notebook:", "-1",
    )
    if notebook_log:
        try:
            last_notebook_commit_time = int(notebook_log.strip())
            if last_notebook_commit_time > marker_mtime:
                # Completion was written — clean up and allow stop
                marker.unlink(missing_ok=True)
                sys.exit(0)
        except (ValueError, OSError):
            pass  # If parsing fails, fall through to normal blocking

    # Guard 4: NOTEBOOK.md must exist
    notebook = Path(project) / "NOTEBOOK.md"
    if not notebook.exists():
        sys.exit(0)

    # Guard 5: Must have meaningful implementation work
    # Count all recent commits
    total_log = git("log", "--oneline", "--since=8 hours ago")
    total_count = len(total_log.splitlines()) if total_log else 0

    # Count plan/notebook-only commits (these don't count as implementation)
    plan_log = git(
        "log", "--oneline", "--since=8 hours ago",
        "--grep=^plan:", "--grep=^notebook:",
    )
    plan_count = len(plan_log.splitlines()) if plan_log else 0

    # Count uncommitted changes
    status = git("status", "--porcelain")
    has_changes = len(status.splitlines()) if status else 0

    impl_count = total_count - plan_count
    if impl_count <= 0 and has_changes == 0:
        sys.exit(0)

    # Find the most recent plan file
    plans_dir = Path(project) / "Plans"
    plan_files = sorted(
        plans_dir.glob("*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    ) if plans_dir.exists() else []
    plan_file = str(plan_files[0]) if plan_files else "(no plan file found in Plans/)"

    # All guards passed — build instructions and block
    instructions = f"""\
═══════════════════════════════════════════════════════
 TASK COMPLETE — COMPLETION SUMMARY REQUIRED
═══════════════════════════════════════════════════════

Before stopping, complete ALL of the following:

1. READ THE PLAN → {plan_file}
   Compare what was planned vs. what actually happened.

2. PRINT A COMPLETION SUMMARY to the console:

   ═══════════════════════════════════════════════════
     COMPLETION SUMMARY: {{title}}
   ═══════════════════════════════════════════════════

     WHAT WAS DONE
     ─────────────
     - {{bullet points of completed work}}

     PLAN DEVIATIONS
     ───────────────
     - {{what didn't go as planned and why}}
     - "None — plan was followed as written" if no deviations

     BUGS & FIX ATTEMPTS
     ───────────────────
     - {{Bug}}: Tried {{X}} → {{outcome}}. Final: {{Y}} ({{why}})
     - "None encountered" if clean execution

     FINAL SOLUTIONS & KEY DECISIONS
     ───────────────────────────────
     - {{what worked and WHY it was the right approach}}
     - {{key technical decisions made during implementation}}

   ═══════════════════════════════════════════════════

3. NOTEBOOK ENTRY → invoke the notebook skill with type: completion
   Include all details from the summary above.

4. DELETE MARKER → rm {marker}

5. AUTO-COMMIT → git add NOTEBOOK.md && git commit -m "notebook: Completion — {{topic}}"

Complete all 5 steps, then you may stop.
═══════════════════════════════════════════════════════"""

    # Output blocking decision as JSON to stdout (Stop hook format)
    # - decision: "block" prevents Claude from stopping
    # - reason: short explanation shown as feedback
    # - additionalContext: detailed instructions injected into Claude's context
    output = {
        "decision": "block",
        "reason": "Completion summary required before stopping — a plan was executed this session.",
        "additionalContext": instructions,
    }
    print(json.dumps(output))

    # Exit 0 — the decision is in the JSON, not the exit code
    sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # On any error, exit cleanly — never block Claude due to a hook bug
        sys.exit(0)
