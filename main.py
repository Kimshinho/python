import time
from utils.logger import log
from utils.logger_trade import log_trade
from strategy.moving_average import (
    MovingAverageRSIStrategy,
    RSIStrategy,
    VolatilityBreakoutStrategy,
    MACDStrategy,
    BollingerBandStrategy
)
from service.market_data import MarketData
from service.trader import Trader  # 추가: Trader 임포트
from config.config import TICKER

def test_all_strategies_loop(interval=300):  # 기본: 1분 간격
    strategies = [
        MovingAverageRSIStrategy(),
        RSIStrategy(),
        VolatilityBreakoutStrategy(),
        MACDStrategy(),
        BollingerBandStrategy()
    ]

    market_data = MarketData(TICKER)
    trader = Trader(strategies, market_data)  # 전략 리스트와 시장 데이터를 전달

    while True:
        try:
            prices = market_data.get_prices()
            if not prices or len(prices) < 20:
                log("⚠️ 가격 데이터 부족 - 건너뜀")
                time.sleep(5)
                continue

            current_price = prices[-1]
            log(f"📊 현재가: {current_price}, 전략 평가 시작")

            for strategy in strategies:
                strategy_name = strategy.__class__.__name__
                log(f"🔍 평가 중 전략: {strategy_name}")
                buy = strategy.should_buy(prices)
                sell = strategy.should_sell(prices)

                print(f"📌 전략: {strategy_name}")
                print(f"   └ 매수 조건: {'✅' if buy else '❌'}")
                print(f"   └ 매도 조건: {'✅' if sell else '❌'}")
                print("-------------------------------------------------")

                try:
                    if buy:
                        log(f"🟢 [{strategy_name}] 매수 조건 충족")
                        krw = trader.get_balance("KRW")
                        log(f"💰 현재 KRW 잔액: {krw:,.0f}원")

                        if krw > 5000:  # 최소 매수 금액 5000 KRW 이상
                            log("📦 매수 주문 시도 중...")
                            res = trader.upbit.buy_market_order(TICKER, krw * 0.9995)
                            log(f"✅ 매수 주문 응답: {res}")
                            log_trade("buy", current_price, krw)
                        else:
                            log("🚫 매수 금액 부족. 주문 생략됨.")

                    elif sell:
                        log(f"🔴 [{strategy_name}] 매도 조건 충족")
                        coin = TICKER.split("-")[1]
                        amount = trader.get_balance(coin)
                        log(f"📦 현재 {coin} 잔액: {amount:.8f}")

                        if amount > 0.0001:  # 최소 매도 수량 0.0001 이상
                            log("📤 매도 주문 시도 중...")
                            res = trader.upbit.sell_market_order(TICKER, amount)
                            log(f"✅ 매도 주문 응답: {res}")
                            log_trade("sell", current_price, amount)
                        else:
                            log("🚫 코인 잔량 부족. 매도 생략됨.")
                except Exception as e:
                    log(f"❗ 전략 평가 오류: {e}")

        except Exception as e:
            log(f"❗ 루프 오류 발생: {str(e)}")

        print(f"\n⏳ {interval}초 후 다시 확인...\n")
        time.sleep(interval)

if __name__ == "__main__":
    test_all_strategies_loop()
