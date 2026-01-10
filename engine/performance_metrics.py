def compute_performance_metrics(trades, equity_curve):
    metrics = {
        "trades": 0,
        "winrate": 0.0,
        "total_pnl": 0.0,
        "avg_win": 0.0,
        "avg_loss": 0.0,
        "max_drawdown": 0.0,
    }

    if not trades:
        return metrics

    profits = [t.profit for t in trades]
    wins = [p for p in profits if p > 0]
    losses = [p for p in profits if p < 0]

    metrics["trades"] = len(trades)
    metrics["total_pnl"] = sum(profits)
    metrics["winrate"] = len(wins) / len(trades) * 100.0
    metrics["avg_win"] = sum(wins) / len(wins) if wins else 0.0
    metrics["avg_loss"] = sum(losses) / len(losses) if losses else 0.0

    # Max Drawdown (Equity-based)
    peak = equity_curve[0]
    max_dd = 0.0

    for equity in equity_curve:
        peak = max(peak, equity)
        dd = equity - peak
        max_dd = min(max_dd, dd)

    metrics["max_drawdown"] = max_dd

    return metrics
