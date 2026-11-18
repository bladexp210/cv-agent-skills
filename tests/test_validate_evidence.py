"""Pytest for skills/evidence-bank/scripts/validate_evidence.py against fixtures."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "evidence-bank" / "scripts" / "validate_evidence.py"
FIXTURES = ROOT / "skills" / "evidence-bank" / "assets" / "fixtures"
OK = FIXTURES / "ok.yaml"
BAD = FIXTURES / "bad-missing-source.yaml"


def _load_validate_evidence():
    spec = importlib.util.spec_from_file_location("validate_evidence", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


ve = _load_validate_evidence()


def test_ok_fixture_exits_0():
    assert ve.main([str(OK)]) == 0


def test_bad_missing_source_exits_1():
    assert ve.main([str(BAD)]) == 1


def test_validate_spot_checks_missing_source_error():
    data = yaml.safe_load(BAD.read_text(encoding="utf-8"))
    errors, warnings = ve.validate(data)
    assert any("missing source" in e for e in errors)
    assert errors  # hard-fail path
    # empty bank / orphan experience warnings are orthogonal; ok fixture has none of these errors
    ok_data = yaml.safe_load(OK.read_text(encoding="utf-8"))
    ok_errors, _ = ve.validate(ok_data)
    assert ok_errors == []
