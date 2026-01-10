class Trade:
    def __init__(self, entry_price, entry_index, sl, tp):
        self.entry_price = entry_price
        self.entry_index = entry_index
        self.sl = sl
        self.tp = tp
        self.exit_price = None
        self.exit_index = None

    @property
    def is_closed(self):
        return self.exit_price is not None
