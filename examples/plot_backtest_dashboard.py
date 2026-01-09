import matplotlib.pyplot as plt

from engine.engine import BacktestEngine
from engine.portfolio import Portfolio
from data.csv_loader import load_ohlc_csv
from examples.sma_crossover import SMACrossoverStrategy


def plot_trade_timeline(data, portfolio):
    closes = [c["close"] for c in data]
    x = list(range(len(closes)))

    fig, (ax_price, ax_equity) = plt.subplots(
        2, 1, figsize=(14, 8), sharex=True
    )

    # -------- Price Plot --------
    ax_price.plot(x, closes, label="Close Price")
    ax_price.set_title("Price with Trades, SL & TP")
    ax_price.set_ylabel("Price")

    for trade in portfolio.trades:
        entry_i = trade["entry_index"]
        exit_i = trade["exit_index"]

        # Entry / Exit
        ax_price.axvline(entry_i, linestyle="--", alpha=0.4)
        ax_price.axvline(exit_i, linestyle="-", alpha=0.4)

        # SL / TP (only during trade)
        ax_price.hlines(
            trade["sl"],
            entry_i,
            exit_i,
            linestyles="dotted",
            alpha=0.6,
        )
        ax_price.hlines(
            trade["tp"],
            entry_i,
            exit_i,
            linestyles="dotted",
            alpha=0.6,
        )

    ax_price.legend()

    # -------- Equity Plot --------
    equity_x = list(range(len(portfolio.equity_curve)))
    ax_equity.step(
        equity_x,
        portfolio.equity_curve,
        where="post",
        label="Equity Curve",
    )

    ax_equity.set_title("Equity Curve (Realized PnL Only)")
    ax_equity.set_xlabel("Candle Index")
    ax_equity.set_ylabel("Equity")
    ax_equity.legend()

    plt.tight_layout()
    plt.show()


def main():
    data = load_ohlc_csv(
        filepath="../data/XAUUSD_PERIOD_15_SHORT.csv",
        time_format="%Y.%m.%d %H:%M:%S",
    )

    portfolio = Portfolio(initial_cash=10_000)
    strategy = SMACrossoverStrategy(short_window=20, long_window=50)
    engine = BacktestEngine(data, portfolio, strategy)

    engine.run()

    plot_trade_timeline(data, portfolio)


if __name__ == "__main__":
    main()
