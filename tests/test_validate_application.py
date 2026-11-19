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


def _mini_argv(**overrides: Path) -> list[str]:
    paths = {
        "style": MINI / "profile" / "export-style.yaml",
        "skills": MINI / "profile" / "skills.yaml",
        "composition": APP / "composition.yaml",
        "draft": APP / "draft.md",
        "evidence": MINI / "profile" / "evidence.yaml",
        "matching": APP / "matching.yaml",
        "identity": MINI / "profile" / "identity.yaml",
    }
    paths.update(overrides)
    argv: list[str] = []
    for key, path in paths.items():
        argv.extend([f"--{key}", str(path)])
    return argv


def test_mini_app_profile_and_app_pass_validator():
    assert va.main(_mini_argv()) == 0


def test_corrupt_composition_yaml_exits_2_no_traceback(tmp_path: Path, capfd):
    bad = tmp_path / "composition.yaml"
    bad.write_text("bullets: [unclosed\n", encoding="utf-8")
    rc = va.main(_mini_argv(composition=bad))
    assert rc == 2
    err = capfd.readouterr().err
    assert "ERROR:" in err
    assert "Recovery:" in err
    assert "Traceback" not in err


def test_list_root_evidence_exits_2_no_traceback(tmp_path: Path, capfd):
    bad = tmp_path / "evidence.yaml"
    bad.write_text("- not\n- a\n- mapping\n", encoding="utf-8")
    rc = va.main(_mini_argv(evidence=bad))
    assert rc == 2
    err = capfd.readouterr().err
    assert "ERROR:" in err
    assert "Recovery:" in err
    assert "Traceback" not in err
