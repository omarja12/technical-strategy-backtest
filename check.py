"""Offline checks of the backtest mechanics on synthetic prices."""
import numpy as np
import pandas as pd

from backtest import (STRATEGIES, hold_between, metrics, optimise, rsi, sma_crossover,
                      strategy_returns, zscore_reversion)

idx = pd.bdate_range("2020-01-01", periods=600)
rng = np.random.default_rng(0)
price = pd.Series(100 * np.exp(np.cumsum(rng.normal(0.0003, 0.01, len(idx)))), index=idx)

# 1. No look-ahead: a position taken at t only earns from t+1.
pos = pd.Series(0.0, index=idx); pos.iloc[100] = 1.0
r = strategy_returns(price, pos, cost_bps=0)
assert r.iloc[100] == 0 and np.isclose(r.iloc[101], price.pct_change().iloc[101])

# 2. Changing the future cannot change past positions of any strategy.
future = price.copy(); future.iloc[400:] *= 3
for name, (strategy, grid) in STRATEGIES.items():
    params = {k: v[0] for k, v in grid.items()}
    a, b = strategy(price, **params), strategy(future, **params)
    if a is None:
        continue
    assert a.iloc[:400].equals(b.iloc[:400]), name

# 3. Costs: one round trip on a flat price costs exactly 2 x cost.
flat = pd.Series(100.0, index=idx[:10])
trip = pd.Series([0, 1, 1, 0, 0, 0, 0, 0, 0, 0], index=flat.index, dtype=float)
assert np.isclose(strategy_returns(flat, trip, cost_bps=10).sum(), -2 * 10 / 1e4)

# 4. Indicators and state machine.
assert rsi(price, 14).dropna().between(0, 100).all()
enter = pd.Series([False, True, False, False, False], dtype=bool)
exit_ = pd.Series([False, False, False, True, False], dtype=bool)
assert hold_between(enter, exit_).tolist() == [0, 1, 1, 0, 0]
assert sma_crossover(price, 50, 20) is None

# 5. Metrics: buy-and-hold max drawdown matches a direct computation.
hold = strategy_returns(price, pd.Series(1.0, index=idx), cost_bps=0)
eq = (1 + hold).cumprod()
assert np.isclose(metrics(hold)["Max drawdown"], (eq / eq.cummax() - 1).min())

# 6. The optimiser returns parameters from its grid.
params, _ = optimise(price, zscore_reversion, {"window": [10, 20], "entry": [1.0], "exit_": [0.0]})
assert params["window"] in (10, 20)
print("all checks passed")
