# When NOT to Test

Testing has real costs: time to write, time to maintain, cognitive overhead. Not all code needs tests. Here's honest guidance on when to skip formal testing.

## Skip Tests For

### Exploratory Notebooks
Jupyter notebooks used for data exploration, visualization, and hypothesis generation are not production code. The output cells ARE the test — you visually inspect results as you go.

**When to graduate**: When notebook code becomes a function that other code depends on, extract it into a module and add tests.

### One-Off Scripts
A script you'll run once (data conversion, one-time cleanup, ad hoc analysis) doesn't need tests. Your time is better spent verifying the output manually.

**When to graduate**: When you run the "one-off" script a third time, it's no longer one-off. Add tests.

### Visualization Code
Testing that a plot "looks right" is hard and brittle. Test the DATA that feeds the plot instead.

```python
# DON'T test: "does the figure have the right colors"
# DO test: "does the data behind the figure have the right values"
def test_volcano_plot_data():
    data = prepare_volcano_data(results)
    assert "log2_fc" in data.columns
    assert "neg_log_p" in data.columns
    assert data["neg_log_p"].min() >= 0
```

### Thin Wrappers
If a function just calls a well-tested library with no logic:

```python
# No test needed — this is just a call to pd.read_csv
def load_counts(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, index_col=0)
```

### Configuration / Constants
```python
# No test needed
DEFAULT_CONFIDENCE = 0.95
AMINO_ACIDS = "ACDEFGHIKLMNPQRSTVWY"
```

## DO Test When

| Signal | Why | Methodology |
|--------|-----|-------------|
| Others depend on your function | Breaking it breaks them | Example-based or property-based |
| Function involves math/statistics | Silent numerical bugs | Property-based + floating-point |
| Function transforms data | Schema drift, NaN propagation | Contract-based (Pandera) |
| Function has known edge cases | Empty input, boundary values | Example-based |
| Bug was found and fixed | Prevent regression | Example-based (regression test) |
| Code will be published | Reproducibility requirement | Golden-file + property-based |

## The Graduation Rule

Code starts informal (notebook, script) and graduates to tested code when:

1. **It's called from more than one place** — now it's shared infrastructure
2. **It produces results that go into a paper** — now correctness matters
3. **Someone else needs to use or modify it** — now it needs a specification
4. **A bug was found** — add a regression test immediately

## The Cost of Over-Testing

Signs you're testing too much:
- Tests take longer to write than the code they test
- Tests break on every refactor but never catch real bugs
- You're testing library behavior (e.g., "does pandas merge work?")
- You're testing obvious one-liners with no logic
- Tests verify mocks more than real behavior

The goal is **confidence that the code is correct**, not 100% coverage. A 60% coverage test suite that tests important logic thoroughly beats a 95% coverage suite full of trivial assertions.
