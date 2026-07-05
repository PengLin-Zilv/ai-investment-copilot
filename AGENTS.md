# AGENTS.md

AI Investment Copilot turns watchlist market news into a ranked daily thesis digest and optional Discord signal briefing.

## Setup
- Use **uv**, never `pip`.
- Install: `uv sync`
- Use `.env` for local secrets. Never commit `.env`.
- If `.env.example` exists, copy it to `.env` before running local delivery.

## Commands
- Test: `uv run pytest`
- Single test: `uv run pytest path/to/test.py::test_name -q`
- Lint: `uv run ruff check`
- Format: `uv run ruff format`

## Product Boundary
- This project is a market intelligence copilot, not a trading advisor.
- Do not add buy/sell/hold recommendations.
- Optimize for thesis monitoring and attention filtering, not generic market news coverage.

## Rules
- Python version follows `pyproject.toml`.
- Do not hand-edit `uv.lock`; use `uv add` / `uv remove`.
- Ask before adding a production dependency.
- Add or update tests for behavior you change.
- Keep mock/news ingestion, ranking, digest formatting, market data, and delivery concerns separated.
- Never commit secrets, `.env`, runtime cache, or generated local output unless explicitly asked.

## Project Notes
- `NewsItem` is the internal contract. External sources must be mapped into `NewsItem`.
- `ranker.py` decides thesis relevance; it should not fetch news or format output.
- `build_digest.py` formats markdown.
- `discord_delivery.py` only sends messages; it should not decide content.
- Full digest can be longer; Discord digest must stay compact and under Discord message limits.

## Graphify
- This project has a knowledge graph at `graphify-out/` with god nodes, community structure, and cross-file relationships.
- When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.
- For codebase questions, first run `graphify query "<question>"` when `graphify-out/graph.json` exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts.
- Dirty `graphify-out/` files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify.
- Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If `graphify-out/wiki/index.md` exists, use it for broad navigation instead of raw source browsing.
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current.

## Change Hygiene
- Keep changes focused.
- For meaningful changes, include a short summary and validation commands.
- Run tests and lint before merging or sharing changes.
- Use branches for larger or uncertain changes.
- Use PRs only when review, CI history, or collaboration is useful.
