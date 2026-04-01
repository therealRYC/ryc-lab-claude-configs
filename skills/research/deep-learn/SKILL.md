<!-- Created: 2026-03-15 -->
<!-- Last updated: 2026-03-28 — Added mandatory reference verification protocol -->

---
name: deep-learn
description: "Rapidly learn any topic by mapping its intellectual landscape: core mental models, expert debates, and deep-understanding tests. Use when starting research in a new domain, preparing for a qualifying exam-style deep dive, or when you want to compress months of learning into a single session. Outputs a structured Brainstorm doc."
user-invocable: true
allowed-tools: Agent, Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch, ToolSearch
argument-hint: "[topic or research question]"
---

# Deep Learn — Accelerated Domain Mastery

Rapidly map the intellectual landscape of a topic using strategic questioning, then synthesize findings into a structured Brainstorm document.

**Topic**: $ARGUMENTS

## Philosophy

The difference between surface knowledge and deep understanding is not the amount of content consumed — it's knowing which questions to ask. This skill follows a structured question sequence that mirrors how domain experts actually think:

1. **Mental models** — the shared frameworks experts use
2. **Fault lines** — where experts disagree and why
3. **Depth probes** — questions that separate deep understanding from memorization
4. **Synthesis** — connecting everything into a coherent intellectual map

## Execution

### Phase 1: Research Sprint

Launch `deep-researcher` agents to gather comprehensive knowledge on the topic. Use maximum effort — search broadly across PubMed, bioRxiv, Google Scholar, and web sources.

Run **two parallel** deep-researcher agents:

**Agent A — Foundations & Reviews**:
> "For the topic '{topic}', find: (1) The most-cited review articles and foundational papers from the last 10 years, (2) Key textbook-level explanations of core concepts, (3) The historical development — how did understanding of this topic evolve? What were the key breakthroughs? Report the top 10-15 most important sources with full citations. Every source you report MUST have been returned by a tool call. For each citation, include the tool that found it and its PMID URL, DOI URL, or direct URL. Do not include any source you cannot verify via tool call. If you found fewer than 10 verifiable sources, report only those — do not pad with unverified ones."

**Agent B — Current Landscape & Controversies**:
> "For the topic '{topic}', find: (1) The most recent advances and active research frontiers (last 2-3 years), (2) Any ongoing debates, contradictory findings, or unresolved questions in the field, (3) Emerging methods, tools, or paradigm shifts. Report the top 10-15 most important sources with full citations. Every source you report MUST have been returned by a tool call. For each citation, include the tool that found it and its PMID URL, DOI URL, or direct URL. Do not include any source you cannot verify via tool call. If you found fewer than 10 verifiable sources, report only those — do not pad with unverified ones."

Wait for both agents to return before proceeding.

### Phase 2: Mental Model Extraction

Using ALL the gathered research, synthesize an answer to:

> **"What are the 5 core mental models that every expert in this field shares?"**

These are not facts or definitions. Mental models are the *frameworks* experts use to think about problems — the lenses through which they interpret data and make predictions. For each mental model:

- **Name it** — give it a clear, memorable label
- **Explain it** — what is the framework and how does it work?
- **Show why it matters** — what does this model let you see that beginners miss?
- **Ground it in evidence** — cite the key papers or findings that established this model
- **Give an example** — a concrete scenario where an expert would apply this model

### Phase 3: Debate Mapping

Using ALL the gathered research, synthesize an answer to:

> **"What are the 3-5 places where experts in this field fundamentally disagree, and what is each side's strongest argument?"**

For each debate:

- **Frame the disagreement** — what is the core question?
- **Side A** — position, strongest evidence, key proponents
- **Side B** — position, strongest evidence, key proponents
- **Why it matters** — what are the practical implications of each position?
- **Current trajectory** — which side has momentum and why?

Do not flatten nuance. If there are more than 2 sides, represent them all.

### Phase 4: Deep Understanding Questions

Generate exactly 10 questions that would **expose whether someone deeply understands this subject versus someone who just memorized facts**.

These questions should:
- Require applying mental models, not reciting definitions
- Test ability to reason about edge cases, exceptions, and counterexamples
- Probe understanding of *why*, not just *what*
- Include at least 2 questions that connect this field to adjacent domains
- Include at least 1 question about what we do NOT yet know

For each question, also prepare:
- **What a surface-level answer looks like** (the memorizer's response)
- **What a deep answer requires** (the key insight or reasoning chain)
- **Key sources** that contain the information needed

### Phase 5: Self-Test & Gap Analysis

Work through each of the 10 questions using the gathered source material. For each:

1. **Construct the best possible answer** from the evidence
2. **Identify gaps** — where is the evidence thin, contradictory, or missing?
3. **Flag follow-ups** — what additional research would strengthen this answer?

If any answer reveals a significant gap in the research gathered, launch an additional `deep-researcher` agent to fill that specific gap before continuing.

### Phase 5.5: Citation Audit

Before writing the brainstorm doc, build a citation audit table. For EVERY reference collected across Phases 1-5:

1. **Re-verify each citation with a direct tool call** — search PubMed, bioRxiv, or Google Scholar for the exact title. Confirm title, first author, year, and journal match.
2. **Record the result** in a structured table:

| # | Claimed Citation | Verification Tool | Verified? | Link | Notes |
|---|-----------------|-------------------|-----------|------|-------|
| 1 | Author et al., Year, Title | PubMed search | YES | https://pubmed.ncbi.nlm.nih.gov/PMID/ | |
| 2 | Author et al., Year, Title | bioRxiv search | NO — title not found | — | DROPPED |

3. **Drop every citation marked NO.** Do not include it in Phase 6.
4. **Include the audit table in the brainstorm doc** as a collapsed section at the end (under a `## Citation Audit` heading). This makes the verification trail inspectable.

This phase is non-negotiable. Every citation in the final doc must have a row in this table with Verified = YES and a clickable link.

### Phase 6: Synthesis — Write the Brainstorm Doc

Create `Brainstorm/YYYY-MM-DD_{topic-slug}.md` (create the `Brainstorm/` directory if needed).

Use this structure:

```markdown
# Deep Learn: {Topic}

**Date**: YYYY-MM-DD
**Session type**: Deep learning sprint
**Topic**: {Full topic description}

## Research Question

{What we set out to understand — frame it as a question}

## Sources Consulted

{Derived from the Citation Audit table — include ONLY references with Verified = YES.
Each entry must have: Author(s), Year, Title, Journal, and clickable link (copied from audit table).
Group by: Foundational / Recent / Reviews / Other}

## Core Mental Models

### 1. {Model Name}
{Full write-up per Phase 2 spec}

### 2. {Model Name}
...

(repeat for all 5)

## Where Experts Disagree

### Debate 1: {Question}
{Full write-up per Phase 3 spec}

### Debate 2: {Question}
...

(repeat for all debates)

## Deep Understanding Test

### Q1: {Question}
**Surface answer**: {What a memorizer would say}
**Deep answer**: {The real insight, grounded in evidence}
**Key sources**: {Citations}

### Q2: {Question}
...

(repeat for all 10)

## Gap Analysis

**Strong understanding**: {Areas where evidence is solid and clear}
**Weak spots**: {Areas where evidence is thin, contradictory, or missing}
**Open questions**: {What remains genuinely unknown in the field}

## Intellectual Landscape Map

{A synthesis paragraph (or two) that ties everything together: how the mental models
relate to each other, how the debates connect to the gaps, and where the field is
heading. This is the "if you only read one section" overview.}

## Follow-Up Directions

- {Specific papers to read next}
- {Adjacent topics worth exploring}
- {Questions to bring to a domain expert}

## Citation Audit

<details>
<summary>Verification trail (click to expand)</summary>

| # | Citation | Tool | Verified | Link |
|---|----------|------|----------|------|
| ... | ... | ... | ... | ... |

</details>
```

### Phase 7: Commit & Notebook

1. Auto-commit the brainstorm doc:
   ```bash
   git add "Brainstorm/YYYY-MM-DD_{topic-slug}.md"
   git commit -m "brainstorm: Deep learn — {Topic} (Brainstorm/YYYY-MM-DD_{topic-slug}.md)"
   ```

2. If a `NOTEBOOK.md` exists in the project root, invoke the `notebook` skill with:
   `research: Deep learn — {Topic}`
   Include a brief summary and link to the brainstorm file.

## Reference Verification Protocol — MANDATORY

Every reference in the final brainstorm doc MUST be tool-call verified. No exceptions.

1. **Every citation must have a link.** Papers get a PubMed URL (`https://pubmed.ncbi.nlm.nih.gov/{PMID}/`), DOI URL (`https://doi.org/{DOI}`), or direct URL from the source database. No link = do not cite.
2. **Phase 5.5 audit is the enforcement mechanism.** The Citation Audit phase (Phase 5.5) is the structured verification pass. Every citation must pass through the audit table before inclusion in Phase 6. The instructions here describe the *standard*; Phase 5.5 *enforces* it.
3. **deep-researcher agents inherit this rule.** The agent definition includes its own verification protocol. If an agent returns a reference without a link or that looks suspicious (e.g., plausible but oddly specific), re-verify it with a direct tool call before including it in the final doc.
4. **"Sources Consulted" section is auditable.** Every entry must include a clickable link. A reader should be able to click each link and land on the actual paper.

## Rules

- **Max effort on research.** Do not cut corners. Use multiple deep-researcher agents in parallel. Search broadly.
- **Never fabricate citations.** Every source must come from actual search results AND be verified with a tool call. If a search returns nothing, say so.
- **Distinguish evidence quality.** Flag preprints, note small sample sizes, mark conflicting findings.
- **Be intellectually honest.** If the field is genuinely uncertain about something, say so. Do not manufacture false confidence.
- **Write for future-you.** The brainstorm doc should be useful months later. Be specific, cite everything with links, explain reasoning.
- **No interaction needed.** This skill runs autonomously from start to finish. The user kicks it off and gets a complete deliverable.
