# 로그 함수
import datetime
import os

# logs 디렉토리 없으면 생성
if not os.path.exists("logs"):
    os.makedirs("logs")

def log(message):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{time}] {message}"
    
    with open("logs/trade.log", "a", encoding="utf-8") as f:
        f.write(log_line + "\n")

    print(log_line)
