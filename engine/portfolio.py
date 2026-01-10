from engine.trade import Trade


class Portfolio:
    def __init__(self):
        self.trades = []
        self.current_trade = None
        self.equity_curve = []

    def open_trade(self, price, index, sl, tp):
        """
        Öffnet einen neuen Trade mit SL/TP
        """
        self.current_trade = Trade(
            entry_price=price,
            entry_index=index,
            sl=sl,
            tp=tp
        )
        self.trades.append(self.current_trade)

    def close_trade(self, price, index):
        """
        Schließt aktuellen Trade
        """
        if self.current_trade is not None:
            self.current_trade.exit_price = price
            self.current_trade.exit_index = index
            self.current_trade = None

    def update_equity(self):
        """
        Equity Curve aktualisieren:
        - Nur abgeschlossene Trades werden berücksichtigt
        - Offene Trades beeinflussen die Equity nicht
        """
        if not self.trades:
            equity = 0
        else:
            equity = sum([t.profit for t in self.trades if t.is_closed])

        self.equity_curve.append(equity)
