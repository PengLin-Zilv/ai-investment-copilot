from ai_investment_copilot import market_data
from ai_investment_copilot.market_data import get_price_moves


class FakeCloseSeries:
    def __init__(self, values: list[float]):
        self.values = values

    def dropna(self):
        return self

    def __len__(self):
        return len(self.values)

    @property
    def iloc(self):
        return self

    def __getitem__(self, index: int):
        return self.values[index]


class FakeHistory:
    def __init__(self, close_values: list[float]):
        self.close_values = close_values

    def __getitem__(self, key: str):
        assert key == "Close"
        return FakeCloseSeries(self.close_values)


def test_get_price_moves_calculates_latest_vs_previous_close(monkeypatch):
    class FakeTicker:
        def __init__(self, ticker: str):
            self.ticker = ticker

        def history(self, period: str):
            assert period == "5d"
            return FakeHistory([100.0, 103.0])

    monkeypatch.setattr(market_data.yf, "Ticker", FakeTicker)
    monkeypatch.setattr(market_data, "configure_yfinance_cache", lambda: None)

    assert get_price_moves(["NVDA"]) == {"NVDA": 3.0}
