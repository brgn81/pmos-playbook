---
applyTo: "**/*.md"
description: "Canonical discovery conventions: assumption categories, quadrant names and the assumption statement pattern"
---

# Discovery conventions

## Assumption categories

Always use exactly these five categories – no others:

| Category | Emoji | Color | Meaning |
| --- | --- | --- | --- |
| **Customer Value** | 💶 | `#EBC3C3` | Users want this; it solves a real problem |
| **Usability** | 🧐 | `#E8DF88` | Users can understand and use it |
| **Feasibility** | ⚒️ | `#A4E2D2` | The team can build and operate it |
| **Business viability** | 💼 | `#B7CBE8` | It fits the business model and operating constraints |
| **Ethics** | 🕊️ | `#D9D9D9` | It is responsible and appropriate to build |

## Assumption map quadrants

Use **importance × evidence** axes – not uncertainty wording:

| Importance ↕ \ Evidence → | Low evidence | High evidence |
| --- | --- | --- |
| **High importance** | **Experiment** | **Plan to build** |
| **Low importance** | **Defer for now** | **Defer** |

- Vertical axis: **High importance** (up) / **Low importance** (down)
- Horizontal axis: **High evidence** (right) / **Low evidence** (left)
- Default priority: **Experiment** quadrant first, then **Plan to build**

## Standard assumption statement pattern

Use this heading and blockquote format for every assumption:

```markdown
**Assumption N:** [short title] (emoji Category)

>We assume that _[actor]_<br>
>will _[behavior]_<br>
>because _[reason]_,<br>
>resulting in _[outcome]_.

<details>
<summary>Assumption details</summary>

- **User outcome:** ...
- **Business outcome:** ...
- **Importance:** High / Medium / Low
- **Evidence:** High / Medium / Low
- **Quadrant:** Experiment / Plan to build / Defer / Defer for now
- **Priority:** High / Medium / Low
- **Suggested test:** [experiment reference or short description]

</details>
<br>
```

## Standard experiment format

Present each experiment as a 2-column table with no header row:

```markdown
| **We believe that...** | [the assumptions being tested] |
| **To verify it, we will...** | [the concrete experiment action] |
| **And measure...** | [the specific metric or signal] |
| **We are right if...** | [the success threshold] |
```
