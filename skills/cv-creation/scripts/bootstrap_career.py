#!/usr/bin/env python3
"""Bootstrap a career/ project tree from templates next to this skill."""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
ASSETS = SKILL_ROOT / "assets"


def copy_template(name: str, dest: Path) -> None:
    src = ASSETS / name
    if not src.exists():
        raise FileNotFoundError(src)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)


def bootstrap(root: Path, force: bool = False) -> None:
    root = root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    cfg = root / "career.config.yaml"
    if cfg.exists() and not force:
        print(f"Exists: {cfg} (use --force to overwrite config)")
    else:
        copy_template("career.config.template.yaml", cfg)
    profile = root / "profile"
    profile.mkdir(exist_ok=True)
    for src_name, dest_name in [
        ("identity.template.yaml", "identity.yaml"),
        ("voice.template.md", "voice.md"),
        ("export-style.template.yaml", "export-style.yaml"),
    ]:
        dest = profile / dest_name
        if dest.exists() and not force:
            print(f"Skip existing {dest}")
        else:
            copy_template(src_name, dest)
    evidence = profile / "evidence.yaml"
    if not evidence.exists() or force:
        # prefer evidence-bank template if present
        eb = SKILL_ROOT.parent / "evidence-bank" / "assets" / "evidence-record-template.yaml"
        if eb.exists():
            shutil.copy2(eb, evidence)
        else:
            evidence.write_text("experiences: []\nevidence: []\nevidence_skills: []\n", encoding="utf-8")
    skills = profile / "skills.yaml"
    if not skills.exists() or force:
        skills.write_text("skills: []\n", encoding="utf-8")
    (profile / "norms" / "ats").mkdir(parents=True, exist_ok=True)
    ats = profile / "norms" / "ats" / "generic.yaml"
    if not ats.exists() or force:
        copy_template("ats-rules.template.yaml", ats)
    (root / "applications").mkdir(exist_ok=True)
    (root / "_skill_state").mkdir(exist_ok=True)
    inbox = root / "inbox"
    for sub in ("resumes", "linkedin", "from-links"):
        (inbox / sub).mkdir(parents=True, exist_ok=True)
    inbox_readme = inbox / "README.md"
    if not inbox_readme.exists() or force:
        copy_template("inbox.README.md", inbox_readme)
    gi = root / ".gitignore"
    if not gi.exists() or force:
        copy_template("gitignore.template", gi)
    print(f"Bootstrapped career root: {root}")
    print("Inbox ready: drop CVs → inbox/resumes/; LinkedIn dumps → inbox/linkedin/; URL saves → inbox/from-links/")
    print("Empty-and-when: evidence empty→prompt at bank/composition; norms lazy; voice elicit at [6] (skippable).")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("root", type=Path, nargs="?", default=Path("."), help="career project root")
    p.add_argument("--force", action="store_true")
    args = p.parse_args(argv)
    try:
        bootstrap(args.root, force=args.force)
    except FileNotFoundError as e:
        print(f"ERROR: missing template {e}", file=sys.stderr)
        print("Recovery: 1) restore assets/  2) reinstall skill tree", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
