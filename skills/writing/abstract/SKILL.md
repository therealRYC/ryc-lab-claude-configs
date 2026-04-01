<!-- Created: 2026-03-18 -->

---
name: abstract
description: "Draft conference abstracts and talk scripts in Robert Chen's voice. Supports poster abstracts (ACNP, APA), poster audio scripts, data blitz talks (5 min), and platform talks (10-15 min)."
user-invocable: true
argument-hint: "[conference/topic | resume]"
---

# Abstract & Talk Writing — Robert Chen

Draft conference abstracts and talk scripts following evidence-based presentation principles.

**Arguments**: $ARGUMENTS

---

## Core Voice Profile

> Universal voice attributes. Read this before the abstract/talk-specific profile below.

### Identity

Robert is a Psychiatry resident (PGY-3 at UW) with a PhD in functional genomics. His brand: **rigorous enthusiasm** — excited about the science, honest about the limitations.

### Universal Rules

- Specific numbers earn trust — ROC, p-values, N — always include these
- Never fabricate data — abstracts require complete data at submission for most conferences
- "Big BUT" adapted: "However, several considerations temper these conclusions..."
- One key takeaway — the audience should remember one thing

---

## Abstract & Talk Voice Profile

### Tone Calibration

**Two distinct outputs with different voices:**

| Dimension | Abstract | Talk Script |
|-----------|----------|-------------|
| **Voice** | Formal, academic, compressed | Conversational, personal, narrative |
| **Goal** | Convince review committee | Connect with live audience |
| **Structure** | Background/Methods/Results/Conclusion | Story arc with tension and payoff |
| **"I" usage** | Rare — "we" predominates | Frequent — "Hi, I'm Rob..." |
| **Jargon** | Defined briefly in-line | Translated in real-time with analogies |

**Abstract mode**: 20% enthusiasm / 80% disciplined precision (closer to manuscript voice)
**Talk mode**: 60% enthusiastic educator / 40% precise scientist (closer to X Article voice)

### Abstract Voice Patterns

**Structured Abstract format**: Background → Methods → Results → Conclusion

**Background**: States the gap directly — no throat-clearing
> "Cognitive impairment is a hallmark of schizophrenia. Development of cognitive phenotyping has relied on large test batteries that are infeasible to deploy in clinical settings."

**Methods**: Precise but readable — includes N, study design, key measures, statistical approach
> "A total of 1,415 stable outpatient individuals with schizophrenia or schizoaffective disorder and 1,062 healthy counterparts were recruited by five laboratories..."

**Results**: Leads with the most important finding, includes specific numbers
> "A boosted generalized linear model performed best, achieving an ROC of 0.899... A minimal ML model using just two neurocognitive tasks achieved an ROC of 0.888, statistically indistinguishable from the full model (p=0.17)."

**Conclusion**: Concise implication + memorable framing
> "These findings support a 'less-is-more' approach to efficient cognitive profiling in schizophrenia."

**Abstract Quality Checklist:**
- [ ] Title under character limit, includes study design or key finding
- [ ] Background is ≤3 sentences — lead with the clinical problem, not background review
- [ ] N reported, effect sizes reported, appropriate statistical tests
- [ ] Conclusion does not exceed what data support
- [ ] Abbreviations minimized and defined on first use
- [ ] Meets conference-specific formatting requirements exactly
- [ ] Readable by someone outside the specific subfield

**Robert's Abstract Patterns to Preserve:**
- Leading with the clinical problem, not the method
- Including specific numbers (ROC, p-values, N)
- Closing with concrete future applications, not vague "more research is needed"
- Naming specific assessment tools and methods

### Talk Voice Patterns

**Opening Formula** (brand signature):
> "Hi, I'm Rob, I'm a [year] psychiatry resident at the University of Washington, and I'd like to share with you [a story / my efforts to / two stories] focused on [topic]."

This is a brand signature — casual, personal, frames research as narrative.

**The ABT Narrative Arc** (Olson, 2015):
```
"We know [established fact] AND [additional context].
 BUT [the gap / the tension / the unresolved question].
 THEREFORE, [what we did about it]."
```

The anti-pattern is "AAA" (And, And, And) — monotonous listing of facts with no narrative tension. Every talk needs a moment of tension (the "BUT") before the resolution.

**Example:**
> "Neurocognitive dysfunction is increasingly recognized as a core feature of schizophrenia [AND]. However, which domains are core and which are redundant remains unclear [BUT]. We applied machine learning to a large multi-site dataset to identify the minimal cognitive battery [THEREFORE]."

**Talk Time Budget:**

| Section | Data Blitz (5 min) | Short Talk (10 min) | Full Talk (15 min) |
|---------|-------------------|--------------------|--------------------|
| Hook / Intro | 30 sec | 1 min | 1.5 min |
| Setup / Methods | 30 sec | 1 min | 1.5 min |
| Results | 2 min | 4 min | 6 min |
| Payoff / So-What | 1 min | 2 min | 3 min |
| Conclusion + Close | 30 sec | 1 min | 1.5 min |
| Q&A buffer | 30 sec | 1 min | 1.5 min |

Key: Audiences retain only **1-2 takeaways** from a talk. Explicitly tell them what to remember.

**Explaining Methods Accessibly:**
- UMAP: "a dimensionality reduction method that compresses the 15 assessments into just two dimensions, allowing us to visualize whether there was global separation"
- Recursive feature elimination: "a method that sequentially removes features from a model until performance suffers significantly"
- ROC: "area under the receiver operating characteristic curve, or ROC"

**Guiding Attention:**
- "What you can appreciate is..."
- "What I hope you can appreciate..."
- "We wondered whether..." (curiosity framing before key analysis)

**Conclusion Pattern:**
1. Restate the key finding in one sentence
2. Methodological insight ("In contrast to traditional univariate analyses, ML leverages...")
3. Future applications (predicting conversion, tracking treatment response)
4. A memorable tagline ("Our results support a 'less-is-more' approach")

**Talk Rules — DO:**
- Start with personal intro — it's your brand
- Frame research as a **story** using the ABT arc, not a methods report
- Translate every technical term in real-time
- End with a memorable tagline
- Practice timing — data blitz must be exactly 5 minutes
- Speak at 100-120 words/minute (slower than conversation)
- Strategic pauses after key findings — let them land

**Talk Rules — DO NOT:**
- Read from slides verbatim
- Present methods before the audience understands why they should care
- Rush the conclusion — it's the most important part
- Skip limitations — address briefly but honestly
- Use manuscript voice in a talk — conversational is better here
- List future applications without grounding at least one emotionally

### Conference-Specific Guidelines

**ACNP (American College of Neuropsychopharmacology)**
- Audience: senior neuroscience and psychopharmacology researchers
- Expect mechanistic depth — this audience knows the biology
- Data blitz format: ~5 minutes, rapid-fire, emphasize novelty
- Include poster audio recording script
- Each data presentation: report N, effect size, power calculation

**APA (American Psychiatric Association)**
- Audience: practicing psychiatrists, trainees, researchers
- Emphasize clinical relevance
- Max 3,000 characters with spaces for abstract
- Max 150 characters for title
- Complete data required at submission — no "results pending"
- No references, citations, tables, or figures in abstract body
- 3+ peer-reviewed references from last 5 years required separately

**Department/University Presentations**
- Audience: mixed — more context needed
- Personal narrative is valued
- Q&A preparation: expect broad questions, not just technical ones

### Slide Design Principles

**Assertion-Evidence Format** — Replace topic-phrase headlines with sentence assertions:
- **BAD**: "Results"
- **GOOD**: "A two-test ML model matches the full 15-test battery (ROC 0.888 vs 0.899, p=0.17)"

**Cognitive Load** (Mayer principles):
- Max **6 elements per slide** — one idea per slide
- Narration + graphics (no competing on-screen text)
- Sans-serif font, high contrast, colorblind-friendly palette

**General Rules:**
- One idea per slide — if you need to say "and also," it's two slides
- Minimum 24pt body, 32pt titles
- Consistent color scheme
- No decorative images — every pixel earns its place

### Q&A Handling

- Lead with curiosity: "That's a great point — can you say more about [specific aspect]?"
- Validate before responding: "You're raising an important limitation..."
- Admit uncertainty honestly: "I'm not sure about that — it's worth investigating"
- Never attack the questioner; always engage the idea
- Repeat the question so everyone hears it

---

## Talk Structure Templates

### Data Blitz (5 minutes, ~5-6 slides)

```
SLIDE 1: Personal intro + problem statement
"Hi, I'm Rob... I'd like to share a story about [topic]"
[State the clinical problem and why current approaches fall short]

SLIDE 2: Study design (ONE sentence) + key visual
[Dataset, N, key measures — keep it brief]
"To tackle this problem, we..."

SLIDE 3: Main result visualization
[Show a key figure — UMAP, heatmap, forest plot]
"What you can appreciate here is..."

SLIDE 4: The punchline (biggest, simplest, most striking finding)
[Headline finding with specific numbers]
"Using just [X], we achieved [metric]..."

SLIDE 5: So-what + conclusion + contact info
[Restate finding → why it matters → QR code]
```

**What to cut in data blitz**: Detailed methods, multiple analyses (pick the ONE most compelling), literature review (one sentence of context is enough), caveats (save for Q&A).

---

### Platform Talk (10-15 minutes, ~12-15 slides)

```
SLIDES 1-2: Introduction & motivation
[Personal intro → clinical problem → scientific gap]
[Frame as a story: "Both questions stem from my deep curiosity about..."]

SLIDES 3-4: Background & prior work
[What's been done, what's missing]
[Use visuals — published figures with permission]

SLIDE 5: Study design
[Dataset, N, key measures, analytical approach]

SLIDES 6-8: Results (progressive reveal)
[Show key figures one at a time]
[Guide interpretation: "What you can appreciate is..."]
[Build from visualization → quantification → reduction]

SLIDES 9-10: Key findings & interpretation
[The "so what" — what does this change?]

SLIDE 11: Limitations & caveats

SLIDE 12: Future directions

SLIDE 13: Acknowledgments
[Mentors, collaborators, funding]
```

---

### Poster Audio Script (2.5-3 minutes, ~500-600 words)

```
[INTRO — 15 seconds]
"Thanks for stopping by my poster. I'm Rob..."
"I'm excited to tell you about [topic]"

[BACKGROUND — 30 seconds]
[State the problem accessibly, one paragraph]

[METHODS — 30 seconds]
[Study design, N, key measures]

[RESULTS — 60 seconds]
[Reference specific poster sections: "In the center of my poster..."]
[Highlight 2-3 main findings with numbers]

[CONCLUSION — 30 seconds]
[Restate key finding, future applications]
[Leave them with one memorable takeaway]
[Invite questions: "Happy to go deeper on any part — what interests you?"]
```

**Key principle**: The poster audio script is a conversation starter, not a monologue. Prepare a 2-minute version AND be ready to go deep on any section.

---

## Workflow (Phases 0–6)

### Phase 0: Setup

1. **Read voice profiles** above
2. **Create working folder**: `$CWD/YYMMDD_Conference_Topic/`
   - Example: `$CWD/260309_ACNP_Pharmotypes/`
3. **Scan context folder** for relevant materials
4. **Determine entry point from arguments**:
   - Empty → Phase 1 (Interview)
   - Topic/conference name → Phase 2 (Format) with that context
   - `"resume"` → Find most recent folder

### Phase 1: Interview

**Understand the submission:**
- What conference is this for? (ACNP, APA, department presentation, other)
- What format? (poster abstract, data blitz, platform talk, poster with audio)
- What's the deadline?
- What's the word/character limit for the abstract?
- Is the data complete, or is this a placeholder?

**Understand the research:**
- What's the study about? (one sentence)
- What's the key finding?
- Is there an existing manuscript this is based on?
- What's the "one thing" you want the audience to walk away with?

### Phase 2: Determine Format

| Format | Output |
|--------|--------|
| Poster abstract only | Structured abstract (Background/Methods/Results/Conclusion) |
| Poster + audio script | Structured abstract + 2.5-3 minute audio recording script |
| Data blitz | 5-minute talk script + slide outline |
| Platform talk | 10-15 minute talk script + slide outline |

### Phase 3: Research (if needed)

If the abstract requires additional context:
1. Check Zotero data for relevant papers (path in `~/.claude/writing/data_reference.md` if accessible)
2. Read context files if provided
3. Read the manuscript if one exists for this project

### Phase 4: Draft

**For Abstracts:**
Follow the structured format from Abstract Voice Patterns above:
- **Background**: State the gap directly — no throat-clearing
- **Methods**: N, design, key measures, statistical approach
- **Results**: Lead with most important finding, specific numbers
- **Conclusion**: Concise implication + memorable framing

Check: Does it meet the word/character limit? Typical: 250-500 words.

**For Talk Scripts:**
Follow the appropriate template:
- Data blitz: ~600-800 words, 5 minutes, 6 slides
- Platform talk: ~1,500-2,000 words, 10-15 minutes, 12-15 slides

Write the script with slide transition markers ("Advance" or "Break").

**For Poster Audio Scripts:**
Follow the Poster Audio Script template above. Open with "Thanks for stopping by my poster. I'm Rob..."

**Save:**
- `$CWD/YYMMDD_Name/abstract.md`
- `$CWD/YYMMDD_Name/talk_script.md` (if applicable)
- `$CWD/YYMMDD_Name/slide_outline.md` (if applicable)

### Phase 5: Slide Planning (for talks)

Provide a slide-by-slide plan:

```
## Slide 1: Title + Personal Intro
- Content: Title, name, affiliation
- Script: "Hi, I'm Rob..."
- Visual: Clean title slide with UW logo
- Timing: ~30 seconds

## Slide 2: The Problem
- Content: [clinical problem framed accessibly]
- Script: "[background paragraph]"
- Visual: [key statistic or image]
- Timing: ~30 seconds
```

### Phase 6: Review & Iterate

Ask Robert:
- "Does the abstract capture the key finding clearly?"
- "Is the talk script at the right level for this audience?"
- "Any data points that need updating?"
- "Want to practice timing?"

---

## Key Reminders

- **Never fabricate data** — abstracts require complete data at submission for most conferences
- **Check word/character limits** — conference systems enforce these strictly
- **Talk voice ≠ manuscript voice** — conversational, accessible, story-driven
- **One key takeaway** — the audience should remember one thing
- **Commit when finalized**: `draft: {Conference} abstract/talk ($CWD/YYMMDD_Name/)`
