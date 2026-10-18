# Second Cut: decision brief

**What the drafts propose:** Corvane plans to accelerate digital revenue and expand margins by launching a paid Pro membership, AI reordering, and dedicated phone sales, while workforce constraints suggest organizational friction and misaligned incentives could derail adoption.

**Bottom line:** 7 of 7 load-bearing assumptions are high-risk (score 15+ of 25). Run their tests before committing budget.

## Ranked assumptions

| # | Risk | Assumption | Lens | Impact | Evidence |
|---|---|---|---|---|---|
| 1 | **25** | Shifting orders online will drive overall gross margin from 22% up to 26% within 18 months despite bulk discounts and delivery costs. | viability | 5/5 | 1/5 |
| 2 | **20** | Contractors will pay a $49 monthly membership fee to receive free next-day delivery and bulk pricing. | desirability | 5/5 | 2/5 |
| 3 | **20** | Contractors will accept unassisted digital ordering rather than relying on branch staff to check their orders. | desirability | 5/5 | 2/5 |
| 4 | **20** | Corvane can hire 20 inside-sales reps in Q1 to drive Pro membership sign-ups. | readiness | 4/5 | 1/5 |
| 5 | **20** | Corvane's historical ERP order data is clean enough to train automated reorder algorithms immediately. | feasibility | 4/5 | 1/5 |
| 6 | **20** | Sales reps will cooperate with moving contractor accounts online without compensation restructuring. | readiness | 4/5 | 1/5 |
| 7 | **15** | The existing IT team has bandwidth to build an AI reorder suggestion feature immediately. | readiness | 3/5 | 1/5 |

## Test plan

### 1. Shifting orders online will drive overall gross margin from 22% up to 26% within 18 months despite bulk discounts and delivery costs.

> "As orders shift online, gross margin rises from 22% to 26% within 18 months, driven by lower cost-to-serve and Pro membership fees." (growth-draft.md)

- **Test (7 days):** Run unit-economic cost simulation modeling the cost of free next-day delivery and bulk price cuts across the top 2,000 SKUs against $49/month fee revenue.
- **Measure:** Projected net gross margin percentage across Pro orders
- **Go if:** \>= 25%
- **Kill if:** \< 22%

### 2. Contractors will pay a $49 monthly membership fee to receive free next-day delivery and bulk pricing.

> "We expect at least 30% of our top 500 accounts to subscribe within six months" (growth-draft.md)

- **Test (14 days):** Outreach by sales reps to 50 top-500 accounts offering an early binding pre-order contract for the $49/month Pro subscription.
- **Measure:** Percentage of contacted accounts signing a binding pre-order agreement
- **Go if:** \>= 30%
- **Kill if:** \< 10%

### 3. Contractors will accept unassisted digital ordering rather than relying on branch staff to check their orders.

> "Corvane's contractors are ready to move ordering online, and the company that captures that shift first will own the regional market." (growth-draft.md)

- **Test (14 days):** Provide 30 high-volume counter/phone customers with a digital ordering portal with a $20 discount credit to place their next live order.
- **Measure:** Percentage of contacted contractors who place their next order entirely online without calling branch staff
- **Go if:** \>= 35%
- **Kill if:** \< 15%

### 4. Corvane can hire 20 inside-sales reps in Q1 to drive Pro membership sign-ups.

> "Hire 20 inside-sales reps in Q1 to call every top-500 account and sign them up for Pro." (growth-draft.md)

- **Test (7 days):** Submit a hiring requisition for 20 inside-sales roles to executive leadership and HR for formal freeze-exception approval.
- **Measure:** Number of approved job requisitions for Q1
- **Go if:** \>= 20
- **Kill if:** \< 5

### 5. Corvane's historical ERP order data is clean enough to train automated reorder algorithms immediately.

> "Our ERP order history is clean enough to train demand forecasts that predict what each contractor will need next week." (growth-draft.md)

- **Test (7 days):** Audit a random sample of 1,000 historical order records to check item code standardization, duplicates, and missing metadata.
- **Measure:** Percentage of historical order records containing clean, uncorrupted product codes
- **Go if:** \>= 95%
- **Kill if:** \< 85%

### 6. Sales reps will cooperate with moving contractor accounts online without compensation restructuring.

> "Reps are the fastest path to adoption because contractors trust their branch contacts." (growth-draft.md)

- **Test (10 days):** Interview 15 branch and inside-sales reps with a mock script asking them to refer top accounts to self-service online checkout under existing commission terms.
- **Measure:** Percentage of interviewed reps willing to actively refer accounts to online ordering without commission credit
- **Go if:** \>= 60%
- **Kill if:** \< 20%

### 7. The existing IT team has bandwidth to build an AI reorder suggestion feature immediately.

> "Start the reorder-model build with the existing IT team." (growth-draft.md)

- **Test (5 days):** Review the 4-person IT team's sprint backlog and ERP upgrade roadmap with the IT lead to determine capacity.
- **Measure:** Hours per week dedicated to AI model development without delaying the ERP upgrade
- **Go if:** \>= 40
- **Kill if:** \< 10

## Conflicts

- **Growth strategy requires hiring 20 inside-sales reps in Q1, but leadership has enacted a strict hiring freeze that shrinks inside-sales headcount.** "Hire 20 inside-sales reps in Q1 to call every top-500 account and sign them up for Pro." (growth-draft.md) vs. "A hiring freeze holds through the end of next fiscal year. Headcount stays flat, and the inside-sales team will shrink from 35 to 28 through attrition." (workforce-draft.md)
- **Growth strategy assumes historical order data is clean enough for forecasting, whereas the workforce draft notes widespread data errors.** "Our ERP order history is clean enough to train demand forecasts that predict what each contractor will need next week." (growth-draft.md) vs. "the team has flagged duplicate and mislabeled product codes in roughly a fifth of historical orders." (workforce-draft.md)
- **Growth strategy expects existing IT to immediately build reorder models, but IT is entirely committed to the ERP upgrade until Q3.** "Start the reorder-model build with the existing IT team." (growth-draft.md) vs. "IT is fully committed to the ERP upgrade until Q3." (workforce-draft.md)
- **Growth strategy claims contractors prefer online ordering, but workforce research indicates most prefer phone and counter interactions to prevent errors.** "Corvane's contractors are ready to move ordering online" (growth-draft.md) vs. "In last year's customer survey, 41 of 50 contractors said they prefer to order by phone or at the counter, mostly because they rely on branch staff to catch mistakes in their orders." (workforce-draft.md)

---

*Risk = impact x (6 - evidence), from 1 to 25. Scores and ranking are computed by code from the model's ratings; every quote above was checked against the source drafts.*

*Generated by Second Cut with gemini-3.8-flash. AI-generated analysis: verify before acting.*

