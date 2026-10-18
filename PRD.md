# Product Requirements: Second Cut

| | |
|---|---|
| **Status** | v0.1 shipped as a command-line tool |
| **Owner** | Yengnong Xiong |
| **Last updated** | October 18, 2026 |

**Contents:** [Summary](#1-summary) · [Problem](#2-problem) · [Users](#3-users-and-jobs-to-be-done) ·
[Goals](#4-goals-and-non-goals) · [Requirements](#5-requirements) · [Success metrics](#6-success-metrics) ·
[Risks](#7-risks-and-mitigations) · [Open questions](#8-open-questions)

## 1. Summary

Second Cut turns a strategy draft into a short list of the beliefs it depends on, ranks them by
risk, and attaches a cheap test with a pass or fail line to each one. It is built for the moment
right after a first draft exists, when a team is about to commit time and budget based on how
confident that draft sounds.

## 2. Problem

Writing a strategy is no longer the slow part. People and AI agents can produce a credible first
draft in minutes. The slow, expensive part is finding out which parts of it are true.

A typical first draft:

- **States beliefs as facts.** "Our customers are ready to move online" reads like a finding, but it is a bet.
- **Hides the two or three bets that matter** among a dozen that don't.
- **Ends with next steps that can't fail.** "Start the pilot" doesn't say what result would stop the plan.
- **Is never checked against its siblings.** A growth plan, a workforce review and a risk scan of the same company often disagree, and nobody lines them up.

The result: budget gets committed on the first draft's confidence, and the riskiest assumption is
discovered last, when it is most expensive to be wrong.

## 3. Users and jobs to be done

| User | What they need |
|---|---|
| **Strategy or product lead** | "Before I take this to leadership, show me what has to be true and how to check it cheaply." |
| **Executive sponsor** | "On one page, tell me which bet could sink this." |
| **Consultant or advisor** starting an engagement | "Turn this draft into a focused, hypothesis-driven plan for the first two weeks." |
| **Product manager** | "Turn the strategy into experiments my team can run this sprint." |

## 4. Goals and non-goals

**Goals**

1. Surface the load-bearing assumptions in one or more drafts, each traceable to an exact quote.
2. Rank them with a transparent rule that gives the same order for the same ratings.
3. Turn each assumption into a test with a metric, a go result, a kill result and a duration of about two weeks.
4. Catch contradictions within a draft and across drafts.

**Non-goals (v0.1)**

- Writing or rewriting the strategy. The first draft is someone else's job.
- Market research or fact-checking against outside sources.
- Running the tests or tracking their results.
- A hosted web app, user accounts or stored history.

## 5. Requirements

**Functional**

| ID | Requirement | v0.1 |
|---|---|---|
| F1 | Accept one or more Markdown or plain-text drafts. | ✅ |
| F2 | Name the 5 to 12 load-bearing assumptions, each stated so it could be proven false. | ✅ |
| F3 | Back every assumption with a verbatim quote, verified by code. Discard untraceable ones and list them in the brief. | ✅ |
| F4 | Rate impact and evidence from 1 to 5, and tag each assumption desirability, viability, feasibility or readiness. | ✅ |
| F5 | Compute risk as impact × (6 − evidence) in code, and rank. | ✅ |
| F6 | Give every assumption a test: method, metric, go result, kill result and days. | ✅ |
| F7 | Flag contradictions, with both sides quoted and verified. | ✅ |
| F8 | Produce a one-page Markdown brief. | ✅ |

**Non-functional**

| ID | Requirement | v0.1 |
|---|---|---|
| N1 | **Trust:** no finding reaches the brief without a verified quote. | ✅ |
| N2 | **Privacy:** no storage, telemetry or third parties beyond the model API. | ✅ |
| N3 | **Safety:** drafts are untrusted input; the model has no tools; output is schema-validated and escaped. | ✅ |
| N4 | **Cost:** input capped at 200,000 characters; token usage shown on every run. | ✅ |
| N5 | **Maintainability:** one source file, one runtime dependency, offline tests running in CI. | ✅ |

## 6. Success metrics

The north-star metric is **behavior change, not output quality**: the tool exists to change what a team does next.

| Metric | Target | Why it matters |
|---|---|---|
| **Tests actually run:** briefs where at least one proposed test is run within two weeks | 50% or more | The north star. A brief nobody acts on is just more reading. |
| **Grounding rate:** findings in the brief backed by a verified quote | 100% | Enforced by code. Trust is the product. |
| **Discard rate:** model findings thrown out for bad quotes | Under 10% | A rising rate is an early warning that the prompt or model is drifting. |
| **Recall:** planted assumptions found in a labeled test set | 80% or more | Measures whether the tool misses the bet that matters. Needs the evaluation set on the roadmap. |
| **Ranking agreement:** overlap between the tool's top 3 and an expert reviewer's top 3 | 2 of 3 or better | Checks that the ranking matches expert judgment. |
| **Time and cost per brief** | Under 3 minutes and under $1 | Cheap enough to run on every draft, not just the big ones. |

## 7. Risks and mitigations

| Risk | Mitigation |
|---|---|
| The model invents an assumption or misquotes a draft. | Every quote is checked against its source by code, and failures are discarded and shown. |
| The model misses the assumption that actually matters. | The prompt asks for fewer, weightier bets. An evaluation set (roadmap) will measure recall before prompt changes ship. A human still reviews the brief. |
| A score looks more precise than it is. | The brief shows the formula and the two ratings behind every score. |
| A draft contains hidden instructions (prompt injection). | Drafts are framed as data, the model has no tools, the output must match a schema, and the text is escaped before rendering. |
| Users send confidential material. | Nothing is stored, data goes only to the model API, and the README tells users to check their own policy first. |
| Teams anchor on the model's suggested thresholds. | Thresholds are presented as starting points; open question 2 below. |

## 8. Open questions

1. **Outside evidence:** should the tool search the web to rate evidence? That would be more complete, but slower, costlier and harder to audit.
2. **Anchoring:** should teams write their own kill threshold before seeing the model's suggestion?
3. **Where it lives:** command line, a tool other AI agents call (MCP), or an add-on inside a document editor?
4. **Learning loop:** how should a test's result flow back to re-rank the remaining assumptions?
