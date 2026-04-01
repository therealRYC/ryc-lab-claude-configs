<!-- Created: 2026-02-23 -->
<!-- Last updated: 2026-02-23 — Initial creation -->

---
name: project-context
description: Fowler Lab research conventions. Use when working on deep mutational scanning, variant effect maps, protein function scores, MaveDB, or Enrich2 data.
user-invocable: false
---

# Fowler Lab Research Conventions

When working on DMS/variant effect data in this lab:

## Data Standards
- Variant notation: use HGVS format (e.g., p.Ala123Val)
- Score files: CSV with columns [hgvs_nt, hgvs_pro, score, se, epsilon]
- Always preserve raw data in data/raw/ — never modify in place
- Processed outputs go to data/processed/

## Analysis Conventions
- Set random seeds explicitly (np.random.seed or random.seed)
- Log all parameter choices to configs/ as YAML
- Use pathlib for all file paths
- Prefer pandas for tabular data, xarray for multidimensional

## Quality Control
- Check for batch effects before merging replicates
- Validate variant counts against expected library complexity
- Flag synonymous variants as internal controls

## Visualization
- Use matplotlib/seaborn for publication figures
- Save figures as both PNG (300 DPI) and SVG
- Use colorblind-friendly palettes (viridis, cividis)
