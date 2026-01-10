class SMACrossoverStrategy:
    def __init__(self, short_window: int = 20, long_window: int = 50):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signal(self, index: int, data):
        if index < self.long_window:
            return None

        closes = [c["close"] for c in data]

        short_sma_prev = sum(
            closes[index - self.short_window - 1 : index - 1]
        ) / self.short_window
        long_sma_prev = sum(
            closes[index - self.long_window - 1 : index - 1]
        ) / self.long_window

        short_sma_curr = sum(
            closes[index - self.short_window : index]
        ) / self.short_window
        long_sma_curr = sum(
            closes[index - self.long_window : index]
        ) / self.long_window

        # Bullish crossover
        if short_sma_prev <= long_sma_prev and short_sma_curr > long_sma_curr:
            return "buy"

        # Bearish crossover
        if short_sma_prev >= long_sma_prev and short_sma_curr < long_sma_curr:
            return "sell"

        return None
