
# 9 algos# --- SMA Crossover ---
def sma_crossover(symbol, short_window=5, long_window=20, bar_time_len="5 mins"):
    duration = calc_duration(long_window, bar_time_len)
    df = get_historical_prices(symbol, duration=duration, barSize=bar_time_len)

    closes = df['close']
    short_sma = closes.tail(short_window).mean()
    long_sma = closes.tail(long_window).mean()

    if short_sma > long_sma:
        place_order(symbol, "buy", 1)
    elif short_sma < long_sma:
        place_order(symbol, "sell", 1)

# --- Bollinger Bands Reversion ---
def bollinger_reversion(symbol, window=20, num_std=2, bar_time_len="5 mins"):
    duration = calc_duration(window, bar_time_len)
    df = get_historical_prices(symbol, duration=duration, barSize=bar_time_len)

    closes = df['close']
    mean = closes.rolling(window).mean().iloc[-1]
    std = closes.rolling(window).std().iloc[-1]
    upper, lower = mean + num_std * std, mean - num_std * std
    current = get_price(symbol)

    if current < lower:
        place_order(symbol, "buy", 1)
    elif current > upper:
        place_order(symbol, "sell", 1)


# --- RSI Strategy ---
def rsi_strategy(symbol, window=14, overbought=70, oversold=30, bar_time_len="1 day"):
    duration = calc_duration(window, bar_time_len)
    df = get_historical_prices(symbol, duration=duration, barSize=bar_time_len)

    delta = df['close'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    latest_rsi = rsi.iloc[-1]
    if latest_rsi < oversold:
        Buy(symbol, 1)
    elif latest_rsi > overbought:
        Sell(symbol, 1)


# --- MACD Strategy ---
def macd_strategy(symbol, short_span=12, long_span=26, signal_span=9, bar_time_len="1 day"):
    # Use long_span since that's the maximum lookback needed
    duration = calc_duration(long_span, bar_time_len)
    df = get_historical_prices(symbol, duration=duration, barSize=bar_time_len)

    closes = df['close']
    short_ema = closes.ewm(span=short_span, adjust=False).mean()
    long_ema = closes.ewm(span=long_span, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_span, adjust=False).mean()

    if macd.iloc[-2] < signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1]:
        Buy(symbol, 1)
    elif macd.iloc[-2] > signal.iloc[-2] and macd.iloc[-1] < signal.iloc[-1]:
        Sell(symbol, 1)


# --- Breakout Strategy ---
def breakout_strategy(symbol, window=20, bar_time_len="1 day"):
    duration = calc_duration(window, bar_time_len)
    df = get_historical_prices(symbol, duration=duration, barSize=bar_time_len)

    highs = df['high'].rolling(window).max()
    lows = df['low'].rolling(window).min()
    close = df['close'].iloc[-1]

    if close > highs.iloc[-2]:
        Buy(symbol, 1)
    elif close < lows.iloc[-2]:
        Sell(symbol, 1)


# --- VWAP Strategy ---
def vwap_strategy(symbol, bar_time_len="5 mins"):
    # VWAP needs just 1 day of intraday data, so keep fixed 1 D
    duration = "1 D"
    df = get_historical_prices(symbol, duration=duration, barSize=bar_time_len)

    typical_price = (df['high'] + df['low'] + df['close']) / 3
    vwap = (typical_price * df['volume']).cumsum() / df['volume'].cumsum()

    close = df['close'].iloc[-1]
    latest_vwap = vwap.iloc[-1]

    if close < latest_vwap:
        Buy(symbol, 1)
    elif close > latest_vwap:
        Sell(symbol, 1)


# --- Pairs Trading ---
def pairs_trading(symbol1, symbol2, window=20, threshold=2, bar_time_len="1 day"):
    duration = calc_duration(window, bar_time_len)
    df1 = get_historical_prices(symbol1, duration=duration, barSize=bar_time_len)['close']
    df2 = yf.download(symbol2, period="6mo", interval="1d")['Close']

    spread = df1 - df2
    mean = spread.rolling(window).mean()
    std = spread.rolling(window).std()
    zscore = (spread - mean) / std

    latest_z = zscore.iloc[-1]
    if latest_z > threshold:
        Sell(symbol1, 1)
        Buy(symbol2, 1)
    elif latest_z < -threshold:
        Buy(symbol1, 1)
        Sell(symbol2, 1)


# --- Volatility Breakout ---
def volatility_breakout(symbol, window=14, multiplier=1.5, bar_time_len="1 day"):
    duration = calc_duration(window, bar_time_len)
    df = get_historical_prices(symbol, duration=duration, barSize=bar_time_len)

    high_low = df['high'] - df['low']
    high_close = (df['high'] - df['close'].shift()).abs()
    low_close = (df['low'] - df['close'].shift()).abs()

    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(window).mean()

    breakout_level = df['close'].shift(1).iloc[-1] + multiplier * atr.iloc[-1]
    breakdown_level = df['close'].shift(1).iloc[-1] - multiplier * atr.iloc[-1]
    close = df['close'].iloc[-1]

    if close > breakout_level:
        Buy(symbol, 1)
    elif close < breakdown_level:
        Sell(symbol, 1)

# Placeholder functions

def Buy(symbol, qty):
    # Executes a buy order for the given symbol and quantity
    pass

def Sell(symbol, qty):
    # Executes a sell order for the given symbol and quantity
    pass

def place_order(symbol, side, qty):
    # Executes an order (buy/sell) for the given symbol and quantity
    pass

def get_historical_prices(symbol, duration, barSize):
    # Returns a DataFrame with at least 'close', 'high', 'low', 'volume' columns
    pass

def get_price(symbol):
    # Returns the latest price of the symbol
    pass

def calc_duration(window, bar_time_len):
    # Calculates and returns the appropriate duration string

    pass
