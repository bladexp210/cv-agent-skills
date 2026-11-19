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


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _base_evidence_yaml(*, status: str = "fact", probe_history: str = "[]", extra_rows: str = "", extra_links: str = "") -> str:
    return f"""experiences:
  - id: exp_acme
    title: Data Engineer
    org: Acme
    start: 2022-03
    end: 2024-08
    location: Paris, FR
evidence:
  - id: ev_001
    experience_id: exp_acme
    fact: "Rebuilt nightly billing ETL with Python and Airflow; cut runtime 40%."
    status: {status}
    source: "fixture"
    probe_history: {probe_history}
    revision_count: 0
{extra_rows}evidence_skills:
  - evidence_id: ev_001
    skill_id: sk_python
    strength: strong
    recency: current
  - evidence_id: ev_001
    skill_id: sk_airflow
    strength: strong
    recency: current
{extra_links}"""


def _base_composition_yaml(*, bullets: str | None = None, bullet_text: str | None = None) -> str:
    if bullets is None and bullet_text is None:
        bullets_block = """bullets:
  - id: b_001
    section: experience
    experience_id: exp_acme
    text: "Rebuilt nightly billing ETL (Python, Airflow); −40% runtime."
    ev_ids: [ev_001]
    skill_ids: [sk_python, sk_airflow]
"""
    elif bullets is not None:
        bullets_block = bullets
    else:
        bullets_block = f"""bullets:
  - id: b_001
    section: experience
    experience_id: exp_acme
    text: {bullet_text}
    ev_ids: [ev_001]
    skill_ids: [sk_python, sk_airflow]
"""
    return f"""section_plan:
  - {{id: header, order: 1, source: identity}}
  - {{id: experience, order: 2, experiences: [exp_acme]}}
  - {{id: skills, order: 3, source: matching}}
{bullets_block}skills_line:
  - {{group: Languages, items: [Python]}}
  - {{group: Tools, items: [Airflow]}}
grounding:
  uncovered: []
  unconfirmed_differentiators_used: []
  cited_ev_ids: [ev_001]
buffered_flags: []
"""


def test_waived_empty_probe_history_dict_fails(tmp_path: Path):
    evidence = _write(
        tmp_path / "evidence.yaml",
        _base_evidence_yaml(status="waived", probe_history="[{}]"),
    )
    composition = _write(tmp_path / "composition.yaml", _base_composition_yaml())
    argv = _mini_full_argv(composition=composition, evidence=evidence)
    assert va.main(argv) == 1


def test_waived_with_waiver_reason_ok(tmp_path: Path):
    evidence = _write(
        tmp_path / "evidence.yaml",
        """experiences:
  - id: exp_acme
    title: Data Engineer
    org: Acme
    start: 2022-03
    end: 2024-08
    location: Paris, FR
evidence:
  - id: ev_001
    experience_id: exp_acme
    fact: "Rebuilt nightly billing ETL with Python and Airflow; cut runtime 40%."
    status: waived
    waiver_reason: "out of scope for this role"
    source: "fixture"
    probe_history: []
    revision_count: 0
evidence_skills:
  - evidence_id: ev_001
    skill_id: sk_python
    strength: strong
    recency: current
  - evidence_id: ev_001
    skill_id: sk_airflow
    strength: strong
    recency: current
""",
    )
    composition = _write(tmp_path / "composition.yaml", _base_composition_yaml())
    argv = _mini_full_argv(composition=composition, evidence=evidence)
    assert va.main(argv) == 0


def test_waived_with_probe_history_answer_ok(tmp_path: Path):
    evidence = _write(
        tmp_path / "evidence.yaml",
        _base_evidence_yaml(
            status="waived",
            probe_history='[{answer: "metric not verifiable"}]',
        ),
    )
    composition = _write(tmp_path / "composition.yaml", _base_composition_yaml())
    argv = _mini_full_argv(composition=composition, evidence=evidence)
    assert va.main(argv) == 0


def test_duplicate_evidence_id_fails(tmp_path: Path):
    evidence = _write(
        tmp_path / "evidence.yaml",
        _base_evidence_yaml(
            extra_rows="""  - id: ev_001
    experience_id: exp_acme
    fact: "duplicate row"
    status: fact
    source: "fixture"
    probe_history: []
    revision_count: 0
""",
        ),
    )
    composition = _write(tmp_path / "composition.yaml", _base_composition_yaml())
    argv = _mini_full_argv(composition=composition, evidence=evidence)
    assert va.main(argv) == 1


def test_duplicate_evidence_skills_link_fails(tmp_path: Path):
    evidence = _write(
        tmp_path / "evidence.yaml",
        _base_evidence_yaml(
            extra_links="""  - evidence_id: ev_001
    skill_id: sk_python
    strength: weak
    recency: current
""",
        ),
    )
    composition = _write(tmp_path / "composition.yaml", _base_composition_yaml())
    argv = _mini_full_argv(composition=composition, evidence=evidence)
    assert va.main(argv) == 1


def test_corrupt_identity_fails(tmp_path: Path):
    bad_identity = _write(tmp_path / "identity.yaml", "name: [unclosed\n")
    argv = _mini_full_argv()
    # replace --identity path
    idx = argv.index("--identity")
    argv = argv[: idx + 1] + [str(bad_identity)] + argv[idx + 2 :]
    assert va.main(argv) == 1


def test_bullets_null_fails(tmp_path: Path):
    composition = _write(
        tmp_path / "composition.yaml",
        _base_composition_yaml(bullets="bullets: null\n"),
    )
    argv = _mini_full_argv(composition=composition)
    assert va.main(argv) == 1


def test_bullet_text_null_fails(tmp_path: Path):
    composition = _write(
        tmp_path / "composition.yaml",
        _base_composition_yaml(bullet_text="null"),
    )
    argv = _mini_full_argv(composition=composition)
    assert va.main(argv) == 1


def test_dangling_evidence_skills_evidence_id_fails(tmp_path: Path):
    evidence = _write(
        tmp_path / "evidence.yaml",
        _base_evidence_yaml(
            extra_links="""  - evidence_id: ev_missing
    skill_id: sk_python
    strength: strong
    recency: current
""",
        ),
    )
    composition = _write(tmp_path / "composition.yaml", _base_composition_yaml())
    argv = _mini_full_argv(composition=composition, evidence=evidence)
    assert va.main(argv) == 1
