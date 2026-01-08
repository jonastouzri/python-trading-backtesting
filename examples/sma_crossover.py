from collections import deque
from typing import Dict

from engine.engine import BacktestEngine
from engine.portfolio import Portfolio


class SMACrossoverStrategy:
    """
    Simple moving average crossover strategy.

    Assumptions:
    - Uses closing prices only
    - Generates:
        - "buy"  when short SMA crosses above long SMA
        - "sell" when short SMA crosses below long SMA
        - "hold" otherwise
    """

    def __init__(self, short_window: int, long_window: int):
        if short_window >= long_window:
            raise ValueError("short_window must be smaller than long_window")

        self.short_window = short_window
        self.long_window = long_window

        self.prices = deque(maxlen=long_window)
        self.prev_signal = "hold"

    def __call__(self, candle: Dict) -> str:
        price = candle["close"]
        self.prices.append(price)

        if len(self.prices) < self.long_window:
            return "hold"

        short_sma = sum(list(self.prices)[-self.short_window:]) / self.short_window
        long_sma = sum(self.prices) / self.long_window

        if short_sma > long_sma and self.prev_signal != "buy":
            self.prev_signal = "buy"
            return "buy"

        if short_sma < long_sma and self.prev_signal != "sell":
            self.prev_signal = "sell"
            return "sell"

        return "hold"


if __name__ == "__main__":
    # Example OHLC data (replace with real historical data)
    data = [
        {"open": 100, "high": 101, "low": 99, "close": 100},
        {"open": 100, "high": 102, "low": 99, "close": 101},
        {"open": 101, "high": 103, "low": 100, "close": 102},
        {"open": 102, "high": 104, "low": 101, "close": 101},
        {"open": 101, "high": 103, "low": 100, "close": 99},
        {"open": 99, "high": 100, "low": 97, "close": 98},
    ]

    portfolio = Portfolio(initial_cash=10_000)
    strategy = SMACrossoverStrategy(short_window=2, long_window=4)

    engine = BacktestEngine(
        data=data,
        portfolio=portfolio,
        strategy=strategy,
    )

    engine.run()

    print("Final equity:", portfolio.equity_curve[-1])
    print("Max drawdown:", portfolio.max_drawdown())
    print("Trades:", portfolio.trades)
