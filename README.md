# AI Investment Copilot

A personal market intelligence copilot that turns market news into a clean daily digest.

This project is not a trading advisor. It does not make buy, sell, or hold decisions. The goal is to filter market information, summarize what matters, and help the user review news with less noise.

## Current Status

The first mock-news pipeline works:

```text
mock_news.json -> load_news -> rank_news -> build_digest -> save_digest -> daily_digest.md
```

The project currently uses mock news data from `data/fixtures/mock_news.json` and generates a markdown digest at `data/output/daily_digest.md`.

## Project Structure

```text
ai-investment-copilot/
├─ data/
│  ├─ fixtures/
│  │  └─ mock_news.json
│  └─ output/
│     └─ daily_digest.md
├─ docs/
├─ src/
│  └─ ai_investment_copilot/
│     ├─ main.py
│     ├─ news_ingest.py
│     ├─ ranker.py
│     ├─ build_digest.py
│     └─ models/
│        └─ news.py
├─ tests/
├─ pyproject.toml
└─ README.md
```

## Pipeline

### 1. `NewsItem`

`NewsItem` is the internal data contract for one news item.

It defines the fields the rest of the pipeline expects, such as ticker, title, URL, themes, published time, and summary.

### 2. `news_ingest.py`

Loads raw JSON news data and converts each item into a `NewsItem`.

This keeps external data formats isolated from the rest of the system.

### 3. `ranker.py`

Ranks news items by importance.

Right now, `rank_news` is a pass-through function. It returns the news items unchanged so the pipeline structure can be tested first. Later, this module can use rules or an LLM to rank news.

### 4. `build_digest.py`

Turns ranked `NewsItem` objects into markdown text and saves the digest to a file.

### 5. `main.py`

Runs the full pipeline in order.

It imports the pipeline steps and orchestrates them without owning the business logic.

## Setup

Install dependencies with uv:

```bash
uv sync
```

## Run

From the project root:

```bash
uv run python -m ai_investment_copilot.main
```

This generates:

```text
data/output/daily_digest.md
```

## Current Limitations

- Uses mock news data only.
- Ranking is currently pass-through.
- No real news API integration yet.
- No LLM summarization or scoring yet.
- No Discord or Telegram delivery yet.
- No frontend yet.

## Next Steps

1. Add a simple rule-based ranker.
2. Add real news ingestion from RSS or an API.
3. Add LLM-based importance scoring.
4. Add scheduled daily digest delivery.
5. Add a lightweight dashboard or chat interface.
