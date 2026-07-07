# AI Market Copilot Context

## Goal
Build a personal market intelligence copilot, not a trading advisor.

The project should reduce market-news noise by collecting relevant news, ranking it by thesis impact, and producing a daily review artifact.

## Current Runtime Flow
`main.py` runs the current production-style path:

```text
WATCHLIST
-> load_ticker_news
-> yfinance news
-> yfinance_news_to_news_item
-> NewsItem list
-> rank_news
-> build_digest
-> save_digest
-> data/output/daily_digest.md
```

If `DISCORD_WEBHOOK_URL` is set, `main.py` also runs the delivery path:

```text
WATCHLIST
-> get_price_moves
-> build_discord_digest_messages
-> send_discord_message for each message
-> Discord channel
```

## Fixture Flow
The mock-news path still exists for tests and local development:

```text
data/fixtures/mock_news.json
-> load_news
-> NewsItem list
-> rank_news
-> build_digest
-> save_digest
```

## Modules
- `main.py`: orchestrates the runtime pipeline.
- `models/news.py`: defines the `NewsItem` data contract.
- `news_ingest.py`: loads fixture news or Yahoo Finance ticker news and normalizes raw items into `NewsItem`.
- `ranker.py`: scores and sorts news by financial, contract, risk, and AI infrastructure signals.
- `build_digest.py`: builds the markdown daily digest and compact Discord digest.
- `market_data.py`: fetches recent close-to-close ticker price moves.
- `discord_delivery.py`: sends the Discord webhook message.
- `yfinance_config.py`: keeps yfinance cache files inside `data/cache/yfinance`.

## Current Status
- Runtime flow uses Yahoo Finance ticker news for `WATCHLIST = ["NVDA", "AMD", "GOOG", "TSM", "PLTR"]`.
- Digest output is written to `data/output/daily_digest.md`.
- Discord delivery is optional and depends on `DISCORD_WEBHOOK_URL`.
- Discord sends every news item with score 4 or higher. If one message is too long, the app splits it into multiple Discord messages.
- The fixture loader remains available for tests and controlled sample data.

## Tests
The test suite covers news ingestion, `NewsItem`, ranking, digest building, market data, and the main orchestration path.

## Next Build
Improve the quality of the ranking and summary signal while keeping the pipeline simple and easy to test.
