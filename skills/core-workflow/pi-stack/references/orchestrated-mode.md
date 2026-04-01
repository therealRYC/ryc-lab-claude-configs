# Pi-Stack: Orchestrated Mode

This file is loaded when `.pi-stack.json` has `invocation_mode: "orchestrated"`.
You do NOT need to read this file in standalone mode.

## What Orchestrated Mode Means

When `/long-run` dispatches a feature to pi-stack, it pre-creates `.pi-stack.json`
with orchestrated mode settings. This changes pi-stack behavior in three key ways:

1. **No user prompts** — feature name and brief are already in the state file
2. **Auto-implement** — Claude writes the code instead of waiting for the user
3. **Skip PR creation** — long-run manages commits across features

**Key change (2026-03-27):** Long-run now handles ALL planning interactively with the
user DURING its decompose phase. By the time pi-stack is invoked in orchestrated mode,
ideation, question, AND plan are already complete. The enriched feature brief contains
the locked plan (architecture, data flow, edge cases, test matrix). Pi-stack starts at
the implement phase.

## State File Fields (orchestrated only)

When `invocation_mode` is `"orchestrated"`, the state file contains:
- `"orchestrator"`: `"long-run"` — who created this pipeline
- `"feature_id"`: long-run feature ID (e.g., `"feat-03"`)
- `"specsheet"`: path to specsheet (e.g., `"Plans/specsheet.md"`)
- `"brief"`: path to feature brief (e.g., `"Plans/features/feat-03-brief.md"`)
- `"skip_ship_pr"`: `true` — skip PR creation in ship phase

## Phase Behavior Differences

### Starting the pipeline (`/pi-stack next`)
- Do NOT ask the user to describe the feature
- Read the brief file (path in `.pi-stack.json`) for full context
- The brief contains a **locked plan** with architecture, data flow, edge cases,
  test matrix, and integration points. This plan was already approved by the user
  during long-run's decompose phase. Follow it.
- Proceed directly to the current phase (typically `implement`)

### Ideation, Question, Plan phases (phases 0-2)
- These are pre-marked as `skipped` in the state file
- Long-run's decompose handled them interactively with the user:
  - Ideation: `/office-hours` stress-tested the feature scope
  - Question: feature scope was challenged and refined
  - Plan: `/plan-eng-review` locked the architecture into the brief
- Do NOT re-run these phases. The locked plan in the brief is authoritative.

### Implement phase (phase 3)
- Implement the feature autonomously
- Read the **locked plan section** of the feature brief for architecture guidance
- Read acceptance criteria, anti-goals, and constraints from the brief
- Write code following CLAUDE.md coding standards (type hints, docstrings, pathlib)
- Write tests per the test matrix in the locked plan, using realistic data
- Run the test oracle if specified in the brief
- Advance directly to review phase when done — do NOT wait for user

### Ship phase (phase 9)
- If `skip_ship_pr` is `true`: skip PR creation
- Still run quality gate checks (lint, tests)
- Commit code following the orchestrator's convention
- Update `.pi-stack.json` with all phases marked `done`
- Do NOT delete `.pi-stack.json` — the orchestrator reads it to verify completion
- Report completion summary (feature name, phases completed, any concerns)

## Important Rules

1. NEVER ask the user to describe the feature in orchestrated mode
2. NEVER stop at the implement phase — auto-implement and advance
3. NEVER create a PR when `skip_ship_pr` is true
4. NEVER delete `.pi-stack.json` — the orchestrator owns cleanup
5. Always read the brief file (not just the feature name) for full context
6. Follow the locked plan in the brief — it was approved by the user during decompose
