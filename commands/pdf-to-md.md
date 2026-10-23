---
description: Convert a born-digital PDF into a deterministic markdown file via a local, script-powered pipeline - no hosted AI
agent: agent
model: Claude Haiku 4.5 (copilot)
---

# /pdf-to-md - Convert a PDF to markdown

Convert a local PDF into a single markdown file by delegating to
[pdf_to_markdown.py](../skills/toolkit/pdf-to-markdown/scripts/pdf_to_markdown.py)
(the `pdf-to-markdown` skill). This command is deterministic orchestration,
not content generation: it validates arguments, runs the script, and reports
the result. It never reads the PDF itself or transcribes/rewrites content.

## Invocation

```text
/pdf-to-md path/to/document.pdf
/pdf-to-md path/to/document.pdf --force
/pdf-to-md path/to/document.pdf -o notes/document.md
```

## Workflow

### Step 1: resolve the PDF path

The script needs a real file on disk - by design, it never reads a chat
attachment's content, extracted text, or rendered pages directly (no hosted
AI, no model transcription; see SKILL.md "When to use"). Work through these
checks **in order**. Do not skip ahead to asking for a path before doing
them - a bare "please provide the file path" is the wrong response any time
a PDF is visible anywhere in the conversation.

1. **A path given in the invocation** - use it, skip the rest of this step.
2. **Check the conversation itself for an attached or open PDF** - not just
   whether one was named in the invocation text. Look at whatever the
   environment exposes for attachments/open files (a workspace-relative or
   absolute path, a file reference, an editor tab), not only the parsed
   text or rendered pages a chat surface may show inline - many surfaces
   save an upload to a real file even while also displaying that inline
   preview.
   - **Exactly one PDF, and a local path is resolvable** - use it directly.
     Do not ask which file, and do not ask for confirmation first.
   - **More than one PDF attached/open** - ask which one, naming each by
     filename so the user can just pick.
   - **A PDF is visibly attached/referenced, but no local path is
     resolvable from anything the environment exposes** - explicitly
     acknowledge the attachment in your reply, then explain in one line
     why a path is still needed. Do not fall back to reading or
     transcribing the attachment's content as a substitute. For example:
     "I see a PDF attached to this conversation, but I don't have a local
     file path for it - this command runs a script that needs the actual
     file on disk. Could you save it locally (e.g., into this workspace)
     and share the path?"
   - **Nothing given and nothing attached anywhere in the conversation** -
     only now ask for a path, with no reference to a nonexistent
     attachment.

### Step 2: check prerequisites once per session

If this is the first PDF conversion this session, or a prior run failed with
exit code 6, run:

```powershell
uv sync --extra pdf
```

Otherwise skip straight to Step 3 - do not re-run `uv sync` on every
invocation.

### Step 3: run the script

```powershell
uv run .claude/skills/toolkit/pdf-to-markdown/scripts/pdf_to_markdown.py {pdf-path} --json
```

Pass through any flags the user asked for: `-o/--output`, `--force`,
`--no-images`, `--assets-dir`, `--diagnostics`. Use `--json` so the result is
easy to parse and report accurately - never guess at what happened from
partial output.

### Step 4: handle the result

Read the JSON result's `exit_code`/`ok` field (or the process exit code):

- **0 (success):** report the output path, page count, and character count
  from the result. Mention any `warnings` (e.g. likely-scanned pages) and,
  if `--diagnostics` was requested or the user seems to want detail, the
  extraction stats (headings/tables/links/images).
- **8 (output exists):** the target `.md` file already exists. Ask the user
  whether to overwrite (`--force`) or choose a different `-o` path - never
  pass `--force` without asking first, since this is exactly the
  "never silently overwrite" guarantee the script is built to uphold.
- **5 (encrypted) / 4 (invalid PDF) / 3 (file not found):** report the
  specific reason from the script's error message. Do not retry blindly;
  ask the user for a corrected path or a decrypted copy if relevant.
- **6 (missing dependency):** run `uv sync --extra pdf` (Step 2) and retry
  once. If it still fails, report the error as-is.
- **9 (scanned/image-only PDF):** report that the PDF has no extractable
  text layer and that OCR is out of scope for this script (see the skill's
  "Deferred scope"). Do not attempt to read the PDF yourself as a
  workaround.
- **7 / 1 (extraction failed / unexpected error):** report the error
  message verbatim; do not speculate about the cause beyond what the script
  reported.

### Step 5: report

Summarize: output file path, pages converted, and any warnings. Do not
paste the full markdown output into chat unless the user asks for it - point
them at the file.
