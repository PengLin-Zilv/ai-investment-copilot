"""
This script turns list[NewsItem] to daily_digest.md
"""
from pathlib import Path
from ai_investment_copilot.models.news import NewsItem
from ai_investment_copilot.ranker import score_news

DISCORD_MESSAGE_LIMIT = 1900

SIGNAL_REASON_TEXT = {
    "Financial category": "Financial results or cash-flow signal",
    "Contract category": "Contract or partnership signal",
    "Risk category": "Thesis risk signal",
    "Thesis risk keyword": "Thesis risk signal",
    "AI infrastructure keyword": "AI infrastructure relevance",
}

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


def build_discord_digest(
    news_items: list[NewsItem],
    price_moves: dict[str, float] | None = None,
    max_items: int = 5,
) -> str:
    """Build a compact Discord notification from ranked news items."""
    price_moves = price_moves or {}
    lines = ["# Daily Market Signals", ""]
    included_count = 0

    for item in news_items:
        score = score_news(item)
        if score.value <= 0:
            continue

        block = [
            f"**{item.ticker}**: [{item.title}]({item.url})",
        ]
        move = price_moves.get(item.ticker)
        if move is not None and abs(move) > 2:
            block.append(f"Move: {move:+.1f}%")

        signal = _signal_text(score.reasons)
        if signal:
            block.append(f"Signal: {signal}")

        block.append(f"Why it matters: {_truncate(item.summary, 280)}")
        block.append("")

        candidate_lines = lines + block
        if len("\n".join(candidate_lines)) > DISCORD_MESSAGE_LIMIT:
            break

        lines = candidate_lines
        included_count += 1
        if included_count >= max_items:
            break

    if included_count == 0:
        return "# Daily Market Signals\n\nNo high-priority thesis signals today."

    return "\n".join(lines).rstrip()


def save_digest(markdown: str, output_path: str) -> None:
    """Save markdown text to a file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown, encoding="utf-8")


def _signal_text(reasons: list[str]) -> str:
    seen = []
    for reason in reasons:
        text = SIGNAL_REASON_TEXT.get(reason)
        if text and text not in seen:
            seen.append(text)

    return "; ".join(seen)


def _truncate(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text

    return text[: max_length - 3].rstrip() + "..."
