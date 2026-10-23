---
description: Brainstorm marketing ideas, positioning, value prop statements, and product names with the Go-to-market helper – creative marketing toolkit
mode: agent
---

# /market-product -- Marketing creative toolkit

Generate creative marketing assets: campaign ideas, positioning statements, value prop copy, and product naming options. All in one workflow or pick specific modules.

Use this prompt with the Go-to-market helper.

## Invocation

```text
/market-product AI scheduling tool for remote teams – need launch marketing
/market-product Help me position our analytics product against enterprise competitors
/market-product We need a name for our new developer productivity feature
```

## Workflow

### Step 1: Understand the marketing need

Ask:
- What is the product? Target audience?
- What do you need? (full marketing toolkit, or specific: ideas, positioning, naming, copy)
- What's the context? (launch, rebrand, campaign, competitive repositioning)
- Any existing brand guidelines or tone of voice?

### Step 2: Generate based on need

**Marketing Ideas** – apply **marketing-ideas** skill:
- 5 creative, cost-effective campaign ideas
- Each with: channel, messaging angle, engagement rationale, estimated effort
- Mix of quick wins and bigger bets

**Positioning** – apply **positioning-ideas** skill:
- Identify top 5 competitors for positioning context
- Generate 3-5 positioning statements differentiated from each
- Include rationale for each positioning angle

**Value Proposition Statements** – apply **value-prop-statements** skill:
- Generate copy for marketing, sales, and onboarding contexts
- Segment-specific variations
- Short (tagline), medium (elevator pitch), and long (landing page) versions

**Product Naming** – apply **product-name** skill:
- Brainstorm 5 unique, memorable names
- Each with: rationale, brand alignment, domain availability notes
- Check for unintended meanings or conflicts

### Step 3: Generate output

```text
## Marketing toolkit: [product]

**Date**: [today]
**Context**: [launch / rebrand / campaign / etc.]

### Marketing campaign ideas
| # | Idea | Channel | Effort | Expected Impact |
| --- | --- | --- | --- | --- |

### Positioning options
| # | Positioning | vs Competitor | Strength | Risk |
| --- | --- | --- | --- | --- |

**Recommended positioning**: [which and why]

### Value prop copy
**Tagline**: [one line]
**Elevator pitch**: [2-3 sentences]
**Landing page hero**: [headline + subheading]
**Sales one-liner**: [for sales conversations]

### Product name options (if requested)
| # | Name | Rationale | Domain | Risk |
| --- | --- | --- | --- | --- |

### Messaging matrix
| Audience | Key Message | Proof Point | CTA |
|----------|-----------|------------|-----|
```

Save as markdown.

### Step 4: Offer next steps

- "Want me to **draft full marketing content** (blog post, email, social)?"
- "Should I **define the North Star metric** for this campaign?"
- "Want me to **create a competitive battlecard** to support positioning?"
- "Should I **plan the full launch**?"

## Notes

- Positioning should be tested, not assumed – recommend A/B testing headlines
- Value prop copy should use the customer's language, not internal jargon
- Marketing ideas should be specific and actionable, not generic ("use social media")
- Product names should be checked for trademark conflicts before committing
- Always tie marketing back to customer JTBD, not product features
