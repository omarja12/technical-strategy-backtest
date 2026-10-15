"""Tune each strategy on 2010-2019, then score it on 2020 onwards against buy-and-hold."""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from backtest import STRATEGIES, metrics, optimise, strategy_returns

TICKERS = ["SPY", "QQQ", "GLD", "TLT"]
SPLIT = "2019-12-31"
COST_BPS = 5.0
DATA = Path("data/prices.csv")
OUT = Path("results")


def load_prices():
    if not DATA.exists():
        import yfinance as yf
        DATA.parent.mkdir(exist_ok=True)
        px = yf.download(TICKERS, start="2010-01-01", end="2026-01-01", auto_adjust=True, progress=False)["Close"]
        px.to_csv(DATA)
    return pd.read_csv(DATA, index_col=0, parse_dates=True)[TICKERS].dropna()


def main():
    prices = load_prices()
    OUT.mkdir(exist_ok=True)
    rows, curves = [], {}
    for ticker in TICKERS:
        price = prices[ticker]
        train = price.loc[:SPLIT]
        test_index = price.loc[SPLIT:].index[1:]
        hold = strategy_returns(price, pd.Series(1.0, index=price.index), COST_BPS).loc[test_index]
        rows.append({"Ticker": ticker, "Strategy": "Buy and hold", "Parameters": "",
                     "Train Sharpe": metrics(strategy_returns(train, pd.Series(1.0, index=train.index), COST_BPS))["Sharpe"],
                     "Time in market": 1.0, **metrics(hold)})
        curves[ticker] = {"Buy and hold": (1 + hold).cumprod()}
        for name, (strategy, grid) in STRATEGIES.items():
            params, train_score = optimise(train, strategy, grid, cost_bps=COST_BPS)
            position = strategy(price, **params)                      # indicators use past data only
            test = strategy_returns(price, position, COST_BPS).loc[test_index]
            rows.append({"Ticker": ticker, "Strategy": name,
                         "Parameters": ", ".join(f"{k}={v}" for k, v in params.items()),
                         "Train Sharpe": train_score,
                         "Time in market": position.shift(1).loc[test_index].mean(), **metrics(test)})
            curves[ticker][name] = (1 + test).cumprod()

    results = pd.DataFrame(rows)
    results.to_csv(OUT / "test_results.csv", index=False)

    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    for ax, ticker in zip(axes.flat, TICKERS):
        for name, curve in curves[ticker].items():
            ax.plot(curve, lw=2.5 if name == "Buy and hold" else 1, color="black" if name == "Buy and hold" else None, label=name)
        ax.set_title(f"{ticker}: growth of 1, test period")
        ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "equity_curves.png", dpi=110)

    cols = ["Ticker", "Strategy", "Parameters", "Train Sharpe", "Sharpe", "CAGR", "Max drawdown", "Time in market"]
    table = results[cols].copy()
    for c in ["CAGR", "Max drawdown", "Time in market"]:
        table[c] = table[c].map(lambda v: f"{v:.1%}")
    for c in ["Train Sharpe", "Sharpe"]:
        table[c] = table[c].map(lambda v: f"{v:.2f}")
    (OUT / "test_results.md").write_text(table.to_markdown(index=False), encoding="utf-8")
    print(table.to_string(index=False))


if __name__ == "__main__":
    main()
