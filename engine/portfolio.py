from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Trade:
    entry_price: float
    exit_price: float
    pnl: float


class Portfolio:
    """
    Minimal portfolio implementation for backtesting.

    Assumptions:
    - single position at a time (long only)
    - fixed position size = 1 unit
    - no transaction costs
    """

    def __init__(self, initial_cash: float):
        self.initial_cash = initial_cash
        self.cash = initial_cash

        self.position_open: bool = False
        self.entry_price: Optional[float] = None

        self.trades: List[Trade] = []
        self.equity_curve: List[float] = [initial_cash]

    def open_position(self, price: float) -> None:
        if self.position_open:
            raise RuntimeError("Position already open")

        self.position_open = True
        self.entry_price = price

    def close_position(self, price: float) -> None:
        if not self.position_open or self.entry_price is None:
            raise RuntimeError("No open position to close")

        pnl = price - self.entry_price
        self.cash += pnl

        self.trades.append(
            Trade(
                entry_price=self.entry_price,
                exit_price=price,
                pnl=pnl,
            )
        )

        self.position_open = False
        self.entry_price = None

    def update_equity(self, current_price: float) -> None:
        """
        Update equity curve.
        If a position is open, unrealized PnL is included.
        """
        equity = self.cash

        if self.position_open and self.entry_price is not None:
            equity += current_price - self.entry_price

        self.equity_curve.append(equity)

    def max_drawdown(self) -> float:
        """
        Compute maximum drawdown from equity curve.
        """
        peak = self.equity_curve[0]
        max_dd = 0.0

        for equity in self.equity_curve:
            if equity > peak:
                peak = equity

            drawdown = peak - equity
            if drawdown > max_dd:
                max_dd = drawdown

        return max_dd
