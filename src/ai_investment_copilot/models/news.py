from pydantic import BaseModel
from datetime import datetime


class NewsItem(BaseModel):
    id: str
    ticker: str
    title: str
    source: str
    url: str
    published_at: datetime
    category: str
    theme: list[str]
    summary: str
