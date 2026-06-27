import pytest
from datetime import datetime
from pydantic import ValidationError

from ai_investment_copilot.models.news import NewsItem


def test_valid_news_item_creates():
    """test if normal data can create NewsItem"""
    item = NewsItem(
        id="NVDA-export-restriction-06-27-2026",
        ticker="NVDA",
        title="Nvdia gets restriction on its chip again",
        source="Reuters",
        url="https://example.com/nvda-export-restriction",
        published_at="2026-06-27T14:00:00Z",
        category="regulation",
        theme=["AI infrastructure", "Semiconductor"],
        summary="Nvidia got restrictin on exporting its advanced chip to China",
    )
    assert item.ticker == "NVDA"
    assert item.source == "Reuters"
