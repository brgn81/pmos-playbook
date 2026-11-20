---
description: File a GitHub issue with consistent triage data, a duplicate check and a severity
mode: agent
---

# /create-issue -- Create a GitHub issue

Create a GitHub issue using the **create-issue** skill (`skills/toolkit/create-issue/SKILL.md`).

## Invocation

```text
/create-issue
/create-issue [short issue title]
```

## Workflow

1. Confirm the scope and the target repository. Ask when either is missing.
2. Resolve the authenticated user with the GitHub MCP `get_me`. Default assignee.
3. Collect title and summary. Lightweight mode needs only title, summary and impact. Full mode adds expected and actual behavior, steps to reproduce, environment and severity.
4. Search for duplicates. Warn and show the top matches, then continue unless the user stops.
5. Create the issue with the body template of the skill. Default label `user-feedback` if the repository has it, default severity `medium`.
6. Report the issue number and URL, the duplicate check result, the assignee and missing triage details. If creation is pending or blocked, say that no issue was created.

## Notes

- Never create an issue before the user confirmed title and target repository.
- A change that needs something PMOS does not offer yet is a `contract` issue in both `brgn81/pmos` and `brgn81/pmos-playbook`, linked.
