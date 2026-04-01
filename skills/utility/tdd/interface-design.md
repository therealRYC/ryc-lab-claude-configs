# Interface Design for Testability

Good interfaces make testing natural. Bad interfaces require mocks, patches, and gymnastics.

## 1. Accept Dependencies, Don't Create Them

```python
# TESTABLE — caller controls the dependency
def score_variants(
    counts: pd.DataFrame,
    normalizer: Callable[[pd.Series], pd.Series] = default_normalizer,
) -> pd.DataFrame:
    normalized = normalizer(counts["raw_count"])
    ...


# HARD TO TEST — creates its own dependency internally
def score_variants(counts: pd.DataFrame) -> pd.DataFrame:
    config = load_config_from_disk("/etc/pipeline/config.yaml")
    ...
```

## 2. Return Results, Don't Produce Side Effects

```python
# TESTABLE — pure function, output depends only on input
def compute_enrichment(
    input_counts: pd.Series, output_counts: pd.Series
) -> pd.Series:
    return np.log2(output_counts / input_counts)


# HARD TO TEST — modifies the DataFrame in place, returns nothing
def compute_enrichment(df: pd.DataFrame) -> None:
    df["enrichment"] = np.log2(df["output"] / df["input"])
```

When you return a result, the test is trivial: call the function, check the return value. When the function mutates state, you have to inspect the mutated object, which couples your test to its internal structure.

## 3. Small Surface Area

- Fewer methods = fewer tests needed
- Fewer parameters = simpler test setup
- See [deep-modules.md](deep-modules.md) for the deep module pattern

```python
# GOOD — one function, clear inputs, clear output
def filter_variants(
    df: pd.DataFrame,
    min_count: int = 10,
    max_missing: float = 0.1,
) -> pd.DataFrame:
    ...


# BAD — scattered across many methods that share hidden state
class VariantFilter:
    def set_min_count(self, n): ...
    def set_max_missing(self, pct): ...
    def set_quality_threshold(self, q): ...
    def load_data(self, path): ...
    def run(self): ...  # Depends on all the above being called first
```

## 4. Separate I/O from Logic

```python
# TESTABLE — logic is pure, I/O is separate
def score_from_counts(input_counts: np.ndarray, output_counts: np.ndarray) -> np.ndarray:
    """Pure scoring logic — no file I/O."""
    return np.log2((output_counts + 0.5) / (input_counts + 0.5))


def score_from_file(path: Path) -> np.ndarray:
    """Thin I/O wrapper — loads data and delegates to pure function."""
    df = pd.read_csv(path)
    return score_from_counts(df["input"].values, df["output"].values)
```

Test `score_from_counts` with synthetic data (fast, no files). Test `score_from_file` with a fixture file (integration test).
