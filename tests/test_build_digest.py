from ai_investment_copilot.build_digest import (
    DISCORD_MESSAGE_LIMIT,
    build_discord_digest_messages,
)
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


def test_build_discord_digest_messages_formats_human_readable_signals():
    item = make_news_item(
        item_id="tsm-ai-chip-deal",
        ticker="TSM",
        title="Meta Eyes $6.5 Billion Samsung AI Chip Deal",
        category="contract",
        themes=["AI infrastructure", "AI chip", "semiconductor"],
        summary="Meta is reportedly discussing a large AI chip deal that may shift foundry demand.",
    )

    markdown = build_discord_digest_messages([item], price_moves={"TSM": 2.4})[0]

    assert markdown.startswith("# Daily Market Signals")
    assert "**TSM**: [Meta Eyes $6.5 Billion Samsung AI Chip Deal](https://example.com/tsm-ai-chip-deal)" in markdown
    assert "Move: +2.4%" in markdown
    assert "Signal: Contract or partnership signal; AI infrastructure relevance" in markdown
    assert "Why it matters: Meta is reportedly discussing a large AI chip deal that may shift foundry demand." in markdown
    assert "Priority:" not in markdown
    assert "keyword" not in markdown


def test_build_discord_digest_messages_skips_low_score_and_small_price_moves():
    relevant_item = make_news_item(
        item_id="nvda-ai-chip-news",
        ticker="NVDA",
        title="Nvidia AI chip demand remains strong",
        category="contract",
        themes=["general"],
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

    markdown = build_discord_digest_messages(
        [relevant_item, noise_item],
        price_moves={"NVDA": 1.9, "PLTR": 3.1},
    )[0]

    assert "Nvidia AI chip demand remains strong" in markdown
    assert "Palantir stock commentary" not in markdown
    assert "Move:" not in markdown
    assert len(markdown) <= 1900


def test_build_discord_digest_messages_include_all_items_with_score_at_least_four():
    items = [
        make_news_item(
            item_id=f"tsm-{i}",
            ticker="TSM",
            title=f"TSM AI chip story {i}",
            category="contract",
            themes=["AI infrastructure", "AI chip"],
            summary=f"AI chip supply signal number {i}.",
        )
        for i in range(4)
    ]

    messages = build_discord_digest_messages(items)
    markdown = "\n".join(messages)

    assert markdown.count("**TSM**") == 4


def test_build_discord_digest_messages_split_when_message_limit_is_reached():
    items = [
        make_news_item(
            item_id=f"pltr-contract-{i}",
            ticker="PLTR",
            title=f"Palantir contract signal {i}",
            category="contract",
            themes=["general"],
            summary=f"Important contract signal {i}. " + ("Details matter. " * 40),
        )
        for i in range(8)
    ]

    messages = build_discord_digest_messages(items)
    markdown = "\n".join(messages)

    assert len(messages) > 1
    assert all(len(message) <= DISCORD_MESSAGE_LIMIT for message in messages)
    for item in items:
        assert item.title in markdown
