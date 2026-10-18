import secondcut as sc
from evals import reliability as rel

DRAFTS = sc.load([rel.ROOT / "examples" / rel.GROWTH, rel.ROOT / "examples" / rel.WORKFORCE])


def test_every_planted_passage_really_is_in_its_draft():
    for passages in rel.BETS.values():
        assert all(sc.grounded(rel.GROWTH, p, DRAFTS) for p in passages), passages
    for growth, workforce in rel.CONFLICTS.values():
        assert all(sc.grounded(rel.GROWTH, p, DRAFTS) for p in growth), growth
        assert all(sc.grounded(rel.WORKFORCE, p, DRAFTS) for p in workforce), workforce


def test_score_credits_partial_quotes_in_either_order():
    test = sc.Test(method="m", metric="x", go_if="g", kill_if="k", days=14)
    pay = sc.Assumption(claim="pay", source=rel.GROWTH, quote="at least 30% of our top 500 accounts to subscribe",
                        lens="desirability", impact=5, evidence=1, test=test)
    reps = pay.model_copy(update={"claim": "reps", "quote": "Hire 20 inside-sales reps in Q1", "impact": 3})
    freeze = sc.Conflict(tension="t", source_a=rel.WORKFORCE, quote_a="A hiring freeze holds through the end",
                         source_b=rel.GROWTH, quote_b="Hire 20 inside-sales reps in Q1 to call")
    result = rel.score(sc.Analysis(thesis="t", assumptions=[reps, pay], conflicts=[freeze]), DRAFTS)
    assert result == {"bets": ["Accounts will pay $49 a month", "20 reps can be hired in Q1"],
                      "conflicts": ["Hiring plan vs. hiring freeze"], "discarded": 0,
                      "top": "Accounts will pay $49 a month"}
