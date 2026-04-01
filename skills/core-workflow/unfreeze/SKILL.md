---
name: unfreeze
description: "Remove the edit restriction set by /freeze, restoring ability to edit files in any directory."
user-invocable: true
allowed-tools:
  - Bash
---

# /unfreeze: Remove Edit Restriction

Removes the directory-scoped edit restriction set by `/freeze`.

## Workflow

1. **Check for state file**:
```bash
cat ~/.claude/.freeze-dir.txt 2>/dev/null
```

2. **If state file exists**: Remove it and confirm:
```
/unfreeze — Edit Restriction Removed
────────────────────────────────────
Previously restricted to: {directory}
Edits now: unrestricted (all directories)
────────────────────────────────────
```

3. **If no state file**: Report that no restriction is active:
```
No /freeze restriction is currently active. Edits are unrestricted.
```

4. **Remove the state file**:
```bash
rm -f ~/.claude/.freeze-dir.txt
```

## Completion

End with status: **DONE**
