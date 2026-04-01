# Fowler Lab Claude Code Configs

Shared Claude Code configurations for computational biology research. Includes 216 skills, 7 agents, 8 hooks, and template settings for the Fowler Lab at the University of Washington.

## Quick Start

```bash
# Clone the repo
git clone https://github.com/therealRYC/ryc-lab-claude-configs.git
cd ryc-lab-claude-configs

# Install everything
./install.sh

# Or preview first
./install.sh --dry-run
```

After installing, edit `~/.claude/CLAUDE.md` to fill in your name, email, GitHub handle, and environment details.

## What's Included

### Skills (216 across 15 categories)

| Category | Count | Description |
|---|---|---|
| **Orchestration** | 1 | `/long-run` — project-level coordination above pi-stack |
| **Core Workflow** | 17 | `/pi-stack` pipeline: ideation through ship, plus safety skills |
| **Research** | 8 | `/deep-learn`, literature review, brainstorming, hypothesis generation |
| **Writing** | 10 | Manuscript, abstract, grant, peer review, citation management |
| **Notebook** | 5 | Lab notebook, project context, work review |
| **Data Analysis** | 5 | Data validation, EDA, statistics, scientific visualization |
| **Database Connectors** | 36 | PubMed, ChEMBL, UniProt, Ensembl, KEGG, gnomAD, ClinVar... |
| **Bioinformatics** | 35 | scanpy, anndata, RDKit, pysam, scvi-tools, ESM, DiffDock... |
| **ML/AI** | 13 | Transformers, scikit-learn, PyTorch Lightning, SHAP... |
| **Scientific Computing** | 26 | statsmodels, NetworkX, PyMC, SymPy, Qiskit... |
| **Lab Integrations** | 14 | Benchling, Opentrons, protocols.io, CELLxGENE Census... |
| **Document Generation** | 16 | PDF, PPTX, LaTeX posters, scientific slides, infographics |
| **Domain-Specific** | 13 | Phylogenetics, clinical decision support, financial data |
| **Utility** | 14 | find-skills, TDD, sandbox, parallel web search |
| **Visualization** | 3 | matplotlib, seaborn, plotly |

See [CATALOG.md](CATALOG.md) for the full list with descriptions.

### Agents (7)

| Agent | Purpose |
|---|---|
| **deep-researcher** | Literature search, evidence synthesis, multi-source comparison |
| **bug-tester** | Edge-case test generation, runs tests, reports bugs by severity |
| **data-validator** | Validates CSV, TSV, VCF, FASTA, BED files for integrity |
| **long-run-evaluator** | External quality evaluator for long-run features |
| **modular-worker** | Implements a single task in worktree isolation (for parallelism) |
| **protocol-writer** | Drafts wet-lab and bioinformatics protocols |
| **work-reviewer** | Plain-English explanations of what code changes did and why |

### Hooks (8)

| Hook | Trigger | Purpose |
|---|---|---|
| validate-bash-command.py | PreToolUse (Bash) | "Safe YOLO" — blocks dangerous commands, prompts for risky ones |
| check-sensitive-file.sh | PreToolUse (Edit/Write) | Blocks edits to .env, credentials, .git internals |
| freeze-boundary.py | PreToolUse (Edit/Write) | Enforces `/freeze` directory boundaries |
| auto-format-code.sh | PostToolUse (Edit/Write) | Auto-formats Python (ruff/black) and R (styler) |
| plan-mode-exit.sh | PostToolUse (ExitPlanMode) | Creates Plans/ directory and completion markers |
| post-completion.py | Stop | Prompts completion summary after plan-based work |
| verify-pi-stack-handoff.py | PostToolUse (Skill) | Validates pi-stack skill dispatches |
| notify-wsl.sh | Notification | Toast notifications on WSL (optional, use `--include-wsl`) |

## Install Options

```bash
# Install only specific categories
./install.sh --categories "core-workflow,research,bioinformatics"

# Overwrite existing configs
./install.sh --force

# Skip agents or hooks
./install.sh --skip-agents --skip-hooks

# Include WSL notification hook
./install.sh --include-wsl
```

The installer **never overwrites** existing skills, agents, or hooks unless you pass `--force`. If `~/.claude/settings.json` or `~/.claude/CLAUDE.md` already exist, the installer skips them and points you to the `.example` files for reference.

## Customization

### CLAUDE.md

The installed `CLAUDE.md` is a template with placeholder values. Fill in:
- Your name, email, and GitHub handle (lines 3-7)
- Your experience level with Python/R
- Your OS/environment
- Your git identity

The rest contains lab conventions (coding style, workflow rules, notebook practices, pi-stack protocols) that work as-is.

### settings.json

The template includes:
- **Permission lists** — pre-configured allow/deny/ask rules for common commands
- **Hook configurations** — all 8 hooks wired to their triggers
- **Defaults** — plan mode on, max effort level

You may want to add:
- `enabledPlugins` for any Claude Code plugins you use
- `model` preference if you have a specific model in mind

## Updating

This repo uses **copies**, not symlinks. To get updates:

```bash
cd ryc-lab-claude-configs
git pull
./install.sh --force   # overwrites existing with latest versions
```

## Regenerating the Catalog

After adding or modifying skills:

```bash
./generate-catalog.sh
```

This reads SKILL.md frontmatter and regenerates [CATALOG.md](CATALOG.md).

## Repository Structure

Skills are organized by category in this repo for browsability, but install **flat** into `~/.claude/skills/` (as Claude Code expects):

```
skills/
├── orchestration/long-run/       -> ~/.claude/skills/long-run/
├── core-workflow/pi-stack/       -> ~/.claude/skills/pi-stack/
├── bioinformatics/scanpy/        -> ~/.claude/skills/scanpy/
└── ...
```
