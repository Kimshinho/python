import pandas as pd
import matplotlib.pyplot as plt
from config.config import TRADE_LOG_FILE  # 거래 기록 CSV 파일 경로 (config에 설정)

def analyze_profit(csv_path=TRADE_LOG_FILE, show_chart=True):
    try:
        # 거래 기록 CSV 파일 읽기
        df = pd.read_csv(csv_path)
        df["datetime"] = pd.to_datetime(df["datetime"])
        df = df.sort_values("datetime")

        trades = []
        position = None

        # 매수/매도 쌍 처리
        for _, row in df.iterrows():
            if row["action"] == "buy":
                position = {
                    "buy_price": row["price"],
                    "volume": row["volume"],
                    "datetime": row["datetime"]
                }
            elif row["action"] == "sell" and position:
                profit = (row["price"] - position["buy_price"]) * float(position["volume"])
                trades.append({
                    "buy_time": position["datetime"],
                    "sell_time": row["datetime"],
                    "buy_price": position["buy_price"],
                    "sell_price": row["price"],
                    "volume": position["volume"],
                    "profit": profit,
                    "return_rate": (row["price"] - position["buy_price"]) / position["buy_price"] * 100
                })
                position = None

        # 거래 결과 데이터프레임 생성
        result_df = pd.DataFrame(trades)

        if result_df.empty:
            print("❗ 분석할 거래 기록이 없습니다.")
            return

        # 📊 수익률 변화 그래프
        if show_chart:
            plt.figure(figsize=(10, 5))
            plt.plot(result_df["sell_time"], result_df["return_rate"], marker='o', label="Return (%)")
            plt.axhline(0, color='red', linestyle='--')
            plt.title("📈 거래 수익 변화 그래프")
            plt.xlabel("판매 시각")
            plt.ylabel("수익률 (%)")
            plt.grid(True)
            plt.legend()
            plt.tight_layout()
            plt.show()

            # 🟩🟥 손익 비율 파이 차트
            wins = (result_df["profit"] > 0).sum()
            losses = (result_df["profit"] <= 0).sum()
            plt.figure(figsize=(5, 5))
            plt.pie([wins, losses], labels=["Profit", "Loss"], autopct='%1.1f%%', colors=["green", "red"])
            plt.title("🟩🟥 손익 비율")
            plt.tight_layout()
            plt.show()

        # 📊 수익 분석 요약 통계 (한글로 출력)
        summary = {
            "총 거래 횟수": len(result_df),
            "총 수익 (KRW)": result_df["profit"].sum(),
            "평균 수익 (KRW)": result_df["profit"].mean(),
            "승률 (%)": (result_df["profit"] > 0).sum() / len(result_df) * 100
        }

        print("\n📊 **수익 분석 요약 통계**")
        for k, v in summary.items():
            print(f"{k}: {v:,.2f} 원" if isinstance(v, float) else f"{k}: {v} 건")

    except FileNotFoundError:
        print(f"❌ 파일을 찾을 수 없습니다: {csv_path}")
