class BacktestEngine:
    def __init__(self, data, portfolio, strategy):
        self.data = data
        self.portfolio = portfolio
        self.strategy = strategy

    def run(self):
        for i, candle in enumerate(self.data):
            close_price = candle["close"]
            high = candle["high"]
            low = candle["low"]

            signal = self.strategy.generate_signal(i, self.data)

            # -------- Entry --------
            if signal == "buy" and not self.portfolio.position_open:
                entry = close_price
                sl = entry - 10.0
                tp = entry + 20.0
                self.portfolio.open_position(entry, i, sl, tp)

            # -------- Exit --------
            if self.portfolio.position_open:
                trade = self.portfolio.current_trade
                exit_price = None
                exit_type = None

                if low <= trade.sl:
                    exit_price = trade.sl
                    exit_type = "sl"
                elif high >= trade.tp:
                    exit_price = trade.tp
                    exit_type = "tp"
                elif signal == "sell":
                    exit_price = close_price
                    exit_type = "strategy"

                if exit_price is not None:
                    self.portfolio.close_position(exit_price, i, exit_type)

            self.portfolio.update_equity()
