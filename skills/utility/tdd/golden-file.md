# Golden-File Testing (pytest-regressions)

Use for: **regression detection on complex outputs** — DataFrames, arrays, pipeline results, any output too complex to assert field-by-field.

Run your code once, save the output as a "golden file." Future runs compare against this reference. If the output changes unexpectedly, the test fails.

## Why This Matters

When your function produces a 1000-row DataFrame, you can't write `assert result == expected` for every cell. Golden-file testing catches unintended changes automatically. It's the safety net that prevents "I only changed the normalization but accidentally broke the filtering too."

**Critical caveat**: Golden tests verify **consistency**, not **correctness**. If your initial output is wrong, the golden file enshrines the bug. Always independently verify the golden file is correct before committing it.

## Install

```bash
pip install pytest-regressions
```

## Core Pattern: DataFrame Regression

```python
def test_fitness_pipeline_output(dataframe_regression):
    """Guards against unintended changes to pipeline output.

    The golden file was verified against manual calculations on 2026-03-15.
    """
    raw_data = load_test_fixture("brca1_counts.csv")
    result = run_fitness_pipeline(raw_data)

    # pytest-regressions saves/compares the DataFrame automatically
    dataframe_regression.check(result)
```

On first run, this creates a golden file at:
`tests/test_pipeline/test_fitness_pipeline_output.csv`

On subsequent runs, it compares the current output against the golden file.

## Tolerance for Floating-Point

Scientific outputs will have minor floating-point variation. Configure tolerance:

```python
def test_enrichment_scores(dataframe_regression):
    """Guards against regression in enrichment calculation.

    Tolerance set to 1e-6 to allow minor floating-point variation
    across platforms while catching real computational changes.
    """
    result = compute_enrichment(test_data)
    dataframe_regression.check(
        result,
        default_tolerance=dict(atol=1e-6, rtol=1e-5),
    )
```

## NumPy Array Regression

```python
def test_correlation_matrix(ndarrays_regression):
    """Guards against changes to the correlation calculation."""
    matrix = compute_correlation_matrix(expression_data)
    ndarrays_regression.check({"correlation": matrix}, default_tolerance=dict(atol=1e-8))
```

## File Regression (Text Outputs)

```python
def test_summary_report(file_regression):
    """Guards against changes to report formatting and content."""
    report = generate_summary_report(experiment_data)
    file_regression.check(report, extension=".txt")
```

## When to Update Golden Files

Golden files need updating when you **intentionally** change behavior:

```bash
# Regenerate all golden files (after verifying changes are correct)
pytest --force-regen
```

**Before running `--force-regen`:**
1. Understand WHY the golden file changed
2. Verify the new output is correct (not just different)
3. Review the diff between old and new golden files
4. Commit the updated golden files with a message explaining the change

## Directory Structure

```
tests/
├── test_pipeline.py
├── test_pipeline/                    # Auto-created by pytest-regressions
│   ├── test_fitness_pipeline_output.csv   # Golden DataFrame
│   ├── test_enrichment_scores.csv         # Golden DataFrame
│   └── test_correlation_matrix.npz        # Golden NumPy array
```

Golden files go in version control. They ARE your regression baseline.

## Combining with Other Methodologies

Golden-file testing works best as a **safety net on top of** property-based and contract-based tests:

```python
# Property test: checks mathematical invariant (always true)
@given(...)
def test_normalization_preserves_total(data):
    ...

# Contract test: checks schema at boundaries (always true)
@pa.check_output(normalized_schema)
def normalize_counts(df):
    ...

# Golden-file test: catches ANY unintended change (regression)
def test_normalization_golden(dataframe_regression):
    result = normalize_counts(fixture_data)
    dataframe_regression.check(result)
```

The property and contract tests tell you the code is correct. The golden-file test tells you nothing changed by accident.

## When NOT to Use Golden Files

- **Stochastic outputs**: Use seed-based testing instead (see [stochastic.md](stochastic.md))
- **Trivial outputs**: If you can assert the result in 2-3 lines, use an example test
- **Rapidly evolving code**: If the output changes every commit during active development, golden files create churn. Add them after the code stabilizes.
