class BacktestEngine:
    """
    Core Backtesting Engine mit SL/TP + Intrabar-Exit
    """

    def __init__(self, data, portfolio, strategy):
        self.data = data
        self.portfolio = portfolio
        self.strategy = strategy

    def run(self):
        for i in range(len(self.data)):
            # Strategie-Signal
            signal_data = self.strategy.generate_signal(i, self.data)

            # Trade öffnen
            if self.portfolio.current_trade is None and signal_data is not None:
                if signal_data["signal"] == "buy":
                    self.portfolio.open_trade(
                        price=self.data[i]["close"],
                        index=i,
                        sl=signal_data["sl"],
                        tp=signal_data["tp"]
                    )

            # Intrabar SL/TP prüfen
            if self.portfolio.current_trade is not None:
                trade = self.portfolio.current_trade
                low = self.data[i]["low"]
                high = self.data[i]["high"]

                if low <= trade.sl:
                    self.portfolio.close_trade(price=trade.sl, index=i)
                elif high >= trade.tp:
                    self.portfolio.close_trade(price=trade.tp, index=i)

            # Equity aktualisieren
            self.portfolio.update_equity()
