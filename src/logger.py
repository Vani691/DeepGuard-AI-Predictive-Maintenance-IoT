import csv
from datetime import datetime
import os

LOG_FILE = "logs/log.csv"

def init_log():
    os.makedirs("logs", exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "timestamp", "engine_id", "cycle", "s2", "s3", "s4",
                "prediction", "probability", "anomaly"
            ])

def log_data(data, prediction, probability, anomaly):
    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            datetime.now(), data["id"], data["cycle"], 
            data["s2"], data["s3"], data["s4"],
            prediction, probability, anomaly
        ])