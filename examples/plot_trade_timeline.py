import matplotlib.pyplot as plt

from engine.engine import BacktestEngine
from engine.portfolio import Portfolio
from data.csv_loader import load_ohlc_csv
from examples.sma_crossover import SMACrossoverStrategy


def plot_trade_timeline(data, portfolio):
    closes = [c["close"] for c in data]
    x = list(range(len(closes)))

    fig, (ax_price, ax_equity) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

    # -------- Price Plot --------
    ax_price.plot(x, closes, label="Close Price")
    ax_price.set_title("Price with Trades, SL/TP & Strategy Exit")
    ax_price.set_ylabel("Price")

    for trade in portfolio.trades:
        entry_i = trade["entry_index"]
        exit_i = trade["exit_index"]
        pnl = trade["pnl"]
        exit_type = trade["exit_type"]

        # Hintergrundfarbe nach PnL
        bg_color = "green" if pnl > 0 else "red"

        # Linienfarbe nach Exit-Type
        if exit_type == "sl":
            line_color = "red"
            arrow_color = "red"
            arrow_symbol = "▼"
        elif exit_type == "tp":
            line_color = "green"
            arrow_color = "green"
            arrow_symbol = "▲"
        else:  # strategy exit
            line_color = "grey"
            arrow_color = "grey"
            arrow_symbol = "▼"  # Strategy Exit Long = Pfeil nach unten

        # Entry / Exit vertikal
        ax_price.axvline(entry_i, linestyle="--", alpha=0.4)
        ax_price.axvline(exit_i, linestyle="-", alpha=0.4)

        # SL/TP horizontale Linie
        ax_price.hlines(trade["sl"], entry_i, exit_i, linestyles="dotted", color=line_color, alpha=0.6)
        ax_price.hlines(trade["tp"], entry_i, exit_i, linestyles="dotted", color=line_color, alpha=0.6)

        # Trade Hintergrund
        ax_price.axvspan(entry_i, exit_i, color=bg_color, alpha=0.1)

        # -------- Exit-Pfeil --------
        exit_price = trade["exit_price"]
        ax_price.text(exit_i, exit_price, arrow_symbol,
                      color=arrow_color, fontsize=12,
                      horizontalalignment="center",
                      verticalalignment="bottom" if arrow_symbol == "▲" else "top")

    ax_price.legend()

    # -------- Equity Plot --------
    equity_x = list(range(len(portfolio.equity_curve)))
    ax_equity.step(equity_x, portfolio.equity_curve, where="post", label="Equity Curve", color="blue")
    ax_equity.set_title("Equity Curve (Realized PnL Only)")
    ax_equity.set_xlabel("Candle Index")
    ax_equity.set_ylabel("Equity")

    # -------- Trade Stats --------
    total_trades = len(portfolio.trades)
    winners = sum(1 for t in portfolio.trades if t["pnl"] > 0)
    win_rate = winners / total_trades * 100 if total_trades > 0 else 0
    stats_text = f"Total Trades: {total_trades}\nWin Rate: {win_rate:.1f}%"
    ax_equity.text(
        0.02, 0.95, stats_text, transform=ax_equity.transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
    )

    ax_equity.legend()
    plt.tight_layout()
    plt.show()


def main():
    data = load_ohlc_csv(
        filepath="../data/XAUUSD_PERIOD_15_SHORT.csv",
        time_format="%Y.%m.%d %H:%M:%S"
    )

    portfolio = Portfolio(initial_cash=10_000)
    strategy = SMACrossoverStrategy(short_window=20, long_window=50)
    engine = BacktestEngine(data, portfolio, strategy)

    engine.run()

    plot_trade_timeline(data, portfolio)


if __name__ == "__main__":
    main()
