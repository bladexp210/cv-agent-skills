#!/usr/bin/env python3
"""Validate profile/evidence.yaml structure and referential integrity.

Hard-fail (exit 1): integrity issues (Q8).
Warn (exit 0 with WARN lines): empty bank; experience with no evidence rows.
Exit 2: file missing / unreadable.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

VALID_STATUS = frozenset({"fact", "ambiguous", "unverified", "waived"})
VALID_STRENGTH = frozenset({"weak", "moderate", "strong"})
VALID_RECENCY = frozenset({"current", "<3y", "stale"})


def load_yaml(path: Path):
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def validate(data: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    experiences = data.get("experiences") or []
    evidence = data.get("evidence") or []
    links = data.get("evidence_skills") or []

    if not experiences and not evidence and not links:
        warnings.append("empty bank (no experiences, evidence, or links)")

    exp_ids: set[str] = set()
    for exp in experiences:
        eid = exp.get("id")
        if not eid:
            errors.append("experience row missing id")
            continue
        if eid in exp_ids:
            errors.append(f"duplicate experience id {eid}")
        exp_ids.add(eid)

    ev_ids: set[str] = set()
    evidence_by_exp: dict[str, int] = {i: 0 for i in exp_ids}

    for row in evidence:
        eid = row.get("id")
        if not eid:
            errors.append("evidence row missing id")
            continue
        if eid in ev_ids:
            errors.append(f"duplicate evidence id {eid}")
        ev_ids.add(eid)

        source = row.get("source")
        if source is None or (isinstance(source, str) and not source.strip()):
            errors.append(f"{eid}: missing source")

        exp = row.get("experience_id")
        if not exp:
            errors.append(f"{eid}: missing experience_id")
        elif exp not in exp_ids:
            errors.append(f"{eid}: unknown experience_id {exp}")
        else:
            evidence_by_exp[exp] = evidence_by_exp.get(exp, 0) + 1

        status = row.get("status")
        hist = row.get("probe_history") or []
        if status is None:
            errors.append(f"{eid}: missing status")
        elif status not in VALID_STATUS:
            errors.append(f"{eid}: invalid status {status}")
        elif status == "ambiguous" and not hist:
            # Ambiguity means a probe already ran or must be recorded.
            errors.append(f"{eid}: ambiguous requires probe_history")
        elif status == "waived" and not hist:
            errors.append(f"{eid}: waived requires probe_history reason")
        # unverified may have empty probe_history while queued (Q4);
        # skill must append history before promoting to fact.

    for exp_id, count in evidence_by_exp.items():
        if count == 0:
            warnings.append(f"{exp_id}: experience has no evidence rows yet")

    for link in links:
        ev = link.get("evidence_id")
        if ev not in ev_ids:
            errors.append(f"evidence_skills: unknown evidence_id {ev}")
        sk = link.get("skill_id")
        if not sk:
            errors.append(f"evidence_skills: missing skill_id on evidence_id {ev}")
        strength = link.get("strength")
        if strength is not None and strength not in VALID_STRENGTH:
            errors.append(f"invalid strength {strength!r} on {ev}")
        recency = link.get("recency")
        if recency is not None and recency not in VALID_RECENCY:
            errors.append(f"invalid recency {recency!r} on {ev}")

    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("evidence_yaml", type=Path, help="path to evidence.yaml")
    args = p.parse_args(argv)

    if not args.evidence_yaml.is_file():
        print(f"ERROR: file not found: {args.evidence_yaml}", file=sys.stderr)
        print("Recovery: 1) create from template  2) pass correct path", file=sys.stderr)
        return 2

    try:
        errors, warnings = validate(load_yaml(args.evidence_yaml))
    except Exception as exc:  # noqa: BLE001 — surface parse errors to operator
        print(f"ERROR: failed to read YAML: {exc}", file=sys.stderr)
        print("Recovery: 1) fix YAML syntax  2) re-run validate", file=sys.stderr)
        return 2

    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print("Recovery: 1) fix listed rows  2) re-run validate", file=sys.stderr)
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
