import matplotlib.pyplot as plt

from engine.engine import BacktestEngine
from engine.portfolio import Portfolio
from data.csv_loader import load_ohlc_csv
from examples.sma_crossover import SMACrossoverStrategy


def plot_trade_timeline(data, portfolio):
    closes = [candle["close"] for candle in data]
    x = list(range(len(closes)))

    fig, (ax_price, ax_equity) = plt.subplots(
        2, 1, figsize=(14, 8), sharex=True
    )

    # -------- Price Plot --------
    ax_price.plot(x, closes, label="Close Price")
    ax_price.set_title("Price with Trade Entries / Exits")
    ax_price.set_ylabel("Price")

    for trade in portfolio.trades:
        ax_price.axvline(
            trade["entry_index"], linestyle="--", alpha=0.4
        )
        ax_price.axvline(
            trade["exit_index"], linestyle="-", alpha=0.4
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
        filepath="data/XAUUSD.csv",
        time_format="%Y-%m-%d %H:%M:%S",
    )

    portfolio = Portfolio(initial_cash=10_000)
    strategy = SMACrossoverStrategy(short_window=20, long_window=50)
    engine = BacktestEngine(data, portfolio, strategy)

    engine.run()

    plot_trade_timeline(data, portfolio)


if __name__ == "__main__":
    main()
