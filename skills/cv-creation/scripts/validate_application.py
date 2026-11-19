#!/usr/bin/env python3
"""Validate application artifacts, export-style MUST flags, taxonomy DAG, and G4 grounding."""
from __future__ import annotations

import argparse
import re
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

SUMMARY_EXPERIENCE = frozenset({"summary", "experience"})
EDU_CERT = frozenset(
    {
        "education",
        "certification",
        "certifications",
        "certs",
        "certificate",
        "certificates",
    }
)
STRENGTH_RANK = {"weak": 1, "moderate": 2, "strong": 3}
ACTION_STRENGTH_FLOOR = {"core": "strong", "use": "moderate"}
SKILLS_LINE_ACTIONS = frozenset({"core", "use", "mention"})
_WS = re.compile(r"\s+")


def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise TypeError(
            f"expected mapping at root of {path}, got {type(data).__name__}"
        )
    return data


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


def _norm_ws(text: str) -> str:
    return _WS.sub(" ", (text or "").strip())


_PROBE_REASON_KEYS = ("reason", "answer", "note", "summary", "text")


def _nonempty_str(val) -> bool:
    return val is not None and bool(str(val).strip())


def _waived_has_reason(row: dict) -> bool:
    if _nonempty_str(row.get("reason")):
        return True
    if _nonempty_str(row.get("waiver_reason")):
        return True
    hist = row.get("probe_history") or []
    if not isinstance(hist, list):
        return False
    for entry in hist:
        if isinstance(entry, str) and entry.strip():
            return True
        if isinstance(entry, dict):
            for key in _PROBE_REASON_KEYS:
                if _nonempty_str(entry.get(key)):
                    return True
    return False


def _section_source_identity(comp: dict, section: str) -> bool:
    for entry in comp.get("section_plan") or []:
        if entry.get("id") == section and entry.get("source") == "identity":
            return True
    return False


def _bullet_identity_exempt(bullet: dict, comp: dict, *, identity_enabled: bool) -> bool:
    """Edu/cert bullets are exempt only when --identity is provided and sourced from identity."""
    if not identity_enabled:
        return False
    section = (bullet.get("section") or "").lower()
    if section not in EDU_CERT:
        return False
    if bullet.get("source") == "identity":
        return True
    return _section_source_identity(comp, section)


def _build_skill_name_index(skills_doc: dict) -> dict[str, str]:
    """Map lowercase display forms → skill id."""
    index: dict[str, str] = {}
    for s in skills_doc.get("skills") or []:
        sid = s.get("id")
        if not sid:
            continue
        forms: list[str] = []
        if s.get("canonical_name"):
            forms.append(str(s["canonical_name"]))
        for form in s.get("ats_forms") or []:
            forms.append(str(form))
        for form in s.get("aliases") or []:
            forms.append(str(form))
        for form in forms:
            key = form.strip().lower()
            if key:
                index[key] = sid
    return index


def _matching_by_skill(matching_doc: dict) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for row in matching_doc.get("matching") or []:
        sid = row.get("skill_id")
        if sid:
            out[sid] = row
    return out


def _evidence_indexes(
    evidence_doc: dict,
) -> tuple[dict[str, dict], dict[str, dict[str, str]], list[str]]:
    """Return (ev_id → row, ev_id → {skill_id → strength}, index errors)."""
    errors: list[str] = []
    by_id: dict[str, dict] = {}
    seen_ids: set[str] = set()
    for row in evidence_doc.get("evidence") or []:
        eid = row.get("id")
        if not eid:
            continue
        if eid in seen_ids:
            errors.append(f"duplicate evidence id {eid}")
        else:
            seen_ids.add(eid)
        by_id[eid] = row
    links: dict[str, dict[str, str]] = {eid: {} for eid in by_id}
    seen_links: set[tuple[str, str]] = set()
    for link in evidence_doc.get("evidence_skills") or []:
        eid = link.get("evidence_id")
        sid = link.get("skill_id")
        if not eid or not sid:
            continue
        if eid not in by_id:
            errors.append(f"evidence_skills: unknown evidence_id {eid}")
            continue
        key = (eid, sid)
        if key in seen_links:
            errors.append(f"duplicate evidence_skills link ({eid}, {sid})")
        else:
            seen_links.add(key)
        links.setdefault(eid, {})[sid] = link.get("strength") or ""
    return by_id, links, errors


def check_grounding(
    comp: dict,
    evidence_doc: dict,
    *,
    matching_doc: dict | None = None,
    skills_doc: dict | None = None,
    draft_text: str | None = None,
    identity_enabled: bool = False,
) -> list[str]:
    """G4 structural checks 1–7 + cited_ev_ids integrity + optional draft substring."""
    errors: list[str] = []
    grounding = comp.get("grounding") or {}
    uncovered = grounding.get("uncovered")
    if uncovered:
        errors.append("grounding.uncovered must be empty at G4")

    ev_by_id, ev_skill_links, index_errors = _evidence_indexes(evidence_doc)
    errors.extend(index_errors)
    cited_list = list(grounding.get("cited_ev_ids") or [])
    cited_set = set(cited_list)

    for eid in cited_list:
        if eid not in ev_by_id:
            errors.append(f"grounding.cited_ev_ids: unknown evidence id {eid}")

    match_by_skill = _matching_by_skill(matching_doc) if matching_doc is not None else {}
    name_index = _build_skill_name_index(skills_doc) if skills_doc is not None else {}

    bullets_raw = comp.get("bullets")
    if not bullets_raw:
        errors.append("composition has no bullets")
        bullets: list = []
    elif not isinstance(bullets_raw, list):
        errors.append("composition has no bullets")
        bullets = []
    else:
        bullets = bullets_raw

    for bullet in bullets:
        bid = bullet.get("id") or "<bullet>"
        section = (bullet.get("section") or "").lower()
        identity_exempt = _bullet_identity_exempt(
            bullet, comp, identity_enabled=identity_enabled
        )

        if identity_exempt:
            continue

        text = bullet.get("text")
        if not _nonempty_str(text):
            errors.append(f"{bid}: missing or empty bullet text")

        # Summary/Experience always; edu/cert when not identity-exempt;
        # other sections only if they cite evidence.
        if section in SUMMARY_EXPERIENCE or section in EDU_CERT:
            needs_ev = True
        elif section:
            needs_ev = bool(bullet.get("ev_ids"))
        else:
            needs_ev = True

        if not needs_ev:
            continue

        ev_ids = list(bullet.get("ev_ids") or [])
        if len(ev_ids) < 1:
            errors.append(f"{bid}: ev_ids length must be ≥ 1")
            continue

        for eid in ev_ids:
            if eid not in ev_by_id:
                errors.append(f"{bid}: unknown evidence id {eid}")
                continue
            if eid not in cited_set:
                errors.append(f"{bid}: cites {eid} not listed in grounding.cited_ev_ids")
            row = ev_by_id[eid]
            status = row.get("status")
            if status == "fact":
                pass
            elif status == "waived":
                if not _waived_has_reason(row):
                    errors.append(f"{bid}: cited {eid} is waived without recorded reason")
            else:
                errors.append(f"{bid}: cited {eid} status must be fact or waived, got {status}")

        skill_ids = bullet.get("skill_ids")
        if skill_ids is None:
            errors.append(f"{bid}: missing skill_ids[]")
            skill_ids = []
        elif not isinstance(skill_ids, list):
            errors.append(f"{bid}: skill_ids must be a list")
            skill_ids = []
        elif len(skill_ids) < 1 and section in SUMMARY_EXPERIENCE:
            errors.append(f"{bid}: skill_ids[] must be non-empty")

        union_skills: dict[str, str] = {}
        for eid in ev_ids:
            for sid, strength in ev_skill_links.get(eid, {}).items():
                prev = union_skills.get(sid)
                if prev is None or STRENGTH_RANK.get(strength, 0) > STRENGTH_RANK.get(prev, 0):
                    union_skills[sid] = strength

        for sid in skill_ids:
            if sid not in union_skills:
                errors.append(
                    f"{bid}: skill_id {sid} not linked via evidence_skills for cited evidence"
                )
                continue
            if matching_doc is not None:
                action = (match_by_skill.get(sid) or {}).get("action")
                floor = ACTION_STRENGTH_FLOOR.get(action) if action else None
                if floor:
                    got = union_skills.get(sid) or ""
                    if STRENGTH_RANK.get(got, 0) < STRENGTH_RANK.get(floor, 0):
                        errors.append(
                            f"{bid}: skill_id {sid} action {action} needs ≥{floor} evidence link, got {got or 'none'}"
                        )

    if matching_doc is not None and skills_doc is not None:
        allowed = {
            sid
            for sid, row in match_by_skill.items()
            if row.get("action") in SKILLS_LINE_ACTIONS
        }
        for group in comp.get("skills_line") or []:
            gname = group.get("group") or "<group>"
            for item in group.get("items") or []:
                key = str(item).strip().lower()
                sid = name_index.get(key)
                if not sid:
                    errors.append(f"skills_line {gname}: unresolved item {item!r}")
                elif sid not in allowed:
                    errors.append(
                        f"skills_line {gname}: {item!r} → {sid} not in matching as core|use|mention"
                    )

    if draft_text is not None:
        draft_norm = _norm_ws(draft_text)
        for bullet in bullets:
            if _bullet_identity_exempt(bullet, comp, identity_enabled=identity_enabled):
                continue
            text = bullet.get("text")
            if not _nonempty_str(text):
                bid = bullet.get("id") or "<bullet>"
                if f"{bid}: missing or empty bullet text" not in errors:
                    errors.append(f"{bid}: missing or empty bullet text")
                continue
            if _norm_ws(str(text)) not in draft_norm:
                bid = bullet.get("id") or "<bullet>"
                errors.append(f"{bid}: bullet text not found as substring of draft.md")

    return errors


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--style", type=Path, help="export-style.yaml")
    p.add_argument("--skills", type=Path, help="skills.yaml")
    p.add_argument("--composition", type=Path, help="composition.yaml")
    p.add_argument("--draft", type=Path, help="draft.md (existence + optional substring check)")
    p.add_argument("--evidence", type=Path, help="evidence.yaml (required with --composition for G4)")
    p.add_argument("--matching", type=Path, help="matching.yaml (skills-line + strength floors)")
    p.add_argument("--identity", type=Path, help="identity.yaml (edu/cert identity exemption)")
    args = p.parse_args(argv)
    try:
        return _run(args)
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001 — mirror validate_evidence; no traceback
        print(f"ERROR: {exc}", file=sys.stderr)
        print(
            "Recovery: 1) fix YAML syntax, permissions, or encoding  2) re-run validator",
            file=sys.stderr,
        )
        return 2


def _run(args: argparse.Namespace) -> int:
    errors: list[str] = []
    if args.style:
        if not args.style.is_file():
            print(f"ERROR: style missing: {args.style}", file=sys.stderr)
            return 4
        errors.extend(check_style(load_yaml(args.style)))
        if any("layout." in e for e in errors):
            for e in errors:
                print(f"ERROR: {e}", file=sys.stderr)
            print(
                "Recovery: 1) reset from export-style.template.yaml  2) fix MUST flags",
                file=sys.stderr,
            )
            return 3
    skills_doc = None
    if args.skills:
        if not args.skills.is_file():
            errors.append(f"skills missing: {args.skills}")
        else:
            skills_doc = load_yaml(args.skills)
            errors.extend(check_taxonomy(skills_doc))

    if args.composition:
        if not args.composition.is_file():
            errors.append(f"composition missing: {args.composition}")
        elif not args.evidence:
            errors.append("--evidence is required when --composition is set (G4 grounding)")
        elif not args.evidence.is_file():
            errors.append(f"evidence missing: {args.evidence}")
        else:
            comp = load_yaml(args.composition)
            evidence_doc = load_yaml(args.evidence)
            matching_doc = None
            if args.matching:
                if not args.matching.is_file():
                    errors.append(f"matching missing: {args.matching}")
                else:
                    matching_doc = load_yaml(args.matching)
            identity_enabled = False
            if args.identity:
                if not args.identity.is_file():
                    errors.append(f"identity missing: {args.identity}")
                else:
                    identity_doc = load_yaml(args.identity)
                    if not identity_doc:
                        errors.append("identity empty or unreadable")
                    else:
                        identity_enabled = True
            draft_text = None
            if args.draft:
                if not args.draft.is_file():
                    errors.append(f"draft missing: {args.draft}")
                else:
                    draft_text = args.draft.read_text(encoding="utf-8")
            errors.extend(
                check_grounding(
                    comp,
                    evidence_doc,
                    matching_doc=matching_doc,
                    skills_doc=skills_doc,
                    draft_text=draft_text,
                    identity_enabled=identity_enabled,
                )
            )
    elif args.draft and not args.draft.is_file():
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
