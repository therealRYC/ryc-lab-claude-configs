# Pi-Stack: Phase-Specific Notes

Detailed behavioral notes for each pipeline phase. The main SKILL.md has the
compact dispatch table; this file has the edge cases and special behaviors.

## Phase 0: `ideation` (optional)

- Invokes `/office-hours`
- Skip if the user already has a clear question or if in orchestrated mode
- Mark as `skipped` rather than leaving `pending`

## Phase 1: `question`

- Invokes `/pi-review`
- Challenges the research question before any code is written
- Skip in orchestrated mode (long-run's decompose already did this per feature via `/office-hours`)

## Phase 2: `plan`

- Invokes `/plan-eng-review`
- Locks architecture, data flow, edge cases, and test matrix
- Produces a plan document that subsequent phases reference
- Skip in orchestrated mode (long-run's decompose already locked the plan per feature via `/plan-eng-review` — the locked plan is embedded in the feature brief)

## Phase 3: `implement`

**Standalone mode** (`invocation_mode` absent or `"standalone"`):
- Claude implements the code using the plan from the previous phase
- Follow CLAUDE.md coding standards (type hints, docstrings, pathlib)
- Write tests alongside the implementation using realistic data
- Run the test oracle if one was defined during planning
- Advance to review when done — do NOT wait for user

**Orchestrated mode** (`invocation_mode: "orchestrated"`):
- See `references/orchestrated-mode.md` for full behavior
- Short version: implement autonomously, advance directly to review

## Phase 4: `review`

- Invokes `/code-review`
- 2-pass paranoid review (Critical + Informational)
- Bio-specific checks, scope drift detection

## Phase 5: `qa`

- Invokes `/qa`
- Run-break-fix loop with health scores
- Three tiers: Quick, Standard, Exhaustive
- Pass through any tier flags from the user (e.g., `--exhaustive`)

## Phase 6: `elegance`

- Invokes `/elegance`
- Code craft grades: readability, Pythonic idiom, scientific clarity, naming
- Claude Slop detection
- Report-only — grades but doesn't modify code

## Phase 7: `visual` (optional)

Before invoking `/visual-review`, check if the project has visual outputs:
- Look for figure files (.png, .jpg, .svg, .pdf) in output/figures directories
- Look for HTML presentations
- If no visual outputs found, ask: "No visual outputs detected. Skip this phase?"
- Mark as `skipped` if no visuals

## Phase 8: `docs`

- Invokes `/doc-check`
- Documentation freshness audit
- Checks docstrings match signatures, README accuracy, NOTEBOOK entries

## Phase 9: `ship`

**Standalone mode:**
- Invokes `/ship`
- Full quality gate: sync with main, run tests, verify docs, open PR
- On success, delete `.pi-stack.json` and celebrate

**Orchestrated mode:**
- See `references/orchestrated-mode.md` for full behavior
- Short version: run quality checks, commit, but skip PR and keep state file

## Side-quest: `investigate`

`/pi-stack investigate` is not a pipeline phase — it's a debugging interrupt:
1. Record the current phase in `.pi-stack.json` (add `"investigating": true`)
2. Invoke `/investigate` with any arguments passed through
3. When investigate completes, remove the `investigating` flag
4. Resume the pipeline at the phase where it was paused
5. Show: "Investigation complete. Resuming pipeline at {phase}."
