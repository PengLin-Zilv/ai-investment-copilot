"""This script turns list[NewsItem] to daily_digest.md"""
from pathlib import Path
from ai_investment_copilot.models.news import NewsItem
from ai_investment_copilot.news_ingest import load_news

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
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown, encoding="utf-8")

if __name__ == "__main__":
    news_items = load_news("data/fixtures/mock_news.json")
    markdown = build_digest(news_items)
    save_digest(markdown, "data/output/daily_digest.md")