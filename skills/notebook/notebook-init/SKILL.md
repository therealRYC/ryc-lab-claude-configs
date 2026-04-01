<!-- Created: 2026-03-03 -->
<!-- Last updated: 2026-03-03 — Initial creation -->

---
name: notebook-init
description: "Initialize a lab notebook for a project. Use when starting a new project, when the user asks to set up a notebook, or when /notebook is invoked but no NOTEBOOK.md exists."
user-invocable: true
argument-hint: "[project-name]"
---

# Initialize Lab Notebook

Create a `NOTEBOOK.md` file in the project root for project: $ARGUMENTS

## Before Writing

1. Check if `NOTEBOOK.md` already exists in the project root. If it does, STOP and tell the user — do not overwrite.
2. Detect project metadata automatically:
   - Project name: from $ARGUMENTS, or directory name, or git remote
   - Repository URL: from `git remote get-url origin` (if available)
   - Current branch: from `git branch --show-current`
   - Date/time: use `date '+%Y-%m-%d %H:%M'`

## NOTEBOOK.md Structure

Write the file with this structure:

```markdown
# Lab Notebook — {Project Name}

<!-- Created: YYYY-MM-DD -->
<!-- Last updated: YYYY-MM-DD — Project initialization -->

**PI**: [Your Name], [Lab Name], [Institution]
**Started**: YYYY-MM-DD
**Repository**: {git remote URL or "local"}

## Project Context

{Summarize from conversation: what is this project, why does it exist, what scientific questions are we asking. 2-4 sentences. If no context is available, write a placeholder and note it should be filled in.}

## Key Questions

- {Extract from conversation, or leave as placeholder bullets}

## Decision Log

| Date | Decision | Reasoning | Alternatives Considered |
|------|----------|-----------|------------------------|

---

## Entries

### YYYY-MM-DD HH:MM — Project initialization

**Type**: init
**Tags**: [setup]

**Summary**: Initialized lab notebook for {project name}.
{Brief description of project goals and initial setup from conversation context.}

**Initial plan**: {If a plan exists, summarize it. Otherwise omit this line.}
**Starting data/inputs**: {If known from context. Otherwise omit.}
**Next steps**: {What we're about to do first.}
```

## After Writing

1. Auto-commit: `git add NOTEBOOK.md && git commit -m "notebook: Initialize lab notebook for {project-name}"`
2. Report to user: "Initialized NOTEBOOK.md — first entry recorded."

## Conventions

- Follow the file timestamp rules (Created + Last updated at top)
- Use the project's actual context from the conversation — don't leave everything as placeholders
- Keep the Project Context and Key Questions sections concise
- The Decision Log table starts empty — it accumulates as /notebook entries add decisions
