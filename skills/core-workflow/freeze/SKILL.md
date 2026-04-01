---
name: freeze
description: "Restrict file editing to a single directory for the session. Blocks Edit and Write operations outside the boundary. Useful for focused debugging or working on a specific module without accidentally modifying unrelated code. Pairs well with /investigate."
user-invocable: true
allowed-tools:
  - Bash
  - AskUserQuestion
---

# /freeze: Directory-Scoped Edit Restriction

Restricts all file modifications (Edit, Write) to a single directory for the remainder of the session. Read-only operations (Read, Grep, Glob, Bash) still work everywhere.

**Origin**: Adapted from Garry Tan's g-stack `/freeze` skill. Prevents accidental modifications to code outside the area you're actively working on.

## When to Use

- Debugging a specific module — prevents fixing symptoms in the wrong file
- Working on a shared codebase — confine your changes to your area
- During `/investigate` — focus edits on the component being debugged
- When touching production-adjacent code — limit blast radius

## Workflow

1. **Parse the user's input** for a directory path. If not provided, ask:

> "Which directory should I restrict edits to? Everything outside this path will be read-only."

2. **Resolve to absolute path** using `realpath` or equivalent.

3. **Write the boundary** to the state file:
```bash
echo "/absolute/path/to/directory" > ~/.claude/.freeze-dir.txt
```

4. **Confirm activation**:
```
/freeze — Edit Restriction Active
────────────────────────────────────
Edits restricted to: /absolute/path/to/directory
Read/search: unrestricted (everywhere)

To remove: run /unfreeze
────────────────────────────────────
```

## How It Works

The `freeze-boundary.py` hook (registered as a PreToolUse hook for Edit and Write) checks:
1. Does `~/.claude/.freeze-dir.txt` exist?
2. If yes, is the target file inside the frozen directory?
3. If outside → deny with explanation. If inside → allow.

## Important Rules

1. **Always resolve to absolute path** before saving — relative paths would break across directory changes.
2. **The state file persists until removed** — it survives within a session but a new session starts clean (the hook allows all if no state file exists).
3. **Bash is NOT restricted** — only Edit and Write tools are checked. The user can still `echo > file` via Bash if they really need to. This is intentional — `/freeze` prevents *accidental* edits, not determined ones.
4. **Works with `/guard`** — guard activates freeze + careful together.

Follow the AskUserQuestion format (see CLAUDE.md Pi-Stack Conventions) for all interactive questions.

## Completion

End with status: **DONE**
