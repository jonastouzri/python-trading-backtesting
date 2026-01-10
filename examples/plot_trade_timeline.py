import matplotlib.pyplot as plt

from engine.engine import BacktestEngine
from engine.portfolio import Portfolio
from engine.performance_metrics import compute_performance_metrics
from strategies.sma_crossover import SMACrossoverStrategy
from utils.csv_loader import load_csv


def plot_dashboard(data, portfolio):
    prices = [c["close"] for c in data]

    fig, (ax_price, ax_equity) = plt.subplots(2, 1, sharex=True, figsize=(14, 8))

    # -------- PRICE --------
    ax_price.plot(prices, label="Price")

    for trade in portfolio.trades:
        ax_price.axvline(trade.entry_index, color="blue", linestyle="--", alpha=0.7)
        ax_price.axvline(trade.exit_index, color="black", linestyle="--", alpha=0.7)

        ax_price.hlines(
            trade.sl,
            trade.entry_index,
            trade.exit_index,
            colors="red",
            linestyles="dotted",
        )
        ax_price.hlines(
            trade.tp,
            trade.entry_index,
            trade.exit_index,
            colors="green",
            linestyles="dotted",
        )

    ax_price.set_title("Price & Trades")
    ax_price.legend()

    # -------- EQUITY --------
    ax_equity.plot(portfolio.equity_curve, label="Equity Curve")
    ax_equity.set_title("Equity Curve")
    ax_equity.legend()

    # -------- METRICS --------
    metrics = compute_performance_metrics(
        portfolio.trades, portfolio.equity_curve
    )

    text = (
        f"Trades: {metrics['trades']}\n"
        f"Winrate: {metrics['winrate']:.1f} %\n"
        f"Total PnL: {metrics['total_pnl']:.2f}\n"
        f"Max DD: {metrics['max_drawdown']:.2f}\n"
        f"Avg Win: {metrics['avg_win']:.2f}\n"
        f"Avg Loss: {metrics['avg_loss']:.2f}"
    )

    ax_equity.text(
        0.02,
        0.95,
        text,
        transform=ax_equity.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
        family="monospace",
    )

    plt.tight_layout()
    plt.show()


def main():
    data = load_csv(
        "../data/XAUUSD_PERIOD_15_SHORT.csv",
        datetime_format="%Y.%m.%d %H:%M:%S",
    )

    portfolio = Portfolio()
    strategy = SMACrossoverStrategy()
    engine = BacktestEngine(data, portfolio, strategy)
    engine.run()

    plot_dashboard(data, portfolio)


if __name__ == "__main__":
    main()
