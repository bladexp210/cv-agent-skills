#!/usr/bin/env python3
"""Export draft.md to md/html/docx/pdf. Pure derivation; never mutates inputs."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

try:
    import docx  # noqa: F401
    from docx import Document
    from docx.shared import Pt, Mm

    HAVE_DOCX = True
except ImportError:
    HAVE_DOCX = False

try:
    from weasyprint import HTML as WeasyHTML

    HAVE_WEASYPRINT = True
except ImportError:
    HAVE_WEASYPRINT = False

FRONTMATTER_RE = re.compile(r"^---\n.*?\n---\n", re.S)
H2_RE = re.compile(r"^##\s+(.+)$")
H3_RE = re.compile(r"^###\s+(.+)$")
BULLET_RE = re.compile(r"^[-*]\s+(.+)$")

# Page style allowlist — reject CSS injection before HTML/PDF build.
ALLOWED_PAGE_SIZES = frozenset({"A4", "Letter", "A3", "Legal"})
MARGIN_RE = re.compile(r"^\d+(\.\d+)?(mm|cm|in|pt)$")
MARGIN_SIDES = ("top", "right", "bottom", "left")


def validate_page_style(style: dict) -> list[str]:
    """Allowlist page.size and strict numeric+unit margins. Fail closed on injection shapes."""
    errs: list[str] = []
    page = style.get("page") or {}
    size = page.get("size", "A4")
    if not isinstance(size, str) or size not in ALLOWED_PAGE_SIZES:
        errs.append(
            f"page.size must be one of {sorted(ALLOWED_PAGE_SIZES)}; got {size!r}"
        )
    margins = page.get("margins") or {}
    if not isinstance(margins, dict):
        errs.append(f"page.margins must be a mapping; got {type(margins).__name__}")
        return errs
    for side in MARGIN_SIDES:
        if side not in margins:
            continue
        val = margins[side]
        if not isinstance(val, str) or not MARGIN_RE.fullmatch(val):
            errs.append(
                f"page.margins.{side} must match "
                r"^\d+(\.\d+)?(mm|cm|in|pt)$; "
                f"got {val!r}"
            )
    return errs


def deny_external_url_fetcher(url: str, *args, **kwargs):
    """WeasyPrint url_fetcher: allow only data: URIs; refuse http/https/file/network.

    Fail closed. Compatible as a plain callable for older WeasyPrint; also usable
    as the body of a custom fetcher. Unit-testable without WeasyPrint installed.
    """
    scheme = ""
    if isinstance(url, str):
        m = re.match(r"^([A-Za-z][A-Za-z0-9+.-]*):", url)
        if m:
            scheme = m.group(1).lower()
    if scheme != "data":
        raise ValueError(f"Refused to fetch URL (only data: allowed): {url}")
    # data: — delegate to WeasyPrint when present so PDF path can embed inlines.
    try:
        from weasyprint import default_url_fetcher  # type: ignore

        return default_url_fetcher(url, *args, **kwargs)
    except ImportError:
        pass
    try:
        from weasyprint.urls import URLFetcher  # type: ignore

        return URLFetcher(allowed_protocols={"data"}).fetch(url)
    except ImportError as e:
        raise ValueError("weasyprint required to decode data: URLs") from e


def _pdf_url_fetcher():
    """Prefer WeasyPrint URLFetcher(allowed_protocols={'data'}) when available."""
    try:
        from weasyprint.urls import URLFetcher  # type: ignore

        return URLFetcher(allowed_protocols={"data"})
    except ImportError:
        return deny_external_url_fetcher


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_yaml(path: Path) -> dict:
    if yaml is None:
        raise SystemExit("PyYAML required: pip install pyyaml")
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def parse_draft(text: str) -> dict:
    text = FRONTMATTER_RE.sub("", text)
    lines = text.splitlines()
    header_lines: list[str] = []
    sections: list[dict] = []
    i = 0
    while i < len(lines) and not H2_RE.match(lines[i]):
        if lines[i].strip():
            header_lines.append(lines[i].strip())
        i += 1
    current = None
    buf_para: list[str] = []
    buf_bullets: list[str] = []
    sub = None

    def flush_blocks(sec):
        nonlocal buf_para, buf_bullets, sub
        if sub is not None:
            if buf_bullets:
                sub["bullets"].extend(buf_bullets)
                buf_bullets = []
            sec["blocks"].append(sub)
            sub = None
        if buf_bullets:
            sec["blocks"].append({"type": "bullets", "items": buf_bullets})
            buf_bullets = []
        if buf_para:
            sec["blocks"].append({"type": "paragraph", "text": "\n".join(buf_para)})
            buf_para = []

    while i < len(lines):
        line = lines[i]
        m2 = H2_RE.match(line)
        m3 = H3_RE.match(line)
        mb = BULLET_RE.match(line)
        if m2:
            if current:
                flush_blocks(current)
                sections.append(current)
            current = {"heading": m2.group(1).strip(), "blocks": []}
            sub = None
        elif m3 and current is not None:
            flush_blocks(current)
            sub = {"type": "subsection", "heading": m3.group(1).strip(), "meta": {"org": "", "dates": ""}, "bullets": []}
        elif mb and current is not None:
            if buf_para:
                current["blocks"].append({"type": "paragraph", "text": "\n".join(buf_para)})
                buf_para = []
            if sub is not None:
                sub["bullets"].append(mb.group(1).strip())
            else:
                buf_bullets.append(mb.group(1).strip())
        elif current is not None:
            if line.strip() == "":
                if buf_bullets and sub is None:
                    current["blocks"].append({"type": "bullets", "items": buf_bullets})
                    buf_bullets = []
                elif buf_para:
                    current["blocks"].append({"type": "paragraph", "text": "\n".join(buf_para)})
                    buf_para = []
            else:
                if buf_bullets and sub is None:
                    current["blocks"].append({"type": "bullets", "items": buf_bullets})
                    buf_bullets = []
                buf_para.append(line.strip())
        i += 1
    if current:
        flush_blocks(current)
        sections.append(current)
    name = header_lines[0] if header_lines else ""
    return {"header": {"name": name, "contact_lines": header_lines[1:]}, "sections": sections}


def check_style_must(style: dict) -> list[str]:
    layout = style.get("layout") or {}
    must = {
        "single_column": True,
        "tables": False,
        "text_boxes": False,
        "content_headers_footers": False,
        "real_list_styles": True,
    }
    return [f"layout.{k} must be {v}" for k, v in must.items() if layout.get(k) != v]


def render_md(model: dict, identity: dict) -> str:
    name = identity.get("name") or model["header"]["name"]
    contact = identity.get("contact") or {}
    lines = [name]
    bits = [contact.get("email"), contact.get("phone"), contact.get("location")]
    lines.append(" · ".join(x for x in bits if x))
    for link in contact.get("links") or []:
        lines.append(str(link))
    lines.append("")
    for sec in model["sections"]:
        lines.append(f"## {sec['heading']}")
        lines.append("")
        for block in sec["blocks"]:
            if block["type"] == "paragraph":
                lines.append(block["text"])
                lines.append("")
            elif block["type"] == "bullets":
                for it in block["items"]:
                    lines.append(f"- {it}")
                lines.append("")
            elif block["type"] == "subsection":
                lines.append(f"### {block['heading']}")
                meta = block.get("meta") or {}
                if meta.get("org") or meta.get("dates"):
                    lines.append(f"{meta.get('org','')} — {meta.get('dates','')}".strip(" —"))
                for it in block.get("bullets") or []:
                    lines.append(f"- {it}")
                lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_html(model: dict, identity: dict, style: dict) -> str:
    md_like = render_md(model, identity)
    # minimal semantic HTML from model
    name = identity.get("name") or model["header"]["name"]
    margins = (style.get("page") or {}).get("margins") or {}
    margin_css = " ".join(margins.get(k, "20mm") for k in ("top", "right", "bottom", "left"))
    parts = [
        "<!DOCTYPE html><html><head><meta charset='utf-8'><style>",
        f"@page {{ size: {(style.get('page') or {}).get('size', 'A4')}; margin: {margin_css}; }}",
        "body { font-family: Calibri, Arial, sans-serif; font-size: 10.5pt; color: #000; }",
        "h1 { font-size: 16pt; } h2 { font-size: 12pt; } ul { list-style: disc; }",
        "</style></head><body>",
        f"<h1>{_esc(name)}</h1>",
    ]
    contact = identity.get("contact") or {}
    parts.append("<p>" + _esc(" · ".join(x for x in [contact.get("email"), contact.get("phone"), contact.get("location")] if x)) + "</p>")
    for sec in model["sections"]:
        parts.append(f"<h2>{_esc(sec['heading'])}</h2>")
        for block in sec["blocks"]:
            if block["type"] == "paragraph":
                parts.append(f"<p>{_esc(block['text'])}</p>")
            elif block["type"] == "bullets":
                parts.append("<ul>" + "".join(f"<li>{_esc(i)}</li>" for i in block["items"]) + "</ul>")
            elif block["type"] == "subsection":
                parts.append(f"<h3>{_esc(block['heading'])}</h3>")
                parts.append("<ul>" + "".join(f"<li>{_esc(i)}</li>" for i in block.get("bullets") or []) + "</ul>")
    parts.append("</body></html>")
    return "\n".join(parts)


def _esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def render_docx(model: dict, identity: dict, style: dict, path: Path) -> None:
    doc = Document()
    name = identity.get("name") or model["header"]["name"]
    doc.add_heading(name, level=0)
    contact = identity.get("contact") or {}
    doc.add_paragraph(" · ".join(x for x in [contact.get("email"), contact.get("phone"), contact.get("location")] if x))
    for sec in model["sections"]:
        doc.add_heading(sec["heading"], level=1)
        for block in sec["blocks"]:
            if block["type"] == "paragraph":
                doc.add_paragraph(block["text"])
            elif block["type"] == "bullets":
                for it in block["items"]:
                    doc.add_paragraph(it, style="List Bullet")
            elif block["type"] == "subsection":
                doc.add_heading(block["heading"], level=2)
                for it in block.get("bullets") or []:
                    doc.add_paragraph(it, style="List Bullet")
    doc.save(path)


def check_env(requested: list[str]) -> int:
    rows = [
        ("md", True, "stdlib", ""),
        ("html", True, "stdlib", ""),
        ("docx", HAVE_DOCX, _ver("docx"), "pip install python-docx"),
        ("pdf", HAVE_WEASYPRINT, _ver("weasyprint"), "pip install weasyprint"),
    ]
    print(f"{'format':<8} {'available':<10} {'version':<12} install_hint")
    missing = []
    for fmt, ok, ver, hint in rows:
        print(f"{fmt:<8} {str(ok):<10} {ver or '-':<12} {hint if not ok else ''}")
        if fmt in requested and not ok:
            missing.append(fmt)
    return 1 if missing else 0


def _ver(pkg: str) -> str:
    try:
        mod = __import__(pkg)
        return getattr(mod, "__version__", "?")
    except Exception:
        return ""


def _export_dir_confined(app_dir: Path, export_dir: Path) -> bool:
    """True if resolved export_dir stays under resolved app_dir (no symlink escape)."""
    app_r = app_dir.resolve()
    exp_r = export_dir.resolve()
    return exp_r.is_relative_to(app_r)


def _refuse_symlink_write(out: Path) -> int | None:
    """Refuse writing through a symlink (do not follow to outside). Exit 5 on refuse."""
    if out.is_symlink():
        print(f"ERROR: refuse to write through symlink: {out}", file=sys.stderr)
        print(
            "Recovery: 1) remove the symlink under export/  2) re-run export",
            file=sys.stderr,
        )
        return 5
    return None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("app_dir", type=Path, nargs="?", help="applications/<app>/ directory")
    p.add_argument("--formats", default="md,html,docx,pdf")
    p.add_argument("--check-env", action="store_true")
    p.add_argument("--career-root", type=Path, default=None, help="career root for identity/style")
    args = p.parse_args(argv)
    requested = [x.strip() for x in args.formats.split(",") if x.strip()]
    formats_explicit = any(a.startswith("--formats") for a in (argv or sys.argv[1:]))
    if args.check_env:
        return check_env(requested)

    if not args.app_dir:
        print("ERROR: app_dir required unless --check-env", file=sys.stderr)
        print("Recovery: 1) pass applications/<id>  2) --check-env", file=sys.stderr)
        return 2

    app_dir = args.app_dir.resolve()
    career = args.career_root or app_dir.parent.parent
    draft = app_dir / "draft.md"
    identity_path = career / "profile" / "identity.yaml"
    style_path = career / "profile" / "export-style.yaml"
    export_dir = app_dir / "export"

    if not identity_path.is_file():
        print(f"ERROR: identity missing: {identity_path}", file=sys.stderr)
        print("Recovery: 1) run bootstrap  2) create identity.yaml", file=sys.stderr)
        return 4

    warnings: list[str] = []
    if style_path.is_file():
        style = load_yaml(style_path)
    else:
        warnings.append("style missing; using safe defaults")
        style = {
            "page": {"size": "A4", "margins": {"top": "20mm", "bottom": "20mm", "left": "18mm", "right": "18mm"}},
            "layout": {
                "single_column": True,
                "tables": False,
                "text_boxes": False,
                "content_headers_footers": False,
                "real_list_styles": True,
            },
        }

    must_errs = check_style_must(style)
    if must_errs:
        for e in must_errs:
            print(f"ERROR: {e}", file=sys.stderr)
        print("Recovery: 1) fix style MUST flags  2) reset template", file=sys.stderr)
        return 3

    page_errs = validate_page_style(style)
    if page_errs:
        for e in page_errs:
            print(f"ERROR: {e}", file=sys.stderr)
        print(
            "Recovery: 1) fix page.size / margins  2) reset from template",
            file=sys.stderr,
        )
        return 3

    if not draft.is_file():
        print(f"ERROR: draft missing: {draft}", file=sys.stderr)
        print("Recovery: 1) run composition  2) pass correct app_dir", file=sys.stderr)
        return 2

    model = parse_draft(draft.read_text(encoding="utf-8"))
    if not model["sections"]:
        print("ERROR: draft.md has no ## sections", file=sys.stderr)
        print("Recovery: 1) re-render draft from composition  2) fix headings", file=sys.stderr)
        return 2

    identity = load_yaml(identity_path)
    if not identity:
        print(f"ERROR: identity missing or empty: {identity_path}", file=sys.stderr)
        print("Recovery: 1) run bootstrap  2) create identity.yaml", file=sys.stderr)
        return 4

    try:
        export_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"ERROR: cannot write export dir {export_dir}: {e}", file=sys.stderr)
        print("Recovery: 1) fix permissions  2) choose writable path", file=sys.stderr)
        return 5

    export_dir = export_dir.resolve()
    if not _export_dir_confined(app_dir, export_dir):
        print(
            f"ERROR: export dir escapes app_dir (symlink?): {export_dir}",
            file=sys.stderr,
        )
        print(
            "Recovery: 1) remove export/ symlink  2) use a real dir under app_dir",
            file=sys.stderr,
        )
        return 5

    produced, skipped, outputs = [], [], []
    for fmt in requested:
        if fmt == "md":
            out = export_dir / "resume.md"
            bad = _refuse_symlink_write(out)
            if bad is not None:
                return bad
            out.write_text(render_md(model, identity), encoding="utf-8")
            produced.append(fmt)
            outputs.append({"format": fmt, "path": str(out.relative_to(app_dir)), "sha256": sha256_file(out), "bytes": out.stat().st_size})
        elif fmt == "html":
            out = export_dir / "resume.html"
            bad = _refuse_symlink_write(out)
            if bad is not None:
                return bad
            out.write_text(render_html(model, identity, style), encoding="utf-8")
            produced.append(fmt)
            outputs.append({"format": fmt, "path": str(out.relative_to(app_dir)), "sha256": sha256_file(out), "bytes": out.stat().st_size})
        elif fmt == "docx":
            if not HAVE_DOCX:
                if not formats_explicit:
                    skipped.append(fmt)
                    print("warn: python-docx missing; skipping docx", file=sys.stderr)
                else:
                    print("ERROR: docx requested but python-docx missing. pip install python-docx", file=sys.stderr)
                    return 1
            else:
                out = export_dir / "resume.docx"
                bad = _refuse_symlink_write(out)
                if bad is not None:
                    return bad
                render_docx(model, identity, style, out)
                produced.append(fmt)
                outputs.append({"format": fmt, "path": str(out.relative_to(app_dir)), "sha256": sha256_file(out)})
        elif fmt == "pdf":
            if not HAVE_WEASYPRINT:
                if not formats_explicit:
                    skipped.append(fmt)
                    print("warn: weasyprint missing; skipping pdf", file=sys.stderr)
                else:
                    print("ERROR: pdf requested but weasyprint missing. pip install weasyprint", file=sys.stderr)
                    return 1
            else:
                html = render_html(model, identity, style)
                out = export_dir / "resume.pdf"
                bad = _refuse_symlink_write(out)
                if bad is not None:
                    return bad
                WeasyHTML(string=html, url_fetcher=_pdf_url_fetcher()).write_pdf(out)
                produced.append(fmt)
                outputs.append({"format": fmt, "path": str(out.relative_to(app_dir)), "sha256": sha256_file(out)})
        else:
            print(f"ERROR: unknown format {fmt}", file=sys.stderr)
            return 1

    manifest = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "application_id": app_dir.name,
        "inputs": {
            "draft_md": {"path": str(draft), "sha256": sha256_file(draft)},
            "identity_yaml": {"path": str(identity_path), "sha256": sha256_file(identity_path)},
            "export_style": {"path": str(style_path) if style_path.is_file() else None, "sha256": sha256_file(style_path) if style_path.is_file() else None},
        },
        "tool": {
            "python": ".".join(map(str, sys.version_info[:3])),
            "python_docx": _ver("docx") if HAVE_DOCX else None,
            "weasyprint": _ver("weasyprint") if HAVE_WEASYPRINT else None,
        },
        "requested_formats": requested,
        "produced_formats": produced,
        "skipped_formats": skipped,
        "outputs": outputs,
        "warnings": warnings,
    }
    man_path = export_dir / "export_manifest.yaml"
    bad = _refuse_symlink_write(man_path)
    if bad is not None:
        return bad
    if yaml:
        man_path.write_text(yaml.safe_dump(manifest, sort_keys=False), encoding="utf-8")
    else:
        man_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {len(produced)} format(s) to {export_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
