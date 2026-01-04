# Python Trading Backtesting

Clean, minimal Python examples for trading strategy backtesting with a focus on
**clear architecture, reproducibility, and risk-aware evaluation**.

This repository is intentionally kept simple and realistic — no hype, no curve fitting,
no promises of profitability.

---

## Purpose

The goal of this project is to demonstrate how trading and backtesting systems can be
implemented in a **clean, maintainable, and extensible way** using Python.

The focus is on:
- proper separation of concerns
- realistic backtesting flow
- transparent performance evaluation

This repository is meant as a **technical reference**, not a turnkey trading system.

---

## Scope

Included in this repository:

- Candle-by-candle backtesting engine
- Simple example strategies (signal-only logic)
- Portfolio and position management
- Basic risk & performance metrics
- CSV-based OHLC data handling

Explicitly **out of scope**:
- Machine Learning / Reinforcement Learning
- Hyperparameter optimization
- Curve fitting
- Live trading without additional safeguards

---

## Project Structure
python-trading-backtesting/
├── backtesting/
│   ├── engine.py        # Backtest loop (candle-by-candle execution)
│   ├── portfolio.py     # Position, PnL & equity tracking
│   └── metrics.py       # Performance and risk metrics
├── strategies/
│   └── sma_crossover.py # Example strategy (signal-only logic)
├── data/
│   └── sample_ohlc.csv  # Example OHLC data
├── run_backtest.py      # Entry point
├── requirements.txt
└── README.

---

## Example Strategy

Currently included example:

- Simple SMA crossover (long-only)
- One open position at a time
- Market orders
- Fixed position size

The strategy is deliberately simple to keep the focus on **architecture and evaluation**,
not on strategy optimization.

---

## Backtesting Approach

- Iteration is performed candle by candle
- Strategies emit signals only (BUY / SELL / HOLD)
- Portfolio logic is handled separately
- Equity is updated on every bar

Metrics include:
- Total return
- Maximum drawdown
- Win rate

No slippage, commissions, or execution latency are applied by default.

---

## Design Principles

- No hidden state in strategies
- No notebooks as core logic
- Explicit data flow
- Readable and debuggable code
- Easy to extend towards live trading or ML-based setups

---

## Disclaimer

This project is provided for **educational and demonstration purposes only**.
It does **not** constitute financial advice and is **not intended for live trading**
without proper validation, testing, and risk management.

Use at your own risk.

---

## Status

🚧 Work in progress

This repository will be extended incrementally with additional examples
(e.g. alternative strategies, extended metrics, MT5 integration).

