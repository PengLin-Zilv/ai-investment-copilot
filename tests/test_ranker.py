from ai_investment_copilot.models.news import NewsItem
from ai_investment_copilot.ranker import rank_news, score_news


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
        published_at="2026-06-27T14:00:00Z",
        category=category,
        themes=themes,
        summary=summary,
    )


def test_score_news_rewards_long_term_thesis_evidence():
    item = make_news_item(
        item_id="tsm-q2-revenue",
        ticker="TSM",
        title="TSMC reports record Q2 revenue on AI chip demand",
        category="revenue",
        themes=["semiconductor manufacturing", "AI chip", "revenue"],
        summary="Revenue beat estimates on demand for advanced AI chips.",
    )

    assert score_news(item) == 8


def test_rank_news_orders_thesis_impact_before_narrow_contract_news():
    thesis_risk = make_news_item(
        item_id="nvda-export-regulation",
        ticker="NVDA",
        title="NVDA shares fall after export restriction",
        category="regulation",
        themes=["AI infrastructure", "semiconductor", "export control"],
        summary="New export restrictions may affect Nvidia chip sales.",
    )
    financial_evidence = make_news_item(
        item_id="tsm-q2-revenue",
        ticker="TSM",
        title="TSMC reports record Q2 revenue on AI chip demand",
        category="revenue",
        themes=["semiconductor manufacturing", "AI chip", "revenue"],
        summary="Revenue beat estimates on demand for advanced AI chips.",
    )
    narrow_contract = make_news_item(
        item_id="pltr-army-contract",
        ticker="PLTR",
        title="Palantir wins Army contract",
        category="contract",
        themes=["software"],
        summary="Palantir won a contract to expand an Army AI system.",
    )

    ranked = rank_news([narrow_contract, financial_evidence, thesis_risk])

    assert ranked == [thesis_risk, financial_evidence, narrow_contract]
