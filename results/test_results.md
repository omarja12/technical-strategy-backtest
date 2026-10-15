| Ticker   | Strategy       | Parameters                              |   Train Sharpe |   Sharpe | CAGR   | Max drawdown   | Time in market   |
|:---------|:---------------|:----------------------------------------|---------------:|---------:|:-------|:---------------|:-----------------|
| SPY      | Buy and hold   |                                         |           0.92 |     0.78 | 15.0%  | -33.7%         | 100.0%           |
| SPY      | SMA crossover  | short=50, long=150                      |           0.94 |     0.58 | 8.5%   | -33.7%         | 77.6%            |
| SPY      | EWMA crossover | short=50, long=150                      |           0.81 |     0.43 | 5.7%   | -30.1%         | 80.2%            |
| SPY      | RSI            | window=21, lower=30, upper=80           |           1.07 |     0.78 | 15.0%  | -33.7%         | 100.0%           |
| SPY      | Stochastic RSI | window=7, lower=0.2, upper=0.9          |           0.67 |     0.84 | 12.5%  | -18.3%         | 50.8%            |
| SPY      | Z-score        | window=10, entry=1.5, exit_=1.0         |           0.84 |     0.21 | 2.2%   | -30.5%         | 32.3%            |
| SPY      | SMA + RSI      | short=50, long=100, window=14, upper=70 |           0.9  |     0.45 | 6.0%   | -34.3%         | 68.8%            |
| QQQ      | Buy and hold   |                                         |           1.03 |     0.85 | 20.1%  | -35.1%         | 100.0%           |
| QQQ      | SMA crossover  | short=50, long=150                      |           0.93 |     0.79 | 15.2%  | -28.6%         | 77.1%            |
| QQQ      | EWMA crossover | short=20, long=200                      |           0.9  |     0.83 | 15.3%  | -29.2%         | 79.6%            |
| QQQ      | RSI            | window=14, lower=30, upper=80           |           1.21 |     0.85 | 18.0%  | -35.1%         | 67.3%            |
| QQQ      | Stochastic RSI | window=7, lower=0.2, upper=0.9          |           0.83 |     0.96 | 17.5%  | -27.1%         | 52.2%            |
| QQQ      | Z-score        | window=10, entry=1.0, exit_=1.0         |           0.93 |     0.27 | 3.4%   | -29.3%         | 36.7%            |
| QQQ      | SMA + RSI      | short=50, long=100, window=14, upper=80 |           0.9  |     0.86 | 16.5%  | -28.6%         | 75.5%            |
| GLD      | Buy and hold   |                                         |           0.25 |     1.13 | 18.6%  | -22.0%         | 100.0%           |
| GLD      | SMA crossover  | short=50, long=150                      |           0.41 |     1.09 | 16.2%  | -18.5%         | 73.4%            |
| GLD      | EWMA crossover | short=50, long=150                      |           0.39 |     1.03 | 15.4%  | -22.4%         | 77.7%            |
| GLD      | RSI            | window=21, lower=40, upper=60           |           0.37 |     0.56 | 4.5%   | -14.0%         | 30.8%            |
| GLD      | Stochastic RSI | window=14, lower=0.2, upper=0.9         |          -0.05 |     0.54 | 6.0%   | -20.2%         | 53.9%            |
| GLD      | Z-score        | window=20, entry=1.5, exit_=1.0         |           0.18 |     0.91 | 7.7%   | -12.3%         | 31.6%            |
| GLD      | SMA + RSI      | short=50, long=200, window=14, upper=80 |           0.13 |     1.06 | 14.9%  | -23.5%         | 72.9%            |
| TLT      | Buy and hold   |                                         |           0.58 |    -0.18 | -4.4%  | -48.4%         | 100.0%           |
| TLT      | SMA crossover  | short=20, long=100                      |           0.66 |     0.14 | 1.0%   | -17.9%         | 45.2%            |
| TLT      | EWMA crossover | short=5, long=200                       |           0.54 |    -0.21 | -2.8%  | -34.3%         | 38.5%            |
| TLT      | RSI            | window=21, lower=40, upper=80           |           0.65 |    -0.12 | -3.0%  | -48.4%         | 95.9%            |
| TLT      | Stochastic RSI | window=14, lower=0.2, upper=0.8         |           0.82 |    -0.18 | -2.9%  | -34.9%         | 47.3%            |
| TLT      | Z-score        | window=10, entry=1.5, exit_=0.0         |           0.6  |    -0.13 | -1.8%  | -32.9%         | 34.5%            |
| TLT      | SMA + RSI      | short=20, long=100, window=14, upper=70 |           0.69 |     0.13 | 0.9%   | -16.0%         | 43.4%            |