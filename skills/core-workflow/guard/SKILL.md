---
name: guard
description: "Maximum safety mode — combines /careful (destructive command warnings) and /freeze (directory-scoped editing) in one command. Recommended when working on shared lab pipelines, production data, or high-stakes code."
user-invocable: true
allowed-tools:
  - Bash
  - AskUserQuestion
---

# /guard: Maximum Safety Mode

Activates both `/careful` protection and `/freeze` directory restriction in one command. This is the "I'm touching something important and I don't want to break anything" mode.

**Origin**: Adapted from Garry Tan's g-stack `/guard` skill.

## When to Use

- Working on shared lab pipelines that others depend on
- Debugging production data processing code
- Touching code that runs on expensive compute (HPC, cloud)
- Any time the blast radius of a mistake would be high

## Workflow

1. **Ask for the directory to freeze**:

> "Which directory should edits be restricted to? (Everything outside will be read-only for this session.)"

2. **Activate /freeze** — write the directory to `~/.claude/.freeze-dir.txt`:
```bash
realpath "{user_input}" > ~/.claude/.freeze-dir.txt
```

3. **Confirm both protections are active**:

```
/guard — Maximum Safety Mode Active
──────────────────────────────────────────

DESTRUCTIVE COMMAND PROTECTION (/careful):
  Deny list: rm -rf, git push --force, git reset --hard, etc.
  Ask list:  rm, git push, pip uninstall, DROP TABLE, etc.
  Hook: ~/.claude/hooks/validate-bash-command.py

DIRECTORY RESTRICTION (/freeze):
  Edits restricted to: {absolute_path}
  Read/search: unrestricted
  Hook: ~/.claude/hooks/freeze-boundary.py

To deactivate: run /unfreeze (removes directory restriction)
Destructive command protection remains active (always on).
──────────────────────────────────────────
```

## Important Rules

1. **`/careful` is always on** — the deny/ask patterns in settings.json are permanent. `/guard` just makes the user aware of them.
2. **`/freeze` is the session-specific part** — `/unfreeze` removes the directory restriction but leaves `/careful` patterns in place.
3. **Read the actual settings.json** to display current deny/ask patterns — don't hardcode the list.

Follow the AskUserQuestion format (see CLAUDE.md Pi-Stack Conventions) for all interactive questions.

## Completion

End with status: **DONE**
