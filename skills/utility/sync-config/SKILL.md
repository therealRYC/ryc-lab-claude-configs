<!-- Created: 2026-03-08 -->
<!-- Last updated: 2026-03-29 — Migrated find-skills/tdd from symlinks to regular skills, removed all external skills complexity -->

---
name: sync-config
description: "Sync Claude Code configuration across machines via a private GitHub repo. Use when: the user says 'sync config', 'push config', 'pull config', 'sync settings', or invokes /sync-config."
user-invocable: true
argument-hint: "[setup | push | pull | diff | status]"
---

# Sync Config

Synchronize Claude Code global configuration across machines using `[YOUR-GITHUB-HANDLE]/claude-config` as transport.

**Argument**: $ARGUMENTS

## Constants

- **Repo**: `[YOUR-GITHUB-HANDLE]/claude-config`
- **Local clone**: `~/.claude-config-repo`
- **Sync marker**: `~/.claude/.sync-config`
### File Inventory

Sync these from `~/.claude/` to `repo/claude/`:

| Source | Repo Path | Notes |
|---|---|---|
| `CLAUDE.md` | `claude/CLAUDE.md` | |
| `DESIGN.md` | `claude/DESIGN.md` | Only if exists |
| `README.md` | `claude/README.md` | |
| `settings.json` | `claude/settings.json` | |
| `keybindings.json` | `claude/keybindings.json` | Only if exists |
| `agents/*.md` | `claude/agents/` | All agent definitions |
| `hooks/*` | `claude/hooks/` | Exclude `*.bak*` files |
| `skills/*/` | `claude/skills/` | All skills (including find-skills, tdd) |
| `commands/` | `claude/commands/` | All command files |
| `writing/` | `claude/writing/` | Voice profiles, templates, exemplars, calibration files |

### Excluded (never sync)

`.credentials.json`, `history.jsonl`, `debug/`, `file-history/`, `session-env/`,
`backups/`, `plugins/`, `tasks/`, `todos/`, `telemetry/`, `projects/`,
`shell-snapshots/`, `paste-cache/`, `settings.local.json`, `*.bak*`, `memory/`

## Parse Subcommand

Determine which subcommand to run from `$ARGUMENTS`:
- `setup` → Subcommand: setup
- `push` → Subcommand: push
- `pull` → Subcommand: pull
- `diff` → Subcommand: diff
- `status` → Subcommand: status
- Empty or unrecognized → Show usage:
  > **Usage**: `/sync-config <subcommand>`
  > - `setup` — Create or connect to the GitHub repo
  > - `push` — Export local config → repo → push
  > - `pull` — Pull repo → import to local
  > - `diff` — Show differences (local vs repo)
  > - `status` — Quick sync overview

## Pre-flight

Run these checks before any subcommand **except** `setup`:

1. **GitHub CLI authenticated**:
   ```bash
   gh auth status 2>&1
   ```
   If fails: "Run `gh auth login` first."

2. **Sync marker exists**:
   ```bash
   test -f ~/.claude/.sync-config
   ```
   If missing: "Run `/sync-config setup` first to initialize."

3. **Local clone exists**:
   ```bash
   test -d ~/.claude-config-repo/.git
   ```
   If missing: "Local clone not found. Run `/sync-config setup` to re-initialize."

## Subcommand: setup

Initialize the sync infrastructure.

1. **Check gh auth**:
   ```bash
   gh auth status 2>&1
   ```
   If fails, stop: "Run `gh auth login` first."

2. **Check if repo exists**:
   ```bash
   gh repo view [YOUR-GITHUB-HANDLE]/claude-config --json name 2>&1
   ```

3. **If repo doesn't exist, create it**:
   ```bash
   gh repo create [YOUR-GITHUB-HANDLE]/claude-config --private --description "Claude Code configuration sync"
   ```

4. **Clone or update local clone**:
   ```bash
   if [ -d ~/.claude-config-repo/.git ]; then
     git -C ~/.claude-config-repo pull --rebase 2>/dev/null || true
   else
     gh repo clone [YOUR-GITHUB-HANDLE]/claude-config ~/.claude-config-repo
   fi
   ```

5. **Create repo directory structure**:
   ```bash
   mkdir -p ~/.claude-config-repo/claude/{agents,hooks,skills,commands,writing}
   ```

6. **Write sync marker**:
   ```bash
   printf 'repo=[YOUR-GITHUB-HANDLE]/claude-config\nclone=%s/.claude-config-repo\nsetup_date=%s\nsetup_host=%s\n' \
     "$HOME" "$(date -Iseconds)" "$(hostname)" > ~/.claude/.sync-config
   ```

7. **Report**:
   > Setup complete. Repo: `[YOUR-GITHUB-HANDLE]/claude-config`. Clone: `~/.claude-config-repo`
   > Run `/sync-config push` to export your current config.

## Subcommand: push

Export local config to repo and push to GitHub.

### Step 1: Pre-flight

Run pre-flight checks.

### Step 2: Pull latest from remote

```bash
git -C ~/.claude-config-repo fetch origin 2>/dev/null
git -C ~/.claude-config-repo pull --rebase 2>/dev/null || true
```

### Step 2.5: Pre-push settings.json validation

Before copying settings.json to the repo, verify it hasn't been corrupted by `claude plugin` CLI operations:

```python
import json
from pathlib import Path

REQUIRED_KEYS = {"permissions", "hooks", "enabledPlugins"}
EXPECTED_KEYS = {"effortLevel", "defaultMode", "extraKnownMarketplaces"}

settings = json.loads((Path.home() / ".claude/settings.json").read_text())
missing_required = REQUIRED_KEYS - set(settings.keys())
missing_expected = EXPECTED_KEYS - set(settings.keys())

if missing_required:
    print(f"ABORT: settings.json missing required keys: {missing_required}")
    print("This likely means the file was corrupted. Do not push.")
    # Stop the push
elif missing_expected:
    print(f"WARNING: settings.json missing expected keys: {missing_expected}")
    print("These may have been stripped by 'claude plugin install/uninstall'.")
    print("Confirm before pushing — do you want to continue?")
    # Ask user to confirm
else:
    print("settings.json validation passed.")
```

If required keys are missing, abort the push. If expected keys are missing, warn and ask for confirmation.

### Step 3: Copy files to repo

**Root config files**:
```bash
cp ~/.claude/CLAUDE.md ~/.claude-config-repo/claude/CLAUDE.md
[ -f ~/.claude/DESIGN.md ] && cp ~/.claude/DESIGN.md ~/.claude-config-repo/claude/DESIGN.md
cp ~/.claude/README.md ~/.claude-config-repo/claude/README.md
cp ~/.claude/settings.json ~/.claude-config-repo/claude/settings.json
# keybindings.json only if it exists
[ -f ~/.claude/keybindings.json ] && cp ~/.claude/keybindings.json ~/.claude-config-repo/claude/keybindings.json
```

**Agents** (clear and re-copy to catch deletions):
```bash
rm -f ~/.claude-config-repo/claude/agents/*.md 2>/dev/null
cp ~/.claude/agents/*.md ~/.claude-config-repo/claude/agents/ 2>/dev/null
```

**Hooks** (exclude .bak files):
```bash
rm -f ~/.claude-config-repo/claude/hooks/* 2>/dev/null
for f in ~/.claude/hooks/*; do
  [ -e "$f" ] || continue
  case "$f" in *.bak*) continue ;; esac
  cp "$f" ~/.claude-config-repo/claude/hooks/
done
```

**Skills**:
```bash
rm -r ~/.claude-config-repo/claude/skills/*/ 2>/dev/null
for d in ~/.claude/skills/*/; do
  [ -e "$d" ] || continue
  skill_name=$(basename "$d")
  mkdir -p ~/.claude-config-repo/claude/skills/"$skill_name"
  cp -r "$d"* ~/.claude-config-repo/claude/skills/"$skill_name"/
done
```

**Commands**:
```bash
rm -f ~/.claude-config-repo/claude/commands/* 2>/dev/null
[ -d ~/.claude/commands ] && cp ~/.claude/commands/* ~/.claude-config-repo/claude/commands/ 2>/dev/null
touch ~/.claude-config-repo/claude/commands/.gitkeep
```

**Writing** (voice profiles, templates, exemplars, calibration files):
```bash
if [ -d ~/.claude/writing ]; then
  rm -r ~/.claude-config-repo/claude/writing 2>/dev/null
  mkdir -p ~/.claude-config-repo/claude/writing
  cp -r ~/.claude/writing/* ~/.claude-config-repo/claude/writing/
fi
```

### Step 4: Generate manifest.json

Create `~/.claude-config-repo/manifest.json` using Python:

```python
import json, hashlib, os, subprocess
from pathlib import Path
from datetime import datetime, timezone

repo = Path.home() / ".claude-config-repo"

# Compute file hashes for all synced files
file_hashes = {}
for root, dirs, files in os.walk(repo):
    root_path = Path(root)
    # Skip .git directory
    if ".git" in root_path.parts:
        continue
    for fname in files:
        fpath = root_path / fname
        rel = str(fpath.relative_to(repo))
        if rel in ("manifest.json", "README.md", "bootstrap.sh"):
            continue
        sha = hashlib.sha256(fpath.read_bytes()).hexdigest()
        file_hashes[rel] = sha

# Extract enabled plugins from settings.json
settings_path = Path.home() / ".claude" / "settings.json"
with open(settings_path) as f:
    settings = json.load(f)
plugins = [k for k, v in settings.get("enabledPlugins", {}).items() if v]

manifest = {
    "version": 1,
    "lastPushed": datetime.now(timezone.utc).isoformat(),
    "pushedFrom": {
        "hostname": subprocess.check_output(["hostname"], text=True).strip(),
        "username": os.environ.get("USER", "unknown"),
    },
    "enabledPlugins": plugins,
    "dependencies": {
        "system": ["jq", "gh"],
        "python": ["ruff"],
        "r": ["styler"],
    },
    "fileHashes": dict(sorted(file_hashes.items())),
}

with open(repo / "manifest.json", "w") as f:
    json.dump(manifest, f, indent=2)
    f.write("\n")

print(f"Manifest written: {len(file_hashes)} files tracked")
```

Run this as `python3 -c '...'` or write to a temp file and execute.

### Step 5: Generate repo README.md

Write `~/.claude-config-repo/README.md` with:
- Title: `# Claude Code Configuration`
- Description: Private config sync for Claude Code across WSL2 machines
- Bootstrap instructions: `gh repo clone [YOUR-GITHUB-HANDLE]/claude-config /tmp/cc && /tmp/cc/bootstrap.sh`
- File inventory summary (count agents, hooks, skills, commands)
- Last sync timestamp and hostname (from manifest)
- Enabled plugins list

### Step 6: Commit and push

```bash
cd ~/.claude-config-repo
git add -A
# Check if there are changes to commit
git diff --cached --quiet 2>/dev/null && echo "No changes to push." && exit 0
git commit -m "sync: push from $(hostname) at $(date '+%Y-%m-%d %H:%M')"
git push origin main
```

If git push fails because the remote branch doesn't exist yet (first push):
```bash
git push -u origin main
```

### Step 7: Report

Show summary:
- Files synced (count by category: N agents, N hooks, N skills, N commands)
- New or removed files since last push
- Commit SHA
- "Config pushed to `[YOUR-GITHUB-HANDLE]/claude-config`"

## Subcommand: pull

Import config from repo to local machine.

### Step 1: Pre-flight

Run pre-flight checks.

### Step 2: Fetch and check for updates

```bash
git -C ~/.claude-config-repo fetch origin
LOCAL=$(git -C ~/.claude-config-repo rev-parse HEAD)
REMOTE=$(git -C ~/.claude-config-repo rev-parse origin/main)
```

If `$LOCAL = $REMOTE`: "Already up to date. No changes to pull." (Stop here unless user forces.)

### Step 3: Conflict detection

Read manifest from the **local** copy (represents what was last pushed/pulled):
```bash
cat ~/.claude-config-repo/manifest.json
```

**Path mapping**: manifest paths use repo-relative paths. Map them to local:
- `claude/<path>` → `~/.claude/<path>`
- All other paths (e.g., `SYNC-GUIDE.md`) → **skip** (no local equivalent)

For each file in `fileHashes`:
1. **Map the path to local** using the rules above. If unmappable → **skip this file**
2. Compute the current local file's SHA-256:
   ```bash
   sha256sum ~/.claude/<relative-path>
   ```
   If the local file doesn't exist (e.g., new file on remote only) → not locally modified
3. Compare against the manifest hash (what was last synced)
4. If they differ → local was modified since last sync

Also check which files the remote changed:
```bash
git -C ~/.claude-config-repo diff HEAD..origin/main --name-only
```

A **conflict** exists when a file has BOTH:
- Local modification (local hash ≠ manifest hash)
- Remote modification (file appears in remote diff)

**Deletion conflicts**: Also check for files that are:
- **Deleted on remote** (present in manifest but absent from remote's file listing)
- **Modified locally** (local hash ≠ manifest hash)

These are deletion-conflicts: the remote wants to delete a file that the user modified locally.
Build a `keep_local` skip-list from conflict resolution to pass to Step 6.

### Step 4: Handle conflicts

For each conflicting file (both-modified conflicts only — not deletion-conflicts):

1. Show the diff:
   ```bash
   diff ~/.claude/<local-path> <(git -C ~/.claude-config-repo show origin/main:<repo-path>)
   ```

2. Ask the user: "File `<path>` changed both locally and remotely."
   - **(1) Keep local** — skip this file during pull → add to `keep_local` skip-list
   - **(2) Take remote** — overwrite local with remote version
   - **(3) Show diff** — display the full diff, then ask again

**Deletion-conflict prompt**: "File `<path>` was **deleted on remote** but **modified locally**."
   - **(1) Keep local** — preserve the local file, do not delete → add to `keep_local`
   - **(2) Delete** — remove the local file to match remote

**Special case — settings.json conflict**: Attempt a JSON-level merge:
- Union the `permissions.allow` arrays (deduplicate)
- Union the `permissions.deny` arrays (deduplicate)
- Union the `permissions.ask` arrays (deduplicate)
- Union the `enabledPlugins` objects (merge keys)
- For `hooks`, take the remote version with a warning
- Preserve local-only keys (`effortLevel`, `defaultMode`, etc.)
- Show the merged result and ask for confirmation before writing

### Step 4.5: Build keep_local skip-list

After conflict resolution, collect all files where the user chose "Keep local" into a skip-list.
This is a simple list of basenames (e.g., `deep-researcher.md`, `hook-a.sh`).
**Note:** Uses basenames only. In the unlikely event that an agent and a command share the same filename, keeping one protects the other from deletion too. Acceptable trade-off — false-keep is safer than false-delete.

```bash
# Example: keep_local=("deep-researcher.md" "my-hook.sh")
# Built from Step 4 conflict resolution choices
```

### Step 5: Pull and merge

```bash
git -C ~/.claude-config-repo pull --rebase origin main
```

### Step 6: Copy files from repo to local

**Important:** The `keep_local` skip-list from Step 4.5 controls which files are protected.
Before deleting any file, check if its basename is in `keep_local`. If so, skip it.

**Root config files** (copy if exists in repo, delete if removed from repo):
```bash
cp ~/.claude-config-repo/claude/CLAUDE.md ~/.claude/CLAUDE.md
cp ~/.claude-config-repo/claude/README.md ~/.claude/README.md
# settings.json — only if no conflict, or after conflict resolution
cp ~/.claude-config-repo/claude/settings.json ~/.claude/settings.json
# Optional files: copy if present, delete if removed from repo
for opt in DESIGN.md keybindings.json; do
  if [ -f ~/.claude-config-repo/claude/"$opt" ]; then
    cp ~/.claude-config-repo/claude/"$opt" ~/.claude/"$opt"
  elif [ -f ~/.claude/"$opt" ]; then
    rm ~/.claude/"$opt" && echo "Removed root config: $opt (deleted on remote)"
  fi
done
```

**Agents** (sync deletions: remove local agents not in repo, respect keep_local):
```bash
# Copy from repo to local
cp ~/.claude-config-repo/claude/agents/*.md ~/.claude/agents/ 2>/dev/null
# Remove local agents that were deleted on remote (skip keep_local)
for f in ~/.claude/agents/*.md; do
  [ -e "$f" ] || continue
  name=$(basename "$f")
  # Skip if user chose "Keep local" during conflict resolution
  [[ " ${keep_local[*]} " =~ " $name " ]] && continue
  [ ! -f ~/.claude-config-repo/claude/agents/"$name" ] && rm "$f" && echo "Removed agent: $name"
done
```

**Hooks** (sync deletions: remove local hooks not in repo, respect keep_local):
```bash
# Copy from repo to local
cp ~/.claude-config-repo/claude/hooks/* ~/.claude/hooks/ 2>/dev/null
chmod +x ~/.claude/hooks/*.sh ~/.claude/hooks/*.py 2>/dev/null
# Remove local hooks that were deleted on remote (skip .bak files + keep_local)
for f in ~/.claude/hooks/*; do
  [ -e "$f" ] || continue
  name=$(basename "$f")
  case "$name" in *.bak*) continue ;; esac
  [[ " ${keep_local[*]} " =~ " $name " ]] && continue
  [ ! -f ~/.claude-config-repo/claude/hooks/"$name" ] && rm "$f" && echo "Removed hook: $name"
done
```

**Skills** (sync deletions: remove local skill dirs not in repo, respect keep_local):
```bash
# Copy from repo to local
for d in ~/.claude-config-repo/claude/skills/*/; do
  [ -e "$d" ] || continue
  skill_name=$(basename "$d")
  mkdir -p ~/.claude/skills/"$skill_name"
  cp -r "$d"* ~/.claude/skills/"$skill_name"/
done
# Remove local skills that were deleted on remote (respect keep_local)
for d in ~/.claude/skills/*/; do
  [ -e "$d" ] || continue
  skill_name=$(basename "$d")
  [[ " ${keep_local[*]} " =~ " $skill_name " ]] && continue
  [ ! -d ~/.claude-config-repo/claude/skills/"$skill_name" ] && rm -r "$d" && echo "Removed skill: $skill_name"
done
```

**Commands** (sync deletions: remove local commands not in repo, respect keep_local):
```bash
mkdir -p ~/.claude/commands
# Copy from repo to local (skip .gitkeep)
for f in ~/.claude-config-repo/claude/commands/*; do
  [ -e "$f" ] || continue
  [ "$(basename "$f")" = ".gitkeep" ] && continue
  cp "$f" ~/.claude/commands/
done
# Remove local commands that were deleted on remote (skip keep_local)
for f in ~/.claude/commands/*; do
  [ -e "$f" ] || continue
  name=$(basename "$f")
  [[ " ${keep_local[*]} " =~ " $name " ]] && continue
  [ ! -f ~/.claude-config-repo/claude/commands/"$name" ] && rm "$f" && echo "Removed command: $name"
done
```

**Writing** (sync deletions: remove local writing subdirs not in repo, respect keep_local):
```bash
if [ -d ~/.claude-config-repo/claude/writing ]; then
  mkdir -p ~/.claude/writing
  # Copy from repo to local (recursive, preserving subdirectory structure)
  for d in ~/.claude-config-repo/claude/writing/*/; do
    [ -e "$d" ] || continue
    dir_name=$(basename "$d")
    mkdir -p ~/.claude/writing/"$dir_name"
    cp -r "$d"* ~/.claude/writing/"$dir_name"/
  done
  # Copy root-level files (e.g., data_reference.md)
  for f in ~/.claude-config-repo/claude/writing/*; do
    [ -f "$f" ] || continue
    cp "$f" ~/.claude/writing/
  done
  # Remove local writing subdirs that were deleted on remote (respect keep_local)
  for d in ~/.claude/writing/*/; do
    [ -e "$d" ] || continue
    dir_name=$(basename "$d")
    [[ " ${keep_local[*]} " =~ " $dir_name " ]] && continue
    [ ! -d ~/.claude-config-repo/claude/writing/"$dir_name" ] && rm -r "$d" && echo "Removed writing dir: $dir_name"
  done
fi
```

### Step 7: Check for missing plugins

```python
import json
from pathlib import Path

settings_path = Path.home() / ".claude" / "settings.json"
plugins_path = Path.home() / ".claude" / "plugins" / "installed_plugins.json"

with open(settings_path) as f:
    settings = json.load(f)
    enabled = set(settings.get("enabledPlugins", {}).keys())

try:
    with open(plugins_path) as f:
        installed = set(json.load(f).get("plugins", {}).keys())
except FileNotFoundError:
    installed = set()

missing = enabled - installed
if missing:
    print(f"⚠ {len(missing)} plugin(s) referenced in settings.json but not installed locally:\n")
    for p in sorted(missing):
        # Parse "name@registry" format
        parts = p.split("@", 1)
        name = parts[0]
        registry = parts[1] if len(parts) > 1 else "unknown"
        print(f"  {p}")
        print(f"    → claude mcp add-plugin {name}  (or search: claude plugin search {name})")
        print()
    print("To install all at once:")
    print("  " + " && ".join(
        f"claude mcp add-plugin {p.split('@')[0]}"
        for p in sorted(missing)
    ))
else:
    print("All plugins installed.")
```

If there are missing plugins, display the output and tell the user:
> **Missing plugins detected.** Your settings.json references plugins that aren't installed on this machine.
> Install commands are shown above — run them individually or use the all-at-once command.
> After installing, restart Claude Code for plugins to take effect.

### Step 8: Report

Show summary:
- Files updated (count by category)
- Any conflicts resolved and how
- Missing plugins (with install commands if any)
- "Config pulled from `[YOUR-GITHUB-HANDLE]/claude-config`"

## Subcommand: diff

Show differences between local config and repo.

### Step 1: Pre-flight

Run pre-flight checks.

### Step 2: Fetch and update local clone

```bash
git -C ~/.claude-config-repo fetch origin 2>/dev/null
git -C ~/.claude-config-repo pull --rebase 2>/dev/null || true
```

### Step 3: Compare each file pair

Build the full file map (local path ↔ repo path) from the File Inventory.

For each pair, compare:
```bash
diff -q <local-path> <repo-path> 2>/dev/null
```

Also check for files that exist only on one side:
- **Local only**: exists in `~/.claude/` but not in repo
- **Repo only**: exists in repo but not in `~/.claude/`

Categorize into: **Modified**, **Local only**, **Repo only**, **Identical**.

### Step 4: Report

Show a grouped summary:

```
## Config Diff: Local vs Repo

### Modified (N)
- <path> — N lines changed

### Local only (N)
- <path>

### Repo only (N)
- <path>

### Identical (N)
(all other files)
```

For modified files, offer: "Show detailed diff for any file? (e.g., `CLAUDE.md`)"

## Subcommand: status

Quick sync overview — no remote fetch.

### Step 1: Pre-flight (relaxed)

Only check that the sync marker and local clone exist. Skip gh auth check.

### Step 2: Read sync metadata

```bash
cat ~/.claude/.sync-config
```

### Step 3: Check local repo state

```bash
cd ~/.claude-config-repo
echo "Branch: $(git branch --show-current)"
echo "Last commit: $(git log -1 --format='%h %s (%ar)')"
echo "Remote: $(git remote get-url origin)"
```

### Step 4: Quick local modification count

Count files that differ between local config and repo (without fetching remote):
```bash
changed=0
total=0
for f in CLAUDE.md README.md settings.json; do
  total=$((total + 1))
  diff -q ~/.claude/"$f" ~/.claude-config-repo/claude/"$f" 2>/dev/null || changed=$((changed + 1))
done
# Also check agents, hooks, skills (count dirs/files)
```

### Step 5: Report

```
## Sync Status

Repo: [YOUR-GITHUB-HANDLE]/claude-config
Clone: ~/.claude-config-repo
Last sync: <from last commit timestamp>
Local changes: ~N files modified since last push

Run `/sync-config diff` for details or `/sync-config push` to export.
```
