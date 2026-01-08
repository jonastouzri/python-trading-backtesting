class BacktestEngine:
    def __init__(self, data, portfolio, strategy):
        self.data = data
        self.portfolio = portfolio
        self.strategy = strategy

    def run(self):
        for i, candle in enumerate(self.data):
            signal = self.strategy(candle)
            price = candle["close"]

            if signal == "buy":
                self.portfolio.buy(price, i)
            elif signal == "sell":
                self.portfolio.sell(price, i)

            self.portfolio.update_equity(price)
