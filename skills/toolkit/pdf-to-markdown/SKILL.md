---
name: pdf-to-markdown
description: Convert a born-digital PDF into a single deterministic markdown file via a local, script-powered pipeline - no hosted AI. Preserves reading order (including simple two-column layouts), headings, paragraphs, lists, links, tables, and embedded images where the source PDF makes that technically possible. Use when a user wants to turn a PDF into editable/reviewable markdown reference material, not when they want an agent to transcribe or summarize a PDF's content.
---

# PDF to markdown

Convert a born-digital PDF into one markdown file using a deterministic,
local, script-powered pipeline. The default (and today, only) path never
calls a hosted AI service and does not use the model to transcribe content -
extraction is delegated entirely to
[pdf_to_markdown.py](scripts/pdf_to_markdown.py).

## When to use

- A user wants to turn a local PDF (a spec, report, article, reference doc)
  into a markdown file they can edit, diff, or feed into other PM OS work.
- The PDF is **born-digital** (has a real text layer) rather than a scan.
- The user wants a fast, predictable, repeatable conversion rather than an
  agent reading and re-typing the PDF's content.
- A PDF was **attached to the conversation**: the script still needs a real
  local path, so `/pdf-to-md` resolves the attachment's actual path rather
  than asking as if nothing were provided - see its Step 1. What it never
  does is substitute the attachment's extracted text/pages for the script.

**Do NOT use for:**
- Scanned or image-only PDFs - this script detects and reports that case
  rather than guessing at OCR (see "Deferred scope").
- Password-protected/encrypted PDFs - reported as a clear failure, not
  prompted for a password.
- Cases where the user explicitly wants an AI summary, rewrite, or analysis
  of a PDF's content - that's a normal chat request, not this skill.

## Prerequisites

The PDF libraries are an optional dependency group, not part of the default
PM OS environment:

```powershell
uv sync --extra pdf
```

Running the script without that extra installed fails fast with exit code 6
and an instruction to run the command above - it never partially degrades.

## Invocation

```powershell
uv run .claude/skills/toolkit/pdf-to-markdown/scripts/pdf_to_markdown.py path/to/document.pdf
```

The paired command is [`/pdf-to-md`](../../../commands/pdf-to-md.prompt.md):

```text
/pdf-to-md path/to/document.pdf
```

Useful flags:

| Flag | Effect |
| --- | --- |
| `-o, --output PATH` | Output `.md` path (default: alongside the input, same stem). |
| `--force` / `--overwrite` | Allow overwriting an existing output file. Without it, an existing output is a hard failure - never silently overwritten. |
| `--no-images` | Skip extracting embedded images to an assets folder. |
| `--assets-dir PATH` | Override the default `<output-stem>_assets/` image folder. |
| `--diagnostics` | Print extraction statistics (pages, headings, tables, links, images, likely-scanned pages) after conversion. |
| `--json` | Print a machine-readable result object instead of a human-readable message - useful for the slash command and for scripting. |
| `--quiet` | Suppress the human-readable success line (errors still print). |

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Success |
| 1 | Unexpected error |
| 2 | Usage error (bad CLI arguments) |
| 3 | Input file not found |
| 4 | Invalid/non-PDF input (missing `%PDF-` signature, or unparseable) |
| 5 | Encrypted/password-protected PDF |
| 6 | Missing optional dependency (`uv sync --extra pdf` not run) |
| 7 | Extraction failed unexpectedly on a valid, unencrypted PDF |
| 8 | Output file already exists and `--force` was not given |
| 9 | Scanned/image-only PDF - nothing extractable (see below) |

## What gets preserved

Where the source PDF's text layer makes it technically possible:

- **Reading order**, including simple two-column layouts (detected
  heuristically from word x-coordinates; the whole left column is emitted
  before the right column).
- **Headings**, inferred from font size relative to the document's most
  common (body-text) size - not from any explicit PDF heading markup, which
  PDF does not have.
- **Paragraphs and lists** (bulleted and numbered; numbered items are all
  emitted as `1.` per `.claude/rules/markdown.md`'s own ordered-list
  convention, relying on markdown renderers to auto-number).
- **Links**, mapped from PDF URI annotations onto the overlapping text run.
- **Tables**, as markdown pipe tables; multi-line cell content is joined
  with `<br>`.
- **Embedded images**, extracted to `<output-stem>_assets/pageN_imgM.<ext>`
  and referenced with a relative markdown image link (unless `--no-images`).
- **Unicode text**, NFC-normalized with LF line endings, written as UTF-8.
  A glyph with no `ToUnicode` mapping in its font (common for bullet/symbol
  glyphs in non-embedded fonts) is written as `�` rather than leaking the
  underlying parser's internal placeholder - visible and honest about the
  data loss instead of silently guessing or dropping it.

All of the above are **heuristics over a pdfminer-derived text/character
stream**, not a layout engine - see "Library choice and licensing" for what
that tradeoff means in practice, and "Deferred scope" for what is
deliberately not attempted.

## Scanned / image-only pages

Every page is checked for a text layer. A page with zero extractable
characters and images covering most of the page area is flagged
`likely_scanned`:

- If **some but not all** pages are like this, conversion still succeeds; a
  warning blockquote naming the affected pages is prepended to the output,
  and the same list appears in `--diagnostics`/`--json`.
- If **the whole document** has no extractable text at all, the run fails
  with exit code 9 rather than emitting a page of nothing. This is a
  deliberate hard stop: OCR is out of scope for this script (see "Deferred
  scope"), and a script that produces a technically-valid-but-empty markdown
  file for a scanned PDF would be a worse outcome than a clear failure.

## Library choice and licensing

Two realistic library stacks were evaluated for the MVP adapter (see the
research table in
[GitHub issue #134](https://github.com/brgn81/pm-os/issues/134)):

| Stack | Fidelity | License |
| --- | --- | --- |
| **`pypdf` + `pdfplumber`** (chosen) | Heuristic: font-size-based headings, x-coordinate-based column/table/link mapping | BSD-3-Clause / MIT - fully permissive |
| `pymupdf4llm` + `PyMuPDF` | Native layout engine: stronger out-of-the-box reading order, table, and image handling | AGPL-3.0-or-commercial |

**This repository has no `LICENSE` file today**, so its own distribution
terms are unsettled - adding an AGPL-licensed *runtime* dependency at that
moment would have been a legal/business decision, not an engineering one.
Given the open question this issue explicitly flagged, the permissive stack
was chosen for the MVP, matching the issue's own stated fallback position.
`pdfplumber`'s own dependencies (`pdfminer.six`, `pypdfium2`, `Pillow`) are
themselves MIT/BSD/Apache-2.0 - no transitive AGPL exposure either.

The tradeoff is real: PyMuPDF's native layout analysis handles complex
multi-column and table layouts more reliably than the heuristics in this
script. If that gap becomes a real problem, a PyMuPDF-backed adapter can be
added later behind the same `PdfExtractor` interface
(`pdf_to_markdown.py`) without changing the CLI contract - at the point
someone is willing to either accept AGPL obligations for that component or
purchase a commercial PyMuPDF license from Artifex.

## Deferred scope

Deliberately out of scope for this script, consistent with "no hosted AI,
minimal footprint" as the default path:

- **OCR / scanned PDFs.** Detected and reported (exit 9 or a warning), never
  attempted. A local-OCR adapter (e.g. Tesseract) could be added later
  behind the same interface.
- **Docling / Marker adapters.** Both are credible higher-fidelity engines
  (see the issue's research table) but pull in large model/runtime
  dependencies disproportionate to this MVP.
- **Hosted or local AI repair/cleanup** of the extracted markdown. Nothing
  in this pipeline calls a model; if a user wants AI cleanup of the output,
  that's a separate, explicit follow-up request in chat.
- **Complex forms, high-fidelity equations/formulas, and vector-diagram
  content.** Text layer extraction only - form fields, embedded LaTeX/MathML
  equivalents, and vector art are not reconstructed.
- **Password-protected/encrypted PDFs.** Reported as a clear failure
  (exit 5); no password prompt or brute-force attempt.
- **Arbitrary N-column layouts.** Only the common single- and two-column
  cases are detected; a three-column layout falls back to single-stream
  reading order.

## Scripts

- [pdf_to_markdown.py](scripts/pdf_to_markdown.py) - the converter CLI.
  `PdfExtractor` (abstract) separates parsing/backend concerns from CLI
  orchestration; `PdfPlumberExtractor` is the only implementation today.
  `MarkdownWriter` renders the extracted structure and writes it atomically
  (temp file + `os.replace`, so a failed write never leaves a partial
  `.md` file behind).

## Tests

[tests/test_pdf_to_markdown.py](tests/test_pdf_to_markdown.py) generates its
own fixture PDFs at test time with `reportlab`, so no binary fixtures are
committed. Run from the Playbook root with:

```text
uv run --with pytest --with reportlab --with "pypdf>=5.0" --with "pdfplumber>=0.11" python -m pytest skills/toolkit/pdf-to-markdown/tests -q
```

The Playbook CI runs the same command.
