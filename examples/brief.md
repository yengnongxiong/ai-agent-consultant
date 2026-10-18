# Second Cut: decision brief

**What the drafts propose:** Corvane plans to increase gross margins from 22% to 26% by launching a paid digital membership program, AI reordering, and an inside-sales push to shift contractor ordering online.

**Bottom line:** 7 of 7 load-bearing assumptions are high-risk (score 15+ of 25). Run their tests before committing budget.

## Ranked assumptions

| # | Risk | Assumption | Lens | Impact | Evidence |
|---|---|---|---|---|---|
| 1 | **20** | At least 30% of top accounts will pay $49 per month for a membership providing free next-day delivery and bulk pricing. | desirability | 5/5 | 2/5 |
| 2 | **20** | Contractor accounts prefer ordering via digital self-service over calling or visiting physical branch counters. | desirability | 5/5 | 2/5 |
| 3 | **20** | The existing four-person IT team can build an AI demand forecasting reorder model while executing their current commitments. | readiness | 4/5 | 1/5 |
| 4 | **20** | Sales reps will actively pitch Corvane Pro and drive digital adoption under current incentive structures. | readiness | 4/5 | 1/5 |
| 5 | **20** | Moving orders online and capturing membership fees will lower cost-to-serve enough to increase company gross margins by 400 basis points. | viability | 4/5 | 1/5 |
| 6 | **20** | Contractors in new metro markets will purchase memberships and supplies without Corvane having local physical branches. | desirability | 4/5 | 1/5 |
| 7 | **15** | Corvane's historical ERP order records are sufficiently clean to build automated next-week predictive reorder carts. | feasibility | 3/5 | 1/5 |

## Test plan

### 1. At least 30% of top accounts will pay $49 per month for a membership providing free next-day delivery and bulk pricing.

> "We expect at least 30% of our top 500 accounts to subscribe within six months" (growth-draft.md)

- **Test (14 days):** Have branch managers present a paid pre-order agreement for Corvane Pro to 50 top accounts with first-month billing starting at launch.
- **Measure:** Paid pre-order sign-up rate among contacted accounts
- **Go if:** \>= 25% of contacted accounts sign binding pre-commitments
- **Kill if:** \< 10% of contacted accounts sign binding pre-commitments

### 2. Contractor accounts prefer ordering via digital self-service over calling or visiting physical branch counters.

> "Corvane's contractors are ready to move ordering online" (growth-draft.md)

- **Test (14 days):** Send an email and SMS portal link to 200 active contractors offering standard ordering with 1-click checkout and same branch pickup/delivery terms.
- **Measure:** Percentage of repeat orders placed via web portal over 14 days
- **Go if:** \>= 20% of orders placed online
- **Kill if:** \< 5% of orders placed online

### 3. The existing four-person IT team can build an AI demand forecasting reorder model while executing their current commitments.

> "Start the reorder-model build with the existing IT team." (growth-draft.md)

- **Test (5 days):** Conduct a capacity sprint planning review with the IT team lead to map hours required for the AI model against ERP upgrade deliverables.
- **Measure:** Dedicated IT engineer hours available per week for reorder model build through Q3
- **Go if:** \>= 25 hours per week unallocated to ERP migration
- **Kill if:** \< 10 hours per week unallocated to ERP migration

### 4. Sales reps will actively pitch Corvane Pro and drive digital adoption under current incentive structures.

> "Reps are the fastest path to adoption because contractors trust their branch contacts." (growth-draft.md)

- **Test (7 days):** Ask 15 inside and counter sales reps across 3 branches to pitch the digital portal to 5 clients each without changing their commission policy.
- **Measure:** Percentage of asked reps who complete all 5 client outreach pitches within one week
- **Go if:** \>= 80% of reps complete outreach
- **Kill if:** \< 40% of reps complete outreach

### 5. Moving orders online and capturing membership fees will lower cost-to-serve enough to increase company gross margins by 400 basis points.

> "gross margin rises from 22% to 26% within 18 months, driven by lower cost-to-serve and Pro membership fees." (growth-draft.md)

- **Test (10 days):** Analyze transaction cost logs from the two-branch online trial to compare true fulfillment, delivery, and discounting costs of web orders versus phone/counter orders.
- **Measure:** Net margin improvement per online order relative to offline baseline
- **Go if:** \>= 300 basis points margin improvement per order
- **Kill if:** \< 100 basis points margin improvement per order

### 6. Contractors in new metro markets will purchase memberships and supplies without Corvane having local physical branches.

> "Expand to two new metro areas in the second half of the year, using Pro as the entry offer rather than opening full branches." (growth-draft.md)

- **Test (14 days):** Run targeted local search ads in the two target metros offering Corvane Pro delivery terms, directing contractors to a landing page with a sign-up call to action.
- **Measure:** Qualified contractor landing page conversion rate to membership waitlist
- **Go if:** \>= 8% conversion rate
- **Kill if:** \< 2% conversion rate

### 7. Corvane's historical ERP order records are sufficiently clean to build automated next-week predictive reorder carts.

> "Our ERP order history is clean enough to train demand forecasts that predict what each contractor will need next week." (growth-draft.md)

- **Test (7 days):** Run an automated data-profiling audit across a random sample of 5,000 historical orders from the past 24 months to identify invalid, duplicate, or mislabeled SKUs.
- **Measure:** Percentage of sampled order records with unresolved SKU or data errors
- **Go if:** \<= 5% error rate
- **Kill if:** \> 15% error rate

## Conflicts

- **The growth strategy requires hiring 20 new inside-sales reps in Q1, but corporate policy mandates a strict hiring freeze where headcount must remain flat or shrink.** "Hire 20 inside-sales reps in Q1 to call every top-500 account and sign them up for Pro." (growth-draft.md) vs. "A hiring freeze holds through the end of next fiscal year." (workforce-draft.md)
- **The growth draft asserts ERP order history is clean enough for predictive modeling, while workforce audit findings show approximately 20% of historical records have duplicate or mislabeled codes.** "Our ERP order history is clean enough to train demand forecasts that predict what each contractor will need next week." (growth-draft.md) vs. "the team has flagged duplicate and mislabeled product codes in roughly a fifth of historical orders." (workforce-draft.md)
- **The growth plan relies on sales reps to drive customer adoption of digital ordering, but sales reps are financially penalized because they earn zero commission on online orders.** "Reps are the fastest path to adoption because contractors trust their branch contacts." (growth-draft.md) vs. "Orders that customers place online earn reps nothing." (workforce-draft.md)
- **The growth thesis states contractors are ready to transition ordering online, whereas internal customer survey data shows over 80% prefer ordering via phone or branch counter.** "Corvane's contractors are ready to move ordering online, and the company that captures that shift first will own the regional market." (growth-draft.md) vs. "In last year's customer survey, 41 of 50 contractors said they prefer to order by phone or at the counter, mostly because they rely on branch staff to catch mistakes in their orders." (workforce-draft.md)

---

*Risk = impact x (6 - evidence), from 1 to 25. Scores and ranking are computed by code from the model's ratings; every quote above was checked against the source drafts.*

*Generated by Second Cut with gemini-3.8-flash. AI-generated analysis: verify before acting.*
