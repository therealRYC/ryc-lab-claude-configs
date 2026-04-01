<!-- Created: 2026-02-23 -->
<!-- Last updated: 2026-02-23 — Initial creation -->

---
name: validate-data
description: Validate data files (CSV, TSV, VCF, FASTA, BED, H5AD) for integrity before analysis
user-invocable: true
allowed-tools: Read, Bash(python *), Bash(head *), Bash(wc *), Grep, Glob
argument-hint: "[file-path or directory]"
---

# Data Validation

Validate the data file(s) at: $ARGUMENTS

## Validation Steps:

### 1. File Basics
- File exists and is readable
- File size (warn if >1GB, error if empty)
- File encoding (UTF-8 expected)
- Line endings (warn on mixed)

### 2. Format-Specific Checks

**CSV/TSV:**
- Consistent column count across all rows
- Header row present and column names are unique
- Data types are consistent within columns
- Missing value patterns (NA, NaN, empty, ".", "-")
- Duplicate rows

**VCF:**
- Valid header (##fileformat, #CHROM line)
- Required columns present (CHROM, POS, ID, REF, ALT, QUAL, FILTER, INFO)
- Chromosome names are consistent (chr1 vs 1)
- POS values are positive integers
- REF/ALT contain valid nucleotides

**FASTA:**
- Valid header lines (start with >)
- Sequences contain only valid characters (ACGTUNRYSWKMBDHV for nucleotides)
- No empty sequences
- Unique sequence IDs

**BED:**
- Tab-delimited with at least 3 columns
- Start < End (0-based coordinates)
- Coordinates are non-negative integers

### 3. Summary Report
- Total records/rows
- Column summary (name, type, % missing, unique values for categoricals)
- Any warnings or errors found
- Recommendation: safe to proceed or needs attention
