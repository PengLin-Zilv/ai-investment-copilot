import yfinance as yf

from ai_investment_copilot.yfinance_config import configure_yfinance_cache


def get_price_moves(tickers: list[str]) -> dict[str, float]:
    """Return each ticker's latest close-to-close percent move."""
    configure_yfinance_cache()
    price_moves = {}

    for ticker in tickers:
        history = yf.Ticker(ticker).history(period="5d")
        closes = history["Close"].dropna()
        if len(closes) < 2:
            continue

        previous_close = float(closes.iloc[-2])
        latest_close = float(closes.iloc[-1])
        if previous_close == 0:
            continue

        price_moves[ticker] = (latest_close - previous_close) / previous_close * 100

    return price_moves
