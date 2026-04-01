# When to Mock

Mock at **system boundaries** only:

- External APIs (NCBI, UniProt, etc.)
- Databases
- File system (sometimes — prefer `tmp_path` fixture)
- Time / randomness (prefer `rng` parameter injection — see [stochastic.md](stochastic.md))
- Network requests

Don't mock:

- Your own classes/modules
- Internal collaborators
- Anything you control

## Designing for Testability: Dependency Injection

Pass external dependencies in rather than creating them internally:

```python
# GOOD — easy to test, easy to mock at the boundary
def fetch_gene_info(gene_symbol: str, client: NCBIClient) -> GeneInfo:
    """Fetch gene metadata from NCBI.

    Args:
        gene_symbol: HGNC gene symbol (e.g., "BRCA1").
        client: NCBI API client. Injected for testability.

    Returns:
        GeneInfo with symbol, name, chromosome, and coordinates.
    """
    return client.query(gene_symbol)


# BAD — creates its own client, impossible to test without network
def fetch_gene_info(gene_symbol: str) -> GeneInfo:
    client = NCBIClient(api_key=os.environ["NCBI_API_KEY"])
    return client.query(gene_symbol)
```

## Mocking External APIs in Tests

```python
from unittest.mock import MagicMock


def test_fetch_gene_info_parses_response():
    """Guards against parsing bugs when NCBI response format changes."""
    mock_client = MagicMock()
    mock_client.query.return_value = {
        "symbol": "BRCA1",
        "name": "BRCA1 DNA repair associated",
        "chromosome": "17",
    }

    result = fetch_gene_info("BRCA1", client=mock_client)
    assert result.symbol == "BRCA1"
    assert result.chromosome == "17"
```

## Prefer Real Objects Over Mocks

When possible, use lightweight real implementations:

```python
# BETTER than a mock — a real in-memory implementation
class InMemoryVariantStore:
    """Test double for VariantStore that stores data in a dict."""

    def __init__(self):
        self.variants = {}

    def save(self, variant_id: str, data: dict) -> None:
        self.variants[variant_id] = data

    def load(self, variant_id: str) -> dict:
        return self.variants[variant_id]


def test_pipeline_saves_results():
    """Guards against data loss in the save step."""
    store = InMemoryVariantStore()
    run_pipeline(data, store=store)
    assert "A2T" in store.variants
```

## pytest Fixtures for Common Mocks

```python
import pytest
from pathlib import Path


@pytest.fixture
def sample_fastq(tmp_path: Path) -> Path:
    """Create a minimal FASTQ file for testing parsers."""
    fastq = tmp_path / "test.fastq"
    fastq.write_text(
        "@read1\n"
        "ACGTACGTACGT\n"
        "+\n"
        "IIIIIIIIIIII\n"
    )
    return fastq


def test_fastq_parser_extracts_sequence(sample_fastq):
    """Guards against parser regression on standard FASTQ format."""
    records = parse_fastq(sample_fastq)
    assert records[0].sequence == "ACGTACGTACGT"
```

## What NOT to Mock

```python
# BAD — mocking your own function defeats the purpose
def test_pipeline(mocker):
    mocker.patch("pipeline.normalize_scores", return_value=fake_scores)
    result = run_pipeline(data)
    # You're not testing normalize_scores at all!

# GOOD — test through the real interface
def test_pipeline():
    result = run_pipeline(test_data)
    assert result["score"].between(-10, 10).all()
```
