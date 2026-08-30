from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from docsmoke.config import Config
from docsmoke.runner import scan

_ROOT = Path(__file__).resolve().parent.parent
_CANONICAL_SCHEMA_URL = "https://fillbyte.github.io/docsmoke/schemas/report.schema.json"


def test_json_report_matches_schema(tmp_path: Path) -> None:
    markdown_path = tmp_path / "README.md"
    markdown_path.write_text(
        "```bash docsmoke\n# docsmoke: name=hello; expect-contains=hello\nprintf 'hello\\n'\n```\n",
        encoding="utf-8",
    )
    schema = json.loads((_ROOT / "schemas" / "report.schema.json").read_text(encoding="utf-8"))

    report = scan([markdown_path], config=Config())

    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(report.to_dict())


def test_pages_artifact_publishes_the_canonical_schema() -> None:
    schema_path = _ROOT / "schemas" / "report.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    workflow = (_ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")

    assert schema["$id"] == _CANONICAL_SCHEMA_URL
    assert "mkdir -p _site/schemas" in workflow
    assert "cp -R docs/site/. _site/" in workflow
    assert "cp schemas/report.schema.json _site/schemas/report.schema.json" in workflow
    assert "cmp --silent schemas/report.schema.json _site/schemas/report.schema.json" in workflow
    assert f'--arg canonical_id "{_CANONICAL_SCHEMA_URL}"' in workflow
    assert "path: _site" in workflow
