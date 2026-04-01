#!/usr/bin/env bash
# plan-mode-exit.sh — PostToolUse hook for ExitPlanMode
#
# Fires after ExitPlanMode is called. Creates Plans/ directory
# and injects strict instructions so the model saves the plan,
# creates a notebook entry, renames the session, and commits.
#
# Session rename: reads .claude-session-name (written by Claude
# before exiting plan mode, per CLAUDE.md rules) and appends "-code".

# Determine project directory (CLAUDE_PROJECT_DIR is set by Claude Code)
PROJECT="${CLAUDE_PROJECT_DIR:-.}"

# Create Plans/ directory if it doesn't exist
mkdir -p "$PROJECT/Plans"

# Create marker file for post-completion hook
# Signals that a plan was made and a completion summary will be needed
# when Claude finishes the task. Deleted by Claude after writing the summary.
echo "$(date '+%Y-%m-%d %H:%M')" > "$PROJECT/.claude-pending-completion"

DATE=$(date '+%Y-%m-%d')
SHORTDATE=$(date '+%y%m%d')

# Read persisted session name (written by Claude before exiting plan mode)
SESSION_NAME=""
if [ -f "$PROJECT/.claude-session-name" ]; then
    SESSION_NAME=$(cat "$PROJECT/.claude-session-name")
fi

# Build the rename instruction
if [ -n "$SESSION_NAME" ]; then
    RENAME_INSTRUCTION="1. RENAME SESSION → /rename ${SESSION_NAME}-code
   - The planning session was named \"${SESSION_NAME}\"
   - Append \"-code\" to mark this as the implementation session"
else
    RENAME_INSTRUCTION="1. RENAME SESSION → /rename ${SHORTDATE}-<plan-topic>-code
   - No session name was persisted. Derive from the plan topic.
   - Example: /rename ${SHORTDATE}-fitness-pipeline-code"
fi

cat <<EOF
═══════════════════════════════════════════════════════
 PLAN MODE EXIT — REQUIRED ACTIONS (DO NOT SKIP)
═══════════════════════════════════════════════════════

You just exited plan mode. Complete ALL of the following
before doing ANYTHING else:

${RENAME_INSTRUCTION}

2. SAVE THE PLAN → Plans/${DATE}_<brief-description>.md
   - Use kebab-case for the description (e.g., add-auth-middleware)
   - Include: goal, approach, subtasks with full detail
   - Add a dependency graph (Mermaid or ASCII) if 3+ subtasks
   - Plans/ directory is ready at: ${PROJECT}/Plans

3. NOTEBOOK ENTRY → invoke the notebook skill with type: plan
   - Format: "Plan: {title} — {1-2 sentence summary of scope
     and approach}. See [full plan](Plans/${DATE}_....md)."
   - The notebook entry is just a pointer — all detail is in
     the plan file.

4. AUTO-COMMIT both files immediately
   - Stage: the plan file AND NOTEBOOK.md
   - Commit message format: "plan: {Brief title}"
   - Do NOT batch with other unrelated changes

5. CLEAN UP → rm ${PROJECT}/.claude-session-name (if it exists)

DO NOT begin implementation until all 5 steps are complete.
═══════════════════════════════════════════════════════
EOF
