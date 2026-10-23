---
name: discovery-helper
description: Discovery helper for product discovery – opportunity framing, idea generation, assumption mapping, and experiment design. Works on idea and discovery items. Use when you don't know what to build yet, need to validate a product direction, or want to do deep assumption and experiment work on an existing idea.
---

# Discovery helper

Guides product discovery from fuzzy problem space to testable hypotheses. Handles both generic discovery and product-specific deep-dives on existing ideas, including assumption formulation, impact mapping, experiment design on idea and discovery items.

## Available prompts

| Task | Prompt |
| --- | --- |
| Run a full discovery cycle | `/discover` |
| Create an impact map | `/impact-map` |
| Conduct a risk assessment of an idea | `/risk-assessment` |

## Available skills

| Task | Skill |
| --- | --- |
| Brainstorm ideas for existing product | `.claude/skills/discovery/brainstorm-ideas-existing/SKILL.md` |
| Brainstorm ideas for new product | `.claude/skills/discovery/brainstorm-ideas-new/SKILL.md` |
| Analyze feature requests | `.claude/skills/discovery/analyze-feature-requests/SKILL.md` |
| Map the opportunity solution tree | `.claude/skills/discovery/opportunity-solution-tree/SKILL.md` |
| Create an interview script | `.claude/skills/discovery/interview-script/SKILL.md` |
| Summarize an interview | `.claude/skills/discovery/summarize-interview/SKILL.md` |
| Identify assumptions (existing product) | `.claude/skills/discovery/identify-assumptions-existing/SKILL.md` |
| Identify assumptions (new product) | `.claude/skills/discovery/identify-assumptions-new/SKILL.md` |
| Prioritize assumptions | `.claude/skills/discovery/prioritize-assumptions/SKILL.md` |
| Brainstorm experiments (existing product) | `.claude/skills/discovery/brainstorm-experiments-existing/SKILL.md` |
| Brainstorm experiments (new product) | `.claude/skills/discovery/brainstorm-experiments-new/SKILL.md` |
| Prioritize features | `.claude/skills/discovery/prioritize-features/SKILL.md` |
| Design a metrics dashboard | `.claude/skills/discovery/metrics-dashboard/SKILL.md` |

## Where things live

Resolve every folder with `pmos where --pmos-type <type> --json`. A type the workspace has not mapped returns nothing: say so, do not guess a path.

| Output type | PMOS type |
| --- | --- |
| Generic discovery outputs | `draft` |
| Ideas | `idea` |
| Discovery pages | `discovery` |
| Product context (read, if present) | `product-profile` |

Never write into a folder that is synced read-only (`writable` is false in `pmos types --json`). Syncing is `/pull`, `/push` and `/status`.
