"""S1–S4 automation for user-docs / HITL i18n (see docs/i18n/fail-tests.md)."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

CORPUS_DOCS = (
    "README.md",
    "quick-start.md",
    "web-chat.md",
    "privacy-security.md",
)
CORPUS_PROMPTS = (
    "install-full.md",
    "install-lite.md",
    "update.md",
)

EB_LOCALES = ROOT / "skills" / "evidence-bank" / "references" / "locales"
CV_LOCALES = ROOT / "skills" / "cv-creation" / "references" / "locales"
STATUS_PATH = ROOT / "docs" / "i18n" / "STATUS.md"

# Shared keys must match byte-for-byte across both skills' locale packs.
SHARED_TOP_KEYS = ("meta", "journey", "turns", "decisions")
SHARED_TURN_IDS = ("t3", "t6")
SHARED_DECISION_TURNS = ("turn3", "turn6")

_MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")
_STATUS_ROW_RE = re.compile(
    r"^\|\s*`(?P<lang>[a-z]{2})`\s*\|\s*(?P<status>[^|]+)\|",
    re.MULTILINE,
)


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(data, dict), f"{path} must be a mapping"
    return data


def _flatten_keys(obj, prefix: str = "") -> set[str]:
    keys: set[str] = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            path = f"{prefix}.{k}" if prefix else str(k)
            keys.add(path)
            keys |= _flatten_keys(v, path)
    return keys


def _current_langs_from_status() -> set[str]:
    """Languages marked current in STATUS.md (excludes en SoT pin row)."""
    text = STATUS_PATH.read_text(encoding="utf-8")
    out: set[str] = set()
    for m in _STATUS_ROW_RE.finditer(text):
        lang = m.group("lang")
        status = m.group("status").strip().lower()
        if lang == "en":
            continue
        if status.startswith("current"):
            out.add(lang)
    return out


def _is_skeleton_dir(path: Path) -> bool:
    """True if dir is missing, empty, or only .gitkeep / empty placeholders."""
    if not path.is_dir():
        return True
    entries = [p for p in path.iterdir() if p.name != ".gitkeep"]
    return len(entries) == 0


# --- S1 ------------------------------------------------------------------


def test_s1_templates_have_full_corpus():
    docs_t = ROOT / "docs" / "user" / "_template"
    prompts_t = ROOT / "prompts" / "_template"
    missing = []
    for name in CORPUS_DOCS:
        if not (docs_t / name).is_file():
            missing.append(f"docs/user/_template/{name}")
    for name in CORPUS_PROMPTS:
        if not (prompts_t / name).is_file():
            missing.append(f"prompts/_template/{name}")
    assert not missing, f"S1 template corpus missing: {missing}"


def test_s1_current_locales_have_full_corpus():
    missing = []
    for lang in sorted(_current_langs_from_status()):
        docs_dir = ROOT / "docs" / "user" / lang
        prompts_dir = ROOT / "prompts" / lang
        for name in CORPUS_DOCS:
            if not (docs_dir / name).is_file():
                missing.append(f"docs/user/{lang}/{name}")
        for name in CORPUS_PROMPTS:
            if not (prompts_dir / name).is_file():
                missing.append(f"prompts/{lang}/{name}")
    assert not missing, f"S1 current-locale corpus missing: {missing}"


def test_s1_non_skeleton_locale_dirs_are_complete_or_current_only():
    """If a lang dir has markdown (not just .gitkeep), require full corpus."""
    missing = []
    for lang_root, corpus in (
        (ROOT / "docs" / "user", CORPUS_DOCS),
        (ROOT / "prompts", CORPUS_PROMPTS),
    ):
        if not lang_root.is_dir():
            continue
        for child in sorted(lang_root.iterdir()):
            if not child.is_dir() or child.name.startswith("_"):
                continue
            if _is_skeleton_dir(child):
                continue
            for name in corpus:
                if not (child / name).is_file():
                    missing.append(f"{child.relative_to(ROOT)}/{name}")
    assert not missing, f"S1 partial locale trees: {missing}"


# --- S2 ------------------------------------------------------------------


def test_s2_relative_links_in_user_and_prompt_locale_trees():
    broken: list[str] = []
    for base in (ROOT / "docs" / "user", ROOT / "prompts"):
        if not base.is_dir():
            continue
        for md in base.rglob("*.md"):
            broken.extend(_check_relative_links_allow_skeleton_targets(md))
    assert not broken, "S2 broken relative links:\n" + "\n".join(broken)


def _check_relative_links_allow_skeleton_targets(md_path: Path) -> list[str]:
    text = md_path.read_text(encoding="utf-8")
    broken: list[str] = []
    for _label, target in _MD_LINK_RE.findall(text):
        target = target.strip()
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        path_part = target.split()[0].split("#", 1)[0]
        if not path_part:
            continue
        resolved = (md_path.parent / path_part).resolve()
        root = ROOT.resolve()
        try:
            rel = resolved.relative_to(root)
        except ValueError:
            continue
        if resolved.exists():
            continue
        # Allow missing targets under a skeleton locale dir (phase 2/3 placeholders).
        parts = rel.parts
        if len(parts) >= 3 and parts[0] == "docs" and parts[1] == "user":
            lang_dir = root / "docs" / "user" / parts[2]
            if _is_skeleton_dir(lang_dir):
                continue
        if len(parts) >= 2 and parts[0] == "prompts" and parts[1] not in (
            "_template",
            "install-full.md",
            "install-lite.md",
            "update.md",
            "adversarial-scripts-pass.md",
        ):
            lang_dir = root / "prompts" / parts[1]
            if lang_dir.is_dir() and _is_skeleton_dir(lang_dir):
                continue
        broken.append(f"{md_path.relative_to(ROOT)} → {target}")
    return broken


# --- S3 / S4 -------------------------------------------------------------


def _shared_slice(data: dict) -> dict:
    turns = data.get("turns") or {}
    decisions = data.get("decisions") or {}
    return {
        "meta": {
            "acceptance": (data.get("meta") or {}).get("acceptance"),
            "plain_label_form": (data.get("meta") or {}).get("plain_label_form"),
            "progress_form": (data.get("meta") or {}).get("progress_form"),
        },
        "journey": data.get("journey"),
        "turns": {k: turns.get(k) for k in SHARED_TURN_IDS},
        "decisions": {k: decisions.get(k) for k in SHARED_DECISION_TURNS},
    }


def test_s3_shared_keys_identical_across_skills_for_each_locale_pack():
    eb_files = {p.name: p for p in EB_LOCALES.glob("*.yaml")}
    cv_files = {p.name: p for p in CV_LOCALES.glob("*.yaml")}
    assert eb_files, "missing evidence-bank locales"
    assert cv_files, "missing cv-creation locales"
    shared_names = sorted(set(eb_files) & set(cv_files))
    assert shared_names, "no overlapping locale pack filenames"
    mismatches = []
    for name in shared_names:
        eb = _shared_slice(_load_yaml(eb_files[name]))
        cv = _shared_slice(_load_yaml(cv_files[name]))
        if eb != cv:
            mismatches.append(name)
        # Also require full shared top-level key presence
        for pack, label in ((eb_files[name], "eb"), (cv_files[name], "cv")):
            data = _load_yaml(pack)
            for key in SHARED_TOP_KEYS:
                if key not in data:
                    mismatches.append(f"{name}:{label}:missing:{key}")
    assert not mismatches, f"S3 shared-key mismatches: {mismatches}"


def test_s3_en_packs_exist_in_both_skills():
    assert (EB_LOCALES / "en.yaml").is_file()
    assert (CV_LOCALES / "en.yaml").is_file()


def test_s4_locale_packs_have_all_en_keys():
    eb_en = _load_yaml(EB_LOCALES / "en.yaml")
    cv_en = _load_yaml(CV_LOCALES / "en.yaml")
    required_eb = _flatten_keys(eb_en)
    required_cv = _flatten_keys(cv_en)
    missing = []
    for path in sorted(EB_LOCALES.glob("*.yaml")):
        if path.name == "en.yaml":
            continue
        have = _flatten_keys(_load_yaml(path))
        gap = sorted(required_eb - have)
        if gap:
            missing.append(f"evidence-bank/{path.name}: {gap}")
    for path in sorted(CV_LOCALES.glob("*.yaml")):
        if path.name == "en.yaml":
            continue
        have = _flatten_keys(_load_yaml(path))
        gap = sorted(required_cv - have)
        if gap:
            missing.append(f"cv-creation/{path.name}: {gap}")
    assert not missing, f"S4 missing keys vs en.yaml:\n" + "\n".join(missing)


def test_s4_en_packs_contain_required_turn_and_decision_keys():
    """Canonical en.yaml must include the playbook turn/decision surface."""
    for path in (EB_LOCALES / "en.yaml", CV_LOCALES / "en.yaml"):
        data = _load_yaml(path)
        turns = data.get("turns") or {}
        decisions = data.get("decisions") or {}
        for tid in ("t0", "t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8"):
            assert tid in turns, f"{path.name} missing turns.{tid}"
        for dkey in (
            "turn0",
            "turn1",
            "turn2",
            "turn3",
            "turn4",
            "turn5",
            "turn6",
            "turn7",
            "turn8",
        ):
            assert dkey in decisions, f"{path.name} missing decisions.{dkey}"
        acceptance = (data.get("meta") or {}).get("acceptance") or ""
        assert "English" in acceptance and "token" in acceptance.lower(), (
            f"{path}: meta.acceptance must state English tokens remain valid"
        )
