"""Pytest for skills/cv-creation/scripts/validate_application.py against mini-app."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "cv-creation" / "scripts" / "validate_application.py"
MINI = ROOT / "skills" / "cv-creation" / "assets" / "fixtures" / "mini-app"
APP = MINI / "applications" / "acme-de-2026-01-01"


def _load_validate_application():
    spec = importlib.util.spec_from_file_location("validate_application", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


va = _load_validate_application()


def test_mini_app_profile_and_app_pass_validator():
    argv = [
        "--style",
        str(MINI / "profile" / "export-style.yaml"),
        "--skills",
        str(MINI / "profile" / "skills.yaml"),
        "--composition",
        str(APP / "composition.yaml"),
        "--draft",
        str(APP / "draft.md"),
    ]
    assert va.main(argv) == 0
