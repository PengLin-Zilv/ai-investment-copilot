"""Build markdown digests for files and Discord messages."""

from pathlib import Path

from ai_investment_copilot.models.news import NewsItem
from ai_investment_copilot.ranker import score_news

DISCORD_MESSAGE_LIMIT = 1900
DISCORD_MESSAGE_TITLE = "# Daily Market Signals"
DISCORD_MIN_SCORE = 4

SIGNAL_REASON_TEXT = {
    "Financial category": "Financial results or cash-flow signal",
    "Contract category": "Contract or partnership signal",
    "Risk category": "Thesis risk signal",
    "Thesis risk keyword": "Thesis risk signal",
    "AI infrastructure keyword": "AI infrastructure relevance",
}

def build_digest(news_items: list[NewsItem]) -> str:
    """Build the full daily markdown digest for the output file."""
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


def build_discord_digest_messages(
    news_items: list[NewsItem],
    price_moves: dict[str, float] | None = None,
) -> list[str]:
    """Build one or more Discord messages for news with score >= 4.

    Discord has a message length limit. This function keeps adding news items to
    the current message until the next item would make it too long. Then it
    starts a new message, so high-priority news is not dropped.
    """
    price_moves = price_moves or {}
    messages = []
    lines = [DISCORD_MESSAGE_TITLE, ""]

    for item in news_items:
        score = score_news(item)
        if score.value < DISCORD_MIN_SCORE:
            continue

        block = _discord_item_block(item, score.reasons, price_moves)
        candidate_lines = lines + block
        candidate_message = "\n".join(candidate_lines).rstrip()
        has_items = len(lines) > 2

        if len(candidate_message) > DISCORD_MESSAGE_LIMIT and has_items:
            messages.append("\n".join(lines).rstrip())
            lines = [DISCORD_MESSAGE_TITLE, ""] + block
        else:
            lines = candidate_lines

    if len(lines) == 2:
        return [f"{DISCORD_MESSAGE_TITLE}\n\nNo high-priority thesis signals today."]

    messages.append("\n".join(lines).rstrip())
    return messages


def _discord_item_block(
    item: NewsItem,
    score_reasons: list[str],
    price_moves: dict[str, float],
) -> list[str]:
    """Build the Discord text block for one news item."""
    block = [
        f"**{item.ticker}**: [{item.title}]({item.url})",
    ]
    move = price_moves.get(item.ticker)
    if move is not None and abs(move) > 2:
        block.append(f"Move: {move:+.1f}%")

    signal = _signal_text(score_reasons)
    if signal:
        block.append(f"Signal: {signal}")

    block.append(f"Why it matters: {_truncate(item.summary, 280)}")
    block.append("")
    return block


def save_digest(markdown: str, output_path: str) -> None:
    """Save markdown text to a file and create the folder if needed."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown, encoding="utf-8")


def _signal_text(reasons: list[str]) -> str:
    """Convert internal score reasons into reader-friendly signal text."""
    seen = []
    for reason in reasons:
        text = SIGNAL_REASON_TEXT.get(reason)
        if text and text not in seen:
            seen.append(text)

    return "; ".join(seen)


def _truncate(text: str, max_length: int) -> str:
    """Shorten long text so Discord messages stay compact."""
    if len(text) <= max_length:
        return text

    return text[: max_length - 3].rstrip() + "..."
