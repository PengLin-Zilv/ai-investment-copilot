"""Score and sort news by how useful it is for the daily digest."""

from dataclasses import dataclass

from ai_investment_copilot.models.news import NewsItem

@dataclass
class NewsScore:
    """Score result for one news item.

    value is the numeric priority. reasons explains why the item received that
    score, so the digest can show a human-readable signal.
    """

    value: int
    reasons: list[str]

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

def score_news(news: NewsItem) -> NewsScore:
    """Return the priority score and reasons for one news item."""
    score = 0
    reasons = []
    category = news.category.lower()
    themes_text = " ".join(news.themes).lower()
    news_text = f"{news.title} {news.summary}".lower()

    if category in FINANCIAL_CATEGORIES:
        score += 5
        reasons.append("Financial category")
    if category in CONTRACT_CATEGORIES:
        score += 4
        reasons.append("Contract category")
    if category in RISK_CATEGORIES:
        score += 4
        reasons.append("Risk category")
    if any(keyword in news_text for keyword in THESIS_RISK_KEYWORDS):
        score += 3
        reasons.append("Thesis risk keyword")
    if any(keyword in themes_text for keyword in AI_INFRA_KEYWORDS):
        score += 3
        reasons.append("AI infrastructure keyword")


    return NewsScore(value=score, reasons=reasons)

def rank_news(news_items: list[NewsItem]) -> list[NewsItem]:
    """Sort news items from highest score to lowest score."""
    return sorted(news_items, key=lambda news: score_news(news).value, reverse=True)
