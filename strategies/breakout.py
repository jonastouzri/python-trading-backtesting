class BreakoutStrategy:
    """
    Simple Breakout Strategy:
    - Buy if current close > max(high of last N candles)
    - Sell signal is handled by engine or SL/TP
    """
    def __init__(self, lookback=20):
        self.lookback = lookback

    def generate_signal(self, index, data):
        # Keine Signale, wenn wir nicht genug Kerzen haben
        if index < self.lookback:
            return None

        current_close = data[index]["close"]
        past_highs = [data[i]["high"] for i in range(index - self.lookback, index)]

        if current_close > max(past_highs):
            return "buy"

        # Kein expliziter sell, Engine übernimmt
        return None
