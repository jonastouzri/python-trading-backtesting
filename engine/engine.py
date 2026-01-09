class BacktestEngine:
    def __init__(self, data, portfolio, strategy):
        self.data = data
        self.portfolio = portfolio
        self.strategy = strategy

    def run(self):
        for i, candle in enumerate(self.data):
            price = candle["close"]
            high = candle["high"]
            low = candle["low"]

            # -------- Entry --------
            signal = self.strategy.generate_signal(i, self.data)
            if signal == "buy":
                entry = price
                sl = entry - 10.0
                tp = entry + 20.0
                self.portfolio.open_position(entry, i, sl, tp)

            # -------- Exit --------
            if self.portfolio.position_open:
                exit_price = None
                exit_type = None

                # Intrabar SL/TP prüfen
                if low <= self.portfolio.sl:
                    exit_price = self.portfolio.sl
                    exit_type = "sl"
                elif high >= self.portfolio.tp:
                    exit_price = self.portfolio.tp
                    exit_type = "tp"
                # Strategy Exit
                elif signal == "sell":
                    exit_price = price
                    exit_type = "strategy"

                if exit_price is not None:
                    # Vertikale Linie auf Close der Kerze, nicht auf Eintrittspunkt der Bedingung
                    self.portfolio.close_position(exit_price, i, exit_type=exit_type)

            # -------- Equity Update --------
            self.portfolio.update_equity()
