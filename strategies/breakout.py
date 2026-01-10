class BreakoutStrategy:
    """
    Breakout Strategy mit dynamischem SL/TP:
    - SL = niedrigster Preis der letzten 5 Kerzen
    - TP = Entry + 0.5*(Entry-SL)
    """

    def __init__(self, lookback=20, sl_lookback=5, risk_reward=0.5):
        self.lookback = lookback
        self.sl_lookback = sl_lookback
        self.risk_reward = risk_reward

    def generate_signal(self, index, data):
        if index < self.lookback:
            return None

        current_close = data[index]["close"]
        past_highs = [data[i]["high"] for i in range(index - self.lookback, index)]
        breakout_level = max(past_highs)

        if current_close > breakout_level:
            sl = min([data[i]["low"] for i in range(max(0, index - self.sl_lookback), index)])
            tp = current_close + (current_close - sl) * self.risk_reward
            return {"signal": "buy", "sl": sl, "tp": tp}

        return None
