#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pypdf>=5.0", "pdfplumber>=0.11"]
# ///
"""Convert a born-digital PDF into a single deterministic Markdown file.

Local, script-powered, no hosted AI: text extraction and layout heuristics
only. Built on the permissive-license stack (`pypdf` + `pdfplumber`) rather
than PyMuPDF/pymupdf4llm, which is AGPL-3.0-or-commercial - see
../SKILL.md ("Library choice and licensing") for the tradeoff record.

Preserves, where the source PDF makes it technically possible: reading
order (including simple two-column layouts), headings, paragraphs, lists,
links, tables, and embedded images (as extracted asset files). Scanned /
image-only pages are detected and reported rather than silently producing
low-quality output - see SCANNED_UNSUPPORTED below.

Usage:
    uv run .claude/skills/toolkit/pdf-to-markdown/scripts/pdf_to_markdown.py document.pdf
    ... document.pdf -o out.md
    ... document.pdf --force
    ... document.pdf --no-images
    ... document.pdf --diagnostics
    ... document.pdf --json

Exit codes (see ExitCode below): 0 success, 1 unexpected error, 2 usage
error, 3 file not found, 4 invalid/non-PDF input, 5 encrypted PDF,
6 missing optional dependency, 7 extraction failed, 8 output already
exists (without --force), 9 scanned/image-only PDF (nothing extractable).
"""

from __future__ import annotations

import argparse
import contextlib
import json
import logging
import os
import re
import sys
import tempfile
import unicodedata
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

# pypdf/pdfminer log parser warnings (e.g. "EOF marker not found") through the
# stdlib logging module. This script reports the same information as a single
# clear [ERROR]/exit-code pair instead, so the underlying parser noise is
# suppressed rather than left to clutter stderr or a --json run.
logging.getLogger("pypdf").setLevel(logging.ERROR)
logging.getLogger("pdfminer").setLevel(logging.ERROR)

try:
    import pypdf
    from pypdf.errors import PyPdfError
except ImportError:  # pragma: no cover - exercised via require_dependencies()
    pypdf = None  # type: ignore[assignment]
    PyPdfError = Exception  # type: ignore[assignment,misc]

try:
    import pdfplumber
except ImportError:  # pragma: no cover - exercised via require_dependencies()
    pdfplumber = None  # type: ignore[assignment]

PDF_MAGIC = b"%PDF-"
# � (the Unicode replacement character) stands in for pdfminer's "(cid:N)"
# placeholders after _normalize_words() runs - see there for why. Symbol/bullet
# glyphs in non-embedded fonts commonly have no ToUnicode mapping and decode to
# exactly this, so both the literal bullet glyphs and the replacement character
# are recognized as list markers.
LIST_UNORDERED_LINE_RE = re.compile(r"^[••●‣⁃\-\*�]\s+\S.*$")
LIST_ORDERED_LINE_RE = re.compile(r"^(\d{1,3}|[a-zA-Z]|[ivxlcdmIVXLCDM]{1,6})[.)]\s+\S.*$")
LIST_UNORDERED_MARKER_RE = re.compile(r"^[••●‣⁃\-\*�]$")
LIST_ORDERED_MARKER_RE = re.compile(r"^(\d{1,3}|[a-zA-Z]|[ivxlcdmIVXLCDM]{1,6})[.)]$")
CID_PLACEHOLDER_RE = re.compile(r"\(cid:\d+\)")


class ExitCode(IntEnum):
    SUCCESS = 0
    UNEXPECTED_ERROR = 1
    USAGE_ERROR = 2
    FILE_NOT_FOUND = 3
    INVALID_PDF = 4
    ENCRYPTED_PDF = 5
    MISSING_DEPENDENCY = 6
    EXTRACTION_FAILED = 7
    OUTPUT_EXISTS = 8
    SCANNED_UNSUPPORTED = 9


class PdfToMarkdownError(Exception):
    """Carries the exit code a CLI failure should map to."""

    def __init__(self, message: str, exit_code: ExitCode) -> None:
        super().__init__(message)
        self.exit_code = exit_code


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class TextRun:
    text: str
    link_uri: Optional[str] = None


@dataclass
class Block:
    kind: str  # "heading" | "paragraph" | "list_item" | "table" | "image"
    runs: List[TextRun] = field(default_factory=list)
    level: int = 0
    ordered: bool = False
    rows: List[List[Optional[str]]] = field(default_factory=list)
    image_path: Optional[str] = None


@dataclass
class PageResult:
    number: int
    blocks: List[Block] = field(default_factory=list)
    char_count: int = 0
    image_count: int = 0
    likely_scanned: bool = False


@dataclass
class PdfInspection:
    page_count: int
    title: Optional[str]


@dataclass
class ExtractionResult:
    title: Optional[str]
    pages: List[PageResult] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    images_written: int = 0

    @property
    def total_chars(self) -> int:
        return sum(p.char_count for p in self.pages)

    @property
    def total_images(self) -> int:
        return sum(p.image_count for p in self.pages)

    @property
    def scanned_pages(self) -> List[int]:
        return [p.number for p in self.pages if p.likely_scanned]


# ---------------------------------------------------------------------------
# Extractor interface - separates PDF parsing from CLI/workflow orchestration.
# A future adapter (PyMuPDF, Docling, Marker, local OCR, ...) can implement
# this same interface without changing the CLI contract; see SKILL.md's
# "Deferred scope" section.
# ---------------------------------------------------------------------------


class PdfExtractor(ABC):
    @abstractmethod
    def inspect(self, pdf_path: Path) -> PdfInspection:
        """Cheap pre-flight: page count, title, encryption check. Raises
        PdfToMarkdownError(ENCRYPTED_PDF | INVALID_PDF) on unsupported input."""

    @abstractmethod
    def extract(
        self,
        pdf_path: Path,
        *,
        want_images: bool,
        assets_dir: Path,
        title: Optional[str],
    ) -> ExtractionResult:
        """Full structured extraction, in reading order."""


def require_dependencies() -> None:
    missing = [name for name, mod in (("pypdf", pypdf), ("pdfplumber", pdfplumber)) if mod is None]
    if missing:
        raise PdfToMarkdownError(
            "Missing optional PDF dependencies: "
            + ", ".join(missing)
            + ". Install them with: uv sync --extra pdf",
            ExitCode.MISSING_DEPENDENCY,
        )


class PdfPlumberExtractor(PdfExtractor):
    """MVP adapter: pypdf for inspection/encryption/images, pdfplumber
    (pdfminer.six under the hood) for layout-aware text, tables, and links."""

    def inspect(self, pdf_path: Path) -> PdfInspection:
        try:
            reader = pypdf.PdfReader(str(pdf_path))
        except Exception as exc:
            raise PdfToMarkdownError(
                f"Could not open '{pdf_path.name}' as a PDF: {exc}", ExitCode.INVALID_PDF
            ) from exc

        if reader.is_encrypted:
            raise PdfToMarkdownError(
                f"'{pdf_path.name}' is password-protected/encrypted; "
                "encrypted PDFs are not supported.",
                ExitCode.ENCRYPTED_PDF,
            )

        try:
            page_count = len(reader.pages)
        except PyPdfError as exc:
            raise PdfToMarkdownError(
                f"Could not read pages of '{pdf_path.name}': {exc}", ExitCode.INVALID_PDF
            ) from exc

        title = None
        if reader.metadata is not None:
            title = getattr(reader.metadata, "title", None) or None

        return PdfInspection(page_count=page_count, title=title)

    def extract(
        self,
        pdf_path: Path,
        *,
        want_images: bool,
        assets_dir: Path,
        title: Optional[str],
    ) -> ExtractionResult:
        pdf_images_by_page: List[list] = []
        if want_images:
            reader = pypdf.PdfReader(str(pdf_path))
            pdf_images_by_page = [list(page.images) for page in reader.pages]

        pages: List[PageResult] = []
        images_written = 0

        with pdfplumber.open(str(pdf_path)) as pdf:
            page_words: List[List[dict]] = []
            size_counts: Dict[float, int] = {}
            for page in pdf.pages:
                words = page.extract_words(
                    use_text_flow=False, keep_blank_chars=False, extra_attrs=["size", "fontname"]
                )
                _normalize_words(words)
                page_words.append(words)
                for w in words:
                    size = round(w["size"], 1)
                    size_counts[size] = size_counts.get(size, 0) + len(w["text"])

            heading_sizes = _compute_heading_sizes(size_counts)

            for index, page in enumerate(pdf.pages):
                pdf_images = pdf_images_by_page[index] if index < len(pdf_images_by_page) else []
                page_result, written = _build_page(
                    page=page,
                    page_number=index + 1,
                    words=page_words[index],
                    heading_sizes=heading_sizes,
                    want_images=want_images,
                    assets_dir=assets_dir,
                    pdf_images=pdf_images,
                )
                images_written += written
                pages.append(page_result)

        warnings: List[str] = []
        scanned = [p.number for p in pages if p.likely_scanned]
        if scanned and len(scanned) < len(pages):
            nums = ", ".join(str(n) for n in scanned)
            warnings.append(
                f"Page(s) {nums} appear to be scanned/image-only; their text could not be "
                "extracted (OCR is out of scope for this script)."
            )

        return ExtractionResult(
            title=title, pages=pages, warnings=warnings, images_written=images_written
        )


# ---------------------------------------------------------------------------
# Per-page layout heuristics
# ---------------------------------------------------------------------------


def _normalize_words(words: List[dict]) -> None:
    """Replace pdfminer's "(cid:N)" placeholders with U+FFFD in place.

    A glyph with no ToUnicode CMap entry - common for bullet/symbol glyphs in
    non-embedded fonts - decodes to a "(cid:N)" debug token rather than real
    text. Surfacing that token verbatim would be its own kind of mojibake, so
    it is normalized to the standard replacement character instead: visible
    and honest about the data loss, without leaking extraction internals."""
    for w in words:
        text = w["text"]
        if "(cid:" in text:
            w["text"] = CID_PLACEHOLDER_RE.sub("�", text)


def _compute_heading_sizes(size_counts: Dict[float, int]) -> Dict[float, int]:
    """Map font sizes larger than the document's body-text size to heading
    levels 1..6, largest first. Body size = the size with the most rendered
    characters (a robust proxy for "normal paragraph text")."""
    if not size_counts:
        return {}
    body_size = max(size_counts.items(), key=lambda kv: kv[1])[0]
    larger = sorted((s for s in size_counts if s > body_size * 1.05), reverse=True)
    return {size: level for level, size in enumerate(larger[:6], start=1)}


def _crosses_gutter_continuously(
    line_words: List[dict], gutter_low: float, gutter_high: float, gap_threshold: float
) -> bool:
    """True when a line's words flow across the midline with normal
    inter-word spacing - a real single-column line. False when there's an
    abnormally large gap overlapping the [gutter_low, gutter_high] band: that
    means two separate column lines were merged into one "line" by
    y-proximity alone (common when two columns share a baseline), not one
    continuous line. The gap only needs to *overlap* the band, not straddle
    an exact midpoint - a column can start exactly at the midline."""
    ordered = sorted(line_words, key=lambda w: w["x0"])
    return all(
        not (
            (b["x0"] - a["x1"]) > gap_threshold and a["x1"] <= gutter_high and b["x0"] >= gutter_low
        )
        for a, b in zip(ordered, ordered[1:])
    )


def _detect_columns(words: List[dict], page_width: float) -> List[Tuple[float, float]]:
    """Return column x-bands: either one full-width band, or two side-by-side
    bands when the page looks like a common two-column layout.

    A per-word left/right/crossing tally alone is not enough: justified
    single-column text also splits roughly 50/50 across the page midline,
    with very few individual words straddling it (a word rarely spans the
    gutter). The distinguishing signal is per LINE, not per word - in a real
    two-column layout almost no line's text runs from the left half into the
    right half, whereas single-column lines routinely do. So a line-based
    "wide line" check gates the word-based left/right split below - but a
    "line" here is grouped by y-proximity alone, before columns are known, so
    two column-lines that happen to share a baseline can merge into one
    y-band. _crosses_gutter_continuously tells that apart from a real wide
    line by looking for the large gap a genuine gutter leaves behind."""
    if not words or page_width <= 0:
        return [(0.0, page_width)]
    lines = _group_lines(words)
    if len(lines) < 4:
        return [(0.0, page_width)]
    mid = page_width / 2
    margin = page_width * 0.04
    gutter_gap_threshold = page_width * 0.06
    wide_lines = sum(
        1
        for ln in lines
        if min(w["x0"] for w in ln) < mid - margin
        and max(w["x1"] for w in ln) > mid + margin
        and _crosses_gutter_continuously(ln, mid - margin, mid + margin, gutter_gap_threshold)
    )
    if wide_lines > len(lines) * 0.15:
        return [(0.0, page_width)]
    left = [w for w in words if w["x1"] <= mid]
    right = [w for w in words if w["x0"] >= mid]
    crossing = [w for w in words if w["x0"] < mid < w["x1"]]
    total = len(words)
    if (
        total >= 20
        and len(left) >= total * 0.25
        and len(right) >= total * 0.25
        and len(crossing) <= total * 0.05
    ):
        return [(0.0, mid), (mid, page_width)]
    return [(0.0, page_width)]


def _assign_column(x0: float, x1: float, columns: List[Tuple[float, float]]) -> int:
    cx = (x0 + x1) / 2
    for i, (a, b) in enumerate(columns):
        if a <= cx < b:
            return i
    return len(columns) - 1


def _group_lines(words: List[dict]) -> List[List[dict]]:
    ordered = sorted(words, key=lambda w: (round(w["top"], 1), w["x0"]))
    lines: List[List[dict]] = []
    current: List[dict] = []
    current_top: Optional[float] = None
    for w in ordered:
        tolerance = max(2.0, w.get("height", 10.0) * 0.35)
        if current and current_top is not None and abs(w["top"] - current_top) > tolerance:
            current.sort(key=lambda x: x["x0"])
            lines.append(current)
            current = []
            current_top = None
        current.append(w)
        current_top = w["top"] if current_top is None else min(current_top, w["top"])
    if current:
        current.sort(key=lambda x: x["x0"])
        lines.append(current)
    lines.sort(key=lambda ln: min(w["top"] for w in ln))
    return lines


def _dominant_size(line_words: List[dict]) -> float:
    counts: Dict[float, int] = {}
    for w in line_words:
        size = round(w.get("size", 0.0), 1)
        counts[size] = counts.get(size, 0) + len(w["text"])
    if not counts:
        return 0.0
    return max(counts.items(), key=lambda kv: kv[1])[0]


def _link_for_word(word: dict, hyperlinks: List[dict]) -> Optional[str]:
    cx = (word["x0"] + word["x1"]) / 2
    cy = (word["top"] + word["bottom"]) / 2
    for link in hyperlinks:
        if link.get("x0", 0) <= cx <= link.get("x1", 0) and link.get("top", 0) <= cy <= link.get(
            "bottom", 0
        ):
            return link.get("uri")
    return None


def _build_runs(words: List[dict], hyperlinks: List[dict]) -> List[TextRun]:
    runs: List[TextRun] = []
    bucket: List[str] = []
    bucket_uri: Optional[str] = None
    for w in words:
        uri = _link_for_word(w, hyperlinks)
        if bucket and uri != bucket_uri:
            runs.append(TextRun(text=" ".join(bucket), link_uri=bucket_uri))
            bucket = []
        bucket_uri = uri
        bucket.append(w["text"])
    if bucket:
        runs.append(TextRun(text=" ".join(bucket), link_uri=bucket_uri))
    return runs


def _words_to_blocks(
    words: List[dict], heading_sizes: Dict[float, int], hyperlinks: List[dict]
) -> List[Tuple[float, Block]]:
    lines = _group_lines(words)
    results: List[Tuple[float, Block]] = []
    # Wrapped continuation lines (no list marker, no heading size) get appended
    # to whichever block - a paragraph or a list item - is still "open" rather
    # than always starting a fresh paragraph, so multi-line list items don't
    # get split into a list item plus an orphan paragraph.
    open_block: Optional[Block] = None
    prev_bottom: Optional[float] = None

    for line_words in lines:
        line_top = min(w["top"] for w in line_words)
        line_bottom = max(w["bottom"] for w in line_words)
        line_text = " ".join(w["text"] for w in line_words)
        dominant_size = _dominant_size(line_words)
        heading_level = heading_sizes.get(round(dominant_size, 1))

        is_unordered = bool(LIST_UNORDERED_LINE_RE.match(line_text))
        is_ordered = False if is_unordered else bool(LIST_ORDERED_LINE_RE.match(line_text))

        if heading_level:
            open_block = None
            results.append(
                (
                    line_top,
                    Block(
                        kind="heading",
                        level=heading_level,
                        runs=_build_runs(line_words, hyperlinks),
                    ),
                )
            )
        elif is_unordered or is_ordered:
            marker_words = line_words
            first_text = line_words[0]["text"]
            if LIST_UNORDERED_MARKER_RE.fullmatch(first_text) or LIST_ORDERED_MARKER_RE.fullmatch(
                first_text
            ):
                marker_words = line_words[1:]
            open_block = Block(
                kind="list_item", ordered=is_ordered, runs=_build_runs(marker_words, hyperlinks)
            )
            results.append((line_top, open_block))
        else:
            line_height = max(line_bottom - line_top, 1.0)
            gap = (line_top - prev_bottom) if prev_bottom is not None else 0.0
            if open_block is None or gap > line_height * 1.4:
                open_block = Block(kind="paragraph", runs=[])
                results.append((line_top, open_block))
            elif open_block.runs:
                open_block.runs.append(TextRun(text=" "))
            open_block.runs.extend(_build_runs(line_words, hyperlinks))

        prev_bottom = line_bottom

    return results


def _images_cover_page(images: List[dict], page_width: float, page_height: float) -> bool:
    page_area = page_width * page_height
    if page_area <= 0:
        return False
    covered = sum(
        max(0.0, img["x1"] - img["x0"]) * max(0.0, img["bottom"] - img["top"]) for img in images
    )
    return covered >= 0.6 * page_area


def _clean_table_cell(value: Optional[str]) -> str:
    if not value:
        return ""
    normalized = value.replace("\r\n", "\n").replace("\r", "\n")
    parts = [" ".join(line.split()) for line in normalized.split("\n")]
    cell = "<br>".join(p for p in parts if p)
    return cell.replace("|", "\\|")


def _build_page(
    *,
    page,
    page_number: int,
    words: List[dict],
    heading_sizes: Dict[float, int],
    want_images: bool,
    assets_dir: Path,
    pdf_images: list,
) -> Tuple[PageResult, int]:
    char_count = len(page.chars)
    tables = page.find_tables()
    hyperlinks = page.hyperlinks
    plumber_images = list(page.images)

    def in_any_table(word: dict) -> bool:
        cx = (word["x0"] + word["x1"]) / 2
        cy = (word["top"] + word["bottom"]) / 2
        for t in tables:
            x0, top, x1, bottom = t.bbox
            if x0 <= cx <= x1 and top <= cy <= bottom:
                return True
        return False

    content_words = [w for w in words if not in_any_table(w)]
    likely_scanned = (
        char_count == 0
        and bool(plumber_images)
        and _images_cover_page(plumber_images, page.width, page.height)
    )

    columns = _detect_columns(content_words, page.width)
    buckets: List[List[Tuple[float, Block]]] = [[] for _ in columns]

    for col_idx in range(len(columns)):
        col_words = [
            w for w in content_words if _assign_column(w["x0"], w["x1"], columns) == col_idx
        ]
        buckets[col_idx].extend(_words_to_blocks(col_words, heading_sizes, hyperlinks))

    for t in tables:
        x0, top, x1, _bottom = t.bbox
        col_idx = _assign_column(x0, x1, columns)
        rows = [[_clean_table_cell(cell) for cell in row] for row in (t.extract() or [])]
        if rows:
            buckets[col_idx].append((top, Block(kind="table", rows=rows)))

    images_written = 0
    if want_images:
        for idx, img in enumerate(pdf_images):
            if idx < len(plumber_images):
                meta = plumber_images[idx]
                top, x0, x1 = meta["top"], meta["x0"], meta["x1"]
            else:
                top, x0, x1 = 10**9 + idx, 0.0, page.width
            col_idx = _assign_column(x0, x1, columns)

            fmt = "png"
            if getattr(img, "image", None) is not None and img.image.format:
                fmt = img.image.format.lower()
            asset_name = f"page{page_number}_img{idx + 1}.{fmt}"
            assets_dir.mkdir(parents=True, exist_ok=True)
            (assets_dir / asset_name).write_bytes(img.data)
            rel_path = Path(assets_dir.name) / asset_name
            buckets[col_idx].append((top, Block(kind="image", image_path=rel_path.as_posix())))
            images_written += 1

    blocks: List[Block] = []
    for bucket in buckets:
        bucket.sort(key=lambda pair: pair[0])
        blocks.extend(b for _, b in bucket)

    return (
        PageResult(
            number=page_number,
            blocks=blocks,
            char_count=char_count,
            image_count=len(plumber_images),
            likely_scanned=likely_scanned,
        ),
        images_written,
    )


# ---------------------------------------------------------------------------
# Markdown rendering + atomic write
# ---------------------------------------------------------------------------


class MarkdownWriter:
    def render(self, result: ExtractionResult) -> str:
        lines: List[str] = []

        partial_scanned = result.scanned_pages
        if partial_scanned and len(partial_scanned) < len(result.pages):
            nums = ", ".join(str(n) for n in partial_scanned)
            lines.append(
                f"> **Warning:** page(s) {nums} appear to be scanned/image-only; text on these "
                "pages could not be extracted (OCR is out of scope for this script)."
            )
            lines.append("")

        prev_kind: Optional[str] = None
        prev_ordered: Optional[bool] = None
        for page in result.pages:
            for block in page.blocks:
                rendered = self._render_block(block)
                if not rendered:
                    continue
                same_list = (
                    block.kind == "list_item"
                    and prev_kind == "list_item"
                    and block.ordered == prev_ordered
                )
                if same_list:
                    lines.append(rendered)
                else:
                    if lines and lines[-1] != "":
                        lines.append("")
                    lines.append(rendered)
                prev_kind = block.kind
                prev_ordered = block.ordered

        text = "\n".join(lines).strip("\n")
        return text + "\n" if text else ""

    def _render_block(self, block: Block) -> Optional[str]:
        if block.kind == "heading":
            text = self._runs_to_text(block.runs)
            return f"{'#' * max(1, min(block.level, 6))} {text}" if text else None
        if block.kind == "paragraph":
            text = self._runs_to_text(block.runs)
            return text or None
        if block.kind == "list_item":
            text = self._runs_to_text(block.runs)
            return f"{'1.' if block.ordered else '-'} {text}" if text else None
        if block.kind == "table":
            return self._render_table(block.rows)
        if block.kind == "image":
            alt = Path(block.image_path).stem if block.image_path else "image"
            return f"![{alt}]({block.image_path})"
        return None

    def _runs_to_text(self, runs: List[TextRun]) -> str:
        parts = []
        for r in runs:
            text = r.text.strip()
            if not text:
                continue
            parts.append(f"[{text}]({r.link_uri})" if r.link_uri else text)
        return " ".join(parts)

    def _render_table(self, rows: List[List[Optional[str]]]) -> str:
        if not rows:
            return ""
        width = max(len(r) for r in rows)
        padded = [list(r) + [""] * (width - len(r)) for r in rows]
        header, *body = padded
        out = ["| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * width) + " |"]
        out.extend("| " + " | ".join(row) + " |" for row in body)
        return "\n".join(out)

    def write(self, markdown_text: str, output_path: Path) -> None:
        normalized = unicodedata.normalize("NFC", markdown_text)
        normalized = normalized.replace("\r\n", "\n").replace("\r", "\n")
        if not normalized.endswith("\n"):
            normalized += "\n"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(
            dir=str(output_path.parent), prefix=f".{output_path.stem}.", suffix=".md.tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(normalized)
            os.replace(tmp_name, output_path)
        except BaseException:
            with contextlib.suppress(OSError):
                os.unlink(tmp_name)
            raise


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def validate_pdf_signature(pdf_path: Path) -> None:
    try:
        with pdf_path.open("rb") as fh:
            head = fh.read(1024)
    except OSError as exc:
        raise PdfToMarkdownError(
            f"Could not read '{pdf_path}': {exc}", ExitCode.FILE_NOT_FOUND
        ) from exc
    if PDF_MAGIC not in head:
        raise PdfToMarkdownError(
            f"'{pdf_path.name}' does not look like a PDF file (missing %PDF- signature).",
            ExitCode.INVALID_PDF,
        )


def derive_output_path(pdf_path: Path, output_arg: Optional[Path]) -> Path:
    if output_arg is None:
        return pdf_path.with_suffix(".md")
    if output_arg.is_dir() or output_arg.suffix == "":
        return output_arg / (pdf_path.stem + ".md")
    return output_arg


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf_to_markdown.py",
        description=(
            "Convert a born-digital PDF into a single deterministic Markdown file, "
            "locally and without hosted AI."
        ),
    )
    parser.add_argument("pdf_path", type=Path, help="Path to the input PDF file.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output .md path (default: alongside the input, same stem).",
    )
    parser.add_argument(
        "--force",
        "--overwrite",
        dest="force",
        action="store_true",
        help="Overwrite the output file if it already exists.",
    )
    parser.add_argument(
        "--no-images",
        dest="extract_images",
        action="store_false",
        default=True,
        help="Do not extract embedded images to an assets folder.",
    )
    parser.add_argument(
        "--assets-dir",
        type=Path,
        default=None,
        help="Folder for extracted images (default: '<output-stem>_assets' next to the output file).",
    )
    parser.add_argument(
        "--diagnostics",
        action="store_true",
        help="Print extraction statistics and warnings after conversion.",
    )
    parser.add_argument(
        "--json",
        dest="as_json",
        action="store_true",
        help="Print a machine-readable JSON result instead of a human-readable message.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress the human-readable success message (errors are still printed).",
    )
    return parser


def run(args: argparse.Namespace) -> dict:
    pdf_path: Path = args.pdf_path
    if not pdf_path.exists() or not pdf_path.is_file():
        raise PdfToMarkdownError(f"Input file not found: {pdf_path}", ExitCode.FILE_NOT_FOUND)

    output_path = derive_output_path(pdf_path, args.output)
    if output_path.exists() and not args.force:
        raise PdfToMarkdownError(
            f"Output file already exists: {output_path} (use --force to overwrite)",
            ExitCode.OUTPUT_EXISTS,
        )

    require_dependencies()
    validate_pdf_signature(pdf_path)

    extractor: PdfExtractor = PdfPlumberExtractor()
    inspection = extractor.inspect(pdf_path)

    assets_dir = args.assets_dir or output_path.with_name(output_path.stem + "_assets")

    try:
        extraction = extractor.extract(
            pdf_path,
            want_images=args.extract_images,
            assets_dir=assets_dir,
            title=inspection.title,
        )
    except PdfToMarkdownError:
        raise
    except Exception as exc:
        raise PdfToMarkdownError(f"Extraction failed: {exc}", ExitCode.EXTRACTION_FAILED) from exc

    if extraction.total_chars == 0 and extraction.total_images > 0:
        raise PdfToMarkdownError(
            "No extractable text found; this looks like a scanned/image-only PDF. "
            "OCR is out of scope for this script - see SKILL.md 'Deferred scope'.",
            ExitCode.SCANNED_UNSUPPORTED,
        )

    writer = MarkdownWriter()
    markdown_text = writer.render(extraction)
    writer.write(markdown_text, output_path)

    return {
        "ok": True,
        "input_path": str(pdf_path),
        "output_path": str(output_path),
        "assets_dir": str(assets_dir) if extraction.images_written else None,
        "pages": len(extraction.pages),
        "total_chars": extraction.total_chars,
        "headings": sum(1 for p in extraction.pages for b in p.blocks if b.kind == "heading"),
        "tables": sum(1 for p in extraction.pages for b in p.blocks if b.kind == "table"),
        "list_items": sum(1 for p in extraction.pages for b in p.blocks if b.kind == "list_item"),
        "links": sum(1 for p in extraction.pages for b in p.blocks for r in b.runs if r.link_uri),
        "images_found": extraction.total_images,
        "images_extracted": extraction.images_written,
        "scanned_pages": extraction.scanned_pages,
        "warnings": extraction.warnings,
    }


def render_diagnostics(summary: dict) -> str:
    lines = [
        "Diagnostics:",
        f"  pages:            {summary['pages']}",
        f"  characters:       {summary['total_chars']}",
        f"  headings:         {summary['headings']}",
        f"  list items:       {summary['list_items']}",
        f"  tables:           {summary['tables']}",
        f"  links:            {summary['links']}",
        f"  images found:     {summary['images_found']}",
        f"  images extracted: {summary['images_extracted']}",
    ]
    if summary["scanned_pages"]:
        lines.append(
            f"  likely-scanned pages: {', '.join(str(n) for n in summary['scanned_pages'])}"
        )
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        summary = run(args)
    except PdfToMarkdownError as exc:
        if args.as_json:
            print(json.dumps({"ok": False, "error": str(exc), "exit_code": int(exc.exit_code)}))
        else:
            print(f"[ERROR] {exc}", file=sys.stderr)
        return int(exc.exit_code)
    except Exception as exc:  # unexpected - never silently swallow
        if args.as_json:
            print(
                json.dumps(
                    {"ok": False, "error": str(exc), "exit_code": int(ExitCode.UNEXPECTED_ERROR)}
                )
            )
        else:
            print(f"[ERROR] Unexpected failure: {exc}", file=sys.stderr)
        return int(ExitCode.UNEXPECTED_ERROR)

    if args.as_json:
        print(json.dumps(summary, indent=2))
    else:
        if not args.quiet:
            print(
                f"Wrote {summary['output_path']} ({summary['pages']} pages, {summary['total_chars']} chars)."
            )
        for warning in summary["warnings"]:
            print(f"[WARN] {warning}")
        if args.diagnostics:
            print(render_diagnostics(summary))
    return int(ExitCode.SUCCESS)


if __name__ == "__main__":
    sys.exit(main())
