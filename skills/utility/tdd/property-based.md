# Property-Based Testing (Hypothesis)

Use for: **mathematical functions, numerical algorithms, any code with clear invariants**.

Instead of testing specific examples, define *properties* that must hold for ALL valid inputs. Hypothesis generates hundreds of random inputs and searches for counterexamples.

## Why This Matters for Scientific Code

Property-based testing found bugs in NumPy, SciPy, and Pandas (Goldstein et al. 2025). It catches floating-point edge cases (NaN, Inf, denormals) that humans forget to test. For scientific functions, mathematical properties ARE the specification.

## Install

```bash
pip install hypothesis
```

## Core Pattern

```python
from hypothesis import given, settings, assume
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays
import numpy as np


@given(st.floats(min_value=-10, max_value=10, allow_nan=False, allow_infinity=False))
def test_log_enrichment_is_antisymmetric(x):
    """Swapping numerator/denominator negates the result.

    Guards against sign errors in enrichment calculations.
    """
    # Skip zero to avoid division-by-zero
    assume(abs(x) > 1e-10)
    result_pos = log_enrichment(x, 1.0)
    result_neg = log_enrichment(1.0, x)
    np.testing.assert_allclose(result_pos, -result_neg, atol=1e-12)
```

## Scientific Properties to Test

### 1. Symmetry
```python
@given(
    a=arrays(np.float64, shape=10, elements=st.floats(-100, 100, allow_nan=False)),
    b=arrays(np.float64, shape=10, elements=st.floats(-100, 100, allow_nan=False)),
)
def test_distance_is_symmetric(a, b):
    """distance(a, b) == distance(b, a). Guards against argument-order bugs."""
    np.testing.assert_allclose(
        compute_distance(a, b),
        compute_distance(b, a),
        rtol=1e-14,
    )
```

### 2. Value Range Constraints
```python
@given(scores=arrays(np.float64, shape=st.integers(1, 100),
                     elements=st.floats(-5, 5, allow_nan=False)))
def test_softmax_outputs_sum_to_one(scores):
    """Probabilities must sum to 1. Guards against normalization bugs."""
    probs = softmax(scores)
    np.testing.assert_allclose(probs.sum(), 1.0, atol=1e-10)
    assert np.all(probs >= 0)
    assert np.all(probs <= 1)
```

### 3. Inverse Relationships (Round-Trip)
```python
@given(seq=st.text(alphabet="ACGT", min_size=1, max_size=100))
def test_reverse_complement_is_involution(seq):
    """Applying reverse complement twice returns the original.

    Guards against incomplete complement mapping or off-by-one in reversal.
    """
    assert reverse_complement(reverse_complement(seq)) == seq
```

### 4. Conservation Laws
```python
@given(counts=arrays(np.int64, shape=(5, 3),
                     elements=st.integers(0, 1000)))
def test_normalization_preserves_total_counts(counts):
    """Total counts before and after normalization must match.

    Guards against off-by-one errors in count redistribution.
    """
    assume(counts.sum() > 0)  # Skip all-zero matrices
    normalized = normalize_counts(counts)
    np.testing.assert_allclose(normalized.sum(), counts.sum(), rtol=1e-10)
```

### 5. Monotonicity
```python
@given(
    x1=st.floats(0.01, 10, allow_nan=False),
    x2=st.floats(0.01, 10, allow_nan=False),
)
def test_log_is_monotonically_increasing(x1, x2):
    """If x1 < x2, then log(x1) < log(x2). Guards against sign flips."""
    assume(x1 != x2)
    if x1 < x2:
        assert safe_log(x1) < safe_log(x2)
    else:
        assert safe_log(x1) > safe_log(x2)
```

### 6. Idempotency
```python
@given(df=dataframe_strategy())
def test_dedup_is_idempotent(df):
    """Deduplicating twice gives the same result as once.

    Guards against stateful side effects in dedup logic.
    """
    once = deduplicate_variants(df)
    twice = deduplicate_variants(once)
    pd.testing.assert_frame_equal(once, twice)
```

## Hypothesis Strategies for Scientific Data

### NumPy Arrays
```python
from hypothesis.extra.numpy import arrays

# Fixed-shape float array with controlled range
arrays(np.float64, shape=(10, 3), elements=st.floats(-1e6, 1e6, allow_nan=False))

# Variable-shape array
arrays(np.float64, shape=st.tuples(st.integers(1, 100), st.integers(1, 10)))
```

### DNA Sequences
```python
dna_strategy = st.text(alphabet="ACGT", min_size=1, max_size=1000)
codon_strategy = st.text(alphabet="ACGT", min_size=3, max_size=3)
```

### DataFrames
```python
from hypothesis.extra.pandas import data_frames, column

fitness_df_strategy = data_frames([
    column("variant", elements=st.text(alphabet="ACGT", min_size=3, max_size=3)),
    column("score", elements=st.floats(-5, 5, allow_nan=False)),
    column("replicate", elements=st.integers(1, 3)),
])
```

## Common Pitfalls

1. **Properties too weak**: `assert result is not None` proves nothing. Test a meaningful mathematical property.
2. **Properties too strong**: Re-implementing the function in the test. If your property IS the implementation, use example-based testing instead.
3. **Slow tests**: Hypothesis generates many inputs. Use `@settings(max_examples=50)` for expensive functions, `@settings(max_examples=1000)` for cheap ones.
4. **Forgetting `assume()`**: Filter impossible inputs with `assume()` rather than letting them cause expected failures.
5. **Not using `allow_nan=False`**: Unless you're specifically testing NaN handling, exclude NaN from float strategies to avoid noise.

## When to Prefer Example-Based Tests Instead

- When the "property" is just "the output equals this specific value" — that's an example test
- When the function has no mathematical invariants (e.g., a parser)
- When the function is so cheap that a few hardcoded examples give full confidence
