"""Vectorised long/flat backtests of classic technical strategies.

Every strategy maps a price series to a position series in {0, 1}. The
position decided at the close of day t is held over day t+1, so returns are
always `position.shift(1) * asset_return`: no signal ever sees the return it
trades on. A cost in basis points is charged on every change of position.
"""
from itertools import product

import numpy as np
import pandas as pd

TRADING_DAYS = 252


# --- indicators -------------------------------------------------------------

def rsi(price, window):
    """Wilder's relative strength index, 0-100."""
    delta = price.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / window, min_periods=window).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / window, min_periods=window).mean()
    return 100 - 100 / (1 + gain / loss)


def stoch_rsi(price, window):
    """Stochastic RSI, 0-1: where today's RSI sits in its own recent range."""
    r = rsi(price, window)
    low, high = r.rolling(window).min(), r.rolling(window).max()
    return (r - low) / (high - low)


def hold_between(enter, exit_):
    """Long from an `enter` signal until the next `exit_` signal, flat otherwise."""
    state = pd.Series(np.nan, index=enter.index)
    state[enter] = 1.0
    state[exit_ & ~enter] = 0.0
    return state.ffill().fillna(0.0)


# --- strategies: price -> position -------------------------------------------

def sma_crossover(price, short, long):
    if short >= long:
        return None
    return (price.rolling(short).mean() > price.rolling(long).mean()).astype(float)


def ewma_crossover(price, short, long):
    if short >= long:
        return None
    return (price.ewm(span=short).mean() > price.ewm(span=long).mean()).astype(float)


def rsi_reversion(price, window, lower, upper):
    r = rsi(price, window)
    return hold_between(r < lower, r > upper)


def stoch_rsi_reversion(price, window, lower, upper):
    s = stoch_rsi(price, window)
    return hold_between(s < lower, s > upper)


def zscore_reversion(price, window, entry, exit_):
    z = (price - price.rolling(window).mean()) / price.rolling(window).std()
    return hold_between(z < -entry, z > exit_)


def sma_rsi_hybrid(price, short, long, window, upper):
    """Trend filter plus momentum guard: long in an uptrend unless RSI is overbought."""
    trend = sma_crossover(price, short, long)
    if trend is None:
        return None
    return trend * (rsi(price, window) < upper).astype(float)


STRATEGIES = {
    "SMA crossover": (sma_crossover, {"short": [5, 10, 20, 50], "long": [50, 100, 150, 200]}),
    "EWMA crossover": (ewma_crossover, {"short": [5, 10, 20, 50], "long": [50, 100, 150, 200]}),
    "RSI": (rsi_reversion, {"window": [7, 14, 21], "lower": [20, 30, 40], "upper": [60, 70, 80]}),
    "Stochastic RSI": (stoch_rsi_reversion, {"window": [7, 14, 21], "lower": [0.1, 0.2], "upper": [0.8, 0.9]}),
    "Z-score": (zscore_reversion, {"window": [10, 20, 50], "entry": [1.0, 1.5, 2.0], "exit_": [0.0, 0.5, 1.0]}),
    "SMA + RSI": (sma_rsi_hybrid, {"short": [10, 20, 50], "long": [100, 200], "window": [14], "upper": [70, 80]}),
}


# --- evaluation ---------------------------------------------------------------

def strategy_returns(price, position, cost_bps=5.0):
    asset = price.pct_change().fillna(0.0)
    held = position.shift(1).fillna(0.0)
    trades = held.diff().abs().fillna(held.abs())
    return held * asset - trades * cost_bps / 1e4


def metrics(returns, alpha=0.05):
    returns = returns.dropna()
    equity = (1 + returns).cumprod()
    years = len(returns) / TRADING_DAYS
    cagr = equity.iloc[-1] ** (1 / years) - 1
    vol = returns.std() * np.sqrt(TRADING_DAYS)
    downside = returns[returns < 0].std() * np.sqrt(TRADING_DAYS)
    drawdown = (equity / equity.cummax() - 1).min()
    gains, losses = returns[returns > 0].sum(), -returns[returns < 0].sum()
    return {
        "CAGR": cagr,
        "Volatility": vol,
        "Sharpe": returns.mean() / returns.std() * np.sqrt(TRADING_DAYS) if returns.std() > 0 else 0.0,
        "Sortino": returns.mean() * TRADING_DAYS / downside if downside > 0 else 0.0,
        "Max drawdown": drawdown,
        "Calmar": cagr / -drawdown if drawdown < 0 else np.nan,
        "Omega": gains / losses if losses > 0 else np.inf,
        f"VaR {int((1 - alpha) * 100)}% (1 day)": -np.quantile(returns, alpha),
    }


def optimise(price, strategy, grid, objective="Sharpe", cost_bps=5.0):
    """Grid search on one price series; returns the best parameters and their score."""
    best, best_score = None, -np.inf
    keys = list(grid)
    for values in product(*grid.values()):
        params = dict(zip(keys, values))
        position = strategy(price, **params)
        if position is None:
            continue
        score = metrics(strategy_returns(price, position, cost_bps))[objective]
        if score > best_score:
            best, best_score = params, score
    return best, best_score
