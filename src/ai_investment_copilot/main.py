import os

from dotenv import load_dotenv

from ai_investment_copilot.build_digest import build_digest, build_discord_digest, save_digest
from ai_investment_copilot.discord_delivery import send_discord_message
from ai_investment_copilot.market_data import get_price_moves
from ai_investment_copilot.news_ingest import load_ticker_news
from ai_investment_copilot.ranker import rank_news

WATCHLIST = ["NVDA", "TSM", "PLTR"]

def main() -> None:
    load_dotenv()
    news_items = load_ticker_news(WATCHLIST)
    ranked_news = rank_news(news_items)
    markdown = build_digest(ranked_news)
    save_digest(markdown, "data/output/daily_digest.md")

    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if webhook_url:
        price_moves = get_price_moves(WATCHLIST)
        discord_markdown = build_discord_digest(ranked_news, price_moves)
        send_discord_message(discord_markdown, webhook_url)

if __name__ == "__main__":
    main()
