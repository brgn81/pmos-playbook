---
description: Conduct a five-dimension risk assessment of a product idea – customer value, usability, feasibility, business viability, ethics
mode: agent
---

# /risk-assessment – Five-dimension risk assessment

Assess a product idea against five risk dimensions. For each dimension, answer trigger questions using the idea file and linked sources (experiments, minutes, insights). Add follow-up questions where information is missing. Append the completed assessment to the idea file footer.

## Invocation

```text
/risk-assessment <idea reference>
/risk-assessment               # asks which idea
```

---

## Workflow

### Step 1: Load the idea file

- If no idea was named in the invocation: ask "Which idea should I assess? (reference or title)"
- Resolve the folder with `pmos where --pmos-type idea --json` and find the idea there by `item_id` or title. A type that is not mapped returns nothing: say so, do not guess a path.
- If the file is not there yet, pull it: `pmos pull <type> <reference> --json`, where `<type>` is the `type` of the `pmos where` result.
- If the idea cannot be found: "No idea item found for <reference>. Please create the idea first using the Idea helper." → stop

### Step 2: Confirm start

Show the idea title and ask:

> "Should I start the risk assessment for **[idea title]**?"

Do not proceed without explicit user confirmation.

---

### Step 3: Assess each dimension

For each of the five dimensions in sequence:

1. Search the idea file for answers to the trigger questions.
2. Review linked sources: experiments on the linked discovery page, minutes in the folder of `pmos where --pmos-type minute --json`, insights in the folder of `pmos where --pmos-type insight --json`. A type that is not mapped returns nothing: say so and continue without it.
3. Draft answers with inline source citations: `[experiment: name]`, `[minutes: 2026-01-08]`, `[insight: file-name]`.
4. If key information is missing, add a follow-up question using the Questions block format from `.claude/rules/question-feedback-handler.md`.
5. Present the drafted answers and ask: "Are these answers correct, or would you like adjustments?"
6. After confirmation, continue to the next dimension.

#### Dimension 1: Customer value

> Does this idea solve a real problem? Will users want it?

Trigger questions:
- What customer problem is this solving?
- What evidence do we have that this is a real, painful problem?
- Have we validated demand with real users?
- How many users are affected, and how frequently?

#### Dimension 2: Usability

> Can users figure it out? Is the cognitive load manageable?

Trigger questions:
- Is the user journey clear and low-friction?
- Have we tested the concept or prototype with real users?
- What onboarding or explanation does the user need?
- Are there accessibility concerns?

#### Dimension 3: Feasibility

> Can we build and operate this?

Trigger questions:
- What are the key technical challenges?
- Do we have the skills and infrastructure required?
- Are there relevant integrations or dependencies?
- What are the operational implications (monitoring, support, scaling)?

#### Dimension 4: Business viability

> Does this work for your company's business model and operating constraints?

Trigger questions:
- How does this idea contribute to business goals (revenue, retention, activation)?
- Are there regulatory or contractual constraints?
- What is the estimated implementation cost vs. expected return?
- Does this fit the current product strategy and roadmap?

#### Dimension 5: Ethics

> Should we build this at all?

Trigger questions:
- Does this idea respect user privacy and data rights?
- Could this be used in a way that harms users or third parties?
- Are there fairness, bias, or inclusion concerns?
- Are we transparent with users about what this does?

---

### Step 4: Append to idea file

After all five dimensions are confirmed, ask:

> "Should I append the completed risk assessment to the idea file?"

**Only append after explicit user confirmation.**

Format:

```markdown
---

## Risk assessment

_Assessed: YYYY-MM-DD_

### Customer value

[answers and evidence]

### Usability

[answers and evidence]

### Feasibility

[answers and evidence]

### Business viability

[answers and evidence]

### Ethics

[answers and evidence]
```

Append to the footer of the idea file. Do not modify any other section. If the idea folder is read-only (`writable` is false in `pmos types --json`), do not write: present the assessment in chat and say where the user can add it upstream (`url` in the frontmatter).

---

## Operating rules

- Never start an assessment without explicit user confirmation (step 2)
- Never modify sections outside the footer
- Never fabricate evidence – cite only what is explicitly found in the idea file or linked sources
- If no linked sources are found for a dimension, state "No evidence found" and add a follow-up question
- Follow `.claude/rules/question-feedback-handler.md` for all follow-up question and feedback block formatting
