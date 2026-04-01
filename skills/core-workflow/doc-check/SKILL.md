---
name: doc-check
description: "Documentation freshness check. AUTO-INVOKE after completing any task that involved writing or updating documentation (README, code walkthrough, config comments, NOTEBOOK). Verifies every claim against actual source files — never from memory. Finds stale docs and offers targeted fixes. Suggest proactively after code changes affecting function signatures or before a PR."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---

# /doc-check: Documentation Freshness Audit

You are a technical writer auditing documentation for accuracy and completeness. Your job is to ensure that what the docs say matches what the code actually does. Stale documentation is worse than no documentation — it actively misleads.

## When to Use This Skill

- After completing a batch of work
- Before creating a PR (part of /ship workflow)
- When the codebase has evolved and docs might be stale
- Periodically as a hygiene check

## Setup

Determine scope:
- No args: Check all documentation in the project
- `--changed`: Only check docs related to recently changed code
- `--file path`: Check a specific doc file

## The Audit (6 Checks)

### Check 1: README.md

Read README.md (if it exists) and verify:

- [ ] Project description matches current functionality
- [ ] Setup/installation instructions are current (correct package names, versions, commands)
- [ ] Usage examples actually work (spot-check at least one)
- [ ] File/directory structure described matches actual structure
- [ ] Any scripts or entry points mentioned still exist
- [ ] Dependencies listed match requirements.txt / environment.yml / pyproject.toml
- [ ] No references to removed features, old paths, or renamed files

**How to check:** Cross-reference README claims against the actual codebase using Grep and Glob. For each claim, verify it.

### Check 2: NOTEBOOK.md

If NOTEBOOK.md exists:

- [ ] Most recent entry is within the last N sessions of work (flag if stale)
- [ ] Decision log is up to date
- [ ] No entries reference plans/approaches that were later abandoned without a follow-up entry
- [ ] Status fields on entries are accurate (nothing marked "active" that's clearly done)

### Check 3: Docstrings

For every Python file changed recently (or all files if --full):

```bash
# Find functions missing docstrings
python3 -c "
import ast, sys
for f in sys.argv[1:]:
    tree = ast.parse(open(f).read())
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if not (node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, (ast.Str, ast.Constant))):
                print(f'{f}:{node.lineno} {node.name} — missing docstring')
" {files}
```

- [ ] All public functions have docstrings
- [ ] Docstrings match function signatures (correct parameter names, return type)
- [ ] No docstrings that describe old behavior (parameter renamed but docstring not updated)

### Check 4: Config Files

If config files exist (YAML, JSON, TOML):

- [ ] Config parameters are actually used in the code (no orphaned params)
- [ ] Default values in configs match default values in code
- [ ] No config references to old file paths or removed features
- [ ] Comments in configs are accurate

### Check 5: Plans/ Directory

If Plans/ exists:

- [ ] No plans marked as "active" that are clearly completed
- [ ] Completed plans have a status update
- [ ] No plans referencing approaches that were abandoned

### Check 6: Cross-Doc Consistency

- [ ] No conflicting information between README and NOTEBOOK
- [ ] Package names consistent across all docs
- [ ] File paths mentioned in docs actually exist
- [ ] Version numbers consistent (if mentioned in multiple places)

## Output Format

```
# Documentation Freshness Report

| Field | Value |
|-------|-------|
| **Date** | {DATE} |
| **Scope** | {project-wide / changed files only} |

## Overall: {Fresh / Stale / Needs Attention}

| Check | Status | Issues |
|-------|--------|--------|
| README.md | {✓ Fresh / ⚠ Stale / ✗ Missing} | {detail} |
| NOTEBOOK.md | {✓ Fresh / ⚠ Stale / ✗ Missing} | {detail} |
| Docstrings | {✓ Complete / ⚠ Gaps / ✗ Missing} | {N functions missing docs} |
| Config files | {✓ Fresh / ⚠ Stale / N/A} | {detail} |
| Plans/ | {✓ Fresh / ⚠ Stale / N/A} | {detail} |
| Cross-doc consistency | {✓ Consistent / ⚠ Conflicts} | {detail} |

## Issues Found
{each: what's stale, where, suggested update}

## Suggested Updates
{concrete text changes, offered for user approval}
```

## Important Rules

1. **Read first, always.** Before making or proposing any fix, read the canonical source file
   (e.g., `config_template.yaml` for default values, the R/Python source for function signatures).
   Never correct a doc from memory or from earlier conversation context.

2. **Two-tier fix policy:**
   - **Factual corrections** (wrong default value, wrong file path, wrong parameter name, wrong
     type) → read the source to confirm the correct value, then auto-fix and auto-commit without
     asking. These are mechanical and verifiable.
   - **Narrative / structural changes** (rewording descriptions, adding new sections, changing
     tone) → propose the change and ask for approval before editing.

3. **Missing docs > stale docs.** It's better to flag "README needs a section on X" than to have
   an incorrect section.

4. **Docstring accuracy > coverage.** A wrong docstring is worse than no docstring.

5. **Be proportional.** A quick script doesn't need full documentation. A shared pipeline does.

Follow the AskUserQuestion format (see CLAUDE.md Pi-Stack Conventions) for all interactive questions.

## Completion

End with status: **DONE** / **DONE_WITH_CONCERNS** / **BLOCKED** / **NEEDS_CONTEXT**

After completing the check, suggest: "Documentation checked — next step is `/ship` when you're ready to push."
