"""Unit tests for PDF export page-style allowlist and deny-all URL fetcher."""
from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "cv-creation" / "scripts" / "export_resume.py"
MINI = ROOT / "skills" / "cv-creation" / "assets" / "fixtures" / "mini-app"
APP_REL = Path("applications") / "acme-de-2026-01-01"


def _load_export_resume():
    spec = importlib.util.spec_from_file_location("export_resume_pdf_sec", SCRIPT)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


er = _load_export_resume()


def _ok_style(**page_overrides) -> dict:
    page = {
        "size": "A4",
        "margins": {
            "top": "20mm",
            "bottom": "20mm",
            "left": "18mm",
            "right": "18mm",
        },
    }
    page.update(page_overrides)
    return {
        "page": page,
        "layout": {
            "single_column": True,
            "tables": False,
            "text_boxes": False,
            "content_headers_footers": False,
            "real_list_styles": True,
        },
    }


@pytest.mark.parametrize("size", sorted(er.ALLOWED_PAGE_SIZES))
def test_allowed_page_sizes_pass(size: str):
    assert er.validate_page_style(_ok_style(size=size)) == []


def test_good_margins_pass():
    style = _ok_style(
        margins={
            "top": "1.5cm",
            "right": "0.5in",
            "bottom": "12pt",
            "left": "18mm",
        }
    )
    assert er.validate_page_style(style) == []


@pytest.mark.parametrize(
    "size",
    [
        "A4; } @import url(http://evil)",
        "url(http://x)",
        "a4",
        "Tabloid",
        "A4; background: red",
    ],
)
def test_injection_shaped_page_size_fails(size: str):
    errs = er.validate_page_style(_ok_style(size=size))
    assert errs
    assert any("page.size" in e for e in errs)


@pytest.mark.parametrize(
    "bad",
    [
        "20mm; }",
        "20mm; background: url(http://x)",
        "url(http://evil)",
        "20mm !important",
        "calc(1mm)",
        "20 mm",
        "-2mm",
        "",
    ],
)
def test_injection_shaped_margins_fail(bad: str):
    style = _ok_style(margins={"top": bad, "right": "18mm", "bottom": "20mm", "left": "18mm"})
    errs = er.validate_page_style(style)
    assert errs
    assert any("page.margins.top" in e for e in errs)


@pytest.mark.parametrize(
    "url",
    [
        "http://example.com/x.png",
        "https://evil.example/steal",
        "file:///etc/passwd",
        "ftp://files.example/a",
        "about:blank",
        "/relative/path.png",
    ],
)
def test_deny_fetcher_rejects_non_data_urls(url: str):
    with pytest.raises(ValueError, match="Refused to fetch"):
        er.deny_external_url_fetcher(url)


def test_main_rejects_bad_page_size_before_export(tmp_path: Path):
    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    style_path = career / "profile" / "export-style.yaml"
    style_path.write_text(
        "page:\n  size: 'A4; } @import url(http://evil)'\n"
        "  margins: { top: 20mm, bottom: 20mm, left: 18mm, right: 18mm }\n"
        "layout:\n  single_column: true\n  tables: false\n"
        "  text_boxes: false\n  content_headers_footers: false\n"
        "  real_list_styles: true\n",
        encoding="utf-8",
    )
    app_dir = career / APP_REL
    rc = er.main(
        ["--formats", "md", "--career-root", str(career), str(app_dir)]
    )
    assert rc == 3


def test_weasyprint_pdf_write_with_deny_fetcher(tmp_path: Path):
    pytest.importorskip("weasyprint")
    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    app_dir = career / APP_REL
    rc = er.main(
        [
            "--formats",
            "pdf",
            "--career-root",
            str(career),
            str(app_dir),
        ]
    )
    assert rc == 0
    assert (app_dir / "export" / "resume.pdf").is_file()


def test_pdf_main_passes_deny_url_fetcher(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    """X8: PDF path must pass a url_fetcher that refuses http (no weasyprint required)."""
    captured: dict = {}

    class FakeHTML:
        def __init__(self, string=None, url_fetcher=None, **kwargs):
            captured["url_fetcher"] = url_fetcher

        def write_pdf(self, path):
            Path(path).write_bytes(b"%PDF-fake")

    monkeypatch.setattr(er, "HAVE_WEASYPRINT", True)
    monkeypatch.setattr(er, "WeasyHTML", FakeHTML, raising=False)

    career = tmp_path / "mini-app"
    shutil.copytree(MINI, career)
    app_dir = career / APP_REL
    rc = er.main(
        ["--formats", "pdf", "--career-root", str(career), str(app_dir)]
    )
    assert rc == 0
    fetcher = captured.get("url_fetcher")
    assert fetcher is not None
    with pytest.raises(Exception):
        if callable(fetcher) and not hasattr(fetcher, "fetch"):
            fetcher("http://example.com/x.png")
        elif hasattr(fetcher, "fetch"):
            fetcher.fetch("http://example.com/x.png")
        else:
            fetcher("http://example.com/x.png")  # type: ignore[operator]
