import csv
from datetime import datetime
from typing import List, Dict


def load_ohlc_csv(
    filepath: str,
    time_format: str = "%Y-%m-%d %H:%M:%S",
) -> List[Dict]:
    """
    Load OHLC data from a CSV file.

    Expected columns:
    - time
    - open
    - high
    - low
    - close

    Parameters
    ----------
    filepath : str
        Path to CSV file.
    time_format : str
        Datetime format used in the 'time' column.

    Returns
    -------
    List[Dict]
        List of candles with parsed values.
    """
    candles = []

    with open(filepath, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        required_columns = {"time", "open", "high", "low", "close"}
        if not required_columns.issubset(reader.fieldnames):
            raise ValueError(
                f"CSV file must contain columns: {required_columns}"
            )

        for row in reader:
            candles.append(
                {
                    "time": datetime.strptime(row["time"], time_format),
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                }
            )

    return candles
