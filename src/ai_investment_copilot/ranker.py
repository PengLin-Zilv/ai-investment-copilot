"""
This script ranks all the news and decide which goes to user notifications
Will use LLM, now is just a draft for the completeness of the pipeline
"""
from ai_investment_copilot.models.news import NewsItem

FINANCIAL_CATEGORIES = {"earnings", "revenue", "cash_flow", "cash flow"}
CONTRACT_CATEGORIES = {"contract", "partnership"}
RISK_CATEGORIES = {"regulation", "supply_chain", "supply chain"}

AI_INFRA_KEYWORDS = [
    "ai infrastructure",
    "ai chip",
    "semiconductor",
    "data center",
    "cloud",
]

THESIS_RISK_KEYWORDS = [
    "restriction",
    "export control",
    "supply chain",
    "demand slowdown",
    "margin pressure",
    "capex cut",
]

def score_news(news: NewsItem) -> int:
    """Return a thesis-impact score for one news item."""
    score = 0
    category = news.category.lower()
    themes_text = " ".join(news.themes).lower()
    news_text = f"{news.title} {news.summary}".lower()

    if category in FINANCIAL_CATEGORIES:
        score += 5
    if category in CONTRACT_CATEGORIES:
        score += 4
    if category in RISK_CATEGORIES:
        score += 4
    if any(keyword in themes_text for keyword in AI_INFRA_KEYWORDS):
        score += 3
    if any(keyword in news_text for keyword in THESIS_RISK_KEYWORDS):
        score += 4

    return score

def rank_news(news_items: list[NewsItem]) -> list[NewsItem]:
    """Rank the news items based on their scores and return the top items"""
    return sorted(news_items, key=score_news, reverse=True)
