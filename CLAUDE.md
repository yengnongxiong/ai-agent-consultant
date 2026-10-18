# CLAUDE.md

Guidance for Claude Code in this repository. Product context: [PRD.md](PRD.md). Design rationale: [README.md](README.md#design-choices-and-their-trade-offs).

## Commands

- `uv run pytest`: offline test suite (no API key, no network)
- `uv run secondcut.py DRAFT [DRAFT ...] > brief.md`: real run; needs `ANTHROPIC_API_KEY`
- `uv run --extra gemini secondcut.py --provider gemini DRAFT ...`: same on Gemini; needs `GEMINI_API_KEY`

## Architecture

Everything lives in `secondcut.py`: `load` (text, Markdown or PDF) → `analyze_claude` or `analyze_gemini` (one structured-output call) → `triage` (quote verification, risk ranking) → `render` (escaped Markdown).

## Conventions

- The model judges; code computes. Scoring, ranking and verification stay in plain Python.
- Never trust model text: verify quotes against the drafts and escape every string in `render`.
- Default runtime dependencies stay at `anthropic` and `pypdf`; other provider SDKs stay optional extras. Tests use `FakeClient` and never call the API.
