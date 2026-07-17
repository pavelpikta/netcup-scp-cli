"""Contract test: every OpenAPI operation is declared implemented or skipped."""

import json
from pathlib import Path

from openapi_coverage import OPENAPI_COVERAGE, SKIP_REASONS

REPO_ROOT = Path(__file__).resolve().parents[1]
OPENAPI_PATH = REPO_ROOT / "openapi.json"
HTTP_METHODS = {"get", "post", "put", "patch", "delete"}


def _openapi_operations() -> set[str]:
    spec = json.loads(OPENAPI_PATH.read_text())
    ops: set[str] = set()
    for path, methods in spec.get("paths", {}).items():
        for method, op in methods.items():
            if method not in HTTP_METHODS or not isinstance(op, dict):
                continue
            ops.add(f"{method.upper()} {path}")
    return ops


def test_openapi_file_exists() -> None:
    assert OPENAPI_PATH.is_file()


def test_coverage_map_matches_openapi() -> None:
    ops = _openapi_operations()
    declared = set(OPENAPI_COVERAGE)
    missing = ops - declared
    extra = declared - ops
    assert not missing, f"OpenAPI ops not in coverage map (triage them): {sorted(missing)}"
    assert not extra, f"Coverage map has ops absent from OpenAPI: {sorted(extra)}"


def test_coverage_statuses_valid() -> None:
    allowed = {"implemented", "skipped"}
    for op, status in OPENAPI_COVERAGE.items():
        assert status in allowed, f"{op}: invalid status {status!r}"
        if status == "skipped":
            assert op in SKIP_REASONS, f"{op}: skipped without reason"
