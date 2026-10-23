---
name: product-explainer
description: Explains the current product from the product profile and the pages of the workspace. Use when the user asks questions about the product, its architecture, personas or workflows.
---

# Product explainer

Answers questions about the product by reading local items.

## Where to read

- The product profile: the folders of `pmos where --pmos-type product-profile --json`.
- Other pages: the folders of `pmos where --pmos-type page --json`.
- A type that is not mapped returns nothing: say so, do not guess a path.
- Read the file names first and open only what the question needs.

## Core principles

- Never fabricate features, facts, personas, insights or context.
- Never infer missing intent.
- If a question cannot be answered from the items, say so explicitly.
- Read only the identity frontmatter (`item_id`, `title`, `url`) and the body.

## Read-only folders

A folder whose `writable` is false in `pmos types --json` is overwritten by the next pull. Never edit it.

When content in such a folder needs to change:

1. Propose the change to the user, with the `url` of the source item so they can edit it upstream.
2. If the user wants a working copy, ask which writable folder it goes to and use the same file name.
3. Never edit the original.

## Related skills

- Competitor analysis: `.claude/skills/pm-market-research/competitor-analysis/SKILL.md`
- User personas: `.claude/skills/pm-market-research/user-personas/SKILL.md`
- Customer journey map: `.claude/skills/pm-market-research/customer-journey-map/SKILL.md`
- Positioning ideas: `.claude/skills/pm-go-to-market/positioning-ideas/SKILL.md`
