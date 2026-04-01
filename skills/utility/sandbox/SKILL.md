---
name: sandbox
description: "Interactively configure and generate a Docker container command for sandboxed Claude Code sessions. Walks through security presets, mount options, and git safety checks."
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Write
  - AskUserQuestion
argument-hint: "[reuse]"
---

<!-- Created: 2026-03-24 -->

# /sandbox: Docker Sandbox for Claude Code

Launch a sandboxed Claude Code session inside a Docker container. This skill walks you through
configuration interactively, ensures git safety, and generates an annotated `docker run` command
to copy-paste into a separate terminal.

## Quick Start

- `/sandbox` — full interactive configuration
- `/sandbox reuse` — reuse last saved configuration

---

## Step 1: Check for Saved Config

If the argument is `reuse`, read `~/.claude/sandbox.local.md` and skip to Step 7 (Review & Confirm)
using the saved settings. If the file doesn't exist, tell the user and fall through to Step 2.

If no argument, check if `~/.claude/sandbox.local.md` exists. If it does, ask:

> **Sandbox setup** — You have a saved configuration from a previous session.
>
> RECOMMENDATION: Reuse your last config to save time. You can always reconfigure.
>
> A) **Reuse last config** — skip to review & confirm
> B) **Configure new** — walk through all settings fresh

---

## Step 2: Pre-flight Checks (automatic, no user input)

Run these checks silently and report results:

```bash
# Check Docker is running
docker info > /dev/null 2>&1

# Check auth credentials exist
test -f ~/.claude/.credentials.json

# Check current directory is a git repo
git rev-parse --is-inside-work-tree 2>/dev/null

# Check git status
git status --porcelain
```

**If Docker is not running**, try `sudo service docker start`. If that fails, report:
> "Docker is not running. Start it with `sudo service docker start` and try again."
> Status: **BLOCKED**

**If not a git repo**, report:
> "The current directory is not a git repository. /sandbox requires git as a safety net
> so you can always restore your code. Initialize with `git init` and commit your files first."
> Status: **BLOCKED**

**If auth credentials don't exist**, note this — the user will need an API key instead.

Report a brief summary of pre-flight results before continuing.

---

## Step 3: Security Preset

This is the gate question. Use AskUserQuestion:

> **Sandbox configuration** — Choose a security level for your Docker sandbox.
> This controls how much access the container has to your files and system.
>
> RECOMMENDATION: Choose Balanced — it lets Claude edit your code while protecting
> your system, with git as your safety net.
>
> A) **Cautious** — Read-only project mount, resource-limited, disposable container.
>    Claude can read your code but can't modify files directly. Best for code review
>    or exploration.
>
> B) **Balanced** — Read-write mount, resource-limited, persisted container.
>    Claude can edit files. Git required as safety net. The sweet spot for development.
>
> C) **YOLO** — Read-write mount, no resource limits, persisted container.
>    Full autonomy. Auto-commits a checkpoint so you can always roll back.
>
> D) **Custom** — Configure every setting individually.

### Preset mappings

After the user picks a preset (A-C), set these variables and skip to Step 7 (Git Safety):

**Cautious:**
- `BASE_IMAGE=python:3.12-slim`
- `MOUNT_MODE=ro`
- `MEMORY=2g`
- `CPUS=2`
- `LIFECYCLE=--rm`
- `GIT_POLICY=require_clean`

**Balanced:**
- `BASE_IMAGE=python:3.12-slim`
- `MOUNT_MODE=rw`
- `MEMORY=4g`
- `CPUS=4`
- `LIFECYCLE=--name claude-sandbox-$(basename $PWD)`
- `GIT_POLICY=require_clean`

**YOLO:**
- `BASE_IMAGE=python:3.12-slim`
- `MOUNT_MODE=rw`
- `MEMORY=` (no limit)
- `CPUS=` (no limit)
- `LIFECYCLE=--name claude-sandbox-$(basename $PWD)`
- `GIT_POLICY=auto_commit`

If **Custom**, continue to Step 4.

---

## Step 4: Base Environment (Custom only)

Use AskUserQuestion:

> **Base environment** — What language/tools do you need in the container?
> Claude Code itself requires Node.js, which is installed automatically on top of your choice.
>
> RECOMMENDATION: Python — it's your primary language and the slim image is fast to pull.
>
> A) **Python 3.12** — `python:3.12-slim` (~50MB pull)
> B) **Node.js 22** — `node:22-slim` (~60MB pull, Claude Code installs faster since Node is already there)
> C) **R** — `rocker/r-ver:4.4` (~300MB pull)
> D) **Multi-language** — `ubuntu:24.04` with Python + Node + R (~400MB pull)

Then ask as a follow-up text prompt (not multiple choice):
> "Any extra packages to pre-install? (e.g., `pandas numpy biopython` for pip, or `vim curl` for apt)
> Press Enter to skip."

---

## Step 5: Mount Configuration (Custom only)

Use AskUserQuestion:

> **Mount configuration** — How should the container access your project files?
>
> Current directory: `{$PWD}`
>
> RECOMMENDATION: Read-write — lets Claude make changes, with git as your safety net.
>
> A) **Read-write** — Container can read and modify your files. Changes appear on your real system.
> B) **Read-only** — Container can see but not modify your files. Safe for exploration/review.
> C) **Copy-in** — Copies files into the container. Your originals are untouched. You manually
>    copy results back with `docker cp`.

---

## Step 6: Container Settings (Custom only)

Use AskUserQuestion (group these together):

> **Container settings** — Resource limits and lifecycle.
>
> RECOMMENDATION: Standard limits + persisted. Prevents runaway processes while letting you
> resume the container later.
>
> **Resources:**
> A) **Light** — 2GB memory, 2 CPUs
> B) **Standard** — 4GB memory, 4 CPUs
> C) **Heavy** — 8GB memory, 8 CPUs
> D) **No limits** — Container can use all host resources

And in the same prompt:

> **Lifecycle:**
> A) **Disposable** (`--rm`) — Container deleted when it stops. Clean slate each time.
> B) **Persisted** — Container stays around. Resume with `docker start`.

---

## Step 7: Git Safety Check (always runs)

Check the git status of the mount directory:

```bash
git status --porcelain
```

**If working tree is clean**: Report "Git status: clean. You have a safe restore point." and continue.

**If there are uncommitted changes**, behavior depends on `GIT_POLICY`:

- **`require_clean`** (Cautious/Balanced):
  > "You have uncommitted changes. The sandbox requires a clean git state so you can
  > restore your code if anything goes wrong."
  >
  > A) **Stash changes** — `git stash` (retrieve later with `git stash pop`)
  > B) **Abort** — I'll stop so you can commit manually

- **`auto_commit`** (YOLO):
  Auto-run:
  ```bash
  git add -A && git commit -m "wip: pre-sandbox checkpoint"
  ```
  Report: "Auto-committed a checkpoint. To undo later: `git reset HEAD~1`"

- **Custom with `proceed_anyway`**:
  Warn but continue: "Proceeding with uncommitted changes. If things go wrong,
  uncommitted work may be harder to recover."

---

## Step 8: Review & Confirm

Build the `docker run` command from the collected settings and display it with annotations.

### WSL2 performance warning
If the mount path starts with `/mnt/`, display:
> **Warning**: Your project is on the Windows filesystem (`/mnt/c/...`). Docker mounts
> across the WSL2/Windows boundary are slow. For better performance, copy your project
> to the Linux filesystem (e.g., `/home/rober/projects/`) first.

### Auth setup
Check which auth is available:
- If `~/.claude/.credentials.json` exists → mount it read-only
- Otherwise → remind user to set `ANTHROPIC_API_KEY` before running the command

### Command template

Display the command in a code block with inline comments:

```bash
docker run -it \
  # --- Project mount ({MOUNT_MODE}) ---
  -v {MOUNT_DIR}:/workspace:{MOUNT_MODE} \
  # --- Auth (OAuth credentials, read-only) ---
  -v ~/.claude/.credentials.json:/root/.claude/.credentials.json:ro \
  # --- Inherit your Claude Code settings (permissions, deny lists) ---
  -v ~/.claude/settings.json:/root/.claude/settings.json:ro \
  # --- Match your host user to avoid root-owned files ---
  --user $(id -u):$(id -g) \
  # --- Resource limits ---
  --memory {MEMORY} --cpus {CPUS} \
  # --- Container lifecycle ---
  {LIFECYCLE} \
  # --- Start in project directory ---
  -w /workspace \
  # --- Base image ---
  {BASE_IMAGE} \
  # --- Install Claude Code and start it ---
  bash -c "apt-get update -qq && apt-get install -y -qq nodejs npm git > /dev/null 2>&1 && npm install -g @anthropic-ai/claude-code > /dev/null 2>&1 && claude"
```

Notes to display:
- "First run will take 30-60 seconds to install Node.js and Claude Code. Subsequent runs of a persisted container are instant."
- "Copy this command and paste it in a **separate terminal** (not here in Claude Code)."

Then ask:
> A) **Looks good** — save this config and show me the command to copy
> B) **Edit something** — go back and change a setting
> C) **Cancel** — abort without launching

---

## Step 9: Save Config

If the user confirmed, save the configuration to `~/.claude/sandbox.local.md`:

```markdown
---
preset: balanced
base_image: python:3.12-slim
mount_dir: /home/rober/my-project
mount_mode: rw
memory: 4g
cpus: 4
lifecycle: persisted
container_name: claude-sandbox-my-project
git_policy: require_clean
last_used: 2026-03-24
---

# Sandbox Configuration

Last generated command:
\`\`\`bash
docker run -it ...
\`\`\`
```

---

## Step 10: Post-Launch Tips

After displaying the command, show this reference card:

```
╔══════════════════════════════════════════════════╗
║  SANDBOX QUICK REFERENCE                         ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  Reconnect to running container:                 ║
║    docker exec -it {CONTAINER_NAME} bash         ║
║                                                  ║
║  Stop the container:                             ║
║    docker stop {CONTAINER_NAME}                  ║
║                                                  ║
║  Restart a stopped container:                    ║
║    docker start -ai {CONTAINER_NAME}             ║
║                                                  ║
║  Delete the container:                           ║
║    docker rm {CONTAINER_NAME}                    ║
║                                                  ║
║  Copy a file out of the container:               ║
║    docker cp {CONTAINER_NAME}:/workspace/f ./f   ║
║                                                  ║
║  Undo sandbox changes (git safety net):          ║
║    git checkout .          (discard all changes) ║
║    git reset HEAD~1        (undo auto-commit)    ║
║    git stash pop           (restore stashed)     ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

---

## Completion

End with status: **DONE**

---

## Important Rules

1. **Never execute the docker run command** — only generate it for the user to run in a separate terminal.
2. **Git is mandatory** — abort if the mount directory is not a git repo.
3. **Always mount auth and settings read-only** (`:ro`) — the container should never modify credentials.
4. **Follow Pi-Stack AskUserQuestion format** — re-ground, simplify, recommend, options.
5. **Explain as you go** — this is a teaching skill. Brief explanations of what each Docker flag does help the user learn.
6. **WSL2 awareness** — warn about `/mnt/` performance issues.
