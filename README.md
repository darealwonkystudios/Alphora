# Alphora – Algorithmic Trading Desktop App

## Description

Alphora is an experimental desktop application for algorithmic trading with Interactive Brokers (IBKR).
It provides a collection of automated trading strategies that can run on live or paper accounts through the IB Gateway client.

The app is **designed for research and testing**. It implements nine common trading strategies using technical indicators such as SMA, RSI, MACD, Bollinger Bands, VWAP, and more.

Alphora connects directly to IBKR’s local IB Gateway/TWS instance — meaning trades are executed through your own brokerage account. The app does **not** send your credentials or funds anywhere else.

---

## Strategies

Alphora implements the following nine trading strategies:

1. **SMA Crossover** – Trades when the short moving average crosses the long moving average.
2. **Bollinger Bands Reversion** – Buys when price is below the lower band, sells when above the upper band.
3. **RSI Strategy** – Uses Relative Strength Index to detect overbought/oversold conditions.
4. **MACD Strategy** – Uses exponential moving average crossovers and MACD signal line.
5. **Breakout Strategy** – Trades when price breaks out of rolling highs/lows.
6. **VWAP Strategy** – Buys when price < VWAP, sells when price > VWAP.
7. **Pairs Trading** – Goes long/short on correlated pairs when their spread deviates beyond a threshold.
8. **Volatility Breakout** – Uses ATR-based breakout/breakdown levels.
9. **Simple Intraday VWAP / Trend Strategies** – Additional intraday-style reversion/continuation trades.

---

## Parameters

Most strategies share a **common parameter set**:

* **symbol** – The stock/ETF ticker (case-sensitive).
* **window** – Lookback period in bars (e.g., 20 means last 20 bars).
* **bar_time_len** – Interval for each bar. Examples: `"1m"`, `"5m"`, `"15m"`, `"1d"`.
* **duration** – Automatically calculated from `window + bar_time_len` (via `calc_duration`). Determines how far back historical data is pulled.

### Strategy-Specific Parameters

**SMA Crossover**

* `short_window` – Short SMA length (default 5).
* `long_window` – Long SMA length (default 20).

**Bollinger Bands Reversion**

* `window` – Lookback window (default 20).
* `num_std` – Standard deviation multiplier for bands (default 2).

**RSI Strategy**

* `window` – RSI lookback (default 14).
* `overbought` – Sell threshold (default 70).
* `oversold` – Buy threshold (default 30).

**MACD Strategy**

* `short_span` – EMA short period (default 12).
* `long_span` – EMA long period (default 26).
* `signal_span` – Signal line EMA (default 9).

**Breakout Strategy**

* `window` – Lookback window for highs/lows (default 20).

**VWAP Strategy**

* Uses intraday bars only.
* No explicit `window` parameter — always computes cumulative VWAP from the session start.

**Pairs Trading**

* `symbol1`, `symbol2` – Two tickers to compare.
* `window` – Lookback for spread calculation.
* `threshold` – Z-score trigger to open long/short (default 2).

**Volatility Breakout**

* `window` – ATR lookback (default 14).
* `multiplier` – ATR multiple for breakout levels (default 1.5).

⚠️ **Important**: All parameters are **case-sensitive** (e.g., `"5m"` vs `"5 mins"` are treated differently).

---

## Legal Notice

This project is:

* **Experimental software** – It may contain bugs, errors, or incomplete features.
* **Not financial advice** – Do not rely on it for real-money trading decisions.
* **No liability** – Use at your own risk.

👉 Always test on **IBKR Paper Trading** before using with a live account.

---

## Security

* Alphora does **not store your IBKR credentials**.
* It connects only to your **local IB Gateway / TWS client**.
* Orders are executed directly via IBKR’s official API — the app has no way to “steal” or move funds outside your brokerage account.
* The exact code used by all strategies is available under the file named "Algorithms"
---

## License

MIT License – Free to use, modify, and experiment with.

---
