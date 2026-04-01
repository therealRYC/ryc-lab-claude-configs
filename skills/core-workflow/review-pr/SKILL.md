<!-- Created: 2026-02-23 -->
<!-- Last updated: 2026-02-23 — Initial creation -->

---
name: review-pr
description: Review a GitHub pull request for code quality, correctness, and style
disable-model-invocation: true
user-invocable: true
context: fork
agent: general-purpose
allowed-tools: Read, Grep, Glob, Bash(gh *)
argument-hint: "[PR-number-or-URL]"
---

# Pull Request Review

Review PR $ARGUMENTS thoroughly.

## Step 1: Gather PR Data
- Get the PR diff, description, and comments using `gh`
- Identify all changed files

## Step 2: Review Checklist
For each changed file, check:

### Correctness
- [ ] Logic is correct and handles edge cases
- [ ] No off-by-one errors, null references, or race conditions
- [ ] Error handling is appropriate

### Security
- [ ] No hardcoded secrets or credentials
- [ ] Input validation at system boundaries
- [ ] No injection vulnerabilities (SQL, command, XSS)

### Style & Quality
- [ ] Functions have docstrings (Google-style for Python, roxygen2 for R)
- [ ] Type hints on Python function signatures
- [ ] No unnecessary complexity or over-engineering
- [ ] Variable/function names are clear and descriptive

### Tests
- [ ] New code has corresponding tests
- [ ] Edge cases are covered
- [ ] Tests actually assert meaningful behavior

### Research-Specific
- [ ] Data file paths use pathlib (Python)
- [ ] Random seeds are set for reproducibility
- [ ] Large data files are not committed (should be in .gitignore)

## Step 3: Summary
Provide a structured summary:
- **Overall assessment**: Approve / Request Changes / Comment
- **Key issues** (if any): numbered list with file:line references
- **Suggestions** (optional): improvements that aren't blocking
