# Output template: customer value map

## File name

`YYMMDD_Customer-value-[customer].md`
Example: `260325_Customer-value-Example-Corp.md`

---

## Document structure

```markdown
# Customer value [product name] for [customer]

_Created: YYYY-MM-DD | Based on: [N] meeting minutes_

## Current challenges of [customer]

### [Theme 1]

- [Short, concise description of the problem.]
  - Mentioned: YYYY-MM-DD in [item_id].
  - By whom: [name(s)] ("[direct quote or the paraphrased core of the statement]").
  - Business impact:
    - [Concrete business impact 1]
    - [Concrete business impact 2]

- [Next problem in the same theme.]
  - Mentioned: YYYY-MM-DD in [item_id 1], YYYY-MM-DD in [item_id 2].
  - By whom: [name(s)].
  - Business impact:
    - [Concrete business impact]

### [Theme 2]

- [Problem.]
  - Mentioned: ...
  - By whom: ...
  - Business impact:
    - ...

## Positive feedback and strengths

- [What works well or is explicitly named as added value.]
  - Mentioned: ...
  - By whom: ...

## Next steps and open questions

- [Concrete next step or urgent open question.]
```

---

## Rules for filling it in

### Theme categories (suggestions)

Choose categories that fit the customer's context. Typical themes:

- Product management and development
- Sales and quoting
- Management and controlling
- Data and IT
- Processes and organization

Group several similar problems under one theme. Do not create a category for a single isolated problem; assign it to the closest theme.

### Style and language

- Language: the language the user asks for, English by default, throughout
- Capitalization: first word and proper nouns only, no title case
- Quotes: direct quotes in quotation marks, paraphrases without
- Business impact: always from the customer's point of view, not the product's
- Sources: refer to the minute by its `item_id`
- Take the date from the minute's content or file name; leave it out if none is visible

### What goes in

- Every explicitly stated problem, complaint or limitation
- Repeated problems from several meetings merged into one entry, with all sources
- Direct quotes preferred where available
- Positive feedback in a section of its own

### What stays out

- Internal company discussions without customer relevance
- Technical implementation details that do not matter to the customer
- Duplicates: the same problem from different meetings becomes one entry
