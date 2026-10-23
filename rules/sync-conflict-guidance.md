---
applyTo: "**"
description: "How to present a blocked pull or push to the user"
---

# Sync conflict guidance

Applies to every `/pull`, `/push` and `/status` run, and to `pmos pull|push|status … --json`.

## Why this rule exists

When an item is blocked because the local file changed, the remote changed, or both, PMOS returns one uniform `guidance` object on the blocked item. In `--json` output it is the `guidance` key of the blocked entry in `items`, and the exit code is 2. Do not re-derive or hand-roll this messaging; read it from the output.

A `guidance` object has:

| Key | Meaning |
| --- | --- |
| `action` | `safe_push`, `conflict` or `local_missing` |
| `item_ref` | the reference of this blocked item |
| `local_file` | the file on disk |
| `reason` | why it is blocked |
| `options` | the choices, each with `id`, `label` and `description` |

Every `item_ref` is the blocked item's own reference, never the root a bulk run started from. A run blocked on several items has several refs.

## Required handling

Do not just relay the raw output. Present the choices to the user with `AskUserQuestion`, using exactly the options of the guidance, in their order:

| Option `id` | What it does |
| --- | --- |
| `push_first` | Present only when the guidance contains it, which means the type can push. Push the item, then retry the pull. |
| `force_overwrite` | Re-run the same pull with `--force` to overwrite the local file with the remote version. |
| `restore` | For `local_missing`: re-run the pull with `--restore` to write the file again. |
| `abort` | Make no changes and stop. |

Rules:

- Act on the option the user picks before reporting results.
- Never pick an option for the user. Never jump to `--force`.
- Never decide from a type's name whether it can push. If `push_first` is missing, do not offer it.
- When several items are blocked, ask once for the whole set and apply the choice to each item with its own ref.
- The push command in a `push_first` description is advice, not a contract: run the push with `/push` and the item's own reference.
