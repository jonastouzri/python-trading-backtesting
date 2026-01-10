import pandas as pd

def load_csv(path, datetime_format="%Y.%m.%d %H:%M:%S"):
    df = pd.read_csv(path, sep="\t")
    df["time"] = pd.to_datetime(df["time"], format=datetime_format)
    return df.to_dict("records")
