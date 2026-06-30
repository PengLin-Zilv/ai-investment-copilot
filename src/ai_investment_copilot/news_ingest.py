""""Turns the news to NewsItem"""

import json
from pathlib import Path

from ai_investment_copilot.models.news import NewsItem

def load_news(json_path: str | Path) -> list[NewsItem]:
    """Read mock news JSON, turns to NewsItem list"""
    path = Path(json_path)
    raw_text = path.read_text(encoding="utf-8")
    raw_items = json.loads(raw_text)

    news_item = [NewsItem(**item) for item in raw_items]

    return news_item

