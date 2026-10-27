---
description: Walk through an idea template question by question – structured interview with clarifying questions, template switching, and file updates
mode: agent
---

# /fill-idea – Template-guided idea interview

Walk through an idea item's template questions one at a time. For each question: read hints, ask clarifying questions, propose an answer, confirm, and write to file.

Read the product profile if the workspace has one (the folders of `pmos where --pmos-type product-profile --json`), and look up personas there and in the market research folder.

## Invocation

```text
/fill-idea <reference>
/fill-idea                   # asks which idea, then finds the file
```

## Prerequisites

An idea file must already exist in the folder of `pmos where --pmos-type idea --json`. If it does not exist, use `/start-idea` first.

## Workflow

### Step 1: Load the idea file

1. Read the item reference (from the invocation, or ask): an issue key, a page id, a URL or a title, depending on the configured platform. Never validate its format.
2. Find the idea file in the folder of `pmos where --pmos-type idea --json` by `item_id` or title. If the folder is read-only (`writable` is false in `pmos types --json`), stop: the idea cannot be written here.
3. Read the file.
4. Identify the current position (first section with placeholder content or where user left off)
5. Announce: "Starting from: **[question text]**. Ready?"

### Step 2: For each template question (loop)

For every unanswered question in template order:

#### 2a. Read the hint section

- Load the hint from the `<details><summary>Hints for this question</summary>` block in the template
- Use hint guidance to inform your clarifying questions (but never copy hints into answers)

#### 2b. Ask the question

- Present the template question to the user
- Wait for their initial answer

#### 2c. Clarifying questions (2-5 follow-ups)

After the user's initial answer:

- Start with outcomes and goals at a high level
- Ask about context, rationale, and constraints
- Explore alternatives or trade-offs
- Request concrete examples where useful
- Ask for technical specificity only when needed to define explicit solution scope
- If hints reference personas, proactively look up the personas file and suggest matches
- Continue until the user signals they're done with this section

#### 2d. Propose the answer

- Formulate a comprehensive, well-structured answer combining all gathered information
- Structure using paragraphs and bullet points for readability
- Present the proposed answer
- Ask: "Should I add this to the idea file, or would you like me to adjust anything?"

#### 2e. Write to file

- Only after user confirmation, update the relevant section
- Content goes AFTER the `</details><br>` tag, never before it
- Preserve all hint sections (they're part of the template)
- Show the updated section to confirm

#### 2f. Advance

- Suggest: "Ready to move to the next question: **[next question]**?"
- Wait for explicit confirmation (`next`, `continue`, `yes`, `proceed`)
- Never auto-advance

### Step 3: Template switching checkpoint

**After completing all questions in "💡Idea capture & context"** and before moving to "🎯Problem & solution framing":

1. Ask: "Does this idea meet the small idea criteria (no risks, implementation less than 4h)?"
2. If **yes**: load the small idea template of the Playbook (`idea-small`), replace sections below "💡Idea capture & context," continue with simplified questions
3. If **no** or **unsure**: continue with standard template

Rules:
- Never infer or guess whether an idea is small
- Template conversion only happens once, at this checkpoint
- Preserve the "💡Idea capture & context" section already completed

### Step 4: Stage 3 handoff checkpoint

**Before stage 3 assumptions work** (non-small ideas only):

Suggest: "For impact mapping, assumption formulation, and experiment design, you can use `/discover` (option c) which is optimized for this work. Continue here, or switch to `/discover`?"

## Writing rules

- Write only what the user explicitly states
- Never add assumed meaning, persona information, or context from reference files unless user confirms
- Prioritize the five dimensions: Customer Value, Usability, Feasibility, Business viability, Ethics
- Keep implementation detail out of the main narrative unless explicitly defined as solution scope
- Detailed technical suggestions belong only inside `<details><summary>Implementation ideas</summary> ... </details>`
- If a point is undecided, insert: `TBD – pending user clarification`
- Use highly structured formatting (paragraphs, bullet points, numbered lists)

## Navigation

- User can jump to any section: "Which section would you like to work on?"
- User can review: "show the draft" (entire file) or "show only [section]"
- User contradicts previous answer: "This differs from your earlier answer. Should I update the previous section?"
