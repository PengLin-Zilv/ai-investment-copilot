"""This script turns list[NewsItem] to daily_digest.md"""

from ai_investment_copilot.models import NewsItem

def build_digest(news_items: list[NewsItem]) -> str:
    """Build a markdown digest from news items."""
    lines = ["# Daily Market Digest", ""]

    for item in news_items:
        lines.append(f"## {item.ticker}: {item.title}")
        lines.append(f"- Themes: {', '.join(item.themes)}")
        lines.append(f"- Source: {item.url}")
        lines.append(f"- Summary: {item.summary}")
        lines.append("")

    return "\n".join(lines)
   
   

def save_digest(markdown: str, output_path: str) -> None:
    """Save markdown text to a file."""