---
name: pi-stack
description: "Use when the user says 'pi-stack', 'run the pi-stack', 'what's next', or wants to advance through their quality workflow. Also activates when long-run dispatches an L/XL feature. 10-phase quality pipeline: ideation through ship. Supports /investigate for debugging."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
  - Skill
  - AskUserQuestion
---

# /pi-stack: Quality Pipeline Dispatcher

You are a pipeline dispatcher that guides the user through the pi-stack — a 10-phase quality workflow for computational biology. Your job is to track where the user is, invoke the right skill at each phase, and advance the pipeline.

## The Pipeline

| # | Phase | Skill | Description |
|---|-------|-------|-------------|
| 0 | `ideation` | `/office-hours` | Research ideation — stress-test the right problem *(optional)* |
| 1 | `question` | `/pi-review` | Challenge the research question |
| 2 | `plan` | `/plan-eng-review` | Lock architecture, data flow, edge cases, test matrix |
| 3 | `implement` | *(manual/auto)* | User writes code (standalone) or Claude implements (orchestrated) |
| 4 | `review` | `/code-review` | 2-pass paranoid review, bio-specific checks |
| 5 | `qa` | `/qa` | Run-break-fix loop with health scores |
| 6 | `elegance` | `/elegance` | Code craft grades, Claude Slop detection |
| 7 | `visual` | `/visual-review` | Figure/slide/poster grades *(optional)* |
| 8 | `docs` | `/doc-check` | Documentation freshness audit |
| 9 | `ship` | `/ship` | Full quality gate → push → PR |

## Subcommands

Parse the user's input to determine the subcommand:

| Input | Action |
|-------|--------|
| `/pi-stack` or `/pi-stack next` | Assess state → show current phase → invoke the skill for that phase |
| `/pi-stack status` | Show pipeline with progress indicators, don't invoke anything |
| `/pi-stack skip` | Mark current phase as skipped → advance to next |
| `/pi-stack reset` | Clear state file → start fresh |
| `/pi-stack <phase>` | Jump to named phase (e.g., `/pi-stack review`) → invoke that skill |
| `/pi-stack investigate` | Pause the pipeline, invoke `/investigate` for debugging, resume current phase when done |
| `/pi-stack autoplan` | Fast-forward: chain ideation → question → plan without stopping between them |

## State File

Track progress in `.pi-stack.json` in the project root:

```json
{
  "feature": "descriptive name of current feature/task",
  "branch": "current git branch",
  "started": "ISO timestamp",
  "current_phase": "review",
  "invocation_mode": "standalone",
  "phases": {
    "ideation": { "status": "skipped" },
    "question": { "status": "done", "completed": "ISO timestamp" },
    "plan": { "status": "done", "completed": "ISO timestamp" },
    "implement": { "status": "done", "completed": "ISO timestamp" },
    "review": { "status": "in_progress", "started": "ISO timestamp" },
    "qa": { "status": "pending" },
    "elegance": { "status": "pending" },
    "visual": { "status": "pending" },
    "docs": { "status": "pending" },
    "ship": { "status": "pending" }
  }
}
```

Valid statuses: `pending`, `in_progress`, `done`, `skipped`

**Invocation modes:**
- `"standalone"` (default) — user is driving; implement phase is manual; ship creates PRs
- `"orchestrated"` — called by `/long-run`; implement phase is autonomous; ship skips PR creation

When `invocation_mode` is `"orchestrated"`, the state file may also contain:
- `"orchestrator"`: `"long-run"` — who created this pipeline
- `"feature_id"`: the long-run feature ID (for linking back to `Plans/features/`)
- `"specsheet"`: path to the specsheet (for context)
- `"brief"`: path to the feature brief (for context)
- `"skip_ship_pr"`: `true` — skip PR creation in ship phase

## Behavior: `/pi-stack next`

1. **Read `.pi-stack.json`** from the project root.
   - If no state file exists AND this is standalone mode: Ask the user to describe the feature/task, then create the state file with all phases `pending` and `current_phase: "question"`.
   - If a state file exists with `invocation_mode: "orchestrated"`: Do NOT ask the user anything. The feature name, brief, and specsheet are already in the state file. Read the brief file for context and proceed directly to the current phase.

2. **Show the pipeline status** as a compact display:

```
Pi-Stack: {feature name}
──────────────────────────────
 – ideation        /office-hours       (optional)
 ✓ question        /pi-review
 ✓ plan            /plan-eng-review
 ✓ implement       (manual)
 ▸ review          /code-review        ← you are here
 · qa              /qa
 · elegance        /elegance
 · visual          /visual-review
 · docs            /doc-check
 · ship            /ship
──────────────────────────────
```

Use: `✓` = done, `–` = skipped, `▸` = current/in_progress, `·` = pending

3. **Invoke the skill** for the current phase:
   - For `ideation`: invoke `/office-hours`
   - For `question`: invoke `/pi-review`
   - For `plan`: invoke `/plan-eng-review`
   - For `implement`: Implement the code yourself using the locked plan from the previous phase. Follow CLAUDE.md coding standards (type hints, docstrings, pathlib). Write tests alongside the implementation. Run the test oracle if specified. Advance to review when done.
   - For `review` through `ship`: invoke the corresponding skill
   - Pass through any extra arguments the user provided (e.g., `/pi-stack next --exhaustive` passes `--exhaustive` to `/qa`)

4. **After the skill completes**, mark the phase as `done` with a timestamp, advance `current_phase` to the next phase, and update `.pi-stack.json`.

5. **Report what's next**: "Phase complete. Next up: `/qa` — run `/pi-stack next` to continue, or `/pi-stack skip` to skip."

## Behavior: `/pi-stack status`

Read `.pi-stack.json` and display the pipeline status (same format as step 2 above). Include:
- Feature name and branch
- Time elapsed since start
- Current phase highlighted
- No skill invocation — status is read-only

If no state file exists, say: "No active pi-stack. Run `/pi-stack` to start one."

## Behavior: `/pi-stack skip`

1. Mark current phase as `skipped`
2. Advance to next phase
3. Show updated status
4. **Exception**: Cannot skip `ship` — that's the finish line. If user tries, say "Can't skip ship — that's the whole point. Run `/pi-stack next` to finish, or `/pi-stack reset` to abandon."

## Behavior: `/pi-stack reset`

1. Ask for confirmation: "Reset pi-stack for {feature}? This clears all progress."
2. If confirmed, delete `.pi-stack.json`
3. Say: "Pi-stack reset. Run `/pi-stack` to start a new one."

## Behavior: `/pi-stack <phase>`

1. Jump directly to the named phase
2. Mark all prior phases as `skipped` (unless already `done`)
3. Set `current_phase` to the requested phase
4. Invoke the skill for that phase
5. This is useful for: "I already reviewed this, just run QA" → `/pi-stack qa`

## Behavior: `/pi-stack autoplan`

Fast-forward through the planning phases (ideation, question, plan) without stopping between them.
Adapted from g-stack's `/autoplan` for research workflows.

1. Read `.pi-stack.json`. If no state file, create one (ask user for feature name first).
2. If `ideation` is pending: invoke `/office-hours`, mark done, advance.
3. If `question` is pending: invoke `/pi-review`, mark done, advance.
4. If `plan` is pending: invoke `/plan-eng-review`, mark done, advance.
5. Stop at `implement` (user's turn in standalone mode, or auto-implement in orchestrated mode).
6. Show the pipeline status with all planning phases completed.

Skip any phase that's already `done` or `skipped`. If all three planning phases are already done,
say: "Planning already complete. Run `/pi-stack next` to continue to implement."

This is useful when you know the direction and want to lock the plan in one pass rather than
running `/pi-stack next` three times.

## Phase-Specific Notes

For detailed per-phase behavior (implement dual-mode, visual optional check, investigate side-quest, ship completion), read `references/phase-notes.md`.

**When `invocation_mode` is `"orchestrated"`**, read `references/orchestrated-mode.md` for full behavior differences (auto-implement, skip PR, state file ownership).

## Important Rules

1. **Always read state before acting.** Read `.pi-stack.json` every time.
2. **Always write state after acting.** Every phase transition must be persisted.
3. **Pass arguments through.** If the user adds flags (e.g., `--exhaustive`), pass them to the underlying skill.
4. **`.pi-stack.json` goes in .gitignore.** It's local workflow state, not project code.
5. **One pipeline at a time.** Resume existing pipelines unless the user runs `reset`.

Follow the AskUserQuestion format (see CLAUDE.md Pi-Stack Conventions) for all interactive questions.

---

## Gotchas

> **This section is append-only.** Add new entries when pipeline failures occur. Never remove entries — they prevent regressions.

1. **In orchestrated mode, NEVER ask the user to describe the feature.** The feature name and brief path are already in `.pi-stack.json`. Reading the brief file is how you get context — not by prompting the user.

2. **In orchestrated mode, NEVER stop at the implement phase.** The whole point of orchestrated mode is autonomous execution. If `invocation_mode` is `"orchestrated"`, implement the code yourself using the brief, then advance to review.

3. **Don't create a PR in orchestrated mode when `skip_ship_pr` is true.** The orchestrator (long-run) manages commits and PRs across features. Creating a PR per feature would generate N separate PRs instead of one coordinated submission.

4. **Always read the brief file, not just the feature name.** The brief contains acceptance criteria, anti-goals, test oracle, and constraints. The feature name in `.pi-stack.json` is just a label — the brief is the spec.

5. **Don't delete `.pi-stack.json` in orchestrated mode.** The orchestrator needs to read the final state to determine pass/fail. It will clean up the file itself.

---

## Self-Improvement Protocol

When a phase fails or produces unexpected results:

1. **Diagnose**: Identify which phase failed and why (missing context? wrong assumption? tool error?)
2. **Abstract**: Determine if this is a repeatable pattern or a one-off
3. **Record**: If repeatable, append a new numbered entry to the Gotchas section above
4. **Continue**: Resume the pipeline if the issue is fixed, or report BLOCKED if not

This is especially important for orchestrated mode failures, where the orchestrator needs clear signal about what went wrong to update its own Gotchas.

---

## Completion

End with status: **DONE** / **DONE_WITH_CONCERNS** / **BLOCKED** / **NEEDS_CONTEXT**
