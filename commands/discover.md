---
description: Run a full product discovery cycle – opportunity discovery to find customer problems worth solving, or solution discovery to stress-test an idea you already have
agent: agent
---

# /discover -- Full discovery cycle

Two discovery modes in one command. Always start with a question to determine whether the user is exploring customer problems or validating an existing idea, then route to the matching workflow. If the user's answer is unclear or incomplete, ask a clarifying follow-up before proceeding.

## Invocation

```text
/discover Retention drop in the onboarding flow
/discover Smart notification system for our project management tool
/discover                    # asks what you're discovering
```

## Forking question

At the start of every `/discover` session, ask:

> "Are you exploring **customer problems** to find what's worth solving – or do you already have an idea and want to stress-test it?
>
> (a) **Opportunity discovery** – I want to understand customer problems before committing to a solution
> (b) **Solution discovery** – I have an idea and want to validate it against real customer needs
> (c) **Idea deep-dive** – I have an existing idea and want to do deep assumption and experiment work on it"

- If the user answers (a) or describes exploring a problem space → follow **Section A: Opportunity discovery** below
- If the user answers (b) or describes a specific idea or feature → follow **Section B: Solution discovery** below
- If the user answers (c) or names an existing idea (a reference or its title) → follow **Section C: Idea deep-dive** below
- If the user's intent is unclear → ask: "Do you already have a specific idea in mind, or are you still figuring out what problem to solve?" then route based on the answer

---

## A. Opportunity discovery

Explore the customer's world to surface and rank problems worth solving. Output is an opportunity map, not a solution.

### Interaction discipline

- Let the user know upfront: this is a 15–30 minute structured workflow
- At each checkpoint, the user can redirect, skip, or go deeper
- If the user has research data, pull insights from it before brainstorming

### Step 1: Understand the discovery context

Determine whether this is:
- **Existing product** – continuous discovery on a known product with real users
- **New product** – initial discovery for a concept without validated demand

Ask the user:
- What are you exploring? (product idea, feature area, opportunity space)
- What do you already know? (prior research, customer feedback, data)
- What decisions will this discovery inform? (build/kill, prioritize, pivot)

Accept context from uploaded files (research, PRDs, transcripts, data), links, or conversation. If the user provides interview transcripts, apply the **summarize-interview** skill to extract key insights first.

### Step 2: Brainstorm ideas (divergent phase)

Apply the **brainstorm-ideas-existing** or **brainstorm-ideas-new** skill:

- Generate ideas from PM, Designer, and Engineer perspectives
- Present the top 10 ideas with brief rationale
- Ask the user to select 3–5 ideas to carry forward, or accept all

**Checkpoint:** "Here are 10 ideas. Which ones should we stress-test? Pick 3–5, or I can carry all forward."

### Step 3: Identify assumptions (critical thinking phase)

For each selected idea, apply the **identify-assumptions-existing** or **identify-assumptions-new** skill:

- Surface assumptions across five canonical risk categories:
  - **Customer value:** Will users want this? Does it solve a real problem?
  - **Usability:** Can users figure it out?
  - **Feasibility:** Can we build it?
  - **Business viability:** Does the business case work? Can we sell, launch, scale, and support it?
  - **Ethics:** Should we do it at all?
- Use devil's advocate multi-perspective analysis
- Compile a master list of all assumptions across all ideas

### Step 4: Prioritize assumptions (focus phase)

Apply the **prioritize-assumptions** skill:

- Map assumptions on an importance × evidence matrix
- Identify the "leap of faith" assumptions – high importance, low evidence
- Rank assumptions by test priority
- Group related assumptions that can be tested together

**Checkpoint:** "Here are your riskiest assumptions. Which ones feel most critical to validate first?"

### Step 5: Design experiments (validation phase)

Apply the **brainstorm-experiments-existing** or **brainstorm-experiments-new** skill:

- Design 1–2 experiments per critical assumption
- For existing products: A/B tests, fake doors, prototypes, user tests, data analysis
- For new products: XYZ hypotheses, pretotypes, landing pages, concierge MVPs
- Include success criteria, timeline, and effort for each
- Sequence experiments by dependency and effort

### Step 6: Create discovery plan

Compile everything into a discovery plan document:

```markdown
## Discovery plan: [topic]

**Date**: [today]
**Product stage**: [existing/new]
**Discovery question**: [what we're trying to learn]

### Ideas explored
[Summary of brainstormed ideas with brief descriptions]

### Selected ideas for validation
[3–5 ideas carried forward with rationale]

### Critical assumptions
| # | Assumption | Category | Importance | Evidence | Priority |
| --- | --- | --- | --- | --- | --- |

### Validation experiments
| # | Tests assumption | Method | Success criteria | Effort | Timeline |
| --- | --- | --- | --- | --- | --- |

### Experiment details
[For each experiment: hypothesis, setup, measurement, decision criteria]

### Discovery timeline
Week 1: [experiments]
Week 2: [experiments]
Week 3: [analysis and decision]

### Decision framework
- If [experiment] succeeds → proceed to [next step]
- If [experiment] fails → [pivot/kill/investigate further]
```

Save the plan as a markdown file to the user's workspace.

### Step 7: Offer next steps

- "Want me to **move into solution discovery** to stress-test the top opportunity?"
- "Should I **design an interview script** to supplement these experiments?" *(uses the **interview-script** skill)*
- "Want me to **set up metrics** to track the experiments?" *(uses the **metrics-dashboard** skill)*
- "Should I **estimate effort** and create user stories for the MVP?"

---

## B. Solution discovery

Stress-test a specific idea against real customer needs, building depth incrementally. Always assumes an existing product context. Output is a pre-filled idea work-item.

### Interaction discipline

**Pacing and sequencing:** Ask one question at a time in phase order. Let the user know upfront this is a 20–40 minute workflow. Confirm at each stage gate before proceeding to the next phase.

**Content integrity:** Never auto-fill answers or fabricate assumptions, personas, or insights. Capture open questions explicitly rather than inventing content. Accept context from uploaded files, pasted transcripts, data, or links at any point.

### Phase 1: Discovery framing

The goal of solution discovery is always the same: explore the idea, surface the riskiest assumptions, and guide toward a **build / stay in discovery / kill** decision. Do not ask the user about desired outcomes.

Ask one question:

1. "What idea or solution are you exploring? (feature concept, proposed capability, specific solution)"

Accept any files, links, or pasted research as additional context before proceeding. If the user provides interview transcripts, apply the **summarize-interview** skill to extract key insights before moving to Phase 1b.

---

### Phase 1b: Anchor to an idea item (optional)

Before diving into the problem space, offer to anchor this discovery to an idea item. Ask:

> "Would you like to anchor this discovery to an **idea item** now so we can track it?
>
> (a) **Yes – create new** – I'll scaffold the idea from the template
> (b) **Yes – link existing** – I already have an idea, just link it
> (c) **Skip for now** – I'll save it at the end of the discovery session"

**If (a) – create new:**
- Resolve the folder with `pmos where --pmos-type idea --json`. A type that is not mapped returns nothing: say so and keep the outputs in the folder of `pmos where --pmos-type draft --json` instead.
- If the idea type is synced from a platform (`platform` is not empty in `pmos types --json`), the item belongs to that platform: ask the user to create it there, then pull it with `pmos pull <type> <reference> --json`, where `<type>` is the `type` of the `pmos where` result. If that folder is read-only (`writable` is false), never write into it.
- Otherwise scaffold a new idea file in that folder from the idea template of the Playbook, with the title from Phase 1.
- Leave all content sections as blank placeholders – do not invent content.
- Confirm: "Idea file created at `<path>`. All discovery outputs will be merged into it."
- Continue to Phase 2

**If (b) – link existing:**
- Ask for the reference (whatever the idea's platform accepts; never validate its format) or the title
- Look for a file with that `item_id` or title in the idea folder
  - If yes: confirm the file and proceed; merge discovery outputs into it during Phase 6
  - If no: pull it with `pmos pull <type> <reference> --json`
- Continue to Phase 2

**If (c) – skip:**
- Note the idea title as a working label
- Continue to Phase 2 – the user can save the idea in Phase 7

---

### Phase 2: Problem space

Work through these four questions **one at a time**, in order. Do not move to the next question until the user has answered the current one. If the user doesn't have an answer, capture it as an open question and continue – never invent content.

1. **What problem are we trying to solve, and why is it important?**
   *(Include evidence from user research, analytics, or customer feedback if available.)*

2. **Who is the target customer or persona?**
   *(Identify the specific customer segment this discovery is for.)*

3. **How are customers behaving today?**
   *(Current workarounds, friction points, behavior patterns – check analytics and interviews.)*

4. **What change in customer behavior would indicate success?**
   *(Define the desired outcome as a behavioral change, per Seiden's definition of outcomes.)*

**Stage gate:** "The problem space is now complete. Ready to move to solution ideation?"

---

### Phase 3: Solution ideation

Apply the **brainstorm-ideas-existing** skill. Grounded in the problem-space answers, generate solution ideas:

- Produce "How might we" ideas from **PM, Designer, and Engineer** perspectives
- For each idea, note **1–2 obvious alternatives** to prevent tunnel vision (Torres' compare & contrast principle)
- Present the **top 5–7 ideas** with brief rationale

**Checkpoint:** "Here are the top ideas. Which 2–3 should we stress-test? Or I can carry all forward."

---

### Phase 4: Assumptions mapping

Apply the **identify-assumptions-existing** skill for each selected idea, then apply the **prioritize-assumptions** skill to rank them.

For each selected idea, surface assumptions across five categories – work through them **one category at a time**:

- **Customer value:** Will users want this? Does it solve a real problem?
- **Usability:** Can users figure it out without help?
- **Feasibility:** Can we actually build it?
- **Business viability:** Does the business case hold? Can we sell, launch, scale, and support it?
- **Ethics:** Should we do it at all?

Map assumptions on an **importance × evidence** matrix using these quadrant names:

- **Experiment** (high importance, low evidence) – leap of faith; test first
- **Plan to build** (high importance, high evidence) – proceed
- **Defer** (low importance, high evidence) – park in backlog
- **Defer for now** (low importance, low evidence) – park in backlog

**Stage gate:** "Here are the riskiest assumptions. Which feel most critical to validate first? Ready to design experiments?"

---

### Phase 5: Experiment design

Apply the **brainstorm-experiments-existing** skill. For each leap-of-faith assumption, design 1–2 lean experiments:

- Methods: A/B tests, fake doors, prototypes, user tests, data analysis, concierge MVPs
- For each experiment define:
  - **Hypothesis:** We believe [actor] will [behavior] because [reason], resulting in [outcome]
  - **Method:** How we'll test it
  - **Success criteria:** What result confirms or invalidates the assumption
  - **Effort:** Time and resources required
  - **Timeline:** When to run it
- Sequence experiments by dependency and effort (cheapest signal first)

---

### Phase 6: Create discovery plan

Compile everything into a discovery plan using the **idea template structure**. Leave any sections that were not explored during this session as blank placeholders – do not invent content for them.

```markdown
## 💡 Idea capture & context

### What is this idea about?
[Summary from Phase 1 – the opportunity and topic]

### Where did this idea come from?
[Discovery framing: outcome, decision context, any linked evidence or files]

---

## 🎯 Problem & solution framing

### Problem space

#### What problem are we trying to solve, and why is it important?
[From Phase 2]

#### Who is the target customer or persona?
[From Phase 2]

#### How are customers behaving today?
[From Phase 2]

#### What change in customer behavior would indicate success?
[From Phase 2]

### Solution space

#### How might we solve this problem?
[Top selected ideas from Phase 3, as "How might we" statements]

#### What alternative solutions could we consider before picking one?
[Alternatives noted during Phase 3]

#### How does this solution deliver value compared to alternatives?
[Leave blank if not yet explored]

#### How does this solution fit into the bigger product vision or roadmap?
[Leave blank if not yet explored]

---

## 📝 Assumptions, risks & validation

### What assumptions must be true for this idea to succeed?
[Numbered list from Phase 4: Assumption N: short title (Category)]

### Which assumptions are most risky?
[Leap-of-faith assumptions from the "Experiment" quadrant of the importance × evidence map]

### How will we test our riskiest assumptions?
[Experiment designs from Phase 5]

### What did we learn from our experiments?
[Leave blank – to be filled as experiments run]

### What decision will we make based on this evidence?
[Leave blank – to be filled after experiments]
```

---

### Phase 7: Save as idea item

Offer to save the discovery plan as an idea item:

> "Would you like to save this as an idea item? I can:
> (a) Scaffold a new idea file from the template
> (b) Merge these discovery outputs into an existing idea – tell me which
> (c) Skip for now"

**If (a) – new idea:**

- Follow Phase 1b (a): resolve the folder, respect a synced or read-only idea type, scaffold from the Playbook idea template
- Pre-fill it with all Phase 1–5 outputs
- Never invent identity fields: `item_id`, `title` and `url` belong to the remote when the idea type is synced

**If (b) – existing idea:**

- Load the existing file from the idea folder
- Merge discovery outputs into the appropriate sections
- Do not overwrite sections that already have substantive content without asking the user

After saving, remind the user that the idea was only changed locally. Pushing it (`/push`, when the idea type can push) is a separate step the user takes.

---

### Phase 8: Offer next steps

- "Should I run an **assumption deep-dive**? If the idea has been saved as an idea item, use `/discover` option (c) to go straight to impact mapping, assumption formulation, and experiment design."
- "Should I **design an interview script** to supplement these experiments?" *(uses the **interview-script** skill)*
- "Want me to **set up metrics** to track the experiments?" *(uses the **metrics-dashboard** skill)*
- "Want me to **create user stories** for the top idea?"

---

## Notes

- The user can redirect, skip, or go deeper at any checkpoint in both modes
- If the user provides research data (transcripts, CSV, analytics), pull insights from it before brainstorming
- Discovery plans are living documents – offer to update them as experiments run
- If the user finishes opportunity discovery and wants to pursue a specific opportunity, offer to continue into solution discovery

---

## C. Idea deep-dive

Deep assumption and experiment work on an existing idea. Unlike section B (solution discovery), this section assumes a fully authored idea item and a linked discovery page already exist, and focuses entirely on assumption formulation, mapping, and experiment design.

### Entry

The user names the idea (a reference or its title), or selects option (c) at the forking question. If nothing was named: ask "Which idea should we work on? (reference or title)"

---

### Phase C1: Load idea file

1. Resolve the folder with `pmos where --pmos-type idea --json` and find the idea there by `item_id` or title. A type that is not mapped returns nothing: say so and stop.
2. If the file is not there yet, pull it: `pmos pull <type> <reference> --json`, where `<type>` is the `type` of the `pmos where` result.
3. Check its state with `pmos status <type> <reference> --json`. If it is blocked, show the guidance options to the user as `.claude/rules/sync-conflict-guidance.md` says; never pick one.
4. If the idea cannot be found: "No idea item found for <reference>. Please create the idea first using the Idea helper." → stop

---

### Phase C2: Check discovery page (guard)

- Check the idea for a linked discovery page (a mapped frontmatter field or a link in the body)
- **If a discovery page is linked:**
  - Resolve the folder with `pmos where --pmos-type discovery --json` and look for the page there by `item_id`
  - If it is not there: `pmos pull <type> <reference> --json`, with the `type` of that `pmos where` result
- **If no discovery page is linked:**
  - Stop and inform: "This idea has no linked discovery page. Detailed assumption and experiment work requires a discovery page. Please create one from the discovery template in your discovery platform and link it in the idea."
  - Do not proceed with assumption drafting until the discovery page is linked and pulled locally

---

### Phase C3: Impact map (optional)

Ask: "Would you like to create an impact map first? It helps identify assumptions by tracing the chain from deliverables to business outcomes. (yes / no)"

If yes: delegate to `/impact-map` with this idea

---

### Phase C4: Assumption formulation

**Opening:** Show any existing assumptions from the idea file. Ask: "Would you like to refine existing assumptions, add new ones, or start fresh?"

**Extract implicit assumptions:**
- Scan the idea content for statements that imply beliefs about users, behavior, or outcomes
- Distinguish between main idea narrative and `<details><summary>Implementation ideas</summary>` blocks
- Treat implementation ideas content as exploratory hypotheses, not fixed scope
- Present findings: "I found the following implicit assumptions in your idea. Let me help you formulate them explicitly."

**For each assumption (one at a time):**

1. **Formulate** using the standard pattern from `discovery-conventions.md`:
   > We assume that *[actor]*<br>
   > will *[behavior]*<br>
   > because *[reason]*,<br>
   > resulting in *[outcome]*.

2. **Split compound assumptions** if an assumption contains multiple beliefs:
   - Ask: "This contains multiple beliefs. Should I split it into Assumption X.1 and X.2?"

3. **Classify** by exactly one category (see `discovery-conventions.md` for categories and emojis). Ask: "Does this primarily relate to [suggested category]?"

4. **Link to outcomes**:
   - Ask: "What is the intended user outcome?" and "What is the related business outcome?"

5. **Place on assumption map**:
   - Assess **importance** (low / medium / high) and **evidence** (low / medium / high)
   - Assign one quadrant: **Plan to build**, **Experiment**, **Defer**, or **Defer for now**

6. **Check testability**: Can we observe the behavior? Can we falsify this belief? If not: "How could we reframe this to make it testable?"

7. **Confirm**: Present the complete assumption with category, outcomes, and quadrant. Ask: "Should I save this to the discovery page and update the idea file?"

**Persistence rules (mandatory):**
- Draft assumptions in chat first – never write to files without explicit user confirmation
- Once assumptions are finalized, save immediately before proceeding to mapping or experiments
- Save in two formats:
  - **Discovery page** (`### Assumptions` section): full template (see below)
  - **Idea file** (assumptions section): condensed – `Assumption N: short title ([emoji] [Category])`
- Numbers are static; new assumptions are added at the end; splits use sub-numbers (1.1, 1.2)
- If no linked discovery page: do not draft assumptions into files; ask user to create/link discovery first

**Full template for discovery page:**

```markdown
**Assumption [number]:** [Expressive title] ([emoji] [Category])

>We assume that *[actor]*<br>
will *[behavior]*<br>
because *[reason]*,<br>
resulting in *[outcome]*.

<details>
<summary>Assumption details</summary>

- **User outcome:** [description]
- **Business outcome:** [description]
- **Importance:** [low/medium/high]
- **Evidence:** [low/medium/high]
- **Quadrant:** [Plan to build/Experiment/Defer/Defer for now]
- **Priority:** [high/medium/low]
- **Suggested test:** [experimental approach]

</details>
<br>

---
```

---

### Phase C5: Experiment design

**Save-before-continue gate:** Verify assumptions are saved in both the discovery page and the idea file before proposing experiments. If not saved: ask "The assumptions are finalized but not saved yet. Should I save them first?"

Ask: "Would you like to design experiments to test any of these assumptions?"

If yes: "Which assumption should we focus on?" → prioritize **Experiment** quadrant (high importance + low evidence)

**For each experiment:**

1. **Use the standard template:**

   | | |
   | --- | --- |
   | We believe that... | [assumption statement] |
   | To verify it, we will... | [experimental method] |
   | And measure... | [specific metrics] |
   | We are right if... | [success criteria] |

2. **Suggest lightweight methods** matched to the assumption category:
   - **Customer Value / Usability**: customer interviews, usability tests, prototype tests, fake-door tests
   - **Feasibility**: technical spike, concierge or manual workflow
   - **Business viability**: fake-door tests, concierge MVP
   - **Ethics**: stakeholder review, privacy assessment

3. **Record the experiment:**
   - Add it to the experiments section of the discovery page, using the experiment template above, with a reference to the assumption it tests
   - PMOS does not create items on a remote platform. If the user wants a ticket for it, they create it there and you add its link to the experiment

---

### Phase C6: Error handling

| Situation | Response |
| --- | --- |
| Idea file does not exist | "No idea item found for <reference>. Please create the idea first using the Idea helper." → stop |
| No linked discovery page | "No discovery page linked. Please create one from the discovery template and link it in the idea." → stop |
| Discovery file does not exist locally | Pull it first: `pmos pull <type> <reference> --json` |
| A pull or push is blocked | Show the guidance options to the user (`.claude/rules/sync-conflict-guidance.md`) and let them choose |
| The folder of a type is not mapped | Say so; never guess a path |
| Assumptions section missing in idea file | "The idea file has no assumptions section. Should I add one?" |
| User contradicts a previous assumption | "This differs from Assumption [number]. Should I update that assumption or create a new one?" |

If any part of the workflow is ambiguous, ask for clarification before proceeding.
