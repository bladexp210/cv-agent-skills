"""Pytest for export_resume md/html on a temp copy of mini-app (never mutates fixtures)."""
from __future__ import annotations

import hashlib
import importlib.util
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "cv-creation" / "scripts" / "export_resume.py"
MINI = ROOT / "skills" / "cv-creation" / "assets" / "fixtures" / "mini-app"
APP_REL = Path("applications") / "acme-de-2026-01-01"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def _fingerprint_tree(root: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(root))] = _sha256(p)
    return out


def _load_export_resume():
    spec = importlib.util.spec_from_file_location("export_resume", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


er = _load_export_resume()


def test_export_md_html_on_temp_copy_does_not_mutate_fixtures(tmp_path: Path):
    before = _fingerprint_tree(MINI)

    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    app_dir = career / APP_REL

    rc = er.main(
        [
            "--formats",
            "md,html",
            "--career-root",
            str(career),
            str(app_dir),
        ]
    )
    assert rc == 0

    export_dir = app_dir / "export"
    assert (export_dir / "resume.md").is_file()
    assert (export_dir / "resume.html").is_file()
    assert (export_dir / "export_manifest.yaml").is_file()

    after = _fingerprint_tree(MINI)
    assert after == before, "committed mini-app fixtures must not change"


def test_empty_identity_exits_4(tmp_path: Path):
    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    identity = career / "profile" / "identity.yaml"
    identity.write_bytes(b"")
    app_dir = career / APP_REL
    export_dir = app_dir / "export"
    if export_dir.exists():
        shutil.rmtree(export_dir)
    rc = er.main(
        ["--formats", "md", "--career-root", str(career), str(app_dir)]
    )
    assert rc == 4
    assert not (export_dir / "resume.md").exists()


def test_symlink_resume_md_does_not_overwrite_outside(tmp_path: Path):
    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    app_dir = career / APP_REL
    export_dir = app_dir / "export"
    export_dir.mkdir(parents=True, exist_ok=True)
    existing = export_dir / "resume.md"
    if existing.exists() or existing.is_symlink():
        existing.unlink()
    victim = tmp_path / "outside_victim.md"
    victim.write_text("SAFE_MARKER\n", encoding="utf-8")
    link = export_dir / "resume.md"
    link.symlink_to(victim)
    rc = er.main(
        ["--formats", "md", "--career-root", str(career), str(app_dir)]
    )
    assert rc == 5
    assert victim.read_text(encoding="utf-8") == "SAFE_MARKER\n"
    assert link.is_symlink()


def test_symlink_export_dir_outside_refused(tmp_path: Path):
    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    app_dir = career / APP_REL
    existing_export = app_dir / "export"
    if existing_export.exists() or existing_export.is_symlink():
        if existing_export.is_symlink() or existing_export.is_file():
            existing_export.unlink()
        else:
            shutil.rmtree(existing_export)
    outside = tmp_path / "outside_export"
    outside.mkdir()
    export_link = app_dir / "export"
    export_link.symlink_to(outside)
    rc = er.main(
        ["--formats", "md", "--career-root", str(career), str(app_dir)]
    )
    assert rc == 5
    assert list(outside.iterdir()) == []


def test_corrupt_identity_yaml_exits_2_no_traceback(tmp_path: Path, capfd):
    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    (career / "profile" / "identity.yaml").write_text("name: [unclosed\n", encoding="utf-8")
    app_dir = career / APP_REL
    rc = er.main(["--formats", "md", "--career-root", str(career), str(app_dir)])
    assert rc == 2
    err = capfd.readouterr().err
    assert "ERROR:" in err
    assert "Recovery:" in err
    assert "Traceback" not in err


def test_list_root_style_exits_2_no_traceback(tmp_path: Path, capfd):
    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    (career / "profile" / "export-style.yaml").write_text("- just\n- a\n- list\n", encoding="utf-8")
    app_dir = career / APP_REL
    rc = er.main(["--formats", "md", "--career-root", str(career), str(app_dir)])
    assert rc == 2
    err = capfd.readouterr().err
    assert "ERROR:" in err
    assert "Recovery:" in err
    assert "Traceback" not in err


def test_control_chars_stripped_from_md(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    real_load = er.load_yaml

    def load_with_nul(path: Path):
        data = real_load(path)
        if path.name == "identity.yaml":
            data = dict(data)
            data["name"] = "Ada\x00Example"
        return data

    monkeypatch.setattr(er, "load_yaml", load_with_nul)
    app_dir = career / APP_REL
    rc = er.main(["--formats", "md", "--career-root", str(career), str(app_dir)])
    assert rc == 0
    text = (app_dir / "export" / "resume.md").read_text(encoding="utf-8")
    assert "\x00" not in text
    assert "AdaExample" in text


def test_control_chars_stripped_from_docx(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    pytest.importorskip("docx")
    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    real_load = er.load_yaml

    def load_with_nul(path: Path):
        data = real_load(path)
        if path.name == "identity.yaml":
            data = dict(data)
            data["name"] = "Ada\x00Example"
        return data

    monkeypatch.setattr(er, "load_yaml", load_with_nul)
    app_dir = career / APP_REL
    rc = er.main(["--formats", "docx", "--career-root", str(career), str(app_dir)])
    assert rc == 0
    from docx import Document

    doc = Document(app_dir / "export" / "resume.docx")
    joined = "\n".join(p.text for p in doc.paragraphs)
    assert "\x00" not in joined
    assert "AdaExample" in joined


def test_atomic_export_leaves_prior_intact_on_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    app_dir = career / APP_REL
    export_dir = app_dir / "export"
    export_dir.mkdir(parents=True, exist_ok=True)
    prior = export_dir / "resume.md"
    prior.write_text("PRIOR_EXPORT\n", encoding="utf-8")

    real_render_md = er.render_md
    calls = {"n": 0}

    def boom_md(*args, **kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("simulated render failure")
        return real_render_md(*args, **kwargs)

    monkeypatch.setattr(er, "render_md", boom_md)
    rc = er.main(["--formats", "md", "--career-root", str(career), str(app_dir)])
    assert rc == 2
    assert prior.read_text(encoding="utf-8") == "PRIOR_EXPORT\n"
    assert not any(app_dir.glob(".export_staging_*"))


def test_esc_apostrophe_and_bidi(tmp_path: Path):
    assert "&#39;" in er._esc("O'Brien")
    assert "\u202e" not in er._esc("ab\u202ecd")
    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    (career / "profile" / "identity.yaml").write_text(
        "name: \"O'Brien\"\n"
        "contact:\n  email: ada@example.com\n  phone: ''\n"
        "  location: Paris\n  links: []\n"
        "education: []\n",
        encoding="utf-8",
    )
    app_dir = career / APP_REL
    rc = er.main(["--formats", "html", "--career-root", str(career), str(app_dir)])
    assert rc == 0
    html = (app_dir / "export" / "resume.html").read_text(encoding="utf-8")
    assert "&#39;" in html
    assert "O'Brien" not in html or "O&#39;Brien" in html


def test_scalar_links_warns_and_skips(tmp_path: Path, capfd):
    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    (career / "profile" / "identity.yaml").write_text(
        "name: Ada Example\n"
        "contact:\n  email: ada@example.com\n  phone: ''\n"
        "  location: Paris\n"
        "  links: https://example.com/me\n"
        "education: []\n",
        encoding="utf-8",
    )
    app_dir = career / APP_REL
    rc = er.main(["--formats", "md", "--career-root", str(career), str(app_dir)])
    assert rc == 0
    err = capfd.readouterr().err
    assert "WARN:" in err
    assert "contact.links" in err
    md = (app_dir / "export" / "resume.md").read_text(encoding="utf-8")
    # Must not explode into one line per character of the URL.
    assert md.count("https://example.com/me") == 0
    assert "h\nt\nt\np" not in md


def test_fonts_warn_on_docx(tmp_path: Path, capfd):
    pytest.importorskip("docx")
    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    app_dir = career / APP_REL
    rc = er.main(["--formats", "docx", "--career-root", str(career), str(app_dir)])
    assert rc == 0
    err = capfd.readouterr().err
    assert "WARN:" in err
    assert "fonts" in err.lower()
    assert "DOCX" in err or "docx" in err
