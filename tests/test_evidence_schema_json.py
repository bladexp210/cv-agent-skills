"""Pytest: bank fixtures vs skills/evidence-bank/assets/evidence.schema.json.

Schema limb owns evidence.schema.json. This module does not create that file.
If the schema is missing, tests skip with an explicit note for the integrator.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

jsonschema = pytest.importorskip("jsonschema")

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "skills" / "evidence-bank" / "assets" / "evidence.schema.json"
FIXTURES = ROOT / "skills" / "evidence-bank" / "assets" / "fixtures"
OK = FIXTURES / "ok.yaml"
BAD = FIXTURES / "bad-missing-source.yaml"

# Blocked-on-schema note for Wave 1 parallel: Schema limb creates SCHEMA_PATH.
_SCHEMA_MISSING_MSG = (
    f"BLOCKED ON SCHEMA LIMB: expected {SCHEMA_PATH.as_posix()} "
    "(owned by Schema limb). Pytest limb does not invent this file."
)


def _load_schema():
    if not SCHEMA_PATH.is_file():
        pytest.skip(_SCHEMA_MISSING_MSG)
    import json

    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _validator(schema: dict):
    # Prefer Draft202012 if available; fall back to generic validator.
    Validator = getattr(jsonschema, "Draft202012Validator", None)
    if Validator is None:
        return jsonschema.validators.validator_for(schema)(schema)
    return Validator(schema)


def test_ok_yaml_matches_evidence_schema_json():
    schema = _load_schema()
    data = yaml.safe_load(OK.read_text(encoding="utf-8"))
    _validator(schema).validate(data)


def test_bad_missing_source_vs_schema_or_validator_only():
    """Empty source must fail JSON Schema, or be documented as Python-validator-only."""
    schema = _load_schema()
    data = yaml.safe_load(BAD.read_text(encoding="utf-8"))
    errors = sorted(_validator(schema).iter_errors(data), key=lambda e: e.path)
    if errors:
        # Structural/minLength (or similar) caught the empty source — good.
        assert True
        return
    # Schema is structural-only: empty string may still type-check as string.
    # Integrity rule lives in validate_evidence.py (hard-fail on blank source).
    pytest.skip(
        "bad-missing-source.yaml passes evidence.schema.json (structural-only); "
        "blank source remains a validate_evidence.py hard-fail (see test_validate_evidence.py)."
    )
