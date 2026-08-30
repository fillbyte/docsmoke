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


def test_distribution_uses_pep_639_license_metadata() -> None:
    metadata = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = metadata["project"]

    assert project["license"] == "Apache-2.0"
    assert project["license-files"] == ["LICENSE", "NOTICE"]
    assert "License :: OSI Approved :: Apache Software License" not in project["classifiers"]


def test_release_publishes_pinned_multi_arch_container_images() -> None:
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    ci_workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    qemu = "uses: docker/setup-qemu-action@96fe6ef7f33517b61c61be40b68a1882f3264fb8 # v4.2.0"
    buildx = "uses: docker/setup-buildx-action@37fe631027851001ddb9b187196cc803df7f5f0e # v4.3.0"

    assert qemu in workflow
    assert buildx in workflow
    assert workflow.index(qemu) < workflow.index(buildx)
    assert "platforms: linux/amd64,linux/arm64" in workflow
    assert qemu in ci_workflow
    assert buildx in ci_workflow
    assert ci_workflow.index(qemu) < ci_workflow.index(buildx)
    assert 'platforms=("linux/amd64" "linux/arm64")' in ci_workflow
    assert 'docker run --rm --platform "$platform" "$image" --version' in ci_workflow
