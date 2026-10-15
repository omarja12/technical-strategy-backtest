# Technical Strategy Backtest

Do classic technical trading rules beat buy-and-hold once they are tuned on one period and judged on the next? Six long/flat strategies are tuned on 2010-2019 and tested on 2020-2025 on four ETFs (US large caps, Nasdaq-100, gold, long Treasuries), with a 5 bp cost on every position change.

## Strategies

| Strategy | Long when | Grid |
|---|---|---|
| SMA crossover | short SMA above long SMA | short 5-50, long 50-200 |
| EWMA crossover | short EWMA above long EWMA | same |
| RSI | from RSI below `lower` until RSI above `upper` | window 7/14/21 |
| Stochastic RSI | same rule on the stochastic RSI | window 7/14/21 |
| Z-score | from price z-score below `−entry` until above `exit` | window 10/20/50 |
| SMA + RSI | uptrend (SMA crossover) and RSI below `upper` | trend filter with overbought guard |

Each strategy's parameters maximise its Sharpe ratio on 2010-2019; those parameters are then applied unchanged from 2020.

## Out-of-sample results (2020-2025)

| | SPY | QQQ | GLD | TLT |
|---|---|---|---|---|
| **Buy and hold**: Sharpe / CAGR / max drawdown | 0.78 / 15.0% / −33.7% | 0.85 / 20.1% / −35.1% | 1.13 / 18.6% / −22.0% | −0.18 / −4.4% / −48.4% |
| Best strategy by test Sharpe | Stochastic RSI: 0.84 / 12.5% / −18.3% | Stochastic RSI: 0.96 / 17.5% / −27.1% | SMA crossover: 1.09 / 16.2% / −18.5% | SMA crossover: 0.14 / 1.0% / −17.9% |

Full table: [`results/test_results.md`](results/test_results.md) · equity curves: [`results/equity_curves.png`](results/equity_curves.png)

- **No strategy beat buy-and-hold on return** for SPY, QQQ or gold. Being out of the market 20-50% of the time cost more in missed rallies than it saved in drawdowns.
- **Some rules improved risk, not return.** Stochastic RSI raised Sharpe slightly on SPY and QQQ and almost halved SPY's maximum drawdown, with half the time in the market.
- **Trend filters helped in a bear market.** On long Treasuries, which fell 48% peak to trough, the SMA crossover and SMA + RSI cut the drawdown to −16% to −18% and turned a loss into a small gain.
- **In-sample Sharpe did not predict out-of-sample Sharpe**: the parameters that won 2010-2019 often ranked mid-table afterwards. The mean-reversion z-score rule was the weakest everywhere.

## Design

- `backtest.py`: indicators, strategies, costs and metrics, all vectorised with pandas. A position decided at the close of day *t* earns day *t+1*'s return, so no signal sees the return it trades on.
- `run.py`: tunes on the training period, scores the test period, and writes `results/`.
- `check.py`: tests the mechanics on synthetic prices. No look-ahead, and changing future prices never changes past positions of any strategy. One round trip on a flat price costs exactly two costs. RSI stays within bounds. The hold state machine and the drawdown maths are exact.

Metrics: CAGR, volatility, Sharpe, Sortino, maximum drawdown, Calmar, Omega and 1-day 95% historical VaR.

## Run it

```bash
pip install -r requirements.txt
python check.py
python run.py
```

`data/prices.csv` is a snapshot of Yahoo Finance adjusted closes (2010 to 2025); delete it to download afresh. The GitHub Actions workflow runs the checks and the backtest on every push.
