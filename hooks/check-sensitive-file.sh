#!/bin/bash
# Created: 2026-02-23
# Last updated: 2026-03-01 — Fix output to use correct hook protocol (permissionDecision)

# PreToolUse hook for Edit|Write events.
# Reads JSON from stdin, extracts the file path, and checks it against
# sensitive patterns. Uses the Claude Code hook protocol:
#   (no output)              — defer to normal permission system (acceptEdits auto-approves)
#   permissionDecision: ask  — prompt the user for confirmation
#   permissionDecision: deny — hard block, cannot be overridden
#
# .env / credentials / keys / lock files → ask (user can override)
# .git/ internals → deny (never legitimate to hand-edit)
# Everything else → no output (auto-approved by acceptEdits mode)

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

# If we can't parse the path, stay silent — don't block on hook failure
if [[ -z "$FILE_PATH" ]]; then
    exit 0
fi

# Helper: emit a hook decision and exit
# Usage: decide "ask"|"deny" "reason string"
decide() {
    local decision="$1"
    local reason="$2"
    printf '{"hookSpecificOutput":{"permissionDecision":"%s","permissionDecisionReason":"%s"}}\n' "$decision" "$reason"
    exit 0
}

# Extract just the filename for basename checks
FILENAME=$(basename "$FILE_PATH")

# --- .git internals → hard deny (editing these corrupts the repo) ---
if [[ "$FILE_PATH" == */.git/* ]]; then
    decide "deny" "Blocked: $FILE_PATH is inside .git/. Editing git internals can corrupt the repository."
fi

# --- Environment / secret files → ask ---
if [[ "$FILENAME" == .env || "$FILENAME" == .env.* || "$FILENAME" == *.env ]]; then
    decide "ask" "Environment file detected: $FILENAME. These often contain secrets."
fi

if [[ "$FILENAME" == credentials* || "$FILENAME" == *secret* || "$FILENAME" == *credential* ]]; then
    decide "ask" "Possible credentials file: $FILENAME."
fi

# --- Private keys → ask ---
if [[ "$FILENAME" == *.pem || "$FILENAME" == *.key || "$FILENAME" == id_rsa* || "$FILENAME" == id_ed25519* ]]; then
    decide "ask" "Private key file detected: $FILENAME."
fi

# --- Lock files (auto-generated, shouldn't be hand-edited) → ask ---
if [[ "$FILENAME" == package-lock.json || "$FILENAME" == poetry.lock || "$FILENAME" == Pipfile.lock || "$FILENAME" == yarn.lock || "$FILENAME" == Gemfile.lock || "$FILENAME" == renv.lock ]]; then
    decide "ask" "Lock file detected: $FILENAME. These are auto-generated."
fi

# --- All checks passed: no output → defer to acceptEdits mode ---
exit 0
