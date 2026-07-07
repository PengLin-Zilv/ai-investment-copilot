from pydantic import BaseModel
from datetime import datetime


class NewsItem(BaseModel):
    """One normalized news story used by the rest of the app."""

    id: str
    ticker: str
    title: str
    source: str
    url: str
    published_at: datetime
    category: str
    themes: list[str]
    summary: str
