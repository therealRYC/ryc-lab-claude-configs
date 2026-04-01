<!-- Created: 2026-02-23 -->
<!-- Last updated: 2026-02-23 — Initial creation -->

---
name: new-pipeline
description: Scaffold a new bioinformatics or data analysis project with standard directory structure
disable-model-invocation: true
user-invocable: true
argument-hint: "[project-name] [analysis-type]"
---

# New Pipeline Scaffold

Create a new project called $0 for $1 analysis.

## Directory Structure:
```
$0/
├── src/                  # Core pipeline code (Python modules)
├── scripts/              # One-off utility scripts
├── data/
│   ├── raw/              # Immutable input data (never modify)
│   └── processed/        # Pipeline outputs
├── configs/              # Parameter files (YAML/JSON)
├── notebooks/            # Exploratory analysis (marimo or .py)
├── tests/                # Unit and integration tests
├── logs/                 # Pipeline run logs
├── figures/              # Publication-quality plots
├── Plans/                # Plan documents
├── .gitignore
└── README.md
```

## Requirements:
- Initialize git repo with worktree-ready main branch
- Create .gitignore (ignore data/raw/*, data/processed/*, logs/*, __pycache__, .env)
- Create README.md with project name, purpose, setup, and usage sections
- Create a minimal src/__init__.py and src/pipeline.py with docstrings
- If Python: include pyproject.toml with project metadata
- Add type hints and Google-style docstrings throughout
- Follow the file timestamp convention (Created + Last updated lines)

Confirm the structure with me before creating files.
