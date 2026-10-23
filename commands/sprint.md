---
description: Sprint lifecycle – plan a sprint, run a retrospective, or generate release notes
mode: agent
---

# /sprint -- Sprint lifecycle

Three modes covering the sprint lifecycle: **plan** for sprint planning, **retro** for retrospectives, **release-notes** for shipping communication.

## Invocation

```text
/sprint plan 2-week sprint, 4 engineers, focus on checkout improvements
/sprint retro [paste team feedback or sprint data]
/sprint release-notes [paste tickets, changelog, or PRD]
/sprint                    # asks which phase you're in
```

## Modes

---

### Plan mode

Prepare for sprint planning with capacity estimation, story selection, and risk identification.

#### Workflow

**Step 1: Gather sprint context**
- Sprint duration (1 or 2 weeks)
- Team composition (engineers, designers, QA – and availability)
- Sprint goal or focus area
- Backlog items to consider (paste, upload, or describe)
- Any carry-over from last sprint
- Known interruptions (holidays, on-call, meetings)

**Step 2: Estimate capacity**

Apply the **sprint-plan** skill:

- Calculate available engineering hours/points after meetings, on-call, PTO
- Apply a velocity adjustment based on historical data (if provided) or industry standard (70% of theoretical capacity)
- Show capacity breakdown per team member

**Step 3: Select and sequence stories**

- Recommend which stories fit within capacity
- Flag dependency chains (A must complete before B starts)
- Identify risks: stories that are underspecified, have external dependencies, or need design input
- Balance quick wins with larger items
- Ensure every story has acceptance criteria

**Step 4: Generate sprint plan**

```text
## Sprint plan: [sprint name/number]

**Duration**: [dates]
**Sprint Goal**: [one sentence]
**Team**: [members and availability]

### Capacity
| Member | Available Days | Points/Hours | Notes |
|--------|--------------|-------------|-------|

**Total capacity**: [X] points/hours
**Recommended commitment**: [Y] points/hours (with buffer)

### Selected stories
| # | Story | Points | Owner | Dependencies | Risk |
| --- | --- | --- | --- | --- | --- |

### Sprint risks
1. [Risk] – Mitigation: [action]

### Definition of done
- [ ] Code reviewed
- [ ] Tests passing
- [ ] Deployed to staging
- [ ] QA approved
- [ ] Documentation updated (if applicable)
```

---

### Retro mode

Facilitate a structured retrospective that produces actionable improvements.

#### Workflow

**Step 1: Gather sprint feedback**

Accept input as:
- Team feedback (pasted from a survey, Slack, or collaborative doc)
- Sprint metrics (velocity, bugs, incidents)
- The user's own observations

Ask: "Which retro format do you prefer?"
- **Start/Stop/Continue** (simple, fast)
- **4Ls** (Liked, Learned, Lacked, Longed for)
- **Sailboat** (Wind = helps, Anchor = slows, Rocks = risks, Island = goals)

**Step 2: Analyze and structure**

Apply the **retro** skill:

- Categorize feedback into the chosen framework
- Identify themes and patterns
- Separate symptoms from root causes
- Highlight wins worth celebrating

**Step 3: Generate retro summary**

```text
## Sprint retrospective: [sprint name]

**Date**: [today]
**Format**: [Start/Stop/Continue | 4Ls | Sailboat]
**Participants**: [if known]

### What went well
[Grouped themes with supporting evidence]

### What didn't go well
[Grouped themes with root cause analysis]

### Key insights
[2-3 patterns that emerged]

### Action items
| # | Action | Owner | Deadline | Priority |
| --- | --- | --- | --- | --- |

### Metrics this sprint
| Metric | This Sprint | Last Sprint | Trend |
| --- | --- | --- | --- |
```

---

### Release notes mode

Generate user-facing release notes from technical artifacts.

#### Workflow

**Step 1: Accept release content**

Accept:
- Jira/Linear tickets or changelog
- PRD or feature specs
- Git commit messages or PR descriptions
- Team's internal summary of what shipped

**Step 2: Transform**

Apply the **release-notes** skill:

- Translate technical language into user benefits
- Categorize as: New Features, Improvements, Bug Fixes
- Write in the product's voice (ask about tone if not clear)
- Highlight the most impactful change first

**Step 3: Generate release notes**

```text
## What's New – [Version/Date]

### Highlights
[1-2 sentence summary of the most important change]

### New features
- **[Feature Name]** – [user-facing benefit in plain language]

### Improvements
- **[Improvement]** – [what's better now]

### Bug fixes
- Fixed [issue] that caused [user impact]

### Coming soon
[Optional teaser for next release]
```

Save as markdown and offer to format for different channels (blog post, in-app, email, Slack announcement).

## Notes

- For plan mode: protect 20% buffer for unplanned work – teams that plan at 100% capacity always miss
- For retro mode: focus on 2-3 high-impact action items, not 10 things nobody will do
- For release notes: always frame changes as user benefits, not technical implementations
- Each mode can chain to the others: plan → (sprint happens) → retro → release-notes
