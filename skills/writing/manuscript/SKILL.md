<!-- Created: 2026-03-18 -->

---
name: manuscript
description: "Draft journal manuscripts — full workflow covering IMRAD drafts, cover letters, and response to reviewers. Supports empirical research, reviews, brief reports. Customize the voice profile below with your own background."
user-invocable: true
argument-hint: "[manuscript name | cover-letter | response | resume]"
---

# Manuscript Writing

Draft journal manuscripts following academic writing conventions.

**Arguments**: $ARGUMENTS

---

## Core Voice Profile

> Universal voice attributes. Read this before the manuscript-specific profile below.

### Identity & Positioning

[YOUR IDENTITY: Replace this with your background, research focus, and unique angle. Example: "A computational biologist at UW studying protein fitness landscapes. Writes at the intersection of deep mutational scanning, machine learning, and protein engineering."]

### Core Tone

The voice is **rigorous enthusiasm** — but manuscript mode shifts the expression dramatically:
- 20% understated enthusiasm / 80% disciplined precision
- More conversational than a dry academic paper, more rigorous than a blog post

### Universal Rules

- Use **specific numbers** for every claim — effect sizes, CIs, sample sizes
- Always provide **scale context** for numbers
- Use **active voice** overwhelmingly
- **C-C-C structure** (Context-Content-Conclusion) at every level: paragraph, section, whole paper
- Acknowledge limitations **specifically** — name the exact limitation
- **Data first, interpretation second** — don't mix Results and Discussion

---

## Manuscript Voice Profile

### Tone Calibration

| Core Voice Attribute | X Article Expression | Manuscript Expression |
|---------------------|---------------------|----------------------|
| Rigorous enthusiasm | "Mind-blowing" / "Absolutely wild" | "These findings suggest a fundamental reassessment of..." / "Notably, these results challenge..." |
| Accessible authority | Analogies, parentheticals | Precise definitions, in-text citations, structured logic |
| First-person stakes | "As a [your role] in [your city]..." | "In practice, these findings may inform..." |
| Intellectual humility | "And... I was wrong." | "These results should be interpreted in light of several limitations..." |
| The Big BUT | "BUT -- and it's a big BUT" | "However, several considerations temper these conclusions." |
| Contrarian curiosity | "'X is always bad' = dogma" | "Although [approach/method] has been historically characterized as [X], recent evidence suggests..." |

### Voice Rules

**DO:**
- Use **active voice** and **first person plural** ("we") for actions the authors took
- Lead every section with the most important information
- Define computational/genomic terminology for clinical audiences and vice versa
- Frame findings in terms of **what changes** — for clinicians: treatment implications; for scientists: mechanistic reframing
- Use **subheadings** generously in Methods and Results
- Write the abstract **last**, after the paper is complete

**DO NOT:**
- Use exclamatory markers ("mind-blowing," "game-changer") — these belong in popular writing
- Use rhetorical questions in the main text (save for rare Discussion flourishes)
- Use analogies/metaphors in Results or Methods (save for Introduction or Discussion, sparingly)
- Speculate beyond what the data support in Discussion
- Use "significant" without specifying statistical vs. clinical significance
- Begin sentences with "It is interesting that..." — just state the finding
- Repeat data from tables/figures verbatim in prose — text should highlight and interpret

### IMRAD Structure

**Introduction: The Funnel to Your Gap**

| Paragraph | Function | Rhetorical Move |
|-----------|----------|-----------------|
| 1 | Broad context | Why should anyone care about this disease/phenomenon? Establish stakes. |
| 2 | Narrow context | What has been done? What do we know? (Brief, not a literature review.) |
| 3 | The gap | What remains unknown, contradictory, or insufficient? This is the pivot. |
| 4 | This study | "In this study, we..." — exactly what you did and why it fills the gap. |

**Methods: Reproducibility Without Tedium**
- Subheadings are mandatory — group by logical phases
- Statistical methods get their own subsection — report tests, software, multiple comparison handling, significance thresholds
- Supplementary appendices for detailed protocols and sensitivity analyses
- Explain the "why" behind methodological choices

**Results: Data First, Interpretation Later**
- Lead each paragraph with **a finding, not a method** ("Abrupt discontinuation added 1.36 points..." not "We then analyzed...")
- Report **effect sizes with confidence intervals**, not just p-values
- Provide **clinical context** for effect sizes
- Structure each Results paragraph: question posed → data presented → answer derived
- Figure titles should communicate **conclusions**, not describe contents

**Discussion: Interpretation Without Overreach**

| Paragraph | Function |
|-----------|----------|
| 1 | Restate main findings in context of the gap from Introduction |
| 2-3 | Compare/contrast with existing literature |
| 4 | Limitations — honest, specific, not formulaic |
| 5 | Implications and future directions |

### Journal-Specific Expectations

**Nature / Cell / Science**
- Short introduction (1-2 paragraphs), lead with the question
- Abstract: unstructured, ~150 words, narratively compelling
- Tone: authoritative but accessible, storytelling valued

**NEJM / Lancet / JAMA**
- Abstract: **structured** (Background, Methods, Results, Conclusions), ~250 words
- CI required alongside p-values
- Reporting checklists mandatory
- Key question: "After this is published, physicians should do X differently"

**JAMA Psychiatry / Lancet Psychiatry**
- Best fit for your work: pharmacogenomics with clinical outcomes, [your research area]
- Lancet Psychiatry: write for "a reasonably well-read, general psychiatrist" — define computational/genomic terms

### Rhetorical Strategies by Paper Type

**Computational Psychiatry** — Open with the clinical problem, introduce computational methods as solutions to clinical problems, connect clusters/subtypes to actionable clinical categories.

**Pharmacogenomics** — Lead with the clinical gap in treatment selection, explain genomic methods for prescribing psychiatrists, report findings in terms of clinical decision-making.

**Translational Neuroscience** — Bridge bench and bedside explicitly; frame preclinical findings as therapeutic hypotheses; end Discussion with a translational roadmap.

**Review Articles** — More narrative freedom, more synthesis, more clearly-labeled opinion. Use the historical arc structure. Include speculative "Future Directions" section.

---

## Templates

### Template 1: Empirical Research Article (IMRAD)

```
TITLE
[Descriptive, specific, conveys the main finding — not a question]

ABSTRACT (Structured — for medical journals)
Objective: [Research question]
Methods: [Design, N, key measures, statistical approach]
Results: [Key findings with specific numbers, effect sizes, CIs]
Conclusions: [Clinical or mechanistic implication]

INTRODUCTION (3-4 paragraphs)
[P1: Broad context]
[P2: Narrow context — what's been done]
[P3: The gap]
[P4: "In this study, we..."]

METHODS
## Participants / Data Sources
## Measures / Variables
## Statistical Analysis
[Report tests, software, multiple comparison handling, α level]

RESULTS
[Lead each paragraph with a finding, not a method]
[Specific numbers: effect sizes, CIs, p-values with clinical context]
[Reference figures: "Figure 1 shows..." or "(Figure 1)"]

DISCUSSION (4-5 paragraphs)
[P1: Restate main findings in context of the Introduction gap]
[P2-3: Compare/contrast with existing literature]
[P4: Limitations — specific, honest, not formulaic]
[P5: Implications and future directions]

REFERENCES
```

---

### Template 2: Review Article

```
TITLE
[Broad but specific — conveys scope and perspective]

ABSTRACT (Unstructured for Nature/Science; Structured for medical journals)
[C-C-C: Context → Content → Conclusion]

INTRODUCTION (2-3 paragraphs)
[Hook with clinical or scientific relevance]
[Scope statement: what this review covers and why now]
[Roadmap: brief outline of sections]

BODY SECTIONS (3-6 sections with descriptive headers)
## [Historical Context / Discovery]
[Storytelling permitted here — narrative arc]
## [Mechanism / Biology]
[Progressive disclosure: name → define → explain why it matters → mechanism]
## [Preclinical Evidence]
[Organize by disease/indication, not chronologically]
## [Clinical Evidence]
[Hierarchy: RCTs > cohort studies > case series > case reports]
## [Future Directions]
[More speculative, opinion clearly labeled]

CONCLUSION (1-2 paragraphs)
[Synthesis, not summary. What the field needs next.]
```

---

### Template 3: Brief Report / Letter

```
TITLE

INTRODUCTION (1 paragraph)
[State the problem and what this study adds — no background review]

METHODS (1-2 paragraphs)
[Compressed but complete]

RESULTS (1-2 paragraphs)
[Key findings with numbers, reference to figure]

DISCUSSION (1-2 paragraphs)
[Interpret → Limitations → Clinical implication]
[Every sentence earns its place — extreme concision]
```

---

### Template 4: Cover Letter

```
Dear [Editor Name],

[Sentence 1: "We submit [title] for consideration as a [type] in [journal]."]

[THE DISCOVERY — 2-3 sentences]
[Lead with the finding, not the process. State central result with specific numbers.]
[Why it matters — what it changes, challenges, or enables.]

[WHY THIS JOURNAL — 2-3 sentences]
[Connect findings to this journal's specific scope and recent publications.]
[Explicit clinical implications for medical journals; bench-to-bedside bridge for translational journals.]

[FORMALITIES]
[Not published/submitted elsewhere. All authors approved.]
[Conflicts and funding.]
[Suggest 3-4 reviewers with rationale. Exclude conflicted reviewers with reasoning.]

Warmly,
[Your Name]
```

**Cover Letter Principles:**
- Lead with the **discovery**, not the process
- Be **specific about impact** with concrete numbers
- Do NOT reproduce the abstract
- The "Problem → Approach → Significance" structure is effective

---

### Template 5: Response to Reviewers

```
Dear [Editor],

We thank you and the reviewers for the thorough evaluation of our manuscript
"[Title]" (Manuscript ID: [XXX]). We have carefully addressed all comments.

SUMMARY OF MAJOR CHANGES
- [New analysis or data added]
- [Structural revision]
- [Key clarification]

---

REVIEWER 1

**Comment 1.1**: *[Quoted reviewer text in italics]*

[Direct answer first: "We agree and have..." or "We performed the requested analysis..."]
[Explanation with reference to revised manuscript location.]

> [Quoted revised text, indented]

In the revised manuscript, this appears on page X, lines Y-Z.
```

**Response Principles:**
1. Overview first, then full point-by-point reviews
2. Be polite regardless of reviewer tone
3. Accept the blame — if they misunderstood, the writing was unclear
4. Make responses self-contained — quote changes with page/line numbers
5. Respond to every point — never skip one
6. Lead with direct answers — "Yes" / "Done" / "We agree" before explaining
7. Draft privately first — never send the first emotional draft

---

## Workflow (Phases 0–7)

### Phase 0: Setup

1. **Read voice profiles** above
2. **Create working folder**: `$CWD/YYMMDD_Brief_Name/`
   - Example: `$CWD/260309_GLP1_Review/`
3. **Scan context folder** for relevant materials
4. **Determine entry point from arguments**:
   - Empty → Phase 1 (Interview)
   - Manuscript name → Phase 2 (Target Journal) with that context
   - `"cover-letter"` → Phase 5
   - `"response"` → Phase 6
   - `"resume"` → Find most recent drafts/manuscript/ folder

### Phase 1: Interview

Ask the user:
- What's the paper about? (one sentence summary of the finding)
- What type of manuscript? (empirical research, review, brief report, letter)
- What data/analyses are complete? What's still in progress?
- Is there an existing draft, or starting from scratch?
- Who are the co-authors and what's your role?
- What gap does this fill?
- What's the "so what" — why should a clinician or scientist change what they do?
- What are the biggest limitations you're already aware of?

### Phase 2: Target Journal

**If the user has a target journal:** Look up scope, word limits, figure limits, abstract format, and reporting requirements. Assess fit. Check voice adjustments (see Journal-Specific Expectations above).

**If the user needs help choosing:**

| Tier | Journal | Best for |
|------|---------|----------|
| Top general | Nature, Science, Cell | Paradigm-shifting discoveries |
| Top medical | NEJM, Lancet, JAMA | Practice-changing clinical data |
| Top translational | Nature Medicine, Nature Mental Health | Mechanism + clinical relevance |
| Top psychiatry | JAMA Psychiatry, Lancet Psychiatry | Clinical psychiatry research |
| Specialty | Biological Psychiatry, Neuropsychopharmacology | Mechanistic/computational work |
| Open access | PLOS Medicine, eLife, Nature Communications | Broad scope |

Recommend: Primary target (aim high), Secondary (realistic), Tertiary (reliable).

### Phase 3: Outline

```
# [Working Title]

**Target journal**: [journal name]
**Type**: [empirical / review / brief report / letter]
**Word limit**: [from journal guidelines]
**Figure limit**: [from journal guidelines]
**Abstract format**: [structured / unstructured]
**Reporting checklist**: [STROBE / PRISMA / CONSORT / none]

## Introduction
- P1 (broad context): [key point]
- P2 (narrow context): [key point]
- P3 (gap): [key point]
- P4 (this study): [key point]

## Methods
### [Subsection 1]
### Statistical Analysis

## Results
- Finding 1: [with anticipated figure/table]
- Finding 2: ...

## Discussion
- Main findings in context
- Comparison with literature: [key papers to address]
- Limitations: [list specific ones]
- Implications

## Figures/Tables Plan
- Figure 1: [description]
- Table 1: [description]
```

Present outline for the user's approval.

### Phase 4: Draft

Write the full manuscript following voice profile and selected template.

**Section-by-section approach:**
1. **Draft Methods first** — most objective section
2. **Draft Results** — led by findings, not methods
3. **Draft Introduction** — now that you know the results, frame the gap precisely
4. **Draft Discussion** — interpret, compare to literature, limitations, implications
5. **Draft Abstract last** — summarize the completed paper
6. **Draft Title** — specific, descriptive, conveys the main finding

**Quality checks:**
- [ ] Every claim has a specific number with confidence interval
- [ ] Active voice predominates
- [ ] No speculation in Results
- [ ] Limitations are specific and named
- [ ] Figures have conclusion-oriented titles
- [ ] Terms defined for the target audience
- [ ] One message per paper — everything serves the central claim
- [ ] Reporting checklist requirements met

**Save:**
- `$CWD/YYMMDD_Name/draft.md` — full manuscript text
- `$CWD/YYMMDD_Name/figures.md` — figure descriptions and specifications
- `$CWD/YYMMDD_Name/outline.md` — the approved outline

### Phase 5: Cover Letter

Write following Template 4 above. Save to `$CWD/YYMMDD_Name/cover_letter.md`

### Phase 6: Response to Reviewers

1. Read the reviews carefully — identify major vs. minor concerns
2. Categorize: Which comments require new analyses? Text changes? Rebuttal only?
3. Draft response following Template 5
4. Revise manuscript — make all changes, track them
5. Cross-reference — ensure every response references exact location of changes

Save to `$CWD/YYMMDD_Name/response_to_reviewers.md`

### Phase 7: Review & Iterate

Ask the user:
- "Does the draft capture the right level of formality for [target journal]?"
- "Any sections that feel over-claimed or under-claimed?"
- "Are the limitations fair and complete?"
- "Ready for co-author review, or do you want to revise first?"

---

## Key Reminders

- **Never fabricate citations or data** — flag as `[VERIFY]` or `[DATA]` if unsure
- **Manuscript voice ≠ X Article voice** — formal, precise, understated enthusiasm
- **One paper = one message** — ruthlessly cut anything that doesn't serve the central claim
- **Check journal guidelines** before finalizing — word limits, figure counts, reporting checklists
- **Commit when finalized**: `draft: {Manuscript Title} ($CWD/YYMMDD_Name/)`
