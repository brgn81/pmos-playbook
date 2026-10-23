---
description: Map stakeholders on a Power × Interest grid and create a tailored communication plan
mode: agent
---

# /stakeholder-map -- Stakeholder mapping & communication plan

Identify all stakeholders for a project, map them by influence and interest, and generate a communication plan that ensures the right people get the right information at the right time.

## Invocation

```text
/stakeholder-map New analytics platform launch
/stakeholder-map Pricing model change affecting all customers
/stakeholder-map [upload a project brief or org chart]
```

## Workflow

### Step 1: Understand the initiative

Ask:
- What is the project or initiative?
- What phase is it in? (planning, building, launching, post-launch)
- Who are the obvious stakeholders you already know about?
- Are there any politically sensitive dynamics to be aware of?

### Step 2: Identify stakeholders

Brainstorm stakeholders the user might not have considered:
- **Internal**: Engineering, Design, QA, Data, Legal, Finance, Marketing, Sales, Support, Leadership
- **External**: Customers, partners, vendors, regulators, board members
- **Often missed**: Adjacent teams, on-call engineers, customer success, documentation team

### Step 3: Map to Power × Interest grid

Apply the **stakeholder-map** skill:

Place each stakeholder in a quadrant:

```text
                    HIGH INTEREST
                         │
    KEEP SATISFIED       │      MANAGE CLOSELY
    (High Power,         │      (High Power,
     Low Interest)       │       High Interest)
                         │
   ──────────────────────┼──────────────────────
                         │
    MONITOR              │      KEEP INFORMED
    (Low Power,          │      (Low Power,
     Low Interest)       │       High Interest)
                         │
                    LOW INTEREST
```

### Step 4: Generate communication plan

```text
## Stakeholder map: [initiative]

### Stakeholder grid
| Stakeholder | Role | Power | Interest | Quadrant | Stance |
| --- | --- | --- | --- | --- | --- |

### Communication plan

#### Manage closely (High Power, High Interest)
| Stakeholder | Channel | Frequency | Content | Owner |
| --- | --- | --- | --- | --- |

#### Keep satisfied (high power, low interest)
| Stakeholder | Channel | Frequency | Content | Owner |
| --- | --- | --- | --- | --- |

#### Keep informed (low power, high interest)
| Stakeholder | Channel | Frequency | Content | Owner |
| --- | --- | --- | --- | --- |

#### Monitor (Low Power, Low Interest)
[Minimal communication – include in broad updates only]

### Potential conflicts
[Where stakeholder interests may clash – with mitigation strategies]

### Escalation path
[Who to go to when decisions are blocked]

### RACI matrix
| Decision Area | Responsible | Accountable | Consulted | Informed |
|--------------|-------------|-------------|-----------|----------|
```

Save as markdown.

### Step 5: Offer next steps

- "Want me to **draft the first stakeholder update** for the 'Manage Closely' group?"
- "Should I **create a meeting prep brief** for key stakeholder conversations?"
- "Want me to **set up a communication cadence** as a recurring checklist?"

## Notes

- The "Manage Closely" quadrant is where PMs spend most of their political capital – get these relationships right
- "Stance" (supportive, neutral, resistant) helps prioritize where to invest relationship-building effort
- Don't forget downstream stakeholders: support, docs, and sales enablement teams are often surprised by launches
- Update the map as the project evolves – stakeholder interest shifts with project phase
