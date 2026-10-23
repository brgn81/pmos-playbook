# Authoring guide

## Adding a type

One change touches three files:

1. `types.yaml` – name, description, Lucide icon, color slot (`type-1` to `type-8`), template path.
2. `preset/pmos.yaml` – the folder a new workspace gets for it.
3. `templates/<name>.md` – the item template.

## Checks before every commit

```text
uv run scripts/lint.py
pmos playbook validate . --json
```

## Versions

Patch for wording, minor for new skills or types, major for removals or renames.
Every release gets a CHANGELOG entry.
