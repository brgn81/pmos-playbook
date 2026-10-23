# PMOS Playbook

Base rules for product management work in this workspace.

## Folders

- Never assume a folder name. Resolve it with `pmos where --pmos-type <type> --json`.
- A type the workspace has not mapped returns nothing. Say so and ask; do not guess a path.
- Never write into a folder that is synced read-only. Write only to work folders and local types.

## Items

- Every synced item opens with `item_id`, `title` and `url`. Read these and the body; nothing else in the frontmatter.
- Edit remote-owned values upstream, not locally.

## Sync

- Sync only with `/pull`, `/push` and `/status`, or `pmos pull|push|status --json`.
- When an item is blocked, show the guidance options to the user. Never pick one for them and never jump to `--force`.

## Style

- Respond in English. Sentence case in headings. En dash with spaces, never em dash.
- Be concise. Use bullet points for lists and steps.
- Keep generated output deterministic and reviewable.
