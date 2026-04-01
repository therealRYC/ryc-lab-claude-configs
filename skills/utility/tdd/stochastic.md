# Testing Stochastic Code

Use for: **Monte Carlo simulations, random sampling, MCMC, bootstrapping, any code with randomness**.

Stochastic code produces different outputs every run. You can't use `assert result == expected`. Instead, use two strategies: (1) fix the seed for deterministic replay, and (2) test statistical properties that should hold regardless of the random draw.

## Strategy 1: Seed-Based Deterministic Testing

Fix the random seed to make outputs reproducible, then test exact values:

```python
import numpy as np


def test_bootstrap_confidence_interval_deterministic():
    """Guards against changes to the bootstrap algorithm by fixing randomness.

    Uses a fixed seed so the test is deterministic and reproducible.
    """
    rng = np.random.default_rng(seed=42)
    data = np.array([0.8, 0.9, 1.1, 0.7, 1.2, 0.95, 1.05])

    ci_low, ci_high = bootstrap_confidence_interval(
        data, n_bootstrap=1000, confidence=0.95, rng=rng
    )

    # With seed=42, these values are deterministic
    np.testing.assert_allclose(ci_low, 0.8214, rtol=1e-3)
    np.testing.assert_allclose(ci_high, 1.1071, rtol=1e-3)
```

### Design Pattern: Accept `rng` as Parameter

```python
def bootstrap_confidence_interval(
    data: np.ndarray,
    n_bootstrap: int = 1000,
    confidence: float = 0.95,
    rng: np.random.Generator | None = None,
) -> tuple[float, float]:
    """Compute bootstrap confidence interval.

    Args:
        data: 1-D array of observations.
        n_bootstrap: Number of bootstrap samples.
        confidence: Confidence level (e.g., 0.95 for 95% CI).
        rng: NumPy random generator. If None, uses default (non-deterministic).

    Returns:
        Tuple of (lower_bound, upper_bound).
    """
    if rng is None:
        rng = np.random.default_rng()
    # ... implementation using rng.choice(), rng.normal(), etc.
```

This pattern makes every function testable with a fixed seed while keeping the default behavior non-deterministic.

## Strategy 2: Statistical Property Testing

Test properties that should hold across ANY random draw (with high probability):

```python
from scipy import stats


def test_bootstrap_ci_coverage():
    """Guards against CI calculation bugs by checking coverage over many trials.

    If we repeatedly sample from a known distribution and compute 95% CIs,
    approximately 95% should contain the true mean.
    """
    true_mean = 5.0
    n_trials = 500
    contains_true_mean = 0

    for seed in range(n_trials):
        rng = np.random.default_rng(seed)
        data = rng.normal(loc=true_mean, scale=1.0, size=50)
        ci_low, ci_high = bootstrap_confidence_interval(data, rng=rng)
        if ci_low <= true_mean <= ci_high:
            contains_true_mean += 1

    coverage = contains_true_mean / n_trials
    # 95% CI should contain true mean ~95% of the time
    # Allow some slack: test that coverage is between 90% and 99%
    assert 0.90 <= coverage <= 0.99, f"Coverage {coverage:.2%} outside expected range"


def test_random_sampler_produces_correct_distribution():
    """Guards against distribution parameter bugs (e.g., using variance instead of std).

    Draws many samples and checks that the empirical distribution matches
    the expected one using a KS test.
    """
    rng = np.random.default_rng(42)
    samples = sample_fitness_scores(n=10_000, mean=0.0, std=1.0, rng=rng)

    # Kolmogorov-Smirnov test: are these samples from N(0, 1)?
    ks_stat, p_value = stats.kstest(samples, "norm", args=(0.0, 1.0))
    assert p_value > 0.01, f"Samples don't match expected distribution (p={p_value:.4f})"
```

## Statistical Properties to Test

| Property | How to Test | Catches |
|----------|------------|---------|
| Mean is near expected | `abs(samples.mean() - expected) < tolerance` | Location parameter bugs |
| Variance is near expected | `abs(samples.var() - expected) < tolerance` | Scale parameter bugs (std vs var) |
| Values in expected range | `assert samples.min() >= 0` | Support/bounds bugs |
| Distribution shape | `scipy.stats.kstest()` or `normaltest()` | Wrong distribution family |
| No correlation when expected | `abs(np.corrcoef(a, b)[0,1]) < 0.1` | Independence assumption violations |
| CI coverage | Multiple trials, check proportion | CI calculation bugs |

## Handling Flaky Tests

Statistical tests can randomly fail. Strategies:

### 1. Use Generous Bounds
```python
# BAD — too tight, will flake
assert 0.94 <= coverage <= 0.96

# GOOD — generous bounds still catch real bugs
assert 0.88 <= coverage <= 0.99
```

### 2. Multiple Seeds with Majority Rule
```python
def test_sampler_statistical_properties():
    """Runs statistical check across 5 seeds; passes if 4/5 succeed."""
    passes = 0
    for seed in range(5):
        rng = np.random.default_rng(seed)
        samples = generate_samples(n=1000, rng=rng)
        if abs(samples.mean()) < 0.1:
            passes += 1
    assert passes >= 4, f"Only {passes}/5 seeds passed mean check"
```

### 3. Large Sample Sizes
```python
# More samples → tighter concentration → less flakiness
samples = generate_samples(n=100_000, rng=rng)  # Not n=100
assert abs(samples.mean() - expected_mean) < 0.01
```

## CI Testing

For stochastic tests in continuous integration:

```python
import pytest

# Mark slow statistical tests so they can be skipped in fast runs
@pytest.mark.slow
def test_monte_carlo_convergence():
    """Takes ~30 seconds. Run with: pytest -m slow"""
    ...
```

```ini
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
]
```

## Anti-Pattern: Testing Randomness Without Seeds

```python
# BAD — non-deterministic, impossible to debug failures
def test_random_function():
    result = random_function()  # Different every run
    assert result > 0           # Might fail randomly

# GOOD — deterministic, reproducible
def test_random_function():
    rng = np.random.default_rng(42)
    result = random_function(rng=rng)
    assert result > 0  # Same result every run
```
