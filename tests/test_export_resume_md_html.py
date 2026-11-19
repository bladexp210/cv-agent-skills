"""Pytest for export_resume md/html on a temp copy of mini-app (never mutates fixtures)."""
from __future__ import annotations

import hashlib
import importlib.util
import shutil
import sys
from pathlib import Path

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
