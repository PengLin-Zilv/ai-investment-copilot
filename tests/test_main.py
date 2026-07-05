from importlib import import_module

from ai_investment_copilot.models.news import NewsItem

app_main = import_module("ai_investment_copilot.main")


def test_main_uses_watchlist_ticker_news_without_webhook(monkeypatch):
    calls = {}
    news_item = NewsItem(
        id="NVDA-story-1",
        ticker="NVDA",
        title="Nvidia AI chip news",
        source="Reuters",
        url="https://example.com/nvda",
        published_at="2026-07-04T12:00:00Z",
        category="general",
        themes=["AI chip"],
        summary="Nvidia AI chip news",
    )

    def fake_load_ticker_news(tickers):
        calls["tickers"] = tickers
        return [news_item]

    def fake_save_digest(markdown, output_path):
        calls["markdown"] = markdown
        calls["output_path"] = output_path

    monkeypatch.setattr(app_main, "load_ticker_news", fake_load_ticker_news)
    monkeypatch.setattr(app_main, "rank_news", lambda items: items)
    monkeypatch.setattr(app_main, "build_digest", lambda items: "full digest")
    monkeypatch.setattr(app_main, "build_discord_digest", lambda items, price_moves: calls.update(discord_digest=True))
    monkeypatch.setattr(app_main, "get_price_moves", lambda tickers: calls.update(price_moves=True))
    monkeypatch.setattr(app_main, "save_digest", fake_save_digest)
    monkeypatch.setattr(app_main, "send_discord_message", lambda markdown, webhook_url: calls.update(discord=True))
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", "")

    app_main.main()

    assert calls["tickers"] == app_main.WATCHLIST
    assert calls["markdown"] == "full digest"
    assert calls["output_path"] == "data/output/daily_digest.md"
    assert "price_moves" not in calls
    assert "discord_digest" not in calls
    assert "discord" not in calls


def test_main_sends_digest_to_discord_when_webhook_is_configured(monkeypatch):
    calls = {}
    news_item = NewsItem(
        id="NVDA-story-1",
        ticker="NVDA",
        title="Nvidia AI chip news",
        source="Reuters",
        url="https://example.com/nvda",
        published_at="2026-07-04T12:00:00Z",
        category="general",
        themes=["AI chip"],
        summary="Nvidia AI chip news",
    )

    def fake_send_discord_message(markdown, webhook_url):
        calls["discord_markdown"] = markdown
        calls["webhook_url"] = webhook_url

    monkeypatch.setattr(app_main, "load_ticker_news", lambda tickers: [news_item])
    monkeypatch.setattr(app_main, "rank_news", lambda items: items)
    monkeypatch.setattr(app_main, "build_digest", lambda items: "full digest")
    monkeypatch.setattr(app_main, "get_price_moves", lambda tickers: {"NVDA": 2.4})
    monkeypatch.setattr(
        app_main,
        "build_discord_digest",
        lambda items, price_moves: f"discord digest {price_moves['NVDA']}",
    )
    monkeypatch.setattr(app_main, "save_digest", lambda markdown, output_path: None)
    monkeypatch.setattr(app_main, "send_discord_message", fake_send_discord_message)
    monkeypatch.setenv("DISCORD_WEBHOOK_URL", "https://discord.test/webhook")

    app_main.main()

    assert calls["discord_markdown"] == "discord digest 2.4"
    assert calls["webhook_url"] == "https://discord.test/webhook"
