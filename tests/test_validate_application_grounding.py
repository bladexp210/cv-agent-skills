"""G4 grounding checks for validate_application.py."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "cv-creation" / "scripts" / "validate_application.py"
MINI = ROOT / "skills" / "cv-creation" / "assets" / "fixtures" / "mini-app"
APP = MINI / "applications" / "acme-de-2026-01-01"
BAD = ROOT / "skills" / "cv-creation" / "assets" / "fixtures" / "grounding-bad"


def _load():
    spec = importlib.util.spec_from_file_location("validate_application_grounding", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


va = _load()

MINI_EVIDENCE = MINI / "profile" / "evidence.yaml"
MINI_SKILLS = MINI / "profile" / "skills.yaml"
MINI_MATCHING = APP / "matching.yaml"
MINI_IDENTITY = MINI / "profile" / "identity.yaml"
MINI_STYLE = MINI / "profile" / "export-style.yaml"


def _mini_full_argv(*, composition: Path | None = None, draft: Path | None = None, evidence: Path | None = None):
    return [
        "--style",
        str(MINI_STYLE),
        "--skills",
        str(MINI_SKILLS),
        "--composition",
        str(composition or (APP / "composition.yaml")),
        "--draft",
        str(draft or (APP / "draft.md")),
        "--evidence",
        str(evidence or MINI_EVIDENCE),
        "--matching",
        str(MINI_MATCHING),
        "--identity",
        str(MINI_IDENTITY),
    ]


def test_mini_app_full_grounding_ok():
    assert va.main(_mini_full_argv()) == 0


def test_empty_ev_ids_fails():
    argv = _mini_full_argv(
        composition=BAD / "empty-ev-ids" / "composition.yaml",
        draft=APP / "draft.md",
    )
    assert va.main(argv) == 1


def test_missing_ev_fails():
    argv = _mini_full_argv(composition=BAD / "missing-ev" / "composition.yaml")
    assert va.main(argv) == 1


def test_non_fact_status_fails():
    argv = _mini_full_argv(
        composition=BAD / "non-fact-status" / "composition.yaml",
        evidence=BAD / "non-fact-status" / "evidence.yaml",
    )
    assert va.main(argv) == 1


def test_skill_not_on_evidence_fails():
    argv = _mini_full_argv(composition=BAD / "skill-not-on-evidence" / "composition.yaml")
    assert va.main(argv) == 1


def test_uncovered_nonempty_fails():
    argv = _mini_full_argv(composition=BAD / "uncovered" / "composition.yaml")
    assert va.main(argv) == 1


def test_draft_missing_bullet_text_fails():
    argv = _mini_full_argv(
        composition=BAD / "draft-mismatch" / "composition.yaml",
        draft=BAD / "draft-mismatch" / "draft.md",
    )
    assert va.main(argv) == 1


def test_cited_not_listed_fails():
    argv = _mini_full_argv(composition=BAD / "cited-not-listed" / "composition.yaml")
    assert va.main(argv) == 1


def test_composition_without_evidence_fails():
    argv = [
        "--composition",
        str(APP / "composition.yaml"),
        "--skills",
        str(MINI_SKILLS),
    ]
    assert va.main(argv) == 1


def test_check_grounding_empty_ev_ids_message():
    comp = va.load_yaml(BAD / "empty-ev-ids" / "composition.yaml")
    evidence = va.load_yaml(MINI_EVIDENCE)
    errors = va.check_grounding(comp, evidence)
    assert any("ev_ids length must be ≥ 1" in e for e in errors)
