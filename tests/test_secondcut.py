import contextlib
from types import SimpleNamespace

import pytest

import secondcut as sc

DRAFTS = {
    "growth.md": "We will **add 20 sales reps** in Q1.\nCustomers say they’d pay more for bundles.",
    "people.md": "A hiring freeze holds through next year.",
    "report.pdf": "\ufb01ve of our branches al-\nready sell on\nline",  # PDF ligature, hyphen and wraps
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
    assert sc.grounded("report.pdf", "five of our branches already sell online", DRAFTS)


def test_grounded_rejects_invented_misattributed_and_trivial_quotes():
    assert not sc.grounded("growth.md", "customers will pay double", DRAFTS)
    assert not sc.grounded("report.pdf", "five of our branches already sell offline", DRAFTS)
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
    md = sc.render(sc.Analysis(thesis="t", assumptions=[a], conflicts=[]), [a], [], [], "test-model")
    assert r"\[click\]" in md and r"\<img\>" in md and r"a\|b" in md
    assert "0 of 1 load-bearing assumptions are high-risk" in md  # risk 9 is below the bar


def test_claude_sends_tagged_drafts_and_returns_parsed_output():
    parsed = sc.Analysis(thesis="t", assumptions=[], conflicts=[])
    usage = SimpleNamespace(input_tokens=1, output_tokens=1)
    client = FakeClient(SimpleNamespace(stop_reason="end_turn", parsed_output=parsed, usage=usage))
    assert sc.analyze_claude(DRAFTS, client) is parsed
    content = client.kwargs["messages"][0]["content"]
    assert '<draft name="people.md">' in content and client.kwargs["output_format"] is sc.Analysis


@pytest.mark.parametrize("stop_reason", ["refusal", "max_tokens"])
def test_claude_fails_loudly_when_the_model_stops_early(stop_reason):
    client = FakeClient(SimpleNamespace(stop_reason=stop_reason, parsed_output=None))
    with pytest.raises(RuntimeError, match=stop_reason):
        sc.analyze_claude(DRAFTS, client)


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


def test_gemini_returns_parsed_output_and_rejects_invalid_replies():
    parsed = sc.Analysis(thesis="t", assumptions=[], conflicts=[])
    usage = SimpleNamespace(prompt_token_count=1, candidates_token_count=1, thoughts_token_count=None)
    calls = []

    def client(reply):
        def generate_content(**kwargs):
            calls.append(kwargs)
            return SimpleNamespace(parsed=reply, candidates=[SimpleNamespace(finish_reason="STOP")], usage_metadata=usage)
        return SimpleNamespace(models=SimpleNamespace(generate_content=generate_content))

    assert sc.analyze_gemini(DRAFTS, client(parsed)) is parsed
    assert calls[0]["config"]["response_schema"] is sc.Analysis and '<draft name="growth.md">' in calls[0]["contents"]
    with pytest.raises(RuntimeError, match="STOP"):
        sc.analyze_gemini(DRAFTS, client(None))


def make_pdf(text):
    """Build a one-page PDF by hand so the test needs no PDF-writing library."""
    stream = f"BT /F1 12 Tf 72 720 Td ({text}) Tj ET".encode()
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R"
        b" /Resources << /Font << /F1 5 0 R >> >> >>",
        b"<< /Length %d >>\nstream\n%s\nendstream" % (len(stream), stream),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    pdf, offsets = b"%PDF-1.4\n", []
    for number, body in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf += b"%d 0 obj\n%s\nendobj\n" % (number, body)
    xref = len(pdf)
    pdf += b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    pdf += b"".join(b"%010d 00000 n \n" % offset for offset in offsets)
    return pdf + b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n" % (len(objects) + 1, xref)


def test_load_reads_pdf_text_and_rejects_broken_or_oversized_pdfs(tmp_path, monkeypatch):
    good = tmp_path / "report.pdf"
    good.write_bytes(make_pdf("We will add 20 sales reps in Q1."))
    assert sc.load([good]) == {"report.pdf": "We will add 20 sales reps in Q1."}

    broken = tmp_path / "broken.pdf"
    broken.write_bytes(b"%PDF-1.4 not really a pdf")
    with pytest.raises(SystemExit, match="cannot read"):
        sc.load([broken])

    monkeypatch.setattr(sc, "MAX_PDF_BYTES", 10)
    with pytest.raises(SystemExit, match="larger than"):
        sc.load([good])


def test_html_brief_is_self_contained_escaped_and_plots_every_assumption():
    risky = assumption("add 20 sales reps", claim="<script>alert(1)</script>", impact=5, evidence=1)
    safe = assumption("pay more for bundles", claim="bundles", impact=2, evidence=4)
    analysis = sc.Analysis(thesis='Grow "fast" & <b>loud</b>', assumptions=[risky, safe], conflicts=[])
    page = sc.render_html(analysis, *sc.triage(analysis, DRAFTS), "test-model")

    assert "<script" not in page and "&lt;script&gt;" in page and "&lt;b&gt;loud&lt;/b&gt;" in page
    assert "default-src 'none'" in page  # the browser itself refuses scripts and remote files
    assert page.count('class="dot"') == 2 and 'href="#a1"' in page and 'id="a2"' in page
    assert "1 of 2 load-bearing assumptions are high-risk" in page and "$" not in page.split("<main>")[1]
