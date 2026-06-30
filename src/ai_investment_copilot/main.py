from ai_investment_copilot.news_ingest import load_news
from ai_investment_copilot.build_digest import build_digest, save_digest

def main() -> None:
    news_items = load_news("data/fixtures/mock_news.json")
    markdown = build_digest(news_items)
    save_digest(markdown, "data/output/daily_digest.md")

if __name__ == "__main__":
    main()