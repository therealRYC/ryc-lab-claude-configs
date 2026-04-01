---
name: long-run
description: "Use when starting a multi-feature project, building an application from scratch, or coordinating work that spans multiple coding sessions. Handles project decomposition, feature dispatching, and quality evaluation. Subcommands: interview, decompose, next, parallel, status, evaluate."
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

<!-- Created: 2026-03-25 -->
<!-- Last updated: 2026-03-27 — Two-phase model: interactive planning up front, autonomous execution -->

# /long-run: Project-Level Orchestration

You are a project orchestrator for long-running development tasks. You decompose entire projects into parallelizable features with dependency management, then coordinate execution — dispatching features to pi-stack or modular-workers as appropriate.

**You sit ABOVE pi-stack.** Pi-stack handles one feature end-to-end. You handle the decomposition of an entire project into features and orchestrate their execution across multiple context windows.

**Core philosophy (from He He):** "The better the specification, the longer the agent can run without intervention."

**Two-phase model:**
1. **Interactive planning** — project interview + per-feature specification with the user. Take as long as needed. This is where quality comes from.
2. **Autonomous execution** — Claude implements each fully-spec'd feature through pi-stack. No user interaction needed until completion.

## IMPORTANT: Run in Normal Mode

**Do NOT run `/long-run` in plan mode.** This skill uses AskUserQuestion with lettered options (A/B/C) for all interviews. That interactive style — where you can hit a letter to advance — only works in normal mode. Plan mode uses a different interaction pattern (propose/approve) that doesn't match the interview flow.

## When to Use This Skill

- Starting a new application or tool from scratch
- Building a multi-feature pipeline or system
- Any project that will take more than one coding session
- When you need parallelizable, independent feature execution
- When you want adversarial quality evaluation

## Subcommands

Parse the user's input to determine the subcommand:

| Input | Action |
|-------|--------|
| `/long-run` or `/long-run interview` | Start interview -> produce specsheet |
| `/long-run decompose` | Take specsheet -> feature breakdown -> per-feature interview -> locked plans |
| `/long-run next [--autonomous\|--supervised]` | Pick next feature -> execute via pi-stack (autonomous) |
| `/long-run parallel` | Pick all independent S/M features -> dispatch to modular-workers |
| `/long-run status` | Dashboard of all features |
| `/long-run evaluate` | Run external evaluator on completed features |
| `/long-run reset` | Clear state and start over |

## State File: `.long-run.json`

Track project state in `.long-run.json` at the project root (add to .gitignore):

```json
{
  "project": "descriptive name",
  "specsheet": "Plans/specsheet.md",
  "feature_list": "Plans/feature-list.json",
  "mode": "supervised",
  "started": "2026-03-25T10:00:00Z",
  "phase": "decomposing",
  "decompose_progress": {
    "step": "feature_spec",
    "features_spec_order": ["feat-01", "feat-02", "feat-03"],
    "current_feature": "feat-02",
    "current_sub_phase": "plan",
    "completed": ["feat-01"]
  },
  "current_feature": null
}
```

Valid phases: `interview`, `specsheet_complete`, `decomposing`, `decomposed`, `executing`, `evaluating`, `complete`

---

## Behavior: `/long-run` or `/long-run interview`

### If `.long-run.json` exists:

Resume the existing project. Show status and ask:
- "Resume {project name}? Currently in phase: {phase}."
- Options: Resume / Reset / New project

### If no state file exists:

Start the interview. Read the specsheet-guide.md reference for the full interview template.

**Setup:**
1. Read README.md, NOTEBOOK.md, any Plans/ or Brainstorm/ files for existing context
2. Check git log for recent work
3. Look for existing data files, configs, or code

**The Interview (6 Sharpening Questions):**

Ask each question using AskUserQuestion where possible. Work through ALL six in order:

1. **Deliverable Definition** -- "What concrete artifact exists when this project is done?"
2. **Test Oracle** -- "How do you know it works?"
3. **Constraints & Resources** -- "What are the hard boundaries?"
4. **Anti-Goals** -- "What shortcuts should Claude NOT take?"
5. **Narrowest Wedge** -- "What's the smallest version that proves the architecture?"
6. **Human Judgment Gates** -- "Where must Claude stop and ask?"

**After all 6 questions:**
1. Compile the specsheet using the format in specsheet-guide.md
2. Save to `Plans/specsheet.md` (create Plans/ directory if needed)
3. Create `.long-run.json` with `phase: "specsheet_complete"`
4. Show the specsheet summary to the user for confirmation
5. Say: "Specsheet complete. Run `/long-run decompose` to break this into features and spec each one."

---

## Behavior: `/long-run decompose`

Decompose is a multi-step process with its own internal state. Each call to `/long-run decompose` advances to the next sub-step. The user drives advancement — one sub-step per invocation.

Read `.long-run.json`. If phase is not `specsheet_complete` or `decomposing`, say: "Wrong phase. Run `/long-run interview` first."

Read the decomposition-guide.md reference for decomposition patterns, schemas, and the per-feature interview protocol.

### Step 1: Initial Breakdown (if no `decompose_progress`)

1. Read `Plans/specsheet.md`
2. **Identify the data flow** — trace input -> transformations -> output
3. **Draw the dependency graph** in Mermaid format
4. **Decompose into features** — break at natural seams, each independently testable
5. **Tag each feature** with:
   - ID, name, description
   - Dependencies (which features must complete first)
   - Complexity estimate (S/M/L/XL)
   - Anti-goals (relevant subset from specsheet)
   - Human gate (yes/no)
6. **Identify execution waves** — group by dependency layers
7. **Calculate the critical path** — longest sequential chain

**Present decomposition to user** via AskUserQuestion:
- Show the dependency graph
- Show the wave breakdown
- Show the critical path
- Ask:
  - A) Looks good, let's spec each feature
  - B) Need to adjust (add/remove/split/merge features)

**After user approves the high-level breakdown:**
1. Save `Plans/feature-tree.md` (dependency graph + waves)
2. Save `Plans/feature-list.json` (feature list with schema from decomposition-guide.md)
3. Create `Plans/features/` directory
4. For each feature, save an initial draft brief `Plans/features/{feature-id}-brief.md`
5. Set phase to `decomposing`, create `decompose_progress`:
   ```json
   {
     "step": "feature_spec",
     "features_spec_order": ["feat-01", "feat-02", ...],
     "current_feature": "feat-01",
     "current_sub_phase": "office-hours",
     "completed": []
   }
   ```
6. Say: "Breakdown approved with {N} features. Now let's spec each one. Run `/long-run decompose` to start interviewing feature 1: {name}."

### Step 2: Per-Feature Specification (iterates for each feature)

Each call to `/long-run decompose` processes the next sub-phase for the current feature. Read `decompose_progress` from `.long-run.json` to determine where you are.

**Sub-phase: `office-hours`**

Present the draft brief for the current feature, then invoke `/office-hours` with feature context. The goal is to stress-test whether this feature is scoped correctly:
- Is this the right problem to solve?
- Is the scope too broad or too narrow?
- Are there hidden assumptions?
- Does this feature actually serve the project goal?

Before invoking, set up context: "We're speccing feature {id}: {name}. Here's the draft brief: {summary}. Let's challenge whether this is the right approach."

After `/office-hours` completes:
1. Update the draft brief with any scope changes or insights
2. Advance `current_sub_phase` to `"plan"`
3. Say: "Office hours complete for {feature name}. Run `/long-run decompose` to lock the architecture."

**Sub-phase: `plan`**

Invoke `/plan-eng-review` with the (potentially revised) feature brief as context. The goal is to lock the architecture before any code is written:
- Data flow diagram for this feature
- Edge cases and test matrix
- File structure (what to create/modify)
- Integration points with other features
- Test oracle (specific command)

Before invoking, set up context: "We're locking the plan for feature {id}: {name}. Here's the current brief: {summary}."

After `/plan-eng-review` completes:
1. Save the locked plan INTO the feature brief (see enriched brief format in decomposition-guide.md)
2. Advance `current_sub_phase` to `"approval"`
3. Say: "Plan locked for {feature name}. Run `/long-run decompose` to review and approve."

**Sub-phase: `approval`**

Show the fully enriched brief (feature scope from office-hours + locked plan from plan-eng-review). Use AskUserQuestion:
- A) Approved — move to next feature
- B) Revise scope — go back to office-hours for this feature
- C) Revise plan only — go back to plan-eng-review
- D) Split this feature — break into sub-features (restart decompose for new features)
- E) Remove this feature

**On approval:**
1. Save the final enriched brief to `Plans/features/{feature-id}-brief.md`
2. Update `Plans/feature-list.json` with enriched metadata (test_cmd, qa_level, etc.)
3. Move feature from `current_feature` to `completed` list
4. Advance `current_feature` to the next in `features_spec_order`
5. Reset `current_sub_phase` to `"office-hours"`

If features remain: "Feature {name} approved ({completed}/{total}). Run `/long-run decompose` for feature {next}: {next_name}."

If all features complete: advance to Step 3.

### Step 3: Final Review

Show a summary of all spec'd features:

```
Decomposition Complete: {project name}
================================================================

Features: {N} total | Critical path: {M} features
Planning time: {elapsed since decompose started}

Feature                  Size  Plan Locked  Test Oracle
------------------------------------------------------
config-parser            [S]   Yes          pytest tests/test_config.py
data-loader              [M]   Yes          pytest tests/test_loader.py
core-calculation         [L]   Yes          python scripts/validate.py
visualization            [M]   Yes          pytest tests/test_viz.py
integration-test         [L]   Yes          python scripts/run_integration.py

All features have locked plans with architecture, edge cases,
and test matrices defined.
================================================================
```

Use AskUserQuestion:
- A) Approved — ready to build
- B) Need to revise a specific feature (which one?)

**On approval:**
1. Update `.long-run.json`: phase -> `"decomposed"`, remove `decompose_progress`
2. Say: "All {N} features spec'd and approved. Run `/long-run next` to start building, or `/long-run parallel` to run independent features in parallel."

---

## Behavior: `/long-run next [--autonomous|--supervised]`

**Default mode:** supervised (stops after each feature, waits for user)
**Override:** `--autonomous` (continues to next feature automatically)

**All features — regardless of size (S/M/L/XL) — execute through pi-stack orchestrated mode, starting at the implement phase.** Planning is already done (locked during decompose). Pi-stack handles: implement -> review -> qa -> elegance -> docs -> ship.

Read `Plans/feature-list.json`. Pick the next feature where:
- Status is `pending`
- All dependencies have status `passing`
- If a human gate exists and this is the first time encountering it, use AskUserQuestion

If no features are available (all pending features are blocked), report the blocking situation.

### Execute the feature:

**Step 1 -- Create pi-stack state:**

Use the handoff scripts in `~/.claude/skills/long-run/scripts/` to manage the pi-stack lifecycle.
These scripts generate correct state deterministically — do NOT write `.pi-stack.json` by hand.

```
Bash: python3 ~/.claude/skills/long-run/scripts/create_pi_stack_state.py \
  --feature "{feature-name}" \
  --feature-id "{feature-id}" \
  --branch "{current git branch}" \
  --brief "Plans/features/{feature-id}-brief.md" \
  --specsheet "Plans/specsheet.md"
```

The script sets `invocation_mode: "orchestrated"`, skips ideation/question/plan (all done during decompose), and starts at `implement`.

**Step 2 -- Invoke pi-stack:**

```
Skill tool call:
  skill: "pi-stack"
  args: "next"
```

Pi-stack reads `.pi-stack.json`, sees orchestrated mode starting at implement, and auto-runs: implement -> review -> qa -> elegance -> docs -> ship(no PR).

**Step 3 -- Verify completion:**

```
Bash: python3 ~/.claude/skills/long-run/scripts/verify_pi_stack_completion.py
```

Exit code 0 = PASS (all phases terminal). Exit code 1 = FAIL (update feature-list.json accordingly).

**Step 4 -- Post-completion (quality gate + regression check):**

1. Write the test-explain doc: `Plans/features/{feature-id}-tests.md`
2. **Run the evaluator on this feature:** Invoke `/long-run evaluate` targeting just this feature (not all features). The evaluator checks all 5 dimensions: correctness, test quality, anti-goal compliance, integration, scope fidelity. This runs for ALL features regardless of size — catch issues before they propagate to dependent features.
3. **Regression check:** Re-run test oracles for all features with status `passing` (not just the current one). If a previously-passing feature now fails, immediately flag it:
   - Set the regressed feature's status to `failing` in feature-list.json
   - Report: "REGRESSION: {feature-name} tests now failing after {current-feature} was implemented"
   - In supervised mode: stop and ask how to proceed
   - In autonomous mode: stop (don't continue past regressions)
4. Update feature-list.json with status, evaluator scores, and regression results
5. Commit with message: `long-run: Complete {feature-name}`

**Step 5 -- Clean up:**

```
Bash: python3 ~/.claude/skills/long-run/scripts/cleanup_pi_stack_state.py
```

This safely removes `.pi-stack.json` (guards against deleting if phases aren't terminal).

### After feature completes:

**Log the dispatch** — Append a row to `Plans/dispatch-log.md` (create from `references/dispatch-log-template.md` if it doesn't exist). Record: timestamp, feature ID, name, complexity, dispatch method, result, duration.

**Supervised mode:** Show a brief status summary with the feature result, total progress (passing/total), blocked count, and what's available next. Then wait for user.

**Autonomous mode:**
- If feature passes (evaluator + regression check clean): pick next available feature and continue
- If feature fails (pi-stack, evaluator, or regression): stop and report the failure (don't blindly continue)
- If all features pass: stop and report completion
- If no features are available: stop and report blockage

---

## Behavior: `/long-run parallel`

**Parallel execution is for implementation only. Planning (decompose) is always sequential** because the user can only interview one feature at a time.

Read `Plans/feature-list.json`. Find ALL features where:
- Status is `pending`
- All dependencies have status `passing`
- Complexity is S or M (don't parallelize L/XL — they need sequential pi-stack with more quality gates)

If no features qualify, say so and suggest `/long-run next` instead.

**For each qualifying feature, dispatch a modular-worker agent:**

```
Agent tool call:
  subagent_type: modular-worker (or general-purpose with worktree isolation)
  isolation: worktree
  prompt: |
    You are implementing feature "{feature-name}" for project "{project-name}".

    Read these files for context:
    1. Plans/specsheet.md -- project specification
    2. Plans/features/{feature-id}-brief.md -- this feature's FULL brief with locked plan

    IMPORTANT: The brief contains a locked plan with architecture, data flow,
    edge cases, test matrix, and integration points. Follow the plan exactly.

    Implement the feature following these steps:
    1. Read the brief carefully — especially the locked plan section
    2. Implement the code per the plan (follow coding standards: type hints, docstrings, pathlib)
    3. Write tests per the test matrix in the plan (realistic data, edge cases)
    4. Run the test oracle: {test_cmd}
    5. Write test explanation to Plans/features/{feature-id}-tests.md
    6. Commit with message: "long-run: Complete {feature-name}"
    7. Report: what you built, tests passing/failing, any concerns
```

**After all workers complete:**
1. Review results from each worker
2. Merge worktree branches into the main working branch
3. If merge conflicts occur, flag them for user review using AskUserQuestion
4. Run all test oracles to verify integration
5. Update feature-list.json with results
6. Report summary:

```
Parallel execution complete:
-------------------------------------
+ {feature-1} -- passing
+ {feature-2} -- passing
x {feature-3} -- failing (test_xyz failed)
-------------------------------------
Features: {passing}/{total} passing
```

**Note:** Parallel S/M features skip some pi-stack quality gates (elegance, visual-review) in exchange for speed. For full quality gates on every feature, use `/long-run next` sequentially instead.

---

## Behavior: `/long-run status`

Read `.long-run.json` and `Plans/feature-list.json`. Display:

```
Long Run: {project name}
Phase: {phase} | Mode: {supervised/autonomous}
Started: {date} | Elapsed: {duration}
==================================================
Clean-pass rate: 75% (3/4) | Coverage: 5/5 dims | Hit rate: 67%
==================================================

Features: {passing}/{total} passing | {blocked} blocked | {failing} failing

+ config-parser      [S]  passing   5/5 dims  (pytest tests/test_config.py)
+ data-loader        [M]  passing   5/5 dims  (pytest tests/test_loader.py)
> core-calculation   [L]  running              <- current
. visualization      [S]  pending              (depends: core-calculation)
x integration-test   [L]  needs work 5/5 dims  (anti-goal violation)
@ api-endpoint       [M]  blocked              (depends: output-generator)
. output-generator   [M]  pending              (depends: core-calculation)

--------------------------------------------------
Next available: {features with met dependencies}
Critical path remaining: {features} (~{time estimate})
```

Symbols: `+` passing, `>` in_progress, `.` pending, `x` failing, `@` blocked

**If phase is `decomposing`**, show decompose progress instead:

```
Long Run: {project name}
Phase: decomposing (speccing features)
==================================================

Features spec'd: {completed}/{total}

+ config-parser      [S]  spec'd (plan locked)
+ data-loader        [M]  spec'd (plan locked)
> core-calculation   [L]  in progress (sub-phase: plan-eng-review)
. visualization      [S]  pending
. integration-test   [L]  pending

--------------------------------------------------
Run /long-run decompose to continue speccing features.
```

**Rate-based health metrics** (shown after the feature list, execution phase only):
```
Health Metrics:
  Clean-pass rate:  75% (3/4 evaluated features)
  Evaluator hit rate: 80% (4/5 findings confirmed)
  Override rate:    20% (1/5 findings overruled)
```

**Auto-generated health check warnings** (shown when patterns suggest gaming):
- `"Warning: Generator has +1 honesty points on every feature -- verify gaps are genuine"`
- `"Warning: Evaluator has 0 findings for 3 consecutive features -- spot-check manually"`
- `"Warning: All features completing under time estimate -- estimates may be sandbagged"`
- `"Warning: Evaluator findings are all style/quality (+1) -- check for substantive issues"`
- `"Warning: Clean-pass rate is 100% -- either excellent code or weak evaluation"`

If no state file exists: "No active long-run project. Run `/long-run` to start one."

---

## Behavior: `/long-run evaluate`

Dispatch the `long-run-evaluator` agent on all features with status `passing`.

For each feature:
```
Agent tool call:
  description: "Evaluate {feature-name}"
  subagent_type: general-purpose
  prompt: |
    You are the long-run-evaluator. Read ~/.claude/agents/long-run-evaluator.md for your full instructions.

    Evaluate feature "{feature-name}" for project "{project-name}".

    Read these files:
    1. Plans/specsheet.md -- anti-goals and success criteria
    2. Plans/features/{feature-id}-brief.md -- acceptance criteria and locked plan
    3. Plans/features/{feature-id}-tests.md -- test explanation (CRITICAL: check "What's NOT Tested")
    4. The implementation source code
    5. The test source code

    Follow the evaluation process in your agent instructions.
    Write your report to Plans/features/{feature-id}-eval.md.
    Output the verdict, scores, and findings summary.
```

**After all evaluations complete:**
1. Collect verdicts and scores
2. Update feature-list.json: downgrade any FAILed features to `failing`
3. Append to `Plans/evaluator-scorecard.md` (create if doesn't exist, using format from evaluation-guide.md)
5. Report:

```
Evaluation complete:
--------------------------------------
+ config-parser      PASS    (gen: +15, eval: 0)
! data-loader        WARN    (gen: +12, eval: +3) -- missing edge case test
x core-calculation   FAIL    (gen: -10, eval: +17) -- reward hack detected!
+ output-generator   PASS    (gen: +13, eval: 0)
--------------------------------------
Generator: {total} | Evaluator: {total}

FAIL details:
  core-calculation: Hardcoded threshold at src/scoring.py:42 matches test
  expected value. Must compute from data per anti-goal #2.

Run /long-run next on failing features to fix them.
```

If the user disagrees with a finding, they can override it. Record overrides:
- "Dismiss as false positive" -> finding removed from scorecard
- "Dismiss as not worth fixing" -> finding recorded as note, not blocking
- "Confirm" -> no change, feature must be fixed

---

## Behavior: `/long-run reset`

Ask for confirmation: "Reset long-run for '{project name}'? This clears `.long-run.json` but keeps Plans/ artifacts. Type 'yes' to confirm."

If confirmed:
1. Delete `.long-run.json`
2. Keep Plans/ directory intact (specsheet, feature list, etc. may be useful)
3. Say: "Long-run reset. Plans/ artifacts preserved. Run `/long-run` to start a new project."

---

## Integration with Existing Infrastructure

| Component | How Long-Run Uses It |
|-----------|---------------------|
| `/office-hours` | Called DURING DECOMPOSE for each feature — stress-tests feature scope |
| `/plan-eng-review` | Called DURING DECOMPOSE for each feature — locks architecture and test matrix |
| `/pi-stack` | Called by `/long-run next` for ALL features — orchestrated mode starting at implement |
| `modular-worker` | Called by `/long-run parallel` for S/M features in worktrees |
| Ralph loop | Combine: `/ralph-loop "/long-run next --autonomous"` for overnight runs |
| `.pi-stack.json` | Separate from `.long-run.json` — pi-stack tracks per-feature execution phases |

**Key principle:** Long-run owns the interview and planning (decompose). Pi-stack owns the quality pipeline (implement through ship). The handoff point is the enriched feature brief with its locked plan.

---

## Important Rules

1. **Always read state before acting.** Read `.long-run.json` and `Plans/feature-list.json` every time.
2. **Always write state after acting.** Every status change must be persisted to both files.
3. **Respect dependencies.** Never start a feature whose dependencies haven't passed.
4. **Test-explain is mandatory.** Every feature produces a test explanation document. No exceptions.
5. **Don't skip the interview.** The specsheet quality determines everything downstream. Spend time here.
6. **Don't skip per-feature specs.** Every feature gets office-hours + plan-eng-review during decompose. This is the whole point of using long-run.
7. **Anti-goals are sacred.** They flow from specsheet -> feature briefs -> evaluator checks. Never ignore them.
8. **Commit after every feature.** Each feature gets its own commit (or commit series for L/XL).
9. **`.long-run.json` goes in .gitignore.** It's local state. `Plans/` directory is committed.
10. **One project at a time.** If a state file exists, resume it or reset before starting new.
11. **Autonomous mode stops on failure.** Never blindly continue past a failing feature.
12. **All AskUserQuestion calls use lettered options.** A) B) C) format, 2-4 options, with a RECOMMENDATION line. Follow the Pi-Stack Conventions in CLAUDE.md.

Follow the AskUserQuestion format (see CLAUDE.md Pi-Stack Conventions) for all interactive questions.

---

## Gotchas

> **This section is append-only.** Add new entries when dispatching failures occur. Never remove entries -- they prevent regressions.

1. **Pi-stack state file must be pre-created.** If you invoke `/pi-stack` without first writing `.pi-stack.json` via the create script, pi-stack will block waiting for user input to describe the feature — which defeats the purpose of autonomous execution.

2. **Pi-stack starts at implement, not plan.** The plan is already locked in the enriched brief from decompose. The create script skips ideation, question, AND plan. If pi-stack starts at plan, it will re-do work that was already approved by the user.

3. **Don't pass feature context as Skill args.** The Skill tool `args` field is for subcommands (e.g., `"next"`), not for passing long feature descriptions. Put context in `.pi-stack.json` and reference files — pi-stack reads those.

4. **Pi-stack's ship phase creates PRs.** When orchestrated by long-run, pi-stack should skip PR creation (long-run manages commits). Set `"skip_ship_pr": true` in `.pi-stack.json` to signal this.

5. **Always clean up `.pi-stack.json` after pi-stack completes.** Long-run owns the state lifecycle — if you leave a stale `.pi-stack.json`, the next `/pi-stack` invocation will try to resume it instead of starting fresh for the next feature.

6. **Parallel dispatch (modular-worker) is different from pi-stack dispatch.** The `parallel` section has a concrete Agent tool call template using modular-workers. Sequential execution (`next`) uses the Skill tool to invoke pi-stack. Don't confuse the two patterns.

7. **Decompose is multi-step — don't try to do it all in one invocation.** Each `/long-run decompose` call processes one sub-step: the initial breakdown, OR one feature's office-hours, OR one feature's plan-eng-review, OR one feature's approval. State tracking in `decompose_progress` knows where you are.

8. **Per-feature interviews are the whole point.** If you skip office-hours or plan-eng-review during decompose to "save time," the specs will be weak and execution will produce wrong results. The user chose /long-run specifically because they want thorough planning. Never skip the per-feature interviews.

9. **Enriched briefs must include the locked plan.** After plan-eng-review, the plan (architecture, data flow, edge cases, test matrix) must be saved INTO the feature brief. The execution phase reads ONLY the brief — if the plan isn't there, Claude has no architectural guidance during implementation.

---

## Self-Improvement Protocol

When a dispatching failure occurs during `/long-run next` (pi-stack didn't start correctly, stalled at a phase, produced unexpected output, or failed to complete):

1. **Diagnose**: Read `.pi-stack.json` to identify where the failure happened
2. **Abstract**: Determine the root cause (missing state? wrong invocation? context loss?)
3. **Record**: Append a new numbered entry to the Gotchas section above with:
   - What went wrong (concrete, not vague)
   - Why it went wrong (root cause)
   - How to prevent it (specific instruction)
4. **Inform the user**: Mention the new gotcha so they know the skill is learning

This protocol also applies to decompose failures (skill invocation issues), evaluation failures, and parallel dispatch failures. Any repeatable failure pattern deserves a gotcha entry.

**Compounding effect:** Each session reads the Gotchas before dispatching, avoiding previous failures. Over time, the skill accumulates corrections and becomes more reliable — without needing manual intervention.

---

## Completion

End with status: **DONE** / **DONE_WITH_CONCERNS** / **BLOCKED** / **NEEDS_CONTEXT**
