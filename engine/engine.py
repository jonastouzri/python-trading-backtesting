class BacktestEngine:
    def __init__(self, data, portfolio, strategy):
        self.data = data
        self.portfolio = portfolio
        self.strategy = strategy

    def run(self):
        for i, candle in enumerate(self.data):
            price = candle["close"]

            # -------- Entry --------
            signal = self.strategy.generate_signal(i, self.data)
            if signal == "buy":
                entry = price
                sl = entry - 10.0
                tp = entry + 20.0
                self.portfolio.open_position(entry, i, sl, tp)

            # -------- Exit --------
            if self.portfolio.position_open:
                # SL/TP Check
                if price <= self.portfolio.sl or price >= self.portfolio.tp:
                    self.portfolio.close_position(price, i)

                # Strategy Exit
                elif signal == "sell":
                    self.portfolio.close_position(price, i)

            # -------- Equity Update --------
            self.portfolio.update_equity()
