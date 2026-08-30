"""Regression tests for the public distribution, import, and CLI identity."""

from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised by the Python 3.10 CI job
    import tomli as tomllib


ROOT = Path(__file__).resolve().parents[1]


def test_public_identity_remains_docsmoke() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = metadata["project"]

    assert project["name"] == "docsmoke"
    assert project["scripts"] == {"docsmoke": "docsmoke.cli:app"}
    assert (ROOT / "src" / "docsmoke" / "__init__.py").is_file()


def test_distribution_links_target_the_canonical_organization_repository() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    urls = metadata["project"]["urls"]

    assert urls["Repository"] == "https://github.com/fillbyte/docsmoke"
    assert urls["Documentation"] == "https://fillbyte.github.io/docsmoke/"
