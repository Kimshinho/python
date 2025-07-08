from strategy.base_strategy import BaseStrategy
from utils.logger import log

# ✅ Moving Average + RSI 전략
class MovingAverageRSIStrategy(BaseStrategy):
    def __init__(self, rsi_period=14, rsi_buy_threshold=35, rsi_sell_threshold=70):
        """
        전략 초기화 메소드
        :param rsi_period: RSI 계산 기간
        :param rsi_buy_threshold: 매수 기준 RSI 임계값
        :param rsi_sell_threshold: 매도 기준 RSI 임계값
        """
        self.rsi_period = rsi_period
        self.rsi_buy_threshold = rsi_buy_threshold
        self.rsi_sell_threshold = rsi_sell_threshold  # 매도 기준 임계값 추가

    def calculate_rsi(self, prices):
        """
        RSI 계산 함수
        :param prices: 가격 리스트
        :return: 계산된 RSI 값
        """
        deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        avg_gain = sum(gains[:self.rsi_period]) / self.rsi_period
        avg_loss = sum(losses[:self.rsi_period]) / self.rsi_period
        for i in range(self.rsi_period, len(deltas)):
            gain = gains[i]
            loss = losses[i]
            avg_gain = (avg_gain * (self.rsi_period - 1) + gain) / self.rsi_period
            avg_loss = (avg_loss * (self.rsi_period - 1) + loss) / self.rsi_period
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def should_buy(self, prices):
        """
        매수 조건 체크
        :param prices: 가격 리스트
        :return: 매수 조건 만족 여부 (True/False)
        """
        if len(prices) < 20: return False
        ma5 = sum(prices[-5:]) / 5  # 5일 이동평균
        ma20 = sum(prices[-20:]) / 20  # 20일 이동평균
        rsi = self.calculate_rsi(prices)  # RSI 계산
        log(f"[MA+RSI 매수] MA5: {ma5:.2f}, MA20: {ma20:.2f}, RSI: {rsi:.2f}")
        # MA5가 MA20보다 크고, RSI가 매수 임계값 미만일 경우 매수
        return ma5 > ma20 and rsi < self.rsi_buy_threshold

    def should_sell(self, prices):
        """
        매도 조건 체크
        :param prices: 가격 리스트
        :return: 매도 조건 만족 여부 (True/False)
        """
        if len(prices) < 20: return False
        ma5 = sum(prices[-5:]) / 5  # 5일 이동평균
        ma20 = sum(prices[-20:]) / 20  # 20일 이동평균
        rsi = self.calculate_rsi(prices)  # RSI 계산
        log(f"[MA+RSI 매도] MA5: {ma5:.2f}, MA20: {ma20:.2f}, RSI: {rsi:.2f}")
        # MA5가 MA20보다 작거나, RSI가 매도 임계값을 초과할 경우 매도
        return ma5 < ma20 or rsi > self.rsi_sell_threshold


# ✅ RSI 단독 전략
class RSIStrategy(BaseStrategy):
    def __init__(self, period=14, buy_threshold=30, sell_threshold=70):
        """
        RSI 전략 초기화
        :param period: RSI 계산 기간
        :param buy_threshold: 매수 기준 RSI 임계값
        :param sell_threshold: 매도 기준 RSI 임계값
        """
        self.period = period
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold

    def calculate_rsi(self, prices):
        """
        RSI 계산 함수
        :param prices: 가격 리스트
        :return: 계산된 RSI 값
        """
        deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
        gains = [d if d > 0 else 0 for d in deltas]
        losses = [-d if d < 0 else 0 for d in deltas]
        avg_gain = sum(gains[:self.period]) / self.period
        avg_loss = sum(losses[:self.period]) / self.period
        for i in range(self.period, len(deltas)):
            gain = gains[i]
            loss = losses[i]
            avg_gain = (avg_gain * (self.period - 1) + gain) / self.period
            avg_loss = (avg_loss * (self.period - 1) + loss) / self.period
        if avg_loss == 0:
            return 100
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    def should_buy(self, prices):
        """
        매수 조건 체크
        :param prices: 가격 리스트
        :return: 매수 조건 만족 여부 (True/False)
        """
        if len(prices) < self.period: return False
        rsi = self.calculate_rsi(prices)
        log(f"[RSI 매수] RSI: {rsi:.2f}")
        return rsi < self.buy_threshold

    def should_sell(self, prices):
        """
        매도 조건 체크
        :param prices: 가격 리스트
        :return: 매도 조건 만족 여부 (True/False)
        """
        if len(prices) < self.period: return False
        rsi = self.calculate_rsi(prices)
        log(f"[RSI 매도] RSI: {rsi:.2f}")
        return rsi > self.sell_threshold


# ✅ 변동성 돌파 전략
class VolatilityBreakoutStrategy(BaseStrategy):
    def __init__(self, k=0.5):
        """
        변동성 돌파 전략 초기화
        :param k: 변동성 돌파 기준 비율
        """
        self.k = k

    def should_buy(self, prices):
        """
        매수 조건 체크 (변동성 돌파 전략)
        :param prices: 가격 리스트
        :return: 매수 조건 만족 여부 (True/False)
        """
        if len(prices) < 2: return False
        yesterday = prices[-2]
        today = prices[-1]
        target = yesterday + (abs(prices[-2] - prices[-3]) * self.k)
        log(f"[돌파 매수] 현재가: {today}, 목표가: {target}")
        return today > target

    def should_sell(self, prices):
        """
        매도 조건 체크 (변동성 돌파 전략)
        :param prices: 가격 리스트
        :return: 매도 조건 만족 여부 (True/False)
        """
        return False  # 단순 버전에서는 매도 전략 미포함


# ✅ MACD 전략
class MACDStrategy(BaseStrategy):
    def __init__(self, short=12, long=26, signal=9):
        """
        MACD 전략 초기화
        :param short: 단기 EMA 기간
        :param long: 장기 EMA 기간
        :param signal: MACD 신호선 기간
        """
        self.short = short
        self.long = long
        self.signal = signal

    def calculate_macd(self, prices):
        """
        MACD 및 신호선 계산 함수
        :param prices: 가격 리스트
        :return: MACD 및 신호선 값
        """
        if len(prices) < self.long + self.signal: return None, None
        ema_short = sum(prices[-self.short:]) / self.short
        ema_long = sum(prices[-self.long:]) / self.long
        macd = ema_short - ema_long
        signal_line = sum([macd] * self.signal) / self.signal
        return macd, signal_line

    def should_buy(self, prices):
        """
        매수 조건 체크 (MACD 전략)
        :param prices: 가격 리스트
        :return: 매수 조건 만족 여부 (True/False)
        """
        macd, signal = self.calculate_macd(prices)
        if macd is None: return False
        log(f"[MACD 매수] MACD: {macd:.4f}, Signal: {signal:.4f}")
        return macd > signal

    def should_sell(self, prices):
        """
        매도 조건 체크 (MACD 전략)
        :param prices: 가격 리스트
        :return: 매도 조건 만족 여부 (True/False)
        """
        macd, signal = self.calculate_macd(prices)
        if macd is None: return False
        log(f"[MACD 매도] MACD: {macd:.4f}, Signal: {signal:.4f}")
        return macd < signal


# ✅ 볼린저 밴드 전략
class BollingerBandStrategy(BaseStrategy):
    def __init__(self, window=20, num_std_dev=2):
        """
        볼린저 밴드 전략 초기화
        :param window: 이동 평균 계산 기간
        :param num_std_dev: 표준편차 기준
        """
        self.window = window
        self.num_std_dev = num_std_dev

    def should_buy(self, prices):
        """
        매수 조건 체크 (볼린저 밴드 전략)
        :param prices: 가격 리스트
        :return: 매수 조건 만족 여부 (True/False)
        """
        if len(prices) < self.window: return False
        window_prices = prices[-self.window:]
        mean = sum(window_prices) / self.window
        std = (sum([(p - mean) ** 2 for p in window_prices]) / self.window) ** 0.5
        lower_band = mean - self.num_std_dev
