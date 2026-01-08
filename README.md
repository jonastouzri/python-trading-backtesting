# Python Trading Backtesting

A minimal and explicit Python-based backtesting framework.

The goal of this repository is **clarity over complexity**:
- no hidden assumptions
- no performance claims
- no overengineering

This project focuses on **understanding and evaluating trading strategies** from a technical perspective, not on live trading or optimization.

---

## ✨ Features

- Minimal backtesting engine
- Explicit portfolio and trade tracking
- Single-position logic (long / flat)
- Clear separation of concerns:
  - strategy logic
  - execution loop
  - portfolio state
- Simple example strategy (SMA crossover)

---

## 📁 Project Structure

engine/  
├── engine.py # Backtesting loop and orchestration  
├── portfolio.py # Portfolio state, trades, equity, drawdown  
examples/  
└── sma_crossover.py # Example strategy implementation  

---

## 🧠 Design Philosophy

This project intentionally avoids:
- complex abstractions
- premature optimization
- black-box components

All assumptions are **explicit** and documented directly in the code.

Current assumptions include:
- single position at a time
- long-only trading
- fixed position size (1 unit)
- no transaction costs or slippage

These constraints are deliberate and serve as a clean foundation that can be extended later.

---

## 📊 Portfolio Tracking

The portfolio component keeps track of:
- executed trades
- equity curve over time
- maximum drawdown

The implementation prioritizes transparency and reproducibility over performance metrics or optimization techniques.

---

## Data

Historical market data is not included in this repository.

To run the examples, place your own CSV file in the `data/` directory
with the following columns:

- time
- open
- high
- low
- close

---

## 🚧 Current Status

This project is under active development.

Currently implemented:
- minimal portfolio implementation
- basic backtesting engine
- example SMA crossover strategy

Planned next steps:
- CSV-based historical data loading
- additional performance metrics
- further example strategies

Please refer to the GitHub Issues for details on planned work.

---

## ⚠️ Disclaimer

This project is intended for **educational and technical purposes only**.
It does **not** provide financial advice and makes **no claims about profitability or trading performance**.
