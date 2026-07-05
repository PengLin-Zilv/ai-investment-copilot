# AI Investment Copilot

A personal investment copilot that watches your list, turns market news into a clean digest, and delivers it to your Discord channel (for now). 

This project is not a trading advisor. It does not make buy, sell, or hold decisions. The goal is to filter market information, summarize what matters, and help the user review news with less noise.

The goal of the project is to build an AI assistant who has your convictions, your styles, and adapatively becoming the AI companion you need - to save your time to work on other important things in life. 

Less unnecessary decision, less unnecessary trade, less unnecessary stress, more necessary time to think and enjoy life.


## Current Status

The pipeline works:

```text
your watchlsit -> sort yfinance news base on your convictions -> build digest -> send to discord 
```

The project currently uses mock news data from `data/fixtures/mock_news.json` and generates a markdown digest at `data/output/daily_digest.md`.

## Project Structure

```text
ai-investment-copilot/
├─ data/
│  ├─ fixtures/
│  │  └─ mock_news.json
│  └─ output/
│     ├─ daily_digest.md
│     └─ test.md
├─ docs/
│  └─ CONTEXT.md
├─ src/
│  └─ ai_investment_copilot/
│     ├─ __init__.py
│     ├─ build_digest.py
│     ├─ discord_delivery.py
│     ├─ main.py
│     ├─ market_data.py
│     ├─ news_ingest.py
│     ├─ ranker.py
│     ├─ yfinance_config.py
│     └─ models/
│        ├─ __init__.py
│        └─ news.py
├─ tests/
│  ├─ test_build_digest.py
│  ├─ test_main.py
│  ├─ test_market_data.py
│  ├─ test_news_ingest.py
│  ├─ test_news_item.py
│  └─ test_ranker.py
├─ .gitignore
├─ .python-version
├─ pyproject.toml
├─ uv.lock
└─ README.md
```


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
and sends a Discord message if `DISCORD_WEBHOOK_URL` is set in `.env`.

## Current Limitations

- Static watchlist hardcoded in `main.py`. User should be able to configure their own watchlist.
- Static news source (Yahoo Finance) hardcoded in `news_ingest.py`. User should be able to choose multiple news sources. (Motley Fool is currently blocked due to low-quality content.)
- Ranking is based on simple keyword matching. User should be able to configure their own ranking rules and weights.
- No Telegram/other platform delivery yet. User should be able to choose their preferred delivery platform.
- No LLM summarization or scoring yet. LLM should be able to summarize news and score importance based on user-defined criteria. User should be able to ask LLM questions about the news digest and get answers in natural language. 
- No frontend yet. User should be able to view the digest in a web interface and interact with the LLM. Add their portfolio and watchlist, and get personalized insights and recommendations.

## Next Steps
1. Add scheduled daily digest delivery.
2. Add a lightweight dashboard or chat interface.
