<!-- Created: 2026-03-25 -->
<!-- Last updated: 2026-03-25 — Revised: replaced point-based scoring with minimal criterion + coverage system (informed by Skalse et al., Brant & Stanley, Mouret & Clune) -->

# Evaluation Guide: Minimal Criterion + Coverage-Based Evaluation

This guide defines the evaluation system between the Generator (planner/coder) and the Evaluator (external critic). The system uses **minimal criteria** (both sides must meet a bar) and **coverage-based assessment** (diversity of evaluation across dimensions), not adversarial point competition.

**Why not points?** Skalse et al. (NeurIPS 2022) proved that any proxy reward will eventually be hacked under strong optimization. Gao et al. (2022) showed overoptimization follows predictable scaling laws — proxy reward increases monotonically but true reward peaks then declines. Points create a zero-sum game that incentivizes gaming over genuine quality. Coverage-based evaluation is harder to game because the evaluator must demonstrate *breadth* across dimensions, not *depth* in one.

**Design principles:**
- **Minimal criterion coevolution** (Brant & Stanley, 2017): Both sides must meet a bar. Neither side "wins."
- **Quality-diversity** (Mouret & Clune, 2015): Track diversity of evaluation across dimensions, not total findings.
- **Continuous signals** (Arjovsky et al., 2017): Never use binary pass/fail. Multi-dimensional assessment.
- **Constitutional constraints** (Bai et al., 2022): Anti-goals are checkable assertions, not just prose.

## The Evaluation Framework

```
Generator writes code + tests + test explanation
         |
Evaluator checks ALL 5 dimensions + runs anti-goal assertions
         |
Scorecard tracks coverage rates and finding diversity
         |
Human reviews findings, overrules false positives
```

## The 5 Evaluation Dimensions (MAP-Elites-inspired)

The evaluator must check ALL 5 dimensions for every feature. Coverage across dimensions matters more than finding count in any single dimension.

| # | Dimension | What It Checks | Minimal Criterion |
|---|-----------|---------------|-------------------|
| 1 | **Correctness** | Does the code do what the brief says? | Tests pass; acceptance criteria met |
| 2 | **Test quality** | Do tests actually catch bugs? Would they fail if the code were wrong? | At least one non-trivial assertion per code path; no trivially passing tests |
| 3 | **Anti-goal compliance** | Does the implementation respect specsheet anti-goals? | Each anti-goal's verification command executed and passed |
| 4 | **Integration** | Does this feature work with existing features? | Integration points from brief verified (inputs consumed, outputs produced correctly) |
| 5 | **Scope fidelity** | Does the implementation match the brief's scope? | No significant additions (scope creep) or omissions (incomplete implementation) |

**Why 5 dimensions?** This prevents the evaluator from fixating on one type of finding (mode collapse). An evaluator that finds 5 test quality issues but skips anti-goal checking is performing worse than one that checks all 5 dimensions and finds nothing.

## Minimal Criteria

### Generator Minimal Criteria (must ALL be met)

- [ ] All tests pass (`test_cmd` from feature-list.json exits with 0)
- [ ] All acceptance criteria from the feature brief are checked off
- [ ] Test explanation document (`Plans/features/{id}-tests.md`) is complete
- [ ] "What's NOT Tested" section in test explanation is non-empty (honest about gaps)
- [ ] Code follows project coding standards (type hints, docstrings, etc.)

If any criterion is not met, the feature status is `failing` regardless of evaluator findings.

### Evaluator Minimal Criteria (must ALL be met)

- [ ] All 5 evaluation dimensions explicitly checked (with evidence for each)
- [ ] All anti-goal verification commands from the specsheet executed
- [ ] "What's NOT Tested" gaps from the test explanation reviewed and risk-assessed
- [ ] At least one non-trivial code path manually traced (not just reading test output)
- [ ] Each finding includes specific file:line evidence and dimension classification

If any criterion is not met, the evaluation is **incomplete** — the evaluator must re-run.

## Verdicts

Verdicts are based on findings, but the bar is the minimal criteria:

| Verdict | Condition | Effect |
|---------|-----------|--------|
| **PASS** | Generator meets all minimal criteria; evaluator finds no issues across all 5 dimensions | Feature status → `passing` |
| **PASS with notes** | Generator meets criteria; evaluator found minor observations (no dimension has a serious issue) | Feature status → `passing`; notes recorded |
| **NEEDS WORK** | Evaluator found a substantive issue in one or more dimensions | Feature status → `failing`; must fix and re-evaluate |
| **INCOMPLETE** | Evaluator did not check all 5 dimensions | Evaluation must be re-run before any verdict |

Note: There is no "WARN" bucket. A finding is either substantive enough to block (NEEDS WORK) or it's a note. This simplifies the decision and prevents the "WARN but do nothing" gray zone.

## Finding Classification

Each evaluator finding is classified by dimension and severity:

| Severity | Meaning | Effect |
|----------|---------|--------|
| **Blocker** | Violates a minimal criterion or anti-goal; code may produce wrong results | Feature must be fixed → NEEDS WORK |
| **Substantive** | Real issue that should be addressed but doesn't violate criteria | Feature should be fixed → NEEDS WORK |
| **Note** | Observation worth recording but not blocking | Feature can pass → PASS with notes |

Every finding must reference a specific dimension (1-5) and include file:line evidence.

## The Scorecard (`Plans/evaluator-scorecard.md`)

The scorecard is a **diagnostic dashboard**, not a leaderboard.

```markdown
# Long Run Scorecard: {Project Name}

**Last updated:** {timestamp}

## Health Metrics
══════════════════════════════════════════════════
Generator clean-pass rate:  75% (3/4 features passed on first attempt)
Evaluator coverage rate:    100% (5/5 dimensions checked on all features)
Evaluator hit rate:         67% (2/3 findings confirmed by human)
Finding diversity:          4/5 dimensions (no integration findings yet)
══════════════════════════════════════════════════

## Feature-by-Feature

| Feature | Complexity | Verdict | Dimensions Checked | Findings | Human Overrides |
|---------|-----------|---------|-------------------|----------|-----------------|
| config-parser | S | PASS | 5/5 | 0 | — |
| data-loader | M | PASS with notes | 5/5 | 1 note (test quality) | — |
| core-calc | L | NEEDS WORK → PASS | 5/5 | 1 blocker (anti-goal) → fixed | — |
| output-gen | M | PASS | 5/5 | 1 note (scope) | 1 overruled |

## Finding Distribution

| Dimension | Findings | Blockers | Notes |
|-----------|----------|----------|-------|
| Correctness | 0 | 0 | 0 |
| Test quality | 1 | 0 | 1 |
| Anti-goal compliance | 1 | 1 | 0 |
| Integration | 0 | 0 | 0 |
| Scope fidelity | 1 | 0 | 1 |

## Trend
- Generator improving: core-calc fixed on first re-attempt
- Evaluator checking all dimensions consistently
- No findings yet in integration dimension — may indicate that integration tests are weak
```

### Health Check Warnings

The `/long-run status` display auto-generates warnings when patterns suggest problems:

| Warning | Trigger | What It Means |
|---------|---------|---------------|
| "Evaluator checked <5 dimensions on {N} features" | Coverage < 100% | Evaluator is skipping dimensions — evaluation is incomplete |
| "All findings in one dimension" | Finding diversity < 3/5 | Evaluator may be fixating; other dimensions unchecked in practice |
| "Clean-pass rate is 100% for 5+ features" | Perfect streak | Either excellent code OR weak evaluation — spot-check manually |
| "Evaluator hit rate below 50%" | Most findings overruled | Evaluator is producing low-quality findings |
| "No findings in {dimension} across all features" | One dimension never triggered | That dimension may not be relevant OR evaluator is skipping it |

## Anti-Goal Verification

Each anti-goal in the specsheet must have a concrete verification method:

```markdown
## Anti-Goals (Specsheet Format)
| Anti-Goal | Verification Method | Command/Check |
|-----------|-------------------|---------------|
| No hardcoded values | Grep for literals matching test expectations | `grep -rn "0.85\|42\|expected_value" src/` |
| No regression shortcuts | Check for fitting imports | `grep -rn "LinearRegression\|\.fit(" src/` |
| No skipped validation | Every public function validates inputs | Review function signatures for type checks |
```

The evaluator runs each verification command and reports the result. If a command finds a match, the evaluator investigates whether it's a genuine violation or a false positive.

## Re-Evaluation (AlphaStar League Training Pattern)

As the project matures, early features may have gaps that weren't visible when first evaluated. `/long-run re-evaluate` re-runs the evaluator on all `passing` features with the current context.

**When to re-evaluate:**
- After completing a wave of new features (new integration context)
- After updating the specsheet (new anti-goals or criteria)
- Before project completion (final sweep)

**What changes in re-evaluation:**
- The evaluator has access to all currently-passing features, not just the one being evaluated
- Integration checks can now test actual cross-feature interactions
- Anti-goals may have evolved since the original evaluation

## Reward Hacking Detection Patterns

Even with coverage-based evaluation, the evaluator should watch for these patterns:

### 1. Hardcoded Values
```python
# SUSPICIOUS: Magic number that matches expected test output
def calculate_score(data):
    return 0.85  # Why this specific number?
```

### 2. Regression/Fitting Shortcuts
```python
# SUSPICIOUS: Fitting to the test data instead of computing from principles
model = LinearRegression().fit(reference_inputs, reference_outputs)
```

### 3. Trivially Passing Tests
```python
# SUSPICIOUS: Test that can never fail
def test_calculation():
    result = calculate(data)
    assert result is not None  # This asserts nothing useful
```

### 4. Mock Everything Pattern
```python
# SUSPICIOUS: Test mocks away the very thing it should be testing
@mock.patch('module.core_function')
def test_core_function(mock_fn):
    mock_fn.return_value = expected
    assert core_function() == expected  # Circular!
```

## Human Override Protocol

The human can override any evaluator finding:

1. **Dismiss as false positive** → finding removed from scorecard
2. **Dismiss as not worth fixing** → finding recorded as note, not blocking
3. **Confirm finding** → feature must be fixed
4. **Escalate** → increase severity (note → blocker)

Override rate is tracked in the scorecard. High override rates (>50%) indicate the evaluator needs recalibration.

## Evaluation Report Format (`Plans/features/{feature-id}-eval.md`)

```markdown
# Evaluation Report: {Feature Name}

**Evaluator:** long-run-evaluator
**Date:** {timestamp}
**Verdict:** {PASS / PASS with notes / NEEDS WORK / INCOMPLETE}

## Dimension Coverage

| # | Dimension | Checked? | Finding? | Details |
|---|-----------|----------|----------|---------|
| 1 | Correctness | Yes | No | Tests pass; acceptance criteria met |
| 2 | Test quality | Yes | Note | test_empty_input doesn't assert output shape |
| 3 | Anti-goal compliance | Yes | No | All 3 verification commands clean |
| 4 | Integration | Yes | No | Output format matches downstream consumer |
| 5 | Scope fidelity | Yes | No | Implementation matches brief |

## Findings

### Finding 1: Test doesn't verify output shape — Note (Test quality)

**Location:** `tests/test_loader.py:28`
**Evidence:** `assert result is not None` — doesn't check DataFrame shape or dtypes
**Impact:** Would not catch a bug that returns the wrong number of rows
**Suggestion:** Add `assert result.shape == (10, 4)` and `assert list(result.dtypes) == [...]`

## Anti-Goal Verification Results

| Anti-Goal | Command | Result | Status |
|-----------|---------|--------|--------|
| No hardcoded values | `grep -rn "0.85" src/` | No matches | Compliant |
| No regression shortcuts | `grep -rn "\.fit(" src/` | No matches | Compliant |

## Test Explanation Review

- "What's NOT Tested" gaps: 2 listed, both reasonable (files >1GB, concurrent access)
- Coverage claims match actual tests: Yes
- Missing gaps not self-reported: None found

## Recommendation

PASS with notes. One minor test quality observation. No blockers.
```
