---
description: Propose 💡 insight statements from a meeting minute and insert the ones you pick at the point they were discussed
agent: agent
---

# /insights-from-minute – Generate insights from a minute

Read a meeting minute (a full transcript or just a collection of notes), propose short, catchy insight candidates, and insert the ones you select directly into the minute – marked with a `💡 ` prefix so they can be extracted into insight items later.

## Invocation

```text
/insights-from-minute <item id>
/insights-from-minute <path to the minute>
/insights-from-minute                     # uses the minute currently open in the editor or attached to the chat, or asks for a path or id, optionally listing recently modified files in the minute folder of `pmos where --pmos-type minute --json` as suggestions
```

## Workflow

Follow [.claude/skills/discovery/insights-from-minute/SKILL.md](../skills/discovery/insights-from-minute/SKILL.md) for the full ruleset. If SKILL.md cannot be loaded, stop immediately and tell the user: "Cannot proceed – SKILL.md not found at .claude/skills/discovery/insights-from-minute/SKILL.md. Please verify the path and try again."

1. Load the target minute and read the full page.
2. Propose a numbered list of insight candidates – do not write anything yet.
3. Ask which candidates to add (by number, "all", or "none"); accept wording edits.
4. Insert each selected insight at its respective location, following the skill's placement rules (same-paragraph linebreak vs. new paragraph) and formatting rules (💡 prefix, same language as the minute, short and to the point, names the expert/company).
5. Report what was added and where. Do not push automatically – remind the user that pushing the minute (`/push`, when the minute type can push) is a separate step.
