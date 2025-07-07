import pyupbit
import time
import json
from strategy import get_ma, get_rsi
from utils import get_balance

with open('../config/config.json', 'r') as f:
    config = json.load(f)

upbit = pyupbit.Upbit(config["access_key"], config["secret_key"])

def auto_trade():
    ticker = config["ticker"]
    budget = config["budget"]
    interval = "minute5"
    short_window = 15
    long_window = 50

    while True:
        try:
            current_price = pyupbit.get_current_price(ticker)
            ma_short = get_ma(ticker, interval, short_window)
            ma_long = get_ma(ticker, interval, long_window)
            rsi = get_rsi(ticker, interval)

            print(f"Price: {current_price}, Short MA: {ma_short}, Long MA: {ma_long}, RSI: {rsi}")

            krw_balance = get_balance(upbit, "KRW")
            coin_balance = get_balance(upbit, ticker.split('-')[1])

            if current_price > ma_short > ma_long and rsi <= 70 and krw_balance >= budget:
                upbit.buy_market_order(ticker, budget)
                print(f"매수: {ticker} {budget}원")

            elif (ma_short < ma_long or rsi <= 30) and coin_balance > 0:
                upbit.sell_market_order(ticker, coin_balance)
                print(f"매도: {ticker} {coin_balance}개")

            time.sleep(10)

        except Exception as e:
            print(e)
            time.sleep(10)

auto_trade()