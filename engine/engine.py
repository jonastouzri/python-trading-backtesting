from typing import Iterable, Dict, Callable
from .portfolio import Portfolio


class BacktestEngine:
    """
    Minimal backtesting engine.

    Assumptions:
    - OHLC data provided as iterable of dicts
    - single strategy function producing buy/sell signals
    - one position at a time (handled by Portfolio)
    """

    def __init__(
        self,
        data: Iterable[Dict],
        portfolio: Portfolio,
        strategy: Callable[[Dict], str],
    ):
        """
        Parameters
        ----------
        data : iterable of dict
            Each element represents one candle (e.g. OHLC).
        portfolio : Portfolio
            Portfolio instance managing positions and equity.
        strategy : callable
            Function that receives a candle and returns:
            - "buy"
            - "sell"
            - "hold"
        """
        self.data = data
        self.portfolio = portfolio
        self.strategy = strategy

    def run(self) -> None:
        """
        Run backtest over the provided data.
        """
        for candle in self.data:
            signal = self.strategy(candle)
            price = candle["close"]

            if signal == "buy" and not self.portfolio.position_open:
                self.portfolio.open_position(price)

            elif signal == "sell" and self.portfolio.position_open:
                self.portfolio.close_position(price)

            # Update equity on every candle
            self.portfolio.update_equity(price)
