class Portfolio:
    def __init__(self, initial_cash: float = 10_000.0):
        self.initial_cash = initial_cash
        self.cash = initial_cash

        self.position_open = False
        self.entry_price = None
        self.entry_index = None

        self.trades = []

        # Equity indexed by candle index
        self.equity_curve = [initial_cash]

    def open_position(self, price: float, index: int):
        if self.position_open:
            return  # ignore signal

        self.position_open = True
        self.entry_price = price
        self.entry_index = index

    def close_position(self, price: float, index: int):
        if not self.position_open:
            return

        pnl = price - self.entry_price
        self.cash += pnl

        trade = {
            "entry_index": self.entry_index,
            "exit_index": index,
            "entry_price": self.entry_price,
            "exit_price": price,
            "pnl": pnl,
        }
        self.trades.append(trade)

        self.position_open = False
        self.entry_price = None
        self.entry_index = None

    def update_equity(self):
        """
        Call once per candle.
        Equity only changes when cash changes (i.e. after trade close).
        """
        self.equity_curve.append(self.cash)
