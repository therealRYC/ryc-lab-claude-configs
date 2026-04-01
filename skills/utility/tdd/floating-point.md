# Floating-Point Testing

Read this before writing ANY numerical test. Floating-point bugs are the #1 source of silent scientific errors.

## The Fundamental Rule

**Never use `==` for floating-point comparison.** Always use tolerance-based assertions.

```python
# WRONG — will fail unpredictably
assert result == 3.14159
assert 0.1 + 0.2 == 0.3  # This is False in every programming language

# RIGHT — tolerance-based
import numpy as np
np.testing.assert_allclose(result, 3.14159, rtol=1e-10)
np.testing.assert_allclose(0.1 + 0.2, 0.3, rtol=1e-15)
```

## Choosing Tolerances

### Relative Tolerance (`rtol`) vs. Absolute Tolerance (`atol`)

```python
np.testing.assert_allclose(actual, expected, rtol=1e-7, atol=0)
```

- **`rtol`** (relative): `|actual - expected| <= rtol * |expected|`
  - Use when values span a wide range
  - Default: `1e-7` (single precision) or `1e-14` (double precision)

- **`atol`** (absolute): `|actual - expected| <= atol`
  - Use when expected values are near zero (where rtol breaks down)
  - Default: `0`

The full check is: `|actual - expected| <= atol + rtol * |expected|`

### Guidelines for Scientific Code

| Computation Type | Suggested `rtol` | Why |
|-----------------|-------------------|-----|
| Direct arithmetic | `1e-14` to `1e-15` | Near machine epsilon for float64 |
| Matrix operations | `1e-10` to `1e-12` | Accumulation of rounding errors |
| Iterative solvers | `1e-6` to `1e-8` | Convergence tolerance dependent |
| Statistics (mean, var) | `1e-10` to `1e-12` | Depends on sample size |
| ML model outputs | `1e-4` to `1e-6` | Optimization is approximate |
| Cross-platform reproducibility | `1e-6` to `1e-8` | Different compilers/BLAS libraries |

## Common Gotchas

### 1. Comparing Near Zero

```python
# BAD — rtol is meaningless when expected ≈ 0
np.testing.assert_allclose(result, 0.0, rtol=1e-7)  # Passes for result=1e-8!

# GOOD — use atol for near-zero comparisons
np.testing.assert_allclose(result, 0.0, atol=1e-12)
```

### 2. Non-Associativity

```python
# These can give different results!
a = (1e-16 + 1.0) - 1.0  # → 0.0 (1e-16 absorbed into 1.0)
b = 1e-16 + (1.0 - 1.0)  # → 1e-16

# Test the property, not a specific order of operations
```

### 3. NaN Propagation

```python
# NaN is not equal to anything, including itself
assert float("nan") == float("nan")  # FAILS
assert float("nan") != float("nan")  # PASSES (!)

# Use explicit NaN checks
assert np.isnan(result)
# Or allow NaN in comparisons
np.testing.assert_equal(result, np.nan)  # Handles NaN==NaN correctly
```

### 4. Comparing Arrays with NaN

```python
# np.testing.assert_allclose does NOT handle NaN by default
a = np.array([1.0, np.nan, 3.0])
b = np.array([1.0, np.nan, 3.0])
np.testing.assert_allclose(a, b)  # FAILS because NaN != NaN

# Use assert_equal for arrays that should contain NaN
np.testing.assert_equal(a, b)  # Treats NaN as equal to NaN

# Or mask NaN and compare the rest
mask = ~np.isnan(a) & ~np.isnan(b)
np.testing.assert_allclose(a[mask], b[mask])
```

### 5. Catastrophic Cancellation

```python
# Subtracting nearly equal numbers destroys precision
x = 1.0000000001
y = 1.0000000000
diff = x - y  # Should be 1e-10, but precision is terrible

# When testing functions that involve cancellation,
# use wider tolerances or test a reformulated version
```

## NumPy Testing Functions

```python
import numpy as np

# Floating-point with tolerance (MOST COMMON)
np.testing.assert_allclose(actual, expected, rtol=1e-7, atol=0)

# Exact equality (for integers, strings, booleans — NOT floats)
np.testing.assert_equal(actual, expected)

# Less than / greater than
np.testing.assert_array_less(a, b)  # Element-wise a < b

# Custom per-element tolerance
np.testing.assert_array_almost_equal(actual, expected, decimal=7)  # Deprecated-ish, prefer assert_allclose
```

## pytest.approx (for scalar comparisons)

```python
# For simple scalar comparisons in non-NumPy code
assert result == pytest.approx(3.14159, rel=1e-5)
assert result == pytest.approx(0.0, abs=1e-10)  # Near zero
```

## Pandas Testing

```python
import pandas as pd

# Compare DataFrames with tolerance
pd.testing.assert_frame_equal(
    actual, expected,
    check_exact=False,  # Allow floating-point tolerance
    rtol=1e-5,          # Relative tolerance
    atol=1e-8,          # Absolute tolerance
)

# Compare Series
pd.testing.assert_series_equal(actual, expected, rtol=1e-5)
```

## Pattern: Tolerance as a Test Parameter

When tolerance itself is a design decision, document it:

```python
# Tolerance chosen based on numerical analysis of the algorithm.
# The scoring function involves log-ratio calculations that accumulate
# ~1e-12 rounding error per operation, with up to 1000 operations per
# variant. Conservative tolerance: 1e-8.
SCORING_TOLERANCE = dict(rtol=1e-8, atol=1e-12)


def test_scoring_accuracy():
    """Guards against numerical drift in scoring algorithm.

    See SCORING_TOLERANCE for tolerance justification.
    """
    result = score_variants(test_data)
    np.testing.assert_allclose(result, expected, **SCORING_TOLERANCE)
```
