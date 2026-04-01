# Fowler Lab Claude Code Configs

Shared [Claude Code](https://docs.anthropic.com/en/docs/claude-code) configurations for computational biology research at the Fowler Lab, University of Washington. This repo gives you **216 skills**, **7 agents**, and **8 hooks** that turn Claude Code into a research-aware coding assistant for bioinformatics, data analysis, scientific writing, and more.

## Getting Started

### 1. Install

```bash
git clone https://github.com/therealRYC/ryc-lab-claude-configs.git
cd ryc-lab-claude-configs
./install.sh
```

This copies skills, agents, and hooks into `~/.claude/`. Existing configs are never overwritten unless you pass `--force`.

### 2. Personalize

Edit `~/.claude/CLAUDE.md` and fill in the placeholder fields at the top:

```markdown
## About Me
- [Your Name], [Lab Name], [Institution] ([your-email])
- Primary languages: Python and R
- [Describe your experience level]
- GitHub: [your-github-handle]
```

The rest of the file contains lab conventions (coding style, workflow rules, notebook practices) that work out of the box.

### 3. Restart Claude Code

Close and reopen Claude Code (or start a new session) to pick up the new skills. Type `/find-skills` to browse what's available, or just start working — many skills activate automatically when relevant.

### 4. Preview before installing (optional)

```bash
./install.sh --dry-run
```

Or install only the categories you want:

```bash
./install.sh --categories "core-workflow,research,bioinformatics,database-connectors"
```

---

## What Each Category Does

### Orchestration (1 skill)

**The big-picture coordinator.** `/long-run` manages multi-feature projects that span multiple coding sessions. It interviews you to build a specification, decomposes the project into features with a dependency graph, then dispatches each feature through the quality pipeline. Think of it as a project manager that sits above everything else.

> **Start here if:** You're building something with 3+ features or that will take more than one session.

### Core Workflow (17 skills)

**The quality pipeline.** This is the pi-stack — a 10-phase workflow adapted from Garry Tan's engineering quality gates for scientific computing. Each phase has its own skill:

| Phase | Skill | What it does |
|---|---|---|
| Ideation | `/office-hours` | Stress-tests whether you're solving the right problem (YC-style forcing questions adapted for research) |
| Scoping | `/pi-review` | Challenges your research question — is it testable? Is the scope right? |
| Planning | `/plan-eng-review` | Locks architecture, data flow, edge cases, and test matrices before any code is written |
| Debugging | `/investigate` | Systematic 4-phase debugging: Investigate, Analyze, Hypothesize, Fix. Iron rule: no fix without root cause |
| Review | `/code-review` | Paranoid pre-commit review focused on scientific correctness — catches silent data corruption, off-by-one errors in genomic coordinates |
| Testing | `/qa` | Test-fix-verify loop with before/after health scores. Three tiers: Quick, Standard, Exhaustive |
| Polish | `/elegance` | Code elegance audit with letter grades. Checks readability, Pythonic idiom, naming quality |
| Visuals | `/visual-review` | Reviews figures for publication readiness |
| Docs | `/doc-check` | Checks that documentation matches the current code |
| Ship | `/ship` | Pre-push quality gate: syncs with main, runs tests, verifies docs, opens a PR |

**Safety skills** (use anytime):
- `/careful` — shows what destructive commands are blocked vs require confirmation
- `/freeze` / `/unfreeze` — restricts edits to one directory (great for focused debugging)
- `/guard` — maximum safety mode (combines careful + freeze)

> **Most useful for day-to-day work:** `/investigate` (debugging), `/code-review` (before commits), `/ship` (before pushing). You don't need to run the full pipeline every time — use individual phases as needed, or `/pi-stack` to walk through them in order.

### Research & Learning (8 skills)

**Learn new domains and explore the literature.** These skills turn Claude into an interactive research partner.

| Skill | Highlight |
|---|---|
| `/deep-learn` | **Best first skill to try.** Rapidly maps the intellectual landscape of any topic: core mental models, expert debates, and deep-understanding tests. Compresses months of learning into one session. |
| `/analyze-literature` | Deep analysis of a single paper — methods, findings, limitations |
| `/literature-review` | Systematic review across PubMed, bioRxiv, arXiv with verified citations |
| `/scientific-brainstorming` | Structured creative exploration of research directions |
| `/hypothesis-generation` | Generates testable hypotheses from observations and literature |

> **Start here if:** You're entering a new research area or want to understand a paper deeply.

### Scientific Writing (10 skills)

**From first draft to submission.** Covers the full writing lifecycle with skills for each document type.

| Skill | Highlight |
|---|---|
| `/manuscript` | Full IMRAD manuscript drafting with proper citations |
| `/abstract` | Structured abstracts (background, methods, results, conclusions) |
| `/grant` | Grant proposal writing with specific aims, significance, and approach |
| `/scientific-writing` | Core writing engine — two-stage process (outline then prose), never bullet points |
| `/peer-review` | Simulates reviewer feedback on your manuscript |
| `/citation-management` | Manages references across documents |

### Lab Notebook (5 skills)

**Track your work like a lab notebook.** Each project maintains a `NOTEBOOK.md` that captures decisions, results, and session summaries.

| Skill | Highlight |
|---|---|
| `/notebook` | Append entries — auto-triggered after brainstorms, plans, and at session end |
| `/notebook-init` | Initialize a new project notebook |
| `/review-work` | Plain-English summary of what code changes did and why |
| `/project-context` | Summarizes the current state of a project for onboarding |

### Data Analysis (5 skills)

**Quality-first data work.** From validation through visualization.

| Skill | Highlight |
|---|---|
| `/validate-data` | Checks CSV, TSV, VCF, FASTA, BED, H5AD files for integrity before analysis |
| `/exploratory-data-analysis` | Auto-detects file type and generates detailed reports across 200+ scientific formats |
| `/statistical-analysis` | Guided test selection with assumption checking and APA-formatted results |
| `/scientific-visualization` | Publication-ready multi-panel figures with journal-specific formatting (Nature, Science, Cell) |

> **Use `/validate-data` early and often.** Catching a malformed VCF or truncated CSV before analysis saves hours of debugging.

### Database Connectors (36 skills)

**Query biological databases directly from Claude Code.** Each skill knows the schema, common queries, and best practices for its database. No need to look up API docs.

Key databases include:
- **Genomics:** Ensembl, gnomAD, ClinVar, GTEx, GEO, GWAS Catalog
- **Proteins:** UniProt, PDB, AlphaFold, InterPro, STRING
- **Pathways:** KEGG, Reactome, Monarch
- **Drugs/Chemistry:** ChEMBL, PubChem, DrugBank, ZINC, BindingDB
- **Literature:** PubMed, OpenAlex, arXiv, bioRxiv
- **Clinical:** ClinicalTrials.gov, FDA, ClinVar, ClinPGx

> **Example:** Type "find all missense variants in BRCA1 with ClinVar pathogenic classification" and the ClinVar skill handles the query construction.

### Bioinformatics Libraries (35 skills)

**Best-practice guidance for common bioinformatics tools.** Each skill knows the library's API, common workflows, and pitfalls.

Highlights:
- **Single-cell:** scanpy, anndata, scvi-tools, scVelo, CELLxGENE Census
- **Molecular:** RDKit, datamol, medchem, molfeat, DiffDock, ESM
- **Sequencing:** pysam, deeptools, polars-bio, TileDB-VCF
- **Genomics:** gget, Biopython, scikit-bio, etetoolkit (phylogenetics)
- **Survival/Clinical:** scikit-survival, PyHealth
- **Drug Discovery:** DeepChem, PyTDC, torchdrug

> **These skills don't replace reading the docs** — they give Claude deep knowledge of each library's API so it writes correct code on the first try instead of hallucinating function signatures.

### ML/AI Frameworks (13 skills)

Guidance for machine learning workflows: **scikit-learn**, **Transformers** (Hugging Face), **PyTorch Lightning**, **SHAP** (explainability), **torch-geometric** (graph neural networks), **stable-baselines3** (RL), and more.

### Scientific Computing (26 skills)

General-purpose scientific tools: **statsmodels**, **NetworkX**, **PyMC** (Bayesian), **SymPy** (symbolic math), **Polars** (fast dataframes), **Dask** (distributed computing), **pymatgen** (materials science), and quantum computing frameworks (Qiskit, Cirq, PennyLane).

### Lab Platform Integrations (14 skills)

Connect Claude to your lab infrastructure: **Benchling**, **Opentrons** (liquid handling robots), **protocols.io**, **DNAnexus**, **Latch Bio**, **OMERO** (imaging), **CELLxGENE Census**, and more.

### Document Generation (16 skills)

Create documents programmatically: **PDF**, **PPTX** (presentations), **DOCX**, **XLSX**, **LaTeX posters**, **scientific slides**, **infographics**, and web-based outputs.

### Domain-Specific (13 skills)

Specialized tools including **phylogenetics**, **clinical decision support**, **treatment plans**, **ISO 13485 certification** (medical devices), and financial data tools (Alpha Vantage, EDGAR, FRED).

### Utility (14 skills)

Meta-tools: `/find-skills` (browse available skills), `/tdd` (test-driven development), `/sandbox` (isolated experimentation), `/parallel-web` (concurrent web searches), `/retro` (weekly retrospectives).

### Visualization (3 skills)

Library-specific guidance for **matplotlib**, **seaborn**, and **plotly**. For publication-ready figures that combine multiple libraries, use `/scientific-visualization` from the Data Analysis category instead.

---

## Agents

Agents are autonomous subprocesses that Claude can dispatch for specialized tasks. They run in the background and return results.

| Agent | When it's used |
|---|---|
| **deep-researcher** | Literature search across PubMed, bioRxiv, and Europe PMC with verified citations. The workhorse behind `/deep-learn` and `/literature-review`. |
| **bug-tester** | Generates edge-case tests for your code, runs them, and reports bugs by severity. Automatically invoked by the quality pipeline. |
| **data-validator** | Validates data files (CSV, TSV, VCF, FASTA, BED) for integrity. Read-only — never modifies your data. |
| **modular-worker** | Implements a coding task in an isolated git worktree. Used by `/long-run` to parallelize independent features. |
| **long-run-evaluator** | Adversarial quality checker for `/long-run` features. Separate from the code generator to avoid self-evaluation bias. |
| **protocol-writer** | Drafts wet-lab and bioinformatics protocols using protocols.io as a reference. |
| **work-reviewer** | Produces plain-English explanations of what code changes did and why. Great for onboarding or reviewing someone else's work. |

---

## Hooks

Hooks run automatically on specific events — you don't invoke them manually.

| Hook | What it does |
|---|---|
| **validate-bash-command.py** | "Safe YOLO" mode — auto-approves safe commands, blocks destructive ones (`rm -rf`, `git push --force`), and prompts for confirmation on risky ones (`git push`, `pip uninstall`) |
| **check-sensitive-file.sh** | Prevents accidental edits to `.env`, credentials, and `.git/` internals |
| **freeze-boundary.py** | Enforces directory restrictions set by `/freeze` |
| **auto-format-code.sh** | Auto-formats Python (ruff/black) and R (styler) after every edit |
| **plan-mode-exit.sh** | Creates `Plans/` directory and sets up completion tracking when exiting plan mode |
| **post-completion.py** | Prompts you for a completion summary comparing the plan to what actually happened |
| **verify-pi-stack-handoff.py** | Validates that pi-stack skill dispatches are configured correctly |
| **notify-wsl.sh** | Desktop toast notifications on WSL *(optional — use `--include-wsl` to install)* |

---

## Top 5 Skills to Try First

These are the highest-impact skills in the toolkit — start here.

### 1. `/deep-learn` (Research)
Rapidly learn any topic by mapping its intellectual landscape: core mental models, what experts disagree about, and deep-understanding tests that verify you actually get it. Compresses months of reading into one interactive session. Outputs a structured Brainstorm doc you can reference later.

**Try it:** `/deep-learn` and give it a topic you're studying.

### 2. `/pi-stack` (Core Workflow)
The quality pipeline. Walk through 10 phases — from challenging whether you're solving the right problem (`/office-hours`) through code review, testing, and shipping. You don't have to run all 10 phases every time; use `/pi-stack` to see where you are and advance to the next phase, or jump directly to individual phases like `/investigate` or `/code-review`.

**Try it:** `/pi-stack` at the start of your next feature or analysis.

### 3. `/long-run` (Orchestration)
For projects bigger than a single feature. Interviews you to build a specification, decomposes the project into features with a dependency graph, then dispatches each feature through the quality pipeline — optionally in parallel using isolated git worktrees. Tracks progress across sessions.

**Try it:** `/long-run` when starting a multi-feature project or tool.

### 4. `/notebook` (Lab Notebook)
Maintains a `NOTEBOOK.md` in each project — a single-file lab notebook that captures decisions, results, and session summaries. Auto-triggers after brainstorm sessions and at session end. Use `/notebook completion:` for retrospectives that compare what you planned vs. what actually happened.

**Try it:** Say "add to notebook" after finishing a piece of work.

### 5. `/frontend-slides` (Document Generation)
Generates interactive HTML slide decks directly from your data and results. Great for lab meetings, journal clubs, and quick presentations without fighting with PowerPoint.

**Try it:** `/frontend-slides` after an analysis to turn results into a presentation.

---

## Install Options

```bash
./install.sh                                    # Install everything
./install.sh --dry-run                          # Preview without copying
./install.sh --categories "core-workflow,research,bioinformatics"  # Selective install
./install.sh --force                            # Overwrite existing configs
./install.sh --skip-agents --skip-hooks         # Skills only
./install.sh --include-wsl                      # Include WSL notification hook
```

## Updating

This repo uses **copies**, not symlinks. To get updates:

```bash
cd ryc-lab-claude-configs
git pull
./install.sh --force
```

## After Install

- **`~/.claude/CLAUDE.md`** — Fill in your personal details. The lab conventions work as-is.
- **`~/.claude/settings.json`** — Pre-configured permissions and hooks. Add `enabledPlugins` or `model` preferences as needed.
- **`/find-skills`** — Browse all installed skills from within Claude Code.
- **[CATALOG.md](CATALOG.md)** — Full index with descriptions for every skill.

## Repository Structure

Skills are organized by category here for browsability, but install **flat** into `~/.claude/skills/`:

```
# In this repo                          # After install
skills/orchestration/long-run/     ->   ~/.claude/skills/long-run/
skills/core-workflow/pi-stack/     ->   ~/.claude/skills/pi-stack/
skills/bioinformatics/scanpy/      ->   ~/.claude/skills/scanpy/
```

To regenerate the catalog after adding skills:

```bash
./generate-catalog.sh
```
