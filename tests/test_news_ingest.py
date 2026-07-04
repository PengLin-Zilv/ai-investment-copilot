from ai_investment_copilot import news_ingest
from ai_investment_copilot.news_ingest import (
    load_ticker_news,
    yfinance_news_to_news_item,
)


def test_yfinance_news_to_news_item_maps_conviction_fields():
    raw_item = {
        "id": "story-1",
        "content": {
            "title": "Nvidia faces AI chip export restriction",
            "summary": "New export control rules may affect semiconductor sales.",
            "pubDate": "2026-07-04T12:00:00Z",
            "provider": {"displayName": "Reuters"},
            "canonicalUrl": {"url": "https://example.com/nvda-export"},
        },
    }

    item = yfinance_news_to_news_item("NVDA", raw_item)

    assert item.id == "NVDA-story-1"
    assert item.ticker == "NVDA"
    assert item.title == "Nvidia faces AI chip export restriction"
    assert item.source == "Reuters"
    assert item.url == "https://example.com/nvda-export"
    assert item.category == "regulation"
    assert item.themes == ["AI infrastructure", "AI chip", "semiconductor"]
    assert item.summary == "New export control rules may affect semiconductor sales."


def test_load_ticker_news_uses_yfinance_ticker_news(monkeypatch):
    calls = []

    class FakeTicker:
        def __init__(self, ticker: str):
            self.ticker = ticker

        def get_news(self, count: int = 10):
            calls.append((self.ticker, count))
            return [
                {
                    "id": "story-1",
                    "content": {
                        "title": "TSMC reports AI chip revenue growth",
                        "summary": "Revenue grew on AI chip demand.",
                        "pubDate": "2026-07-04T12:00:00Z",
                        "provider": {"displayName": "CNBC"},
                        "canonicalUrl": {"url": "https://example.com/tsm-revenue"},
                    },
                }
            ]

    monkeypatch.setattr(news_ingest.yf, "Ticker", FakeTicker)

    items = load_ticker_news(["TSM"], limit_per_ticker=1)

    assert calls == [("TSM", 1)]
    assert len(items) == 1
    assert items[0].ticker == "TSM"
    assert items[0].category == "revenue"


def test_load_ticker_news_filters_blocked_sources(monkeypatch):
    class FakeTicker:
        def __init__(self, ticker: str):
            self.ticker = ticker

        def get_news(self, count: int = 10):
            return [
                {
                    "id": "fool-story",
                    "content": {
                        "title": "10 stupid stock picks for AI chip riches",
                        "summary": "Generic hype about semiconductor stocks.",
                        "pubDate": "2026-07-04T12:00:00Z",
                        "provider": {"displayName": "The Motley Fool"},
                        "canonicalUrl": {"url": "https://example.com/fool"},
                    },
                },
                {
                    "id": "good-story",
                    "content": {
                        "title": "TSMC reports AI chip revenue growth",
                        "summary": "Revenue grew on AI chip demand.",
                        "pubDate": "2026-07-04T12:00:00Z",
                        "provider": {"displayName": "CNBC"},
                        "canonicalUrl": {"url": "https://example.com/tsm-revenue"},
                    },
                },
            ]

    monkeypatch.setattr(news_ingest.yf, "Ticker", FakeTicker)

    items = load_ticker_news(["TSM"], limit_per_ticker=5)

    assert [item.source for item in items] == ["CNBC"]
    assert all("motley fool" not in item.source.lower() for item in items)
