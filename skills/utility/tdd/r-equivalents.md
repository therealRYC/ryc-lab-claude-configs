# R Equivalents

Quick-reference for translating each Python testing pattern to R/testthat.

## Setup

```r
# install.packages(c("testthat", "pointblank", "withr"))
# usethis::use_testthat()  # sets up tests/ directory in an R package
```

## Example-Based Testing (TDD)

| Python (pytest) | R (testthat) |
|----------------|-------------|
| `def test_foo():` | `test_that("foo works", { ... })` |
| `assert result == expected` | `expect_equal(result, expected)` |
| `assert x > 0` | `expect_gt(x, 0)` |
| `with pytest.raises(ValueError):` | `expect_error(foo(), class = "simpleError")` |
| `@pytest.fixture` | `withr::local_*()` or setup/teardown in `helper.R` |
| `@pytest.mark.parametrize(...)` | `purrr::walk(inputs, \(x) test_that(...))` or loop inside test |
| `tmp_path` fixture | `withr::local_tempdir()` |

```r
test_that("normalize_fitness_scores centers on wildtype", {
  raw_scores <- tibble(
    variant = c("WT", "A2T", "G5R"),
    fitness = c(1.0, 0.8, 1.2)
  )
  normalized <- normalize_fitness_scores(raw_scores, reference = "WT")

  wt_score <- normalized |> filter(variant == "WT") |> pull(fitness)
  expect_equal(wt_score, 0.0)
})
```

## Floating-Point Comparison

| Python | R |
|--------|---|
| `np.testing.assert_allclose(a, b, rtol=1e-7)` | `expect_equal(a, b, tolerance = 1e-7)` |
| `np.testing.assert_allclose(a, 0, atol=1e-12)` | `expect_equal(a, 0, tolerance = 1e-12)` |
| `pytest.approx(3.14, rel=1e-5)` | `expect_equal(x, 3.14, tolerance = 1e-5)` |
| `pd.testing.assert_frame_equal(a, b, rtol=1e-5)` | `expect_equal(a, b, tolerance = 1e-5)` |
| `assert np.isnan(result)` | `expect_true(is.nan(result))` |

testthat's `tolerance` is absolute by default. For relative tolerance:
```r
# Relative comparison (manual)
expect_true(abs(actual - expected) / abs(expected) < 1e-7)

# Or use expect_equal which does relative comparison when both values are > 0
expect_equal(actual, expected, tolerance = 1e-7)
```

## Property-Based Testing

R's property-based ecosystem is less mature than Python's Hypothesis. Options:

| Python (Hypothesis) | R Equivalent |
|--------------------|-------------|
| `@given(st.floats(...))` | `hedgehog::forall(gen.element(...), \(x) ...)` |
| `hypothesis.extra.numpy` | No direct equivalent — generate with `runif()`, `rnorm()` |
| `assume(x > 0)` | `if (x <= 0) return()` inside generator |
| Automatic shrinking | `hedgehog` does shrinking; manual approach doesn't |

**Pragmatic R approach** — use randomized testing without a framework:

```r
test_that("distance is symmetric across random inputs", {
  set.seed(42)
  for (i in 1:100) {
    a <- rnorm(10)
    b <- rnorm(10)
    expect_equal(
      compute_distance(a, b),
      compute_distance(b, a),
      tolerance = 1e-14
    )
  }
})

test_that("reverse complement is an involution", {
  set.seed(42)
  bases <- c("A", "C", "G", "T")
  for (i in 1:100) {
    seq <- paste0(sample(bases, sample(1:50, 1), replace = TRUE), collapse = "")
    expect_equal(reverse_complement(reverse_complement(seq)), seq)
  }
})
```

This gives you 90% of Hypothesis's value without adding a dependency.

## Contract-Based Testing (Data Validation)

| Python (Pandera) | R (pointblank) |
|-----------------|----------------|
| `pa.DataFrameSchema({...})` | `create_agent(df) |> ...` |
| `pa.Column(float, pa.Check.in_range(0, 1))` | `col_vals_between(columns, 0, 1)` |
| `pa.Check.str_matches(r"^[ACGT]+$")` | `col_vals_regex(columns, "^[ACGT]+$")` |
| `@pa.check_input(schema)` | Validate inside function or use `pointblank::expect_*()` |
| `nullable=False` | `col_vals_not_null(columns)` |
| `schema.validate(df, lazy=True)` | `interrogate(agent)` (collects all failures) |

```r
library(pointblank)

validate_fitness_data <- function(df) {
  agent <- create_agent(tbl = df) |>
    col_vals_not_null(variant_id) |>
    col_vals_regex(variant_id, "^[A-Z]\\d+[A-Z]$") |>
    col_vals_between(fitness_score, -10, 10) |>
    col_vals_in_set(replicate, 1:10) |>
    interrogate()

  if (any(!agent$validation_set$all_passed)) {
    stop("Data validation failed. Run interrogate() for details.")
  }
  invisible(df)
}
```

**Alternative**: `validate` package for simpler rules:
```r
library(validate)

rules <- validator(
  fitness_score >= -10,
  fitness_score <= 10,
  !is.na(variant_id),
  replicate %in% 1:10
)
result <- confront(df, rules)
summary(result)
```

## Golden-File / Snapshot Testing

| Python (pytest-regressions) | R (testthat 3e) |
|----------------------------|----------------|
| `dataframe_regression.check(df)` | `expect_snapshot_value(df, style = "serialize")` |
| `file_regression.check(text)` | `expect_snapshot(cat(text))` |
| `ndarrays_regression.check({"x": arr})` | `expect_snapshot_value(arr, style = "serialize")` |
| `pytest --force-regen` | `snapshot_accept()` or delete `_snaps/` dir |
| Tolerance via `default_tolerance=` | `expect_snapshot_value(df, tolerance = 1e-6)` |

```r
test_that("fitness pipeline output is stable", {
  result <- run_fitness_pipeline(test_data)
  # First run creates snapshot; subsequent runs compare
  expect_snapshot_value(result, style = "serialize", tolerance = 1e-6)
})
```

Snapshots are stored in `tests/testthat/_snaps/`. Commit them to version control.

## Stochastic Testing

| Python | R |
|--------|---|
| `rng = np.random.default_rng(42)` | `set.seed(42)` or `withr::with_seed(42, ...)` |
| Pass `rng=` parameter | Use `withr::local_seed()` in tests |
| `scipy.stats.kstest(samples, "norm")` | `ks.test(samples, "pnorm")` |
| `@pytest.mark.slow` | `testthat::skip_on_cran()` or custom `skip_if_slow()` |

```r
test_that("bootstrap CI has correct coverage", {
  n_trials <- 500
  true_mean <- 5.0
  contains_true <- 0

  for (seed in seq_len(n_trials)) {
    withr::local_seed(seed)
    data <- rnorm(50, mean = true_mean, sd = 1)
    ci <- bootstrap_ci(data)
    if (ci[1] <= true_mean && true_mean <= ci[2]) {
      contains_true <- contains_true + 1
    }
  }

  coverage <- contains_true / n_trials
  expect_true(coverage >= 0.90 && coverage <= 0.99)
})
```

**Design pattern**: accept a seed parameter for testability:
```r
bootstrap_ci <- function(data, n_bootstrap = 1000, confidence = 0.95, seed = NULL) {

  if (!is.null(seed)) set.seed(seed)
  # ... implementation
}
```

## Mocking

| Python | R |
|--------|---|
| `unittest.mock.MagicMock()` | `mockery::mock()` or `testthat::local_mocked_bindings()` |
| `mocker.patch("module.func")` | `local_mocked_bindings(func = \(...) fake_value)` |
| `mock.return_value = x` | `mock(\(...) x)` |

```r
test_that("fetch_gene_info parses response", {
  local_mocked_bindings(
    query_ncbi = function(symbol) {
      list(symbol = "BRCA1", chromosome = "17")
    }
  )
  result <- fetch_gene_info("BRCA1")
  expect_equal(result$chromosome, "17")
})
```

## Test Organization

| Python | R |
|--------|---|
| `tests/test_pipeline.py` | `tests/testthat/test-pipeline.R` |
| `class TestScoring:` | Group with `describe("scoring", { ... })` (testthat 3e) |
| `conftest.py` (shared fixtures) | `tests/testthat/helper.R` (auto-loaded) |
| `pytest.ini` markers | `.Rprofile` or test helpers for skip conditions |
| `pytest -k "slow"` | `testthat::test_that()` with `skip_if_slow()` |

## Key Differences to Watch For

1. **testthat uses `tolerance` not `rtol`/`atol`** — it's a single parameter that does relative comparison when values are large and absolute when near zero.

2. **No decorator pattern** — R doesn't have Python's `@check_input` decorators. Validate explicitly inside functions or at test time.

3. **`set.seed()` is global** — unlike Python's `rng` parameter pattern, R's `set.seed()` affects all random functions globally. Use `withr::local_seed()` in tests to avoid polluting state.

4. **Snapshot tests need testthat 3e** — make sure `testthat::edition_get()` returns 3.

5. **No Hypothesis equivalent at Hypothesis's maturity level** — the pragmatic loop-with-random-inputs approach covers most needs.
