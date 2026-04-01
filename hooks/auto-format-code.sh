#!/bin/bash
# Created: 2026-02-23
# Last updated: 2026-02-23 — Use jq for JSON parsing

# Auto-format hook for Claude Code PostToolUse events (Edit|Write).
# Reads JSON from stdin to get the file path, then formats:
#   - Python files (.py) with ruff (preferred) or black (fallback)
#   - R files (.R, .r, .Rmd) with styler::style_file()
#
# Exits 0 always — formatting failures should never block Claude.

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Exit early if no file path was provided
if [[ -z "$FILE_PATH" || ! -f "$FILE_PATH" ]]; then
    exit 0
fi

# Format Python files
if [[ "$FILE_PATH" == *.py ]]; then
    if command -v ruff &>/dev/null; then
        ruff format "$FILE_PATH" 2>/dev/null || true
    elif command -v black &>/dev/null; then
        black -q "$FILE_PATH" 2>/dev/null || true
    fi
fi

# Format R files (.R, .Rmd, .r)
if [[ "$FILE_PATH" == *.R || "$FILE_PATH" == *.r || "$FILE_PATH" == *.Rmd ]]; then
    if command -v Rscript &>/dev/null; then
        Rscript -e "styler::style_file('$FILE_PATH')" 2>/dev/null || true
    fi
fi

exit 0
