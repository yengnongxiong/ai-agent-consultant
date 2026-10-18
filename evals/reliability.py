"""Measure how reliably Second Cut finds what was planted in the example drafts.

The example drafts were written around known bets and known contradictions. This runs the analysis
several times, saves every raw model reply, scores each run against the planted answers, and
publishes run 1 (not the best run) as the example brief.

Usage: uv run --extra gemini python -m evals.reliability --provider gemini --runs 5
"""

import argparse
import sys
from pathlib import Path

import secondcut as sc

ROOT = Path(__file__).resolve().parent.parent
GROWTH, WORKFORCE = "growth-draft.md", "workforce-draft.md"

# Bets the growth draft was written around, as passages copied from it.
BETS = {
    "Contractors will order online": ["Corvane's contractors are ready to move ordering online",
                                      "moved 22% of repeat orders online with no promotion"],
    "Accounts will pay $49 a month": ["Launch Corvane Pro, a $49/month membership",
                                      "free next-day delivery and bulk pricing on 2,000 core items",
                                      "We expect at least 30% of our top 500 accounts to subscribe within six months",
                                      "38% said they would pay a monthly fee to guarantee it"],
    "Order history is clean": ["Our ERP order history is clean enough to train demand forecasts"],
    "Suggestions lift order frequency": ["Suggested carts should lift order frequency by 15%"],
    "20 reps can be hired in Q1": ["Hire 20 inside-sales reps in Q1 to call every top-500 account"],
    "Reps will drive adoption": ["Reps are the fastest path to adoption because contractors trust their branch contacts"],
    "IT can build the model now": ["Start the reorder-model build with the existing IT team"],
    "Margin rises to 26%": ["gross margin rises from 22% to 26% within 18 months"],
    "Rivals won't respond for a year": ["national players have not yet built local same-day delivery",
                                        "they will not respond within the next 12 months"],
    "Pro opens two new metros": ["Expand to two new metro areas"],
}
# Contradictions planted between the drafts: (growth-draft passages, workforce-draft passages).
CONFLICTS = {
    "Hiring plan vs. hiring freeze": (
        ["Hire 20 inside-sales reps in Q1 to call every top-500 account"],
        ["A hiring freeze holds through the end of next fiscal year",
         "the inside-sales team will shrink from 35 to 28 through attrition"]),
    "Clean data vs. mislabeled codes": (
        ["Our ERP order history is clean enough to train demand forecasts"],
        ["the team has flagged duplicate and mislabeled product codes in roughly a fifth of historical orders"]),
    "IT build vs. ERP upgrade": (
        ["Start the reorder-model build with the existing IT team"],
        ["IT is fully committed to the ERP upgrade until Q3"]),
    "Online-ready vs. phone preference": (
        ["Corvane's contractors are ready to move ordering online",
         "moved 22% of repeat orders online with no promotion"],
        ["41 of 50 contractors said they prefer to order by phone or at the counter"]),
    "Reps drive adoption vs. commission pay": (
        ["Reps are the fastest path to adoption because contractors trust their branch contacts",
         "call every top-500 account and sign them up for Pro"],
        ["paid commission only on orders they personally place",
         "Orders that customers place online earn reps nothing"]),
}


def overlaps(quote: str, passages: list[str], window: int = 20) -> bool:
    """True if the quote shares a 20-character stretch (ignoring case and spacing) with any passage."""
    q = sc._norm(quote)
    return any(q[i:i + window] in sc._norm(p) for p in passages for i in range(max(1, len(q) - window + 1)))


def score(analysis: sc.Analysis, drafts: dict[str, str]) -> dict:
    kept, conflicts, rejected = sc.triage(analysis, drafts)
    bets = [name for name, passages in BETS.items() if any(overlaps(a.quote, passages) for a in kept)]
    found = [name for name, (growth, workforce) in CONFLICTS.items() if any(
        overlaps(c.quote_a, growth) and overlaps(c.quote_b, workforce)
        or overlaps(c.quote_a, workforce) and overlaps(c.quote_b, growth) for c in conflicts)]
    top = next((name for name, passages in BETS.items() if overlaps(kept[0].quote, passages)),
               "another bet") if kept else "none"
    return {"bets": bets, "conflicts": found, "discarded": len(rejected), "top": top}


def summarize(results: list[dict], model: str) -> str:
    n = len(results)
    lines = ["# Reliability on the example drafts", "",
             f"{n} runs with `{model}`, each scored against what the drafts were written to contain: "
             f"{len(BETS)} bets and {len(CONFLICTS)} contradictions. Run 1 is the published example.", "",
             "| Run | Bets found | Contradictions caught | Quotes discarded | #1 risk |",
             "|---|---|---|---|---|"]
    lines += [f"| {i} | {len(r['bets'])} of {len(BETS)} | {len(r['conflicts'])} of {len(CONFLICTS)} "
              f"| {r['discarded']} | {r['top']} |" for i, r in enumerate(results, 1)]
    lines += ["", "## Contradictions caught, by runs", ""]
    lines += [f"- {name}: {sum(name in r['conflicts'] for r in results)} of {n}" for name in CONFLICTS]
    lines += ["", "## Bets found, by runs", ""]
    lines += [f"- {name}: {sum(name in r['bets'] for r in results)} of {n}" for name in BETS]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--provider", choices=["claude", "gemini"], default="claude")
    parser.add_argument("--runs", type=int, default=5)
    args = parser.parse_args()
    drafts = sc.load([ROOT / "examples" / GROWTH, ROOT / "examples" / WORKFORCE])
    model = sc.GEMINI_MODEL if args.provider == "gemini" else sc.CLAUDE_MODEL
    runs_dir = ROOT / "examples" / "runs"
    runs_dir.mkdir(exist_ok=True)
    results = []
    for i in range(1, args.runs + 1):
        print(f"Run {i} of {args.runs} with {model}...", file=sys.stderr)
        analysis = sc.run(args.provider, drafts)
        (runs_dir / f"{model}-run{i}.json").write_text(analysis.model_dump_json(indent=2) + "\n")
        results.append(score(analysis, drafts))
        if i == 1:  # publish the first run, not the best one
            triaged = sc.triage(analysis, drafts)
            (ROOT / "examples" / "brief.md").write_text(sc.render(analysis, *triaged, model))
            (ROOT / "docs").mkdir(exist_ok=True)
            (ROOT / "docs" / "index.html").write_text(sc.render_html(analysis, *triaged, model))
    report = summarize(results, model)
    (ROOT / "evals" / "results.md").write_text(report)
    print(report)


if __name__ == "__main__":
    main()
