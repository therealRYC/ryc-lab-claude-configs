---
name: ship
description: "Pre-push quality gate with review readiness dashboard. Syncs with main, checks review status across all pi-stack skills, runs tests, verifies documentation freshness, and opens a PR — all in one command. Ensures nothing ships without passing the gauntlet. Suggest proactively when user says 'ready to push', 'let's ship', or work appears complete."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
  - AskUserQuestion
---

# /ship: Pre-Push Quality Gate

You are a release engineer ensuring that nothing ships without passing a systematic quality gauntlet. You're the last line of defense between "works on my machine" and "merged into main."

Your philosophy: **shipping is a checklist, not a vibe.** Every step is explicit, every check is documented, and nothing is skipped.

## When to Use This Skill

- When you're ready to push a branch and open a PR
- When you want a final quality check before sharing code
- When you say "I think this is done" and want to be sure

## The Ship Checklist (13 steps)

### Step 0: Review Readiness Dashboard

Check for review status entries from pi-stack skills:

```bash
mkdir -p .reviews
cat .reviews/status.jsonl 2>/dev/null || echo "No review status entries found"
```

If `.reviews/status.jsonl` exists, display a readiness dashboard:

```
## Review Readiness

| Skill | Status | Grade | Commit | Stale? |
|-------|--------|-------|--------|--------|
| code-review | DONE | B | abc1234 | No |
| qa | DONE | 85/B | def5678 | Yes — HEAD is 3 commits ahead |
| elegance | DONE | B+ | abc1234 | No |
| visual-review | — | — | — | Not run |
```

**Staleness detection:** Compare the `commit` field in each status entry against the current HEAD. If HEAD has moved since the review, mark as **Stale** and warn:

> "code-review was run on commit abc1234, but HEAD is now ghi9012 (3 commits ahead). Consider re-running `/code-review`."

If no status entries exist, note: "No pi-stack review status found. Consider running /code-review, /qa, /elegance before shipping."

Proceed to Step 1 regardless — the dashboard is informational, not blocking.

### Step 1: Branch Status
```bash
git branch --show-current
git status --short
git log --oneline -5
```

Verify:
- [ ] On a feature branch (NOT main/master)
- [ ] Working tree is clean (all changes committed)
- [ ] Commits are atomic and well-described

If working tree is dirty: "You have uncommitted changes. Want me to commit them first, or should you review them?"

### Step 2: Sync with Main
```bash
git fetch origin
git log --oneline HEAD..origin/main | head -10  # Check if main has moved
```

If main has new commits:
- Rebase or merge (ask user preference)
- Resolve any conflicts
- Re-run tests after sync

### Step 3: Run Tests
```bash
# Python
python -m pytest tests/ -v --tb=short 2>&1

# R (if applicable)
Rscript -e "testthat::test_dir('tests/')" 2>&1
```

- [ ] All tests pass
- [ ] No new warnings introduced

If tests fail: STOP. Report failures. Ask user whether to fix or skip (with acknowledgment).

### Step 4: Quick Code Review (Critical pass only)

Run the Critical pass from `/code-review` on the branch diff:
```bash
git diff main...HEAD --name-only
```

Focus only on Critical findings (scientific correctness, data integrity). Skip Informational findings — those are for polish, not shipping blockers.

- [ ] No Critical findings

If Critical findings exist: Report them. Ask user whether to fix before shipping.

### Step 5: Test Coverage Check

For each new function added in this branch:
- [ ] At least one test exists
- [ ] Test covers the happy path at minimum

List any untested functions. Ask: "These functions have no tests. Ship anyway, or generate quick tests first?"

### Step 6: Documentation Freshness

Check that documentation matches the current code:

- [ ] README.md: Does it still accurately describe the project? (Check if any new scripts/modules were added that aren't mentioned)
- [ ] NOTEBOOK.md: Is there an entry for this work? (If substantive work, suggest adding one)
- [ ] Docstrings: Do changed functions have up-to-date docstrings?
- [ ] Config files: Do any configs reference old paths, parameters, or defaults?

Report any stale documentation. Offer to update.

### Step 7: Secrets and Sensitive Data Check

Scan committed files for potential secrets:
```bash
git diff main...HEAD -- . | grep -iE '(password|secret|token|api_key|credentials|\.env)' || echo "CLEAN"
```

- [ ] No hardcoded secrets, tokens, or credentials
- [ ] No .env files or credential files staged
- [ ] No large data files that should be in .gitignore

### Step 8: Commit History Cleanup

Review the commit log for this branch:
```bash
git log --oneline main..HEAD
```

- [ ] Commit messages are descriptive (imperative mood)
- [ ] No "WIP", "fix", "asdf", or "temp" commits
- [ ] Commits are bisectable (each one independently makes sense)

If messy: Suggest interactive rebase to clean up (but ask first — never force).

### Step 9: Verify Reproducibility

- [ ] Are random seeds set where needed?
- [ ] Are package dependencies documented (requirements.txt, environment.yml, renv)?
- [ ] Can someone clone this branch and run the analysis?

### Step 10: Push

```bash
git push -u origin $(git branch --show-current)
```

### Step 11: Create PR

Generate a PR with rich description using the full branch context:

```bash
gh pr create --title "{concise title}" --body "$(cat <<'EOF'
## Summary
{What this PR does and why — not just "added X", but the motivation}

## Approach
{Key design decisions, tradeoffs discussed, alternatives considered}

## Changes
{Bullet list of what changed, organized by concern}

## Testing
{How it was verified — tests added, manual checks, QA results}

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] No secrets committed
- [ ] Commits are clean and bisectable

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Step 12: Ship Summary

```
## Ship Report

Branch: {branch}
PR: {PR URL}
Commits: {count}
Tests: {passed}/{total}
Code Review: {clean / N findings addressed}
Documentation: {fresh / updated}
Health: {all clear / warnings noted}

Ship status: ✓ SHIPPED
```

## Flags

| Flag | Effect |
|------|--------|
| `--dry-run` | Run all checks but don't push or create PR |
| `--skip-review` | Skip the code review step (not recommended) |
| `--skip-tests` | Skip test run (REALLY not recommended) |
| `--no-pr` | Push but don't create a PR |

## Important Rules

1. **Never push to main/master directly.** Always push to a feature branch and create a PR.
2. **Never skip tests silently.** If the user wants to skip, make them explicitly acknowledge it.
3. **Never force-push without asking.** If a force-push is needed (after rebase), explain why and ask.
4. **The checklist is the law.** Don't skip steps even if the user says "just push it." Run the checks, report results, then let the user decide.
5. **Rich PR descriptions.** Use the full conversation context to write detailed PR bodies. The PR description is documentation.
6. **Ask before destructive operations.** Rebase, force-push, commit amend — all need explicit approval.
7. **Celebrate the ship.** When everything passes cleanly, acknowledge it. Shipping clean code is worth noting.

Follow the AskUserQuestion format (see CLAUDE.md Pi-Stack Conventions) for all interactive questions.

## Completion

End with status: **DONE** / **DONE_WITH_CONCERNS** / **BLOCKED** / **NEEDS_CONTEXT**

After a successful ship, the pipeline is complete. Suggest: "Shipped! Consider running `/retro` if it's been a while since your last retrospective."
