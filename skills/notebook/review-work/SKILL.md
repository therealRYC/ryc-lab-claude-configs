<!-- Created: 2026-03-08 -->
<!-- Last updated: 2026-03-08 — Initial creation -->

---
name: review-work
description: "Review and explain recent code changes in plain English. Produces an educational report of what was done, why, and how. Use when the user wants to understand session work, says 'review my work', 'what did we do', 'explain the changes', or invokes /review-work."
user-invocable: true
argument-hint: "[--branch | --since=<time> | <commit-sha> | <branch-name>]"
---

# Review Work

Generate an educational, plain-English review of recent code changes.

**Argument**: $ARGUMENTS

## Step 1: Pre-flight Checks

### Verify git repo
```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```
If this fails, stop immediately:
> "This isn't a git repository. `/review-work` needs git history to analyze. Navigate to a project repo and try again."

### Get project context
- Read the repo name: `basename $(git rev-parse --show-toplevel)`
- Check for README.md or CLAUDE.md at the repo root for project context
- Get the current branch: `git branch --show-current`

## Step 2: Determine Scope

Parse `$ARGUMENTS` to determine the commit range to review.

### Scope Rules

| Argument | Behavior | Git command for log |
|----------|----------|---------------------|
| *(empty)* | Session commits: last 4 hours by current user | `git log --since="4 hours ago" --author="$(git config user.name)" --oneline` |
| `--branch` | All commits since diverging from main/master | `git log main..HEAD --oneline` (detect default branch) |
| `--since=<time>` | Commits since the given time | `git log --since="<time>" --author="$(git config user.name)" --oneline` |
| A commit SHA | All commits from that SHA to HEAD | `git log <sha>..HEAD --oneline` |
| A branch name | All commits on that branch since main | `git log main..<branch> --oneline` |

### Detect default branch
```bash
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || echo "main"
```

### Collect the data

Once the commit range is determined:

1. **Commit log** (detailed):
   ```bash
   git log <range> --format="%h|%s|%ai" --stat
   ```

2. **Full diff**:
   ```bash
   git diff <first_commit>^..<last_commit>
   ```
   For the session default (no range), use:
   ```bash
   git diff $(git log --since="4 hours ago" --author="$(git config user.name)" --format="%H" | tail -1)^..HEAD
   ```

3. **File list with stats**:
   ```bash
   git diff --stat <range>
   ```

4. **Count commits**:
   ```bash
   git log <range> --oneline | wc -l
   ```

### Handle edge cases

- **No commits found**: Stop and report:
  > "No commits found in the requested scope. Try a different range:
  > - `/review-work --branch` — all commits since main
  > - `/review-work --since=8h` — last 8 hours
  > - `/review-work abc1234` — since a specific commit"

- **Large scope (50+ commits)**: Warn before proceeding:
  > "Found {N} commits — this is a large review. Want me to proceed, or narrow the scope?"
  Wait for user confirmation. If they proceed, group minor/housekeeping changes aggressively.

- **Only staged/unstaged changes (no commits)**: Check `git diff --stat` and `git diff --cached --stat`. If there are uncommitted changes but no commits in range, mention them:
  > "No commits in the requested range, but there are uncommitted changes. Want me to review those instead?"

## Step 3: Launch Analysis

Invoke the `work-reviewer` agent with all collected data.

Pass the agent:
- The full diff
- The commit log (with stats)
- The commit range description
- The project name and any context from README/CLAUDE.md
- The number of files changed, additions, and deletions

The agent will return a structured markdown report. Receive it and proceed to Step 4.

## Step 4: Write Report

### Create Reviews directory
```bash
mkdir -p Reviews
```

### Generate filename
Format: `Reviews/YYYY-MM-DD_{brief-description}.md`

The `brief-description` comes from the report title, lowercased, spaces replaced with hyphens, max 50 chars. Example: `Reviews/2026-03-08_add-normalization-pipeline.md`

```bash
date '+%Y-%m-%d'
```

### Write the report
Write the agent's report to the generated file path. The report should follow the template defined in the `work-reviewer` agent.

## Step 5: Notebook Entry (if applicable)

Check if `NOTEBOOK.md` exists at the project root. If it does, append a brief summary entry — NOT the full report.

### Notebook entry format

Append to NOTEBOOK.md:

```markdown
---

### YYYY-MM-DD HH:MM — Review: {Title}

**Type**: session
**Status**: completed
**Tags**: [review, {relevant-tags}]

**Goal**: Review and document recent code changes.

**Summary**:
- {3-5 bullet points summarizing what was done — pulled from the report's Summary section}

**Report**: `Reviews/YYYY-MM-DD_{description}.md`

**Related commits**:
- `{sha7}` — {first commit message}
- `{sha7}` — {last commit message}
- *(+{N} more — see report for full log)*
```

Also update the "Last updated" comment on line 2 of NOTEBOOK.md.

## Step 6: Auto-commit

```bash
git add Reviews/ && git commit -m "review: {Brief title} (Reviews/YYYY-MM-DD_{desc}.md)"
```

If NOTEBOOK.md was also updated:
```bash
git add Reviews/ NOTEBOOK.md && git commit -m "review: {Brief title} (Reviews/YYYY-MM-DD_{desc}.md)"
```

## Step 7: Terminal Summary

Print an abbreviated summary to the terminal. This should be scannable in 10 seconds:

```
## Work Review: {Title}

**Scope**: {N} commits, {M} files changed ({range description})

### What was done:
- {Purpose group 1}: {one-line summary}
- {Purpose group 2}: {one-line summary}
- {Purpose group 3}: {one-line summary}

### Key decisions:
- {Most important decision}: {one-line reasoning}
- {Second decision}: {one-line reasoning}

📄 Full report: Reviews/YYYY-MM-DD_{description}.md
```

Do NOT print the full report to the terminal — it's too long. The file is the artifact; the terminal output is the summary.
