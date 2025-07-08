import csv
import os
from datetime import datetime

TRADE_LOG_FILE = "logs/trade_history.csv"

def init_trade_log():
    if not os.path.exists(TRADE_LOG_FILE):
        with open(TRADE_LOG_FILE, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["datetime", "action", "price", "volume"])

def log_trade(action, price, volume):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(TRADE_LOG_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([now, action, price, volume])
