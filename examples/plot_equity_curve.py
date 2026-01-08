import matplotlib.pyplot as plt

from engine.portfolio import Portfolio
from engine.engine import BacktestEngine
from data.csv_loader import load_ohlc_csv
from examples.sma_crossover import SMACrossoverStrategy


def main():
    # CSV-Datei
    csv_path = "data/XAUUSD.csv"

    # Daten laden
    data = load_ohlc_csv(filepath=csv_path, time_format="%Y-%m-%d %H:%M:%S")

    # Portfolio initialisieren
    portfolio = Portfolio(initial_cash=10_000)

    # Strategy initialisieren
    strategy = SMACrossoverStrategy(short_window=20, long_window=50)

    # Engine initialisieren
    engine = BacktestEngine(data=data, portfolio=portfolio, strategy=strategy)

    # Backtest laufen lassen
    engine.run()

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot([candle["time"] for candle in data], portfolio.equity_curve, label="Equity Curve")
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.title("Portfolio Equity Curve")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
