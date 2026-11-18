#!/usr/bin/env python3
"""Regenerate applications/<app>/views/* from YAML sources. Never blocks on mismatch."""
from __future__ import annotations

import argparse
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_yaml(path: Path) -> dict:
    if not path.is_file():
        return {}
    if yaml is None:
        raise SystemExit("PyYAML required")
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def write_view(path: Path, sources: list[Path], body: str) -> str:
    joined = b"".join(s.read_bytes() if s.is_file() else b"" for s in sources)
    digest = sha256_bytes(joined)
    banner = f"<!-- GENERATED from {' + '.join(s.name for s in sources)}. Do not edit. sha256: {digest} -->\n"
    path.write_text(banner + body, encoding="utf-8")
    return digest


def regen(app_dir: Path) -> int:
    views = app_dir / "views"
    views.mkdir(exist_ok=True)
    meta = load_yaml(app_dir / "meta.yaml")
    req = app_dir / "requirements.yaml"
    kw = app_dir / "keywords.yaml"
    scores = app_dir / "scores.yaml"
    matching = app_dir / "matching.yaml"
    manifest_sources = {}

    app = meta.get("application") or {}
    title = f"{app.get('company', 'App')} · {app.get('role', '')} — CV application"

    body = f"# Requirements\n\nSource: requirements.yaml\n\n```yaml\n{(req.read_text(encoding='utf-8') if req.is_file() else 'requirements: []')}\n```\n"
    manifest_sources["requirements.md"] = write_view(views / "requirements.md", [req], body)

    body = f"# Keywords\n\n```yaml\n{(kw.read_text(encoding='utf-8') if kw.is_file() else 'jd_keywords: []')}\n```\n"
    manifest_sources["keywords.md"] = write_view(views / "keywords.md", [kw], body)

    body = f"# Scoring\n\n```yaml\n{(scores.read_text(encoding='utf-8') if scores.is_file() else 'job_skill_scores: []')}\n```\n"
    manifest_sources["scoring.md"] = write_view(views / "scoring.md", [scores], body)

    body = f"# Matching\n\n```yaml\n{(matching.read_text(encoding='utf-8') if matching.is_file() else 'matching: []')}\n```\n"
    manifest_sources["matching.md"] = write_view(views / "matching.md", [matching], body)

    tracker = f"""# {title}

> [!info] {app.get('id', app_dir.name)}
> JD: {app.get('jd_source', '')} · created {app.get('created', '')} · updated {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%MZ')}

Stage: {app.get('stage', '')} · flags {len(app.get('open_flags') or [])}
"""
    manifest_sources["tracker.md"] = write_view(
        views / "tracker.md",
        [app_dir / "meta.yaml", matching, scores],
        tracker,
    )

    man = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "sources": {k: v for k, v in manifest_sources.items()},
    }
    if yaml:
        (views / "_manifest.yaml").write_text(yaml.safe_dump(man, sort_keys=False), encoding="utf-8")
    print(f"Regenerated views in {views}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("app_dir", type=Path)
    args = p.parse_args(argv)
    if not args.app_dir.is_dir():
        print(f"ERROR: not a directory: {args.app_dir}", file=sys.stderr)
        print("Recovery: 1) pass applications/<id>  2) create app first", file=sys.stderr)
        return 2
    return regen(args.app_dir)


if __name__ == "__main__":
    raise SystemExit(main())
