import pyupbit

def get_ma(ticker, interval, window):
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=window)
    return df['close'].mean()

def get_rsi(ticker, interval="minute5", period=14):
    df = pyupbit.get_ohlcv(ticker, interval=interval, count=period + 1)
    delta = df['close'].diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    avg_gain = up.rolling(window=period).mean()
    avg_loss = abs(down.rolling(window=period).mean())
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]