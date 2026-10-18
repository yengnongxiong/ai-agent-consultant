# CLAUDE.md

Guidance for Claude Code in this repository. Product context: [PRD.md](PRD.md). Design rationale: [README.md](README.md#design-choices).

## Commands

- `uv run pytest`: offline test suite (no API key, no network)
- `uv run secondcut.py DRAFT [DRAFT ...] > brief.md`: real run; needs `ANTHROPIC_API_KEY`
- `uv run --extra gemini secondcut.py --provider gemini DRAFT ...`: same on Gemini; needs `GEMINI_API_KEY`
- add `--html` for the web brief (layout in `template.html`)
- `uv run --extra gemini python -m evals.reliability --provider gemini --runs 5`: score repeated runs against the planted answer key; rewrites `examples/brief.md`, `docs/index.html` and `evals/results.md`

## Architecture

Everything lives in `secondcut.py`: `load` (text, Markdown or PDF) → `analyze_claude` or `analyze_gemini` (one structured-output call) → `triage` (quote verification, risk ranking) → `render` (escaped Markdown) or `render_html` (self-contained page, risk map SVG).

## Conventions

- The model judges; code computes. Scoring, ranking and verification stay in plain Python.
- Never trust model text: verify quotes against the drafts and escape every string in `render`.
- Default runtime dependencies stay at `anthropic` and `pypdf`; other provider SDKs stay optional extras. Tests use `FakeClient` and never call the API.
