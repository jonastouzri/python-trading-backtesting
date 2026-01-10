class Trade:
    def __init__(self, entry_price, entry_index, sl, tp):
        self.entry_price = entry_price
        self.entry_index = entry_index
        self.sl = sl
        self.tp = tp

        self.exit_price = None
        self.exit_index = None
        self.exit_type = None
        self.profit = None


class Portfolio:
    def __init__(self, initial_balance=0.0):
        self.initial_balance = initial_balance
        self.balance = initial_balance

        self.position_open = False
        self.current_trade = None
        self.trades = []

        self.equity_curve = [initial_balance]

    def open_position(self, price, index, sl, tp):
        if self.position_open:
            return

        self.current_trade = Trade(price, index, sl, tp)
        self.position_open = True

    def close_position(self, price, index, exit_type):
        trade = self.current_trade
        trade.exit_price = price
        trade.exit_index = index
        trade.exit_type = exit_type
        trade.profit = price - trade.entry_price

        self.balance += trade.profit
        self.trades.append(trade)

        self.current_trade = None
        self.position_open = False

    def update_equity(self):
        self.equity_curve.append(self.balance)
