# Markdown authoring rules

## Headings

Use sentence case for all headings and titles: capitalize only the first word and proper nouns
(product names, acronyms such as OKR, SQL, GTM). All other words are lowercase at every level.

**Correct:** `## Output deliverables`, `## SWOT analysis`
**Incorrect:** `## Output Deliverables`, `## Swot Analysis`

## Punctuation

- Use an en dash (–) with a space before and after for separators, ranges and breaks.
- Never use an em dash.

## Code blocks

Always add a language identifier to a fenced block. For a block without highlighting, use `text`.

```python
def alert_ok(value: int) -> bool:
    return value >= 0
```

## Tables

Use pipe tables:

| Metric | Threshold | Status |
| --- | --- | --- |
| Invalid records | > 100 | ERROR |

## Allowed syntax

- CommonMark.
- HTML only for `<details>` / `<summary>` (expandable sections), `<br>` (line break) and `<u>` (underline).
- When a line uses `<br>`, keep a real newline in the source as well.

## Forbidden

- HTML tags such as `<strong>`, `<em>`, `<i>`, `<b>`. Use markdown emphasis.
- Jira wiki macros: `{code}`, `{quote}`, `{panel}`, `{expand}`, `||` tables.

Use the markdown equivalents: fenced blocks, `>` blockquotes, pipe tables, `<details>`.
