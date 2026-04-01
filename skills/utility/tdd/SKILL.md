---
name: tdd
description: "Scientific code testing with layered methodologies: property-based (Hypothesis), contract-based (Pandera), example-based (TDD), golden-file regression, floating-point tolerance, and stochastic testing. ALWAYS consult this skill before writing any test code, choosing a testing strategy, or advising on how to test scientific/numerical code. This includes: writing pytest tests, fixing flaky tests, choosing between testing approaches, handling floating-point comparison, testing stochastic/random code, validating DataFrames with Pandera, setting up Hypothesis property-based tests, regression testing pipeline outputs, and deciding what NOT to test. Even if you know how to write tests, this skill provides methodology selection guidance and scientific testing patterns that produce significantly better results."
---

# Scientific Testing

## Philosophy

**No single testing methodology fits all scientific code.** Choose based on what you're testing.

TDD's red-green-refactor is excellent for deterministic utilities, but it breaks down for exploratory analysis, stochastic algorithms, and complex numerical code. This skill provides a layered approach where each methodology targets a specific class of scientific code.

**Core principle** (retained from TDD): Tests should verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

## The Scientific Testing Diamond

Scientific code benefits from a diamond-shaped testing strategy — heavy in the middle where most scientific logic lives:

```
          ╱  E2E  ╲            Few: full pipeline reproducibility checks
         ╱─────────╲
        ╱ Golden-File╲         Many: regression detection for complex outputs
       ╱───────────────╲
      ╱   Contract-Based ╲    Many: Pandera schemas at pipeline boundaries
     ╱─────────────────────╲
    ╱  Property + Example    ╲ Many: unit tests for math/algorithm functions
   ╱─────────────────────────╲
  ╱    Static Analysis         ╲ Base: type hints + mypy + linters
 ╱─────────────────────────────╲
```

| Layer | Code Type | Methodology | Tool | Reference |
|-------|-----------|-------------|------|-----------|
| 1 | Mathematical functions | Property-based testing | Hypothesis | [property-based.md](property-based.md) |
| 2 | Deterministic utilities | Example-based TDD | pytest | [example-based.md](example-based.md) |
| 3 | Data pipeline stages | Contract-based testing | Pandera | [contract-based.md](contract-based.md) |
| 4 | Pipeline regression | Golden-file testing | pytest-regressions | [golden-file.md](golden-file.md) |
| 5 | Stochastic components | Seed + statistical tests | pytest + scipy.stats | [stochastic.md](stochastic.md) |
| 6 | Test quality audit | Mutation testing | mutmut / Cosmic Ray | (periodic, not per-commit) |

## ⚠ Floating-Point First

Before writing ANY numerical test, read [floating-point.md](floating-point.md).

The #1 gotcha in scientific testing: **never use `==` for floating-point comparison**.

```python
# WRONG — will fail due to floating-point representation
assert 0.1 + 0.2 == 0.3

# RIGHT — tolerance-based comparison
import numpy as np
np.testing.assert_allclose(0.1 + 0.2, 0.3, rtol=1e-15)
```

## Methodology Selection Guide

Ask: **"What kind of code am I testing?"** Then follow the decision tree:

```
Is the output deterministic for a given input?
├── YES: Does it involve floating-point math?
│   ├── YES → Property-based testing (check invariants + tolerances)
│   │         See property-based.md
│   └── NO → Example-based TDD (red-green-refactor)
│             See example-based.md
└── NO: Is it stochastic (random/Monte Carlo)?
    ├── YES → Seed-based + statistical property tests
    │         See stochastic.md
    └── NO: Is it a data pipeline stage?
        ├── YES → Contract-based (Pandera schemas)
        │         See contract-based.md
        └── NO → Golden-file regression testing
                  See golden-file.md
```

**Combine methodologies freely.** A pipeline function might use:
- Pandera schema on input/output (contract)
- Property-based tests for its core calculation (invariants)
- A golden-file test for regression detection (snapshot)

## Workflow

### 1. Planning

Before writing any code or tests:

- [ ] Identify what kind of code you're testing (use selection guide above)
- [ ] Choose methodology(ies) — often you'll combine 2-3
- [ ] If a `/plan-eng-review` test plan exists, consume it — map each test case to a methodology
- [ ] List the behaviors/properties/contracts to test
- [ ] Confirm with user which behaviors are highest priority

Ask: "What invariants should this function preserve? What would a wrong answer look like?"

### 2. Implementation Loop

For **example-based TDD** (deterministic code):
```
RED:   Write one test → fails
GREEN: Write minimal code → passes
REFACTOR: Clean up → tests still pass
Repeat.
```

For **property-based** (numerical/mathematical code):
```
1. Identify mathematical properties (symmetry, conservation, bounds)
2. Write Hypothesis strategies for input generation
3. Write property tests — each asserts one invariant
4. Run and fix any counterexamples Hypothesis finds
```

For **contract-based** (data pipelines):
```
1. Define Pandera schema for expected input/output
2. Decorate pipeline functions with @pa.check_input / @pa.check_output
3. Write a test that feeds representative data through the function
4. Add edge cases: empty DataFrame, NaN values, single row
```

For **golden-file** (complex outputs):
```
1. Write the function
2. Generate output with known-good input
3. Save as golden file (pytest-regressions handles this)
4. Future runs compare against golden file with tolerance
```

### 3. Anti-Pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.**

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

Tests written in bulk test *imagined* behavior, not *actual* behavior. Vertical slices respond to what you learned from each cycle.

### 4. Refactor

After tests pass, look for [refactor candidates](refactoring.md):

- [ ] Extract duplication
- [ ] Deepen modules (see [deep-modules.md](deep-modules.md))
- [ ] Improve interfaces for testability (see [interface-design.md](interface-design.md))
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

### 5. Handoff to /qa

When tests are written and passing, the `/qa` skill can:
- Run the full test suite
- Verify coverage against the test plan from `/plan-eng-review`
- Check for untested edge cases
- Produce a health score

## When NOT to Test

See [when-not-to-test.md](when-not-to-test.md) for honest guidance.

Short version: **skip formal testing** for exploratory notebooks, one-off scripts, visualization code, and early prototypes. Add tests when code stabilizes and others will depend on it.

## R Users

All examples in this skill are Python/pytest. For R/testthat equivalents (testthat, pointblank, withr, snapshot testing), see [r-equivalents.md](r-equivalents.md).

## Mocking

See [mocking.md](mocking.md). Summary: mock at **system boundaries** only (external APIs, databases, time/randomness). Never mock your own modules.

## Dependencies

```bash
# Core (likely already installed)
pip install pytest numpy

# Property-based testing
pip install hypothesis

# Contract-based testing (DataFrame validation)
pip install pandera

# Golden-file regression testing
pip install pytest-regressions

# Mutation testing (periodic audits, not per-commit)
pip install mutmut
```

## Checklist Per Test

```
[ ] Test describes behavior or property, not implementation
[ ] Floating-point comparisons use tolerance (rtol/atol)
[ ] Test uses realistic biological data, not [1, 2, 3]
[ ] Test docstring explains what it guards against
[ ] Test would survive internal refactor
```

## Evidence Base

This layered approach is supported by:
- Nagappan et al. 2008 — TDD reduces defects 40-90% at 15-35% time cost ([Springer](https://link.springer.com/article/10.1007/s10664-008-9062-z))
- Wilson et al. 2014 — Best Practices for Scientific Computing ([PLOS Biology](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745))
- Goldstein et al. 2025 — Property-based testing found bugs in NumPy, SciPy, Pandas ([arXiv](https://arxiv.org/html/2510.09907v1))
- Pandera validated for scientific DataFrames ([SciPy Proceedings](https://proceedings.scipy.org/articles/gerudo-f2bc6f59-010))
