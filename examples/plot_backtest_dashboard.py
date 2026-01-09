import matplotlib.pyplot as plt
from engine.portfolio import Portfolio
from engine.engine import BacktestEngine
from data.csv_loader import load_ohlc_csv
from examples.sma_crossover import SMACrossoverStrategy


def plot_dashboard(data, portfolio: Portfolio):
    times = [c["time"] for c in data]
    equity = portfolio.equity_curve[1:]

    buy_times, buy_equity = [], []
    sell_times, sell_equity = [], []

    for trade in portfolio.trades:
        entry_idx = trade.get("entry_index")
        exit_idx = trade.get("exit_index")

        if entry_idx is not None:
            buy_times.append(times[entry_idx])
            buy_equity.append(equity[entry_idx])

        if exit_idx is not None:
            sell_times.append(times[exit_idx])
            sell_equity.append(equity[exit_idx])

    plt.figure(figsize=(14, 7))
    plt.plot(times, equity, label="Equity Curve", color="blue")
    plt.scatter(buy_times, buy_equity, marker="^", color="green", label="Buy")
    plt.scatter(sell_times, sell_equity, marker="v", color="red", label="Sell")

    # Max Drawdown
    peak = equity[0]
    max_dd = [0]
    for value in equity:
        if value > peak:
            peak = value
        max_dd.append(peak - value)
    plt.fill_between(times, equity, [e - d for e, d in zip(equity, max_dd)], color="red", alpha=0.1, label="Drawdown")

    plt.xlabel("Time")
    plt.ylabel("Equity / Price")
    plt.title("Backtest Dashboard: Equity Curve, Trades & Drawdown")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    csv_path = "../data/XAUUSD_PERIOD_15_SHORT.csv"
    data = load_ohlc_csv(filepath=csv_path, time_format="%Y.%m.%d %H:%M:%S")

    portfolio = Portfolio(initial_cash=10_000)
    strategy = SMACrossoverStrategy(short_window=20, long_window=50)
    engine = BacktestEngine(data=data, portfolio=portfolio, strategy=strategy)
    engine.run()

    plot_dashboard(data, portfolio)


if __name__ == "__main__":
    main()
