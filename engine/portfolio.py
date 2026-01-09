class Portfolio:
    def __init__(self, initial_cash: float = 10_000.0):
        self.initial_cash = initial_cash
        self.cash = initial_cash

        self.position_open = False
        self.entry_price = None
        self.entry_index = None
        self.sl = None
        self.tp = None

        self.trades = []
        self.equity_curve = [initial_cash]

    def open_position(self, price: float, index: int, sl: float, tp: float):
        if self.position_open:
            return  # ignore signal

        self.position_open = True
        self.entry_price = price
        self.entry_index = index
        self.sl = sl
        self.tp = tp

    def close_position(self, price: float, index: int, exit_type: str = "strategy"):
        """
        exit_type: "strategy" | "sl" | "tp"
        """
        if not self.position_open:
            return

        pnl = price - self.entry_price
        self.cash += pnl

        trade = {
            "entry_index": self.entry_index,
            "exit_index": index,
            "entry_price": self.entry_price,
            "exit_price": price,
            "sl": self.sl,
            "tp": self.tp,
            "pnl": pnl,
            "exit_type": exit_type,  # sehr wichtig für Linienfarbe
        }
        self.trades.append(trade)

        # Position zurücksetzen
        self.position_open = False
        self.entry_price = None
        self.entry_index = None
        self.sl = None
        self.tp = None

    def update_equity(self):
        """Call once per candle. Equity changes only when a trade is closed."""
        self.equity_curve.append(self.cash)
