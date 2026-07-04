from ai_investment_copilot.build_digest import build_discord_digest
from ai_investment_copilot.models.news import NewsItem


def make_news_item(
    item_id: str,
    ticker: str,
    title: str,
    category: str,
    themes: list[str],
    summary: str,
) -> NewsItem:
    return NewsItem(
        id=item_id,
        ticker=ticker,
        title=title,
        source="Reuters",
        url=f"https://example.com/{item_id}",
        published_at="2026-07-04T12:00:00Z",
        category=category,
        themes=themes,
        summary=summary,
    )


def test_build_discord_digest_formats_human_readable_signals():
    item = make_news_item(
        item_id="tsm-ai-chip-deal",
        ticker="TSM",
        title="Meta Eyes $6.5 Billion Samsung AI Chip Deal",
        category="contract",
        themes=["AI infrastructure", "AI chip", "semiconductor"],
        summary="Meta is reportedly discussing a large AI chip deal that may shift foundry demand.",
    )

    markdown = build_discord_digest([item], price_moves={"TSM": 2.4})

    assert markdown.startswith("# Daily Market Signals")
    assert "**TSM**: [Meta Eyes $6.5 Billion Samsung AI Chip Deal](https://example.com/tsm-ai-chip-deal)" in markdown
    assert "Move: +2.4%" in markdown
    assert "Signal: Contract or partnership signal; AI infrastructure relevance" in markdown
    assert "Why it matters: Meta is reportedly discussing a large AI chip deal that may shift foundry demand." in markdown
    assert "Priority:" not in markdown
    assert "keyword" not in markdown


def test_build_discord_digest_skips_low_score_and_small_price_moves():
    relevant_item = make_news_item(
        item_id="nvda-ai-chip-news",
        ticker="NVDA",
        title="Nvidia AI chip demand remains strong",
        category="general",
        themes=["AI chip"],
        summary="Demand for AI chips remains a useful signal for infrastructure growth.",
    )
    noise_item = make_news_item(
        item_id="pltr-stock-commentary",
        ticker="PLTR",
        title="Palantir stock commentary",
        category="general",
        themes=["general"],
        summary="Generic market commentary.",
    )

    markdown = build_discord_digest(
        [relevant_item, noise_item],
        price_moves={"NVDA": 1.9, "PLTR": 3.1},
    )

    assert "Nvidia AI chip demand remains strong" in markdown
    assert "Palantir stock commentary" not in markdown
    assert "Move:" not in markdown
    assert len(markdown) <= 1900
