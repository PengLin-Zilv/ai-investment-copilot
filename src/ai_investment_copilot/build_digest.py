"""
This script turns list[NewsItem] to daily_digest.md
"""
from pathlib import Path
from ai_investment_copilot.models.news import NewsItem
from ai_investment_copilot.ranker import score_news

def build_digest(news_items: list[NewsItem]) -> str:
    """Build a markdown digest from news items."""
    lines = ["# Daily Market Digest", ""]

    for item in news_items:
        score = score_news(item)
        lines.append(f"## {item.ticker}: {item.title}")
        lines.append(f"- Priority: {score.value}")
        lines.append(f"- Why it matters: {', '.join(score.reasons)}")
        lines.append(f"- Themes: {', '.join(item.themes)}")
        lines.append(f"- Source: {item.url}")
        lines.append(f"- Summary: {item.summary}")
        lines.append("")

    return "\n".join(lines)

def save_digest(markdown: str, output_path: str) -> None:
    """Save markdown text to a file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown, encoding="utf-8")