import contextlib
from types import SimpleNamespace

import pytest

import secondcut as sc

DRAFTS = {
    "growth.md": "We will **add 20 sales reps** in Q1.\nCustomers say they’d pay more for bundles.",
    "people.md": "A hiring freeze holds through next year.",
}


def assumption(quote, claim="c", source="growth.md", impact=3, evidence=3):
    test = sc.Test(method="m", metric="x", go_if="g", kill_if="k", days=14)
    return sc.Assumption(claim=claim, source=source, quote=quote, lens="viability",
                         impact=impact, evidence=evidence, test=test)


class FakeClient:
    """Stands in for anthropic.Anthropic so tests run offline and free."""

    def __init__(self, message):
        self.beta = SimpleNamespace(messages=self)
        self.message, self.kwargs = message, None

    def stream(self, **kwargs):
        self.kwargs = kwargs
        return contextlib.nullcontext(SimpleNamespace(get_final_message=lambda: self.message))


def test_grounded_tolerates_case_whitespace_and_smart_quotes():
    assert sc.grounded("growth.md", "customers say they'd   PAY more", DRAFTS)


def test_grounded_rejects_invented_misattributed_and_trivial_quotes():
    assert not sc.grounded("growth.md", "customers will pay double", DRAFTS)
    assert not sc.grounded("people.md", "add 20 sales reps", DRAFTS)
    assert not sc.grounded("growth.md", "We", DRAFTS)
    assert not sc.grounded("missing.md", "add 20 sales reps", DRAFTS)


def test_triage_ranks_by_risk_and_discards_untraceable_findings():
    reps = assumption("add 20 sales reps", claim="reps", impact=5, evidence=1)  # risk 25
    bundles = assumption("pay more for bundles", claim="bundles", impact=2, evidence=4)  # risk 4
    invented = assumption("demand will triple overnight", claim="invented")
    real = sc.Conflict(tension="hire vs freeze", source_a="growth.md", quote_a="add 20 sales reps",
                       source_b="people.md", quote_b="a hiring freeze holds")
    fake = real.model_copy(update={"tension": "fake", "quote_b": "layoffs start in May"})
    analysis = sc.Analysis(thesis="t", assumptions=[bundles, invented, reps], conflicts=[real, fake])

    kept, conflicts, rejected = sc.triage(analysis, DRAFTS)

    assert [a.claim for a in kept] == ["reps", "bundles"]
    assert conflicts == [real]
    assert rejected == ["invented", "fake"]


def test_render_escapes_model_text_so_it_cannot_inject_links_or_html():
    a = assumption("add 20 sales reps", claim="[click](https://example.com) <img> a|b")
    md = sc.render(sc.Analysis(thesis="t", assumptions=[a], conflicts=[]), [a], [], [])
    assert r"\[click\]" in md and r"\<img\>" in md and r"a\|b" in md
    assert "0 of 1 load-bearing assumptions are high-risk" in md  # risk 9 is below the bar


def test_analyze_sends_tagged_drafts_and_returns_parsed_output():
    parsed = sc.Analysis(thesis="t", assumptions=[], conflicts=[])
    client = FakeClient(SimpleNamespace(stop_reason="end_turn", parsed_output=parsed))
    assert sc.analyze(DRAFTS, client) is parsed
    content = client.kwargs["messages"][0]["content"]
    assert '<draft name="people.md">' in content and client.kwargs["output_format"] is sc.Analysis


@pytest.mark.parametrize("stop_reason", ["refusal", "max_tokens"])
def test_analyze_fails_loudly_when_the_model_stops_early(stop_reason):
    client = FakeClient(SimpleNamespace(stop_reason=stop_reason, parsed_output=None))
    with pytest.raises(RuntimeError, match=stop_reason):
        sc.analyze(DRAFTS, client)


def test_load_rejects_empty_duplicate_and_oversized_input(tmp_path):
    empty = tmp_path / "empty.md"
    empty.write_text("  \n")
    big = tmp_path / "big.md"
    big.write_text("x" * (sc.MAX_INPUT_CHARS + 1))
    small = tmp_path / "a.md"
    small.write_text("ok")
    (tmp_path / "sub").mkdir()
    twin = tmp_path / "sub" / "a.md"
    twin.write_text("ok")
    for paths in ([empty], [big], [small, twin]):
        with pytest.raises(SystemExit):
            sc.load(paths)
