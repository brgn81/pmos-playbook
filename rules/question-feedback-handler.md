---
applyTo: "**/*.md"
description: "Consistent question and feedback handling in markdown items"
---

# Question and feedback handling

Keep question and feedback handling consistent across all markdown work-items in this workspace.

## When to apply

Apply these rules when:
- Adding or updating stakeholder questions in a work-item.
- Collecting feedback statements.
- Marking items as answered or considered.
- The file contains or should contain collapsible Questions or Feedback blocks.
- An auditable trail of handled inputs is needed.

**Do NOT apply for:**
- Synchronization with the remote (`/pull`, `/push`, `/status`), timestamps, or conflict handling.
- Rewriting product content without explicit user confirmation.
- Auto-closing or auto-striking items without user instruction.

## Critical rules

**Canonical wrappers:**
- Questions block: `<details><summary>Questions</summary>`
- Feedback block: `<details><summary>Feedback</summary>`
- Always add `<br/>` immediately after each closing `</details>` tag.

**Question entry format:**
- Questions are listed per person where useful, for example `@Name:`.
- Answers use strict arrow format directly after the question line:
  - `-> answer text`
- Multiple answers are allowed, each on its own `->` line.

**Feedback entry format:**
- Feedback is captured as line-by-line statements (typically bullets).
- No `->` marker is required for feedback lines.
- Each feedback line is independently actionable.

**Resolution marker:**
- Use markdown strikethrough on the specific handled line: `~~...~~`
- Keep struck lines visible for audit trail.

**Person mention policy:**
- If the workspace has a persons registry, use the simplified display name it holds (for example `@Alex Example`).
- Without a registry, or for a person it does not list, write the name as the user gives it. Never guess a name.

## Status model

### Question workflow

- **open**: no answer yet.
- **answered**: at least one `->` answer line exists.
- **considered**: answer has been integrated into relevant sections and the question line is struck through.

### Feedback workflow

- **open**: feedback statements are collected but not yet handled.
- **considered**: the relevant feedback line has been integrated into relevant sections and that line is struck through.

## Handling workflow

1. Collect only what the user explicitly states.
2. Keep Questions and Feedback blocks where the user places them.
3. For questions, append `->` answer lines under the question item.
4. For feedback, add plain lines or bullets without `->`.
5. When user confirms integration, strike through only the specific question or feedback line that was considered.
6. Never remove resolved lines unless the user explicitly requests cleanup.
7. Add `<br/>` directly after each `</details>` block to improve readability.

## Examples

### Questions block

```markdown
<details>
<summary>Questions</summary>

@Product stakeholder:
- Should we display the confidence score in the first release?
-> show it only to internal users first

@Data owner:
- Which data source is the source of truth?

</details>
<br/>
```

State interpretation:
- First question is **answered**.
- Second question is **open**.

### Considered question

```markdown
<details>
<summary>Questions</summary>

@Product stakeholder:
~~- Should we display the confidence score in the first release?~~
-> show it only to internal users first

</details>
<br/>
```

State interpretation:
- Question is **considered**.

### Feedback block

```markdown
<details>
<summary>Feedback</summary>

- Keep the onboarding flow below three steps.
- Explain score calculation with one concrete example.

</details>
<br/>
```

Both feedback lines are **open**.

### Considered feedback lines

```markdown
<details>
<summary>Feedback</summary>

~~- Keep the onboarding flow below three steps.~~
- Explain score calculation with one concrete example.

</details>
<br/>
```

State interpretation:
- First feedback line is **considered**.
- Second feedback line remains **open**.
