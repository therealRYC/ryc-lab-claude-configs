---
name: careful
description: "Show or toggle destructive command protection status. Lists what commands are blocked (deny) vs require confirmation (ask). Use when you want to check safety rules, temporarily adjust protection, or understand what's guarded."
user-invocable: true
allowed-tools:
  - Read
  - Bash
  - AskUserQuestion
---

# /careful: Destructive Command Protection

Shows the current state of destructive command protection. This protection is implemented via the `validate-bash-command.py` hook and the deny/ask patterns in `settings.json`.

**Origin**: Adapted from Garry Tan's g-stack `/careful` skill. In g-stack, this was a standalone hook; in pi-stack, it's merged into the existing `validate-bash-command.py` infrastructure.

## What It Does

When invoked, read `~/.claude/settings.json` and display the current protection status:

### Display Format

```
/careful — Destructive Command Protection
──────────────────────────────────────────

BLOCKED (deny):
  rm -rf, rm -r, git push --force, git reset --hard,
  git checkout -- ., git restore ., git clean -f,
  git branch -D, DROP DATABASE, TRUNCATE TABLE,
  kubectl delete namespace, docker system prune -a,
  dd if=, chmod 777, mkfs, shutdown, reboot, sudo

CONFIRM (ask):
  rm, rmdir, git push, git stash drop/clear,
  pip uninstall, conda remove, DROP TABLE,
  docker rm -f, docker stop, kubectl delete,
  gh repo delete, gh pr/issue close, gh pr merge

SAFE EXCEPTIONS (auto-approved even with rm):
  __pycache__, .pytest_cache, .snakemake, .nextflow,
  htmlcov, dist, build, node_modules, .cache, .turbo,
  *.fai, *.bai, *.tbi (rebuildable index files)

Hook: ~/.claude/hooks/validate-bash-command.py
Config: ~/.claude/settings.json → permissions.deny / permissions.ask
```

## Subcommands

| Input | Action |
|-------|--------|
| `/careful` | Show current protection status (default) |
| `/careful off` | Temporarily note that the user wants relaxed protection. Remind them this doesn't actually disable the hook — they need to manually override prompts. |
| `/careful check <command>` | Check what would happen if a specific command were run (deny/ask/allow) |

## Important Rules

1. **Read settings.json live** — don't rely on cached knowledge of what's in the deny/ask lists.
2. **Never modify settings.json directly** from this skill — if the user wants to change protection rules, guide them to do it manually or use `/update-config`.
3. **The safe exceptions list is maintained in `validate-bash-command.py`** — display it but note that changes require editing the hook script.
4. This is a **status display** skill, not a configuration tool.

Follow the AskUserQuestion format (see CLAUDE.md Pi-Stack Conventions) for all interactive questions.

## Completion

End with status: **DONE**
