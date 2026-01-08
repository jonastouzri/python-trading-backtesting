from engine.engine import BacktestEngine
from engine.portfolio import Portfolio
from data.csv_loader import load_ohlc_csv
from examples.sma_crossover import SMACrossoverStrategy


def main():
    # Path to your XAUUSD CSV file
    csv_path = "../data/XAUUSD_PERIOD_15.csv"

    # Load historical OHLC data
    data = load_ohlc_csv(
        filepath=csv_path,
        time_format="%Y.%m.%d %H:%M:%S",  # adjust if needed
    )

    # Initialize portfolio
    portfolio = Portfolio(initial_cash=10_000)

    # Initialize strategy
    strategy = SMACrossoverStrategy(
        short_window=20,
        long_window=50,
    )

    # Initialize and run backtest
    engine = BacktestEngine(
        data=data,
        portfolio=portfolio,
        strategy=strategy,
    )

    engine.run()

    # Results
    print("Final equity:", portfolio.equity_curve[-1])
    print("Max drawdown:", portfolio.max_drawdown())
    print("Number of trades:", len(portfolio.trades))


if __name__ == "__main__":
    main()
