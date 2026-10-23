---
description: Prepare a customer interview script or summarize an interview transcript into structured insights
mode: agent
---

# /interview -- Customer interview prep & summary

Two modes: **prep** creates a structured interview script before you talk to customers, **summarize** extracts insights after you've done the interview.

## Invocation

```text
/interview prep Onboarding experience for enterprise users
/interview summarize [paste transcript or upload file]
/interview                    # asks which mode you need
```

## Modes

---

### Prep mode

Create a structured interview script tailored to your research question.

#### Workflow

**Step 1: Understand the research goal**

Ask the user:
- What are you trying to learn? (specific research question)
- Who are you interviewing? (segment, role, relationship to product)
- How much time do you have? (15 min, 30 min, 60 min)
- What decisions will this research inform?

**Step 2: Generate interview script**

Apply the **interview-script** skill:

- Follow "The Mom Test" principles – ask about their life, not your idea
- No leading questions, no pitching, focus on past behavior and real situations
- Structure the script in sections:

```text
## Interview script: [research topic]

**Research Question**: [what we're trying to learn]
**Target Participant**: [who]
**Duration**: [X] minutes

### Warm-up (3-5 min)
[Rapport-building questions, role/context understanding]

### Core exploration (15-40 min)
[JTBD probing, past behavior, current workflow, pain points]
- For each question: the question + why you're asking it + follow-up prompts

### Specific topics (5-10 min)
[Targeted questions about specific features or concepts – if needed]

### Wrap-up (3-5 min)
[Open-ended closing, referral ask, next steps]

### Note-taking template
[Pre-formatted template to capture insights during the interview]

### Red flags to watch for
[Signs the conversation is going off-track or the participant is being polite rather than honest]
```

**Step 3: Customize and review**

- Adjust question count to fit the time slot
- Add probing questions for specific hypotheses the user wants to test
- Flag questions that might lead the witness
- Offer a printable version (markdown file saved to workspace)

---

### Summarize mode

Transform an interview transcript into structured, actionable insights.

#### Workflow

**Step 1: Accept the transcript**

Accept in any format:
- **Pasted text**: Raw transcript or notes
- **Uploaded file**: Document, text file, or meeting notes export
- **Audio summary**: If the user describes what was said (not a full transcript)

If the input is rough notes rather than a full transcript, work with what's available and note the limitations.

**Step 2: Extract and structure**

Apply the **summarize-interview** skill:

Parse the transcript to identify:
- **Participant profile**: Role, experience level, segment, context
- **Jobs to Be Done**: What the participant is trying to accomplish
- **Current workflow**: How they solve the problem today
- **Pain points**: Frustrations, workarounds, time sinks
- **Satisfaction signals**: What works well, moments of delight
- **Quotes**: Verbatim quotes that capture key insights (with timestamps if available)
- **Surprises**: Anything unexpected or that contradicts assumptions
- **Feature reactions**: If specific features/concepts were discussed, capture reactions

**Step 3: Generate interview summary**

```text
## Interview summary

**Participant**: [anonymized profile – role, segment, experience]
**Date**: [if known]
**Duration**: [if known]
**Interviewer**: [if known]

### Key insights
1. **[Insight]** – [supporting evidence/quote]
2. **[Insight]** – [supporting evidence/quote]
3. ...

### Jobs to be done
- **Primary JTBD**: [When I..., I want to..., so I can...]
- **Related JTBDs**: [additional jobs]

### Current workflow
[How the participant currently solves the problem, step by step]

### Pain points
| Pain Point | Severity | Quote |
| --- | --- | --- |

### Satisfaction signals
| What Works | Why | Quote |
| --- | --- | --- |

### Notable quotes
> "[quote]" – on [topic]

### Assumptions validated / invalidated
| Assumption | Status | Evidence |
| --- | --- | --- |

### Action items
- [ ] [Follow-up action from this interview]
- [ ] [Research question to explore further]

### Raw notes
[If helpful, include annotated key sections]
```

Save the summary as a markdown file.

**Step 4: Connect to broader research**

Offer:
- "Want me to **compare this with other interview summaries** you've done?"
- "Should I **update assumptions** based on what this participant said?"
- "Want me to **extract personas** from multiple interviews?"

## Notes

- In prep mode, always include "why you're asking" annotations – they help the interviewer stay on track
- In summarize mode, distinguish between what the participant *said* vs. what they *did* (behavioral > stated)
- Flag contradictions within the same interview (says one thing, describes doing another)
- If the transcript mentions competitor products, capture competitive intelligence
- For summarize mode, if multiple transcripts are provided, synthesize across them with cross-participant patterns
