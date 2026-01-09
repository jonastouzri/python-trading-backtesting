class BacktestEngine:
    def __init__(self, data, portfolio, strategy):
        """
        data: list of dicts with keys: open, high, low, close, time (optional)
        portfolio: Portfolio instance
        strategy: Strategy with generate_signal(index, data) -> "buy", "sell" or None
        """
        self.data = data
        self.portfolio = portfolio
        self.strategy = strategy

    def run(self):
        for i, candle in enumerate(self.data):
            signal = self.strategy.generate_signal(i, self.data)
            print(i)
            # Entry
            if signal == "buy":
                self.portfolio.open_position(
                    price=candle["close"],
                    index=i,
                )

            # Exit
            elif signal == "sell":
                self.portfolio.close_position(
                    price=candle["close"],
                    index=i,
                )

            # Equity is updated once per candle (event-based)
            self.portfolio.update_equity()
