---
description: Start an idea session – load or create an idea item, resolve sync conflicts, and identify where to continue
agent: idea-helper
---

# /start-idea – Begin an idea session

Initialize a working session on a product idea. Handles item lookup, sync conflict resolution, and positions you at the next unanswered question.

## Invocation

```text
/start-idea <reference>
/start-idea                  # asks for the item reference
```

## Workflow

### Step 1: Get the item reference

An idea lives on whichever platform the type `idea` is configured for, so the reference format follows that platform: an issue key, a page id, a URL, or a title. Accept whatever the user gives.

If nothing was given in the invocation, ask: "Which idea should we work on? (reference or title)"

Never reject a reference because of its format. If it cannot be resolved, say so.

### Step 2: Locate or import the idea item

1. Resolve the folder with `pmos where --pmos-type idea --json`. A type that is not mapped returns nothing: say so and stop, do not guess a path. The `type` in the result is the type name used in the next calls.
2. Look in that folder for a file whose `item_id` or `title` matches.
3. If there is none, import it with `pmos pull <type> <reference> --json`.
4. If the remote cannot return the item, report the error. Do not create a local file for a synced type.

### Step 3: Resolve remote changes for an existing item

Check the item without writing anything:

```text
pmos status <type> <reference> --json
```

- If the item is up to date, continue with the local file.
- If only the remote changed, offer to pull it.
- If the local file changed, or both changed, show the guidance options to the user as `.claude/rules/sync-conflict-guidance.md` says. Do not overwrite without explicit confirmation.

### Step 4: Identify next unanswered question

1. Scan the idea file top to bottom
2. Find the first section containing `TBD – pending user clarification` or empty content after a `</details><br>` tag
3. Report: "Next unanswered question: **[question text]**. Continue there, or work on a different section?"
4. If all questions answered: "All sections are filled. What would you like to update?"

## Rules

- Never invent references and never create identity fields (`item_id`, `title`, `url`): the remote owns them
- Sync only with `/pull`, `/push`, `/status` or `pmos pull|push|status`; on a blocked item present the guidance options and never choose one
- Never write into a folder that is synced read-only (`writable` is false in `pmos types --json`)
- Never infer an idea folder: resolve it with `pmos where`
- Local files represent the current working state and take priority
