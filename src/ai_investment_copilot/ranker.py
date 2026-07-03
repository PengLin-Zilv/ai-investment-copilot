"""
This script ranks all the news and decide which goes to user notifications
Will use LLM, now is just a draft for the completeness of the pipeline
"""
from ai_investment_copilot.models.news import NewsItem
from ai_investment_copilot.models.news import News

def score_news(news: NewsItem) -> int:
    """Return a score for the news item based on various criteria"""
    score = 0

    if news.category in ["Earnings", "Revenue", "Cash Flow"]:
        score += 5
    if news.category in ["contract", "partnership"]:
        score += 4
    if news.category in ["regulation", "supply_chain"]:
        score += 4
    ai_infra_keywords = [
        "AI infrastructure",
        "AI chip",
        "semiconductor",
        "data center",
        "cloud",
    ]
    if any(keyword in news.themes for keyword in ai_infra_keywords):
        score += 3

    return score

def rank_news(news_items: News) -> list[NewsItem]:
    """Rank the news items based on their scores and return the top items"""
    return sorted(news_items, key=score_news, reverse=True)
