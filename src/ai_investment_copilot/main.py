from ai_investment_copilot.news_ingest import load_news
from ai_investment_copilot.build_digest import build_digest, save_digest
from ai_investment_copilot.ranker import rank_news

def main() -> None:
    news_items = load_news("data/fixtures/mock_news.json")
    ranked_news = rank_news(news_items)
    markdown = build_digest(ranked_news)
    save_digest(markdown, "data/output/daily_digest.md")

if __name__ == "__main__":
    main()