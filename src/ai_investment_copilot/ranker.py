"""
This script ranks all the news and decide which goes to user notifications
Will use LLM, now is just a draft for the completeness of the pipeline
"""
from ai_investment_copilot.models.news import NewsItem

def rank_news(news_items: list[NewsItem]) -> list[NewsItem]:
    """Return News Items in a Ranked Order"""
    return news_items

