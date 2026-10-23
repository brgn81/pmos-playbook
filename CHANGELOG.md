# Changelog

## 0.1.0 – unreleased

- Structure: `manifest.yaml`, `types.yaml` with 12 types, neutral `preset/pmos.yaml`, item templates.
- Base rules: `playbook.md`, `rules/markdown.md`, `rules/language.md`.
- Tooling: `scripts/lint.py`, CI with `pmos playbook validate`.
- Type `product-profile` for base knowledge about the product (a recommended folder, not required).
- Agents: `pm-agent` and eight helpers, ported from the legacy PM OS; folders come from `pmos where`.
- Rules: `idea-authoring`, `discovery-conventions`, `question-feedback-handler`, `sync-conflict-guidance`.
- Skills: `discovery` (14), `strategy` (13) and `market-research` (7), ported from the legacy PM OS and, except `insights-from-minute`, derived from phuryn/pm-skills (see NOTICE). Packs carry the name of the type they serve, without the `pm-` prefix.
