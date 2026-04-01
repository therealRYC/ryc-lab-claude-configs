#!/usr/bin/env python3
# Created: 2026-02-23
# Last updated: 2026-03-21 — Safe-path exceptions for rm commands (/careful)

"""
PreToolUse hook for Bash commands in Claude Code.

Implements "safe YOLO" permission logic:
  1. Check for pipe-to-shell patterns (curl|bash) → deny
  2. Split command into parts (handles &&, ||, ;, |)
  3. For each part: deny > ask > auto-approve

The key insight: instead of maintaining a growing allowlist, we flip the
model to "allow by default" with focused deny and ask lists. The deny list
catches destructive/dangerous commands. The ask list catches commands that
need user confirmation (pushes, deletes, etc.). Everything else auto-approves.

The allow list in settings.json is kept but only used as documentation/fallback
if this hook is ever disabled.

Output protocol (JSON on stdout):
  - {"hookSpecificOutput": {"permissionDecision": "allow", ...}}  → auto-approve
  - {"hookSpecificOutput": {"permissionDecision": "deny", ...}}   → block
  - {"hookSpecificOutput": {"permissionDecision": "ask", ...}}    → prompt user
  - (no output)                                                    → defer to normal system
"""

import sys
import json
import re
import fnmatch
import subprocess
from pathlib import Path

# Branches where direct commits should require user confirmation
PROTECTED_BRANCHES = {"main", "master"}

# Directories where rm -rf is safe because contents are rebuildable.
# If ALL targets of an rm command are inside these paths, the deny rule
# is bypassed and the command is auto-approved.
#
# Two categories:
#   1. Git repos that can be re-cloned from remote
#   2. Build/cache artifacts that are regenerated automatically
_HOME = Path.home()
SAFE_RM_DIRS: list[Path] = [
    # Git repo clones (re-cloneable from remote)
    _HOME / ".claude-config-repo",
    # Python build/cache artifacts
    Path("__pycache__"),       # relative — matches anywhere
    Path(".pytest_cache"),
    Path(".ruff_cache"),
    Path(".mypy_cache"),
    Path("htmlcov"),
    Path("dist"),
    Path("build"),
    Path(".eggs"),
    # Pipeline temp directories
    Path(".snakemake"),
    Path(".nextflow"),
    Path("work"),              # nextflow work dir
    # Bioinformatics rebuildable indices
    # (handled by suffix check in is_rebuildable_index, not here)
    # JS/Node build artifacts
    Path("node_modules"),
    Path(".next"),
    Path(".turbo"),
    Path("coverage"),
]

# File extensions that are rebuildable index files (can always be safely deleted)
REBUILDABLE_INDEX_SUFFIXES = {".fai", ".bai", ".tbi", ".idx"}


def load_permissions() -> tuple[list[str], list[str], list[str]]:
    """Load Bash allow/deny/ask patterns from settings.json.

    Reads the permissions object and extracts patterns from each section,
    stripping the "Bash(...)" wrapper.

    Returns:
        Tuple of (allow_patterns, deny_patterns, ask_patterns).
        Each list contains bare command patterns like "git push *".
    """
    settings_path = Path.home() / ".claude" / "settings.json"
    with open(settings_path) as f:
        settings = json.load(f)

    perms = settings.get("permissions", {})
    allow = []
    deny = []
    ask = []

    # Helper to strip the Bash(...) wrapper from a pattern
    def extract_bash_patterns(section_name: str) -> list[str]:
        """Extract bare command patterns from a permissions section.

        Args:
            section_name: Key in the permissions object ("allow", "deny", "ask").

        Returns:
            List of command patterns with "Bash(" prefix and ")" suffix removed.
        """
        patterns = []
        for pattern in perms.get(section_name, []):
            if pattern.startswith("Bash(") and pattern.endswith(")"):
                patterns.append(pattern[5:-1])  # Strip "Bash(" and ")"
        return patterns

    allow = extract_bash_patterns("allow")
    deny = extract_bash_patterns("deny")
    ask = extract_bash_patterns("ask")

    return allow, deny, ask


def detect_pipe_to_shell(cmd: str) -> bool:
    """Check if a command pipes a download into a shell interpreter.

    Catches patterns like:
      - curl https://example.com | bash
      - wget -O- url | sh
      - curl url | sudo bash

    These are dangerous because they execute arbitrary remote code.

    Args:
        cmd: The full command string (before splitting).

    Returns:
        True if a pipe-to-shell pattern is detected.
    """
    # Pattern: (curl|wget) ... | ... (bash|sh|zsh|dash|sudo)
    # The \s*\|+\s* handles both | and || (though || is logical-or,
    # better safe than sorry — the user can always run it manually)
    pattern = r"(curl|wget)\s+.*\|\s*(sudo\s+)?(bash|sh|zsh|dash|python[23]?|perl|ruby)"
    return bool(re.search(pattern, cmd, re.IGNORECASE))


def split_compound_command(cmd: str) -> list[str]:
    """Split a compound command on &&, ||, ;, | while respecting quotes.

    Handles:
      - Single and double quotes (operators inside quotes are not split on)
      - $() subshell nesting (operators inside subshells are not split on)
      - Backtick subshells

    Args:
        cmd: The full compound command string.

    Returns:
        List of individual command strings, whitespace-stripped.
    """
    parts = []
    current = ""
    i = 0
    in_single_quote = False
    in_double_quote = False
    subshell_depth = 0  # Nesting level for $() and ()
    in_backtick = False

    while i < len(cmd):
        char = cmd[i]

        # --- Track quoting state ---
        if char == "'" and not in_double_quote and not in_backtick:
            in_single_quote = not in_single_quote
            current += char
            i += 1
            continue

        if char == '"' and not in_single_quote and not in_backtick:
            in_double_quote = not in_double_quote
            current += char
            i += 1
            continue

        if char == "`" and not in_single_quote:
            in_backtick = not in_backtick
            current += char
            i += 1
            continue

        # --- Track subshell nesting ---
        if not in_single_quote and not in_backtick:
            if char == "(":
                subshell_depth += 1
                current += char
                i += 1
                continue
            if char == ")" and subshell_depth > 0:
                subshell_depth -= 1
                current += char
                i += 1
                continue

        # --- Split on operators (only outside quotes/subshells) ---
        if (
            not in_single_quote
            and not in_double_quote
            and not in_backtick
            and subshell_depth == 0
        ):
            # Two-character operators: && and ||
            if i + 1 < len(cmd) and cmd[i : i + 2] in ("&&", "||"):
                stripped = current.strip()
                if stripped:
                    parts.append(stripped)
                current = ""
                i += 2
                continue

            # Single-character operators: ; and |
            # (but not || which is caught above)
            if char == ";":
                stripped = current.strip()
                if stripped:
                    parts.append(stripped)
                current = ""
                i += 1
                continue

            if char == "|":
                stripped = current.strip()
                if stripped:
                    parts.append(stripped)
                current = ""
                i += 1
                continue

        current += char
        i += 1

    # Don't forget the last segment
    stripped = current.strip()
    if stripped:
        parts.append(stripped)

    return parts


def clean_for_matching(cmd: str) -> str:
    """Strip redirections and leading env-var assignments from a command.

    This normalizes commands so they can be matched against permission
    patterns. For example:
      "VAR=1 grep -r 'foo' dir 2>/dev/null" → "grep -r 'foo' dir"

    Args:
        cmd: A single command string (not compound).

    Returns:
        The cleaned command string.
    """
    # Remove redirections: 2>/dev/null, >/file, 2>&1, </input, etc.
    cleaned = re.sub(r"\d*>[>&]?\s*\S+", "", cmd)
    cleaned = re.sub(r"<\s*\S+", "", cleaned)

    # Remove leading env-var assignments: VAR=value VAR2="value" ...
    # These are NAME=VALUE pairs before the actual command
    cleaned = re.sub(r"^(\s*\w+=\S*\s+)+", "", cleaned)

    return cleaned.strip()


def matches_any_pattern(cmd: str, patterns: list[str]) -> bool:
    """Check if a command matches any glob pattern from the permission list.

    Handles three cases:
      1. Direct match:  "git status" matches "git status"
      2. Glob match:    "git log --oneline" matches "git log *"
      3. Bare command:  "sort" (no args, e.g. in a pipeline) matches "sort *"
         This works by checking if the command name + a dummy arg would match.

    Args:
        cmd: The cleaned command string.
        patterns: List of glob patterns to match against.

    Returns:
        True if any pattern matches.
    """
    for pattern in patterns:
        if fnmatch.fnmatch(cmd, pattern):
            return True

    # Handle bare commands in pipelines (e.g., "sort" should match "sort *")
    # by testing whether the command name + a dummy argument would match
    first_word = cmd.split()[0] if cmd.split() else cmd
    for pattern in patterns:
        # "sort x" matches "sort *" → means "sort" is an allowed command
        if fnmatch.fnmatch(first_word + " x", pattern):
            return True
        # Also check exact match on first word (for patterns like "env")
        if fnmatch.fnmatch(first_word, pattern):
            return True

    return False


def extract_rm_targets(cmd: str) -> list[str] | None:
    """Extract file/directory targets from an rm command.

    Parses the command to find arguments that aren't flags (don't start
    with -). Returns None if the command is not an rm command.

    Args:
        cmd: A cleaned single command string.

    Returns:
        List of target paths if this is an rm command, None otherwise.
    """
    parts = cmd.split()
    if not parts or parts[0] != "rm":
        return None

    targets = []
    for part in parts[1:]:
        # Skip flags (-f, -r, -rf, --force, etc.)
        if part.startswith("-"):
            continue
        # Expand ~ and $HOME to actual home directory
        expanded = part.replace("~", str(Path.home()))
        expanded = expanded.replace("$HOME", str(Path.home()))
        targets.append(expanded)

    return targets


def is_inside_safe_dir(target: str) -> bool:
    """Check if a path is inside any of the safe rm directories.

    Handles both absolute and relative safe dirs:
      - Absolute (e.g., ~/.claude-config-repo): target must be inside it
      - Relative (e.g., __pycache__): any path component can match

    Also checks for rebuildable index file suffixes (.fai, .bai, .tbi).

    Args:
        target: The file or directory path to check.

    Returns:
        True if the target is inside a safe directory or is a rebuildable file.
    """
    target_path = Path(target)

    # Check rebuildable index suffixes (e.g., *.fai, *.bai)
    # Handle glob patterns like *.fai by checking the pattern itself
    for suffix in REBUILDABLE_INDEX_SUFFIXES:
        if target.endswith(suffix):
            return True

    for safe_dir in SAFE_RM_DIRS:
        if safe_dir.is_absolute():
            # Absolute safe dir: target must start with this path
            # Resolve to handle symlinks, but also check string prefix
            # for glob patterns (e.g., ~/.claude-config-repo/claude/skills/*)
            safe_str = str(safe_dir)
            if target.startswith(safe_str + "/") or target == safe_str:
                return True
        else:
            # Relative safe dir: any path component can match
            # e.g., __pycache__ matches /any/path/__pycache__ or __pycache__/*
            safe_name = str(safe_dir)
            # Check if safe_name appears as a directory component
            if f"/{safe_name}/" in target or f"/{safe_name}" == target[-len(f"/{safe_name}"):]:
                return True
            # Also match if the target starts with the safe name (bare relative path)
            if target == safe_name or target.startswith(safe_name + "/"):
                return True

    return False


def rm_targets_all_safe(cmd: str) -> bool:
    """Check if an rm command only targets safe (rebuildable) paths.

    Returns True only if:
      1. The command IS an rm command
      2. It has at least one target (not just flags)
      3. ALL targets are inside safe directories

    If any single target is not in a safe directory, returns False
    and the normal deny/ask logic applies.

    Args:
        cmd: A cleaned single command string.

    Returns:
        True if all rm targets are in safe directories.
    """
    targets = extract_rm_targets(cmd)
    if targets is None:
        return False  # Not an rm command
    if not targets:
        return False  # No targets found (just flags?) — don't bypass

    return all(is_inside_safe_dir(t) for t in targets)


def make_decision(decision: str, reason: str) -> None:
    """Print a hook decision as JSON and exit.

    Args:
        decision: One of "allow", "deny", or "ask".
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


def check_commit_on_protected_branch(parts: list[str]) -> str | None:
    """Check if any command part is a git commit on a protected branch.

    Only runs `git branch --show-current` when the command actually contains
    a git commit — so no subprocess overhead on normal commands.

    Args:
        parts: List of individual command strings from split_compound_command().

    Returns:
        A reason string if the commit should require confirmation, None otherwise.
    """
    has_commit = any(
        re.match(r"git\s+commit", clean_for_matching(part))
        for part in parts
    )
    if not has_commit:
        return None

    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True, text=True, timeout=5,
        )
        branch = result.stdout.strip()
    except Exception:
        return None  # Can't determine branch — don't block

    if branch in PROTECTED_BRANCHES:
        return (
            f"Committing directly to '{branch}'. "
            "Use a worktree or feature branch for new work."
        )
    return None


def main() -> None:
    """Entry point: read command from stdin, validate, emit decision.

    Decision priority for each command part:
      1. deny list match  → block entire command
      2. ask list match   → prompt user for entire command
      3. protected branch → prompt user for git commit on main/master
      4. everything else  → auto-approve

    For compound commands, the strictest result wins:
      deny > ask > allow
    """
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        # Can't parse input — don't interfere, let normal system handle it
        return

    command = input_data.get("tool_input", {}).get("command", "")
    if not command:
        return

    # --- Pre-split check: pipe-to-shell is always dangerous ---
    if detect_pipe_to_shell(command):
        make_decision(
            "deny",
            "Blocked: piping downloaded content into a shell interpreter is dangerous",
        )

    # --- Load permission lists ---
    # On failure, exit silently → falls back to settings.json rules
    try:
        _allow, deny_patterns, ask_patterns = load_permissions()
    except Exception:
        return

    # --- Split into parts and check each one ---
    parts = split_compound_command(command)

    # --- Protected branch check: git commit on main/master → ask ---
    branch_reason = check_commit_on_protected_branch(parts)
    if branch_reason:
        make_decision("ask", branch_reason)

    denied_parts = []
    asked_parts = []

    for part in parts:
        cleaned = clean_for_matching(part)
        if not cleaned:
            # Empty after cleaning (e.g., bare redirection) — safe to skip
            continue

        # Safe-path exception: if an rm command targets only rebuildable
        # directories (build artifacts, caches, re-cloneable repos), skip
        # the deny check and auto-approve. This lets /sync-config and
        # build scripts clean up without triggering /careful rules.
        if rm_targets_all_safe(cleaned):
            continue  # Auto-approve — all targets are safe

        # Deny list takes priority — if any part is denied, block the whole command
        if matches_any_pattern(cleaned, deny_patterns):
            denied_parts.append(cleaned)
            continue

        # Ask list — user confirmation needed
        if matches_any_pattern(cleaned, ask_patterns):
            asked_parts.append(cleaned)
            continue

        # Everything else: auto-approve (no action needed)

    # --- Final decision: strictest result wins ---
    if denied_parts:
        make_decision("deny", f"Blocked: '{denied_parts[0]}' matches a deny rule")
    elif asked_parts:
        preview = ", ".join(asked_parts[:3])
        suffix = f" (+{len(asked_parts) - 3} more)" if len(asked_parts) > 3 else ""
        make_decision("ask", f"Needs confirmation: {preview}{suffix}")
    else:
        # YOLO: everything auto-approved
        make_decision("allow", "Auto-approved")


if __name__ == "__main__":
    # Top-level exception handler: if anything goes wrong, exit silently.
    # This means the normal permission system takes over — safe degradation.
    try:
        main()
    except Exception:
        sys.exit(0)
