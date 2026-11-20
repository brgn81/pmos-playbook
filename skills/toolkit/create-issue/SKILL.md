---
name: create-issue
description: "Create and triage a GitHub issue through the GitHub MCP tools. Use when the user wants to file, report or log an issue, bug or feature request in one of the PMOS repositories."
disable-model-invocation: true
---
# Create issue

Create a clear GitHub issue with consistent triage data. This skill is the one place where the Playbook talks to GitHub: it uses the GitHub MCP tools, not `pmos`, because an issue is not a PMOS item.

## Scope

- Target repository: ask the user, or take it from the request. Typical targets are `brgn81/pmos`, `brgn81/pmos-playbook` and `brgn81/pmos-docs`. Never guess and never assume a default.
- Duplicate handling: warn only, never block creation automatically.
- Default label: `user-feedback`, only if the label exists in the target repository.
- Default assignee: the authenticated GitHub user.

## Workflow

1. Confirm intent and scope. If the topic is unclear, ask what the issue should cover.
2. Resolve the actor with `get_me`. Its login is the default assignee unless the user says otherwise.
3. Resolve the target repository. If the user's request names none, ask.
4. Collect inputs. Always required: title and short summary. In lightweight mode, title, summary and impact are enough. In full mode also collect expected behavior, actual behavior, steps to reproduce, environment, severity and impact.
5. Build metadata. Apply the default label if it exists (check with `get_label`), merge labels the user names, set the assignee. Ask for milestone or issue type only when needed and never block on them.
6. Check duplicates with `search_issues` (use `gh api -X GET search/issues -f q='repo:<owner>/<repo> is:issue <terms>'` if the MCP search tool is not available). If likely duplicates exist, show the top matches and warn. Continue unless the user stops.
7. If the issue needs something PMOS does not offer yet, it is a `contract` issue in both `brgn81/pmos` and `brgn81/pmos-playbook`, linked to each other. Offer to create the second one.
8. Create the issue with `issue_write`, `method: create`. Use the body template below. Severity is optional and defaults to `medium`; if given, it is one of `blocker`, `high`, `medium`, `low`.
9. Treat the issue as created only when the tool returns an issue number and URL. If it returns a pending state or asks for a confirmation form, say that nothing was created, do not repeat the call and do not report success.
10. Report the issue number and URL, the duplicate check result, the assignee and any missing triage details.

## Body template

```markdown
## Summary

[short problem statement]

## Severity

[blocker | high | medium | low, default medium]

## Expected behavior

[what should happen]

## Actual behavior

[what happens instead]

## Steps to reproduce

1. ...

## Environment

- OS:
- PMOS version (`pmos --version`):
- Playbook version:

## Evidence

- Logs:
- Error messages:
- Related files or links:

## Impact

[who is affected and how]

## Notes

- Duplicate check:
- Follow-up triage:
```

## Quality checks

- The issue is specific, reproducible and testable.
- Expected and actual behavior are separate.
- Evidence is concrete, not speculative.
- Secrets, tokens and credentials are redacted from logs before publishing.
- Examples use the neutral sample product "Acme Planner"; no customer names or site URLs.
