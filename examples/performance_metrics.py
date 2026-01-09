from engine.portfolio import Portfolio
from engine.engine import BacktestEngine
from data.csv_loader import load_ohlc_csv
from examples.sma_crossover import SMACrossoverStrategy
import numpy as np


def calculate_metrics(portfolio: Portfolio):
    """
    Compute basic performance metrics:
    - Total Return
    - CAGR (approximate)
    - Max Drawdown
    - Winrate
    """
    equity = np.array(portfolio.equity_curve)
    total_return = (equity[-1] / equity[0]) - 1

    # Approximate CAGR assuming daily bars
    num_days = len(equity) - 1  # exclude initial cash
    cagr = (equity[-1] / equity[0]) ** (252 / num_days) - 1  # 252 trading days/year

    # Max Drawdown
    peak = equity[0]
    max_dd = 0
    for value in equity:
        if value > peak:
            peak = value
        drawdown = peak - value
        if drawdown > max_dd:
            max_dd = drawdown

    # Winrate: % profitable trades
    if portfolio.trades:
        wins = sum(1 for t in portfolio.trades if t.get("pnl", 0) > 0)
        winrate = wins / len(portfolio.trades)
    else:
        winrate = 0

    return {
        "Total Return": total_return,
        "CAGR": cagr,
        "Max Drawdown": max_dd,
        "Winrate": winrate,
        "Number of Trades": len(portfolio.trades),
    }


def main():
    csv_path = "../data/XAUUSD_PERIOD_15_SHORT.csv"

    data = load_ohlc_csv(filepath=csv_path, time_format="%Y.%m.%d %H:%M:%S")

    portfolio = Portfolio(initial_cash=10_000)
    strategy = SMACrossoverStrategy(short_window=20, long_window=50)
    engine = BacktestEngine(data=data, portfolio=portfolio, strategy=strategy)

    engine.run()

    metrics = calculate_metrics(portfolio)
    print("\nPerformance Metrics:")
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")


if __name__ == "__main__":
    main()
