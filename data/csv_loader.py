import csv
from datetime import datetime
from typing import List, Dict

def load_ohlc_csv(filepath: str, time_format: str = "%Y.%m.%d %H:%M:%S") -> List[Dict]:
    candles = []
    with open(filepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile, delimiter="\t")  # Tab-delimited

        required_columns = {"time", "open", "high", "low", "close"}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(f"CSV file must contain columns: {required_columns}")

        for row in reader:
            candles.append({
                "time": datetime.strptime(row["time"], time_format),
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"])
            })

    return candles