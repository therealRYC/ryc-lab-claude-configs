<!-- Created: 2026-03-03 -->
<!-- Last updated: 2026-03-17 — Replace retro type with completion type -->

---
name: notebook
description: "Append a lab notebook entry. Use when: the user asks to document, capture, or record work; after plan-to-execution transitions; when research findings are produced; when a session involves substantive work and is ending; when the user says 'add to notebook' or similar. Also handles retrospectives."
user-invocable: true
argument-hint: "[topic or type: topic] (types: plan, research, completion)"
---

# Lab Notebook Entry

Append a new entry to `NOTEBOOK.md` in the project root.

**Argument**: $ARGUMENTS

## Before Writing

1. **Check NOTEBOOK.md exists**. If not, invoke the `notebook-init` skill first to create it.
2. **Determine entry type** from argument prefix or conversation context:
   - `plan: topic` → Plan capture (plan + research context + decision rationale)
   - `research: topic` → Research findings (literature, deep research, analysis results)
   - `completion: topic` → Task completion (plan vs. reality, deviations, bugs, fixes)
   - No prefix or plain topic → General session entry
   - If ambiguous, infer from conversation context. Most entries are general.
3. **Get timestamp**: `date '+%Y-%m-%d %H:%M'` — entries always get date AND time.
4. **Collect recent commits** from this session: `git log --oneline --since="4 hours ago" --author="Robert" 2>/dev/null | head -10` (adjust timeframe if needed). These go in the Related Commits section.

## Entry Format

Append a horizontal rule (`---`) and the entry after the last entry in NOTEBOOK.md.

### General Session Entry

```markdown
---

### YYYY-MM-DD HH:MM — {Topic}

**Type**: session
**Status**: completed
**Tags**: [{relevant, topic, tags}]

**Goal**: {What we were trying to accomplish — one sentence}

**Approach**: {What we did and why we chose this approach. Be specific about methods and reasoning. 2-4 sentences.}

**Key findings**:
- {Finding 1}
- {Finding 2}

**Decisions made**:
- {Decision}: {Reasoning} (over {alternatives considered})

**Artifacts**:
- `{path/to/file}` — {what it is}
- `{path/to/figure}` — {what it shows}

**Related commits**:
- `{sha7}` — {commit message}

**Open questions**:
- {Anything unresolved}

**Next steps**:
- {What to do next}
```

### Plan Entry (type: plan)

Use when transitioning from plan mode to execution, or when the user asks to capture a plan.

```markdown
---

### YYYY-MM-DD HH:MM — Plan: {Topic}

**Type**: plan
**Status**: active
**Tags**: [{relevant, topic, tags}]

**Scientific question**: {What question is this plan addressing?}

**Background/motivation**: {Why this matters, what led to this. Include key research findings from the session if any deep research or literature analysis was done.}

**Approach**:
{Summarize the plan. Include key steps, tools, and methods. If a plan file exists in Plans/, link to it.}

**Key decisions**:
- {Decision}: {Reasoning} (over {alternatives considered})

**Research context**:
- {Key findings from literature or deep research that informed the plan}
- {Link to papers, preprints, or tools discovered}

**Success criteria**: {How we'll know if this worked}

**Plan file**: `{Plans/YYYY-MM-DD_topic.md}` (if one exists)

**Related commits**:
- `{sha7}` — {commit message}
```

### Research Entry (type: research)

Use after deep research, literature analysis, or `/analyze-literature`.

```markdown
---

### YYYY-MM-DD HH:MM — Research: {Topic}

**Type**: research
**Status**: completed
**Tags**: [{relevant, topic, tags}]

**Question**: {What were we investigating?}

**Sources consulted**:
- {Paper/tool/resource 1} — {key finding}
- {Paper/tool/resource 2} — {key finding}

**Summary of findings**:
{2-6 sentences synthesizing what we learned. Focus on what's actionable.}

**Implications for our work**:
- {How this affects our approach}

**Key references**:
- [{Author et al., Year, Title}]({DOI or URL})

**Open questions**:
- {What we still don't know}
```

### Completion Entry (type: completion)

Post-mortem for any finished work — planned or unplanned. Captures what was done,
what went wrong, how it was fixed, and lessons learned. Triggered automatically by
the post-completion Stop hook, or manually via `/notebook completion:`. Also the
target when the user says "retro", "retrospective", or "post-mortem".

If a plan exists, compare plan vs. reality. If no plan exists, skip the plan/deviations
sections and focus on what was done, what broke, and what was learned.

```markdown
---

### YYYY-MM-DD HH:MM — Completion: {Topic}

**Type**: completion
**Status**: completed
**Tags**: [{relevant, topic, tags}]

**Plan**: `{Plans/YYYY-MM-DD_topic.md}` *(omit this line if no plan existed)*

**Goal**: {What we set out to accomplish}

**What was done**:
- {Completed work item — be specific about files, functions, methods}
- {Another completed item}

**What worked well**:
- {Approach, tool, or decision that paid off — and why}

**What didn't work / failed attempts**:
| What Failed | Why | What Worked Instead |
|-------------|-----|---------------------|
| {approach that didn't work} | {why it failed} | {what replaced it} |
| "Nothing — clean execution" if no failures | | |

**Plan deviations** *(only if a plan existed)*:
| Planned | Actual | Why |
|---------|--------|-----|
| {what was planned} | {what happened instead} | {reason for deviation} |

**Bugs & fixes**:
| Bug | Attempted Fix | Outcome | Final Solution |
|-----|---------------|---------|----------------|
| {bug encountered} | {what was tried} | {did it work?} | {final fix and why} |
| "None encountered" if clean execution | | | |

**Key decisions**:
- {Decision}: {Why it was the right approach} (over {alternatives considered})

**Lessons learned**:
- {What to do differently next time}
- {Patterns to repeat}

**Artifacts**:
- `{path/to/file}` — {what it is}

**Related commits**:
- `{sha7}` — {commit message}

**Open questions**:
- {Anything unresolved}

**Next steps**:
- {What to do next based on results}
```

## After Writing the Entry

### Update the Decision Log

If the entry contains any **Decisions made** or **Key decisions**, append rows to the Decision Log table near the top of NOTEBOOK.md:

```markdown
| YYYY-MM-DD HH:MM | {Decision} | {Reasoning} | {Alternatives} |
```

Insert new rows at the END of the table (before any blank line after the table).

### Update the Last Updated timestamp

Change line 2 of NOTEBOOK.md:
```
<!-- Last updated: YYYY-MM-DD — {Brief description of entry} -->
```

### Auto-commit

```bash
git add NOTEBOOK.md && git commit -m "notebook: {Topic} (NOTEBOOK.md)"
```

The commit message format is always `notebook: {Topic}` — this enables `git log --grep="notebook:"` to find all notebook commits.

### Report to user

Briefly confirm: "Added notebook entry: {topic}" with the timestamp.

## Status Field

Every entry gets a `**Status**` field. This prevents future sessions from misreading historical entries (e.g., treating an abandoned approach as a current plan).

**Valid values**:
- `completed` — Work is done, results are final. Default for session and research entries.
- `active` — In progress or current. Default for new plan entries.
- `abandoned` — Tried and stopped. The entry explains why. **Do not implement approaches from abandoned entries.**
- `superseded` — Replaced by a later entry. Add `(see YYYY-MM-DD)` linking to the replacement. **Use the newer entry instead.**

**When to update status**: If a later session invalidates a previous entry (e.g., a plan was abandoned, or an approach replaced), update the old entry's status field in-place. This is the one case where editing a previous entry is expected.

## Content Guidelines

- **Pull from conversation context**: Read the full session to extract what was done, what decisions were made, what results looked like. The user should NOT have to re-explain what happened.
- **Be terse**: Bullet points over paragraphs. It's more important to capture quickly than to write beautifully.
- **Be specific**: Include actual parameter values, file paths, function names, error messages. Vague entries are useless.
- **Record failures**: Failed approaches are as valuable as successes. Always document what didn't work and why.
- **Link artifacts**: Every file created, modified, or generated should be listed with its path.
- **Omit empty sections**: If there are no open questions, don't include the heading. Keep entries lean.
- **Tags should be lowercase**, comma-separated, and reflect searchable concepts (e.g., `normalization`, `qc`, `variant-calling`, `dms`).

## Reading Guidelines (for future sessions)

When reading NOTEBOOK.md for project context, follow these rules:

1. **Check the Status field first.** Only treat `completed` and `active` entries as current. Ignore `abandoned` and `superseded` entries unless you need to understand what was already tried and why it failed.
2. **Newer entries take precedence.** If two entries address the same topic, the more recent one reflects the current state.
3. **Retro entries document failures.** The "What failed" table in retrospectives is explicitly *not* a plan — it's a record of what to avoid.
4. **Plans are not instructions.** A `plan` entry captures intent at a point in time. Always confirm with the user before executing an old plan — the context may have changed.
5. **When in doubt, ask.** If a notebook entry is ambiguous about whether something is current or historical, ask the user rather than guessing.
