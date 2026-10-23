"""Offline coverage for the pdf-to-markdown converter .

Every fixture PDF is generated at test time with ``reportlab`` (a test-only
dependency, see the Tests section of ../SKILL.md) rather
than committed as a binary file, so the suite has no checked-in PDFs to keep
in sync with the converter.

Coverage matches the issue's acceptance criteria: CLI validation (missing
file, non-PDF content, malformed PDF, encrypted PDF, missing optional
dependency), output naming, overwrite protection, Unicode handling, and
representative extraction behavior (headings, paragraphs, lists, links,
tables, multi-column reading order, images, scanned-page detection).
"""

from __future__ import annotations

import json
import unicodedata
from pathlib import Path

import pytest
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

import pdf_to_markdown as m

# ---------------------------------------------------------------------------
# Fixture PDF generators
# ---------------------------------------------------------------------------


def _simple_pdf(path: Path) -> None:
    """Heading + two-line paragraph + a link + a small table, one page."""
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(1 * inch, 10 * inch, "Heading One")
    c.setFont("Helvetica", 11)
    c.drawString(1 * inch, 9.5 * inch, "This is a paragraph of body text for the probe document.")
    c.drawString(1 * inch, 9.2 * inch, "Second line of the same paragraph, close together.")
    c.setFillColorRGB(0, 0, 1)
    c.drawString(1 * inch, 8.7 * inch, "Anthropic website")
    c.linkURL(
        "https://www.anthropic.com", (1 * inch, 8.65 * inch, 2.5 * inch, 8.85 * inch), relative=0
    )
    c.setFillColorRGB(0, 0, 0)
    c.line(1 * inch, 8 * inch, 4 * inch, 8 * inch)
    c.line(1 * inch, 7.7 * inch, 4 * inch, 7.7 * inch)
    c.line(1 * inch, 7.4 * inch, 4 * inch, 7.4 * inch)
    c.line(1 * inch, 8 * inch, 1 * inch, 7.4 * inch)
    c.line(2.5 * inch, 8 * inch, 2.5 * inch, 7.4 * inch)
    c.line(4 * inch, 8 * inch, 4 * inch, 7.4 * inch)
    c.drawString(1.1 * inch, 7.85 * inch, "Col A")
    c.drawString(2.6 * inch, 7.85 * inch, "Col B")
    c.drawString(1.1 * inch, 7.55 * inch, "1")
    c.drawString(2.6 * inch, 7.55 * inch, "2")
    c.showPage()
    c.save()


def _columns_pdf(path: Path) -> None:
    """A clean two-column layout: 20 lines per side, wide empty gutter."""
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setFont("Helvetica", 11)
    y = 10 * inch
    for i in range(20):
        c.drawString(0.75 * inch, y, f"Left column line {i}")
        y -= 0.3 * inch
    y = 10 * inch
    for i in range(20):
        c.drawString(4.25 * inch, y, f"Right column line {i}")
        y -= 0.3 * inch
    c.showPage()
    c.save()


def _full_width_pdf(path: Path) -> None:
    """Single-column body text where every line spans nearly the full page
    width, with normal word spacing throughout (no gutter) - the case
    _detect_columns must not mistake for two columns."""
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setFont("Helvetica", 11)
    y = 10 * inch
    for i in range(8):
        filler = " ".join(["word"] * 16)
        c.drawString(0.75 * inch, y, f"Line{i} {filler} end{i}")
        y -= 0.25 * inch
    c.showPage()
    c.save()


def _list_pdf(path: Path) -> None:
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1 * inch, 10 * inch, "Shopping List")
    c.setFont("Helvetica", 11)
    y = 9.5 * inch
    for item in ["Apples", "Bread", "Cheese"]:
        c.drawString(1 * inch, y, f"• {item}")
        y -= 0.25 * inch
    y -= 0.15 * inch
    for i, item in enumerate(["Wake up", "Make coffee", "Write code"], start=1):
        c.drawString(1 * inch, y, f"{i}. {item}")
        y -= 0.25 * inch
    c.showPage()
    c.save()


def _image_pdf(path: Path, image_path: Path) -> None:
    from PIL import Image

    Image.new("RGB", (100, 60), color=(200, 30, 30)).save(image_path)
    c = canvas.Canvas(str(path), pagesize=letter)
    c.drawImage(str(image_path), 1 * inch, 9 * inch, width=1.5 * inch, height=0.9 * inch)
    c.setFont("Helvetica", 11)
    c.drawString(1 * inch, 8.5 * inch, "Caption text near the image.")
    c.showPage()
    c.save()


def _full_page_image(canvas_obj: "canvas.Canvas", image_path: Path) -> None:
    from PIL import Image

    Image.new("RGB", (800, 1000), color=(220, 220, 220)).save(image_path)
    canvas_obj.drawImage(str(image_path), 0, 0, width=letter[0], height=letter[1])


def _scanned_pdf(path: Path, image_path: Path) -> None:
    """Single page, image-only: no text layer at all."""
    c = canvas.Canvas(str(path), pagesize=letter)
    _full_page_image(c, image_path)
    c.showPage()
    c.save()


def _partial_scanned_pdf(path: Path, image_path: Path) -> None:
    """Page 1 has real text; page 2 is image-only (scanned-like)."""
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setFont("Helvetica", 11)
    c.drawString(1 * inch, 10 * inch, "This page has a normal text layer.")
    c.showPage()
    _full_page_image(c, image_path)
    c.showPage()
    c.save()


def _encrypted_pdf(path: Path) -> None:
    from reportlab.lib import pdfencrypt

    enc = pdfencrypt.StandardEncryption("userpw", ownerPassword="ownerpw", canPrint=1)
    c = canvas.Canvas(str(path), pagesize=letter, encrypt=enc)
    c.setFont("Helvetica", 11)
    c.drawString(1 * inch, 10 * inch, "Secret content")
    c.showPage()
    c.save()


def _unicode_pdf(path: Path) -> None:
    """German umlauts/eszett via reportlab's base-14 Helvetica (WinAnsi) -
    no external font file, so this fixture has no system-font dependency."""
    c = canvas.Canvas(str(path), pagesize=letter)
    c.setFont("Helvetica", 14)
    c.drawString(1 * inch, 10 * inch, "Grüße aus München: Straße, Übung, Fußgänger.")
    c.drawString(1 * inch, 9.5 * inch, "Café, naïve, Zürich – öffentliche Prüfung, façade.")
    c.showPage()
    c.save()


@pytest.fixture(scope="session")
def fixtures(tmp_path_factory: pytest.TempPathFactory) -> dict:
    d = tmp_path_factory.mktemp("pdf_fixtures")
    paths = {
        "simple": d / "simple.pdf",
        "columns": d / "columns.pdf",
        "full_width": d / "full_width.pdf",
        "list": d / "list.pdf",
        "image": d / "image.pdf",
        "scanned": d / "scanned.pdf",
        "partial_scanned": d / "partial_scanned.pdf",
        "encrypted": d / "encrypted.pdf",
        "unicode": d / "unicode.pdf",
        "malformed": d / "malformed.pdf",
        "not_a_pdf": d / "not_a_pdf.txt",
    }
    _simple_pdf(paths["simple"])
    _columns_pdf(paths["columns"])
    _full_width_pdf(paths["full_width"])
    _list_pdf(paths["list"])
    _image_pdf(paths["image"], d / "_src_image.png")
    _scanned_pdf(paths["scanned"], d / "_src_scan.png")
    _partial_scanned_pdf(paths["partial_scanned"], d / "_src_partial_scan.png")
    _encrypted_pdf(paths["encrypted"])
    _unicode_pdf(paths["unicode"])
    paths["malformed"].write_bytes(b"%PDF-1.4\nnot really a pdf body, truncated garbage")
    paths["not_a_pdf"].write_text("just some ordinary text, not a PDF at all")
    return paths


def _run(argv: list) -> int:
    return m.main([str(a) for a in argv])


def _run_json(argv: list, capsys: pytest.CaptureFixture) -> dict:
    code = _run([*argv, "--json"])
    out = json.loads(capsys.readouterr().out)
    assert out.get("exit_code", 0) == code or out.get("ok") is True
    return out


# ---------------------------------------------------------------------------
# CLI validation / exit codes
# ---------------------------------------------------------------------------


def test_missing_file_exits_file_not_found(tmp_path: Path) -> None:
    code = _run([tmp_path / "does_not_exist.pdf"])
    assert code == m.ExitCode.FILE_NOT_FOUND


def test_directory_as_input_exits_file_not_found(tmp_path: Path) -> None:
    code = _run([tmp_path])
    assert code == m.ExitCode.FILE_NOT_FOUND


def test_non_pdf_content_exits_invalid_pdf(fixtures: dict, tmp_path: Path) -> None:
    code = _run([fixtures["not_a_pdf"], "-o", tmp_path / "out.md"])
    assert code == m.ExitCode.INVALID_PDF


def test_malformed_pdf_exits_invalid_pdf(fixtures: dict, tmp_path: Path) -> None:
    code = _run([fixtures["malformed"], "-o", tmp_path / "out.md"])
    assert code == m.ExitCode.INVALID_PDF


def test_encrypted_pdf_exits_encrypted(fixtures: dict, tmp_path: Path) -> None:
    code = _run([fixtures["encrypted"], "-o", tmp_path / "out.md"])
    assert code == m.ExitCode.ENCRYPTED_PDF


def test_missing_optional_dependency_exits_missing_dependency(
    fixtures: dict, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(m, "pypdf", None)
    code = _run([fixtures["simple"], "-o", tmp_path / "out.md"])
    assert code == m.ExitCode.MISSING_DEPENDENCY


def test_usage_error_with_no_arguments_exits_2() -> None:
    with pytest.raises(SystemExit) as exc_info:
        m.main([])
    assert exc_info.value.code == 2


def test_scanned_only_pdf_exits_scanned_unsupported_and_writes_nothing(
    fixtures: dict, tmp_path: Path
) -> None:
    out = tmp_path / "scanned.md"
    code = _run([fixtures["scanned"], "-o", out])
    assert code == m.ExitCode.SCANNED_UNSUPPORTED
    assert not out.exists()


# ---------------------------------------------------------------------------
# Output naming
# ---------------------------------------------------------------------------


def test_default_output_path_is_input_stem_with_md_suffix(fixtures: dict, tmp_path: Path) -> None:
    src = tmp_path / "my-document.pdf"
    src.write_bytes(fixtures["simple"].read_bytes())
    code = _run([src])
    assert code == m.ExitCode.SUCCESS
    assert (tmp_path / "my-document.md").exists()


def test_output_directory_argument_uses_input_stem(fixtures: dict, tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    code = _run([fixtures["simple"], "-o", out_dir])
    assert code == m.ExitCode.SUCCESS
    assert (out_dir / "simple.md").exists()


def test_explicit_output_path_is_used_verbatim(fixtures: dict, tmp_path: Path) -> None:
    out = tmp_path / "nested" / "custom-name.md"
    code = _run([fixtures["simple"], "-o", out])
    assert code == m.ExitCode.SUCCESS
    assert out.exists()


# ---------------------------------------------------------------------------
# Overwrite protection
# ---------------------------------------------------------------------------


def test_existing_output_blocks_without_force(fixtures: dict, tmp_path: Path) -> None:
    out = tmp_path / "out.md"
    out.write_text("sentinel content that must survive")
    code = _run([fixtures["simple"], "-o", out])
    assert code == m.ExitCode.OUTPUT_EXISTS
    assert out.read_text() == "sentinel content that must survive"


def test_force_flag_overwrites_existing_output(fixtures: dict, tmp_path: Path) -> None:
    out = tmp_path / "out.md"
    out.write_text("sentinel content that must NOT survive")
    code = _run([fixtures["simple"], "-o", out, "--force"])
    assert code == m.ExitCode.SUCCESS
    assert "sentinel" not in out.read_text()
    assert "Heading One" in out.read_text()


def test_write_leaves_no_temp_file_behind(fixtures: dict, tmp_path: Path) -> None:
    out = tmp_path / "out.md"
    code = _run([fixtures["simple"], "-o", out])
    assert code == m.ExitCode.SUCCESS
    assert list(tmp_path.glob("*.tmp")) == []
    assert list(tmp_path.glob(".*.md.tmp")) == []


def test_write_failure_cleans_up_temp_file(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    def _boom(*_args: object, **_kwargs: object) -> None:
        raise OSError("simulated failure")

    monkeypatch.setattr(m.os, "replace", _boom)
    writer = m.MarkdownWriter()
    out = tmp_path / "out.md"
    with pytest.raises(OSError):
        writer.write("# hello\n", out)
    assert not out.exists()
    assert list(tmp_path.iterdir()) == []


# ---------------------------------------------------------------------------
# Unicode handling
# ---------------------------------------------------------------------------


def test_unicode_german_text_is_preserved_without_mojibake(fixtures: dict, tmp_path: Path) -> None:
    out = tmp_path / "unicode.md"
    code = _run([fixtures["unicode"], "-o", out])
    assert code == m.ExitCode.SUCCESS
    text = out.read_text(encoding="utf-8")
    for word in ("Grüße", "München", "Straße", "Übung", "Fußgänger", "Café", "naïve"):
        assert word in text
    assert "(cid:" not in text
    assert text == unicodedata.normalize("NFC", text)


def test_output_is_utf8_with_lf_newlines(fixtures: dict, tmp_path: Path) -> None:
    out = tmp_path / "unicode.md"
    _run([fixtures["unicode"], "-o", out])
    raw = out.read_bytes()
    assert b"\r\n" not in raw
    raw.decode("utf-8")  # raises if not valid UTF-8


# ---------------------------------------------------------------------------
# Representative extraction behavior
# ---------------------------------------------------------------------------


def test_heading_is_rendered_as_markdown_heading(fixtures: dict, tmp_path: Path) -> None:
    out = tmp_path / "out.md"
    _run([fixtures["simple"], "-o", out])
    assert "# Heading One" in out.read_text()


def test_paragraph_lines_are_joined(fixtures: dict, tmp_path: Path) -> None:
    out = tmp_path / "out.md"
    _run([fixtures["simple"], "-o", out])
    text = out.read_text()
    assert "This is a paragraph of body text for the probe document." in text
    assert "Second line of the same paragraph, close together." in text


def test_link_is_rendered_as_markdown_link(fixtures: dict, tmp_path: Path) -> None:
    out = tmp_path / "out.md"
    _run([fixtures["simple"], "-o", out])
    assert "[Anthropic website](https://www.anthropic.com)" in out.read_text()


def test_table_is_rendered_as_pipe_table(fixtures: dict, tmp_path: Path) -> None:
    out = tmp_path / "out.md"
    _run([fixtures["simple"], "-o", out])
    text = out.read_text()
    assert "| Col A | Col B |" in text
    assert "| --- | --- |" in text
    assert "| 1 | 2 |" in text


def test_unordered_and_ordered_lists_are_rendered_separately(
    fixtures: dict, tmp_path: Path
) -> None:
    out = tmp_path / "out.md"
    _run([fixtures["list"], "-o", out])
    text = out.read_text()
    assert "- Apples" in text
    assert "- Bread" in text
    assert "- Cheese" in text
    assert "1. Wake up" in text
    assert "1. Make coffee" in text
    assert "1. Write code" in text
    assert "(cid:" not in text


def test_two_column_layout_reads_left_column_fully_before_right(
    fixtures: dict, tmp_path: Path
) -> None:
    out = tmp_path / "out.md"
    _run([fixtures["columns"], "-o", out])
    text = out.read_text()
    assert "Left column line 0" in text
    assert "Right column line 0" in text
    assert text.index("Left column line 19") < text.index("Right column line 0")


def test_full_width_single_column_text_is_not_split_into_columns(
    fixtures: dict, tmp_path: Path
) -> None:
    out = tmp_path / "out.md"
    _run([fixtures["full_width"], "-o", out])
    text = out.read_text()
    assert "Line0" in text and "end0" in text and "Line1" in text
    # If _detect_columns wrongly treated this full-width single-column text
    # as two columns, "end0" (the tail of line 0) would be split into the
    # second column's bucket and emitted only after every line's start (from
    # the first column), instead of right after "Line0" itself.
    assert text.index("end0") < text.index("Line1")


def test_image_is_extracted_and_referenced(fixtures: dict, tmp_path: Path) -> None:
    out = tmp_path / "out.md"
    _run([fixtures["image"], "-o", out])
    text = out.read_text()
    assert "![" in text and "](" in text
    assets_dir = tmp_path / "out_assets"
    assert assets_dir.is_dir()
    images = list(assets_dir.iterdir())
    assert len(images) == 1
    assert images[0].read_bytes().startswith(b"\x89PNG")
    assert "out_assets/" in text


def test_no_images_flag_skips_asset_extraction(fixtures: dict, tmp_path: Path) -> None:
    out = tmp_path / "out.md"
    _run([fixtures["image"], "-o", out, "--no-images"])
    text = out.read_text()
    assert "![" not in text
    assert not (tmp_path / "out_assets").exists()
    assert "Caption text near the image." in text


def test_partial_scanned_document_succeeds_with_warning(fixtures: dict, tmp_path: Path) -> None:
    out = tmp_path / "out.md"
    code = _run([fixtures["partial_scanned"], "-o", out])
    assert code == m.ExitCode.SUCCESS
    text = out.read_text()
    assert "This page has a normal text layer." in text
    assert "> **Warning:**" in text
    assert "scanned" in text.lower()


# ---------------------------------------------------------------------------
# --diagnostics / --json
# ---------------------------------------------------------------------------


def test_diagnostics_flag_prints_stats(
    fixtures: dict, tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    out = tmp_path / "out.md"
    code = _run([fixtures["simple"], "-o", out, "--diagnostics"])
    assert code == m.ExitCode.SUCCESS
    captured = capsys.readouterr().out
    assert "Diagnostics:" in captured
    assert "headings:" in captured
    assert "tables:" in captured


def test_json_flag_emits_valid_result_object(
    fixtures: dict, tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    out = tmp_path / "out.md"
    result = _run_json([fixtures["simple"], "-o", out], capsys)
    assert result["ok"] is True
    assert result["output_path"] == str(out)
    assert result["pages"] == 1
    assert result["headings"] == 1
    assert result["tables"] == 1


def test_json_flag_emits_valid_result_object_on_error(
    fixtures: dict, tmp_path: Path, capsys: pytest.CaptureFixture
) -> None:
    code = _run([tmp_path / "missing.pdf", "--json"])
    result = json.loads(capsys.readouterr().out)
    assert result["ok"] is False
    assert result["exit_code"] == code == m.ExitCode.FILE_NOT_FOUND


# ---------------------------------------------------------------------------
# Small helper-function unit tests
# ---------------------------------------------------------------------------


def test_derive_output_path_defaults_to_input_stem(tmp_path: Path) -> None:
    assert m.derive_output_path(tmp_path / "doc.pdf", None) == tmp_path / "doc.md"


def test_derive_output_path_directory_argument(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    assert m.derive_output_path(tmp_path / "doc.pdf", out_dir) == out_dir / "doc.md"


def test_derive_output_path_explicit_file(tmp_path: Path) -> None:
    explicit = tmp_path / "renamed.md"
    assert m.derive_output_path(tmp_path / "doc.pdf", explicit) == explicit


def test_compute_heading_sizes_ranks_larger_sizes_first() -> None:
    sizes = m._compute_heading_sizes({11.0: 500, 20.0: 20, 16.0: 40})
    assert sizes == {20.0: 1, 16.0: 2}


def test_compute_heading_sizes_empty_input() -> None:
    assert m._compute_heading_sizes({}) == {}


def test_normalize_words_replaces_cid_placeholder() -> None:
    words = [{"text": "(cid:127)"}, {"text": "normal"}, {"text": "mixed(cid:9)text"}]
    m._normalize_words(words)
    assert words[0]["text"] == "�"
    assert words[1]["text"] == "normal"
    assert words[2]["text"] == "mixed�text"
