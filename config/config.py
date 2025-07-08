import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")
#TICKER = "KRW-BTC"  # ✅ 정확한 형식입니다.(비트코인)
#TICKER = "KRW-ZIL"  # ✅ 정확한 형식입니다.(질리카)
TICKER = "KRW-CARV"  # ✅ 정확한 형식입니다.(카브)

# 거래 기록 CSV 파일 경로 설정
TRADE_LOG_FILE = "logs/trade_history.csv"  # 실제 경로로 변경하세요

# 전략
#USE_STRATEGY = "RSIStrategy"
USE_STRATEGY = "MovingAverageRSIStrategy"
#USE_STRATEGY = "VolatilityBreakoutStrategy"
#USE_STRATEGY = "MACDStrategy"
#USE_STRATEGY = "BollingerBandStrategy"

