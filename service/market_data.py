import pyupbit
import time
from utils.logger import log

class MarketData:
    def __init__(self, ticker):
        self.ticker = ticker

    def get_prices(self, retry=5):
        """
        5분 간격으로 최근 시세 데이터를 가져옴
        최대 retry 횟수까지 시도하며, 실패하면 예외를 발생시킴
        """
        for attempt in range(1, retry + 1):
            try:
                # 시세 데이터 요청
                df = pyupbit.get_ohlcv(self.ticker, interval="minute5", count=25)
                
                # 응답 처리
                if df is None:
                    log(f"⚠️ OHLVC 응답 없음 (None) - 시도 {attempt}/{retry}")
                elif 'close' not in df:
                    log(f"⚠️ 'close' 컬럼 없음 - 시도 {attempt}/{retry}")
                elif len(df) < 20:
                    log(f"⚠️ 캔들 개수 부족 ({len(df)}개) - 시도 {attempt}/{retry}")
                else:
                    log(f"✅ 시세 데이터 정상 수신 (캔들 {len(df)}개)")
                    return df['close'].tolist()  # 종가 데이터 반환

            except Exception as e:
                log(f"❌ 데이터 가져오기 실패 - {str(e)} - 시도 {attempt}/{retry}")
                
            time.sleep(3)  # 잠시 대기 후 재시도

        # 모든 시도 후에도 데이터를 못 가져오면 예외 발생
        raise Exception("시세 데이터를 충분히 가져오지 못했습니다.")
