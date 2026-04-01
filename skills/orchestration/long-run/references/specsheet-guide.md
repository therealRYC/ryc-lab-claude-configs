<!-- Created: 2026-03-25 -->
<!-- Last updated: 2026-03-25 — Initial creation -->

# Specsheet Guide: The Interview Template

The specsheet is the single most important artifact in a long-run project. A sharp specsheet enables hours of autonomous work; a vague one produces drift and reward hacking within minutes.

**Design principle (from He He):** "The better the specification, the longer the agent can run without intervention. It felt a bit like designing an ML course assignment — the task had to be achievable under the agent's constraints."

## The 6 Sharpening Questions

Work through ALL six questions in order. Each builds on the previous. Use AskUserQuestion for each question to keep the interview interactive.

### Question 1: Deliverable Definition

**Ask:** "What concrete artifact exists when this project is done?"

Not "what does it do" — what *thing* does the user hold at the end?

Push for specificity:
- Is it a Python package installable via pip?
- A CLI tool that takes X and produces Y?
- A pipeline that runs on a schedule?
- A report/notebook with specific figures?
- An API endpoint that serves predictions?
- A trained model with specific performance characteristics?

**What you're listening for:**
- Vague answers like "a tool that analyzes data" → push back: "What file format does it read? What does the output look like?"
- Overly ambitious answers → check against constraints in Q3
- The answer shapes the entire feature decomposition downstream

**Red flag:** If the user can't describe the deliverable in concrete terms, the project isn't ready for long-run. Suggest `/office-hours` first to find the right question.

### Question 2: Test Oracle

**Ask:** "How do you know it works? What specific thing will be true when this succeeds that isn't true now?"

Force a quantifiable success metric. This becomes the project-level acceptance criteria AND the basis for automated tests.

Types of test oracles (from Anthropic's long-running Claude research):
- **Reference implementation**: "Output matches CLASS within 0.1% accuracy"
- **Known-answer validation**: "On this specific input, the output should be exactly X"
- **Benchmark comparison**: "Performance exceeds baseline by N% on dataset Y"
- **Property-based**: "Output always has property X" (e.g., scores sum to 1.0, coordinates are within chromosome bounds)
- **Human judgment**: "I'll look at the output and it should look like..." (weakest — push for something more specific)

**What you're listening for:**
- "It should work correctly" → too vague. Push: "Correctly compared to what? Do you have reference data?"
- "I'll know it when I see it" → push for at least ONE quantifiable criterion
- Good answers produce test commands: `pytest tests/ -x -q` or `python validate.py --reference expected_output.tsv`

**Red flag:** No test oracle means no way for the agent to verify its own work. This is the #1 predictor of long-run failure.

### Question 3: Constraints & Resources

**Ask:** "What are the hard boundaries — compute, data, time, tech stack, dependencies?"

| Constraint | What to Ask | Why It Matters |
|------------|------------|----------------|
| **Compute** | Local laptop? HPC? GPU? How much RAM? | Determines parallelism, data size limits |
| **Data** | What exists? Formats? Sizes? Where is it? | Shapes data loading features |
| **Time horizon** | Afternoon? Week? Ongoing? | Determines depth of testing, docs |
| **Tech stack** | Python version? Required libraries? Existing code? | Prevents incompatible choices |
| **External deps** | APIs? Databases? Hardware? Auth required? | Features that need mocking/stubs |

**What you're listening for:**
- Contradictions between deliverable ambition and available resources
- Existing code that can be reused (avoid reinventing)
- Hard constraints that should become anti-goals (Q4)

### Question 4: Anti-Goals (Reward Hacking Prevention)

**Ask:** "What shortcuts should Claude NOT take? What would 'technically correct but wrong' look like?"

This is the He He lesson: agents will find the shortest path to satisfying the spec, even if it misses the intent. Explicitly define what success does NOT look like.

**Prompt the user with examples:**
- "Do NOT hardcode expected values or thresholds"
- "Do NOT skip validation by assuming clean input"
- "Do NOT solve this as a regression/fitting problem when the goal is a generalizable metric"
- "Do NOT mock the database in integration tests"
- "Do NOT use deprecated APIs even if they're simpler"
- "Do NOT optimize for the test cases at the expense of generalization"

**What you're listening for:**
- Domain-specific shortcuts the user has seen before
- Places where "technically passes the test" doesn't mean "actually works"
- These become constraints the evaluator agent checks against

**Critical:** Every anti-goal should be concrete and verifiable. "Don't take shortcuts" is useless. "Don't hardcode the threshold — it must be computed from the data" is verifiable.

### Question 5: Narrowest Wedge

**Ask:** "What's the smallest version that proves the architecture works end-to-end?"

Fight scope creep before it starts. Identify the 3-5 features that demonstrate:
1. Data can get in
2. The core computation works
3. Results can get out
4. The whole pipeline connects

**What you're listening for:**
- The user's instinct about what's essential vs. nice-to-have
- Which features are load-bearing (architecture) vs. decorative (polish)
- This shapes Wave 1 in the dependency graph

**Tip:** Frame it as "If you could only ship 3 features, which ones prove this works?"

### Question 6: Human Judgment Gates

**Ask:** "Where must Claude stop and ask you before proceeding?"

Not every decision can be automated. Identify the points where:
- Domain expertise is required (e.g., "which normalization method to use depends on the biology")
- Architectural choices have long-term consequences (e.g., "database schema is hard to change later")
- Reward hacking is most likely (e.g., "the scoring function is where shortcuts happen")
- The user explicitly wants oversight (e.g., "always show me the output before writing to production")

These become `"human_gate": true` flags in the feature list, where `/long-run next` will pause and use AskUserQuestion.

## Specsheet Output Format

After all 6 questions are answered, compile the specsheet and save to `Plans/specsheet.md`:

```markdown
# Specsheet: {Project Name}

**Generated:** {date}
**Author:** /long-run interview
**Session:** {session name if available}

## Vision
> {1-2 sentence description of what this project IS — from Q1}

## Deliverable
{Concrete artifact description — what exists when done}
{Include: file formats, expected outputs, how it's run}

## Success Criteria
- [ ] {Quantifiable criterion 1 — from Q2}
- [ ] {Quantifiable criterion 2 — from Q2}
- [ ] {Test oracle command: how to verify automatically}

## Constraints
| Constraint | Value |
|------------|-------|
| Compute | {from Q3} |
| Data | {from Q3} |
| Time | {from Q3} |
| Tech stack | {from Q3} |
| Dependencies | {from Q3} |

## Anti-Goals
> These are things Claude must NOT do, even if they technically satisfy the criteria.
> Each anti-goal has a verification method — a concrete way the evaluator checks compliance.

| Anti-Goal | Verification Method | Check Command |
|-----------|-------------------|---------------|
| {Anti-goal 1 — from Q4} | {how to verify} | `{grep/check command}` |
| {Anti-goal 2 — from Q4} | {how to verify} | `{grep/check command}` |
- {Anti-goal 3 — from Q4}

## Narrowest Wedge
{Description of the minimum viable feature set — from Q5}
{The first 3-5 features to implement, and why these prove the architecture}

## Human Judgment Gates
| Gate | When | Why |
|------|------|-----|
| {Gate 1} | {trigger condition} | {why human needed — from Q6} |
| {Gate 2} | {trigger condition} | {why human needed — from Q6} |

## Context
{Any background, prior work, related papers, existing code to build on}
{Gathered from README.md, NOTEBOOK.md, git log, and conversation}
```

## Interview Tips

- **Go in order.** The questions build on each other — deliverable before constraints, constraints before anti-goals.
- **Push back on vagueness.** A vague specsheet produces vague features. Better to spend 10 extra minutes sharpening than to debug reward hacking later.
- **Use AskUserQuestion** with options when possible — it's faster than open-ended questions.
- **Read existing project context** (README, NOTEBOOK, git log) before starting — don't ask questions the codebase already answers.
- **The anti-goals question is the most important.** Most long-run failures come from underspecified anti-goals. Spend extra time here.
