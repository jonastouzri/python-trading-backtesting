class SMACrossoverStrategy:
    def __init__(self, short_window=20, long_window=50):
        self.short_window = short_window
        self.long_window = long_window
        self.prices = []

    def __call__(self, candle):
        self.prices.append(candle["close"])
        if len(self.prices) < self.long_window:
            return None

        short_sma = sum(self.prices[-self.short_window:]) / self.short_window
        long_sma = sum(self.prices[-self.long_window:]) / self.long_window

        if short_sma > long_sma:
            return "buy"
        elif short_sma < long_sma:
            return "sell"
        else:
            return None