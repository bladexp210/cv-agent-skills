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
