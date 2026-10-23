---
name: customer-value-doc
description: Generate a structured customer value map by extracting pain points, challenges and feedback from meeting minutes. Use when a user asks to create a customer value map, analyse customer pain points, or summarize what a specific customer needs. Starts by asking for the customer name and relevant contacts, then searches the minutes.
---

# Customer value map

Generates a structured markdown document that captures a customer's current challenges, pain points and feedback, extracted from the meeting minutes of the workspace.

## Workflow

### Step 1: Ask for customer and contacts

Always start with:

> "Which customer should the value map be for? Please give the customer name and, optionally, the names of relevant contacts."

Wait for the response before proceeding.

### Step 2: Find relevant minutes

Resolve the minutes folder with `pmos where --pmos-type minute --json`. A type that is not mapped returns nothing: say so, do not guess a path.

Run the search script from the workspace root:

```text
uv run .claude/skills/go-to-market/customer-value-doc/scripts/find_customer_minutes.py --folder <minutes folder> "<customer>" ["<contact>" ...]
```

- Use the customer name and each contact name as separate search terms.
- The script searches file names and content, case-insensitive.
- Tell the user which files were found: "I found [N] relevant minutes: ..."

If no files are found, say so and suggest alternative spellings or abbreviations.

### Step 3: Read and extract from minutes

Read each matched file in full. For each file, extract:

- **Problems and pain points** – anything the customer describes as a challenge, limitation, complaint or inefficiency
- **Direct quotes** – exact customer statements are especially valuable
- **Who said it** – name and role if available
- **When** – the date from the content or the file name
- **Positive feedback** – explicit praise or confirmed value

### Step 4: Synthesize and write the value map

Apply the structure and rules from [references/output-template.md](references/output-template.md).

- Group pain points into thematic categories (the template suggests some).
- Merge duplicate problems from several meetings into one entry and list all sources.
- Sort categories by business relevance, most systemic issues first.
- Refer to a source minute by its `item_id` (identity frontmatter), with its `title` if helpful.
- Write in the language the user asks for; English by default.

### Step 5: Save or present the output

Suggested file name: `YYMMDD_Customer-value-[customer].md`

Ask where to save it. Write only to a folder that is not synced read-only (`writable` is true in `pmos types --json`), for example the folder of `pmos where --pmos-type go-to-market --json`, or `pmos where --pmos-type draft --json` for a scratch version.

## Notes

- If a meeting mentions a customer only in passing, include the insight only if it contains a clear, attributable pain point.
- Do not invent or infer pain points. Document only what the minutes state explicitly.
