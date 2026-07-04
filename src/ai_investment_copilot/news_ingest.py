""""
This script turns the news to NewsItem
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import yfinance as yf

from ai_investment_copilot.models.news import NewsItem


FINANCIAL_KEYWORDS = ["earnings", "revenue", "cash flow", "margin", "guidance"]
CONTRACT_KEYWORDS = ["contract", "partnership", "collaboration", "agreement", "deal"]
RISK_KEYWORDS = ["regulation", "restriction", "export control", "supply chain"]

THEME_KEYWORDS = [
    ("AI infrastructure", ["ai infrastructure", "ai chip", "data center", "semiconductor", "cloud"]),
    ("AI chip", ["ai chip", "gpu"]),
    ("semiconductor", ["semiconductor", "chip"]),
    ("data center", ["data center"]),
    ("cloud", ["cloud"]),
]


def load_news(json_path: str | Path) -> list[NewsItem]:
    """Read mock news JSON, turns to NewsItem list"""
    path = Path(json_path)
    raw_text = path.read_text(encoding="utf-8")
    raw_items = json.loads(raw_text)

    news_item = [NewsItem(**item) for item in raw_items]

    return news_item


def load_ticker_news(tickers: list[str], limit_per_ticker: int = 5) -> list[NewsItem]:
    """Load recent Yahoo Finance news for watchlist tickers."""
    news_items = []

    for ticker in tickers:
        raw_items = yf.Ticker(ticker).get_news(count=limit_per_ticker)
        news_items.extend(
            yfinance_news_to_news_item(ticker, raw_item)
            for raw_item in raw_items[:limit_per_ticker]
        )

    return news_items


def yfinance_news_to_news_item(ticker: str, raw_item: dict) -> NewsItem:
    """Convert one yfinance news item to the internal NewsItem contract."""
    content = raw_item.get("content", raw_item)
    title = content.get("title", "")
    summary = content.get("summary") or content.get("description") or title

    return NewsItem(
        id=f"{ticker}-{raw_item.get('id') or content.get('id') or _slug(title)}",
        ticker=ticker,
        title=title,
        source=_source(content, raw_item),
        url=_url(content, raw_item),
        published_at=_published_at(content, raw_item),
        category=infer_category(title, summary),
        themes=infer_themes(title, summary),
        summary=summary,
    )


def infer_category(title: str, summary: str) -> str:
    """Infer the broad category used by the ranker."""
    text = f"{title} {summary}".lower()

    if any(keyword in text for keyword in FINANCIAL_KEYWORDS):
        return "revenue"
    if any(keyword in text for keyword in CONTRACT_KEYWORDS):
        return "contract"
    if any(keyword in text for keyword in RISK_KEYWORDS):
        return "regulation"

    return "general"


def infer_themes(title: str, summary: str) -> list[str]:
    """Infer themes that match the user's AI infrastructure thesis."""
    text = f"{title} {summary}".lower()
    themes = [
        theme
        for theme, keywords in THEME_KEYWORDS
        if any(keyword in text for keyword in keywords)
    ]

    return themes or ["general"]


def _source(content: dict, raw_item: dict) -> str:
    provider = content.get("provider", {})
    return provider.get("displayName") or content.get("publisher") or raw_item.get("publisher") or "Yahoo Finance"


def _url(content: dict, raw_item: dict) -> str:
    canonical_url = content.get("canonicalUrl", {})
    click_url = content.get("clickThroughUrl", {})
    return (
        canonical_url.get("url")
        or click_url.get("url")
        or content.get("link")
        or raw_item.get("link")
        or ""
    )


def _published_at(content: dict, raw_item: dict) -> datetime | str:
    if content.get("pubDate"):
        return content["pubDate"]

    timestamp = raw_item.get("providerPublishTime") or content.get("providerPublishTime")
    if timestamp:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)

    return datetime.now(timezone.utc)


def _slug(text: str) -> str:
    return "-".join(text.lower().split())[:80] or "news"

