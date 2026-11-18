#!/usr/bin/env python3
"""Validate application artifacts, export-style MUST flags, and taxonomy DAG."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

MUST = {
    "single_column": True,
    "tables": False,
    "text_boxes": False,
    "content_headers_footers": False,
    "real_list_styles": True,
}


def load_yaml(path: Path):
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def check_style(style: dict) -> list[str]:
    errors = []
    layout = style.get("layout") or {}
    for key, expected in MUST.items():
        if layout.get(key) != expected:
            errors.append(f"layout.{key} must be {expected}, got {layout.get(key)}")
    return errors


def check_taxonomy(skills_doc: dict) -> list[str]:
    errors = []
    skills = skills_doc.get("skills") or []
    ids = {s.get("id") for s in skills if s.get("id")}
    children: dict[str, list[str]] = {i: [] for i in ids}
    for s in skills:
        sid = s.get("id")
        parent = s.get("parent_id")
        if parent:
            if parent not in ids:
                errors.append(f"{sid}: unknown parent_id {parent}")
            else:
                children[parent].append(sid)
    # cycle detect
    visiting, visited = set(), set()

    def dfs(n: str) -> None:
        if n in visiting:
            errors.append(f"taxonomy cycle involving {n}")
            return
        if n in visited:
            return
        visiting.add(n)
        for c in children.get(n, []):
            dfs(c)
        visiting.remove(n)
        visited.add(n)

    for i in ids:
        dfs(i)
    return errors


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--style", type=Path, help="export-style.yaml")
    p.add_argument("--skills", type=Path, help="skills.yaml")
    p.add_argument("--composition", type=Path, help="composition.yaml")
    p.add_argument("--draft", type=Path, help="draft.md (existence check)")
    args = p.parse_args(argv)
    errors: list[str] = []
    if args.style:
        if not args.style.is_file():
            print(f"ERROR: style missing: {args.style}", file=sys.stderr)
            return 4
        errors.extend(check_style(load_yaml(args.style)))
        if any("layout." in e for e in errors):
            for e in errors:
                print(f"ERROR: {e}", file=sys.stderr)
            print("Recovery: 1) reset from export-style.template.yaml  2) fix MUST flags", file=sys.stderr)
            return 3
    if args.skills and args.skills.is_file():
        errors.extend(check_taxonomy(load_yaml(args.skills)))
    if args.composition and args.composition.is_file():
        comp = load_yaml(args.composition)
        if (comp.get("grounding") or {}).get("uncovered"):
            errors.append("grounding.uncovered must be empty at G4")
    if args.draft and not args.draft.is_file():
        errors.append(f"draft missing: {args.draft}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print("Recovery: 1) fix listed issues  2) re-run validator", file=sys.stderr)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
