---
description: Create an impact map for any product or idea – traces the value chain from deliverables to behavioral outcomes to business goal
mode: agent
---

# /impact-map – Impact map

Create an impact map that makes the solution's value chain explicit: from deliverables to behavioral outcomes to business goal. Every actor–outcome connection implies beliefs about user behavior and business impact that have not yet been validated – use the output as a starting point for assumption identification.

## Invocation

```text
/impact-map <idea reference>
/impact-map Smart notification system for our SaaS tool
/impact-map                    # asks what you're mapping
```

## Mode detection

- **Idea mode**: user provides the reference or title of an idea → load the idea item as context, offer save options
- **Generic mode**: any other product or feature description → proceed without an idea file, save to the folder of `pmos where --pmos-type draft --json`

---

## Workflow

### Step 1: Load context

**Idea mode (idea provided):**
1. Resolve the folder with `pmos where --pmos-type idea --json` and find the idea there by `item_id` or title. A type that is not mapped returns nothing: say so, do not guess a path.
2. If the file is not there yet, pull it: `pmos pull <type> <reference> --json`, where `<type>` is the `type` of the `pmos where` result.
3. If the idea cannot be found: "No idea item found for <reference>. Please create the idea first using the Idea helper." → stop
4. Extract from the idea: title, problem description, target users, and any solution framing as starting context

**Generic mode:**
- If no product or feature was provided in the invocation: ask "What product, feature, or concept should we map?"

---

### Step 2: Gather inputs

Ask the following questions conversationally. Accept partial answers and let the user provide more later.

1. **Business goal**: What measurable outcome is the organization pursuing? (e.g. increase renewal rate, reduce churn, grow activation)
2. **Actors**: Whose behavior must change to reach this goal? (internal users, external customers, partners – not the team itself)
3. **Outcomes**: For each actor: what observable behavioral change is needed?
4. **Deliverables**: What does the team build or produce to enable each outcome?

In Idea mode: propose initial answers from the idea file content and ask the user to confirm or adjust – never invent content beyond what the idea file states.

---

### Step 3: Present the impact map

Format the map as a markdown table with a business goal statement above it:

> **🟡 Business goal:** [measurable outcome the organization is pursuing]

| 🟢 Actor | 🔵 Outcome (behavioral change) | 🔴 Deliverable |
| --- | --- | --- |
| [who changes behavior] | [observable behavior change] | [what we build to enable it] |

_Last updated: YYYY-MM-DD_

**Rules:**
- 🟡 **Business goal** – one top-level goal, measurable if possible
- 🟢 **Actors** – people whose behavior must change; not the building team
- 🔵 **Outcomes** – observable behavioral changes, expressed as actions (not features)
- 🔴 **Deliverables** – outputs the team produces to enable the behavioral outcome
- Multiple actors and outcomes per business goal are normal; each row is one actor–outcome–deliverable combination

Ask: "Does this look right? Any rows to add, change, or remove?"

---

### Step 4: Save the impact map

**Idea mode:**

> "Where would you like to save this impact map?
> - **(a) Discovery page** – recommended for long-term reference
> - **(b) Idea file** – adds it to the 'How does this solution create impact?' section
> - **(c) Draft file only** – writes to the draft folder"

**(a) Discovery page:**
- Resolve the folder with `pmos where --pmos-type discovery --json` and find the linked page there; if it is not local yet, pull it with `pmos pull <type> <reference> --json`
- Add the map under `### Impact map` inside `## Outcomes, assumptions and experiments`
- Add `_Last updated: YYYY-MM-DD_` below the table
- Never write into a read-only folder (`writable` is false in `pmos types --json`). Pushing the page (`/push`) is a separate step for the user.

**(b) Idea file:**
- Replace the empty body of "How does this solution create impact?" with the impact map table
- Add `_Last updated: YYYY-MM-DD_` below the table

**(c) Draft file:**
- Write `impact-map-[slug].md` to the folder of `pmos where --pmos-type draft --json`
- Confirm the path

**Generic mode:**
- Save to `impact-map-[slug].md` in the folder of `pmos where --pmos-type draft --json`
- Confirm and offer to copy

---

### Step 5: Offer next steps

- "Every actor–outcome connection implies an assumption we haven't validated yet. Want to **identify assumptions** from this map?" → use `/discover` and select option (c) for product ideas, or option (b) for generic
- "Want to **design experiments** to test the riskiest assumptions?"

## Notes

- Impact maps evolve over time – always include `_Last updated: YYYY-MM-DD_` when saving
- Actors are people whose behavior changes, not abstract entities or systems
- Outcomes describe behavioral change, not outputs – avoid feature-describing language in the Outcome column
- Never fabricate content; in Idea mode propose only what the idea file states

