import pyupbit
import time
from config.config import ACCESS_KEY, SECRET_KEY, TICKER
from strategy.moving_average import (
    MovingAverageRSIStrategy,
    RSIStrategy,
    VolatilityBreakoutStrategy,
    MACDStrategy,
    BollingerBandStrategy
)
from utils.logger import log
from utils.logger_trade import init_trade_log, log_trade

class Trader:
    def __init__(self, strategies, market_data):
        self.strategies = strategies  # 전략 리스트
        self.market_data = market_data  # 시세 데이터
        self.upbit = pyupbit.Upbit(ACCESS_KEY, SECRET_KEY)
        self.current_position = None  # 현재 매수한 전략을 추적
        init_trade_log()
        log("🚀 자동매매 시작됨")

    def get_balance(self, currency):
        try:
            balances = self.upbit.get_balances()
            for b in balances:
                if b['currency'] == currency:
                    return float(b['balance'])
        except Exception as e:
            log(f"❌ 잔고 조회 실패: {e}")
        return 0

    def place_order_with_retry(self, order_function, ticker, amount, retries=3):
        for _ in range(retries):
            try:
                return order_function(ticker, amount)
            except Exception as e:
                log(f"❌ 주문 실패: {e}")
                time.sleep(3)
        return None

    def run(self):
        while True:
            try:
                prices = self.market_data.get_prices()
                if not prices or len(prices) < 20:
                    log("⚠️ 가격 데이터 부족 - 건너뜀")
                    time.sleep(5)
                    continue

                current_price = prices[-1]
                log(f"📊 현재가: {current_price}, 전략 평가 시작")

                # 매수 중인 전략이 있다면, 해당 전략 외에는 매수, 매도 금지
                if self.current_position:
                    log(f"💡 현재 매수 중인 전략: {self.current_position}")
                else:
                    log("❗ 현재 매수 중인 전략이 없습니다.")

                for strategy in self.strategies:
                    strategy_name = strategy.__class__.__name__
                    log(f"🔍 평가 중 전략: {strategy_name}")

                    try:
                        # 매수 중인 전략이 있으면, 매수는 그 전략에서만
                        if self.current_position and self.current_position != strategy_name:
                            log(f"⛔ [{strategy_name}] 현재 다른 전략이 매수 중이므로 거래 불가")
                            continue  # 다른 전략이 매수 중이면, 해당 전략은 매수할 수 없음

                        # 매수 조건 평가
                        if strategy.should_buy(prices) and not self.current_position:
                            log(f"🟢 [{strategy_name}] 매수 조건 충족")
                            krw = self.get_balance("KRW")
                            log(f"💰 현재 KRW 잔액: {krw:,.0f}원")

                            if krw > 5000:  # 최소 매수 금액 5000 KRW 이상
                                try:
                                    order_amount = krw * 0.9995  # 잔액의 99.95% 매수
                                    res = self.place_order_with_retry(self.upbit.buy_market_order, TICKER, order_amount)
                                    if res:
                                        self.current_position = strategy_name  # 매수한 전략 기록
                                        log(f"✅ [{strategy_name}] 매수 주문 성공")
                                        log_trade("buy", current_price, order_amount)
                                    else:
                                        log(f"❌ [{strategy_name}] 매수 주문 실패")
                                except Exception as e:
                                    log(f"❌ 매수 실패: {e}")
                            else:
                                log("🚫 매수 금액 부족. 주문 생략됨.")

                        # 매도 조건 평가 (현재 매수한 전략에서만 매도)
                        elif strategy.should_sell(prices) and self.current_position == strategy_name:
                            log(f"🔴 [{strategy_name}] 매도 조건 충족")
                            coin = TICKER.split("-")[1]
                            amount = self.get_balance(coin)
                            log(f"📦 현재 {coin} 잔액: {amount:.8f}")

                            if amount > 0.0001:  # 최소 매도 수량 0.0001 이상
                                try:
                                    res = self.place_order_with_retry(self.upbit.sell_market_order, TICKER, amount)
                                    if res:
                                        self.current_position = None  # 매도 후 전략 해제
                                        log(f"✅ [{strategy_name}] 매도 주문 성공")
                                        log_trade("sell", current_price, amount)
                                    else:
                                        log(f"❌ [{strategy_name}] 매도 주문 실패")
                                except Exception as e:
                                    log(f"❌ 매도 실패: {e}")
                            else:
                                log("🚫 보유 코인 부족. 매도 생략됨.")
                        else:
                            log(f"⛔ [{strategy_name}] 조건 불충족 – 거래 없음")

                    except Exception as e:
                        log(f"❗ 전략 평가 오류: {e}")

            except Exception as e:
                log(f"❗ 루프 오류 발생: {str(e)}")

            time.sleep(5)  # 5초 대기 후 재시도
