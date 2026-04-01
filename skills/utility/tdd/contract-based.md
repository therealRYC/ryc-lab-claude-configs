# Contract-Based Testing (Pandera)

Use for: **data pipeline stages** — any function that transforms a DataFrame.

Contracts define what data MUST look like at each pipeline boundary. When Step 3 produces NaN values that would normally propagate silently to Step 7, a contract catches it at the source.

## Why This Matters

In scientific pipelines, bugs often manifest as *valid-looking but wrong data* — a column of fitness scores that should be in [-10, 10] quietly drifts to [-1000, 1000] after a normalization bug. Pandera catches this at runtime.

## Install

```bash
pip install pandera
```

## Core Pattern: Schema Definition

```python
import pandera as pa
from pandera.typing import DataFrame, Series


# Define what valid fitness data looks like
fitness_schema = pa.DataFrameSchema({
    "variant_id": pa.Column(
        str,
        pa.Check.str_matches(r"^[A-Z]\d+[A-Z]$"),  # e.g., "A2T", "G5R"
        nullable=False,
        description="Single amino acid substitution in standard notation",
    ),
    "fitness_score": pa.Column(
        float,
        pa.Check.in_range(-10.0, 10.0),
        nullable=False,
        description="Log-ratio fitness score relative to wildtype",
    ),
    "replicate": pa.Column(
        int,
        pa.Check.in_range(1, 10),
        nullable=False,
    ),
    "count": pa.Column(
        int,
        pa.Check.greater_than_or_equal_to(0),
        nullable=False,
    ),
})
```

## Using Schemas as Decorators

```python
import pandera as pa


# Validate input AND output of a pipeline function
@pa.check_input(raw_counts_schema)
@pa.check_output(fitness_schema)
def compute_fitness_scores(raw_counts: pd.DataFrame) -> pd.DataFrame:
    """Transform raw sequencing counts into fitness scores.

    Args:
        raw_counts: DataFrame with variant_id, input_count, output_count columns.

    Returns:
        DataFrame with variant_id, fitness_score, replicate, count columns.
    """
    # ... transformation logic ...
    return result
```

Now any call to `compute_fitness_scores` automatically validates:
- The input matches `raw_counts_schema`
- The output matches `fitness_schema`
- Failures raise `pa.errors.SchemaError` with a clear message

## Schema Patterns for Scientific Data

### Sequencing Count Data
```python
count_schema = pa.DataFrameSchema({
    "variant": pa.Column(str, nullable=False),
    "input_count": pa.Column(int, pa.Check.greater_than_or_equal_to(0)),
    "output_count": pa.Column(int, pa.Check.greater_than_or_equal_to(0)),
    "total_reads": pa.Column(int, pa.Check.greater_than(0)),  # Must have reads
})
```

### Normalized Scores
```python
normalized_schema = pa.DataFrameSchema({
    "variant": pa.Column(str, nullable=False, unique=True),
    "score": pa.Column(float, nullable=False),
    "se": pa.Column(float, pa.Check.greater_than(0), nullable=False),
    "n_replicates": pa.Column(int, pa.Check.in_range(1, 100)),
})
```

### Custom Checks
```python
# Check that wildtype variant exists in the data
has_wildtype = pa.Check(
    lambda s: "WT" in s.values,
    error="DataFrame must contain a wildtype (WT) row",
)

schema = pa.DataFrameSchema({
    "variant": pa.Column(str, checks=has_wildtype),
    "score": pa.Column(float),
})
```

### Statistical Checks
```python
# Pandera can test distributional properties
schema = pa.DataFrameSchema({
    "z_score": pa.Column(
        float,
        checks=[
            pa.Check.in_range(-10, 10),
            # Mean should be near zero for z-scores
            pa.Check(lambda s: abs(s.mean()) < 1.0,
                     error="Z-scores should be roughly centered on zero"),
        ],
    ),
})
```

## Writing Tests with Schemas

```python
import pytest
import pandas as pd
import pandera as pa


def test_fitness_pipeline_produces_valid_output():
    """Guards against schema violations from the fitness scoring pipeline.

    Validates column types, value ranges, and non-null constraints.
    """
    raw_data = pd.DataFrame({
        "variant": ["WT", "A2T", "G5R"],
        "input_count": [1000, 500, 750],
        "output_count": [900, 200, 1100],
    })
    result = compute_fitness_scores(raw_data)
    fitness_schema.validate(result)  # Raises SchemaError on failure


def test_fitness_pipeline_rejects_negative_counts():
    """Guards against upstream bugs that produce negative counts."""
    bad_data = pd.DataFrame({
        "variant": ["WT", "A2T"],
        "input_count": [1000, -5],  # Invalid!
        "output_count": [900, 200],
    })
    with pytest.raises(pa.errors.SchemaError):
        compute_fitness_scores(bad_data)
```

## When to Use Contracts vs. Other Methods

| Situation | Use Contracts? |
|-----------|---------------|
| Function takes/returns a DataFrame | **Yes** — define input/output schemas |
| Function is a pure math calculation | No — use property-based testing |
| Validating external data on load | **Yes** — schema on ingestion |
| Testing a specific edge case | No — use example-based test |
| Checking pipeline stage boundaries | **Yes** — this is the sweet spot |

## Performance Note

Schema validation adds runtime overhead. For production pipelines processing millions of rows:

```python
# Validate only in development/testing
import os

if os.getenv("VALIDATE_SCHEMAS", "true").lower() == "true":
    @pa.check_input(input_schema)
    @pa.check_output(output_schema)
    def pipeline_step(df):
        ...
else:
    def pipeline_step(df):
        ...
```

Or use Pandera's lazy validation to collect all errors at once instead of failing on the first one:

```python
schema.validate(df, lazy=True)  # Reports ALL violations, not just the first
```
