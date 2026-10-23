---
applyTo: "**/*.md"
description: "Guidance for creating and refining idea items"
---

# Idea authoring guidance

## Scope

- Applies to items of the type `idea`: the files in the folder of `pmos where --pmos-type idea --json`.
- Folders of type `product-profile` and of any synced read-only type are reference only. Copy only what is needed into the idea.

## Writing behavior

- Progress in clear, incremental steps and confirm assumptions when context is missing.
- Keep statements evidence-oriented and avoid speculative claims.
- Capture open questions explicitly instead of filling gaps with invented details.

## Discovery page linking

- Before assumption work for non-small ideas, check that the idea links a discovery page.
- If one is linked, use it as the source of truth for detailed assumptions and make sure it exists locally in the folder of `pmos where --pmos-type discovery --json` before editing.
- Keep the assumptions section of the idea condensed and numbered (`Assumption N: short title`).
- If none is linked, stop drafting assumptions and ask the user to create a discovery page from the discovery template and link it.
- Do not name a tool when asking. Say "your discovery tool".

## Structure and quality

- Preserve the section order unless the user asks to restructure.
- Keep edits minimal and local.
- Prefer concise bullets and explicit acceptance criteria when relevant.
- Output follows `.claude/rules/markdown.md`.
