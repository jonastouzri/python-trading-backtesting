class Portfolio:
    def __init__(self, initial_cash: float):
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.position = 0
        self.trades = []
        self.equity_curve = [initial_cash]

        self._current_trade_index = None

    def buy(self, price: float, index: int):
        if self.position == 0:
            self.position = 1
            self.trades.append({
                "entry_index": index,
                "entry_price": price,
                "exit_index": None,
                "exit_price": None,
                "pnl": 0
            })
            self._current_trade_index = len(self.trades) - 1

    def sell(self, price: float, index: int):
        if self.position == 1:
            self.position = 0
            trade = self.trades[self._current_trade_index]
            trade["exit_index"] = index
            trade["exit_price"] = price
            trade["pnl"] = trade["exit_price"] - trade["entry_price"]
            self._current_trade_index = None

    def update_equity(self, current_price: float):
        equity = self.cash + self.position * current_price
        self.equity_curve.append(equity)

    def max_drawdown(self):
        peak = self.equity_curve[0]
        max_dd = 0
        for value in self.equity_curve:
            if value > peak:
                peak = value
            drawdown = peak - value
            if drawdown > max_dd:
                max_dd = drawdown
        return max_dd