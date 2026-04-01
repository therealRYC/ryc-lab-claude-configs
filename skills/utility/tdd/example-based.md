# Example-Based Testing (TDD Red-Green-Refactor)

Use for: **deterministic utility functions** — parsers, file I/O, data transformations, string manipulation.

This is classical TDD adapted for Python/pytest with scientific examples.

## The Cycle

```
RED:   Write a test that fails (defines desired behavior)
GREEN: Write minimal code to make it pass
REFACTOR: Clean up without changing behavior
```

One cycle at a time. Never write multiple tests before implementing.

## Good Tests

**Integration-style**: test through real interfaces, not mocks of internal parts.

```python
# GOOD: Tests observable behavior through public interface
def test_parse_variant_id_extracts_components():
    """Guards against parser regression when variant ID format changes."""
    variant = parse_variant_id("BRCA1:c.5266dupC")
    assert variant.gene == "BRCA1"
    assert variant.hgvs == "c.5266dupC"


# GOOD: Tests a data transformation end-to-end
def test_normalize_fitness_scores_centers_on_wildtype():
    """Guards against normalization bugs that shift the reference point."""
    raw_scores = pd.DataFrame({
        "variant": ["WT", "A2T", "G5R"],
        "fitness": [1.0, 0.8, 1.2],
    })
    normalized = normalize_fitness_scores(raw_scores, reference="WT")

    # Wildtype should be exactly 0 after normalization
    wt_score = normalized.loc[normalized["variant"] == "WT", "fitness"].iloc[0]
    assert wt_score == 0.0
```

Characteristics:
- Tests behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test
- Docstring explains what the test guards against

## Bad Tests

**Implementation-detail tests**: coupled to internal structure.

```python
# BAD: Tests implementation details (what function was called internally)
def test_normalize_calls_subtract(mocker):
    mock_sub = mocker.patch("pipeline.subtract_reference")
    normalize_fitness_scores(df, reference="WT")
    mock_sub.assert_called_once()


# BAD: Bypasses interface to verify
def test_save_results_writes_to_disk(tmp_path):
    save_results(data, tmp_path / "output.csv")
    # Reading the raw file instead of using the load function
    with open(tmp_path / "output.csv") as f:
        assert "variant" in f.readline()


# GOOD: Verifies through the interface (round-trip)
def test_save_and_load_results_preserves_data(tmp_path):
    """Guards against serialization bugs that lose columns or corrupt types."""
    save_results(data, tmp_path / "output.csv")
    loaded = load_results(tmp_path / "output.csv")
    pd.testing.assert_frame_equal(data, loaded)
```

Red flags:
- Mocking internal collaborators
- Testing private methods (functions starting with `_`)
- Asserting on call counts/order
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT

## Edge Cases for Scientific Data

Per CLAUDE.md, always test data transformations with:

```python
def test_aggregate_scores_handles_empty_dataframe():
    """Guards against IndexError on empty input from upstream filtering."""
    empty_df = pd.DataFrame(columns=["variant", "score", "replicate"])
    result = aggregate_scores(empty_df)
    assert len(result) == 0


def test_aggregate_scores_handles_single_row():
    """Guards against off-by-one in aggregation with n=1."""
    single = pd.DataFrame({"variant": ["A2T"], "score": [0.85], "replicate": [1]})
    result = aggregate_scores(single)
    assert len(result) == 1


def test_aggregate_scores_handles_nan_values():
    """Guards against NaN propagation that silently corrupts downstream analysis."""
    df = pd.DataFrame({
        "variant": ["A2T", "A2T", "A2T"],
        "score": [0.8, float("nan"), 0.9],
        "replicate": [1, 2, 3],
    })
    result = aggregate_scores(df)
    # Decide: should NaN be skipped or propagated? Test the chosen behavior.
    assert not result["score"].isna().any()
```

## pytest Conventions

```python
import pytest
import pandas as pd
import numpy as np


class TestFitnessScoring:
    """Tests for the fitness scoring module."""

    def test_known_good_case(self):
        """Guards against regression in the core scoring algorithm."""
        ...

    def test_edge_case_all_synonymous(self):
        """Guards against division-by-zero when all variants are synonymous."""
        ...

    @pytest.mark.parametrize("n_replicates", [1, 2, 3, 10])
    def test_scoring_works_across_replicate_counts(self, n_replicates):
        """Guards against assumptions about specific replicate counts."""
        ...
```

Use `pytest.mark.parametrize` to test the same behavior across multiple inputs without duplicating test logic.
